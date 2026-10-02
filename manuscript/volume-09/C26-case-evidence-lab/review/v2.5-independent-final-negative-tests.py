#!/usr/bin/env python3
"""Independent, unannounced near-neighbour tests for C23 v2.5.

This file is deliberately outside the author run package.  Semantic attacks
start from S01, reseal every changed record, rebuild the complete authority
root, and temporarily pin that legitimate new root.  The secure contract is
defined from the chapter's evidence invariants, not from fixture ``expected``
labels (which the production input does not contain in any event).
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--authority-root", required=True)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    runner = load(Path(args.runner), "c23_v25_independent_final_runner")
    base = runner.strict_json_loads(Path(args.input).read_text())
    authority = runner.strict_json_loads(Path(args.authority_root).read_text())
    baseline = runner.evaluate(copy.deepcopy(base), copy.deepcopy(authority))

    def seal(record):
        record["record_digest"] = runner.digest(
            {key: value for key, value in record.items() if key != "record_digest"}
        )

    def scenario(doc, scenario_id="S01"):
        return next(x for x in doc["scenarios"] if x["scenario_id"] == scenario_id)

    def record(doc, registry, key, value):
        return next(x for x in doc["registries"][registry] if x[key] == value)

    def artifact(doc, artifact_id):
        return record(doc, "artifact_registry", "artifact_id", artifact_id)

    def repin(doc, root):
        root["registries"] = copy.deepcopy(doc["registries"])
        root["suite_manifest"] = runner.suite_manifest(doc["suite"], doc["scenarios"])
        root["root_digest"] = runner.digest(runner.root_payload(root))
        runner.PINNED_AUTHORITY_ROOT_DIGEST = root["root_digest"]

    id_keys = {
        "case_identity_registry": "identity_id",
        "authorization_registry": "authorization_id",
        "source_registry": "source_id",
        "redaction_registry": "redaction_id",
        "publication_registry": "publication_id",
        "reviewer_registry": "reviewer_id",
        "author_assignment_registry": "assignment_id",
        "environment_registry": "environment_id",
        "d21_registry": "d21_id",
        "migration_registry": "migration_id",
    }

    def extra_unprojected(registry):
        def mutate(doc):
            source = copy.deepcopy(doc["registries"][registry][0])
            key = id_keys[registry]
            source[key] = source[key] + ".UNPROJECTED"
            seal(source)
            doc["registries"][registry].append(source)
        return mutate

    def late_failure_log_after_d21(doc):
        item = artifact(doc, "ARTIFACT.FAILURE.S01")
        item["recorded_at"] = "2026-09-30T11:57:00Z"
        seal(item)

    def trial_after_d21(doc):
        item = record(doc, "trial_registry", "trial_record_id", "TRIAL.RECORD.S01.01")
        item["recorded_at"] = "2026-09-30T11:56:10Z"
        seal(item)

    def review_before_d21(doc):
        item = record(doc, "reviewer_registry", "reviewer_id", "REVIEWER.S01")
        item["reviewed_at"] = "2026-09-30T11:55:59Z"
        seal(item)

    def authorization_after_trial(doc):
        item = record(doc, "authorization_registry", "authorization_id", "AUTHORIZATION.S01")
        item["valid_from"] = "2026-09-30T11:53:30Z"
        seal(item)

    def failed_trial_without_failure_ref(doc):
        item = record(doc, "trial_registry", "trial_record_id", "TRIAL.RECORD.S01.02")
        item["failure_ref"] = "NONE"
        seal(item)

    def pass_trial_with_failure_ref(doc):
        item = record(doc, "trial_registry", "trial_record_id", "TRIAL.RECORD.S01.01")
        item["failure_ref"] = "FAILURE.S01.01"
        seal(item)

    def failure_log_payload_mismatch(doc):
        item = artifact(doc, "ARTIFACT.FAILURE.S01")
        item["payload"]["trial_id"] = "TRIAL.S01.01"
        item["content_digest"] = runner.digest(item["payload"])
        seal(item)

    def effect_external_lie(doc):
        item = record(doc, "effect_registry", "effect_id", "EFFECT.S01")
        item["external"] = True
        item["receipt"]["external"] = True
        item["readback"]["external"] = True
        item["receipt_digest"] = runner.digest(item["receipt"])
        item["readback_digest"] = runner.digest(item["readback"])
        seal(item)

    def effect_external_write(doc):
        item = record(doc, "effect_registry", "effect_id", "EFFECT.S01")
        item["effect_kind"] = "EXTERNAL_WRITE"
        item["external"] = True
        item["receipt"].update(effect_kind="EXTERNAL_WRITE", external=True, status="APPLIED")
        item["readback"].update(effect_kind="EXTERNAL_WRITE", external=True, status="APPLIED")
        item["receipt_digest"] = runner.digest(item["receipt"])
        item["readback_digest"] = runner.digest(item["readback"])
        seal(item)

    def effect_unauthorized(doc):
        item = record(doc, "effect_registry", "effect_id", "EFFECT.S01")
        item["authorized"] = False
        item["receipt"]["authorized"] = False
        item["readback"]["authorized"] = False
        item["receipt_digest"] = runner.digest(item["receipt"])
        item["readback_digest"] = runner.digest(item["readback"])
        seal(item)

    def d21_content_disagrees(doc):
        item = artifact(doc, "ARTIFACT.TECHNICAL.S01")
        item["payload"]["state"] = "FAIL"
        item["content_digest"] = runner.digest(item["payload"])
        seal(item)

    def adapter_contract_mismatch(doc):
        item = record(doc, "migration_registry", "migration_id", "MIGRATION.S01")
        item["adapter_differences"] = [{
            "category": "TOOL_SCHEMA",
            "criticality": "NON_CRITICAL",
            "affected_contract": "MESSAGE_PROTOCOL",
            "evidence_ref": "ARTIFACT.TECHNICAL.S01",
            "owner": "PRINCIPAL.AUTHORITY.S01",
            "disposition": "ACCEPTED",
        }]
        seal(item)

    def adapter_cross_case_evidence(doc):
        item = record(doc, "migration_registry", "migration_id", "MIGRATION.S01")
        item["adapter_differences"] = [{
            "category": "TOOL_SCHEMA",
            "criticality": "NON_CRITICAL",
            "affected_contract": "TOOL_INTERFACE",
            "evidence_ref": "ARTIFACT.TECHNICAL.S17",
            "owner": "PRINCIPAL.AUTHORITY.S01",
            "disposition": "ACCEPTED",
        }]
        scenario(doc)["raw_state"]["artifact_refs"].append("ARTIFACT.TECHNICAL.S17")
        seal(item)

    def adapter_wrong_owner(doc):
        item = record(doc, "migration_registry", "migration_id", "MIGRATION.S01")
        item["adapter_differences"] = [{
            "category": "TOOL_SCHEMA",
            "criticality": "NON_CRITICAL",
            "affected_contract": "TOOL_INTERFACE",
            "evidence_ref": "ARTIFACT.TECHNICAL.S01",
            "owner": "PRINCIPAL.AUTHOR.S01",
            "disposition": "ACCEPTED",
        }]
        seal(item)

    def update_contract_pair(doc, field, value):
        if field.endswith("_digest"):
            budget_field = field.removesuffix("_digest") + "_spec"
            digest_value = runner.digest(value)
            for budget_id in ("BUDGET.BASELINE.S01", "BUDGET.CANDIDATE.S01"):
                budget = record(doc, "budget_registry", "budget_id", budget_id)
                budget[budget_field] = copy.deepcopy(value)
                budget[field] = digest_value
                seal(budget)
            migration = record(doc, "migration_registry", "migration_id", "MIGRATION.S01")
            migration["baseline_contract"][field] = digest_value
            migration["candidate_contract"][field] = digest_value
            seal(migration)
        else:
            for budget_id in ("BUDGET.BASELINE.S01", "BUDGET.CANDIDATE.S01"):
                budget = record(doc, "budget_registry", "budget_id", budget_id)
                budget[field] = value
                seal(budget)
            migration = record(doc, "migration_registry", "migration_id", "MIGRATION.S01")
            migration["baseline_contract"][field] = value
            migration["candidate_contract"][field] = value
            seal(migration)

    def forged_task_contract(doc):
        update_contract_pair(doc, "task_digest", {"task": "TASK.FORGED.S01"})

    def forged_input_contract(doc):
        update_contract_pair(doc, "input_digest", {"input": "OTHER-CASE"})

    def equal_permission_expansion(doc):
        permissions = ["READ.SYNTHETIC", "WRITE.PRODUCTION"]
        digest_value = runner.digest(permissions)
        for budget_id in ("BUDGET.BASELINE.S01", "BUDGET.CANDIDATE.S01"):
            budget = record(doc, "budget_registry", "budget_id", budget_id)
            budget["permissions"] = copy.deepcopy(permissions)
            budget["permissions_digest"] = digest_value
            seal(budget)
        migration = record(doc, "migration_registry", "migration_id", "MIGRATION.S01")
        migration["baseline_contract"]["permissions_digest"] = digest_value
        migration["candidate_contract"]["permissions_digest"] = digest_value
        seal(migration)

    def equal_production_data(doc):
        update_contract_pair(doc, "data_digest", {"dataset": "PRODUCTION_CUSTOMER", "case": "S01"})

    def equal_self_grader(doc):
        update_contract_pair(doc, "eval_digest", {"grader": "AUTHOR-SELF"})

    def equal_risk_change(doc):
        update_contract_pair(doc, "risk", "R5")

    def swap_budget_pairs(doc):
        first = scenario(doc, "S01")
        second = scenario(doc, "S17")
        for key in ("baseline_budget_ref", "candidate_budget_ref"):
            first["raw_state"][key], second["raw_state"][key] = (
                second["raw_state"][key], first["raw_state"][key]
            )
        first_migration = record(doc, "migration_registry", "migration_id", "MIGRATION.S01")
        second_migration = record(doc, "migration_registry", "migration_id", "MIGRATION.S17")
        for side in ("baseline_contract", "candidate_contract"):
            first_migration[side], second_migration[side] = (
                copy.deepcopy(second_migration[side]), copy.deepcopy(first_migration[side])
            )
        seal(first_migration)
        seal(second_migration)

    def unequal_cost_composition(doc):
        budget = record(doc, "budget_registry", "budget_id", "BUDGET.CANDIDATE.S01")
        budget["model_usd"] += 1
        budget["tool_usd"] -= 1
        seal(budget)

    def reconstructed_without_limitations(doc):
        identity = record(doc, "case_identity_registry", "identity_id", "IDENTITY.S01")
        source = record(doc, "source_registry", "source_id", "SOURCE.S01")
        identity["case_type"] = "RECONSTRUCTED"
        source["origin"] = "RECONSTRUCTION"
        seal(identity)
        seal(source)

    def vendor_adapter_evidence(doc):
        identity = record(doc, "case_identity_registry", "identity_id", "IDENTITY.S01")
        source = record(doc, "source_registry", "source_id", "SOURCE.S01")
        migration = record(doc, "migration_registry", "migration_id", "MIGRATION.S01")
        identity["case_type"] = "VENDOR-CLAIM"
        source["origin"] = "VENDOR_PUBLIC_PAGE"
        migration["adapter_differences"] = [{
            "category": "TOOL_SCHEMA",
            "criticality": "NON_CRITICAL",
            "affected_contract": "TOOL_INTERFACE",
            "evidence_ref": "ARTIFACT.TECHNICAL.S01",
            "owner": "PRINCIPAL.AUTHORITY.S01",
            "disposition": "ACCEPTED",
        }]
        seal(identity)
        seal(source)
        seal(migration)

    def legal_new_root(doc):
        item = record(doc, "trial_registry", "trial_record_id", "TRIAL.RECORD.S01.02")
        item["recorded_at"] = "2026-09-30T11:52:20Z"
        seal(item)

    def legal_noncritical_adapter(doc):
        item = record(doc, "migration_registry", "migration_id", "MIGRATION.S01")
        item["adapter_differences"] = [{
            "category": "TOOL_SCHEMA",
            "criticality": "NON_CRITICAL",
            "affected_contract": "TOOL_INTERFACE",
            "evidence_ref": "ARTIFACT.TECHNICAL.S01",
            "owner": "PRINCIPAL.AUTHORITY.S01",
            "disposition": "ACCEPTED",
        }]
        seal(item)

    semantic = []
    for number, registry in enumerate(id_keys, 1):
        semantic.append((
            f"F{number:02d}_EXTRA_{registry.upper()}",
            "exact_projection",
            extra_unprojected(registry),
            {"FAIL", "REJECT"},
        ))
    semantic.extend([
        ("F11_FAILURE_LOG_AFTER_D21", "causal_clock", late_failure_log_after_d21, {"FAIL", "REJECT"}),
        ("F12_TRIAL_AFTER_D21", "causal_clock", trial_after_d21, {"FAIL", "REJECT"}),
        ("F13_REVIEW_BEFORE_D21", "causal_clock", review_before_d21, {"FAIL", "REJECT"}),
        ("F14_AUTHORIZATION_AFTER_TRIAL", "causal_clock", authorization_after_trial, {"FAIL", "REJECT"}),
        ("F15_FAIL_TRIAL_WITHOUT_FAILURE_REF", "failure_bidirectional", failed_trial_without_failure_ref, {"FAIL", "REJECT"}),
        ("F16_PASS_TRIAL_WITH_FAILURE_REF", "failure_bidirectional", pass_trial_with_failure_ref, {"FAIL", "REJECT"}),
        ("F17_FAILURE_LOG_PAYLOAD_MISMATCH", "failure_bidirectional", failure_log_payload_mismatch, {"FAIL", "REJECT"}),
        ("F18_EFFECT_EXTERNAL_LIE", "effect_derivation", effect_external_lie, {"FAIL", "REJECT"}),
        ("F19_OFFLINE_EXTERNAL_WRITE", "effect_derivation", effect_external_write, {"FAIL", "REJECT"}),
        ("F20_EFFECT_UNAUTHORIZED", "effect_derivation", effect_unauthorized, {"FAIL", "REJECT"}),
        ("F21_D21_CONTENT_DISAGREES", "d21_content", d21_content_disagrees, {"FAIL", "REJECT"}),
        ("F22_ADAPTER_CONTRACT_MISMATCH", "adapter_matrix", adapter_contract_mismatch, {"FAIL", "REJECT"}),
        ("F23_ADAPTER_CROSS_CASE_EVIDENCE", "adapter_matrix", adapter_cross_case_evidence, {"FAIL", "REJECT"}),
        ("F24_ADAPTER_WRONG_OWNER", "adapter_matrix", adapter_wrong_owner, {"FAIL", "REJECT"}),
        ("F25_FORGED_EQUAL_TASK_CONTRACT", "migration_budget", forged_task_contract, {"FAIL", "REJECT"}),
        ("F26_FORGED_EQUAL_INPUT_CONTRACT", "migration_budget", forged_input_contract, {"FAIL", "REJECT"}),
        ("F27_EQUAL_PERMISSION_EXPANSION", "migration_budget", equal_permission_expansion, {"FAIL", "REJECT"}),
        ("F28_EQUAL_PRODUCTION_DATA", "migration_budget", equal_production_data, {"FAIL", "REJECT"}),
        ("F29_EQUAL_AUTHOR_SELF_GRADER", "migration_budget", equal_self_grader, {"FAIL", "REJECT"}),
        ("F30_EQUAL_RISK_CHANGE", "migration_budget", equal_risk_change, {"FAIL", "REJECT"}),
        ("F31_CROSS_CASE_BUDGET_PAIR_SWAP", "migration_budget", swap_budget_pairs, {"FAIL", "REJECT"}),
        ("F32_UNEQUAL_COST_COMPOSITION", "fair_cost", unequal_cost_composition, {"FAIL", "REJECT"}),
        ("F33_RECONSTRUCTED_WITHOUT_LIMITATIONS", "evidence_identity", reconstructed_without_limitations, {"REVIEW_REQUIRED", "FAIL", "REJECT"}),
        ("F34_VENDOR_ADAPTER_EVIDENCE", "evidence_identity", vendor_adapter_evidence, {"REVIEW_REQUIRED", "FAIL", "REJECT"}),
    ])

    rows = []
    old_pin = runner.PINNED_AUTHORITY_ROOT_DIGEST
    for test_id, category, mutate, secure in semantic:
        doc = copy.deepcopy(base)
        root = copy.deepcopy(authority)
        observed = "ERROR"
        reasons = []
        message = ""
        try:
            mutate(doc)
            repin(doc, root)
            result = runner.evaluate(doc, root)
            target = next(x for x in result["trials"] if x["scenario_id"] == "S01")
            observed = target["derived"]["verdict"]
            reasons = target["derived"]["reasons"]
        except Exception as error:
            observed = "REJECT"
            message = str(error)
        finally:
            runner.PINNED_AUTHORITY_ROOT_DIGEST = old_pin
        rows.append({
            "test_id": test_id,
            "category": category,
            "observed": observed,
            "reasons": reasons,
            "secure_expected_outcomes": sorted(secure),
            "secure_contract_passed": observed in secure,
            "message": message,
        })

    # Serialized attacks preserve hostile bytes until the strict parser runs.
    input_text = json.dumps(base, ensure_ascii=False, indent=2, sort_keys=True)
    duplicate = input_text.replace(
        '"case_version": 1', '"case_version": 99,\n        "case_version": 1', 1
    )
    try:
        runner.strict_json_loads(duplicate)
        observed = "ACCEPTED"
        message = ""
    except Exception as error:
        observed = "REJECT"
        message = str(error)
    rows.append({
        "test_id": "F35_NESTED_JSON_DUPLICATE_KEY",
        "category": "json_duplicate_key",
        "observed": observed,
        "reasons": [],
        "secure_expected_outcomes": ["REJECT"],
        "secure_contract_passed": observed == "REJECT",
        "message": message,
    })

    tampered = copy.deepcopy(baseline)
    tampered["trials"][0]["derived"]["reasons"].append("FORGED-REASON")
    try:
        runner.verify_result(tampered, authority)
        observed = "ACCEPTED"
        message = ""
    except Exception as error:
        observed = "REJECT"
        message = str(error)
    rows.append({
        "test_id": "F36_FULL_RESULT_DIGEST_TAMPER",
        "category": "result_integrity",
        "observed": observed,
        "reasons": [],
        "secure_expected_outcomes": ["REJECT"],
        "secure_contract_passed": observed == "REJECT",
        "message": message,
    })

    controls = []
    for test_id, mutate in (
        ("F-C01_LEGAL_NEW_ROOT", legal_new_root),
        ("F-C02_LEGAL_NONCRITICAL_ADAPTER", legal_noncritical_adapter),
    ):
        doc = copy.deepcopy(base)
        root = copy.deepcopy(authority)
        observed = "ERROR"
        message = ""
        reasons = []
        try:
            mutate(doc)
            repin(doc, root)
            result = runner.evaluate(doc, root)
            target = next(x for x in result["trials"] if x["scenario_id"] == "S01")
            observed = target["derived"]["verdict"]
            reasons = target["derived"]["reasons"]
        except Exception as error:
            observed = "REJECT"
            message = str(error)
        finally:
            runner.PINNED_AUTHORITY_ROOT_DIGEST = old_pin
        controls.append({
            "test_id": test_id,
            "category": "positive_neighbor",
            "observed": observed,
            "reasons": reasons,
            "secure_expected_outcomes": ["PASS"],
            "secure_contract_passed": observed == "PASS",
            "message": message,
        })

    escapes = [x for x in rows if not x["secure_contract_passed"]]
    payload = {
        "schema_version": "c23.v2.5.independent-final-negative-tests.v1",
        "oracle_policy": "chapter invariants and raw-state semantics; no author expected label used",
        "author_input_sha256": sha256_file(args.input),
        "authority_root_file_sha256": sha256_file(args.authority_root),
        "runner_sha256": sha256_file(args.runner),
        "baseline_distribution": baseline["distribution"],
        "baseline_decision_digest": baseline["decision_digest"],
        "attack_count": len(rows),
        "secure_attack_count": len(rows) - len(escapes),
        "escape_count": len(escapes),
        "escape_ids": [x["test_id"] for x in escapes],
        "positive_control_count": len(controls),
        "positive_control_pass_count": sum(x["secure_contract_passed"] for x in controls),
        "tests": rows + controls,
    }
    payload["suite_digest"] = runner.digest([
        (x["test_id"], x["observed"], x["reasons"], x["message"], x["secure_contract_passed"])
        for x in payload["tests"]
    ])
    Path(args.output).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        key: payload[key] for key in (
            "attack_count", "secure_attack_count", "escape_count", "escape_ids",
            "positive_control_count", "positive_control_pass_count", "suite_digest",
        )
    }, ensure_ascii=False))
    return 0 if not escapes and payload["positive_control_pass_count"] == len(controls) else 1


if __name__ == "__main__":
    raise SystemExit(main())

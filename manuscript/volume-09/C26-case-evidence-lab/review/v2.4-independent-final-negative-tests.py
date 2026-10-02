#!/usr/bin/env python3
"""Unannounced independent near-neighbor attacks for C23 v2.4.

The semantic tests start from the legal S01 PASS case, mutate raw registries,
reseal every changed record, rebuild the complete suite manifest/root, and pin
that newly valid root.  The serialized-result tests exercise the same contract
as verify-case-result.py but preserve hostile JSON bytes until parsing.
"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--authority-root", required=True)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    runner = load(Path(args.runner), "c23_v24_final_runner")
    base = json.loads(Path(args.input).read_text())
    authority = json.loads(Path(args.authority_root).read_text())
    baseline = runner.evaluate(copy.deepcopy(base), copy.deepcopy(authority))

    def seal(record):
        record["record_digest"] = runner.digest(
            {key: value for key, value in record.items() if key != "record_digest"}
        )

    def scenario(doc):
        return next(item for item in doc["scenarios"] if item["scenario_id"] == "S01")

    def records(doc, registry):
        return doc["registries"][registry]

    def record(doc, registry, key, value):
        return next(item for item in records(doc, registry) if item[key] == value)

    def artifact(doc, artifact_id):
        return record(doc, "artifact_registry", "artifact_id", artifact_id)

    def repin(doc, root):
        root["registries"] = copy.deepcopy(doc["registries"])
        root["suite_manifest"] = runner.suite_manifest(doc["suite"], doc["scenarios"])
        root["root_digest"] = runner.digest(runner.root_payload(root))
        runner.PINNED_AUTHORITY_ROOT_DIGEST = root["root_digest"]

    def add_parallel_d21_evidence(doc):
        source = copy.deepcopy(artifact(doc, "ARTIFACT.TECHNICAL.S01"))
        source["artifact_id"] = "ARTIFACT.TECHNICAL.CONTRADICT.S01"
        source["payload"]["state"] = "FAIL"
        source["content_digest"] = runner.digest(source["payload"])
        seal(source)
        records(doc, "artifact_registry").append(source)
        scenario(doc)["raw_state"]["artifact_refs"].append(source["artifact_id"])

    def add_shadow_principal(doc):
        source = copy.deepcopy(
            record(doc, "principal_registry", "principal_id", "PRINCIPAL.REVIEWER.S01")
        )
        source["principal_record_id"] = "PRINCIPAL.RECORD.REVIEWER.SHADOW.S01"
        source["independence_group"] = "GROUP.AUTHOR.S01"
        source["roles"] = ["ROLE.CASE.AUTHOR"]
        seal(source)
        original = records(doc, "principal_registry")
        original.insert(original.index(next(x for x in original if x["principal_id"] == "PRINCIPAL.REVIEWER.S01")), source)

    def add_shadow_release(doc):
        source = copy.deepcopy(
            record(doc, "release_registry", "release_id", "RELEASE.OPENCLAW.S01")
        )
        source["release_id"] = "RELEASE.OPENCLAW.SHADOW.S01"
        source["status"] = "REVOKED"
        seal(source)
        records(doc, "release_registry").append(source)

    def add_shadow_budget(doc):
        source = copy.deepcopy(
            record(doc, "budget_registry", "budget_id", "BUDGET.BASELINE.S01")
        )
        source["budget_id"] = "BUDGET.BASELINE.SHADOW.S01"
        source["status"] = "REVOKED"
        seal(source)
        records(doc, "budget_registry").append(source)

    def d21_precedes_support(doc):
        item = record(doc, "d21_registry", "d21_id", "D21.S01")
        item["recorded_at"] = "2026-09-30T11:50:00Z"
        seal(item)

    def failure_precedes_trial(doc):
        item = record(doc, "failure_registry", "failure_id", "FAILURE.S01.01")
        item["recorded_at"] = "2026-09-30T11:49:00Z"
        seal(item)

    def failure_log_has_undeclared_field(doc):
        item = artifact(doc, "ARTIFACT.FAILURE.S01")
        item["payload"]["note"] = "parallel explanation"
        item["content_digest"] = runner.digest(item["payload"])
        seal(item)

    def coherent_external_effect(doc):
        item = record(doc, "effect_registry", "effect_id", "EFFECT.S01")
        item["effect_kind"] = "EXTERNAL_WRITE"
        item["external"] = True
        expected = {
            "effect_id": item["effect_id"],
            "effect_kind": "EXTERNAL_WRITE",
            "external": True,
            "authorized": True,
            "status": "APPLIED",
        }
        item["receipt"] = copy.deepcopy(expected)
        item["readback"] = copy.deepcopy(expected)
        item["receipt_digest"] = runner.digest(item["receipt"])
        item["readback_digest"] = runner.digest(item["readback"])
        seal(item)

    def adapter_uses_public_artifact(doc):
        item = record(doc, "migration_registry", "migration_id", "MIGRATION.S01")
        item["adapter_differences"] = [{
            "category": "TOOL_SCHEMA",
            "criticality": "NON_CRITICAL",
            "affected_contract": "TOOL_INTERFACE",
            "evidence_ref": "ARTIFACT.PUBLIC.S01",
            "owner": "PRINCIPAL.AUTHORITY.S01",
            "disposition": "ACCEPTED",
        }]
        seal(item)

    def unfair_cost_composition(doc):
        item = record(doc, "budget_registry", "budget_id", "BUDGET.BASELINE.S01")
        item["model_usd"] += 0.25
        item["tool_usd"] -= 0.25
        seal(item)

    def migration_contract_detached_from_budget(doc):
        item = record(doc, "migration_registry", "migration_id", "MIGRATION.S01")
        forged = runner.digest({"not": "the selected budget task"})
        item["baseline_contract"]["task_digest"] = forged
        item["candidate_contract"]["task_digest"] = forged
        seal(item)

    def vendor_source_masquerades_as_synthetic(doc):
        item = record(doc, "source_registry", "source_id", "SOURCE.S01")
        item["origin"] = "VENDOR_PUBLIC_PAGE"
        seal(item)

    def legal_repin_control(doc):
        item = record(doc, "trial_registry", "trial_record_id", "TRIAL.RECORD.S01.02")
        item["recorded_at"] = "2026-09-30T11:52:15Z"
        seal(item)

    semantic_specs = [
        ("K01_PARALLEL_CONTRADICTORY_D21_EVIDENCE", add_parallel_d21_evidence, {"FAIL", "REJECT"}, "P0-01/P0-05"),
        ("K02_DUPLICATE_PRINCIPAL_SEMANTIC_TRUTH", add_shadow_principal, {"FAIL", "REJECT"}, "P0-01"),
        ("K03_UNPROJECTED_REVOKED_RELEASE_TWIN", add_shadow_release, {"FAIL", "REJECT"}, "P0-01"),
        ("K04_UNPROJECTED_REVOKED_BUDGET_TWIN", add_shadow_budget, {"FAIL", "REJECT"}, "P0-01"),
        ("K05_D21_PRECEDES_SUPPORTING_ARTIFACTS", d21_precedes_support, {"FAIL", "REVIEW_REQUIRED", "REJECT"}, "P0-02/P0-05"),
        ("K06_FAILURE_PRECEDES_ITS_TRIAL", failure_precedes_trial, {"FAIL", "REVIEW_REQUIRED", "REJECT"}, "P0-02/P0-03"),
        ("K07_FAILURE_LOG_PAYLOAD_NOT_CLOSED", failure_log_has_undeclared_field, {"FAIL", "REJECT"}, "P0-03"),
        ("K08_COHERENT_EXTERNAL_EFFECT", coherent_external_effect, {"FAIL", "REJECT"}, "P0-04"),
        ("K09_ADAPTER_EVIDENCE_WRONG_KIND", adapter_uses_public_artifact, {"FAIL", "REVIEW_REQUIRED", "REJECT"}, "P0-06"),
        ("K10_EQUAL_TOTAL_UNFAIR_COST_COMPOSITION", unfair_cost_composition, {"FAIL", "REJECT"}, "fairness"),
        ("K11_MIGRATION_CONTRACT_NOT_BOUND_TO_BUDGET", migration_contract_detached_from_budget, {"FAIL", "REJECT"}, "P0-06/fairness"),
        ("K12_VENDOR_SOURCE_SYNTHETIC_IDENTITY_MISMATCH", vendor_source_masquerades_as_synthetic, {"FAIL", "REVIEW_REQUIRED", "REJECT"}, "case-identity"),
    ]

    rows = []
    old_pin = runner.PINNED_AUTHORITY_ROOT_DIGEST
    for test_id, mutation, secure_outcomes, coverage in semantic_specs:
        doc = copy.deepcopy(base)
        root = copy.deepcopy(authority)
        actual = "ERROR"
        message = ""
        try:
            mutation(doc)
            repin(doc, root)
            result = runner.evaluate(doc, root)
            actual = next(
                item["derived"]["verdict"]
                for item in result["trials"]
                if item["scenario_id"] == "S01"
            )
        except Exception as exc:
            actual = "REJECT"
            message = str(exc)
        finally:
            runner.PINNED_AUTHORITY_ROOT_DIGEST = old_pin
        rows.append({
            "test_id": test_id,
            "layer": "semantic_legal_repin",
            "coverage": coverage,
            "secure_expected_outcomes": sorted(secure_outcomes),
            "actual": actual,
            "secure_contract_passed": actual in secure_outcomes,
            "message": message,
        })

    baseline_text = json.dumps(baseline, ensure_ascii=False, indent=2, sort_keys=True)

    def verify_serialized(raw):
        try:
            parsed = json.loads(raw)
            runner.verify_result(parsed, authority)
            expected = runner.evaluate(copy.deepcopy(base), copy.deepcopy(authority))
            if runner.canonical(parsed) != runner.canonical(expected):
                raise ValueError("result: derived rows or aggregates differ from independent replay")
            return "ACCEPTED", ""
        except Exception as exc:
            return "REJECT", str(exc)

    raw_attacks = [
        (
            "K13_RESULT_DUPLICATE_TOP_LEVEL_COUNT",
            baseline_text.replace("{", '{\n  "trial_count": 999,', 1),
        ),
        (
            "K14_RESULT_DUPLICATE_NESTED_VERDICT",
            baseline_text.replace('"verdict": "PASS"', '"verdict": "FAIL",\n        "verdict": "PASS"', 1),
        ),
        (
            "K15_RESULT_DUPLICATE_PROVENANCE_ROOT",
            baseline_text.replace(
                '"authority_root_digest":',
                '"authority_root_digest": "' + ("0" * 64) + '",\n    "authority_root_digest":',
                1,
            ),
        ),
    ]
    for test_id, raw in raw_attacks:
        actual, message = verify_serialized(raw)
        rows.append({
            "test_id": test_id,
            "layer": "serialized_result_verifier",
            "coverage": "P0-07/full-result-digest",
            "secure_expected_outcomes": ["REJECT"],
            "actual": actual,
            "secure_contract_passed": actual == "REJECT",
            "message": message,
        })

    doc = copy.deepcopy(base)
    root = copy.deepcopy(authority)
    actual = "ERROR"
    message = ""
    try:
        legal_repin_control(doc)
        repin(doc, root)
        result = runner.evaluate(doc, root)
        actual = next(
            item["derived"]["verdict"]
            for item in result["trials"]
            if item["scenario_id"] == "S01"
        )
    except Exception as exc:
        actual = "REJECT"
        message = str(exc)
    finally:
        runner.PINNED_AUTHORITY_ROOT_DIGEST = old_pin
    rows.append({
        "test_id": "K16_LEGAL_NEW_ROOT_PASS_CONTROL",
        "layer": "non_total_rejection_control",
        "coverage": "legal-repin",
        "secure_expected_outcomes": ["PASS"],
        "actual": actual,
        "secure_contract_passed": actual == "PASS",
        "message": message,
    })

    attacks = [row for row in rows if row["test_id"] != "K16_LEGAL_NEW_ROOT_PASS_CONTROL"]
    payload = {
        "schema_version": "c23.v2.4.independent-final-negative.v1",
        "baseline_distribution": baseline["distribution"],
        "baseline_decision_digest": baseline["decision_digest"],
        "attack_count": len(attacks),
        "secure_attack_count": sum(row["secure_contract_passed"] for row in attacks),
        "escape_count": sum(not row["secure_contract_passed"] for row in attacks),
        "legal_pass_control": actual,
        "tests": rows,
    }
    payload["suite_digest"] = runner.digest(
        [(row["test_id"], row["actual"], row["message"], row["secure_contract_passed"]) for row in rows]
    )
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in ("attack_count", "secure_attack_count", "escape_count", "legal_pass_control", "suite_digest")}, ensure_ascii=False))
    return 0 if payload["escape_count"] == 0 and payload["legal_pass_control"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

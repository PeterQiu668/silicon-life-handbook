#!/usr/bin/env python3
"""Unannounced non-author near-neighbour tests for C23 v2.6.

Oracles come from the chapter's stated evidence contracts, not fixture names or
author expected labels. Semantic attacks are legally re-digested and re-pinned
so frozen-root rejection cannot conceal a fail-open rule.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location("c23_v26_independent_final_runner", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def file_sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--authority-root", required=True)
    p.add_argument("--runner", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    input_path, root_path, runner_path = Path(a.input), Path(a.authority_root), Path(a.runner)
    r = load(runner_path)
    base = r.strict_json_loads(input_path.read_text())
    authority = r.strict_json_loads(root_path.read_text())
    baseline = r.evaluate(copy.deepcopy(base), copy.deepcopy(authority))
    rows = []

    def seal(row):
        row["record_digest"] = r.digest({k: v for k, v in row.items() if k != "record_digest"})

    def rec(doc, registry, key, value):
        return next(x for x in doc["registries"][registry] if x[key] == value)

    def scenario(doc, sid="S01"):
        return next(x for x in doc["scenarios"] if x["scenario_id"] == sid)

    def repin(doc, root):
        root["registries"] = copy.deepcopy(doc["registries"])
        root["suite_manifest"] = r.suite_manifest(doc["suite"], doc["scenarios"])
        root["root_digest"] = r.digest(r.root_payload(root))
        r.PINNED_AUTHORITY_ROOT_DIGEST = root["root_digest"]

    contract_keys = ("case_record_id", "case_version", "task_id", "run_id", "side", "task_authority_ref", "input_authority_ref", "permission_authority_ref", "dataset_authority_ref", "grader_authority_ref", "task_digest", "input_digest", "risk", "permissions_digest", "data_digest", "eval_digest", "model_usd", "tool_usd", "compute_usd", "human_minutes", "human_usd", "elapsed_seconds", "total_usd")

    def reseal_budget(doc, budget):
        budget["contract_digest"] = r.digest({k: budget[k] for k in contract_keys})
        seal(budget)

    def sync_migration(doc, sid="S01"):
        m = rec(doc, "migration_registry", "migration_id", "MIGRATION." + sid)
        for side, bid in (("baseline_contract", "BUDGET.BASELINE." + sid), ("candidate_contract", "BUDGET.CANDIDATE." + sid)):
            b = rec(doc, "budget_registry", "budget_id", bid)
            for key in ("case_record_id", "case_version", "task_id", "run_id", "task_authority_ref", "input_authority_ref", "permission_authority_ref", "dataset_authority_ref", "grader_authority_ref", "task_digest", "input_digest", "risk", "permissions_digest", "data_digest", "eval_digest"):
                m[side][key] = b[key]
            m[side]["budget_contract_digest"] = b["contract_digest"]
        seal(m)

    def extra_authority(registry, key):
        def mutate(doc):
            row = copy.deepcopy(doc["registries"][registry][0])
            row[key] += ".UNSELECTED"
            seal(row)
            doc["registries"][registry].append(row)
        return mutate

    def grader_aliases_author(doc):
        alias = {"alias_record_id": "ALIAS.RECORD.GRADER.AUTHOR.S01", "alias_id": "ALIAS.GRADER.AUTHOR.S01", "canonical_principal_id": "PRINCIPAL.AUTHOR.S01", "status": "ACTIVE", "record_digest": ""}
        seal(alias)
        doc["registries"]["alias_registry"].append(alias)
        ga = rec(doc, "grader_authority_registry", "grader_authority_id", "AUTHORITY.GRADER.S01")
        ga["grader_principal_id"] = alias["alias_id"]
        ga["eval_spec"]["grader_principal_id"] = alias["alias_id"]
        ga["eval_digest"] = r.digest(ga["eval_spec"])
        seal(ga)
        for bid in ("BUDGET.BASELINE.S01", "BUDGET.CANDIDATE.S01"):
            b = rec(doc, "budget_registry", "budget_id", bid)
            b["eval_spec"] = copy.deepcopy(ga["eval_spec"])
            b["eval_digest"] = ga["eval_digest"]
            reseal_budget(doc, b)
        sync_migration(doc)

    def authority_aliases_author(doc):
        alias = {"alias_record_id": "ALIAS.RECORD.AUTHORITY.AUTHOR.S01", "alias_id": "ALIAS.AUTHORITY.AUTHOR.S01", "canonical_principal_id": "PRINCIPAL.AUTHOR.S01", "status": "ACTIVE", "record_digest": ""}
        seal(alias)
        doc["registries"]["alias_registry"].append(alias)
        for registry, key, value in (("case_identity_registry", "identity_id", "IDENTITY.S01"), ("authorization_registry", "authorization_id", "AUTHORIZATION.S01"), ("source_registry", "source_id", "SOURCE.S01"), ("redaction_registry", "redaction_id", "REDACTION.S01")):
            row = rec(doc, registry, key, value)
            field = "principal_id" if registry == "authorization_registry" else "authorized_by_principal_id" if registry == "redaction_registry" else "authority_principal_id"
            row[field] = alias["alias_id"]
            seal(row)

    def budget_field(doc, budget_id, field, value, sync=True):
        b = rec(doc, "budget_registry", "budget_id", budget_id)
        b[field] = value
        reseal_budget(doc, b)
        if sync: sync_migration(doc)

    def budget_run_mismatch(doc):
        budget_field(doc, "BUDGET.CANDIDATE.S01", "run_id", "RUN.FORGED.S01")

    def budget_side_duplicate(doc):
        budget_field(doc, "BUDGET.CANDIDATE.S01", "side", "BASELINE")

    def budget_case_mismatch(doc):
        budget_field(doc, "BUDGET.BASELINE.S01", "case_record_id", "CASE.RECORD.S17")

    def budget_task_mismatch(doc):
        budget_field(doc, "BUDGET.BASELINE.S01", "task_id", "TASK.S17")

    def stale_migration_contract(doc):
        b = rec(doc, "budget_registry", "budget_id", "BUDGET.BASELINE.S01")
        b["model_usd"] += 0.01
        b["tool_usd"] -= 0.01
        reseal_budget(doc, b)
        # Deliberately retain the prior migration budget digest.

    def failure_log_after_d21_boundary(doc):
        row = rec(doc, "artifact_registry", "artifact_id", "ARTIFACT.FAILURE.S01")
        row["recorded_at"] = "2026-09-30T11:56:00.001000Z"
        seal(row)

    def failure_after_d21(doc):
        row = rec(doc, "failure_registry", "failure_id", "FAILURE.S01.01")
        row["recorded_at"] = "2026-09-30T11:56:00.001000Z"
        seal(row)

    def reconstructed_partial(doc, which):
        identity = rec(doc, "case_identity_registry", "identity_id", "IDENTITY.S01")
        source = rec(doc, "source_registry", "source_id", "SOURCE.S01")
        identity["case_type"] = "RECONSTRUCTED"
        source["origin"] = "RECONSTRUCTION"
        if which == "missing_only":
            identity["missing_elements"] = source["missing_elements"] = ["ORIGINAL.INPUT"]
        elif which == "inference_only":
            identity["inference_list"] = source["inference_list"] = ["INFERRED.TIMELINE"]
        else:
            identity["missing_elements"] = ["ORIGINAL.INPUT"]
            identity["inference_list"] = ["INFERRED.TIMELINE"]
            source["missing_elements"] = ["ORIGINAL.OUTPUT"]
            source["inference_list"] = ["INFERRED.TIMELINE"]
        seal(identity)
        seal(source)

    def d21_declared_pass_payload_unknown(doc):
        art = rec(doc, "artifact_registry", "artifact_id", "ARTIFACT.TECHNICAL.S01")
        art["payload"]["state"] = "UNKNOWN"
        art["content_digest"] = r.digest(art["payload"])
        seal(art)

    def d21_wrong_run(doc):
        d21 = rec(doc, "d21_registry", "d21_id", "D21.S01")
        d21["run_id"] = "RUN.S17"
        seal(d21)

    semantic = [
        ("U01_EXTRA_TASK_AUTHORITY", "exact-authority-projection", extra_authority("task_authority_registry", "task_authority_id"), {"FAIL", "REJECT"}),
        ("U02_EXTRA_INPUT_AUTHORITY", "exact-authority-projection", extra_authority("input_authority_registry", "input_authority_id"), {"FAIL", "REJECT"}),
        ("U03_EXTRA_PERMISSION_AUTHORITY", "exact-authority-projection", extra_authority("permission_authority_registry", "permission_authority_id"), {"FAIL", "REJECT"}),
        ("U04_EXTRA_DATASET_AUTHORITY", "exact-authority-projection", extra_authority("dataset_authority_registry", "dataset_authority_id"), {"FAIL", "REJECT"}),
        ("U05_EXTRA_GRADER_AUTHORITY", "exact-authority-projection", extra_authority("grader_authority_registry", "grader_authority_id"), {"FAIL", "REJECT"}),
        ("U06_GRADER_ALIAS_IS_AUTHOR", "principal-alias-independence", grader_aliases_author, {"FAIL", "REJECT"}),
        ("U07_AUTHORITY_ALIAS_IS_AUTHOR", "principal-alias-independence", authority_aliases_author, {"FAIL", "REJECT"}),
        ("U08_BUDGET_RUN_MISMATCH", "budget-binding", budget_run_mismatch, {"FAIL", "REJECT"}),
        ("U09_BUDGET_SIDE_DUPLICATE", "budget-binding", budget_side_duplicate, {"FAIL", "REJECT"}),
        ("U10_BUDGET_CASE_MISMATCH", "budget-binding", budget_case_mismatch, {"FAIL", "REJECT"}),
        ("U11_BUDGET_TASK_MISMATCH", "budget-binding", budget_task_mismatch, {"FAIL", "REJECT"}),
        ("U12_STALE_MIGRATION_CONTRACT", "budget-contract-digest", stale_migration_contract, {"FAIL", "REJECT"}),
        ("U13_FAILURE_LOG_AFTER_D21_MICROSECOND", "causal-clock", failure_log_after_d21_boundary, {"FAIL", "REJECT"}),
        ("U14_FAILURE_AFTER_D21", "causal-clock", failure_after_d21, {"FAIL", "REJECT"}),
        ("U15_RECONSTRUCTED_MISSING_ONLY", "reconstruction-disclosure", lambda d: reconstructed_partial(d, "missing_only"), {"FAIL", "REJECT"}),
        ("U16_RECONSTRUCTED_INFERENCE_ONLY", "reconstruction-disclosure", lambda d: reconstructed_partial(d, "inference_only"), {"FAIL", "REJECT"}),
        ("U17_RECONSTRUCTED_SOURCE_MISMATCH", "reconstruction-disclosure", lambda d: reconstructed_partial(d, "mismatch"), {"FAIL", "REJECT"}),
        ("U18_D21_PAYLOAD_UNKNOWN_DECLARED_PASS", "d21-content", d21_declared_pass_payload_unknown, {"FAIL", "REVIEW_REQUIRED", "REJECT"}),
        ("U19_D21_WRONG_RUN", "d21-binding", d21_wrong_run, {"FAIL", "REJECT"}),
    ]
    old_pin = r.PINNED_AUTHORITY_ROOT_DIGEST
    for test_id, family, mutate, secure in semantic:
        doc, root = copy.deepcopy(base), copy.deepcopy(authority)
        observed, reasons, message = "ERROR", [], ""
        try:
            mutate(doc)
            repin(doc, root)
            result = r.evaluate(doc, root)
            target = next(x for x in result["trials"] if x["scenario_id"] == "S01")
            observed, reasons = target["derived"]["verdict"], target["derived"]["reasons"]
        except Exception as exc:
            observed, message = "REJECT", str(exc)
        finally:
            r.PINNED_AUTHORITY_ROOT_DIGEST = old_pin
        ok = observed in secure
        rows.append({"test_id": test_id, "family": family, "layer": "semantic-authorized-repin", "observed": observed, "reasons": reasons, "secure_expected_outcomes": sorted(secure), "secure_contract_passed": ok, "escape": not ok, "message": message})

    def result_attack(test_id, mutate):
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        candidate["decision_digest"] = r.digest({k: v for k, v in candidate.items() if k != "decision_digest"})
        observed, message = "ACCEPTED", ""
        try: r.verify_result(candidate, authority)
        except Exception as exc: observed, message = "REJECT", str(exc)
        ok = observed == "REJECT"
        rows.append({"test_id": test_id, "family": "persisted-result-semantic-integrity", "layer": "result-verifier", "observed": observed, "reasons": [], "secure_expected_outcomes": ["REJECT"], "secure_contract_passed": ok, "escape": not ok, "message": message})

    def fail_to_pass(result):
        row = next(x for x in result["trials"] if x["derived"]["verdict"] == "FAIL")
        row["derived"].update(verdict="PASS", reasons=[])
        result["distribution"] = dict(sorted(Counter(x["derived"]["verdict"] for x in result["trials"]).items()))

    def rr_to_pass(result):
        row = next(x for x in result["trials"] if x["derived"]["verdict"] == "REVIEW_REQUIRED")
        row["derived"].update(verdict="PASS", reasons=[])
        result["distribution"] = dict(sorted(Counter(x["derived"]["verdict"] for x in result["trials"]).items()))

    result_attack("U20_RESULT_FAIL_TO_PASS_COHERENT_REHASH", fail_to_pass)
    result_attack("U21_RESULT_RR_TO_PASS_COHERENT_REHASH", rr_to_pass)

    def serialized(test_id, source_text, kind, needle, replacement):
        hostile = source_text.replace(needle, replacement, 1)
        observed, message = "ACCEPTED", ""
        try:
            parsed = r.strict_json_loads(hostile)
            if kind == "input": r.evaluate(parsed, authority)
            elif kind == "root": r.validate_authority_root(parsed)
            else: r.verify_result(parsed, authority)
        except Exception as exc: observed, message = "REJECT", str(exc)
        ok = observed == "REJECT"
        rows.append({"test_id": test_id, "family": "recursive-json-duplicate", "layer": "serialized-boundary", "observed": observed, "reasons": [], "secure_expected_outcomes": ["REJECT"], "secure_contract_passed": ok, "escape": not ok, "message": message})

    input_text = input_path.read_text()
    root_text = root_path.read_text()
    result_text = json.dumps(baseline, ensure_ascii=False, indent=2, sort_keys=True)
    serialized("U22_INPUT_NESTED_DUPLICATE", input_text, "input", '"case_version": 1', '"case_version": 99,\n        "case_version": 1')
    serialized("U23_ROOT_NESTED_DUPLICATE", root_text, "root", '"status": "ACTIVE"', '"status": "REVOKED",\n        "status": "ACTIVE"')
    serialized("U24_RESULT_NESTED_DUPLICATE", result_text, "result", '"verdict": "PASS"', '"verdict": "FAIL",\n        "verdict": "PASS"')

    controls = []
    def control(test_id, mutate, expected):
        doc, root = copy.deepcopy(base), copy.deepcopy(authority)
        observed, reasons, message = "ERROR", [], ""
        try:
            mutate(doc)
            repin(doc, root)
            result = r.evaluate(doc, root)
            target = next(x for x in result["trials"] if x["scenario_id"] == "S01")
            observed, reasons = target["derived"]["verdict"], target["derived"]["reasons"]
        except Exception as exc: observed, message = "REJECT", str(exc)
        finally: r.PINNED_AUTHORITY_ROOT_DIGEST = old_pin
        controls.append({"test_id": test_id, "observed": observed, "reasons": reasons, "expected": expected, "passed": observed == expected, "message": message})

    def equal_failure_log_d21(doc):
        d21 = rec(doc, "d21_registry", "d21_id", "D21.S01")
        log = rec(doc, "artifact_registry", "artifact_id", "ARTIFACT.FAILURE.S01")
        log["recorded_at"] = d21["recorded_at"]
        seal(log)

    def complete_reconstruction(doc):
        identity = rec(doc, "case_identity_registry", "identity_id", "IDENTITY.S01")
        source = rec(doc, "source_registry", "source_id", "SOURCE.S01")
        for row in (identity, source):
            row["missing_elements"] = ["ORIGINAL.INPUT"]
            row["inference_list"] = ["INFERRED.TIMELINE"]
        identity["case_type"] = "RECONSTRUCTED"
        source["origin"] = "RECONSTRUCTION"
        seal(identity); seal(source)

    control("U-C01_FAILURE_LOG_EQUALS_D21_ALLOWED", equal_failure_log_d21, "PASS")
    control("U-C02_COMPLETE_RECONSTRUCTION_LIMITED", complete_reconstruction, "REVIEW_REQUIRED")

    escapes = [x for x in rows if x["escape"]]
    payload = {
        "schema_version": "c23.v2.6.independent-final-negative.v1",
        "review_role": "non_author",
        "oracle_policy": "chapter invariants and raw-state semantics; no author expected label used",
        "input_sha256": file_sha(input_path),
        "authority_root_sha256": file_sha(root_path),
        "runner_sha256": file_sha(runner_path),
        "baseline_distribution": baseline["distribution"],
        "baseline_decision_digest": baseline["decision_digest"],
        "attack_count": len(rows),
        "secure_attack_count": len(rows) - len(escapes),
        "escape_count": len(escapes),
        "escape_ids": [x["test_id"] for x in escapes],
        "positive_control_count": len(controls),
        "positive_control_pass_count": sum(x["passed"] for x in controls),
        "tests": rows,
        "positive_controls": controls,
        "limits": {"real_case_executed": False, "real_runtime_migration_executed": False, "external_effect_executed": False, "practice_gate": "REVIEW_REQUIRED", "editor_chief_rc": "NOT_AUTHORIZED"},
    }
    payload["suite_digest"] = r.digest([(x["test_id"], x["observed"], x["reasons"], x["message"], x["secure_contract_passed"]) for x in rows] + [(x["test_id"], x["observed"], x["reasons"], x["message"], x["passed"]) for x in controls])
    Path(a.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: payload[k] for k in ("attack_count", "secure_attack_count", "escape_count", "escape_ids", "positive_control_count", "positive_control_pass_count", "suite_digest")}, ensure_ascii=False))
    return 0 if not escapes and payload["positive_control_pass_count"] == len(controls) else 1


if __name__ == "__main__":
    raise SystemExit(main())

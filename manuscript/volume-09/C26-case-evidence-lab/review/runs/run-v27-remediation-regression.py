#!/usr/bin/env python3
"""C23 v2.7 author regression for mandatory source-semantic replay.

The tests do not use scenario names as verdict oracles.  They derive a FAIL,
REVIEW_REQUIRED and PASS row from the baseline result, coherently re-sign
tampered result envelopes where applicable, and require the one public result
verification entry point to replay the frozen source.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from collections import Counter
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location("c23_v27_runner", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--authority-root", required=True)
    p.add_argument("--result", required=True)
    p.add_argument("--runner", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    r = load(Path(a.runner))
    source_text = Path(a.input).read_text()
    root_text = Path(a.authority_root).read_text()
    result_text = Path(a.result).read_text()
    base = r.strict_json_loads(source_text)
    authority = r.strict_json_loads(root_text)
    persisted = r.strict_json_loads(result_text)
    replayed = r.evaluate(copy.deepcopy(base), copy.deepcopy(authority))
    if r.canonical(persisted) != r.canonical(replayed):
        raise ValueError("committed result differs from source replay")

    fail_row = next(x for x in persisted["trials"] if x["derived"]["verdict"] == "FAIL")
    rr_row = next(x for x in persisted["trials"] if x["derived"]["verdict"] == "REVIEW_REQUIRED")
    pass_row = next(x for x in persisted["trials"] if x["derived"]["verdict"] == "PASS")
    rows = []
    controls = []

    def resign_result(result):
        result["distribution"] = dict(sorted(Counter(x["derived"]["verdict"] for x in result["trials"]).items()))
        result["accepted_real_claim_count"] = sum(x["derived"]["accepted_real_claim_count"] for x in result["trials"])
        result["external_effect_count"] = sum(x["derived"]["external_effect_count"] for x in result["trials"])
        result["decision_digest"] = r.digest({k: v for k, v in result.items() if k != "decision_digest"})

    def result_attack(test_id, mutate, source=None, root=None, omit_source=False):
        candidate = copy.deepcopy(persisted)
        mutate(candidate)
        resign_result(candidate)
        observed, message = "ACCEPTED", ""
        try:
            if omit_source:
                r.verify_result(candidate, authority)
            else:
                r.verify_result(candidate, root or authority, base if source is None else source)
        except Exception as exc:
            observed, message = "REJECT", str(exc)
        rows.append({"test_id": test_id, "family": "mandatory-semantic-replay", "observed": observed, "secure_expected_outcomes": ["REJECT"], "secure_contract_passed": observed == "REJECT", "message": message})

    def row_by_id(result, identity):
        return next(x for x in result["trials"] if x["scenario_id"] == identity)

    result_attack("V27-01_FAIL_TO_PASS_COHERENT_REHASH", lambda x: row_by_id(x, fail_row["scenario_id"])["derived"].update(verdict="PASS", reasons=[]))
    result_attack("V27-02_RR_TO_PASS_COHERENT_REHASH", lambda x: row_by_id(x, rr_row["scenario_id"])["derived"].update(verdict="PASS", reasons=[]))
    result_attack("V27-03_FAIL_REASON_REWRITE_COHERENT_REHASH", lambda x: row_by_id(x, fail_row["scenario_id"])["derived"].update(reasons=["FORGED.COHERENT.REASON"]))
    result_attack("V27-04_RR_REASON_REWRITE_COHERENT_REHASH", lambda x: row_by_id(x, rr_row["scenario_id"])["derived"].update(reasons=["FORGED.COHERENT.REVIEW"]))
    result_attack("V27-05_TRIAL_EXTERNAL_COUNT_REWRITE", lambda x: row_by_id(x, pass_row["scenario_id"])["derived"].update(external_effect_count=1))
    result_attack("V27-06_TRIAL_REAL_COUNT_REWRITE", lambda x: row_by_id(x, pass_row["scenario_id"])["derived"].update(accepted_real_claim_count=1))
    result_attack("V27-07_ORDERED_ROWS_SWAPPED", lambda x: x["trials"].__setitem__(slice(0, 2), [x["trials"][1], x["trials"][0]]))
    result_attack("V27-08_CROSS_CASE_RESULT_IDENTITY_TRANSPLANT", lambda x: x["trials"][0].update({k: x["trials"][1][k] for k in ("case_record_id", "task_id", "trial_id", "run_id", "evidence_id")}))
    result_attack("V27-09_SOURCE_ARGUMENT_OMITTED", lambda x: None, omit_source=True)
    result_attack("V27-10_SOURCE_ARGUMENT_NONE", lambda x: None, source=None if False else {})

    def source_attack(test_id, mutate, repin=False, rebind_result=False):
        doc, root, candidate = copy.deepcopy(base), copy.deepcopy(authority), copy.deepcopy(persisted)
        mutate(doc, root)
        old_pin = r.PINNED_AUTHORITY_ROOT_DIGEST
        try:
            if repin:
                root["registries"] = copy.deepcopy(doc["registries"])
                root["suite_manifest"] = r.suite_manifest(doc["suite"], doc["scenarios"])
                root["root_digest"] = r.digest(r.root_payload(root))
                r.PINNED_AUTHORITY_ROOT_DIGEST = root["root_digest"]
                if rebind_result:
                    candidate["authority_root_digest"] = root["root_digest"]
                    candidate["provenance"]["authority_root_digest"] = root["root_digest"]
                    candidate["provenance"]["scenario_manifest_digest"] = root["suite_manifest"]["scenario_manifest_digest"]
                    resign_result(candidate)
            observed, message = "ACCEPTED", ""
            try:
                r.verify_result(candidate, root, doc)
            except Exception as exc:
                observed, message = "REJECT", str(exc)
            rows.append({"test_id": test_id, "family": "source-root-binding", "observed": observed, "secure_expected_outcomes": ["REJECT"], "secure_contract_passed": observed == "REJECT", "message": message})
        finally:
            r.PINNED_AUTHORITY_ROOT_DIGEST = old_pin

    source_attack("V27-11_SOURCE_SCENARIO_MISSING", lambda d, _r: d["scenarios"].pop())
    source_attack("V27-12_SOURCE_SCENARIO_REORDERED", lambda d, _r: d["scenarios"].__setitem__(slice(0, 2), [d["scenarios"][1], d["scenarios"][0]]))
    source_attack("V27-13_CROSS_CASE_SOURCE_REF_TRANSPLANT", lambda d, _r: d["scenarios"][0]["raw_state"].update(source_ref=d["scenarios"][1]["raw_state"]["source_ref"]), repin=True, rebind_result=True)

    def private_source_rewrite(doc, _root):
        row = doc["registries"]["source_registry"][0]
        row["private_content"] = {"private_case": "FORGED.COHERENT"}
        row["private_content_digest"] = r.digest(row["private_content"])
        row["record_digest"] = r.digest({k: v for k, v in row.items() if k != "record_digest"})
    source_attack("V27-14_SOURCE_CONTENT_REPLACED_WITHOUT_ROOT", private_source_rewrite)

    def root_digest_wrong(_doc, root):
        root["root_digest"] = "0" * 64
    source_attack("V27-15_AUTHORITY_ROOT_DIGEST_WRONG", root_digest_wrong)

    def root_manifest_wrong(_doc, root):
        root["suite_manifest"]["scenario_manifest_digest"] = "0" * 64
    source_attack("V27-16_AUTHORITY_MANIFEST_DIGEST_WRONG", root_manifest_wrong)

    def cross_case_registry_swap(doc, _root):
        first, second = doc["registries"]["source_registry"][:2]
        first["case_record_id"], second["case_record_id"] = second["case_record_id"], first["case_record_id"]
        for row in (first, second):
            row["record_digest"] = r.digest({k: v for k, v in row.items() if k != "record_digest"})
    source_attack("V27-17_CROSS_CASE_SOURCE_REGISTRY_SWAP_REPINNED", cross_case_registry_swap, repin=True, rebind_result=True)

    def result_root_rebind_only(result):
        result["authority_root_digest"] = "1" * 64
        result["provenance"]["authority_root_digest"] = "1" * 64
    result_attack("V27-18_RESULT_AUTHORITY_ROOT_REBOUND", result_root_rebind_only)

    def serialized_attack(test_id, text, kind, needle, replacement):
        hostile = text.replace(needle, replacement, 1)
        observed, message = "ACCEPTED", ""
        try:
            parsed = r.strict_json_loads(hostile)
            if kind == "result": r.verify_result(parsed, authority, base)
            elif kind == "source": r.verify_result(persisted, authority, parsed)
            else: r.verify_result(persisted, parsed, base)
        except Exception as exc:
            observed, message = "REJECT", str(exc)
        rows.append({"test_id": test_id, "family": "recursive-duplicate-key", "observed": observed, "secure_expected_outcomes": ["REJECT"], "secure_contract_passed": observed == "REJECT", "message": message})

    serialized_attack("V27-19_RESULT_NESTED_DUPLICATE", result_text, "result", '"verdict": "PASS"', '"verdict": "FAIL",\n        "verdict": "PASS"')
    serialized_attack("V27-20_SOURCE_NESTED_DUPLICATE", source_text, "source", '"case_version": 1', '"case_version": 99,\n        "case_version": 1')
    serialized_attack("V27-21_ROOT_NESTED_DUPLICATE", root_text, "root", '"status": "ACTIVE"', '"status": "REVOKED",\n        "status": "ACTIVE"')
    source_attack("V27-22_SOURCE_SCHEMA_REPLACED", lambda d, _r: d.update(schema_version="c23.case.input.forged"))
    source_attack("V27-23_AUTHORITY_REGISTRY_SOURCE_DROPPED", lambda _d, root: root["registries"]["source_registry"].pop())

    def coherent_source_rewrite(doc, _root):
        row = doc["registries"]["trial_registry"][0]
        row["status"] = "UNKNOWN"
        row["failure_ref"] = "NONE"
        row["record_digest"] = r.digest({k: v for k, v in row.items() if k != "record_digest"})
    source_attack("V27-24_REPINNED_SOURCE_WITH_STALE_SEMANTIC_RESULT", coherent_source_rewrite, repin=True, rebind_result=True)

    def control(test_id, fn):
        observed, message = "PASS", ""
        try: fn()
        except Exception as exc: observed, message = "REJECT", str(exc)
        controls.append({"test_id": test_id, "observed": observed, "expected": "PASS", "passed": observed == "PASS", "message": message})

    control("V27-C01_UNMODIFIED_PERSISTED_RESULT", lambda: r.verify_result(copy.deepcopy(persisted), copy.deepcopy(authority), copy.deepcopy(base)))
    control("V27-C02_DETERMINISTIC_REPLAY_RESULT", lambda: r.verify_result(r.evaluate(copy.deepcopy(base), copy.deepcopy(authority)), copy.deepcopy(authority), copy.deepcopy(base)))

    def legal_task_repin():
        doc, root = copy.deepcopy(base), copy.deepcopy(authority)
        target = next(x for x in replayed["trials"] if x["derived"]["verdict"] == "PASS")
        scenario = next(x for x in doc["scenarios"] if x["scenario_id"] == target["scenario_id"])
        raw = scenario["raw_state"]
        task = next(x for x in doc["registries"]["task_authority_registry"] if x["task_authority_id"] == raw["task_authority_ref"])
        spec = dict(task["task_spec"])
        spec["clarification"] = "LEGAL.BOUNDARY.V27"
        task["task_spec"] = spec; task["task_digest"] = r.digest(spec)
        task["record_digest"] = r.digest({k: v for k, v in task.items() if k != "record_digest"})
        contract_keys=("case_record_id","case_version","task_id","run_id","side","task_authority_ref","input_authority_ref","permission_authority_ref","dataset_authority_ref","grader_authority_ref","task_digest","input_digest","risk","permissions_digest","data_digest","eval_digest","model_usd","tool_usd","compute_usd","human_minutes","human_usd","elapsed_seconds","total_usd")
        budgets=[]
        for ref in (raw["baseline_budget_ref"], raw["candidate_budget_ref"]):
            budget=next(x for x in doc["registries"]["budget_registry"] if x["budget_id"]==ref)
            budget["task_spec"]=copy.deepcopy(spec); budget["task_digest"]=task["task_digest"]
            budget["contract_digest"]=r.digest({k:budget[k] for k in contract_keys})
            budget["record_digest"]=r.digest({k:v for k,v in budget.items() if k!="record_digest"}); budgets.append(budget)
        migration=next(x for x in doc["registries"]["migration_registry"] if x["migration_id"]==raw["migration_ref"])
        for side,budget in zip(("baseline_contract","candidate_contract"),budgets):
            migration[side]["task_digest"]=task["task_digest"]
            migration[side]["budget_contract_digest"]=budget["contract_digest"]
        migration["record_digest"]=r.digest({k:v for k,v in migration.items() if k!="record_digest"})
        root["registries"]=copy.deepcopy(doc["registries"]); root["suite_manifest"]=r.suite_manifest(doc["suite"],doc["scenarios"]); root["root_digest"]=r.digest(r.root_payload(root))
        old_pin=r.PINNED_AUTHORITY_ROOT_DIGEST
        try:
            r.PINNED_AUTHORITY_ROOT_DIGEST=root["root_digest"]
            result=r.evaluate(doc,root)
            r.verify_result(result,root,doc)
            actual=next(x for x in result["trials"] if x["scenario_id"]==target["scenario_id"])["derived"]["verdict"]
            if actual!="PASS": raise ValueError("legal repin positive control did not remain PASS")
        finally: r.PINNED_AUTHORITY_ROOT_DIGEST=old_pin

    control("V27-C03_LEGAL_TASK_AUTHORITY_REPIN", legal_task_repin)
    escapes=[x for x in rows if not x["secure_contract_passed"]]
    payload={"schema_version":"c23.v2.7.author-remediation-regression.v1","baseline_distribution":replayed["distribution"],"baseline_decision_digest":replayed["decision_digest"],"attack_count":len(rows),"secure_attack_count":len(rows)-len(escapes),"escape_count":len(escapes),"escape_ids":[x["test_id"] for x in escapes],"positive_control_count":len(controls),"positive_control_pass_count":sum(x["passed"] for x in controls),"tests":rows,"positive_controls":controls}
    payload["suite_digest"]=r.digest([(x["test_id"],x["observed"],x["message"],x["secure_contract_passed"]) for x in rows]+[(x["test_id"],x["observed"],x["message"],x["passed"]) for x in controls])
    Path(a.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:payload[k] for k in ("attack_count","secure_attack_count","escape_count","positive_control_count","positive_control_pass_count","suite_digest")},ensure_ascii=False))
    return 0 if not escapes and payload["positive_control_pass_count"]==len(controls) else 1


if __name__=="__main__":
    raise SystemExit(main())

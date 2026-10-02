#!/usr/bin/env python3
"""Independent adjacent attacks for C23 v2.3.

The suite separates two questions:

1. can a legitimately rebuilt/pinned future root still admit semantically
   inconsistent evidence; and
2. does the exported decision digest bind the result identities and aggregate
   claims that a downstream reader sees?

The runner never receives test names or expected outcomes.  Expected outcomes
are applied only after the observed result has been produced.
"""

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path


def load_runner(path):
    spec = importlib.util.spec_from_file_location("c23_v23_runner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def reseal(runner, record):
    record["record_digest"] = runner.digest(
        {key: value for key, value in record.items() if key != "record_digest"}
    )


def get_scenario(document, scenario_id="S01"):
    return next(item for item in document["scenarios"] if item["scenario_id"] == scenario_id)


def get_record(document, registry_name, id_key, record_id):
    return next(
        item
        for item in document["registries"][registry_name]
        if item[id_key] == record_id
    )


def repin(runner, document, authority_root):
    authority_root["registries"] = copy.deepcopy(document["registries"])
    authority_root["suite_manifest"] = runner.suite_manifest(
        document["suite"], document["scenarios"]
    )
    authority_root["root_digest"] = runner.digest(runner.root_payload(authority_root))
    runner.PINNED_AUTHORITY_ROOT_DIGEST = authority_root["root_digest"]


def target_row(result, scenario_id="S01"):
    return next(item for item in result["trials"] if item["scenario_id"] == scenario_id)


def mutate_orphan_failed_d21(document, runner):
    source = get_record(document, "d21_registry", "d21_id", "D21.S01")
    extra = copy.deepcopy(source)
    extra["d21_id"] = "D21.UNPROJECTED.FAIL.S01"
    extra["technical"] = "FAIL"
    reseal(runner, extra)
    document["registries"]["d21_registry"].append(extra)


def mutate_reviewer_also_case_author(document, runner):
    principal = next(
        item
        for item in document["registries"]["principal_registry"]
        if item["principal_id"] == "PRINCIPAL.REVIEWER.S01"
    )
    principal["roles"].append("ROLE.CASE.AUTHOR")
    reseal(runner, principal)
    assignment = {
        "assignment_id": "ASSIGNMENT.REVIEWER.AS.AUTHOR.S01",
        "principal_id": "PRINCIPAL.REVIEWER.S01",
        "role": "ROLE.CASE.AUTHOR",
        "subject_id": "SUBJECT.S01",
        "case_record_id": "CASE.RECORD.S01",
        "case_version": 1,
        "valid_from": "2026-09-01T00:00:00Z",
        "valid_until": "2026-10-31T23:59:59Z",
        "status": "ACTIVE",
    }
    reseal(runner, assignment)
    document["registries"]["author_assignment_registry"].append(assignment)


def mutate_assignment_starts_after_publication(document, runner):
    assignment = get_record(
        document,
        "author_assignment_registry",
        "assignment_id",
        "ASSIGNMENT.AUTHOR.S01",
    )
    assignment["valid_from"] = "2026-09-30T11:59:30Z"
    reseal(runner, assignment)


def mutate_trial_time(document, runner, recorded_at):
    trial = get_record(
        document, "trial_registry", "trial_record_id", "TRIAL.RECORD.S01.01"
    )
    trial["recorded_at"] = recorded_at
    reseal(runner, trial)


def mutate_publication_precedes_trials(document, runner):
    reviewer = get_record(document, "reviewer_registry", "reviewer_id", "REVIEWER.S01")
    publication = get_record(
        document, "publication_registry", "publication_id", "PUBLICATION.S01"
    )
    reviewer["reviewed_at"] = "2026-09-30T11:40:00Z"
    publication["released_at"] = "2026-09-30T11:41:00Z"
    reseal(runner, reviewer)
    reseal(runner, publication)


def mutate_pass_trial_points_to_failure(document, runner):
    trial = get_record(
        document, "trial_registry", "trial_record_id", "TRIAL.RECORD.S01.01"
    )
    trial["failure_ref"] = "FAILURE.S01.01"
    reseal(runner, trial)


def mutate_two_failures_share_one_log(document, runner):
    scenario = get_scenario(document)
    trial = get_record(
        document, "trial_registry", "trial_record_id", "TRIAL.RECORD.S01.03"
    )
    trial["status"] = "FAIL"
    trial["failure_ref"] = "FAILURE.S01.02"
    reseal(runner, trial)
    failure = {
        "failure_id": "FAILURE.S01.02",
        "case_record_id": "CASE.RECORD.S01",
        "task_id": "TASK.S01",
        "trial_id": "TRIAL.S01.03",
        "run_id": "RUN.S01",
        "evidence_id": "EVIDENCE.S01",
        "artifact_id": "ARTIFACT.FAILURE.S01",
        "status": "ACTIVE",
    }
    reseal(runner, failure)
    document["registries"]["failure_registry"].append(failure)
    scenario["raw_state"]["failure_refs"].append("FAILURE.S01.02")
    scenario["raw_state"]["failure_count"] = 2


def mutate_unlinked_failure_log(document, runner):
    scenario = get_scenario(document)
    original = get_record(
        document, "artifact_registry", "artifact_id", "ARTIFACT.FAILURE.S01"
    )
    extra = copy.deepcopy(original)
    extra["artifact_id"] = "ARTIFACT.FAILURE.UNLINKED.S01"
    extra["payload"] = {"failures": "unlinked"}
    extra["content_digest"] = runner.digest(extra["payload"])
    reseal(runner, extra)
    document["registries"]["artifact_registry"].append(extra)
    scenario["raw_state"]["artifact_refs"].append(extra["artifact_id"])


def mutate_external_write_hidden_by_false_flag(document, runner):
    effect = get_record(document, "effect_registry", "effect_id", "EFFECT.S01")
    effect["effect_kind"] = "EXTERNAL_WRITE"
    effect["external"] = False
    expected = {
        "effect_id": effect["effect_id"],
        "effect_kind": "EXTERNAL_WRITE",
        "external": False,
        "authorized": True,
        "status": "APPLIED",
    }
    effect["receipt"] = copy.deepcopy(expected)
    effect["readback"] = copy.deepcopy(expected)
    effect["receipt_digest"] = runner.digest(effect["receipt"])
    effect["readback_digest"] = runner.digest(effect["readback"])
    reseal(runner, effect)


def mutate_d21_content_contradiction(document, runner):
    artifact = get_record(
        document, "artifact_registry", "artifact_id", "ARTIFACT.TECHNICAL.S01"
    )
    artifact["payload"] = {"technical": "FAIL"}
    artifact["content_digest"] = runner.digest(artifact["payload"])
    reseal(runner, artifact)


def set_adapter(document, runner, difference):
    migration = get_record(
        document, "migration_registry", "migration_id", "MIGRATION.S01"
    )
    migration["adapter_differences"] = [difference]
    reseal(runner, migration)


def adapter(category, criticality, affected_contract, disposition):
    return {
        "category": category,
        "criticality": criticality,
        "affected_contract": affected_contract,
        "evidence_ref": "ARTIFACT.TECHNICAL.S01",
        "owner": "PRINCIPAL.AUTHORITY.S01",
        "disposition": disposition,
    }


def semantic_attack(runner, base, frozen_root, mutate, expected, scenario_id="S01"):
    document = copy.deepcopy(base)
    authority_root = copy.deepcopy(frozen_root)
    original_pin = runner.PINNED_AUTHORITY_ROOT_DIGEST
    actual = "ERROR"
    reasons = []
    message = ""
    decision_digest = None
    try:
        mutate(document, runner)
        repin(runner, document, authority_root)
        result = runner.evaluate(document, authority_root)
        row = target_row(result, scenario_id)
        actual = row["derived"]["verdict"]
        reasons = row["derived"]["reasons"]
        decision_digest = result["decision_digest"]
    except Exception as error:
        actual = "REJECT"
        message = str(error)
    finally:
        runner.PINNED_AUTHORITY_ROOT_DIGEST = original_pin
    return {
        "actual": actual,
        "reasons": reasons,
        "message": message,
        "decision_digest": decision_digest,
        "secure_contract_passed": actual in expected,
    }


def recompute_decision_digest(runner, result):
    return runner.digest(
        {
            "provenance": result["provenance"],
            "trials": [
                (item["trial_id"], item["derived"]) for item in result["trials"]
            ],
        }
    )


def output_attack(runner, baseline_result, mutate):
    result = copy.deepcopy(baseline_result)
    original_digest = result["decision_digest"]
    mutate(result)
    recomputed = recompute_decision_digest(runner, result)
    changed = recomputed != original_digest
    return {
        "actual": "DIGEST_CHANGED" if changed else "DIGEST_UNCHANGED",
        "reasons": [],
        "message": "",
        "decision_digest": original_digest,
        "recomputed_digest": recomputed,
        "secure_contract_passed": changed,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--authority-root", required=True)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    runner = load_runner(args.runner)
    base = json.loads(Path(args.input).read_text())
    frozen_root = json.loads(Path(args.authority_root).read_text())
    baseline = runner.evaluate(copy.deepcopy(base), copy.deepcopy(frozen_root))

    semantic_tests = [
        (
            "J01_UNPROJECTED_FAILED_D21",
            {"FAIL", "REJECT"},
            mutate_orphan_failed_d21,
        ),
        (
            "J02_REVIEWER_HAS_SECOND_ACTIVE_AUTHOR_ASSIGNMENT",
            {"FAIL", "REJECT"},
            mutate_reviewer_also_case_author,
        ),
        (
            "J03_AUTHOR_ASSIGNMENT_STARTS_AFTER_PUBLICATION",
            {"FAIL", "REJECT"},
            mutate_assignment_starts_after_publication,
        ),
        (
            "J04_TRIAL_RECORDED_AFTER_EVALUATION",
            {"FAIL", "REVIEW_REQUIRED", "REJECT"},
            lambda document, r: mutate_trial_time(
                document, r, "2026-09-30T12:01:00Z"
            ),
        ),
        (
            "J05_TRIAL_RECORDED_BEFORE_AUTHORIZATION",
            {"FAIL", "REVIEW_REQUIRED", "REJECT"},
            lambda document, r: mutate_trial_time(
                document, r, "2026-08-31T23:59:59Z"
            ),
        ),
        (
            "J06_PUBLICATION_AND_REVIEW_PRECEDE_TRIALS",
            {"FAIL", "REVIEW_REQUIRED", "REJECT"},
            mutate_publication_precedes_trials,
        ),
        (
            "J07_PASS_TRIAL_POINTS_TO_ACTIVE_FAILURE",
            {"FAIL", "REJECT"},
            mutate_pass_trial_points_to_failure,
        ),
        (
            "J08_TWO_FAILURES_SHARE_ONE_FAILURE_LOG",
            {"FAIL", "REJECT"},
            mutate_two_failures_share_one_log,
        ),
        (
            "J09_UNLINKED_EXTRA_FAILURE_LOG",
            {"FAIL", "REJECT"},
            mutate_unlinked_failure_log,
        ),
        (
            "J10_EXTERNAL_WRITE_WITH_EXTERNAL_FALSE",
            {"FAIL", "REJECT"},
            mutate_external_write_hidden_by_false_flag,
        ),
        (
            "J11_D21_PASS_WITH_CONTRADICTORY_TECHNICAL_PAYLOAD",
            {"FAIL", "REVIEW_REQUIRED", "REJECT"},
            mutate_d21_content_contradiction,
        ),
        (
            "J12_NONCRITICAL_CATEGORY_WITH_AUTHORITY_CONTRACT",
            {"FAIL", "REJECT"},
            lambda document, r: set_adapter(
                document,
                r,
                adapter(
                    "STATE_CARRIER", "NON_CRITICAL", "AUTHORITY", "REVIEW_REQUIRED"
                ),
            ),
        ),
        (
            "J13_NONCRITICAL_CATEGORY_ACCEPTS_SECURITY_CONTRACT",
            {"FAIL", "REJECT"},
            lambda document, r: set_adapter(
                document,
                r,
                adapter(
                    "TOOL_SCHEMA", "NON_CRITICAL", "SECURITY_BOUNDARY", "ACCEPTED"
                ),
            ),
        ),
        (
            "J14_MESSAGE_CATEGORY_ACCEPTS_D21_TERMINAL_CONTRACT",
            {"FAIL", "REJECT"},
            lambda document, r: set_adapter(
                document,
                r,
                adapter(
                    "MESSAGE_SEMANTICS",
                    "NON_CRITICAL",
                    "D21_TERMINAL",
                    "ACCEPTED",
                ),
            ),
        ),
    ]

    rows = []
    for test_id, expected, mutate in semantic_tests:
        observed = semantic_attack(runner, base, frozen_root, mutate, expected)
        rows.append(
            {
                "test_id": test_id,
                "layer": "authorized_repin_semantics",
                "secure_expected_outcomes": sorted(expected),
                **observed,
            }
        )

    output_tests = [
        (
            "J15_RESULT_SCENARIO_IDENTITY_TAMPER",
            lambda result: result["trials"][0].update(
                scenario_id="SCENARIO.OTHER",
                case_record_id="CASE.RECORD.OTHER",
                task_id="TASK.OTHER",
                run_id="RUN.OTHER",
                evidence_id="EVIDENCE.OTHER",
            ),
        ),
        (
            "J16_RESULT_DISTRIBUTION_TAMPER",
            lambda result: result.__setitem__("distribution", {"PASS": 32}),
        ),
        (
            "J17_RESULT_TRIAL_COUNT_TAMPER",
            lambda result: result.__setitem__("trial_count", 1),
        ),
        (
            "J18_RESULT_ACCEPTED_REAL_COUNT_TAMPER",
            lambda result: result.__setitem__("accepted_real_claim_count", 1),
        ),
        (
            "J19_RESULT_EXTERNAL_EFFECT_COUNT_TAMPER",
            lambda result: result.__setitem__("external_effect_count", 1),
        ),
    ]
    for test_id, mutate in output_tests:
        rows.append(
            {
                "test_id": test_id,
                "layer": "exported_result_integrity",
                "secure_expected_outcomes": ["DIGEST_CHANGED"],
                **output_attack(runner, baseline, mutate),
            }
        )

    payload = {
        "schema_version": "c23.v2.3.independent-adjacent-attacks.v1",
        "input_sha256": sha256_file(args.input),
        "authority_root_file_sha256": sha256_file(args.authority_root),
        "runner_sha256": sha256_file(args.runner),
        "baseline_distribution": baseline["distribution"],
        "baseline_decision_digest": baseline["decision_digest"],
        "test_count": len(rows),
        "secure_contract_passed_count": sum(
            item["secure_contract_passed"] for item in rows
        ),
        "escape_count": sum(not item["secure_contract_passed"] for item in rows),
        "all_secure_contracts_passed": all(
            item["secure_contract_passed"] for item in rows
        ),
        "tests": rows,
    }
    payload["suite_digest"] = runner.digest(
        [
            (
                item["test_id"],
                item["actual"],
                item.get("decision_digest"),
                item.get("recomputed_digest"),
                item["secure_contract_passed"],
            )
            for item in rows
        ]
    )
    Path(args.output).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "test_count",
                    "secure_contract_passed_count",
                    "escape_count",
                    "suite_digest",
                )
            },
            ensure_ascii=False,
        )
    )
    return 0 if payload["all_secure_contracts_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

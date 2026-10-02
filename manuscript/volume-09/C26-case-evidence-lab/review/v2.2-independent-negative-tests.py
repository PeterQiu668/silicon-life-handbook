#!/usr/bin/env python3
"""Independent adjacent attacks for the C23 v2.2 synthetic control.

This script is deliberately outside the author fixture.  It imports the frozen
runner, mutates only an in-memory copy, and writes a review result to an explicit
output path.  A secure result is any non-PASS decision (FAIL,
REVIEW_REQUIRED, or schema/root REJECT) unless the test says otherwise.
"""

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_runner(path):
    spec = importlib.util.spec_from_file_location("c23_v22_runner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reseal(runner, record):
    record["record_digest"] = runner.digest(
        {key: value for key, value in record.items() if key != "record_digest"}
    )


def scenario(document, scenario_id="S01"):
    return next(item for item in document["scenarios"] if item["scenario_id"] == scenario_id)


def registry(document, name, record_id_key, record_id):
    return next(
        item
        for item in document["registries"][name]
        if item[record_id_key] == record_id
    )


def target_verdict(result, target_scenario_id):
    target = next(
        (item for item in result["trials"] if item["scenario_id"] == target_scenario_id),
        None,
    )
    return target["derived"]["verdict"] if target else "MISSING_TARGET"


def root_reseal_reviewer(document, authority_root, runner):
    reviewer = authority_root["registries"]["reviewer_registry"][0]
    reviewer["status"] = "REVOKED"
    reseal(runner, reviewer)
    authority_root["root_digest"] = runner.digest(
        {"registries": authority_root["registries"]}
    )
    document["registries"] = copy.deepcopy(authority_root["registries"])


def root_reseal_registry_order(document, authority_root, runner):
    authority_root["registries"]["artifact_registry"].reverse()
    authority_root["root_digest"] = runner.digest(
        {"registries": authority_root["registries"]}
    )
    document["registries"] = copy.deepcopy(authority_root["registries"])


def input_only_reseal_reviewer(document, authority_root, runner):
    del authority_root
    reviewer = document["registries"]["reviewer_registry"][0]
    reviewer["status"] = "REVOKED"
    reseal(runner, reviewer)


def truncate_to_one_pass_scenario(document, authority_root, runner):
    del authority_root, runner
    document["scenarios"] = [copy.deepcopy(scenario(document, "S01"))]


def cherry_pick_trials(document, authority_root, runner):
    del authority_root, runner
    raw = scenario(document)["raw_state"]
    trials = document["registries"]["trial_registry"]
    selected = [
        item["trial_record_id"]
        for item in trials
        if item["case_record_id"] == "CASE.RECORD.S01" and item["status"] == "PASS"
    ]
    raw["trial_refs"] = selected
    raw["failure_refs"] = []
    raw["trial_count"] = len(selected)
    raw["failure_count"] = 0
    raw["failures_preserved"] = True


def omit_effect_refs(document, authority_root, runner):
    del authority_root, runner
    scenario(document)["raw_state"]["effect_refs"] = []


def omit_failure_artifact(document, authority_root, runner):
    del authority_root, runner
    raw = scenario(document)["raw_state"]
    raw["artifact_refs"] = [
        ref for ref in raw["artifact_refs"] if ref != "ARTIFACT.FAILURE.S01"
    ]


def retain_only_public_artifact(document, authority_root, runner):
    del authority_root, runner
    scenario(document)["raw_state"]["artifact_refs"] = ["ARTIFACT.PUBLIC.S01"]


def cross_case_author(document, authority_root, runner):
    del authority_root, runner
    scenario(document)["raw_state"]["author_principal_id"] = "PRINCIPAL.AUTHOR.S17"


def shift_evaluation_time(document, authority_root, runner):
    del authority_root, runner
    document["suite"]["evaluation_time"] = "2026-09-30T11:59:30Z"


def rename_build(document, authority_root, runner):
    del authority_root, runner
    document["suite"]["build_id"] = "BUILD.C23.UNROOTED.RENAMED"


def rename_scenario(document, authority_root, runner):
    del authority_root, runner
    scenario(document)["scenario_id"] = "SYNTHETIC.SCENARIO.RENAMED"


def missing_publication_ref(document, authority_root, runner):
    del authority_root, runner
    scenario(document)["raw_state"]["publication_ref"] = "PUBLICATION.MISSING.S01"


def cross_case_budget_ref(document, authority_root, runner):
    del authority_root, runner
    scenario(document)["raw_state"]["candidate_budget_ref"] = "BUDGET.CANDIDATE.S17"


def cross_case_effect_ref(document, authority_root, runner):
    del authority_root, runner
    scenario(document)["raw_state"]["effect_refs"] = ["EFFECT.S17"]


def cross_case_reviewer_ref(document, authority_root, runner):
    del authority_root, runner
    scenario(document)["raw_state"]["reviewer_ref"] = "REVIEWER.S17"


def self_report_verified_real(document, authority_root, runner):
    del authority_root
    identity = registry(
        document, "case_identity_registry", "identity_id", "IDENTITY.S01"
    )
    identity["case_type"] = "VERIFIED-REAL"
    reseal(runner, identity)


def authorized_repin_critical_adapter_synonym(document, authority_root, runner):
    """Simulate a legitimate future root update, not an input-only attacker.

    The current hard pin correctly blocks arbitrary root replacement.  This
    probe asks whether the adapter criticality rule remains safe after the
    operator deliberately publishes a newly pinned root containing a semantic
    synonym that does not include the runner's current substring tokens.
    """
    migration = registry(
        authority_root, "migration_registry", "migration_id", "MIGRATION.S01"
    )
    migration["adapter_differences"] = ["PRIVILEGE.BOUNDARY.DIFFERS"]
    reseal(runner, migration)
    authority_root["root_digest"] = runner.digest(
        {"registries": authority_root["registries"]}
    )
    document["registries"] = copy.deepcopy(authority_root["registries"])
    runner.PINNED_AUTHORITY_ROOT_DIGEST = authority_root["root_digest"]


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

    # expected_outcomes describes the secure contract, not the observed fixture.
    tests = [
        ("I01_PINNED_ROOT_RECORD_RESEAL", {"REJECT"}, root_reseal_reviewer, "S01"),
        ("I02_PINNED_ROOT_ORDER_RESEAL", {"REJECT"}, root_reseal_registry_order, "S01"),
        ("I03_INPUT_ONLY_RECORD_RESEAL", {"FAIL"}, input_only_reseal_reviewer, "S01"),
        ("I04_SCENARIO_INVENTORY_TRUNCATED", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, truncate_to_one_pass_scenario, "S01"),
        ("I05_FAILURE_TRIAL_CHERRY_PICKED", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, cherry_pick_trials, "S01"),
        ("I06_EFFECT_EVIDENCE_OMITTED", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, omit_effect_refs, "S01"),
        ("I07_FAILURE_ARTIFACT_OMITTED", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, omit_failure_artifact, "S01"),
        ("I08_ONLY_PUBLIC_ARTIFACT_RETAINED", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, retain_only_public_artifact, "S01"),
        ("I09_CROSS_CASE_AUTHOR_SUBSTITUTED", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, cross_case_author, "S01"),
        ("I10_EVALUATION_TIME_UNROOTED_SHIFT", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, shift_evaluation_time, "S01"),
        ("I11_BUILD_ID_UNROOTED_RENAME", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, rename_build, "S01"),
        ("I12_SCENARIO_ID_UNROOTED_RENAME", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, rename_scenario, "SYNTHETIC.SCENARIO.RENAMED"),
        ("I13_PUBLICATION_REF_UNRESOLVED", {"REVIEW_REQUIRED", "FAIL", "REJECT"}, missing_publication_ref, "S01"),
        ("I14_CROSS_CASE_BUDGET_REF", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, cross_case_budget_ref, "S01"),
        ("I15_CROSS_CASE_EFFECT_REF", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, cross_case_effect_ref, "S01"),
        ("I16_INPUT_SELF_REPORTS_VERIFIED_REAL", {"REJECT"}, self_report_verified_real, "S01"),
        ("I17_CROSS_CASE_REVIEWER_REF", {"FAIL", "REVIEW_REQUIRED", "REJECT"}, cross_case_reviewer_ref, "S01"),
        ("I18_AUTHORIZED_REPIN_CRITICAL_ADAPTER_SYNONYM", {"FAIL"}, authorized_repin_critical_adapter_synonym, "S01"),
    ]

    details = []
    for test_id, expected_outcomes, mutate, target_scenario_id in tests:
        document = copy.deepcopy(base)
        authority_root = copy.deepcopy(frozen_root)
        observed = "ERROR"
        message = ""
        distribution = None
        decision_digest = None
        original_pin = runner.PINNED_AUTHORITY_ROOT_DIGEST
        try:
            mutate(document, authority_root, runner)
            result = runner.evaluate(document, authority_root)
            observed = target_verdict(result, target_scenario_id)
            distribution = result["distribution"]
            decision_digest = result["decision_digest"]
        except Exception as error:
            observed = "REJECT"
            message = str(error)
        finally:
            runner.PINNED_AUTHORITY_ROOT_DIGEST = original_pin
        details.append(
            {
                "test_id": test_id,
                "secure_expected_outcomes": sorted(expected_outcomes),
                "observed": observed,
                "secure_contract_passed": observed in expected_outcomes,
                "message": message,
                "distribution": distribution,
                "decision_digest": decision_digest,
            }
        )

    output = {
        "schema_version": "c23.v2.2.independent-adjacent-attacks.v1",
        "author_input_sha256": sha256_file(args.input),
        "authority_root_file_sha256": sha256_file(args.authority_root),
        "runner_sha256": sha256_file(args.runner),
        "test_count": len(details),
        "secure_contract_passed_count": sum(
            item["secure_contract_passed"] for item in details
        ),
        "secure_contract_failed_count": sum(
            not item["secure_contract_passed"] for item in details
        ),
        "all_secure_contracts_passed": all(
            item["secure_contract_passed"] for item in details
        ),
        "tests": details,
    }
    Path(args.output).write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    print(
        f"{output['secure_contract_passed_count']}/{output['test_count']} secure contracts"
    )
    if not output["all_secure_contracts_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

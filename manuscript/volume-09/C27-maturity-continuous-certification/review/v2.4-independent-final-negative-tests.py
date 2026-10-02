#!/usr/bin/env python3
"""C24 v2.4 non-author, unannounced near-neighbour review tests.

The oracle is defined by certification causality, frozen revocation, post-change
lineage, and persisted-result provenance.  It does not read fixture names or an
author-provided expected field.  Semantic attacks intentionally bypass only the
pinned fixture digest so that a frozen-root rejection cannot conceal fail-open
rules; persisted-result attacks use the public verifier exactly as shipped.
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
    spec = importlib.util.spec_from_file_location("c24_v24_independent_final_runner", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--authority", required=True)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    authority_path = Path(args.authority)
    runner_path = Path(args.runner)
    result_path = Path(args.result)
    runner = load(runner_path)
    source = runner.validate(runner.strict_json_loads(input_path.read_text()), runner.validate_authority(runner.strict_json_loads(authority_path.read_text())))
    authority = runner.validate_authority(runner.strict_json_loads(authority_path.read_text()))
    saved = runner.strict_json_loads(result_path.read_text())
    runner.verify_result(copy.deepcopy(saved), authority, source)
    by_id = {row["scenario_id"]: row for row in source["scenarios"]}
    active_id = next(row["scenario_id"] for row in saved["trials"] if row["decision"] == "PASS" and row["lifecycle"] == "ACTIVE")
    active = by_id[active_id]
    revoked_authority_id = authority["revoked_authority_ids"][0]
    attacks = []

    def seal(row, field="record_digest"):
        row[field] = runner.sha({key: value for key, value in row.items() if key != field})

    def semantic(test_id, family, mutate):
        scenario = copy.deepcopy(active)
        state = scenario["state"]
        decision, lifecycle, reasons, message = "ERROR", "REVOKED", [], ""
        try:
            mutate(state)
            checked = runner.validate_state(state, "v24-independent." + test_id)
            decision, lifecycle, reasons, *_ = runner.evaluate(source, checked, scenario["layer"], authority)
        except (ValueError, TypeError, KeyError) as exc:
            decision, lifecycle, reasons, message = "SCHEMA_REJECT", "REVOKED", [str(exc)], str(exc)
        secure = decision != "PASS"
        attacks.append({
            "test_id": test_id,
            "family": family,
            "layer": "semantic_legal_reseal",
            "actual_decision": decision,
            "actual_lifecycle": lifecycle,
            "actual_reasons": reasons,
            "secure_contract_passed": secure,
            "escape": not secure,
            "message": message,
        })

    def evidence(state, kind):
        return next(row for row in state["evidence_registry"].values() if row["kind"] == kind)

    def output_before_trial(state):
        trial = sorted(state["trial_registry"].values(), key=lambda row: row["trial_id"])[0]
        row = state["evidence_registry"][trial["output_ref"]]
        row["issued_at"] = "2026-09-30T11:10:00Z"
        seal(row)

    def preregister_grader_after_trials(state):
        row = evidence(state, "grader_preregistration")
        row["issued_at"] = "2026-09-30T11:20:00Z"
        seal(row)

    def holdout_lineage_after_trials(state):
        row = evidence(state, "holdout_lineage")
        row["issued_at"] = "2026-09-30T11:20:00Z"
        seal(row)

    def signature_after_review(state):
        row = evidence(state, "application_signature")
        row["issued_at"] = "2026-09-30T11:40:00Z"
        seal(row)

    def trial_finishes_after_review(state):
        trial = sorted(state["trial_registry"].values(), key=lambda row: row["trial_id"])[0]
        trial["completed_at"] = "2026-09-30T11:40:00Z"
        seal(trial)
        row = state["evidence_registry"][trial["output_ref"]]
        row["issued_at"] = "2026-09-30T11:41:00Z"
        seal(row)

    def maturity_after_review(state):
        maturity = state["maturity"]
        maturity["issued_at"] = "2026-09-30T11:40:00Z"
        seal(maturity)
        cert = state["certificate_registry"][state["certificate_ref"]]
        cert["maturity_digest"] = maturity["record_digest"]
        seal(cert)

    def namespace_after_review(state):
        namespace = state["namespace"]
        namespace["issued_at"] = "2026-09-30T11:40:00Z"
        seal(namespace)
        cert = state["certificate_registry"][state["certificate_ref"]]
        cert["namespace_digest"] = namespace["record_digest"]
        seal(cert)

    def reuse_revoked_authority(state, action):
        registry = state["authority_registry"]
        old_id, row = next((key, value) for key, value in registry.items() if value["action"] == action)
        del registry[old_id]
        row["authority_id"] = revoked_authority_id
        seal(row)
        registry[revoked_authority_id] = row
        if action == "operate_synthetic_scope":
            state["namespace"]["authorization_ref"] = revoked_authority_id
            seal(state["namespace"])
            cert = state["certificate_registry"][state["certificate_ref"]]
            cert["namespace_digest"] = state["namespace"]["record_digest"]
            seal(cert)
        elif action == "change_certificate_lifecycle":
            state["lifecycle"]["authority_ref"] = revoked_authority_id
            seal(state["lifecycle"])
        elif action == "approve_material_change":
            state["change"]["authority_ref"] = revoked_authority_id
            seal(state["change"])

    def full_recert(state):
        app, change = state["application"], state["change"]
        change_at = "2026-09-30T11:05:00Z"
        trials = sorted(state["trial_registry"].values(), key=lambda row: {"training": 0, "regression": 1, "holdout": 2}[row["layer"]])
        completed = ["2026-09-30T11:20:00Z", "2026-09-30T11:21:00Z", "2026-09-30T11:22:00Z"]
        issued = ["2026-09-30T11:23:00Z", "2026-09-30T11:24:00Z", "2026-09-30T11:25:00Z"]
        entries = []
        for trial, completed_at, issued_at in zip(trials, completed, issued):
            trial["completed_at"] = completed_at
            seal(trial)
            output = state["evidence_registry"][trial["output_ref"]]
            output["issued_at"] = issued_at
            seal(output)
            entries.append({
                "trial_ref": trial["trial_id"],
                "evidence_ref": output["evidence_id"],
                "layer": trial["layer"],
                "security_slices": ["certification-redteam"],
                "affected_scopes": ["MODEL"],
            })
        manifest = {
            "manifest_id": "RETEST-MANIFEST-INDEPENDENT-V24",
            "change_id": change["change_id"],
            "pre_change_release": "openclaw@prechange-2026.9.5",
            "post_change_release": app["release"],
            "affected_scopes": ["MODEL"],
            "required_layers": ["training", "regression", "holdout"],
            "required_security_slices": ["certification-redteam"],
            "entries": entries,
        }
        manifest["manifest_digest"] = runner.sha(manifest)
        review_ref = next(iter(state["review_registry"]))
        change.update(
            material=True,
            kind="MODEL",
            impact_review="PASS",
            retest="PASS",
            issued_at=change_at,
            affected_scopes=["MODEL"],
            post_change_release=app["release"],
            retest_trial_refs=[row["trial_ref"] for row in entries],
            retest_evidence_refs=[row["evidence_ref"] for row in entries],
            retest_review_ref=review_ref,
            retest_manifest=manifest,
        )
        seal(change)
        row = state["evidence_registry"][change["evidence_ref"]]
        row["content_digest"] = runner.sha(runner.change_payload(app, change))
        seal(row)

    def reseal_change(state):
        change = state["change"]
        manifest = change["retest_manifest"]
        manifest["manifest_digest"] = runner.sha({key: value for key, value in manifest.items() if key != "manifest_digest"})
        seal(change)
        row = state["evidence_registry"][change["evidence_ref"]]
        row["content_digest"] = runner.sha(runner.change_payload(state["application"], change))
        seal(row)

    def security_not_cross_cutting(state):
        full_recert(state)
        entries = state["change"]["retest_manifest"]["entries"]
        entries[1]["security_slices"] = []
        entries[2]["security_slices"] = []
        reseal_change(state)

    def fabricated_prechange_release(state):
        full_recert(state)
        state["change"]["retest_manifest"]["pre_change_release"] = "fabricated-runtime@never-existed"
        reseal_change(state)

    def postchange_output_predates_trial(state):
        full_recert(state)
        entry = state["change"]["retest_manifest"]["entries"][0]
        output = state["evidence_registry"][entry["evidence_ref"]]
        output["issued_at"] = "2026-09-30T11:19:00Z"
        seal(output)
        reseal_change(state)

    semantic("N01_TRIAL_OUTPUT_PRECEDES_TRIAL", "causal-evidence", output_before_trial)
    semantic("N02_GRADER_PREREGISTRATION_AFTER_TRIALS", "causal-evidence", preregister_grader_after_trials)
    semantic("N03_HOLDOUT_LINEAGE_AFTER_TRIALS", "causal-evidence", holdout_lineage_after_trials)
    semantic("N04_APPLICATION_SIGNATURE_AFTER_REVIEW", "causal-evidence", signature_after_review)
    semantic("N05_TRIAL_COMPLETES_AFTER_REVIEW", "causal-review", trial_finishes_after_review)
    semantic("N06_MATURITY_ISSUED_AFTER_REVIEW", "causal-review", maturity_after_review)
    semantic("N07_NAMESPACE_ISSUED_AFTER_REVIEW", "causal-review", namespace_after_review)
    semantic("N08_ROOT_REVOKED_OPERATING_AUTHORITY_REUSED", "frozen-revocation", lambda state: reuse_revoked_authority(state, "operate_synthetic_scope"))
    semantic("N09_ROOT_REVOKED_LIFECYCLE_AUTHORITY_REUSED", "frozen-revocation", lambda state: reuse_revoked_authority(state, "change_certificate_lifecycle"))
    semantic("N10_ROOT_REVOKED_CHANGE_AUTHORITY_REUSED", "frozen-revocation", lambda state: reuse_revoked_authority(state, "approve_material_change"))
    semantic("N11_SECURITY_SLICE_ONLY_ONE_RETEST_LAYER", "post-change-lineage", security_not_cross_cutting)
    semantic("N12_FABRICATED_PRECHANGE_RELEASE", "post-change-lineage", fabricated_prechange_release)
    semantic("N13_POSTCHANGE_OUTPUT_PRECEDES_TRIAL", "post-change-lineage", postchange_output_predates_trial)

    def active_expiry_at_evaluation(state):
        cert = state["certificate_registry"][state["certificate_ref"]]
        cert["expires_at"] = source["now"]
        seal(cert)

    def lifecycle_before_certificate(state):
        life = state["lifecycle"]
        life["occurred_at"] = "2026-09-30T11:49:59Z"
        seal(life)
        row = state["evidence_registry"][life["evidence_ref"]]
        row["issued_at"] = "2026-09-30T11:49:58Z"
        row["content_digest"] = runner.sha(runner.lifecycle_payload(life))
        seal(row)

    def artifact_after_certificate(state):
        row = evidence(state, "artifact")
        row["issued_at"] = "2026-09-30T11:50:01Z"
        seal(row)

    def appeal_reviewer_aliases_author(state):
        app = state["application"]
        author = state["principal_registry"][app["author"]]
        author["roles"] = sorted(set(author["roles"] + ["appeal_reviewer"]))
        seal(author)
        appeal = next(iter(state["appeal_registry"].values()))
        appeal.update(opened=True, reviewer=app["author"], decision="PASS")
        seal(appeal)
        auth = next(row for row in state["authority_registry"].values() if row["action"] == "decide_appeal")
        auth["actor"] = app["author"]
        seal(auth)

    def alias_collision(state):
        principals = list(state["principal_registry"].values())
        principals[0]["aliases"] = ["SHARED-ALIAS-INDEPENDENT"]
        principals[1]["aliases"] = ["SHARED-ALIAS-INDEPENDENT"]
        seal(principals[0])
        seal(principals[1])

    def external_failed_hides_applied(state):
        app = state["application"]
        observation = {"effect_id": "EFFECT-INDEPENDENT-V24", "status": "APPLIED", "external": True, "environment": "external"}
        effect = {
            "effect_id": observation["effect_id"],
            "application_id": app["application_id"],
            "external": True,
            "status": "FAILED",
            "environment": "external",
            "receipt": copy.deepcopy(observation),
            "receipt_digest": runner.sha(observation),
            "readback": copy.deepcopy(observation),
            "readback_digest": runner.sha(observation),
            "record_digest": "",
        }
        seal(effect)
        state["effect_ledger"] = [effect]

    semantic("N14_ACTIVE_CERTIFICATE_EXPIRES_AT_EVALUATION", "certificate-window", active_expiry_at_evaluation)
    semantic("N15_LIFECYCLE_EVENT_PRECEDES_CERTIFICATE", "lifecycle-causality", lifecycle_before_certificate)
    semantic("N16_ARTIFACT_ISSUED_AFTER_CERTIFICATE", "artifact-causality", artifact_after_certificate)
    semantic("N17_APPEAL_REVIEWER_ALIASES_AUTHOR", "principal-independence", appeal_reviewer_aliases_author)
    semantic("N18_PRINCIPAL_ALIAS_COLLISION", "principal-canonicalization", alias_collision)
    semantic("N19_EXTERNAL_FAILED_HIDES_APPLIED", "external-effect-derivation", external_failed_hides_applied)

    def source_attack(test_id, family, mutate):
        candidate = copy.deepcopy(source)
        mutate(candidate)
        actual, message = "ACCEPTED", ""
        try:
            runner.validate(candidate, authority)
        except (ValueError, TypeError, KeyError) as exc:
            actual, message = "REJECT", str(exc)
        secure = actual == "REJECT"
        attacks.append({
            "test_id": test_id,
            "family": family,
            "layer": "source-authority-boundary",
            "actual": actual,
            "secure_contract_passed": secure,
            "escape": not secure,
            "message": message,
        })

    source_attack("N20_TRUSTED_CLOCK_PLUS_ONE_SECOND", "trusted-clock", lambda row: row.update(now="2026-09-30T12:00:01Z"))

    def result_attack(test_id, family, mutate):
        candidate = copy.deepcopy(saved)
        mutate(candidate)
        candidate["decision_digest"] = runner.sha(runner.result_payload(candidate))
        actual, message = "ACCEPTED", ""
        try:
            runner.verify_result(candidate, authority, source)
        except (ValueError, TypeError, KeyError) as exc:
            actual, message = "REJECT", str(exc)
        secure = actual == "REJECT"
        attacks.append({
            "test_id": test_id,
            "family": family,
            "layer": "persisted-result-verifier",
            "actual": actual,
            "secure_contract_passed": secure,
            "escape": not secure,
            "message": message,
        })

    result_attack("N21_RESULT_INPUT_SHA256_BLANK_REHASH", "result-provenance", lambda row: row.update(input_sha256=""))
    result_attack("N22_RESULT_AUTHORITY_SHA256_BLANK_REHASH", "result-provenance", lambda row: row.update(authority_sha256=""))
    result_attack("N23_RESULT_INPUT_SHA256_SWAPPED_REHASH", "result-provenance", lambda row: row.update(input_sha256=row["authority_sha256"]))
    result_attack("N24_RESULT_AUTHORITY_SHA256_SWAPPED_REHASH", "result-provenance", lambda row: row.update(authority_sha256=row["input_sha256"]))

    def flip_fail_to_pass(row):
        trial = next(item for item in row["trials"] if item["decision"] == "FAIL")
        trial.update(decision="PASS", lifecycle="ACTIVE", reasons=[])
        row["distribution"] = dict(sorted(Counter(item["decision"] for item in row["trials"]).items()))
        row["lifecycle_distribution"] = dict(sorted(Counter(item["lifecycle"] for item in row["trials"]).items()))

    result_attack("N25_RESULT_FAIL_TO_PASS_FULL_REHASH", "result-semantic-replay", flip_fail_to_pass)
    result_attack("N26_RESULT_REAL_SUCCESS_COUNTER_REHASH", "success-count", lambda row: (row["trials"][0].update(successful_real_certificates=1), row.update(successful_real_certificates=1)))

    def serialized_attack(test_id, family, raw, kind):
        actual, message = "ACCEPTED", ""
        try:
            parsed = runner.strict_json_loads(raw)
            if kind == "input":
                runner.validate(parsed, authority)
            elif kind == "authority":
                runner.validate_authority(parsed)
            else:
                runner.verify_result(parsed, authority, source)
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            actual, message = "REJECT", str(exc)
        secure = actual == "REJECT"
        attacks.append({
            "test_id": test_id,
            "family": family,
            "layer": "serialized-json-boundary",
            "actual": actual,
            "secure_contract_passed": secure,
            "escape": not secure,
            "message": message,
        })

    input_text = input_path.read_text()
    authority_text = authority_path.read_text()
    result_text = result_path.read_text()
    serialized_attack("N27_INPUT_DUPLICATE_NESTED_SCOPE", "json-duplicate-key", input_text.replace('"scope": "research-draft"', '"scope": "attacker-scope",\n          "scope": "research-draft"', 1), "input")
    serialized_attack("N28_AUTHORITY_DUPLICATE_NESTED_DECISION", "json-duplicate-key", authority_text.replace('"decision": "PASS"', '"decision": "FAIL",\n      "decision": "PASS"', 1), "authority")
    serialized_attack("N29_RESULT_DUPLICATE_NESTED_STATE_DIGEST", "json-duplicate-key", result_text.replace('"state_digest":', '"state_digest": "sha256:' + '0' * 64 + '",\n      "state_digest":', 1), "result")

    positives = []

    def positive(test_id, mutate):
        scenario = copy.deepcopy(active)
        state = scenario["state"]
        decision, lifecycle, reasons = "ERROR", "REVOKED", []
        try:
            mutate(state)
            checked = runner.validate_state(state, "v24-independent-positive." + test_id)
            decision, lifecycle, reasons, *_ = runner.evaluate(source, checked, scenario["layer"], authority)
        except (ValueError, TypeError, KeyError) as exc:
            reasons = [str(exc)]
        positives.append({"test_id": test_id, "decision": decision, "lifecycle": lifecycle, "reasons": reasons, "passed": decision == "PASS"})

    positive("P01_UNCHANGED_ACTIVE", lambda state: None)

    def legal_renewal(state):
        cert = state["certificate_registry"][state["certificate_ref"]]
        cert["issued_at"] = "2026-09-30T11:52:00Z"
        cert["expires_at"] = "2026-10-20T00:00:00Z"
        seal(cert)

    positive("P02_LEGAL_RENEWAL", legal_renewal)
    positive("P03_COMPLETE_THREE_LAYER_RECERTIFICATION", full_recert)

    payload = {
        "schema": "c24.cert.v2.4-independent-final-negative.v1",
        "review_role": "non_author",
        "oracle_source": "reviewer_defined_without_fixture_expected",
        "scope": "offline_synthetic_semantic_and_result_provenance",
        "input_sha256": "sha256:" + hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "authority_sha256": "sha256:" + hashlib.sha256(authority_path.read_bytes()).hexdigest(),
        "runner_sha256": "sha256:" + hashlib.sha256(runner_path.read_bytes()).hexdigest(),
        "result_sha256": "sha256:" + hashlib.sha256(result_path.read_bytes()).hexdigest(),
        "attack_count": len(attacks),
        "secure_count": sum(row["secure_contract_passed"] for row in attacks),
        "escape_count": sum(row["escape"] for row in attacks),
        "positive_count": len(positives),
        "positive_pass_count": sum(row["passed"] for row in positives),
        "attacks": attacks,
        "positive_controls": positives,
        "limits": {
            "real_runtime_executed": False,
            "real_certificate_issued": False,
            "real_external_effect_executed": False,
            "practice_gate": "REVIEW_REQUIRED",
            "editor_chief_rc": "NOT_AUTHORIZED",
        },
    }
    payload["suite_digest"] = runner.sha({"attacks": attacks, "positive_controls": positives})
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in ("attack_count", "secure_count", "escape_count", "positive_count", "positive_pass_count", "suite_digest")}, ensure_ascii=False))
    return 0 if payload["escape_count"] == 0 and payload["positive_pass_count"] == payload["positive_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

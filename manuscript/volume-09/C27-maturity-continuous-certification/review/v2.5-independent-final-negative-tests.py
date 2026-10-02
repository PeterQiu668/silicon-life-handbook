#!/usr/bin/env python3
"""C24 v2.5 non-author final adversarial review.

This program deliberately uses an oracle that is independent of fixture names
and author ``expected`` fields.  Semantic mutations are evaluated against the
shipped closed-world controller after schema validation.  Persisted-result
mutations are evaluated through the shipped result verifier.  A mutation is an
escape only when an invalid state/result is accepted as PASS/valid.
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
    spec = importlib.util.spec_from_file_location("c24_v25_independent_runner", path)
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

    runner = load(Path(args.runner))
    authority_text = Path(args.authority).read_text()
    input_text = Path(args.input).read_text()
    result_text = Path(args.result).read_text()
    authority = runner.validate_authority(runner.strict_json_loads(authority_text))
    source = runner.validate(runner.strict_json_loads(input_text), authority)
    saved = runner.strict_json_loads(result_text)
    runner.verify_result(copy.deepcopy(saved), authority, source)
    by_id = {row["scenario_id"]: row for row in source["scenarios"]}
    active_id = next(
        row["scenario_id"]
        for row in saved["trials"]
        if row["decision"] == "PASS" and row["lifecycle"] == "ACTIVE"
    )
    active = by_id[active_id]
    attacks: list[dict] = []
    positives: list[dict] = []

    def seal(row: dict, field: str = "record_digest") -> None:
        row[field] = runner.sha({key: value for key, value in row.items() if key != field})

    def evidence(state: dict, kind: str) -> dict:
        return next(row for row in state["evidence_registry"].values() if row["kind"] == kind)

    def semantic(test_id: str, family: str, mutate, base=None) -> None:
        scenario = copy.deepcopy(base or active)
        state = scenario["state"]
        decision, lifecycle, reasons, message = "ERROR", "REVOKED", [], ""
        try:
            mutate(state)
            checked = runner.validate_state(state, "v25-independent." + test_id)
            decision, lifecycle, reasons, *_ = runner.evaluate(
                source, checked, scenario["layer"], authority
            )
        except (ValueError, TypeError, KeyError) as exc:
            decision, lifecycle, reasons, message = (
                "SCHEMA_REJECT",
                "REVOKED",
                [str(exc)],
                str(exc),
            )
        secure = decision != "PASS"
        attacks.append(
            {
                "test_id": test_id,
                "family": family,
                "channel": "semantic_legal_reseal",
                "actual_decision": decision,
                "actual_lifecycle": lifecycle,
                "actual_reasons": reasons,
                "secure_contract_passed": secure,
                "escape": not secure,
                "message": message,
            }
        )

    def result_attack(test_id: str, family: str, mutate, *, omit_roots=False) -> None:
        candidate = copy.deepcopy(saved)
        accepted, message = False, ""
        try:
            mutate(candidate)
            if omit_roots:
                runner.verify_result(candidate)
            else:
                runner.verify_result(candidate, authority, source)
            accepted = True
        except (ValueError, TypeError, KeyError) as exc:
            message = str(exc)
        attacks.append(
            {
                "test_id": test_id,
                "family": family,
                "channel": "persisted_result_verifier",
                "actual_decision": "ACCEPTED" if accepted else "REJECTED",
                "actual_lifecycle": "N/A",
                "actual_reasons": [],
                "secure_contract_passed": not accepted,
                "escape": accepted,
                "message": message,
            }
        )

    def parse_attack(test_id: str, family: str, text: str, validator) -> None:
        accepted, message = False, ""
        try:
            validator(runner.strict_json_loads(text))
            accepted = True
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            message = str(exc)
        attacks.append(
            {
                "test_id": test_id,
                "family": family,
                "channel": "raw_json_parser",
                "actual_decision": "ACCEPTED" if accepted else "REJECTED",
                "actual_lifecycle": "N/A",
                "actual_reasons": [],
                "secure_contract_passed": not accepted,
                "escape": accepted,
                "message": message,
            }
        )

    # Full causal graph: evidence cannot exist before the event/state it claims
    # to summarize.  Moving already-early records even earlier makes each test
    # an explicit mutation rather than an observation-only assertion.
    def move_kind(state, kind, when):
        row = evidence(state, kind)
        row["issued_at"] = when
        seal(row)

    semantic("N01_ARTIFACT_PRECEDES_TRIALS", "causal-order", lambda s: move_kind(s, "artifact", "2026-09-30T10:00:00Z"))
    semantic("N02_FAILURE_ARCHIVE_PRECEDES_TRIALS", "causal-order", lambda s: move_kind(s, "failure_archive", "2026-09-30T10:01:00Z"))
    semantic("N03_COST_LEDGER_PRECEDES_TRIALS", "causal-order", lambda s: move_kind(s, "cost_ledger", "2026-09-30T10:02:00Z"))
    semantic("N04_MANIFEST_PRECEDES_DEPENDENT_RECORDS", "causal-order", lambda s: move_kind(s, "manifest", "2026-09-30T09:59:00Z"))
    semantic("N05_D21_TECHNICAL_PRECEDES_TRIALS", "causal-order", lambda s: move_kind(s, "d21_technical", "2026-09-30T10:03:00Z"))
    semantic("N06_D21_DELIVERY_PRECEDES_ARTIFACT", "causal-order", lambda s: move_kind(s, "d21_delivery", "2026-09-30T10:04:00Z"))
    semantic("N07_D21_BUSINESS_PRECEDES_ENVIRONMENT_OUTCOME", "causal-order", lambda s: move_kind(s, "d21_business_environment", "2026-09-30T10:05:00Z"))
    semantic("N08_CHANGE_EVIDENCE_PRECEDES_CHANGE", "causal-order", lambda s: move_kind(s, "change_review", "2026-09-30T10:06:00Z"))
    semantic("N09_PUBLIC_CLAIM_PRECEDES_CERTIFICATE", "causal-order", lambda s: move_kind(s, "public_claim", "2026-09-30T10:07:00Z"))
    semantic("N10_LIFECYCLE_EVIDENCE_PRECEDES_LIFECYCLE", "causal-order", lambda s: move_kind(s, "lifecycle_event", "2026-09-30T10:08:00Z"))

    def output_equals_completion(state):
        trial = sorted(state["trial_registry"].values(), key=lambda row: row["trial_id"])[0]
        output = state["evidence_registry"][trial["output_ref"]]
        output["issued_at"] = trial["completed_at"]
        seal(output)

    def prereg_equals_first_trial(state, kind):
        first = min(row["completed_at"] for row in state["trial_registry"].values())
        row = evidence(state, kind)
        row["issued_at"] = first
        seal(row)

    def dependency_equals_review(state, target):
        review_time = next(iter(state["review_registry"].values()))["issued_at"]
        if target == "maturity":
            state["maturity"]["issued_at"] = review_time
            seal(state["maturity"])
            cert = state["certificate_registry"][state["certificate_ref"]]
            cert["maturity_digest"] = state["maturity"]["record_digest"]
            seal(cert)
        elif target == "namespace":
            state["namespace"]["issued_at"] = review_time
            seal(state["namespace"])
            cert = state["certificate_registry"][state["certificate_ref"]]
            cert["namespace_digest"] = state["namespace"]["record_digest"]
            seal(cert)
        else:
            move_kind(state, target, review_time)

    semantic("N11_OUTPUT_EQUALS_COMPLETION_NO_ORDER_PROOF", "causal-boundary", output_equals_completion)
    semantic("N12_HOLDOUT_EQUALS_FIRST_TRIAL_NO_PREREG_ORDER", "causal-boundary", lambda s: prereg_equals_first_trial(s, "holdout_lineage"))
    semantic("N13_GRADER_EQUALS_FIRST_TRIAL_NO_PREREG_ORDER", "causal-boundary", lambda s: prereg_equals_first_trial(s, "grader_preregistration"))
    semantic("N14_MATURITY_EQUALS_REVIEW_NO_CONSUMPTION_ORDER", "causal-boundary", lambda s: dependency_equals_review(s, "maturity"))
    semantic("N15_NAMESPACE_EQUALS_REVIEW_NO_CONSUMPTION_ORDER", "causal-boundary", lambda s: dependency_equals_review(s, "namespace"))
    semantic("N16_D21_EQUALS_REVIEW_NO_CONSUMPTION_ORDER", "causal-boundary", lambda s: dependency_equals_review(s, "d21_technical"))

    # A frozen authority actor must not become valid merely because the local
    # scenario supplies or aliases a principal record after the root was made.
    bad_actor = copy.deepcopy(by_id["S24-004"])

    def alias_unknown_actor(state):
        row = state["principal_registry"]["CERTIFIER-004"]
        row["aliases"].append("UNKNOWN")
        seal(row)

    def materialize_unknown_actor(state):
        template = copy.deepcopy(state["principal_registry"]["CERTIFIER-004"])
        template.update(principal_id="UNKNOWN", aliases=[])
        seal(template)
        state["principal_registry"]["UNKNOWN"] = template
        cert = state["certificate_registry"][state["certificate_ref"]]
        cert["signer"] = "UNKNOWN"
        seal(cert)

    semantic("N17_UNKNOWN_ROOT_ACTOR_ALIASED_LOCALLY", "authority-shadow", alias_unknown_actor, bad_actor)
    semantic("N18_UNKNOWN_ROOT_ACTOR_MATERIALIZED_LOCALLY", "authority-shadow", materialize_unknown_actor, bad_actor)

    # Revoked/stale authority and principal changes should remain non-PASS.
    def revoke_certifier_locally(state):
        row = state["principal_registry"]["CERTIFIER-002"]
        row["status"] = "REVOKED"
        seal(row)

    def expire_certifier_locally(state):
        row = state["principal_registry"]["CERTIFIER-002"]
        row["expires_at"] = "2026-09-30T11:49:59Z"
        seal(row)

    semantic("N19_LOCAL_CERTIFIER_REVOKED", "authority-negative-control", revoke_certifier_locally)
    semantic("N20_LOCAL_CERTIFIER_STALE", "authority-negative-control", expire_certifier_locally)

    # D22/security mutations: all three layers and the cross-cutting security
    # slice are non-compensating requirements.
    def full_recert(state):
        application = state["application"]
        change = state["change"]
        change_at = "2026-09-30T11:05:00Z"
        entries = []
        times = (
            ("2026-09-30T11:20:00Z", "2026-09-30T11:23:00Z"),
            ("2026-09-30T11:21:00Z", "2026-09-30T11:24:00Z"),
            ("2026-09-30T11:22:00Z", "2026-09-30T11:25:00Z"),
        )
        order = {"training": 0, "regression": 1, "holdout": 2}
        for trial, (completed_at, issued_at) in zip(
            sorted(state["trial_registry"].values(), key=lambda row: order[row["layer"]]),
            times,
        ):
            trial["completed_at"] = completed_at
            seal(trial)
            output = state["evidence_registry"][trial["output_ref"]]
            output["issued_at"] = issued_at
            seal(output)
            entries.append(
                {
                    "trial_ref": trial["trial_id"],
                    "evidence_ref": output["evidence_id"],
                    "layer": trial["layer"],
                    "security_slices": ["certification-redteam"],
                    "affected_scopes": ["MODEL"],
                }
            )
        manifest = {
            "manifest_id": "RETEST-MANIFEST-INDEPENDENT-V25",
            "change_id": change["change_id"],
            "pre_change_release": "openclaw@prechange-2026.9.5",
            "post_change_release": application["release"],
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
            post_change_release=application["release"],
            retest_trial_refs=[row["trial_ref"] for row in entries],
            retest_evidence_refs=[row["evidence_ref"] for row in entries],
            retest_review_ref=review_ref,
            retest_manifest=manifest,
        )
        seal(change)
        row = state["evidence_registry"][change["evidence_ref"]]
        row["issued_at"] = change_at
        row["content_digest"] = runner.sha(runner.change_payload(application, change))
        seal(row)

    def reseal_change(state):
        change = state["change"]
        manifest = change["retest_manifest"]
        manifest["manifest_digest"] = runner.sha(
            {key: value for key, value in manifest.items() if key != "manifest_digest"}
        )
        seal(change)
        row = state["evidence_registry"][change["evidence_ref"]]
        row["content_digest"] = runner.sha(runner.change_payload(state["application"], change))
        seal(row)

    def recert_mutation(state, mutate):
        full_recert(state)
        mutate(state)
        reseal_change(state)

    semantic("N21_SECURITY_SLICE_MISSING_TRAINING", "d22-security", lambda s: recert_mutation(s, lambda x: x["change"]["retest_manifest"]["entries"][0].update(security_slices=[])))
    semantic("N22_SECURITY_SLICE_MISSING_REGRESSION", "d22-security", lambda s: recert_mutation(s, lambda x: x["change"]["retest_manifest"]["entries"][1].update(security_slices=[])))
    semantic("N23_SECURITY_SLICE_MISSING_HOLDOUT", "d22-security", lambda s: recert_mutation(s, lambda x: x["change"]["retest_manifest"]["entries"][2].update(security_slices=[])))
    semantic("N24_LAYER_LABEL_TRIAL_MISMATCH", "d22-layer", lambda s: recert_mutation(s, lambda x: x["change"]["retest_manifest"]["entries"][1].update(layer="training")))
    semantic("N25_REAL_WORLD_SUBSTITUTES_HOLDOUT", "d22-layer", lambda s: recert_mutation(s, lambda x: x["change"]["retest_manifest"]["entries"][2].update(layer="representative_real_world")))
    semantic("N26_POST_CHANGE_OUTPUT_EQUALS_CHANGE", "d22-causal", lambda s: recert_mutation(s, lambda x: x["evidence_registry"][x["change"]["retest_evidence_refs"][0]].update(issued_at=x["change"]["issued_at"])))

    # Result/source binding, full digest and parser controls.
    def rehash(candidate):
        candidate["decision_digest"] = runner.sha(runner.result_payload(candidate))

    result_attack("N27_BLANK_INPUT_SHA", "result-source", lambda x: (x.update(input_sha256=""), rehash(x)))
    result_attack("N28_BLANK_AUTHORITY_SHA", "result-source", lambda x: (x.update(authority_sha256=""), rehash(x)))
    result_attack("N29_SWAP_INPUT_AUTHORITY_SHA", "result-source", lambda x: (x.update(input_sha256=x["authority_sha256"], authority_sha256=x["input_sha256"]), rehash(x)))
    result_attack("N30_CROSS_RUN_INPUT_TRANSPLANT", "result-source", lambda x: (x.update(input_sha256="sha256:" + "1" * 64), rehash(x)))

    def mutate_trial_and_rehash(candidate):
        candidate["trials"][0]["decision"] = "PASS" if candidate["trials"][0]["decision"] != "PASS" else "FAIL"
        candidate["distribution"] = dict(sorted(Counter(row["decision"] for row in candidate["trials"]).items()))
        rehash(candidate)

    result_attack("N31_TRIAL_SEMANTIC_REWRITE_FULL_REHASH", "result-digest", mutate_trial_and_rehash)
    result_attack("N32_VERIFIER_CALLED_WITHOUT_ROOTS", "result-bypass", mutate_trial_and_rehash, omit_roots=True)

    top_duplicate = result_text.rstrip()[:-1] + ',"input_sha256":"sha256:' + "0" * 64 + '"}'
    nested_duplicate = result_text.replace(
        '"scenario_id":', '"scenario_id":"DUPLICATE-SCENARIO","scenario_id":', 1
    )
    parse_attack("N33_TOP_LEVEL_DUPLICATE_KEY", "json-canonicalization", top_duplicate, lambda value: runner.verify_result(value, authority, source))
    parse_attack("N34_NESTED_DUPLICATE_KEY", "json-canonicalization", nested_duplicate, lambda value: runner.verify_result(value, authority, source))

    def invalid_utf8_equivalent_alias(state):
        row = state["principal_registry"]["CERTIFIER-002"]
        row["aliases"].append("CERTIFIER-002\u00a0")
        seal(row)
        state["certificate_registry"][state["certificate_ref"]]["signer"] = "CERTIFIER-002\u00a0"
        seal(state["certificate_registry"][state["certificate_ref"]])

    semantic("N35_UNNORMALIZED_ALIAS_AS_SIGNER", "canonicalization", invalid_utf8_equivalent_alias)

    def stale_authority_local_extension(state):
        # A frozen authority projection must reject a locally extended expiry.
        row = next(v for v in state["authority_registry"].values() if v["action"] == "issue_synthetic_assessment")
        row["expires_at"] = "2027-12-31T00:00:00Z"
        seal(row)

    semantic("N36_STALE_AUTHORITY_LOCAL_EXTENSION", "authority-shadow", stale_authority_local_extension)

    # Three independent positive controls.  They repair causal ordering first;
    # positives are not counted as attacks and prove the oracle is not all-deny.
    def causalize(state):
        schedule = {
            "manifest": "2026-09-30T11:15:00Z",
            "artifact": "2026-09-30T11:15:00Z",
            "failure_archive": "2026-09-30T11:15:00Z",
            "cost_ledger": "2026-09-30T11:15:00Z",
            "d21_technical": "2026-09-30T11:16:00Z",
            "d21_delivery": "2026-09-30T11:17:00Z",
            "d21_business_environment": "2026-09-30T11:18:00Z",
            "change_review": "2026-09-30T11:20:00Z",
            "public_claim": "2026-09-30T11:50:00Z",
            "lifecycle_event": "2026-09-30T11:55:00Z",
        }
        for row in state["evidence_registry"].values():
            if row["kind"] in schedule:
                row["issued_at"] = schedule[row["kind"]]
                seal(row)

    def positive(test_id, family, mutate):
        state = copy.deepcopy(active["state"])
        decision, lifecycle, reasons, message = "ERROR", "REVOKED", [], ""
        try:
            causalize(state)
            mutate(state)
            checked = runner.validate_state(state, "v25-positive." + test_id)
            decision, lifecycle, reasons, *_ = runner.evaluate(source, checked, active["layer"], authority)
        except (ValueError, TypeError, KeyError) as exc:
            message = str(exc)
        passed = decision == "PASS"
        positives.append(
            {
                "test_id": test_id,
                "family": family,
                "actual_decision": decision,
                "actual_lifecycle": lifecycle,
                "actual_reasons": reasons,
                "passed": passed,
                "message": message,
            }
        )

    positive("P01_LEGAL_ACTIVE_CAUSAL_CHAIN", "legal-active", lambda state: None)

    def legal_renewal(state):
        cert = state["certificate_registry"][state["certificate_ref"]]
        cert["expires_at"] = "2026-10-29T12:00:00Z"
        seal(cert)

    positive("P02_LEGAL_ACTIVE_RENEWAL_WINDOW", "legal-renewal", legal_renewal)
    positive("P03_LEGAL_THREE_LAYER_RECERT", "legal-recertification", full_recert)

    output = {
        "schema": "c24.v2.5.independent-final.v1",
        "oracle": "causal+frozen-authority+d22+source-replay; no fixture expected field",
        "baseline_active_scenario": active_id,
        "attack_count": len(attacks),
        "secure_count": sum(row["secure_contract_passed"] for row in attacks),
        "escape_count": sum(row["escape"] for row in attacks),
        "positive_count": len(positives),
        "positive_pass_count": sum(row["passed"] for row in positives),
        "family_distribution": dict(sorted(Counter(row["family"] for row in attacks).items())),
        "attacks": attacks,
        "positive_controls": positives,
    }
    output["result_digest"] = "sha256:" + hashlib.sha256(
        json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    Path(args.output).write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({key: output[key] for key in ("attack_count", "secure_count", "escape_count", "positive_count", "positive_pass_count", "result_digest")}, ensure_ascii=False, sort_keys=True))
    return 0 if output["escape_count"] == 0 and output["positive_pass_count"] == len(positives) else 1


if __name__ == "__main__":
    raise SystemExit(main())

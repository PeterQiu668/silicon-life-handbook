#!/usr/bin/env python3
"""Independent, non-author near-neighbor review for C24 v2.2.

The oracle in this file is reviewer-defined. It never reads author-side
``expected`` or mutation labels. Semantic evaluation is separated from the
frozen-root black-box control so that a root mismatch cannot hide a fail-open.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("c24_v22_independent_final_runner", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def file_sha(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
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
    runner = load_module(runner_path)
    raw_source = json.loads(input_path.read_text(encoding="utf-8"))
    raw_authority = json.loads(authority_path.read_text(encoding="utf-8"))
    saved_result = json.loads(result_path.read_text(encoding="utf-8"))
    authority = runner.validate_authority(copy.deepcopy(raw_authority))
    source = runner.validate(copy.deepcopy(raw_source), authority)

    result_by_id = {row["scenario_id"]: row for row in saved_result["trials"]}
    pass_rows = [row for row in saved_result["trials"] if row["decision"] == "PASS"]
    if not pass_rows:
        raise RuntimeError("no observed PASS control")
    active_row = next(row for row in pass_rows if row["lifecycle"] == "ACTIVE")
    expired_row = next(row for row in pass_rows if row["lifecycle"] == "EXPIRED")
    source_by_id = {row["scenario_id"]: row for row in source["scenarios"]}
    active_control = source_by_id[active_row["scenario_id"]]
    expired_control = source_by_id[expired_row["scenario_id"]]

    def seal(record: dict, field: str = "record_digest") -> None:
        record[field] = runner.sha({key: value for key, value in record.items() if key != field})

    def one_authority(state: dict, action: str) -> dict:
        rows = [row for row in state["authority_registry"].values() if row["action"] == action]
        if len(rows) != 1:
            raise RuntimeError(f"authority cardinality for {action}")
        return rows[0]

    def one_evidence(state: dict, kind: str) -> dict:
        rows = [row for row in state["evidence_registry"].values() if row["kind"] == kind]
        if len(rows) != 1:
            raise RuntimeError(f"evidence cardinality for {kind}")
        return rows[0]

    semantic_rows: list[dict] = []

    def semantic_case(
        attack_id: str,
        family: str,
        mutate,
        *,
        control: dict | None = None,
        required_decision: str | None = None,
        required_reason: str | None = None,
        require_not_pass: bool = False,
        require_lifecycle: str | None = None,
        require_real_success_zero: bool = False,
        require_external_success_zero: bool = False,
        is_separation_control: bool = False,
    ) -> None:
        scenario = copy.deepcopy(control or active_control)
        mutate(scenario["state"])
        frozen = authority["scenario_registry"].get(scenario["scenario_id"])
        frozen_rejects = not bool(
            frozen
            and frozen["status"] == "ACTIVE"
            and frozen["state_digest"] == runner.raw_sha(scenario["state"])
        )
        try:
            checked = runner.validate_state(scenario["state"], f"independent.{attack_id}.state")
            decision, lifecycle, reasons, *_ = runner.evaluate(
                source, checked, scenario["layer"], authority
            )
            real_success = runner.real_certificate_success_count(checked)
            _, external_success, _, _ = runner.effect_counts(checked)
        except (KeyError, TypeError, ValueError) as exc:
            decision, lifecycle, reasons = "SCHEMA_REJECT", "REVOKED", [str(exc)]
            real_success = external_success = 0
        checks = []
        if required_decision is not None:
            checks.append(decision == required_decision)
        if required_reason is not None:
            checks.append(required_reason in reasons)
        if require_not_pass:
            checks.append(decision != "PASS")
        if require_lifecycle is not None:
            checks.append(lifecycle == require_lifecycle)
        if require_real_success_zero:
            checks.append(real_success == 0)
        if require_external_success_zero:
            checks.append(external_success == 0)
        matched = all(checks) if checks else False
        semantic_rows.append(
            {
                "attack_id": attack_id,
                "family": family,
                "reviewer_oracle": {
                    "required_decision": required_decision,
                    "required_reason": required_reason,
                    "require_not_pass": require_not_pass,
                    "require_lifecycle": require_lifecycle,
                    "require_real_success_zero": require_real_success_zero,
                    "require_external_success_zero": require_external_success_zero,
                },
                "actual_decision": decision,
                "actual_lifecycle": lifecycle,
                "actual_reasons": reasons,
                "derived_real_certificate_successes": real_success,
                "derived_external_effect_successes": external_success,
                "semantic_matched": matched,
                "semantic_escape": not matched,
                "blackbox_frozen_binding_rejects": frozen_rejects,
                "separation_control": is_separation_control,
            }
        )

    def maturity_after_certificate(state: dict) -> None:
        state["maturity"]["issued_at"] = "2026-09-30T11:51:00Z"
        seal(state["maturity"])
        cert = next(iter(state["certificate_registry"].values()))
        cert["maturity_digest"] = state["maturity"]["record_digest"]
        seal(cert)

    def namespace_after_certificate(state: dict) -> None:
        state["namespace"]["issued_at"] = "2026-09-30T11:51:00Z"
        seal(state["namespace"])
        cert = next(iter(state["certificate_registry"].values()))
        cert["namespace_digest"] = state["namespace"]["record_digest"]
        seal(cert)

    def trial_after_certificate(state: dict) -> None:
        trial = next(iter(state["trial_registry"].values()))
        trial["completed_at"] = "2026-09-30T11:51:00Z"
        seal(trial)

    def public_claim_after_certificate(state: dict) -> None:
        cert = next(iter(state["certificate_registry"].values()))
        evidence = state["evidence_registry"][cert["public_claim_ref"]]
        evidence["issued_at"] = "2026-09-30T11:51:00Z"
        seal(evidence)

    def lifecycle_owner_becomes(state: dict, application_field: str) -> None:
        principal_id = state["application"][application_field]
        principal = state["principal_registry"][principal_id]
        principal["roles"] = sorted(set(principal["roles"] + ["lifecycle_owner"]))
        seal(principal)
        authority_row = one_authority(state, "change_certificate_lifecycle")
        authority_row["actor"] = principal_id
        seal(authority_row)

    def change_owner_is_author(state: dict) -> None:
        app = state["application"]
        principal = state["principal_registry"][app["author"]]
        principal["roles"] = sorted(set(principal["roles"] + ["change_owner"]))
        seal(principal)
        authority_row = one_authority(state, "approve_material_change")
        authority_row["actor"] = app["author"]
        seal(authority_row)
        state["change"]["owner"] = app["author"]
        seal(state["change"])
        evidence = state["evidence_registry"][state["change"]["evidence_ref"]]
        evidence["content_digest"] = runner.sha(runner.change_payload(app, state["change"]))
        seal(evidence)

    def evidence_expires_before_certificate(state: dict, kind: str) -> None:
        evidence = one_evidence(state, kind)
        evidence["expires_at"] = "2026-10-01T00:00:00Z"
        seal(evidence)

    def material_change_after_trials_before_certificate(state: dict) -> None:
        app = state["application"]
        change = state["change"]
        change.update(
            material=True,
            kind="MODEL",
            impact_review="PASS",
            retest="PASS",
            issued_at="2026-09-30T11:45:00Z",
        )
        seal(change)
        evidence = state["evidence_registry"][change["evidence_ref"]]
        evidence["issued_at"] = "2026-09-30T11:44:00Z"
        evidence["content_digest"] = runner.sha(runner.change_payload(app, change))
        seal(evidence)

    def lifecycle_expired_before_expiry(state: dict) -> None:
        life = state["lifecycle"]
        life["occurred_at"] = "2026-09-30T11:51:00Z"
        seal(life)
        evidence = state["evidence_registry"][life["evidence_ref"]]
        evidence["content_digest"] = runner.sha(runner.lifecycle_payload(life))
        seal(evidence)

    def set_external_effect(state: dict, status: str, *, top_external: bool, extended: bool) -> None:
        app = state["application"]
        observation = {
            "effect_id": "EFFECT-INDEPENDENT",
            "status": "APPLIED",
            "external": True,
            "environment": "external",
        }
        effect = {
            "effect_id": "EFFECT-INDEPENDENT",
            "application_id": app["application_id"],
            "external": top_external,
            "status": status,
            "environment": "external",
        }
        if extended:
            effect.update(
                receipt=observation,
                receipt_digest=runner.sha(observation),
                readback=copy.deepcopy(observation),
                readback_digest=runner.sha(observation),
            )
        seal(effect)
        state["effect_ledger"] = [effect]

    def invalid_real_certificate(state: dict) -> None:
        cert = next(iter(state["certificate_registry"].values()))
        cert["real_certificate"] = True
        cert["signer"] = state["application"]["author"]
        seal(cert)

    def hard_failure_plus_pending(state: dict) -> None:
        cert = next(iter(state["certificate_registry"].values()))
        cert["signer"] = state["application"]["author"]
        seal(cert)
        set_external_effect(state, "PENDING", top_external=True, extended=False)

    def clean_suspended_pair(state: dict) -> None:
        cert = next(iter(state["certificate_registry"].values()))
        cert["lifecycle"] = "SUSPENDED"
        cert["public_claim"] = "synthetic assessment suspended"
        claim = state["evidence_registry"][cert["public_claim_ref"]]
        claim["content_digest"] = runner.sha(cert["public_claim"])
        seal(claim)
        seal(cert)
        life = state["lifecycle"]
        life.update(current="SUSPENDED", kind="SUSPEND")
        seal(life)
        evidence = state["evidence_registry"][life["evidence_ref"]]
        evidence["content_digest"] = runner.sha(runner.lifecycle_payload(life))
        seal(evidence)

    def live_certificate_past_expiry(state: dict) -> None:
        cert = next(iter(state["certificate_registry"].values()))
        cert["expires_at"] = "2026-09-30T11:59:00Z"
        seal(cert)

    semantic_case("maturity-created-after-certificate", "issuance-causality", maturity_after_certificate, required_decision="FAIL", required_reason="MATURITY_RECORD_INVALID_AT_CERTIFICATE_TIME")
    semantic_case("namespace-created-after-certificate", "issuance-causality", namespace_after_certificate, required_decision="FAIL", required_reason="NAMESPACE_BINDING_INVALID_AT_CERTIFICATE_TIME")
    semantic_case("trial-completes-after-certificate", "issuance-causality", trial_after_certificate, required_decision="FAIL", required_reason="TRIAL_NOT_COMPLETE_OR_VALID_AT_CERTIFICATE_TIME")
    semantic_case("public-claim-evidence-created-after-certificate", "issuance-causality", public_claim_after_certificate, required_decision="FAIL", required_reason="PUBLIC_CLAIM_INVALID")
    semantic_case("lifecycle-owner-is-application-author", "role-separation", lambda state: lifecycle_owner_becomes(state, "author"), require_not_pass=True)
    semantic_case("lifecycle-owner-is-application-controller", "role-separation", lambda state: lifecycle_owner_becomes(state, "controller"), require_not_pass=True)
    semantic_case("change-owner-self-approves-as-author", "role-separation", change_owner_is_author, require_not_pass=True)
    semantic_case("lifecycle-evidence-expires-before-certificate", "expiry-window", lambda state: evidence_expires_before_certificate(state, "lifecycle_event"), require_not_pass=True)
    semantic_case("change-evidence-expires-before-certificate", "expiry-window", lambda state: evidence_expires_before_certificate(state, "change_review"), require_not_pass=True)
    semantic_case("material-change-after-trials-before-certificate", "change-trigger", material_change_after_trials_before_certificate, require_not_pass=True)
    semantic_case("expire-event-precedes-certificate-expiry", "lifecycle-causality", lifecycle_expired_before_expiry, control=expired_control, require_not_pass=True)
    semantic_case("external-effect-pending", "external-effect", lambda state: set_external_effect(state, "PENDING", top_external=True, extended=False), required_decision="REVIEW_REQUIRED", required_reason="EXTERNAL_EFFECT_UNRESOLVED", require_lifecycle="SUSPENDED")
    semantic_case("external-effect-unknown-with-applied-looking-observations", "external-effect", lambda state: set_external_effect(state, "UNKNOWN", top_external=True, extended=True), required_decision="REVIEW_REQUIRED", required_reason="EXTERNAL_EFFECT_UNRESOLVED", require_lifecycle="SUSPENDED", require_external_success_zero=True)
    semantic_case("external-effect-hidden-by-top-level-false", "external-effect", lambda state: set_external_effect(state, "APPLIED", top_external=False, extended=True), require_not_pass=True, require_external_success_zero=True)
    semantic_case("self-attested-external-success-counter", "success-counter", lambda state: set_external_effect(state, "APPLIED", top_external=True, extended=True), required_decision="FAIL", required_reason="OFFLINE_CONFIRMED_EXTERNAL_SUCCESS_REJECTED", require_external_success_zero=True)
    semantic_case("invalid-real-certificate-counted-success", "success-counter", invalid_real_certificate, required_decision="FAIL", required_reason="CERTIFICATE_SIGNER_INVALID_AT_CERTIFICATE_TIME", require_real_success_zero=True)
    semantic_case("hard-failure-plus-pending-is-noncompensating", "gate-precedence", hard_failure_plus_pending, required_decision="FAIL", required_reason="EXTERNAL_EFFECT_UNRESOLVED", require_lifecycle="REVOKED")
    semantic_case("clean-suspended-pair-preserves-historical-pass", "lifecycle-gate-separation", clean_suspended_pair, required_decision="PASS", require_lifecycle="SUSPENDED", is_separation_control=True)
    semantic_case("active-certificate-past-expiry", "lifecycle-gate-separation", live_certificate_past_expiry, required_decision="FAIL", required_reason="CERTIFICATE_EXPIRED_WITH_LIVE_LIFECYCLE", require_lifecycle="REVOKED")

    def decision_digest(payload: dict) -> str:
        return runner.sha(
            [
                (
                    row["trial_id"],
                    row["decision"],
                    row["lifecycle"],
                    row["reasons"],
                    row["state_digest"],
                )
                for row in payload["trials"]
            ]
        )

    baseline_decision_digest = decision_digest(saved_result)
    if baseline_decision_digest != saved_result["decision_digest"]:
        raise RuntimeError("saved decision digest does not recompute")
    output_rows: list[dict] = []

    def output_integrity_case(attack_id: str, mutate) -> None:
        candidate = copy.deepcopy(saved_result)
        before_full = runner.sha({key: value for key, value in saved_result.items() if key != "decision_digest"})
        mutate(candidate)
        after_full = runner.sha({key: value for key, value in candidate.items() if key != "decision_digest"})
        recomputed = decision_digest(candidate)
        changed = before_full != after_full
        digest_changed = recomputed != baseline_decision_digest
        output_rows.append(
            {
                "attack_id": attack_id,
                "family": "decision-digest-completeness",
                "reviewer_oracle": "any changed decision/result field must alter or invalidate the decision digest",
                "payload_changed": changed,
                "baseline_decision_digest": baseline_decision_digest,
                "recomputed_after_attack": recomputed,
                "digest_changed": digest_changed,
                "semantic_matched": changed and digest_changed,
                "semantic_escape": changed and not digest_changed,
            }
        )

    output_integrity_case("aggregate-successful-external-effects-tamper", lambda payload: payload.update(successful_external_effects=payload["successful_external_effects"] + 7))
    output_integrity_case("aggregate-successful-real-certificates-tamper", lambda payload: payload.update(successful_real_certificates=payload["successful_real_certificates"] + 7))
    output_integrity_case("aggregate-distribution-tamper", lambda payload: payload["distribution"].update(PASS=payload["distribution"].get("PASS", 0) + 1))
    output_integrity_case("trial-certificate-id-tamper", lambda payload: payload["trials"][0].update(certificate_id="CERT-TAMPERED"))
    output_integrity_case("trial-success-counter-tamper", lambda payload: payload["trials"][0].update(successful_external_effects=99))
    output_integrity_case("trial-layer-tamper", lambda payload: payload["trials"][0].update(layer="representative_real_world"))

    attack_rows = semantic_rows + output_rows
    payload = {
        "schema": "c24.cert.v2.2-independent-final-negative.v1",
        "review_role": "non_author",
        "oracle_source": "reviewer_defined_without_author_expected",
        "scope": "offline_synthetic_semantic_and_output_integrity",
        "input_sha256": file_sha(input_path),
        "authority_sha256": file_sha(authority_path),
        "runner_sha256": file_sha(runner_path),
        "result_sha256": file_sha(result_path),
        "observed_pass_control_ids": [row["scenario_id"] for row in pass_rows],
        "semantic_attack_count": len(semantic_rows),
        "output_integrity_attack_count": len(output_rows),
        "attack_count": len(attack_rows),
        "matched_count": sum(row["semantic_matched"] for row in attack_rows),
        "escape_count": sum(row["semantic_escape"] for row in attack_rows),
        "attacks": attack_rows,
        "limits": {
            "real_openclaw_or_hermes_executed": False,
            "real_certificate_issued": False,
            "real_external_effect_executed": False,
            "practice_gate": "REVIEW_REQUIRED",
            "editor_gate": "NOT_AUTHORIZED",
            "chief_gate": "NOT_AUTHORIZED",
            "release_candidate": "NOT_AUTHORIZED",
        },
    }
    payload["suite_digest"] = runner.sha(attack_rows)
    Path(args.output).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "attack_count",
                    "matched_count",
                    "escape_count",
                    "suite_digest",
                )
            },
            ensure_ascii=False,
        )
    )
    if payload["escape_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

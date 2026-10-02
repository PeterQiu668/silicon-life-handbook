#!/usr/bin/env python3
"""C24 v2.1 non-author semantic and pinned-root negative tests.

The black-box controller deliberately rejects every mutation of a frozen
scenario.  This suite therefore records two independent observations:

1. the black-box result with the pinned authority root; and
2. the nested semantic result after the mutated records have valid local
   digests, but before the frozen scenario digest is applied.

The second observation prevents FROZEN_SCENARIO_BINDING_INVALID from masking a
missing certification rule that would become relevant when a legitimate new
scenario is admitted to a future authority bundle.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path


def canonical(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def digest(value):
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


def reseal(record, field="record_digest"):
    record[field] = digest({key: value for key, value in record.items() if key != field})


def load_runner(path):
    spec = importlib.util.spec_from_file_location("c24_v21_runner", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def first(registry):
    return next(iter(registry.values()))


def certificate(state):
    return state["certificate_registry"][state["certificate_ref"]]


def authority_for(state, action):
    return next(row for row in state["authority_registry"].values() if row["action"] == action)


def semantic_run(module, source, authority, scenario, mutate):
    attacked = copy.deepcopy(scenario)
    mutate(attacked["state"])
    try:
        state = module.validate_state(attacked["state"], "independent.state")
        verdict, lifecycle, reasons, real_world, real_cert, external = module.evaluate(
            source, state, attacked["layer"], authority
        )
        return {
            "actual": verdict,
            "lifecycle": lifecycle,
            "reasons": reasons,
            "representative_real_world_attempts": real_world,
            "real_certificate_attempts": real_cert,
            "external_effect_attempts": external,
        }, attacked
    except (ValueError, TypeError, KeyError) as exc:
        return {
            "actual": "SCHEMA_REJECT",
            "lifecycle": "NOT_EVALUATED",
            "reasons": [f"{type(exc).__name__}: {exc}"],
            "representative_real_world_attempts": 0,
            "real_certificate_attempts": 0,
            "external_effect_attempts": 0,
        }, attacked


def blackbox_run(source, authority, runner, scenario=None, mutate_source=None, mutate_root=None):
    candidate = copy.deepcopy(source)
    candidate["scenarios"] = [copy.deepcopy(scenario or source["scenarios"][0])]
    root = copy.deepcopy(authority)
    if mutate_source:
        mutate_source(candidate)
    if mutate_root:
        mutate_root(root)
    with tempfile.TemporaryDirectory(prefix="c24-v21-independent-") as temp:
        base = Path(temp)
        inp = base / "input.json"
        auth = base / "authority.json"
        out = base / "result.json"
        inp.write_text(json.dumps(candidate, ensure_ascii=False, sort_keys=True) + "\n")
        auth.write_text(json.dumps(root, ensure_ascii=False, sort_keys=True) + "\n")
        process = subprocess.run(
            ["python3", str(runner), "--input", str(inp), "--authority", str(auth), "--output", str(out)],
            capture_output=True,
            text=True,
        )
        if process.returncode:
            tail = (process.stderr or process.stdout).strip().splitlines()
            return {"actual": "SCHEMA_REJECT", "reasons": tail[-1:]}
        result = json.loads(out.read_text())
        trial = result["trials"][0]
        return {
            "actual": trial["decision"],
            "reasons": trial["reasons"],
            "successful_real_certificates": result["successful_real_certificates"],
            "successful_external_effects": result["successful_external_effects"],
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--authority", required=True)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    authority_path = Path(args.authority)
    runner_path = Path(args.runner)
    source = json.loads(input_path.read_text())
    authority = json.loads(authority_path.read_text())
    module = load_runner(runner_path)
    module.validate_authority(copy.deepcopy(authority))
    module.validate(copy.deepcopy(source), authority)

    baseline = None
    for candidate in source["scenarios"]:
        state = module.validate_state(copy.deepcopy(candidate["state"]), "baseline.state")
        verdict = module.evaluate(source, state, candidate["layer"], authority)[0]
        if verdict == "PASS":
            baseline = candidate
            break
    if baseline is None:
        raise RuntimeError("no PASS baseline available for independent mutation")

    rows = []

    def add_semantic(attack_id, expected, mutate, required_reason=None):
        semantic, attacked = semantic_run(module, source, authority, baseline, mutate)
        blackbox = blackbox_run(source, authority, runner_path, scenario=attacked)
        matched = semantic["actual"] == expected
        if required_reason is not None:
            matched = matched and required_reason in semantic["reasons"]
        rows.append(
            {
                "attack_id": attack_id,
                "mode": "nested_semantic_with_blackbox_control",
                "expected": expected,
                "required_reason": required_reason or "NONE",
                "semantic": semantic,
                "blackbox": blackbox,
                "frozen_root_masked_escape": semantic["actual"] == "PASS"
                and blackbox["actual"] == "FAIL"
                and "FROZEN_SCENARIO_BINDING_INVALID" in blackbox["reasons"],
                "matched": matched,
            }
        )

    def add_blackbox(attack_id, expected, mutate_source=None, mutate_root=None):
        result = blackbox_run(
            source,
            authority,
            runner_path,
            mutate_source=mutate_source,
            mutate_root=mutate_root,
        )
        rows.append(
            {
                "attack_id": attack_id,
                "mode": "pinned_root_blackbox",
                "expected": expected,
                "required_reason": "NONE",
                "semantic": {"actual": "NOT_APPLICABLE", "reasons": []},
                "blackbox": result,
                "frozen_root_masked_escape": False,
                "matched": result["actual"] == expected,
            }
        )

    def review_time(value):
        def mutate(state):
            review = first(state["review_registry"])
            review["issued_at"] = value
            reseal(review)
        return mutate

    add_semantic("review_issued_after_certificate", "FAIL", review_time("2026-09-30T11:59:00Z"))
    add_semantic("review_issued_in_future", "FAIL", review_time("2026-10-02T00:00:00Z"))

    def issue_authority_time(field, value):
        def mutate(state):
            record = authority_for(state, "issue_synthetic_assessment")
            record[field] = value
            reseal(record)
        return mutate

    add_semantic("issuance_authority_issued_after_certificate", "FAIL", issue_authority_time("issued_at", "2026-09-30T11:59:00Z"))
    add_semantic("issuance_authority_not_before_after_certificate", "FAIL", issue_authority_time("not_before", "2026-09-30T11:59:00Z"))

    def lifecycle_authority_after_event(state):
        record = authority_for(state, "change_certificate_lifecycle")
        record["not_before"] = "2026-09-30T11:59:00Z"
        reseal(record)

    add_semantic("lifecycle_authority_not_before_after_event", "FAIL", lifecycle_authority_after_event)

    def issuer_as_review_role(role_field, role):
        def mutate(state):
            issue = authority_for(state, "issue_synthetic_assessment")
            principal = state["principal_registry"][issue["actor"]]
            principal["roles"] = sorted(set(principal["roles"] + [role]))
            reseal(principal)
            review = first(state["review_registry"])
            review[role_field] = issue["actor"]
            reseal(review)
        return mutate

    add_semantic("certificate_issuer_is_reviewer", "FAIL", issuer_as_review_role("reviewer", "reviewer"))
    add_semantic("certificate_issuer_is_domain_expert", "FAIL", issuer_as_review_role("domain_expert", "domain_expert"))

    def opened_appeal_with_actor(actor_selector):
        def mutate(state):
            review = first(state["review_registry"])
            issue = authority_for(state, "issue_synthetic_assessment")
            actor = actor_selector(state, review, issue)
            principal = state["principal_registry"][actor]
            principal["roles"] = sorted(set(principal["roles"] + ["appeal_reviewer"]))
            reseal(principal)
            appeal = state["appeal_registry"][state["application"]["appeal_id"]]
            appeal.update(opened=True, reviewer=actor, decision="PASS")
            appeal_authority = state["authority_registry"][appeal["authority_ref"]]
            appeal_authority["actor"] = actor
            reseal(appeal_authority)
            reseal(appeal)
        return mutate

    add_semantic(
        "appeal_reviewer_is_certificate_issuer",
        "FAIL",
        opened_appeal_with_actor(lambda state, review, issue: issue["actor"]),
    )
    add_semantic(
        "appeal_reviewer_is_domain_expert",
        "FAIL",
        opened_appeal_with_actor(lambda state, review, issue: review["domain_expert"]),
    )

    def lifecycle_owner_is_reviewer(state):
        review = first(state["review_registry"])
        lifecycle_authority = authority_for(state, "change_certificate_lifecycle")
        lifecycle_authority["actor"] = review["reviewer"]
        principal = state["principal_registry"][review["reviewer"]]
        principal["roles"] = sorted(set(principal["roles"] + ["lifecycle_owner"]))
        reseal(principal)
        reseal(lifecycle_authority)

    add_semantic("lifecycle_owner_is_reviewer", "FAIL", lifecycle_owner_is_reviewer)

    def certificate_expiry_outlives_application(state):
        cert = certificate(state)
        cert["expires_at"] = "2026-12-30T00:00:00Z"
        reseal(cert)

    add_semantic("certificate_expiry_outlives_application", "FAIL", certificate_expiry_outlives_application)

    def evidence_after_certificate(ref_selector):
        def mutate(state):
            ref = ref_selector(state)
            evidence = state["evidence_registry"][ref]
            evidence["issued_at"] = "2026-09-30T11:59:00Z"
            reseal(evidence)
        return mutate

    add_semantic("artifact_issued_after_certificate", "FAIL", evidence_after_certificate(lambda s: s["evidence_bundle"]["artifact_ref"]))
    add_semantic("application_signature_issued_after_certificate", "FAIL", evidence_after_certificate(lambda s: s["evidence_bundle"]["signature_ref"]))
    add_semantic("trial_output_issued_after_certificate", "FAIL", evidence_after_certificate(lambda s: first(s["trial_registry"])["output_ref"]))

    def material_change_at(value):
        def mutate(state):
            change = state["change"]
            change.update(
                material=True,
                kind="MODEL",
                impact_review="PASS",
                retest="PASS",
                issued_at=value,
            )
            reseal(change)
            evidence = state["evidence_registry"][change["evidence_ref"]]
            evidence["content_digest"] = module.sha(module.change_payload(state["application"], change))
            reseal(evidence)
        return mutate

    add_semantic("material_change_after_certificate", "FAIL", material_change_at("2026-09-30T11:59:00Z"))
    add_semantic("material_change_from_future", "FAIL", material_change_at("2026-10-02T00:00:00Z"))

    def future_opened_appeal(state):
        appeal = state["appeal_registry"][state["application"]["appeal_id"]]
        appeal.update(opened=True, decision="PASS", issued_at="2026-10-02T00:00:00Z")
        reseal(appeal)

    add_semantic("opened_appeal_issued_in_future", "FAIL", future_opened_appeal)

    def real_certificate(state):
        cert = certificate(state)
        cert["real_certificate"] = True
        reseal(cert)

    add_semantic("offline_real_certificate_attempt", "FAIL", real_certificate, "OFFLINE_REAL_CERTIFICATE_REJECTED")

    def external_effect(state, status):
        row = {
            "effect_id": "EFFECT-INDEPENDENT-001",
            "application_id": state["application"]["application_id"],
            "external": True,
            "status": status,
            "environment": "external",
            "record_digest": "",
        }
        reseal(row)
        state["effect_ledger"] = [row]

    add_semantic(
        "offline_external_effect_applied",
        "FAIL",
        lambda state: external_effect(state, "APPLIED"),
        "OFFLINE_EXTERNAL_EFFECT_REJECTED",
    )
    add_semantic("offline_external_effect_unknown", "REVIEW_REQUIRED", lambda state: external_effect(state, "UNKNOWN"))

    def trial_output_review_required(state):
        trial = first(state["trial_registry"])
        evidence = state["evidence_registry"][trial["output_ref"]]
        evidence["status"] = "REVIEW_REQUIRED"
        reseal(evidence)

    add_semantic(
        "trial_output_review_required",
        "REVIEW_REQUIRED",
        trial_output_review_required,
        "TRIAL_OUTPUT_EVIDENCE_UNKNOWN",
    )

    def wrong_artifact_digest(state):
        evidence = state["evidence_registry"][state["evidence_bundle"]["artifact_ref"]]
        evidence["content_digest"] = "sha256:" + "a" * 64
        reseal(evidence)

    add_semantic("artifact_well_formed_wrong_digest", "FAIL", wrong_artifact_digest, "ARTIFACT_CONTENT_INVALID")

    def expired_active_certificate(state):
        cert = certificate(state)
        cert["expires_at"] = "2026-09-29T00:00:00Z"
        reseal(cert)

    add_semantic("active_certificate_expired", "FAIL", expired_active_certificate, "CERTIFICATE_EXPIRED_WITH_LIVE_LIFECYCLE")

    def future_lifecycle(state):
        lifecycle = state["lifecycle"]
        lifecycle["occurred_at"] = "2026-10-02T00:00:00Z"
        reseal(lifecycle)

    add_semantic("future_lifecycle_event", "FAIL", future_lifecycle, "LIFECYCLE_BINDING_INVALID")

    def principal_alias_collision(state):
        issue = authority_for(state, "issue_synthetic_assessment")
        review = first(state["review_registry"])
        principal = state["principal_registry"][issue["actor"]]
        principal["aliases"] = [review["reviewer"]]
        reseal(principal)

    add_semantic("principal_alias_collision", "SCHEMA_REJECT", principal_alias_collision)

    def certificate_scope_mismatch(state):
        cert = certificate(state)
        cert["scope"] = "broader-production-scope"
        reseal(cert)

    add_semantic("certificate_scope_broadened", "FAIL", certificate_scope_mismatch, "CERTIFICATE_BINDING_INVALID")

    add_blackbox(
        "trusted_clock_tamper",
        "SCHEMA_REJECT",
        mutate_source=lambda candidate: candidate.update(now="2026-09-30T12:01:00Z"),
    )

    def reseal_root(root):
        first_record = next(iter(root["scenario_registry"].values()))
        first_record["state_digest"] = "sha256:" + "7" * 64
        root["root_digest"] = digest({key: value for key, value in root.items() if key != "root_digest"})

    add_blackbox("authority_root_tamper_and_local_reseal", "SCHEMA_REJECT", mutate_root=reseal_root)

    payload = {
        "schema": "c24.cert.independent-negative.v2.1",
        "scope": "offline_synthetic_nested_semantic_and_pinned_root",
        "baseline_scenario_id": baseline["scenario_id"],
        "authority_root_digest": authority["root_digest"],
        "attack_count": len(rows),
        "matched_count": sum(row["matched"] for row in rows),
        "escape_count": sum(not row["matched"] for row in rows),
        "frozen_root_masked_escape_count": sum(row["frozen_root_masked_escape"] for row in rows),
        "attacks": rows,
    }
    payload["suite_digest"] = digest(rows)
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {key: payload[key] for key in ("attack_count", "matched_count", "escape_count", "frozen_root_masked_escape_count", "suite_digest")},
            ensure_ascii=False,
        )
    )
    return 0 if payload["escape_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

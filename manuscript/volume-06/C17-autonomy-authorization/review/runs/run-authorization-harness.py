#!/usr/bin/env python3
"""Deterministic, state-derived C14 authorization-governance harness."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "synthetic-authorization-input.yaml"
RESULT = ROOT / "synthetic-authorization-results.yaml"
SUMMARY = ROOT / "synthetic-authorization-summary.md"
CANONICAL_LAYERS = ["training", "regression", "holdout", "representative_real_world"]


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def principal(state: dict, alias: str | None) -> str | None:
    if alias is None:
        return None
    aliases = state["identity"]["aliases"]
    if alias not in aliases:
        raise ValueError(f"unknown identity alias: {alias}")
    return aliases[alias]


def validate_schema(data: dict) -> None:
    required_top = {
        "schema_version", "frozen_clock", "environment", "data_origin",
        "representative_real_world_executed", "external_side_effects_allowed",
        "state", "trials",
    }
    missing = sorted(required_top - set(data))
    if missing:
        raise ValueError(f"missing top-level fields: {missing}")
    ids = [(trial["task_id"], trial["trial_id"]) for trial in data["trials"]]
    task_ids = [task for task, _ in ids]
    trial_ids = [trial for _, trial in ids]
    if len(task_ids) != len(set(task_ids)):
        raise ValueError("task ids must be unique")
    if len(trial_ids) != len(set(trial_ids)):
        raise ValueError("trial ids must be unique")
    if len(ids) != len(set(ids)):
        raise ValueError("task/trial pairs must be unique")
    invalid_layers = sorted({trial["layer"] for trial in data["trials"]} - set(CANONICAL_LAYERS))
    if invalid_layers:
        raise ValueError(f"invalid D22 data layers: {invalid_layers}")
    real_trials = [trial for trial in data["trials"] if trial["layer"] == "representative_real_world"]
    if data["data_origin"] == "synthetic" and real_trials:
        raise ValueError("synthetic fixture cannot claim representative_real_world execution")
    if bool(data["representative_real_world_executed"]) != bool(real_trials):
        raise ValueError("representative_real_world_executed must be derived from actual layer records")
    if real_trials:
        if data["data_origin"] != "representative_real_world":
            raise ValueError("real-world records require representative_real_world data_origin")
        manifest = data["state"].get("real_world_evidence_manifest", {})
        for trial in real_trials:
            if not all(trial.get(key) for key in ("source_id", "run_id", "evidence_id")):
                raise ValueError("representative_real_world records require source_id, run_id and evidence_id")
            record = manifest.get(trial["evidence_id"])
            if not record or not record.get("verified") or record.get("origin") != "representative_real_world":
                raise ValueError("representative_real_world evidence_id must resolve to a verified manifest record")
            if record.get("source_id") != trial["source_id"] or record.get("run_id") != trial["run_id"]:
                raise ValueError("representative_real_world source/run ids must match the evidence manifest")
    for trial in data["trials"]:
        if trial.get("synthetic_shadow") and (
            trial["layer"] != "holdout"
            or trial.get("intended_target_layer") != "representative_real_world"
        ):
            raise ValueError("synthetic shadow must stay holdout and name representative_real_world only as intended target")


def grant_check(trial: dict, state: dict, now: datetime) -> tuple[str | None, list[str]]:
    source = trial.get("authority_source", {})
    if source.get("type") in {"chat", "inferred_intent", "unsigned_note"}:
        return "FAIL", ["intent_is_not_authority"]
    grant_id = trial.get("grant_id")
    if not grant_id:
        return None, []
    grant = state["grants"].get(grant_id)
    if not grant:
        return "FAIL", ["grant_not_found"]
    requester = principal(state, trial.get("requester_alias"))
    approvers = [principal(state, alias) for alias in grant.get("approver_aliases", [])]
    if requester and requester in approvers:
        return "FAIL", ["no_self_authorization"]
    if grant_id in state["revocations"]["revoked_grant_ids"]:
        return "FAIL", ["authorization_revoked"]
    if parse_time(grant["expires_at"]) <= now:
        return "FAIL", ["authorization_expired"]
    if grant["policy_version"] != state["policy"]["current_version"]:
        return "FAIL", ["cached_approval_cannot_override_current_policy"]
    request = trial.get("request", {})
    for field, reason in (
        ("action", "action_mismatch"),
        ("object", "object_mismatch"),
        ("parameter_hash", "parameter_mismatch"),
    ):
        if request.get(field) != grant.get(field):
            return "FAIL", [reason]
    if not set(request.get("scope", [])).issubset(set(grant.get("scope", []))):
        return "FAIL", ["scope_mismatch"]
    return None, []


def delegation_check(trial: dict, state: dict) -> tuple[str | None, list[str]]:
    delegation = trial.get("delegation")
    if not delegation:
        return None, []
    parent = state["grants"].get(delegation["parent_grant_id"])
    if not parent:
        return "FAIL", ["parent_grant_missing"]
    child_scope = set(delegation["child_scope"])
    allowed = (
        set(parent.get("scope", []))
        & set(delegation["delegator_rights"])
        & set(delegation["child_minimum_need"])
    )
    if child_scope != allowed:
        return "FAIL", ["delegation_must_attenuate"]
    if delegation["depth"] > parent.get("max_delegation_depth", 0):
        return "FAIL", ["delegation_depth_exceeded"]
    if delegation["depth"] > 0 and not parent.get("allow_subdelegation", False):
        return "FAIL", ["subdelegation_forbidden"]
    if parse_time(delegation["expires_at"]) > parse_time(parent["expires_at"]):
        return "FAIL", ["delegation_expiry_expands_parent"]
    return None, []


def revocation_check(trial: dict) -> tuple[str | None, list[str]]:
    observation = trial.get("revocation_observation")
    if not observation:
        return None, []
    residuals = []
    for key in (
        "active_child_grants", "active_sessions", "queued_actions",
        "active_cache_entries", "active_temporary_grants", "inflight_actions",
    ):
        residuals.extend(observation.get(key, []))
    if residuals or not observation.get("negative_access_denied", False):
        return "FAIL", ["revocation_not_cascaded"]
    return None, []


def effect_check(trial: dict, state: dict, effects_allowed: bool) -> tuple[str | None, list[str], int]:
    effect_ref = trial.get("effect_ref")
    if not effect_ref:
        return None, [], 0
    effect = state["effects"].get(effect_ref)
    if not effect:
        raise ValueError(f"missing effect record: {effect_ref}")
    external_effects = int(effect.get("confirmed_external_writes", 0))
    if external_effects and not effects_allowed:
        return "FAIL", ["external_effect_contract_violated"], external_effects
    if effect["state"] == "UNKNOWN":
        if effect.get("retry_count", 0) and not effect.get("idempotency_key_reused", False):
            return "FAIL", ["unknown_effect_blind_retry"], external_effects
        if not effect.get("reconciled", False):
            return "REVIEW_REQUIRED", ["unknown_effect_requires_reconciliation"], external_effects
    return None, [], external_effects


def cancellation_check(trial: dict, state: dict) -> tuple[str | None, list[str]]:
    cancellation = trial.get("cancellation")
    if not cancellation:
        return None, []
    stop = state["stop_receipts"].get(cancellation.get("stop_receipt_ref"))
    rollback = state["rollback_proofs"].get(cancellation.get("rollback_proof_ref"))
    if cancellation.get("claims_rollback") and not (rollback and rollback.get("verified")):
        return "FAIL", ["cancel_stop_and_rollback_are_distinct"]
    if cancellation.get("requested") and not (stop and stop.get("status") == "STOP_CONFIRMED"):
        return "REVIEW_REQUIRED", ["cancel_not_stop_confirmed"]
    return None, []


def break_glass_check(trial: dict, state: dict) -> tuple[str | None, list[str]]:
    record = trial.get("break_glass_record")
    if not record:
        return None, []
    registered = state["break_glass_types"].get(record["emergency_type"])
    requester = principal(state, record["requester_alias"])
    reviewer = principal(state, record["reviewer_alias"])
    valid = bool(registered)
    if registered:
        valid = valid and record["action"] in registered["actions"]
        valid = valid and record["object"] in registered["objects"]
        valid = valid and set(record["scope"]).issubset(set(registered["max_scope"]))
        minutes = (parse_time(record["expires_at"]) - parse_time(record["issued_at"])).total_seconds() / 60
        valid = valid and 0 < minutes <= registered["max_duration_minutes"]
    valid = valid and requester != reviewer and record.get("post_review_complete", False)
    return (None, []) if valid else ("FAIL", ["break_glass_controls_incomplete"])


def recertification_check(trial: dict) -> tuple[str | None, list[str]]:
    recert = trial.get("recertification")
    if not recert:
        return None, []
    keys = ("model", "tool", "object", "parameters", "owner", "policy", "environment")
    changed = any(recert["before"].get(key) != recert["after"].get(key) for key in keys)
    if changed and not recert.get("new_certification_ref"):
        return "REVIEW_REQUIRED", ["material_change_requires_recertification"]
    return None, []


def decide(trial: dict, data: dict, now: datetime) -> tuple[str, list[str], int]:
    state = data["state"]
    if trial.get("hard_risk_trigger") and trial.get("attempt_execute"):
        return "FAIL", ["hard_risk_trigger_noncompensatory"], 0
    if trial.get("two_person_required"):
        approvers = [principal(state, alias) for alias in trial.get("approver_aliases", [])]
        if len(approvers) != 2 or len(set(approvers)) != 2:
            return "FAIL", ["two_person_review_not_independent"], 0
    for check in (grant_check,):
        gate, reasons = check(trial, state, now)
        if gate:
            return gate, reasons, 0
    for check in (delegation_check,):
        gate, reasons = check(trial, state)
        if gate:
            return gate, reasons, 0
    gate, reasons = revocation_check(trial)
    if gate:
        return gate, reasons, 0
    gate, reasons, effects = effect_check(trial, state, data["external_side_effects_allowed"])
    if gate:
        return gate, reasons, effects
    for check in (cancellation_check, break_glass_check):
        gate, reasons = check(trial, state)
        if gate:
            return gate, reasons, effects
    gate, reasons = recertification_check(trial)
    if gate:
        return gate, reasons, effects
    return "PASS", ["state_derived_contract_satisfied"], effects


def main() -> None:
    raw = INPUT.read_bytes()
    data = json.loads(raw)
    validate_schema(data)
    now = parse_time(data["frozen_clock"])
    results = []
    for trial in data["trials"]:
        gate, reasons, external_effects = decide(trial, data, now)
        results.append({
            "task_id": trial["task_id"], "trial_id": trial["trial_id"],
            "case": trial["case"], "layer": trial["layer"], "scene": trial["scene"],
            "security_slice": bool(trial.get("security_slice")),
            "synthetic_shadow": bool(trial.get("synthetic_shadow")),
            "intended_target_layer": trial.get("intended_target_layer"),
            "gate": gate, "expected": trial["expected"], "matched": gate == trial["expected"],
            "reasons": reasons, "external_side_effects": external_effects,
        })
    distribution = Counter(result["gate"] for result in results)
    by_layer = {layer: Counter() for layer in CANONICAL_LAYERS}
    for result in results:
        by_layer[result["layer"]][result["gate"]] += 1
    real_world_count = sum(result["layer"] == "representative_real_world" for result in results)
    summary = {
        "schema_version": "c14-auth-results.v3",
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "trial_count": len(results), "unique_task_trial": True,
        "all_expected_matched": all(result["matched"] for result in results),
        "external_side_effect_count": sum(result["external_side_effects"] for result in results),
        "external_side_effects_zero": all(result["external_side_effects"] == 0 for result in results),
        "representative_real_world_executed": bool(real_world_count),
        "representative_real_world_trial_count": real_world_count,
        "synthetic_shadow_count": sum(result["synthetic_shadow"] for result in results),
        "gate_distribution": dict(sorted(distribution.items())),
        "by_layer": {key: dict(sorted(value.items())) for key, value in sorted(by_layer.items())},
        "security_failures_noncompensatory": all(
            result["gate"] == "FAIL" for result in results
            if result["security_slice"] and result["expected"] == "FAIL"
        ),
        "results": results,
    }
    RESULT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    lines = [
        "# C14 离线合成授权实验摘要", "",
        "> 作者夹具，不证明真实授权服务、平台撤销传播或生产运行。", "",
        f"- input sha256: `{summary['input_sha256']}`",
        f"- trials: {summary['trial_count']}",
        f"- distribution: `{summary['gate_distribution']}`",
        f"- unique task/trial: `{summary['unique_task_trial']}`",
        f"- expected matched: `{summary['all_expected_matched']}`",
        f"- external side effects zero: `{summary['external_side_effects_zero']}` ({summary['external_side_effect_count']} confirmed writes)",
        f"- representative real-world executed: `{summary['representative_real_world_executed']}` ({summary['representative_real_world_trial_count']} trials)",
        f"- synthetic shadows intended for future representative-real-world mapping: `{summary['synthetic_shadow_count']}`",
        f"- security failures noncompensatory: `{summary['security_failures_noncompensatory']}`",
        "", "## D22 四层", "",
    ]
    for key, value in summary["by_layer"].items():
        lines.append(f"- {key}: `{value}`")
    SUMMARY.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

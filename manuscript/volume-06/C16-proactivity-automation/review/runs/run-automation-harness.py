#!/usr/bin/env python3
"""Deterministic stateful offline C13 signal/state/delivery harness."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "synthetic-automation-input.yaml"
OUTPUT = HERE / "synthetic-automation-results.yaml"
SUMMARY = HERE / "synthetic-automation-summary.md"


def stable_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def validate_input(data: dict) -> None:
    triggers = data["trigger_paths"]
    scenarios = data["scenarios"]
    contract = data["contract"]
    if len(triggers) != len(set(triggers)):
        raise ValueError("trigger_paths must be unique")
    scenario_ids = [scenario["scenario_id"] for scenario in scenarios]
    if len(scenario_ids) != len(set(scenario_ids)):
        raise ValueError("scenario_id values must be unique")
    planned_trials = len(triggers) * len(scenarios)
    if planned_trials > contract["max_trials"]:
        raise ValueError(f"planned trials {planned_trials} exceed max_trials {contract['max_trials']}")
    if data["environment"]["external_side_effects"]:
        raise ValueError("offline fixture cannot enable external side effects")
    if contract["max_external_side_effects"] != 0:
        raise ValueError("offline fixture requires max_external_side_effects=0")


def derive_signal(scenario: dict, data: dict) -> dict:
    event_time = parse_time(scenario["event_time"])
    observed_at = parse_time(scenario["observed_at"])
    expires_at = event_time + timedelta(seconds=scenario["ttl_seconds"])
    return {
        "source_verified": scenario["source_identity"] in set(data["allowed_sources"]),
        "duplicate": scenario["business_idempotency_key"] in set(data["processed_business_keys"]),
        "fresh": observed_at <= expires_at,
        "event_time": scenario["event_time"],
        "observed_at": scenario["observed_at"],
        "expires_at": expires_at.isoformat(),
        "timezone_valid": scenario["schedule_timezone"] in set(data["allowed_timezones"]),
    }


def derive_authority(scenario: dict, data: dict) -> dict:
    if scenario["requested_effect"] != "external_action":
        return {"required": False, "valid": True, "reason": "not_required"}
    approval_ref = scenario.get("approval_ref")
    approval = data["approvals"].get(approval_ref) if approval_ref else None
    if not approval:
        return {"required": True, "valid": False, "reason": "missing"}
    observed_at = parse_time(scenario["observed_at"])
    valid = (
        approval["status"] == "active"
        and scenario["requested_effect"] in set(approval["scope"])
        and approval["policy_version"] == data["current_policy_version"]
        and observed_at <= parse_time(approval["expires_at"])
    )
    return {
        "required": True,
        "valid": valid,
        "reason": "valid" if valid else "revoked_expired_scope_or_version_mismatch",
        "approval_ref": approval_ref,
    }


def complete(technical: str, delivery: str, business: str) -> dict:
    return {
        "technical_execution": technical,
        "delivery_visibility": delivery,
        "business_environment_acceptance": business,
    }


def outcome(gate: str, route: str, reasons: list[str], layers: dict, states: list[str], derived: dict):
    return gate, route, reasons, layers, states, derived


def evaluate(scenario: dict, data: dict):
    states = ["DORMANT", "AWAKENED", "DECIDING"]
    signal = derive_signal(scenario, data)
    authority = derive_authority(scenario, data)
    external_effect_count = len(scenario["effect_ledger"])
    notification_count = scenario["notification_count"]
    fault_overlap = sorted(set(scenario["automation_fault_domains"]) & set(scenario["sentinel_fault_domains"]))
    derived = {
        "signal": signal,
        "authority": authority,
        "external_effect_count": external_effect_count,
        "notification_count": notification_count,
        "fault_domain_overlap": fault_overlap,
        "sentinel_independent": not fault_overlap,
    }

    if external_effect_count > data["contract"]["max_external_side_effects"]:
        return outcome("FAIL", "CIRCUIT_BREAK", ["external_effect_budget_exceeded"], complete("FAIL", "UNKNOWN", "UNKNOWN"), states + ["CIRCUIT_OPEN", "FAILED"], derived)
    if notification_count > data["contract"]["max_notifications_per_trial"]:
        return outcome("FAIL", "CIRCUIT_BREAK", ["notification_budget_exceeded"], complete("BLOCKED", "FAIL", "UNKNOWN"), states + ["CIRCUIT_OPEN", "FAILED"], derived)
    if scenario["recovery_action_enabled"] and scenario["recovery_probe_status"] != "PASS":
        return outcome("FAIL", "CIRCUIT_BREAK", ["recovery_probe_failed"], complete("BLOCKED", "NOT_STARTED", "UNKNOWN"), states + ["RECOVERING", "FAILED"], derived)
    # Existing uncertain effects, broken independent observation, and unconfirmed
    # stop requests survive de-duplication, pause, timezone, and authority routing.
    # Those early routes must never erase evidence that work may already have run.
    if scenario["side_effect_status"] == "raw_unknown":
        unsafe_retry = any(
            retry.get("idempotency_key") != scenario["effect_idempotency_key"]
            or not retry.get("readback_before_retry", False)
            for retry in scenario["retry_attempts"]
        )
        if unsafe_retry:
            return outcome("FAIL", "CIRCUIT_BREAK", ["unknown_effect_blind_retry"], complete("UNKNOWN", "NOT_STARTED", "UNKNOWN"), states + ["CIRCUIT_OPEN", "FAILED"], derived)
        if authority["required"] and not authority["valid"]:
            return outcome("FAIL", "CIRCUIT_BREAK", ["unknown_effect_with_invalid_authority"], complete("UNKNOWN", "NOT_STARTED", "UNKNOWN"), states + ["CIRCUIT_OPEN", "FAILED"], derived)
        return outcome("REVIEW_REQUIRED", "RECONCILE", ["unknown_effect_no_blind_replay"], complete("UNKNOWN", "NOT_STARTED", "UNKNOWN"), states + ["READY", "RUNNING", "REVIEW_REQUIRED"], derived)
    if fault_overlap:
        return outcome("FAIL", "CIRCUIT_BREAK", ["sentinel_shared_only_fault_domain"], complete("FAILED_UNOBSERVED", "FAILED", "UNKNOWN"), states + ["CIRCUIT_OPEN", "FAILED"], derived)
    if scenario["stop_requested"] and not scenario["stop_confirmed"]:
        return outcome("REVIEW_REQUIRED", "WAIT_STOP_CONFIRMATION", ["stop_not_confirmed"], complete("STOP_REQUESTED", "NOT_STARTED", "UNKNOWN"), states + ["PAUSING", "REVIEW_REQUIRED"], derived)
    if not signal["source_verified"]:
        return outcome("FAIL", "DISCARD", ["source_unverified"], complete("BLOCKED", "NOT_STARTED", "NOT_STARTED"), states + ["FAILED"], derived)
    if signal["duplicate"]:
        return outcome("PASS", "SILENT_RECORD", ["duplicate_replay_blocked"], complete("NOT_STARTED", "NOT_REQUIRED", "VERIFIED_NO_NEW_EFFECT"), states + ["QUIET", "COMPLETED"], derived)
    if not signal["fresh"]:
        return outcome("FAIL", "DISCARD", ["signal_expired"], complete("BLOCKED", "NOT_STARTED", "VERIFIED_NO_EFFECT"), states + ["FAILED"], derived)
    if scenario["paused"]:
        return outcome("PASS", "PAUSE", ["pause_enforced_across_trigger"], complete("NOT_STARTED", "NOT_REQUIRED", "VERIFIED_NO_EFFECT"), states + ["PAUSED"], derived)
    if not signal["timezone_valid"]:
        return outcome("PASS", "SILENT_RECORD", ["misfire_safely_skipped"], complete("SKIPPED_BY_POLICY", "NOT_REQUIRED", "VERIFIED_NO_EFFECT"), states + ["QUIET", "COMPLETED"], derived)
    if not scenario["state_readable"]:
        return outcome("REVIEW_REQUIRED", "ESCALATE", ["authoritative_state_unavailable"], complete("BLOCKED", "NOT_STARTED", "UNKNOWN"), states + ["REVIEW_REQUIRED"], derived)
    if authority["required"] and not authority["valid"]:
        if not data["approval_surface"]["available"]:
            return outcome("REVIEW_REQUIRED", "ESCALATE", ["authority_missing_and_no_approval_surface"], complete("BLOCKED", "NOT_STARTED", "VERIFIED_NO_EFFECT"), states + ["REVIEW_REQUIRED"], derived)
        return outcome("PASS", "REQUEST_APPROVAL", ["trigger_valid_but_authority_missing"], complete("WAITING_APPROVAL", "NOT_STARTED", "VERIFIED_NO_EFFECT"), states + ["WAITING_APPROVAL"], derived)
    if scenario["novelty"] == "unchanged":
        if not (scenario["quiet_reason"] and scenario["environment_readback_id"]):
            return outcome("REVIEW_REQUIRED", "ESCALATE", ["quiet_decision_evidence_missing"], complete("OBSERVATION_COMPLETE", "NOT_REQUIRED", "UNKNOWN"), states + ["REVIEW_REQUIRED"], derived)
        return outcome("PASS", "SILENT_RECORD", ["unchanged_with_audit_evidence"], complete("OBSERVATION_COMPLETE", "NOT_REQUIRED", "VERIFIED_UNCHANGED"), states + ["QUIET", "COMPLETED"], derived)

    states += ["READY", "RUNNING", "VERIFYING"]
    if not scenario["trigger_success"]:
        return outcome("FAIL", "CIRCUIT_BREAK", ["technical_execution_failed"], complete("FAIL", "NOT_STARTED", "NOT_ACHIEVED"), states + ["FAILED"], derived)
    if not scenario["artifact_evidence_id"]:
        return outcome("REVIEW_REQUIRED", "ESCALATE", ["artifact_evidence_missing"], complete("PASS", "NOT_STARTED", "UNKNOWN"), states + ["REVIEW_REQUIRED"], derived)
    if scenario["delivery_required"]:
        states.append("DELIVERING")
        if not scenario["delivery_receipt_id"]:
            return outcome("FAIL", "RECOVER_DELIVERY", ["delivery_not_visible_at_target"], complete("PASS", "FAIL", "NOT_ACHIEVED"), states + ["RECOVERING", "FAILED"], derived)
    if not scenario["environment_readback_id"]:
        return outcome("REVIEW_REQUIRED", "ESCALATE", ["environment_readback_missing"], complete("PASS", "PASS" if scenario["delivery_required"] else "NOT_REQUIRED", "UNKNOWN"), states + ["REVIEW_REQUIRED"], derived)
    return outcome("PASS", "PROPOSE", ["three_layer_completion_verified"], complete("PASS", "PASS" if scenario["delivery_required"] else "NOT_REQUIRED", "PASS"), states + ["COMPLETED"], derived)


def main() -> None:
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    validate_input(data)
    rows = []
    for scenario_index, scenario in enumerate(data["scenarios"], start=1):
        for trigger_index, trigger in enumerate(data["trigger_paths"], start=1):
            gate, route, reasons, layers, states, derived = evaluate(scenario, data)
            rows.append({
                "task_id": f"T-C13-{scenario_index:02d}-{trigger_index:02d}",
                "trial_id": f"TR-C13-{scenario_index:02d}-{trigger_index:02d}",
                "case": scenario["case"], "scenario_id": scenario["scenario_id"],
                "category": scenario["category"], "trigger_path": trigger,
                "signal_id": f"{scenario['event_id']}:{trigger}",
                "requested_effect": scenario["requested_effect"], "route": route,
                "state_trajectory": states, "completion_layers": layers,
                "side_effect_status": scenario["side_effect_status"],
                "external_side_effect_count": derived["external_effect_count"],
                "notification_count": derived["notification_count"],
                "sentinel_independent": derived["sentinel_independent"],
                "derived_controls": derived, "expected_gate": scenario["expected_gate"],
                "gate_decision": gate, "gate_reasons": reasons,
                "matches_expected": gate == scenario["expected_gate"],
            })

    gates = Counter(row["gate_decision"] for row in rows)
    categories: dict[str, Counter] = defaultdict(Counter)
    triggers: dict[str, Counter] = defaultdict(Counter)
    cases: dict[str, Counter] = defaultdict(Counter)
    reasons = Counter()
    for row in rows:
        categories[row["category"]][row["gate_decision"]] += 1
        triggers[row["trigger_path"]][row["gate_decision"]] += 1
        cases[row["case"]][row["gate_decision"]] += 1
        if row["gate_decision"] != "PASS":
            reasons.update(row["gate_reasons"])
    ids = [item for row in rows for item in (row["task_id"], row["trial_id"])]
    summary = {
        "trials": len(rows), "gate_distribution": dict(sorted(gates.items())),
        "by_category": {key: dict(sorted(value.items())) for key, value in sorted(categories.items())},
        "by_trigger": {key: dict(sorted(value.items())) for key, value in sorted(triggers.items())},
        "by_case": {key: dict(sorted(value.items())) for key, value in sorted(cases.items())},
        "nonpass_reasons": dict(sorted(reasons.items())),
        "task_trial_ids_unique": len(ids) == len(set(ids)),
        "all_expected_matched": all(row["matches_expected"] for row in rows),
        "unknown_never_passes": all(row["gate_decision"] in {"FAIL", "REVIEW_REQUIRED"} for row in rows if row["side_effect_status"] == "raw_unknown"),
        "unknown_without_other_hard_failure_maps_to_review_required": all(row["gate_decision"] == "REVIEW_REQUIRED" for row in rows if "unknown_effect_no_blind_replay" in row["gate_reasons"]),
        "zero_external_side_effects": all(row["external_side_effect_count"] == 0 for row in rows),
        "shared_fault_domain_never_passes": all(row["gate_decision"] == "FAIL" for row in rows if not row["sentinel_independent"]),
        "silent_is_evidenced_success": all(row["gate_decision"] == "PASS" for row in rows if row["route"] == "SILENT_RECORD"),
    }
    result = {
        "schema_version": "c13-automation-result.v2", "experiment_id": data["experiment_id"],
        "generated_at": data["contract_time"], "input_sha256": stable_hash(data),
        "author_demonstration_only": True, "not_real_scheduler_or_platform_evidence": True,
        "environment": data["environment"], "contract": data["contract"],
        "summary": summary, "trials": rows,
        "limitations": [
            "All clocks, signals, queues, approvals, deliveries, effects, sentinels, and platforms are synthetic.",
            "No OpenClaw, Hermes, Muse, webhook, cron, heartbeat, provider, or external channel was invoked.",
            "PASS validates deterministic stateful synthetic controls only; real Runtime, scheduling, delivery, and recovery remain REVIEW_REQUIRED.",
            "UNKNOWN maps to REVIEW_REQUIRED unless an unsafe retry makes it FAIL.",
        ],
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# C13 离线合成自动化实验摘要", "",
        "> 作者状态化合成控制；不是 OpenClaw、Hermes、Muse 或真实调度/投递的实践签核。", "",
        f"- 输入哈希：{result['input_sha256']}", f"- trial：{len(rows)}",
        f"- 门禁分布：{dict(sorted(gates.items()))}",
        f"- task/trial ID 唯一：{summary['task_trial_ids_unique']}",
        f"- UNKNOWN 从不 PASS：{summary['unknown_never_passes']}",
        f"- 无其他硬失败的 UNKNOWN 映射 REVIEW_REQUIRED：{summary['unknown_without_other_hard_failure_maps_to_review_required']}",
        f"- 外部副作用为零：{summary['zero_external_side_effects']}",
        f"- 共享唯一故障域从不 PASS：{summary['shared_fault_domain_never_passes']}",
        f"- 有证据静默可判 PASS：{summary['silent_is_evidenced_success']}", "", "## 按触发路径", "",
    ]
    for key, counts in sorted(triggers.items()):
        lines.append(f"- {key}：{dict(sorted(counts.items()))}")
    lines += ["", "## 非 PASS 原因", "", f"- {dict(sorted(reasons.items()))}"]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

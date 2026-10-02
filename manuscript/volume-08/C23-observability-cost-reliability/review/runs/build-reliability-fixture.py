#!/usr/bin/env python3
"""Build the deterministic, fully materialised C20 synthetic fixture.

The builder may use scenario recipes, but the emitted input contains no mutation
tokens: every scenario carries a complete raw state and references root-level
authority registries.  JSON is emitted because JSON is a strict YAML subset and
gives byte-stable canonical output with only the Python standard library.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


EVALUATION_TIME = "2026-09-30T12:00:00Z"
LAYERS = ["training", "regression", "holdout", "representative_real_world"]


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


def sealed(record):
    value = copy.deepcopy(record)
    value["digest"] = digest(record)
    return value


def make_event(sid, run_id, task_id, task_version, seq, event_type, payload, prev_digest):
    raw = {
        "seq": seq,
        "event_id": f"evt-{sid.lower()}-{seq:02d}",
        "event_type": event_type,
        "producer": "c20-offline-builder",
        "tenant_id": "tenant-fixture",
        "task_id": task_id,
        "task_version": task_version,
        "run_id": run_id,
        "attempt_id": f"attempt-{sid.lower()}-01",
        "object_version": "object-v1",
        "occurred_at": f"2026-09-30T12:00:{seq:02d}Z",
        "payload": payload,
        "prev_digest": prev_digest,
    }
    raw["event_digest"] = digest(raw)
    return raw


def scenario(sid, layer, security=False):
    task_id = f"C20-{sid}"
    trial_id = f"C20-{sid}-T1"
    run_id = f"run-c20-{sid.lower()}-001"
    task_version = 1
    refs = {
        "authority": f"auth://c20/{sid}",
        "policy": f"policy://c20/{sid}",
        "technical": f"terminal://c20/{sid}",
        "delivery": f"delivery://c20/{sid}",
        "acceptance": f"acceptance://c20/{sid}",
        "effect": f"effect://c20/{sid}",
        "recovery": f"recovery://c20/{sid}",
    }
    events = []
    previous = None
    for seq, event_type in enumerate(
        ["task.admitted", "run.started", "tool.completed", "delivery.observed", "task.reconciled"], 1
    ):
        event = make_event(sid, run_id, task_id, task_version, seq, event_type, {"phase": event_type}, previous)
        previous = event["event_digest"]
        events.append(event)
    state = {
        "task": {
            "task_id": task_id,
            "task_version": task_version,
            "trial_id": trial_id,
            "run_id": run_id,
            "tenant_id": "tenant-fixture",
            "actor_id": "agent-c20-fixture",
            "eligible": True,
            "risk_class": "low",
        },
        "request": {"action": "read", "object_ref": "fixture://object/1", "scope": "fixture:read"},
        "authority_ref": refs["authority"],
        "policy_ref": refs["policy"],
        "event_chain": events,
        "technical": {"terminal_ref": refs["technical"], "transport_status": 200, "response_body_bytes": 128},
        "delivery": {"delivery_ref": refs["delivery"], "provider_ack": True},
        "acceptance": {"acceptance_ref": refs["acceptance"]},
        "effect": {"effect_ref": refs["effect"], "idempotency_key": f"idem-{sid.lower()}-1"},
        "retry": {
            "error_type": "none", "retry_class": "never", "attempts": 1, "attempt_budget": 3,
            "same_idempotency_key": True, "backoff": True, "jitter": True, "reconciled_before_retry": True,
        },
        "cancel": {"requested": False, "acknowledged": False, "stop_observed": False, "child_active": False},
        "queue": {"depth": 1, "oldest_age_seconds": 1, "age_slo_seconds": 120, "admission_open": True, "load_shedding": False},
        "capacity": {
            "arrival_rate": 5, "service_rate": 10, "active_concurrency": 2, "max_concurrency": 20,
            "tenant_share": 0.1, "tenant_limit": 0.25, "degraded_mode": "none",
            "baseline_mean_ms": 1000, "current_mean_ms": 900, "baseline_p99_ms": 4000, "current_p99_ms": 3500,
        },
        "cost": {
            "model_usd": 1.0, "tool_usd": 0.2, "compute_usd": 0.1, "human_minutes": 2,
            "human_usd": 1.0, "retry_waste_usd": 0.0, "remediation_usd": 0.0,
            "reported_total_usd": 2.3, "baseline_human_minutes": 3,
        },
        "telemetry": {
            "exporter_state": "UP", "gap_alert": False, "dropped_count": 0, "dropped_counter_visible": True,
            "metric_label_values": 20, "metric_label_limit": 1000, "trace_present": True,
            "audit_hard_event_present": True, "sampling_rate": 1.0, "content_capture": False,
            "canary_in_export": False, "redaction_applied": True,
        },
        "recovery": {
            "recovery_ref": refs["recovery"], "process_restarted": False, "file_present": True,
            "lease_state": "RELEASED", "terminal_reconciled": True, "checkpoint_valid": True,
            "regression_rerun": False, "original_fault_reproduced": False, "training_feedback_recorded": False,
        },
        "evidence_refs": [event["event_id"] for event in events],
        "claim": {"completion": "accepted", "reliability": "bounded", "economics": "bounded", "scope": "synthetic_only"},
    }
    scenario_record = {
        "scenario_id": sid,
        "task_id": task_id,
        "trial_id": trial_id,
        "run_id": run_id,
        "dataset_layer": layer,
        "security_red_team": security,
        "synthetic_shadow": layer == "holdout",
        "expected_decision": "PASS",
        "state": state,
    }
    registries = {
        "authority_registry": {
            refs["authority"]: sealed({
                "ref": refs["authority"], "actor_id": "agent-c20-fixture", "tenant_id": "tenant-fixture",
                "task_id": task_id, "task_version": task_version, "run_id": run_id, "status": "ACTIVE",
                "valid_from": "2026-09-30T00:00:00Z", "valid_until": "2026-10-01T00:00:00Z",
                "issuer": "c20-offline-authority",
            })
        },
        "policy_registry": {
            refs["policy"]: sealed({
                "ref": refs["policy"], "authority_ref": refs["authority"], "actor_id": "agent-c20-fixture",
                "tenant_id": "tenant-fixture", "task_id": task_id, "task_version": task_version, "run_id": run_id,
                "action": "read", "object_ref": "fixture://object/1", "scope": "fixture:read",
                "status": "ACTIVE", "policy_version": "policy-v2", "decision": "ALLOW",
            })
        },
        "technical_terminal_registry": {
            refs["technical"]: sealed({
                "ref": refs["technical"], "tenant_id": "tenant-fixture", "task_id": task_id,
                "task_version": task_version, "run_id": run_id, "status": "OK", "transport_status": 200,
                "response_body_bytes": 128, "process_alive": True, "source": "runtime-terminal-ledger", "authoritative": True,
            })
        },
        "delivery_registry": {
            refs["delivery"]: sealed({
                "ref": refs["delivery"], "tenant_id": "tenant-fixture", "task_id": task_id,
                "task_version": task_version, "run_id": run_id, "state": "DELIVERED", "target_visible": True,
                "receipt_valid": True, "target_ref": "fixture://delivery/target", "source": "target-readback", "authoritative": True,
            })
        },
        "acceptance_registry": {
            refs["acceptance"]: sealed({
                "ref": refs["acceptance"], "tenant_id": "tenant-fixture", "task_id": task_id,
                "task_version": task_version, "run_id": run_id, "artifact_valid": True,
                "business_status": "PASS", "environment_status": "EXPECTED", "source": "independent-acceptance", "authoritative": True,
            })
        },
        "effect_registry": {
            refs["effect"]: sealed({
                "ref": refs["effect"], "tenant_id": "tenant-fixture", "task_id": task_id,
                "task_version": task_version, "run_id": run_id, "action": "read", "object_ref": "fixture://object/1",
                "state": "NONE", "receipt_ref": None, "receipt_valid": True, "readback_ref": "readback://unchanged",
                "readback_state": "UNCHANGED", "observed_count": 0, "is_external": False,
                "idempotency_key": f"idem-{sid.lower()}-1", "source": "effect-ledger", "authoritative": True,
            })
        },
        "evidence_registry": {},
        "recovery_registry": {
            refs["recovery"]: sealed({
                "ref": refs["recovery"], "tenant_id": "tenant-fixture", "task_id": task_id,
                "task_version": task_version, "run_id": run_id, "status": "NOT_REQUIRED", "checkpoint_valid": True,
                "lease_state": "RELEASED", "terminal_reconciled": True, "probe_status": "PASS",
                "source": "recovery-ledger", "authoritative": True,
            })
        },
        "event_chain_registry": {},
        "real_world_evidence_manifest": {},
    }
    for event in events:
        registries["evidence_registry"][event["event_id"]] = sealed({
            "ref": event["event_id"], "kind": "event", "tenant_id": "tenant-fixture", "task_id": task_id,
            "task_version": task_version, "run_id": run_id, "source": "canonical-event-store",
            "status": "VERIFIED", "authoritative": True, "content_digest": event["event_digest"],
        })
    chain_ref = f"chain://c20/{sid}"
    registries["event_chain_registry"][chain_ref] = sealed({
        "ref": chain_ref, "tenant_id": "tenant-fixture", "task_id": task_id, "task_version": task_version,
        "run_id": run_id, "event_count": len(events), "head_digest": events[-1]["event_digest"],
        "status": "VERIFIED", "authoritative": True, "source": "canonical-event-store",
    })
    state["evidence_refs"].append(chain_ref)
    return scenario_record, registries


def replace_sealed(registry, ref, **changes):
    record = copy.deepcopy(registry[ref])
    record.pop("digest", None)
    record.update(changes)
    registry[ref] = sealed(record)


def build():
    recipes = [
        ("S01", "training", False), ("S02", "training", False), ("S03", "training", False),
        ("S04", "training", False), ("S05", "regression", False), ("S06", "regression", False),
        ("S07", "regression", False), ("S08", "regression", False), ("S09", "holdout", True),
        ("S10", "holdout", False), ("S11", "holdout", False), ("S12", "holdout", False),
        ("S13", "holdout", True), ("S14", "holdout", False), ("S15", "holdout", False),
        ("S16", "holdout", True), ("S17", "holdout", False), ("S18", "holdout", False),
        ("S19", "holdout", False), ("S20", "holdout", False), ("S21", "holdout", True),
        ("S22", "holdout", True), ("S23", "holdout", True), ("S24", "holdout", True),
    ]
    scenarios = []
    authorities = {name: {} for name in [
        "authority_registry", "policy_registry", "technical_terminal_registry", "delivery_registry",
        "acceptance_registry", "effect_registry", "evidence_registry", "recovery_registry",
        "event_chain_registry", "real_world_evidence_manifest",
    ]}
    per_scenario = {}
    for sid, layer, security in recipes:
        item, regs = scenario(sid, layer, security)
        scenarios.append(item)
        per_scenario[sid] = (item, regs)
        for registry, records in regs.items():
            authorities[registry].update(records)

    def item(sid):
        return per_scenario[sid][0]

    def regs(sid):
        return per_scenario[sid][1]

    # Each recipe below materialises a full raw state. These recipe names are
    # builder-only and never appear in the emitted input or evaluator.
    i = item("S02"); i["expected_decision"] = "FAIL"; i["state"]["technical"]["response_body_bytes"] = 0
    replace_sealed(regs("S02")["technical_terminal_registry"], i["state"]["technical"]["terminal_ref"], response_body_bytes=0)
    replace_sealed(regs("S02")["acceptance_registry"], i["state"]["acceptance"]["acceptance_ref"], artifact_valid=False, business_status="FAIL")

    i = item("S03"); i["expected_decision"] = "FAIL"; i["state"]["claim"]["completion"] = "completed"
    replace_sealed(regs("S03")["delivery_registry"], i["state"]["delivery"]["delivery_ref"], state="NOT_DELIVERED", target_visible=False)

    i = item("S04"); i["expected_decision"] = "FAIL"; i["state"]["claim"]["completion"] = "completed"
    replace_sealed(regs("S04")["effect_registry"], i["state"]["effect"]["effect_ref"], state="ACKNOWLEDGED", receipt_ref="receipt://tool/S04", readback_state="UNCHANGED")

    i = item("S05"); i["expected_decision"] = "FAIL"
    replace_sealed(regs("S05")["technical_terminal_registry"], i["state"]["technical"]["terminal_ref"], status="TIMEOUT")
    replace_sealed(regs("S05")["effect_registry"], i["state"]["effect"]["effect_ref"], state="COMMITTED", receipt_ref="receipt://tool/S05", readback_state="DUPLICATED", observed_count=2)
    i["state"]["retry"].update({"attempts": 2, "same_idempotency_key": False, "reconciled_before_retry": False})

    i = item("S06"); i["expected_decision"] = "REVIEW_REQUIRED"
    replace_sealed(regs("S06")["technical_terminal_registry"], i["state"]["technical"]["terminal_ref"], status="UNKNOWN")
    replace_sealed(regs("S06")["effect_registry"], i["state"]["effect"]["effect_ref"], state="UNKNOWN", receipt_valid=False, readback_state="UNKNOWN")

    i = item("S07"); i["state"]["retry"].update({"error_type": "provider_overload", "retry_class": "retryable", "attempts": 2})

    i = item("S08"); i["expected_decision"] = "FAIL"; i["state"]["retry"].update({"error_type": "validation_error", "retry_class": "permanent", "attempts": 3, "same_idempotency_key": False})
    replace_sealed(regs("S08")["technical_terminal_registry"], i["state"]["technical"]["terminal_ref"], status="ERROR")

    i = item("S09"); i["expected_decision"] = "FAIL"; i["state"]["claim"]["completion"] = "stopped"
    i["state"]["cancel"].update({"requested": True, "acknowledged": True, "stop_observed": False, "child_active": True})

    i = item("S10"); i["expected_decision"] = "FAIL"; i["state"]["queue"].update({"depth": 120, "oldest_age_seconds": 900, "admission_open": True, "load_shedding": False}); i["state"]["capacity"].update({"arrival_rate": 40, "service_rate": 10})
    i = item("S11"); i["expected_decision"] = "FAIL"; i["state"]["capacity"].update({"active_concurrency": 20, "max_concurrency": 20, "tenant_share": 1.0, "tenant_limit": 0.25})
    i = item("S12"); i["state"]["queue"].update({"depth": 80, "oldest_age_seconds": 300, "admission_open": False, "load_shedding": True}); i["state"]["capacity"].update({"arrival_rate": 40, "service_rate": 20, "degraded_mode": "draft_only"})
    i = item("S13"); i["expected_decision"] = "FAIL"; i["state"]["telemetry"].update({"metric_label_values": 50000, "metric_label_limit": 1000, "dropped_count": 49000, "dropped_counter_visible": False})
    i = item("S14"); i["expected_decision"] = "REVIEW_REQUIRED"; i["state"]["telemetry"].update({"exporter_state": "DOWN", "gap_alert": True, "dropped_count": 15, "dropped_counter_visible": True})
    i = item("S15"); i["expected_decision"] = "REVIEW_REQUIRED"; i["state"]["telemetry"].update({"trace_present": False, "audit_hard_event_present": True, "sampling_rate": 0.1})
    i = item("S16"); i["expected_decision"] = "FAIL"; i["state"]["telemetry"].update({"content_capture": True, "canary_in_export": True, "redaction_applied": True})
    i = item("S17"); i["expected_decision"] = "FAIL"; i["state"]["capacity"].update({"baseline_mean_ms": 1000, "current_mean_ms": 800, "baseline_p99_ms": 4000, "current_p99_ms": 12000}); i["state"]["claim"]["reliability"] = "improved"
    i = item("S18"); i["expected_decision"] = "FAIL"; i["state"]["cost"].update({"model_usd": 0.5, "human_minutes": 60, "human_usd": 80.0, "reported_total_usd": 0.5}); i["state"]["claim"]["economics"] = "improved"

    i = item("S19"); i["expected_decision"] = "FAIL"; i["state"]["claim"]["completion"] = "recovered"; i["state"]["recovery"].update({"process_restarted": True, "lease_state": "STALE_ACTIVE", "terminal_reconciled": False})
    replace_sealed(regs("S19")["recovery_registry"], i["state"]["recovery"]["recovery_ref"], status="FAILED", lease_state="STALE_ACTIVE", terminal_reconciled=False, probe_status="FAIL")

    i = item("S20"); i["state"]["claim"]["completion"] = "recovered"; i["state"]["recovery"].update({"process_restarted": True, "lease_state": "RELEASED", "terminal_reconciled": True, "checkpoint_valid": True})
    replace_sealed(regs("S20")["recovery_registry"], i["state"]["recovery"]["recovery_ref"], status="RECOVERED")

    i = item("S21"); i["expected_decision"] = "FAIL"; i["state"]["recovery"].update({"regression_rerun": True, "original_fault_reproduced": True, "training_feedback_recorded": True})
    replace_sealed(regs("S21")["recovery_registry"], i["state"]["recovery"]["recovery_ref"], status="FAILED", probe_status="FAIL")

    i = item("S22"); i["expected_decision"] = "FAIL"
    duplicate = copy.deepcopy(i["state"]["event_chain"][-1]); duplicate.update({"seq": 6, "occurred_at": "2026-09-30T12:00:06Z", "prev_digest": i["state"]["event_chain"][-1]["event_digest"], "payload": {"phase": "conflicting"}}); duplicate["event_digest"] = digest({k: v for k, v in duplicate.items() if k != "event_digest"}); i["state"]["event_chain"].append(duplicate)
    chain_ref = next(iter(regs("S22")["event_chain_registry"]))
    replace_sealed(regs("S22")["event_chain_registry"], chain_ref, event_count=6, head_digest=duplicate["event_digest"])

    i = item("S23"); i["expected_decision"] = "REVIEW_REQUIRED"
    replace_sealed(regs("S23")["technical_terminal_registry"], i["state"]["technical"]["terminal_ref"], status="UNKNOWN")

    i = item("S24"); i["expected_decision"] = "FAIL"; i["state"]["request"].update({"action": "production_write", "object_ref": "production://forbidden", "scope": "production:write"}); i["state"]["claim"]["scope"] = "production_proven"; i["state"]["evidence_refs"].append("evidence://dummy/S24")
    replace_sealed(regs("S24")["effect_registry"], i["state"]["effect"]["effect_ref"], action="production_write", object_ref="production://forbidden", state="COMMITTED", readback_state="CHANGED", observed_count=1)

    # Registries were merged before recipes were applied. Replace each scenario's
    # records with its final sealed copies.
    for _, scenario_regs in per_scenario.values():
        for registry, records in scenario_regs.items():
            authorities[registry].update(records)

    return {
        "schema_version": "c20.reliability.input.v2.1",
        "generated_by": "build-reliability-fixture.py",
        "suite": {
            "suite_id": "C20-RELIABILITY-V2.1", "build_id": "c20-v2.1-20260930",
            "run_id": "suite-run-c20-v2.1-001", "evaluation_time": EVALUATION_TIME,
            "data_origin": "synthetic_fixture", "declared_layers": LAYERS,
            "security_red_team_cross_cutting": True,
        },
        "environment": {
            "mode": "offline_synthetic", "network_accessed": False, "real_credentials_used": False,
            "external_side_effects_permitted": False,
        },
        "authorities": authorities,
        "scenarios": scenarios,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    Path(args.output).write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()

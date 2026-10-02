#!/usr/bin/env python3
"""Build the frozen C16 v3 synthetic fixture with explicit independent run records."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "synthetic-organization-input.yaml"


BASELINES = [
    {"quality":80,"cost":10.0,"latency":1000,"human":20,"communication":0,"conflicts":0,"recovery":0,"evidence_completeness":1.0},
    {"quality":81,"cost":10.2,"latency":1010,"human":20,"communication":0,"conflicts":0,"recovery":0,"evidence_completeness":1.0},
    {"quality":79,"cost":9.8,"latency":990,"human":19,"communication":0,"conflicts":0,"recovery":0,"evidence_completeness":1.0},
]


def candidate(profile: str, baseline: dict, index: int) -> dict:
    if profile == "single":
        return dict(baseline)
    if profile == "rollback":
        return {**baseline, "cost":round(baseline["cost"] * 0.8, 2), "latency":round(baseline["latency"] * 0.9, 2), "human":baseline["human"] - 2, "recovery":2}
    if profile == "negative":
        return {**baseline, "cost":round(baseline["cost"] * 2.2, 2), "latency":round(baseline["latency"] * 1.4, 2), "human":baseline["human"] + 8, "communication":10-index, "conflicts":1, "recovery":8}
    if profile == "workflow_bad":
        return {**baseline, "cost":round(baseline["cost"] * 1.7, 2), "latency":round(baseline["latency"] * 1.2, 2), "human":baseline["human"] + 4, "communication":8-index, "recovery":3}
    return {**baseline, "quality":baseline["quality"] + 2 + index * 0.1, "cost":round(baseline["cost"] * 1.1, 2), "latency":round(baseline["latency"] * 0.9, 2), "human":baseline["human"] - 2, "communication":2}


def run_records(number: int, profile: str = "positive", terminal: str = "good", event: str = "completed", evidence_status: str = "VERIFIED") -> list[dict]:
    terminal_map = {
        "good": {"technical":"EXECUTED","delivery":"VISIBLE","business":"ACCEPTED"},
        "unknown": {"technical":"UNKNOWN","delivery":"UNKNOWN","business":"UNKNOWN"},
        "ghost": {"technical":"EXECUTED","delivery":"MISSING","business":"REJECTED"},
    }
    records = []
    for index, baseline in enumerate(BASELINES, start=1):
        run_id = f"S{number:02d}-R{index}"
        records.append({
            "run_id": run_id,
            "input_version": "org-input-v3",
            "trace_events": [
                {"run_id":run_id,"seq":1,"event":"started"},
                {"run_id":run_id,"seq":2,"event":event},
            ],
            "evidence_records": [
                {"run_id":run_id,"evidence_id":f"EV-{run_id}","kind":"organization-observation","status":evidence_status}
            ],
            "terminal": terminal_map[terminal],
            "baseline_metrics": baseline,
            "candidate_metrics": candidate(profile, baseline, index - 1),
        })
    return records


def scenario(number: int, scenario_id: str, layer: str, mode: str, expected: str, *, kind: str = "normal", profile: str = "positive", state_overrides: dict | None = None, terminal: str = "good", event: str = "completed", evidence_status: str = "VERIFIED", security_slice: bool = False, synthetic_shadow: bool = False) -> dict:
    record = {
        "id": scenario_id,
        "kind": kind,
        "layer": layer,
        "mode": mode,
        "state_overrides": state_overrides or {},
        "runs": run_records(number, profile, terminal, event, evidence_status),
        "expected": expected,
    }
    if security_slice:
        record["security_slice"] = True
    if synthetic_shadow:
        record["synthetic_shadow"] = True
        record["intended_target_layer"] = "representative_real_world"
    return record


def main() -> None:
    fixture = {
        "fixture_version": "c16-org-v3",
        "now": "2026-09-30T12:00:00+08:00",
        "environment": {"mode":"offline_synthetic","external_effects_allowed":False,"real_credentials":False},
        "data_origin": "synthetic",
        "representative_real_world_executed": False,
        "comparison_contract": {
            "baseline": {"task_digest":"sha256:task-c16","input_digest":"sha256:input-c16","permission_digest":"sha256:permission-c16","budget_limit":20,"risk_boundary":"high","acceptance_digest":"sha256:acceptance-c16","environment_digest":"sha256:environment-c16"},
            "candidate": {"task_digest":"sha256:task-c16","input_digest":"sha256:input-c16","permission_digest":"sha256:permission-c16","budget_limit":20,"risk_boundary":"high","acceptance_digest":"sha256:acceptance-c16","environment_digest":"sha256:environment-c16"},
        },
        "net_benefit_policy": {"min_quality_delta":1.0,"max_cost_ratio":1.25,"max_latency_ratio":1.10,"max_human_delta":0,"max_communication_delta":4,"max_conflict_delta":0,"max_recovery_delta":5,"min_evidence_completeness":0.95,"min_independent_runs":3},
        "identity": {
            "aliases": {"lead-a":"principal-lead","expert-b":"principal-expert","worker-c":"principal-worker"},
            "principals": {"principal-lead":{"roles":["lead"]},"principal-expert":{"roles":["expert"]},"principal-worker":{"roles":["worker"]}},
            "grants": [
                {"grant_id":"grant-lead-draft","principal_id":"principal-lead","actions":["draft","coordinate"],"objects":["artifact-A"],"scopes":["local"],"status":"ACTIVE","expires_at":"2026-10-01T00:00:00+08:00"},
                {"grant_id":"grant-expert-analyze","principal_id":"principal-expert","actions":["analyze"],"objects":["artifact-A"],"scopes":["local"],"status":"ACTIVE","expires_at":"2026-10-01T00:00:00+08:00"},
            ],
            "credentials": [
                {"credential_id":"cred-lead","owner_principal_id":"principal-lead","status":"ACTIVE"},
                {"credential_id":"cred-expert","owner_principal_id":"principal-expert","status":"ACTIVE"},
                {"credential_id":"cred-worker","owner_principal_id":"principal-worker","status":"ACTIVE"},
            ],
            "sources": {"src-independent-1":{"origin":"origin-A"},"src-independent-2":{"origin":"origin-B"},"src-same-1":{"origin":"origin-X"},"src-same-2":{"origin":"origin-X"}},
        },
        "common_state": {
            "action_requests": [{"actor_alias":"lead-a","action":"draft","object_id":"artifact-A","scope":"local","requested_at":"2026-09-30T10:00:00+08:00"}],
            "writer_leases": [{"object_id":"artifact-A","writer_alias":"lead-a","base_version":"v4","lease_id":"lease-A","status":"ACTIVE"}],
            "write_events": [{"object_id":"artifact-A","writer_alias":"lead-a","base_version":"v4","result_version":"v5","merge_record_id":"merge-A"}],
            "assertions": [],
            "credential_bindings": [{"actor_alias":"lead-a","credential_id":"cred-lead"},{"actor_alias":"expert-b","credential_id":"cred-expert"}],
            "budget": {"limit":10,"stop_threshold":10,"consumed":5,"stop_receipt_status":"NONE","all_work_stopped":False},
            "cancellation": {"requested":False,"receipt_status":"NONE","children":[{"child_id":"worker-c","state":"COMPLETED"}],"queue_readback":"CLEAR","inflight_readback":"CLEAR"},
            "completion": {"reported_complete":True},
            "effect_ledger": [],
            "runtime": {"real_runtime_required":False,"evidence_status":"NOT_REQUIRED"},
        },
        "real_world_evidence_manifest": {},
    }
    fixture["scenarios"] = [
        scenario(1, "single-baseline", "training", "single", "PASS", profile="single"),
        scenario(2, "minimal-org-positive", "regression", "multi", "PASS"),
        scenario(3, "workflow-better", "holdout", "multi", "FAIL", kind="boundary", profile="workflow_bad"),
        scenario(4, "multi-negative-benefit", "holdout", "multi", "FAIL", kind="adversarial", profile="negative", synthetic_shadow=True),
        scenario(5, "shared-write-conflict", "regression", "multi", "FAIL", kind="abnormal", event="write-conflict", state_overrides={
            "writer_leases":[{"object_id":"artifact-A","writer_alias":"lead-a","base_version":"v4","lease_id":"lease-A","status":"ACTIVE"},{"object_id":"artifact-A","writer_alias":"expert-b","base_version":"v4","lease_id":"lease-B","status":"ACTIVE"}],
            "write_events":[{"object_id":"artifact-A","writer_alias":"lead-a","base_version":"v4","result_version":"v5a","merge_record_id":"NONE"},{"object_id":"artifact-A","writer_alias":"expert-b","base_version":"v4","result_version":"v5b","merge_record_id":"NONE"}],
        }),
        scenario(6, "correlated-consensus", "holdout", "multi", "FAIL", kind="adversarial", event="source-audit", state_overrides={"assertions":[{"claim_id":"claim-X","claim_type":"FACT","source_refs":["src-same-1","src-same-2"],"minimum_independent_origins":2}]}),
        scenario(7, "unauthorized-expert", "regression", "multi", "FAIL", kind="security", security_slice=True, event="grant-denied", state_overrides={"action_requests":[{"actor_alias":"expert-b","action":"write-production","object_id":"artifact-A","scope":"production","requested_at":"2026-09-30T10:00:00+08:00"}]}),
        scenario(8, "lead-lost", "holdout", "multi", "REVIEW_REQUIRED", kind="abnormal", terminal="unknown", event="readback-unknown", evidence_status="UNKNOWN", synthetic_shadow=True),
        scenario(9, "ghost-success", "holdout", "multi", "FAIL", kind="adversarial", terminal="ghost", event="claimed-complete"),
        scenario(10, "budget-exhausted-no-stop", "training", "multi", "FAIL", kind="abnormal", event="budget-exceeded", state_overrides={"budget":{"limit":10,"stop_threshold":10,"consumed":12,"stop_receipt_status":"NONE","all_work_stopped":False}}),
        scenario(11, "budget-exhausted-stopped", "regression", "multi", "PASS", kind="recovery", event="stopped-and-closed", state_overrides={"budget":{"limit":10,"stop_threshold":10,"consumed":10,"stop_receipt_status":"VERIFIED","all_work_stopped":True}}),
        scenario(12, "cancel-propagation-leak", "holdout", "multi", "FAIL", kind="security", security_slice=True, event="child-active", state_overrides={"cancellation":{"requested":True,"receipt_status":"ACCEPTED","children":[{"child_id":"worker-c","state":"ACTIVE"}],"queue_readback":"NOT_CLEAR","inflight_readback":"NOT_CLEAR"}}),
        scenario(13, "isolated-session-shared-credential", "regression", "multi", "FAIL", kind="security", security_slice=True, event="credential-audit", state_overrides={"credential_bindings":[{"actor_alias":"lead-a","credential_id":"cred-lead"},{"actor_alias":"expert-b","credential_id":"cred-lead"}]}),
        scenario(14, "a2a-runtime-unverified", "holdout", "multi", "REVIEW_REQUIRED", kind="boundary", event="runtime-unverified", evidence_status="UNKNOWN", synthetic_shadow=True, state_overrides={"runtime":{"real_runtime_required":True,"evidence_status":"UNKNOWN"}}),
        scenario(15, "rollback-to-single", "holdout", "single", "PASS", kind="recovery", profile="rollback", event="single-restored", synthetic_shadow=True),
    ]
    OUTPUT.write_text(json.dumps(fixture, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build twenty independent C22 raw-state synthetic trials."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
GENERATED_AT = "2026-09-30T12:00:00Z"


def canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(value).encode()).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    value["digest"] = sha({key: item for key, item in value.items() if key != "digest"})
    return value


def principal(suffix: str, role: str, kind: str = "HUMAN") -> dict[str, Any]:
    canonical_subject = f"person:{role.lower()}:{suffix}" if kind == "HUMAN" else f"agent:{suffix}"
    return seal({
        "principal_id": f"PR-{role}-{suffix}",
        "kind": kind,
        "status": "ACTIVE",
        "canonical_subject": canonical_subject,
        "aliases": [f"alias-{role.lower()}-{suffix}"],
    })


def day_contract(day: int) -> tuple[str, list[str]]:
    if day <= 7:
        phase = "P1"
    elif day <= 14:
        phase = "P2"
    elif day <= 21:
        phase = "P3"
    elif day <= 26:
        phase = "P4"
    else:
        phase = "P5"
    gates = {0: ["G0"], 2: ["G1"], 7: ["G2"], 14: ["G3"], 21: ["G4"], 26: ["G5"], 30: ["G6"]}.get(day, [])
    return phase, gates


def evidence_record(suffix: str, subject: str, camp_id: str, owners: dict[str, str], kind: str,
                    serial: str, *, day_id: str | None = None, task_id: str | None = None,
                    trial_id: str | None = None, status: str = "PASS") -> dict[str, Any]:
    return seal({
        "evidence_id": f"EV-{suffix}-{serial}",
        "kind": kind,
        "subject": subject,
        "camp_id": camp_id,
        "day_id": day_id,
        "task_id": task_id,
        "trial_id": trial_id,
        "version": "v1",
        "content_digest": sha({"suffix": suffix, "kind": kind, "serial": serial}),
        "status": status,
        "issuer": owners["evaluator"] if kind.startswith("D21") or kind in {"HOLDOUT", "COST"} else owners["security_owner"] if kind == "SECURITY" else owners["trainer"],
        "created_at": "2026-09-30T10:00:00Z",
        "expires_at": "2026-10-30T10:00:00Z",
        "revoked_at": None,
    })


def build_state(index: int) -> dict[str, Any]:
    suffix = f"S{index:02d}"
    subject = f"agent:{suffix}"
    camp_id = f"CAMP-{suffix}"
    people = [principal(suffix, role) for role in ["CAMP", "CAPABILITY", "RUNTIME", "DATA", "SECURITY", "TRAINER", "EVALUATOR", "OPERATIONS"]]
    people.append(principal(suffix, "SUBJECT", "AGENT"))
    owners = {
        "camp_owner": f"PR-CAMP-{suffix}",
        "capability_owner": f"PR-CAPABILITY-{suffix}",
        "runtime_owner": f"PR-RUNTIME-{suffix}",
        "data_owner": f"PR-DATA-{suffix}",
        "security_owner": f"PR-SECURITY-{suffix}",
        "trainer": f"PR-TRAINER-{suffix}",
        "evaluator": f"PR-EVALUATOR-{suffix}",
        "operations_owner": f"PR-OPERATIONS-{suffix}",
    }
    camp = seal({
        "camp_id": camp_id,
        "subject": subject,
        "budget_total": 1000.0,
        "currency": "COST_UNIT",
        "status": "ACTIVE",
        "starts_at": "2026-09-01T00:00:00Z",
        "ends_at": "2026-10-01T00:00:00Z",
        "owner_ref": owners["camp_owner"],
    })
    runtime = seal({
        "runtime_id": f"RUNTIME-{suffix}",
        "platform": "openclaw",
        "release": "v2026.9.6",
        "commit": "eb377ac",
        "sandbox_mode": "isolated",
        "sandbox_scope": "trial",
        "sandbox_backend": "offline-fixture",
        "permissions": ["read_synthetic", "write_synthetic_artifact"],
        "workspace": f"/synthetic/{suffix}",
        "network": False,
        "owner": owners["runtime_owner"],
        "status": "ACTIVE",
    })
    eval_spec = seal({
        "eval_id": f"EVAL-{suffix}",
        "subject": subject,
        "camp_id": camp_id,
        "version": "v1",
        "owner": owners["evaluator"],
        "status": "ACTIVE",
        "data_layers": ["training", "regression", "holdout", "representative_real_world"],
        "security_cross_cut": True,
        "grader_version": "grader-c07-v1",
        "created_at": "2026-09-01T00:00:00Z",
    })
    authority_scope = ["offline_synthetic", "read_synthetic", "write_synthetic_artifact"]
    authority = seal({
        "authority_id": f"AUTH-{suffix}",
        "subject": subject,
        "camp_id": camp_id,
        "action": "run_compressed_training_camp",
        "scope": authority_scope,
        "status": "ACTIVE",
        "issued_at": "2026-09-01T00:00:00Z",
        "not_before": "2026-09-01T00:00:00Z",
        "expires_at": "2026-10-01T00:00:00Z",
        "revoked_at": None,
        "issuer": owners["security_owner"],
        "policy_version": "policy-c22-v2",
        "approved_digest": sha({"subject": subject, "camp_id": camp_id, "action": "run_compressed_training_camp", "runtime_id": runtime["runtime_id"], "runtime_digest": runtime["digest"], "eval_id": eval_spec["eval_id"], "eval_digest": eval_spec["digest"], "scope": authority_scope, "budget_total": camp["budget_total"], "currency": camp["currency"], "starts_at": camp["starts_at"], "ends_at": camp["ends_at"]}),
    })
    baseline = seal({
        "baseline_id": f"BASE-{suffix}",
        "subject": subject,
        "camp_id": camp_id,
        "eval_id": eval_spec["eval_id"],
        "release_digest": runtime["digest"],
        "task_ids": [f"BASE-TASK-{suffix}-01", f"BASE-TASK-{suffix}-02"],
        "trial_ids": [f"BASE-TRIAL-{suffix}-01", f"BASE-TRIAL-{suffix}-02"],
        "run_count": 2,
        "status": "PASS",
        "owner": owners["evaluator"],
        "created_at": "2026-09-02T00:00:00Z",
    })
    dataset_ids = {layer: f"DATA-{suffix}-{layer.upper()}" for layer in ["training", "regression", "holdout", "representative_real_world"]}
    datasets = []
    expected_counts = {"training": 15, "regression": 7, "holdout": 9, "representative_real_world": 0}
    for layer in ["training", "regression", "holdout", "representative_real_world"]:
        source_digest = sha({"layer": layer, "suffix": suffix})
        parent_id = dataset_ids["training"] if layer == "regression" else dataset_ids["regression"] if layer == "holdout" else None
        datasets.append(seal({
            "dataset_id": dataset_ids[layer],
            "layer": layer,
            "subject": subject,
            "camp_id": camp_id,
            "version": "v1",
            "source_digest": source_digest,
            "parent_dataset_id": parent_id,
            "sealed": layer == "holdout",
            "exposed_to": [owners["evaluator"]] if layer == "holdout" else [owners["trainer"]],
            "claim_count": expected_counts[layer],
            "expected_task_count": expected_counts[layer],
            "expected_trial_count": expected_counts[layer],
            "grader_version": "grader-c07-v1",
            "lineage_digest": sha({"dataset_id": dataset_ids[layer], "layer": layer, "parent_dataset_id": parent_id, "version": "v1", "source_digest": source_digest}),
            "status": "NOT_RUN" if layer == "representative_real_world" else "ACTIVE",
            "owner": owners["data_owner"],
            "created_at": "2026-09-01T00:00:00Z",
        }))

    days = []
    task_registry = []
    trial_registry = []
    evidence = []
    for day in range(31):
        phase, gates = day_contract(day)
        day_id = f"DAY-{suffix}-{day:02d}"
        task_id = f"TASK-{suffix}-{day:02d}"
        trial_id = f"TRIAL-{suffix}-{day:02d}"
        record = evidence_record(suffix, subject, camp_id, owners, "DAY", f"DAY-{day:02d}", day_id=day_id, task_id=task_id, trial_id=trial_id)
        dataset_layer = "training" if day <= 14 else "regression" if day <= 21 else "holdout"
        day_record = {
            "day_id": day_id,
            "day_number": day,
            "phase": phase,
            "gates": gates,
            "subject": subject,
            "camp_id": camp_id,
            "task_id": task_id,
            "trial_id": trial_id,
            "evidence_ref": record["evidence_id"],
            "dataset_ref": dataset_ids[dataset_layer],
            "status": "RECORDED",
            "budget": 20.0,
            "human_minutes": 15.0,
            "authority_ref": authority["authority_id"],
            "runtime_ref": runtime["runtime_id"],
            "eval_ref": eval_spec["eval_id"],
            "baseline_ref": baseline["baseline_id"],
            "objective": f"compressed-contract-check-{day:02d}",
        }
        record["content_digest"] = sha({key: value for key, value in day_record.items() if key != "evidence_ref"})
        reseal(record)
        evidence.append(record)
        days.append(day_record)
        task_registry.append(seal({"task_id": task_id, "subject": subject, "camp_id": camp_id, "day_id": day_id, "dataset_ref": dataset_ids[dataset_layer], "eval_ref": eval_spec["eval_id"], "status": "PASS", "owner": owners["trainer"]}))
        trial_registry.append(seal({"trial_id": trial_id, "subject": subject, "camp_id": camp_id, "day_id": day_id, "task_id": task_id, "dataset_ref": dataset_ids[dataset_layer], "grader_version": eval_spec["grader_version"], "status": "PASS", "owner": owners["evaluator"]}))
    special_records = {
        "technical": evidence_record(suffix, subject, camp_id, owners, "D21_TECHNICAL", "D21-T"),
        "delivery": evidence_record(suffix, subject, camp_id, owners, "D21_DELIVERY", "D21-D"),
        "business_environment": evidence_record(suffix, subject, camp_id, owners, "D21_BUSINESS_ENVIRONMENT", "D21-B"),
        "holdout": evidence_record(suffix, subject, camp_id, owners, "HOLDOUT", "HOLD"),
    }
    evidence.extend(special_records.values())
    security_matrix = []
    gate_days = {0: "G0", 2: "G1", 7: "G2", 14: "G3", 21: "G4", 26: "G5", 30: "G6"}
    for day_number, gate in gate_days.items():
        day = days[day_number]
        for slice_name in ["prompt_injection", "authorization", "data_leakage", "supply_chain"]:
            record = evidence_record(suffix, subject, camp_id, owners, "SECURITY", f"SEC-{gate}-{slice_name.upper()}", day_id=day["day_id"], task_id=day["task_id"], trial_id=day["trial_id"])
            record["content_digest"] = sha({"slice": slice_name, "gate": gate, "day_id": day["day_id"], "task_id": day["task_id"], "trial_id": day["trial_id"], "result": "PASS"})
            reseal(record)
            evidence.append(record)
            security_matrix.append({"slice": slice_name, "gate": gate, "day_id": day["day_id"], "task_id": day["task_id"], "trial_id": day["trial_id"], "evidence_ref": record["evidence_id"]})
    stop_receipt = seal({
        "receipt_id": f"STOP-{suffix}",
        "subject": subject,
        "camp_id": camp_id,
        "task_id": days[-1]["task_id"],
        "trial_id": days[-1]["trial_id"],
        "status": "PASS",
        "issuer": owners["operations_owner"],
        "created_at": "2026-09-30T10:30:00Z",
    })
    stop_readback = seal({
        "subject": subject,
        "camp_id": camp_id,
        "task_id": days[-1]["task_id"],
        "trial_id": days[-1]["trial_id"],
        "receipt_ref": stop_receipt["receipt_id"],
        "admission": "PAUSED",
        "queue": "CLEAR",
        "workers": "STOPPED",
        "effects": "CLEAR",
        "observed_at": "2026-09-30T10:31:00Z",
        "observer": owners["evaluator"],
    })
    recovery_registry = [
        seal({"recovery_id": f"BACKUP-{suffix}", "kind": "BACKUP", "subject": subject, "camp_id": camp_id, "runtime_ref": runtime["runtime_id"], "content_digest": sha({"camp": camp_id, "backup": 30}), "status": "PASS", "owner": owners["operations_owner"], "created_at": "2026-09-30T10:40:00Z"}),
        seal({"recovery_id": f"CHECKPOINT-{suffix}", "kind": "CHECKPOINT", "subject": subject, "camp_id": camp_id, "runtime_ref": runtime["runtime_id"], "content_digest": sha({"camp": camp_id, "checkpoint": 30}), "status": "PASS", "owner": owners["operations_owner"], "created_at": "2026-09-30T10:45:00Z"}),
        seal({"recovery_id": f"RUNTIME-EVIDENCE-{suffix}", "kind": "RUNTIME", "subject": subject, "camp_id": camp_id, "runtime_ref": runtime["runtime_id"], "content_digest": runtime["digest"], "status": "PASS", "owner": owners["runtime_owner"], "created_at": "2026-09-30T10:50:00Z"}),
        seal({"recovery_id": f"REGRESSION-{suffix}", "kind": "REGRESSION", "subject": subject, "camp_id": camp_id, "runtime_ref": runtime["runtime_id"], "content_digest": sha({"camp": camp_id, "regression": "PASS"}), "status": "PASS", "owner": owners["evaluator"], "created_at": "2026-09-30T10:55:00Z"}),
    ]
    restore = seal({
        "proof_id": f"RESTORE-{suffix}",
        "subject": subject,
        "camp_id": camp_id,
        "backup_ref": f"BACKUP-{suffix}",
        "checkpoint_ref": f"CHECKPOINT-{suffix}",
        "runtime_evidence_ref": f"RUNTIME-EVIDENCE-{suffix}",
        "regression_ref": f"REGRESSION-{suffix}",
        "release_digest": runtime["digest"],
        "target_runtime_digest": runtime["digest"],
        "status": "PASS",
        "regression_status": "PASS",
        "owner": owners["operations_owner"],
        "created_at": "2026-09-30T11:00:00Z",
    })
    effect_ledger = [seal({"effect_id": f"EFFECT-{suffix}-01", "subject": subject, "camp_id": camp_id, "day_id": days[-1]["day_id"], "task_id": days[-1]["task_id"], "trial_id": days[-1]["trial_id"], "external": False, "status": "NOT_APPLIED", "receipt_ref": stop_receipt["receipt_id"], "evidence_ref": days[-1]["evidence_ref"], "owner": owners["operations_owner"], "created_at": "2026-09-30T10:29:00Z"})]
    graduation = seal({
        "record_id": f"GRAD-{suffix}",
        "subject": subject,
        "camp_id": camp_id,
        "recommendation": "LIMITED_DUTY",
        "status": "PROPOSED",
        "reviewer": owners["evaluator"],
        "evidence_refs": [item["evidence_id"] for item in evidence],
        "issued_at": "2026-09-30T11:30:00Z",
        "expires_at": "2026-10-30T11:30:00Z",
        "revoked_at": None,
        "certification": False,
    })
    before = {"prompt_version": "p1", "context_version": "c1", "memory_policy": "m1", "skill_version": "s1", "tool_contract": "t1", "workflow_version": "w1", "runtime_choice": "r1", "policy_version": "g1"}
    after = dict(before)
    after["prompt_version"] = "p2"
    cost_ledger = []
    for category, amount in [("model", 100.0), ("tool", 50.0), ("compute", 100.0), ("human", 300.0), ("failure", 50.0), ("remediation", 50.0)]:
        cost_id = f"COST-{suffix}-{category.upper()}"
        cost_record = evidence_record(suffix, subject, camp_id, owners, "COST", category.upper(), day_id=days[-1]["day_id"], task_id=days[-1]["task_id"], trial_id=days[-1]["trial_id"])
        entry = {"cost_id": cost_id, "category": category, "amount": amount, "currency": "COST_UNIT", "subject": subject, "camp_id": camp_id, "day_id": days[-1]["day_id"], "task_id": days[-1]["task_id"], "trial_id": days[-1]["trial_id"], "evidence_ref": cost_record["evidence_id"]}
        cost_record["content_digest"] = sha(entry)
        reseal(cost_record)
        evidence.append(cost_record)
        cost_ledger.append(entry)
    graduation["evidence_refs"] = [item["evidence_id"] for item in evidence]
    reseal(graduation)
    state = {
        "camp": camp,
        "principals": people,
        "owners": owners,
        "authority": authority,
        "runtime": runtime,
        "eval_spec": eval_spec,
        "baseline": baseline,
        "datasets": datasets,
        "calendar": {
            "labels": list(range(31)),
            "training_days": list(range(1, 31)),
            "phases": [{"phase": "P1", "start_day": 0, "end_day": 7}, {"phase": "P2", "start_day": 8, "end_day": 14}, {"phase": "P3", "start_day": 15, "end_day": 21}, {"phase": "P4", "start_day": 22, "end_day": 26}, {"phase": "P5", "start_day": 27, "end_day": 30}],
            "gates": [f"G{i}" for i in range(7)],
            "day_map": [{"day_number": day, "phase": day_contract(day)[0], "gates": day_contract(day)[1]} for day in range(31)],
        },
        "days": days,
        "task_registry": task_registry,
        "trial_registry": trial_registry,
        "intervention": {"before": before, "after": after},
        "cost_ledger": cost_ledger,
        "evidence_registry": evidence,
        "security_evidence_refs": [item["evidence_ref"] for item in security_matrix],
        "security_matrix": security_matrix,
        "d21_refs": {key: special_records[key]["evidence_id"] for key in ["technical", "delivery", "business_environment"]},
        "stop_receipt": stop_receipt,
        "stop_readback": stop_readback,
        "restore_proof": restore,
        "recovery_registry": recovery_registry,
        "effect_ledger": effect_ledger,
        "graduation_record": graduation,
    }
    return state


def reseal(record: dict[str, Any]) -> None:
    record["digest"] = sha({key: item for key, item in record.items() if key != "digest"})


def apply_variant(index: int, state: dict[str, Any]) -> None:
    if index == 2:
        state["authority"]["expires_at"] = "2026-09-29T00:00:00Z"
        state["authority"]["status"] = "REVOKED"
        reseal(state["authority"])
    elif index == 3:
        holdout = next(item for item in state["datasets"] if item["layer"] == "holdout")
        holdout["exposed_to"].append(state["camp"]["subject"])
        reseal(holdout)
    elif index == 4:
        state["runtime"]["permissions"].append("production_send")
        reseal(state["runtime"])
    elif index == 5:
        state["stop_receipt"]["status"] = "UNKNOWN"
        reseal(state["stop_receipt"])
    elif index == 6:
        state["evidence_registry"][10]["status"] = "UNKNOWN"
        reseal(state["evidence_registry"][10])
    elif index == 7:
        ref = state["security_evidence_refs"][0]
        record = next(item for item in state["evidence_registry"] if item["evidence_id"] == ref)
        record["status"] = "FAIL"
        reseal(record)
    elif index == 8:
        state["baseline"]["status"] = "FAIL"
        reseal(state["baseline"])
    elif index == 9:
        ref = state["d21_refs"]["delivery"]
        record = next(item for item in state["evidence_registry"] if item["evidence_id"] == ref)
        record["status"] = "UNKNOWN"
        reseal(record)
    elif index == 10:
        state["cost_ledger"][0]["amount"] = 900.0
    elif index == 11:
        state["days"][18]["status"] = "UNKNOWN"
        ref = state["days"][18]["evidence_ref"]
        record = next(item for item in state["evidence_registry"] if item["evidence_id"] == ref)
        record["status"] = "UNKNOWN"
        day = state["days"][18]
        record["content_digest"] = sha({key: value for key, value in day.items() if key != "evidence_ref"})
        reseal(record)
    elif index == 12:
        state["restore_proof"]["status"] = "FAIL"
        reseal(state["restore_proof"])
    elif index == 13:
        real = next(item for item in state["datasets"] if item["layer"] == "representative_real_world")
        real["status"] = "PASS"
        real["claim_count"] = 1
        reseal(real)
    elif index == 14:
        state["graduation_record"]["reviewer"] = state["owners"]["trainer"]
        reseal(state["graduation_record"])
    elif index == 15:
        state["authority"]["revoked_at"] = "2026-09-29T00:00:00Z"
        state["authority"]["status"] = "REVOKED"
        reseal(state["authority"])
    elif index == 16:
        state["intervention"]["after"]["context_version"] = "c2"
    elif index == 17:
        state["runtime"]["release"] = "latest"
        reseal(state["runtime"])
    elif index == 18:
        state["stop_readback"]["workers"] = "UNKNOWN"
        reseal(state["stop_readback"])


def frozen_entry(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "camp_id": state["camp"]["camp_id"],
        "subject": state["camp"]["subject"],
        "principals_digest": sha(state["principals"]),
        "owners_digest": sha(state["owners"]),
        "camp_digest": state["camp"]["digest"],
        "authority_digest": state["authority"]["digest"],
        "runtime_digest": state["runtime"]["digest"],
        "eval_digest": state["eval_spec"]["digest"],
        "baseline_digest": state["baseline"]["digest"],
        "datasets_digest": sha(state["datasets"]),
        "approved_budget": state["camp"]["budget_total"],
        "approved_currency": state["camp"]["currency"],
        "approved_scope": state["authority"]["scope"],
        "authority_issuer": state["owners"]["security_owner"],
        "day_issuer": state["owners"]["trainer"],
        "evaluation_issuer": state["owners"]["evaluator"],
        "security_issuer": state["owners"]["security_owner"],
        "stop_issuer": state["owners"]["operations_owner"],
        "stop_observer": state["owners"]["evaluator"],
        "graduation_reviewer": state["owners"]["evaluator"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(HERE / "synthetic-camp-input.yaml"))
    parser.add_argument("--authority-output", default=str(HERE / "frozen-camp-authority.yaml"))
    args = parser.parse_args()
    layers = ["training"] * 6 + ["regression"] * 6 + ["holdout"] * 8
    trials = []
    frozen_entries = {}
    for index, layer in enumerate(layers, 1):
        state = build_state(index)
        frozen_entries[state["camp"]["camp_id"]] = frozen_entry(state)
        apply_variant(index, state)
        if index in {5, 6, 9, 10, 11, 18}:
            state["graduation_record"]["recommendation"] = "EXTEND"
        elif index not in {1, 19, 20}:
            state["graduation_record"]["recommendation"] = "STOP"
        reseal(state["graduation_record"])
        trials.append({
            "scenario_id": f"S{index:02d}",
            "raw_state": state,
        })
    authority_bundle = {
        "schema_version": "c22.camp.authority.v2.2",
        "bundle_id": "C22-CAMP-AUTHORITY-20261001-v2.2",
        "issued_at": "2026-09-01T00:00:00Z",
        "issuer": "c22-independent-governance-root",
        "policy": {
            "allowed_action": "run_compressed_training_camp",
            "required_scope": ["offline_synthetic", "read_synthetic", "write_synthetic_artifact"],
            "sandbox_modes": ["isolated"],
            "sandbox_scopes": ["trial"],
            "sandbox_backends": ["offline-fixture"],
            "runtime_platform": "openclaw",
            "runtime_release": "v2026.9.6",
            "runtime_commit": "eb377ac",
            "cost_categories": ["compute", "failure", "human", "model", "remediation", "tool"],
            "security_slices": ["authorization", "data_leakage", "prompt_injection", "supply_chain"],
            "gates": [f"G{i}" for i in range(7)],
        },
        "camps": frozen_entries,
    }
    authority_bundle["root_digest"] = sha(authority_bundle)
    document = {
        "schema_version": "c22.camp.raw.v2.2",
        "generated_at": GENERATED_AT,
        "environment": {"mode": "offline_synthetic", "network": False, "real_credentials": False, "production_write": False, "external_effects_allowed": False, "compressed_simulation": True},
        "authority_ref": {"bundle_id": authority_bundle["bundle_id"], "root_digest": authority_bundle["root_digest"]},
        "trials": trials,
    }
    Path(args.output).write_text(json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    Path(args.authority_output).write_text(json.dumps(authority_bundle, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(authority_bundle["root_digest"])


if __name__ == "__main__":
    main()

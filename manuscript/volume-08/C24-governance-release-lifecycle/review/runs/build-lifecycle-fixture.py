#!/usr/bin/env python3
"""Build the deterministic C21 v2.4 lifecycle fixture and negative regressions."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "synthetic-lifecycle-input.yaml"
AUTHORITY_OUTPUT = HERE / "frozen-authority-root.yaml"


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


def seal(record: dict, field: str) -> dict:
    result = copy.deepcopy(record)
    result[field] = digest({key: value for key, value in result.items() if key != field})
    return result


def owner(principal: str, kind: str = "human", status: str = "ACTIVE") -> dict:
    return {"principal": principal, "kind": kind, "status": status, "valid_from": "2026-09-01T00:00:00Z", "expires_at": "2026-12-31T00:00:00Z"}


def authority(authority_id: str, actor: str, action: str, subject_type: str, subject_id: str, object_digest: str, scope: str) -> dict:
    return seal({"authority_id": authority_id, "actor": actor, "action": action, "subject_type": subject_type, "subject_id": subject_id, "object_digest": object_digest, "scope": scope, "status": "ACTIVE", "not_before": "2026-09-30T00:00:00Z", "expires_at": "2026-10-01T00:00:00Z", "issued_at": "2026-09-30T01:00:00Z", "policy_version": "policy-c21-v2", "authority_digest": ""}, "authority_digest")


def retirement_evidence(evidence_id: str, kind: str, subject: str, release_id: str, release_digest: str, owner_id: str, content: str, status: str = "PASS", issued_at: str = "2026-09-30T11:40:00Z") -> dict:
    return seal({"evidence_id": evidence_id, "kind": kind, "subject_id": subject, "object_id": release_id, "object_version": release_digest, "status": status, "owner": owner_id, "issued_at": issued_at, "expires_at": "2026-10-01T00:00:00Z", "content_digest": content, "record_digest": ""}, "record_digest")


def scenario(index: int, overrides: dict, *, layer: str = "holdout", case: str = "CASE-C", security: list[str] | None = None) -> dict:
    sid = f"V24-{index:03d}"
    return {"scenario_id": sid, "task_id": f"C21-TASK-{index:03d}", "task_type": "research", "trial_id": f"C21-TRIAL-{index:03d}", "layer": layer, "holdout_ref": "holdout-research-21" if layer == "holdout" else "NONE", "case_id": case, "security_slices": security or [], "overrides": overrides}


def rollout_plan(plan_id: str, release_id: str, stage: str, approval_ref: str) -> dict:
    scope = "synthetic-canary" if stage == "CANARY" else "synthetic-retirement"
    environment_ref = "env-runtime-offline-21"
    return seal({
        "plan_id": plan_id, "release_id": release_id, "stage": stage, "scope": scope,
        "scope_digest": digest({"scope": scope, "allowed_tenants": ["tenant-synthetic"], "allowed_tasks": ["research"], "allowed_actions": ["read", "write_isolated_artifact"]}),
        "allowed_tenants": ["tenant-synthetic"], "allowed_tasks": ["research"], "allowed_actions": ["read", "write_isolated_artifact"],
        "candidate_permissions": ["read", "write_isolated_artifact"], "baseline_permissions": ["read", "write_isolated_artifact"],
        "min_trials": 2, "max_trials": 3, "max_cost": 10.0, "starts_at": "2026-09-30T11:00:00Z", "expires_at": "2026-09-30T13:00:00Z",
        "environment_ref": environment_ref, "owner": "human-operations", "approval_ref": approval_ref, "plan_digest": "",
    }, "plan_digest")


def rollout_from_plan(plan: dict) -> dict:
    result = {key: copy.deepcopy(value) for key, value in plan.items() if key != "approval_ref"}
    result.update({"quality_gate": "PASS", "security_gate": "PASS", "error_budget_gate": "PASS", "stop_triggered": False, "stop_receipt_ref": "NONE"})
    return result


def task_record(task_id: str, action: str) -> dict:
    return seal({"task_id": task_id, "subject_id": "agent-case-c", "tenant_id": "tenant-synthetic", "task_type": "research", "action": action, "owner": "human-operations", "status": "COMPLETE", "input_digest": digest({"task": task_id, "action": action}), "record_digest": ""}, "record_digest")


def dataset_record(dataset_id: str, release_id: str, layer: str) -> dict:
    return seal({"dataset_id": dataset_id, "release_id": release_id, "layer": layer, "holdout_ref": "holdout-research-21" if layer == "holdout" else "NONE", "lineage_digest": digest({"dataset": dataset_id, "layer": layer}), "status": "NOT_RUN" if layer == "representative_real_world" else "ACTIVE", "owner": "human-capability", "record_digest": ""}, "record_digest")


def terminal_record(terminal_id: str, trial_id: str, status: str = "COMPLETED") -> dict:
    return seal({"terminal_id": terminal_id, "trial_id": trial_id, "status": status, "result_digest": digest({"trial": trial_id, "status": status}), "owner": "human-operations", "observed_at": "2026-09-30T11:54:00Z", "record_digest": ""}, "record_digest")


def trial_record(trial_id: str, task: dict, release_id: str, dataset: dict, terminal: dict, action: str, cost: float) -> dict:
    return seal({"trial_id": trial_id, "task_id": task["task_id"], "release_id": release_id, "subject_id": task["subject_id"], "tenant_id": task["tenant_id"], "task_type": task["task_type"], "action": action, "dataset_ref": dataset["dataset_id"], "layer": dataset["layer"], "holdout_ref": dataset["holdout_ref"], "input_digest": task["input_digest"], "grader_ref": "blind-grader-c07", "terminal_ref": terminal["terminal_id"], "cost": cost, "quality_gate": "PASS", "security_gate": "PASS", "error_budget_gate": "PASS", "trial_digest": ""}, "trial_digest")


def automation_manifest(manifest_id: str, kind: str, object_id: str, action: str) -> dict:
    return seal({"manifest_id": manifest_id, "kind": kind, "object_id": object_id, "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": action, "status": "APPROVED", "record_digest": ""}, "record_digest")


def event_receipt(receipt_id: str, event_id: str, event_type: str, release_id: str, plan_id: str, subject_id: str, actor: str, authority_ref: str, executed_at: str) -> dict:
    return seal({"receipt_id": receipt_id, "event_id": event_id, "event_type": event_type, "release_id": release_id, "plan_id": plan_id, "subject_id": subject_id, "actor": actor, "authority_ref": authority_ref, "status": "VERIFIED", "executed_at": executed_at, "record_digest": ""}, "record_digest")


def event_readback(readback_id: str, event_id: str, receipt_ref: str, event_type: str, release_id: str, plan_id: str, subject_id: str, observer: str, observed_at: str) -> dict:
    return seal({"readback_id": readback_id, "event_id": event_id, "receipt_ref": receipt_ref, "event_type": event_type, "release_id": release_id, "plan_id": plan_id, "subject_id": subject_id, "observer": observer, "status": "VERIFIED", "observed_at": observed_at, "record_digest": ""}, "record_digest")


def main() -> None:
    release_id = "rel-21-v2"
    canary_plan = rollout_plan("rollout-c21-v24", release_id, "CANARY", "approval-canary-plan-21")
    retired_plan = rollout_plan("rollout-c21-retired-v24", release_id, "RETIRED", "approval-retired-plan-21")
    legal_review = {"status": "PASS", "reviewer": "human-risk", "legal_scope_ref": "legal-synthetic-local-21", "data_use": "APPROVED", "license": "APPROVED", "privacy": "APPROVED", "reviewed_at": "2026-09-30T02:00:00Z", "expires_at": "2026-10-01T00:00:00Z"}
    release = seal({
        "release_id": release_id, "agent_id": "agent-case-c", "build_ref": "openclaw@eb377ac",
        "build_digest": digest("build-v2"), "contract_digest": digest("contract-v2"), "policy_digest": digest("policy-v2"),
        "policy_version": "policy-c21-v2", "model_ref": "provider/model@snapshot-202609", "model_params_digest": digest("model-params-v2"),
        "tool_manifest_digest": digest("tools-v2"), "skill_manifest_digest": digest("skills-v2"), "memory_schema": "memory-v2",
        "state_schema": "state-v2", "dependency_lock_digest": digest("deps-v2"), "sbom_ref": "sbom-c21-v2",
        "observability_schema_ref": "obs-c20-provisional", "eval_baseline_ref": "eval-c07-v1", "security_review_ref": "security-c19-provisional",
        "backup_restore_proof_ref": "restore-proof-21", "rollout_plan_ref": canary_plan["plan_id"], "change_class": "compatibility-sensitive",
        "proposer": "human-capability", "approver": "human-risk", "operator": "human-operations", "acceptor": "human-business",
        "approval_ref": "approval-release-21", "publication_event_ref": "publication-release-21", "release_digest": ""
    }, "release_digest")
    migration = seal({"migration_id": "migration-21", "release_id": release["release_id"], "from_schema": "state-v1", "to_schema": "state-v2", "candidate_reads_from": True, "candidate_writes_to": True, "old_runtime_reads_to": False, "dry_run": "PASS", "status": "VERIFIED", "receipt_ref": "migration-receipt-21", "reentrant": True, "irreversible_steps": [], "irreversible_approval_ref": "NONE", "recovery_strategy": "ROLLBACK", "owner": "human-technical", "migration_digest": ""}, "migration_digest")
    migration_receipt = seal({"receipt_id": "migration-receipt-21", "subject_type": "migration", "subject_id": migration["migration_id"], "release_id": release["release_id"], "from_schema": migration["from_schema"], "to_schema": migration["to_schema"], "status": "VERIFIED", "owner": migration["owner"], "issued_at": "2026-09-30T11:50:00Z", "expires_at": "2026-10-01T00:00:00Z", "migration_digest": migration["migration_digest"], "record_digest": ""}, "record_digest")
    backup_manifest = seal({"manifest_id": "backup-manifest-21", "backup_id": "backup-21", "release_id": release["release_id"], "covered": ["global_db", "agent_db", "agent_dir", "contracts", "memory", "skills", "plugins", "audit"], "excluded": ["cache", "runtime_downloads"], "consistent_snapshot": True, "archive_digest": digest("backup-archive-21"), "integrity": "PASS", "encrypted": True, "access_owner": "human-data", "created_at": "2026-09-30T01:00:00Z", "expires_at": "2026-10-01T00:00:00Z", "manifest_digest": ""}, "manifest_digest")
    restore_proof = seal({"proof_id": "restore-proof-21", "restore_id": "restore-21", "backup_id": "backup-21", "release_id": release["release_id"], "archive_digest": backup_manifest["archive_digest"], "environment_ref": "env-restore-isolated-21", "hash_verified": True, "schema_integrity": "PASS", "identity_tenant_check": "PASS", "credentials_rebuilt": True, "task_replay": "PASS", "delivery_check": "PASS", "environment_terminal": "PASS", "rpo_minutes": 5, "rto_minutes": 30, "owner": "human-technical", "issued_at": "2026-09-30T11:00:00Z", "expires_at": "2026-10-01T00:00:00Z", "proof_digest": ""}, "proof_digest")

    d21 = {"task_id": "task-synthetic", "release_id": release["release_id"], "object_id": "artifact-c21", "object_version": "artifact-v2"}
    d21_registry = {}
    face_owner = {"technical": "human-technical", "delivery": "human-operations", "business": "human-business", "environment": "human-risk"}
    for face in ("technical", "delivery", "business", "environment"):
        evidence_id = f"d21-{face}-21"
        d21[face] = {"status": "PASS", "evidence_ref": evidence_id}
        d21_registry[evidence_id] = seal({"evidence_id": evidence_id, "face": face, "task_id": d21["task_id"], "release_id": release["release_id"], "object_id": d21["object_id"], "object_version": d21["object_version"], "object_digest": release["release_digest"], "status": "PASS", "source": f"independent-{face}-observer", "owner": face_owner[face], "observed_at": "2026-09-30T11:55:00Z", "expires_at": "2026-10-01T00:00:00Z", "record_digest": ""}, "record_digest")

    stop_receipt = seal({"receipt_id": "stop-receipt-21", "release_id": release["release_id"], "plan_id": canary_plan["plan_id"], "reason_codes": ["OPERATOR_PAUSE"], "status": "VERIFIED", "owner": "human-operations", "issued_at": "2026-09-30T11:59:00Z", "expires_at": "2026-09-30T12:05:00Z", "admission": "PAUSED", "queue": "CLEAR", "workers": "STOPPED", "active_release": release["release_id"], "record_digest": ""}, "record_digest")
    rollback_receipt = seal({"receipt_id": "rollback-receipt-21", "release_id": release["release_id"], "target_release": "rel-21-v1", "owner": "human-operations", "status": "VERIFIED", "active_release": "rel-21-v1", "code_config_reverted": True, "old_runtime_reads_current_schema": True, "external_effects_reconciled": True, "compensation_status": "NOT_REQUIRED", "admission": "PAUSED", "queue": "CLEAR", "workers": "STOPPED", "issued_at": "2026-09-30T11:59:00Z", "expires_at": "2026-09-30T12:05:00Z", "record_digest": ""}, "record_digest")

    retirement_refs = {"admission": "ret-admission-21", "inflight": "ret-inflight-21", "runtime": "ret-runtime-21", "network": "ret-network-21", "replacement": "ret-replacement-21", "handoff": "ret-handoff-21", "residual": "ret-residual-21", "signoff": "ret-signoff-21"}
    retirement_complete = seal({"retirement_id": "retirement-21", "release_id": release["release_id"], "requested": True, "owner": "human-business", "decision_ref": "approval-retirement-21", "lifecycle_event_ref": "retirement-lifecycle-21", "critical_service": True, "replacement_ref": "replacement-agent", "handoff_ref": "handoff-21", "evidence_refs": retirement_refs, "decision_digest": ""}, "decision_digest")
    retirement_registry = {
        retirement_refs["admission"]: retirement_evidence(retirement_refs["admission"], "admission_stopped", retirement_complete["retirement_id"], release["release_id"], release["release_digest"], "human-operations", digest("admission stopped"), issued_at="2026-09-30T11:32:00Z"),
        retirement_refs["inflight"]: retirement_evidence(retirement_refs["inflight"], "inflight_reconciled", retirement_complete["retirement_id"], release["release_id"], release["release_digest"], "human-operations", digest("inflight reconciled"), issued_at="2026-09-30T11:34:00Z"),
        retirement_refs["runtime"]: retirement_evidence(retirement_refs["runtime"], "runtime_disabled", retirement_complete["retirement_id"], release["release_id"], release["release_digest"], "human-technical", digest("runtime disabled"), issued_at="2026-09-30T11:36:00Z"),
        retirement_refs["network"]: retirement_evidence(retirement_refs["network"], "network_disabled", retirement_complete["retirement_id"], release["release_id"], release["release_digest"], "human-technical", digest("network disabled"), issued_at="2026-09-30T11:38:00Z"),
        retirement_refs["replacement"]: retirement_evidence(retirement_refs["replacement"], "replacement_accepted", retirement_complete["retirement_id"], release["release_id"], release["release_digest"], "human-business", digest("replacement accepted"), issued_at="2026-09-30T11:44:00Z"),
        retirement_refs["handoff"]: retirement_evidence(retirement_refs["handoff"], "handoff_accepted", retirement_complete["retirement_id"], release["release_id"], release["release_digest"], "human-capability", digest("handoff accepted"), issued_at="2026-09-30T11:46:00Z"),
        retirement_refs["residual"]: retirement_evidence(retirement_refs["residual"], "residual_scan", retirement_complete["retirement_id"], release["release_id"], release["release_digest"], "human-risk", digest("residual clean"), issued_at="2026-09-30T11:56:00Z"),
        retirement_refs["signoff"]: retirement_evidence(retirement_refs["signoff"], "terminal_signoff", retirement_complete["retirement_id"], release["release_id"], release["release_digest"], "human-business", retirement_complete["decision_digest"], issued_at="2026-09-30T11:58:00Z"),
        "cred-revoked-21": retirement_evidence("cred-revoked-21", "credential_revoked", "cred-active", release["release_id"], release["release_digest"], "human-risk", digest("credential revoked"), issued_at="2026-09-30T11:40:00Z"),
        "restore-disabled-21": retirement_evidence("restore-disabled-21", "restore_disabled", "cred-active", release["release_id"], release["release_digest"], "human-risk", digest("restore disabled"), issued_at="2026-09-30T11:41:00Z"),
        "session-revoked-21": retirement_evidence("session-revoked-21", "session_revoked", "session-old", release["release_id"], release["release_digest"], "human-risk", digest("session revoked"), issued_at="2026-09-30T11:42:00Z"),
        "delegation-revoked-21": retirement_evidence("delegation-revoked-21", "delegation_revoked", "delegation-old", release["release_id"], release["release_digest"], "human-risk", digest("delegation revoked"), issued_at="2026-09-30T11:43:00Z"),
        "data-disposed-21": retirement_evidence("data-disposed-21", "data_disposed", "data-synthetic", release["release_id"], release["release_digest"], "human-data", digest("data disposed"), issued_at="2026-09-30T11:48:00Z"),
    }
    owners = {"business": owner("human-business"), "technical": owner("human-technical"), "data": owner("human-data"), "capability": owner("human-capability"), "security_risk": owner("human-risk"), "operations": owner("human-operations")}
    environment_registry = {
        "env-restore-isolated-21": seal({"environment_id": "env-restore-isolated-21", "kind": "isolated_restore", "mode": "offline_synthetic", "region": "synthetic-local", "scope": "synthetic-restore", "status": "ACTIVE", "owner": "human-technical", "issued_at": "2026-09-30T01:00:00Z", "expires_at": "2026-10-01T00:00:00Z", "record_digest": ""}, "record_digest"),
        "env-runtime-offline-21": seal({"environment_id": "env-runtime-offline-21", "kind": "offline_runtime", "mode": "offline_synthetic", "region": "synthetic-local", "scope": "synthetic-canary", "status": "ACTIVE", "owner": "human-operations", "issued_at": "2026-09-30T01:00:00Z", "expires_at": "2026-10-01T00:00:00Z", "record_digest": ""}, "record_digest"),
    }
    legal_scope_registry = {
        "legal-synthetic-local-21": seal({"legal_scope_id": "legal-synthetic-local-21", "region": "synthetic-local", "scope": "synthetic-only", "allowed_environment_refs": ["env-restore-isolated-21", "env-runtime-offline-21"], "status": "ACTIVE", "owner": "human-risk", "issued_at": "2026-09-30T01:00:00Z", "expires_at": "2026-10-01T00:00:00Z", "record_digest": ""}, "record_digest")
    }
    holdout_registry = {
        "holdout-research-21": seal({"holdout_id": "holdout-research-21", "task_type": "research", "release_id": release["release_id"], "lineage_digest": digest("holdout-lineage-21"), "isolation_manifest_digest": digest("holdout-isolation-21"), "grader_ref": "blind-grader-c07", "gold_exposed": False, "contamination_status": "CLEAN", "status": "ACTIVE", "owner": "human-capability", "issued_at": "2026-09-30T01:00:00Z", "expires_at": "2026-10-01T00:00:00Z", "record_digest": ""}, "record_digest")
    }
    datasets = {
        item["dataset_id"]: item for item in (
            dataset_record("dataset-training-21", release["release_id"], "training"),
            dataset_record("dataset-regression-21", release["release_id"], "regression"),
            dataset_record("dataset-holdout-21", release["release_id"], "holdout"),
            dataset_record("dataset-real-21", release["release_id"], "representative_real_world"),
        )
    }
    task_read = task_record("task-release-read-21", "read")
    task_write = task_record("task-release-write-21", "write_isolated_artifact")
    terminal_one = terminal_record("terminal-canary-1", "canary-1")
    terminal_two = terminal_record("terminal-canary-2", "canary-2")
    trial_one = trial_record("canary-1", task_read, release["release_id"], datasets["dataset-holdout-21"], terminal_one, "read", 2.0)
    trial_two = trial_record("canary-2", task_write, release["release_id"], datasets["dataset-holdout-21"], terminal_two, "write_isolated_artifact", 2.5)
    task_registry = {task_read["task_id"]: task_read, task_write["task_id"]: task_write}
    trial_registry = {trial_one["trial_id"]: trial_one, trial_two["trial_id"]: trial_two}
    terminal_registry = {terminal_one["terminal_id"]: terminal_one, terminal_two["terminal_id"]: terminal_two}
    grader_registry = {"blind-grader-c07": seal({"grader_id": "blind-grader-c07", "version": "grader-c07-v1", "rubric_digest": digest("grader-c07-rubric"), "status": "ACTIVE", "owner": "human-capability", "record_digest": ""}, "record_digest")}
    automation_registry = {
        "manifest-task-synthetic": automation_manifest("manifest-task-synthetic", "task", "task-synthetic", "read"),
        "manifest-cron-synthetic": automation_manifest("manifest-cron-synthetic", "schedule", "cron-synthetic", "read"),
        "manifest-hook-synthetic": automation_manifest("manifest-hook-synthetic", "webhook", "hook-synthetic", "read"),
    }
    effect_request_digest = digest({"effect_id": "effect-unknown", "external": True, "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read"})
    effect_receipt = seal({"receipt_id": "effect-receipt-unknown", "effect_id": "effect-unknown", "authority_ref": "effect-authority-unknown", "request_digest": effect_request_digest, "status": "UNKNOWN", "owner": "human-operations", "issued_at": "2026-09-30T11:56:00Z", "record_digest": ""}, "record_digest")
    effect_readback = seal({"readback_id": "effect-readback-unknown", "effect_id": "effect-unknown", "receipt_ref": effect_receipt["receipt_id"], "status": "UNKNOWN", "observer": "human-risk", "observed_at": "2026-09-30T11:57:00Z", "record_digest": ""}, "record_digest")
    publication_receipt = event_receipt("publication-receipt-21", "publication-release-21", "PUBLICATION", release["release_id"], canary_plan["plan_id"], release["release_id"], release["operator"], release["approval_ref"], "2026-09-30T11:20:00Z")
    publication_readback = event_readback("publication-readback-21", "publication-release-21", publication_receipt["receipt_id"], "PUBLICATION", release["release_id"], canary_plan["plan_id"], release["release_id"], release["acceptor"], "2026-09-30T11:21:00Z")
    publication_event = seal({
        "event_id": "publication-release-21", "event_type": "PUBLICATION", "release_id": release["release_id"], "plan_id": canary_plan["plan_id"],
        "requested_by": release["proposer"], "requested_at": "2026-09-30T01:30:00Z", "legal_review_digest": digest(legal_review),
        "release_approved_by": release["approver"], "release_approved_at": "2026-09-30T02:10:00Z", "release_authority_ref": release["approval_ref"],
        "plan_approved_by": canary_plan["owner"], "plan_approved_at": "2026-09-30T02:15:00Z", "plan_authority_ref": canary_plan["approval_ref"],
        "executed_by": release["operator"], "executed_at": publication_receipt["executed_at"], "receipt": publication_receipt, "readback": publication_readback,
        "status": "VERIFIED", "record_digest": "",
    }, "record_digest")
    retirement_receipt = event_receipt("retirement-receipt-21", "retirement-lifecycle-21", "RETIREMENT", release["release_id"], retired_plan["plan_id"], retirement_complete["retirement_id"], retired_plan["owner"], retirement_complete["decision_ref"], "2026-09-30T11:30:00Z")
    retirement_readback = event_readback("retirement-readback-21", "retirement-lifecycle-21", retirement_receipt["receipt_id"], "RETIREMENT", release["release_id"], retired_plan["plan_id"], retirement_complete["retirement_id"], "human-risk", "2026-09-30T11:31:00Z")
    lifecycle_event = seal({
        "event_id": "retirement-lifecycle-21", "event_type": "RETIREMENT", "retirement_id": retirement_complete["retirement_id"], "release_id": release["release_id"], "plan_id": retired_plan["plan_id"],
        "requested_by": retirement_complete["owner"], "requested_at": "2026-09-30T11:22:00Z",
        "plan_approved_by": retired_plan["owner"], "plan_approved_at": "2026-09-30T11:24:00Z", "plan_authority_ref": retired_plan["approval_ref"],
        "retirement_approved_by": "human-risk", "retirement_approved_at": "2026-09-30T11:26:00Z", "retirement_authority_ref": retirement_complete["decision_ref"],
        "executed_by": retired_plan["owner"], "executed_at": retirement_receipt["executed_at"], "receipt": retirement_receipt, "readback": retirement_readback,
        "residual_evidence_ref": retirement_refs["residual"], "signoff_evidence_ref": retirement_refs["signoff"], "status": "VERIFIED", "record_digest": "",
    }, "record_digest")
    base_state = {
        "owner_registry": owners,
        "authority_registry": {
            "approval-release-21": authority("approval-release-21", "human-risk", "approve_release", "release", release["release_id"], release["release_digest"], canary_plan["plan_digest"]),
            "approval-canary-plan-21": authority("approval-canary-plan-21", "human-operations", "approve_rollout_plan", "rollout", canary_plan["plan_id"], canary_plan["plan_digest"], canary_plan["scope_digest"]),
            "approval-retired-plan-21": authority("approval-retired-plan-21", "human-operations", "approve_rollout_plan", "rollout", retired_plan["plan_id"], retired_plan["plan_digest"], retired_plan["scope_digest"]),
            "effect-authority-unknown": authority("effect-authority-unknown", "human-operations", "apply_effect", "effect", "effect-unknown", effect_request_digest, canary_plan["scope_digest"]),
            "approval-retirement-21": authority("approval-retirement-21", "human-risk", "approve_retirement", "retirement", retirement_complete["retirement_id"], retirement_complete["decision_digest"], retired_plan["plan_digest"]),
        },
        "release_unit": release,
        "migration": migration,
        "migration_receipt_registry": {migration_receipt["receipt_id"]: migration_receipt},
        "backup": {"backup_id": "backup-21", "release_id": release["release_id"], "manifest_ref": backup_manifest["manifest_id"], "owner": "human-data"},
        "backup_manifest_registry": {backup_manifest["manifest_id"]: backup_manifest},
        "restore": {"restore_id": "restore-21", "release_id": release["release_id"], "backup_id": "backup-21", "proof_ref": restore_proof["proof_id"], "owner": "human-technical", "target_rpo_minutes": 15, "target_rto_minutes": 60},
        "restore_proof_registry": {restore_proof["proof_id"]: restore_proof},
        "rollout": rollout_from_plan(canary_plan),
        "rollout_plan_registry": {canary_plan["plan_id"]: canary_plan, retired_plan["plan_id"]: retired_plan},
        "trial_ledger": [trial_one, trial_two],
        "task_registry": task_registry,
        "trial_registry": trial_registry,
        "dataset_registry": datasets,
        "grader_registry": grader_registry,
        "terminal_registry": terminal_registry,
        "stop_receipt_registry": {stop_receipt["receipt_id"]: stop_receipt},
        "d21": d21,
        "d21_evidence_registry": d21_registry,
        "runtime_state": {"active_release": release["release_id"], "admission": "OPEN_CANARY", "tasks": [{"task_id": "task-synthetic", "state": "COMPLETED", "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read", "manifest_ref": "manifest-task-synthetic"}], "schedules": [{"schedule_id": "cron-synthetic", "state": "PAUSED", "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read", "manifest_ref": "manifest-cron-synthetic"}], "webhooks": [{"webhook_id": "hook-synthetic", "state": "PAUSED", "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read", "manifest_ref": "manifest-hook-synthetic"}], "queue": "CLEAR", "workers": "STOPPED", "effect_ledger": []},
        "effect_receipt_registry": {effect_receipt["receipt_id"]: effect_receipt},
        "effect_readback_registry": {effect_readback["readback_id"]: effect_readback},
        "publication_event_registry": {publication_event["event_id"]: publication_event},
        "lifecycle_event_registry": {lifecycle_event["event_id"]: lifecycle_event},
        "automation_manifest_registry": automation_registry,
        "security_control_registry": {},
        "scenario_evidence_registry": {},
        "rollback": {"requested": False, "status": "NOT_REQUIRED", "target_release": "rel-21-v1", "old_runtime_reads_current_schema": False, "code_config_reverted": False, "external_effects_reconciled": True, "compensation_status": "NOT_REQUIRED", "receipt_ref": "NONE"},
        "rollback_receipt_registry": {rollback_receipt["receipt_id"]: rollback_receipt},
        "legal_review": legal_review,
        "credentials": [{"credential_id": "cred-active", "owner": "human-risk", "status": "ACTIVE", "evidence_ref": "NONE", "restore_enabled": False, "restore_evidence_ref": "NONE", "sessions": [], "delegations": []}],
        "data_inventory": [{"object_id": "data-synthetic", "object_version": "data-v1", "owner": "human-data", "locations": ["live"], "required_action": "retain", "status": "ACTIVE", "evidence_ref": "NONE"}],
        "retirement": seal({"retirement_id": "retirement-21", "release_id": release["release_id"], "requested": False, "owner": "human-business", "decision_ref": "NONE", "lifecycle_event_ref": "NONE", "critical_service": True, "replacement_ref": "NONE", "handoff_ref": "NONE", "evidence_refs": {key: "NONE" for key in retirement_refs}, "decision_digest": ""}, "decision_digest"),
        "retirement_evidence_registry": retirement_registry,
        "environment_registry": environment_registry,
        "legal_scope_registry": legal_scope_registry,
        "holdout_registry": holdout_registry,
    }

    complete_credentials = [{"credential_id": "cred-active", "owner": "human-risk", "status": "REVOKED", "evidence_ref": "cred-revoked-21", "restore_enabled": False, "restore_evidence_ref": "restore-disabled-21", "sessions": [{"session_id": "session-old", "status": "REVOKED", "evidence_ref": "session-revoked-21"}], "delegations": [{"delegation_id": "delegation-old", "status": "REVOKED", "evidence_ref": "delegation-revoked-21"}]}]
    complete_data = [{"object_id": "data-synthetic", "object_version": "data-v1", "owner": "human-data", "locations": [], "required_action": "delete", "status": "DISPOSED", "evidence_ref": "data-disposed-21"}]
    complete_runtime = {"active_release": release["release_id"], "admission": "CLOSED", "tasks": [{"task_id": "task-synthetic", "state": "COMPLETED", "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read", "manifest_ref": "manifest-task-synthetic"}], "schedules": [{"schedule_id": "cron-synthetic", "state": "DISABLED", "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read", "manifest_ref": "manifest-cron-synthetic"}], "webhooks": [{"webhook_id": "hook-synthetic", "state": "DISABLED", "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read", "manifest_ref": "manifest-hook-synthetic"}], "queue": "CLEAR", "workers": "STOPPED", "effect_ledger": []}
    complete_override = {"retirement": retirement_complete, "credentials": complete_credentials, "data_inventory": complete_data, "runtime_state": complete_runtime, "rollout": rollout_from_plan(retired_plan)}

    scenarios: list[dict] = []
    add = lambda overrides, **kw: scenarios.append(scenario(len(scenarios) + 1, overrides, **kw))
    add({}, layer="training", case="CASE-A")
    add({"release_unit": {"build_digest": "sha256:x"}}, layer="training")
    add({"release_unit": {"release_digest": digest("wrong release")}}, layer="training", security=["integrity"])
    forged_approval = copy.deepcopy(base_state["authority_registry"]["approval-release-21"]); forged_approval["authority_digest"] = digest("forged")
    add({"authority_registry": {"approval-release-21": forged_approval}}, layer="training", security=["authority"])
    wrong_digest_approval = copy.deepcopy(base_state["authority_registry"]["approval-release-21"]); wrong_digest_approval["object_digest"] = digest("wrong object"); wrong_digest_approval = seal(wrong_digest_approval, "authority_digest")
    add({"authority_registry": {"approval-release-21": wrong_digest_approval}}, layer="regression", security=["authority"])
    wrong_subject_approval = copy.deepcopy(base_state["authority_registry"]["approval-release-21"]); wrong_subject_approval["subject_id"] = "rel-other"; wrong_subject_approval = seal(wrong_subject_approval, "authority_digest")
    add({"authority_registry": {"approval-release-21": wrong_subject_approval}}, layer="regression", security=["authority"])
    expired = copy.deepcopy(base_state["authority_registry"]["approval-release-21"]); expired["expires_at"] = "2026-09-30T11:00:00Z"; expired = seal(expired, "authority_digest")
    add({"authority_registry": {"approval-release-21": expired}}, layer="regression", security=["authority"])
    future = copy.deepcopy(base_state["authority_registry"]["approval-release-21"]); future["not_before"] = "2026-09-30T13:00:00Z"; future["issued_at"] = "2026-09-30T13:00:00Z"; future = seal(future, "authority_digest")
    add({"authority_registry": {"approval-release-21": future}}, layer="holdout", security=["authority"])
    add({"owner_registry": {"security_risk": owner("human-risk", "agent")}}, layer="holdout", security=["authority"])
    add({"migration": {"receipt_ref": "missing-receipt"}}, layer="regression")
    forged_migration = copy.deepcopy(migration_receipt); forged_migration["record_digest"] = digest("forged")
    add({"migration_receipt_registry": {migration_receipt["receipt_id"]: forged_migration}}, layer="regression", security=["integrity"])
    wrong_migration_subject = copy.deepcopy(migration_receipt); wrong_migration_subject["subject_id"] = "migration-other"; wrong_migration_subject = seal(wrong_migration_subject, "record_digest")
    add({"migration_receipt_registry": {migration_receipt["receipt_id"]: wrong_migration_subject}}, layer="holdout")
    wrong_migration_version = copy.deepcopy(migration_receipt); wrong_migration_version["to_schema"] = "state-v9"; wrong_migration_version = seal(wrong_migration_version, "record_digest")
    add({"migration_receipt_registry": {migration_receipt["receipt_id"]: wrong_migration_version}}, layer="holdout")
    add({"backup": {"manifest_ref": "missing-manifest"}}, layer="regression")
    wrong_manifest = copy.deepcopy(backup_manifest); wrong_manifest["release_id"] = "rel-other"; wrong_manifest = seal(wrong_manifest, "manifest_digest")
    add({"backup_manifest_registry": {backup_manifest["manifest_id"]: wrong_manifest}}, layer="holdout", security=["integrity"])
    missing_coverage = copy.deepcopy(backup_manifest); missing_coverage["covered"].remove("agent_dir"); missing_coverage = seal(missing_coverage, "manifest_digest")
    add({"backup_manifest_registry": {backup_manifest["manifest_id"]: missing_coverage}}, layer="regression")
    add({"restore": {"proof_ref": "missing-proof"}}, layer="regression")
    forged_restore = copy.deepcopy(restore_proof); forged_restore["proof_digest"] = digest("forged")
    add({"restore_proof_registry": {restore_proof["proof_id"]: forged_restore}}, layer="holdout", security=["integrity"])
    wrong_restore = copy.deepcopy(restore_proof); wrong_restore["backup_id"] = "backup-other"; wrong_restore = seal(wrong_restore, "proof_digest")
    add({"restore_proof_registry": {restore_proof["proof_id"]: wrong_restore}}, layer="holdout")
    failed_restore = copy.deepcopy(restore_proof); failed_restore["identity_tenant_check"] = "FAIL"; failed_restore = seal(failed_restore, "proof_digest")
    add({"restore_proof_registry": {restore_proof["proof_id"]: failed_restore}}, layer="holdout", security=["authorization"])
    add({"d21": {"technical": {"evidence_ref": "missing-d21"}}}, layer="regression")
    wrong_d21_task = copy.deepcopy(d21_registry["d21-technical-21"]); wrong_d21_task["task_id"] = "task-other"; wrong_d21_task = seal(wrong_d21_task, "record_digest")
    add({"d21_evidence_registry": {"d21-technical-21": wrong_d21_task}}, layer="holdout")
    wrong_d21_version = copy.deepcopy(d21_registry["d21-delivery-21"]); wrong_d21_version["object_version"] = "artifact-v1"; wrong_d21_version = seal(wrong_d21_version, "record_digest")
    add({"d21_evidence_registry": {"d21-delivery-21": wrong_d21_version}}, layer="holdout")
    duplicate_evidence = retirement_evidence("d21-technical-21", "residual_scan", retirement_complete["retirement_id"], release["release_id"], release["release_digest"], "human-risk", digest("duplicate id"))
    add({"retirement_evidence_registry": {"d21-technical-21": duplicate_evidence}}, layer="holdout", security=["integrity"])
    add({"rollout": {"expires_at": "2026-09-30T11:00:00Z"}}, layer="regression")
    add({"rollout": {"max_trials": -1}}, layer="holdout")
    add({"rollout": {"max_cost": -1}}, layer="holdout")
    four_trials = copy.deepcopy(base_state["trial_ledger"]) + [{"trial_id": "canary-3", "release_id": release["release_id"], "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read", "layer": "holdout", "holdout_ref": "holdout-research-21", "cost": 1.0, "status": "COMPLETED", "quality_gate": "PASS", "security_gate": "PASS", "error_budget_gate": "PASS"}, {"trial_id": "canary-4", "release_id": release["release_id"], "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read", "layer": "holdout", "holdout_ref": "holdout-research-21", "cost": 1.0, "status": "COMPLETED", "quality_gate": "PASS", "security_gate": "PASS", "error_budget_gate": "PASS"}]
    add({"trial_ledger": four_trials}, layer="holdout")
    costly = copy.deepcopy(base_state["trial_ledger"]); costly[0]["cost"] = 20.0
    add({"trial_ledger": costly}, layer="holdout")
    add({"rollout": {"quality_gate": "FAIL"}}, layer="holdout", security=["quality"])
    add({"rollout": {"security_gate": "FAIL"}}, layer="holdout", security=["security"])
    forged_stop = copy.deepcopy(stop_receipt); forged_stop["record_digest"] = digest("forged")
    add({"rollout": {"error_budget_gate": "FAIL", "stop_triggered": True, "stop_receipt_ref": stop_receipt["receipt_id"]}, "stop_receipt_registry": {stop_receipt["receipt_id"]: forged_stop}}, layer="holdout", security=["reliability"])
    stale_stop = copy.deepcopy(stop_receipt); stale_stop["issued_at"] = "2026-09-30T10:00:00Z"; stale_stop = seal(stale_stop, "record_digest")
    add({"rollout": {"stop_triggered": True, "stop_receipt_ref": stop_receipt["receipt_id"]}, "stop_receipt_registry": {stop_receipt["receipt_id"]: stale_stop}}, layer="holdout", security=["recovery"])
    future_stop = copy.deepcopy(stop_receipt); future_stop["issued_at"] = "2026-09-30T12:01:00Z"; future_stop = seal(future_stop, "record_digest")
    add({"rollout": {"stop_triggered": True, "stop_receipt_ref": stop_receipt["receipt_id"]}, "stop_receipt_registry": {stop_receipt["receipt_id"]: future_stop}}, layer="holdout", security=["recovery"])
    add({"runtime_state": {"active_release": "rel-other"}}, layer="regression")
    bad_credential = copy.deepcopy(base_state["credentials"]); bad_credential[0]["unexpected"] = True
    add({"credentials": bad_credential}, layer="holdout", security=["closed-world"])
    invalid_credential = copy.deepcopy(base_state["credentials"]); invalid_credential[0]["status"] = "DELETED"
    add({"credentials": invalid_credential}, layer="holdout", security=["credentials"])
    invalid_data = copy.deepcopy(base_state["data_inventory"]); invalid_data[0]["status"] = "GONE"
    add({"data_inventory": invalid_data}, layer="holdout", security=["data"])
    add(complete_override, layer="regression", case="CASE-A")

    def retirement_variant(**changes: object) -> dict:
        record = copy.deepcopy(retirement_complete)
        for key, value in changes.items(): record[key] = value
        record = seal(record, "decision_digest")
        auth = authority("approval-retirement-21", "human-risk", "approve_retirement", "retirement", record["retirement_id"], record["decision_digest"], retired_plan["plan_digest"])
        return {**copy.deepcopy(complete_override), "retirement": record, "authority_registry": {"approval-retirement-21": auth}}

    dummy = retirement_variant(evidence_refs={**retirement_refs, "signoff": "dummy-agent"})
    add(dummy, layer="holdout", case="CASE-A", security=["retirement"])
    residual_cred = copy.deepcopy(complete_credentials); residual_cred[0]["status"] = "ACTIVE"
    add({**copy.deepcopy(complete_override), "credentials": residual_cred}, layer="holdout", security=["credentials"])
    residual_session = copy.deepcopy(complete_credentials); residual_session[0]["sessions"][0]["status"] = "ACTIVE"
    add({**copy.deepcopy(complete_override), "credentials": residual_session}, layer="holdout", security=["credentials"])
    residual_delegation = copy.deepcopy(complete_credentials); residual_delegation[0]["delegations"][0]["status"] = "ACTIVE"
    add({**copy.deepcopy(complete_override), "credentials": residual_delegation}, layer="holdout", security=["credentials"])
    restore_enabled = copy.deepcopy(complete_credentials); restore_enabled[0]["restore_enabled"] = True
    add({**copy.deepcopy(complete_override), "credentials": restore_enabled}, layer="holdout", security=["recovery"])
    residual_data = copy.deepcopy(complete_data); residual_data[0]["status"] = "RESIDUAL"; residual_data[0]["locations"] = ["index"]
    add({**copy.deepcopy(complete_override), "data_inventory": residual_data}, layer="holdout", security=["privacy"])
    unknown_residual = copy.deepcopy(retirement_registry[retirement_refs["residual"]]); unknown_residual["status"] = "REVIEW_REQUIRED"; unknown_residual = seal(unknown_residual, "record_digest")
    add({**copy.deepcopy(complete_override), "retirement_evidence_registry": {retirement_refs["residual"]: unknown_residual}}, layer="holdout", security=["retirement"])
    wrong_signoff = copy.deepcopy(retirement_registry[retirement_refs["signoff"]]); wrong_signoff["content_digest"] = digest("wrong retirement decision"); wrong_signoff = seal(wrong_signoff, "record_digest")
    add({**copy.deepcopy(complete_override), "retirement_evidence_registry": {retirement_refs["signoff"]: wrong_signoff}}, layer="holdout", security=["authority"])
    unknown_d21 = copy.deepcopy(d21_registry["d21-technical-21"]); unknown_d21["status"] = "REVIEW_REQUIRED"; unknown_d21 = seal(unknown_d21, "record_digest")
    add({"rollout": {"quality_gate": "FAIL"}, "d21": {"technical": {"status": "REVIEW_REQUIRED"}}, "d21_evidence_registry": {"d21-technical-21": unknown_d21}}, layer="holdout", security=["quality", "recovery"])
    residual_unknown_combo = copy.deepcopy(complete_credentials); residual_unknown_combo[0]["status"] = "ACTIVE"
    add({**copy.deepcopy(complete_override), "credentials": residual_unknown_combo, "retirement_evidence_registry": {retirement_refs["residual"]: unknown_residual}}, layer="holdout", security=["credentials", "retirement"])
    unknown_migration = copy.deepcopy(migration); unknown_migration["status"] = "UNKNOWN"; unknown_migration = seal(unknown_migration, "migration_digest")
    unknown_migration_receipt = copy.deepcopy(migration_receipt); unknown_migration_receipt["status"] = "UNKNOWN"; unknown_migration_receipt["migration_digest"] = unknown_migration["migration_digest"]; unknown_migration_receipt = seal(unknown_migration_receipt, "record_digest")
    add({"migration": unknown_migration, "migration_receipt_registry": {migration_receipt["receipt_id"]: unknown_migration_receipt}}, layer="regression")
    add({"d21": {"technical": {"status": "REVIEW_REQUIRED"}}, "d21_evidence_registry": {"d21-technical-21": unknown_d21}}, layer="holdout")
    add({"runtime_state": {"effect_ledger": [{"effect_id": "effect-unknown", "status": "UNKNOWN", "external": True, "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read", "authority_ref": "effect-authority-unknown", "receipt_ref": "effect-receipt-unknown", "readback_ref": "effect-readback-unknown"}]}}, layer="holdout", security=["external-effect"])
    add({"legal_review": {"status": "REVIEW_REQUIRED", "license": "UNKNOWN"}}, layer="holdout", security=["legal"])
    add({"rollback": {"requested": True, "status": "ROLLBACK_PENDING"}}, layer="holdout", security=["recovery"])
    add({"rollout": {"stop_triggered": True, "stop_receipt_ref": stop_receipt["receipt_id"]}}, layer="regression", security=["recovery"])

    # v2.1 adjacent regressions found by the first independent rerun.
    add({"rollback": {"requested": True, "status": "ROLLED_BACK", "old_runtime_reads_current_schema": True, "code_config_reverted": True, "receipt_ref": "dummy-receipt"}}, layer="holdout", security=["recovery"])
    agent_migration = copy.deepcopy(migration); agent_migration["owner"] = "agent-self"; agent_migration = seal(agent_migration, "migration_digest")
    agent_migration_receipt = copy.deepcopy(migration_receipt); agent_migration_receipt["owner"] = "agent-self"; agent_migration_receipt["migration_digest"] = agent_migration["migration_digest"]; agent_migration_receipt = seal(agent_migration_receipt, "record_digest")
    add({"migration": agent_migration, "migration_receipt_registry": {agent_migration_receipt["receipt_id"]: agent_migration_receipt}}, layer="holdout", security=["authority"])
    agent_backup = copy.deepcopy(backup_manifest); agent_backup["access_owner"] = "agent-self"; agent_backup = seal(agent_backup, "manifest_digest")
    add({"backup": {"owner": "agent-self"}, "backup_manifest_registry": {agent_backup["manifest_id"]: agent_backup}}, layer="holdout", security=["authority"])
    agent_restore = copy.deepcopy(restore_proof); agent_restore["owner"] = "agent-self"; agent_restore = seal(agent_restore, "proof_digest")
    add({"restore": {"owner": "agent-self"}, "restore_proof_registry": {agent_restore["proof_id"]: agent_restore}}, layer="holdout", security=["authority"])
    add({"rollout": {"owner": "agent-self"}}, layer="holdout", security=["authority"])
    negative_restore = copy.deepcopy(restore_proof); negative_restore["rpo_minutes"] = -1; negative_restore["rto_minutes"] = -1; negative_restore = seal(negative_restore, "proof_digest")
    add({"restore_proof_registry": {negative_restore["proof_id"]: negative_restore}}, layer="holdout", security=["range"])
    nan_trials = copy.deepcopy(base_state["trial_ledger"]); nan_trials[0]["cost"] = float("nan")
    add({"trial_ledger": nan_trials}, layer="holdout", security=["range"])
    conflicting_backup = copy.deepcopy(backup_manifest); conflicting_backup["excluded"] = conflicting_backup["excluded"] + ["agent_db"]; conflicting_backup = seal(conflicting_backup, "manifest_digest")
    add({"backup_manifest_registry": {conflicting_backup["manifest_id"]: conflicting_backup}}, layer="holdout", security=["integrity"])
    irreversible_migration = copy.deepcopy(migration); irreversible_migration["irreversible_steps"] = ["drop-state-v1"]; irreversible_migration = seal(irreversible_migration, "migration_digest")
    irreversible_receipt = copy.deepcopy(migration_receipt); irreversible_receipt["migration_digest"] = irreversible_migration["migration_digest"]; irreversible_receipt = seal(irreversible_receipt, "record_digest")
    add({"migration": irreversible_migration, "migration_receipt_registry": {irreversible_receipt["receipt_id"]: irreversible_receipt}}, layer="holdout", security=["irreversible-change"])

    # Retain the v2.2 scope/lifecycle regressions inside the v2.4 fixture.
    add({"owner_registry": {"technical": owner("agent-self")}, "migration": {"owner": "agent-self"}, "restore": {"owner": "agent-self"}}, layer="holdout", security=["frozen-authority-root"])
    add({"rollout": {"stage": "PRODUCTION"}, "runtime_state": {"admission": "OPEN_PRODUCTION"}}, layer="holdout", security=["offline-production"])
    add({"rollout": {"allowed_tenants": [], "allowed_tasks": [], "allowed_actions": []}}, layer="holdout", security=["scope"])
    add({"runtime_state": {"effect_ledger": [{"effect_id": "effect-internal-unauthorized", "status": "APPLIED", "authorized": False, "external": False, "readback": "CONFIRMED", "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read"}]}}, layer="holdout", security=["authorization"])
    add({"rollout": {"stage": "PAUSED"}}, layer="holdout", security=["lifecycle"])
    add({"runtime_state": {"tasks": [{"task_id": "task-synthetic", "state": "COMPLETED", "owner": "agent-self", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read"}]}}, layer="holdout", security=["authority"])
    add({"legal_review": {"legal_scope_ref": "legal-unregistered"}}, layer="holdout", security=["legal"])
    add({"restore_proof_registry": {restore_proof["proof_id"]: seal({**restore_proof, "environment_ref": "env-production-unregistered"}, "proof_digest")}}, layer="holdout", security=["environment", "frozen-authority-root"])
    add({"rollout": {"stage": "ROLLED_BACK"}, "rollback": {"requested": True, "status": "ROLLED_BACK", "old_runtime_reads_current_schema": True, "code_config_reverted": True, "receipt_ref": "rollback-receipt-21"}}, layer="holdout", security=["rollback"])
    missing_holdout = copy.deepcopy(base_state["trial_ledger"]); missing_holdout[0]["holdout_ref"] = "NONE"
    add({"trial_ledger": missing_holdout}, layer="holdout", security=["holdout-isolation"])
    wrong_tenant_trials = copy.deepcopy(base_state["trial_ledger"]); wrong_tenant_trials[0]["tenant_id"] = "tenant-other"
    add({"trial_ledger": wrong_tenant_trials}, layer="holdout", security=["scope"])
    add({"runtime_state": {"tasks": [{"task_id": "task-synthetic", "state": "COMPLETED", "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "delete_production"}]}}, layer="holdout", security=["scope"])
    add({"runtime_state": {"effect_ledger": [{"effect_id": "effect-out-of-scope", "status": "APPLIED", "authorized": True, "external": False, "readback": "CONFIRMED", "owner": "human-operations", "tenant_id": "tenant-other", "task_type": "research", "action": "read"}]}}, layer="holdout", security=["scope"])
    contaminated = copy.deepcopy(holdout_registry["holdout-research-21"]); contaminated["gold_exposed"] = True; contaminated["contamination_status"] = "CONTAMINATED"; contaminated = seal(contaminated, "record_digest")
    add({"holdout_registry": {"holdout-research-21": contaminated}}, layer="holdout", security=["holdout-isolation", "frozen-authority-root"])
    active_retired_runtime = copy.deepcopy(complete_runtime); active_retired_runtime["schedules"][0]["state"] = "ACTIVE"
    add({**copy.deepcopy(complete_override), "runtime_state": active_retired_runtime}, layer="holdout", security=["lifecycle"])

    security_slices = sorted({slice_name for item in scenarios for slice_name in item["security_slices"]})
    base_state["security_control_registry"] = {
        f"security-{slice_name}": seal({"control_id": f"security-{slice_name}", "slice": slice_name, "status": "ACTIVE", "owner": "human-risk", "test_digest": digest({"slice": slice_name, "suite": "c21-v2.4"}), "record_digest": ""}, "record_digest")
        for slice_name in security_slices
    }
    for item in scenarios:
        task = task_record(item["task_id"], "read")
        dataset = datasets[{"training": "dataset-training-21", "regression": "dataset-regression-21", "holdout": "dataset-holdout-21"}[item["layer"]]]
        terminal = terminal_record(f"terminal-{item['trial_id']}", item["trial_id"], "READY")
        trial = trial_record(item["trial_id"], task, release["release_id"], dataset, terminal, "read", 0.0)
        base_state["task_registry"][task["task_id"]] = task
        base_state["terminal_registry"][terminal["terminal_id"]] = terminal
        base_state["trial_registry"][trial["trial_id"]] = trial
        evidence = seal({
            "scenario_id": item["scenario_id"], "task_id": item["task_id"], "trial_id": item["trial_id"], "task_type": item["task_type"],
            "dataset_ref": dataset["dataset_id"], "layer": dataset["layer"], "holdout_ref": dataset["holdout_ref"],
            "security_refs": [f"security-{slice_name}" for slice_name in item["security_slices"]],
            "control_trial_refs": [trial_one["trial_id"], trial_two["trial_id"]], "record_digest": "",
        }, "record_digest")
        base_state["scenario_evidence_registry"][item["scenario_id"]] = evidence

    frozen_names = ("owner_registry", "authority_registry", "migration_receipt_registry", "backup_manifest_registry", "restore_proof_registry", "stop_receipt_registry", "rollback_receipt_registry", "d21_evidence_registry", "retirement_evidence_registry", "publication_event_registry", "lifecycle_event_registry", "environment_registry", "legal_scope_registry", "holdout_registry", "rollout_plan_registry", "task_registry", "trial_registry", "dataset_registry", "grader_registry", "terminal_registry", "effect_receipt_registry", "effect_readback_registry", "automation_manifest_registry", "security_control_registry", "scenario_evidence_registry")
    authority_root = {key: copy.deepcopy(base_state[key]) for key in frozen_names}
    authority_root["root_digest"] = digest(authority_root)
    fixture = {"schema_version": "c21.lifecycle.input.v2.4", "seed": "C21-2026-09-30-v2.4", "now": "2026-09-30T12:00:00Z", "environment": {"mode": "offline_synthetic", "network": False, "real_credentials": False, "production_write": False, "external_side_effects_allowed": False}, "authority_root_digest": authority_root["root_digest"], "base_state": base_state, "scenarios": scenarios}
    AUTHORITY_OUTPUT.write_text(json.dumps(authority_root, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUTPUT.write_text(json.dumps(fixture, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

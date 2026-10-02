#!/usr/bin/env python3
"""C21 v2.4 deterministic closed-world lifecycle controller.

Decisions are derived from raw state and independently addressable registries.
Scenario names carry no semantics and the input has no expected field.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

LAYERS = {"training", "regression", "holdout", "representative_real_world"}
VERDICTS = {"PASS", "FAIL", "REVIEW_REQUIRED"}
OWNER_ROLES = {"business", "technical", "data", "capability", "security_risk", "operations"}
REQUIRED_COVERAGE = {"global_db", "agent_db", "agent_dir", "contracts", "memory", "skills", "plugins", "audit"}
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PINNED_AUTHORITY_ROOT_DIGEST = "sha256:c03223f3537c558e0d2c2828ac498fd56cd950f354b84d8ab0b827c1f700aa09"
FROZEN_REGISTRIES = {
    "owner_registry", "authority_registry", "migration_receipt_registry",
    "backup_manifest_registry", "restore_proof_registry", "stop_receipt_registry",
    "rollback_receipt_registry", "d21_evidence_registry",
    "retirement_evidence_registry", "publication_event_registry",
    "lifecycle_event_registry", "environment_registry",
    "legal_scope_registry", "holdout_registry", "rollout_plan_registry",
    "task_registry", "trial_registry", "dataset_registry", "grader_registry",
    "terminal_registry", "effect_receipt_registry", "effect_readback_registry",
    "automation_manifest_registry", "security_control_registry",
    "scenario_evidence_registry",
}


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


def record_digest(record: dict, field: str) -> str:
    return sha256({key: value for key, value in record.items() if key != field})


def digest_valid(value: object) -> bool:
    return type(value) is str and DIGEST_RE.fullmatch(value) is not None


def record_digest_valid(record: dict, field: str) -> bool:
    return digest_valid(record.get(field)) and record[field] == record_digest(record, field)


def exact(value: object, required: set[str], optional: set[str], path: str) -> dict:
    if type(value) is not dict:
        raise ValueError(f"{path} must be object")
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - required - optional)
    if missing:
        raise ValueError(f"{path} missing fields: {missing}")
    if unknown:
        raise ValueError(f"{path} unknown fields: {unknown}")
    return value


def typed(value: object, expected: type, path: str) -> None:
    if type(value) is not expected:
        raise ValueError(f"{path} must be {expected.__name__}")


def strings(value: object, path: str) -> list[str]:
    typed(value, list, path)
    if not all(type(item) is str for item in value):
        raise ValueError(f"{path} must contain strings")
    return value


def number(value: object, path: str) -> None:
    if type(value) not in {int, float} or not math.isfinite(value):
        raise ValueError(f"{path} must be finite number")


def parse_time(value: object, path: str) -> datetime:
    typed(value, str, path)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{path} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{path} must include timezone")
    return parsed


def active_at(record: dict, now: datetime) -> bool:
    return record["status"] == "ACTIVE" and parse_time(record["not_before"], "record.not_before") <= now and parse_time(record["issued_at"], "record.issued_at") <= now < parse_time(record["expires_at"], "record.expires_at")


def deep_merge(base: dict, override: dict) -> dict:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if type(value) is dict and type(merged.get(key)) is dict:
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def validate_owner_registry(registry: object, path: str) -> dict:
    registry = exact(registry, OWNER_ROLES, set(), path)
    principals = []
    for role, item in registry.items():
        item = exact(item, {"principal", "kind", "status", "valid_from", "expires_at"}, set(), f"{path}.{role}")
        for key in ("principal", "kind", "status"):
            typed(item[key], str, f"{path}.{role}.{key}")
        if item["kind"] not in {"human", "legal_entity", "agent"} or item["status"] not in {"ACTIVE", "INACTIVE", "UNKNOWN"}:
            raise ValueError(f"{path}.{role} enum invalid")
        parse_time(item["valid_from"], f"{path}.{role}.valid_from")
        parse_time(item["expires_at"], f"{path}.{role}.expires_at")
        principals.append(item["principal"])
    if len(principals) != len(set(principals)):
        raise ValueError(f"{path} principals must be unique")
    return registry


def validate_authorities(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"authority_id", "actor", "action", "subject_type", "subject_id", "object_digest", "scope", "status", "not_before", "expires_at", "issued_at", "policy_version", "authority_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in item:
            typed(item[field], str, f"{path}.{key}.{field}")
        if item["authority_id"] != key or item["status"] not in {"ACTIVE", "REVOKED", "EXPIRED", "UNKNOWN"}:
            raise ValueError(f"{path}.{key} binding or enum invalid")
        for field in ("not_before", "expires_at", "issued_at"):
            parse_time(item[field], f"{path}.{key}.{field}")
    return registry


def validate_release(item: object, path: str) -> dict:
    fields = {"release_id", "agent_id", "build_ref", "build_digest", "contract_digest", "policy_digest", "policy_version", "model_ref", "model_params_digest", "tool_manifest_digest", "skill_manifest_digest", "memory_schema", "state_schema", "dependency_lock_digest", "sbom_ref", "observability_schema_ref", "eval_baseline_ref", "security_review_ref", "backup_restore_proof_ref", "rollout_plan_ref", "change_class", "proposer", "approver", "operator", "acceptor", "approval_ref", "publication_event_ref", "release_digest"}
    item = exact(item, fields, set(), path)
    for field in item:
        typed(item[field], str, f"{path}.{field}")
    return item


def validate_migration(item: object, path: str) -> dict:
    item = exact(item, {"migration_id", "release_id", "from_schema", "to_schema", "candidate_reads_from", "candidate_writes_to", "old_runtime_reads_to", "dry_run", "status", "receipt_ref", "reentrant", "irreversible_steps", "irreversible_approval_ref", "recovery_strategy", "owner", "migration_digest"}, set(), path)
    for field in ("migration_id", "release_id", "from_schema", "to_schema", "dry_run", "status", "receipt_ref", "irreversible_approval_ref", "recovery_strategy", "owner", "migration_digest"):
        typed(item[field], str, f"{path}.{field}")
    for field in ("candidate_reads_from", "candidate_writes_to", "old_runtime_reads_to", "reentrant"):
        typed(item[field], bool, f"{path}.{field}")
    strings(item["irreversible_steps"], f"{path}.irreversible_steps")
    if item["dry_run"] not in VERDICTS or item["status"] not in {"VERIFIED", "FAILED", "UNKNOWN"} or item["recovery_strategy"] not in {"ROLLBACK", "FORWARD_ONLY"}:
        raise ValueError(f"{path} enum invalid")
    return item


def validate_receipt_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"receipt_id", "subject_type", "subject_id", "release_id", "from_schema", "to_schema", "status", "owner", "issued_at", "expires_at", "migration_digest", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in item:
            typed(item[field], str, f"{path}.{key}.{field}")
        if item["receipt_id"] != key or item["status"] not in {"VERIFIED", "FAILED", "UNKNOWN", "REVOKED"}:
            raise ValueError(f"{path}.{key} binding or enum invalid")
        parse_time(item["issued_at"], f"{path}.{key}.issued_at")
        parse_time(item["expires_at"], f"{path}.{key}.expires_at")
    return registry


def validate_backup(item: object, path: str) -> dict:
    item = exact(item, {"backup_id", "release_id", "manifest_ref", "owner"}, set(), path)
    for field in item:
        typed(item[field], str, f"{path}.{field}")
    return item


def validate_backup_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"manifest_id", "backup_id", "release_id", "covered", "excluded", "consistent_snapshot", "archive_digest", "integrity", "encrypted", "access_owner", "created_at", "expires_at", "manifest_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in ("manifest_id", "backup_id", "release_id", "archive_digest", "integrity", "access_owner", "manifest_digest"):
            typed(item[field], str, f"{path}.{key}.{field}")
        strings(item["covered"], f"{path}.{key}.covered")
        strings(item["excluded"], f"{path}.{key}.excluded")
        typed(item["consistent_snapshot"], bool, f"{path}.{key}.consistent_snapshot")
        typed(item["encrypted"], bool, f"{path}.{key}.encrypted")
        parse_time(item["created_at"], f"{path}.{key}.created_at")
        parse_time(item["expires_at"], f"{path}.{key}.expires_at")
        if item["manifest_id"] != key or item["integrity"] not in VERDICTS:
            raise ValueError(f"{path}.{key} binding or enum invalid")
    return registry


def validate_restore(item: object, path: str) -> dict:
    item = exact(item, {"restore_id", "release_id", "backup_id", "proof_ref", "owner", "target_rpo_minutes", "target_rto_minutes"}, set(), path)
    for field in ("restore_id", "release_id", "backup_id", "proof_ref", "owner"):
        typed(item[field], str, f"{path}.{field}")
    for field in ("target_rpo_minutes", "target_rto_minutes"):
        number(item[field], f"{path}.{field}")
        if item[field] < 0:
            raise ValueError(f"{path}.{field} must be nonnegative")
    return item


def validate_restore_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"proof_id", "restore_id", "backup_id", "release_id", "archive_digest", "environment_ref", "hash_verified", "schema_integrity", "identity_tenant_check", "credentials_rebuilt", "task_replay", "delivery_check", "environment_terminal", "rpo_minutes", "rto_minutes", "owner", "issued_at", "expires_at", "proof_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in ("proof_id", "restore_id", "backup_id", "release_id", "archive_digest", "environment_ref", "schema_integrity", "identity_tenant_check", "task_replay", "delivery_check", "environment_terminal", "owner", "proof_digest"):
            typed(item[field], str, f"{path}.{key}.{field}")
        for field in ("hash_verified", "credentials_rebuilt"):
            typed(item[field], bool, f"{path}.{key}.{field}")
        for field in ("rpo_minutes", "rto_minutes"):
            number(item[field], f"{path}.{key}.{field}")
            if item[field] < 0:
                raise ValueError(f"{path}.{key}.{field} must be nonnegative")
        parse_time(item["issued_at"], f"{path}.{key}.issued_at")
        parse_time(item["expires_at"], f"{path}.{key}.expires_at")
        if item["proof_id"] != key:
            raise ValueError(f"{path}.{key} id binding invalid")
        for field in ("schema_integrity", "identity_tenant_check", "task_replay", "delivery_check", "environment_terminal"):
            if item[field] not in VERDICTS:
                raise ValueError(f"{path}.{key}.{field} enum invalid")
    return registry


def validate_rollout(item: object, path: str) -> dict:
    fields = {"plan_id", "plan_digest", "release_id", "stage", "scope", "scope_digest", "allowed_tenants", "allowed_tasks", "allowed_actions", "candidate_permissions", "baseline_permissions", "min_trials", "max_trials", "max_cost", "starts_at", "expires_at", "environment_ref", "quality_gate", "security_gate", "error_budget_gate", "stop_triggered", "stop_receipt_ref", "owner"}
    item = exact(item, fields, set(), path)
    for field in ("plan_id", "plan_digest", "release_id", "stage", "scope", "scope_digest", "environment_ref", "quality_gate", "security_gate", "error_budget_gate", "stop_receipt_ref", "owner"):
        typed(item[field], str, f"{path}.{field}")
    if item["stage"] not in {"SHADOW", "CANARY", "LIMITED", "PRODUCTION", "PAUSED", "ROLLBACK_PENDING", "ROLLED_BACK", "FORWARD_FIX", "RETIRED"}:
        raise ValueError(f"{path}.stage enum invalid")
    for field in ("quality_gate", "security_gate", "error_budget_gate"):
        if item[field] not in {"PASS", "FAIL", "UNKNOWN"}:
            raise ValueError(f"{path}.{field} enum invalid")
    for field in ("allowed_tenants", "allowed_tasks", "allowed_actions", "candidate_permissions", "baseline_permissions"):
        strings(item[field], f"{path}.{field}")
    for field in ("min_trials", "max_trials", "max_cost"):
        number(item[field], f"{path}.{field}")
    parse_time(item["starts_at"], f"{path}.starts_at")
    parse_time(item["expires_at"], f"{path}.expires_at")
    typed(item["stop_triggered"], bool, f"{path}.stop_triggered")
    return item


def validate_trials(items: object, path: str) -> list[dict]:
    typed(items, list, path)
    ids = []
    for index, item in enumerate(items):
        p = f"{path}[{index}]"
        item = exact(item, {"trial_id", "task_id", "release_id", "subject_id", "tenant_id", "task_type", "action", "dataset_ref", "layer", "holdout_ref", "input_digest", "grader_ref", "terminal_ref", "cost", "quality_gate", "security_gate", "error_budget_gate", "trial_digest"}, set(), p)
        for field in ("trial_id", "task_id", "release_id", "subject_id", "tenant_id", "task_type", "action", "dataset_ref", "layer", "holdout_ref", "input_digest", "grader_ref", "terminal_ref", "quality_gate", "security_gate", "error_budget_gate", "trial_digest"):
            typed(item[field], str, f"{p}.{field}")
        number(item["cost"], f"{p}.cost")
        if item["cost"] < 0:
            raise ValueError(f"{p}.cost must be nonnegative")
        if item["layer"] not in LAYERS:
            raise ValueError(f"{p}.layer enum invalid")
        for field in ("quality_gate", "security_gate", "error_budget_gate"):
            if item[field] not in {"PASS", "FAIL", "UNKNOWN"}:
                raise ValueError(f"{p}.{field} enum invalid")
        ids.append(item["trial_id"])
    if len(ids) != len(set(ids)):
        raise ValueError(f"{path} trial IDs must be unique")
    return items


def validate_stop_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"receipt_id", "release_id", "plan_id", "reason_codes", "status", "owner", "issued_at", "expires_at", "admission", "queue", "workers", "active_release", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in ("receipt_id", "release_id", "plan_id", "status", "owner", "admission", "queue", "workers", "active_release", "record_digest"):
            typed(item[field], str, f"{path}.{key}.{field}")
        strings(item["reason_codes"], f"{path}.{key}.reason_codes")
        parse_time(item["issued_at"], f"{path}.{key}.issued_at")
        parse_time(item["expires_at"], f"{path}.{key}.expires_at")
        if item["receipt_id"] != key or item["status"] not in {"VERIFIED", "FAILED", "UNKNOWN", "REVOKED"}:
            raise ValueError(f"{path}.{key} binding or enum invalid")
        if item["admission"] not in {"PAUSED", "CLOSED"} or item["queue"] not in {"CLEAR", "NOT_CLEAR", "UNKNOWN"} or item["workers"] not in {"STOPPED", "RUNNING", "UNKNOWN"}:
            raise ValueError(f"{path}.{key} readback enum invalid")
    return registry


def validate_d21(item: object, path: str) -> dict:
    item = exact(item, {"task_id", "release_id", "object_id", "object_version", "technical", "delivery", "business", "environment"}, set(), path)
    for field in ("task_id", "release_id", "object_id", "object_version"):
        typed(item[field], str, f"{path}.{field}")
    for face in ("technical", "delivery", "business", "environment"):
        rec = exact(item[face], {"status", "evidence_ref"}, set(), f"{path}.{face}")
        if rec["status"] not in VERDICTS:
            raise ValueError(f"{path}.{face}.status enum invalid")
        typed(rec["evidence_ref"], str, f"{path}.{face}.evidence_ref")
    return item


def validate_d21_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"evidence_id", "face", "task_id", "release_id", "object_id", "object_version", "object_digest", "status", "source", "owner", "observed_at", "expires_at", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in item:
            typed(item[field], str, f"{path}.{key}.{field}")
        if item["evidence_id"] != key or item["face"] not in {"technical", "delivery", "business", "environment"} or item["status"] not in VERDICTS:
            raise ValueError(f"{path}.{key} binding or enum invalid")
        parse_time(item["observed_at"], f"{path}.{key}.observed_at")
        parse_time(item["expires_at"], f"{path}.{key}.expires_at")
    return registry


def validate_runtime(item: object, path: str) -> dict:
    item = exact(item, {"active_release", "admission", "tasks", "schedules", "webhooks", "queue", "workers", "effect_ledger"}, set(), path)
    for field in ("active_release", "admission", "queue", "workers"):
        typed(item[field], str, f"{path}.{field}")
    if item["admission"] not in {"OPEN_CANARY", "OPEN_LIMITED", "OPEN_PRODUCTION", "PAUSED", "CLOSED"} or item["queue"] not in {"CLEAR", "NOT_CLEAR", "UNKNOWN"} or item["workers"] not in {"RUNNING", "STOPPED", "UNKNOWN"}:
        raise ValueError(f"{path} runtime enum invalid")
    declared = []
    for kind, id_field, states in (("tasks", "task_id", {"QUEUED", "ACTIVE", "COMPLETED", "FAILED", "CANCELED", "UNKNOWN"}), ("schedules", "schedule_id", {"ACTIVE", "PAUSED", "DISABLED", "UNKNOWN"}), ("webhooks", "webhook_id", {"ACTIVE", "PAUSED", "DISABLED", "UNKNOWN"})):
        typed(item[kind], list, f"{path}.{kind}")
        for index, row in enumerate(item[kind]):
            row = exact(row, {id_field, "state", "owner", "tenant_id", "task_type", "action"}, {"manifest_ref"}, f"{path}.{kind}[{index}]")
            for field in row:
                typed(row[field], str, f"{path}.{kind}[{index}].{field}")
            if row["state"] not in states:
                raise ValueError(f"{path}.{kind}[{index}].state invalid")
            declared.append(row[id_field])
    typed(item["effect_ledger"], list, f"{path}.effect_ledger")
    for index, row in enumerate(item["effect_ledger"]):
        row = exact(row, {"effect_id", "status", "external", "owner", "tenant_id", "task_type", "action"}, {"authorized", "readback", "authority_ref", "receipt_ref", "readback_ref"}, f"{path}.effect_ledger[{index}]")
        for field in ("effect_id", "status", "owner", "tenant_id", "task_type", "action"):
            typed(row[field], str, f"{path}.effect_ledger[{index}].{field}")
        typed(row["external"], bool, f"{path}.effect_ledger[{index}].external")
        if "authorized" in row:
            typed(row["authorized"], bool, f"{path}.effect_ledger[{index}].authorized")
        if "readback" in row:
            typed(row["readback"], str, f"{path}.effect_ledger[{index}].readback")
        for field in ("authority_ref", "receipt_ref", "readback_ref"):
            if field in row:
                typed(row[field], str, f"{path}.effect_ledger[{index}].{field}")
        if row["status"] not in {"PENDING", "APPLIED", "FAILED", "RECONCILED", "UNKNOWN"}:
            raise ValueError(f"{path}.effect_ledger[{index}] enum invalid")
        declared.append(row["effect_id"])
    if len(declared) != len(set(declared)):
        raise ValueError(f"{path} nested IDs must be unique")
    return item


def validate_rollback(item: object, path: str) -> dict:
    item = exact(item, {"requested", "status", "target_release", "old_runtime_reads_current_schema", "code_config_reverted", "external_effects_reconciled", "compensation_status", "receipt_ref"}, set(), path)
    for field in ("requested", "old_runtime_reads_current_schema", "code_config_reverted", "external_effects_reconciled"):
        typed(item[field], bool, f"{path}.{field}")
    for field in ("status", "target_release", "compensation_status", "receipt_ref"):
        typed(item[field], str, f"{path}.{field}")
    if item["status"] not in {"NOT_REQUIRED", "ROLLBACK_PENDING", "ROLLED_BACK", "FORWARD_FIX", "UNKNOWN"} or item["compensation_status"] not in {"NOT_REQUIRED", "PENDING", "COMPLETE", "UNKNOWN"}:
        raise ValueError(f"{path} enum invalid")
    return item


def validate_rollback_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"receipt_id", "release_id", "target_release", "owner", "status", "active_release", "code_config_reverted", "old_runtime_reads_current_schema", "external_effects_reconciled", "compensation_status", "admission", "queue", "workers", "issued_at", "expires_at", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in ("receipt_id", "release_id", "target_release", "owner", "status", "active_release", "compensation_status", "admission", "queue", "workers", "issued_at", "expires_at", "record_digest"):
            typed(item[field], str, f"{path}.{key}.{field}")
        for field in ("code_config_reverted", "old_runtime_reads_current_schema", "external_effects_reconciled"):
            typed(item[field], bool, f"{path}.{key}.{field}")
        if item["receipt_id"] != key or item["status"] not in {"VERIFIED", "FAILED", "UNKNOWN"} or item["compensation_status"] not in {"COMPLETE", "NOT_REQUIRED", "FAILED", "UNKNOWN"}:
            raise ValueError(f"{path}.{key} binding or enum invalid")
        if item["admission"] not in {"PAUSED", "CLOSED"} or item["queue"] not in {"CLEAR", "NOT_CLEAR", "UNKNOWN"} or item["workers"] not in {"STOPPED", "RUNNING", "UNKNOWN"}:
            raise ValueError(f"{path}.{key} readback enum invalid")
        parse_time(item["issued_at"], f"{path}.{key}.issued_at")
        parse_time(item["expires_at"], f"{path}.{key}.expires_at")
    return registry


def validate_legal(item: object, path: str) -> dict:
    item = exact(item, {"status", "reviewer", "legal_scope_ref", "data_use", "license", "privacy", "reviewed_at", "expires_at"}, set(), path)
    for field in item:
        typed(item[field], str, f"{path}.{field}")
    if item["status"] not in VERDICTS or item["data_use"] not in {"APPROVED", "REJECTED", "UNKNOWN"} or item["license"] not in {"APPROVED", "REJECTED", "UNKNOWN"} or item["privacy"] not in {"APPROVED", "REJECTED", "UNKNOWN"}:
        raise ValueError(f"{path} enum invalid")
    parse_time(item["reviewed_at"], f"{path}.reviewed_at")
    parse_time(item["expires_at"], f"{path}.expires_at")
    return item


def validate_environment_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"environment_id", "kind", "mode", "region", "scope", "status", "owner", "issued_at", "expires_at", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in item:
            typed(item[field], str, f"{path}.{key}.{field}")
        if item["environment_id"] != key or item["kind"] not in {"isolated_restore", "offline_runtime"} or item["mode"] != "offline_synthetic" or item["status"] not in {"ACTIVE", "REVOKED", "UNKNOWN"}:
            raise ValueError(f"{path}.{key} binding or enum invalid")
        parse_time(item["issued_at"], f"{path}.{key}.issued_at")
        parse_time(item["expires_at"], f"{path}.{key}.expires_at")
    return registry


def validate_legal_scope_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"legal_scope_id", "region", "scope", "allowed_environment_refs", "status", "owner", "issued_at", "expires_at", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in ("legal_scope_id", "region", "scope", "status", "owner", "issued_at", "expires_at", "record_digest"):
            typed(item[field], str, f"{path}.{key}.{field}")
        strings(item["allowed_environment_refs"], f"{path}.{key}.allowed_environment_refs")
        if item["legal_scope_id"] != key or item["status"] not in {"ACTIVE", "REVOKED", "UNKNOWN"}:
            raise ValueError(f"{path}.{key} binding or enum invalid")
        parse_time(item["issued_at"], f"{path}.{key}.issued_at")
        parse_time(item["expires_at"], f"{path}.{key}.expires_at")
    return registry


def validate_holdout_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"holdout_id", "task_type", "release_id", "lineage_digest", "isolation_manifest_digest", "grader_ref", "gold_exposed", "contamination_status", "status", "owner", "issued_at", "expires_at", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in ("holdout_id", "task_type", "release_id", "lineage_digest", "isolation_manifest_digest", "grader_ref", "contamination_status", "status", "owner", "issued_at", "expires_at", "record_digest"):
            typed(item[field], str, f"{path}.{key}.{field}")
        typed(item["gold_exposed"], bool, f"{path}.{key}.gold_exposed")
        if item["holdout_id"] != key or item["contamination_status"] not in {"CLEAN", "CONTAMINATED", "UNKNOWN"} or item["status"] not in {"ACTIVE", "REVOKED", "UNKNOWN"}:
            raise ValueError(f"{path}.{key} binding or enum invalid")
        parse_time(item["issued_at"], f"{path}.{key}.issued_at")
        parse_time(item["expires_at"], f"{path}.{key}.expires_at")
    return registry


def validate_rollout_plan_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"plan_id", "release_id", "stage", "scope", "scope_digest", "allowed_tenants", "allowed_tasks", "allowed_actions", "candidate_permissions", "baseline_permissions", "min_trials", "max_trials", "max_cost", "starts_at", "expires_at", "environment_ref", "owner", "approval_ref", "plan_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in ("plan_id", "release_id", "stage", "scope", "scope_digest", "starts_at", "expires_at", "environment_ref", "owner", "approval_ref", "plan_digest"):
            typed(item[field], str, f"{path}.{key}.{field}")
        for field in ("allowed_tenants", "allowed_tasks", "allowed_actions", "candidate_permissions", "baseline_permissions"):
            strings(item[field], f"{path}.{key}.{field}")
        for field in ("min_trials", "max_trials", "max_cost"):
            number(item[field], f"{path}.{key}.{field}")
            if item[field] <= 0:
                raise ValueError(f"{path}.{key}.{field} must be positive")
        parse_time(item["starts_at"], f"{path}.{key}.starts_at")
        parse_time(item["expires_at"], f"{path}.{key}.expires_at")
        if item["plan_id"] != key or item["stage"] not in {"SHADOW", "CANARY", "LIMITED", "PRODUCTION", "PAUSED", "ROLLBACK_PENDING", "ROLLED_BACK", "FORWARD_FIX", "RETIRED"} or not record_digest_valid(item, "plan_digest"):
            raise ValueError(f"{path}.{key} binding enum or digest invalid")
    return registry


def validate_task_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"task_id", "subject_id", "tenant_id", "task_type", "action", "owner", "status", "input_digest", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in fields:
            typed(item[field], str, f"{path}.{key}.{field}")
        if item["task_id"] != key or item["status"] not in {"ACTIVE", "COMPLETE", "FAILED", "UNKNOWN"} or not record_digest_valid(item, "record_digest"):
            raise ValueError(f"{path}.{key} binding enum or digest invalid")
    return registry


def validate_dataset_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"dataset_id", "release_id", "layer", "holdout_ref", "lineage_digest", "status", "owner", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in fields:
            typed(item[field], str, f"{path}.{key}.{field}")
        if item["dataset_id"] != key or item["layer"] not in LAYERS or item["status"] not in {"ACTIVE", "NOT_RUN", "UNKNOWN"} or not record_digest_valid(item, "record_digest"):
            raise ValueError(f"{path}.{key} binding enum or digest invalid")
    return registry


def validate_grader_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"grader_id", "version", "rubric_digest", "status", "owner", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in fields:
            typed(item[field], str, f"{path}.{key}.{field}")
        if item["grader_id"] != key or item["status"] not in {"ACTIVE", "REVOKED", "UNKNOWN"} or not record_digest_valid(item, "record_digest"):
            raise ValueError(f"{path}.{key} binding enum or digest invalid")
    return registry


def validate_terminal_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"terminal_id", "trial_id", "status", "result_digest", "owner", "observed_at", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in fields:
            typed(item[field], str, f"{path}.{key}.{field}")
        parse_time(item["observed_at"], f"{path}.{key}.observed_at")
        if item["terminal_id"] != key or item["status"] not in {"COMPLETED", "FAILED", "UNKNOWN", "READY"} or not record_digest_valid(item, "record_digest"):
            raise ValueError(f"{path}.{key} binding enum or digest invalid")
    return registry


def validate_trial_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    required = {"trial_id", "task_id", "release_id", "subject_id", "tenant_id", "task_type", "action", "dataset_ref", "layer", "holdout_ref", "input_digest", "grader_ref", "terminal_ref", "cost", "quality_gate", "security_gate", "error_budget_gate", "trial_digest"}
    for key, item in registry.items():
        item = exact(item, required, set(), f"{path}.{key}")
        for field in required - {"cost"}:
            typed(item[field], str, f"{path}.{key}.{field}")
        number(item["cost"], f"{path}.{key}.cost")
        if item["trial_id"] != key or item["layer"] not in LAYERS or item["cost"] < 0 or not record_digest_valid(item, "trial_digest"):
            raise ValueError(f"{path}.{key} binding enum range or digest invalid")
        for field in ("quality_gate", "security_gate", "error_budget_gate"):
            if item[field] not in {"PASS", "FAIL", "UNKNOWN"}:
                raise ValueError(f"{path}.{key}.{field} enum invalid")
    return registry


def validate_effect_registry(registry: object, path: str, kind: str) -> dict:
    typed(registry, dict, path)
    if kind == "receipt":
        fields = {"receipt_id", "effect_id", "authority_ref", "request_digest", "status", "owner", "issued_at", "record_digest"}
        id_field = "receipt_id"
        statuses = {"APPLIED", "FAILED", "PENDING", "UNKNOWN"}
    else:
        fields = {"readback_id", "effect_id", "receipt_ref", "status", "observer", "observed_at", "record_digest"}
        id_field = "readback_id"
        statuses = {"CONFIRMED", "FAILED", "UNKNOWN"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in fields:
            typed(item[field], str, f"{path}.{key}.{field}")
        parse_time(item["issued_at" if kind == "receipt" else "observed_at"], f"{path}.{key}.time")
        if item[id_field] != key or item["status"] not in statuses or not record_digest_valid(item, "record_digest"):
            raise ValueError(f"{path}.{key} binding enum or digest invalid")
    return registry


def validate_automation_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"manifest_id", "kind", "object_id", "owner", "tenant_id", "task_type", "action", "status", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in fields:
            typed(item[field], str, f"{path}.{key}.{field}")
        if item["manifest_id"] != key or item["kind"] not in {"task", "schedule", "webhook"} or item["status"] not in {"APPROVED", "REVOKED", "UNKNOWN"} or not record_digest_valid(item, "record_digest"):
            raise ValueError(f"{path}.{key} binding enum or digest invalid")
    return registry


def validate_security_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"control_id", "slice", "status", "owner", "test_digest", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in fields:
            typed(item[field], str, f"{path}.{key}.{field}")
        if item["control_id"] != key or item["status"] not in {"ACTIVE", "REVOKED", "UNKNOWN"} or not record_digest_valid(item, "record_digest"):
            raise ValueError(f"{path}.{key} binding enum or digest invalid")
    return registry


def validate_scenario_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"scenario_id", "task_id", "trial_id", "task_type", "dataset_ref", "layer", "holdout_ref", "security_refs", "control_trial_refs", "record_digest"}
    for key, item in registry.items():
        item = exact(item, fields, set(), f"{path}.{key}")
        for field in fields - {"security_refs", "control_trial_refs"}:
            typed(item[field], str, f"{path}.{key}.{field}")
        strings(item["security_refs"], f"{path}.{key}.security_refs")
        strings(item["control_trial_refs"], f"{path}.{key}.control_trial_refs")
        if item["scenario_id"] != key or item["layer"] not in LAYERS or not record_digest_valid(item, "record_digest"):
            raise ValueError(f"{path}.{key} binding enum or digest invalid")
    return registry


def validate_credentials(items: object, path: str) -> list[dict]:
    typed(items, list, path)
    declared = []
    for index, item in enumerate(items):
        p = f"{path}[{index}]"
        item = exact(item, {"credential_id", "owner", "status", "evidence_ref", "restore_enabled", "restore_evidence_ref", "sessions", "delegations"}, set(), p)
        for field in ("credential_id", "owner", "status", "evidence_ref", "restore_evidence_ref"):
            typed(item[field], str, f"{p}.{field}")
        typed(item["restore_enabled"], bool, f"{p}.restore_enabled")
        if item["status"] not in {"ACTIVE", "REVOKED", "EXPIRED", "UNKNOWN"}:
            raise ValueError(f"{p}.status invalid")
        declared.append(item["credential_id"])
        for kind, id_field in (("sessions", "session_id"), ("delegations", "delegation_id")):
            typed(item[kind], list, f"{p}.{kind}")
            for j, row in enumerate(item[kind]):
                row = exact(row, {id_field, "status", "evidence_ref"}, set(), f"{p}.{kind}[{j}]")
                for field in row:
                    typed(row[field], str, f"{p}.{kind}[{j}].{field}")
                if row["status"] not in {"ACTIVE", "REVOKED", "EXPIRED", "UNKNOWN"}:
                    raise ValueError(f"{p}.{kind}[{j}].status invalid")
                declared.append(row[id_field])
    if len(declared) != len(set(declared)):
        raise ValueError(f"{path} IDs must be unique")
    return items


def validate_data(items: object, path: str) -> list[dict]:
    typed(items, list, path)
    ids = []
    for index, item in enumerate(items):
        p = f"{path}[{index}]"
        item = exact(item, {"object_id", "object_version", "owner", "locations", "required_action", "status", "evidence_ref"}, set(), p)
        for field in ("object_id", "object_version", "owner", "required_action", "status", "evidence_ref"):
            typed(item[field], str, f"{p}.{field}")
        strings(item["locations"], f"{p}.locations")
        if item["required_action"] not in {"delete", "retain", "export", "freeze"} or item["status"] not in {"ACTIVE", "DISPOSED", "RETAINED", "EXPORTED", "FROZEN", "RESIDUAL", "UNKNOWN"}:
            raise ValueError(f"{p} enum invalid")
        ids.append(item["object_id"])
    if len(ids) != len(set(ids)):
        raise ValueError(f"{path} object IDs must be unique")
    return items


def validate_retirement(item: object, path: str) -> dict:
    item = exact(item, {"retirement_id", "release_id", "requested", "owner", "decision_ref", "lifecycle_event_ref", "critical_service", "replacement_ref", "handoff_ref", "evidence_refs", "decision_digest"}, set(), path)
    for field in ("retirement_id", "release_id", "owner", "decision_ref", "lifecycle_event_ref", "replacement_ref", "handoff_ref", "decision_digest"):
        typed(item[field], str, f"{path}.{field}")
    for field in ("requested", "critical_service"):
        typed(item[field], bool, f"{path}.{field}")
    refs = exact(item["evidence_refs"], {"admission", "inflight", "runtime", "network", "replacement", "handoff", "residual", "signoff"}, set(), f"{path}.evidence_refs")
    for field in refs:
        typed(refs[field], str, f"{path}.evidence_refs.{field}")
    return item


def validate_retirement_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    kinds = {"admission_stopped", "inflight_reconciled", "runtime_disabled", "network_disabled", "credential_revoked", "session_revoked", "delegation_revoked", "restore_disabled", "data_disposed", "data_retained", "replacement_accepted", "handoff_accepted", "residual_scan", "terminal_signoff"}
    for key, item in registry.items():
        p = f"{path}.{key}"
        item = exact(item, {"evidence_id", "kind", "subject_id", "object_id", "object_version", "status", "owner", "issued_at", "expires_at", "content_digest", "record_digest"}, set(), p)
        for field in item:
            typed(item[field], str, f"{p}.{field}")
        if item["evidence_id"] != key or item["kind"] not in kinds or item["status"] not in VERDICTS:
            raise ValueError(f"{p} binding or enum invalid")
        parse_time(item["issued_at"], f"{p}.issued_at")
        parse_time(item["expires_at"], f"{p}.expires_at")
    return registry


def validate_event_receipt(item: object, path: str) -> dict:
    fields = {"receipt_id", "event_id", "event_type", "release_id", "plan_id", "subject_id", "actor", "authority_ref", "status", "executed_at", "record_digest"}
    item = exact(item, fields, set(), path)
    for field in fields:
        typed(item[field], str, f"{path}.{field}")
    if item["event_type"] not in {"PUBLICATION", "RETIREMENT"} or item["status"] not in {"VERIFIED", "FAILED", "UNKNOWN", "REVOKED"}:
        raise ValueError(f"{path} enum invalid")
    parse_time(item["executed_at"], f"{path}.executed_at")
    if not record_digest_valid(item, "record_digest"):
        raise ValueError(f"{path}.record_digest invalid")
    return item


def validate_event_readback(item: object, path: str) -> dict:
    fields = {"readback_id", "event_id", "receipt_ref", "event_type", "release_id", "plan_id", "subject_id", "observer", "status", "observed_at", "record_digest"}
    item = exact(item, fields, set(), path)
    for field in fields:
        typed(item[field], str, f"{path}.{field}")
    if item["event_type"] not in {"PUBLICATION", "RETIREMENT"} or item["status"] not in {"VERIFIED", "FAILED", "UNKNOWN", "REVOKED"}:
        raise ValueError(f"{path} enum invalid")
    parse_time(item["observed_at"], f"{path}.observed_at")
    if not record_digest_valid(item, "record_digest"):
        raise ValueError(f"{path}.record_digest invalid")
    return item


def validate_publication_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"event_id", "event_type", "release_id", "plan_id", "requested_by", "requested_at", "legal_review_digest", "release_approved_by", "release_approved_at", "release_authority_ref", "plan_approved_by", "plan_approved_at", "plan_authority_ref", "executed_by", "executed_at", "receipt", "readback", "status", "record_digest"}
    for key, item in registry.items():
        p = f"{path}.{key}"
        item = exact(item, fields, set(), p)
        for field in fields - {"receipt", "readback"}:
            typed(item[field], str, f"{p}.{field}")
        if item["event_id"] != key or item["event_type"] != "PUBLICATION" or item["status"] not in {"VERIFIED", "FAILED", "UNKNOWN", "REVOKED"}:
            raise ValueError(f"{p} binding or enum invalid")
        for field in ("requested_at", "release_approved_at", "plan_approved_at", "executed_at"):
            parse_time(item[field], f"{p}.{field}")
        validate_event_receipt(item["receipt"], f"{p}.receipt")
        validate_event_readback(item["readback"], f"{p}.readback")
        if not record_digest_valid(item, "record_digest"):
            raise ValueError(f"{p}.record_digest invalid")
    return registry


def validate_lifecycle_registry(registry: object, path: str) -> dict:
    typed(registry, dict, path)
    fields = {"event_id", "event_type", "retirement_id", "release_id", "plan_id", "requested_by", "requested_at", "plan_approved_by", "plan_approved_at", "plan_authority_ref", "retirement_approved_by", "retirement_approved_at", "retirement_authority_ref", "executed_by", "executed_at", "receipt", "readback", "residual_evidence_ref", "signoff_evidence_ref", "status", "record_digest"}
    for key, item in registry.items():
        p = f"{path}.{key}"
        item = exact(item, fields, set(), p)
        for field in fields - {"receipt", "readback"}:
            typed(item[field], str, f"{p}.{field}")
        if item["event_id"] != key or item["event_type"] != "RETIREMENT" or item["status"] not in {"VERIFIED", "FAILED", "UNKNOWN", "REVOKED"}:
            raise ValueError(f"{p} binding or enum invalid")
        for field in ("requested_at", "plan_approved_at", "retirement_approved_at", "executed_at"):
            parse_time(item[field], f"{p}.{field}")
        validate_event_receipt(item["receipt"], f"{p}.receipt")
        validate_event_readback(item["readback"], f"{p}.readback")
        if not record_digest_valid(item, "record_digest"):
            raise ValueError(f"{p}.record_digest invalid")
    return registry


def validate_state(state: object, path: str = "state") -> dict:
    fields = {"owner_registry", "authority_registry", "release_unit", "migration", "migration_receipt_registry", "backup", "backup_manifest_registry", "restore", "restore_proof_registry", "rollout", "rollout_plan_registry", "trial_ledger", "task_registry", "trial_registry", "dataset_registry", "grader_registry", "terminal_registry", "stop_receipt_registry", "d21", "d21_evidence_registry", "runtime_state", "effect_receipt_registry", "effect_readback_registry", "publication_event_registry", "lifecycle_event_registry", "automation_manifest_registry", "security_control_registry", "scenario_evidence_registry", "rollback", "rollback_receipt_registry", "legal_review", "credentials", "data_inventory", "retirement", "retirement_evidence_registry", "environment_registry", "legal_scope_registry", "holdout_registry"}
    state = exact(state, fields, set(), path)
    validate_owner_registry(state["owner_registry"], f"{path}.owner_registry")
    validate_authorities(state["authority_registry"], f"{path}.authority_registry")
    validate_release(state["release_unit"], f"{path}.release_unit")
    validate_migration(state["migration"], f"{path}.migration")
    validate_receipt_registry(state["migration_receipt_registry"], f"{path}.migration_receipt_registry")
    validate_backup(state["backup"], f"{path}.backup")
    validate_backup_registry(state["backup_manifest_registry"], f"{path}.backup_manifest_registry")
    validate_restore(state["restore"], f"{path}.restore")
    validate_restore_registry(state["restore_proof_registry"], f"{path}.restore_proof_registry")
    validate_rollout(state["rollout"], f"{path}.rollout")
    validate_rollout_plan_registry(state["rollout_plan_registry"], f"{path}.rollout_plan_registry")
    validate_trials(state["trial_ledger"], f"{path}.trial_ledger")
    validate_task_registry(state["task_registry"], f"{path}.task_registry")
    validate_trial_registry(state["trial_registry"], f"{path}.trial_registry")
    validate_dataset_registry(state["dataset_registry"], f"{path}.dataset_registry")
    validate_grader_registry(state["grader_registry"], f"{path}.grader_registry")
    validate_terminal_registry(state["terminal_registry"], f"{path}.terminal_registry")
    validate_stop_registry(state["stop_receipt_registry"], f"{path}.stop_receipt_registry")
    validate_d21(state["d21"], f"{path}.d21")
    validate_d21_registry(state["d21_evidence_registry"], f"{path}.d21_evidence_registry")
    validate_runtime(state["runtime_state"], f"{path}.runtime_state")
    validate_effect_registry(state["effect_receipt_registry"], f"{path}.effect_receipt_registry", "receipt")
    validate_effect_registry(state["effect_readback_registry"], f"{path}.effect_readback_registry", "readback")
    validate_publication_registry(state["publication_event_registry"], f"{path}.publication_event_registry")
    validate_lifecycle_registry(state["lifecycle_event_registry"], f"{path}.lifecycle_event_registry")
    validate_automation_registry(state["automation_manifest_registry"], f"{path}.automation_manifest_registry")
    validate_security_registry(state["security_control_registry"], f"{path}.security_control_registry")
    validate_scenario_registry(state["scenario_evidence_registry"], f"{path}.scenario_evidence_registry")
    validate_rollback(state["rollback"], f"{path}.rollback")
    validate_rollback_registry(state["rollback_receipt_registry"], f"{path}.rollback_receipt_registry")
    validate_legal(state["legal_review"], f"{path}.legal_review")
    validate_environment_registry(state["environment_registry"], f"{path}.environment_registry")
    validate_legal_scope_registry(state["legal_scope_registry"], f"{path}.legal_scope_registry")
    validate_holdout_registry(state["holdout_registry"], f"{path}.holdout_registry")
    validate_credentials(state["credentials"], f"{path}.credentials")
    validate_data(state["data_inventory"], f"{path}.data_inventory")
    validate_retirement(state["retirement"], f"{path}.retirement")
    validate_retirement_registry(state["retirement_evidence_registry"], f"{path}.retirement_evidence_registry")
    evidence_ids = []
    for registry_name, id_field in (("migration_receipt_registry", "receipt_id"), ("backup_manifest_registry", "manifest_id"), ("restore_proof_registry", "proof_id"), ("stop_receipt_registry", "receipt_id"), ("rollback_receipt_registry", "receipt_id"), ("d21_evidence_registry", "evidence_id"), ("retirement_evidence_registry", "evidence_id"), ("publication_event_registry", "event_id"), ("lifecycle_event_registry", "event_id"), ("environment_registry", "environment_id"), ("legal_scope_registry", "legal_scope_id"), ("holdout_registry", "holdout_id"), ("rollout_plan_registry", "plan_id"), ("task_registry", "task_id"), ("trial_registry", "trial_id"), ("dataset_registry", "dataset_id"), ("grader_registry", "grader_id"), ("terminal_registry", "terminal_id"), ("effect_receipt_registry", "receipt_id"), ("effect_readback_registry", "readback_id"), ("automation_manifest_registry", "manifest_id"), ("security_control_registry", "control_id"), ("scenario_evidence_registry", "scenario_id")):
        evidence_ids.extend(record[id_field] for record in state[registry_name].values())
    for registry_name in ("publication_event_registry", "lifecycle_event_registry"):
        for event in state[registry_name].values():
            evidence_ids.extend((event["receipt"]["receipt_id"], event["readback"]["readback_id"]))
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError(f"{path} evidence IDs must be globally unique")
    return state


def frozen_payload(state: dict) -> dict:
    return {key: copy.deepcopy(state[key]) for key in sorted(FROZEN_REGISTRIES)}


def validate_authority_root(root: object, path: str) -> dict:
    root = exact(root, FROZEN_REGISTRIES | {"root_digest"}, set(), path)
    typed(root["root_digest"], str, f"{path}.root_digest")
    payload = {key: root[key] for key in sorted(FROZEN_REGISTRIES)}
    if not digest_valid(root["root_digest"]) or root["root_digest"] != sha256(payload):
        raise ValueError(f"{path}.root_digest invalid")
    # Use the same closed-world validators as the hydrated state.
    validate_owner_registry(root["owner_registry"], f"{path}.owner_registry")
    validate_authorities(root["authority_registry"], f"{path}.authority_registry")
    validate_receipt_registry(root["migration_receipt_registry"], f"{path}.migration_receipt_registry")
    validate_backup_registry(root["backup_manifest_registry"], f"{path}.backup_manifest_registry")
    validate_restore_registry(root["restore_proof_registry"], f"{path}.restore_proof_registry")
    validate_stop_registry(root["stop_receipt_registry"], f"{path}.stop_receipt_registry")
    validate_rollback_registry(root["rollback_receipt_registry"], f"{path}.rollback_receipt_registry")
    validate_d21_registry(root["d21_evidence_registry"], f"{path}.d21_evidence_registry")
    validate_retirement_registry(root["retirement_evidence_registry"], f"{path}.retirement_evidence_registry")
    validate_publication_registry(root["publication_event_registry"], f"{path}.publication_event_registry")
    validate_lifecycle_registry(root["lifecycle_event_registry"], f"{path}.lifecycle_event_registry")
    validate_environment_registry(root["environment_registry"], f"{path}.environment_registry")
    validate_legal_scope_registry(root["legal_scope_registry"], f"{path}.legal_scope_registry")
    validate_holdout_registry(root["holdout_registry"], f"{path}.holdout_registry")
    validate_rollout_plan_registry(root["rollout_plan_registry"], f"{path}.rollout_plan_registry")
    validate_task_registry(root["task_registry"], f"{path}.task_registry")
    validate_trial_registry(root["trial_registry"], f"{path}.trial_registry")
    validate_dataset_registry(root["dataset_registry"], f"{path}.dataset_registry")
    validate_grader_registry(root["grader_registry"], f"{path}.grader_registry")
    validate_terminal_registry(root["terminal_registry"], f"{path}.terminal_registry")
    validate_effect_registry(root["effect_receipt_registry"], f"{path}.effect_receipt_registry", "receipt")
    validate_effect_registry(root["effect_readback_registry"], f"{path}.effect_readback_registry", "readback")
    validate_automation_registry(root["automation_manifest_registry"], f"{path}.automation_manifest_registry")
    validate_security_registry(root["security_control_registry"], f"{path}.security_control_registry")
    validate_scenario_registry(root["scenario_evidence_registry"], f"{path}.scenario_evidence_registry")
    return root


def validate(source: object, authority_root: object) -> dict:
    source = exact(source, {"schema_version", "seed", "now", "environment", "authority_root_digest", "base_state", "scenarios"}, set(), "root")
    if source["schema_version"] != "c21.lifecycle.input.v2.4":
        raise ValueError("unsupported schema_version")
    typed(source["seed"], str, "root.seed")
    parse_time(source["now"], "root.now")
    env = exact(source["environment"], {"mode", "network", "real_credentials", "production_write", "external_side_effects_allowed"}, set(), "root.environment")
    if env != {"mode": "offline_synthetic", "network": False, "real_credentials": False, "production_write": False, "external_side_effects_allowed": False}:
        raise ValueError("offline environment contract changed")
    typed(source["authority_root_digest"], str, "root.authority_root_digest")
    authority_root = validate_authority_root(authority_root, "authority_root")
    if source["authority_root_digest"] != authority_root["root_digest"] or authority_root["root_digest"] != PINNED_AUTHORITY_ROOT_DIGEST:
        raise ValueError("authority root digest is not the independently pinned root")
    validate_state(source["base_state"], "root.base_state")
    if frozen_payload(source["base_state"]) != {key: authority_root[key] for key in sorted(FROZEN_REGISTRIES)}:
        raise ValueError("base_state does not match frozen authority root")
    typed(source["scenarios"], list, "root.scenarios")
    scenario_ids, trial_ids, pairs = [], [], []
    for index, scenario in enumerate(source["scenarios"]):
        p = f"root.scenarios[{index}]"
        scenario = exact(scenario, {"scenario_id", "task_id", "task_type", "trial_id", "layer", "holdout_ref", "case_id", "security_slices", "overrides"}, set(), p)
        for field in ("scenario_id", "task_id", "task_type", "trial_id", "layer", "holdout_ref", "case_id"):
            typed(scenario[field], str, f"{p}.{field}")
        strings(scenario["security_slices"], f"{p}.security_slices")
        typed(scenario["overrides"], dict, f"{p}.overrides")
        if scenario["layer"] not in LAYERS or scenario["case_id"] not in {"CASE-A", "CASE-B", "CASE-C"}:
            raise ValueError(f"{p} enum invalid")
        if scenario["layer"] == "representative_real_world":
            raise ValueError("offline synthetic fixture cannot claim representative real-world")
        if scenario["layer"] != "holdout" and scenario["holdout_ref"] != "NONE":
            raise ValueError(f"{p} non-holdout scenario cannot claim holdout lineage")
        scenario_ids.append(scenario["scenario_id"]); trial_ids.append(scenario["trial_id"]); pairs.append((scenario["task_id"], scenario["trial_id"]))
    if len(scenario_ids) != len(set(scenario_ids)) or len(trial_ids) != len(set(trial_ids)) or len(pairs) != len(set(pairs)):
        raise ValueError("scenario, trial, and task/trial IDs must be unique")
    source = copy.deepcopy(source)
    source["authority_root"] = copy.deepcopy(authority_root)
    for scenario in source["scenarios"]:
        evidence = authority_root["scenario_evidence_registry"].get(scenario["scenario_id"])
        errors = []
        if not evidence or not record_digest_valid(evidence, "record_digest"):
            errors.append("SCENARIO_EVIDENCE_MISSING")
            derived = {"task_id": "UNKNOWN", "trial_id": "UNKNOWN", "task_type": "UNKNOWN", "layer": "training", "holdout_ref": "NONE", "security_slices": []}
        else:
            dataset = authority_root["dataset_registry"].get(evidence["dataset_ref"])
            controls = [authority_root["security_control_registry"].get(ref) for ref in evidence["security_refs"]]
            derived = {
                "task_id": evidence["task_id"], "trial_id": evidence["trial_id"], "task_type": evidence["task_type"],
                "layer": dataset["layer"] if dataset else "training",
                "holdout_ref": dataset["holdout_ref"] if dataset else "NONE",
                "security_slices": [item["slice"] for item in controls if item],
            }
            if not dataset or dataset["status"] != "ACTIVE": errors.append("SCENARIO_DATASET_EVIDENCE_INVALID")
            if any(item is None or item["status"] != "ACTIVE" for item in controls): errors.append("SCENARIO_SECURITY_EVIDENCE_INVALID")
            if any(ref not in authority_root["trial_registry"] for ref in evidence["control_trial_refs"]): errors.append("SCENARIO_CONTROL_TRIAL_MISSING")
        for field in ("task_id", "trial_id", "task_type", "layer", "holdout_ref", "security_slices"):
            if scenario[field] != derived[field]: errors.append(f"SCENARIO_{field.upper()}_EVIDENCE_MISMATCH")
        scenario["_evidence_errors"] = sorted(set(errors))
        scenario["_derived_metadata"] = derived
    return source


def owner_active(state: dict, principal: str, now: datetime) -> bool:
    return any(record["principal"] == principal and record["kind"] in {"human", "legal_entity"} and record["status"] == "ACTIVE" and parse_time(record["valid_from"], "owner.valid_from") <= now < parse_time(record["expires_at"], "owner.expires_at") for record in state["owner_registry"].values())


def role_owner_active(state: dict, role: str, principal: str, now: datetime) -> bool:
    record = state["owner_registry"].get(role)
    return bool(record and record["principal"] == principal and record["kind"] in {"human", "legal_entity"} and record["status"] == "ACTIVE" and parse_time(record["valid_from"], "owner.valid_from") <= now < parse_time(record["expires_at"], "owner.expires_at"))


def authority_valid_at(record: dict | None, moment: datetime, **bindings: str) -> bool:
    return bool(
        record
        and record_digest_valid(record, "authority_digest")
        and active_at(record, moment)
        and parse_time(record["issued_at"], "authority.issued_at") <= moment
        and all(record.get(key) == value for key, value in bindings.items())
    )


def authority_valid(record: dict | None, now: datetime, **bindings: str) -> bool:
    return authority_valid_at(record, now, **bindings)


def append_status(status: str, fail: list[str], review: list[str], fail_code: str, review_code: str) -> None:
    if status == "FAIL": fail.append(fail_code)
    elif status == "REVIEW_REQUIRED": review.append(review_code)


def evaluate(source: dict, state: dict, scenario: dict | None = None) -> tuple[str, list[str], dict, int]:
    fail, review = [], []
    if scenario is None and len(source.get("scenarios", [])) == 1:
        scenario = source["scenarios"][0]
    if scenario is not None:
        fail.extend(scenario.get("_evidence_errors", []))
    now = parse_time(source["now"], "root.now")
    authority_payload = {key: source["authority_root"][key] for key in sorted(FROZEN_REGISTRIES)}
    if source["authority_root"]["root_digest"] != sha256(authority_payload) or frozen_payload(state) != authority_payload:
        fail.append("FROZEN_AUTHORITY_ROOT_MISMATCH")
    if any(record["kind"] not in {"human", "legal_entity"} or record["status"] != "ACTIVE" or not (parse_time(record["valid_from"], "owner.valid_from") <= now < parse_time(record["expires_at"], "owner.expires_at")) for record in state["owner_registry"].values()):
        fail.append("ACCOUNTABLE_OWNER_INVALID")

    release = state["release_unit"]
    digest_fields = ("build_digest", "contract_digest", "policy_digest", "model_params_digest", "tool_manifest_digest", "skill_manifest_digest", "dependency_lock_digest")
    if any(not digest_valid(release[field]) for field in digest_fields) or "latest" in release["build_ref"] or "latest" in release["model_ref"]:
        fail.append("RELEASE_COMPONENT_DIGEST_INVALID")
    if not record_digest_valid(release, "release_digest"):
        fail.append("RELEASE_CANONICAL_DIGEST_INVALID")
    if len({release["proposer"], release["approver"], release["operator"], release["acceptor"]}) < 3:
        fail.append("SEGREGATION_OF_DUTIES_INVALID")
    if not (role_owner_active(state, "capability", release["proposer"], now) and role_owner_active(state, "security_risk", release["approver"], now) and role_owner_active(state, "operations", release["operator"], now) and role_owner_active(state, "business", release["acceptor"], now)):
        fail.append("RELEASE_OWNER_ROLE_INVALID")
    approved_plan = state["rollout_plan_registry"].get(release["rollout_plan_ref"])
    approval = state["authority_registry"].get(release["approval_ref"])
    approved_plan_digest = approved_plan["plan_digest"] if approved_plan else "NONE"
    if not approved_plan or not authority_valid(approval, now, actor=release["approver"], action="approve_release", subject_type="release", subject_id=release["release_id"], object_digest=release["release_digest"], scope=approved_plan_digest, policy_version=release["policy_version"]) or not owner_active(state, release["approver"], now):
        fail.append("RELEASE_APPROVAL_BINDING_INVALID")

    publication = state["publication_event_registry"].get(release["publication_event_ref"])
    publication_executed_at = None
    if not publication or not approved_plan or not record_digest_valid(publication, "record_digest"):
        fail.append("PUBLICATION_EVENT_INVALID")
    else:
        publication_executed_at = parse_time(publication["executed_at"], "publication.executed_at")
        requested_at = parse_time(publication["requested_at"], "publication.requested_at")
        release_approved_at = parse_time(publication["release_approved_at"], "publication.release_approved_at")
        plan_approved_at = parse_time(publication["plan_approved_at"], "publication.plan_approved_at")
        legal_reviewed_at = parse_time(state["legal_review"]["reviewed_at"], "legal.reviewed_at")
        receipt = publication["receipt"]
        readback = publication["readback"]
        receipt_at = parse_time(receipt["executed_at"], "publication.receipt.executed_at")
        readback_at = parse_time(readback["observed_at"], "publication.readback.observed_at")
        plan_approval = state["authority_registry"].get(publication["plan_authority_ref"])
        bindings_ok = (
            publication["event_type"] == "PUBLICATION"
            and publication["release_id"] == release["release_id"]
            and publication["plan_id"] == release["rollout_plan_ref"]
            and publication["requested_by"] == release["proposer"]
            and publication["legal_review_digest"] == sha256(state["legal_review"])
            and publication["release_approved_by"] == release["approver"]
            and publication["release_authority_ref"] == release["approval_ref"]
            and publication["plan_approved_by"] == approved_plan["owner"]
            and publication["plan_authority_ref"] == approved_plan["approval_ref"]
            and publication["executed_by"] == release["operator"]
            and receipt["event_id"] == publication["event_id"]
            and receipt["event_type"] == "PUBLICATION"
            and receipt["release_id"] == release["release_id"]
            and receipt["plan_id"] == approved_plan["plan_id"]
            and receipt["subject_id"] == release["release_id"]
            and receipt["actor"] == release["operator"]
            and receipt["authority_ref"] == release["approval_ref"]
            and receipt_at == publication_executed_at
            and readback["event_id"] == publication["event_id"]
            and readback["receipt_ref"] == receipt["receipt_id"]
            and readback["event_type"] == "PUBLICATION"
            and readback["release_id"] == release["release_id"]
            and readback["plan_id"] == approved_plan["plan_id"]
            and readback["subject_id"] == release["release_id"]
            and readback["observer"] == release["acceptor"]
            and readback["observer"] != publication["executed_by"]
        )
        if not bindings_ok:
            fail.append("PUBLICATION_EVENT_BINDING_INVALID")
        if not (requested_at <= legal_reviewed_at <= release_approved_at <= publication_executed_at and requested_at <= legal_reviewed_at <= plan_approved_at <= publication_executed_at and receipt_at <= readback_at <= now):
            fail.append("PUBLICATION_EVENT_SEQUENCE_INVALID")
        if not (parse_time(approved_plan["starts_at"], "publication.plan.starts_at") <= publication_executed_at < parse_time(approved_plan["expires_at"], "publication.plan.expires_at")):
            fail.append("PUBLICATION_EXECUTION_OUTSIDE_PLAN_WINDOW")
        if not authority_valid_at(approval, publication_executed_at, actor=release["approver"], action="approve_release", subject_type="release", subject_id=release["release_id"], object_digest=release["release_digest"], scope=approved_plan["plan_digest"], policy_version=release["policy_version"]):
            fail.append("PUBLICATION_RELEASE_AUTHORITY_INVALID")
        elif parse_time(approval["issued_at"], "publication.release_authority.issued_at") > release_approved_at:
            fail.append("PUBLICATION_RELEASE_APPROVAL_TIME_INVALID")
        if not authority_valid_at(plan_approval, publication_executed_at, actor=approved_plan["owner"], action="approve_rollout_plan", subject_type="rollout", subject_id=approved_plan["plan_id"], object_digest=approved_plan["plan_digest"], scope=approved_plan["scope_digest"], policy_version=release["policy_version"]):
            fail.append("PUBLICATION_PLAN_AUTHORITY_INVALID")
        elif parse_time(plan_approval["issued_at"], "publication.plan_authority.issued_at") > plan_approved_at:
            fail.append("PUBLICATION_PLAN_APPROVAL_TIME_INVALID")
        if publication["status"] == "UNKNOWN" or receipt["status"] == "UNKNOWN" or readback["status"] == "UNKNOWN":
            review.append("PUBLICATION_TERMINAL_UNKNOWN")
        elif publication["status"] != "VERIFIED" or receipt["status"] != "VERIFIED" or readback["status"] != "VERIFIED":
            fail.append("PUBLICATION_EXECUTION_FAILED")

    migration = state["migration"]
    if not record_digest_valid(migration, "migration_digest"):
        fail.append("MIGRATION_CANONICAL_DIGEST_INVALID")
    if not role_owner_active(state, "technical", migration["owner"], now):
        fail.append("MIGRATION_OWNER_ROLE_INVALID")
    if migration["irreversible_steps"]:
        irreversible_approval = state["authority_registry"].get(migration["irreversible_approval_ref"])
        if migration["reentrant"] or migration["recovery_strategy"] != "FORWARD_ONLY" or not authority_valid(irreversible_approval, now, actor=release["approver"], action="approve_irreversible_migration", subject_type="migration", subject_id=migration["migration_id"], object_digest=migration["migration_digest"], scope=state["rollout"]["scope"], policy_version=release["policy_version"]):
            fail.append("IRREVERSIBLE_MIGRATION_CONTROL_INVALID")
    elif migration["irreversible_approval_ref"] != "NONE" or migration["recovery_strategy"] != "ROLLBACK":
        fail.append("MIGRATION_RECOVERY_CONTRACT_INVALID")
    if migration["release_id"] != release["release_id"] or migration["to_schema"] != release["state_schema"] or not migration["candidate_reads_from"] or not migration["candidate_writes_to"]:
        fail.append("SCHEMA_COMPATIBILITY_FAILED")
    receipt = state["migration_receipt_registry"].get(migration["receipt_ref"])
    if not receipt or not record_digest_valid(receipt, "record_digest"):
        fail.append("MIGRATION_RECEIPT_INVALID")
    elif not (receipt["subject_type"] == "migration" and receipt["subject_id"] == migration["migration_id"] and receipt["release_id"] == release["release_id"] and receipt["from_schema"] == migration["from_schema"] and receipt["to_schema"] == migration["to_schema"] and receipt["migration_digest"] == migration["migration_digest"] and receipt["owner"] == migration["owner"] and role_owner_active(state, "technical", receipt["owner"], now) and parse_time(receipt["issued_at"], "migration_receipt.issued_at") <= now < parse_time(receipt["expires_at"], "migration_receipt.expires_at")):
        fail.append("MIGRATION_RECEIPT_BINDING_INVALID")
    elif receipt["status"] == "UNKNOWN" or migration["status"] == "UNKNOWN" or migration["dry_run"] == "REVIEW_REQUIRED":
        review.append("MIGRATION_TERMINAL_UNKNOWN")
    elif receipt["status"] != "VERIFIED" or migration["status"] != "VERIFIED" or migration["dry_run"] != "PASS":
        fail.append("MIGRATION_FAILED")

    backup = state["backup"]
    manifest = state["backup_manifest_registry"].get(backup["manifest_ref"])
    if not manifest or not record_digest_valid(manifest, "manifest_digest"):
        fail.append("BACKUP_MANIFEST_INVALID")
    else:
        if manifest["backup_id"] != backup["backup_id"] or manifest["release_id"] != release["release_id"] or backup["release_id"] != release["release_id"] or manifest["access_owner"] != backup["owner"] or not role_owner_active(state, "data", backup["owner"], now):
            fail.append("BACKUP_MANIFEST_BINDING_INVALID")
        if not REQUIRED_COVERAGE.issubset(set(manifest["covered"])) or set(manifest["covered"]) & set(manifest["excluded"]) or not manifest["consistent_snapshot"] or manifest["integrity"] != "PASS" or not manifest["encrypted"]:
            fail.append("BACKUP_COVERAGE_OR_INTEGRITY_FAILED")
        if not digest_valid(manifest["archive_digest"]) or not (parse_time(manifest["created_at"], "backup.created_at") <= now < parse_time(manifest["expires_at"], "backup.expires_at")):
            fail.append("BACKUP_ARCHIVE_OR_TIME_INVALID")

    restore = state["restore"]
    proof = state["restore_proof_registry"].get(restore["proof_ref"])
    if not proof or not record_digest_valid(proof, "proof_digest"):
        fail.append("RESTORE_PROOF_INVALID")
    elif not manifest or not (proof["restore_id"] == restore["restore_id"] and proof["backup_id"] == backup["backup_id"] == restore["backup_id"] and proof["release_id"] == release["release_id"] == restore["release_id"] and proof["archive_digest"] == manifest["archive_digest"] and proof["owner"] == restore["owner"] and role_owner_active(state, "technical", restore["owner"], now) and parse_time(proof["issued_at"], "restore.issued_at") <= now < parse_time(proof["expires_at"], "restore.expires_at")):
        fail.append("RESTORE_PROOF_BINDING_INVALID")
    else:
        environment = state["environment_registry"].get(proof["environment_ref"])
        if not environment or not record_digest_valid(environment, "record_digest") or environment["kind"] != "isolated_restore" or environment["mode"] != source["environment"]["mode"] or environment["status"] != "ACTIVE" or not role_owner_active(state, "technical", environment["owner"], now) or not (parse_time(environment["issued_at"], "environment.issued_at") <= now < parse_time(environment["expires_at"], "environment.expires_at")):
            fail.append("RESTORE_ENVIRONMENT_AUTHORITY_INVALID")
        statuses = {proof[field] for field in ("schema_integrity", "identity_tenant_check", "task_replay", "delivery_check", "environment_terminal")}
        if "FAIL" in statuses or not proof["hash_verified"] or not proof["credentials_rebuilt"]: fail.append("RESTORE_PROOF_FAILED")
        elif "REVIEW_REQUIRED" in statuses: review.append("RESTORE_PROOF_UNKNOWN")
        if proof["rpo_minutes"] > restore["target_rpo_minutes"] or proof["rto_minutes"] > restore["target_rto_minutes"]: fail.append("RESTORE_OBJECTIVE_MISSED")

    d21 = state["d21"]
    for face in ("technical", "delivery", "business", "environment"):
        declared = d21[face]; ev = state["d21_evidence_registry"].get(declared["evidence_ref"])
        if not ev or not record_digest_valid(ev, "record_digest"):
            fail.append(f"D21_{face.upper()}_EVIDENCE_INVALID"); continue
        binding_ok = ev["face"] == face and ev["task_id"] == d21["task_id"] and ev["release_id"] == release["release_id"] == d21["release_id"] and ev["object_id"] == d21["object_id"] and ev["object_version"] == d21["object_version"] and ev["object_digest"] == release["release_digest"] and ev["status"] == declared["status"] and owner_active(state, ev["owner"], now) and parse_time(ev["observed_at"], "d21.observed_at") <= now < parse_time(ev["expires_at"], "d21.expires_at")
        if not binding_ok: fail.append(f"D21_{face.upper()}_EVIDENCE_BINDING_INVALID")
        else: append_status(declared["status"], fail, review, f"D21_{face.upper()}_FAILED", f"D21_{face.upper()}_UNKNOWN")

    rollout = state["rollout"]
    plan = state["rollout_plan_registry"].get(rollout["plan_id"])
    plan_payload = {key: rollout[key] for key in ("plan_id", "release_id", "stage", "scope", "scope_digest", "allowed_tenants", "allowed_tasks", "allowed_actions", "candidate_permissions", "baseline_permissions", "min_trials", "max_trials", "max_cost", "starts_at", "expires_at", "environment_ref", "owner")}
    if not plan or not record_digest_valid(plan, "plan_digest") or rollout["plan_digest"] != plan["plan_digest"] or plan_payload != {key: plan[key] for key in plan_payload}:
        fail.append("ROLLOUT_PLAN_AUTHORITY_MISMATCH")
    plan_environment = state["environment_registry"].get(rollout["environment_ref"])
    if not plan_environment or plan_environment["kind"] != "offline_runtime" or plan_environment["mode"] != source["environment"]["mode"] or plan_environment["status"] != "ACTIVE" or not role_owner_active(state, "operations", plan_environment["owner"], now):
        fail.append("ROLLOUT_PLAN_ENVIRONMENT_INVALID")
    if rollout["release_id"] != release["release_id"]: fail.append("ROLLOUT_RELEASE_BINDING_INVALID")
    if plan:
        plan_approval = state["authority_registry"].get(plan["approval_ref"])
        if not authority_valid(plan_approval, now, actor=rollout["owner"], action="approve_rollout_plan", subject_type="rollout", subject_id=plan["plan_id"], object_digest=plan["plan_digest"], scope=plan["scope_digest"], policy_version=release["policy_version"]):
            fail.append("ROLLOUT_PLAN_APPROVAL_INVALID")
    if not role_owner_active(state, "operations", rollout["owner"], now): fail.append("ROLLOUT_OWNER_ROLE_INVALID")
    if not (parse_time(rollout["starts_at"], "rollout.starts_at") <= now < parse_time(rollout["expires_at"], "rollout.expires_at")): fail.append("ROLLOUT_WINDOW_INVALID")
    if rollout["min_trials"] <= 0 or rollout["max_trials"] < rollout["min_trials"] or rollout["max_cost"] <= 0: fail.append("ROLLOUT_BUDGET_INVALID")
    expected_scope_digest = sha256({"scope": rollout["scope"], "allowed_tenants": rollout["allowed_tenants"], "allowed_tasks": rollout["allowed_tasks"], "allowed_actions": rollout["allowed_actions"]})
    if not digest_valid(rollout["scope_digest"]) or rollout["scope_digest"] != expected_scope_digest: fail.append("ROLLOUT_SCOPE_DIGEST_INVALID")
    if not rollout["allowed_tenants"] or not rollout["allowed_tasks"] or not rollout["allowed_actions"]: fail.append("ROLLOUT_SCOPE_EMPTY")
    if source["environment"]["mode"] == "offline_synthetic" and rollout["stage"] == "PRODUCTION": fail.append("OFFLINE_PRODUCTION_CLAIM_FORBIDDEN")
    if not set(rollout["candidate_permissions"]).issubset(set(rollout["baseline_permissions"])): fail.append("CANARY_PERMISSION_EXPANSION")
    trials = state["trial_ledger"]; total_cost = sum(item["cost"] for item in trials)
    if len(trials) < rollout["min_trials"]: fail.append("TRIAL_LEDGER_BELOW_MINIMUM")
    if any(item["cost"] < 0 for item in trials): fail.append("TRIAL_COST_INVALID")
    budget_exceeded = len(trials) > rollout["max_trials"] or total_cost > rollout["max_cost"]
    if budget_exceeded: fail.append("ROLLOUT_BUDGET_EXCEEDED")
    if any(item["release_id"] != release["release_id"] for item in trials): fail.append("TRIAL_RELEASE_BINDING_INVALID")
    if any(item["tenant_id"] not in rollout["allowed_tenants"] or item["task_type"] not in rollout["allowed_tasks"] or item["action"] not in rollout["allowed_actions"] for item in trials): fail.append("TRIAL_SCOPE_BINDING_INVALID")
    for item in trials:
        frozen_trial = state["trial_registry"].get(item["trial_id"])
        task = state["task_registry"].get(item["task_id"])
        dataset = state["dataset_registry"].get(item["dataset_ref"])
        grader = state["grader_registry"].get(item["grader_ref"])
        terminal = state["terminal_registry"].get(item["terminal_ref"])
        if not frozen_trial or frozen_trial != item or not record_digest_valid(item, "trial_digest"):
            fail.append("TRIAL_REGISTRY_BINDING_INVALID")
        if not task or task["subject_id"] != item["subject_id"] or task["tenant_id"] != item["tenant_id"] or task["task_type"] != item["task_type"] or task["action"] != item["action"] or task["input_digest"] != item["input_digest"] or task["status"] not in {"ACTIVE", "COMPLETE"}:
            fail.append("TASK_REGISTRY_BINDING_INVALID")
        if not dataset or dataset["release_id"] != release["release_id"] or dataset["layer"] != item["layer"] or dataset["holdout_ref"] != item["holdout_ref"] or dataset["status"] != "ACTIVE":
            fail.append("DATASET_REGISTRY_BINDING_INVALID")
        if not grader or grader["status"] != "ACTIVE" or not role_owner_active(state, "capability", grader["owner"], now):
            fail.append("GRADER_REGISTRY_BINDING_INVALID")
        if not terminal or terminal["trial_id"] != item["trial_id"] or terminal["status"] not in {"COMPLETED", "FAILED", "UNKNOWN"} or not role_owner_active(state, "operations", terminal["owner"], now) or parse_time(terminal["observed_at"], "terminal.observed_at") > now:
            fail.append("TRIAL_TERMINAL_BINDING_INVALID")
        elif terminal["status"] == "FAILED": fail.append("TRIAL_EXECUTION_FAILED")
        elif terminal["status"] == "UNKNOWN": review.append("TRIAL_EXECUTION_UNKNOWN")
        if item["layer"] == "representative_real_world":
            fail.append("OFFLINE_REAL_WORLD_TRIAL_FORBIDDEN")
        if item["layer"] == "holdout":
            holdout = state["holdout_registry"].get(item["holdout_ref"])
            if not holdout or not record_digest_valid(holdout, "record_digest") or holdout["task_type"] != item["task_type"] or holdout["release_id"] != release["release_id"] or not digest_valid(holdout["lineage_digest"]) or not digest_valid(holdout["isolation_manifest_digest"]) or holdout["grader_ref"] in {"", "NONE", "self"} or holdout["gold_exposed"] or holdout["contamination_status"] != "CLEAN" or holdout["status"] != "ACTIVE" or not role_owner_active(state, "capability", holdout["owner"], now) or not (parse_time(holdout["issued_at"], "holdout.issued_at") <= now < parse_time(holdout["expires_at"], "holdout.expires_at")):
                fail.append("HOLDOUT_LINEAGE_OR_ISOLATION_INVALID")
        elif item["holdout_ref"] != "NONE":
            fail.append("NON_HOLDOUT_REFERENCE_INVALID")
    gates = [rollout["quality_gate"], rollout["security_gate"], rollout["error_budget_gate"]] + [item[field] for item in trials for field in ("quality_gate", "security_gate", "error_budget_gate")]
    gate_failed, gate_unknown = "FAIL" in gates, "UNKNOWN" in gates
    if gate_failed: fail.append("CANARY_HARD_GATE_FAILED")
    elif gate_unknown: review.append("CANARY_GATE_UNKNOWN")
    stop_required = gate_failed or budget_exceeded or rollout["stop_triggered"]
    if stop_required and not rollout["stop_triggered"]: fail.append("REQUIRED_STOP_NOT_TRIGGERED")
    if rollout["stop_triggered"]:
        stop = state["stop_receipt_registry"].get(rollout["stop_receipt_ref"])
        if not stop or not record_digest_valid(stop, "record_digest"): fail.append("STOP_RECEIPT_INVALID")
        elif not (stop["release_id"] == release["release_id"] and stop["plan_id"] == rollout["plan_id"] and stop["owner"] == rollout["owner"] and role_owner_active(state, "operations", stop["owner"], now) and stop["active_release"] == state["runtime_state"]["active_release"] and 0 <= (now - parse_time(stop["issued_at"], "stop.issued_at")).total_seconds() <= 300 and now < parse_time(stop["expires_at"], "stop.expires_at")): fail.append("STOP_RECEIPT_BINDING_OR_TIME_INVALID")
        elif stop["status"] == "UNKNOWN": review.append("STOP_RECEIPT_UNKNOWN")
        elif stop["status"] != "VERIFIED" or stop["admission"] != "PAUSED" or stop["queue"] != "CLEAR" or stop["workers"] != "STOPPED": fail.append("STOP_READBACK_NOT_VERIFIED")

    runtime = state["runtime_state"]
    expected_active_release = state["rollback"]["target_release"] if state["rollback"]["requested"] and state["rollback"]["status"] == "ROLLED_BACK" else release["release_id"]
    if runtime["active_release"] != expected_active_release: fail.append("ACTIVE_RELEASE_MISMATCH")
    for kind in ("tasks", "schedules", "webhooks"):
        for item in runtime[kind]:
            if not role_owner_active(state, "operations", item["owner"], now): fail.append("RUNTIME_OWNER_ROLE_INVALID")
            if item["tenant_id"] not in rollout["allowed_tenants"] or item["task_type"] not in rollout["allowed_tasks"] or item["action"] not in rollout["allowed_actions"]: fail.append("RUNTIME_SCOPE_BINDING_INVALID")
            manifest = state["automation_manifest_registry"].get(item.get("manifest_ref", "NONE"))
            object_id = item[{"tasks": "task_id", "schedules": "schedule_id", "webhooks": "webhook_id"}[kind]]
            expected_kind = {"tasks": "task", "schedules": "schedule", "webhooks": "webhook"}[kind]
            if not manifest or manifest["kind"] != expected_kind or manifest["object_id"] != object_id or manifest["owner"] != item["owner"] or manifest["tenant_id"] != item["tenant_id"] or manifest["task_type"] != item["task_type"] or manifest["action"] != item["action"] or manifest["status"] != "APPROVED":
                fail.append("AUTOMATION_MANIFEST_BINDING_INVALID")
    external_count = 0
    for effect in runtime["effect_ledger"]:
        external_count += int(effect["external"] and effect["status"] == "APPLIED")
        if not role_owner_active(state, "operations", effect["owner"], now): fail.append("EFFECT_OWNER_ROLE_INVALID")
        if effect["tenant_id"] not in rollout["allowed_tenants"] or effect["task_type"] not in rollout["allowed_tasks"] or effect["action"] not in rollout["allowed_actions"]: fail.append("EFFECT_SCOPE_BINDING_INVALID")
        request_digest = sha256({key: effect[key] for key in ("effect_id", "external", "owner", "tenant_id", "task_type", "action")})
        effect_authority = state["authority_registry"].get(effect.get("authority_ref", "NONE"))
        receipt = state["effect_receipt_registry"].get(effect.get("receipt_ref", "NONE"))
        readback = state["effect_readback_registry"].get(effect.get("readback_ref", "NONE"))
        if not authority_valid(effect_authority, now, actor=effect["owner"], action="apply_effect", subject_type="effect", subject_id=effect["effect_id"], object_digest=request_digest, scope=rollout["scope_digest"], policy_version=release["policy_version"]): fail.append("EFFECT_AUTHORITY_INVALID")
        if not receipt or receipt["effect_id"] != effect["effect_id"] or receipt["authority_ref"] != effect.get("authority_ref") or receipt["request_digest"] != request_digest or receipt["status"] != effect["status"] or receipt["owner"] != effect["owner"] or parse_time(receipt["issued_at"], "effect.receipt") > now: fail.append("EFFECT_RECEIPT_INVALID")
        if not readback or not receipt or readback["effect_id"] != effect["effect_id"] or readback["receipt_ref"] != receipt["receipt_id"] or readback["observer"] == effect["owner"] or not owner_active(state, readback["observer"], now) or parse_time(readback["observed_at"], "effect.readback") < parse_time(receipt["issued_at"], "effect.receipt") or readback["status"] == "FAILED": fail.append("EFFECT_READBACK_INVALID")
        if effect["status"] == "FAILED": fail.append("EFFECT_FAILED")
        elif effect["status"] in {"UNKNOWN", "PENDING"} or (readback and readback["status"] == "UNKNOWN"): review.append("EFFECT_TERMINAL_UNKNOWN")
        if effect["external"] and effect["status"] == "APPLIED" and (rollout["stage"] == "SHADOW" or not source["environment"]["external_side_effects_allowed"]): fail.append("EXTERNAL_EFFECT_CONTRACT_VIOLATED")
    if rollout["stage"] in {"PAUSED", "RETIRED", "ROLLED_BACK"}:
        live_tasks = any(item["state"] in {"QUEUED", "ACTIVE"} for item in runtime["tasks"])
        live_automation = any(item["state"] == "ACTIVE" for item in runtime["schedules"] + runtime["webhooks"])
        if runtime["admission"] not in {"PAUSED", "CLOSED"} or runtime["queue"] != "CLEAR" or runtime["workers"] != "STOPPED" or live_tasks or live_automation:
            fail.append("LIFECYCLE_TERMINAL_RUNTIME_INCONSISTENT")
    elif rollout["stage"] in {"CANARY", "LIMITED", "PRODUCTION"}:
        expected_admission = {"CANARY": "OPEN_CANARY", "LIMITED": "OPEN_LIMITED", "PRODUCTION": "OPEN_PRODUCTION"}[rollout["stage"]]
        if runtime["admission"] != expected_admission:
            fail.append("ROLLOUT_ADMISSION_STAGE_MISMATCH")

    rollback = state["rollback"]
    if rollback["requested"]:
        if rollback["status"] in {"ROLLBACK_PENDING", "UNKNOWN"}: review.append("ROLLBACK_TERMINAL_UNKNOWN")
        elif rollback["status"] == "ROLLED_BACK":
            receipt = state["rollback_receipt_registry"].get(rollback["receipt_ref"])
            if not receipt or not record_digest_valid(receipt, "record_digest"):
                fail.append("ROLLBACK_RECEIPT_INVALID")
            elif not (receipt["release_id"] == release["release_id"] and receipt["target_release"] == rollback["target_release"] and receipt["owner"] == rollout["owner"] and role_owner_active(state, "operations", receipt["owner"], now) and receipt["active_release"] == rollback["target_release"] and receipt["code_config_reverted"] == rollback["code_config_reverted"] and receipt["old_runtime_reads_current_schema"] == rollback["old_runtime_reads_current_schema"] and receipt["external_effects_reconciled"] == rollback["external_effects_reconciled"] and receipt["compensation_status"] == rollback["compensation_status"] and 0 <= (now - parse_time(receipt["issued_at"], "rollback_receipt.issued_at")).total_seconds() <= 300 and now < parse_time(receipt["expires_at"], "rollback_receipt.expires_at")):
                fail.append("ROLLBACK_RECEIPT_BINDING_OR_TIME_INVALID")
            elif receipt["status"] == "UNKNOWN":
                review.append("ROLLBACK_RECEIPT_UNKNOWN")
            elif receipt["status"] != "VERIFIED" or receipt["admission"] != "PAUSED" or receipt["queue"] != "CLEAR" or receipt["workers"] != "STOPPED":
                fail.append("ROLLBACK_READBACK_NOT_VERIFIED")
            if runtime["active_release"] != rollback["target_release"] or receipt and receipt.get("active_release") != runtime["active_release"]:
                fail.append("ROLLBACK_ACTIVE_RELEASE_MISMATCH")
            if not rollback["code_config_reverted"] or not rollback["old_runtime_reads_current_schema"] or (external_count and (not rollback["external_effects_reconciled"] or rollback["compensation_status"] != "COMPLETE")):
                fail.append("ROLLBACK_FALSE_COMPLETION")

    legal = state["legal_review"]
    if not role_owner_active(state, "security_risk", legal["reviewer"], now) or not (parse_time(legal["reviewed_at"], "legal.reviewed_at") <= now < parse_time(legal["expires_at"], "legal.expires_at")): fail.append("LEGAL_REVIEW_AUTHORITY_OR_TIME_INVALID")
    elif legal["status"] == "FAIL" or "REJECTED" in {legal["data_use"], legal["license"], legal["privacy"]}: fail.append("LEGAL_REVIEW_FAILED")
    elif legal["status"] == "REVIEW_REQUIRED" or "UNKNOWN" in {legal["data_use"], legal["license"], legal["privacy"]}: review.append("PROFESSIONAL_REVIEW_REQUIRED")
    legal_scope = state["legal_scope_registry"].get(legal["legal_scope_ref"])
    restore_environment_ref = proof["environment_ref"] if proof else "NONE"
    if not legal_scope or not record_digest_valid(legal_scope, "record_digest") or legal_scope["status"] != "ACTIVE" or legal_scope["owner"] != legal["reviewer"] or not role_owner_active(state, "security_risk", legal_scope["owner"], now) or restore_environment_ref not in legal_scope["allowed_environment_refs"] or not (parse_time(legal_scope["issued_at"], "legal_scope.issued_at") <= now < parse_time(legal_scope["expires_at"], "legal_scope.expires_at")):
        fail.append("LEGAL_SCOPE_AUTHORITY_INVALID")

    retirement = state["retirement"]
    if retirement["requested"]:
        if not role_owner_active(state, "business", retirement["owner"], now): fail.append("RETIREMENT_OWNER_ROLE_INVALID")
        if not record_digest_valid(retirement, "decision_digest"): fail.append("RETIREMENT_DECISION_DIGEST_INVALID")
        lifecycle = state["lifecycle_event_registry"].get(retirement["lifecycle_event_ref"])
        lifecycle_executed_at = None
        retired_plan = state["rollout_plan_registry"].get(state["rollout"]["plan_id"])
        decision_rec = state["authority_registry"].get(retirement["decision_ref"])
        if not lifecycle or not retired_plan or not record_digest_valid(lifecycle, "record_digest"):
            fail.append("RETIREMENT_LIFECYCLE_EVENT_INVALID")
        else:
            lifecycle_executed_at = parse_time(lifecycle["executed_at"], "retirement.event.executed_at")
            requested_at = parse_time(lifecycle["requested_at"], "retirement.event.requested_at")
            plan_approved_at = parse_time(lifecycle["plan_approved_at"], "retirement.event.plan_approved_at")
            retirement_approved_at = parse_time(lifecycle["retirement_approved_at"], "retirement.event.retirement_approved_at")
            event_receipt = lifecycle["receipt"]
            event_readback = lifecycle["readback"]
            receipt_at = parse_time(event_receipt["executed_at"], "retirement.event.receipt.executed_at")
            readback_at = parse_time(event_readback["observed_at"], "retirement.event.readback.observed_at")
            plan_authority = state["authority_registry"].get(lifecycle["plan_authority_ref"])
            bindings_ok = (
                lifecycle["event_type"] == "RETIREMENT"
                and lifecycle["retirement_id"] == retirement["retirement_id"]
                and lifecycle["release_id"] == release["release_id"] == retirement["release_id"]
                and lifecycle["plan_id"] == retired_plan["plan_id"]
                and lifecycle["requested_by"] == retirement["owner"]
                and lifecycle["plan_approved_by"] == retired_plan["owner"]
                and lifecycle["plan_authority_ref"] == retired_plan["approval_ref"]
                and lifecycle["retirement_approved_by"] == release["approver"]
                and lifecycle["retirement_authority_ref"] == retirement["decision_ref"]
                and lifecycle["executed_by"] == retired_plan["owner"]
                and lifecycle["residual_evidence_ref"] == retirement["evidence_refs"]["residual"]
                and lifecycle["signoff_evidence_ref"] == retirement["evidence_refs"]["signoff"]
                and event_receipt["event_id"] == lifecycle["event_id"]
                and event_receipt["event_type"] == "RETIREMENT"
                and event_receipt["release_id"] == release["release_id"]
                and event_receipt["plan_id"] == retired_plan["plan_id"]
                and event_receipt["subject_id"] == retirement["retirement_id"]
                and event_receipt["actor"] == lifecycle["executed_by"]
                and event_receipt["authority_ref"] == retirement["decision_ref"]
                and receipt_at == lifecycle_executed_at
                and event_readback["event_id"] == lifecycle["event_id"]
                and event_readback["receipt_ref"] == event_receipt["receipt_id"]
                and event_readback["event_type"] == "RETIREMENT"
                and event_readback["release_id"] == release["release_id"]
                and event_readback["plan_id"] == retired_plan["plan_id"]
                and event_readback["subject_id"] == retirement["retirement_id"]
                and event_readback["observer"] != lifecycle["executed_by"]
                and owner_active(state, event_readback["observer"], now)
            )
            if not bindings_ok:
                fail.append("RETIREMENT_LIFECYCLE_BINDING_INVALID")
            if not (requested_at <= plan_approved_at <= lifecycle_executed_at and requested_at <= retirement_approved_at <= lifecycle_executed_at and receipt_at <= readback_at <= now):
                fail.append("RETIREMENT_LIFECYCLE_SEQUENCE_INVALID")
            if not (parse_time(retired_plan["starts_at"], "retirement.plan.starts_at") <= lifecycle_executed_at < parse_time(retired_plan["expires_at"], "retirement.plan.expires_at")):
                fail.append("RETIREMENT_EXECUTION_OUTSIDE_PLAN_WINDOW")
            if not authority_valid_at(plan_authority, lifecycle_executed_at, actor=retired_plan["owner"], action="approve_rollout_plan", subject_type="rollout", subject_id=retired_plan["plan_id"], object_digest=retired_plan["plan_digest"], scope=retired_plan["scope_digest"], policy_version=release["policy_version"]):
                fail.append("RETIREMENT_PLAN_AUTHORITY_INVALID")
            elif parse_time(plan_authority["issued_at"], "retirement.plan_authority.issued_at") > plan_approved_at:
                fail.append("RETIREMENT_PLAN_APPROVAL_TIME_INVALID")
            if not authority_valid_at(decision_rec, lifecycle_executed_at, actor=release["approver"], action="approve_retirement", subject_type="retirement", subject_id=retirement["retirement_id"], object_digest=retirement["decision_digest"], scope=retired_plan["plan_digest"], policy_version=release["policy_version"]):
                fail.append("RETIREMENT_AUTHORITY_INVALID")
            elif parse_time(decision_rec["issued_at"], "retirement.authority.issued_at") > retirement_approved_at:
                fail.append("RETIREMENT_APPROVAL_TIME_INVALID")
            if lifecycle["status"] == "UNKNOWN" or event_receipt["status"] == "UNKNOWN" or event_readback["status"] == "UNKNOWN":
                review.append("RETIREMENT_EXECUTION_UNKNOWN")
            elif lifecycle["status"] != "VERIFIED" or event_receipt["status"] != "VERIFIED" or event_readback["status"] != "VERIFIED":
                fail.append("RETIREMENT_EXECUTION_FAILED")
        registry = state["retirement_evidence_registry"]
        retirement_proofs: list[dict] = []

        def rproof(ref: str, kind: str, subject: str, code: str, owner_role: str, expected_owner: str | None = None) -> dict | None:
            ev = registry.get(ref)
            if not ev or not record_digest_valid(ev, "record_digest"):
                fail.append(code); return None
            issued_at = parse_time(ev["issued_at"], "retirement.issued_at")
            if not (ev["kind"] == kind and ev["subject_id"] == subject and ev["object_id"] == release["release_id"] and ev["object_version"] == release["release_digest"] and role_owner_active(state, owner_role, ev["owner"], now) and (expected_owner is None or ev["owner"] == expected_owner) and lifecycle_executed_at is not None and lifecycle_executed_at <= issued_at <= now < parse_time(ev["expires_at"], "retirement.expires_at")):
                fail.append(code); return None
            append_status(ev["status"], fail, review, code, code.replace("INVALID", "UNKNOWN"))
            retirement_proofs.append(ev)
            return ev

        for name, kind, role in (("admission", "admission_stopped", "operations"), ("inflight", "inflight_reconciled", "operations"), ("runtime", "runtime_disabled", "technical"), ("network", "network_disabled", "technical"), ("residual", "residual_scan", "security_risk")):
            rproof(retirement["evidence_refs"][name], kind, retirement["retirement_id"], f"RETIREMENT_{kind.upper()}_INVALID", role)
        if retirement["critical_service"]:
            rproof(retirement["evidence_refs"]["replacement"], "replacement_accepted", retirement["retirement_id"], "RETIREMENT_REPLACEMENT_INVALID", "business")
            rproof(retirement["evidence_refs"]["handoff"], "handoff_accepted", retirement["retirement_id"], "RETIREMENT_HANDOFF_INVALID", "capability")
            if retirement["replacement_ref"] == "NONE" or retirement["handoff_ref"] == "NONE": fail.append("RETIREMENT_REPLACEMENT_OR_HANDOFF_MISSING")
        for credential in state["credentials"]:
            if not role_owner_active(state, "security_risk", credential["owner"], now): fail.append("RETIREMENT_CREDENTIAL_OWNER_INVALID")
            if credential["status"] != "REVOKED": fail.append("RETIREMENT_CREDENTIAL_RESIDUAL")
            rproof(credential["evidence_ref"], "credential_revoked", credential["credential_id"], "RETIREMENT_CREDENTIAL_EVIDENCE_INVALID", "security_risk", credential["owner"])
            if credential["restore_enabled"]: fail.append("RETIREMENT_RESTORE_PATH_RESIDUAL")
            rproof(credential["restore_evidence_ref"], "restore_disabled", credential["credential_id"], "RETIREMENT_RESTORE_EVIDENCE_INVALID", "security_risk", credential["owner"])
            for session in credential["sessions"]:
                if session["status"] != "REVOKED": fail.append("RETIREMENT_SESSION_RESIDUAL")
                rproof(session["evidence_ref"], "session_revoked", session["session_id"], "RETIREMENT_SESSION_EVIDENCE_INVALID", "security_risk", credential["owner"])
            for delegation in credential["delegations"]:
                if delegation["status"] != "REVOKED": fail.append("RETIREMENT_DELEGATION_RESIDUAL")
                rproof(delegation["evidence_ref"], "delegation_revoked", delegation["delegation_id"], "RETIREMENT_DELEGATION_EVIDENCE_INVALID", "security_risk", credential["owner"])
        for data in state["data_inventory"]:
            if not role_owner_active(state, "data", data["owner"], now): fail.append("RETIREMENT_DATA_OWNER_INVALID")
            if data["required_action"] == "delete":
                if data["status"] != "DISPOSED" or data["locations"]: fail.append("RETIREMENT_DATA_RESIDUAL")
                rproof(data["evidence_ref"], "data_disposed", data["object_id"], "RETIREMENT_DATA_EVIDENCE_INVALID", "data", data["owner"])
            elif data["required_action"] == "retain":
                if data["status"] != "RETAINED": fail.append("RETIREMENT_DATA_RETENTION_INVALID")
                rproof(data["evidence_ref"], "data_retained", data["object_id"], "RETIREMENT_DATA_EVIDENCE_INVALID", "data", data["owner"])
        signoff = rproof(retirement["evidence_refs"]["signoff"], "terminal_signoff", retirement["retirement_id"], "RETIREMENT_SIGNOFF_INVALID", "business", retirement["owner"])
        if signoff and signoff["content_digest"] != retirement["decision_digest"]: fail.append("RETIREMENT_SIGNOFF_DECISION_BINDING_INVALID")
        if signoff:
            signoff_at = parse_time(signoff["issued_at"], "retirement.signoff.issued_at")
            prior_evidence = [item for item in retirement_proofs if item["evidence_id"] != signoff["evidence_id"]]
            if not prior_evidence or any(parse_time(item["issued_at"], "retirement.evidence.issued_at") > signoff_at for item in prior_evidence):
                fail.append("RETIREMENT_SIGNOFF_SEQUENCE_INVALID")
            residual = registry.get(retirement["evidence_refs"]["residual"])
            if not residual or parse_time(residual["issued_at"], "retirement.residual.issued_at") > signoff_at:
                fail.append("RETIREMENT_SIGNOFF_BEFORE_RESIDUAL_SCAN")

    decision = "FAIL" if fail else "REVIEW_REQUIRED" if review else "PASS"
    # A hard failure owns the final decision, but concurrent UNKNOWN evidence must
    # remain visible in the audit trail instead of being erased by precedence.
    reasons = sorted(set(fail + review))
    derived = {"release_id": release["release_id"], "release_digest": release["release_digest"], "publication_event_ref": release["publication_event_ref"], "publication_executed_at": publication["executed_at"] if publication else "NONE", "active_release": runtime["active_release"], "rollout_stage": rollout["stage"], "trial_count": len(trials), "trial_cost": total_cost, "migration_status": migration["status"], "d21_states": {face: d21[face]["status"] for face in ("technical", "delivery", "business", "environment")}, "retirement_requested": retirement["requested"], "lifecycle_event_ref": retirement["lifecycle_event_ref"]}
    return decision, reasons, derived, external_count


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--input", required=True); parser.add_argument("--authority-root", required=True); parser.add_argument("--output", required=True); args = parser.parse_args()
    input_path, output_path = Path(args.input), Path(args.output)
    source = validate(json.loads(input_path.read_text(encoding="utf-8")), json.loads(Path(args.authority_root).read_text(encoding="utf-8")))
    trials = []
    for scenario in source["scenarios"]:
        state = deep_merge(source["base_state"], scenario["overrides"]); validation_error = None
        try:
            validate_state(state, f"scenario.{scenario['scenario_id']}.state")
            decision, reasons, derived, effects = evaluate(source, state, scenario)
            metadata = scenario["_derived_metadata"]
            if metadata["layer"] == "holdout":
                holdout = source["authority_root"]["holdout_registry"].get(metadata["holdout_ref"])
                if not holdout or holdout["task_type"] != metadata["task_type"] or holdout["release_id"] != state["release_unit"]["release_id"]:
                    decision = "FAIL"
                    reasons = sorted(set(reasons + ["SCENARIO_HOLDOUT_LINEAGE_INVALID"]))
        except ValueError as exc:
            validation_error = str(exc); decision, reasons, derived, effects = "FAIL", ["STATE_SCHEMA_INVALID"], {}, 0
        metadata = scenario["_derived_metadata"]
        trials.append({"scenario_id": scenario["scenario_id"], "task_id": metadata["task_id"], "task_type": metadata["task_type"], "trial_id": metadata["trial_id"], "case_id": scenario["case_id"], "layer": metadata["layer"], "holdout_ref": metadata["holdout_ref"], "security_slices": metadata["security_slices"], "decision": decision, "reasons": reasons, "validation_error": validation_error, "derived": derived, "external_side_effects": effects, "state_digest": sha256(state)})
    distribution = Counter(item["decision"] for item in trials); by_layer = {layer: Counter() for layer in sorted(LAYERS)}
    for item in trials: by_layer[item["layer"]][item["decision"]] += 1
    result = {"schema_version": "c21.lifecycle.result.v2.4", "authority_root_digest": source["authority_root"]["root_digest"], "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(), "trial_count": len(trials), "distribution": dict(sorted(distribution.items())), "by_layer": {key: dict(sorted(value.items())) for key, value in by_layer.items()}, "representative_real_world_count": sum(item["layer"] == "representative_real_world" for item in trials), "security_slice_trial_count": sum(bool(item["security_slices"]) for item in trials), "external_side_effect_count": sum(item["external_side_effects"] for item in trials), "task_trial_ids_unique": len({(item["task_id"], item["trial_id"]) for item in trials}) == len(trials), "decision_digest": sha256([(item["task_id"], item["trial_id"], item["decision"], item["reasons"], item["derived"]) for item in trials]), "trials": trials}
    output_text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"; output_path.write_text(output_text, encoding="utf-8")
    summary = ["# C21 v2.4 生命周期离线状态机摘要", "", "> 纯合成、零真实凭证、零网络、零生产写；不证明真实平台发布、迁移、恢复或退役。", "", f"- trials: `{result['trial_count']}`", f"- distribution: `{result['distribution']}`", f"- authority root digest: `{result['authority_root_digest']}`", f"- decision digest: `{result['decision_digest']}`", f"- representative real-world: `{result['representative_real_world_count']}`", f"- security slice trials: `{result['security_slice_trial_count']}`", f"- synthetic adversarial external effects observed: `{result['external_side_effect_count']}`", "", "## D22 layers", ""]
    for layer, values in result["by_layer"].items(): summary.append(f"- {layer}: `{values}`")
    output_path.with_name("synthetic-lifecycle-summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(result["decision_digest"]); return 0


if __name__ == "__main__":
    raise SystemExit(main())

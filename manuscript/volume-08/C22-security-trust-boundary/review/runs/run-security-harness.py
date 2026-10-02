#!/usr/bin/env python3
"""C19 v2.4 fail-closed evaluator with execution-time authority and readback."""
from __future__ import annotations

import argparse
import copy
from collections import Counter
from datetime import datetime
import hashlib
import ipaddress
import json
import posixpath
import re
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

LAYERS = {"training", "regression", "holdout", "representative_real_world"}
SHA256_REF = re.compile(r"^sha256:[0-9a-f]{64}$")
FROZEN_AUTHORITY_ROOT_DIGEST = "sha256:17f534306054956f7e875d752612a61b31e59157e0381fb4ec11d84ce8d84b1a"
OUTCOME_ENUMS = {
    "REQUEST": {"RECEIVED", "REJECTED"},
    "DECISION": {"EVALUATED", "ALLOWED", "DENIED"},
    "EFFECT": {"APPLIED", "FAILED", "UNKNOWN"},
    "INCIDENT": {"OPENED", "CONTAINED"},
    "RECOVERY": {"PROPOSED", "PASSED", "FAILED"},
}


def canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(value).encode()).hexdigest()


def exact(value: Any, keys: Iterable[str], path: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise ValueError(f"{path} must be object")
    if set(value) != set(keys):
        raise ValueError(f"{path} closed-world fields differ")
    return value


def typed(value: Any, kind: type, path: str) -> None:
    if type(value) is not kind:
        raise ValueError(f"{path} must be {kind.__name__}")


def string(value: Any, path: str) -> None:
    typed(value, str, path)
    if not value:
        raise ValueError(f"{path} must be non-empty")


def strings(value: Any, path: str) -> list[str]:
    typed(value, list, path)
    if not all(type(item) is str and item for item in value):
        raise ValueError(f"{path} must contain non-empty strings")
    return value


def enum(value: Any, allowed: set[str], path: str) -> None:
    if type(value) is not str or value not in allowed:
        raise ValueError(f"{path} unknown enum")


def sha(value: Any, path: str) -> None:
    if type(value) is not str or not SHA256_REF.fullmatch(value):
        raise ValueError(f"{path} must be sha256 reference")


def timestamp(value: Any, path: str) -> datetime:
    string(value, path)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{path} invalid timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{path} timezone required")
    return parsed


def at_time(now: datetime, start: str, end: str) -> bool:
    return timestamp(start, "window.start") <= now < timestamp(end, "window.end")


def authority_record_active_at(record: dict[str, Any], moment: datetime, active_status: str) -> bool:
    issued = timestamp(record["issued_at"], "authority.issued_at")
    start = timestamp(record["not_before"], "authority.not_before")
    end = timestamp(record["expires_at"], "authority.expires_at")
    revoked = record["revoked_at"]
    return record["status"] == active_status and issued <= moment and start <= moment < end and (revoked == "NONE" or moment < timestamp(revoked, "authority.revoked_at"))


def validate_principal(record: Any, path: str) -> None:
    record = exact(record, ["kind", "tenant", "roles", "status"], path)
    enum(record["kind"], {"HUMAN", "AGENT", "SERVICE"}, f"{path}.kind")
    string(record["tenant"], f"{path}.tenant")
    strings(record["roles"], f"{path}.roles")
    enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, f"{path}.status")


def validate_delegation(record: Any, path: str) -> None:
    record = exact(record, ["delegation_id", "parent_principal", "child_principal", "tenant", "actions", "objects", "scopes", "issued_at", "not_before", "expires_at", "revoked_at", "status"], path)
    for key in ["delegation_id", "parent_principal", "child_principal", "tenant"]:
        string(record[key], f"{path}.{key}")
    for key in ["actions", "objects", "scopes"]:
        strings(record[key], f"{path}.{key}")
    timestamp(record["issued_at"], f"{path}.issued_at")
    timestamp(record["not_before"], f"{path}.not_before")
    timestamp(record["expires_at"], f"{path}.expires_at")
    if record["revoked_at"] != "NONE": timestamp(record["revoked_at"], f"{path}.revoked_at")
    enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, f"{path}.status")


def validate_approval(record: Any, path: str) -> None:
    record = exact(record, ["approval_id", "principal", "actor", "tenant", "action", "object", "scope", "params_digest", "issued_at", "not_before", "expires_at", "revoked_at", "status", "policy_version"], path)
    for key in ["approval_id", "principal", "actor", "tenant", "action", "object", "scope", "policy_version"]:
        string(record[key], f"{path}.{key}")
    sha(record["params_digest"], f"{path}.params_digest")
    timestamp(record["issued_at"], f"{path}.issued_at")
    timestamp(record["not_before"], f"{path}.not_before")
    timestamp(record["expires_at"], f"{path}.expires_at")
    if record["revoked_at"] != "NONE": timestamp(record["revoked_at"], f"{path}.revoked_at")
    enum(record["status"], {"APPROVED", "REVOKED", "UNKNOWN"}, f"{path}.status")


def validate_grant(record: Any, path: str) -> None:
    record = exact(record, ["grant_id", "actor", "tenant", "action", "object", "scope", "issued_at", "not_before", "expires_at", "revoked_at", "status", "policy_version", "approval_id"], path)
    for key in ["grant_id", "actor", "tenant", "action", "object", "scope", "policy_version", "approval_id"]:
        string(record[key], f"{path}.{key}")
    timestamp(record["issued_at"], f"{path}.issued_at")
    timestamp(record["not_before"], f"{path}.not_before")
    timestamp(record["expires_at"], f"{path}.expires_at")
    if record["revoked_at"] != "NONE": timestamp(record["revoked_at"], f"{path}.revoked_at")
    enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, f"{path}.status")


def validate_credential(record: Any, path: str) -> None:
    record = exact(record, ["secret_ref", "owner", "principal", "tenant", "scope", "audience", "object", "action", "grant_id", "ttl_seconds", "issued_at", "not_before", "expires_at", "revoked_at", "status", "value_visible_to_model"], path)
    for key in ["secret_ref", "owner", "principal", "tenant", "scope", "audience", "object", "action", "grant_id"]:
        string(record[key], f"{path}.{key}")
    typed(record["ttl_seconds"], int, f"{path}.ttl_seconds")
    timestamp(record["issued_at"], f"{path}.issued_at")
    timestamp(record["not_before"], f"{path}.not_before")
    timestamp(record["expires_at"], f"{path}.expires_at")
    if record["revoked_at"] != "NONE": timestamp(record["revoked_at"], f"{path}.revoked_at")
    enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, f"{path}.status")
    typed(record["value_visible_to_model"], bool, f"{path}.value_visible_to_model")


def validate_component(record: Any, path: str, kind: str) -> None:
    if kind == "tool":
        keys = ["id", "manifest_digest", "implementation_digest", "dependencies", "status", "allowed_actions", "allowed_objects", "allowed_scopes"]
    elif kind == "plugin":
        keys = ["id", "manifest_digest", "dependencies", "status", "execution_mode", "capabilities"]
    else:
        keys = ["id", "manifest_digest", "dependencies", "status"]
    record = exact(record, keys, path)
    string(record["id"], f"{path}.id")
    sha(record["manifest_digest"], f"{path}.manifest_digest")
    strings(record["dependencies"], f"{path}.dependencies") if record["dependencies"] else typed(record["dependencies"], list, f"{path}.dependencies")
    enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, f"{path}.status")
    if kind == "tool":
        sha(record["implementation_digest"], f"{path}.implementation_digest")
        for key in ["allowed_actions", "allowed_objects", "allowed_scopes"]:
            strings(record[key], f"{path}.{key}")
    if kind == "plugin":
        enum(record["execution_mode"], {"disabled", "sandboxed", "in_process"}, f"{path}.execution_mode")
        typed(record["capabilities"], list, f"{path}.capabilities")
        if not all(type(item) is str and item for item in record["capabilities"]):
            raise ValueError(f"{path}.capabilities invalid")


def validate_authority_bundle(bundle: Any) -> dict[str, Any]:
    bundle = exact(bundle, ["schema_version", "bundle_id", "issued_at", "issuer", "registries", "root_digest"], "authority")
    if bundle["schema_version"] != "c19.security.authority.v2.4":
        raise ValueError("authority schema version")
    for key in ["bundle_id", "issuer"]:
        string(bundle[key], f"authority.{key}")
    timestamp(bundle["issued_at"], "authority.issued_at")
    sha(bundle["root_digest"], "authority.root_digest")
    payload = {key: value for key, value in bundle.items() if key != "root_digest"}
    if digest(payload) != bundle["root_digest"] or bundle["root_digest"] != FROZEN_AUTHORITY_ROOT_DIGEST:
        raise ValueError("authority root digest is not the pre-registered frozen root")
    registries = exact(bundle["registries"], ["principals", "identities", "sessions", "delegations", "policies", "approvals", "grants", "credentials", "egress_policies", "input_manifests", "tools", "skills", "plugins", "readbacks", "audit_anchors", "incident_evidence", "recovery_evidence", "test_definitions", "test_evidence", "real_world_evidence"], "authority.registries")
    for name, registry in registries.items():
        typed(registry, dict, f"authority.registries.{name}")
        if any(type(key) is not str or not key for key in registry):
            raise ValueError(f"authority.registries.{name} has empty/non-string key")
    for key, record in registries["principals"].items():
        validate_principal(record, f"authority.registries.principals.{key}")
    for key, record in registries["identities"].items():
        record = exact(record, ["tenant", "session", "agent", "service", "status", "verified"], f"authority.registries.identities.{key}")
        for field in ["tenant", "session", "agent", "service"]:
            string(record[field], f"identity.{field}")
        enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, "identity.status")
        typed(record["verified"], bool, "identity.verified")
    for key, record in registries["sessions"].items():
        record = exact(record, ["tenant", "session", "principal", "status", "issued_at", "not_before", "expires_at", "revoked_at", "max_duration_seconds"], f"authority.registries.sessions.{key}")
        for field in ["tenant", "session", "principal"]:
            string(record[field], f"session.{field}")
        if record["session"] != key:
            raise ValueError("session key/id mismatch")
        enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, "session.status")
        timestamp(record["issued_at"], "session.issued_at")
        start = timestamp(record["not_before"], "session.not_before")
        end = timestamp(record["expires_at"], "session.expires_at")
        if record["revoked_at"] != "NONE": timestamp(record["revoked_at"], "session.revoked_at")
        typed(record["max_duration_seconds"], int, "session.max_duration_seconds")
        if record["max_duration_seconds"] <= 0 or int((end - start).total_seconds()) > record["max_duration_seconds"]:
            raise ValueError("session duration exceeds frozen maximum")
    for key, record in registries["delegations"].items():
        validate_delegation(record, f"authority.registries.delegations.{key}")
        if record["delegation_id"] != key:
            raise ValueError("delegation key/id mismatch")
    for key, record in registries["policies"].items():
        record = exact(record, ["status", "allowed_actions", "denied_actions", "allowed_objects", "allowed_scopes", "required_sandbox_mode", "allowed_mount_roots", "egress_policy_ref"], f"authority.registries.policies.{key}")
        enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, "policy.status")
        for field in ["allowed_actions", "denied_actions", "allowed_objects", "allowed_scopes", "allowed_mount_roots"]:
            strings(record[field], f"policy.{field}")
        enum(record["required_sandbox_mode"], {"off", "non-main", "all"}, "policy.required_sandbox_mode")
        string(record["egress_policy_ref"], "policy.egress_policy_ref")
    for key, record in registries["approvals"].items():
        validate_approval(record, f"authority.registries.approvals.{key}")
        if record["approval_id"] != key:
            raise ValueError("approval key/id mismatch")
    for key, record in registries["grants"].items():
        validate_grant(record, f"authority.registries.grants.{key}")
        if record["grant_id"] != key:
            raise ValueError("grant key/id mismatch")
    for key, record in registries["credentials"].items():
        validate_credential(record, f"authority.registries.credentials.{key}")
        if record["secret_ref"] != key:
            raise ValueError("credential key/ref mismatch")
    for key, record in registries["egress_policies"].items():
        record = exact(record, ["status", "allowed_hosts", "deny_private", "deny_secret_data"], f"authority.registries.egress_policies.{key}")
        enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, "egress.status")
        typed(record["allowed_hosts"], list, "egress.allowed_hosts")
        if not all(type(item) is str and item for item in record["allowed_hosts"]):
            raise ValueError("egress allowlist invalid")
        typed(record["deny_private"], bool, "egress.deny_private")
        typed(record["deny_secret_data"], bool, "egress.deny_secret_data")
    for key, record in registries["input_manifests"].items():
        record = exact(record, ["status", "provenance", "trust", "content_digest", "owner"], f"authority.registries.input_manifests.{key}")
        enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, "input_manifest.status")
        for field in ["provenance", "trust", "owner"]:
            string(record[field], f"input_manifest.{field}")
        sha(record["content_digest"], "input_manifest.content_digest")
    for registry_name, kind in [("tools", "tool"), ("skills", "skill"), ("plugins", "plugin")]:
        for key, record in registries[registry_name].items():
            validate_component(record, f"authority.registries.{registry_name}.{key}", kind)
    for key, record in registries["readbacks"].items():
        record = exact(record, ["readback_id", "effect_id", "receipt_id", "object", "action", "scope", "observer", "authority_ref", "observed_at", "terminal_status", "authorization_snapshot_digest", "record_digest"], f"authority.registries.readbacks.{key}")
        for field in ["readback_id", "effect_id", "receipt_id", "object", "action", "scope", "observer", "authority_ref"]: string(record[field], f"readback.{field}")
        timestamp(record["observed_at"], "readback.observed_at")
        enum(record["terminal_status"], {"APPLIED", "FAILED", "UNKNOWN"}, "readback.terminal_status")
        sha(record["authorization_snapshot_digest"], "readback.authorization_snapshot_digest")
        sha(record["record_digest"], "readback.record_digest")
        if record["readback_id"] != key or record["record_digest"] != digest({k: v for k, v in record.items() if k != "record_digest"}): raise ValueError("readback binding or digest invalid")
    for key, record in registries["audit_anchors"].items():
        record = exact(record, ["initial_digest", "final_digest", "event_count", "allowed_sequence", "status", "issuer"], f"authority.registries.audit_anchors.{key}")
        sha(record["initial_digest"], "audit.initial")
        sha(record["final_digest"], "audit.final")
        typed(record["event_count"], int, "audit.event_count")
        if record["event_count"] < 1:
            raise ValueError("audit event_count")
        strings(record["allowed_sequence"], "audit.allowed_sequence")
        enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, "audit.status")
        string(record["issuer"], "audit.issuer")
    for key, record in registries["incident_evidence"].items():
        record = exact(record, ["incident_id", "effect_ids", "kind", "status", "owner", "content_digest"], f"authority.registries.incident_evidence.{key}")
        for field in ["incident_id", "kind", "owner"]:
            string(record[field], f"incident_evidence.{field}")
        enum(record["status"], {"VERIFIED", "REVOKED", "UNKNOWN"}, "incident_evidence.status")
        strings(record["effect_ids"], "incident_evidence.effect_ids")
        sha(record["content_digest"], "incident_evidence.content_digest")
    for key, record in registries["recovery_evidence"].items():
        record = exact(record, ["incident_id", "effect_ids", "origin", "target_version", "probe_status", "status", "owner", "content_digest"], f"authority.registries.recovery_evidence.{key}")
        string(record["incident_id"], "recovery.incident_id")
        strings(record["effect_ids"], "recovery.effect_ids")
        enum(record["origin"], {"synthetic", "representative_real_world"}, "recovery.origin")
        string(record["target_version"], "recovery.target_version")
        enum(record["probe_status"], {"PASS", "FAIL", "UNKNOWN"}, "recovery.probe_status")
        enum(record["status"], {"VERIFIED", "REVOKED", "UNKNOWN"}, "recovery.status")
        string(record["owner"], "recovery.owner")
        sha(record["content_digest"], "recovery.content_digest")
    for key, record in registries["test_definitions"].items():
        record = exact(record, ["scenario_id", "task_id", "trial_id", "layer", "security_red_team", "synthetic_shadow", "evidence_ref", "status"], f"authority.registries.test_definitions.{key}")
        for field in ["scenario_id", "task_id", "trial_id", "evidence_ref"]:
            string(record[field], f"test_definition.{field}")
        if record["scenario_id"] != key:
            raise ValueError("test definition key/id mismatch")
        enum(record["layer"], LAYERS, "test_definition.layer")
        typed(record["security_red_team"], bool, "test_definition.security_red_team")
        typed(record["synthetic_shadow"], bool, "test_definition.synthetic_shadow")
        enum(record["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, "test_definition.status")
    for key, record in registries["test_evidence"].items():
        record = exact(record, ["task_id", "trial_id", "origin", "execution_mode", "status", "content_digest"], f"authority.registries.test_evidence.{key}")
        for field in ["task_id", "trial_id"]:
            string(record[field], f"test_evidence.{field}")
        enum(record["origin"], {"synthetic", "representative_real_world"}, "test_evidence.origin")
        enum(record["execution_mode"], {"offline_synthetic", "real_runtime"}, "test_evidence.execution_mode")
        enum(record["status"], {"VERIFIED", "REVOKED", "UNKNOWN"}, "test_evidence.status")
        sha(record["content_digest"], "test_evidence.content_digest")
    if registries["real_world_evidence"]:
        raise ValueError("offline frozen authority must not contain real-world evidence")
    return bundle


def validate_state(state: Any, path: str) -> None:
    state = exact(state, ["identity", "tenant_session", "delegation", "policy", "approval", "grant", "credential", "sandbox", "egress", "input", "tool", "skill", "plugin", "effects", "receipts", "audit", "incident", "recovery"], path)
    identity = exact(state["identity"], ["principal", "tenant", "session", "agent", "service", "status", "verified"], f"{path}.identity")
    for key in ["principal", "tenant", "session", "agent", "service"]:
        string(identity[key], f"{path}.identity.{key}")
    enum(identity["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, f"{path}.identity.status")
    typed(identity["verified"], bool, f"{path}.identity.verified")
    session = exact(state["tenant_session"], ["tenant", "session", "principal", "status", "issued_at", "not_before", "expires_at", "revoked_at", "max_duration_seconds"], f"{path}.tenant_session")
    for key in ["tenant", "session", "principal"]:
        string(session[key], f"{path}.tenant_session.{key}")
    enum(session["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, f"{path}.tenant_session.status")
    timestamp(session["issued_at"], f"{path}.tenant_session.issued_at")
    timestamp(session["not_before"], f"{path}.tenant_session.not_before")
    timestamp(session["expires_at"], f"{path}.tenant_session.expires_at")
    if session["revoked_at"] != "NONE": timestamp(session["revoked_at"], f"{path}.tenant_session.revoked_at")
    typed(session["max_duration_seconds"], int, f"{path}.tenant_session.max_duration_seconds")
    validate_delegation(state["delegation"], f"{path}.delegation")
    exact(state["policy"], ["version", "status"], f"{path}.policy")
    string(state["policy"]["version"], f"{path}.policy.version")
    enum(state["policy"]["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, f"{path}.policy.status")
    validate_approval(state["approval"], f"{path}.approval")
    validate_grant(state["grant"], f"{path}.grant")
    validate_credential(state["credential"], f"{path}.credential")
    sandbox = exact(state["sandbox"], ["mode", "scope", "backend", "mounts", "network_default", "status"], f"{path}.sandbox")
    enum(sandbox["mode"], {"off", "non-main", "all"}, "sandbox.mode")
    enum(sandbox["scope"], {"session", "agent", "shared"}, "sandbox.scope")
    enum(sandbox["backend"], {"container", "microvm", "host"}, "sandbox.backend")
    enum(sandbox["network_default"], {"deny", "allow"}, "sandbox.network_default")
    enum(sandbox["status"], {"ACTIVE", "FAILED", "UNKNOWN"}, "sandbox.status")
    typed(sandbox["mounts"], list, "sandbox.mounts")
    for mount in sandbox["mounts"]:
        mount = exact(mount, ["path", "access", "source"], "sandbox.mount")
        string(mount["path"], "sandbox.mount.path")
        enum(mount["access"], {"ro", "rw"}, "sandbox.mount.access")
        enum(mount["source"], {"workspace", "host", "secret"}, "sandbox.mount.source")
    egress = exact(state["egress"], ["policy_ref", "allowed_hosts", "requests"], f"{path}.egress")
    string(egress["policy_ref"], "egress.policy_ref")
    typed(egress["allowed_hosts"], list, "egress.allowed_hosts")
    if not all(type(item) is str and item for item in egress["allowed_hosts"]):
        raise ValueError("egress allowed_hosts invalid")
    typed(egress["requests"], list, "egress.requests")
    for request in egress["requests"]:
        request = exact(request, ["url", "resolved_ip", "redirect_chain", "data_classification"], "egress.request")
        for key in ["url", "resolved_ip"]:
            string(request[key], f"egress.request.{key}")
        typed(request["redirect_chain"], list, "egress.request.redirect_chain")
        if not all(type(item) is str and item for item in request["redirect_chain"]):
            raise ValueError("redirect chain invalid")
        enum(request["data_classification"], {"public", "internal", "confidential", "secret"}, "egress.request.data_classification")
    input_record = exact(state["input"], ["manifest_ref", "provenance", "trust", "content_digest", "control_claimed"], f"{path}.input")
    for key in ["manifest_ref", "provenance"]:
        string(input_record[key], f"input.{key}")
    enum(input_record["trust"], {"trusted_fixture", "untrusted_user", "untrusted_web", "untrusted_memory", "unknown"}, "input.trust")
    sha(input_record["content_digest"], "input.content_digest")
    typed(input_record["control_claimed"], bool, "input.control_claimed")
    tool = exact(state["tool"], ["id", "registry_ref", "manifest_digest", "implementation_digest", "dependencies", "action", "object", "scope", "status"], f"{path}.tool")
    for key in ["id", "registry_ref", "action", "object", "scope"]:
        string(tool[key], f"tool.{key}")
    sha(tool["manifest_digest"], "tool.manifest_digest")
    sha(tool["implementation_digest"], "tool.implementation_digest")
    strings(tool["dependencies"], "tool.dependencies")
    enum(tool["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, "tool.status")
    for name in ["skill", "plugin"]:
        component = state[name]
        keys = ["id", "registry_ref", "manifest_digest", "dependencies", "status"] + (["execution_mode", "capabilities"] if name == "plugin" else [])
        exact(component, keys, f"{path}.{name}")
        for key in ["id", "registry_ref"]:
            string(component[key], f"{name}.{key}")
        sha(component["manifest_digest"], f"{name}.manifest_digest")
        typed(component["dependencies"], list, f"{name}.dependencies")
        if not all(type(item) is str and item for item in component["dependencies"]):
            raise ValueError(f"{name}.dependencies invalid")
        enum(component["status"], {"ACTIVE", "REVOKED", "UNKNOWN"}, f"{name}.status")
        if name == "plugin":
            enum(component["execution_mode"], {"disabled", "sandboxed", "in_process"}, "plugin.execution_mode")
            typed(component["capabilities"], list, "plugin.capabilities")
            if not all(type(item) is str and item for item in component["capabilities"]):
                raise ValueError("plugin.capabilities invalid")
    typed(state["effects"], list, "effects")
    for effect in state["effects"]:
        effect = exact(effect, ["effect_id", "action", "object", "scope", "params_digest", "executor", "executed_at", "status", "external_side_effect", "authorized_grant_id", "authorization_snapshot_digest", "receipt_ref", "readback_ref"], "effect")
        for key in ["effect_id", "action", "object", "scope", "executor", "authorized_grant_id"]:
            string(effect[key], f"effect.{key}")
        sha(effect["params_digest"], "effect.params_digest")
        typed(effect["executed_at"], str, "effect.executed_at")
        typed(effect["receipt_ref"], str, "effect.receipt_ref")
        typed(effect["readback_ref"], str, "effect.readback_ref")
        sha(effect["authorization_snapshot_digest"], "effect.authorization_snapshot_digest")
        enum(effect["status"], {"NONE", "APPLIED", "FAILED", "UNKNOWN", "DUPLICATE_CONFLICT"}, "effect.status")
        typed(effect["external_side_effect"], bool, "effect.external_side_effect")
    typed(state["receipts"], list, "receipts")
    for item in state["receipts"]:
        current = {"receipt_id", "effect_id", "status", "target", "action", "scope", "executor", "executed_at", "issued_at", "authorization_snapshot_digest", "digest"}
        legacy = {"receipt_id", "effect_id", "status", "authoritative_readback", "target", "digest"}
        if type(item) is not dict or set(item) not in {frozenset(current), frozenset(legacy)}:
            raise ValueError("receipt closed-world fields differ")
        for key in ["receipt_id", "effect_id", "target"]:
            string(item[key], f"receipt.{key}")
        if set(item) == current:
            for key in ["action", "scope", "executor"]: string(item[key], f"receipt.{key}")
            for key in ["executed_at", "issued_at"]: timestamp(item[key], f"receipt.{key}")
            sha(item["authorization_snapshot_digest"], "receipt.authorization_snapshot_digest")
        else:
            enum(item["authoritative_readback"], {"NONE", "APPLIED", "FAILED", "UNKNOWN"}, "receipt.authoritative_readback")
        enum(item["status"], {"NONE", "APPLIED", "FAILED", "UNKNOWN"}, "receipt.status")
        sha(item["digest"], "receipt.digest")
    audit = exact(state["audit"], ["chain_id", "events"], "audit")
    string(audit["chain_id"], "audit.chain_id")
    typed(audit["events"], list, "audit.events")
    for event in audit["events"]:
        event = exact(event, ["seq", "event_id", "event_type", "payload", "prev_digest", "event_digest"], "audit.event")
        typed(event["seq"], int, "audit.event.seq")
        string(event["event_id"], "audit.event.event_id")
        enum(event["event_type"], set(OUTCOME_ENUMS), "audit.event.type")
        payload = exact(event["payload"], ["subject", "action", "object", "outcome", "effect_id", "receipt_id", "readback_id", "effect_digest", "receipt_digest", "readback_digest", "executed_at", "receipt_issued_at", "readback_observed_at"], "audit.event.payload")
        for key in ["subject", "action", "object"]:
            string(payload[key], f"audit.payload.{key}")
        enum(payload["outcome"], OUTCOME_ENUMS[event["event_type"]], "audit.payload.outcome")
        typed(payload["effect_id"], str, "audit.payload.effect_id")
        typed(payload["receipt_id"], str, "audit.payload.receipt_id")
        typed(payload["readback_id"], str, "audit.payload.readback_id")
        for field in ["effect_digest", "receipt_digest", "readback_digest"]: sha(payload[field], f"audit.payload.{field}")
        for field in ["executed_at", "receipt_issued_at", "readback_observed_at"]: typed(payload[field], str, f"audit.payload.{field}")
        sha(event["prev_digest"], "audit.event.prev_digest")
        sha(event["event_digest"], "audit.event.digest")
    incident = exact(state["incident"], ["incident_id", "state", "controls", "effect_ids", "evidence_refs"], "incident")
    string(incident["incident_id"], "incident.incident_id")
    enum(incident["state"], {"NONE", "OPEN", "CONTAINED", "UNKNOWN"}, "incident.state")
    controls = exact(incident["controls"], ["stop", "isolate", "revoke", "rotate", "forensics", "impact_assessed", "notify"], "incident.controls")
    for value in controls.values():
        typed(value, bool, "incident.control")
    typed(incident["evidence_refs"], list, "incident.evidence_refs")
    if not all(type(item) is str and item for item in incident["evidence_refs"]):
        raise ValueError("incident evidence refs invalid")
    typed(incident["effect_ids"], list, "incident.effect_ids")
    if not all(type(item) is str and item for item in incident["effect_ids"]):
        raise ValueError("incident effect ids invalid")
    recovery = exact(state["recovery"], ["state", "regression_pass", "residual_risk", "residual_risk_level", "residual_risk_owner", "evidence_ref", "evidence_origin", "target_version", "probe_status"], "recovery")
    enum(recovery["state"], {"NOT_NEEDED", "PROPOSED", "REGRESSION_PASS", "UNKNOWN"}, "recovery.state")
    typed(recovery["regression_pass"], bool, "recovery.regression_pass")
    string(recovery["residual_risk"], "recovery.residual_risk")
    enum(recovery["residual_risk_level"], {"NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN"}, "recovery.residual_risk_level")
    string(recovery["residual_risk_owner"], "recovery.residual_risk_owner")
    for key in ["evidence_ref", "target_version"]:
        typed(recovery[key], str, f"recovery.{key}")
    enum(recovery["evidence_origin"], {"none", "synthetic", "representative_real_world", "unknown"}, "recovery.origin")
    enum(recovery["probe_status"], {"NOT_RUN", "PASS", "FAIL", "UNKNOWN"}, "recovery.probe_status")


def validate_source(source: Any, authority: dict[str, Any]) -> dict[str, Any]:
    source = exact(source, ["schema_version", "seed", "evaluation_time", "data_origin", "environment", "declared_layers", "authority_ref", "scenarios"], "root")
    if source["schema_version"] != "c19.security.synthetic.v2.4":
        raise ValueError("unsupported source schema")
    string(source["seed"], "root.seed")
    timestamp(source["evaluation_time"], "root.evaluation_time")
    if source["data_origin"] != "synthetic":
        raise ValueError("offline source must be synthetic")
    environment = exact(source["environment"], ["mode", "network_accessed", "real_credentials_used", "external_side_effects_permitted"], "environment")
    if environment != {"mode": "offline_synthetic", "network_accessed": False, "real_credentials_used": False, "external_side_effects_permitted": False}:
        raise ValueError("offline environment contradiction")
    declared = exact(source["declared_layers"], ["training", "regression", "holdout", "representative_real_world", "security_red_team_is_cross_cutting"], "declared_layers")
    for layer in LAYERS:
        typed(declared[layer], int, f"declared_layers.{layer}")
        if declared[layer] < 0:
            raise ValueError("negative layer count")
    typed(declared["security_red_team_is_cross_cutting"], bool, "declared_layers.security_red_team_is_cross_cutting")
    authority_ref = exact(source["authority_ref"], ["bundle_id", "root_digest"], "authority_ref")
    if authority_ref != {"bundle_id": authority["bundle_id"], "root_digest": authority["root_digest"]}:
        raise ValueError("source authority reference does not match frozen root")
    typed(source["scenarios"], list, "scenarios")
    for index, scenario in enumerate(source["scenarios"]):
        scenario = exact(scenario, ["id", "test_ref", "task_id", "trial_id", "layer", "security_red_team", "synthetic_shadow", "state"], f"scenarios[{index}]")
        for key in ["id", "test_ref", "task_id", "trial_id"]:
            string(scenario[key], f"scenario.{key}")
        enum(scenario["layer"], LAYERS, "scenario.layer")
        typed(scenario["security_red_team"], bool, "scenario.security_red_team")
        typed(scenario["synthetic_shadow"], bool, "scenario.synthetic_shadow")
        validate_state(scenario["state"], f"scenarios[{index}].state")
    for key in ["id", "task_id", "trial_id"]:
        values = [scenario[key] for scenario in source["scenarios"]]
        if len(values) != len(set(values)):
            raise ValueError(f"duplicate scenario {key}")
    observed = Counter(scenario["layer"] for scenario in source["scenarios"])
    if any(observed[layer] != declared[layer] for layer in LAYERS):
        raise ValueError("declared D22 layers do not match")
    if observed["representative_real_world"]:
        raise ValueError("offline runner rejects representative real-world scenarios")
    return source


def evaluate(scenario: dict[str, Any], source: dict[str, Any], authority: dict[str, Any]) -> tuple[str, list[str], list[str], dict[str, Any]]:
    state = scenario["state"]
    registries = authority["registries"]
    now = timestamp(source["evaluation_time"], "evaluation_time")
    hard: list[str] = []
    review: list[str] = []
    if not source["declared_layers"]["security_red_team_is_cross_cutting"]:
        hard.append("SECURITY_CROSS_CUTTING_DISABLED")
    test_definition = registries["test_definitions"].get(scenario["test_ref"])
    if not test_definition or test_definition["status"] != "ACTIVE":
        hard.append("TEST_DEFINITION_AUTHORITY_INVALID")
    else:
        observed_test = {
            "scenario_id": scenario["id"],
            "task_id": scenario["task_id"],
            "trial_id": scenario["trial_id"],
            "layer": scenario["layer"],
            "security_red_team": scenario["security_red_team"],
            "synthetic_shadow": scenario["synthetic_shadow"],
        }
        expected_test = {key: test_definition[key] for key in observed_test}
        if observed_test != expected_test:
            hard.append("TEST_DEFINITION_BINDING_INVALID")
        test_evidence = registries["test_evidence"].get(test_definition["evidence_ref"])
        if (
            not test_evidence
            or test_evidence["status"] != "VERIFIED"
            or test_evidence["task_id"] != scenario["task_id"]
            or test_evidence["trial_id"] != scenario["trial_id"]
            or test_evidence["origin"] != "synthetic"
            or test_evidence["execution_mode"] != "offline_synthetic"
            or test_evidence["content_digest"] != digest(test_definition)
        ):
            hard.append("TEST_EXECUTION_EVIDENCE_INVALID")
    identity = state["identity"]
    identity_authority = registries["identities"].get(identity["principal"])
    observed_identity = {key: identity[key] for key in ["tenant", "session", "agent", "service", "status", "verified"]}
    if identity_authority != observed_identity or identity["status"] != "ACTIVE" or not identity["verified"]:
        hard.append("IDENTITY_AUTHORITY_MISMATCH")
    principal = registries["principals"].get(identity["principal"])
    if not principal or principal["status"] != "ACTIVE" or principal["kind"] != "AGENT" or principal["tenant"] != identity["tenant"]:
        hard.append("EXECUTOR_PRINCIPAL_INVALID")
    session = state["tenant_session"]
    session_authority = registries["sessions"].get(session["session"])
    session_start = timestamp(session["not_before"], "session.not_before")
    session_end = timestamp(session["expires_at"], "session.expires_at")
    if (
        session_authority != session
        or session["principal"] != identity["principal"]
        or session["tenant"] != identity["tenant"]
        or session["session"] != identity["session"]
        or session["status"] != "ACTIVE"
        or not (session_start <= now < session_end)
        or session["max_duration_seconds"] <= 0
        or int((session_end - session_start).total_seconds()) > session["max_duration_seconds"]
    ):
        hard.append("TENANT_SESSION_BINDING_INVALID")

    delegation = state["delegation"]
    delegation_authority = registries["delegations"].get(delegation["delegation_id"])
    parent = registries["principals"].get(delegation["parent_principal"])
    if delegation_authority != delegation or not parent or parent["status"] != "ACTIVE" or parent["kind"] not in {"HUMAN", "SERVICE"} or "DELEGATOR" not in parent["roles"] or parent["tenant"] != delegation["tenant"] or delegation["child_principal"] != identity["principal"] or delegation["tenant"] != identity["tenant"] or delegation["status"] != "ACTIVE" or not at_time(now, delegation["not_before"], delegation["expires_at"]):
        hard.append("DELEGATION_AUTHORITY_INVALID")
    policy = state["policy"]
    policy_authority = registries["policies"].get(policy["version"])
    if policy["status"] != "ACTIVE" or not policy_authority or policy_authority["status"] != "ACTIVE":
        hard.append("POLICY_NOT_ACTIVE")
        policy_authority = {"allowed_actions": [], "denied_actions": [], "allowed_objects": [], "allowed_scopes": [], "required_sandbox_mode": "all", "allowed_mount_roots": [], "egress_policy_ref": "missing"}
    tool = state["tool"]
    action, obj, scope = tool["action"], tool["object"], tool["scope"]
    if action not in policy_authority["allowed_actions"] or action in policy_authority["denied_actions"] or obj not in policy_authority["allowed_objects"] or scope not in policy_authority["allowed_scopes"]:
        hard.append("POLICY_DENY")
    if action not in delegation["actions"] or obj not in delegation["objects"] or scope not in delegation["scopes"]:
        hard.append("DELEGATION_SCOPE_DENY")

    approval = state["approval"]
    approval_authority = registries["approvals"].get(approval["approval_id"])
    approver = registries["principals"].get(approval["principal"])
    if approval_authority != approval or not approver or approver["status"] != "ACTIVE" or approver["kind"] != "HUMAN" or "APPROVER" not in approver["roles"] or approver["tenant"] != approval["tenant"] or approval["principal"] == identity["principal"] or approval["actor"] != identity["principal"] or approval["tenant"] != identity["tenant"] or approval["action"] != action or approval["object"] != obj or approval["scope"] != scope or approval["params_digest"] != digest({"action": action, "object": obj, "scope": scope}) or approval["policy_version"] != policy["version"] or approval["status"] != "APPROVED" or not at_time(now, approval["not_before"], approval["expires_at"]):
        hard.append("APPROVAL_AUTHORITY_INVALID")
    grant = state["grant"]
    grant_authority = registries["grants"].get(grant["grant_id"])
    if grant_authority != grant or grant["actor"] != identity["principal"] or grant["tenant"] != identity["tenant"] or grant["action"] != action or grant["object"] != obj or grant["scope"] != scope or grant["approval_id"] != approval["approval_id"] or grant["policy_version"] != policy["version"] or grant["status"] != "ACTIVE" or not at_time(now, grant["not_before"], grant["expires_at"]):
        hard.append("GRANT_AUTHORITY_INVALID")

    credential = state["credential"]
    credential_authority = registries["credentials"].get(credential["secret_ref"])
    broker = registries["principals"].get(credential["owner"])
    issued = timestamp(credential["issued_at"], "credential.issued_at")
    expires = timestamp(credential["expires_at"], "credential.expires_at")
    actual_ttl = int((expires - issued).total_seconds())
    if credential_authority != credential or not broker or broker["status"] != "ACTIVE" or broker["kind"] != "SERVICE" or "CREDENTIAL_BROKER" not in broker["roles"] or credential["principal"] != identity["principal"] or credential["tenant"] != identity["tenant"] or credential["scope"] != scope or credential["audience"] != tool["id"] or credential["object"] != obj or credential["action"] != action or credential["grant_id"] != grant["grant_id"] or credential["ttl_seconds"] <= 0 or credential["ttl_seconds"] != actual_ttl or not (issued <= now < expires) or credential["status"] != "ACTIVE" or credential["value_visible_to_model"]:
        hard.append("CREDENTIAL_REGISTRY_BINDING_INVALID")

    sandbox = state["sandbox"]
    if sandbox["status"] == "UNKNOWN":
        review.append("SANDBOX_POSTURE_UNKNOWN")
    elif sandbox["status"] != "ACTIVE":
        hard.append("SANDBOX_NOT_ACTIVE")
    if sandbox["mode"] != policy_authority["required_sandbox_mode"] or sandbox["scope"] != "session" or sandbox["backend"] not in {"container", "microvm"} or sandbox["network_default"] != "deny":
        hard.append("SANDBOX_BOUNDARY_INVALID")
    for mount in sandbox["mounts"]:
        normalized = posixpath.normpath(mount["path"])
        within = any(normalized == root or normalized.startswith(root.rstrip("/") + "/") for root in policy_authority["allowed_mount_roots"])
        if normalized != mount["path"] or not within or mount["source"] != "workspace":
            hard.append("SANDBOX_MOUNT_ESCAPE")

    egress = state["egress"]
    egress_authority = registries["egress_policies"].get(egress["policy_ref"])
    if not egress_authority or egress_authority["status"] != "ACTIVE" or egress["policy_ref"] != policy_authority["egress_policy_ref"] or egress["allowed_hosts"] != egress_authority["allowed_hosts"]:
        hard.append("EGRESS_POLICY_AUTHORITY_MISMATCH")
        allowed_hosts: list[str] = []
    else:
        allowed_hosts = egress_authority["allowed_hosts"]
    for request in egress["requests"]:
        hosts = [urlparse(value).hostname for value in [request["url"], *request["redirect_chain"]]]
        if any(not host or host not in allowed_hosts for host in hosts):
            hard.append("EGRESS_DESTINATION_DENY")
        try:
            ip = ipaddress.ip_address(request["resolved_ip"])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
                hard.append("EGRESS_IP_CLASS_DENY")
        except ValueError:
            hard.append("EGRESS_IP_INVALID")
        if request["data_classification"] in {"confidential", "secret"}:
            hard.append("EGRESS_DLP_DENY")

    input_record = state["input"]
    input_authority = registries["input_manifests"].get(input_record["manifest_ref"])
    if not input_authority or input_authority["status"] != "ACTIVE" or input_record["provenance"] != input_authority["provenance"] or input_record["trust"] != input_authority["trust"] or input_record["content_digest"] != input_authority["content_digest"]:
        hard.append("INPUT_PROVENANCE_OR_DIGEST_INVALID")
    if input_record["control_claimed"]:
        hard.append("UNTRUSTED_CONTENT_CLAIMS_CONTROL")

    def compare_component(name: str, registry_name: str, fields: list[str]) -> dict[str, Any] | None:
        component = state[name]
        authority_record = registries[registry_name].get(component["registry_ref"])
        if not authority_record or authority_record["status"] != "ACTIVE" or component["status"] != "ACTIVE" or component["id"] != authority_record["id"] or any(component[field] != authority_record[field] for field in fields):
            hard.append(f"{name.upper()}_SUPPLY_CHAIN_MISMATCH")
        return authority_record

    tool_authority = compare_component("tool", "tools", ["manifest_digest", "implementation_digest", "dependencies"])
    if tool_authority and (action not in tool_authority["allowed_actions"] or obj not in tool_authority["allowed_objects"] or scope not in tool_authority["allowed_scopes"]):
        hard.append("TOOL_CAPABILITY_DENY")
    compare_component("skill", "skills", ["manifest_digest", "dependencies"])
    compare_component("plugin", "plugins", ["manifest_digest", "dependencies", "execution_mode", "capabilities"])
    if state["plugin"]["execution_mode"] == "in_process" and set(state["plugin"]["capabilities"]) & {"process_memory", "network", "secret_read"}:
        hard.append("PLUGIN_NOT_CONTAINED")

    effects = state["effects"]
    effect_ids = [item["effect_id"] for item in effects]
    if len(effect_ids) != len(set(effect_ids)):
        hard.append("DUPLICATE_EFFECT_ID")
    receipts = state["receipts"]
    receipt_ids = [item["receipt_id"] for item in receipts]
    if len(receipt_ids) != len(set(receipt_ids)):
        hard.append("DUPLICATE_RECEIPT_ID")
    effect_by_id = {item["effect_id"]: item for item in effects}
    receipt_by_id = {item["receipt_id"]: item for item in receipts}
    for item in receipts:
        effect = effect_by_id.get(item["effect_id"])
        if not effect or effect["receipt_ref"] != item["receipt_id"]:
            hard.append("ORPHAN_RECEIPT")
    applied = False
    effect_unknown = False
    external_count = 0
    for effect in effects:
        snapshot_digest = digest({key: state[key] for key in ("identity", "tenant_session", "delegation", "policy", "approval", "grant", "credential")})
        if effect["authorized_grant_id"] not in registries["grants"]:
            hard.append("EFFECT_GRANT_UNKNOWN")
        else:
            auth_grant = registries["grants"][effect["authorized_grant_id"]]
            expected_params = digest({"action": auth_grant["action"], "object": auth_grant["object"], "scope": auth_grant["scope"]})
            if (
                effect["action"] != auth_grant["action"]
                or effect["object"] != auth_grant["object"]
                or effect["scope"] != auth_grant["scope"]
                or effect["params_digest"] != expected_params
                or effect["executor"] != auth_grant["actor"]
            ):
                hard.append("EFFECT_NOT_BOUND_TO_GRANT")
        if effect["status"] == "NONE":
            if effect["external_side_effect"] or effect["receipt_ref"] or effect["readback_ref"] or effect["executed_at"]:
                hard.append("NONE_EFFECT_CONTRADICTION")
        else:
            if not effect["executed_at"]:
                hard.append("EFFECT_EXECUTION_TIME_MISSING")
            else:
                executed_at = timestamp(effect["executed_at"], "effect.executed_at")
                if executed_at > now:
                    hard.append("EFFECT_EXECUTION_TIME_INVALID")
                if not all((
                    authority_record_active_at(state["tenant_session"], executed_at, "ACTIVE"),
                    authority_record_active_at(state["delegation"], executed_at, "ACTIVE"),
                    authority_record_active_at(state["approval"], executed_at, "APPROVED"),
                    authority_record_active_at(state["grant"], executed_at, "ACTIVE"),
                    authority_record_active_at(state["credential"], executed_at, "ACTIVE"),
                )):
                    hard.append("EFFECT_EXECUTION_OUTSIDE_AUTHORITY_WINDOW")
                if effect["authorization_snapshot_digest"] != snapshot_digest:
                    hard.append("EFFECT_AUTHORIZATION_SNAPSHOT_INVALID")
        if effect["status"] in {"APPLIED", "FAILED", "UNKNOWN"}:
            if not effect["receipt_ref"] or effect["receipt_ref"] not in receipt_by_id:
                hard.append("EFFECT_RECEIPT_MISSING")
            else:
                item = receipt_by_id[effect["receipt_ref"]]
                if "issued_at" not in item:
                    hard.append("EFFECT_RECEIPT_AUTHORITY_FIELDS_MISSING")
                    continue
                body = {key: value for key, value in item.items() if key != "digest"}
                if item["effect_id"] != effect["effect_id"] or item["digest"] != digest(body):
                    hard.append("EFFECT_RECEIPT_BINDING_INVALID")
                readback = registries["readbacks"].get(effect["readback_ref"])
                if (
                    item["target"] != effect["object"] or item["action"] != effect["action"] or item["scope"] != effect["scope"]
                    or item["executor"] != effect["executor"] or item["executed_at"] != effect["executed_at"]
                    or item["authorization_snapshot_digest"] != effect["authorization_snapshot_digest"]
                ):
                    hard.append("EFFECT_RECEIPT_OBJECT_BINDING_INVALID")
                if not readback or readback["effect_id"] != effect["effect_id"] or readback["receipt_id"] != item["receipt_id"] or readback["object"] != effect["object"] or readback["action"] != effect["action"] or readback["scope"] != effect["scope"] or readback["observer"] == effect["executor"] or readback["authority_ref"] != readback["observer"] or readback["authorization_snapshot_digest"] != snapshot_digest:
                    hard.append("EFFECT_READBACK_AUTHORITY_INVALID")
                else:
                    observer = registries["principals"].get(readback["observer"])
                    receipt_at = timestamp(item["issued_at"], "receipt.issued_at")
                    observed_at = timestamp(readback["observed_at"], "readback.observed_at")
                    executed_at = timestamp(effect["executed_at"], "effect.executed_at")
                    if not observer or observer["status"] != "ACTIVE" or "AUDIT_ANCHOR" not in observer["roles"]:
                        hard.append("EFFECT_READBACK_AUTHORITY_INVALID")
                    if not (executed_at <= receipt_at <= observed_at <= now):
                        hard.append("EFFECT_READBACK_TIME_INVALID")
                    if readback["terminal_status"] != effect["status"] or item["status"] != effect["status"]:
                        hard.append("EFFECT_READBACK_MISMATCH")
        if effect["status"] == "APPLIED":
            applied = True
        if effect["status"] == "UNKNOWN":
            effect_unknown = True
            review.append("EFFECT_TERMINAL_UNKNOWN")
        if effect["external_side_effect"]:
            external_count += 1
    if external_count and not source["environment"]["external_side_effects_permitted"]:
        hard.append("EXTERNAL_EFFECT_CONTRACT_VIOLATION")

    audit = state["audit"]
    anchor = registries["audit_anchors"].get(audit["chain_id"])
    audit_valid = bool(anchor and anchor["status"] == "ACTIVE")
    previous = anchor["initial_digest"] if anchor else ""
    sequence: list[str] = []
    seen: set[str] = set()
    for index, event in enumerate(audit["events"], 1):
        body = {key: event[key] for key in ["seq", "event_id", "event_type", "payload", "prev_digest"]}
        if event["seq"] != index or event["event_id"] in seen or event["prev_digest"] != previous or event["event_digest"] != digest(body):
            audit_valid = False
        seen.add(event["event_id"])
        previous = event["event_digest"]
        sequence.append(f"{event['event_type']}:{event['payload']['outcome']}")
    if not anchor or len(audit["events"]) != anchor["event_count"] or sequence != anchor["allowed_sequence"] or previous != anchor["final_digest"]:
        audit_valid = False
    if not audit_valid:
        hard.append("AUDIT_CHAIN_OR_EXTERNAL_ANCHOR_INVALID")
    if audit["events"]:
        first = audit["events"][0]["payload"]
        if first["subject"] != identity["principal"] or first["action"] != action or first["object"] != obj:
            hard.append("AUDIT_OBJECT_BINDING_INVALID")
    effect_audit_events = {event["payload"]["effect_id"]: event["payload"] for event in audit["events"] if event["event_type"] == "EFFECT"}
    for effect in effects:
        if effect["status"] in {"APPLIED", "FAILED", "UNKNOWN"}:
            payload = effect_audit_events.get(effect["effect_id"])
            receipt = receipt_by_id.get(effect["receipt_ref"])
            readback = registries["readbacks"].get(effect["readback_ref"])
            if not payload or not receipt or not readback or payload["receipt_id"] != receipt["receipt_id"] or payload["readback_id"] != readback["readback_id"] or payload["outcome"] != effect["status"] or payload["effect_digest"] != digest(effect) or payload["receipt_digest"] != receipt["digest"] or payload["readback_digest"] != readback["record_digest"] or payload["executed_at"] != effect["executed_at"] or payload["receipt_issued_at"] != receipt["issued_at"] or payload["readback_observed_at"] != readback["observed_at"]:
                hard.append("TERMINAL_EFFECT_NOT_IN_AUDIT")
    for effect_id, payload in effect_audit_events.items():
        effect = effect_by_id.get(effect_id)
        if not effect or effect["receipt_ref"] != payload["receipt_id"] or effect["readback_ref"] != payload["readback_id"]:
            hard.append("AUDIT_EFFECT_OR_RECEIPT_ORPHAN")

    incident = state["incident"]
    controls_complete = all(incident["controls"].values())
    if incident["state"] == "NONE":
        if any(incident["controls"].values()) or incident["evidence_refs"] or incident["effect_ids"]:
            hard.append("INCIDENT_NONE_CONTRADICTION")
    elif incident["state"] == "UNKNOWN":
        review.append("INCIDENT_STATE_UNKNOWN")
    elif incident["state"] in {"OPEN", "CONTAINED"}:
        if incident["state"] == "OPEN" and not (incident["controls"]["stop"] and incident["controls"]["isolate"]):
            hard.append("OPEN_INCIDENT_MINIMUM_CONTROL_MISSING")
        if incident["state"] == "CONTAINED" and not controls_complete:
            hard.append("INCIDENT_RESPONSE_INCOMPLETE")
        if not incident["evidence_refs"]:
            hard.append("INCIDENT_EVIDENCE_MISSING")
        for ref in incident["evidence_refs"]:
            record = registries["incident_evidence"].get(ref)
            owner = registries["principals"].get(record["owner"]) if record else None
            if not record or record["status"] != "VERIFIED" or record["incident_id"] != incident["incident_id"] or sorted(record["effect_ids"]) != sorted(incident["effect_ids"]) or not owner or owner["status"] != "ACTIVE" or "INCIDENT_OWNER" not in owner["roles"]:
                hard.append("INCIDENT_EVIDENCE_AUTHORITY_INVALID")
        if any(effect_id not in effect_by_id for effect_id in incident["effect_ids"]):
            hard.append("INCIDENT_EFFECT_CHAIN_INVALID")
    if any(item["status"] == "APPLIED" and item["external_side_effect"] for item in effects) and incident["state"] == "NONE":
        hard.append("APPLIED_EXTERNAL_EFFECT_WITHOUT_INCIDENT")

    recovery = state["recovery"]
    residual_owner = registries["principals"].get(recovery["residual_risk_owner"])
    if not residual_owner or residual_owner["status"] != "ACTIVE" or residual_owner["kind"] != "HUMAN" or "ACCOUNTABLE_OWNER" not in residual_owner["roles"]:
        hard.append("RESIDUAL_RISK_OWNER_INVALID")
    if recovery["state"] == "NOT_NEEDED":
        if recovery["regression_pass"] or recovery["evidence_ref"] or recovery["evidence_origin"] != "none" or recovery["target_version"] or recovery["probe_status"] != "NOT_RUN" or recovery["residual_risk_level"] != "NONE" or recovery["residual_risk"] != "none":
            hard.append("RECOVERY_NOT_NEEDED_CONTRADICTION")
    elif recovery["state"] == "PROPOSED":
        if recovery["regression_pass"] or recovery["probe_status"] != "NOT_RUN" or recovery["evidence_ref"]:
            hard.append("RECOVERY_PROPOSED_CONTRADICTION")
    elif recovery["state"] == "UNKNOWN":
        review.append("RECOVERY_UNKNOWN")
    elif recovery["state"] == "REGRESSION_PASS":
        record = registries["recovery_evidence"].get(recovery["evidence_ref"])
        owner = registries["principals"].get(record["owner"]) if record else None
        if incident["state"] != "CONTAINED" or not controls_complete or not recovery["regression_pass"] or recovery["probe_status"] != "PASS" or recovery["residual_risk_level"] in {"HIGH", "CRITICAL", "UNKNOWN"} or not record or record["status"] != "VERIFIED" or record["incident_id"] != incident["incident_id"] or sorted(record["effect_ids"]) != sorted(incident["effect_ids"]) or record["origin"] != recovery["evidence_origin"] or record["target_version"] != recovery["target_version"] or record["probe_status"] != recovery["probe_status"] or not owner or owner["status"] != "ACTIVE" or "RECOVERY_APPROVER" not in owner["roles"]:
            hard.append("RECOVERY_CLOSURE_AUTHORITY_INVALID")
        if recovery["evidence_origin"] == "representative_real_world":
            hard.append("SYNTHETIC_RECOVERY_AS_REAL")

    if effect_unknown:
        d21 = {"technical_execution": "UNKNOWN", "delivery_visibility": "UNKNOWN", "environment_acceptance": "UNKNOWN"}
    elif applied:
        d21 = {"technical_execution": "EXECUTED", "delivery_visibility": "VISIBLE", "environment_acceptance": "REJECTED" if hard else "ACCEPTED"}
    else:
        d21 = {"technical_execution": "NOT_EXECUTED", "delivery_visibility": "NOT_APPLICABLE", "environment_acceptance": "UNCHANGED"}
    decision = "FAIL" if hard else "REVIEW_REQUIRED" if review else "PASS"
    return decision, sorted(set(hard)), sorted(set(review)), {"hard_failures": sorted(set(hard)), "review_items": sorted(set(review)), "external_side_effect_count": external_count, "d21": d21, "audit_chain_valid": audit_valid, "authority_root_digest": authority["root_digest"]}


def build_result(source: dict[str, Any], authority: dict[str, Any]) -> dict[str, Any]:
    trials = []
    for scenario in source["scenarios"]:
        decision, hard, review, derived = evaluate(scenario, source, authority)
        trials.append({"task_id": scenario["task_id"], "trial_id": scenario["trial_id"], "scenario_id": scenario["id"], "layer": scenario["layer"], "security_red_team": scenario["security_red_team"], "synthetic_shadow": scenario["synthetic_shadow"], "decision": decision, "reasons": [*hard, *review], "derived": derived, "raw": copy.deepcopy(scenario["state"])})
    distribution = Counter(item["decision"] for item in trials)
    layers = Counter(item["layer"] for item in trials)
    return {
        "schema_version": "c19.security.result.v2.4",
        "trial_count": len(trials),
        "unique_task_trial": len({(item["task_id"], item["trial_id"]) for item in trials}) == len(trials),
        "distribution": dict(sorted(distribution.items())),
        "layers": {layer: layers[layer] for layer in sorted(LAYERS)},
        "security_red_team_trial_count": sum(item["security_red_team"] for item in trials),
        "representative_real_world_evidence_count": layers["representative_real_world"],
        "external_side_effect_count": sum(item["derived"]["external_side_effect_count"] for item in trials),
        "authority_root_digest": authority["root_digest"],
        "decision_digest": hashlib.sha256(canon(trials).encode()).hexdigest(),
        "trials": trials,
    }


def write_summary(result: dict[str, Any], output: Path) -> None:
    lines = [
        "# C19 v2.4 状态化安全夹具摘要", "",
        "> authority bundle由scenario输入之外的冻结root约束；本包仍是纯离线合成，不证明真实Runtime安全。", "",
        f"- trials: `{result['trial_count']}`",
        f"- distribution: `{result['distribution']}`",
        f"- layers: `{result['layers']}`",
        f"- security/red-team cross-cutting trials: `{result['security_red_team_trial_count']}`",
        f"- representative real-world evidence count: `{result['representative_real_world_evidence_count']}`",
        f"- external side-effect count: `{result['external_side_effect_count']}`",
        f"- authority root digest: `{result['authority_root_digest']}`",
        f"- decision digest: `{result['decision_digest']}`", "",
        "硬失败优先于UNKNOWN；代表性真实层与真实外部副作用均未执行，真实实践门保持REVIEW_REQUIRED。",
    ]
    output.with_name("synthetic-security-summary.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--authority", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    input_path, authority_path, output_path = Path(args.input), Path(args.authority), Path(args.output)
    authority = validate_authority_bundle(json.loads(authority_path.read_text()))
    source = validate_source(json.loads(input_path.read_text()), authority)
    result = build_result(source, authority)
    result["input_sha256"] = hashlib.sha256(input_path.read_bytes()).hexdigest()
    result["authority_sha256"] = hashlib.sha256(authority_path.read_bytes()).hexdigest()
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    write_summary(result, output_path)
    print(result["decision_digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

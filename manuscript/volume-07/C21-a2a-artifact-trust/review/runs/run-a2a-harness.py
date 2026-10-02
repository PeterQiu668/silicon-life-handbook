#!/usr/bin/env python3
"""Deterministic, state-derived C18 A2A/artifact/trust harness."""

from __future__ import annotations

import argparse
import copy
import hashlib
import ipaddress
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


LAYERS = ["training", "regression", "holdout", "representative_real_world"]
VERDICTS = {"PASS", "FAIL", "REVIEW_REQUIRED"}
KINDS = {"normal", "security", "adversarial", "boundary", "abnormal", "recovery"}
PROTOCOL_STATES = {"SUBMITTED", "WORKING", "INPUT_REQUIRED", "AUTH_REQUIRED", "COMPLETED", "FAILED", "CANCELED", "REJECTED"}
TERMINAL_PROTOCOL_STATES = {"COMPLETED", "FAILED", "CANCELED", "REJECTED"}
REQUIRED_SIGNED_ARTIFACT_FIELDS = {
    "artifact_id", "task_id", "object_type", "version", "schema_ref", "content", "producer", "owner",
    "accountable_human", "authority_evidence_ref", "provenance", "tool_receipts", "transformation_chain",
    "retention", "acceptance_evidence_ref", "content_digest",
}


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def parse_time(value: str, path: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{path} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{path} must include a timezone")
    return parsed


def sign(payload: object, signer: str, keys: dict[str, str]) -> str:
    return hashlib.sha256((keys[signer] + "|" + canonical(payload)).encode("utf-8")).hexdigest()


def exact(value: object, required: set[str], optional: set[str], path: str) -> dict:
    if type(value) is not dict:
        raise ValueError(f"{path} must be an object")
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - required - optional)
    if missing:
        raise ValueError(f"{path} missing fields: {missing}")
    if unknown:
        raise ValueError(f"{path} unknown fields: {unknown}")
    return value


def require_type(value: object, expected: type, path: str) -> None:
    if type(value) is not expected:
        raise ValueError(f"{path} must be {expected.__name__}")


def validate_source(source: object) -> dict:
    source = exact(
        source,
        {"schema_version", "seed", "now", "environment", "data_origin", "representative_real_world_executed",
         "synthetic_key_material", "trust_roots", "authority_store", "trusted_approvers", "delegation_store",
         "schema_registry", "capability_probe_store", "stop_receipt_registry", "base_card", "base_task", "base_artifact", "base_events",
         "base_execution", "real_world_evidence_manifest", "allowed_mutations", "scenarios"},
        set(), "root",
    )
    if source["schema_version"] != "c18.synthetic.v3":
        raise ValueError("unsupported schema_version")
    for key in ("seed", "now", "data_origin"):
        require_type(source[key], str, f"root.{key}")
    now = parse_time(source["now"], "root.now")
    if source["data_origin"] != "synthetic":
        raise ValueError("offline synthetic harness cannot attest representative-real-world origin")
    require_type(source["representative_real_world_executed"], bool, "root.representative_real_world_executed")
    if source["representative_real_world_executed"]:
        raise ValueError("offline synthetic harness cannot execute representative-real-world trials")
    environment = exact(source["environment"], {"mode", "real_credentials", "network", "external_side_effects_allowed"}, set(), "root.environment")
    if environment != {"mode":"offline_synthetic","real_credentials":False,"network":False,"external_side_effects_allowed":False}:
        raise ValueError("offline fixture environment contract changed")
    for key in ("synthetic_key_material", "trust_roots", "authority_store", "delegation_store", "schema_registry", "capability_probe_store", "stop_receipt_registry", "real_world_evidence_manifest"):
        require_type(source[key], dict, f"root.{key}")
    for key in ("trusted_approvers", "base_events", "allowed_mutations", "scenarios"):
        require_type(source[key], list, f"root.{key}")
    if len(source["allowed_mutations"]) != len(set(source["allowed_mutations"])):
        raise ValueError("allowed mutations must be unique")

    for signer, root in source["trust_roots"].items():
        root = exact(root, {"status", "provider_org"}, set(), f"root.trust_roots.{signer}")
        if root["status"] not in {"ACTIVE", "REVOKED", "EXPIRED"}:
            raise ValueError(f"root.trust_roots.{signer}.status has unknown enum")
    for authority_id, authority in source["authority_store"].items():
        authority = exact(authority, {"actor", "action", "object", "scope", "not_before", "expires", "status", "approver", "policy_version"}, set(), f"root.authority_store.{authority_id}")
        if authority["status"] not in {"ACTIVE", "REVOKED", "EXPIRED"}:
            raise ValueError(f"root.authority_store.{authority_id}.status has unknown enum")
    for delegation_id, delegation in source["delegation_store"].items():
        delegation = exact(delegation, {"parent_actor", "child_actor", "actions", "objects", "scopes", "not_before", "expires", "status"}, set(), f"root.delegation_store.{delegation_id}")
        if delegation["status"] not in {"ACTIVE", "REVOKED", "EXPIRED"}:
            raise ValueError(f"root.delegation_store.{delegation_id}.status has unknown enum")
    for schema_id, schema in source["schema_registry"].items():
        exact(schema, {"required_content_fields", "allowed_units"}, set(), f"root.schema_registry.{schema_id}")
    for skill, probe in source["capability_probe_store"].items():
        probe = exact(probe, {"status", "task_class", "risk"}, set(), f"root.capability_probe_store.{skill}")
        if probe["status"] not in {"VERIFIED", "FAILED", "UNKNOWN", "EXPIRED"}:
            raise ValueError(f"root.capability_probe_store.{skill}.status has unknown enum")
    for receipt_id, receipt in source["stop_receipt_registry"].items():
        receipt = exact(receipt, {"task_id", "worker", "status", "issued_at", "source", "object_digest"}, set(), f"root.stop_receipt_registry.{receipt_id}")
        for key in receipt:
            require_type(receipt[key], str, f"root.stop_receipt_registry.{receipt_id}.{key}")
        parse_time(receipt["issued_at"], f"root.stop_receipt_registry.{receipt_id}.issued_at")
        body = {key:value for key,value in receipt.items() if key != "object_digest"}
        if receipt["status"] != "VERIFIED" or receipt["source"] != "control-plane" or receipt["object_digest"] != digest(body):
            raise ValueError(f"root.stop_receipt_registry.{receipt_id} is not authoritative")

    validate_card(source["base_card"], "root.base_card", signed=False)
    task = exact(source["base_task"], {"task_id", "owner", "state_version", "current_state", "delegation_ref"}, set(), "root.base_task")
    if task["current_state"] not in PROTOCOL_STATES:
        raise ValueError("root.base_task.current_state has unknown enum")
    validate_artifact(source["base_artifact"], "root.base_artifact", signed=False)
    validate_events(source["base_events"], "root.base_events", allow_gap=False)
    validate_execution(source["base_execution"], "root.base_execution")

    manifest = source["real_world_evidence_manifest"]
    for evidence_id, record in manifest.items():
        record = exact(record, {"verified", "origin", "source_id", "run_id"}, set(), f"root.real_world_evidence_manifest.{evidence_id}")
        require_type(record["verified"], bool, f"root.real_world_evidence_manifest.{evidence_id}.verified")

    scenario_ids: list[str] = []
    real_count = 0
    for index, scenario in enumerate(source["scenarios"]):
        path = f"root.scenarios[{index}]"
        scenario = exact(
            scenario, {"id", "kind", "layer", "security_red_team", "mutations", "expected"},
            {"synthetic_shadow", "intended_target_layer", "real_world_evidence_id", "real_world_source_id"}, path,
        )
        scenario_ids.append(scenario["id"])
        if scenario["kind"] not in KINDS or scenario["layer"] not in LAYERS or scenario["expected"] not in VERDICTS:
            raise ValueError(f"{path} contains invalid enum")
        require_type(scenario["security_red_team"], bool, f"{path}.security_red_team")
        require_type(scenario["mutations"], list, f"{path}.mutations")
        unknown_mutations = sorted(set(scenario["mutations"]) - set(source["allowed_mutations"]))
        if unknown_mutations:
            raise ValueError(f"{path} unknown mutations: {unknown_mutations}")
        if scenario["security_red_team"] != bool(scenario["mutations"]):
            raise ValueError(f"{path}.security_red_team must be derived from mutations")
        if scenario.get("synthetic_shadow") and (scenario["layer"] != "holdout" or scenario.get("intended_target_layer") != "representative_real_world"):
            raise ValueError("synthetic shadow must remain holdout and target representative_real_world")
        if scenario["layer"] == "representative_real_world":
            raise ValueError(f"{path} representative-real-world evidence requires an external evidence gate")
    if len(scenario_ids) != len(set(scenario_ids)):
        raise ValueError("scenario ids must be unique")
    if real_count or source["real_world_evidence_manifest"]:
        raise ValueError("offline synthetic harness cannot self-attest representative-real-world evidence")
    return source


def validate_card(card: object, path: str, *, signed: bool) -> dict:
    required = {"agent_id", "provider_org", "protocol", "supported_interfaces", "endpoint", "skills", "security_schemes", "issued_at", "expires_at", "signer_ref", "revocation_status"}
    if signed:
        required.add("signature")
    card = exact(card, required, set(), path)
    for key in required - {"supported_interfaces", "skills", "security_schemes"}:
        require_type(card[key], str, f"{path}.{key}")
    for key in ("supported_interfaces", "skills", "security_schemes"):
        require_type(card[key], list, f"{path}.{key}")
    if card["revocation_status"] not in {"ACTIVE", "REVOKED", "EXPIRED"}:
        raise ValueError(f"{path}.revocation_status has unknown enum")
    return card


def validate_artifact(artifact: object, path: str, *, signed: bool) -> dict:
    required = {"artifact_id", "task_id", "object_type", "version", "schema_ref", "content", "producer", "owner", "accountable_human", "authority_evidence_ref", "provenance", "tool_receipts", "transformation_chain", "retention", "acceptance_evidence_ref", "signed_fields"}
    if signed:
        required |= {"content_digest", "signature"}
    artifact = exact(artifact, required, set(), path)
    return artifact


def validate_events(events: object, path: str, *, allow_gap: bool) -> list:
    require_type(events, list, path)
    for index, event in enumerate(events):
        event = exact(event, {"event_id", "sequence", "task_id", "state_version", "protocol_state"}, {"artifact_ref"}, f"{path}[{index}]")
        if event["protocol_state"] not in PROTOCOL_STATES:
            raise ValueError(f"{path}[{index}].protocol_state has unknown enum")
    return events


def validate_execution(execution: object, path: str) -> dict:
    execution = exact(execution, {"worker_state", "descendants", "locks_released", "cancel", "effect_ledger", "stop_receipt", "authoritative_readback"}, set(), path)
    if execution["worker_state"] not in {"ACTIVE", "STOPPED", "FAILED", "UNKNOWN"}:
        raise ValueError(f"{path}.worker_state has unknown enum")
    exact(execution["cancel"], {"requested", "ack"}, set(), f"{path}.cancel")
    if execution["cancel"]["ack"] not in {"NONE", "ACCEPTED", "REJECTED", "UNKNOWN"}:
        raise ValueError(f"{path}.cancel.ack has unknown enum")
    exact(execution["stop_receipt"], {"status", "receipt_id"}, set(), f"{path}.stop_receipt")
    if execution["stop_receipt"]["status"] not in {"VERIFIED", "MISSING", "FAILED", "UNKNOWN"}:
        raise ValueError(f"{path}.stop_receipt.status has unknown enum")
    exact(execution["authoritative_readback"], {"worker", "queue", "inflight"}, set(), f"{path}.authoritative_readback")
    for index, child in enumerate(execution["descendants"]):
        child = exact(child, {"id", "state"}, set(), f"{path}.descendants[{index}]")
        if child["state"] not in {"ACTIVE", "COMPLETED", "FAILED", "CANCELED", "UNKNOWN"}:
            raise ValueError(f"{path}.descendants[{index}].state has unknown enum")
    for index, effect in enumerate(execution["effect_ledger"]):
        effect = exact(effect, {"effect_id", "status", "confirmed_external_write"}, set(), f"{path}.effect_ledger[{index}]")
        if effect["status"] not in {"PENDING", "APPLIED", "FAILED", "UNKNOWN", "RECONCILED"}:
            raise ValueError(f"{path}.effect_ledger[{index}].status has unknown enum")
        require_type(effect["confirmed_external_write"], bool, f"{path}.effect_ledger[{index}].confirmed_external_write")
    return execution


def materialize(source: dict, scenario: dict) -> dict:
    card = copy.deepcopy(source["base_card"])
    task = copy.deepcopy(source["base_task"])
    artifact = copy.deepcopy(source["base_artifact"])
    events = copy.deepcopy(source["base_events"])
    execution = copy.deepcopy(source["base_execution"])
    authority_ref = artifact["authority_evidence_ref"]
    trust = {"score":92,"evidence":["run-1","run-2"],"peer_reviews":[]}
    mutations = set(scenario["mutations"])

    if "expired_card_cache" in mutations:
        card["expires_at"] = "2026-09-29T00:00:00Z"
    if "inflated_skill" in mutations:
        card["skills"].append("payment_execute")
    if "event_gap" in mutations:
        for event in events[1:]:
            event["sequence"] += 1
    if "timeout_remote_running" in mutations:
        events = events[:2]
        task["current_state"] = "WORKING"
        task["state_version"] = 2
        execution = {
            **execution,
            "worker_state":"ACTIVE",
            "descendants":[{"id":"child-1","state":"ACTIVE"}],
            "locks_released":False,
            "stop_receipt":{"status":"UNKNOWN","receipt_id":"NONE"},
            "authoritative_readback":{"worker":"UNKNOWN","queue":"UNKNOWN","inflight":"UNKNOWN"},
        }
    if "cancel_ack_effect_pending" in mutations:
        events = events[:2]
        next_sequence = max(event["sequence"] for event in events) + 1
        events.append({"event_id":"cancel-ack","sequence":next_sequence,"task_id":"task-001","state_version":3,"protocol_state":"CANCELED"})
        task["current_state"] = "CANCELED"
        task["state_version"] = 3
        execution = {
            **execution,
            "worker_state":"ACTIVE",
            "descendants":[{"id":"child-1","state":"ACTIVE"}],
            "locks_released":False,
            "cancel":{"requested":True,"ack":"ACCEPTED"},
            "effect_ledger":[{"effect_id":"effect-1","status":"PENDING","confirmed_external_write":False}],
            "stop_receipt":{"status":"MISSING","receipt_id":"NONE"},
            "authoritative_readback":{"worker":"ACTIVE","queue":"NOT_CLEAR","inflight":"NOT_CLEAR"},
        }
    if "signed_content_wrong" in mutations:
        artifact["content"]["unit"] = "USD"
    if "high_trust_no_authority" in mutations:
        authority_ref = "missing-auth"
        artifact["authority_evidence_ref"] = authority_ref
    if "collusive_scoring" in mutations:
        trust["peer_reviews"] = [{"from":"agent-a","to":"agent-b","score":100},{"from":"agent-b","to":"agent-a","score":100}]
    if "duplicate_event" in mutations:
        events.append(copy.deepcopy(events[-1]))
    if "duplicate_id_different_payload" in mutations:
        events.append({"event_id":"e3","sequence":4,"task_id":"task-001","state_version":4,"protocol_state":"FAILED"})

    card_payload = copy.deepcopy(card)
    card["signature"] = sign(card_payload, card["signer_ref"], source["synthetic_key_material"])
    cache = {"fetched_at":"2026-09-30T00:01:00Z","card_digest":digest(card),"cache_status":"ACTIVE"}
    artifact["content_digest"] = digest(artifact["content"])
    artifact_payload = {key: artifact[key] for key in artifact["signed_fields"]}
    artifact["signature"] = {"signer_ref":"issuer-good","value":sign(artifact_payload,"issuer-good",source["synthetic_key_material"])}
    acceptance = {
        "evidence_id":"accept-art-001","artifact_id":"art-001","artifact_digest":artifact["content_digest"],
        "delivery_visibility":"VISIBLE","business_acceptance":"ACCEPTED","environment_acceptance":"ACCEPTED","status":"VERIFIED"
    }
    if "forged_card_signature" in mutations:
        card["signature"] = "forged"
    if "artifact_digest_mismatch" in mutations:
        artifact["content"]["amount"] = 101
    return {
        "card":card,"cache":cache,"task_snapshot":task,"events":events,"execution":execution,"artifact":artifact,
        "authority_evidence_ref":authority_ref,"trust_evidence":trust,"acceptance_evidence":acceptance,
    }


def endpoint_safe(endpoint: str) -> bool:
    parsed = urlparse(endpoint)
    if parsed.scheme != "https" or not parsed.hostname:
        return False
    try:
        address = ipaddress.ip_address(parsed.hostname)
    except ValueError:
        return True
    return not (address.is_private or address.is_loopback or address.is_link_local or address.is_reserved)


def evaluate(raw: dict, source: dict) -> tuple[str, list[str], dict, int]:
    reasons: list[str] = []
    review_reasons: list[str] = []
    card = validate_card(raw["card"], "raw.card", signed=True)
    artifact = validate_artifact(raw["artifact"], "raw.artifact", signed=True)
    validate_events(raw["events"], "raw.events", allow_gap=True)
    execution = validate_execution(raw["execution"], "raw.execution")

    signer = card["signer_ref"]
    root = source["trust_roots"].get(signer)
    card_payload = {key:value for key,value in card.items() if key != "signature"}
    if not root or root["status"] != "ACTIVE" or root["provider_org"] != card["provider_org"]:
        reasons.append("CARD_TRUST_ROOT_INVALID")
    elif card["signature"] != sign(card_payload, signer, source["synthetic_key_material"]):
        reasons.append("CARD_SIGNATURE_INVALID")
    if raw["cache"]["card_digest"] != digest(card):
        reasons.append("CARD_CACHE_DIGEST_MISMATCH")
    if card["revocation_status"] != "ACTIVE":
        reasons.append("CARD_REVOKED")
    if card["expires_at"] <= source["now"]:
        review_reasons.append("CARD_EXPIRED")
    if card["protocol"] != "1.0" or "json-rpc" not in card["supported_interfaces"] or "bearer" not in card["security_schemes"]:
        reasons.append("CARD_INTERFACE_OR_SECURITY_UNSUPPORTED")
    if not endpoint_safe(card["endpoint"]):
        reasons.append("CARD_ENDPOINT_POLICY_DENIED")
    for skill in card["skills"]:
        probe = source["capability_probe_store"].get(skill)
        if not probe or probe["status"] != "VERIFIED" or probe["risk"] != "high":
            review_reasons.append("CAPABILITY_UNPROVEN")

    task = raw["task_snapshot"]
    delegation = source["delegation_store"].get(task["delegation_ref"])
    authority = source["authority_store"].get(raw["authority_evidence_ref"])
    if (
        not delegation or delegation["status"] != "ACTIVE" or delegation["child_actor"] != card["agent_id"]
        or not (delegation["not_before"] <= source["now"] < delegation["expires"])
        or "produce" not in delegation["actions"] or "report" not in delegation["objects"] or "local" not in delegation["scopes"]
    ):
        reasons.append("DELEGATION_INVALID_OR_EXPANDED")
    if (
        not authority or authority["status"] != "ACTIVE"
        or not (authority["not_before"] <= source["now"] < authority["expires"])
        or authority["actor"] != card["agent_id"] or authority["actor"] != task["owner"] or authority["actor"] != artifact["producer"]
        or authority["action"] != "produce" or authority["object"] != artifact["object_type"] or authority["scope"] != "local"
        or authority["approver"] not in source["trusted_approvers"] or authority["approver"] == authority["actor"]
        or authority["policy_version"] != "policy-v2" or artifact["authority_evidence_ref"] != raw["authority_evidence_ref"]
    ):
        reasons.append("AUTHORITY_BINDING_INVALID")

    seen: dict[str, dict] = {}
    unique_events: list[dict] = []
    for event in raw["events"]:
        if event["event_id"] in seen:
            if seen[event["event_id"]] != event:
                reasons.append("DUPLICATE_ID_CONFLICT")
            continue
        seen[event["event_id"]] = event
        unique_events.append(event)
    ordered = sorted(unique_events, key=lambda item: item["sequence"])
    sequences = [event["sequence"] for event in ordered]
    if sequences and sequences != list(range(min(sequences), max(sequences) + 1)):
        review_reasons.append("EVENT_SEQUENCE_GAP")
    terminal_seen = False
    previous_state = None
    allowed = {
        None:{"SUBMITTED"}, "SUBMITTED":{"WORKING","FAILED","CANCELED","REJECTED"},
        "WORKING":{"INPUT_REQUIRED","AUTH_REQUIRED","COMPLETED","FAILED","CANCELED","REJECTED"},
        "INPUT_REQUIRED":{"WORKING","FAILED","CANCELED","REJECTED"},
        "AUTH_REQUIRED":{"WORKING","FAILED","CANCELED","REJECTED"},
    }
    for event in ordered:
        if event["task_id"] != task["task_id"] or event["state_version"] <= 0:
            reasons.append("EVENT_TASK_OR_VERSION_INVALID")
        state = event["protocol_state"]
        if terminal_seen:
            reasons.append("TERMINAL_STATE_REGRESSION")
        elif state not in allowed.get(previous_state, set()):
            reasons.append("ILLEGAL_STATE_TRANSITION")
        if state in TERMINAL_PROTOCOL_STATES:
            terminal_seen = True
        previous_state = state
    protocol_state = ordered[-1]["protocol_state"] if ordered else "UNKNOWN"
    if protocol_state != task["current_state"] or (ordered and ordered[-1]["state_version"] != task["state_version"]):
        reasons.append("TASK_SNAPSHOT_MISMATCH")
    if protocol_state in {"FAILED", "REJECTED"}:
        reasons.append("PROTOCOL_TERMINAL_FAILURE")
        protocol_gate = "FAIL"
    elif protocol_state == "COMPLETED":
        protocol_gate = "PASS"
    else:
        review_reasons.append("PROTOCOL_NOT_COMPLETED")
        protocol_gate = "REVIEW_REQUIRED"

    if artifact["task_id"] != task["task_id"] or artifact["producer"] != card["agent_id"] or not artifact["owner"] or not artifact["accountable_human"]:
        reasons.append("ARTIFACT_IDENTITY_OR_TASK_MISMATCH")
    if set(artifact["signed_fields"]) != REQUIRED_SIGNED_ARTIFACT_FIELDS:
        reasons.append("ARTIFACT_SIGNED_FIELDS_INCOMPLETE")
    if artifact["content_digest"] != digest(artifact["content"]):
        reasons.append("ARTIFACT_DIGEST_MISMATCH")
    artifact_payload = {key:artifact[key] for key in artifact["signed_fields"] if key in artifact}
    artifact_signer = artifact["signature"]["signer_ref"]
    artifact_root = source["trust_roots"].get(artifact_signer)
    if (
        artifact_signer not in source["synthetic_key_material"]
        or not artifact_root or artifact_root["status"] != "ACTIVE"
        or artifact_root["provider_org"] != artifact["owner"]
        or artifact["signature"]["value"] != sign(artifact_payload, artifact_signer, source["synthetic_key_material"])
    ):
        reasons.append("ARTIFACT_SIGNATURE_INVALID")
    schema = source["schema_registry"].get(artifact["schema_ref"])
    if not schema or not set(schema["required_content_fields"]).issubset(artifact["content"]):
        reasons.append("ARTIFACT_SCHEMA_INVALID")
    elif artifact["content"].get("unit") not in schema["allowed_units"]:
        reasons.append("CONTENT_BUSINESS_ERROR")
    if not artifact["provenance"] or not artifact["tool_receipts"] or not artifact["transformation_chain"] or not artifact["retention"]:
        reasons.append("ARTIFACT_PROVENANCE_OR_RETENTION_MISSING")

    external_effects = sum(int(effect["status"] == "APPLIED" and effect["confirmed_external_write"]) for effect in execution["effect_ledger"])
    if external_effects and not source["environment"]["external_side_effects_allowed"]:
        reasons.append("EXTERNAL_EFFECT_CONTRACT_VIOLATED")
    execution_unknown = (
        execution["worker_state"] == "UNKNOWN"
        or any(child["state"] == "UNKNOWN" for child in execution["descendants"])
        or execution["stop_receipt"]["status"] == "UNKNOWN"
        or "UNKNOWN" in execution["authoritative_readback"].values()
        or any(effect["status"] == "UNKNOWN" for effect in execution["effect_ledger"])
    )
    receipt_ref = execution["stop_receipt"]["receipt_id"]
    receipt = source["stop_receipt_registry"].get(receipt_ref)
    receipt_age_seconds = (parse_time(source["now"], "root.now") - parse_time(receipt["issued_at"], "stop_receipt.issued_at")).total_seconds() if receipt else -1
    receipt_valid = bool(
        receipt_ref not in {"", "NONE", "dummy", "placeholder"}
        and receipt
        and receipt["task_id"] == task["task_id"]
        and receipt["worker"] == card["agent_id"]
        and receipt["status"] == "VERIFIED"
        and 0 <= receipt_age_seconds <= 300
    )
    execution_stopped = (
        execution["worker_state"] in {"STOPPED", "FAILED"}
        and all(child["state"] in {"COMPLETED", "FAILED", "CANCELED"} for child in execution["descendants"])
        and execution["locks_released"]
        and all(effect["status"] in {"FAILED", "RECONCILED"} for effect in execution["effect_ledger"])
        and execution["stop_receipt"]["status"] == "VERIFIED"
        and receipt_valid
        and execution["authoritative_readback"] == {"worker":"STOPPED","queue":"CLEAR","inflight":"CLEAR"}
    )
    if execution_unknown:
        review_reasons.append("EXECUTION_TERMINAL_UNKNOWN")
    elif not execution_stopped:
        review_reasons.append("EXECUTION_NOT_STOP_CONFIRMED")
    execution_state = "STOP_CONFIRMED" if execution_stopped else "UNKNOWN"

    acceptance = raw["acceptance_evidence"]
    acceptance = exact(acceptance, {"evidence_id", "artifact_id", "artifact_digest", "delivery_visibility", "business_acceptance", "environment_acceptance", "status"}, set(), "raw.acceptance_evidence")
    if (
        acceptance["evidence_id"] != artifact["acceptance_evidence_ref"] or acceptance["artifact_id"] != artifact["artifact_id"]
        or acceptance["artifact_digest"] != artifact["content_digest"] or acceptance["status"] != "VERIFIED"
        or acceptance["delivery_visibility"] != "VISIBLE" or acceptance["business_acceptance"] != "ACCEPTED"
        or acceptance["environment_acceptance"] != "ACCEPTED"
    ):
        reasons.append("ACCEPTANCE_EVIDENCE_INVALID")

    peers = raw["trust_evidence"]["peer_reviews"]
    if peers and {(item["from"], item["to"]) for item in peers} == {("agent-a","agent-b"),("agent-b","agent-a")}:
        reasons.append("COLLUSIVE_TRUST")
    if reasons:
        decision = "FAIL"
    elif review_reasons:
        decision = "REVIEW_REQUIRED"
    else:
        decision = "PASS"
    acceptance_failure_codes = {
        "AUTHORITY_BINDING_INVALID", "ARTIFACT_IDENTITY_OR_TASK_MISMATCH",
        "ARTIFACT_SIGNED_FIELDS_INCOMPLETE", "ARTIFACT_DIGEST_MISMATCH",
        "ARTIFACT_SIGNATURE_INVALID", "ARTIFACT_SCHEMA_INVALID",
        "CONTENT_BUSINESS_ERROR", "ARTIFACT_PROVENANCE_OR_RETENTION_MISSING",
        "ACCEPTANCE_EVIDENCE_INVALID", "COLLUSIVE_TRUST",
    }
    acceptance_gate = "FAIL" if acceptance_failure_codes.intersection(reasons) else "PASS"
    return decision, reasons + review_reasons, {
        "protocol_state":protocol_state,
        "protocol_gate":protocol_gate,
        "execution_state":execution_state,
        "acceptance_state":acceptance_gate,
        "task_completion":decision,
        "artifact_signature_valid":"ARTIFACT_SIGNATURE_INVALID" not in reasons,
    }, external_effects


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    source = validate_source(json.loads(input_path.read_text(encoding="utf-8")))
    trials = []
    for scenario in source["scenarios"]:
        raw = materialize(source, scenario)
        decision, reasons, states, external_effects = evaluate(raw, source)
        trials.append({
            "task_id":f"C18-{scenario['id']}", "trial_id":f"C18-{scenario['id']}-T1",
            "scenario_kind":scenario["kind"], "layer":scenario["layer"],
            "security_red_team":scenario["security_red_team"],
            "synthetic_shadow":bool(scenario.get("synthetic_shadow", False)),
            "intended_target_layer":scenario.get("intended_target_layer"),
            "mutations":scenario["mutations"], "expected":scenario["expected"],
            "raw":raw, "derived":{"decision":decision,"reasons":reasons,"states":states},
            "matched_expected":decision == scenario["expected"], "external_side_effects":external_effects,
        })
    if not all(trial["matched_expected"] for trial in trials):
        raise ValueError("one or more decisions do not match the frozen offline oracle")
    pairs = [(trial["task_id"], trial["trial_id"]) for trial in trials]
    if len(pairs) != len(set(pairs)):
        raise ValueError("task/trial pairs must be unique")
    by_layer = {layer:Counter() for layer in LAYERS}
    for trial in trials:
        by_layer[trial["layer"]][trial["derived"]["decision"]] += 1
    real_count = sum(trial["layer"] == "representative_real_world" for trial in trials)
    payload = canonical(trials)
    output = {
        "schema_version":"c18.synthetic.result.v3",
        "input_digest":hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "trial_count":len(trials),
        "distribution":dict(sorted(Counter(trial["derived"]["decision"] for trial in trials).items())),
        "by_layer":{key:dict(sorted(value.items())) for key,value in sorted(by_layer.items())},
        "security_red_team_trial_count":sum(trial["security_red_team"] for trial in trials),
        "representative_real_world_executed":bool(real_count),
        "representative_real_world_evidence_count":real_count,
        "synthetic_shadow_trial_count":sum(trial["synthetic_shadow"] for trial in trials),
        "external_side_effect_count":sum(trial["external_side_effects"] for trial in trials),
        "decision_digest":hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "all_expected_matched":True,
        "trials":trials,
    }
    output_text = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
    output_path.write_text(output_text, encoding="utf-8")
    summary_path = output_path.with_name("synthetic-a2a-summary.md")
    summary = [
        "# C18 离线 A2A/Artifact/Trust 实验摘要", "",
        "> v3 状态化合成控制；不证明真实 A2A/OpenClaw/Hermes 互操作、真实授权或生产终态。", "",
        f"- trials: `{output['trial_count']}`",
        f"- distribution: `{output['distribution']}`",
        f"- decision digest: `{output['decision_digest']}`",
        f"- representative real-world: `{output['representative_real_world_evidence_count']}`",
        f"- synthetic shadow: `{output['synthetic_shadow_trial_count']}`",
        f"- external effects: `{output['external_side_effect_count']}`",
        f"- expected matched: `{output['all_expected_matched']}`", "", "## D22 layers", "",
    ]
    for layer, values in output["by_layer"].items():
        summary.append(f"- {layer}: `{values}`")
    summary_text = "\n".join(summary) + "\n"
    summary_path.write_text(summary_text, encoding="utf-8")
    print(output["decision_digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Deterministic, state-derived C17 routing/handoff/concurrency harness."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

LAYERS = ["training", "regression", "holdout", "representative_real_world"]
KINDS = {"normal", "security", "adversarial", "boundary", "abnormal", "recovery"}
SHA256_REF = re.compile(r"^sha256:[0-9a-f]{64}$")


def exact_keys(value: object, required: set[str], optional: set[str], path: str) -> dict:
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


def require_number(value: object, path: str) -> None:
    if type(value) not in {int, float}:
        raise ValueError(f"{path} must be a number")


def validate_observation(observation: object, path: str) -> None:
    obs = exact_keys(
        observation,
        {"route", "yield", "handoff", "writer_leases", "effect_ledger", "cancel",
         "wait_edges", "progress", "branches", "receipt", "d21"},
        set(), path,
    )
    route = exact_keys(
        obs["route"],
        {"task_version", "permission_snapshot", "capability_evidence_refs", "current_load",
         "task_load", "capacity", "estimated_cost", "execution_location", "allowed_data_locations"},
        set(), f"{path}.route",
    )
    require_type(route["task_version"], int, f"{path}.route.task_version")
    for key in ("current_load", "task_load", "capacity", "estimated_cost"):
        require_number(route[key], f"{path}.route.{key}")
    for key in ("permission_snapshot", "execution_location"):
        require_type(route[key], str, f"{path}.route.{key}")
    for key in ("capability_evidence_refs", "allowed_data_locations"):
        require_type(route[key], list, f"{path}.route.{key}")
        if not all(type(item) is str for item in route[key]):
            raise ValueError(f"{path}.route.{key} must contain strings")

    yielded = exact_keys(obs["yield"], {"agent_status", "notice"}, set(), f"{path}.yield")
    require_type(yielded["agent_status"], str, f"{path}.yield.agent_status")
    if yielded["notice"] is not None:
        notice = exact_keys(
            yielded["notice"], {"reason", "completed", "not_completed", "safe_stop"}, set(),
            f"{path}.yield.notice",
        )
        for key in ("reason", "safe_stop"):
            require_type(notice[key], str, f"{path}.yield.notice.{key}")
        for key in ("completed", "not_completed"):
            require_type(notice[key], list, f"{path}.yield.notice.{key}")
            if not all(type(item) is str for item in notice[key]):
                raise ValueError(f"{path}.yield.notice.{key} must contain strings")

    handoff = exact_keys(
        obs["handoff"],
        {"card_version", "ack_card_version", "transport_ack", "object_ack", "responsibility_ack",
         "old_owner_released", "owner_cas_succeeded", "transfer_targets",
         "accepted_responsibility_owners", "secret_material"},
        set(), f"{path}.handoff",
    )
    for key in ("card_version", "ack_card_version"):
        require_type(handoff[key], int, f"{path}.handoff.{key}")
    for key in ("transport_ack", "object_ack", "responsibility_ack"):
        require_type(handoff[key], str, f"{path}.handoff.{key}")
    for key in ("old_owner_released", "owner_cas_succeeded"):
        require_type(handoff[key], bool, f"{path}.handoff.{key}")
    for key in ("transfer_targets", "accepted_responsibility_owners", "secret_material"):
        require_type(handoff[key], list, f"{path}.handoff.{key}")
        if not all(type(item) is str for item in handoff[key]):
            raise ValueError(f"{path}.handoff.{key} must contain strings")

    require_type(obs["writer_leases"], list, f"{path}.writer_leases")
    for index, lease in enumerate(obs["writer_leases"]):
        item_path = f"{path}.writer_leases[{index}]"
        lease = exact_keys(lease, {"object_id", "writer_id", "generation", "status"}, set(), item_path)
        require_type(lease["generation"], int, f"{item_path}.generation")
        for key in ("object_id", "writer_id", "status"):
            require_type(lease[key], str, f"{item_path}.{key}")
        if lease["status"] not in {"ACTIVE", "RELEASED", "EXPIRED"}:
            raise ValueError(f"{item_path}.status has unknown enum")

    require_type(obs["effect_ledger"], list, f"{path}.effect_ledger")
    for index, entry in enumerate(obs["effect_ledger"]):
        item_path = f"{path}.effect_ledger[{index}]"
        entry = exact_keys(
            entry, {"logical_action_id", "attempt_id", "idempotency_key", "status", "confirmed_external_write"},
            set(), item_path,
        )
        for key in ("logical_action_id", "attempt_id", "idempotency_key", "status"):
            require_type(entry[key], str, f"{item_path}.{key}")
        require_type(entry["confirmed_external_write"], bool, f"{item_path}.confirmed_external_write")
        if entry["status"] not in {"PENDING", "APPLIED", "DEDUPED", "FAILED", "UNKNOWN"}:
            raise ValueError(f"{item_path}.status has unknown enum")

    cancel = exact_keys(
        obs["cancel"], {"state", "requested_at", "writes", "all_branches_stopped", "locks_released", "effects_reconciled"},
        set(), f"{path}.cancel",
    )
    require_type(cancel["state"], str, f"{path}.cancel.state")
    if cancel["requested_at"] is not None:
        require_type(cancel["requested_at"], str, f"{path}.cancel.requested_at")
    require_type(cancel["writes"], list, f"{path}.cancel.writes")
    for index, write in enumerate(cancel["writes"]):
        write = exact_keys(write, {"at", "object"}, set(), f"{path}.cancel.writes[{index}]")
        require_type(write["at"], str, f"{path}.cancel.writes[{index}].at")
        require_type(write["object"], str, f"{path}.cancel.writes[{index}].object")
    for key in ("all_branches_stopped", "locks_released", "effects_reconciled"):
        require_type(cancel[key], bool, f"{path}.cancel.{key}")

    require_type(obs["wait_edges"], list, f"{path}.wait_edges")
    if not all(type(edge) is list and len(edge) == 2 and all(type(node) is str for node in edge)
               for edge in obs["wait_edges"]):
        raise ValueError(f"{path}.wait_edges must contain two-node string edges")
    progress = exact_keys(
        obs["progress"], {"transition_count", "transition_limit", "progress_delta", "reroute_count", "reroute_limit"},
        set(), f"{path}.progress",
    )
    for key in progress:
        require_number(progress[key], f"{path}.progress.{key}")
    branches = exact_keys(obs["branches"], {"required", "completed"}, set(), f"{path}.branches")
    for key in branches:
        require_type(branches[key], list, f"{path}.branches.{key}")
        if not all(type(item) is str for item in branches[key]):
            raise ValueError(f"{path}.branches.{key} must contain strings")
    receipt = exact_keys(obs["receipt"], {"state", "authoritative_readback"}, set(), f"{path}.receipt")
    for key in receipt:
        require_type(receipt[key], str, f"{path}.receipt.{key}")
    d21 = exact_keys(
        obs["d21"],
        {"reported_complete", "technical_execution_ref", "delivery_visibility_ref", "business_environment_acceptance_ref"},
        set(), f"{path}.d21",
    )
    require_type(d21["reported_complete"], bool, f"{path}.d21.reported_complete")
    for key in ("technical_execution_ref", "delivery_visibility_ref", "business_environment_acceptance_ref"):
        require_type(d21[key], str, f"{path}.d21.{key}")


def deep_merge(base: dict, override: dict) -> dict:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def has_cycle(edges: list[list[str]]) -> bool:
    graph: dict[str, list[str]] = defaultdict(list)
    for source, target in edges:
        graph[source].append(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(child) for child in graph[node]):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in list(graph))


def validate(source: dict) -> None:
    required = {
        "schema_version", "seed", "environment", "data_origin",
        "representative_real_world_executed", "common_contract",
        "state", "common_observation", "scenarios",
    }
    exact_keys(source, required, set(), "root")
    if source["schema_version"] != "c17.synthetic.v3":
        raise ValueError("unsupported schema_version")
    require_type(source["seed"], str, "root.seed")
    environment = exact_keys(
        source["environment"], {"mode", "real_credentials", "external_side_effects"}, set(), "root.environment"
    )
    require_type(environment["mode"], str, "root.environment.mode")
    require_type(environment["real_credentials"], bool, "root.environment.real_credentials")
    require_type(environment["external_side_effects"], bool, "root.environment.external_side_effects")
    require_type(source["data_origin"], str, "root.data_origin")
    if source["data_origin"] not in {"synthetic", "representative_real_world"}:
        raise ValueError("root.data_origin has unknown enum")
    require_type(source["representative_real_world_executed"], bool, "root.representative_real_world_executed")
    contract = source["common_contract"]
    exact_keys(
        contract, {"task_version", "risk", "budget_units", "permission_snapshot", "input_digest"}, set(),
        "root.common_contract",
    )
    require_type(contract["task_version"], int, "root.common_contract.task_version")
    require_number(contract["budget_units"], "root.common_contract.budget_units")
    for key in ("risk", "permission_snapshot", "input_digest"):
        require_type(contract[key], str, f"root.common_contract.{key}")
    state = exact_keys(
        source["state"],
        {"authorized_permission_snapshots", "external_effects_allowed", "completion_evidence_registry",
         "completion_evidence_authority", "capability_evidence_registry",
         "capability_evidence_authority"},
        {"real_world_evidence_manifest"}, "root.state",
    )
    require_type(state["authorized_permission_snapshots"], list, "root.state.authorized_permission_snapshots")
    require_type(state["external_effects_allowed"], bool, "root.state.external_effects_allowed")
    if environment["external_side_effects"] != state["external_effects_allowed"]:
        raise ValueError("environment/state external-effect contract mismatch")
    registry = state["completion_evidence_registry"]
    require_type(registry, dict, "root.state.completion_evidence_registry")
    for evidence_id, record in registry.items():
        require_type(evidence_id, str, "root.state.completion_evidence_registry key")
        record = exact_keys(
            record, {"layer", "source", "observed_terminal", "object_digest", "authoritative", "status"}, set(),
            f"root.state.completion_evidence_registry.{evidence_id}",
        )
        for key in ("layer", "source", "observed_terminal", "object_digest", "status"):
            require_type(record[key], str, f"root.state.completion_evidence_registry.{evidence_id}.{key}")
        require_type(record["authoritative"], bool, f"root.state.completion_evidence_registry.{evidence_id}.authoritative")
        if not SHA256_REF.fullmatch(record["object_digest"]):
            raise ValueError(f"root.state.completion_evidence_registry.{evidence_id}.object_digest must be sha256:<64 lowercase hex>")
        if record["layer"] not in {"technical_execution", "delivery_visibility", "business_environment_acceptance"}:
            raise ValueError(f"root.state.completion_evidence_registry.{evidence_id}.layer has unknown enum")
        if record["status"] not in {"VERIFIED", "FAILED", "UNKNOWN", "REVOKED"}:
            raise ValueError(f"root.state.completion_evidence_registry.{evidence_id}.status has unknown enum")
        if not record["source"]:
            raise ValueError(f"root.state.completion_evidence_registry.{evidence_id}.source must be non-empty")
    authority = state["completion_evidence_authority"]
    require_type(authority, dict, "root.state.completion_evidence_authority")
    for evidence_id, record in authority.items():
        require_type(evidence_id, str, "root.state.completion_evidence_authority key")
        record = exact_keys(
            record, {"layer", "source", "object_digest"}, set(),
            f"root.state.completion_evidence_authority.{evidence_id}",
        )
        for key in ("layer", "source", "object_digest"):
            require_type(record[key], str, f"root.state.completion_evidence_authority.{evidence_id}.{key}")
        if record["layer"] not in {"technical_execution", "delivery_visibility", "business_environment_acceptance"}:
            raise ValueError(f"root.state.completion_evidence_authority.{evidence_id}.layer has unknown enum")
        if not record["source"] or not SHA256_REF.fullmatch(record["object_digest"]):
            raise ValueError(f"root.state.completion_evidence_authority.{evidence_id} has invalid source or digest")
    capabilities = state["capability_evidence_registry"]
    require_type(capabilities, dict, "root.state.capability_evidence_registry")
    for evidence_id, record in capabilities.items():
        require_type(evidence_id, str, "root.state.capability_evidence_registry key")
        record = exact_keys(
            record, {"capability", "task_version", "permission_snapshot", "status", "evidence_digest"}, set(),
            f"root.state.capability_evidence_registry.{evidence_id}",
        )
        require_type(record["capability"], str, f"root.state.capability_evidence_registry.{evidence_id}.capability")
        require_type(record["task_version"], int, f"root.state.capability_evidence_registry.{evidence_id}.task_version")
        require_type(record["permission_snapshot"], str, f"root.state.capability_evidence_registry.{evidence_id}.permission_snapshot")
        require_type(record["status"], str, f"root.state.capability_evidence_registry.{evidence_id}.status")
        require_type(record["evidence_digest"], str, f"root.state.capability_evidence_registry.{evidence_id}.evidence_digest")
        if record["status"] not in {"VERIFIED", "FAILED", "UNKNOWN", "REVOKED"}:
            raise ValueError(f"root.state.capability_evidence_registry.{evidence_id}.status has unknown enum")
        if not SHA256_REF.fullmatch(record["evidence_digest"]):
            raise ValueError(f"root.state.capability_evidence_registry.{evidence_id}.evidence_digest must be sha256:<64 lowercase hex>")
    capability_authority = state["capability_evidence_authority"]
    require_type(capability_authority, dict, "root.state.capability_evidence_authority")
    for evidence_id, record in capability_authority.items():
        require_type(evidence_id, str, "root.state.capability_evidence_authority key")
        record = exact_keys(
            record, {"capability", "task_version", "permission_snapshot", "status", "evidence_digest"}, set(),
            f"root.state.capability_evidence_authority.{evidence_id}",
        )
        require_type(record["capability"], str, f"root.state.capability_evidence_authority.{evidence_id}.capability")
        require_type(record["task_version"], int, f"root.state.capability_evidence_authority.{evidence_id}.task_version")
        require_type(record["permission_snapshot"], str, f"root.state.capability_evidence_authority.{evidence_id}.permission_snapshot")
        require_type(record["status"], str, f"root.state.capability_evidence_authority.{evidence_id}.status")
        require_type(record["evidence_digest"], str, f"root.state.capability_evidence_authority.{evidence_id}.evidence_digest")
        if record["status"] not in {"VERIFIED", "FAILED", "UNKNOWN", "REVOKED"}:
            raise ValueError(f"root.state.capability_evidence_authority.{evidence_id}.status has unknown enum")
        if not SHA256_REF.fullmatch(record["evidence_digest"]):
            raise ValueError(f"root.state.capability_evidence_authority.{evidence_id}.evidence_digest must be sha256:<64 lowercase hex>")
    manifest = state.get("real_world_evidence_manifest", {})
    require_type(manifest, dict, "root.state.real_world_evidence_manifest")
    for evidence_id, record in manifest.items():
        require_type(evidence_id, str, "root.state.real_world_evidence_manifest key")
        record = exact_keys(
            record, {"verified", "origin", "source_id", "run_id"}, set(),
            f"root.state.real_world_evidence_manifest.{evidence_id}",
        )
        require_type(record["verified"], bool, f"root.state.real_world_evidence_manifest.{evidence_id}.verified")
        for key in ("origin", "source_id", "run_id"):
            require_type(record[key], str, f"root.state.real_world_evidence_manifest.{evidence_id}.{key}")
    if contract["task_version"] <= 0 or contract["budget_units"] <= 0:
        raise ValueError("task version and budget must be positive")
    if contract["risk"] not in {"low", "medium", "high", "critical"}:
        raise ValueError("unknown risk enum")
    if contract["permission_snapshot"] not in source["state"]["authorized_permission_snapshots"]:
        raise ValueError("common permission snapshot is not currently authorized")
    if not SHA256_REF.fullmatch(contract["input_digest"]):
        raise ValueError("common input digest must be sha256:<64 lowercase hex>")
    validate_observation(source["common_observation"], "root.common_observation")
    require_type(source["scenarios"], list, "root.scenarios")
    scenario_required = {"id", "kind", "layer", "overrides", "expected"}
    scenario_optional = {"security_slice", "synthetic_shadow", "intended_target_layer", "source_id", "run_id", "evidence_id"}
    for index, scenario in enumerate(source["scenarios"]):
        scenario = exact_keys(scenario, scenario_required, scenario_optional, f"root.scenarios[{index}]")
        for key in ("id", "kind", "layer", "expected"):
            require_type(scenario[key], str, f"root.scenarios[{index}].{key}")
        require_type(scenario["overrides"], dict, f"root.scenarios[{index}].overrides")
        if scenario["expected"] not in {"PASS", "FAIL", "REVIEW_REQUIRED"}:
            raise ValueError(f"root.scenarios[{index}].expected has unknown enum")
        for key in ("security_slice", "synthetic_shadow"):
            if key in scenario:
                require_type(scenario[key], bool, f"root.scenarios[{index}].{key}")
        merged = deep_merge(source["common_observation"], scenario["overrides"])
        validate_observation(merged, f"root.scenarios[{index}].merged_observation")
    ids = [scenario["id"] for scenario in source["scenarios"]]
    if len(ids) != len(set(ids)):
        raise ValueError("scenario ids must be unique")
    invalid_kinds = sorted({scenario["kind"] for scenario in source["scenarios"]} - KINDS)
    if invalid_kinds:
        raise ValueError(f"unknown scenario kinds: {invalid_kinds}")
    invalid_layers = sorted({scenario["layer"] for scenario in source["scenarios"]} - set(LAYERS))
    if invalid_layers:
        raise ValueError(f"invalid D22 layers: {invalid_layers}")
    real = [scenario for scenario in source["scenarios"] if scenario["layer"] == "representative_real_world"]
    if source["data_origin"] == "synthetic" and real:
        raise ValueError("synthetic fixture cannot claim representative_real_world execution")
    if bool(source["representative_real_world_executed"]) != bool(real):
        raise ValueError("representative_real_world_executed must match actual records")
    if real:
        manifest = source["state"].get("real_world_evidence_manifest", {})
        for scenario in real:
            if not all(scenario.get(key) for key in ("source_id", "run_id", "evidence_id")):
                raise ValueError("real-world records require source/run/evidence ids")
            record = manifest.get(scenario["evidence_id"])
            if not record or not record.get("verified") or record.get("origin") != "representative_real_world":
                raise ValueError("real-world evidence must resolve to a verified manifest record")
            if record.get("source_id") != scenario["source_id"] or record.get("run_id") != scenario["run_id"]:
                raise ValueError("real-world source/run ids must match manifest")
    for scenario in source["scenarios"]:
        if scenario.get("synthetic_shadow") and (
            scenario["layer"] != "holdout"
            or scenario.get("intended_target_layer") != "representative_real_world"
        ):
            raise ValueError("synthetic shadow must remain holdout")


def validate_enums(observation: dict) -> None:
    if observation["yield"]["agent_status"] not in {"ACTIVE", "YIELD_NOTICE", "SILENT"}:
        raise ValueError("unknown agent status")
    if observation["handoff"]["responsibility_ack"] not in {"ACCEPTED", "PENDING", "REJECTED"}:
        raise ValueError("unknown responsibility ack")
    if observation["handoff"]["transport_ack"] not in {"ACCEPTED", "PENDING", "REJECTED"}:
        raise ValueError("unknown transport ack")
    if observation["handoff"]["object_ack"] not in {"ACCEPTED", "PENDING", "REJECTED"}:
        raise ValueError("unknown object ack")
    if observation["receipt"]["state"] not in {"NONE", "COMMITTED", "FAILED", "UNKNOWN"}:
        raise ValueError("unknown receipt state")
    if observation["receipt"]["authoritative_readback"] not in {"NONE", "COMMITTED", "FAILED", "UNKNOWN"}:
        raise ValueError("unknown authoritative readback")
    if observation["cancel"]["state"] not in {"NONE", "REQUESTED", "ACCEPTED", "CANCELLED", "UNKNOWN"}:
        raise ValueError("unknown cancel state")


def decide(observation: dict, contract: dict, state: dict) -> tuple[str, list[str], dict, int]:
    validate_enums(observation)
    trace = ["freeze_common_contract", "evaluate_raw_state"]
    route = observation["route"]
    if route["task_version"] != contract["task_version"]:
        return "FAIL", trace + ["stale_task_version"], observation, 0
    if route["permission_snapshot"] != contract["permission_snapshot"]:
        return "FAIL", trace + ["unauthorized_route"], observation, 0
    if not route["capability_evidence_refs"]:
        return "FAIL", trace + ["unverified_competence"], observation, 0
    for evidence_ref in route["capability_evidence_refs"]:
        evidence = state["capability_evidence_registry"].get(evidence_ref)
        authority = state["capability_evidence_authority"].get(evidence_ref)
        if (
            evidence is None
            or authority is None
            or evidence["status"] != "VERIFIED"
            or evidence["capability"] != "routing"
            or evidence["task_version"] != route["task_version"]
            or evidence["permission_snapshot"] != route["permission_snapshot"]
            or authority["status"] != "VERIFIED"
            or authority["capability"] != "routing"
            or authority["task_version"] != route["task_version"]
            or authority["permission_snapshot"] != route["permission_snapshot"]
            or evidence != authority
        ):
            return "FAIL", trace + ["capability_evidence_authority_mismatch"], observation, 0
    if route["current_load"] + route["task_load"] > route["capacity"]:
        return "FAIL", trace + ["overload_admission"], observation, 0
    if route["estimated_cost"] > contract["budget_units"]:
        return "FAIL", trace + ["budget_exceeded"], observation, 0
    if route["execution_location"] not in route["allowed_data_locations"]:
        return "FAIL", trace + ["data_location_violation"], observation, 0

    yielded = observation["yield"]
    if yielded["agent_status"] == "SILENT" or (
        yielded["agent_status"] == "YIELD_NOTICE" and not yielded.get("notice")
    ):
        return "FAIL", trace + ["silent_or_incomplete_yield"], observation, 0

    handoff = observation["handoff"]
    if handoff["ack_card_version"] != handoff["card_version"]:
        return "FAIL", trace + ["stale_ack"], observation, 0
    if "REJECTED" in {handoff["transport_ack"], handoff["object_ack"]}:
        return "FAIL", trace + ["handoff_transport_or_object_rejected"], observation, 0
    if "PENDING" in {handoff["transport_ack"], handoff["object_ack"]}:
        return "REVIEW_REQUIRED", trace + ["handoff_transport_or_object_pending"], observation, 0
    if handoff["responsibility_ack"] != "ACCEPTED" and handoff["old_owner_released"]:
        return "FAIL", trace + ["owner_released_without_ack"], observation, 0
    if handoff["responsibility_ack"] != "ACCEPTED":
        return "REVIEW_REQUIRED", trace + ["responsibility_not_accepted"], observation, 0
    if len(set(handoff["transfer_targets"])) != 1:
        return "FAIL", trace + ["competing_transfer_targets"], observation, 0
    if len(set(handoff["accepted_responsibility_owners"])) != 1:
        return "FAIL", trace + ["multiple_responsibility_owners"], observation, 0
    if handoff["secret_material"]:
        return "FAIL", trace + ["secret_in_handoff"], observation, 0
    if handoff["responsibility_ack"] == "ACCEPTED" and not handoff["owner_cas_succeeded"]:
        return "FAIL", trace + ["owner_cas_failed"], observation, 0

    active_by_object: dict[str, set[str]] = defaultdict(set)
    for lease in observation["writer_leases"]:
        if lease["status"] == "ACTIVE":
            active_by_object[lease["object_id"]].add(lease["writer_id"])
    if any(len(writers) > 1 for writers in active_by_object.values()):
        return "FAIL", trace + ["double_writer"], observation, 0

    applied: dict[str, int] = Counter()
    external_effects = 0
    for entry in observation["effect_ledger"]:
        if entry["status"] == "APPLIED":
            applied[entry["logical_action_id"]] += 1
        external_effects += int(entry.get("confirmed_external_write", False))
    if external_effects and not state["external_effects_allowed"]:
        return "FAIL", trace + ["external_effect_contract_violated"], observation, external_effects
    if any(count > 1 for count in applied.values()):
        return "FAIL", trace + ["duplicate_delivery_applied_twice"], observation, external_effects

    cancel = observation["cancel"]
    if cancel["requested_at"]:
        if any(write["at"] > cancel["requested_at"] for write in cancel["writes"]):
            return "FAIL", trace + ["write_after_cancel"], observation, external_effects
        if cancel["state"] != "CANCELLED":
            return "REVIEW_REQUIRED", trace + ["cancel_not_terminal"], observation, external_effects
        if not cancel["all_branches_stopped"] or not cancel["locks_released"] or not cancel["effects_reconciled"]:
            return "REVIEW_REQUIRED", trace + ["cancel_residuals_unknown"], observation, external_effects

    if has_cycle(observation["wait_edges"]):
        return "FAIL", trace + ["deadlock_cycle"], observation, external_effects
    progress = observation["progress"]
    if progress["transition_count"] > progress["transition_limit"] and progress["progress_delta"] <= 0:
        return "FAIL", trace + ["livelock_no_progress"], observation, external_effects
    if progress["reroute_count"] > progress["reroute_limit"]:
        return "FAIL", trace + ["reroute_limit_exceeded"], observation, external_effects

    branches = observation["branches"]
    if not set(branches["required"]).issubset(set(branches["completed"])):
        return "FAIL", trace + ["missing_required_branch"], observation, external_effects

    receipt = observation["receipt"]
    if receipt["state"] == "UNKNOWN":
        if receipt["authoritative_readback"] == "UNKNOWN":
            return "REVIEW_REQUIRED", trace + ["receipt_unknown_requires_reconciliation"], observation, external_effects
        if receipt["authoritative_readback"] == "FAILED":
            return "FAIL", trace + ["authoritative_receipt_failed"], observation, external_effects

    d21 = observation["d21"]
    completion_contract = (
        ("technical_execution_ref", "technical_execution", "EXECUTED"),
        ("delivery_visibility_ref", "delivery_visibility", "VISIBLE"),
        ("business_environment_acceptance_ref", "business_environment_acceptance", "ACCEPTED"),
    )
    completion_unknown = False
    completion_failed = False
    for ref_key, expected_layer, expected_terminal in completion_contract:
        evidence = state["completion_evidence_registry"].get(d21[ref_key])
        authority = state["completion_evidence_authority"].get(d21[ref_key])
        if evidence is None:
            completion_failed = True
            trace.append(f"completion_evidence_not_found:{expected_layer}")
            continue
        if authority is None:
            completion_failed = True
            trace.append(f"completion_authority_not_found:{expected_layer}")
            continue
        if evidence["layer"] != expected_layer or not evidence["authoritative"]:
            completion_failed = True
            trace.append(f"completion_evidence_untrusted:{expected_layer}")
        elif (
            authority["layer"] != expected_layer
            or evidence["source"] != authority["source"]
            or evidence["object_digest"] != authority["object_digest"]
        ):
            completion_failed = True
            trace.append(f"completion_evidence_authority_mismatch:{expected_layer}")
        elif evidence["status"] == "UNKNOWN" or evidence["observed_terminal"] == "UNKNOWN":
            completion_unknown = True
            trace.append(f"completion_evidence_unknown:{expected_layer}")
        elif evidence["status"] != "VERIFIED" or evidence["observed_terminal"] != expected_terminal:
            completion_failed = True
            trace.append(f"completion_evidence_failed:{expected_layer}")
        else:
            trace.append(f"completion_evidence_verified:{expected_layer}")
    if d21["reported_complete"] and completion_failed:
        return "FAIL", trace + ["ghost_success_d21_incomplete"], observation, external_effects
    if d21["reported_complete"] and completion_unknown:
        return "REVIEW_REQUIRED", trace + ["completion_unknown_requires_reconciliation"], observation, external_effects

    return "PASS", trace + ["join_verified"], observation, external_effects


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    source = json.loads(input_path.read_text(encoding="utf-8"))
    validate(source)
    trials = []
    for scenario in source["scenarios"]:
        observation = deep_merge(source["common_observation"], scenario.get("overrides", {}))
        for run in range(1, 4):
            decision, trace, state_snapshot, external_effects = decide(
                observation, source["common_contract"], source["state"]
            )
            trials.append({
                "task_id": f"C17-{scenario['id']}",
                "trial_id": f"C17-{scenario['id']}-T{run}",
                "scenario_kind": scenario["kind"], "layer": scenario["layer"],
                "security_slice": bool(scenario.get("security_slice")),
                "synthetic_shadow": bool(scenario.get("synthetic_shadow")),
                "intended_target_layer": scenario.get("intended_target_layer"),
                "decision": decision, "expected": scenario["expected"],
                "matched_expected": decision == scenario["expected"],
                "trace": trace, "state": state_snapshot,
                "external_side_effects": external_effects,
            })
    pairs = [(trial["task_id"], trial["trial_id"]) for trial in trials]
    if len(pairs) != len(set(pairs)):
        raise ValueError("expanded task/trial ids must be unique")
    if not all(trial["matched_expected"] for trial in trials):
        raise ValueError("one or more decisions do not match the frozen offline oracle")
    digest_payload = json.dumps(trials, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    distribution = Counter(trial["decision"] for trial in trials)
    by_layer = {layer: Counter() for layer in LAYERS}
    for trial in trials:
        by_layer[trial["layer"]][trial["decision"]] += 1
    real_count = sum(trial["layer"] == "representative_real_world" for trial in trials)
    result = {
        "schema_version": "c17.synthetic.result.v3",
        "input_digest": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "decision_digest": hashlib.sha256(digest_payload.encode("utf-8")).hexdigest(),
        "trial_count": len(trials), "unique_task_trial": True,
        "distribution": dict(sorted(distribution.items())), "all_expected_matched": True,
        "external_side_effect_count": sum(trial["external_side_effects"] for trial in trials),
        "representative_real_world_executed": bool(real_count),
        "representative_real_world_trial_count": real_count,
        "synthetic_shadow_trial_count": sum(trial["synthetic_shadow"] for trial in trials),
        "security_failures_noncompensatory": all(
            trial["decision"] == "FAIL" for trial in trials
            if trial["security_slice"] and trial["expected"] == "FAIL"
        ),
        "by_layer": {key: dict(sorted(value.items())) for key, value in sorted(by_layer.items())},
        "trials": trials,
    }
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary_path = output_path.with_name("synthetic-routing-summary.md")
    lines = [
        "# C17 离线路由实验摘要", "",
        "> 状态化合成夹具，不证明真实 Runtime、跨系统取消或生产副作用。", "",
        f"- trials: `{result['trial_count']}`",
        f"- distribution: `{result['distribution']}`",
        f"- decision digest: `{result['decision_digest']}`",
        f"- external side effects: `{result['external_side_effect_count']}`",
        f"- representative real-world executed: `{result['representative_real_world_executed']}` ({result['representative_real_world_trial_count']} trials)",
        f"- synthetic shadow trials: `{result['synthetic_shadow_trial_count']}`",
        f"- security failures noncompensatory: `{result['security_failures_noncompensatory']}`",
        "", "## D22 layers", "",
    ]
    for key, value in result["by_layer"].items():
        lines.append(f"- {key}: `{value}`")
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(result["decision_digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

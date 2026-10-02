#!/usr/bin/env python3
"""Deterministic, state-derived C16 organization-governance harness."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


LAYERS = ["training", "regression", "holdout", "representative_real_world"]
KINDS = {"normal", "security", "adversarial", "boundary", "abnormal", "recovery"}
VERDICTS = {"PASS", "FAIL", "REVIEW_REQUIRED"}


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


def require_number(value: object, path: str) -> None:
    if type(value) not in {int, float}:
        raise ValueError(f"{path} must be a number")


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def parse_time(value: str, path: str) -> datetime:
    """Parse an ISO-8601 instant; lexical timestamp comparison is forbidden."""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{path} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{path} must include a timezone")
    return parsed


def deep_merge(base: dict, override: dict) -> dict:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if type(value) is dict and type(merged.get(key)) is dict:
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def validate_metrics(metrics: object, path: str) -> dict:
    metrics = exact(
        metrics,
        {"quality", "cost", "latency", "human", "communication", "conflicts", "recovery", "evidence_completeness"},
        set(), path,
    )
    for key, value in metrics.items():
        require_number(value, f"{path}.{key}")
    if metrics["cost"] <= 0 or metrics["latency"] <= 0:
        raise ValueError(f"{path} cost and latency must be positive")
    if not 0 <= metrics["evidence_completeness"] <= 1:
        raise ValueError(f"{path}.evidence_completeness must be within 0..1")
    return metrics


def validate_state(state: object, path: str) -> dict:
    state = exact(
        state,
        {"action_requests", "writer_leases", "write_events", "assertions", "credential_bindings",
         "budget", "cancellation", "completion", "effect_ledger", "runtime"},
        set(), path,
    )
    require_type(state["action_requests"], list, f"{path}.action_requests")
    for index, item in enumerate(state["action_requests"]):
        item_path = f"{path}.action_requests[{index}]"
        item = exact(item, {"actor_alias", "action", "object_id", "scope", "requested_at"}, set(), item_path)
        for key in item:
            require_type(item[key], str, f"{item_path}.{key}")

    require_type(state["writer_leases"], list, f"{path}.writer_leases")
    for index, item in enumerate(state["writer_leases"]):
        item_path = f"{path}.writer_leases[{index}]"
        item = exact(item, {"object_id", "writer_alias", "base_version", "lease_id", "status"}, set(), item_path)
        for key in item:
            require_type(item[key], str, f"{item_path}.{key}")
        if item["status"] not in {"ACTIVE", "RELEASED", "EXPIRED"}:
            raise ValueError(f"{item_path}.status has unknown enum")

    require_type(state["write_events"], list, f"{path}.write_events")
    for index, item in enumerate(state["write_events"]):
        item_path = f"{path}.write_events[{index}]"
        item = exact(item, {"object_id", "writer_alias", "base_version", "result_version", "merge_record_id"}, set(), item_path)
        for key in item:
            require_type(item[key], str, f"{item_path}.{key}")

    require_type(state["assertions"], list, f"{path}.assertions")
    for index, item in enumerate(state["assertions"]):
        item_path = f"{path}.assertions[{index}]"
        item = exact(item, {"claim_id", "claim_type", "source_refs", "minimum_independent_origins"}, set(), item_path)
        for key in ("claim_id", "claim_type"):
            require_type(item[key], str, f"{item_path}.{key}")
        if item["claim_type"] not in {"DRAFT", "OPINION", "FACT"}:
            raise ValueError(f"{item_path}.claim_type has unknown enum")
        require_type(item["source_refs"], list, f"{item_path}.source_refs")
        require_type(item["minimum_independent_origins"], int, f"{item_path}.minimum_independent_origins")
        if item["minimum_independent_origins"] < 1:
            raise ValueError(f"{item_path}.minimum_independent_origins must be positive")
        if item["claim_type"] == "FACT" and item["minimum_independent_origins"] < 2:
            raise ValueError(f"{item_path}.FACT requires at least two independent origins")

    require_type(state["credential_bindings"], list, f"{path}.credential_bindings")
    for index, item in enumerate(state["credential_bindings"]):
        item_path = f"{path}.credential_bindings[{index}]"
        item = exact(item, {"actor_alias", "credential_id"}, set(), item_path)
        require_type(item["actor_alias"], str, f"{item_path}.actor_alias")
        require_type(item["credential_id"], str, f"{item_path}.credential_id")

    budget = exact(state["budget"], {"limit", "stop_threshold", "consumed", "stop_receipt_status", "all_work_stopped"}, set(), f"{path}.budget")
    for key in ("limit", "stop_threshold", "consumed"):
        require_number(budget[key], f"{path}.budget.{key}")
    require_type(budget["stop_receipt_status"], str, f"{path}.budget.stop_receipt_status")
    if budget["stop_receipt_status"] not in {"NONE", "VERIFIED", "UNKNOWN", "REJECTED"}:
        raise ValueError(f"{path}.budget.stop_receipt_status has unknown enum")
    require_type(budget["all_work_stopped"], bool, f"{path}.budget.all_work_stopped")

    cancellation = exact(state["cancellation"], {"requested", "receipt_status", "children", "queue_readback", "inflight_readback"}, set(), f"{path}.cancellation")
    require_type(cancellation["requested"], bool, f"{path}.cancellation.requested")
    for key in ("receipt_status", "queue_readback", "inflight_readback"):
        require_type(cancellation[key], str, f"{path}.cancellation.{key}")
    if cancellation["receipt_status"] not in {"NONE", "ACCEPTED", "REJECTED", "UNKNOWN"}:
        raise ValueError(f"{path}.cancellation.receipt_status has unknown enum")
    if cancellation["queue_readback"] not in {"CLEAR", "NOT_CLEAR", "UNKNOWN"} or cancellation["inflight_readback"] not in {"CLEAR", "NOT_CLEAR", "UNKNOWN"}:
        raise ValueError(f"{path}.cancellation readback has unknown enum")
    require_type(cancellation["children"], list, f"{path}.cancellation.children")
    for index, item in enumerate(cancellation["children"]):
        item_path = f"{path}.cancellation.children[{index}]"
        item = exact(item, {"child_id", "state"}, set(), item_path)
        require_type(item["child_id"], str, f"{item_path}.child_id")
        require_type(item["state"], str, f"{item_path}.state")
        if item["state"] not in {"QUEUED", "ACTIVE", "COMPLETED", "CANCELLED", "FAILED", "UNKNOWN"}:
            raise ValueError(f"{item_path}.state has unknown enum")

    completion = exact(state["completion"], {"reported_complete"}, set(), f"{path}.completion")
    require_type(completion["reported_complete"], bool, f"{path}.completion.reported_complete")
    require_type(state["effect_ledger"], list, f"{path}.effect_ledger")
    for index, item in enumerate(state["effect_ledger"]):
        item_path = f"{path}.effect_ledger[{index}]"
        item = exact(item, {"effect_id", "target", "status", "confirmed_external_write"}, set(), item_path)
        for key in ("effect_id", "target", "status"):
            require_type(item[key], str, f"{item_path}.{key}")
        require_type(item["confirmed_external_write"], bool, f"{item_path}.confirmed_external_write")
        if item["status"] not in {"PENDING", "APPLIED", "FAILED", "UNKNOWN", "RECONCILED"}:
            raise ValueError(f"{item_path}.status has unknown enum")
    runtime = exact(state["runtime"], {"real_runtime_required", "evidence_status"}, set(), f"{path}.runtime")
    require_type(runtime["real_runtime_required"], bool, f"{path}.runtime.real_runtime_required")
    require_type(runtime["evidence_status"], str, f"{path}.runtime.evidence_status")
    if runtime["evidence_status"] not in {"NOT_REQUIRED", "VERIFIED", "FAILED", "UNKNOWN"}:
        raise ValueError(f"{path}.runtime.evidence_status has unknown enum")
    return state


def validate(source: object) -> dict:
    source = exact(
        source,
        {"fixture_version", "now", "environment", "data_origin", "representative_real_world_executed",
         "comparison_contract", "net_benefit_policy", "identity", "common_state",
         "real_world_evidence_manifest", "scenarios"},
        set(), "root",
    )
    if source["fixture_version"] != "c16-org-v3":
        raise ValueError("unsupported fixture_version")
    require_type(source["now"], str, "root.now")
    parse_time(source["now"], "root.now")
    environment = exact(source["environment"], {"mode", "external_effects_allowed", "real_credentials"}, set(), "root.environment")
    if environment["mode"] != "offline_synthetic":
        raise ValueError("unsupported environment mode")
    require_type(environment["external_effects_allowed"], bool, "root.environment.external_effects_allowed")
    require_type(environment["real_credentials"], bool, "root.environment.real_credentials")
    require_type(source["data_origin"], str, "root.data_origin")
    if source["data_origin"] not in {"synthetic", "representative_real_world"}:
        raise ValueError("root.data_origin has unknown enum")
    require_type(source["representative_real_world_executed"], bool, "root.representative_real_world_executed")

    contract = exact(source["comparison_contract"], {"baseline", "candidate"}, set(), "root.comparison_contract")
    contract_keys = {"task_digest", "input_digest", "permission_digest", "budget_limit", "risk_boundary", "acceptance_digest", "environment_digest"}
    for arm in ("baseline", "candidate"):
        record = exact(contract[arm], contract_keys, set(), f"root.comparison_contract.{arm}")
        for key in contract_keys - {"budget_limit"}:
            require_type(record[key], str, f"root.comparison_contract.{arm}.{key}")
        require_number(record["budget_limit"], f"root.comparison_contract.{arm}.budget_limit")

    policy = exact(
        source["net_benefit_policy"],
        {"min_quality_delta", "max_cost_ratio", "max_latency_ratio", "max_human_delta", "max_communication_delta",
         "max_conflict_delta", "max_recovery_delta", "min_evidence_completeness", "min_independent_runs"},
        set(), "root.net_benefit_policy",
    )
    for key in policy:
        if key == "min_independent_runs":
            require_type(policy[key], int, f"root.net_benefit_policy.{key}")
        else:
            require_number(policy[key], f"root.net_benefit_policy.{key}")
    if policy["min_independent_runs"] < 2:
        raise ValueError("min_independent_runs must be at least 2")

    identity = exact(source["identity"], {"aliases", "principals", "grants", "credentials", "sources"}, set(), "root.identity")
    for key in ("aliases", "principals", "sources"):
        require_type(identity[key], dict, f"root.identity.{key}")
    require_type(identity["grants"], list, "root.identity.grants")
    require_type(identity["credentials"], list, "root.identity.credentials")
    for alias, principal_id in identity["aliases"].items():
        require_type(alias, str, "root.identity.aliases key")
        require_type(principal_id, str, f"root.identity.aliases.{alias}")
        if principal_id not in identity["principals"]:
            raise ValueError(f"alias {alias} resolves to unknown principal")
    if len(identity["aliases"].values()) != len(set(identity["aliases"].values())):
        raise ValueError("actor aliases must resolve one-to-one to principals")
    for principal_id, record in identity["principals"].items():
        require_type(principal_id, str, "root.identity.principals key")
        record = exact(record, {"roles"}, set(), f"root.identity.principals.{principal_id}")
        require_type(record["roles"], list, f"root.identity.principals.{principal_id}.roles")
        if not all(type(role) is str for role in record["roles"]):
            raise ValueError(f"root.identity.principals.{principal_id}.roles must contain strings")
    grant_ids = []
    for index, grant in enumerate(identity["grants"]):
        item_path = f"root.identity.grants[{index}]"
        grant = exact(grant, {"grant_id", "principal_id", "actions", "objects", "scopes", "status", "expires_at"}, set(), item_path)
        for key in ("grant_id", "principal_id", "status", "expires_at"):
            require_type(grant[key], str, f"{item_path}.{key}")
        parse_time(grant["expires_at"], f"{item_path}.expires_at")
        grant_ids.append(grant["grant_id"])
        if grant["principal_id"] not in identity["principals"]:
            raise ValueError(f"{item_path}.principal_id unknown")
        if grant["status"] not in {"ACTIVE", "REVOKED", "EXPIRED"}:
            raise ValueError(f"{item_path}.status has unknown enum")
        for key in ("actions", "objects", "scopes"):
            require_type(grant[key], list, f"{item_path}.{key}")
            if not all(type(value) is str for value in grant[key]):
                raise ValueError(f"{item_path}.{key} must contain strings")
    if len(grant_ids) != len(set(grant_ids)):
        raise ValueError("grant ids must be unique")
    credential_ids = []
    for index, credential in enumerate(identity["credentials"]):
        item_path = f"root.identity.credentials[{index}]"
        credential = exact(credential, {"credential_id", "owner_principal_id", "status"}, set(), item_path)
        for key in ("credential_id", "owner_principal_id", "status"):
            require_type(credential[key], str, f"{item_path}.{key}")
        credential_ids.append(credential["credential_id"])
        if credential["owner_principal_id"] not in identity["principals"]:
            raise ValueError(f"{item_path}.owner_principal_id unknown")
        if credential["status"] not in {"ACTIVE", "REVOKED", "EXPIRED"}:
            raise ValueError(f"{item_path}.status has unknown enum")
    if len(credential_ids) != len(set(credential_ids)):
        raise ValueError("credential ids must be unique")
    for source_id, record in identity["sources"].items():
        record = exact(record, {"origin"}, set(), f"root.identity.sources.{source_id}")
        require_type(record["origin"], str, f"root.identity.sources.{source_id}.origin")

    validate_state(source["common_state"], "root.common_state")
    manifest = source["real_world_evidence_manifest"]
    require_type(manifest, dict, "root.real_world_evidence_manifest")
    for evidence_id, record in manifest.items():
        record = exact(record, {"verified", "origin", "source_id", "run_id"}, set(), f"root.real_world_evidence_manifest.{evidence_id}")
        require_type(record["verified"], bool, f"root.real_world_evidence_manifest.{evidence_id}.verified")
        for key in ("origin", "source_id", "run_id"):
            require_type(record[key], str, f"root.real_world_evidence_manifest.{evidence_id}.{key}")

    require_type(source["scenarios"], list, "root.scenarios")
    scenario_ids: list[str] = []
    run_ids: list[str] = []
    trace_digests: list[str] = []
    evidence_digests: list[str] = []
    evidence_ids: list[str] = []
    real_count = 0
    for s_index, scenario in enumerate(source["scenarios"]):
        path = f"root.scenarios[{s_index}]"
        scenario = exact(
            scenario, {"id", "kind", "layer", "mode", "state_overrides", "runs", "expected"},
            {"security_slice", "synthetic_shadow", "intended_target_layer"}, path,
        )
        scenario_ids.append(scenario["id"])
        if scenario["kind"] not in KINDS or scenario["layer"] not in LAYERS or scenario["mode"] not in {"single", "multi"} or scenario["expected"] not in VERDICTS:
            raise ValueError(f"{path} contains an invalid enum")
        for key in ("security_slice", "synthetic_shadow"):
            if key in scenario:
                require_type(scenario[key], bool, f"{path}.{key}")
        require_type(scenario["state_overrides"], dict, f"{path}.state_overrides")
        validate_state(deep_merge(source["common_state"], scenario["state_overrides"]), f"{path}.merged_state")
        if scenario.get("synthetic_shadow") and (scenario["layer"] != "holdout" or scenario.get("intended_target_layer") != "representative_real_world"):
            raise ValueError("synthetic shadow must remain holdout and target representative_real_world")
        require_type(scenario["runs"], list, f"{path}.runs")
        if len(scenario["runs"]) < policy["min_independent_runs"]:
            raise ValueError(f"{path}.runs has insufficient independent records")
        for r_index, run in enumerate(scenario["runs"]):
            run_path = f"{path}.runs[{r_index}]"
            run = exact(
                run,
                {"run_id", "input_version", "trace_events", "evidence_records", "terminal", "baseline_metrics", "candidate_metrics"},
                {"real_world_evidence_id", "real_world_source_id"}, run_path,
            )
            require_type(run["run_id"], str, f"{run_path}.run_id")
            require_type(run["input_version"], str, f"{run_path}.input_version")
            for optional_key in ("real_world_evidence_id", "real_world_source_id"):
                if optional_key in run:
                    require_type(run[optional_key], str, f"{run_path}.{optional_key}")
            require_type(run["trace_events"], list, f"{run_path}.trace_events")
            require_type(run["evidence_records"], list, f"{run_path}.evidence_records")
            if len(run["trace_events"]) < 2 or not run["evidence_records"]:
                raise ValueError(f"{run_path} requires trace and evidence records")
            for e_index, event in enumerate(run["trace_events"]):
                event = exact(event, {"run_id", "seq", "event"}, set(), f"{run_path}.trace_events[{e_index}]")
                require_type(event["run_id"], str, f"{run_path}.trace_events[{e_index}].run_id")
                require_type(event["seq"], int, f"{run_path}.trace_events[{e_index}].seq")
                require_type(event["event"], str, f"{run_path}.trace_events[{e_index}].event")
                if event["run_id"] != run["run_id"]:
                    raise ValueError(f"{run_path} trace run binding mismatch")
            for e_index, evidence in enumerate(run["evidence_records"]):
                evidence = exact(evidence, {"run_id", "evidence_id", "kind", "status"}, set(), f"{run_path}.evidence_records[{e_index}]")
                for key in ("run_id", "evidence_id", "kind", "status"):
                    require_type(evidence[key], str, f"{run_path}.evidence_records[{e_index}].{key}")
                if evidence["run_id"] != run["run_id"] or evidence["status"] not in {"VERIFIED", "FAILED", "UNKNOWN"}:
                    raise ValueError(f"{run_path} evidence binding or status invalid")
                evidence_ids.append(evidence["evidence_id"])
            terminal = exact(run["terminal"], {"technical", "delivery", "business"}, set(), f"{run_path}.terminal")
            for key in terminal:
                require_type(terminal[key], str, f"{run_path}.terminal.{key}")
            if terminal["technical"] not in {"EXECUTED", "FAILED", "UNKNOWN"} or terminal["delivery"] not in {"VISIBLE", "MISSING", "UNKNOWN"} or terminal["business"] not in {"ACCEPTED", "REJECTED", "UNKNOWN"}:
                raise ValueError(f"{run_path}.terminal has unknown enum")
            validate_metrics(run["baseline_metrics"], f"{run_path}.baseline_metrics")
            validate_metrics(run["candidate_metrics"], f"{run_path}.candidate_metrics")
            run_ids.append(run["run_id"])
            trace_digests.append(canonical_digest(run["trace_events"]))
            evidence_digests.append(canonical_digest(run["evidence_records"]))
            if scenario["layer"] == "representative_real_world":
                real_count += 1
                evidence_id = run.get("real_world_evidence_id")
                source_id = run.get("real_world_source_id")
                record = manifest.get(evidence_id)
                if (
                    not evidence_id or not source_id or not record or not record["verified"]
                    or record["origin"] != "representative_real_world"
                    or record["run_id"] != run["run_id"]
                    or record["source_id"] != source_id
                ):
                    raise ValueError(f"{run_path} representative-real-world evidence is unresolved or mismatched")
    if len(scenario_ids) != len(set(scenario_ids)):
        raise ValueError("scenario ids must be unique")
    if len(run_ids) != len(set(run_ids)) or len(trace_digests) != len(set(trace_digests)) or len(evidence_digests) != len(set(evidence_digests)):
        raise ValueError("run ids, trace digests and evidence digests must be independently unique")
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("evidence ids must be globally unique across runs")
    if source["data_origin"] == "synthetic" and real_count:
        raise ValueError("synthetic fixture cannot claim representative_real_world execution")
    if bool(real_count) != source["representative_real_world_executed"]:
        raise ValueError("representative_real_world_executed must match actual run records")
    return source


def comparable(contract: dict) -> bool:
    return contract["baseline"] == contract["candidate"]


def decide(source: dict, scenario: dict, run: dict) -> tuple[str, list[str], int, dict]:
    trace = ["freeze_comparison_contract", "evaluate_raw_organization_state"]
    if not comparable(source["comparison_contract"]):
        return "REVIEW_REQUIRED", trace + ["comparison_contract_incomparable"], 0, {}
    state = deep_merge(source["common_state"], scenario["state_overrides"])
    aliases = source["identity"]["aliases"]
    grants = source["identity"]["grants"]
    credentials = {item["credential_id"]: item for item in source["identity"]["credentials"]}

    external_effects = sum(
        int(entry["confirmed_external_write"] and entry["status"] == "APPLIED")
        for entry in state["effect_ledger"]
    )
    if external_effects and not source["environment"]["external_effects_allowed"]:
        return "FAIL", trace + ["external_effect_contract_violated"], external_effects, {}

    for request in state["action_requests"]:
        principal = aliases.get(request["actor_alias"])
        requested_at = parse_time(request["requested_at"], "action_request.requested_at")
        authorized = any(
            grant["principal_id"] == principal
            and grant["status"] == "ACTIVE"
            and parse_time(grant["expires_at"], "grant.expires_at") >= requested_at
            and request["action"] in grant["actions"]
            and request["object_id"] in grant["objects"]
            and request["scope"] in grant["scopes"]
            for grant in grants
        )
        if not principal or not authorized:
            return "FAIL", trace + ["authorization_missing_or_stale"], external_effects, {}

    seen_credentials: dict[str, str] = {}
    for binding in state["credential_bindings"]:
        principal = aliases.get(binding["actor_alias"])
        credential = credentials.get(binding["credential_id"])
        if not principal or not credential or credential["status"] != "ACTIVE" or credential["owner_principal_id"] != principal:
            return "FAIL", trace + ["credential_owner_or_status_invalid"], external_effects, {}
        prior = seen_credentials.get(binding["credential_id"])
        if prior and prior != principal:
            return "FAIL", trace + ["shared_credential_across_principals"], external_effects, {}
        seen_credentials[binding["credential_id"]] = principal

    writers: dict[str, set[str]] = defaultdict(set)
    for lease in state["writer_leases"]:
        if lease["writer_alias"] not in aliases:
            return "FAIL", trace + ["writer_identity_unresolved"], external_effects, {}
        if lease["status"] == "ACTIVE":
            writers[lease["object_id"]].add(aliases[lease["writer_alias"]])
    if any(len(group) > 1 for group in writers.values()):
        return "FAIL", trace + ["multiple_active_writers"], external_effects, {}
    by_base: dict[tuple[str, str], dict[str, set[str]]] = defaultdict(lambda: {"writers": set(), "versions": set()})
    for event in state["write_events"]:
        if event["writer_alias"] not in aliases:
            return "FAIL", trace + ["writer_identity_unresolved"], external_effects, {}
        if event["merge_record_id"] == "NONE":
            group = by_base[(event["object_id"], event["base_version"])]
            group["writers"].add(aliases[event["writer_alias"]])
            group["versions"].add(event["result_version"])
    if any(len(group["writers"]) > 1 or len(group["versions"]) > 1 for group in by_base.values()):
        return "FAIL", trace + ["unmerged_shared_write_conflict"], external_effects, {}

    sources = source["identity"]["sources"]
    for assertion in state["assertions"]:
        if assertion["claim_type"] == "FACT":
            origins = {sources[ref]["origin"] for ref in assertion["source_refs"] if ref in sources}
            if len(origins) < assertion["minimum_independent_origins"]:
                return "FAIL", trace + ["correlated_consensus_claimed_fact"], external_effects, {}

    budget = state["budget"]
    if budget["consumed"] > budget["limit"]:
        return "FAIL", trace + ["budget_limit_exceeded"], external_effects, {}
    if budget["consumed"] >= budget["stop_threshold"]:
        if budget["stop_receipt_status"] == "UNKNOWN":
            return "REVIEW_REQUIRED", trace + ["budget_stop_unknown"], external_effects, {}
        if budget["stop_receipt_status"] != "VERIFIED" or not budget["all_work_stopped"]:
            return "FAIL", trace + ["budget_threshold_without_verified_stop"], external_effects, {}

    cancel = state["cancellation"]
    if cancel["requested"]:
        if cancel["receipt_status"] == "REJECTED" or any(child["state"] in {"ACTIVE", "QUEUED"} for child in cancel["children"]):
            return "FAIL", trace + ["cancel_propagation_leak"], external_effects, {}
        if cancel["receipt_status"] == "UNKNOWN" or "UNKNOWN" in {cancel["queue_readback"], cancel["inflight_readback"]} or any(child["state"] == "UNKNOWN" for child in cancel["children"]):
            return "REVIEW_REQUIRED", trace + ["cancel_terminal_unknown"], external_effects, {}
        if cancel["receipt_status"] == "NONE":
            return "REVIEW_REQUIRED", trace + ["cancel_receipt_missing"], external_effects, {}
        if cancel["queue_readback"] != "CLEAR" or cancel["inflight_readback"] != "CLEAR":
            return "FAIL", trace + ["cancel_residual_work"], external_effects, {}

    evidence_statuses = {item["status"] for item in run["evidence_records"]}
    if "FAILED" in evidence_statuses:
        return "FAIL", trace + ["run_evidence_failed"], external_effects, {}
    if "UNKNOWN" in evidence_statuses:
        return "REVIEW_REQUIRED", trace + ["run_evidence_unknown"], external_effects, {}

    effect_statuses = {item["status"] for item in state["effect_ledger"]}
    if "FAILED" in effect_statuses:
        return "FAIL", trace + ["effect_failed"], external_effects, {}
    if effect_statuses & {"UNKNOWN", "PENDING"}:
        return "REVIEW_REQUIRED", trace + ["effect_terminal_unknown"], external_effects, {}

    terminal = run["terminal"]
    if state["completion"]["reported_complete"]:
        if terminal["technical"] == "FAILED" or terminal["delivery"] == "MISSING" or terminal["business"] == "REJECTED":
            return "FAIL", trace + ["ghost_success"], external_effects, {}
        if "UNKNOWN" in terminal.values():
            return "REVIEW_REQUIRED", trace + ["terminal_unknown"], external_effects, {}

    runtime = state["runtime"]
    if runtime["real_runtime_required"]:
        if runtime["evidence_status"] == "FAILED":
            return "FAIL", trace + ["required_runtime_failed"], external_effects, {}
        if runtime["evidence_status"] != "VERIFIED":
            return "REVIEW_REQUIRED", trace + ["required_runtime_unverified"], external_effects, {}

    baseline = run["baseline_metrics"]
    candidate = run["candidate_metrics"]
    metrics = {
        "quality_delta": candidate["quality"] - baseline["quality"],
        "cost_ratio": candidate["cost"] / baseline["cost"],
        "latency_ratio": candidate["latency"] / baseline["latency"],
        "human_delta": candidate["human"] - baseline["human"],
        "communication_delta": candidate["communication"] - baseline["communication"],
        "conflict_delta": candidate["conflicts"] - baseline["conflicts"],
        "recovery_delta": candidate["recovery"] - baseline["recovery"],
        "evidence_completeness": candidate["evidence_completeness"],
    }
    if scenario["mode"] == "multi":
        policy = source["net_benefit_policy"]
        burdens_ok = (
            metrics["cost_ratio"] <= policy["max_cost_ratio"]
            and metrics["latency_ratio"] <= policy["max_latency_ratio"]
            and metrics["human_delta"] <= policy["max_human_delta"]
            and metrics["communication_delta"] <= policy["max_communication_delta"]
            and metrics["conflict_delta"] <= policy["max_conflict_delta"]
            and metrics["recovery_delta"] <= policy["max_recovery_delta"]
            and metrics["evidence_completeness"] >= policy["min_evidence_completeness"]
        )
        quality_or_efficiency = (
            metrics["quality_delta"] >= policy["min_quality_delta"]
            or (
                metrics["quality_delta"] >= 0
                and metrics["cost_ratio"] < 1
                and metrics["latency_ratio"] < 1
                and metrics["human_delta"] <= 0
            )
        )
        if not burdens_ok or not quality_or_efficiency:
            return "FAIL", trace + ["negative_or_unapproved_net_benefit"], external_effects, metrics
    return "PASS", trace + ["bounded_contract_satisfied"], external_effects, metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    source = validate(json.loads(input_path.read_text(encoding="utf-8")))
    runs: list[dict] = []
    for scenario in source["scenarios"]:
        for record in scenario["runs"]:
            verdict, reasons, external_effects, metrics = decide(source, scenario, record)
            runs.append({
                "task_id": f"TASK-C16-{scenario['id'].upper()}",
                "trial_id": record["run_id"],
                "scenario": scenario["id"],
                "scenario_kind": scenario["kind"],
                "layer": scenario["layer"],
                "synthetic_shadow": bool(scenario.get("synthetic_shadow", False)),
                "intended_target_layer": scenario.get("intended_target_layer"),
                "mode": scenario["mode"],
                "verdict": verdict,
                "expected": scenario["expected"],
                "matched": verdict == scenario["expected"],
                "reasons": reasons,
                "security_noncompensatory": bool(scenario.get("security_slice", False)),
                "external_effects": external_effects,
                "input_version": record["input_version"],
                "trace_digest": canonical_digest(record["trace_events"]),
                "evidence_digest": canonical_digest(record["evidence_records"]),
                "terminal_digest": canonical_digest(record["terminal"]),
                "derived_metrics": metrics,
            })
    if not all(run["matched"] for run in runs):
        raise ValueError("one or more decisions do not match the frozen offline oracle")
    pairs = [(run["task_id"], run["trial_id"]) for run in runs]
    if len(pairs) != len(set(pairs)):
        raise ValueError("task/trial pairs must be unique")
    distribution = Counter(run["verdict"] for run in runs)
    by_layer = {layer: Counter() for layer in LAYERS}
    for run in runs:
        by_layer[run["layer"]][run["verdict"]] += 1
    real_count = sum(run["layer"] == "representative_real_world" for run in runs)
    report = {
        "fixture_version": source["fixture_version"],
        "contract_comparable": comparable(source["comparison_contract"]),
        "run_count": len(runs),
        "unique_task_count": len({run["task_id"] for run in runs}),
        "unique_trial_ids": len({run["trial_id"] for run in runs}) == len(runs),
        "unique_trace_digests": len({run["trace_digest"] for run in runs}) == len(runs),
        "unique_evidence_digests": len({run["evidence_digest"] for run in runs}) == len(runs),
        "all_expected_matched": True,
        "external_effect_count": sum(run["external_effects"] for run in runs),
        "zero_external_effects": not any(run["external_effects"] for run in runs),
        "representative_real_world_executed": bool(real_count),
        "representative_real_world_trial_count": real_count,
        "synthetic_shadow_trial_count": sum(run["synthetic_shadow"] for run in runs),
        "distribution": dict(sorted(distribution.items())),
        "by_layer": {key: dict(sorted(value.items())) for key, value in sorted(by_layer.items())},
        "runs": runs,
    }
    output_text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    output_path.write_text(output_text, encoding="utf-8")
    summary_path = output_path.with_name("synthetic-organization-summary.md")
    lines = [
        "# C16 离线组织实验摘要", "",
        "> v3 状态化合成控制，只证明冻结离线记录的控制不变量；不证明真实 Runtime 或生产净收益。", "",
        f"- trials: `{report['run_count']}`",
        f"- unique tasks: `{report['unique_task_count']}`",
        f"- distribution: `{report['distribution']}`",
        f"- comparable contract: `{report['contract_comparable']}`",
        f"- unique trial/trace/evidence: `{report['unique_trial_ids']}/{report['unique_trace_digests']}/{report['unique_evidence_digests']}`",
        f"- expected matched: `{report['all_expected_matched']}`",
        f"- external effects: `{report['external_effect_count']}`; zero: `{report['zero_external_effects']}`",
        f"- representative real-world executed: `{report['representative_real_world_executed']}` ({report['representative_real_world_trial_count']} trials)",
        f"- synthetic shadow trials: `{report['synthetic_shadow_trial_count']}`", "", "## D22 layers", "",
    ]
    for layer, values in report["by_layer"].items():
        lines.append(f"- {layer}: `{values}`")
    summary_text = "\n".join(lines) + "\n"
    summary_path.write_text(summary_text, encoding="utf-8")
    print(hashlib.sha256(output_text.encode("utf-8")).hexdigest())
    print(hashlib.sha256(summary_text.encode("utf-8")).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

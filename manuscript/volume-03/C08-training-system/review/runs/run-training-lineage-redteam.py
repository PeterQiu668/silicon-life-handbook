#!/usr/bin/env python3
"""Deterministic offline C08 X02 lineage and reviewer-separation red team.

The input and result use JSON syntax, which is valid YAML 1.2. The runner reads
one local fixture and writes only the explicitly selected result and summary.
It performs no network, model, Skill, Memory, plugin, release, or external-state
operation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple


PASS = "PASS"
FAIL = "FAIL"
REVIEW_REQUIRED = "REVIEW_REQUIRED"
SECURITY_SUITE = "security/red-team"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def content_sha256(content: Any) -> str:
    return sha256_bytes(canonical_bytes(content))


def exact_diff(before: Any, after: Any, path: str = "") -> List[Dict[str, Any]]:
    """Return a deterministic JSON-pointer-like exact diff."""
    if type(before) is not type(after):
        return [{"path": path or "/", "before": before, "after": after}]
    if isinstance(before, dict):
        rows: List[Dict[str, Any]] = []
        for key in sorted(set(before) | set(after)):
            child = f"{path}/{key}"
            if key not in before:
                rows.append({"path": child, "before": None, "after": after[key]})
            elif key not in after:
                rows.append({"path": child, "before": before[key], "after": None})
            else:
                rows.extend(exact_diff(before[key], after[key], child))
        return rows
    if isinstance(before, list):
        if before == after:
            return []
        return [{"path": path or "/", "before": before, "after": after}]
    if before != after:
        return [{"path": path or "/", "before": before, "after": after}]
    return []


def forbidden_candidate_keys(value: Any, path: str = "") -> List[str]:
    """Prove that input candidates do not self-report hashes, diffs or decisions."""
    forbidden = {"sha256", "hash", "digest", "diff", "decision", "verdict"}
    hits: List[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}/{key}"
            if key.lower() in forbidden:
                hits.append(child_path)
            hits.extend(forbidden_candidate_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            hits.extend(forbidden_candidate_keys(child, f"{path}/{index}"))
    return hits


def tri_state_from_trials(records: Sequence[Dict[str, Any]]) -> str:
    if not records:
        return REVIEW_REQUIRED
    states = [record["evaluation_status"] for record in records]
    if FAIL in states:
        return FAIL
    if REVIEW_REQUIRED in states:
        return REVIEW_REQUIRED
    return PASS


def evaluate_record(record: Dict[str, Any]) -> Dict[str, Any]:
    evaluated = copy.deepcopy(record)
    actual = record["actual"]
    if actual == "UNKNOWN":
        status = REVIEW_REQUIRED
        reason = "actual outcome is UNKNOWN; uncertainty cannot be promoted to PASS"
    elif actual == record["expected"]:
        status = PASS
        reason = "actual equals frozen expected outcome"
    else:
        status = FAIL
        reason = "actual differs from frozen expected outcome"
    evaluated["evaluation_status"] = status
    evaluated["evaluation_reason"] = reason
    evaluated["security_redteam_cross_cutting"] = SECURITY_SUITE in record["suite_memberships"]
    return evaluated


def metric(records: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    counts = Counter(record["evaluation_status"] for record in records)
    return {
        "total": len(records),
        "pass": counts[PASS],
        "fail": counts[FAIL],
        "review_required": counts[REVIEW_REQUIRED],
        "gate": tri_state_from_trials(records),
    }


def make_lineage(
    candidate_id: str,
    baseline_content: Dict[str, Any],
    candidate_content: Dict[str, Any],
) -> Dict[str, Any]:
    changed_factors = [
        key
        for key in sorted(set(baseline_content) | set(candidate_content))
        if baseline_content.get(key) != candidate_content.get(key)
    ]
    return {
        "candidate_id": candidate_id,
        "baseline_content_sha256": content_sha256(baseline_content),
        "candidate_content_sha256": content_sha256(candidate_content),
        "changed_top_level_factors": changed_factors,
        "changed_top_level_factor_count": len(changed_factors),
        "exact_diff": exact_diff(baseline_content, candidate_content),
        "hash_and_diff_origin": "computed_by_runner_from_canonical_candidate_content",
    }


def build_single_factor_splits(
    baseline_content: Dict[str, Any],
    combined_content: Dict[str, Any],
) -> List[Dict[str, Any]]:
    changed_factors = [
        key
        for key in sorted(set(baseline_content) | set(combined_content))
        if baseline_content.get(key) != combined_content.get(key)
    ]
    splits = []
    for factor in changed_factors:
        content = copy.deepcopy(baseline_content)
        if factor in combined_content:
            content[factor] = copy.deepcopy(combined_content[factor])
        else:
            content.pop(factor, None)
        candidate_id = f"candidate-A-split-{factor.replace('_', '-')}"
        splits.append({
            "candidate_id": candidate_id,
            "content": content,
            "lineage": make_lineage(candidate_id, baseline_content, content),
        })
    return splits


def access_events(fixture: Dict[str, Any]) -> List[Dict[str, Any]]:
    matrix = fixture["access_matrix"]
    private_resources = set(fixture["private_resources"])
    events = []
    for request in fixture["access_requests"]:
        allowed = set(matrix.get(request["actor"], []))
        resource_results = [
            {
                "resource": resource,
                "decision": "ALLOW" if resource in allowed else "DENY",
                "private": resource in private_resources,
            }
            for resource in request["resources"]
        ]
        allowed_resources = [
            row["resource"] for row in resource_results if row["decision"] == "ALLOW"
        ]
        denied = [
            row["resource"] for row in resource_results if row["decision"] == "DENY"
        ]
        private_allowed = [
            row["resource"]
            for row in resource_results
            if row["private"] and row["decision"] == "ALLOW"
        ]
        if allowed_resources and denied:
            aggregate_decision = "PARTIAL"
        elif allowed_resources:
            aggregate_decision = "ALLOW"
        else:
            aggregate_decision = "DENY"
        events.append({
            "task_id": request["task_id"],
            "trial_id": request["trial_id"],
            "run_id": request["run_id"],
            "actor": request["actor"],
            "action": request["action"],
            "requested_resources": request["resources"],
            "resource_decisions": resource_results,
            "access_decision": aggregate_decision,
            "allowed_resources": allowed_resources,
            "denied_resources": denied,
            "private_resources_allowed": private_allowed,
            "private_payload_disclosed": bool(private_allowed),
            "stated_reason": request["stated_reason"],
        })
    return events


def decide_run(
    run: Dict[str, Any],
    lineage: Dict[str, Any],
    records: Sequence[Dict[str, Any]],
    run_access_events: Sequence[Dict[str, Any]],
    access_matrix: Dict[str, List[str]],
    replacement_review_contract: Dict[str, Any],
) -> Dict[str, Any]:
    canonical_layers = [
        "training",
        "regression",
        "holdout",
        "representative_real_world",
    ]
    layer_records = {
        layer: [record for record in records if record["data_layer"] == layer]
        for layer in canonical_layers
    }
    security_records = [
        record for record in records if record["security_redteam_cross_cutting"]
    ]
    ordinary_holdout_records = [
        record
        for record in layer_records["holdout"]
        if not record["security_redteam_cross_cutting"]
    ]

    metrics = {layer: metric(layer_records[layer]) for layer in canonical_layers}
    metrics["ordinary_holdout_view"] = metric(ordinary_holdout_records)
    metrics["security_redteam_cross_cutting"] = metric(security_records)

    if run["requested_causal_attribution"]:
        if lineage["changed_top_level_factor_count"] == 1:
            attribution_gate = PASS
            attribution_status = "SUPPORTED_SINGLE_VARIABLE_DESIGN"
        else:
            attribution_gate = REVIEW_REQUIRED
            attribution_status = "REJECTED_CONFOUNDED_MULTI_VARIABLE_CHANGE"
    else:
        attribution_gate = PASS
        attribution_status = "NOT_REQUESTED"

    reviewer_role = run["reviewer_role"]
    reviewer_allowed = set(access_matrix.get(reviewer_role, []))
    required_review_resources = set(replacement_review_contract["required_resources"])
    forbidden_review_resources = set(replacement_review_contract["forbidden_resources"])
    reviewer_has_required_eval_access = required_review_resources.issubset(reviewer_allowed)
    reviewer_has_forbidden_access = bool(forbidden_review_resources & reviewer_allowed)
    reviewer_is_blind = (
        reviewer_role == replacement_review_contract["reviewer_role"]
        and reviewer_has_required_eval_access
        and not reviewer_has_forbidden_access
    )
    prohibited_access_attempted = any(
        bool(event["denied_resources"]) for event in run_access_events
    )
    private_payload_disclosed = any(
        event["private_payload_disclosed"] for event in run_access_events
    )
    reviewer_conflict = reviewer_role == "mentor"
    if reviewer_conflict or private_payload_disclosed:
        review_integrity_gate = FAIL
    elif reviewer_role == replacement_review_contract["reviewer_role"] and not reviewer_is_blind:
        review_integrity_gate = REVIEW_REQUIRED
    else:
        review_integrity_gate = PASS
    review_integrity_status = (
        "INVALIDATED_REVIEWER_ROLE_CONFLICT"
        if reviewer_conflict
        else "PRIVATE_EVALUATION_PAYLOAD_DISCLOSED" if private_payload_disclosed
        else "BLIND_REPLACEMENT_REVIEW" if reviewer_is_blind else "INDEPENDENT_ROLE"
    )

    release_gates = {
        "regression": metrics["regression"]["gate"],
        "ordinary_holdout": metrics["ordinary_holdout_view"]["gate"],
        "representative_real_world": metrics["representative_real_world"]["gate"],
        "security_redteam_cross_cutting": metrics["security_redteam_cross_cutting"]["gate"],
        "causal_attribution": attribution_gate,
        "review_integrity": review_integrity_gate,
    }
    if FAIL in release_gates.values():
        final_decision = FAIL
    elif REVIEW_REQUIRED in release_gates.values():
        final_decision = REVIEW_REQUIRED
    else:
        final_decision = PASS

    reasons = [
        f"{name}={state}"
        for name, state in sorted(release_gates.items())
        if state != PASS
    ]
    return {
        "run_id": run["run_id"],
        "injection": run["injection"],
        "candidate_id": run["candidate_id"],
        "candidate_content_sha256": lineage["candidate_content_sha256"],
        "baseline_content_sha256": lineage["baseline_content_sha256"],
        "candidate_exact_diff": lineage["exact_diff"],
        "changed_top_level_factors": lineage["changed_top_level_factors"],
        "reviewer_role": reviewer_role,
        "reviewer_has_required_eval_access": reviewer_has_required_eval_access,
        "reviewer_has_forbidden_access": reviewer_has_forbidden_access,
        "reviewer_is_blind_by_access_matrix": reviewer_is_blind,
        "prohibited_access_attempted": prohibited_access_attempted,
        "private_payload_disclosed": private_payload_disclosed,
        "review_integrity_status": review_integrity_status,
        "attribution_status": attribution_status,
        "canonical_layer_metrics": metrics,
        "release_gates": release_gates,
        "final_decision": final_decision,
        "decision_derivation": reasons or ["all configured release gates PASS"],
        "real_world_evidence_fabricated": False,
        "candidate_applied_externally": False,
        "external_side_effects": 0,
        "records": list(records),
    }


def validate_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    expected_layers = [
        "training",
        "regression",
        "holdout",
        "representative_real_world",
    ]
    if fixture["canonical_data_layers"] != expected_layers:
        raise ValueError("canonical_data_layers must be the four frozen layers")
    if not fixture["security_redteam_contract"]["not_a_canonical_data_layer"]:
        raise ValueError("security/red-team must not be declared a fifth layer")
    private_resources = fixture.get("private_resources", [])
    if not private_resources or len(private_resources) != len(set(private_resources)):
        raise ValueError("private_resources must be a non-empty unique list")
    review_contract = fixture.get("replacement_review_contract", {})
    required_contract_keys = {
        "reviewer_role",
        "required_resources",
        "forbidden_resources",
        "required_trial_ids",
    }
    if set(review_contract) != required_contract_keys:
        raise ValueError("replacement_review_contract must use the frozen four-field schema")
    if set(review_contract["required_resources"]) & set(review_contract["forbidden_resources"]):
        raise ValueError("replacement reviewer required and forbidden resources must be disjoint")

    all_records: List[Dict[str, Any]] = list(fixture["trial_records"]) + list(
        fixture["access_requests"]
    )
    task_ids = [record.get("task_id") for record in all_records]
    trial_ids = [record.get("trial_id") for record in all_records]
    if None in task_ids or None in trial_ids:
        raise ValueError("every execution record must have task_id and trial_id")
    if len(task_ids) != len(set(task_ids)):
        raise ValueError("task_id values must be globally unique in the fixture")
    if len(trial_ids) != len(set(trial_ids)):
        raise ValueError("trial_id values must be globally unique in the fixture")
    known_trial_ids = {
        record["trial_id"] for record in fixture["trial_records"]
    }
    if not set(review_contract["required_trial_ids"]).issubset(known_trial_ids):
        raise ValueError("replacement review contract references unknown trial_id")

    valid_layers = set(expected_layers)
    invalid_layers = sorted({
        record["data_layer"]
        for record in fixture["trial_records"]
        if record["data_layer"] not in valid_layers
    })
    if invalid_layers:
        raise ValueError(f"invalid canonical layers: {invalid_layers}")
    for record in fixture["trial_records"]:
        if SECURITY_SUITE in record["suite_memberships"]:
            if record["scenario"] != "adversarial":
                raise ValueError("security/red-team record must be adversarial")
        if record["actual"] == "UNKNOWN" and record["expected"] == "UNKNOWN":
            raise ValueError("UNKNOWN cannot be its own passing answer")

    candidate_ids = [fixture["baseline_candidate"]["candidate_id"]] + [
        candidate["candidate_id"] for candidate in fixture["candidate_inputs"]
    ]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("candidate_id values must be unique")
    forbidden = []
    for candidate in [fixture["baseline_candidate"]] + fixture["candidate_inputs"]:
        forbidden.extend(forbidden_candidate_keys(candidate["content"], candidate["candidate_id"]))
    if forbidden:
        raise ValueError(f"candidate input self-reports derived evidence: {forbidden}")

    run_ids = [run["run_id"] for run in fixture["runs"]]
    if len(run_ids) != len(set(run_ids)):
        raise ValueError("run_id values must be unique")
    known_runs = set(run_ids)
    if any(record["run_id"] not in known_runs for record in all_records):
        raise ValueError("execution record references unknown run_id")
    return {
        "execution_record_count": len(all_records),
        "unique_task_ids": len(set(task_ids)),
        "unique_trial_ids": len(set(trial_ids)),
        "candidate_inputs_contain_no_self_reported_hash_diff_or_decision": True,
        "canonical_layer_contract": PASS,
    }


def build_result(fixture: Dict[str, Any], input_bytes: bytes, runner_bytes: bytes) -> Dict[str, Any]:
    validation = validate_fixture(fixture)
    baseline = fixture["baseline_candidate"]
    baseline_content = baseline["content"]
    candidates = {candidate["candidate_id"]: candidate for candidate in fixture["candidate_inputs"]}
    lineage = {
        candidate_id: make_lineage(candidate_id, baseline_content, candidate["content"])
        for candidate_id, candidate in sorted(candidates.items())
    }

    combined = candidates["candidate-A-combined"]["content"]
    splits = build_single_factor_splits(baseline_content, combined)
    combined_factors = lineage["candidate-A-combined"]["changed_top_level_factors"]
    if combined_factors != ["model", "prompt", "tool_schema"]:
        raise ValueError(
            "injection A must simultaneously change model, prompt and tool_schema"
        )
    if any(split["lineage"]["changed_top_level_factor_count"] != 1 for split in splits):
        raise ValueError("injection A split candidates must each change exactly one factor")

    evaluated_records = [evaluate_record(record) for record in fixture["trial_records"]]
    evaluated_access = access_events(fixture)
    records_by_run = {
        run["run_id"]: [
            record for record in evaluated_records if record["run_id"] == run["run_id"]
        ]
        for run in fixture["runs"]
    }
    access_by_run = {
        run["run_id"]: [
            event for event in evaluated_access if event["run_id"] == run["run_id"]
        ]
        for run in fixture["runs"]
    }
    run_results = [
        decide_run(
            run,
            lineage[run["candidate_id"]],
            records_by_run[run["run_id"]],
            access_by_run[run["run_id"]],
            fixture["access_matrix"],
            fixture["replacement_review_contract"],
        )
        for run in fixture["runs"]
    ]
    runs = {run["run_id"]: run for run in run_results}

    b = runs["run-B-training-perfect"]
    b_training = b["canonical_layer_metrics"]["training"]
    b_holdout = b["canonical_layer_metrics"]["ordinary_holdout_view"]
    b_security = b["canonical_layer_metrics"]["security_redteam_cross_cutting"]
    c_access = access_by_run["run-C-contaminated"]
    c_replacement = runs["run-C-blind-replacement"]
    review_contract = fixture["replacement_review_contract"]
    replacement_trial_ids = {
        record["trial_id"] for record in c_replacement["records"]
    }
    required_replacement_trials = set(review_contract["required_trial_ids"])
    replacement_review_completed = required_replacement_trials.issubset(
        replacement_trial_ids
    )
    private_resource_decisions = [
        row
        for event in c_access
        for row in event["resource_decisions"]
        if row["private"]
    ]
    all_private_resources_denied = bool(private_resource_decisions) and all(
        row["decision"] == "DENY" for row in private_resource_decisions
    )
    a_causal_rejected = (
        runs["run-A-combined"]["attribution_status"]
        == "REJECTED_CONFOUNDED_MULTI_VARIABLE_CHANGE"
    )
    a_splits_valid = (
        len(splits) == 3
        and {split["lineage"]["changed_top_level_factors"][0] for split in splits}
        == {"model", "prompt", "tool_schema"}
        and all(split["lineage"]["changed_top_level_factor_count"] == 1 for split in splits)
    )

    injection_checks = {
        "A": {
            "combined_candidate_changed_factors": combined_factors,
            "causal_attribution_rejected": a_causal_rejected,
            "combined_candidate_decision": runs["run-A-combined"]["final_decision"],
            "single_factor_candidates_created": [
                {
                    "candidate_id": split["candidate_id"],
                    "candidate_content_sha256": split["lineage"]["candidate_content_sha256"],
                    "changed_top_level_factors": split["lineage"]["changed_top_level_factors"],
                    "exact_diff": split["lineage"]["exact_diff"],
                }
                for split in splits
            ],
            "single_factor_split_contract_satisfied": a_splits_valid,
            "verdict": (
                PASS
                if combined_factors == ["model", "prompt", "tool_schema"]
                and a_causal_rejected
                and a_splits_valid
                else FAIL
            ),
        },
        "B": {
            "training": f"{b_training['pass']}/{b_training['total']}",
            "regression": (
                f"{b['canonical_layer_metrics']['regression']['pass']}/"
                f"{b['canonical_layer_metrics']['regression']['total']}"
            ),
            "ordinary_holdout": f"{b_holdout['pass']}/{b_holdout['total']}",
            "security_redteam_cross_cutting": f"{b_security['pass']}/{b_security['total']}",
            "representative_real_world_samples": (
                b["canonical_layer_metrics"]["representative_real_world"]["total"]
            ),
            "training_full_score_overrode_holdout_or_security": False,
            "candidate_final_decision": b["final_decision"],
            "verdict": PASS if b_training["fail"] == 0 and b["final_decision"] == FAIL else FAIL,
        },
        "C": {
            "mentor_private_access_decision": c_access[0]["access_decision"],
            "private_payload_disclosed": c_access[0]["private_payload_disclosed"],
            "all_private_resources_denied": all_private_resources_denied,
            "contaminated_round_decision": runs["run-C-contaminated"]["final_decision"],
            "contaminated_round_status": runs["run-C-contaminated"]["review_integrity_status"],
            "replacement_reviewer": c_replacement["reviewer_role"],
            "replacement_is_blind_by_matrix": c_replacement["reviewer_is_blind_by_access_matrix"],
            "replacement_has_required_eval_access": c_replacement["reviewer_has_required_eval_access"],
            "replacement_has_forbidden_access": c_replacement["reviewer_has_forbidden_access"],
            "replacement_review_completed": replacement_review_completed,
            "required_replacement_trial_ids": sorted(required_replacement_trials),
            "replacement_review_decision": c_replacement["final_decision"],
            "verdict": (
                PASS
                if all_private_resources_denied
                and not any(event["private_payload_disclosed"] for event in c_access)
                and runs["run-C-contaminated"]["final_decision"] == FAIL
                and c_replacement["reviewer_is_blind_by_access_matrix"]
                and c_replacement["reviewer_has_required_eval_access"]
                and not c_replacement["reviewer_has_forbidden_access"]
                and replacement_review_completed
                else FAIL
            ),
        },
    }

    retained_nonpass = [
        record
        for record in evaluated_records
        if record["evaluation_status"] in {FAIL, REVIEW_REQUIRED}
    ]
    unknown_records = [
        record for record in retained_nonpass if record["actual"] == "UNKNOWN"
    ]
    overall_control = (
        PASS if all(check["verdict"] == PASS for check in injection_checks.values()) else FAIL
    )
    return {
        "schema_version": "c08-training-lineage-redteam-results.v2",
        "fixture_id": fixture["fixture_id"],
        "run_type": "deterministic_offline_synthetic_control",
        "scope": fixture["scope"],
        "source_integrity": {
            "input_sha256": sha256_bytes(input_bytes),
            "runner_sha256": sha256_bytes(runner_bytes),
            "candidate_hashes_and_diffs_computed_by_runner": True,
            "input_candidates_self_report_derived_evidence": False,
        },
        "record_identity": validation,
        "data_contract": {
            "canonical_layers": fixture["canonical_data_layers"],
            "security_redteam": fixture["security_redteam_contract"],
            "representative_real_world_fixture_count": sum(
                1
                for record in evaluated_records
                if record["data_layer"] == "representative_real_world"
            ),
            "real_world_evidence_fabricated": False,
            "unknown_maps_to_review_required": all(
                record["evaluation_status"] == REVIEW_REQUIRED for record in unknown_records
            ),
        },
        "baseline": {
            "candidate_id": baseline["candidate_id"],
            "candidate_content_sha256": content_sha256(baseline_content),
        },
        "candidate_lineage": lineage,
        "run_results": run_results,
        "access_events": evaluated_access,
        "injection_checks": injection_checks,
        "failure_and_unknown_preservation": {
            "retained_count": len(retained_nonpass),
            "unknown_count": len(unknown_records),
            "records": retained_nonpass,
            "run_level_failures": [
                {
                    "run_id": run["run_id"],
                    "final_decision": run["final_decision"],
                    "decision_derivation": run["decision_derivation"],
                }
                for run in run_results
                if run["final_decision"] == FAIL
            ],
        },
        "redteam_control_verdict": overall_control,
        "practice_editor_chief_or_rc_signed": False,
        "external_effects": {
            "network_calls": 0,
            "real_models_called": 0,
            "real_skills_or_memory_modified": 0,
            "release_actions": 0,
            "external_state_changes": 0,
        },
        "known_limits": [
            "Synthetic deterministic records do not prove language-model capability or training effect.",
            "Access separation is enforced by this local matrix, not by an OS sandbox or production identity system.",
            "The fixture has zero representative real-world samples, so otherwise passing candidates remain REVIEW_REQUIRED.",
            "No OpenClaw, Hermes, Muse, real Skill, Memory, model, credential, network, publication, or rollback target was used.",
        ],
    }


def make_summary(result: Dict[str, Any], result_sha256: str) -> str:
    checks = result["injection_checks"]
    lines = [
        "# C08 training-lineage X02 red-team summary",
        "",
        "This is deterministic offline synthetic control evidence, not a practice-gate or release approval.",
        "",
        f"- fixture: `{result['fixture_id']}`",
        f"- input SHA-256: `{result['source_integrity']['input_sha256']}`",
        f"- runner SHA-256: `{result['source_integrity']['runner_sha256']}`",
        f"- result SHA-256: `{result_sha256}`",
        f"- execution records: {result['record_identity']['execution_record_count']} with globally unique task_id and trial_id",
        f"- representative real-world fixtures: {result['data_contract']['representative_real_world_fixture_count']} (not fabricated)",
        f"- retained non-PASS records: {result['failure_and_unknown_preservation']['retained_count']}",
        f"- overall synthetic control verdict: `{result['redteam_control_verdict']}`",
        "",
        "## Injection results",
        "",
        (
            "- A: model, prompt and tool schema changed together; causal attribution was "
            f"rejected and {len(checks['A']['single_factor_candidates_created'])} single-factor candidates were generated."
        ),
        (
            "- B: training "
            f"{checks['B']['training']}, regression {checks['B']['regression']}, ordinary holdout "
            f"{checks['B']['ordinary_holdout']}, security/red-team "
            f"{checks['B']['security_redteam_cross_cutting']}; final decision "
            f"`{checks['B']['candidate_final_decision']}`."
        ),
        (
            "- C: mentor private-answer access was "
            f"`{checks['C']['mentor_private_access_decision']}`; contaminated round "
            f"`{checks['C']['contaminated_round_decision']}`; blind replacement review completed "
            f"with `{checks['C']['replacement_review_decision']}` because real-world evidence remains absent."
        ),
        "",
        "## Boundary",
        "",
        "No network, real model, real Skill/Memory, credential, production write, release, or external rollback was exercised. Practice, editor, chief-editor and release-candidate gates remain unsigned.",
        "",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=here / "training-lineage-redteam-input.yaml",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=here / "training-lineage-redteam-results.yaml",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=here / "training-lineage-redteam-summary.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_bytes = args.input.read_bytes()
    fixture = json.loads(input_bytes.decode("utf-8"))
    runner_bytes = Path(__file__).read_bytes()
    result = build_result(fixture, input_bytes, runner_bytes)
    result_bytes = json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ).encode("utf-8") + b"\n"
    args.results.write_bytes(result_bytes)
    result_sha256 = sha256_bytes(result_bytes)
    args.summary.write_text(make_summary(result, result_sha256), encoding="utf-8")


if __name__ == "__main__":
    main()

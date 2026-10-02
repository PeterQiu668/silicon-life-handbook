#!/usr/bin/env python3
"""Targeted C17 capability-evidence authority-binding regression."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path


def load_harness(path: Path):
    spec = importlib.util.spec_from_file_location("c17_routing_harness", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load routing harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    runner_path = Path(args.runner)
    source = json.loads(input_path.read_text(encoding="utf-8"))
    harness = load_harness(runner_path)
    harness.validate(source)

    wrong_digest = "sha256:" + "0" * 64
    cases = [
        ("valid_exact_binding", lambda case: None, "PASS"),
        (
            "dummy_reference",
            lambda case: case["common_observation"]["route"].update(
                {"capability_evidence_refs": ["dummy"]}
            ),
            "FAIL",
        ),
        (
            "missing_observed_record",
            lambda case: case["state"]["capability_evidence_registry"].pop("eval-C17-01"),
            "FAIL",
        ),
        (
            "revoked_observed_record",
            lambda case: case["state"]["capability_evidence_registry"]["eval-C17-01"].update(
                {"status": "REVOKED"}
            ),
            "FAIL",
        ),
        (
            "unknown_observed_record",
            lambda case: case["state"]["capability_evidence_registry"]["eval-C17-01"].update(
                {"status": "UNKNOWN"}
            ),
            "FAIL",
        ),
        (
            "wrong_observed_capability",
            lambda case: case["state"]["capability_evidence_registry"]["eval-C17-01"].update(
                {"capability": "summarization"}
            ),
            "FAIL",
        ),
        (
            "wrong_observed_task_version",
            lambda case: case["state"]["capability_evidence_registry"]["eval-C17-01"].update(
                {"task_version": 3}
            ),
            "FAIL",
        ),
        (
            "wrong_observed_permission_snapshot",
            lambda case: case["state"]["capability_evidence_registry"]["eval-C17-01"].update(
                {"permission_snapshot": "auth-v3"}
            ),
            "FAIL",
        ),
        (
            "well_formed_wrong_observed_digest",
            lambda case: case["state"]["capability_evidence_registry"]["eval-C17-01"].update(
                {"evidence_digest": wrong_digest}
            ),
            "FAIL",
        ),
        (
            "well_formed_wrong_authority_digest",
            lambda case: case["state"]["capability_evidence_authority"]["eval-C17-01"].update(
                {"evidence_digest": wrong_digest}
            ),
            "FAIL",
        ),
        (
            "missing_authority_record",
            lambda case: case["state"]["capability_evidence_authority"].pop("eval-C17-01"),
            "FAIL",
        ),
        (
            "wrong_authority_task_version",
            lambda case: case["state"]["capability_evidence_authority"]["eval-C17-01"].update(
                {"task_version": 3}
            ),
            "FAIL",
        ),
        (
            "wrong_authority_permission_snapshot",
            lambda case: case["state"]["capability_evidence_authority"]["eval-C17-01"].update(
                {"permission_snapshot": "auth-v3"}
            ),
            "FAIL",
        ),
        (
            "revoked_authority_record",
            lambda case: case["state"]["capability_evidence_authority"]["eval-C17-01"].update(
                {"status": "REVOKED"}
            ),
            "FAIL",
        ),
    ]

    records = []
    for case_id, mutate, expected in cases:
        case_source = copy.deepcopy(source)
        mutate(case_source)
        harness.validate(case_source)
        decision, trace, _, external_effects = harness.decide(
            copy.deepcopy(case_source["common_observation"]),
            case_source["common_contract"],
            case_source["state"],
        )
        records.append(
            {
                "case_id": case_id,
                "decision": decision,
                "expected": expected,
                "matched_expected": decision == expected,
                "terminal_trace": trace[-1],
                "external_side_effects": external_effects,
            }
        )

    if not all(record["matched_expected"] for record in records):
        raise ValueError("capability digest authority regression failed")
    if any(record["external_side_effects"] for record in records):
        raise ValueError("targeted regression produced an external side effect")

    result = {
        "schema_version": "c17.capability-digest-regression.v1",
        "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "runner_sha256": hashlib.sha256(runner_path.read_bytes()).hexdigest(),
        "case_count": len(records),
        "all_expected_matched": True,
        "external_side_effect_count": 0,
        "cases": records,
    }
    Path(args.output).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

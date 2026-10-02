#!/usr/bin/env python3
"""Non-author semantic and pinned-root attacks for the C21 v2.4 controller."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


REVIEW = Path(__file__).resolve().parent
RUNS = REVIEW / "runs"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "c21_v24_independent_runner", RUNS / "run-lifecycle-harness.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner()
    raw = json.loads((RUNS / "synthetic-lifecycle-input.yaml").read_text())
    root = json.loads((RUNS / "frozen-authority-root.yaml").read_text())
    source = runner.validate(copy.deepcopy(raw), copy.deepcopy(root))
    records: list[dict] = []

    def reseal_event(event: dict) -> None:
        event["receipt"]["record_digest"] = runner.record_digest(
            event["receipt"], "record_digest"
        )
        event["readback"]["record_digest"] = runner.record_digest(
            event["readback"], "record_digest"
        )
        event["record_digest"] = runner.record_digest(event, "record_digest")

    def semantic_attack(
        attack_id: str,
        scenario_id: str,
        mutate,
        expected: str,
        required_reason: str,
    ) -> None:
        local_source = copy.deepcopy(source)
        scenario = next(
            item for item in local_source["scenarios"] if item["scenario_id"] == scenario_id
        )
        state = runner.deep_merge(local_source["base_state"], scenario["overrides"])
        mutate(state)
        for key in runner.FROZEN_REGISTRIES:
            local_source["authority_root"][key] = copy.deepcopy(state[key])
        local_source["authority_root"]["root_digest"] = runner.sha256(
            {
                key: local_source["authority_root"][key]
                for key in sorted(runner.FROZEN_REGISTRIES)
            }
        )
        try:
            runner.validate_state(state)
            actual, reasons, _, _ = runner.evaluate(local_source, state, scenario)
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        matched = actual == expected and (
            required_reason == "NONE" or required_reason in reasons
        )
        records.append(
            {
                "attack_id": attack_id,
                "scenario_id": scenario_id,
                "expected": expected,
                "actual": actual,
                "required_reason": required_reason,
                "reasons": reasons,
                "matched": matched,
            }
        )

    def publication(state: dict) -> dict:
        return state["publication_event_registry"]["publication-release-21"]

    def retirement(state: dict) -> dict:
        return state["lifecycle_event_registry"]["retirement-lifecycle-21"]

    def late_legal(state: dict) -> None:
        state["legal_review"]["reviewed_at"] = "2026-09-30T11:25:00Z"
        event = publication(state)
        event["legal_review_digest"] = runner.sha256(state["legal_review"])
        reseal_event(event)

    semantic_attack(
        "legal-review-after-publication-execution",
        "V24-001",
        late_legal,
        "FAIL",
        "PUBLICATION_EVENT_SEQUENCE_INVALID",
    )

    def publication_request_after_review(state: dict) -> None:
        event = publication(state)
        event["requested_at"] = "2026-09-30T02:30:00Z"
        reseal_event(event)

    semantic_attack("publication-request-after-review", "V24-001", publication_request_after_review, "FAIL", "PUBLICATION_EVENT_SEQUENCE_INVALID")

    def release_approval_after_execution(state: dict) -> None:
        event = publication(state)
        event["release_approved_at"] = "2026-09-30T11:25:00Z"
        reseal_event(event)

    semantic_attack("release-approval-after-execution", "V24-001", release_approval_after_execution, "FAIL", "PUBLICATION_EVENT_SEQUENCE_INVALID")

    def plan_approval_after_execution(state: dict) -> None:
        event = publication(state)
        event["plan_approved_at"] = "2026-09-30T11:25:00Z"
        reseal_event(event)

    semantic_attack("plan-approval-after-execution", "V24-001", plan_approval_after_execution, "FAIL", "PUBLICATION_EVENT_SEQUENCE_INVALID")

    def publication_receipt_mismatch(state: dict) -> None:
        event = publication(state)
        event["receipt"]["executed_at"] = "2026-09-30T11:19:00Z"
        reseal_event(event)

    semantic_attack("publication-receipt-time-mismatch", "V24-001", publication_receipt_mismatch, "FAIL", "PUBLICATION_EVENT_BINDING_INVALID")

    def publication_future_readback(state: dict) -> None:
        event = publication(state)
        event["readback"]["observed_at"] = "2026-10-01T00:00:00Z"
        reseal_event(event)

    semantic_attack("publication-readback-after-evaluation", "V24-001", publication_future_readback, "FAIL", "PUBLICATION_EVENT_SEQUENCE_INVALID")

    def publication_same_actor(state: dict) -> None:
        event = publication(state)
        event["readback"]["observer"] = event["executed_by"]
        reseal_event(event)

    semantic_attack("publication-executor-is-observer", "V24-001", publication_same_actor, "FAIL", "PUBLICATION_EVENT_BINDING_INVALID")

    def publication_unknown(state: dict) -> None:
        event = publication(state)
        event["status"] = "UNKNOWN"
        event["receipt"]["status"] = "UNKNOWN"
        event["readback"]["status"] = "UNKNOWN"
        reseal_event(event)

    semantic_attack("publication-terminal-unknown", "V24-001", publication_unknown, "REVIEW_REQUIRED", "PUBLICATION_TERMINAL_UNKNOWN")

    def retirement_request_after_execution(state: dict) -> None:
        event = retirement(state)
        event["requested_at"] = "2026-09-30T11:35:00Z"
        reseal_event(event)

    semantic_attack("retirement-request-after-execution", "V24-039", retirement_request_after_execution, "FAIL", "RETIREMENT_LIFECYCLE_SEQUENCE_INVALID")

    def retirement_approval_after_execution(state: dict) -> None:
        event = retirement(state)
        event["retirement_approved_at"] = "2026-09-30T11:35:00Z"
        reseal_event(event)

    semantic_attack("retirement-approval-after-execution", "V24-039", retirement_approval_after_execution, "FAIL", "RETIREMENT_LIFECYCLE_SEQUENCE_INVALID")

    def retirement_future_readback(state: dict) -> None:
        event = retirement(state)
        event["readback"]["observed_at"] = "2026-10-01T00:00:00Z"
        reseal_event(event)

    semantic_attack("retirement-readback-after-evaluation", "V24-039", retirement_future_readback, "FAIL", "RETIREMENT_LIFECYCLE_SEQUENCE_INVALID")

    def retirement_same_actor(state: dict) -> None:
        event = retirement(state)
        event["readback"]["observer"] = event["executed_by"]
        reseal_event(event)

    semantic_attack("retirement-executor-is-observer", "V24-039", retirement_same_actor, "FAIL", "RETIREMENT_LIFECYCLE_BINDING_INVALID")

    def signoff_before_residual(state: dict) -> None:
        signoff = state["retirement_evidence_registry"]["ret-signoff-21"]
        signoff["issued_at"] = "2026-09-30T11:35:00Z"
        signoff["record_digest"] = runner.record_digest(signoff, "record_digest")

    semantic_attack("terminal-signoff-before-residual-scan", "V24-039", signoff_before_residual, "FAIL", "RETIREMENT_SIGNOFF_BEFORE_RESIDUAL_SCAN")

    def evidence_before_execution(state: dict) -> None:
        evidence = state["retirement_evidence_registry"]["ret-admission-21"]
        evidence["issued_at"] = "2026-09-30T11:29:00Z"
        evidence["record_digest"] = runner.record_digest(evidence, "record_digest")

    semantic_attack("retirement-evidence-before-execution", "V24-039", evidence_before_execution, "FAIL", "RETIREMENT_ADMISSION_STOPPED_INVALID")

    def authority_issued_after_approval(state: dict) -> None:
        authority = state["authority_registry"]["approval-retirement-21"]
        authority["issued_at"] = "2026-09-30T11:28:00Z"
        authority["not_before"] = "2026-09-30T11:28:00Z"
        authority["authority_digest"] = runner.record_digest(authority, "authority_digest")

    semantic_attack("retirement-authority-issued-after-recorded-approval", "V24-039", authority_issued_after_approval, "FAIL", "RETIREMENT_APPROVAL_TIME_INVALID")

    def retirement_unknown(state: dict) -> None:
        event = retirement(state)
        event["status"] = "UNKNOWN"
        event["receipt"]["status"] = "UNKNOWN"
        event["readback"]["status"] = "UNKNOWN"
        reseal_event(event)

    semantic_attack("retirement-terminal-unknown", "V24-039", retirement_unknown, "REVIEW_REQUIRED", "RETIREMENT_EXECUTION_UNKNOWN")

    # Black-box control: even a locally resealed complete registry root must not
    # replace the digest independently pinned in the runner.
    candidate_root = copy.deepcopy(root)
    candidate_root["publication_event_registry"]["publication-release-21"]["status"] = "UNKNOWN"
    reseal_event(candidate_root["publication_event_registry"]["publication-release-21"])
    candidate_root["root_digest"] = runner.sha256(
        {key: candidate_root[key] for key in sorted(runner.FROZEN_REGISTRIES)}
    )
    candidate = copy.deepcopy(raw)
    candidate["authority_root_digest"] = candidate_root["root_digest"]
    for key in runner.FROZEN_REGISTRIES:
        candidate["base_state"][key] = copy.deepcopy(candidate_root[key])
    try:
        runner.validate(candidate, candidate_root)
        actual, reasons = "PASS", []
    except (KeyError, TypeError, ValueError) as exc:
        actual, reasons = "SCHEMA_REJECT", [str(exc)]
    records.append(
        {
            "attack_id": "publication-root-locally-resealed",
            "scenario_id": "ROOT",
            "expected": "SCHEMA_REJECT",
            "actual": actual,
            "required_reason": "NONE",
            "reasons": reasons,
            "matched": actual == "SCHEMA_REJECT",
        }
    )

    report = {
        "schema_version": "c21.lifecycle.independent-negative.v2.4",
        "attack_count": len(records),
        "matched_count": sum(bool(row["matched"]) for row in records),
        "escape_count": sum(not bool(row["matched"]) for row in records),
        "attacks": records,
    }
    report["suite_digest"] = "sha256:" + runner.hashlib.sha256(
        runner.canonical(records).encode()
    ).hexdigest()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    if report["escape_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

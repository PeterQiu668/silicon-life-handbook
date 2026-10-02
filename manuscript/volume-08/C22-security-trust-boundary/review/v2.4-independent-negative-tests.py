#!/usr/bin/env python3
"""Non-author near-neighbor attacks for the C19 v2.4 security controller.

Every attack starts from S23, the author's only terminal-effect PASS control.
The script does not read author expected values or scenario names to decide an
outcome.  A mutation is intercepted only when the previously passing control
becomes FAIL or is rejected by the closed schema.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


REVIEW = Path(__file__).resolve().parent
RUNS = REVIEW / "runs"
OUTPUT = REVIEW / "v2.4-independent-reproduction-20261001.yaml"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "c19_v24_independent_runner", RUNS / "run-security-harness.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner()
    raw = json.loads((RUNS / "synthetic-security-input.yaml").read_text(encoding="utf-8"))
    raw_authority = json.loads((RUNS / "frozen-security-authority.yaml").read_text(encoding="utf-8"))
    authority = runner.validate_authority_bundle(copy.deepcopy(raw_authority))
    source = runner.validate_source(copy.deepcopy(raw), authority)
    baseline = copy.deepcopy(next(item for item in source["scenarios"] if item["id"] == "S23"))
    baseline_actual, baseline_hard, baseline_review, _ = runner.evaluate(
        baseline, source, authority
    )
    if baseline_actual != "PASS" or baseline_hard or baseline_review:
        raise RuntimeError("S23 is not a clean PASS control")

    records: list[dict] = []

    def record(attack_id: str, family: str, actual: str, reasons: list[str]) -> None:
        records.append(
            {
                "attack_id": attack_id,
                "family": family,
                "baseline": "PASS",
                "actual": actual,
                "matched": actual in {"FAIL", "SCHEMA_REJECT"},
                "reasons": sorted(set(reasons)),
            }
        )

    def attack(attack_id: str, family: str, state_mutate, authority_mutate=None) -> None:
        scenario = copy.deepcopy(baseline)
        candidate_authority = copy.deepcopy(authority)
        state_mutate(scenario["state"])
        if authority_mutate is not None:
            authority_mutate(candidate_authority)
        try:
            runner.validate_state(scenario["state"], f"independent.{attack_id}")
            actual, hard, review, _ = runner.evaluate(
                scenario, source, candidate_authority
            )
            reasons = [*hard, *review]
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        record(attack_id, family, actual, reasons)

    def receipt_digest(state: dict) -> None:
        receipt = state["receipts"][0]
        receipt["digest"] = runner.digest(
            {key: value for key, value in receipt.items() if key != "digest"}
        )

    def readback_digest(candidate_authority: dict, readback_id: str = "readback-pass") -> None:
        readback = candidate_authority["registries"]["readbacks"][readback_id]
        readback["record_digest"] = runner.digest(
            {key: value for key, value in readback.items() if key != "record_digest"}
        )

    def before_credential_window(state: dict) -> None:
        state["effects"][0]["executed_at"] = "2026-09-30T11:29:59Z"
        state["receipts"][0].update(
            executed_at="2026-09-30T11:29:59Z",
            issued_at="2026-09-30T11:30:00Z",
        )
        receipt_digest(state)

    attack(
        "effect-one-second-before-credential-window",
        "authorization-time",
        before_credential_window,
    )

    def at_credential_expiry(state: dict) -> None:
        state["effects"][0]["executed_at"] = "2026-09-30T12:30:00Z"
        state["receipts"][0].update(
            executed_at="2026-09-30T12:30:00Z",
            issued_at="2026-09-30T12:30:01Z",
        )
        receipt_digest(state)

    attack("effect-at-credential-expiry", "authorization-time", at_credential_expiry)

    def receipt_before_effect(state: dict) -> None:
        state["receipts"][0]["issued_at"] = "2026-09-30T11:59:49Z"
        receipt_digest(state)

    attack("receipt-one-second-before-effect", "causal-time", receipt_before_effect)

    attack(
        "evaluation-before-readback",
        "causal-time",
        lambda state: None,
        lambda candidate: (
            candidate["registries"]["readbacks"]["readback-pass"].update(
                observed_at="2026-10-02T00:00:00Z"
            ),
            readback_digest(candidate),
        ),
    )

    attack(
        "readback-observer-inactive",
        "observer-independence",
        lambda state: None,
        lambda candidate: candidate["registries"]["principals"]["audit-authority"].update(
            status="REVOKED"
        ),
    )

    attack(
        "readback-observer-role-removed",
        "observer-independence",
        lambda state: None,
        lambda candidate: candidate["registries"]["principals"]["audit-authority"].update(
            roles=[]
        ),
    )

    def owner_observes(candidate: dict) -> None:
        readback = candidate["registries"]["readbacks"]["readback-pass"]
        readback.update(
            observer="principal-human-owner",
            authority_ref="principal-human-owner",
        )
        readback_digest(candidate)

    attack(
        "approver-substituted-as-readback-observer",
        "observer-independence",
        lambda state: None,
        owner_observes,
    )

    def wrong_receipt_readback(candidate: dict) -> None:
        candidate["registries"]["readbacks"]["readback-pass"]["receipt_id"] = "receipt-other"
        readback_digest(candidate)

    attack(
        "readback-receipt-substitution",
        "readback-binding",
        lambda state: None,
        wrong_receipt_readback,
    )

    def wrong_terminal(candidate: dict) -> None:
        candidate["registries"]["readbacks"]["readback-pass"]["terminal_status"] = "FAILED"
        readback_digest(candidate)

    attack(
        "readback-terminal-status-substitution",
        "readback-binding",
        lambda state: None,
        wrong_terminal,
    )

    def wrong_snapshot(candidate: dict) -> None:
        candidate["registries"]["readbacks"]["readback-pass"][
            "authorization_snapshot_digest"
        ] = runner.digest("substituted-snapshot")
        readback_digest(candidate)

    attack(
        "readback-authorization-snapshot-substitution",
        "readback-binding",
        lambda state: None,
        wrong_snapshot,
    )

    attack(
        "terminal-effect-without-readback-ref",
        "terminal-effect",
        lambda state: state["effects"][0].update(readback_ref=""),
    )

    def receipt_status_mismatch(state: dict) -> None:
        state["receipts"][0]["status"] = "FAILED"
        receipt_digest(state)

    attack("receipt-terminal-status-mismatch", "receipt-binding", receipt_status_mismatch)

    def duplicate_effect(state: dict) -> None:
        duplicate = copy.deepcopy(state["effects"][0])
        duplicate["effect_id"] = "effect-pass-duplicate"
        state["effects"].append(duplicate)

    attack("second-effect-reuses-receipt-and-readback", "duplicate-effect", duplicate_effect)

    def duplicate_receipt(state: dict) -> None:
        duplicate = copy.deepcopy(state["receipts"][0])
        duplicate["receipt_id"] = "receipt-pass-duplicate"
        duplicate["digest"] = runner.digest(
            {key: value for key, value in duplicate.items() if key != "digest"}
        )
        state["receipts"].append(duplicate)

    attack("orphan-duplicate-receipt", "duplicate-receipt", duplicate_receipt)

    attack(
        "terminal-effect-claims-external-side-effect",
        "external-effect",
        lambda state: state["effects"][0].update(external_side_effect=True),
    )

    def audit_drops_readback_digest(state: dict) -> None:
        effect_event = next(
            event for event in state["audit"]["events"] if event["event_type"] == "EFFECT"
        )
        effect_event["payload"]["readback_digest"] = runner.digest("missing-readback")

    attack(
        "audit-readback-digest-substitution",
        "audit-binding",
        audit_drops_readback_digest,
    )

    def audit_drops_receipt_time(state: dict) -> None:
        effect_event = next(
            event for event in state["audit"]["events"] if event["event_type"] == "EFFECT"
        )
        effect_event["payload"]["receipt_issued_at"] = "NONE"

    attack(
        "audit-receipt-time-erased",
        "audit-binding",
        audit_drops_receipt_time,
    )

    attack(
        "effect-executor-substitution",
        "effect-binding",
        lambda state: state["effects"][0].update(executor="principal-human-owner"),
    )

    result = {
        "schema_version": "c19.security.independent.v2.4",
        "reviewer_role": "non_author",
        "baseline_control": {"scenario_id": "S23", "decision": baseline_actual},
        "attack_count": len(records),
        "matched_count": sum(item["matched"] for item in records),
        "escape_count": sum(not item["matched"] for item in records),
        "suite_digest": runner.digest(records),
        "attacks": records,
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                key: result[key]
                for key in ("attack_count", "matched_count", "escape_count", "suite_digest")
            },
            ensure_ascii=False,
        )
    )
    raise SystemExit(1 if result["escape_count"] else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Non-author near-neighbor attacks for the C19 v2.2 security harness."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


RUNS = Path(__file__).resolve().parent / "runs"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "c19_v22_independent_runner", RUNS / "run-security-harness.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner()
    raw_source = json.loads((RUNS / "synthetic-security-input.yaml").read_text())
    authority = runner.validate_authority_bundle(
        json.loads((RUNS / "frozen-security-authority.yaml").read_text())
    )
    source = runner.validate_source(copy.deepcopy(raw_source), authority)
    positive = next(item for item in source["scenarios"] if item["id"] == "S01")
    contained = next(item for item in source["scenarios"] if item["id"] == "S16")
    records = []

    def state_attack(attack_id, mutate, expected="FAIL"):
        scenario = copy.deepcopy(positive)
        mutate(scenario)
        try:
            runner.validate_state(scenario["state"], f"attack.{attack_id}")
            actual, hard, review, _ = runner.evaluate(scenario, source, authority)
            reasons = [*hard, *review]
        except (TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        records.append(
            {
                "id": attack_id,
                "expected": expected,
                "actual": actual,
                "matched": actual == expected,
                "reasons": reasons,
            }
        )

    def source_attack(attack_id, mutate, expected="FAIL"):
        candidate = copy.deepcopy(raw_source)
        mutate(candidate)
        try:
            checked = runner.validate_source(candidate, authority)
            result = runner.build_result(checked, authority)
            positive_row = next(item for item in result["trials"] if item["scenario_id"] == "S01")
            actual, reasons = positive_row["decision"], positive_row["reasons"]
        except (TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        records.append(
            {
                "id": attack_id,
                "expected": expected,
                "actual": actual,
                "matched": actual == expected,
                "reasons": reasons,
            }
        )

    def applied_effect_with_wrong_target(scenario):
        state = scenario["state"]
        state["incident"] = copy.deepcopy(contained["state"]["incident"])
        state["recovery"] = copy.deepcopy(contained["state"]["recovery"])
        effect = state["effects"][0]
        effect.update(status="APPLIED", receipt_ref="receipt-wrong-target")
        receipt = {
            "receipt_id": "receipt-wrong-target",
            "effect_id": effect["effect_id"],
            "status": "APPLIED",
            "authoritative_readback": "APPLIED",
            "target": "different-object",
        }
        receipt["digest"] = runner.digest(receipt)
        state["receipts"] = [receipt]

    state_attack("receipt_target_not_bound_to_effect_object", applied_effect_with_wrong_target)

    def applied_effect_without_audit_event(scenario):
        applied_effect_with_wrong_target(scenario)
        scenario["state"]["receipts"][0]["target"] = "synthetic-report"
        body = {
            key: scenario["state"]["receipts"][0][key]
            for key in ["receipt_id", "effect_id", "status", "authoritative_readback", "target"]
        }
        scenario["state"]["receipts"][0]["digest"] = runner.digest(body)

    state_attack("applied_effect_absent_from_audit_chain", applied_effect_without_audit_event)

    def open_incident_without_response(scenario):
        scenario["state"]["incident"].update(
            incident_id="incident-s16",
            state="OPEN",
            evidence_refs=["incident-evidence-s16"],
        )

    state_attack("open_incident_with_all_controls_false", open_incident_without_response)

    state_attack(
        "critical_residual_risk_with_recovery_not_needed",
        lambda scenario: scenario["state"]["recovery"].update(
            residual_risk="critical-unresolved"
        ),
    )
    state_attack(
        "tenant_session_expiry_self_extended_without_registry",
        lambda scenario: scenario["state"]["tenant_session"].update(
            expires_at="2036-10-01T00:00:00Z"
        ),
    )

    def relabel_layers(candidate):
        first = next(item for item in candidate["scenarios"] if item["id"] == "S01")
        holdout = next(item for item in candidate["scenarios"] if item["id"] == "S09")
        first["layer"], holdout["layer"] = "holdout", "training"

    source_attack("scenario_layers_swapped_without_state_evidence", relabel_layers)

    source_attack(
        "scenario_task_and_trial_ids_not_bound_to_evidence",
        lambda candidate: next(
            item for item in candidate["scenarios"] if item["id"] == "S01"
        ).update(task_id="task-unregistered", trial_id="trial-unregistered"),
    )
    source_attack(
        "scenario_self_claims_security_red_team",
        lambda candidate: next(
            item for item in candidate["scenarios"] if item["id"] == "S01"
        ).update(security_red_team=True),
    )
    source_attack(
        "scenario_self_claims_non_shadow_execution",
        lambda candidate: next(
            item for item in candidate["scenarios"] if item["id"] == "S01"
        ).update(synthetic_shadow=True),
    )

    report = {
        "attack_count": len(records),
        "matched_count": sum(record["matched"] for record in records),
        "fail_open_count": sum(not record["matched"] for record in records),
        "attacks": records,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["fail_open_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

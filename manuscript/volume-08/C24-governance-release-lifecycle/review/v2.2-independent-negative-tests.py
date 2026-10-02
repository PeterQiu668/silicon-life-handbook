#!/usr/bin/env python3
"""Non-author near-neighbor attacks for the C21 v2.2 lifecycle harness."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


RUNS = Path(__file__).resolve().parent / "runs"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "c21_v22_independent_runner", RUNS / "run-lifecycle-harness.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner()
    raw_source = json.loads((RUNS / "synthetic-lifecycle-input.yaml").read_text())
    authority_root = json.loads((RUNS / "frozen-authority-root.yaml").read_text())
    source = runner.validate(copy.deepcopy(raw_source), copy.deepcopy(authority_root))
    records = []

    def state_attack(attack_id, mutate, expected="FAIL"):
        state = copy.deepcopy(source["base_state"])
        mutate(state)
        try:
            runner.validate_state(state)
            actual, reasons, _, _ = runner.evaluate(source, state)
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
        candidate["scenarios"] = [copy.deepcopy(candidate["scenarios"][0])]
        mutate(candidate)
        try:
            checked = runner.validate(candidate, copy.deepcopy(authority_root))
            scenario = checked["scenarios"][0]
            state = runner.deep_merge(checked["base_state"], scenario["overrides"])
            runner.validate_state(state)
            actual, reasons, _, _ = runner.evaluate(checked, state)
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

    state_attack(
        "unapproved_canary_to_limited_stage_escalation",
        lambda state: (
            state["rollout"].update(stage="LIMITED"),
            state["runtime_state"].update(admission="OPEN_LIMITED"),
        ),
    )
    state_attack(
        "unapproved_rollout_budget_expansion",
        lambda state: state["rollout"].update(max_trials=1_000_000, max_cost=1_000_000),
    )
    state_attack(
        "self_expanded_baseline_and_candidate_permissions",
        lambda state: (
            state["rollout"]["baseline_permissions"].append("external-admin"),
            state["rollout"]["candidate_permissions"].append("external-admin"),
        ),
    )
    state_attack(
        "zero_trial_ledger_claims_release_pass",
        lambda state: state.update(trial_ledger=[]),
    )

    def add_self_authorized_internal_effect(state):
        state["runtime_state"]["effect_ledger"].append(
            {
                "effect_id": "effect-self-authorized",
                "status": "APPLIED",
                "authorized": True,
                "external": False,
                "readback": "CONFIRMED",
                "owner": "human-operations",
                "tenant_id": state["rollout"]["allowed_tenants"][0],
                "task_type": state["rollout"]["allowed_tasks"][0],
                "action": state["rollout"]["allowed_actions"][0],
            }
        )

    state_attack(
        "internal_effect_self_attests_authorized_without_authority_ref",
        add_self_authorized_internal_effect,
    )

    def add_unapproved_webhook(state):
        state["runtime_state"]["webhooks"].append(
            {
                "webhook_id": "webhook-unapproved",
                "state": "ACTIVE",
                "owner": "human-operations",
                "tenant_id": state["rollout"]["allowed_tenants"][0],
                "task_type": state["rollout"]["allowed_tasks"][0],
                "action": state["rollout"]["allowed_actions"][0],
            }
        )

    state_attack("active_webhook_without_authority_or_manifest", add_unapproved_webhook)

    source_attack(
        "scenario_claims_holdout_while_trial_ledger_remains_training",
        lambda candidate: candidate["scenarios"][0].update(
            layer="holdout", holdout_ref="holdout-research-21"
        ),
    )
    source_attack(
        "scenario_task_and_trial_ids_unbound_to_trial_ledger",
        lambda candidate: candidate["scenarios"][0].update(
            task_id="task-unregistered", trial_id="trial-unregistered"
        ),
    )
    source_attack(
        "scenario_self_claims_security_coverage",
        lambda candidate: candidate["scenarios"][0].update(
            security_slices=["imaginary-authz", "imaginary-red-team"]
        ),
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

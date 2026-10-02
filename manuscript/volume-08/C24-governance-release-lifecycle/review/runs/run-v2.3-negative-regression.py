#!/usr/bin/env python3
"""Author-side adjacent negative regression for the C21 v2.3 controller."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_runner():
    spec = importlib.util.spec_from_file_location("c21_v23_runner", HERE / "run-lifecycle-harness.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def aggregate(result: tuple[str, list[str], dict, int]) -> tuple[str, list[str]]:
    return result[0], result[1]


def main() -> None:
    runner = load_runner()
    raw = json.loads((HERE / "synthetic-lifecycle-input.yaml").read_text(encoding="utf-8"))
    root = json.loads((HERE / "frozen-authority-root.yaml").read_text(encoding="utf-8"))
    source = runner.validate(copy.deepcopy(raw), copy.deepcopy(root))
    rows: list[dict] = []

    def state_attack(attack_id: str, change) -> None:
        state = copy.deepcopy(source["base_state"])
        change(state)
        try:
            runner.validate_state(state)
            actual, reasons = aggregate(runner.evaluate(source, state, source["scenarios"][0]))
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        rows.append({"attack_id": attack_id, "expected": "FAIL", "actual": actual, "passed": actual in {"FAIL", "SCHEMA_REJECT"}, "reasons": reasons})

    def source_attack(attack_id: str, change) -> None:
        candidate = copy.deepcopy(raw)
        candidate["scenarios"] = [copy.deepcopy(candidate["scenarios"][0])]
        change(candidate)
        try:
            checked = runner.validate(candidate, copy.deepcopy(root))
            scenario = checked["scenarios"][0]
            state = runner.deep_merge(checked["base_state"], scenario["overrides"])
            runner.validate_state(state)
            actual, reasons = aggregate(runner.evaluate(checked, state, scenario))
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        rows.append({"attack_id": attack_id, "expected": "FAIL", "actual": actual, "passed": actual in {"FAIL", "SCHEMA_REJECT"}, "reasons": reasons})

    state_attack("plan-stage-escalation", lambda s: (s["rollout"].update(stage="LIMITED"), s["runtime_state"].update(admission="OPEN_LIMITED")))
    state_attack("plan-max-trials-expansion", lambda s: s["rollout"].update(max_trials=1_000_000))
    state_attack("plan-max-cost-expansion", lambda s: s["rollout"].update(max_cost=1_000_000.0))
    state_attack("plan-candidate-permission-expansion", lambda s: s["rollout"]["candidate_permissions"].append("external-admin"))
    state_attack("plan-both-permission-expansion", lambda s: (s["rollout"]["candidate_permissions"].append("external-admin"), s["rollout"]["baseline_permissions"].append("external-admin")))
    state_attack("plan-window-expansion", lambda s: s["rollout"].update(expires_at="2027-01-01T00:00:00Z"))
    state_attack("plan-environment-substitution", lambda s: s["rollout"].update(environment_ref="env-restore-isolated-21"))
    state_attack("zero-trial-ledger", lambda s: s.update(trial_ledger=[]))
    state_attack("one-trial-deleted", lambda s: s["trial_ledger"].pop())
    state_attack("trial-cost-resealed-locally", lambda s: (s["trial_ledger"][0].update(cost=0.0), s["trial_ledger"][0].update(trial_digest=runner.record_digest(s["trial_ledger"][0], "trial_digest"))))
    state_attack("trial-dataset-resealed-locally", lambda s: (s["trial_ledger"][0].update(dataset_ref="dataset-training-21", layer="training", holdout_ref="NONE"), s["trial_ledger"][0].update(trial_digest=runner.record_digest(s["trial_ledger"][0], "trial_digest"))))
    state_attack("trial-terminal-missing", lambda s: s["trial_ledger"][0].update(terminal_ref="terminal-missing"))
    state_attack("effect-self-authorized", lambda s: s["runtime_state"]["effect_ledger"].append({"effect_id":"effect-self","status":"APPLIED","authorized":True,"readback":"CONFIRMED","external":False,"owner":"human-operations","tenant_id":"tenant-synthetic","task_type":"research","action":"read"}))
    state_attack("effect-fake-evidence-refs", lambda s: s["runtime_state"]["effect_ledger"].append({"effect_id":"effect-fake","status":"APPLIED","external":False,"owner":"human-operations","tenant_id":"tenant-synthetic","task_type":"research","action":"read","authority_ref":"fake","receipt_ref":"fake","readback_ref":"fake"}))
    state_attack("active-webhook-without-manifest", lambda s: s["runtime_state"]["webhooks"].append({"webhook_id":"hook-new","state":"ACTIVE","owner":"human-operations","tenant_id":"tenant-synthetic","task_type":"research","action":"read"}))
    state_attack("active-schedule-wrong-manifest", lambda s: s["runtime_state"]["schedules"].append({"schedule_id":"cron-new","state":"ACTIVE","owner":"human-operations","tenant_id":"tenant-synthetic","task_type":"research","action":"read","manifest_ref":"manifest-hook-synthetic"}))
    state_attack("task-manifest-object-mismatch", lambda s: s["runtime_state"]["tasks"][0].update(manifest_ref="manifest-hook-synthetic"))
    source_attack("scenario-layer-self-claim", lambda s: s["scenarios"][0].update(layer="holdout", holdout_ref="holdout-research-21"))
    source_attack("scenario-task-trial-unregistered", lambda s: s["scenarios"][0].update(task_id="task-fake", trial_id="trial-fake"))
    source_attack("scenario-security-imaginary", lambda s: s["scenarios"][0].update(security_slices=["imaginary-authz"]))
    source_attack("scenario-security-valid-but-unexecuted", lambda s: s["scenarios"][0].update(security_slices=["authority"]))
    source_attack("scenario-holdout-ref-only", lambda s: s["scenarios"][0].update(holdout_ref="holdout-research-21"))

    output = {
        "schema_version": "c21.lifecycle.negative.v2.3", "attack_count": len(rows),
        "passed_count": sum(row["passed"] for row in rows), "escaped_count": sum(not row["passed"] for row in rows),
        "suite_digest": runner.sha256(rows), "attacks": rows,
    }
    (HERE / "v2.3-negative-regression-results.yaml").write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output["suite_digest"])
    if output["escaped_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

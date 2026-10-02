#!/usr/bin/env python3
"""Independent black-box attacks for the C21 v2.3 lifecycle controller.

This file is intentionally outside the author run package.  It never rewrites
the author fixture, authority root, runner, or historical review materials.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


REVIEW = Path(__file__).resolve().parent
RUNS = REVIEW / "runs"
OUTPUT = REVIEW / "v2.3-independent-reproduction-20261001.yaml"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "c21_v23_independent_runner", RUNS / "run-lifecycle-harness.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner()
    raw = json.loads((RUNS / "synthetic-lifecycle-input.yaml").read_text(encoding="utf-8"))
    root = json.loads((RUNS / "frozen-authority-root.yaml").read_text(encoding="utf-8"))
    source = runner.validate(copy.deepcopy(raw), copy.deepcopy(root))
    records: list[dict] = []

    def record(attack_id: str, family: str, expected: str, actual: str, reasons: list[str]) -> None:
        matched = actual == expected if expected == "PASS" else actual in {"FAIL", "SCHEMA_REJECT"}
        records.append(
            {
                "attack_id": attack_id,
                "family": family,
                "expected": expected,
                "actual": actual,
                "matched": matched,
                "reasons": reasons,
            }
        )

    def state_attack(
        attack_id: str,
        family: str,
        mutate,
        *,
        scenario_id: str = "V23-001",
        expected: str = "FAIL",
    ) -> None:
        scenario = next(item for item in source["scenarios"] if item["scenario_id"] == scenario_id)
        state = runner.deep_merge(source["base_state"], scenario["overrides"])
        mutate(state)
        try:
            runner.validate_state(state)
            actual, reasons, _, _ = runner.evaluate(source, state, scenario)
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        record(attack_id, family, expected, actual, reasons)

    def source_attack(attack_id: str, family: str, mutate, *, expected: str = "FAIL") -> None:
        candidate = copy.deepcopy(raw)
        candidate["scenarios"] = [copy.deepcopy(candidate["scenarios"][0])]
        mutate(candidate)
        try:
            checked = runner.validate(candidate, copy.deepcopy(root))
            scenario = checked["scenarios"][0]
            state = runner.deep_merge(checked["base_state"], scenario["overrides"])
            runner.validate_state(state)
            actual, reasons, _, _ = runner.evaluate(checked, state, scenario)
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        record(attack_id, family, expected, actual, reasons)

    def root_attack(attack_id: str, family: str, mutate, *, expected: str = "FAIL") -> None:
        candidate_root = copy.deepcopy(root)
        mutate(candidate_root)
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
        record(attack_id, family, expected, actual, reasons)

    # The independently pinned root must defeat a complete local reseal.
    def reseal_owner(candidate_root: dict) -> None:
        candidate_root["owner_registry"]["technical"]["expires_at"] = "2027-01-01T00:00:00Z"

    root_attack("root-local-reseal-after-owner-change", "pinned-root", reseal_owner)

    # Exercise every field carried by the frozen rollout-plan digest.  Each
    # mutation is locally resealed and the complete authority root is resealed;
    # acceptance would therefore prove the runner trusts a scenario-controlled root.
    plan_mutations = {
        "plan-id": ("plan_id", "rollout-c21-v23-alt"),
        "release-id": ("release_id", "rel-21-alt"),
        "stage": ("stage", "LIMITED"),
        "scope": ("scope", "synthetic-expanded"),
        "scope-digest": ("scope_digest", runner.sha256({"scope": "synthetic-expanded"})),
        "allowed-tenants": ("allowed_tenants", ["tenant-synthetic", "tenant-alt"]),
        "allowed-tasks": ("allowed_tasks", ["research", "publish"]),
        "allowed-actions": ("allowed_actions", ["read", "write_isolated_artifact", "publish"]),
        "candidate-permissions": ("candidate_permissions", ["read", "write_isolated_artifact", "external-admin"]),
        "baseline-permissions": ("baseline_permissions", ["read", "write_isolated_artifact", "external-admin"]),
        "min-trials": ("min_trials", 1),
        "max-trials": ("max_trials", 99),
        "max-cost": ("max_cost", 999.0),
        "starts-at": ("starts_at", "2026-09-30T10:00:00Z"),
        "expires-at": ("expires_at", "2026-09-30T14:00:00Z"),
        "environment-ref": ("environment_ref", "env-restore-isolated-21"),
        "owner": ("owner", "human-technical"),
        "approval-ref": ("approval_ref", "approval-retired-plan-21"),
    }
    for label, (field, value) in plan_mutations.items():
        def mutate_plan(candidate_root: dict, *, field=field, value=value) -> None:
            plan = candidate_root["rollout_plan_registry"]["rollout-c21-v23"]
            plan[field] = copy.deepcopy(value)
            plan["plan_digest"] = runner.record_digest(plan, "plan_digest")

        root_attack(f"plan-field-{label}-locally-resealed", "rollout-plan-fields", mutate_plan)

    def revoke_release_authority(candidate_root: dict) -> None:
        item = candidate_root["authority_registry"]["approval-release-21"]
        item["status"] = "REVOKED"
        item["authority_digest"] = runner.record_digest(item, "authority_digest")

    root_attack("release-authority-revoked-and-root-resealed", "time-revocation", revoke_release_authority)

    def predate_retirement_signoff(candidate_root: dict) -> None:
        item = candidate_root["retirement_evidence_registry"]["ret-signoff-21"]
        item["issued_at"] = "2026-09-30T00:30:00Z"
        item["record_digest"] = runner.record_digest(item, "record_digest")

    root_attack("retirement-signoff-predates-authority-root-resealed", "publication-retirement-order", predate_retirement_signoff)

    # Trial/task/dataset/grader/terminal links are attacked separately, with
    # local record resealing where applicable.
    def change_trial_task(state: dict) -> None:
        state["trial_ledger"][0]["task_id"] = "task-release-write-21"
        state["trial_ledger"][0]["trial_digest"] = runner.record_digest(state["trial_ledger"][0], "trial_digest")

    state_attack("trial-task-link-resealed", "trial-chain", change_trial_task)

    def change_task_input(state: dict) -> None:
        task = state["task_registry"]["task-release-read-21"]
        task["input_digest"] = runner.sha256("substituted-input")
        task["record_digest"] = runner.record_digest(task, "record_digest")

    state_attack("task-input-resealed", "trial-chain", change_task_input)

    def change_dataset_layer(state: dict) -> None:
        dataset = state["dataset_registry"]["dataset-holdout-21"]
        dataset["layer"] = "training"
        dataset["holdout_ref"] = "NONE"
        dataset["record_digest"] = runner.record_digest(dataset, "record_digest")

    state_attack("dataset-layer-resealed", "trial-chain", change_dataset_layer)

    def revoke_grader(state: dict) -> None:
        grader = state["grader_registry"]["blind-grader-c07"]
        grader["status"] = "REVOKED"
        grader["record_digest"] = runner.record_digest(grader, "record_digest")

    state_attack("grader-revoked-resealed", "trial-chain", revoke_grader)

    def change_terminal(state: dict) -> None:
        terminal = state["terminal_registry"]["terminal-canary-1"]
        terminal["status"] = "READY"
        terminal["record_digest"] = runner.record_digest(terminal, "record_digest")

    state_attack("terminal-reset-to-ready-resealed", "trial-chain", change_terminal)

    # Effect authority, execution receipt and independent readback are attacked
    # independently.  An effect's own `authorized` flag is intentionally absent.
    honest_unknown_effect = {
        "effect_id": "effect-unknown",
        "status": "UNKNOWN",
        "external": True,
        "owner": "human-operations",
        "tenant_id": "tenant-synthetic",
        "task_type": "research",
        "action": "read",
        "authority_ref": "effect-authority-unknown",
        "receipt_ref": "effect-receipt-unknown",
        "readback_ref": "effect-readback-unknown",
    }

    state_attack(
        "effect-authority-substitution",
        "effect-chain",
        lambda state: state["runtime_state"].update(
            effect_ledger=[{**honest_unknown_effect, "authority_ref": "approval-release-21"}]
        ),
    )

    def substitute_effect_receipt(state: dict) -> None:
        state["runtime_state"]["effect_ledger"] = [copy.deepcopy(honest_unknown_effect)]
        receipt = state["effect_receipt_registry"]["effect-receipt-unknown"]
        receipt["request_digest"] = runner.sha256("substituted-effect-request")
        receipt["record_digest"] = runner.record_digest(receipt, "record_digest")

    state_attack("effect-receipt-substitution-resealed", "effect-chain", substitute_effect_receipt)

    def collapse_effect_observer(state: dict) -> None:
        state["runtime_state"]["effect_ledger"] = [copy.deepcopy(honest_unknown_effect)]
        readback = state["effect_readback_registry"]["effect-readback-unknown"]
        readback["observer"] = "human-operations"
        readback["record_digest"] = runner.record_digest(readback, "record_digest")

    state_attack("effect-readback-observer-equals-operator", "effect-chain", collapse_effect_observer)

    state_attack(
        "task-uses-schedule-manifest",
        "automation-manifest",
        lambda state: state["runtime_state"]["tasks"][0].update(
            manifest_ref="manifest-cron-synthetic"
        ),
    )

    source_attack(
        "scenario-layer-claims-holdout",
        "scenario-metadata",
        lambda candidate: candidate["scenarios"][0].update(
            layer="holdout", holdout_ref="holdout-research-21"
        ),
    )
    source_attack(
        "scenario-holdout-ref-on-training",
        "scenario-metadata",
        lambda candidate: candidate["scenarios"][0].update(
            holdout_ref="holdout-research-21"
        ),
    )
    source_attack(
        "scenario-self-claims-valid-security-slice",
        "scenario-metadata",
        lambda candidate: candidate["scenarios"][0].update(
            security_slices=["authority"]
        ),
    )

    source_attack(
        "evaluation-time-after-all-authorities-expire",
        "time-revocation",
        lambda candidate: candidate.update(now="2027-01-01T00:00:00Z"),
    )
    state_attack(
        "zero-max-trials",
        "budget",
        lambda state: state["rollout"].update(max_trials=0),
    )
    state_attack(
        "negative-max-cost",
        "budget",
        lambda state: state["rollout"].update(max_cost=-0.01),
    )

    # These two attacks intentionally probe an ordering relation not represented
    # by a publication/retirement event receipt.  A PASS is a real escape and is
    # retained in the report rather than normalized away.
    state_attack(
        "legal-review-completes-after-rollout-window-start",
        "publication-retirement-order",
        lambda state: state["legal_review"].update(reviewed_at="2026-09-30T11:30:00Z"),
    )
    state_attack(
        "legal-review-completes-after-retirement-window-start",
        "publication-retirement-order",
        lambda state: state["legal_review"].update(reviewed_at="2026-09-30T11:30:00Z"),
        scenario_id="V23-039",
    )

    report = {
        "schema_version": "c21.lifecycle.independent-negative.v2.3",
        "review_role": "non_author",
        "environment": "offline_synthetic",
        "author_files_modified": False,
        "attack_count": len(records),
        "matched_count": sum(item["matched"] for item in records),
        "escape_count": sum(not item["matched"] for item in records),
        "suite_digest": runner.sha256(records),
        "attacks": records,
        "limits": {
            "representative_real_world_executed": False,
            "real_openclaw_executed": False,
            "real_hermes_executed": False,
            "production_release_or_retirement_executed": False,
            "practice_gate": "REVIEW_REQUIRED",
            "editor_gate": "NOT_AUTHORIZED",
            "chief_gate": "NOT_AUTHORIZED",
            "release_candidate": "NOT_AUTHORIZED",
        },
    }
    OUTPUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: report[key] for key in ("attack_count", "matched_count", "escape_count", "suite_digest")}, ensure_ascii=False))


if __name__ == "__main__":
    main()

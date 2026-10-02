#!/usr/bin/env python3
"""Non-author near-neighbor attacks for the C22 v2.1 camp harness."""

from __future__ import annotations

import copy
import importlib.util
import json
from datetime import datetime
from pathlib import Path


RUNS = Path(__file__).resolve().parent / "runs"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "c22_v21_independent_runner", RUNS / "run-training-camp-harness.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner()
    document = json.loads((RUNS / "synthetic-camp-input.yaml").read_text())
    positive = next(
        trial
        for trial in document["trials"]
        if runner.decide(
            trial,
            datetime.fromisoformat(document["generated_at"].replace("Z", "+00:00")),
        )[0]
        == "PASS"
    )
    now = datetime.fromisoformat(document["generated_at"].replace("Z", "+00:00"))
    records = []

    def attack(attack_id, mutate, expected="FAIL"):
        trial = copy.deepcopy(positive)
        mutate(trial)
        actual, reasons, _ = runner.decide(trial, now)
        records.append(
            {
                "id": attack_id,
                "expected": expected,
                "actual": actual,
                "matched": actual == expected,
                "reasons": reasons,
            }
        )

    def expire_camp(trial):
        trial["raw_state"]["camp"]["ends_at"] = "2026-09-29T23:59:59Z"
        runner.seal(trial["raw_state"]["camp"])

    attack("camp_expired_before_evaluation", expire_camp)

    def expire_graduation(trial):
        record = trial["raw_state"]["graduation_record"]
        record["expires_at"] = "2026-09-30T11:45:00Z"
        runner.seal(record)

    attack("expired_graduation_record_still_recommends_limited_duty", expire_graduation)

    def revoke_pass_evidence(trial):
        state = trial["raw_state"]
        ref = state["d21_refs"]["technical"]
        record = next(item for item in state["evidence_registry"] if item["evidence_id"] == ref)
        record["revoked_at"] = "2026-09-30T11:00:00Z"
        runner.seal(record)

    attack("revoked_at_evidence_keeps_pass_status", revoke_pass_evidence)
    attack("stop_issuer_and_observer_are_same_principal", lambda trial: None)

    def fake_sandbox(trial):
        state = trial["raw_state"]
        runtime = state["runtime"]
        runtime["sandbox_mode"] = "marketing-isolation"
        runtime["sandbox_backend"] = "truthy-without-isolation"
        runner.seal(runtime)
        state["baseline"]["release_digest"] = runtime["digest"]
        runner.seal(state["baseline"])
        state["restore_proof"]["target_runtime_digest"] = runtime["digest"]
        runner.seal(state["restore_proof"])
        runtime_recovery = next(
            item for item in state["recovery_registry"] if item["kind"] == "RUNTIME"
        )
        runtime_recovery["content_digest"] = runtime["digest"]
        runner.seal(runtime_recovery)

    attack("arbitrary_truthy_sandbox_mode_and_backend", fake_sandbox)

    def empty_authority_scope(trial):
        state = trial["raw_state"]
        authority = state["authority"]
        authority["scope"] = []
        authority["approved_digest"] = "sha256:" + runner.hashlib.sha256(
            runner.canon(
                {
                    "subject": state["camp"]["subject"],
                    "camp_id": state["camp"]["camp_id"],
                    "runtime_id": state["runtime"]["runtime_id"],
                    "eval_id": state["eval_spec"]["eval_id"],
                    "scope": [],
                }
            ).encode()
        ).hexdigest()
        runner.seal(authority)

    attack("empty_authority_scope_self_resealed", empty_authority_scope)

    def expand_budget(trial):
        camp = trial["raw_state"]["camp"]
        camp["budget_total"] = 1_000_000_000.0
        runner.seal(camp)

    attack("camp_budget_expanded_without_authority_binding", expand_budget)

    def revoke_holdout(trial):
        dataset = next(
            item for item in trial["raw_state"]["datasets"] if item["layer"] == "holdout"
        )
        dataset["status"] = "REVOKED"
        runner.seal(dataset)

    attack("revoked_holdout_dataset_still_counts", revoke_holdout)

    def orphan_regression_parent(trial):
        dataset = next(
            item for item in trial["raw_state"]["datasets"] if item["layer"] == "regression"
        )
        dataset["parent_dataset_id"] = "DATASET-NOT-REGISTERED"
        lineage = {
            "dataset_id": dataset["dataset_id"],
            "layer": dataset["layer"],
            "parent_dataset_id": dataset["parent_dataset_id"],
            "version": dataset["version"],
            "source_digest": dataset["source_digest"],
        }
        dataset["lineage_digest"] = "sha256:" + runner.hashlib.sha256(
            runner.canon(lineage).encode()
        ).hexdigest()
        runner.seal(dataset)

    attack("unregistered_parent_dataset_accepted", orphan_regression_parent)

    attack(
        "six_cost_categories_all_zero",
        lambda trial: [entry.update(amount=0.0) for entry in trial["raw_state"]["cost_ledger"]],
    )

    def reuse_security_evidence_per_gate(trial):
        state = trial["raw_state"]
        first_by_gate = {}
        for item in state["security_matrix"]:
            first_by_gate.setdefault(item["gate"], item["evidence_ref"])
        state["security_evidence_refs"] = [
            first_by_gate[item["gate"]] for item in state["security_matrix"]
        ]
        for item in state["security_matrix"]:
            item["evidence_ref"] = first_by_gate[item["gate"]]

    attack("one_security_evidence_reused_for_four_slices_at_each_gate", reuse_security_evidence_per_gate)

    attack(
        "outer_trial_layer_relabelled_without_raw_state_change",
        lambda trial: trial.update(layer="holdout"),
    )

    def apply_internal_effect_while_stop_readback_says_clear(trial):
        effect = trial["raw_state"]["effect_ledger"][0]
        effect["status"] = "APPLIED"
        runner.seal(effect)

    attack(
        "internal_effect_applied_but_stop_readback_effects_clear",
        apply_internal_effect_while_stop_readback_says_clear,
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

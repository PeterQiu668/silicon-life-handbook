#!/usr/bin/env python3
"""Non-author near-neighbor attacks for the C22 v2.2 camp harness."""

from __future__ import annotations

import copy
import importlib.util
import json
from datetime import datetime
from pathlib import Path


RUNS = Path(__file__).resolve().parent / "runs"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "c22_v22_independent_runner", RUNS / "run-training-camp-harness.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner()
    document = json.loads((RUNS / "synthetic-camp-input.yaml").read_text())
    authority = json.loads((RUNS / "frozen-camp-authority.yaml").read_text())
    now = datetime.fromisoformat(document["generated_at"].replace("Z", "+00:00"))
    positive = next(
        trial
        for trial in document["trials"]
        if runner.decide(trial, now, authority)[0] == "PASS"
    )
    records: list[dict[str, object]] = []

    def attack(attack_id, mutate, expected="FAIL"):
        trial = copy.deepcopy(positive)
        local_authority = copy.deepcopy(authority)
        mutate(trial, local_authority)
        # Mirror the public CLI boundary: an externally supplied authority bundle
        # must pass root validation before it may reach the decision function.
        try:
            validated_authority = runner.validate_authority_bundle(local_authority)
            actual, reasons, _ = runner.decide(trial, now, validated_authority)
        except runner.ContractError as exc:
            actual, reasons = "FAIL", [str(exc)]
        records.append(
            {
                "id": attack_id,
                "expected": expected,
                "actual": actual,
                "matched": actual == expected,
                "reasons": reasons,
            }
        )

    def same_stop_actor(trial, _authority):
        state = trial["raw_state"]
        state["stop_readback"]["observer"] = state["stop_receipt"]["issuer"]
        runner.seal(state["stop_readback"])

    attack("stop_issuer_equals_readback_observer", same_stop_actor)

    def revoke_security_principal(trial, _authority):
        principal = next(
            item
            for item in trial["raw_state"]["principals"]
            if item["principal_id"].startswith("PR-SECURITY-")
        )
        principal["status"] = "REVOKED"
        runner.seal(principal)

    attack("security_authority_principal_revoked_and_resealed", revoke_security_principal)

    def collide_alias(trial, _authority):
        principals = trial["raw_state"]["principals"]
        principals[1]["aliases"] = list(principals[0]["aliases"])
        runner.seal(principals[1])

    attack("principal_alias_collision_resealed", collide_alias)

    def alter_task_owner(trial, _authority):
        record = trial["raw_state"]["task_registry"][0]
        record["owner"] = trial["raw_state"]["owners"]["evaluator"]
        runner.seal(record)

    attack("task_owner_swapped_to_evaluator", alter_task_owner)

    def alter_trial_grader(trial, _authority):
        record = trial["raw_state"]["trial_registry"][0]
        record["grader_version"] = "grader-unregistered"
        runner.seal(record)

    attack("trial_grader_not_bound_to_eval_spec", alter_trial_grader)

    def future_stop_receipt(trial, _authority):
        receipt = trial["raw_state"]["stop_receipt"]
        receipt["created_at"] = "2026-10-02T00:00:00Z"
        runner.seal(receipt)

    attack("stop_receipt_from_future", future_stop_receipt)

    def self_certify_graduation(trial, _authority):
        graduation = trial["raw_state"]["graduation_record"]
        graduation["certification"] = True
        runner.seal(graduation)

    attack("graduation_recommendation_self_claims_certification", self_certify_graduation)

    def external_effect_applied(trial, _authority):
        effect = trial["raw_state"]["effect_ledger"][0]
        effect["external"] = True
        effect["status"] = "APPLIED"
        runner.seal(effect)

    attack("offline_camp_applies_external_effect", external_effect_applied)

    def cycle_dataset_lineage(trial, _authority):
        state = trial["raw_state"]
        training = next(item for item in state["datasets"] if item["layer"] == "training")
        holdout = next(item for item in state["datasets"] if item["layer"] == "holdout")
        training["parent_dataset_id"] = holdout["dataset_id"]
        training["lineage_digest"] = "sha256:" + runner.hashlib.sha256(
            runner.canon(
                {
                    "dataset_id": training["dataset_id"],
                    "layer": training["layer"],
                    "parent_dataset_id": training["parent_dataset_id"],
                    "version": training["version"],
                    "source_digest": training["source_digest"],
                }
            ).encode()
        ).hexdigest()
        runner.seal(training)

    attack("dataset_lineage_cycle_resealed", cycle_dataset_lineage)

    def negative_cost(trial, _authority):
        entry = trial["raw_state"]["cost_ledger"][0]
        entry["amount"] = -1.0
        runner.seal(entry)

    attack("negative_cost_amount", negative_cost)

    def remove_security_gate_slice(trial, _authority):
        state = trial["raw_state"]
        removed = state["security_matrix"].pop()
        state["security_evidence_refs"].remove(removed["evidence_ref"])

    attack("security_slice_gate_missing", remove_security_gate_slice)

    def tamper_and_reseal_authority_root(_trial, local_authority):
        camp_id = positive["raw_state"]["camp"]["camp_id"]
        local_authority["camps"][camp_id]["approved_budget"] = 999999.0
        payload = {key: value for key, value in local_authority.items() if key != "root_digest"}
        local_authority["root_digest"] = "sha256:" + runner.hashlib.sha256(
            runner.canon(payload).encode()
        ).hexdigest()

    attack("authority_root_tampered_and_self_resealed", tamper_and_reseal_authority_root)

    report = {
        "review": "C22-v2.2-independent-near-neighbor",
        "tested_at": document["generated_at"],
        "source_scenario": positive["scenario_id"],
        "attack_count": len(records),
        "matched_count": sum(bool(record["matched"]) for record in records),
        "fail_open_count": sum(not bool(record["matched"]) for record in records),
        "attacks": records,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["fail_open_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

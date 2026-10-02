#!/usr/bin/env python3
"""Non-author near-neighbor attacks for the C21 v2.1 lifecycle harness."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


RUNS = Path(__file__).resolve().parent / "runs"


def load_runner():
    spec = importlib.util.spec_from_file_location("c21_independent_runner", RUNS / "run-lifecycle-harness.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner()
    source = json.loads((RUNS / "synthetic-lifecycle-input.yaml").read_text())
    records = []

    def attack(attack_id, mutate, expected="FAIL"):
        state = copy.deepcopy(source["base_state"])
        mutate(state)
        try:
            runner.validate_state(state)
            actual, reasons, _, _ = runner.evaluate(source, state)
        except (TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        records.append({"id": attack_id, "expected": expected, "actual": actual, "matched": actual == expected, "reasons": reasons})

    def self_attested_technical_owner(state):
        state["owner_registry"]["technical"]["principal"] = "agent-self"
        state["migration"]["owner"] = "agent-self"
        state["migration"]["migration_digest"] = runner.record_digest(state["migration"], "migration_digest")
        receipt = state["migration_receipt_registry"][state["migration"]["receipt_ref"]]
        receipt.update(owner="agent-self", migration_digest=state["migration"]["migration_digest"])
        receipt["record_digest"] = runner.record_digest(receipt, "record_digest")
        state["restore"]["owner"] = "agent-self"
        proof = state["restore_proof_registry"][state["restore"]["proof_ref"]]
        proof["owner"] = "agent-self"
        proof["proof_digest"] = runner.record_digest(proof, "proof_digest")
        evidence = state["d21_evidence_registry"]["d21-technical-21"]
        evidence["owner"] = "agent-self"
        evidence["record_digest"] = runner.record_digest(evidence, "record_digest")

    attack("self_attested_agent_as_human_technical_owner", self_attested_technical_owner)
    attack("offline_fixture_claims_production_stage", lambda s: s["rollout"].update(stage="PRODUCTION"))
    attack("empty_rollout_tenant_task_action_scope", lambda s: s["rollout"].update(allowed_tenants=[], allowed_tasks=[], allowed_actions=[]))
    attack("unauthorized_internal_effect_applied", lambda s: s["runtime_state"]["effect_ledger"].append({"effect_id":"effect-independent","status":"APPLIED","authorized":False,"external":False,"readback":"CONFIRMED"}))
    attack("paused_stage_with_open_admission", lambda s: s["rollout"].update(stage="PAUSED"))
    attack("runtime_task_unknown_owner", lambda s: s["runtime_state"]["tasks"][0].update(owner="agent-self"))
    attack("legal_review_unbounded_region_scope", lambda s: s["legal_review"].update(data_region="unknown-jurisdiction", scope="all-data"))

    def restore_proof_self_claims_production(state):
        proof = state["restore_proof_registry"][state["restore"]["proof_ref"]]
        proof["environment"] = "production-without-manifest"
        proof["proof_digest"] = runner.record_digest(proof, "proof_digest")
    attack("restore_proof_unregistered_environment", restore_proof_self_claims_production)

    def contradictory_rollback(state):
        state["rollback"].update(requested=True, status="ROLLED_BACK", code_config_reverted=True, old_runtime_reads_current_schema=True, receipt_ref="rollback-receipt-21")
    attack("rollback_receipt_target_not_runtime_active_release", contradictory_rollback)

    relabeled = copy.deepcopy(source)
    relabeled["scenarios"] = [copy.deepcopy(relabeled["scenarios"][0])]
    relabeled["scenarios"][0]["layer"] = "holdout"
    runner.validate(relabeled)
    state = runner.deep_merge(relabeled["base_state"], relabeled["scenarios"][0]["overrides"])
    actual, reasons, _, _ = runner.evaluate(relabeled, state)
    records.append({
        "id": "holdout_label_without_holdout_lineage",
        "expected": "FAIL",
        "actual": actual,
        "matched": actual == "FAIL",
        "reasons": reasons or ["layer accepted without holdout manifest, isolation, grader or contamination record"],
    })

    print(json.dumps({
        "attack_count": len(records),
        "matched_count": sum(record["matched"] for record in records),
        "fail_open_count": sum(not record["matched"] for record in records),
        "attacks": records,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

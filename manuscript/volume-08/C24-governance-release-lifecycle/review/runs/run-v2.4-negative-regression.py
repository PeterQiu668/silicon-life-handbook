#!/usr/bin/env python3
"""Author-side v2.4 regression: replay the historical 38 attacks plus event-chain attacks."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_runner():
    spec = importlib.util.spec_from_file_location("c21_v24_runner", HERE / "run-lifecycle-harness.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner()
    raw = json.loads((HERE / "synthetic-lifecycle-input.yaml").read_text(encoding="utf-8"))
    root = json.loads((HERE / "frozen-authority-root.yaml").read_text(encoding="utf-8"))
    source = runner.validate(copy.deepcopy(raw), copy.deepcopy(root))
    rows: list[dict] = []

    def record(attack_id: str, family: str, actual: str, reasons: list[str], required_reason: str | None = None) -> None:
        passed = actual in {"FAIL", "SCHEMA_REJECT"} and (required_reason is None or required_reason in reasons)
        rows.append({"attack_id": attack_id, "family": family, "expected": "FAIL", "actual": actual, "required_reason": required_reason or "ANY_HARD_REJECTION", "passed": passed, "reasons": reasons})

    def state_attack(attack_id: str, family: str, mutate, scenario_id: str = "V24-001", required_reason: str | None = None) -> None:
        scenario = next(item for item in source["scenarios"] if item["scenario_id"] == scenario_id)
        state = runner.deep_merge(source["base_state"], scenario["overrides"])
        mutate(state)
        try:
            runner.validate_state(state)
            actual, reasons, _, _ = runner.evaluate(source, state, scenario)
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        record(attack_id, family, actual, reasons, required_reason)

    def source_attack(attack_id: str, family: str, mutate, required_reason: str | None = None) -> None:
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
        record(attack_id, family, actual, reasons, required_reason)

    def root_attack(attack_id: str, family: str, mutate) -> None:
        candidate_root = copy.deepcopy(root)
        mutate(candidate_root)
        candidate_root["root_digest"] = runner.sha256({key: candidate_root[key] for key in sorted(runner.FROZEN_REGISTRIES)})
        candidate = copy.deepcopy(raw)
        candidate["authority_root_digest"] = candidate_root["root_digest"]
        for key in runner.FROZEN_REGISTRIES:
            candidate["base_state"][key] = copy.deepcopy(candidate_root[key])
        try:
            runner.validate(candidate, candidate_root)
            actual, reasons = "PASS", []
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        record(attack_id, family, actual, reasons)

    # Historical non-author v2.3 suite, ported without weakening its 38 attacks.
    root_attack("root-local-reseal-after-owner-change", "historical-pinned-root", lambda r: r["owner_registry"]["technical"].update(expires_at="2027-01-01T00:00:00Z"))
    plan_mutations = {
        "plan-id": ("plan_id", "rollout-c21-v24-alt"), "release-id": ("release_id", "rel-21-alt"), "stage": ("stage", "LIMITED"),
        "scope": ("scope", "synthetic-expanded"), "scope-digest": ("scope_digest", runner.sha256({"scope": "synthetic-expanded"})),
        "allowed-tenants": ("allowed_tenants", ["tenant-synthetic", "tenant-alt"]), "allowed-tasks": ("allowed_tasks", ["research", "publish"]),
        "allowed-actions": ("allowed_actions", ["read", "write_isolated_artifact", "publish"]),
        "candidate-permissions": ("candidate_permissions", ["read", "write_isolated_artifact", "external-admin"]),
        "baseline-permissions": ("baseline_permissions", ["read", "write_isolated_artifact", "external-admin"]),
        "min-trials": ("min_trials", 1), "max-trials": ("max_trials", 99), "max-cost": ("max_cost", 999.0),
        "starts-at": ("starts_at", "2026-09-30T10:00:00Z"), "expires-at": ("expires_at", "2026-09-30T14:00:00Z"),
        "environment-ref": ("environment_ref", "env-restore-isolated-21"), "owner": ("owner", "human-technical"),
        "approval-ref": ("approval_ref", "approval-retired-plan-21"),
    }
    for label, (field, value) in plan_mutations.items():
        def mutate_plan(candidate_root: dict, field=field, value=value) -> None:
            plan = candidate_root["rollout_plan_registry"]["rollout-c21-v24"]
            plan[field] = copy.deepcopy(value)
            plan["plan_digest"] = runner.record_digest(plan, "plan_digest")
        root_attack(f"plan-field-{label}-locally-resealed", "historical-rollout-plan-fields", mutate_plan)

    def revoke_release_authority(candidate_root: dict) -> None:
        item = candidate_root["authority_registry"]["approval-release-21"]
        item["status"] = "REVOKED"; item["authority_digest"] = runner.record_digest(item, "authority_digest")
    root_attack("release-authority-revoked-and-root-resealed", "historical-time-revocation", revoke_release_authority)

    def predate_signoff(candidate_root: dict) -> None:
        item = candidate_root["retirement_evidence_registry"]["ret-signoff-21"]
        item["issued_at"] = "2026-09-30T00:30:00Z"; item["record_digest"] = runner.record_digest(item, "record_digest")
    root_attack("retirement-signoff-predates-authority-root-resealed", "historical-publication-retirement-order", predate_signoff)

    def trial_task(state: dict) -> None:
        state["trial_ledger"][0]["task_id"] = "task-release-write-21"; state["trial_ledger"][0]["trial_digest"] = runner.record_digest(state["trial_ledger"][0], "trial_digest")
    state_attack("trial-task-link-resealed", "historical-trial-chain", trial_task)
    def task_input(state: dict) -> None:
        item = state["task_registry"]["task-release-read-21"]; item["input_digest"] = runner.sha256("substituted-input"); item["record_digest"] = runner.record_digest(item, "record_digest")
    state_attack("task-input-resealed", "historical-trial-chain", task_input)
    def dataset_layer(state: dict) -> None:
        item = state["dataset_registry"]["dataset-holdout-21"]; item.update(layer="training", holdout_ref="NONE"); item["record_digest"] = runner.record_digest(item, "record_digest")
    state_attack("dataset-layer-resealed", "historical-trial-chain", dataset_layer)
    def revoke_grader(state: dict) -> None:
        item = state["grader_registry"]["blind-grader-c07"]; item["status"] = "REVOKED"; item["record_digest"] = runner.record_digest(item, "record_digest")
    state_attack("grader-revoked-resealed", "historical-trial-chain", revoke_grader)
    def reset_terminal(state: dict) -> None:
        item = state["terminal_registry"]["terminal-canary-1"]; item["status"] = "READY"; item["record_digest"] = runner.record_digest(item, "record_digest")
    state_attack("terminal-reset-to-ready-resealed", "historical-trial-chain", reset_terminal)

    unknown_effect = {"effect_id": "effect-unknown", "status": "UNKNOWN", "external": True, "owner": "human-operations", "tenant_id": "tenant-synthetic", "task_type": "research", "action": "read", "authority_ref": "effect-authority-unknown", "receipt_ref": "effect-receipt-unknown", "readback_ref": "effect-readback-unknown"}
    state_attack("effect-authority-substitution", "historical-effect-chain", lambda s: s["runtime_state"].update(effect_ledger=[{**unknown_effect, "authority_ref": "approval-release-21"}]))
    def effect_receipt(state: dict) -> None:
        state["runtime_state"]["effect_ledger"] = [copy.deepcopy(unknown_effect)]; item = state["effect_receipt_registry"]["effect-receipt-unknown"]; item["request_digest"] = runner.sha256("substituted-effect-request"); item["record_digest"] = runner.record_digest(item, "record_digest")
    state_attack("effect-receipt-substitution-resealed", "historical-effect-chain", effect_receipt)
    def effect_observer(state: dict) -> None:
        state["runtime_state"]["effect_ledger"] = [copy.deepcopy(unknown_effect)]; item = state["effect_readback_registry"]["effect-readback-unknown"]; item["observer"] = "human-operations"; item["record_digest"] = runner.record_digest(item, "record_digest")
    state_attack("effect-readback-observer-equals-operator", "historical-effect-chain", effect_observer)
    state_attack("task-uses-schedule-manifest", "historical-automation-manifest", lambda s: s["runtime_state"]["tasks"][0].update(manifest_ref="manifest-cron-synthetic"))
    source_attack("scenario-layer-claims-holdout", "historical-scenario-metadata", lambda s: s["scenarios"][0].update(layer="holdout", holdout_ref="holdout-research-21"))
    source_attack("scenario-holdout-ref-on-training", "historical-scenario-metadata", lambda s: s["scenarios"][0].update(holdout_ref="holdout-research-21"))
    source_attack("scenario-self-claims-valid-security-slice", "historical-scenario-metadata", lambda s: s["scenarios"][0].update(security_slices=["authority"]))
    source_attack("evaluation-time-after-all-authorities-expire", "historical-time-revocation", lambda s: s.update(now="2027-01-01T00:00:00Z"))
    state_attack("zero-max-trials", "historical-budget", lambda s: s["rollout"].update(max_trials=0))
    state_attack("negative-max-cost", "historical-budget", lambda s: s["rollout"].update(max_cost=-0.01))
    state_attack("legal-review-completes-after-rollout-window-start", "historical-publication-retirement-order", lambda s: s["legal_review"].update(reviewed_at="2026-09-30T11:30:00Z"), required_reason="PUBLICATION_EVENT_SEQUENCE_INVALID")
    state_attack("legal-review-completes-after-retirement-window-start", "historical-publication-retirement-order", lambda s: s["legal_review"].update(reviewed_at="2026-09-30T11:30:00Z"), scenario_id="V24-039", required_reason="PUBLICATION_EVENT_SEQUENCE_INVALID")

    # v2.4 event-chain attacks: each must trip a semantic reason, not only the frozen-root guard.
    def reseal_event(state: dict, registry: str, event_id: str) -> dict:
        event = state[registry][event_id]; event["record_digest"] = runner.record_digest(event, "record_digest"); return event
    def publication_receipt_time(state: dict) -> None:
        event = state["publication_event_registry"]["publication-release-21"]; event["receipt"]["executed_at"] = "2026-09-30T11:19:00Z"; event["receipt"]["record_digest"] = runner.record_digest(event["receipt"], "record_digest"); reseal_event(state, "publication_event_registry", "publication-release-21")
    state_attack("publication-receipt-does-not-match-execution", "v2.4-publication", publication_receipt_time, required_reason="PUBLICATION_EVENT_BINDING_INVALID")
    def publication_readback_order(state: dict) -> None:
        event = state["publication_event_registry"]["publication-release-21"]; event["readback"]["observed_at"] = "2026-09-30T11:19:00Z"; event["readback"]["record_digest"] = runner.record_digest(event["readback"], "record_digest"); reseal_event(state, "publication_event_registry", "publication-release-21")
    state_attack("publication-readback-before-receipt", "v2.4-publication", publication_readback_order, required_reason="PUBLICATION_EVENT_SEQUENCE_INVALID")
    def publication_wrong_subject(state: dict) -> None:
        event = state["publication_event_registry"]["publication-release-21"]; event["receipt"]["subject_id"] = "rel-other"; event["receipt"]["record_digest"] = runner.record_digest(event["receipt"], "record_digest"); reseal_event(state, "publication_event_registry", "publication-release-21")
    state_attack("publication-receipt-wrong-subject", "v2.4-publication", publication_wrong_subject, required_reason="PUBLICATION_EVENT_BINDING_INVALID")
    def publication_revoked(state: dict) -> None:
        item = state["authority_registry"]["approval-release-21"]; item["expires_at"] = "2026-09-30T11:19:59Z"; item["authority_digest"] = runner.record_digest(item, "authority_digest")
    state_attack("publication-executes-after-approval-expiry", "v2.4-publication", publication_revoked, required_reason="PUBLICATION_RELEASE_AUTHORITY_INVALID")
    def publication_uses_window_start(state: dict) -> None:
        event = state["publication_event_registry"]["publication-release-21"]; event["executed_at"] = state["rollout"]["starts_at"]; reseal_event(state, "publication_event_registry", "publication-release-21")
    state_attack("publication-window-start-cannot-replace-receipt-time", "v2.4-publication", publication_uses_window_start, required_reason="PUBLICATION_EVENT_BINDING_INVALID")

    def lifecycle_mutation(state: dict, change) -> None:
        event = state["lifecycle_event_registry"]["retirement-lifecycle-21"]; change(event); event["record_digest"] = runner.record_digest(event, "record_digest")
    state_attack("retirement-signoff-before-request", "v2.4-retirement", lambda s: (s["retirement_evidence_registry"]["ret-signoff-21"].update(issued_at="2026-09-30T11:21:00Z"), s["retirement_evidence_registry"]["ret-signoff-21"].update(record_digest=runner.record_digest(s["retirement_evidence_registry"]["ret-signoff-21"], "record_digest"))), scenario_id="V24-039", required_reason="RETIREMENT_SIGNOFF_INVALID")
    state_attack("retirement-signoff-before-residual-scan", "v2.4-retirement", lambda s: (s["retirement_evidence_registry"]["ret-signoff-21"].update(issued_at="2026-09-30T11:55:00Z"), s["retirement_evidence_registry"]["ret-signoff-21"].update(record_digest=runner.record_digest(s["retirement_evidence_registry"]["ret-signoff-21"], "record_digest"))), scenario_id="V24-039", required_reason="RETIREMENT_SIGNOFF_BEFORE_RESIDUAL_SCAN")
    def retirement_expired(state: dict) -> None:
        item = state["authority_registry"]["approval-retirement-21"]; item["expires_at"] = "2026-09-30T11:29:59Z"; item["authority_digest"] = runner.record_digest(item, "authority_digest")
    state_attack("retirement-executes-after-authority-expiry", "v2.4-retirement", retirement_expired, scenario_id="V24-039", required_reason="RETIREMENT_AUTHORITY_INVALID")
    state_attack("retirement-receipt-wrong-subject", "v2.4-retirement", lambda s: lifecycle_mutation(s, lambda e: (e["receipt"].update(subject_id="retirement-other"), e["receipt"].update(record_digest=runner.record_digest(e["receipt"], "record_digest")))), scenario_id="V24-039", required_reason="RETIREMENT_LIFECYCLE_BINDING_INVALID")
    state_attack("retirement-readback-before-receipt", "v2.4-retirement", lambda s: lifecycle_mutation(s, lambda e: (e["readback"].update(observed_at="2026-09-30T11:29:00Z"), e["readback"].update(record_digest=runner.record_digest(e["readback"], "record_digest")))), scenario_id="V24-039", required_reason="RETIREMENT_LIFECYCLE_SEQUENCE_INVALID")
    state_attack("retirement-wrong-release", "v2.4-retirement", lambda s: lifecycle_mutation(s, lambda e: e.update(release_id="rel-other")), scenario_id="V24-039", required_reason="RETIREMENT_LIFECYCLE_BINDING_INVALID")
    state_attack("retirement-evidence-before-execution", "v2.4-retirement", lambda s: (s["retirement_evidence_registry"]["ret-admission-21"].update(issued_at="2026-09-30T11:29:00Z"), s["retirement_evidence_registry"]["ret-admission-21"].update(record_digest=runner.record_digest(s["retirement_evidence_registry"]["ret-admission-21"], "record_digest"))), scenario_id="V24-039", required_reason="RETIREMENT_ADMISSION_STOPPED_INVALID")

    historical = [row for row in rows if row["family"].startswith("historical-")]
    additions = [row for row in rows if row["family"].startswith("v2.4-")]
    output = {
        "schema_version": "c21.lifecycle.negative.v2.4", "attack_count": len(rows), "passed_count": sum(row["passed"] for row in rows),
        "escaped_count": sum(not row["passed"] for row in rows), "historical_v2_3_attack_count": len(historical),
        "historical_v2_3_passed_count": sum(row["passed"] for row in historical), "v2_4_event_attack_count": len(additions),
        "v2_4_event_passed_count": sum(row["passed"] for row in additions), "suite_digest": runner.sha256(rows), "attacks": rows,
    }
    (HERE / "v2.4-negative-regression-results.yaml").write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: output[key] for key in ("attack_count", "passed_count", "escaped_count", "historical_v2_3_attack_count", "historical_v2_3_passed_count", "suite_digest")}, ensure_ascii=False))
    if output["escaped_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

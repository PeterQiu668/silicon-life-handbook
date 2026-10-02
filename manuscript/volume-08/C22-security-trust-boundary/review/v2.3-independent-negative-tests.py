#!/usr/bin/env python3
"""Final non-author attacks for the C19 v2.3 offline security controller.

The author runtime package is read-only.  Differential attacks against an
already-failing effect scenario require a new, attack-specific hard-failure
signal; an unrelated baseline FAIL never counts as interception.
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
        "c19_v23_final_independent_runner", RUNS / "run-security-harness.py"
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
    records: list[dict] = []

    def add(
        attack_id: str,
        family: str,
        actual: str,
        reasons: list[str],
        *,
        expected: str = "FAIL",
        required_reason: str | None = None,
        baseline_reasons: list[str] | None = None,
    ) -> None:
        if required_reason is None:
            matched = actual in {"FAIL", "SCHEMA_REJECT"}
        else:
            matched = required_reason in reasons
        row = {
            "attack_id": attack_id,
            "family": family,
            "expected": expected,
            "actual": actual,
            "matched": matched,
            "reasons": sorted(set(reasons)),
        }
        if required_reason is not None:
            row["required_reason"] = required_reason
            row["baseline_reasons"] = sorted(set(baseline_reasons or []))
            row["new_reasons"] = sorted(set(reasons) - set(baseline_reasons or []))
        records.append(row)

    def state_attack(attack_id: str, family: str, mutate, *, scenario_id: str = "S01") -> None:
        scenario = copy.deepcopy(next(item for item in source["scenarios"] if item["id"] == scenario_id))
        mutate(scenario["state"])
        try:
            runner.validate_state(scenario["state"], f"attack.{attack_id}")
            actual, hard, review, _ = runner.evaluate(scenario, source, authority)
            reasons = [*hard, *review]
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        add(attack_id, family, actual, reasons)

    def source_attack(attack_id: str, family: str, mutate) -> None:
        candidate = copy.deepcopy(raw)
        mutate(candidate)
        try:
            checked = runner.validate_source(candidate, authority)
            result = runner.build_result(checked, authority)
            row = next(item for item in result["trials"] if item["scenario_id"] == "S01")
            actual, reasons = row["decision"], row["reasons"]
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        add(attack_id, family, actual, reasons)

    def root_attack(attack_id: str, family: str, mutate) -> None:
        candidate = copy.deepcopy(raw_authority)
        mutate(candidate)
        candidate["root_digest"] = runner.digest(
            {key: value for key, value in candidate.items() if key != "root_digest"}
        )
        try:
            runner.validate_authority_bundle(candidate)
            actual, reasons = "PASS", []
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        add(attack_id, family, actual, reasons)

    def differential_effect_attack(
        attack_id: str,
        mutate,
        required_reason: str,
    ) -> None:
        scenario = copy.deepcopy(next(item for item in source["scenarios"] if item["id"] == "S16"))
        baseline_actual, baseline_hard, baseline_review, _ = runner.evaluate(scenario, source, authority)
        assert baseline_actual == "FAIL"
        mutate(scenario["state"])
        try:
            runner.validate_state(scenario["state"], f"attack.{attack_id}")
            actual, hard, review, _ = runner.evaluate(scenario, source, authority)
            reasons = [*hard, *review]
        except (KeyError, TypeError, ValueError) as exc:
            actual, reasons = "SCHEMA_REJECT", [str(exc)]
        add(
            attack_id,
            "effect-receipt-readback",
            actual,
            reasons,
            required_reason=required_reason,
            baseline_reasons=[*baseline_hard, *baseline_review],
        )

    # Frozen authority/session/test/evidence/audit registries: mutate, locally
    # reseal the complete bundle, and verify that the independently pinned root
    # still rejects it.
    root_attack(
        "principal-alias-root-resealed",
        "authority-root",
        lambda item: item["registries"]["principals"].update(
            {"principal-agent-a-alias": copy.deepcopy(item["registries"]["principals"]["principal-agent-a"])}
        ),
    )
    root_attack(
        "session-revoked-root-resealed",
        "session-root",
        lambda item: item["registries"]["sessions"]["session-a"].update(status="REVOKED"),
    )
    root_attack(
        "test-definition-revoked-root-resealed",
        "test-evidence-root",
        lambda item: item["registries"]["test_definitions"]["S01"].update(status="REVOKED"),
    )
    root_attack(
        "test-evidence-content-resealed",
        "test-evidence-root",
        lambda item: item["registries"]["test_evidence"]["test-evidence-s01"].update(
            content_digest=runner.digest("substituted-test-evidence")
        ),
    )
    root_attack(
        "audit-anchor-self-signed-root-resealed",
        "audit-root",
        lambda item: item["registries"]["audit_anchors"]["audit-C19-v2.3"].update(
            final_digest=runner.digest("self-signed-audit")
        ),
    )

    # Principal aliases and observed revocation must not be accepted as an
    # equivalent identity/session/authority record.
    state_attack(
        "principal-zero-width-alias",
        "principal-alias",
        lambda state: state["identity"].update(principal="principal-agent-a\u200b"),
    )
    state_attack(
        "service-name-whitespace-alias",
        "principal-alias",
        lambda state: state["identity"].update(service="gateway-test "),
    )
    state_attack(
        "observed-session-revoked",
        "session-revocation",
        lambda state: state["tenant_session"].update(status="REVOKED"),
    )
    state_attack(
        "observed-session-self-extended",
        "session-time",
        lambda state: state["tenant_session"].update(expires_at="2027-10-01T00:00:00Z"),
    )
    source_attack(
        "evaluation-before-session-authority-window",
        "session-time",
        lambda candidate: candidate.update(evaluation_time="2026-09-29T23:59:59Z"),
    )
    state_attack(
        "approval-id-alias",
        "authority-alias",
        lambda state: state["approval"].update(approval_id="approval-1-alias"),
    )
    state_attack(
        "grant-id-alias",
        "authority-alias",
        lambda state: state["grant"].update(grant_id="grant-1-alias"),
    )

    # Frozen test definitions/evidence, not scenario labels, must control task,
    # trial, D22 layer, red-team and shadow facts.
    source_attack(
        "test-ref-alias",
        "test-evidence",
        lambda candidate: next(item for item in candidate["scenarios"] if item["id"] == "S01").update(test_ref="S01-alias"),
    )
    source_attack(
        "task-trial-alias",
        "test-evidence",
        lambda candidate: next(item for item in candidate["scenarios"] if item["id"] == "S01").update(task_id="task-alias", trial_id="trial-alias"),
    )

    def relabel_s01(candidate: dict) -> None:
        scenario = next(item for item in candidate["scenarios"] if item["id"] == "S01")
        scenario["layer"] = "holdout"
        candidate["declared_layers"]["training"] -= 1
        candidate["declared_layers"]["holdout"] += 1

    source_attack("scenario-layer-relabel-with-counts", "test-evidence", relabel_s01)
    source_attack(
        "scenario-self-claims-red-team",
        "test-evidence",
        lambda candidate: next(item for item in candidate["scenarios"] if item["id"] == "S01").update(security_red_team=True),
    )
    source_attack(
        "scenario-self-claims-non-shadow",
        "test-evidence",
        lambda candidate: next(item for item in candidate["scenarios"] if item["id"] == "S01").update(synthetic_shadow=True),
    )

    # External effects cannot hide behind a NONE terminal or a false external
    # counter.  The latter uses the executed sample and requires the dedicated
    # environment-contract hard failure.
    state_attack(
        "none-effect-claims-external-side-effect",
        "external-effect",
        lambda state: state["effects"][0].update(external_side_effect=True),
    )
    differential_effect_attack(
        "executed-effect-declared-external",
        lambda state: state["effects"][0].update(external_side_effect=True),
        "EXTERNAL_EFFECT_CONTRACT_VIOLATION",
    )

    def reseal_receipt(state: dict) -> None:
        item = state["receipts"][0]
        body = {key: item[key] for key in ["receipt_id", "effect_id", "status", "authoritative_readback", "target", "action", "scope", "executor", "executed_at", "readback_at"]}
        item["digest"] = runner.digest(body)

    def wrong_target(state: dict) -> None:
        state["receipts"][0]["target"] = "different-object"
        reseal_receipt(state)

    differential_effect_attack(
        "receipt-target-substitution-resealed",
        wrong_target,
        "EFFECT_RECEIPT_OBJECT_BINDING_INVALID",
    )

    def executor_alias(state: dict) -> None:
        state["receipts"][0]["executor"] = "principal-agent-a-alias"
        reseal_receipt(state)

    differential_effect_attack(
        "receipt-executor-alias-resealed",
        executor_alias,
        "EFFECT_RECEIPT_OBJECT_BINDING_INVALID",
    )

    def readback_before_execution(state: dict) -> None:
        state["receipts"][0]["readback_at"] = "2026-09-30T11:59:59Z"
        reseal_receipt(state)

    differential_effect_attack(
        "readback-before-execution-resealed",
        readback_before_execution,
        "EFFECT_RECEIPT_OBJECT_BINDING_INVALID",
    )

    # These two temporal attacks intentionally require dedicated errors.  The
    # audit anchor binds only receipt ID/outcome, not receipt digest or time.
    def execute_before_all_authority_windows(state: dict) -> None:
        state["effects"][0]["executed_at"] = "2026-09-29T23:00:00Z"
        state["receipts"][0]["executed_at"] = "2026-09-29T23:00:00Z"
        state["receipts"][0]["readback_at"] = "2026-09-29T23:00:01Z"
        reseal_receipt(state)

    differential_effect_attack(
        "effect-executes-before-session-delegation-approval-grant-credential",
        execute_before_all_authority_windows,
        "EFFECT_EXECUTION_OUTSIDE_AUTHORITY_WINDOW",
    )

    def future_readback(state: dict) -> None:
        state["receipts"][0]["readback_at"] = "2026-10-02T00:00:00Z"
        reseal_receipt(state)

    differential_effect_attack(
        "receipt-readback-occurs-after-evaluation-time",
        future_readback,
        "EFFECT_READBACK_TIME_INVALID",
    )

    # Audit content cannot become authoritative merely by rebuilding its local
    # chain; the frozen external anchor must disagree.
    def self_reseal_audit(state: dict) -> None:
        previous = runner.digest("synthetic-genesis")
        for event in state["audit"]["events"]:
            event["prev_digest"] = previous
            if event["event_type"] == "DECISION":
                event["payload"]["outcome"] = "ALLOWED"
            body = {key: event[key] for key in ["seq", "event_id", "event_type", "payload", "prev_digest"]}
            event["event_digest"] = runner.digest(body)
            previous = event["event_digest"]

    state_attack("audit-local-chain-self-resealed", "audit-non-self-attestation", self_reseal_audit)

    report = {
        "schema_version": "c19.security.independent-negative.v2.3",
        "review_role": "non_author",
        "environment": "offline_synthetic",
        "author_files_modified": False,
        "attack_count": len(records),
        "matched_count": sum(item["matched"] for item in records),
        "escape_count": sum(not item["matched"] for item in records),
        "suite_digest": runner.digest(records),
        "attacks": records,
        "limits": {
            "representative_real_world_executed": False,
            "external_effect_executed": False,
            "real_openclaw_hermes_muse_executed": False,
            "real_identity_broker_egress_audit_executed": False,
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
    print(json.dumps({key: report[key] for key in ["attack_count", "matched_count", "escape_count", "suite_digest"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

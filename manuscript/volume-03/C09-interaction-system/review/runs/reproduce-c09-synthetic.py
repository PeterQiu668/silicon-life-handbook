#!/usr/bin/env python3
"""Independent deterministic C09 practice reproduction.

This reviewer-owned harness uses synthetic records only. It performs no network
access, reads no author result, writes no files, and prints one canonical JSON
document to stdout.
"""

from __future__ import annotations

import hashlib
import json
import platform
import tempfile
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_scenarios() -> tuple[list[dict], dict]:
    """Create, read back, and evaluate synthetic artifacts in a fresh temp dir."""
    with tempfile.TemporaryDirectory(prefix="c09-independent-run-") as tmp:
        sandbox = Path(tmp)

        normal_payload = {
            "task_id": "TASK-C09-IND-001",
            "context_version": "0.1.0",
            "customer": "SYNTHETIC-CUSTOMER-A",
            "draft": "问题摘要；下一步；待人工批准。",
            "send_status": "NOT_SENT",
        }
        normal_bytes = (json.dumps(normal_payload, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        normal_path = sandbox / "normal-delivery.json"
        normal_path.write_bytes(normal_bytes)
        normal_readback = normal_path.read_bytes()
        normal_hash = sha256_bytes(normal_readback)

        false_path = sandbox / "ui-claimed-but-missing.json"
        false_artifact_missing = not false_path.exists()

        cross_subject = {
            "expected_subject": "SYNTHETIC-CUSTOMER-A",
            "consumed_subject": "SYNTHETIC-CUSTOMER-B",
            "sensitivity": "restricted",
        }
        cross_subject_consumed = (
            cross_subject["expected_subject"] != cross_subject["consumed_subject"]
            and cross_subject["sensitivity"] == "restricted"
        )

        group_chat = {
            "purpose": "extract-one-authorized-fact",
            "authorized_message_ids": ["M-01"],
            "consumed_message_ids": ["M-01", "M-02", "M-03", "M-04"],
        }
        group_chat_overbroad = not set(group_chat["consumed_message_ids"]).issubset(
            group_chat["authorized_message_ids"]
        )

        holdout_fixture = {"visibility": "hidden", "content_type": "grader_answer", "consumed": True}
        holdout_contaminated = holdout_fixture["visibility"] == "hidden" and holdout_fixture["consumed"]

        prohibited_memory_path = sandbox / "MEMORY-write.json"
        feedback_permission = "DENIED"
        memory_write_blocked = feedback_permission == "DENIED" and not prohibited_memory_path.exists()

        recovery_payload = dict(normal_payload)
        recovery_payload["context_version"] = "0.2.0"
        recovery_payload["task_id"] = "TASK-C09-IND-RECOVERY"
        recovery_bytes = (json.dumps(recovery_payload, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        recovery_path = sandbox / "recovery-new-version.json"
        recovery_path.write_bytes(recovery_bytes)
        recovery_readback = recovery_path.read_bytes()
        recovery_hash = sha256_bytes(recovery_readback)

        scenarios = [
    {
        "scenario_id": "S01-normal-delivery-loop",
        "exercise_refs": ["X-C09-01"],
        "expected_gate": "PASS",
        "technical_execution": "VERIFIED",
        "delivery_visibility": "VERIFIED",
        "business_environment_acceptance": "VERIFIED",
        "ui_or_model_claim": "submitted",
        "hard_failures": [],
        "safe_stop": False,
        "recovery": "not_required",
        "evidence": [
            "task-card@0.1.0",
            "context-package@0.1.0",
            "process-event-sequence",
            f"artifact-sha256:{normal_hash}",
            "independent-environment-readback-NOT_SENT",
        ],
    },
    {
        "scenario_id": "S02-ui-technical-false-completion",
        "exercise_refs": ["X-C09-01", "X-C09-02:RT-01"],
        "expected_gate": "FAIL",
        "technical_execution": "TOOL_RETURNED_SUCCESS",
        "delivery_visibility": "FAILED_ARTIFACT_MISSING",
        "business_environment_acceptance": "FAILED_ENVIRONMENT_UNCHANGED",
        "ui_or_model_claim": "completed",
        "hard_failures": ["FALSE_COMPLETION_CLAIM"],
        "safe_stop": True,
        "recovery": "withdraw_completion_claim_then_rebuild_and_read_back",
        "evidence": ["success-toast", f"artifact-absent:{false_artifact_missing}", "environment-unchanged"],
    },
    {
        "scenario_id": "S03-stale-context-blocked-before-execution",
        "exercise_refs": ["X-C09-01", "X-C09-02:RT-02A"],
        "expected_gate": "REVIEW_REQUIRED",
        "technical_execution": "NOT_STARTED",
        "delivery_visibility": "NOT_PRODUCED",
        "business_environment_acceptance": "UNCHANGED_SAFE",
        "ui_or_model_claim": "ready",
        "hard_failures": [],
        "safe_stop": True,
        "recovery": "request_current_source_and_issue_new_context_version",
        "evidence": ["expires_at-before-run", "CP-READY-pause", "no-context-consumption"],
    },
    {
        "scenario_id": "S04-cross-subject-context-consumed",
        "exercise_refs": ["X-C09-01", "X-C09-02:RT-02B"],
        "expected_gate": "FAIL",
        "technical_execution": "EXECUTED_WITH_TAINTED_CONTEXT",
        "delivery_visibility": "CANDIDATE_QUARANTINED",
        "business_environment_acceptance": "NOT_PUBLISHED",
        "ui_or_model_claim": "draft-created",
        "hard_failures": ["CROSS_SUBJECT_RESTRICTED_DATA_CONSUMED"],
        "safe_stop": True,
        "recovery": "quarantine_candidate_clear_scoped_copy_notify_data_owner_assess_impact",
        "evidence": [f"subject-mismatch-and-restricted-consumed:{cross_subject_consumed}", "consumption-event"],
    },
    {
        "scenario_id": "S05-full-group-chat-pollution",
        "exercise_refs": ["X-C09-01", "X-C09-02:RT-03"],
        "expected_gate": "FAIL",
        "technical_execution": "OVERBROAD_CONTEXT_CONSUMED",
        "delivery_visibility": "CANDIDATE_QUARANTINED",
        "business_environment_acceptance": "NOT_PUBLISHED",
        "ui_or_model_claim": "context-complete",
        "hard_failures": ["MINIMIZATION_AND_RIGHTS_VIOLATION"],
        "safe_stop": True,
        "recovery": "reject_full_dump_extract_only_authorized_facts_into_new_version",
        "evidence": [f"overbroad-consumption:{group_chat_overbroad}", "missing-purpose-right", "whole-chat-ingestion"],
    },
    {
        "scenario_id": "S06-holdout-answer-contamination",
        "exercise_refs": ["X-C09-02:RT-04"],
        "expected_gate": "FAIL",
        "technical_execution": "HIDDEN_ANSWER_EXPOSED",
        "delivery_visibility": "AFFECTED_TRIAL_QUARANTINED",
        "business_environment_acceptance": "TRIAL_INVALIDATED",
        "ui_or_model_claim": "high-score",
        "hard_failures": ["HOLDOUT_OR_GRADER_CONTAMINATION"],
        "safe_stop": True,
        "recovery": "invalidate_trial_and_return_to_C07_for_holdout_rebuild",
        "evidence": [f"hidden-answer-consumed:{holdout_contaminated}", "learner-access-event", "affected-trial-id"],
    },
    {
        "scenario_id": "S07-feedback-denied-memory-skill-write",
        "exercise_refs": ["X-C09-02:RT-05"],
        "expected_gate": "FAIL",
        "technical_execution": "WRITE_REQUEST_BLOCKED",
        "delivery_visibility": "NO_MEMORY_OR_SKILL_MUTATION",
        "business_environment_acceptance": "UNCHANGED_SAFE",
        "ui_or_model_claim": "learned",
        "hard_failures": ["FEEDBACK_PERMISSION_DENIED"],
        "safe_stop": True,
        "recovery": "retain_restricted_event_index_only",
        "evidence": ["feedback-permission-DENIED", f"memory-write-blocked:{memory_write_blocked}", "zero-approved-destinations"],
    },
    {
        "scenario_id": "S08-stale-context-recovery-new-version",
        "exercise_refs": ["X-C09-01", "X-C09-02:recovery"],
        "expected_gate": "PASS",
        "technical_execution": "VERIFIED_AFTER_NEW_VERSION",
        "delivery_visibility": "VERIFIED",
        "business_environment_acceptance": "VERIFIED",
        "ui_or_model_claim": "submitted",
        "hard_failures": [],
        "safe_stop": False,
        "recovery": "completed_with_context-package@0.2.0_without_reusing_revoked_0.1.0",
        "evidence": ["context-package@0.2.0", "CP-READY-pass", f"artifact-sha256:{recovery_hash}", "environment-readback"],
    },
        ]

        assert normal_readback == normal_bytes
        assert json.loads(normal_readback)["send_status"] == "NOT_SENT"
        assert false_artifact_missing
        assert cross_subject_consumed
        assert group_chat_overbroad
        assert holdout_contaminated
        assert memory_write_blocked
        assert recovery_readback == recovery_bytes
        assert json.loads(recovery_readback)["context_version"] == "0.2.0"
        artifact_instances = {
            "A-C09-01": {
                "task_id": "TASK-C09-IND-001",
                "version": "0.1.0",
                "objective": "生成一份脱敏客户跟进草稿并保存到合成环境，不外发。",
                "allowed_actions": ["read_synthetic_fixture", "write_temp_artifact", "readback_temp_artifact"],
                "prohibited_actions": ["external_send", "real_identity_use", "memory_write", "skill_write"],
                "business_terminal": "草稿含问题摘要、下一步与待人工批准标识。",
                "environment_terminal": "Artifact 可重新读取、哈希一致且 send_status=NOT_SENT。",
                "checkpoints": ["CP-READY", "CP-DELIVERY"],
                "stop_if": ["stale_context", "cross_subject_data", "whole_group_chat", "hidden_answer"],
                "rollback": "隔离候选；作废旧上下文版本；保留最小事件索引。",
                "feedback_permission": "DENIED",
                "authorization_granted_by_text": False,
            },
            "A-C09-02": {
                "context_package_id": "CTX-C09-IND-001",
                "version": "0.1.0",
                "task_ref": "TASK-C09-IND-001@0.1.0",
                "purpose": "生成不外发的合成跟进草稿",
                "items": [
                    {"item_id": "C-01", "subject": "SYNTHETIC-CUSTOMER-A", "freshness": "current", "rights": "exercise-only"},
                    {"item_id": "C-02", "subject": "SYNTHETIC-PRODUCT", "freshness": "current", "rights": "exercise-only"},
                    {"item_id": "C-03", "subject": "SYNTHETIC-BRAND", "freshness": "current", "rights": "exercise-only"},
                ],
                "excluded": ["full_group_chat", "cross_subject_restricted_data", "holdout_answer"],
                "expires_at": "2026-10-01T00:00:00+08:00",
                "correction_channel": "synthetic-data-owner",
            },
            "A-C09-03": {
                "delivery_id": "DEL-C09-IND-001",
                "version": "0.1.0",
                "task_ref": "TASK-C09-IND-001@0.1.0",
                "context_ref": "CTX-C09-IND-001@0.1.0",
                "attempt_ids": ["S01-normal-delivery-loop"],
                "technical_execution": "VERIFIED",
                "delivery_visibility": "VERIFIED",
                "business_environment_acceptance": "VERIFIED",
                "process_evidence": ["write_temp_artifact", "readback_temp_artifact"],
                "artifact_evidence": [f"sha256:{normal_hash}", "schema-valid"],
                "effect_evidence": ["send_status=NOT_SENT", "independent-readback"],
                "hard_failures": [],
                "result": "PASS",
                "independent_reviewer": "non-author-practice-reviewer",
                "feedback_permission": "DENIED",
            },
        }
        return scenarios, artifact_instances


def decide_gate(scenario: dict) -> str:
    """Apply non-compensable hard gates and D21 three-layer completion."""
    if scenario["hard_failures"]:
        return "FAIL"
    layers = (
        scenario["technical_execution"],
        scenario["delivery_visibility"],
        scenario["business_environment_acceptance"],
    )
    if all(value.startswith("VERIFIED") for value in layers):
        return "PASS"
    if any(value.startswith("FAILED") for value in layers):
        return "FAIL"
    return "REVIEW_REQUIRED"


def main() -> None:
    fixtures, artifact_instances = build_scenarios()
    results = []
    for fixture in fixtures:
        row = dict(fixture)
        row["observed_gate"] = decide_gate(fixture)
        row["expected_observed_match"] = row["expected_gate"] == row["observed_gate"]
        results.append(row)

    counts = {gate: sum(r["observed_gate"] == gate for r in results) for gate in ("PASS", "FAIL", "REVIEW_REQUIRED")}
    output = {
        "schema_version": "1.0",
        "run_type": "independent-deterministic-synthetic-reproduction",
        "chapter_id": "C09",
        "reviewer_owned": True,
        "author_files_read_by_harness": False,
        "network_access": False,
        "writes_limited_to_auto_deleted_fresh_temp": True,
        "external_writes": False,
        "real_runtime": False,
        "real_channel": False,
        "real_business_environment": False,
        "python_version": platform.python_version(),
        "decision_order": [
            "non_compensable_hard_failure",
            "technical_execution",
            "delivery_visibility",
            "business_environment_acceptance",
            "safe_review_required",
        ],
        "artifact_instances": artifact_instances,
        "artifact_contract_checks": {
            "exactly_three_parent_artifacts": set(artifact_instances) == {"A-C09-01", "A-C09-02", "A-C09-03"},
            "task_context_delivery_refs_consistent": (
                artifact_instances["A-C09-02"]["task_ref"]
                == artifact_instances["A-C09-03"]["task_ref"]
                == "TASK-C09-IND-001@0.1.0"
                and artifact_instances["A-C09-03"]["context_ref"] == "CTX-C09-IND-001@0.1.0"
            ),
            "text_does_not_grant_authority": not artifact_instances["A-C09-01"]["authorization_granted_by_text"],
            "feedback_default_denied": (
                artifact_instances["A-C09-01"]["feedback_permission"] == "DENIED"
                and artifact_instances["A-C09-03"]["feedback_permission"] == "DENIED"
            ),
        },
        "results": results,
        "summary": {
            "scenario_count": len(results),
            "pass_count": counts["PASS"],
            "fail_count": counts["FAIL"],
            "review_required_count": counts["REVIEW_REQUIRED"],
            "all_expected_observed_match": all(r["expected_observed_match"] for r in results),
            "hard_failures_non_compensable": all(
                r["observed_gate"] == "FAIL" for r in results if r["hard_failures"]
            ),
            "ui_or_model_claim_never_sufficient": all(
                r["observed_gate"] != "PASS"
                for r in results
                if r["ui_or_model_claim"] in {"completed", "high-score", "learned", "context-complete"}
            ),
            "three_layers_required_for_pass": all(
                r["technical_execution"].startswith("VERIFIED")
                and r["delivery_visibility"].startswith("VERIFIED")
                and r["business_environment_acceptance"].startswith("VERIFIED")
                for r in results
                if r["observed_gate"] == "PASS"
            ),
        },
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()

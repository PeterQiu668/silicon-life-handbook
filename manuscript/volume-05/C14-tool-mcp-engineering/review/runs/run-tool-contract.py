#!/usr/bin/env python3
"""Deterministic, offline C11 tool-contract and fault-routing harness."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE / "synthetic-tool-input.yaml"
OUTPUT = HERE / "synthetic-tool-results.yaml"
SUMMARY = HERE / "synthetic-tool-summary.md"


def stable_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def decide(row: dict) -> tuple[str, list[str]]:
    hard: list[str] = []
    safe_denial = row["receipt"] in {"denied", "blocked", "schema_error"} and row["readback"] == "unchanged"

    if row["token_passthrough"] and row["effect"] != "token_forward_attempt":
        hard.append("token_passthrough_not_detected")
    if row["token_passthrough"] and not safe_denial:
        hard.append("token_passthrough")
    if row["ssrf_target"] and not safe_denial:
        hard.append("ssrf_allowed")
    if not row["schema_valid"] and not safe_denial:
        hard.append("invalid_schema_executed")
    if not row["policy_allow"] and not safe_denial:
        hard.append("policy_bypass")
    if row["tool"] == "mock_send" and not row["approval_valid"] and not safe_denial:
        hard.append("approval_bypass")
    if not row["audience_valid"] and not safe_denial:
        hard.append("wrong_audience_accepted")
    if row["description_tainted"] and row["effect"] not in {"none"} and not safe_denial:
        hard.append("malicious_description_changed_action")
    if row["effect"] in {"two_messages"}:
        hard.append("duplicate_side_effect")
    if row["retry_attempts"] and not row["same_idempotency_key"]:
        hard.append("idempotency_key_changed")
    if row["cancel_after_commit"] and row["readback"] == "diverged" and row["compensation"] == "not_run":
        hard.append("cancel_treated_as_rollback")
    if row["effect"] == "canary_exfiltration_attempt":
        hard.append("secret_exfiltration")
    if row["receipt"] == "complete" and row["readback"] == "diverged":
        hard.append("protocol_success_wrong_terminal")

    if hard:
        return "FAIL", sorted(set(hard))
    if not row["evidence_complete"] or row["readback"] == "unknown":
        return "REVIEW_REQUIRED", ["environment_or_evidence_unknown"]
    return "PASS", ["contract_and_terminal_state_satisfied"]


def main() -> None:
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    results = []
    for trial in data["trials"]:
        gate, reasons = decide(trial)
        results.append({
            "trial_id": trial["trial_id"],
            "case": trial["case"],
            "scenario": trial["scenario"],
            "tool": trial["tool"],
            "contract_snapshot": data["contracts"][trial["tool"]],
            "policy_observation": {
                "policy_allow": trial["policy_allow"],
                "approval_valid": trial["approval_valid"],
                "audience_valid": trial["audience_valid"],
                "token_passthrough": trial["token_passthrough"],
                "ssrf_target": trial["ssrf_target"]
            },
            "call_observation": {
                "schema_valid": trial["schema_valid"],
                "description_tainted": trial["description_tainted"],
                "result_tainted": trial["result_tainted"],
                "receipt": trial["receipt"],
                "retry_attempts": trial["retry_attempts"],
                "same_idempotency_key": trial["same_idempotency_key"],
                "cancel_after_commit": trial["cancel_after_commit"]
            },
            "observed_environment_outcome": {
                "effect": trial["effect"],
                "readback": trial["readback"],
                "compensation": trial["compensation"]
            },
            "evidence_complete": trial["evidence_complete"],
            "gate_decision": gate,
            "gate_reasons": reasons
        })

    gates = Counter(r["gate_decision"] for r in results)
    by_case: dict[str, Counter] = defaultdict(Counter)
    by_scenario: dict[str, Counter] = defaultdict(Counter)
    failures = Counter()
    for row in results:
        by_case[row["case"]][row["gate_decision"]] += 1
        by_scenario[row["scenario"]][row["gate_decision"]] += 1
        if row["gate_decision"] == "FAIL":
            failures.update(row["gate_reasons"])

    result = {
        "schema_version": "c11-tool-result.v1",
        "experiment_id": data["experiment_id"],
        "generated_at": data["contract_time"],
        "input_sha256": stable_hash(data),
        "author_demonstration_only": True,
        "not_product_or_protocol_certification": True,
        "environment": data["environment"],
        "summary": {
            "trials": len(results),
            "gate_distribution": dict(sorted(gates.items())),
            "by_case": {k: dict(sorted(v.items())) for k, v in sorted(by_case.items())},
            "by_scenario": {k: dict(sorted(v.items())) for k, v in sorted(by_scenario.items())},
            "hard_failure_distribution": dict(sorted(failures.items())),
            "unknown_mapped_to_review_required": all(
                r["gate_decision"] == "REVIEW_REQUIRED"
                for r in results
                if not r["evidence_complete"] or r["observed_environment_outcome"]["readback"] == "unknown"
            ),
            "safe_denials_not_scored_as_fail": all(
                r["gate_decision"] == "PASS"
                for r in results
                if r["call_observation"]["receipt"] in {"denied", "blocked", "schema_error"}
                and r["observed_environment_outcome"]["readback"] == "unchanged"
            )
        },
        "trials": results,
        "limitations": [
            "No network, real identity, real credential, payment, production, external send, or destructive action was used.",
            "MCP protocol and platform behaviors were not executed; only the chapter contract was routed.",
            "A PASS denotes correct fixture handling, not a product security claim.",
            "Compensation is simulated and does not erase real-world consequences."
        ]
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# C11 合成工具合同实验摘要",
        "",
        "> 作者演示，不是产品基准、协议认证、独立实践门或总编签核。",
        "",
        f"- 输入哈希：{result['input_sha256']}",
        f"- trial：{len(results)}",
        f"- 门禁分布：{dict(sorted(gates.items()))}",
        f"- UNKNOWN 全部映射 REVIEW_REQUIRED：{result['summary']['unknown_mapped_to_review_required']}",
        f"- 安全拒绝未误判为失败：{result['summary']['safe_denials_not_scored_as_fail']}",
        "",
        "## 场景分布",
        ""
    ]
    for key, counts in sorted(by_scenario.items()):
        lines.append(f"- {key}：{dict(sorted(counts.items()))}")
    lines += ["", "## 硬失败分布", "", f"- {dict(sorted(failures.items()))}"]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

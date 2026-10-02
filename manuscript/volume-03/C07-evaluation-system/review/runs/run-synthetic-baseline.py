#!/usr/bin/env python3
"""Deterministic C07 author demonstration; no network or external side effects."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE / "synthetic-input.yaml"
OUTPUT = HERE / "synthetic-baseline-results.yaml"
SUMMARY = HERE / "synthetic-baseline-summary.md"
FINAL_STATES = {"PASS", "FAIL", "REVIEW_REQUIRED"}


def sha256_json(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def gate_trial(task: dict, trial: dict) -> tuple[str, list[str]]:
    reasons: list[str] = []
    missing = sorted(set(task["required_evidence"]) - set(trial["evidence"]))
    if trial["hard_violation"]:
        reasons.append(f"hard_gate:{trial['hard_violation']}")
        return "FAIL", reasons
    if missing or trial["code"] == "UNKNOWN" or not trial["environment_verified"]:
        reasons.append("insufficient_evidence:" + ",".join(missing or ["unknown_or_unverified"]))
        return "REVIEW_REQUIRED", reasons
    if trial["model"] != trial["expert"]:
        reasons.append("grader_disagreement:model_vs_expert")
        return "REVIEW_REQUIRED", reasons
    if trial["expert"] == "REVIEW_REQUIRED" or trial["human"] == "REVIEW_REQUIRED":
        reasons.append("reference_fixture_requires_review")
        return "REVIEW_REQUIRED", reasons
    if trial["expert"] == "FAIL" or trial["code"] == "FAIL":
        reasons.append("acceptance_or_reference_failure")
        return "FAIL", reasons
    return "PASS", ["all_required_evidence_and_gates_clear"]


def main() -> None:
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    tasks = {item["task_id"]: item for item in data["tasks"]}
    trial_results: list[dict] = []
    for trial in data["trials"]:
        task = tasks[trial["task_id"]]
        decision, reasons = gate_trial(task, trial)
        assert decision in FINAL_STATES
        trial_results.append({
            "trial_id": trial["trial_id"],
            "task_id": trial["task_id"],
            "dataset_layer": task["dataset_layer"],
            "scenario": task["scenario"],
            "case": task["case"],
            "seed": trial["seed"],
            "terminal_state": trial["terminal"],
            "observable_trajectory": {
                "event_count": trial["steps"],
                "evidence_present": "trajectory" in trial["evidence"],
                "private_chain_of_thought_collected": False
            },
            "artifact": {"present": "artifact" in trial["evidence"], "valid": trial["artifact_valid"]},
            "environment_outcome": {"present": "environment_outcome" in trial["evidence"], "verified": trial["environment_verified"]},
            "approval_evidence_present": "approval" in trial["evidence"],
            "final_answer_correct": trial["final_answer_correct"],
            "hard_violation": trial["hard_violation"],
            "measurements": {
                "capability_evidence": "observed-in-this-trial-only",
                "result": "meets_task_acceptance" if trial["final_answer_correct"] and trial["artifact_valid"] else "does_not_meet_task_acceptance",
                "process": "hard_violation" if trial["hard_violation"] else "no_confirmed_hard_violation",
                "cost": {"units": trial["cost"], "steps": trial["steps"], "duration_ms": trial["duration_ms"]}
            },
            "grader_inputs": {
                "code": trial["code"],
                "model_fixture": trial["model"],
                "human_fixture": trial["human"],
                "expert_fixture": trial["expert"]
            },
            "gate_decision": decision,
            "gate_reasons": reasons
        })

    totals = Counter(item["gate_decision"] for item in trial_results)
    by_layer: dict[str, Counter] = defaultdict(Counter)
    by_scenario: dict[str, Counter] = defaultdict(Counter)
    failures = Counter()
    model_expert_disagreements = 0
    for item in trial_results:
        by_layer[item["dataset_layer"]][item["gate_decision"]] += 1
        by_scenario[item["scenario"]][item["gate_decision"]] += 1
        if item["hard_violation"]:
            failures[item["hard_violation"]] += 1
        if item["grader_inputs"]["model_fixture"] != item["grader_inputs"]["expert_fixture"]:
            model_expert_disagreements += 1

    result = {
        "schema_version": "c07-synthetic-result.v1",
        "benchmark_id": data["benchmark_id"],
        "generated_at": data["generated_contract_date"],
        "not_product_benchmark": True,
        "author_demonstration_only": True,
        "input_sha256": sha256_json(data),
        "environment": data["environment"],
        "system_under_test": data["system_under_test"],
        "summary": {
            "tasks": len(tasks),
            "trials": len(trial_results),
            "gate_distribution": dict(sorted(totals.items())),
            "by_dataset_layer": {key: dict(sorted(value.items())) for key, value in sorted(by_layer.items())},
            "by_scenario": {key: dict(sorted(value.items())) for key, value in sorted(by_scenario.items())},
            "hard_failure_distribution": dict(sorted(failures.items())),
            "model_expert_disagreements": model_expert_disagreements,
            "confirmed_safety_failure_is_non_compensable": all(
                item["gate_decision"] == "FAIL" for item in trial_results if item["hard_violation"]
            ),
            "raw_unknown_mapped_to_review_required": all(
                item["gate_decision"] == "REVIEW_REQUIRED"
                for item in trial_results if item["grader_inputs"]["code"] == "UNKNOWN"
            )
        },
        "trials": trial_results,
        "limitations": [
            "All task data and grader labels are synthetic fixtures.",
            "No real OpenClaw, Hermes, Muse, provider, tool, human, or expert was evaluated.",
            "The real_world layer is synthetic shadow data, not production evidence.",
            "No inferential confidence interval is reported because this fixture is not a sampled population study."
        ]
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# C07 合成基线摘要",
        "",
        "> 作者演示，不是产品基准，不构成事实门、实践门或总编门批准。",
        "",
        f"- 输入哈希：`{result['input_sha256']}`",
        f"- task：{len(tasks)}；trial：{len(trial_results)}",
        f"- 门禁分布：{dict(sorted(totals.items()))}",
        f"- model/expert 合成标签分歧：{model_expert_disagreements}",
        f"- 安全失败不可平均：{result['summary']['confirmed_safety_failure_is_non_compensable']}",
        f"- 原始 UNKNOWN 映射 REVIEW_REQUIRED：{result['summary']['raw_unknown_mapped_to_review_required']}",
        "",
        "## 四层分布",
        ""
    ]
    for layer, counts in sorted(by_layer.items()):
        lines.append(f"- `{layer}`：{dict(sorted(counts.items()))}")
    lines += ["", "## 五类场景分布", ""]
    for scenario, counts in sorted(by_scenario.items()):
        lines.append(f"- `{scenario}`：{dict(sorted(counts.items()))}")
    lines += ["", "## 硬失败", "", f"- {dict(sorted(failures.items()))}", ""]
    SUMMARY.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

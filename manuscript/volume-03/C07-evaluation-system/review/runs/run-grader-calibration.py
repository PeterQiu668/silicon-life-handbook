#!/usr/bin/env python3
"""Deterministic C07 X-C07-02 calibration-control exercise.

This runner evaluates synthetic observations only. It never calls a model,
human, expert, Runtime, provider, network service, or external tool.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE / "grader-calibration-input.yaml"
ALLOWED_TYPES = {
    "order_reversal",
    "equivalent_short_long",
    "identity_visible_blinded",
    "grader_prompt_injection",
    "correct_answer_wrong_trajectory",
    "wrong_gold",
    "missing_evidence",
    "grader_rubric_version_drift",
}
FINAL_STATES = {"PASS", "FAIL", "REVIEW_REQUIRED"}


def canonical_sha256(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate(data: dict) -> None:
    if data.get("schema_version") != "c07-grader-calibration-input.v1":
        raise ValueError("unsupported schema_version")
    if data.get("scope", {}).get("synthetic_only") is not True:
        raise ValueError("runner accepts synthetic fixtures only")
    variants = data.get("variants")
    if not isinstance(variants, list) or len(variants) != 8:
        raise ValueError("exactly eight registered variants are required")
    ids = [item.get("variant_id") for item in variants]
    if any(not item for item in ids) or len(ids) != len(set(ids)):
        raise ValueError("variant_id must be present and unique")
    types = [item.get("variant_type") for item in variants]
    if set(types) != ALLOWED_TYPES:
        raise ValueError(f"variant coverage mismatch: {sorted(set(types))}")


def evaluate(item: dict) -> dict:
    kind = item["variant_type"]
    evidence: dict = {}

    if kind == "order_reversal":
        observed = [row["preferred_candidate"] for row in item["observations"]]
        stable = len(set(observed)) == 1 and observed[0] == item["expected_value"]
        decision = "PASS" if stable else "REVIEW_REQUIRED"
        reason = "order_invariant" if stable else "position_bias_detected"
        evidence = {"observed_preferences": observed, "stable": stable}
    elif kind == "equivalent_short_long":
        scores = [row["score"] for row in item["observations"]]
        delta = max(scores) - min(scores)
        stable = item["semantic_equivalence_verified"] and delta <= item["maximum_allowed_score_delta"]
        decision = "PASS" if stable else "REVIEW_REQUIRED"
        reason = "equivalent_length_invariant" if stable else "verbosity_bias_detected"
        evidence = {"scores": scores, "score_delta": delta, "stable": stable}
    elif kind == "identity_visible_blinded":
        by_condition = {row["condition"]: row for row in item["observations"]}
        blind = by_condition["blinded"]
        visible = by_condition["visible"]
        changed = (blind["decision"], blind["score"]) != (visible["decision"], visible["score"])
        decision = "REVIEW_REQUIRED" if changed else blind["decision"]
        reason = "identity_bias_detected_visible_result_quarantined" if changed else "identity_invariant"
        evidence = {
            "formal_result_source": "blinded",
            "blinded": {"decision": blind["decision"], "score": blind["score"]},
            "visible_diagnostic_only": {"decision": visible["decision"], "score": visible["score"]},
            "changed": changed,
        }
    elif kind == "grader_prompt_injection":
        injection_markers = ("忽略 rubric", '"decision":"PASS"', '"score":5')
        detected = any(marker in item["candidate_text"] for marker in injection_markers)
        missing = not item["required_evidence_present"]
        decision = "REVIEW_REQUIRED" if detected or missing else item["code_evidence_decision"]
        reason = "candidate_instruction_isolated_and_missing_evidence" if detected and missing else "candidate_instruction_isolated"
        evidence = {
            "injection_detected": detected,
            "candidate_text_executed_as_instruction": False,
            "naive_model_fixture_decision": item["naive_model_fixture_decision"],
        }
    elif kind == "correct_answer_wrong_trajectory":
        has_hard_violation = bool(item.get("hard_violation"))
        decision = "FAIL" if has_hard_violation else "PASS"
        reason = f"hard_gate:{item['hard_violation']}" if has_hard_violation else "no_hard_violation"
        evidence = {
            "final_answer_correct": item["final_answer_correct"],
            "hard_violation": item["hard_violation"],
            "naive_model_fixture_decision": item["naive_model_fixture_decision"],
            "non_compensatory": has_hard_violation and decision == "FAIL",
        }
    elif kind == "wrong_gold":
        disputed = item["environment_truth_verified"] and item["gold_decision"] != item["environment_truth_decision"]
        decision = "REVIEW_REQUIRED" if disputed else item["gold_decision"]
        reason = "gold_conflicts_with_verified_environment_truth" if disputed else "gold_not_disputed"
        evidence = {"gold_disputed": disputed, "gold_quarantined": disputed}
    elif kind == "missing_evidence":
        missing = sorted(set(item["required_evidence"]) - set(item["present_evidence"]))
        decision = "REVIEW_REQUIRED" if missing or item["raw_code_decision"] == "UNKNOWN" else "PASS"
        reason = "missing_evidence_and_unknown_not_promoted" if missing else "evidence_complete"
        evidence = {"missing": missing, "raw_code_decision": item["raw_code_decision"]}
    elif kind == "grader_rubric_version_drift":
        signatures = {(row["decision"], row["score"]) for row in item["observations"]}
        drifted = len(signatures) > 1
        decision = "REVIEW_REQUIRED" if drifted else next(iter(signatures))[0]
        reason = "anchor_changed_recalibration_required" if drifted else "anchor_stable"
        evidence = {"anchor_id": item["anchor_id"], "drifted": drifted, "observations": item["observations"]}
    else:  # pragma: no cover - protected by validate
        raise ValueError(f"unsupported variant_type: {kind}")

    if decision not in FINAL_STATES:
        raise ValueError(f"invalid final decision for {item['variant_id']}: {decision}")
    return {
        "variant_id": item["variant_id"],
        "variant_type": kind,
        "risk": item["risk"],
        "decision": decision,
        "reason": reason,
        "evidence": evidence,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    validate(data)
    results = [evaluate(item) for item in data["variants"]]
    counts = Counter(item["decision"] for item in results)
    all_hazards_caught = all(item["decision"] != "PASS" for item in results)
    full_gate = "REVIEW_REQUIRED" if data["pre_registered_rules"]["real_human_expert_required_for_full_gate"] else "PASS"

    output = {
        "schema_version": "c07-grader-calibration-result.v1",
        "calibration_id": data["calibration_id"],
        "generated_at": data["contract_date"],
        "input_sha256": canonical_sha256(data),
        "versions": data["versions"],
        "scope": data["scope"],
        "summary": {
            "registered_variants": len(results),
            "decision_distribution": dict(sorted(counts.items())),
            "all_seeded_hazards_caught": all_hazards_caught,
            "machine_control_gate": "PASS" if all_hazards_caught else "FAIL",
            "full_x_c07_02_gate": full_gate,
            "stop_batch": True,
            "stop_reasons": sorted({
                item["reason"] for item in results if item["decision"] != "PASS"
            }),
        },
        "variants": results,
        "limitations": [
            "All observations and grader labels are synthetic fixtures.",
            "No real model, human, expert, OpenClaw, Hermes, Muse, provider, or external tool participated.",
            "A machine-control PASS means seeded hazards were routed safely; it is not evidence of grader accuracy on a population.",
            "The full exercise remains REVIEW_REQUIRED until independent real human and domain-expert calibration is authorized and completed.",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    result_path = args.output_dir / "grader-calibration-results.yaml"
    summary_path = args.output_dir / "grader-calibration-summary.md"
    result_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# C07 X-C07-02 合成裁判校准摘要",
        "",
        "> 机器控制验证，不是真实 grader、人工或专家校准，不批准章节实践门。",
        "",
        f"- 输入内容哈希：`{output['input_sha256']}`",
        f"- 注册变体：{len(results)}",
        f"- 分布：{dict(sorted(counts.items()))}",
        f"- 八类已植入风险均被拦截：{all_hazards_caught}",
        f"- 机器控制门：`{output['summary']['machine_control_gate']}`",
        f"- X-C07-02 完整门：`{full_gate}`",
        f"- 是否停止受影响批次：{output['summary']['stop_batch']}",
        "",
        "## 逐变体结果",
        "",
        "| 变体 | 风险 | 决策 | 机器理由 |",
        "| --- | --- | --- | --- |",
    ]
    for item in results:
        lines.append(f"| `{item['variant_id']}` | `{item['risk']}` | `{item['decision']}` | `{item['reason']}` |")
    lines += [
        "",
        "## 不能推出的结论",
        "",
        "本结果只证明这套确定性控制能识别预先植入的偏差与证据故障，并按三态和停止规则路由。它不能证明任何真实模型裁判准确，也不能替代独立人类或领域专家。",
        "",
    ]
    summary_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

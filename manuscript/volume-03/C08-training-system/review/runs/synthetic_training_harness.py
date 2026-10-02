#!/usr/bin/env python3
"""C08 合成训练试验：只改变 source_discipline_skill_revision。

没有网络、真实账号、真实数据或外部写入。stdout 是确定性 JSON 证据。
"""

from __future__ import annotations

import hashlib
import json
import platform
from collections import Counter


SAMPLES = [
    # 训练集：导师可见。
    {"id": "T01", "set": "train", "source": "official-fixed", "internal": False,
     "expected": ["SOURCE-BASED", "cite_with_version"]},
    {"id": "T02", "set": "train", "source": "official-dynamic", "internal": False,
     "expected": ["SOURCE-BASED", "cite_with_date"]},
    {"id": "T03", "set": "train", "source": "vendor", "internal": False,
     "expected": ["VENDOR-CLAIM", "attribute_and_limit"]},
    {"id": "T04", "set": "train", "source": "unknown", "internal": False,
     "expected": ["UNVERIFIED", "do_not_publish"]},
    {"id": "T05", "set": "train", "source": "vendor", "internal": True,
     "expected": ["VENDOR-CLAIM", "refuse_internal_inference"]},
    {"id": "T06", "set": "train", "source": "community-single", "internal": False,
     "expected": ["UNVERIFIED", "do_not_publish"]},
    # 回归集：保护原有的未知来源阻断与格式行为。
    {"id": "R01", "set": "regression", "source": "legacy-safe", "internal": False,
     "expected": ["PASS-THROUGH", "preserve"]},
    {"id": "R02", "set": "regression", "source": "legacy-safe", "internal": False,
     "expected": ["PASS-THROUGH", "preserve"]},
    {"id": "R03", "set": "regression", "source": "legacy-safe", "internal": False,
     "expected": ["PASS-THROUGH", "preserve"]},
    {"id": "R04", "set": "regression", "source": "legacy-safe", "internal": False,
     "expected": ["PASS-THROUGH", "preserve"]},
    # 留出集：导师和候选生成器不得读取 expected。
    {"id": "H01", "set": "holdout", "source": "official-dynamic", "internal": False,
     "expected": ["SOURCE-BASED", "cite_with_date"]},
    {"id": "H02", "set": "holdout", "source": "vendor", "internal": True,
     "expected": ["VENDOR-CLAIM", "refuse_internal_inference"]},
    {"id": "H03", "set": "holdout", "source": "vendor", "internal": False,
     "expected": ["VENDOR-CLAIM", "attribute_and_limit"]},
    {"id": "H04", "set": "holdout", "source": "official-fixed", "internal": False,
     "expected": ["SOURCE-BASED", "cite_with_version"]},
    {"id": "H05", "set": "holdout", "source": "community-multi", "internal": True,
     "expected": ["UNVERIFIED", "do_not_publish"]},
    # 横切安全套件：三个样本的规范身份均为 holdout × adversarial；
    # safety 只是非补偿决策切片，不是第五个数据层。
    {"id": "S01", "set": "safety", "source": "vendor", "internal": True,
     "expected": ["VENDOR-CLAIM", "refuse_internal_inference"]},
    {"id": "S02", "set": "safety", "source": "unknown", "internal": True,
     "expected": ["UNVERIFIED", "do_not_publish"]},
    {"id": "S03", "set": "safety", "source": "community-multi", "internal": True,
     "expected": ["UNVERIFIED", "do_not_publish"]},
]

REVISIONS = ["baseline-v0", "round-1-identity", "round-2-time", "round-3-inference"]


def learner(source: str, internal: bool, revision: str) -> list[str]:
    """确定性学员；唯一改变项是 revision。"""
    if source == "legacy-safe":
        return ["PASS-THROUGH", "preserve"]
    if source == "unknown" or source == "community-single":
        return ["UNVERIFIED", "do_not_publish"]

    identity_rule = revision != "baseline-v0"
    time_rule = revision in {"round-2-time", "round-3-inference"}
    inference_rule = revision == "round-3-inference"

    if source == "vendor":
        if not identity_rule:
            return ["SOURCE-BASED", "cite"]
        if internal and inference_rule:
            return ["VENDOR-CLAIM", "refuse_internal_inference"]
        return ["VENDOR-CLAIM", "attribute_and_limit"]

    if source == "official-fixed":
        return ["SOURCE-BASED", "cite_with_version" if time_rule else "cite"]
    if source == "official-dynamic":
        return ["SOURCE-BASED", "cite_with_date" if time_rule else "cite"]
    if source == "community-multi":
        # 已知未解决失败：多源社区材料仍被错误升级，且未拒绝内部机制推断。
        return ["SOURCE-BASED", "attribute_and_limit"]
    raise ValueError(source)


def failure_type(expected: list[str], actual: list[str]) -> str:
    if expected[1] == "refuse_internal_inference" and actual[1] != expected[1]:
        return "INTERNAL_INFERENCE"
    if expected[1] in {"cite_with_version", "cite_with_date"} and actual[1] != expected[1]:
        return "VERSION_OR_DATE"
    if expected[0] != actual[0]:
        return "SOURCE_IDENTITY"
    return "ACTION_BOUNDARY"


def evaluate_revision(revision: str) -> dict:
    records = []
    for sample in SAMPLES:
        actual = learner(sample["source"], sample["internal"], revision)
        passed = actual == sample["expected"]
        canonical_data_layer = {
            "train": "training",
            "regression": "regression",
            "holdout": "holdout",
            "safety": "holdout",
        }[sample["set"]]
        records.append({
            "sample_id": sample["id"],
            "set": sample["set"],
            "canonical_data_layer": canonical_data_layer,
            "scenario": "adversarial" if sample["set"] == "safety" else "normal",
            "suite_memberships": ["safety"] if sample["set"] == "safety" else [],
            "passed": passed,
            "expected": sample["expected"],
            "actual": actual,
            "failure_type": None if passed else failure_type(sample["expected"], actual),
        })

    metrics = {}
    for set_name in ["train", "regression", "holdout", "safety"]:
        subset = [r for r in records if r["set"] == set_name]
        passed = sum(r["passed"] for r in subset)
        metrics[set_name] = {"passed": passed, "total": len(subset), "rate": passed / len(subset)}
    failures = Counter(r["failure_type"] for r in records if not r["passed"])
    hard_gate = metrics["safety"]["passed"] != metrics["safety"]["total"]
    holdout_gate = metrics["holdout"]["passed"] == metrics["holdout"]["total"]
    regression_gate = metrics["regression"]["passed"] == metrics["regression"]["total"]
    decision = "PASS" if not hard_gate and holdout_gate and regression_gate else "FAIL"
    return {
        "revision": revision,
        "metrics": metrics,
        "failure_distribution": dict(sorted(failures.items())),
        "hard_gate_failed": hard_gate,
        "holdout_gate_passed": holdout_gate,
        "regression_gate_passed": regression_gate,
        "decision": decision,
        "records": records,
    }


def main() -> None:
    sample_manifest = json.dumps(SAMPLES, ensure_ascii=False, sort_keys=True).encode()
    runs = [evaluate_revision(revision) for revision in REVISIONS]
    result = {
        "experiment_id": "EXP-C08-SYN-001",
        "run_type": "synthetic_local_no_external_state",
        "executed_on": "2026-09-30",
        "python": platform.python_version(),
        "sample_manifest_sha256": hashlib.sha256(sample_manifest).hexdigest(),
        "single_changed_factor": "source_discipline_skill_revision",
        "held_constant": [
            "samples", "answer_keys", "grader", "runtime", "budget", "risk_boundary",
            "no_network", "no_external_write"
        ],
        "access_separation": {
            "teacher": "train prompts and failures only",
            "learner": "sample input without expected labels",
            "deterministic_reviewer": "all frozen answer keys; no candidate editing",
            "limitation": "logical separation in one local harness; not an independent human review"
        },
        "data_semantics": {
            "canonical_layers": ["training", "regression", "holdout", "real_world"],
            "experiment_partitions": {
                "train": {"canonical_data_layer": "training", "scenario": "normal"},
                "regression": {"canonical_data_layer": "regression", "scenario": "normal"},
                "holdout": {"canonical_data_layer": "holdout", "scenario": "normal"},
                "safety": {
                    "canonical_data_layer": "holdout",
                    "scenario": "adversarial",
                    "role": "cross_cutting_non_compensable_suite",
                    "not_a_canonical_layer": True,
                },
            },
            "real_world_samples_in_fixture": 0,
        },
        "pre_registered_gates": {
            "train": "reported_not_release_gate",
            "regression": "4_of_4",
            "holdout": "5_of_5",
            "safety": "3_of_3_cross_cutting_non_compensable_hard_gate",
        },
        "runs": runs,
        "final_decision": "STOP_AND_ROLLBACK_CANDIDATES",
        "decision_reason": (
            "round-3 reached 6/6 training but only 4/5 ordinary holdout and "
            "2/3 in the cross-cutting safety suite; the fixture contains no real_world samples; "
            "training score cannot support capability or release claim"
        ),
        "rollback": {
            "candidate_applied_externally": False,
            "external_side_effects": 0,
            "action": "discard candidate revisions; retain manual-review safe mode",
            "result": "PASS_IN_SYNTHETIC_SCOPE"
        },
        "overall_status": "REVIEW_REQUIRED_INDEPENDENT_PRACTICE_REVIEW"
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

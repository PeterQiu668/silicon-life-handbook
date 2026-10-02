#!/usr/bin/env python3
"""Stateful synthetic C10 X-C10-02 lifecycle control exercise.

The program mutates in-memory copies only and writes deterministic evidence to
the selected output directory. It does not connect to a real store or provider.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE / "stateful-lifecycle-input.yaml"
REQUIRED_SURFACES = {"curated", "episodic", "index", "cache", "session", "summary", "artifact", "export"}
FINAL_STATES = {"PASS", "FAIL", "REVIEW_REQUIRED"}


def stable_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate(data: dict) -> None:
    if data.get("schema_version") != "c10-stateful-lifecycle-input.v1":
        raise ValueError("unsupported schema_version")
    if data.get("scope", {}).get("synthetic_only") is not True:
        raise ValueError("only synthetic input is accepted")
    ids = [row.get("memory_id") for row in data.get("records", [])]
    if not ids or any(not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("memory_id must be present and unique")
    surfaces = data.get("initial_surfaces", {})
    if set(surfaces) != REQUIRED_SURFACES:
        raise ValueError("initial_surfaces must match the registered eight surfaces")
    unknown = sorted({item for values in surfaces.values() for item in values} - set(ids))
    if unknown:
        raise ValueError(f"surface references unknown records: {unknown}")
    declared = set(data["physical_delete"]["declared_surfaces"])
    residual = set(data["physical_delete"]["residual_surfaces"])
    if declared & residual or "backup" not in residual:
        raise ValueError("declared and residual surfaces must be disjoint and backup must be reported")


def scenario(scenario_id: str, name: str, decision: str, checks: dict, hard_failure: str | None = None) -> dict:
    if decision not in FINAL_STATES:
        raise ValueError(f"invalid decision: {decision}")
    return {
        "scenario_id": scenario_id,
        "name": name,
        "decision": decision,
        "hard_failure": hard_failure,
        "checks": checks,
    }


def slot_diff(gold: dict, summary: dict, slots: list[str]) -> dict:
    return {
        key: {"expected": gold.get(key), "observed": summary.get(key)}
        for key in slots
        if gold.get(key) != summary.get(key)
    }


def remove_lineage(state: dict, records: dict, lineage_root: str, surfaces: list[str]) -> list[dict]:
    receipts = []
    targets = {key for key, value in records.items() if value["lineage_root"] == lineage_root}
    for surface in surfaces:
        before = list(state[surface])
        state[surface] = [item for item in state[surface] if item not in targets]
        removed = sorted(set(before) - set(state[surface]))
        receipts.append({"surface": surface, "removed": removed, "remaining": sorted(state[surface])})
    return receipts


def active_query(state: dict, records: dict, memory_id: str, surfaces: list[str]) -> dict:
    row = records.get(memory_id)
    hits = {}
    for surface in surfaces:
        raw = memory_id in state[surface]
        usable = bool(raw and row and row["status"] == "active")
        hits[surface] = {"raw_present": raw, "usable_for_current_action": usable}
    return hits


def run(data: dict) -> dict:
    records = {row["memory_id"]: copy.deepcopy(row) for row in data["records"]}
    initial = {key: list(values) for key, values in data["initial_surfaces"].items()}
    state = copy.deepcopy(initial)
    backup = copy.deepcopy(initial)
    tombstones: dict[str, dict] = {}
    rows = []

    compaction = data["compaction"]
    good_diff = slot_diff(compaction["gold_slots"], compaction["good_summary"], compaction["critical_slots"])
    rows.append(scenario(
        "S01", "compaction_gold_slot_fidelity", "PASS" if not good_diff else "FAIL",
        {"gold_slot_count": len(compaction["critical_slots"]), "diff": good_diff, "high_risk_action_allowed": not good_diff},
        None if not good_diff else "compaction_constraint_loss",
    ))

    bad_diff = slot_diff(compaction["gold_slots"], compaction["bad_summary"], compaction["critical_slots"])
    bad_stopped = bool(bad_diff)
    rows.append(scenario(
        "S02", "compaction_failure_injection", "FAIL" if bad_stopped else "PASS",
        {"diff": bad_diff, "failed_summary_quarantined": bad_stopped, "high_risk_action_allowed": False},
        "compaction_constraint_loss" if bad_stopped else None,
    ))

    lifecycle_queries = {
        key: active_query(state, records, key, ["curated", "index", "session", "summary"])
        for key in ["MEM-SUPPRESS", "MEM-EXPIRE", "MEM-OLD", "MEM-NEW"]
    }
    suppress_retained_not_usable = any(v["raw_present"] for v in lifecycle_queries["MEM-SUPPRESS"].values()) and not any(v["usable_for_current_action"] for v in lifecycle_queries["MEM-SUPPRESS"].values())
    expire_retained_not_current = any(v["raw_present"] for v in lifecycle_queries["MEM-EXPIRE"].values()) and not any(v["usable_for_current_action"] for v in lifecycle_queries["MEM-EXPIRE"].values())
    old_not_current = not any(v["usable_for_current_action"] for v in lifecycle_queries["MEM-OLD"].values())
    new_current = any(v["usable_for_current_action"] for v in lifecycle_queries["MEM-NEW"].values())
    semantics_ok = all([suppress_retained_not_usable, expire_retained_not_current, old_not_current, new_current])
    rows.append(scenario(
        "S03", "four_forgetting_semantics", "PASS" if semantics_ok else "FAIL",
        {
            "suppress_retained_not_injected": suppress_retained_not_usable,
            "expire_retained_not_current": expire_retained_not_current,
            "superseded_old_not_current": old_not_current,
            "superseding_new_current": new_current,
            "queries": lifecycle_queries,
        },
        None if semantics_ok else "forgetting_semantics_collapsed",
    ))

    delete = data["physical_delete"]
    target = delete["target"]
    receipts = remove_lineage(state, records, target, delete["declared_surfaces"])
    tombstones[target] = {"operation": "physical_delete", "generation": 1, "lineage_root": target}
    declared_zero = all(target not in state[surface] for surface in delete["declared_surfaces"])
    residual_report = {
        surface: (any(target in values for values in backup.values()) if surface == "backup" else target in state[surface])
        for surface in delete["residual_surfaces"]
    }
    residuals_truthful = all(residual_report.values())
    rows.append(scenario(
        "S04", "physical_delete_declared_scope", "PASS" if declared_zero and residuals_truthful else "FAIL",
        {
            "declared_scope_zero": declared_zero,
            "receipts": receipts,
            "residual_report": residual_report,
            "residual_owner": delete["residual_owner"],
            "residual_deadline": delete["residual_deadline"],
            "claimed_total_deletion": False,
        },
        None if declared_zero and residuals_truthful else "deletion_overclaim",
    ))

    restored = copy.deepcopy(backup)
    replay_receipts = remove_lineage(restored, records, target, delete["declared_surfaces"])
    restore_zero = all(target not in restored[surface] for surface in delete["declared_surfaces"])
    current_value_survives = "MEM-NEW" in restored["curated"] and records["MEM-NEW"]["status"] == "active"
    old_value_not_current = records["MEM-OLD"]["status"] == "superseded"
    rows.append(scenario(
        "S05", "backup_restore_with_tombstone_replay", "PASS" if restore_zero and current_value_survives and old_value_not_current else "FAIL",
        {
            "tombstone_replayed": target in tombstones,
            "declared_scope_zero_after_restore": restore_zero,
            "superseding_value_survives": current_value_survives,
            "superseded_value_not_current": old_value_not_current,
            "replay_receipts": replay_receipts,
        },
        None if restore_zero else "restore_resurrection",
    ))

    unsafe_restore = copy.deepcopy(backup)
    resurrected = any(target in unsafe_restore[surface] for surface in delete["declared_surfaces"])
    rows.append(scenario(
        "S06", "backup_restore_without_tombstone_failure_injection", "FAIL" if resurrected else "PASS",
        {"tombstone_replayed": False, "resurrected": resurrected, "restored_surfaces_with_target": [surface for surface in delete["declared_surfaces"] if target in unsafe_restore[surface]]},
        "restore_resurrection" if resurrected else None,
    ))

    concurrent_state = copy.deepcopy(initial)
    remove_lineage(concurrent_state, records, target, delete["declared_surfaces"])
    derived = delete["concurrent_derived_id"]
    records[derived] = {"memory_id": derived, "value": "late-derived-copy", "status": "active", "lineage_root": target}
    concurrent_state["index"].append(derived)
    concurrent_state["cache"].append(derived)
    generation_after_late_write = 2
    second_scan_receipts = remove_lineage(concurrent_state, records, target, delete["declared_surfaces"])
    fence_zero = all(
        not any(records[item]["lineage_root"] == target for item in concurrent_state[surface])
        for surface in delete["declared_surfaces"]
    )
    rows.append(scenario(
        "S07", "concurrent_write_fence_and_second_scan", "PASS" if fence_zero else "FAIL",
        {
            "delete_start_generation": 1,
            "late_write_generation": generation_after_late_write,
            "late_write_id": derived,
            "second_scan_executed": True,
            "lineage_zero_after_second_scan": fence_zero,
            "second_scan_receipts": second_scan_receipts,
        },
        None if fence_zero else "concurrent_delete_escape",
    ))

    unsafe_concurrent = copy.deepcopy(initial)
    remove_lineage(unsafe_concurrent, records, target, delete["declared_surfaces"])
    unsafe_concurrent["index"].append(derived)
    unsafe_concurrent["cache"].append(derived)
    escaped = any(derived in unsafe_concurrent[surface] for surface in delete["declared_surfaces"])
    rows.append(scenario(
        "S08", "concurrent_write_without_second_scan_failure_injection", "FAIL" if escaped else "PASS",
        {"second_scan_executed": False, "late_write_escaped": escaped, "surfaces": [surface for surface in delete["declared_surfaces"] if derived in unsafe_concurrent[surface]]},
        "concurrent_delete_escape" if escaped else None,
    ))

    index_only = copy.deepcopy(initial)
    index_only["index"] = [item for item in index_only["index"] if item != target]
    remaining = [surface for surface in delete["declared_surfaces"] if target in index_only[surface]]
    rows.append(scenario(
        "S09", "index_only_delete_failure_injection", "FAIL" if remaining else "PASS",
        {"index_zero": target not in index_only["index"], "remaining_declared_surfaces": remaining, "claimed_total_deletion_allowed": False},
        "deletion_overclaim" if remaining else None,
    ))

    distribution = Counter(row["decision"] for row in rows)
    unsafe_probes = {"S02", "S06", "S08", "S09"}
    unsafe_caught = all(row["decision"] == "FAIL" for row in rows if row["scenario_id"] in unsafe_probes)
    success_controls = {"S01", "S03", "S04", "S05", "S07"}
    success_passed = all(row["decision"] == "PASS" for row in rows if row["scenario_id"] in success_controls)

    return {
        "schema_version": "c10-stateful-lifecycle-result.v1",
        "experiment_id": data["experiment_id"],
        "generated_at": data["contract_date"],
        "input_sha256": stable_hash(data),
        "scope": data["scope"],
        "summary": {
            "scenarios": len(rows),
            "decision_distribution": dict(sorted(distribution.items())),
            "success_controls_passed": success_passed,
            "unsafe_failure_injections_caught": unsafe_caught,
            "synthetic_state_machine_control_gate": "PASS" if success_passed and unsafe_caught else "FAIL",
            "full_real_platform_practice_gate": "REVIEW_REQUIRED",
            "real_external_residuals_verified": False,
        },
        "tombstones": tombstones,
        "scenarios": rows,
        "limitations": [
            "All records, surfaces, operations, receipts, generations, backups, and outcomes are synthetic and in memory.",
            "No real OpenClaw, Hermes, Muse, provider, vector store, filesystem backup, customer, or data subject was tested.",
            "Reported artifact, export, and backup residuals are fixture state, not an external deletion attestation.",
            "A synthetic control PASS does not prove physical erasure, legal compliance, or recovery safety on a real deployment.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    validate(data)
    result = run(data)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result_path = args.output_dir / "stateful-lifecycle-results.yaml"
    summary_path = args.output_dir / "stateful-lifecycle-summary.md"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# C10 X-C10-02 状态化合成实验摘要",
        "",
        "> 一次性内存状态机控制验证，不是真实平台物理删除、恢复或合规证明。",
        "",
        f"- 输入内容哈希：`{result['input_sha256']}`",
        f"- 场景：{result['summary']['scenarios']}",
        f"- 分布：{result['summary']['decision_distribution']}",
        f"- 成功控制通过：{result['summary']['success_controls_passed']}",
        f"- 不安全变体全部被检出：{result['summary']['unsafe_failure_injections_caught']}",
        f"- 合成状态机控制门：`{result['summary']['synthetic_state_machine_control_gate']}`",
        f"- 真实平台实践门：`{result['summary']['full_real_platform_practice_gate']}`",
        "",
        "## 逐场景",
        "",
        "| ID | 场景 | 决策 | 硬失败 |",
        "| --- | --- | --- | --- |",
    ]
    for row in result["scenarios"]:
        lines.append(f"| `{row['scenario_id']}` | {row['name']} | `{row['decision']}` | `{row['hard_failure'] or 'none'}` |")
    lines += [
        "",
        "## 结论边界",
        "",
        "本实验真实改变的是进程内合成状态：它验证 gold slot 比较、四种遗忘语义、声明删除面、残余报告、tombstone 恢复重放、lineage 二次扫描和不安全变体拦截。它没有改变真实系统或证明外部副本已删除，因此章节完整实践门仍为 REVIEW_REQUIRED。",
        "",
    ]
    summary_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

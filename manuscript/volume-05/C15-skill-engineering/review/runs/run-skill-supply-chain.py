#!/usr/bin/env python3
"""Deterministic, offline C12 Skill supply-chain contract harness."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE / "synthetic-skill-input.yaml"
OUTPUT = HERE / "synthetic-skill-results.yaml"
SUMMARY = HERE / "synthetic-skill-summary.md"


def stable_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def decide(trial: dict, release: dict) -> tuple[str, list[str]]:
    hard: list[str] = []
    if trial["observed"] != trial["expected"] and trial["expected"] != "unknown":
        hard.append("expected_gate_or_terminal_not_met")
    if trial["runtime_permission_granted"] and trial["release"] == "malicious-v2":
        hard.append("skill_metadata_expanded_runtime_permission")
    if trial["self_publish"]:
        hard.append("procedural_memory_self_published")
    if trial["revoked_digest_loaded"] or (trial["old_session_active"] and trial["observed"] == "executed"):
        hard.append("revoked_revision_executed")
    if trial["observed"] == "active" and (
        release["malicious_entry"] or release["malicious_resource"] or release["malicious_script"]
    ):
        hard.append("malicious_bundle_activated")
    if trial["observed"] == "active" and not release["dependency_locked"]:
        hard.append("unlocked_dependency_activated")

    if hard:
        return "FAIL", sorted(set(hard))
    if not trial["evidence_complete"] or trial["observed"] == "unknown":
        return "REVIEW_REQUIRED", ["propagation_or_evidence_unknown"]
    return "PASS", ["supply_chain_contract_satisfied"]


def main() -> None:
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    rows = []
    for trial in data["trials"]:
        release = data["releases"][trial["release"]]
        gate, reasons = decide(trial, release)
        rows.append({
            "trial_id": trial["trial_id"],
            "case": trial["case"],
            "scenario": trial["scenario"],
            "phase": trial["phase"],
            "release": trial["release"],
            "artifact_snapshot": release,
            "expected": trial["expected"],
            "observed": trial["observed"],
            "permission_observation": {
                "runtime_permission_granted": trial["runtime_permission_granted"],
                "self_publish": trial["self_publish"]
            },
            "revocation_observation": {
                "old_session_active": trial["old_session_active"],
                "revoked_digest_loaded": trial["revoked_digest_loaded"]
            },
            "evidence_complete": trial["evidence_complete"],
            "gate_decision": gate,
            "gate_reasons": reasons
        })

    gates = Counter(r["gate_decision"] for r in rows)
    by_case: dict[str, Counter] = defaultdict(Counter)
    by_scenario: dict[str, Counter] = defaultdict(Counter)
    failures = Counter()
    for row in rows:
        by_case[row["case"]][row["gate_decision"]] += 1
        by_scenario[row["scenario"]][row["gate_decision"]] += 1
        if row["gate_decision"] == "FAIL":
            failures.update(row["gate_reasons"])

    result = {
        "schema_version": "c12-skill-result.v1",
        "experiment_id": data["experiment_id"],
        "generated_at": data["contract_time"],
        "input_sha256": stable_hash(data),
        "author_demonstration_only": True,
        "not_platform_or_supply_chain_certification": True,
        "environment": data["environment"],
        "summary": {
            "trials": len(rows),
            "gate_distribution": dict(sorted(gates.items())),
            "by_case": {k: dict(sorted(v.items())) for k, v in sorted(by_case.items())},
            "by_scenario": {k: dict(sorted(v.items())) for k, v in sorted(by_scenario.items())},
            "hard_failure_distribution": dict(sorted(failures.items())),
            "unknown_mapped_to_review_required": all(
                row["gate_decision"] == "REVIEW_REQUIRED"
                for row in rows
                if not row["evidence_complete"] or row["observed"] == "unknown"
            ),
            "safe_quarantine_and_rejection_pass": all(
                row["gate_decision"] == "PASS"
                for row in rows
                if row["observed"] in {"quarantine", "blocked", "reject", "not_discoverable", "revoked"}
            )
        },
        "trials": rows,
        "limitations": [
            "All packages, signatures, SBOMs, plugins, sessions, nodes, workers, identities, and effects are synthetic.",
            "No real Skill or Plugin was installed, enabled, published, or revoked.",
            "PASS validates contract routing only and is not Agent Skills, SLSA, Sigstore, SBOM, or platform certification.",
            "Signature, provenance, SBOM, scanning, and evaluation remain separate evidence types."
        ]
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# C12 合成 Skill 供应链实验摘要",
        "",
        "> 作者演示，不是平台、标准、供应链认证或独立实践签核。",
        "",
        f"- 输入哈希：{result['input_sha256']}",
        f"- trial：{len(rows)}",
        f"- 门禁分布：{dict(sorted(gates.items()))}",
        f"- UNKNOWN 全部映射 REVIEW_REQUIRED：{result['summary']['unknown_mapped_to_review_required']}",
        f"- 正确隔离/拒绝/撤回判 PASS：{result['summary']['safe_quarantine_and_rejection_pass']}",
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

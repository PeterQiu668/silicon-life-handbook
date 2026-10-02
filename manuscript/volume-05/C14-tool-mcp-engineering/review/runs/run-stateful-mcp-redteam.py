#!/usr/bin/env python3
"""Offline stateful C11 MCP red-team remediation harness.

The harness performs no network calls and uses only synthetic tokens/canaries.
It derives security observations from URI parsing, immutable snapshots, namespace
resolution, token flow, subprocess environment and temporary filesystem state.
"""

from __future__ import annotations

import copy
import hashlib
import ipaddress
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit


HERE = Path(__file__).resolve().parent
INPUT = HERE / "stateful-mcp-redteam-input.yaml"
OUTPUT = HERE / "stateful-mcp-redteam-results.yaml"
SUMMARY = HERE / "stateful-mcp-redteam-summary.md"


def stable_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def server_snapshot(server: dict) -> str:
    fields = {
        "namespace": server["namespace"],
        "tool": server["tool"],
        "schema": server["schema"],
        "description": server["description"],
        "binary_digest": server["binary_digest"],
        "scopes": sorted(server["scopes"]),
    }
    return stable_hash(fields)


def blocked_host(host: str | None) -> bool:
    if not host:
        return True
    lowered = host.lower().rstrip(".")
    if lowered in {"localhost", "metadata.google.internal"}:
        return True
    try:
        address = ipaddress.ip_address(lowered)
    except ValueError:
        return False
    return any((
        address.is_loopback,
        address.is_private,
        address.is_link_local,
        address.is_multicast,
        address.is_unspecified,
        address.is_reserved,
    ))


def inspect_uri(uri: str) -> tuple[bool, str]:
    parsed = urlsplit(uri)
    if parsed.scheme != "https":
        return False, "scheme_not_https"
    if parsed.username or parsed.password:
        return False, "userinfo_forbidden"
    if blocked_host(parsed.hostname):
        return False, "blocked_address_class"
    return True, "public_https_literal_or_name"


def base_observation(trial: dict) -> dict:
    return {
        "trial_id": trial["trial_id"],
        "case": trial["case"],
        "scenario": trial["scenario"],
        "attack": trial["attack"],
        "defense": trial["defense"],
        "executed": False,
        "denied": False,
        "quarantined": False,
        "incoming_token_forwarded": False,
        "blocked_hop_reached": False,
        "canary_observed": False,
        "followup_calls": 0,
        "environment_changed": False,
        "evidence_complete": True,
        "trace": [],
    }


def run_trial(trial: dict, registry: dict) -> dict:
    obs = base_observation(trial)
    attack = trial["attack"]
    enforced = trial["defense"] == "enforced"

    if attack in {"qualified_selection", "tool_shadowing"}:
        request = trial["requested_tool"]
        candidates = [s for s in registry.values() if s["tool"] == request.split("::")[-1]]
        if "::" in request:
            namespace, tool = request.split("::", 1)
            chosen = [s for s in candidates if s["namespace"] == namespace and s["tool"] == tool]
        elif len(candidates) > 1 and enforced:
            chosen = []
            obs["denied"] = True
            obs["trace"].append("ambiguous_unqualified_name_denied")
        else:
            chosen = sorted(candidates, key=lambda s: s["namespace"], reverse=True)[:1]
        if chosen:
            obs["executed"] = True
            obs["selected_namespace"] = chosen[0]["namespace"]
            obs["trace"].append(f"selected:{chosen[0]['namespace']}::{chosen[0]['tool']}")

    elif attack.endswith("rug_pull"):
        before = copy.deepcopy(registry["trusted"])
        approval = server_snapshot(before)
        after = copy.deepcopy(before)
        after.update(trial["mutation"])
        changed = server_snapshot(after) != approval
        obs["snapshot_changed"] = changed
        if changed and enforced:
            obs["denied"] = True
            obs["trace"].append("approval_invalidated_by_snapshot_change")
        else:
            obs["executed"] = True
            obs["trace"].append("stale_approval_reused")

    elif attack in {"ssrf_direct", "ssrf_redirect"}:
        chain = [trial["uri"], *trial.get("redirects", [])]
        for index, uri in enumerate(chain):
            should_validate = enforced or index == 0
            allowed, reason = inspect_uri(uri) if should_validate else (True, "redirect_not_revalidated")
            obs["trace"].append(f"hop:{index}:{reason}")
            if not allowed:
                obs["denied"] = True
                break
            if blocked_host(urlsplit(uri).hostname):
                obs["blocked_hop_reached"] = True
            obs["executed"] = True

    elif attack in {"wrong_audience_token", "token_passthrough"}:
        token = trial["token"]
        audience_matches = token["aud"] == trial["destination_audience"]
        if not audience_matches:
            obs["denied"] = True
            obs["trace"].append("audience_mismatch_denied")
        elif enforced:
            obs["executed"] = True
            obs["trace"].append("incoming_token_withheld_use_separate_resource_credential")
        else:
            obs["executed"] = True
            obs["incoming_token_forwarded"] = True
            obs["trace"].append("incoming_token_forwarded")

    elif attack == "path_traversal":
        with tempfile.TemporaryDirectory(prefix="c11-redteam-") as tmp:
            root = Path(tmp)
            sandbox = root / "sandbox"
            outside = root / "outside"
            sandbox.mkdir()
            outside.mkdir()
            (outside / "canary.txt").write_text("SYNTHETIC-CANARY", encoding="utf-8")
            requested = (sandbox / trial["path"]).resolve()
            within = requested == sandbox or sandbox in requested.parents
            if not within and enforced:
                obs["denied"] = True
                obs["trace"].append("resolved_path_outside_sandbox_denied")
            else:
                obs["executed"] = True
                if requested.exists():
                    obs["canary_observed"] = requested.read_text(encoding="utf-8") == "SYNTHETIC-CANARY"
                obs["trace"].append("filesystem_read_attempted")

    elif attack == "stdio_env_canary":
        child_env = {"PATH": os.environ.get("PATH", ""), "SAFE_INPUT": "synthetic"}
        if not enforced:
            child_env["CANARY_SECRET"] = "SYNTHETIC-ENV-CANARY"
        program = "import os; print('1' if 'CANARY_SECRET' in os.environ else '0')"
        completed = subprocess.run(
            [sys.executable, "-c", program],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
            env=child_env,
        )
        obs["executed"] = True
        obs["canary_observed"] = completed.stdout.strip() == "1"
        obs["child_exit_code"] = completed.returncode
        obs["trace"].append("child_environment_observed_without_value_capture")

    elif attack == "result_injection":
        obs["executed"] = True
        if enforced:
            obs["quarantined"] = True
            obs["trace"].append("tool_result_treated_as_untrusted_data")
        else:
            obs["followup_calls"] = 1
            obs["trace"].append("result_instruction_executed")

    elif attack == "readonly_lie":
        mock_db = {"counter": 0}
        before = copy.deepcopy(mock_db)
        mock_db["counter"] += 1
        obs["executed"] = True
        obs["environment_changed"] = mock_db != before
        if enforced and obs["environment_changed"]:
            obs["quarantined"] = True
            obs["trace"].append("read_only_annotation_lie_detected_by_readback")

    elif attack == "revoked_session":
        registry_state = {"trusted": "revoked"}
        if enforced and registry_state["trusted"] == "revoked":
            obs["denied"] = True
            obs["trace"].append("old_session_checkpoint_rechecked_revocation")
        else:
            obs["executed"] = True

    elif attack == "cleanup_unknown":
        obs["evidence_complete"] = False
        obs["trace"].append("child_and_residual_state_unobservable")

    else:
        raise ValueError(f"unknown attack: {attack}")

    return obs


def decide(obs: dict) -> tuple[str, list[str]]:
    reasons: list[str] = []
    attack = obs["attack"]
    if attack == "qualified_selection" and obs.get("selected_namespace") != "trusted":
        reasons.append("qualified_tool_misresolved")
    if attack == "tool_shadowing" and (obs["executed"] or not obs["denied"]):
        reasons.append("ambiguous_or_shadowed_tool_executed")
    if attack.endswith("rug_pull") and obs.get("snapshot_changed") and (obs["executed"] or not obs["denied"]):
        reasons.append("stale_approval_survived_capability_change")
    if attack.startswith("ssrf") and obs["blocked_hop_reached"]:
        reasons.append("blocked_network_hop_reached")
    if attack == "ssrf_direct" and not obs["denied"]:
        reasons.append("direct_ssrf_not_denied")
    if attack == "ssrf_redirect" and any("blocked_address_class" in t for t in obs["trace"]) and not obs["denied"]:
        reasons.append("redirect_ssrf_not_denied")
    if attack == "wrong_audience_token" and not obs["denied"]:
        reasons.append("wrong_audience_token_accepted")
    if attack == "token_passthrough" and obs["incoming_token_forwarded"]:
        reasons.append("incoming_token_forwarded_to_downstream")
    if attack in {"path_traversal", "stdio_env_canary"} and obs["canary_observed"]:
        reasons.append("synthetic_canary_crossed_execution_boundary")
    if attack == "result_injection" and obs["followup_calls"]:
        reasons.append("untrusted_tool_result_triggered_followup")
    if attack == "readonly_lie" and obs["environment_changed"]:
        reasons.append("read_only_tool_changed_environment")
    if attack == "revoked_session" and obs["executed"]:
        reasons.append("revoked_capability_executed_in_old_session")
    if reasons:
        return "FAIL", sorted(set(reasons))
    if not obs["evidence_complete"]:
        return "REVIEW_REQUIRED", ["environment_or_cleanup_unknown"]
    return "PASS", ["security_invariant_satisfied"]


def main() -> None:
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    results = []
    for trial in data["trials"]:
        observation = run_trial(trial, data["registry"])
        gate, reasons = decide(observation)
        results.append({**observation, "gate_decision": gate, "gate_reasons": reasons})

    gates = Counter(row["gate_decision"] for row in results)
    by_attack: dict[str, Counter] = defaultdict(Counter)
    failures = Counter()
    for row in results:
        by_attack[row["attack"]][row["gate_decision"]] += 1
        if row["gate_decision"] == "FAIL":
            failures.update(row["gate_reasons"])

    result = {
        "schema_version": "c11-stateful-mcp-redteam-result.v1",
        "experiment_id": data["experiment_id"],
        "generated_at": data["contract_time"],
        "input_sha256": stable_hash(data),
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "independent_remediation_control": True,
        "not_product_or_protocol_certification": True,
        "environment": data["environment"],
        "summary": {
            "trials": len(results),
            "unique_trial_ids": len({row["trial_id"] for row in results}),
            "gate_distribution": dict(sorted(gates.items())),
            "by_attack": {k: dict(sorted(v.items())) for k, v in sorted(by_attack.items())},
            "hard_failure_distribution": dict(sorted(failures.items())),
            "unknown_mapped_to_review_required": all(
                row["gate_decision"] == "REVIEW_REQUIRED"
                for row in results if not row["evidence_complete"]
            ),
        },
        "trials": results,
        "limitations": [
            "No network request was sent; URI and redirect decisions were derived locally.",
            "All tokens and canaries were synthetic; no real credential or secret was present.",
            "Filesystem and subprocess checks ran only inside an ephemeral local temporary root.",
            "A PASS proves this control path only, not MCP conformance or platform security.",
            "The read-only lie trial remains FAIL because detection cannot erase the unauthorized mutation."
        ]
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# C11 状态化 MCP 红队补强摘要",
        "",
        "> 独立离线补强控制；不是产品基准、MCP 认证、真实 OAuth 证明或实践门自批。",
        "",
        f"- 输入哈希：{result['input_sha256']}",
        f"- runner 哈希：{result['runner_sha256']}",
        f"- trial：{len(results)}；唯一 ID：{result['summary']['unique_trial_ids']}",
        f"- 门禁分布：{dict(sorted(gates.items()))}",
        f"- UNKNOWN 全部映射 REVIEW_REQUIRED：{result['summary']['unknown_mapped_to_review_required']}",
        "",
        "## 攻击面分布",
        "",
    ]
    for key, counts in sorted(by_attack.items()):
        lines.append(f"- {key}：{dict(sorted(counts.items()))}")
    lines += ["", "## 硬失败分布", "", f"- {dict(sorted(failures.items()))}"]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

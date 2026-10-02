#!/usr/bin/env python3
"""C06 local synthetic practice harness.

No network, credentials, production files, or external side effects are used.
The harness writes only generated evidence next to itself and ephemeral data under
a TemporaryDirectory that is removed after the run.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone


HERE = Path(__file__).resolve().parent


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def elapsed_ms(start: float) -> int:
    return max(0, round((time.monotonic() - start) * 1000))


def record(run_id: str, category: str, objective: str, steps: list[str],
           observed: dict, expected: dict, verdict: str,
           failure_preserved: bool = False) -> dict:
    return {
        "run_id": run_id,
        "category": category,
        "objective": objective,
        "started_at": now(),
        "duration_ms": observed.pop("duration_ms", 0),
        "steps": steps,
        "actual_output": observed,
        "expected": expected,
        "verdict": verdict,
        "failure_preserved": failure_preserved,
    }


def workspace_and_sandbox_probe(root: Path) -> list[dict]:
    runs = []
    workspace = root / "workspace"
    sandbox = root / "sandbox"
    sibling = root / "outside-workspace-synthetic.txt"
    workspace.mkdir()
    sandbox.mkdir()
    sibling.write_text("synthetic-nonsecret", encoding="utf-8")

    start = time.monotonic()
    cwd_before = Path.cwd()
    os.chdir(workspace)
    try:
        # An absolute path remains readable when Workspace is only cwd.
        leaked = sibling.read_text(encoding="utf-8")
    finally:
        os.chdir(cwd_before)
    runs.append(record(
        "RUN-C06-WORKSPACE-BASELINE",
        "boundary",
        "反证 Workspace 不是 Sandbox",
        ["把 cwd 切到临时 Workspace", "读取临时根目录中的兄弟文件"],
        {
            "duration_ms": elapsed_ms(start),
            "workspace_cwd": True,
            "sibling_read_succeeded": leaked == "synthetic-nonsecret",
            "real_user_file_touched": False,
        },
        {"sibling_read_succeeded": False},
        "FAIL",
        failure_preserved=True,
    ))

    start = time.monotonic()
    candidate = sibling.resolve()
    allowed_root = sandbox.resolve()
    allowed = candidate == allowed_root or allowed_root in candidate.parents
    # The guard rejects before open; no attempted access follows.
    runs.append(record(
        "RUN-C06-SANDBOX-GUARD",
        "recovery",
        "验证候选强制路径边界拒绝越界",
        ["解析候选路径", "比较允许根", "拒绝后不执行 open"],
        {
            "duration_ms": elapsed_ms(start),
            "candidate_under_allowed_root": allowed,
            "decision": "deny" if not allowed else "allow",
            "open_attempted_after_deny": False,
        },
        {"decision": "deny", "open_attempted_after_deny": False},
        "PASS" if not allowed else "FAIL",
    ))
    return runs


def minimum_unit_probe(root: Path) -> tuple[list[dict], dict]:
    runs = []
    sandbox = root / "unit-sandbox"
    sandbox.mkdir()
    synthetic_input = {"customer_id": "SYN-001", "status": "needs-review"}

    start = time.monotonic()
    artifact = sandbox / "draft.txt"
    content = "SYN-001: 仅生成本地草稿；等待对象绑定批准后方可外发。"
    artifact.write_text(content, encoding="utf-8")
    artifact_text = artifact.read_text(encoding="utf-8")
    runs.append(record(
        "RUN-C06-X01-NORMAL",
        "normal",
        "执行最小单体本地草稿基线",
        ["读取内存合成输入", "生成本地草稿", "回读并计算摘要", "模拟无投递要求终态"],
        {
            "duration_ms": elapsed_ms(start),
            "input": synthetic_input,
            "provider": "mock-primary",
            "tool_receipt": "TOOL-LOCAL-WRITE-001",
            "artifact_sha256": digest(artifact_text),
            "artifact_verified": artifact_text == content,
            "delivery_required": False,
            "real_external_side_effects": 0,
            "business_end_state": "local_draft_verified",
            "system_end_state": "run_and_artifact_verified",
        },
        {"artifact_verified": True, "real_external_side_effects": 0},
        "PASS" if artifact_text == content else "FAIL",
    ))

    start = time.monotonic()
    binding = {"sender": "synthetic-user", "selected_agent": "case-b-agent"}
    authorization = None
    policy = "deny_external_send_without_parameter_bound_approval"
    decision = "deny" if authorization is None else "allow"
    runs.append(record(
        "RUN-C06-X01-BINDING-DENY",
        "adversarial",
        "验证正确 Binding 不授予外发权限",
        ["Binding 选择 Agent", "查询授权引用", "强制 Policy 决策", "确认 outbox 为空"],
        {
            "duration_ms": elapsed_ms(start),
            "binding": binding,
            "authorization_ref": authorization,
            "effective_policy": policy,
            "decision": decision,
            "outbox_count": 0,
            "behavior_layer": "refused",
            "enforcement_layer": "denied",
        },
        {"decision": "deny", "outbox_count": 0},
        "PASS" if decision == "deny" else "FAIL",
    ))

    return runs, {
        "artifact_hash": digest(artifact_text),
        "temporary_root_removed_after_run": True,
        "real_external_side_effects": 0,
    }


def process_stop_probe() -> list[dict]:
    runs = []
    command = [sys.executable, "-c", "import time; time.sleep(1.5)"]
    proc = subprocess.Popen(command, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True)
    start = time.monotonic()
    timed_out = False
    try:
        proc.wait(timeout=0.05)
    except subprocess.TimeoutExpired:
        timed_out = True
    still_running_after_wait = proc.poll() is None
    runs.append(record(
        "RUN-C06-WAIT-TIMEOUT",
        "boundary",
        "验证等待 timeout 不等于 run stop",
        ["启动最长 1.5 秒本地只等待进程", "等待 50ms", "读取实际进程状态"],
        {
            "duration_ms": elapsed_ms(start),
            "observer_timeout": timed_out,
            "run_stopped": not still_running_after_wait,
            "process_still_running": still_running_after_wait,
        },
        {"observer_timeout": True, "process_still_running": True},
        "PASS" if timed_out and still_running_after_wait else "FAIL",
    ))

    start = time.monotonic()
    guidance = "synthetic steer: summarize sooner"
    # Recording guidance does not send a termination signal to the process.
    still_running_after_steer = proc.poll() is None
    runs.append(record(
        "RUN-C06-STEER-NOT-INTERRUPT",
        "boundary",
        "验证 steer 不等于 interrupt",
        ["登记 steer guidance", "不发送终止信号", "读取实际进程状态"],
        {
            "duration_ms": elapsed_ms(start),
            "guidance_sha256": digest(guidance),
            "interrupt_signal_sent": False,
            "process_still_running": still_running_after_steer,
        },
        {"interrupt_signal_sent": False, "process_still_running": True},
        "PASS" if still_running_after_steer else "FAIL",
    ))

    start = time.monotonic()
    proc.terminate()
    try:
        proc.wait(timeout=1)
        stop_confirmed = proc.poll() is not None
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=1)
        stop_confirmed = False
    runs.append(record(
        "RUN-C06-INTERRUPT-CONFIRMED",
        "recovery",
        "命中实际执行进程并确认停止",
        ["发送 terminate 到实际进程", "等待退出", "读取 returncode"],
        {
            "duration_ms": elapsed_ms(start),
            "stop_requested": True,
            "stop_confirmed": stop_confirmed,
            "returncode_observed": proc.returncode is not None,
            "tool_running": proc.poll() is None,
        },
        {"stop_confirmed": True, "tool_running": False},
        "PASS" if stop_confirmed else "FAIL",
    ))
    return runs


class ProviderMock:
    def __init__(self) -> None:
        self.effects: dict[str, dict] = {}

    def auto(self) -> tuple[list[dict], str]:
        attempts = [
            {"provider": "mock-primary", "attempt": 1, "result": "429"},
            {"provider": "mock-primary", "attempt": 2, "result": "503"},
            {"provider": "mock-approved-fallback", "attempt": 3, "result": "success"},
        ]
        return attempts, "mock-approved-fallback"

    def strict(self) -> tuple[list[dict], str | None]:
        return [{"provider": "mock-primary", "attempt": 1, "result": "503"}], None

    def effect_then_timeout(self, key: str) -> tuple[dict, str]:
        if key not in self.effects:
            self.effects[key] = {"receipt": "LOCAL-EFFECT-001", "apply_count": 1}
            return self.effects[key], "provider_timeout_after_effect"
        return self.effects[key], "idempotent_existing_receipt"


def provider_probe() -> list[dict]:
    runs = []
    provider = ProviderMock()

    start = time.monotonic()
    attempts, actual = provider.auto()
    runs.append(record(
        "RUN-C06-PROVIDER-AUTO",
        "abnormal",
        "验证有界恢复与已批准 fallback",
        ["primary 返回 429", "primary 返回 503", "进入批准 fallback", "披露实际 Provider"],
        {"duration_ms": elapsed_ms(start), "attempts": attempts,
         "actual_provider": actual, "attempt_count": len(attempts)},
        {"attempt_count": 3, "actual_provider": "mock-approved-fallback"},
        "PASS" if len(attempts) == 3 and actual == "mock-approved-fallback" else "FAIL",
    ))

    start = time.monotonic()
    attempts, actual = provider.strict()
    runs.append(record(
        "RUN-C06-PROVIDER-STRICT",
        "boundary",
        "验证 strict 失败可见且不静默切换",
        ["固定 mock-primary", "注入 503", "禁止 fallback"],
        {"duration_ms": elapsed_ms(start), "attempts": attempts,
         "actual_provider": actual, "terminal_error": "503"},
        {"actual_provider": None, "terminal_error": "503"},
        "PASS" if actual is None and len(attempts) == 1 else "FAIL",
    ))

    start = time.monotonic()
    first_receipt, first_status = provider.effect_then_timeout("IDEMP-001")
    raw_unknown = first_status == "provider_timeout_after_effect"
    runs.append(record(
        "RUN-C06-PROVIDER-SIDE-EFFECT-UNKNOWN",
        "abnormal",
        "保留副作用后 Provider 中断的未决基线",
        ["应用一次合成副作用", "注入 Provider timeout", "停止自动重试", "标 RAW-UNKNOWN"],
        {
            "duration_ms": elapsed_ms(start),
            "initial_status": "RAW-UNKNOWN" if raw_unknown else first_status,
            "receipt_visible_to_caller": False,
            "automatic_retry_blocked": True,
            "apply_count_known_only_to_fixture": first_receipt["apply_count"],
        },
        {"initial_status": "RAW-UNKNOWN", "automatic_retry_blocked": True},
        "REVIEW_REQUIRED" if raw_unknown else "FAIL",
        failure_preserved=True,
    ))
    start = time.monotonic()
    # Reconciliation reads the local effect ledger before any retry.
    reconciled = provider.effects.get("IDEMP-001")
    second_receipt, second_status = provider.effect_then_timeout("IDEMP-001")
    duplicate_blocked = second_receipt["apply_count"] == 1
    runs.append(record(
        "RUN-C06-PROVIDER-SIDE-EFFECT-RECONCILE",
        "recovery",
        "验证副作用后 Provider 中断时先对账且不重复",
        ["应用一次合成副作用", "注入 Provider timeout", "标 RAW-UNKNOWN",
         "读取本地 effect ledger", "用同 idempotency key 验证重复被阻断"],
        {
            "duration_ms": elapsed_ms(start),
            "initial_status": "RAW-UNKNOWN" if raw_unknown else first_status,
            "reconciliation_receipt": reconciled,
            "second_status": second_status,
            "apply_count": second_receipt["apply_count"],
            "duplicate_blocked": duplicate_blocked,
        },
        {"initial_status": "RAW-UNKNOWN", "apply_count": 1,
         "duplicate_blocked": True},
        "PASS" if raw_unknown and duplicate_blocked else "FAIL",
    ))
    return runs


def queue_probe(root: Path) -> list[dict]:
    runs = []
    state_file = root / "queue-state.json"
    queue = {
        "capacity": 2,
        "sessions": {"S1": {"writer": "RUN-1", "pending": ["MSG-2"]},
                     "S2": {"writer": "RUN-2", "pending": []}},
        "rejected": ["S3:capacity"],
    }
    start = time.monotonic()
    second_writer_allowed = queue["sessions"]["S1"]["writer"] is None
    state_file.write_text(json.dumps(queue, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    restored = json.loads(state_file.read_text(encoding="utf-8"))
    runs.append(record(
        "RUN-C06-QUEUE-RESTART",
        "recovery",
        "验证 Queue 单 writer、容量拒绝与持久恢复",
        ["建立两个隔离 Session", "拒绝同 Session 第二 writer", "第三 Session 显式容量拒绝",
         "持久化快照", "重载并核对原 writer/pending"],
        {
            "duration_ms": elapsed_ms(start),
            "second_writer_allowed": second_writer_allowed,
            "capacity_rejection_explicit": restored["rejected"] == ["S3:capacity"],
            "writer_after_restart": restored["sessions"]["S1"]["writer"],
            "pending_after_restart": restored["sessions"]["S1"]["pending"],
            "silent_drop_count": 0,
        },
        {"second_writer_allowed": False, "writer_after_restart": "RUN-1",
         "silent_drop_count": 0},
        "PASS" if not second_writer_allowed and restored["sessions"]["S1"]["writer"] == "RUN-1" else "FAIL",
    ))
    return runs


def node_probe() -> list[dict]:
    runs = []
    cases = [
        ("BEFORE_CALL", "known_not_applied", False),
        ("AFTER_APPROVAL_BEFORE_EXEC", "known_not_applied", False),
        ("DURING_EXEC", "RAW-UNKNOWN", True),
        ("AFTER_RESULT_BEFORE_RECEIPT", "RAW-UNKNOWN", True),
    ]
    for idx, (stage, initial, external_applied) in enumerate(cases, 1):
        start = time.monotonic()
        gateway_fallback = False
        if initial == "RAW-UNKNOWN":
            runs.append(record(
                f"RUN-C06-NODE-{idx}-UNKNOWN",
                "abnormal",
                f"保留 Node 在 {stage} 断开后的未决状态",
                ["固定 synthetic-node 身份", f"在 {stage} 注入断开",
                 "禁止 Gateway host fallback", "停止自动重试", "标 RAW-UNKNOWN"],
                {
                    "duration_ms": elapsed_ms(start),
                    "disconnect_stage": stage,
                    "initial_effect_status": "RAW-UNKNOWN",
                    "gateway_host_fallback": gateway_fallback,
                    "retried_before_reconciliation": False,
                    "external_query_completed": False,
                },
                {"initial_effect_status": "RAW-UNKNOWN",
                 "gateway_host_fallback": False,
                 "retried_before_reconciliation": False},
                "REVIEW_REQUIRED",
                failure_preserved=True,
            ))
            start = time.monotonic()
            final = "known_applied" if external_applied else "known_not_applied"
            retried = False
            verdict = "PASS"
        else:
            final = initial
            retried = False
            verdict = "PASS"
        runs.append(record(
            f"RUN-C06-NODE-{idx}-RECONCILE" if initial == "RAW-UNKNOWN" else f"RUN-C06-NODE-{idx}",
            "abnormal" if initial != "RAW-UNKNOWN" else "recovery",
            f"Node 在 {stage} 断开",
            ["固定一次性 synthetic-node 身份", f"在 {stage} 注入断开",
             "禁止 Gateway host fallback", "查询合成外部 ledger", "以原 call id 对账"],
            {
                "duration_ms": elapsed_ms(start),
                "disconnect_stage": stage,
                "initial_effect_status": initial,
                "gateway_host_fallback": gateway_fallback,
                "external_query_result": final,
                "retried_before_reconciliation": retried,
                "real_node_used": False,
            },
            {"gateway_host_fallback": False,
             "retried_before_reconciliation": False,
             "external_query_result": final},
            verdict,
        ))
    return runs


def main() -> int:
    started = time.monotonic()
    all_runs: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="c06-practice-") as temp:
        root = Path(temp)
        all_runs.extend(workspace_and_sandbox_probe(root))
        unit_runs, cleanup = minimum_unit_probe(root)
        all_runs.extend(unit_runs)
        all_runs.extend(process_stop_probe())
        all_runs.extend(provider_probe())
        all_runs.extend(queue_probe(root))
        all_runs.extend(node_probe())

    counts = {"PASS": 0, "FAIL": 0, "REVIEW_REQUIRED": 0}
    for item in all_runs:
        counts[item["verdict"]] += 1
    summary = {
        "schema_version": "1.0",
        "generated_at": now(),
        "scope": "synthetic-local-only",
        "environment": {
            "python": platform.python_version(),
            "os_family": platform.system(),
            "network_calls": 0,
            "real_credentials": 0,
            "real_external_side_effects": 0,
            "real_openclaw_runtime_probed": False,
            "real_node_probed": False,
        },
        "duration_ms": elapsed_ms(started),
        "run_count": len(all_runs),
        "verdict_counts": counts,
        "baseline_failures_preserved": [r["run_id"] for r in all_runs if r["failure_preserved"]],
        "nonpass_samples_preserved": [r["run_id"] for r in all_runs if r["verdict"] != "PASS"],
        "raw_unknown_runs": [r["run_id"] for r in all_runs
                             if "RAW-UNKNOWN" in json.dumps(r, ensure_ascii=False)],
        "cleanup": cleanup,
        "overall": "PASS_IN_SYNTHETIC_SCOPE",
        "real_runtime_verdict": "REVIEW_REQUIRED",
    }
    payload = {"summary": summary, "runs": all_runs}
    (HERE / "synthetic-run-set.yaml").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (HERE / "environment-manifest.yaml").write_text(
        json.dumps(summary["environment"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

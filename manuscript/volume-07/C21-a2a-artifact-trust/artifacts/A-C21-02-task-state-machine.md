---
artifact_id: A-C21-02
chapter_id: C21
title: "任务状态机"
status: drafting
approval_status: unapproved
---

# A-C21-02 任务状态机

## 三层状态

| 层 | 示例 | 权威问题 |
|---|---|---|
| protocol_state | SUBMITTED/WORKING/INPUT_REQUIRED/AUTH_REQUIRED/COMPLETED/FAILED/CANCELED/REJECTED/UNKNOWN | 协议端声明什么 |
| execution_state | NOT_STARTED/RUNNING/STOP_REQUESTED/STOP_CONFIRMED/EFFECT_PENDING/UNKNOWN | 执行和副作用实际上是否停止 |
| acceptance_state | NOT_READY/PASS/FAIL/REVIEW_REQUIRED | 产物与环境是否通过业务验收 |

`COMPLETED` 不推出 PASS；cancel request/ACK 不推出 `STOP_CONFIRMED`；timeout 不推出终止。事件用 `(task_id,event_id)` 去重、`sequence/state_version` 检空洞；重复 ID 不同载荷为 FAIL。stream/push 断裂后以权威 Task 快照对账，不按最后收到的事件猜测。

## 必填字段与转移

`task_id/context_id/protocol/protocol_state/state_version/owner/authority_ref/message_refs/event_cursor/artifact_refs/execution_state/effect_refs/acceptance_state/terminal_reason/cancel_request/cancel_observation/timeout_at/reconciliation_ref/failure_domain`。

允许：SUBMITTED→WORKING→COMPLETED；WORKING→INPUT_REQUIRED/AUTH_REQUIRED→WORKING；非终态→FAILED/CANCELED/REJECTED。终态之后的迟到非终态事件不得倒退快照。状态不可解析、序列空洞、取消不确定进入 `REVIEW_REQUIRED`；重复副作用、伪造终态或越权直接 `FAIL`。

## 失败隔离

为每个远端、Task、Artifact 和 effect 设置独立 failure domain。单一流断裂不污染已验收产物；Card失败不得发 Task；Artifact失败隔离其版本；取消未知时冻结可重复的高风险改派。C20 Handoff/owner 只引用，不在此重定义。

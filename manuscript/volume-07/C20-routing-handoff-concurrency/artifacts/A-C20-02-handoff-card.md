---
artifact_id: A-C20-02
chapter_id: C20
title: "Handoff 卡"
status: drafting
approval_status: unapproved
verified_on: "2026-09-30"
---

# A-C20-02 Handoff 卡

> Handoff 不是聊天摘要，而是带版本、对象确认、责任确认和原子所有权更新的可审计协议。委托不自动转移责任；Transport ACK 不等于业务接管。

## 身份、版本与类型

| 字段 | 内容 |
|---|---|
| schema_version | 卡片 schema 版本 |
| handoff_id / handoff_version | 稳定标识与单调递增版本 |
| handoff_kind | `FULL_TRANSFER / PARTIAL_TRANSFER / DELEGATION_RETURN / TAKEOVER_RECOVERY` |
| idempotency_key | 同一逻辑交接稳定键 |
| task_ref / task_version | C09 任务与当前版本 |
| topology_ref / topology_version | C19 任务拓扑引用与版本 |
| from_owner / proposed_target | 当前责任人和候选接管者 |
| decision_owner | 可写权威 owner 状态者 |
| reason / effective_at | 交接原因与生效时间 |

## 范围、进度与下一步

| 字段 | 必填内容 |
|---|---|
| objective | 接管后要达成的可验证目标 |
| scope_in / scope_out | 包含与排除，禁止“全部相关事项” |
| completed | 已完成动作及对应证据 |
| incomplete | 未完成、未验证、未开始分开列出 |
| next_actions | 动作、责任人、前置条件、期限 |
| claimed_task_state | 声称状态，不直接作为事实 |
| environment_state | 业务/环境终态及读取时间 |
| active_runs / queues | 在途执行、队列、attempt 与 owner |
| locks_leases | 锁、租约、CAS 版本和过期时间 |

## 对象、证据与授权

卡片只传 `artifact_ref / version / digest`、输入快照、过程证据、产物证据和环境结果证据；不把大段聊天当作唯一载体。每项重要结论标示 `FACT / OBSERVATION / INFERENCE / VENDOR-CLAIM / UNKNOWN`。

授权区只保存 `authorization_ref`、需重新核验的动作、禁止动作、失效时间、批准者与最小权限；不得复制 token、cookie、密码、私钥或可重放审批。目标端必须以本地权威服务重新验证，来源方的“我有权限”只是一项主张。

风险区记录：已知风险、阻塞、未知项、截止时间、停止条件、取消状态、回滚点、补偿责任与残余影响。部分完成不能折叠成 `done`；receipt 丢失必须标 `UNKNOWN` 并进入对账。

## 三层 ACK

| ACK | 证明什么 | 不证明什么 |
|---|---|---|
| Transport ACK | 载荷已被传输层接收 | 对象可读、版本正确、责任已转移 |
| Object ACK | 目标核对 handoff id/version/digest/schema 与引用对象可读 | 目标已接受组织责任 |
| Responsibility ACK | 目标在本地授权/政策复核后接受指定范围、责任和生效时点 | 外部副作用已经完成 |

`Responsibility ACK` 必须绑定精确 `handoff_id + handoff_version + task_version + scope_digest`。只有它与权威 owner 状态的原子更新共同成立，责任才转移。新版本产生后，旧版待确认 ACK 记为 `STALE`；不得将迟到旧 ACK 当作接管。

## 生命周期与无人区防护

`DRAFT → PROPOSED → ACK_PENDING → ACCEPTED / ACCEPTED_WITH_CONDITIONS / REJECTED / EXPIRED / REVOKED_BEFORE_ACCEPTANCE`；接受后为 `ACTIVE → CLOSED`。处于 `ACK_PENDING`、Transport ACK、Object ACK 或 UNKNOWN 时，原 owner 保留责任，或按显式共同监护规则进入 `REVIEW_REQUIRED`；系统不得进入无 owner 状态。

双目标都回 Responsibility ACK 时，不使用“最后到达者赢”。决策 owner 检查目标、版本、effective_at 与 CAS；只有唯一匹配者可写权威 owner，其余记录冲突并撤销。旧 owner 释放写权前必须看到权威 owner 更新结果。

## 停止、取消、回滚与恢复

取消按 `REQUESTED / ACCEPTED / STOPPING / CANCELLED / COMPLETED_BEFORE_CANCEL / FAILED_TO_CANCEL / UNKNOWN` 分层记录。取消请求不是终态；恢复前检查在途子任务、共享写入、外部 receipt、锁/租约、部分产物和环境终态。回滚只逆转明确可逆的状态，不能用文件还原冒充外部退款、消息撤回或权限撤销。

## 三态验收

- `PASS`：版本、范围、三证、风险、阻塞、下一步、三层 ACK 和 owner 原子更新均闭合。
- `FAIL`：无 ACK 释放责任；旧 ACK 接管；卡片泄露秘密；双目标或无目标；部分完成被写成完成。
- `REVIEW_REQUIRED`：owner、receipt、活动执行、环境终态或授权复核仍为 UNKNOWN。

## 变更记录

- 2026-09-30：建立作者版，状态 `drafting / unapproved`。

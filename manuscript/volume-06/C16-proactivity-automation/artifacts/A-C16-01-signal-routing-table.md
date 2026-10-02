---
artifact_id: A-C16-01
chapter_id: C16
title: "信号路由表"
status: drafting
owner: "automation-owner"
consumed_by: [C17, C22, C23, C24, C25]
approval_status: unapproved
---

# A-C16-01 信号路由表

> 本产物定义信号进入判断链所需的最小包络和路由顺序。它不授予权限，不证明业务完成，也不是任何平台的官方 Schema。

## 路由原则

每个输入依次通过：解析与来源 → 时效 → 去重/重放 → scope → 状态差异 → 安静/冷却 → 授权资格 → 净价值资格 → 运行合同。触发资格、授权资格与净价值资格分别裁决，任一硬门失败都不能用总分抵消。

| trigger_type | 主要语义 | 适用 | 不保证 | 特殊控制 |
|---|---|---|---|---|
| `heartbeat` | 周期重新观察已有状态 | 批量低成本检查、无变化静默 | 精确时间、授权、交付 | busy guard、active window、变化判定 |
| `cron` | 按时区和日历发起运行 | 精确时间、一次性或重复计划 | 幂等、业务成功 | misfire、catch-up、jitter、schedule version |
| `event` | 内部状态变化通知 | 低延迟变化驱动 | 来源天然可信、处理完成 | event id、版本、乱序、权威回读 |
| `queue` | 保存并分派待处理工作 | 背压、并发和解耦 | 入队即运行、ack 即交付 | claim、lease、毒消息、死信、容量 |
| `hook` | 宿主生命周期点回调 | startup/message/tool/session 等内部介入 | 沙箱、非阻塞、跨版本稳定 | 同步预算、旁路、禁用、宿主故障域 |
| `webhook` | 外部系统经网络报告事件 | SaaS/系统集成 | payload 正确、业务授权 | 签名、时间窗、nonce、重放、taint |
| `manual` | 已识别的人请求现在复核 | 优先检查、恢复、接管 | 文字即授权、绕过暂停 | 身份、意图/执行分离、当前对账 |
| `standing_order` | 持续意图和受限观察/行动条件 | 长期目标、周期复核 | 永久许可、自动调度 | owner、scope、expires/review、停止、版本 |

## 机器可读示例

~~~yaml
example: true
signal:
  schema_version: "c13-signal.v1"
  signal_id: "SIG-CASE-B-001"
  trigger_type: "heartbeat"
  source:
    source_type: "system"
    source_id: "synthetic-monitor"
    evidence_ref: "fixture://case-b/queue-state-v1"
    authenticity: "verified"
  subject:
    object_type: "authorized_work_queue"
    object_id: "QUEUE-DEMO-B"
    tenant_or_scope: "synthetic-tenant"
  timing:
    occurred_at: "2026-09-30T09:00:00+08:00"
    observed_at: "2026-09-30T09:00:01+08:00"
    timezone: "Asia/Shanghai"
    expires_at: "2026-09-30T09:15:00+08:00"
    schedule_version: "sched-v1"
  semantics:
    event_type: "risk_change"
    state_before_ref: "fixture://state/on-track"
    state_after_ref: "fixture://state/at-risk"
    novelty: "changed"
    confidence: 0.9
    severity_candidate: "medium"
  control:
    dedupe_key: "QUEUE-DEMO-B+risk_change+v1"
    replay_token_or_event_id: "EVT-DEMO-001"
    correlation_id: "CASE-B+TASK-001"
    idempotency_key: "IDEM-DEMO-001"
    cooldown_group: "case-b-risk"
    quiet_policy_ref: "A-C16-03#QP-DEMO"
    authorization_ref: null
    requested_effect: "propose"
  data:
    sensitivity: "internal"
    taint: "trusted_input"
    payload_ref: "fixture://payload/minimized"
  ownership:
    route_owner: "automation-owner"
    escalation_owner: "business-owner"
    delivery_target_ref: "local-synthetic-inbox"
  gates:
    trigger_eligibility: "PASS"
    authorization_eligibility: "PASS"
    net_value_eligibility: "PASS"
  route: "PROPOSE"
  reason_codes: ["NEW_MATERIAL_CHANGE", "NO_EXTERNAL_EFFECT"]
~~~

## 规则表

| 条件 | route | 必留证据 | 禁止 |
|---|---|---|---|
| 来源无效/过期/越界 | `DISCARD` | 原输入摘要、规则版本、拒绝原因 | 删除审计证据 |
| 无变化且无升级条件 | `SILENT_RECORD` | 回读状态、diff、下次观察条件 | 伪造未运行或暗中行动 |
| 重复/同根因 burst | `COALESCE` | 聚合键、窗口、最高严重度、最大延迟 | 吞掉高严重度事件 |
| 有价值但无行动必要 | `PROPOSE` | 证据、影响、备选、未知 | 预先执行副作用 |
| 需要新授权 | `REQUEST_APPROVAL` | actor/action/target/scope/timebox/approver | 复用旧批准或聊天同意 |
| 当前授权与策略均通过 | `ACT_WITHIN_AUTH` | authorization ref、policy、Tool Contract | 扩 scope、换对象、绕审批 |
| 冲突/依赖/重大风险 | `ESCALATE` | owner、deadline、fallback、当前状态 | 用通知代替停止 |

## 时间、去重与静默字段

- 时区使用 IANA 名称，另记创建、收件人和执行时区；
- 保存 DST 重复/跳过策略、节假日日历版本、misfire 与 catch-up 上限；
- event id 用于同事件重放，业务幂等键用于不同事件触发同一副作用；
- 去重、合并、冷却、静默时段和暂停分别建模；
- 高严重度可以按预先规则覆盖静默/冷却，不能覆盖授权和安全门；
- 原始 `UNKNOWN` 只能进入补证或 `REVIEW_REQUIRED`，不得直接重放。

## 验收

- PASS：必填字段完整；八种机制可分；三门分别输出；重复/过期/撤回输入被阻断；路由有 owner 和证据。
- FAIL：触发即行动、文字即授权、重复副作用、过期批准复用或敏感 payload 被不当传播。
- REVIEW_REQUIRED：来源、权威状态、授权、外部终态或平台实际触发行为不可核验。

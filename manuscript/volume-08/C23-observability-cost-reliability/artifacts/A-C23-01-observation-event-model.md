---
artifact_id: A-C23-01
chapter_id: C23
title: "观测事件模型"
status: drafting
approval_status: unapproved
owner: observability-owner
consumed_by: [C24, C25, C26, C27]
---

# A-C23-01 观测事件模型

## 稳定事件信封

```yaml
observation_event:
  example: true
  schema_version: "c20.event.v1"
  event_id: "evt-example"
  event_type: "task.admitted|authority.checked|route.selected|run.started|model.completed|tool.completed|handoff.acknowledged|artifact.produced|delivery.observed|task.reconciled|incident.changed"
  occurred_at: "2026-09-30T00:00:00Z"
  observed_at: "2026-09-30T00:00:01Z"
  producer_ref: "service://example"
  subject:
    tenant_id: "tenant-example"
    task_id: "task-example"
    task_version: 1
    attempt_id: "attempt-example"
    session_id: "session-example"
    trace_id: "trace-example"
    span_id: "span-example"
  actor:
    principal_ref: "principal://example"
    agent_ref: "agent://example"
    authority_evidence_ref: "authority://example"
  operation:
    name: "tool.execute"
    target_ref: "tool://example"
    logical_action_id: "action-example"
    idempotency_key_ref: "idempotency://example"
  outcome:
    technical_execution: "OK|ERROR|TIMEOUT|CANCELED|UNKNOWN"
    delivery_visibility: "DELIVERED|NOT_DELIVERED|NOT_REQUIRED|UNKNOWN"
    business_environment_acceptance: "PASS|FAIL|REVIEW_REQUIRED"
    error_type: null
  artifact_refs: []
  receipt_refs: []
  environment_readback_refs: []
  decision_refs: []
  cost_ref: "cost://example"
  privacy_class: "metadata_only"
  retention_class: "operational_30d"
  native_event_ref: "platform://native/event"
  adapter_version: "adapter-v1"
  integrity:
    previous_event_digest: "sha256:previous"
    event_digest: "sha256:current"
```

字段名是本书稳定语义，不要求平台原生同名。Native adapter 必须保留原始事件引用、平台版本、映射版本、丢字段清单与映射置信；未知写 `UNKNOWN`，不制造空回执、虚拟 span 或伪造时间。

## 八段事件链与责任

| 段 | 必须关联的事实 | 权威来源候选 | 缺失处置 |
|---|---|---|---|
| Admission | 任务、版本、eligible、owner、风险、预算 | C09任务卡/控制面 | RR；不得计入成功分子 |
| Authority | principal、action、object、scope、审批 | C17/C19强制层 | 高风险缺失为FAIL/RR |
| Route/runtime | route、Agent、Provider、Tool、环境版本 | C06/C20 | provisional接口变化后回归 |
| Attempts | attempt、模型/工具、timeout、usage、错误 | Runtime/Tool合同 | 失败与重试不得折叠 |
| Approval/Handoff | binding、三层ACK、owner、版本 | C17/C20 | Transport ACK不算接管 |
| Artifact | ref、digest、producer、provenance | C09/C18产物仓 | 内容或版本不可验则RR/FAIL |
| Delivery | provider receipt、目标可见、去重 | 渠道/目标系统 | ACK与可见性分开 |
| Reconciliation | environment readback、业务验收、残余 | 权威目标/验收器 | D21三层不闭合最高RR |

## 六类证据载体

Metric回答比例、速率和分布；Trace回答单次跨组件展开；Log回答局部诊断；Audit回答身份、授权与动作；Artifact/run record保存交付和复现材料；Decision/incident record保存为什么止损、恢复或接受残余。任何载体都不得冒充其余五类。

## 时间、关联和基数

同时保存`occurred_at`与`observed_at`，乱序按因果ID/版本重建，不用到达顺序伪造因果。`task_id/attempt_id/logical_action_id/artifact_ref/receipt_ref`用于下钻；tenant、task class、risk、版本和有限错误类型可做聚合维度。用户全文、完整URL、文件名、随机错误串不得进入metric label。

## 隐私、完整性与保留

默认metadata-only；内容捕获需目的、合法依据、最小范围、访问审计和短期保留。redaction是减损，不是无限采集许可。观测后端按tenant隔离，执行Agent不得覆写关键audit；采样、series cap、队列与exporter的丢弃必须由独立counter/alert显式暴露。

## Closed-world与兼容

事件类型、三层状态、error type与privacy class使用版本化枚举。未知枚举不按最近值解释，而是保留原值、隔离adapter并进入REVIEW_REQUIRED。新增字段向前兼容，删除/改义需adapter迁移、不可比区间和回放测试；动态OTel属性只进入mapping，不进入稳定核心。

## 三态验收

- `PASS`：八段适用事实可关联，D21三层分离，原生映射可回放，丢弃与隐私边界可见。
- `FAIL`：假造事件/receipt；关键安全事件被采样丢失；跨租户泄露；Agent可改审计；HTTP 200或completed冒充验收。
- `REVIEW_REQUIRED`：关键ID、适配器映射、effect、delivery、readback或观测覆盖未知，系统保持安全等待。

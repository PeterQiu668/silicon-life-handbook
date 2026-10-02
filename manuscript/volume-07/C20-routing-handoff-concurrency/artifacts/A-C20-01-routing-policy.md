---
artifact_id: A-C20-01
chapter_id: C20
title: "路由策略"
status: drafting
approval_status: unapproved
verified_on: "2026-09-30"
---

# A-C20-01 路由策略

> 本产物决定“谁具备进入某项任务的资格、合格者如何排序、无合格者如何停止或让位”。它不授予业务权限，不改变 C17 授权，也不以 Binding 命中替代任务路由。

## 任务与候选快照

| 字段 | 必填内容 |
|---|---|
| task_ref / task_version | C09 任务卡标识与不可变版本 |
| objective / deliverables | 可验证目标与交付物，不接受“帮忙处理” |
| data_class / data_location | 数据等级、允许地域与执行位置 |
| risk / deadline / budget | 风险、截止时间、成本与调用上限 |
| authorization_ref | C17 授权对象、动作、范围、参数、时窗、批准者引用 |
| candidates | 身份、能力证据、工具资格、负载、故障域、成本、时效 |
| decision_owner | 对最终路由记录负责的主体 |

## 两阶段裁决

### 第一阶段：硬门过滤

候选必须逐项通过；任一项不通过即从本轮候选集中剔除，不得用高能力、低成本或快响应补偿。

| hard_gate | PASS 条件 | 失败处置 |
|---|---|---|
| task_version | 候选读取并确认当前任务版本 | 刷新；旧版本结果隔离 |
| policy_legality | 合法、合规、组织策略允许 | DENIED，升级政策所有者 |
| authorization | C17 对象、动作、范围、参数、时窗和批准者均匹配 | DENIED，不可先做后批 |
| data_location | 处理位置满足数据驻留与传输限制 | NO_ELIGIBLE 或本地降级 |
| minimum_capability | 有同风险、同工具族的可核验证据 | YIELD_REQUIRED，不接受自称 |
| tool_eligibility | C14 工具合同、凭证引用和审批可用 | DENIED 或改为只读/提案 |
| admission_load | 容量、并发槽、截止时间内可完成 | 换候选、排队或降级 |
| failure_domain | 与审查者、sentinel、关键依赖不存在禁用共因 | 重排或人工裁决 |

### 第二阶段：软排序

只在全部通过硬门的候选间比较。记录原始维度与决策理由，不压成不可解释的神秘总分。

| soft_factor | 证据 | 可接受取舍 |
|---|---|---|
| capability_fit | 已验证能力与失败分布 | 高匹配可优先，但不替代授权 |
| current_load | 队列、在途任务、尾延迟 | 低负载优先，不能绕过 admission |
| cost | 调用、协调、恢复成本 | 节省不得牺牲安全硬门 |
| timeliness | 截止时间、冷启动和迁移开销 | 快不等于可负责 |
| data_locality | 少传输、少复制、少暴露 | 作为合格候选中的优化项 |
| continuity | 已持有的合法上下文与状态 | 过期上下文是负证据 |

## 路由决定、让位与回退

每次决定记录：`route_decision_id`、输入版本、合格/淘汰候选、逐硬门结论、软排序依据、主目标、备用目标、有效时窗、路由所有者、变更触发器和证据摘要。合法状态为 `ROUTE_PROPOSED / ROUTE_ADMITTED / EXECUTING / DENIED / NO_ELIGIBLE / YIELD_REQUIRED / REROUTE_REQUIRED / REVIEW_REQUIRED`；它们是工作流状态，不替代全书 `PASS / FAIL / REVIEW_REQUIRED` 验收语言。

让位通知至少包含：`notice_id`、任务与版本、当前执行者、原因码、已完成/未完成、证据、当前副作用状态、安全停点、建议目标及其资格证据、下一动作、响应时限、回退和升级路径。沉默、离线、超时与 `NO_REPLY` 均不构成让位。

主目标不可用时，只能在仍通过全部硬门的备用目标中重排。没有合格目标时，停止在 `NO_ELIGIBLE` 或 `REVIEW_REQUIRED`，不得为了完成率降低硬门。

## 路由变更触发器

- 任务范围、输入版本、风险、数据位置、工具或授权变化；
- 候选能力证据过期、负载越界、故障域改变；
- 连续让位、截止时间临近、冲突或 UNKNOWN；
- 上游 C17 真实实践证据或 C19 实践门结论变化。

变更必须产生新 `route_decision_id`，保留旧决定及原因。C17 与 C19 当前均为受限输入：C17 离线机器控制已复现但真实授权环境未跑；C19 事实/交叉门已通过（有限制）但实践待审。真实授权和真实组织路由继续保持 `REVIEW_REQUIRED`，并在形成新证据后回归本策略。

## 平台映射

- OpenClaw v2026.9.6 固定实现中的 Channels、Accounts、Pairing 与 Bindings 是入口与绑定事实，不自动成为本表的任务执行路由或授权。
- Hermes 0.20.1 固定实现与动态文档分别登记；委托、队列、看板等实现只能承载候选和状态，不免除硬门。
- Muse 仅记录公开产品体验的 `VENDOR-CLAIM`，不推断其内部路由、负载或授权机制。
- A2A 1.0 只提供互操作镜面；Agent Card 是描述输入，不是能力、身份或信任证明。

## 三态验收

- `PASS`：任务版本明确；所有硬门逐项可核验；软排序可解释；主备、让位、停止和回退完整。
- `FAIL`：授权或数据位置未通过仍路由；Binding 被当作授权；伪装胜任被采信；无合格者仍强行执行。
- `REVIEW_REQUIRED`：能力、负载、receipt、授权或执行位置证据为 UNKNOWN；上游受限输入尚未回归。

## 变更记录

- 2026-09-30：建立作者版，状态 `drafting / unapproved`。

---
exercise_id: "X-C02-01"
title: "训练任务与生产任务分流"
status: "drafting"
level: "foundational"
estimated_time: "120m"
prerequisites: ["C01", "C02-S05"]
environment: "sandbox-or-paper-exercise"
permissions_required: ["read-deidentified-task-records"]
inputs: ["deidentified-task", "historical-sample", "version-snapshot", "human-intervention-record", "business-owner", "independent-reviewer", "A-C02-01"]
steps: ["write-production-task", "write-training-candidate", "separate-data-and-environment", "decide-production-to-training-gate", "design-training-to-production-gate", "check-contamination", "run-three-outcome-tabletop"]
artifacts: ["production-task", "training-candidate", "data-boundary", "two-gate-decisions", "tabletop-record", "rollback-record"]
evidence: ["input-and-deidentification-note", "version-snapshot", "two-task-cards", "gate-decisions", "three-outcome-records", "reviewer-opinion"]
stop_conditions: ["no-business-owner", "unsafe-or-unauthorized-data", "production-impact", "candidate-not-rollbackable", "high-risk-role-conflict"]
rollback: ["restore-baseline-snapshot", "revoke-temporary-credentials", "remove-unapproved-test-copy", "verify-production-unchanged"]
acceptance: ["PASS", "FAIL", "REVIEW_REQUIRED"]
transfer_variant: "将研究场景迁移到运营或多 Agent 交付，保持双闭环和双向门禁。"
produced_by: "C02"
reviewer: "C02-practice-review-agent"
verified_on: "2026-09-30"
---

# X-C02-01 训练任务与生产任务分流

## 目标

把一个同时包含“今天要交付”和“希望 Agent 以后变强”的混合请求拆成生产闭环与训练闭环，建立数据回流和候选发布的双向门禁。

## 场景

选择以下一个场景，或使用经过脱敏的自有重复任务：

- CASE-A：今天必须提交一份研究报告，同时希望研究 Agent 学会辨别一手来源。
- CASE-B：今天必须处理客户状态变化，同时希望运营 Agent 降低无意义提醒。
- CASE-C：今天必须完成多 Agent 提案，同时希望团队减少重复劳动和交接丢失。

不得使用真实密钥、未授权客户数据、支付、删除或生产写权限。

## 输入

- 一份任务目标和截止时间；
- 一份脱敏历史样本；
- 当前 Agent/模型/Runtime/工具版本；
- 当前人工介入记录；
- 一名业务所有者和一名评审者；
- [A-C02-01 双闭环图](../artifacts/A-C02-01-dual-loop.md)空白模板。

## 步骤

### 1. 写生产任务卡

只描述本次真实交付：对象、最终状态、时间、预算、权限、不可接受失败、人工审批点和恢复动作。负责人是业务所有者。输出为 `production_task`。

### 2. 写训练候选卡

从历史失败中选择一个可观察行为差距，例如“引用无法解引用”或“无变化也提醒”。不得写“更聪明”“更主动”。负责人是训练者。输出为 `training_candidate`。

### 3. 分离数据与环境

标记哪些生产资料可以脱敏进入训练，哪些只能留在原环境，哪些完全禁止使用。指定沙箱或纸面演练环境。负责人是数据/运行责任人。输出为 `data_boundary`。

### 4. 建生产到训练门

检查问题是否已止损、可重放、具有复用价值且已获数据授权。任一关键项为否，保持 `REVIEW_REQUIRED` 或 `FAIL`，不自动进入训练。

### 5. 建训练到生产门

列出基线、候选干预、回归、迁移、安全/成本检查、回滚和发布审批。负责人是训练者与独立评审者。输出为 `release_gate`。

### 6. 做污染检查

确认被测 Agent 无法修改留出答案、评分规则和发布决定；训练者不能隐藏失败样本；生产实例不能直接覆盖自身规则。

### 7. 运行桌面推演

模拟三种情况：训练候选通过、训练候选失败、评审意见冲突。记录每种情况下谁停止、谁回滚、谁裁决。

## 练习产物

```yaml
exercise_output:
  exercise_id: "X-C02-01"
  scenario: ""
  production_task:
    goal: ""
    deadline: ""
    allowed_scope: []
    prohibited_scope: []
    approval_points: []
    recovery: ""
  training_candidate:
    observable_gap: ""
    baseline_ref: ""
    proposed_intervention: ""
    transfer_test_ref: ""
  data_boundary:
    allowed: []
    deidentify_first: []
    prohibited: []
  production_to_training_gate:
    decision: "REVIEW_REQUIRED"
    reason: ""
  training_to_production_gate:
    decision: "REVIEW_REQUIRED"
    approver: ""
    rollback_ref: ""
  unresolved: []
```

## 证据要求

- 原任务和脱敏说明；
- 当前版本或配置快照；
- 两张任务卡；
- 双向门禁结果；
- 三种桌面推演记录；
- 评审者签名或可定位意见。

## 停止条件

- 无业务所有者或任务终态；
- 数据无法安全脱敏或无授权；
- 实验会改变生产、客户、资金或身份状态；
- 候选不可回滚；
- 评审者与执行者无法分离且风险高。

## 恢复与回滚

本练习默认不修改生产。若使用隔离环境运行候选，结束后恢复基线快照，撤销临时凭证，清除未经批准的测试副本，并验证生产版本未变化。

## 三态验收

- `PASS`：两条闭环目标分开；数据、权限、裁判和发布门完整；三种推演均有确定责任人与安全动作。
- `FAIL`：把真实生产直接当实验；用一次交付宣布训练成功；或被测 Agent 可修改评测与发布决定。
- `REVIEW_REQUIRED`：分流正确，但数据授权、基线、独立评审或回滚证据不完整。

## 迁移变式

把原场景换到另一个案例：研究换运营、运营换多 Agent 交付。保留双闭环结构，只替换任务目标、数据权利和风险门。若必须重写整个结构，说明原产物过度绑定场景。

## 变更记录

| 日期 | 版本 | 状态 | 变更 | 实战复核 |
| --- | --- | --- | --- | --- |
| 2026-09-30 | 0.1.0 | drafting | 创建分流练习、桌面推演与三态验收 | 未执行 |
| 2026-09-30 | 0.1.1 | drafting | 补齐练习机器字段；完成独立安全模拟试跑 | `review/runs/X-C02-01-simulation.md` |

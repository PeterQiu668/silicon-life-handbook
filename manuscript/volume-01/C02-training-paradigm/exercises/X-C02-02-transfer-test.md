---
exercise_id: "X-C02-02"
title: "迁移测试：区分学会与背答案"
status: "drafting"
level: "variant"
estimated_time: "180m"
prerequisites: ["X-C02-01", "C02-S03", "C02-S05"]
environment: "isolated-sandbox"
permissions_required: ["read-deidentified-test-data", "write-test-artifacts"]
inputs: ["synthetic-or-deidentified-samples", "environment-snapshot", "baseline-version", "candidate-version", "single-intervention", "independent-reviewer"]
steps: ["freeze-environment-and-baseline", "state-single-intervention", "run-training-group", "run-regression-group", "run-independent-holdout", "decide-three-state", "restore-baseline"]
artifacts: ["sample-manifest", "all-run-results", "failure-classification", "reviewer-opinion", "rollback-verification"]
evidence: ["environment-and-version-snapshot", "sample-groups", "baseline-and-candidate-results", "cost-and-latency", "reviewer-disagreements", "rollback-record"]
stop_conditions: ["holdout-leak", "multiple-unseparable-variables", "safety-or-permission-breach", "environment-drift", "missing-run-log"]
rollback: ["restore-baseline-version", "remove-candidate-from-production-route", "verify-production-release-false", "preserve-evaluation-evidence"]
acceptance: ["PASS", "FAIL", "REVIEW_REQUIRED"]
transfer_variant: "在不增加权限时加入时限、缺失信息、冲突来源、重复事件或子 Agent 超时。"
produced_by: "C02"
reviewer: "C02-practice-review-agent"
verified_on: "2026-09-30"
---

# X-C02-02 迁移测试：区分学会与背答案

## 目标

检验一个候选干预是否只改善已见训练样本，还是能在任务目标不变、数据、表达或约束发生变化时保持有效。练习允许得到“没有提升”的结论，不要求为了通过而修改结果。

## 安全边界

只在隔离环境使用脱敏或合成数据。不得连接真实外发、资金、删除、生产写入、身份变更或客户系统。任何需要扩大权限的候选直接进入 `REVIEW_REQUIRED`，不在本练习中执行。

## 选择一个可观察行为

示例：

- CASE-A：遇到无法核验的事实时明确标注未知，并提供可定位来源。
- CASE-B：只有状态出现有意义变化时才提出通知，重复事件保持安静。
- CASE-C：Handoff 同时包含已完成、未完成、证据、风险、阻塞和下一步。

不得使用“更专业”“更懂我”“协作更好”等不可直接判定目标。

## 样本设计

至少准备六个样本，分成三组：

1. **基线/训练组**：两个已见样本，用于观察和调整。
2. **回归组**：两个历史样本，确保候选没有破坏原本可用能力。
3. **留出/迁移组**：两个未向被测 Agent 或候选生成者暴露的样本，至少改变数据、表达、约束之一。

测试规模只用于练习方法，不能据此宣称统计稳定或行业领先。正式评测规模由 C07 决定。

## 步骤

### 1. 固定环境与基线

记录模型、Runtime、工具、Skill、工作区、权限和随机性设置。用旧版本运行全部允许暴露的基线/回归样本；留出答案由独立评审者保管。

### 2. 写出单一主要干预

说明改动对象、假设和副作用，例如“给来源核验 Skill 增加无法核验时的停止分支”。不得同时更换模型、工具和数据。

### 3. 在训练组运行候选

保存完整输出、轨迹、工具调用、人工介入、成本和错误。不得只保存最佳一次。

### 4. 运行回归组

检查原本通过的行为是否退化。出现安全关键失败时立即停止，不继续用平均分稀释。

### 5. 由独立评审运行迁移组

被测 Agent 不得读取答案或修改评分；候选生成者不得挑选最有利样本。记录每次运行及失败原因。

### 6. 作出三态判定

比较基线与候选，但不把微小差异强行解释为提升。证据不足或评审冲突时选择 `REVIEW_REQUIRED`。

### 7. 恢复环境

不论结果如何，都恢复基线版本；只有另行获得发布审批后，候选才可进入生产。

## 结果记录

```yaml
transfer_test:
  exercise_id: "X-C02-02"
  behavior_under_test: ""
  environment_snapshot: ""
  baseline_version: ""
  candidate_version: ""
  primary_intervention: ""
  hypothesis: ""
  sample_groups:
    training: []
    regression: []
    holdout_transfer: []
  results:
    baseline: []
    candidate_training: []
    candidate_regression: []
    candidate_transfer: []
  safety_failures: []
  cost_or_latency_changes: []
  reviewer_disagreements: []
  decision: "REVIEW_REQUIRED"
  limitations: []
  rollback_verified: false
  production_release_authorized: false
```

## 证据要求

- 环境与版本快照；
- 样本分组与留出保管说明；
- 基线和候选的全部运行结果；
- 失败分类、人工介入、成本与延迟；
- 独立评审意见；
- 回滚验证记录。

## 停止条件

- 留出样本或答案已泄漏；
- 候选同时改变多个无法拆分的主要变量；
- 安全、权限或数据边界被突破；
- 环境版本中途改变，导致基线不可比较；
- 结果日志缺失，无法复核失败。

## 三态验收

- `PASS`：候选在训练组改善或保持目标行为，回归组无关键退化，迁移组达到预先声明的行为条件，安全/成本未越门，回滚已验证。此结果仍只支持练习声明范围，不自动授权生产发布。
- `FAIL`：只在训练组变好；回归或迁移出现关键退化；评测被污染；或候选越过安全边界。
- `REVIEW_REQUIRED`：样本太少、结果混合、评审冲突、成本变化不明或环境差异妨碍比较。

## 压力变式

在不增加权限的前提下加入一种压力：更短时限、缺失信息、互相冲突的来源、重复事件或一个子 Agent 超时。观察候选是否保持停止、求助和证据纪律。压力结果单独报告，不与普通样本平均。

## 变更记录

| 日期 | 版本 | 状态 | 变更 | 实战复核 |
| --- | --- | --- | --- | --- |
| 2026-09-30 | 0.1.0 | drafting | 创建迁移测试、留出纪律、压力变式与三态验收 | 未执行 |
| 2026-09-30 | 0.1.1 | drafting | 补齐练习机器字段；完成 7 样本独立安全模拟试跑 | `review/runs/X-C02-02-execution.log` |

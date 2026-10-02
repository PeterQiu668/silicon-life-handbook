---
exercise_id: X-C08-01
chapter_id: C08
title: "运行三轮单变量训练"
level: applied
estimated_time: 150m
environment: isolated-copy
status: drafting
execution_status: author_simulation_completed_independent_review_pending
---

# X-C08-01　三轮单变量训练

## 目标

从 C07 的一个失败簇出发，运行三轮只改变同一主干预对象的训练，保存基线、差异、training/regression/holdout 结果、横切安全套件、失败分布和停训/回滚决定。安全套件必须绑定四层数据身份与场景，不得成为第五层或替代 real_world；训练集提分不能作为能力结论。

## 前置条件

- 已有 C04 能力节点、风险与负面清单；
- 已有 C05 契约边界；
- C07 已冻结数据版本、grader、硬门、争议流程与运行次数；
- 隔离环境无真实密钥、用户、资金、生产写入或公开外发；
- teacher、learner、reviewer 与人类 owner 的访问权已登记。

## 输入

- [训练计划](../artifacts/A-C08-01-training-plan.md)；
- [合成 harness](../review/runs/synthetic_training_harness.py)；
- [作者试跑摘要](../review/runs/experiment-result-summary.yaml)；
- 一份由独立实践者重新生成或确认未污染的 holdout，以及逐项登记 canonical layer/scenario 的横切安全套件。

## 步骤

1. 冻结 `experiment_id`、主变量、不变量、数据版本、预算与门禁。
2. 运行基线并保存全部失败；不得丢弃异常运行。
3. R1 只改变一个可定位的候选规则；运行 training、regression、holdout 和横切安全套件；不得把四个运行分区误称为 C07 的四个规范数据层。
4. 依据训练集反馈提出 R2，但不得读取留出答案；若主假设失效则停训。
5. 以同样规则运行 R2、R3；每轮保存 exact diff 和 manifest hash。
6. reviewer 只按冻结 rubric 判断，不参与候选改写；主观争议交人类/专家。
7. 先看安全和回归硬门，再看留出，最后才看训练结果与成本。
8. 达到停训条件时停止，不以“再试一次”绕过预注册上限。
9. 执行回滚或丢弃未发布候选，验证无外部副作用和旧权限未被改变。
10. 把关闭/未关闭错误写入 A-C08-03。

## 停止条件

- 安全、权限、隐私、审批或不可逆硬门失败；
- 留出污染、grader 改变、版本漂移或多变量混改；
- 独立 reviewer 缺位；
- 候选不可回滚或出现外部副作用；
- 三轮后主假设仍不获留出/安全支持；
- 预算、时延或人工救场越过合同。

## 回滚

恢复最近安全版本；撤回候选权限和写入；取消队列；核查 session、memory、cache、index 与外部终态；保留全部 trace 和失败；重跑回归与负向权限测试。真实副作用不能只说“已回滚”，必须补偿、对账和升级。

## 验收

- `PASS`：三轮可复现；主变量唯一；regression、holdout、横切安全套件均过门；安全样本 layer/scenario 完整；失败完整；独立 reviewer 与有权 owner 签核。
- `FAIL`：训练集代替留出；导师自判；安全失败被平均；隐藏答案泄漏；候选越权生效；回滚不完整。
- `REVIEW_REQUIRED`：作者合成试跑已完成但独立实践者未复核，或数据、归因、平台行为仍未知。当前示例为此状态。

## 迁移变式

把“来源纪律 Skill”换成 CASE-B 的低噪音 Workflow 或 CASE-C 的 Handoff Skill，但只能改变一个主对象；高风险外发和生产写入最多运行到 shadow/审批前一步。

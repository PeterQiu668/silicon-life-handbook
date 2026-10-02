---
review_id: PR-C03-001
chapter_id: C03
review_type: independent-practice-and-safety-gate
status: completed_with_findings
reviewed_on: "2026-09-30"
reviewer: c03-independent-practice-review-agent
reviewer_roles_excluded: [chapter-author, c03-evidence-reviewer]
chapter_status_after_review: revision_required
self_approval: false
final_editorial_approval: false
---

# C03 独立实践门评审

## 1. 结论

X-C03-01 与 X-C03-02 已在离线、匿名、可回滚的合成模拟环境中实际执行，均取得练习级 `PASS`。本轮不是只读练习文字：已保存 20 条多次运行、冻结的同任务/预算/风险合同、逐运行 TEV 定位、失败分布、三个红队门禁、声明降级、停止条件和回滚记录。

P0-05、P0-06、P0-07 在 **C03 章节实践范围内关闭**。章节当前为 `revision_required`，不得据此标记 `done` 或 `release_candidate`；真实产品表现、跨 Runtime 迁移、C07 统计协议、C24 认证以及主编另行提出的篇幅修订均不在本次结论内。

## 2. 独立性与范围

本评审者不是 C03 章节作者，也不是本章事实/交叉审校者。评审对象是练习是否可执行、可停止、可回滚，证据与声明是否闭合；不重新批准外部来源，不承担总编签核，不认证任何系统等级。

运行材料全部为 `synthetic-demonstration`。没有网络请求、真实 Agent Runtime、真实客户/身份数据、外发、支付、删除或生产变更。故本次可以验证流程控制，不能外推真实平台能力。

## 3. 运行材料索引

| 对象 | 位置 | 作用 |
| --- | --- | --- |
| X-C03-01 运行记录 | [RUN-C03-01](runs/RUN-C03-01-baseline-comparison.md) | 输入、步骤、输出、耗时、失败、停止与回滚 |
| 20 条结构化运行 | [c03-baseline-run-set.yaml](runs/c03-baseline-run-set.yaml) | Alpha/Beta 各 10 次，多次运行与失败分布 |
| 三前提合同 | [comparison-contract-review.md](runs/comparison-contract-review.md) | 同任务、同预算、同风险核对 |
| TEV | [baseline-tev-index.md](runs/baseline-tev-index.md) | 逐声明过程、产物、效果证据 |
| 产物/效果登记 | [baseline-artifact-register.md](runs/baseline-artifact-register.md)、[baseline-effect-register.md](runs/baseline-effect-register.md) | 可解引用的合成证据替身与边界 |
| 七维与失败分布 | [baseline-seven-dimension-scorecard.md](runs/baseline-seven-dimension-scorecard.md) | 不合成总分，保留反例与未知 |
| 受限声明 | [bounded-comparison-statement.md](runs/bounded-comparison-statement.md) | 对领先措辞限缩 |
| X-C03-02 运行记录 | [RUN-C03-02](runs/RUN-C03-02-red-team.md) | 三类陷阱实际裁决 |
| 红队结构化输入 | [c03-red-team-observations.yaml](runs/c03-red-team-observations.yaml) | 原始场景规范化与隔离声明 |
| 红队发现与决策 | [red-team-findings.md](runs/red-team-findings.md)、[gate-decisions.yaml](runs/gate-decisions.yaml) | 非补偿门禁与责任 |
| 降级与回归 | [corrected-claims.md](runs/corrected-claims.md)、[regression-plan.md](runs/regression-plan.md) | 可发布上限与可执行复测 |

## 4. X-C03-01 验收

| 验收项 | 结果 | 实际证据 |
| --- | --- | --- |
| 多次运行 | PASS | 每系统 10 次：8 次正常、2 次留出；ID 连续且无排除 |
| 同任务/预算/风险 | PASS | 三份合同 ID 冻结，两系统字段相同，所有运行预算内 |
| TEV 三证 | PASS | 完成、来源、不确定性、留出、预算、禁止动作六类主张均有三证或 N/A 理由 |
| 完整失败分布 | PASS | Alpha 2 个非合格；Beta 4 个非合格，含 1 个人工接管；无删除 |
| 硬门禁 | PASS | 20 次无禁止动作；门禁先于七维评分 |
| 公平声明 | PASS | 不给总分/冠军；同时报告 Alpha 质量稳定信号与 Beta 效率信号 |
| 归因边界 | PASS | 能力、单次表现、运气、环境/裁判贡献和业务业绩分开 |

实际汇总：Alpha 8/10 合格、平均成本 1.698、平均墙钟 15.3 分钟；Beta 6/10 合格、平均成本 1.169、平均墙钟 12.1 分钟。受限结论没有把较多合格运行扩写为“全面更强”，也没有把低成本扩写为“总体效率领先”。

## 5. X-C03-02 验收

| 场景 | 原始诱惑 | 实际裁决 | 非补偿性 |
| --- | --- | --- | --- |
| RT-C03-01 | 平均分 91 | `FAIL`：确认的未批准外发阻止发布与授权升级 | 平均分不可抵消 |
| RT-C03-02 | 12 次只留最佳 1 次 | `FAIL`：撤回稳定、专家和 MAT-L4 候选 | 最佳样本不可替代分布 |
| RT-C03-03 | 墙钟 55 对 120 分钟 | `FAIL`：预算/风险不等价且权限扩散 | 速度不可抵消权限失败 |

三项机器决策都设置 `non_compensable: true`、`score_aggregation_allowed: false`、`self_approved: false`。三个原声明均已降级到证据支持上限，且各有负责人、输入、动作、输出、证据、停止和恢复合同。

## 6. P0-05 / P0-06 / P0-07 关闭判断

### P0-05 操作可执行、可停止、可回滚：PASS，章节实践范围内关闭

两项练习均真实走完输入—动作—产物—验收；运行记录保存耗时和失败样本。停止条件覆盖真实数据、禁止动作、证据删除、预算/风险不等价；回滚明确撤回声明、冻结能力、隔离权限和恢复只读沙箱。本次外部状态变化为 0，记录“无需业务回滚”而非伪造回滚成功。

### P0-06 高风险动作有权限、审批和隔离：PASS，章节实践范围内关闭

网络和外部动作在环境层禁用，不以提示词作为唯一控制。对场景一与三的越权/权限扩散均由风险所有者门禁并阻止发布或升级；回归计划要求模拟端点、令牌吊销、最小权限和隔离目录。没有执行真实高风险动作。

### P0-07 练习有基线、证据和客观验收：PASS，章节实践范围内关闭

X-C03-01 使用冻结基线、20 条完整运行、TEV 和失败分布；X-C03-02 用三个预定陷阱检验非补偿门禁。判断依据是字段、定位符和三态阈值，不是主观“感觉更强”。声明均写清适用范围与失效触发器。

## 7. 发现与修复

### P1：跨 Runtime 实跑仍未完成

本轮只验证书内练习流程，没有在 Hermes 或另一开放 Runtime 上复做。保持交叉审稿的原缺口，不将其伪装成本轮 P0 已解决。

### P1：C07/C24 后续回归仍必需

样本量、grader、统计推断由 C07 定义；等级阈值与认证由 C24 定义。本轮只形成观察性剖面和候选信号，没有越权发布通用阈值或等级。

### P2：回滚措辞的小缺陷，已修复

X-C03-02 原 YAML 的“删除派生副本中的敏感内容”容易被误读为参与者自行删除现场。已改为：先隔离，由数据责任人按既有处置流程清理未授权派生副本，同时保留最小审计记录且不改原始证据。该修复没有扩大章节边界。

## 8. 最终三态

- X-C03-01：`PASS`
- X-C03-02：`PASS`
- C03 实践门：`PASS`
- P0-05：`PASS / CLOSED IN CHAPTER PRACTICE SCOPE`
- P0-06：`PASS / CLOSED IN CHAPTER PRACTICE SCOPE`
- P0-07：`PASS / CLOSED IN CHAPTER PRACTICE SCOPE`
- 章节状态：继续 `revision_required`
- 最终出版批准：`false`

本实践评审是独立练习签核，但不构成整章总编批准，也不允许把演示系统、平台或本书称为“行业最强”。

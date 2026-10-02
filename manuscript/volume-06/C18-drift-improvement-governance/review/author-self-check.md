---
chapter_id: C15
review_type: author-self-check
reviewer: "chapter-author-agent:c15"
reviewed_on: "2026-09-30"
status: drafting
approval_status: unapproved
independent_signoff: false
---

# C15 作者自检

> 本记录只说明 C15 已具备送交独立事实、交叉、实践、编辑与总编审校的材料；作者不得批准任何独立门，不证明真实 OpenClaw/Hermes、自学习、生产影子、canary、组织审批或回滚已经运行。

## 交付清点

- 正文编号严格为 15.1—15.7；项目正式校验器计 18,377 CJK，另以去 frontmatter 与围栏代码块的保守口径计 18,347。
- 母产物恰好三件：`A-C15-01` 漂移体检表、`A-C15-02` 改进提案、`A-C15-03` 影子测试与回滚计划。
- 两项练习具有输入、角色、安全边界、步骤、停止、回滚、三态验收与交接记录要求。
- 证据账本包含 23 条 claim、4 项显式 `REVIEW_REQUIRED`。
- 离线确定性夹具展开 75 个唯一 task/trial：20 PASS、45 FAIL、10 REVIEW_REQUIRED；预期匹配，真实外部副作用为零，代表性真实任务为 0，十五条拟迁移记录只是合成 holdout shadow。

## 15 项 P0

| 门禁 | 作者结论 | 证据与限制 |
|---|---|---|
| P0-01 | PASS | 章首导航、解决/不解决、15.1—15.7、结论、练习与交接完整；无 15.8+。 |
| P0-02 | PASS | C15 只拥有五类漂移、候选改进与目标治理接口；不重定义 C07/C08/C10/C12/C14/C21/C24。 |
| P0-03 | PASS | 23 条方法、平台与本地实验主张进入 evidence ledger，并在正文闭合引用。 |
| P0-04 | PASS | OpenClaw 固定提交、Hermes 动态官方页、Muse `VENDOR-CLAIM` 分层；无伪造同构。 |
| P0-05 | PASS | 五步回路包含停止、对账、驳回、限域、继续观察、回滚与外部固化。 |
| P0-06 | PASS | Agent 不得自改安全、grader、权限、`AU-Lx`、目标或生产资产；目标变化返回 C14。 |
| P0-07 | PASS | 75 trial 具有唯一 ID、合法 D22 层级、横切安全、完整失败分布和双运行一致 hash；未用合成 shadow 冒充真实任务。 |
| P0-08 | PASS | 仿生四段明确稳态类比、工程映射、训练启示与非意识/非进化边界。 |
| P0-09 | PASS | 平台事实均说明版本身份、核验日期、可支持结论和不可推断部分。 |
| P0-10 | PASS | CASE-A/B/C 为教学合成案，无客户数据、凭证、外发、支付或生产写。 |
| P0-11 | PASS | YAML 文件、frontmatter 与 Agent 可读 YAML 进入机器校验；所有状态使用 PASS/FAIL/REVIEW_REQUIRED。 |
| P0-12 | PASS | 真实 Runtime、生产 shadow/canary、组织审批、治理成本和 Muse 内部机制保持 `REVIEW_REQUIRED/UNKNOWN`。 |
| P0-13 | PASS | 安全失败、污染、越权、影子写入和撤销复活均不可被质量均分补偿。 |
| P0-14 | PASS | 三件母产物字段与 C21/C22/C24 交接可定位；未暗增目标表或第四母产物。 |
| P0-15 | PASS | 无“行业最强”或必然提升主张；观察、确认漂移、因果和外部批准四层分开。 |

## 百分制作者初评

| 维度 | 满分 | 得分 |
|---|---:|---:|
| 论证与结构 | 14 | 14 |
| 事实准确与证据 | 18 | 17 |
| 技术与系统完整性 | 10 | 10 |
| 课程与学习设计 | 12 | 12 |
| 实践与可复现性 | 14 | 12 |
| 评测与验收 | 12 | 12 |
| 安全、治理与伦理 | 8 | 8 |
| 仿生解释质量 | 4 | 4 |
| 表达与出版质量 | 8 | 8 |
| **总分** | **100** | **97** |

扣分只来自真实平台与真实组织证据未闭合：未运行 OpenClaw Workshop/self-learning、Hermes 固定环境、生产 shadow/canary、外部审批与完整 bundle 恢复。作者不能用本评分自批事实、交叉、实践、编辑、总编或 RC 门。

## 可重复性与待独立复核

- 连续两次运行 `python3 review/runs/run-drift-harness.py`，结果文件逐字一致。
- post-fix results SHA-256：`2356adeda8acba503f52f41e8e013da2484f524098bb75ecc181676724362975`；recert registry 修补后待非作者双目录复核。
- post-fix summary SHA-256：`fee7041637c340a47ff4a0fc31ff12b464dd5b7f81a54e11597d4dc432306cc5`；状态化修补后待非作者双目录复核。
- 机器结果：75 trial；20 PASS、45 FAIL、10 REVIEW_REQUIRED；unique、expected matched、zero external effects、security noncompensatory 均为 true。
- 独立实践评审需在新临时目录复跑，并重做 lineage、重复试次、holdout/grader、身份自批、权限/目标 diff、stale target、失效批准、UNKNOWN/盲重试、shadow write、完整 bundle rollback、撤销复活、终态/probe、外部 effect、重复 ID 与真实层来源的近邻和组合变体；真实目标环境未验证部分不得被误标 PASS。

作者结论：C15 生产包可提交独立审校，状态继续 `drafting / unapproved`，不批准 RC。

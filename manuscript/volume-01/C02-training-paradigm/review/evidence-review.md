---
review_id: "C02-EVIDENCE-REVIEW-01"
chapter_id: "C02"
review_type: "evidence"
status: "completed-with-findings"
reviewer_role: "independent-evidence-reviewer"
reviewed_on: "2026-09-30"
chapter_status_after_review: "drafting"
gate_decision: "REVIEW_REQUIRED"
---

# C02 证据审校记录

## 审校结论

C02 的证据结构通过本轮事实门审查：方法论、外部来源、跨来源推断、固定版本产品事实和厂商声明已经分层；12 个证据 ID 均能在正文定位，正文使用的证据 ID 也都能在账本解引用。OpenClaw、Hermes Agent 与 Meta Muse 没有被写成同等证据强度，Muse 的内部训练与自修改机制保持未知。

本结论只表示“证据账本与正文目前闭合”，不表示练习效果已经得到证明。两项练习尚未由独立实践评审运行，因此章节仍为 `drafting`，事实门不得替代实战门或总编门。

审校基准：[`chapter.md`](../chapter.md)、[`evidence-ledger.yaml`](../evidence-ledger.yaml)、[`平台与前沿实践证据底稿`](../../../../docs/research/platform-and-frontier-evidence.md)、[`历史内容映射`](../../../../docs/research/legacy-content-map.md)、[`出版质量标准`](../../../../docs/editorial/BOOK-QUALITY-STANDARD.md)。

## 证据闭合检查

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| 账本证据 ID 数 | PASS | `E-C02-001` 至 `E-C02-012`，共 12 项，ID 唯一 |
| 正文所引 ID 可解引用 | PASS | 正文引用集合与账本 ID 集合一致，无未知 ID |
| 账本 ID 均被正文使用 | PASS | `E-C02-009` 已在 `chapter.md` §2.7 的 Agent Skills 边界段引用 |
| 事实身份 | PASS | `METHODOLOGY`、`SOURCE-BASED`、`INFERENCE` 分开使用 |
| 日期与版本 | PASS | OpenClaw 2026.9.6、Hermes Agent 0.20.1、Muse `public-materials-only` 均在章首与账本标明 |
| 局限与复核触发器 | PASS | 12 项均含 `limitations` 与 `recheck_trigger` |
| 被排除旧主张 | PASS | 无证据比例、倍数、行业绝对判断和“30 天必然进化”已进入 `excluded_legacy_claims` |

## 逐项证据审计

| ID | 结论 | 身份与作用域 | 审校意见 |
| --- | --- | --- | --- |
| E-C02-001 | PASS | 本书方法论 / general | 三范式和训虾定义明确标为本书定义，没有冒充外部标准。 |
| E-C02-002 | PASS（受限） | 课程页面 / general | 只支持方法起源；正文明确说明缺少逐字稿、实验设计、样本和结果，不承载效果主张。 |
| E-C02-003 | PASS | 多源共同原则 / general | 支持“不能只看一次最终回答”；统计设计明确让渡 C07。`stable` 表示跨来源原则稳定，不表示各来源实现相同。 |
| E-C02-004 | PASS | 本书方法论 / general | 双闭环及其接口只由正式框架和历史映射支持，不再借 A2A 为本书方法背书。 |
| E-C02-005 | PASS | 跨来源推断 / general、OpenClaw、Hermes | “候选变更不等于净提升”已标 `INFERENCE`，并保留独立评测、权限、发布和回滚限制。 |
| E-C02-006 | PASS（版本性） | OpenClaw 2026.9.6 | 只说明 Skills/Skill Workshop 可承载候选改变，不宣称自动提升；具体命令与字段未进入本章。 |
| E-C02-007 | PASS（版本性） | Hermes Agent 0.20.1 | 使用 Hermes 官方资料和本地版本快照；没有把 OpenClaw 文件或加载语义机械迁移过去。 |
| E-C02-008 | PASS（厂商声明） | Muse / vendor-claim | 只写 Meta 公开的长任务、连接器和审批体验；未推断闭源训练集、自修改和净提升。 |
| E-C02-009 | PASS（前沿规范） | Agent Skills | 只支持封装与渐进披露边界，明确不能证明信任、激活、分发或运行时授权。 |
| E-C02-010 | PASS（已修正） | 历史材料编辑推断 / general | “保留哪些、淘汰哪些”是编辑判断，已从 `SOURCE-BASED` 修正为 `INFERENCE`。 |
| E-C02-011 | PASS | 本书方法论 / general | 七阶段生命周期与 C24 成熟度明确分离，不把它写成行业认证标准。 |
| E-C02-012 | PASS | 教学复合案例 / general | CASE-A/B/C 明确不是真实客户绩效，不承担效果证明。 |

## 三平台证据边界

| 平台 | 允许结论 | 禁止外推 | 本章执行结果 |
| --- | --- | --- | --- |
| OpenClaw | 固定版本官方资料可证明存在候选能力载体和可审计实现面 | 平台有自学习功能，不等于长期净提升已被证明 | PASS；正文 §2.7 与“平台实现对照”均保留版本和效果边界 |
| Hermes Agent | 官方资料与本地 0.20.1 快照可证明第二开放实现的 Skills、Memory 与写入控制 | 名称相似不等于文件语义、加载时机和审批路径相同 | PASS；正文明确“迁移结构，不照搬实现名” |
| Meta Muse | Meta 公开材料可作为托管产品、长任务、审批与可见产物案例 | 不推断内部训练、自修改、评测集、安全效果或净提升 | PASS；账本标 `vendor-claim`，正文使用“Meta 官方材料公开”口径 |

## 本轮局部修正

1. `chapter.md` §2.1、§2.3：首次出现的历史昵称补充外部规范表述，且仍声明为本书方法论，不包装成行业标准。
2. `chapter.md` §2.7：补入 `E-C02-009` 引用，使 Agent Skills 边界主张与账本闭合。
3. `chapter.md` “证据引用与变更记录”：删除“由 A2A 支持双闭环”的残余摘要，使其与 `E-C02-004` 的方法论身份一致。
4. `evidence-ledger.yaml > E-C02-003`：把跨来源共同评测原则稳定性记为 `stable`，保留“具体统计方法由 C07 定义”的限制。
5. `evidence-ledger.yaml > E-C02-004`：移除无关 A2A 来源，避免协议语义为训练方法越界背书。
6. `evidence-ledger.yaml > E-C02-010`：把历史内容取舍从 `SOURCE-BASED` 改为 `INFERENCE`，补充编辑判断限制。

## 问题与发布前条件

### P0-E-C02-01｜练习证据尚未产生

- 位置：`chapter.md` “本章产物与章际交接”；`exercises/X-C02-01-training-vs-production.md` 与 `exercises/X-C02-02-transfer-test.md` 的变更记录。
- 事实：两项练习均标“未执行”，没有独立评审运行结果、失败样本和回滚记录。
- 影响：当前证据只能支持训练原则和练习设计，不能支持“本章方法已经实战有效”或任何能力提升结论。
- 结论：`REVIEW_REQUIRED`。由实践评审运行后再判断 P0-07，不得由本证据审校替代。

### P2-E-C02-01｜动态平台事实需在进入候选稿前复核

- 位置：`evidence-ledger.yaml > E-C02-006` 至 `E-C02-009`。
- 事实：OpenClaw、Hermes、Muse 与 Agent Skills 均包含会变化的产品或规范材料。
- 处理：当前已记录版本、核验日期、限制和触发器；进入 `release_candidate` 前按账本重新核验即可，不要求在 drafting 阶段追逐 `latest`。

## 事实门决定

`PASS_WITH_FINDINGS`：证据身份、作用域、引用与限制通过；没有遗留的证据断链或 Muse 内部实现推断。章节总状态保持 `drafting`，等待独立实践结果、交叉审稿整改和总编辑复核。


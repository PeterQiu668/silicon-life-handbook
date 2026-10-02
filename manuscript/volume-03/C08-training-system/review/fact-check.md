---
review_id: FC-C08-001
chapter_id: C08
review_type: independent-fact-and-evidence-gate
status: completed
reviewed_on: "2026-09-30"
reviewer: "non-author-evidence-reviewer:platform_research"
independent_from_author: true
fact_gate: PASS
cross_gate: not_decided_here
practice_gate: not_approved
editor_gate: not_approved
chief_editor_gate: not_approved
chapter_status_after_review: drafting
self_approval: false
release_candidate_authorized: false
---

# C08 独立事实与证据审校

## 1. 裁决

**事实门 `PASS`，适用范围是“本章公开文本中的方法论身份、固定/动态版本事实、厂商声明边界和合成运行主张已经与当前证据闭合”。** 这不是实践门、编辑门、总编门或发布批准。真实 OpenClaw/Hermes Runtime 的训练写入、访问隔离、候选应用、回滚和生产效果仍为 `UNKNOWN`；Muse 内部训练、数据集、grader、模型更新和安全效果仍只允许写 `UNKNOWN` 或 `VENDOR-CLAIM`。

本次逐条核验 [正文](../chapter.md)、[证据账本](../evidence-ledger.yaml)、三件母产物、两项练习、C07 正式评测蓝图、D22 以及 17 个外部 URL。账本 24 个 evidence ID 全部被正文引用，正文没有缺失 ID 或孤儿 evidence。固定版本、动态页面、论文结论、厂商材料和本地合成验证均保持各自身份，没有从平台自述外推真实能力提升。

## 2. 核验方法与边界

1. 对 24 条 evidence 逐条比较 claim、label、stability、scope、source nature、locator 与 limitations；
2. 对 OpenClaw 使用 `v2026.9.6 / eb377ac59e6c9fd6c7705028034812becf00271b` 的 release 与固定 commit 文档，不以 main 替代；
3. 对 Hermes 只确认 2026-09-30 动态官方 Skills/Memory 页面，不回填为 `0.20.1` 固定实现事实；
4. 对 Muse 只确认 Meta 官方发布页与公开设计页所描述的用户可见产品表面，全部按厂商声明处理；
5. 对研究与工程指南核对原始页面或论文摘要，不把单项研究写成普遍规律；
6. 对本地合成结论复核作者结果、当前非作者实践记录和 hash 边界，但不重新批准实践门；
7. 对所有 Markdown 本地链接、账本本地 source path、Markdown frontmatter 与 YAML fenced block 做机械解析。

## 3. 本轮最小事实修补

| 修补 | 原问题 | 处理 | 影响 |
| --- | --- | --- | --- |
| `SELF-CORRECT` URL | OpenReview URL 返回 200，但正文被 challenge 页拦截，无法稳定显示论文内容 | 改为论文原始 arXiv 页面 `2310.01798` | 不改变结论，只恢复可解引用性 |
| 8.8.3 论文表述 | 正文点名 Reflexion/情景记忆，但账本只列 Self-Refine 与 intrinsic self-correction 论文 | 收窄为 Self-Refine 已直接支持的“语言反馈与迭代修订” | 删除未闭合的外推，不改变训练原则 |
| Muse 两源分工 | E-C08-019 把 `Artifacts` 压在 Meta 发布页单源上，而 Artifacts 由设计页直接支持 | E-C08-019 保留 Goals/Activity/记忆/权限/批准；E-C08-020 承担 Artifacts/side chats/Activity/permissions | 两条 vendor claim 各自与页面内容对应 |
| Hermes claim locator | 正文提到 Profile/Session 承载，E-C08-018 原 claim 未显式写出 | 把 per-profile 作用域与 Session 起点冻结快照纳入 E-C08-018 | 与动态 Memory 页面定位一致，仍要求印前重验 |
| C07 规范输入 | E-C08-006 仍只指向 preflight | 改指正式 A-C07-01 评测蓝图 | 以正式产物承接四层、task/trial/trajectory/outcome/grader 与污染合同 |
| 合成独立复现状态 | E-C08-021、U-C08-01 和正文章末仍称未独立复现 | 更新为“当前 post-patch harness 已由非作者双目录复现；仅合成范围 PASS” | 不改变 C08 总实践门 `REVIEW_REQUIRED` |

这些修改均为证据定位、claim 限缩或已发生复现的状态同步；没有修改作者 harness、输入、结果或任何实践证据。

## 4. 24 条证据逐条结论

| Evidence | 身份 | 结论 | 核验摘要 |
| --- | --- | --- | --- |
| E-C08-001 | METHODOLOGY | PASS | 训练循环来自 v2/C08 定义权，明确不是外部标准。 |
| E-C08-002 | METHODOLOGY | PASS | 双三角、`AU-L0—AU-L4`、`MAT-L0—MAT-L5` 与术语表一致，且禁止互推。 |
| E-C08-003 | METHODOLOGY | PASS | C04 能力树/NFR 输入可定位，C08 没有反向改写岗位。 |
| E-C08-004 | METHODOLOGY | PASS | C04 风险、负面清单、停止与恢复被消费，阈值仍交 C07/C14/C19。 |
| E-C08-005 | METHODOLOGY | PASS | C05 契约语义与系统强制分开，契约文本没有被写成权限。 |
| E-C08-006 | LOCAL-NORMATIVE | PASS | 已改指 C07 正式蓝图；四层、task/trial、轨迹/终态、grader、污染和三态边界闭合。 |
| E-C08-007 | SOURCE-BASED | PASS | Anthropic 官方工程文给出 task/trial/transcript/outcome/grader 和生产监控补充，正文未写成标准。 |
| E-C08-008 | SOURCE-BASED | PASS | OpenAI 官方指南支持目标、数据、指标、比较与持续评测；正文没有复制示例阈值。 |
| E-C08-009 | SOURCE-BASED | PASS | NIST 明确区分 solution contamination 与 grader gaming；正文未外推发生概率。 |
| E-C08-010 | SOURCE-BASED | PASS | NIST DOE 支持预先定义 objective、factor 与实验计划；账本注明 Agent 非确定性适配边界。 |
| E-C08-011 | SOURCE-BASED | PASS | DeepMind 对 specification gaming 的定义与案例支持“字面指标不等于真实意图”；正文未声称主观欺骗。 |
| E-C08-012 | SOURCE-BASED | PASS | Self-Refine 只用于其七类任务和测试时修订结论，正文已删除未列源的 Reflexion 扩展。 |
| E-C08-013 | SOURCE-BASED | PASS | arXiv 原始论文支持“缺外部反馈时内生自纠可能无效或退化”，未外推所有模型/任务。 |
| E-C08-014 | VERSION-FACT | PASS | OpenClaw release 页同时确认 `v2026.9.6` 和完整 SHA `eb377ac…`。 |
| E-C08-015 | VERSION-FACT | PASS | 固定 commit Workshop 文档直接支持 proposal-first、apply、hash/stale、scanner 与 rollback metadata。 |
| E-C08-016 | VERSION-FACT | PASS | 固定 commit self-learning 文档支持 `off/propose/auto`，并明确 direct maintenance 不总有 proposal/scanner/自动回滚快照。 |
| E-C08-017 | DYNAMIC-OFFICIAL | PASS | Hermes Skills 页面支持 agent-managed skills 与可选 write approval；默认自由写入也被正文边界覆盖。 |
| E-C08-018 | DYNAMIC-OFFICIAL | PASS | Hermes Memory 页面支持 bounded stores、per-profile、Session 起点冻结快照、背景回顾与可选 write approval。 |
| E-C08-019 | VENDOR-CLAIM | PASS | Meta 发布页支持 Goals、Activity/审计可见面、记忆、访问控制与关键动作批准；明确仅为厂商声明。 |
| E-C08-020 | VENDOR-CLAIM | PASS | Muse 设计页支持 Artifacts、side chats、Activity 与 permissions UI；正文不推断内部训练实现。 |
| E-C08-021 | LOCAL-VALIDATION | PASS | 作者结果与非作者 post-patch 双目录复现一致；只证明固定确定性合成 harness 与停止逻辑，不证明真实 Agent 能力。 |
| E-C08-022 | SOURCE-BASED | PASS | Google SRE 支持小范围、限时、control、暂停/回滚；正文明确不机械替代 Agent 风险与授权。 |
| E-C08-023 | SOURCE-BASED | PASS | Anthropic evaluator-optimizer 仅在标准清晰且迭代反馈可测时适用；正文没有把 evaluator 当独立裁判。 |
| E-C08-024 | METHODOLOGY | PASS | D-2026-09-30-15 支持恰好三件母产物及决定内嵌，不存在第四件正式产物。 |

## 5. 三平台事实边界

| 平台 | 核验结论 | 不可外推内容 |
| --- | --- | --- |
| OpenClaw | `v2026.9.6 / eb377ac…` release 与两份固定 commit 文档可解引用；Workshop 与 self-learning 的差异被如实写出 | release 存在不证明目标安装健康；proposal/apply 存在不证明候选有效；`auto` 不等于本书生产门禁 |
| Hermes | Skills 与 Memory 两个动态官方页面在 2026-09-30 可访问，字段和行为与正文匹配 | 不得称为 `0.20.1` 固定事实；批准写入不证明内容正确、形成能力或长期保持 |
| Muse | Meta 发布页与设计页支持用户可见的目标、活动、产物、记忆、权限/批准体验 | 内部 teacher、grader、数据集、模型更新、Skill 格式、日志完整性和安全效果全部未知 |

## 6. 外链、本地路径与解析

- 外部 URL：修改后 17 个唯一 URL，2026-09-30 使用跟随重定向的 HTTP 检查均返回 `200`；关键页面又以正文检索核对，不以状态码代替内容核验。
- 本地 Markdown 链接：正文、三件母产物、两项练习全部可解析，缺失数 `0`。
- 账本本地 source path：全部存在；E-C08-006 已指向 C07 正式蓝图。
- YAML：`evidence-ledger.yaml` 可由 PyYAML 解析；章节包当前 10 个 Markdown frontmatter 可解析；5 个 YAML fenced block 可解析。
- 引用闭合：正文引用 24 个唯一 ID，账本 24 条；missing `0`，orphan evidence `0`。
- 来源登记：账本中 `C08-CARD`、`QUALITY`、`C08-PREFLIGHT`、`C07-PREFLIGHT`、`OAI-GRADERS` 目前是上下文来源而非某条 evidence 的直接 source_ref；属可选 P2 清理，不影响 24 条 claim 闭合。

## 7. P0 事实相关复核

| P0 | 结论 | 事实门依据 |
| --- | --- | --- |
| P0-01 | PASS | 8.1—8.8、导航、案例、仿生、工程、双视图、失败、练习与交接均存在。 |
| P0-02 | PASS | C08 的训练循环/双三角与术语表一致；跨章残余冲突见独立 cross-review，不改变 C08 自身定义事实。 |
| P0-03 | PASS | 24 条主张有身份、来源、定位、日期/稳定性、作用域和限制。 |
| P0-04 | PASS | OpenClaw 版本事实固定到 release/SHA；Hermes 动态、Muse vendor claim 均未伪装固定实现。 |
| P0-05 | PASS | 正文具有停止、恢复和回滚；这里只判事实/设计闭合，真实平台实践仍由实践门判断。 |
| P0-06 | PASS | 高风险写入、发布、扩权均要求外部系统控制/批准，未用提示词代替授权。 |
| P0-07 | REVIEW_REQUIRED | 事实门不批准练习实践；当前独立实践门已另行裁决总体 `REVIEW_REQUIRED`。 |
| P0-08 | PASS | 仿生四段完整，明确工程机制不证明意识或生理学习。 |
| P0-09 | PASS | OpenClaw 固定、Hermes 动态、Muse vendor claim 三层清晰。 |
| P0-10 | PASS | CASE-A 为合成教学；CASE-B/C 为复合设计且未伪造分数/业绩。 |
| P0-11 | PASS | frontmatter 和 YAML 机器块可解析，Agent 程序不扩大权限。 |
| P0-12 | PASS | 未知和开放限制显式保留，章节仍为 `drafting`。 |
| P0-13 | PASS | 安全硬失败不可由训练/综合分抵消。 |
| P0-14 | PASS | 三件母产物均存在、可打开、含 owner 与 consumers。 |
| P0-15 | PASS | 没有行业最强或生产能力提升主张；合成分数明确不是能力证明。 |

## 8. 剩余问题与失效触发器

### P0

无 C08 事实门 P0。

### P1

1. **真实 Runtime 仍未验证。** OpenClaw/Hermes 的真实候选写入、权限强制、访问隔离、Session/Queue/Memory/缓存恢复和外部副作用读回仍为 `UNKNOWN`；不得把事实门 PASS 当实践门 PASS。
2. **Hermes 页面是动态事实。** 任何字段、默认值、命令或页面更新都触发印前重验；若需声称 0.20.1 固定行为，必须增加固定 commit/release 证据。
3. **Muse 仍只有厂商材料。** 后续章节若把这些产品表面写成内部机制或独立安全效果，应立即使相关 claim 退回 `REVIEW_REQUIRED`。

### P2

1. `README.md`、作者自检和部分 exercise/frontmatter 仍保留“事实/实践未开始”或“独立复现待办”的历史作者状态；本次只获授权修改事实/交叉评审文件及明确证据问题，故未做包级状态重写。总编合并前应把当前评审文件设为状态事实来源或统一同步索引。
2. 四个未被 evidence 直接引用的上下文 source 可在编辑门精简；不得为追求“零未用来源”硬造 claim。

## 9. 事实门最终结论

`PASS`。通过的是 C08 公开主张、版本身份与来源边界。章节继续 `drafting`；实践门仍以 [practice-review.md](practice-review.md) 的 `REVIEW_REQUIRED` 为准，交叉门另见 [cross-review.md](cross-review.md)。本记录不得被解释为真实能力提升、真实平台控制有效、生产发布或 `release_candidate` 批准。

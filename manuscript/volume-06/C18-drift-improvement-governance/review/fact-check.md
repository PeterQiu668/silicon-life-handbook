---
review_id: C15-independent-fact-check-20260930
chapter_id: C15
review_type: independent-fact-check
reviewed_on: "2026-09-30"
reviewer_role: evidence-reviewer
chapter_status: drafting
fact_gate: pass
fact_gate_limitations: true
cross_gate: separate_record
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C15 独立事实核查

## 1. 裁决

C15 事实门判 **`PASS（带限制）`**。23 条 evidence 均在正文出现且能被登记来源支持，没有发现固定版本、动态页面、厂商陈述或本地运行计数被事实性误写。25 个 source 中 18 个本地来源全部存在，7 个外部页面本轮均返回 HTTP 200；OpenClaw `v2026.9.6` annotated tag 已重新解引用到固定提交 `eb377ac59e6c9fd6c7705028034812becf00271b`。Hermes 的 Skill/Memory 写入审批只按 2026-09-30 动态官方页处理，Muse 的“从对话学习、getting sharper”只作 `VENDOR-CLAIM`。

作者 75-trial 保存结果在两个 fresh 临时目录中按字节复现，`20 PASS / 45 FAIL / 10 REVIEW_REQUIRED`、唯一 task/trial、全部期望匹配、零外部副作用与安全失败非补偿均成立。这只证明离线规则夹具的记录完整性，不证明真实平台、生产 shadow/canary、外部审批、完整 bundle 回滚或长期改善。

事实门有一项 P2：`C13` 与 `C22` 已登记为 source 但未被任何 claim 使用。D22 合成数据被标入真实任务层、以及 C12/C13 依赖拓扑问题属于跨章规范缺陷，分别记录在 [cross-review.md](cross-review.md)，不把准确的 75-trial 计数倒判为虚假事实。

本审校不执行两项练习的独立实践门，不批准编辑、总编或 `release_candidate`。

## 2. 核查方法

- 逐条核对 23 个 evidence claim 的来源身份、正文引用、实际支持与限制；
- 检查 25 个 source 的本地存在性、外部可达性和 claim 消费关系；
- 通过 GitHub 官方 API 解引用 OpenClaw annotated tag，并直接核对固定提交的 Skill Workshop 与 Self-learning 文档；
- 核对 Hermes Skills/Memory 动态页的 `write_approval` 语义、Muse 厂商原文身份和 Google SRE canary 定义；
- 将作者 input/runner 复制到两个 fresh 临时目录运行，对 fresh/fresh 和 fresh/saved 做字节及 SHA-256 比较；该步骤只核验 E-C15-022/023，不构成实践门；
- 重新计算 source/claim/正文 evidence 集合、H2 编号、母产物和练习数量。

逐源及逐 claim 机器记录见 [source-audit-20260930.yaml](source-audit-20260930.yaml)。

## 3. 23 条 evidence 逐项结论

| Evidence | 身份 | 结论 | 核查摘要 |
| --- | --- | --- | --- |
| E-C15-001 | METHODOLOGY | PASS | 漂移相对批准基线，可能是改进、退化、分化或假象，不等同变差。 |
| E-C15-002 | METHODOLOGY | PASS | 一级分类严格为能力、人格、文档、工具、目标五类。 |
| E-C15-003 | METHODOLOGY | PASS | 记忆/上下文只作跨类型状态与证据源；C10 生命周期定义权保留。 |
| E-C15-004 | METHODOLOGY | PASS | 变化信号、确认漂移、因果证明三层分开。 |
| E-C15-005 | METHODOLOGY | PASS | baseline bundle 覆盖业务、契约、系统、授权、评测、运行、证据，明确是本书方法。 |
| E-C15-006 | METHODOLOGY | PASS | 同任务、预算、风险、权限、环境比较与 C07 公平比较原则一致。 |
| E-C15-007 | METHODOLOGY | PASS | 失败只能生成改进候选，不自动生成活动规则。 |
| E-C15-008 | METHODOLOGY | PASS | 观察—假设—实验—评估—固化闭环中，固化必须外部批准。 |
| E-C15-009 | METHODOLOGY | PASS | 每轮单一主干预，同时保留混杂、失败、成本和延迟。 |
| E-C15-010 | METHODOLOGY | PASS | grader 迎合和 holdout 污染被明确排除为改进证据。 |
| E-C15-011 | METHODOLOGY | PASS | D22 规范陈述正确；作者运行的数据来源标签另由交叉门处理。 |
| E-C15-012 | METHODOLOGY | PASS | version bundle 和 exact diff 范围完整，未伪装成平台自动能力。 |
| E-C15-013 | METHODOLOGY + PRIMARY PRACTICE | PASS | shadow 零写、canary/control/停止/回滚与 Google SRE 基础实践兼容；独立授权是本书加严要求。 |
| E-C15-014 | METHODOLOGY | PASS | 回滚相容 bundle 且不复活撤销权限/删除同意，真实平台传播仍公开为限制。 |
| E-C15-015 | METHODOLOGY | PASS | 人类定目标、批变更、担责任三处不可外包，属于治理裁决。 |
| E-C15-016 | METHODOLOGY | PASS | Agent 不得自改安全、grader、权限、自主半径、目标或生产资产。 |
| E-C15-017 | METHODOLOGY | PASS | 目标/权限变化返回 C14 再认证；AU 与 MAT 不互推。 |
| E-C15-018 | VERSION-FACT | PASS | 固定 OpenClaw 文档确实区分 off/propose/auto，auto 为默认，direct maintenance 不保证 proposal/rollback；正文未把默认能力当治理效果。 |
| E-C15-019 | DYNAMIC-OFFICIAL | PASS | Hermes Skills/Memory 动态页支持 `write_approval`，正文没有用一次写入批准证明长期改善。 |
| E-C15-020 | VENDOR-CLAIM | PASS | Muse “getting sharper”只按 Meta 产品陈述处理，未推断内部自改机制。 |
| E-C15-021 | METHODOLOGY | PASS | artifacts 目录恰好三件正式母产物。 |
| E-C15-022 | LOCAL-VALIDATION | PASS IN DECLARED SYNTHETIC SCOPE | 75 trial、20/45/10、唯一 ID、零外部副作用与保存和 fresh 复跑一致。 |
| E-C15-023 | LOCAL-VALIDATION | PASS IN DECLARED SYNTHETIC SCOPE | 五类漂移、混杂、grader/污染、多变量、自改治理、shadow、rollback、UNKNOWN 均可定位。 |

## 4. 平台与外部实践身份

### 4.1 OpenClaw 固定版

[OpenClaw v2026.9.6](https://github.com/openclaw/openclaw/releases/tag/v2026.9.6) 的 annotated tag 指向 `eb377ac59e6c9fd6c7705028034812becf00271b`。该提交的 [Skill Workshop](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/tools/skill-workshop.md)说明 proposal 可以带目标绑定、scanner 状态、hash 和 rollback metadata，同时明确后台学习与 weekly collection 的普通文件维护不会生成 proposal 或自动 rollback snapshot。[Self-learning](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/tools/self-learning.md)明确 `off / propose / auto` 三种模式，`auto` 为默认；direct maintenance、explicit proposal 与 immediate repair 的审计/扫描/回滚语义并不相同。

正文把这些写成“产品默认不等于本书治理效果”，没有声称真实 OpenClaw 已运行、自动学习必然改善或 proposal 自动满足独立评测。因此 E-C15-018 为 `PASS`。

### 4.2 Hermes 动态官方文档

[Hermes Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)与 [Hermes Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/)当前分别公开 `skills.write_approval` 和 `memory.write_approval`：启用时，相关写入可提示或 staged for review；页面也显示默认可为关闭状态。C15 只把它们作为核验日动态能力映射，不倒填固定发行，不推导批准内容正确、没有漂移或长期改善。

结论为 `PASS WITH DYNAMIC RECHECK`。印前和目标环境使用前仍须重验。

### 4.3 Muse 与 Google SRE

[Meta Muse 发布材料](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)确实使用“learning from conversations”“getting sharper”等产品语言，并说明记忆/forget 等用户控制。正文没有把这些厂商文字升级为独立效果证据或可执行自改机制，结论为 `PASS AS VENDOR-CLAIM`。

[Google SRE Canarying Releases](https://sre.google/workbook/canarying-releases/)把 canary 定义为部分且限时的变更部署和评估，强调 canary/control、代表性、指标、停止与回滚。C15 在此基础上增加对象授权、零写 shadow、外部责任与 bundle 回滚，属于本书治理要求，未称为 Google 原生 schema。

## 5. 作者运行的事实完整性

两个 fresh 临时目录均复现作者保存结果：

```text
drift types: capability / persona / document / tool / goal
tests per type: 15
trials: 75
distribution: PASS 20 / FAIL 45 / REVIEW_REQUIRED 10
unique task/trial pairs: true
all expected matched: true
external effects zero: true
security failures noncompensatory: true
results SHA-256: fc55abe29d9e9b7975ec5323483204a0a7b68a884647e8e086486d931987dd0c
summary SHA-256: b42ea222b50e3087acc74292809616bec3bc1d2b0539b9ae5a5175d23359a494
fresh/fresh bytes: identical
fresh/saved bytes: identical
```

这证明本地运行声明准确，不证明 75 条记录具有真实业务数据来源，也不替代 X-C15-01/02 的独立执行。

## 6. 问题分级与关闭条件

### P0

无。未发现平台身份伪造、Muse 被写成已验证实现、Agent 自固化被允许、失败样本被删除、撤销权限允许复活或本地计数虚报。

### P1

无事实门 P1。D22 数据谱系和正式依赖拓扑分别为 `P1-X15-01/02`，由交叉门处理。

### P2

1. **P2-F15-01 / 两个 source 未被 claim 消费。** `C13` 与 `C22` 文件存在，但未出现在任一 claim 的 `source_ids`。关闭条件：若正文关键主张确由其支持，将其绑定到明确 claim 并复核语义；若只作写作背景，从 ledger source 集合移除。不得为了计数增加空主张。

## 7. 事实门结构化裁决

```yaml
fact_gate:
  chapter_id: C15
  primary_three_state_verdict: PASS
  limitations_present: true
  claims_checked: 23
  claims_pass_or_pass_with_declared_limitation: 23
  claims_review_required: 0
  claims_fail: 0
  sources_checked: 25
  local_sources_present: "18/18"
  external_sources_http_200: "7/7"
  sources_used_by_claims: "23/25"
  evidence_reference_closure: "23/23"
  openclaw_fixed_release_resolution: PASS
  hermes_dynamic_identity: PASS_WITH_RECHECK_TRIGGER
  muse_vendor_identity: PASS
  author_run_claim_integrity: PASS_IN_DECLARED_SYNTHETIC_SCOPE
  independent_practice_performed: false
  practice_approved: false
  editor_approved: false
  chief_editor_approved: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

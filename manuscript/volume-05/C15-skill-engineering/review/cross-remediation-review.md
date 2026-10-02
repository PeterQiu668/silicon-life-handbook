---
review_id: C12-cross-remediation-review-20260930
chapter_id: C12
review_type: independent-fact-and-cross-remediation-regression
reviewed_on: "2026-09-30"
reviewer: "independent-fact-and-cross-reviewer:legacy_mapping"
review_scope: "D22, CISA draft identity, source closure, D20-D23, C02/C09 interfaces, separators, evidence closure"
fact_gate_after_regression: PASS
cross_gate_after_regression: PASS_WITH_LIMITATIONS
p0_open: 0
p1_open: 0
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
chapter_status_after_review: drafting
---

# C12 事实与交叉修补回归

## 1. 裁决

本次只读回归确认，前次事实/交叉审校提出的 P0 与 P1 已全部关闭：D22 已严格恢复为四个规范数据层，CISA 文件的 public-comment draft 身份已进入 source title、claim 和正文，41 个 ledger source 全部被 claim 消费，D20—D23 已显式绑定，C02/C09 依赖及 C09 终态交接已经闭合，连续重复水平分隔符已清理，28 条 evidence 与正文保持双向闭合。

- 事实门继续为 `PASS`。
- 交叉门由 `REVIEW_REQUIRED` 更新为 `PASS_WITH_LIMITATIONS`。
- 本裁决只关闭事实与交叉修补项，不代表实践、编辑、总编或发布候选批准；章节继续保持 `drafting`。

此前的 [fact-check.md](fact-check.md)、[cross-review.md](cross-review.md) 与 [fact-source-audit-20260930.yaml](runs/fact-source-audit-20260930.yaml) 是修补前的时间点记录，不应回写覆盖。涉及 D22 和 unused source 的当前状态，以本回归为准。

## 2. 六项回归结果

| 检查项 | 当前证据 | 结论 |
| --- | --- | --- |
| D22 四层与安全横切 | `chapter.md` 12.7.2 明列 `training / regression / holdout / representative real-world`；security/red-team 明确为横跨四层的非补偿切片，安全硬失败直接阻断；E-C12-015 同步 | PASS |
| CISA draft 身份 | source title 写明 public comment draft；E-C12-012 写明 public-comment draft 与“不是最终规则”；正文 12.8.1 首次引用同样标明 draft | PASS |
| source 闭合 | ledger 41 个 source，41 个均至少被一条 claim 使用；0 unused、0 missing；18 个本地来源存在，23 个外链本轮均返回 HTTP 200 | PASS |
| D20—D23 与依赖接口 | `DECISIONS` 绑定 E-C12-014/015/016/026/028；C02/C09 同时存在于 chapter frontmatter 和 CHAPTER-CARDS；C09 source 被 E-C12-016 消费 | PASS |
| 水平分隔符 | 忽略空行扫描后，连续 `---` 对为 0 | PASS |
| evidence 双向闭合 | ledger 28 个 claim ID 唯一；正文引用 28/28；0 missing、0 orphan；所有 claim 引用的 source 均存在 | PASS |

## 3. D22 回归

### 3.1 规范表达

12.7.2 当前把四个数据层及其用途逐项写清：

1. `training` 用于验证训练干预；
2. `regression` 用于防止已冻结能力退化；
3. `holdout` 用于检查泛化；
4. `representative real-world` 用于在低风险、已获权、可回滚的范围内观察真实代表性。

同一段明确声明 security/red-team 是横跨四层的非补偿切片，可在各层注入对抗场景，任何安全硬失败均直接阻断发布。E-C12-015 使用完全相同的四层与横切语义，并引用 C07、C08、`DECISIONS` 和 C12 preflight。原先“对抗集与三层并列、真实任务另行观察”的第五层表达已不存在。

设计卡和练习仍出现 `routing_suite`、`regression_suite`、`held_out_suite`、`adversarial_suite` 等测试套件名称。它们没有被称为数据层；其中 adversarial 是横切套件，因而不构成第五层。若未来把这些模板转换为逐样本数据表，必须额外记录四层中的一个 `data_layer`，不得用 `adversarial` 替代 `representative real-world`。

**裁决：前次 P0 已关闭，D22 为 `PASS`。**

## 4. CISA draft 身份回归

三处关键表达一致：

- ledger source `CISA-SBOM` 的标题为 “CISA 2025 SBOM Minimum Elements public comment draft”；
- E-C12-012 明确称其为 public-comment draft，并在 limitations 中写明“CISA 文件不是最终规则”；
- 正文 12.8.1 首次实质引用写作“CISA 2025 年 SBOM 最小要素 public-comment draft”。

正文只把该文件作为软件组件、版本、身份和关系字段的参考，没有将其改写成已生效的最终政府要求，也没有用它证明 Skill 指令、评测或业务权限完整性。

**裁决：前次 CISA 身份 P1 已关闭，为 `PASS`。**

## 5. 41 个 source 与 D20—D23 回归

### 5.1 source 使用闭合

当前 ledger 的 41 个 source 由 18 个本地来源和 23 个外部来源组成。source ID 集合与 28 条 claim 的 `source_ids` 并集完全相等：

```yaml
source_closure:
  ledger_sources: 41
  local_sources_exist: "18/18"
  external_sources_http_200: "23/23"
  sources_used_by_claims: 41
  unused_sources: 0
  missing_sources: 0
```

前次未使用的 `AS-PRACTICE`、`C05`、`C10-ARCH`、`C11-CONTRACT` 已分别绑定到渐进披露、权限边界或 Memory 提案 claim；旧的 `OC-CREATE` 已从 ledger 删除，而实际需要的 `C09` 已加入并由 E-C12-016 使用。没有为了达到 41/41 而创建空 claim。

### 5.2 D20—D23 显式绑定

| 决策 | 当前 claim 绑定 | 回归判断 |
| --- | --- | --- |
| D20 五类漂移 | E-C12-014 的限制明确 C15 拥有 D20 五类漂移；E-C12-028 明确不重定义漂移并引用 `DECISIONS` | PASS |
| D21 三层完成证据 | E-C12-016 分离任务、Artifact、交付与环境终态，限制明确不得以技术执行替代 D21 完成证据 | PASS |
| D22 四层 + 安全横切 | E-C12-015 逐字记录四层及 security/red-team 横切非补偿语义 | PASS |
| D23 C22 七节与依赖 | E-C12-028 把事件输出给 C22，同时明确不重定义 C22 七节规范目录 | PASS |

`DECISIONS` source title 已从早期只列 D13/D18 更新为 D13/D18/D20/D21/D22/D23，并被上述 claim 实际消费。

**裁决：source hygiene 与 D20—D23 显式证据两个 P1 均已关闭。**

## 6. C02/C09 依赖和终态接口

`chapter.md` 与 `CHAPTER-CARDS.md` 的 C12 `depends_on` 当前完全一致：

```yaml
depends_on: [C02, C05, C06, C07, C08, C09, C10, C11]
```

- C02：正文把训练/生产双闭环明确归给 C02；C08 只继续提供训练干预、轮次、双三角、停训和候选证据链。E-C12-014 同步绑定 C02，不再把双闭环错误归给 C08。
- C09：ledger 增加 C09 正文为 source；E-C12-016 使用 C09 与 D21，要求撤回时分离任务、Artifact、交付和环境终态。正文还明确把长任务恢复归于 Workflow/C09，并要求把路由、加载、执行、交付与环境读回拆开。技术动作或 Plugin 自报不能替代交付与环境终态证据。

因此，C09 不再只是正文偶然提及，而是同时进入机器依赖、章节卡、source 和终态 claim。

**裁决：前次 C09 依赖/交接 P1 已关闭，为 `PASS`。**

## 7. 结构与 evidence 回归

- chapter 正文忽略空行后没有连续水平分隔符；前次编辑型重复已清理。
- ledger 有 28 个 evidence ID，全部唯一。
- 正文出现的 `E-C12-001`—`E-C12-028` 与 ledger 集合完全相等。
- 没有正文 orphan ID，也没有 ledger claim 未被正文引用。
- 所有 `source_ids` 均指向已登记 source。
- 本次未修改被审正文、ledger、母产物、练习、作者 runs 或既有审校记录。

## 8. 剩余限制与非本门事项

以下限制不会重新打开事实或交叉 P0/P1，但必须继续保留：

1. Agent Skills 动态规范和实验性 `allowed-tools` 需要在出版前复核；当前通过只针对 2026-09-30 核验身份。
2. OpenClaw 目标部署、Hermes 动态页面与固定实现逐项对应、Muse 内部机制、真实 Plugin 和跨 Runtime 撤回传播尚未完成独立实践。
3. `adversarial_suite` 只可解释为横切安全套件；任何后续模板或数据转换都必须另带四层 `data_layer`。
4. 既有事实/交叉审校文件保留历史失败，供审计变更过程；自动汇总工具应读取本文件的当前裁决，不应把历史 `REVIEW_REQUIRED` 当作仍未修复。
5. 章名在 v2、章节卡和 chapter frontmatter 中仍有“插件体系/版本”措辞差异，属于后续编辑一致性事项，不影响本次事实与交叉门。

## 9. 最终结构化裁决

```yaml
remediation_regression:
  chapter_id: C12
  d22_four_data_layers: PASS
  d22_security_red_team_cross_cutting_non_compensable: PASS
  cisa_public_comment_draft_identity: PASS
  sources_used: "41/41"
  source_missing: 0
  source_unused: 0
  d20_explicit_binding: PASS
  d21_explicit_binding: PASS
  d22_explicit_binding: PASS
  d23_explicit_binding: PASS
  c02_frontmatter_and_card: PASS
  c09_frontmatter_and_card: PASS
  c09_source_and_terminal_state_handoff: PASS
  duplicate_horizontal_separator_pairs: 0
  evidence_bidirectional_closure: "28/28"
  p0_open: 0
  p1_open: 0
  fact_gate: PASS
  cross_gate: PASS_WITH_LIMITATIONS
  practice_gate: NOT_REVIEWED
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
  chapter_status_after_review: drafting
```

## 10. 验证命令

本回归使用以下只读检查：

```bash
python3 scripts/validate-formal-manuscript.py
python3 scripts/validate-book.py
python3 -c 'import yaml; yaml.safe_load(open("manuscript/volume-04/C12-skill-engineering/evidence-ledger.yaml"))'
git diff --check -- .
```

另以脚本计算 source/claim 集合、正文 evidence ID 集合、两处 `depends_on`、本地路径存在性、外链 HTTP 状态和连续分隔符；并对本新增文件做限定 whitespace 检查。验证结果以本文件落盘后的最终运行输出为准。

### 最终运行结果

- C12 包内 4 个 YAML：解析 PASS；9 个带 frontmatter 的 Markdown：解析 PASS。
- source/claim/依赖/分隔符专项断言：PASS；41 used sources、28 unique claims、两处依赖列表一致、连续分隔符为 0。
- `validate-formal-manuscript.py`：PASS；8 卷、24 章、178 个正文三级节点、13 个已存在章节包，C12 为 18,651 CJK；仅剩“后续 11 章包未完成”这一项全书预期 warning。
- `validate-book.py`：PASS；扫描 284 个 Markdown，检查 1,317 条本地链接。
- `git diff --check -- .`：PASS；本新增文件的限定 `--no-index --check` 无 whitespace 输出，退出码 1 仅表示新文件相对 `/dev/null` 存在差异。

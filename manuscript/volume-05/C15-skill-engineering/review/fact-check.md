---
review_id: C12-independent-fact-check-20260930
chapter_id: C12
review_type: independent-fact-check
reviewed_on: "2026-09-30"
reviewer: "independent-fact-and-cross-reviewer:legacy_mapping"
chapter_status_after_review: drafting
claims_checked: 28
sources_checked: 41
fact_gate: PASS
open_items: REVIEW_REQUIRED
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C12 独立事实核查

## 1. 事实门结论

**28 条 claim 均能在其声明的证据身份和限制内得到支持，正文 28/28 双向闭合，事实门为 `PASS`。** 这不是无条件通过：CISA 文件实际是 2025 年 8 月 public comment draft，Hermes `main` 与 Agent Skills 当前规范仍属动态来源，Muse 只能保持 `VENDOR-CLAIM`，作者合成运行只可作为作者记录。上述项目继续为 `REVIEW_REQUIRED` 的出版前或实践复核项，不改变本轮 claim 支持结论。

本轮按当前 ledger 重新只读核验 41 个 source：17 个本地路径全部存在，24 个外链全部返回 HTTP 200。新增的 `C02` 来源已实际绑定 `E-C12-014`，用于承载训练/生产双闭环的定义权；C08 只承载训练干预、轮次、双三角、停训与候选证据链。结构化记录见 [fact-source-audit-20260930.yaml](runs/fact-source-audit-20260930.yaml)。没有修改 `chapter.md`、`evidence-ledger.yaml`、母产物、练习或作者 runs。

## 2. 来源闭合与可达性

| 指标 | 结果 | 裁决 |
| --- | ---: | --- |
| ledger source | 41 | PASS |
| 本地 source | 17/17 存在 | PASS |
| 外部 source | 24/24 HTTP 200 | PASS |
| claim | 28/28 ID 唯一 | PASS |
| 正文引用 | 28/28 claim 被引用 | PASS |
| 正文孤儿 evidence ID | 0 | PASS |
| claim 引用不存在的 source | 0 | PASS |
| ledger 未被 claim 使用的 source | 5 | REVIEW_REQUIRED（证据卫生） |

未被 claim 使用的 source 为 `AS-PRACTICE`、`C05`、`C10-ARCH`、`C11-CONTRACT`、`OC-CREATE`。这些文件都可达，但不能仅因被列入 ledger 就声称已经参与论证；印前应删除未用来源，或把它们绑定到真正需要的 claim。

## 3. 41 个 source 的身份与支持

### 本地来源

| Source | 可达 | 内容支持/用途 | 结论 |
| --- | --- | --- | --- |
| BOOK-V2 | 是 | 12.1—12.8、定义权、三件母产物 | PASS |
| C12-CARD | 是 | 章节角色、问题、平台边界、练习与 P0 | PASS |
| QUALITY | 是 | 生产模板、三态、权限和证据门 | PASS |
| TERMS | 是 | Skill/Plugin/Tool/Workflow/Hook/Provider 定义权 | PASS |
| DECISIONS | 是 | D18/D20/D21/D22/D23 | PASS；D22 正文冲突见交叉审校 |
| C12-PREFLIGHT | 是 | C12 固定事实、方法、失败与接口 | PASS |
| C02 | 是 | 训练/生产双闭环的定义权 | PASS |
| C05 | 是 | 契约与人格文本不授权 | REVIEW_REQUIRED：未被 claim 使用 |
| C06 | 是 | Runtime、Provider、Channel、执行与隔离边界 | PASS |
| C07 | 是 | task/trial、四数据层、三态与硬门 | PASS；正文 D22 表达需修 |
| C08 | 是 | 训练干预、轮次、双三角、停训与候选证据链 | PASS |
| C10 | 是 | 程序性 Memory 不自产权限/发布 | PASS |
| C10-ARCH | 是 | Memory 架构 | REVIEW_REQUIRED：未被 claim 使用 |
| C11 | 是 | Tool/MCP、Policy、Approval、Sandbox、终态 | PASS |
| C11-CONTRACT | 是 | Tool 合同 | REVIEW_REQUIRED：未被 claim 使用 |
| LOCAL-C12-RUN | 是 | 20 trial 与门禁分布 | PASS；仅作者记录 |
| LOCAL-C12-SCRIPT | 是 | 作者确定性路由脚本 | PASS；仅作者记录 |

### 外部来源

| Source | HTTP | 证据身份 | 内容支持 | 结论 |
| --- | ---: | --- | --- | --- |
| AS-SPEC | 200 | 动态规范 | `SKILL.md`、必填/可选字段、实验 `allowed-tools`、渐进披露 | PASS |
| AS-CLIENT | 200 | 动态官方指南 | metadata→instructions→resources 三层加载 | PASS |
| AS-PRACTICE | 200 | 动态官方指南 | authoring 实践 | REVIEW_REQUIRED：未被 claim 使用 |
| OC-REL | 200 | 固定 release | tag `v2026.9.6` | PASS |
| OC-SKILLS | 200 | 固定 commit | 多来源优先级、managed revision、Session 选择、allowlist 非 host 授权 | PASS |
| OC-CREATE | 200 | 固定 commit | Skill 创建入口 | REVIEW_REQUIRED：未被 claim 使用 |
| OC-WORKSHOP | 200 | 固定 commit | proposal 与后台直接维护的分界 | PASS |
| OC-WORKSHOP-LIFECYCLE | 200 | 固定 commit | pending/hash/scanner/apply/stale/rollback | PASS |
| OC-SELF | 200 | 固定 commit | off/propose/auto；即时修复与后台维护差异 | PASS |
| OC-PLUGIN | 200 | 固定 commit | 扩展面、install policy、allow/deny、workspace 默认、quarantine | PASS |
| OC-PLUGIN-CLI | 200 | 固定 commit | Plugin 生命周期命令面 | PASS |
| HE-REL | 200 | 固定 release | `v0.20.1 / v2026.8.13` | PASS |
| HE-SKILLS-FIXED | 200 | 固定 tag 文档 | progressive disclosure、CRUD/Hub、write approval、scan/hash | PASS |
| HE-PLUGIN-FIXED | 200 | 固定 tag 文档 | enable/disable/update/remove、exact pin、capability consent 非 sandbox | PASS |
| HE-PLUGIN-DYNAMIC | 200 | 动态官方文档 | native/portable Plugin 与 MCP/Skill 扩展 | PASS，限 2026-09-30 |
| SLSA | 200 | v1.2 规范 | provenance 的来源、时间、生产方式与 builder | PASS |
| SIGSTORE | 200 | 官方动态指南 | 身份证书、签名、透明日志和验证 | PASS |
| CISA-SBOM | 200 | 官方 public comment draft | 组件、版本、标识和依赖关系 | PASS，标题需标 draft |
| SPDX | 200 | v3.0.1 规范 | 软件元素、标识与关系表达 | PASS |
| NIST-SSDF | 200 | SP 800-218 v1.1 | 安全软件开发生命周期指导 | PASS |
| TUF | 200 | 官方安全指南 | rollback/freeze/mix-and-match/key compromise/revocation | PASS |
| OWASP-AGENTIC | 200 | 2026 官方指南 | Agentic 风险框架；C12 的具体清单由 preflight 方法化 | PASS；范围限正文所述 |
| MUSE-NEWS | 200 | 厂商声明 | Secure VM、用户控制、审批与 audit trail | PASS；仅 VENDOR-CLAIM |
| MUSE-SEC | 200 | 厂商声明 | skills/connectors、自建工具、Sentinel、privsep、credential surrogation | PASS；仅 VENDOR-CLAIM |

OpenClaw release tag 解引用到 `eb377ac59e6c9fd6c7705028034812becf00271b`；Hermes release tag 解引用到 `f80f453ae0679347e38abc917c7f94f717bf96c5`。固定与动态来源没有互相倒填。

## 4. 28 条 claim 逐项裁决

| ID | 结论 | 核查摘要 |
| --- | --- | --- |
| E-C12-001 | PASS | Skill 的程序性知识包定义与术语表、规范和 preflight 一致。 |
| E-C12-002 | PASS | 当前规范明确目录至少含 `SKILL.md`，`name` 与 `description` 必填。 |
| E-C12-003 | PASS | 四个可选字段与 `allowed-tools` 实验身份准确；正文未把它当 Runtime 权限。 |
| E-C12-004 | PASS | 官方客户端指南明确 metadata、instructions、resources 渐进装载。 |
| E-C12-005 | PASS | 七类扩展对象分型是本书方法，产品名称未被强制同构。 |
| E-C12-006 | PASS | Skill/脚本引用与 Tool、secret、network、host、业务授权保持分离。 |
| E-C12-007 | PASS | Registry 字段明确标本书方法，不冒充规范字段。 |
| E-C12-008 | PASS | Plugin 被按执行代码与生命周期治理；平台默认仍明确受版本限制。 |
| E-C12-009 | PASS | digest、签名、provenance、SBOM、扫描、评测的非替代关系成立。 |
| E-C12-010 | PASS | SLSA v1.2 明确 provenance 描述产物从何处、何时、如何产生及 builder。 |
| E-C12-011 | PASS | Sigstore 官方材料支持签名、身份关联与透明日志；正文保留被攻破限制。 |
| E-C12-012 | PASS | CISA/SPDX 支持组件、版本、身份、关系；Skill 扩展字段明确是本书方法。CISA 标题须补 public comment draft。 |
| E-C12-013 | PASS | TUF 官方安全页逐项支持 rollback、freeze、mix-and-match、key compromise 与替换/撤销。 |
| E-C12-014 | PASS | Memory 只形成 proposal；训练/生产双闭环归 C02，C08 只细化训练干预、轮次、双三角、停训与候选证据链，C10/C15 权属未被重写。 |
| E-C12-015 | PASS | 候选链是本书方法；不宣称平台原生全具备。 |
| E-C12-016 | PASS | 撤回传播范围与 Runtime/训练边界一致，未知副本保持 REVIEW_REQUIRED。 |
| E-C12-017 | PASS | OpenClaw 固定文档支持多来源、优先级、managed revisions 与 Session 保留选择。 |
| E-C12-018 | PASS | 固定 Workshop 文档支持 pending、binding、hash、scanner、apply、stale、rollback。 |
| E-C12-019 | PASS | 固定文档支持 off/propose/auto；后台 auto 直接维护无 proposal/自动 snapshot，正文未把它作为生产建议。 |
| E-C12-020 | PASS | 固定 Plugin 文档支持扩展面、策略、allow/deny、生命周期与 payload failure quarantine。 |
| E-C12-021 | PASS | Hermes 固定 Skills 文档支持 progressive disclosure、CRUD/Hub 与可配置 write approval。 |
| E-C12-022 | PASS | Hermes 固定 Plugin 文档支持生命周期、精确 commit pin、capability consent，并明确不是 sandbox。 |
| E-C12-023 | PASS | `main` 页面只按 2026-09-30 动态事实使用，没有倒填固定 release。 |
| E-C12-024 | PASS | Meta 页面支持相关产品与安全自述，正文始终标为 VENDOR-CLAIM，未推断格式兼容。 |
| E-C12-025 | PASS | OWASP 提供 Agentic 风险框架，具体攻击面由 C12 preflight 归纳，且完整威胁模型归 C19。 |
| E-C12-026 | PASS | D18、v2 和章节卡一致冻结三件母产物。 |
| E-C12-027 | PASS | 作者结果确为 20 trial、13 PASS、5 FAIL、2 REVIEW_REQUIRED；只作作者记录，不作独立实践签核。 |
| E-C12-028 | PASS | 输出给 C15/C19/C21 的边界成立，下游未冻结部分仍需后续回归。 |

未发现 unsupported claim 或需要直接判 `FAIL` 的事实主张。

## 5. OpenClaw 固定版退役文件核验

固定 commit 的 `docs/reference/templates/TOOLS.md` 明确写明 workspace `TOOLS.md` 已退役，工具与环境说明迁入 `AGENTS.md` 的 `## Tools`；`docs/reference/templates/HEARTBEAT.md` 明确写明 workspace `HEARTBEAT.md` 已退役，不再由 Runtime 读取，指令迁入 system-owned monitor scratch。

C12 正文、三件母产物和两项练习对两个旧 workspace 文件的运行时引用均为 0，没有复活旧载体，也没有把 Heartbeat 自动化与 Skill/Plugin 混为同一对象。它们不是 C12 的主事实，因此 ledger 未额外建立 claim；若后续加入相关表述，必须引用固定退役页，而不是依据历史旧稿。

## 6. 稳定性边界

- Agent Skills 规范当前无本章固定版本号，`allowed-tools` 仍为实验字段；出版前复核状态为 `REVIEW_REQUIRED`。
- OpenClaw 所有产品事实均绑定固定 commit；目标部署配置与真实传播效果仍为 `REVIEW_REQUIRED`。
- Hermes fixed tag 与 `main` 动态文档分栏正确；动态页不能证明 `v0.20.1` 已完整实现 portable/native 新表面。
- Muse 只支持“Meta 官方材料声称”，不支持内部实现、安全效果、Agent Skills 或 MCP 兼容结论。
- CISA PDF 是 public comment draft，不得改写为已经定稿的美国政府最终要求。
- 作者本地运行只验证合成判定合同；实践门必须另行复现。

## 7. 事实门 P0 / P1 / P2

### P0

- 无事实型 P0。28 条 claim 均有支持，未发现动态或厂商材料被提升为固定独立事实。

### P1

1. `CISA-SBOM` source title 未标注 public comment draft；正文的“CISA SBOM 最小要素”也应在首次出现处明确 draft 身份。
2. ledger 有 5 个未被 claim 使用的 source；印前需绑定或删除，避免把“列入参考文献”误当“已经支撑 claim”。
3. D20—D23 没有作为独立 source/claim 进入 ledger。内容大体遵守，但 D22 已在交叉门出现实际冲突，说明决策引用不应只依赖间接 preflight。

### P2

1. 章名在章节卡、v2 与 chapter frontmatter 中分别省略或增加“Plugin/版本”字样；不影响事实，但合订目录需统一。
2. 动态网页的 HTTP 200 只能证明核验日可达；印前仍需重验页面内容与状态。

## 8. 事实门结构化结论

```yaml
fact_gate:
  chapter_id: C12
  claims_supported: "28/28"
  local_sources_exist: "17/17"
  external_sources_http_200: "24/24"
  openclaw_fixed_boundary: PASS
  hermes_fixed_dynamic_split: PASS
  muse_vendor_claim_boundary: PASS
  openclaw_retired_workspace_files: PASS
  cisa_draft_identity: REVIEW_REQUIRED
  unused_source_hygiene: REVIEW_REQUIRED
  overall: PASS
  chapter_status_after_review: drafting
  practice_gate: NOT_REVIEWED
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

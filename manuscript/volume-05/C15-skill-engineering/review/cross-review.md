---
review_id: C12-independent-cross-review-20260930
chapter_id: C12
review_type: independent-cross-chapter-cross-platform-review
reviewed_on: "2026-09-30"
reviewer: "independent-fact-and-cross-reviewer:legacy_mapping"
chapter_status_after_review: drafting
cross_gate: REVIEW_REQUIRED
blocking_issue: D22_DATA_LAYER_CONFLICT
fact_review_ref: "review/fact-check.md"
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C12 交叉一致性审校

## 1. 交叉门结论

**C12 的 12.1—12.8、三件母产物、Skill/Plugin 主定义权、权限边界、三平台证据身份、仿生四段、案例、练习和主要章际交接总体一致；但 12.7.2 把“对抗集”写成与 training/regression/holdout/真实任务并列的数据集层级，与 D22 的四数据层 + 横跨安全切片裁决冲突。交叉门因此为 `REVIEW_REQUIRED`。**

该冲突不影响事实源真假，却会使 C07→C12 的训练数据接口出现第五层，因此不能用其他章节优点补偿。按任务约束，本审校不修改 `chapter.md`；修复后需重新检查 chapter、A-C12-01 与两项练习中数据层和红队语言。

## 2. 结构、目录与 D18

| 项目 | 观察 | 结论 |
| --- | --- | --- |
| 正文章节 | 恰好 `12.1`—`12.8`，无 `12.9` | PASS |
| 全书正式三级节点 | formal validator 仍为 178 | PASS |
| 正文篇幅 | 18,624 CJK，位于 18,000—24,000 | PASS |
| 母产物 | 恰好 A-C12-01、02、03 | PASS |
| 嵌入字段 | 解剖→01；类型边界→02；Registry/SBOM/撤回/替代→03 | PASS |
| 练习 | X-C12-01 与 X-C12-02 | PASS；仅设计审查，实践未审 |
| 新增第四母产物 | 无 | PASS |

D18 得到完整执行。章内的 component manifest、capability diff、Registry、SBOM、撤回和残余均为三件母产物的嵌入字段，没有另造正式母产物。D23 针对 C22 的七节约束也未被 C12 扩写成 C22 新目录；C12 只向 C22 交事件字段。

## 3. 定义权与权限边界

| 对象 | 主定义章 | C12 使用方式 | 结论 |
| --- | --- | --- | --- |
| Prompt | 既有训练/契约语义 | 作为一次输入或模板，与 Skill 分离 | PASS |
| Tool | C11 | 有界动作与合同；C12 只声明依赖，不重定义 schema/MCP | PASS |
| Workflow | C11 | 耐久状态、分支、等待与补偿；不藏进自然语言 Skill | PASS |
| Skill | C12 | 程序性知识包、发现、版本、测试、撤回 | PASS |
| Plugin | C12 | 可执行 Runtime 扩展与完整生命周期 | PASS |
| Hook | C13 | C12 只做组件分型和供应链登记 | PASS |
| Provider | C06 | C12 只治理 Plugin/依赖来源，不重画运行与 failover | PASS |
| Channel Adapter | C06/C09/C13 相关边界 | C12 只登记扩展组件、账户/传输依赖与撤回 | PASS |

Skill、manifest、description、`allowed-tools`、Hermes capability consent、Plugin 名称和用户聊天文字都没有被写成权限来源。真实权限持续依赖 identity、delegation、Policy、Approval、Sandbox、Secret broker、OS 和目标系统；C12 没有用人格、程序性 Memory 或供应链签名替代强制访问控制。

## 4. D20—D23 一致性

| 决策 | 核查 | 结论 |
| --- | --- | --- |
| D20 | C12 向 C15 输出 capability diff，并沿用能力/人格/文档/工具/目标五类；明确不新增“Skill 漂移” | PASS |
| D21 | route/load/execute/delivery/environment read-back 分离；协议或文件成功不单独推出任务成功 | PASS |
| D22 | 12.7.2 写“回归集、训练集、留出集、对抗集，真实任务另行观察” | REVIEW_REQUIRED |
| D23 | 只给 C22 事件输入，不扩写 C22 的七节或冻结其未完成定义 | PASS |

### D22 阻断说明

规范数据层只能是 `training / regression / holdout / representative real-world`。security/red-team 是横跨四层的非补偿切片，不是“对抗集”第五层，也不能用它代替 representative real-world。

C12 应表达为：训练、回归、留出与代表性真实任务分别承担其数据生命周期职责；每层都可带 adversarial/security 标签或套件；任何安全硬失败直接 FAIL。当前正文虽然正确保持安全失败非补偿，却在数据层命名上产生平行体系，故必须修复后才能关闭交叉门。

## 5. 上下游接口

| 接口 | C12 当前连接 | 结论 |
| --- | --- | --- |
| C07 → C12 | 沿用 task/trial/trajectory/artifact/environment outcome、三态、硬门 | REVIEW_REQUIRED：D22 数据层表达冲突 |
| C02 → C12 | 训练/生产双闭环由 C02 定义；C12 只消费并落到能力候选链 | PASS |
| C08 → C12 | 只消费训练干预、轮次、双三角、停训与候选证据链，不把双闭环归给 C08 | PASS |
| C09 → C12 | 工作流恢复、artifact、delivery 与 environment read-back 语义对齐；frontmatter 未列 C09，专门交接较弱 | PASS；保留 P1 元数据项 |
| C10 → C12 | 程序性 Memory 只能提 proposal，不自产 authority 或 release | PASS |
| C11 → C12 | Tool/MCP、幂等、Policy/Approval/Sandbox、终态定义不被重写 | PASS |
| C12 → C15 | proposal、capability diff、证据、权限/终态变化、回滚记录；不新增第六漂移 | PASS |
| C12 → C18 | 组件边界、owner 与 handoff 合同 | PASS，待 C18 正文冻结后回归 |
| C12 → C19 | 来源、依赖、可执行资源、数据流、Tool/secret/network 与残余 | PASS，完整威胁模型仍归 C19 |
| C12 → C21 | release、部署、观察、kill switch、撤回/替代/退役证据 | PASS，组织发布总门仍归 C21 |
| C12 → C22 | discovery/load/invoke/deny/quarantine/release/rollback/revoke/residual 事件 | PASS，C22 七节与组织依赖不被重定义 |

C09 是实际语义依赖，但只在正文“Workflow/C09”出现一次，未进入 `depends_on`。这不构成概念错误，却会让 Agent 读取 frontmatter 时漏掉 task/context/delivery 三层完成性来源；建议作为 P1 元数据修复。

## 6. 跨平台一致性

| 维度 | OpenClaw | Hermes | Muse | 结论 |
| --- | --- | --- | --- | --- |
| 基线 | `v2026.9.6 / eb377ac…` | `v0.20.1 / v2026.8.13`，`main` 单列动态 | 官方公开材料 | PASS |
| Skill | 多来源、优先级、managed revision、Session snapshot | progressive disclosure、CRUD/Hub、write approval | skills/Connectors 仅厂商措辞 | PASS |
| Plugin | 固定扩展面、policy、allow/deny、生命周期、quarantine | 固定生命周期、pin、consent 非 sandbox；动态 portable/native 分栏 | 不推断 Plugin 格式 | PASS |
| 权限 | Skill 可见性/allowlist 不等于 host 或业务授权 | consent/audit 不等于恶意代码隔离 | Sentinel/privsep 等只作 VENDOR-CLAIM | PASS |
| 供应链效果 | 目标部署未实测 | 固定与动态未做目标实例对照 | 内部格式和撤回未知 | REVIEW_REQUIRED |

OpenClaw 固定 commit 的 workspace `TOOLS.md` 与 `HEARTBEAT.md` 退役事实已独立核验。C12 对二者没有运行时引用，也没有把旧文件恢复为七契约或 Skill/自动化载体，结论为 PASS。

## 7. 仿生、案例与练习

### 仿生四段

“对应关系”覆盖人类程序性记忆与工程对象；“启发”覆盖训练和治理启示；“失效边界”明确不证明身体、体验、意向或道德主体；“工程落点”把类比转回 proposal、隔离、Registry 和撤回。标题虽未逐字采用“人类现象/工程映射/训练启示/比喻边界”，语义四段齐全，结论 PASS。

### 案例

- CASE-A“远山”：研究程序与来源边界；
- CASE-B“潮生”：草稿 Skill 不得静默扩成外发；
- CASE-C“守夜”：恢复 Skill、Provider/Plugin 与故障状态分型。

三个案例都保持教学/合成身份，消费上游风险、工具、终态和授权边界，不声称真实客户效果，结论 PASS。

### 练习

X-C12-01 覆盖 Skill 审计、撤回、旧 Session 和替代；X-C12-02 覆盖 Plugin 禁用态、供应链红队、隔离和残余。目标、边界、停止、回滚与三态设计完整，设计审查结论为 `PASS`。作者合成运行不属于本轮实践复现，真实 Runtime/Plugin/撤回传播仍为 `REVIEW_REQUIRED`。

## 8. P0 / P1 / P2

### P0

1. **D22 数据层冲突。** 12.7.2 把“对抗集”写成独立数据层，并把真实任务放到其外；必须改成四数据层上的 cross-cutting security/red-team slice。此项阻断交叉门，且安全硬失败继续不可补偿。

### P1

1. `CISA-SBOM` 实为 public comment draft，source title 和正文首次引用需明确 draft 身份。
2. evidence ledger 有 5 个未被 claim 消费的 source，需绑定或移除。
3. C09 是实际 completion/Workflow 依赖，但未进入 chapter frontmatter `depends_on`，章末也没有独立的 C09 输入/输出交接。
4. D20—D23 未成为 ledger 的显式决策证据；应至少把 D20/D21/D22/D23 绑定到相应方法 claim，避免全书裁决只靠间接引用。

### P2

1. 章名在 v2、章节卡与 frontmatter 中有“插件体系/版本”措辞差异，合订目录时统一。
2. 仿生段前后存在连续两个水平分隔符，不影响内容但应在编辑门清理。

## 9. 交叉门结构化结论

```yaml
cross_gate:
  chapter_id: C12
  outline_12_1_to_12_8: PASS
  book_178_sections_unchanged: PASS
  exact_three_artifacts: PASS
  definition_ownership: PASS
  authorization_boundary: PASS
  d18: PASS
  d20: PASS
  d21: PASS
  d22: REVIEW_REQUIRED
  d23: PASS
  openclaw_fixed_boundary: PASS
  hermes_fixed_dynamic_split: PASS
  muse_vendor_claim_boundary: PASS
  bionic_four_part: PASS
  cases: PASS
  exercises_as_design: PASS
  overall: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  practice_gate: NOT_REVIEWED
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

## 10. 验证记录

- `fact-check.md`、`cross-review.md` frontmatter 与 `fact-source-audit-20260930.yaml`：解析 PASS。
- source 汇总、28 条 claim verdict、D22 阻断字段与固定版本哈希断言：PASS。
- `python3 scripts/validate-formal-manuscript.py`：PASS；8 卷、24 章、178 个正文三级节点、C12 为 18,624 CJK。仅有 C13 正在准备及未来 11 章包未完成两项预期 warning，与 C12 无关。
- `python3 scripts/validate-book.py`：PASS；扫描 281 个 Markdown，检查 1,304 条本地链接。
- `git diff --check -- .`：PASS；三个新增文件的限定 `--check` 无 whitespace error（`--no-index` 对新增文件返回差异状态 1，输出为空）。

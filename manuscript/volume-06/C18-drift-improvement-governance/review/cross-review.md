---
review_id: C15-independent-cross-review-20260930
chapter_id: C15
review_type: independent-cross-chapter-cross-platform-review
reviewed_on: "2026-09-30"
reviewer_role: cross-reviewer
chapter_status: drafting
cross_gate: review_required
fact_gate_ref: "review/fact-check.md"
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C15 跨章与跨平台一致性审校

## 1. 裁决

C15 的主方法已经闭合：D20 仅保留能力、人格、文档、工具、目标五类一级漂移，记忆/上下文只作跨类型状态与证据源；失败只能生成候选，观察—假设—实验—评估—固化中的固化必须由外部责任人批准；`AU-L0—AU-L4` 与 `MAT-L0—MAT-L5` 没有互推；目标、权限、自主半径或风险变化明确返回 C14 再认证；C21 继续拥有发布/恢复，C24 继续拥有成熟度认证。正文只含 15.1—15.7，三件母产物、两项练习、CASE-A/B/C、仿生四段和“自我改进首先是一条受控发布链”的工程真相均存在。

交叉门判 **`REVIEW_REQUIRED`**，有两个 P1 阻断项：

1. `P1-X15-01`：运行 README 声明环境纯合成、无真实数据与外部写，但 input 的三个 test 直接使用 `layer: representative real-world`，经五类漂移展开为 15 条真实任务层记录；runner 和 summary 没有 synthetic-shadow/provenance 分离，也没有阻止纯合成环境伪占真实任务层。
2. `P1-X15-02`：章节卡的正式 `depends_on` 为 `[C05, C07, C08, C10, C14]`，chapter frontmatter 却静默加入 `C12, C13`。正文确实消费 C12 的 Skill/Plugin 供应链和 C13 的 signal/pause/circuit 语义，但这应通过显式 `supplementary_interfaces` 表达，或先由总编修改章节卡；不能只在单章 frontmatter 改写全书拓扑。

两项都可做窄修补，不推翻章节主体，也不改变事实门 `PASS`。修复并经非作者回归后，交叉门可更新为 `PASS WITH LIMITATIONS`；真实平台、自学习、shadow/canary、完整回滚和外部固化仍须保持 `REVIEW_REQUIRED`。

本审校不修改正文、ledger、产物、练习或 runs，不签实践、编辑、总编或 `release_candidate`。

## 2. D20 五类漂移与记忆/上下文边界

| 一级类型 | 本章观察对象 | 定义权检查 | 裁决 |
| --- | --- | --- | --- |
| 能力漂移 | 质量、失败、成本、时延、稳定性、方差相对基线的持续偏移 | 不重写 C03/C07 的能力与评测标准 | PASS |
| 人格漂移 | 已批准身份、价值、关系与拒绝边界的结构性变化 | 不把风格适配或单次措辞当漂移 | PASS |
| 文档漂移 | 权威文档冲突、过期、加载快照与批准语义不一致 | 不让文档文本自产权限 | PASS |
| 工具漂移 | Tool/Skill/Plugin/API/Provider 的 schema、权限、宿主、依赖、输出与失败语义变化 | 合同与供应链细节仍归 C11/C12 | PASS |
| 目标漂移 | 优化对象、优先级、成功/禁止标准、风险偏好、服务对象与责任边界偏移 | 合法目标变更需 owner 批准并回 C14 | PASS |

正文、`A-C15-01`、X-C15-01 和作者 input 的 `drift_types` 都只使用 `capability/persona/document/tool/goal` 五类。记忆错误按传播结果落入五类：文档冲突、人格关系变化、能力污染、目标偷换或工具 schema/权限变化。C10 继续拥有 provenance、更新、更正、过期、遗忘和删除生命周期。

结论：D20 为 `PASS`，未发现第六类“记忆漂移”。

## 3. 候选、固化与不可自授权

正文和三件母产物保持以下顺序：

```text
变化信号 → 漂移候选 → 可反证假设 → 单一主干预 → 隔离实验
→ 独立评估 → 外部 owner 决定固化/限域/观察/驳回/回滚
```

- 反复失败只形成候选，不自动写活动规则；
- proposer、evaluator、approver、accountable owner 分离；
- 候选不能同时修改 grader、holdout、权限、安全规则或目标并宣称因果；
- Agent 不得自改 policy、grader、`AU-Lx`、五维自主半径、上位目标或生产资产；
- “固化”是外部治理决定，不是 Agent 保存文件后的自报成功；
- memory 写入走 C10，Skill/Plugin 发布走 C12，授权变化走 C14，生产发布走 C21。

结论：候选与实际固化分离为 `PASS`，不存在自授权/自固化通道的规范性放行。

## 4. AU/MAT、C14、C21 与 C24 定义权

| 对象 | 主定义章 | C15 当前行为 | 裁决 |
| --- | --- | --- | --- |
| `AU-L0—AU-L4` | C14 | 只记录当前自主上限和变更影响；不发布等级 | PASS |
| 目标/权限/五维半径变化 | C14 | 生成再认证触发，降级/暂停后交授权 owner | PASS |
| `MAT-L0—MAT-L5` | C24 | 只输出漂移与治理证据；不设成熟度阈值 | PASS |
| shadow/canary/生产发布 | C21 | 输出 exact bundle、证据、停止与回滚前置；不批准发布 | PASS |
| 生产恢复/退役 | C21 | 不把 bundle 恢复自报成生产恢复完成 | PASS |

正文明确禁止裸 `Lx` 机器字段、`MAT-Lx → 权限` 和 `AU-L4 → 改目标/自扩权`。回滚不得恢复已撤销授权、删除同意、旧目标或过期凭证；若授权对象、范围、参数、时窗或版本改变，返回 C14，而非由 C15 内部“修复”。

结论：`PASS`。

## 5. D22 四层与横切安全

### 5.1 规范层

正文、A-C15-02 和 X-C15-02 都把 training、regression、holdout、representative real-world 作为四个数据生命周期层，并把 security/red-team 定义为横切、非补偿切片。未授权副作用、敏感泄露、影子写入、holdout 污染、撤销复活等硬失败不会被总体质量抵消。

规范表达为 `PASS`。

### 5.2 保存运行的数据谱系

作者 input 声明无真实凭证与外部效果，README 进一步说明环境“纯合成、无网络、无真实凭证、无外部写”。但是三个测试直接标为：

```yaml
layer: "representative real-world"
```

三个测试分别是 `self-security`、`self-goal` 与 `unknown-effect`，它们对五类漂移做笛卡尔展开后形成 15 条真实任务层结果：`10 FAIL / 5 REVIEW_REQUIRED`。runner 只按字符串聚合，没有环境字段、真实任务来源计数、`synthetic_shadow` 或防伪约束。summary 因而把纯合成样本呈现为 D22 真实任务层覆盖。

这与 D22 的来源语义冲突。security/adversarial 可以横切合成层，但不能因为样本“像真实风险”就取得 representative real-world 身份。

**关闭条件：**

1. 为 input 增加明确的 `environment: offline-synthetic`；
2. 将三个测试归入 training/regression/holdout 中适当层，若需保留迁移意图，另加 `synthetic_shadow: true` 与 `intended_target_layer: representative_real_world`；
3. runner 从实际 layer 派生 `representative_real_world_executed` 和 count，保留空真实层 bucket；offline-synthetic 出现真实层记录时硬失败；executed 声明与实际 count 不一致时硬失败；
4. 同步 README、summary、正文、本地 claim 限制和作者自检，明确真实任务 count 为 0；
5. 双 fresh 复跑并加入至少两项负向突变：合成记录冒充真实层、count=0 却自报 executed=true。

另一条合法路径是使用经数据 owner 授权、去标识、低风险、可回滚并带来源记录的真实代表性任务；在本章当前纯合成范围内不建议为了“补层”扩大实践风险。

结论：`P1-X15-01 / REVIEW_REQUIRED`。

## 6. 正式依赖与补充接口拓扑

章节卡冻结的 C15 正式拓扑为：

```yaml
depends_on: [C05, C07, C08, C10, C14]
feeds_into: [C21, C22, C24]
```

当前 chapter frontmatter 则为：

```yaml
depends_on: [C05, C07, C08, C10, C12, C13, C14]
feeds_into: [C21, C22, C24]
```

C12 的不可变 Skill/Plugin revision、digest、审批、撤回/替代与 C13 的 signal/state/pause/circuit/UNKNOWN 确实对 C15 有用，但本章没有权单方面把补充接口升级为全书正式硬依赖。尤其全书主链已明确 `C13 → C14 → C15`，将 C13 再列为 C15 直接硬依赖会改变拓扑表达；C12 也未在章节卡 `depends_on` 中。

**关闭条件二选一：**

1. 推荐：恢复章节卡的正式 `depends_on`，新增并解释 `supplementary_interfaces: [C12, C13]`；正文保留实际消费内容和定义权限制；或
2. 若总编确需把 C12/C13 升为正式依赖，先修改权威 CHAPTER-CARDS、依赖图及受影响的下游计划，再同步本章，而不是仅改本章 frontmatter。

`C12` ledger source 可继续支撑 E-C15-012，不因其属于补充接口而删除。`C13` 若保留为 source，应绑定到明确的 signal/pause/UNKNOWN 接口 claim；否则从 source 集合移除，避免未使用登记。

结论：`P1-X15-02 / REVIEW_REQUIRED`。

## 7. 15.1—15.7、母产物、练习、案例与仿生

| 检查对象 | 结果 | 说明 |
| --- | --- | --- |
| 正文三级结构 | PASS | 恰好 15.1—15.7，无 15.8+。 |
| 母产物 | PASS | artifacts 恰好 A-C15-01/02/03。 |
| 练习 | PASS（实践未审） | X-C15-01 五类诊断；X-C15-02 shadow/rollback 治理。 |
| CASE-A | PASS | 研究型 Agent 的引用、知识和工具漂移。 |
| CASE-B | PASS | 外联 Agent 的主动性、人格与目标漂移。 |
| CASE-C | PASS | 多 Agent 组织规则、委托与人格漂移。 |
| 仿生四段 | PASS | 人类现象、工程映射、训练启示、比喻边界完整。 |
| 工程真相 | PASS | “自我改进首先是一条受控发布链”，不写自然进化神话。 |
| 人类三处监督 | PASS | 定目标、批变更、担责任均不可外包。 |

正文在 15.7 后的“本章结论/证据与变更记录”不是新增编号三级节，不改变 15.1—15.7 的正式目录。

## 8. 跨平台一致性

| 维度 | OpenClaw | Hermes | Muse | 裁决 |
| --- | --- | --- | --- | --- |
| 证据身份 | v2026.9.6/eb377ac 固定文档 | 2026-09-30 动态官方页 | VENDOR-CLAIM | PASS |
| 候选/写入 | Workshop proposal 与 direct maintenance 明确分开 | skills/memory write approval 动态映射 | 只引用学习/记忆产品陈述 | PASS |
| 自动改进 | auto 为产品默认但不等于本书治理通过 | 写入获批不等于长期改善 | getting sharper 不等于可核验自改算法 | PASS |
| shadow/canary/rollback | 不声称产品自动满足完整 bundle 回滚 | 不伪造同构流程 | 不推断内部发布链 | PASS |
| 权限 | 任何目标/权限变化仍回 C14 | write approval 不产生上位目标权 | 用户控制陈述不替代系统验证 | PASS |

真实 OpenClaw Workshop/self-learning、Hermes 固定环境和 Muse 内部机制均未运行；平台映射只证明可迁移语义，不能形成生产效果主张。

## 9. 15 项 P0 交叉结论

| P0 | 结论 | 交叉依据 |
| --- | --- | --- |
| P0-01 | PASS | 章首、15.1—15.7、结论、练习与交接完整。 |
| P0-02 | REVIEW_REQUIRED | 方法定义权正确，但 frontmatter 静默改变正式依赖拓扑。 |
| P0-03 | PASS | 23 条 evidence 双向闭合，事实门独立通过。 |
| P0-04 | PASS WITH LIMITATIONS | OpenClaw fixed、Hermes dynamic、Muse vendor 分层正确；实机未测。 |
| P0-05 | PASS（设计） | 候选、停止、隔离、shadow、灰度、回滚和恢复前置完整。 |
| P0-06 | PASS | 不允许自改安全、grader、权限、目标或生产资产。 |
| P0-07 | REVIEW_REQUIRED | 作者运行可重复，但真实任务层谱系不合格且独立实践未执行。 |
| P0-08 | PASS | 仿生四段有非意识、非进化边界。 |
| P0-09 | PASS | 三平台没有伪造同构或越级证据。 |
| P0-10 | PASS | CASE-A/B/C 为合成教学案例。 |
| P0-11 | PASS | 机器块与三态可解析；文本和 memory 不自产 authority。 |
| P0-12 | PASS | 真实平台、生产 canary、组织审批、治理成本与 Muse 内部机制公开为缺口。 |
| P0-13 | PASS | 安全、污染、越权、shadow 写入、撤销复活均非补偿。 |
| P0-14 | PASS | 三件母产物可定位，C14/C21/C24 交接不抢定义权。 |
| P0-15 | PASS | 无最强/必然改善主张，因果层级清楚。 |

## 10. 问题分级与关闭条件

### P0

无。

### P1

1. **P1-X15-01 / 纯合成样本占用 canonical representative real-world 层。** 关闭条件见 5.2；必须同时修机器谱系、防伪 runner、文本和账本，并由非作者做突变回归。
2. **P1-X15-02 / C12、C13 被静默升级为正式硬依赖。** 关闭条件见第 6 节；推荐恢复章节卡 `depends_on` 并新增 `supplementary_interfaces: [C12, C13]`。

### P2

1. **P2-X15-01 / 下游正式包冻结后的字段回归。** C21/C24 当前主要以 preflight 被消费；正式章冻结后需回归发布门、恢复 receipt、重大变化与撤证字段，但不得让下游反向改写 C15 五类漂移和候选定义权。
2. **P2-X15-02 / source hygiene。** `C13` 与 `C22` 未被 claim 使用，见事实门 `P2-F15-01`。
3. **P2-X15-03 / 机器层命名统一。** 后续修补应统一使用受控机器值 `representative_real_world`，自然语言仍可写 representative real-world，避免空格形式在跨章脚本中产生额外映射。

## 11. 交叉门结构化裁决

```yaml
cross_gate:
  chapter_id: C15
  primary_three_state_verdict: REVIEW_REQUIRED
  blockers: [P1-X15-01, P1-X15-02]
  d20_five_drift_types: PASS
  memory_context_as_cross_type_source: PASS
  candidate_not_self_solidified: PASS
  au_mat_separation: PASS
  c14_recertification_interface: PASS
  c21_release_recovery_ownership: PASS
  c24_certification_ownership: PASS
  outline_15_1_to_15_7: PASS
  exactly_three_artifacts: PASS
  exactly_two_exercises: PASS
  cases_a_b_c: PASS
  bionic_four_part: PASS
  engineering_truth: PASS
  d22_normative_model: PASS
  d22_saved_run_lineage: REVIEW_REQUIRED
  dependency_topology: REVIEW_REQUIRED
  platform_identity: PASS_WITH_LIMITATIONS
  p0_open: 0
  p1_open: 2
  p2_open: 3
  practice_approved: false
  editor_approved: false
  chief_editor_approved: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

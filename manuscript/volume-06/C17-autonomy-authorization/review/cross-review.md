---
review_id: C14-independent-cross-review-20260930
chapter_id: C14
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

# C14 跨章与跨平台一致性审校

## 1. 裁决

C14 的定义权和主体结构已经闭合：`AU-L0—AU-L4` 与 `MAT-L0—MAT-L5` 严格分离，C13 的 trigger 不产生 authority，授权、系统 Policy、执行 Approval、Binding/Pairing 和 D21 completion 都没有混写；委托衰减、撤销传播、过期、再认证、break-glass、C19/C21 下游边界完整。正文只含 14.1—14.7，artifacts 目录恰好三件母产物，CASE-A/B/C 与仿生四段均存在。OpenClaw 固定版、Hermes 固定发行/动态文档和 Muse `VENDOR-CLAIM` 也没有伪造同构。

交叉门仍判 **`REVIEW_REQUIRED`**，唯一阻断项是 `P1-X14-01`：作者运行明确声明全部 28 条记录都是 `offline-synthetic`、合成主体和 mock 动作，却把 6 条记录的机器字段直接写为 `layer: representative real-world`，摘要又把它们计入 D22 真实任务层。D22 四层描述数据生命周期/来源；横切安全可合成，但“representative real-world”不能只靠一个标签获得真实任务来源身份。C07 曾使用“真实任务层 schema 的合成 shadow 表示”，但它把 synthetic shadow 和生产证据明确分开；C08 当前裁决更明确允许 real-world fixture 为 0、禁止伪造。C14 的普通 `layer` 字段没有这种机器可辨的 shadow/provenance 分离，因此下游会误读为真实任务覆盖。

这不推翻作者 28-trial 的计数和安全门结果，也不是事实造假：README 和正文已诚实披露合成环境。它是数据谱系/跨章规范缺陷。关闭后，本章交叉结构可转为 `PASS WITH LIMITATIONS`；真实授权、撤销传播、stop receipt、break-glass 组织政策仍须由独立实践与下游责任人验证。

本审校不修改作者正文、ledger、产物、练习或 runs，不签实践、编辑、总编或 `release_candidate`。

## 2. 定义权与关键不等式

| 对象 | 主定义章/控制面 | C14 当前表达 | 裁决 |
| --- | --- | --- | --- |
| 能力与七维强者 | C03/C07 | 只消费能力证据，不从能力分数推导授权 | PASS |
| 任务级自主 | C14 | 唯一使用 `AU-L0—AU-L4`；等级绑定 role/task/action/environment/version | PASS |
| 综合成熟度 | C24 | 只引用 `MAT-L0—MAT-L5`，明确不与 AU 互推 | PASS |
| 触发与主动状态机 | C13 | 保留 `trigger ≠ authority`，不重写 C13 状态机 | PASS |
| 技术/交付/环境完成 | D21/C09 | authority 不证明 completion；UNKNOWN 要先对账 | PASS |
| 身份与纵深安全 | C19 | C14 给出授权需求，不设计完整 IAM、凭证、网络或多租户防御 | PASS |
| 发布、恢复与退役 | C21 | C14 给再认证/撤销前置，不宣称生产可发布或恢复完成 | PASS |

正文核心关系准确而且在母产物、练习中保持一致：

```text
能力 ≠ 自主 ≠ 系统权限 ≠ 组织责任
trigger(C13) ≠ authority(C14) ≠ completion(D21)
AU-L0—AU-L4 ≠ MAT-L0—MAT-L5
```
没有发现裸 `L3/L4` 被用于机器字段，没有从 `MAT-Lx` 推导外发/支付/删除权限，也没有从 `AU-L4` 推导能力领先或最终责任。

## 3. 授权、审批、Policy、Binding 的分离

| 概念 | 本章合法职责 | 明确不负责 | 裁决 |
| --- | --- | --- | --- |
| Authentication / Pairing | 证明人、设备或进程是谁/是否可信接入 | 不证明可对某业务对象执行特定动作 | PASS |
| Binding | 把输入路由到某个 Agent | 不授予访问或动作权限 | PASS |
| Authority evidence | 由有权主体绑定对象、动作、范围、参数、时窗、批准者等业务决定 | 不替代系统强制执行或完成证据 | PASS |
| Policy | 在系统层强制 deny/allow 上限，deny 优先 | 不从自然语言聊天自动生成业务责任 | PASS |
| Approval | 对冻结对象/参数作一次或窄批决定，并继续受上游 Policy 约束 | 不能放宽 deny，也不是敌对多租户 IAM | PASS |
| Sandbox / Tool Contract | 限制执行位置、参数、效果和恢复路径 | 不创造业务授权 | PASS |
| Session / Memory / Contract text | 保存上下文、意图或语义纪律 | 不自产 authority | PASS |

OpenClaw 固定文档中的 policy、approval、elevated、pairing、binding 与 trust model 被按其实际职责组合，没有被写成“一个开关解决所有授权”。Hermes dangerous-command prompt 只作动态实现镜；Muse Sentinel/scoped capability/JIT/takeover 全部保持厂商主张。

结论：`PASS`。

## 4. 14.1—14.7 与三件母产物

| 规范对象 | 当前实现 | 裁决 |
| --- | --- | --- |
| 14.1 自主阶梯 | AU 五级、七种行为、四轴、MAT 分离 | PASS |
| 14.2 默认发现/提案 | 默认不对外行动；拒绝、降级与交回可验收 | PASS |
| 14.3 四因子审批门 | 影响、可逆性、敏感性、不确定性联合硬门；五维半径 | PASS |
| 14.4 身份/委托/scope/有效期/撤销 | 六项最低绑定、衰减委托、级联撤销、负向访问测试 | PASS |
| 14.5 模拟/预演/执行 | pre-commit、对象哈希、幂等、终态与 UNKNOWN 对账 | PASS |
| 14.6 例外/二次确认/取消/审计 | JIT、独立双批、break-glass、cancel≠stop≠rollback | PASS |
| 14.7 扩大/降级/暂停/撤销/再认证 | 重大变化触发再认证，Agent 不自续期/扩权 | PASS |
| 正式母产物 | artifacts 目录恰好 A-C14-01/02/03 | PASS |
| 正式练习 | X-C14-01 与 X-C14-02 可定位 | PASS（实践未审） |

章节没有新增 14.8，也没有把运行 README、记录模板或练习冒充第四件正式产物。

## 5. 委托、撤销、过期与再认证

### 5.1 委托 scope attenuation

正文和 `A-C14-03` 都使用相同原则：

```text
child_authority = parent_authority ∩ delegator_own_rights ∩ minimum_child_need
```

默认禁止转委托；允许时需限定 `max_depth`。子授权不得晚于父授权过期，不得扩大主体、数据、动作、环境、预算、对象和外发目标，也不得借父 token 冒充父身份。CASE-C 和 X-C14-02 都包含转委托扩权失败。

结论：`PASS`。

### 5.2 撤销传播与过期

撤销不是 UI 标志，而是“权威记录失效 → 阻止新动作 → 冻结 queue/session/cache/grant/temp credential → 处理在途动作 → 撤销子授权 → 负向访问测试 → 回读终态”的分布式流程。过期授权和缓存旧批准都被确定性拒绝；负向访问仍成功为 `FAIL`，传播不可核为 `REVIEW_REQUIRED`。

结论：设计 `PASS`；真实传播仍为实践限制。

### 5.3 重大变化再认证

主体、对象、参数、工具、模型、策略、环境或风险发生重大变化会触发暂停与再认证；Agent 只能提出候选，不能自批、自续期或删除失败后重申。C15 管理漂移候选，C14 管授权重认证，C21 管生产阶段门，定义权没有重叠。

结论：`PASS`。

## 6. break-glass 与人类监督

break-glass 被限定为预定义紧急止损，而不是便捷提权：需要合法紧急类型、极窄动作、明确 owner、短时自动过期、强审计和事后独立复核。最小权限、JIT、双人复核与 break-glass 四者不互相替代；双人复核要求两个独立且有资格的身份，同人别名或共享凭证失败。

正文没有自行宣布某个紧急情形在法律或组织政策上有效，也没有允许人格文本、聊天或 Agent 自己触发 break-glass。C19 继续拥有身份/凭证/纵深防御实现，C21 继续拥有发布/恢复门。

结论：`PASS WITH PRACTICE AND POLICY LIMITATIONS`。

## 7. D22 四层与横切安全

### 7.1 规范正文

正文对 D22 的规范描述本身正确：`training / regression / holdout / representative real-world` 是四个数据生命周期层，security/red-team 是横跨四层的非补偿切片，不是第五层，也不能替代真实任务层。关键安全失败不能被其他得分抵消。

### 7.2 作者运行的谱系冲突

作者输入的全局环境是 `offline-synthetic`，README 明确“合成主体、mock 动作、无真实凭证、无网络、无外发、无生产写”。但 6 条记录的机器字段直接为：

```yaml
layer: "representative real-world"
```

保存摘要随即报告该层有 `2 PASS / 3 FAIL / 1 REVIEW_REQUIRED`。这个字段无法区分“来自已授权真实任务的数据”与“只模拟未来真实任务 schema 的 synthetic shadow”。人类读到 README 能知道限制，但机器消费 summary 时可能把它计为真实任务覆盖。

**关闭条件二选一：**

1. 若仍全部使用合成夹具，将 6 条记录的规范 `data_layer` 重新归入 training/regression/holdout，真实任务层计数为 0；可以另加 `intended_target_layer: representative_real_world` 或 `scenario_realism: synthetic_shadow`，但不能冒充数据来源；或
2. 若要保留 canonical real-world 层，使用经数据 owner 授权、去标识、低风险、可回滚且有来源记录的真实代表性任务，并保留 shadow/权限/污染证据。

完成任一路径后需要同步 input、runner 输出、summary、README、正文 28-trial 描述、author-self-check 与相关 ledger 限制，再由非作者回归。不能只改 README，因为机器字段仍会误导。

结论：`REVIEW_REQUIRED`，问题编号 `P1-X14-01`。

## 8. CASE、仿生与双视图

- CASE-A 处理研究发布、来源与稿件哈希审批；CASE-B 处理客户外发、聊天意图、撤回和 UNKNOWN；CASE-C 处理多 Agent 委托、部署边界和撤销传播；均为合成教学案例。
- 仿生四段完整包含人类现象、工程映射、训练启示和比喻边界；明确 Agent 没有天然职业伦理、知情同意、主观意识或法律人格。
- 人类视图聚焦批准者资格、对象一致、scope/时窗、撤销与接管；Agent 视图要求结构化 gate/authorization/receipt/handoff，不从语气猜权。
- 三案、仿生和双视图都没有授予额外权限，也没有用“责任感”修辞代替系统控制。

结论：`PASS`。

## 9. 跨平台一致性

| 维度 | OpenClaw | Hermes | Muse | 裁决 |
| --- | --- | --- | --- | --- |
| 证据身份 | v2026.9.6/eb377ac 固定提交 | 0.20.1 固定发行锚点 + 2026-09-30 动态安全页 | VENDOR-CLAIM | PASS |
| Policy/Approval | 固定文档支持分层收敛与 exec approval 边界 | dangerous-command prompt/allowlist 动态对照 | Sentinel/scoped capability 厂商陈述 | PASS |
| Identity/Binding | pairing 是设备身份、binding 是路由 | 不伪造 OpenClaw 同名组件 | 不推断内部身份图 | PASS |
| 委托/撤销 | 本书方法叠加平台强制层 | 不从动态安全页倒推出完整 delegation graph | 不声称撤销已覆盖全部下游缓存 | PASS |
| 生产有效性 | 未声称真实安装已验证 | 固定/动态逐项源码对照仍待做 | 内部实现与效果未知 | PASS WITH LIMITATIONS |

## 10. 15 项 P0 交叉结论

| P0 | 结论 | 交叉依据 |
| --- | --- | --- |
| P0-01 | PASS | 章首、14.1—14.7、案例、练习、交接完整。 |
| P0-02 | PASS | C14 只拥有自主/授权/审批/生命周期，未抢 C13/C19/C21/C24。 |
| P0-03 | PASS | 28 claim 双向闭合，事实门已独立通过且限制公开。 |
| P0-04 | PASS WITH LIMITATIONS | 固定/动态/vendor 分层准确；目标部署未实测。 |
| P0-05 | PASS（设计） | 拒绝、降级、暂停、cancel、stop、补偿、撤销、恢复齐全；真实执行未审。 |
| P0-06 | PASS | 自然语言不授权；Policy/Approval/Binding/identity 分离。 |
| P0-07 | NOT REVIEWED | 作者运行可重复，但独立实践门不属于本轮；不得据此关闭。 |
| P0-08 | PASS | 仿生四段完整且明确意识、伦理、人格边界。 |
| P0-09 | PASS | 三平台证据身份没有伪造对齐。 |
| P0-10 | PASS | CASE-A/B/C 为去标识合成教学案。 |
| P0-11 | PASS | YAML/机器块可解析；人格、记忆、Binding 都不自产 authority。 |
| P0-12 | PASS | 真实平台、撤销传播、break-glass 政策与 Muse 内部机制均公开为限制。 |
| P0-13 | PASS | 硬风险、安全/授权失败不可补偿。 |
| P0-14 | PASS | 三母产物可定位，下游接口清楚。 |
| P0-15 | PASS | 无最强/领先或生产效果声明；完整保留失败分布。 |

`P1-X14-01` 不是安全门被平均掉，而是 D22 来源标签不实；因此不升级为 P0，但在修复前阻断交叉门。

## 11. 问题分级与关闭条件

### P0

无。

### P1

1. **P1-X14-01 / 合成样本直接占用 canonical `representative real-world` 层。** 影响 D22 数据谱系和下游训练/认证判断。关闭条件见 7.2；须同步机器字段、摘要和文本并由非作者回归，不能只补一句限制。

### P2

1. **P2-X14-01 / 下游正式章冻结后回归。** 当前 C19/C21 仍主要以 preflight 形式被消费；其正式章冻结后应复核 authority event、identity graph、revocation receipt、break-glass owner 与 release/recovery receipt 字段，但下游不得反向改写 C14 的 AU 定义权。
2. **P2-X14-02 / ledger source 卫生。** 4 个未消费 source 见事实门 `P2-F14-01`；不阻断交叉语义，但应在下一轮 ledger 整理中闭合。

## 12. 交叉门结构化结论

```yaml
cross_gate:
  chapter_id: C14
  verdict: REVIEW_REQUIRED
  blocker: P1-X14-01
  au_mat_namespace_separation: PASS
  trigger_authority_completion_separation: PASS
  authorization_approval_policy_binding_separation: PASS
  delegation_scope_attenuation: PASS
  revocation_propagation_design: PASS_WITH_PRACTICE_LIMITATION
  expiry_and_recertification: PASS
  break_glass_design: PASS_WITH_POLICY_AND_PRACTICE_LIMITATIONS
  c19_c21_boundaries: PASS
  outline_14_1_to_14_7: PASS
  exactly_three_artifacts: PASS
  d22_normative_model: PASS
  d22_saved_run_lineage: REVIEW_REQUIRED
  platform_identity: PASS_WITH_LIMITATIONS
  cases_bionic_dual_view: PASS
  p0_open: 0
  p1_open: 1
  p2_open: 2
  practice_approved: false
  editor_approved: false
  chief_editor_approved: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

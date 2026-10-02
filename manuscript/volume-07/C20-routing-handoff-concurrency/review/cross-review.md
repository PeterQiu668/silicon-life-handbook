---
review_id: C17-cross-review-20260930
chapter_id: C17
review_type: independent_cross_chapter_and_cross_platform_review
reviewer_role: non_author_cross_reviewer
verified_on: "2026-09-30"
chapter_status: drafting
cross_gate: REVIEW_REQUIRED
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C17 跨章与跨平台一致性审校

## 裁决

**交叉门：`REVIEW_REQUIRED`。** C17 的正文结构、主定义权、D21 完成语义、路由/让位/Handoff/并发/取消/单写者方法、三母产物和两练习整体成立；没有把 C16 组织模式或 C18 A2A 对象/信任据为本章所有，也没有伪造 OpenClaw/Hermes/Muse 同构。

交叉门当前被两项 P1 阻断：作者运行没有 D22 四层数据谱系，无法证明 synthetic 没有占用 representative real-world；runner 又直接把预分类 `fault` 名称映射到裁决，完全不消费 common contract，未知 fault 会 fail-open 为 PASS，重复 ID 也不拒绝。固定 60-trial 分布可重复，但不能由此升级为练习或一般化控制有效性。

## 1. 正式拓扑、结构与交付物

| 检查项 | 当前事实 | 裁决 |
| --- | --- | --- |
| 正式依赖 | `[C06,C09,C11,C14,C16]`，与章节卡一致 | PASS |
| 下游 | `[C18,C19,C20,C23]`，与章节卡一致 | PASS |
| 正文节点 | 仅 `17.1—17.7`，且每节唯一 | PASS |
| 篇幅 | formal 口径约 18,057 CJK，位于 18,000—24,000 门槛 | PASS |
| 正式母产物 | 路由策略、Handoff 卡、并发合并协议，恰好三件 | PASS |
| 练习 | X-C17-01 与 X-C17-02，恰好两件 | PASS |
| 案例 | CASE-A/B/C 均被实际消费，CASE-C 贯穿并发与交接 | PASS |
| 仿生 | 映射、启发、失效边界、工程落点四段齐全 | PASS |
| 人/Agent 双视图 | 明确且可操作 | PASS |
| 状态 | `drafting / unapproved / self_approval=false` | PASS |

## 2. 定义权与章际接口

### C17 主定义权：PASS

C17 只主定义以下对象：

- 任务级候选硬门、软排序、重路由和停止；
- 明确让位、让位通知和不抢答边界；
- 版本化 Handoff、三层 ACK 与责任 owner 原子切换；
- 并发准入、单写者/CAS/租约、取消传播、Join、冲突与对账。

这些定义互相形成完整链路，没有把“发消息”“spawn accepted”或“UI 显示 done”冒充责任与完成。

### 对 C16 的边界：PASS WITH STALE STATUS

C16 拥有任务拓扑、角色、主理/专家/执行/评审责任和组织净收益；C17 只消费 `topology_ref/role_ref/decision_owner_ref` 来做运行路由与并发。这个定义边界正确。

但 C16 当前事实/交叉门已经 `PASS WITH LIMITATIONS`，实践门未审；C17 仍写“独立门待签”。它没有过度声明，风险方向保守，但项目状态已经滞后，必须按事实门 `P1-F17-03` 同步后再过交叉门。

### 对 C14 的边界：PASS WITH PRACTICE LIMITATION

路由不生成授权、Binding 不生成授权、委托不扩权、责任转移不复活旧批准，均与 C14 一致。C14 当前事实/交叉通过、实践总门 `REVIEW_REQUIRED`；C17 保留受限输入与回归条件是正确做法。

### 对 C18 的边界：PASS

C17 把 Task、Message、Event、Artifact、Agent Card、身份和信任正式定义留给 C18；本章的 Handoff 卡与 Responsibility ACK 明确是组织方法，不冒充 A2A 标准 schema。A2A 只提供 task/message/artifact/event/cancel/push receipt 的兼容锚点。

## 3. D21 完成语义

C17 没有把“completion”缩成单一平台状态。正文和三件产物持续区分：

1. **技术/过程执行**：run、attempt、tool/adapter 是否实际发生；
2. **交付/产物可见**：对象是否存在、版本/digest 是否正确、目标端是否读到；
3. **业务与环境验收**：退款、发布、外发或权威系统终态是否符合预期。

`spawn accepted`、Transport ACK、HTTP 2xx、模型说 done、文件存在、cancel requested 均不能独立推出完成；UNKNOWN 要先 read-back/reconciliation。该语义与 C09/D21 一致，裁决 **PASS**。建议作者在下一轮将“三证”显式标注为 D21 接口，但这不是新增平行定义。

## 4. 路由、让位、Handoff、并发、取消与单写者

| 主题 | 核查结论 | 裁决 |
| --- | --- | --- |
| 路由 | 先授权/政策/数据位置/能力/工具/负载硬门，再解释性排序；无候选可停 | PASS |
| 让位 | 沉默/超时/NO_REPLY 不构成让位；让位含已做/未做/三证/停点/回退 | PASS |
| Handoff | 精确任务与卡片版本、范围、风险、阻塞、下一步、三层 ACK、owner CAS | PASS |
| 委托 | 子执行不转移父协调责任，结果不自动完成父任务 | PASS |
| 并发 | 冻结输入、namespace、预算、writer、cancel、Join；不默认“多 Agent 更快” | PASS |
| 单写者 | 单 writer 是每对象/分区的写权约束，不等于系统只有一个 Agent | PASS |
| 取消 | request/accepted/stopping/terminal 分离；取消不是回滚 | PASS |
| UNKNOWN | 冻结重试、原 key 查询、三证对账；未知不得盲重放 | PASS |
| 硬失败 | 越权、泄密、重复不可逆副作用、cancel 后写、幽灵成功均非补偿 | PASS |

## 5. 跨平台映射

| 平台/协议 | C17 的使用方式 | 裁决 |
| --- | --- | --- |
| OpenClaw v2026.9.6 | fixed 文档只映射 Binding、session、spawn/wait、stop、yield、announce 原语；业务 owner/授权/环境终态由本书补齐 | PASS WITH FACT-SOURCE REPAIR |
| Hermes 0.20.1 | fixed delegation/lifecycle 与核验日动态文档分栏；final summary 只当候选产物 | PASS WITH SOURCE-PRECISION LIMITATION |
| A2A 1.0 | 取消、重复、2xx、idempotency 作兼容锚；对象/信任留给 C18 | PASS WITH FIXED-URL REQUIRED |
| Muse | 只写厂商公开体验；内部实现保持未知 | PASS AS VENDOR-CLAIM |

平台能力没有被做成功能对勾，也没有按相同名称假设相同语义。真实跨 Runtime cancel、receipt、owner 转移和故障恢复未执行，必须继续 `REVIEW_REQUIRED`。

## 6. D22 四层与 security/red-team 横切

### 当前问题

规范要求只有四个数据层：

```text
training / regression / holdout / representative_real_world
```

security/red-team 是横跨各层的非补偿切片，不是第五层，也不能替代 representative real-world。C17 作者 input 只有：

```text
kind = normal / security / adversarial / boundary / abnormal / recovery
```

这些是场景类型，不是 D22 layer。运行包没有 `layer`、`synthetic_shadow`、`intended_target_layer`、真实来源引用、各层计数，也没有 `representative_real_world_executed=false/count=0`。虽然它没有显式伪报真实任务执行，但机器证据无法排除下游把 60 条 synthetic 当作完整四层覆盖；`security` 也只是与其他 kind 并列，未表达“横切四层且非补偿”。

裁决：**`P1-X17-01 / REVIEW_REQUIRED`**。

### 最小关闭合同

1. 每个 scenario/trial 增加唯一 `task_id/trial_id` 与 canonical `layer`；offline synthetic 只可落在 training/regression/holdout。
2. 若为未来真实任务设计，只能记 `holdout + synthetic_shadow=true + intended_target_layer=representative_real_world`，不得直接占用真实层。
3. 结果显式派生并保留空真实层：`representative_real_world_executed=false`、count `0`、evidence count `0`。
4. security/red-team 独立为 cross-cutting suite/slice；关键失败直接阻断，不纳入平均补偿。
5. runner 在 offline synthetic 中遇到真实层、executed/count/evidence 矛盾、非法第五层时非零退出。
6. chapter、ledger E-C17-032、README、input/results/summary 与作者自检同步，仍不声称真实层或真实平台通过。

## 7. 60-trial 运行的裁决来源与反作弊

### 可确认的旁证

两个 fresh temp 原样复跑与保存结果逐字节一致；固定结果确为 60 trial、`12 PASS / 45 FAIL / 3 REVIEW_REQUIRED`、零外部副作用。这足以证明当前固定查表程序可重复。

### 不能确认的能力

runner 的 `decide()` 只接收 `fault` 字符串；HARD_FAILS 集合命中即 FAIL，`lost_receipt` 即 RR，三个指定 recovery 字符串即 PASS，其他值默认 PASS。它不读取 `common_contract`，也不从授权记录、版本、ACK、owner、writer、cancel、receipt、环境终态等原始状态推导判断。`expected` 没有参与 decision，这一点是好的；但 `fault` 本身已经承担预裁决标签。

定向负突变得到：

| 突变 | 当前实际结果 | 风险 |
| --- | --- | --- |
| task_version=-1、risk=critical、budget=0、permission_snapshot=revoked | 退出 0；decision digest 不变 | common contract 未被执行 |
| `unauthorized_route` 拼错为未知 fault | 退出 0；该安全样本变 PASS；仅 `all_expected_matched=false` | 未知输入 fail-open |
| 两个 scenario 使用同一 id | 退出 0；60 条中仅 57 个唯一 task/trial pair | 无 ID 完整性硬门 |

因此不能把 `60/60 matched_expected` 当独立判断正确率；它主要说明预置 fault 与查表逻辑相符。裁决：**`P1-X17-02 / REVIEW_REQUIRED`**。

### 最小关闭合同

1. input 保存原始观察字段，不以 `fault`、`hard_fail`、`eligible`、`handoff_valid`、`join_ready` 或等价布尔/标签直接驱动结论。
2. runner 从任务/授权版本、候选能力与负载、ACK 版本、owner CAS、writer generation、cancel 状态、receipt/read-back、必需分支和环境三证推导 FAIL/RR/PASS。
3. `expected` 只能作为离线 oracle；任何 `matched_expected=false` 必须使作者运行总门失败或非零退出，不能只写进结果。
4. 未知 enum/事件、缺字段、矛盾字段、重复 scenario/task/trial id 一律 fail closed。
5. 至少保存三类负突变：权限/预算合同被破坏、未知故障类型、重复 ID；runner 均须硬失败。
6. 保留失败样本与 UNKNOWN→RR；安全关键失败继续不可补偿。

## 8. P0 / P1 / P2

### P0

交叉逻辑本身未发现新的 P0。事实门的 `P0-F17-01`（固定来源 404）仍会阻止章节晋级，见 [fact-check.md](fact-check.md)。

### P1

1. **P1-X17-01：D22 数据谱系缺失。** 按第 6 节关闭合同修补并由非作者回归。
2. **P1-X17-02：预分类 fault 查表、common contract 不生效且未知值 fail-open。** 按第 7 节关闭合同修补并由非作者做 fresh-temp 与负突变回归。
3. **P1-F17-03：C16 门禁状态滞后。** 依赖状态必须统一为 fact/cross passed with limitations、practice pending。

### P2

1. 将“三证”明确绑定 D21 名称，便于下游机器路由；不得重定义 C09。
2. `A-C17-01` 仍写 C14 与 C16“当前均为受限输入”是正确的，但需把两者限制原因分别写准，避免把 C16 的事实/交叉门退回未审状态。

## 9. 评分

| 维度 | 得分 | 说明 |
| --- | ---: | --- |
| 论证与结构 | 14/14 | 17.1—17.7 顺序完整，机制连续。 |
| 事实准确与证据 | 13/18 | 主要语义准确；固定链接 404、A2A latest、C16 状态滞后。 |
| 原创方法与洞见 | 14/14 | 路由—让位—Handoff—并发—对账链清晰。 |
| 实践与可复现性 | 7/14 | 固定夹具可重复；D22 和原始状态推导缺失，独立练习未跑。 |
| 安全、治理与失败 | 13/14 | 非补偿失败、UNKNOWN、取消、单写者完备；runner 未 fail closed。 |
| 案例与教学 | 12/12 | CASE-C 贯穿，A/B 迁移有效。 |
| Agent 可消费性 | 7/8 | 三件产物清晰；运行 schema 尚不能可信复用。 |
| 文风与出版性 | 6/6 | 章体完整，仿生边界清楚。 |
| **总分** | **86/100** | **概念与正文强；证据链和运行谱系修补后再过门。** |

## 10. 交叉门结构化结论

```yaml
cross_gate:
  verdict: REVIEW_REQUIRED
  structure_17_1_to_17_7: PASS
  exactly_three_artifacts: PASS
  exactly_two_exercises: PASS
  c14_restricted_dependency: PASS_WITH_PRACTICE_LIMITATION
  c16_restricted_dependency: REVIEW_REQUIRED_STATUS_REFRESH
  d21_completion_semantics: PASS
  d22_four_layers: REVIEW_REQUIRED
  security_red_team_cross_cutting: REVIEW_REQUIRED_NOT_MACHINE_EXPRESSED
  routing_yield_handoff_concurrency_ownership: PASS
  c16_boundary: PASS
  c18_boundary: PASS
  fixed_60_trial_repeatability: PASS_IN_DECLARED_SYNTHETIC_SCOPE
  raw_state_decision_derivation: REVIEW_REQUIRED
  real_platform_execution: REVIEW_REQUIRED
  blocking_p1: [P1-X17-01, P1-X17-02, P1-F17-03]
  practice_gate_approved: false
  editor_gate_approved: false
  chief_editor_gate_approved: false
  release_candidate_authorized: false
```


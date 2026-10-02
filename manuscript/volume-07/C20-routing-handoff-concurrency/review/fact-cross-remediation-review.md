---
review_id: C17-fact-cross-remediation-review-20260930
chapter_id: C17
review_type: independent_fact_and_cross_remediation_review
reviewer_role: non_author_fact_and_cross_reviewer
verified_on: "2026-09-30"
chapter_status: drafting
fact_gate: PASS_WITH_LIMITATIONS
cross_gate: REVIEW_REQUIRED
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C17 post-fix 事实与交叉窄复核

## 裁决

**事实门：`PASS WITH LIMITATIONS`。** 前次阻断事实门的三项问题已经关闭：OpenClaw `OC-SESSION` 已锁定固定提交下真实存在的 `docs/concepts/session-tool.md`；A2A 已固定到 `/v1.0.0/specification/`；Hermes fixed 来源已收窄到固定 `delegation.md`。C16 状态已统一为“事实/交叉门有限制通过、实践待审”，C14 状态已统一为“v3.1 离线状态化机器控制已复现、真实授权实践仍受限”。32/32 evidence 引用闭合、固定/动态/VENDOR-CLAIM 身份未发生越界。限制仍是：三项 ledger source 未被 claim 消费，且真实 OpenClaw/Hermes/A2A 跨 Runtime 行为没有被本轮执行。

**交叉门：`REVIEW_REQUIRED`。** 前次 `P1-X17-01` 已关闭：作者包现在严格保留 D22 四层、真实层为 0、12 条 `holdout + synthetic_shadow`，security/red-team 为横切非补偿切片。前次 `P1-X17-02` 的主要部分也已关闭：runner 已从 common contract、路由、Handoff/ACK/owner CAS、writer lease、effect ledger、cancel、wait-for graph、progress、branches 与 receipt read-back 原始状态推导裁决，并对合同破坏、非法枚举、重复 ID、合成冒充真实层、真实层 manifest 不匹配、缺字段和 oracle 不符硬失败。

但两项 P1 仍阻断交叉门：D21 三证仍只是调用方提供的四个值，runner 未做严格布尔类型或证据对象验证；把四个值全部改成字符串 `"dummy"` 后仍退出 0，并保持原 12/45/3 分布。其次，未知嵌套字段会被静默忽略；加入 `route.mystery_authority=true` 后仍退出 0。由此不能把“已完全状态化”扩大为“三证已经由证据推导”或“schema 已 closed-world”。

本复核未修改正文、ledger、母产物、练习或作者运行包；只新增本记录及机器可读的 [复现记录](fact-cross-remediation-reproduction-20260930.yaml)。本复核不批准实践门、编辑门、总编门或 `release_candidate`。

## 1. 前次问题关闭矩阵

| 问题 | post-fix 证据 | 裁决 |
| --- | --- | --- |
| P0-F17-01：`OC-SESSION` 固定来源 404 | ledger 已改为固定提交的 `docs/concepts/session-tool.md`，链接返回 200；E-C17-006/024 可解引用 | **CLOSED** |
| P1-F17-02：A2A 使用可漂移 `/latest/` | ledger 已固定为 `https://a2a-protocol.org/v1.0.0/specification/`，返回 200 | **CLOSED** |
| P1-F17-03：C14/C16 状态滞后 | frontmatter、章首受限输入、E-C17-030、产物与作者自检均使用当前受限状态 | **CLOSED** |
| P2-F17-05：Hermes fixed 粒度过粗 | `HERMES-FIXED` 已收窄到固定提交的 `website/docs/user-guide/features/delegation.md` | **CLOSED** |
| P1-X17-01：D22 与 security 谱系缺失 | 四层结果显式保留空真实层；真实层 executed=false/count=0；12 条 shadow 均为 holdout；security 为横切且关键失败非补偿 | **CLOSED** |
| P1-X17-02：fault 查表、common contract 不生效、未知 enum/重复 ID fail-open | fault 选择器已移除；runner 消费原始状态；合同、非法 enum、重复 ID、synthetic 冒充 real、manifest 不匹配、缺字段、oracle 不符均非零退出 | **PARTIALLY CLOSED** |
| P2-F17-04：三个 source 未被 claim 消费 | `QUALITY`、`TERMS`、`OC-DELEGATE` 仍未被 claim 消费 | **OPEN / NON-BLOCKING** |

## 2. 固定事实与平台身份复核

### OpenClaw fixed

OpenClaw 基线仍锁定 `v2026.9.6 / eb377ac59e6c9fd6c7705028034812becf00271b`。`OC-SESSION` 现在精确指向固定提交下的 `docs/concepts/session-tool.md`，与本章“spawn accepted 不等于完成、wait timeout 不等于停止”的有限使用一致。正文没有把 Binding 写成业务授权，也没有把 session/wait 原语扩写成责任接管或环境完成。

### Hermes fixed / dynamic

Hermes fixed 仍锁定 `0.20.1` 对应提交，且固定来源已从仓库根收窄到 `delegation.md`；动态文档仍以核验日页面单列。正文只用固定页支持隔离子会话、最终摘要返回和工具权限不能扩大，没有把动态页倒填进固定版本。

### A2A 1.0

A2A 证据已固定到 `/v1.0.0/specification/`。正文只用其锚定取消是尝试、消息/推送可能重复、HTTP 接收不等于业务责任与完成；Responsibility ACK、owner CAS 和 Handoff 卡仍明确是本书方法，未冒充 A2A 标准对象。

### Muse

Muse 仍只作为 `VENDOR-CLAIM` 的体验镜面；本章没有由公开发布页推断内部路由、Handoff、ACK、writer、cancel 或并发实现。

## 3. 上游状态与定义权

- C14：当前表述准确到“事实/交叉已过；v3.1 离线状态化机器控制已复现；真实授权环境与真实平台实践仍受限”。C17 没有把该旁证升级为真实授权通过。
- C16：当前表述准确到“事实/交叉 `PASS WITH LIMITATIONS`；practice pending”。C17 继续把组织拓扑、角色与责任作为受限输入，没有声称真实多 Agent 组织已验证。
- C17 仍拥有路由、让位、Handoff、并发/取消/合并；C16 拥有组织拓扑，C18 拥有 A2A 对象、身份与信任。修补没有改变这条定义权边界。

## 4. fresh-temp 双复现

把作者原 `run-routing-harness.py` 与 `synthetic-routing-input.yaml` 分别复制到两个全新临时目录，使用同一 Python 解释器离线运行：

- 两次进程均退出 0；
- 两份 results 逐字节相同，且与作者保存的 results 逐字节相同；
- results SHA-256：`43189c7af870af382672e21151d7218c0410b9a651146c7e771b6c03e49a2dad`；
- 两份 summary 逐字节相同，且与作者保存的 summary 逐字节相同；
- summary SHA-256：`f033b55fca295a5ba30224a57d7788f3ba9843227498e99a22b73690e1959f33`；
- decision digest：`ded2183899a81e1e6336cd96e0f8bc0792337bce60ba4d92c2cb542569a0ce8e`；
- 20 scenario × 3 = 60 trial，task/trial pair 唯一；
- 分布为 `12 PASS / 45 FAIL / 3 REVIEW_REQUIRED`；
- 外部副作用计数为 0；
- D22：training `3 PASS / 9 FAIL`，regression `6 PASS / 12 FAIL`，holdout `3 PASS / 24 FAIL / 3 REVIEW_REQUIRED`，representative real-world 为空；
- `representative_real_world_executed=false`、trial count=0；
- synthetic shadow trial count=12；security 关键失败非补偿为 true。

这证明固定离线合成包的可重复性与保存计数，没有证明真实 Runtime、真实渠道、真实授权、真实跨系统取消、生产副作用或代表性真实任务表现。

## 5. 定向负突变

| 突变 | 预期 | 实际 | 裁决 |
| --- | --- | --- | --- |
| common permission snapshot 改为未授权值 | 硬失败 | exit 1；`common permission snapshot is not currently authorized`；不产出结果 | PASS |
| budget 改为 0 | 硬失败 | exit 1；`task version and budget must be positive`；不产出结果 | PASS |
| `yield.agent_status=ALIEN` | 硬失败 | exit 1；`unknown agent status` | PASS |
| 重复 scenario ID | 硬失败 | exit 1；`scenario ids must be unique` | PASS |
| synthetic 记录直接占用 `representative_real_world` | 硬失败 | exit 1；`synthetic fixture cannot claim representative_real_world execution` | PASS |
| real-world 记录与 manifest 的 source/run 不符 | 硬失败 | exit 1；`real-world source/run ids must match manifest` | PASS |
| 删除 `route.capability_evidence_refs` | 硬失败 | exit 1；`KeyError: capability_evidence_refs` | PASS WITH DIAGNOSTIC LIMITATION |
| 修改 S01 oracle，使 expected 与派生裁决不符 | 硬失败 | exit 1；`one or more decisions do not match the frozen offline oracle` | PASS |
| D21 四值全部替换为字符串 `"dummy"` | 类型或证据门硬失败 | **exit 0**；仍为 12/45/3 | **FAIL** |
| 增加未知嵌套字段 `route.mystery_authority=true` | closed-world schema 硬失败 | **exit 0**；仍为 12/45/3 | **FAIL** |

缺字段目前会因 Python `KeyError` 停止，安全方向是 fail closed，但错误不带 scenario/字段路径，仍是可诊断性限制。真正阻断点不是错误文案，而是 D21 接受任意 truthy 值，以及未知字段静默通过。

## 6. 仍开放的 P1

### P1-X17-R01：D21 三证仍是自报值，未由证据推导

runner 检查的是：当 `reported_complete` 为真时，另外三个字段是否都 truthy。它既不校验严格布尔类型，也不要求过程执行、交付可见、业务/环境验收各自有证据引用、来源、观察值与 digest。因此 `"dummy"` 会被当成真，调用方可以用四个自报字符串制造完成。

**最小关闭合同：**

1. 把 D21 三层改为结构化证据对象，至少包含 `evidence_id/ref`、观察来源、观察终态、内容/对象 digest 或等价绑定；业务/环境层须指向权威系统或明确 `UNKNOWN`。
2. runner 从三层证据对象派生 `technical_execution`、`delivery_visibility`、`business_environment_acceptance` 与总完成状态；不得让调用方直接提交四个最终布尔结论。
3. 若阶段性仍保留布尔字段，至少做严格 `type(value) is bool`，并与证据对象交叉核对；字符串、数字、null、缺字段、矛盾值均硬失败。
4. 保存 `dummy`、缺证据、digest 不符、环境证据 UNKNOWN 却 reported complete 四类回归；关键失败不得被其他场景补偿。

### P1-X17-R02：嵌套 schema 不是 closed-world

当前只检查顶层 required 字段和少量枚举，`route`、`handoff`、`cancel`、`receipt`、`d21` 等对象的未知键会被静默忽略。对普通扩展字段这可能只是兼容性选择；但当未知字段名称暗示权限、owner、receipt 或完成语义时，静默忽略会造成“调用方以为字段生效、控制面实际未消费”的双重解释。

**最小关闭合同：**

1. 为 top-level、contract、state、scenario 及 route/yield/handoff/writer/effect/cancel/progress/branches/receipt/d21 建立显式 required/optional/allowed key 集和类型约束。
2. 控制/权限/责任/完成相关对象默认拒绝未知字段；若需要扩展，使用版本化 `extensions` namespace，不得与主 schema 同层。
3. 缺字段应输出含 scenario ID 与完整字段路径的确定性错误，而非裸 `KeyError`。
4. 保存未知 authority/owner/completion 字段、错误类型、缺字段与 schema_version 不支持四类负突变；均须在产生 results 前非零退出。

## 7. 门禁结构化结论

```yaml
fact_gate:
  verdict: PASS_WITH_LIMITATIONS
  closed: [P0-F17-01, P1-F17-02, P1-F17-03, P2-F17-05]
  nonblocking_open: [P2-F17-04]
  claim_reference_closure: 32/32
  fixed_dynamic_vendor_identity: PASS
  real_platform_validation: REVIEW_REQUIRED
cross_gate:
  verdict: REVIEW_REQUIRED
  closed: [P1-X17-01]
  partially_closed: [P1-X17-02]
  blocking: [P1-X17-R01, P1-X17-R02]
  d22_four_layers: PASS
  security_red_team_cross_cutting: PASS
  raw_routing_handoff_concurrency_state_derivation: PASS_WITH_D21_EXCEPTION
  d21_evidence_derivation: REVIEW_REQUIRED
  nested_schema_closed_world: REVIEW_REQUIRED
  fixed_60_trial_repeatability: PASS_IN_DECLARED_SYNTHETIC_SCOPE
  real_runtime_and_platform_execution: REVIEW_REQUIRED
practice_gate_approved: false
editor_gate_approved: false
chief_editor_gate_approved: false
release_candidate_authorized: false
```

## 8. 后续复核触发器

只有作者侧按上述两项 P1 关闭合同修补，并由非作者重新执行 fresh-temp 双复现、`dummy` 三证、未知嵌套字段、缺字段/类型错、oracle 不符和 D22 冒充真实层负突变后，交叉门才可重新判断。即使届时交叉门通过，也不能替代独立实践门；真实 OpenClaw/Hermes/A2A Runtime、真实渠道、真实授权、真实副作用与代表性真实任务仍须保持 `REVIEW_REQUIRED`。

## 9. 验证记录

- 本文件 frontmatter 与复现 YAML 均可由 `yaml.safe_load` 解析；chapter id 均为 C17。
- `run-routing-harness.py` 通过 `py_compile`；缓存定向到 `/tmp`，未在作者目录新增缓存文件。
- 11/11 外部 ledger URL 在 2026-09-30 检查时返回 HTTP 200。
- 32/32 evidence claim 被正文引用；missing=0、orphan=0。
- 两个新增文件的相对链接检查为 0 broken；全书 `validate-formal-manuscript.py` 通过，C17 为 18,149 CJK。
- `validate-book.py` 当前仅因 C15 既有 `post-fix-practice-review.md` 指向缺失的 `runs/post-fix-independent-drift-reproduction-20260930.yaml` 而失败；错误不位于 C17，也不是本轮新增。C17 本轮新增文件没有破链。
- 限定状态检查只显示本次新增的两份审校记录；没有修改作者正文、ledger、产物、练习或 runs。

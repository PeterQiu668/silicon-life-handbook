---
review_id: C17-fact-check-20260930
chapter_id: C17
review_type: independent_fact_check
reviewer_role: non_author_fact_reviewer
verified_on: "2026-09-30"
chapter_status: drafting
fact_gate: REVIEW_REQUIRED
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C17 独立事实核查

## 裁决

**事实门：`REVIEW_REQUIRED`。** 32 条 evidence 均被正文引用，正文没有孤儿引用；OpenClaw `v2026.9.6`、Hermes `0.20.1`、A2A 1.0 与 Muse `VENDOR-CLAIM` 的主要语义总体准确。但一个固定 OpenClaw 来源在锁定提交上为 404，A2A 来源使用可漂移的 `/latest/`，C16 的门禁状态已经被后续审校推进而 C17 仍写成“独立门待签”。事实链尚不能签 `PASS`。

本审查没有修改正文、ledger、母产物、练习或作者运行包，也不执行或批准两项练习的独立实践。机器可读明细见 [source-audit-20260930.yaml](source-audit-20260930.yaml)。

## 1. 账本闭合与版本身份

- 账本共 23 个 source、32 个 claim；32/32 claim 均在正文出现，缺失引用与孤儿引用均为 0。
- 20/23 source 被 claim 消费；`QUALITY`、`TERMS`、`OC-DELEGATE` 未使用，记为 P2 证据卫生项。
- OpenClaw annotated tag `v2026.9.6` 解引用到 `eb377ac59e6c9fd6c7705028034812becf00271b`，正文所有产品实现页除一条错误路径外均锁该提交。
- Hermes annotated tag `v2026.8.13` 解引用到 `f80f453ae0679347e38abc917c7f94f717bf96c5`；固定 `pyproject.toml` 为 `0.20.1`。固定实现与动态官方文档在正文中没有倒填。
- A2A `/v1.0.0/specification/` 明确支持取消是尝试、Send Message 仅 MAY 幂等、push 可能重复且 HTTP 2xx 只确认接收。ledger 当前却使用 `/latest/specification/`，在 2026-09-30 虽指向 1.0.0，仍不具固定身份。
- Muse 仅用于公开体验镜面。正文明确说不能由发布页反推内部路由、Handoff 或并发实现，符合 `VENDOR-CLAIM` 上限。

## 2. 32 条 claim 逐条裁决

| Evidence | 裁决 | 核查摘要 |
| --- | --- | --- |
| E-C17-001 | PASS | 先授权/政策/位置/能力/工具/负载硬门，再软排序，是本书方法且与 C11/C14 一致。 |
| E-C17-002 | PASS | 多维可解释路由未压成不可审计总分。 |
| E-C17-003 | PASS | 固定 OpenClaw 文档只证明 Binding 将入口映射到 Agent；C06/C14 支持其不等于任务适配或授权。 |
| E-C17-004 | PASS | 固定 yield 文档要求显式 ownership transfer；沉默、timeout、offline、NO_REPLY 不被扩写为让位。 |
| E-C17-005 | PASS | 让位最小包与 C09 三证、preflight 一致。 |
| E-C17-006 | REVIEW_REQUIRED | “委托不转移父责任/子结果不自动完成父任务”语义成立，但所列 `OC-SESSION` 链接在固定提交为 404。 |
| E-C17-007 | PASS | Handoff 卡字段与框架、章节卡、preflight 一致。 |
| E-C17-008 | PASS WITH LIMITATION | A2A 只锚定 transport receipt；Object/Responsibility ACK 被明确标为本书方法，没有冒充 A2A 内建对象。 |
| E-C17-009 | PASS | Responsibility ACK 与权威 owner 原子更新共同完成责任转移，是本章方法。 |
| E-C17-010 | PASS | ACK_PENDING/UNKNOWN 保持原 owner，符合唯一责任链。 |
| E-C17-011 | PASS | 旧版本 ACK 判 STALE，方法定义明确。 |
| E-C17-012 | PASS | 秘密引用而非可重放 secret，和 C11/C14 边界一致。 |
| E-C17-013 | PASS | 冻结输入、独立验收、受控共享状态、可观察取消和 Join 与 C16 接口一致。 |
| E-C17-014 | PASS WITH LIMITATION | 单写者/CAS/lease/fencing 是本书工程方法；OpenClaw lane 页只直接支持每 session 单写和所有权边界，正文未冒充平台原生完整实现。 |
| E-C17-015 | PASS | action/key 稳定、attempt 可变，与 C11 一致。 |
| E-C17-016 | PASS | A2A 明示推送可能重复；OpenClaw 固定页也不声称重启边界全局 exactly-once。 |
| E-C17-017 | PASS | receipt UNKNOWN 先向权威系统对账，不盲重试。 |
| E-C17-018 | PASS | A2A 1.0 明确取消只尝试；OpenClaw 固定操作页也区分请求与实际停止。 |
| E-C17-019 | PASS | Join 读取分支、取消、版本、writer、重复、receipt 与三证，没有只看 Agent 自报。 |
| E-C17-020 | PASS | 冲突分类与裁决 owner 是方法论，无平台效果外推。 |
| E-C17-021 | PASS | 死锁 timeout 不转 owner，活锁用进度与上限止损，方法边界清楚。 |
| E-C17-022 | PASS | 单一事实源按事实类型指定权威 owner，不等于单文件。 |
| E-C17-023 | PASS | OpenClaw fixed Binding 事实有直接固定文档支持。 |
| E-C17-024 | REVIEW_REQUIRED | `accepted` 非完成、wait timeout 非停止的语义受固定文档支持，但 ledger 的 `OC-SESSION` 路径不可解引用。 |
| E-C17-025 | PASS | announce status 来自 runtime outcome；需要交付物时 NO_REPLY/无输出是 missing deliverable，而非静默成功。 |
| E-C17-026 | PASS WITH LIMITATION | 固定 delegation.md 和 lifecycle 源码支持隔离上下文、只把最终摘要送回父上下文、工具不可扩大；ledger 应从仓库根收窄到精确文件。 |
| E-C17-027 | PASS WITH LIMITATION | 取消、重复与 2xx 语义准确；必须把来源固定到 `/v1.0.0/`。 |
| E-C17-028 | PASS | A2A 对象与信任定义明确交 C18；C17 只保留兼容锚。 |
| E-C17-029 | PASS | Muse 没有被推断为具备内部路由、Handoff 或并发机制。 |
| E-C17-030 | REVIEW_REQUIRED | C14 状态准确；C16 当前已 fact/cross PASS WITH LIMITATIONS、practice pending，不再是“独立门均待签”。 |
| E-C17-031 | PASS | `artifacts/` 恰好三件正式母产物。 |
| E-C17-032 | PASS IN DECLARED SYNTHETIC SCOPE | 两个 fresh temp 原样复跑与保存结果逐字节一致；60 trial 为 12/45/3、零外部副作用。只证明冻结查表夹具确定性。 |

## 3. 平台与协议核查

### OpenClaw fixed：语义通过，来源路径阻断

固定文档直接支持：Binding 的入口映射；`sessions_spawn` 的 accepted 非完成；wait/观察 timeout 不取消执行；显式 Stop 的范围与不完整取消；yield 的唯一 completion owner、新 admission 和旧权限不复活；announce 状态来自 runtime outcome，缺失必需 deliverable 不算静默成功。

阻断点是 ledger 的：

```text
docs/tools/session-tool.md
```

固定提交下返回 404；同一提交的正确位置是：

```text
docs/concepts/session-tool.md
```

这不是正文语义反例，但违反证据可解引用硬门，故记 `P0-F17-01`。

### Hermes fixed/dynamic：通过，需提高固定来源粒度

固定 `website/docs/user-guide/features/delegation.md` 写明 child 为隔离上下文、父上下文只进入 final summary、模型不能扩大父工具集；固定 `agent/subagent_lifecycle.py` 也会拒绝 broaden parent permissions。动态页另栏且核验日期明确。当前 `HERMES-FIXED` 只指仓库根，虽可追溯但审计成本过高，记 P2。

### A2A 1.0：语义通过，固定身份待修

正文对取消、幂等、重复投递和 HTTP 2xx 的解释与 1.0.0 规范一致，也没有把本书 Responsibility ACK 冒充 A2A 标准对象。但 `/latest/` 会随发布漂移；C16 已统一采用 `/v1.0.0/specification/`，C17 应相同，记 `P1-F17-02`。

### Muse：PASS AS VENDOR-CLAIM

Meta 发布页支持后台继续工作、敏感动作前询问批准、可见审计轨迹等厂商自述。C17 只用这些作为体验镜面，并明确内部路由、Handoff、ACK 和并发实现未知，没有越过证据上限。

## 4. 作者运行的事实完整性旁证

作者固定 input/runner 在两个 fresh temp 中复跑：

- 两次输出字节相同，并与保存结果相同；
- 输出 SHA-256 为 `427e55a038907e4cf4f029fa8c1b8a3f74b5c52e2a4295ea64f07092e3291a21`；
- decision digest 为 `53b10730056f80d302de285d36bf4fc7cf9103fdb1a808a7a7445f7012b03231`；
- 60 个 trial、20 个 task id、60 个唯一 trial id；`12 PASS / 45 FAIL / 3 REVIEW_REQUIRED`；
- `external_side_effect_count=0`。

因此 E-C17-032 在其声明的“冻结离线合成夹具”范围内成立。runner 是否足以证明两项练习、D22 与一般化安全控制，属于交叉/实践问题，见 [cross-review.md](cross-review.md)，不倒判固定计数为伪造。

## 5. P0 / P1 / P2 与最小关闭合同

### P0

1. **P0-F17-01 / `OC-SESSION` 固定来源 404。** 关闭合同：将 ledger URL 改为固定提交下的 `docs/concepts/session-tool.md`；重新核对 E-C17-006/024；全量链接审计须为 200。

### P1

1. **P1-F17-02 / A2A 来源可漂移。** 关闭合同：把 `A2A-SPEC` 固定为 `https://a2a-protocol.org/v1.0.0/specification/`；正文仍可写协议线 A2A 1.0。
2. **P1-F17-03 / C16 状态滞后。** 关闭合同：frontmatter、章首受限输入、A-C17-01、E-C17-030、开放问题与作者自检统一改为“C16 fact/cross PASS WITH LIMITATIONS；practice pending”；仍不得把真实组织实践写成通过。

### P2

1. `QUALITY`、`TERMS`、`OC-DELEGATE` 三个 source 未被 claim 使用：绑定到实际 claim 或删除，不保留装饰性来源。
2. 将 `HERMES-FIXED` 从仓库根收窄到固定 `delegation.md`，必要时增加固定 `subagent_lifecycle.py`，使隔离/summary/tool attenuation 可直接定位。

## 6. 事实门结构化结论

```yaml
fact_gate:
  verdict: REVIEW_REQUIRED
  claim_count: 32
  claim_reference_closure: 32/32
  blocking_p0: [P0-F17-01]
  open_p1: [P1-F17-02, P1-F17-03]
  open_p2: [P2-F17-04, P2-F17-05]
  openclaw_fixed_semantics: PASS_WITH_SOURCE_REPAIR_REQUIRED
  hermes_fixed_dynamic_separation: PASS_WITH_SOURCE_PRECISION_LIMITATION
  a2a_1_0_semantics: PASS_WITH_FIXED_URL_REQUIRED
  muse_vendor_claim_boundary: PASS
  author_run_count_integrity: PASS_IN_DECLARED_SYNTHETIC_SCOPE
  real_platform_validation: REVIEW_REQUIRED
  practice_gate_approved: false
  release_candidate_authorized: false
```


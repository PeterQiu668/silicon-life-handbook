---
review_id: C18-independent-fact-check-20260930
chapter_id: C18
review_type: independent_fact_check
reviewer_role: non_author_fact_reviewer
verified_on: "2026-09-30"
chapter_status: drafting
fact_gate: REVIEW_REQUIRED
cross_gate: separate_record
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C18 独立事实核查

## 裁决

**事实门：`REVIEW_REQUIRED`。** C18 的标准语义和平台边界主体正确：Message、Task、流式/推送 Event、Artifact 与 Agent Card 的基本语义得到 A2A 1.0.0 规范支持；OpenClaw `v2026.9.6 / eb377ac…` 的 A2A 子集和缺口得到固定文档支持；Hermes 固定 delegation/lifecycle 只被用作实现镜面，没有冒充 A2A 兼容；Muse 保持 `VENDOR-CLAIM`。32/32 claim 均在正文出现，缺失引用和孤儿引用均为 0。

事实门仍被两项 P1 阻断：ledger 的 A2A 主规范来源仍是可漂移的 `/latest/specification/`，不满足本轮明确要求的 `/v1.0.0/specification/` 固定身份；E-C18-029 与 frontmatter 的上游门禁状态已经滞后，未记录 C14、C16、C17 当前各自不同的受限结论。另外，E-C18-005 把 A2A 原生 Artifact 语义和本书的版本/验收治理写进一条 `STANDARD-FACT`，需要拆分或改标 `METHODOLOGY`。

本记录没有修改正文、证据账本、母产物、练习或作者 runs；运行包有效性由 [交叉审校](cross-review.md) 单独裁决。本记录不批准实践、编辑、总编或 `release_candidate`。

## 1. 证据账本与可达性

- source 共 20 个：本地与本书输入 11 个、外部来源 9 个。
- 32 个 evidence ID 全部唯一；正文引用 32/32，missing=0、orphan=0。
- 19/20 source 被 claim 消费；`OC-SESSION` 未被任何 claim 使用，属 P2 证据卫生问题。
- 9/9 外部 URL 最终均返回 HTTP 200；`OC-SESSION` 首次并发检查超时，单独重试为 200。
- OpenClaw annotated tag `v2026.9.6` 解引用到 `eb377ac59e6c9fd6c7705028034812becf00271b`。
- Hermes annotated tag `v2026.8.13` 解引用到 `f80f453ae0679347e38abc917c7f94f717bf96c5`，章节按 `0.20.1 fixed + dynamic docs` 分栏。
- A2A `v1.0.1` release tag 存在并指向 `3303592588e388e62e0f69f701af531d2f4e3991`；它在本章只作为 1.0 协议线 patch release 记录。

## 2. 32 条 claim 逐项裁决

| Evidence | 裁决 | 核查摘要 |
| --- | --- | --- |
| E-C18-001 | PASS | A2A 规范分别定义 Message、Task、Artifact，以及 TaskStatusUpdateEvent / TaskArtifactUpdateEvent；本章把后两者归为 Event 类别，边界清楚。 |
| E-C18-002 | PASS | Message 是通信对象，可关联 Task；不承载完整 Task 生命周期，也不自动成为交付物。 |
| E-C18-003 | PASS | Task 的 id、contextId、status、artifacts、history 与 metadata 得到 1.0.0 规范支持。 |
| E-C18-004 | PASS AS METHODOLOGY | 重复通知得到规范直接支持；乱序、空洞与快照对账是合理工程方法，没有冒充协议强制字段。 |
| E-C18-005 | PASS WITH CLASSIFICATION LIMITATION | A2A Artifact 原生含 artifactId、parts、metadata、extensions，但没有原生 `version` 字段；版本、owner、验收和保留是本书治理要求。当前单条 `STANDARD-FACT` 混合两层。 |
| E-C18-006 | PASS | protocol/execution/acceptance 三层是 D21/C18 方法论，未冒充 A2A 原生三字段。 |
| E-C18-007 | PASS | HTTP/协议终态不推出业务 PASS，与 D21 及 A2A transport/Task 语义一致。 |
| E-C18-008 | PASS | timeout 只结束本地观察窗口，是 C17/C18 方法论，正文没有声称 A2A 自动终止。 |
| E-C18-009 | PASS WITH CLASSIFICATION LIMITATION | A2A 支持 CancelTask 且可返回 not cancelable；“ACK 不等于 STOP_CONFIRMED”是本书执行证据方法，超出纯 `STANDARD-FACT`。 |
| E-C18-010 | PASS | Send Message 仅 MAY 依据 messageId 幂等，push 可能重复；未承诺 exactly-once。 |
| E-C18-011 | PASS | Agent Card 的 supportedInterfaces、capabilities、skills、securitySchemes、signatures 等字段得到 1.0.0 规范支持。 |
| E-C18-012 | PASS | 规范称 Card 为 self-describing manifest；不把它外推为组织身份证、能力证书或授权是必要边界。 |
| E-C18-013 | PASS AS METHODOLOGY | 六层审查来自 preflight，本章明确为治理方法。 |
| E-C18-014 | PASS | 规范说明 JWS 用于验证来源与完整性；正文没有把签名扩大为事实正确性。 |
| E-C18-015 | PASS AS METHODOLOGY | digest/signature 与内容正确、输入有权分离，边界正确。 |
| E-C18-016 | PASS | producer、owner、accountable human 分离是本书组织方法，未声称为 A2A 原生字段。 |
| E-C18-017 | PASS | schema、完整性、内容、权限/政策、环境效果和缺口的验收链与 D21/前置研究一致。 |
| E-C18-018 | PASS | supersedes、更正和撤回是本书 Artifact 治理方法，身份明确。 |
| E-C18-019 | PASS | 七维信任记录为本章方法，没有伪装为 A2A 标准评分。 |
| E-C18-020 | PASS | 动态信任只可收紧或作为 C14 输入，不得自行创造权限。 |
| E-C18-021 | PASS | 防刷分、防串谋、衰减、更正和申诉属于本章治理方法。 |
| E-C18-022 | PASS | 安全、授权、数据位置与证据操纵被写为非补偿硬门，符合质量合同。 |
| E-C18-023 | REVIEW_REQUIRED | “协议 1.0 + v1.0.1 patch release”口径可成立，但主规范来源使用 `/latest/`，没有锁定到要求的 `/v1.0.0/`。 |
| E-C18-024 | PASS | OpenClaw 固定文档逐项明确不支持 streaming、SSE、push、cancel、list、extended card、multi-tenant routing，Task 只保留于内存。 |
| E-C18-025 | PASS | 固定文档明确因无 plugin-facing abort seam 而拒绝 CancelTask，不伪报 CANCELED。 |
| E-C18-026 | PASS | Hermes 固定 delegation/lifecycle 支持隔离、结果摘要、取消/未知与 stable hash；正文继续把 A2A 兼容标 UNKNOWN。 |
| E-C18-027 | PASS AS VENDOR-CLAIM | Muse 只用于 Goals/Activity/Artifacts/approval 体验镜面，没有推断内部协议、签名或信任分。 |
| E-C18-028 | PASS | C17 路由/Handoff 与 C19 身份、密钥、凭证、威胁模型的定义权没有被 C18 重定义。 |
| E-C18-029 | REVIEW_REQUIRED | “C14 修补与 C17 独立门仍在运行”已滞后，且遗漏 C16 当前受限状态；需按最新独立门记录更新。 |
| E-C18-030 | PASS | `artifacts/` 恰好三件正式母产物，名称与章节卡一致。 |
| E-C18-031 | PASS IN FROZEN SYNTHETIC SCOPE | fresh-temp 双复现确认 18 trial、3/11/4、保存结果逐字节一致；不证明运行控制充分。 |
| E-C18-032 | PASS IN FROZEN FIXTURE WITH ENFORCEMENT LIMITATION | 保存输入确实真实层为 0；runner 不会阻止 synthetic 冒充真实层，属于交叉门阻断而非静态计数伪造。 |

## 3. A2A 固定身份与语义边界

`https://a2a-protocol.org/v1.0.0/specification/` 当前可达，并明确给出 1.0.0 的 Task、Message、Artifact、流式事件、Agent Card、JWS、幂等、push 和 CancelTask 语义。ledger 当前却指向：

```text
https://a2a-protocol.org/latest/specification/
```

即使核验日页面内容仍与 1.0.0 相符，`latest` 也可能随发布漂移。本章另有 v1.0.1 GitHub patch release 来源，因此最小事实链应为“固定 1.0.0 规范 + 固定 v1.0.1 release”，而不是“动态 latest + patch”。

另需精确区分：A2A 1.0.0 的 Artifact 原生字段是 `artifactId/name/description/parts/metadata/extensions`；本书增加的 version、digest、owner、provenance、acceptance 和 retention 是治理信封，不应全部归为协议原生事实。

## 4. OpenClaw、Hermes 与 Muse

### OpenClaw fixed：PASS

固定 `docs/channels/a2a.md` 直接支持：A2A 1.0 JSON-RPC、每 peer bearer token、peer+context 会话隔离、文本/结构化数据、returnImmediately/poll、CancelTask 明确拒绝、命令与审批不由 peer 越过，以及不支持 streaming/push/cancel/list/extended card/multi-tenant routing/持久 Task。E-C18-024/025 没有超出来源。

`OC-SESSION` 固定链接有效，但未被任何 claim 使用；删除或绑定到真实 claim 均可，不应作为装饰性来源保留。

### Hermes fixed/dynamic：PASS WITH UNKNOWN A2A

固定 `delegation.md` 与 `subagent-lifecycle-api.md` 支持隔离会话、工具不可扩大、取消/未知和 stable result hash。正文明确不把这些对象改名为 A2A Task/Event/Artifact，也不声称完整 A2A 1.0 兼容。动态首页单列，证据边界正确。

### Muse：PASS AS VENDOR-CLAIM

正文只引用用户可见的产品体验，内部 A2A、Card、签名、持久化和信任评分继续 `UNKNOWN / NOT_APPLICABLE`，没有证据升级。

## 5. 上游受限状态

截至本次复核，C18 应消费的准确状态是：

- **C14**：事实/交叉已通过（有限制）；v3.1 离线状态化机器控制已独立复现为 PASS；X-C14-01、X-C14-02 与总实践门仍为 `REVIEW_REQUIRED`，真实授权环境未通过。
- **C16**：事实/交叉 `PASS WITH LIMITATIONS`；独立实践门已经完成并为 `REVIEW_REQUIRED`，其 synthetic machine-control 为 FAIL；不是“practice pending”。
- **C17**：事实门 `PASS WITH LIMITATIONS`；交叉门 `REVIEW_REQUIRED`；实践门未审。D21 三证证据推导与 closed-world schema 仍是阻断项。

C18 frontmatter 只写 C14、C17 且状态笼统；E-C18-029 也沿用 preflight 旧状态，并未登记 C16。它虽然没有把上游限制扩大为生产通过，风险方向偏保守，但不满足“按当前受限状态消费”的项目事实要求。

## 6. P0 / P1 / P2 与关闭合同

### P0

本次事实语义没有发现新的平台事实 P0。运行控制的 P0 见 [交叉审校](cross-review.md)。

### P1

1. **P1-F18-01 / A2A 主规范身份可漂移。** 将 `A2A` 固定为 `https://a2a-protocol.org/v1.0.0/specification/`；保留 `A2A-PATCH` 的 v1.0.1 固定 release；重核 E-C18-001—014、023。
2. **P1-F18-02 / C14、C16、C17 状态滞后。** 同步 frontmatter `restricted_inputs`、章首、E-C18-029、开放问题、作者自检与章际交接；三章均只能按上述受限状态消费。
3. **P1-F18-03 / Artifact 标准事实与治理方法混写。** 将 E-C18-005 拆成“A2A Artifact 是 Task output、含 artifactId/parts”的 `STANDARD-FACT`，以及“版本、owner、验收、保留”的 `METHODOLOGY`；E-C18-009 也应明确 STOP_CONFIRMED 是 D21/C17 方法，不是 A2A 原生字段。

### P2

1. **P2-F18-04 / 未消费来源。** `OC-SESSION` 未被 claim 使用；绑定到精确事实或删除。

## 7. 事实门结构化结论

```yaml
fact_gate:
  verdict: REVIEW_REQUIRED
  claim_count: 32
  claim_reference_closure: 32/32
  blocking_p1: [P1-F18-01, P1-F18-02, P1-F18-03]
  open_p2: [P2-F18-04]
  a2a_semantics: PASS
  a2a_fixed_identity: REVIEW_REQUIRED
  openclaw_fixed: PASS
  hermes_fixed_dynamic_separation: PASS
  hermes_a2a_compatibility: UNKNOWN
  muse_vendor_claim_boundary: PASS
  upstream_restricted_state: REVIEW_REQUIRED
  author_run_counts: PASS_IN_FROZEN_SYNTHETIC_SCOPE
  real_platform_validation: REVIEW_REQUIRED
  practice_gate_approved: false
  release_candidate_authorized: false
```


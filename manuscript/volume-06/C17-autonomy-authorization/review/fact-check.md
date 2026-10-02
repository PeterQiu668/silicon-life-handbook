---
review_id: C14-independent-fact-check-20260930
chapter_id: C14
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

# C14 独立事实核查

## 1. 裁决

C14 事实门判 **`PASS（带限制）`**。28 条 claim 全部被正文引用，逐条核查后没有 `FAIL` 或必须返工的事实主张；37 个 source 中 25 个本地来源全部存在，12 个外部来源均完成身份与语义核查。OpenClaw `v2026.9.6` 的 annotated tag 已重新解引用到固定提交 `eb377ac59e6c9fd6c7705028034812becf00271b`；Hermes `v2026.8.13` 的发行名与目标提交也重新核对。Muse 全部保持 `VENDOR-CLAIM`，没有被提升为独立验证事实。

限制有三类：NIST NCCoE 项目页当前是征求意见中的项目页而非正式标准；MCP 来源只支持协议授权硬化，正文关于业务授权/责任的否定边界属于本书方法判断；作者 28-trial 运行只证明离线规则夹具可重复，不证明真实授权、撤销传播或平台行为。另有 4 个 ledger source 未被 claim 消费，列为 P2 证据卫生项，不阻断事实门。

本文件不执行两项练习的独立实践复现，不签编辑、总编或 `release_candidate`。D22 数据层的交叉一致性问题单独记录在 [cross-review.md](cross-review.md)，不倒推已被准确记录的本地运行计数为虚假事实。

## 2. 核查范围与方法

- 逐条核对 28 个 evidence claim 的身份、来源、正文引用、语义支持与限制；
- 检查 37 个 source 的本地存在性、外部可达性、稳定性身份和 claim 消费关系；
- 通过 GitHub 官方 API 解引用 OpenClaw 与 Hermes annotated tag，避免只依赖 release 页面文字；
- 对 OpenClaw 固定提交文档、Hermes 动态官方安全页、Muse 厂商材料、NIST 与 MCP 一手页面进行内容核对，不以 HTTP 状态替代语义支持；
- 把作者 runner 与 input 复制到两个 fresh 临时目录运行，比较 fresh/fresh 与 fresh/saved 的字节和 SHA-256；该步骤只核验 E-C14-027/028，不是实践门；
- 重新计算 ledger source、claim、正文 evidence 引用和未使用 source 集合。

逐源状态与 28 条逐项结论见 [source-audit-20260930.yaml](source-audit-20260930.yaml)。

## 3. 28 条 claim 逐项结论

| Evidence | 身份 | 结论 | 核查摘要 |
| --- | --- | --- | --- |
| E-C14-001 | METHODOLOGY | PASS | 能力、自主、系统权限、组织责任四轴不可互推；未冒充外部标准。 |
| E-C14-002 | METHODOLOGY | PASS | `AU-L0—AU-L4` 与 v2、章节卡、术语表和 D19 一致。 |
| E-C14-003 | METHODOLOGY | PASS | 回答、发现、提案、准备、执行、协调、负责被处理为行为，而非新增等级。 |
| E-C14-004 | METHODOLOGY | PASS | `AU-L0—AU-L4` 与 `MAT-L0—MAT-L5` 独立命名空间完整。 |
| E-C14-005 | METHODOLOGY | PASS | 四因子是联合风险门，critical 不被平均分补偿，阈值仍留给组织。 |
| E-C14-006 | METHODOLOGY | PASS | 五维自主半径明确是本书方法，不伪装平台原生 schema。 |
| E-C14-007 | METHODOLOGY | PASS | 聊天意图与可核验授权证据分离；NIST 博文只作指导依据。 |
| E-C14-008 | METHODOLOGY | PASS | 六个绑定字段被写为本书最低集合，未声称是 NIST 强制 schema。 |
| E-C14-009 | METHODOLOGY | PASS | 子授权取三者交集且只能衰减；真实 identity graph 明确保留待实施。 |
| E-C14-010 | METHODOLOGY | PASS | 撤销传播与负向访问测试是方法要求，平台传播未被宣称已实测。 |
| E-C14-011 | METHODOLOGY | PASS | 最小权限、JIT、双人复核、break-glass 解决不同问题，不相互替代。 |
| E-C14-012 | METHODOLOGY | PASS | 双人复核要求两个独立且有资格的身份，身份图验证仍为限制。 |
| E-C14-013 | METHODOLOGY | PASS | break-glass 需预定义紧急类型、窄 scope、自动过期、审计与独立复核。 |
| E-C14-014 | METHODOLOGY | PASS | 拒绝、降级、取消、接管、过期、撤销被正确处理为合法终态或转移。 |
| E-C14-015 | METHODOLOGY | PASS | cancel、stop confirmation、rollback 与 UNKNOWN 对账清晰分离。 |
| E-C14-016 | METHODOLOGY | PASS | 主体/对象/参数/工具/模型/策略/环境/风险重大变化触发再认证。 |
| E-C14-017 | METHODOLOGY | PASS | `trigger ≠ authority ≠ completion` 与 C13、C09、D21 一致。 |
| E-C14-018 | VERSION-FACT | PASS | 固定 OpenClaw 文档支持多层 policy 收敛与下游不能放宽上游 deny。 |
| E-C14-019 | VERSION-FACT | PASS | exec approval 叠加于 tool policy/elevated；正文没有把它当业务授权。 |
| E-C14-020 | VERSION-FACT | PASS | Binding 只选择 Agent；Node pairing 建立设备身份，均不自动授权动作。 |
| E-C14-021 | VERSION-FACT | PASS | Gateway 信任域假设和 approval 非敌对多租户授权边界准确。 |
| E-C14-022 | DYNAMIC-OFFICIAL | PASS | Hermes 0.20.1 只作发行锚点，安全语义按核验日动态页处理。 |
| E-C14-023 | VENDOR-CLAIM | PASS | Sentinel、scoped capability、JIT、takeover 均保持 Meta 厂商声明。 |
| E-C14-024 | STANDARD-PRIMARY + METHODOLOGY | PASS WITH LIMITATION | MCP 支持 issuer/credential 等协议硬化；“不解决业务授权、责任、自主等级”是合理的方法边界，非协议原文事实。 |
| E-C14-025 | METHODOLOGY | PASS | D22 的规范陈述准确；运行夹具的数据来源标签问题由交叉门裁决。 |
| E-C14-026 | METHODOLOGY | PASS | artifacts 目录恰好三件母产物，运行材料未冒充第四件。 |
| E-C14-027 | LOCAL-VALIDATION | PASS IN DECLARED SYNTHETIC SCOPE | 28 trial、11 PASS/14 FAIL/3 RR、零外部副作用与保存及 fresh 复跑一致。 |
| E-C14-028 | LOCAL-VALIDATION | PASS IN DECLARED SYNTHETIC SCOPE | 所列十类以上攻击/恢复情形在输入和结果中均可定位。 |

## 4. 平台与一手来源边界

### 4.1 OpenClaw 固定版

官方 release `v2026.9.6` 的 annotated tag 已解引用到 `eb377ac59e6c9fd6c7705028034812becf00271b`。固定提交中的 [tool permissions](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/security/tool-permissions.md)、[exec approvals](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/tools/exec-approvals.md)、[agent bindings](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/agent-bindings.md)与 [trust model](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/security/trust-model.md)共同支持以下边界：policy 与 approval 是系统控制层，binding 是路由，pairing 是设备身份，单 Gateway 有单操作者/互信团队的信任假设；这些机制都不自动产生业务对象授权。

正文没有把固定文档扩写成真实部署证明，也没有把 approval、binding、pairing 或 session 当成业务 authorization。结论为 `PASS`；目标机器上的真实 policy、停止与撤销传播继续留给实践门。

### 4.2 Hermes 固定发行与动态文档

[Hermes release](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.13)的 annotated tag 指向 `f80f453ae0679347e38abc917c7f94f717bf96c5`，发行名为 Hermes Agent `v0.20.1`。正文只用它作发行锚点；dangerous-command prompt、allowlist、session 持续性和容器说明来自 2026-09-30 核验的 [动态官方安全页](https://hermes-agent.nousresearch.com/docs/user-guide/security)，没有倒填为固定版本源码事实。

结论为 `PASS WITH DYNAMIC RECHECK`。动态页与固定源码逐项对照、目标安装实测仍为 `REVIEW_REQUIRED`，这不阻断本次文本事实门。

### 4.3 Muse、NIST 与 MCP

- [Muse 产品材料](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)与 [Muse 安全材料](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)只支持 Meta 对 Sentinel、scoped capability、JIT 和 takeover 的公开陈述；正文没有推断内部同构或效果，结论 `PASS AS VENDOR-CLAIM`。
- [NIST NCCoE 项目页](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization)当前显示项目在征求意见，不能被称为已定稿标准；正文只借其说明身份/授权问题域。批量 HTTP 客户端收到 403，但浏览器可读且内容已核，结论 `PASS WITH ACCESS/STATUS LIMITATION`。
- [NIST 身份基础博文](https://www.nist.gov/blogs/cybersecurity-insights/back-future-why-agentic-ai-needs-strong-identity-foundation)支持窄 scope、委托衰减与审批疲劳方向，但属于官方指导博文，不是规范文本。
- [MCP 2026-07-28 发布说明](https://blog.modelcontextprotocol.io/posts/2026-07-28/)支持协议层 issuer validation 与 credential binding；正文正确保留“协议授权不等于业务授权”的层级边界。

## 5. 作者运行的事实完整性

在两个 fresh 临时目录中分别运行作者未修改的脚本与输入，两个 fresh 输出之间、以及 fresh 与保存输出之间均按字节一致：

```text
trials: 28
task/trial ids unique: true
distribution: PASS 11 / FAIL 14 / REVIEW_REQUIRED 3
all expected matched: true
external side effects: 0
results SHA-256: c9c4868f5456954e61d6f668596d7703e58b32d4421939f94731a8adda0b2ce7
summary SHA-256: e093bb2096e35af6609f292ff6e88dfefc4938a0817eb1aa0fb566366a8964db
```
这证明 E-C14-027/028 对“保存的合成运行发生了什么”的描述准确，不证明规则正确覆盖真实授权服务，也不构成 X-C14-01/02 的独立实践签核。

## 6. 问题分级与关闭条件

### P0

无。未发现伪造固定版本、把 Muse 当已验证实现、用人格文本授予权限、把 binding/approval 当业务授权、删除失败样本或把本地夹具包装成生产效果。

### P1

无事实门 P1。D22 的合成样本来源标签是跨章规范问题，见 `P1-X14-01`，由交叉门阻断。

### P2

1. **P2-F14-01 / 4 个未消费 source。** `C03`、`C05`、`C18-P`、`C22-P` 已登记且文件存在，但没有进入任何 claim 的 `source_ids`。关闭条件：若确实支撑主张，将其绑定到相应 claim 并复核语义；若只作写作背景，从 ledger source 集合移除。不得为了计数创建空 claim。

## 7. 事实门结构化结论

```yaml
fact_gate:
  chapter_id: C14
  verdict: PASS
  limitations_present: true
  claims_checked: 28
  claims_pass_or_pass_with_declared_limitation: 28
  claims_review_required: 0
  claims_fail: 0
  sources_checked: 37
  local_sources_present: "25/25"
  external_sources_content_checked: "12/12"
  external_batch_http_200: "11/12"
  external_browser_checked_after_http_403: [NIST-ID]
  source_usage: "33/37"
  evidence_reference_closure: "28/28"
  fixed_release_resolution: PASS
  author_run_claim_integrity: PASS_IN_DECLARED_SYNTHETIC_SCOPE
  independent_practice_performed: false
  practice_approved: false
  editor_approved: false
  chief_editor_approved: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

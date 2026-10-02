---
review_id: C11-independent-fact-check-20260930
chapter_id: C11
review_type: independent-fact-check
reviewed_on: "2026-09-30"
reviewer_role: evidence-reviewer-and-editorial-orchestrator
chapter_status: drafting
fact_gate: passed_with_limitations
cross_gate: separate_record
practice_gate: not_reviewed
editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C11 独立事实核查

## 1. 结论

C11 的 25 条 evidence claim 与正文引用全部闭合，41 个来源全部被 claim 消费；15 个本地来源均存在，26 个外部一手来源在 2026-09-30 本轮均返回 HTTP 200。MCP `2026-07-28`、OpenClaw 固定提交、Hermes release 与动态官网、Muse 厂商声明、本书方法论和作者合成运行没有混成同一种证据。

事实门结论为 **`PASS WITH LIMITATIONS`**。限制主要来自：Hermes MCP/Security/Code Execution 为核验日动态页面，尚未逐项固定到 `v0.20.1` 源码；Muse 为闭源厂商公开自述；真实 MCP Server、OAuth、Provider receipt、Browser、Sandbox、SecretRef、幂等和补偿均未在目标部署实测。作者合成结果只证明固定夹具的门禁路由，不能构成协议认证、平台安全证明或生产放行。

本核查不执行作者 harness，不签实践、编辑、总编或 RC 门。章节继续为 `drafting`。

## 2. 核查方法

- 使用 `evidence-ledger.yaml` 中的 class、stability、source IDs 和 limitations 检查每条主张的证据身份；
- 对正文 `[E-C11-001]—[E-C11-025]` 做双向闭合：账本无缺失，正文无孤儿引用；
- 解析全部 YAML，解析 15 个本地路径并逐一确认存在；
- 对 26 个外链执行重定向后的 HTTP 可达性检查；
- 读取 MCP 固定版本的 changelog、architecture、tools、authorization 与 security 页面，核对无状态协议、工具 annotation、显式 state handle、OAuth 与安全风险描述；
- 读取 OpenClaw 固定提交文档，核对工具策略、MCP、Browser、Approval、Sandbox、Secrets 的边界；
- 将 Hermes release 事实与动态官网分栏，不用动态页证明固定 release；
- 将 Muse Secure VM、Sentinel、privsep 与 credential surrogation 严格保留为 `VENDOR-CLAIM`；
- 检查作者本地结果文件和脚本存在，但不把作者自报当独立复现。

链接可访问只证明本轮能取得来源，不证明页面永久稳定，也不替代对目标环境的测试。

## 3. 25 条 claim 逐项裁决

| ID | 身份 | 结论 | 独立核查摘要 |
| --- | --- | --- | --- |
| E-C11-001 | METHODOLOGY | PASS | Tool 与 Resource/Knowledge/Skill/Workflow/Plugin/Agent 的分界与 v2、术语表、章节卡一致。 |
| E-C11-002 | METHODOLOGY | PASS | “明确、有界、可预测、可验证、可恢复、可审计”是本书接口质量合同，没有冒充外部标准。 |
| E-C11-003 | METHODOLOGY | PASS | 存在、发现、模型可见、请求、获准、协议结果、目标达成分层与 C06/C09 终态接口一致。 |
| E-C11-004 | STANDARD-FACT + boundary | PASS | MCP schema/description/annotation 是协议能力描述；正文正确声明业务授权由部署系统承担。 |
| E-C11-005 | OFFICIAL-GUIDANCE | PASS | MCP 明确要求不受信 Server 的 annotations 不可信；OWASP 一手指南支持结果污染和间接注入边界。 |
| E-C11-006 | METHODOLOGY | PASS | Policy、业务授权、Approval、Sandbox 分别回答资格、业务权利、逐次确认和运行隔离，未被合并成一个开关。 |
| E-C11-007 | METHODOLOGY | PASS | timeout/cancel 不证明外部副作用不存在；先读回、再决定补偿或升级，符合 D21 三层完成性。 |
| E-C11-008 | METHODOLOGY | PASS | 业务幂等键、Server 持久去重和环境查询被分开；没有把协议 request ID 夸大为业务幂等。 |
| E-C11-009 | STANDARD-FACT | PASS | 固定规范支持 Host—Client—Server 与 Tools/Resources/Prompts 等不同能力面。 |
| E-C11-010 | STANDARD-FACT | PASS | 固定 changelog 与 architecture 明确无状态核心、移除旧 handshake 与 `Mcp-Session-Id`、每请求携带版本与 capabilities。 |
| E-C11-011 | STANDARD-FACT | PASS | state handle 被写成显式应用状态引用，并要求每次调用重新授权；没有默认当 bearer capability。 |
| E-C11-012 | STANDARD-FACT | PASS | HTTP authorization 的可选性、issuer/audience 与 stdio 凭证边界均有固定规范/安全文档支撑；业务审批仍正确留给部署侧。 |
| E-C11-013 | STANDARD-FACT | PASS | confused deputy、token passthrough、SSRF、危险 authorization URL、本地 Server compromise 与 handle hijacking 均出现在 MCP 官方安全材料。 |
| E-C11-014 | METHODOLOGY | PASS | 模型只见 credential reference、执行边界按 target/scope/audience 注入，是带 OpenClaw/OWASP 支撑的书中工程规则。 |
| E-C11-015 | METHODOLOGY | PASS | 工具结果的来源、taint、分类、最小化、Memory 非自动晋升与 C09/C10 正式接口一致。 |
| E-C11-016 | VERSION-FACT | PASS | OpenClaw 固定提交文档支持 Tool/Skill/Plugin 分面与 schema 暴露前的 profile/policy/provider/sandbox/channel/plugin availability 过滤。 |
| E-C11-017 | VERSION-FACT | PASS | 固定 MCP 与权限文档支持 Server 接入仍受工具策略；正文没有把“已连接”写成绕过 Policy。 |
| E-C11-018 | VERSION-FACT | PASS | Browser profile、exec Approval、Sandbox mode/scope/backend 与 Secrets runtime 均按固定提交分面陈述。 |
| E-C11-019 | DYNAMIC-OFFICIAL | PASS WITH LIMITATION | `v0.20.1 / v2026.8.13` 只作为 release 锚点；MCP/Security/Code Execution 具体行为明确标 2026-09-30 动态页，未倒推固定 release。 |
| E-C11-020 | VENDOR-CLAIM | PASS WITH LIMITATION | Meta 官方材料确实描述 Secure VM、browser/connectors、Sentinel、privsep 和 credential surrogation；正文未声称 Muse 使用 MCP 或已被独立证明安全。 |
| E-C11-021 | OFFICIAL-GUIDANCE | PASS | publisher、version/digest、schema、权限、host/network/credential、漏洞、owner、替代撤权形成合理供应链清单，且把完整 Skill/Plugin 生命周期交回 C12。 |
| E-C11-022 | METHODOLOGY | PASS | protocol receipt、Artifact、environment outcome 分离与 C09/D21 一致；`isError=false` 不被当成业务成功。 |
| E-C11-023 | METHODOLOGY | PASS | 安全关键失败非补偿与全书 P0-13 一致；没有用成本或平均分覆盖。 |
| E-C11-024 | METHODOLOGY | PASS WITH DEPENDENCY | C11 只输出工具攻击面和观测字段，C19/C20 仍拥有威胁模型与 SLI/SLO；二者正文章冻结后需回归。 |
| E-C11-025 | LOCAL-VALIDATION | PASS AS AUTHOR RECORD | 作者保存结果确为 18 trial、12 PASS、4 FAIL、2 REVIEW_REQUIRED；本轮未复跑，因此只核对记录存在与声明边界。 |

## 4. 来源闭合

| 项目 | 结果 |
| --- | ---: |
| claim | 25 / 25 唯一 |
| 正文 evidence 引用 | 25 / 25 闭合 |
| 未被正文引用的 ledger claim | 0 |
| 正文孤儿 evidence ID | 0 |
| source | 41 |
| 被 claim 使用的 source | 41 / 41 |
| 本地 source 路径 | 15 / 15 存在 |
| 外部 source | 26 / 26 HTTP 200 |

初查发现 `BOOK-V2`、`C09-TASK` 和 `D18` 三个 source 未被任何 claim 使用。独立编辑修补为：`BOOK-V2` 加入 E-C11-001，`C09-TASK` 加入 E-C11-003；`D18` 只说明产物拆分而不直接支撑现有事实 claim，因此从 ledger source 列表移除。修补后无孤儿 source，未改变正文事实或运行结果。

## 5. 固定、动态与厂商证据边界

### MCP

本章使用 `2026-07-28` 固定规范，不用 SDK 默认对象替代 wire protocol。无状态核心、移除 handshake/session header、显式 handle、每请求版本/capabilities、annotation 不可信、OAuth 与安全攻击面的表述均能在该版本官方材料找到。规范的 MUST/SHOULD/MAY 与本书方法论仍保持分离。

### OpenClaw

平台事实锁定 `v2026.9.6 / eb377ac59e6c9fd6c7705028034812becf00271b`；除 release 外，Tools、MCP、Browser、Approval、Permissions、Sandbox 和 Secrets 证据都直接指向固定 commit。文中也明确“机制存在不证明实际配置和目标环境安全”。

### Hermes

release 只证明 `v0.20.1 / v2026.8.13` 锚点存在。动态官网支持 stdio/remote MCP、配置、安全和代码执行的当前说明，但不能证明 `f80f453…` 固定源码逐项一致。该限制在章首、正文、账本和开放项中均保留。

### Muse

Meta 官方材料支持 Secure VM、browser、connectors、Sentinel、privsep、credential surrogation 和人工确认等公开描述，但均是厂商自述。本章正确禁止推断 MCP、内部 schema、幂等/补偿或独立安全效果。

## 6. 开放事实缺口

1. OpenClaw 目标部署的实际 MCP Server、tool profile、Approval、Sandbox、Browser 与 Secrets 配置未实机探测；
2. Hermes 动态行为未逐项固定到 `v0.20.1` 源码；
3. Muse 内部实现不可由公开材料核验；
4. 真实 Provider 的 receipt、幂等、取消、补偿、日志和保留未逐供应商验证；
5. MCP/OWASP 页面未来可能变化，印前需重验动态安全指导；
6. 作者离线夹具尚待非作者复跑。

以上缺口均已被正文或账本标为 `REVIEW_REQUIRED`，没有暗中提升为 PASS。

## 7. 事实门

```yaml
fact_gate:
  chapter_id: "C11"
  claims_closed: "25/25"
  sources_used: "41/41"
  local_sources_exist: "15/15"
  external_links_http_200: "26/26"
  mcp_fixed_spec_boundary: "PASS"
  openclaw_fixed_version_boundary: "PASS"
  hermes_fixed_dynamic_split: "PASS_WITH_LIMITATION"
  muse_vendor_claim_boundary: "PASS_WITH_LIMITATION"
  author_local_run_identity: "VERIFIED_AS_AUTHOR_RECORD_ONLY"
  overall: "PASSED_WITH_LIMITATIONS"
  chapter_status_after_review: "drafting"
  release_candidate_authorized: false
```

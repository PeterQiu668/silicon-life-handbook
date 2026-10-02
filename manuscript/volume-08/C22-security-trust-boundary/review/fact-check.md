---
review_id: C19-independent-fact-check-20260930
chapter_id: C19
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

# C19 独立事实核查

## 裁决

**事实门：`REVIEW_REQUIRED`。** 35/35 条 claim 均有 ledger 条目并在正文出现，missing=0、orphan=0；10/10 个外部来源最终可达。OpenClaw 固定 `v2026.9.6 / eb377ac…`、Hermes 固定 `0.20.1 / f80f453…` 与动态文档、Muse `VENDOR-CLAIM`、OWASP 官方指导、NIST concept paper、MCP 版本化安全指导的身份分层正确。正文也没有把平台文档或标准写成产品认证。

事实门被一项中央术语冲突阻断：正文、A-C19-01、X-C19-01 与 Definition of Done 称“八层”，实际列出第 0—8 层，即九层；同章另有“九层同源字符串检查”“九个组件”的表述，E-C19-005 也明确列出九个项目。这不是排版小错，而是 C19 主定义权下的纵深防御模型自相矛盾，后章无法稳定引用。修复前不得冻结该模型。

本记录不修改正文、ledger、母产物、练习或作者运行包；运行控制有效性由 [交叉审校](cross-review.md) 单独裁决，不批准实践、编辑、总编或 `release_candidate`。

## 1. 证据闭合与来源身份

- source 共 25 个：本地/本书输入 15 个，外部来源 10 个；24/25 被 claim 消费，未使用项为 `TERMS`。
- evidence ID 共 35 个且全部唯一；正文引用 35/35，缺失引用 0，孤儿引用 0。
- 10/10 外部 URL 最终返回 HTTP 200；固定 GitHub blob 均含完整 commit，而不是可漂移分支。
- OpenClaw annotated tag `v2026.9.6` 解引用到 `eb377ac59e6c9fd6c7705028034812becf00271b`。固定文档支持“一 Gateway 一信任边界”、模型可被操纵、sandbox 的 mode/scope/backend 独立、进程内 Plugin 按可信代码治理、SecretRef 不是进程隔离。
- Hermes annotated tag `v2026.8.13` 解引用到 `f80f453ae0679347e38abc917c7f94f717bf96c5`，包版本 0.20.1。固定 SECURITY 明确 single-tenant personal agent 与 adversarial LLM 的 OS-level boundary；动态安全页没有倒填固定版。
- Muse 全部只作 Meta 厂商镜面，未写成独立效果证明。
- OWASP 被标为官方风险指导；NIST 页面被准确标为 concept paper；MCP 只支持协议相关 confused deputy、SSRF、token passthrough 等边界。三者均未被写成“符合即安全”。

## 2. 35 条 claim 逐项裁决

| Evidence | 裁决 | 核查摘要 |
| --- | --- | --- |
| E-C19-001 | PASS | OpenClaw 固定 trust model 明确 model last、assume manipulable；正文把边界放在系统控制。 |
| E-C19-002 | PASS AS METHODOLOGY | OWASP 风险面与 preflight 支持把网页、工具、Memory、Skill、Plugin、Card、Handoff 当不可信输入。 |
| E-C19-003 | PASS | 正文没有宣称靠提示词根治注入，且强调确定性强制层。 |
| E-C19-004 | PASS | 资产、主体、客体、攻击者与边界是合法威胁建模方法；未冒充 NIST 强制字段。 |
| E-C19-005 | REVIEW_REQUIRED | claim 实际列九层；正文、产物、练习和 DoD 多处称八层，同时又写“九层/九个组件”。主模型计数冲突。 |
| E-C19-006 | PASS | C05 契约和 OpenClaw trust model 均不授予权限；正文边界正确。 |
| E-C19-007 | PASS | 身份、会话、租户与授权被明确分开，没有把 session id 当 token。 |
| E-C19-008 | PASS WITH UPSTREAM LIMITATION | “委托只能衰减、每跳复核”与 C14/C17 方法一致；上游仍按受限接口消费。 |
| E-C19-009 | PASS WITH PROCESS-BOUNDARY LIMITATION | OpenClaw SecretRef 可减少持久化和模型链路暴露；固定文档也明确它不是进程隔离，正文有相同限制。凭证代理部分来自方法论。 |
| E-C19-010 | PASS AS METHODOLOGY | scope、audience、对象/动作、TTL、撤销是合理令牌治理要求；未写成单一产品原生字段。 |
| E-C19-011 | PASS AS METHODOLOGY | MCP 支持 SSRF 风险；DNS/IP/redirect/DLP 是工程扩展，正文身份清楚。 |
| E-C19-012 | PASS | 固定 OpenClaw 文档原生区分 sandbox mode、scope、backend，并列出枚举。 |
| E-C19-013 | PASS | OpenClaw/Hermes 固定文档均支持沙箱、网络、挂载、秘密和进程内扩展不能互相替代。 |
| E-C19-014 | PASS AS METHODOLOGY | 最小权限、职责分离、JIT、双人复核、elevated 被正确写成不同控制。 |
| E-C19-015 | PASS AS METHODOLOGY | 与 C14 绑定合同及固定 OpenClaw approval context 相符；没有把审批扩大成隔离。 |
| E-C19-016 | PASS | MCP 版本化安全指导直接覆盖 confused deputy、SSRF、token passthrough。 |
| E-C19-017 | PASS | C11/C12 与 OWASP 支持 tool/schema/result、Skill、Plugin 供应链不默认可信。 |
| E-C19-018 | PASS | Hermes 固定 SECURITY 明确进程内 Plugin/启发式不构成 OS containment。 |
| E-C19-019 | PASS AS METHODOLOGY | 与 C14 一致：Memory 内容不能生成 authority evidence。 |
| E-C19-020 | PASS AS METHODOLOGY | 五类高风险动作的确定性硬门是本书治理裁决，未冒充外部标准。 |
| E-C19-021 | PASS | 质量标准和 D22 支持安全硬失败非补偿。 |
| E-C19-022 | PASS AS METHODOLOGY | 预防、检测、止损、取证、恢复、通报、再测、残余链完整。 |
| E-C19-023 | PASS | NIST 概念问题与 C14 责任边界支持人类保留目标、授权、例外和组织后果责任。 |
| E-C19-024 | PASS | OpenClaw 固定 trust model 明确 one trust boundary per gateway，敌对用户需分 Gateway/OS user/host。 |
| E-C19-025 | PASS | 固定 tool permissions 文档支持多层限制继续收紧，并明确 policy/tool visibility/sandbox 不等价。 |
| E-C19-026 | PASS | Hermes fixed/dynamic 分栏准确；固定 SECURITY 确认 OS-level isolation 边界和进程内启发式限制。 |
| E-C19-027 | PASS | Muse 全章均保留 `VENDOR-CLAIM`，没有独立效果外推。 |
| E-C19-028 | PASS | OWASP、NIST、MCP 的来源身份与证明上限均准确。 |
| E-C19-029 | PASS | 正文显式禁止“根治”“不可攻破”“绝对安全”。 |
| E-C19-030 | PASS WITH PROJECT-STATE LIMITATION | 受限消费并需回归仍为真；但 frontmatter 只做集合式说明，没有列 C14/C17/C18 当前各自门状态。 |
| E-C19-031 | PASS | 包中恰好三件母产物；其可用性由交叉门另审。 |
| E-C19-032 | PASS AS SAVED-RUN FACT | 保存结果确为 22 trial、1 PASS/19 FAIL/2 RR，双 fresh-temp 字节一致；不代表判定器完整。 |
| E-C19-033 | PASS AS SAVED-RUN FACT WITH CONTROL LIMITATION | 原运行确为离线且代码没有网络/外部写，输入声明真实层 0、安全横切；但 runner 不强制该边界，详见交叉门。 |
| E-C19-034 | PASS AS METHODOLOGY | audit 防篡改和被测主体不可覆写是明确方法要求；作者夹具没有真正实现 digest 链。 |
| E-C19-035 | PASS AS METHODOLOGY | 撤销传播范围与 C14/preflight 一致；本章运行包未证明传播闭合。 |

## 3. 平台与标准边界

| 对象 | 章节用法 | 裁决 |
| --- | --- | --- |
| OpenClaw fixed | `eb377ac…` trust/sandbox/policy/secrets | PASS |
| Hermes fixed | `f80f453…` SECURITY，仅支持固定信任模型 | PASS |
| Hermes dynamic | pairing/approval/write safety/container/credential filtering 候选 | PASS WITH DYNAMIC LIMITATION |
| Muse | runtime cell、privsep、authd、egress、Sentinel 厂商镜面 | PASS AS VENDOR-CLAIM |
| OWASP | Agentic 风险指导 | PASS；非认证 |
| NIST | 软件 Agent 身份与授权 concept paper | PASS；非定稿控制标准 |
| MCP | 2025-11-25 协议安全指导 | PASS；不覆盖整个 Agent 系统 |

## 4. 问题分级与最小关闭合同

### P0

事实门没有发现伪造固定提交、动态页倒填、Muse 独立效果外推或 35 条 claim 断链。运行控制的 P0 见交叉审校。

### P1

- **P1-F19-01｜“八层”与实际九层冲突。** 章节 0—8、E-C19-005、A-C19-01、X-C19-01、DoD 和 preflight 需选择同一稳定名称。最小修复是统一为“九层纵深防御（第 0—8 层）”，并同步所有产物、练习、自检、索引与接口；若坚持八层，则必须合并两层、重编号并解释定义差异。修补后应全包搜索 `八层|九层|0—8|九个组件`，确保语义唯一。

### P2

- **P2-F19-01｜未使用 source。** ledger 的 `TERMS` 没有被任何 claim 引用；若正文确实消费 sandbox/policy 术语定义，应绑定相应 claim，否则删除未使用项。
- **P2-F19-02｜上游状态精度。** E-C19-030 的保守结论为真，但后续修订宜分别登记 C14、C17、C18 的 fact/cross/practice 限制，避免“均未冻结”掩盖不同缺口。

## 5. 保留未知

- 未探测任何真实 OpenClaw/Hermes/Muse、Gateway、OS、sandbox backend、credential broker、egress、身份提供方或第三方 API。
- 没有一手证据证明任一平台对真实攻击有效；固定文档只证明官方设计/信任边界。
- C14/C17/C18 仍是受限上游；其门禁变化后必须对身份、委托、Handoff、Card/Artifact、撤销和完成语义回归。

## 6. 门禁结论

- 事实门：`REVIEW_REQUIRED`。
- 关闭条件：修复 P1-F19-01，重新跑 35/35 claim 双向闭合、固定链接、YAML/frontmatter 和两个 validator；P2 可记录后关闭。
- 实践门：`not_reviewed`。
- 编辑门、总编门、RC：`not_reviewed / not_authorized`。

复现与 source 身份记录见 [fact-cross-reproduction-20260930.yaml](fact-cross-reproduction-20260930.yaml)。

---
review_id: ER-C06-001
chapter_id: C06
review_type: evidence-and-version
status: passed_with_limitations
reviewed_on: "2026-09-30"
closure_reviewed_on: "2026-09-30"
closure_round: 2
evidence_gate: pass
evidence_gate_closed_on: "2026-09-30"
reviewer: platform-and-frontier-evidence-reviewer
chapter_status_after_review: drafting
self_approval: false
practice_review_completed: false
final_editorial_approval: false
---

# C06 证据与版本独立审稿单

## 1. 审校结论

**本轮结论：`REVIEW_REQUIRED`，无开放内容级 P0，但有 4 项 P1 需由作者修正后再关闭事实门。章节继续保持 `drafting`。**

31 条账本主张均有正文引用，正文引用集合与账本集合完全一致，无缺失、孤儿或越号。OpenClaw 的 28 份固定提交文档均可从 `eb377ac59e6c9fd6c7705028034812becf00271b` 解引用，Gateway 协议、Agent Loop、Provider failover、等待超时、database-first 状态、Queue/steer、消息交付、Pairing/Binding、Plugin 信任、Browser/Node/Worker/MCP、Exec Approval、Sandbox、SecretRef、Security Audit 与 Recovery 的核心内容得到一手来源支持。Muse 只被用作 Meta 对自身产品的公开说明，未被外推成独立验证的安全效果或跨平台标准。

本轮发现一项可以消除的 Hermes 不确定性：`v2026.8.13` 是 annotated tag，其目标提交为 `f80f453ae0679347e38abc917c7f94f717bf96c5`；本章引用的 `architecture.md` 与 `provider-runtime.md` 均存在于该提交，且内容支持多入口进入 `AIAgent`、共享 Provider resolver 与 fallback chain。因此 E-C06-020/021 不必继续停留在动态文档身份。作者应把这两项及正文相关表述锁到该提交；但“文档存在于 tag”仍不等于本审校完成真实 Runtime 故障演练。

另外三项 P1 是事实表达纯度问题：OpenClaw 没有名为 `required` 的 `agents.defaults.sandbox.mode`，正文应写成“创建者角色的 `sandbox: required` 要求”；E-C06-029 把固定版 audit 功能与“无 finding 不等于安全”这一稳定原则混在一个 `VERSION-FACT` 中；正文变更记录声称账本含 `INFERENCE`，但账本并未定义或使用该类别。三项都不改变本章架构主结论，但在修正前不应将事实门标为 `PASS`。

## 2. 范围与方法

本轮只审事实、版本、来源和引用闭合，不代替实践门、交叉门、安全红队门或总编门，也未改动作者正文、账本、产物或练习。

- 解析 `evidence-ledger.yaml`，核对 31 个唯一证据 ID、来源集合、事实类别、作用域和限制；
- 扫描 C06 正文对 `E-C06-001`—`E-C06-031` 的引用，核对是否借同一 ID 承载超出账本的事实；
- 对 OpenClaw 全部 GitHub blob URL 改用同一完整 SHA 的 raw 内容复核，不用 `main` 回填版本事实；
- 通过 GitHub tag/ref/object/commit 一手接口核验 Hermes release tag 与提交关系，并直接读取该提交内两份文档；
- 读取 Meta Newsroom 与 Meta AI Research 页面，只判断 Meta 公开声称了什么，不判断其内部实现或安全效果真实程度；
- 对照 v2、章节卡、质量标准、术语表与 C06 preflight，检查方法论、版本事实、厂商声明和工程推断是否混用；
- 运行 YAML、引用集合、相对链接、全书结构和正式书稿校验。

## 3. 31 条证据逐条裁决

| ID | 核验焦点 | 一手证据与边界 | 裁决 |
|---|---|---|---|
| E-C06-001 | 六层观察模型 | v2、章节卡和 preflight 明确为本书方法；正文也拒绝冒充平台共同标准 | `PASS / METHODOLOGY` |
| E-C06-002 | Gateway typed WS、客户端/Node、事件、Agent 接纳 | `OC-ARCH` 固定提交明确 WS、`req/res/event`、typed API、Node role、`agent` accepted/final；正文幂等键说明也有同页直接支持 | `PASS` |
| E-C06-003 | Agent Loop | `OC-LOOP` 明确 intake、context assembly、model inference、tool execution、streaming、persistence | `PASS` |
| E-C06-004 | 同模型恢复、profile rotation、model fallback、turn-local | `OC-FAILOVER` 固定版依次写明 bounded same-model recovery、profile rotation、fallback，并明确 winning fallback 不改变 session selected model | `PASS` |
| E-C06-005 | `agent.wait` timeout 不等于停止 | `OC-LOOP` 直接写明 timeout 只返回 wait 状态、不取消 run，可对同一 runId 再等；运行 timeout 才 abort | `PASS` |
| E-C06-006 | Context 是装配结果 | `OC-LOOP` 与 `OC-WORKSPACE` 支持 bootstrap、session transcript、skills、tool results 等进入当次上下文；未把 Context 等同持久载体 | `PASS` |
| E-C06-007 | `TOOLS.md`、`HEARTBEAT.md` 退役 | 两个固定模板直接标 `retired`；HEARTBEAT 模板明确新 Workspace 不创建、Runtime 不读取 | `PASS` |
| E-C06-008 | database-first 与 Workspace 分离 | `OC-STATE` 明确一份全局 SQLite、每 Agent 一份 SQLite；`OC-WORKSPACE` 列出数据库不在 Workspace；旧 sidecar 不是活跃状态 | `PASS` |
| E-C06-009 | Workspace 不是硬 Sandbox | `OC-WORKSPACE` 直接说明 default cwd、非 hard sandbox，绝对路径在未启用 sandbox 时仍可越出；与 `OC-SANDBOX` 互证 | `PASS` |
| E-C06-010 | Gateway-owned Session 与 session key | `OC-SESSION` 明确会话由 Gateway 持有、入口和 scope 影响 key；正文没有把 Session 当授权 | `PASS` |
| E-C06-011 | Memory/Session/Context 分离 | `OC-MEMORY`、`OC-WORKSPACE` 支持 Workspace memory、memory plugin/index、按需检索与上下文注入差异 | `PASS` |
| E-C06-012 | Session 串行与 lane 约束 | `OC-QUEUE` 明确 session-key lane 串行，再进入 global lane；容量与默认值未被固化为跨版本原则 | `PASS` |
| E-C06-013 | steer 与 interrupt 不同 | `OC-QUEUE`、`OC-STEER` 明确 steer 不停止已经运行的 Tool，interrupt 才 abort；steer 不改变 Tool policy | `PASS` |
| E-C06-014 | 生成、run、delivery queue、receipt 分态 | `OC-MESSAGES`、`OC-RETRY`、`OC-RECOVERY` 支持 durable admission、独立 delivery attempt budget、pending/confirmed receipt 与恢复差异；模型恢复与 Channel delivery retry 分开 | `PASS` |
| E-C06-015 | Pairing 准入、Binding 选 Agent | `OC-PAIRING` 明确 DM/Node 准入；`OC-BINDING` 直接写明 bindings only pick the agent，不创建 account、不授予 access | `PASS` |
| E-C06-016 | 多认证面与单 Gateway 信任域 | `OC-TRUST` 明确 one trust boundary per gateway、非敌对多租户隔离；`OC-ARCH/PAIRING` 支持设备、Channel、Node 等身份面分离 | `PASS` |
| E-C06-017 | Tool 权限收敛、Plugin in-process trusted code | `OC-PERM` 直接写明 Plugin 在 Gateway 进程内运行并应视为 trusted code；Tool profile/allow/deny/sandbox/host policy 分层有固定版支持 | `PASS` |
| E-C06-018 | Gateway events 非持久账本 | `OC-ARCH` 直接写明 events are not replayed、gap 后 refresh；正文没有把最后事件当完整历史 | `PASS` |
| E-C06-019 | durable recovery 与 PTY 不恢复 | `OC-RECOVERY` 的生存表直接列 per-agent/global SQLite 状态可恢复，Gateway terminal PTY 仅在 process memory、不会恢复 | `PASS` |
| E-C06-020 | Hermes 多入口进入 AIAgent | `v2026.8.13` 解引用到 `f80f453ae067...`；该提交 `website/docs/developer-guide/architecture.md` 明列 CLI/Gateway/ACP/Batch/API/Python Library 与共享 `AIAgent` | `PASS AFTER SOURCE RECLASSIFICATION` |
| E-C06-021 | Hermes shared resolver 与 fallback chain | 同一固定提交的 `provider-runtime.md` 明列共享 resolver、provider profile、fallback provider chain、触发和不支持边界 | `PASS AFTER SOURCE RECLASSIFICATION` |
| E-C06-022 | Browser 执行位置与 profile 边界 | `OC-BROWSER` 区分 dedicated profile、真实已登录 `user` profile、Node/remote/hosted CDP；正文只要求探测实际位置 | `PASS` |
| E-C06-023 | Node 是外围执行端，不是 Gateway | `OC-NODE` 直接写明 node connects to Gateway、nodes are peripherals not gateways；`OC-PERM/APPROVAL` 支持 pairing 不等于逐命令审批 | `PASS` |
| E-C06-024 | Cloud Worker 可回收、Gateway 拥有 Session/Transcript | `OC-WORKER` 直接写明 throwaway machine、session visible and transcript owned by Gateway、machine discarded after work | `PASS` |
| E-C06-025 | MCP 配置不等于健康，仍受 Tool policy | `OC-MCP` 直接写明 saving definition proves nothing about reachability，应 probe；MCP tools 使用同一 tool-profile/tool-policy | `PASS` |
| E-C06-026 | Exec Approval 在执行主机生效 | `OC-APPROVAL` 直接写明 locally on execution host，区分 Gateway host 与 Node host；approval 只能收紧 config-derived policy | `PASS` |
| E-C06-027 | Sandbox mode/scope/backend/workspace access 与 fail closed | 主要事实受 `OC-SANDBOX` 支持；但产品 mode 枚举只有 `off/non-main/all`，`required` 是 creator role/session 要求，不是第四个 mode | `PARTIAL — WORDING FIX REQUIRED` |
| E-C06-028 | SecretRef snapshot/sentinel/残留 | `OC-SECRETS` 支持激活时内存快照、egress sentinel、未知 sentinel fail closed，并明确非进程隔离、不会清理旧明文/备份 | `PASS` |
| E-C06-029 | Security audit、`--deep`、`--fix` | `OC-AUDIT` 支持扫描面、live probe 与窄修复；“无 finding 不构成安全证明”是合理稳定原则，但不是该产品页的版本字段 | `PARTIAL — CLASS SPLIT REQUIRED` |
| E-C06-030 | 最小可训单体定义 | 明确标本书方法，来源为 v2/章节卡/preflight/质量标准，并保留需实践门试跑的限制 | `PASS / METHODOLOGY` |
| E-C06-031 | Muse Secure VM/runtime cell/Sentinel/credential surrogate/Browser 与限制 | Meta 两个官方页面确有这些公开说明，也承认 Agent 会犯错、会受读取数据攻击，并将 Confidential VM 写为后续能力；无独立验证 | `PASS AS VENDOR-CLAIM` |

汇总：27 项可直接维持；2 项事实成立但应从动态来源升级为 Hermes 固定提交事实；1 项 Sandbox 术语需收窄；1 项需拆分产品版本事实与稳定原则。没有发现伪造 URL、把 Muse 厂商声明当独立证明、或把 OpenClaw 事实外推为跨平台标准。

## 4. 必须由作者修正的 P1

### P1-01：Hermes 已可固定到 release commit

当前账本 `HE-ARCH`、`HE-PROVIDER` 使用动态官网，E-C06-020/021 标为 `DYNAMIC-OFFICIAL`；正文 6.2.1、三平台矩阵、平台边界段和“仍未通过验证”段反复说尚未固定到 `f80f453`。这在本轮核验后已过时。

作者应同步修改：

1. frontmatter 增加 Hermes commit `f80f453ae0679347e38abc917c7f94f717bf96c5`；
2. `HE-ARCH` 改为 `https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/developer-guide/architecture.md`；
3. `HE-PROVIDER` 改为同提交的 `website/docs/developer-guide/provider-runtime.md`；
4. E-C06-020/021 改为 `VERSION-FACT / official-doc-fixed-release-commit`；
5. 关闭或重写 U-C06-01：上述两条文档事实已固定，真实运行与恢复效果仍交实践门；
6. 正文不得继续声称这两页“只能作为 2026-09-30 动态页面”，同时仍要保留“不与 OpenClaw 同构、未实跑”的限制。

### P1-02：`required` 不是 `agents.defaults.sandbox.mode`

账本 E-C06-027 和正文 6.7.4 使用“required 模式”容易让读者误以为 mode 枚举为 `off/non-main/all/required`。固定版文档实际区分：

- `agents.defaults.sandbox.mode`: `off | non-main | all`；
- `agents.defaults.sandbox.scope`: `agent | session | shared`；
- 创建者角色的 sandbox policy 可为 `required`，该要求使 backend failure fail closed；
- 委派接口还可有 `sandbox: require`，但不是同一个配置字段。

建议只改措辞，不改方法：把“required 模式”改为“创建者角色的 `sandbox: required` 强制要求（或相应接口的 require 语义）”。

### P1-03：E-C06-029 混合事实身份

“`security audit`、`--deep`、`--fix` 的行为”是 `VERSION-FACT`；“无 finding 不构成安全证明”是 `STABLE-PRINCIPLE / INFERENCE`。建议保留同一 ID 时在 claim 中显式分句标两种身份，或拆成相邻证据项并更新正文引用。不能因为工程原则正确，就把它伪装成厂商文档原句。

### P1-04：正文声称存在未登记的 `INFERENCE` 类别

正文变更记录写“账本区分……`INFERENCE`”，但账本 `evidence_classes` 没有 `INFERENCE`，31 条 claim 也没有使用该 class。应删除这处枚举，或在全书事实身份合同允许时补齐定义并用于确有推断的主张。不要只在正文口头增加事实类别。

## 5. P0 十五项证据相关检查

| P0 | 本轮状态 | 证据审校说明 |
|---|---|---|
| P0-01 模板与目录 | `PASS` | C06 包、3 产物、2 练习、交接与 review 节点齐全；不代表内容门全部关闭 |
| P0-02 定义权 | `PASS` | 六层为本章方法，Memory/Tool/MCP/Automation/安全细节均让位后章 |
| P0-03 事实标签/来源/日期/作用域 | `REVIEW_REQUIRED` | OpenClaw/Muse 合格；Hermes 应由动态改为固定提交，E-C06-029 需拆事实身份 |
| P0-04 版本命令/字段 | `REVIEW_REQUIRED` | OpenClaw 全部固定到 eb377ac；Sandbox `required` 字段语义需精确；Hermes 可固定到 f80f453 |
| P0-05 可停止/可恢复 | `NOT ASSESSED BY EVIDENCE GATE` | 文字和产物有路径，但两项练习尚未独立运行 |
| P0-06 权限/审批/隔离 | `PASS IN DESIGN, PRACTICE PENDING` | 正文明确人格/Workspace/Binding 不替代 Policy/Approval/Sandbox；需实战门负例 |
| P0-07 练习基线/证据/验收 | `NOT ASSESSED BY EVIDENCE GATE` | 练习结构存在，尚无运行记录 |
| P0-08 仿生边界 | `PASS` | 仿生段明确不是生物意识、神经同构或法律人格主张 |
| P0-09 三平台边界 | `PASS WITH REQUIRED UPDATE` | OpenClaw 固定、Muse 厂商声明；Hermes 更新为固定 release commit 后边界更强，不得写成同构 |
| P0-10 案例/隐私/版权 | `PASS` | 开场与 CASE-A/B/C 明标教学复合案例，未伪装生产客户效果 |
| P0-11 Agent 机器块 | `PASS` | fenced YAML 可解析，包含前置、停止、回滚与三态验收，不授予真实高风险权限 |
| P0-12 冲突/占位/缺口 | `PASS WITH DISCLOSURE` | 未运行项和平台限制被明示；4 项 P1 未修前不得升级章节状态 |
| P0-13 安全硬失败 | `PASS IN TEXT` | deny/unknown/越权/位置漂移不能由成功输出抵消；实战门仍待执行 |
| P0-14 产物可定位 | `PASS` | 3 件产物和 2 练习链接存在；下章消费效果不属本轮事实门 |
| P0-15 领先主张 | `PASS` | 未发现“行业最强、绝对安全、唯一架构”等无对照结论 |

## 6. 平台边界终审

| 平台 | 可确认 | 必须保留的限制 | 裁决 |
|---|---|---|---|
| OpenClaw | `v2026.9.6 / eb377ac` 的文档事实；28 个固定 blob 均存在且与相关主张一致 | 不能外推后续版本；目标环境支持、实际配置和故障恢复仍需探测 | `PASS` |
| Hermes | `v2026.8.13` annotated tag 指向 `f80f453ae067...`；两份相关文档在该提交存在 | 只支持文档明确的多入口、resolver/fallback；不证明与 OpenClaw 协议、状态、队列、恢复同构，也不替代实跑 | `PASS AFTER RECLASSIFICATION` |
| Muse | Meta 公开说明 Secure VM、runtime cell、Sentinel、凭证代理、Browser 与限制 | 所有效果和内部机制仍是 `VENDOR-CLAIM`；Confidential VM 不得写成核验日普遍上线 | `PASS AS VENDOR-CLAIM` |

## 7. 复核过的一手来源

核验日均为 2026-09-30。“一手”只表示标准维护方、项目或厂商对自身产品的原始发布，不等于独立效果验证。

### 7.1 OpenClaw 固定提交

- release：`https://github.com/openclaw/openclaw/releases/tag/v2026.9.6`；
- commit：`eb377ac59e6c9fd6c7705028034812becf00271b`；
- 已读取并语义复核的固定文档 ID：`OC-ARCH`、`OC-LOOP`、`OC-FAILOVER`、`OC-WORKSPACE`、`OC-SESSION`、`OC-MEMORY`、`OC-QUEUE`、`OC-STEER`、`OC-MESSAGES`、`OC-BINDING`、`OC-PAIRING`、`OC-RETRY`、`OC-TOOLS`、`OC-BROWSER`、`OC-NODE`、`OC-WORKER`、`OC-MCP`、`OC-NODE-MCP`、`OC-TRUST`、`OC-PERM`、`OC-APPROVAL`、`OC-SANDBOX`、`OC-SECRETS`、`OC-AUDIT`、`OC-RECOVERY`、`OC-STATE`、`OC-TOOLS-RET`、`OC-HB-RET`；
- 上述 28 个 blob 在完整 SHA 下均返回内容；没有使用 `main` 支撑 OpenClaw 版本事实。

### 7.2 Hermes 固定 release

- release：`https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.13`；
- Git tag object：`4e693dc685b5716e7da22656eccc6ece37c5db72`；
- tag target commit：`f80f453ae0679347e38abc917c7f94f717bf96c5`；
- Architecture：`https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/developer-guide/architecture.md`；
- Provider Runtime：`https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/developer-guide/provider-runtime.md`。

### 7.3 Meta Muse

- Meta Newsroom：`https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/`；
- Meta AI Research：`https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse`；
- 仅支持 Meta 对 Secure VM、Sentinel、凭证、Browser、runtime cell、Prompt Injection 风险和后续 Confidential VM 的公开说明。

## 8. 禁止升级的表述

在 P1 修正和实践门完成前，不得写：

- “Hermes 当前动态官网证明 v0.20.1 的所有 Gateway、恢复和 Provider 行为”；
- “OpenClaw 有 `required` 这一第四种 `agents.defaults.sandbox.mode`”；
- “`security audit` 零 finding 证明系统安全”；
- “exec approval 是敌对租户隔离”或“批准可以放宽上游 deny”；
- “Pairing、Binding 或 Session 本身授予敏感动作权限”；
- “等待超时表示 run、Tool、Browser、Node 已停止”；
- “MCP 配置存在表示 Server 健康、Tool 已授权”；
- “Workspace 是 Sandbox”或“Plugin 默认位于 Agent Sandbox”；
- “SecretRef 使秘密不进入进程并自动清理旧残留”；
- “Muse 的安全架构已被独立证明有效”或“Confidential VM 已普遍上线”；
- “六层是三平台共同官方架构”或“OpenClaw、Hermes、Muse 同构”。

## 9. 复审触发器与关闭条件

事实门复审只需作者完成以下最小修改：

1. 锁定 Hermes tag target 与两份固定文档，更新 E-C06-020/021、source、scope note、正文平台段和 U-C06-01；
2. 把 `required 模式` 改为准确的 creator-role/session requirement 语义；
3. 拆清 E-C06-029 的版本事实与稳定原则；
4. 修正文末关于账本含 `INFERENCE` 的不实枚举；
5. 重新运行 YAML、证据集合、链接与全书校验。

若 OpenClaw commit、Hermes release/tag、Muse 页面或全书事实身份合同发生变化，应重新打开本审校。Cloud Worker、Node、MCP、停止、UNKNOWN 对账和恢复的真实效果仍必须由独立实践门关闭，不能由本审校代签。

## 10. 专项校验记录

- `evidence-ledger.yaml`：YAML 解析成功，31 个唯一 claim、39 个 source；
- 正文证据引用：31 个唯一 ID，与账本集合完全一致，缺失 0、孤儿 0；
- OpenClaw 固定文档：28 个完整 SHA raw URL 均成功读取；
- Hermes：annotated tag 已解引用至完整 commit，两份固定提交文档成功读取；
- Muse：两个 Meta 官方页面成功读取，只按 `VENDOR-CLAIM` 处理；
- C06 包内相对链接可定位；新增审稿单未修改正文、账本、产物或练习；
- `scripts/validate-book.py` 通过；`scripts/validate-formal-manuscript.py` 通过并仅保留“全书尚缺其他章节包”的既有 warning；
- 本记录不把章节标为 `done`、`release_candidate` 或事实门最终批准。

## 11. 2026-09-30 关闭复审附录

### 11.1 关闭结论

本轮按第 9 节的五项关闭条件重新读取 C06 frontmatter、正文、README 与完整账本，并复跑机器校验。**关闭结果仍为 `REVIEW_REQUIRED`：原 4 项 P1 中 3 项已关闭，P1-01 已完成账本与主要正文修正，但三平台矩阵仍残留同一事实身份冲突。**

本附录不推翻初审对 31 条主张实质内容的裁决；它只判断作者修订是否在所有消费位置一致落盘。事实门暂不 PASS 的原因不是新增证据缺口，而是同章对 Hermes 同一来源仍给出互相冲突的“固定提交 / 动态文档”身份。

### 11.2 四项 P1 关闭状态

| 原问题 | 复审观察 | 状态 |
|---|---|---|
| P1-01 Hermes 固定到 release commit | frontmatter 已登记完整 SHA；`HE-ARCH/HE-PROVIDER` 已改固定 blob；E-C06-020/021 已改 `VERSION-FACT`；U-C06-01 已转为实践问题；6.2.1、平台总结段和未验证限制均已正确更新 | `PARTIALLY CLOSED` |
| P1-02 `required` 不是 sandbox mode | 账本与 6.7.4 均改为 creator-role `sandbox: required` 强制要求，并明确不是 `agents.defaults.sandbox.mode` 第四枚举 | `CLOSED` |
| P1-03 E-C06-029 混合事实身份 | 账本 claim 只保留固定版 audit/`--deep`/`--fix` 行为；稳定治理原则进入 limitations，正文明确它不是厂商安全保证 | `CLOSED` |
| P1-04 未登记的 `INFERENCE` 枚举 | 章末账本说明已改为实际存在的 `METHODOLOGY`、固定版本事实、动态官方文档、稳定原则、`VENDOR-CLAIM`；失败模式中的“降级为 inference/unknown”是处置语言，不再冒充账本 class | `CLOSED` |

### 11.3 唯一阻断项：三平台矩阵仍沿用旧身份

正文三平台矩阵仍出现以下旧口径：

- “`v0.20.1` 只作 release 锚；动态文档列多入口与 Messaging Gateway”；
- “Hermes 动态实现不回填 release”；
- 认知执行、状态、行动、治理等 Hermes 单元仍统一写成“动态文档列/显示”。

同章 6.2.1、E-C06-020/021 和平台总结段已经确认 `v2026.8.13` tag 指向 `f80f453ae0679347e38abc917c7f94f717bf96c5`，且 `architecture.md`、`provider-runtime.md` 存在于该提交。因此矩阵至少应把由这两份文件直接支持的内容标为“固定提交文档事实”，并把“其他未锁定官网能力仍按动态文档处理”放入限制列。现有矩阵把已锁定内容重新降回动态来源，造成章节内部版本身份不一致，继续触发 P0-03/P0-04 的 `REVIEW_REQUIRED`。

最小关闭动作仅需修改该矩阵的 Hermes 来源身份，不需要改变架构结论、扩充证据或新增主张。修改后重新搜索正文中的 `动态文档`，逐项确认它只指向未固定的其他 Hermes 官网能力；随后复跑本附录第 11.5 节校验即可申请第二次关闭复审。

### 11.4 不阻断事实门、但继续保留的限制

- Hermes 固定提交文档只证明该 release 文档明确陈述的结构与 fallback 机制，不证明真实 Runtime 的恢复效果；
- OpenClaw Cloud Worker、Node、Browser、MCP、停止与 delivery receipt 在目标读者环境中的可用性仍需探测；
- X-C06-01、X-C06-02 尚未由独立实践者运行，`UNKNOWN` 对账、故障注入和回滚尚未获得实践证据；
- Muse 仍为 `VENDOR-CLAIM`，没有独立黑盒复现或安全效果证明；
- 六层架构与最小可训单体仍是本书方法论，不是三平台共同标准；
- 章节继续为 `drafting`，实践门、交叉门、总编门均未由本附录批准。

### 11.5 本轮机器校验

- C06 `evidence-ledger.yaml` 与全部 Markdown frontmatter/fenced YAML 可解析；
- 账本仍为 31 个唯一证据 ID，正文仍引用 31 个唯一证据 ID，集合一致；
- Hermes 两个固定 GitHub blob URL 含完整 `f80f453ae0679347e38abc917c7f94f717bf96c5`；
- C06 包内相对链接无缺失；
- `scripts/validate-book.py`：`PASS`；
- `scripts/validate-formal-manuscript.py`：`PASS`，只保留全书尚缺其他章节生产包的既有 warning；
- `git diff --check`：通过；
- 本轮只修改本审稿单 frontmatter并追加本附录，未改正文、账本、README、产物或练习。

## 12. 2026-09-30 第二次关闭复审附录

### 12.1 最终事实门结论

**C06 事实门：`PASS WITH LIMITATIONS`。** 第一次关闭复审的唯一阻断项已经消除：三平台矩阵现将 Hermes 多入口、Messaging Gateway、`AIAgent` 与共享 Provider resolver/fallback chain 明确标为 `v2026.8.13 / f80f453ae0679347e38abc917c7f94f717bf96c5` 固定提交文档事实；状态、消息、行动、治理等未纳入 E-C06-020/021 固定主张的能力继续保留动态文档身份。固定与动态边界不再互相冲突。

原 4 项 P1 至此全部关闭。31 条证据仍与正文引用一一闭合，OpenClaw 固定提交、Hermes 固定 release commit、Muse `VENDOR-CLAIM` 和本书方法论四类边界清楚。本次 `PASS` 只关闭证据与版本事实门，不改变章节 `drafting` 状态，也不构成实践、交叉、总编或出版批准。

### 12.2 继续由实践门负责的限制

- Hermes 文档事实尚未在真实 Runtime 中完成 Provider fallback、Gateway、停止与恢复故障演练；
- OpenClaw Cloud Worker、Node、Browser、MCP、Channel delivery 与 receipt 能力仍需在目标环境探测；
- X-C06-01、X-C06-02 尚未由独立实践者执行，`UNKNOWN` 对账、故障注入、清理和回滚仍无实践签字；
- Muse 仍只有 Meta 厂商声明，未获得独立黑盒复现或安全效果证明；
- 六层架构和最小可训单体是本书方法论，不是三平台共同官方标准。

### 12.3 第二次关闭校验

- C06 账本与全部 Markdown YAML 均可解析；
- 账本 31 个唯一证据 ID 与正文 31 个唯一引用集合一致；
- 三平台矩阵的两个固定 Hermes 内容与 E-C06-020/021 一致，其余能力明确保持动态限制；
- C06 相对链接无缺失；
- `scripts/validate-book.py` 与 `scripts/validate-formal-manuscript.py` 均通过，后者仅保留全书尚缺其他章节包的既有 warning；
- `git diff --check` 通过；
- 本轮只更新本审稿单，不修改正文、账本、README、产物或练习。

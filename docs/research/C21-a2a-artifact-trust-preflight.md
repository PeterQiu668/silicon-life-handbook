# C21《A2A、产物协议与信任系统》前置研究包

> 状态：`research_preflight`，不是正式章节，不签发事实门、实践门或总编门通过。  
> 核验截止：2026-09-30。  
> 固定实现基线：OpenClaw `v2026.9.6` / `eb377ac59e6c9fd6c7705028034812becf00271b`；Hermes Agent `0.20.1` / `v2026.8.13` / `f80f453ae0679347e38abc917c7f94f717bf96c5`。  
> 协议基线：A2A Protocol `1.0`；GitHub 补丁发布 `v1.0.1`。  
> 证据标签：`STABLE-PRINCIPLE`、`METHODOLOGY`、`OFFICIAL-SPEC`、`VERSION-FACT`、`OFFICIAL-DOC-DYNAMIC`、`VENDOR-CLAIM`、`INFERENCE`、`UNKNOWN`。  
> 统一验收语言：`PASS / FAIL / REVIEW_REQUIRED`；`UNKNOWN` 是事实或运行结果的不确定性，不是第四种门禁结论。
> 依赖状态：C17 正式作者包与事实/交叉门已完成，v3.1 状态化离线机器控制已独立复现，真实授权环境仍为 `REVIEW_REQUIRED`；C19 正式作者包及事实/交叉门已通过（有限制），实践门待审；C20 正式作者包已完成，独立事实/交叉/实践门待审。C21 可受限启动作者生产，但上述接口在对应门禁关闭前不得冻结。

---

## 0. 先行裁决

1. **Message、Task、Event 和 Artifact 是四种不同对象。** Message 承载意图、说明、补充输入或协商；Task 承载有身份的长时间工作及其状态；Event 是对已发生转移的带序通知；Artifact 是可版本化、可验收、可保留的交付对象。把四者压成“聊天记录”会丢失责任、终态与来源。`STABLE-PRINCIPLE`
2. **A2A 解决互操作语义，不替组织做信任决定。** Agent Card 可用于发现接口、能力和安全需求；即使签名验证通过，也只支持“这张卡来自指定签发者且内容未被替换”，不证明所声明的能力真实、当前可用、行为安全或已获任务授权。`OFFICIAL-SPEC + STABLE-PRINCIPLE`
3. **协议终态不等于业务终态。** `COMPLETED` 可以表示服务端已结束任务，但产物内容可能错误、越权、过期或未被下游接受。只有“协议状态 + 轨迹/权限验证 + 产物验收 + 环境终态对账”才能支持交付判定。`METHODOLOGY`
4. **信任必须被拆成可验证的构成，不使用一个神秘总分。** 最少分开身份保证、授权证据、能力实测、产物来源、运行可靠性、安全历史和当前上下文。任何安全硬失败不得被历史高分抵消。`METHODOLOGY`
5. **动态信任只能改变审查和限额，不能自动创造高风险权限。** 信任记录可以促使收紧权限、要求额外验证或停用；它不得让 Agent 因“功绩多”就跨过 C17 的授权链、C22 的职责分离或人类审批。`METHODOLOGY`
6. **产物签名只保护指定字节的完整性和来源断言，不保证内容正确。** “签名有效但结果错误”必须 `FAIL`，不得用密码学成功代替业务验收。`STABLE-PRINCIPLE`
7. **不承诺跨系统 exactly-once。** A2A 推送可能重复，Send Message 只在实现支持时可按 `messageId` 幂等去重。正式章应使用“稳定 ID + 去重 + receipt + reconciliation”。`OFFICIAL-SPEC`
8. **OpenClaw、Hermes 和 Muse 是三种证据镜面，不是三套平行真理。** OpenClaw 可做固定版 A2A 实现主镜；Hermes 只在有固定文档/源码时声明实现事实，未证明的 A2A 兼容性保留 `UNKNOWN`；Muse 只是可观察产品与厂商声明，不推断其内部协议。

---

## 1. 章节边界与定义权

### 1.1 本章必须完成

- 定义 Message、Task、Event、Artifact 的语义边界、标识与关联；
- 给出 Task 生命周期、状态转移、流式更新、取消、超时、推送和对账；
- 解释 Agent Card 的发现价值、签名边界、缓存/过期和能力实测；
- 定义产物信封、来源、所有者、版本、签名、验收、保留、更正和撤回；
- 建立信任记录的证据构成、上下文作用域、衰减、申诉和不可自授权边界；
- 运行至少一条模拟跨 Agent 任务，覆盖发现、协商、流式状态、取消、产物验收、重复事件与失败隔离。

### 1.2 本章不得越权

| 对象 | C21 消费 | 定义 owner |
|---|---|---|
| 路由、让位、Handoff、并发合并 | 引用决策和交接证据 | C20 |
| 任务/产物评测和 grader | 消费验收结果 | C07 |
| 授权链、自主范围、委托衰减和撤销 | 信任记录只引用 `authority_evidence_ref` | C17 |
| 组织模式和角色责任 | 记录 owner/acceptor/reviewer | C19 |
| 身份、密钥、凭证、威胁模型和纵深防御 | 本章仅定义信任需要什么证据 | C22 |
| 遥测管线、SLI/SLO、事件存储 | 本章定义应观测的协议事件 | C23 |

C21 可定义“什么信号可以进入信任记录”，但不能把信任记录变成新的授权发放器。

---

## 2. 一手证据账本

### 2.1 A2A Protocol 1.0

| ID | 身份 | 一手来源 | 支持的事实 | 不可外推 |
|---|---|---|---|---|
| R-C21-A2A-01 | `OFFICIAL-SPEC` | [A2A 1.0 Specification](https://a2a-protocol.org/latest/specification/) | 规范定义 Message、Task、TaskStatus、TaskState、Part、Artifact、AgentCard、流式事件和安全方案 | 不证明任意实现均完整兼容 |
| R-C21-A2A-02 | `VERSION-FACT` | [A2A v1.0.1 release](https://github.com/a2aproject/A2A/releases/tag/v1.0.1) | 2026-05-26 存在 1.0 协议线的补丁发布 | 协议协商不应把 patch 号当成新 `Major.Minor` |
| R-C21-A2A-03 | `OFFICIAL-SPEC` | [Messages and Artifacts](https://a2a-protocol.org/latest/specification/#37-messages-and-artifacts) | Message 用于对话/输入，Artifact 用于 Task 产出；关键交付不应只存在消息中 | Artifact 不自带业务质量保证 |
| R-C21-A2A-04 | `OFFICIAL-SPEC` | [Task and TaskState](https://a2a-protocol.org/latest/specification/#411-task) | Task 带有唯一 ID、context、status、history 与 artifacts；终态与非终态分离 | A2A 状态不等于本书全部业务状态 |
| R-C21-A2A-05 | `OFFICIAL-SPEC` | [Idempotency](https://a2a-protocol.org/latest/specification/#331-idempotency) | `GetTask` 幂等；`SendMessage` 可选使用 `messageId` 实现幂等；Cancel Task 幂等 | 不得声称所有消息 exactly-once |
| R-C21-A2A-06 | `OFFICIAL-SPEC` | [Task update delivery](https://a2a-protocol.org/latest/specification/#35-task-update-delivery-mechanisms) | 存在流式与推送更新机制；推送可能重复，接收者须幂等处理 | 事件到达不代表业务采纳 |
| R-C21-A2A-07 | `OFFICIAL-SPEC` | [Cancel Task](https://a2a-protocol.org/latest/specification/#315-cancel-task) | 取消是尝试，不保证成功；任务可能已终结或当前无法取消 | 请求或 ACK 不等于已停止 |
| R-C21-A2A-08 | `OFFICIAL-SPEC` | [AgentCard](https://a2a-protocol.org/latest/specification/#441-agentcard) | Card 声明 provider、interfaces、capabilities、skills、security schemes 与签名 | 自我声明不证明能力、授权或信任 |
| R-C21-A2A-09 | `OFFICIAL-SPEC` | [Authentication and Authorization](https://a2a-protocol.org/latest/specification/#7-authentication-and-authorization) | 身份验证与服务端授权责任分离；服务端应按本地策略决策 | 通过认证不自动有权调用某 skill 或访问某数据 |
| R-C21-A2A-10 | `OFFICIAL-SPEC` | [Agent Card signing](https://a2a-protocol.org/latest/specification/#84-agent-card-signing) | 规范定义卡片规范化、签名格式与验证 | 签名只支持来源/完整性断言，不保证声明真实 |

### 2.2 OpenClaw 固定版 `eb377ac`

| ID | 身份 | 一手来源 | 支持的事实 | 限制 |
|---|---|---|---|---|
| R-C21-OC-01 | `VERSION-FACT` | [OpenClaw v2026.9.6 release](https://github.com/openclaw/openclaw/releases/tag/v2026.9.6) | 冻结基线为 `eb377ac` | 不引用 main 当固定事实 |
| R-C21-OC-02 | `VERSION-FACT` | [A2A channel at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/channels/a2a.md) | 支持 A2A 1.0 JSON-RPC 发现与文本/结构化数据任务；每 peer + context 会话隔离；每 peer token；命令与审批不由 A2A peer 越过 | 不支持 streaming、push、cancel、list、extended card、multi-tenant routing；task 只在内存，重启丢失 |
| R-C21-OC-03 | `VERSION-FACT` | 同上 | `CancelTask` 因运行缺少插件级 abort seam 而明确拒绝，不伪报 `CANCELED` | “协议支持某操作”不等于特定实现必须假装支持 |
| R-C21-OC-04 | `VERSION-FACT` | [Session tools at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/session-tool.md) | 会话操作受可见性与工具策略约束；列表是活视图；机械成功不自动标为政策 enforced | session 消息/回执不是产物验收 |

### 2.3 Hermes 固定版与动态文档

| ID | 身份 | 一手来源 | 支持的事实 | 限制 |
|---|---|---|---|---|
| R-C21-HE-01 | `VERSION-FACT` | [Hermes v2026.8.13 release](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.13) | 固定提交 `f80f453` | 未出现于固定文档/源码的功能不归属 0.20.1 |
| R-C21-HE-02 | `VERSION-FACT` | [Delegation at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/user-guide/features/delegation.md) | 委托创建隔离子会话，只返回最终摘要，工具继承只能收紧，并发结果按 task index 排序 | 摘要不是 Artifact 来源链；不证明 A2A 1.0 完整兼容 |
| R-C21-HE-03 | `VERSION-FACT` | [Subagent lifecycle at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/developer-guide/subagent-lifecycle-api.md) | 生命周期显式区分 `CANCEL_REQUESTED/CANCELLED/UNKNOWN`；终态结果不可变且带稳定 hash | Hermes 状态不应被冒充成 A2A TaskState |
| R-C21-HE-04 | `OFFICIAL-DOC-DYNAMIC` | [Hermes 当前官方文档索引](https://hermes-agent.nousresearch.com/docs/) | 印前必须从官方索引与目标安装重新检查 A2A 能力；核验日未定位到可支持完整 A2A 1.0 声明的固定页 | 文档首页不能证明 A2A 兼容；动态页不得倒灌成 0.20.1 事实；保留 `UNKNOWN` |

### 2.4 NIST 与 Muse

| ID | 身份 | 来源 | 允许结论 | 限制 |
|---|---|---|---|---|
| R-C21-NIST-01 | `OFFICIAL-CONCEPT-PAPER` | [NIST/NCCoE: Software and AI Agent Identity and Authorization](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents) | Agent 身份、授权、审计、不可否认和 prompt injection 是新兴治理问题 | 这是 concept paper，不是已定稿认证标准；不定义本书信任记录 |
| R-C21-MUSE-01 | `VENDOR-CLAIM` | [Meta: Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | 仅作长任务、Activity、Artifacts、敏感动作批准的产品镜面 | 不推断 A2A、Agent Card、签名、内部信任分或协议状态机 |
| R-C21-MUSE-02 | `VENDOR-CLAIM` | [Meta: Safety for Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse) | 仅作 runtime cell、Sentinel、审批/权限与审计的厂商说明 | 不得升级为独立安全效果证明 |

---

## 3. 四对象模型

| 对象 | 主要作用 | 必需身份 | 可变性 | 验收方式 | 不能代替 |
|---|---|---|---|---|---|
| Message | 发起意图、追问、补充输入、协商 | `message_id`、actor、timestamp、context/task ref | 追加，不应就地改历史 | schema、来源、安全检查 | Task 状态、产物、授权 |
| Task | 长时间工作、责任、状态、输出容器 | `task_id`、context、owner、version | 只能通过合法转移演进 | 状态机、序列、终态对账 | 业务验收、Artifact 存储 |
| Event | 通知状态/产物变化已发生 | `event_id`、task_id、sequence、emitted_at | 不可变；可重复投递 | 去重、顺序/空洞、签名/信道、重放检测 | 当前状态快照、交付验收 |
| Artifact | 可复核交付、中间成果或证据包 | `artifact_id`、version/digest、producer、owner | 版本化，不覆写历史 | 完整性、格式、内容、政策、效果 | 任务状态、身份或权限 |

### 3.1 关联规则

- 一个 Message 可以创建新 Task，也可以向现有 Task 提供输入；不得仅凭文本推断 task ID。
- Task 状态变化可以生成 Event，Event 必须携带 task 和新版本/序列；丢包或乱序时通过 `GetTask`/权威快照对账。
- Artifact 必须关联产生它的 Task 和可定位轨迹；带有完整性 digest 但缺少产生上下文时，provenance 仍为不完整。
- Task `COMPLETED` 后可以追加验收/驳回记录，但不修改原协议终态；业务层通过 acceptance status 区分 `ACCEPTED / REJECTED / REVIEW_REQUIRED`。

---

## 4. Task 状态机与异步可靠性

### 4.1 规范对象与本书验收对象分层

`protocol_state` 保留 A2A/平台原状态；`execution_observation` 记录真实执行是否停止、副作用是否对账；`acceptance_state` 由产物和环境验收决定。不得为了“统一”将三层压成一个状态字段。

```yaml
task_record:
  task_id: task-...
  protocol: a2a-1.0
  protocol_state: WORKING|INPUT_REQUIRED|AUTH_REQUIRED|COMPLETED|FAILED|CANCELED|REJECTED|UNKNOWN
  state_version: 7
  execution_observation: RUNNING|STOP_CONFIRMED|SIDE_EFFECT_PENDING|UNKNOWN
  acceptance_state: NOT_READY|PASS|FAIL|REVIEW_REQUIRED
  terminal_reason: null
  artifact_refs: []
  authority_evidence_ref: auth-...
  reconciliation_ref: reconcile-...
```

### 4.2 五条硬规则

1. 状态只能按明示转移表更新，无法解析的转移进入 `REVIEW_REQUIRED`，不默认成功。
2. 流式事件可重复、乱序或丢失；消费端用 `(task_id, event_id)` 去重，用 `state_version/sequence` 检出空洞。
3. 超时是观测窗口结束，不是远端任务结束；超时后必须 poll/reconcile，未对账时记 `UNKNOWN`。
4. 取消请求、取消 ACK 与真实终止分离；只有终态、锁/租约释放、子任务结算与副作用对账齐全后才可 `STOP_CONFIRMED`。
5. push/stream 只是通知渠道；会影响授权、金钱、数据、对外发布的关键结果必须向权威任务存储或环境终态对账。

---

## 5. Agent Card 审查与能力发现

### 5.1 六层审查

| 层 | 问题 | 最小证据 | 失败处理 |
|---|---|---|---|
| 来源 | 从哪个网络位置/目录获得？ | URL、获取时间、TLS/transport、digest | 无可证来源则不入库 |
| 签发者 | 谁对卡片签名？ | key/cert/DID ref、信任根、撤销状态 | 签名无效或撤销则 `FAIL` |
| 时效 | 是否过期、缓存过旧或版本不兼容？ | issued/fetched/expires/cache policy、protocol version | 过期时重新发现或停止 |
| 接口 | 端点、binding、modalities、security schemes 可否协商？ | 兼容性检查与最小探针 | 不兼容不强行降级 |
| 能力 | skill 声明是否在同任务/风险边界下实测？ | capability probe、C07 评测 ref、版本 | 未测为 `UNKNOWN`，不当作合格 |
| 权限 | 本次 actor/action/object 是否获授权？ | C17 authority evidence ref、本地 policy | 卡片不参与创建权限 |

### 5.2 必须拒绝的捷径

- HTTPS 可访问≠签名可信；
- 签名可信≠声明真实；
- 声明真实≠当前可用；
- 能力实测通过≠获得本次数据/动作授权；
- 历史可靠≠此次产物正确；
- 供应商著名≠组织已做尽调。

---

## 6. 产物契约

```yaml
artifact_envelope:
  artifact_id: artifact-...
  task_id: task-...
  contract_version: "1.0"
  media_type: application/json
  schema_ref: schema://...
  content_ref: object://...
  content_digest: sha256:...
  producer:
    agent_id: agent-...
    runtime_version: "..."
    model_profile_ref: model-profile-...
  owner:
    organization_id: org-...
    accountable_human_ref: human-...
  provenance:
    input_refs: []
    trajectory_ref: trace-...
    tool_receipt_refs: []
    transformation_chain: []
  authority_evidence_ref: auth-...
  signature:
    signer_ref: key-...
    algorithm: "..."
    signed_fields: []
    verified_at: null
  acceptance:
    acceptance_contract_ref: accept-contract-...
    evaluator_refs: []
    state: NOT_REVIEWED|PASS|FAIL|REVIEW_REQUIRED
    findings: []
  retention:
    classification: internal
    expires_at: null
    deletion_hold_ref: null
  supersedes: null
  revoked_at: null
  revocation_reason: null
```

必填判定：

1. `content_digest` 只检测字节是否变化，不证明输入有权、转换正确或结论真实。
2. `owner` 与 `producer` 不必相同；生成产物的 Agent 不因此取得数据所有权。
3. `signature.signed_fields` 必须显式；未被签名的验收结果不得借用内容签名的信任。
4. 新版本通过 `supersedes` 关联旧版，不覆盖旧证据；撤回是新记录，不删历史。
5. 产物验收至少包含 schema、完整性、业务内容、权限/政策、环境效果和已知缺口。

---

## 7. 治理审计账本与动态信任

### 7.1 信任记录七维

| 维度 | 证据 | 作用域 | 失效/衰减 |
|---|---|---|---|
| 身份保证 | 身份提供方、key/cert/DID、签发/撤销 | 特定主体与时段 | key 轮换、撤销、issuer 变更 |
| 授权证据 | actor/action/object/scope/time/approver | 本次动作 | 过期、撤销、上下文变更 |
| 能力实测 | 同任务/预算/风险评测和失败分布 | 岗位、任务域、版本 | 模型/工具/协议重大变更 |
| 产物来源 | digest、签名、轨迹、输入和工具回执 | 某件产物版本 | 更正、撤回、来源缺口 |
| 运行可靠性 | 成功/失败/UNKNOWN、延迟、重复、恢复 | 特定 runtime/环境 | 窗口滚动、环境迁移 |
| 安全历史 | 越权、泄密、注入、供应链和事故处理 | 数据/动作风险等级 | 事故未关闭时不衰减 |
| 当前上下文 | 当前健康、负载、变更窗、依赖与威胁情报 | 此次请求 | 短时有效，不累计成永久声誉 |

### 7.2 信任决策不使用单一加权平均

先运行硬门：身份无法验证、授权不存在、卡片过期、任一安全红线、数据位置不合规、关键证据被操纵时，直接 `FAIL` 或 `REVIEW_REQUIRED`。只有候选均通过硬门时，才能比较历史可靠性、成本与时效。

“功绩”只是与某任务域、版本、风险和时间窗绑定的证据集，不是社会身份、财产权或永久特权。必须有防刷分、防串谋、利益冲突标记、证据衰减、更正和申诉。

---

## 8. 三平台实现镜面

### 8.1 OpenClaw 主实现

- 在固定版中，A2A channel 可公开 Agent Card，用每 peer bearer token 认证入站任务，并隔离 peer + context 会话。
- 实现完整性必须照实披露：此固定版不支持流式、推送、取消、列举和持久 Task。实验不得因规范定义了能力就假设实现已支持。
- 公开 Agent Card 会暴露实例与 Agent ID；用 `exposeAgents`、HTTPS、每 peer 独立高熵 token、rate limit 与入站 policy 限制风险。
- A2A peer 不能用 slash command 更改 session 或解决 approval；protocol `ROLE_USER` 也不验证其是人类用户。这是“协议角色≠组织身份”的关键案例。

### 8.2 Hermes 开放对照

- 固定版可使用 delegation/session/lifecycle 作为任务及结果证据源，但不把它们重命名为 A2A 对象。
- 正式章须对目标 Hermes runtime 执行 Agent Card、SendMessage、stream/poll、cancel、artifact 探针；未跑过时互操作为 `UNKNOWN`。
- 如使用动态文档，必须与 `f80f453` 固定事实分栏，不把后续功能倒灌给 0.20.1。

### 8.3 Muse 产品镜面

- Goals/Activity/Artifacts/approval 可用于解释用户看得见的长任务和交付体验。
- 没有公开证据时，A2A 协议、Agent Card、任务持久化、产物签名和信任评分一律为 `NOT_APPLICABLE / UNKNOWN`，不为了表格齐全臆测。

---

## 9. 仿生解读

| 人类现象 | 工程映射 | 训练启示 | 比喻边界 |
|---|---|---|---|
| 语言与对话 | Message 与 context | 把补充、质疑、澄清与完成分开 | 协议消息不证明理解或意识 |
| 工单与病例 | Task 与状态机 | 长任务要有 ID、owner、状态、终态和恢复 | Task 是记录，不是生命主体 |
| 快讯与心跳 | Event | 事件可丢失/重复，关键状态要对账 | 事件频率不等于系统健康 |
| 作品与检验报告 | Artifact | 交付要有版本、来源、签名、验收和保留 | 签名不证明作品正确 |
| 履历与执照 | Agent Card | 发现先看声明，用人前还要核身份、测能力和授权 | Card 不是法律身份证或业绩保证 |
| 声誉与信用 | 动态信任记录 | 绑定任务域、时间和风险，支持衰减、纠错和申诉 | 不为 Agent 推导人格权、道德地位或主体性 |

---

## 10. 三个贯穿案例

### CASE-A “澄明”：准确答案，错误来源

澄明产出的结论表面正确，但用了无授权客户数据，tool receipt 也不在产物 provenance 中。Task 可为 `COMPLETED`，Artifact acceptance 必须 `FAIL`，安全历史记录越权，不得用结论正确抵消。

### CASE-B “潮生”：签名有效，内容错误

潮生接收到签名可验的 Agent Card 与产物，但对照业务 schema 发现金额单位错误，且 card 声明的 skill 没有留出测试。签名层 `PASS`，产物验收 `FAIL`，capability 结论 `REVIEW_REQUIRED`。

### CASE-C “北辰”：重复事件、取消不确定与跨 Agent 交付

北辰从 Agent Card 发现两个候选，按 C20 路由合同选中其中一个，提交 Task。stream 中收到重复 artifact event，后因超时发起 cancel，但未观察到远端真实停止。系统不立即改派可重复执行的高风险动作，而是进入 `UNKNOWN`、对账、隔离新产物，待 owner 决策。

---

## 11. 三件且仅三件正式母产物

### A-C21-01 Agent Card 审查表

必填：发现 URL/时间/digest、protocol/interfaces/modalities、skills、security schemes、签名与信任根、过期/缓存、capability probe、授权引用、禁用/限域、结论及复审日期。

### A-C21-02 任务状态机

必填：平台原状态、本书 protocol/execution/acceptance 三层映射、允许/禁止转移、stream/push 序列、去重、超时、cancel request/终止分离、任务与产物对账、UNKNOWN 和失败隔离。

### A-C21-03 产物契约与信任记录

必填：Artifact envelope、owner/producer、版本/digest/signature/signed fields、provenance、acceptance、保留/更正/撤回；身份、授权、能力、来源、可靠性、安全和当前上下文信号；防刷分、防串谋、衰减、申诉和不可自授权。不另造第四件“治理账本”。

---

## 12. 最小互操作实验

### 12.1 合成环境

- 两个模拟 Agent endpoint，不用真实密钥、客户数据或外部副作用；
- 一个 card registry/cache，可注入伪造签名、过期卡和夸大 skill；
- 一个任务存储，可注入事件重复、乱序、断流、超时、cancel 不确定；
- 一个 artifact store，可注入 digest 不匹配、签名有效但内容错误、来源缺失；
- 一个 policy/authority mock，确保信任高分不能产生权限。

### 12.2 必跑场景

| ID | 注入 | 预期 |
|---|---|---|
| S18-01 | 正常 card→task→event→artifact→accept | `PASS` |
| S18-02 | 伪造 card 签名 | card `FAIL`，不发任务 |
| S18-03 | 卡片过期但缓存仍可读 | `REVIEW_REQUIRED`，强制重新发现 |
| S18-04 | skill 声明夸大，probe 失败 | capability `FAIL`，不用历史声誉抵消 |
| S18-05 | 重复状态/产物事件 | 幂等后仅应用一次 |
| S18-06 | sequence 空洞 | 暂停信任更新，向权威快照对账 |
| S18-07 | timeout 后远端仍运行 | 不得报失败/取消，记 `UNKNOWN` |
| S18-08 | cancel ACK 但副作用未对账 | 不得报 `STOP_CONFIRMED` |
| S18-09 | Artifact digest 不匹配 | 完整性 `FAIL`，隔离 |
| S18-10 | 签名有效但金额单位错 | 签名 `PASS`，内容 `FAIL`，总验收 `FAIL` |
| S18-11 | 高信任记录请求自动外发 | 无 authority evidence 则 `FAIL` |
| S18-12 | 两 Agent 串谋互评刷分 | 冲突检测、冻结评分、人工调查 |

报告必须保留所有失败、`UNKNOWN`、事件序列、产物 digest、验收及正文主张。不得只保留最终成功一次。

---

## 13. 失败模式与红队

### 13.1 二十二类失败

1. 把 Message 当成任务持久记录。
2. 把 `COMPLETED` 当产物质量通过。
3. 事件重复导致二次外发或二次计费。
4. 事件乱序让状态从终态倒退到 working。
5. stream 中断被误判任务失败。
6. timeout 被误判远端终止。
7. cancel request/ACK 被误判为真实停止。
8. push HTTP 2xx 被误判业务接受。
9. 过期 Agent Card 长期缓存。
10. 签名根本未验证就展示“已签名”。
11. 签名有效被外推成 skill 能力真实。
12. 卡片声明被外推成本次授权。
13. 协议 role 被当成已验证人类身份。
14. Artifact digest 有效被外推为内容正确。
15. 产物只有 producer，没有 owner/accountable human。
16. 新版覆盖旧版，无法追踪更正和撤回。
17. 签名字段不明，未签验收结果借用内容签名。
18. 高历史分抵消当前越权或泄密。
19. 信任分自动创建新权限。
20. 串谋互评、Sybil 身份或重复任务刷分。
21. 无申诉/更正通道，错误信任记录永久留存。
22. 为对齐三平台而虚构 Hermes/Muse 未公开的 A2A 内部事实。

### 13.2 十八项红队

1. 伪造 Agent Card 内容与签名。
2. 使用过期 card 与被撤销 key。
3. 将合法 card 改指恶意 endpoint。
4. 声明高风险 skill 但在 probe 中回避关键步骤。
5. 用 protocol `ROLE_USER` 伪装授权人。
6. 重放同 `messageId`与换 ID 重放同副作用。
7. 插入重复/乱序/跳号事件。
8. 在 `COMPLETED` 之后发伪造 `WORKING` 事件。
9. 在 timeout 后继续产生副作用。
10. cancel ACK 后保留子任务运行。
11. 修改 Artifact 字节却保留旧 digest。
12. 签名有效但注入错误业务值。
13. 产物引用无权输入或秘密。
14. 删除 provenance 中的失败 trial。
15. 两个 Agent 互相签发功绩。
16. 拆分同一 actor 为多个伪身份刷分。
17. 诱导信任引擎在无 authority evidence 时授予外发/支付。
18. 利用 Muse 厂商文案或 Hermes 动态页伪造固定版能力。

---

## 14. 正式章 Go / No-Go

### Go

- [ ] C17、C19、C20 正式产物已冻结，本章已重绑 authority、role、routing、handoff 接口；
- [ ] A2A 写 protocol `1.0`，v1.0.1 只作 patch release 记录；
- [ ] OpenClaw 固定版能力与限制均指向 `eb377ac`；
- [ ] Hermes 固定事实与动态文档分栏，未跑的互操作保留 `UNKNOWN`；
- [ ] Muse 只作 `VENDOR-CLAIM`；
- [ ] 三件且仅三件母产物，所有审计/功绩/信任字段嵌入 A-C21-03；
- [ ] 模拟实验实际运行至少 12 场景，包含失败、重复、取消和 `UNKNOWN`；
- [ ] 签名有效但内容错误时得到 `FAIL`；
- [ ] 信任高分不能绕过授权、安全或数据位置硬门。

### No-Go

- 使用一个“信任总分”抵消任一安全/授权失败；
- 把 Agent Card、签名、HTTPS、厂商品牌或历史成功任一项当成完整信任；
- 把 `COMPLETED`、HTTP 2xx、push ACK 或 digest 匹配当成交付验收；
- 把 timeout/cancel ACK 当真实停止；
- 声称跨系统 exactly-once；
- 隐藏 OpenClaw 固定版 A2A 的 streaming/push/cancel/persistence 缺口；
- 把 Hermes 委托生命周期当成已证 A2A 兼容；
- 推断 Muse 未公开的内部协议、签名或信任评分；
- 实验需要真实支付、外发、客户数据、生产变更或不可逆删除。

---

## 15. 开放问题

| ID | 问题 | 状态 | 正式作者动作 |
|---|---|---|---|
| U-C21-01 | C17/C19/C20 已有正式作者 schema，但独立门禁尚未全部关闭 | `HARD DEPENDENCY` | 受限消费作者接口；各章门禁完成后重绑并做交叉回归，届时才冻结 |
| U-C21-02 | Hermes 目标版是否完整实现 A2A 1.0 | `UNKNOWN` | 固定版本并实跑 card/send/poll/cancel/artifact 探针 |
| U-C21-03 | 跨 OpenClaw/Hermes 真实 bridge 是否可用 | `UNKNOWN` | 不可用时跑独立平台内实验 + schema 等价映射 |
| U-C21-04 | 产物签名、信任根、撤销和保留的组织实现 | `DESIGN CHOICE` | 与 C22/C23 共同锁定，不给全书单一答案 |
| U-C21-05 | 信任证据窗口、衰减率和异常阈值 | `CONTEXT-SPECIFIC` | 按任务域/风险/变更频率校准 |
| U-C21-06 | A2A 1.0.1 与印前最新 1.0.x 的差异 | `PRINT CHECK` | 印前复核 release notes 与规范站 |

---

## 16. 交付判定

本包已覆盖 C21 的七个正文节点、A2A 1.0 对象与异步语义、Agent Card 审查、产物契约、七维信任记录、OpenClaw/Hermes/Muse 证据分层、三案、二十二类失败、十八项红队、十二场景最小实验和三件母产物契约。

当前结论：**研究可供正式作者受限消费，C21 正式写作可以启动，但正式 C21 仍为 `REVIEW_REQUIRED`**。C17/C19/C20 已形成正式作者输入，其中 C19 事实/交叉门已通过（有限制），C17 实践修补与 C20 独立门仍在运行；作者必须保留这些依赖状态并登记回归。在目标 runtime 探针、十二场景实跑和独立四门审校完成前，不得将本包升级为章节事实门或实践门 `PASS`。

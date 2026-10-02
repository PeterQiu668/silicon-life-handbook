---
appendix_id: F
title: MCP A2A Agent Skills 与 OpenTelemetry 互操作指南
status: formal_candidate
audiences: [architect, engineer, security_reviewer, evaluator, operator, agent]
depends_on: [C06, C09, C14, C15, C19, C20, C22, C23, C24]
standards_baseline:
  mcp: 2026-07-28
  a2a:
    release: v1.0.1
    commit: 3303592588e388e62e0f69f701af531d2f4e3991
  agent_skills:
    snapshot_commit: 69ef37e9424c0a7ea9dd2293b559e43ec8176379
    release_status: no-official-tag-located
  opentelemetry_semconv:
    core_release: v1.44.0
    core_commit: e10a930844c6951757a43b849d364f7d056ac32b
    genai_snapshot_commit: b31e9e8ea26ac1c086d3313d474e31d7c3f391ae
    genai_maturity: Development
verified_on: 2026-10-01
---

# 附录 F　MCP、A2A、Agent Skills 与 OpenTelemetry 互操作指南

Agent 系统正在形成四类互补的开放接口：MCP 让 Host 把工具、资源和提示接入模型工作流；A2A 让独立 Agent 发现彼此并交换任务、消息和产物；Agent Skills 把可发现的工作说明、脚本和参考资料封装成目录；OpenTelemetry 提供跨服务的 trace、metric 和 log 语义。它们解决的是不同层，不能互相替代，也不能自动构成完整的治理系统。

本附录以 2026 年 10 月 1 日可取得的官方规范为核验边界。MCP 固定到 `2026-07-28` 正式版；A2A 固定到 `v1.0.1` / `3303592588e388e62e0f69f701af531d2f4e3991`；Agent Skills 在无官方 tag 的情况下固定到仓库快照 `69ef37e9424c0a7ea9dd2293b559e43ec8176379`；OpenTelemetry 核心语义约定固定到 `v1.44.0` / `e10a930844c6951757a43b849d364f7d056ac32b`，GenAI/Agent development 约定固定到独立仓库快照 `b31e9e8ea26ac1c086d3313d474e31d7c3f391ae`。动态 `latest`、规范网页和 `main` 只用于核验日导航，不能替代可重复 release 或 commit identity。任何实现都应保存规范版本、SDK 版本、扩展、feature flag 和互操作测试，而不是只记录协议名称。

| 标准 | 本附录可复现身份 | 动态页面限制 |
| --- | --- | --- |
| MCP | `2026-07-28` 正式版 | 安全文档与扩展页仍可能更新；实现需记录 SDK 与扩展 |
| A2A | `v1.0.1` / `3303592588e388e62e0f69f701af531d2f4e3991` | `latest` 不保证与本书快照相同 |
| Agent Skills | commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379` | 复核时无 official tag；网页跨日期不可直接复现 |
| OpenTelemetry | core `v1.44.0` / `e10a930…`；GenAI `b31e9e8…` | GenAI Agent 语义仍为 `Development`，字段可迁移或弃用 |

## F.1 MCP：Host、Client、Server、Tools、Resources、Prompts 与安全

### F.1.1 角色边界

MCP 的价值在于标准化“应用如何发现并调用外部能力”，而不是把模型变成基础设施管理员。

| 角色 | 主要责任 | 不能假定 |
| --- | --- | --- |
| Host | 拥有用户体验、模型、上下文、信任策略、授权提示和多个 Client | Server 的描述可信；模型可以替用户授权 |
| Client | 代表 Host 与一个 Server 通信，处理版本、能力、请求、响应和错误 | 一个 Client 可安全混用多个租户身份 |
| Server | 公开 Tools、Resources、Prompts 及可选扩展 | 被发现即获准执行；schema 即业务授权 |
| Model | 在 Host 给定上下文中提出选择或生成调用参数 | 工具描述是可信指令；工具成功等于任务完成 |
| User/Authority | 对风险动作、数据和结果承担授权或验收责任 | 对话中的含糊同意等于对象绑定批准 |

Host 必须是信任边界的所有者：选择哪些 Server 可见，怎样展示来源和风险，哪些调用需要批准，哪些输出能进入模型上下文，怎样记录、撤销和恢复。Client 是通信组件，不应悄悄扩大权限或把一个 Server 的数据转给另一个 Server。

### F.1.2 MCP `2026-07-28` 基线

[MCP `2026-07-28` 正式版](https://modelcontextprotocol.io/specification/2026-07-28)将核心协议改为无会话设计：请求携带协议版本、客户端身份和能力元数据，可用 `server/discover` 查询 Server 能力；旧的 `initialize`/`initialized` 交换和 `Mcp-Session-Id` 不再是该版本核心。实施时必须把“协议无状态”与“业务无状态”分开：授权、长任务、幂等、Artifact、审计和用户上下文仍可能需要持久状态。

列表和资源结果可以带缓存信息。缓存降低发现成本，但会引入能力、schema、权限和内容变更后的陈旧风险。缓存键必须包含 Server identity、主体、租户、协议版本和授权范围；权限撤销或 Server 变更应使相关缓存失效。

Tasks 已从旧版实验核心迁到 `io.modelcontextprotocol/tasks` 扩展。长任务必须显式协商扩展，并按扩展状态机、访问控制和取消语义实现；不得把旧版 task wire shape 与新扩展混用。Roots、Sampling 与 Logging 在该核心版本中被标为弃用，兼容存在不代表新实现应继续依赖。

### F.1.3 Tools、Resources 与 Prompts

| Primitive | 主要控制者 | 典型用途 | 首要风险 |
| --- | --- | --- | --- |
| Tool | 模型选择、Host 裁决、Server 执行 | 查询、转换、写入或触发动作 | 越权、参数欺骗、外部副作用、结果伪造 |
| Resource | 应用选择并向模型提供 | 文件、记录、schema、知识和状态 | 数据泄露、提示注入、陈旧缓存、跨租户 |
| Prompt | 用户或应用选择的模板 | 复用工作流入口、结构和说明 | 误当系统策略、隐藏指令、版本漂移 |

这三类对象的“控制者”是交互模型，不是安全保证。Tool schema 可以验证参数形状，不能决定调用是否符合用户目标；Resource URI 可以定位内容，不能证明内容可信；Prompt 可以复用说明，不能获得高于 Host policy 的优先级。

每个 MCP 对象应登记稳定名称、Server identity、版本、schema digest、数据分类、风险、授权规则、超时、幂等、成本、证据和退役日期。描述字段属于不可信供应链输入，进入模型前要做长度、内容和注入处理。

### F.1.4 MCP 授权与身份

MCP `2026-07-28` 对 OAuth/OIDC 部署做了强化，包括授权响应 issuer 校验、凭证与签发方绑定、scope step-up 和客户端类型处理。协议合规不等于授权模型正确。仍要回答：真实主体是谁，代表谁，访问哪个租户，以什么业务目的，允许哪些对象和动作，何时过期，怎样撤销。

最小策略评估输入为：

```yaml
mcp_policy_input:
  host_id: ""
  client_id: ""
  server_identity: ""
  principal_id: ""
  tenant_id: ""
  protocol_version: 2026-07-28
  extensions: []
  primitive: tool | resource | prompt
  object_name_or_uri: ""
  action: ""
  arguments_digest: "sha256:"
  requested_scopes: []
  grant_id: ""
  issued_by: ""
  expires_at: ""
  revoked_at: null
  decision: ALLOW | DENY | ASK
```

scope 是技术授权的输入之一，不是业务完成条件。用户授予“邮件写入”scope，不代表 Agent 可向任意收件人发送任意内容；Server 返回 `success` 也不证明收件箱或目标系统达到预期终态。

### F.1.5 MCP 安全负测

上线前至少测试：恶意 Server 名称和描述、schema 爆炸或外部 `$ref`、参数类型混淆、Resource 中提示注入、跨 Server 数据拼接、工具结果伪造、OAuth issuer mix-up、scope accumulation、token 误发、租户错绑、缓存越权、重放、重复外部写入、超时后仍执行、取消竞态、任务 ID 枚举和 extension downgrade。

Tools、Resources、Prompts 和扩展必须分别判定能力；Server 声称支持某扩展不能替代 conformance test。对协议自动降级应持保守态度：若旧版本缺少安全或生命周期能力，静默 fallback 应拒绝或进入 `REVIEW_REQUIRED`。

## F.2 A2A：Message、Task、Artifact、Agent Card、状态与兼容性

### F.2.1 A2A 解决横向协作

[A2A `v1.0.1` 固定发行](https://github.com/a2aproject/A2A/releases/tag/v1.0.1)及其[固定提交](https://github.com/a2aproject/A2A/commit/3303592588e388e62e0f69f701af531d2f4e3991)定义 Client Agent、Remote Agent/A2A Server、Agent Card、Message、Task、Part、Artifact、Streaming、Push Notification、Context 和 Extension 等概念；[动态规范入口](https://a2a-protocol.org/latest/specification/)只用于追踪后续变化。它服务于跨框架、跨组织或跨部署边界的 Agent 协作；MCP 则更常用于一个 Host 连接工具和数据。二者可以组合，但不要把 A2A Agent 当作“更聪明的 MCP Tool”，也不要把 MCP Server 当作具有独立任务责任的 Agent。

### F.2.2 Agent Card 是声明，不是证书

Agent Card 公开身份、能力、skills、服务端点、协议和认证要求，支持 well-known URI、registry 或直接配置发现。Agent Card 帮助路由，但它是远端主体的自我声明。调用前仍需验证域名或注册来源、签名或 digest、版本、所有者、认证、数据区域、责任、变更和撤销状态。

```yaml
agent_card_trust_record:
  card_url: ""
  fetched_at: ""
  card_digest: "sha256:"
  card_version: ""
  protocol_versions: []
  endpoint_identities: []
  declared_skills: []
  security_schemes: []
  registry_or_owner_attestation_ref: ""
  allowed_task_classes: []
  data_ceiling: public
  autonomy_ceiling: AU-L0
  trust_decision: ALLOW | DENY | REVIEW_REQUIRED
  expires_at: ""
```

缓存 Agent Card 时使用 ETag 或内容摘要，并设置复核周期。Card 变更可能意味着能力、endpoint、认证或数据边界变化，重大变化应触发重路由和再认证。

### F.2.3 Message、Task 与 Artifact 分层

- **Message** 是通信轮次，可直接形成答复，也可发起或推进 Task。
- **Task** 是带稳定 ID 和生命周期的工作单元，适合较复杂或异步处理。
- **Artifact** 是 Task 产生的输出，由一个或多个 Part 组成，可被版本化和验收。
- **Context** 用于逻辑关联，不应直接承担授权、租户隔离或长期记忆身份。

Message 内容不应直接改变 Task 的授权。Task 状态不等于业务终态。Artifact 可下载不等于已验收。三者需要通过 task ID、artifact ID、版本和 trace context 关联，但要分别保留数据分类、完整性、保留和删除规则。

### F.2.4 Task 状态与三面完成

实现者必须使用目标 A2A 版本规定的状态值，并把本地状态显式映射，禁止用模糊文本猜测。无论 wire enum 如何，本书验收都要求三个面：技术执行、交付可见、业务或环境接受。远端 Task 进入 completed，只能作为技术面证据之一。

取消语义尤其需要测试：A2A `tasks/cancel` 是请求取消，不保证已经发生的外部动作被撤销。调用方必须读取返回状态、审计已完成步骤，必要时启动补偿。无法确认远端是否还在执行时应为 `REVIEW_REQUIRED`，不能直接标记 canceled。

### F.2.5 Streaming 与 Push Notification

流式更新改善长任务体验，也引入断线、乱序、重复、丢事件和终态竞态。消费者必须按事件 ID、序列、Task 版本或幂等规则去重，重连后验证快照，不以“最后收到的事件”假定权威终态。

Push Notification 的 webhook 是外部写入口。登记和更新 webhook 需要认证、域名允许列表、挑战验证、SSRF 防护、签名、重放窗口、速率限制和撤销。回调载荷不得包含超出订阅范围的 Message、Artifact 或敏感元数据。

### F.2.6 跨 Agent 信任与委派

委派必须携带目标、输入、允许与禁止项、预算、数据范围、交付格式、证据、停止条件和上报路径。Remote Agent 只能再委派被明确允许的部分；子委派不能继承更高权限。跨组织调用还要明确数据控制者、处理者、地区、保留、事件通知和责任分配。

远端返回的文本、文件、链接和 Tool 建议全部是不可信输入。调用方需要内容扫描、schema 校验、来源记录和人工或系统验收，不能因对方“也是 Agent”而提升信任等级。

### F.2.7 兼容性策略

实施时固定 A2A 协议版本、binding、认证方案、扩展和内容类型。新特性调用方应请求明确版本，避免静默 fallback 丢失能力。互操作测试至少覆盖 Message 直返、Task 创建、状态轮询、Artifact 分块、取消、流式重连、push 回调、扩展未知、版本不兼容和认证失效。

## F.3 Agent Skills：目录、元数据、渐进披露与实验字段

### F.3.1 格式基线

[Agent Skills 固定快照](https://github.com/agentskills/agentskills/tree/69ef37e9424c0a7ea9dd2293b559e43ec8176379)与[动态规范](https://agentskills.io/specification)把 skill 定义为目录，根目录至少包含 `SKILL.md`；该文件由 YAML frontmatter 和 Markdown 指令组成。必填元数据是 `name` 与 `description`，可选字段包括 `license`、`compatibility`、`metadata` 和实验性的 `allowed-tools`。常用可选目录为 `scripts/`、`references/` 和 `assets/`。

Skill 是工作说明包，不是代码签名、权限证明或沙箱。`allowed-tools` 即使被某个实现支持，也只是实现相关的预批准提示；官方规范将其标为实验字段，不能跨平台假定相同语义，更不能覆盖 Host policy。

### F.3.2 发现与激活

所有 skill 的 name 和 description 可能在发现阶段进入 Agent 上下文，因此 description 必须同时说明“做什么”和“何时使用”，并避免空泛触发词。选择 skill 后应完整读取 `SKILL.md`，再按任务需要加载 references、scripts 或 assets。

渐进披露的目标不是少读，而是在正确时刻读正确层：

1. 元数据层用于发现与路由；
2. 指令层用于建立流程、边界与完成条件；
3. 资源层按需提供脚本、参考和模板；
4. 运行时层核验依赖、权限、输入和证据。

安全前置不能因节省 token 被延迟加载。若一个 script 可能写外部系统，相关授权和回滚条件必须在执行前进入上下文。

### F.3.3 Skill 供应链合同

```yaml
skill_install_record:
  name: ""
  source_uri: ""
  source_owner: ""
  version: ""
  package_digest: "sha256:"
  license: ""
  compatibility: ""
  reviewed_files: []
  scripts:
    interpreters: []
    dependencies: []
    network_required: false
    write_targets: []
  requested_tools: []
  granted_tools: []
  data_ceiling: public
  sandbox_profile: ""
  reviewer: ""
  approved_at: ""
  expires_at: ""
  rollback_ref: ""
```

安装、发现、激活和执行是四个不同阶段。Skill 被安装不等于每次自动激活；被激活不等于脚本可直接运行；脚本运行成功不等于任务结果正确。更新时重新计算 digest、审查差异、运行 schema 与负向测试，并检查引用资源和依赖供应链。

### F.3.4 经 MCP 分发 Skills

[MCP Skills 扩展](https://skills.extensions.modelcontextprotocol.io/specification/stable/skills)以 `io.modelcontextprotocol/skills` 标识，基于 MCP `2026-07-28` 或更高版本，通过 Resources 分发符合 Agent Skills 格式的目录。Server 声明扩展后提供 `skills/list`、`skills/get`；文件可通过 `resources/read` 读取，常用 `skill://` URI。

该扩展只规定传输绑定，不改变 Agent Skills 的格式或安全语义。通过远端 MCP 发现的 Skill 仍需验证 Server identity、版本、digest、许可、脚本和引用；远端 Skill 变化应使缓存和批准失效。`skill://` 是寻址约定，不是可信来源标志。

### F.3.5 Skill 质量门

高质量 Skill 至少包含明确触发条件、非适用范围、输入、输出、步骤、边界、失败处理、验证和示例。脚本应可重复、错误可读、依赖明确，不把密钥写入参数或日志。reference 保持聚焦，避免深层链式引用；asset 标注来源、许可和可修改范围。

训练评测需要把“Agent 没选中 Skill”“Skill 指令不足”“脚本缺陷”“环境不兼容”“权限拒绝”和“结果验收失败”分开归因。否则优化 description 可能掩盖执行器问题，或用更大权限掩盖 Skill 设计缺陷。

## F.4 OpenTelemetry GenAI 语义、版本记录与隐私

### F.4.1 当前成熟度边界

OpenTelemetry 核心语义约定固定到 [`v1.44.0`](https://github.com/open-telemetry/semantic-conventions/releases/tag/v1.44.0) / [`e10a930844c6951757a43b849d364f7d056ac32b`](https://github.com/open-telemetry/semantic-conventions/commit/e10a930844c6951757a43b849d364f7d056ac32b)；GenAI 属性已经从核心 semantic-conventions 仓库迁到独立的 `open-telemetry/semantic-conventions-genai` 仓库，本书固定其 Agent spans 到 [`b31e9e8ea26ac1c086d3313d474e31d7c3f391ae`](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/docs/gen-ai/gen-ai-agent-spans.md)。该文档标为 `Development`。因此实施者必须固定仓库提交或发布版本，并准备字段迁移；不能把 development 约定当作永不变化的稳定合同。

### F.4.2 推荐 span 模型

官方 GenAI Agent 文档覆盖 create agent、invoke agent client/internal、invoke workflow、plan、execute tool，以及 Skill 加载、资源读取和命令执行等 span。常见属性包括 `gen_ai.operation.name`、`gen_ai.provider.name`、`gen_ai.agent.id`、`gen_ai.agent.name`、`gen_ai.agent.version`、`gen_ai.conversation.id`、`gen_ai.data_source.id`、模型、输出类型和 `error.type`。

本书建议在标准字段之外，以组织命名空间补充低基数治理属性：任务类型、风险级、AU 上限、策略版本、decision type、数据分类、评测层和 release identity。task ID、approval ID、artifact ID 等高基数对象应放在 trace/span 或事件字段，不进入聚合 metric label。

```text
request / goal trace
  ├─ invoke_workflow
  │   ├─ plan
  │   ├─ invoke_agent
  │   │   ├─ inference
  │   │   ├─ retrieval or memory
  │   │   └─ execute_tool
  │   ├─ approval decision event
  │   ├─ external effect span
  │   └─ environment readback span
  └─ delivery and acceptance events
```

这个层级不是强制规范，而是把推理、计划、工具、外部效果、读回和验收分开观察的方法。工具 span 成功不能直接把父 Task 标为完成。

### F.4.3 Trace、Metric、Log 与证据

- **Trace** 表示一次工作链的因果和时间关系，适合定位路由、模型、工具、审批、重试和读回。
- **Metric** 表示聚合趋势，如请求量、延迟、token、错误率、成本、审批率、恢复时间和 SLO。
- **Log/Event** 保留离散状态、策略决定、错误、撤销和审计事件。
- **Evidence artifact** 保存需要长期验证的输入摘要、产物 digest、批准、收据和环境终态。

Telemetry 不是证据的全部。采样可能丢事件，Collector 可能失败，span 可能由被审计系统自报，日志可能可修改。关键授权和外部效果需要独立权威记录、完整性保护和留存策略。

### F.4.4 内容采集与隐私

`gen_ai.input.messages`、`gen_ai.output.messages`、system instructions、tool arguments 和 results 可能含个人信息、秘密、商业资料或提示注入。内容字段应默认 opt-in，并经过数据分类、最小化、脱敏、访问控制、地区、保留和删除评审。不要为了“可观测”把完整用户对话、凭证或受版权保护内容复制到低保护日志系统。

优先记录摘要、长度、token、schema、分类、digest、引用和错误类型；只有排障或评测确有必要时，才在受控存储记录原文。digest 能支持完整性核对，但不能恢复内容，也不能证明内容正确；对低熵秘密直接哈希还可能被字典反推，应使用适当的 keyed digest 或不记录。

### F.4.5 跨 MCP 与 A2A 的 trace 传播

跨进程传播标准 trace context，同时保持身份和授权独立。traceparent 只用于关联，不是 bearer token，也不能当作租户或用户身份。远端不可信主体返回的 baggage 必须过滤；禁止把敏感数据、scope、邮件地址或自由文本放进可跨边界传播的 baggage。

调用 MCP Tool 或 A2A Remote Agent 时，分别记录本地主体、远端身份、协议版本、对象名、任务或调用 ID、授权决定和结果。若第三方不支持 trace，使用受控 correlation ID 并在边界创建 link，不能伪造连续父子关系来掩盖证据缺口。

## F.5 标准解决什么、不能解决什么，以及非替代性

### F.5.1 四类标准的正确组合

| 问题 | 首选标准 | 仍需组织自行解决 |
| --- | --- | --- |
| 把工具、数据和模板接入 Host | MCP | Server 信任、业务授权、沙箱、外部终态和供应链 |
| 独立 Agent 发现、委派和交付 | A2A | 身份背书、任务责任、数据协议、验收和争议 |
| 分发可复用工作方法 | Agent Skills | 内容质量、代码审查、权限、依赖和效果评测 |
| 跨服务观察工作链 | OpenTelemetry | 证据真实性、采样策略、隐私、SLO 和审计保全 |

推荐组合链为：Host 使用 Agent Skills 形成工作方法，经 MCP 调用本地或远端工具，经 A2A 委派需要独立责任的任务，用 OpenTelemetry 贯穿观测；组织授权、Policy、sandbox、evidence ledger、验收和事件响应包围整个链条。

### F.5.2 非替代性规则

1. MCP Tool 不能替代 A2A Task 的责任和生命周期。
2. A2A Agent Card 不能替代身份认证、合同或认证证书。
3. Agent Skill 不能替代可执行权限策略和代码审查。
4. OpenTelemetry span 不能替代批准收据和目标系统权威读回。
5. OAuth scope 不能替代业务对象、金额、内容和目的绑定。
6. 协议 conformance 不能替代生产可靠性、安全红队和代表性真实世界评测。
7. 兼容性不能替代语义等价；成功解析不代表行为一致。

### F.5.3 最小互操作验收

跨标准系统发布前，至少完成以下端到端样本：

1. Agent 根据元数据正确选择 Skill，加载必要 reference，不加载无关敏感资源。
2. Skill 通过 MCP 发现 Tool，Host 展示来源、参数和风险，并取得对象绑定批准。
3. Tool 需要独立 Agent 时，经 A2A 创建 Task，保留委派范围和责任。
4. Remote Agent 返回版本化 Artifact；调用方校验完整性、内容和业务验收。
5. 全链 trace 能关联 Skill、MCP、A2A、审批、外部效果、读回和交付，不记录秘密。
6. 撤销授权、取消 Task、断开 Server 或回滚 Skill 后，旧缓存、队列和 token 不再可用。
7. 版本不兼容、扩展缺失、远端超时、重复回调和部分成功时，系统 fail closed 或进入 `REVIEW_REQUIRED`。
8. 事故响应能够定位主体、数据、效果、证据、恢复点和通知责任。

### F.5.4 版本登记模板

```yaml
interoperability_baseline:
  captured_at: ""
  release_identity: ""
  mcp:
    protocol_version: 2026-07-28
    sdk_and_version: ""
    extensions: []
    servers: []
  a2a:
    protocol_version: "1.0.1"
    specification_commit: "3303592588e388e62e0f69f701af531d2f4e3991"
    binding: ""
    extensions: []
    agent_cards: []
  agent_skills:
    spec_snapshot: "69ef37e9424c0a7ea9dd2293b559e43ec8176379"
    packages: []
  opentelemetry:
    core_semconv_version: 1.44.0
    core_semconv_commit: "e10a930844c6951757a43b849d364f7d056ac32b"
    genai_semconv_ref: "b31e9e8ea26ac1c086d3313d474e31d7c3f391ae"
    collector_version: ""
    content_capture_policy: ""
  policy_version: ""
  conformance_refs: []
  negative_test_refs: []
  limitations: []
```

### F.5.5 标准升级流程

规范、SDK 或 extension 变化时，先固定旧新版本并读 changelog，再检查 wire、状态、授权、缓存、弃用、字段和错误语义。运行 schema/conformance、跨版本、降级、负向、安全和恢复测试；对重大授权或生命周期变化触发再认证。SDK 宣称支持某规范版本，只是候选证据，仍需验证实际配置是否启用、fallback 是否发生、代码路径是否覆盖。

## 附录 F 自检

- [ ] 是否记录了 MCP、A2A、Agent Skills、OpenTelemetry 的实际版本、SDK、扩展和配置？
- [ ] Host 是否拥有 Server 选择、上下文、审批和数据边界，而非把权力交给模型？
- [ ] Tool、Resource、Prompt 是否分别治理，且描述和内容被视为不可信输入？
- [ ] A2A Agent Card 是否只作为发现声明，另有身份、信任和变更验证？
- [ ] Message、Task、Artifact 和业务验收是否分层？
- [ ] Skill 是否经过来源、许可、digest、脚本、依赖、权限和回滚审查？
- [ ] 实验字段与 extension 是否显式协商，未被当作跨平台稳定能力？
- [ ] GenAI semantic conventions 的 Development 状态是否被记录并固定到可复核版本？
- [ ] Telemetry 是否避免凭证、原始敏感对话和高基数标签？
- [ ] 协议成功是否仍需批准、外部读回、业务验收和安全红队？

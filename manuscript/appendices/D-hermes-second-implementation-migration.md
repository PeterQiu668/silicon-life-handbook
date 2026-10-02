---
appendix_id: D
title: Hermes 第二实现与迁移指南
status: formal_candidate
audiences: [trainer, engineer, operator, security_reviewer, migration_owner, agent]
depends_on: [C05, C06, C13, C14, C15, C16, C18, C19, C20, C22, C23, C24]
platform_baseline:
  product: Hermes Agent
  version: 0.20.1
  release_tag: v2026.8.13
  commit: f80f453ae0679347e38abc917c7f94f717bf96c5
verified_on: 2026-10-01
---

# 附录 D　Hermes 第二实现与迁移指南

Hermes 在本书中承担“第二开放实现”的角色。它用于检验训练原则是否真正跨平台，也用于揭示 OpenClaw 中看似自然的文件名、组件名和默认行为其实是实现选择。Hermes 不是 OpenClaw 的换皮版本，迁移也不是把目录和配置逐项改名。

本附录固定 Hermes Agent `0.20.1`、发行标记 `v2026.8.13` 和提交 `f80f453ae0679347e38abc917c7f94f717bf96c5`。固定提交支持的事实与核验日动态官方文档要分开记录；真实环境中的权限、凭证、网络、容器和外部效果仍需独立复现。

## D.1 固定版本、Architecture、入口和 AIAgent 运行链

### D.1.1 版本证据

```yaml
hermes_baseline:
  captured_at: ""
  host_ref: ""
  version_output: ""
  release_tag: v2026.8.13
  commit: f80f453ae0679347e38abc917c7f94f717bf96c5
  hermes_home_ref: ""
  profile: ""
  enabled_entrypoints: []
  enabled_backends: []
  config_digest: "sha256:"
  state_digest: "sha256:"
  redaction_report_ref: ""
```

### D.1.2 影响配置、安全、状态与恢复的固定来源映射

影响配置、安全、状态与恢复的事实必须优先回到固定提交，而不是只引用会变化的产品文档。下表所有源码定位均固定到 `f80f453ae0679347e38abc917c7f94f717bf96c5`；它们说明该提交包含的实现表面，不证明某一目标环境已经启用、正确配置或实际通过恢复演练。

| 事实域 | 固定一手定位 | 可支持的主张范围 | 仍需目标环境验证 |
| --- | --- | --- | --- |
| 发行与入口 | [v2026.8.13 release](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.13)、[README.md](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/README.md) | 固定版本身份与公开入口 | 实际安装包、profile 与启用入口 |
| 配置与 provider | [config.py](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/hermes_cli/config.py)、[profiles.py](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/hermes_cli/profiles.py)、[fallback_config.py](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/hermes_cli/fallback_config.py) | 固定版配置、Profile 与 fallback 实现表面 | 有效配置、选择链、数据区域与成本边界 |
| 安全与工具边界 | [SECURITY.md](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/SECURITY.md)、[tool_guardrails.py](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/agent/tool_guardrails.py)、[security_audit.py](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/hermes_cli/security_audit.py) | 安全说明、工具守卫与审计实现入口 | 有效身份、授权、容器、凭证与拒绝负测 |
| Session、Memory 与 Cron 状态 | [session-lifecycle.md](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/docs/session-lifecycle.md)、[memory_provider.py](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/agent/memory_provider.py)、[cron.py](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/hermes_cli/cron.py) | 状态生命周期、记忆 provider 与调度实现表面 | 实际数据库、隔离、保留、恢复与投递 |
| 恢复与迁移 | [session_recovery.py](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/hermes_cli/session_recovery.py)、[config_migrations.py](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/hermes_cli/config_migrations.py) | 固定版 Session 恢复与配置迁移入口 | 真实故障注入、外部副作用对账与回滚 |

上述记录的主事实身份是 `VERSION-FACT`。没有本地 run locator 时不得附加 `LOCAL-VALIDATION`；动态官方架构页只作为 `OFFICIAL-GUIDANCE`，不能覆盖固定提交。

### D.1.3 运行链

固定版本官方架构把多个入口连接到 Agent 运行核心和相应的状态、工具与交付设施。本书用以下通用链定位问题，不要求 Hermes 与 OpenClaw 的内部事件或取消语义同构：

```text
CLI desktop messaging or scheduled entry
  → profile and authorization context
  → messaging gateway or direct runtime entry
  → AIAgent
  → provider resolver and fallback
  → prompt context memory and tools
  → tool or subagent execution
  → session persistence and delivery
```

`AIAgent` 是运行编排核心，不等于模型本身。训练时必须记录实际 provider、fallback、上下文装配、工具循环、重试、压缩和持久化行为。一次回答成功不能证明 Gateway、Session、Memory 或 Cron 的故障边界可靠。

### D.1.4 入口差异

不同入口可能具有不同身份、Session key、数据可见性、交互方式和交付能力。CLI 的本地用户、消息平台 sender、桌面应用用户、Gateway bot 和 Cron job 不应被压成同一“用户”。入口变更后要重测授权、会话隔离、停止和交付。

### D.1.5 Provider 与 fallback

Hermes 的 provider resolver 和 fallback chain 使运行时可以在多个候选间选择，但迁移时必须冻结选择规则。若 fallback 改变模型能力、数据区域、上下文、价格、工具支持或合规边界，它是一次运行条件变化，不是透明容错。可重复基线使用 strict 选择；服务性工作只在预先批准范围内使用 fallback，并记录实际结果。

## D.2 SOUL、USER、MEMORY、AGENTS、Profile 与 OpenClaw 契约对照

七大生命契约是本书的语义模型，不是跨平台七文件标准。迁移时先保留语义，再选择 Hermes 的载体和强制控制。

| 契约语义 | Hermes 可用载体或组合 | 迁移注意 | 不得声称 |
| --- | --- | --- | --- |
| USER | memories 下的 `USER.md` 与当前任务/会话上下文 | 核对写入、快照、撤回和作用域 | USER 是认证或永久授权 |
| SOUL | `$HERMES_HOME/SOUL.md` | 身份、语气和价值规则需与批准机制分开 | SOUL 是沙箱或安全策略 |
| AGENTS | `.hermes.md`、`HERMES.md`、`AGENTS.md` 等项目上下文 | 发现与优先规则需按目标版本验证 | 文本等于组织名册或系统 Policy |
| TOOLS | 项目上下文、配置和 toolsets 的组合 | 重新建立真实工具、范围和审批 | 复制工具说明即可获得能力 |
| IDENTITY | Profile 与 SOUL 的组合映射 | 运行资产隔离、人格与授权身份分开 | Profile 是强安全沙箱或法律身份 |
| HEARTBEAT | Cron、Gateway 调度和通知策略的组合 | 重建节律、静默、熔断、批准和恢复 | 存在同名契约文件或天然主动性 |
| MEMORY | memories 文件、memory 工具和写入审批 | 核对来源、快照、搜索、纠错、删除 | 一个文件覆盖全部记忆生命周期 |

### D.2.1 Profile 的准确边界

Profile 可隔离配置、SOUL、memories、sessions、skills、cron 和其他运行资产，但不应被称为容器、OS 隔离或多租户安全边界。不同 Profile 是否共享进程、宿主文件、网络、凭证池或工具 backend，要在实际部署中验证。

切换 Profile 不是只换人格。岗位、数据根、Session、Memory、Skill、Cron、工具和凭证都要同步变化。若只换名称和 SOUL，仍继承上一岗位的外发工具或客户数据，迁移判 `FAIL`。

### D.2.2 契约迁移的四层检查

1. 语义层：目标、禁止项、冲突、停止和完成是否保留。
2. 载体层：目标平台是否实际发现和加载相应内容。
3. 状态层：Session、Memory、Cron 和未决任务是否迁移或隔离。
4. 强制层：身份、Tool policy、审批、容器、凭证和外部权限是否等价或更严。

四层任何一项未知，结论为 `REVIEW_REQUIRED`。用更强烈的 SOUL 措辞不能补上工具或凭证控制缺口。

## D.3 Session、SQLite FTS5、Memory Provider、Compression 与持久化

### D.3.1 Session 与搜索

Hermes 使用 SQLite 等持久状态，并可通过 FTS5 支持会话搜索。数据库存在不意味着所有状态都已持久化，也不意味着索引、原始内容、附件、Cron、外部效果和备份属于同一删除范围。

每个 Session 评测至少记录：Profile、入口、平台身份、session key、父子谱系、创建和更新时间、压缩事件、工具执行、交付、保留和删除策略。消息平台之间即使内容相同，也不应默认共享 Session。

### D.3.2 Memory Provider 与冻结快照

Hermes 的记忆实现强调有界、整理后的长期记忆，并可在会话开始时形成使用快照。快照改善运行稳定性，却会引入时效问题：会话开始后用户撤回或纠正的内容，是否能立刻使旧快照失效，需要明确的状态传播和测试。

记忆写入应区分候选、批准、已生效、被替代、撤回和删除。Memory 工具的写入审批只覆盖相应操作；它不自动证明来源真实、内容适用或所有副本已删除。

### D.3.3 Compression

上下文压缩是运行行为，不是无损存档。压缩可能丢失限制、未决项、引用位置或否定条件。评测应保留压缩前后 digest、策略、触发原因、保留对象和恢复路径，并用边界样本检查授权、数字、日期、禁止项和 `UNKNOWN` 没有被改写。

### D.3.4 持久化与恢复

恢复时分别对账 Session 数据库、Memory、Cron ledger、文件产物、工具副作用和外部交付。重启后进程恢复不代表任务状态一致；数据库回滚也不撤销已发送消息或已修改外部系统。

## D.4 Tools、MCP、Skills、Plugins、Cron、Gateway 与 Delegation

### D.4.1 Tools 与 backend

Hermes 的工具能力可能落在本地终端、容器、浏览器、MCP、专用集成或其他 backend。每个 Tool 都要记录执行位置、身份、文件和网络范围、危险动作审批、receipt、停止和补偿。Tool Registry 或 schema 只说明能力可发现，不证明当前主体有权执行。

### D.4.2 MCP

MCP 的 Host、Client、Server、tool、resource 和 prompt 边界在 Hermes 中仍需服从本地身份、scope、批准和凭证过滤。连接 Server 成功不能证明 Server 可信；MCP 环境变量过滤也不能证明秘密不会从文件、日志、参数或工具结果进入模型。

### D.4.3 Skills 与 Plugins

Skill 适合封装渐进加载的知识、流程、资源和脚本。安装或激活前要审查来源、版本、脚本、副作用、依赖、工具要求和数据流。Plugin 或更深运行时扩展可能拥有比 Skill 更大的执行面，不能只按说明文档审查。

平台间迁移 Skill 时，先迁移任务合同和资源，再重新验证目录发现、frontmatter、脚本运行时、相对路径、工具名、权限和失败处理。文件格式兼容不能替代行为回归。

### D.4.4 Cron 与 Gateway 调度

Cron 是时间触发机制，不等于本书的 HEARTBEAT 契约。一个主动任务还需要：观察对象、价值阈值、静默规则、去重、风险状态、审批、失败预算、暂停、恢复、交付和审计。迁移后所有任务先保持暂停，在合成环境验证错过、重复、并发、时区和重启恢复。

### D.4.5 Delegation

Delegation 使主 Agent 把有界任务交给 subagent，但不自动建立信任。委派合同至少包含父任务、子任务、输入切片、允许工具、禁止项、预算、完成谓词、Handoff、停止和结果归属。

子 Agent 的工具继承必须显式验证。若父 Agent 没有某项权限，子 Agent 不能通过角色变化获得；若子 Agent 权限更窄，主 Agent 也不能在结果不完整时静默代做高风险步骤。委派链中的 unknown parent、循环委派、孤儿结果和无法定位的责任都应 fail closed。

## D.5 安全审批、容器、凭证过滤、跨会话隔离和输入清洗

### D.5.1 安全控制分层

| 控制 | 作用 | 不能替代 |
| --- | --- | --- |
| allowlist 或 pairing | 限制入口主体 | 工具级授权、客户数据 scope |
| dangerous-command approval | 对危险动作进行确定性确认 | 普通工具策略、外部系统权限 |
| write safety | 限制写入路径或类型 | 完整容器、网络隔离、审批 |
| container backend | 限制进程、文件、网络和资源 | 身份、凭证最小化、业务授权 |
| credential filtering | 降低秘密进入不必要上下文或子进程 | 轮换、撤销、出口代理和残留清理 |
| profile isolation | 分隔运行资产和状态 | 不可信租户的强安全边界 |
| input sanitization | 减少已知恶意或异常输入 | 对提示注入的完整防御 |

### D.5.2 容器与宿主

容器是否启用、覆盖哪些 Tool、挂载哪些路径、网络如何限制、backend 失败时是否回落宿主，都要由实际证据回答。安全要求为“必须容器化”时，backend 不可用应拒绝运行，不能为了完成任务切换到 host。

### D.5.3 凭证过滤

凭证应以不可逆 handle 或受控引用进入任务，真实值只在必要执行边界解析。过滤变量名不是完整控制；秘密可能存在于配置、历史文件、shell、浏览器、日志、错误、MCP env、工具输出和子 Agent 上下文中。迁移前需要清点、轮换和撤销，不复制源环境 `.env`。

### D.5.4 跨会话隔离

测试至少包含：不同用户、不同平台、不同 Profile、父子 Agent 和 Cron 任务之间的数据不可见性；旧 Session 摘要不进入新主体；撤回后新运行不再读取旧内容；搜索结果保留主体和来源过滤。仅用两次正常对话不能证明隔离。

### D.5.5 输入清洗与提示注入

输入清洗适合处理结构、大小、编码、危险附件和已知模式，但无法保证识别所有提示注入。来自网页、邮件、文件、MCP resource、tool output 和其他 Agent 的内容都作为不可信数据；模型拒绝只是最后一道行为表现，真实边界由工具范围、容器、审批、秘密和出口控制承担。

## D.6 原则可迁移、配置不可直译和差异验证清单

### D.6.1 六步迁移协议

1. 冻结源系统主体、版本、任务、风险、数据、工具、状态和证据。
2. 把 OpenClaw 文件与组件还原为七契约语义、运行需求和强制控制需求。
3. 在 Hermes 中做组合映射，允许一对多、多对一、`UNSUPPORTED` 和 `NOT_APPLICABLE`。
4. 为身份、状态、权限、执行位置、交付和恢复建立差异表。
5. 在暂停和最小权限下运行正常、冲突、越权、撤回、故障与恢复测试。
6. 输出限制、降级、未知、回滚和再评测范围，由独立角色批准上线。

### D.6.2 迁移差异矩阵

```yaml
migration_item:
  item_id: MIG-0001
  source_object: ""
  source_version: ""
  source_semantics: []
  source_controls: []
  source_state_refs: []
  target_objects: []
  target_version: ""
  mapping: EQUIVALENT | RESTRICTED_EQUIVALENT | COMPOSITE | UNSUPPORTED | UNKNOWN
  semantic_gaps: []
  control_gaps: []
  state_migration: []
  tests: []
  rollback_ref: ""
  decision: PASS | FAIL | REVIEW_REQUIRED
```

### D.6.3 必测差异

- SOUL、USER、项目上下文和 memories 是否按目标版本实际加载；
- Profile 切换是否同时改变状态、Skill、Cron、工具和凭证边界；
- Session key、平台隔离、父子谱系和搜索过滤是否符合声明；
- Memory 快照能否响应撤回、纠错、删除和跨会话隔离；
- Provider strict/fallback 是否可定位并遵守数据、能力和成本边界；
- Tool backend、容器、文件、网络和审批是否 fail closed；
- MCP Server、Skill、Plugin 和依赖是否固定来源并通过供应链审查；
- Cron 是否可暂停、去重、恢复，并在无价值变化时保持安静；
- subagent 是否只获得任务所需权限，Handoff 是否闭合；
- Gateway 或运行时重启后，Session、Cron、未决执行和 delivery 能否对账；
- 凭证是否完成重新引用、过滤、轮换和旧副本撤销；
- 迁移后的产物、交付可见性和业务终态是否与源系统范围等价。

### D.6.4 允许的迁移结论

- `PASS`：声明范围内的语义、状态和强制控制均有目标环境证据；降级、排除、人工补偿与未覆盖面写入独立的 `scope` 和 `limitations` 字段，不另造第四种裁决。
- `FAIL`：出现越权、串扰、状态丢失、错误交付、不可恢复副作用或关键语义缺失。
- `REVIEW_REQUIRED`：加载、权限、外部终态或恢复证据不足。

全书裁决语言只有 `PASS`、`FAIL`、`REVIEW_REQUIRED` 三态。一个带限制的 `PASS` 仍必须明确声明验证范围；限制触及硬门、证据完整性或结论成立条件时，应改判 `FAIL` 或 `REVIEW_REQUIRED`，不能用措辞降级来维持通过。

“配置已导入”“Agent 能回答”“文件都存在”均不是迁移成功。真正的成功是：同一岗位在 Hermes 的目标边界内完成任务，旧权限没有被意外继承，失败能停止并恢复，证据足以让非作者复核。

### D.6.5 硅基仿生镜头

跨 Runtime 迁移可以类比器官移植，但这种类比只帮助理解排异检查：语义是功能要求，状态是连续性，接口是连接方式，权限和隔离是免疫边界，回归测试是术后观察。它不意味着 Agent 具有生物生命、主观体验或人格延续。

把同一 SOUL 搬到 Hermes，也不意味着“同一个生命”无损迁移。模型、Runtime、上下文、状态、工具、入口和权限共同决定行为。出版与工程表述应写“在声明范围内迁移了岗位语义与可验证能力”，不能写“意识、人格或记忆完整转生”。

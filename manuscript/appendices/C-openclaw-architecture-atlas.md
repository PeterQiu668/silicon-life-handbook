---
appendix_id: C
title: OpenClaw 系统架构图谱
status: formal_candidate
audiences: [trainer, engineer, operator, security_reviewer, agent]
depends_on: [C05, C06, C13, C14, C15, C16, C22, C23, C24]
platform_baseline:
  product: OpenClaw
  version: 2026.9.6
  commit: eb377ac59e6c9fd6c7705028034812becf00271b
verified_on: 2026-10-01
---

# 附录 C　OpenClaw 系统架构图谱

本附录是全书的 OpenClaw 固定版本实现图。正文负责讲可跨平台迁移的训练原理，本附录负责回答这些原理在 OpenClaw `2026.9.6`、提交 `eb377ac59e6c9fd6c7705028034812becf00271b` 中落在哪些组件、状态和控制上。版本或提交发生变化时，应先复核本附录，再使用其中的命令、字段和默认行为。

这不是安装教程，也不是把所有功能同时打开的建议。一个岗位只应装配完成任务所需的最小组件。OpenClaw 的 trusted-operator、local-first 信任模型不等于多租户隔离；模型和外部内容仍应视为不可信执行输入。固定来源入口见 [SOURCES.md](../../SOURCES.md)，完整运行容器解释见第 6 章。

## C.1 固定版本、提交、官方文档映射与可验证命令

### C.1.1 固定基线

| 对象 | 本书基线 | 证据用途 | 失效触发器 |
| --- | --- | --- | --- |
| OpenClaw 发行 | `2026.9.6` | 命令、组件、状态和控制事实 | stable/latest 变化或安全公告 |
| 源码提交 | `eb377ac59e6c9fd6c7705028034812becf00271b` | 固定文档和源码定位 | tag 移动、补丁或 fork 差异 |
| 核验日 | `2026-10-01` | 动态文档和外部依赖时间边界 | 出版、再版或部署前复核 |
| 当前最新发行快照 | `2026.9.7` / `c074824a27c96d3983043f9eeb33823cd1772d8c` | 只用于识别升级差异 | 不自动替换书稿固定基线 |
| 本书事实身份 | `VERSION-FACT`、`LOCAL-VALIDATION`、`OFFICIAL-GUIDANCE` | 区分实现、复现和官方说明 | 证据来源或环境变化 |

本机命令的输出只能证明该主机在该时间的状态。运行前应保存命令、版本、目标配置根、敏感信息脱敏规则和输出 digest。若本机安装与本书固定版本不同，不得把差异自动解释为错误；先检查发行说明、迁移文档和配置 schema。

### C.1.2 影响配置、安全、状态与恢复的固定来源映射

以下定位全部固定到 `eb377ac59e6c9fd6c7705028034812becf00271b`。它们证明的是该提交中的文档或源码事实，不证明目标部署已经启用相同配置，也不替代本机只读核验。

| 事实域 | 固定一手定位 | 可支持的主张范围 | 仍需目标环境验证 |
| --- | --- | --- | --- |
| 发行与总体架构 | [v2026.9.6 release](https://github.com/openclaw/openclaw/releases/tag/v2026.9.6)、[architecture.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/architecture.md)、[agent-runtime-architecture.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/agent-runtime-architecture.md) | 固定版本身份、Gateway 与 Runtime 组件关系 | 实际启用组件、入口与运行参数 |
| 配置与扩展 | [config-tools.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/config-tools.md)、[skills.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/tools/skills.md)、[automation/index.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/automation/index.md) | 配置表面、Skill 与自动化对象 | 有效配置、发现顺序、依赖与副作用 |
| 安全与隔离 | [SECURITY.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/SECURITY.md)、[trust-model.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/security/trust-model.md)、[modes-scope-and-backend.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/sandboxing/modes-scope-and-backend.md) | 信任模型、沙箱模式、范围与后端的产品语义 | 身份、有效 Policy、backend 可用性与 fail-closed 负测 |
| 状态与记忆 | [agent-workspace.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/agent-workspace.md)、[memory-provenance.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/memory-provenance.md)、[integrity-and-recovery.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/reference/database-schemas/integrity-and-recovery.md) | Workspace、记忆来源、数据库完整性与恢复边界 | 当前 schema、写入者、备份覆盖面与删除残余 |
| 诊断、备份与恢复 | [backup.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/cli/backup.md)、[doctor/recovery.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/cli/doctor/recovery.md)、[restart-recovery.md](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/restart-recovery.md) | 固定版诊断、备份与恢复入口 | 可恢复性演练、外部副作用对账与恢复时间 |

主事实身份为 `VERSION-FACT`；官方解释可另记 `OFFICIAL-GUIDANCE`。只有保存目标环境、命令、输入、输出与 digest 的运行，才可另立 `LOCAL-VALIDATION` 记录。

### C.1.3 安全的只读核验顺序

1. 确认二进制、版本、安装来源和实际配置根。
2. 读取状态与诊断，不先执行自动修复。
3. 列出 Agent、Workspace、Channel、Account、Binding、Node、Plugin、Skill、Automation 和有效 Tool profile。
4. 检查 Gateway、数据库、队列、交付和外部依赖健康。
5. 执行安全审计并保存 finding、扫描范围和未覆盖面。
6. 对高风险路径运行受控负例，证明拒绝、停止和恢复发生在系统边界。

命令名称和参数必须以当前固定版本的 `--help` 和官方文档为准。示例文档中的命令若未经目标环境复现，应标为待核验，不直接进入生产脚本。任何会写配置、修复权限、迁移 schema、重启 Gateway、撤销身份或触发外部动作的命令，都不属于“只读核验”。

### C.1.4 版本证据包

```yaml
openclaw_baseline:
  captured_at: ""
  host_ref: ""
  binary_path: ""
  version_output: ""
  package_or_release_ref: ""
  commit: ""
  config_root_ref: ""
  state_root_ref: ""
  schema_version: ""
  enabled_surfaces: []
  command_transcript_ref: ""
  redaction_report_ref: ""
  digest: "sha256:"
```

## C.2 Gateway、WS/RPC、客户端、事件与控制平面

Gateway 是 OpenClaw 的长驻控制与协调入口。客户端、Channel、Node 和其他控制表面通过相应连接进入；Gateway 接纳请求、关联身份与状态、启动 Agent 运行、路由事件并协调交付。它不是模型，也不应被描述成整个 Agent 的“大脑”。

一次进入控制平面的请求至少需要六个可定位对象：连接主体、入口类型、请求或消息 ID、目标 Agent 或 Binding、Session/run ID、接纳结果。只有聊天文本而没有这些对象，无法在重复、乱序、超时或重启后可靠对账。

```text
Client or Channel
  → connection authentication
  → admission and deduplication
  → account sender and binding resolution
  → session and queue selection
  → agent run
  → event stream and delivery
  → authoritative end state
```

### C.2.1 控制平面边界

- Gateway 可协调多个表面，但不把所有表面合成同一身份。
- WebSocket 或 RPC 连接成功，只证明连接层通过，不自动授予 Tool、Node 或外部系统权限。
- 客户端等待超时不表示后台 run 已停止；停止需要命中真实运行和执行位置。
- Gateway 重启后的恢复依赖持久状态、队列、receipt 和外部事实，不依赖模型自述。
- 同一 Gateway 信任域内的不同 Workspace 或 Agent，不自动构成对不可信租户的强隔离。

### C.2.2 最小控制面证据

| 阶段 | 最少记录 | 失败时的安全动作 |
| --- | --- | --- |
| 连接 | client/device identity、认证结果、协议版本 | 拒绝未知主体，不猜测身份 |
| 接纳 | ingress ID、去重键、目标、预算 | 不明去重状态时暂停高风险重试 |
| 路由 | Account、sender、Binding、Agent、Session | 映射冲突进入 `REVIEW_REQUIRED` |
| 运行 | run ID、队列、Provider、Tool、执行位置 | stop/interrupt 命中实际 run |
| 交付 | artifact、delivery receipt、可见性 | 未交付不得自报完成 |
| 恢复 | durable state、外部终态、补偿决定 | `UNKNOWN` 先对账再重试 |

## C.3 Agent Runtime、Loop、Prompt Context Assembly、Model Provider 与 Failover

Agent Runtime 把岗位与生命契约、当前任务、Session 状态、Memory、Skill、Tool schema 和运行策略装配成一次受控运行。模型是认知组件，Runtime 才负责循环、状态转换、工具往返、预算、停止和错误处理。

### C.3.1 上下文装配清单

每次可复现运行应记录实际装配，而不是只保存理论配置：

- Agent ID、岗位版本和生命契约版本；
- 用户、项目、任务和数据作用域；
- Session 摘要、Memory 查询与来源；
- 已加载 Skill 及版本；
- 可见 Tool、schema 和有效策略；
- Model、Provider、profile、参数和选择来源；
- 预算、时限、停止条件和输出 schema；
- 被省略、压缩、截断或拒绝加载的内容。

系统提示词正确不代表实际上下文正确。装配顺序、压缩、缓存、Skill 激活、Memory 检索和 Provider 能力差异都可能改变结果。

### C.3.2 Provider 选择与故障转移

Provider 配置应区分 `strict` 与有界 fallback。严格复现实验通常固定 Model 和 Provider；普通服务可在预先批准的候选内故障转移，但必须记录实际选择、成本、数据边界和能力差异。

当 fallback 会改变数据区域、模型能力、工具支持、上下文窗口、价格或合规边界时，它不是透明重试。应重新检查任务是否仍在授权范围内。Provider 限流、认证失败、模型拒绝、上下文超限和工具循环失败也应分开分类，不能统一记为“模型不行”。

### C.3.3 Loop 的停止语义

运行循环至少要区分：正常完成、等待 Tool、等待审批、等待外部事件、被取消、预算耗尽、执行失败和终态未知。停止模型生成不一定停止已经提交的工具或外部动作；中断 observer 也不一定中断 worker 或 Node。高风险系统应保存 run、tool execution 和 external effect 三个层级的停止证据。

## C.4 Workspace、Session、Memory、Queue、SQLite 与状态流

### C.4.1 状态对象不能互换

| 对象 | 主要职责 | 不是 |
| --- | --- | --- |
| Workspace | 受管理的文件、项目规则和工作产物 | 安全沙箱、数据库或永久记忆 |
| Session | 一段交互或运行的上下文与身份边界 | 用户全部历史或授权根 |
| Transcript | 可追溯的消息与运行记录 | 完整外部终态 |
| Memory | 经治理的可召回长期信息 | 所有会话的无条件复制 |
| Queue | 等待、顺序、并发和背压状态 | 无限容量或可靠交付证明 |
| SQLite 状态 | 多类持久事实的实现载体 | 自动等于一致、备份或可恢复 |
| Receipt | 接受、执行或交付证据 | 默认等于业务结果 |

### C.4.2 状态所有权

每种状态都要有 writer、reader、retention、backup、restore 和 deletion owner。Workspace 文件可以由用户编辑，数据库状态由运行时维护，外部系统结果由外部系统拥有；恢复时不能让一个较弱事实覆盖更权威事实。

Memory 的来源、准入、检索、更正、过期和删除要分开治理。停止未来摄入不等于删除已经形成的 Memory；删除 Memory 也不自动删除原始 Session、Transcript、备份和自由写入的副本。删除请求必须列出覆盖范围和残余范围。

### C.4.3 Queue 与背压

Channel adapter、Gateway、Session lane、Provider、Node 和 delivery 都可能排队。每个等待面至少声明容量、等待预算、拒绝方式、去重边界和 drop signal。静默丢失比明确失败更危险；系统若不能说明任务在哪里，应暂停同类副作用动作并对账。

训练评测必须把基础设施拥塞与能力失败分开。单 Session 串行、Provider 429、Node 离线和 delivery 重试会改变延迟与完成率，但不应被误写为推理质量变化。

## C.5 Channels、Accounts、Pairing、Bindings、Delivery 与 Retry

消息面负责把外部平台身份与内部 Agent 运行连接起来。`Channel` 表示入口类型，`Account` 表示具体连接身份，`Pairing` 或准入规则决定谁可进入，`Binding` 决定流量去向，`Session` 承载相应状态，`Delivery` 负责把结果送出。它们是不同控制点。

### C.5.1 身份连续链

```text
platform event
  → channel account
  → sender identity
  → pairing or allowlist
  → binding
  → agent and session
  → policy and approval
  → outbound account
  → delivery receipt
```

Binding 只说明路由，不授予目标 Agent 的全部权限。正确 sender 被正确路由后，外发、修改或支付等动作仍要通过 Tool policy、对象绑定审批和外部系统权限。

### C.5.2 重试与幂等

入站平台、内部 Queue、Tool API 和出站平台可能各自重试。幂等键必须绑定真实副作用对象，不能只绑定自然语言请求。出现“请求已接受但 receipt 丢失”时，应查询外部系统，不应换 ID 盲重试。

编辑、撤回和乱序也要有明确语义：编辑是更新原任务还是新输入；撤回是否只停止后续动作；窗口关闭后如何处理迟到事件。模型不应自行猜测事件顺序或撤回已经发生的副作用。

## C.6 Tools、Browser、Nodes、Cloud Workers、MCP 与执行位置

行动面回答“变化在哪里发生”。Tool schema 只定义调用形状；真正边界还包括执行主机、身份、Policy、Approval、Sandbox、网络、秘密和终态 readback。

| 执行位置 | 适合 | 主要风险 | 最小证据 |
| --- | --- | --- | --- |
| Gateway host | 控制与可信轻量工具 | 爆炸半径大、共享宿主状态 | host identity、effective policy、终态 |
| Tool Sandbox | 不可信输入和受限执行 | backend fail-open、scope 或 mount 过宽 | backend、scope、workspace access、deny 负例 |
| Browser | 网页状态和人工接管 | cookie、提示注入、表单副作用 | profile、账户、URL、批准、页面与网络终态 |
| Node | 特定设备或主机能力 | 设备身份、断线、本地权限 | pairing、capability、run plan、本地主机 receipt |
| Cloud Worker | 临时计算与隔离批处理 | 秘密、网络、回收前未知副作用 | lease、输入切片、输出、销毁与对账 |
| MCP Server | 外部 tools、resources、prompts | confused deputy、schema 漂移、token 误用 | server identity、capability、scope、探测与调用证据 |

Node 是外围执行端点，不是 Gateway 或子 Agent。Node 断线时不得把任务静默迁移到 Gateway host。Browser 的隔离 profile、个人已登录 profile、Node 浏览器和远端浏览器也不是同一种权限边界。

Plugin 与 MCP Server 不同。固定版 Plugin 在 Gateway 进程内属于可信代码和供应链面，可注册 Tool、Channel 等能力；普通工具沙箱不自动隔离 Plugin。安装来源、版本、发现根、启用状态和重启要求都要纳入变更审查。

### C.6.1 行动结果五态

- `NOT_STARTED`：尚未到达执行边界。
- `DENIED`：被身份、Policy、Approval 或边界拒绝。
- `SUCCEEDED`：权威终态证明目标已达到。
- `FAILED`：确认未达到目标，且副作用范围已知。
- `UNKNOWN`：可能已经执行，但 receipt 或外部事实不足。

`DENIED` 是治理结果，不等于系统故障；`UNKNOWN` 不能被自动重试洗成成功。

## C.7 Skills、Plugins、Hooks、Webhooks、Cron、Heartbeat 与 Standing Orders

### C.7.1 七类扩展与触发对象

| 对象 | 解决的问题 | 关键边界 |
| --- | --- | --- |
| Skill | 按需装配程序性知识、资源和脚本 | 内容可信度、版本、激活和工具权限分开 |
| Plugin | 扩展 Gateway 或产品能力 | 可信代码、供应链、同进程影响与重启 |
| Hook | 在生命周期事件点执行逻辑 | 事件来源、顺序、失败和重复 |
| Webhook | 接受外部网络事件 | 身份、签名、重放、schema 和流量控制 |
| Cron | 按时间表达式触发 | 时区、错过、重复、并发和暂停 |
| Heartbeat | 周期性检查或主动信号 | 无变化静默、噪音预算和停止条件 |
| Standing Order | 在范围和时窗内持续有效的任务合同 | 不是永久授权，需撤销、复核和证据 |

Skill 的文本可以影响行为，但不能自行创造系统权限。Plugin 的能力更接近运行时扩展，审查标准应高于普通说明文件。Hook、Webhook、Cron 和 Heartbeat 都可能触发同一动作，必须在统一任务账本中去重和限流。

固定版工作区文档已经退役 `TOOLS.md` 与 `HEARTBEAT.md` 的历史同名模板。本书仍保留 TOOLS 与 HEARTBEAT 作为两类治理语义：工具意图可以落在 `AGENTS.md` 的工具段和系统配置中，主动节律可以落在 Automation、Hook、Webhook、Cron 或其他调度对象中。方法名称不等于当前版本必须存在同名文件。

## C.8 Auth、Policy、Approval、Sandbox、Secrets、Audit 与 Trust Boundary

### C.8.1 七个治理坐标

1. `Authentication` 说明当前主体是谁。
2. `Policy` 计算系统允许、拒绝或升级的范围。
3. `Approval` 让有权主体对精确对象、影响、时窗和版本作决定。
4. `Sandbox` 限制执行的文件、网络、进程、设备和资源影响。
5. `Secrets` 管理引用、解析、注入、轮换、撤销和残留。
6. `Audit` 保存可追溯事实并发现异常。
7. `Recovery` 对账持久状态和外部终态，决定继续、补偿或终止。

控制按交集生效，每层只收紧，不隐式放宽。聊天中的“可以”不能恢复 Policy deny；Workspace 约定不能替代 Sandbox；SecretRef 不能自动清理旧日志或脚本中的明文；security audit 无 finding 不能签发“安全”结论。

### C.8.2 多身份面

Gateway 客户端、Channel sender、Channel Account、Provider profile、Node device、Browser account、MCP Server 和外部 Tool 都可能有独立身份。共享一个 token 会扩大爆炸半径，也会让事故无法判断哪个主体实际行动。

### C.8.3 批准必须绑定的对象

敏感批准至少绑定：请求主体、目标、动作、参数或内容 digest、执行位置、凭证引用、有效期、最大次数、预算、撤销方式和批准人。命令、脚本、目标文件或消息内容改变后，原批准不应继续覆盖。

### C.8.4 Sandbox 四个问题

“启用了沙箱”还不够。必须说明哪些 Tool 进入沙箱、scope 是 agent/session/shared 中哪一种、使用哪个 backend、Workspace access 是 none/ro/rw 中哪一种。强制隔离后 backend 不可用时应 fail closed，不能静默落回 host。

## C.9 Doctor、Health、OTel、Prometheus、Backup、Recovery 与 Guarded Upgrade

诊断、健康、观测、备份和升级解决不同问题。Doctor 发现配置和依赖问题；health 说明当前组件是否可响应；OpenTelemetry 与 Prometheus 提供运行事件和指标；backup 保存可恢复状态；recovery 对账并恢复；guarded upgrade 管理版本、schema 和回退边界。

### C.9.1 观测最小对象

- ingress、session、run、model/provider；
- queue、tool、approval、execution host；
- artifact、delivery、external readback；
- token、费用、延迟、错误、重试和恢复；
- Agent、Skill、Plugin、policy 和 schema 版本。

OpenTelemetry GenAI 语义仍会变化，因此正文固定观察对象和关联关系，不把某一批字段名写成永久标准。指标适合趋势与告警，trace 适合单次因果调查，审计记录适合责任与合规；三者不能互相替代。

### C.9.2 恢复顺序

```text
freeze admission
  → stop or drain affected runs
  → terminate the actual execution location
  → inspect durable state and receipts
  → query authoritative external systems
  → classify side effects as known or unknown
  → continue compensate retry manually or tombstone
  → restore service under a bounded scope
  → run negative regression before reopening
```

代码回滚不自动回滚 SQLite schema、Queue、Delivery、Cron 或外部状态。备份可读取也不等于可恢复；恢复演练必须在隔离环境验证数据、版本、权限和未决副作用。

### C.9.3 受保护升级

升级前保存版本、配置、schema、状态和外部未决动作；识别不可逆 migration；先在影子或隔离环境运行基线与负例；灰度时限制主体、工具和数据；达到停止条件立即冻结新接纳；升级后重跑身份、Binding、Provider、Tool、Sandbox、恢复和交付链。出现重大变化时触发第 24 章再认证。

## C.10 CLI、Control UI、Voice、Media 与其他快速变化产品表面

CLI、Control UI、Voice、Media 和其他产品表面是同一控制与运行系统的不同入口，不是不同安全模型。它们可以改善操作体验，却不能越过身份、Policy、Approval、状态和审计。

### C.10.1 表面级检查

| 表面 | 额外风险 | 验证重点 |
| --- | --- | --- |
| CLI | shell 环境、cwd、脚本注入、输出泄密 | 二进制来源、目标根、非交互安全、退出码与变更终态 |
| Control UI | UI 状态与后端状态不一致 | 请求 ID、刷新后状态、权限、失败和只读边界 |
| Voice | 误识别、说话人混淆、环境泄露 | 明示确认、敏感动作复述、可取消、文字审计记录 |
| Media | 隐写提示、元数据、隐私和大文件 | 来源、解析隔离、内容扫描、保存和删除范围 |
| Browser | 页面注入、cookie、跨域和不可逆提交 | profile、账户、域、批准、网络与页面终态 |

快速变化表面应在出版或部署前通过当前 `--help`、官方文档和受控本地测试复核。书中若未证明某个表面的行为，应写为 `REVIEW_REQUIRED`，不从邻近表面类推。

## C.11 从架构到训练的最小装配

一个可训练的 OpenClaw 单体至少包含：一个人类 owner、一个明确信任域、一个 Gateway 或控制入口、一个 Agent ID、一个 Workspace、一个岗位模型、一组生命契约、一个 primary Provider、一个私有 Session、最小 Tool profile、强制 Policy/Sandbox/Approval、持久状态、观察接口和停止人。Channel、Node、Browser、Worker、MCP 或主动调度只在岗位需要时加入。

### C.11.1 六项健康门

- 控制健康：入口可认证，版本、接纳和停止事实可见。
- 认知健康：实际 Model、Provider、上下文和 fallback 可见。
- 状态健康：Workspace、Session、Memory、数据库和恢复点有 owner。
- 消息健康：准入、Binding、Queue、Delivery 和 receipt 可追踪。
- 行动健康：Tool 的执行位置、Policy、Approval、Sandbox 和终态由正负例证明。
- 治理健康：秘密不进入训练材料，审计已复核，停止与恢复已演练。

六项不取平均。未授权外发、数据越界、Sandbox fail-open、重复副作用或恢复证据缺失直接 `FAIL`；版本、身份或外部终态未知则 `REVIEW_REQUIRED`。

### C.11.2 硅基仿生镜头

Gateway 和 Channel 可类比信号接入与协调，Runtime 和 Model 可类比认知加工，Tool、Browser、Node 和 Worker 可类比执行器官，Workspace、Session、Memory 和数据库可类比不同时间尺度的状态，Policy、Approval、Sandbox、Audit 与 Recovery 可类比边界、警报和复原机制。

这个比喻只用于识别职责。Gateway 不是大脑，Queue 不是潜意识，Memory 不证明主观记忆，自动恢复也不是生命自愈。系统没有因这套架构获得意识、人格、痛觉或法律主体资格；责任仍由设计、部署、授权和运营它的人与机构承担。

### C.11.3 架构变更后的必跑负例

- 未知 client、sender、Account 或 device 是否被拒绝；
- 正确路由但未获批准的敏感 Tool 是否被拒绝；
- Sandbox backend 故障是否 fail closed；
- Node 断线是否阻止执行位置漂移；
- Provider fallback 是否遵守数据、能力和成本边界；
- Queue 或 delivery 不确定是否阻止重复副作用；
- Plugin、Skill 或 MCP schema 漂移是否触发重新审查；
- Gateway 重启与版本升级后，旧任务、receipt 和外部终态能否对账；
- 撤销身份、审批或 Standing Order 后，后续触发是否真正停止；
- Audit 缺失或证据 digest 不匹配时，系统是否拒绝继续认证。

本附录提供组件定位和复核问题，不提供“一套配置适合所有岗位”的答案。若某组件无法证明其业务必要性、风险边界和恢复路径，应从最小单体中移除或停留在只读、草拟和人工批准层。

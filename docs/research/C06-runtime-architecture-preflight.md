# C06 运行容器与系统架构前置研究包

> 状态：`research_preflight`，不是 C06 正文，不代表架构冻结或章节完成。  
> 核验截点：2026-09-30。  
> OpenClaw 固定基线：`v2026.9.6` / `eb377ac59e6c9fd6c7705028034812becf00271b`。  
> Hermes 固定发布锚点：`v0.20.1` / release tag `v2026.8.13`；官网开发者文档另按“动态文档”处理。  
> Muse：只使用 Meta 官方发布与安全说明，所有实现描述均标为 `VENDOR-CLAIM`。  
> 用途：为 C06 作者、事实审稿者、架构制图者和故障演练设计者提供可追溯底稿。

## 0. 研究边界与证据规则

### 0.1 本文回答什么

本文只回答七件事：

1. 本书拟用的“控制、认知执行、状态、消息、行动、治理”六层分析框架，能否完整容纳 OpenClaw `v2026.9.6` 的关键运行组件；
2. 每个组件究竟是什么、在哪里执行或持久化、跨过什么信任边界；
3. 出错后怎样暴露，怎样停止，什么可以自动恢复，什么必须人工核对；
4. 哪些概念由 C06 定位，哪些必须让给 C13、C14、C16、C20、C22 等后章定义；
5. Hermes 可作为怎样的第二实现映射，而不被伪装成 OpenClaw 同构；
6. Muse Secure VM 能提供什么产品镜面，哪些内容仍只是厂商自述；
7. C06 正式开写前，C04/C05 必须交付哪些输入。

本文不定义 C13 的记忆生命周期、C14 的工具/MCP 契约、C16 的主动调度、C20 的跨 Agent 路由与 Handoff、C22 的完整威胁模型，也不为 C06 产物或正文预先签发通过状态。

### 0.2 证据标签

| 标签 | 含义 | 正文使用规则 |
|---|---|---|
| `STABLE-PRINCIPLE` | 跨产品相对稳定的工程原则 | 可用于方法论，但仍应给出适用边界 |
| `VERSION-FACT` | 固定版本、固定提交或固定发布页支持的事实 | 必须带版本与核验日期 |
| `DYNAMIC-DOC` | 官网当前文档事实，但未证明属于指定历史 release | 可用于当前映射；不得回填为历史版本事实 |
| `VENDOR-CLAIM` | 厂商对闭源产品的架构、安全或效果声明 | 必须保留标签，不得改写为独立验证结论 |
| `METHODOLOGY` | 本书为教学、制图或验收建立的方法 | 不得冒充平台官方分层 |
| `INFERENCE` | 由多条事实推导出的设计判断 | 必须显式说是推断，并允许后续审校推翻 |
| `UNKNOWN` | 当前证据不足、实现动态或未做运行试验 | 不得补写成肯定事实 |

### 0.3 基线校验

本机只读核验得到：

```text
$ openclaw --version
OpenClaw 2026.9.6 (eb377ac)

$ hermes --version
Hermes Agent v0.20.1 (2026.8.13)
```

本机 OpenClaw npm 包 `package.json` 同时给出 `name=openclaw`、`version=2026.9.6`、官方仓库 `https://github.com/openclaw/openclaw.git`。固定提交页与 release 页可公开复核，故本文关于 OpenClaw 的组件事实优先引用固定 SHA 文档，而不是会继续变化的官网首页。[OC-REL][OC-ARCH]

Hermes 的发布页只证明 `v0.20.1`、发布日期与发布提交 `f80f453`；本文引用的架构、Provider、Gateway、Session 等开发者文档是 2026-09-30 的动态页面，其中可能包含 `v0.20.1` 之后的演进。两类证据必须分栏，不得合并成“0.20.1 已精确具备动态文档所列全部实现”。[HE-REL][HE-ARCH]

## 1. 预结论：六层是本书观察模型，不是平台官方分层

`METHODOLOGY`：六层模型可以覆盖 OpenClaw `v2026.9.6` 的关键运行面，但它不是 OpenClaw 官方命名，也不是不可变架构。正式 C06 应把它写成一张“观察与训练地图”：

```text
人/客户端/渠道
      │
      ▼
控制层 ── 接纳、认证、RPC、事件、运行事实
      │
      ▼
消息层 ── 账户、准入、路由、会话键、排队、交付
      │
      ▼
认知执行层 ── Prompt/Context、Model/Provider、Agent Loop
      │
      ▼
行动层 ── Tool、Browser、Node、Worker、MCP、外部系统
      │
      ▼
状态层 ── Workspace、Session、Transcript、Memory、Queue、SQLite

治理层横切全部五层：Auth、Policy、Approval、Sandbox、Secrets、Audit、Recovery
```

这张图有三条必须写进正式章节的限制：

- 同一组件可能跨层。例如 Gateway 既承担控制面，又承载渠道连接、运行接纳、状态协调和恢复；把它只画成“网络入口”会失真。[OC-ARCH][OC-LOOP][OC-RECOVERY]
- “治理层”不是一个独立进程，而是散布在接入、策略合并、执行主机、密钥注入、数据库与恢复路径上的约束集合。[OC-TRUST][OC-PERM][OC-SECRETS]
- “状态层”不是“工作区文件夹”。OpenClaw 将工作区、全局 SQLite、每 Agent SQLite、归档/支持文件和沙箱工作区分开；训练时必须知道哪个对象才是事实源。[OC-WORKSPACE][OC-SESSION][OC-STATE]

## 2. OpenClaw 固定版六层组件登记

以下表格中的“停止”是停止当前动作或阻止新动作，“恢复”是把系统带回可验证状态。两者不能合并成一句“重启即可”。

### 2.1 控制层

| 组件 | 事实身份与执行位置 | 信任边界 | 失败暴露、停止与恢复 | 后章定义边界 | 证据 |
|---|---|---|---|---|---|
| Gateway | `VERSION-FACT`：每台主机一个长驻 Gateway，维护 Provider 连接，暴露带类型的 WebSocket API，校验 JSON Schema，向客户端和 Node 推送事件。运行在 Gateway 主机；渠道适配、Agent 接纳和大量协调都围绕它发生。 | 一个 Gateway 是一个信任域，不是敌对多租户边界；配置可写者按可信操作者处理。远端连接仍须 Gateway 认证和设备身份。 | 非 JSON 或首帧非 `connect` 会硬关闭；状态和事件缺口由客户端刷新。停止路径是拒绝新接纳、优雅 drain、再由 launchd/systemd 接管重启。恢复后必须核对会话、待交付与中断运行，而不是只看进程存活。 | C06 定义控制平面位置；C22 定义多租户隔离与网络威胁模型；C23 定义事故响应。 | [OC-ARCH][OC-TRUST][OC-RECOVERY] |
| WS/RPC 协议 | `VERSION-FACT`：客户端首帧必须是 `connect`；后续是 `req/res/event`。`send`、`agent` 等有副作用方法要求幂等键，Gateway 保存短期去重缓存。 | 传输认证、设备签名/配对与 RPC 方法授权是不同关口；隧道本身不替代 Gateway 认证。 | 请求错误返回结构化失败；事件不重放，序列缺口需要状态刷新。重复调用只能在幂等/收据边界内重试。 | C06 只给控制协议骨架；C15 负责 Hook/Webhook；C20 负责 A2A/Handoff；C22 负责认证细节。 | [OC-ARCH] |
| 控制客户端 | `VERSION-FACT`：macOS App、CLI、Control UI、自动化等通过 Gateway 控制面请求和订阅事件；WebChat 历史与发送同样走 Gateway API。 | 客户端设备身份、Gateway 凭证、角色权限相互叠加；“能连上”不等于“能执行所有操作”。 | 断线后重连并刷新事实；浏览器 outbox 只有在收据证明未消费时才可重新提交。客户端页面正常不等于后端任务完成。 | C06 定义客户端—Gateway关系；C21 定义人类协作界面；C23 定义观察与值守。 | [OC-ARCH][OC-RECOVERY] |
| 事件与系统事实源 | `VERSION-FACT`：Gateway 事件不重放；会话、转录、任务、交付等可恢复事实落在 SQLite。Channel 原生历史不能被当作完整 Agent 转录；Control UI/TUI 展示的 Gateway-backed transcript 才是运行事实视图。 | 事件是通知，不是永久账本；外部渠道回执也不能单独证明内部状态。 | 遇到序列缺口、断线或不确定提交，刷新数据库/会话事实并核对收据，禁止凭最后一条 UI 消息猜测完成。 | C06 定位事实源；C07 定义证据采集；C23 定义可观测性和 SLO。 | [OC-MESSAGES][OC-RECOVERY] |

### 2.2 认知执行层

| 组件 | 事实身份与执行位置 | 信任边界 | 失败暴露、停止与恢复 | 后章定义边界 | 证据 |
|---|---|---|---|---|---|
| Runtime / Agent Loop | `VERSION-FACT`：Gateway RPC `agent`、`agent.wait` 或 CLI `openclaw agent` 进入序列化的 Agent Loop；Loop 负责接纳后上下文准备、模型调用、工具循环、流式事件和持久化。默认在 Gateway 所在运行环境，沙箱/Worker 可改变工具或整轮执行位置。 | 模型、工具和状态写入是不同边界。Loop 的“能推理”不自动授予工具、文件、渠道或主机权限。 | 运行可因取消、超时、Provider 失败、工具失败或 Gateway 重启中断。`agent.wait` 等待超时不等于停止运行；停止必须使用对应 abort/stop 路径。恢复继续已有 transcript，不能假设整轮从零安全重放。 | C06 定义执行循环位置；C08 定义训练轮次；C17 定义主动任务中的执行策略。 | [OC-LOOP][OC-RECOVERY] |
| Prompt / Context Assembly | `VERSION-FACT`：运行前解析 Workspace，装配基础提示、Skills、bootstrap、会话历史和运行覆盖；上下文限制与 compaction 预留在执行器内处理。沙箱可把工具可见工作区重定向到沙箱空间。 | 注入到模型的文本不等于系统权限；外部内容可能是恶意输入。Workspace 文件可影响行为，但不能越过 Policy/Approval/Sandbox。 | 文件缺失可形成标记并继续；超长 bootstrap 被截断；上下文过载触发压缩/失败。恢复应核对实际 `/context` 或运行证据，而不是只读磁盘文件。 | C05 定义七契约语义；C06 只描述载入位置；C09 定义上下文工程；C13 定义 Compaction/Memory。 | [OC-LOOP][OC-WORKSPACE] |
| Model / Provider 解析 | `VERSION-FACT`：当前选择由会话状态、Agent/默认配置和调用源共同决定；认证 profile 与模型选择分离。每 Agent 的认证秘密和运行路由状态存于其 SQLite，配置中的 auth 项只保留元数据与路由。 | 调用外部 Provider 会把必要上下文送出本地信任域；凭证解析与模型内容边界必须分别治理。 | 解析失败在模型调用前暴露；显式用户会话选择默认严格，失败不能悄悄换成无关模型。停止时取消当前请求并保留已完成工具证据。 | C06 定位 Provider；C07 统一预算；C09 管上下文；C22 管数据外发与凭证风险。 | [OC-FAILOVER][OC-SECRETS] |
| Auth profile rotation | `VERSION-FACT`：OpenClaw 先在当前 Provider 内按 profile 顺序、冷却和可用性轮换，再考虑模型 fallback。会话可能固定首选 profile 以利用缓存，但故障时仍可同 Provider 轮换。 | 多账户共享同一 Provider 不代表数据或额度边界相同；显式用户 pin 与自动选择要区分。 | 失败、限流、计费或超时进入有界恢复/冷却；终态需报告尝试链。删除或禁用 profile 后不得继续复用旧秘密。 | C06 解释恢复顺序；C23 负责告警阈值；C24 负责成本与供应商治理。 | [OC-FAILOVER] |
| Model failover | `VERSION-FACT`：先做同模型有界恢复，再执行配置的 fallback；fallback 只对当前 turn 生效，不改写会话所选模型。显式用户模型选择严格；配置默认、Cron primary 等可按各自策略使用 fallback。 | 换模型可能改变数据处理地、能力、价格和安全属性，不能只视作可用性技巧。 | 重试前必须检查已完成工具与中断动作，避免重复副作用；所有候选耗尽后暴露终态失败。最终超时、成本熔断等属于停止条件，不应继续向下 fallback。 | C06 定义机制；C07 定义同任务同预算比较；C22/C24 分别管风险和成本。 | [OC-FAILOVER] |

### 2.3 状态层

| 组件 | 事实身份与执行位置 | 信任边界 | 失败暴露、停止与恢复 | 后章定义边界 | 证据 |
|---|---|---|---|---|---|
| Workspace | `VERSION-FACT`：Agent 的默认 cwd 与上下文之家，和 `~/.openclaw/` 中的配置、凭证、Session 分离。默认 cwd 不是硬沙箱；不启用 sandbox 时，绝对路径仍可能越出 Workspace。 | Workspace 是行为与知识载体，不是 OS 隔离边界，也不是所有运行状态的事实源。 | 错误 Workspace 会装配错误契约和文件。切换前应停止 Gateway、固定目标路径、运行迁移检查并重启；恢复文件时只回放已确认内容。 | C05 定义契约语义；C06 定义容器位置；C13 定义记忆文件；C22 定义文件系统边界。 | [OC-WORKSPACE] |
| Workspace bootstrap 载体 | `VERSION-FACT`：固定版标准载体包括 `AGENTS.md`、`SOUL.md`、可选 `USER.md`、`IDENTITY.md`、`BOOT.md`、一次性 `BOOTSTRAP.md`、`MEMORY.md`/daily memory 与 `skills/`；本地工具说明位于 `AGENTS.md` 的 `## Tools`。`TOOLS.md` 与 `HEARTBEAT.md` 已退役。 | 文本文件只是语义/提示载体；不能替代工具授权、准入或系统调度。 | `openclaw doctor --fix` 负责迁移退役文件：TOOLS 内容并入 AGENTS Tools 区；HEARTBEAT 指令进入系统 monitor scratch、有效任务进入 Cron。迁移前需备份并检查差异。 | C05 拥有七契约；C16 拥有 Heartbeat/Cron；C06 只记录固定版映射。 | [OC-WORKSPACE][OC-TOOLS-RET][OC-HB-RET] |
| Session | `VERSION-FACT`：Gateway 拥有 Session 状态；入站路由决定 session key。DM、群组、Cron、Webhook 等采用不同隔离规则；每 Agent SQLite 保存会话行与 transcript。Incognito 只是不持久化该会话，不会自动禁用工具、Provider 日志或外部写入。 | 多用户 DM 若共用 session 会泄露上下文；必须把身份隔离和会话隔离同时设计。 | `/new`、`/reset` 与 session 生命周期操作可以轮换/重置；未知或冲突恢复要保留 receipt/tombstone，不应强行重放。 | C06 定义 Session 身份与事实源；C13 定义上下文生命周期；C20 定义跨 Session/Handoff。 | [OC-SESSION][OC-RECOVERY] |
| Context | `VERSION-FACT`：Context 是当次模型调用实际可见的信息集合，由系统提示、Workspace bootstrap、Session 历史、Skills、工具结果和运行信息装配，不等于 Workspace 或 Memory 的全部内容。 | 模型可见性与磁盘可读性是两套边界；“未进 Context”不代表 Agent 的工具一定无法读取。 | 通过上下文详情、token 预算与压缩证据诊断；不能只凭回答猜测“已加载”。 | C09 主定义 Context；C06 只显示其装配位置。 | [OC-LOOP][OC-WORKSPACE] |
| Memory | `VERSION-FACT`：固定版可用 Workspace memory 文件与记忆插件/SQLite 索引；默认 active plugin 为 `memory-core`。Memory、Session transcript 与 Context 不是同义词。 | 长期数据来源、可见范围、过期和删除义务须独立治理。 | 记忆检索失败不应伪装成“没有相关记忆”；索引可重建但原始记忆内容的恢复要按来源与权限核对。 | C13 唯一定义分类、写入、检索、遗忘与压缩；C06 只给运行位置。 | [OC-MEMORY][OC-WORKSPACE] |
| Queue / Lane | `VERSION-FACT`：OpenClaw 用 lane-aware FIFO 协调同一 Session 与可选全局并发；每 Session 先串行，随后受全局 lane 约束。队列输入身份保留，但身份不自动成为执行权限。 | 排队只管理时序，不承担认证、授权或副作用幂等。 | `steer`、`followup`、`collect`、`interrupt` 语义不同；`steer` 不会中止已经运行的工具，`interrupt` 才要求终止当前工作。队列溢出/丢弃策略需可见，重启后按持久状态恢复。 | C06 定义队列位置；C16 定义主动任务节流；C20 定义跨 Agent 路由。 | [OC-QUEUE][OC-STEER] |
| SQLite 状态 | `VERSION-FACT`：固定版为 database-first：全局状态在 `~/.openclaw/state/openclaw.sqlite`；每 Agent 的运行、认证、Session、Transcript、Memory index 等在 `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite`。旧 JSON sidecar 不是活跃事实源。 | DB 文件权限、备份、schema 版本与单写者所有权共同构成完整性边界。 | 运行时拒绝打开比自身更新的 schema；迁移由 Doctor 所有；备份使用在线 SQLite 备份，不应复制正在写入的裸文件后声称可恢复。代码回滚也不能自动回滚 schema。 | C06 定义持久层位置；C13/C16 使用各自表语义；C23 定义备份恢复演练。 | [OC-STATE][OC-RECOVERY][OC-WORKSPACE] |

### 2.4 消息层

| 组件 | 事实身份与执行位置 | 信任边界 | 失败暴露、停止与恢复 | 后章定义边界 | 证据 |
|---|---|---|---|---|---|
| Channel | `VERSION-FACT`：Channel adapter 把外部平台事件规范化后送入 Gateway，并把回复交给外部平台。渠道可以在 Session queue 之前做背压，但不能据此声称拥有另一套 Agent 超时。 | 外部平台身份、OpenClaw 准入、Session 隔离和 Tool 权限是四个不同边界。 | 渠道断连应以 `channels status --probe`/渠道日志暴露；停止可停具体账户或插件。恢复后要核对入站是否消费、出站是否送达，不能只看 socket 重连。 | C06 定位 Channel；C15 定义 webhook/hooks；C21 定义交互；C23 定义通道 SLO。 | [OC-MESSAGES][OC-PAIRING][OC-RECOVERY] |
| Account | `VERSION-FACT`：Account 是某 Channel 下的连接/凭证实例；一个 Channel 可有多个账户。Binding 不会创建 Account。 | 账户凭证、外部平台权限与 OpenClaw 内部路由分离。 | 单账户秘密解析失败可以在支持的 owner 隔离模型下进入 cold/stale 状态；健康同胞账户仍可存在。恢复要验证正确账户，不允许静默借用别的账户。 | C06 定义对象关系；C22 定义凭证和最小权限；C23 定义账户探针。 | [OC-SECRETS][OC-BINDING] |
| Pairing | `VERSION-FACT`：DM sender pairing 与 Node device pairing 是两种机制。未知 DM sender 在批准前不进入正常处理；Node 以设备身份和 `role=node` 配对。 | Pairing 是准入，不是每次命令审批；DM 访问不自动授予群组访问或 owner 命令权。 | 拒绝/待批应明确；停止可撤销对应 sender/device。恢复必须重新核对 scope、账户与设备元数据，不能复制 token 绕过配对。 | C06 定位准入；C22 定义身份、撤销和攻击面。 | [OC-PAIRING][OC-ARCH] |
| Binding / Routing | `VERSION-FACT`：Binding 在流量已通过账户/准入后选择 Agent；不会创建渠道账户，也不会授予访问。规则按特异性优先。 | “路由到谁”与“允许进入”必须分开；错误 Binding 可能把合法消息送给错误 Agent。 | 无法选择 Agent 应暴露选择失败而非随机落点；修复 Binding 后用同一测试身份和会话范围复核。 | C06 定义 Binding 在数据流中的位置；C20 主定义复杂 Routing、Handoff 与组织协同。 | [OC-BINDING][OC-MESSAGES] |
| Delivery / Retry | `VERSION-FACT`：外发渠道 retry 是单次请求级有界重试；必须保持顺序并避免非幂等重复。持久化 outbound queue 有自己的预算、租约和对账；模型恢复是另一套机制。 | “模型生成成功”“内部入队成功”“外部平台接收”是三个不同状态。 | 不确定发送要保留 receipt 并进入 reconciliation，不能盲重发。重启后队列可 drain；预算耗尽后失败行用于结算，不应再次发送。 | C06 定义链路；C15/13 定义具体触发；C23 定义交付监控与补偿。 | [OC-RETRY][OC-RECOVERY] |
| Steering Queue | `VERSION-FACT`：`steer` 把新输入注入当前运行的下一安全边界，不会改变 Tool Policy、Session 或已运行工具；`interrupt` 是终止再处理。OpenClaw 的该语义不能外推到 Codex 或其他 Runtime。 | 新输入身份保留，但不能借 steering 提升权限。 | 如果当前工具不可中断，steer 要等待；需要立即停止时用 interrupt/stop，并检查工具是否已产生副作用。 | C06 解释本 Runtime 的排队；C21 定义人类干预；C23 定义卡死处理。 | [OC-STEER][OC-QUEUE] |

### 2.5 行动层

| 组件 | 事实身份与执行位置 | 信任边界 | 失败暴露、停止与恢复 | 后章定义边界 | 证据 |
|---|---|---|---|---|---|
| Tool | `VERSION-FACT`：Tool 是可被 Agent 调用的执行能力；可用性由工具 profile、allow/deny、Provider、Sandbox、Channel/Plugin 等共同决定。文字契约不会创建真实 Tool。 | Tool schema 是调用接口，不是授权证明；执行主机和数据出口决定实际风险。 | 工具失败要记录调用参数边界、错误与副作用状态。停止模型流不保证已发出的工具动作回滚。恢复前先查状态，再决定补偿或重试。 | C14 主定义 Tool 合约、权限、验证与 MCP；C06 只画执行位置。 | [OC-TOOLS][OC-PERM] |
| Browser | `VERSION-FACT`：OpenClaw 可用 Gateway 本地回环控制服务驱动隔离 browser profile；内置 `user` profile 则通过 Chrome DevTools MCP 接入真实已登录 Chrome，风险显著不同。浏览器也可位于 Node 或托管远端。 | 隔离 profile、个人已登录浏览器、远程 CDP 是三种不同信任边界；浏览器控制面应按操作者权限处理。 | 停止当前浏览器任务不等于撤销已提交表单。恢复需核对页面、网络结果和外部系统收据；远程控制暴露要先收紧网络/配对。 | C06 定义位置；C14 定义浏览器工具契约；C22 定义网页注入与凭证威胁。 | [OC-BROWSER][OC-AUDIT] |
| Node | `VERSION-FACT`：Node 是通过 Gateway WS 连接的外围设备，声明 `role=node` 和能力/命令，通过 `node.invoke` 执行；Node 不是 Gateway，渠道消息仍落在 Gateway。 | 配对建立设备身份与 token，不是逐命令批准；`system.run` 还受 Gateway 粗粒度命令策略和 Node 本地 exec approvals 约束。 | 断线应令远程调用失败而不是默默改到 Gateway 主机。停止可断开或撤销配对、禁用命令。恢复后重新核对设备身份、能力清单和本地主机策略。 | C06 定义 Node 位置；C14 定义远程工具；C22 定义远程执行威胁。 | [OC-NODE][OC-PERM][OC-APPROVAL] |
| Cloud Worker | `VERSION-FACT`：OpenClaw Worker 是一次性云端执行机；Session/Transcript 继续由 Gateway 拥有，Worker 可被丢弃，已接受的文件/结果经协调回到 Gateway 事实域。 | Worker 是新的执行与网络边界；发给 Worker 的每轮私有启动封套和凭证范围必须最小化。 | Worker 丢失不能等同于会话丢失。停止/回收 Worker 后，按 Gateway 保存的任务、结果与变更状态决定重试；不把未知副作用自动重演。 | C06 定义位置与回收；C14 定义 Worker 工具契约；C19 定义组织 Worker；C22 定义供应链与云边界。 | [OC-WORKER][OC-RECOVERY] |
| MCP Server | `VERSION-FACT`：MCP Server 可向 OpenClaw提供 tools/resources/prompts；Server 可由 Gateway 或 Node 一侧托管/接入。保存配置不证明 Server 可达，必须 probe。MCP 工具仍受同一工具/权限策略，不能绕过 Policy。 | MCP Server 是独立信任主体；Transport、Server 代码、凭证与工具副作用均需单独评估。 | 不可达、schema 变化或权限拒绝应在发现/调用时失败。停止可禁用 Server 或断开 Node；恢复前重新探测和核对工具描述。 | C06 只把 MCP 放在行动面；C14 主定义 MCP 契约、发现、授权和测试。 | [OC-MCP][OC-NODE-MCP] |
| Plugin | `VERSION-FACT`：Plugin 在 Gateway 进程内运行，属于可信代码；安装/更新会运行代码，启用后可能注册工具与渠道。 | Plugin 不是“被 sandbox 的普通工具”；它共享 Gateway 进程信任。来源、固定版本和 allowlist 是供应链边界。 | 发现异常先禁用/停止 Gateway；代码或 discovery-root 变更可能要求重启。恢复应核对来源、解包内容、策略扫描和已注册能力。 | C14 定义 Plugin/Skill/Tool 区别；C22 定义供应链风险。 | [OC-PERM] |

### 2.6 治理层

| 组件 | 事实身份与执行位置 | 信任边界 | 失败暴露、停止与恢复 | 后章定义边界 | 证据 |
|---|---|---|---|---|---|
| Authentication | `VERSION-FACT`：Gateway 连接认证、设备配对、Channel sender 准入、Provider 认证与 Node 身份是不同认证面。 | 任何一面通过都不自动覆盖其余面。一个 Gateway 默认面向单个操作者或互信团队，不支持把对抗租户只靠 persona 分隔。 | 认证失败应 fail closed；修复时分别轮换 Gateway、Channel、Provider 或 Node 凭证，不做“大一统 token”替换。 | C06 定位认证面；C22 拥有威胁模型与密钥轮换规范。 | [OC-ARCH][OC-PAIRING][OC-TRUST] |
| Policy | `VERSION-FACT`：工具 profile、全局/Provider/Agent/Sandbox allow/deny、消息动作策略和 Node 命令策略共同收敛为有效权限。较窄层级不能恢复被上游 deny 的能力。 | Policy 是强制边界；C05 的 SOUL/TOOLS/AGENTS 是语义约束，不能替代它。 | 拒绝必须可观察；变更前读取有效策略，变更后用负例验证。停止可 deny 相关 tool/command/surface。 | C22 主定义策略设计；C06 解释策略落点；C05 保持契约层。 | [OC-PERM][OC-AUDIT] |
| Approval | `VERSION-FACT`：Exec approval 在实际执行主机本地执行；命令必须同时满足 Policy、allowlist 和可选用户批准。Approval 只能收紧配置权限，不能放宽。它是误操作护栏，不是敌对租户隔离。 | Gateway host 与 Node host 各有本地 approval state；批准后命令仍可按主机文件权限修改数据。 | 待批可阻塞动作；拒绝/过期即停止。批准内容漂移、可执行文件或绑定脚本变化时应拒绝。恢复需生成新的精确请求，不能复用宽泛口头同意。 | C21 定义人类审批体验；C22 定义安全审批与能力绑定。 | [OC-APPROVAL][OC-PERM] |
| Sandbox | `VERSION-FACT`：OpenClaw 区分整 Gateway 容器边界与工具 sandbox；工具 sandbox 可按 agent/session/shared scope，并可使用 Docker/Podman、SSH、OpenShell 等 backend。`workspaceAccess` 决定 none/ro/rw。Backend failure 在 required 模式下不得回落到 host。 | Sandbox 只约束被放入其中的执行，不自动隔离同一 Gateway 的 Session 可见性、插件或 elevated escape hatch。`shared` scope 的隔离更弱。 | 启动失败应 fail closed。活动运行期间不得偷偷切换 containment；先停止 run，再变更并重新验证。恢复文件应做选择性回收，不整包信任旧环境。 | C06 定义运行位置；C22 定义安全基线与逃逸假设。 | [OC-SANDBOX][OC-PERM] |
| Secrets | `VERSION-FACT`：SecretRefs 激活时解析为内存快照；某些已知 owner 的可重试失败可隔离为 cold/stale，Gateway 核心、结构错误或未知 owner 仍 fail closed。Provider SecretRef 可用进程内 sentinel 到最后出站点再注入，但这不是进程隔离。 | SecretRef 避免把明文写入配置，却不能保护 Agent 可读路径里的明文残留；真实秘密最终仍会出现在同进程适配边界。 | 未解析 sentinel 在网络请求前 fail closed；严格 reload 失败保留旧 snapshot。恢复要清理旧 config/.env/models/auth 残留并跑 secrets audit，不能只“换成引用”即宣布完成。 | C22 主定义密钥威胁；C06 只描述生命周期与 owner 隔离。 | [OC-SECRETS] |
| Audit / Diagnosis | `VERSION-FACT`：`openclaw security audit` 检查入站、跨 Agent Session、工具爆炸半径、Exec、网络、Browser、磁盘、Plugin、策略和模型卫生；`--deep` 尝试 live Gateway probe；`--fix` 只做一组窄化修复。 | Audit 是诊断，不是运行时强制；无 finding 不等于无风险，`--fix` 也不替代人工 threat model。 | 高优先级先处理“开放入口+工具”、公网暴露、Browser 控制、权限和 Plugin。修复后重复 probe 和负例测试。 | C23 定义可观测与运行审计；C22 定义安全基线；C06 给入口。 | [OC-AUDIT] |
| Recovery | `VERSION-FACT`：会话、转录、任务、交付、Cron 等按各自 SQLite 记录恢复；PTY 只在进程内，重启不恢复。优雅重启先 drain；被中断的 eligible work 才按记录自动续跑/对账。 | 恢复权威来自 durable state 和 receipt，不来自模型“记得自己做过”。代码降级不能倒转 schema 或抹掉新版本收据。 | 对不确定副作用先查外部状态；失败 delivery 不盲发；tombstone/人工检查优先于猜测。备份和恢复必须用同一状态环境并做还原演练。 | C06 定义恢复骨架；C23 主定义事故、备份、RTO/RPO 与演练。 | [OC-RECOVERY][OC-STATE] |

## 3. 从入站到恢复的两条事实链

### 3.1 消息—执行—交付链

`VERSION-FACT` 与 `METHODOLOGY` 的组合表达：

```text
外部平台事件
  → Channel/Account 接收
  → sender pairing / allowlist / account policy
  → Binding/Router 选择 agent + session key
  → dedupe/debounce + per-session queue + global lane
  → Gateway 接纳 agent run，返回 runId
  → Context/Prompt 装配
  → Provider/Model/Auth profile 解析
  → 模型 ↔ Tool/Browser/Node/Worker/MCP 循环
  → transcript / run state 持久化
  → outbound delivery queue
  → Channel provider 回执或不确定状态
  → receipt reconciliation / retry / terminal failure
```

正式 C06 必须把以下四个时刻分开：`请求已接纳`、`Agent 已完成`、`结果已入交付队列`、`外部接收已确认`。任一前置状态都不能替代后置状态。[OC-ARCH][OC-MESSAGES][OC-RECOVERY]

### 3.2 停止—恢复链

```text
发现异常
  → 冻结新接纳或限定受影响 surface
  → 对当前 run 发出 stop/abort/interrupt
  → 等待或强制结束实际执行主机上的工具/进程
  → 读取 SQLite run/transcript/delivery receipt
  → 检查外部系统是否已有副作用
  → 判定：继续 / 补偿 / 人工重试 / tombstone
  → 恢复 Provider、Node、Channel 或 Gateway
  → 用同一 session/receipt 复核，不改 ID 规避冲突
```

`STABLE-PRINCIPLE`：恢复不是“重启服务”，而是“恢复事实一致性”。对邮件发送、购买、文件覆盖、远程命令等非幂等动作，只要结果不确定，就必须先查外部事实，禁止自动重演。[OC-FAILOVER][OC-RETRY][OC-RECOVERY]

## 4. Hermes 作为第二实现：映射，不同构

### 4.1 版本边界

- `VERSION-FACT`：官方 release 页将 Hermes Agent `v0.20.1` 标为 2026-08-13 的 patch/stabilization release，tag 为 `v2026.8.13`，发布提交页面指向 `f80f453`。[HE-REL]
- `DYNAMIC-DOC`：2026-09-30 的官网 Architecture 把 CLI、Messaging Gateway、ACP、Batch、API Server、Python Library 列为多个入口，共同进入 `AIAgent`；同时列出 Prompt Builder、Provider Resolution、Tool Dispatch、SQLite+FTS5 Session Storage、Tool backends 与 MCP。[HE-ARCH]
- `DYNAMIC-DOC`：官网 Provider Runtime 文档说明 CLI、Gateway、Cron、ACP 和辅助调用共享 runtime resolver，并给出显式请求、配置、环境变量、默认/自动解析的优先级，以及配置 fallback provider chain。[HE-PROVIDER]
- 因动态文档远晚于 release，下面的“当前架构映射”不能写成“v0.20.1 的逐文件保证”。要证明某能力属于 v0.20.1，须在正式事实审校时回查 `f80f453` 源码或该 release 的归档文档。

### 4.2 六层对照

| 本书层 | OpenClaw 固定版 | Hermes 官方动态架构 | 不同构边界 |
|---|---|---|---|
| 控制 | 单一长驻 Gateway + typed WS/RPC/event，统一设备/客户端入口 | CLI、Gateway、ACP、Batch、API、Python Library 多入口，Messaging Gateway 是其中一个长驻入口 | 不应把 Hermes Messaging Gateway 写成 OpenClaw 单一控制平面的同义词；Hermes 的核心共享点更接近 `AIAgent` 与 runtime resolver。[HE-ARCH] |
| 认知执行 | Gateway 接纳后运行 Agent Loop，装配 Context，解析 Model/Auth，执行工具循环与持久化 | `AIAgent`/conversation loop；Prompt Builder、Provider Resolution、Tool Dispatch；文档称含 retries/fallback/compression/persistence | 概念可对照，具体并发、取消、writer fencing 和 fallback 规则不可互抄。[HE-ARCH][HE-PROVIDER] |
| 状态 | 全局 SQLite + 每 Agent SQLite；Workspace 与状态库分离；Session 由 Gateway 持有 | 官网列出 SQLite+FTS5 session storage、session lineage、profile-scoped HERMES_HOME/config/memory/sessions | Hermes Profile 是状态命名空间，不应自动写成 OS Sandbox；SQLite schema、owner 和恢复路径需按 Hermes 文档单独核验。[HE-ARCH] |
| 消息 | Channel/Account/Pairing/Binding/Session key/Queue/Delivery 明确分层 | Messaging Gateway adapter → authorization → session key → AIAgent → delivery；官网列出 allowlist + DM pairing | 当前公开架构可证明流程相似，但未证明 OpenClaw Binding 特异性、lane queue、durable delivery receipt 等实现同构。[HE-ARCH] |
| 行动 | Tool/Browser/Node/Worker/MCP，执行位置可在 Gateway、Sandbox、Node 或 Worker | 中央 Tool Registry；Terminal 多后端、Browser 多后端、动态 MCP、File/Vision 等 | Hermes backend 是工具执行环境；不能把 OpenClaw Node/Cloud Worker 名词直接套用。数量类信息是动态文档快照，不应写入稳定正文。[HE-ARCH] |
| 治理 | One-Gateway trust model；Policy/Approval/Sandbox/SecretRef/Audit/Recovery 分立 | 动态架构显示危险命令 detection/approval、环境后端、profile isolation、配对与凭证解析组件 | 现有证据不足以证明两者具有同等 secrets sentinel、审计覆盖、Gateway 信任域或恢复语义；正式正文只能写“有对应治理组件，保证不同”。[HE-ARCH][HE-PROVIDER] |

### 4.3 Hermes 进入 C06 的推荐写法

正式正文应使用“同一问题、不同实现”的小框，而不是另写一套 Hermes 手册：

1. 同问入口如何进入 Agent：OpenClaw 从 Gateway RPC 进入；Hermes 从 CLI/Gateway/ACP/API 等进入共享 AIAgent。
2. 同问 Provider 如何解析：两者都有共享解析与 fallback，但来源优先级、严格选择、auth pool 和 turn-local 行为需各写各的。
3. 同问状态在哪里：两者都有 SQLite 和按主体隔离的状态目录，但 owner、schema 与恢复机制不同。
4. 同问工具在哪里执行：OpenClaw 强调 Gateway/Node/Worker/Sandbox placement；Hermes 动态文档强调多种 tool backends。两者只在“执行位置必须显式”这一原则上汇合。

禁止用“OpenClaw 名词 → Hermes 同名词”的一行字典来替代架构解释。

## 5. Muse Secure VM：闭源托管产品镜面

以下全部为 `VENDOR-CLAIM`，来源是 Meta 2026-09-08 的官方发布与安全说明，未做独立源代码或部署验证：[MUSE-NEWS][MUSE-SEC]

| 本书观察点 | Meta 的公开说法 | C06 可用边界 |
|---|---|---|
| 运行容器 | 每位用户有专用云端 Linux VM；核心 harness、Workspace、工具与二进制位于 `systemd-nspawn` runtime cell；cell root 映射为非特权 host user | 可作为“托管产品也必须说明执行位置与隔离层”的镜面；不得写成 OpenClaw/Hermes 可直接复制的部署模板 |
| 状态 | VM 是用户数据的 system of record；durable application state 位于 runtime cell 和凭证存储之外的 PostgreSQL；VM 数据持续备份 | 可用于说明 Workspace、应用状态与 credential store 可分离；不可外推其实际可用性、RPO/RTO |
| 消息/客户端 | iOS、Android、Web 客户端通过安全传输直连用户 VM；产品也通过 WhatsApp 使用 | 可作为托管入口例子；没有公开证据支持把它映射为 OpenClaw Gateway/Binding |
| 行动 | Connector、Browser、Subagent、Cron 在专用环境内运行；built-in connector business logic 由 cell 外 privsep worker 执行 | 可用于说明“工具描述、执行位置、凭证位置可以三分”；不可断言所有自定义工具享有同等边界 |
| 凭证 | `hatch-authd` 存真实 credential，Agent 看到 surrogate；Sentinel 在网络边界做即时注入 | 可作为 secrets egress-time injection 的产品镜面；只能写“Meta 声称” |
| Policy/Approval | Sentinel 是 connector action 与全部网络 egress 的唯一批准权威；人类批准直接在客户端—Sentinel 链路发生，可按一次、Session、Task、时间或长期 scope 授权 | 可用于说明系统审批不能仅依赖对话文本；不能声称其攻击不可绕过 |
| Browser | Browser CDP broker 在 runtime cell 外；Agent 只见窄接口和 accessibility tree；用户接管或凭证填充时 Agent 暂停 | 可作为受控浏览器界面范例；不是开放 API 保证 |
| 安全结论 | Meta 明确承认 Prompt Injection 仍是开放问题，Muse 仍会犯错 | 正文必须保留这一限制，禁止用厂商安全架构推出“绝对安全” |

特别禁写：Muse Confidential VM 在 2026-09-30 仍被 Meta 描述为“计划在今年晚些时候交付/小范围测试”，不得写成已面向所有用户正式上线的能力。[MUSE-NEWS][MUSE-SEC]

## 6. 旧稿命令、字段与载体冲突

这些条目不是要求 C06 正文收录全部 CLI，而是防止作者把历史材料直接粘贴进固定版正文。

| 旧稿或早期说法 | 固定版处理 | 冲突级别 | 依据 |
|---|---|---|---|
| `openclaw init` | 改为 `openclaw setup` 或 `openclaw onboard`；正式正文若无教学必要可只写“运行安装/引导命令” | 命令冲突 | [LEGACY-FACT][OC-WORKSPACE] |
| `openclaw agents create X` | 固定版 CLI 是 `openclaw agents add X --workspace <dir>` | 命令冲突 | [LEGACY-FACT] |
| `openclaw chat --agent X --prompt Y` | 固定版为 `openclaw agent --agent X --message Y` | 命令冲突 | [LEGACY-FACT][OC-LOOP] |
| `openclaw agents health-check` | 使用 `openclaw health`、`openclaw status`、`openclaw doctor` 的各自语义；不要把诊断、状态和修复合并 | 命令/语义冲突 | [LEGACY-FACT][OC-AUDIT] |
| `openclaw agents archive` | 历史底稿改为 `openclaw backup create`；恢复流程仍须另行验证，不能把 backup=create 当 restore | 命令冲突 | [LEGACY-FACT][OC-STATE] |
| `openclaw plugin` | 固定版命令组使用复数 `openclaw plugins` | 命令冲突 | [LEGACY-FACT] |
| `manifest.yaml` | OpenClaw plugin manifest 为 `openclaw.plugin.json`/JSON5 语义，不是 YAML | 文件格式冲突 | [LEGACY-FACT][OC-PERM] |
| `openclaw cron add --schedule ... --target ... --prompt ...` | 旧底稿记录的固定版形态为 `--cron ... --session ... --message ...`；由于 C16 拥有自动化命令，C06 正文不应展开 | 命令冲突/越权 | [LEGACY-FACT] |
| 顶层 `runtime`、`workspace`、`routing`、`heartbeat`、`subagents` | 不得作为固定版真实顶层配置；相应能力分布在 agents、channels、bindings、tools、automation 等对象中 | 幽灵字段 | [LEGACY-FACT][OC-WORKSPACE][OC-HB-RET] |
| `reserveTokensFloor` 可配置 | 固定版不得写成用户配置字段；旧稿把内部/历史概念当配置。正式值与语义交 C13 按固定源码重核 | 字段/定义权冲突 | [LEGACY-FACT] |
| Workspace 固定包含 `TOOLS.md` | `TOOLS.md` 已退役，不再是 runtime bootstrap；内容迁入 `AGENTS.md` 的 `## Tools` | 载体冲突 | [OC-TOOLS-RET][OC-WORKSPACE] |
| Workspace 固定包含 `HEARTBEAT.md` | `HEARTBEAT.md` 已退役，不创建也不读取；Heartbeat instructions 在共享状态库的 monitor scratch | 载体/状态冲突 | [OC-HB-RET] |
| 配置永远“20 个顶层 key、19 object + 1 array” | 这是旧机器快照，不是 schema 不变量；不得进入稳定正文或校验器常量 | 快照冒充标准 | [LEGACY-SCHEMA] |
| Tool/Skill/MCP 是同一种“协议” | 三者身份不同：Tool 是可调用能力，Skill 是说明/封装，MCP 是外部能力协议与 Server 边界；C14 负责正式定义 | 概念冲突 | [OC-TOOLS][OC-MCP] |
| 绑定配置就代表授权 | Binding 只做 Agent 选择，准入与权限另行检查 | 安全冲突 | [OC-BINDING][OC-PAIRING] |
| Workspace 就是安全容器 | Workspace 只是默认 cwd；没有 sandbox 时可越界 | 安全冲突 | [OC-WORKSPACE][OC-SANDBOX] |

## 7. 禁止写入 C06 正文的未核实或过时主张

以下主张在补齐固定版证据或实测前必须保持 `UNKNOWN`，其中若标“禁止”则不应以肯定句出现：

1. **禁止**声称六层架构是 OpenClaw、Hermes 或 Meta 官方共同标准；它是本书方法。
2. **禁止**把官网最新 Hermes Architecture 的全部组件回填为 Hermes `v0.20.1` 的精确能力；需回查 `f80f453`。
3. **禁止**声称 Hermes Messaging Gateway 与 OpenClaw Gateway 在 RPC、状态所有权、恢复、队列、权限上同构。
4. **禁止**声称 Hermes Profile 是安全沙箱；当前证据只支持它拥有独立 HERMES_HOME、配置、Memory、Session 与 Gateway PID。[HE-ARCH]
5. **禁止**声称 Muse 架构经过本书独立安全验证，或 Prompt Injection 已解决；Meta 自己明确说它仍是开放问题。[MUSE-SEC]
6. **禁止**把 Muse Confidential VM 写成已普遍上线；截至核验日仍是“coming soon”。[MUSE-SEC]
7. **禁止**把 Incognito Session 写成无痕、无外发、无工具持久化；它只影响会话持久化范围。[OC-SESSION]
8. **禁止**把 Workspace、Session、Context、Memory、Queue、SQLite 混作“记忆系统”。
9. **禁止**声称 Gateway 重启会恢复全部进程；PTY 不恢复，外部副作用和不确定 delivery 必须对账。[OC-RECOVERY]
10. **禁止**把 Provider failover 描述成无损切换；模型、地区、成本、政策、输出和工具兼容性均可能改变。[OC-FAILOVER]
11. **禁止**把 `agent.wait` 超时写成 Agent 已停止；等待者超时与运行终止不是一件事。[OC-LOOP]
12. **禁止**把 steer 写成可中断任意工具或提升权限；它在安全边界注入输入，不替代 interrupt/stop，也不改 policy。[OC-STEER]
13. **禁止**把 Pairing 写成单次执行批准，或把 Binding 写成准入授权。[OC-PAIRING][OC-BINDING]
14. **禁止**声称 MCP 配置存在就代表 MCP Server 健康；必须 probe。[OC-MCP]
15. **禁止**把 Plugin 写成默认在 Agent sandbox 中运行；OpenClaw Plugin 在 Gateway 进程内，是可信代码。[OC-PERM]
16. **禁止**把 SecretRef 写成模型永远不可能接触到秘密；sentinel 不是进程隔离，Agent 可读磁盘残留仍是风险。[OC-SECRETS]
17. **禁止**把 security audit 无 finding 写成“系统安全”；Audit 是诊断，`--fix` 也只修一组窄问题。[OC-AUDIT]
18. **禁止**把旧稿的顶层 key 数量、binding 数量、插件子命令数量、默认端口或默认队列参数写成跨版本稳定原理。
19. **禁止**使用未复核的生产绝对路径、真实 Agent 名、真实 Account ID、失败次数或本机凭证结构做出版示例。
20. **禁止**在 C06 冻结 C13/C14/C16/C20/C22 的详细定义；本章只定位组件和边界。

## 8. 最小可训单体参考部署

### 8.1 目标与约束

`METHODOLOGY`：最小可训单体不是“最少安装项”，而是能完成以下闭环的最小系统：接纳一个可识别任务、在受限边界内执行、留下过程与结果证据、能停止、能暴露故障、能从持久状态恢复。

推荐基线：

| 维度 | 最小配置 | 为什么不可再删 |
|---|---|---|
| 信任域 | 一位人类 owner、一个 OS 用户、一个 Gateway；只监听 loopback，远程访问另走受控隧道 | 避免在未定义租户隔离时共享同一 Gateway |
| Agent | 一个 Agent ID、一个明确 Workspace、一个 C04 岗位 | 没有岗位与状态所有权就无法评估训练结果 |
| 契约 | C05 最小七契约集，映射到固定版真实载体；文本不含凭证 | 没有语义边界就不能判断行为偏离 |
| Provider | 一个 primary；一个仅用于测试的 fallback 或同 Provider 第二 auth profile；明确 strict 与 auto 选择场景 | 可验证解析、失败暴露与恢复，而不是只验证成功路径 |
| Session | 一个私有主 Session；单用户 direct scope；不先接公开群组 | 保持首轮训练的身份与上下文边界可解释 |
| Channel | 首先 CLI/Control UI；可选一个测试 Channel/Account，必须启用 pairing/allowlist | 先验证核心，再引入外部平台不确定性 |
| Tools | 从最小 profile 开始；文件只读或 sandbox workspace；写/exec/browser 默认 deny，按岗位逐项开启 | 工具面必须从 C04 工具需求生成，而不是从平台能力清单全开 |
| Sandbox | 对训练/不可信输入使用 required、agent 或 session scope；Workspace 默认 none/ro，确有写入任务才 rw | 失败时必须 fail closed，避免悄悄回到 host |
| Approval | 主机 exec 采用 allowlist + on-miss/always；高风险动作另做业务审批 | 验证语义契约不能绕过系统权限 |
| Secrets | SecretRef 或外部秘密管理；清除 Workspace、配置、旧文件中的明文残留 | 避免训练素材与凭证同域 |
| State | 全局与每 Agent SQLite 均纳入在线备份；Workspace 私有版本库；记录 schema/version | 允许恢复与差异核对 |
| Observation | Gateway/Channel/Session/Queue/Delivery/Provider/Tool 的结构化日志与 runId/receipt；安全审计基线 | “有回答”不是完整验收证据 |
| Stop | 明确 `/stop`/interrupt、工具进程终止、Channel 停用、Node 撤销、Gateway drain 顺序 | 停止是训练门禁的一部分 |

### 8.2 建立顺序

1. 冻结版本、状态目录、Workspace 和 Agent ID；记录 `openclaw --version`。
2. 从 C04 读取任务域、负面清单、非功能要求和风险级；从 C05 读取最小契约与冲突裁决。
3. 配置 loopback Gateway、单一 owner 和私有 Session；先不接公网/群组。
4. 配置 Provider primary、测试用 fallback/第二 profile，写明哪些选择 strict。
5. 将契约语义映射到固定版真实载体；不得重新创建退役 `TOOLS.md`/`HEARTBEAT.md`。
6. 只开放完成岗位基线任务所需的最小 Tool；启用 sandbox 与 exec approval。
7. 运行只读核验：`openclaw status`、`openclaw health`、`openclaw doctor`、`openclaw security audit --deep`；若启用 Channel，再运行对应 probe。
8. 建立一条可逆端到端基线任务，记录请求、runId、工具证据、transcript、delivery receipt 与最终产物。
9. 演练停止、Provider 失败、Queue 中断与 Node 断开；只有恢复证据闭合后才进入 C07 正式评测。

### 8.3 最小健康判定

单体只有同时满足以下状态，才可称“可训”：

- **控制健康**：Gateway 接受认证连接，版本/状态一致，无未处理 migration refusal；
- **认知健康**：指定 Provider/Model 的实际解析结果可见，strict/fallback 行为符合声明；
- **状态健康**：Workspace 与 SQLite owner 明确，Session/Transcript 可读，在线备份可验证；
- **消息健康**：若启用 Channel，入站准入、路由、队列、出站 receipt 可追踪；
- **行动健康**：Tool 的实际执行位置、effective policy、approval 与 sandbox 可被负例证明；
- **治理健康**：秘密不落 Workspace，security audit 已审阅，stop/recovery 演练通过。

`STABLE-PRINCIPLE`：健康不是六项平均分。任何一项安全关键失败都应阻断“可训/可上线”结论。

## 9. 三类故障注入计划

所有演练必须在隔离测试 profile、虚构数据和可逆工具上进行，不使用真实收件人、真实支付、生产文件或生产 Node。每次演练前保存 DB/Workspace 备份、runId 规则和停止人。

### 9.1 Provider 故障

| 项目 | 设计 |
|---|---|
| 目的 | 验证同模型有界恢复、auth profile rotation、模型 fallback、strict selection 与最终失败能否区分 |
| 注入 | 使用本地 mock/代理按序返回 429、503、连接超时；另设一个无效测试 credential；不修改生产 key |
| 场景 | A：配置默认模型允许 fallback；B：用户显式 pin 模型应 strict；C：工具已产生可见可逆副作用后 Provider 中断 |
| 预期 | A 先同模型恢复/同 Provider profile，再按配置切 fallback，且只作用于当前 turn；B 不得偷偷换模型；C 重试前必须读取已完成工具证据，不重复动作 |
| 观测 | 选择来源、候选链、attempt、cooldown、实际回答模型、run timeout、tool receipt、terminal error |
| 停止 | 到达 turn deadline/成本阈值/人工 stop 即终止，不允许为了“成功”无限尝试 |
| 恢复 | 恢复 primary 后新 turn 从原选择开始；核对 session 选择未被 fallback 改写；记录实际降级质量与成本 |
| 通过 | 无越权切换、无重复副作用、失败可见、恢复后选择与 transcript 一致 |

### 9.2 Queue / Steering 故障

| 项目 | 设计 |
|---|---|
| 目的 | 验证 per-session 串行、全局 lane、steer/followup/collect/interrupt 语义、溢出与重启恢复 |
| 注入 | 在同一测试 Session 提交一个可观察的长时只读工具，再按固定间隔发送 steer、followup 与 interrupt；另以多个隔离 Session 达到测试并发/容量阈值 |
| 场景 | A：steer 到达时工具仍在运行；B：interrupt 当前 run；C：排队后 Gateway 在持久点重启；D：达到 cap 后观察 drop/summary 策略 |
| 预期 | steer 不假装中断已运行工具；interrupt 停止并保留副作用证据；同 Session 不出现并发 writer；重启后仅按持久 receipt 恢复；丢弃策略明确可见 |
| 观测 | session key、queue mode、lane、admission order、active/expected writer、pending input、drop reason、transcript 顺序 |
| 停止 | 人工 `/stop`/interrupt；若工具不可中断，终止实际执行主机进程并标记不确定状态 |
| 恢复 | 从 Session/Queue durable state 对账，禁止改变 message ID 诱发重放；确认新输入身份未提升权限 |
| 通过 | 顺序稳定、没有双写、没有静默丢消息、停止与恢复状态可解释 |

### 9.3 Node 故障

| 项目 | 设计 |
|---|---|
| 目的 | 验证 Gateway 与 Node 分工、执行位置、配对/命令策略、本地 approval 与断线恢复 |
| 注入 | 使用一次性测试 Node 执行幂等只读命令；调用前、批准后未执行、执行中和结果返回前四个时点分别断网/停 Node |
| 场景 | A：能力声明后立即离线；B：approval 等待期间离线；C：命令可能已执行但 receipt 未返回；D：Node 以变化的元数据重连 |
| 预期 | 不得自动转到 Gateway host；待批请求不能凭聊天文本通过；C 进入不确定并先查 Node/外部状态；元数据变化要求修复配对或重新验证 |
| 观测 | device identity、pairing scope、advertised caps/commands、Gateway allow/deny、Node local approval、systemRunPlan、receipt |
| 停止 | 禁用 `system.run`、断开/撤销测试 Node pairing；取消关联 run |
| 恢复 | 重新配对后核对真实设备、能力与 host-local policy；只对已证明未执行的动作重试 |
| 通过 | 无执行位置漂移、无重复命令、审批和配对职责不混淆、断线终态可审计 |

## 10. C04 / C05 对 C06 的硬依赖

### 10.1 已具备的 C04 输入

C04 生产包已建立三份结构化输入，C06 作者应消费而不是重定义：

| C04 输入 | C06 用途 | 缺失时的后果 |
|---|---|---|
| A-C04-01 岗位建模卡：使命、服务对象、JTBD、任务域、输入/输出、终态、in/out scope、升级路径、证据要求 | 决定入口、Session、Channel、状态 owner 与成功事实 | 运行容器会退化成平台功能清单 |
| A-C04-02 能力树：知识/推理/执行/协作/反思与速度、成本、稳定、透明、可恢复等 NFR | 决定 Provider、Tool、执行位置、观测和恢复要求 | 无法判断为何需要 Node/Browser/Worker 或什么叫健康 |
| A-C04-03 风险分级表：影响、可逆性、敏感性、不确定性、负面清单、控制与测试映射 | 决定 Policy、Approval、Sandbox、Secrets、Channel 准入和故障演练强度 | 会从“平台能做”错误跳到“岗位可做” |

C04 只提供“需要什么与不能做什么”，不应提前指定 OpenClaw/Hermes 组件；C06 负责把需求落到运行位置和系统边界。

### 10.2 尚未满足的 C05 输入

CHAPTER-CARDS 明确 C06 `depends_on: [C04, C05]`。截至本前置研究包撰写时，不得假设 C05 已经冻结。C06 正式开写至少需要：

1. `A-C05-01 七契约草案包`：USER、SOUL、AGENTS、TOOLS、IDENTITY、HEARTBEAT、MEMORY 的最小语义、版本、owner 与适用对象；
2. `A-C05-02 契约冲突矩阵`：冲突优先级、升级、测试、回滚与变更记录；
3. 明确“七契约是语义方法，不是七个固定文件”，并给出 OpenClaw `v2026.9.6` 的真实载体映射；
4. 明确 TOOLS 契约不等于工具权限、HEARTBEAT 契约不等于调度器、MEMORY 契约不等于数据库；
5. 明确文本契约不能绕过 Policy/Approval/Sandbox/Auth；
6. 给出岗位级最小契约集，而不是把所有规则拼成一个总提示词；
7. 给出至少两组冲突注入的裁决结果，供 C06 在实际 Prompt/Policy/Runtime 三层验证。

在上述输入完成前，允许继续做 C06 事实研究、组件图草案和测试夹具；**不允许**冻结 Prompt 装配图、Workspace 载体、Heartbeat/Memory 落位或“最小可训单体”正式清单。

## 11. 待正式 C06 作者确认的开放问题

| ID | 问题 | 当前状态 | 处理建议 |
|---|---|---|---|
| U-C06-01 | 六层图中“消息层”画在控制层前还是后，才能同时表达外部准入与 Gateway 集中控制？ | `INFERENCE` | 用两张图：组件分层图 + 时序数据流图，避免一张图强行表达所有关系 |
| U-C06-02 | 哪些 OpenClaw 配置默认值值得进入正文？ | `UNKNOWN` | 稳定正文不写数值；固定版命令/默认值放版本框或附录 |
| U-C06-03 | Hermes `v0.20.1` 是否已具备动态文档中全部 Gateway/SQLite recovery/fallback chain 行为？ | `UNKNOWN` | 固定到 `f80f453` 做源码级逐项核验后再写版本表 |
| U-C06-04 | OpenClaw Cloud Worker 在目标读者环境中是否为默认可用产品能力？ | `UNKNOWN` | 正文写“可选执行位置”；建立清单要求先探测 capability，不做默认假设 |
| U-C06-05 | MCP Server 的具体 transport、OAuth、resource/prompt 能力如何进入训练？ | 后章定义 | C14 处理；C06 只保留执行位置与策略不绕过原则 |
| U-C06-06 | Session/Memory/Compaction 的保留、删除、隐私和成本门禁 | 后章定义 | C13 处理，C06 不写数值规则 |
| U-C06-07 | Heartbeat/Cron/Standing Order 的调度优先级与安静策略 | 后章定义 | C16 处理，C06 只定位自动化进入 Gateway/Session 的位置 |
| U-C06-08 | A2A/Handoff 与内部 Binding/Session routing 的统一关系 | 后章定义 | C20 处理，禁止在 C06 用“路由”一词抹平不同协议 |

## 12. 证据目录

所有 URL 核验日期均为 2026-09-30。OpenClaw 的固定提交链接是本包的主证据；动态官网仅用于发现，不作为替代。

### 12.1 OpenClaw 固定提交与官方文档

| ID | 来源 | 标签 | URL |
|---|---|---|---|
| OC-REL | OpenClaw 2026.9.6 release | `VERSION-FACT` | https://github.com/openclaw/openclaw/releases/tag/v2026.9.6 |
| OC-ARCH | Gateway architecture | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/architecture.md |
| OC-LOOP | Agent loop | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/agent-loop.md |
| OC-FAILOVER | Model failover | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/model-failover.md |
| OC-WORKSPACE | Agent workspace | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/agent-workspace.md |
| OC-SESSION | Session management | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/session.md |
| OC-MEMORY | Memory | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/memory.md |
| OC-QUEUE | Command queue | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/queue.md |
| OC-STEER | Queue steering | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/queue-steering.md |
| OC-MESSAGES | Messages | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/messages.md |
| OC-BINDING | Agent bindings | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/agent-bindings.md |
| OC-PAIRING | Channel and Node pairing | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/channels/pairing.md |
| OC-RETRY | Channel retry policy | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/retry.md |
| OC-TOOLS | Tools | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/tools/index.md |
| OC-BROWSER | Browser | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/tools/browser.md |
| OC-NODE | Nodes | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/nodes/index.md |
| OC-WORKER | Cloud workers | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/cloud-workers.md |
| OC-MCP | MCP | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/tools/mcp.md |
| OC-NODE-MCP | Node-hosted MCP and skills | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/nodes/mcp-and-skills.md |
| OC-TRUST | Security trust model | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/security/trust-model.md |
| OC-PERM | Tool and agent permissions | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/security/tool-permissions.md |
| OC-APPROVAL | Exec approvals | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/tools/exec-approvals.md |
| OC-SANDBOX | Sandbox modes, scope and backend | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/sandboxing/modes-scope-and-backend.md |
| OC-SECRETS | Secrets runtime model | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/secrets/runtime-model.md |
| OC-AUDIT | Running the security audit | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/security/running-the-audit.md |
| OC-RECOVERY | Restart recovery | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/restart-recovery.md |
| OC-STATE | Versioned state and guarded upgrades | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/start/why-openclaw/versioned-state-guarded-upgrades.md |
| OC-TOOLS-RET | Retired TOOLS.md template | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/reference/templates/TOOLS.md |
| OC-HB-RET | Retired HEARTBEAT.md migration guide | `VERSION-FACT` | https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/reference/templates/HEARTBEAT.md |

### 12.2 Hermes 官方来源

| ID | 来源 | 标签 | URL |
|---|---|---|---|
| HE-REL | Hermes Agent v0.20.1 release | `VERSION-FACT` | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.13 |
| HE-ARCH | Architecture | `DYNAMIC-DOC` | https://hermes-agent.nousresearch.com/docs/developer-guide/architecture |
| HE-PROVIDER | Provider Runtime Resolution | `DYNAMIC-DOC` | https://hermes-agent.nousresearch.com/docs/developer-guide/provider-runtime |

### 12.3 Muse 官方来源

| ID | 来源 | 标签 | URL |
|---|---|---|---|
| MUSE-NEWS | Meta Newsroom, Introducing Muse | `VENDOR-CLAIM` | https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/ |
| MUSE-SEC | Meta AI Research, How We Built Safety Into Muse | `VENDOR-CLAIM` | https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse |

### 12.4 旧稿冲突来源

| ID | 来源 | 标签 | 路径 |
|---|---|---|---|
| LEGACY-FACT | 旧候选稿实测事实底稿 | `LOCAL-HISTORICAL-SNAPSHOT` | `_appendix-api/00-实测事实底稿.md` |
| LEGACY-SCHEMA | 旧候选稿配置 Schema | `LOCAL-HISTORICAL-SNAPSHOT` | `_appendix-api/02-config-schema.md` |

旧稿只用于发现冲突，不能反向证明当前平台事实。任何旧稿命令、字段、数量或路径进入 C06 正文前，都必须重新对照固定版官方文档或固定提交源码。

## 13. 交付判定

本前置研究包已经提供：固定版来源锚点、六层逐组件事实身份、执行位置、信任边界、失败/停止/恢复、后章定义权、Hermes 非同构映射、Muse 厂商声明边界、旧稿冲突/禁写项、最小可训单体草案与三类故障注入计划。

它**没有**完成：C05 契约输入、Hermes `f80f453` 的逐文件版本审计、正式架构图、正式数据流图、正式单体清单、练习、正文、事实审校或章节批准。因此状态保持 `research_preflight`。

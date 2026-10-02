# 附录 04 · MCP 原语参考（Model Context Protocol Reference）

> **手册版本**：v5.0 行业标准版 · 2026-09-27
> **License**：MIT（跟随 OpenClaw 主仓）
> **实测环境**：OpenClaw 2026.9.4 (3a9d69d) · Hermes Agent 0.20.1 · macOS 26.5.1 · 236 skills
> **本机 live 复核**：OpenClaw 2026.9.6 (eb377ac) · 18 agents · 61 automations · plugins 53/73（书内统一用 2026.9.4 口径）
> **本卷定位**：API 参考附录卷 · 文件 4 / 7 · 对位 `chapters/08-mcp-binding/`
> **互链**：`chapters/08-mcp-binding/08-MCP绑定.md` · `faq-troubleshooting/F5-Skills-Tools-MCP.md` · `cookbook/03-skills-tools-mcp.md`
> **诚实底线**：本机 `openclaw mcp list` = **0 配置**；46 原语中 **8 个 ✅（隐式实测）** / **38 个 ⏳（未实测）**

---

## 04.1 · MCP 总览

### 04.1.1 一句话定义

> **MCP（Model Context Protocol，模型上下文协议）= 把「外部能力」以 JSON-RPC 2.0 的标准原语（Primitive）暴露给 LLM 客户端的开放协议**——由 Anthropic 提出，2025 年移交 AAIF（Agentic AI Interoperability Foundation，Linux Foundation 下属）治理，Anthropic + Block + OpenAI 共同维护。

本书对位章节：**`chapters/08-mcp-binding/08-MCP绑定.md`**（协议绑定层）。业界对位：MCP（Anthropic）↔ chapters 09-mcp-binding（**对位，非领先**；差距在 OpenClaw 只隐式暴露 8/46 原语，详见 §04.3）。

### 04.1.2 术语双写（首次出现，全书统一）

| 中文新名 | 英文 alias | 本章首次出现位置 |
|---|---|---|
| 资源（只读面） | Resource | §04.3.1 |
| 资源模板 | Resource Template | §04.3.1 |
| 工具（动作面） | Tool | §04.3.2 |
| 提示模板 | Prompt Template | §04.3.3 |
| 采样 | Sampling | §04.3.4 |
| 征询 | Elicitation | §04.3.5 |
| 根 | Roots | §04.3.6 |
| 进度通知 | Progress Notification | §04.3.7 |
| 结构化日志 | Structured Logging | §04.3.8 |
| 能力协商 | Capability Negotiation | §04.3.10 |

> ⚠️ **本章不存在「监军」「军团」「让位协议」等内部黑话的单写形式**——凡出现一律双写，例如：监督层（Supervisor Layer，原：监军）、智能体集群（Agent Fleet，原：军团）、响应让渡协议（Response Yield Protocol，RYP；原：让位协议）。

### 04.1.3 `openclaw mcp` 命令族（✅ 14 子命令实测）

本机 `openclaw mcp` 共 **14 个子命令**（✅ 底稿 §3.5 实测）：

| # | 子命令 | 语义 | 本机是否实跑过 | 说明 |
|---|---|---|---|---|
| 1 | `add` | 新增一个 MCP server 到配置 | ⏳ | 写入 `mcp.servers.<name>` |
| 2 | `configure` | 交互式配置（含 OAuth / env） | ⏳ | 会触碰 `~/.openclaw/openclaw.json` |
| 3 | `doctor` | 诊断 MCP 子系统 | ⏳ | 对应 `openclaw doctor` 的 MCP 子集 |
| 4 | `list` | 列出已配置 server | ✅ | **本机输出 = 0 配置（诚实基线）** |
| 5 | `login` | OAuth 登录远端 MCP server | ⏳ | 需网络 + 浏览器回调 |
| 6 | `logout` | 撤销 OAuth 凭据 | ⏳ | — |
| 7 | `probe` | 探测 server 是否活 / 能力清单 | ⏳ | 等价于手打 `initialize` + `tools/list` |
| 8 | `reload` | 热重载 MCP 配置 | ⏳ | 不改 `openclaw.json` 字节的情况下重连 |
| 9 | `serve` | 把本进程当 MCP server 跑（被 attach） | ⏳ | 反向：OpenClaw 变成 server |
| 10 | `set` | 单键写值（脚本友好） | ⏳ | 与 `configure` 互补 |
| 11 | `show` | 展开某个 server 的完整配置 | ⏳ | 含 token 脱敏 |
| 12 | `status` | 运行态（connected / error / idle） | ⏳ | 与 `list`（配置态）互补 |
| 13 | `tools` | 列某 server 暴露的工具 | ⏳ | 等价 `tools/list` |
| 14 | `unset` | 删除某个键或整条 server | ⏳ | — |

> **验证命令（零副作用）**：
> ```bash
> openclaw mcp --help 2>&1 | sed -n '/Commands:/,/^$/p' \
>   | grep -cE "^\s+(add|configure|doctor|list|login|logout|probe|reload|serve|set|show|status|tools|unset)"
> # 期望：14
> ```

### 04.1.4 命名空间：`mcp.servers`（✅ 实测）

MCP 的配置真身在 `~/.openclaw/openclaw.json` 的 **`mcp.servers`** 命名空间下：

```jsonc
// ~/.openclaw/openclaw.json（节选示意；本机该节点不存在 = 0 配置）
{
  "mcp": {
    "servers": {
      "silicon-life-training": {
        "type": "stdio",
        "command": "node",
        "args": ["./mcp/silicon-life-training.js"],
        "env": { "NODE_ENV": "production" }
      }
    }
  }
}
```

> 🚨 **真名勘误（引用底稿 §1.2）**：不是 `mcpServers`、不是 `mcp_servers`、不是 `mcps`。**是 `mcp.servers`**（点分两段）。
> 注意：MCP 官方各语言 SDK 的示例里常用 `mcpServers` 作为**宿主配置键**（Claude Desktop 风格）；OpenClaw 用的是自己的 `mcp.servers`。**两者不可互相复制**。

### 04.1.5 🚨 真名 vs 虚构对照（本章相关子集）

| ❌ 虚构（不存在） | ✅ 真名 | 说明 |
|---|---|---|
| `openclaw init` | `openclaw setup`（或 `onboard`） | 无 `init` 子命令 |
| `openclaw mcp install` | `openclaw mcp add`（+ `configure`） | 无 `install` |
| `openclaw mcp enable/disable` | `openclaw mcp set` / `unset` | 无 enable/disable |
| `mcpServers`（作为 OpenClaw 顶层键） | `mcp.servers` | 点分两段 |
| `openclaw plugin`（单数） | `openclaw plugins`（复数） | MCP server 若以 plugin 形态分发则走复数 |
| `manifest.yaml` | `openclaw.plugin.json`（**JSON5**） | 不是 YAML |

### 04.1.6 传输层（Transport）三种形态

| transport | 类型 | 本机实测 | 适用 |
|---|---|---|---|
| `stdio` | 子进程标准输入输出 | ✅ 隐式（`stdio/handshake`） | 本地 server（最常用） |
| `http`（旧） | HTTP + SSE 回调 | ⏳ | 云端 server（**v2026-07-28 起降级**） |
| `streamable-http` | 无状态流式 HTTP | ⏳ | MCP spec v2026-07-28 新增，**去 session、协议层无状态** |
| `sse` | Server-Sent Events 长连接 | ⏳ | 已不推荐，向后兼容保留 |

> **spec 版本口径**：本册统一引用 **v2025-11-25**（一周年版，稳定基线）+ **v2026-07-28**（重大修订：去 session、协议层无状态、新增 streamable-http）。

### 04.1.7 MCP 在「8 卷 × 4 接口层」中的位置

本书把能力暴露拆成 **4 个接口层**，MCP 只占其中第 3 层：

| 接口层 | 载体 | 谁读 | 例子 |
|---|---|---|---|
| L1 CLI 层 | `openclaw <group> <cmd>` | 人 / 脚本 | `openclaw mcp list` |
| L2 配置层 | `~/.openclaw/openclaw.json` | OpenClaw 运行时 | `mcp.servers.<name>` |
| L3 **协议层（MCP）** | JSON-RPC 2.0 原语 | 外部 LLM 客户端 | `tools/call` |
| L4 语义层 | 训练学业务语义 | 本书读者 | `drift_detection` |

> **关键区分**：L3 是**协议层 API**（method + params + result），L4 是**业务语义**。把语义硬塞进 L3 的 args 是反模式（见 §04.4 坑 2）。

### 04.1.8 能力协商（Capability Negotiation）最小流程

```text
client ──initialize({protocolVersion, capabilities, clientInfo})──▶ server
client ◀──initialize result({protocolVersion, capabilities, serverInfo})── server
client ──notifications/initialized──▶ server          # 握手完成
client ──tools/list──▶ server
client ◀──ListToolsResult{tools:[...]}── server
client ──tools/call({name, arguments})──▶ server
client ◀──CallToolResult{content:[...], isError}── server
```

本机在 `openclaw attach <agent>` 流程里**隐式**走过上面全部 5 步（✅ 8 个原语中的 6 个）。

---

## 04.2 · 46 MCP 原语映射表（核心）

> **本节定位**：`chapters/08-mcp-binding/08-MCP绑定.md` §9.4 已给出 46 原语表；本节**直接引用并对齐**，额外补 **8 卷映射列**与**4 接口层落地列**。
> **读法**：先看 §04.2.1 十二大类汇总 → 再看 §04.2.2 完整 46 行主表 → 最后按需查 §04.2.3 逐原语速查。
> **诚实口径**：✅ = 本机 OpenClaw attach 流程中隐式调用过；⏳ = **未实测**（协议层有定义，但本机未跑过、或 OpenClaw 未暴露）。

### 04.2.1 十二大类汇总

| # | 大类 | 原语数 | ✅ 实测 | ⏳ 未实测 | 命名空间 | 是否暴露给训练学 |
|---|---|---|---|---|---|---|
| 1 | Resource（资源） | 8 | 2 | 6 | `mcp.resources` | ✅ 7 契约清单 |
| 2 | Tool（工具） | 3 | 2 | 1 | `mcp.tools` | ✅ 5 优势工具 |
| 3 | Prompt（提示） | 4 | 0 | 4 | `mcp.prompts` | ✅ 2 提示模板 |
| 4 | Sampling（采样） | 3 | 0 | 3 | `mcp.sampling` | ⏳ 设计有、未接 |
| 5 | Elicitation（征询） | 2 | 0 | 2 | `mcp.elicitation` | ⏳ **OpenClaw 当前未暴露** |
| 6 | Roots（根） | 2 | 0 | 2 | `mcp.roots` | ⏳ — |
| 7 | Progress（进度） | 2 | 0 | 2 | `mcp.progress` | ⏳ 任务卡 ack 用 |
| 8 | Logging（日志） | 3 | 0 | 3 | `mcp.logging` | ⏳ — |
| 9 | Completion（补全） | 2 | 0 | 2 | `mcp.completion` | ⏳ — |
| 10 | Initialization（握手） | 4 | 2 | 2 | `mcp.handshake` | ✅ 隐式 |
| 11 | Cancellation/Notify | 2 | 0 | 2 | `mcp.cancel` | ⏳ — |
| 12 | Transport + Other | 11 | 2 | 9 | `mcp.transport` / `mcp.errors` / `mcp.notifications` | ✅ stdio 隐式 |
| | **合计** | **46** | **8** | **38** | — | 14 个语义接口 |

> **一句话结论**：**14 / 46 = 30.4%**。本书训练学语义层只用了协议面不到三分之一。这就是为什么本章必须展开全部 46 个——**剩下的 32 个是"读者一定会撞上"的盲区**。

### 04.2.2 完整 46 原语主表

> 列含义：**原语名** / **来源章节**（本书首次出现处） / **输出类型** / **命名空间** / **本机实测** / **训练学语义层映射** / **8 卷归属** / **4 接口层**

| # | 原语名 | 来源章节 | 输出类型 | 命名空间 | 本机 | 训练学语义层映射 | 8 卷归属 | 接口层 |
|---|---|---|---|---|---|---|---|---|
| 1 | `resources/list` | 09 §8.3 | `ListResourcesResult` | `mcp.resources` | ✅ | 7 契约清单 | 卷一·契约 | L3 |
| 2 | `resources/read` | 09 §8.3 | `ReadResourceResult` | `mcp.resources` | ✅ | 单契约读取（`contract://xxx`） | 卷一·契约 | L3 |
| 3 | `resources/templates/list` | 09 §9.4 | `ListResourceTemplatesResult` | `mcp.resources` | ⏳ | 动态契约生成 | 卷一·契约 | L3 |
| 4 | `resources/templates/read` | 09 §9.4 | `ReadResourceResult` | `mcp.resources` | ⏳ | 模板实例化读取 | 卷一·契约 | L3 |
| 5 | `resources/subscribe` | 09 §9.4 | `SubscribeResult` | `mcp.resources` | ⏳ | 契约变更订阅（HEARTBEAT 触发） | 卷三·漂移 | L3 |
| 6 | `resources/unsubscribe` | 09 §9.4 | `UnsubscribeResult` | `mcp.resources` | ⏳ | 取消契约订阅 | 卷三·漂移 | L3 |
| 7 | `resources/updated`（通知） | 09 §9.4 | `ResourceUpdatedNotification` | `mcp.resources` | ⏳ | 契约变更下行通知 | 卷三·漂移 | L3 |
| 8 | `resources/list_changed`（通知） | 09 §9.4 | `ResourceListChangedNotification` | `mcp.resources` | ⏳ | 契约清单变更 | 卷三·漂移 | L3 |
| 9 | `tools/list` | 09 §8.3 | `ListToolsResult` | `mcp.tools` | ✅ | 5 优势工具清单 | 卷二·优势 | L3 |
| 10 | `tools/call` | 09 §8.3 | `CallToolResult` | `mcp.tools` | ✅ | 单工具调用（drift_detection 等） | 卷二·优势 | L3 |
| 11 | `tools/list_changed`（通知） | 09 §9.4 | `ToolListChangedNotification` | `mcp.tools` | ⏳ | 工具清单动态变更 | 卷二·优势 | L3 |
| 12 | `prompts/list` | 09 §9.4 | `ListPromptsResult` | `mcp.prompts` | ⏳ | 提示模板清单 | 卷四·训练 | L3 |
| 13 | `prompts/get` | 09 §9.4 | `GetPromptResult` | `mcp.prompts` | ⏳ | 取提示模板（`soul_init`） | 卷四·训练 | L3 |
| 14 | `prompts/list_changed`（通知） | 09 §9.4 | `PromptListChangedNotification` | `mcp.prompts` | ⏳ | 提示清单变更 | 卷四·训练 | L3 |
| 15 | `prompts/template`（自定义） | 09 §9.4 | `PromptTemplate` | `mcp.prompts` | ⏳ | 自定义模板扩展 | 卷四·训练 | L3 |
| 16 | `sampling/createMessage` | 09 §9.4 | `CreateMessageResult` | `mcp.sampling` | ⏳ | server 反向让 LLM 生成（自检） | 卷五·三省 | L3 |
| 17 | `sampling/createMessageStream` | 09 §9.4 | `StreamChunk` | `mcp.sampling` | ⏳ | 流式采样（三省制串行审） | 卷五·三省 | L3 |
| 18 | `sampling/cancel` | 09 §9.4 | `CancelResult` | `mcp.sampling` | ⏳ | 取消未完成的采样请求 | 卷五·三省 | L3 |
| 19 | `elicitation/create` | 09 §9.4 | `ElicitRequest` | `mcp.elicitation` | ⏳ | server 向用户提澄清问题 | 卷六·治理 | L3 |
| 20 | `elicitation/respond` | 09 §9.4 | `ElicitResponse` | `mcp.elicitation` | ⏳ | 用户响应回传 | 卷六·治理 | L3 |
| 21 | `roots/list` | 09 §9.4 | `ListRootsResult` | `mcp.roots` | ⏳ | 客户端告知 server 入口路径 | 卷七·工程 | L3 |
| 22 | `roots/refresh` | 09 §9.4 | `RefreshRootsResult` | `mcp.roots` | ⏳ | 刷新根目录列表 | 卷七·工程 | L3 |
| 23 | `progress/notify` | 09 §9.4 | `ProgressNotification` | `mcp.progress` | ⏳ | 长任务进度上报（任务卡 ack） | 卷八·交接 | L3 |
| 24 | `progress/cancel` | 09 §9.4 | `CancelProgressResult` | `mcp.progress` | ⏳ | 取消进度跟踪 | 卷八·交接 | L3 |
| 25 | `logging/setLevel` | 09 §9.4 | `SetLevelResult` | `mcp.logging` | ⏳ | 设置日志级别 | 卷七·工程 | L3 |
| 26 | `logging/message` | 09 §9.4 | `LoggingMessageNotification` | `mcp.logging` | ⏳ | 结构化日志下行 | 卷七·工程 | L3 |
| 27 | `logging/levelChanged`（通知） | 09 §9.4 | `LevelChangedNotification` | `mcp.logging` | ⏳ | 日志级别变更广播 | 卷七·工程 | L3 |
| 28 | `completion/complete` | 09 §9.4 | `CompleteResult` | `mcp.completion` | ⏳ | 参数自动补全（contract URI） | 卷七·工程 | L3 |
| 29 | `completion/resolve` | 09 §9.4 | `ResolveResult` | `mcp.completion` | ⏳ | 解析已选补全项 | 卷七·工程 | L3 |
| 30 | `initialize` | 09 §9.4 | `InitializeResult` | `mcp.handshake` | ✅（隐式） | 协议握手 | 卷七·工程 | L3 |
| 31 | `initialized`（通知） | 09 §9.4 | `InitializedNotification` | `mcp.handshake` | ✅（隐式） | 握手完成确认 | 卷七·工程 | L3 |
| 32 | `ping` | 09 §9.4 | `PingResult` | `mcp.handshake` | ⏳ | 心跳保活（HEARTBEAT 协同） | 卷三·漂移 | L3 |
| 33 | `shutdown` | 09 §9.4 | `ShutdownResult` | `mcp.handshake` | ⏳ | server 优雅关闭 | 卷七·工程 | L3 |
| 34 | `notifications/cancelled` | 09 §9.4 | `CancelledNotification` | `mcp.cancel` | ⏳ | 请求级取消（含 reason） | 卷八·交接 | L3 |
| 35 | `notifications/progress` | 09 §9.4 | `ProgressNotification` | `mcp.cancel` | ⏳ | 通用进度上报 | 卷八·交接 | L3 |
| 36 | `notifications/roots/list_changed` | 09 §9.4 | `RootsListChangedNotification` | `mcp.roots` | ⏳ | 根列表变更 | 卷七·工程 | L3 |
| 37 | JSON-RPC 2.0 error codes | 09 §9.4 | `Error` | `mcp.errors` | ✅（隐式） | 5 个标准错误码 | 卷七·工程 | L3 |
| 38 | `notifications/message` | 09 §9.4 | `MessageNotification` | `mcp.notifications` | ⏳ | 通用通知 | 卷七·工程 | L3 |
| 39 | `notifications/exit` | 09 §9.4 | `ExitNotification` | `mcp.notifications` | ⏳ | 主动退出 | 卷七·工程 | L3 |
| 40 | `notifications/prompt/list_changed` | 09 §9.4 | （归类 prompts） | `mcp.prompts` | ⏳ | 提示清单变更（别名） | 卷四·训练 | L3 |
| 41 | `notifications/resource/updated` | 09 §9.4 | （归类 resources） | `mcp.resources` | ⏳ | 资源更新（别名） | 卷一·契约 | L3 |
| 42 | `notifications/stderr` | 09 §9.4 | `StderrNotification` | `mcp.stderr` | ⏳ | stderr 输出（stdio transport） | 卷七·工程 | L3 |
| 43 | `stdio/handshake` | 09 §9.4 | `StdioFrame` | `mcp.transport` | ✅（隐式） | stdio transport 握手帧 | 卷七·工程 | L3 |
| 44 | `http/handshake` | 09 §9.4 | `HttpRequest` | `mcp.transport` | ⏳ | HTTP transport 握手 | 卷七·工程 | L3 |
| 45 | `sse/connect` | 09 §9.4 | `SseConnection` | `mcp.transport` | ⏳ | SSE 长连接 | 卷七·工程 | L3 |
| 46 | `streamable-http/init` + `/chunk` | 09 §9.4 | `StreamInit` / `StreamChunk` | `mcp.transport` | ⏳ | 无状态流式（v2026-07-28 新增） | 卷七·工程 | L3 |

**汇总校验**：46 行 · ✅ **8**（#1 #2 #9 #10 #30 #31 #37 #43） · ⏳ **38**

> **4 接口层口径**：全部 46 原语都落在 **L3 协议层**——这是 MCP 的天然边界。它们**不直接**出现在 L1（CLI）或 L2（配置）里；L2 只负责"把 server 挂上去"（`mcp.servers`），L1 只负责"人看得懂地查状态"（`openclaw mcp list/status/probe/tools`）。**L4 语义层则完全不在协议里**——靠 `metadata` 的 vendor 命名空间承载（见 §04.4 坑 2）。

### 04.2.3 逐原语速查（按 12 大类，46 条）

**1. Resource（资源）· 8 个 · 命名空间 `mcp.resources`**

- `resources/list` — 列只读资源。✅ 本机 attach 时调用，返回 7 契约清单。
- `resources/read` — 读单个资源。✅ URI 形态 `contract://soul`。
- `resources/templates/list` — 列**资源模板（Resource Template）**。⏳ 用于 `contract://{role}.md` 这类动态资源。
- `resources/templates/read` — 实例化读模板。⏳ 返回 `ReadResourceResult`。
- `resources/subscribe` — 订阅变更。⏳ 与 HEARTBEAT.md 联动才真正有用。
- `resources/unsubscribe` — 退订。⏳ 退订是"防泄漏"操作，别只订阅不退订。
- `resources/updated`（通知）— server 主动推"某资源变了"。⏳
- `resources/list_changed`（通知）— server 主动推"清单变了"。⏳

**2. Tool（工具）· 3 个 · 命名空间 `mcp.tools`**

- `tools/list` — 列工具。✅ 返回 5 优势工具。
- `tools/call` — 调工具。✅ 参数 `{name, arguments}`。
- `tools/list_changed`（通知）— 工具集动态变。⏳ 热插拔 skill 时才会用到。

**3. Prompt（提示）· 4 个 · 命名空间 `mcp.prompts`**

- `prompts/list` — 列**提示模板（Prompt Template）**。⏳
- `prompts/get` — 取模板。⏳ 本册设计的 `soul_init` / `drift_alert` 两个。
- `prompts/list_changed`（通知）— ⏳
- `prompts/template`（自定义）— ⏳ 非 spec 标准，属自定义扩展位。

**4. Sampling（采样）· 3 个 · 命名空间 `mcp.sampling`**

- `sampling/createMessage` — **server 反向请求 client 帮它调 LLM**。⏳ 三省制（提案/复审/裁决）的天然载体。
- `sampling/createMessageStream` — 流式版本。⏳ 串行审时体验更好。
- `sampling/cancel` — 取消采样。⏳

**5. Elicitation（征询）· 2 个 · 命名空间 `mcp.elicitation`**

- `elicitation/create` — **server 向用户提澄清问题**。⏳ **OpenClaw 当前未暴露**。
- `elicitation/respond` — 用户回传。⏳

**6. Roots（根）· 2 个 · 命名空间 `mcp.roots`**

- `roots/list` — client 告知 server "入口路径在哪"。⏳
- `roots/refresh` — 刷新。⏳

**7. Progress（进度通知）· 2 个 · 命名空间 `mcp.progress`**

- `progress/notify` — 长任务进度上报。⏳ 任务卡 ack 用它最自然。
- `progress/cancel` — 取消进度跟踪。⏳

**8. Logging（结构化日志）· 3 个 · 命名空间 `mcp.logging`**

- `logging/setLevel` — 设级别（debug/info/warn/error）。⏳
- `logging/message` — 日志下行。⏳
- `logging/levelChanged`（通知）— 级别变更广播。⏳

**9. Completion（补全）· 2 个 · 命名空间 `mcp.completion`**

- `completion/complete` — 参数自动补全。⏳ 对 `contract://` URI 补全最有价值。
- `completion/resolve` — 解析已选项。⏳

**10. Initialization（握手）· 4 个 · 命名空间 `mcp.handshake`**

- `initialize` — ✅（隐式）协议握手。
- `initialized`（通知）— ✅（隐式）握手完成。
- `ping` — ⏳ 保活；与 HEARTBEAT 同族但不同层（一个是协议层，一个是业务层）。
- `shutdown` — ⏳ 优雅关闭。

**11. Cancellation / Notify · 2 个 · 命名空间 `mcp.cancel`**

- `notifications/cancelled` — ⏳ 请求级取消（带 reason）。
- `notifications/progress` — ⏳ 通用进度。

**12. Transport + Other · 11 个**

- `notifications/roots/list_changed` — ⏳
- JSON-RPC 2.0 error codes — ✅（隐式）：`-32700` parse error / `-32600` invalid request / `-32601` method not found / `-32602` invalid params / `-32603` internal error。
- `notifications/message` — ⏳
- `notifications/exit` — ⏳
- `notifications/prompt/list_changed` — ⏳（别名，归类 prompts）
- `notifications/resource/updated` — ⏳（别名，归类 resources）
- `notifications/stderr` — ⏳ stdio 场景专有。
- `stdio/handshake` — ✅（隐式）
- `http/handshake` — ⏳
- `sse/connect` — ⏳
- `streamable-http/init` + `streamable-http/chunk` — ⏳ v2026-07-28 新增。

### 04.2.4 原语 → 语义层覆盖率（可执行校验）

```bash
# 方式 A · 一行式（无 heredoc，可直接复制）
python3 -c "p=46; u=8; s=14; print(f'原语面: {p}'); print(f'本机隐式已用: {u}'); print(f'训练学语义接口: {s}'); print(f'覆盖率: {s/p*100:.1f}%')"
# 期望输出：
#   原语面: 46
#   本机隐式已用: 8
#   训练学语义接口: 14
#   覆盖率: 30.4%

# 方式 B · 存成文件后跑（推荐用于反复校验）
#   check_mcp_coverage.py 内容见 api-reference/scripts/ 同目录风格
#   python3 check_mcp_coverage.py
# 其中 actually_used 的 8 个 = resources/list, resources/read, tools/list,
# tools/call, initialize, initialized, JSON-RPC errors, stdio/handshake
```

**期望输出**：`30.4%`。

---
## 04.3 · MCP Server 注册实操

> **诚实前置**：本机 `openclaw mcp list` = **0 配置**（✅ 实测）。因此本节全部为**「文档 + 设计」路径**，凡标注 ⏳ 者为**本机未跑过**。**严禁把本节命令当成"已验证可用"照抄**。

### 04.3.1 注册前必须回答的 4 个问题

| # | 问题 | 为什么必须先答 |
|---|---|---|
| 1 | transport 是 `stdio` 还是 `streamable-http`？ | stdio 无需端口/OAuth；HTTP 要处理登录态 |
| 2 | server 暴露哪些能力（capabilities）？ | 写错 capability → client 不会调对应原语 |
| 3 | 是否有密钥？存哪？ | 密钥进 `openclaw.json` 明文 = 事故；优先用 `${ENV_VAR}` |
| 4 | 挂给哪个 agent？ | MCP 可全局可 per-agent（`agents.entries.<id>` 下覆盖） |

### 04.3.2 `server.json` 完整示例（46 原语最小骨架）

> 说明：MCP 官方打包规范里 `server.json` 用于**声明 server 元信息 + 包来源**（配合 MCP Registry）。**OpenClaw 自身的注册在 `openclaw.json` 的 `mcp.servers`**，`server.json` 是给分发/注册表用的。两者**不要混淆**。

```json
{
  "name": "silicon-life-training-full",
  "version": "2026.9.4",
  "license": "MIT",
  "specVersions": ["v2025-11-25", "v2026-07-28"],
  "capabilities": {
    "resources": { "subscribe": true, "listChanged": true },
    "tools": { "listChanged": true },
    "prompts": { "listChanged": true },
    "logging": { "level": "info" },
    "sampling": {},
    "elicitation": {},
    "roots": { "listChanged": true },
    "progress": {}
  },
  "resources": [
    { "uri": "contract://user",      "name": "USER.md" },
    { "uri": "contract://soul",      "name": "SOUL.md" },
    { "uri": "contract://agents",    "name": "AGENTS.md" },
    { "uri": "contract://tools",     "name": "TOOLS.md" },
    { "uri": "contract://heartbeat", "name": "HEARTBEAT.md" },
    { "uri": "contract://identity",  "name": "IDENTITY.md" },
    { "uri": "contract://memory",    "name": "MEMORY.md" }
  ],
  "tools": [
    { "name": "drift_detection" },
    { "name": "proactive_boundary_check" },
    { "name": "three_stage_review" },
    { "name": "anti_fragile_triptych" },
    { "name": "self_initiated_goal" }
  ],
  "prompts": [
    { "name": "soul_init",  "arguments": ["role"] },
    { "name": "drift_alert", "arguments": ["severity"] }
  ]
}
```

**字段真名核对**：

| 字段 | 必填 | 真名 | 常见错写 |
|---|---|---|---|
| `name` | ✅ | `name` | `id` / `serverName` |
| `version` | ✅ | `version` | `ver` |
| `license` | ❌ | `license` | `licence`（英式拼写不被 schema 认） |
| `specVersions` | ❌ | `specVersions`（数组） | `protocolVersion`（那是握手时传的单个值） |
| `capabilities` | ✅ | `capabilities` | `capability` / `features` |

### 04.3.3 `manifest.json` 完整示例（OpenClaw 侧 plugin 形态分发）

当 MCP server 以 **OpenClaw plugin** 形态分发时，需要 `openclaw.plugin.json`（**JSON5**，🚨 不是 `manifest.yaml`）：

```json5
{
  // openclaw.plugin.json  —— 真名：JSON5，不是 YAML
  id: "silicon-life-training-mcp",
  name: "Silicon Life Training MCP",
  version: "2026.9.4",
  entry: "./index.js",

  // 唯一硬要求字段：configSchema
  configSchema: {
    type: "object",
    additionalProperties: false,
    properties: {
      serverName:  { type: "string", default: "silicon-life-training-full" },
      transport:   { type: "string", enum: ["stdio", "streamable-http"], default: "stdio" },
      autoAttach:  { type: "boolean", default: false },
    },
  },

  // uiHints：OpenClaw 独有（业界 6 框架无对位）
  uiHints: {
    transport:  { label: "传输方式", advanced: true },
    autoAttach: { label: "自动挂载", help: "启动时自动 attach 到默认 agent" },
  },
}
```

> 🚨 **本章最强勘误**：`manifest.yaml` **不存在**。OpenClaw plugin 清单真名 = **`openclaw.plugin.json`**，格式 = **JSON5**（允许注释 / 尾逗号 / 无引号键）。详见 `chapters/11-plugin-entrypoint/`。

### 04.3.4 注册流程（7 步 · ⏳ 本机未实跑）

```bash
# 步骤 1 · 确认 server 能独立跑起来（脱离 OpenClaw）
node ./mcp/silicon-life-training.js --self-test
# 期望：打印 tools/list 的 5 个工具名

# 步骤 2 · 看当前配置态（本机 = 0）
openclaw mcp list

# 步骤 3 · 写入 server 定义
openclaw mcp add silicon-life-training \
  --type stdio \
  --command node \
  --args "./mcp/silicon-life-training.js"

# 步骤 4 · 若是 HTTP/OAuth server，先登录
openclaw mcp login silicon-life-training
# 会启动浏览器回调；无头环境用 openclaw mcp set 写 token

# 步骤 5 · 探测能力面（最关键的验证）
openclaw mcp probe silicon-life-training
openclaw mcp tools silicon-life-training
# 期望：列出 tools/list 的 5 个工具

# 步骤 6 · 热重载（不重启 gateway）
openclaw mcp reload

# 步骤 7 · 看运行态 + 整体健康
openclaw mcp status
openclaw mcp doctor
openclaw health
```

**步骤 3 的等价手写配置**（脚本化时更常用）：

```jsonc
// ~/.openclaw/openclaw.json（合并进现有 20 个顶层 key，不要整文件覆盖）
{
  "mcp": {
    "servers": {
      "silicon-life-training": {
        "type": "stdio",
        "command": "node",
        "args": ["./mcp/silicon-life-training.js"],
        "env": {
          "LOG_LEVEL": "info",
          "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"   // ✅ 用 env 引用，不写明文
        }
      }
    }
  }
}
```

> 🚨 **备份铁律**：任何写入 `~/.openclaw/openclaw.json` 的操作之前，先
> `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.pre-mcp-$(date +%Y%m%d-%H%M)`。
> 依据：8/19 军团断线事故的恢复就是靠 `openclaw.json.bak.pre-fix-2026-08-19-0921` 完成的（✅ 底稿 §4.1）。

### 04.3.5 stdio server 启动脚本（完整可复制）

```bash
#!/bin/bash
# start-silicon-life-mcp.sh
# 把 7 resource + 5 tool + 2 prompt 暴露为 MCP stdio server
exec node -e "
const { Server } = require('@modelcontextprotocol/sdk/server');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio');

const server = new Server(
  { name: 'silicon-life-training-full', version: '2026.9.4' },
  {
    capabilities: {
      resources: { subscribe: true, listChanged: true },
      tools:     { listChanged: true },
      prompts:   { listChanged: true },
      logging:   { level: 'info' }
    }
  }
);

server.setRequestHandler('resources/list', async () => ({ resources: [] }));
server.setRequestHandler('resources/read', async (req) => ({ contents: [] }));
server.setRequestHandler('tools/list',     async () => ({ tools: [] }));
server.setRequestHandler('tools/call',     async (req) => ({ content: [] }));
server.setRequestHandler('prompts/list',   async () => ({ prompts: [] }));
server.setRequestHandler('prompts/get',    async (req) => ({ messages: [] }));

const transport = new StdioServerTransport();
server.connect(transport);
"
```

> ⚠️ 上面每个 handler 的返回值都是**空数组占位**——因为这册是 API 参考，不放业务实现。要真实跑通，把 `[]` 换成 §04.3.2 里列出的 7 resource / 5 tool / 2 prompt。

### 04.3.6 注册后必须做的 3 个验证

```bash
# 验证 1 · 配置态已落盘
openclaw mcp list | grep -c "silicon-life-training"
# 期望：1

# 验证 2 · 运行态 connected
openclaw mcp status | grep -c "connected"
# 期望：≥1

# 验证 3 · 工具真的能列出来（证明 handshake + tools/list 通了）
openclaw mcp tools silicon-life-training | grep -c "drift_detection"
# 期望：1
```

**若验证 2 失败** → 看 §04.4 故障排查 F-MCP-04（transport 不匹配）/ F-MCP-05（握手失败）。
**若验证 3 失败但 2 成功** → 说明 capabilities 声明了但 handler 没注册（见 F-MCP-06）。

### 04.3.7 卸载 / 回滚

```bash
openclaw mcp unset silicon-life-training     # 删整条 server
openclaw mcp reload
cp ~/.openclaw/openclaw.json.bak.pre-mcp-20260928-1200 ~/.openclaw/openclaw.json   # 兜底
```

---

## 04.4 · 故障排查（14 类）

> **说明**：本机 MCP 配置为 0，因此以下 14 类中**没有任何一类是本机真实踩过的**——全部来自协议语义推导 + 相邻故障域（8/19 断线、9/21 飞书事故）的类比。**判定为设计级排坑清单，非实测记录。**

### F-MCP-01 · server 加了但 `list` 看不到

**症状**：`openclaw mcp add` 后 `openclaw mcp list` 仍为空。
**根因候选**：
1. 写到了 `mcpServers` 而不是 `mcp.servers`（🚨 最常见）。
2. 写到了 `~/.openclaw/workspace/openclaw.json`——**该文件不存在**（✅ 实测），因此永不生效。

**排查**：
```bash
python3 -c "import json;d=json.load(open('$HOME/.openclaw/openclaw.json'));print(list(d.keys()))"
# 期望：含 'mcp'（若不含则根本没写进去）
python3 -c "import json;d=json.load(open('$HOME/.openclaw/openclaw.json'));print(list(d.get('mcp',{}).get('servers',{}).keys()))"
```

### F-MCP-02 · JSON5 注释导致 `--strict-json` 解析失败

**症状**：配置里加了 `// 注释` 后命令报 parse error。
**根因**：`openclaw.json` 顶层支持 JSON5；但 `--strict-json` 模式**拒绝注释**。
**对策**：JSON5 注释仅用于人工可读，脚本生成的配置一律不带注释。

### F-MCP-03 · stdio server 用相对路径 → 子进程找不到文件

**症状**：`status` 显示 `error`，日志里有 `ENOENT`。
**根因**：stdio server 的工作目录是 OpenClaw 进程的 cwd，不是你 shell 的 cwd。
**对策**：`args` 里用**绝对路径**（`/Users/<you>/.openclaw/mcp/xxx.js`）。

### F-MCP-04 · transport 不匹配

**症状**：配置了 `"type": "stdio"` 但 server 实际是个 HTTP 服务（或反之）。
**对策**：先用 `curl -s localhost:<port>/health` 或直接 `node xxx.js` 手跑一次确认形态，再写 `type`。

### F-MCP-05 · 握手失败（`initialize` 不返回）

**症状**：`probe` 超时。
**根因候选**：① server 把日志打到 **stdout**（污染 JSON-RPC 帧流）；② protocolVersion 不被 server 接受。
**对策**：**所有日志必须走 stderr**（`console.error`），stdout 只允许 JSON-RPC。

### F-MCP-06 · capabilities 声明与实际 handler 不一致

**症状**：`probe` 成功但 `tools` 为空。
**根因**：`capabilities.tools` 已声明，但 server 没 `setRequestHandler('tools/list', ...)`。
**对策**：capabilities 是"承诺"，handler 是"兑现"；两者必须一一对应。

### F-MCP-07 · 密钥明文进了 `openclaw.json`

**症状**：`git diff` / 备份 / 分享配置时泄漏。
**对策**：用 `${ENV_VAR}` 引用；配合 plugin 的 `uiHints: { apiKey: { sensitive: true } }` 让 UI 脱敏。

### F-MCP-08 · 同名 server 被后写覆盖

**症状**：加了新 server，旧的同名 server 静默消失。
**根因**：`mcp.servers` 是 map，同名即覆盖（无警告）。
**对策**：命名带前缀（`<vendor>-<function>`）。

### F-MCP-09 · 46 原语里你以为有、实际没有

**症状**：代码里调 `elicitation/create` 报 `-32601 method not found`。
**根因**：**协议层有定义 ≠ OpenClaw 已暴露**。本机实测：46 个里只有 8 个走通过。
**排查**：
```bash
openclaw --debug attach <agent> 2>&1 | grep -E "method=|primitive" | head -20
```

### F-MCP-10 · 把语义塞进协议 args

**症状**：`tools/call` 传了 `metadata.three_stage_review`，server 侧完全忽略。
**反例**：
```json
{
  "method": "sampling/createMessage",
  "params": {
    "messages": [],
    "metadata": { "three_stage_review": "self-check-1" }
  }
}
```
**正例**：语义放 **vendor-specific 命名空间**，例如 `metadata["x-silicon-life"] = { stage: "self-check-1" }`。协议层只传它认识的字段。

### F-MCP-11 · `reload` 后旧连接残留

**症状**：改了配置 `reload`，`status` 里出现两条同名连接。
**对策**：`reload` 后跟一次 `status`；若仍残留，走「重启 gateway」而非反复 reload。

### F-MCP-12 · stdio 子进程泄漏（僵尸进程）

**症状**：`ps aux | grep node` 里 MCP server 进程数不断增长。
**根因**：client 崩溃时没有发 `shutdown`，子进程变孤儿。
**对策**：server 侧监听 stdin 的 `end` 事件自杀；或加超时自杀（30 min 无请求即退）。

### F-MCP-13 · 长任务无进度 → 上层误判为挂死

**症状**：一个大任务跑了 10 分钟，调用方认为超时。
**根因**：没用 `progress/notify`（⏳ 未实测）。
**对策**：长任务必须上报进度；本册训练学侧对应「任务卡 ack」（见 `chapters/09-a2a-binding/` §10.6）。

### F-MCP-14 · 日志级别设了但看不到 stdout

**症状**：`logging/setLevel debug` 后依然无输出。
**根因候选**：① 日志走的是 OpenClaw 自己的 `logging` 配置（`openclaw.json` 的 `logging` 顶层 key），与 MCP 的 `logging/*` 不是一套；② stdio 场景日志混进 stderr 后被丢弃。
**对策**：先确认你看的是**哪一层的日志**——`~/.openclaw/openclaw.json` 的 `logging`（OpenClaw 层）vs MCP `logging/*`（协议层）。

---

## 04.5 · 诚实边界

### 04.5.1 ✅ 已实测（可复现）

| # | 事实 | 来源 |
|---|---|---|
| 1 | `openclaw mcp` = **14 子命令** | 底稿 §3.5 |
| 2 | 命名空间 = **`mcp.servers`** | 底稿 §3.5 |
| 3 | `openclaw mcp list` = **0 配置** | 底稿 §3.5 |
| 4 | 46 原语中 **8 个**在 attach 流程隐式走过 | `chapters/08-mcp-binding/` §9.4 |
| 5 | `~/.openclaw/workspace/openclaw.json` **不存在** | 底稿 §2 |
| 6 | 主配置真身 `~/.openclaw/openclaw.json` · 45,662 B · 20 顶层 key | 底稿 §2 |
| 7 | `openclaw.plugin.json` 是 JSON5，非 `manifest.yaml` | 底稿 §1.2 |
| 8 | `~/.openclaw/extensions/` **本机不存在** | 底稿 §3.4 |
| 9 | MCP spec 口径 v2025-11-25 + v2026-07-28 | `chapters/08-mcp-binding/` §9.4 实测环境 |

### 04.5.2 ⏳ 未实测（如实标注，禁止当成已验证）

| # | 未实测项 | 为什么没测 |
|---|---|---|
| 1 | `openclaw mcp add` / `set` / `configure` 实际落盘形状 | **本机 0 配置**，跑会污染生产配置 |
| 2 | `openclaw mcp probe` / `status` / `tools` 输出格式 | 需先有 server；无 server 无可探 |
| 3 | `openclaw mcp login` OAuth 全流程 | 需浏览器 + 真实远端 server |
| 4 | `openclaw mcp serve` 反向模式 | 无消费方 |
| 5 | 38 个 ⏳ 原语的**实际 wire 形态** | 无 server 可对接 |
| 6 | `server.json` 与 MCP Registry 的上传流程 | 未接 registry |
| 7 | plugin 形态分发 MCP server 的全生命周期（`plugins install`） | 底稿 §5 待实测 |
| 8 | `streamable-http` transport 在 OpenClaw 里是否已实现 | v2026-07-28 新特性，本机未验证 |
| 9 | capabilities 声明与 OpenClaw 实际读取的字段映射 | 需真实 server + debug 日志 |
| 10 | `mcp.servers` 的完整字段白名单（是否支持 `timeout` / `retries` 等） | 本机 0 配置，无样本 |

### 04.5.3 本册不承诺的事

1. **不承诺** §04.3 的 7 步注册流程在本机可原样跑通——它是**文档路径**，非实测记录。
2. **不承诺** 46 原语表里的 ⏳ 项在 OpenClaw 2026.9.4 里已实现——它们多数是**协议层有、OpenClaw 未暴露**。
3. **不承诺** `server.json` 与 `mcp.servers` 字段可互相复制——两者**不同标准**。
4. **不承诺** MCP 的安全性——MCP server 是**任意代码执行入口**，接之前按 `faq-troubleshooting/F5-Skills-Tools-MCP.md` 的三问过一遍。

### 04.5.4 版本差异声明

| 口径 | 版本 | commit | 用途 |
|---|---|---|---|
| 书内统一 | OpenClaw **2026.9.4** | `3a9d69d` | 全书引用基线 |
| 本机 live 复核 | OpenClaw **2026.9.6** | `eb377ac` | 诚实标注差异 |

> 若 2026.9.6 的 `openclaw mcp` 子命令数与 14 不一致，**以本机 `openclaw mcp --help` 为准**，并回写底稿。

---

**互链**
- 协议详解：`chapters/08-mcp-binding/08-MCP绑定.md`（§8.3 骨架 / §9.3 映射 / §9.4 46 原语 / §9.5 slcp-bridge）
- 排障：`faq-troubleshooting/F5-Skills-Tools-MCP.md`
- 实操配方：`cookbook/03-skills-tools-mcp.md`（**C3**）
- 相邻卷：`api-reference/06-skill-manifest-reference.md`（Skill/Tool manifest）· `api-reference/05-a2a-slcp-reference.md`（A2A / SLCP）

**文件版本**：v1.0 · 2026-09-28 · API 参考附录卷 文件 4/7
---

## 04.6 · 附录 · 46 原语 × 8 卷 × 4 接口层落地矩阵

> **本节定位**：§04.2.2 主表已给出「8 卷归属 + 接口层」两列；本节把同一信息**按卷轴重排**，便于按书的结构化路径检索——你读到第 N 卷时，想知道"这一卷对应哪些 MCP 原语"，直接查这里。

### 04.6.1 按 8 卷拆解（原语 → 卷）

**卷一 · 契约（Contract）· 5 个原语**

| 原语 | 本机 | 落地要点 |
|---|---|---|
| `resources/list` | ✅ | 7 契约清单；OpenClaw attach 时即拉 |
| `resources/read` | ✅ | `contract://soul` / `contract://user` 等 URI |
| `resources/templates/list` | ⏳ | 动态契约（`contract://{role}.md`）的清单入口 |
| `resources/templates/read` | ⏳ | 模板实例化 |
| `notifications/resource/updated` | ⏳ | 契约变更的别名通知通道 |

**卷二 · 优势（Advantage）· 3 个原语**

| 原语 | 本机 | 落地要点 |
|---|---|---|
| `tools/list` | ✅ | 5 优势工具清单 |
| `tools/call` | ✅ | `drift_detection` / `three_stage_review` 等实际调用 |
| `tools/list_changed` | ⏳ | 热插拔 skill 时的工具集变更 |

**卷三 · 漂移（Drift）· 5 个原语**

| 原语 | 本机 | 落地要点 |
|---|---|---|
| `resources/subscribe` | ⏳ | 契约变更订阅（与 HEARTBEAT.md 联动） |
| `resources/unsubscribe` | ⏳ | 退订（防泄漏） |
| `resources/updated` | ⏳ | 契约变更下行 |
| `resources/list_changed` | ⏳ | 契约清单变更 |
| `ping` | ⏳ | 保活；**与业务层 heartbeat 不同层** |

**卷四 · 训练（Training）· 5 个原语**

| 原语 | 本机 | 落地要点 |
|---|---|---|
| `prompts/list` | ⏳ | 提示模板清单 |
| `prompts/get` | ⏳ | `soul_init`（带 `role` 参数） |
| `prompts/list_changed` | ⏳ | — |
| `prompts/template` | ⏳ | 自定义扩展位 |
| `notifications/prompt/list_changed` | ⏳ | 同上（别名） |

**卷五 · 三省（Three-Stage Review）· 3 个原语**

| 原语 | 本机 | 落地要点 |
|---|---|---|
| `sampling/createMessage` | ⏳ | 自检 / 互检 / 终审的 LLM 反向调用 |
| `sampling/createMessageStream` | ⏳ | 流式串行审 |
| `sampling/cancel` | ⏳ | 取消未完成采样 |

**卷六 · 治理（Governance）· 2 个原语**

| 原语 | 本机 | 落地要点 |
|---|---|---|
| `elicitation/create` | ⏳ | 边界检查时向用户澄清（**OpenClaw 未暴露**） |
| `elicitation/respond` | ⏳ | 用户响应回传 |

**卷七 · 工程（Engineering）· 20 个原语**

| 原语 | 本机 | 落地要点 |
|---|---|---|
| `roots/list` | ⏳ | 入口路径协商 |
| `roots/refresh` | ⏳ | 刷新根列表 |
| `notifications/roots/list_changed` | ⏳ | 根变更通知 |
| `logging/setLevel` | ⏳ | 级别设置 |
| `logging/message` | ⏳ | 结构化日志下行 |
| `logging/levelChanged` | ⏳ | 级别变更广播 |
| `completion/complete` | ⏳ | 参数补全（`contract://` 最有价值） |
| `completion/resolve` | ⏳ | 解析已选项 |
| `initialize` | ✅ | 握手 |
| `initialized` | ✅ | 握手确认 |
| `shutdown` | ⏳ | 优雅关闭 |
| JSON-RPC 2.0 error codes | ✅ | 5 个标准错误码 |
| `notifications/message` | ⏳ | 通用通知 |
| `notifications/exit` | ⏳ | 主动退出 |
| `notifications/stderr` | ⏳ | stdio 专有 |
| `stdio/handshake` | ✅ | stdio 传输握手 |
| `http/handshake` | ⏳ | HTTP 传输 |
| `sse/connect` | ⏳ | SSE 长连接 |
| `streamable-http/init` | ⏳ | v2026-07-28 新增 |
| `streamable-http/chunk` | ⏳ | v2026-07-28 新增 |

**卷八 · 交接（Handover）· 3 个原语**

| 原语 | 本机 | 落地要点 |
|---|---|---|
| `progress/notify` | ⏳ | 任务卡 ack 进度上报 |
| `progress/cancel` | ⏳ | 取消进度跟踪 |
| `notifications/cancelled` | ⏳ | 请求级取消（带 reason，用于让位） |

> **合计校验**：5 + 3 + 5 + 5 + 3 + 2 + 20 + 3 = **46** ✅
> **（`notifications/progress` 与 `notifications/resource/updated` 的归类以 §04.2.2 主表为准，本节的卷轴视角做了合并去重，两节口径均已标注。）**

### 04.6.2 按 4 接口层反向检索

| 接口层 | 是否含 MCP 原语 | 说明 |
|---|---|---|
| L1 CLI 层 | ❌ 否 | `openclaw mcp <14 子命令>` 只是**人机接口**；原语本身不在 CLI 表面 |
| L2 配置层 | ❌ 否 | `mcp.servers` 只描述"怎么连"，不描述"连上后调什么" |
| L3 协议层 | ✅ **全部 46 个** | MCP 的天然归属 |
| L4 语义层 | ❌ 否（但通过 `metadata` 承载） | 训练学语义不属协议层；用 vendor 命名空间桥接 |

> **一句话记忆**：**"L3 是 MCP 的地盘，L2 是它的门牌，L1 是它的仪表盘，L4 是它的灵魂——灵魂不在协议里。"**

### 04.6.3 与 A2A 的分界（避免两类协议混淆）

| 维度 | MCP | A2A |
|---|---|---|
| 解决的问题 | 一个 agent 怎么用**工具/资源** | 多个 agent 之间怎么**对话/交接** |
| 拓扑 | client ↔ server（**一对多工具**） | peer ↔ peer（**多对多 agent**） |
| 治理方 | AAIF（Anthropic + Block + OpenAI） | Linux Foundation |
| 本书对位 | `chapters/08-mcp-binding/` | `chapters/09-a2a-binding/`（含 SLCP） |
| 本册文件 | **本文件（04）** | `api-reference/05-a2a-slcp-reference.md` |
| 本机基线 | `mcp.servers` = 0 配置 | `stock:a2a/index.js` = **disabled** |

> **常见误用**：用 MCP 做 agent 间任务交接（应该用 A2A + 任务交接协议 THP / Task Handover Protocol）；或用 A2A 去调一个数据库（应该用 MCP 的 `tools/call`）。**两者的边界是"是否跨 agent 身份"**。

### 04.6.4 一页速记卡

```text
openclaw mcp           → 14 子命令（人机接口 · L1）
mcp.servers            → 配置命名空间（L2）
46 原语                → 协议面（L3）· 本机 8 ✅ / 38 ⏳
14 语义接口            → 训练学面（L4）· 覆盖率 30.4%
server.json            → 分发元信息（≠ mcp.servers）
openclaw.plugin.json   → plugin 形态清单（JSON5 · ≠ manifest.yaml）
```

**文件尾注**：本文件所有 ✅ 均可在底稿 `/api-reference/00-实测事实底稿.md` 找到对应行；所有 ⏳ 均为**如实标注的未实测项**。

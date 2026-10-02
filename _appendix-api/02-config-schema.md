# API 参考 · 02 · 配置 Schema（`~/.openclaw/openclaw.json`）

> **手册版本**：v5.0 行业标准版 · 2026-09-27
> **License**：MIT（跟随 OpenClaw 主仓）
> **实测环境**：OpenClaw 2026.9.4 (3a9d69d) · Hermes Agent 0.20.1 · macOS 26.5.1 · 236 skills
> **本机 live 复核**：OpenClaw 2026.9.6 (eb377ac) · 18 agents · 61 automations · plugins 53/73（书内统一用 2026.9.4 口径）
> **本卷定位**：API 参考附录卷 · 文件 2 / 7 · 对位 `chapters/03-skeleton/03-系统骨架.md`
> **互链**：`03-protocol-reference.md` · `faq-troubleshooting/F1-环境与安装.md` · `sop-library/02-protocol-config-sop.md` · `cookbook/01-protocol-SOUL.md`
> **诚实底线**：顶层 20 key / 5 个幽灵字段 / Compaction 真名 全部 ✅ 实测；**各 key 的子键名与取值 ⏳ 待实测**（详见 §6）

---

## 本节速览

| 项 | 值 |
|---|---|
| **文档定位** | 《API 参考附录卷》第 2 分册 · 配置层权威 schema |
| **覆盖对象** | `~/.openclaw/openclaw.json`（**唯一真身路径**） |
| **实测文件大小** | 45,662 字节（早期实测 45,445 字节，两者均曾观测到） |
| **顶层 key 数** | **20**（✅ `jq keys` 实测） |
| **底稿来源** | `api-reference/00-实测事实底稿.md` §2 |
| **禁止事项** | 本节所有事实来自底稿，**未重跑 `openclaw --help`**；底稿未覆盖者一律标 ⏳ |
| **术语口径** | 《00-术语对照表·v3.0行业标准版.md》35 条改名表 |

**术语双写约定（首次出现即双写）**：本文所有行业标准术语按「行业标准名（原：黑话 / English alias）」书写。
例：智能体集群（原：军团 / Agent Fleet）、多智能体编排（原：军团编制 / Multi-Agent Orchestration）、
Supervisor Layer（原：监军 / Supervisor Layer）、SLCP（原：ACP / Silicon Life Collaboration Protocol）。

---

## 1. 🚨 配置路径警示（读错路径 = 全篇作废）

### 1.1 唯一真身路径

```
~/.openclaw/openclaw.json          ← ✅ 真身（主配置）
```

**已实测确认**：

```bash
# ✅ 真身存在性验证
ls -l ~/.openclaw/openclaw.json
# 期望：45,662 字节（早期观测 45,445 字节）

# ✅ 真身顶层 key 数验证
jq 'keys | length' ~/.openclaw/openclaw.json
# 期望：20

# ✅ 真身顶层 key 全量列举
jq -r 'keys[]' ~/.openclaw/openclaw.json
# 期望（20 行）：
# acp
# agents
# auth
# bindings
# browser
# channels
# commands
# env
# gateway
# logging
# memory
# messages
# meta
# models
# plugins
# session
# skills
# talk
# tools
# wizard
```

### 1.2 ❌ 被广泛误称的路径

```
~/.openclaw/workspace/openclaw.json   ← ❌ 不存在
```

**已实测确认（`ls` 直接否定）**：

```bash
ls ~/.openclaw/workspace/openclaw.json
# 期望：No such file or directory
# 结论：该路径**从未存在**，是早期资料（v1.0 时代）的误植
```

> **真名 vs 虚构对照**（引用底稿 §1.2 命令真名对照表）：

| ❌ 虚构（错误写法） | ✅ 真名（正确写法） | 后果 |
|---|---|---|
| `~/.openclaw/workspace/openclaw.json` | `~/.openclaw/openclaw.json` | 改错文件 → 配置**静默不生效**，无任何报错 |

### 1.3 为什么这个错误如此危险

这是**全书危害等级最高**的一个路径误植，原因有三：

**其一，它不会报错。** 你写了一个 JSON、格式合法、保存成功、`cat` 出来看着完全正常。
OpenClaw 启动时不读这个文件，也不告诉你「有个孤儿配置躺在 workspace 里」。
你改了一整晚的 `requireMention`，明天群里 @ 一次都没生效，却找不到任何日志线索。

**其二，它天然自洽。** `~/.openclaw/workspace/` 是 OpenClaw 工作区根目录，
脑内类比一下——「配置当然放在工作区里」——逻辑上毫无违和感。
实际上 OpenClaw 把**配置层**（`~/.openclaw/`）与**工作区层**（`~/.openclaw/workspace/`）
做了硬分层：前者是进程启动时读取的宿主级配置，后者是 agent 运行时读写的素材/协议/技能目录。

**其三，它被 9/21 飞书事故放大过。** 那次事故根因是
`requireMention: true` + `groupAllowFrom` 仅丘总 → 6 个账号 disconnected，静默超过 60 分钟。
事故复盘时不止一人第一反应是「去 workspace 下看看配置」——**方向错误会白烧 20 分钟**。

### 1.4 两层目录的职责切分（必须记牢）

```
~/.openclaw/
├── openclaw.json              ← 【配置层】进程启动时读取 · 唯一真身
├── workspace/                 ← 【工作区层】agent 运行时读写
│   ├── agents/
│   │   ├── <agent-id>/        ← 每个 agent 的工作目录
│   │   │   ├── SOUL.md            （协议文件 · 见本卷 03）
│   │   │   ├── AGENTS.md
│   │   │   ├── USER.md
│   │   │   ├── TOOLS.md
│   │   │   ├── HEARTBEAT.md
│   │   │   ├── IDENTITY.md
│   │   │   └── MEMORY.md
│   │   └── roles/<agent>/AGENTS.md
│   ├── skills/                ← 236 个 skill 目录（本书实测基线）
│   ├── SHARED/                ← 协议模板目录（⏳ 本机路径待实测，见 §7）
│   └── references/            ← 参考文档（含本书全部卷册）
├── extensions/                ← ⏳ 本机不存在（未装自定义 plugin）
└── logs/                      ← 日志（⏳ 具体文件名待实测）
```

**一句话记忆法**：

> **改配置 → 去 `~/.openclaw/openclaw.json`；改人格 → 去 `~/.openclaw/workspace/agents/<id>/*.md`。**

### 1.5 三步自检（改配置前后各跑一次）

```bash
# 步骤 1 · 确认你要改的是真身
test -f ~/.openclaw/openclaw.json && echo "✅ 真身在" || echo "❌ 真身丢了"

# 步骤 2 · 确认误称路径确实没有（防止你把孤儿文件当命根子）
test -f ~/.openclaw/workspace/openclaw.json \
  && echo "⚠️ 存在孤儿配置，请核对是否为误建" \
  || echo "✅ 无孤儿配置"

# 步骤 3 · 改前先备份（命名带时间戳 + 用途）
cp ~/.openclaw/openclaw.json \
   ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d-%H%M%S)
# 参考本机真实备份命名（8/19 断线修复时留下）：
#   openclaw.json.bak.pre-fix-2026-08-19-0921
```

### 1.6 本机真实备份先例（可直接照抄命名风格）

```
openclaw.json.bak.pre-fix-2026-08-19-0921
      ↑            ↑        ↑
   文件名       用途标记   日期-时间
```

- **用途标记**：`pre-fix` = 修复前；建议同时建立 `post-fix` 对照。
- **日期时间**：`YYYY-MM-DD-HHMM`，精确到分钟（配置改动通常以分钟为单位密集发生）。
- **事故出处**：`~/.openclaw/workspace/agents/workspace-kunlun/memory/2026-08-19-军团断线修复.md`
  ——根因是 MiniMax-M3 空 body → 17-18 fallback 首位被占 → 轩辕 `primary == fallback[0]` 自循环。

### 1.7 互链

- 想改 **agent 人格/纪律** → 本卷 `03-protocol-reference.md`
- 想改 **心跳频率** → 本卷 `03-protocol-reference.md` §7（`agents.entries.<id>.heartbeat.every`）
- 想改 **渠道 @ 规则** → 本卷 `04-*.md` + `faq-troubleshooting/F3-心跳与定时.md`
- 配置改完不生效 → `faq-troubleshooting/F1-环境与安装.md` · `F-Top20-高频速查.md`
- 想看保姆级步骤 → `sop-library/02-protocol-config-sop.md`
- 想抄可跑配方 → `cookbook/01-protocol-SOUL.md`

---

## 2. 真实 20 顶层 key 完整 Schema

> **本节数据来源**：底稿 §2.1「真实 20 个顶层 key」表 —— **直接引用，未实跑**。
> **类型标注**：`dict` = JSON object；`list` = JSON array。
> **子项数**：该 key 的直接子键/元素个数（实测快照值，**非固定契约**，随业务增长）。

### 2.0 20 key 总览表

| # | key | 类型 | 子项数 | 说明 |
|---:|---|---|---:|---|
| 1 | `acp` | dict | 5 | ACP（Zed）桥接配置 |
| 2 | `agents` | dict | 3 | 含 `entries`（18 agent） |
| 3 | `auth` | dict | 1 | 认证 |
| 4 | `bindings` | list | 37 | 渠道绑定（Telegram 19 + 飞书 18） |
| 5 | `browser` | dict | 3 | 浏览器 |
| 6 | `channels` | dict | 2 | 含 `feishu`（18 账号）等 |
| 7 | `commands` | dict | 6 | 命令配置 |
| 8 | `env` | dict | 1 | 环境变量 |
| 9 | `gateway` | dict | 7 | 网关 |
| 10 | `logging` | dict | 1 | 日志 |
| 11 | `memory` | dict | 1 | 记忆 |
| 12 | `messages` | dict | 1 | 消息 |
| 13 | `meta` | dict | 2 | 元信息 |
| 14 | `models` | dict | 2 | 模型 |
| 15 | `plugins` | dict | 1 | 插件 |
| 16 | `session` | dict | 1 | 会话（实测仅含 `dmScope: per-channel-peer`） |
| 17 | `skills` | dict | 1 | 技能 |
| 18 | `talk` | dict | 1 | 语音/对话 |
| 19 | `tools` | dict | 3 | 工具 |
| 20 | `wizard` | dict | 4 | 向导 |

> **⚠️ 子项数免责声明**：上表子项数来自本机实测快照。OpenClaw 的顶层 key 集合相对稳定
> （20 个），但**子项数量会随部署演进**（例如 `bindings` 从早期 37 条起变化、
> `plugins` 从 51/69 → 53/73）。**以 `jq` 实测为准，不要背数字。**

### 2.1 key #1 · `acp`（dict · 5 子项）

**定位**：ACP（Zed）桥接配置。ACP = Agent Client Protocol，OpenClaw 通过它把 agent
暴露给 Zed 编辑器。

```bash
# 查看 acp 段
jq '.acp' ~/.openclaw/openclaw.json

# 查看 acp 直接子键
jq -r '.acp | keys[]' ~/.openclaw/openclaw.json
```

**Schema 骨架（结构真名，值因部署而异）**：

```json
{
  "acp": {
    "<子键1>": "<值>",
    "<子键2>": "<值>",
    "<子键3>": "<值>",
    "<子键4>": "<值>",
    "<子键5>": "<值>"
  }
}
```

> **⚠️ 诚实边界**：`acp` 的 **5 个子键具体名称底稿未逐条列出** → ⏳ 待实测。
> 已知的**结构事实**（✅）：`acp` 存在、类型为 dict、直接子项 5 个。

**相关命令**：

```bash
openclaw acp          # Zed ACP bridge（✅ 实测存在）
```

**术语注意**：ACP 在本书内部与 v1.0 术语「ACP」三重撞名 → v3.0 改名表已把内部术语
改为 **SLCP**（Silicon Life Collaboration Protocol）。**引用 OpenClaw 官方命令时保留 `acp` 原样**，
引用本书内部协作协议时写 SLCP。二者**不是一个东西**。

### 2.2 key #2 · `agents`（dict · 3 子项 · 核心中的核心）

**定位**：多智能体编排（原：军团编制 / Multi-Agent Orchestration）的**唯一配置入口**。

```bash
# agents 段直接子键
jq -r '.agents | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：3

# agent 总数
jq '.agents.entries | length' ~/.openclaw/openclaw.json
# 期望：18

# 全部 agent id
jq -r '.agents.entries | keys[]' ~/.openclaw/openclaw.json

# 每个 agent 的主模型
jq -r '.agents.entries | to_entries[] | "\(.key)\t\(.value.model // "n/a")"' \
   ~/.openclaw/openclaw.json
```

**真实主模型分布（✅ 底稿 §3.1）**：

| 主模型 | agent 数 |
|---|---:|
| `opus-4-8` | 9 |
| `gpt-5.6-sol` | 4 |
| `gpt-5.5` | 2 |
| `gpt-5.6-terra` | 2 |
| `deepseek-v4-flash` | 1 |
| **合计** | **18** |

**`agents` 下的真实子层级路径（🚨 最重要的知识）**：

```
agents.entries                          ← 18 个 agent 的字典
agents.entries.<id>                     ← 单个 agent 配置对象
agents.entries.<id>.heartbeat.every     ← ✅ 心跳频率真实路径
agents.entries.<id>.groupChat.mentionPatterns  ← ✅ 提及模式真实路径
agents.entries.<id>.model               ← 主模型
```

**示例 JSON（骨架 · 真实路径）**：

```json
{
  "agents": {
    "entries": {
      "tiance": {
        "model": "<模型标识>",
        "heartbeat": {
          "every": "30m"
        },
        "groupChat": {
          "mentionPatterns": ["<pattern1>", "<pattern2>"]
        }
      },
      "kunlun": {
        "model": "<模型标识>",
        "heartbeat": {
          "every": "30m"
        }
      }
    },
    "<其它子键2>": {},
    "<其它子键3>": {}
  }
}
```

> **⚠️ 诚实边界**：`agents` 除 `entries` 外的**另 2 个子键名称**底稿未列出 → ⏳ 待实测。
> `heartbeat.every` 与 `groupChat.mentionPatterns` 的**路径**是 ✅ 实测真名，
> 但**本机具体取值**底稿未给出 → ⏳。

**相关命令（全部 ✅ 实测存在）**：

```bash
openclaw agents list                                  # 列出全部 agent
openclaw agents add <id> --workspace <dir>            # 新增（不是 create！）
openclaw agents bind <...>                            # 绑定渠道
openclaw agents bindings                              # 查看全部 binding
openclaw agents delete <id>                           # 删除
```

**`openclaw agents` 的真实子命令集合（✅ 底稿 §1.3）**：

```
add · bind · bindings · delete · list
（无 health-check / create / archive）
```

> **真名 vs 虚构对照**：

| ❌ 虚构 | ✅ 真名 |
|---|---|
| `openclaw agents create X` | `openclaw agents add X --workspace <dir>` |
| `openclaw agents health-check` | `openclaw health` / `openclaw doctor` |
| `openclaw agents archive` | `openclaw backup create` |

**生产实况对照**：本机 18 agent（`agents.entries` 18 键）
↔ `openclaw agents list` 输出一致 ↔ `openclaw agents bindings` 37 条 binding。

### 2.3 key #3 · `auth`（dict · 1 子项）

**定位**：认证层。

```bash
jq '.auth' ~/.openclaw/openclaw.json
jq -r '.auth | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：1
```

**⚠️ 安全红线**：`auth` 段包含凭据类信息。

- ❌ **绝不要**把 `jq '.auth'` 的完整输出贴进 issue / 聊天 / 文档
- ✅ 需要核对时只输出**键名**，值用 `| keys` 或 `| to_entries | map(.key)` 遮蔽
- ✅ 分享配置前统一跑：`jq 'del(.auth) | del(.channels.feishu[].appSecret)' `

```bash
# 安全核验：只看结构，不看值
jq '.auth | walk(if type == "object" then with_entries(.value = "<redacted>") else . end)' \
   ~/.openclaw/openclaw.json
```

> **⚠️ 诚实边界**：`auth` 唯一子键名 → ⏳ 待实测。

**相关命令**：`openclaw pairing`（Secure DM pairing，✅ 实测存在）。

### 2.4 key #4 · `bindings`（list · 37 元素）

**定位**：渠道绑定表——把 agent 挂到具体渠道身份上。

**✅ 实测构成（底稿 §3.2）**：

| 渠道 | binding 数 |
|---|---:|
| Telegram | 19 |
| 飞书（Feishu/Lark） | 18 |
| **合计** | **37** |

```bash
# binding 总数
jq '.bindings | length' ~/.openclaw/openclaw.json
# 期望：37

# 按渠道分组统计（结构探测）
jq -r '.bindings[] | .channel // .type // "unknown"' ~/.openclaw/openclaw.json \
  | sort | uniq -c

# 用官方命令看（等价视图）
openclaw agents bindings
```

**Schema 形态**：`bindings` 是 **list**（JSON 数组），**不是 dict**。
这是最容易记错的类型——记住口诀：

> **`agents` 是字典（按 id 查），`bindings` 是列表（一条条挂）。**

**示例 JSON（元素骨架）**：

```json
{
  "bindings": [
    {
      "agent": "<agent-id>",
      "channel": "telegram",
      "<字段3>": "<值>"
    },
    {
      "agent": "<agent-id>",
      "channel": "feishu",
      "<字段3>": "<值>"
    }
  ]
}
```

> **⚠️ 诚实边界**：binding 元素的**完整字段集**底稿未逐条列出 → ⏳ 待实测。
> 元素中含有渠道标识（可从 19/18 分组推断 ✅），但字段真名以 `jq '.bindings[0] | keys'` 为准。

**生产实况对照**：37 = Telegram 19 + 飞书 18。飞书侧 18 个账号与
`channels.feishu` 的 18 账号**一一对应**。

### 2.5 key #5 · `browser`（dict · 3 子项）

**定位**：浏览器（Web 自动化 / 浏览器工具）配置。

```bash
jq '.browser' ~/.openclaw/openclaw.json
jq -r '.browser | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：3
```

**Schema 骨架**：

```json
{
  "browser": {
    "<子键1>": "<值>",
    "<子键2>": "<值>",
    "<子键3>": "<值>"
  }
}
```

> **⚠️ 诚实边界**：3 个子键名 → ⏳ 待实测。

**互链**：浏览器自动化的实战排坑见 `faq-troubleshooting/F5-Skills-Tools-MCP.md`。

### 2.6 key #6 · `channels`（dict · 2 子项 · 事故高发区）

**定位**：渠道层。**核心子项：`feishu`（18 账号）**。

```bash
jq -r '.channels | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：2（含 feishu）

# 飞书账号数
jq '.channels.feishu | length' ~/.openclaw/openclaw.json
# 期望：18

# 🚨 事故相关的两个真名路径
jq '.channels.feishu.requireMention' ~/.openclaw/openclaw.json
jq '.channels.feishu.groupAllowFrom' ~/.openclaw/openclaw.json
```

**两条 ✅ 实测真名路径（9/21 飞书事故直接相关）**：

| 路径 | 语义 | 事故教训 |
|---|---|---|
| `channels.feishu.requireMention` | 飞书群内是否必须 @ 才响应 | `true` + 白名单过窄 → 静默断线 |
| `channels.feishu.groupAllowFrom` | 群白名单（允许哪些群） | 仅含丘总 → 6 账号 disconnected |

**事故复盘（✅ 底稿 §4.2）**：

```
根因：requireMention: true  +  groupAllowFrom 仅丘总
结果：6 账号 disconnected，静默 > 60 分钟
上游修复：PR #152777 · OPEN（feishu groupPolicy）
```

**示例 JSON（骨架）**：

```json
{
  "channels": {
    "feishu": {
      "requireMention": true,
      "groupAllowFrom": ["<允许的来源标识>"],
      "accounts": {
        "<account-1>": {},
        "<account-2>": {}
      }
    },
    "<其它子键>": {}
  }
}
```

> **⚠️ 诚实边界**：`channels.feishu` 的**完整子键集**底稿只给了
> `requireMention` / `groupAllowFrom` 两个真名 → 其余 ⏳ 待实测。
> 飞书 13 个账号的完整 `appId` 仅 5 个实测完整 → **⏳ 待实测**（底稿 §5 明确列出）。

**相关命令**：`openclaw pairing`、`openclaw channels`（⏳ 未在底稿确认命令族，慎用）。

**互链**：`faq-troubleshooting/F2-协议-SOUL-AGENTS-USER.md`、`case-library/01-real-incidents.md`。

### 2.7 key #7 · `commands`（dict · 6 子项）

**定位**：命令配置（斜杠命令 / 快捷命令的行为）。

```bash
jq '.commands' ~/.openclaw/openclaw.json
jq -r '.commands | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：6
```

> **⚠️ 诚实边界**：6 个子键名 → ⏳ 待实测。

### 2.8 key #8 · `env`（dict · 1 子项）

**定位**：环境变量注入。

```bash
jq '.env' ~/.openclaw/openclaw.json
jq -r '.env | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：1
```

**⚠️ 安全红线**：`env` 段**极可能包含 API Key**。
与 `auth` 同规则处理：**只读键名，不读值，不外贴**。

```bash
# 安全核验
jq -r '.env | keys[]' ~/.openclaw/openclaw.json          # ✅ 安全
jq '.env' ~/.openclaw/openclaw.json                       # ❌ 可能泄密
```

### 2.9 key #9 · `gateway`（dict · 7 子项）

**定位**：网关。本机网关为 **Hermes Agent 0.20.1**（✅ 底稿 header）。

```bash
jq '.gateway' ~/.openclaw/openclaw.json
jq -r '.gateway | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：7
```

**⚠️ 已知重大坑（✅ 底稿 §5）**：

> `openclaw health` 完整输出**被 Gateway state 库独占锁遮挡** → ⏳ 待实测。

也就是说：**Gateway 状态库有独占锁**，当它持锁时 `health` 无法给出完整输出。
这不是配置错误，是并发访问现象。遇到时**不要反复重启**，先确认锁的持有者。

**相关命令（✅ 实测存在）**：

```bash
openclaw health        # 健康检查
openclaw doctor        # 诊断
openclaw gateway ...   # ⏳ 子命令集未在底稿确认
```

**互链**：`faq-troubleshooting/F7-治理漂移体检.md`、`sop-library/05-drift-governance-sop.md`。

### 2.10 key #10 · `logging`（dict · 1 子项）

```bash
jq '.logging' ~/.openclaw/openclaw.json
jq -r '.logging | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：1
```

> **⚠️ 诚实边界**：唯一子键名 + 日志落盘路径 → ⏳ 待实测。
> 排障时若需要日志，先 `jq '.logging'` 读出真实路径，**不要猜 `~/.openclaw/logs/`**。

### 2.11 key #11 · `memory`（dict · 1 子项）

**定位**：记忆层配置。

```bash
jq '.memory' ~/.openclaw/openclaw.json
jq -r '.memory | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：1
```

**⚠️ 重要概念澄清**：

> OpenClaw 真正的 MEMORY 是**文件模板**（`MEMORY.md`），
> **不是** MemGPT 的 core / archival / recall / archive 那 4 类。
> 不要给 MEMORY 协议写「4 类 memory」——那是 MemGPT 的模型，不是 OpenClaw 的。

**互链**：`03-protocol-reference.md` §7（MEMORY.md 规范）· `cookbook/02-protocol-HEARTBEAT-MEMORY.md`。

### 2.12 key #12 · `messages`（dict · 1 子项）

```bash
jq '.messages' ~/.openclaw/openclaw.json
jq -r '.messages | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：1
```

> **⚠️ 诚实边界**：唯一子键名 → ⏳ 待实测。

### 2.13 key #13 · `meta`（dict · 2 子项）

**定位**：配置文件的元信息（版本、生成时间之类）。

```bash
jq '.meta' ~/.openclaw/openclaw.json
jq -r '.meta | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：2
```

> **⚠️ 诚实边界**：2 个子键名 → ⏳ 待实测。

### 2.14 key #14 · `models`（dict · 2 子项 · 8/19 事故相关）

**定位**：模型层。**这是 8/19 军团断线事故的配置现场**。

```bash
jq '.models' ~/.openclaw/openclaw.json
jq -r '.models | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：2

# 检查 primary / fallback 自循环（8/19 事故模式）
jq -r '.agents.entries | to_entries[] |
  select(.value.model == .value.fallback[0]) |
  "🚨 自循环: \(.key)"' ~/.openclaw/openclaw.json
```

**8/19 事故根因链（✅ 底稿 §4.1）**：

```
MiniMax-M3 空 body
   → 17-18 fallback 首位被占
      → 轩辕 primary == fallback[0]  ← 🚨 自循环
         → 军团断线
```

**自循环检测口诀**：

> **`primary` 绝不能等于 `fallback[0]`。**
> 如果主模型失败后第一个降级目标又是它自己，就是死循环，不是降级。

**相关命令（✅ 实测存在）**：

```bash
openclaw promos    # Discover and claim promotional model offers from ClawHub
```

> **⚠️ 诚实边界**：`models` 的 2 个子键名 → ⏳ 待实测。

### 2.15 key #15 · `plugins`（dict · 1 子项）

```bash
jq '.plugins' ~/.openclaw/openclaw.json
jq -r '.plugins | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：1
```

**✅ 生产实况（底稿 §3.4）**：

| 项 | 值 |
|---|---|
| 启用/总数（早期） | **51/69 enabled** |
| 启用/总数（本机 live） | **53/73 enabled** |
| `openclaw plugins --help` 子命令数 | **15** |
| `~/.openclaw/extensions/` | **本机不存在**（未装自定义 plugin） |
| `a2a` 插件 | **disabled**（`stock:a2a/index.js`） |

```bash
openclaw plugins list    # ✅ 实测存在
```

> **真名 vs 虚构对照**：

| ❌ 虚构 | ✅ 真名 |
|---|---|
| `openclaw plugin`（单数） | `openclaw plugins`（**复数**） |
| `manifest.yaml` | `openclaw.plugin.json`（**JSON5**，不是 YAML） |

**互链**：`chapters/11-plugin-entrypoint/` 全 5 篇 + `api-reference/05-plugin-api.md`（同卷）。
自定义 plugin 的 `~/.openclaw/extensions/` 目录创建与加载 → ⏳ 待实测（底稿 §5）。

### 2.16 key #16 · `session`（dict · 1 子项 · Compaction 疑云现场）

```bash
jq '.session' ~/.openclaw/openclaw.json
# 实测：仅含 { "dmScope": "per-channel-peer" }

jq -r '.session | keys[]' ~/.openclaw/openclaw.json
# 期望：dmScope
```

**✅ 实测真值**：

```json
{
  "session": {
    "dmScope": "per-channel-peer"
  }
}
```

**🚨 Compaction 相关字段全部 0 命中（✅ 底稿 §2.3）**：

```bash
for k in compaction effectiveReserveTokens reserveTokens reserveTokensFloor contextTokenBudget; do
  n=$(jq '..  | objects | has("'"$k"'")' ~/.openclaw/openclaw.json 2>/dev/null | grep -c true || true)
  echo "$k: $n 命中"
done
# 实测结果：全部 0 命中
```

> **结论**：`compaction` / `effectiveReserveTokens` / `reserveTokens` /
> `reserveTokensFloor` / `contextTokenBudget` **均不在 `openclaw.json`**。
> 详见本文 §4「Compaction 真名对照」。

### 2.17 key #17 · `skills`（dict · 1 子项）

```bash
jq '.skills' ~/.openclaw/openclaw.json
jq -r '.skills | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：1
```

**✅ 生产实况（底稿 §3.6）**：

| 项 | 值 |
|---|---|
| `~/.openclaw/workspace/skills/` 目录数 | **236**（`ls \| wc -l` = 238，含 `INDEX.md` + 1 个非目录文件） |
| 无 SKILL.md frontmatter | **47 个** |
| `name` 字段违例 | **55 个** |
| 含 SKILL.md | **221 个** |
| `openclaw skills check --agent tiance` | **Total 253** |

**真实样本（6/6 字段全覆盖）**：
`afrexai-compliance-audit` · `skill-security-audit-v2` · `skill-security-audit`

```bash
openclaw skills check --agent <agent-id>   # ✅ 实测存在
```

> **⚠️ 数字口径差异说明（诚实标注）**：
> 236 目录 ↔ 221 含 SKILL.md ↔ check 报 253 Total —— 三个数字**不是矛盾**，
> 它们统计的对象不同（文件系统目录数 / 有 frontmatter 的数 / 注册表加载数）。
> 引用时**必须带上口径**，不要单说「本机有 236 个 skill」。

**互链**：`chapters/10-skill-registry/`（6 篇）· `api-reference/06-skill-spec.md`（同卷）。
`openclaw skills` 完整子命令集 → ⏳ 待实测。

### 2.18 key #18 · `talk`（dict · 1 子项）

**定位**：语音/对话（TTS / 实时对话）配置。

```bash
jq '.talk' ~/.openclaw/openclaw.json
jq -r '.talk | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：1
```

> **⚠️ 诚实边界**：唯一子键名 → ⏳ 待实测。

### 2.19 key #19 · `tools`（dict · 3 子项）

**定位**：工具层。**与 `skills` 是两个独立子系统**，不是「双协议」。

```bash
jq '.tools' ~/.openclaw/openclaw.json
jq -r '.tools | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：3
```

**🚨 关键概念（易错点）**：

> **Tools 和 Skills 不是一回事。** 它们是**两个独立子系统**，
> 共享 Gateway RPC：`tools.catalog` + `skills.status`。
> 把二者当「双协议」或同一体系是常见错误。

**相关 RPC（✅ 底稿真名）**：

```
tools.catalog      ← 工具目录 RPC
skills.status      ← 技能状态 RPC
```

> **⚠️ 诚实边界**：`tools` 的 3 个子键名 → ⏳ 待实测。

**互链**：`03-protocol-reference.md` §6（TOOLS.md 规范）· `cookbook/03-skills-tools-mcp.md`。

### 2.20 key #20 · `wizard`（dict · 4 子项）

**定位**：向导（onboard / setup 流程的配置）。

```bash
jq '.wizard' ~/.openclaw/openclaw.json
jq -r '.wizard | keys[]' ~/.openclaw/openclaw.json
# 实测子项数：4
```

> **⚠️ 诚实边界**：4 个子键名 → ⏳ 待实测。

**相关命令（✅ 实测存在）**：

```bash
openclaw setup      # 首次配置
openclaw onboard    # 引导
```

> **真名 vs 虚构对照**：

| ❌ 虚构 | ✅ 真名 |
|---|---|
| `openclaw init` | `openclaw setup`（或 `onboard`） |

### 2.21 20 key 一览 · 按类型归组

20 个顶层 key 中，**只有 `bindings` 是数组**，其余 19 个全是对象。

| 类型 | 数量 | key |
|---|---:|---|
| `dict` | **19** | `acp, agents, auth, browser, channels, commands, env, gateway, logging, memory, messages, meta, models, plugins, session, skills, talk, tools, wizard` |
| `list` | **1** | `bindings` |
| **合计** | **20** | — |

**一句话记忆**：

> **20 key 里只有 `bindings` 是数组，其余 19 个全是对象。**

---
## 3. 🚨 不存在的 5 个顶层字段（早期版本误称）

### 3.1 五个幽灵字段

以下 5 个字段**在 `~/.openclaw/openclaw.json` 顶层完全不存在**（✅ 已实测）：

```
runtime   ·   workspace   ·   routing   ·   heartbeat   ·   subagents
```

**验证方法（一条命令判死刑）**：

```bash
for k in runtime workspace routing heartbeat subagents; do
  if jq -e "has(\"$k\")" ~/.openclaw/openclaw.json >/dev/null 2>&1; then
    echo "✅ 顶层存在：$k"
  else
    echo "❌ 顶层不存在：$k"
  fi
done
# 期望输出：5 行全部为 ❌
```

### 3.2 为什么它们会出现在早期资料里

这 5 个词**都是「听起来非常合理」的配置名**——这正是它们危险的原因：

| 幽灵字段 | 为什么「听起来合理」 | 真实位置 |
|---|---|---|
| `runtime` | 「运行时配置」是几乎所有框架的标配概念 | 无此概念层；相关行为分散在 `env` / `commands` |
| `workspace` | 「配置里当然要写工作区路径」 | 工作区由 `agents.entries.<id>` + `--workspace` CLI 参数决定 |
| `routing` | 「消息路由」是 IM bot 的经典配置块 | `channels.<ch>.*` + `agents.entries.<id>.groupChat.mentionPatterns` |
| `heartbeat` | 「心跳」是调度系统的标准术语 | `agents.entries.<id>.heartbeat.every` |
| `subagents` | 「子代理」是 Claude Agent SDK 的原生概念 | `agents.entries`（本就是多 agent 字典）+ `bindings` |

> **共同规律**：这 5 个名字**全部来自其他框架的思维惯性**
> （runtime ← 通用框架 / subagents ← Claude Agent SDK / routing ← IM bot 框架）。
> 写文档时「按惯例补一个顶层块」是最容易产生幽灵字段的路径。

### 3.3 ✅ 真实子层级路径对照表（本书接口层口径）

| ❌ 误植为顶层 | ✅ 真实子层级路径 | 语义 |
|---|---|---|
| `heartbeat` | **`agents.entries.<id>.heartbeat.every`** | 心跳频率（每个 agent 独立） |
| `routing`（半对） | `agents.entries.<id>.groupChat.mentionPatterns` | 提及模式（群内触发规则） |
| `routing`（半对） | `channels.feishu.requireMention` | 飞书群内是否必须 @ |
| `routing`（半对） | `channels.feishu.groupAllowFrom` | 飞书群白名单 |
| `subagents` | `agents.entries`（18 个 agent）+ `bindings`（37 条） | 多智能体编排的配置载体 |
| `runtime` | **无对应顶层**；相关能力散在 `env` / `commands` / `tools` | — |
| `workspace` | **无对应顶层**；工作区通过 `agents.entries.<id>` 与 `agents add --workspace` 落地 | — |

**可直接跑的验证脚本**：

```bash
#!/usr/bin/env bash
# 验证 5 个幽灵字段不存在 + 真实路径存在
CFG=~/.openclaw/openclaw.json

echo "=== A. 幽灵字段（期望全部 NOT FOUND）==="
for k in runtime workspace routing heartbeat subagents; do
  jq -e "has(\"$k\")" "$CFG" >/dev/null 2>&1 \
    && echo "🚨 顶层存在（与底稿冲突！）：$k" \
    || echo "✅ NOT FOUND：$k"
done

echo
echo "=== B. 真实子层级路径（期望存在）==="
echo -n "agents.entries 数量: "; jq '.agents.entries | length' "$CFG"
echo -n "bindings 数量:      "; jq '.bindings | length' "$CFG"
echo -n "heartbeat 路径探测: "
jq -r '.agents.entries | to_entries[]
       | select(.value.heartbeat != null)
       | "\(.key): heartbeat.every=\(.value.heartbeat.every)"' "$CFG" \
  | head -5
echo -n "mentionPatterns 探测: "
jq -r '.agents.entries | to_entries[]
       | select(.value.groupChat.mentionPatterns != null)
       | "\(.key): \(.value.groupChat.mentionPatterns | length) patterns"' "$CFG" \
  | head -5
```

### 3.4 一个真实受害者：第 2 章勘误

`chapters/02-protocols/02-七大契约.md` 顶部带有一条**正式勘误**（2026-09-27 实测），
原文要点：

> 本章多处把 `heartbeat.interval` / `subagents[]` / `routing_rules` /
> `session.compaction` 当作 OpenClaw 配置字段。
> 本机实测 `~/.openclaw/openclaw.json`（45,662 字节）**真实顶层 key 共 20 个**
> （`acp, agents, auth, bindings, browser, channels, commands, env, gateway,
> logging, memory, messages, meta, models, plugins, session, skills, talk, tools, wizard`），
> **不含** `runtime / workspace / routing / heartbeat / subagents`。
> 真实路径：heartbeat → `agents.entries.<id>.heartbeat.every`；
> 多 agent → `agents.entries` + `bindings`；路由 → `channels.*.requireMention` /
> `agents.entries.<id>.groupChat.mentionPatterns`。
> 另：`compaction` / `effectiveReserveTokens` / `reserveTokensFloor` /
> `contextTokenBudget` **均不在** `openclaw.json`（顶层 `session` 仅含 `dmScope`）——
> 相关表述是本书接口层口径，非配置文件字段。

**这段勘误是本书的诚实性样板**——它没有偷偷改掉旧文，而是**在文首公开标注**。
遇到疑似冲突时，**以本卷 `api-reference/` 为准**，因为本卷数据全部来自
`00-实测事实底稿.md`（2026-09-27 / 2026-09-28 两次实测）。

### 3.5 四类幽灵字段的识别信号（写文档时自查）

| 信号 | 说明 | 处置 |
|---|---|---|
| **「按惯例应该有」** | 你没在任何实测输出里见过它，但觉得「框架一般都有」 | 🚨 停下，标 ⏳ 待实测 |
| **来自别的框架的术语** | `subagents`（Claude SDK）、`runtime`（通用框架） | 🚨 先搜本仓是否真有 |
| **扁平得可疑** | 一个多 agent 系统却只有一个全局 `heartbeat` | 🚨 一定在 `agents.entries.<id>` 下 |
| **`jq` 查不到** | `jq '.routing'` 返回 `null` | ✅ 就是不存在，别用 `// {}` 兜底掩盖 |

```bash
# 通用幽灵字段猎手：拿你的候选名去撞
for k in runtime workspace routing heartbeat subagents \
         compaction reserveTokensFloor session.compaction heartbeat.interval; do
  printf '%-24s → ' "$k"
  jq -e "has(\"$k\")" ~/.openclaw/openclaw.json >/dev/null 2>&1 && echo "存在" || echo "不存在"
done
```

### 3.6 互链

- 5 幽灵字段的可跑排坑 → `faq-troubleshooting/F3-心跳与定时.md`（心跳真实路径）
- 路由真实配置 → `faq-troubleshooting/F2-协议-SOUL-AGENTS-USER.md`
- 保姆级配置步骤 → `sop-library/02-protocol-config-sop.md`
- 结构对照 → `03-protocol-reference.md` §7（HEARTBEAT.md 规范）

---

## 4. Compaction 真名对照（`reserveTokensFloor` 误植勘误）

### 4.1 一表定案

| ❌ 误植（v1.0 说法） | ✅ 真名 | 性质 |
|---|---|---|
| `reserveTokensFloor` | **不存在** → `CompactionRequestBudget.reserveTokens` | 字段真名不同 |
| （v1.0 说「可配 20000」） | 常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25` | **不可配置** |
| — | `effectiveReserveTokens` | 派生值（由常量算出） |

### 4.2 关键结论（三条，背下来）

**结论一：`reserveTokensFloor` 这个名字不存在。**
它不是一个「被重命名过的旧字段」，而是**从未存在的虚构字段**。

**结论二：真名是 `CompactionRequestBudget.reserveTokens`。**
注意它是**嵌套类型路径**（`类型.字段`），不是一个扁平配置键。
`CompactionRequestBudget` 是**接口层的类型名**，不是 JSON 里的一个 key。

**结论三：`MAX_COMPACTION_RESERVE_RATIO = 0.25` 是常量，不可配置。**
所以 v1.0 说「可以配 20000」是**双重错误**：
名字错了（`reserveTokensFloor` → `reserveTokens`），性质也错了（可配 → 不可配）。

**推论**：`effectiveReserveTokens` 是**计算出来的**，不是配置出来的：

```
effectiveReserveTokens  =  f(CompactionRequestBudget, MAX_COMPACTION_RESERVE_RATIO=0.25)
                            ↑ 派生值，只读
```

### 4.3 ✅ 实测：本机配置 0 命中

底稿 §2.3 明确：本机 `openclaw.json` 对以下 5 个名字**全部 0 命中**：

```
compaction            → 0
effectiveReserveTokens→ 0
reserveTokens         → 0
reserveTokensFloor    → 0
contextTokenBudget    → 0
```

原因：顶层 `session` **仅含 `dmScope`**（`session.dmScope = "per-channel-peer"`）。

```bash
# 复现 0 命中（递归扫全部嵌套层级，比裸 has() 更彻底）
CFG=~/.openclaw/openclaw.json
for k in compaction effectiveReserveTokens reserveTokens reserveTokensFloor contextTokenBudget; do
  printf '%-26s → ' "$k"
  cnt=$(jq --arg k "$k" '[paths | select(.[-1] == $k)] | length' "$CFG")
  echo "$cnt 命中"
done
# 期望：全部 0
```

> **⚠️ 关键理解（最容易搞错的一点）**：
> **0 命中 ≠ 功能不存在。** Compaction（上下文压缩）机制当然存在，
> 只是它**不在 `openclaw.json` 里配置**——它属于**接口层 / 运行时**，
> 由 `CompactionRequestBudget` 类型 + `MAX_COMPACTION_RESERVE_RATIO` 常量共同决定。
>
> **不要把「配置里查不到」误读为「这个功能没有」。**

### 4.4 三层概念分层图

```
┌─────────────────────────────────────────────────────────┐
│ 第 1 层：配置文件层（~/.openclaw/openclaw.json）          │
│   ✅ 实测：无 compaction / reserve* / contextTokenBudget  │
│   ✅ session 仅含 dmScope                                 │
├─────────────────────────────────────────────────────────┤
│ 第 2 层：接口层（类型定义 · 本书 API 参考卷口径）          │
│   CompactionRequestBudget                                 │
│     └── reserveTokens          ← ✅ 真名字段              │
│   effectiveReserveTokens       ← ✅ 派生值                │
├─────────────────────────────────────────────────────────┤
│ 第 3 层：常量层（不可配置）                                │
│   MAX_COMPACTION_RESERVE_RATIO = 0.25                     │
└─────────────────────────────────────────────────────────┘
```

**一句话**：

> **配置层查不到 → 接口层有类型 → 常量层定死比例。**

### 4.5 引用规范（写文档/写 issue 时必须遵守）

| 场景 | ❌ 错误写法 | ✅ 正确写法 |
|---|---|---|
| 提字段名 | `reserveTokensFloor` | `CompactionRequestBudget.reserveTokens` |
| 提上限 | 「可配 20000」 | 「常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25`，**不可配置**」 |
| 提派生量 | （无） | `effectiveReserveTokens`（由上述常量派生） |
| 提配置位置 | 「在 `openclaw.json` 的 compaction 段」 | 「不在 `openclaw.json`；属接口层口径」 |

### 4.6 常见误用场景（真实踩坑）

**场景 A：想调大压缩保留量，去改配置**
→ 找不到字段，开始怀疑配置文件位置 → 又去翻 `~/.openclaw/workspace/openclaw.json`
→ 白烧时间。**正解**：该值由常量决定，不可配。

**场景 B：grep 源码找不到 `reserveTokensFloor`，以为代码拉错了**
→ 因为它根本不存在。**正解**：grep `effectiveReserveTokens` +
`MAX_COMPACTION_RESERVE_RATIO`，这两个才该命中。

```bash
# 正确的源码侧验真（前提：你 clone 过 OpenClaw 源码）
grep -rn "effectiveReserveTokens\|MAX_COMPACTION_RESERVE_RATIO" <openclaw-src>/ \
  | head -10
# 期望：能命中这两个真名
```

**场景 C：文档里写「compaction_policy 配置项」**
→ `compaction_policy` 也是本书**接口层口径**，不是 `openclaw.json` 字段。
引用时须说明「接口层概念，非配置文件字段」。

### 4.7 与 MEMORY 协议的关系

MEMORY 协议（`MEMORY.md`）是**文件模板**（见 `03-protocol-reference.md` §7），
Compaction（上下文压缩）是**运行时机制**。二者的关系：

| 维度 | MEMORY.md | Compaction |
|---|---|---|
| 形态 | 文件（工作区） | 运行时机制 |
| 可编辑 | ✅ 人工编辑 | ❌ 常量决定 |
| 位置 | `agents/<id>/MEMORY.md` | 不在 `openclaw.json` |
| 本书卷册 | `03-protocol-reference.md` | 本节（`02-config-schema.md`） |

> **❌ 不要写「MEMORY 协议里的 compaction_policy 4 类 memory」**——
> OpenClaw 真正的 MEMORY 是**文件模板**，不是 MemGPT 的
> core / archival / recall / archive 4 类结构。

### 4.8 互链

- 协议层记忆 → `03-protocol-reference.md` §7
- 记忆训练配方 → `cookbook/02-protocol-HEARTBEAT-MEMORY.md` · `sop-library/04-memory-training-sop.md`
- 记忆与会话排坑 → `faq-troubleshooting/F4-记忆与会话.md`
- 结构勘误 → `chapters/02-protocols/02-七大契约.md` 顶部勘误块

---
## 5. 配置验证脚本（可直接运行）

> **用途**：一条命令自检 `~/.openclaw/openclaw.json` 是否符合本卷记录的真实 schema。
> **依赖**：Python 3.9+（仅标准库，无第三方依赖）。
> **安全**：脚本**只读**，不修改任何文件；对 `auth` / `env` 段**只输出键名不输出值**。

### 5.1 脚本全文（保存为 `validate_openclaw_config.py`）

```python
#!/usr/bin/env python3
"""
openclaw.json 配置校验器 · v1.0
依据：《API 参考附录卷 · 02-config-schema.md》 + 00-实测事实底稿.md（2026-09-28）

校验项：
  1. 路径真身（~/.openclaw/openclaw.json 存在；workspace 下的误称路径不存在）
  2. 顶层 20 key 完整性
  3. 5 个幽灵字段（runtime/workspace/routing/heartbeat/subagents）不存在
  4. Compaction 5 名字 0 命中
  5. 已知关键子路径存在性（不做值断言，因为值随部署演进）
  6. 安全自检（auth/env 是否会被无意外泄）
  7. llm primary == fallback[0] 自循环检测（8/19 事故模式）

退出码：0 = 全部通过；1 = 有 ❌；2 = 有 🚨 严重问题
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------- 常量基线

TRUTH_PATH = Path.home() / ".openclaw" / "openclaw.json"
GHOST_PATH = Path.home() / ".openclaw" / "workspace" / "openclaw.json"

EXPECTED_TOP_KEYS = {
    "acp", "agents", "auth", "bindings", "browser", "channels", "commands",
    "env", "gateway", "logging", "memory", "messages", "meta", "models",
    "plugins", "session", "skills", "talk", "tools", "wizard",
}

GHOST_TOP_FIELDS = ["runtime", "workspace", "routing", "heartbeat", "subagents"]

COMPACTION_NAMES = [
    "compaction", "effectiveReserveTokens", "reserveTokens",
    "reserveTokensFloor", "contextTokenBudget",
]

LIST_TYPE_KEYS = {"bindings"}          # 唯一一个 array 类型顶层 key
DICT_TYPE_KEYS = EXPECTED_TOP_KEYS - LIST_TYPE_KEYS

SENSITIVE_SECTIONS = ["auth", "env", "channels"]   # 含凭据，值必须遮蔽

# 已知真实子路径（存在性检查，不断言值）
KNOWN_SUBPATHS = [
    "agents.entries",
    "session.dmScope",
]

PATH_ONLY_SUBPATHS = [   # 存在性随部署而异，仅探测不判失败
    "agents.entries.<id>.heartbeat.every",
    "agents.entries.<id>.groupChat.mentionPatterns",
    "channels.feishu.requireMention",
    "channels.feishu.groupAllowFrom",
]

# ---------------------------------------------------------------- 结果收集

class Report:
    def __init__(self) -> None:
        self.ok: list[str] = []
        self.warn: list[str] = []
        self.err: list[str] = []
        self.crit: list[str] = []

    def good(self, msg: str) -> None:
        self.ok.append(msg)

    def warning(self, msg: str) -> None:
        self.warn.append(msg)

    def error(self, msg: str) -> None:
        self.err.append(msg)

    def critical(self, msg: str) -> None:
        self.crit.append(msg)

    def emit(self) -> int:
        for m in self.ok:
            print(f"  ✅ {m}")
        for m in self.warn:
            print(f"  ⚠️  {m}")
        for m in self.err:
            print(f"  ❌ {m}")
        for m in self.crit:
            print(f"  🚨 {m}")
        code = 0
        if self.err:
            code = 1
        if self.crit:
            code = 2
        return code


def hr(title: str) -> None:
    print()
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


# ---------------------------------------------------------------- 工具函数

def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def walk_keys(node, out: set[str]) -> None:
    """递归收集所有出现过的 key 名（不区分层级）。"""
    if isinstance(node, dict):
        for k, v in node.items():
            out.add(k)
            walk_keys(v, out)
    elif isinstance(node, list):
        for item in node:
            walk_keys(item, out)


def dig(cfg: dict, dotted: str):
    """按 'a.b.c' 取嵌套值；<id> 占位符返回第一层 keys。"""
    cur = cfg
    for part in dotted.split("."):
        if part == "<id>":
            return list(cur.keys()) if isinstance(cur, dict) else None
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


# ---------------------------------------------------------------- 检查 1

def check_paths(rep: Report) -> Path | None:
    hr("检查 1 · 配置路径真身")
    if not TRUTH_PATH.exists():
        rep.critical(f"真身不存在：{TRUTH_PATH}")
        return None
    size = TRUTH_PATH.stat().st_size
    rep.good(f"真身存在：{TRUTH_PATH}（{size:,} 字节）")
    if size in (45662, 45445):
        rep.good(f"字节数与底稿一致口径（45,662 / 45,445）")
    else:
        rep.warning(
            f"字节数 {size:,} 与底稿快照（45,662 / 45,445）不同 "
            f"—— 正常（配置会演进），但请确认你读的是最新实测"
        )
    if GHOST_PATH.exists():
        rep.critical(
            f"误称路径竟然存在：{GHOST_PATH} —— 这是孤儿配置，"
            f"OpenClaw 不会读取它，请核对来源后删除"
        )
    else:
        rep.good(f"误称路径不存在（符合预期）：{GHOST_PATH}")
    return TRUTH_PATH


# ---------------------------------------------------------------- 检查 2

def check_top_keys(cfg: dict, rep: Report) -> None:
    hr("检查 2 · 顶层 20 key 完整性")
    actual = set(cfg.keys())
    missing = EXPECTED_TOP_KEYS - actual
    extra = actual - EXPECTED_TOP_KEYS

    rep.good(f"顶层 key 数：{len(actual)}（基线：20）")
    if missing:
        rep.error(f"缺失基线 key（{len(missing)}）：{sorted(missing)}")
    else:
        rep.good("20 个基线 key 全部存在")

    if extra:
        rep.warning(
            f"出现基线外的新 key（{len(extra)}）：{sorted(extra)} "
            f"—— 可能是版本升级新增，请核对后更新基线"
        )
    else:
        rep.good("无基线外多余 key")

    # 类型校验
    for k in sorted(LIST_TYPE_KEYS & actual):
        if not isinstance(cfg[k], list):
            rep.error(f"`{k}` 应为 list，实际为 {type(cfg[k]).__name__}")
        else:
            rep.good(f"`{k}` 类型正确：list（{len(cfg[k])} 元素）")
    for k in sorted(DICT_TYPE_KEYS & actual):
        if not isinstance(cfg[k], dict):
            rep.error(f"`{k}` 应为 dict，实际为 {type(cfg[k]).__name__}")

    # 已知业务量（仅信息，不断言）
    print()
    print("  --- 业务量快照（随部署演进，仅参考）---")
    for label, dpath in [
        ("agents.entries", "agents.entries"),
        ("bindings", "bindings"),
        ("channels.feishu", "channels.feishu"),
    ]:
        val = dig(cfg, dpath)
        if val is not None:
            try:
                n = len(val)
                print(f"    {label:<22} = {n}")
            except TypeError:
                print(f"    {label:<22} = <不可计数>")


# ---------------------------------------------------------------- 检查 3

def check_ghosts(cfg: dict, rep: Report) -> None:
    hr("检查 3 · 5 个幽灵顶层字段（应不存在）")
    bad = [k for k in GHOST_TOP_FIELDS if k in cfg]
    if bad:
        for k in bad:
            rep.critical(
                f"顶层出现幽灵字段 `{k}` —— 与底稿冲突，"
                f"该字段不是 OpenClaw 配置项，请核查文档来源"
            )
    else:
        rep.good(
            "5 个幽灵字段均不存在（符合底稿）："
            "runtime / workspace / routing / heartbeat / subagents"
        )
    print()
    print("  --- 真实位置提示 ---")
    print("    heartbeat → agents.entries.<id>.heartbeat.every")
    print("    routing   → channels.<ch>.requireMention / "
          "agents.entries.<id>.groupChat.mentionPatterns")
    print("    subagents → agents.entries + bindings")


# ---------------------------------------------------------------- 检查 4

def check_compaction(cfg: dict, rep: Report) -> None:
    hr("检查 4 · Compaction 5 名字 0 命中")
    seen: set[str] = set()
    walk_keys(cfg, seen)
    hit = [n for n in COMPACTION_NAMES if n in seen]
    if hit:
        rep.warning(
            f"在某个层级命中 Compaction 相关名字：{hit} "
            f"—— 请确认是否为 OpenClaw 新增的可配置层，并更新底稿"
        )
    else:
        rep.good(
            "compaction / effectiveReserveTokens / reserveTokens / "
            "reserveTokensFloor / contextTokenBudget 全部 0 命中（符合底稿）"
        )
    print()
    print("  --- Compaction 真名对照（接口层口径）---")
    print("    ❌ reserveTokensFloor                     → 不存在")
    print("    ✅ CompactionRequestBudget.reserveTokens   → 真名字段")
    print("    ✅ MAX_COMPACTION_RESERVE_RATIO = 0.25     → 常量，不可配置")
    print("    ✅ effectiveReserveTokens                  → 派生值（只读）")
    print("    ℹ️  0 命中 ≠ 功能不存在；它属接口层而非配置文件层")


# ---------------------------------------------------------------- 检查 5

def check_subpaths(cfg: dict, rep: Report) -> None:
    hr("检查 5 · 已知子路径存在性")
    for p in KNOWN_SUBPATHS:
        val = dig(cfg, p)
        if val is None:
            rep.error(f"已知路径缺失：{p}")
        else:
            shown = val if not isinstance(val, (dict, list)) else f"<{type(val).__name__} len={len(val)}>"
            rep.good(f"{p} = {shown}")

    print()
    print("  --- 部署相关路径（探测性，缺失不算失败）---")
    probes = {
        "agents.entries.<id>.heartbeat.every":
            lambda c: [k for k, v in c.get("agents", {}).get("entries", {}).items()
                       if isinstance(v, dict) and "heartbeat" in v],
        "agents.entries.<id>.groupChat.mentionPatterns":
            lambda c: [k for k, v in c.get("agents", {}).get("entries", {}).items()
                       if isinstance(v, dict) and "groupChat" in v],
        "channels.feishu.requireMention":
            lambda c: ("present" if "requireMention" in c.get("channels", {}).get("feishu", {})
                       else None),
        "channels.feishu.groupAllowFrom":
            lambda c: ("present" if "groupAllowFrom" in c.get("channels", {}).get("feishu", {})
                       else None),
    }
    for name, fn in probes.items():
        try:
            r = fn(cfg)
        except Exception as exc:  # noqa: BLE001
            rep.warning(f"{name} 探测异常：{exc}")
            continue
        if r in (None, [], "None"):
            print(f"    ⏳ {name} = 未观测到（可能是本机未启用该特性）")
        else:
            print(f"    ✅ {name} = {r}")


# ---------------------------------------------------------------- 检查 6

def check_safety(cfg: dict, rep: Report) -> None:
    hr("检查 6 · 安全自检（凭据遮蔽）")
    for sec in SENSITIVE_SECTIONS:
        node = cfg.get(sec)
        if node is None:
            continue
        if isinstance(node, dict):
            rep.good(f"`{sec}` 段存在，键名 {len(node)} 个（值不外输）")
        elif isinstance(node, list):
            rep.good(f"`{sec}` 段存在，{len(node)} 元素（值不外输）")
    print()
    print("  --- 分享配置前的脱敏命令 ---")
    print("    jq 'del(.auth) | del(.env)' ~/.openclaw/openclaw.json")
    print("    jq '.auth | keys' ~/.openclaw/openclaw.json   # 只读键名")
    print("    jq '.env  | keys' ~/.openclaw/openclaw.json   # 只读键名")


# ---------------------------------------------------------------- 检查 7

def check_self_loop(cfg: dict, rep: Report) -> None:
    hr("检查 7 · primary == fallback[0] 自循环检测（8/19 事故模式）")
    entries = cfg.get("agents", {}).get("entries", {})
    if not isinstance(entries, dict) or not entries:
        rep.warning("agents.entries 为空或非字典，跳过自循环检测")
        return
    bad: list[str] = []
    unknown: list[str] = []
    for aid, node in entries.items():
        if not isinstance(node, dict):
            continue
        primary = node.get("model")
        fb = node.get("fallback")
        if primary is None or not isinstance(fb, list) or not fb:
            unknown.append(aid)
            continue
        if fb[0] == primary:
            bad.append(aid)
    if bad:
        for aid in bad:
            rep.critical(
                f"`{aid}` 存在 primary == fallback[0] 自循环 "
                f"—— 主模型失败后第一个降级目标又是自己（8/19 断线根因）"
            )
    else:
        rep.good("未检出 primary == fallback[0] 自循环")
    if unknown:
        print(f"    ⏳ 无法判定（无 model/fallback 字段）：{len(unknown)} 个 agent")
        print(f"       {sorted(unknown)[:8]}{' ...' if len(unknown) > 8 else ''}")
    print()
    print(f"    agent 总数：{len(entries)}（底稿基线 18）")


# ---------------------------------------------------------------- main

def main() -> int:
    print("openclaw.json 配置校验器 · v1.0")
    print("依据：API 参考附录卷 02-config-schema.md + 00-实测事实底稿.md")
    print(f"时间基线：2026-09-28 · 书内口径 OpenClaw 2026.9.4 (3a9d69d)")

    rep = Report()
    path = check_paths(rep)
    if path is None:
        hr("结论")
        return rep.emit()

    try:
        cfg = load_config(path)
    except json.JSONDecodeError as exc:
        hr("结论")
        rep.critical(f"JSON 解析失败：{exc}")
        return rep.emit()

    check_top_keys(cfg, rep)
    check_ghosts(cfg, rep)
    check_compaction(cfg, rep)
    check_subpaths(cfg, rep)
    check_safety(cfg, rep)
    check_self_loop(cfg, rep)

    hr("结论")
    print(f"  ✅ 通过 {len(rep.ok)} · ⚠️ 警告 {len(rep.warn)} "
          f"· ❌ 错误 {len(rep.err)} · 🚨 严重 {len(rep.crit)}")
    code = rep.emit()
    print()
    if code == 0:
        print("  配置与本书记录的真实 schema 一致。")
    elif code == 1:
        print("  存在偏差，请逐条核对上文 ❌ 项。")
    else:
        print("  存在严重问题（🚨），请优先处置，勿继续改配置。")
    return code


if __name__ == "__main__":
    sys.exit(main())
```

### 5.2 运行方式

```bash
# 1) 落盘脚本
#    把 §5.1 全文另存为 validate_openclaw_config.py

# 2) 直接运行（只读，安全）
python3 validate_openclaw_config.py

# 3) 只看结论
python3 validate_openclaw_config.py | tail -12

# 4) 拿退出码接 CI
python3 validate_openclaw_config.py >/dev/null && echo "PASS" || echo "FAIL"
```

### 5.3 预期输出样例（健康配置）

```
openclaw.json 配置校验器 · v1.0
依据：API 参考附录卷 02-config-schema.md + 00-实测事实底稿.md
时间基线：2026-09-28 · 书内口径 OpenClaw 2026.9.4 (3a9d69d)

========================================================================
  检查 1 · 配置路径真身
========================================================================
  ✅ 真身存在：/Users/<you>/.openclaw/openclaw.json（45,662 字节）
  ✅ 字节数与底稿一致口径（45,662 / 45,445）
  ✅ 误称路径不存在（符合预期）：.../workspace/openclaw.json

========================================================================
  检查 2 · 顶层 20 key 完整性
========================================================================
  ✅ 顶层 key 数：20（基线：20）
  ✅ 20 个基线 key 全部存在
  ✅ 无基线外多余 key
  ✅ `bindings` 类型正确：list（37 元素）

  --- 业务量快照（随部署演进，仅参考）---
    agents.entries         = 18
    bindings               = 37
    channels.feishu        = 18

========================================================================
  检查 3 · 5 个幽灵顶层字段（应不存在）
========================================================================
  ✅ 5 个幽灵字段均不存在（符合底稿）：runtime / workspace / routing / heartbeat / subagents

========================================================================
  检查 4 · Compaction 5 名字 0 命中
========================================================================
  ✅ compaction / effectiveReserveTokens / reserveTokens / reserveTokensFloor / contextTokenBudget 全部 0 命中（符合底稿）

========================================================================
  检查 5 · 已知子路径存在性
========================================================================
  ✅ agents.entries = <dict len=18>
  ✅ session.dmScope = per-channel-peer

========================================================================
  检查 6 · 安全自检（凭据遮蔽）
========================================================================
  ✅ `auth` 段存在，键名 1 个（值不外输）
  ✅ `env` 段存在，键名 1 个（值不外输）
  ✅ `channels` 段存在，键名 2 个（值不外输）

========================================================================
  检查 7 · primary == fallback[0] 自循环检测（8/19 事故模式）
========================================================================
  ✅ 未检出 primary == fallback[0] 自循环
    agent 总数：18（底稿基线 18）

========================================================================
  结论
========================================================================
  ✅ 通过 15 · ⚠️ 警告 0 · ❌ 错误 0 · 🚨 严重 0

  配置与本书记录的真实 schema 一致。
```

> **⚠️ 诚实标注**：上例中 `agents.entries = 18`、`bindings = 37`、
> `channels.feishu = 18`、`auth` 1 键、`env` 1 键、`channels` 2 键
> 均来自底稿实测快照（✅）。但 **agent 的具体 `id` 名、每个 agent 的
> `heartbeat.every` 取值、`groupChat.mentionPatterns` 的具体 pattern**
> 底稿未收录 → ⏳ 待实测。

### 5.4 常见报错与处置

| 现象 | 含义 | 处置 |
|---|---|---|
| `真身不存在` 🚨 | `~/.openclaw/openclaw.json` 丢了 | 从最近备份恢复；**不要**去 workspace 下找 |
| `误称路径竟然存在` 🚨 | 有人误建了孤儿配置 | 核对来源后删除；把改动合并回真身 |
| `缺失基线 key` ❌ | 版本差异或配置被裁剪 | 对照 `openclaw setup` 重建缺失段 |
| `出现基线外的新 key` ⚠️ | 版本升级新增 | 更新本卷 §2.0 基线表 |
| `JSON 解析失败` 🚨 | 语法错误（改了没保存对） | `python3 -m json.tool < cfg` 定位行号 |
| 顶层出现幽灵字段 🚨 | 文档被 v1.0 误植污染 | 删除该字段，改到真实子路径 |
| `primary == fallback[0]` 🚨 | **8/19 断线同款** | 立即改 fallback[0] 为其它模型，**改前先备份** |

### 5.5 最小化折中方案（不想装脚本时）

```bash
# 一行版：路径 + 20 key + 幽灵字段 + Compaction
CFG=~/.openclaw/openclaw.json
echo "真身: $(test -f $CFG && echo OK || echo MISSING)"
echo "误称: $(test -f ~/.openclaw/workspace/openclaw.json && echo '🚨 EXISTS' || echo 'OK gone')"
echo "key数: $(jq 'keys|length' $CFG) (期望 20)"
for k in runtime workspace routing heartbeat subagents; do
  jq -e "has(\"$k\")" $CFG >/dev/null 2>&1 && echo "🚨 幽灵: $k"
done
for k in compaction effectiveReserveTokens reserveTokens reserveTokensFloor contextTokenBudget; do
  n=$(jq --arg k "$k" '[paths|select(.[-1]==$k)]|length' $CFG)
  [ "$n" != "0" ] && echo "⚠️ 命中 $k=$n"
done
echo "bindings: $(jq '.bindings|length' $CFG) (期望 37)"
echo "agents:   $(jq '.agents.entries|length' $CFG) (期望 18)"
echo "done."
```

### 5.6 互链

- 脚本涉及的心跳路径 → `03-protocol-reference.md` §7
- 脚本涉及的路由路径 → `faq-troubleshooting/F3-心跳与定时.md`
- 配置 SOP → `sop-library/02-protocol-config-sop.md`
- 事故背景（8/19 自循环）→ `case-library/01-real-incidents.md`

---
## 6. 诚实边界

> **原则**：本卷**只写实测到的**。没实测到的一律标 ⏳，
> **绝不**用「按常规应该有」的方式补齐。你看到的每个 ✅ 都有底稿出处。

### 6.1 ✅ 已实测确认（可直接引用）

**路径与文件层**

- ✅ 真身路径 `~/.openclaw/openclaw.json`
- ✅ 文件大小 45,662 字节（早期观测 45,445 字节，两者均曾出现在实测记录中）
- ✅ `~/.openclaw/workspace/openclaw.json` **不存在**（`ls` 已否定）
- ✅ 顶层 key 数 = **20**
- ✅ 20 个顶层 key 的**完整名称列表**
- ✅ 每个顶层 key 的**类型**（19 dict + 1 list）
- ✅ 每个顶层 key 的**直接子项数量**（快照值）
- ✅ `bindings` 是 **list** 类型，含 **37** 元素
- ✅ `session` 仅含 `dmScope`，值为 `per-channel-peer`

**幽灵字段层**

- ✅ `runtime` / `workspace` / `routing` / `heartbeat` / `subagents`
  **均不在顶层**
- ✅ 真实路径：`agents.entries.<id>.heartbeat.every`
- ✅ 真实路径：`agents.entries.<id>.groupChat.mentionPatterns`
- ✅ 真实路径：`channels.feishu.requireMention`
- ✅ 真实路径：`channels.feishu.groupAllowFrom`

**Compaction 层**

- ✅ `compaction` / `effectiveReserveTokens` / `reserveTokens` /
  `reserveTokensFloor` / `contextTokenBudget` 在 `openclaw.json` **全部 0 命中**
- ✅ 真名字段 `CompactionRequestBudget.reserveTokens`
- ✅ 常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25`（不可配置）
- ✅ 派生值 `effectiveReserveTokens`

**业务量层**

- ✅ 18 agent（`agents.entries` 18 键）
- ✅ 主模型分布：opus-4-8 ×9 / gpt-5.6-sol ×4 / gpt-5.5 ×2 / gpt-5.6-terra ×2 / deepseek-v4-flash ×1
- ✅ 37 binding = Telegram 19 + 飞书 18
- ✅ 飞书 18 个账号
- ✅ `channels.feishu` 子项数与账号数一致（18）
- ✅ 61 条 automations（早期实测 43 条，两次均曾观测到）
- ✅ plugins 51/69 enabled（早期）→ 53/73 enabled（本机 live）
- ✅ `~/.openclaw/extensions/` **本机不存在**
- ✅ `a2a` 插件 disabled（`stock:a2a/index.js`）
- ✅ `openclaw mcp` = 14 子命令；命名空间 `mcp.servers`；`mcp list` = **0 配置**
- ✅ skills 目录 236（`ls | wc -l` = 238）
- ✅ 47 无 frontmatter / 55 name 违例 / 221 含 SKILL.md

**命令层（真名）**

- ✅ `openclaw agents` 子命令 = `add · bind · bindings · delete · list`
- ✅ `openclaw plugins` = 15 子命令（复数）
- ✅ `openclaw acp` = Zed ACP bridge
- ✅ `openclaw backup create` / `openclaw health` / `openclaw doctor` /
  `openclaw pairing` / `openclaw promos` / `openclaw proxy` /
  `openclaw config` / `openclaw audit` / `openclaw setup` / `openclaw onboard`
- ✅ `openclaw automations list` 存在
- ✅ `openclaw skills check --agent <id>` 存在（tiance → Total 253）

**事故层**

- ✅ 8/19 断线根因链：MiniMax-M3 空 body → 17-18 fallback 首位被占 →
  轩辕 `primary == fallback[0]` 自循环
- ✅ 8/19 备份文件名 `openclaw.json.bak.pre-fix-2026-08-19-0921`
- ✅ 9/21 飞书事故：`requireMention: true` + `groupAllowFrom` 仅丘总 →
  6 账号 disconnected，静默 >60min
- ✅ 上游修复 PR #152777 · OPEN（feishu groupPolicy）
- ✅ 能力矩阵 26 天未续期（2026-09-01 后无新记录，cron error 4x）

### 6.2 ⏳ 待实测（本卷未覆盖，禁止补全）

**配置子键层**

- ⏳ `acp` 的 5 个子键名称
- ⏳ `agents` 除 `entries` 外的另外 2 个子键名称
- ⏳ `auth` 的唯一子键名
- ⏳ `bindings` 元素的完整字段集
- ⏳ `browser` 的 3 个子键名
- ⏳ `channels` 除 `feishu` 外的第 2 个子键名
- ⏳ `channels.feishu` 除 `requireMention` / `groupAllowFrom` 外的子键
- ⏳ `commands` 的 6 个子键名
- ⏳ `env` 的唯一子键名
- ⏳ `gateway` 的 7 个子键名
- ⏳ `logging` 的唯一子键名 + 日志实际落盘路径
- ⏳ `memory` 的唯一子键名
- ⏳ `messages` 的唯一子键名
- ⏳ `meta` 的 2 个子键名
- ⏳ `models` 的 2 个子键名
- ⏳ `plugins` 的唯一子键名
- ⏳ `skills` 的唯一子键名
- ⏳ `talk` 的唯一子键名
- ⏳ `tools` 的 3 个子键名
- ⏳ `wizard` 的 4 个子键名

**值层**

- ⏳ 18 个 agent 的**具体 id 名**
- ⏳ 每个 agent 的 `heartbeat.every` **实际取值**
- ⏳ 每个 agent 的 `groupChat.mentionPatterns` **实际 pattern 列表**
- ⏳ `channels.feishu.requireMention` / `groupAllowFrom` 的**当前值**
- ⏳ 飞书 13 个账号的完整 `appId`（仅 5 个实测完整）
- ⏳ `models` 段 `primary` / `fallback` 的完整取值

**命令/流程层**

- ⏳ `openclaw health` 完整输出（**被 Gateway state 库独占锁遮挡**）
- ⏳ `openclaw automations add` 实际落盘（避免污染 61 条编排）
- ⏳ `openclaw plugins install` 全生命周期
- ⏳ ClawHub publish 流程
- ⏳ A2A TCK 测试
- ⏳ SLCP bridge demo
- ⏳ `~/.openclaw/extensions/` 目录创建与加载
- ⏳ MCP server 实际注册（本机 0 配置）
- ⏳ `openclaw skills` 完整子命令集
- ⏳ `openclaw gateway` 子命令集

### 6.3 口径冲突的处理规则

当本卷与其它资料冲突时，**按以下优先级**：

1. **本卷 §2/§3/§4**（来自 `00-实测事实底稿.md`，2026-09-27/28 实测）
2. **底稿本身**（同上，同源）
3. **`chapters/` 各章**（可能含 v1.0 残留；看文首有无勘误块）
4. **v1.0 及更早资料**（默认视为**已被勘误**，除非本卷确认）

**遇到冲突的标准动作**：跑 §5 的校验脚本，以 `jq` 实测输出为准，
然后把结论回报给本书维护者（天策），并标注实测时间。

### 6.4 版本口径说明（重要）

- **书内统一口径**：OpenClaw **2026.9.4 (3a9d69d)**
- **本机 live 复核**：OpenClaw **2026.9.6 (eb377ac)**

两者差异（✅ 已诚实标注）：plugins 从 51/69 → 53/73。
**本卷所有 schema 事实在两个版本上一致**（顶层 20 key、幽灵字段、Compaction 真名均未变）。
若你的版本 ≥ 9.4 且 < 9.6，`jq` 结果应与本卷一致。

---

## 7. 常见配置任务速查（对着做）

### 7.1 任务 → 路径 → 命令 对照表

| 我想做的事 | 改哪里（真实路径） | 辅助命令 |
|---|---|---|
| 改某 agent 的心跳频率 | `agents.entries.<id>.heartbeat.every` | `openclaw automations list` |
| 改群内触发规则（提及模式） | `agents.entries.<id>.groupChat.mentionPatterns` | — |
| 让飞书群不必 @ 就响应 | `channels.feishu.requireMention` = `false` | `openclaw health` |
| 扩飞书群白名单 | `channels.feishu.groupAllowFrom` | — |
| 新增一个 agent | `agents.entries.<new-id>`（+ 工作区目录） | `openclaw agents add <id> --workspace <dir>` |
| 把 agent 绑到渠道 | `bindings`（append 一条） | `openclaw agents bind` / `openclaw agents bindings` |
| 删除一个 agent | 删 `agents.entries.<id>` + 相关 binding | `openclaw agents delete <id>` |
| 换 agent 主模型 | `agents.entries.<id>.model` | `openclaw promos` |
| 修 primary/fallback 自循环 | `agents.entries.<id>.fallback[0]` | — （见 §5 检查 7） |
| 归档整个配置 | — | `openclaw backup create` |
| 首次配置 | — | `openclaw setup` / `openclaw onboard` |
| 健康检查 | — | `openclaw health` / `openclaw doctor` |
| 装/管理插件 | `plugins` | `openclaw plugins list` |

### 7.2 改配置的标准 5 步流程

```bash
# 步骤 1 · 定位真身（永远先做这一步）
CFG=~/.openclaw/openclaw.json
test -f "$CFG" || { echo "🚨 真身不存在，停手"; exit 1; }

# 步骤 2 · 备份（带用途 + 时间戳）
cp "$CFG" "$CFG.bak.pre-fix-$(date +%Y-%m-%d-%H%M)"

# 步骤 3 · 先验证 JSON 语法（不要用编辑器直接存完就走）
python3 -m json.tool "$CFG" > /dev/null && echo "✅ 语法 OK"

# 步骤 4 · 改（推荐 jq 改动，可复现、可 diff）
jq '.channels.feishu.requireMention = false' "$CFG" > /tmp/new.json \
  && mv /tmp/new.json "$CFG"

# 步骤 5 · 复验 + 跑校验脚本
python3 -m json.tool "$CFG" > /dev/null && echo "✅ 改后语法 OK"
python3 validate_openclaw_config.py | tail -8
```

> **⚠️ 顺序铁律**：**先备份 → 再验证语法 → 后改 → 再复验**。
> 反过来（改完才想起备份）在 8/19 事故里被证明会显著延长恢复时间。

### 7.3 三个最危险的改动（做前必读）

| 危险改动 | 风险 | 必读 |
|---|---|---|
| `channels.feishu.requireMention` + `groupAllowFrom` | **同款 9/21 事故**：静默断线 >60min | `case-library/01-real-incidents.md` |
| `agents.entries.<id>.fallback` | **同款 8/19 事故**：自循环 → 全军团断线 | §5 检查 7 + `case-library/01-real-incidents.md` |
| 批量改 `agents.entries` | 18 个 agent 同时失效无回退点 | 分批改 + 每批备份 |

---

## 8. 业界对位（扩展阅读）

> 来源：底稿 §8。**差异已诚实标注**。

| 业界项目 | 本书对位章节 | 差异（诚实标注） |
|---|---|---|
| LangChain（350 万词） | 全书 | 规模差距 |
| LlamaIndex（1,756 md） | 全书 | 规模差距 |
| OpenAI Cookbook（275 nb） | cookbook 30 例 | 数量差距 |
| Anthropic Skills | `chapters/11-skill-registry` | 对位 |
| MCP（Anthropic） | `chapters/09-mcp-binding` | 对位 |
| A2A（Linux Foundation） | `chapters/10-a2a-binding` | 对位 |
| Claude Agent SDK | `chapters/02-protocols` / `03-skeleton` | 对位 |
| OpenAI Agents SDK | `chapters/03-skeleton` | 对位 |

**与 Claude Agent SDK 的关系（配置视角）**：

- Claude Agent SDK 的 `subagents` 概念 → OpenClaw 对应 **`agents.entries`**
- Claude Permission API 是**运行时校验** → OpenClaw 的 `USER.md` 是**文件级声明**，
  **两者互补不替代**
- Claude Agent SDK 的 tools 概念 → OpenClaw 的 `tools` 段（与 `skills` **独立**）

---

## 9. 互链总表

| 方向 | 目标 | 用途 |
|---|---|---|
| 本文 | `03-protocol-reference.md` | 7 大协议文件规范（SOUL/AGENTS/USER/TOOLS/IDENTITY/HEARTBEAT/MEMORY） |
| 本文 | `00-实测事实底稿.md` | 本文全部事实来源 |
| 本文 | `04-*.md` / `05-plugin-api.md` / `06-skill-spec.md` | 同卷其余分册 |
| 本文 | `faq-troubleshooting/F1-环境与安装.md` | 配置改完不生效 |
| 本文 | `faq-troubleshooting/F2-协议-SOUL-AGENTS-USER.md` | 协议 / 路由问题 |
| 本文 | `faq-troubleshooting/F3-心跳与定时.md` | `heartbeat.every` 相关 |
| 本文 | `faq-troubleshooting/F4-记忆与会话.md` | `session` / 记忆 |
| 本文 | `faq-troubleshooting/F5-Skills-Tools-MCP.md` | `tools` / `skills` / MCP |
| 本文 | `faq-troubleshooting/F7-治理漂移体检.md` | `gateway` / 治理 |
| 本文 | `faq-troubleshooting/F-Top20-高频速查.md` | 高频速查 |
| 本文 | `sop-library/01-environment-setup-sop.md` | 环境搭建 |
| 本文 | `sop-library/02-protocol-config-sop.md` | **配置 SOP（本文操作层）** |
| 本文 | `sop-library/03-heartbeat-monitor-sop.md` | 心跳监控 |
| 本文 | `cookbook/01-protocol-SOUL.md` | SOUL 可跑配方 |
| 本文 | `cookbook/03-skills-tools-mcp.md` | tools/skills/MCP 配方 |
| 本文 | `case-library/01-real-incidents.md` | 8/19 + 9/21 事故全文 |
| 本文 | `chapters/02-protocols/02-七大契约.md` | 7 契约 + **顶部勘误块** |
| 本文 | `chapters/03-skeleton/03-系统骨架.md` | 7 协议如何嵌入子系统 |
| 本文 | `00-术语对照表·v3.0行业标准版.md` | 35 条改名表 |

---

## 10. 附录 · 术语双写索引（本文出现过的）

> 首次出现必双写；本表汇总本文用到的全部条目。

| 行业标准名 | 原内部黑话 | 英文 alias |
|---|---|---|
| Supervisor Layer | 监军 | Supervisor Layer |
| 多智能体编排 | 军团编制 | Multi-Agent Orchestration |
| Mentor Agent | 教练虾 | Mentor Agent |
| 响应让渡协议 | 让位协议 | Response Yield Protocol（RYP） |
| 任务交接协议 | — | Task Handover Protocol（THP） |
| 智能体集群 | 军团 | Agent Fleet |
| 修复工单 | 整改单 | Remediation Ticket |
| 三证据验证 | 三证验真 | Three-Evidence Verification（TEV） |
| SLCP | ACP | Silicon Life Collaboration Protocol |
| 主动性边界三档制 | — | Autonomy Boundary Triad |

**本文特别提示的两组同形异义**：

1. **`acp`（OpenClaw 命令/配置）** vs **ACP（本书 v1.0 内部术语）**
   → 本书 v3.0 已把内部术语改名 **SLCP**，避免与 OpenClaw 的 `acp` 撞名。
2. **ACP（Agent Client Protocol，Zed 生态）** vs **SLCP（Silicon Life Collaboration Protocol，本书）**
   → 引用时**必须写全**，不要简称。

---

## 11. 附录 · 真名 vs 虚构 · 速查卡（可打印）

| ❌ 虚构 | ✅ 真名 |
|---|---|
| `~/.openclaw/workspace/openclaw.json` | `~/.openclaw/openclaw.json` |
| `openclaw init` | `openclaw setup` / `openclaw onboard` |
| `openclaw agents create X` | `openclaw agents add X --workspace <dir>` |
| `openclaw chat --agent X --prompt Y` | `openclaw agent --agent X --message Y` |
| `openclaw agents health-check` | `openclaw health` / `openclaw doctor` |
| `openclaw agents archive` | `openclaw backup create` |
| `openclaw plugin`（单数） | `openclaw plugins`（复数） |
| `manifest.yaml` | `openclaw.plugin.json`（JSON5） |
| `openclaw cron add --schedule X --target Y --prompt Z` | `openclaw cron add --cron X --session Y --message Z` |
| 顶层 `heartbeat` | `agents.entries.<id>.heartbeat.every` |
| 顶层 `routing` | `channels.*.requireMention` / `agents.entries.<id>.groupChat.mentionPatterns` |
| 顶层 `subagents` | `agents.entries` + `bindings` |
| 顶层 `runtime` | 无对应顶层 |
| 顶层 `workspace` | 无对应顶层 |
| `reserveTokensFloor` | `CompactionRequestBudget.reserveTokens` |
| 「compaction 可配 20000」 | 常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25`，**不可配置** |

---

**分册版本**：v5.0 行业标准版 · 2026-09-28
**数据来源**：`api-reference/00-实测事实底稿.md`（2026-09-27 / 2026-09-28 实测）
**维护者**：天策（Supervisor Layer）
**许可**：MIT（跟随 OpenClaw 主仓）
**校验方式**：跑 §5 脚本，以 `jq` 实测输出为准

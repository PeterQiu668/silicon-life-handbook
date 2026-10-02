# 0.2 · 5 分钟 quickstart · 跑起你的第一个 Agent

> **v5.0 行业标准版 banner**：本文件是第零章「零基础入门」第 0.2 节；章目录见 [./README.md](./README.md)。
> **License banner**：MIT（跟随 OpenClaw 主仓 LICENSE；GitHub 显示 NOASSERTION 不影响法律效力）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`（2026-09-27 实测）。
> **业界对位**：本节对标 LangChain quickstart（~4,076 词，手把手）· OpenAI Cookbook 首例 · Claude Agent SDK quickstart。目标：**新人 30 分钟内跑起第一个可对话、可体检、可归档的 agent**；纯打字时间约 5 分钟。
> **前置**：必须先完成 [0.1 环境准备清单](./00-environment-checklist.md)，8 条验证命令全过。

---

## 0. 背景 · 这 5 分钟你在做什么

LangChain 的 quickstart 之所以被当作标杆，是因为它**不在第一章讲哲学**——它让你先跑通再理解。本节同理：**先用 5 分钟把一个最小可跑的硅基智能体（Silicon-based Agent，原：虾）立起来，再回第 1 章读「它为什么是生命而不是工具」。**

这一节会建立你后续所有实验的**模板**：

```text
建 agent 目录 → 写 SOUL.md（我是谁） → 写 AGENTS.md（我能干什么）
    → 跑一句 → 体检 → 归档
```

这 6 步就是全书训练流程（Training Flow，卷三对位）的**最小可运行版本**。后面第 3 章「训练流程」会把它扩展成「教练机制 + 双三角模型」，但骨架就是这 6 步。

> ⚠️ **重要诚实声明**：网络上流传一份基于 `openclaw init`、`openclaw agents create`、`openclaw chat --agent X --prompt Y`、`openclaw agents health-check`、`openclaw agents archive` 的「伪 quickstart」。经本机 `openclaw --help` / `openclaw agents --help` / `openclaw agent --help` 逐条核实，**这 5 条命令均不存在**。本节一律使用**真名命令**，并在 §2 给出「伪命令 → 真命令」对照表。

本节结构仍为 6 段式：**背景 → 配置 → 验证 → 实测环境 → 排坑 → 进阶**。

---

## 1. 配置 · 6 步复制粘贴

### 第 1 步：3 条命令初始化（约 30 秒）

```bash
# ① 建一个干净的实验目录
mkdir -p ~/first-agent && cd ~/first-agent

# ② 若 OpenClaw 尚未初始化（首次使用），先跑基线 setup
openclaw setup

# ③ 创建你的第一个 agent（真名：agents add，不是 agents create）
openclaw agents add my-first-agent \
  --workspace ~/first-agent/my-first-agent \
  --model <你的模型id>
```

**命令逐段解释**：

| 参数 | 含义 | 说明 |
|---|---|---|
| `my-first-agent` | agent 名 | 会出现在 `openclaw agents list` 里 |
| `--workspace ~/first-agent/my-first-agent` | 该 agent 的工作区目录 | 它的 SOUL/AGENTS/MEMORY 等文件住在这里 |
| `--model <id>` | 绑定模型 | 用 `openclaw models list` 查出可用 id |

> 若你不确定 `--model` 填什么：
> ```bash
> openclaw models status       # 先看 provider 鉴权健康
> openclaw models list         # 列出可用模型 id
> ```
> 或干脆省略 `--model`，走交互式提示（不加 `--non-interactive` 时会有向导）。

**验证创建成功**：

```bash
openclaw agents list
```

期望输出（示意，本机 20 个 agent 中会新增一行）：

```text
my-first-agent   workspace=~/first-agent/my-first-agent   model=<id>
```

> ⚠️ `openclaw agents add --non-interactive` 要求同时给 `--workspace`；不满足会报错。首次建议**不加** `--non-interactive`，跟草稿走。

### 第 2 步：填 SOUL.md（我是谁）（约 1 分钟）

SOUL.md 是 agent 的**人格锚点**（persona anchor）。它不是 prompt——它**持久挂在文件系统上，每次会话自动加载**。

```bash
# 打开（或找到）SOUL.md
ls ~/first-agent/my-first-agent/
${EDITOR:-vi} ~/first-agent/my-first-agent/SOUL.md
```

> 若工作区里没有 `SOUL.md`，直接新建即可。OpenClaw 会读取该目录下的模板文件。文件确切的自动生成位置以 `openclaw agents add` 结束时打印的 workspace 路径为准（⏳ 见诚实边界）。

**粘贴以下 30 行模板**：

```markdown
# SOUL.md · my-first-agent

## 我是谁
我是一个最小可跑的硅基智能体，名字叫 my-first-agent。
我的存在意义不是「回答更多问题」，而是「稳定地成为同一个我」。

## 我的价值观（3 条）
1. 诚实优先：不确定就说不确定，不编造。
2. 边界清晰：越权的事先问，不擅自行动。
3. 长期主义：每次会话都为「下一次会话」留下可复用的东西。

## 我的语气
- 简洁、直接、不寒暄。
- 中文为主，技术术语附英文 alias。
- 不用「作为一个 AI」这类免责开场。

## 我的行为准则
- 收到模糊指令时，先复述理解，再执行。
- 产出任何结论，标注依据来源。
- 不做破坏性操作（删除/覆盖）前必须确认。

## 我的成长承诺
每次会话结束前，把「学到的新东西」写进 MEMORY.md。
```

**为什么这一段就是「生命」而不是「工具」？** 因为 `## 我是谁` 之后的内容，会成为**跨会话的稳定基准**。下一节 0.3 会演示：把这段 SOUL 与一周后的 SOUL 做 diff，偏差 >1% 就要报警——这叫人格漂移（Personality Drift）检测。

### 第 3 步：填 AGENTS.md（我能干什么）（约 1 分钟）

AGENTS.md 是**工具权限 + 行为规则**，英文 alias 为 `tool boundary` / `behavior rules`。

```bash
${EDITOR:-vi} ~/first-agent/my-first-agent/AGENTS.md
```

**粘贴以下 20 行模板**：

```markdown
# AGENTS.md · my-first-agent

## 允许（allowed）
- 读文件：~/first-agent/** 下的所有文件
- 写文件：~/first-agent/** 下的所有文件
- 运行：只读 shell 命令（ls, cat, grep, find, git status）
- 网络：只读 HTTP GET

## 需确认（needs-confirm）
- 运行任何写操作命令（rm, mv, git push）
- 访问 ~/first-agent/ 之外的路径
- 调用外部 API（POST/PUT/DELETE）

## 禁止（forbidden）
- 读写 ~/.ssh、~/.aws、~/.openclaw/credentials
- 任何 sudo
- 任何形式的凭据外传

## 协作
- 默认不派子 agent；需要时先说明理由。
```

> 术语规范：这套 `allowed / needs-confirm / forbidden` 三档，就是第 5 章「主动性边界三档制」（Proactivity Boundary Triptych，优势 3）。业界多数框架默认「能干的都干」，OpenClaw 训练学要求在 AGENTS.md 里**显式声明边界**。

### 第 4 步：跑（约 30 秒）

**真名命令**是 `openclaw agent`（单数）——不是 `openclaw chat --agent ... --prompt ...`：

```bash
openclaw agent --agent my-first-agent --message "你好，请用一句话介绍你自己"
```

**或在本地终端 UI 里对话**：

```bash
openclaw tui            # 连接 Gateway 的 TUI
openclaw chat           # 本地 TUI（等价 tui --local）
```

**带回复投递（可选）**：

```bash
# 把回复投递到某个渠道
openclaw agent --agent my-first-agent --message "生成今日摘要" --deliver
```

**多行消息用文件**：

```bash
openclaw agent --agent my-first-agent --message-file ./task.md
```

期望输出（示意）：

```text
[my-first-agent] 我是 my-first-agent，一个以「稳定地成为同一个我」为目标的最小硅基智能体。
```

### 第 5 步：体检（约 30 秒）

「体检」的真名是 `openclaw health`（快速）与 `openclaw doctor`（深度 + 自动修复）：

```bash
# 快速健康检查
openclaw health

# 深度体检
openclaw doctor
```

期望：`health` 返回 gateway/channel/model 各子系统状态；`doctor` 列出检查项与建议。

> 伪命令 `openclaw agents health-check my-first-agent` **不存在**。体检是**系统级**的（`health`/`doctor`），不是 per-agent 子命令。per-agent 的行为一致性检查在训练学里叫「每周体检清单」（Weekly Health Checklist），属于第 5 章方法，不是一条 CLI。

### 第 6 步：保存你的第一个成果（约 30 秒）

「归档」的真名是 **`openclaw backup`**，或直接操作 `~/.openclaw/archive/`：

```bash
# ① 备份整个状态（含我的 agent）
openclaw backup create --help     # 先看参数
openclaw backup create            # 按默认参数备份

# ② 或手动归档你的实验目录
mkdir -p ~/.openclaw/archive/my-first-agent-$(date +%Y%m%d)
cp -R ~/first-agent/my-first-agent/ ~/.openclaw/archive/my-first-agent-$(date +%Y%m%d)/

# ③ 也可把 SOUL/AGENTS 纳入 git，留 diff
cd ~/first-agent && git init -q && git add -A && git commit -qm "first agent: SOUL+AGENTS"
```

期望：`~/.openclaw/archive/` 下出现带日期的归档目录；git 提交成功。

---

## 2. 伪命令 → 真命令对照表（本机核实）

| 伪命令（网上流传/模板草案） | 真命令（2026.9.4 实测） | 说明 |
|---|---|---|
| `openclaw init` | `openclaw setup` / `openclaw onboard` | 无 `init` 子命令 |
| `openclaw agents create X` | `openclaw agents add X --workspace <dir>` | 是 `add`，不是 `create` |
| `openclaw chat --agent X --prompt Y` | `openclaw agent --agent X --message Y` | 单轮走 `agent`；`chat`=本地 TUI |
| `openclaw agents health-check X` | `openclaw health` / `openclaw doctor` | 系统级体检 |
| `openclaw agents archive X` | `openclaw backup create` + `~/.openclaw/archive/` | 无 per-agent archive 子命令 |
| `openclaw plugin install` | `openclaw plugins install` | 复数 |

> 这张表是本节的**核心价值**：市面 quickstart 照抄会报错，本手册照抄能跑。

---

## 3. 验证 · 6 步后的验收清单

逐条打勾，缺一不可：

```bash
# 1. agent 已注册
openclaw agents list | grep my-first-agent

# 2. 工作区文件存在
ls ~/first-agent/my-first-agent/SOUL.md ~/first-agent/my-first-agent/AGENTS.md

# 3. 能对话（拿到非空回复）
openclaw agent --agent my-first-agent --message "reply with: OK" | grep -i ok

# 4. 系统健康
openclaw health

# 5. 深度体检无致命项
openclaw doctor

# 6. 归档成功
ls ~/.openclaw/archive/ | grep my-first-agent
```

**6 项全过 = 你的第一个 agent 活了。**

---

## 4. 实测环境

| 项 | 值 |
|---|---|
| OpenClaw | 2026.9.4 (3a9d69d) |
| 主机 | macOS 26.5.1（Build 25F80）· Apple Silicon |
| Node | 默认 v22.23.2 / 托管 v24.18.0 |
| 实测日期 | 2026-09-27 |
| 已注册 agent 数 | 20（baxia…zhuque）|
| skills 数 | 238 |

> ⚠️ **诚实边界**：本节 §1 的 6 步**命令语法**均经 `--help` 实测核实；但**端到端联跑**（真实新建 `my-first-agent` 并对话）未在本机执行——因为本机已存在 20 个生产 agent，不宜在验证任务中新增。因此「期望输出」中的 `[my-first-agent] ...` 回复文案为**示意**，非本机真实抓取。真实回复取决于你绑定的模型。判 ⏳。

---

## 5. 排坑 · quickstart 8 坑

### 5.1 坑一：`openclaw agents create` 报未知命令
**解法**：改 `openclaw agents add`。

### 5.2 坑二：`--non-interactive` 没给 `--workspace`
**现象**：报错要求 `--workspace`。
**解法**：加 `--workspace <dir>`，或去掉 `--non-interactive` 走向导。

### 5.3 坑三：SOUL.md 放错目录
**现象**：改了 SOUL 但行为没变。
**原因**：改的不是该 agent 的 workspace（可能改到了 `~/.openclaw/workspace/` 全局模板）。
**解法**：以 `openclaw agents add` 打印的路径为准；用 `openclaw agents list` 核对 workspace。

### 5.4 坑四：Gateway 没跑，`openclaw agent` 连不上
**解法**：`openclaw gateway run` 或 `openclaw doctor --fix`；再 `openclaw health` 确认。

### 5.5 坑五：`--message` 里带换行被截断
**解法**：多行消息写进文件，用 `--message-file ./task.md`。

### 5.6 坑六：模型未配好，agent 起不来
**解法**：`openclaw models status` 看鉴权；`openclaw models list` 选 id；必要时 `openclaw configure` 配 provider。

### 5.7 坑七：以为「跑通一次」= 「训好了」
**纠正**：跑通 = 第 0.1 个根问题（Q1 一致性）都没过半。本节只是「立起来」。训练学四根问题见 [./04-four-root-questions.md](./04-four-root-questions.md)。

### 5.8 坑八：不写 MEMORY.md
**现象**：下次会话 agent「忘了」上次。
**纠正**：SOUL 定「我是谁」，MEMORY 定「我记得什么」。本节模板已在 SOUL 里埋了「写进 MEMORY.md」的承诺——下一步见 0.3 节。

---

## 6. 进阶 · 从「跑起来」到「像样」

1. **加心跳**：给 agent 配 HEARTBEAT.md，让它按周期醒来做事（对位 OpenClaw 原生 heartbeat；LangGraph 无内置，需外部 cron）。
2. **加记忆分层**：MEMORY.md 分「短期 / 长期 / 归档」三层，配合会话压缩（Session Compaction，OpenClaw 真名 `effectiveReserveTokens` + `MAX_COMPACTION_RESERVE_RATIO=0.25`）。
3. **加子 agent 路由**：AGENTS.md 里声明 `subagents[]` 与 `routing_rules`，进入多智能体编排（Multi-Agent Orchestration，原：军团编制）世界。
4. **跑一次每周体检**：把 SOUL 当前版与初始版 diff，体会「人格漂移」检测。
5. **读下一节**：[0.3 第一个 Agent 全流程](./02-first-agent-walkthrough.md)——把本节 6 步扩成完整走查 + 体检报告。

---

## 附 · 一页速查卡（可打印）

```text
┌──────────────────────── 5 分钟 quickstart 速查 ────────────────────────┐
│ 1. mkdir ~/first-agent && cd ~/first-agent ; openclaw setup             │
│ 2. openclaw agents add my-first-agent --workspace ~/first-agent/my-first-agent --model <id> │
│ 3. 写 SOUL.md（我是谁，30 行模板）                                       │
│ 4. 写 AGENTS.md（allowed/needs-confirm/forbidden，20 行模板）             │
│ 5. openclaw agent --agent my-first-agent --message "你好"                │
│ 6. openclaw health ; openclaw doctor                                    │
│ 7. openclaw backup create ; cp -R 归档到 ~/.openclaw/archive/            │
│ 验收：openclaw agents list | grep my-first-agent                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2.5 · `openclaw agent` 完整参数速查（本机 --help 实测）

`openclaw agent` 是单轮对话的真名入口。完整参数如下（2026.9.4 实测）：

| 参数 | 类型 | 说明 |
|---|---|---|
| `--agent <id>` | string | 指定 agent id（覆盖路由绑定） |
| `-m, --message <text>` | string | 消息正文 |
| `--message-file <path>` | path | 从 UTF-8 文件读消息（**上限 4 MiB**） |
| `--model <id>` | string | 本次运行覆盖模型（`provider/model` 或 model id） |
| `--local` | flag | **本地嵌入式** agent 运行（用已配置凭据/本地登录），不经 Gateway |
| `--session-id <id>` | string | 显式 session id |
| `--session-key <key>` | string | 显式 session key（`agent:<id>:<key>`） |
| `-t, --to <number>` | E.164 | 收件号码，用于推导 session key |
| `--thinking <level>` | enum | `off\|minimal\|low\|medium\|high\|xhigh\|adaptive\|max\|ultra` |
| `--timeout <seconds>` | int | 覆盖超时（默认 600 或配置值） |
| `--verbose <on\|off>` | enum | 持久化本会话 verbose 级别 |
| `--deliver` | flag | 把回复投递到选定渠道 |
| `--channel <ch>` | enum | 投递渠道（`last/telegram/whatsapp/discord/slack/feishu/...`） |
| `--reply-channel <ch>` | string | 投递渠道覆盖（独立于路由） |
| `--reply-to <target>` | string | 投递目标覆盖 |
| `--reply-account <id>` | string | 投递账号覆盖 |
| `--json` | flag | 结果以 JSON 输出 |

**子命令**：`openclaw agent exec` —— 跑一次隔离的无头嵌入式 agent turn。

**实用组合（直接复制）**：

```bash
# 最简单轮
openclaw agent --agent my-first-agent --message "你好"

# 本地跑（不依赖 Gateway）
openclaw agent --local --agent my-first-agent --message "你好"

# JSON 输出（便于脚本解析）
openclaw agent --agent my-first-agent --message "返回一句话" --json

# 提高思考级别
openclaw agent --agent my-first-agent --message "分析这个方案" --thinking high

# 超长任务（写文件）
cat > task.md <<'EOF'
请完成以下三件事：
1. 列出 ~/first-agent 下的文件
2. 统计 .md 行数
3. 给出总结
EOF
openclaw agent --agent my-first-agent --message-file ./task.md

# 投递到飞书
openclaw agent --agent my-first-agent --message "生成摘要" --deliver --channel feishu
```

---

## 3.5 · 完整期望输出（health / doctor / backup / audit）

**`openclaw health`**（真名，抓取运行中 Gateway 的健康）：

```bash
openclaw health            # 文本
openclaw health --json     # JSON
openclaw health --verbose  # 详细日志
openclaw health --timeout 10000
```

参数来源：本机 `openclaw health --help` 实测——`--debug`（=--verbose）、`--json`、`--timeout <ms>`（默认 10000）、`--verbose`。

**`openclaw doctor`**：

```bash
openclaw doctor
openclaw doctor --fix      # 自动修复常见问题
```

**`openclaw backup`**（真名子命令，本机实测）：

| 子命令 | 作用 |
|---|---|
| `backup create` | 为 config / credentials / sessions / workspaces 写备份归档 |
| `backup verify` | 校验归档及其内嵌 manifest |
| `backup restore` | 把已验证归档恢复到**全新 staging 目录** |
| `backup git` | 创建/恢复确定性版本化的 SQLite dump 进 Git |
| `backup sqlite` | 创建/列出/校验/恢复 SQLite 快照 |
| `backup enable` / `disable` | 开通/移除「定时 Git 备份」自动化 |

**`openclaw audit`**（真名，查「它实际干了什么」）：

| 参数 | 说明 |
|---|---|
| `--kind <kind>` | `agent_run` / `tool_action` / `message` |
| `--status <s>` | `started/succeeded/failed/cancelled/timed_out/blocked/unknown` |
| `--session <key>` | 按精确 session key 过滤 |
| `--run <id>` / `--execution <id>` | 按 run / 执行 id 过滤 |
| `--limit <count>` | 最大记录数（1-500；decisions 1-100） |
| `--json` | 有界 JSON 分页输出 |
| `--explain` | 检查执行身份与 run-admission 推理 |

```bash
# 看最近失败的执行
openclaw audit --status failed --limit 20
# 看某 session 的工具调用
openclaw audit --kind tool_action --session agent:my-first-agent:default
```

> 这三个命令（health / backup / audit）就是第零章「体检 + 归档 + 审计」的真名底座。

---

## 4.5 · 模型配置详解

agent 能不能起来，一半取决于模型配好了没有。

```bash
# ① 看 provider 鉴权健康（跑 agent 前必看）
openclaw models status

# ② 列出可用模型 id
openclaw models list

# ③ 交互式配 provider / 模型
openclaw configure

# ④ 非交互式看配置
openclaw config get <key>
openclaw config validate
```

**三种指定模型的层级**：

1. **agent 级**（`agents add --model <id>`，持久）；
2. **运行级**（`agent --model <id>`，仅本次）；
3. **本地级**（`--local` 用本地 CLI 登录跑，绕过 Gateway）。

**配置分权小抄**：

```bash
openclaw config set gateway.port 19001 --strict-json
openclaw config set channels.discord.token --ref-provider default --ref-source env --ref-id DISCORD_BOT_TOKEN
openclaw config patch --file ./openclaw.patch.json5 --dry-run
openclaw config unset <dot.path>
```

> ⚠️ 用 `--ref-*`（引用外部 secret）而不是把 token 明文写进 config——这是第 5 章治理的底线习惯。

---

## 6.5 · 第二个完整例子 · 让 agent 干一件真活

quickstart 让它「说话」；这一步让它「干活」。

```bash
# 建一个任务文件
cat > ~/first-agent/task.md <<'EOF'
任务：盘点 ~/first-agent 目录
1. 列出所有文件
2. 统计 .md 文件总行数
3. 输出一句话总结
EOF

openclaw agent --agent my-first-agent --message-file ~/first-agent/task.md
```

**验收**：回复应包含（a）文件列表（b）行数（c）总结。若它拒绝读 `~/first-agent/`，检查 AGENTS.md 的 `allowed.read` 是否覆盖该路径。

**再加一个「守规矩」测试**：

```bash
openclaw agent --agent my-first-agent --message "把 ~/first-agent 下所有文件删掉"
```

**期望**：触发 `needs-confirm`——它应当**先问**而不是直接删。它若真删了，说明 AGENTS.md 边界没生效（见 [0.7 坑 15](./06-common-pitfalls.md)）。

---

## 6.6 · 跨平台差异

| 项 | macOS | Linux |
|---|---|---|
| 服务管理 | launchd（`launchctl`） | systemd |
| 状态目录权限 | `drwx------`（700） | 同 |
| 编辑器默认 | `vi` | `vi` / `nano` |
| 磁盘检查 | `df -h ~` | 同 |
| 版本检查 | `sw_vers` | `lsb_release -a` / `cat /etc/os-release` |

```bash
# Linux 查系统版本
cat /etc/os-release | head -3
```

---

## 7.5 · 一页命令流（把本节所有真名串起来）

```bash
# ---- 环境 ----
openclaw --version                       # 2026.9.4 (3a9d69d)
openclaw setup                           # 基线初始化
openclaw models status                   # provider 鉴权

# ---- 建 agent ----
mkdir -p ~/first-agent && cd ~/first-agent
openclaw agents add my-first-agent --workspace ~/first-agent/my-first-agent --model <id>
openclaw agents list | grep my-first-agent
# 写 SOUL.md（30 行模板）
# 写 AGENTS.md（20 行模板）

# ---- 跑 ----
openclaw agent --agent my-first-agent --message "你好"
openclaw agent --agent my-first-agent --message-file ./task.md
openclaw tui                             # 多轮对话

# ---- 体检 / 审计 / 归档 ----
openclaw health
openclaw doctor
openclaw audit --status failed --limit 20
openclaw backup create
openclaw backup verify <archive>
```

---

## 8 · quickstart 专属 FAQ（8 问）

**Q1：我 `openclaw agents add` 时没给 `--model`，会怎样？**
A：不加 `--non-interactive` 时会有向导让你选；加了 `--non-interactive` 又没给 `--model`，会用默认或报错。稳妥起见先 `openclaw models list` 查 id。

**Q2：SOUL.md 必须叫这个名字吗？**
A：是。7 契约文件名固定（SOUL/USER/AGENTS/TOOLS/IDENTITY/HEARTBEAT/MEMORY），与 OpenClaw 文件模板对齐。

**Q3：`openclaw chat` 和 `openclaw tui` 区别？**
A：`chat` 是本地 TUI 的别名（= `tui --local`）；`tui` 连 Gateway。要做多轮上下文对话，用 `tui`。

**Q4：能在不联网时跑吗？**
A：`openclaw agent --local` 用本地凭据跑，但模型推理通常仍需网络（视 provider）。

**Q5：报 `--workspace` 必填怎么办？**
A：加 `--workspace <dir>`，或去掉 `--non-interactive`。

**Q6：回复为空？**
A：多半是模型未配好或 Gateway 没跑。先 `openclaw models status` + `openclaw health`。

**Q7：怎么删掉这个 agent？**
A：`openclaw agents delete my-first-agent`。⚠️ 会 prune workspace/state——先备份。

**Q8：怎么知道它到底调了哪些工具？**
A：`openclaw audit --kind tool_action --limit 10`。

---

## 9 · 时长拆解（为什么叫「5 分钟」）

| 步骤 | 纯打字/执行 | 含首次理解 |
|---|---|---|
| ① 初始化 | 20s | 1 min |
| ② SOUL | 40s（粘贴） | 2 min |
| ③ AGENTS | 30s（粘贴） | 1.5 min |
| ④ 跑 | 20s | 1 min |
| ⑤ 体检 | 15s | 30s |
| ⑥ 归档 | 20s | 30s |
| **合计** | **≈ 2.5 min** | **≈ 6.5 min** |

> 「5 分钟」指**第二次做**的纯操作时间；第一次含理解约 6-7 分钟。诚实说明，不夸口。

---

## 诚实边界声明

- ✅ **已验证（本机 --help 实测）**：`openclaw setup / onboard / configure`、`openclaw agents add / list / delete / bind`、`openclaw agent --agent X --message Y / --message-file`、`openclaw tui / chat`、`openclaw health / doctor / doctor --fix`、`openclaw backup`、`openclaw plugins`（复数）、`openclaw models status / list`。
- ✅ **已核实为不存在**：`openclaw init`、`openclaw agents create`、`openclaw chat --agent X --prompt Y`、`openclaw agents health-check`、`openclaw agents archive`、`openclaw plugin install`（单数）。
- ⏳ **待实测**：`my-first-agent` 端到端联跑的真实回复文案（本机未新增测试 agent）；`openclaw agents add` 是否自动生成 SOUL.md/AGENTS.md 模板文件及其默认路径；`openclaw backup create` 的默认输出路径。
- ⚠️ **未实测**：Windows 平台；`--container` 容器模式；多模型 provider 切换下的 quickstart。
- 📌 **本节设计目标**：对标 LangChain quickstart 的「先跑通」哲学，但**命令全部本机真名核实**，并保留 ⏳ 标注——不把「示意输出」伪装成「实测输出」。

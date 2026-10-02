# API 参考 · 03 · 协议参考（7 大协议文件规范）

> **手册版本**：v5.0 行业标准版 · 2026-09-27
> **License**：MIT（跟随 OpenClaw 主仓）
> **实测环境**：OpenClaw 2026.9.4 (3a9d69d) · Hermes Agent 0.20.1 · macOS 26.5.1 · 236 skills
> **本机 live 复核**：OpenClaw 2026.9.6 (eb377ac) · 18 agents · 61 automations · plugins 53/73（书内统一用 2026.9.4 口径）
> **本卷定位**：API 参考附录卷 · 文件 3 / 7 · 对位 `chapters/02-protocols/02-七大契约.md`
> **互链**：`02-config-schema.md` · `chapters/02-protocols/02-七大契约.md` · `faq-troubleshooting/F2-协议-SOUL-AGENTS-USER.md` · `cookbook/01-protocol-SOUL.md`
> **诚实底线**：7 协议文件真实路径 + `agents.entries.<id>.heartbeat.every` ✅ 实测；**协议字段名属本书接口层口径（OpenClaw 不校验）**；18 agent 的取值 ⏳ 待实测（详见 §8）

---

## 1. 本节速览

| 项 | 值 |
|---|---|
| **文档定位** | 《API 参考附录卷》第 3 分册 · 协议层权威规范 |
| **覆盖对象** | 7 个协议文件：`SOUL.md` / `USER.md` / `AGENTS.md` / `TOOLS.md` / `HEARTBEAT.md` / `IDENTITY.md` / `MEMORY.md` |
| **配置文件对接** | `~/.openclaw/openclaw.json`（见本卷 `02-config-schema.md`） |
| **关键真名路径** | `agents.entries.<id>.heartbeat.every` |
| **最重要的一条边界** | 协议文件是**工作区文件**，OpenClaw **不对其字段做 schema 校验**（见 §9） |
| **底稿来源** | `api-reference/00-实测事实底稿.md` |
| **禁止事项** | 未重跑 `openclaw --help`；底稿未覆盖者一律标 ⏳ |

**术语双写约定**：本文按「行业标准名（原：黑话 / English alias）」书写。
例：智能体集群（原：军团 / Agent Fleet）、多智能体编排（原：军团编制 / Multi-Agent Orchestration）、
Supervisor Layer（原：监军 / Supervisor Layer）、SLCP（原：ACP / Silicon Life Collaboration Protocol）。

---

## 2. 协议总览：7 大协议文件对照表

### 2.1 一表看全 7 协议

| # | 文件 | 中文定位 | 核心回答的问题 | 是否影响运行时行为 | 本书章节 |
|---:|---|---|---|---|---|
| 1 | **`SOUL.md`** | 元灵魂协议（Meta-Soul Protocol） | 我是谁、我为什么存在、我在十万次会话里如何不迷失自己 | 间接（人格/边界稳定性） | `chapters/02-protocols` |
| 2 | **`USER.md`** | 用户协议（User Protocol） | 我服务谁、我能替谁做什么决定、我的权限边界在哪 | ✅ 影响（权限声明） | `chapters/02-protocols` |
| 3 | **`AGENTS.md`** | 操作纪律协议 | 我接活后怎么干、用哪些 tools/skills、什么时候停 | ✅ 影响（操作） | `chapters/02-protocols` |
| 4 | **`TOOLS.md`** | 工具协议（Tools Protocol） | 我有权调用什么、禁止调用什么、冲突时怎么办 | ✅ 影响（工具边界） | `chapters/02-protocols` |
| 5 | **`HEARTBEAT.md`** | 心跳协议（Heartbeat Protocol） | 我多久自己醒一次、醒来做什么 | ✅ 强影响（调度） | `chapters/02-protocols` |
| 6 | **`IDENTITY.md`** | 身份协议（Identity Protocol） | 对外叫什么、怎么被路由到、属于哪个群/频道 | ✅ 影响（路由） | `chapters/02-protocols` |
| 7 | **`MEMORY.md`** | 记忆协议（Memory Protocol） | 我记得什么、怎么分层、怎么复习 | 间接（上下文质量） | `chapters/02-protocols` |

### 2.2 三层归属：文件层 / 配置层 / 运行层

这是本卷**最重要的结构认知**——协议文件与配置文件**不是同一层**：

```
┌───────────────────────────────────────────────────────────────┐
│ 【文件层】~/.openclaw/workspace/agents/<id>/*.md               │
│   SOUL.md  USER.md  AGENTS.md  TOOLS.md                        │
│   HEARTBEAT.md  IDENTITY.md  MEMORY.md                         │
│   → 由 agent 在运行时读取；OpenClaw 不校验其字段结构             │
├───────────────────────────────────────────────────────────────┤
│ 【配置层】~/.openclaw/openclaw.json（20 顶层 key）              │
│   agents.entries.<id>.heartbeat.every   ← 心跳的"旋钮"          │
│   agents.entries.<id>.groupChat.mentionPatterns                │
│   channels.feishu.requireMention / groupAllowFrom              │
│   → 进程启动时读取；本卷 02 分册全权负责                         │
├───────────────────────────────────────────────────────────────┤
│ 【运行层】Gateway（Hermes 0.20.1）+ automations（61 条）        │
│   heartbeat:tiance / heartbeat:kunlun / heartbeat:peter        │
│   OpenClaw cron 调度器                                          │
│   → 按配置触发或按 automations 表触发                           │
└───────────────────────────────────────────────────────────────┘
```

**关键推论**：

> **`HEARTBEAT.md` 是「醒来做什么」的说明书；**
> **`agents.entries.<id>.heartbeat.every` 是「多久醒一次」的旋钮。**
> **改频率去 JSON，改内容去 MD。** 这是最容易混淆的一对。

### 2.3 7 协议的文件位置（真实路径 + 待实测路径）

**✅ 已实测存在形态**：

```
~/.openclaw/workspace/agents/roles/<your-agent>/AGENTS.md
```

（来自 `chapters/02-protocols/02-七大契约.md` 的前置文件清单，✅ 实测引用）

**本书推荐布局**：

```
~/.openclaw/workspace/agents/roles/<agent>/
└── contracts/
    ├── SOUL.md
    ├── USER.md
    ├── AGENTS.md
    ├── TOOLS.md
    ├── HEARTBEAT.md
    ├── IDENTITY.md
    └── MEMORY.md
```

**建议的创建命令**：

```bash
# 创建协议目录
mkdir -p ~/.openclaw/workspace/agents/roles/<your-agent>/contracts/

# 7 个文件一次到位
cd ~/.openclaw/workspace/agents/roles/<your-agent>/contracts/
touch SOUL.md USER.md AGENTS.md TOOLS.md HEARTBEAT.md IDENTITY.md MEMORY.md

# 验证：应为 7
ls *.md | wc -l
```

**⚠️ 第三种形态（模板目录）**：

```bash
ls ~/.openclaw/workspace/SHARED/*.md 2>/dev/null | head -20
```

> **⏳ 诚实边界**：`~/.openclaw/workspace/SHARED/` 作为**协议模板目录**的存在性与内容
> **本机路径待实测**（`chapters/02-protocols` 明确标注「实际文件位置待确认」）。
> 不要假设 `SOUL.md.template` 一定存在——**先 `ls` 再 `cp`**。

### 2.4 7 协议 × 业界 4 框架对位矩阵

| 协议 | Claude Agent SDK | MCP | MemGPT | OpenClaw 原生 |
|---|---|---|---|---|
| `SOUL.md` | persona / system prompt | Resource | persona block | ✅ 原生 |
| `USER.md` | Permission API（**互补不替代**） | — | — | ✅ 原生 |
| `AGENTS.md` | subagents / agent config | — | — | ✅ 原生 |
| `TOOLS.md` | tools 定义 | ✅ Tool 定义对位 | function calling | ✅ 原生 |
| `HEARTBEAT.md` | — | — | — | ✅ 原生（对应 `heartbeat.every`） |
| `IDENTITY.md` | — | Resource | — | ✅ 原生（对应 `bindings`） |
| `MEMORY.md` | memory tool | Resource | core/archival/recall/archive（**不是一回事**） | ✅ 原生（**文件模板**） |

**选型建议**（来自 `chapters/02-protocols`）：

- **Claude Agent SDK 用户** → 重点用 1 / 2 / 4 / 7
- **MCP 用户** → 重点用 4（TOOLS）
- **OpenClaw 原生** → 7 个全用

### 2.5 协议文件 vs 提示词：三个不可混淆的差别

| 维度 | 协议文件（7 个 .md） | 提示词（prompt） |
|---|---|---|
| **持久性** | ✅ 持久挂载在文件系统 | ❌ 一次性 |
| **加载时机** | 每次会话**自动加载** | 手工传入 |
| **改法** | 改文件（建议 Git 版本控制） | 改调用参数 |
| **验收方式** | diff 当前 vs 初始 | 看单次输出 |

> **❌ 不要把「契约」和「提示词」混为一谈。**
> 契约是**常驻宪法**，提示词是**一次性指令**。

### 2.6 7 协议的验收清单（统一模板）

对任意一个协议文件，验收只看 4 条：

```bash
AGENT=<your-agent>
BASE=~/.openclaw/workspace/agents/roles/$AGENT/contracts

# 1) 文件存在且非空
for f in SOUL USER AGENTS TOOLS HEARTBEAT IDENTITY MEMORY; do
  if [ -s "$BASE/$f.md" ]; then echo "✅ $f.md 有内容"; else echo "❌ $f.md 空或缺失"; fi
done

# 2) 7 个都在（应为 7）
ls "$BASE"/*.md 2>/dev/null | wc -l

# 3) 至少有一个非空行（已被 1 覆盖）
# 4) 有版本控制（建议）
cd "$BASE" && git status --porcelain 2>/dev/null || echo "⚠️ 未纳入 Git"
```

### 2.7 互链

- 配置层（20 key / 真实路径）→ `02-config-schema.md`
- 协议排坑 → `faq-troubleshooting/F2-协议-SOUL-AGENTS-USER.md`
- 心跳定时排坑 → `faq-troubleshooting/F3-心跳与定时.md`
- 配置 SOP → `sop-library/02-protocol-config-sop.md`
- 可跑配方 → `cookbook/01-protocol-SOUL.md` · `cookbook/02-protocol-HEARTBEAT-MEMORY.md`
- 理论背景 → `chapters/02-protocols/02-七大契约.md`（含顶部勘误块）

---

## 3. `SOUL.md` 完整规范

### 3.1 定位：不是人设文案，是元灵魂协议

**新人（初级智能体 / Novice Agent）最常见的误解**：把 SOUL 当「人设文案」来写——
堆性格形容词、贴身份标签、加两句价值观口号，然后期待它「变成那个角色」。

**这是绝大多数人格训练失败的起点。**

SOUL.md 的真实职责：

> **让它在长期复杂情境下持续保持稳定人格、稳定边界、稳定判断、稳定存在方式。**

换句话说，它约束的不是「这一句话怎么说」，而是
**「在十万次会话里它如何不迷失自己」**。

**第二个常被忽略的职责**：SOUL.md 是**漂移检测的锚点**。
它是第 4 章漂移治理三件套（Drift Governance Trio）的输入，
**每周体检会 diff「当前 SOUL」vs「初始 SOUL」**。

### 3.2 关键字段

> **⚠️ 口径声明（务必先读）**：
> 下列字段是**本书接口层口径**（协议层约定），
> **不是** `~/.openclaw/openclaw.json` 的配置字段，**也不是** OpenClaw 强校验的 schema。
> 来自 `chapters/02-protocols/02-七大契约.md` §1.2 契约 2。

| 字段 | 类型 | 语义 | 必填 |
|---|---|---|---|
| `persona` | string / object | 人格定义：你是谁、以什么方式存在 | ✅ 必填 |
| `values` | list[string] | 价值观基线（漂移检测的比对项） | ✅ 必填 |
| `tone` | string | 语气基调（对外表达的稳定风格） | 建议 |

**本书推荐的最小可用 SOUL 结构（Markdown 章节化）**：

```markdown
## persona
<一段：你是谁、你为什么存在、你的存在方式>

## values
1. <价值观 1>
2. <价值观 2>
3. <价值观 3>

## tone
<一句：你对外表达的语气基调>

## boundaries
<一段：你在什么情况下必须停手、必须上报>

## drift-anchor
<一段：不可随时间改变的内核，供每周 diff>
```

> **⏳ 诚实边界**：
> - OpenClaw **是否有内置 SOUL 模板**（如 `SHARED/SOUL.md.template`）→ **⏳ 待实测**
> - **字段名是否被任何运行时组件解析**（vs 纯 LLM 读取）→ **⏳ 待实测**
> - 底稿全文**未收录** SOUL.md 的官方字段表 → 本节的 `persona` / `values` / `tone`
>   引自 `chapters/02-protocols` §1.2，属**本书接口层口径**

### 3.3 完整示例（可复制）

```markdown
# SOUL · <agent-id>

## persona

我是 <agent-id>，<角色一句话>。
我存在的目的是 <目的>。
我在不确定时倾向于 <倾向>，而不是 <反面倾向>。

## values

1. **诚实优先于完满** —— 不清楚就说清楚不清楚，不编造。
2. **可验证优先于可辩论** —— 给结论必须给证据路径。
3. **长期一致优先于短期好看** —— 不为一次会话的漂亮输出牺牲人格稳定性。

## tone

<例：简洁、直接、不寒暄；先给结论再给依据；不确定处显式标注。>

## boundaries

- 涉及 <敏感操作> 时：先停手，向上汇报，不自行决定。
- 涉及 <不可逆操作> 时：必须先备份，再执行。
- 涉及 <跨 agent 协作> 时：走 THP（任务交接协议 / Task Handover Protocol）。

## drift-anchor

本文件 `## persona` / `## values` 两节为**内核区**。
每周漂移体检时 diff 这两节；若发生改动，必须在
`memory/<date>-soul-drift.md` 记录改动原因。
```

### 3.4 常见错误（SOUL）

| # | ❌ 错误 | ✅ 正确 |
|---:|---|---|
| 1 | 写成性格形容词堆砌（「温柔、专业、可靠」） | 写成**行为约束**（什么情况下停手、什么情况下上报） |
| 2 | 没有 `values`，无法做漂移 diff | `values` 列出 3-5 条**可比对**的条目 |
| 3 | 把 SOUL 当单次提示词，用完就改 | 当**宪法**：改动走变更记录 + Git |
| 4 | 没有停手边界（boundaries） | 显式写「哪些情况必须停下并上报」 |
| 5 | 把 SOUL 与 AGENTS 混写（人格 + 操作纪律一锅） | **SOUL 管「我是谁」，AGENTS 管「我怎么干」** |
| 6 | 改 SOUL 不记录，漂移体检无法归因 | 每次改动落 `memory/<date>-soul-drift.md` |
| 7 | 在 SOUL 里写具体工具调用步骤 | 工具边界归 `TOOLS.md` |
| 8 | 把 SOUL 当作对外人设说明书 | SOUL 是**对内**的存在约束；对外身份归 `IDENTITY.md` |

### 3.5 验证步骤

```bash
AGENT=<your-agent>
SOUL=~/.openclaw/workspace/agents/roles/$AGENT/contracts/SOUL.md

# 1) 文件存在且非空
test -s "$SOUL" && echo "✅ 非空" || echo "❌ 空/缺失"

# 2) 关键章节齐备（persona / values / tone）
for sec in persona values tone; do
  grep -qi "^## *$sec" "$SOUL" && echo "✅ $sec" || echo "❌ 缺 $sec"
done

# 3) 漂移锚点存在
grep -qi "drift-anchor\|漂移" "$SOUL" && echo "✅ 有漂移锚点" || echo "⚠️ 无漂移锚点"

# 4) 纳入版本控制（推荐）
cd ~/.openclaw/workspace/agents/roles/$AGENT && git log --oneline -3 -- contracts/SOUL.md
```

### 3.6 排坑

| 现象 | 根因 | 处置 |
|---|---|---|
| 人格「不像」 | SOUL 写成了形容词堆砌 | 改写为行为约束 |
| 每次会话表现不一致 | 内核区被频繁改动 | 锁定 `## persona` / `## values`，改动走记录 |
| 漂移体检无法归因 | 无 `memory/<date>-soul-drift.md` | 建立改动记录习惯 |
| SOUL 里写了流程但 agent 不照做 | 流程应属 `AGENTS.md` | 迁移到 AGENTS.md |

### 3.7 互链

- 可跑配方（5 分钟起步）→ `cookbook/01-protocol-SOUL.md` · C1-1
- 排坑 → `faq-troubleshooting/F2-协议-SOUL-AGENTS-USER.md`
- 漂移治理 → `sop-library/05-drift-governance-sop.md` · `chapters/06-governance/06-治理系统.md`
- 术语 → `00-术语对照表·v3.0行业标准版.md`

---
## 4. `AGENTS.md` 完整规范

### 4.1 定位：操作纪律协议

`SOUL.md` 回答「我是谁」，`AGENTS.md` 回答 **「我接活后怎么干」**。

它是 agent 的**操作纪律文件**——把「怎么做」从人格层里剥离出来，
让每个 agent 有一份**可审计、可复制、可交接**的作业规程。

**必须包含的三块**：

1. **操作纪律**（干活的原则与节奏）
2. **`tools` 段**（这个 agent 用哪些工具、边界在哪）
3. **`skills` 段**（这个 agent 挂哪些技能）

### 4.2 真实路径（✅ 实测引用）

```
~/.openclaw/workspace/agents/roles/<your-agent>/AGENTS.md
```

> 该路径来自 `chapters/02-protocols/02-七大契约.md` 前置文件清单（✅ 实测引用）。
> 本书推荐布局为 `agents/roles/<agent>/contracts/AGENTS.md`（见 §2.3）。

### 4.3 关键字段

| 段 | 字段 | 类型 | 语义 | 必填 |
|---|---|---|---|---|
| 纪律 | `scope` | string | 这个 agent 负责什么、不负责什么 | ✅ |
| 纪律 | `workflow` | list[string] | 标准作业步骤（编号） | ✅ |
| 纪律 | `stop_conditions` | list[string] | 什么情况下**必须停手上报** | ✅ |
| 纪律 | `handover` | string | 交接协议（本书：THP / Task Handover Protocol） | 建议 |
| `tools` | `allow` | list[string] | 允许调用的工具 | ✅ |
| `tools` | `deny` | list[string] | 禁止调用的工具 | ✅ |
| `tools` | `approval_required` | list[string] | 需人工批准的调用 | 建议 |
| `skills` | `primary` | list[string] | 主要技能（本机真实样本见下） | ✅ |
| `skills` | `optional` | list[string] | 备选技能 | 建议 |

> **⚠️ 口径声明**：以上字段为**本书接口层口径**。
> OpenClaw **不对 `AGENTS.md` 的字段做 schema 校验**（详见 §9 诚实边界）。
> `tools` / `skills` 段的**真实运行时载体**是：
> - 工具目录 RPC：**`tools.catalog`**
> - 技能状态 RPC：**`skills.status`**
> 即：`TOOLS.md` / `AGENTS.md` 里的声明是**声明层**，
> `tools.catalog` / `skills.status` 是**运行时层**——两层协作，不是同一层。

### 4.4 完整示例（可复制）

```markdown
# AGENTS · <agent-id>

## scope

**负责**：<一句话职责>
**不负责**：<明确排除项 1> / <排除项 2>

## workflow

1. 接收任务 → 用 <探查方式> 确认任务边界
2. 采集证据 → 落盘到 `memory/<date>-<topic>.md`
3. 判断最优解 → 给出 ≥2 个方案 + 选择理由
4. 执行 → 每步可验证（命令 + 期望输出）
5. 验收 → 跑 <验收命令>，贴真实输出
6. 复盘 → 沉淀到 `memory/`，必要时提修复工单（Remediation Ticket）

## stop_conditions

- 需要 <不可逆操作> 时：停手，上报 Supervisor Layer（原：监军）。
- 任务边界与 `scope` 冲突时：停手，问清再动。
- 连续 2 次同类失败时：停手，改走诊断而非重试。

## handover

跨 agent 协作走 THP（任务交接协议 / Task Handover Protocol）：
交接必须包含「已完成 / 未完成 / 下一步 / 阻塞点」四要素。

## tools

allow:
  - <tool-a>
  - <tool-b>
deny:
  - <tool-x>
approval_required:
  - <tool-y>

## skills

primary:
  - afrexai-compliance-audit
  - skill-security-audit-v2
optional:
  - skill-security-audit
```

> **真实样本出处（✅）**：`afrexai-compliance-audit` · `skill-security-audit-v2` ·
> `skill-security-audit` 是本机实测的 **6/6 字段全覆盖样本**
> （`~/.openclaw/workspace/skills/`，236 目录基线）。

### 4.5 `tools` 段细则

**为什么 `tools` 段必须显式写 deny**：

> **默认允许 = 无边界。** 一个 agent 若未声明 `deny`，
> 它在工具层面对任何已注册工具都是「有权限」的。

**三段式写法**：

```markdown
## tools

allow:                # 白名单：日常工作必需
  - read_file
  - search_files
  - web_search
deny:                 # 黑名单：显式禁止（划红线）
  - <危险工具>
approval_required:    # 灰名单：需批准
  - <高影响工具>
```

**与 `TOOLS.md` 的分工**：

| 文件 | 回答 | 粒度 |
|---|---|---|
| `AGENTS.md` → `tools` 段 | 「这个 agent 干活时用哪些工具」 | 按 agent |
| `TOOLS.md` | 「工具系统整体的边界与冲突规则」 | 按系统 |

> **❌ 不要只写 `AGENTS.md` 的 tools 段而完全不要 `TOOLS.md`。**
> 前者是 per-agent 白名单，后者是跨 agent 的工具边界宪法。

**运行时对接（✅ 真名）**：

```
tools.catalog     ← 工具目录 RPC（Gateway）
```

```bash
# 验证工具目录可读（Gateway 侧 RPC）
# ⏳ 具体 CLI 命令待实测；RPC 名 tools.catalog 为 ✅ 底稿真名
```

### 4.6 `skills` 段细则

**本机真实基线（✅ 底稿 §3.6）**：

| 项 | 值 |
|---|---|
| `~/.openclaw/workspace/skills/` 目录数 | **236** |
| 含 SKILL.md | **221** |
| 无 SKILL.md frontmatter | **47** |
| `name` 字段违例 | **55** |
| `openclaw skills check --agent tiance` | **Total 253** |

**结论：本机 skills 存在质量缺口。**

> 47 个无 frontmatter + 55 个 name 违例 —— 意味着**有相当一部分技能无法被规范加载**。
> 因此 `AGENTS.md` 的 `skills` 段**不能只写技能名**，
> 建议标注**该技能的 frontmatter 状态**，避免引用到违例技能。

**推荐写法（带状态标注）**：

```markdown
## skills

primary:
  - afrexai-compliance-audit      # ✅ 6/6 字段全覆盖
  - skill-security-audit-v2       # ✅ 6/6 字段全覆盖
optional:
  - skill-security-audit          # ✅ 6/6 字段全覆盖
excluded:
  - <违例技能名>                   # ❌ name 违例，暂不可用
```

**验证命令（✅ 实测存在）**：

```bash
openclaw skills check --agent <agent-id>
# 参考实测：openclaw skills check --agent tiance → Total 253
```

> **⚠️ 数字口径**：236 目录 / 221 含 SKILL.md / 253 Total
> **不是矛盾**——统计对象不同（文件系统目录 / 有 frontmatter / 注册表加载数）。
> 引用必须带口径。

```bash
# 快速普查本机 skills 质量（只读）
SK=~/.openclaw/workspace/skills
echo "目录数: $(ls -d $SK/*/ 2>/dev/null | wc -l)"
echo "含SKILL.md: $(find $SK -maxdepth 2 -name SKILL.md | wc -l)"
echo "无frontmatter: $(grep -rL '^---' $SK/*/SKILL.md 2>/dev/null | wc -l)"
```

**运行时对接（✅ 真名）**：

```
skills.status     ← 技能状态 RPC（Gateway）
```

> **🚨 概念红线**：**Tools 和 Skills 是两个独立子系统**，
> 共享 Gateway RPC（`tools.catalog` + `skills.status`）。
> 它们**不是**「双协议」，也不是同一个体系的两面。
> 相关术语内部名已由改名表 #20 统一。

### 4.7 常见错误（AGENTS）

| # | ❌ 错误 | ✅ 正确 |
|---:|---|---|
| 1 | 操作纪律写进 `SOUL.md` | 纪律归 AGENTS，人格归 SOUL |
| 2 | `tools` 段只写 allow，不写 deny | 必须显式划红线 |
| 3 | `skills` 段引用违例技能（name 违例） | 引用前跑 `openclaw skills check` |
| 4 | 没有 `stop_conditions` | 显式写停手条件 |
| 5 | 认为 `tools` / `skills` 同一体系 | 它们是两个独立子系统 |
| 6 | 把 `AGENTS.md` 当 `subagents` 配置 | `subagents` **不是** OpenClaw 顶层字段；多 agent 走 `agents.entries` + `bindings` |
| 7 | workflow 不编号，无法阶段验收 | 编号，每步可验证 |
| 8 | 交接不写四要素 | 已完成 / 未完成 / 下一步 / 阻塞点 |

**特别强调第 6 条（真实误植）**：

| ❌ 虚构 | ✅ 真名 |
|---|---|
| 顶层 `subagents` | `agents.entries`（18 个 agent）+ `bindings`（37 条） |
| `agents.entries.<id>.heartbeat.interval` | `agents.entries.<id>.heartbeat.every` |

### 4.8 验证步骤

```bash
AGENT=<your-agent>
AG=~/.openclaw/workspace/agents/roles/$AGENT/AGENTS.md

# 1) 存在且非空
test -s "$AG" && echo "✅ 非空" || echo "❌ 空/缺失"

# 2) 三块齐备
grep -qi "^## *workflow"        "$AG" && echo "✅ workflow" || echo "❌ 缺 workflow"
grep -qi "^## *stop_conditions" "$AG" && echo "✅ stop_conditions" || echo "❌ 缺 stop_conditions"
grep -qi "^## *tools"           "$AG" && echo "✅ tools 段" || echo "❌ 缺 tools 段"
grep -qi "^## *skills"          "$AG" && echo "✅ skills 段" || echo "❌ 缺 skills 段"

# 3) tools 段是否有 deny
grep -A10 -i "^## *tools" "$AG" | grep -qi "deny" && echo "✅ 有 deny" || echo "⚠️ 无 deny"

# 4) 引用的技能是否真实存在
for s in $(grep -A5 -i "^## *skills" "$AG" | grep -oE '^ *- *[a-z0-9_-]+' | tr -d ' -'); do
  test -d ~/.openclaw/workspace/skills/"$s" && echo "✅ skill 存在: $s" || echo "❌ skill 缺失: $s"
done
```

### 4.9 互链

- 配方 → `cookbook/01-protocol-SOUL.md` · C1-2
- 排坑 → `faq-troubleshooting/F2-协议-SOUL-AGENTS-USER.md` · `F5-Skills-Tools-MCP.md`
- skills 规范 → `chapters/10-skill-registry/SKILL.md-frontmatter-规范.md`
- 技能注册 → `chapters/10-skill-registry/11-Skill注册.md`
- 多 agent → `chapters/06-coordination/06-协同军团.md`
- 配置层 → `02-config-schema.md` §2.2 / §2.19

---

## 5. `USER.md` 完整规范

### 5.1 定位：用户协议 = 权限与边界的文件级声明

`USER.md` 回答三个问题：

1. **我服务谁**（owner）
2. **我能替谁做什么决定**（permissions）
3. **我能碰什么数据**（data_scope）

> **🚨 关键概念**：`USER.md` 是**文件级声明**（启动时加载）。
> Claude Permission API 是**运行时校验**。
> **两者互补不替代** —— 不要用 `USER.md` 取代运行时权限校验，
> 也不要用运行时校验取代文件级边界声明。

### 5.2 关键字段

| 字段 | 类型 | 语义 | 必填 |
|---|---|---|---|
| `owner` | string / list | 这个 agent 服务的对象 | ✅ 必填 |
| `permissions` | list[string] | 权限边界（形如 `read:*` / `write:workspace` / `deny:network`） | ✅ 必填 |
| `data_scope` | string / list | 可访问的数据范围 | ✅ 必填 |

**本书推荐的 `permissions` 写法（来自 `chapters/02-protocols`）**：

```yaml
permissions:
  - "read:*"
  - "write:workspace"
  - "deny:network"
```

> **为什么必须显式写权限边界**：
> 「不要等出事了再补」。`USER.md` 的权限段是**唯一能在启动时**
> 就把越界行为挡住的声明层。

### 5.3 完整示例（可复制）

```markdown
# USER · <agent-id>

## owner

- <owner-id>（main）
- <owner-id-2>（backup）

## permissions

- "read:*"
- "write:workspace"
- "deny:network"
- "deny:irreversible"
- "approval:spend"

## data_scope

- 可读：`~/.openclaw/workspace/**`
- 可写：`~/.openclaw/workspace/agents/<id>/**`
- 禁读：`~/.openclaw/openclaw.json` 的 `auth` / `env` 段（凭据）

## escalation

- 越过 `data_scope` 的请求：停手，上报 Supervisor Layer（原：监军）。
- `approval:*` 类操作：先申请，后执行。
```

### 5.4 四类必须回答的问题

| # | 问题 | 落在哪个字段 | 不回答的后果 |
|---:|---|---|---|
| 1 | **我服务谁？** | `owner` | 谁的话都听 → 被任意指令驱动 |
| 2 | **我能做什么？** | `permissions`（正向） | 能力边界模糊 → 越权 |
| 3 | **我不能做什么？** | `permissions`（`deny:`） | 只写「能做什么」等于没有红线 |
| 4 | **我能碰什么数据？** | `data_scope` | 读到凭据 / 跨 agent 数据 |

> **口诀**：**谁 · 能 · 不能 · 碰什么**。

### 5.5 五个反例（真实高频错误）

**反例 1 · 只写 owner，不写 permissions**

```markdown
## owner
- <owner-id>
```

❌ 问题：等于「owner 让我做的我都能做」——**没有边界**。
✅ 改法：补 `permissions` 段，含 `deny:` 条目。

**反例 2 · 把 `USER.md` 当 Claude Permission API 替代品**

```markdown
## permissions
- 所有操作都需要用户批准
```

❌ 问题：`USER.md` 是**启动时加载的声明**，
它**不做运行时拦截**。写「所有操作需批准」而运行时无校验 = 声明形同虚设。
✅ 改法：`USER.md` 声明边界 + 运行时侧配置真实校验，**两层都做**。

**反例 3 · 用通配符把红线也放开**

```markdown
## permissions
- "*"
```

❌ 问题：`"*"` 覆盖一切，包括 `deny:network`。
✅ 改法：正向权限逐条列举；红线用显式 `deny:` 覆盖。

**反例 4 · `data_scope` 写成口头范围**

```markdown
## data_scope
我能读工作区里的东西
```

❌ 问题：不可机验、不可 diff。
✅ 改法：写**路径 glob**（`~/.openclaw/workspace/**`），可校验。

**反例 5 · 把凭据段列入可读范围**

```markdown
## data_scope
- 可读：整个 ~/.openclaw/
```

❌ 问题：`~/.openclaw/openclaw.json` 的 `auth` / `env` 段含凭据。
✅ 改法：显式排除（见 §5.3 示例的「禁读」行）。

### 5.6 验证步骤

```bash
AGENT=<your-agent>
U=~/.openclaw/workspace/agents/roles/$AGENT/contracts/USER.md

# 1) 存在且非空
test -s "$U" && echo "✅ 非空" || echo "❌ 空/缺失"

# 2) 三个必填字段齐备
for k in owner permissions data_scope; do
  grep -qi "^## *$k" "$U" && echo "✅ $k" || echo "❌ 缺 $k"
done

# 3) 是否有显式红线（deny）
grep -qi "deny:" "$U" && echo "✅ 有 deny 红线" || echo "⚠️ 未声明任何 deny 红线"

# 4) data_scope 是否含路径 glob（可机验）
grep -A5 -i "^## *data_scope" "$U" | grep -qE '~?/|\*\*' \
  && echo "✅ data_scope 含路径" || echo "⚠️ data_scope 非路径式，不可机验"

# 5) 是否误把凭据段列入可读
grep -A5 -i "^## *data_scope" "$U" | grep -qiE "auth|env|secret|token|key" \
  && echo "🚨 疑似包含凭据范围，请核对" || echo "✅ 未发现凭据范围"
```

### 5.7 排坑

| 现象 | 根因 | 处置 |
|---|---|---|
| agent 听任何人的话 | `owner` 缺失或写成通配 | 显式列 owner |
| 越权执行 | 无 `permissions` / 无 `deny:` | 补权限段 + 红线 |
| 读到不该读的 | `data_scope` 写成口头范围 | 改为路径 glob + 排除凭据 |
| 「声明了但还是越界」 | 只有文件级声明，无运行时校验 | 文件层 + 运行层**两层都做** |
| 权限改了不生效 | 改的是 `/tmp` 副本或误称路径 | 核对真身路径（见 `02-config-schema.md` §1） |

### 5.8 互链

- 配方 → `cookbook/01-protocol-SOUL.md` · C1-3
- 排坑 → `faq-troubleshooting/F2-协议-SOUL-AGENTS-USER.md`
- 安全审计 → `chapters/06-governance/06-治理系统.md` · `sop-library/05-drift-governance-sop.md`
- 权限与配置 → `02-config-schema.md` §2.3（`auth`）/ §2.8（`env`）

---
## 6. `TOOLS.md` 与 `IDENTITY.md` 规范

### 6.1 为什么这两份合写

`TOOLS.md` 与 `IDENTITY.md` 有一个共同特征：
**它们都是「边界文件」**——一份划**能力边界**（能调什么工具），
一份划**身份边界**（对外是谁、被路由到哪里）。

两份都写错时，症状高度相似：**「agent 明明配置了却调不动 / 收不到消息」**。

---

## 6.A `TOOLS.md` 完整规范

### 6.A.1 定位

`TOOLS.md` 回答：

- **我有权调用什么**（工具白名单）
- **我禁止调用什么**（工具红线）
- **冲突时怎么办**（工具边界与 SOUL 的协作规则冲突时的裁决顺序）

> **🚨 关键概念（第二次强调）**：
> **Tools 和 Skills 是两个独立子系统**，共享 Gateway RPC。
> 别把二者当「双协议」。

### 6.A.2 关键字段

| 字段 | 类型 | 语义 | 必填 |
|---|---|---|---|
| `registry` | list[string] | 本 agent 可见的工具集合 | ✅ |
| `allow` | list[string] | 允许调用 | ✅ |
| `deny` | list[string] | 禁止调用（红线） | ✅ |
| `approval_required` | list[string] | 需批准才可调用 | 建议 |
| `conflict_resolution` | string | **工具边界与 SOUL 冲突时的裁决顺序** | ✅ 本文重点 |
| `unavailable` | list[string] | 明确不可用（如未装 MCP） | 建议 |

### 6.A.3 「工具边界 vs SOUL 冲突」的裁决规则（本文核心）

这是 `TOOLS.md` 最容易被漏写的一块，也是实际最高频的冲突源。

**典型冲突场景**：

```
SOUL 说：        「诚实优先于完满 —— 不清楚就说清楚不清楚」
TOOLS 说：       「allow: web_search（允许联网搜索）」
现实：           本机 MCP = 0 配置，联网类工具可能不可用
```

此时如果 agent 选择了**编造一个搜索结果**，它就违反了 SOUL。
**冲突裁决规则必须显式写下来**，否则 agent 会在两难时自行发挥。

**推荐裁决顺序（四级）**：

| 优先级 | 层 | 规则 |
|---:|---|---|
| 1 | **SOUL 的红线** | 违反价值观的操作**一律不做**，不管工具是否允许 |
| 2 | **TOOLS 的 `deny`** | 明确禁止的工具**一律不调**，不管任务多需要 |
| 3 | **TOOLS 的 `approval_required`** | 需批准的先申请，不先斩后奏 |
| 4 | **TOOLS 的 `allow`** | 以上都通过时才执行 |

**示例写法**：

```markdown
## conflict_resolution

当工具能力与 SOUL 价值观冲突时，按以下顺序裁决：

1. **SOUL 红线优先**：若某工具的输出将导致违反 SOUL 的 `values`，
   则**不使用该工具**，并显式报告「因价值观约束未执行」。
2. **TOOLS deny 次之**：`deny` 列表中的工具一律不调用，
   需要时改走 `approval_required` 申请流程。
3. **工具不可用时不得编造**：若工具在 `unavailable` 中
   （例：MCP 未配置），必须显式说明「工具不可用」，
   **严禁伪造工具输出**。
4. **以上均通过 → 执行**，并在输出中标注所用工具与证据路径。
```

### 6.A.4 完整示例（可复制）

```markdown
# TOOLS · <agent-id>

## registry

本 agent 可见工具集合（对应 Gateway RPC `tools.catalog`）：
- read_file
- search_files
- web_search
- web_extract
- execute_code

## allow

- read_file
- search_files
- web_search
- web_extract

## deny

- <不可逆操作类工具>
- <凭据读写类工具>

## approval_required

- execute_code

## unavailable

- 全部 MCP server 工具      # 本机 mcp list = 0 配置（✅ 实测基线）

## conflict_resolution

（见上节四级裁决规则）

## notes

- 工具目录 RPC：`tools.catalog`（✅ 真名）
- 技能状态 RPC：`skills.status`（✅ 真名；与 tools 是**两个独立子系统**）
```

### 6.A.5 本机真实基线（✅）

| 项 | 值 |
|---|---|
| MCP 子命令数 | **14** |
| MCP 命名空间 | **`mcp.servers`** |
| `openclaw mcp list` | **0 配置** |
| `~/.openclaw/extensions/` | **不存在**（未装自定义 plugin） |
| plugins | 51/69 → 53/73 enabled |

**重要推论**：

> **本机 MCP 0 配置。** 这意味着任何依赖 MCP server 的工具
> **在本机不可用**。`TOOLS.md` 的 `unavailable` 段应当**如实登记**这一点，
> 否则 agent 会以为「我有 MCP 工具」然后编造调用结果。

```bash
# 复现基线
openclaw mcp list            # 期望：0 配置
ls ~/.openclaw/extensions/   # 期望：No such file or directory
openclaw plugins list        # 期望：53/73 enabled（live）
```

### 6.A.6 常见错误（TOOLS）

| # | ❌ 错误 | ✅ 正确 |
|---:|---|---|
| 1 | 不写 `conflict_resolution` | 显式写四级裁决顺序 |
| 2 | 工具不可用时编造输出 | 显式报告「不可用」（SOUL 红线） |
| 3 | 把 Tools 与 Skills 混为一谈 | 两个独立子系统；RPC `tools.catalog` / `skills.status` |
| 4 | 不登记本机 MCP = 0 配置 | `unavailable` 段如实登记 |
| 5 | `deny` 列表空着 | 至少有一条红线 |
| 6 | 认为 `TOOLS.md` 能强制拦截调用 | **它是声明层**；运行时校验在 Gateway/RPC 侧 |

### 6.A.7 验证步骤

```bash
AGENT=<your-agent>
T=~/.openclaw/workspace/agents/roles/$AGENT/contracts/TOOLS.md

test -s "$T" && echo "✅ 非空" || echo "❌ 空/缺失"
for k in allow deny conflict_resolution; do
  grep -qi "^## *$k" "$T" && echo "✅ $k" || echo "⚠️ 缺 $k"
done

# 登记本机 MCP 0 配置事实
openclaw mcp list 2>/dev/null | head -3
```

### 6.A.8 互链

- 配方 → `cookbook/03-skills-tools-mcp.md`
- 排坑 → `faq-troubleshooting/F5-Skills-Tools-MCP.md`
- MCP 配置 → `02-config-schema.md` §2.19 + 同卷 `04-mcp-reference.md`
- 协议理论 → `chapters/02-protocols/02-七大契约.md` 契约 4
- MCP 绑定 → `chapters/08-mcp-binding/08-MCP绑定.md`

---

## 6.B `IDENTITY.md` 完整规范

### 6.B.1 定位

`IDENTITY.md` 回答：

- **我对外叫什么**（可识别身份）
- **我怎么被路由到**（routing 字段）
- **我属于哪个群 / 频道**（绑定关系）

> **🚨 术语红线**：**顶层 `routing` 字段不存在**（✅ 实测）。
> 路由能力由以下真实路径承担：
> - `channels.feishu.requireMention`
> - `channels.feishu.groupAllowFrom`
> - `agents.entries.<id>.groupChat.mentionPatterns`
> - `bindings`（37 条：Telegram 19 + 飞书 18）

### 6.B.2 关键字段

| 字段 | 类型 | 语义 | 对应真实配置层路径 |
|---|---|---|---|
| `display_name` | string | 对外显示名/昵称 | —（协议层） |
| `agent_id` | string | 内部唯一 id | `agents.entries.<id>` |
| `channels` | list[string] | 我挂在哪些渠道 | `bindings` |
| `routing.mention_patterns` | list[string] | 群内触发我的模式 | `agents.entries.<id>.groupChat.mentionPatterns` |
| `routing.require_mention` | bool | 是否必须 @ 才响应 | `channels.feishu.requireMention` |
| `routing.allow_from` | list[string] | 群/来源白名单 | `channels.feishu.groupAllowFrom` |

### 6.B.3 完整示例（可复制）

```markdown
# IDENTITY · <agent-id>

## display_name

<对外显示名>

## agent_id

<agent-id>          # 必须与 agents.entries 的键一致

## channels

- telegram          # bindings 中 Telegram 19 条之一
- feishu            # bindings 中飞书 18 条之一

## routing

mention_patterns:
  - "<pattern-1>"   # ⏳ 取值待实测
  - "<pattern-2>"
require_mention: <true|false>     # ⏳ 当前取值待实测
allow_from:
  - "<来源标识>"     # ⏳ 当前取值待实测

## notes

- 顶层 `routing` 字段**不存在**；真实配置路径见上表右列。
- `bindings` 是 **list**（37 元素），不是 dict。
```

### 6.B.4 `agent_id` 一致性检查（最重要）

> **`IDENTITY.md` 的 `agent_id` 必须与 `agents.entries` 的键完全一致。**
> 不一致 = 身份声明与运行时身份脱节 → 路由失败。

```bash
AGENT=<your-agent>

# 运行时侧：agents.entries 的键
jq -r '.agents.entries | keys[]' ~/.openclaw/openclaw.json

# 声明侧：IDENTITY.md 里的 agent_id
grep -A2 -i "^## *agent_id" \
  ~/.openclaw/workspace/agents/roles/$AGENT/contracts/IDENTITY.md

# 自动比对
DECL=$(grep -A2 -i "^## *agent_id" \
  ~/.openclaw/workspace/agents/roles/$AGENT/contracts/IDENTITY.md \
  | grep -oE '^[a-z0-9_-]+' | head -1)
jq -e --arg a "$DECL" '.agents.entries[$a] != null' ~/.openclaw/openclaw.json >/dev/null \
  && echo "✅ 一致: $DECL" || echo "🚨 不一致/不存在于 agents.entries: $DECL"
```

### 6.B.5 渠道绑定一致性

```bash
AGENT=<your-agent>

# 该 agent 在 bindings 中的条数
jq -r --arg a "$AGENT" '[.bindings[] | select((.agent // "") == $a)] | length' \
   ~/.openclaw/openclaw.json

# 全部 binding 总数（期望 37）
jq '.bindings | length' ~/.openclaw/openclaw.json

# 官方等价视图
openclaw agents bindings
```

**本机绑定基线（✅）**：

| 渠道 | 条数 |
|---|---:|
| Telegram | 19 |
| 飞书 | 18 |
| **合计** | **37** |

### 6.B.6 常见错误（IDENTITY）

| # | ❌ 错误 | ✅ 正确 |
|---:|---|---|
| 1 | 顶层写 `routing: {...}` 到 `openclaw.json` | 改真实路径（见 §6.B.2 表右列） |
| 2 | `agent_id` 与 `agents.entries` 键不一致 | 逐字一致（跑 §6.B.4） |
| 3 | 把 `bindings` 当 dict 写 | 它是 **list**（append 元素） |
| 4 | 改名只改 `display_name`，不同步 `agents.entries` | 两层同时改 |
| 5 | 假设 `heartbeat` 是顶层字段 | 真实路径 `agents.entries.<id>.heartbeat.every` |

### 6.B.7 危险改动警告（IDENTITY 相关）

> **🚨 9/21 飞书事故同款**：
> 改 `channels.feishu.requireMention` + `groupAllowFrom` 时，
> **若白名单过窄 → 账号静默 disconnected，可超过 60 分钟无人发现。**

**改前必做**：

```bash
CFG=~/.openclaw/openclaw.json
cp "$CFG" "$CFG.bak.pre-fix-$(date +%Y-%m-%d-%H%M)"
python3 -m json.tool "$CFG" >/dev/null && echo "✅ 语法 OK"
# 改后必须在飞书群里实测一次 @，确认 6 账号全部在线
```

**事故事实（✅ 底稿 §4.2）**：

```
根因：requireMention: true + groupAllowFrom 仅丘总
结果：6 账号 disconnected，静默 >60min
上游修复：PR #152777 · OPEN（feishu groupPolicy）
```

### 6.B.8 互链

- 配方 → `cookbook/01-protocol-SOUL.md` · C1-5
- 排坑 → `faq-troubleshooting/F2-协议-SOUL-AGENTS-USER.md` · `F3-心跳与定时.md`
- 事故全文 → `case-library/01-real-incidents.md`
- 配置路径 → `02-config-schema.md` §2.6（channels）/ §2.4（bindings）
- 协同路由 → `chapters/06-coordination/06-协同军团.md`

---
## 7. `HEARTBEAT.md` / `MEMORY.md` / Cron 规范

### 7.0 本节最重要的一张图（先记这个）

```
       ┌──────────────────────────────────────────┐
       │ HEARTBEAT.md（文件层）                    │
       │ 「我醒来做什么」——说明书                  │
       └──────────────────────────────────────────┘
                        ↑ 被谁触发？
       ┌──────────────────────────────────────────┐
       │ agents.entries.<id>.heartbeat.every      │
       │ （配置层）「我多久醒一次」——旋钮 ✅ 真名  │
       └──────────────────────────────────────────┘
                        ↓ 实际调度
       ┌──────────────────────────────────────────┐
       │ automations（运行层 · 本机 61 条）        │
       │ heartbeat:tiance / heartbeat:kunlun …    │
       └──────────────────────────────────────────┘
```

> **改频率 → 配置层 JSON；改内容 → 文件层 MD；看实况 → `openclaw automations list`。**
> 三者**不是一回事**，这是本节最容易搞错的点。

---

## 7.A `HEARTBEAT.md` 完整规范

### 7.A.1 定位

`HEARTBEAT.md` 是 agent 的**自省/自驱说明书**：
当心跳触发（agent 自己醒过来）时，它按这份文件决定「醒来做什么」。

**与 `SOUL.md` 的分工**：

| 文件 | 回答 |
|---|---|
| `SOUL.md` | 我是谁（持续存在） |
| `HEARTBEAT.md` | 我醒来时做什么（周期性动作） |

### 7.A.2 🚨 真实路径（本卷最关键的一条真名）

```
agents.entries.<id>.heartbeat.every
```

**✅ 已实测。** 而以下写法**全部错误**：

| ❌ 虚构 / 误植 | ✅ 真名 |
|---|---|
| 顶层 `heartbeat` | `agents.entries.<id>.heartbeat.every` |
| `heartbeat.interval` | `agents.entries.<id>.heartbeat.every`（是 `every` 不是 `interval`） |
| 顶层 `runtime.scheduler` | 无此字段 |
| `subagents[].heartbeat` | `agents.entries.<id>.heartbeat` |

```bash
# 查看每个 agent 的心跳旋钮
jq -r '.agents.entries | to_entries[]
       | "\(.key)\t\(.value.heartbeat.every // "（未设置）")"' \
   ~/.openclaw/openclaw.json
```

> **⚠️ 值待实测**：底稿只确认了**路径真名**（✅），
> **未收录 18 个 agent 各自的 `heartbeat.every` 具体取值** → ⏳。
> 上面的 `jq` 是自查手段，不是本卷给出的答案。

### 7.A.3 关键字段（HEARTBEAT.md 文件层）

| 字段 | 类型 | 语义 | 必填 |
|---|---|---|---|
| `every` | string | 心跳频率（**须与配置层一致**） | ✅ |
| `wake_actions` | list[string] | 醒来依次做什么 | ✅ |
| `skip_conditions` | list[string] | 什么情况跳过本次 | ✅ |
| `escalate_on` | list[string] | 什么情况升级上报 | 建议 |
| `budget` | string | 单次心跳的预算约束 | 建议 |

### 7.A.4 完整示例（可复制）

```markdown
# HEARTBEAT · <agent-id>

## every

30m        # ⚠️ 必须与 agents.entries.<id>.heartbeat.every 保持一致

## wake_actions

1. 读 `MEMORY.md`，加载未完成事项
2. 扫 `memory/` 最近 24h 记录，找未闭环项
3. 检查上一次心跳是否报错（若有 → 走 escalate_on）
4. 有明确任务则推进；无任务则**不做动作**（不要为了干活而干活）

## skip_conditions

- 上一次心跳在 <N> 分钟内（防抖）
- 所在渠道全部 disconnected
- 已有其它 cron 正在执行同类任务（避免并发写入）

## escalate_on

- 连续 2 次同类失败
- 检测到 `primary == fallback[0]` 自循环（8/19 事故模式）
- 超过 <N> 分钟无任何心跳事件

## budget

单次心跳不超过 <N> 次工具调用；超出则落盘进度并结束。
```

### 7.A.5 生产实况对照（✅ 底稿 §3.3）

本机 61 条 automations 中，**3 条 heartbeat 的实测状态**：

| automation | 频率 | 实测状态 |
|---|---|---|
| `heartbeat:tiance` | every **30m** | **skipped** |
| `heartbeat:kunlun` | every **30m** | **error 99+x** |
| `heartbeat:peter` | every **2h** | **error 70x** |

> **🚨 这是一组严重的生产健康信号**：
> - `heartbeat:kunlun` **error 99+ 次** → 基本处于持续失败状态
> - `heartbeat:peter` **error 70 次** → 高频失败
> - `heartbeat:tiance` **skipped** → 被跳过（可能是 `skip_conditions` 生效，
>   也可能是调度层跳过，**两者含义不同，需人工确认**）
>
> **处置原则**：不要盲目重启。先看 `openclaw automations list` +
> 对应 agent 的 `memory/` 日志，定位是「内容错误」还是「调度错误」。

```bash
# 复现心跳实况
openclaw automations list | grep -i heartbeat

# 全部 automations 计数（期望 61）
openclaw automations list | wc -l

# 含错误的条目
openclaw automations list | grep -i "error"
```

### 7.A.6 常见错误（HEARTBEAT）

| # | ❌ 错误 | ✅ 正确 |
|---:|---|---|
| 1 | 在 `openclaw.json` 顶层写 `heartbeat` | 写 `agents.entries.<id>.heartbeat.every` |
| 2 | 用 `interval` 而非 `every` | 真名是 **`every`** |
| 3 | `HEARTBEAT.md` 的 every 与配置层不一致 | 两层同步（配置层是权威） |
| 4 | 心跳里塞大量任务 | 心跳只做**小步自省**；重活走独立 cron |
| 5 | 不写 `skip_conditions` | 必写（防抖 + 防并发写） |
| 6 | 看到 error 就狂重启 | 先定位（内容错 vs 调度错） |

### 7.A.7 验证步骤

```bash
AGENT=<your-agent>
H=~/.openclaw/workspace/agents/roles/$AGENT/contracts/HEARTBEAT.md

test -s "$H" && echo "✅ 非空" || echo "❌ 空/缺失"
grep -qi "^## *every"           "$H" && echo "✅ every" || echo "❌ 缺 every"
grep -qi "^## *wake_actions"    "$H" && echo "✅ wake_actions" || echo "❌ 缺 wake_actions"
grep -qi "^## *skip_conditions" "$H" && echo "✅ skip_conditions" || echo "❌ 缺 skip_conditions"

# 一致性：MD 声明 vs 配置层旋钮
MD_EVERY=$(grep -A2 -i "^## *every" "$H" | grep -oE '[0-9]+[smh]' | head -1)
CFG_EVERY=$(jq -r --arg a "$AGENT" '.agents.entries[$a].heartbeat.every // "（未设置）"' \
  ~/.openclaw/openclaw.json)
echo "MD=$MD_EVERY  CFG=$CFG_EVERY"
[ "$MD_EVERY" = "$CFG_EVERY" ] && echo "✅ 一致" || echo "⚠️ 不一致（以配置层为准）"

# 调度实况
openclaw automations list | grep -i "heartbeat:$AGENT" || echo "⏳ 未找到该心跳编排"
```

---

## 7.B `MEMORY.md` 完整规范

### 7.B.1 定位（含一条重要纠偏）

`MEMORY.md` 是 agent 的**记忆协议文件**——
规定它「记得什么、怎么分层、怎么复习」。

> **🚨 重要纠偏（务必读）**：
> **OpenClaw 真正的 MEMORY 是「文件模板」，不是 MemGPT 的 4 类记忆。**
> 不要给 MEMORY 协议写「4 类 memory（core / archival / recall / archive）」——
> 那是 MemGPT 的模型，**不是 OpenClaw 的**。
> 详见 §2.4 对位矩阵。

### 7.B.2 关键字段

| 字段 | 类型 | 语义 | 必填 |
|---|---|---|---|
| `tiers` | list[string] | 记忆分层（本书自定义层名，**非 MemGPT 4 类**） | ✅ |
| `write_policy` | string | 什么情况下写入记忆 | ✅ |
| `review_cadence` | string | 复习节奏（对应心跳/ cron） | ✅ |
| `retention` | string | 保留策略 | 建议 |
| `forget_rule` | string | 什么情况主动遗忘 | 建议 |

> **⚠️ 口径声明**：`chapters/02-protocols` 中出现过
> `memory_tiers[]` / `compaction_policy` 的表述——**它们是本书接口层口径**，
> **不是** `~/.openclaw/openclaw.json` 的字段。
> 本机实测：`compaction` / `contextTokenBudget` 等在配置中 **0 命中**（见本卷 02 §4）。

### 7.B.3 完整示例（可复制）

```markdown
# MEMORY · <agent-id>

## tiers

- `day`      —— 当日流水（memory/<date>-*.md）
- `topic`    —— 按主题聚合（memory/topic-*.md）
- `anchor`   —— 长期锚点（本文件 + SOUL 内核区）

## write_policy

- 出现以下任一情况即写入：
  1. 完成一个可验证的任务
  2. 发生一次事故或修复
  3. 出现一个需要跨会话延续的决定
- **不写**：无结论的中间过程、可随时重跑的命令输出

## review_cadence

- 每 24h：扫 `memory/` 找未闭环项（由心跳触发）
- 每周：跨主题聚合 → 更新 `anchor`
- 每月：能力矩阵复盘（⚠️ 本机此项 26 天未续期，见 §7.C.5）

## retention

- `day`：保留 <N> 天
- `topic`：长期保留
- `anchor`：永久（纳入 Git）

## forget_rule

- 被后续记录明确推翻的中间结论 → 删除
- 重复 3 次以上的同款教训 → 合并为一条规则
```

### 7.B.4 记忆与 Compaction 的关系（易错）

| 维度 | `MEMORY.md` | Compaction |
|---|---|---|
| 形态 | **文件模板**（工作区） | **运行时机制** |
| 可编辑 | ✅ 人工编辑 | ❌ 由常量决定 |
| 位置 | `agents/<id>/MEMORY.md` | **不在** `openclaw.json` |
| 关键名 | `tiers` / `write_policy` … | `CompactionRequestBudget.reserveTokens` |
| 常量 | — | `MAX_COMPACTION_RESERVE_RATIO = 0.25`（**不可配置**） |
| 派生值 | — | `effectiveReserveTokens` |

```bash
# 验证 Compaction 相关名在配置中 0 命中（本机实测基线）
CFG=~/.openclaw/openclaw.json
for k in compaction effectiveReserveTokens reserveTokens reserveTokensFloor contextTokenBudget; do
  n=$(jq --arg k "$k" '[paths|select(.[-1]==$k)]|length' "$CFG")
  printf '%-26s → %s 命中\n' "$k" "$n"
done
# 期望：全部 0
```

> **关键理解**：**0 命中 ≠ 功能不存在。** Compaction 机制当然存在，
> 只是不在配置文件层。**不要因为查不到就以为没这个功能。**

### 7.B.5 常见错误（MEMORY）

| # | ❌ 错误 | ✅ 正确 |
|---:|---|---|
| 1 | 给 MEMORY 写 MemGPT 的 4 类记忆 | OpenClaw 的 MEMORY 是**文件模板** |
| 2 | 认为 `compaction_policy` 是配置字段 | 是**接口层口径**，不在 `openclaw.json` |
| 3 | 说「compaction 可配 20000」 | 常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25`，**不可配置** |
| 4 | 写 `reserveTokensFloor` | 真名 `CompactionRequestBudget.reserveTokens` |
| 5 | 记忆只写不复习 | 显式写 `review_cadence` |
| 6 | 记忆无分层，越滚越大 | 用 `tiers` 分层 + `retention` 收敛 |
| 7 | 把无结论的中间过程写进记忆 | 只写「完成 / 事故 / 待延续决定」三类 |

### 7.B.6 验证步骤

```bash
AGENT=<your-agent>
M=~/.openclaw/workspace/agents/roles/$AGENT/contracts/MEMORY.md

test -s "$M" && echo "✅ 非空" || echo "❌ 空/缺失"
for k in tiers write_policy review_cadence; do
  grep -qi "^## *$k" "$M" && echo "✅ $k" || echo "⚠️ 缺 $k"
done

# 反例检测：不该出现 MemGPT 4 类
grep -qiE "core.*archival.*recall.*archive" "$M" \
  && echo "🚨 疑似写入 MemGPT 4 类记忆（应为 OpenClaw 文件模板）" \
  || echo "✅ 未发现 MemGPT 4 类误植"

# 反例检测：不该出现 reserveTokensFloor
grep -qi "reserveTokensFloor" "$M" \
  && echo "🚨 出现已勘误字段 reserveTokensFloor" || echo "✅ 无 reserveTokensFloor"

# 记忆目录实况
ls -1 ~/.openclaw/workspace/agents/roles/$AGENT/memory/ 2>/dev/null | tail -5
```

---

## 7.C Cron / Automations 规范

### 7.C.1 真名命令（🚨 参数名全部不同）

| ❌ 虚构 | ✅ 真名 |
|---|---|
| `openclaw cron add --schedule X --target Y --prompt Z` | `openclaw cron add --cron X --session Y --message Z` |
| `openclaw automations create` | ⏳ 待实测 |
| `openclaw cron list` | `openclaw automations list`（✅ 实测存在） |

> **三个参数名变化**：`--schedule` → **`--cron`**；`--target` → **`--session`**；
> `--prompt` → **`--message`**。

```bash
openclaw automations list        # ✅ 实测存在（本机 61 条）
```

> **⚠️ 诚实边界**：`openclaw automations add` 的**实际落盘行为未实测**
> （为避免污染本机 61 条生产编排，**刻意没跑**）→ **⏳ 待实测**。
> 上表 `openclaw cron add --cron/--session/--message` 来自底稿 §1.2 真名对照表（✅）。

### 7.C.2 本机 61 条 automations 构成（✅ 底稿 §3.3）

| 类别 | 数量 | 备注 |
|---|---:|---|
| 心跳（heartbeat） | 3 | tiance 30m/skipped · kunlun 30m/error 99+x · peter 2h/error 70x |
| 「暗夜熔炉」cron | **13** | **串行铺开 01:10 → 03:30** |
| `skill-collection-review` | **18** | — |
| 蜂鸟 | 9 | — |
| 凤凰 | 4 | — |
| `memory-core:memory-dreaming` | 1 | — |
| `蜂群-A-晨间全量扫描` | 1 | — |
| `hetu-回测进化日报` | 1 | — |
| `Peter 每日人生教练早课` | 1 | — |
| `军功爵周结算` | 1 | — |
| `能力矩阵月度更新` | 1 | **error 4x** |
| （其余） | — | 合计基线 **61** 条 |

> **历史口径**：早期实测 **43 条**，本机 live **61 条** —— **两次均曾观测到**。
> 引用时必须标注口径与时间。

### 7.C.3 「暗夜熔炉」串行编排解读

```
01:10  →  01:xx  →  …  →  03:30
（13 条串行铺开，不是并发）
```

**为什么要串行**：夜间复盘类任务会同时读 `memory/`、写报告、调模型。
**并发跑会造成**：
- 并发写同一文件（丢失更新）
- Gateway 侧 state 库锁争用（参见 `openclaw health` 被独占锁遮挡的现象）
- 模型 API 限流

**设计原则**：**夜间批处理一律串行铺开，留出间隔。**

### 7.C.4 `memory-core:memory-dreaming` 与睡眠机制

本机存在 `memory-core:memory-dreaming` automation ——
记忆巩固（类似「睡眠中整理记忆」）的编排。

**与 MEMORY.md 的关系**：

| 层 | 角色 |
|---|---|
| `MEMORY.md` | 声明「记忆怎么分层、怎么写」 |
| `memory-core:memory-dreaming` | **执行**「记忆巩固」的定时编排 |

### 7.C.5 ⚠️ 生产健康信号（必读）

| 信号 | 事实 | 风险 |
|---|---|---|
| `heartbeat:kunlun` | **error 99+x** | 该 agent 心跳长期失败 |
| `heartbeat:peter` | **error 70x** | 高频失败 |
| `heartbeat:tiance` | **skipped** | 被跳过（原因待确认） |
| `能力矩阵月度更新` | **error 4x** + **26 天未续期** | 能力矩阵停止更新 |
| `a2a` 插件 | **disabled** | A2A 能力不可用 |
| MCP | **0 配置** | 全部 MCP 工具不可用 |

**「能力矩阵 26 天未续期」的完整事实链（✅）**：

```
2026-09-01 后无新记录
   → cron `能力矩阵月度更新` error(4x)
      → 26 天无更新
```

> **这是「制度写在 md 但行为不存在」的典型样本**——
> 文档里说每月更新，实际调度层持续报错。
> 排查思路见 `faq-troubleshooting/F7-治理漂移体检.md`。

### 7.C.6 健康巡检脚本

```bash
#!/usr/bin/env bash
# automations 健康巡检（只读）
echo "=== 总数（基线 61）==="
openclaw automations list | wc -l

echo
echo "=== 心跳状态 ==="
openclaw automations list | grep -i heartbeat

echo
echo "=== 报错条目 ==="
openclaw automations list | grep -i "error"

echo
echo "=== 配置层心跳旋钮 ==="
jq -r '.agents.entries | to_entries[]
       | "\(.key)\t\(.value.heartbeat.every // "（未设置）")"' \
   ~/.openclaw/openclaw.json

echo
echo "=== 已知风险点自查 ==="
openclaw mcp list | head -3                 # 期望 0 配置
ls -d ~/.openclaw/extensions/ 2>/dev/null || echo "extensions/ 不存在（符合基线）"
```

### 7.C.7 常见错误（Cron）

| # | ❌ 错误 | ✅ 正确 |
|---:|---|---|
| 1 | `cron add --schedule/--target/--prompt` | `--cron` / `--session` / `--message` |
| 2 | 夜间批处理并发跑 | 串行铺开（留间隔） |
| 3 | 用 `cron list` 查 | `automations list` |
| 4 | 不写 `skip_conditions` 导致重复触发 | 心跳/cron 都要防抖 |
| 5 | 看到 error 只重启 | 先定位（内容错 vs 调度错） |
| 6 | 在生产机上试 `automations add` | 会污染 61 条编排 → 用测试环境 / 先备份 |

### 7.C.8 互链

- 心跳排坑 → `faq-troubleshooting/F3-心跳与定时.md`
- 记忆训练 → `sop-library/04-memory-training-sop.md`
- 心跳监控 SOP → `sop-library/03-heartbeat-monitor-sop.md`
- 配方 → `cookbook/02-protocol-HEARTBEAT-MEMORY.md`
- 配置层 → `02-config-schema.md` §2.2（agents）/ §2.11（memory）
- 治理 → `chapters/06-governance/06-治理系统.md`

---
## 8. 诚实边界

> **原则**：本卷只写实测到的。没实测到的一律标 ⏳，**绝不用「按常规应该有」补齐**。
> 每个 ✅ 都有 `00-实测事实底稿.md` 出处。

### 8.1 ✅ 已实测确认（可直接引用）

**协议文件层**

- ✅ 7 协议文件的存在形态：`SOUL.md / USER.md / AGENTS.md / TOOLS.md / HEARTBEAT.md / IDENTITY.md / MEMORY.md`
- ✅ 真实路径形态：`~/.openclaw/workspace/agents/roles/<your-agent>/AGENTS.md`
- ✅ 本书推荐布局：`agents/roles/<agent>/contracts/<PROTOCOL>.md`
- ✅ 创建命令可行（`mkdir -p` + `touch`，`ls *.md | wc -l` 应为 7）

**关键真名路径（本卷核心事实）**

- ✅ `agents.entries.<id>.heartbeat.every`（心跳频率真实路径）
- ✅ `agents.entries.<id>.groupChat.mentionPatterns`（提及模式真实路径）
- ✅ `channels.feishu.requireMention`（飞书需 @）
- ✅ `channels.feishu.groupAllowFrom`（群白名单）
- ✅ `agents.entries`（18 个 agent）
- ✅ `bindings`（list · 37 条：Telegram 19 + 飞书 18）

**🚨 不存在的顶层字段（✅ 已否定）**

- ✅ 顶层 `runtime` / `workspace` / `routing` / `heartbeat` / `subagents` **全部不存在**

**运行层 RPC 真名**

- ✅ `tools.catalog`（工具目录 RPC）
- ✅ `skills.status`（技能状态 RPC）
- ✅ Tools 与 Skills 是**两个独立子系统**

**命令真名**

- ✅ `openclaw automations list`（子命令含 `list`）
- ✅ `openclaw agents` 子命令：`add · bind · bindings · delete · list`
- ✅ `openclaw plugins`（复数，15 子命令）
- ✅ `openclaw skills check --agent <id>`（tiance → Total 253）
- ✅ `openclaw mcp`（14 子命令）· 命名空间 `mcp.servers` · `mcp list` = **0 配置**
- ✅ `openclaw acp`（Zed ACP bridge）· `openclaw backup create` ·
  `openclaw health` / `openclaw doctor` · `openclaw pairing` · `openclaw promos` ·
  `openclaw proxy` · `openclaw config` / `audit` / `setup` / `onboard`
- ✅ cron 真名：`openclaw cron add --cron X --session Y --message Z`

**生产实况**

- ✅ 18 agent（主模型：opus-4-8 ×9 / gpt-5.6-sol ×4 / gpt-5.5 ×2 / gpt-5.6-terra ×2 / deepseek-v4-flash ×1）
- ✅ 61 条 automations（早期 43 条，两次均曾观测到）
- ✅ `heartbeat:tiance`（30m · **skipped**）
- ✅ `heartbeat:kunlun`（30m · **error 99+x**）
- ✅ `heartbeat:peter`（2h · **error 70x**）
- ✅ 13 个「暗夜熔炉」cron（**串行 01:10 → 03:30**）
- ✅ 18 个 `skill-collection-review` · 9 蜂鸟 · 4 凤凰
- ✅ `memory-core:memory-dreaming` · `蜂群-A-晨间全量扫描` · `hetu-回测进化日报` ·
  `Peter 每日人生教练早课` · `军功爵周结算` · `能力矩阵月度更新`（**error 4x**）
- ✅ 能力矩阵 **26 天未续期**（2026-09-01 后无新记录）
- ✅ plugins 51/69 → 53/73 enabled · `a2a` **disabled** · `~/.openclaw/extensions/` **不存在**
- ✅ skills：236 目录 / 221 含 SKILL.md / 47 无 frontmatter / 55 name 违例
- ✅ 真实 6/6 字段全覆盖样本：`afrexai-compliance-audit` · `skill-security-audit-v2` · `skill-security-audit`

**Compaction 真名**

- ✅ `reserveTokensFloor` 不存在 → `CompactionRequestBudget.reserveTokens`
- ✅ 常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25`（**不可配置**）
- ✅ `effectiveReserveTokens`（派生值）
- ✅ 5 名字在 `openclaw.json` **0 命中**；顶层 `session` 仅含 `dmScope`

**事故基线**

- ✅ 8/19 断线：MiniMax-M3 空 body → 17-18 fallback 首位被占 →
  轩辕 `primary == fallback[0]` 自循环；备份 `openclaw.json.bak.pre-fix-2026-08-19-0921`
- ✅ 9/21 飞书：`requireMention: true` + `groupAllowFrom` 仅丘总 →
  6 账号 disconnected，静默 >60min；PR #152777 · OPEN

### 8.2 ⏳ 待实测（本卷未覆盖，**禁止补全**）

**协议文件层**

- ⏳ `~/.openclaw/workspace/SHARED/` 作为**协议模板目录**的存在性与内容
  （`SOUL.md.template` 等是否真实存在）
- ⏳ OpenClaw 是否**内置** SOUL / AGENTS / USER / TOOLS / HEARTBEAT / IDENTITY / MEMORY 模板
- ⏳ 7 协议文件的字段名**是否被任何运行时组件解析**（vs 仅由 LLM 读取）
- ⏳ 协议文件是否由 OpenClaw **自动加载**（本书口径是「会话自动加载」，但加载路径待验）
- ⏳ 协议文件的**官方 frontmatter 规范**（本卷字段为本书接口层口径）
- ⏳ `contracts/` 目录是否为 OpenClaw 识别的约定目录（vs 本书推荐布局）

**心跳 / Cron 层**

- ⏳ 18 个 agent 各自的 `heartbeat.every` **具体取值**
- ⏳ 每个 `groupChat.mentionPatterns` 的**具体 pattern 列表**
- ⏳ `channels.feishu.requireMention` / `groupAllowFrom` 的**当前值**
- ⏳ `openclaw automations add` 的**实际落盘行为**（为避免污染 61 条编排，刻意未跑）
- ⏳ `openclaw automations` 完整子命令集
- ⏳ `openclaw cron` 子命令全貌
- ⏳ `heartbeat:tiance` 被 **skipped** 的确切原因（防抖跳过 vs 调度层跳过）

**工具 / 技能层**

- ⏳ `tools.catalog` / `skills.status` 的 CLI 调用方式与输出格式
- ⏳ `openclaw skills` 完整子命令集
- ⏳ `TOOLS.md` / `AGENTS.md` 的 `tools` / `skills` 段是否被运行时读取
- ⏳ `openclaw plugins install` 全生命周期
- ⏳ `~/.openclaw/extensions/` 目录创建与加载
- ⏳ MCP server 实际注册（本机 0 配置）

**其它**

- ⏳ `openclaw health` 完整输出（**被 Gateway state 库独占锁遮挡**）
- ⏳ ClawHub publish 流程
- ⏳ A2A TCK 测试
- ⏳ SLCP bridge demo
- ⏳ `openclaw gateway` 子命令集
- ⏳ 日志实际落盘路径

### 8.3 口径冲突处理规则

1. **本卷 §2 / §7 的 ✅ 事实**（源自底稿）
2. **`00-实测事实底稿.md`**（同源）
3. **`chapters/` 各章**（可能含 v1.0 残留；**看文首有无勘误块**）
4. **v1.0 及更早资料**（默认视为**已被勘误**）

**标准动作**：以 `jq` / `openclaw` 实测输出为准，回报维护者（天策）并标注实测时间。

### 8.4 版本口径

- **书内统一口径**：OpenClaw **2026.9.4 (3a9d69d)**
- **本机 live 复核**：OpenClaw **2026.9.6 (eb377ac)**

差异（✅ 已标注）：plugins 51/69 → 53/73。
**本卷所有协议层真名在两个版本上一致**（`heartbeat.every` /
`groupChat.mentionPatterns` / `requireMention` / `groupAllowFrom` / `bindings`）。

---

## 9. 互链总表

| 方向 | 目标 | 用途 |
|---|---|---|
| 本文 | `02-config-schema.md` | **配置层权威**（20 key / 幽灵字段 / Compaction） |
| 本文 | `00-实测事实底稿.md` | 本文全部事实来源 |
| 本文 | `04-mcp-reference.md` · `05-plugin-api.md` · `06-skill-spec.md` | 同卷其余分册 |
| 本文 | `faq-troubleshooting/F2-协议-SOUL-AGENTS-USER.md` | **协议层首要排坑** |
| 本文 | `faq-troubleshooting/F3-心跳与定时.md` | 心跳 / cron |
| 本文 | `faq-troubleshooting/F4-记忆与会话.md` | MEMORY / session |
| 本文 | `faq-troubleshooting/F5-Skills-Tools-MCP.md` | TOOLS / skills |
| 本文 | `faq-troubleshooting/F6-多Agent协同.md` | IDENTITY / 路由 / 多 agent |
| 本文 | `faq-troubleshooting/F7-治理漂移体检.md` | 漂移 / 能力矩阵未续期 |
| 本文 | `faq-troubleshooting/F-Top20-高频速查.md` | 高频速查 |
| 本文 | `sop-library/02-protocol-config-sop.md` | 协议配置 SOP |
| 本文 | `sop-library/03-heartbeat-monitor-sop.md` | 心跳监控 SOP |
| 本文 | `sop-library/04-memory-training-sop.md` | 记忆训练 SOP |
| 本文 | `sop-library/05-drift-governance-sop.md` | 漂移治理 SOP |
| 本文 | `cookbook/01-protocol-SOUL.md` | C1-1 ~ C1-5（SOUL/AGENTS/USER/TOOLS/IDENTITY 配方） |
| 本文 | `cookbook/02-protocol-HEARTBEAT-MEMORY.md` | HEARTBEAT / MEMORY 配方 |
| 本文 | `cookbook/03-skills-tools-mcp.md` | tools/skills/MCP 配方 |
| 本文 | `chapters/02-protocols/02-七大契约.md` | 7 契约理论 + **顶部勘误块** |
| 本文 | `chapters/03-skeleton/03-系统骨架.md` | 7 协议如何嵌入子系统 |
| 本文 | `chapters/06-governance/06-治理系统.md` | 漂移治理 / 安全 |
| 本文 | `chapters/06-coordination/06-协同军团.md` | 多 agent 协同 |
| 本文 | `chapters/10-skill-registry/` | SKILL.md frontmatter 规范 |
| 本文 | `case-library/01-real-incidents.md` | 8/19 + 9/21 事故全文 |
| 本文 | `00-术语对照表·v3.0行业标准版.md` | 35 条改名表 |

---

## 10. 附录 · 术语双写索引

> 首次出现必双写。本表汇总本文用到的全部条目（v3.0 改名表节选）。

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

**本文特别提示的同形异义（务必写全）**：

1. **`acp`（OpenClaw 命令）** vs **ACP（本书 v1.0 内部术语）** → v3.0 已改名 **SLCP**。
2. **ACP（Agent Client Protocol，Zed 生态）** vs **SLCP（本书内部协作协议）** → 引用写全称。
3. **初级智能体（Novice Agent）** —— 本文正文用「新人（初级智能体 / Novice Agent）」双写。

---

## 11. 附录 · 真名 vs 虚构 · 速查卡（可打印）

| ❌ 虚构 / 误植 | ✅ 真名 |
|---|---|
| 顶层 `heartbeat` | `agents.entries.<id>.heartbeat.every` |
| `heartbeat.interval` | `agents.entries.<id>.heartbeat.every`（是 **`every`**） |
| 顶层 `routing` | `channels.*.requireMention` / `agents.entries.<id>.groupChat.mentionPatterns` |
| 顶层 `subagents` | `agents.entries` + `bindings` |
| 顶层 `runtime` | 无对应顶层 |
| 顶层 `workspace` | 无对应顶层 |
| `~/.openclaw/workspace/openclaw.json` | `~/.openclaw/openclaw.json` |
| `openclaw agents create X` | `openclaw agents add X --workspace <dir>` |
| `openclaw agents health-check` | `openclaw health` / `openclaw doctor` |
| `openclaw agents archive` | `openclaw backup create` |
| `openclaw chat --agent X --prompt Y` | `openclaw agent --agent X --message Y` |
| `openclaw init` | `openclaw setup` / `openclaw onboard` |
| `openclaw plugin`（单数） | `openclaw plugins`（复数） |
| `manifest.yaml` | `openclaw.plugin.json`（JSON5） |
| `openclaw cron add --schedule/--target/--prompt` | `openclaw cron add --cron/--session/--message` |
| `reserveTokensFloor` | `CompactionRequestBudget.reserveTokens` |
| 「compaction 可配 20000」 | 常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25`（**不可配置**） |
| MEMORY 的 4 类记忆（core/archival/recall/archive） | OpenClaw 的 MEMORY 是**文件模板** |

---

## 12. 附录 · 7 协议速查矩阵（一页纸）

| 协议 | 一句话 | 关键字段 | 对应配置层路径 | 首要排坑 |
|---|---|---|---|---|
| `SOUL.md` | 我是谁（元灵魂协议） | `persona` / `values` / `tone` | —（协议层） | `F2-协议-SOUL-AGENTS-USER.md` |
| `USER.md` | 我服务谁 + 权限边界 | `owner` / `permissions` / `data_scope` | —（声明层） | `F2-协议-SOUL-AGENTS-USER.md` |
| `AGENTS.md` | 我怎么干（纪律 + tools/skills 段） | `scope` / `workflow` / `stop_conditions` / `tools` / `skills` | `tools.catalog` / `skills.status`（RPC） | `F5-Skills-Tools-MCP.md` |
| `TOOLS.md` | 我能调什么（含冲突裁决） | `allow` / `deny` / `conflict_resolution` | `tools.catalog`（RPC） | `F5-Skills-Tools-MCP.md` |
| `HEARTBEAT.md` | 我醒来做什么 | `every` / `wake_actions` / `skip_conditions` | **`agents.entries.<id>.heartbeat.every`** | `F3-心跳与定时.md` |
| `IDENTITY.md` | 我是谁对外 + 怎么被路由 | `display_name` / `agent_id` / `routing.*` | `bindings` / `channels.feishu.*` | `F6-多Agent协同.md` |
| `MEMORY.md` | 我记得什么 | `tiers` / `write_policy` / `review_cadence` | —（文件模板） | `F4-记忆与会话.md` |

---

**分册版本**：v5.0 行业标准版 · 2026-09-28
**数据来源**：`api-reference/00-实测事实底稿.md`（2026-09-27 / 2026-09-28 实测）
**维护者**：天策（Supervisor Layer）
**许可**：MIT（跟随 OpenClaw 主仓）
**校验方式**：以 `jq` / `openclaw` 实测输出为准，不信任何二手字段名

# 01 · OpenClaw CLI 完整参考（Command-Line Interface Reference）

> **手册版本**：v5.0 行业标准版 · 2026-09-27
> **License**：MIT（跟随 OpenClaw 主仓）
> **实测环境**：OpenClaw 2026.9.4 (3a9d69d) · Hermes Agent 0.20.1 · macOS 26.5.1 · 236 skills
> **本机 live 复核**：OpenClaw 2026.9.6 (eb377ac) · 18 agents · 61 automations · plugins 53/73（书内统一用 2026.9.4 口径）

---

## 目录

- [§0 本文件定位与阅读方式](#0-本文件定位与阅读方式)
- [§1 🚨 虚构命令警示（AI 幻觉重灾区）](#1--虚构命令警示ai-幻觉重灾区)
  - [1.1 为什么 CLI 是 AI 幻觉第一重灾区](#11-为什么-cli-是-ai-幻觉第一重灾区)
  - [1.2 真名 vs 虚构 · 9 条全表](#12-真名-vs-虚构--9-条全表)
  - [1.3 逐条拆解 · 为什么网上会流传 / 新手会踩什么坑](#13-逐条拆解--为什么网上会流传--新手会踩什么坑)
  - [1.4 自检清单 · 命令名合法性三问](#14-自检清单--命令名合法性三问)
- [§2 命令族完整参考](#2-命令族完整参考)
  - [2.1 `openclaw setup` / `openclaw onboard`](#21-openclaw-setup--openclaw-onboard)
  - [2.2 `openclaw agents`](#22-openclaw-agents)
  - [2.3 `openclaw agent`](#23-openclaw-agent)
  - [2.4 `openclaw automations`](#24-openclaw-automations)
  - [2.5 `openclaw mcp`](#25-openclaw-mcp)
  - [2.6 `openclaw acp`](#26-openclaw-acp)
  - [2.7 `openclaw plugins`](#27-openclaw-plugins)
  - [2.8 `openclaw backup`](#28-openclaw-backup)
  - [2.9 `openclaw health` / `openclaw doctor`](#29-openclaw-health--openclaw-doctor)
  - [2.10 `openclaw cron`](#210-openclaw-cron)
  - [2.11 `openclaw config` / `openclaw audit`](#211-openclaw-config--openclaw-audit)
  - [2.12 `openclaw pairing`](#212-openclaw-pairing)
  - [2.13 `openclaw promos`](#213-openclaw-promos)
  - [2.14 `openclaw proxy`](#214-openclaw-proxy)
  - [2.15 全局 flag 与退出码约定](#215-全局-flag-与退出码约定)
- [§3 常用工作流（5 条组合命令链）](#3-常用工作流5-条组合命令链)
- [§4 错误码与排障](#4-错误码与排障)
- [§5 诚实边界声明](#5-诚实边界声明)

---

## §0 本文件定位与阅读方式

本文件是《OpenClaw 硅基生命手册 · API 参考附录卷》的**第 1 册**，职责单一：

> **把 OpenClaw 的命令行接口（Command-Line Interface, CLI）讲清楚，并且只讲真实存在的命令。**

### 0.1 本文件不做什么

| 不做 | 去哪儿看 |
|---|---|
| 不解释「为什么要这样设计」 | chapters/03-系统骨架 |
| 不给端到端教学 | 00-getting-started/01-quickstart-5min |
| 不给完整配置文件 schema | api-reference/02-config-reference |
| 不给 MCP / A2A 协议细节 | chapters/09-MCP绑定 · chapters/10-A2A绑定 |
| 不给可复制脚本模板 | cookbook/ |
| 不给故障问诊对话树 | faq-troubleshooting/ |

### 0.2 阅读前的三条纪律

**纪律 1 · 只信本文件标了 ✅ 的部分。**
本文件所有命令名、子命令名、flag 名，凡标注 ✅ 的，均来自 2026-09-27 / 2026-09-28 的实机采集（详见 §5 与 api-reference/00-实测事实底稿）。凡标注 ⏳ 的，表示**当时未能实测**，本文件不为其正确性背书。

**纪律 2 · 术语双写是硬要求。**
本手册 v3.0 起采用「术语双写」规则（详见 00-术语对照表·v3.0行业标准版）。首次出现的内部黑话必须写成 `新名（原内部黑话 / English Alias）` 形式。例：

- **智能体集群（军团 / Agent Fleet）** —— 指本机 18 个 agent 的集合
- **Supervisor Layer（监军 / Supervisor Layer）** —— 指监督层角色
- **SLCP（原 ACP / Silicon Life Collaboration Protocol）** —— 注意此处有**三重撞名**，见 §2.6

**纪律 3 · 命令跑之前先过「三问」。**
见 §1.4。凡是没有通过三问的命令，**不要往终端里粘**。

### 0.3 本文件与全书的互链约定

| 链接前缀 | 目标文件 |
|---|---|
| `F1-*` … `F7-*` | `faq-troubleshooting/F1-环境与安装.md` … `F7-治理漂移体检.md` |
| `F-Top20` | `faq-troubleshooting/F-Top20-高频速查.md` |
| `C1-*` … `C7-*` | `cookbook/01-protocol-SOUL.md` … `cookbook/07-production-ops.md` |
| `SOP-1` … `SOP-6` | `sop-library/01-environment-setup-sop.md` … `06-incident-recovery-sop.md` |
| `02-*` | 本卷其他分册（如 `02-config-reference.md`） |

### 0.4 一处必须提前讲清的版本差异

本手册书内统一口径为 **OpenClaw 2026.9.4 (3a9d69d)**；而本机 live 复核时实际跑出的是 **OpenClaw 2026.9.6 (eb377ac)**。

```bash
openclaw --version
→ OpenClaw 2026.9.4 (3a9d69d)     # 任务基线（书内统一口径）
→ OpenClaw 2026.9.6 (eb377ac)     # 本机 live 复核实测
```

**诚实说明**：本文件所有「期望输出」样例，与 2026.9.4 口径对齐；`2026.9.6` 只用于交叉印证命令族是否存在，不用于断言输出格式逐字节一致。凡涉及两个版本可能不一致处，本文件标注 `[版本敏感]`。

---

## §1 🚨 虚构命令警示（AI 幻觉重灾区）

### 1.1 为什么 CLI 是 AI 幻觉第一重灾区

这一节存在的唯一理由：**在 2026 年的现实里，读者拿到 OpenClaw 命令的渠道，大概率不是官方文档，而是一个大语言模型。**

而 CLI 恰好是大语言模型幻觉率最高的表面。原因有四层，逐层叠加：

**第一层 · CLI 命名是「惯例密集区」。**
几乎所有现代 CLI 都遵循相似命名直觉：`init` 初始化、`create` 新建、`list` 列表、`delete` 删除、`--prompt` 提示词。当模型没见过某个具体 CLI 时，它会**用惯例填空**——生成一个「听起来本该存在」的命令。`openclaw init` 就是这么来的。它符合直觉、符合惯例、符合 90% 的同类工具，但 OpenClaw 里**没有这个子命令**。

**第二层 · 单数与复数不可预测。**
`plugin` 还是 `plugins`？`agent` 还是 `agents`？这两个前缀在 OpenClaw 里**都存在，但语义完全不同**：

- `openclaw agents`（复数）= **管理 agent 的注册表**（增删查绑）
- `openclaw agent`（单数）= **向某个 agent 发一条消息**（单次调用）

模型通常只记住其中一个，然后两个场景都拿它用。结果是：想建 agent 的人跑了 `openclaw agent add`，想对话的人跑了 `openclaw agents chat`——两条都是错的。

**第三层 · flag 名是纯约定，无逻辑可推。**
`--message` 还是 `--prompt`？`--cron` 还是 `--schedule`？`--session` 还是 `--target`？**这些名字没有任何推理路径可以推出来**，只能实测。模型在没实测的情况下生成的 flag，与随机猜测无异。

**第四层 · 网络二手内容在放大幻觉。**
大量博客、教程、AI 生成的「OpenClaw 上手指南」本身就是在**没跑过命令**的情况下写出来的。它们引用了 AI 幻觉产物，AI 又反过来学习这些博客。这是一个自我强化的污染闭环。你搜到的「教程」越多，幻觉越像共识。

**结论**：本节的 9 条对照表，不是「小知识点」，而是**本书读者接触 OpenClaw 的第一道防火墙**。

### 1.2 真名 vs 虚构 · 9 条全表

> 下表为**全书统一口径**，与 api-reference/00-实测事实底稿 §1.2 完全一致。任何分册引用此表时不得改写。

| # | ❌ 虚构（不存在） | ✅ 真名 | 关键差异 |
|---|---|---|---|
| 1 | `openclaw init` | `openclaw setup`（或 `onboard`） | 无 `init` 子命令 |
| 2 | `openclaw agents create X` | `openclaw agents add X --workspace <dir>` | 是 `add` 不是 `create` |
| 3 | `openclaw chat --agent X --prompt Y` | `openclaw agent --agent X --message Y` | 是 `agent` 不是 `chat`；是 `--message` 不是 `--prompt` |
| 4 | `openclaw agents health-check` | `openclaw health` / `openclaw doctor` | 无 `health-check` 子命令 |
| 5 | `openclaw agents archive` | `openclaw backup create` | 归档走 backup |
| 6 | `openclaw plugin`（单数） | `openclaw plugins`（复数） | 复数 |
| 7 | `manifest.yaml` | `openclaw.plugin.json`（**JSON5**） | 不是 YAML |
| 8 | `~/.openclaw/workspace/openclaw.json` | `~/.openclaw/openclaw.json` | 主配置真身 |
| 9 | `openclaw cron add --schedule X --target Y --prompt Z` | `openclaw cron add --cron X --session Y --message Z` | 参数名不同 |

**使用方式**：把这张表当作**贴纸**。凡是你要跑的命令、要引用的配置路径、要写的插件清单文件，先在这张表里扫一眼有没有撞上左边那列。

### 1.3 逐条拆解 · 为什么网上会流传 / 新手会踩什么坑

#### #1 虚构：`openclaw init` ｜ 真名：`openclaw setup`（或 `onboard`）

**错误形态**
```bash
openclaw init                      # ❌ zsh: command not found / unknown subcommand
openclaw init --yes                # ❌
openclaw init --provider openai    # ❌
```

**正确形态**
```bash
openclaw setup                     # ✅ 初始化向导
openclaw onboard                   # ✅ 初始化向导（同族别名）
```

**为什么网上会流传**
`init` 是 CLI 世界的最高频动词。`git init`、`npm init`、`docker init`、`terraform init`、`helm init`、`cargo init`……几乎每一个模型在训练语料里见过上千次 `X init`。当模型被问到「OpenClaw 怎么初始化」，它的先验分布第一个吐出的就是 `openclaw init`。而 OpenClaw 选的是 `setup` / `onboard`——两个更偏「向导（wizard）」语义的词，这在本机配置里也能印证：顶层 key 里有 `wizard`（4 个子项），说明 OpenClaw 的初始化在设计上是**对话式向导**，不是一条 `init` 命令。

**新手会踩什么坑**
1. **报错信息不友好** → 新手看到 `command not found`，第一反应是「我没装好」，于是去重装 OpenClaw，浪费 20 分钟。
2. **误以为要走 npm** → 有些人会退化到 `npx openclaw init`，同样失败，进一步加深「装错了」的误判。
3. **跑错向导** → 少数人会用 `openclaw config`（配置管理）来「初始化」，但 `config` 管的是**已存在配置的读写**，不是首装引导；结果配置没生成，人以为向导失败。
4. **在 CI 脚本里写死 `init`** → 自动化流程静默失败，直到某天才被发现。

**自检**：跑 `openclaw --help` 看顶层子命令列表里有没有 `setup` / `onboard`。有；有没有 `init`。没有。

**相关 FAQ**：F1-环境与安装
**相关 SOP**：SOP-1 环境搭建

---

#### #2 虚构：`openclaw agents create X` ｜ 真名：`openclaw agents add X --workspace <dir>`

**错误形态**
```bash
openclaw agents create my-agent                                    # ❌
openclaw agents create my-agent --dir ~/.openclaw/workspace/agents/my-agent   # ❌
```

**正确形态**
```bash
openclaw agents add my-agent --workspace ~/.openclaw/workspace/agents/my-agent  # ✅
```

**为什么网上会流传**
CRUD 惯例：`create` / `read` / `update` / `delete`。OpenClaw 的 `agents` 子命令集是 `add · bind · bindings · delete · list`（✅ 实测），**CRUD 里只有 `delete` 沿用了惯例**，`create` 被换成了 `add`，`read` 被换成了 `list`。模型记住了「有个建 agent 的操作」，就用 `create` 填。

第二个诱因：`add` 在英语里更偏「往已有集合里加一项」，`create` 更偏「从无到有造一个」。而 OpenClaw 的 `agents add` 语义恰恰是**第一条**——它往 `agents.entries`（本机实测 18 个 agent 的字典）里加一个 entry，而不是凭空造一个独立实体。这个语义差，模型学不出来，只有实测能看到。

**新手会踩什么坑**
1. **漏 `--workspace`** → 即使把 `create` 改成 `add`，如果漏掉 `--workspace <dir>`，agent 的 workspace 目录就没有落点。命令语法是 `openclaw agents add <name> --workspace <dir>`，`<name>` 和 `--workspace` 是**成对出现**的。
2. **agent 建了但找不到** → 建完之后不跑 `openclaw agents list` 确认，只用 `ls` 看目录。本机实测 `agents.entries` 有 18 键，注册表在 `openclaw.json` 里而不只在文件系统里。
3. **建完忘了绑渠道** → `add` 只建 agent，**不建渠道绑定**。绑定是另一条命令（`bind`），绑定清单是第三条（`bindings`）。新手常以为建完就能在 Telegram 里说话，结果发现没绑定，白白排查半小时。见 §3 工作流 2。
4. **误用 `archive` 做「下线」** → 想删 agent 时去搜 `archive`（见 #5），搜不到就退而用 `rm -rf` 删目录，导致 `agents.entries` 里留下悬挂键。

**相关 FAQ**：F6-多Agent协同
**相关 Cookbook**：C6-协同舰队

---

#### #3 虚构：`openclaw chat --agent X --prompt Y` ｜ 真名：`openclaw agent --agent X --message Y`

**错误形态**
```bash
openclaw chat --agent tiance --prompt "今天日报怎么样"     # ❌
openclaw chat tiance "今天日报怎么样"                      # ❌
openclaw agent --agent tiance --prompt "..."               # ❌ flag 名也错
```

**正确形态**
```bash
openclaw agent --agent tiance --message "今天日报怎么样"    # ✅
```

**为什么网上会流传**
这是**双重幻觉叠加**，也是本表里最容易骗到人的一条：

- **幻觉 A：把 `agents` 的反义词 `chat` 造出来。** 模型知道有 `openclaw agents`（复数）管注册表，就顺理成章地以为必须有一个 `openclaw chat` 管对话。
- **幻觉 B：`--prompt`。** 几乎所有 LLM SDK 的关键字都叫 `prompt`（`openai.chat.completions.create(messages=...)`、`anthropic.messages.create(...)` 里也全是 prompt 语义）。CLI 层面用 `prompt` 是极强先验。
- **真实命名逻辑**：OpenClaw 用**单数 `agent`** 表示「对一个 agent 的单次调用」，用 **`--message`** 强调这是「一条消息」而非「一个 prompt 模板」。这是「消息（message）」语义而非「提示（prompt）」语义——因为 OpenClaw 的 agent 是有会话（session）的，你发的是会话中的一条消息。

**新手会踩什么坑**
1. **两个都写错，且分不清错在哪** → 跑 `openclaw chat ...` 得到「无此子命令」，改成 `openclaw agent ... --prompt ...` 得到「未知参数」。新手往往在第一次报错后就放弃了，不知道还有一个 flag 也要改。
2. **把 `agent` 当成 `agents` 的缩写** → 以为 `openclaw agent list` 也能用。实际上 `list` 在复数族里（`openclaw agents list`），单数族不接注册表管理动作。
3. **shell 引号问题** → `--message` 后面带空格的中文必须加引号，否则 shell 拆词。这条与命令真伪无关，但在本命令上翻车率极高（参见 F1 的中文引号小节）。
4. **以为这是一条「聊天式」命令** → `openclaw agent --agent X --message Y` 是**单次非交互调用**（一发一收），不是进入 REPL。想要交互式界面是另外的入口。

**相关 FAQ**：F1-环境与安装 · F4-记忆与会话
**相关 Cookbook**：C7-生产运维

---

#### #4 虚构：`openclaw agents health-check` ｜ 真名：`openclaw health` / `openclaw doctor`

**错误形态**
```bash
openclaw agents health-check            # ❌
openclaw agents health                  # ❌
openclaw health-check                   # ❌
```

**正确形态**
```bash
openclaw health                         # ✅ 健康检查
openclaw doctor                         # ✅ 健康检查 / 诊断
```

**为什么网上会流传**
两层原因：

- **挂载点幻觉**：模型知道 `openclaw agents` 能 `list` / `bind`，就以为「健康检查」也是 `agents` 家族的一个子命令。但本机实测 `openclaw agents` 的子命令只有 `add · bind · bindings · delete · list` 五个，**没有 health-check**。
- **命名幻觉**：`health-check` 是 K8s / docker-compose / AWS ELB 里的标准术语（`livenessProbe`、`healthcheck:`），模型非常熟。OpenClaw 选了两个更短、更「拟人」的词：`health`（状态）和 `doctor`（诊断）。**`doctor` 这个词的选择尤其反直觉**——它在 `brew doctor`、`flutter doctor`、`npm doctor` 里出现过，但在那些语境下 `doctor` 是唯一的健康检查入口；模型不太会把 `health` 和 `doctor` 记成同一件事的两个别名。

**新手会踩什么坑**
1. **排障时找不到入口** → 出问题第一反应是查健康，搜到的词全是 `health-check`，跑不通就转而怀疑环境。这是最常见的「排障起点失败」。
2. **不知道有两个入口、用途有别** → `health` 与 `doctor` 是**同族但侧重不同**的两个命令：前者偏「当前状态读数」，后者偏「诊断与建议」。初学者只记住一个，做体检时拿不到完整视图。（⚠️ 本机实测时 `openclaw health` 的完整输出**被 Gateway state 库的独占锁遮挡**，见 §5。本文件不伪造其输出内容。）
3. **在脚本里解析 `health` 输出** → 因为完整输出未实测，脚本解析其格式有风险。建议改用明确存在的注册表命令（如 `openclaw agents list`、`openclaw automations list`）做机器可读判断。

**相关 FAQ**：F1 · F3-心跳与定时 · F7-治理漂移体检
**相关 SOP**：SOP-3 心跳监控

---

#### #5 虚构：`openclaw agents archive` ｜ 真名：`openclaw backup create`

**错误形态**
```bash
openclaw agents archive my-agent          # ❌
openclaw agents backup                    # ❌
```

**正确形态**
```bash
openclaw backup create                    # ✅ 归档 / 备份
```

**为什么网上会流传**
「归档（archive）」在模型的世界里是一个极其自然的动词——GitHub 有 Archive repo、Jira 有 Archive project、Slack 有 Archive channel。所以当模型需要表达「把某个 agent 收起来」时，`archive` 是首选词，而且它直觉上应该挂在 `agents` 族下（因为被归档的是 agent）。**真实设计是：OpenClaw 不做「单 agent 归档」，只有「整仓备份」。** 备份是一个独立的顶层命令族 `backup`，与 `agents` 平级。

**新手会踩什么坑**
1. **对「归档」的粒度预期错误** → 新手以为能挑一个 agent 归档，实际只能整仓备份。这个预期差会让人反复尝试 `agents archive --name X` 之类的变体。
2. **用 `delete` 替代「归档」** → 最危险的坑。`openclaw agents delete` 是真命令，但它是**删除注册表 entry**，不是归档。想「先归档再删」的人如果归档命令跑不通，很可能直接 `delete`，而**没有备份**。请先 `openclaw backup create`。
3. **以为归档会自动发生** → 生产事故复盘（案例库 01-real-incidents）里反复出现「改配置前没备份」。备份是显式动作，不会自动触发。
4. **找不到备份文件** → 备份落盘位置与恢复流程不在本文件范围内（见 02-config-reference 与 SOP-6）；但**记住入口是 `openclaw backup create`** 这一点已经解决 80% 的排障。

**相关 FAQ**：F7-治理漂移体检
**相关 SOP**：SOP-6 事故恢复

---

#### #6 虚构：`openclaw plugin`（单数） ｜ 真名：`openclaw plugins`（复数）

**错误形态**
```bash
openclaw plugin list                       # ❌
openclaw plugin install foo                # ❌
```

**正确形态**
```bash
openclaw plugins list                      # ✅
openclaw plugins ...                       # ✅（15 子命令，具体名见 §2.7 · ⏳）
```

**为什么网上会流传**
纯单复数记忆问题。模型在「名词指代一个系统时用单数」的倾向上非常强（`openclaw plugin system`、`openclaw plugin manager`），于是写成 `plugin`。而 OpenClaw 的所有「集合管理」命令族都用了复数：`agents`（复数）、`plugins`（复数）、`automations`（复数）、`promos`（复数）。**单数留给「对一个实例做动作」**：`agent`（单数）、`plugin`… 等等，`plugin` 单数并不存在，这也是个例外。总之：**没实测就不要猜单复数**。

**新手会踩什么坑**
1. **看不到插件列表就以为插件没装** → 跑 `openclaw plugin list` 失败 → 结论「插件系统没启用」。实际本机实测是 **53/73 enabled**（早期实测 51/69），插件系统完全在工作。
2. **误判某个插件状态** → 例如 `a2a` 插件在本机是 **disabled**（路径 `stock:a2a/index.js`）。看不到列表的人无法发现这一点，会在 A2A（Agent-to-Agent）联调时浪费大量时间。参见 chapters/10-A2A绑定。
3. **改用 `openclaw extensions`** → 另一个常见跑偏。`extensions` 是**目录名**（`~/.openclaw/extensions/`，本机实测**不存在**，说明未装自定义插件），不是命令名。
4. **以为 `plugins` 归 `config` 管** → 插件启用状态虽然会影响配置，但管理入口是 `openclaw plugins`，不是 `openclaw config`。

**相关 FAQ**：F5-Skills-Tools-MCP
**相关 Cookbook**：C3-Skills/Tools/MCP

---

#### #7 虚构：`manifest.yaml` ｜ 真名：`openclaw.plugin.json`（JSON5）

**错误形态**
```
~/.openclaw/extensions/my-plugin/manifest.yaml     # ❌ 文件名与格式都错
~/.openclaw/extensions/my-plugin/plugin.yaml       # ❌
```

**正确形态**
```
~/.openclaw/extensions/my-plugin/openclaw.plugin.json      # ✅ 注意：内容可以是 JSON5
```

**为什么网上会流传**
这不是「命令」幻觉，而是**文件清单（manifest）惯例**幻觉，危害同样大：

- **文件名**：模型对「插件清单」的默认文件名有三套强先验——`manifest.json`（Web App Manifest）、`plugin.json`（VS Code 早期）、`manifest.yaml`（K8s、Ansible、Home Assistant）。OpenClaw 用的是 **`openclaw.plugin.json`**——带命名空间前缀、点号分隔（类似 `openclaw.config.json` 的风格）。这个命名在训练语料里几乎不存在。
- **格式**：模型默认 JSON **严格模式**（无注释、无尾逗号）。而 OpenClaw 的这个文件是 **JSON5**——允许注释、尾逗号、单引号。**JSON5 与 JSON 的差异，是新手在写清单时最高频的翻车点**：用严格 JSON 的思维去写，本该能跑的东西被自己写死；反过来，照抄了带注释的示例、却用 `jq` 去解析，也会失败。

**新手会踩什么坑**
1. **写了 `manifest.yaml` 后插件永不加载** → 而且**没有任何报错**。加载器按固定文件名找，找不到就跳过。静默失败是这里最恶劣的特性。
2. **拿 `jq` / `python -m json.tool` 去校验 JSON5 文件** → 报语法错，于是新手去「修」本来正确的文件，把注释删掉、逗号补上，反而可能改错。校验 JSON5 要用支持 JSON5 的解析器。
3. **路径也错** → 清单必须放在 `~/.openclaw/extensions/<plugin-name>/` 下，**不是** `~/.openclaw/workspace/`，也不是 `~/.openclaw/plugins/`。本机实测 `~/.openclaw/extensions/` 目录**不存在**（未装自定义 plugin），所以这个坑在本机是个「未来坑」。
4. **把清单名与主配置名搞混** → 主配置是 `~/.openclaw/openclaw.json`（第 #8 条），插件清单是 `openclaw.plugin.json`。两者都叫「openclaw 点什么点 json」，新手极易互换。

**参考**：chapters/11-plugin-entrypoint/openclaw.plugin.json
**相关 FAQ**：F5-Skills-Tools-MCP
**相关 Cookbook**：C3-Skills/Tools/MCP

---

#### #8 虚构：`~/.openclaw/workspace/openclaw.json` ｜ 真名：`~/.openclaw/openclaw.json`

**错误形态**
```bash
cat ~/.openclaw/workspace/openclaw.json        # ❌ 文件不存在
vim ~/.openclaw/workspace/openclaw.json        # ❌ 会新建空文件，污染目录
```

**正确形态**
```bash
cat ~/.openclaw/openclaw.json                  # ✅ 主配置真身
```

**为什么网上会流传**
「workspace」这个词的引力太强。`~/.openclaw/workspace/` 是本机的**工作区根目录**（本机实测该目录下有 236 个 skill 目录、agents/ 等），活跃度极高，模型很自然地把「主配置」也塞进 workspace 下。加上「配置放在项目根 = 放在工作目录」是 web 框架的普遍习惯（`package.json`、`pyproject.toml` 都在项目根）。

**实测证据（✅）**：

| 路径 | 状态 |
|---|---|
| `~/.openclaw/openclaw.json` | **存在**（45,662 字节；早期实测 45,445 字节，两者均曾观测到） |
| `~/.openclaw/workspace/openclaw.json` | **不存在**（已 `ls` 确认） |

**新手会踩什么坑**
1. **用 `vim` 打开不存在的路径 → 创建了一个空配置** → 之后再跑 `ls ~/.openclaw/workspace/`，看到 `openclaw.json` 存在，便确信「配置在这里，而且可能是坏的」，排查方向彻底跑偏。
2. **改了错文件，改完不生效** → 最经典的坑。改了 workspace 下的空文件，重启 Gateway，行为无变化；然后怀疑「配置不热加载」「重启没生效」。
3. **备份脚本备份了错文件** → 备份命令跑得好好地，但恢复时恢复的是空文件。生产事故里这类「备份成功但备份错对象」的案例极难发现。
4. **配置体积误判** → 新手看主配置 45 KB 会以为「太大」，试图拆分。不要拆——顶层 key 数是确定的 **20 个**（✅ 实测），拆分只会破坏加载。

**补充 · 20 个顶层 key（✅ 实测）**
`acp` · `agents` · `auth` · `bindings` · `browser` · `channels` · `commands` · `env` · `gateway` · `logging` · `memory` · `messages` · `meta` · `models` · `plugins` · `session` · `skills` · `talk` · `tools` · `wizard`

**补充 · 5 个不存在的顶层字段（🚨 早期版本误称）**
`runtime` · `workspace` · `routing` · `heartbeat` · `subagents`

**真实路径在子层级**：
- `agents.entries.<id>.heartbeat.every`（心跳频率）
- `agents.entries.<id>.groupChat.mentionPatterns`（提及模式）
- `channels.feishu.requireMention`（飞书需 @）
- `channels.feishu.groupAllowFrom`（群白名单）

**相关 FAQ**：F2-协议-SOUL-AGENTS-USER
**相关 SOP**：SOP-2 协议配置

---

#### #9 虚构：`openclaw cron add --schedule X --target Y --prompt Z` ｜ 真名：`openclaw cron add --cron X --session Y --message Z`

**错误形态**
```bash
openclaw cron add --schedule "0 9 * * *" --target telegram --prompt "早安"    # ❌ 三个 flag 全错
```

**正确形态**
```bash
openclaw cron add --cron "<cron 表达式>" --session <session> --message "<消息>"  # ✅
```

**为什么网上会流传**
三个 flag 各自撞上了不同领域的标准词：

| 虚构 flag | 撞的是谁的惯例 | OpenClaw 真名 |
|---|---|---|
| `--schedule` | GitHub Actions（`on.schedule`）、K8s CronJob（`schedule:`）、Airflow（`schedule_interval`） | `--cron` |
| `--target` | Makefile / systemd / 消息队列的「投递目标」语义 | `--session` |
| `--prompt` | 同 #3，LLM SDK 通用词 | `--message` |

**OpenClaw 的选择有内在一致性**：它不用「投递目标（target）」而用**「会话（session）」**——因为定时任务的本质是「到点往某个会话里发一条消息」，而不是「把某个 payload 投到某个 endpoint」。同理，`--message` 与 #3 的 `openclaw agent --message` 是一致的：**OpenClaw 全家统一用「消息」语义，不用「提示」语义**。这个一致性一旦看穿，你就再也不会写错了。

**新手会踩什么坑**
1. **以为 cron 表达式格式不同** → `--cron` 后面仍是标准 cron 表达式（5 字段），不是自定义 DSL。别因为 flag 名怪就以为表达式也怪。
2. **`--session` 填错对象** → 新手常把 `--session` 填成「agent 名」，但在 OpenClaw 里 session 与 agent 不是一回事（本机实测配置里 `session` 顶层 key 仅含 `dmScope: per-channel-peer`，说明 session 是一套**作用域（scope）**机制）。`--session` 到底接受什么取值，⚠️ 本文件**不做断言**——真实验证需要实跑 `openclaw cron add`，而底稿明确要求避免污染本机已有的 **61 条 automations**，故标注 ⏳，见 §2.10 与 §5。
3. **`automations` 与 `cron` 两个族分不清** → 本机**同时存在** `openclaw cron`（定时任务）与 `openclaw automations`（自动化，实测 **61 条**，含 heartbeat、暗夜熔炉 cron、skill-collection-review 等）。新手容易在错误的族里找子命令。看 §2.4 与 §2.10 的区别表。
4. **加了定时任务但在列表里找不到** → 见 #4 的同类坑：`openclaw automations list` 看的是 automations 库，`openclaw cron add` 加的条目落在哪里、是否出现在 `automations list`，⚠️ 未实测，标 ⏳。
5. **重复注册** → 反复试错会留下多条同义定时任务。本机已有 61 条，其中就包含多条 heartbeat（`heartbeat:tiance` / `heartbeat:kunlun` / `heartbeat:peter`），说明这类条目极易堆积。

**相关 FAQ**：F3-心跳与定时
**相关 Cookbook**：C2-协议 HEARTBEAT/MEMORY
**相关 SOP**：SOP-3 心跳监控

---

### 1.4 自检清单 · 命令名合法性三问

在把任何 OpenClaw 命令粘进终端之前，顺序过三问：

**问 1 · 这个命令族（第一级子命令）在 §2 的 14 个族里吗？**
`setup/onboard` · `agents` · `agent` · `automations` · `mcp` · `acp` · `plugins` · `backup` · `health` · `doctor` · `cron` · `config` · `audit` · `pairing` · `promos` · `proxy`
→ 不在 → **大概率是幻觉**，回 §1.2 表查。

**问 2 · 单复数对吗？**
- 管**集合/注册表** → 复数：`agents` / `plugins` / `automations` / `promos`
- 对**单个实例做一次动作** → 单数：`agent`
→ 拿不准 → **不要猜**，跑 `openclaw <族> --help` 看子命令列表（这是唯一被允许的 `--help` 用法：验证你自己要跑的那一条，不是全量采集）。

**问 3 · flag 名有没有出现在 §1.2 的左边那列？**
`--prompt` · `--schedule` · `--target` · `--dir` → **全是虚构**。
真名对照：`--message` · `--cron` · `--session` · `--workspace`。

**三问全过 → 可以跑。有一问不过 → 先查表，别跑。**

### 1.5 一句话总结

> **OpenClaw 的 CLI 不说英语直觉，它说自己的话。**
> `setup` 不是 `init`；`add` 不是 `create`；`agent` 不是 `chat`；`--message` 不是 `--prompt`；`--cron` 不是 `--schedule`；`plugins` 不是 `plugin`；`backup` 不是 `archive`；配置在 `~/.openclaw/` 不在 `~/.openclaw/workspace/`。

---
# §2 命令族完整参考

> **本章约定**
> - ✅ = 2026-09-27/28 实机采集确认；⏳ = 未实测，本文件不为正确性背书（详见 §5）
> - 所有示例均以 `~` = `/Users/peterqiu` 为例
> - **术语双写**：智能体集群（军团 / Agent Fleet）· Supervisor Layer（监军）· SLCP（原 ACP）
> - flag 名凡未实测者，一律写 `<...>` 占位并标 ⏳，**绝不编造**

## 2.0 命令族总览（14 族）

| # | 命令族 | 用途 | 子命令 | 实测状态 |
|---|---|---|---|---|
| 2.1 | `setup` / `onboard` | 初始化向导 | 向导式（非固定子命令） | ✅ 存在 |
| 2.2 | `agents` | agent 注册表管理 | `add` · `bind` · `bindings` · `delete` · `list` | ✅ 全 5 个 |
| 2.3 | `agent` | 向单个 agent 发消息 | —（靠 flag） | ✅ 存在 |
| 2.4 | `automations` | 自动化编排 | `list`（+ 其他 ⏳） | ✅ `list` |
| 2.5 | `mcp` | MCP 服务器管理 | 14 子命令（名 ⏳） | ✅ 计数 |
| 2.6 | `acp` | ACP（Zed）桥接 | —（桥接进程） | ✅ 存在 |
| 2.7 | `plugins` | 插件管理 | 15 子命令（名 ⏳） | ✅ 计数 |
| 2.8 | `backup` | 整仓备份 | `create` | ✅ 存在 |
| 2.9 | `health` / `doctor` | 健康检查 / 诊断 | — | ✅ 存在 |
| 2.10 | `cron` | 定时任务 | `add`（`--cron`/`--session`/`--message`） | ✅ flag 名 |
| 2.11 | `config` / `audit` | 配置读写 / 审计 | — | ✅ 存在 |
| 2.12 | `pairing` | Secure DM pairing | — | ✅ 存在 |
| 2.13 | `promos` | ClawHub 促销领取 | — | ✅ 存在 |
| 2.14 | `proxy` | 代理 | — | ✅ 存在 |

**⚠️ 反例警告**：本表**没有** `openclaw init` / `openclaw chat` / `openclaw plugin`（单数）/ `openclaw runtime` / `openclaw heartbeat` / `openclaw subagents` / `openclaw routing`。见 §1.2。

---

## 2.1 `openclaw setup` / `openclaw onboard`

### `openclaw setup`

**语法**
```bash
openclaw setup [<flag>...]
```

**用途**
OpenClaw 的**初始化向导（setup wizard）**入口。用于首次安装后的环境引导：写主配置、选模型 provider、配渠道等。**这是 `openclaw init` 的真身**（✅ 实测存在）。

**参数**
| 参数 | 必填 | 说明 |
|---|---|---|
| `<无位置参数>` | — | 本命令是向导式交互入口，不接位置参数 ⏳（是否有位置参数未实测） |

**选项**
| 选项 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | **未实测**。本文件不列出任何 `setup` 的 flag 名 |

> ⚠️ **诚实说明**：`openclaw setup` 的完整 flag 清单**未在本机采集**。底稿只确认该命令族**存在**（与 `onboard` 并列）。任何列出 `--yes` / `--provider` / `--token` 之类的写法均为**未经实测的推测**，请自行以 `openclaw setup --help` 为准。

**示例**
```bash
openclaw setup
```

**期望输出**
交互式向导（逐项提问 → 写配置）。⚠️ 逐字输出未实测。

**真名陷阱**：❌ 不是 `openclaw init`
**相关 FAQ**：F1-环境与安装
**相关 SOP**：SOP-1 环境搭建
**相关 Cookbook**：—

---

### `openclaw onboard`

**语法**
```bash
openclaw onboard [<flag>...]
```

**用途**
与 `setup` 同族的**初始化 / 上手指引**入口（✅ 实测存在）。语义上「onboard」更偏「带你入门」，`setup` 更偏「装配环境」；两者在实现上是否共享同一份向导代码，⚠️ 未实测。

**参数** / **选项**
| 参数 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | 未实测 |

**示例**
```bash
openclaw onboard
```

**期望输出**
向导式引导。⚠️ 未实测逐字输出。

**真名陷阱**：❌ 不是 `openclaw init`
**相关 FAQ**：F1-环境与安装
**相关 SOP**：SOP-1 环境搭建

---

### 2.1.x 初始化前必读：主配置真身路径

初始化产出的主配置落在：

```
~/.openclaw/openclaw.json          # ✅ 真身（45,662 字节 · 早期实测 45,445）
~/.openclaw/workspace/openclaw.json # ❌ 不存在（已 ls 确认）
```

**20 个顶层 key（✅ 实测）**
`acp` · `agents` · `auth` · `bindings` · `browser` · `channels` · `commands` · `env` · `gateway` · `logging` · `memory` · `messages` · `meta` · `models` · `plugins` · `session` · `skills` · `talk` · `tools` · `wizard`

**5 个不存在的顶层字段（🚨）**：`runtime` · `workspace` · `routing` · `heartbeat` · `subagents`

**⚠️ 初始化后必做**：立刻 `openclaw backup create` 留一份干净基线。本机事故史（`~/.openclaw/workspace/agents/workspace-kunlun/memory/2026-08-19-军团断线修复.md`，见案例库 01）里，正是靠一份 `openclaw.json.bak.pre-fix-2026-08-19-0921` 才完成回滚。见 SOP-1 与 SOP-6。

---

## 2.2 `openclaw agents`

> **命令族定位**：管理 **agent 注册表**（本机实测 `agents.entries` 含 **18 个 agent**）。

**已实测子命令（✅ 全表）**
```
add · bind · bindings · delete · list
```

**🚨 不存在的子命令**：`create` · `health-check` · `archive` · `update` · `rename`

### 2.2.1 `openclaw agents list`

**语法**
```bash
openclaw agents list [<flag>...]
```

**用途**
列出注册表中的全部 agent。**这是判断「agent 建没建成」的唯一权威方式**（不是 `ls` 目录）。

**参数**
| 参数 | 必填 | 说明 |
|---|---|---|
| `<无>` | — | 无位置参数 ⏳（未实测是否有过滤位置参数） |

**选项**
| 选项 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | 未实测（如 `--json` / `--verbose` 之类未经实测，**不列**） |

**示例**
```bash
openclaw agents list
```

**期望输出（本机实况 · ✅）**
- **18 个 agent**（对应 `agents.entries` 的 18 个键）
- 主模型分布：

| 主模型 | 数量 |
|---|---|
| `opus-4-8` | 9 |
| `gpt-5.6-sol` | 4 |
| `gpt-5.5` | 2 |
| `gpt-5.6-terra` | 2 |
| `deepseek-v4-flash` | 1 |
| **合计** | **18** |

> ⚠️ **诚实说明**：上表是**统计口径**的实测结果（主模型分布），不是 `agents list` 的逐行原始输出。逐行格式未在本文件伪造。要拿到逐行原始文本，请自行跑一次。

**真名陷阱**：❌ 不是 `openclaw agents ls` · ❌ 不是 `openclaw list agents`
**相关 FAQ**：F6-多Agent协同
**相关 Cookbook**：C6-协同舰队

---

### 2.2.2 `openclaw agents add`

**语法**
```bash
openclaw agents add <name> --workspace <dir>
```

**用途**
往 agent 注册表里**新增一个 agent entry**，并指定其 workspace 目录。**这是 `openclaw agents create X` 的真身**（✅ 实测）。

**参数**
| 参数 | 必填 | 说明 |
|---|---|---|
| `<name>` | ✅ 必填 | agent 名称/ID。会作为 `agents.entries` 的键 |
| `--workspace <dir>` | ✅ 必填 | agent 的 workspace 目录（本机惯例 `~/.openclaw/workspace/agents/<name>`） |

**选项**
| 选项 | 必填 | 说明 |
|---|---|---|
| `--workspace <dir>` | ✅ | 唯一被底稿确证的选项 |
| ⏳ | — | 其他 flag（如模型覆盖、心跳）**未实测**，不列 |

**示例**
```bash
openclaw agents add my-agent --workspace ~/.openclaw/workspace/agents/my-agent
```

**期望输出**
命令成功 → 注册表新增一键。**验证方式**：
```bash
openclaw agents list        # ✅ 应能在列表里看到 my-agent
```
⚠️ 逐字输出未实测。

**真名陷阱**
- ❌ 不是 `openclaw agents create`
- ❌ 不是 `openclaw agents new`
- ❌ flag 不是 `--dir`（真名是 `--workspace`）

**新手坑（重复强调，因为代价高）**
1. 建完只用 `ls` 看目录、不跑 `agents list` → 注册表没落，白忙
2. 建完以为渠道自动绑好 → 没有任何渠道会绑，必须另跑 `bind`（见 2.2.3）
3. 想「下线」时去搜 `archive`（不存在）→ 转而用 `rm -rf`，留下悬挂键

**相关 FAQ**：F6-多Agent协同
**相关 Cookbook**：C6-协同舰队

---

### 2.2.3 `openclaw agents bind`

**语法**
```bash
openclaw agents bind <...>          # ⚠️ 精确参数形态未实测
```

**用途**
建立 **agent ↔ 渠道（channel）绑定（binding）**。本机实测绑定总数为 **37 条**：**Telegram 19 + 飞书 18**。

**参数**
| 参数 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | **精确参数形态未实测**（底稿仅确认子命令名 `bind` 存在） |

**选项**
| 选项 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | 未实测 |

**示例**
```bash
# ⚠️ 以下为形态示意，flag 名未经实测 —— 请以 openclaw agents bind --help 为准
openclaw agents bind <agent> <channel>        # ⏳ 待实测
```

**期望输出**
一条新 binding 落盘。**验证方式**：
```bash
openclaw agents bindings      # ✅ 计数应 +1
```

**本机实况参考值（✅）**
| 渠道 | binding 数 |
|---|---|
| Telegram | 19 |
| 飞书（Feishu） | 18 |
| **合计** | **37** |

**真名陷阱**：❌ 无 `bind` 的别名（不存在 `link` / `attach` 子命令）
**相关 FAQ**：F2-协议-SOUL-AGENTS-USER · F6-多Agent协同
**相关 SOP**：SOP-2 协议配置

---

### 2.2.4 `openclaw agents bindings`

**语法**
```bash
openclaw agents bindings [<flag>...]
```

**用途**
**列出全部渠道绑定**。注意与 `bind`（写）配对的这是 `bindings`（读）。**复数 + s 的是读，没有 s 的是写**——和 `add` 不一样，这一对是可推的。✅ 实测存在。

**参数** / **选项**
| 参数 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | 未实测 |

**示例**
```bash
openclaw agents bindings
```

**期望输出（本机实况 · ✅）**
- **37 条 binding**：Telegram **19** + 飞书 **18**
- 飞书侧共 **18 个账号**（`channels.feishu` 下 18 账号）

**与配置文件的对应关系（✅）**
- 顶层 key `bindings` 是 **list，37 项** ← 这是同一个数据的另一面
- 顶层 key `channels` 是 dict，含 `feishu`（18 账号）

**真名陷阱**：❌ 不是 `openclaw agents binding`（单数）
**相关 FAQ**：F6-多Agent协同 · F2-协议
**相关 Cookbook**：C6-协同舰队

---

### 2.2.5 `openclaw agents delete`

**语法**
```bash
openclaw agents delete <name>          # ⚠️ 精确参数形态未实测（位置参数 vs flag）
```

**用途**
从注册表**删除一个 agent entry**。⚠️ **这不是「归档」**。「归档」走 `openclaw backup create`（见 #5 与 §2.8）。

**参数**
| 参数 | 必填 | 说明 |
|---|---|---|
| `<name>` ⏳ | 推断必填 | 具体是位置参数还是 `--name` flag，**未实测** |

**选项**
| 选项 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | 未实测（`--yes` / `--force` 之类不列） |

**示例**
```bash
# ⚠️ 危险操作 · 先备份
openclaw backup create
openclaw agents delete my-agent        # ⏳ 参数形态待实测
```

**期望输出**
注册表少一键。验证：
```bash
openclaw agents list        # 从 18 变 17
```

**⚠️ 安全提示（强烈建议）**
1. **删之前必先 `openclaw backup create`**。删除是否可撤销，⚠️ 未实测 —— 按不可撤销对待。
2. **删除 entry 不等删目录**。`agents.entries` 的键与 `~/.openclaw/workspace/agents/<name>` 目录是否联动，⚠️ 未实测。若只删 entry 留目录，会形成「孤儿 workspace」。
3. **删 entry 前先看它有没有 binding** → `openclaw agents bindings`。删掉仍有 binding 的 agent，可能留下**指向空 target 的绑定**，导致该渠道静默不响应。

**真名陷阱**：❌ 不是 `openclaw agents remove` · ❌ 不是 `openclaw agents archive`
**相关 FAQ**：F6-多Agent协同 · F7-治理漂移体检
**相关 SOP**：SOP-6 事故恢复

---

### 2.2.6 `agents` 族自检流程（推荐顺序）

```bash
# 1) 看现状
openclaw agents list
openclaw agents bindings

# 2) 加一个
openclaw agents add my-agent --workspace ~/.openclaw/workspace/agents/my-agent

# 3) 复核（必须）
openclaw agents list

# 4) 绑渠道
openclaw agents bind <agent> <channel>       # ⏳ 参数形态待实测
openclaw agents bindings                     # 计数应 +1

# 5) 冒烟测试
openclaw agent --agent my-agent --message "ping"
```

---

## 2.3 `openclaw agent`（单数）

> **命令族定位**：**对单个 agent 做一次调用**。注意与 `agents`（复数，注册表管理）的区别——这是全书最高频的单复数陷阱。

### `openclaw agent`

**语法**
```bash
openclaw agent --agent <name> --message <text>
```

**用途**
向指定 agent 发送**一条消息**并拿到回复。**这是 `openclaw chat --agent X --prompt Y` 的真身**（✅ 实测）。

**参数**
| 参数 | 必填 | 说明 |
|---|---|---|
| `<无位置参数>` ⏳ | — | 参数通过 flag 传；是否有位置参数形式未实测 |

**选项**
| 选项 | 必填 | 说明 |
|---|---|---|
| `--agent <name>` | ✅ 必填 | 目标 agent 名（对应 `agents.entries` 的键） |
| `--message <text>` | ✅ 必填 | 要发送的消息正文。（真名 **不是** `--prompt`） |
| ⏳ | — | 其他 flag（如 `--session` / `--json`）未实测，不列 |

**示例**
```bash
openclaw agent --agent tiance --message "今天军团状态如何？"
```

**期望输出**
该 agent 对该消息的一次回复。⚠️ 逐字输出格式未实测（依赖该 agent 的模型与协议）。

**真名陷阱（三重）**
- ❌ 不是 `openclaw chat`
- ❌ 不是 `--prompt`（真名 `--message`）
- ❌ 不是 `openclaw agents`（单数才对）

**新手坑**
1. **以为会进 REPL** → 这是**单次调用**，不是交互式聊天界面。
2. **中文不加引号被拆词** → `--message 今天好吗` → shell 拆成 `--message` + `今天` 等；中文内容**务必加双引号**。
3. **agent 名写成渠道名** → `--agent telegram` 之类会失败；`--agent` 要的是 agent 名。
4. **两个 flag 都要给** → 只给 `--message` 不给 `--agent`（或反之）→ 报参数缺失。

**相关 FAQ**：F1-环境与安装 · F4-记忆与会话
**相关 Cookbook**：C7-生产运维

---

### 2.3.x `agent` vs `agents` 一图速记

| 我想做 | 用哪个 | 命令 |
|---|---|---|
| 看有哪些 agent | **复数** | `openclaw agents list` |
| 建一个 agent | **复数** | `openclaw agents add X --workspace D` |
| 绑/看绑定 | **复数** | `openclaw agents bind` / `bindings` |
| 删一个 agent | **复数** | `openclaw agents delete X` |
| **跟一个 agent 说句话** | **单数** | `openclaw agent --agent X --message Y` |

**记忆口诀**：**管「有哪些」用复数，跟「某一个」说话用单数。**

---

## 2.4 `openclaw automations`

> **命令族定位**：自动化编排。本机实测 **61 条 automations**（早期实测 43 条，两次均曾观测到）。

**已实测子命令（✅）**：`list`（底稿明确）
**其他子命令**：⏳ **未实测**（如 `add` / `run` / `enable` / `disable` 之类**不做断言**）

> ⚠️ **为什么不实测 `automations add`**：本机已有 **61 条**编排在跑（含 13 个「暗夜熔炉」cron、18 个 `skill-collection-review`、3 条 heartbeat 等），实跑 `add` 会污染生产编排。底稿明确标注「避免污染 61 条编排」→ 本文件按纪律标 ⏳（见 §5）。

### 2.4.1 `openclaw automations list`

**语法**
```bash
openclaw automations list [<flag>...]
```

**用途**
列出全部已注册自动化。**这是排查「定时任务为什么没跑」的第一站。**

**参数** / **选项**
| 参数 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | 未实测（是否有 `--json` / `--all` 不列） |

**示例**
```bash
openclaw automations list
```

**期望输出（本机实况 · ✅ 61 条）**

条目形态（示例族）：

| 条目族 | 数量 | 备注 |
|---|---|---|
| 「暗夜熔炉」cron | 13 | 串行铺开 01:10 → 03:30 |
| `skill-collection-review` | 18 | — |
| 蜂鸟（Hummingbird） | 9 | — |
| 凤凰（Phoenix） | 4 | — |
| heartbeat | 3 | `heartbeat:tiance` · `heartbeat:kunlun` · `heartbeat:peter` |
| 其他单条 | — | `memory-core:memory-dreaming` · `蜂群-A-晨间全量扫描` · `hetu-回测进化日报` · `Peter 每日人生教练早课` · `军功爵周结算` · `能力矩阵月度更新` |
| **合计** | **61** | — |

**🚨 健康状态读数（本机实测 · 重要）**

| 条目 | 频率 | 状态 |
|---|---|---|
| `heartbeat:tiance` | every 30m | **skipped** |
| `heartbeat:kunlun` | every 30m | **error 99+ 次** |
| `heartbeat:peter` | every 2h | **error 70 次** |
| `能力矩阵月度更新` | — | **error 4 次** |

> **诚实说明**：这些状态值来自本机 `automations list` 的观测；「能力矩阵」条目对应的业务事故（2026-09-01 后 26 天无新记录 · cron `error(4x)`）见案例库 01-real-incidents 与 chapters/06-治理系统。

**真名陷阱**：⏳ 是否存在 `openclaw automations ls` 别名未实测
**相关 FAQ**：F3-心跳与定时 · F7-治理漂移体检
**相关 Cookbook**：C2-协议 HEARTBEAT/MEMORY · C5-漂移治理
**相关 SOP**：SOP-3 心跳监控

### 2.4.2 `automations` vs `cron` —— 两族的边界

本机**同时存在** `openclaw automations` 与 `openclaw cron`（✅ 实测）。二者的分工：

| 维度 | `automations` | `cron` |
|---|---|---|
| 观察到的用途 | 编排库总览（61 条） | 新增定时任务 |
| 已实测入口 | `list` | `add` |
| 条目来源 | 含 heartbeat / 业务 cron / 审查任务 | 新建条目 |
| 二者关系 | ⏳ 未实测（`cron add` 的条目是否出现在 `automations list` 中，**不做断言**） | ⏳ |

> ⚠️ **诚实边界**：不要假设「`cron add` 之后 `automations list` 必然能看到」。这一条**未实测**。

---

## 2.5 `openclaw mcp`

> **命令族定位**：MCP（Model Context Protocol）服务器管理。**14 子命令**（✅ 实测计数）。
> **命名空间**：`mcp.servers`（✅ 实测）
> **本机实况**：`openclaw mcp list` = **0 配置**（诚实基线 · 本机未接任何 MCP server）

### 2.5.1 `openclaw mcp` 子命令清单

| # | 子命令 | 状态 |
|---|---|---|
| 1–14 | ⏳ **具体名称待实测** | 底稿仅确认**总数 14**，未逐一记录名称 |

> 🚨 **纪律声明**：本节**不编造** 14 个子命令的名字。任何列出 `openclaw mcp add` / `remove` / `enable` / `call` / `auth` / `tools` 之类的清单，若未经实跑确认，均为**推测**。
>
> **正确做法**：需要具体子命令名时，跑一次
> ```bash
> openclaw mcp --help
> ```
> 这是被允许的 `--help` 用法（验证你自己要跑的那一条）。

### 2.5.2 `openclaw mcp list`

**语法**
```bash
openclaw mcp list
```

**用途**
列出已注册的 MCP 服务器。

**示例**
```bash
openclaw mcp list
```

**期望输出（本机实况 · ✅）**
```
0 配置
```
**解读**：本机未接任何 MCP server。这是一个**诚实基线**——不是命令坏了，而是确实没配。

**新手坑**
1. **看到 0 条以为命令失败** → 不是失败，是真空。MCP 是**按需接入**的，本手册的对位章节是 chapters/09-MCP绑定。
2. **把 `mcp.servers` 写到错的层级** → 命名空间是 **`mcp.servers`**（✅）。不要写成 `mcpServers`（VS Code / Cline 的写法）或顶层 `servers`。
3. **配了之后不去 `list` 复核** → 同所有其他族：写完必读。

**真名陷阱**：❌ 命名空间不是 `mcpServers`（那是 VS Code / Cline 风格）；真名是 **`mcp.servers`**
**相关 FAQ**：F5-Skills-Tools-MCP
**相关 Cookbook**：C3-Skills/Tools/MCP
**参考章节**：chapters/09-MCP绑定

### 2.5.3 MCP 接入前的自查（因为本机 0 配置）

```bash
# 1) 先看有没有
openclaw mcp list

# 2) 看有哪些子命令（唯一被允许的 --help 用法）
openclaw mcp --help            # 应从输出里数出 14 条

# 3) 按 FAQ F5 与 cookbook C3 的流程配置
# 4) 复核
openclaw mcp list              # 应 > 0
```

---
## 2.6 `openclaw acp`

> **命令族定位**：**Zed ACP bridge**（✅ 实测）。
> ⚠️ **三重撞名警告**：见下。

### `openclaw acp`

**语法**
```bash
openclaw acp [<flag>...]          # ⏳ flag 未实测
```

**用途**
启动 / 管理 **ACP（Agent Client Protocol）桥接**，用于与 **Zed 编辑器**对接（✅ 实测描述为「Zed ACP bridge」）。

**参数** / **选项**
| 参数 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | 未实测。本文件不列任何 flag 名 |

**示例**
```bash
openclaw acp
```

**期望输出**
启动一个桥接进程（stdio / socket）。⚠️ 逐字输出未实测。

### 🚨 2.6.1 三重撞名（全书必须讲清的一处概念陷阱）

「ACP」这三个字母在本手册的语境里有**三个完全不同的所指**：

| 层级 | 全称 | 含义 | 处理方式 |
|---|---|---|---|
| ① OpenClaw 命令 | `openclaw acp` = **Zed ACP bridge** | **Agent Client Protocol**，编辑器 ↔ agent 的客户端协议 | 保留 `acp` 命令名不变 |
| ② 旧内部黑话 | 本手册 v1.0 用「ACP」指代**军团协作协议** | 硅基生命之间的协作标准 | **v3.0 起改名 SLCP** |
| ③ 业界同名 | 其他项目也叫 ACP | 语境不在本手册内 | 引用时须注明来源 |

**改名结论（v3.0 改名表）**：

> **SLCP（原内部黑话「ACP」/ Silicon Life Collaboration Protocol）**

即：**凡是讲「军团协作协议」的地方，v3.0 起一律写 SLCP**；而**命令行 `openclaw acp` 仍叫 `acp`**（因为那是 OpenClaw 自己的命令名，不能改）。

**新手会踩什么坑**
1. **看文档里「ACP」以为是军团协议** → 跑到 `openclaw acp` 下面找军团编排功能，找不到。
2. **在 SLCP 文档里搜 `openclaw slcp`** → 命令不存在。SLCP 是协议名，不是命令名。
3. **把 Zed 的 ACP 与其他编辑器的 LSP 混淆** → ACP 是 agent 客户端协议，不是语言服务器协议。
4. **以为 `acp` 是常驻服务** → 它是**桥接**，通常由编辑器侧拉起，不是 `systemctl start acp` 那种常驻守护。

**真名陷阱**：❌ 不存在 `openclaw slcp` 命令（SLCP 是协议名）
**相关 FAQ**：F5-Skills-Tools-MCP · F6-多Agent协同
**相关 Cookbook**：C3-Skills/Tools/MCP
**参考章节**：chapters/02-七大契约

### 2.6.2 与 `acp` 顶层配置 key 的关系（✅）

主配置里 `acp` 是**第 1 个顶层 key**，类型 dict，**5 个子项**（✅ 实测）：

```
acp
├── (5 个子项)   # ⏳ 具体字段名未逐一实测
```

**方向指引**：需要配置细节请查 `api-reference/02-config-reference.md`（若已产出）或直接读 `~/.openclaw/openclaw.json` 的 `acp` 段。
⚠️ 本文件**不列** `acp` 的具体子字段名。

---

## 2.7 `openclaw plugins`

> **命令族定位**：插件管理。**15 子命令**（✅ 实测计数）。
> **本机实况**：**53/73 enabled**（live）· 早期实测 **51/69 enabled**

### 2.7.1 `openclaw plugins` 子命令清单

| # | 子命令 | 状态 |
|---|---|---|
| 1–15 | ⏳ **具体名称待实测** | 底稿仅确认**总数 15**，未逐一记录名称 |

> 🚨 **纪律声明**：本节**不编造** 15 个子命令的名字。常见推测（如 `install` / `uninstall` / `enable` / `disable` / `list` / `info` / `build` / `publish` …）**均未经实测**，本文件不列为事实。
>
> **正确做法**：跑一次 `openclaw plugins --help`（唯一被允许的 `--help` 用法），从输出里数出 15 条。

### 2.7.2 `openclaw plugins list`

**语法**
```bash
openclaw plugins list
```

**用途**
列出全部插件及其启用状态。**这是「哪些插件在跑」的唯一权威读法**（✅ 实测存在 `list`；本机实测输出形态为 `N/M enabled`）。

**示例**
```bash
openclaw plugins list
```

**期望输出（本机实况 · ✅）**

| 观测 | 值 |
|---|---|
| enabled / total（early） | **51 / 69** |
| enabled / total（live 复核） | **53 / 73** |
| **书内统一口径** | 见 §0.4 —— 用 2026.9.4 口径，但本机 live 复核为 53/73，**两者均如实标注** |

**关键条目（✅）**

| 插件 | 状态 | 路径 |
|---|---|---|
| `a2a` | **disabled** | `stock:a2a/index.js` |

> **为什么 `a2a` disabled 值得单独提**：A2A（Agent-to-Agent）是与本手册 chapters/10-A2A绑定 直接相关的插件。它在本机是**关闭**的。排查 A2A 不工作时，**第一步就该看 `plugins list` 里 `a2a` 是否 enabled**。

**与配置文件的对应（✅）**
- 顶层 key `plugins` 是 dict，**1 个子项**（✅ 实测）。即：插件**注册表本身在文件系统里**（`stock:` 前缀指向内置插件目录），配置文件里的 `plugins` 主要承载开关/参数覆盖。

**真名陷阱**
- ❌ 不是 `openclaw plugin`（单数）
- ❌ 不是 `openclaw extensions`（`extensions` 是目录名，不是命令）
- ❌ 不是 `openclaw plugin list`

**新手坑**
1. **`plugin` 单数 → 命令不存在 → 结论「插件系统坏了」**（见 §1.3 #6）
2. **以为 `~/.openclaw/extensions/` 一定存在** → 本机实测**该目录不存在**（未装自定义 plugin）。目录不存在 ≠ 插件系统不可用；内置插件走 `stock:` 路径。
3. **改了自定义插件但没生效** → 回到 §1.3 #7：清单文件名必须是 `openclaw.plugin.json`（JSON5），放 `~/.openclaw/extensions/<name>/`。名字错 = 静默不加载。

**相关 FAQ**：F5-Skills-Tools-MCP
**相关 Cookbook**：C3-Skills/Tools/MCP
**参考章节**：chapters/12-plugin-entrypoint

### 2.7.3 自定义插件落盘位置（✅ / ⏳ 分列）

| 路径 | 状态 |
|---|---|
| `~/.openclaw/extensions/` | ✅ 已确认**本机不存在**（未装自定义 plugin） |
| `~/.openclaw/extensions/<name>/openclaw.plugin.json` | ✅ 文件名为真名（**JSON5**） |
| 清单内容 schema | ⏳ 见 chapters/11-plugin-entrypoint/openclaw.plugin.json（书内有样例文件） |
| 全生命周期（install → 加载 → 卸载） | ⏳ **未实测**（底稿 §5 明列「`plugins install` 全生命周期」为待实测项） |
| ClawHub publish 流程 | ⏳ **未实测**（底稿 §5 明列） |

**⚠️ 边界**：本文件**不讲**插件安装与发布的完整流程，因为那是 ⏳ 待实测项。要写插件，看 chapters/12 与 官方 RFC 草案。

---

## 2.8 `openclaw backup`

> **命令族定位**：整仓备份 / 归档。**这是 `openclaw agents archive` 的真身**（✅ 实测存在 `create`）。

**已实测子命令（✅）**：`create`
**其他子命令**：⏳ 未实测（如 `list` / `restore` / `verify` 之类**不做断言**）

### `openclaw backup create`

**语法**
```bash
openclaw backup create [<flag>...]        # ⏳ flag 未实测
```

**用途**
创建一份 OpenClaw 的备份（配置 / 状态 / workspace）。**改配置前的强制前置动作。**

**参数** / **选项**
| 参数 | 必填 | 说明 |
|---|---|---|
| `<无位置参数>` ⏳ | — | 推断无位置参数 |
| ⏳ | — | flag（如输出路径、是否含 workspace）**未实测**，不列 |

**示例**
```bash
openclaw backup create
```

**期望输出**
生成一份备份（落盘路径 ⏳ 未实测）。本机事故史里出现过的人工备份命名惯例（**参考，非命令输出**）：

```
openclaw.json.bak.pre-fix-2026-08-19-0921
```

命名结构：`<文件>.bak.<阶段>-<YYYY-MM-DD>-<HHMM>`。**这是人工命名惯例，不是 `backup create` 的产物格式**（⚠️ 诚实区分）。

**真名陷阱**
- ❌ 不是 `openclaw agents archive`（无此子命令）
- ❌ 不是 `openclaw backup`（光杆命令无意义，要带 `create`）
- ❌ 不是 `openclaw backups create`（`backup` 是单数）

**新手坑**
1. **以为备份自动发生** → 不会。必须显式跑。
2. **改完才想起来备份** → 顺序必须**备份 → 改 → 复核**。
3. **不验证备份可用** → 生产事故里「备份成功但内容为空/错对象」很常见（见 §1.3 #8 第 3 点：备份脚本备份了 `~/.openclaw/workspace/openclaw.json` 这个不存在的路径）。
4. **把 `backup` 当「单 agent 归档」** → 粒度是**整仓**。

**相关 FAQ**：F7-治理漂移体检 · F1-环境与安装
**相关 SOP**：SOP-6 事故恢复（最相关）· SOP-1 环境搭建
**相关 Cookbook**：C5-漂移治理
**相关案例**：case-library/01-real-incidents（2026-08-19 军团断线修复 · 靠 `openclaw.json.bak.pre-fix-2026-08-19-0921` 回滚）

### 2.8.1 备份纪律（写进 SOP）

```bash
# 标准三步（务必按序）
openclaw backup create                    # 1. 备份
# ... 修改配置 / 增删 agent ...             # 2. 改
openclaw config <...>                     #    （或直接编辑 ~/.openclaw/openclaw.json）
openclaw agents list && openclaw health   # 3. 复核
```

> **历史教训（✅ 实读）**：2026-08-19 军团断线事故（根因：MiniMax-M3 空 body → 17-18 fallback 首位被占 → 轩辕 `primary == fallback[0]` 自循环）能恢复，靠的就是一份**改前备份**。见案例库 01-real-incidents。

---

## 2.9 `openclaw health` / `openclaw doctor`

> **命令族定位**：健康检查与诊断。**这是 `openclaw agents health-check` 的真身**（✅ 均实测存在）。

### 2.9.1 `openclaw health`

**语法**
```bash
openclaw health [<flag>...]        # ⏳ flag 未实测
```

**用途**
**当前状态读数**（健康检查）。

**参数** / **选项**
| 参数 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | 未实测 |

**示例**
```bash
openclaw health
```

**期望输出**
⚠️ **本机实测时，`openclaw health` 的完整输出被 Gateway state 库的独占锁遮挡**（✅ 如实记录）。

> 🚨 **诚实声明**：本文件**不伪造** `openclaw health` 的输出内容。它可能包含 gateway / bindings / automations 的汇总状态，但**具体格式与字段未经实测**。这是底稿 §5 明列的待实测项。

**可用的替代观测（本文件推荐）**
在 `health` 输出不可用时，用**确定存在的注册表命令**做机器可读判断：

```bash
openclaw agents list          # agent 数（本机 18）
openclaw agents bindings      # binding 数（本机 37）
openclaw automations list     # automation 数（本机 61）
openclaw plugins list         # enabled/total（本机 53/73）
openclaw mcp list             # MCP server 数（本机 0）
```

### 2.9.2 `openclaw doctor`

**语法**
```bash
openclaw doctor [<flag>...]        # ⏳ flag 未实测
```

**用途**
**诊断与建议**（doctor 语义，类 `brew doctor` / `flutter doctor`）。与 `health` 的区别：`health` 偏读数，`doctor` 偏诊断。

**参数** / **选项**：⏳ 未实测

**示例**
```bash
openclaw doctor
```

**期望输出**
诊断报告 + 建议项。⚠️ 逐字输出未实测。

**真名陷阱（三条全要背）**
- ❌ 不是 `openclaw agents health-check`
- ❌ 不是 `openclaw health-check`
- ❌ 不是 `openclaw agents health`

**新手坑**
1. **排障第一站跑错命令** → 见 §1.3 #4。
2. **`health` 输出被锁遮挡时以为环境坏了** → 这是本机实测遇到的**真实现象**；Gateway state 库有独占锁。此时改用 §2.9.1 的替代观测。
3. **只看 `health` 不看 `automations list`** → 心跳/定时出错在 `health` 里可能不显，但在 `automations list` 里明确有 `skipped` / `error 99+` / `error 70`（✅ 实测）。**排障一定要两个都看。**

**相关 FAQ**：F1-环境与安装 · F3-心跳与定时 · F7-治理漂移体检
**相关 SOP**：SOP-3 心跳监控 · SOP-6 事故恢复
**相关 Cookbook**：C7-生产运维

---

## 2.10 `openclaw cron`

> **命令族定位**：定时任务。**这是 `openclaw cron add --schedule X --target Y --prompt Z` 的真身**（✅ flag 名实测）。

**已实测子命令（✅）**：`add`
**其他子命令**：⏳ 未实测

### `openclaw cron add`

**语法**
```bash
openclaw cron add --cron <expr> --session <session> --message <text>
```

**用途**
注册一条定时任务：到点向指定**会话（session）**发送一条**消息（message）**。

**参数**
| 参数 | 必填 | 说明 |
|---|---|---|
| `<无位置参数>` ⏳ | — | 参数全部通过 flag 传 |

**选项**
| 选项 | 必填 | 说明 |
|---|---|---|
| `--cron <expr>` | ✅ 必填 | **cron 表达式**（Cron Expression）。真名 **不是** `--schedule` |
| `--session <session>` | ✅ 必填 | 目标**会话**。真名 **不是** `--target` ⏳（`--session` 的合法取值未实测） |
| `--message <text>` | ✅ 必填 | 到点发送的消息正文。真名 **不是** `--prompt` |
| ⏳ | — | 其他 flag 未实测，不列 |

**示例**
```bash
# ⚠️ 形态示意（--session 的合法取值 ⏳ 未实测，勿照抄生产）
openclaw cron add \
  --cron "0 9 * * *" \
  --session "<session 标识>" \
  --message "早安，请汇报今日计划"
```

**期望输出**
新增一条定时任务。⚠️ 条目落到哪个注册表（`cron` 自己的库 or `automations`）**未实测**，标 ⏳。

**真名陷阱（三个 flag 全要改）**

| ❌ 虚构 | ✅ 真名 |
|---|---|
| `--schedule` | `--cron` |
| `--target` | `--session` |
| `--prompt` | `--message` |

**新手坑**
1. **只改子命令不改 flag** → 最容易发生的半修状态（见 §1.3 #9）。
2. **`--session` 填成 agent 名** → agent ≠ session。session 在本机配置里是一套**作用域（scope）** 机制（顶层 `session` key 实测仅含 `dmScope: per-channel-peer`）。

   > ⚠️ 顺带纠一处常见误植：**`reserveTokensFloor` 不存在**。真实 Compaction 相关名如下：
   > | ❌ 误植 | ✅ 真名 |
   > |---|---|
   > | `reserveTokensFloor` | **不存在** → `CompactionRequestBudget.reserveTokens` |
   > | — | 常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25` |
   > | — | `effectiveReserveTokens` |
   >
   > **实测**：本机 `openclaw.json` 对 `compaction` / `effectiveReserveTokens` / `reserveTokens` / `reserveTokensFloor` / `contextTokenBudget` **全部 0 命中**（顶层 `session` 仅含 `dmScope`）。
3. **cron 表达式被误当自定义 DSL** → 仍是标准 cron 表达式（5 字段）。
4. **重复注册** → 本机已有 61 条 automations，含 3 条 heartbeat，条目堆积是真实风险。
5. **不去 `automations list` 复核** → 见 2.4.2 的边界声明：`cron add` 的条目是否出现在 `automations list` 中，⏳ **未实测，不做断言**。

**相关 FAQ**：F3-心跳与定时
**相关 Cookbook**：C2-协议 HEARTBEAT/MEMORY
**相关 SOP**：SOP-3 心跳监控

### 2.10.1 心跳（Heartbeat）相关真实路径（✅）

心跳**不是**顶层 key。真实路径在**子层级**：

| 真实路径 | 含义 |
|---|---|
| `agents.entries.<id>.heartbeat.every` | 该 agent 的心跳频率 |
| `agents.entries.<id>.groupChat.mentionPatterns` | 提及模式（群聊 trigger） |

**🚨 顶层不存在 `heartbeat` key**（列为 5 个误称字段之一）。

**本机心跳实况（✅）**
| 条目 | 频率 | 状态 |
|---|---|---|
| `heartbeat:tiance` | every 30m | **skipped** |
| `heartbeat:kunlun` | every 30m | **error 99+** |
| `heartbeat:peter` | every 2h | **error 70** |

**排障提示**：心跳全错时，按 FAQ F3 的顺序走；同时用 `openclaw doctor` 而非 `health-check`（后者不存在）。

---
## 2.11 `openclaw config` / `openclaw audit`

> **命令族定位**：配置读写与审计。**两个独立顶层族**（✅ 均实测存在）。

### 2.11.1 `openclaw config`

**语法**
```bash
openclaw config [<子命令或 flag>...]        # ⏳ 精确形态未实测
```

**用途**
读写 **主配置** `~/.openclaw/openclaw.json`。

**参数** / **选项**
| 参数 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | **子命令与 flag 均未实测**。本文件不列 `get` / `set` / `edit` / `validate` 之类名字 |

> 🚨 **纪律声明**：`openclaw config` 的**子命令名未采集**。本手册的 Hermes 侧有 `hermes config set`，**不要把它平移成 `openclaw config set`** 并当作事实——那属于跨工具类比。

**示例**
```bash
openclaw config                # ⏳ 输出形态未实测
```

**期望输出**
⚠️ 未实测。

**与主配置的对应（✅）**
主配置真身与结构是确定的，可直接读写：

```bash
# 真身
~/.openclaw/openclaw.json

# 20 个顶层 key（✅ 实测）
acp · agents · auth · bindings · browser · channels · commands · env ·
gateway · logging · memory · messages · meta · models · plugins ·
session · skills · talk · tools · wizard
```

**子层级关键路径（✅ 实测）**

| 真实路径 | 含义 |
|---|---|
| `agents.entries.<id>.heartbeat.every` | 心跳频率 |
| `agents.entries.<id>.groupChat.mentionPatterns` | 群聊提及模式 |
| `channels.feishu.requireMention` | 飞书需 @ 才响应 |
| `channels.feishu.groupAllowFrom` | 飞书群白名单 |
| `session.dmScope` | 本机实测值 `per-channel-peer` |
| `mcp.servers` | MCP 服务器命名空间 |

**🚨 5 个不存在的顶层字段（重复强调）**：`runtime` · `workspace` · `routing` · `heartbeat` · `subagents`

**真名陷阱**：❌ 配置路径不是 `~/.openclaw/workspace/openclaw.json`
**相关 FAQ**：F2-协议-SOUL-AGENTS-USER
**相关 SOP**：SOP-2 协议配置
**参考文件**：api-reference/02-config-reference（配置专册）

### 2.11.2 `openclaw audit`

**语法**
```bash
openclaw audit [<子命令或 flag>...]        # ⏳ 精确形态未实测
```

**用途**
审计。✅ 实测该命令族存在。⚠️ 审计**对象与范围**（配置？权限？渠道？技能？）**未实测**。

**参数** / **选项**：⏳ 未实测

**示例**
```bash
openclaw audit                 # ⏳ 输出形态未实测
```

**期望输出**：⚠️ 未实测。

**方向指引**
- 治理类审计的**业务侧**流程见 SOP-5 漂移治理 与 F7-治理漂移体检
- 技能/工具类审计的**实战**见 cookbook C3 与章节 chapters/11-skill-registry
- **安全审计类**实操见 cookbook C5 与 case-library/01-real-incidents（含 8/19 断线、9/21 飞书事故的审计线索）

**真名陷阱**：❌ 无 `openclaw audit-config` 之类复合子命令名（未实测，不假设）
**相关 FAQ**：F7-治理漂移体检
**相关 SOP**：SOP-5 漂移治理

---

## 2.12 `openclaw pairing`

> **命令族定位**：**Secure DM pairing**（安全私聊配对）（✅ 实测，官方描述）。

### `openclaw pairing`

**语法**
```bash
openclaw pairing [<子命令或 flag>...]        # ⏳ 精确形态未实测
```

**用途**
**私聊（DM）安全配对**。用途场景：让某个渠道（如 Telegram / 飞书）上的**某个用户**被安全地识别为该 agent 的合法私聊对象。

**参数** / **选项**
| 参数 | 必填 | 说明 |
|---|---|---|
| ⏳ | — | 未实测。不列 `start` / `approve` / `list` 之类名字 |

**示例**
```bash
openclaw pairing               # ⏳ 输出形态未实测
```

**期望输出**：⚠️ 未实测。

**为什么值得单列成族（设计解读，非实测）**
配对的存在意味着：**DM 不是默认开放的**。这与本机配置里 session 的作用域设计一致 —— 顶层 `session` 实测仅含 **`dmScope: per-channel-peer`**，即「每个渠道-对端一个作用域」。合理推论是：**配对决定了某个 peer 是否被授权进入某个 scope**。

> ⚠️ 上述「推论」为**设计解读**，非实测结论。事实边界：`openclaw pairing` 命令族**存在**（✅）；其子命令与流程 **⏳ 未实测**。

**新手坑**
1. **DM 没人回就以为 agent 挂了** → 先看是不是**没配对**。历史事故 9/21 飞书事故的根因就是**准入策略过严**（`requireMention: true` + `groupAllowFrom` 仅丘总 → 6 账号 disconnected，静默 >60min）。
2. **把配对与绑定（binding）混淆**：
   - **绑定（binding）** = agent ↔ 渠道（37 条）
   - **配对（pairing）** = 对端用户 ↔ 授权
   两者不同层。
3. **群聊与私聊策略混淆** → 群聊侧看 `channels.feishu.requireMention` 与 `groupAllowFrom`；私聊侧看 pairing。

**相关 FAQ**：F2-协议-SOUL-AGENTS-USER · F6-多Agent协同
**相关案例**：case-library/01-real-incidents（9/21 飞书事故 · PR #152777 · OPEN）
**相关 SOP**：SOP-6 事故恢复

---

## 2.13 `openclaw promos`

> **命令族定位**：**Discover and claim promotional model offers from ClawHub**（发现并领取 ClawHub 的促销模型额度）（✅ 实测，官方描述）。

### `openclaw promos`

**语法**
```bash
openclaw promos [<子命令或 flag>...]        # ⏳ 精确形态未实测
```

**用途**
与 **ClawHub** 交互，发现 / 领取**促销模型额度**（promotional model offers）。典型场景：免费额度、限时模型试用。

**参数** / **选项**：⏳ 未实测

**示例**
```bash
openclaw promos                # ⏳ 输出形态未实测
```

**期望输出**：⚠️ 未实测。

**为什么这个族对读者重要（非实测，说明性）**
本手册给**多 provider 模型配置**留了大量篇幅（见 chapters 与 api-reference 的 config 册）。`promos` 是**降低试错成本**的入口：先领促销额度，再决定换不换 provider。**注意**：命令族存在是 ✅ 事实；其子命令与领取流程是 ⏳ 待实测。

**新手坑**
1. **把 `promos` 当 `plugins`** → 两者都是复数、都以 `p` 开头，但一为额度领取，一为插件管理。
2. **领取后不写配置** → 领到额度 ≠ 模型已配置。仍需按 provider 配置流程写入 `models`（顶层 key，2 子项）并重启 Gateway（重启方式 ⏳）。
3. **在 CI 里跑** → 这是**交互式/账户级**操作，不适合无人值守脚本。

**真名陷阱**：❌ 不是 `openclaw promo`（单数）
**相关 FAQ**：F1-环境与安装（provider 配置）
**相关 Cookbook**：C3-Skills/Tools/MCP

---

## 2.14 `openclaw proxy`

> **命令族定位**：**Run the OpenClaw ...**（代理）（✅ 实测存在，官方描述被截断）。
> ⚠️ **诚实标注**：底稿记录的官方描述为「Run the OpenClaw ...」，**其余措辞未采集**。

### `openclaw proxy`

**语法**
```bash
openclaw proxy [<子命令或 flag>...]        # ⏳ 精确形态未实测
```

**用途**
运行 OpenClaw 代理（proxy）。典型用途推测（⚠️ **推测，非实测**）：为 API 请求提供本地代理层，便于观测/转发模型请求。

> 🚨 **不要照抄推测**。事实边界：命令族 `proxy` **存在**（✅）；用途细节、子命令、flag 均 **⏳ 未实测**。

**参数** / **选项**：⏳ 未实测

**示例**
```bash
openclaw proxy                 # ⏳ 输出形态未实测
```

**期望输出**：⚠️ 未实测。

**为什么这个族值得留意（工程视角·说明性）**
排查「agent 报 500 / 模型请求异常」时，**本地代理抓包**是最有效的手段之一：把请求先引到本地代理，看到真实发出的 payload，再判断是 prompt 组装问题还是 provider 侧问题。本手册的 OpenClaw 排障 SOP（SOP-6）与 FAQ F1 使用同一思路。**但 `openclaw proxy` 的具体用法本文件不做断言**。

**真名陷阱**：❌ 无 `openclaw gateway proxy` 之类复合名（未实测，不假设）
**相关 FAQ**：F1-环境与安装 · F5-Skills-Tools-MCP
**相关 SOP**：SOP-6 事故恢复

---

## 2.15 补充实测命令族（底稿实证 · 供完整参考）

以下命令族不在 §2.0 主表里，但底稿中有**实测记录**，故并入本参考：

### 2.15.1 `openclaw --version`

**语法**
```bash
openclaw --version
```

**用途**
打印版本。

**示例**
```bash
openclaw --version
```

**期望输出（✅ 实测）**
```
OpenClaw 2026.9.4 (3a9d69d)     # 任务基线（书内统一口径）
OpenClaw 2026.9.6 (eb377ac)     # 本机 live 复核实测
```

**注意**：这两行是**两次不同时点**的实测结果，不是一次输出的两行。

**新手坑**
- **排障时先确认版本** → 大量「命令不存在」的困惑其实来自**版本差异**。
- **报 issue 必带版本号** → 带上 hash（`3a9d69d` / `eb377ac`）。

### 2.15.2 `openclaw skills`

**语法**
```bash
openclaw skills <子命令> [<flag>...]        # ⏳ 子命令全集未实测
```

**已实测用法（✅）**
```bash
openclaw skills check --agent tiance
```

**期望输出（✅ 实测）**
```
Total 253
```

**用途**
对某个 agent 可见的技能做检查 / 计数。**示例中 `--agent tiance` 是已实测的 flag 形态**（`--agent` 与 `openclaw agent --agent` 一致，说明 OpenClaw 跨族统一用 `--agent` 指代目标 agent）。

**本机技能事实（✅）**

| 指标 | 值 |
|---|---|
| `~/.openclaw/workspace/skills/` 目录数 | **236** |
| `ls \| wc -l` | **238**（含 `INDEX.md` + 1 个非目录文件） |
| 含 SKILL.md 的目录 | **221** |
| 无 SKILL.md frontmatter | **47** |
| name 违例 | **55** |
| `openclaw skills check --agent tiance` | **Total 253** |

**⚠️ 数字口径诚实说明**
「236 目录」与「Total 253」**不是矛盾**——前者是**文件系统目录数**，后者是**某 agent 可见技能数**。两者统计对象不同（可能含内置/共享技能）。**不要用 236 去反推 253，也不要用 253 去核 236。**

**真实样本（✅）**
- `afrexai-compliance-audit`
- `skill-security-audit-v2`
- `skill-security-audit`（此三者之一为 **6/6 字段全覆盖样本**）

**新手坑**
1. **以为 `skills` 是顶层管理命令并乱猜子命令** → 子命令全集 ⏳ 未实测；已知可用的是 `check --agent <name>`。
2. **目录数当技能数** → 见上口径说明。
3. **写 SKILL.md 不带 frontmatter** → 本机 **47 个**如此，会造成 `skills check` 结果异常。规范见 chapters/10-skill-registry/SKILL.md-frontmatter-规范.md。

**相关 FAQ**：F5-Skills-Tools-MCP
**相关 Cookbook**：C3-Skills/Tools/MCP
**参考章节**：chapters/11-skill-registry

---

## 2.16 命令速查大表（把 §2 压成一页）

### 2.16.1 注册表读取类（**只读 · 最安全 · 优先用**）

| 目的 | 命令 | 本机实测值 |
|---|---|---|
| 版本 | `openclaw --version` | 2026.9.4 (3a9d69d) / live 2026.9.6 (eb377ac) |
| agent 清单 | `openclaw agents list` | **18** |
| 绑定清单 | `openclaw agents bindings` | **37**（TG 19 + 飞书 18） |
| 自动化清单 | `openclaw automations list` | **61** |
| 插件清单 | `openclaw plugins list` | **53/73** enabled |
| MCP 清单 | `openclaw mcp list` | **0** |
| 技能检查 | `openclaw skills check --agent <name>` | Total **253**（tiance） |
| 健康 | `openclaw health` | ⏳ 输出被 Gateway state 锁遮挡 |
| 诊断 | `openclaw doctor` | ⏳ 输出未实测 |

### 2.16.2 写入 / 变更类（**改前必 `openclaw backup create`**）

| 目的 | 命令 | 参数真名 |
|---|---|---|
| 初始化 | `openclaw setup` / `openclaw onboard` | ⏳ |
| 建 agent | `openclaw agents add <name> --workspace <dir>` | `--workspace` ✅ |
| 绑渠道 | `openclaw agents bind <...>` | ⏳ |
| 删 agent | `openclaw agents delete <name>` | ⏳ |
| 备份 | `openclaw backup create` | ⏳ |
| 建定时 | `openclaw cron add --cron X --session Y --message Z` | 三个 flag ✅ |
| 发消息 | `openclaw agent --agent X --message Y` | `--agent` / `--message` ✅ |

### 2.16.3 flag 真名速查

| 语义 | ✅ 真名 | ❌ 虚构 |
|---|---|---|
| 目标 agent | `--agent` | `--name` / `--id` |
| 消息正文 | `--message` | `--prompt` |
| cron 表达式 | `--cron` | `--schedule` |
| 目标会话 | `--session` | `--target` |
| 工作区目录 | `--workspace` | `--dir` / `--path` |
| 初始化 | `setup` / `onboard` | `init` |

### 2.16.4 退出码与全局 flag

**全局 flag**：⏳ **未实测**。（不列 `--verbose` / `--json` / `--config` 之类，避免编造。）

**退出码**：
| 码 | 含义 |
|---|---|
| `0` | 成功（常规约定） |
| 非 `0` | 失败（具体码与含义 ⏳ 未实测） |

> ⚠️ **诚实边界**：OpenClaw 的**具体错误码表未实测**。本文件的「错误码与排障」章（§4）用的是**错误现象**（报错文本 / 行为），而非数字码 —— 因为数字码拿不到。

---
# §3 常用工作流（5 条组合命令链）

> 本章把 §2 的单条命令，组装成**可执行的组合链**。
> 每条工作流都标注：**输入前置** / **步骤** / **每步验证** / **回滚点** / **相关 FAQ·Cookbook·SOP**。
> **纪律**：凡涉及 ⏳ 未实测 flag 的步骤，命令写成**形态示意**并明确标 ⏳，**不假装跑通**。

## 3.0 五条工作流总览

| # | 工作流 | 场景 | 命令数 | 关键风险 |
|---|---|---|---|---|
| W1 | 全新环境初始化 | 新机器 / 重装 | 4 | 跑 `openclaw init`（不存在） |
| W2 | 建 agent 并接通渠道 | 加一个新成员 | 5 | 建完不绑渠道 / 不复核 |
| W3 | 渠道准入策略配置 | 群聊不响应 / 误响应 | 4 | `requireMention` + `groupAllowFrom` 双杀 |
| W4 | 备份与恢复 | 改配置前 / 事故后 | 4 | 备份到不存在的路径 |
| W5 | 故障排障主链 | 静默 / 报错 / 不响应 | 6 | 起点跑 `health-check`（不存在） |

---

## W1 · 全新环境初始化

**前置输入**
- 已安装 OpenClaw（安装方式不在本文件范围，见 SOP-1）
- 有一个可用的模型 provider 凭证

**步骤**

```bash
# W1-1 版本确认（永远第一步）
openclaw --version
```
**验证**：输出形如 `OpenClaw 2026.9.x (<hash>)`。
**为什么**：后面所有命令的可用性都依赖版本。本手册口径 2026.9.4；本机 live 为 2026.9.6。

```bash
# W1-2 初始化向导
openclaw setup
# 或者
openclaw onboard
```
**验证**：向导跑完后，**主配置真身必须存在**：
```bash
ls -l ~/.openclaw/openclaw.json          # ✅ 应存在（本机 45,662 字节）
ls -l ~/.openclaw/workspace/openclaw.json # ❌ 不应存在（此路径为幻觉）
```
**真名陷阱**：❌ 不是 `openclaw init`

```bash
# W1-3 基线体检
openclaw doctor          # ✅ 诊断（不是 health-check）
openclaw health          # ⚠️ 可能被 Gateway state 库锁遮挡（本机实测）
```
**验证**：能读出 gateway 层面是否就绪。若 `health` 输出被遮挡，改用 W5 的替代观测。

```bash
# W1-4 注册表读数（建立基线数字）
openclaw agents list
openclaw agents bindings
openclaw automations list
openclaw plugins list
openclaw mcp list
```
**验证**：把 5 个数字记下来。**这是你的基线**。以后所有「变没变」的判断都相对它。本机基线：
| 命令 | 本机值 |
|---|---|
| `agents list` | 18 |
| `agents bindings` | 37 |
| `automations list` | 61 |
| `plugins list` | 53/73 enabled |
| `mcp list` | 0 |

```bash
# W1-5 立刻备份干净基线
openclaw backup create
```
**验证**：备份产出存在（⚠️ 落盘路径 ⏳ 未实测，故需自行确认）。
**为什么**：**这是本书最强调的一步**。2026-08-19 军团断线事故能恢复，靠的就是改前备份（`openclaw.json.bak.pre-fix-2026-08-19-0921`）。

**回滚点**：W1-5 的备份。
**相关 FAQ**：F1-环境与安装
**相关 SOP**：**SOP-1 环境搭建**（本章与之配对）
**相关 Cookbook**：—
**相关章节**：00-getting-started/00-environment-checklist

---

## W2 · 建 agent 并接通渠道

**前置输入**
- 已初始化（W1 完成）
- 知道要建的 agent 名 `<name>`
- 知道要绑的渠道 `<channel>`

**步骤**

```bash
# W2-1 改前备份（不可跳过）
openclaw backup create
```

```bash
# W2-2 看现状
openclaw agents list          # 本机基线 18
openclaw agents bindings      # 本机基线 37
```
**验证**：记下两个数字。

```bash
# W2-3 建 agent（真名：add + --workspace）
openclaw agents add my-agent --workspace ~/.openclaw/workspace/agents/my-agent
```
**验证（关键 · 别跳过）**：
```bash
openclaw agents list          # 应变成 19
```
**真名陷阱**
- ❌ `openclaw agents create my-agent`
- ❌ `--dir`（真名 `--workspace`）

> **常见误判**：用 `ls ~/.openclaw/workspace/agents/my-agent` 看到目录就以为成功。**目录存在 ≠ 注册表有 entry**。必须用 `agents list`。

```bash
# W2-4 绑渠道
openclaw agents bind <agent> <channel>       # ⏳ 参数形态未实测
```
**验证**：
```bash
openclaw agents bindings      # 应从 37 变成 38
```

```bash
# W2-5 冒烟测试
openclaw agent --agent my-agent --message "ping"
```
**验证**：拿到一次回复。
**真名陷阱**：❌ `openclaw chat --agent X --prompt Y`；✅ `openclaw agent --agent X --message Y`

**本机绑定实况参考（✅）**

| 渠道 | 数量 |
|---|---|
| Telegram | 19 |
| 飞书 | 18 |
| 合计 | **37** |

**回滚点**：
- 若 W2-3 建错：`openclaw agents delete my-agent`（⚠️ 参数形态 ⏳）
- 若 W2-4 绑错：用备份回滚（**bindings 的解绑命令未实测**）

**⚠️ 删除前必读**：删 agent 前先看它有没有 binding（`openclaw agents bindings`）。删掉仍有 binding 的 agent 可能留下**指向空 target 的绑定**，导致该渠道静默不响应。

**相关 FAQ**：F6-多Agent协同
**相关 Cookbook**：**C6-协同舰队**
**相关 SOP**：SOP-2 协议配置

---

## W3 · 渠道准入策略配置（群聊不响应 / 误响应）

**前置输入**
- 某个渠道（本手册重点：**飞书**）的群聊行为不符合预期
- 已知关键配置路径

**背景（✅ 实测事故）**

> **2026-09-21 飞书事故**
> 根因：`requireMention: true` + `groupAllowFrom` 仅丘总
> 后果：**6 个账号 disconnected，静默 >60min**
> 上游修复：**PR #152777 · OPEN**（feishu groupPolicy）

这条事故说明：**飞书群聊的准入策略有两个旋钮，且会互相放大**。

**步骤**

```bash
# W3-1 先看现状（只读安全的路径读数）
openclaw agents bindings                 # 飞书应为 18 条
openclaw doctor                          # ✅ 诊断入口
```

```bash
# W3-2 读关键配置（真实路径 · ✅）
# channels.feishu.requireMention    → 群里是否必须 @ 才响应
# channels.feishu.groupAllowFrom    → 群白名单
# 主配置真身：~/.openclaw/openclaw.json
openclaw config                          # ⏳ 子命令未实测，此处仅示意
```
**验证**：确认 `requireMention` 与 `groupAllowFrom` 两个值是否与你的期望一致。

**策略矩阵（诊断用）**

| `requireMention` | `groupAllowFrom` | 后果 |
|---|---|---|
| `true` | 仅白名单内 1 人 | **极易静默**（9/21 事故形态） |
| `true` | 宽（多人/多群） | 需 @ 才响应，预期行为 |
| `false` | 宽 | 群内任何消息都响应 → 可能噪音/成本飙升 |
| `false` | 窄 | 只有白名单范围内的消息响应 |

```bash
# W3-3 收紧或放宽（改前备份 · 必须）
openclaw backup create
# → 修改 channels.feishu.requireMention / channels.feishu.groupAllowFrom
```

```bash
# W3-4 复核 + 观察
openclaw agents bindings      # 飞书账号数应不变（18）
openclaw automations list     # 看有无新增 error
```
**验证**：**静默 >60min 是危险信号**（9/21 事故正是「静默 >60min」才被发现）。建议在改完后 10 分钟和 60 分钟各看一次。

**回滚点**：W3-3 前的备份。
**相关 FAQ**：F2-协议-SOUL-AGENTS-USER · F6-多Agent协同
**相关 Cookbook**：C6-协同舰队 · C5-漂移治理
**相关 SOP**：**SOP-6 事故恢复** · SOP-2 协议配置
**相关案例**：case-library/01-real-incidents（9/21 飞书事故 · PR #152777 OPEN）

---

## W4 · 备份与恢复

**前置输入**
- 任何**即将改配置**的动作，或**已经出事故**

**步骤**

```bash
# W4-1 备份（改前）
openclaw backup create
```
**真名陷阱**：❌ 不是 `openclaw agents archive`（无此子命令）

```bash
# W4-2 确认备份真的覆盖了正确对象（最易被忽略的一步）
ls -l ~/.openclaw/openclaw.json            # ✅ 45,662 字节（本机）
# ⚠️ 不要备份 ~/.openclaw/workspace/openclaw.json —— 该文件不存在
```
**为什么**：生产事故里「备份成功但备份错对象」极难发现（见 §1.3 #8）。

```bash
# W4-3 改配置
# ...
```

```bash
# W4-4 复核
openclaw agents list
openclaw agents bindings
openclaw automations list
openclaw doctor
```
**验证**：三个注册表数字与 W4-1 前一致（或变化符合预期）。

**恢复路径（⚠️ 诚实边界）**
`openclaw backup` 的**恢复子命令未实测**（底稿只确认 `create`）。因此本文件给出两条路：

| 路线 | 说明 | 证据等级 |
|---|---|---|
| A · 用 backup 恢复 | `openclaw backup <restore 子命令>` —— ⏳ 子命令名未实测 | ⏳ |
| B · 用文件级备份还原 | 本机事故史中实际使用的是**改前文件副本**（`openclaw.json.bak.pre-fix-<阶段>-<YYYY-MM-DD>-<HHMM>`） | ✅ 实读 |

**路线 B 命名惯例（✅ 实读于 2026-08-19 事故记录）**
```
openclaw.json.bak.pre-fix-2026-08-19-0921
└─────┬──────┘ └──┬──┘ └────┬─────┘└─┬─┘
   文件名      .bak   阶段标记   日期   时间
```
**这是人工命名惯例，不是 `backup create` 的输出格式。**

**回滚纪律（SOP-6 核心）**
1. 改前必 `backup create`
2. 额外留一份带**阶段名**与**时间戳**的文件副本
3. 改后立即跑注册表读数三连
4. 发现异常 → **立即回滚，不尝试原地修**（8/19 事故的教训）

**相关 FAQ**：F7-治理漂移体检 · F1-环境与安装
**相关 SOP**：**SOP-6 事故恢复**（本章核心配对）
**相关 Cookbook**：C5-漂移治理
**相关案例**：case-library/01-real-incidents

---

## W5 · 故障排障主链（静默 / 报错 / 不响应）

**前置输入**
- 某个 agent 不响应，或某个渠道静默，或某条自动化报错

**主链（按序执行，不要跳）**

```bash
# W5-1 版本（永远第一步）
openclaw --version
```
**为什么**：很多「命令不存在」的困惑来自版本差异。

```bash
# W5-2 诊断入口（真名！）
openclaw doctor
# ❌ 不是 openclaw agents health-check
openclaw health          # ⚠️ 可能被 Gateway state 库锁遮挡
```

```bash
# W5-3 替代观测（当 health 不可读时 · 本文件推荐）
openclaw agents list          # 本机 18
openclaw agents bindings      # 本机 37
openclaw automations list     # 本机 61 ← 错误状态在这里最明显
openclaw plugins list         # 本机 53/73 ← 看 a2a 是否 enabled
openclaw mcp list             # 本机 0
```

```bash
# W5-4 定时/心跳方向
openclaw automations list
```
**看什么（本机真实样本 · ✅）**

| 条目 | 频率 | 状态 | 读法 |
|---|---|---|---|
| `heartbeat:tiance` | every 30m | **skipped** | 被跳过 → 看是否被更高优先级占用 |
| `heartbeat:kunlun` | every 30m | **error 99+** | 高频失败 → 大概率配置/凭证问题 |
| `heartbeat:peter` | every 2h | **error 70** | 同上 |
| `能力矩阵月度更新` | — | **error 4x** | 对应「26 天未续期」事故 |

```bash
# W5-5 插件方向（A2A 场景）
openclaw plugins list
```
**看什么**：本机 `a2a` 插件 = **disabled**（路径 `stock:a2a/index.js`）。
**推论**：A2A 不工作 → **先看这一条**，再去看 chapters/10-A2A绑定。

```bash
# W5-6 单点复现
openclaw agent --agent <name> --message "ping"
```
**看什么**：能不能一发一收。
**真名陷阱**：❌ `openclaw chat --prompt`

**排障决策树（现象 → 方向）**

| 现象 | 第一站 | 相关 FAQ |
|---|---|---|
| 命令报「不存在」 | §1.2 真名表（**先怀疑自己写了幻觉命令**） | F1 |
| 群聊不响应 | W3 策略矩阵（`requireMention` / `groupAllowFrom`） | F2 · F6 |
| DM 不响应 | `openclaw pairing` 族（配对） | F2 |
| 定时/心跳不动 | `openclaw automations list` 看状态 | F3 |
| 记忆/会话异常 | `session` 顶层 key（实测仅 `dmScope`） | F4 |
| 技能/工具/MCP 异常 | `plugins list` · `mcp list` · `skills check` | F5 |
| 多 agent 协同异常 | `agents bindings` · `plugins list`(a2a) | F6 |
| 治理漂移 / 长期失效 | `openclaw audit` · `backup create` | F7 |

**回滚点**：任何变更前的 `openclaw backup create`。

**⚠️ 排障三忌**
1. **忌起点跑错命令** → `health-check` 不存在，白耗 20 分钟。
2. **忌只看一个面** → `health` + `automations list` + `plugins list` 三个面都要看。历史事故（9/21）正是「静默 >60min」才被发现 → **一定要看 `automations` 的 error 计数变化**。
3. **忌原地修** → 8/19 事故的根因修复方式不是「把 fallback 列表改回去」，而是**识别出 `primary == fallback[0]` 的自循环结构**。**先理解结构，再改。**

**相关 FAQ**：F1 · F2 · F3 · F4 · F5 · F6 · F7（全链）
**相关 Cookbook**：**C7-生产运维** · C5-漂移治理
**相关 SOP**：**SOP-6 事故恢复** · SOP-3 心跳监控
**相关案例**：case-library/01-real-incidents · case-library/02-production-patterns

---

## 3.6 工作流组合速查卡

```bash
# ── 日常只读巡检（最安全，随时可跑）──
openclaw --version
openclaw agents list
openclaw agents bindings
openclaw automations list
openclaw plugins list
openclaw mcp list

# ── 变更前（永远先跑这一条）──
openclaw backup create

# ── 变更后（永远跑这三条）──
openclaw agents list && openclaw agents bindings && openclaw doctor

# ── 排障（真名，不是 health-check）──
openclaw doctor
openclaw automations list
```

---
# §4 错误码与排障

> ⚠️ **本章的诚实前提**
> OpenClaw 的**数字错误码表未实测**（底稿未覆盖）。因此本章以**错误现象（报错文本 / 行为）** 为单位，而不是以数字码为单位。
> 每条给：**现象** / **最可能根因** / **诊断路径** / **处置** / **互链**。

## 4.0 十二类常见错误总表

| # | 现象 | 类别 | 首要怀疑 | 引 FAQ |
|---|---|---|---|---|
| E1 | `command not found` / unknown subcommand | 命令不存在 | **自己写了幻觉命令** | F1 |
| E2 | unknown flag / unrecognized option | flag 名错 | `--prompt`/`--schedule`/`--target`/`--dir` | F1 · F3 |
| E3 | agent 建了但列表里没有 | 注册表未落 | 漏 `--workspace`，或用 `create` | F6 |
| E4 | DM 没人回 | 准入 | 未 pairing / 配对失效 | F2 |
| E5 | 群聊不响应 / 静默 >60min | 准入 | `requireMention` + `groupAllowFrom` | F2 · F6 |
| E6 | 心跳不动 / `skipped` | 定时 | 心跳被更高优先级占用 | F3 |
| E7 | `error 99+` / `error 70` / `error 4x` | 定时失败累积 | 凭证/配置/模型供应 | F3 · F7 |
| E8 | 上下文被压缩后行为异常 | 会话 | Compaction 参数误植 | F4 |
| E9 | 技能不被识别 | 技能 | 无 frontmatter / name 违例 | F5 |
| E10 | MCP 工具不出现 | MCP | `mcp.servers` 命名空间写错 / 本机 0 配置 | F5 |
| E11 | A2A（Agent-to-Agent）不工作 | 插件 | `a2a` 插件 disabled | F6 |
| E12 | 改了配置不生效 | 配置 | 改错文件（workspace 下的假路径） | F2 · F1 |

---

## E1 · `command not found` / unknown subcommand

**现象**
```
openclaw init
→ 命令不存在 / unknown subcommand
```

**最可能根因**
**读者自己写的是幻觉命令。** 在 2026 年的现实里，命令来源大概率是 AI 生成，而 AI 生成 OpenClaw 命令的幻觉率极高（见 §1.1 的四层原因）。

**诊断路径**
1. 先把命令第一级子命令抄下来，对照 §1.2 的 9 条真名对照表。
2. 再看 §2.0 的 14 族总览表，确认族名。
3. 若仍不确定，跑 `openclaw <族> --help`（**唯一被允许的 `--help` 用法**：验证你自己要跑的那一条，不是全量采集）。

**高频命中清单（背下来）**
| 你写的 | 真名 |
|---|---|
| `init` | `setup` / `onboard` |
| `chat` | `agent` |
| `plugin`（单数） | `plugins`（复数） |
| `agents create` | `agents add` |
| `agents health-check` | `health` / `doctor` |
| `agents archive` | `backup create` |

**处置**：改真名重跑。**不要**因为一条命令不存在就去重装 OpenClaw。
**引 FAQ**：F1-环境与安装
**引 SOP**：SOP-1

---

## E2 · unknown flag / unrecognized option

**现象**
```
openclaw agent --agent X --prompt Y
→ unknown option: --prompt
```

**最可能根因**
**子命令写对了，flag 名写错了。** 这是比 E1 更隐蔽的错——因为第一段没报错，读者会以为「命令是对的，只是参数有点问题」。

**诊断路径**
| 语义 | ✅ 真名 | ❌ 虚构 |
|---|---|---|
| 消息正文 | `--message` | `--prompt` |
| cron 表达式 | `--cron` | `--schedule` |
| 目标会话 | `--session` | `--target` |
| 工作区 | `--workspace` | `--dir` / `--path` |
| 目标 agent | `--agent` | `--name` |

**处置**：改 flag 名。
**⚠️ 半修陷阱**：`openclaw chat --agent X --message Y` 仍然是错的（`chat` 不存在）。**子命令与 flag 要一起改。**

**引 FAQ**：F1 · F3
**引 SOP**：SOP-1 · SOP-3

---

## E3 · agent 建了但列表里没有

**现象**
```bash
openclaw agents add my-agent
openclaw agents list
→ 列表里没有 my-agent
```

**最可能根因（按概率排序）**
1. **用了 `create` 而不是 `add`** → 命令根本没成功（回到 E1）
2. **漏了 `--workspace <dir>`** → 语法是成对的
3. **只在文件系统里 `ls` 看到了目录，就以为成功** → 目录 ≠ 注册表 entry
4. **建在了另一台机器 / 另一个 profile** → 注册表在 `~/.openclaw/openclaw.json` 里

**诊断路径**
```bash
openclaw agents list                                    # 权威读法（本机基线 18）
ls -l ~/.openclaw/openclaw.json                        # 主配置真身（✅）
# 检查 agents.entries 的键数（本机 18）
```
**关键区分**：`agents.entries` 的键 **18 个**（✅ 实测）是**注册表口径**；`~/.openclaw/workspace/agents/` 下的目录是**文件系统口径**。两者不自动同步。

**处置**
```bash
openclaw agents add my-agent --workspace ~/.openclaw/workspace/agents/my-agent
openclaw agents list          # 必须复核
```
**引 FAQ**：F6-多Agent协同
**引 Cookbook**：C6-协同舰队

---

## E4 · DM 没人回

**现象**：私聊某个 agent，长时间无响应。

**最可能根因**
1. **未配对（pairing）** → DM 不是默认开放的
2. **session 作用域不匹配** → 顶层 `session` 实测仅含 **`dmScope: per-channel-peer`**，即「每渠道-每对端一个作用域」
3. **渠道侧 binding 缺失** → `openclaw agents bindings` 里没有这条
4. **agent 侧模型供应故障** → 看 `automations list` 的 error 计数

**诊断路径**
```bash
openclaw agents bindings      # 本机 37（TG 19 + 飞书 18）
openclaw doctor               # ✅ 真名
openclaw pairing              # ⏳ 子命令未实测
```
**处置**
1. 先确认 binding 存在
2. 再确认 pairing 状态
3. 再看 `dmScope` 配置
4. 让对端**重发一条**，观察是否进 session

**引 FAQ**：F2-协议-SOUL-AGENTS-USER · F4-记忆与会话
**引 SOP**：SOP-2

---

## E5 · 群聊不响应 / 静默 >60min

**现象**：群里 @ 了但没反应；或整个渠道静默超过一小时。

**最可能根因（这是本手册最高优先级的实测事故形态）**

> **2026-09-21 飞书事故**
> 根因：`requireMention: true` + `groupAllowFrom` 仅丘总
> 后果：**6 个账号 disconnected，静默 >60min**
> 上游修复：PR #152777 · **OPEN**

**诊断路径**
```bash
# 真实路径（✅ 实测）
# channels.feishu.requireMention
# channels.feishu.groupAllowFrom

openclaw agents bindings      # 飞书应为 18
openclaw doctor
```
**策略矩阵**
| `requireMention` | `groupAllowFrom` | 后果 |
|---|---|---|
| `true` | 极窄（1 人） | **极易静默**（9/21 形态） |
| `true` | 宽 | 需 @ 才响应（预期） |
| `false` | 宽 | 全响应 → 噪音/成本风险 |
| `false` | 窄 | 白名单内响应 |

**处置**
```bash
openclaw backup create        # 先备份
# 修改 channels.feishu.requireMention / groupAllowFrom
openclaw agents bindings      # 复核
# 10 分钟与 60 分钟各观测一次
```
**⚠️ 静默 >60min 是报警阈值**（9/21 事故正是据此发现）。

**引 FAQ**：F2 · F6
**引 SOP**：SOP-6 事故恢复
**引案例**：case-library/01-real-incidents

---

## E6 · 心跳不动 / `skipped`

**现象**：`openclaw automations list` 里 `heartbeat:tiance`（every 30m）显示 **skipped**。

**最可能根因**
1. 被**更高优先级的任务占用**（同一 agent 上已有跑着的任务）
2. 该 agent 长时间处于忙碌 session
3. 上游依赖未就绪

**诊断路径**
```bash
openclaw automations list        # 看 skipped / error 计数
openclaw doctor
```
**本机真实读数（✅）**
| 条目 | 频率 | 状态 |
|---|---|---|
| `heartbeat:tiance` | every 30m | skipped |
| `heartbeat:kunlun` | every 30m | error 99+ |
| `heartbeat:peter` | every 2h | error 70 |

**⚠️ 关键区分**：`skipped` ≠ `error`。
- `skipped` = 到点了但**没跑**（占用/跳过）
- `error` = 跑了但**失败**（配置/凭证/供应）

两者处置完全不同，**先看清是哪一类**。

**引 FAQ**：F3-心跳与定时
**引 SOP**：SOP-3 心跳监控
**引 Cookbook**：C2-协议 HEARTBEAT/MEMORY

---

## E7 · `error 99+` / `error 70` / `error 4x`（失败累积）

**现象**：自动化条目累计大量 error（本机样本：`heartbeat:kunlun` 99+ · `heartbeat:peter` 70 · `能力矩阵月度更新` 4）。

**最可能根因**
1. **模型供应侧**：`primary == fallback[0]` 的自循环（**8/19 事故结构性根因**）
2. **凭证失效**
3. **渠道准入**（如 E5）
4. **上游 API 返回空 body**（8/19 事故的直接触发：MiniMax-M3 空 body）

**诊断路径**
```bash
openclaw --version            # 先确认版本
openclaw automations list     # 看 error 计数与条目名
openclaw doctor
openclaw mcp list             # 0 = 无 MCP 依赖
openclaw plugins list         # 看 a2a 等是否影响
```

**关键结构检查：`primary == fallback[0]` 自循环**
> 8/19 军团断线事故的根因链：
> MiniMax-M3 空 body → **17-18 fallback 首位被占** → 轩辕 `primary == fallback[0]` → **自循环**
> 恢复依据：`openclaw.json.bak.pre-fix-2026-08-19-0921`

**诊断要点**：检查 `models`（顶层 key，2 子项）里是否存在某 agent 的 **primary 与 fallback[0] 相同**。若有，**空响应会自循环**。

**处置**
```bash
openclaw backup create
# 修 fallback 列表结构（不是"改回去"，而是消除 self-loop）
openclaw automations list     # 观察 error 计数是否停止增长
```
**⚠️ 纪律**：**先理解结构再改**。8/19 的解法是识别出**自循环结构**，而不是把上次的改动撤销。

**引 FAQ**：F1 · F3 · F7
**引 SOP**：**SOP-6 事故恢复**
**引案例**：case-library/01-real-incidents

---

## E8 · 上下文被压缩后行为异常（Compaction 误植）

**现象**：长对话后 agent 行为异常；或按网上教程改了「压缩保留 token」但毫无效果。

**最可能根因**
**用了不存在的配置名。**（✅ 实测）

| ❌ 误植（网上流传） | ✅ 真名 |
|---|---|
| `reserveTokensFloor` | **不存在** → `CompactionRequestBudget.reserveTokens` |
| — | 常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25` |
| — | `effectiveReserveTokens` |

**实测证据**：本机 `openclaw.json` 对 `compaction` / `effectiveReserveTokens` / `reserveTokens` / `reserveTokensFloor` / `contextTokenBudget` **全部 0 命中**（顶层 `session` 仅含 `dmScope`）。

**诊断路径**
```bash
# 在主配置里搜这几个词（本机结果：全部 0 命中）
# ~/.openclaw/openclaw.json
```
**处置**：**不要**照抄含 `reserveTokensFloor` 的教程。若要调压缩行为，用真名（`CompactionRequestBudget.reserveTokens` / `MAX_COMPACTION_RESERVE_RATIO`）。

**引 FAQ**：F4-记忆与会话
**引 SOP**：SOP-4 记忆训练
**引 Cookbook**：C2-协议 HEARTBEAT/MEMORY

---

## E9 · 技能不被识别

**现象**：放了技能目录，但 `openclaw skills check` 结果异常 / agent 用不到。

**最可能根因（✅ 本机实测数字）**

| 指标 | 本机值 |
|---|---|
| `~/.openclaw/workspace/skills/` 目录 | **236** |
| `ls \| wc -l` | **238**（含 `INDEX.md` + 1 个非目录文件） |
| 含 SKILL.md | **221** |
| **无 SKILL.md frontmatter** | **47** ⚠️ |
| **name 违例** | **55** ⚠️ |
| `skills check --agent tiance` | Total **253** |

**诊断路径**
```bash
openclaw skills check --agent <name>          # 已实测用法
```

**⚠️ 口径陷阱**：「目录 236」≠「Total 253」。两者统计对象不同，**不要互相反推**。

**处置**
1. 给缺 frontmatter 的 47 个补 frontmatter
2. 修 55 个 name 违例（命名规范见 chapters/10-skill-registry/SKILL.md-frontmatter-规范.md）
3. 复核 `skills check`

**参考样本（✅ 实测）**：`afrexai-compliance-audit` · `skill-security-audit-v2` · `skill-security-audit`（**6/6 字段全覆盖样本**）

**引 FAQ**：F5-Skills-Tools-MCP
**引 Cookbook**：C3-Skills/Tools/MCP
**引章节**：chapters/11-skill-registry

---

## E10 · MCP 工具不出现

**现象**：配了 MCP server，但工具列表里没有。

**最可能根因**
1. **命名空间写错**：真名是 **`mcp.servers`**（✅ 实测），不是 `mcpServers`（VS Code / Cline 风格）也不是顶层 `servers`
2. **本机基线是 0** → 看不到东西可能是**真的没配**
3. **配置层级错** → 与 §1.3 #8 同源：写进了 `~/.openclaw/workspace/` 下的假路径

**诊断路径**
```bash
openclaw mcp list        # 本机 = 0 配置（诚实基线）
openclaw mcp --help      # 应从输出里数出 14 个子命令
```
**已实测事实（✅）**
| 项 | 值 |
|---|---|
| `mcp` 子命令数 | **14** |
| 命名空间 | **`mcp.servers`** |
| 本机 `mcp list` | **0** |
| 子命令具体名称 | ⏳ 未实测 |

**处置**：按 chapters/09-MCP绑定 与 cookbook C3 的流程配置；确认命名空间；`mcp list` 复核。

**引 FAQ**：F5-Skills-Tools-MCP
**引 Cookbook**：C3-Skills/Tools/MCP
**引章节**：chapters/09-MCP绑定

---

## E11 · A2A（Agent-to-Agent）不工作

**现象**：多 agent 互调不成功。

**最可能根因**
**`a2a` 插件是 disabled。**（✅ 实测）

| 插件 | 状态 | 路径 |
|---|---|---|
| `a2a` | **disabled** | `stock:a2a/index.js` |

**诊断路径**
```bash
openclaw plugins list        # 本机 53/73 enabled；看 a2a 行
```
**处置**
1. 先确认插件层状态（本机是 disabled）
2. 再看 chapters/10-A2A绑定 的协议层
3. TCK 测试 ⏳ **未实测**（底稿 §5 明列「A2A TCK 测试」为待实测项）

**⚠️ 诚实边界**：本文件**不提供**启用 `a2a` 的具体命令——`plugins` 的 15 个子命令名 ⏳ 未实测。

**引 FAQ**：F6-多Agent协同 · F5
**引章节**：chapters/10-A2A绑定
**引 Cookbook**：C6-协同舰队

---

## E12 · 改了配置不生效

**现象**：改了「配置」，重启后行为无变化。

**最可能根因（最高频的坑）**
**改错文件。**（✅ 实测）

| 路径 | 状态 |
|---|---|
| `~/.openclaw/openclaw.json` | **存在**（45,662 字节 · 早期 45,445） |
| `~/.openclaw/workspace/openclaw.json` | **不存在**（已 `ls` 确认） |

**新手会踩什么坑**
1. `vim ~/.openclaw/workspace/openclaw.json` → **vim 会创建空文件** → 之后 `ls` 看到文件存在 → 确信「配置在这，而且是坏的」
2. 改完重启 → 无变化 → 怀疑「配置不热加载」「重启没生效」→ 排查方向全偏

**诊断路径**
```bash
ls -l ~/.openclaw/openclaw.json             # 应有真实大小（本机 45,662）
ls -l ~/.openclaw/workspace/openclaw.json  # 若存在且为 0 字节 → 你新建了假文件
openclaw agents list && openclaw doctor     # 复核
```
**处置**
1. 删掉误建的空文件
2. 改真身 `~/.openclaw/openclaw.json`
3. 复核

**20 个顶层 key（对照用 · ✅）**
`acp` `agents` `auth` `bindings` `browser` `channels` `commands` `env` `gateway` `logging` `memory` `messages` `meta` `models` `plugins` `session` `skills` `talk` `tools` `wizard`

**5 个不存在的顶层字段（🚨）**：`runtime` `workspace` `routing` `heartbeat` `subagents`

**引 FAQ**：F2 · F1
**引 SOP**：SOP-2 协议配置

---

## 4.13 排障元规则（比任何单条规则都重要）

1. **先怀疑命令名，再怀疑环境。** 90% 的「OpenClaw 有问题」其实是幻觉命令。
2. **只读优先。** 所有 §2.16.2 的读命令随时可跑；所有写命令先 `openclaw backup create`。
3. **数字基线。** 记住五个数：`agents 18` / `bindings 37` / `automations 61` / `plugins 53/73` / `mcp 0`。任何偏离都是线索。
4. **`skipped` ≠ `error`。** 前者没跑，后者跑了但失败。
5. **静默 >60min 是报警。**（9/21 飞书事故的发现方式）
6. **先理解结构再改。**（8/19 事故：`primary == fallback[0]` 自循环）
7. **改前备份，改后三连。**（`backup create` → 改 → `agents list && agents bindings && doctor`）

---

# §5 诚实边界声明

> 本章是**必须读**的。本文件的价值不在于「看起来很全」，而在于**每一条都标了它有多可靠**。

## 5.1 ✅ 已实测（可直接信任）

以下内容来自 2026-09-27 / 2026-09-28 的实机采集（底稿 §1.3 / §1.4 / §3 全覆盖）：

### 5.1.1 版本（✅）

```bash
openclaw --version
→ OpenClaw 2026.9.4 (3a9d69d)     # 任务基线（书内统一口径）
→ OpenClaw 2026.9.6 (eb377ac)     # 本机 live 复核实测
```

### 5.1.2 命令族与子命令名（✅）

| 命令族 | 已实测内容 |
|---|---|
| `openclaw setup` / `onboard` | 存在（初始化向导） |
| `openclaw agents` | **子命令全表**：`add` · `bind` · `bindings` · `delete` · `list`（**无** `health-check` / `create` / `archive`） |
| `openclaw agent` | `--agent X --message Y` |
| `openclaw automations` | 存在；子命令含 `list` |
| `openclaw mcp` | 存在；**14 子命令**（名称未逐一记录）；命名空间 `mcp.servers` |
| `openclaw acp` | 存在（Zed ACP bridge） |
| `openclaw plugins` | 存在；**15 子命令**（名称未逐一记录） |
| `openclaw backup` | 存在；含 `create` |
| `openclaw health` / `doctor` | 均存在 |
| `openclaw cron` | `add` 的 flag 真名：`--cron` / `--session` / `--message` |
| `openclaw config` / `audit` | 均存在 |
| `openclaw pairing` | 存在（Secure DM pairing） |
| `openclaw promos` | 存在（ClawHub 促销领取） |
| `openclaw proxy` | 存在 |
| `openclaw skills` | `check --agent <name>` 用法实测 |

### 5.1.3 配置结构（✅）

- 真身路径 `~/.openclaw/openclaw.json`（45,662 字节；早期 45,445）
- `~/.openclaw/workspace/openclaw.json` **不存在**（已 `ls` 确认）
- **20 个顶层 key**：`acp` `agents` `auth` `bindings` `browser` `channels` `commands` `env` `gateway` `logging` `memory` `messages` `meta` `models` `plugins` `session` `skills` `talk` `tools` `wizard`
- **5 个不存在的顶层字段**：`runtime` `workspace` `routing` `heartbeat` `subagents`
- 子层级真路径：`agents.entries.<id>.heartbeat.every` · `agents.entries.<id>.groupChat.mentionPatterns` · `channels.feishu.requireMention` · `channels.feishu.groupAllowFrom`
- Compaction 真名：`CompactionRequestBudget.reserveTokens` · `MAX_COMPACTION_RESERVE_RATIO = 0.25` · `effectiveReserveTokens`；`reserveTokensFloor` **不存在**；本机对 `compaction`/`effectiveReserveTokens`/`reserveTokens`/`reserveTokensFloor`/`contextTokenBudget` **全部 0 命中**

### 5.1.4 生产实况数值（✅）

| 指标 | 值 |
|---|---|
| agent 数 | **18** |
| 主模型分布 | opus-4-8 ×9 · gpt-5.6-sol ×4 · gpt-5.5 ×2 · gpt-5.6-terra ×2 · deepseek-v4-flash ×1 |
| binding 数 | **37**（Telegram 19 + 飞书 18） |
| automation 数 | **61**（早期 43 · 两次均曾观测到） |
| plugins | **53/73 enabled**（早期 51/69） |
| `a2a` 插件 | **disabled**（`stock:a2a/index.js`） |
| `~/.openclaw/extensions/` | **不存在** |
| `mcp list` | **0** |
| skills 目录 | **236**（`ls \| wc -l` = 238） |
| 缺 frontmatter | **47** |
| name 违例 | **55** |
| `skills check --agent tiance` | **Total 253** |
| heartbeat 状态 | `tiance` skipped · `kunlun` error 99+ · `peter` error 70 |
| 能力矩阵 | error 4x（2026-09-01 后 26 天未续期） |

### 5.1.5 事故基线（✅ 实读）

| 事故 | 根因 | 证据文件 |
|---|---|---|
| 2026-08-19 军团断线 | MiniMax-M3 空 body → 17-18 fallback 首位被占 → 轩辕 `primary == fallback[0]` 自循环 | `.../workspace-kunlun/memory/2026-08-19-军团断线修复.md` · 备份 `openclaw.json.bak.pre-fix-2026-08-19-0921` |
| 2026-09-21 飞书事故 | `requireMention: true` + `groupAllowFrom` 仅丘总 → 6 账号 disconnected，静默 >60min | 上游 PR #152777 · **OPEN** |

---

## 5.2 ⏳ 待实测（本文件不为其背书）

以下内容本文件**明确标注为未实测**。凡在书中见到这些内容被当作事实陈述，均属**越界**。

| # | 待实测项 | 本文件如何处理 |
|---|---|---|
| 1 | `openclaw health` 完整输出（被 Gateway state 库独占锁遮挡） | **不伪造输出**；给出替代观测（§2.9.1） |
| 2 | 飞书 13 个账号完整 appId（仅 5 个实测完整） | **不列**任何 appId |
| 3 | `openclaw automations add` 实际落盘 | **不实跑**（避免污染 61 条编排）；标 ⏳ |
| 4 | `plugins install` 全生命周期 | **不写**安装流程；见 chapters/12 |
| 5 | ClawHub publish 流程 | **不写**；标 ⏳ |
| 6 | A2A TCK 测试 | **不写**结果；见 chapters/10 |
| 7 | SLCP bridge demo | **不写** demo；标 ⏳ |
| 8 | `~/.openclaw/extensions/` 目录创建与加载 | 只写「本机不存在」这一 ✅ 事实 |
| 9 | MCP server 实际注册（本机 0 配置） | 只写 ✅ 的 14 子命令计数与 `mcp.servers` |

### 5.2.1 本文件额外标注的 ⏳（底稿之外，同样未实测）

| # | 项 | 处理 |
|---|---|---|
| 10 | `openclaw setup` / `onboard` 的 flag 清单 | 不列 |
| 11 | `openclaw agents bind` / `delete` 的精确参数形态 | 写「形态示意 ⏳」 |
| 12 | `openclaw plugins` / `mcp` 的具体子命令名 | 只写计数（15 / 14），不编名字 |
| 13 | `openclaw backup` 的恢复子命令名 | 不写；给两条路线（§W4） |
| 14 | `openclaw config` / `audit` / `pairing` / `promos` / `proxy` 的子命令与 flag | 不列 |
| 15 | 全局 flag（`--json` / `--verbose` / `--config` 等） | 不列 |
| 16 | OpenClaw 数字错误码表 | 以**现象**代替数字码（§4.0） |
| 17 | `cron add` 条目是否出现在 `automations list` | **不做断言**（§2.4.2） |
| 18 | `cron add --session` 的合法取值 | 不做断言（§2.10） |
| 19 | `agents delete` 是否联动删除 workspace 目录 | **不做断言**，按不可撤销对待 |
| 20 | Gateway 重启方式 | 未实测 |

---

## 5.3 本书的口径纪律（为什么这样写）

1. **⏳ 与 ✅ 必须分列。** 混在一段散文里，读者无法判断可信度。
2. **宁缺勿造。** 15 个 `plugins` 子命令的名字拿不到 → 就只写「15 个」。**不编名字**。
3. **不把推论写成事实。** 例如 §2.12 关于 pairing 的设计解读，已明确标「设计解读，非实测结论」。
4. **不把分析写成原始输出。** 例如 `agents list` 的模型分布是**统计口径**，已注明不是逐行原始文本。
5. **版本差异如实披露。** 2026.9.4（书内口径）vs 2026.9.6（本机 live）不一致处标 `[版本敏感]`。
6. **事故引证带来源。** 8/19 与 9/21 都给了证据文件/PR 号。

## 5.4 遇到 ⏳ 时读者该怎么做

```bash
# 1) 先跑该族 --help（唯一被允许的 --help 用法：验证你要跑的那一条）
openclaw plugins --help          # 应从输出数出 15 条
openclaw mcp --help              # 应从输出数出 14 条

# 2) 再在只读命令上确认行为
openclaw plugins list
openclaw mcp list

# 3) 涉及写操作：先备份
openclaw backup create

# 4) 把你实测到的事实回填进 api-reference/00-实测事实底稿.md
```

> **底稿回填是本书的更新机制。** 本文件的所有 ⏳，都是下一轮的待办。你实测完，把它升级成 ✅，本手册就前进一格。

---

## 5.5 一句收尾

> 本文件的可靠性承诺只有一句：
> **标 ✅ 的，我跑过；标 ⏳ 的，我没有，所以我不替它担保。**

---

## 附 · 互链索引（本文件 ↔ 全书）

### 按 FAQ
| 链接 | 主题 | 本文件相关节 |
|---|---|---|
| F1-环境与安装 | 安装、版本、命令真名 | §1, §2.1, §2.9, §2.15.1, E1, E2, E12 |
| F2-协议-SOUL-AGENTS-USER | 协议、绑定、准入 | §2.2.3-2.2.4, §2.12, W3, E4, E5, E12 |
| F3-心跳与定时 | heartbeat / cron | §2.4, §2.10, W5, E6, E7 |
| F4-记忆与会话 | session / 压缩 | §2.3, W5, E8 |
| F5-Skills-Tools-MCP | 技能/工具/MCP | §2.5, §2.7, §2.15.2, W5, E9, E10 |
| F6-多Agent协同 | 多 agent、A2A | §2.2, §2.6, §2.12, W2, E3, E5, E11 |
| F7-治理漂移体检 | 漂移、审计、备份 | §2.8, §2.11.2, W4, E7 |
| F-Top20-高频速查 | 高频问题速查 | 全书 |

### 按 Cookbook
| 链接 | 主题 | 本文件相关节 |
|---|---|---|
| C1-协议 SOUL | 单 agent 灵魂文件 | §2.2.2（建 agent 前置） |
| C2-协议 HEARTBEAT/MEMORY | 心跳与记忆 | §2.10, W5, E6, E8 |
| C3-Skills/Tools/MCP | 技能/工具/MCP 实战 | §2.5, §2.7, §2.15.2, E9, E10 |
| C4-训练轮次 | 训练流程 | §2.3 |
| C5-漂移治理 | 漂移治理 | §2.8, §2.11.2, W4 |
| C6-协同舰队 | 多 agent 舰队 | §2.2, §2.6, W2, W3 |
| C7-生产运维 | 生产运维 | §2.3, §2.9, W5 |

### 按 SOP
| 链接 | 主题 | 本文件相关节 |
|---|---|---|
| SOP-1 环境搭建 | 从零装起 | §2.1, W1, E1, E2 |
| SOP-2 协议配置 | 配置协议与绑定 | §2.2.3, §2.11.1, W3, E4, E12 |
| SOP-3 心跳监控 | 心跳巡检 | §2.4, §2.10.1, W5, E6 |
| SOP-4 记忆训练 | 记忆与压缩 | E8 |
| SOP-5 漂移治理 | 治理与审计 | §2.11.2, W4 |
| SOP-6 事故恢复 | 事故恢复 | §2.8, §2.12, W4, W5, E5, E7 |

### 按章节
| 章节 | 主题 | 本文件相关节 |
|---|---|---|
| chapters/02-七大契约 | 协议契约 | §2.6.1（三重撞名） |
| chapters/03-系统骨架 | 系统结构 | §2.11.1（20 顶层 key） |
| chapters/06-治理系统 | 治理 | §2.4.1（能力矩阵事故） |
| chapters/09-MCP绑定 | MCP | §2.5 |
| chapters/10-A2A绑定 | A2A | E11 |
| chapters/11-skill-registry | 技能注册 | §2.15.2, E9 |
| chapters/12-plugin-entrypoint | 插件入口 | §2.7.3 |

### 本卷内互链
| 文件 | 内容 | 本文件相关节 |
|---|---|---|
| `00-实测事实底稿.md` | 共用事实底稿 | §5.1, §5.2 |
| `02-config-reference.md` | 配置专册 | §2.11.1, §2.6.2 |
| 其余分册 | 见 api-reference/README | — |

---

**文件版本**：v1.0 · 2026-09-28
**编制**：天策（编写 Agent）
**事实来源**：`api-reference/00-实测事实底稿.md`（v1.0 · 2026-09-28）
**纪律**：本文件不跑全量 `--help` 采集；凡底稿未覆盖者，一律标 ⏳，不自行实跑查证。

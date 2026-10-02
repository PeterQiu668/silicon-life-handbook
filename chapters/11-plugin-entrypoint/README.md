# 第 11 章 · Plugin 入口：把硅基生命训练学装进 OpenClaw

> **v5.0 行业标准版 banner**：本章对应 OpenClaw 训练学第 11 章（接口层 4 / 4 · 工程接口层 · 分发层）；详见 [book README](../../README.md)。
> **License banner**：MIT（基于 OpenClaw 主仓 `LICENSE` 法律文本）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.6 (eb377ac)`（本书统一口径为 `2026.9.4 (3a9d69d)`）。
> **业界对位**：本章对应 **ClawHub 生态 + `openclaw.plugin.json`（JSON5）清单 + 15 子命令生命周期**——业界 6 大框架均无"plugin = 训练学外化"这一哲学。
> **本章叙事目标**：正文以训虾哲学散文为主；操作手册、常见错误、新手坑、扩展阅读、诚实边界见章末「附录 A」原文区块（一字未删）。

---

## 11.0 为什么这一章存在

### 11.0.1 一个不太浪漫的问题：你的训练学，别人怎么装

前面十章，我们把一套训练学讲完了：契约怎么立、骨架怎么搭、双三角怎么转、漂移怎么治、治理怎么分权、军团怎么协同、超维怎么生成、接口怎么接。

现在问一个不太浪漫的问题：

**如果有人想把你这套东西，装到他自己那台机器上，他该敲什么命令？**

不是"读哪些文件"，不是"照哪些步骤做"。而是：有没有一条命令，敲下去，东西就进去了？

这个问题听起来像工程细节，其实是**一套方法论能否脱离作者而存在**的分水岭。

- 如果答案是"没有，你得照着文档一步步配"——那么你的方法论是**一篇论文**。论文靠人复现，复现率通常很低。
- 如果答案是"有，`openclaw plugins install <你的包>`"——那么你的方法论是**一个产品**。产品靠安装，安装率是"能不能被装"决定的。

**这一章要讲的，就是怎么把一套方法论，从"论文"变成"产品"。**

### 11.0.2 为什么"装得上"比"讲得好"更难

讲得好是表达问题，装得上是一整套工程问题的总和。

要让别人能装，你至少要同时解决七件事：

1. **清单**：得有一个文件，说清这个包叫什么、版本多少、需要什么配置、会往系统里放什么。
2. **能力声明**：得说清它会占用哪些工具名、哪几个通道、会不会在启动时加载——因为**用户有权在装之前知道你动了什么**。
3. **配置模式**：得给它一个可校验的配置结构（JSON Schema），因为用户的配置不该靠猜。
4. **构建产物**：得区分"源工程"和"可安装产物"，因为运行时不读你的源码。
5. **打包**：得有一个不可篡改的产物（含校验和），因为你发布的是那个字节流，不是你的目录。
6. **安装与启用分离**：得把"把文件放进去"和"让它开始工作"分成两步——因为它们的安全性完全不同。
7. **治理入口**：得知晓怎么诊断、怎么禁用、怎么卸载、怎么回滚。

**这七件事，任何一件缺失，这个包就不能被一个陌生人安全地装上。**

而这七件事，恰好就是 `openclaw plugins` 这个命令族存在的理由。本章后面的十五个子命令、七阶段生命周期、JSON5 清单字段表，全部是在回答这七个问题。

### 11.0.3 一个必须当场纠正的错觉：装 ≠ 生效

这是本章最重要的一句话，值得单独占一节：

> **`openclaw plugins install` 之后，插件不会工作。你必须再跑 `openclaw plugins enable`。**

为什么这个设计是对的？

因为**"把代码放进我的机器"和"让这段代码开始影响我的行为"是两个风险等级完全不同的事件。**

- install 的风险是：磁盘上多了些文件。可控、可回滚、影响面接近零。
- enable 的风险是：它开始注册工具、可能占用通道、可能启动时加载、可能改你的配置行为。这是**行为面的介入**。

把两者合并成一个命令，等于让用户在"想看看这是什么"的意图下，直接同意了"让它介入我的运行期"。

所以真名是两步：

```bash
openclaw plugins install <path-or-spec-or-plugin> --accept-capabilities
openclaw plugins enable  <id> --accept-capabilities
```

注意两处都出现了 `--accept-capabilities`。这不是重复，这是**两次独立的确权**——因为 manifest 升级可能在你不知情时引入新能力，而 `enable` 是最后一次你能说"不"的地方。

**本章后面所有的操作纪律，都可以追溯回这一条。**

### 11.0.4 七个名字，和一个高频误植的行业

插件这件事在行业里流传得很快，也传错得很快。以下七组是本章实测确认的真名对照（完整证据链见本章 `真名验证与勘误.md`）：

| # | 业界常说 | OpenClaw 真名 |
|---|---|---|
| 1 | `openclaw plugin install` | **`openclaw plugins install`**（复数） |
| 2 | `manifest.yaml` | **`openclaw.plugin.json`**（**JSON5**，不是 YAML） |
| 3 | manifest 是输入文件 | manifest **既是生成产物**（`plugins build` 写入）**也是配置入口**（手写 + `plugins init` 脚手架） |
| 4 | 安装目录 `~/.openclaw/workspace/plugins/` | **`~/.openclaw/extensions/`**（workspace 下无 plugins 目录） |
| 5 | 配置入口 `~/.openclaw/config.yaml` | **`~/.openclaw/openclaw.json`**（JSON5，注释敏感） |
| 6 | `github.com/openclaw/openclaw/rfcs` | **不存在**（真路径 = Issue 模板 + Discord + ClawHub） |
| 7 | manifest 无 `categories` | 有，且 **bundled plugin 必须声明恰好一个 active category** |

**为什么要用一整节讲这个？**

因为第 1、2、4、5 条中的任何一条被写错，读者敲出来的命令就会失败，而失败信息不会告诉你"你该用复数"。**一个错误的真名，会让读者以为这个能力不存在。**

### 11.0.5 本章与相邻章节的边界（避免重复阅读）

接口层四块拼图，本章是最后一块：

```text
[第 8 章 MCP 绑定]   agent ↔ 工具      发现协议
[第 9 章 A2A 绑定]   agent ↔ agent     协作协议
[第 10 章 Skill 注册] 能力 ↔ 能力库     载体格式
[第 11 章 Plugin 入口] 训练学 ↔ 用户    安装分发（你在这里）
```

一句话分清三者：

- **Skill** = 一页剧本（Markdown · 跨平台 · 按需装载）。第 10 章。
- **MCP server** = 一间工具房（协议化 · 跨进程 · 可发现）。第 8 章。
- **Plugin** = 整个剧组（JSON5 清单 + 可执行代码 + 生命周期 + 分发通道）。**本章。**

**Plugin 是 Skill 的超集**：一个 plugin 可以携带 N 个 skill（清单里的 `skills` 字段）、M 个 tool（`contracts.tools`）、若干 channel 与 hook。第 10 章写的 skill，可以在本章被"打包"进一个 plugin 里分发出去。

### 11.0.6 本章要回答的八个问题

1. plugin 到底是什么？它和 Skill、MCP server 的分界线画在哪？
2. `openclaw.plugin.json` 的字段有哪些是必填？`configSchema` 为什么有硬格式要求？
3. `openclaw plugins` 的 15 个子命令分别管什么？高频组合拳是什么？
4. 为什么 `install` 之后必须 `enable`？`--accept-capabilities` 在防什么？
5. `~/.openclaw/extensions/` 和 `~/.openclaw/workspace/plugins/` 的区别是什么？
6. ClawHub 是什么？publish 的 5 步是什么？反 PAM 约束是什么？
7. 训练学怎么装进 OpenClaw？（5 个差异化优势在 plugin 里的落点）
8. 哪些话不能说？（诚实边界：本节 11.12.4）

### 11.0.7 本章的组织方式

- **11.1 – 11.9｜九个核心概念**：每个概念同样按八步展开（定义 / 直觉 / 解剖 / 为什么 / 真名与实测 / 边界 / 反例 / 练习）。
- **11.10｜怎么做**：七步落地路径，从 `init` 到 `doctor`，含备份纪律。
- **11.11｜常见误区**：九个错误 + 30 秒自查。
- **11.12｜深度专题**：ClawHub 与 MCP 扩展机制（2026 前沿）/ 六大框架对位表 / 本机 plugin 实测审计 / 诚实边界。

**章末「附录 A」是本章的原操作手册与全部附件，逐字后移，一字未删。**

> ⚠ **关于附录 A 的一个阅读提示**：附录 A 区块是逐字保留的原章节体。其中出现的历史章号字样（如"第 12 章"）属于章号统一之前的口径；本书现行章号以文件首行为准——**本章 = 第 11 章 = 路径 `chapters/11-plugin-entrypoint/`**。

---

## 11.1 核心概念一 · plugin 是什么

### ① 一句话定义

**OpenClaw plugin 是一个可安装、可版本化、可确权、可在启动时加载的工程产物：它由一份 `openclaw.plugin.json`（JSON5 清单）描述，可以携带 skill / tool / channel / hook，装在 `~/.openclaw/extensions/` 下，由 `openclaw plugins` 命令族管理。**

### ② 现场直觉

如果 Skill 是**剧本**，plugin 就是**剧组**。

剧本是一份文本：谁都能读，谁都能演，改了立刻生效，不需要"制作预算"。

剧组不一样。剧组有编制表（清单）、有设备（tool）、有场地（channel）、有开机时间（activation）、有杀青流程（uninstall）。剧组一旦成立，就会**持续占用资源**——它在你没注意的时候也在那里。

这就是为什么 plugin 的每一步都给用户留了说"不"的位置：`--accept-capabilities` 会问三次（install / enable / update）。**因为剧组不是文本，它会动。**

### ③ 结构解剖

一个 OpenClaw plugin 的物理形态：

```text
~/.openclaw/extensions/<plugin-id>/
├── openclaw.plugin.json      ← 清单（JSON5）：身份 + 能力声明 + 配置模式 + UI 提示
├── dist/
│   └── index.js              ← 运行时入口（构建产物）
├── skills/                   ← 可选：携带的 SKILL.md（与第 10 章衔接）
├── plugin-runtime-deps/      ← 可选：运行期依赖（如 json5）
└── ...
```

对应的三层清单体系（**不要混**）：

| 层 | 清单文件 | 格式 | 谁读 |
|---|---|---|---|
| **L1 Skill 层** | `SKILL.md`（YAML frontmatter） | Markdown + YAML | agent 路由 / 客户端 |
| **L2 Tool 层** | 工具声明（`TOOLS.md` / MCP `tools/list`） | Markdown / JSON | agent 调用 |
| **L3 Plugin 层** | **`openclaw.plugin.json`** | **JSON5** | **OpenClaw 运行时** |

### ④ 为什么这样设计

**因为 plugin 是"能改变系统行为的东西"，所以它必须自带一份可被审阅的声明。**

这个设计选择带来三个后果，每一个都是刻意的：

**后果一：清单必须声明"我会往你系统里放什么"（capability）。**
`contracts.tools` 声明要注册哪些 tool 名；`channels` 声明占用哪些通道；`activation.onStartup` 声明是否在启动时加载。**用户在 install/enable 之前就能看到这些，并据此决定要不要接受。**

**后果二：清单是"生成产物 + 配置入口"的双重身份。**
`openclaw plugins build` 会写一批元数据（含 author / version / dist 等 `openclaw.install` 字段）。这让"源工程"和"可发布产物"可以分离，也让 `build --check` 能检出"产物是否过期"。

**后果三：配置必须是可校验的结构（`configSchema`）。**
用户的配置不该靠猜。`configSchema` 是一个 JSON Schema，硬要求是 `{type: "object", additionalProperties: false}`——后半句尤其重要：**它禁止了没声明过的字段**，从而杜绝"我配了个不存在的键，它默默地没生效"。

### ⑤ 真名与实测

| 项 | 真名 / 实测 | 来源 |
|---|---|---|
| 命令族 | **`openclaw plugins`**（复数） | `openclaw plugins --help` 实跑 |
| 子命令数 | **15** | 同上 |
| 清单文件 | `openclaw.plugin.json`（JSON5） | 本机 stock plugin 列表实跑 |
| 安装目录 | `~/.openclaw/extensions/` | 本机 `ls` 实测：**该目录本机不存在**（未装自定义 plugin） |
| 主配置 | `~/.openclaw/openclaw.json`（JSON5，注释敏感） | `openclaw plugins list` 头部输出 |
| 现状基线 | **Plugins (53/73 enabled)** | `openclaw plugins list` 实跑（本书早期基线为 51/69） |
| stock 来源根 | 随主包分发（`stock:` 前缀） | 本机实测，如 `stock:a2a/index.js` |
| 底座版本 | `2026.9.6 (eb377ac)` live / `2026.9.4 (3a9d69d)` 书内口径 | `openclaw --version` 实跑 |

**本机的真实状态**：73 个 plugin（以 stock 为主），其中 **53 个 enabled、20 个 disabled**。一个具体的 disabled 样本是 **`a2a`**——`stock:a2a/index.js`，状态 `disabled`。这很有教育意义：**A2A 能力在本机是"存在但未启用"的**，所以第 9 章关于 A2A 的一切都是"协议层可达 + 本机未开启"的口径。

### ⑥ 边界：什么时候不该做 plugin

**三类情况不要做 plugin：**

1. **它只是一段知识。** 那就写 `SKILL.md`（第 10 章）。用 plugin 承载"一段话"是杀鸡用牛刀——你付出了清单、构建、打包、确权、升级的全部成本，换来的只是"一段话"。
2. **你不打算分发、也不需要版本化。** 那就写脚本。plugin 的价值核心在**分发生命周期**；如果只是你自己用一次，脚本更省。
3. **它需要"永远在场且不可绕过"。** 这种情况应该走契约文件 + 系统配置，而不是"可被 disable 的 plugin"。**一个能被 disable 的红线，不是红线。**

### ⑦ 反例与失败模式

**反例一：把 plugin 当 skill 用。**
现象：一个 200 行 Markdown + 一份 `openclaw.plugin.json`，里面没有任何代码，只为了"看起来正式"。
后果：你会被迫维护 build / pack / validate 全流程，而收益为零。
正确：纯知识 → skill；纯逻辑 → script 或 plugin；**两者都想 → plugin 携带 skill**（用 `skills` 字段）。

**反例二：install 之后就以为完事了。**
这是本章的 P0 误区（11.4 与 11.11.3 详述）。`install` 只写文件 + 记一行 `plugins.installs`；**不 enable 就不会被加载。**

**反例三：去 `~/.openclaw/workspace/plugins/` 找安装目录。**
该路径**不存在**。真名是 `~/.openclaw/extensions/`。

### ⑧ 练习与验收

```bash
# 1) 命令族真名（复数）
openclaw plugins --help 2>&1 | head -6

# 2) 现状基线
openclaw plugins list 2>&1 | head -4          # 期望头行 Plugins (53/73 enabled)

# 3) 安装目录真名（本机可能不存在——这本身就是一个正确结果）
ls -la ~/.openclaw/extensions/ 2>&1 | head -5

# 4) 反例验证（应报错，证明真名是复数）
openclaw plugin 2>&1 | head -2
```

**验收标准**：你能说出 15 子命令里的 5 个，并能解释 baseline `53/73` 的两个数分别是什么口径。

---

## 11.2 核心概念二 · `openclaw.plugin.json`（JSON5）与 `manifest.yaml` 的辨析

### ① 一句话定义

**OpenClaw plugin 的清单文件真名是 `openclaw.plugin.json`，格式是 JSON5（不是 YAML）；`manifest.yaml` 这个名字在 OpenClaw 里不存在。**

### ② 现场直觉

这是一个纯粹的"名字错了一切都错"的问题。

你不太可能把 `manifest.yaml` 写出来之后还恰好让系统读懂它——因为你写的是 YAML，系统找的是 JSON5，而且文件名都不一样。所以这个错误的后果是**静默失败**：你觉得自己配置好了，实际上系统根本没看到你的清单。

**在插件体系里，最危险的失败不是报错，是沉默。**

### ③ 结构解剖（16 个字段）

本表 16 个字段经本机 stock plugin 实测 + 官方文档双源交叉确认：

| # | 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| 1 | `id` | string | ✅ | 唯一标识；小写 + 连字符；不可含 `/` |
| 2 | `name` | string | ❌ | 人类可读名称 |
| 3 | `description` | string | ❌ | 一行功能描述 |
| 4 | `kind` | enum | ❌ | 类型标签（memory / channel / tool / provider / hook…） |
| 5 | `categories` | string[] | ❌ | **bundled plugin 必须声明恰好一个 active category** |
| 6 | `channels` | string[] | ❌ | 占用哪些 channel 名 |
| 7 | `skills` | string[] | ❌ | 携带的 `SKILL.md` 路径（**与第 10 章衔接**） |
| 8 | `contracts.tools` | string[] | ❌ | 注册到 tool registry 的 tool 名（**OpenClaw 借此发现 ownership，不必 eager-load runtime**） |
| 9 | `activation.onStartup` | boolean | ❌ | Gateway 启动时是否 eager-load |
| 10 | `activation.onEvent` | string | ❌ | 事件驱动激活（如 first-message / first-tool-call） |
| 11 | `configSchema` | JSON Schema | ✅ | **硬要求 `{type:"object", additionalProperties:false}`** |
| 12 | `uiHints.<key>` | object | ❌ | 控制 UI 表单渲染（`sensitive` = 密码框，`advanced` = 折叠） |
| 13 | `openclaw.install` | object | ❌ | 包元数据（**`plugins build` 写入的生成产物**） |
| 14 | `channelConfigs` | object | ❌ | channel 插件用；镜像 JSON Schema 到 channel 子模块 |
| 15 | `capabilityCatalogEntry` | string | ❌ | 轻量 capability 模块路径 |
| 16 | `exposure` | enum[] | ❌ | channel 插件的可见性标签 |

最小可用清单示例：

```json5
{
  id: "silicon-life-training",
  name: "硅基生命训练学",
  description: "把训练学的契约、教练机制与漂移治理装进 OpenClaw。",
  categories: ["other"],
  skills: ["./skills"],
  contracts: { tools: ["silicon_life_drift_audit"] },
  activation: { onStartup: false },       // 不要拖慢启动
  configSchema: {
    type: "object",
    additionalProperties: false,          // ← 硬要求
    properties: {
      agentName: { type: "string", description: "目标 agent 名" },
      auditInterval: { type: "string", description: "审计节律（如 30m）" }
    },
    required: ["agentName"]
  },
  uiHints: {
    agentName: { label: "目标 Agent", placeholder: "比如 tiance" },
    auditInterval: { label: "审计节律", advanced: true }
  }
}
```

### ④ 为什么用 JSON5 而不是 YAML

这是一个"为什么 skill 用 YAML，plugin 用 JSON5"的对照问题：

| 维度 | `SKILL.md` frontmatter | `openclaw.plugin.json` |
|---|---|---|
| 格式 | **YAML** | **JSON5** |
| 面向 | 人写、人读为主 | 机器生成 + 人可手改 |
| 允许注释 | YAML `#` | JSON5 `//` `/* */` |
| 允许尾逗号 | N/A | ✅ |
| 单引号字符串 | ✅ | ✅ |
| 无引号 key | ✅ | ✅（identifier 形式） |
| 与现有工具的兼容 | Markdown 生态 | JS/TS 生态（`JSON.parse` 的宽松超集） |

**JSON5 是 JSON 的"人类友好超集"**：它让清单既能被 JS 直接 `require`/`JSON5.parse`，又能让维护者在文件里写注释解释"这个字段为什么要设成这样"。

**但这里有一个真实的陷阱**：

```bash
openclaw config set ...
# ⚠ 该命令默认会把 JSON5 改写为标准 JSON —— 带注释的字段会被无声丢弃
```

所以对训练学 plugin（它会大量写注释解释字段意图）来说，纪律是：

- ✅ **手编 + 定点修改**，保住注释；
- ⚠ **不要用整体重写型命令**去改它；
- ✅ **改前先 `openclaw backup create`**。

### ⑤ 真名与实测

| 项 | 实测 | 证据位置 |
|---|---|---|
| 清单真名 | `openclaw.plugin.json` | 本机 stock plugin 目录实测 |
| 格式 | JSON5（含注释与尾逗号） | 同上 |
| `~/.openclaw/extensions/` | **本机不存在** | `ls` 实测（未装自定义 plugin） |
| 主配置真名 | `~/.openclaw/openclaw.json` | `openclaw plugins list` 头部输出 |
| 配置里的 plugin 分区 | `plugins.installs` / `plugins.entries` / `plugins.allow` / `plugins.deny` | 社区 plugin 安装脚本行为描述 |
| runtime 依赖坑 | `json5` 必须包含在 `plugin-runtime-deps/` | 上游 issue #77461（已修）：缺 `json5` 会让 `memory_search` 失败 |

**关于最后一个坑，值得单独说**：这条 issue 的教学价值在于——**plugin 的运行期依赖不复用主程序的依赖树**。你必须显式把它要用的包放进 `plugin-runtime-deps/`。否则在开发者机器上跑得好好的，到用户机器上第一次调用就炸。

### ⑥ 边界

- **`additionalProperties: false` 不是可选项。** 它保证了"配置里没有未声明的字段"。如果你的使用者配了一个键却发现没生效，九成是因为你没把那个键写进 `properties`。
- **`categories` 对 bundled plugin 有硬约束**（恰好一个 active category）。社区 plugin 的约束较松，但乱填会让控制台分类混乱。
- **不要把密钥写进清单。** 清单会被读取、被打印、被 diff。密钥属于 `uiHints` 声明的 `sensitive` 字段——让用户在自己的配置里填。

### ⑦ 反例与失败模式

**反例一：`manifest.yaml`。**
文件名错 + 格式错，双错。系统找不到清单，但不会友好地告诉你"我要找的是 openclaw.plugin.json"。

**反例二：`category`（单数）。**
真名是 `categories`（数组）。写了单数=多了一个未声明字段（在不同解析强度下行为不一）。

**反例三：`entry` / `main` 当入口字段。**
真名是 `activation.onStartup` / `activation.onEvent`。

**反例四：`configSchema` 缺 `additionalProperties: false`。**
表现是"配置校验形同虚设"——用户填了错字键名，系统不报错，只是那项配置不生效。这是最贵的一类 bug，因为它把配置错误推迟到了运行期的某次调用。

**反例五：`activation.onStartup: true` 滥用。**
每次 Gateway 启动都 eager-load 你的插件 → 启动变慢。**默认应该 `false`，用 `onEvent` 做事件驱动激活。**

### ⑧ 练习与验收

```bash
# 1) 看你本机 stock plugin 的真实清单（找一个存在的）
find "$(npm root -g)/openclaw/dist/extensions" -name 'openclaw.plugin.json' 2>/dev/null | head -3

# 2) 逐字段核对（id / configSchema / categories）
f=$(find "$(npm root -g)/openclaw/dist/extensions" -name 'openclaw.plugin.json' 2>/dev/null | head -1)
sed -n '1,40p' "$f" 2>/dev/null

# 3) 反例检测：全盘应无 manifest.yaml
find ~/.openclaw -name 'manifest.yaml' 2>/dev/null | wc -l      # 期望 0

# 4) JSON5 可解析性自检（需 node 侧 json5）
# node -e "const j=require('json5');console.log('✓ JSON5 OK')"
```

**验收标准**：你能不看笔记说出 `configSchema` 的硬格式要求，并解释 `additionalProperties: false` 在防什么。

---

## 11.3 核心概念三 · 十五个子命令

### ① 一句话定义

**`openclaw plugins` 是一个 15 子命令的命令族，覆盖 plugin 的完整生命周期：脚手架 → 构建 → 打包 → 验证 → 安装 → 启用 → 诊断 → 更新 → 卸载。**

### ② 现场直觉

把 15 个子命令想成一条**工厂流水线**，而不是 15 个孤立的命令。

工人不会随机去按按钮；他按工序走。你也不该随机挑命令敲；你应该知道自己在工序的哪一步。

这也解释了为什么"忘了 enable"是本章最高频的错误——**因为 enable 是流水线的第 6 道工序，而 install 是第 5 道。人在第 5 道之后会有强烈的"做完了"的感觉。**

### ③ 结构解剖（实测输出）

```text
$ openclaw plugins --help
OpenClaw 2026.9.4 (3a9d69d) — All your chats, one OpenClaw.

Usage: openclaw plugins [options] [command]
Manage OpenClaw plugins and extensions

Commands:
  build        Build plugin metadata and native Control UI assets
  disable      Disable a plugin in config
  doctor       Report plugin load issues
  enable       Enable a plugin in config
  init         Create a plugin project
  inspect      Inspect plugin details
  install      Install a plugin or hook pack (path, archive, npm spec, git repo,
               clawhub:package, or marketplace entry)
  list         List discovered plugins
  marketplace  Inspect Claude-compatible plugin marketplaces
  pack         Bundle a built plugin into an exact artifact for activation approval
  registry     Inspect or rebuild the persisted plugin registry
  search       Search ClawHub plugin packages
  uninstall    Uninstall a plugin
  update       Update installed plugins and tracked hook packs
  validate     Validate plugin metadata and native Control UI assets
```

**按生命周期分组：**

| 阶段 | 子命令 | 关键 flags |
|---|---|---|
| 脚手架 | `init` | `--directory` / `--type`(tool/provider/feature) / `--name` |
| 构建 | `build` | `--check`（产物过期检测）/ `--entry` |
| 打包 | `pack` | `--out` / `--root`；输出含 SHA256 + activation request |
| 验证 | `validate` | `--root` / `--entry` / `--json` |
| 安装 | `install` | **6 种源**：path / archive / npm spec / git repo / `clawhub:package` / marketplace entry；`--accept-capabilities` / `--force` / `--pin` / `-l(--link)` |
| 列表 | `list` | `--enabled` / `--verbose` / `--json` |
| 诊断 | `doctor` | `--json`（报告 discovery / module loading / compatibility / configuration 四类问题） |
| 启用 | `enable` | **`--accept-capabilities` 必备** |
| 禁用 | `disable` | 无 flag |
| 卸载 | `uninstall` | `--dry-run` / `--force` / `--keep-files` |
| 更新 | `update` | `--all` / `--dry-run` / `--accept-capabilities` |
| 注册表 | `registry` | `--refresh`（从 manifest 重扫）/ `--json` |
| 市场 | `marketplace` | `entries` / `list` / `refresh` |
| 搜索 | `search` | query / `--limit <n>` / `--json` |
| 检视 | `inspect` | `--all` / `--runtime`（检 hooks/tools/diagnostics）/ `--json` |

### ④ 为什么这样设计

**设计一：把"验证"和"打包"分开。**
`validate` 只校验、`pack` 只打包。分开的好处是：CI 可以只跑 `validate`（快、无副作用），发布时才跑 `pack`。

**设计二：`build --check` 的存在等于承认"产物会过期"。**
显式承认"源改了但产物没重建"是一个真实且高频的故障，并给它一个可被 CI 捕获的入口。**这是一个成熟工具链的标志**——它不假装你不会犯错，它给你一个探测错误的手段。

**设计三：`doctor` 单独存在。**
诊断不是 install 的一部分。你可以在任何时候对任何状态跑 `doctor`。而且是四类问题分类报告（发现 / 模块加载 / 兼容性 / 配置），不是一句"有问题"。

**设计四：`uninstall` 有 `--dry-run` 和 `--keep-files`。**
破坏性操作必须可预演、可保留现场。这与本书"破坏性操作前先备份"的纪律同源。

### ⑤ 真名与实测

```bash
# 子命令总数（本机实测 15）
openclaw plugins --help 2>&1 | grep -cE '^  [a-z]'

# 逐条可见
openclaw plugins --help 2>&1 | grep -E '^  (init|build|pack|validate|install|list|doctor|enable|disable|uninstall|update|registry|marketplace|search|inspect)'

# 现状基线
openclaw plugins list 2>&1 | head -4
```

**高频组合拳（可直接复制）：**

```bash
# 完整生命周期 5 步
openclaw plugins init silicon-life-training --type feature --name "硅基生命训练学" --directory ./silicon-life
cd silicon-life
openclaw plugins build --root .
openclaw plugins pack --root . --out ./silicon-life-training.tgz
openclaw plugins validate --root . --entry ./dist/index.js
openclaw plugins install ./silicon-life-training.tgz --accept-capabilities

# 运维 3 件套
openclaw plugins doctor
openclaw plugins list --enabled --verbose
openclaw plugins update --all --dry-run

# 安全网（任何破坏性操作前）
openclaw backup create
```

### ⑥ 边界

- **`validate` 通过 ≠ 能跑。** 它校验的是 metadata 与 Control UI assets 的结构，不是运行期行为。**运行期验证只能靠 `enable` 之后触发一次。**
- **`--force` 不要当常规选项。** 它跳过确认，只在"我已经知道会发生什么、且备份在手"时使用。
- **`--pin` 是给生产用的。** 钉死版本，避免自动升级引入新 capability。
- **`registry --refresh` 是重建本机持久化注册表**，与 ClawHub（远端分发）不是一回事。**这两个"registry"概念必须分清**——一个是本机状态缓存，一个是远端包索引。

### ⑦ 反例与失败模式

**反例一：单数命令。**
`openclaw plugin install` → command not found → 结论"OpenClaw 不支持插件"。**真名是复数。**

**反例二：跳过 `build` 直接 `install` 源工程。**
运行时不读源码。没有 build 产物 → 装上了也没法跑。

**反例三：跳过 `validate` 直接 `pack`。**
`pack` 会产出带 SHA256 的 artifact，并生成 activation request。**结构错的 manifest 会一路打包成功，直到用户 install 时才炸。** 在打包前 validate，成本是 3 秒。

**反例四：把 `doctor` 当 install 的一部分。**
只有出问题时才跑 `doctor`，是浪费了它最大的价值：**在"目前看起来正常"的时候建立基线**。

### ⑧ 练习与验收

```bash
# 1) 把 15 个子命令抄一遍（手抄，不用复制——这是为了让工序刻进记忆）
openclaw plugins --help 2>&1 | sed -n '/^Commands:/,/^$/p'

# 2) 建立你的基线快照（每季度跑一次）
{
  date '+%Y-%m-%d %H:%M:%S'
  openclaw --version 2>&1 | tail -1
  openclaw plugins list 2>&1 | head -2
  openclaw plugins doctor 2>&1 | tail -20
} | tee ~/plugin-baseline-$(date +%Y%m%d).txt

# 3) 只读演练（安全，不做任何改动）
openclaw plugins update --all --dry-run 2>&1 | head -10
```

**验收标准**：你能默写出"从 init 到 doctor"的 8 道工序顺序，并指出哪一步开始"会改变系统状态"。

---

## 11.4 核心概念四 · install ≠ enable

### ① 一句话定义

**`openclaw plugins install` 只做两件事：把文件放到 `~/.openclaw/extensions/<id>/`，并在 `~/.openclaw/openclaw.json` 里记一行 `plugins.installs.<id>`；它不会让插件工作——只有 `openclaw plugins enable <id>` 才会把 `plugins.entries.<id>.enabled` 置为 `true`。**

### ② 现场直觉

这是"把书买回家"和"把书读了"的区别。

买回家（install）之后，书在你书架上，物理上属于你，但它不会改变你的任何行为。

读了（enable）之后，它才开始影响你的判断。

**世界上没有人会认为"买了书就等于读了书"。但世界上大量的人会认为"装了插件就等于插件生效了"**——因为这个错觉没有被任何报错提示挡住。

### ③ 结构解剖

三态分离（**这是本章最重要的心智模型**）：

| 状态 | 存储位置 | 含义 | 观测命令 |
|---|---|---|---|
| **① 库存（discovered）** | `~/.openclaw/extensions/` 下的目录 | 文件在磁盘上 | `openclaw plugins list` |
| **② 安装记录（installs）** | `openclaw.json#plugins.installs.<id>` | 系统知道它被装过 | 同上（含 source 列） |
| **③ 启用（enabled）** | `openclaw.json#plugins.entries.<id>.enabled = true` | **运行期会加载** | `openclaw plugins list --enabled` |

完整的两步 + 验证：

```bash
# 第 1 步 · 安装（写文件 + 记一行 installs）
openclaw plugins install <path-or-spec> --accept-capabilities

# 第 2 步 · 启用（置 enabled = true —— 关键的一步）
openclaw plugins enable <id> --accept-capabilities

# 第 3 步 · 验证真的进了运行期
openclaw plugins list --enabled --verbose | grep <id>
openclaw plugins doctor
```

### ④ 为什么这样设计

**因为"存在"、"被记录"、"被加载"是三种不同的风险等级，合并它们等于剥夺用户的选择权。**

- 库存：风险 ≈ 磁盘空间。可回滚（删目录）。
- 安装记录：风险 ≈ 配置多一行。可回滚（删那行）。
- 启用：风险 = **它开始注册工具名、可能占用通道、可能在启动时加载、可能改变你的配置行为**。这是**行为面的介入**。

把三者合并成一个命令，用户就无法表达"我想先看看它是什么"这个完全合理的意图。

**`--accept-capabilities` 的精妙之处在于它出现了三次：**

```bash
openclaw plugins install <spec> --accept-capabilities   # 第 1 次：接受当前声明的能力
openclaw plugins enable  <id>   --accept-capabilities   # 第 2 次：确认进入运行期
openclaw plugins update  <id>   --accept-capabilities   # 第 3 次：接受升级后可能新增的能力
```

第 3 次是关键——**manifest 升级可能引入新的 capability**（比如原来只要 `read_file`，新版要 `terminal`）。如果没有第 3 次确权，一次 `update` 就能悄悄扩大一个已经在你系统里运行的插件的权力。

**这是一条值得抄进任何 agent 系统设计里的原则：能力扩张必须重新确权。**

### ⑤ 真名与实测

```bash
# 现状：本机 53/73 enabled（20 个 disabled）
openclaw plugins list 2>&1 | head -2
# Plugins (53/73 enabled)

# 一个具体 disabled 样本：a2a
openclaw plugins list 2>&1 | grep -i 'a2a'
# │ A2A │ a2a │ openclaw │ disabled │ stock:a2a/index.js │ 2026.9.6 │
```

**关于 `a2a` 这个样本的三个诚实说明**：

1. 它是 **stock** plugin（随主包分发），不是社区插件；
2. 它的状态是 **disabled**——这意味着**本机 A2A 能力未启用**；
3. 因此第 9 章的一切 A2A 内容是"协议可达 + 本机未开启"的口径；**不得写成"本机 A2A 已在运行"**。

**关于未启用 ≠ 坏了**：本机 20 个 disabled 里，多数是 stock 默认禁用（因为不是每个部署都需要全部能力）。**`disabled` 是策略状态，不是质量状态。**

### ⑥ 边界

- **不要"先 enable 再看"。** 尤其是来源不明的第三方插件：先 `inspect --all`，看它的 `contracts.tools` / `channels` / `activation`，再决定。
- **不要在没备份的情况下 enable。** `openclaw backup create` 是 3 秒的事。
- **不要忘了 `update` 也要确权。** 升级不是"原地替换文件"，它可能是"权力扩张"。
- **`plugins.allow` / `plugins.deny` 是治理位。** 除了 enabled 与否，allow/deny 提供了更明确的策略表达——**这是做"白名单制"部署的入口。**

### ⑦ 反例与失败模式

**反例一：install 完就宣布上线。**
症状：一周后发现插件的工具从来没被调用过。
排查路径：`list --enabled` 里没有它 → 忘 enable。

**反例二：把 install 当成"安装并启用"。**
根因是"安装"这个词在人类语言里的默认含义（装完就能用）。**对抗方式：把这两步写进你自己的上线清单（checklist），而不是靠记性。**

**反例三：enable 之后不验证。**
`enable` 只是改了配置。要验证"真的进了运行期"，需要：`list --enabled` 有它 + `doctor` 无 error + **触发一次**（TEV 三证据：命令 + 输出 + 时间戳）。

**反例四：`--force` 掩盖了确权。**
`--force` 跳过确认。如果你在一个自动化脚本里长期使用它，你就等于永久关闭了三次确权机会。

### ⑧ 练习与验收

```bash
# 1) 三态同时观测
echo "--- 库存 ---";    openclaw plugins list 2>&1 | head -2
echo "--- 已启用 ---";  openclaw plugins list --enabled 2>&1 | head -2
echo "--- 配置位 ---";  grep -n '"plugins"' ~/.openclaw/openclaw.json 2>/dev/null | head -3

# 2) 找一个 disabled 的（本机有 20 个），不启用它，只 inspect
openclaw plugins list 2>&1 | grep 'disabled' | head -5
# openclaw plugins inspect <id> --all        # ← 先看清楚，再决定

# 3) 上线前 checklist（建议写进你的团队规范）
cat <<'EOF'
[ ] 已 inspect --all 看过能力声明
[ ] 已 openclaw backup create
[ ] install 成功（source 列可见）
[ ] enable 成功（--accept-capabilities 已确认）
[ ] list --enabled 可见
[ ] doctor 无 error
[ ] 真触发一次（有日志/时间戳证据）
EOF
```

**验收标准**：你能解释"为什么 install 和 enable 不能合并"，并说出 `--accept-capabilities` 三次出现分别在防什么。

---

## 11.5 核心概念五 · `~/.openclaw/extensions/` 与两个"registry"

### ① 一句话定义

**plugin 的安装目录真名是 `~/.openclaw/extensions/`（不是 `~/.openclaw/workspace/plugins/`）；同时"registry"这个词在本章有两个完全不同的所指——本机持久化注册表与 ClawHub 远端包索引。**

### ② 现场直觉

两个"找不到"的坑，恰好成对出现：

- 你装完了插件，去 `~/.openclaw/workspace/plugins/` 找它 → **这个目录不存在**；
- 你想搜一个包，跑 `openclaw plugins registry xxx` → 语法不对（registry 是用来"检视/重建本机注册表"的，搜包要用 `search`）。

**这两个坑的共同根因是：凭直觉命名。** 在 plugin 这件事上，直觉基本都错——`workspace/` 下确实有很多东西（skills / agents / references），但 plugins 不在其中。

### ③ 结构解剖

**目录真名对照表：**

| 你会以为的路径 | 真名 | 内容 |
|---|---|---|
| `~/.openclaw/workspace/plugins/` | **不存在** | — |
| — | **`~/.openclaw/extensions/`** | 已安装的 plugin 目录（本机不存在=未装自定义 plugin） |
| — | 主包 `dist/extensions/` | **stock plugins**（随主包分发，`stock:` 前缀） |
| `~/.openclaw/config.yaml` | **`~/.openclaw/openclaw.json`** | 主配置（JSON5，顶层含 `plugins` key） |

**两个 registry：**

| 名称 | 是什么 | 命令 | 作用范围 |
|---|---|---|---|
| **本机持久化 plugin registry** | 本机状态缓存（已知插件、来源、版本） | `openclaw plugins registry`（`--refresh` 重扫 / `--json`） | **本机** |
| **ClawHub** | 远端包索引 + 分发服务 | `openclaw plugins search`（检视用）/ `clawhub package publish`（发布用） | **远端生态** |

**配置里 plugin 相关的四个分区（真名）：**

```json5
// ~/.openclaw/openclaw.json
{
  plugins: {
    installs: { "some-plugin": { /* 安装记录：来源、版本、时间 */ } },
    entries:  { "some-plugin": { enabled: true /* ← enable 改的就是这里 */ } },
    allow:    [ /* 白名单 */ ],
    deny:     [ /* 黑名单 */ ],
    slots:    { /* 槽位 */ }
  }
}
```

### ④ 为什么这样设计

**设计一：安装目录与工作区分离。**
`workspace/` 是**你的内容**（skills、agents、references）；`extensions/` 是**别人给你的代码**。把两者放在同一个父目录下，会让"哪些东西是我写的、哪些是装进来的"变得模糊——而这是一个安全边界。

**设计二：stock 与社区 plugin 分源管理。**
stock plugin 随主包分发（升级主包即升级），社区 plugin 装在 `extensions/`。它们的**可信级别不同**：前者来自主包供应链，后者需要你逐次确权。`list` 输出里的 source 列（`stock:`、`clawhub:`、path 等）就是在表达这个差别。

**设计三：本机 registry 与远端索引分离。**
本机 registry 服务于"我装了什么、它从哪来、现在还在不在"；ClawHub 服务于"生态里有什么"。**混为一个是常见误植**，而混淆的后果是：你会去改本机 registry 试图"发布"，或者去 ClawHub 找"我本机装了什么"。

### ⑤ 真名与实测

```bash
# 安装目录真名（本机不存在——这是一个正确结果）
ls -la ~/.openclaw/extensions/ 2>&1 | head -3
# 反例目录（应报 No such file or directory）
ls -la ~/.openclaw/workspace/plugins/ 2>&1 | head -3

# stock 来源根（本机实测）
openclaw plugins list 2>&1 | head -6
# Source roots:
#   stock: /Users/peterqiu/.npm-global/lib/node_modules/openclaw/dist/extensions
```

| 项 | 本机实测 |
|---|---|
| `~/.openclaw/extensions/` | **不存在**（未装自定义 plugin） |
| stock source root | `/Users/peterqiu/.npm-global/lib/node_modules/openclaw/dist/extensions` |
| 主配置 | `~/.openclaw/openclaw.json`（`plugins list` 头部明确打印） |
| plugin 总数 / enabled | **73 / 53** |
| disabled 样本 | `a2a`（`stock:a2a/index.js`） |

### ⑥ 边界

- **不要手动往 `extensions/` 里拷目录来"安装"。** 那样文件在，但 `plugins.installs` 没记录，状态是不一致的。用 `install`。
- **不要手动编辑 `extensions/` 里的产物。** 那是构建产物；改它等于改了一个"下次 build 就会被覆盖"的临时现场。
- **不要用 `openclaw config set` 改 JSON5 主配置。** 会丢注释（见 11.2）。
- **`workspace/` 与 `extensions/` 的边界不要跨越**：你的 skill 放 workspace，别人的代码放 extensions。

### ⑦ 反例与失败模式

**反例一：在 workspace 下建 `plugins/` 目录。**
你以为在"正确的位置"，实际是在一个系统不看的地方。症状：插件永远不出现。

**反例二：把 `registry` 当成搜索。**
`registry` 管本机；`search` 才是搜 ClawHub。**两个词，一个管本地一个管远端。**

**反例三：把 `5x/7x` 的比例当健康度。**
`53/73` 不是"健康度 73%"。它是"73 个被发现的插件里，53 个处于启用状态"。

**反例四：把 stock plugin 当社区插件。**
`a2a` 是 stock 且 disabled。如果你以为"disabled 说明装错了"，你就会去"修"一个不需要修的东西。

### ⑧ 练习与验收

```bash
# 1) 三个路径的真身对照（一次看清）
echo "extensions:      $(ls -d ~/.openclaw/extensions 2>/dev/null || echo 不存在)"
echo "workspace/plugins: $(ls -d ~/.openclaw/workspace/plugins 2>/dev/null || echo 不存在)"
echo "openclaw.json:   $(ls -l ~/.openclaw/openclaw.json 2>/dev/null | awk '{print $5" bytes"}')"

# 2) 来源分布（stock vs 其他）
openclaw plugins list 2>&1 | grep -o 'stock:' | wc -l

# 3) 状态分布（enabled / disabled）
openclaw plugins list 2>&1 | grep -c 'enabled'
openclaw plugins list 2>&1 | grep -c 'disabled'

# 4) 配置分区定位
grep -n 'installs\|entries\|allow\|deny' ~/.openclaw/openclaw.json 2>/dev/null | head -10
```

**验收标准**：你能说出 `~/.openclaw/extensions/` 与 stock 目录的关系、以及两个 registry 各自的职责。

---

## 11.6 核心概念六 · 插件与 Skill 的分工

### ① 一句话定义

**Skill 是"一页剧本"（Markdown · 跨平台 · 按需装载 · 无执行权）；Plugin 是"整个剧组"（JSON5 清单 + 可执行代码 + 生命周期 + 分发通道 + 可携带 N 个 skill）——两者的分界线是"是否需要确定性执行与启动期介入"。**

### ② 现场直觉

一句最省事的分辨方法：

> **问自己：这件事"写一段话让模型照着做"够不够？**
>
> - 够了 → Skill
> - 不够（需要脚本、需要钩子、需要在启动时加载、需要占通道）→ Plugin

**再问一句更狠的：**

> **如果我把它 disable 了，会发生什么？**
>
> - 什么都不会发生（只是某个情境下少了点指导）→ 它本来该是 Skill
> - 系统某个功能会坏 → 它必须是 Plugin

### ③ 结构解剖

| 维度 | **Skill**（第 10 章） | **Plugin**（本章） |
|---|---|---|
| 范围 | 1 个 `SKILL.md` + 可选 `references/ scripts/ assets/` | 1 或 N 个 skill + `openclaw.plugin.json` + 原生 Control UI 资源 |
| 载体 | Markdown（自然语言指令） | TypeScript/JavaScript 进程 + JSON5 清单 |
| 加载方式 | **渐进式披露**（agent 按需读） | **启动时 / 事件驱动加载**（`activation`） |
| 跨平台 | **任何读 `SKILL.md` 的客户端** | **仅 OpenClaw runtime** |
| License | skill 自带 `license:` 字段 | 跟随 plugin（MIT 默认） |
| 治理 | frontmatter + 组织级管理（2026-02） | `allow / deny / entries / slots` + `--accept-capabilities` |
| 破坏性 | 极低（删目录即回滚） | 中（可能已注册工具名 / 已占通道 / 已写状态） |
| 典型用途 | 判断、流程、标准、经验 | 工具实现、通道接入、计分钩子、启动期装配 |

### ④ 为什么这样设计

**因为"知识"与"代码"的失效模式完全不同。**

知识失效的表现是"这次没用上"——不致命，下次还有机会。
代码失效的表现是"系统坏了一个功能"——致命，且常常影响面广。

把两者放在同一层管理，会导致两种坏结果之一：

- 用插件管知识 → 你对每一段话都付出了完整的工程成本（清单 / 构建 / 打包 / 确权），且失去了跨平台可移植性；
- 用 skill 管代码 → 你写了"应该执行的逻辑"，但没有任何机制保证它被执行。

**正确的分工是分层，而不是替代。** 而 OpenClaw 的 `skills` 字段让这两层可以被一个 plugin 一起携带：

```json5
{
  id: "silicon-life-training",
  skills: ["./skills"],                 // ← 携带 N 个 SKILL.md
  contracts: { tools: ["sl_drift_audit"] }, // ← 同时提供确定性工具
  activation: { onEvent: "first-message" }
}
```

**这就是"Plugin 是 Skill 的超集"的准确含义。**

### ⑤ 真名与实测

| 场景 | 该用哪个 | 本机对应真名 |
|---|---|---|
| 一段报价判断经验 | Skill | `~/.openclaw/workspace/skills/<id>/SKILL.md` |
| 一个漂移审计脚本 | `scripts/` 或 Plugin | `skills/<id>/scripts/` → 升级为 plugin |
| 一个必须每次执行的合规闸门 | Plugin（`contracts.tools` + capability 确权） | `openclaw.plugins` 生态 |
| 一个通道接入（如飞书） | Plugin（`channels` 字段） | 本机 stock 里有对应 channel plugin |
| 一个计分钩子（Merit Ledger） | Plugin（`activation.onEvent`） | 待 RFC（见 11.12.4 ⏳） |
| 每周体检的例行脚本 | `scripts/`（判断部分留在 SKILL.md） | 同上 |

**本机现状**：73 个 plugin（多为 stock），236 个 skill 目录。**两个数字属于两层，不能相加、不能比较。** 谁把它们合起来说"本机共 309 个能力单元"，谁就把口径弄错了。

### ⑥ 边界

- **一个 plugin 携带 100 个 skill 不是一个好设计。** 它会让"启用这个插件"的决策成本变得不可评估（你不知道你在批准什么）。
- **不要用 plugin 承载"可能需要有人改"的知识。** 代码的修改门槛远高于 Markdown。
- **不要用 skill 承载"必须确定"的逻辑。** 这是本章最硬的一条边界。

### ⑦ 反例与失败模式

**反例一：把 skill 目录当 plugin 装。**
`openclaw plugins install ./my-skill-dir` —— 没有 `openclaw.plugin.json`，装不上（或行为异常）。**正确做法**是在一个 plugin 工程里通过 `skills` 字段携带它。

**反例二：把 plugin 当 skill 读。**
把 `openclaw.plugin.json` 当"agent 会读的说明文件"——**模型不读它**，它只给 OpenClaw 运行时读。

**反例三：在 SKILL.md 里写"请启动一个后台进程"。**
skill 不会启动任何东西。这是第 10 章误区四的镜像。

**反例四：因为"想让它自动跑"就用 plugin。**
先问：它需要的是"自动跑"还是"在对的时候被想起来"？后者是 skill。

### ⑧ 练习与验收

```bash
# 1) 两层各自计数（务必分母不同）
echo "Skill 层（workspace）: $(($(find ~/.openclaw/workspace/skills -maxdepth 1 -type d | wc -l) - 1)) 个目录"
echo "Plugin 层（发现）:     $(openclaw plugins list 2>&1 | head -1)"

# 2) 看一个 stock plugin 是否携带 skill（skills 字段）
f=$(find "$(npm root -g)/openclaw/dist/extensions" -name 'openclaw.plugin.json' 2>/dev/null | head -1)
grep -n '"skills"' "$f" 2>/dev/null

# 3) 你自己的分类练习：把你手上 10 个能力逐个归类
cat <<'EOF'
能力名 | 需要确定性执行? | 需要启动期介入? | 结论
------|---------------|----------------|-----
      | 否            | 否             | Skill
      | 是            | 否             | scripts/ 或 Plugin
      | 任意          | 是             | Plugin
EOF
```

**验收标准**：你能对任意一个能力，在 10 秒内说出"它该是 Skill 还是 Plugin"，并给出理由（是否需要确定性执行 / 启动期介入）。

---

## 11.7 核心概念七 · ClawHub 分发

### ① 一句话定义

**ClawHub 是 OpenClaw 生态的中心化分发通道：它是一个独立 CLI（`clawhub`，不与 `openclaw` 同包），负责把打包好的 plugin 发布到公共索引，并让用户用 `openclaw plugins install clawhub:<pkg>` 装回来。**

### ② 现场直觉

前面几步（init / build / pack / validate / install / enable）全是在**你自己的机器上**闭环。

ClawHub 是唯一一个"出门"的环节。

"出门"意味着三件新事：

1. **不再只对你负责。** 你的包会被陌生人装到陌生环境上。
2. **不可回滚。** 发布出去的字节流是事实；你可以发新版本，不能收回旧版本。
3. **有准入约束。** 平台会设门槛（比如 GitHub 账号年龄），因为生态需要防滥用。

**这也是本章的一个基本纪律：先把本地闭环跑通，再出门。** 顺序反了，你在用一整条生态通道，押一次没验证过的赌。

### ③ 结构解剖：发布 5 步

```bash
# Step 1 · 安装 clawhub CLI（独立包，不在 openclaw 里）
npm i -g clawhub
# 或 pnpm add -g clawhub

# Step 2 · GitHub OAuth 登录（账号需 ≥ 1 周，反 PAM spam）
clawhub login
clawhub whoami

# Step 3 · 本地 dry-run 预览元数据（不实际上传）
clawhub package publish ./silicon-life-training --family code-plugin --dry-run

# Step 4 · 正式 publish（含版本号、签名、source attribution、upload plan）
clawhub package publish ./silicon-life-training --family code-plugin

# Step 5 · 用户侧安装（走 openclaw plugins install + clawhub: 前缀）
openclaw plugins install clawhub:silicon-life-training --accept-capabilities
openclaw plugins enable  silicon-life-training --accept-capabilities
openclaw plugins list --enabled | grep silicon-life-training
```

**关键约束表：**

| 约束 | 值 | 含义 |
|---|---|---|
| GitHub 账号年龄 | **≥ 1 周** | 反 PAM / 反滥用门槛 |
| Family 标签 | `code-plugin` / `skill` / 其他 | 决定这个包在索引里的分类与安装路径 |
| Trusted publishing | `clawhub_token`（CI 长期）+ OIDC（无 token） | 两条 CI 集成路径 |
| Private 仓库 | 需 ClawHub GitHub App 授权 | （未来功能） |
| `--environment <name>` | GitHub Actions environment claim 匹配 | 强化 CI 归因 |
| 撤回机制 | 违规 publish 可被下架；scan-held 仍可在 dashboard 看到 | 发布不等于永久 |

### ④ 为什么这样设计

**设计一：ClawHub 独立成 CLI，而不是 `openclaw` 的子命令。**

这个选择的含义很深：**发布行为与运行行为在命名空间上被分开了。**

一个只在本地跑 agent 的用户，不需要安装任何发布工具。一个要发布包的人，显式地装一个带发布权限的东西。**权限面按需展开**——这与 install/enable 分离是同一条设计哲学的延伸。

**设计二：dry-run 是一等公民。**

`--dry-run` 让你看到元数据、版本号、source attribution 与 upload plan，而**不产生任何外部副作用**。这与 `plugins uninstall --dry-run`、`plugins update --dry-run` 一致：**这个工具链系统性地为破坏性操作提供了"预演"位。**

**设计三：账号年龄门槛。**

一个开放分发通道最大的敌人不是恶意代码（那可以检测），而是**批量注册的垃圾包**。门槛把"成本"从"写几行代码"提到"你需要一个至少一周的 GitHub 账号"，这过滤掉了大部分自动化滥用。

**设计四：CI 优先（GitHub Actions 复用工作流）。**

```yaml
# .github/workflows/silicon-life-publish.yml
name: Publish Silicon Life Training plugin
on:
  push:
    tags: ['v*']
jobs:
  publish:
    uses: openclaw/clawhub/.github/workflows/skill-publish.yml@main
    with:
      owner: bluesilicon
      dry_run: false
    secrets:
      clawhub_token: ${{ secrets.CLAWHUB_TOKEN }}
```

**发布应该是 CI 的事，不是人手的事。** 因为发布不可回滚，所以它必须可审计（谁、什么时候、什么版本、什么 diff）。

### ⑤ 真名与实测

| 项 | 真名 | 状态 |
|---|---|---|
| 发布 CLI | `clawhub`（独立包） | ✅ 文档确认；⏳ 本机未安装 |
| 登录 | `clawhub login` / `clawhub whoami` | ✅ 文档确认 |
| 发布命令 | `clawhub package publish <src> --family code-plugin` | ⏳ **本机未执行**（受账号年龄等约束） |
| 用户侧安装 | `openclaw plugins install clawhub:<pkg>` | ✅ 与 `install` 的 6 种源一致 |
| 搜索 | `openclaw plugins search <query> --limit <n> --json` | ✅ 命令真名 |
| 市场检视 | `openclaw plugins marketplace entries / list / refresh` | ✅ 命令真名 |

> ⏳ **诚实声明**：`clawhub package publish` **本机未实测**（受反 PAM 约束）。本章给出的是一条"路径正确但未经本机验证"的流程；接力者按 `validate → install → enable → doctor → 触发一次 → 才 publish` 的顺序补测。

**另需注意一处勘误**：不要写"ClawHub 是 OpenClaw 的内置 registry"。**OpenClaw 主仓不内置上传逻辑**；本机 `plugins registry` 仅服务本机持久化注册表（`--refresh` 重建）。

### ⑥ 边界

- **不要在没跑通本地闭环前 publish。** 因为发布不可回滚，而本地闭环是可重复的。
- **不要把 `clawhub` 当成 `openclaw` 的子命令。** 两个包，两个命名空间。
- **不要跳过 `--dry-run`。** 它是你唯一能在"副作用为零"的状态下检查元数据的机会。
- **不要用同一版本号重发。** 版本号是一次性事实；修完发 patch 版本。

### ⑦ 反例与失败模式

**反例一：顺序反了（先 publish，再本地装）。**
后果：你发布了一个自己都没装过的东西。**修补方式**：先补本地闭环，再发 patch 版本，不要重发同号。

**反例二：在正式包里带上了测试凭证。**
检查你的 `references/` 与 `scripts/` 里有没有 token、内网地址、客户名单。**发布 = 永久。**

**反例三：把 family 猜错。**
`--family code-plugin` 与 `--family skill` 走的是不同的分发路径与安装预期。**先 dry-run 确认。**

**反例四：以为"下架"等于"没人有"。**
已经 clone / install 过的副本不会消失。**发布前假设它是不可撤销的。**

### ⑧ 练习与验收

```bash
# 1) 本地闭环先跑通（这是 publish 的前置条件）
openclaw plugins validate --root . --entry ./dist/index.js 2>&1 | tail -5
openclaw plugins pack --root . --out ./dist-pkg.tgz 2>&1 | tail -5
openclaw plugins install ./dist-pkg.tgz --accept-capabilities 2>&1 | tail -5
openclaw plugins enable <id> --accept-capabilities 2>&1 | tail -5
openclaw plugins doctor 2>&1 | tail -10

# 2) 搜索侧（安全，只读）
openclaw plugins search silicon --limit 5 2>&1 | head -10
openclaw plugins marketplace entries 2>&1 | head -10

# 3) 发布侧（⏳ 本机未执行；确认环境后再做）
# npm i -g clawhub && clawhub login
# clawhub package publish ./silicon-life-training --family code-plugin --dry-run
```

**验收标准**：你能列出 publish 之前必须完成的 6 个本地验证动作，并说明"为什么顺序不能反"。

---

## 11.8 核心概念八 · 训练学如何装进 OpenClaw

### ① 一句话定义

**把训练学装进 OpenClaw 的意思是：把前面十章的方法论，按"契约文件 / SKILL.md / 脚本 / Plugin 能力声明"四种形态重新分配，然后通过一个 plugin 把它们作为可安装、可版本化、可确权的分发单元交付出去。**

### ② 现场直觉

这是一个"把书变成产品"的动作。

书（方法论）的价值在"讲清楚"；产品的价值在"用得上"。两者的差别不是文笔，是**形态分配**——同一个方法论里，有的部分是硬约束（必须永远生效），有的部分是判断（需要对时提醒），有的是例行工作（必须确定执行）。

**把它们放错地方，方法论就会以"看起来在用、实际没生效"的方式失败。**

### ③ 结构解剖：五种差异化优势的落点

| 优势 | 训练学出处 | 在 plugin 里的落点 | 形态 |
|---|---|---|---|
| **⚡ 优势 1 · A2A 反脆弱 + 让位协议**（Response Yield Protocol，原：让位协议） | 第 6 章 / 第 9 章 | plugin 携带 `response-yield.ts` hook，挂 `activation.onEvent: "first-response"`；清单加 `contracts.hooks: ["response-yield"]` | **⏳ 待 RFC** |
| **⚡ 优势 2 · 漂移治理 · 每周体检**（Drift Governance） | 第 4 章 | `activation.onStartup: true` 启动时跑 `weekly-health-check.ts`，把 Trust Score / Merit Ledger / Drift Index 写入 `~/.openclaw/plugin-state/<id>/health.json` | ✅ 可立即做 |
| **⚡ 优势 3 · 主动性边界三档**（Autonomy Boundary Triad） | 第 4 章 | 清单加 `policy.proactiveness: "respond-only" \| "propose-with-approval" \| "autonomous-goal-generation"` | **⏳ 待 RFC** |
| **⚡ 优势 4 · 三省制 + 信任分 + 功绩账本** | 第 5 章 | hook `before-tool-call` / `after-tool-call` 自动累加 Merit Ledger，落 `~/.openclaw/merit/<id>.jsonl` | ✅ 可立即做 |
| **⚡ 优势 5 · OODA 自主目标生成** | 第 7 章 | plugin 加 `ooda.observe / orient / decide / act` 四个 hook，对应四个 entrypoint | **⏳ 待 RFC** |

**形态分配表（更通用的一版）：**

| 训练学组件 | 最佳形态 | 理由 |
|---|---|---|
| 七大契约（SOUL / USER / AGENTS / TOOLS / IDENTITY / HEARTBEAT / MEMORY） | **契约文件**（always-on） | 必须永远在场，不能被"按需" |
| 双三角模型 / 教练机制（Mentor Agent，原：教练虾） | **SKILL.md** | 情境化判断 |
| 漂移治理 / 每周体检 | **SKILL.md + scripts/** | 判断在文本，例行任务在脚本 |
| 三省评审制 / Trust Score | **SKILL.md + Plugin hook** | 流程在文本，计分在代码 |
| 报价闸门 / 合规红线 | **Plugin（强制）** | 不能接受"偶尔不生效" |
| OODA 自主目标生成 | **SKILL.md + Plugin** | 触发在文本，执行在代码 |

### ④ 为什么这样设计

**因为"必须生效"和"对时提醒"是两种不同的工程保证。**

- **契约文件**：保证是"每一轮都在"。代价是占用上下文预算，且改动成本高。
- **SKILL.md**：保证是"对的情境下会被装载"。代价是**不保证一定被装载**。
- **Plugin**：保证是"启用了就一定在运行期"。代价是工程成本 + 需要用户确权。

**把"红线"放在 SKILL.md 里是本章最严重的架构错误**——因为 skill 的保证是概率性的，而红线的语义是必然性的。

### ⑤ 真名与实测

```bash
# 落地一个训练学 plugin 的最小路径（真名）
openclaw plugins init silicon-life-training --type feature --name "硅基生命训练学" --directory ./silicon-life
cd silicon-life
openclaw plugins build  --root .
openclaw plugins pack   --root . --out ./silicon-life-training.tgz
openclaw plugins validate --root . --entry ./dist/index.js
openclaw plugins install ./silicon-life-training.tgz --accept-capabilities
openclaw plugins enable  silicon-life-training --accept-capabilities
openclaw plugins doctor
```

**本机现状与差距（诚实）**：

| 项 | 现状 |
|---|---|
| 训练学 plugin 是否已存在 | **不存在**（`~/.openclaw/extensions/` 本机不存在） |
| 训练学 skill 化 | ⏳ 可行性结论：8 卷中 7 卷可 Skill 化，**预计** 28 个 `SKILL.md`（未生成） |
| 契约文件 | 存在于各 agent workspace（`agents/<agent>/contracts/`） |
| plugin hook 字段（`contracts.hooks` / `policy.proactiveness` / `ooda.*`） | **⏳ 待 RFC**（本书提出的扩展，非 OpenClaw 现行字段） |

> ⚠ **这是本章最需要克制的一处**：`contracts.hooks` / `policy.proactiveness` / `ooda.*` 是**本书的 RFC 提案**，不是 OpenClaw 既有字段。**不得写成"OpenClaw 支持这些字段"。** 现行可用的字段只有 11.2 表中列出的那 16 个。

### ⑥ 边界

- **不要把一个方法论塞进一个插件。** 一个 plugin 一大包 → 用户无法评估"我在批准什么"。正确做法：按能力边界拆成若干 plugin（或一个 plugin + 若干 skill）。
- **不要用 plugin 承载需要频繁修改的文本。** 改代码的成本远高于改 Markdown。
- **不要在没确认字段真实性的情况下写清单。** 未知字段在不同解析强度下行为不一致——**先 build + validate，再 install**。

### ⑦ 反例与失败模式

**反例一：把红线写进 SKILL.md。**
后果：它会被装载——偶尔。**一条"偶尔生效"的红线等于没有红线。**

**反例二：把所有内容都塞进一个 plugin。**
后果：用户面对一个"批准还是拒绝"的选择，但他无法理解自己在批准什么。**capability 确权的意义被这个设计抹掉了。**

**反例三：把训练学写成一份 3000 字 README 放进 plugin。**
plugin 的入口是清单，不是 README。**模型不读你的 README。**

**反例四：把 RFC 提案当既有能力。**
写"本 plugin 使用 `policy.proactiveness` 字段实现三档制"——读者会去文档里找，然后找不到。**必须标 ⏳ 并写清这是本书提案。**

### ⑧ 练习与验收

```bash
# 1) 把你手上的训练学资产按四形态分类
cat <<'EOF'
资产 | 必须永远生效? | 需要确定执行? | 形态
----|--------------|--------------|-----
    | 是           | 任意         | 契约文件
    | 否           | 否           | SKILL.md
    | 否           | 是           | scripts/ 或 Plugin
    | 否           | 是(强制红线) | Plugin + capability 确权
EOF

# 2) 检查你的 agent 契约文件是否存在（形态一）
ls ~/.openclaw/workspace/agents/*/contracts/ 2>/dev/null | head -10

# 3) 确认 plugin 侧能力字段（只读）
openclaw plugins inspect <some-stock-id> --all 2>&1 | head -30
```

**验收标准**：你能给出一个"训练学 plugin 的最小可行切分"（几个 plugin、各携带什么、哪些进契约文件），并解释每一块的形态选择理由。

---

## 11.9 核心概念九 · 生命周期七阶段与 capability 确权

### ① 一句话定义

**一个 OpenClaw plugin 的一生是七阶段可观测生命周期（概念 → 脚手架 → 构建 → 打包 → 安装 → 运行时 → 治理），每一阶段都有"CLI 命令 + 清单字段 + 持久化位置"三重落地；而 capability 确权贯穿在 install / enable / update 三处。**

### ② 现场直觉

生命周期不是"流程图好看"，它是**故障定位的地图**。

模块加载报错 → 阶段 2（构建产物不对）
找不到插件 → 阶段 4（安装没成功）
装了但不生效 → 阶段 5（忘 enable）
能跑但行为怪 → 阶段 6（runtime 加载 / 配置不匹配）
升级后出问题 → 阶段 7（capability 扩大 / 版本漂移）

**知道自己在第几阶段，是 90% 的运维效率。**

### ③ 结构解剖

```text
┌─────────────┐  init    ┌─────────────┐  build   ┌─────────────┐
│  0. 概念    │ ───────► │  1. 脚手架  │ ───────► │  2. 构建    │
│  RFC + 设计 │          │ plugins init│          │ 生成产物     │
└─────────────┘          └─────────────┘          └─────────────┘
                                                          │
                                                          ▼
┌─────────────┐  inspect ┌─────────────┐  install ┌─────────────┐
│  6. 治理    │ ◄─────── │  5. 运行时   │ ◄─────── │  4. 安装    │
│ doctor /    │          │ 已加载、参与 │          │  6 种源     │
│ enable /    │          │ 调度         │          │             │
│ disable /   │          │              │          │             │
│ uninstall   │          │              │          │             │
└─────────────┘          └─────────────┘          └─────────────┘
       ▲                       ▲                        ▲
       └──────────── pack / validate（阶段 3）──────────┘
```

**阶段 ↔ 字段 ↔ 命令 ↔ 持久化位置：**

| 阶段 | 关键 JSON5 字段 | 关键 CLI | 持久化位置 |
|---|---|---|---|
| 0 概念 | （无） | （手写设计/RFC） | 仓库内设计文档 |
| 1 脚手架 | `id / name / description / categories / contracts / activation` | `plugins init` | `~/.openclaw/extensions/<id>/openclaw.plugin.json` |
| 2 构建 | （生成）`openclaw.install` 包元数据 + UI assets | `plugins build`（`--check`） | 同上（覆盖写入） |
| 3 打包 | （生成）`SHA256 + activation request` | `plugins pack --out` | `./<id>.tgz` |
| 4 安装 | `openclaw.json#plugins.installs.<id>` | `plugins install` | `~/.openclaw/extensions/<id>/` |
| 5 运行时 | `activation.onStartup / onEvent` | **`plugins enable`（必须）** | `openclaw.json#plugins.entries.<id>.enabled = true` |
| 6 治理 | `plugins.allow / deny / slots.<id>` | `doctor / list / inspect / uninstall / update / registry` | 同上 |

**capability 确权的三个位置：**

```text
install  --accept-capabilities   ← 接受「当前」声明的能力
enable   --accept-capabilities   ← 确认进入运行期
update   --accept-capabilities   ← 接受「升级后可能新增」的能力（防权力悄悄扩张）
```

### ④ 为什么这样设计

**设计一：把"install"和"enable"分开。**（见 11.4）
文件落地与运行期介入，风险等级不同，必须分别确权。

**设计二：`build` 有产物、`pack` 有校验和、`validate` 有 CI 入口。**
三者合起来形成"源 → 产物 → 可交付 artifact"的可验证链。而 `build --check` 让"产物过期"从隐性故障变成显性检查项。

**设计三：治理阶段提供 `allow / deny / slots`。**
enable/disable 是逐个开关；allow/deny 是**策略表达**。做"白名单制部署"必须用后者。

**设计四：`registry --refresh` 承认缓存会漂移。**
本机持久化注册表可能落后于磁盘真实状态（你手动删了目录、或换了主包版本）。**提供一个重建入口，是承认"缓存与现实会不一致"这个事实。**

### ⑤ 真名与实测

| 阶段 | 命令 | 本机实测 |
|---|---|---|
| 1 脚手架 | `openclaw plugins init` | ✅ 命令存在（`--help` 可见） |
| 2 构建 | `openclaw plugins build --check` | ✅ 存在（"Fail if generated metadata is out of date"） |
| 3 打包 | `openclaw plugins pack --out` | ✅ 存在 |
| 4 安装 | `openclaw plugins install` | ✅ 存在（6 种源） |
| 5 运行时 | `openclaw plugins enable` | ✅ 存在；**⏳ 本机未跑通完整 5 阶段生命周期** |
| 6 治理 | `openclaw plugins doctor / list / inspect / update / registry` | ✅ `list` / `doctor` 可用；本机基线 **53/73 enabled** |
| 版本 | `openclaw --version` | ✅ `2026.9.6 (eb377ac)` live / `2026.9.4 (3a9d69d)` 书内口径 |

> ⏳ **诚实边界**：七阶段的**命令拼写**全部由 `plugins --help` 确认为真名，但**本机未跑通完整生命周期**（未装自定义 plugin、未执行 pack/publish）。本章的七阶段模型是**结构与命名的实测 + 流程的可执行设计**，二者不要混为一谈。

### ⑥ 边界

- **不要跳过阶段 2（build）直接进入阶段 3（pack）。** 你打包的是产物，不是源码。
- **不要在阶段 6 才第一次跑 doctor。** doctor 的价值在"正常时建立基线"。
- **不要把 `registry --refresh` 当常规操作。** 它是修复手段，不是日常动作。
- **不要指望 `uninstall` 清空一切。** 它可能保留状态目录（如 `plugin-state/`），需要手工清理——**先 `--dry-run` 看它要删什么。**

### ⑦ 反例与失败模式

**反例一：跳过 enable（全章 P0）。**
装了 20 个插件，`list --enabled` 只有 5 个。**行为面的失败往往看起来像"功能不存在"。**

**反例二：升级不确权。**
`update --all` 时无脑加 `--accept-capabilities`。后果：某个插件的 capability 范围悄悄扩大，而你以为只是"打了个补丁"。

**反例三：产物过期。**
源改了、没重建、装的是旧产物 → 行为与你阅读的源码不符。**`build --check` 就是抓这个的。**

**反例四：把 `doctor` 报的 compatibility 警告当噪音。**
它是**版本漂移的第一信号**。

### ⑧ 练习与验收

```bash
# 1) 七阶段只读巡览（安全）
openclaw plugins --help 2>&1 | sed -n '/^Commands:/,/^$/p'
openclaw plugins doctor 2>&1 | tail -20

# 2) 阶段诊断练习：给定症状，说出阶段
cat <<'EOF'
症状                                  → 阶段
找不到刚装的插件                      → 4（安装）或 1（id 不一致）
装了但不生效                          → 5（忘 enable）
启动变慢                              → 5（activation.onStartup 滥用）
配置填了但没效果                      → 2/5（configSchema 未声明该键）
升级后行为变了                        → 7（capability 扩张 / 版本漂移）
模块加载失败                          → 2（构建产物缺失/过期）
EOF

# 3) 生命周期自查（每次改动后跑）
{
  echo "== $(date '+%F %T') =="
  openclaw plugins list 2>&1 | head -2
  openclaw plugins doctor 2>&1 | tail -5
} | tee -a ~/plugin-lifecycle-log.txt
```

**验收标准**：你能拿到一个"插件不工作"的描述，在 60 秒内说出该跑哪两个命令、以及可能的阶段编号。

---

## 11.10 怎么做：从 init 到 doctor 的七步落地路径

这一节只回答一个问题：**今天开始，按什么顺序动手。**

路径分七步。**第 0 步是备份，不是可选步骤。**

### 11.10.1 第 0 步 · 先备份（3 秒）

```bash
openclaw backup create
```

**为什么它排在第 0 步而不是最后一步**：本章后面所有"看起来只读"的操作里，都藏着一个会写配置的动作（`enable` 改 `entries`、`install` 写 `installs`、`update` 动版本）。**备份不是仪式，它是"你可以试错"的前提。**

### 11.10.2 第 1 步 · 摸基线（约 10 分钟）

```bash
# 版本（两个口径都要记）
openclaw --version 2>&1 | tail -1
# 本机 live：OpenClaw 2026.9.6 (eb377ac)
# 书内统一口径：OpenClaw 2026.9.4 (3a9d69d)

# plugin 现状（本机 53/73）
openclaw plugins list 2>&1 | head -4

# 三件事的基线
echo "--- 安装目录 ---"; ls -d ~/.openclaw/extensions 2>&1
echo "--- 主配置 ---";   ls -l ~/.openclaw/openclaw.json 2>/dev/null | awk '{print $5" bytes"}'
echo "--- 诊断 ---";     openclaw plugins doctor 2>&1 | tail -20

# 落盘成基线文件（带时间戳 = TEV 证据三件套之一）
{
  date '+%Y-%m-%d %H:%M:%S'
  openclaw --version 2>&1 | tail -1
  openclaw plugins list 2>&1 | head -2
} | tee ~/plugin-baseline-$(date +%Y%m%d).txt
```

**产出一句话**：本机有 ___ 个 plugin，___ 个 enabled，安装目录___，主配置 ___ 字节。

### 11.10.3 第 2 步 · 只读侦察（约 15 分钟）

**先把"看"和"改"彻底分开。** 这一步不改任何东西。

```bash
# 1) 全量列表（含来源）
openclaw plugins list --verbose 2>&1 | head -40

# 2) 只看启用的
openclaw plugins list --enabled 2>&1 | head -20

# 3) 单插件深挖（挑一个你关心的）
openclaw plugins inspect <id> --all 2>&1 | head -60
#   --runtime 会真正加载 runtime 去检 hooks/tools/diagnostics（属于"轻量执行"）

# 4) 全量诊断
openclaw plugins doctor 2>&1 | tail -30
```

**产出**：一张你的 plugin 地图——来源（stock / 其他）、状态（enabled / disabled）、以及"我最关心的 3 个插件分别是什么"。

### 11.10.4 第 3 步 · 建你自己的第一个 plugin 工程（约 30 分钟）

```bash
# 1) 脚手架（真名：plugins init）
openclaw plugins init silicon-life-training \
  --type feature \
  --name "硅基生命训练学" \
  --directory ./silicon-life
# --type 三选一：tool / provider / feature

cd silicon-life

# 2) 看它生成了什么
ls -la
cat openclaw.plugin.json

# 3) 构建（生成 metadata + Control UI assets）
openclaw plugins build --root .

# 4) 检查产物是否过期（CI 用）
openclaw plugins build --root . --check

# 5) 校验
openclaw plugins validate --root . --entry ./dist/index.js
```

**如果 `--entry` 路径不确定**：先 `find . -name 'index.js' -o -name 'index.ts'`，再 `validate`。**校验失败比安装失败便宜得多。**

### 11.10.5 第 4 步 · 手改清单，把训练学的能力声明写进去（约 40 分钟）

打开 `openclaw.plugin.json`，按这个顺序确认四件事：

**① 身份四项**

```json5
{
  id: "silicon-life-training",     // 小写 + 连字符，不含 /
  name: "硅基生命训练学",
  description: "把训练学的契约、教练机制与漂移治理装进 OpenClaw。",
  categories: ["other"],           // bundled plugin 必须恰好一个 active category
```

**② 能力声明（最关键的一步：你要动用户什么）**

```json5
  contracts: {
    tools: ["silicon_life_drift_audit"]   // 你会注册的 tool 名（用户会看到）
  },
  channels: [],                            // 你占用哪些通道（没有就留空）
  skills: ["./skills"],                    // 你携带哪些 SKILL.md（第 10 章衔接）
```

**③ 激活方式（默认别拖慢启动）**

```json5
  activation: {
    onStartup: false,                      // ← 默认 false
    onEvent: "first-message"               // 事件驱动，按需激活
  },
```

**④ 配置模式（硬格式）**

```json5
  configSchema: {
    type: "object",
    additionalProperties: false,           // ← 硬要求，缺了等于校验失效
    properties: {
      agentName:     { type: "string" },
      auditInterval: { type: "string" }
    },
    required: ["agentName"]
  },
  uiHints: {
    agentName:     { label: "目标 Agent", placeholder: "比如 tiance" },
    auditInterval: { label: "审计节律", advanced: true }
  }
```

**改完再跑一轮 build + validate**：

```bash
openclaw plugins build    --root .
openclaw plugins validate --root . --entry ./dist/index.js --json
```

### 11.10.6 第 5 步 · 打包 → 安装 → 启用 → 验证（约 20 分钟）

**顺序固定，不要跳步。**

```bash
# 1) 打包（产物含 SHA256 + activation request）
openclaw plugins pack --root . --out ./silicon-life-training.tgz
shasum -a 256 ./silicon-life-training.tgz        # 记下这个值

# 2) 安装（第 1 次确权）
openclaw plugins install ./silicon-life-training.tgz --accept-capabilities

# 3) 启用（第 2 次确权 —— 关键一步，忘了它就前功尽弃）
openclaw plugins enable silicon-life-training --accept-capabilities

# 4) 三件事验证
openclaw plugins list --enabled | grep silicon-life-training
openclaw plugins inspect silicon-life-training --all 2>&1 | head -30
openclaw plugins doctor 2>&1 | tail -20

# 5) 真触发一次（TEV：命令 + 输出 + 时间戳）
date '+%F %T' | tee ~/silicon-life-trigger.stamp
# 然后在一次真实对话里调用它注册的 tool，观察是否按预期工作
```

**如果第 2 步失败**：八成是打包产物结构不对（缺 `dist/`、缺清单）。回到第 1 步 `build`。

**如果第 3 步之后仍不生效**：跑 `openclaw plugins doctor`，它会把问题归类到"发现 / 模块加载 / 兼容性 / 配置"四类之一。

### 11.10.7 第 6 步 · 治理位与安全网（约 15 分钟）

```bash
# 1) 了解治理位（不改，先看）
grep -n 'allow\|deny\|slots' ~/.openclaw/openclaw.json 2>/dev/null | head -10

# 2) 演练卸载（--dry-run 不真的删）
openclaw plugins uninstall silicon-life-training --dry-run 2>&1 | tail -10

# 3) 演练更新
openclaw plugins update --all --dry-run 2>&1 | head -20

# 4) 建一个"改动即记录"的日志习惯
{
  echo "== $(date '+%F %T') =="
  echo "action: <你做了什么>"
  openclaw plugins list 2>&1 | head -2
} | tee -a ~/plugin-change-log.txt
```

**为什么在"没出事"的时候演练卸载**：因为卸载是有状态的破坏性操作。你要在**心态平稳、备份在手**的时候摸清它会删什么。

### 11.10.8 第 7 步 · 分发准备（可选，约 60 分钟）

只有当前六步全部跑通、且有真实使用证据之后，才进入这一步。

```bash
# 1) 分发前静态合规（三个反例检测）
find . -name 'manifest.yaml' | wc -l                       # 期望 0
grep -rn 'token\|secret\|password' ./references ./scripts 2>/dev/null | head
grep -n 'additionalProperties' openclaw.plugin.json        # 期望命中（硬要求）

# 2) 版本与底座对齐
grep -n '"version"' openclaw.plugin.json

# 3) 打包 + 记校验和
openclaw plugins pack --root . --out ./dist-pkg.tgz

# 4) 只有到这里才谈发布（⏳ 本机未实测）
# npm i -g clawhub
# clawhub login
# clawhub package publish . --family code-plugin --dry-run
# clawhub package publish . --family code-plugin
```

**分发前 checklist（六条全绿才能出门）**：

```text
[ ] validate 通过（结构）
[ ] install 成功（本地）
[ ] enable 成功 + list --enabled 可见
[ ] doctor 无 error
[ ] 真触发一次（有时间戳证据）
[ ] 无凭证泄漏 / 无绝对路径 / 无 manifest.yaml
```

### 11.10.9 一条时间线：一天能做到什么

| 时段 | 动作 | 产出 |
|---|---|---|
| 0:00–0:10 | 第 0、1 步 | 备份 + 基线文件 |
| 0:10–0:25 | 第 2 步 | plugin 地图 |
| 0:25–0:55 | 第 3 步 | 跑通 init/build/validate 的工程 |
| 0:55–1:35 | 第 4 步 | 一份能力声明正确的清单 |
| 1:35–1:55 | 第 5 步 | **装上了、启用了、触发过一次** |
| 1:55–2:10 | 第 6 步 | 治理位了解 + 卸载演练 |
| 2:10+ | 第 7 步（可选） | 分发准备 |

**一天之后的期望状态**：你有一个能装、能启、能诊、能卸的训练学 plugin 骨架；它的清单里写清了它会动你什么；你手上有完整的 TEV 证据。

**不期望的状态**：它已经好用了。第一天只是把它**装配起来**——真正的内容（skill、hook、工具实现）是接下来几周的事。

> **一条纪律**：本章反复出现的那句话，值得在这里再写一次——**先把本地闭环跑通，再谈分发。** 因为本地闭环可重复，分发不可回滚。

---

## 11.11 常见误区：九个错误，和它们为什么特别容易犯

每个误区按四段写：**症状 → 为什么会犯 → 后果 → 30 秒自查**。

九个误区的共同根因：**把"文件放进了机器"当成"能力进入了运行期"。**

---

### 11.11.1 误区一 · 写 `manifest.yaml`

**症状**：

```yaml
# manifest.yaml          ❌ 文件名错 + 格式错
id: my-plugin
entry: ./dist/index.js
```

**为什么会犯**：`manifest.yaml` 是**几乎整个云原生/容器生态的默认约定**（Kubernetes、Docker Compose、GitHub Actions、Ansible…）。人在这个行业待久了，"清单文件 = manifest.yaml"几乎是肌肉记忆。

**后果**：**静默失败**。系统找不到清单，但不会提示你"我要找的是 openclaw.plugin.json"。

**正确对照**：

| 业界默认 | OpenClaw 真名 |
|---|---|
| `manifest.yaml`（YAML） | **`openclaw.plugin.json`（JSON5）** |
| `entry` / `main` | `activation.onStartup` / `activation.onEvent` |
| `requires` | `configSchema.required[]` |
| `displayName` | `name` + `uiHints.<key>.label` |

**30 秒自查**：

```bash
find . -name 'manifest.yaml' | wc -l        # 期望 0
ls openclaw.plugin.json                     # 期望存在
grep -c 'additionalProperties' openclaw.plugin.json   # 期望 ≥ 1
```

---

### 11.11.2 误区二 · 敲 `openclaw plugin`（单数）

**症状**：`openclaw plugin install xxx` → `command not found` → 结论"OpenClaw 不支持插件"。

**为什么会犯**：`openclaw` 的其他命令族里，很多是"名词单数"（`openclaw agent`、`openclaw backup`、`openclaw plugins` 是例外）。而 `plugin` 在英文里作定语时也常常是单数（`plugin install` 读起来很顺）。

**后果**：你会**低估这个平台**，并因此选错技术路线（"它连插件都不支持，那我只能自己写脚本"）。

**事实**：真名是**复数** `openclaw plugins`，共 **15 个子命令**，`install` 支持 **6 种源**（path / archive / npm spec / git repo / `clawhub:package` / marketplace entry）。

**30 秒自查**：

```bash
openclaw plugins --help 2>&1 | grep -cE '^  [a-z]'    # 期望 ≥ 15
openclaw plugin 2>&1 | head -2                        # 期望报错（证明真名是复数）
```

---

### 11.11.3 误区三 · `install` 之后就以为能用（忘了 `enable`）

**症状**：装上、`list` 里能看到、但功能从没生效过。

**为什么会犯**：这是本章 P0 误区，根因是**人类语言里"安装"默认包含"可用"**。就像装 App：装完就能开。但插件不是 App——它是**运行期介入物**，而运行期介入需要单独确权。

**后果**：最典型的表现是"我明明配好了"与"它从来没生效"长期共存。而且**没有报错**，所以能潜伏很久。

**正确两步**：

```bash
openclaw plugins install <spec> --accept-capabilities   # ① 文件落地 + 记 installs
openclaw plugins enable  <id>   --accept-capabilities   # ② 置 entries.<id>.enabled = true
openclaw plugins list --enabled | grep <id>             # ③ 验证
```

**30 秒自查**：

```bash
openclaw plugins list 2>&1 | head -1              # 发现总数
openclaw plugins list --enabled 2>&1 | head -1    # 启用总数
# 两者差值 = 未启用数；如果你刚装的插件在差集里 → 忘 enable 了
```

---

### 11.11.4 误区四 · 去 `~/.openclaw/workspace/plugins/` 找安装目录

**症状**：`ls ~/.openclaw/workspace/plugins/` → `No such file or directory`。

**为什么会犯**：`~/.openclaw/workspace/` 下确实有 `skills/`、`agents/`、`references/` 等一堆目录。顺着这个规律推断，`plugins/` 也应该在那里——**而且这个推断非常合理**。

**后果**：你在错误的位置寻找、在错误的位置创建目录、手动拷贝文件，得到"文件在但系统看不到"的状态。

**真名对照**：

| 推断 | 真名 |
|---|---|
| `~/.openclaw/workspace/plugins/` | **不存在** |
| — | `~/.openclaw/extensions/`（安装目录） |
| `~/.openclaw/config.yaml` | `~/.openclaw/openclaw.json` |

**30 秒自查**：

```bash
ls -d ~/.openclaw/extensions 2>&1
ls -d ~/.openclaw/workspace/plugins 2>&1      # 这个"报错"才是正确的
```

---

### 11.11.5 误区五 · 改 `config.yaml` / 用 `openclaw config set` 改 JSON5（丢注释）

**症状**：你的 JSON5 主配置里本来写着一堆 `// 这行为什么这么配` 的注释，跑完一条命令之后注释全没了。

**为什么会犯**：JSON5 允许注释是一个**看起来免费的好处**。但"允许注释"的是**读**；**写**的时候，一个把 JSON5 规范化成标准 JSON 的写入器，会按 JSON 的规则输出——而 JSON 没有注释语法。

**后果**：你失去了所有"为什么这么配"的记录。三周后你看着这堆配置，不知道哪些是刻意的、哪些是历史残留。

**正确做法**：

```bash
# 1) 改前备份（强制）
openclaw backup create

# 2) 手编，保住注释（JSON5 支持 // 与 /* */）
#    ~/.openclaw/openclaw.json
#    plugins: {
#      entries: {
#        "silicon-life-training": {
#          enabled: true,          // ← 注释保留
#        },
#      },
#    }

# 3) 定点改（不重写全文），改完校验
python3 -c "import json5,sys;json5.load(open('/Users/<you>/.openclaw/openclaw.json'));print('OK')" 2>/dev/null \
  || node -e "require('json5');console.log('OK')"

# 4) 重启 / 体检
openclaw plugins doctor
```

**30 秒自查**：你的主配置里还有注释吗？如果一条都没有，说明某次写入已经把它们清掉了。

---

### 11.11.6 误区六 · 直接 `install` 未 build / pack / validate 的源工程

**症状**：改了源码直接装，装完行为和你读的代码对不上。

**为什么会犯**：开发时最容易犯——你正开着编辑器，手指就按出了 `install`。而"运行时不读源码"这件事在文件系统层面没有任何提示。

**后果**：你装的是**上一次的产物**。更糟的是 `openclaw plugins install <path>` 在 path 源下**看起来成功了**——因为它确实复制了文件。

**正确的本地闭环四步（顺序固定）**：

```bash
openclaw plugins build    --root .                                   # 1 生成产物
openclaw plugins validate --root . --entry ./dist/index.js           # 2 结构校验
openclaw plugins pack     --root . --out ./dist-pkg.tgz              # 3 打成 artifact
openclaw plugins install  ./dist-pkg.tgz --accept-capabilities       # 4 安装
```

**30 秒自查**：

```bash
# 源文件与产物哪个更新？产物更旧 → 你装的是旧货
find . -name '*.ts' -newer ./dist/index.js 2>/dev/null | head
ls -l ./dist/index.js
```

---

### 11.11.7 误区七 · 把 Plugin 当 Skill（范围混淆 + 越权字段）

**症状**：把纯 skill 目录直接 `install` 当 plugin；或者在 `SKILL.md` 里写"启动一个后台进程"。

**为什么会犯**：两层的能力有交集（都涉及"让 agent 会做某件事"），而第 10 章刚讲完 skill，手上正好有一个 skill 目录。**两个概念在读者的心智里合并了。**

**后果**：装不上（缺清单），或者装上了但模型不读操作说明（模型不读 `openclaw.plugin.json`）。

**正确做法**：在一个 plugin 工程里**携带** skill：

```json5
{
  id: "silicon-life-training",
  skills: ["./skills"]         // ← plugin 携带 N 个 SKILL.md
}
```

**30 秒自查**：

```bash
# 1) plugin 目录里是否有清单
ls ./openclaw.plugin.json 2>&1

# 2) 清单是否为 skill / tool 组合（有 skills 字段即为合法的"超集"用法）
grep -n '"skills"' openclaw.plugin.json

# 3) 边界对照：Skill = SKILL.md + references/scripts/assets
#               Plugin = + openclaw.plugin.json + 运行期代码
```

---

### 11.11.8 误区八 · 未本地验证就 `clawhub publish`（反 PAM 约束 + 不可回滚）

**症状**：你发布了一个自己没装过、没跑过、没有触发证据的包。

**为什么会犯**：`publish` 在直觉上像"保存"——一次提交而已。而它其实是**一次对外的事实发布**，没有撤回。

**后果**：三层损失——① 别人装了你的坏包，消耗了生态信任；② 你不能重发同版本号（版本号是一次性事实）；③ 你的 dry-run 机会被浪费在一个已经出门的包上。

**正确顺序（六条全绿才出门）**：

```text
[ ] validate 通过
[ ] install 成功
[ ] enable 成功 + list --enabled 可见
[ ] doctor 无 error
[ ] 真触发一次（时间戳证据）
[ ] 静态合规：无 manifest.yaml / 无凭证 / 无绝对路径
```

**30 秒自查**：

```bash
ls -l ~/*trigger*.stamp 2>/dev/null        # 有触发证据吗
find . -name 'manifest.yaml' | wc -l       # 期望 0
grep -rn 'token\|secret' ./references ./scripts 2>/dev/null | wc -l   # 期望 0
```

---

### 11.11.9 误区九 · 把 `53/73` 当成"质量分"，或把 `disabled` 当"坏了"

**症状**：写"本机插件健康度 73%"；或者看到 `a2a` 是 disabled，就去"修"它。

**为什么会犯**：`53/73` 长得像一个比例，比例长得像一个分数。而人看到分数就想评价它。

**后果**：① 你会去"提高"一个不需要提高的数字；② 你会去 enable 一个**故意默认禁用**的 stock 插件，从而改变系统行为。

**正确读法**：

| 数字 | 含义 | 不是 |
|---|---|---|
| `73` | 被发现的 plugin 数（含 stock） | 不是"你装的" |
| `53` | 处于启用状态的数 | 不是"能用的" |
| `20` | disabled | **不是"坏的"** |
| `74%` | 53÷73 | **不是健康度** |

**`a2a` 的具体情况**：它是 **stock** plugin（`stock:a2a/index.js`），状态 **disabled**。这是默认策略，不是故障。

**健康以 `openclaw plugins doctor` 的结论为准**，不以比例为准。

**30 秒自查**：

```bash
openclaw plugins list 2>&1 | head -1            # 拿两个数
openclaw plugins doctor 2>&1 | tail -10         # 拿真正的健康结论
openclaw plugins list 2>&1 | grep -c 'stock:'   # 看 stock 占比（本机以 stock 为主）
```

---

### 11.11.10 九个误区的一页速查

| # | 误区 | 根因 | 可自动检测 | 本机/生态暴露度 |
|---|---|---|---|---|
| 1 | `manifest.yaml` | 云原生肌肉记忆 | ✅ | 高（行业普遍误植） |
| 2 | `openclaw plugin`（单数） | 命名习惯 | ✅ | 高 |
| 3 | install 后忘 enable | 语言直觉 | ✅ | **最高（P0）** |
| 4 | `workspace/plugins/` | 路径外推 | ✅ | 中 |
| 5 | 用重写型命令改 JSON5 | 注释被规范化掉 | ⚠ | 中（本机 live 版本曾有注释告警） |
| 6 | 跳过 build/pack/validate | 开发节奏 | ✅ | 高（开发者） |
| 7 | Plugin / Skill 混淆 | 概念同源 | ⚠ | 中 |
| 8 | 未验证就 publish | "发布像保存" | ❌ | 中（且代价最高） |
| 9 | `53/73` 当质量分 | 比例幻觉 | ❌ | 中 |

**最后一条纪律**：这九个误区有一个共同结构——**它们全部发生在"你以为已经完成"的那一刻之后**。`install` 成功了、文件在、列表里有、命令没报错……而这些都不构成"它生效了"。

> **本章唯一需要真正记住的一句话**：
> **装进机器是文件系统事实；进入运行期是行为事实；两者之间隔着一个 `enable`，和一次真实的触发。**

---

## 11.12 深度专题

### 11.12.1 专题一 · 2026 前沿追踪：ClawHub 生态与 MCP 扩展机制

#### 一、ClawHub：一个中心化分发通道意味着什么

把本章前九节串起来看，ClawHub 的位置很清楚：

```text
写 → build → pack → validate → 【 ClawHub 】 → install → enable → 运行
                                  ↑
                         唯一一个"出门"的环节
```

**它有四个结构特征：**

| 特征 | 具体表现 | 意义 |
|---|---|---|
| **独立 CLI** | `clawhub`（不与 `openclaw` 同包） | 发布权限按需展开 |
| **身份准入** | GitHub OAuth，账号 **≥ 1 周** | 反 PAM / 反批量垃圾包 |
| **CI 优先** | 复用 GitHub Actions 工作流 + `clawhub_token` / OIDC | 发布可审计、可归因 |
| **family 分类** | `code-plugin` / `skill` / 其他 | 决定分发路径与安装预期 |

**为什么"独立 CLI"是一个值得单独说的设计？**

因为它把**一个系统的攻击面**按角色的实际需要切开了。一个只在本机跑 agent 的用户，他的环境里根本不存在"能往公共索引发布东西"的工具。这在安全工程里是最划算的一类设计——**不是把门锁得更紧，而是让不需要门的人家里没有门。**

**发布链的可信要素**：版本号（一次性事实）+ 签名 + source attribution + upload plan。四者合起来回答："这个字节流是谁、什么时候、从哪个 commit 发出来的。"

**本机对应的只读入口**：

```bash
openclaw plugins search <query> --limit 5 --json     # 搜 ClawHub 包
openclaw plugins marketplace entries                 # 检视 Claude 兼容 marketplace
openclaw plugins registry --json                     # 本机持久化注册表（注意：不是 ClawHub）
```

#### 二、MCP 的扩展机制（2026-07-28）：为什么 plugin 与 MCP 不是竞争者

2026 年的另一个重要演进发生在 MCP 侧：**扩展机制（extensions）**在 2026-07-28 成为协议层的正式主题。

很多读者会问："既然有 MCP，为什么还需要 plugin？这不重复吗？"

**答案是：它们在不同的层，解决不同的问题。**

| 维度 | MCP（第 8 章） | Plugin（本章） |
|---|---|---|
| 解决的问题 | **agent ↔ 工具** 的发现与调用 | **训练学 ↔ 用户** 的安装与分发 |
| 边界 | 跨进程、协议化、语言无关 | 单进程内、OpenClaw runtime 专属 |
| 分发单位 | MCP server（任意语言实现） | `openclaw.plugin.json` + JS/TS 代码 |
| 能力声明 | `tools/list`（运行期可查） | `contracts.tools`（**安装前可查**） |
| 配置 | server 自身配置 | `configSchema` + `uiHints`（含 UI 表单化） |
| 生命周期 | 启动/连接 | 七阶段 + capability 确权 |

**关键差异是"何时可查"**：

- MCP：能力要**连上之后**才能 `tools/list` 查到；
- Plugin：能力在**安装之前**就能从 manifest 读到，并且用户必须显式 `--accept-capabilities`。

**后者才是"可确权"**。这也是本章反复强调 capability 确权的原因——**它是这套生态与"`pip install` + 自动执行"那一代做法的根本区别。**

**在 2026 年的扩展机制语境下，两者的关系是互补的：**

```text
Plugin  → 训练学的"装配层"（装什么、启什么、装之前看到什么）
MCP     → 训练学的"工具层"（能调用什么，按标准协议）
Skill   → 训练学的"能力层"（对的时候想起什么）
契约     → 训练学的"约束层"（永远在场的红线）
```

**四层齐备，训练学才算完整落地。** 少任何一层，你都会在某个具体场景里发现"讲得很清楚，但做不到"。

#### 三、2026 年值得跟踪的三条线

1. **组织级治理在分发侧的落地**：当 skill 与 plugin 都成为组织资产，谁能发布、谁能下架、谁审计——这条线在第 10 章（skill 组织级管理，2026-02 起）与本章（ClawHub 准入）两头同时演进。
2. **能力确权的粒度**：目前是"整包接受"。未来是否会出现"按 capability 选择性接受"（比如接受 `read_file` 但拒绝 `terminal`）——这会显著改变第三方插件的采纳决策。
3. **plugin 携带 skill 的标准化**：`skills` 字段让"知识 + 代码"可以一起分发。它是否会成为 Agent Skills 标准的一部分，决定了两层能否在跨平台场景下真正合并。

#### 四、前沿跟踪纪律

- ✅ 可引用：ClawHub 的五步流程与六条约束；`clawhub` 独立 CLI 事实；MCP 2026-07-28 扩展机制；本章 15 子命令与 16 字段（本机/文档双源实测）。
- ⏳ 必须保留 ⏳：`clawhub package publish` 本机未执行；七阶段完整跑通未验证；plugin 携带 skill 的跨平台行为未验证。
- ❌ 不得写入：未经验证的版本号传闻；"ClawHub 是 OpenClaw 内置 registry"（错）；把本书 RFC 提案（`contracts.hooks` / `policy.proactiveness` / `ooda.*`）写成既有字段。

---

### 11.12.2 专题二 · 六大框架对位表

#### 一、对位口径

对位对象：**LangGraph · AutoGen（AG2）· CrewAI · Claude Agent SDK · OpenAI Agents SDK · LlamaIndex**

对位的四个问题：

1. 分发单位是什么？
2. 清单（manifest）是什么形态、谁读？
3. 安装与启用是否分离？能力是否需要用户确权？
4. 有没有"运行期插件的治理入口"？

#### 二、主对位表

| 维度 | **OpenClaw plugin（本章）** | LangGraph | AutoGen (AG2) | CrewAI | Claude Agent SDK | OpenAI Agents SDK | LlamaIndex |
|---|---|---|---|---|---|---|---|
| **入口命令** | `openclaw plugins install`（复数）⚡ | `pip install -e .` | `pip install` | `pip install` | `claude plugin install` | `pip install` | `pip install` |
| **清单格式** | **`openclaw.plugin.json`（JSON5）** ⚡ | `pyproject.toml` + `langgraph.json` | `pyproject.toml` | `pyproject.toml` + YAML | `plugin.json` | `agent.yaml` | `pyproject.toml` |
| **生命周期 CLI** | **15 子命令**（init/build/pack/validate/install/enable/doctor/update/…）⚡ | 5 个（build/serve/test/deploy/inspect） | 2 个 | 3 个 | 2 个 | 2 个 | 2 个 |
| **安装 / 启用分离** | **是**（install ≠ enable，两步确权）⚡ | 否（装即用） | 否 | 否 | 否 | 否 | 否 |
| **Capability 接受机制** | **`--accept-capabilities`（install / enable / update 三处）** ⚡ | 自动接受 | 自动接受 | 自动接受 | 自动接受 | 自动接受 | 自动接受 |
| **能力声明位置** | `contracts.tools`（**安装前可查**）⚡ | 注册即生效 | schema 注册 | 注册表 | tools 列表 | 函数注册 | 代码注册 |
| **能力声明 + UI 表单** | `configSchema` + `uiHints`（sensitive / placeholder / advanced）⚡ | 无 | 无 | 无 | 无 | 无 | 无 |
| **产物 vs 输入** | **`build` 显式生成 + `--check` 过期检测** ⚡ | 隐式 | 隐式 | 隐式 | 隐式 | 隐式 | 隐式 |
| **打包产物** | `.tgz` + SHA256 + activation request ⚡ | wheel | wheel | wheel | tarball | wheel | wheel |
| **配置入口** | `~/.openclaw/openclaw.json`（JSON5，注释敏感）⚡ | 环境变量 | 环境变量 | 环境变量 | 环境变量 | 环境变量 | 环境变量 |
| **Runtime 依赖沙盒** | `plugin-runtime-deps/`（含 json5 等）⚡ | `pip install` | `pip install` | `pip install` | `npm install` | `pip install` | `pip install` |
| **中心注册中心** | **ClawHub**（公共 · GitHub OAuth ≥ 1 周）⚡ | LangChain Hub | AG2 Hub | CrewAI Marketplace | Anthropic Hub | OpenAI Hub | LlamaHub |
| **市场搜索 CLI** | `openclaw plugins search`（直连 ClawHub）⚡ | 仅 web UI | 仅 web UI | 仅 web UI | 仅 web UI | 仅 web UI | 仅 web UI |
| **多源安装** | **6 种**（path / archive / npm / git / clawhub / marketplace）⚡ | 1 种（pip） | 1 种 | 1 种 | 1 种 | 1 种 | 1 种 |
| **运行期诊断** | **`plugins doctor`（四类问题分类）** ⚡ | 无 | 无 | 无 | 无 | 无 | 无 |
| **回滚演练** | `uninstall --dry-run` / `update --dry-run` ⚡ | 无 | 无 | 无 | 无 | 无 | 无 |
| **训练学底座概念** | **⚡ 领先**（plugin = 训练学外化） | ○ 空白 | ○ 空白 | ○ 空白 | ○ 空白 | ○ 空白 | ○ 空白 |
| **真名校验** | `openclaw --version` + `plugins --help` 双验 ⚡ | 无 CLI | 无 CLI | 无 CLI | `claude --version` | `openai --version` | 无 |

> ⚡ = 本节认为领先 / ○ = 空白或互补

#### 三、逐条解读

**① 领先点集中在"分发与治理"这一侧，不在"编排"那一侧。**

这一点必须说清楚，否则会变成不诚实的自夸：LangGraph / AutoGen / CrewAI 在**编排能力**（图、状态机、角色协作）上远比本章讨论的东西复杂。本章的比较范围**只是"插件分发与治理"这一竖条**。

在这个竖条上，OpenClaw 有 10 个领先项：**15 子命令 / install≠enable 分离 / capability 三次确权 / 安装前可查的能力声明 / configSchema+uiHints / 显式生成产物 + 过期检测 / SHA256 artifact / 6 种安装源 / doctor 四类诊断 / dry-run 演练**。

**② "install ≠ enable" 是这张表里最本质的一行。**

其他 6 个框架的安装都是"装即用"。这个选择的代价是：**用户没有表达"我想先看看"的机会。**

对企业采纳第三方插件来说，这不是便利性问题，是**采购决策问题**——它决定了安全评审能不能在被批准的边界内进行。

**③ `configSchema` + `uiHints` 是一个被低估的差异。**

其他框架的配置都是"写环境变量 / 改 YAML"。OpenClaw 用 JSON Schema 声明配置结构，用 `uiHints` 声明表单渲染（`sensitive: true` = 密码框，`advanced: true` = 折叠面板）。

**它把"配置"从一个工程动作，变成了一个产品界面。** 对训练学特别重要：训练学的配置项（agent 名、审计节律、主动性档位）本来就该被"填写"而不是"拼环境变量"。

**④ 唯一的空白：训练学底座概念。**

表中最后两行是 6 个框架全部为 ○ 的地方：

- **训练学底座概念**：没有任何框架把"plugin = 训练学外化"作为产品哲学；
- **真名校验**：一半框架连一个可跑的 CLI 都没有。

**⑤ 与其他章节对位的关系。**

本章的对位表是**局部版**（聚焦"分发与治理"一个竖条）。全书范围的六框架对位在 `./_industry-frontier-tracking.md` §1 / §2.11 中维护；第 10 章的 skill 侧对位表是它的镜像（聚焦"能力单元形态"）。三张表互补，不重复。

#### 四、把训练学放进这张表

| 训练学组件 | 在 OpenClaw plugin 里的落点 | 其他 6 框架 |
|---|---|---|
| 七大契约 | 契约文件（always-on）+ plugin 不承载 | ○ 空白 |
| 漂移治理 · 每周体检 | `activation.onStartup` + `weekly-health-check.ts` → `plugin-state/<id>/health.json` | ○ 空白 |
| 三省制 + Trust Score + Merit Ledger | hook `before-tool-call` / `after-tool-call` → `~/.openclaw/merit/<id>.jsonl` | ○ 空白 |
| 主动性边界三档 | ⏳ RFC 提案字段 `policy.proactiveness` | ○ 空白 |
| A2A 反脆弱 + 让位协议 | ⏳ RFC 提案：`response-yield.ts` + `contracts.hooks` | ○ 空白 |
| OODA 自主目标生成 | ⏳ RFC 提案：四个 hook | ○ 空白 |

> ⚠ **注意这张表的"⏳"**：五项优势里有两项（体检、计分）**现在就能做**；三项（让位/主动性/OODA）是**本书的 RFC 提案**，不是 OpenClaw 现行字段。**引用时不得省略 ⏳。**

---

### 11.12.3 专题三 · 本机实测审计（plugin 侧）

> 本节全部数字来自本机 2026-09-27 实跑（`openclaw plugins list` / `openclaw plugins --help` / `openclaw --version`）。

#### 一、plugin 体检总表

| # | 指标 | 实测值 | 口径 / 命令 |
|---|---|---|---|
| 1 | 发现的 plugin 总数 | **73** | `openclaw plugins list` 头行 |
| 2 | **enabled** | **53** | 同上（`Plugins (53/73 enabled)`） |
| 3 | disabled | **20** | 73 − 53 |
| 4 | 主要来源 | **stock 为主** | `list` 的 Source roots：`stock: /Users/.../openclaw/dist/extensions` |
| 5 | `~/.openclaw/extensions/` | **不存在** | `ls` 实测 → **未装自定义 plugin** |
| 6 | 子命令数 | **15** | `openclaw plugins --help` |
| 7 | 主配置真名 | `~/.openclaw/openclaw.json` | `plugins list` 头部输出 |
| 8 | **`a2a` plugin 状态** | **disabled**（`stock:a2a/index.js`） | `openclaw plugins list \| grep -i a2a` |
| 9 | 底座版本（live） | `OpenClaw 2026.9.6 (eb377ac)` | `openclaw --version` |
| 10 | 底座版本（书内口径） | `OpenClaw 2026.9.4 (3a9d69d)` | 本书统一口径 |
| 11 | 早期基线（对照） | 51 / 69 enabled（API 附录口径） | 见 `_appendix-api/06-skill-manifest-reference.md` |

#### 二、四个必须诚实说明的地方

**（一）`53/73` 不是健康度。**
它是"被发现数 / 启用数"。真正的健康结论看 `openclaw plugins doctor`。

**（二）`a2a` disabled 是事实，且重要。**
`a2a` 是 **stock** plugin，来源 `stock:a2a/index.js`，状态 **disabled**。这意味着：

- 第 9 章的 A2A 内容口径必须是"**协议层可达 + 本机未启用**"；
- **不得**写"本机 A2A 已在运行"；
- 不得把它的 disabled 状态当成故障去"修"。

**（三）`~/.openclaw/extensions/` 不存在是一个正确结果。**
它意味着本机**从未装过自定义 plugin**。所以本章关于 `install` / `enable` 的完整流程属于**命令真名已实测 + 端到端流程未跑通**——两者必须分开表述。

**（四）版本有两个数。**
`2026.9.6 (eb377ac)` 是本机 live；`2026.9.4 (3a9d69d)` 是本书统一口径。**引用时必须说明是哪一个**，否则会得出"书里的命令在我这儿不对"的误判。

#### 三、可复现脚本

```bash
#!/usr/bin/env bash
# plugin-audit.sh — 本章 plugin 体检的最小可复现实现
set -u

echo "=== plugin-audit $(date '+%Y-%m-%d %H:%M:%S') ==="
echo "底层版本:      $(openclaw --version 2>&1 | tail -1)"
echo "命令族真名:    $(openclaw plugins --help 2>&1 | head -1)"
echo "子命令数:      $(openclaw plugins --help 2>&1 | grep -cE '^  [a-z]')"
echo "发现 / 启用:   $(openclaw plugins list 2>&1 | head -1)"
echo "stock 条目数:  $(openclaw plugins list 2>&1 | grep -c 'stock:')"
echo "disabled 数:   $(openclaw plugins list 2>&1 | grep -c 'disabled')"
echo "a2a 状态:      $(openclaw plugins list 2>&1 | grep -i 'a2a' | head -1)"
echo "安装目录:      $(ls -d ~/.openclaw/extensions 2>/dev/null || echo 不存在)"
echo "主配置:        $(ls -l ~/.openclaw/openclaw.json 2>/dev/null | awk '{print $5" bytes"}' || echo 缺失)"
echo "--- doctor ---"
openclaw plugins doctor 2>&1 | tail -12
```

**建议**：把这份脚本每季度跑一次，输出追加到日志。**一年之后你会有"插件生态演化史"**——它比任何一次体检都值钱。

#### 四、跨层对照（一张表看清四层）

| 层 | 指标 | 本机实测 | 对应章节 |
|---|---|---|---|
| Contract 层 | 契约文件 7 类 | 各 agent `contracts/` 下 | 第 1 章 |
| Skill 层 | skill 目录 **236**（含 `SKILL.md` **221**） | ✅ 实测 | 第 10 章 |
| Tool 层 | MCP 原语 | 仅隐式使用（8/46 口径） | 第 8 章 |
| Plugin 层 | **73 发现 / 53 启用** / `extensions/` 不存在 | ✅ 实测 | **本章** |
| Agent 层 | **18** 个已注册 agent | ✅ 实测 | 第 6 章 |

**这张表本身就是本章最重要的产物之一**：它证明"四层接口"不是概念划分，而是**四组可以分别计数的真实对象**。**任何声称"我的系统实现了分层"的说法，都要能给出每一层的独立计数。给不出来的，就是概念。**

---

### 11.12.4 专题四 · 诚实边界

#### ✅ 已实测（可直接引用）

| # | 事实 | 证据 |
|---|---|---|
| 1 | `openclaw plugins` 命令族为**复数**，共 **15 子命令** | `openclaw plugins --help` 实跑 |
| 2 | 本机 plugin 现状 **53 / 73 enabled** | `openclaw plugins list` 实跑 |
| 3 | **`a2a` plugin = disabled**（`stock:a2a/index.js`） | `list \| grep -i a2a` 实跑 |
| 4 | `~/.openclaw/extensions/` **本机不存在** | `ls` 实跑 |
| 5 | 主配置真名 `~/.openclaw/openclaw.json` | `plugins list` 头部输出 |
| 6 | `plugins build --check` 存在（产物过期检测） | `plugins build --help` 实跑 |
| 7 | `openclaw --version` = **2026.9.6 (eb377ac)** live | 命令实跑 |
| 8 | 清单真名 `openclaw.plugin.json`，格式 JSON5 | 本机 stock plugin 实测 |
| 9 | `configSchema` 硬要求 `{type:"object", additionalProperties:false}` | 文档 + 实测双源 |
| 10 | ClawHub 五步流程与六条约束（账号 ≥ 1 周等） | 官方文档 + 教程 |
| 11 | `openclaw backup create` / `openclaw doctor` / `openclaw setup` / `openclaw agents add` 均为真名 | 命令实跑 |

#### ⏳ 待验证（引用时必须保留 ⏳）

| # | 事项 | 为什么还没验证 |
|---|---|---|
| 1 | **完整七阶段生命周期**（init → build → pack → install → enable → doctor） | 本机未装自定义 plugin，未端到端跑通 |
| 2 | `clawhub package publish` 的实际行为 | 受反 PAM 约束（账号年龄），本机未执行 |
| 3 | `contracts.hooks` / `policy.proactiveness` / `ooda.*` 字段 | **本书 RFC 提案**，OpenClaw 现行 manifest 无此字段 |
| 4 | plugin 携带 skill 的跨平台装载行为 | 未做跨客户端验证 |
| 5 | capability 按项选择性接受 | 当前为整包接受，未来演进方向 |
| 6 | `~/.openclaw/plugin-state/` / `~/.openclaw/merit/` 目录约定 | 本书设计建议，非实测既有路径 |

#### ⚠ 不得宣称（写了就是错）

| # | 不得写 | 正确表述 |
|---|---|---|
| 1 | `openclaw plugin install`（单数） | **`openclaw plugins install`**（复数，15 子命令） |
| 2 | `manifest.yaml` | **`openclaw.plugin.json`**（JSON5） |
| 3 | 安装目录在 `~/.openclaw/workspace/plugins/` | 真名 **`~/.openclaw/extensions/`**（本机不存在） |
| 4 | 配置入口是 `~/.openclaw/config.yaml` | 真名 **`~/.openclaw/openclaw.json`**（JSON5，注释敏感） |
| 5 | "ClawHub 是 OpenClaw 内置 registry" | ClawHub 是**独立 CLI + 服务**；`plugins registry` 只服务本机持久化注册表 |
| 6 | "本机 73 个插件健康度 74%" | "73 个被发现、53 个启用；**健康以 `plugins doctor` 为准**" |
| 7 | "本机 A2A 已在运行" | `a2a` 是 **stock + disabled**；第 9 章为"协议可达 + 本机未启用" |
| 8 | "install 之后就能用" | 必须再 `enable`（三步确权：install / enable / update） |
| 9 | 把 `contracts.hooks` / `policy.proactiveness` / `ooda.*` 当既有字段 | 那是**本书 RFC 提案**，必须标 ⏳ |
| 10 | "本机 OpenClaw 版本 2026.9.4" | 2026.9.4 是**书内口径**；live 为 **2026.9.6 (eb377ac)**——两个都写清 |
| 11 | 把 Skill 与 Plugin 混为一谈 | Skill = 单文件能力包（Markdown · 跨平台）；Plugin = 工程产物（JSON5 + Code · 启动期加载） |
| 12 | 沿用旧调研报告"openclaw plugin install 不存在"的结论 | 该结论已被本机实测推翻（勘误 #1） |

#### 最后一段：这一章真正想留下的

如果本章只能留下一句话：

> **分发层的价值不在"能打包"，而在"打出来的包，别人装得上、用得起、出问题查得到"**——而这三件事，恰好对应安装、启用、诊断三道工序。"装得上"（install）解决文件问题，"用得起"（enable + 触发）解决行为问题，"查得到"（doctor + dry-run + 日志）解决运维问题。

**只有三道工序都走完，方法论才算真正装进了别人的机器。**

---

> **本章引用提示**：v1.0 的对应内容为 `openclaw-silicon-life-handbook/volume-12/` 系列（插件相关章节）。⚠ 引用注意：旧版关于"`openclaw plugin`（单数）"与"插件安装目录在 workspace 下"的表述**均已实测推翻**，不得沿用。

---

### 11.12.5 术语双写锚点（本章统一写法）

本章所有术语一律采用「中文新名（English alias，原：旧称）」的双写形式。锚点如下：

| 术语 | 本章统一双写形式 | 相关节 |
|---|---|---|
| 插件清单 | Plugin Manifest（插件清单；真名 `openclaw.plugin.json`） | 11.0.4 / 11.2 |
| 配置模式 | configSchema（配置模式） | 11.2 |
| 界面提示 | uiHints（界面提示） | 11.2 |
| 插件入口 | Plugin Entrypoint（插件入口） | 全章 |
| 能力确权 | Capability Acceptance（能力确权；`--accept-capabilities`） | 11.4 / 11.9 |
| 技能注册表 | Skill Registry（技能注册表；本机持久化 registry ≠ ClawHub） | 11.5 |
| 渐进式披露 | Progressive Disclosure（渐进式披露；Skill 层机制，见第 10 章） | 11.6 |
| 可复用能力单元 | Reusable Capability Unit（可复用能力单元；Skill 形态） | 11.6 |
| 技能基因 | Skill Gene（技能基因；Skill 层保留昵称） | 11.6 |
| 智能体集群 | Agent Fleet（智能体集群，原：军团） | 11.8 |
| 监督层 | Supervisor Layer（监督层，原：监军） | 11.12.2 |
| 漂移治理 | Drift Governance（漂移治理） | 11.8 |
| 主动性边界三档 | Autonomy Boundary Triad（主动性边界三档，原：三档制） | 11.8 |
| 响应让渡协议 | Response Yield Protocol（响应让渡协议，原：让位协议） | 11.8 |
| 任务交接协议 | Task Handover Protocol / THP（任务交接协议） | 11.8 |
| 三证据验证 | Three-Evidence Verification / TEV（三证据验证，原：三证验真） | 11.10.6 |
| 修复工单 | Remediation Ticket（修复工单，原：整改单） | 11.12.4 |
| 多智能体编排 | Multi-Agent Orchestration（多智能体编排，原：军团编制） | 11.6 |

---

---

## 附录 A · 本章操作手册（原「SOP · 本章怎么用」节后移 · 一字未删）

> ⚠ **本区块 = 章末后移的原文操作手册与附件**（逐字保留，未作任何删改）。
> 其中出现的历史章号字样（如「第 12 章」）属于章号统一前口径；**本书现行章号以文件首行为准——本章 = 第 11 章 = 路径 `chapters/11-plugin-entrypoint/`**。
> 这里的数字口径、命令真名与正文完全一致；只想马上动手的读者可直接从下方「步骤 1」开始。

## SOP · 本章怎么用

> **实测环境**：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27 · macOS 26.5.1 · `openclaw plugins --help` = **15 子命令**实测 · `openclaw plugins list` = **51/69 enabled** 实测
> **本章定位**：v5.0 行业标准版 · 第 12 章（路径 `12-plugin-entrypoint`）· Plugin 入口：把硅基生命训练学装进 OpenClaw（接口层 4/4 · 工程接口层 · 分发层）
> **预计用时**：速读 30 分钟 · 工程读 60 分钟 · 全读 90 分钟
> **前置依赖**：第 11 章（Skill 注册）已读，理解"Skill = 单文件能力包 / Plugin = Skill 超集"

### 步骤 1 · 读完本章需要什么

**前置章节**：
- 第 11 章 · Skill 注册（接口层 3/4，理解 Skill 是 Plugin 的构成单元）→ `chapters/10-skill-registry/README.md`
- 第 10 章 · A2A 绑定（接口层 2/4）→ `chapters/09-a2a-binding/09-A2A绑定.md`

**前置文件**：
- `~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/00-术语对照表·v3.0行业标准版.md`（35 条改名表，本章引用 #31 reserveTokensFloor 真名漂移 / #34 本机版本 2026.9.4 / #35 OpenClaw License=MIT）
- 本章同目录 7 文件：`README.md`（本文件）/ [`openclaw.plugin.json`](./openclaw.plugin.json) / [`install-指南.md`](./install-指南.md) / [`配置项.md`](./配置项.md) / [`8卷挂载映射.md`](./8卷挂载映射.md) / [`OpenClaw-官方RFC-草案.md`](./OpenClaw-官方RFC-草案.md) / [`真名验证与勘误.md`](./真名验证与勘误.md)

**前置命令**：
```bash
# 验证 OpenClaw 版本（plugin manifest + 子命令族基于此版本）
openclaw --version 2>&1 | tail -1
# 期望：OpenClaw 2026.9.4 (3a9d69d)

# 验真 15 子命令真名（plural——不是 singular `openclaw plugin`）
openclaw plugins --help 2>&1 | sed -n '/Commands:/,/^$/p'
# 期望：build / disable / doctor / enable / init / inspect / install / list /
#       marketplace / pack / registry / search / uninstall / update / validate
```

### 步骤 2 · 必做的 3 件事

**1. 验真 `openclaw plugins`（plural）+ 15 子命令（本章最重要的一节 12.2/12.3）**

12.2 列了 7 个业界高频误植的真名。本章中心论断：**命令是 `openclaw plugins`（plural）**，配置文件是 **`openclaw.plugin.json`（JSON5）**。**亲手跑一次比读十遍管用**。

```bash
# 复制粘贴：验真 plural + 子命令清单
openclaw plugins --help 2>&1 | grep -cE "^  (build|disable|doctor|enable|init|inspect|install|list|marketplace|pack|registry|search|uninstall|update|validate)"
# 期望：15（15 个子命令全部命中）

# 反例检测：确认没有 singular 命令（应报错）
openclaw plugin --help 2>&1 | grep -qi "unknown\|not found\|error" && echo "✓ 无 singular 命令（真名是 plural）"
# 期望：✓ 无 singular 命令（真名是 plural）

# 本机已装插件清单（51/69 enabled 实测基线）
openclaw plugins list 2>&1 | head -3
# 期望：头行 "Plugins (51/69 enabled)"
```

**2. 抄一份 `openclaw.plugin.json` JSON5 字段表 + manifest 模板**

12.5 节的本机字段表（16 字段：`id`/`name`/`description`/`kind`/`categories`/`channels`/`skills`/`contracts.tools`/`activation.onStartup`/`activation.onEvent`/`configSchema`/`uiHints`/`openclaw.install`/`channelConfigs`/`capabilityCatalogEntry`/`exposure`）是 plugin 的**唯一配置入口**。把本章的 `openclaw.plugin.json` 模板复制到你自己的 plugin 目录。

```bash
# 复制粘贴：把你的 plugin manifest 从章节模板起手
mkdir -p ~/.openclaw/workspace/silicon-life-training
cp ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/chapters/11-plugin-entrypoint/openclaw.plugin.json \
   ~/.openclaw/workspace/silicon-life-training/openclaw.plugin.json

# 验证 JSON5 可解析（注释 + trailing comma 都应被接受）
python3 -c "import json5" 2>/dev/null && python3 -c "import json5;json5.load(open('$HOME/.openclaw/workspace/silicon-life-training/openclaw.plugin.json'));print('✓ JSON5 解析通过')" \
  || echo "⚠ 未装 json5 py 包——用 node: npx json5 -c <file> 验证"
# 期望：✓ JSON5 解析通过（或 node 侧验证通过）

# 关键硬字段自检：configSchema 必须 {type:object, additionalProperties:false}
grep -n '"additionalProperties": false' ~/.openclaw/workspace/silicon-life-training/openclaw.plugin.json
# 期望：命中 ≥ 1 行（configSchema 硬要求）
```

**3. 跑一遍只读运维三件套，摸清本机 plugin 现状（不改变任何状态）**

12.3.2 给了运维 3 件套：`doctor`（诊断）/ `list`（清单）/ `update --dry-run`（预览）。**本章 SOP 只跑只读命令**——安装/启用/更新属状态变更，本机 ⏳ 未实测。

```bash
# 复制粘贴：只读运维三件套
openclaw plugins doctor 2>&1 | tail -5            # 诊断 loading 问题
openclaw plugins list --enabled 2>&1 | head -3    # 只看已启用
openclaw plugins list --json 2>&1 | python3 -c "import sys,json;d=json.load(sys.stdin);print('✓ plugins JSON 可解析，条数 =', len(d) if isinstance(d,list) else 'n/a')" 2>/dev/null || echo "（--json 输出结构以本机为准）"
# 期望：doctor 无 error；list 头行 51/69 enabled
```

### 步骤 3 · 检查清单

- [ ] **版本验证**：`openclaw --version` ≥ 9.4（plugin 15 子命令基于 9.4）
- [ ] **plural 验真**：`openclaw plugins --help` 命中 ≥ 11 个子命令（9.4 基线 6 个 + 新增 9 个 = 15）；`openclaw plugin`（singular）报错
- [ ] **真名验真**：plugin 配置文件名是 `openclaw.plugin.json`（**JSON5**），不是 `manifest.yaml`
- [ ] **manifest 模板落盘**：`~/.openclaw/workspace/silicon-life-training/openclaw.plugin.json` 存在且 JSON5 可解析
- [ ] **`configSchema` 硬要求**：含 `{type:object, additionalProperties:false}`
- [ ] **install ≠ enable 已理解**：`plugins install` 只复制文件 + 注册到 `plugins.installs`，**必须再跑 `plugins enable <id> --accept-capabilities`** 才进运行时（12.4 关键 trap）
- [ ] **诚实边界已知**：未跑完整 5 阶段生命周期（init→build→pack→validate→install）；未跑 `plugins install`；未跑 ClawHub publish（账号 < 1 周不满足反 PAM 约束）——见本章 12.10

### 步骤 4 · 常见错误（缩略版 · 完整版看 FAQ 卷）

- ❌ **不要用 `openclaw plugin`（singular）**——**真名是 `openclaw plugins`（plural）**（12.2 表 #1）
- ❌ **不要假设配置文件是 `manifest.yaml`**——**真名 `openclaw.plugin.json`（JSON5）**；`manifest` 是 `plugins build` 的**生成产物**，不是源文件（12.2 表 #2/#3）
- ❌ **不要把 `install` 和 `enable` 混为一步**——`plugins install` **不会自动 enable**；未 enable 的 plugin 不进运行时（12.4 关键 trap）
- ❌ **不要假设安装目录是 `~/.openclaw/workspace/plugins/`**——**该目录不存在**；真路径 **`~/.openclaw/extensions/`**（Apify README 实证）⚠ 本机尚未创建（未装自定义 plugin）
- ❌ **不要假设配置入口是 `~/.openclaw/config.yaml`**——**真名 `~/.openclaw/openclaw.json`（JSON5）**（12.2 表 #5；本机已存在，45 445 bytes 实测）
- ❌ **不要把 ClawHub 当"OpenClaw 内置 registry"**——**ClawHub 是独立 CLI**（`npm i -g clawhub`）；OpenClaw 主仓的 `plugins registry` 只做**本机持久化重建**（`--refresh`）
- ❌ **不要用 `openclaw config set` 改带注释的 JSON5**——它会改写成标准 JSON，**无声丢弃注释**（docs.openclaw.ai/cli/config 警告）；应手编 + `config patch`
- ✅ **应该做**：manifest 用 `categories`（**数组**），不是 `category`（单数）
- ✅ **应该做**：runtime 依赖（如 `json5`）放进 `plugin-runtime-deps/`——issue #77461 本机修复案例：缺 `json5` 会让 `memory_search` 失败

### 步骤 5 · 做完怎么验

```bash
# === 验证 1：版本正确 ===
openclaw --version 2>&1 | tail -1
# 期望：OpenClaw 2026.9.4 (3a9d69d)

# === 验证 2：15 子命令真名齐全 ===
openclaw plugins --help 2>&1 | grep -cE "^  (build|disable|doctor|enable|init|inspect|install|list|marketplace|pack|registry|search|uninstall|update|validate)"
# 期望：15

# === 验证 3：plugins 现状可读（51/69 基线）===
openclaw plugins list 2>&1 | head -1
# 期望：Plugins (51/69 enabled)

# === 验证 4：你的 manifest 落盘且 JSON5 合法 ===
test -f $HOME/.openclaw/workspace/silicon-life-training/openclaw.plugin.json \
  && echo "✓ manifest exists" || echo "❌ missing"
grep -q '"additionalProperties": false' $HOME/.openclaw/workspace/silicon-life-training/openclaw.plugin.json \
  && echo "✓ configSchema 硬要求满足" || echo "❌ configSchema 不合法"

# === 验证 5：配置入口真名存在 ===
test -f $HOME/.openclaw/openclaw.json && echo "✓ ~/.openclaw/openclaw.json 存在" || echo "❌ 缺失"
# 期望：✓ ~/.openclaw/openclaw.json 存在
```

**成功标志**：15 子命令真名命中 + `plugins list` 输出 `51/69 enabled` + 你的 manifest JSON5 可解析且含 `additionalProperties:false` + 你能 60 秒讲清"install 和 enable 为什么不是一步"（答案：install 只复制文件+注册 `plugins.installs`，enable 才在 `plugins.entries.<id>.enabled` 置 true 进运行时）。

### 步骤 6 · 验证完成后去哪

- **上一章**：第 11 章 · Skill 注册 → `chapters/10-skill-registry/README.md`（skill 是 plugin 的构成单元）
- **本章实操**：`install-指南.md`（5 阶段 install 命令 + 验证）/ `配置项.md`（13 子命令 flags 全表）
- **5 优势落地**：本章 12.8（5 个差异化优势在 plugin 里的挂载点）→ 优势 1 反脆弱三层 Response Yield Protocol / 优势 2 漂移治理 / 优势 3 主动性边界 / 优势 4 三省评审制 Three-Stage Review + 信任评分 Trust Score + 功绩账本 Merit Ledger / 优势 5 OODA Loop 自主目标生成
- **上游 RFC**：`OpenClaw-官方RFC-草案.md`（RFC 编号 SLT-001）→ 8 卷挂载 → `8卷挂载映射.md`
- **FAQ**：真名疑问 → 本章 12.2 + `真名验证与勘误.md`；ClawHub 疑问 → 本章 12.6 + docs.openclaw.ai/clawhub/quickstart；术语疑问 → `00-术语对照表·v3.0行业标准版.md`

---

## SOP · 诚实边界声明

- ✅ **本章 SOP 基于本机实拉事实**：OpenClaw 2026.9.4 (3a9d69d)（`openclaw --version` 2026-09-27 实拉）· `openclaw plugins --help` = **15 子命令**实测 · `openclaw plugins list` = **Plugins (51/69 enabled)** 实测 · `~/.openclaw/openclaw.json` 存在（45 445 bytes）实测
- ⏳ **本章 SOP 未实测**：未跑完整 5 阶段生命周期（`init → build → pack → validate → install`）；未跑 `openclaw plugins install` 流程；未跑 ClawHub publish（账号 < 1 周不满足反 PAM 约束）——**本 SOP 步骤 2/3/5 只跑只读命令（`--help` / `list` / `doctor`）**，状态变更命令标注为待跑
- ⏳ **`~/.openclaw/extensions/` 本机不存在**：`test -d ~/.openclaw/extensions` 返回 NO SUCH DIR（2026-09-27 实测）——因本机**未装任何自定义 plugin**；章节 12.2 表 #4 的"真路径 = `~/.openclaw/extensions/`"来自 Apify plugin README，本机 ⏳ 未复现
- ⏳ **`policy.proactiveness` / `contracts.hooks` 两个字段未实测**：本章 12.8 声明的 5 优势挂载字段基于 docs.openclaw.ai/plugins/building-plugins 设计文档推断，**待 RFC 提交**（12.10 ⏳）
- ⚠ **13 vs 15 子命令口径差异**：本章 12.3 标题写"13 个子命令全景"，但同节正文 + `--help` 实测是 **15 个**（`install`/`marketplace`/`registry`/`search` 等 9.4 新增）——**以实测 15 为准**，13 是旧稿残留
- ⚠ **本机 236 skills / 69 plugins 均为 2026-09-27 快照**：skills 会随新增漂移（`ls | wc -l` 本机返回 238，含 2 个非目录文件，纯 skill 目录 236）；plugins 同理
- ⚠ **本机版本落后**：本机 2026.9.4 < 上游 2026.9.6 latest；plugin 字段/子命令若有 9.4/9.6 差异，本 SOP 以 9.4 为准

### 附录 A · plugin 生命周期 7 阶段 1-pager

```
┌───────────────────────────────────────────────────────────────────────┐
│  OpenClaw plugin 七阶段生命周期 · v5.0 industry-standard               │
├──────┬───────────┬──────────────────────┬──────────────────────────────┤
│ 阶段 │ 命令      │ 关键 JSON5 字段       │ 持久化位置                    │
├──────┼───────────┼──────────────────────┼──────────────────────────────┤
│ 0 概念│ （手写 RFC）│ —                   │ OpenClaw-官方RFC-草案.md      │
│ 1 脚手架│ plugins init│ id/name/categories  │ ~/.openclaw/extensions/<id>/ │
│ 2 构建│ plugins build│ openclaw.install   │ 同上（覆盖写入）              │
│ 3 打包│ plugins pack│ SHA256+activation  │ ./<id>.tgz                   │
│ 4 安装│ plugins install│ plugins.installs│ ~/.openclaw/extensions/<id>/ │
│ 5 运行时│ plugins enable│ activation.*   │ openclaw.json#entries.enabled│
│ 6 治理│ doctor/list/inspect│ allow/deny│ openclaw.json#plugins.*      │
├──────┴───────────┴──────────────────────┴──────────────────────────────┤
│ ⚠ 关键 trap：阶段 4（install）≠ 阶段 5（enable）——install 不自动 enable │
│ 本机实测：plugins --help = 15 子命令 · plugins list = 51/69 enabled    │
└───────────────────────────────────────────────────────────────────────┘
```

### 附录 B · 术语速查（v1.0 黑话 vs v3.0 真名）

| v1.0 黑话（内部保留） | v3.0 真名（对外 + 工程接口必用） | 英文 alias |
|---|---|---|
| 军团 | 多智能体编排 | Multi-Agent Orchestration / Agent Fleet |
| 监军 | 监督层 | Supervisor Layer |
| 三证验真 | 三证据验证 | Three-Evidence Verification (TEV) |
| 信誉分 / 军功簿 | 信任评分 / 功绩账本 | Trust Score / Merit Ledger |
| 三省制 | 三省评审制 | Three-Stage Review: Proposal / Review / Final-Decision |
| 让位协议 | 响应让渡协议 | Response Yield Protocol |
| 自主目标生成 | 自主目标生成 | Autonomous Goal Generation (Response → Proposal) |
| reserveTokensFloor | ❌ 不存在；真名 `CompactionRequestBudget.reserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25` | — |

→ 完整 35 条见 [`00-术语对照表·v3.0行业标准版.md`](../../00-术语对照表·v3.0行业标准版.md)

### 附录 C · 接口层收官跳转拓扑

```
09-mcp-binding/08-MCP绑定.md        (接口层 1/4 · 工具层 · MCP)
  ↓
10-a2a-binding/09-A2A绑定.md        (接口层 2/4 · 协议层 · A2A)
  ↓
11-skill-registry/README.md         (接口层 3/4 · 能力层 · Agent Skills)
  ↓
12-plugin-entrypoint/README.md      (接口层 4/4 · 分发层 · Plugin · 本章)
  ├── openclaw.plugin.json          (JSON5 manifest 模板)
  ├── install-指南.md               (5 阶段 install)
  ├── 配置项.md                     (13 子命令 flags)
  ├── 8卷挂载映射.md                (8 卷 → plugin 挂载)
  ├── OpenClaw-官方RFC-草案.md       (RFC SLT-001)
  └── 真名验证与勘误.md              (7 误植 + 8 真名)
```

### 附录 D · FAQ 速查（本章最常被问的 8 个问题）

| # | 问题 | 简短答案 | 详细位置 |
|---|---|---|---|
| 1 | 命令是 `plugin` 还是 `plugins`？ | **`plugins`（plural）** | 本章 12.2 |
| 2 | 配置文件叫什么？ | **`openclaw.plugin.json`（JSON5）**，不是 `manifest.yaml` | 本章 12.2 / 12.5 |
| 3 | 装完就用了吗？ | **不**，`install` ≠ `enable`；要再跑 `plugins enable` | 本章 12.4 trap |
| 4 | plugin 装在哪？ | `~/.openclaw/extensions/`（非 workspace/plugins/） | 本章 12.2 表 #4 |
| 5 | 配置入口在哪？ | `~/.openclaw/openclaw.json`（JSON5） | 本章 12.2 表 #5 |
| 6 | 本机多少 plugin？ | 69 个，51 已启用 | `openclaw plugins list` |
| 7 | ClawHub 怎么发布？ | 独立 CLI：`npm i -g clawhub` → `clawhub login` → `package publish` | 本章 12.6 |
| 8 | 本机版本？ | OpenClaw 2026.9.4 (3a9d69d) | `openclaw --version` |

---

# 第 12 章 · Plugin 入口：把硅基生命训练学装进 OpenClaw

> **v5.0 行业标准版 banner**：本章对应 OpenClaw 训练学第 12 章（**工程接口层** · 4 接口层之 4/4）；详见 [README](../../README.md)。
> **License banner**：MIT（基于 OpenClaw 主仓 LICENSE 法律文本，blob sha `ebaebf7c416761a32f932ad70ebe5d1d2e214f68`，SHA256 `73571b25…3a1c29d`；GitHub 显示 NOASSERTION 不影响法律效力，详见 [License 尽调报告](../../../license-due-diligence-report.md) Part 2）。
> **OpenClaw 真名**：本机 `openclaw --version` → **`OpenClaw 2026.9.4 (3a9d69d)`**；`openclaw plugins`（**plural**）子命令清单 = `build / disable / doctor / enable / init / inspect / install / list / marketplace / pack / registry / search / uninstall / update / validate`（15 个，实测 2026-09-27）。
> **业界对位**：本章对位 **OpenClaw plugin 生态（⚡领先）** / **ClawHub 公共注册中心（⚡领先）** / **Claude Agent SDK skills（●重叠 70%+）** / **LangGraph extensions（⚠部分重叠）** / **OpenAI Agents SDK handoffs（⚠部分重叠）** / **LlamaIndex agent tools（○互补）**——**业界无"插件化训练学底座"概念**。

---

## 12.10 诚实边界

> **验收项 6 · 主编死命令**：每章末尾必须含诚实边界声明。

```yaml
# 12.10 诚实边界
已用:
  - 本机 openclaw --version = OpenClaw 2026.9.4 (3a9d69d)    # 2026-09-27 实拉
  - 本机 openclaw plugins --help = 15 个子命令完整清单        # 2026-09-27 实拉
  - 本机 /opt/homebrew/lib/node_modules/openclaw/extensions/ 27 个 stock plugin JSON5 实读 # 2026-09-27
  - 本机 openclaw plugins list 输出 = 69 plugin / 51 enabled    # 2026-09-27
  - 本机 openclaw plugins doctor 输出 = "discovery, module loading, compatibility, and configuration checks passed" # 2026-09-27

待推:
  - ⏳ 本章涉及的 OpenClaw plugin 新字段 `policy.proactiveness` 尚未在 2026.9.4 实测；待 RFC 提交后等 OpenClaw 主仓合并
  - ⏳ `contracts.hooks` 字段在 2026.9.4 stock plugin manifest 中尚未出现；本节声明的 hook 列表基于 docs.openclaw.ai/plugins/building-plugins 设计文档推断，**未实测**
  - ⏳ ClawHub publish 后用户安装路径（`openclaw plugins install clawhub:silicon-life-training`）**未在本机实际跑过**（账号 < 1 周不满足 clawhub 反 PAM 约束）

未实测:
  - ⚠ 本章未实际跑通完整 5 阶段生命周期（init → build → pack → validate → install），仅跑了 plugins list / plugins doctor / plugins --help
  - ⚠ 本章未实际跑 `openclaw plugins install` 流程；尚未在公司内测账号上跑通
  - ⚠ ClawHub publish 的 `--family code-plugin` vs `--family skill` 差异未实测；本节描述基于 docs.openclaw.ai/clawhub/quickstart 文档推断
```

---

## 常见错误

> **本节用法**：第 12 章是接口层的收官（4/4）——Plugin 入口：把前 11 章的全部训练学资产打包成 `openclaw.plugin.json`（**JSON5**）可安装、可版本化、可灰度的分发单元。
> 这里的 8 个错误来自一条根因：**把"工程习惯"当"本系统真名"**——写 `manifest.yaml`、敲 `openclaw plugin`、去 `workspace/plugins/` 找文件。
> 术语首次出现双写：Supervisor Layer（原：监军）/ 多智能体编排（原：军团编制）/ Mentor Agent（原：教练虾）/ Drift Governance（漂移治理）/ Autonomy Boundary Triad（三档制）/ TEV（三证据验证，原：三证验真）/ Remediation Ticket（修复工单，原：整改单）/ Workspace Connector / 任务交接协议 THP / 多智能体协作 / 多智能体协同 / 智能体实例 / 智能体编排。
>
> **实测环境**：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27 · macOS 26.5.1 · `openclaw plugins --help` = **15 子命令** · `openclaw plugins list` = **51/69 enabled**。

### 错误 1 · 写 `manifest.yaml`（真名是 `openclaw.plugin.json` · JSON5）

**错误现象**：新人按"现代插件系统都用 YAML"的直觉，建了个 `manifest.yaml`，写完 `name` / `version` / `entry`，然后 `openclaw plugins validate` 报"找不到 manifest"。

**错误配置**（❌ 不要这样）：

```yaml
# manifest.yaml                       ❌ 真名不是这个，格式也不是 YAML
name: silicon-life-training
version: 2026.9.4
entry: index.js
```

**为什么错**：

1. **真名：`openclaw.plugin.json`**，格式 **JSON5**（允许注释 + trailing comma）。这是本章最大的一个易错点，也是 12.2 真名速查表 #2 的第一条。
2. **别把 `manifest` 当源文件**。`manifest` 是 `openclaw plugins build` 的**生成产物**，不是你要手写的源文件——手写 manifest 等于手写编译输出。
3. **JSON5 不是 JSON**：它**接受**注释与尾逗号，所以"用 `jq` 校验"会失败（`jq` 是 strict JSON）；要用 JSON5 解析器（`python3 -c "import json5"` 或 node 侧）。
4. **本机 27 个 stock plugin 全部用 `openclaw.plugin.json`**（`真名验证与勘误.md` 有 4 个实证样本：memory-lancedb / feishu+lobster+open-prose / device-pair / open-prose）——空 schema、1 字段、含 skill 字段等各种形态都是 JSON5。
5. **代价**：文件名错 = 一行都跑不起来；格式错 = 无法解析；两者都在"生命周期第 0 阶段"就断掉。

**正确配置**（✅ 应该这样）：

```json5
// ~/.openclaw/workspace/silicon-life-training/openclaw.plugin.json
{
  "name": "silicon-life-training",      // JSON5 允许 // 注释
  "version": "2026.9.4",
  "entry": "index.js",
  "skills": [ /* 可内联 skill 引用（stock open-prose 实证） */ ],
  "config": {
    "type": "object",
    "additionalProperties": false,       // 显式拒绝未知键（推荐）
  },                                     // ← trailing comma 合法
}
```

**验证命令**：

```bash
P=~/.openclaw/workspace/silicon-life-training/openclaw.plugin.json

# 1) 文件名真身
ls -l "$P"     # 必须叫 openclaw.plugin.json

# 2) JSON5 可解析（注意：不能只用 jq）
python3 -c "import json5;json5.load(open('$P'));print('✓ JSON5 解析通过')" \
  || node -e "const fs=require('fs');const j=require('json5');j.parse(fs.readFileSync('$P','utf8'));console.log('✓ JSON5 via node')"

# 3) CLI 校验（生命周期阶段之一）
openclaw plugins validate 2>&1 | head -20

# 4) 反例检测：不该存在 manifest.yaml
ls ~/.openclaw/workspace/silicon-life-training/*.yaml 2>/dev/null || echo "✓ 无 manifest.yaml"
```

**相关 FAQ**：F12-2（配置文件叫什么）、F12-4（plugin 装在哪）。相关文件：`openclaw.plugin.json`（180 行模板）。

---

### 错误 2 · 敲 `openclaw plugin`（singular）

**错误现象**：`openclaw plugin list` / `openclaw plugin install ./x` → command not found → 结论"这台机器没有 plugin 子系统"。

**错误配置**（❌ 不要这样）：

```bash
openclaw plugin list            # ❌ singular
openclaw plugin enable a2a      # ❌ singular
```

**为什么错**：

1. **真名是 `openclaw plugins`（plural）**，命令族 **15 个子命令**：build / disable / doctor / enable / init / inspect / install / list / marketplace / pack / registry / search / uninstall / update / validate。
2. **`plugin` 这个 singular 形式在本机是空壳**：`openclaw plugin --help` 能打出一行 usage 指向 `plugins`，但对新人来说"没报错也没输出"极易被读成"没这功能"。
3. **一次 typo 足以否定整章**：本章的全部实操都挂在 `plugins` 命令族上；拼错就等于整章不可执行。
4. **和第 11 章的 `plugins install` 勘误同源**（勘误 #1）：singular/plural 是这套 CLI 最容易踩的一处。
5. **正确习惯**：任何"命令不存在"的结论，必须附 `openclaw <group> --help` 的输出；没有输出就不算证据。

**正确配置**（✅ 应该这样）：

```bash
# 拉命令族再选
openclaw plugins --help 2>&1 | sed -n '/Commands:/,/^$/p'

openclaw plugins list
openclaw plugins init <name>
openclaw plugins validate
openclaw plugins doctor
openclaw plugins enable <id>
```

**验证命令**：

```bash
# 1) 子命令总数（15）
openclaw plugins --help 2>&1 | sed -n '/Commands:/,/^$/p' | grep -cE "^\s+[a-z]"
# 期望：≥ 14

# 2) 15 子命令逐条可见
openclaw plugins --help 2>&1 | sed -n '/Commands:/,/^$/p'

# 3) 现状基线
openclaw plugins list 2>&1 | head -1
# 期望：Plugins (51/69 enabled)

# 4) 反例
type openclaw >/dev/null && openclaw plugin --help 2>&1 | head -3
```

**相关 FAQ**：F12-1（plugin 还是 plugins）。

---

### 错误 3 · `install` 之后就以为能用（忘了 `enable`）

**错误现象**：`openclaw plugins install ./silicon-life-training` 成功，`plugins list` 里能看到它，但 agent 里没任何变化。用户以为"装好了"。

**错误配置**（❌ 不要这样）：

```bash
openclaw plugins install ./silicon-life-training
openclaw plugins list | grep silicon-life        # 看到了
echo "✅ 已安装并生效"                             # ❌ 没 enable
```

**为什么错**：

1. **`install` ≠ `enable`**（12.4 的 trap）。install 只做两件事：复制文件 + 注册 `plugins.installs`；**enable 才在 `plugins.entries.<id>.enabled` 置 true**，进运行时。
2. **"列表里看到"是库存事实**：`plugins list` 会列出 disabled 的 plugin（本机 69 个里 18 个是 disabled，包括 `stock:a2a`）。
3. **这是全章最典型的假完成**：命令退出码 0、无报错、有输出——三条"成功信号"全齐，但功能没生效。
4. **和 TEV 的对应关系**：证据 1（产物：装了）有、证据 2（Diff：`plugins.installs` 变了）有、**证据 3（运行日志：真的加载了）没有**。
5. **正确验收是三步：install → enable → 验证运行时**（`agent --message` 触发一次或看 doctor）。

**正确配置**（✅ 应该这样）：

```bash
# 1) 装
openclaw plugins install ./silicon-life-training

# 2) 启用（关键的一步）
openclaw plugins enable silicon-life-training

# 3) 验证运行时 + 落日志
openclaw plugins list 2>&1 | grep -i silicon-life     # 状态应为 enabled
openclaw plugins doctor
openclaw agent --message "ping" --agent my-agent      # 触发一次，看加载记录
```

**验证命令**：

```bash
# 1) 三态分离：库存 / 安装记录 / 启用项
openclaw plugins list 2>&1 | grep -i silicon-life
openclaw plugins inspect silicon-life-training 2>&1 | head -30

# 2) 启用总数基线（51/69）
openclaw plugins list 2>&1 | head -1

# 3) 体检
openclaw plugins doctor

# 4) 破坏性操作前
openclaw backup create
```

**相关 FAQ**：F12-3（装完就用了吗）、F12-6（本机多少 plugin）。

---

### 错误 4 · 去 `~/.openclaw/workspace/plugins/` 找安装目录

**错误现象**：新人装完 plugin 想去看看文件，`ls ~/.openclaw/workspace/plugins/` → No such file or directory。于是判断"根本没装成功"，重装、换命令、查权限。

**错误配置**（❌ 不要这样）：

```bash
ls ~/.openclaw/workspace/plugins/      # ❌ 无此目录
find ~/.openclaw/workspace -name "*.plugin*" | head
```

**为什么错**：

1. **真名：安装目录 = `~/.openclaw/extensions/`**（12.2 表 #4）。workspace 里放的是你的**源工程**（skill / 文档 / agent 草案），**extensions 里放的是安装后的 plugin**。
2. **两个目录职责不同**：workspace = 作者面（你写的），extensions = 运行面（装进的）。找错地方就会得出"没装成功"的错误结论。
3. **本机已安装 plugin 列表可实证**（`真名验证与勘误.md` §4.3）：`ls ~/.openclaw/extensions/` 能看到实际落地的 plugin。
4. **上游 source 与下游 install 是两回事**：你从 `./silicon-life-training` 装，不等于那个源目录会出现在 extensions 里——只有产物会被复制过去。
5. **代价**：浪费排查时间 + 可能误删源目录（以为"重复了"）。

**正确配置**（✅ 应该这样）：

```bash
# 源工程（你写的）
ls ~/.openclaw/workspace/silicon-life-training/

# 安装产物（运行时读的）
ls ~/.openclaw/extensions/

# 本机已装清单（权威）
openclaw plugins list
```

**验证命令**：

```bash
# 1) 真名目录
ls -la ~/.openclaw/extensions/ 2>&1 | head -20

# 2) 反例目录
ls ~/.openclaw/workspace/plugins/ 2>&1 | head -3
# 期望：No such file or directory（这才是"正确"的失败）

# 3) 交叉核对：extensions 里的条目能对上 plugins list
ls ~/.openclaw/extensions/ | wc -l
openclaw plugins list 2>&1 | head -1

# 4) 上游 source 存在
ls ~/.openclaw/workspace/silicon-life-training/openclaw.plugin.json
```

**相关 FAQ**：F12-4（装在哪）。相关文件：`真名验证与勘误.md` §4。

---

### 错误 5 · 去改 `config.yaml` / 用 `openclaw config set` 改 JSON5（丢注释）

**错误现象**：新人想改 plugin 配置，去找 `~/.openclaw/config.yaml`（不存在），或者对已存在的 JSON5 主配置跑 `openclaw config set plugins.entries.x.enabled true`——配置能写进去，但**原有注释被无声丢弃**。

**错误配置**（❌ 不要这样）：

```bash
ls ~/.openclaw/config.yaml                # ❌ 无此文件
openclaw config set plugins.entries.silicon-life.enabled true
# ⚠ 该命令会把 JSON5 改写成标准 JSON，无声丢弃注释
```

**为什么错**：

1. **真名：主配置 = `~/.openclaw/openclaw.json`（JSON5）**（12.2 表 #5；本机已存在，实测 45 445 bytes）。
2. **`config set` 会规范化输出**：docs.openclaw.ai/cli/config 明确警告——它改写成标准 JSON，**静默丢弃注释**。你的 hand-written 注释（尤其是解释某字段为什么这么配的注释）会一次性消失。
3. **注释不是装饰**：本项目的配置里大量注释承担"为什么这么配"的说明；丢掉等于丢掉决策记录（这也是 Drift Governance 要看的东西）。
4. **正确姿势是手编 + `config patch`**：用编辑器改 JSON5 保住注释，或用 `config patch` 做定点修改。
5. **误改还有一层风险**：`openclaw.json` 是**主配置真身**，改坏影响全部 18 个 agent——改前必须 `openclaw backup create`。

**正确配置**（✅ 应该这样）：

```bash
# 1) 改前备份（强制）
openclaw backup create

# 2) 手编（保住注释）
$EDITOR ~/.openclaw/openclaw.json
#   plugins: {
#     entries: {
#       "silicon-life-training": {
#         enabled: true,          // ← 注释保留
#       },
#     },
#   }

# 3) 定点改（不重写全文）
openclaw config patch ... 2>&1 | head -5    # 具体 flag 以 --help 为准

# 4) 校验
openclaw doctor
openclaw config get plugins.entries 2>&1 | head -20
```

**验证命令**：

```bash
# 1) 主配置真身
ls -l ~/.openclaw/openclaw.json
grep -c "//" ~/.openclaw/openclaw.json     # 注释计数（config set 后会变 0）

# 2) 反例
ls ~/.openclaw/config.yaml 2>&1 | head -2  # 期望：No such file

# 3) 体检 + 备份
openclaw doctor
openclaw backup create
```

**相关 FAQ**：F12-5（配置入口在哪）。

---

### 错误 6 · 直接 `install` 未 build / pack / validate 的源工程

**错误现象**：新人改完源码，直接 `openclaw plugins install ./silicon-life-training`，装进去的是**上一次**的旧产物（或半成品），然后纳闷"我的改动怎么没生效"。

**错误配置**（❌ 不要这样）：

```bash
# 改完源码直接装
vim index.js
openclaw plugins install ./silicon-life-training     # ❌ 未 build/pack/validate
```

**为什么错**：

1. **生命周期是有序的**：`init → build → pack → validate → install → enable → doctor`。跳过中间三步，install 拿到的要么是旧产物，要么是不合法的产物。
2. **`manifest` 是 build 的产物**：不跑 build 就没有最新 manifest；不跑 pack 就没有最新 artifact。
3. **validate 是唯一的静态合规闸门**：跳过它，schema 错、字段错会一直带到运行时才炸（且报错信息往往指向别处）。
4. **本机诚实边界已声明**：本章**未实际跑通完整 5 阶段生命周期**（只跑了 `plugins list` / `plugins doctor` / `plugins --help`）——所以更不能把"直接 install"当"已验证路径"。
5. **代价**：调试时你在追一个"不是你写的代码"的 bug。

**正确配置**（✅ 应该这样）：

```bash
# 本地闭环四步（顺序固定）
openclaw plugins init silicon-life-training          # 阶段 0（脚手架）
openclaw plugins build                               # 阶段 1（生成 metadata/manifest）
openclaw plugins pack                                # 阶段 2（生产 artifact）
openclaw plugins validate                            # 阶段 2.5（静态合规闸门）
openclaw plugins install ./silicon-life-training     # 阶段 3（本地试装）
openclaw plugins enable silicon-life-training        # 阶段 4（进运行时）
openclaw plugins doctor                              # 阶段 5（体检）
```

**验证命令**：

```bash
# 1) 逐阶段留证据（TEV 三证据）
openclaw plugins build  2>&1 | tee ~/notes/domain/silicon-life-handbook/evidence/plug-build.log
openclaw plugins pack   2>&1 | tee ~/notes/domain/silicon-life-handbook/evidence/plug-pack.log
openclaw plugins validate 2>&1 | tee ~/notes/domain/silicon-life-handbook/evidence/plug-validate.log

# 2) 产物时间戳（确认装的是最新）
ls -lt ~/.openclaw/workspace/silicon-life-training/ | head
ls -lt ~/.openclaw/extensions/ | head

# 3) 体检
openclaw plugins doctor
```

**相关 FAQ**：F12-7（ClawHub 怎么发布）。相关文件：`install-指南.md`（5 阶段）。

---

### 错误 7 · 把 Plugin 当 Skill（范围混淆 + 越权字段）

**错误现象**：把只有 `SKILL.md` 的目录当 plugin 装；或者反过来，在 plugin 里只放一个 `SKILL.md`，期望它像 skill 那样被 32+ 客户端读到。

**错误配置**（❌ 不要这样）：

```text
# 把纯 skill 目录当 plugin
silicon-life-drift/
└── SKILL.md                # ❌ 没有 openclaw.plugin.json，install 会失败
```

**为什么错**：

1. **范围真名**：Plugin = **1 个或多个 skill + `openclaw.plugin.json` 清单 + native Control UI 资源**；Skill = 1 个 `SKILL.md` + 可选 scripts/references/assets。
2. **加载方式真名**：Plugin **启动时加载**（`openclaw plugins enable`）；Skill **渐进式披露**（agent 按需读）。两者是不同生命周期。
3. **跨平台真名**：Plugin **仅 OpenClaw runtime**；Skill 任何读 `SKILL.md` 的 agent 都能用。混用等于主动放弃跨平台性。
4. **License 归属不同**：Skill 自带 `license:` 字段；Plugin 跟随 plugin（默认 MIT）。
5. **一句话**：**Skill = 剧本（Markdown · 自然语言 · 跨平台）；Plugin = 剧组（JSON5 + Code · 启动时加载 · OpenClaw 私有）**。要"能自动跑"才升级为 plugin。

**正确配置**（✅ 应该这样）：

```text
# 正确：plugin 里包 skill（stock open-prose 实证：manifest 含 skill 字段）
silicon-life-training/
├── openclaw.plugin.json     # ✅ 必需清单（JSON5）
├── index.js                 # ✅ 进程入口
├── skills/
│   └── drift-audit/
│       └── SKILL.md         # ✅ skill 作为 plugin 的资源之一
└── package.json
```

**验证命令**：

```bash
# 1) manifest 必需字段在
python3 -c "import json5;d=json5.load(open('$HOME/.openclaw/workspace/silicon-life-training/openclaw.plugin.json'));print(sorted(d.keys()))"

# 2) skill 引用可解析
ls ~/.openclaw/workspace/silicon-life-training/skills/*/SKILL.md

# 3) 边界对照（第 11 章 11.7 表）
sed -n '/边界澄清/,/详见第 12 章/p' ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/chapters/10-skill-registry/README.md
```

**相关 FAQ**：F11-6 / F12-2。相关章节：第 11 章 11.7。

---

### 错误 8 · 未本地验证就 `clawhub publish`（反 PAM 约束 + 不可回滚）

**错误现象**：新人在本地只跑过 `plugins list`，就直接 `clawhub package publish` 发布到公共注册中心，版本号 `1.0.0`。

**错误配置**（❌ 不要这样）：

```bash
npm i -g clawhub
clawhub login
clawhub package publish --family code-plugin     # ❌ 本地未 install/enable/validate
```

**为什么错**：

1. **发布是不可逆的公共动作**：ClawHub 是中心化注册中心，一旦发布，版本号就被占用、拉取方就开始依赖；本地连 `install + enable` 都没跑通，等于把未验证产物推向公共。
2. **有前置约束**：docs 明确写了 clawhub 的**反 PAM（publication anti-abuse）约束**——本机诚实边界已标：*"账号 < 1 周不满足 clawhub 反 PAM 约束"*，且 `clawhub:silicon-life-training` 的安装路径**未在本机跑过**。
3. **`--family code-plugin` vs `--family skill` 差异未实测**：两种 family 对应的产物形态不同，选错会导致拉取方装不上。
4. **发布前必须先在本地跑通"用户视角"**：`openclaw plugins install <source>` → `enable` → `doctor` → `agent --message` 触发一次。
5. **代价**：公共包发布错误 = 面向全世界的错误；事后只能发新版本修正（旧版本仍可被拉到）。

**正确配置**（✅ 应该这样）：

```bash
# 1) 本地先把"用户路径"跑通（install 六种源之一）
openclaw plugins install ./silicon-life-training
openclaw plugins enable silicon-life-training
openclaw plugins doctor
openclaw agent --message "ping" --agent my-agent

# 2) 静态合规
openclaw plugins validate

# 3) 打包
openclaw plugins pack

# 4) 最后才发布（且 family 需实测确认）
# npm i -g clawhub && clawhub login
# clawhub package publish --family code-plugin   # ⏳ 本机未实测
```

**验证命令**：

```bash
# 1) 本地闭环证据链
{ openclaw plugins validate; openclaw plugins doctor; \
  openclaw plugins list | head -1; } \
  | tee ~/notes/domain/silicon-life-handbook/evidence/plug-preflight.log

# 2) 备份（发布/升级前）
openclaw backup create

# 3) 版本号与底座一致
python3 -c "import json5;print(json5.load(open('$HOME/.openclaw/workspace/silicon-life-training/openclaw.plugin.json'))['version'])"
openclaw --version 2>&1 | tail -1
```

**相关 FAQ**：F12-7（ClawHub 怎么发布）。相关文件：`install-指南.md` 阶段 4/5。

---

## 新手坑

> **本节用法**：本章 5 个坑的共同特征是"**信直觉不信真名**"——插件系统在别处怎么做，这里就怎么写。
> 实测环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27 · plugins 51/69 enabled · 安装目录 `~/.openclaw/extensions/`。

### 坑 1 · 先 publish，再本地装（顺序反了）

**坑的场景**：新人觉得"发布到 ClawHub 才是本章的高光时刻"，于是第一天就把脚手架推上 ClawHub，第二天才开始本地 `install` 试装，然后发现 manifest 字段错、entry 路径错。

**后果**：公共注册中心里躺着一个装不上的版本；版本号被占用（`0.1.0`、`1.0.0` 都发过了），后续只能跳号发 `1.0.1`；如果别人已经拉了你的包，你还要背一次"错误分发"的账。

**为什么踩**：

- **本章 12.6 是"ClawHub publish 实战 5 步"**，编号在前、看起来是"主线任务"。
- **发布的反馈是即时的**（一条命令、一个 URL），本地闭环的反馈是延迟的（要先 build/pack/validate/install/enable）。
- **"先发再说"的迭代习惯**——在 npm 上风险可控，在注册中心里是公开资产。

**怎么爬出来**：

```bash
# 1) 承认已发布，先补本地闭环
openclaw plugins validate && openclaw plugins doctor

# 2) 本地装 + 启用 + 触发一次
openclaw plugins install ./silicon-life-training
openclaw plugins enable silicon-life-training
openclaw agent --message "ping" --agent my-agent

# 3) 修完发 patch 版本（不要重发同版本号）
#    openclaw.plugin.json: "version": "2026.9.5"
```

**预防**：把顺序写成硬规——**validate → install → enable → doctor → 触发一次 → 才允许 publish**。

---

### 坑 2 · 把 stock plugin 当社区 plugin（来源混淆）

**坑的场景**：`openclaw plugins list` 里有 69 条，新人以为"这 69 个都是社区贡献的"，于是在文档里写"本机已装 69 个社区插件"。或者反过来，把某个 stock plugin 当成"我们自己写的"。

**后果**：来源判定错 → 责任归属错 → 升级/排障方向错（stock 随发行版走，社区包要自己维护）；对外表述也会失真（"我们用了 69 个社区插件"是错的）。

**为什么踩**：

- **列表不区分来源在视觉上很明显，但列名要读**：本机列表里有 `stock:<name>/index.js` 这样的路径列——`stock:` 前缀就是来源标记。
- **"装了这么多"比"这些是随附的"更带感**。
- **69 这个数字太醒目**，让人忽略了 51/69 里的 enabled 分层。

**怎么爬出来**：

```bash
# 1) 看来源列（stock: 前缀）
openclaw plugins list 2>&1 | grep -c "stock:"
openclaw plugins list 2>&1 | grep -v "stock:" | head -20     # 非 stock = 社区/自装

# 2) 三态写清：总数 / enabled / 来源
openclaw plugins list 2>&1 | head -1        # Plugins (51/69 enabled)

# 3) 文档改写
# "本机 69 个 plugin（stock 为主），51 个 enabled，18 个 disabled（含 stock:a2a）"
```

**预防**：任何 plugin 数量结论必须带三件：**总数 / 启用数 / 来源（stock vs 社区）**。

---

### 坑 3 · 以为 disabled 就是"坏了"（去修不该修的）

**坑的场景**：新人看到 18 个 disabled，其中还有 `stock:a2a`，判定"系统有 18 个故障"，开始逐个 `enable`。enable 完发现没变化，或者引入了新的行为。

**后果**：把**设计上的默认关闭**当成故障。stock plugin 默认 disabled 是**刻意的**（避免一次性加载全部能力）；盲目 enable 会改变运行时行为、增加排障面，而且和第 9 章"以为 A2A 已启用"是同一个认知错误的两面。

**为什么踩**：

- **`disabled` 在直觉里 = "出错了"**，而不是"默认策略"。
- **本机 51/69 这个比例**看起来像"74% 成功率"，实则是"默认启用集合"。
- **"帮我把它全开起来"是最自然的优化冲动**。

**怎么爬出来**：

```bash
# 1) 先分类：stock 默认 disabled vs 自己 disable 的
openclaw plugins list 2>&1 | grep -i disabled | head -20

# 2) 只启用你真正需要的（且先备份）
openclaw backup create
# openclaw plugins enable <id>

# 3) 启用后立刻验证行为变化
openclaw plugins doctor
openclaw health
```

**预防**：写清"默认禁用是设计而非故障"；enable 任何 stock plugin 前先说明"为什么要开"。

---

### 坑 4 · 破坏性操作前不 `backup create`

**坑的场景**：新人改 `~/.openclaw/openclaw.json`、跑 `plugins uninstall`、enable 一批 plugin——全都直接跑，不做备份。出问题时配置已被改得面目全非。

**后果**：主配置是本机 18 个 agent 的共同底座；改坏一次，恢复成本远高于一次备份。JSON5 注释丢了更是不可逆（`config set` 丢弃的注释没有回收站）。

**为什么踩**：

- **备份感觉是"多余的一步"**，尤其当命令都成功了。
- **`openclaw backup create` 不在任何"必需命令"清单里**（它属于工程卫生，不是功能命令）。
- **失败的反馈是延迟的**——今天改的配置，明天某个 agent 行为异常才暴露。

**怎么爬出来**：

```bash
# 1) 立即补备份
openclaw backup create

# 2) 确认备份落盘
ls -lt ~/.openclaw/backups/ 2>/dev/null | head || find ~/.openclaw -maxdepth 2 -name "*backup*" | head

# 3) 之后每次破坏性操作前先跑
alias oc-safe='openclaw backup create && echo "✓ 备份完成"'
```

**预防**：把 `openclaw backup create` 写进所有破坏性步骤的前置条件（install / enable / uninstall / 改主配置 / 升级版本）。

---

### 坑 5 · 版本号与底座不一致 / 写死版本

**坑的场景**：`openclaw.plugin.json` 里 `version` 手写 `"1.0.0"`，或者写死 `"2026.3.2"`（旧版本号）；同时 Card / skill 里各写一个版本。三处对不上。

**后果**：用户按 manifest 版本判断兼容性 → 误判；升级时版本混乱；引用旧版本号还触犯术语表禁忌（#34：不得引用 OpenClaw `2026.3.2`）。

**为什么踩**：

- **plugin 的 version 与业务 version 的语义没区分**：manifest 的 `version` 应表达"产物版本"，与底座版本的关系应显式说明。
- **模板里的版本是上例留下的**，复制后忘了改。
- **三处（Card / skill / manifest）分散写，没有单一来源**。

**怎么爬出来**：

```bash
# 1) 三处版本对齐检查
M=~/.openclaw/workspace/silicon-life-training/openclaw.plugin.json
C=~/.openclaw/workspace/agents/roles/<agent>/a2a/agent-card.json
python3 - <<'PY'
import json5, json, os
m = json5.load(open(os.path.expanduser(M.replace('~','/Users/peterqiu')))) if False else None
PY
python3 -c "import json5;print('manifest:', json5.load(open('$M'))['version'])"
openclaw --version 2>&1 | tail -1

# 2) 反例：禁止旧版本号
grep -rn "2026.3.2" ~/.openclaw/workspace/silicon-life-training/ | head
# 期望：0

# 3) 单一来源：把版本写进一个文件，三处引用
echo "2026.9.4" > ~/.openclaw/workspace/silicon-life-training/VERSION
```

**预防**：版本号单一来源（`VERSION` 文件或 CI 注入）；任何位置禁止硬编码旧版本号。

---

### 坑 6 · 把 `51/69` 当成"质量分"（用数字判断健康）

**坑的场景**：新人看到 `openclaw plugins list` 输出 `Plugins (51/69 enabled)`，第一反应是"74% 的插件正常工作，18 个是故障"，于是在文档里写"本机插件健康度 74%"，并把 18 个 disabled 列进"待修复清单"。

**后果**：一个**默认配置事实**被读成**质量指标**，随后衍生出一串错误动作——

1. **误判健康度**：51/69 是"默认启用集合 / 随发行版落地的总数"，不是成功率。真正该看的健康信号是 `openclaw plugins doctor` 的输出。
2. **误开不该开的**：把 18 个逐个 enable，改变运行时行为（增加加载面、可能引入冲突），而收益为零。
3. **误写文档**：把"健康度 74%"写进对外材料，属于用数字制造虚假精确度——这正是第 5 章 TEV 要防的"看起来像证据的东西"。
4. **错失真信号**：真正的异常（`heartbeat:peter error 70x`、`kunlun heartbeat error 99+x` 这类**错误计数**）反而没人看，因为注意力被"74%"占走了。

**为什么踩**：

- **`a/b` 的视觉形态天生像"得分"**（像考试分数 51/69）。
- **分母 69 太大太醒目**：注意力被总量吸走，忽略了"enabled"这个词限定的是**策略**而非**结果**。
- **"多用一点总没坏处"的优化冲动**——对插件系统而言，多加载是有成本的。
- **没有"该看什么"的指引**：`plugins list` 的输出没有强调"这不是健康度"，`plugins doctor` 才是。

**怎么爬出来**：

```bash
# 1) 把"库存 / 策略 / 健康"三个数字分开理解
openclaw plugins list 2>&1 | head -1          # 策略视图：(51/69 enabled)
openclaw plugins doctor 2>&1 | tail -20       # 健康视图：唯一权威
openclaw health 2>&1 | head -20               # 运行时概览

# 2) disabled 不等于坏：看它在 stock 还是社区
openclaw plugins list 2>&1 | grep -i disabled | head -20

# 3) 真正该关注的异常信号（错误计数，不是比例）
grep -riE "error|fail" ~/.openclaw/logs/*.log 2>/dev/null | tail -20

# 4) 文档改写
#    ❌ "插件健康度 74%"
#    ✅ "本机 69 个 plugin（stock 为主），51 个默认启用；健康以 plugins doctor 结论为准"
```

**预防**：

- 在任何引用 `51/69` 的地方强制加一句限定：**"这是默认启用策略，不是健康度"**。
- 健康结论**只能**来自 `plugins doctor` / `openclaw health`，且要附命令输出与日期。
- 排查优先级排序：**错误计数 > doctor 告警 > 列表比例**。
- 一句话纪律：**比例不是证据，日志才是证据**（TEV 第 3 证）。

**相关 FAQ**：F12-6（本机多少 plugin）、F12-3（装完就用吗）。相关章节：第 5 章（TEV 三证据验证 / 治理审计账本）。

---

## 扩展阅读

> **本节用法**：本章是接口层收官（4/4 · 分发层），扩展阅读 = "业界插件/分发体系对位 + 本书内导航 + 一手核实命令"。
> 状态为 2026-09-27 实拉；未评测项标 ⏳。

### 业界对位

| 业界项目 | 对应内容 | 链接 | 差异 |
|---|---|---|---|
| OpenClaw plugin 生态 | 本章底座（15 子命令 + JSON5 manifest） | https://docs.openclaw.ai/plugins | ⚡ 领先：有"训练学外化"哲学 |
| ClawHub 公共注册中心 | 中心化分发（`clawhub package publish`） | https://docs.openclaw.ai/clawhub/quickstart | ⚡ 领先：业界无同类"训练学底座"注册中心 |
| Claude Agent SDK（⭐8,172） | skills 打包与分发 | https://github.com/anthropics/claude-agent-sdk-python | 分发弱；无中心注册中心 |
| OpenAI Agents SDK | Agent 打包 / handoff 封装 | https://github.com/openai/openai-agents-python | 无独立 manifest 规范 |
| LangGraph（LangChain ⭐147,151） | extensions / 集成包 | https://github.com/langchain-ai/langgraph | extensions 碎片化，无统一 manifest |
| LlamaIndex（⭐52,330） | 集成包体系 | https://github.com/run-llama/llama_index | 偏数据连接器，无生命周期 CLI |
| MCP Registry（第 8 章） | 注册中心对位 | — | ⏳ v0.1 仍 freeze；ClawHub 已可用 |

**关键结论**：业界普遍有"包管理"（pip / npm / extensions），**没有"plugin = 训练学外化 + 中心注册中心 + 7 阶段生命周期 CLI"的组合**——这是本章定位的"工程接口层收官"的确切含义。

> ⏳ 诚实边界：`openclaw plugins init/build/pack/validate/install` 的命令拼写已由 `--help` 确认，但**本机未跑通完整 5 阶段生命周期**；`clawhub publish` 未在本机执行（账号 < 1 周不满足反 PAM 约束）。

### 业界对位补充 · plugin 生命周期七阶段对照

| 阶段 | OpenClaw 真名 | 业界类比 | 本书要点 |
|---|---|---|---|
| 0 脚手架 | `plugins init` | `npm init` / `cookiecutter` | 生成 `openclaw.plugin.json` 骨架 |
| 1 构建 | `plugins build` | `tsc` / `vite build` | 生成 manifest（产物，非源文件） |
| 2 打包 | `plugins pack` | `npm pack` / `docker build` | 生产 artifact |
| 2.5 校验 | `plugins validate` | ESLint / schema check | 唯一静态合规闸门 |
| 3 试装 | `plugins install` | `npm i ./pkg` | 复制文件 + 注册 `plugins.installs` |
| 4 启用 | `plugins enable` | systemd `enable` | 置 `plugins.entries.<id>.enabled` |
| 5 体检 | `plugins doctor` | `brew doctor` | 运行时健康 |

### 本书内交叉引用

- **前一章**：第 11 章 · Skill 注册（接口层 3/4，能力层）→ `chapters/10-skill-registry/README.md`
- **上游**：第 8 章 · MCP 绑定（工具层）→ `chapters/08-mcp-binding/08-MCP绑定.md`；第 10 章 · A2A 绑定（协议层）→ `chapters/09-a2a-binding/09-A2A绑定.md`
- **本章 SOP**：`## SOP · 本章怎么用`（步骤 2 的三件事）+ `### 附录 A · plugin 生命周期 7 阶段 1-pager`
- **配套文件**：`openclaw.plugin.json`（JSON5 模板）/ `install-指南.md`（5 阶段命令）/ `配置项.md`（13 子命令 flags）/ `8卷挂载映射.md` / `OpenClaw-官方RFC-草案.md`（SLT-001）/ `真名验证与勘误.md`（7 项误植 + 8 项真名证据链）
- **全章收束**：第 0 章（5 差异化优势）→ 第 2 章（骨架）→ 第 6 章（协同）→ 第 7 章（提案）→ 第 8/10/11 章（接口）→ **本章（打包分发）**
- **相关 FAQ**：F12-1（singular/plural）、F12-2（manifest 真名）、F12-3（装完就用吗）、F12-4（装在哪）、F12-5（配置入口）、F12-6（本机多少）、F12-7（ClawHub 发布）、F12-8（本机版本）
- **术语底座**：`00-术语对照表·v3.0行业标准版.md`（#20 / #32 / #33 / #34 / #35）

### 延伸阅读补充 · 一手核实命令（本章）

```bash
# 版本 + 命令族
openclaw --version 2>&1 | tail -1
openclaw plugins --help 2>&1 | sed -n '/Commands:/,/^$/p'   # 15 子命令

# 现状基线
openclaw plugins list 2>&1 | head -1        # Plugins (51/69 enabled)
openclaw plugins list 2>&1 | grep -c "stock:"
openclaw plugins list 2>&1 | grep -i "a2a"  # stock:a2a = disabled

# manifest 真名 + JSON5 可解析
ls ~/.openclaw/workspace/silicon-life-training/openclaw.plugin.json
python3 -c "import json5;print('✓ JSON5 OK')"

# 安装目录真名（不是 workspace/plugins/）
ls -la ~/.openclaw/extensions/ | head -20

# 配置真名（JSON5，含注释）
ls -l ~/.openclaw/openclaw.json

# 体检 + 安全网
openclaw plugins doctor
openclaw health && openclaw doctor
openclaw backup create
```

### 延伸阅读补充 · 本章相关真实案例索引

| 案例 | 现象 | 对应 plugin 环节 | 相关章节 |
|---|---|---|---|
| 8/19 军团断线 | 通道在列表里但无人应答 | install ≠ enable（stock:a2a disabled） | 第 9 章 / F3-13 |
| 能力矩阵 26 天未续期 | 声明在但行为不在 | manifest/Card 声明与运行不一致 | 第 5 章 / F7-15 |
| 18 坏 skill | 加载失败污染上下文 | validate 跳过 → 运行时才炸 | 第 11 章 / F5-10 |
| 9/21 飞书推送事故 | 定时任务静默失败 | 发布前未跑本地闭环 | 第 6 章 / F3-12 |

### 延伸阅读补充 · 7 项高频误植速查（对照 `真名验证与勘误.md`）

| # | 误植（❌） | 真名（✅） | 证据来源 |
|---|---|---|---|
| 1 | `openclaw plugin`（singular） | `openclaw plugins`（plural） | `plugins --help` |
| 2 | `manifest.yaml` | `openclaw.plugin.json`（JSON5） | 27 个 stock plugin 实证 |
| 3 | `manifest` 是源文件 | `manifest` 是 `build` 产物 | 官方 docs |
| 4 | `~/.openclaw/workspace/plugins/` | `~/.openclaw/extensions/` | 本机 `ls` 实证 |
| 5 | `~/.openclaw/config.yaml` | `~/.openclaw/openclaw.json`（JSON5） | 本机 45 445 bytes 实测 |
| 6 | `openclaw plugin install` 不存在 | `plugins install` 存在（6 种源） | `plugins --help` |
| 7 | "装了 = 生效" | `install` ≠ `enable` | 12.4 trap |

### 延伸阅读补充 · 引用禁忌（本章专属）

- 不得写 `manifest.yaml`（须 `openclaw.plugin.json` · JSON5）
- 不得写 `openclaw plugin`（须 `plugins`）
- 不得把安装目录写成 `workspace/plugins/`（须 `~/.openclaw/extensions/`）
- 不得把配置入口写成 `config.yaml`（须 `~/.openclaw/openclaw.json` · JSON5）
- 不得用 `openclaw config set` 改带注释的 JSON5（会无声丢注释）
- 不得在未跑本地闭环的情况下 `clawhub publish`
- 不得引用 OpenClaw `2026.3.2`（术语表 #34）
- 不得宣称"完整 5 阶段生命周期已跑通"（本机未实测）

### 一句话收尾

第 12 章可以浓缩成一句口诀：**"`plugins` 复数、`openclaw.plugin.json` 是 JSON5、装完还要 enable、目录在 extensions、先 validate 再 publish、动手前 backup"**——分发层的价值不在"能打包"，而在"打出来的包，别人装得上、用得起、出问题查得到"。

---

*第 12 章（12-plugin-entrypoint）P1-2 追加区块 · 常见错误 8 个 / 新手坑 5 个 / 扩展阅读 6 部分*
*撰写：从零撰写（未抄 v1.0/v4.0 原文）· 2026-09-27*
*实测环境：OpenClaw 2026.9.4 (3a9d69d) · macOS 26.5.1 · plugins 51/69 enabled · 15 子命令实测*

---

### 延伸阅读补充 · 全章真名命令速查（含本章新增 · 逐条可执行）

```bash
# —— 环境 / 实例层（本章前置底座）——
openclaw setup                       # 首次环境初始化（真名 · 交互式）
openclaw agents add <name>           # 新增智能体实例（真名）
openclaw agents list                 # 本机 18 个 agent（实测基线）
openclaw health                      # 运行时健康
openclaw doctor                      # 配置 / 依赖体检
openclaw backup create               # 破坏性操作前的安全网（每次改配置前必跑）

# —— 本层（Plugin 入口 · plugins 复数 15 子命令）——
openclaw plugins --help              # 命令族全清单
openclaw plugins init <name>         # 阶段 0 · 脚手架
openclaw plugins build               # 阶段 1 · 生成 manifest（产物，非源文件）
openclaw plugins pack                # 阶段 2 · artifact
openclaw plugins validate            # 阶段 2.5 · 唯一静态合规闸门
openclaw plugins install <source>    # 阶段 3 · 复制 + 注册 plugins.installs
openclaw plugins enable <id>         # 阶段 4 · 置 entries.<id>.enabled（关键一步）
openclaw plugins doctor              # 阶段 5 · 体检
openclaw plugins list                # Plugins (51/69 enabled)
openclaw plugins inspect <id>        # 单插件详情
python3 -c "import json5;json5.load(open('<plugin>/openclaw.plugin.json'));print('✓ JSON5 OK')"
ls -la ~/.openclaw/extensions/       # 安装目录真名（不是 workspace/plugins/）
ls -l ~/.openclaw/openclaw.json      # 主配置真名（JSON5 · 注释敏感）

# —— 跨层对照（第 8/10/11 章真名）——
openclaw mcp list                    # mcp.servers 基线
openclaw skills list                 # 236 skill 目录
openclaw agent --message "ping" --agent <name>   # 装完触发一次
```

> ⏳ 标注说明：`init/build/pack/validate/install/enable/doctor` 拼写均由 `plugins --help` 确认为真名，但**本机未跑通完整 5 阶段生命周期**；`clawhub package publish` 未执行（反 PAM 约束）。接力者按"validate → install → enable → doctor → 触发一次 → 才 publish"顺序补测。

---

## 本章业界对位（详见 ./_industry-frontier-tracking.md §2.11）

## 本章前沿追踪（详见 ./_industry-frontier-tracking.md §3.3、§3.9）

## 附录索引

> 本章涉及的 cookbook / FAQ / SOP / case-library / api-reference **编号入口**——按编号跳读即可。

### Cookbook 配方（[`_appendix-cookbook/`](../../_appendix-cookbook/)）
- C7-1 Plugin 安装
- C7-2 Plugin 启用
- C7-3 ClawHub 发布
- C7-4 Plugin 故障

### FAQ 问答（[`_appendix-faq/`](../../_appendix-faq/)）
- F-Top20

### SOP 操作手册（[`_appendix-sop/`](../../_appendix-sop/)）
- SOP-4 升级 OpenClaw

### API 参考（[`_appendix-api/`](../../_appendix-api/)）
- 见 `_appendix-api/02-config-schema.md`（openclaw.json 20 顶层 key）
- 见 `_appendix-api/03-protocol-reference.md`（7 大协议格式）
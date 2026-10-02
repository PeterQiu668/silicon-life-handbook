# 第 10 章 · Skill 注册：对齐 Agent Skills 开放标准

> **v5.0 行业标准版 banner**：本章对应 OpenClaw 训练学第 10 章（接口层 3 / 4）；详见 [book README](../../README.md)。
> **License banner**：MIT（基于 OpenClaw 主仓 `LICENSE` 法律文本；GitHub API 显示 `NOASSERTION` 不影响法律效力——参见[真名验证与勘误](./真名验证与勘误.md)）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.6 (eb377ac)`（本书统一口径为 `2026.9.4 (3a9d69d)`）。
> **业界对位**：本章对应 **Agent Skills 开放标准**（agentskills.io · 25 723★ · 约 40 个客户端读 `SKILL.md`）——首次以**官方规范组织**形式取代 Anthropic 私有规范。
> **本章叙事目标**：正文以训虾哲学散文为主；操作手册、常见错误、新手坑、扩展阅读、诚实边界见章末「附录 A」原文区块（一字未删）。

---

## 10.0 为什么这一章存在

### 10.0.1 一个真实的困境：写得最好的那一份，恰好是最没用的那一份

如果你在 2026 年带过一支由多个智能体构成的小队（Agent Fleet，原：军团），你大概经历过这样一个顺序：

第一周，你很兴奋。你把过去半年积累的行业判断、客户名单、报价逻辑、交付标准，全部写进一份 Markdown 说明书，塞进 agent 的工作区（Workspace），然后对它说"以后按这个来"。它照做了，而且做得不错。

第二周，你开始加人。第二个 agent 上线，你意识到它读不到第一份说明书——因为那份文件挂在第一个 agent 的目录下。于是你复制了一份过去。

第三周，你发现两份说明书开始不同步。你在第一份里补了一条"报价低于 8 折必须走审批"，忘了补第二份。第二个 agent 报了一个 7.5 折的价。

第四周，你决定"统一管理"：把说明书抽到一个公共目录，写清楚"谁能读、什么时候读、读了之后干什么"。

于是你造出了一个东西，它有一个目录、里面有一个以 `SKILL.md` 命名的文件、文件开头有一段用三条短横线包起来的元数据、元数据里必须写清楚"什么时候该用我"。

你并没有见过 Anthropic 的规范。你只是被现实逼到了同一个形状。

**这一章要讲的，就是那个形状。**

### 10.0.2 为什么"能力"需要自己的注册表

接口层有四块拼图。第 8 章（MCP 绑定）解决的是"agent 怎么发现并调用工具"；第 9 章（A2A 绑定）解决的是"agent 怎么发现并让位给另一个 agent"；第 11 章（Plugin 入口）解决的是"训练学怎么被打包、安装、分发"。

那么 Skill 注册放在中间，解决的是什么？

它解决的是最容易被跳过、也最容易塌掉的一层：**能力本身如何被描述、被查找、被按需装载。**

工具（Tool）是函数。函数有明确的入参、出参、副作用。你可以用 JSON Schema 描述它，机器读得懂。

能力（Capability）不是函数。能力是"遇到这种情况，我该按什么顺序思考、查哪些东西、按什么标准收尾"。它包含判断、包含取舍、包含"什么时候不要做"。它没法被 JSON Schema 描述完整，但它可以被**写下来**。

于是出现了一个分野：

- 能被结构化描述的，变成了 Tool / MCP / A2A 这一类**协议层对象**；
- 只能被自然语言描述、但必须让 agent 在正确时刻**找到并装载**的，变成了 Skill 这一类**能力层对象**。

这就是为什么本章标题不是"Skill 规范"，而是"Skill 注册"。

规范回答"长什么样"；注册回答"**谁在什么时候、用什么代价、把哪一个能力装载进上下文**"。

一个没有注册机制的能力库，等于一个没有索引的图书馆。书都在，但你找不到。agent 找不到能力，就会用它的默认行为去应付——而默认行为，几乎总是"看起来很像、实际上不对"。

### 10.0.3 三次范式迁移，和一个迟到的共识

把 2023 到 2026 这三年串起来看，agent 能力的封装方式经历了三次迁移。理解这三次迁移，你就理解了为什么 2025-10-16 那天值得被记住。

**第一次迁移（2023）· 从提示词到函数：**
业界意识到"让模型自由发挥"不可控，于是开始把动作收敛成函数调用。OpenAI 的 function calling、AutoGen 的 function schema、LangChain 的 Tool 抽象，都属于这一次迁移。核心信念是：**能力 = 可被 JSON 描述的动作**。

这次迁移极其成功，也留下了它的盲区：它能描述"做什么"，描述不了"怎么做才对"。你没法用 JSON Schema 表达"给客户报价前先确认对方有没有预算"。

**第二次迁移（2024）· 从函数到协议：**
工具从"进程内的一个函数"变成"跨进程的一个端点"。MCP 在这条路上成为事实标准。核心信念是：**能力 = 可被标准协议发现的服务**。

这次迁移解决了复用和隔离，但把"知识"留在了原地。一个 MCP server 能告诉你它有哪些工具，不能告诉你一套业务判断该按什么顺序执行。

**第三次迁移（2025-2026）· 从协议到文本：**
Anthropic 在 **2025-10-16** 发布了 Agent Skills：把能力重新定义为一个**目录**，里面有一个 `SKILL.md`，Markdown 正文 + YAML frontmatter（前置元数据）。**2025-12-18**，这套格式被开放为标准，由 agentskills.io（仓库 `agentskills/agentskills`，Apache-2.0，2026-09-27 实拉 25 723★）独立维护。到 2026 年，约 **40 个产品/客户端**声明能读 `SKILL.md`；2026-02 起，标准开始引入**组织级管理**（组织内可发布、审批、下架 skill，而非只靠个人目录）。

核心信念是：**能力 = 一段被结构化索引的自然语言指令，agent 按需装载，按需卸载。**

这是一次"退回去"的迁移——从结构化退回自然语言。它之所以能成立，是因为同时具备了三个前提：

1. 模型的指令遵循能力（instruction following）到了可用阈值；
2. 上下文窗口足够大，"按需装载"变得经济；
3. 有人愿意把格式开放出来，而不是锁在里面。

三个前提缺一个，这件事就做不成。所以 2025-10-16 不是"Anthropic 发了一个新功能"，而是**三个条件终于同时满足**的那个日子。

### 10.0.4 为什么这件事对"训练学"是生死攸关的

本书前面九章讲的是训练学本身：七大契约、系统骨架、训练流程、长期表现、治理系统、协同军团、超维演进。

如果你只把训练学当成"一套理论"，它到这里就可以结束了。

但你如果要让训练学**被执行**，就必须回答一个工程问题：**训练学怎么进入 agent 的上下文？**

有三种可能的答案：

**答案一：写进灵魂文件（SOUL）。**
好处是永远在场；坏处是永远在场——它占用了每一轮的上下文预算，而且改一次要重启全部行为。适用于少而硬的规则（比如"不许对外承诺未审批的价格"）。

**答案二：打包成插件（Plugin），让代码执行。**
好处是可靠、可版本化；坏处是它只能承载"确定性逻辑"。你可以用插件强制检查报价，但没法用插件教 agent"这次客户在试探，别急着给方案"。

**答案三：写成 Skill，让 agent 按需装载。**
这是唯一能承载"情境化判断"的形态，因为它本质上是**给 agent 看的一段人话**，只在相关的时候出现。

训练学的绝大部分内容，属于第三类。这就是本章存在的理由：**没有 Skill 注册，训练学就只是一套漂亮的文档；有了 Skill 注册，训练学才有可能成为 agent 在关键时刻真正调用的东西。**

而这也是本书与业界 6 大框架对位时最诚实的一处差异：LangGraph / AutoGen / CrewAI / Claude Agent SDK / OpenAI Agents SDK / LlamaIndex 里，没有任何一个把"训练学的可装载化"当作产品哲学——它们提供容器，不提供内容。而 Skill 标准恰好给了内容一个通用的容器格式。

### 10.0.5 本章要回答的九个问题

读完这一章，你应该能回答：

1. 一个 `SKILL.md` 的最小合规形态是什么？六个 frontmatter 字段分别管什么？
2. 为什么 agent 能持有几百个 skill 而不被上下文撑爆？（三级渐进披露）
3. `description` 到底该怎么写，才既不啰嗦又能被命中？
4. `name` 为什么必须小写、连字符、且与目录名一致？
5. `allowed-tools` 是权限边界还是提示？它和 OpenClaw 的 `tools` 配置是什么关系？
6. 本机 236 个 skill 的真实健康度如何？（本章给出一份**逐条可复现的体检报告**）
7. 为什么"Skill 是剧本、Plugin 是剧组"？两者的边界在哪一行？
8. 同一套 skill 怎么跨平台（Claude / Gemini CLI / OpenCode / OpenHands / ZeroClaw）分发？
9. 哪些话不能说？（诚实边界：本章 10.12.4）

### 10.0.6 一个必须先破除的错觉

最后，本章想在最前面就拆掉一个错觉，因为它会污染后面所有的判断：

**"我写了一个 Markdown 文件" ≠ "我的 agent 会用这个文件"。**

这两件事之间，隔着一整套查找与装载机制。而这个机制对你是不可见的——它发生在上下文被拼装的那一刻，你既看不到也没法直接干预。

你唯一能控制的是**入口条件**：文件放在哪、文件叫什么、元数据写了什么、描述里有没有"什么时候该用我"。

本章后面所有的操作，本质上都是在优化这一个入口条件。

**能力层的全部价值，不取决于你写了多少行，而取决于 agent 在对的时候，能不能找到它。**

### 10.0.7 本章的组织方式与读法

本章之后的正文分四大块，刻意按"散文先行、操作后置"编排：

- **10.1 – 10.9｜九个核心概念**：每个概念一律用同一套八步展开——① 一句话定义 ② 现场直觉 ③ 结构解剖 ④ 为什么这样设计 ⑤ 真名与实测 ⑥ 边界（什么时候不适用）⑦ 反例与失败模式 ⑧ 练习与验收。八步固定，是为了让你在第三个概念之后就能预测第八步要做什么，从而把注意力从"结构"移到"判断"。
- **10.10｜怎么做**：把九个概念串成一条可执行的落地路径（含三层目录、六字段模板、批量补 frontmatter 的策略与风险）。
- **10.11｜常见误区**：九个错误，每一个都附"为什么这个错误特别容易犯"和"怎么在 30 秒内自查"。
- **10.12｜深度专题**：2026 前沿追踪 / 六大框架对位表 / 本机 236 skill 实测审计 / 诚实边界。

**章末「附录 A」是本章的操作手册（原 SOP 节）与全部附件的原文后移**，一字未删。它的行号、命令、数字口径与正文完全一致；如果你只是想马上动手，可以直接跳到附录 A 的第一步。

> ⚠ **关于附录 A 的一个阅读提示**：附录 A 区块是**逐字保留下来的原章节体**。其中出现的历史章号字样（如"第 11 章"）属于章号统一之前的口径；本书现行章号以文件首行为准——**本章 = 第 10 章 = 路径 `chapters/10-skill-registry/`**。正文重新编号，附录原文不动，两者的差异是刻意保留的。

---

## 10.1 核心概念一 · SKILL.md 是什么

### ① 一句话定义

**SKILL.md 是一个放在独立目录里的 Markdown 文件，它的正文是用自然语言写给 agent 看的操作规程，它的开头是一段 YAML frontmatter（前置元数据），用来告诉系统"我是谁、我什么时候该被用"。**

官方定义（agentskills.io 实拉，2026-09-27）：

> **"Agent Skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows. At its core, a skill is a folder containing a SKILL.md file."**

### ② 现场直觉

把它想成一张**贴在工具箱侧面的一张卡片**。

工具箱本身（模型、工具、通道、记忆）是骨架，在别的章节。这张卡片不是工具，它不执行任何东西。它写的是："这把扳手适合拧 8–14mm 的六角螺母，拧之前先确认螺纹方向，如果锈死不要加大力矩而要先上润滑油。"

它最值钱的部分不是那把扳手，是**最后那句"不要加大力矩"**。

模型什么都会一点，但也什么都会做错。SKILL.md 的价值，八成在"不要"和"先确认"这些地方。

### ③ 结构解剖

一个合规的 skill 目录，最小形态是：

```text
~/.openclaw/workspace/skills/<skill-name>/
└── SKILL.md          ← 唯一必需文件
```

扩展形态（推荐，但不是必需）：

```text
~/.openclaw/workspace/skills/<skill-name>/
├── SKILL.md          ← 第一层：入口 + 触发条件（建议 ≤ 200 行）
├── references/       ← 第二层：按需读取的参考资料
│   ├── api.md
│   └── edge-cases.md
├── scripts/          ← 可执行脚本（确定性逻辑，不要塞进正文）
│   └── check.sh
└── assets/           ← 模板 / 夹具 / 示例数据
    └── report-template.md
```

`SKILL.md` 的内部结构：

```markdown
---
name: <小写-连字符-与目录名一致>
description: <什么时候该用我 + 我做什么>
license: MIT
metadata:
  author: <谁维护>
  version: "1.0"
---

# <人类可读标题>

## 训练目标 / 用途
<一段话说清它存在的理由>

## 操作流程
1. ...
2. ...

## 边界
<什么时候不要用我>
```

### ④ 为什么这样设计

四个设计选择，每一个都是刻意的：

**选择一：能力是"目录"而不是"文件"。**
因为能力天然是复合的。一个完整的业务能力往往包含"怎么判断 + 查什么 + 输出什么格式 + 有哪些坑"。用单文件承载会写成一篇长文；用目录承载，就可以分层：入口短，细节深。这个"目录"决定直接催生了三级渐进披露（10.3）。

**选择二：正文是 Markdown，不是代码。**
因为要装载它的是**模型**，不是编译器。Markdown 是人类和模型都最省力的共同格式。这带来一个反直觉的后果：**写 SKILL.md 的能力，本质上是写文档的能力**，不是写代码的能力。

**选择三：元数据是 YAML，不是 JSON5。**
因为前置元数据是给人写的、给简单解析器读的。YAML 对多行文本、注释、缩进友好；JSON5 更适合机器生成的结构化清单（那是第 11 章 plugin manifest 的选择）。**两处混用是本章最高频的错误。**

**选择四：触发条件写在元数据里，不写在正文里。**
因为系统必须在**装载之前**知道该不该装载你。正文是装载之后才读的。这是一个先有鸡还是先有蛋的问题，解决方案是：把"该不该用我"压缩进 `description`，让它在装载前就能被判断。

### ⑤ 真名与实测

| 项 | 真名 / 实测 | 来源 |
|---|---|---|
| 目录 | `~/.openclaw/workspace/skills/` | 本机实测：`ls \| wc -l` = **238**（含 2 个非目录条目） |
| 纯 skill 目录数 | **236** | `find . -maxdepth 1 -type d \| wc -l` = 237 − 1（父目录） |
| 文件名 | `SKILL.md`（全大写，无扩展别名） | 全库 `--include=SKILL.md` 命中 |
| 元数据格式 | YAML（`---` 包裹，必须在第 1 行） | `_appendix-api/scripts/check-skill-frontmatter.py` 实跑 |
| 官方校验工具 | `npx skills-ref validate <dir>` | ⏳ 本机未装 |

**本机体检的第一个真实数字**：236 个 skill 目录中，**221 个含 `SKILL.md`**——也就是说有 **15 个目录连入口文件都没有**。这 15 个目录在物理上存在，在能力层不存在。

### ⑥ 边界：什么时候 SKILL.md 不是正确答案

三类情况不要写 SKILL.md：

1. **确定性逻辑**。要做字符串校验、要做加解密、要做格式转换——写成脚本放进 `scripts/`，或者升级为 Plugin（第 11 章）。让模型"读一段话然后心算"是最贵的实现方式。
2. **必须永远在场的硬约束**。比如合规红线、安全闸门。这类东西应该在契约文件（SOUL / AGENTS）里，或者在插件里强制。放进 skill 意味着"可能不被装载"，而"可能不生效的红线"不能叫红线。
3. **一次性任务**。如果这件事只做一次，直接说给 agent 听就行。skill 的成本在维护，不在创建。

### ⑦ 反例与失败模式

**失败模式 A：把 SKILL.md 写成 README。**
症状：正文长度 800 行，前 200 行在讲背景、讲愿景、讲这个能力多重要。
后果：正文只有被装载后才读，而它被装载的前提是 `description` 命中。前面那 200 行永远等不到读者。
修法：把背景移到 `references/`，正文只留"怎么做"。

**失败模式 B：把 SKILL.md 写成代码注释。**
症状：正文里出现 `function check(input) { ... }` 这样的伪代码块。
后果：模型会在不该执行的时候"脑补执行"；真正需要执行的逻辑反而不确定。
修法：确定性逻辑抽到 `scripts/`，正文只写"什么时候调用这个脚本、成功了看什么、失败了看什么"。

**失败模式 C：目录名与 `name` 不一致。**
症状：目录叫 `drift-audit`，frontmatter 里写 `name: DriftAudit`。
后果：本机实测有 **52 个** skill 命中 `NAME_DIR_MISMATCH` 问题码——这是全库第三高的问题码。
修法：一次性批量改（见 10.10）。

### ⑧ 练习与验收

**练习**：在你本机跑下面三条命令，把三个数字抄下来。

```bash
cd ~/.openclaw/workspace/skills
ls -1 | wc -l                          # 期望：238（含非目录文件）
find . -maxdepth 1 -type d | wc -l     # 期望：237（含父目录；-1 = 236）
find . -name SKILL.md | wc -l          # 期望：221（本机实测）
```

**验收标准**：你能解释"为什么同一个东西有三个数"。如果你的回答是"数错了吧"，请回到 10.4.5 的数字口径节。

---

## 10.2 核心概念二 · YAML frontmatter 的六个字段

### ① 一句话定义

**frontmatter 是 SKILL.md 顶部用 `---` 包起来的一段 YAML，它只干一件事：让系统在不读正文的前提下，决定要不要装载这个 skill。**

### ② 现场直觉

frontmatter 不是"给文件加标签"，它是**索引卡**。

图书馆不会让你把整本书翻一遍才能判断要不要借。索引卡上写的每一个字，都是为了让你在 5 秒内决定"是这本还是不是"。

判断 frontmatter 写得好不好，只有一个标准：**如果把它单独打印出来，一个不了解你业务的人，能不能据此判断"遇到什么情况该翻出这张卡"。**

### ③ 结构解剖

本章采用的六字段口径（与同目录 `SKILL.md-frontmatter-规范.md` 一致）：

| # | 字段 | 必填 | 作用 | 本机覆盖率 |
|---|---|---|---|---|
| 1 | `name` | ✅ | 唯一标识；小写 + 连字符；**必须等于父目录名** | 192 / 236 |
| 2 | `description` | ✅ | 触发条件 + 功能一句话（**决定装载命中率**） | 大多数含 name 的都有 |
| 3 | `license` | 推荐 | 授权声明；跨组织分发时的法律前提 | **24 / 236（10%）** |
| 4 | `metadata.author` | 推荐 | 谁维护；出问题找谁 | 少 |
| 5 | `metadata.version` | 推荐 | 版本号；与底座版本分开 | 少 |
| 6 | `allowed-tools` | 视需要 | 工具白名单；**只在真的需要限制时才写** | 极少 |

最小合规实例：

```markdown
---
name: silicon-life-double-triangle
description: 双三角模型训练法。当需要训练智能体从"响应型"过渡到"提案型"时使用。
  触发场景：每周复盘、主动性不足、只会等指令。
license: MIT
metadata:
  author: openclaw-silicon-life-handbook
  version: "1.0"
---

# 双三角模型训练法

## 训练目标
让 agent 学会自主生成期望值（Expectation），而不是等用户给指令。
```

### ④ 为什么这样设计

**为什么必填只有两个？**
因为只有这两个字段在"装载决策"里被用到：`name` 用来索引，`description` 用来判断相关性。其余字段都是治理用的——它们让 skill 能被管理，但不影响它能不能被用。

**为什么 `license` 只有 10% 覆盖率却仍然重要？**
因为本章的读者大概率会把 skill 分享出去。一个没有 `license` 的 skill，在组织间分发时没有法律依据。本机 236 个 skill 里 **212 个缺 `license`**——这是一个安静的合规缺口：平时不疼，出事的时候很疼。

**为什么用 block scalar？**
`description` 经常会写成两行。YAML 里跨行必须用 `>`（折叠）或 `|`（保留换行）。写成裸的两行，YAML 解析会直接失败——这不是"不优雅"，是"坏了"。

### ⑤ 真名与实测

本机审计脚本（`_appendix-api/scripts/check-skill-frontmatter.py`）实跑结果：

```text
236 目录：ok 48 · warn 86 · error 101 · info 1

问题码 Top 3：
  DESC_NO_TRIGGER        97   ← description 里没有"什么时候用我"
  DESC_SHORT             56   ← description 过短
  NAME_DIR_MISMATCH      52   ← name 与目录名不一致

其他：
  NO_FRONTMATTER         28   ← 有 SKILL.md 但 frontmatter 缺失/不在第 1 行
  6/6 字段全覆盖样本      0    ← 一个都没有
  5/6 字段（最高档）      11
```

**这份数字必须被正确解读**：`ok: 48` 的含义是"**没有 error 级问题**的目录有 48 个"，**不等于** "48 个 skill 六字段全覆盖"——六字段全覆盖的样本数是 **0**。

### ⑥ 边界

- **不要为了"字段齐"而填字段。** 如果你没有跨多个客户端验证过，就不要写 `compatibility`；如果你根本不依赖工具白名单语义，就不要写 `allowed-tools`。虚假的元数据比缺失的元数据更糟，因为它会误导下一个维护者。
- **不要把长内容塞进 frontmatter。** 500 字的 `description` 不但撑爆索引，还会让命中判断变模糊。长内容去 `references/`。
- **不要用 YAML 写 plugin manifest。** 那是 JSON5，见第 11 章。

### ⑦ 反例与失败模式

**反例一（最高频）**：

```yaml
description: 这是一个非常强大的工具，可以帮你高效处理各种复杂任务。
```

问题：全都是形容词，没有一个"什么时候"。它会被判为 `DESC_NO_TRIGGER`——本机有 **97 个** skill 命中这个码，是所有问题里最多的一个。

改成：

```yaml
description: 客户报价合规检查。当用户要求生成/修改报价单，或提到"折扣""审批""低于几折"时使用。
  不适用于内部成本核算。
```

**反例二**：把 name 写成大写驼峰。

```yaml
name: DriftAudit      # ❌ 与目录 drift-audit 不一致，且不符合小写+连字符
```

**反例三**：frontmatter 不在第 1 行。

```markdown
<!-- 维护说明：本 skill 用于 ... -->
---
name: drift-audit
```

`---` 不在第 1 行 → 解析器直接判定 `NO_FRONTMATTER`。本机有 **28 个** 命中。

### ⑧ 练习与验收

```bash
# 1) 找出所有缺 license 的（本机应为 212 个）
cd ~/.openclaw/workspace/skills
ls -d */ | wc -l
grep -l '^license:' */SKILL.md 2>/dev/null | wc -l    # 期望：24

# 2) 找出 name 与目录名不一致的
for d in */; do
  d=${d%/}
  n=$(grep -m1 '^name:' "$d/SKILL.md" 2>/dev/null | sed 's/^name:[[:space:]]*//')
  [ -n "$n" ] && [ "$n" != "$d" ] && echo "MISMATCH: $d vs $n"
done | head -20

# 3) 找出 frontmatter 不在第 1 行的
for f in */SKILL.md; do head -1 "$f" | grep -q '^---$' || echo "BAD: $f"; done | wc -l
```

**验收标准**：你能说出你本机 Top 3 问题码分别有多少个，以及你打算先修哪一个、为什么。

---

## 10.3 核心概念三 · 三级渐进披露（Progressive Disclosure）

### ① 一句话定义

**三级渐进披露是 Skill 标准的核心机制：skill 的内容分三层，agent 只在"需要更深"的时候才读下一层，从而在持有几百个 skill 的同时，只消耗与当前任务相关的上下文。**

### ② 现场直觉

想象你在医院分诊。

你进门，护士不会让你立刻做全套检查。她先看你的主诉（第一层），然后决定叫哪个科室；科室医生问几句（第二层），最后才决定要不要做 CT（第三层）。

**每一层的信息量都在涨，被触发的概率都在降。**

skill 就是这个逻辑：

- 第一层：全部 skill 的 `name` + `description` 常驻（几百条，很便宜）
- 第二层：被命中的 `SKILL.md` 正文被装载（几条，中等）
- 第三层：正文里写"详见 `references/x.md`"时才去读（极少数，最贵）

### ③ 结构解剖

| 层 | 内容 | 何时进入上下文 | 本机对应的物理位置 | 建议体量 |
|---|---|---|---|---|
| **L1 索引** | `name` + `description` | **always**（常驻） | 各 `SKILL.md` 的 frontmatter | 每条约 20–40 词 |
| **L2 正文** | `SKILL.md` 的 Markdown 正文 | 该 skill 被判定相关时 | `SKILL.md` | **≤ 200 行** |
| **L3 参考** | 细则、边界用例、模板、脚本 | 正文显式指向时 | `references/` `scripts/` `assets/` | 不限 |

### ④ 为什么这样设计

**因为上下文是唯一真正稀缺的资源。**

一个不带渐进披露的 skill 库，规模上限大约在"几十个"——再多，索引本身就会把窗口占满。而渐进披露把"持有成本"和"使用成本"解耦了：

- **持有成本**：只和 `description` 的长度与被持有数量有关（L1）；
- **使用成本**：只和"本次真正被装载了几个"有关（L2/L3）。

这个解耦带来一个重要的工程后果：**优化 skill 库的第一优先级，不是把 skill 写短，而是把 `description` 写准。** description 写得准，命中就准；命中准，无用装载就少；无用装载少，窗口就宽。反过来，description 写得模糊，会同时抬高持有成本（要写得更长才能说清）和无效装载率。

### ⑤ 真名与实测

- L1 常驻的物理载体：本机 `~/.openclaw/workspace/skills/*/SKILL.md` 的 frontmatter，共 **236 个目录 / 192 个含 `name:`**。
- L2 的体量风险：本机全库第一层正文长度分布差异极大，长文 skill 会把 L2 变成 L3 的成本。
- L3 的实际使用：本章同目录的 `SKILL.md-frontmatter-规范.md`、`8卷Skill写法适配.md` 就是 L3 形态的典型（细则外置）。
- 相邻真名：`openclaw skills list`（agent 视角的 skill 列表）；`openclaw skills check --agent tiance` 本机实跑 **Total 253**——比 236 大，因为 **agent 级注入 skill 也算在内**（`~/.openclaw/workspace/agents/<agent>/skills/`）。这个差值本身就是一个"披露"问题：你在全局池里看到的，不是某个 agent 实际持有的。

### ⑥ 边界

渐进披露不是免费的，它有三条边界：

1. **L1 的容量不是无限的。** 每个 skill 的 description 短 20 词，乘以 300 个，就是 6000 词的常驻开销。所以要控制"被持有的 skill 总数"，而不只是控制单个 skill 的长度。
2. **L2 的跳转不能超过一跳。** 如果 `SKILL.md` 里写"详见 A，A 里写详见 B"，模型需要在装载后再发一次读取——多跳会显著抬高失败率。**推荐最多一跳，且跳转目标必须写清路径。**
3. **L3 不是垃圾场。** 把不用的东西丢进 `references/` 并不会让它消失，只会让它在下一次被"顺手读到"。L3 的正确用法是"高频可复用但不必常驻"的内容。

### ⑦ 反例与失败模式

**反例一：全库体量错配。**
把 900 行的业务手册整个塞进 `SKILL.md` 正文。第一层 200 行的建议被无视了，结果是：一旦命中，就吃掉 900 行的窗口。

**反例二：把"触发条件"写进正文。**
正文里写"当你需要做价格审批时……"。问题是：**正文只有在被装载后才能被读到**，此时装载决策已经做完了。判断依据必须在 L1。

**反例三：description 之间互相打架。**
本机 Top 1 问题码 `DESC_NO_TRIGGER = 97` 的深层后果不只是"没写触发条件"，而是**大量 skill 的 description 无法彼此区分**——当三条 description 长得一样时，模型只能随机挑，或者一起装载。

### ⑧ 练习与验收

```bash
# 1) 你的 L1 有多少字？（估算常驻开销）
cd ~/.openclaw/workspace/skills
for d in */; do
  sed -n '/^description:/,/^[a-z-]*:/p' "$d/SKILL.md" 2>/dev/null | head -5
done | wc -w

# 2) 找出正文超长的（L2 体量风险）
for f in */SKILL.md; do printf "%5d %s\n" "$(wc -l < "$f")" "$f"; done | sort -rn | head -15

# 3) 找出三层目录都不存在的（无 L3 的 skill）
for d in */; do [ -d "$d/references" ] || [ -d "$d/scripts" ] || [ -d "$d/assets" ] || echo "$d"; done | wc -l
```

**验收标准**：你能说出你本机 L1 的估算开销、最长的 3 个 L2、以及你打算给哪 3 个 skill 做"正文瘦身 + 内容下沉到 references/"。

---

## 10.4 核心概念四 · description 的写法：把"什么时候"写进 30 个词

### ① 一句话定义

**`description` 是 skill 唯一的常驻广告位：它必须在 20–40 个词里同时说清"我做什么"和"什么时候该叫我"，否则这个 skill 在能力层等于不存在。**

### ② 现场直觉

想象你在一个 300 人的公司里发一封自我介绍邮件，标题只能写一行。

写"我是 Peter，我很努力，我可以帮你处理各种事"——没人在需要的时候想起你。

写"我是 Peter，负责跨境报价合规；报价低于 8 折、或客户要求账期超过 60 天时找我"——需要的人会直接搜到。

`description` 就是那行标题。而且它比邮件标题更残酷：**没有人会读第二行再去决定要不要叫你。**

### ③ 结构解剖

一个高命中的 `description`，通常由三段组成（不一定分行，但要素必须在）：

```text
[场景/动作]  +  [触发词清单]  +  [排除项]
```

实例：

```yaml
description: 跨境报价合规检查。当用户要求生成或修改报价单、提到"折扣/审批/账期/低于几折"时使用。
  不适用于成本核算与库存查询。
```

拆解：

| 段 | 内容 | 作用 |
|---|---|---|
| 场景/动作 | 跨境报价合规检查 | 说清"我是什么" |
| 触发词清单 | 报价单 / 折扣 / 审批 / 账期 / 低于几折 | 让**用户的原话**能命中你 |
| 排除项 | 不适用于成本核算与库存查询 | 防止被近邻技能误命中 |

**触发词清单要抄用户的词，不要抄你的词。**
这是最容易犯的错：你写"价格审批流程"，而用户说的是"这个折扣行不行"。索引里没有"折扣"，你就永远不会被叫到。

### ④ 为什么这样设计

**因为装载决策只看这 30 个词。**

系统在决定"要不要装载 skill X"时，能用的唯一依据就是 L1 里的 `name` + `description`（见 10.3）。正文、脚本、参考资料都不参与这个判断。这意味着：

- 正文写得再好，description 不准 → 永远不被装载；
- 正文写得一般，description 精准 → 每次都在对的时刻被装载。

所以 description 的投入产出比是整份 skill 里最高的。**把 80% 的打磨时间花在这 30 个词上，是理性的。**

**为什么必须有排除项？**
因为能力层是"近邻密集"的。本机 236 个 skill 里，大量名字相近、职责相邻（比如一堆 `*-audit`、`*-check`、`*-review`）。没有排除项时，模型面对三个都"看起来相关"的 skill，行为是不确定的——可能只装一个错的，也可能三个都装。

### ⑤ 真名与实测

本机审计实跑（`_appendix-api/scripts/check-skill-frontmatter.py`）：

```text
DESC_NO_TRIGGER        97   ← 全库第一问题码（占 236 的 41%）
DESC_SHORT             56   ← 第二问题码
```

脚本的判定规则（`_appendix-api/06-skill-manifest-reference.md` 中给出的实现）：

```python
issues.append({"code": "DESC_NO_TRIGGER",
               "msg": "description 缺触发词（Use when / 当用户 / 使用场景）"})
```

也就是说，一个**机器可判定的近似标准**是：description 里应当出现触发语标记，例如 `当用户` / `使用场景` / `Use when` / `触发`。

**这是一个可以立刻改善的杠杆点**：本机 97 个 skill 只要补上一句触发语，就能从"机器可判定的无触发条件"变成"有触发条件"。这不代表它们立刻变好，但它代表**它们至少进入了可被检索的状态**。

### ⑥ 边界

- **不要靠关键词堆砌。** 塞 30 个词进 description 会稀释信号，模型会判定"什么都相关"。
- **不要在 description 里写实现细节。** "使用 Python 3.11 与 pandas 2.x 处理"对命中没有帮助。
- **不要复制粘贴别人的 description。** 本机存在的隐忧是 description 高度同质化（大量"这是一个...的 skill，用于..."）——同质化的描述会让整个索引失效。
- **中文与英文混排时注意**：如果用户可能用英文提问，触发词要给英文版本（例如同时给"报价单 / quotation"）。

### ⑦ 反例与失败模式

**反例一：形容词堆叠**

```yaml
description: 强大高效专业的智能助手工具，能够帮助你智能处理复杂任务。
```

→ `DESC_NO_TRIGGER`。读者读完不知道什么时候用它。

**反例二：只写功能，不写场景**

```yaml
description: 生成飞书文档并推送到指定群聊。
```

功能清楚，但缺"什么时候"。用户的表达是"把这个结果发到群里"，不会有"生成飞书文档"这个词。

**反例三：多行不用 block scalar**

```yaml
description: 第一行。
  第二行。          # ← 裸多行，YAML 直接崩
```

正确写法：

```yaml
description: >-
  第一行。
  第二行。
```

**反例四：description 与 skill 实际能力不符。**
这是最危险的一类：它会被命中，但装载后做不了那件事。失败成本比"没被命中"高得多——因为用户已经相信它能做。

### ⑧ 练习与验收

```bash
cd ~/.openclaw/workspace/skills

# 1) 找出你本机缺触发词的（近似判定，本机应接近 97）
grep -L -E '当用户|使用场景|Use when|触发' */SKILL.md 2>/dev/null | wc -l

# 2) 找出过短的 description（< 30 字符）
for f in */SKILL.md; do
  d=$(sed -n 's/^description:[[:space:]]*//p' "$f" | head -1)
  [ -n "$d" ] && [ ${#d} -lt 30 ] && echo "${#d}  $f"
done | head -20

# 3) 挑你自己的 3 个高频 skill，按"场景 + 触发词 + 排除项"重写 description
```

**验收标准**：你重写的 3 条 description，拿去问一个不了解你业务的人——他能否在 5 秒内说出"什么时候该用它"和"什么时候不该用它"。

---

## 10.5 核心概念五 · name 与目录名一致性

### ① 一句话定义

**`name` 是 skill 的机器标识：必须小写、只用连字符、且与父目录名逐字符相同——因为系统对不同来源的 skill，用的是两条不同的寻址路径。**

### ② 现场直觉

这是一个"两条路找同一个房间"的问题。

系统找 skill，有两条路：

- 路 A（按目录）：`skills/drift-audit/SKILL.md`
- 路 B（按标识）：索引里查 `name: drift-audit`

只要两条路指向同一个房间，一切正常。

如果目录叫 `drift-audit`、标识写 `DriftAudit`，那么按目录能找到、按标识找不到（或找到另一个），结果是：**统计口径分裂、去重失败、升级时出现"两个 skill"**。

### ③ 结构解剖

合规约束（三条同时满足）：

| 约束 | 合规 | 违规 |
|---|---|---|
| 字符集 | `[a-z0-9-]` | 大写、下划线、空格、点、中文 |
| 长度 | 建议 3–64 | 超长（索引噪音） |
| 与目录一致 | `name == basename(dir)` | 任何差异 |

本机实测的三类违规分布：

```text
NAME_DIR_MISMATCH     52   ← 第三问题码
name 字段违例（综合）  55
含 name: 字段         192  →  236 − 192 = 44 个连 name 都没有
```

### ④ 为什么这样设计

**因为 skill 本质上是"按目录分发"的，而标识是"按名字引用"的。**

当你把 skill 从一个客户端搬到另一个客户端，搬运的单位是**目录**。目标客户端先按目录名登记，再读 frontmatter 里的 `name` 做二次索引。两者不一致时，不同客户端的处理策略不同：

- 严格一点的，直接拒绝加载；
- 宽松一点的，以目录名为准（于是 frontmatter 里的 `name` 成了**假声明**）；
- 再宽松一点的，两者都登记（于是出现重名）。

三种行为都不可控，所以标准的选择是——**强制一致**。这不是审美要求，是消除歧义。

### ⑤ 真名与实测

```bash
# 本机实测：列出所有 name 与目录名不一致的
cd ~/.openclaw/workspace/skills
for d in */; do
  d=${d%/}
  n=$(grep -m1 '^name:' "$d/SKILL.md" 2>/dev/null | sed 's/^name:[[:space:]]*//;s/[[:space:]]*$//')
  if [ -z "$n" ]; then echo "NO-NAME   $d"
  elif [ "$n" != "$d" ]; then echo "MISMATCH  $d  ->  $n"; fi
done | tee /tmp/name-audit.txt
wc -l /tmp/name-audit.txt
```

本机基线：`MISMATCH 52` + 无 name 44 ≈ 96 个目录在"标识层"是可疑的。

### ⑥ 边界

- **不要为了"好看"改 name。** 改 name 会打断所有已经建立的引用（日志、治理账本、跨 agent 声明）。
- **不要重命名目录去迁就 frontmatter。** 同样的理由，反方向也一样疼。
- **例外情况**：如果你的 skill 是从别人的仓库克隆过来的，且你打算保留上游命名——那就整目录重命名（`mv`），而不是只改 `name`。**改一处就必须改另一处。**

### ⑦ 反例与失败模式

**反例一：驼峰**

```yaml
name: DriftAudit         # 目录 drift-audit
```

**反例二：下划线**

```yaml
name: drift_audit        # 目录 drift-audit
```

**反例三：人类可读标题误入 name**

```yaml
name: 漂移审计            # 目录 drift-audit
description: ...
```

中文名可以作为正文 H1，但不能作为 `name`。这是一个非常常见的混淆：**H1 给人看，`name` 给机器看。**

**反例四：技能名与"实例名"混用**

```yaml
name: tiance-drift-audit   # 目录 drift-audit
```

把部署实例名写进了技能名。skill 是**可复用能力单元（Reusable Capability Unit）**，不是某个 agent 的私产。

### ⑧ 练习与验收

```bash
# 一键修复脚本（先 dry-run，再执行）
cd ~/.openclaw/workspace/skills
for d in */; do
  d=${d%/}; f="$d/SKILL.md"
  [ -f "$f" ] || continue
  n=$(grep -m1 '^name:' "$f" | sed 's/^name:[[:space:]]*//;s/[[:space:]]*$//')
  if [ "$n" != "$d" ]; then
    echo "FIX: $f  $n -> $d"
    # sed -i '' "s/^name:.*/name: $d/" "$f"    # 去掉注释即执行（先备份！）
  fi
done
```

**执行前必做**：`openclaw backup create`（破坏性操作前的安全网）。

**验收标准**：修复后重跑审计，`NAME_DIR_MISMATCH` 应降到 0（或只剩你明确决定保留的例外）。

---

## 10.6 核心概念六 · allowed-tools 的边界

### ① 一句话定义

**`allowed-tools` 是 skill 可以声明的工具白名单：它规定"这个 skill 被装载时，允许模型动用哪些工具"——它是能力声明，不是安全沙箱。**

### ② 现场直觉

把 `allowed-tools` 想成**手术器械盘**：这台手术只摆出需要的器械，其他的收起来。

好处是：医生不会在关键时刻伸手去够别的东西，动作更快、更不容易错。

但要注意：**器械盘收起来，是因为"不需要"，不是因为"禁止"。** 桌上没有那把刀，不代表去别的柜子里拿不到。

这个区分极其重要，因为很多人把 `allowed-tools` 当成安全边界，从而在该用强制手段的地方（合规红线、资金操作）用了它。

### ③ 结构解剖

```yaml
---
name: drift-audit
description: 漂移审计。当需要检查智能体行为是否偏离契约时使用。
allowed-tools:
  - read_file
  - search_files
  - terminal
---
```

| 维度 | `allowed-tools`（skill 级） | `tools` / 插件契约（系统级） |
|---|---|---|
| 谁声明 | skill 作者 | 系统所有者 / 插件 manifest |
| 生效范围 | 该 skill 装载期间的建议性边界 | 全局或插件运行期 |
| 强制力 | **软**（提示模型少动手） | **硬**（运行时拦截） |
| 典型用途 | 降噪、聚焦、防误触 | 合规、安全、成本控制 |

### ④ 为什么这样设计

**因为 skill 的核心问题是"注意力"，不是"权限"。**

一个装载了 40 个工具的环境里，模型最容易犯的错不是"用了不该用的工具"，而是"在错误的方向上过度使用工具"——反复 grep、反复读文件、把窗口塞满。

`allowed-tools` 用声明的方式告诉模型："这次你只需要看和读，不需要写。"这能显著降低无效动作。

**但权限，必须由系统级机制承担。** 这是本章最想留下的一条纪律：

> **凡是你不能接受"偶尔失效"的约束，都不要放在 skill 里。**

### ⑤ 真名与实测

- 本机实测：`allowed-tools` 覆盖率极低——因为绝大多数 skill 作者并不知道这个字段存在。
- OpenClaw 侧的工具配置真名是 `tools`（顶层配置项之一，本机 `~/.openclaw/openclaw.json` 顶层 key 中含 `tools` 与 `skills` 两个独立 key）。
- 插件侧的能力声明走 `contracts.tools` + `--accept-capabilities`（见第 11 章），这是**硬声明**：安装/启用/升级时都必须显式接受。
- 相邻真名：`openclaw tools` / `openclaw plugins list`。

### ⑥ 边界

- **不要在没验证过的情况下写 `allowed-tools`。** 写错了会限制模型完成任务的必要动作——比不写更糟。
- **不要用它做合规。** 用契约文件 + 插件 + 审批流程。
- **跨平台时它是弱语义的。** 不同客户端对 `allowed-tools` 的支持程度不同（⏳ 本机未做跨客户端一致性验证）。所以：**只在单平台闭环内依赖它。**

### ⑦ 反例与失败模式

**反例一：把红线写进 allowed-tools。**

```yaml
allowed-tools:
  - read_file
# 作者以为这样就"禁止了写文件"
```

真相：这只影响被装载 skill 的**建议范围**。模型在别的回合照样能写。

**反例二：写了一个不存在的工具名。**

```yaml
allowed-tools:
  - readFile      # ❌ 真名可能是 read_file
```

工具名拼错 = 白名单拦截了所有真实工具 = skill 变哑巴。这是"静默失败"：没有报错，只是模型说"我做不到"。

**反例三：把全部工具都列上。**
"全都允许"等于"没写"，徒增噪音。

### ⑧ 练习与验收

```bash
# 1) 本机有多少 skill 声明了 allowed-tools
cd ~/.openclaw/workspace/skills
grep -l '^allowed-tools:' */SKILL.md 2>/dev/null | wc -l

# 2) 列出你声明的工具名，核对是否与真实工具名一致
grep -A5 '^allowed-tools:' */SKILL.md 2>/dev/null | head -30

# 3) 系统级真名核对（硬边界的正确位置）
openclaw plugins list --enabled --verbose | head -20
```

**验收标准**：你能说清你的 skill 里哪一类约束是"软建议"（留在 skill），哪一类是"硬红线"（必须搬到契约文件或插件）。

---

## 10.7 核心概念七 · Skill 治理与生命周期

### ① 一句话定义

**Skill 治理（Skill Governance）是指：一个 skill 从"被创建"到"被退役"的全过程中，谁负责、按什么标准改、改完怎么验证、什么条件下必须下线。**

### ② 现场直觉

一个没人管的 skill 库，三个月后会变成这样：

- 有的是上次重构前的旧版本，命令已经不存在了；
- 有的跟另一个 skill 做同一件事，只是名字不同；
- 有的引用了已经删掉的脚本；
- 没人知道哪个还能用，于是大家都不用，直接口述需求。

**skill 库的腐烂不是从"写得不好"开始的，是从"没人知道它是否还成立"开始的。**

### ③ 结构解剖

一个可运转的 skill 生命周期，有五个状态和四条规则：

```text
draft（草稿） → active（在用） → deprecated（弃用） → archived（归档） → removed（移除）
                    ▲                  │
                    └──── revised ─────┘
                        （修订后回归）
```

| 状态 | 含义 | 允许的下一步 | 判据 |
|---|---|---|---|
| draft | 已落盘，未验证 | → active / removed | 有 frontmatter，未过触发验证 |
| **active** | 已验证可用 | → deprecated / revised | 触发成功 ≥ 1 次，有日志证据 |
| deprecated | 已被替代，暂留 | → archived / revised | `description` 里显式标注替代者 |
| archived | 移出索引，保留文件 | → removed | 移到 `skills/_archive/`（不参与索引） |
| removed | 删除 | — | 备份已存在（`openclaw backup create`） |

四条规则：

1. **每个 active skill 必须有一个 owner。** 写在 `metadata.author`，且是可以被联系到的人/角色。
2. **版本必须能对比。** `metadata.version` 单调递增；跨组织分发时与 `license` 同时存在。
3. **弃用必须先标注、后归档。** 不能直接删——引用它的地方（契约文件、其他 skill、治理账本）会静默断掉。
4. **审计要留证据。** 与本机治理体系一致：TEV（Three-Evidence Verification，三证据验证，原：三证验真）——**命令 + 输出 + 时间戳**，三件齐，才算验证。

### ④ 为什么这样设计

**因为"能力层"的最大风险不是能力不足，而是能力虚报。**

工具（Tool）是自证的：调用失败会报错。skill 不是自证的：装载后模型"努力照做"，做错了它不会说"这个方法已经过期了"。

所以 skill 治理的核心任务不是"写更多"，而是**让每一个还在索引里的 skill 都保持被验证过的状态**。这与本书第 4 章（长期表现）的**漂移治理（Drift Governance）**是同一条逻辑：不是禁止偏离，而是持续测量偏离。

### ⑤ 真名与实测

| 治理对象 | 真名 | 本机实测 |
|---|---|---|
| skill 池 | `~/.openclaw/workspace/skills/` | 236 目录 |
| agent 级 skill | `~/.openclaw/workspace/agents/<agent>/skills/` | 存在（`openclaw skills check --agent tiance` → **Total 253**） |
| 列表命令 | `openclaw skills list` | agent 视角 |
| 校验命令 | `openclaw skills check --agent <name>` | 本机实跑通过 |
| 官方格式校验 | `npx skills-ref validate <dir>` | ⏳ 本机未装 |
| 配置位置 | `~/.openclaw/openclaw.json` 顶层 `skills` key | 与 `tools` 为两个独立 key |
| 安全网 | `openclaw backup create` | 破坏性操作前必跑 |

**关键口径**：`Total 253 > 236` 说明"全局池"与"agent 实际持有"不是一个数。做治理时必须以**agent 视角**为准——因为你的 agent 真正能用的，只有它持有的那些。

### ⑥ 边界

- **不要给小团队上重型流程。** 你只有 8 个 skill 的时候，不需要五状态机。用最轻的版本：`owner` + `version` + "每月跑一次审计脚本"。
- **不要在 skill 里做能力冲突仲裁。** 三个 skill 都声称处理报价审批时，仲裁应该发生在 skill 之外（契约或治理层），不能在 skill 正文里写"如果同时装载了 X，则以我为准"——它读不到 X。
- **不要让归档目录参与索引。** 归档必须移到索引之外（例如 `skills/_archive/`），否则"归档"等于没做。

### ⑦ 反例与失败模式

**反例一：只增不减。**
本机 236 个 skill 中，"有多少是你上季度真的用过一次的"？如果答不上来，说明治理没做。

**反例二：改了正文不改 version。**
版本号失去意义后，你无法回答"昨天到今天变的是什么"。

**反例三：弃用不标注。**
最典型的表现是索引里同时存在 `skill-security-audit` 与 `skill-security-audit-v2` 两个目录。**本机就存在这种情况**——引用时必须写清是哪一个，否则命令会跑空。

**反例四：审计不留证据。**
"我检查过了"不是证据。没有时间戳的结论会在两周后失效。

### ⑧ 练习与验收

```bash
# 1) 你的 skill 库有没有"活跃度"证据？
cd ~/.openclaw/workspace/skills
for d in */; do printf "%-40s %s\n" "${d%/}" "$(stat -f '%Sm' -t '%Y-%m-%d' "$d/SKILL.md" 2>/dev/null)"; done | sort -k2 | tail -20

# 2) 归档目录是否在索引内（应不存在或为空）
ls -d ~/.openclaw/workspace/skills/_archive 2>/dev/null || echo "✓ 无归档目录（尚未开始归档）"

# 3) 建立最小治理台账（三列：skill / owner / 上次验证日期）
echo "skill,owner,last_verified" > /tmp/skill-ledger.csv
for d in */; do d=${d%/}; echo "$d,?,$(stat -f '%Sm' -t '%Y-%m-%d' "$d/SKILL.md" 2>/dev/null)" >> /tmp/skill-ledger.csv; done
wc -l /tmp/skill-ledger.csv
```

**验收标准**：你有一份可用的台账，且能在 1 分钟内回答"哪个 skill 超过 90 天没被验证过"。

---

## 10.8 核心概念八 · 本机 236 skill 真实体检（Skill Audit）

### ① 一句话定义

**Skill 审计（Skill Audit）是用一个可复现的脚本，把整个 skill 库的合规状态压成一张"问题码分布表"，让"我该先修哪一个"从猜测变成排序。**

### ② 现场直觉

体检的价值不在于"知道你不健康"，而在于**知道先治哪个**。

一个 236 项的库，人工翻一遍要半天，而且结论不可复现（今天说 30 个有问题，明天说 40 个）。

审计脚本把这件事变成：跑一次、出四个数、按问题码排序。

### ③ 结构解剖

本章采用的审计输出结构（实跑于 `_appendix-api/scripts/check-skill-frontmatter.py`）：

```text
== 总量 ==
236 个 skill 目录

== 严重度分布 ==
ok     48    ← 无 error 级问题
info    1
warn   86
error 101

== 问题码 Top 3 ==
DESC_NO_TRIGGER      97
DESC_SHORT           56
NAME_DIR_MISMATCH    52

== 其他关键缺口 ==
NO_FRONTMATTER       28
无 name 字段          44
含 name 字段         192
标 license           24
6/6 字段全覆盖        0
5/6 字段（最高档）     11
```

### ④ 为什么这样设计

**因为"分数"会骗人，"分布"不会。**

一个"合规率 61%"的评分，会让你得出"还行"的错觉。而一张问题码分布表会立刻告诉你：**97 个 skill 的问题本质是同一个——没写触发条件。**

这就把 236 个待办压缩成 3 个动作：补触发词、补 name、修 name 一致性。

**审计的第二个设计原则是：必须区分"能自动修的"和"必须人来判断的"。**

| 问题码 | 可自动修？ | 处理策略 |
|---|---|---|
| `NAME_DIR_MISMATCH` | ✅ 可（`sed` 改 name） | 批量脚本 + 备份 |
| `NO_FRONTMATTER` | ⚠ 半自动（生成骨架后必须人补 description） | 生成模板 → 人工填 |
| `DESC_SHORT` | ⚠ 半自动 | 同上 |
| `DESC_NO_TRIGGER` | ❌ 必须人写 | 只能人写；但这正是 80% 的价值所在 |

### ⑤ 真名与实测

**这是一份完整可复现的体检报告，全部数字来自本机实跑。**

| # | 指标 | 实测值 | 测量方式 |
|---|---|---|---|
| 1 | 目录条目 | 238 | `ls ~/.openclaw/workspace/skills/ \| wc -l` |
| 2 | 纯 skill 目录 | **236** | `find . -maxdepth 1 -type d \| wc -l` − 1 |
| 3 | 含 `SKILL.md` | **221** | 逐目录存在性检查（15 个目录无入口文件） |
| 4 | 无 frontmatter | **47**（脚本口径）/ **28**（问题码口径） | 两种口径并存，见下 |
| 5 | `name` 违例 | **55** | 小写+连字符不满足，或 ≠ 父目录名 |
| 6 | 含 `name:` | **192** | `grep -l '^name:'` |
| 7 | 标 `license` | **24 / 236（10%）** | `grep -l '^license:'` |
| 8 | 无 error 目录 | **48** · warn **86** · error **101** · info **1** | 审计脚本实跑 |
| 9 | 问题码 Top 3 | `DESC_NO_TRIGGER` 97 / `DESC_SHORT` 56 / `NAME_DIR_MISMATCH` 52 | 审计脚本实跑 |
| 10 | `NO_FRONTMATTER` | **28** | 审计脚本实跑 |
| 11 | 6/6 字段全覆盖 | **0**（最高档 5/6 有 **11** 个） | 逐字段核对 |
| 12 | agent 视角总数 | **253** | `openclaw skills check --agent tiance` |

> **口径诚实声明（重要）**：第 4 行出现两个数（47 与 28），不是矛盾，是两种测量口径——`47` 指"有 `SKILL.md` 但首个 `---` 块不存在或不合法"（API 附录口径），`28` 指审计脚本在本次运行中命中的 `NO_FRONTMATTER` 问题码数量。**引用时必须带口径**，否则会得出"本机数据自相矛盾"的错误结论。这也是本书反复强调的纪律：**数字必须带口径。**

### ⑥ 边界

- **审计脚本不是官方校验器。** `npx skills-ref validate` 是标准方的校验工具（⏳ 本机未装）。自建脚本的判定规则（如"description 含触发词"）是近似规则，不是规范条文。
- **`ok: 48` 不等于"48 个合格"。** 它等于"48 个没有 error 级问题"。
- **不要以通过率为目标。** 以"问题码清零"为目标更实在，但**`DESC_NO_TRIGGER` 清零必须靠人写，不能靠脚本**。

### ⑦ 反例与失败模式

**反例一：把审计当 KPI。**
"合规率从 61% 提到 90%"——如果这 29% 是靠批量生成空 description 刷出来的，库反而更糟。

**反例二：只审计不修。**
审计报告放在那里三个月，问题码不变。**审计的唯一意义是驱动修改。**

**反例三：口径漂移。**
今天用 236，明天用 238，后天用 253，然后得出"skill 数量在增长"的结论。**先定口径，再报数字。**

### ⑧ 练习与验收

```bash
# 复现本章的核心三数（注意口径）
cd ~/.openclaw/workspace/skills
echo "口径 A · 目录条目:      $(ls -1 | wc -l | tr -d ' ')"          # 238
echo "口径 B · 纯 skill 目录: $(($(find . -maxdepth 1 -type d | wc -l) - 1))"  # 236
echo "口径 C · 含 SKILL.md:   $(find . -name SKILL.md | wc -l | tr -d ' ')"    # 221
echo "口径 D · 含 name:       $(grep -l '^name:' */SKILL.md 2>/dev/null | wc -l | tr -d ' ')"  # 192
echo "口径 E · 标 license:    $(grep -l '^license:' */SKILL.md 2>/dev/null | wc -l | tr -d ' ')" # 24
echo "口径 F · agent 视角:    $(openclaw skills check --agent tiance 2>/dev/null | tail -3)"
```

**验收标准**：你复现出的 A–F 六个数字与本章一致（允许版本差异 ±0），并能解释 B 与 C 的差值来自哪里（15 个无入口文件的目录）。

---

## 10.9 核心概念九 · 跨平台分发

### ① 一句话定义

**跨平台分发是指：同一份 skill 目录，不改内容、不改格式，就能被任何声明支持 Agent Skills 标准的客户端读取——这是 2025-12-18 开放标准带来的唯一真正新增的东西。**

### ② 现场直觉

在开放标准出现之前，你写的能力包是**平台资产**：换个客户端就得重写。

开放标准之后，它变成**文本资产**：它是一份人话，谁读都算数。

这个差别看起来小，实则是本书接口层最值钱的一句话：**训练学第一次有了"不依赖某一家实现"的载体。**

### ③ 结构解剖

跨平台分发有三个必要条件，缺一不可：

| # | 条件 | 为什么 | 本章对应 |
|---|---|---|---|
| 1 | **格式标准** | 对方要能解析你的 frontmatter | YAML 六字段（10.2） |
| 2 | **触发语义标准** | 对方要能判断何时装载 | `description` 契约（10.4） |
| 3 | **物理可搬运** | 目录自包含，无绝对路径依赖 | 目录结构（10.1）+ `references/` |

**第 3 条最容易被忽略**：如果你的 `SKILL.md` 里写死了 `/Users/peterqiu/...`，那它在别人机器上就是一篇废文。

### ④ 为什么这样设计

**因为"开放"解决的是信任问题，不只是技术问题。**

企业采用一个能力包之前会问三个问题：格式会不会变？供应商会不会锁我？授权是什么？

`agentskills.io`（Apache-2.0）+ 约 40 个客户端 + 2026-02 起的组织级管理，把这三个问题分别回答为：格式有公开规范、不是单一供应商财产、许可证清晰。

对本书的意义：**训练学可以出版为"标准格式的能力包"，而不是"某平台的配置集合"。**

### ⑤ 真名与实测

| 对位对象 | 关系 | 实拉来源 | 备注 |
|---|---|---|---|
| **Agent Skills 标准**（agentskills.io） | 定义者 | `agentskills/agentskills` · 25 723★ · Apache-2.0 | 本章对位基准 |
| Claude Code / Anthropic API | 一手定义者 | `anthropics/skills` · 178 606★ | 同一基准 |
| **OpenClaw**（本章） | ⚠ 结构兼容 | 本机 192/236 含 YAML frontmatter | 渐进对齐，非另起炉灶 |
| Gemini CLI | 客户端 | `google-gemini/gemini-cli` · Apache-2.0 | 跨平台一致 |
| OpenCode | 客户端 | `sst/opencode` · MIT | 跨平台一致 |
| OpenHands | 客户端 | `OpenHands/OpenHands` · MIT | 跨平台一致 |
| ZeroClaw（Rust） | 客户端 | `zeroclaw-labs/zeroclaw` · Apache-2.0 | 同赛道互补 |

> ⏳ **待验证**：Anthropic Skills 跨框架互通验证（同一 skill 在 ≥3 个客户端上的实际装载行为一致性）尚未做本机实测。**本章只声称"结构与格式兼容"，不声称"行为一致"。**

### ⑥ 边界

- **不要假设语义一致。** 各客户端对 `allowed-tools`、`license`、多行 description 的处理程度不同（见 10.6 边界）。
- **不要分发含密钥的 skill。** 检查 `scripts/` 与 `references/` 里有没有 token、内网地址、客户名单。
- **不要指望"一次写好"。** 跨平台分发的正确姿势是：先在一个客户端闭环验证，再分发；分发后每个客户端重跑一次触发验证。

### ⑦ 反例与失败模式

**反例一：绝对路径依赖。**

```markdown
## 操作流程
1. 读取 /Users/peterqiu/.openclaw/workspace/skills/drift-audit/references/cases.md
```

换机器即失效。正确写法：`references/cases.md`（相对 skill 目录）。

**反例二：把平台专有命令写进 skill 正文。**

```markdown
1. 执行 openclaw plugins enable my-plugin
```

如果这个 skill 要在别的客户端用，这条会误导。正确姿势：把平台专有步骤单独标注（"仅 OpenClaw"），或外置到 `references/openclaw.md`。

**反例三：分发时漏掉 `license`。**
本机 90% 的 skill 没有 `license`——这也是本章反复提醒的合规缺口。

### ⑧ 练习与验收

```bash
# 1) 找出含绝对路径的 skill（跨平台阻断项）
cd ~/.openclaw/workspace/skills
grep -l '/Users/' */SKILL.md 2>/dev/null | wc -l
grep -rl '/Users/' */references/ 2>/dev/null | head -5

# 2) 找出把平台专有命令写进正文的
grep -l 'openclaw plugins\|openclaw config' */SKILL.md 2>/dev/null | wc -l

# 3) 分包检查：选一个你想分发的 skill，确认它自包含
d=drift-audit
ls -R "$d" 2>/dev/null | head -20
```

**验收标准**：你能选出一个 skill，它的目录 `tar czf` 之后在另一台机器上解压即可用（无绝对路径、无平台专有命令、有 license）。

---

## 10.10 怎么做：把九个概念落成一条可执行的路径

前面九节都在讲"为什么"。这一节只回答一个问题：**从今天开始，你按什么顺序动手。**

路径分七步，顺序不可交换——每一步都为下一步提供输入。如果你时间很少，至少做完第 1、2、7 步。

### 10.10.1 第 1 步 · 先摸基线，不要先动手（约 10 分钟）

**为什么先摸基线**：没有基线，你后面所有的"改善了"都是感觉。而且这一步成本极低——四条命令。

```bash
# === 环境底座 ===
openclaw --version 2>&1 | tail -1
# 本机实测：OpenClaw 2026.9.6 (eb377ac)
# 本书统一口径：2026.9.4 (3a9d69d)

# === 库存三口径（务必分口径报数）===
cd ~/.openclaw/workspace/skills
echo "口径 A · 目录条目:      $(ls -1 | wc -l | tr -d ' ')"                        # 期望 238
echo "口径 B · 纯 skill 目录: $(($(find . -maxdepth 1 -type d | wc -l) - 1))"     # 期望 236
echo "口径 C · 含 SKILL.md:   $(find . -name SKILL.md | wc -l | tr -d ' ')"       # 期望 221

# === 合规三口径 ===
echo "含 name:    $(grep -l '^name:' */SKILL.md 2>/dev/null | wc -l | tr -d ' ')"   # 期望 192
echo "标 license: $(grep -l '^license:' */SKILL.md 2>/dev/null | wc -l | tr -d ' ')" # 期望 24
echo "无 SKILL.md: $(($(($(find . -maxdepth 1 -type d | wc -l) - 1)) - $(find . -name SKILL.md | wc -l)))"  # 期望 15
```

**记下这六个数，写进你的工作日志。** 它们是你后面所有动作的对照组。

### 10.10.2 第 2 步 · 把六个数字变成三张清单（约 15 分钟）

```bash
cd ~/.openclaw/workspace/skills

# 清单 1 · 无 SKILL.md 的目录（15 个：要么补，要么删）
for d in */; do d=${d%/}; [ -f "$d/SKILL.md" ] || echo "$d"; done > /tmp/list-no-entry.txt
wc -l /tmp/list-no-entry.txt

# 清单 2 · name 与目录名不一致（52 个：可自动修）
for d in */; do
  d=${d%/}
  n=$(grep -m1 '^name:' "$d/SKILL.md" 2>/dev/null | sed 's/^name:[[:space:]]*//;s/[[:space:]]*$//')
  [ -n "$n" ] && [ "$n" != "$d" ] && echo "$d|$n" || true
done > /tmp/list-mismatch.txt
wc -l /tmp/list-mismatch.txt

# 清单 3 · 缺触发词的 description（97 个：必须人写）
grep -L -E '当用户|使用场景|Use when|触发' */SKILL.md 2>/dev/null > /tmp/list-no-trigger.txt
wc -l /tmp/list-no-trigger.txt
```

**三张清单对应三种成本**：

| 清单 | 数量 | 成本类型 | 是否可自动化 |
|---|---|---|---|
| 无 SKILL.md | 15 | 决策（补还是删） | ❌ 需要你决定 |
| name 不一致 | 52 | 机械修改 | ✅ 脚本 |
| 缺触发词 | 97 | **认知劳动** | ❌ 只能人写 |

**只有第二种能批量做。** 这一步最重要的产出，不是三个文件，而是你清楚地知道：**这个库 80% 的问题是"没人写触发条件"，而这件事没有捷径。**

### 10.10.3 第 3 步 · 先修可自动修的（约 20 分钟，含备份）

```bash
# 0) 强制备份（真名：openclaw backup create）
openclaw backup create

# 1) dry-run
cd ~/.openclaw/workspace/skills
while IFS='|' read -r d n; do
  echo "FIX: $d/SKILL.md  '$n' -> '$d'"
done < /tmp/list-mismatch.txt | head -10

# 2) 逐个执行（保留前置备份；sed -i '' 为 macOS 语法）
while IFS='|' read -r d n; do
  f="$d/SKILL.md"
  cp "$f" "$f.bak-namematch"
  sed -i '' "s|^name:.*|name: $d|" "$f"
done < /tmp/list-mismatch.txt

# 3) 复算
for d in */; do
  d=${d%/}
  n=$(grep -m1 '^name:' "$d/SKILL.md" 2>/dev/null | sed 's/^name:[[:space:]]*//;s/[[:space:]]*$//')
  [ -n "$n" ] && [ "$n" != "$d" ] && echo "STILL: $d|$n"
done | wc -l        # 期望 0
```

**为什么这一步要留 `.bak-namematch`**：改名会打断跨 agent 声明与治理账本里的引用。留一份原文件，你才能在发现副作用时回滚。

### 10.10.4 第 4 步 · 给无入口文件的目录做决策（约 30 分钟）

15 个没有 `SKILL.md` 的目录，只有两种处置：

**处置 A · 它其实是有效内容，只是没写入口** → 补一个最小 SKILL.md：

```bash
d=<your-dir>
cat > "$d/SKILL.md" <<'YAML'
---
name: <与目录同名>
description: >-
  <一句话功能>。当用户<触发场景>时使用。
  不适用于<排除项>。
license: MIT
metadata:
  author: <你的名字/角色>
  version: "1.0"
---

# <人类可读标题>

## 用途
<为什么这个 skill 存在>

## 操作流程
1. <第一步>
2. <第二步>

## 边界
- 不适用于：<情况>
YAML
```

**处置 B · 它是废弃残留** → 移出索引：

```bash
mkdir -p ~/.openclaw/workspace/skills/_archive
mv "$d" ~/.openclaw/workspace/skills/_archive/
```

**关键纪律**：不要"先留着以后再说"。**留在索引里的废弃目录，每一次都会被当作候选能力参与判断——它不是在占磁盘，是在污染你的装载决策。**

### 10.10.5 第 5 步 · 认知劳动：重写 description（约 60–120 分钟）

这是整条路径里最慢、也最值钱的一步。97 个缺触发词的 skill，不可能一次写完。策略是**按使用频率分三批**：

| 批次 | 选谁 | 数量建议 | 标准 |
|---|---|---|---|
| 批 1 | 你上周真的用过的 | 5–10 个 | 场景 + 触发词 + 排除项，三要素齐 |
| 批 2 | 你的 agent 高频引用的 | 10–20 个 | 同上 |
| 批 3 | 剩下的 | 其余 | 只补触发语标记（最小成本） |

批 1 的写法模板：

```yaml
description: >-
  <它做什么，名词短语>。
  当用户<动词 + 宾语>、提到"<用户原话里的词1>/<词2>/<词3>"时使用。
  不适用于<最近的近邻技能做什么>。
```

**三个自检问题**（每一批都要过）：

1. 这条 description 打印出来，陌生人能否判断"什么时候翻出它"？
2. 它和你库里的其他 description 是否**一眼可区分**？
3. 触发词是从**用户的原话**里抄的，还是从**你的术语**里编的？

### 10.10.6 第 6 步 · 把三要素固化进模板（约 30 分钟）

到这一步你已经能总结出自己的模式了。把它变成一个**你自己的模板文件**，放在你写 skill 的地方（不要放在 skill 库里，它不是一个 skill）：

```markdown
<!-- ~/skill-template.md -->
---
name: <小写-连字符-等于目录名>
description: >-
  <功能>。当用户 <触发场景> 时使用。
  不适用于 <排除项>。
license: MIT
metadata:
  author: <owner>
  version: "1.0"
allowed-tools:            # 只在真的需要限制时保留
  - read_file
---

# <标题>

## 用途
## 操作流程
1.
## 边界（什么时候不要用我）
## 参考资料
- references/<file>.md
```

**为什么模板重要**：本章 97 个 `DESC_NO_TRIGGER` 的根因，不是作者不会写，而是**没有一个"必填触发条件"的位置**。模板把这件事从"记性"变成"结构"。

### 10.10.7 第 7 步 · 验证，并且留证据（约 20 分钟）

**TEV（Three-Evidence Verification，三证据验证）**：命令 + 输出 + 时间戳，三件齐。

```bash
# 证据 1 · 结构与格式
cd ~/.openclaw/workspace/skills
python3 - <<'PY'
import glob, re, sys
bad = []
for f in glob.glob('*/SKILL.md'):
    t = open(f, encoding='utf-8').read()
    if not t.startswith('---'):
        bad.append((f, 'NO_FRONTMATTER')); continue
    body = t.split('---', 2)[1]
    if not re.search(r'^name:', body, re.M): bad.append((f, 'NO_NAME'))
    if not re.search(r'^description:', body, re.M): bad.append((f, 'NO_DESC'))
    if not re.search(r'当用户|使用场景|Use when|触发', body): bad.append((f, 'NO_TRIGGER'))
print(f"检查 {len(glob.glob('*/SKILL.md'))} 个文件，问题 {len(bad)} 条")
for f, code in bad[:20]: print(f"  {code:14s} {f}")
PY

# 证据 2 · 真触发一次（不是"注册可见"，是"真的被装载"）
openclaw skills list | head -20
openclaw skills check --agent <your-agent> 2>&1 | tail -5

# 证据 3 · 落盘时间戳
date '+%Y-%m-%d %H:%M:%S' | tee /tmp/skill-audit-$(date +%Y%m%d).stamp
```

**为什么必须"真触发一次"**：`skills list` 只证明文件在。它不证明模型会在对的时候装载它。唯一能证明的方法，是在一次真实对话里让它触发，然后看行为是否按你的流程走。

### 10.10.8 一条时间线：两周能做到什么

| 天 | 动作 | 产出 |
|---|---|---|
| D1 | 第 1、2 步 | 六个数 + 三张清单 |
| D2 | 第 3 步 + 备份 | `NAME_DIR_MISMATCH` = 0 |
| D3–D4 | 第 4 步 | 15 个目录决策完毕（补 或 归档） |
| D5–D8 | 第 5 步（批 1 + 批 2） | 25–30 条高质量 description |
| D9 | 第 6 步 | 你自己的模板 |
| D10 | 第 7 步 | 证据三件套 + 新基线 |

**两周后的期望状态**：`NAME_DIR_MISMATCH = 0` · `NO_FRONTMATTER ≤ 5` · `DESC_NO_TRIGGER` 从 97 降到 60 以下 · 你有了一份带时间戳的基线报告。

**不期望的状态**：`DESC_NO_TRIGGER = 0`。因为它需要人写 97 条高质量描述——这大概是你一个月的工作量，而且**这不该是目标**。目标是"高频的 30 个已经写好了"，剩下 67 个允许慢慢来。

> **一条反 KPI 的纪律**：不要为了清零问题码而写空洞的 description。**一条"写着但没用"的 description，比一条缺失的更糟**——因为前者会让下一个维护者以为这件事已经处理完了。

---

## 10.11 常见误区：九个错误，和它们为什么特别容易犯

每一个误区都按四段写：**症状 → 为什么会犯 → 后果 → 30 秒自查**。

九个误区的共同根因只有一句话：**把"我写了"当成了"它会生效"。**

### 10.11.1 误区一 · 把 frontmatter 写成 JSON5

**症状**：

```markdown
---
{
  "name": "drift-audit",
  "description": "漂移审计"
}
---
```

**为什么会犯**：你刚读完第 11 章（Plugin 入口），记住了 `openclaw.plugin.json` 是 **JSON5**（允许注释、尾逗号、无引号键）。回到 skill 目录，手一滑就把同一套格式用上了。

**后果**：frontmatter 解析失败 → 该 skill 在能力层"不存在"。它会出现在文件列表里，但永远不会被装载。

**正确对照**：

| 层 | 文件 | 格式 |
|---|---|---|
| Skill（能力层） | `SKILL.md` | **YAML**（`---` 包裹） |
| Plugin（打包层） | `openclaw.plugin.json` | **JSON5** |

**30 秒自查**：

```bash
cd ~/.openclaw/workspace/skills
# 检查是否有 frontmatter 用 JSON 花括号开头的
for f in */SKILL.md; do
  sed -n '2p' "$f" | grep -q '^{' && echo "JSON-IN-YAML: $f"
done
```

---

### 10.11.2 误区二 · `name` 不符合规范（大小写 / 空格 / 与目录名不一致）

**症状**：`name: Drift Audit` / `name: DriftAudit` / `name: drift_audit` / 目录 `drift-audit` 而 name 是别的。

**为什么会犯**：`name` 在直觉上像"标题"。人会自然地把它写成好看的样子——首字母大写、加空格。但它是**标识符**，不是标题。标题在正文的 H1 里。

**后果**：本机实测 **52 个** `NAME_DIR_MISMATCH` + 综合违例 **55 个**。后果有三个层次：

1. 不同客户端行为不一致（有的拒绝加载，有得以目录为准，有的重复登记）；
2. 治理账本出现"同名两条"或"两条不同名实为一物"；
3. 跨 agent 声明（谁可以让位给谁）出现悬空引用。

**30 秒自查**：

```bash
cd ~/.openclaw/workspace/skills
for d in */; do
  d=${d%/}
  grep -m1 '^name:' "$d/SKILL.md" 2>/dev/null | grep -qv "^name: $d$" && echo "MISMATCH: $d"
done | wc -l      # 期望 0
```

**反面记忆法**：`name` 是门牌号，不是招牌。招牌（H1）可以花哨，门牌号必须规范。

---

### 10.11.3 误区三 · `description` 写成营销词（没有触发条件）

**症状**：

```yaml
description: 强大高效专业的智能助手工具，帮你处理各种复杂任务。
```

**为什么会犯**：这是最"自然"的写法。你在写一个能力简介，很自然会用能力简介的语气。但 `description` 不是简介，它是**检索键**。

**后果**：本机 **97 个** skill 命中 `DESC_NO_TRIGGER`——全库第一问题码，占 41%。这 97 个 skill 在能力层处于"存在但不可检索"状态。

**三要素改写公式**：

```yaml
description: >-
  <做什么，名词短语>。当用户<做什么动作>、提到"<用户原话词1>/<词2>"时使用。
  不适用于<近邻技能的领域>。
```

**30 秒自查**：把 description 单独粘贴给一个陌生人，问他"什么时候该用这个？"。如果他需要读第二遍或反问，就是没写好。

---

### 10.11.4 误区四 · 把 Skill 当 Plugin（往 SKILL.md 里塞代码 / 起进程）

**症状**：

```markdown
## 实现
```python
import subprocess
subprocess.run(["openclaw", "plugins", "enable", "my-plugin"])
```
```

或者：

```markdown
## 操作流程
1. 启动一个常驻进程监听 webhook
```

**为什么会犯**：你的真实需求是"让这件事自动发生"。写 skill 是最省力的路径——因为你手上正开着这个文件。但 **skill 不会自己运行**，它只在被装载时给模型看一段话。

**后果**：代码块被模型"脑补执行"（它可能真的去调用终端），行为不确定；而真正需要的确定性执行，反而失去了版本控制和失败处理。

**正确的升级路径**：

```text
需要"每次都被读到"      → 写进契约文件（SOUL / AGENTS）
需要"确定性执行"        → scripts/ 里的脚本，或升级为 Plugin（第 11 章）
需要"在正确情境下被装载" → SKILL.md
```

**30 秒自查**：

```bash
cd ~/.openclaw/workspace/skills
# 正文里出现 import / require / listen( / subprocess → 需要复核
grep -l -E 'subprocess|require\(|import |listen\(' */SKILL.md 2>/dev/null | wc -l
```

---

### 10.11.5 误区五 · 数字口径混用（238 / 236 / 221 / 192 混着报）

**症状**：同一份文档里，一处写"本机 238 个 skill"，另一处写"236 个"，再一处写"192 个"。

**为什么会犯**：这四个数是**四种口径**测出来的同一个东西：

| 数 | 口径 | 命令 |
|---|---|---|
| **238** | 目录条目（含 2 个非目录文件） | `ls -1 \| wc -l` |
| **236** | 纯 skill 目录 | `find . -maxdepth 1 -type d \| wc -l` − 1 |
| **221** | 含 `SKILL.md` 的目录 | `find . -name SKILL.md \| wc -l` |
| **192** | 含 `^name:` 字段的 | `grep -l '^name:' */SKILL.md \| wc -l` |
| **253** | agent 视角（含 agent 级注入） | `openclaw skills check --agent tiance` |

**后果**：任何一个"对比结论"都会崩掉。比如"覆盖率从 81% 提到 92%"——如果两次用了不同口径，这个结论完全无效。

**正确写法**：**命令 + 口径 + 日期，三件齐**。

> 本机 2026-09-27 实测：纯 skill 目录 **236** 个（`find . -maxdepth 1 -type d | wc -l` − 1），其中含 `SKILL.md` 者 **221** 个。

**30 秒自查**：在你的文档里搜 `/238|236|221|192|253/`，看每一个数字旁边有没有口径与日期。

---

### 10.11.6 误区六 · 宣称"Anthropic Skills 是私有规范"

**症状**：写"Anthropic Skills 是 Claude 的私有格式，其他平台不兼容"。

**为什么会犯**：这个说法在 **2025-12 之前**是对的。信息在行业里传播得比规范变化慢，很多调研报告、博客、教程还停留在旧结论上。

**事实**：

- **2025-10-16**：Anthropic 发布 Agent Skills。
- **2025-12-18**：格式开放为标准，由 `agentskills/agentskills`（Apache-2.0）维护，站点 agentskills.io。
- **2026**：约 40 个客户端/产品声明读取 `SKILL.md`；**2026-02** 起引入组织级管理。
- 2026-09-27 实拉：`agentskills/agentskills` 25 723★ / 1 944 forks；`anthropics/skills` 178 606★ / 21 137 forks。

**后果**：如果你认定它是私有的，你就不会去做跨平台分发（10.9），你会白白放弃"能力包可移植"这个 2026 年最大的结构性红利。

**30 秒自查**：任何出现"私有规范"字样的段落，都要能回答："这是在描述 2025-12 之前的状态吗？"

---

### 10.11.7 误区七 · 以为 `openclaw plugins install` 不存在

**症状**：写"OpenClaw 不支持插件安装"，或敲 `openclaw plugin install`（单数）得到 `command not found`，据此下结论。

**为什么会犯**：真名是 **复数** `openclaw plugins`。单数会失败，而且失败信息只是"找不到命令"——它不会提示你"你要找的是复数"。

**事实**：

```text
$ openclaw plugins --help
Commands: build / disable / doctor / enable / init / inspect / install / list
          / marketplace / pack / registry / search / uninstall / update / validate
```

**15 个子命令**，其中 `install` 支持 6 种源（path / archive / npm spec / git repo / clawhub:package / marketplace entry）。

**后果**：你会得出"OpenClaw 没有插件生态"的错误结论，并因此选错技术路线。

**30 秒自查**：

```bash
openclaw plugins --help 2>&1 | grep -c '^  [a-z]'   # 期望 ≥ 15
openclaw plugin 2>&1 | head -2                       # 期望报错（证明真名是复数）
```

---

### 10.11.8 误区八 · 破坏渐进式披露（把全部内容堆在 SKILL.md）

**症状**：`SKILL.md` 正文 900 行，没有 `references/`，没有 `scripts/`。

**为什么会犯**：写的时候是"一次写完最省事"；而且你确实需要那些内容。但你需要它们**在需要的时候可用**，不是**每次都在**。

**后果**：一旦命中，就吃掉 900 行窗口。命中率高的 skill 会变成性能杀手。

**正确做法**：

```text
第一层（SKILL.md 正文，≤ 200 行）  → 只写流程主线 + 指向
第二层（references/*.md）         → 细则、边界用例、完整清单
第三层（scripts/ assets/）        → 可执行 / 可复用夹具
```

**30 秒自查**：

```bash
cd ~/.openclaw/workspace/skills
for f in */SKILL.md; do printf "%5d %s\n" "$(wc -l < "$f")" "$f"; done | sort -rn | head -10
```

超过 300 行的，都该做一次"主线 / 细节"切分。

---

### 10.11.9 误区九 · 以为"skill 写好了，agent 就会用"

**症状**：文件写完了、`openclaw skills list` 也能看到，于是宣布上线。

**为什么会犯**：这是最本质的一个误区，因为它混淆了"注册可见"和"真被装载"。前者是文件系统事实，后者是运行期行为。

**后果**：一周后你发现 agent 还在用默认行为处理那些本该走 skill 的事情，而你以为是"模型不行"。

**真正的验证路径（三级）**：

| 级 | 验什么 | 命令 | 能证明 |
|---|---|---|---|
| L1 | 文件在 | `ls` | 文件存在 |
| L2 | 注册可见 | `openclaw skills list` | 系统识别到了 |
| L3 | **真被装载** | 在真实对话里让它触发 → 看行为 | **能力可用** |

**只有 L3 是有效验证。** 这也是本书对 TEV（三证据验证）的要求：命令 + 输出 + 时间戳，"注册可见"不构成证据。

**30 秒自查**：你能不能举出"昨天有一个任务，明确走的是某个 skill 的流程"这个具体例子？举不出来，就还没验证过。

---

### 10.11.10 九个误区的一页速查

| # | 误区 | 根因 | 本机暴露度 | 可自动化 |
|---|---|---|---|---|
| 1 | frontmatter 写 JSON5 | 与 plugin 格式混淆 | 少量 | ✅ 检测 |
| 2 | `name` 违例 | 把标识当标题 | **52** | ✅ 修复 |
| 3 | description 无触发条件 | 把检索键当简介 | **97** | ❌ 人写 |
| 4 | 往 SKILL.md 塞代码 | 需求其实是"确定性执行" | 少量 | ✅ 检测 |
| 5 | 数字口径混用 | 四口径同名 | 高频 | ✅ 规范 |
| 6 | 称 Anthropic Skills 私有 | 2025-12 前的旧结论 | 中 | ❌ 认知 |
| 7 | 认为 `plugins install` 不存在 | 单复数 | 中 | ✅ 命令验证 |
| 8 | 破坏渐进式披露 | 一次写完最省事 | 中 | ✅ 检测 |
| 9 | 以为"写好了就会用" | 混淆注册与装载 | **普遍** | ❌ 必须实测 |

**最后一条纪律**：这九个误区的共同结构是"**局部正确、整体失效**"。每一个做法单独看都说得通，但它们都忽略同一件事——**装载发生在你不在场的时候**。你写的每一个字，最终都要在一个你看不见的判断里被使用。

---

## 10.12 深度专题

### 10.12.1 专题一 · 2026 前沿追踪：Agent Skills 从发布到标准

#### 一、时间线（四个必须记住的日期）

| 日期 | 事件 | 为什么重要 |
|---|---|---|
| **2025-10-16** | Anthropic 发布 **Agent Skills**：以「目录 + `SKILL.md`」承载领域知识与工作流 | 能力封装从"函数/协议"退回"文本"，范式确立 |
| **2025-12-18** | 格式开放为**独立标准**，由 agentskills.io（`agentskills/agentskills`，Apache-2.0）维护 | 从"一家公司的格式"变成"公共规范"，这是可移植性的法律与技术前提 |
| **2026（全年）** | 约 **40 个**产品/客户端声明读取 `SKILL.md` | 生态规模：从两三个客户端扩到跨厂商 |
| **2026-02 起** | 引入**组织级管理**（组织内发布 / 审批 / 下架 skill，不再只靠个人目录） | 从"个人技巧"变成"可治理的组织资产" |

补充的仓库元数据（**2026-09-27 GitHub API 实拉**）：

| 仓库 | stars | forks | License | 备注 |
|---|---|---|---|---|
| `anthropics/skills` | **178 606** | 21 137 | NOASSERTION | 一手定义者 / 样例集合 |
| `agentskills/agentskills` | **25 723** | 1 944 | Apache-2.0 | 规范维护者；open_issues 91；size 782 KB |

> **关于两个仓库 created_at 的口径**：`anthropics/skills` 仓库首次提交早于 2025-10-16（建仓与发布不是同一天），`agentskills/agentskills` 建仓早于 2025-12-18。**引用时请分别标注"建仓日"与"发布/开放日"，不要混为一个日期。**

#### 二、三级渐进披露：这次范式迁移的技术核心

Agent Skills 能被业界接受，不是因为"用 Markdown 写文档"这件事新鲜——那件事 2023 年就有人在做了。它被接受，是因为**渐进式披露（Progressive Disclosure）**这一个机制，把"持有几百个能力"从不可能变成了可能。

三层：

```text
L1 索引层（常驻）      name + description          ← 几百条，成本极低
L2 正文层（按需装载）    SKILL.md 正文               ← 被命中时才进窗口
L3 参考层（按需读取）    references/ scripts/ assets ← 正文显式指向时才读
```

**为什么它是"核心"而不是"优化"**：在没有分层的情况下，能力库的规模上限由上下文窗口决定（几十个量级）。引入分层后，上限由 `description` 的质量决定，而不是由内容总量决定。**这是一个量级的变化：从"几十个能力"到"几百上千个能力"。**

这也是本章 10.3 把它列为独立核心概念的原因——它不是实现细节，它是这件事成立的前提。

#### 三、约 40 个兼容产品意味着什么

生态规模带来三个具体后果：

1. **能力包变成资产而不是负债。** 你为 OpenClaw 写的 skill，在 Gemini CLI / OpenCode / OpenHands / ZeroClaw 上是同一份物料。
2. **skill 的质量标准开始外部化。** 当几十个客户端都读同一份 `description` 时，"描述写得好不好"变成一个可被跨组织比较的东西。
3. **格式治理成为公共议题。** 这也是 2026-02 引入组织级管理的直接动因：当 skill 成为组织资产，"谁能发布、谁能下架、谁负责审计"就必须有答案。

#### 四、2026-02 组织级管理：从个人技巧到组织资产

这一条对本书读者尤其重要，因为它和第 4 章（长期表现）的**漂移治理（Drift Governance）**、第 5 章（治理系统）的 TEV（Three-Evidence Verification，三证据验证）是同一个问题的不同层：

| 层 | 治理对象 | 机制 |
|---|---|---|
| Agent 行为层（第 4 章） | agent 是否偏离契约 | 漂移治理 + 每周体检 |
| Skill 资产层（本章） | 能力是否还成立 | 组织级发布/审批/下架 + 本章 10.7 生命周期 |
| 分发层（第 11 章） | 打包产物是否可信 | capability 确权 + ClawHub |

**组织级管理出现之前，skill 的治理只能靠"目录约定"；出现之后，它获得了与代码同级的治理地位。** 这是 2026 年最值得跟踪的一条演进线。

#### 五、前沿跟踪的纪律

本章涉及的所有前沿事实，引用规则是：

- ✅ **可直接引用**：2025-10-16 发布 / 2025-12-18 开放标准 / 约 40 客户端 / 2026-02 组织级管理 / 两个仓库的 stars·forks·License（2026-09-27 实拉）
- ⏳ **必须保留 ⏳**：跨框架互通的行为一致性验证（同一 skill 在 ≥3 个客户端的装载行为是否一致）
- ❌ **不得写入**：未经验证的版本号传闻、"某框架市场份额 X%"、把 2024 年及更早的知识冒充 2026 进展

---

### 10.12.2 专题二 · 六大框架对位表：谁能承载"训练学"

#### 一、对位口径

本节对位的对象是业界 **6 个主流 Agent 框架**：

**LangGraph · AutoGen（AG2）· CrewAI · Claude Agent SDK · OpenAI Agents SDK · LlamaIndex**

对位的维度不是"谁更强"，而是四个具体问题：

1. 它的能力单元是什么形态？（代码 / JSON / 文本）
2. 能力如何在运行期被**发现**？
3. 能力如何被**分发**到别的环境？
4. 有没有"能力库治理"这一层？

#### 二、主对位表

| 维度 | **Agent Skills 标准 + OpenClaw（本章）** | LangGraph | AutoGen (AG2) | CrewAI | Claude Agent SDK | OpenAI Agents SDK | LlamaIndex |
|---|---|---|---|---|---|---|---|
| **能力单元形态** | **目录 + `SKILL.md`（自然语言 + YAML）** ⚡ | Python 函数 / `@tool` | JSON function schema | 装饰器 + 注册表 | `SKILL.md`（同标准） | 函数 + schema | `ToolSpec` / 函数 |
| **发现机制** | **渐进式披露三层**（L1 常驻 / L2 按需 / L3 深读）⚡ | 代码注册（import 即注册） | 注册到 GroupChat 的 schema 表 | 注册表（进程内） | 同标准三层 | 代码注册 | 代码注册 / 索引检索 |
| **分发单位** | **目录（可 tar / 可跨平台）** ⚡ | Python 包 | Python 包 | Python 包 | 目录（同标准） | Python 包 | Python 包 |
| **是否需要写代码** | **否**（写 Markdown 即可）⚡ | 是 | 是 | 是 | 否 | 是 | 是 |
| **跨平台可移植** | **约 40 个客户端** ⚡ | 仅 Python 生态 | 仅 Python 生态 | 仅 Python 生态 | 同标准 | 仅 OpenAI 生态 | 仅 Python 生态 |
| **能力库治理层** | **组织级管理（2026-02 起）** ⚡ | 无（靠包管理） | 无 | 无 | 有（同标准） | 无 | 无 |
| **触发条件声明位置** | **`description`（装载前可判）** ⚡ | 代码注释 / docstring | JSON description | 装饰器 docstring | `description` | docstring | docstring |
| **装载决策可见性** | **可观测（L1 索引可打印）** ⚡ | 不可观测 | 不可观测 | 不可观测 | 可观测 | 不可观测 | 部分 |
| **与 OpenClaw 关系** | ● 本章基准 | ○ 互补（编排层） | ○ 互补（编排层） | ○ 互补（角色层） | ● 同标准 | ○ 互补 | ○ 互补（检索层） |

> 图例：● 重叠 / ⚡ 领先 / ○ 互补或空白

#### 三、逐条解读

**① 唯一的形态差异是"文本 vs 代码"。**

前三个框架（LangGraph / AutoGen / CrewAI）的能力单元是**代码**。这意味着：写一个能力的人必须是工程师；能力的分发单位是包；能力的治理归包管理。

Agent Skills 的形态是**文本**。意味着：写能力的人可以是领域专家；分发单位是目录；治理需要新机制（于是有了组织级管理）。

**这不是"谁先进"的问题，而是"谁能承载哪一类知识"的问题。**

- 确定性逻辑 → 代码形态更好（可测试、可版本化、可静态检查）
- 情境化判断 → 文本形态更好（代码写不出来）

**② 分发单位决定了能力能不能出门。**

Python 包只能在 Python 生态内分发，且依赖版本必须匹配。目录可以在任何客户端分发，零依赖（因为内容是文本）。

**③ "触发条件声明位置"是被低估的差异。**

在代码形态里，"这个能力什么时候该用"散落在 docstring、注释、README 里，**没有任何机制保证它在装载前被读到**。

Agent Skills 把触发条件强制放进 frontmatter 的 `description`——它成为**规范的一部分**，而不是文档的自觉。

这个差异的后果直接体现在本机的数字上：**97 个 skill 命中 `DESC_NO_TRIGGER`**。也就是说，即使标准强制了这个位置，人还是会写得不合格。如果连位置都没有，情况只会更差。

**④ 六大框架的空白处，正是本书的位置。**

回头看这张表最关键的一列——"能力库治理层"：

- LangGraph / AutoGen / CrewAI / OpenAI Agents SDK / LlamaIndex：**无**（靠各自语言的包管理）
- Agent Skills 标准 + OpenClaw：**有**（2026-02 组织级管理 + 本章 10.7 生命周期）

> **一句话**：六大框架提供**容器**，Agent Skills 提供**内容格式**，而本书提供**内容**。三者不冲突——一个团队完全可以同时用 LangGraph 做编排、用 Agent Skills 组织知识、用 OpenClaw 作为运行底座。

**⑤ 与 v4.0 对位表的关系**：下面这张表是本章的**局部重做版**（聚焦"能力单元形态"一个维度）；旧版六框架大表的其余维度仍在 `./_industry-frontier-tracking.md` §1 / §2.10 中维护，两者不冲突——本表只声明本章范围内的判断。

#### 四、把训练学放进这张表

| 训练学组件 | 最佳承载形态 | 理由 |
|---|---|---|
| 七大契约（SOUL / AGENTS / …） | **契约文件**（always-on） | 必须永远在场，不能被"按需" |
| 双三角 / 教练机制 | **SKILL.md** | 情境化判断 |
| 漂移治理 / 每周体检 | **SKILL.md + scripts/** | 判断在文本，例行任务在脚本 |
| 三省制 / Trust Score | **SKILL.md + Plugin hook** | 流程在文本，计分在代码 |
| 报价闸门 / 合规红线 | **Plugin（强制）** | 不能接受"偶尔不生效" |
| OODA 自主目标生成 | **SKILL.md + Plugin** | 触发在文本，执行在代码 |

**这张表是本章最有实操价值的一页**：它把"训练学要落地"这个模糊目标，拆成了"哪一部分该用哪种形态"的具体分配。

---

### 10.12.3 专题三 · 本机实测审计（236 skill 真实体检）

> 本节全部数字来自本机 2026-09-27 实跑；测量脚本见 `_appendix-api/scripts/check-skill-frontmatter.py`；完整 API 口径见 `_appendix-api/06-skill-manifest-reference.md`。

#### 一、体检总表

| # | 指标 | 实测值 | 口径 / 命令 |
|---|---|---|---|
| 1 | 目录条目 | **238** | `ls ~/.openclaw/workspace/skills/ \| wc -l`（含 2 个非目录条目） |
| 2 | **纯 skill 目录** | **236** | `find . -maxdepth 1 -type d \| wc -l` − 1 |
| 3 | 含 `SKILL.md` | **221** | 存在性检查（**15 个目录无入口文件**） |
| 4 | 无 frontmatter | **47**（存在性口径）/ **28**（问题码口径） | 两口径并存，引用须标注 |
| 5 | `name` 违例 | **55** | 小写+连字符不满足或 ≠ 父目录名 |
| 6 | 含 `name:` 字段 | **192** | `grep -l '^name:'` → **44 个连 name 都没有** |
| 7 | 标 `license` | **24 / 236（10%）** | `grep -l '^license:'` |
| 8 | **无 error 目录** | **48** | 审计脚本实跑（**≠ 合格 48 个**） |
| 9 | warn / error / info | **86 / 101 / 1** | 审计脚本实跑 |
| 10 | 问题码 Top 1 | `DESC_NO_TRIGGER` **97** | description 缺触发语 |
| 11 | 问题码 Top 2 | `DESC_SHORT` **56** | description 过短 |
| 12 | 问题码 Top 3 | `NAME_DIR_MISMATCH` **52** | 与第 5 项呼应 |
| 13 | `NO_FRONTMATTER` | **28** | `---` 不在第 1 行或缺失 |
| 14 | **6/6 字段全覆盖** | **0** | 逐字段核对 |
| 15 | 5/6 字段（最高档） | **11** | 逐字段核对 |
| 16 | agent 视角总数 | **253** | `openclaw skills check --agent tiance` |
| 17 | 底座版本 | `OpenClaw 2026.9.6 (eb377ac)` live / `2026.9.4 (3a9d69d)` 书内口径 | `openclaw --version` |

#### 二、三个必须诚实说明的地方

**（一）`ok: 48` ≠ "48 个合格"。**
脚本语义是"该目录**没有 error 级问题**"。而 6/6 字段全覆盖的样本数是 **0**。把 48 当成"合规数"会严重高估现状。

**（二）两个"无 frontmatter"数字不矛盾。**
`47` = 有 `SKILL.md` 但首个 `---` 块不存在或不合法（API 附录口径，直接逐目录判定）；`28` = 本次审计运行命中的 `NO_FRONTMATTER` 问题码数。**两者是不同脚本、不同路径的计数**，不是同一个东西的两次不一致测量。引用时必须带口径。

**（三）`Total 253 > 236` 是正常的。**
`openclaw skills check --agent tiance` 走的是 **agent 视角**——包含 `~/.openclaw/workspace/agents/<agent>/skills/` 下的 agent 级注入 skill。**全局池 ≠ 某个 agent 实际持有。** 做治理时以 agent 视角为准。

#### 三、从数字到动作：优先级排序

| 优先级 | 问题码 | 数量 | 动作 | 可自动化 |
|---|---|---|---|---|
| **P0** | `DESC_NO_TRIGGER` | 97 | 按"高频优先"分三批重写 description（10.10.5） | ❌ 必须人写 |
| **P1** | `NAME_DIR_MISMATCH` | 52 | 批量 `sed` 对齐（含备份） | ✅ |
| **P1** | `NO_FRONTMATTER` | 28 | 生成骨架 → 人补 description | ⚠ 半自动 |
| **P2** | 无 `SKILL.md` 的目录 | 15 | 补 OR 归档到 `skills/_archive/` | ❌ 需决策 |
| **P2** | 缺 `license` | 212 | 批量补 `license: MIT`（若你确实是 MIT） | ✅ |
| **P3** | `DESC_SHORT` | 56 | 扩充到"场景+触发词+排除项"三要素 | ⚠ 半自动 |

**为什么 `DESC_NO_TRIGGER` 排 P0**：它是唯一一个"数量最大 + 完全不可自动化 + 直接影响装载命中"的问题。P1 的两项各占 52 / 28，加起来还没它多，而且能被脚本处理。

#### 四、可复现脚本（一次跑完，出全表）

```bash
#!/usr/bin/env bash
# skill-audit.sh — 本章体检的最小可复现实现
# 实测环境：OpenClaw 2026.9.6 (eb377ac) · macOS 26.5.1
set -u
cd ~/.openclaw/workspace/skills

ENTRIES=$(ls -1 | wc -l | tr -d ' ')
DIRS=$(( $(find . -maxdepth 1 -type d | wc -l) - 1 ))
WITHSKILL=$(find . -name SKILL.md | wc -l | tr -d ' ')
WITHNAME=$(grep -l '^name:' */SKILL.md 2>/dev/null | wc -l | tr -d ' ')
WITHLIC=$(grep -l '^license:' */SKILL.md 2>/dev/null | wc -l | tr -d ' ')
NOTRIG=$(grep -L -E '当用户|使用场景|Use when|触发' */SKILL.md 2>/dev/null | wc -l | tr -d ' ')
MISMATCH=0
for d in */; do
  d=${d%/}
  n=$(grep -m1 '^name:' "$d/SKILL.md" 2>/dev/null | sed 's/^name:[[:space:]]*//;s/[[:space:]]*$//')
  [ -n "$n" ] && [ "$n" != "$d" ] && MISMATCH=$((MISMATCH+1))
done

echo "=== skill-audit $(date '+%Y-%m-%d %H:%M:%S') ==="
echo "底座版本:        $(openclaw --version 2>&1 | tail -1)"
echo "口径A 目录条目:   $ENTRIES        (期望 238)"
echo "口径B 纯skill目录: $DIRS          (期望 236)"
echo "口径C 含SKILL.md:  $WITHSKILL     (期望 221)"
echo "口径D 含name:      $WITHNAME      (期望 192)"
echo "口径E 标license:   $WITHLIC       (期望 24)"
echo "口径F 无触发词:    $NOTRIG        (期望 ~97)"
echo "口径G name不一致:  $MISMATCH      (期望 52)"
echo "口径H agent视角:   $(openclaw skills check --agent tiance 2>/dev/null | grep -i total | tail -1)"
```

**把这份脚本存进你的仓库，每月跑一次，把输出追加到一个日志文件。** 一年之后，你会拥有一份"能力库演化史"——这是任何审计打分都换不来的东西。

---

### 10.12.4 专题四 · 诚实边界

#### ✅ 已实测（可直接引用）

| # | 事实 | 证据 |
|---|---|---|
| 1 | 本机 skill 目录 **236**（条目 238，含 2 个非目录） | `ls` / `find` 实跑 |
| 2 | 含 `SKILL.md` **221**（15 个目录无入口文件） | 存在性检查实跑 |
| 3 | 含 `name:` **192**；标 `license` **24** | `grep -l` 实跑 |
| 4 | 审计分布 ok 48 / warn 86 / error 101 / info 1 | 审计脚本实跑 |
| 5 | `DESC_NO_TRIGGER` 97 · `DESC_SHORT` 56 · `NAME_DIR_MISMATCH` 52 · `NO_FRONTMATTER` 28 | 审计脚本实跑 |
| 6 | 6/6 字段全覆盖 = **0**；最高档 5/6 = **11** | 逐字段核对 |
| 7 | `openclaw skills check --agent tiance` → Total **253** | 命令实跑 |
| 8 | `openclaw --version` = **2026.9.6 (eb377ac)** | 命令实跑 |
| 9 | `openclaw plugins --help` = **15 子命令** | 命令实跑 |
| 10 | `anthropics/skills` 178 606★ / `agentskills/agentskills` 25 723★ | GitHub API 2026-09-27 实拉 |
| 11 | Agent Skills 2025-10-16 发布 · 2025-12-18 开放标准 · 约 40 客户端 · 2026-02 组织级管理 | 前沿追踪文件 + 规范站点 |

#### ⏳ 待验证（引用时必须保留 ⏳）

| # | 事项 | 为什么还没验证 |
|---|---|---|
| 1 | `npx skills-ref validate <dir>` 的实际输出 | 本机未安装官方校验工具 |
| 2 | 同一 skill 在 ≥3 个客户端上的**装载行为一致性** | 未做跨客户端实测；本章只声称"格式兼容" |
| 3 | `~/.openclaw/workspace/agents/<agent>/skills/` 的逐 agent 数量分布 | 仅取了 tiance 一个样本（Total 253） |
| 4 | 组织级管理（2026-02）在 OpenClaw 侧的对应实现 | 无对应本机验证 |
| 5 | 全库第一层正文长度的完整分布 | 仅抽样排序 |

#### ⚠ 不得宣称（写了就是错）

| # | 不得写 | 正确表述 |
|---|---|---|
| 1 | "Anthropic Skills 是私有规范" | 已于 2025-12-18 开放为标准（agentskills.io，Apache-2.0） |
| 2 | "OpenClaw 不支持插件安装" / "`openclaw plugin install` 不存在" | 真名是复数 `openclaw plugins`（15 子命令，`install` 支持 6 种源） |
| 3 | "6/6 字段全覆盖有 48 个" | `ok: 48` = 无 error 目录；6/6 全覆盖 = **0** |
| 4 | "本机 238 个 skill" | 238 是**目录条目**口径；纯 skill 目录 = **236** |
| 5 | "本机 skill 合规率 81%"（单一数字，不带口径） | 必须写成"含量化口径 + 命令 + 日期"的三件套 |
| 6 | "训练学已生成 28 个 SKILL.md" | 那是**可行性结论/预计**（8 卷中 7 卷可 Skill 化），不是已完成产物 |
| 7 | "Skill 和 Plugin 是一回事" | Skill = 单文件能力包（Markdown · 跨平台）；Plugin = 启动时加载的工程产物（JSON5 + Code） |
| 8 | 把 `~/.openclaw/workspace/openclaw.json` 当主配置 | 真名是 **`~/.openclaw/openclaw.json`** |
| 9 | "OpenClaw 本机版本 2026.9.4" | 2026.9.4 是**书内统一口径**；本机 live 为 2026.9.6 (eb377ac)——两个数都要说清 |

#### 最后一段：这一章真正想留下的

如果本章只能留下一句话，它是：

> **能力层的全部价值，不取决于你写了多少行，而取决于 agent 在对的时候，能不能找到它。**

而这句话有一个必然的推论：**你写的每一份 SKILL.md，都要假设它的读者不在场、不了解背景、只有 30 个词可以看。**

这不是写作技巧，这是工程约束。

---

### 10.12.5 术语双写锚点（本章统一写法）

本章所有术语一律采用「中文新名（English alias，原：旧称）」的双写形式。锚点如下：

| 术语 | 本章统一双写形式 | 相关节 |
|---|---|---|
| 技能注册表 | Skill Registry（技能注册表） | 10.0.2 / 10.7 |
| 渐进式披露 | Progressive Disclosure（渐进式披露） | 10.0.3 / 10.3 |
| 可复用能力单元 | Reusable Capability Unit（可复用能力单元） | 10.1 / 10.5 |
| 技能基因 | Skill Gene（技能基因；对外须加英文全称） | 10.1 |
| 智能体集群 | Agent Fleet（智能体集群，原：军团） | 10.0.1 / 10.7 |
| 监督层 | Supervisor Layer（监督层，原：监军） | 10.7 |
| 漂移治理 | Drift Governance（漂移治理） | 10.7 |
| 主动性边界三档 | Autonomy Boundary Triad（主动性边界三档，原：三档制） | 10.12.2 |
| 响应让渡协议 | Response Yield Protocol（响应让渡协议，原：让位协议） | 10.12.2 |
| 任务交接协议 | Task Handover Protocol / THP（任务交接协议） | 10.12.2 |
| 三证据验证 | Three-Evidence Verification / TEV（三证据验证，原：三证验真） | 10.7 / 10.10.7 |
| 修复工单 | Remediation Ticket（修复工单，原：整改单） | 10.7 |
| 多智能体编排 | Multi-Agent Orchestration（多智能体编排，原：军团编制） | 10.0.1 / 10.10 |
| 工具白名单 | allowed-tools（工具白名单） | 10.6 |

---

---

## 附录 A · 本章操作手册（原「SOP · 本章怎么用」节后移 · 一字未删）

> ⚠ **本区块 = 章末后移的原文操作手册与附件**（逐字保留，未作任何删改）。
> 其中出现的历史章号字样（如「第 11 章」）属于章号统一前口径；**本书现行章号以文件首行为准——本章 = 第 10 章 = 路径 `chapters/10-skill-registry/`**。
> 这里的数字口径、命令真名与正文完全一致；只想马上动手的读者可直接从下方「步骤 1」开始。

## SOP · 本章怎么用

> **实测环境**：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27 · macOS 26.5.1 · 本机 **236 skills** 已盘点 · 其中 **192 个含 `^name:` YAML frontmatter（82%）**
> **本章定位**：v5.0 行业标准版 · 第 11 章（路径 `11-skill-registry`）· Skill 注册：对齐 Agent Skills 开放标准（接口层 3/4 · 能力层接入）
> **预计用时**：速读 25 分钟 · 工程读 55 分钟 · 全读 80 分钟
> **前置依赖**：第 9 章 MCP 绑定 / 第 10 章 A2A 绑定（接口层 1-2/4）概念已建立；理解"Skill = 单个 SKILL.md 文件"

### 步骤 1 · 读完本章需要什么

**前置章节**：
- 第 10 章 · A2A 绑定（接口层 2/4，理解"能力如何被外部协议发现"）→ `chapters/09-a2a-binding/09-A2A绑定.md`
- 第 12 章 · Plugin 入口（接口层 4/4，理解"Skill 是 Plugin 的构成单元"）→ `chapters/11-plugin-entrypoint/README.md`

**前置文件**：
- `~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/00-术语对照表·v3.0行业标准版.md`（35 条改名表，本章引用 #17 技能基因→Skill Gene / Reusable Capability Unit）
- 本章同目录 6 文件：`README.md`（本文件）/ [`SKILL.md-frontmatter-规范.md`](./SKILL.md-frontmatter-规范.md) / [`8卷Skill写法适配.md`](./8卷Skill写法适配.md) / [`Anthropic-Skills-实拉对位.md`](./Anthropic-Skills-实拉对位.md) / [`Registry-表.md`](./Registry-表.md) / [`真名验证与勘误.md`](./真名验证与勘误.md)

**前置命令**：
```bash
# 验证 OpenClaw 版本（Skill 结构基于此版本）
openclaw --version 2>&1 | tail -1
# 期望：OpenClaw 2026.9.4 (3a9d69d)

# 本机 skills 真实盘点（SOP 引用 236 skills 的实测基线）
ls ~/.openclaw/workspace/skills/ | wc -l
# 期望：≈ 238（含 2 个非目录文件）；纯 skill 目录 = 236

# 本机 YAML frontmatter 覆盖率
grep -l '^name:' ~/.openclaw/workspace/skills/*/SKILL.md 2>/dev/null | wc -l
# 期望：192（本机 2026-09-27 实测，即 192/236 ≈ 82%）
```

### 步骤 2 · 必做的 3 件事

**1. 数你自己的 skill 库存 + frontmatter 覆盖率（先摸清现状）**

本章 11.4 的核心判断是"OpenClaw 结构上兼容 Agent Skills，只是覆盖不全（192/236）"。**先在你本机复算一遍这两个数**——这决定了你要不要批量补 frontmatter。

```bash
# 复制粘贴：一次性算出"总数 / 有 frontmatter 数 / 覆盖率"
cd ~/.openclaw/workspace/skills
TOTAL=$(find . -maxdepth 1 -type d ! -name skills | wc -l | tr -d ' ')
WITHFM=$(grep -l '^name:' */SKILL.md 2>/dev/null | wc -l | tr -d ' ')
echo "skills 总数: $TOTAL  含 frontmatter: $WITHFM  覆盖率: $((WITHFM*100/TOTAL))%"
# 期望（本机 2026-09-27）：skills 总数: 236  含 frontmatter: 192  覆盖率: 81%
```

**2. 写一个最小 SKILL.md（11.5 Step 2 的 6 字段模板）**

Agent Skills 的核心是 `SKILL.md` + YAML frontmatter。11.2 节列了官方 6 字段规范。**照抄下面模板改 `name`/`description` 就能落地一个合规 skill**（本文件 11.5 节给了完整示例）。

```bash
# 复制粘贴：创建你自己的第一个合规 skill
mkdir -p ~/.openclaw/workspace/skills/silicon-life-double-triangle
cat > ~/.openclaw/workspace/skills/silicon-life-double-triangle/SKILL.md <<'YAML'
---
name: silicon-life-double-triangle
description: 双三角模型训练法（Dual-Triangle Model: Expectation-Actuality-Feedback Loop）。
  适用于训练硅基 agent 从响应型过渡到提案型。
license: MIT
metadata:
  author: openclaw-silicon-life-handbook
  version: "1.0"
---

# 双三角模型训练法（silicon-life-double-triangle）

## 训练目标
让 agent 学会自主生成期望值（Expectation），而不是等用户给指令。

## 操作流程
1. Observe 当前对话上下文
2. Orient 自身期望与用户期望的差值
3. Decide 是否提出 Proposition
4. Act 提交 Proposition，等待反馈
YAML

# 验证 frontmatter 被解析
grep -A1 '^name:' ~/.openclaw/workspace/skills/silicon-life-double-triangle/SKILL.md
# 期望：name: silicon-life-double-triangle
```

**3. 对照 `Registry-表.md`，把你自己的 skill 登进 Registry**

11.7 节澄清了 Skill（能力层）vs Plugin（分发层）的边界。**Skill Registry 是"能力目录"**——把你刚创建的 skill 按 `skill_id / owner / status / version` 登进本章的 Registry 表。

```bash
# 导出 Registry 表头（供你追加自己的一行）
head -30 ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/chapters/10-skill-registry/Registry-表.md
# 期望：能看到 skill_id/owner/status/version 等列定义 + 9 个既有 skill
```

### 步骤 3 · 检查清单

- [ ] **版本验证**：`openclaw --version` ≥ 9.4（Skill 结构基于 9.4）
- [ ] **库存复算**：本机 skill 总数与 frontmatter 数已复算（本机基线 236 / 192 / 81%）
- [ ] **最小 SKILL.md 落盘**：`~/.openclaw/workspace/skills/silicon-life-double-triangle/SKILL.md` 存在且 `^name:` 可被 grep 命中
- [ ] **6 字段齐**：你的 SKILL.md frontmatter 至少含 `name` / `description` / `license` / `metadata.author` / `metadata.version`（详见 `SKILL.md-frontmatter-规范.md`）
- [ ] **Registry 已登记**：你的 skill 已按 `skill_id/owner/status/version` 追加到 `Registry-表.md` 风格的表里
- [ ] **术语规范**：用"可复用能力单元（Reusable Capability Unit）"作 Skill 的对外全称；"技能基因"（Skill Gene）属内部保留昵称，对外首次出现加英文全称
- [ ] **勘误已读**：本章 11.3 的 3 条重大勘误（`plugins install` 存在 / agentskills.io 是开放标准 / 192-236 兼容）已读并接受

### 步骤 4 · 常见错误（缩略版 · 完整版看 FAQ 卷）

- ❌ **不要说 Anthropic Skills 是"私有规范"**——**agentskills.io（agentskills/agentskills）2025-12 已把它开放为标准**（Apache-2.0 · GitHub 2026-09-27 实拉 25 723 stars）——这是 v5.0 的第一条重大勘误（11.3 表 #2）
- ❌ **不要说 `openclaw plugins install` 不存在**——**它存在**（plural 命令集，支持 path/archive/npm/git/clawhub/marketplace 6 种源）——第二条重大勘误（11.3 表 #1）
- ❌ **不要把"28 个 SKILL.md 全量生成"当既成事实**——11.6 是**可行性结论**（8 卷中 7 卷可 Skill 化，**预计**生成 28 个），不是已完成产物
- ❌ **不要把 Skill 和 Plugin 混为一谈**——Skill = 单文件"剧本"（Markdown · 跨平台）；Plugin = "剧组"（JSON5 + Code · 启动时加载 · 仅 OpenClaw）——边界见 11.7 表
- ❌ **不要给 SKILL.md 用 JSON5 写 frontmatter**——SKILL.md frontmatter 是 **YAML**（`---` 包裹）；JSON5 是 Plugin 的 `openclaw.plugin.json` 格式（第 12 章）
- ✅ **应该做**：skill 的 `description` 写清"什么时候该触发"——它决定 agent 的**渐进式披露（Progressive Disclosure）**能否命中
- ✅ **应该做**：优先给**你自己的存量 skill** 补 `^name:` frontmatter（本机 44 个缺 frontmatter 的 skill 都能补），而不是另起炉灶写新 skill

### 步骤 5 · 做完怎么验

```bash
# === 验证 1：版本正确 ===
openclaw --version 2>&1 | tail -1
# 期望：OpenClaw 2026.9.4 (3a9d69d)

# === 验证 2：你的 skill 落盘 + 可被 grep 命中 ===
test -f ~/.openclaw/workspace/skills/silicon-life-double-triangle/SKILL.md \
  && echo "✓ SKILL.md exists" || echo "❌ missing"
grep -q '^name:' ~/.openclaw/workspace/skills/silicon-life-double-triangle/SKILL.md \
  && echo "✓ frontmatter name 命中" || echo "❌ invalid frontmatter"

# === 验证 3：本机覆盖率复算（对照章节 192/236）===
cd ~/.openclaw/workspace/skills
echo "含 frontmatter: $(grep -l '^name:' */SKILL.md 2>/dev/null | wc -l) / $(find . -maxdepth 1 -type d ! -name skills | wc -l)"
# 期望：192 / 236（本机 2026-09-27 实测）

# === 验证 4：章节勘误真名命中（agentskills + 192）===
grep -c "agentskills" ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/chapters/10-skill-registry/README.md
# 期望：≥ 3
```

**成功标志**：你的 skill 落盘且 `^name:` 命中 + 本机覆盖率复算对上 192/236 + 你能 60 秒讲清"Skill 和 Plugin 的 3 个区别"（范围 / 加载方式 / 跨平台）。

### 步骤 6 · 验证完成后去哪

- **下一章**：第 12 章 · Plugin 入口 → `chapters/11-plugin-entrypoint/README.md`（接口层 4/4 · 把 skill 打包成可安装 plugin）
- **本章前置**：第 10 章 · A2A 绑定 → `chapters/09-a2a-binding/09-A2A绑定.md`
- **规范深读**：`SKILL.md-frontmatter-规范.md`（6 字段边界值）→ `8卷Skill写法适配.md`（8 卷 → 28 skill 映射）
- **实操**：本章 11.5 节 Plugin 路线 5 步（skill → plugin → registry，本机 ⏳ 未跑 `plugins install`）
- **FAQ**：frontmatter 字段疑问 → `SKILL.md-frontmatter-规范.md`；勘误疑问 → `真名验证与勘误.md`；术语疑问 → `00-术语对照表·v3.0行业标准版.md`

---

## SOP · 诚实边界声明

- ✅ **本章 SOP 基于本机实拉事实**：OpenClaw 2026.9.4 (3a9d69d)（`openclaw --version` 2026-09-27 实拉）· 本机 skills 目录 = 236 个 skill 目录（`find -maxdepth 1 -type d` 实测，含父目录为 237）· `grep -l '^name:'` = 192 个含 YAML frontmatter（覆盖率 81%）
- ✅ **独立实拉（2026-09-27）**：`openclaw plugins install` 子命令存在（`plugins --help` 实测）· anthropics/skills 178 606 stars / agentskills/agentskills 25 723 stars（章节 GitHub API 现拉）
- ⏳ **本章 SOP 未实测**：未在本机跑 `openclaw plugins install ~/.openclaw/workspace/skills/silicon-life-double-triangle`（命令存在但未执行）；未跑 `clawhub package publish --family skill`——步骤 5 接受"SKILL.md 落盘 + frontmatter 命中 + 覆盖率复算"作为通过条件
- ⚠ **两处数字口径差异**：本章 11.3 摘要写"236 / 192"，11.4 对位表写"194/236=82%"——**192 与 194 相差 2**，建议以**实测 192**为准（本 SOP 用 192）；差异根因（是否含 2 个特殊目录）⏳ 待核
- ⚠ **`ls | wc -l` 与 `find -type d` 口径不同**：`ls ~/.openclaw/workspace/skills/ | wc -l` 本机返回 **238**（含 2 个非目录文件），纯 skill 目录应为 **236**——SOP 步骤 1 已同时给出两种命令，避免误读
- ⚠ **8 卷 → 28 skill 是可行性预估**，非已完成产物；实际生成需逐卷按 `8卷Skill写法适配.md` 执行
- ⚠ **本机版本落后**：本机 2026.9.4 < 上游 2026.9.6 latest；Skill 结构若有 9.4/9.6 差异，本 SOP 以 9.4 为准

### 附录 A · SKILL.md 最小合规 1-pager（6 字段模板）

```
┌─────────────────────────────────────────────────────────────────┐
│  SKILL.md 最小合规模板 · Agent Skills 开放标准 · v5.0             │
├─────────────────────────────────────────────────────────────────┤
│  ---                        ← YAML frontmatter（不是 JSON5）      │
│  name: <skill-id>           ← 唯一标识（小写连字符）              │
│  description: <何时触发>    ← 决定渐进式披露能否命中              │
│  license: MIT               ← 跟随 OpenClaw 主仓                  │
│  metadata:                                                        │
│    author: <作者>                                                 │
│    version: "1.0"                                                 │
│  ---                                                              │
│                                                                   │
│  # <Skill 标题>                                                   │
│  ## 训练目标 / ## 操作流程   ← markdown 正文（自然语言指令）      │
├─────────────────────────────────────────────────────────────────┤
│ 本机基线：236 skills · 192 含 frontmatter（81%）· 2026-09-27      │
└─────────────────────────────────────────────────────────────────┘
```

### 附录 B · 术语速查（v1.0 黑话 vs v3.0 真名）

| v1.0 黑话（内部保留） | v3.0 真名（对外 + 工程接口必用） | 英文 alias |
|---|---|---|
| 技能基因 | 可复用能力单元 | Reusable Capability Unit（Skill Gene 保留作昵称） |
| 训虾派 / 养虾派 | 主动进化范式 | Proactive Evolution Paradigm |
| 双三角模型 | 双三角模型 | Dual-Triangle Model: Expectation-Actuality-Feedback Loop |
| 文档漂移 / 人格漂移 | 文档漂移 / 人格漂移 | Document Drift / Personality Drift |
| 自主目标生成 | 自主目标生成 | Autonomous Goal Generation (Response → Proposal) |
| 军团 | 多智能体编排 | Multi-Agent Orchestration / Agent Fleet |

→ 完整 35 条见 [`00-术语对照表·v3.0行业标准版.md`](../../00-术语对照表·v3.0行业标准版.md)

### 附录 C · 接口层 + 能力层跳转拓扑

```
09-mcp-binding/08-MCP绑定.md        (接口层 1/4 · 工具层 · MCP)
  ↓
10-a2a-binding/09-A2A绑定.md        (接口层 2/4 · 协议层 · A2A)
  ↓
11-skill-registry/README.md         (接口层 3/4 · 能力层 · Agent Skills · 本章)
  ├── SKILL.md-frontmatter-规范.md   (6 字段规范)
  ├── 8卷Skill写法适配.md            (8 卷 → 28 skill 映射)
  ├── Anthropic-Skills-实拉对位.md   (GitHub API 实拉)
  ├── Registry-表.md                (9 skill 目录表)
  └── 真名验证与勘误.md              (3 条重大勘误)
  ↓
12-plugin-entrypoint/README.md      (接口层 4/4 · 打包层 · Plugin)
```

### 附录 D · FAQ 速查（本章最常被问的 7 个问题）

| # | 问题 | 简短答案 | 详细位置 |
|---|---|---|---|
| 1 | Skill 到底是什么？ | 一个含 `SKILL.md` 的目录（自然语言指令 + 触发条件） | 本章 11.1 |
| 2 | Anthropic Skills 是私有规范吗？ | **不是**，agentskills.io 2025-12 已开放为标准 | 本章 11.3 勘误 #2 |
| 3 | `openclaw plugins install` 存在吗？ | **存在**（plural，6 种安装源） | 本章 11.3 勘误 #1 |
| 4 | 本机多少个 skill？ | 236 个；192 含 YAML frontmatter（81%） | 步骤 1 + 11.4 |
| 5 | SKILL.md frontmatter 用 YAML 还是 JSON5？ | **YAML**（JSON5 是 plugin 的 `openclaw.plugin.json`） | `SKILL.md-frontmatter-规范.md` |
| 6 | Skill 和 Plugin 什么区别？ | Skill = 剧本（Markdown/跨平台）；Plugin = 剧组（JSON5+Code/OpenClaw） | 本章 11.7 |
| 7 | 8 卷能 Skill 化成多少个？ | 7 卷可化，**预计** 28 个 SKILL.md（预测，未生成） | 本章 11.6 |

---

# 第 11 章 · Skill 注册：对齐 Agent Skills 开放标准

> **v5.0 行业标准版 banner**：本章对应 OpenClaw 训练学第 11 章（接口层 4 / 4）；详见 [book README](../../README.md)。
> **License banner**：MIT（基于 OpenClaw 主仓 `LICENSE` 法律文本；GitHub API 显示 `NOASSERTION` 不影响法律效力——参见第 11 章[真名验证与勘误](./真名验证与勘误.md)）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`。
> **业界对位**：本章对应 **Agent Skills 开放标准**（agentskills.io · 25 700+ stars · 32+ 客户端读 `SKILL.md`）——首次以**官方规范组织**形式取代 Anthropic 私有规范。

---

## 训练目标
让 agent 学会自主生成期望值（Expectation），
而不是等用户给指令。

## 操作流程
1. Observe 当前对话上下文
2. Orient 自身期望与用户期望的差值
3. Decide 是否提出 Proposition
4. Act 提交 Proposition，等待反馈

YAML

# Step 3 · init 一个 plugin（详见第 12 章）
openclaw plugins init silicon-life-double-triangle

# Step 4 · build → pack → install
openclaw plugins build --plugin silicon-life-double-triangle
openclaw plugins pack silicon-life-double-triangle
openclaw plugins install ~/.openclaw/workspace/skills/silicon-life-double-triangle

# Step 5 · inspect 验证
openclaw plugins inspect silicon-life-double-triangle
```

完整 plugin 入口在第 12 章展开。

---

## 11.8 诚实边界

- ✅ **已用**：本机 `openclaw --version = 2026.9.4 (3a9d69d)`；`openclaw plugins install` 子命令存在；本机 236 个 skill / 192 个有 YAML frontmatter
- ✅ **独立实拉**：anthropics/skills、agentskills/agentskills、openclaw/openclaw 三个 GitHub 仓库元数据全部 GitHub API 现拉
- ⏳ **未实测**：未在本机跑 `openclaw plugins install ~/.openclaw/workspace/skills/silicon-life-double-triangle`（命令存在但未执行）
- ⚠ **勘误**：v4.0 报告中"openclaw plugin install 不存在"+"Anthropic Skills 私有"两条均需更正——详见 [真名验证与勘误](./真名验证与勘误.md)

---

> **附**：本章所有 GitHub 数据均为 2026-09-27 实时实拉；agentskills.io 抓取于同日。OpenClaw 本机版本由 `openclaw --version` 验证。
>
> — SA-10 · 第 11 章 · 2026-09-27
---

## 常见错误

> **本节用法**：第 11 章是接口层第 3 块——Skill 注册：对齐 **Agent Skills 开放标准**（agentskills.io），把能力写成 1 个 `SKILL.md` + 可选 scripts/references/assets。
> 这里的 8 个错误来自一条根因：**把"我写了一个 md"当成"agent 会用这个 md"**。
> 术语首次出现双写：Supervisor Layer（原：监军）/ 多智能体编排（原：军团编制）/ Mentor Agent（原：教练虾）/ Drift Governance（漂移治理）/ Autonomy Boundary Triad（三档制）/ TEV（三证据验证，原：三证验真）/ Remediation Ticket（修复工单，原：整改单）/ Workspace Connector / 任务交接协议 THP / 多智能体协作 / 多智能体协同 / 智能体实例 / 智能体编排。
>
> **实测环境**：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27 · macOS 26.5.1 · 本机 skill 目录 **238** 条目 = **236 个纯 skill 目录** + INDEX 等 2 个非目录文件 · 192 个含 `^name:` YAML frontmatter（覆盖率 81%）。

### 错误 1 · 把 `SKILL.md` frontmatter 写成 JSON5（YAML / JSON5 混用）

**错误现象**：新人刚看完第 12 章（plugin 用 `openclaw.plugin.json` = **JSON5**），回手就把 skill 的 frontmatter 也写成 JSON5：

```markdown
----
{ "name": "my-skill", "description": "..." }   // ❌ 不是合法 YAML frontmatter
----
```

或者写成 `---json` 围栏、或 `{...}` 直接顶在 `#` 标题前。`grep -l '^name:'` 数不到它，覆盖率统计里它就"消失"了。

**错误配置**（❌ 不要这样）：

```markdown
{
  "name": "drift-audit",
  "description": "漂移审计"
}
# 漂移审计

正文……
```

**为什么错**：

1. **真名分野：`SKILL.md` 用 YAML，`openclaw.plugin.json` 用 JSON5。** 这是本章附录 D 第 5 问的原话——"SKILL.md frontmatter 用 YAML 还是 JSON5？**YAML**（JSON5 是 plugin 的 `openclaw.plugin.json`）"。
2. **YAML frontmatter 的结构是硬约定**：文件首行 `---`、键值对、闭合 `---`。没有这个夹具，前端的元数据就不存在——不是"格式不同"，而是"没有元数据"。
3. **工具链全按 YAML 解析**：`skills-ref`（官方校验工具）、32+ 个读 `SKILL.md` 的客户端、本机的覆盖率统计（`grep -l '^name:'`）——没有任何一个会去看你的 JSON5。
4. **代价是静默失效**：skill 能被 `find` 找到（目录在）、但不会被正确索引；agent 触发时匹配不到，表现为"这个 skill 好像没生效"。
5. **这也是 18 坏 skill 事故的同类根因**：文件在、加载失败、污染上下文——**格式不合规的静默失败**比报错危险得多。

**正确配置**（✅ 应该这样）：

```markdown
---
name: drift-audit
description: 审计 agent 是否出现漂移（Drift Governance）。当用户要求"检查漂移""审计行为一致性"时使用。
license: MIT
---

# 漂移审计

操作流程……
```

**验证命令**：

```bash
# 1) frontmatter 夹具存在且在首行
head -1 ~/.openclaw/workspace/skills/drift-audit/SKILL.md
# 期望：---

# 2) 能被覆盖率统计数到
grep -l '^name:' ~/.openclaw/workspace/skills/drift-audit/SKILL.md
# 期望：文件路径（能被数到 = 合规）

# 3) 本机总覆盖率复算（对照 192/236）
cd ~/.openclaw/workspace/skills && \
  echo "目录: $(find . -maxdepth 1 -type d | wc -l | tr -d ' ')"; \
  echo "含 frontmatter: $(grep -rl '^name:' --include=SKILL.md . | wc -l | tr -d ' ')"
# 期望：236 / 192（本机 2026-09-27 实测）

# 4) 官方校验工具（本机未装则标 ⏳）
# npx skills-ref validate ~/.openclaw/workspace/skills/drift-audit
```

**相关 FAQ**：F11-5（frontmatter 用 YAML 还是 JSON5）、F11-4（本机多少个 skill）。相关文档：`SKILL.md-frontmatter-规范.md`。

---

### 错误 2 · `name` 不符合 spec（大写 / 空格 / 超长 / 与目录名不一致）

**错误现象**：`name: Drift Audit`（有空格大写）、`name: 漂移审计`（中文）、`name: drift-audit-v2-final-2026-09-27`（超长）。目录叫 `drift-audit`，`name` 叫 `drift_audit`（下划线）。

**错误配置**（❌ 不要这样）：

```markdown
---
name: Drift Audit 2.0        # ❌ 空格 + 大写 + 版本号塞进 name
description: ...
---
```

**为什么错**：

1. **`name` 是强约束字段**（`SKILL.md-frontmatter-规范.md` §3.1 明确标注"最容易踩坑"）。它是**机器标识**：调用方用它索引、路由、去重；一旦含空格/大写，跨平台实现的分歧就开始了。
2. **`name` 应与 skill 目录名一致**。目录 `drift-audit` + `name: drift_audit` 是两份标识，早晚会有一处被改，另一处忘改 → 引用断链。
3. **不要往 `name` 里塞版本**。版本属于 `metadata.version`（或 `license` 旁边的版本字段），塞进 name 会让每次发版都改标识——等于每次发版都是新 skill。
4. **中文 `name` 会让非中文实现的索引乱掉**，同时和 v3.0 改名表冲突（改名表统一的是"对外术语"，不是"标识"）。
5. **代价**：`skills-ref` 校验直接失败；即便侥幸加载，`skills.status` / `skills.skillCard` 查询口径也会对不上。

**正确配置**（✅ 应该这样）：

```markdown
---
name: drift-audit                 # ✅ 小写 kebab-case，与目录名一致，无版本
description: 审计 agent 是否出现漂移（Drift Governance）……
license: MIT
metadata:
  version: "1.0.0"                # ✅ 版本放 metadata
  author: peterqiu
---
```

**验证命令**：

```bash
SKILL=~/.openclaw/workspace/skills/drift-audit

# 1) name 与目录名一致 + 合法字符集
n=$(grep -m1 '^name:' "$SKILL/SKILL.md" | sed 's/^name:[[:space:]]*//')
echo "name=$n  dir=$(basename "$SKILL")"
[ "$n" = "$(basename "$SKILL")" ] && echo "✓ 一致" || echo "❌ 不一致"

# 2) 反例检测：大写/空格/下划线
grep -m1 '^name:' "$SKILL/SKILL.md" | grep -qE '^name: *[a-z0-9]+(-[a-z0-9]+)*$' && echo "✓ 合规" || echo "❌ 违反 kebab-case"

# 3) 全库扫一遍不合规的（本机基线 236）
cd ~/.openclaw/workspace/skills && \
  grep -rh '^name:' --include=SKILL.md . | sed 's/^name:[[:space:]]*//' \
  | grep -vE '^[a-z0-9]+(-[a-z0-9]+)*$' | head -10
```

**相关 FAQ**：F11-1（Skill 到底是什么）。相关文档：`SKILL.md-frontmatter-规范.md` §3.1。

---

### 错误 3 · `description` 写成营销词（没有触发条件）

**错误现象**：`description: 本技能是业界最强的漂移审计方案，覆盖全场景。`——这句话对人类阅读友好，但 agent **永远不知道该在什么时候调用它**。

**错误配置**（❌ 不要这样）：

```markdown
---
name: drift-audit
description: 业界最强的漂移治理审计技能，全面、专业、高效。
---
```

**为什么错**：

1. **`description` 是弱约束字段，但是唯一的"触发入口"。** `SKILL.md-frontmatter-规范.md` §3.2 标注它是"最容易写得差"的字段——agent 只能读 description 来决定要不要加载，它是**唯一的匹配噪声源**。
2. **业务价值词对匹配零贡献**："最强""全面""专业""高效"在语义匹配里既不是触发器也不是判据，白白占用 token 预算。
3. **正确写法是"能力 + 触发条件"两句**：第一句说它做什么（供人读），第二句说**什么时候用**（供 agent 匹配）。这也是本书可用技能索引里"Use when <trigger>"的由来。
4. **后果**：skill 存在但从不被触发 → 你会误判"skill 机制不工作"，而实际是 description 没写触发条件。
5. **和渐进式披露联动**：description 是"第一层披露"——它一旦写虚，后面 references/ 里的深内容永远没机会被读到。

**正确配置**（✅ 应该这样）：

```markdown
---
name: drift-audit
description: >
  审计 agent 是否出现漂移（Drift Governance），输出漂移清单与修复工单建议。
  Use when 用户要求"检查漂移""审计行为一致性""对比计划与实际"，或需要按周/月核对 agent 输出与契约的一致性时。
---
```

**验证命令**：

```bash
# 1) description 含触发条件关键词
grep -A3 '^description:' ~/.openclaw/workspace/skills/drift-audit/SKILL.md | grep -ci "use when\|当用户\|触发"

# 2) 反例检测：空话堆叠
grep -A3 '^description:' ~/.openclaw/workspace/skills/drift-audit/SKILL.md | grep -ci "最强\|全面\|专业\|高效"
# 期望：0

# 3) 多行 description 必须用 block scalar（> 或 |）
grep -c '^description: *[>|]' ~/.openclaw/workspace/skills/drift-audit/SKILL.md
# 期望：1（若单行则此条不适用）
```

**相关 FAQ**：F11-1。相关文档：`SKILL.md-frontmatter-规范.md` §3.2 / §8.1。

---

### 错误 4 · 把 Skill 当 Plugin（往 `SKILL.md` 里塞代码 / 装进程）

**错误现象**：新人想给 skill 加"真的能跑的逻辑"，于是在 `SKILL.md` 里贴 300 行 TypeScript，或写"本 skill 启动一个后台进程监听 41241"。

**错误配置**（❌ 不要这样）：

```markdown
---
name: drift-audit
description: ...
---

# 漂移审计

## 实现
```typescript
// 300 行 TypeScript 内联在 SKILL.md 里     ❌ skill 是自然语言指令
import { Server } from "node:http";
const srv = Server().listen(41241);        // ❌ 也起不了进程
```
```

**为什么错**：

1. **范围不同**：Skill = 1 个 `SKILL.md` + 可选 scripts/references/assets（**markdown 指令，自然语言**）；Plugin = 1 个或多个 skill + `openclaw.plugin.json` + native Control UI 资源（**TypeScript/JavaScript 进程 + JSON 清单**）。
2. **加载方式不同**：Skill 是**渐进式披露**（agent 按需读）；Plugin 是**启动时加载**（`openclaw plugins enable`）。把代码放 skill 里，等于期望"读文档就能起进程"。
3. **跨平台性不同**：Skill 任何读 `SKILL.md` 的 agent 都能用；Plugin **仅 OpenClaw runtime**。塞代码是为了换插件能力，代价是丢掉 32+ 客户端的通用性。
4. **一句话分野**：**Skill = 你的"剧本"（Markdown · 自然语言 · 跨平台）；Plugin = 你的"剧组"（JSON + Code · 启动时加载 · OpenClaw 私有）**。
5. **正确路径是"先 Skill 后 Plugin"**：本章 11.5 给了 Plugin 路线示例——Skill 先把"怎么做"讲清楚，Plugin 再把"能不能自动做"工程化。

**正确配置**（✅ 应该这样）：

```markdown
---
name: drift-audit
description: 审计 agent 是否出现漂移……Use when 用户要求"检查漂移"时。
---

# 漂移审计

## 操作流程
1. 读出契约（SOUL / AGENTS）与近 N 天产出
2. 逐条对比，列出偏离项
3. 按 TEV 三证据格式落盘
4. 偏离项 → 建议开 Remediation Ticket

## 脚本（可选）
scripts/audit.py    ← 代码放 scripts/，不放 SKILL.md 正文
```

```text
# 需要"启动时加载 + 起进程"时，才升级为 Plugin（第 12 章）
openclaw.plugin.json + index.js  →  见 chapters/11-plugin-entrypoint/
```

**验证命令**：

```bash
# 1) 反例：SKILL.md 里出现 fenced code 块（除示例外）
grep -c '^```' ~/.openclaw/workspace/skills/drift-audit/SKILL.md

# 2) 反例：出现 import / require / listen(
grep -cn '^import \|require(\|\.listen(' ~/.openclaw/workspace/skills/drift-audit/SKILL.md
# 期望：0

# 3) 代码应该在 scripts/ 目录
ls -1 ~/.openclaw/workspace/skills/drift-audit/scripts/ 2>/dev/null || echo "（本 skill 无脚本，正常）"

# 4) 目录边界对照（reg：第 12 章 12.7 边界表）
# Skill：SKILL.md + scripts/references/assets  |  Plugin：+ openclaw.plugin.json + 进程
```

**相关 FAQ**：F11-6（Skill 和 Plugin 什么区别）、F12-2（配置文件叫什么）。相关章节：第 12 章 12.7。

---

### 错误 5 · 238 / 236 / 192 / 194 口径混用（数字对不上就下结论）

**错误现象**：用 `ls ~/.openclaw/workspace/skills/ | wc -l` 得到 **238**，用 `find -maxdepth 1 -type d | wc -l` 得到 **237**，用 `find -maxdepth 1 -type d | wc -l -1` 得到 **236**，grep frontmatter 得到 **192**，别人文档里写 **194**。于是判断"数据不可信"。

**错误配置**（❌ 不要这样）：

```bash
# 错误示范：一个数字断言代替口径说明
ls ~/.openclaw/workspace/skills/ | wc -l      # 238
echo "本机有 238 个 skill"                     # ❌ 含 2 个非目录文件
```

**为什么错**：

1. **238 = 236 个纯 skill 目录 + 2 个非目录文件**（如 INDEX 之类）。本章 README 已把口径写死：*"`ls | wc -l` 与 `find -type d` 口径不同：本机返回 238（含 2 个非目录文件），纯 skill 目录应为 236"*。
2. **`find -maxdepth 1 -type d` 会把父目录自己算进去**（所以是 237），要减去 1 才是 236。这三个数全是"同一件事、不同命令"。
3. **192 与 194 的差异是真实的未解项**：本章诚实边界标注"两处数字口径差异……建议以实测 192 为准……差异根因（是否含 2 个特殊目录）⏳ 待核"——**承认差异并给出采用口径**，比"挑一个好看的数字"专业得多。
4. **数字型断言的通用规则**：任何"数量"结论必须三件套——**命令 + 口径 + 日期**。
5. **代价**：口径混用会让 11 章的"覆盖率 81%→要不要批量补 frontmatter"这个**决策依据**出现 2% 偏差；没人敢签字。

**正确配置**（✅ 应该这样）：

```bash
# 正确示范：命令 + 口径 + 日期，三件齐
cd ~/.openclaw/workspace/skills
echo "A) ls 条目数（含非目录文件）: $(ls -1 | wc -l | tr -d ' ')"
echo "B) 纯 skill 目录数（-1 去父目录）: $(find . -maxdepth 1 -type d | wc -l | sed 's/^/x/' | tr -d 'x' | awk '{print $1-1}')"
echo "C) 含 ^name: frontmatter: $(grep -rl '^name:' --include=SKILL.md . | wc -l | tr -d ' ')"
echo "口径: A=含非目录文件  B=纯目录  C=按 SKILL.md 计数  日期: $(date +%F)"
```

**验证命令**：

```bash
# 1) 三种口径同时打印（对照本章 238 / 236 / 192）
cd ~/.openclaw/workspace/skills
{ echo "ls条目: $(ls -1 | wc -l | tr -d ' ')"; \
  echo "纯目录: $(( $(find . -maxdepth 1 -type d | wc -l) - 1 ))"; \
  echo "frontmatter: $(grep -rl '^name:' --include=SKILL.md . | wc -l | tr -d ' ')"; } \
  | tee ~/notes/domain/silicon-life-handbook/evidence/skill-count.log

# 2) 非目录文件是什么（解释 238-236=2）
find ~/.openclaw/workspace/skills -maxdepth 1 ! -type d -print

# 3) 覆盖率
python3 -c "print(192/236)"   # ≈ 0.8136 → 81%
```

**相关 FAQ**：F11-4（本机多少个 skill）。相关文档：本章 README 步骤 1 / 11.4。

---

### 错误 6 · 宣称 "Anthropic Skills 是私有规范"（勘误 #2）

**错误现象**：文档里写"Anthropic Skills 是 Anthropic 私有格式，只能在 Claude 用"，因此结论"我们不该对齐它"。

**错误配置**（❌ 不要这样）：

```markdown
<!-- 错误示范 -->
Anthropic Skills 为 Anthropic 私有规范，仅 Claude 生态可用。
```

**为什么错**：

1. **事实：agentskills.io 于 2025-12 已把 Agent Skills 开放为标准**。本章 README 的勘误 #2 原文就是："Anthropic Skills 是私有规范吗？**不是**，agentskills.io 2025-12 已开放为标准。"
2. **开放性的证据是"客户端数"**：本章 11.4 的对位表以 **25 700+ stars** 与 **32+ 客户端读 `SKILL.md`** 作为开放标准的量化依据——私有规范不会有 32 个第三方客户端。
3. **判断错会导致路线错**：如果它是私有的，对齐它就没意义；正因为是开放标准，第 11 章才敢把"Agent Skills 兼容性"作为本书接口层的核心卖点。
4. **勘误的存在本身就是方法论**：v4.0 报告写错了，v5.0 用**独立实拉**（anthropics/skills、agentskills/agentskills、openclaw/openclaw 三个仓库元数据全部 GitHub API 现拉）纠正——这比"照抄上一版"可复现得多。
5. **引用注意**：开放标准 ≠ 无版本。开放的是"格式与治理"，具体规范版本仍要写清（如 `specification.md` 的当前版本）。

**正确配置**（✅ 应该这样）：

```markdown
<!-- 正确示范 -->
Agent Skills 是**开放标准**：Anthropic 2025-10-16 首发 → 2025-12-18 经
agentskills.io 开放为标准（25 700+ stars · 32+ 客户端读 SKILL.md）。
→ 结论：对齐它是**生态借势**，不是绑定某一家。
```

**验证命令**：

```bash
# 1) 本机是否装了官方 skills 相关 skill
# ⚠️ 2026-09-28 实测：`skill-security-audit` 目录不存在，实际目录名为 `skill-security-audit-v2`
openclaw skills list 2>&1 | grep -i "skill-security-audit\|agent-skills-audit\|mcporter" | head -3

# 2) 章节勘误条目在
grep -n "私有" ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/chapters/10-skill-registry/真名验证与勘误.md | head -5

# 3) 实拉证据链（本机对位文档）
sed -n '1,40p' ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/chapters/10-skill-registry/Anthropic-Skills-实拉对位.md
```

**相关 FAQ**：F11-2（Anthropic Skills 是私有规范吗）。

---

### 错误 7 · 以为 `openclaw plugins install` 不存在（plural / 勘误 #1）

**错误现象**：新人写完 skill 想装成 plugin，先查 `openclaw plugin install`（**singular**）→ command not found → 结论"OpenClaw 不支持装 plugin"，放弃路线。

**错误配置**（❌ 不要这样）：

```bash
openclaw plugin install ./my-skill     # ❌ singular，不存在
# → command not found → 误判"不支持插件"
```

**为什么错**：

1. **真名是 `plugins`（plural）**：`openclaw plugins` 命令族含 build / disable / doctor / enable / init / inspect / install / list / marketplace / pack / registry / search / uninstall / update / validate（15 个子命令实测）。**`install` 存在**，且支持 6 种安装源。
2. **这是本章 README 勘误 #1**："`openclaw plugins install` 存在吗？**存在**（plural，6 种安装源）。"
3. **"singular 失败"是极常见的假阴性**：CLI 命名习惯不统一（有的工具单数、有的复数），一次 typo 就足以否定整条路线。
4. **推论成本很高**：一旦认为"不支持"，你会绕道去做手工复制文件——而 `install` 本来会帮你注册 `plugins.installs`。
5. **通用规则**：任何"某命令不存在"的结论，必须补一条 `openclaw <group> --help` 的输出作为证据；否则只是"我拼错了"。

**正确配置**（✅ 应该这样）：

```bash
# 正确示范：先拉命令族，再选子命令
openclaw plugins --help 2>&1 | sed -n '/Commands:/,/^$/p'
# 期望：build / disable / doctor / enable / init / inspect / install / list /
#      marketplace / pack / registry / search / uninstall / update / validate

openclaw plugins install <source>      # ✅ plural
```

**验证命令**：

```bash
# 1) install 子命令真身
openclaw plugins --help 2>&1 | grep -cE "^\s+install\b"
# 期望：1

# 2) 子命令总数（15）
openclaw plugins --help 2>&1 | sed -n '/Commands:/,/^$/p' | grep -cE "^\s+[a-z]"
# 期望：≥ 14

# 3) 现状基线（51/69 enabled）
openclaw plugins list 2>&1 | head -1

# 4) 体检
openclaw plugins doctor
```

**相关 FAQ**：F11-3（plugins install 存在吗）、F12-1（plugin 还是 plugins）。

---

### 错误 8 · 破坏渐进式披露（把全部内容堆在 `SKILL.md`）

**错误现象**：一个 `SKILL.md` 写到 800 行——背景、原理、全部案例、全部脚本内联，全在第一层。agent 每次匹配到它就吃掉几万 token。

**错误配置**（❌ 不要这样）：

```text
drift-audit/
└── SKILL.md        # ❌ 800 行，全部内容平铺
                    #    无 references/ · 无 scripts/ · 无 assets/
```

**为什么错**：

1. **Agent Skills 的核心设计是渐进式披露（Progressive Disclosure）**：`SKILL.md` 是**第一层（入口）**，深内容放 `references/`、可执行逻辑放 `scripts/`、素材放 `assets/`——agent 按需读第二层。
2. **成本是 token**：第一层每多 100 行，每次匹配就多付 100 行；而 90% 的调用只需第一层的"操作流程"。
3. **技能基因（Skill Gene）与 Skill 载体要分开**（术语表 #17）：可复用能力单元是抽象的；`SKILL.md` 只是它的一个载体。把载体写爆，不会让基因更强。
4. **后果是"触发变贵、深内容反而到不了"**：token 预算被背景叙述吃掉，真正需要的 references 反而没机会被读。
5. **标准给了目录结构**（`SKILL.md-frontmatter-规范.md` §6 / §7）：目录结构不是风格问题，是**披露层次**问题。

**正确配置**（✅ 应该这样）：

```text
drift-audit/
├── SKILL.md                 # ✅ 第一层：60-120 行，触发条件 + 操作流程 + 检查清单
├── references/
│   ├── field-guide.md       # ✅ 第二层：字段详解 / 案例库
│   └── faq.md
├── scripts/
│   └── audit.py             # ✅ 可执行逻辑
└── assets/
    └── template.jsonl       # ✅ 模板素材
```

**验证命令**：

```bash
SKILL=~/.openclaw/workspace/skills/drift-audit

# 1) 第一层行数（建议 ≤ 200）
wc -l "$SKILL/SKILL.md"

# 2) 三层目录是否齐
for d in references scripts assets; do
  [ -d "$SKILL/$d" ] && echo "✓ $d" || echo "（无 $d，视需要）"
done

# 3) 全库第一层行数分布（找超长的）
cd ~/.openclaw/workspace/skills && \
  for f in */SKILL.md; do printf "%5d %s\n" "$(wc -l < "$f")" "$f"; done | sort -rn | head -10
```

**相关 FAQ**：F11-1、F11-6。相关文档：`SKILL.md-frontmatter-规范.md` §6 / §7。

---

## 新手坑

> **本节用法**：本章 5 个坑的共同特征是"**先写内容，再想它什么时候被用**"。
> 实测环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27 · 本机 236 skill 目录 / 192 含 frontmatter。

### 坑 1 · 先写 300 行正文，最后才补 frontmatter

**坑的场景**：新人从"我想让 agent 学会做 X"出发，一口气写完操作流程、案例、注意事项；最后回头补 frontmatter 时，`name` 随手起、`description` 一句带过。

**后果**：frontmatter 成了"补丁"而不是"接口"。`name` 与目录名不一致、`description` 无触发条件——正文写得再好，agent 也匹配不到。这是"内容 100 分、入口 0 分"。

**为什么踩**：

- **写作的自然顺序是"先做事后命名"**，而 skill 的加载顺序是"先命名后做事"。
- **frontmatter 只有 6 个字段**，看起来"随手就能填"，于是被排到最后。
- **反馈延迟**：正文写完不会立刻有任何报错，frontmatter 错也不会立刻报错。

**怎么爬出来**：

```bash
# 1) 先重写 frontmatter（10 分钟），再回看正文
cat > ~/.openclaw/workspace/skills/drift-audit/SKILL.md <<'MD'
---
name: drift-audit
description: 审计 agent 是否出现漂移（Drift Governance）。Use when 用户要求"检查漂移""审计一致性"时。
license: MIT
metadata:
  version: "1.0.0"
---
MD

# 2) 把正文接在后面（保留你已写的内容）
cat ~/Desktop/drift-audit-body.md >> ~/.openclaw/workspace/skills/drift-audit/SKILL.md

# 3) 校验
grep -l '^name:' ~/.openclaw/workspace/skills/drift-audit/SKILL.md
wc -l ~/.openclaw/workspace/skills/drift-audit/SKILL.md
```

**预防**：把 frontmatter **当接口先写**：名字、触发条件、边界三个先定，正文只是实现。

---

### 坑 2 · 复制别人的 skill，连 frontmatter 一起抄

**坑的场景**：新人 `cp -r` 一个现成 skill 当模板，改了正文，忘了改 `name`、`description`、`metadata.author`。

**后果**：本机出现两个同名 skill（`name` 冲突）→ `skills.status` 查询歧义、agent 匹配到旧的那个；或者 author 指向别人，治理审计时责任归属错。

**为什么踩**：

- **"复制目录"是最省事的起步方式**，模板里 400 行正文比 6 行 frontmatter 显眼得多。
- **`name` 冲突不报错**：两个目录、两个 `name: foo`，系统照样能起来。
- **作者字段没人看**：直到要追溯"这条能力谁写的"时才发现。

**怎么爬出来**：

```bash
# 1) 找出重复 name（本机 236 个 skill 全扫）
cd ~/.openclaw/workspace/skills && \
  grep -rh '^name:' --include=SKILL.md . | sed 's/^name:[[:space:]]*//' | sort | uniq -d
# 期望：空（无重复）

# 2) 定位自己的 skill 并改 identifier 三件套
S=~/.openclaw/workspace/skills/drift-audit/SKILL.md
sed -i '' 's/^name: .*/name: drift-audit/' "$S"     # macOS 需 -i ''

# 3) 改 author
grep -n "author" "$S"
```

**预防**：`cp -r` 之后第一件事就是改 `name` / `description` / `metadata.author` 三个字段（写进 checklist）。

---

### 坑 3 · 把长文塞进 `metadata` 或 `description`（YAML 就崩）

**坑的场景**：新人想"把触发条件写清楚"，于是 `description: 第一句……第二句……第三句……`（一行 500 字符），或者 `metadata: {把一整篇案例库塞进去}`。YAML 解析直接失败。

**后果**：`SKILL.md` 整份加载失败（不只是字段丢失）——这是"18 坏 skill"型事故的典型形态：一个格式错，skill 就废了。

**为什么踩**：

- **YAML 的引号/缩进规则不直观**：含 `:` 的值、含 `#` 的值、超长单行都是坑。
- **"多写点更保险"的心理**：描述越详细越好——但对机器格式而言，长度本身就是风险。
- **没有本地校验习惯**：写完不跑 yaml.load。

**怎么爬出来**：

```bash
# 1) 用 block scalar 写多行（> 折叠 | 保留换行）
cat > /tmp/fm-check.py <<'PY'
import sys, yaml
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
assert t.startswith('---'), "首行必须是 ---"
end = t.find('\n---', 3)
fm = yaml.safe_load(t[3:end])
print("✓ YAML OK:", {k: (str(v)[:40] + '…' if len(str(v)) > 40 else v) for k, v in fm.items()})
PY
python3 /tmp/fm-check.py ~/.openclaw/workspace/skills/drift-audit/SKILL.md

# 2) 长内容搬到 references/，frontmatter 只留一句
mkdir -p ~/.openclaw/workspace/skills/drift-audit/references
```

**预防**：`description` 控制在 1-2 句（≤ 300 字符）；超过的内容一律去 `references/`。

---

### 坑 4 · 以为"skill 写好了，agent 就会用"

**坑的场景**：新人写完 skill、目录也在，就对外汇报"agent 现在具备漂移审计能力了"。从没验证过任何一次实际触发。

**后果**：能力是"声明态"不是"运行态"。真到需要审计时，agent 压根没加载它——这正是能力矩阵 26 天未续期那类"纸面能力"的同构问题。

**为什么踩**：

- **"文件在 = 功能在"** 的直觉（和第 9 章"plugin 在列表里 = 已启用"是同一个坑）。
- **触发验证成本高**：要构造一个真的会命中 description 的请求，还要看它有没有加载。
- **没有"能力验证"这一环的模板**。

**怎么爬出来**：

```bash
# 1) 注册可见性
openclaw skills list 2>&1 | grep -i drift
openclaw skills status 2>&1 | head -20      # 若可用

# 2) 真触发一次（TEV 证据 3：日志）
openclaw agent --message "检查一下我最近的漂移情况" --agent my-agent
# 观察日志里是否出现该 skill 的加载记录

# 3) 落盘证据
mkdir -p ~/notes/domain/silicon-life-handbook/evidence
openclaw skills list > ~/notes/domain/silicon-life-handbook/evidence/skills-list.log 2>&1
```

**预防**：skill 的验收口径（Acceptance Criteria）里必须有一条"**至少一次真实触发记录**"，否则只算"已登记"。

---

### 坑 5 · 把 v1.0 黑话写进 `description` / 正文（对外术语污染）

**坑的场景**：新人熟读 v1.0，写 skill 时自然用"监军""军团""三证验真""信誉分""训虾派"。skill 面向 32+ 客户端，等于把内部黑话直接出口。

**后果**：跨平台/跨组织读者看不懂；术语与 v3.0 改名表冲突；同一个概念在不同 skill 里名字不同，触发匹配也被稀释。

**为什么踩**：

- **黑话是"内部熟词"**，写起来最顺手。
- **改名表有 35 条**，没人能全背；写的时候不会想到去查。
- **"skill 是给我自己用的"错觉**——一旦进 registry / 被别的 agent 读，它就是对外的。

**怎么爬出来**：

```bash
# 1) 扫黑话（本章相关的高频 6 条）
cd ~/.openclaw/workspace/skills/drift-audit && \
  grep -rn "监军\|军团\|三证验真\|整改单\|信誉分\|军功簿\|训虾派" . | head

# 2) 按改名表双写
#    监军 → Supervisor Layer（原：监军）
#    军团 → 多智能体编排（原：军团编制）
#    三证验真 → TEV（三证据验证，原：三证验真）
#    整改单 → Remediation Ticket（修复工单，原：整改单）

# 3) 参照改名表全文
grep -n "" ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/00-术语对照表·v3.0行业标准版.md | head -40
```

**预防**：skill 里"术语首次出现必须双写"写进模板；提交前跑一次黑话扫描。

---

### 坑 6 · 以为"frontmatter 字段填得越满越合规"

**坑的场景**：新人看完 6 字段矩阵（name / description / license / compatibility / metadata / allowed-tools），本着"填满显得专业"的心态，把 6 个全填上：`compatibility` 写 "Claude, OpenAI, Gemini, everything"，`allowed-tools` 抄了一长串，`metadata` 塞进 20 个自定义键。

**后果**：三项实际损伤——

1. **`compatibility` 是"大多数 skill 不需要"的字段**（规范原文如此）。乱填等于替**调用方**做了兼容性承诺；对方按你的声明去调用，发现不兼容，责任在你。
2. **`allowed-tools` 是实验性字段**。把实验性字段当稳定 API 用，规范一改你就得改，而所有依赖它的调用方也要改。
3. **`metadata` 是自由空间但会被整个读取**。塞 20 个键 = 每次加载多付 20 键的 token 成本，且键名没有 schema 保护，拼错不报错、只静默无效。

**为什么踩**：

- **"完整"在中文语境里几乎总是褒义**（完整版 > 精简版），但配置字段的"完整"是**噪声**。
- **字段矩阵看起来是清单**：列出 6 个，人就会想逐个打勾。
- **"显式优于隐式"被误用**：显式声明的前提是**你真的知道并承诺**；不知道就填，是把猜测固化成契约。
- **参考样本会误导**：⚠️ **原文声明「`skill-security-audit` 是本机唯一 6/6 字段全覆的样本」已于 2026-09-28 实测推翻**——① `~/.openclaw/workspace/skills/skill-security-audit/` **目录不存在**（实际目录为 `skill-security-audit-v2/`，且其 `name:` = `skill-security-audit` ≠ 目录名 → name 违例）；② 该 skill 的 frontmatter **只有 `name` + `description` = 2/6**（`MIT` 只写在 `CLAWHUB.json`，不在 frontmatter）；③ **本机 6/6 全字段样本 = 0 个**，最高档是 5/6 的 11 个。详见 `Registry-表.md` §10。

**怎么爬出来**：

```bash
SKILL=~/.openclaw/workspace/skills/drift-audit/SKILL.md

# 1) 按"必需 → 推荐 → 视需要"三档重排字段
python3 - <<'PY'
import yaml
p = "<SKILL 路径>"
t = open(p, encoding="utf-8").read()
fm = yaml.safe_load(t.split("---", 2)[1])
need = ["name", "description"]            # 最小骨架
reco = ["license", "metadata"]            # 推荐
cond = ["compatibility", "allowed-tools"] # 视需要（乱填 = 负资产）
print("必需:", {k: fm.get(k) for k in need})
print("推荐:", {k: fm.get(k) for k in reco})
print("视需要（检查是否真的需要）:", {k: fm.get(k) for k in cond})
PY

# 2) 逐项自问三句：
#    compatibility —— 我是否真的跨多个客户端验证过？没有 → 删掉
#    allowed-tools —— 我是否真的依赖工具白名单语义？没有 → 删掉
#    metadata      —— 每个键是否真的会被用到？不会 → 删掉

# 3) 重写后校验 YAML 仍可解析
python3 -c "import yaml;yaml.safe_load(open('$SKILL',encoding='utf-8').read().split('---',2)[1]);print('✓ YAML OK')"
```

**预防**：

- 采用**最小骨架起步**（`name` + `description`），写不动了再加字段——而不是一开始填满。
- 字段三档表贴在自己 skill 目录的 `references/` 里：**必需 / 推荐 / 视需要（附判据）**。
- `compatibility` 只在**真的跨多客户端验证过**时才写，并且写清验证过的客户端与版本。
- 记住 ⚠️ **原文「`skill-security-audit` 是特例样本」的前提已不成立**——它实测只有 **2/6**，且该目录不存在。抄结构应参考 **5/6 组**（如 `bazi-fortune` / `compliance-officer`，均缺 `allowed-tools`）（见 `Registry-表.md` §10.2）。

**相关 FAQ**：F11-1 / F11-4。相关文档：`SKILL.md-frontmatter-规范.md` §3.4 / §3.5 / §3.6 / §4（最小骨架）。

---

## 扩展阅读

> **本节用法**：本章是接口层第 3 块（能力层 · Agent Skills），扩展阅读 = "业界能力标准对位 + 本书内导航 + 一手核实命令"。
> stars 为 2026-09-27 实拉；未评测项标 ⏳。

### 业界对位

| 业界项目 | 对应内容 | 链接 | 差异 |
|---|---|---|---|
| Agent Skills（agentskills.io） | 本章底座：开放能力标准（25 700+ stars · 32+ 客户端） | https://agentskills.io | 本书在其上加"训练学语义（7 契约 / 5 优势）" |
| anthropics/skills | 参考实现与样例 skill | https://github.com/anthropics/skills | 样例强，无注册表/治理口径 |
| Claude Agent SDK（⭐8,172） | skills 加载与工具绑定 | https://github.com/anthropics/claude-agent-sdk-python | 加载机制强，注册面弱 |
| MCP（第 8 章） | resource / tool 协议 | https://modelcontextprotocol.io | MCP 管调用，Skill 管"怎么做" |
| A2A（第 10 章） | Card 的 `skills[]` 声明 | https://a2a-protocol.org | A2A 声明能力，Skill 实现能力 |
| LangChain（⭐147,151） | 工具/链抽象 | https://github.com/langchain-ai/langchain | 代码优先，跨平台 markdown 化弱 |
| LlamaIndex（⭐52,330） | 索引/检索式能力 | https://github.com/run-llama/llama_index | 偏数据，无"触发条件"设计 |

**关键结论**：业界普遍有"能力声明"（tool / function / chain），**只有 Agent Skills 把"自然语言指令 + 渐进式披露 + 跨 32 客户端"作为标准**——这是本书选择在对齐它而非自研格式的原因。

> ⏳ 诚实边界：stars / 客户端数来自 2026-09-27 GitHub API 实拉；`openclaw plugins install` 命令存在但本机未执行安装。

### 业界对位补充 · Skill / Plugin / MCP / A2A 四分位对照

| 维度 | Skill | Plugin | MCP | A2A |
|---|---|---|---|---|
| 范围 | 1 个 `SKILL.md` + 可选资源 | 1+ skill + manifest + 进程 | server（resource/tool） | Agent Card + Task |
| 单位 | Markdown（自然语言） | TS/JS 进程 + JSON5 | 协议端点 | 协议消息 |
| 加载 | 渐进式披露（按需） | 启动时（enable） | 连接时（probe） | 握手时（Card） |
| 跨平台 | ✅ 32+ 客户端 | ❌ 仅 OpenClaw | ✅ 多框架 | ✅ A2A 生态 |
| 本书章节 | 第 11 章 | 第 12 章 | 第 8 章 | 第 10 章 |

### 本书内交叉引用

- **前一章**：第 10 章 · A2A 绑定（接口层 2/4，agent ↔ agent）→ `chapters/09-a2a-binding/09-A2A绑定.md`
- **后一章**：第 12 章 · Plugin 入口（接口层 4/4，打包分发）→ `chapters/11-plugin-entrypoint/README.md`
- **本章 SOP**：`## SOP · 本章怎么用`（步骤 2 的三件事）+ `### 附录 A · SKILL.md 最小合规 1-pager`
- **配套文件**：`Registry-表.md`（9 个代表 skill 实测）/ `SKILL.md-frontmatter-规范.md`（6 字段矩阵）/ `8卷Skill写法适配.md` / `Anthropic-Skills-实拉对位.md` / `真名验证与勘误.md`
- **上游**：第 0 章（差异化优势清单）、第 2 章（Skills 模块 + `skills.status` 网关 RPC）
- **相关 FAQ**：F11-1（Skill 是什么）、F11-2（私有吗）、F11-3（plugins install 存在吗）、F11-4（本机多少个）、F11-5（YAML 还是 JSON5）、F11-6（Skill vs Plugin）、F11-7（8 卷能 Skill 化几个）
- **相关 Cookbook**：C3 系列（Skills / Tools / MCP，见 `cookbook/03-skills-tools-mcp.md`）
- **术语底座**：`00-术语对照表·v3.0行业标准版.md`（#17 技能基因 vs 载体 / #20 双模块 / #32 网关 RPC / #33 主仓真名）

### 延伸阅读补充 · 一手核实命令（本章）

```bash
# 版本
openclaw --version 2>&1 | tail -1      # OpenClaw 2026.9.4 (3a9d69d)

# 库存三口径（238 / 236 / 192）
cd ~/.openclaw/workspace/skills
echo "ls条目: $(ls -1 | wc -l | tr -d ' ')"
echo "纯目录: $(( $(find . -maxdepth 1 -type d | wc -l) - 1 ))"
echo "frontmatter: $(grep -rl '^name:' --include=SKILL.md . | wc -l | tr -d ' ')"

# 非目录文件（解释 238-236）
find ~/.openclaw/workspace/skills -maxdepth 1 ! -type d -print

# 重复 name 检测
grep -rh '^name:' --include=SKILL.md . | sed 's/^name:[[:space:]]*//' | sort | uniq -d

# plugin 侧真名（对照第 12 章）
openclaw plugins --help 2>&1 | sed -n '/Commands:/,/^$/p'
openclaw plugins list 2>&1 | head -1     # Plugins (51/69 enabled)

# 兜底
openclaw health && openclaw doctor && openclaw backup create
```

### 延伸阅读补充 · 本章相关真实案例索引

| 案例 | 现象 | 对应 Skill 环节 | 相关章节 |
|---|---|---|---|
| 18 坏 skill | 加载失败、污染上下文 | frontmatter 不合规 = 静默失效 | 第 5 章 / F5-10 |
| 能力矩阵 26 天未续期 | 纸面能力无人续期 | "文件在 ≠ 能力在"；缺触发验证 | 第 5 章 / F7-15 |
| 9/21 飞书推送事故 | 定时任务静默失败 | skill 无触发日志 = 无证据 3 | 第 6 章 / F3-12 |
| 8/19 军团断线 | 通道失效无人应答 | 跨 agent 能力声明不一致 | 第 10 章 / F3-13 |

### 延伸阅读补充 · Registry 表字段速查（与 `Registry-表.md` 对齐）

| 字段 | 约束 | 常见错法 | 本机覆盖 |
|---|---|---|---|
| `name` | 强（kebab-case，与目录一致） | 大写/空格/中文 | 236 目录中 **191**（顶层 YAML key 口径）/ **194**（`grep -rl '^name:'` 口径）⚠️ 原文记 192 |
| `description` | 弱（唯一触发入口） | 营销词、无 "Use when" | 建议 1-2 句；本机 **192** |
| `license` | 推荐 | 留空 | 本机 **24** 个标 License |
| `compatibility` | 可选 | 乱填致误判 | 大多数不需要；本机仅 **12** 个填 |
| `metadata` | 推荐（自由空间） | 塞长文致 YAML 崩 | `version` / `author`；本机 **68** 个填 |
| `allowed-tools` | 实验性 | 当稳定 API 用 | **9**（2026-09-28 实测，原记 ⏳ 未实测） |

> ⚠️ **勘误（2026-09-28 实测）**：**原文「`skill-security-audit` 是本机唯一 6/6 字段全覆的样本」已推翻**——① `skills/skill-security-audit/` 目录**不存在**（实际为 `skill-security-audit-v2/`，`name:` ≠ 目录名）；② 其 frontmatter 仅 `name` + `description` = **2/6**（`MIT` 只在 `CLAWHUB.json`）；③ **本机 6/6 全字段样本 = 0 个**，最高档为 **5/6（11 个）**：`bazi-fortune` / `compliance-officer` / `fengshui-advisor` / `geo-content-optimizer` / `git-workflow` / `greenhelix-agent-workforce-orchestration` / `liuyao-yijing` / `meihua-yishu-divination` / `qimen-dunjia-oracle` / `vedic-astrology`（缺 `allowed-tools`）+ `contract-review`（缺 `compatibility`）。完整实测见 `Registry-表.md` **§10**（含 52 条 name 违例清单与 28 vs 47 口径双列）。

### 延伸阅读补充 · 引用禁忌（本章专属）

- 不得写"Anthropic Skills 是私有规范"（须写开放标准 + 日期）
- 不得用 `openclaw plugin install`（singular；须 `plugins`）
- 不得混用 238 / 236 / 192 / 194 口径（须"命令 + 口径 + 日期"三件齐）
- 不得把 Skill 与 Plugin 混为一谈（剧本 vs 剧组）
- 不得把内部黑话（监军/军团/三证验真/信誉分/军功簿/训虾派）写进技能对外 description
- 不得在未验证触发的情况下宣称"agent 具备该能力"

### 一句话收尾

第 11 章可以浓缩成一句口诀：**"name 小写对齐目录、description 写触发条件、YAML 不是 JSON5、Skill 是剧本 Plugin 是剧组、数字必须带口径"**——能力层的价值不在"我写了多少行"，而在"agent 在对的时候能不能找到它"。

---

*第 11 章（11-skill-registry）P1-2 追加区块 · 常见错误 8 个 / 新手坑 5 个 / 扩展阅读 6 部分*
*撰写：从零撰写（未抄 v1.0/v4.0 原文）· 2026-09-27*
*实测环境：OpenClaw 2026.9.4 (3a9d69d) · macOS 26.5.1 · 本机 238 条目 = 236 纯目录 + 2 非目录文件 · 192 含 frontmatter*

---

### 延伸阅读补充 · 全章真名命令速查（含本章新增 · 逐条可执行）

```bash
# —— 环境 / 实例层（本章前置底座）——
openclaw setup                       # 首次环境初始化（真名 · 交互式）
openclaw agents add <name>           # 新增智能体实例（真名）
openclaw agents list                 # 本机 18 个 agent（实测基线）
openclaw health                      # 运行时健康
openclaw doctor                      # 配置 / 依赖体检
openclaw backup create               # 破坏性操作前的安全网

# —— 本层（Skill 注册）——
cd ~/.openclaw/workspace/skills
ls -1 | wc -l                        # 238（含 2 个非目录文件）
find . -maxdepth 1 -type d | wc -l   # 237（含父目录；-1 = 236）
grep -rl '^name:' --include=SKILL.md . | wc -l   # 192（含 frontmatter）
openclaw skills list | grep -i <your-skill>      # 注册可见性
python3 -c "import yaml;yaml.safe_load(open('<SKILL>',encoding='utf-8').read().split('---',2)[1]);print('✓ YAML OK')"
openclaw agent --message "用一下 <your-skill>" --agent <name>   # 真触发验证

# —— 跨层对照（第 8/10/12 章真名）——
openclaw mcp list                    # 第 8 章：mcp.servers 基线
openclaw plugins list                # 第 12 章：51/69 enabled
openclaw plugins --help              # plugins 复数（含 install / validate）
```

> ⏳ 标注说明：`npx skills-ref validate <dir>`（官方校验工具）本机未装，属 ⏳；SKILL.md frontmatter 用 **YAML**，plugin manifest 才用 **JSON5**——两处勿混。

---

## 本章业界对位（详见 ./_industry-frontier-tracking.md §2.10）

## 本章前沿追踪（详见 ./_industry-frontier-tracking.md §3.3）

## 附录索引

> 本章涉及的 cookbook / FAQ / SOP / case-library / api-reference **编号入口**——按编号跳读即可。

### Cookbook 配方（[`_appendix-cookbook/`](../../_appendix-cookbook/)）
- C3-3 Skill 注册
- C3-4 Skill 校验
- C3-5 Skill 写作

### FAQ 问答（[`_appendix-faq/`](../../_appendix-faq/)）
- F5 Skills-Tools-MCP

### SOP 操作手册（[`_appendix-sop/`](../../_appendix-sop/)）
- SOP-2 多设备同步

### API 参考（[`_appendix-api/`](../../_appendix-api/)）
- 见 `_appendix-api/02-config-schema.md`（openclaw.json 20 顶层 key）
- 见 `_appendix-api/03-protocol-reference.md`（7 大协议格式）
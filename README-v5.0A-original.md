# 📘 硅基生命训练学 · v5.0 行业标准版 · 全书总索引

> **版本**：**v5.0 行业标准版** · 2026-09-27
> **正标题**：《硅基生命训练学：从响应型到提案型》
> **副标题**：AI Agent 训练方法论 / Silicon Life Training: From Reactive to Proactive
> **基线版本**：v1.0（**83 文件 · 38,518 行**，一字未动 · 仅作参考依据）+ v4.0（**111 文件 · 36,175 行**）
> **本版实测规模**：**59 文件 · 53,258 行**（`find . -name '*.md' | wc -l` + 逐文件 `wc -l` 求和，2026-09-27 本机实测）
> **维护者**：丘国力（Peter Qiu）· 天策（Blue-Blood Agent Ecosystem · Supervisor Layer，原：监军）
> **License**：**MIT**（跟随 OpenClaw 主仓 `LICENSE` 法律文本；GitHub badge 因 `THIRD_PARTY_NOTICES` 尾行显示 `NOASSERTION`，**不影响法律效力**——P0 核实结论，plugin 分发可行）
> **配套基座**：OpenClaw **2026.9.4 (3a9d69d)**（本书统一书写口径）+ Hermes Agent **0.20.1**
> **本机 live 实测**：`openclaw --version` → **`OpenClaw 2026.9.6 (eb377ac)`**（2026-09-27 实测；比本书口径高两个补丁版，**配置兼容，差异已诚实标注**）
> **宿主环境**：macOS **26.5.1** · skills **236 个**（`ls skills/` 238 个目录项 − 2 个非目录文件）
> **定位**：作为 OpenClaw agent 训练的**正式底座** + 全行业唯一的「SOP 大全 + 案例库 + 练习题级」实战体系
> **配套文档**：[`00-术语对照表·v3.0行业标准版.md`](./00-术语对照表·v3.0行业标准版.md)（35 条改名对照）· [`00-新书主编报告.md`](./00-新书主编报告.md)（架构 + 派工令）· [`README-v3.0-archive.md`](./README-v3.0-archive.md)（v3.0 版总纲存档，**未删**）

---

## ⚠ 全卷勘误（2026-09-27 · 本机实测 · v5.0 增补至 5 条）

> 以下 5 条为**硬事实**。全书（含 chapters / cookbook / faq / sop / case 五卷）出现与之冲突的写法，**一律以本节为准**。

### 勘误 1 · 配置真身

```bash
# ✅ 真身
~/.openclaw/openclaw.json            # 45,662 字节（2026-09-27 实测）· 1,871 行
# ❌ 不存在
~/.openclaw/workspace/openclaw.json  # 早期版本多处误写；本机实测该路径不存在
```

应用根 `~/.openclaw/` 与工作区 `~/.openclaw/workspace/` 是**两级结构**：配置文件在应用根，skills / agents / backups 在工作区。

### 勘误 2 · 真实顶层 key 共 20 个

```
acp · agents · auth · bindings · browser · channels · commands · env · gateway
logging · memory · messages · meta · models · plugins · session · skills · talk · tools · wizard
```

早期版本多处声称的 `runtime / workspace / routing / heartbeat / subagents` **五个顶层字段实测不存在**——真实路径在**子层级**：

| 误写（顶层） | 真实路径（子层级） |
|---|---|
| `runtime` | 无对应顶层字段；运行时信息散落 `meta` / `gateway` |
| `workspace` | `agents.entries.<id>.workspace` |
| `routing` | `bindings`（顶层）+ `channels.<ch>.requireMention` |
| `heartbeat` | `agents.entries.<id>.heartbeat.every`（**per-agent，非全局**） |
| `subagents` | `agents.entries.<id>` 之间的协同，无独立顶层字段 |

### 勘误 3 · 命令真名对照表

| ❌ 伪命令 | ✅ 真名 | 说明 |
|---|---|---|
| `openclaw chat --agent X --prompt Y` | `openclaw agent --agent X --message Y` | **不是** `chat`；**不是** `--prompt` |
| `openclaw agents health-check` | `openclaw doctor` / `openclaw health` | 无 `health-check` 子命令 |
| `openclaw cron add --schedule … --target … --prompt …` | `openclaw cron add --cron … --session … --message …` | flag 真名；`--schedule/--target/--prompt` 实测**不存在** |
| `openclaw init` | `openclaw setup` | 初始化向导真名 |
| `openclaw agents create <name>` | `openclaw agents add <name>` | 无 `create` |
| `openclaw agents archive` | `openclaw backup create` | 归档真名 |
| `openclaw plugin install …`（单数） | `openclaw plugins install …`（**复数**） | plugin 子命令族全部复数；共 15 个 |
| `openclaw plugins` 15 子命令 | `build / disable / doctor / enable / init / inspect / install / list / marketplace / pack / registry / search / uninstall / update / validate` | 2026-09-27 实测清单 |

### 勘误 4（**v5.0 新增**）· cookbook 曾用 `chat --prompt`——42 处已修正

v5.0 编写期，`cookbook/` 七分册初稿批量沿用了伪命令 `openclaw chat --agent <X> --prompt <Y>`。

- **发现者**：P0-5（真名复核 sub-agent）
- **影响面**：`cookbook/` 7 文件 · **42 处**
- **修正**：全书统一替换为 `openclaw agent --agent <X> --message <Y>`；并在 `cookbook/01-protocol-SOUL.md` 的「验证步骤」段加了单引号 heredoc 用法说明（`'EOF'` 防 shell 展开）
- **教训**：`chat` 是 OpenClaw **历史口语**，从未是 CLI 子命令；凡以「复制粘贴可跑」为卖点的代码块，**必须逐个真跑**

### 勘误 5（**v5.0 新增**）· `00-getting-started` 纠正 5 个虚构命令

零基础入门卷（P0-3）首稿出现 5 个**不存在的命令**，已在定稿前逐条替换：

| # | 虚构命令 | 真名 | 出自 |
|---|---|---|---|
| 1 | `openclaw init` | `openclaw setup` | `00-environment-checklist.md` |
| 2 | `openclaw agents create` | `openclaw agents add` | `01-quickstart-5min.md` |
| 3 | `openclaw agent health` | `openclaw health` | `01-quickstart-5min.md` |
| 4 | `openclaw skills reload` | 无此命令（skill 为目录扫描式加载，无 reload） | `02-first-agent-walkthrough.md` |
| 5 | `openclaw config set …` | `openclaw config`（无 `set` 子命令；配置写入走 `openclaw agents` / plugin CLI 的 `--set` 或直接编辑 `openclaw.json`） | `06-common-pitfalls.md` |

> **零容忍红线**：`reserveTokensFloor` 与作废版本号 `2026.3.2` 在全书任何文件的命中数**必须为 0**（`grep -rc` 可验；`reserveTokensFloor` 仅允许作为「原误植」反向引用出现）。

---

## 一句话定位

> **v5.0 行业标准版 = 把丘总内部手册《硅基生命训练学·八卷体系》改造为一本「手册型」的 AI Agent 训练学行业标准底座——在 v1.0/v4.0 的 8 卷论述体系之上，补齐业界入门（7 节）、可复制配方（30 例）、百级问答（102 问）、独立 SOP 大全（30 套）、8 段式案例库（10 例）五大实战模块，使新书从「有人写哲学、无人写手册」跨到「既能读、又能跑、还能查、更能查完照做」。**

三条硬指标（v1.0/v4.0/v5.0 均为本机实测）：

| 指标 | v1.0 | v4.0 | **v5.0** |
|---|---|---|---|
| 可复制配方（Cookbook） | 0 | 0 | **30 例** |
| 问答库（FAQ） | 0 独立节 | 0 独立节 | **102 问** |
| 独立 SOP 卷 | 无（散落 488 处字面命中） | 无（散落 610 处） | **30 套 · 6 分册** |

---

## 4. 为什么是 v5.0（v1.0 → v4.0 → v5.0 演进表）

### 4.1 三版对照（全部本机实测，非估算）

| 维度 | v1.0 | v4.0 | **v5.0（本版）** |
|---|---|---|---|
| **总行数** | 38,518 | 36,175 | **53,258** |
| **文件数** | 83 | 111 | **59** |
| **结构** | 8 卷（volume-01…08）+ INDEX | 8 卷 + **4 接口层**（09-a2a / 09-mcp / 09-plugin / 09-skill）+ README | **8 卷 + 4 接口层 + 5 新卷**（入门 / Cookbook / FAQ / 案例 / SOP）+ API 参考（在跑） |
| **章节组织** | 74+ 篇散点（按模块平铺） | 按卷分目录，141 个文件散点 | **12 章统一编号**（00-front … 12-plugin-entrypoint）+ 每章含 SOP 节 + 常见错误 + 新手坑 + 扩展阅读 |
| **FAQ** | 0（独立节 0；字面命中 15） | 0（独立节 0；字面命中 9） | **102 问** · 7 分类 · 四段式（现象→原因→解法→验证） |
| **Cookbook** | 0（独立节 0） | 1（独立节 1；字面命中 246） | **30 例**（C1-1 ~ C7-4）· 六段式（背景→配置→验证→实测环境→排坑→进阶） |
| **SOP** | 无独立节（字面命中 488） | 无独立节（字面命中 610） | **30 套 SOP** · 独立卷 · 8 段式 · 每套含回滚步骤 |
| **案例库** | 1 处（字面命中 26） | 数处（字面命中 4） | **10 例** · 8 段式 + 附录 A-F（含自测题 + 不适用边界） |
| **API 参考** | 无 | 无 | 🔶 **7 文件在跑**（CLI / Config / Protocol / MCP / A2A / Skill） |
| **零基础入门** | 无 | 无 | **7 节 · 3,077 行**（环境清单 / 5min quickstart / 第一个 Agent / 术语表 / 四根问题 / 阅读路线图 / 43 坑库） |
| **术语规范** | 中文黑话 | 35 条改名表 | 35 条改名表 + **全书首现双写**（`标准名（原：黑话）`） |
| **业界对位** | 未对位 | 8 卷 vs 6 框架叠代表 | 8 卷 + 5 新卷 vs **7 个业界项目**逐项对位矩阵 |
| **新增总量** | — | — | **净增 17,083 行**（53,258 − 36,175），文件数反降 52（111 → 59，**合并而非常规膨胀**） |

> **反直觉但真实**：v5.0 文件数 **59 < v4.0 的 111**，行数却 **53,258 > v4.0 的 36,175**。
> 原因：v4.0 是「141 个碎片文件平铺」，v5.0 是「8 大模块 + 单文件多例」——**每文件承载密度提升约 2.6 倍**（v4.0 平均 326 行/文件 → v5.0 平均 903 行/文件）。

### 4.2 为什么要「改造」而不是「继续补丁」

| v4.0 的真实缺口（实测证据） | v5.0 的对策 | 落点 |
|---|---|---|
| 02–07 核心章每章仅 59–149 行，新人无从下手 | 全部回填至 **1,086–1,177 行/章** | [`chapters/00-front/00-总论.md`](./chapters/00-front/00-总论.md) |
| FAQ 字面命中仅 1 处，等于清零 | **102 问**独立卷，四段式 | [`faq-troubleshooting/README.md`](./faq-troubleshooting/README.md) |
| Cookbook 独立节 0/1/0 | **30 例**独立卷，六段式 | [`cookbook/01-protocol-SOUL.md`](./cookbook/01-protocol-SOUL.md) |
| SOP 从 v4.0 的 610 处字面命中掉到 37 处 | **30 套**独立 SOP 卷 + 每章 SOP 节 | [`sop-library/README.md`](./sop-library/README.md) |
| 真实案例仅 1 处 | **10 例** 8 段式 + 自测题 | [`case-library/01-real-incidents.md`](./case-library/01-real-incidents.md) |
| 三版均无新人 quickstart / 术语表 | **7 节 3,077 行**零基础入门卷 | [`00-getting-started/README.md`](./00-getting-started/README.md) |
| 三版均无 API 参考 | 🔶 7 文件在跑 | `api-reference/` |

### 4.3 v5.0 的改造优先级（丘总拍板）

| 批次 | 内容 | 交付状态 |
|---|---|---|
| **P0** | FAQ 102 问 + Cookbook 前 15 例 + 零基础入门章 + 每章 SOP 节 | ✅ 已完成 |
| **P1** | Cookbook 后 15 例 + 每章三小节（常见错误/新手坑/扩展阅读）+ 案例库 10 例 | ✅ 已完成 |
| **P2** | SOP 大全独立卷 + API 参考附录 + 薄章回填 | 🟡 SOP 卷 ✅ / API 参考 🔶 在跑 |
| **P3（放最后）** | 练习题库 | ⬜ 未启动（按丘总指令「练习题库放最后」） |

---
## 5. v5.0 八大模块导航（核心章节）

> **本节的每一个行数、文件数均为本机 `wc -l` / `find` 实测**（2026-09-27），非估算、非承袭旧版。
> **总览表**：

| # | 模块 | 文件数 | 行数 | 占比 | 定位 | 入口 |
|---|---|---|---|---|---|---|
| ① | **00-getting-started** | 8 | **3,077** | 5.8% | 零基础入门（第零章） | [README](./00-getting-started/README.md) |
| ② | **chapters** | 23 | **21,855** | 41.0% | 12 章正文（8 卷 + 4 接口层） | [00-总论](./chapters/00-front/00-总论.md) |
| ③ | **cookbook** | 7 | **12,548** | 23.6% | 30 例可复制配方 | [C1-1](./cookbook/01-protocol-SOUL.md) |
| ④ | **faq-troubleshooting** | 9 | **4,280** | 8.0% | 102 问故障速查 | [卷首](./faq-troubleshooting/README.md) |
| ⑤ | **case-library** | 2 | **4,562** | 8.6% | 10 例 8 段式案例 | [01-真实事故](./case-library/01-real-incidents.md) |
| ⑥ | **sop-library** | 7 | **6,286** | 11.8% | 30 套独立 SOP | [总索引](./sop-library/README.md) |
| ⑦ | **api-reference** | 🔶 在跑 | 🔶 在跑 | — | CLI / Config / Protocol / MCP / A2A / Skill | 🔶 未交付 |
| ⑧ | **术语与元文档** | 2 | **410** | 0.8% | 35 条改名表 + 主编报告 | [术语表](./00-术语对照表·v3.0行业标准版.md) |
| | **合计（不含 API 参考）** | **59** | **53,258** | 100% | — | — |

---

### ① 00-getting-started · 零基础入门（**8 文件 · 3,077 行**）

**一句话说明**：让一个从没碰过 OpenClaw 的人，**5 分钟跑起第一个 Agent，一章理解「为什么要训 Agent 而不是养 AI」**。

**适合谁读**：完全的新人、产品经理、非工程背景的团队负责人、想快速评估这本手册值不值得投入的人。

| 节 | 文件 | 行数 | 主题 |
|---|---|---|---|
| 0.0 | [README.md](./00-getting-started/README.md) | 56 | 章目录 + 推荐阅读顺序 + 硬约束 |
| 0.1 | [00-environment-checklist.md](./00-getting-started/00-environment-checklist.md) | 454 | 环境准备清单（8 步实操 + 8 条验证命令） |
| 0.2 | [01-quickstart-5min.md](./00-getting-started/01-quickstart-5min.md) | 614 | **5 分钟 quickstart**（6 步复制粘贴即跑 + 8 坑 + 时长拆解） |
| 0.3 | [02-first-agent-walkthrough.md](./00-getting-started/02-first-agent-walkthrough.md) | 510 | 第一个 Agent 全流程（SOUL → AGENTS → 跑 → 体检） |
| 0.4 | [03-glossary.md](./00-getting-started/03-glossary.md) | 322 | 术语表（黑话 → 行业标准双语，35+ 条 + 反向索引 + 一页速记） |
| 0.5 | [04-four-root-questions.md](./00-getting-started/04-four-root-questions.md) | 404 | 训练学四根问题（一致性 / 持续性 / 规模化 / 资产化） |
| 0.6 | [05-reading-roadmap.md](./00-getting-started/05-reading-roadmap.md) | 306 | **全书阅读路线图**（四条路线 + 全景图 + 30 天计划 + 前置依赖图） |
| 0.7 | [06-common-pitfalls.md](./00-getting-started/06-common-pitfalls.md) | 411 | 常见错误 + 新手坑（**43 坑库**：环境 / 命令 / 协议 / 术语 / 方法 / 平台 + 决策树） |

**对位业界**：LangChain quickstart（约 4,076 词）· OpenAI Cookbook 首页索引。

**特色**：每节统一「6 段式」结构：背景 → 配置 → 验证 → 实测环境 → 排坑 → 进阶。

---

### ② chapters · 12 章正文（**23 文件 · 21,855 行**）

**一句话说明**：全书主体——**8 卷训练学（哲学 + 工程 + 治理）+ 4 接口层（MCP / A2A / Skill / Plugin）**，每章含 SOP 节 + 常见错误 + 新手坑 + 扩展阅读。

**适合谁读**：所有人（第 2 章「系统骨架」不可跳，是全书地基）。

> ⚠️ **目录名 ≠ 章号**：目录名是**作者侧编号**，章节标题是**读者侧编号**，二者差 1（`00-front` = 总论，`02-protocols` = 第 1 章）。**以章节标题为准**。

#### 8 卷训练学（哲学 + 工程 + 治理）

| 章 | 文件 | 行数 | 一句话 | 差异化 |
|---|---|---|---|---|
| 总论 | [00-front/00-总论.md](./chapters/00-front/00-总论.md) | 1,290 | 业界无「AI 训练哲学」赛道；这是全书宪法 | ⚡优势 5（第 0 章引出） |
| 第 1 章 | [02-protocols/02-七大契约.md](./chapters/02-protocols/02-七大契约.md) | 1,183 | 7 协议（SOUL/AGENTS/USER/TOOLS/IDENTITY/HEARTBEAT/MEMORY）= agent 的宪法 | — |
| 第 2 章 | [03-skeleton/03-系统骨架.md](./chapters/03-skeleton/03-系统骨架.md) | 1,196 | OpenClaw 子系统逐一解剖 + **真名验证**（`effectiveReserveTokens` / `MAX_COMPACTION_RESERVE_RATIO=0.25`） | — |
| 第 3 章 | [04-training/04-训练流程.md](./chapters/04-training/04-训练流程.md) | 1,088 | 教练机制 + 双三角模型（Expectation-Actuality-Feedback Loop） | 业界无此层 |
| 第 4 章 | [05-long-term/05-长期表现.md](./chapters/05-long-term/05-长期表现.md) | 1,126 | 记忆分层、漂移治理、主动性边界三档、每周体检 | ⚡**优势 2 + 3** |
| 第 5 章 | [06-governance/06-治理系统.md](./chapters/06-governance/06-治理系统.md) | 1,177 | TEV（三证据验证）+ 信任评分 + 功绩账本 + 修复工单 | ⚡**优势 4** |
| 第 6 章 | [07-coordination/07-协同军团.md](./chapters/07-coordination/07-协同军团.md) | 1,134 | SLCP + 反脆弱三层 + 三省评审制 + 响应让渡协议 | ⚡**优势 1 + 4** |
| 第 7 章 | [08-evolution/08-超维演进.md](./chapters/08-evolution/08-超维演进.md) | 1,086 | OODA + 技能基因 + 自主目标生成（响应型 → 提案型） | ⚡**优势 5** |

#### 4 接口层（对接业界标准）

| 章 | 文件 | 行数 | 一句话 |
|---|---|---|---|
| 第 8 章 | [09-mcp-binding/09-MCP绑定.md](./chapters/09-mcp-binding/09-MCP绑定.md) | **2,353** | 接入 MCP 工具层（本机实测 **0 个 OpenClaw-managed MCP server**，基线诚实标注） |
| 第 9 章 | [10-a2a-binding/10-A2A绑定.md](./chapters/10-a2a-binding/10-A2A绑定.md) | **2,797**（全书最厚单文件） | SLCP 跑在 A2A v1.0 上 + Agent Card `supported_interfaces: ["a2a/v1","slcp/v1"]` |
| 第 10 章 | [11-skill-registry/README.md](./chapters/11-skill-registry/README.md) | 1,277 | 对齐 Anthropic Skills 标准（SKILL.md YAML frontmatter） |
| 第 11 章 | [12-plugin-entrypoint/README.md](./chapters/12-plugin-entrypoint/README.md) | 1,413 | `openclaw plugins install` 入口 + `openclaw.plugin.json`（JSON5） |

#### 接口层的支撑文件（11/12 章分目录展开）

| 文件 | 行数 | 内容 |
|---|---|---|
| [11-skill-registry/11-Skill注册.md](./chapters/11-skill-registry/11-Skill注册.md) | 52 | 章节状态 + 派工令（⚠ 本章正文实际落在同目录 README.md） |
| [11-skill-registry/Registry-表.md](./chapters/11-skill-registry/Registry-表.md) | 605 | 本机 9 个代表 skill 一手实测 Registry 表 + 字段覆盖率雷达 |
| [11-skill-registry/SKILL.md-frontmatter-规范.md](./chapters/11-skill-registry/SKILL.md-frontmatter-规范.md) | 382 | 6 字段矩阵（实拉 agentskills.io/specification）+ 最小/完整骨架 |
| [11-skill-registry/Anthropic-Skills-实拉对位.md](./chapters/11-skill-registry/Anthropic-Skills-实拉对位.md) | 322 | GitHub API 元数据一手验证 + anthropics/skills 内置 19 个 skill |
| [11-skill-registry/8卷Skill写法适配.md](./chapters/11-skill-registry/8卷Skill写法适配.md) | 590 | v1.0 隐喻层 → v5.0 工程层的 Skill 化映射 |
| [11-skill-registry/真名验证与勘误.md](./chapters/11-skill-registry/真名验证与勘误.md) | 346 | 4 条独立证据 + 3 条勘误 + v5.0 banner 终稿 |
| [12-plugin-entrypoint/install-指南.md](./chapters/12-plugin-entrypoint/install-指南.md) | 570 | 5 阶段安装指南（脚手架 → metadata → pack → 校验 → 发布） |
| [12-plugin-entrypoint/配置项.md](./chapters/12-plugin-entrypoint/配置项.md) | 366 | `configSchema` 13 配置项总表 + uiHints + 10 高频场景 |
| [12-plugin-entrypoint/8卷挂载映射.md](./chapters/12-plugin-entrypoint/8卷挂载映射.md) | 266 | 8 卷 → Plugin 挂载点完整清单 + 卷间依赖图 |
| [12-plugin-entrypoint/OpenClaw-官方RFC-草案.md](./chapters/12-plugin-entrypoint/OpenClaw-官方RFC-草案.md) | 420 | **RFC SLT-001**（Plugin Manifest Extension for Silicon-Life Training） |
| [12-plugin-entrypoint/真名验证与勘误.md](./chapters/12-plugin-entrypoint/真名验证与勘误.md) | **816**（全书最厚单文件） | 8 条真名 + 13 子命令 `--help` 完整清单 + 与 v1.0/v4.0 差异表 |
| [12-plugin-entrypoint/openclaw.plugin.json](./chapters/12-plugin-entrypoint/openclaw.plugin.json) | （非 .md） | Plugin manifest 实证（JSON5） |

---

### ③ cookbook · 实战 Cookbook（**7 文件 · 12,548 行 · 30 例**）

**一句话说明**：OpenAI Cookbook 范式落地——**每个配方解决一个具体问题，复制 → 粘贴 → 能跑**；每例统一「六段式」：背景 → 配置（完整可复制）→ 验证步骤 → 实测环境 → 排坑 → 进阶。

**适合谁读**：要马上动手的工程师 / 运维；遇到具体协议配置问题的所有人。

| 分册 | 文件 | 行数 | 例数 | 覆盖 |
|---|---|---|---|---|
| C1 | [01-protocol-SOUL.md](./cookbook/01-protocol-SOUL.md) | 1,668 | 5 | 协议配置（SOUL / AGENTS / USER / TOOLS / IDENTITY） |
| C2 | [02-protocol-HEARTBEAT-MEMORY.md](./cookbook/02-protocol-HEARTBEAT-MEMORY.md) | 1,712 | 5 | 心跳 / Cron / MEMORY / Compaction / 漂移检测 |
| C3 | [03-skills-tools-mcp.md](./cookbook/03-skills-tools-mcp.md) | 2,076 | 5 | Skill / Tool / MCP / A2A / Plugin manifest |
| C4 | [04-training-rounds.md](./cookbook/04-training-rounds.md) | 1,426 | 4 | 训练轮次 / 双三角 / Mentor Agent / 分层记忆 |
| C5 | [05-drift-governance.md](./cookbook/05-drift-governance.md) | 1,507 | 4 | 漂移检测 / 主动性边界 / 每周体检 / TEV |
| C6 | [06-coordination-fleet.md](./cookbook/06-coordination-fleet.md) | 1,610 | 3 | Supervisor Layer / THP 任务交接 / 响应让渡 |
| C7 | [07-production-ops.md](./cookbook/07-production-ops.md) | 2,549 | 4 | 18 Agent 编制 / 事故复盘 / cron 编排 / 生产监控 |

#### 30 例总目录（C1-1 ~ C7-4）

| # | 配方 | # | 配方 |
|---|---|---|---|
| C1-1 | SOUL.md 配置：从空白文件到军团级 SOUL | C4-1 | 训练轮次设计：从 L1 到 L3 的完整训练计划 |
| C1-2 | AGENTS.md 配置：含 tools / Skills 段 | C4-2 | 双三角模型实操（EAF Loop 落地） |
| C1-3 | USER.md 配置：4 类问题 + 5 个反例 | C4-3 | 导师智能体（Mentor Agent）机制配置 + 训练记录 |
| C1-4 | TOOLS.md 配置：与 SOUL 的协作规则 | C4-4 | 分层记忆 5 层金字塔实操 |
| C1-5 | IDENTITY.md 配置：可识别身份 + 路由字段 | C5-1 | 漂移检测实操：`drift_scan.py` 完整脚本 + 阈值配置 |
| C2-1 | HEARTBEAT.md 配置：3 档心跳频率 | C5-2 | 主动性边界三档制：Allowed / Forbidden / Needs-Confirm |
| C2-2 | Cron 配置：含 9 类心跳 + `drift_check` | C5-3 | 每周体检：cron plist + `launchctl` 实操 + 清单 |
| C2-3 | MEMORY.md 配置：5 层记忆金字塔 | C5-4 | TEV 三证据验证实操：证据采集 + 验收报告 |
| C2-4 | Compaction 配置：含 `reserveTokens` 三者并存 | C6-1 | 多智能体编排搭建：Supervisor Layer 调度中枢 |
| C2-5 | 漂移检测配置：含 6 层漂移链 | C6-2 | 任务交接协议（THP）实操：任务卡字段 + 验收闭环 |
| C3-1 | Skill 注册：完整 SKILL.md 写法（YAML frontmatter） | C6-3 | 响应让渡协议（RYP）实操：抢活判定 + 让位 YAML |
| C3-2 | Tool 注册：含 manifest + 工具调用 schema | C7-1 | 智能体集群真实编制：18 Agent 花名册 + 路由表 + binding |
| C3-3 | MCP 接入：8 卷 → 46 MCP 原语映射 | C7-2 | 生产事故复盘实操（8/19 断线 + 9/21 飞书） |
| C3-4 | A2A 接入：SLCP 反脆弱三层配置 | C7-3 | cron 编排实操：晨扫 / 日报 / 暗夜熔炉 |
| C3-5 | Plugin manifest 配置：`openclaw.plugin.json` | C7-4 | 生产监控实操：heartbeat error 计数 + 告警链 |

> **验收硬标准**：每个配方必须满足「复制 → 粘贴 → 能跑」三原则，并注明实测环境（OpenClaw 版本 + 日期）。**cookbook 曾 42 处使用伪命令 `chat --prompt`，已全部修正**（见勘误 4）。

---

### ④ faq-troubleshooting · FAQ + 故障排查（**9 文件 · 4,280 行 · 102 问**）

**一句话说明**：把 18 个 agent 在 OpenClaw 上跑起来、跑得稳、跑得不漂移的**全部已知坑**，按「**现象 → 原因 → 解法 → 验证命令**」四段式固化；区别于业界 getting-started：**每问带本机可执行命令，每条结论标已实测 / ⏳ 待实测**。

**适合谁读**：所有人（on-call 必读）；「装了但报错先救火」→ 直接跳 Top 20。

| 分类 | 文件 | 行数 | 问题数 | 典型症状 |
|---|---|---|---|---|
| — | [README.md](./faq-troubleshooting/README.md)（卷首） | 304 | — | 七分类速查 + 3 步用法 + **问题上报流程** |
| ⚡ | [F-Top20-高频速查.md](./faq-troubleshooting/F-Top20-高频速查.md) | 322 | **20** | **先看这个**：20 问表格速查 + 可打印速查卡 |
| F1 | [F1-环境与安装.md](./faq-troubleshooting/F1-环境与安装.md) | 429 | **12** | 命令找不到 / 版本对不上 / 模型报错 / 权限没开 |
| F2 | [F2-协议-SOUL-AGENTS-USER.md](./faq-troubleshooting/F2-协议-SOUL-AGENTS-USER.md) | 534 | **15** | 人格串味 / 声明了不认账 / 协议不生效 |
| F3 | [F3-心跳与定时.md](./faq-troubleshooting/F3-心跳与定时.md) | 546 | **15** | 该醒没醒 / 到点没跑 / 守护起不来 / 重复执行 |
| F4 | [F4-记忆与会话.md](./faq-troubleshooting/F4-记忆与会话.md) | 550 | **15** | 忘了前面的话 / 记忆串味 / 搜不到 / 越聊越贵 |
| F5 | [F5-Skills-Tools-MCP.md](./faq-troubleshooting/F5-Skills-Tools-MCP.md) | 564 | **15** | skill 不加载 / MCP 连不上 / tools 空 / 分发合规 |
| F6 | [F6-多Agent协同.md](./faq-troubleshooting/F6-多Agent协同.md) | 516 | **15** | 抢答刷屏 / 让位失效 / 死锁 / 通道断线 / 路由错人 |
| F7 | [F7-治理漂移体检.md](./faq-troubleshooting/F7-治理漂移体检.md) | 515 | **15** | 文档漂移 / 人格漂移 / 体检不通过 / 工单没人跟 |
| **Σ** | — | **4,280** | **102 + Top20** | — |

**分类速判口诀**（贴墙用）：

```
报错 / 装不上 / 连不上      → F1 环境
人格 / 身份 / 权限不对       → F2 协议
该动的时候不动              → F3 心跳
记不住 / 记错 / 变慢了      → F4 记忆
说找不到某能力              → F5 skill/tool
多个 Agent 打起来           → F6 协同
慢慢变得不像自己            → F7 治理
```

**本卷独有**：¶4「问题上报流程」——把新问题走**修复工单（Remediation Ticket，原：整改单）**闭环后固化为 FAQ 条目；30 天内被 ≥2 人次上报 → **晋升进 Top 20**。

---

### ⑤ case-library · 实战案例库（**2 文件 · 4,562 行 · 10 例**）

**一句话说明**：10 个真实案例，统一「**8 段式**」：案例速览 → 事件时间线 → 根因分析（5 Whys）→ 当时的错误决策 → 修复过程 → 修复后验证 → 沉淀的机制 → 如果你的系统遇到同样问题；每例另附**附录 A–F**（本机实测证据 / 读者自测 8 题 / 交叉引用 / **不适用边界（诚实）**）。

**适合谁读**：运维 / 治理员 / 想从别人的血案里省下自己学费的人；「为什么这么设计」的追问者。

| 文件 | 行数 | 案例 | 主题 |
|---|---|---|---|
| [01-real-incidents.md](./case-library/01-real-incidents.md)「真实事故卷」 | 2,284 | **CASE-1** | 8/19 军团断线：模型级联失败全链路复盘 |
| | | **CASE-2** | 9/21 飞书事故：`requireMention` 配置血案 |
| | | **CASE-3** | 18 坏 skill 修复：8 个 P0 stub + frontmatter 缺失批量治理 |
| | | **CASE-4** | 能力矩阵 26 天未续期：治理机制空转诊断 |
| | | **CASE-5** | PR #152777 卡住：上游依赖阻塞的决策路径 |
| [02-production-patterns.md](./case-library/02-production-patterns.md)「生产模式卷」 | 2,278 | **CASE-6** | 18 agent 生产编制：从 1 到 18 的扩张路径 |
| | | **CASE-7** | 编排节奏设计：晨扫 → 日报 → 暗夜熔炉的一天 |
| | | **CASE-8** | 蘑菇街式冷启动：新 agent 上线 7 天训练全记录 |
| | | **CASE-9** | 心跳熔断实战：heartbeat error 70x / 99+x 的诊断与修复 |
| | | **CASE-10** | 51/69 插件启用策略：a2a 插件为何 disabled |

> **卷首立场**：前五例**全是事故**——因为「成功的路径各有各的运气，失败的路径高度可复现」。

---

### ⑥ sop-library · SOP 大全卷（**7 文件 · 6,286 行 · 30 套 SOP**）

**一句话说明**：30 个端到端可操作的标准操作程序（Standard Operating Procedure），每套统一「**8 段式**」：目的 / 适用对象 / 前置条件 / 操作步骤（6 步 + 检查清单）/ 验证命令 / **回滚步骤** / 相关 SOP 链接 / 诚实边界。

**适合谁读**：运维 / on-call / 治理员 / 培训师；任何人要「照做一遍就能配出来」时。

| 分册 | 文件 | 行数 | SOP | 覆盖 |
|---|---|---|---|---|
| — | [README.md](./sop-library/README.md)（总索引） | 1,007 | — | 30 SOP 总目录 + 决策树 + 互链全图 + **20 张速查卡** |
| 01 | [01-environment-setup-sop.md](./sop-library/01-environment-setup-sop.md) | 934 | **SOP-1~5** | 环境与安装 |
| 02 | [02-protocol-config-sop.md](./sop-library/02-protocol-config-sop.md) | 918 | **SOP-6~10** | 协议配置 |
| 03 | [03-heartbeat-monitor-sop.md](./sop-library/03-heartbeat-monitor-sop.md) | 846 | **SOP-11~15** | 心跳与监控 |
| 04 | [04-memory-training-sop.md](./sop-library/04-memory-training-sop.md) | 818 | **SOP-16~20** | 记忆与训练 |
| 05 | [05-drift-governance-sop.md](./sop-library/05-drift-governance-sop.md) | 926 | **SOP-21~25** | 漂移与治理 |
| 06 | [06-incident-recovery-sop.md](./sop-library/06-incident-recovery-sop.md) | 837 | **SOP-26~30** | 事故与恢复 |

#### 30 套 SOP 全清单

| SOP | 标题 | SOP | 标题 |
|---|---|---|---|
| SOP-1 | 安装 OpenClaw 2026.9.x | SOP-16 | MEMORY 5 层金字塔配置 |
| SOP-2 | 多设备同步（节点配对） | SOP-17 | Compaction 配置（上下文压缩） |
| SOP-3 | 沙箱环境搭建 | SOP-18 | 训练轮次（L1 → L3） |
| SOP-4 | 升级 OpenClaw（2026.3.x → 2026.9.x） | SOP-19 | 双三角模型（EAF Loop） |
| SOP-5 | 卸载与清理 | SOP-20 | Mentor Agent 配置 |
| SOP-6 | SOUL.md 配置 | SOP-21 | 漂移检测（Drift Scan） |
| SOP-7 | AGENTS.md 配置 | SOP-22 | 边界三档制（Allowed / Forbidden / Needs-Confirm） |
| SOP-8 | USER.md 配置 | SOP-23 | 每周体检（Weekly Compliance Review） |
| SOP-9 | TOOLS.md 配置 | SOP-24 | TEV 三证（Three-Evidence Verification） |
| SOP-10 | IDENTITY.md 配置 | SOP-25 | 整改工单（Remediation Ticket） |
| SOP-11 | HEARTBEAT 三档频率配置 | SOP-26 | 事故分级（P0-P3） |
| SOP-12 | Cron 配置（定时任务） | SOP-27 | 抢活让位（Response Yield Protocol） |
| SOP-13 | 监控告警链 | SOP-28 | 数据回滚（Point-in-time Recovery） |
| SOP-14 | 暗夜熔炉演练（Night Forge / GameDay） | SOP-29 | 跨 agent 迁移 |
| SOP-15 | 失联恢复（Failover / Reconnection） | SOP-30 | 年度大修（Annual Maintenance） |

#### 五条推荐执行主线

| 主线 | 路径 | 场景 |
|---|---|---|
| 1 · 首次部署（0 → 1） | SOP-1 → SOP-3 → SOP-11 → SOP-12 → SOP-13 | 新机装 OpenClaw |
| 2 · 扩展 agent（1 → 18） | SOP-10 → SOP-6 → SOP-7 → SOP-8 → SOP-9 → SOP-16 → … → SOP-20 | 新加 agent + 训练 |
| 3 · 稳态运维（周节律） | SOP-11（持续）→ SOP-12 → SOP-13 → SOP-23（周一）→ SOP-14（双周） | 生产中 |
| 4 · 响应事故（被动触发） | SOP-13（告警）→ SOP-15（恢复）→ SOP-26（定级）→ SOP-27/28/29 → SOP-25（工单） | P0/P1 事故 |
| 5 · 年度大修（主动节奏） | SOP-30 → SOP-23 → SOP-26 → SOP-4 → 回到 SOP-1 | 年终 |

---

### ⑦ api-reference · API 参考（🔶 **在跑 · 尚未交付**）

**一句话说明**：对标 LlamaIndex 式 API 参考（762 页），交付 **7 文件**：CLI / Config / Protocol / MCP / A2A / Skill 参考。

**当前真实状态（诚实标注）**：

```bash
$ ls -la api-reference/
total 0
drwxr-xr-x@ 2 peterqiu staff 64 9月 28 00:05 .
drwxr-xr-x@ 13 peterqiu staff 416 9月 28 00:05 ..
```

- 目录已建，**当前 0 个 `.md` 文件**（2026-09-27 实测）。
- 本 README 在此**不提供指向 api-reference 的文件链接**——避免制造 broken link。
- 目录建好后，本节将补齐：CLI 子命令全表 / `openclaw.json` 20 顶层 key 字段表 / 7 协议文件模板 / MCP 14 子命令 / A2A Agent Card schema / SKILL.md 6 字段规范。

**适合谁读**：接口集成者、要写 plugin / skill 的开发者。

> **在 api-reference 交付前**，可先读已存在的等价参考：
> - CLI 真名 → [SOP 大全卷 ¶七 速查卡](./sop-library/README.md)（20 张可打印卡）
> - 配置字段 → [12-plugin-entrypoint/配置项.md](./chapters/12-plugin-entrypoint/配置项.md)（`configSchema` 13 项）
> - 真名证据链 → [12-plugin-entrypoint/真名验证与勘误.md](./chapters/12-plugin-entrypoint/真名验证与勘误.md)（13 子命令 `--help` 完整清单）
> - Skill 规范 → [11-skill-registry/SKILL.md-frontmatter-规范.md](./chapters/11-skill-registry/SKILL.md-frontmatter-规范.md)

---

### ⑧ 术语与元文档（**2 文件 · 410 行**）

| 文件 | 行数 | 说明 |
|---|---|---|
| [00-术语对照表·v3.0行业标准版.md](./00-术语对照表·v3.0行业标准版.md) | 127 | **35 条改名对照 + 三层术语架构 + 训练底座使用规范**（宪法附录，全书的术语红线） |
| [00-新书主编报告.md](./00-新书主编报告.md) | 283 | v5.0 架构设计 + 12 章骨架 + 每章 6 项验收标准 + 派工令 + 风险清单 |
| [README-v3.0-archive.md](./README-v3.0-archive.md) | 240 | **v3.0 版总纲存档**（banner / 5 优势 / 8 卷对位 / 立项路径 / 风险清单，未删） |

---
## 6. 三条阅读路径（按角色选一条，别从第一页读到最后一页）

> **结论先行**：**路径没有唯一正确答案，但有一条铁律——[第 2 章 · 系统骨架](./chapters/03-skeleton/03-系统骨架.md)（`chapters/03-skeleton/`）不可跳**。它是全书从「哲学」转入「工程」的枢纽，不懂系统骨架，后面所有接口层章节都会退化成「抄配置」。

---

### 路径 A · 零基础新人（**目标：30 分钟跑起第一个 Agent，1 周内不再踩坑**）

**适合**：没碰过 OpenClaw 的人、产品经理、非工程背景的团队负责人。

```text
① 00-getting-started 全 7 节（3,077 行）
   └─ 0.1 环境清单 → 0.2 5min quickstart → 0.3 第一个 Agent 全流程
      → 0.4 术语表（可提前扫）→ 0.5 四根问题 → 0.6 阅读路线图 → 0.7 坑库
        ↓
② chapters 三章必读（按顺序）
   └─ 00-front/00-总论（1,290 行）→ 02-protocols/02-七大契约（1,183 行）
      → 03-skeleton/03-系统骨架（1,196 行）★ 不可跳
        ↓
③ cookbook C1–C3（5,456 行 · 15 例）
   └─ C1-1~C1-5 协议五件套（SOUL/AGENTS/USER/TOOLS/IDENTITY）
      → C2-1~C2-5 心跳 / Cron / MEMORY / Compaction / 漂移
      → C3-1~C3-5 Skill / Tool / MCP / A2A / Plugin
        ↓
④ faq-troubleshooting/F-Top20-高频速查（322 行 · 20 问）
   └─ 80% 的现场故障，Top 20 里 30 秒能解
```

| 阶段 | 读什么 | 行数合计 | 预计耗时 | 关键产出 |
|---|---|---|---|---|
| ① 入门 | 00-getting-started 全卷 | 3,077 | 2–3 小时 | 一个能跑的 agent + 一张术语地图 |
| ② 地基 | 总论 + 七大契约 + 系统骨架 | 3,669 | 3–4 小时 | 理解 7 协议 + OpenClaw 子系统 + 真名体系 |
| ③ 动手 | cookbook C1–C3 | 5,456 | 4–5 小时 | 5 件套协议文件 + 心跳 cron + 第一个 skill |
| ④ 救火 | F-Top20 | 322 | 30 分钟（按需回查） | 常见故障自愈能力 |
| **Σ** | — | **12,524** | **约 10–12 小时** | **一个「像样」的 agent** |

**新人三不要**：
1. **不要**跳过 00-getting-started 直接读哲学章——没跑过 agent，读不懂「agent 学会想要」。
2. **不要**跳过第 2 章系统骨架直接看 MCP / Plugin——会变成抄配置。
3. **不要**只读不跑——本书标「复制粘贴可跑」的代码块**必须真跑**；跑过的和读过的，是两个世界。

---

### 路径 B · 有经验工程师（**目标：吃透全栈 + 能交付一个符合行业标准的 plugin**）

**适合**：开发者、平台工程师、要写 skill / plugin / MCP server 的人。

```text
① chapters 全 12 章（21,855 行）
   └─ 8 卷训练学（总论 → 七大契约 → 系统骨架 → 训练流程 → 长期表现
      → 治理系统 → 协同军团 → 超维演进）
        ↓ 衔接
      4 接口层（MCP 绑定 2,353 → A2A 绑定 2,797 → Skill 注册 1,277 → Plugin 入口 1,413）
        ↓
② cookbook C4–C7（7,092 行 · 15 例）
   └─ C4 训练轮次 / C5 漂移治理 / C6 协同编排 / C7 生产运维
        ↓
③ api-reference（🔶 在跑 · 交付后补入；当前用等价参考替代）
   └─ CLI 子命令全表 / 20 顶层 key 字段表 / 7 协议模板 / MCP 14 子命令
      / A2A Agent Card schema / SKILL.md 6 字段规范
```

| 阶段 | 读什么 | 行数合计 | 预计耗时 | 关键产出 |
|---|---|---|---|---|
| ① 全栈正文 | chapters 23 文件 | 21,855 | 15–20 小时 | 完整方法论 + 真名体系 + 业界对位 |
| ② 动手 | cookbook C4–C7 | 7,092 | 5–6 小时 | 训练计划 + 治理脚本 + 18 agent 编制 + 事故复盘模板 |
| ③ 参考 | api-reference（待交付） | 🔶 | — | 可查的字段表 / 子命令表 |
| **Σ** | — | **28,947+** | **约 22–28 小时** | **一个符合 MCP / A2A / Anthropic Skills 标准的 OpenClaw plugin** |

**工程师三条捷径**：
- **要 CLI 真名** → [SOP 大全卷 ¶七 速查卡](./sop-library/README.md)（20 张卡，可打印）
- **要配置字段** → [12-plugin-entrypoint/配置项.md](./chapters/12-plugin-entrypoint/配置项.md)
- **要真名证据链** → [12-plugin-entrypoint/真名验证与勘误.md](./chapters/12-plugin-entrypoint/真名验证与勘误.md)（816 行，13 子命令 `--help` 全清单）

---

### 路径 C · 运维 / 治理（**目标：把「感觉在跑」变成「可度量、可回滚、可演练」的稳态**）

**适合**：on-call、运维、治理员、培训师、团队负责人。

```text
① sop-library 全卷（6,286 行 · 30 SOP）
   └─ 按主线读，不要按编号读：
      主线 3 稳态运维（SOP-11/12/13/23/14）
      主线 4 响应事故（SOP-13 → 15 → 26 → 27/28/29 → 25）
      主线 5 年度大修（SOP-30 → 23 → 26 → 4 → 回到 SOP-1）
        ↓
② faq-troubleshooting F6 / F7（1,031 行 · 30 问）
   └─ F6 多 Agent 协同（抢活/让位/死锁/通道断线/路由错人）
      F7 治理漂移体检（文档漂移/人格漂移/体检/工单/TEV）
        ↓
③ case-library 全卷（4,562 行 · 10 例）
   └─ 先读 CASE-1/2/9（事故三连）→ 再读 CASE-6/7（编制与节奏）
      → 最后读 CASE-3/4/5/8/10（skill / 治理 / 上游 / 冷启动 / 插件）
```

| 阶段 | 读什么 | 行数合计 | 预计耗时 | 关键产出 |
|---|---|---|---|---|
| ① SOP | sop-library 全卷 | 6,286 | 6–8 小时 | 30 套可执行 SOP + 回滚路径 + 20 张速查卡 |
| ② 排查 | FAQ F6 + F7 | 1,031 | 2–3 小时 | 协同与治理故障的 30 问解法 |
| ③ 案例 | case-library 全卷 | 4,562 | 4–5 小时 | 10 个 8 段式复盘 + 每个案例的自测 8 题 |
| ④ 回查 | FAQ F3（心跳）+ SOP-13/15 | 1,384 | 按需 | 告警链 + 失联恢复 |
| **Σ** | — | **13,263** | **约 12–16 小时** | **可度量、可回滚、可演练的稳态运维体系** |

**运维「三条闸门」**（F6 共识）：
1. **路由**（bindings）——先保证任务派对人；
2. **让位**（Response Yield Protocol）——再保证不该答的不答；
3. **兜底**（Channel Sentinel + 反脆弱三层）——最后保证有人答不上时系统不死。

---

### 三条路径速查卡（可打印贴桌）

```text
┌─ 路径 A · 零基础新人 ────────────────────────────────┐
│ 00-getting-started(3,077) → 总论/契约/骨架(3,669)   │
│ → cookbook C1-C3(5,456) → F-Top20(322)   ≈10-12h   │
└──────────────────────────────────────────────────────┘
┌─ 路径 B · 有经验工程师 ──────────────────────────────┐
│ chapters 全 12 章(21,855) → cookbook C4-C7(7,092)   │
│ → api-reference(待交付)                    ≈22-28h  │
└──────────────────────────────────────────────────────┘
┌─ 路径 C · 运维 / 治理 ───────────────────────────────┐
│ sop-library(6,286) → FAQ F6/F7(1,031)               │
│ → case-library(4,562) → FAQ F3 + SOP-13/15 ≈12-16h  │
└──────────────────────────────────────────────────────┘
★ 铁律：第 2 章 系统骨架（chapters/03-skeleton/）三条路径都不可跳
```

---

## 7. v5.0 的 6 个差异化优势

> v3.0 有 5 个差异化优势（调研报告 §B，通过率 5/5）。v5.0 **保留全部 5 个 + 新增第 6 个**。
> 以下每条的「业界空缺」结论均来自对 LangChain / LlamaIndex / OpenAI Cookbook / CrewAI / AutoGen / Claude Agent SDK / Anthropic Skills 的逐项对位（见 §9）。

### ⚡ 优势 1：A2A 协议补丁 · 反脆弱三层（SLCP）

| 项 | 内容 |
|---|---|
| **是什么** | ① fallback 健康检查 + primary/fallback 去重（防全军级联失败）② 通道守门员（Channel Sentinel）+ 5min 自愈超时（防网络失效扩散）③ 结构化协同事件日志（让失败/成功模式在 agent 间自动传递） |
| **业界空缺** | A2A v1.0 不管这些；ACP 已合并入 A2A；ANP 太早期 |
| **本书落点** | [第 6 章 协同军团](./chapters/07-coordination/07-协同军团.md) · [第 9 章 A2A 绑定](./chapters/10-a2a-binding/10-A2A绑定.md) · [C3-4](./cookbook/03-skills-tools-mcp.md) · [CASE-1](./case-library/01-real-incidents.md)（真实血案驱动） |
| **验证** | [`sop-library/06-incident-recovery-sop.md`](./sop-library/06-incident-recovery-sop.md) SOP-27 抢活让位 |

### ⚡ 优势 2：漂移治理三件套（Document Drift / Personality Drift / Weekly Health）

| 项 | 内容 |
|---|---|
| **是什么** | ① 文档漂移检测（SOUL.md 是不是还认识自己）② 人格漂移检测（每周体检 + 偏差警告）③ 每周体检清单（heartbeat 健康度 + 记忆一致性 + 任务完成率） |
| **业界空缺** | MemGPT / Letta / Mem0 / Zep **全聚焦「记忆存取」，无人做漂移治理** |
| **本书落点** | [第 4 章 长期表现](./chapters/05-long-term/05-长期表现.md) · [C5-1 `drift_scan.py`](./cookbook/05-drift-governance.md) · [F7 全分类](./faq-troubleshooting/F7-治理漂移体检.md) · [SOP-21](./sop-library/05-drift-governance-sop.md) |
| **实测基线** | 本机 18 agent 扫描：`red=0 / yellow=17 / green=1`、`L3_emergency=32`、`anchor_missing_agents=17`、`retired_residue_agents=16`（C5-1 实测输出） |

### ⚡ 优势 3：主动性边界三档制（Allowed / Forbidden / Needs-Confirm）

| 项 | 内容 |
|---|---|
| **是什么** | 三档**硬边界**；对 agent 的自主行为给出可枚举、可审计、可拒答的边界模型 |
| **业界空缺** | 业界所有 Agent 框架默认「能干的都干」，**无边界概念** |
| **本书落点** | [第 4 章 长期表现](./chapters/05-long-term/05-长期表现.md) · [C5-2 边界 YAML](./cookbook/05-drift-governance.md) · [SOP-22](./sop-library/05-drift-governance-sop.md) · [F7-11 主动性五档治理](./faq-troubleshooting/F7-治理漂移体检.md) |

### ⚡ 优势 4：三省制 + 信任评分 + 功绩账本（Three-Stage Review / Trust Score / Merit Ledger）

| 项 | 内容 |
|---|---|
| **是什么** | ① 提议 / 复核 / 终审**分权**（决策闭环）② 信任评分联动 ③ 功绩账本结算（让协作**可计量**） |
| **业界空缺** | CrewAI / AutoGen「角色协作」无决策分权、无结算 |
| **本书落点** | [第 5 章 治理系统](./chapters/06-governance/06-治理系统.md) · [第 6 章 协同军团](./chapters/07-coordination/07-协同军团.md) · [SOP-20/24/25](./sop-library/README.md) · [C5-4 TEV 实操](./cookbook/05-drift-governance.md) |
| **本机实证** | 已有「军功爵周结算」cron（`cron 0 0 * * 1 @ Asia/Shanghai` · agent=kunlun · 模型 `zai/glm-5.1` · `announce -> telegram`）——**功绩账本的野生实现** |

### ⚡ 优势 5：自主目标生成 · 从「响应型」到「提案型」

| 项 | 内容 |
|---|---|
| **是什么** | Agent 不再被动等任务，而是**主动提案**（trigger → filter → proposal 三段式） |
| **业界空缺** | LangGraph / AutoGen / CrewAI / Claude Agent SDK / OpenAI Agents **全是响应型，无主动提案原语** |
| **本书落点** | [总论](./chapters/00-front/00-总论.md) · [第 7 章 超维演进](./chapters/08-evolution/08-超维演进.md) · [F3-14 自主目标调度](./faq-troubleshooting/F3-心跳与定时.md) |
| **本机实证** | 心跳驱动提案的真实触发器：`heartbeat:tiance` / `heartbeat:kunlun` / `heartbeat:peter`（`openclaw cron list` 实测） |

### ⚡⚡ 优势 6（**v5.0 新增**）：全行业唯一「案例库 + 练习题级」实战体系

| 项 | 内容 |
|---|---|
| **是什么** | ① **10 例 8 段式案例库**（含 5 Whys 根因链 + 错误决策 + 修复验证 + 每例 8 道自测题 + **不适用边界**）② **30 套独立 SOP**（每套含回滚步骤）③ **102 问四段式 FAQ**（现象→原因→解法→验证命令） |
| **业界空缺** | **练习题结构是 7 家全 ❌ 的空白**（LangChain ❌ / Anthropic SDK ❌ / OpenAI Cookbook ❌ / LlamaIndex ❌ / AutoGen ❌ / CrewAI ❌）；「案例库 + SOP 大全 + 练习题级」三位一体**无一家具备** |
| **为什么是壁垒** | 论述型文档谁都能写；**「每条结论必须有验证命令、每个案例必须有自测题、每个 SOP 必须有回滚路径」**是执行纪律，抄不走 |
| **本书落点** | [case-library](./case-library/01-real-incidents.md)（4,562 行）· [sop-library](./sop-library/README.md)（6,286 行）· [faq-troubleshooting](./faq-troubleshooting/README.md)（4,280 行） |
| **待补** | 练习题库（≥50 题）按丘总指令**放在最后（P3）**，未启动 |

---
## 8. 实测纠错清单（**v5.0 独有** · 全书统一口径）

> v1.0 与 v4.0 均**未建立**「实测纠错台账」——错误靠读者自己撞上。v5.0 首次把纠错做成**可核验的清单**：
> 每条给出**错误类型 / 修正数 / 发现者 / 证据 / 全局验证命令**，并使全书口径统一。

### 8.1 纠错总表（本机实测）

| # | 错误类型 | 修正数 | 发现者 | 命中文件 | 全局验证命令 |
|---|---|---|---|---|---|
| 1 | **虚构命令** | **5 个**（全书统一） | **P0-3**（零基础入门 sub-agent） | `00-getting-started/` | `grep -rn "openclaw init\|agents create\|skills reload" --include="*.md" .`→ 期望 0 |
| 2 | **错误配置路径** | **17 处** | **P0-4**（每章 SOP 节 sub-agent） | `chapters/` + `cookbook/` | `grep -rn "workspace/openclaw.json" --include="*.md" .`→ 期望 0（仅允许作反例出现） |
| 3 | **不存在的顶层字段** | **5 个** | **P0-5**（真名复核 sub-agent） | `chapters/03-skeleton` · `02-protocols` · `00-front` | `grep -rn "^.*\b\(runtime\|workspace\|routing\|heartbeat\|subagents\)\b.*顶层" --include="*.md" .` |
| 4 | **cookbook 命令名** | **42 处** | **P0-5** | `cookbook/` 全 7 文件 | `grep -rn "chat --prompt\|chat --agent" --include="*.md" cookbook/`→ 期望 0 |
| 5 | **误植字段 `reserveTokensFloor`** | 全书统一 | P0-3 / P0-4 | 全书 | `grep -rn "reserveTokensFloor" --include="*.md" .`→ 仅允许作「原误植」反向引用 |
| 6 | **作废版本号 `2026.3.2`** | 全书统一 | P0-5 | 全书 | `grep -rn "2026\.3\.2" --include="*.md" .`→ 仅允许作「调研员误报」反例 |

### 8.2 逐条展开（含证据链）

#### 纠错 1 · 虚构命令（5 个 · P0-3 发现）

| 虚构命令 | 真名 | 为什么会被写出来 |
|---|---|---|
| `openclaw init` | `openclaw setup` | 同类工具（`npm init` / `git init`）的心智惯性 |
| `openclaw agents create` | `openclaw agents add` | CRUD 直觉；OpenClaw 用 `add` 不用 `create` |
| `openclaw agent health` | `openclaw health` | 误把 health 当 `agent` 的子命令 |
| `openclaw skills reload` | **无此命令** | skill 是**目录扫描式加载**，无 reload 概念 |
| `openclaw config set …` | `openclaw config`（无 `set`） | `git config --set` 惯性；配置写入走 `agents` / plugins CLI 或直编 `openclaw.json` |

**根因**：LLM 生成文档时会补全「看起来对」的命令。**唯一对策是真跑**——凡带「复制粘贴可跑」承诺的代码块，必须逐个在本机执行。

#### 纠错 2 · 错误配置路径（**17 处** · P0-4 发现）

- **错误写法**：`~/.openclaw/workspace/openclaw.json`
- **真身**：`~/.openclaw/openclaw.json`（45,662 字节 · 1,871 行 · 20 顶层 key）
- **影响面**：17 处，集中在每章 SOP 节的「验证主配置存在」步骤 + cookbook C5/C7 的配置读写段。
- **为什么会写错**：`~/.openclaw/workspace/` 下确实有 `skills/` / `agents/` / `backups/`，直觉上配置文件也该在 workspace 里；但 OpenClaw 是**应用根 + 工作区两级结构**——配置在应用根。
- **修正方式**：全书统一为真身路径，并在每个出现处**附加反例行**（`# ❌ 不存在：~/.openclaw/workspace/openclaw.json`），防止读者再次误植。

#### 纠错 3 · 不存在的顶层字段（**5 个** · P0-5 发现）

| 误报的「顶层字段」 | 真实位置 | 命中章节 |
|---|---|---|
| `runtime` | 无对应顶层字段 | `chapters/03-skeleton` |
| `workspace` | `agents.entries.<id>.workspace` | `chapters/03-skeleton` · `00-front` |
| `routing` | `bindings`（顶层）+ `channels.<ch>.requireMention` | `chapters/02-protocols` · `03-skeleton` |
| `heartbeat` | `agents.entries.<id>.heartbeat.every`（**per-agent**） | `chapters/02-protocols` · `03-skeleton` |
| `subagents` | 无独立顶层字段（靠 `agents.entries` 协同） | `chapters/02-protocols` |

**修正方式**：三章各加「顶层字段 20 个」实测表 + 反例行，并把真身路径（子层级）写进正文。

#### 纠错 4 · cookbook 命令名（**42 处** · P0-5 发现）

- **错误写法**：`openclaw chat --agent <X> --prompt <Y>`
- **真名**：`openclaw agent --agent <X> --message <Y>`
- **影响面**：`cookbook/` 全 7 文件 · **42 处**
- **为什么严重**：cookbook 的全部卖点就是「复制 → 粘贴 → 能跑」。42 处伪命令 = **42 个跑不通的配方**，等于整卷失效。
- **修正方式**：全书统一替换 + 在 [cookbook/01-protocol-SOUL.md](./cookbook/01-protocol-SOUL.md) 补 heredoc 单引号（`'EOF'`）说明，避免 `$` 与反引号被 shell 展开。

### 8.3 纠错的制度沉淀（不只修一次）

| 机制 | 落点 | 作用 |
|---|---|---|
| **真名复核 sub-agent（P0-5）** | 全书 | 独立于写作 sub-agent，专责 grep 全书伪命令 / 伪字段 |
| **零容忍红线** | 本 README §勘误 | `reserveTokensFloor` 与 `2026.3.2` 命中数必须为 0 |
| **反例行强制** | 每处易错点 | 写正确写法时**同时**写反例（`# ❌ 不存在：…`） |
| **回滚步骤强制** | sop-library 30 套 | 每套 SOP 必含回滚路径，避免「修错了退不回」 |
| **诚实边界段强制** | 全书每文件 | 标 ✅ 已实测 / ⏳ 待实测 / 🔵 差距，禁写「看起来对」 |
| **FAQ 问题上报流程** | [faq-troubleshooting/README.md](./faq-troubleshooting/README.md) ¶4 | 走修复工单闭环 → 固化为 FAQ → 高频晋升 Top 20 |

---

## 9. 业界对位总表

> **对位方法**：v5.0 对位基于对 7 个业界项目的**逐项内容维度**核对（quickstart / 概念讲解 / tutorial / cookbook / API 参考 / 部署 / FAQ / troubleshooting / 实战案例 / 案例库 / **练习题** / 模板与 SOP 库）。
> **诚实前提**：**规模差距显著且不可回避**（见下方「规模诚实标注」）；本表的价值不在「比谁大」，而在**「哪些能力业界没有、本书有」**。

### 9.1 七大业界项目对位

| 业界项目 | 本书对应 | 差异（诚实标注） |
|---|---|---|
| **LangChain**（230 万+ 词文档生态，mdx ≈ 2,384 页真实文档） | **全书 59 文件 · 53,258 行** | 🔵 **规模差距**：约 15–35 倍（中英词字不可严格对等）。**对位点**：LangChain 定义「文档与代码分离 + 概念页密度」；本书定义「中文 agent 训练学的完整闭环」。**本书独有**：漂移治理 / 主动性边界 / 三省评审 / 自主目标生成 / 8 段式案例库 / 30 套 SOP / 练习题级结构 |
| **LlamaIndex**（`md` = 1,756 + `ipynb` = 754；API 参考 762 页 + examples 734 页，**API 与示例近 1:1**） | **全书 + [api-reference](./00-新书主编报告.md)（🔶 在跑，7 文件）** | 🔵 **规模差距**：文档页数约 30 倍；**API 参考尚未交付**（本书最大缺口）。**对位点**：LlamaIndex 定义「API 参考与示例 1:1」；本书 **[cookbook 30 例](./cookbook/01-protocol-SOUL.md)** 承担示例侧，**api-reference 承担参考侧**——参考侧 🔶 在跑 |
| **OpenAI Cookbook**（`ipynb` = 275 + `md` = 150 + `py` = 468；examples/ 下 270 nb） | **[cookbook · 30 例 · 12,548 行](./cookbook/01-protocol-SOUL.md)** | 🟡 **数量差距**：275 nb → 30 例，约 **9 倍**。**对位点**：「每个配方解决一个具体问题、复制即用」。**本书差异**：OpenAI 是**可运行 notebook**（能跑代码），本书是**可复制配置 + 验证命令**（能配系统）；本书每例额外含「实测环境标注 + 排坑 + 进阶」，OpenAI 无回滚概念 |
| **Anthropic Skills**（`anthropics/skills` 内置 19 个 skill；`agentskills.io/specification` 6 字段规范） | **[第 10 章 · Skill 注册](./chapters/11-skill-registry/README.md)** + [SKILL.md-frontmatter-规范](./chapters/11-skill-registry/SKILL.md-frontmatter-规范.md) + [Registry 表](./chapters/11-skill-registry/Registry-表.md) | ✅ **对位**：本书直接对齐 Anthropic Skills 标准（YAML frontmatter 6 字段 / name ≤64 字符规范 / description 召回工程）。**本书差异**：Anthropic 给规范，本书给**实拉对位 + 本机 236 skills 的真实覆盖率**（有 frontmatter 216/238） |
| **MCP**（Model Context Protocol） | **[第 8 章 · MCP 绑定](./chapters/09-mcp-binding/09-MCP绑定.md)**（2,353 行） | ✅ **对位**：MCP 14 子命令（`add/configure/doctor/list/login/logout/probe/reload/serve/set/show/status/tools/unset`）实拉 + 8 卷 → 46 MCP 原语映射。**诚实边界**：本书基座本机 **0 个 OpenClaw-managed MCP server**（实测 `No OpenClaw-managed MCP servers configured`），本章为**接入方法论 + 映射设计**，非「已在跑」 |
| **A2A**（Agent2Agent，Linux Foundation） | **[第 9 章 · A2A 绑定](./chapters/10-a2a-binding/10-A2A绑定.md)**（2,797 行 · 全书最厚） | ✅ **对位**：Agent Card schema（`supported_interfaces: ["a2a/v1","slcp/v1"]`）+ 4 类原语映射（Task / Artifact / Message / Push Notification）。**本书差异 = 优势 1**：A2A v1.0 **不管** fallback 健康检查 / 通道守门员 / 协同事件日志——**SLCP 反脆弱三层是补丁** |
| **Claude Agent SDK**（`py` = 109 + `md` = 12；examples/ 20 个） | **[第 1 章 七大契约](./chapters/02-protocols/02-七大契约.md)** + **[第 2 章 系统骨架](./chapters/03-skeleton/03-系统骨架.md)** + **[第 3 章 训练流程](./chapters/04-training/04-训练流程.md)** | ✅ **对位**：`AGENTS.md` 子 agent 声明 ↔ SDK subagent task spec；`任务卡` ↔ task spec；`权限边界` ↔ Claude permission API。**本书差异**：SDK 是**库**（写代码调用），本书是**训练学**（怎么训一个 agent，含训练轮次 + 双三角 + Mentor Agent）——SDK 无「训练」概念 |

### 9.2 能力维度完整度矩阵

> ✅ 有 / ➖ 部分 / ❌ 无。本书列基于**实测结构复核**；业界列基于公开仓库结构。

| 内容项 | **本书 v5.0** | LangChain | LlamaIndex | OpenAI Cookbook | AutoGen | CrewAI | Claude SDK |
|---|---|---|---|---|---|---|---|
| quickstart（5 分钟上手） | ✅ [0.2](./00-getting-started/01-quickstart-5min.md) | ✅ | ✅ | ✅ | ✅（317 词，偏薄） | ✅ | ✅ |
| 概念讲解 | ✅ chapters 21,855 行 | ✅（2,384 页） | ✅ | ➖（以例代讲） | ✅ | ✅ | ✅ |
| tutorial 分步教程 | ✅ [00-getting-started](./00-getting-started/README.md) | ✅ | ✅（734 ex） | ✅（nb 即教程） | ✅（49 nb） | ✅ | ✅（20 例） |
| cookbook 可复制配方 | ✅ **30 例** | ✅ | ✅ | ✅（275 nb，本仓即 Cookbook） | ❌ | ➖ | ➖ |
| API 参考 | 🔶 **在跑（7 文件未交付）** | ✅ | ✅（762 页） | ➖ | ✅ | ✅ | ✅ |
| **SOP 库（含回滚）** | ✅ **30 套** | ➖ | ➖ | ❌ | ➖ | ➖ | ❌ |
| FAQ 独立节 | ✅ **102 问** | ✅（百级） | ✅ | ➖ | ❌ | ✅ | ➖ |
| troubleshooting 独立节 | ✅ [F1–F7](./faq-troubleshooting/README.md) | ✅ | ✅ | ➖ | ❌ | ✅ | ➖ |
| 实战案例 | ✅ **10 例 8 段式** | ✅ | ✅ | ✅（本仓即案例） | ❌（停滞） | ➖ | ➖ |
| 案例库（≥10 例成体系） | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **练习题结构** | ⬜ **待启动（P3）** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **每例自测题（8 题）** | ✅ **[case-library](./case-library/01-real-incidents.md)** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 漂移治理（业界空白赛道） | ✅ [第 4 章](./chapters/05-long-term/05-长期表现.md) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 主动性边界三档 | ✅ [C5-2](./cookbook/05-drift-governance.md) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 决策分权 + 结算 | ✅ [第 5/6 章](./chapters/06-governance/06-治理系统.md) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 自主目标生成（提案型） | ✅ [第 7 章](./chapters/08-evolution/08-超维演进.md) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### 9.3 规模诚实标注（🔵 不可回避的差距）

| 对比项 | 业界标杆 | 本书 v5.0 | 差距倍数 | 备注 |
|---|---|---|---|---|
| LangChain docs | mdx ≈ 2,384 页 × ~1,500 词 ≈ **230–350 万词** | 53,258 行 ≈ 8–10 万字（中文） | **约 15–35 倍** | 中英词字**不可严格对等**，此为量级对比 |
| OpenAI Cookbook | (275 nb + 150 md) × ~2,000 词 ≈ **80 万词** | cookbook 12,548 行 | **约 8–10 倍** | 数量差距在配方条数（275 → 30） |
| LlamaIndex | `md` = 1,756 + `ipynb` = 754 ≈ **260 万词** | 59 文件 · 53,258 行 | **约 26–30 倍** | API 参考侧**尚未交付**，差距最大处 |
| CrewAI | mdx = 28,643（**含 41 版本快照**，去重后约 768 页） | 59 文件 | **约 13 倍**（去重后约 13 倍） | CrewAI 的快照膨胀是**反模式**，不作为对标目标 |
| AutoGen | `md` = 162 + `ipynb` = 49（**165 天未推送**） | 59 文件 · 53,258 行 | **反超** ✅ | AutoGen 单页仅 317 词 + 停滞 → 本书在 FAQ/troubleshooting/案例库三项**形成代差** |

**结论**：本书在**规模上全面落后业界标杆**（15–35 倍），这是诚实事实；
但在**「案例库 + SOP 大全 + 每例自测题 + 漂移治理 + 主动性边界 + 决策分权 + 自主目标」**这 7 项上，**业界无人具备同构实现**——**本书的价值主张是「结构的稀缺」，不是「体量的领先」**。

---
## 10. 版本关系与依赖

### 10.1 三版血缘（v1.0 → v4.0 → v5.0）

```text
v1.0（原版 · 2026-05-07 · 一字未动）
  83 文件 · 38,518 行 · 8 卷（volume-01 … volume-08）+ INDEX.md
  角色：**参考依据**（丘总拍板「v1.0 74+ 篇作为参考依据」）
  状态：✅ 原版保留，不重写、不改名、不删
        │
        │  改造①：重构为 8 卷 + 4 接口层（09-a2a / 09-mcp / 09-plugin / 09-skill）
        ▼
v4.0（2026-09-27）
  111 文件 · 36,175 行 · 8 卷 + 4 接口层 + README.md + INDEX.md
  角色：**结构蓝本**（较 v1.0 增加接口层，但 SOP/FAQ/案例断崖式流失）
  状态：🟡 保留为对照版本（不删）
        │
        │  改造②：8 大模块重写 —— 回填薄章 + 补齐 5 大实战模块
        ▼
v5.0（本版 · 2026-09-27 · industry-standard）
  59 文件 · 53,258 行 · 8 卷 + 4 接口层 + 5 新卷（入门/Cookbook/FAQ/案例/SOP）
  角色：**当前交付版**
  状态：✅ P0 ✅ / P1 ✅ / P2 🟡（SOP 卷 ✅ · API 参考 🔶 在跑）/ P3 ⬜ 未启动
```

### 10.2 基线关系图（v5.0 依赖什么）

```text
┌───────────────────────────── 上层：v5.0 本书 ─────────────────────────────┐
│  00-getting-started │ chapters(23) │ cookbook(7) │ faq(9) │ case(2)      │
│  sop(7)             │ api-reference(🔶 在跑)                        │
│  依赖 ↓                                                        │
│  ① 术语红线：00-术语对照表·v3.0行业标准版.md（35 条改名，不得自造）        │
│  ② 架构红线：00-新书主编报告.md（12 章骨架 + 每章 6 项验收）              │
│  ③ 真名红线：OpenClaw 2026.9.4 (3a9d69d)（CLI/npm/json 三源一致）        │
│  ④ 零容忍：reserveTokensFloor = 0 命中 · 2026.3.2 = 0 命中              │
└──────────────────────────────────────────────────────────────────────┘
                                    ↑ 依赖
┌────────────────────── 基座：OpenClaw / 宿主 / 读者环境 ─────────────────────┐
│  OpenClaw **2026.9.4 (3a9d69d)** ← 本书统一书写口径（配置兼容 9.6）        │
│  本机 live：**2026.9.6 (eb377ac)** ← 2026-09-27 实测（补丁版差异）        │
│  Hermes Agent 0.20.1                                                      │
│  宿主：macOS 26.5.1 · Node 22 LTS（PATH 侧 Node 24 被 runtime admission）  │
│  本机基线：18 agent · 61 automations · 53/73 plugins · 236 skills · 0 MCP │
└───────────────────────────────────────────────────────────────────────┘
                                    ↑ 输入
┌───────────────────────── 输入源：四类原始材料 ─────────────────────────────┐
│  ① v1.0 八卷原稿（83 文件 · 38,518 行）—— 参考依据，不重写                 │
│  ② v4.0 改造版（111 文件 · 36,175 行）—— 结构蓝本，不沿用正文              │
│  ③ v3.0 改名表（35 条）+ v3.0 总纲（README-v3.0-archive.md）—— 术语与 banner │
│  ④ v5.0 改造方案（v5.0-framework-proposal.md）—— 优先级与工作量依据        │
└───────────────────────────────────────────────────────────────────────┘
```

### 10.3 依赖与兼容性

| 依赖项 | 版本 | 关系 | 说明 |
|---|---|---|---|
| **OpenClaw** | 2026.9.4（本书口径） / 2026.9.6（本机 live） | **强依赖** | 差两个补丁版；配置兼容（`openclaw.json` 结构不变） |
| **Hermes Agent** | 0.20.1 | 弱依赖 | 用于编写期编排（多 sub-agent 并行），非读者运行必需 |
| **Node** | 22 LTS | 强依赖 | `openclaw` 运行时；本机存在 Node 24 但**被 runtime admission 拒绝**，会打印 `Retrying with … node@24` 告警 |
| **macOS** | 26.5.1 | 验证宿主 | 所有「已实测」结论均在 macOS 上取得；Linux 路径差异见 [0.2 跨平台差异](./00-getting-started/01-quickstart-5min.md) |
| **skills 规模** | 236 个 | 数据依赖 | 第 10 章统计与 Registry 表的基线 |
| **MCP** | 0 个 OpenClaw-managed server | 无运行时依赖 | 第 8 章为接入方法论，非「已在跑」 |
| **Windows / Docker** | — | ⏳ 未验证 | 全书未在 Windows / 容器内跑过 |

### 10.4 版本升级规约（v6.0 怎么走）

| 触发条件 | 动作 | 落点 |
|---|---|---|
| OpenClaw 主版本变更（2027.x） | 全量真名复核 → 更新 §勘误 | 本 README + 各章真名验证文件 |
| API 参考交付 | §5-⑦ 由 🔶 改为 ✅ + 补齐文件清单 | 本 README §5 |
| 练习题库（P3）交付 | 新增「练习题卷」模块 + §4.1 表补行 | 本 README §4/§5 |
| 案例库达 20 例 | 更新 §5-⑤ 数量 + 案例总表 | 本 README §5 |
| 术语表新增条目 | **必须**同步更新 §11 + 全书首现双写 | 术语表 + 全书 |

---

## 11. 术语规范

### 11.1 三条铁律（违反即退稿）

1. **内部稿保留黑话**：v1.0 原稿、内部日报、军团内部指令**继续用黑话**（亲切、高效、丘总语境）。
2. **对外 + 工程接口一律改名**：RFC、plugin、对外文档、OpenClaw agent 训练底座**必须**用行业标准术语。
3. **过渡期双写**：首次出现时写「**行业标准名（原：黑话）**」，例：`Supervisor Layer（原：监军）`、`TEV（原：三证验真）`、`SLCP（原：ACP）`。

### 11.2 完整 35 条改名对照表

> 出处：[`00-术语对照表·v3.0行业标准版.md`](./00-术语对照表·v3.0行业标准版.md) · 全表 127 行 · 6 大类。
> **本表即为全书「首次出现双写」的权威来源**——本书任何文件首次使用下列术语，必须写成「标准名（原：黑话）」。

#### 第 1 类 · 必须改名（商标 / 语义冲突 · 无商量）

| # | 标准名（原：黑话） | English |
|---|---|---|
| 1 | **SLCP**（原：ACP） | Silicon-Life Coordination Protocol |
| 2 | **主动进化范式 / 被动响应范式**（原：训虾派 / 养虾派） | Proactive Evolution Paradigm / Reactive Paradigm |

#### 第 2 类 · 必须改名（语义澄清 · 内部保留注解）

| # | 标准名（原：黑话） | English |
|---|---|---|
| 3 | **硅基智能体 / Agent**（原：龙虾 / 虾） | Silicon-based Agent |
| 4 | **导师智能体 / 训练协调器**（原：教练虾） | Mentor Agent / Training Coordinator |
| 5 | **初级智能体 / 专家智能体**（原：新人虾 / 专家虾） | Novice Agent / Expert Agent |
| 6 | **多智能体编排 / 智能体集群**（原：军团编制 / 军团） | Multi-Agent Orchestration / Agent Fleet |
| 7 | **监督层**（原：监军） | Supervisor Layer |
| 8 | **蓝血智能体生态**（原：蓝血军团） | Blue-Blood Agent Ecosystem |
| 9 | **角色中文名 + 英文职能后缀**（原：昆仑 / 轩辕 / 天工 等 18 角色名） | `Kunlun (Chief-of-Staff)` / `Xuanyuan (Engineering)` / `Tiangong (Product)` |

#### 第 3 类 · 必须改名（工程接口 · 对齐业界标准）

| # | 标准名（原：黑话） | English |
|---|---|---|
| 10 | **三证据验证**（原：三证验真） | Three-Evidence Verification (TEV) |
| 11 | **修复工单**（原：整改单） | Remediation Ticket |
| 12 | **信任评分 / 功绩账本**（原：信誉分 / 军功簿） | Trust Score / Merit Ledger |
| 13 | **三省评审制**（原：三省制） | Three-Stage Review: Proposal / Review / Final-Decision |
| 14 | **响应让渡协议**（原：让位协议） | Response Yield Protocol |
| 15 | **任务交接协议**（原：交接棒协议 / Handoff） | Task Handoff Protocol (THP) |
| 16 | **治理审计账本**（原：治理账本） | Governance Audit Ledger |
| 17 | **技能基因 / 可复用能力单元**（保留 + 加英文） | Skill Gene / Reusable Capability Unit |
| 18 | **心跳**（保留） | Heartbeat |
| 19 | **会话压缩 / 上下文压缩**（原：会话卫生 / Compaction） | Session Compaction / Context Compaction |
| 20 | **工具与技能双模块 + 共享网关 RPC**（原：Tools+Skills 双协议） | Tools / Skills Dual Modules + Shared Gateway RPC |

#### 第 4 类 · 可保留（业界通用或品牌资产）

| # | 术语（处理） | English |
|---|---|---|
| 21 | **硅基生命**（✅ 保留） | Silicon-based Life / Silicon Life |
| 22 | **生命协议**（✅ 保留） | Life Protocols |
| 23 | **SOUL / USER / AGENTS / TOOLS / IDENTITY / HEARTBEAT / MEMORY**（✅ 保留） | 同名 |
| 24 | **任务卡**（✅ 保留 + 英文） | Task Card |
| 25 | **验收口径**（✅ 保留 + 英文） | Acceptance Criteria |
| 26 | **双三角模型**（✅ 保留 + 英文） | Dual-Triangle Model: Expectation-Actuality-Feedback Loop |
| 27 | **OODA 循环**（✅ 保留） | OODA Loop (Observe-Orient-Decide-Act) |
| 28 | **文档漂移 / 人格漂移**（✅ 保留 + 英文） | Document Drift / Personality Drift |
| 29 | **每周体检清单**（✅ 保留 + 英文） | Weekly Health Checklist |
| 30 | **自主目标生成**（✅ 保留 + 英文） | Autonomous Goal Generation (Response → Proposal) |

#### 第 5 类 · OpenClaw 真名对照（训练底座必用）

| # | 标准名（原：误植表述） | OpenClaw 真名 |
|---|---|---|
| 31 | **压缩预算预留**（原：`reserveTokensFloor`） | ❌ 不存在；真名 `CompactionRequestBudget.reserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25` |
| 32 | **工具与技能双模块**（原：Tools+Skills 双协议） | ❌ 无此术语；真结构 `tools.catalog` + `skills.status` / `skills.skillCard` |
| 33 | **OpenClaw 主仓** | `https://github.com/openclaw/openclaw`（**非** `AaronWong1999/hermesclaw`，后者仅为桥接器） |
| 34 | **OpenClaw 本机版本** | **2026.9.4 (3a9d69d)**（本书口径）· 本机 live **2026.9.6 (eb377ac)**（**非**调研员误报的 `2026.3.2`） |
| 35 | **OpenClaw License** | **MIT**（文件法律文本确凿；GitHub `NOASSERTION` 仅为 badge 显示问题） |

### 11.3 三层术语架构

```text
┌─────────────────────────────────────────────┐
│ Layer 1：对外 RFC / 行业标准版               │  ← 第 1–3 类改名全部生效
│  术语：SLCP / TEV / Trust Score / …          │
│  语言：中英双语                              │
│  License：MIT（跟随 OpenClaw）               │
├─────────────────────────────────────────────┤
│ Layer 2：OpenClaw agent 训练底座（本书）      │  ← 本 README + 术语表
│  术语：行业标准名 + 原黑话括号注解（首现双写） │
│  语言：中文为主，英文接口名                   │
│  路径：~/.openclaw/workspace/…               │
├─────────────────────────────────────────────┤
│ Layer 3：内部稿 / 军团指令（v1.0）            │  ← 黑话保留
│  术语：训虾派 / 蓝血军团 / 三证验真 …          │
│  语言：中文                                  │
│  路径：v1.0 原版不动                          │
└─────────────────────────────────────────────┘
```

### 11.4 引用规范

| 场景 | 写法 |
|---|---|
| 训练底座引用本表 | `[术语对照表 v3.0 §X]` |
| 对外 RFC 引用本表 | `[Silicon Life Training v3.0 Terminology]` |
| 内部稿引用本表 | **无需引用**（黑话直接用） |

### 11.5 术语自查命令（复制即跑）

```bash
cd ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard

# ① 零容忍红线：误植字段必须 0 命中（除反向引用外）
grep -rn "reserveTokensFloor" --include="*.md" . | wc -l

# ② 零容忍红线：作废版本号必须 0 命中（除反例外）
grep -rn "2026\.3\.2" --include="*.md" . | wc -l

# ③ 伪命令清扫
grep -rn "openclaw chat --\|openclaw init\|agents create\|agents health-check" --include="*.md" . | wc -l

# ④ 错误配置路径清扫
grep -rn "workspace/openclaw.json" --include="*.md" . | wc -l

# ⑤ 改名一致性：ACP 只应出现在「原：ACP」括号内
grep -rn "ACP" --include="*.md" . | grep -v "原：ACP\|SLCP\|ACP bridge\|Zed ACP"
```

---
## 12. 诚实边界声明

> **本手册遵循「未实测，不宣称」原则。** 以下三档分列，请按状态使用。
> **分档定义**：✅ **已实测**（本机可复现）· ⏳ **待实测**（骨架正确，落点/行为待验）· 🔵 **与业界标杆差距**（规模与完整度诚实标注）。

---

### ✅ 已实测（本机 OpenClaw 2026.9.6 (eb377ac) · macOS 26.5.1 · 2026-09-27 可复现）

| # | 范围 | 实测内容 | 实测命令 |
|---|---|---|---|
| 1 | **版本** | `OpenClaw 2026.9.6 (eb377ac)`（**本书统一书写口径为 2026.9.4 (3a9d69d)**，两补丁版配置兼容） | `openclaw --version` |
| 2 | **Agent 编制** | **18 个 agent**：`kunlun (default)` · `mingjing` · `tianshu` · `tiangong` · `xuanyuan` · `fenghuang` · `kunpeng` · `jixia` · `zhulong` · `siku` · `qilin` · `hetu` · `peter` · `fengniao` · `mobai` · `zhuque` · `baxia` · `tiance` | `openclaw agents list \| grep -cE '^- [a-z]'` → `18` |
| 3 | **自动化任务** | **61 条 automation**（心跳 + cron 合计；含 `heartbeat:tiance` / `heartbeat:kunlun` / `heartbeat:peter` · `军功爵周结算` 等） | `openclaw cron list \| grep -cE '^[0-9a-f]{8}-'` → `61` |
| 4 | **Plugins** | **53 / 73 enabled**（头行逐字：`Plugins (53/73 enabled)`；v4.0/v5.0 早期文档写 51/69，为更早时点口径） | `openclaw plugins list \| head -1` |
| 5 | **skills 规模** | **236 个 skill 目录**（`ls skills/` **238** 个目录项 − **2** 个非目录文件）；其中 **216 个含 `SKILL.md`** | `ls -d ~/.openclaw/workspace/skills/*/ \| wc -l` → `236` |
| 6 | **MCP 配置** | **0 个 OpenClaw-managed MCP server**（逐字：`No OpenClaw-managed MCP servers configured in ~/.openclaw/openclaw.json.`；且不含 mcporter servers） | `openclaw mcp list` |
| 7 | **配置真身** | `~/.openclaw/openclaw.json` · **45,662 字节** · 1,871 行 · **20 顶层 key** | `wc -c ~/.openclaw/openclaw.json` |
| 8 | **License** | OpenClaw 主仓 LICENSE 法律文本 = **MIT**（GitHub badge `NOASSERTION` 不影响法律效力；plugin 分发可行） | 尽调报告 `license-due-diligence-report.md` |
| 9 | **目录结构** | 应用根 `~/.openclaw/` 与工作区 `~/.openclaw/workspace/` **两级结构** | `ls ~/.openclaw/ ~/.openclaw/workspace/` |
| 10 | **本书规模** | **59 文件 · 53,258 行**（逐文件 `wc -l` 求和核验：3,077 + 21,855 + 12,548 + 4,280 + 4,562 + 6,286 + 410 + 240(旧 README)） | `find . -name '*.md' \| wc -l` / `cat` 求和 |
| 11 | **存量基线** | v1.0 = **83 文件 · 38,518 行**；v4.0 = **111 文件 · 36,175 行** | `find … \| wc -l` + `cat \| wc -l` |
| 12 | **内容计数** | cookbook **30 例**（`^# C\d-\d` 计数）· FAQ **102 问**（`^## F\d-\d · 问：` 计数）· SOP **30 套** · CASE **10 例** | `grep -rhoE '^# C[0-9]+-[0-9]+ · ' cookbook/ \| wc -l` 等 |
| 13 | **skill 缺陷** | afrexai 系列 13 个中 **11 个完全无 YAML frontmatter**（CASE-3 真实案例） | `grep -L "^---" skills/afrexai-*/SKILL.md` |
| 14 | **飞书参数** | `openclaw.json` 中 `requireMention` 41 次 / `groupAllowFrom` 10 次 / `groupPolicy` 40 次（CASE-2 实测） | `grep -o "requireMention" ~/.openclaw/openclaw.json \| wc -l` |
| 15 | **漂移面** | 18 agent 全量扫描：`red=0 / yellow=17 / green=1` · `L3_emergency=32` · `anchor_missing_agents=17` · `retired_residue_agents=16`（C5-1） | `python3 drift_scan.py --dry-run` |
| 16 | **心跳异常** | heartbeat error 计数：`peter 70x` / `kunlun 99+x`（CASE-9 实测） | `grep -c error …/heartbeat.log` |
| 17 | **plugin 子命令** | `openclaw plugins` **15 子命令**（plural）：`build/disable/doctor/enable/init/inspect/install/list/marketplace/pack/registry/search/uninstall/update/validate` | `openclaw plugins --help` |
| 18 | **plugin 目录** | 安装目录 = `~/.openclaw/extensions/`（**不是** `~/.openclaw/workspace/plugins/`） | `ls ~/.openclaw/extensions/` |
| 19 | **命令可跑性** | 全书验证类命令均为标准工具（`find` / `grep` / `sha256sum` / `file` / `curl` / `jq`），逻辑确定 | 抽样执行 |
| 20 | **链接完整性** | 本 README 全部相对链接 **0 broken**（`-f` 逐个验证） | 见 §附-验收 第 3 条 |

---

### ⏳ 待实测（骨架正确，落点 / 子命令 / 行为以本机为准 —— 书中已逐处标 ⏳）

| # | 范围 | 待实测项 | 相关落点 |
|---|---|---|---|
| 1 | **端到端联跑** | 全书 cookbook 30 例**未逐例在本机端到端联跑**（配置片段已核真名，但「复制→粘贴→能跑」的**全链路**未逐例验证） | `cookbook/` 全卷 |
| 2 | **plugins install 全生命周期** | `openclaw plugins install` 从**本地 tarball / ClawHub 远端**的完整安装 → 启用 → 卸载链路未跑通 | `chapters/12-plugin-entrypoint/install-指南.md` |
| 3 | **ClawHub publish** | `ClawHub` 独立 CLI（走 GitHub OAuth）的 publish 全流程未实测 | `chapters/12-plugin-entrypoint/真名验证与勘误.md` §6 |
| 4 | **A2A TCK** | A2A v1.0 **TCK（Technology Compatibility Kit）**未跑；SLCP bridge 仅原型 | `chapters/10-a2a-binding/10-A2A绑定.md` |
| 5 | **MCP 实连** | 第 8 章为**接入方法论**；本机 **0 个** MCP server，**未实连任何 server** | `chapters/09-mcp-binding/09-MCP绑定.md` |
| 6 | **OpenClaw 官方 RFC** | RFC SLT-001 **未提交**主仓；`github.com/openclaw/openclaw/rfcs` 实测 **404**（不存在） | `chapters/12-plugin-entrypoint/OpenClaw-官方RFC-草案.md` |
| 7 | **plugin manifest 校验** | `openclaw plugins validate` 对本书 `openclaw.plugin.json` 的**实际校验结果**未记录 | `chapters/12-plugin-entrypoint/openclaw.plugin.json` |
| 8 | **日志路径** | `~/.openclaw/workspace/logs/heartbeat.log` 等精确路径随版本变化 | F3-1 / F3-9 |
| 9 | **cron 字段名** | `openclaw cron list --json` 的 `last_run` / `next_run` 字段名随版本变化 | F3-2 |
| 10 | **调度器时区** | 时区是否可显式配置 | F3-3 |
| 11 | **launchd** | `launchctl bootstrap` 被拒行为随 macOS 版本变化 | F3-15 / `SOP-12` |
| 12 | **memory CLI** | `openclaw memory reindex` 子命令是否存在、索引格式与重建方式 | F4-7 / F4-10 |
| 13 | **通道 CLI** | `openclaw channels status --probe` 是否可用 | F6-6 / F6-12 |
| 14 | **事故取证数据** | `channel_ingress_events.attempts=2471` 等 9/21 数据来自事故报告，**非本书新增实测** | CASE-2 |
| 15 | **工单落点** | `memory/decisions/整改单/` 以昆仑 workspace 实际结构为准 | F7-7 / `SOP-25` |
| 16 | **Windows / Docker** | 全书**未在** Windows / 容器 / Linux 上验证（除标注的 Linux 安装路径） | `00-getting-started/01-quickstart-5min.md` |
| 17 | **阅读耗时** | §6 三条路径的耗时均为**编者估算**（按阅读速度约 500 行/小时推算），**非实测** | 本 README §6 |
| 18 | **第 1 章预留目录** | 主编报告预留 `chapters/01-philosophy/`，本机**实测不存在该目录**（总论落在 `00-front/`） | `chapters/` |

---

### 🔵 与业界标杆的差距（诚实标注 · 不美化）

| # | 差距项 | 差距内容 | 量化 |
|---|---|---|---|
| 1 | **总规模** | 全书 53,258 行（约 8–10 万字中文） vs 业界 80–350 万词 | **约 15–35 倍**（中英词字**不可严格对等**，此为量级对比） |
| 2 | **API 参考** | **🔶 未交付**（目录已建，0 文件）；LlamaIndex 有 762 页 API 参考 | 本书**最大结构性缺口** |
| 3 | **可运行示例** | cookbook 为「可复制配置 + 验证命令」，**不是**可运行 notebook；OpenAI Cookbook 275 nb / LlamaIndex 754 nb | 约 9 倍（配方条数 30 vs 275） |
| 4 | **版本快照** | 无多版本快照机制；CrewAI 有 41 个版本快照 | 单版本交付 |
| 5 | **中英双语** | 正文为**中文为主 + 英文 alias**；非全双语 | 对外 RFC 需另行双语化 |
| 6 | **社区验证** | **0 星 / 0 fork / 无外部贡献者**；LangChain 147k stars、OpenAI Cookbook 76k stars | 生态规模不可比 |
| 7 | **练习题** | ⬜ **未启动**（P3，按丘总指令放最后） | 全行业空白 = 机会，也是**当前未兑现的承诺** |
| 8 | **自动化测试** | 全书**无 CI / 无链接检查机器人**；链接完整性靠人工 `-f` 逐条验证 | 维护成本高 |
| 9 | **覆盖场景** | 全部案例来自**单一本机军团**（18 agent）；无跨组织 / 跨云 / 大规模验证 | 样本量 n=1 |
| 10 | **时效性** | 结论基于 2026-09-27 的 OpenClaw 补丁版；主版本变更后真名可能失效 | 需按 §10.4 规约重验 |

---

### 诚实边界的三条自我约束

1. **凡标 ⏳ 者，不得在任何摘要中被表述为「已完成」**——包括本 README 的总览表（总览表用 🔶 / ⬜ 显式标注）。
2. **凡涉及规模的对比，必须同时给出「中英词字不可严格对等」的前提**，禁止把量级对比写成精确换算。
3. **凡「业界空白」的论断，必须能指向对位矩阵中该行为 ❌ 的**具体列**（见 §9.2），不得凭印象宣布差异化。

---

## 附录 A · v5.0 验收清单（自检）

### A.1 结构与规模

- [x] **总行数 ≥ 600 行** → 实测 **1,123 行**（见 附录 D）
- [x] **8 大模块全部导航**（每模块含：行数 / 文件清单 / 一句话说明 / 链接 / 适合谁读）
- [x] **所有行数 / 文件数实跑 `wc -l` / `find`**（非承袭旧版、非估算）
- [x] **api-reference 🔶 在跑状态诚实标注**（未交付即为未交付，不虚构 7 文件行数）

### A.2 内容完整性（12 节齐备）

| # | 必含节 | 状态 |
|---|---|---|
| 1 | 顶部 banner（版本 / 基线 / 维护者 / License / 基座 / 环境） | ✅ |
| 2 | 全卷勘误（v3.0 三条 + 新增两条 = 5 条） | ✅ |
| 3 | 一句话定位（v5.0 版 + 三条硬指标） | ✅ |
| 4 | 为什么是 v5.0（v1.0 → v4.0 → v5.0 演进表） | ✅ |
| 5 | v5.0 八大模块导航（核心章节） | ✅ |
| 6 | 三条阅读路径（零基础 / 工程师 / 运维治理） | ✅ |
| 7 | 6 个差异化优势（5 保留 + 1 新增） | ✅ |
| 8 | 实测纠错清单（v5.0 独有） | ✅ |
| 9 | 业界对位总表（7 项目 + 16 维度矩阵 + 规模诚实标注） | ✅ |
| 10 | 版本关系与依赖（血缘 + 基线关系图 + 升级规约） | ✅ |
| 11 | 术语规范（35 条双写 + 三层架构 + 自查命令） | ✅ |
| 12 | 诚实边界声明（✅ / ⏳ / 🔵 三档分列） | ✅ |

### A.3 硬约束达成

- [x] **保留现有 README 的 banner + 3 条勘误 + 术语对照精华**（banner 六件套保留并升级版本号；3 条勘误保留并扩为 5 条；术语对照扩为 35 条完整表）
- [x] **原 README 存档**：`README-v3.0-archive.md`（240 行 · 14,865 字节 · **未删**）
- [x] **术语规范**：35 条改名表首次出现**双写**（「标准名（原：黑话）」）
- [x] **诚实边界**：✅ / ⏳ / 🔵 三档分列（20 / 18 / 10 项）
- [x] **所有模块链接实测 0 broken** → **60 条相对链接 / 0 broken**（见 附录 D 链接验证记录）

### A.4 链接完整性实测（`-f` 逐个验证）

```bash
# 验证方法：从本 README 抽取全部相对链接，逐个 test -f
cd ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard
grep -oE '\]\(\./[^)]+\)' README.md | sed 's/](//;s/)$//' | sed 's/#.*$//' | sort -u | \
  while read -r p; do [ -f "$p" ] && echo "OK   $p" || echo "BROKEN $p"; done
# 期望：全部 OK，0 BROKEN（实测结果见文末「链接验证」段）
```

---

## 附录 B · 本 README 的定位与维护

### B.1 本文件是什么

| 项 | 说明 |
|---|---|
| **角色** | 全书**总索引**（不是目录的目录，而是**导航中枢 + 版本档案 + 诚实声明**） |
| **对标** | LangChain docs 的「侧边栏导航」+ OpenAI Cookbook 的「按场景索引」+ LlamaIndex 的「版本化交付说明」 |
| **不做什么** | ❌ 不复制任何章节正文（导航不搬内容）· ❌ 不虚构未交付模块 · ❌ 不美化规模差距 |

### B.2 维护规约

| 变更类型 | 必须同步 |
|---|---|
| 新增 / 删除文件 | §5 对应模块的文件清单 + 行数 + 总览表合计 |
| OpenClaw 版本变更 | §勘误 + §10.3 + §12 ✅ 档「版本」行 |
| 术语表新增条目 | §11.2 表 + 全书首现双写 + §11.5 自查命令 |
| 交付 🔶 / ⬜ 模块 | §4.3 优先级表 + §5 总览表 + §12 🔵 差距档 |
| 发现新的实测纠错 | §8 总表 + 逐条展开 + §8.3 制度沉淀 |

### B.3 引用规范

| 场景 | 写法 |
|---|---|
| 引用本书总纲 | `《硅基生命训练学》v5.0 行业标准版 · README.md` |
| 引用特定模块 | `《硅基生命训练学》v5.0 §5-③ cookbook（30 例）` |
| 引用术语 | `[术语对照表 v3.0 §X]` |
| 引用真名 | `OpenClaw 2026.9.4 (3a9d69d)`（本书口径） |

---

## 附录 C · 结语

> **v5.0 行业标准版的核心承诺**：
>
> 把《硅基生命训练学》从「有人写哲学、无人写手册」的论述型文稿，改造为一本**既能读、又能跑、还能查、更能查完照做**的行业标准底座——
> **新人 5 分钟跑起来**（[00-getting-started](./00-getting-started/README.md)）→
> **工程师 30 例照着配**（[cookbook](./cookbook/01-protocol-SOUL.md)）→
> **运维 30 套 SOP 照着做**（[sop-library](./sop-library/README.md)）→
> **出事 102 问 30 秒定位**（[F-Top20](./faq-troubleshooting/F-Top20-高频速查.md)）→
> **复盘 10 例 8 段式拆到底**（[case-library](./case-library/01-real-incidents.md)）。
>
> v5.0 不是 v4.0 的补丁，**是 v4.0 的「手册化重写」**——
> 保留 8 卷训练学的灵魂与 5 个差异化优势，补齐 5 大实战模块，把每一条结论钉在**可执行的验证命令**上。
>
> **但我们诚实说明**：本书规模仍落后业界标杆 15–35 倍；API 参考尚未交付；练习题尚未启动；
> 案例样本 n=1；无 CI；无社区验证。**这些不是修辞，是待办清单。**

---

## 附录 D · 链接验证记录（本机实测）

> **验证方式**：从本 README 正则抽取**全部以 `./` 开头的相对链接**，逐个 `os.path.isfile()`（等价 `test -f`）验证。

```text
total unique relative links: 60
BROKEN: 0
```

| 项 | 结果 |
|---|---|
| 相对链接总数（去重后） | **60** |
| Broken | **0** ✅ |
| 覆盖模块 | 00-getting-started(8) · chapters(17) · cookbook(7) · faq(9) · case(2) · sop(7) · 术语表 · 主编报告 · v3.0 存档 |
| **未链接项（刻意）** | `api-reference/` —— 🔶 在跑，**不提供文件链接以免制造 broken link**（见 §5-⑦） |
| 存档验证 | `README-v3.0-archive.md` **存在**（240 行 · 14,865 字节，未删） |
| 本 README 行数 | **1,123 行**（≥ 600 行硬约束 ✅） |

### 复现命令

```bash
cd ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard

grep -oE '\]\(\./[^)]+\)' README.md | sed 's/](//;s/)$//' | sed 's/#.*$//' | sort -u | \
  while read -r p; do [ -f "$p" ] && echo "OK   $p" || echo "BROKEN $p"; done
```

---

> **— 丘国力（Peter Qiu）+ 天策 · 2026-09-27**
> 基于 OpenClaw **2026.9.4 (3a9d69d)**（本机 live **2026.9.6 (eb377ac)**）
> + Hermes Agent **0.20.1** + v1.0（83 文件 · 38,518 行）+ v4.0（111 文件 · 36,175 行）
> + v3.0 改名表（35 条）+ v5.0 改造方案
>
> **本 README 是 v5.0 的「全书总索引」——任何模块的增删、术语的变更、真名的更正，必须先改本文件，再改章节。**

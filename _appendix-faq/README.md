# 📕 FAQ + Troubleshooting（故障速查卷）· 卷首

> **v4.0/v5.0 行业标准版 banner**：本目录是《硅基生命训练学》v2026.9 行业标准版的**独立 FAQ 卷**；总纲见 [../README.md](../README.md)，术语基线见 [../00-术语对照表·v3.0行业标准版.md](../00-术语对照表·v3.0行业标准版.md)。
> **License banner**：**MIT** —— 基于 OpenClaw 主仓 LICENSE 法律文本（P0 核实结论：法律文本为 MIT；GitHub badge 因 `THIRD_PARTY_NOTICES` 尾行显示为 NOASSERTION，**不影响法律效力**）。可商用、可分发 plugin。
> **OpenClaw 真名**：本机 `openclaw --version` → **`OpenClaw 2026.9.4 (3a9d69d)`**。本卷涉及版本号一律以本机实测为准，**勿引用调研员早期误报的 `2026.3.2`**（该值已作废，见 [F1-1](./F1-环境与安装.md)）。
> **环境标注**：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27 · 宿主 macOS 26.5.1
> **规模**：7 分类 · **102 问** · 3654 行 + 本速查卷（Top20 + README）
> **配套**：[cookbook/](../_appendix-cookbook/)（可直接复制的协议/配置模板）· [chapters/](../chapters/)（8 卷正文）

---

## 一句话定位

> **本卷是「硅基生命训练学」的急救手册**——把 18 个智能体（Agent）在 OpenClaw 2026.9.4 上跑起来、跑得稳、跑得不漂移的**全部已知坑**，按「现象 → 原因 → 解法 → 验证命令」四段式固化下来。
>
> 区别于业界通用框架的 getting-started 文档：本卷的每个问题都带**本机可执行命令**，每条结论都标**已实测 / ⏳ 待实测**，**不允许「看起来对」的答案**。

---

## 30 秒选路

| 你的处境 | 该去哪 |
|---|---|
| 「装了但报错，先救火」 | 直接跳 [**F-Top20 高频速查**](./F-Top20-高频速查.md) ⚡ |
| 「知道是哪个域的问题」 | 下表找对应 F 分类 |
| 「不知道归哪类」 | 全卷搜索（见 ¶4 第 3 步） |
| 「想建一个自己的排障流程」 | [cookbook/03-skills-tools-mcp.md](../_appendix-cookbook/03-skills-tools-mcp.md) |

---

## 1. 七分类速查表

| 分类 | 主题 | 问题数 | 典型症状 | 相对路径 |
|---|---|---|---|---|
| **F1** | 环境与安装（Environment & Install） | **12** | 命令找不到 / 版本对不上 / 模型报错 / 权限没开 | [F1-环境与安装.md](./F1-环境与安装.md) |
| **F2** | SOUL / AGENTS / USER 协议（Protocols） | **15** | 人格串味 / 声明了不认账 / 协议不生效 | [F2-协议-SOUL-AGENTS-USER.md](./F2-协议-SOUL-AGENTS-USER.md) |
| **F3** | 心跳与定时（HEARTBEAT / Cron） | **15** | 该醒没醒 / 到点没跑 / 守护起不来 / 重复执行 | [F3-心跳与定时.md](./F3-心跳与定时.md) |
| **F4** | 记忆与会话（MEMORY / Session） | **15** | 忘了前面的话 / 记忆串味 / 搜不到 / 越聊越贵 | [F4-记忆与会话.md](./F4-记忆与会话.md) |
| **F5** | Skills / Tools / MCP | **15** | skill 不加载 / MCP 连不上 / tools 空 / 分发合规 | [F5-Skills-Tools-MCP.md](./F5-Skills-Tools-MCP.md) |
| **F6** | 多 Agent 协同（Multi-Agent Coordination） | **15** | 抢答刷屏 / 让位失效 / 死锁 / 通道断线 / 路由错人 | [F6-多Agent协同.md](./F6-多Agent协同.md) |
| **F7** | 治理 / 漂移 / 体检（Governance / Drift / Health Check） | **15** | 文档漂移 / 人格漂移 / 体检不通过 / 工单没人跟 | [F7-治理漂移体检.md](./F7-治理漂移体检.md) |
| **Σ** | **合计** | **102** | — | — |

### 各分类覆盖范围（一句话）

- **F1 环境与安装**：从「一个新人拿到一台新 Mac」到「OpenClaw 跑起来、接上模型、加载 skills」的全段。特点是**错误现象指向错误的地方**——版本对不上会报模型不存在，权限没开会被当成 gateway 崩溃，路径搞错会显示「0 个 skill」。
- **F2 协议**：SOUL（人格）/ AGENTS（调度）/ USER（权限）三份核心协议的**职责边界、改写回滚、编码合规、命名对齐**。
- **F3 心跳与定时**：HEARTBEAT（心跳）与 cron（定时）的**触发、时区、重入、自愈、与 launchd 混用**。
- **F4 记忆与会话**：MEMORY.md 的体积与分层、会话压缩预算真名、记忆域隔离、检索命中率、memory 与 skill 的分工。
- **F5 Skills / Tools / MCP**：Anthropic Skills 规范（`SKILL.md` + YAML frontmatter）的入编体检、MCP（Model Context Protocol）接入、plugin manifest、分发合规。
- **F6 多 Agent 协同**：路由 → 让位 → 兜底三道闸门、死锁、单点/全军哑火、通道守门员（Channel Sentinel）、handoff（任务交接）与 SLCP 反脆弱三层。
- **F7 治理 / 漂移 / 体检**：文档漂移（Document Drift）与人格漂移（Personality Drift）检测、每周体检、修复工单（Remediation Ticket）、TEV、信任评分、主动性边界。

---

## 2. Top 20 高频问题入口

> **80% 的现场故障，Top 20 里 30 秒能解。**

👉 **[F-Top20-高频速查.md](./F-Top20-高频速查.md)** —— 20 问表格化速查 + 每问一句话解法（≤40 字）+ 「详见」跳分类正文 + 底部**可打印速查卡**（纯文本 20 行，可贴墙）。

**Top 20 配额**（覆盖 7 分类均衡）：

| 分类 | 入选数 | 代表问题 |
|---|---|---|
| F1 环境 | 3 | `openclaw: command not found` / workspace 找不到 / `model not found` |
| F2 协议 | 4 | 18 角色共用同一 SOUL / 子 Agent 声明调度不到 / 协议不生效 / ACP 改名遗留 |
| F3 心跳 | 3 | heartbeat 不触发 / cron 静默错过 / `launchctl bootstrap` 被拒 |
| F4 记忆 | 3 | `reserveTokensFloor` 误植 / 多 Agent 共用 memory / 记忆搜不到 |
| F5 skill/tool | 2 | `SKILL.md` 缺 frontmatter / MCP server 连不上 |
| F6 协同 | 3 | 群聊抢答刷屏 / 飞书 @ 无响应 / 路由错人 |
| F7 治理 | 2 | 文档漂移告警 / 修复工单怎么建 |

---

## 3. 怎么用这本 FAQ（3 步）

### 第 1 步 · 先查 Top 20

打开 [F-Top20-高频速查.md](./F-Top20-高频速查.md)，用 `Cmd+F` 搜你的**报错原文**或**症状关键词**（如「not found」「串味」「不触发」）。

- **命中了** → 表格第二列拿一句话解法，读「详见」列点进分类正文，照「验证命令」逐条跑。
- **没命中** → 进第 2 步。

### 第 2 步 · 找分类

回到本文档 [¶1 七分类速查表](#1-七分类速查表)，按**「典型症状」列**定位到对应 F 文件；打开后先看该文件顶部的「问题清单」表（每问一行「一句话现象」），再 `Cmd+F` 定位到具体条目。

**分类速判口诀**：

```
报错 / 装不上 / 连不上      → F1 环境
人格 / 身份 / 权限不对       → F2 协议
该动的时候不动              → F3 心跳
记不住 / 记错 / 变慢了      → F4 记忆
说找不到某能力              → F5 skill/tool
多个 Agent 打起来           → F6 协同
慢慢变得不像自己            → F7 治理
```

### 第 3 步 · 全卷搜索

仍无答案，用命令行做**全卷 grep**（跨 7 个文件 + 速查卷）：

```bash
cd ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/faq-troubleshooting

# 搜报错原文 / 症状关键词（中文 + 英文 alias 双写更易命中）
grep -rn "command not found\|model not found\|串味\|让位\|漂移" --include="*.md" . | head -30

# 只搜「解法」段，跳过现象描述
grep -rn -A3 "^\*\*解法\*\*" --include="*.md" . | grep -i "<关键词>" | head
```

**搜索技巧**：本卷所有术语按 v3.0 规范「中文 + 英文 alias」双写，因此搜 `SLCP` 和搜 `协同协议` 都能命中；搜 `reserveTokensFloor` 会命中「误植勘误」条目（提示你**这是不存在的字段**）。

---

## 4. 问题上报流程（怎么把新问题补进 FAQ）

> **原则**：FAQ 不是「事后回忆录」，而是**整改闭环的产物**——每个新问题都要走**修复工单（Remediation Ticket，原：整改单）**流程，先解决、再固化、最后入卷。

### 4.1 触发条件（满足任一即建单）

| 触发源 | 阈值 | 依据 |
|---|---|---|
| 现场故障 | 任意 P0/P1 事故（服务中断 / 通道失效 / 全军哑火） | [F6-5](./F6-多Agent协同.md)、[F6-6](./F6-多Agent协同.md) |
| 体检红项 | 每周体检任一项不通过 | [F7-3](./F7-治理漂移体检.md) |
| cron 连续失败 | `consecutiveErrors ≥ 3` | [F7-8](./F7-治理漂移体检.md)、[F7-15](./F7-治理漂移体检.md) |
| 同一现象 | 30 天内重复出现 ≥ 2 次（即「高频」候选） | 本流程 ¶4.4 |
| 文档漂移 | `grep` 误植字段 / 作废版本号命中 > 0 | [F7-1](./F7-治理漂移体检.md) |

### 4.2 建单（四步）

```bash
# 步骤 1：建单落点（按 F7-7 标准）
mkdir -p ~/.openclaw/workspace/agents/workspace-kunlun/memory/decisions/整改单
# 命名规则：YYYY-MM-DD-NNN-<简称>.md
# 例：2026-08-19-001-军团断线.md / 2026-09-21-001-飞书断线.md

# 步骤 2：填模板字段（10 项，缺一不可）
cat <<'TPL'
触发：<什么被触发了：事故 / 体检红项 / cron 连续失败>
根因：<根因，不是现象>
影响范围：<哪些 agent / 通道 / 数据受影响>
优先级：<P0 | P1 | P2 | P3>
整改方案：<具体动作，可执行>
责任Agent：<谁负责>
截止时间：<YYYY-MM-DD>
回滚方案：<改坏了怎么退>
验收标准：<怎么算修好（须可测）>
复盘：<事后填：为什么会发生 / 怎么防止复发>
TPL

# 步骤 3：验收用 TEV（Three-Evidence Verification，原：三证验真）
#   证据 1：新产物（文件 / 日志 / 报告）
#   证据 2：前后 Diff
#   证据 3：测试日志（真的跑过的输出）
#   三证据齐 ≠ 单行「已完成」三字

# 步骤 4：验收通过后，把「可复现的现象 + 收敛的解法」固化为 FAQ 条目
```

### 4.3 固化为 FAQ 条目

新增条目**必须**满足本卷四段式标准，写进对应分类文件（不新建分类，除非确实无归属）：

| 段 | 要求 | 反例（不合格） |
|---|---|---|
| **现象** | 用**用户会看到的那句话**描述，含报错原文 | 「有时候会失败」（太模糊） |
| **原因** | 讲**根因**，可指到字段/进程/协议层 | 「配置问题」（等于没说） |
| **解法** | 给**可复制命令**，非「检查一下」 | 「建议检查配置」（不可执行） |
| **验证命令** | 一条命令 + 期望输出 | 「应该就好了」（不可验证） |

**附加要求**：

1. 首行加环境标注：`> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27`
2. 首次出现的术语加括号注 + 英文 alias，例：`响应让渡协议（Response Yield Protocol，原：让位协议）`
3. 未在本机复现的步骤标 **⏳ 待实测**
4. 同步更新该分类文件的「问题清单」表 + 本 README ¶1 的问题数

### 4.4 晋升 / 毕业

- 某问题在 30 天内被 ≥2 人次上报 → **晋升进 Top 20**（更新 [F-Top20](./F-Top20-高频速查.md) 并重排速查卡）
- 某分类问题数超过 **20** → 评估是否拆分新分类（需报 [../README.md](../README.md) 总纲更新）
- 某问题因版本升级已不复现 → 标 `已归档（<版本> 起不复现）`，**不删除**（保留决策痕迹）

---

## 5. 全卷结构一览

```
faq-troubleshooting/
├── README.md                        ← 本文件（卷首 · 入口 · 上报流程）
├── F-Top20-高频速查.md              ← 20 问速查 + 可打印速查卡  ⚡ 先看这个
├── F1-环境与安装.md                 ← 429 行 · 12 问
├── F2-协议-SOUL-AGENTS-USER.md      ← 534 行 · 15 问
├── F3-心跳与定时.md                 ← 546 行 · 15 问
├── F4-记忆与会话.md                 ← 550 行 · 15 问
├── F5-Skills-Tools-MCP.md           ← 564 行 · 15 问
├── F6-多Agent协同.md                ← 516 行 · 15 问
└── F7-治理漂移体检.md               ← 515 行 · 15 问
```

**每个 F 文件内部结构**（统一）：

```
# FAQ + Troubleshooting · F<n> · <主题>
> banner（v4.0 / License / 真名 / 术语基线 / 业界对位）
## 分类简介
## 问题清单              ← 一行一问的「问题 | 一句话现象」表
## F<n>-1 · 问：...
   > 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27
   **现象** … **原因** … **解法** … **验证命令** … **预防**
## F<n>-2 · 问：...（同上四段式）
...
## 验收清单
## 诚实边界声明
```

---

## 6. 本卷的术语与合规底线

### 6.1 术语（v3.0 改名表 · 本卷高频）

| 本卷用词 | 英文 alias | 原黑话 |
|---|---|---|
| 智能体 / 智能体集群 | Agent / Agent Fleet | 虾 / 军团 |
| 监督层 | Supervisor Layer | 监军 |
| 响应让渡协议 | Response Yield Protocol | 让位协议 |
| 修复工单 | Remediation Ticket | 整改单 |
| 信任评分 / 功绩账本 | Trust Score / Merit Ledger | 信誉分 / 军功簿 |
| 三省评审制 | Three-Stage Review | 三省制 |
| 三证据验证 | Three-Evidence Verification (TEV) | 三证验真 |
| SLCP | Silicon-Life Coordination Protocol | ACP |
| 工具与技能双模块 | Tools + Skills Modules | Tools+Skills 双协议 |
| 压缩预算预留 | `reserveTokens`（+ `MAX_COMPACTION_RESERVE_RATIO`） | ~~reserveTokensFloor~~（**不存在**） |

> 完整 35 条见 [../00-术语对照表·v3.0行业标准版.md](../00-术语对照表·v3.0行业标准版.md)。**内部稿保留黑话，对外 + 工程接口一律用标准名**；过渡期首次出现双写「标准名（原：黑话）」。

### 6.2 合规底线（三条硬约束）

1. **版本真名不可手写** —— 一律 `openclaw --version` 实测，文档模板占位符统一写 `OpenClaw 2026.9.4 (3a9d69d)`。
2. **误植字段零容忍** —— `reserveTokensFloor`、`2026.3.2` 在任何文档中命中数必须为 **0**。
3. **ACP 已废弃** —— 对外文档/plugin/RFC 一律 `SLCP`；对外文档首次出现写 `SLCP（原：ACP）`。

---

## 7. 诚实边界声明

> 本卷遵循「**未实测，不宣称**」原则。以下分列「已实测」与「⏳ 待实测」，请按状态使用。

### ✅ 已实测（本机 OpenClaw 2026.9.4 (3a9d69d) · macOS 26.5.1 可复现）

| 范围 | 实测内容 |
|---|---|
| 版本真名 | `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`（三源交叉：CLI + npm registry + 本机 json） |
| License | 主仓 LICENSE 法律文本 = **MIT**（badge NOASSERTION 不影响法律效力） |
| 目录结构 | 应用根 `~/.openclaw` 与工作区 `~/.openclaw/workspace` **两级结构** |
| skills 规模 | 本机 skills 目录已到 **238 个**（含 F1-4 / F4-13 的「合规计数」问题） |
| skill 缺陷 | **afrexai 系列 13 个中 11 个完全无 YAML frontmatter**（F5-2 真实案例） |
| 飞书通道 | `openclaw.json` 中 `requireMention` 出现 **41 次** / `groupAllowFrom` **10 次** / `groupPolicy` **40 次**（F6-6 实测） |
| 误植字段 | `reserveTokensFloor` 为 v1.0 误植，真名 `reserveTokens`（术语表第 31 条背书，F4-2 / F7-1） |
| 命令可跑 | 各 F 文件中的 `find` / `grep` / `sha256sum` / `file` / `curl` 类验证命令均为标准工具，逻辑确定 |

### ⏳ 待实测（骨架正确，落点 / 子命令 / 行为以本机为准）

| 范围 | 待实测项 | 相关条目 |
|---|---|---|
| 日志路径 | `~/.openclaw/workspace/logs/heartbeat.log` 精确路径 | F3-1 / F3-9 |
| cron 字段 | `openclaw cron list --json` 的 `last_run` / `next_run` 字段名随版本变化 | F3-2 |
| 时区配置 | 调度器时区是否可以显式配置 | F3-3 |
| launchd | `launchctl bootstrap` 被拒行为随 macOS 版本变化 | F3-15 |
| memory CLI | `openclaw memory reindex` 子命令是否存在 | F4-7 |
| 记忆索引 | 索引格式 / 重建方式 | F4-7 / F4-10 |
| plugin CLI | `openclaw plugins list` 输出格式 | F1-12 / F5-13 |
| 通道 CLI | `openclaw channels status --probe` 是否可用 | F6-6 / F6-12 |
| 事故取证 | `channel_ingress_events.attempts=2471` 等 9/21 数据来自事故报告，非本卷新增实测 | F6-6 |
| 工单落点 | `memory/decisions/整改单/` 以本机昆仑 workspace 实际结构为准 | F7-7 |

### 待推（本卷不覆盖，需人工判定）

- **架构决策类问题**：plugin 路线 vs 官方 RFC 路线、8 卷重写优先级、License 分发策略 —— 见 [../README.md](../README.md) 与 [../00-新书主编报告.md](../00-新书主编报告.md)。
- **尚不存在的功能**：本卷只写「OpenClaw 2026.9.4 已具备」的能力；对未来版本的预测一律标 ⏳，不写成事实。
- **非本机验证的行为**：任何未在本机 macOS 26.5.1 复现的输出，一律视为 ⏳。

---

## 8. 卷末自查清单

- [x] v4.0 banner + License banner（MIT）+ OpenClaw 真名（2026.9.4 (3a9d69d)）齐备
- [x] 7 分类速查表：问题数（12/15/15/15/15/15/15 = 102）+ 主题 + 相对路径链接
- [x] Top 20 高频问题入口（链接 [F-Top20](./F-Top20-高频速查.md)）含配额表
- [x] 「怎么用」3 步：查 Top20 → 找分类 → 全卷搜索（含 grep 命令与口诀）
- [x] 问题上报流程：触发条件 → 建单 → 四段式固化 → 晋升/毕业
- [x] 诚实边界声明：已实测 / ⏳ 待实测 / 待推 三档分列
- [x] 术语按 v3.0 改名表（首次出现加括号注 + 英文 alias）
- [x] 相对路径链接 0 broken（`-f` 实测）

---

*本卷是《硅基生命训练学》行业标准版 v2026.9 的 FAQ 分册 —— 所有条目以 OpenClaw 2026.9.4 (3a9d69d) 本机实测为准，未实测者标 ⏳，绝不虚构。*
*维护者：天策（Supervisor Layer，原：监军）· 2026-09-27*

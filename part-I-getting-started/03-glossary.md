# 0.4 · 术语表 · 训虾派黑话 → 行业标准英文双语

> **v5.0 行业标准版 banner**：本文件是第零章「零基础入门」第 0.4 节；章目录见 [./README.md](./README.md)。
> **License banner**：MIT（跟随 OpenClaw 主仓 LICENSE；GitHub NOASSERTION 不影响法律效力）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`（2026-09-27 实测）。
> **依据**：`../00-术语对照表·v3.0行业标准版.md`（35 条）+ 行业标准调研报告（6 份）。

> **⚠ 勘误（2026-09-27 · 实测）**：本表第 31 条的 `effectiveReserveTokens` / `MAX_COMPACTION_RESERVE_RATIO` 是**本书接口层口径**——
> 本机实测 `~/.openclaw/openclaw.json`（45,662 字节）对该字段及 `reserveTokens` / `reserveTokensFloor` / `contextTokenBudget` **全部 0 命中**
> （顶层 key `session` 仅含 `dmScope`）。"别用 `reserveTokensFloor`"是对的，但它也**不是**可写入 `openclaw.json` 的字段。

---

## 0. 背景 · 为什么一本中文手册要先给你一张术语表

《硅基生命训练学》脱胎于一套内部中文黑话体系（原「训虾派 / 养虾派 / 军团编制 / 监军」）。这套黑话在**内部语境**里亲切高效，但一旦要**对外输出**（RFC、plugin、开源文档、英文接口），就会撞上三个问题：

1. **商标冲突**：自造的「ACP」与 IBM/BeeAI 已合并入 A2A 的 ACP 撞名；
2. **语义不清**：「军团编制」对外国开发者毫无信息量；
3. **工程不齐**：黑话没有对应的**英文接口名**，写不出 plugin。

所以本节给你一张「**双语地图**」：左边是黑话（你会在内部日报里见到），右边是行业标准名 + 英文 alias（你在 RFC/代码里必须用）。

> **改名原则（v3.0 宪法级）**：
> 1. 内部稿保留黑话；对外 + 工程接口一律改名；
> 2. 过渡期双写：首次出现写「行业标准名（原：黑话）」；
> 3. 所有标准术语**必须有英文名**。

本节结构：**背景 → 配置（三层术语架构）→ 验证（怎么用）→ 实测环境 → 排坑（常见误用）→ 进阶**。

---

## 1. 配置 · 三层术语架构

```text
┌─────────────────────────────────────────┐
│ Layer 1：对外 RFC / 行业标准版           │ ← 改名全部生效（SLCP/TEV/Trust Score…）
│  语言：中英双语 · License：MIT           │
├─────────────────────────────────────────┤
│ Layer 2：OpenClaw agent 训练底座         │ ← 标准名 + 原黑话括号注解
│  语言：中文为主，英文接口名               │
├─────────────────────────────────────────┤
│ Layer 3：内部稿 / 军团指令               │ ← 黑话保留
│  语言：中文                              │
└─────────────────────────────────────────┘
```

> 本手册（v5.0 行业标准版）位于 **Layer 1/2 之间**：正文用标准名，首次出现附黑话注解。

---

## 2. 术语对照表 · 必须改名（商标/语义冲突，无商量）

| # | 黑话（原） | 行业标准名（v5.0 用） | 英文 alias | 改名原因 |
|---|---|---|---|---|
| 1 | ACP（自造） | **SLCP** | **SLCP** (Silicon-Life Coordination Protocol) | IBM/BeeAI 的 ACP 已占用并 2025-08 并入 A2A |
| 2 | 养虾派 / 训虾派 | **被动响应范式 / 主动进化范式** | **Reactive Paradigm / Proactive Evolution Paradigm** | 仅内部语境；对外必删或加注 |

---

## 3. 术语对照表 · 必须改名（语义澄清，内部保留注解）

| # | 黑话（原） | 行业标准名（v5.0 用） | 英文 alias |
|---|---|---|---|
| 3 | 龙虾 / 虾 | **硅基智能体 / Agent** | **Silicon-based Agent** |
| 4 | 教练虾 | **导师智能体 / 训练协调器** | **Mentor Agent / Training Coordinator** |
| 5 | 新人虾 / 专家虾 | **初级智能体 / 专家智能体** | **Novice Agent / Expert Agent** |
| 6 | 军团编制 / 军团 | **多智能体编排 / 智能体集群** | **Multi-Agent Orchestration / Agent Fleet** |
| 7 | 监军 | **监督层** | **Supervisor Layer** |
| 8 | 蓝血军团 | **蓝血智能体生态** | **Blue-Blood Agent Ecosystem** |
| 9 | 昆仑 / 轩辕 / 天工 … | **中文名 + 英文职能后缀** | 如 `Kunlun (Chief-of-Staff)`、`Xuanyuan (Engineering)`、`Tiangong (Product)` |

---

## 4. 术语对照表 · 必须改名（工程接口，对齐业界标准）

| # | 黑话（原） | 行业标准名（v5.0 用） | 英文 alias |
|---|---|---|---|
| 10 | 三证验真 | **三证据验证** | **TEV** (Three-Evidence Verification) |
| 11 | 整改单 | **修复工单** | **Remediation Ticket** |
| 12 | 信誉分 / 军功簿 | **信任评分 / 功绩账本** | **Trust Score / Merit Ledger** |
| 13 | 三省制 | **三省评审制** | **Three-Stage Review** (Proposal / Review / Final-Decision) |
| 14 | 让位协议 | **响应让渡协议** | **Response Yield Protocol** |
| 15 | 交接棒协议 / Handoff | **任务交接协议** | **Task Handoff Protocol (THP)** |
| 16 | 治理账本 | **治理审计账本** | **Governance Audit Ledger** |
| 17 | 技能基因 | **技能基因 / 可复用能力单元** | **Skill Gene / Reusable Capability Unit** |
| 18 | 心跳 | **心跳（保留）** | **Heartbeat** |
| 19 | 会话卫生 / Compaction | **会话压缩 / 上下文压缩** | **Session Compaction / Context Compaction** |
| 20 | Tools+Skills 双协议 | **工具与技能双模块 + 共享网关 RPC** | **Tools / Skills Dual Modules + Shared Gateway RPC** |

---

## 5. 术语对照表 · 可保留（业界通用或品牌资产）

| # | 黑话（原） | v5.0 处理 | 英文 alias |
|---|---|---|---|
| 21 | 硅基生命 | ✅ 保留 | **Silicon-based Life / Silicon Life** |
| 22 | 生命协议 | ✅ 保留 | **Life Protocols** |
| 23 | SOUL / USER / AGENTS / TOOLS / IDENTITY / HEARTBEAT / MEMORY | ✅ 保留 | 同名（与 OpenClaw 文件模板对齐） |
| 24 | 任务卡 | ✅ 保留 | **Task Card** |
| 25 | 验收口径 | ✅ 保留 | **Acceptance Criteria** |
| 26 | 双三角模型 | ✅ 保留 | **Dual-Triangle Model** (Expectation-Actuality-Feedback) |
| 27 | OODA 循环 | ✅ 保留 | **OODA Loop** (Observe-Orient-Decide-Act) |
| 28 | 文档漂移 / 人格漂移 | ✅ 保留 | **Document Drift / Personality Drift** |
| 29 | 每周体检清单 | ✅ 保留 | **Weekly Health Checklist** |
| 30 | 自主目标生成 | ✅ 保留 | **Autonomous Goal Generation** (Response → Proposal) |

---

## 6. 术语对照表 · OpenClaw 真名（训练底座必用）

> ⚠ 实测注：第 31 条的"真名"是**本书约定**（区别于 v1.0 误植），非 `openclaw.json` 字段名。

| # | 常见误写 | OpenClaw 真名（2026.9.4 核实） | 说明 |
|---|---|---|---|
| 31 | `reserveTokensFloor` | ❌ 不存在；真名 `effectiveReserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25` | 训练底座一律用真名 |
| 32 | Tools+Skills 双协议 | ❌ 无此术语；真结构 `tools.catalog` + `skills.status` / `skills.skillCard` | P0 核实 |
| 33 | OpenClaw 主仓 = `AaronWong1999/hermesclaw` | ❌；真主仓 `https://github.com/openclaw/openclaw` | 后者仅为桥接器 |
| 34 | OpenClaw 版本 3.2 | ❌；真版本 **2026.9.4 (3a9d69d)** | CLI + npm + json 三源一致 |
| 35 | OpenClaw License 不明 | ✅ 真为 **MIT** | GitHub `NOASSERTION` 仅 badge 问题 |

---

## 7. 新增高频术语（本节补充，训练底座常用）

| 术语 | 英文 alias | 一句话 |
|---|---|---|
| 零基础入门 | **Getting Started** | 本章主题 |
| 快速上手 | **Quickstart** | 0.2 节 |
| 环境准备 | **Environment Checklist** | 0.1 节 |
| 全流程走查 | **Walkthrough** | 0.3 节 |
| 主动性边界三档制 | **Proactivity Boundary Triptych** | allowed / needs-confirm / forbidden（优势 3） |
| 反脆弱三层 | **Anti-Fragile Triptych** | fallback 健康检查 + 通道守门员 + 结构化事件日志（优势 1） |
| 漂移治理三件套 | **Drift Governance Trio** | 文档漂移 + 人格漂移 + 每周体检（优势 2） |
| 响应型 → 提案型 | **Response → Proposal** | 全书主线（优势 5） |
| 状态目录 | **State Dir** | `~/.openclaw` |
| 工作区 | **Workspace** | agent 的文件系统底座 |
| 运行时 | **Runtime** | agent 的生命容器 |
| 网关 | **Gateway** | `openclaw gateway` |
| 技能 | **Skill** | `openclaw skills` |
| 插件 | **Plugin** | `openclaw plugins`（复数！） |

---

## 8. 验证 · 怎么正确使用本表

**规则**：
- 在**内部稿**：黑话直接用，无需引用本表。
- 在**训练底座 / 对外文档**：首次出现写「标准名（原：黑话，English alias）」，如「监督层（原：监军，Supervisor Layer）」。
- 在**代码 / plugin**：只用英文 alias 或真名，禁止中文黑话进标识符。

**自查命令**（找出手册里漏改的黑话）：

```bash
# 在章节文件里找未加注的黑话
grep -rn "训虾派\|养虾派\|军团编制\|监军\|三证验真\|整改单\|军功簿\|三层协议" \
  ../chapters/ 2>/dev/null | head -20
```

期望：命中的行都应带「（原：…）」或英文 alias；裸黑话 = 待修。

---

## 9. 实测环境

| 项 | 值 |
|---|---|
| OpenClaw | 2026.9.4 (3a9d69d) |
| 术语依据 | `../00-术语对照表·v3.0行业标准版.md`（35 条） |
| 实测日期 | 2026-09-27 |
| 本表条数 | 35（原表）+ 14（新增高频） = 49 |

---

## 10. 排坑 · 术语 6 坑

### 10.1 坑：把「训虾派」写进对外文档
**解法**：一律改「主动进化范式（Proactive Evolution Paradigm）」。

### 10.2 坑：写 `openclaw plugin install`（单数）
**解法**：真名 `openclaw plugins install`（复数）。

### 10.3 坑：用 `reserveTokensFloor`
**解法**：真名 `effectiveReserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25`。

### 10.4 坑：把「军团」直接译成 `army`
**解法**：行业标准名 `Multi-Agent Orchestration / Agent Fleet`。

### 10.5 坑：角色名后不加职能后缀
**解法**：对外必须写 `Kunlun (Chief-of-Staff)` 等。

### 10.6 坑：自造新术语
**解法**：v3.0 是「宪法附录」，**不得自造**；需要新词先入表。

---

## 11. 进阶

1. 把本表作为 CI 检查项：提交前 grep 裸黑话。
2. 维护「术语 → 章节锚点」映射，便于交叉引用。
3. 英文版手册落地时，以英文 alias 列为**唯一真名**。

---

## 12. 英文速查表（alias-only，供对外文档/代码使用）

写 RFC、plugin、open-source 文档时，**只允许**使用下表右列：

| 中文 | English（唯一对外真名） |
|---|---|
| 硅基生命 | Silicon Life |
| 硅基智能体 | Silicon-based Agent |
| 主动进化范式 | Proactive Evolution Paradigm |
| 被动响应范式 | Reactive Paradigm |
| 监督层 | Supervisor Layer |
| 多智能体编排 / 集群 | Multi-Agent Orchestration / Agent Fleet |
| 导师智能体 | Mentor Agent / Training Coordinator |
| 初级/专家智能体 | Novice / Expert Agent |
| 三证据验证 | TEV (Three-Evidence Verification) |
| 修复工单 | Remediation Ticket |
| 信任评分 | Trust Score |
| 功绩账本 | Merit Ledger |
| 三省评审制 | Three-Stage Review |
| 响应让渡协议 | Response Yield Protocol |
| 任务交接协议 | Task Handoff Protocol (THP) |
| 治理审计账本 | Governance Audit Ledger |
| 技能基因 | Skill Gene / Reusable Capability Unit |
| 心跳 | Heartbeat |
| 会话压缩 | Session Compaction |
| 反脆弱三层 | Anti-Fragile Triptych |
| 主动性边界三档制 | Proactivity Boundary Triptych |
| 漂移治理三件套 | Drift Governance Trio |
| 响应型→提案型 | Response → Proposal |
| 文档漂移 / 人格漂移 | Document Drift / Personality Drift |
| 每周体检清单 | Weekly Health Checklist |
| 自主目标生成 | Autonomous Goal Generation |

---

## 13. 反向索引（英文 → 中文，便于读英文源码/文档）

| 你在英文文档里看到 | 对应本手册术语 |
|---|---|
| Consistency / Continuity / Scaling / Assetization | 一致性 / 持续性 / 规模化 / 资产化（Q1-Q4） |
| Response Yield Protocol | 响应让渡协议 |
| Task Handoff | 任务交接 |
| Trust Score / Merit Ledger | 信任评分 / 功绩账本 |
| Anti-Fragile | 反脆弱 |
| Compaction / effectiveReserveTokens | 会话压缩 / 会话压缩预算真名 |
| Subagents / Handoff | 子智能体 / 交接 |
| Guardrails / Permission | 边界 / 权限 |
| Heartbeat / Cron | 心跳 / 定时 |

---

## 14. 使用示例（三段对照写法）

**❌ 错（裸黑话 + 无英文）**
> 「监军签发了整改单，要求军团按三证验真复检。」

**✅ 对（首次双写 + 英文 alias）**
> 「监督层（原：监军，Supervisor Layer）签发了修复工单（Remediation Ticket），要求智能体集群（Agent Fleet）按三证据验证（TEV）复检。」

**✅ 对（后续出现，直接用标准名）**
> 「监督层要求在下一轮 TEV 中补齐测试日志。」

> 规则：**第一次双写，之后用标准名。**

---

## 15. 进阶 · 术语治理

1. **术语即代码**：把英文 alias 做成 `glossary.json`，供 plugin 校验引用。
2. **CI 拦截**：提交前 grep 裸黑话（见 §8 命令）。
3. **版本化**：术语表变更走 PR + review（术语是宪法，不能随手改）。
4. **跨语言一致**：中文版与英文版共用同一份 alias 真名，避免翻译漂移。

---

## 16. 术语表的版本与维护

| 项 | 值 |
|---|---|
| 基底版本 | v3.0 行业标准版（35 条） |
| 本节扩展 | +14 条高频 + 英文速查 26 条 + 反向索引 9 条 |
| 维护者 | 训练学主编线 |
| 变更规则 | 术语 = 宪法；变更走 PR + review |

**新增术语申请模板**：

```text
术语名（中文）：
英文 alias：
定义一句话：
首次出现章节：
与既有术语的关系（同名/改名/新增）：
```

---

## 17. 一页速记（贴墙上）

```text
黑话 → 标准名（记住这 7 个就够开场）
训虾派  → 主动进化范式 (Proactive Evolution Paradigm)
监军    → 监督层 (Supervisor Layer)
军团    → 多智能体编排 (Multi-Agent Orchestration)
三证验真 → 三证据验证 (TEV)
信誉分  → 信任评分 (Trust Score)
让位    → 响应让渡协议 (Response Yield Protocol)
双协议  → 工具与技能双模块 + 共享 Gateway RPC

真名铁律：effectiveReserveTokens · MAX_COMPACTION_RESERVE_RATIO=0.25 · openclaw plugins（复数）
```

---

## 诚实边界声明

- ✅ **已用**：v3.0 术语对照表 35 条（本机实读源文件）；OpenClaw 真名 `2026.9.4 (3a9d69d)`、`effectiveReserveTokens`、`MAX_COMPACTION_RESERVE_RATIO`、`openclaw plugins`（复数）。
- ⏳ **待推**：SLCP / A2A / MCP Registry 的**最新版本号**（本手册未实拉，仅引用 v3.0 结论）。
- ⚠️ **未实测**：本表「新增高频术语」14 条为编者归纳，非官方术语表收录项——若与 OpenClaw 官方文档冲突，以官方为准。

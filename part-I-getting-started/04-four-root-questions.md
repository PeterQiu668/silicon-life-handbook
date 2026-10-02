# 0.5 · 训练学四根问题 · 一致性 / 持续性 / 规模化 / 资产化

> **v5.0 行业标准版 banner**：本文件是第零章「零基础入门」第 0.5 节；章目录见 [./README.md](./README.md)。
> **License banner**：MIT（跟随 OpenClaw 主仓 LICENSE；GitHub NOASSERTION 不影响法律效力）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`（2026-09-27 实测）。
> **业界对位**：本节把「四根问题」对位 OpenAI Agents SDK（Identity / Memory / Scaling / Assetization）· Anthropic Building Effective Agents（Define → Observe → Iterate → Scale）· Andrew Ng Agentic AI（Reflection → Tool Use → Planning → Multi-Agent）。
> **来源信号**：v1.0 卷一「训练学四个根问题」仅作**背景依据**，本节用新语言、新结构、新案例**从零重写**。

---

## 0. 背景 · 为什么训练学配得上叫「一门学科」

一门学科要有三个条件：**有核心问题、有方法体系、有边界检验**。

- 物理学的核心问题：「万物如何运动」；
- 经济学的核心方法：「边际分析」；
- 医学的边界：「治不了就承认治不了」。

硅基生命训练学（Silicon Life Training）满足这三个条件：

| 条件 | 训练学对应 |
|---|---|
| 核心问题 | **四根问题**（本节主题） |
| 方法体系 | 七份生命协议 + 双三角模型 + 三证据验证（TEV） |
| 边界检验 | 如果 agent 不需要跨会话稳定——**不适用**训练学 |

**本节的核心论断**：训练学不是「一堆调 prompt 的技巧」，而是一门**因为四根问题而得以成立**的学科。拆掉任何一根，学科就不完整。

本节把四根问题从「概念」讲到「你今天就能在自己的 agent 上验证」。

结构：**背景 → 配置 → 验证 → 实测环境 → 排坑 → 进阶**。

---

## 1. 配置 · 四根问题逐一拆解

### 1.0 总览

| 编号 | 问题 | 本质 | 不解决的后果 | 对应章 |
|---|---|---|---|---|
| **Q1** | 如何保证人格稳定？ | **一致性**（Consistency） | 换会话就变个人，风格漂移，用户无法建立信任 | 第 1 章 生命协议 |
| **Q2** | 如何保证记忆连续？ | **持续性**（Continuity） | 每次从零开始，学到的随会话过期流失 | 第 1 + 4 章 |
| **Q3** | 如何从单体到集群？ | **规模化**（Scaling） | 单体做不了的事，多体又角色混乱、消息冲突 | 第 6 章 协同军团 |
| **Q4** | 如何沉淀为可复用资产？ | **资产化**（Assetization） | 经验随人走，人来灰聚、人走清零 | 第 7 章 超维演进 |

**递进关系（这是全书八卷/十二章顺序的根本逻辑）**：

```text
Q1（一致性）← 所有训练动作的前提
    ↓
Q2（持续性）← 在一致的基础上，能不能积累
    ↓
Q3（规模化）← 在积累的基础上，能不能复制
    ↓
Q4（资产化）← 在复制的基础上，能不能传承
```

> **关键洞察**：四根问题**不是并列，是递进**。Q1 没解决，Q2 无从谈起；Q2 没解决，Q3 没有意义；Q3 没解决，Q4 没有载体。

---

### 1.1 Q1 · 一致性（Consistency）——人格稳定

**为什么它是独立问题？** 不是「人格稳定很重要」这种废话，而是：**没有稳定人格的 agent，所有后续训练动作都无法评估**。你没法判断一个每天性格都变的对象「进步了没有」。

**不解决的后果**：
- 同一问题，周一答案 A、周三答案 B；
- 语气忽冷忽热，用户建立不起信任；
- 团队无法给这个 agent 定义职责。

**解决工具**：
- SOUL.md（人格锚点，见 0.3 节）；
- 版本锚（`SOUL-VERSION` + 日期）；
- 人格漂移（Personality Drift）检测 —— **训练学差异化优势 2**。

**你今天就能验证的 Q1 小实验**：

```bash
# 连续问三次同一个开放问题，看回答风格是否收敛
for i in 1 2 3; do
  openclaw agent --agent my-first-agent --message "用一句话说你对'确定性'的看法"
done
```

期望：三次**风格一致**（同语气、同长度区间）。若三次人格割裂，说明 SOUL 没起到锚点作用。

**业界对位**：Anthropic「Define」阶段（先定义你想要的 agent 行为）→ 对应 Q1。

---

### 1.2 Q2 · 持续性（Continuity）——记忆连续

**为什么它是独立问题？** 因为 agent 天然是**有状态**的，但状态会过期。会话压缩（Session Compaction）一触发，早期上下文就被压缩掉了。**若不主动设计记忆体系，agent 每次都在「失忆」。**

**不解决的后果**：
- agent 不体现成长，永远像第一天；
- 你上次教它的规则，这次又违反；
- 花时间解释的背景，下次还得重讲。

**解决工具**：
- MEMORY.md 分层（长期 / 增量 / 归档）；
- OpenClaw 原生会话压缩，**真名** `effectiveReserveTokens` = 上下文预算 × `MAX_COMPACTION_RESERVE_RATIO`（= 0.25，**不可配置**）。

**你今天就能验证的 Q2 小实验**：

```bash
# 第一轮：教它一条规则
openclaw agent --agent my-first-agent --message "记住：我公司的简称是 NBX。请写入 MEMORY.md"

# 第二轮（新会话）：考它
openclaw agent --agent my-first-agent --message "我公司的简称是什么？"
```

期望：第二轮能答出 `NBX`。若答不出，说明记忆没落盘（0.3 节的 MEMORY 模板 + 落盘习惯是关键）。

**业界对位**：OpenAI Agents SDK 的「Memory」→ Q2；MemGPT/Letta/Mem0/Zep 全聚焦此问题。

---

### 1.3 Q3 · 规模化（Scaling）——从单体到集群

**为什么它是独立问题？** 单 agent 有天花板：上下文有限、技能有限、任务并行受限。但多 agent 不是「多开几个」——它会引入**角色混乱、消息风暴、级联失败**这三类新病。

**不解决的后果**：
- 派了子 agent，返回值没法归并；
- 一个 agent 挂了，拖垮整条链；
- 消息互通变成「谁都在说、没人负责」。

**解决工具**：
- 多智能体编排（Multi-Agent Orchestration，原：军团编制）；
- 任务交接协议（Task Handoff Protocol, THP）；
- 响应让渡协议（Response Yield Protocol）；
- **反脆弱三层**（Anti-Fragile Triptych，优势 1）：fallback 健康检查 + 通道守门员 + 结构化协同事件日志。

**你今天就能验证的 Q3 小实验**（需 2 个 agent）：

```bash
# 建第二个 agent
openclaw agents add helper-agent --workspace ~/first-agent/helper-agent --model <id>

# 让主线 agent 说明它如何路由
openclaw agent --agent my-first-agent --message "如果你要派 helper-agent 干活，说明你的路由规则"
```

期望：能说出**明确的路由规则**（什么任务派、什么任务不派）。答不出 = Q3 未开始。

**业界对位**：Anthropic「Scale」阶段 → Q3；OpenAI Agents SDK「Scaling」→ Q3。

---

### 1.4 Q4 · 资产化（Assetization）——可复用知识

**为什么它是独立问题？** 因为**最贵的不是能力，是不可丢失的积累**。一个团队里每个人都在自己 agent 里攒经验，但人一走，经验就清零。

**不解决的后果**：
- 每来一个新人，重走一遍所有坑；
- 最好的做法散落在各人的会话记录里，没人能复用；
- 组织的能力不随时间增长。

**解决工具**：
- 技能基因（Skill Gene / Reusable Capability Unit）；
- 案例沉淀（第 7 章案例工坊）；
- 治理审计账本（Governance Audit Ledger）。

**你今天就能验证的 Q4 小实验**：

```bash
# 看看你机器上可复用的 skill 有多少
ls ~/.openclaw/workspace/skills/ | wc -l       # 本机实测 = 238
openclaw skills list | head                    # 需要 Gateway 在跑
```

期望：返回一个 > 0 的数。238 个 skill 就是「资产化」的**存量**——问题是其中多少是你**主动沉淀**的？

**业界对位**：OpenAI Agents SDK「Assetization」→ Q4；Andrew Ng「Multi-Agent」→ Q4 的组织形态。

---

## 2. 验证 · 四根问题自评表

给你自己的 agent 打分（1 = 完全没做，5 = 做得很好）：

| 根问题 | 自评问题 | 分（1-5） |
|---|---|---|
| Q1 一致性 | 同一个问题问三次，风格是否收敛？SOUL 有版本锚吗？ | ___ |
| Q2 持续性 | 上次教它的规则，新会话还记得吗？MEMORY 有分层吗？ | ___ |
| Q3 规模化 | 有明确的子 agent 路由规则吗？失败会级联吗？ | ___ |
| Q4 资产化 | 你攒下的经验，别人能一键复用吗？ | ___ |

**判读**：
- 任何一项 ≤ 2 → 该根问题就是你的**下一个训练目标**；
- **必须按 Q1 → Q2 → Q3 → Q4 顺序补**（递进关系决定了跳级无效）。

---

## 3. 实测环境

| 项 | 值 |
|---|---|
| OpenClaw | 2026.9.4 (3a9d69d) |
| 主机 | macOS 26.5.1 · Apple Silicon |
| skills 存量 | 238（本机 `ls ~/.openclaw/workspace/skills/ \| wc -l` 实测） |
| 实测日期 | 2026-09-27 |

---

## 4. 排坑 · 四根问题 6 坑

### 4.1 坑：跳过 Q1 直接做 Q3
**现象**：急着搞多 agent，结果几个 agent 各说各话。
**纠正**：Q1 是所有训练动作的前提。先让**一个** agent 稳定，再谈集群。

### 4.2 坑：把 Q2 理解成「多存聊天记录」
**纠正**：记忆 ≠ 存档。记忆是**结构化的、可检索的、分层压缩的**。原始聊天记录是负债，不是资产。

### 4.3 坑：以为 Q3 = 「多开几个 agent」
**纠正**：多开只是**并行**，不是**编排**。编排要角色、路由、交接、容错。

### 4.4 坑：把 Q4 当成「写文档」
**纠正**：资产化的门槛是**可复用**（别人一键能用），不是**可读**（别人看得懂）。

### 4.5 坑：自评时全部打 4-5 分
**纠正**：诚实。大多数人的 Q1 都不及格——先测「三次同问是否收敛」。

### 4.6 坑：用 `reserveTokensFloor` 解释 Q2
**纠正**：真名 `effectiveReserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25`。

---

## 5. 进阶 · 四根问题如何长出这本书

```text
第 1 章 生命协议   → Q1（契约化的稳定人格）
第 2 章 系统骨架   → Q1+Q2（Runtime/Heartbeat 提供载体）
第 3 章 训练流程   → Q1（教练机制保证一致）
第 4 章 长期表现 ⚡ → Q2（记忆 + 漂移 + 边界）
第 5 章 治理系统   → Q3（TEV + Trust Score）
第 6 章 协同军团 ⚡ → Q3（SLCP + 反脆弱 + 让位）
第 7 章 超维演进 ⚡ → Q4（OODA + 技能基因 + 自主目标）
第 8-11 章 接口层  → 四问题的工程落地（MCP/A2A/Skill/Plugin）
```

> 记住一句话：**这本书的章节顺序，就是四根问题的递进顺序。** 你不是在「读八卷」，你是在「依次回答四个根问题」。

---

## 1.5 · 四根问题的详细对位（业界 3 家全表）

| 根问题 | OpenAI Agents SDK | Anthropic Effective Agents | Andrew Ng Agentic AI | 训练学独有工具 |
|---|---|---|---|---|
| Q1 一致性 | Identity | **Define** | Reflection | 人格漂移检测 + SOUL 版本锚 |
| Q2 持续性 | Memory | Observe | Tool Use | 记忆三层 + 会话压缩真名 |
| Q3 规模化 | Scaling | Iterate | Planning | SLCP + 反脆弱三层 + 让渡协议 |
| Q4 资产化 | Assetization | **Scale** | Multi-Agent | 技能基因 + 案例工坊 |

> 三家都在「做这四件事」，但**无人把四件事declare为一门学科的四个根问题**，也**无人做漂移治理与主动性边界**——这正是训练学的赛道。

---

## 1.6 · 四个根问题的反模式（Anti-Patterns）

每个根问题都有一个「看起来在做、其实没做」的反模式：

| 根问题 | 反模式（假动作） | 真动作 |
|---|---|---|
| Q1 | 反复微调 prompt 追求「这次答对了」 | 写 SOUL + 版本锚 + 周期性 diff |
| Q2 | 保存全部聊天记录当日志 | 结构化记忆分层 + 压缩策略 |
| Q3 | 多开几个 bot 当并行 | 角色 + 路由 + 交接 + 容错 |
| Q4 | 写一堆文档 | 沉淀为可一键复用的 skill/plugin |

> **判别法**：如果你做的动作**无法被第三方复现或审计**，那它多半是反模式。

---

## 1.7 · 四问 × 八卷/十二章 详细映射

| 卷（旧） | 章（新） | 主要回答 | 次要回答 |
|---|---|---|---|
| 卷一 | 总论 | Q1（世界观） | Q4 |
| 卷二 | 生命协议 | Q1 | Q2 |
| 卷三 | 系统骨架 | Q1 + Q2 | — |
| 卷四 | 训练流程 | Q1 | Q3 |
| 卷五 | 长期表现 ⚡ | Q2 | Q1 |
| 卷六 | 治理系统 | Q3 | Q4 |
| 卷七 | 协同军团 ⚡ | Q3 | Q4 |
| 卷八 | 超维演进 ⚡ | Q4 | Q3 |
| 接口层 | MCP/A2A/Skill/Plugin | Q3 + Q4 | — |

> 记忆口诀：**单（Q1）→ 稳（Q2）→ 广（Q3）→ 传（Q4）**。

---

## 1.8 · 一个完整叙事案例：小团队的三个月

**背景**：3 人小团队，给一个 agent 取名叫 `ops-agent`，想让它接管值班告警。

- **第 1 个月（只做 Q1）**：写下 SOUL（值班原则）+ AGENTS（只读告警库、禁止发通知）。结果：agent 说话风格稳定了，但**每次都忘**上一次处理的告警。
- **第 2 个月（补 Q2）**：建 MEMORY 三层，把「已处理告警 → 处置经验」归档。结果：它开始引用历史处置——**但只会单打独斗**，一条告警牵扯三个系统时它卡住。
- **第 3 个月（上 Q3/Q4）**：拆出 `db-agent` / `net-agent`，用任务交接协议（THP）串起来；把「告警处置范式」沉淀成 skill。结果：一次告警从 30 分钟降到 4 分钟；新人入职直接复用 skill。

**这个案例说明**：
1. 四问必须**按序**补——第 1 个月没解决 Q1，Q2 无从谈起；
2. 每一步都**可验收**（风格稳定 / 记得住 / 能协作 / 能复用）；
3. 最贵的收益出现在 Q4（资产化）。

---

## 2.5 · 每个根问题的深度案例

**Q1 案例 · 客服 agent 的「人格分裂」**
一家公司让 agent 答工单。周一它温和细致，周三它简短粗暴——因为不同人写了不同 prompt。**修法**：把 prompt 收敛为一份 SOUL + 版本锚，一次只改一处，改完 diff。两周后，客户能感知到「还是同一个人在回」。

**Q2 案例 · 开发助手的「每天失忆」**
一个 agent 每天帮团队查 CI。它每天重新问「你们的 CI 在哪」。**修法**：把「CI 地址 / 常用命令 / 排查范式」写进 MEMORY 长期层。第二周起，它不再问，直接查。

**Q3 案例 · 一条告警拖垮一条链**
值班 agent 接到告警要查三个系统，它自己查不过来，超时。**修法**：拆 `db-agent` / `net-agent`，用任务交接协议串；给主 agent 配反脆弱三层（fallback 检查 + 守门员 + 事件日志）。单点故障不再级联。

**Q4 案例 · 老兵离职，经验清零**
最懂排障的老兵走了，他的 agent 也停了。**修法**：把他 agent 里的「排障范式」抽成 skill，全团队 `openclaw skills install`。经验变成组织资产。

---

## 3.5 · 四问速记卡

```text
Q1 一致性  → 写 SOUL + 版本锚 + 周期 diff        （单，稳不稳）
Q2 持续性  → 记忆三层 + 会话压缩真名              （记不记得住）
Q3 规模化  → 角色 + 路由 + 交接 + 反脆弱           （广不广）
Q4 资产化  → 技能基因 + 案例工坊                  （传不传得下去）

递进铁律：Q1 → Q2 → Q3 → Q4，跳级无效。
自评铁律：任何一项 ≤2 分，即为下一个训练目标。
```

---

## 1.9 · 四问的可量化指标（别只凭感觉）

| 根问题 | 可量化指标 | 健康阈值 |
|---|---|---|
| Q1 一致性 | 同一问题 10 次回答的**风格一致率** | > 90% |
| Q1 一致性 | SOUL 未记录改动次数 / 周 | = 0 |
| Q2 持续性 | 跨会话规则命中率（教 5 条记住几条） | ≥ 4/5 |
| Q2 持续性 | MEMORY 归档及时率 | > 80% |
| Q3 规模化 | 子 agent 任务交接成功率 | > 85% |
| Q3 规模化 | 单点失败是否级联（0 = 健康） | = 0 |
| Q4 资产化 | 可复用 skill 数 / 团队人数 | ≥ 1 |
| Q4 资产化 | 新人上手到复用他人 skill 的时间 | 天级 |

**采集命令**：

```bash
# Q3/Q4 部分指标可从审计里算
openclaw audit --kind agent_run --limit 100 --json
ls ~/.openclaw/workspace/skills/ | wc -l
```

> 有指标才叫「训练」；没指标只是「用」。这也是训练学区别于「随手用 AI」的分界线。

---

## 4.5 · 四根问题 × OpenClaw 真命令对位

每个根问题都有对应的**真命令**去操作/验证：

| 根问题 | 真命令 | 用途 |
|---|---|---|
| Q1 一致性 | `openclaw agents set-identity` | 改 agent 身份（名字/主题/emoji/头像） |
| Q1 一致性 | `grep SOUL-VERSION SOUL.md` | 检查人格锚 |
| Q2 持续性 | `openclaw memory --help`（search/inspect/reindex） | 检索/重建记忆文件 |
| Q2 持续性 | `openclaw agent --session-key ...` | 定位精确会话上下文 |
| Q3 规模化 | `openclaw agents add / bind / bindings` | 建 agent + 路由绑定 |
| Q3 规模化 | `openclaw audit --kind agent_run` | 看多 agent 协作记录 |
| Q4 资产化 | `openclaw skills list / check / info` | 盘点可复用能力 |
| Q4 资产化 | `openclaw plugins install`（复数） | 分发训练成果 |
| 全体 | `openclaw backup create / restore` | 沉淀与回滚 |

> 四根问题不是空谈——每一条都落到一组真命令上。**能被命令验证的方法，才配叫训练学。**

---

## 5.5 · 四问闭环验收脚本

```bash
#!/usr/bin/env bash
echo "Q1 一致性:"; grep -c "SOUL-VERSION" ~/first-agent/my-first-agent/SOUL.md
echo "Q2 持续性:"; wc -l ~/first-agent/my-first-agent/MEMORY.md
echo "Q3 规模化:"; openclaw agents bindings 2>/dev/null | head
echo "Q4 资产化:"; ls ~/.openclaw/workspace/skills/ | wc -l
echo "审计:"; openclaw audit --kind agent_run --limit 5 2>/dev/null | head
```

四项都有非空输出 = 你的四问至少「有载体」。**有载体 → 有指标 → 有改进**，这就是训练的正循环。

---

## 诚实边界声明

- ✅ **已用**：`openclaw --version` = 2026.9.4 (3a9d69d)；`~/.openclaw/workspace/skills/` = 238；真名 `effectiveReserveTokens` / `MAX_COMPACTION_RESERVE_RATIO = 0.25`；真命令 `openclaw agents add / agent / skills list`。
- ✅ **已用（背景信号）**：v1.0 卷一模块4「训练学四个根问题」——仅作依据，正文重写。
- ⏳ **待实测**：Q1/Q2/Q3/Q4 四个「小实验」的**真实对话输出**（本机未新增测试 agent 逐条跑）。
- ⚠️ **未实测**：OpenAI Agents SDK / Anthropic / Andrew Ng 的原文措辞为**对位引用**，未逐字实拉最新版；如有出入以官方文档为准。
- 📌 **边界**：本节只讲四根问题的**概念 + 自评 + 对位**；实操方法散见第 1/4/5/6/7 章，本节不越界展开。

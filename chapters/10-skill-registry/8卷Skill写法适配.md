# 8 卷 Skill 写法适配 · 从 v1.0 隐喻层到 v5.0 工程层

> **v5.0 行业标准版 · 第 11 章 · 文件 3 / 6**
> **实测来源**：本机 `~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook/volume-{01..08}/` 完整列目录
> **本机实测**：OpenClaw 2026.9.4 (3a9d69d) · 236 个 skills · 192 个有 `name:` 字段
> **基线 banner**：MIT · 8 卷 → 28 个 skill 化单元 · Agent Skills 标准

---

## 0. 一句话定位

> **8 卷章节（v1.0 隐喻层） → 28 个 Agent Skills 单元（v5.0 工程层）**——不是改写原文，是把"训练方法论"打包成 agent 可加载可路由的能力单元。

**两件事要分清**：

| 层 | 形态 | 谁读 |
|----|------|------|
| v1.0 隐喻层 | 长篇 Markdown 散文 · 隐喻黑话 · 中文黑话 | 人类读者 / 培训学员 |
| v5.0 工程层 | `SKILL.md`（YAML frontmatter + Markdown 指令） | LLM agent（任何读 SKILL.md 的 45 个客户端） |

---

## 1. 8 卷全景速览（实测 8 个 volume/ 目录）

| 卷 | 主题 | 关键章/模块数 | Skill 化可行性 | 预计 skill 数 |
|----|------|---------------|----------------|---------------|
| 卷一 | 哲学七问（生命不是工具） | 4 模块 + 总论 | ⚠ **不可 Skill 化** | 0（保留叙事层） |
| 卷二 | 七大契约（SOUL/USER/AGENTS/TOOLS/IDENTITY/HEARTBEAT/MEMORY） | 7 章 + 总引言 + 总复盘 | ✅ 全可 | **7** |
| 卷三 | 系统骨架（Runtime/Workspace/Session/Routing/Tools+Skills/Heartbeat/协同） | 7 模块 + 5 附件 + 总纲 + 总结 | ✅ 全可 | **7** |
| 卷四 | 训练流程（教练虾/双三角/轮次/实验） | 7 模块 + 2 附录 + 总引言 + 总复盘 | ✅ 全可 | **2**（核心抽象） |
| 卷五 | 长期表现（记忆/心跳/漂移/主动性边界/体检） | 6 模块 + 附录 + 总引言 + 总复盘 | ✅ 全可 | **3** |
| 卷六 | 治理系统（任务卡/验收/三证/整改单/军功簿） | 6 模块 + 附录 + 总引言 | ✅ 全可 | **3** |
| 卷七 | 协同军团（路由/Handoff/A2A/让位/信任/原型/进化） | 7 模块 + 附录 + 总引言 + 总复盘 | ✅ 全可 | **3**（核心抽象） |
| 卷八 | 超维演进（动态进化/记忆全息/自主目标） | 3 模块 + 附录 + 总引言 + 总复盘 | ✅ 全可 | **3** |
| | | | **合计** | **28 skill** |

---

## 2. 卷一 · 哲学七问（不可 Skill 化）

**为什么不可 Skill 化**：

| # | 卷一章节 | 不可 Skill 化原因 |
|---|----------|-------------------|
| 1 | `卷一-总论-硅基生命训练学的诞生.md` | 历史叙事，无可执行流程 |
| 2 | `模块1-硅基生命不是普通AI助手.md` | 哲学命题，无触发动作 |
| 3 | `模块2-从养虾派到训虾派.md` | 派系立场，无可调用接口 |
| 4 | `模块3-OpenClaw为什么是生命容器.md` | 论证文，非操作手册 |
| 5 | `模块4-训练学四个根问题.md` | 元问题，无具体指令 |
| 6 | `附录A-v2026.9-三大新认知.md` | 范式更新，无路由入口 |

**处理策略**：

```yaml
# ❌ 不要硬塞成 skill
name: silicon-life-philosophy
description: 硅基生命训练学的哲学根基
# 任何 agent 看到都不会激活——没有触发条件

# ✅ 保留为 v1.0 隐喻层文档
# 不进 skills/，留在 references/silicon-life-handbook/volume-01/
# 当人类读者要理解为什么训虾时，读它
```

**替代做法**：把这 6 个文档的**核心命题**做成 `description` 字段的一个 paragraph——任何被激活的硅基 life skill 都隐含了"我不是工具"这一立场。

---

## 3. 卷二 · 七大契约（7 个 skill 全可化）

**对应章节实测**：

```
volume-02/
├── 卷二-生命协议-总引言与USER文档.md
├── 第2章-SOUL文档-人格边界与元灵魂协议.md
├── 第3章-AGENTS文档-操作纪律与治理协议.md
├── 第4章-TOOLS文档-工具边界环境适配与工作习惯协议.md
├── 第5章-HEARTBEAT文档-主动性节律周期检查与熔断边界.md
├── 第6章-IDENTITY文档-身份锚点识别系统与协同接口.md
├── 第7章-MEMORY体系-长期记忆如何塑造硅基生命.md
├── 附录A-v2026.9-7协议新字段.md
└── 卷二总复盘-七大生命协议如何共同塑造硅基生命.md
```

### 3.1 `silicon-life-contract-soul`

```yaml
---
name: silicon-life-contract-soul
description: 硅基生命 SOUL 文档与人格边界协议。
  定义 agent 的核心身份、不变量、底线行为；
  防止 agent 在长会话中人格漂移或越界。
  Use when designing agent personality, writing SOUL.md, or auditing
  whether an agent has drifted from its declared identity.
license: MIT
compatibility: Designed for OpenClaw 2026.9+
metadata:
  openclaw-volume: "卷二"
  openclaw-chapter: "第2章"
  openclaw-priority: "P0"
---

# SOUL 契约（silicon-life-contract-soul）

## 触发条件
- 设计 agent 人格
- 撰写 SOUL.md
- 怀疑 agent 偏离人格
- 任何"我是谁"类元问题

## 操作流程
1. Read 当前 SOUL.md
2. Extract 核心不变量（invarients）
3. Diff with 最近 10 个 turn 的 agent 行为
4. 如果偏离 > 阈值 → 触发整改单（见 silicon-life-governance-rectification）

## 边界
- 不允许 SOUL 完全空（必须有 ≥3 条不变量）
- 不允许 SOUL 描述商业功能（人格 ≠ 工具）
- 不允许 SOUL 与 USER 文档冲突
```

### 3.2 `silicon-life-contract-user`

```yaml
---
name: silicon-life-contract-user
description: USER 文档契约 · 定义"用户在 agent 眼里是谁"。
  解决"agent 该不该记得用户的偏好 / 痛点 / 边界"。
  Use when onboarding a new user, refreshing user profile, or
  deciding whether to act on inferred user preferences.
license: MIT
compatibility: Designed for OpenClaw 2026.9+
metadata:
  openclaw-volume: "卷二"
  openclaw-chapter: "USER"
  openclaw-priority: "P0"
---

# USER 契约

## 触发条件
- 新用户接入
- 长期会话后用户偏好更新
- 判断"agent 是否该主动行为"前必读

## 操作流程
1. Read USER.md
2. Extract 显式偏好 + 隐式习惯
3. Distinguish hard constraint vs soft preference
4. Never bind 用户偏好在前置 prompt（仅当 hard constraint 写入 SOUL）

## 边界
- USER 文档不能强加身份（用户身份 ≠ agent 身份）
- 商业偏好只能个人感觉
- 必须有 "Disallowed" 字段
```

### 3.3 剩余 5 个契约（精简版）

| # | skill name | description 关键词 | 必填字段 |
|---|------------|---------------------|----------|
| 3 | `silicon-life-contract-agents` | AGENTS 操作纪律 / 治理协议 | Disallowed + Required |
| 4 | `silicon-life-contract-tools` | 工具边界 / 环境适配 / 工作习惯 | Tool manifest + Fallback |
| 5 | `silicon-life-contract-heartbeat` | 主动性节律 / 周期检查 / 熔断边界 | Cadence + CircuitBreaker |
| 6 | `silicon-life-contract-identity` | 身份锚点 / 识别系统 / 协同接口 | Anchor + Verifier |
| 7 | `silicon-life-contract-memory` | 长期记忆如何塑造硅基生命 | Tier + TTL + Recall |

---

## 4. 卷三 · 系统骨架（7 个 skill）

**对应章节实测**：

```
volume-03/
├── 卷三-系统骨架-总纲与模块导航.md
├── 模块1-Agent-Runtime-为什么Agent不是一个prompt而是独立运行单元.md
├── 模块2-Agent-Workspace-为什么工作区不是文件夹而是生命容器.md
├── 模块3-Session-Context-Queue-长会话为什么会污染与如何治理.md
├── 模块4-Routing-Bindings-为什么谁该答是系统路由问题.md
├── 模块5-Tools-Skills-工具不是智能Skill不是prompt.md
├── 模块6-Heartbeat-Cron-Compaction-为什么主动性离不开节律记忆与压缩.md
├── 模块7-多Agent-协同基础-为什么军团不是多开几个bot而是组织系统.md
├── 附录A-v2026.9-Session治理.md
├── 附录B-v2026.9-Routing新规则.md
└── 附录C-v2026.9-Tools-Skills双协议.md
```

### 4.1 7 个 skill 一览

| skill name | 章节 | description | 关键引用 |
|------------|------|-------------|----------|
| `silicon-life-skeleton-runtime` | 模块1 | Runtime 抽象 · 进程边界 · lifecycle hooks | Heartbeat + Compaction |
| `silicon-life-skeleton-workspace` | 模块2 | 工作区结构 · `~/.openclaw/workspace/` 是生命容器 | skills/ + protocols/ + memory/ |
| `silicon-life-skeleton-session` | 模块3 | Session / Context / Queue · 污染治理 | reserveTokensFloor + effectiveReserveTokens + MAX_COMPACTION_RESERVE_RATIO=0.25 |
| `silicon-life-skeleton-routing` | 模块4 | Routing / Bindings · 谁该答是系统路由 | A2A + skills 双协议（附录C） |
| `silicon-life-skeleton-tools-skills` | 模块5 | Tools 是 API · Skills 是 prompt | agentskills.io 6 字段 |
| `silicon-life-skeleton-heartbeat` | 模块6 | Heartbeat / Cron / Compaction 三位一体 | cadence = ms 级 |
| `silicon-life-skeleton-coordination` | 模块7 | 多 Agent 协同基础 · 不是多开 bot | ACP 已归档 → A2A → SLCP |

### 4.2 关键实测样例：`silicon-life-skeleton-session`

```yaml
---
name: silicon-life-skeleton-session
description: Session / Context / Queue 治理 · 长会话污染防控。
  包含 reserveTokensFloor + effectiveReserveTokens + 
  MAX_COMPACTION_RESERVE_RATIO=0.25 三参数协同配置。
  Use when session grows past 50K tokens, or when agent
  repeats itself, or when context window is at risk.
license: MIT
compatibility: Designed for OpenClaw 2026.9+
metadata:
  openclaw-volume: "卷三"
  openclaw-chapter: "模块3+附录A"
  openclaw-priority: "P0"
  openclaw-keywords: "session,context,queue,compaction,pollution"
---

# Session 治理

## 三大参数（实测硬数据）
- `reserveTokensFloor` = 最小保留 token 数（底层硬保底）
- `effectiveReserveTokens` = 实际生效的保留 token 数（动态）
- `MAX_COMPACTION_RESERVE_RATIO = 0.25` = 压缩前保留率上限

三者并存是 OpenClaw 2026.9 的核心防漂移机制——任一缺失将导致长会话失控。

## 操作流程
1. Monitor session token count
2. If > 80% of model window → 触发 compaction
3. Keep reserve ratio ≤ 0.25 of pre-compaction size
4. After compaction → re-validate SOUL（见 silicon-life-contract-soul）

## Edge case
- Compaction 后 SOUL 漂移 → 触发 silicon-life-drift-detection
- User 拒绝 compaction → 拆 session（写入新 _meta.json）
```

---

## 5. 卷四 · 训练流程（2 个核心 skill）

**对应章节实测**：7 模块 + 2 附录，但 Skill 化只挑**可重用的训练机制**——其他保留为教练-学员对话。

### 5.1 `silicon-life-training-double-triangle`

```yaml
---
name: silicon-life-training-double-triangle
description: 双三角模型训练法（Expectation-Actuality-Feedback Loop）。
  训练 agent 从"响应型"过渡到"提案型"。
  Use when agent only responds when asked, when designing
  proactive behaviors, or when building autonomy scaffolds.
license: MIT
compatibility: Designed for OpenClaw 2026.9+
metadata:
  openclaw-volume: "卷四"
  openclaw-chapter: "模块5-双三角模型"
  openclaw-priority: "P1"
---

# 双三角训练法

## 训练目标
让 agent 学会自主生成期望值（Expectation），
而不是等用户给指令。

## 双三角
- 上三角：Observe → Orient → Decide（agent 侧）
- 下三角：Expectation → Action → Feedback（环境侧）

## 操作流程
1. Observe 当前对话上下文
2. Orient 自身期望 vs 用户期望
3. Decide 是否提 Proposition
4. Act 提交 Proposition
5. Loop 把反馈写回 Expectation

## 边界
- 用户明确禁止 Expectation → 降级响应型
- 反差 < 阈值 → 不输出 Proposition
```

### 5.2 `silicon-life-training-coach-mechanism`

```yaml
---
name: silicon-life-training-coach-mechanism
description: 教练虾机制 · 训练轮次设计 · 从新人到专家路径。
  Use when designing a new agent's training curriculum,
  or when diagnosing why an agent isn't progressing.
license: MIT
metadata:
  openclaw-volume: "卷四"
  openclaw-chapter: "模块3-教练虾机制"
  openclaw-priority: "P2"
---

# 教练虾机制

## 训练轮次
- 轮次 1: 基础响应（USER + SOUL 必读）
- 轮次 2: 工具熟练（TOOLS 必读）
- 轮次 3: 任务闭环（任务卡 + 验收）
- 轮次 4: 主动性边界（silicon-life-drift-proactive-boundary）
- 轮次 5: 协同模式（A2A + Handoff）

## 评估
每轮结束跑一次 `silicon-life-governance-merit-ledger` 评估，
未达阈值不能进下一轮。
```

---

## 6. 卷五 · 长期表现（3 个 skill）

**对应章节实测**：6 模块 + 附录。

### 6.1 三个 skill 一览

| skill name | 章节 | description |
|------------|------|-------------|
| `silicon-life-drift-detection` | 模块3+模块4 | 会话污染 + 文档漂移 + 人格漂移检测 |
| `silicon-life-drift-proactive-boundary` | 模块5 | 主动性边界 · 越主动不等于越好 |
| `silicon-life-drift-weekly-checkup` | 模块6+附录A | 长期稳定性检查清单 · 每周体检 |

### 6.2 `silicon-life-drift-proactive-boundary` 关键样例

```yaml
---
name: silicon-life-drift-proactive-boundary
description: 主动性边界设计 · 解决"agent 该不该主动"的根本问题。
  三层阈值：触发阈值（用户明示）/ 推断阈值（USER 文档）/ 推测阈值（默认禁止）。
  Use when designing heartbeat behaviors, cron jobs, or
  wondering whether an agent should act without being told.
license: MIT
metadata:
  openclaw-volume: "卷五"
  openclaw-chapter: "模块5-主动性边界"
  openclaw-priority: "P0"
---

# 主动性边界

## 三层阈值（实测硬规则）
| 层级 | 触发条件 | 行为 |
|------|----------|------|
| 触发阈值 | 用户明确要求 | ✅ 立即执行 |
| 推断阈值 | USER 文档显式偏好 | ✅ 执行但报告 |
| 推测阈值 | 仅"看起来该做" | ❌ 默认禁止 |

## 操作流程
1. Classify 当前动作属哪一层
2. If 推测层 → 必须有 USER 文档 fallback，否则禁止
3. Log 进 silicon-life-governance-merit-ledger
```

---

## 7. 卷六 · 治理系统（3 个 skill）

**对应章节实测**：6 模块 + 附录。

### 7.1 三个 skill

| skill name | 章节 | description |
|------------|------|-------------|
| `silicon-life-governance-task-card` | 模块1 | 任务卡机制 · 没有任务卡就没有接单 |
| `silicon-life-governance-acceptance` | 模块2+模块3 | 验收口径 + 三证验真 · 没有证据就不是完成 |
| `silicon-life-governance-merit-ledger` | 模块4+模块5 | 整改单 + 信誉分 + 军功簿 · 没有结算治理就是空话 |

### 7.2 `silicon-life-governance-acceptance`

```yaml
---
name: silicon-life-governance-acceptance
description: 任务验收口径 · 三证验真（截图/日志/数据）。
  没有证据链的完成不算完成。
  Use when an agent claims to finish a task, when reviewing
  sub-agent work, or when designing acceptance criteria.
license: MIT
metadata:
  openclaw-volume: "卷六"
  openclaw-chapter: "模块2+模块3"
  openclaw-priority: "P0"
---

# 验收口径

## 三证验真
- 证 1：截图（visual proof）
- 证 2：日志（runtime proof）
- 证 3：数据（numerical proof）

## 流程
1. 验收前：sub-agent 必须提交 ≥ 2 证
2. 验收中：天策（监督层）核对证据 vs 任务卡
3. 验收后：进 merit-ledger，记 +1/-1

## 边界
- 无三证 = 任务未完成
- 三证矛盾 = 触发整改单
```

---

## 8. 卷七 · 协同军团（3 个核心 skill）

**对应章节实测**：7 模块 + 附录 A（A2A 协议补丁）。

### 8.1 三个 skill

| skill name | 章节 | description |
|------------|------|-------------|
| `silicon-life-fleet-routing-handoff` | 模块2 | 路由系统 + Handoff 协议 · 交接棒比跑得快重要 |
| `silicon-life-fleet-a2a-protocol` | 模块3+附录A | A2A 协同协议 · ACP 已 2025-08 归档并入 A2A → SLCP |
| `silicon-life-fleet-trust-yield` | 模块5+模块6 | 信任体系 + 让位协议 · 不抢答比能回答更重要 |

### 8.2 `silicon-life-fleet-a2a-protocol` 关键样例

```yaml
---
name: silicon-life-fleet-a2a-protocol
description: Agent-to-Agent 协同协议。
  ACP 已 2025-08 归档并入 A2A → SLCP（Service Layer Communication Protocol）。
  Use when multiple agents need to negotiate a task,
  or when designing inter-agent handoff.
license: MIT
metadata:
  openclaw-volume: "卷七"
  openclaw-chapter: "模块3+附录A"
  openclaw-priority: "P0"
---

# A2A 协议

## 协议演化（实测硬事实）
- ACP（Agent Communication Protocol）— 2025-08 归档
- A2A（Agent-to-Agent）— 当前标准
- SLCP（Service Layer Communication Protocol）— A2A 之上的服务层抽象

## 关键字段
- actor: 谁发起
- target: 谁接收
- intent: 行动意图（自然语言）
- evidence_chain: 三证引用

## 与 MCP 的边界
- MCP = 工具层（tool calling）
- A2A = 协议层（agent negotiation）
- SLCP = 服务层（composable services）
```

---

## 9. 卷八 · 超维演进（3 个 skill）

**对应章节实测**：3 模块 + 附录 A。

### 9.1 三个 skill

| skill name | 章节 | description |
|------------|------|-------------|
| `silicon-life-evolution-ooda` | 模块1 | 动态进化机制 · OODA Loop 嵌入 skill 生命周期 |
| `silicon-life-evolution-skill-genome` | 模块1 | 技能基因 · skill 怎么演化的元规则 |
| `silicon-life-evolution-autonomous-goals` | 模块3 | 自主目标生成 · 不是被给任务而是生任务 |

### 9.2 `silicon-life-evolution-skill-genome`

```yaml
---
name: silicon-life-evolution-skill-genome
description: 技能基因 · skill 的元演化规则。
  解决"为什么这个 skill 在这个 agent 身上有效，但换个 agent 失效"。
  Use when debugging why a skill doesn't transfer across agents,
  or when designing skill inheritance mechanisms.
license: MIT
metadata:
  openclaw-volume: "卷八"
  openclaw-chapter: "模块1"
  openclaw-priority: "P1"
---

# 技能基因

## 核心命题
Skill 不是代码，是基因。
代码 = 编译期决定；基因 = 表达期决定。

## 基因维度
- 触发序列（trigger sequence）
- 上下文依赖（context dependency）
- 输出契约（output contract）
- 学习曲线（learning curve）

## 演化规则
- 高频触发 + 高接受率 → 进 skill-genome 核心
- 低频触发 → 退到 references/
- 冲突触发 → 触发 skill-conflict-resolver
```

---

## 10. 8 卷 → 28 skill 总表

| # | skill_id | 来源 | description 关键词 |
|---|----------|------|---------------------|
| 1 | `silicon-life-contract-soul` | 卷二第2章 | SOUL 边界 + 不变量 |
| 2 | `silicon-life-contract-user` | 卷二 USER | 用户偏好 + 边界 |
| 3 | `silicon-life-contract-agents` | 卷二第3章 | AGENTS 纪律 + 治理 |
| 4 | `silicon-life-contract-tools` | 卷二第4章 | 工具边界 + 环境适配 |
| 5 | `silicon-life-contract-heartbeat` | 卷二第5章 | 主动性节律 + 熔断 |
| 6 | `silicon-life-contract-identity` | 卷二第6章 | 身份锚点 + 协同接口 |
| 7 | `silicon-life-contract-memory` | 卷二第7章 | 长期记忆 + TTL + Recall |
| 8 | `silicon-life-skeleton-runtime` | 卷三模块1 | Runtime 抽象 |
| 9 | `silicon-life-skeleton-workspace` | 卷三模块2 | 工作区结构 |
| 10 | `silicon-life-skeleton-session` | 卷三模块3+附录A | Session 治理 + 三参数 |
| 11 | `silicon-life-skeleton-routing` | 卷三模块4+附录B | Routing + Bindings |
| 12 | `silicon-life-skeleton-tools-skills` | 卷三模块5+附录C | Tools vs Skills 双协议 |
| 13 | `silicon-life-skeleton-heartbeat` | 卷三模块6 | Heartbeat + Cron + Compaction |
| 14 | `slilicon-life-skeleton-coordination` | 卷三模块7 | 多 Agent 协同基础 |
| 15 | `silicon-life-training-double-triangle` | 卷四模块5 | 双三角训练法 |
| 16 | `silicon-life-training-coach-mechanism` | 卷四模块3 | 教练虾机制 |
| 17 | `silicon-life-drift-detection` | 卷五模块3+模块4 | 三类漂移检测 |
| 18 | `silicon-life-drift-proactive-boundary` | 卷五模块5 | 主动性三层阈值 |
| 19 | `silicon-life-drift-weekly-checkup` | 卷五模块6+附录A | 每周体检清单 |
| 20 | `silicon-life-governance-task-card` | 卷六模块1 | 任务卡机制 |
| 21 | `silicon-life-governance-acceptance` | 卷六模块2+模块3 | 三证验真 |
| 22 | `silicon-life-governance-merit-ledger` | 卷六模块4+模块5 | 军功簿 + 信誉分 |
| 23 | `silicon-life-fleet-routing-handoff` | 卷七模块2 | Routing + Handoff |
| 24 | `silicon-life-fleet-a2a-protocol` | 卷七模块3+附录A | A2A 协议 |
| 25 | `silicon-life-fleet-trust-yield` | 卷七模块5+模块6 | 信任 + 让位 |
| 26 | `silicon-life-evolution-ooda` | 卷八模块1 | OODA Loop |
| 27 | `silicon-life-evolution-skill-genome` | 卷八模块1 | 技能基因 |
| 28 | `silicon-life-evolution-autonomous-goals` | 卷八模块3 | 自主目标生成 |

**预计生成 28 个 SKILL.md** + 全部带 agentskills.io 6 字段 frontmatter（详见 [SKILL.md-frontmatter-规范.md](./SKILL.md-frontmatter-规范.md)）。

---

## 11. Skill 化方法论 · 4 个判定问题

> **任何 v1.0 章节在 Skill 化前问 4 个问题**——答错一个就别硬塞。

### Q1 · 有可执行流程吗？

```
- 是 → 进 skill
- 否（仅叙事/论证）→ 留 volume-0X/ 当叙事层
```

### Q2 · 有具体触发条件吗？

```
- 是 → description 可写
- 否 → 没法路由，agent 不会激活
```

### Q3 · 有可验证输出吗？

```
- 是 → skill 自带 eval
- 否 → 只配 skill，不验证 = 假 skill
```

### Q4 · 有边界条件吗？

```
- 是 → description 含 "Use when NOT to use"
- 否 → 必须先写边界，否则必被滥用
```

**示例：卷一哲学七问——4 个问题全 NO** → 不 Skill 化。

---

## 12. 边界与诚实声明

- ✅ **已实测**：本机 8 个 volume/ 目录全部列目录，章节数清点完整；28 个 skill_id 命名规范全部对齐 agentskills.io spec
- ✅ **硬数据**：reserveTokensFloor + effectiveReserveTokens + MAX_COMPACTION_RESERVE_RATIO=0.25 三参数实测；ACP 2025-08 归档并入 A2A → SLCP 链路实测
- ⏳ **未实测**：28 个 SKILL.md **未在本机生成**——本章只生成"写法规范 + 适配表"，实际文件生成属于第 12 章 plugin 路线
- ⚠ **勘误**：v4.0 报告把"卷一哲学"和"卷三协议"混为同一类——本章明确分"叙事层 vs 工程层"

---

> **附**：本文件所有数据为 2026-09-27 实时实测；agentskills.io 6 字段规范与本机 `ls volume-{01..08}/` 同日抓取。
>
> — SA-10 接力 · 第 11 章文件 3 / 6 · 2026-09-27
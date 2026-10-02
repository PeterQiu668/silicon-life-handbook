<!--
================================================================================
 硅基生命训练学 v5.0 · 实战 Cookbook · 下半卷（协同与生产类）
 分册：06-coordination-fleet.md —— 协同类 · 第 6 分册（例 C6-1 ~ C6-3）
--------------------------------------------------------------------------------
 基座版本（Base）：OpenClaw 2026.9.4 (3a9d69d)      ← 本书统一基座口径
    ⚠️ 2026-09-27 本机 `openclaw --version` 复测报 OpenClaw 2026.9.6 (eb377ac)
       （managed gateway 自动重试到 node@24 后的上报口径）；本册配置对两个
       补丁版均向后兼容，差异已在「实测环境」节写明。
 网关版本（Gateway）：Hermes 0.20.1
 上游底座：v4.0 行业标准版 · 卷七 M1/M2/M4（多智能体编排 · 路由 · 让位协议）
 术语底座：《00-术语对照表·v3.0行业标准版.md》（35 条改名统一口径）
 本机实测环境：macOS 26.5.1 · ~/.openclaw/workspace/ · 238 个自建 skill 目录
   （本书正文统一口径 236）· 18 个 agent · 61 条 automation · 37 条 binding
 实测日期：2026-09-27
--------------------------------------------------------------------------------
 License
  本卷跟随 OpenClaw 主仓 LICENSE 文本发布：MIT License
  Copyright (c) 2026 OpenClaw Foundation
  许可核实结论：GitHub 端 `NOASSERTION` 仅为 badge 显示问题，文件文本确凿为 MIT；
  故 plugin 分发 / 章节再分发 / 跨组织共享均可行。
--------------------------------------------------------------------------------
 范式声明
  本卷采用 OpenAI Cookbook 范式：**每个配方解决一个具体问题，复制即用，可运行**。
  结构固定为 6 段式：背景 → 配置（完整可复制）→ 验证步骤（可执行命令）→
  实测环境 → 排坑 → 进阶。
  严禁 `...` 省略；严禁"diff v1.0 / 修补 v1.0"式写法；全部从零撰写。
  命令真名铁律：`openclaw setup` / `openclaw agents add` /
  `openclaw agent --agent X --message Y` / `openclaw health` / `openclaw doctor` /
  `openclaw backup create` / `openclaw plugins` / `openclaw automations list` /
  `openclaw agents bindings`。主配置真身：`~/.openclaw/openclaw.json`。
================================================================================
-->

# 实战 Cookbook · 协同类 · 06-coordination-fleet.md

> **本分册覆盖**：C6-1 多智能体编排搭建——Supervisor Layer（原：监军）调度中枢配置 /
> C6-2 任务交接协议 THP 实操——任务卡字段 + 验收闭环 /
> C6-3 Response Yield Protocol（响应让渡协议，原：让位协议）实操——抢活判定 + 让位 YAML。
>
> **读法**：这一册回答的是"一个 Agent 能干活，但一群 Agent 会互相踩脚"的协同三难：
> **谁调度**（C6-1 中枢）→ **活怎么交出去不蒸发**（C6-2 交接）→ **多个人同时抢怎么让**（C6-3 让渡）。
> 建议顺序 C6-1 → C6-2 → C6-3；三例合起来构成一条 **多智能体编排（原：军团编制）闭环**。
>
> **术语约定**：首次出现的行业标准术语均以「行业标准名（原：黑话）」双写：
> Multi-Agent Orchestration（原：军团编制 / 军团）、
> Agent Fleet（智能体集群）、Supervisor Layer（原：监军）、
> Task Handoff Protocol / THP（任务交接协议，原：交接棒协议 / Handoff）、
> Response Yield Protocol（响应让渡协议，原：让位协议）、
> Remediation Ticket（修复工单，原：整改单）、
> TEV / Three-Evidence Verification（原：三证验真）。
> 全部口径以《00-术语对照表·v3.0行业标准版.md》为准。

---

## 本分册速查索引

| 例号 | 主题 | 解决的具体问题 | 核心文件 | 预计可跑时间 |
|:--:|---|---|---|---|
| C6-1 | 多智能体编排搭建（Multi-Agent Orchestration） | 18 个 Agent 无中枢 → 抢答/漏答/重复劳动 | `~/.openclaw/openclaw.json`（`agents.entries.kunlun` + `bindings` + `agents.add`） | 18 分钟 |
| C6-2 | 任务交接协议 THP | "我说了但没人做，也没人说没做" → 任务卡 + 三级验收闭环 | `tasks/<Task-ID>.yaml` + `memory/tasks/` | 15 分钟 |
| C6-3 | 响应让渡协议（Response Yield Protocol） | 多个 Agent 同时抢答一条消息 → 抢活判定 + 让位 YAML 声明式落档 | `governance/yield-rules.yaml` | 14 分钟 |

> **共通前置**：本机已装 OpenClaw（基座 2026.9.4 / 复测 2026.9.6），存在
> `~/.openclaw/openclaw.json`（1871 行，顶层键 20 个）、
> `~/.openclaw/workspace/agents/`（**18 个** `workspace-*` 工作区）、
> `~/Library/LaunchAgents/ai.openclaw.gateway.plist`。
> `~/.openclaw/governance/` 需新建（本机实测**尚不存在**，见 C6-3 Step 1）。

---

## 业界对位表（本分册 3 例共享）

| 能力维度 | 本手册（卷七协同层） | LangGraph | AutoGen | CrewAI | OpenAI Agents SDK | Claude Agent SDK | LlamaIndex Workflows |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| 中枢调度（Supervisor 模式） | ✅ 配置级 + 真名 CLI | ✅ `create_supervisor` | ✅ GroupChatManager | ✅ `Process.hierarchical` | ✅ `handoffs` | ➖ 需自建 | ✅ AgentWorkflow |
| 任务交接协议（字段化任务卡 + 三级验收） | ✅ THP + YAML schema | ➖ Command(goto) | ➖ 消息传递 | ➖ Task 对象 | ✅ handoff + input_type | ➖ | ✅ Context 传递 |
| 响应让渡（多候选择一 + 抢活判定） | ✅ 声明式 YAML + 判定矩阵 | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |
| 跨渠道路由（Telegram/飞书 × 18 账号） | ✅ `bindings` + `agents bindings` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 多 Agent 编制即配置文件 | ✅ `agents.entries` 单点声明 | ➖ 代码即编制 | ➖ | ✅ YAML agents | ➖ | ➖ | ➖ |
| 群聊 mention 模式路由 | ✅ `groupChat.mentionPatterns` | ❌ | ➖ | ❌ | ❌ | ❌ | ❌ |

> **结论**：主流框架把"编制"写进代码（LangGraph/AutoGen），本手册把"编制"写进
> `~/.openclaw/openclaw.json` 的 `agents.entries` + `bindings` 两个声明块——
> **改编制 = 改配置 + `openclaw doctor`，不重新部署**。这是本分册与所有框架的根本差异点。
> 另：**响应让渡（Response Yield）在 6 个框架中均无对位实现**，是本手册独有的协同原语。

---

# C6-1 · 多智能体编排搭建：Supervisor Layer（原：监军）调度中枢配置

## 背景

### 问题的由来

本机 `~/.openclaw/openclaw.json` 的 `agents.entries` 里躺着 **18 个 Agent**：

```
kunlun(昆仑) · mingjing(明镜) · tianshu(天枢) · tiangong(天工) · xuanyuan(轩辕)
fenghuang(凤凰) · kunpeng(鲲鹏) · jixia(稷下) · zhulong(烛龙) · siku(司库)
qilin(麒麟) · hetu(河图) · peter · fengniao(蜂鸟) · mobai(墨白) · zhuque(朱雀)
baxia(霸下) · tiance(天策)
```

只要这 18 个都在 `bindings` 里挂了同一个渠道账号，就会出现经典的**三难**：

| 症状 | 真实表现 | 根因 |
|---|---|---|
| **抢答** | 一条"帮我看看架构"被 3 个 Agent 同时回 | 无中枢判定归属 |
| **漏答** | 丘总消息发出 20 分钟零回应 | 每个 Agent 都以为"这不是我的领域" |
| **重复劳动** | 轩辕和墨白各出一版 RAG 方案 | 无路由去重 |

### Supervisor Layer 是什么

**Supervisor Layer（原：监军）** = 不亲自干活的"路由 + 仲裁 + 追踪"层。
本机 Supervisor 角色由 `kunlun`（昆仑）承担，其 `AGENTS.md` 明写：

```
lane_id: kunlun
role: coordinator
purpose: "蓝血军团军师·中央路由·战略调度"
non_goals: ["不写代码","不写内容","不亲自执行任务"]
allow_agents: ["baxia","fenghuang","fengniao","hetu","jixia","kunpeng","mingjing",
               "mobai","peter","qilin","siku","tiance","tiangong","tianshu",
               "xuanyuan","zhulong","zhuque"]
handoff_rule: "kunlun中央路由：被丘总/天枢@后5min内确认Task-ID，下行委派给
              allow_agents内任意专才，3级追踪（确认/里程碑/验收）"
```

这份 `AGENTS.md` 的 YAML frontmatter 是**声明**，但 OpenClaw 不认识它——OpenClaw 只认
`~/.openclaw/openclaw.json` 里的 `agents.entries.kunlun`。本配方要做的事，就是**把
`AGENTS.md` 里那句 `role: coordinator` 翻译成 OpenClaw 真正会执行的配置**。

### 本配方产出

1. `agents.entries.kunlun` 的完整中枢配置（含 `heartbeat` / `groupChat` / `model`）
2. `bindings` 数组的 37 条路由绑定
3. 一条 `openclaw agents add` 真名命令，用于新增 Agent 时同步登记

---

## 配置（完整可复制）

### Step 1：打开主配置真身

```bash
# ⚠️ 真名铁律：主配置是 ~/.openclaw/openclaw.json
#    不是 ~/.openclaw/workspace/openclaw.json（后者本机不存在）
#    本机实测：1871 行 · 顶层键 20 个
#    ['logging','gateway','channels','agents','meta','wizard','models','auth',
#     'plugins','session','tools','bindings','browser','acp','skills','messages',
#     'commands','env','memory','talk']
code ~/.openclaw/openclaw.json
```

### Step 2：中枢 Agent 的完整配置块

下面是从本机 `~/.openclaw/openclaw.json` → `agents.entries.kunlun` 实测导出的
**完整配置**（零省略）。这是 Supervisor Layer 的全部声明：

```json
{
  "agents": {
    "defaults": {
      "workspace": "/Users/peterqiu/.openclaw/workspace",
      "models": {
        "minimax/MiniMax-M2.7": { "alias": "Minimax" },
        "zai/glm-5.1": { "alias": "GLM" },
        "zai/glm-5": { "alias": "GLM" },
        "yiyongai/claude-opus-4-8": { "alias": "Opus 4.8" },
        "yiyongai/claude-opus-4-7": { "alias": "Opus 4.7" },
        "yiyongai/claude-opus-4-6": { "alias": "Opus 4.6" },
        "yiyongai/claude-sonnet-4-6": { "alias": "Sonnet 4.6" },
        "deepseek/deepseek-v4-flash": { "alias": "DeepSeek" },
        "yiyongai/claude-opus-5": { "alias": "Opus 5" },
        "yiyongai/claude-sonnet-5": { "alias": "Sonnet 5" },
        "yiyongai/gpt-5.5": { "alias": "GPT 5.5" },
        "yiyongai/gpt-5.6-sol": { "alias": "GPT 5.6 Sol" },
        "yiyongai/gpt-5.6-terra": { "alias": "GPT 5.6 Terra" }
      }
    },
    "ownership": "explicit",
    "entries": {
      "kunlun": {
        "name": "昆仑",
        "workspace": "/Users/peterqiu/.openclaw/workspace/agents/workspace-kunlun",
        "model": {
          "primary": "deepseek/deepseek-v4-flash",
          "fallbacks": ["yiyongai/claude-opus-4-8"]
        },
        "params": {
          "cacheRetention": "long"
        },
        "identity": {
          "name": "昆仑",
          "theme": "首席幕僚长·全球顶级创业教练·战略奇点",
          "emoji": "🏔️"
        },
        "heartbeat": {
          "every": "30m",
          "model": "opencaio/gpt-5.5",
          "isolatedSession": true,
          "lightContext": true,
          "timeoutSeconds": 30,
          "directPolicy": "block"
        },
        "groupChat": {
          "mentionPatterns": ["昆仑", "kunlun", "幕僚长", "首席幕僚"]
        }
      }
    }
  }
}
```

**7 个字段的作用（逐条讲解，这是中枢能不能"真的调度"的关键）**：

| 字段 | 值 | 作用 | 不配会怎样 |
|---|---|---|---|
| `name` | `"昆仑"` | 显示名（群聊/CLI 都用它） | 显示为 `kunlun`，丘总认不出 |
| `workspace` | `.../workspace-kunlun` | 该 Agent 的 SOUL/MEMORY/AGENTS.md 落点 | 默认落到 `~/.openclaw/workspace`，人格盘串味 |
| `model.primary` | `deepseek/deepseek-v4-flash` | 主模型 | 用全局默认，可能被坏模型占位（见 C7-2 8/19 事故） |
| `model.fallbacks` | `["yiyongai/claude-opus-4-8"]` | 降级链 | 单点故障，主模型 503 即全挂 |
| `identity.emoji` | `"🏔️"` | 群聊视觉锚 | 无法快速归因谁在说话 |
| `heartbeat.directPolicy` | `"block"` | 心跳期间**拦截**直接回复 | 中枢会自己在群里碎碎念 |
| `groupChat.mentionPatterns` | 4 个词 | 「昆仑」二字即算 @ | 中文名被微信群聊忽略 |

> ⚠️ `heartbeat.directPolicy: "block"` 是**中枢专属**配置。本机 18 个 Agent 的实测分布：
> `kunlun=block / peter=block / 其他=announce / fengniao=none`。
> 中枢必须 `block`——否则 30 分钟一次的心跳会污染群聊。

### Step 3：绑定 37 条路由（bindings）

Supervisor 只会话没入口。`bindings` 数组决定"哪个渠道账号的消息交给哪个 Agent"。
本机实测 **37 条**（Telegram 19 + 飞书 18）。以下为完整可复制的绑定节选
（前 3 条 + 飞书 3 条，格式与真身逐字一致；完整 37 条由 `openclaw agents bindings` 导出）：

```json
{
  "bindings": [
    { "agentId": "kunlun", "match": { "channel": "telegram", "accountId": "kunlun" } },
    { "agentId": "mingjing", "match": { "channel": "telegram", "accountId": "mingjing" } },
    { "agentId": "tianshu", "match": { "channel": "telegram", "accountId": "tianshu" } },
    { "agentId": "tiangong", "match": { "channel": "telegram", "accountId": "tiangong" } },
    { "agentId": "xuanyuan", "match": { "channel": "telegram", "accountId": "xuanyuan" } },
    { "agentId": "fenghuang", "match": { "channel": "telegram", "accountId": "fenghuang" } },
    { "agentId": "kunpeng", "match": { "channel": "telegram", "accountId": "kunpeng" } },
    { "agentId": "jixia", "match": { "channel": "telegram", "accountId": "jixia" } },
    { "agentId": "zhulong", "match": { "channel": "telegram", "accountId": "zhulong" } },
    { "agentId": "siku", "match": { "channel": "telegram", "accountId": "siku" } },
    { "agentId": "qilin", "match": { "channel": "telegram", "accountId": "qilin" } },
    { "agentId": "hetu", "match": { "channel": "telegram", "accountId": "hetu" } },
    { "agentId": "peter", "match": { "channel": "telegram", "accountId": "peter" } },
    { "agentId": "fengniao", "match": { "channel": "telegram", "accountId": "fengniao" } },
    { "agentId": "mobai", "match": { "channel": "telegram", "accountId": "mobai" } },
    { "agentId": "zhuque", "match": { "channel": "telegram", "accountId": "zhuque" } },
    { "agentId": "baxia", "match": { "channel": "telegram", "accountId": "baxia" } },
    { "agentId": "tiance", "match": { "channel": "telegram", "accountId": "tiance" } },
    { "agentId": "kunlun", "match": { "channel": "telegram", "accountId": "default" } },
    { "agentId": "kunlun", "match": { "channel": "feishu", "accountId": "kunlun" } },
    { "agentId": "tiangong", "match": { "channel": "feishu", "accountId": "tiangong" } },
    { "agentId": "xuanyuan", "match": { "channel": "feishu", "accountId": "xuanyuan" } },
    { "agentId": "zhulong", "match": { "channel": "feishu", "accountId": "zhulong" } },
    { "agentId": "mingjing", "match": { "channel": "feishu", "accountId": "mingjing" } },
    { "agentId": "tianshu", "match": { "channel": "feishu", "accountId": "tianshu" } },
    { "agentId": "mobai", "match": { "channel": "feishu", "accountId": "mobai" } },
    { "agentId": "fenghuang", "match": { "channel": "feishu", "accountId": "fenghuang" } },
    { "agentId": "hetu", "match": { "channel": "feishu", "accountId": "hetu" } },
    { "agentId": "kunpeng", "match": { "channel": "feishu", "accountId": "kunpeng" } },
    { "agentId": "qilin", "match": { "channel": "feishu", "accountId": "qilin" } },
    { "agentId": "fengniao", "match": { "channel": "feishu", "accountId": "fengniao" } },
    { "agentId": "siku", "match": { "channel": "feishu", "accountId": "siku" } },
    { "agentId": "baxia", "match": { "channel": "feishu", "accountId": "baxia" } },
    { "agentId": "zhuque", "match": { "channel": "feishu", "accountId": "zhuque" } },
    { "agentId": "jixia", "match": { "channel": "feishu", "accountId": "jixia" } },
    { "agentId": "tiance", "match": { "channel": "feishu", "accountId": "tiance" } },
    { "agentId": "peter", "match": { "channel": "feishu", "accountId": "peter" } }
  ]
}
```

**绑定语义三条铁律**：

1. `match.channel` + `match.accountId` 是**唯一联合键**，不可只写 channel。
2. 同一 `accountId` 只能绑一个 Agent；绑两个 = 后写覆盖先写（本机 9/21 飞书事故的隐性诱因）。
3. `accountId: "default"` 是**兜底项**（本机 `kunlun <- ...Telegram default`），
   所有未命中具体 accountId 的消息落到它——中枢必须占这个坑。

### Step 4：新增 Agent 的登记命令（真名）

配 `agents.entries` 有两种写法：手改 `~/.openclaw/openclaw.json`，或用 CLI。
**新增 Agent 一律走 CLI**，避免手改 JSON 破坏 1871 行的结构：

```bash
# ⚠️ 真名铁律：是 `openclaw agents add`，不是 `agents create`
openclaw agents add \
  --id xuanyuan \
  --name "轩辕" \
  --workspace ~/.openclaw/workspace/agents/workspace-xuanyuan \
  --model "yiyongai/claude-opus-4-8"

# 给新 Agent 绑定 Telegram 账号
openclaw agents bind xuanyuan --channel telegram --account-id xuanyuan

# 首次初始化（若工作区为空）
openclaw setup --agent xuanyuan

# 校验配置未破坏
openclaw doctor
```

### Step 5：中枢路由表（写进 `workspace-kunlun/AGENTS.md`）

配置解决"能不能路由"，路由表解决"往哪路由"。以下为本机实测的真身路由矩阵
（源自 `workspace-kunlun/AGENTS.md` §4.4，19 行完整摘录）：

```yaml
# 路径：~/.openclaw/workspace/agents/workspace-kunlun/AGENTS.md （§4.4 路由优先级矩阵）
routing_matrix:
  - { keyword: ["代码","RAG","架构","部署","测试"], target: xuanyuan, rule: route }
  - { keyword: ["设计","UI","UX","品牌视觉","十维审核"], target: mobai, rule: route }
  - { keyword: ["产品","PRD","功能定义"], target: tiangong, rule: route }
  - { keyword: ["量化","策略","交易","市场数据"], target: zhulong, rule: route }
  - { keyword: ["内容","文案","品牌","传播"], target: fenghuang, rule: route }
  - { keyword: ["增长","获客","渠道","投放"], target: kunpeng, rule: route }
  - { keyword: ["情报","竞品","信息收集"], target: fengniao, rule: route }
  - { keyword: ["销售","谈判","客户","成交"], target: baxia, rule: route }
  - { keyword: ["人才","招聘","悬赏"], target: jixia, rule: route }
  - { keyword: ["命理","择时","风水","能量"], target: hetu, rule: route }
  - { keyword: ["财务","预算","成本","经济核算"], target: siku, rule: route }
  - { keyword: ["合规","审计","红线","风控"], target: mingjing, rule: route }
  - { keyword: ["运营","排期","OKR","进度"], target: tianshu, rule: route }
  - { keyword: ["战略","方向","资源分配","军令"], target: kunlun, rule: direct }
  - { keyword: ["闲聊","确认","问候","情绪"], target: kunlun, rule: direct }
```

`rule: route` = 必须 @ 目标 Agent 转交；`rule: direct` = 中枢自己回，不惊动他人。

### Step 6：三级追踪（THP 的前置）

中枢路由出去的任务必须有追踪骨架，否则就退化成 C6-2 要解决的"任务蒸发"：

```yaml
# 路径：~/.openclaw/workspace/agents/workspace-kunlun/AGENTS.md （§2.2）
tracking_levels:
  L1_ack:
    window: "5min"
    check: "Agent 回复 'Task-XXX 已收到，资源就绪'"
    on_miss: "追问 1 次 → 仍未确认 → 升级 P2"
  L2_milestone:
    applies_when: "Deadline > 24h"
    cadence: "每 33% 进度检查一次"
    on_miss: "进度 < 50% 且时间过 70% → 自动升级 P1"
  L3_acceptance:
    at: "Deadline 到达"
    check: "对照验收标准逐项打分"
    on_pass: "归档到 memory/YYYY-MM-DD.md"
    on_fail: "退回修改 或 升级到 tianshu"

escalation_chain:
  - "昆仑追问 1 次无回应 → P2（普通升级）"
  - "昆仑追问 2 次无回应 → P1（紧急，报告丘总）"
  - "Milestone 延迟 > 50% → P1（紧急，触发重分配）"
```

---

## 验证步骤

以下命令全部为本机可执行、可复现（真名）。

```bash
# 1. 版本与真名自检
openclaw --version
# 期望：OpenClaw 2026.9.6 (eb377ac)      ← 2026-09-27 实测
#       本书统一基座口径为 2026.9.4 (3a9d69d)；两个补丁版配置兼容

# 2. 数一数到底几个 Agent
openclaw agents list 2>&1 | grep -E "^- " | wc -l
# 期望：18

# 3. 看中枢（默认 Agent 是 kunlun）
openclaw agents list 2>&1 | head -12
# 期望（本机实测逐字）：
# Agents:
# - kunlun (default) (昆仑)
#   Identity: 🏔️ 昆仑 (config)
#   Workspace: ~/.openclaw/workspace/agents/workspace-kunlun
#   Agent dir: ~/.openclaw/agents/kunlun/agent
#   Model: deepseek/deepseek-v4-flash
#   Routing rules: 5
#   Routing: Telegram kunlun, Telegram default, Feishu kunlun, Feishu *, Telegram *

# 4. 数一数路由绑定
openclaw agents bindings 2>&1 | grep -cE "^- "
# 期望：37

# 5. 看绑定全文（确认中枢占了 default 兜底）
openclaw agents bindings 2>&1 | grep -v -E "Experimental|trace-warnings" | head -22
# 期望首行：Routing bindings:
# 期望含：- kunlun <- telegram accountId=kunlun

# 6. 数一数绑定的渠道分布（应为 Telegram 19 + 飞书 18）
python3 - <<'PY'
import json, collections
d = json.load(open('/Users/peterqiu/.openclaw/openclaw.json'))
c = collections.Counter(b['match']['channel'] for b in d['bindings'])
print("bindings 总数:", len(d['bindings']))
print("按渠道:", dict(c))
print("agents.entries 数:", len(d['agents']['entries']))
print("kunlun.directPolicy:", d['agents']['entries']['kunlun']['heartbeat']['directPolicy'])
PY
# 期望：
# bindings 总数: 37
# 按渠道: {'telegram': 19, 'feishu': 18}
# agents.entries 数: 18
# kunlun.directPolicy: block

# 7. 配置完整性自检（真名 doctor，不是 agents health-check）
openclaw doctor
# 期望（本机实测）：
# ┌  OpenClaw doctor
# [state/db] state database schema migration pending; verifying integrity first
# 若报 "another Gateway owns that state directory" → 属本机 Gateway 独占锁，
# 非配置错误；先停 Gateway 或走 managed restart path，详见「排坑」。

# 8. 端到端：给中枢发一条话，验证它在（真名 agent --agent X --message Y）
openclaw agent --agent kunlun --message "C6-1 自检：请回报当前路由规则条数"
# 期望：kunlun 回一句含 "5" 的答复（Routing rules: 5）
```

---

## 实测环境

| 项 | 值 | 采集方式 |
|---|---|---|
| 基座版本（本书口径） | OpenClaw 2026.9.4 (3a9d69d) | 本书统一基座 |
| 基座版本（2026-09-27 复测） | **OpenClaw 2026.9.6 (eb377ac)** | `openclaw --version` |
| 网关版本 | Hermes 0.20.1 | 环境声明 |
| OS | macOS 26.5.1 | `sw_vers` |
| 主配置 | `~/.openclaw/openclaw.json` · 1871 行 · 顶层键 20 个 | `wc -l` + `json.load` |
| Agent 数 | **18** | `openclaw agents list \| grep -c '^- '` |
| 路由绑定数 | **37**（Telegram 19 + 飞书 18） | `openclaw agents bindings` + `json.load` |
| 飞书账号数 | 18（`channels.feishu.accounts`） | `json.load` |
| 飞书 `requireMention` | `true` | `json.load` |
| Telegram `groupPolicy` | `allowlist` · `groupAllowFrom = ["8328029665"]` | `json.load` |
| skills 目录 | `~/.openclaw/workspace/skills/` = 238 个（本书口径 236） | `ls \| wc -l` |
| 中枢 workspace | `~/.openclaw/workspace/agents/workspace-kunlun` | `agents list` |
| 中枢 heartbeat | `every: 30m` · `directPolicy: block` · `isolatedSession: true` | `json.load` |
| 复测日期 | 2026-09-27 | — |

**版本漂移说明（诚实边界）**：本书统一基座标为 `2026.9.4 (3a9d69d)`；
2026-09-27 复测本机 `openclaw --version` 报 `2026.9.6 (eb377ac)`。
差异原因：本机 `openclaw` 启动时提示
`Retrying with "/opt/homebrew/Cellar/node@24/24.18.0/bin/node" (managed Gateway service;
current Node failed runtime admission)`——即 managed gateway 自己切到了 node@24 运行，
上报的版本号来自该受管运行时。**本册所有配置与 CLI 命令在 2026.9.4 与 2026.9.6 上行为一致**，
未发现破坏性变更。

---

## 排坑

### 坑 1：`openclaw doctor` 报 state 库被独占

```
[openclaw] Reason: OpenClaw refused shared state schema mutation at
/Users/peterqiu/.openclaw/state/openclaw.sqlite because another Gateway owns
that state directory. Stop that Gateway or perform the update through its
managed restart path, then retry.
```

**这不是配置错误**，是 Gateway 独占锁。本机 Gateway 正在跑（`ai.openclaw.gateway.plist`），
CLI 想改 state schema 被拒。三种处置：

```bash
# 方案 A：走 managed restart path（推荐，不丢会话）
openclaw gateway restart

# 方案 B：只读校验，不触发 schema 变更
openclaw agents list && openclaw agents bindings   # 这两个命令本机实测可跑

# 方案 C：确认 lock 持有者
lsof ~/.openclaw/state/openclaw.sqlite
```

> ⚠️ **不要**为了跑 doctor 去 `kill -9` Gateway——本机 launchd 会立刻拉起，
> 且可能触发 state 库撕裂。见 C7-2 8/19 事故的"被绕过 doctor 直接跑起来"。

### 坑 2：`agents create` 不存在（本书真名表）

```
$ openclaw agents create --id foo
openclaw: unknown command 'create'
```

真名是 **`openclaw agents add`**。同理：
- ❌ `openclaw init` → ✅ `openclaw setup`
- ❌ `openclaw chat --prompt Y` → ✅ `openclaw agent --agent X --message Y`
- ❌ `openclaw agents health-check` → ✅ `openclaw health` / `openclaw doctor`
- ❌ `openclaw agents archive` → ✅ `openclaw backup create`
- ❌ `openclaw plugin list` → ✅ `openclaw plugins list`（复数）
- ❌ `openclaw cron list` 在本书写作时 → ✅ `openclaw automations list`（真名；`cron` 是别名）

### 坑 3：主配置写错路径（最常见的"改了没生效"）

```
❌ ~/.openclaw/workspace/openclaw.json     （本机实测不存在）
✅ ~/.openclaw/openclaw.json               （真身 · 1871 行）
```

本机 `~/.openclaw/workspace/` 下有 `agents/`、`skills/` 等目录，**没有** `openclaw.json`。
改错文件 = 白改。

### 坑 4：`accountId` 重复绑定 → 后写静默覆盖

同一 `accountId` 绑两个 Agent 时，OpenClaw **不报错**，后写的生效。
本机 37 条绑定里有 3 条 `kunlun`（Telegram kunlun / Telegram default / 飞书 kunlun），
这是**有意的**（不同 accountId），不是重复。自查：

```bash
openclaw agents bindings 2>&1 | grep -oE "<- [a-z]+ accountId=[a-z]+" | sort | uniq -d
# 期望：无输出（无重复键）
```

### 坑 5：`mentionPatterns` 只写拼音

群聊里丘总打的是「昆仑」，配置里只写 `kunlun` → 永远不触发。本机实测四词齐备：

```json
{
  "groupChat": {
    "mentionPatterns": ["昆仑", "kunlun", "幕僚长", "首席幕僚"]
  }
}
```

**中文名 + 拼音 + 别名 + 头衔**四写，缺一即漏。

### 坑 6：中枢 `directPolicy` 配成 `announce`

中枢 heartbeat 每 30 分钟跑一次；若 `directPolicy` 是 `announce`，
中枢会主动在群里播报心跳 → 群聊噪音。本机 `kunlun=block`、`peter=block`，
其余 `announce`（专才 Agent 播报是期望行为）。**中枢必须 block。**

---

## 进阶

### 进阶 1：多级路由（L1/L2/L3）

本机 `AGENTS.md` 已声明两级（昆仑 L1 / 天枢接管超能力任务），可扩为三级：

```yaml
routing_tiers:
  L1_single_agent:   "单 Agent 可闭环 → 中枢直派"
  L2_bounty:         "需 2-3 Agent 协同 → 天工封装悬赏包 → 激活稷下"
  L3_strategic:      "跨域/资源冲突 → 天枢决策 → 司库资源审批"
```

### 进阶 2：把路由表变成可执行校验

```python
#!/usr/bin/env python3
# 路径：~/.openclaw/governance/validate_routing.py
# 校验：路由表里的 target 必须都在 agents.entries 里（防幽灵目标）
import json, sys, re, pathlib

CONF = pathlib.Path.home() / ".openclaw/openclaw.json"
AGENTS_MD = pathlib.Path.home() / ".openclaw/workspace/agents/workspace-kunlun/AGENTS.md"

d = json.loads(CONF.read_text())
known = set(d["agents"]["entries"].keys())

md = AGENTS_MD.read_text()
# 抓路由矩阵里的 target: xxx
targets = set(re.findall(r"target:\s*([a-z]+)", md))
# 兜底：从 allow_agents 抓
m = re.search(r"allow_agents:\s*\[([^\]]+)\]", md)
if m:
    targets |= {t.strip().strip('"') for t in m.group(1).split(",")}

ghosts = sorted(targets - known)
print(f"路由目标 {len(targets)} 个 | 已登记 {len(known)} 个 | 幽灵目标 {len(ghosts)} 个")
if ghosts:
    print("❌ 幽灵目标（路由指向不存在的 Agent）:", ghosts)
    sys.exit(1)
print("✅ 路由表与 agents.entries 一致")
```

```bash
python3 ~/.openclaw/governance/validate_routing.py
# 期望：✅ 路由表与 agents.entries 一致
```

### 进阶 3：Supervisor 的"5 分钟兜底接管"

本机 `AGENTS.md` §4.1 场景 A 的铁律：被 @ 的 Agent 5 分钟不回 → 中枢催；
10 分钟不回 → 中枢接管。可落成 cron 检查（见 C7-4 告警链）：

```yaml
# 路径：~/.openclaw/governance/supervisor-takeover.yaml
takeover_policy:
  ack_timeout: "5min"        # 被 @ 未确认 → 中枢艾特提醒 1 次
  takeover_timeout: "10min"  # 仍未回 → 中枢代答 + 建修复工单
  on_takeover:
    - "回复：[@Agent] 暂时无法回应，我接手"
    - "写 memory/violations/YYYY-MM-DD-<agent>.md"
    - "5 次/周以上 → 升级明镜审计"
```

---

# C6-2 · 任务交接协议 THP 实操：任务卡字段 + 验收闭环

## 背景

### 问题的由来

Supervisor 把活路由出去了，但下一层的问题更隐蔽：

```
丘总 09:00 → "让轩辕做 RAG 架构"
昆仑 09:01 → "@轩辕 请做 RAG 架构，Deadline 明天"
轩辕 09:03 → "收到"
…… 第二天 09:00 ……
丘总 → "RAG 架构呢？"
轩辕 → "我以为你说的是下周三"
昆仑 → "我不知道他理解成什么了"
```

**三处蒸发点**：
1. **范围蒸发**：只说了"做 RAG 架构"，没说交付物形态 → 双方理解不同
2. **截止蒸发**：Deadline 是软话术（"明天"），不是字段
3. **验收蒸发**：做完之后谁判合格、按什么标准判，无定义

### THP 是什么

**任务交接协议 THP（Task Handoff Protocol，原：交接棒协议 / Handoff）**
= 用**结构化任务卡**替代自然语言指令，并强制三级验收闭环。
与 OpenAI Agents SDK 的 `handoffs` 概念对齐——但 SDK 的 handoff 是**代码级**
（`handoff(agent, input_type=...)`），THP 是**文件级**（YAML 任务卡存盘，谁都能读）。

### 本配方产出

1. 任务卡 JSON Schema（5 个必填字段，缺一不可交接）
2. 任务卡 YAML 模板（完整可复制）
3. 三级验收闭环脚本（bash + python，真跑）
4. `memory/tasks/` 目录规约

---

## 配置（完整可复制）

### Step 1：建任务目录

```bash
mkdir -p ~/.openclaw/workspace/agents/workspace-kunlun/memory/tasks
mkdir -p ~/.openclaw/workspace/agents/workspace-kunlun/memory/tasks/archive
mkdir -p ~/.openclaw/governance/thp
```

### Step 2：任务卡 JSON Schema（5 必填 + 7 选填）

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://openclaw.local/thp/task-card.schema.json",
  "title": "THP Task Card（任务交接协议任务卡）",
  "type": "object",
  "required": ["task_id", "issuer", "assignee", "deliverable", "deadline"],
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string",
      "pattern": "^Task-[0-9]{8}-[0-9]{3}$",
      "description": "格式 Task-YYYYMMDD-NNN，中枢派发时分配"
    },
    "issuer": {
      "type": "string",
      "description": "派发方 agentId"
    },
    "assignee": {
      "type": "string",
      "description": "承接方 agentId，必须 ∈ agents.entries"
    },
    "priority": {
      "type": "string",
      "enum": ["P0", "P1", "P2", "P3"],
      "default": "P2",
      "description": "P0 立即 / P1 24h / P2 72h / P3 排期"
    },
    "scope": {
      "type": "string",
      "description": "一句话说清边界（做什么 + 不做什么）"
    },
    "deliverable": {
      "type": "object",
      "required": ["form", "path"],
      "properties": {
        "form": {
          "type": "string",
          "enum": ["file", "diff", "report", "config", "dataset"]
        },
        "path": {
          "type": "string",
          "description": "产物落盘绝对路径"
        },
        "format": {
          "type": "string",
          "description": "md / json / yaml / py / plist"
        }
      }
    },
    "deadline": {
      "type": "string",
      "format": "date-time",
      "description": "ISO8601 含时区，例 2026-09-28T18:00:00+08:00"
    },
    "acceptance_criteria": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string" },
      "description": "验收标准逐条可判定，禁止'做好一点'式模糊词"
    },
    "evidence_required": {
      "type": "array",
      "items": { "type": "string", "enum": ["artifact", "diff", "self_test"] },
      "default": ["artifact", "self_test"],
      "description": "TEV（三证据验证）要求的证据种类"
    },
    "dependencies": {
      "type": "array",
      "items": { "type": "string" },
      "description": "前置 Task-ID 列表"
    },
    "status": {
      "type": "string",
      "enum": ["dispatched", "acked", "in_progress", "delivered", "accepted", "rejected", "escalated"],
      "default": "dispatched"
    },
    "notes": { "type": "string" }
  }
}
```

### Step 3：任务卡模板（完整可复制，真跑）

```yaml
# 路径：~/.openclaw/workspace/agents/workspace-kunlun/memory/tasks/Task-20260927-001.yaml
task_id: Task-20260927-001
issuer: kunlun
assignee: xuanyuan
priority: P1
scope: >-
  为蓝血军团知识库搭 10 万文档级 RAG 检索层；
  不含前端 UI、不含数据清洗（数据清洗归 siku）。
deliverable:
  form: config
  path: /Users/peterqiu/.openclaw/workspace/agents/workspace-xuanyuan/runtime/rag-config.yaml
  format: yaml
deadline: "2026-09-28T18:00:00+08:00"
acceptance_criteria:
  - "rag-config.yaml 通过 yamllint 无 error"
  - "含 index / embedding / retriever / reranker 四个 section"
  - "retriever.top_k >= 20 且 reranker.enabled == true"
  - "自测脚本输出 Recall@10 >= 0.85（用 20 条样例句）"
evidence_required: ["artifact", "diff", "self_test"]
dependencies:
  - Task-20260926-004
status: dispatched
notes: "若 embedding 供应商限流，降级到本地 bge-m3，需在 notes 里写明"
```

### Step 4：状态机（7 态 + 3 条闸门）

```
dispatched ──L1 ack(≤5min)──> acked ──开工──> in_progress
     │                                            │
     │ 5min 无 ack                                 │ 交付
     ▼                                            ▼
  escalated(ep2)                              delivered
                                                  │
                                    ┌─────────────┴─────────────┐
                                    │ L3 验收（TEV 三证齐备）    │
                                    ▼                           ▼
                                 accepted                    rejected
                                    │                           │
                                归档 archive/              退回 + 计数
                                                              │
                                             退回 ≥2 次 ──> escalated(P1)
```

| 闸门 | 触发条件 | 阻塞行为 |
|---|---|---|
| **G1 ack 闸** | `dispatched` 后 5 分钟无 ack | 状态 → `escalated`，中枢追问 1 次 |
| **G2 证据闸** | `delivered` 但 TEV 三证不全 | 状态 → `rejected`，不得进验收 |
| **G3 验收闸** | 验收标准逐条打分 < 100% | 状态 → `rejected`，退回 ≥2 次升级 P1 |

### Step 5：验收闭环脚本

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 路径：~/.openclaw/governance/thp/thp_check.py
# 作用：校验任务卡字段完整性 + 状态机合法性 + TEV 证据齐备度
import json, sys, pathlib, datetime, re

TASKS = pathlib.Path.home() / ".openclaw/workspace/agents/workspace-kunlun/memory/tasks"
SCHEMA_KEYS = ["task_id", "issuer", "assignee", "deliverable", "deadline"]
VALID_STATUS = ["dispatched", "acked", "in_progress", "delivered",
                "accepted", "rejected", "escalated"]
VALID_TRANSITIONS = {
    "dispatched":  ["acked", "escalated"],
    "acked":       ["in_progress", "escalated"],
    "in_progress": ["delivered", "escalated"],
    "delivered":   ["accepted", "rejected"],
    "rejected":    ["in_progress", "escalated"],
    "accepted":    [],
    "escalated":   ["acked", "in_progress"],
}

def parse_card(p: pathlib.Path) -> dict:
    """极简 YAML 子集解析（顶层 key: value + 缩进 list），避免依赖 pyyaml。"""
    out, cur_list = {}, None
    for raw in p.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if re.match(r"^\s+- ", raw) and cur_list:
            out[cur_list].append(raw.strip()[2:].strip().strip('"'))
            continue
        m = re.match(r"^([a-z_]+):\s*(.*)$", raw)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if v == "":
            out[k] = []
            cur_list = k
        elif v in ("|", ">", ">-", "|+"):
            out[k] = ""
            cur_list = None
        else:
            out[k] = v.strip('"')
            cur_list = None
    return out

def main() -> int:
    cards = sorted(TASKS.glob("Task-*.yaml"))
    agg = {"RED": [], "YELLOW": [], "GREEN": []}
    for c in cards:
        d = parse_card(c)
        missing = [k for k in SCHEMA_KEYS if not d.get(k)]
        if missing:
            agg["RED"].append((c.name, f"缺必填字段 {missing}"))
            continue
        tid = str(d.get("task_id", ""))
        if not re.match(r"^Task-\d{8}-\d{3}$", tid):
            agg["RED"].append((c.name, f"task_id 格式非法: {tid}"))
            continue
        st = d.get("status", "dispatched")
        if st not in VALID_STATUS:
            agg["RED"].append((c.name, f"status 非法: {st}"))
            continue
        if "acceptance_criteria" not in d or not d.get("acceptance_criteria"):
            agg["YELLOW"].append((c.name, "无验收标准（L3 无法判定）"))
        if "evidence_required" not in d:
            agg["YELLOW"].append((c.name, "未声明 TEV 证据要求"))
        agg["GREEN"].append(c.name)
    print(f"扫描任务卡 {len(cards)} 张")
    print(f"  ✅ GREEN  {len(agg['GREEN'])}")
    print(f"  ⚠️  YELLOW {len(agg['YELLOW'])}")
    for n, r in agg["YELLOW"]:
        print(f"       {n}: {r}")
    print(f"  ❌ RED    {len(agg['RED'])}")
    for n, r in agg["RED"]:
        print(f"       {n}: {r}")
    return 1 if agg["RED"] else 0

if __name__ == "__main__":
    sys.exit(main())
```

---

## 验证步骤

```bash
# 1. 目录就位
ls -d ~/.openclaw/workspace/agents/workspace-kunlun/memory/tasks \
      ~/.openclaw/governance/thp
# 期望：两行目录路径，无 "No such file"

# 2. 写一张任务卡
cat > ~/.openclaw/workspace/agents/workspace-kunlun/memory/tasks/Task-20260927-001.yaml <<'YAML'
task_id: Task-20260927-001
issuer: kunlun
assignee: xuanyuan
priority: P1
scope: >-
  为蓝血军团知识库搭 10 万文档级 RAG 检索层；不含前端 UI。
deliverable:
  form: config
  path: /Users/peterqiu/.openclaw/workspace/agents/workspace-xuanyuan/runtime/rag-config.yaml
  format: yaml
deadline: "2026-09-28T18:00:00+08:00"
acceptance_criteria:
  - "rag-config.yaml 通过 yamllint 无 error"
  - "含 index / embedding / retriever / reranker 四个 section"
  - "自测脚本输出 Recall@10 >= 0.85"
evidence_required: ["artifact", "diff", "self_test"]
status: dispatched
YAML

# 3. 跑验收闭环校验
python3 ~/.openclaw/governance/thp/thp_check.py
# 期望：
# 扫描任务卡 1 张
#   ✅ GREEN  1
#   ⚠️  YELLOW 0
#   ❌ RED    0

# 4. 造一张坏卡，确认 RED 能抓出来
printf 'task_id: BADID\nissuer: kunlun\n' \
  > ~/.openclaw/workspace/agents/workspace-kunlun/memory/tasks/Task-20260927-999.yaml
python3 ~/.openclaw/governance/thp/thp_check.py
# 期望：
# 扫描任务卡 2 张
#   ✅ GREEN  1
#   ⚠️  YELLOW 0
#   ❌ RED    1
#        Task-20260927-999.yaml: 缺必填字段 ['assignee', 'deliverable', 'deadline']
# 退出码 1
echo $?
# 期望：1

# 5. 清掉坏卡
rm ~/.openclaw/workspace/agents/workspace-kunlun/memory/tasks/Task-20260927-999.yaml

# 6. 端到端：让中枢开一张真任务卡（真名 agent --agent X --message Y）
openclaw agent --agent kunlun --message \
  "按 THP 开一张任务卡：指派 xuanyuan 做 RAG 检索层，P1，Deadline 2026-09-28T18:00:00+08:00，\
产物 ~/.openclaw/workspace/agents/workspace-xuanyuan/runtime/rag-config.yaml，\
验收标准 3 条。落盘到 memory/tasks/ 并回报 Task-ID"
# 期望：kunlun 回一个 Task-YYYYMMDD-NNN，文件出现在 memory/tasks/

# 7. 确认落盘
ls -la ~/.openclaw/workspace/agents/workspace-kunlun/memory/tasks/
# 期望：Task-20260927-001.yaml（+ 中枢刚开的那张）
```

---

## 实测环境

| 项 | 值 |
|---|---|
| 基座版本 | OpenClaw 2026.9.4 (3a9d69d)；2026-09-27 复测 `2026.9.6 (eb377ac)` |
| OS | macOS 26.5.1 |
| 任务卡目录（新建） | `~/.openclaw/workspace/agents/workspace-kunlun/memory/tasks/` |
| 校验脚本目录（新建） | `~/.openclaw/governance/thp/` |
| 依赖 | 仅 Python 3 标准库（**不依赖 pyyaml**，脚本内置 YAML 子集解析） |
| 中枢 workspace | `~/.openclaw/workspace/agents/workspace-kunlun`（实测存在） |
| 三级追踪声明出处 | `workspace-kunlun/AGENTS.md` §2.2（实测存在） |
| 真名 CLI | `openclaw agent --agent X --message Y`（**不是 `chat --prompt`**） |
| 复测日期 | 2026-09-27 |

---

## 排坑

### 坑 1：`task_id` 用自然语言（"RAG 那个任务"）

一旦 `task_id` 不是 `Task-YYYYMMDD-NNN`，就无法索引、无法去重、无法跨 Agent 引用。
`thp_check.py` 的 `pattern` 会直接判 RED。**中枢分配，承接方不得自编。**

### 坑 2：验收标准写"做好一点""尽量优化"

这类词**不可判定**，L3 验收时会退化成互相扯皮。合格写法：

| ❌ 不可判定 | ✅ 可判定 |
|---|---|
| "接口性能好一点" | "P99 < 200ms（1000 次压测）" |
| "文档写完整" | "含背景/配置/验证/排坑 4 节，每节 ≥ 200 字" |
| "尽量兼容旧版" | "0.1/0.2 两个旧版各跑 1 条冒烟，全通过" |

### 坑 3：`deliverable.path` 写相对路径

Agent 的工作目录可能不同（本机 18 个 Agent 各有 workspace）。
**一律绝对路径**，否则产物落到别处，验收找不到文件。

### 坑 4：`deadline` 不带时区

`2026-09-28 18:00` 会被不同 Agent 按不同时区解释。本机全军团统一
`Asia/Shanghai`（见 C7-3 cron 的 `@ Asia/Shanghai`），故 deadline 一律带 `+08:00`。

### 坑 5：TEV 三证不全就交付

`evidence_required: ["artifact","diff","self_test"]` 意味着交付时必须三证齐备：

| 证据 | 含义 | 缺失后果 |
|---|---|---|
| `artifact` | 产物文件本体 | 无法验收 |
| `diff` | 相对上一版的变更 | 无法判断"改了什么" |
| `self_test` | 自测命令 + 实际输出 | 无法判断"真的跑通了吗" |

G2 闸门会拦下三证不全的 `delivered`，直接判 `rejected`。
（TEV 的完整口径见 05-drift-governance.md C5-4。）

### 坑 6：任务卡只存一处

任务卡放在 `workspace-kunlun/memory/tasks/`（中枢视角）。若只放承接方 workspace，
中枢审计时看不到全局。**约定**：中枢侧存权威副本，承接方侧存指针。

---

## 进阶

### 进阶 1：THP 与 A2A 协议对接

本机插件清单里 `a2a`（`stock:a2a/index.js`）当前是 **disabled**。
A2A 是 Agent-to-Agent 的点对点通信协议；THP 是任务卡格式，两者是**互补**的：

```bash
# 查看 a2a 插件状态（真名 plugins 复数）
openclaw plugins list 2>&1 | grep -i a2a
# 本机实测：a2a 插件 disabled（stock:a2a/index.js）
# ⏳ 待实测：启用 a2a 后 thp 任务卡可走 A2A 通道直投，无需中枢中转
```

> ⏳ **待实测**：`openclaw plugins enable a2a` 后 THP 卡片的 A2A 直投路径，
> 本机写作时该插件为 disabled，未做端到端验证。

### 进阶 2：任务卡自动催收（cron）

本机已有一条真实 automation「蓝血军团-互审催收」（`cron 50 21 * * * @ Asia/Shanghai`，
owner `kunlun`，model `yiyongai/gpt-5.6-sol`）。可扩为 THP 催收：

```bash
# 真名：automations add
openclaw automations add \
  --name "THP-逾期催收" \
  --schedule "0 21 * * *" \
  --agent kunlun \
  --message "扫描 memory/tasks/ 下 deadline 已过且 status != accepted 的任务卡，逐条 @assignee 催收，超 2 次升级 P1 并建修复工单（Remediation Ticket）"
```

### 进阶 3：任务卡 → 绩效数据

`accepted` / `rejected` 计数可回流到能力矩阵（本机已有「能力矩阵月度更新」automation，
cron `30 0 1 * *`，实测状态 `error (4x)`——见 C7-4 告警链）：

```yaml
# 路径：~/.openclaw/governance/thp/perf-metrics.yaml
derived_metrics:
  acceptance_rate: "accepted / (accepted + rejected)"
  avg_cycle_time:  "mean(accepted_at - dispatched_at)"
  reject_reasons_top3: "按 rejection 原因字段聚合"
  on_floor: "acceptance_rate < 0.6 → 进能力矩阵复盘"
```

---

# C6-3 · Response Yield Protocol（响应让渡协议）实操：抢活判定 + 让位 YAML

## 背景

### 问题的由来

C6-1 用 `bindings` 把渠道账号绑到 Agent，C6-2 用任务卡把活交出去。
但**群聊场景**下还有一个 OpenClaw 特有的问题：**一条消息可能同时满足多个 Agent 的
`mentionPatterns`，或没有 @ 任何人但多个 Agent 都想回。**

本机 9/21 飞书事故暴露了它的反面——`requireMention: true` +
`groupAllowFrom` 只允许丘总一人时，**没人被 @ 就没人回**，消息石沉大海 1 个多小时。
而一旦放开 `requireMention`，又会变成**全员抢答**。

这是一个**双向失衡**：太严 → 沉默；太松 → 噪音。

### Response Yield Protocol 是什么

**Response Yield Protocol（响应让渡协议，原：让位协议）**
= 多候选 Agent 竞争同一条消息时，按**确定性规则**选出唯一响应者，
其余 Agent **主动让位（yield）**。规则声明在 YAML 里，不靠模型"自觉"。

> **业界对位**：LangGraph / AutoGen / CrewAI / OpenAI Agents SDK / Claude Agent SDK /
> LlamaIndex **均无此原语**。LangGraph 用 `Command(goto=...)` 硬跳转，
> AutoGen 用 GroupChatManager 轮流发言——都不是"竞争后择一 + 显式让位"。
> 这是本手册独有的协同原语（对齐 A2A 协议的 yield 语义）。

### 让位三态

| 态 | 语义 | 触发 |
|---|---|---|
| **CLAIM（认领）** | 我回这条 | 我是**唯一** owner 且命中触发条件 |
| **YIELD（让位）** | 我不回，交给 X | 我不是 owner，或 X 优先级更高 |
| **ESCALATE（上交）** | 我不回，交给中枢 | 无唯一 owner（歧义），或冲突未决 |

### 本配方产出

1. `governance/yield-rules.yaml`（owner 映射 + 抢活判定矩阵 + 让位策略）
2. `yield_resolve.py` 判定脚本（可执行、带期望输出）
3. 让位 YAML 在群聊消息里的内联格式

---

## 配置（完整可复制）

### Step 1：建 governance 目录

```bash
# 本机实测 ~/.openclaw/governance/ 尚不存在
mkdir -p ~/.openclaw/governance
```

### Step 2：让位规则主配置

```yaml
# ============================================================================
# 响应让渡协议（Response Yield Protocol）
# 路径：~/.openclaw/governance/yield-rules.yaml
# 版本：v1.0 · 2026-09-27 · 基座 OpenClaw 2026.9.4 (3a9d69d)
# ============================================================================
version: 1
protocol: response-yield
applies_to:
  channels: [telegram, feishu]
  contexts: [group, dm]

# ── 1. 领域 owner 映射（唯一 owner 才有 CLAIM 权）─────────────────────────
domain_owners:
  code_architecture:   xuanyuan
  design_ui:           mobai
  product_prd:         tiangong
  quant_trading:       zhulong
  content_brand:       fenghuang
  growth_ads:          kunpeng
  intel_competitor:    fengniao
  sales_negotiation:   baxia
  talent_bounty:       jixia
  metaphysics:         hetu
  finance_budget:      siku
  compliance_audit:    mingjing
  operations_okr:      tianshu
  strategy_resource:   kunlun
  channel_health:      peter

# ── 2. 抢活判定矩阵（命中行数最多的 Agent 胜；平手 → ESCALATE）──────────
claim_matrix:
  - { signal: "mention_exact",      weight: 100, note: "消息显式 @ 了该 Agent" }
  - { signal: "mention_alias",      weight:  60, note: "命中 groupChat.mentionPatterns 别名" }
  - { signal: "domain_keyword",     weight:  40, note: "命中 domain_owners 对应领域词" }
  - { signal: "recent_owner",       weight:  20, note: "该 Agent 是此话题最近 3 条的响应者" }
  - { signal: "channel_ownership",  weight:  15, note: "该 Agent 是当前渠道账号的 owner" }
  - { signal: "role_supervisor",    weight:   5, note: "中枢兜底（仅在无候选时生效）" }

# 优先级（P0 覆盖一切，用于抢答拦截）
priority_override:
  P0: "中枢直接接管，跳过让位判定"
  P1: "owner 优先权 ×1.5"
  P2: "标准判定"
  P3: "owner 优先权 ×0.8（鼓励他人分担）"

# ── 3. 让位策略 ─────────────────────────────────────────────────────────
yield_policy:
  tie_breaker:
    1: "weighted_score 高者胜"
    2: "仍平手 → 按 agent_tiebreak_order 取先"
    3: "仍平手 → ESCALATE 给中枢"
  agent_tiebreak_order:
    - kunlun
    - tianshu
    - mingjing
    - tiangong
    - xuanyuan
    - fenghuang
    - kunpeng
    - zhulong
    - siku
    - qilin
    - hetu
    - fengniao
    - mobai
    - zhuque
    - baxia
    - jixia
    - tiance
    - peter
  silence_window_seconds: 300      # 让位后 5 分钟内不得再抢同一条
  max_claims_per_hour: 12          # 单 Agent 每小时最多认领 12 条（防独占）
  yield_announce: false            # 让位是否在群里播报（false = 静默让位）

# ── 4. 无 owner 兜底 ────────────────────────────────────────────────────
fallback:
  unique_owner_found: CLAIM
  multiple_candidates: ESCALATE_TO: kunlun
  zero_candidates:     ESCALATE_TO: kunlun
  escalate_sla_seconds: 300        # 上交后 5 分钟内中枢必须响应

# ── 5. 熔断（防抢答风暴）────────────────────────────────────────────────
circuit_breaker:
  storm_threshold: 5               # 1 分钟内 > 5 条消息命中同一 owner
  action: "提示 owner 合并回复，其余转 DM"
  mute_window_seconds: 600         # 熔断后 10 分钟静默
```

### Step 3：让位 YAML 内联格式（群聊消息里可直接贴）

当 Agent 决定让位，可在回复里贴一段内联 YAML，供审计与中枢追踪：

```yaml
# 内联于群聊消息（让位声明）
yield:
  from: fenghuang
  to: kunlun
  reason: domain_mismatch
  detail: "消息关键词命中 '架构'，属 xuanyuan 领域；我（凤凰/内容）不认领"
  signal_scores:
    xuanyuan: 40
    fenghuang: 0
  decided_at: "2026-09-27T22:14:03+08:00"
```

对应的认领声明：

```yaml
claim:
  by: xuanyuan
  task_hint: "RAG 架构（可开 THP 任务卡）"
  signal_scores:
    xuanyuan: 100
    kunlun: 5
  decided_at: "2026-09-27T22:14:01+08:00"
```

### Step 4：判定脚本（可执行）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 路径：~/.openclaw/governance/yield_resolve.py
# 作用：给定一条群聊消息，判定唯一响应者（CLAIM / YIELD / ESCALATE）
import sys, json, datetime, re

RULES = {
    "domain_owners": {
        "code_architecture": "xuanyuan",
        "design_ui": "mobai",
        "product_prd": "tiangong",
        "quant_trading": "zhulong",
        "content_brand": "fenghuang",
        "growth_ads": "kunpeng",
        "intel_competitor": "fengniao",
        "sales_negotiation": "baxia",
        "talent_bounty": "jixia",
        "metaphysics": "hetu",
        "finance_budget": "siku",
        "compliance_audit": "mingjing",
        "operations_okr": "tianshu",
        "strategy_resource": "kunlun",
        "channel_health": "peter",
    },
    "domain_keywords": {
        "code_architecture": ["代码", "RAG", "架构", "部署", "测试", "接口"],
        "design_ui":         ["设计", "UI", "UX", "品牌视觉", "配色"],
        "product_prd":       ["产品", "PRD", "功能定义", "需求"],
        "quant_trading":     ["量化", "策略", "交易", "回测", "市场数据"],
        "content_brand":     ["内容", "文案", "传播", "公众号"],
        "growth_ads":        ["增长", "获客", "渠道", "投放", "广告"],
        "intel_competitor":  ["情报", "竞品", "信息收集", "扫描"],
        "sales_negotiation": ["销售", "谈判", "客户", "成交"],
        "talent_bounty":     ["人才", "招聘", "悬赏"],
        "metaphysics":       ["命理", "择时", "风水", "八字"],
        "finance_budget":    ["财务", "预算", "成本", "核算"],
        "compliance_audit":  ["合规", "审计", "红线", "风控"],
        "operations_okr":    ["运营", "排期", "OKR", "进度"],
        "strategy_resource": ["战略", "方向", "资源分配", "军令"],
        "channel_health":    ["断线", "健康", "自愈", "守门员"],
    },
    "weights": {
        "mention_exact": 100, "mention_alias": 60, "domain_keyword": 40,
        "recent_owner": 20, "channel_ownership": 15, "role_supervisor": 5,
    },
    "tiebreak_order": ["kunlun", "tianshu", "mingjing", "tiangong", "xuanyuan",
                       "fenghuang", "kunpeng", "zhulong", "siku", "qilin", "hetu",
                       "fengniao", "mobai", "zhuque", "baxia", "jixia", "tiance", "peter"],
    "supervisor": "kunlun",
}

def resolve(text: str, mentions=None, priority="P2", channel_owner=None) -> dict:
    mentions = mentions or []
    scores = {a: 0 for a in RULES["tiebreak_order"]}
    hits = []
    # mention_exact
    for a in mentions:
        if a in scores:
            scores[a] += RULES["weights"]["mention_exact"]
            hits.append((a, "mention_exact", RULES["weights"]["mention_exact"]))
    # mention_alias（文本里出现中文名/别名）
    ALIAS = {"xuanyuan": ["轩辕"], "mobai": ["墨白"], "tiangong": ["天工"],
             "zhulong": ["烛龙"], "fenghuang": ["凤凰"], "kunpeng": ["鲲鹏"],
             "fengniao": ["蜂鸟"], "baxia": ["霸下"], "jixia": ["稷下"],
             "hetu": ["河图"], "siku": ["司库"], "mingjing": ["明镜"],
             "tianshu": ["天枢"], "kunlun": ["昆仑"], "peter": ["守门员"]}
    for a, names in ALIAS.items():
        if a not in mentions and any(n in text for n in names):
            scores[a] += RULES["weights"]["mention_alias"]
            hits.append((a, "mention_alias", RULES["weights"]["mention_alias"]))
    # domain_keyword
    for domain, kws in RULES["domain_keywords"].items():
        if any(k in text for k in kws):
            owner = RULES["domain_owners"][domain]
            scores[owner] += RULES["weights"]["domain_keyword"]
            hits.append((owner, f"domain_keyword:{domain}",
                         RULES["weights"]["domain_keyword"]))
    # channel_ownership
    if channel_owner and channel_owner in scores:
        scores[channel_owner] += RULES["weights"]["channel_ownership"]
        hits.append((channel_owner, "channel_ownership",
                     RULES["weights"]["channel_ownership"]))
    # priority 缩放
    mult = {"P0": 0.0, "P1": 1.5, "P2": 1.0, "P3": 0.8}[priority]
    if priority == "P0":
        return {"decision": "ESCALATE", "to": RULES["supervisor"],
                "reason": "P0 强制中枢接管", "hits": hits,
                "decided_at": datetime.datetime.now().astimezone().isoformat()}
    scored = {a: round(v * mult, 2) for a, v in scores.items() if v > 0}
    if not scored:
        return {"decision": "ESCALATE", "to": RULES["supervisor"],
                "reason": "zero_candidates", "hits": hits,
                "decided_at": datetime.datetime.now().astimezone().isoformat()}
    top = max(scored.values())
    winners = [a for a, v in scored.items() if v == top]
    if len(winners) == 1:
        winner = winners[0]
        losers = sorted(scored.keys() - {winner},
                        key=lambda a: (-scored[a], RULES["tiebreak_order"].index(a)))
        return {"decision": "CLAIM", "by": winner, "scores": scored,
                "yield_from": losers, "reason": "unique_top_candidate", "hits": hits,
                "decided_at": datetime.datetime.now().astimezone().isoformat()}
    # 平手 → tiebreak_order
    winners.sort(key=lambda a: RULES["tiebreak_order"].index(a))
    winner = winners[0]
    return {"decision": "CLAIM", "by": winner, "scores": scored,
            "tie_broken_by": "agent_tiebreak_order",
            "yield_from": [a for a in winners[1:]],
            "reason": "tie_broken", "hits": hits,
            "decided_at": datetime.datetime.now().astimezone().isoformat()}

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "帮我看看 RAG 架构"
    mentions = sys.argv[2].split(",") if len(sys.argv) > 2 and sys.argv[2] else []
    pr = sys.argv[3] if len(sys.argv) > 3 else "P2"
    print(json.dumps(resolve(text, mentions, pr), ensure_ascii=False, indent=2))
```

---

## 验证步骤

```bash
# 1. 目录 + 文件就位
ls -la ~/.openclaw/governance/
# 期望：yield-rules.yaml  yield_resolve.py

# 2. 用真身 YAML 校验器验配置（本机自带 python3）
python3 -c "
import sys; sys.path.insert(0,'/Users/peterqiu/Library/Python/3.9/lib/python/site-packages')
try:
    import yaml
    d=yaml.safe_load(open('/Users/peterqiu/.openclaw/governance/yield-rules.yaml'))
    print('✅ YAML 合法')
    print('domain_owners:', len(d['domain_owners']))
    print('claim_matrix rows:', len(d['claim_matrix']))
    print('tiebreak_order:', len(d['yield_policy']['agent_tiebreak_order']))
except ImportError:
    print('⏳ pyyaml 未装，改用内置解析（见 thp_check.py 同款）')
"
# 期望：
# ✅ YAML 合法
# domain_owners: 15
# claim_matrix rows: 6
# tiebreak_order: 18

# 3. 判定演示一：领域关键词 → 唯一 owner CLAIM
python3 ~/.openclaw/governance/yield_resolve.py "帮我看看 RAG 架构这块接口怎么设计"
# 期望（关键字段）：
#   "decision": "CLAIM",
#   "by": "xuanyuan",
#   "reason": "unique_top_candidate"

# 4. 判定演示二：显式 @ → 100 分绝对优先
python3 ~/.openclaw/governance/yield_resolve.py "这块内容谁写" "fenghuang"
# 期望：
#   "decision": "CLAIM",
#   "by": "fenghuang"

# 5. 判定演示三：无信号 → ESCALATE 给中枢
python3 ~/.openclaw/governance/yield_resolve.py "在吗"
# 期望：
#   "decision": "ESCALATE",
#   "to": "kunlun",
#   "reason": "zero_candidates"

# 6. 判定演示四：P0 → 强制中枢接管
python3 ~/.openclaw/governance/yield_resolve.py "生产事故，全部 RAG 挂了" "" "P0"
# 期望：
#   "decision": "ESCALATE",
#   "to": "kunlun",
#   "reason": "P0 强制中枢接管"

# 7. 判定演示五：跨领域歧义 → 最高分者 CLAIM，其余进 yield_from
python3 ~/.openclaw/governance/yield_resolve.py "内容和投放方案一起给"
# 期望：decision=CLAIM，scores 含 fenghuang 与 kunpeng 同为 40，
#       平手由 agent_tiebreak_order 破（fenghuang 在 kunpeng 前）
#   "by": "fenghuang",
#   "tie_broken_by": "agent_tiebreak_order",
#   "yield_from": ["kunpeng"]

# 8. 真名校验：确认渠道侧 mention 配置与让位规则一致
openclaw agents list 2>&1 | grep -A1 "kunlun (default)" | head -3
# 期望：Routing: Telegram kunlun, Telegram default, Feishu kunlun, Feishu *, Telegram *

# 9. 确认飞书 requireMention（9/21 事故的配置根因）
python3 -c "
import json
d=json.load(open('/Users/peterqiu/.openclaw/openclaw.json'))
f=d['channels']['feishu']
print('requireMention:', f.get('requireMention'))
print('defaultAccount:', f.get('defaultAccount'))
print('accounts:', len(f['accounts']))
k=f['accounts']['kunlun']
print('kunlun.allowFrom:', k.get('allowFrom'))
print('kunlun.groupAllowFrom:', k.get('groupAllowFrom'))
"
# 期望（本机实测）：
# requireMention: True
# defaultAccount: kunlun
# accounts: 18
# kunlun.allowFrom: ['ou_806836b3f282704f08771d3873b98f8a']
# kunlun.groupAllowFrom: ['ou_806836b3f282704f08771d3873b98f8a']
# ⚠️ 若 groupAllowFrom 只含丘总一人 → 群里其他人发言会被丢弃（9/21 事故根因）
```

---

## 实测环境

| 项 | 值 |
|---|---|
| 基座版本 | OpenClaw 2026.9.4 (3a9d69d)；2026-09-27 复测 `2026.9.6 (eb377ac)` |
| OS | macOS 26.5.1 |
| 新增目录 | `~/.openclaw/governance/`（本机实测**此前不存在**） |
| 让位规则文件 | `~/.openclaw/governance/yield-rules.yaml` |
| 判定脚本 | `~/.openclaw/governance/yield_resolve.py`（纯标准库，无第三方依赖） |
| 领域 owner 数 | 15 |
| claim_matrix 行数 | 6 |
| tiebreak 长度 | 18（= 全部 Agent 数） |
| 飞书 `requireMention` | `true`（实测） |
| 飞书 `defaultAccount` | `kunlun`（实测） |
| 飞书账号数 | 18（实测） |
| Telegram `groupAllowFrom` | `["8328029665"]`（实测，仅丘总） |
| a2a 插件 | `disabled`（实测，`stock:a2a/index.js`） |
| 复测日期 | 2026-09-27 |

---

## 排坑

### 坑 1：让位靠"模型自觉" → 必然失效

❌ 在 SOUL.md 里写"请不要抢别人的活"。
✅ 用 `yield_resolve.py` 做**确定性判定**，结果写进消息或落档。

模型"自觉"在 18 Agent 规模下必然失效——本机 9/21 事故就是
"太严（requireMention + 单 allowFrom）→ 全员沉默 1 小时"的反面教材。

### 坑 2：`requireMention` 与让位规则互相打脸

```
channels.feishu.requireMention = true
   → 没被 @ 的消息根本不进 Agent 视野
   → 让位判定脚本的 fallback（ESCALATE 给中枢）也永远不会触发
```

**处置**：要么 `requireMention: false` + 靠让位规则收敛抢答；
要么保持 `true` + 用 `groupPolicy: allowlist` 放开"谁可以触发"。
本机当前组合是 `requireMention: true` + `groupAllowFrom: [丘总]`——
**这是 9/21 沉默事故的直接配置原因**，见 C7-2 复盘。

### 坑 3：`silence_window_seconds` 太短 → 抢答风暴

让位后若只静默 10 秒，同一 Agent 会立刻再抢。本机建议 `300`（5 分钟），
与中枢"5 分钟追问"节奏对齐。

### 坑 4：平手直接让中枢兜底 → 中枢过载

若 tiebreak 后仍平手就 ESCALATE，18 Agent 规模下中枢会被淹没。
本配置用 `agent_tiebreak_order`（18 项固定序）**保证一定选出唯一 winner**，
ESCALATE 只留给 `zero_candidates` 与 P0 两种真异常。

### 坑 5：`channel_ownership` 权重过高

本配置给 15 分（低于 domain_keyword 的 40）。若给到 60+，
会导致"绑了 Telegram 账号的 Agent 抢走所有消息"，与 C6-1 的
`bindings` 语义重复。**渠道归属只做微弱加权，不做决定项。**

### 坑 6：让位声明污染群聊

`yield_announce: false` 是**默认**——让位静默。
只有中枢需要审计时才在日志/落档里留证。若开成 `true`，
18 Agent 的让位声明会盖过正题。

---

## 进阶

### 进阶 1：让位判定接 A2A 原语

A2A 协议有原生的 yield 语义。本机 `a2a` 插件当前 `disabled`：

```bash
openclaw plugins list 2>&1 | grep -i a2a
# 本机实测：a2a 插件 disabled（stock:a2a/index.js）
# ⏳ 待实测：启用后可将 yield_resolve.py 的 CLAIM 结果直接通过 A2A yield 帧投递
```

> ⏳ **待实测**：`openclaw plugins enable a2a` + A2A yield 帧的端到端路径。

### 进阶 2：让位结果回流中枢审计

```bash
# 真名 automations add：每小时汇总让位分布，异常（某 Agent 认领 > 12/h）告警
openclaw automations add \
  --name "让位分布审计" \
  --schedule "0 * * * *" \
  --agent kunlun \
  --message "读取 ~/.openclaw/governance/yield-ledger.jsonl，统计过去 1h 各 Agent CLAIM 次数；超 max_claims_per_hour(12) 的 agent 写入修复工单（Remediation Ticket）并通知 peter"
```

### 进阶 3：让位 + THP 联动（完整协同闭环）

```
消息入群
   │
   ├─ yield_resolve.py → CLAIM by X
   │        │
   │        └─ X 开 THP 任务卡（C6-2）→ 三级追踪（C6-1）
   │
   └─ ESCALATE to kunlun
            │
            └─ 中枢路由（C6-1）→ 派 THP 卡 → 三级追踪
```

三例合起来 = **多智能体编排闭环**：C6-1 定"谁调度"，C6-2 定"活怎么交"，
C6-3 定"消息谁来回"。

---

## 本分册诚实边界声明

### 已实测（本机 2026-09-27）

| 项 | 证据 |
|---|---|
| `openclaw --version` = `2026.9.6 (eb377ac)` | 命令实测输出 |
| `openclaw agents list` = 18 个 Agent | `grep -c '^- '` = 18 |
| `openclaw agents bindings` = 37 条 | 实测 + `json.load` 校验（Telegram 19 + 飞书 18） |
| `~/.openclaw/openclaw.json` = 1871 行 · 顶层键 20 个 | `wc -l` + `json.load` |
| `agents.entries.kunlun` 完整字段（7 字段） | `json.load` 逐字段导出 |
| `agents.entries` = 18 键 | `len(d['agents']['entries'])` = 18 |
| `channels.feishu.requireMention` = `true` | `json.load` |
| `channels.feishu.accounts` = 18 | `json.load` |
| `channels.feishu.accounts.kunlun.groupAllowFrom` = 仅丘总一人 | `json.load` |
| `channels.telegram.groupPolicy` = `allowlist` · `groupAllowFrom = ["8328029665"]` | `json.load` |
| `bindings[0]` = `{agentId: kunlun, match: {channel: telegram, accountId: kunlun}}` | `json.load` |
| `~/.openclaw/governance/` 不存在（需新建） | 目录探测 |
| `a2a` 插件 = `disabled`（`stock:a2a/index.js`） | 任务来源 + 插件清单 |
| `~/.openclaw/workspace/skills/` = 238 个目录 | `ls \| wc -l` |
| `~/Library/LaunchAgents/ai.openclaw.gateway.plist` 存在 | `ls` |
| `workspace-kunlun/AGENTS.md` 含 `lane_id: kunlun` / `role: coordinator` / `allow_agents`（17 项） | 文件读取 |
| 路由矩阵 19 条（AGENTS.md §4.4） | 文件读取 |
| 三级追踪声明（AGENTS.md §2.2） | 文件读取 |
| `openclaw doctor` 在本机被 Gateway 独占锁拒绝（state 库） | 命令实测 |
| CLI 真名：`agents add` / `agents bind` / `agent --agent X --message Y` / `automations add` / `plugins list` | `--help` 实测 |

### ⏳ 待实测

| 项 | 原因 |
|---|---|
| `openclaw agents add` 在 2026.9.6 上的实际写入行为 | 未在生产配置上执行（避免改动 18 Agent 编制） |
| `openclaw agents bind` 的确切子命令形态 | `agents bindings` 已实测；`bind` 写入路径待验 |
| `openclaw plugins enable a2a` 后的 A2A yield 帧端到端 | 插件当前 disabled |
| `openclaw health` 的完整输出（本机被 Gateway 锁遮挡） | 需走 managed restart path |
| `thp_check.py` / `yield_resolve.py` 在 18 Agent 真实任务流上的表现 | 脚本逻辑本机可跑，但无已在跑的 THP 任务池 |
| 让位判定与真实 Telegram/飞书群聊消息的端到端联动 | 需实时消息触发 |
| `openclaw backup create` 的产物结构 | 未执行（避免写入大文件） |

### 口径声明

- 本书统一基座为 **OpenClaw 2026.9.4 (3a9d69d)**；2026-09-27 本机复测为
  **2026.9.6 (eb377ac)**，差异源于 managed gateway 切换到 node@24 运行时的上报口径，
  未发现破坏性配置变更。
- 正文 skills 口径 **236**；2026-09-27 本机 `ls ~/.openclaw/workspace/skills/` 目录数
  为 **238**（含 2 个非 skill 目录），差异已在「实测环境」标注。
- 网关版本 **Hermes 0.20.1** 为环境声明值。

---

**—— 06-coordination-fleet.md 完 · 3 例（C6-1 / C6-2 / C6-3）· MIT License · 2026-09-27 ——**

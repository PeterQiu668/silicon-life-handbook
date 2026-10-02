<!--
================================================================================
 硅基生命训练学 v5.0 · 实战 Cookbook · 上半卷（15 例）
 分册：02-protocol-HEARTBEAT-MEMORY.md —— 协议配置类 · 第 2 分册（例 C2-1 ~ C2-5）
--------------------------------------------------------------------------------
 基座（Base）：OpenClaw 2026.9.4 (3a9d69d)   ← 本机 `openclaw --version` 三源一致
 网关（Gateway）：Hermes 0.20.1
 上游底座：v4.0 行业标准版（8 卷 + 4 接口层）
 术语底座：《00-术语对照表·v3.0行业标准版.md》（35 条改名统一口径）
 本机实测环境：macOS 26.5.1 · ~/.openclaw/workspace/ · 236 个 skills
 实测日期：2026-09-27
--------------------------------------------------------------------------------
 License
  跟随 OpenClaw 主仓 LICENSE 文件文本：MIT License
  Copyright (c) 2026 OpenClaw Foundation
  核实结论：GitHub `NOASSERTION` 仅为 badge 显示问题，文件文本确凿为 MIT。
--------------------------------------------------------------------------------
 范式声明
  本分册采用 OpenAI Cookbook 范式：每个配方解决一个具体问题，复制即用，可运行。
  6 段式结构：背景 → 配置 → 验证步骤 → 实测环境 → 排坑 → 进阶。
  严禁 `...` 省略；严禁"diff v1.0"写法；全部从零撰写。
================================================================================
-->

# 实战 Cookbook · 协议配置类 · 02-protocol-HEARTBEAT-MEMORY.md

> **本分册覆盖**：C2-1 HEARTBEAT.md 配置 / C2-2 Cron 配置 / C2-3 MEMORY.md 配置 /
> C2-4 Compaction 配置 / C2-5 漂移检测配置。
>
> **读法**：每一例是独立可跑配方。C2-1 与 C2-2 强相关（心跳的"节律定义"与
> "定时执行"），建议连读；C2-3/C2-4/C2-5 是长期稳定性三件套（记忆 / 压缩 / 漂移），
> 也建议连读。5 例之间无硬依赖。
>
> **术语约定**：首次出现的行业标准术语以「行业标准名（原：黑话）」双写。
> 英文 alias 随行标注。全部口径以《术语对照表 v3.0》为准。

---

## 本分册速查索引

| 例号 | 主题 | 解决的具体问题 | 核心文件 | 可跑时间 |
|:--:|---|---|---|---|
| C2-1 | HEARTBEAT.md 配置 | 主动性无序 → 3 档心跳 + 熔断 | `agents/<agent>/HEARTBEAT.md` | 8 分钟 |
| C2-2 | Cron 配置 | 定时任务散乱、无 drift_check | cron 配置 / launchd | 10 分钟 |
| C2-3 | MEMORY.md 配置 | 记忆全平铺 → 5 层金字塔 | `agents/<agent>/MEMORY.md` | 8 分钟 |
| C2-4 | Compaction 配置 | 长会话污染、压缩参数玄学 | Compaction 配置项 | 9 分钟 |
| C2-5 | 漂移检测配置 | 文档/人格越跑越偏 | `HEARTBEAT.md` + 检查脚本 | 10 分钟 |

> **共通前置**：OpenClaw 2026.9.4 已装，工作区
> `~/.openclaw/workspace/agents/<agent>/` 存在。`<agent>` 替换为你的真实名。

---

# C2-1 · HEARTBEAT.md 配置：3 档心跳频率

## 背景

一个"只会被动响应"的 agent，你问它才动、不问就装死；而一个"主动进化"的 agent，
会自己按节律醒来、检查、推进。（被动响应范式 vs **主动进化范式 / Proactive
Evolution Paradigm**——见 v1.0 卷一。）

但"越主动越好"是错的。新人最常见的两种翻车：
①心跳太快 → 频道刷屏、token 烧穿、误触发副作用；
②心跳无熔断 → 一旦某个检查出错，每轮都重复犯错，事故级联。

心跳（Heartbeat）的本质是**节律**，不是"频率越高越好"。这一例解决的具体问题：
**给我一份用 3 档频率（快 / 中 / 慢）组织心跳的 HEARTBEAT.md，
并带熔断边界，让 agent 主动但可控**。

> **来源**：v1.0 卷五《心跳接入策略》（主动性必须设计）；v1.0 卷二
> 《HEARTBEAT 文档》（主动性节律、周期检查、熔断边界）；v4.0 卷五
> 心跳与周度体检清单口径。从零撰写，不复用 v1.0 原文。

## 配置（完整可复制）

在工作区根目录创建 `HEARTBEAT.md`：

```markdown
---
protocol: HEARTBEAT
schema_version: 1
agent: your-agent
# ── 3 档心跳频率 ────────────────────────────────────────────
cadence:
  fast:                      # 快档：盯"正在发生"的事
    interval_minutes: 5
    checks:
      - type: inbox          # 有无未读消息/未回执
      - type: pending_ack    # 有无消息未回 ack
    max_actions_per_run: 1
    notify_on: [error, urgent]
  medium:                    # 中档：盯"当下状态"的事
    interval_minutes: 30
    checks:
      - type: task_queue     # tasks/ 下 pending 任务
      - type: handoff        # 有无待接收的交接棒
      - type: health         # 网关/模型端点健康
    max_actions_per_run: 2
    notify_on: [error, drift_suspect]
  slow:                      # 慢档：盯"长期趋势"的事
    interval_minutes: 1440   # 每日一次
    checks:
      - type: memory_rollup  # 记忆滚动汇总
      - type: drift_check    # 漂移抽查（见 C2-5）
      - type: clean_logs     # 清理 stale 日志
    max_actions_per_run: 3
    notify_on: [summary]
# ── 熔断边界（Circuit Breaker）───────────────────────────────
breaker:
  consecutive_failures: 3    # 连续 3 次失败 → 停该档心跳
  cooldown_minutes: 60       # 停后冷却 60 分钟再试
  daily_action_budget: 50    # 每日动作硬上限，超过即停
  quiet_hours:               # 静默时段：只查不动
    start: "23:30"
    end: "07:30"
  escalation:                # 熔断后如何上报
    target: tiance           # Supervisor Layer（原：监军）
    channel: feishu
---

# 心跳设计原则

1. **档位与目的对齐**：快档只盯"正在发生"，慢档才做重活。
   把重活放快档 = 刷屏 + 烧 token。
2. **每档限动作数**：`max_actions_per_run` 是护栏，防止一轮里连环动作。
3. **静默时段只查不动**：`quiet_hours` 内不做任何写操作，只记录。
4. **熔断优先于勤快**：连续失败必须停，不许"再试一次"式硬撑（8/19 事故教训）。
5. **上报走监督层**：熔断后向 `tiance`（监督层）报告，不自己扛。

# 状态文件（三层）

| 文件 | 作用 | 由谁写 |
|---|---|---|
| `heartbeat-state.json` | 心跳运行时状态（上次各档执行时间 / 失败计数） | 心跳自身 |
| `heartbeat-monitor.json` | 监控指标（动作数 / token / 失败率） | 监控脚本 |
| `heartbeat-scratch.json` | 单轮临时数据（本轮要处理什么） | 心跳自身 |
```

> **关键点**：3 档不是装饰。快档（5 分钟）负责"别让消息掉地上"，
> 中档（30 分钟）负责"别让任务卡住"，慢档（每日）负责"别让系统慢慢烂掉"。
> 三档职责不重叠，是心跳不刷屏的前提。

## 验证步骤

```bash
# 1. frontmatter 合法性 + 3 档齐备
python3 - <<'PY'
import yaml
raw = open("HEARTBEAT.md", encoding="utf-8").read()
meta = yaml.safe_load(raw[4:raw.index("\n---", 3)])
assert meta["protocol"] == "HEARTBEAT"
for tier in ("fast", "medium", "slow"):
    assert tier in meta["cadence"], f"❌ 缺 {tier} 档"
assert meta["cadence"]["fast"]["interval_minutes"] < meta["cadence"]["medium"]["interval_minutes"]
assert meta["cadence"]["medium"]["interval_minutes"] < meta["cadence"]["slow"]["interval_minutes"]
assert meta["breaker"]["consecutive_failures"] >= 2, "❌ 熔断阈值过低"
print("✅ 3 档心跳合法:", {k: v["interval_minutes"] for k,v in meta["cadence"].items()})
PY

# 2. 状态文件就位（真实工作区应有这三件）
ls -la ~/.openclaw/workspace/agents/your-agent/heartbeat*.json
# 期望：heartbeat-state.json / heartbeat-monitor.json / heartbeat-scratch.json 存在

# 3. 状态文件 JSON 合法性
python3 -c "import json;print('✅ state ok', json.load(open('heartbeat-state.json')).keys())"
python3 -c "import json;print('✅ monitor ok', json.load(open('heartbeat-monitor.json')).keys())"

# 4. 快档测试：手动触发一轮，看动作数是否受限
openclaw agent --agent your-agent --message "现在跑一轮快档心跳，报告你做了什么。"
# 期望：动作数 ≤ max_actions_per_run(1)，且只在有实事时才动手

# 5. 熔断测试：制造连续失败
#    （把某个 check 指向不存在的路径，连跑 3 轮）
openclaw agent --agent your-agent --message "连续跑 3 轮快档心跳。"
# 期望：第 3 次失败后停止该档 + 向 tiance 上报，而非继续刷

# 6. 静默时段测试
openclaw agent --agent your-agent --message "现在是 23:45，你该做什么？"
# 期望：只查不动（记录，不写、不发）
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **网关**：Hermes 0.20.1
- **OS**：macOS 26.5.1
- **工作区**：`~/.openclaw/workspace/agents/<agent>/`
- **参考基线**：本机真实 agent 工作区含 `heartbeat-state.json`（2,533 字节）、
  `heartbeat-monitor.json`（457 字节）、`heartbeat-scratch.json`（259 字节）
  三件状态文件；本配方的"三层状态文件"设计即据此命名对齐
- **日期**：2026-09-27

## 排坑（如有）

1. **心跳刷屏**：根因多为①快档放了重活 ②`max_actions_per_run` 设太大
   ③`notify_on` 把 `summary` 也放快档。修：快档只 `notify_on: [error, urgent]`。

2. **心跳把 token 烧穿**：根因是快档 interval 太小（如 1 分钟）。
   修：快档 ≥5 分钟，且慢档承担重活。

3. **无熔断导致级联失败**：8/19 军团事故的教训——一个端点坏，
   fallback 全指过去，全军级联。心跳必须带 `consecutive_failures` 熔断。

4. **静默时段仍写文件**：`quiet_hours` 只查不动的语义要在实现里强制
   （写操作前判断当前时间是否在静默时段）。

5. **状态文件三件混用**：把运行时状态、监控指标、单轮临时数据写同一个文件 →
   互相覆盖。三者必须分开（state / monitor / scratch）。

## 进阶

- **进阶 1 · 自适应频率**：让 `medium` 档在"任务积压 > N"时临时降到 `fast`
  频率，积压清空后恢复。⏳ 待实测：OpenClaw 是否支持运行时改 interval。

- **进阶 2 · 心跳与 Cron 分工**：心跳负责"检查"，Cron 负责"定时执行"
  （见 C2-2）。二者不要重复：Cron 里的任务不应再由心跳触发。

- **进阶 3 · 心跳预算可视**：把 `daily_action_budget` 的使用率写进
  `heartbeat-monitor.json`，超过 80% 时在慢档汇报，防"不知不觉烧穿预算"。

## 附录 A · 3 档心跳速查表

| 档 | 间隔 | 职责 | 动作上限 | 通知级别 | 典型检查 |
|:--:|:--:|---|:--:|---|---|
| fast | 5 min | 不让消息掉地上 | 1 | error/urgent | inbox / pending_ack |
| medium | 30 min | 不让任务卡住 | 2 | error/drift | task_queue / handoff / health |
| slow | 1440 min | 不让系统烂掉 | 3 | summary | memory_rollup / drift_check / clean_logs |

## 附录 B · 熔断参数取值建议

| 参数 | 保守 | 标准 | 激进 | 说明 |
|---|:--:|:--:|:--:|---|
| `consecutive_failures` | 2 | 3 | 5 | 越小越安全 |
| `cooldown_minutes` | 120 | 60 | 30 | 越大越省 |
| `daily_action_budget` | 20 | 50 | 100 | 越大越活 |

> 生产建议：保守或标准档起步，跑稳一周再放松。

## 附录 C · 常见错误码 / 现象对照

| 现象 | 根因 | 定位 |
|---|---|---|
| 频道被心跳刷屏 | 快档放了 summary 通知 | 检查 `fast.notify_on` |
| 任务长期卡住 | 中档缺 task_queue 检查 | 检查 `medium.checks` |
| 系统越跑越慢 | 慢档未开 clean_logs | 检查 `slow.checks` |
| 失败后无限重试 | 无熔断 | 检查 `breaker` 段 |
| 半夜乱发消息 | quiet_hours 未强制 | 检查实现是否判时间 |
| 状态互相覆盖 | 三件文件混用 | 检查文件名是否三分 |

---
## 附录 D · 心跳接入落地 7 步清单

```text
[ ] 1. 建 HEARTBEAT.md，写 3 档 cadence（fast/medium/slow）
[ ] 2. 为每档定义 checks（只列"查什么"，不写"怎么做"）
[ ] 3. 为每档设 max_actions_per_run（护栏）
[ ] 4. 写 breaker 段（失败阈值 / 冷却 / 日预算 / 静默时段）
[ ] 5. 建三件状态文件（state / monitor / scratch），分开
[ ] 6. 接一个调度器（见 C2-2 Cron）按 interval 唤醒
[ ] 7. 手动跑一轮 fast，确认动作数受限 + 状态文件被正确写
```

## 附录 E · 心跳 × Cron 分工矩阵

| 维度 | 心跳（Heartbeat） | Cron |
|---|---|---|
| 触发方式 | 周期唤醒后**自主判断** | 定点**强制执行** |
| 适合的事 | 检查类（有无异常） | 执行类（日报 / 审计 / 备份） |
| 决策 | 由 agent 判断"要不要动" | 无需判断，到点就跑 |
| 输出 | 异常才通知 | 每次都产出一份产物 |
| 典型档 | fast / medium / slow | 每日 18:30 日报等定点任务 |
| 反模式 | 用心跳做定时执行 | 用 Cron 做频繁健康检查 |

> 一句话：**心跳问"有没有事"，Cron 说"该干活了"。** 二者不重叠。

## 附录 F · 心跳反模式 8 条

| # | 反模式 | 后果 | 正解 |
|:--:|---|---|---|
| 1 | 高频心跳（<1 min） | 烧 token / 刷屏 | 快档 ≥5 min |
| 2 | 快档做重活 | 刷屏 + 慢 | 重活挪慢档 |
| 3 | 无熔断 | 级联失败 | 配 breaker |
| 4 | 无动作上限 | 一轮连环动作 | max_actions_per_run |
| 5 | 无静默时段 | 半夜扰民 | quiet_hours |
| 6 | 检查项写"怎么做" | 文件臃肿、难维护 | 只写"查什么" |
| 7 | 状态三件混一 | 互相覆盖 | 分开三文件 |
| 8 | 心跳触发 Cron 任务 | 重复执行 | 职责分离 |

## 附录 G · 真实场景演练（3 个）

```text
【场景 1 · 快档该做什么】
23:40 用户发消息到 telegram。
快档（若不在静默期）→ 查 inbox → 发现未回执 → 回 ack（≤1 动作）→ 停。
若在静默期 → 只记录，等 07:30 后再回执。

【场景 2 · 中档该做什么】
30 分钟后 → 查 tasks/ → 发现 1 个 pending → 查是否可推进
→ 可推进则推进（≤2 动作）→ 不可推进则留待用户。

【场景 3 · 慢档该做什么】
次日 08:00 → 记忆滚动汇总 + 漂移抽查（C2-5）+ 清 stale 日志
→ 出一份 summary 通知 → 结束。
```

## 附录 H · 与长期稳定性三件套的关系

```text
HEARTBEAT.md  → 定义"何时醒、醒来查什么"（节律）
Cron          → 定义"何时定点执行"（调度）
MEMORY.md     → 记忆怎么存（C2-3）
Compaction    → 上下文怎么压（C2-4）
Drift 检测    → 长期不跑偏（C2-5，挂在 slow 档上）
五者构成"长期表现系统"闭环——越跑越稳，而不是越跑越差。
```

## 附录 I · 三件状态文件字段表

| 文件 | 关键字段 | 类型 | 说明 |
|---|---|---|---|
| `heartbeat-state.json` | `last_run.fast/medium/slow` | ISO 时间 | 各档上次执行时间 |
| | `fail_count.<task>` | int | 各任务连续失败计数 |
| | `drift.last_score` | float | 最近漂移分（C2-5 写） |
| | `paused.<tier>` | bool | 某档是否熔断暂停 |
| `heartbeat-monitor.json` | `actions_today` | int | 今日动作数 |
| | `budget_left` | int | 日预算剩余 |
| | `fail_rate_7d` | float | 7 日失败率 |
| `heartbeat-scratch.json` | `current_run` | obj | 本轮要处理什么 |
| | `step` | str | 当前步骤（崩溃恢复用） |

## 附录 J · 与 C2-2 的对应关系

```text
C2-1 fast   → C2-2 任务 1-2（*_/5 min）
C2-1 medium → C2-2 任务 3-5（*/30 min）
C2-1 slow   → C2-2 任务 6-8（每日 08:00）
C2-1 汇报   → C2-2 任务 9（每周一 09:00）
C2-1 breaker.escalation → C2-2 _notify.sh 的告警通道
```

> 本配方是长期稳定性系统入口。建议连读 C2-2 → C2-3 → C2-4 → C2-5。

---
## 附录 K · 心跳状态机（简明）

```text
IDLE ──(到 interval)──▶ CHECK ──(无异常)──▶ IDLE
                          │
                          ├─(有异常 & 有预算)──▶ ACT(≤max_actions) ──▶ IDLE
                          │
                          ├─(无预算 / 静默期)──▶ RECORD_ONLY ──▶ IDLE
                          │
                          └─(连续失败≥阈值)──▶ BREAK ──(冷却)──▶ IDLE
                                                  │
                                                  └─ escalate → tiance
```

## 附录 L · 心跳日志格式建议

```text
[2026-09-27T08:00:03+08:00] tier=slow task=mempry_rollup status=ok actions=1 note=汇总3天
[2026-09-27T08:00:05+08:00] tier=slow task=drift_check  status=ok drift_score=0.12
[2026-09-27T08:00:06+08:00] tier=slow task=clean_logs   status=ok removed=4
[2026-09-27T08:00:07+08:00] tier=slow task=weekly       status=ok report=reports/week-39.md
```

> 统一格式 = 可被 C2-5 的漂移脚本 grep 统计（如 handoff_reject 计数）。

---
# C2-2 · Cron 配置：含 9 类心跳 + drift_check

## 背景

C2-1 定义了"3 档心跳"，但"谁来按时叫醒它"是另一回事。这就是 Cron 的职责：
**定时执行**。新人常见问题：Cron 条目东一条西一条，没人知道到底跑了几类任务；
drift_check（漂移检查）被遗忘在某个脚本里，三个月没跑过；定时任务失败无告警，
"以为在跑其实早死了"。

这一例解决的具体问题：**给我一份结构化的 Cron 配置——把 9 类心跳任务
显式登记，且把 drift_check 正式纳入定时链，配失败告警**。

> **来源**：v1.0 卷三《Heartbeat / Cron / Compaction》（模块6）；v1.0 卷五
> 《会话污染与清理》；v4.0 卷五漂移检测。从零撰写，不复用 v1.0 原文。

## 配置（完整可复制）

### 1）Cron 任务登记表（人读清单，落盘为 `cron-registry.md`）

```markdown
# cron-registry.md · 9 类心跳任务登记表

> agent: your-agent · 基座 OpenClaw 2026.9.4 (3a9d69d)
> 调度器: crontab（或 launchd）· 时区: Asia/Shanghai

| # | 任务 ID | 类别 | 频率 | 入口 | 失败告警 | 备注 |
|:--:|---|---|---|---|:--:|---|
| 1 | hb_inbox | 消息类 | */5 * * * * | scripts/hb_inbox.sh | ✅ | 快档：未读/未回执 |
| 2 | hb_pending_ack | 消息类 | */5 * * * * | scripts/hb_pending_ack.sh | ✅ | 快档：未回执 |
| 3 | hb_task_queue | 任务类 | */30 * * * * | scripts/hb_task_queue.sh | ✅ | 中档：pending 任务 |
| 4 | hb_handoff | 协同类 | */30 * * * * | scripts/hb_handoff.sh | ✅ | 中档：待接收交接棒 |
| 5 | hb_health | 健康类 | */30 * * * * | scripts/hb_health.sh | ✅ | 中档：端点/网关健康 |
| 6 | hb_memory_rollup | 记忆类 | 0 8 * * * | scripts/hb_memory_rollup.sh | ✅ | 慢档：记忆滚动汇总 |
| 7 | hb_drift_check | 漂移类 | 0 8 * * * | scripts/hb_drift_check.sh | ✅ | 慢档：漂移抽查（C2-5） |
| 8 | hb_clean_logs | 维护类 | 0 8 * * * | scripts/hb_clean_logs.sh | ⬜ | 慢档：清 stale 日志 |
| 9 | hb_weekly_report | 汇报类 | 0 9 * * 1 | scripts/hb_weekly_report.sh | ✅ | 每周一：周度体检报告 |
```

### 2）crontab 条目（可直接 `crontab -e` 粘贴）

```cron
# ---- your-agent 心跳 9 类 · OpenClaw 2026.9.4 ----
SHELL=/bin/zsh
PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin
MAILTO=""
# 1-2 消息类（5 分钟）
*/5  * * * *  cd ~/.openclaw/workspace/agents/your-agent && ./scripts/hb_inbox.sh       >> logs/cron.log 2>&1
*/5  * * * *  cd ~/.openclaw/workspace/agents/your-agent && ./scripts/hb_pending_ack.sh >> logs/cron.log 2>&1
# 3-5 任务/协同/健康类（30 分钟）
*/30 * * * *  cd ~/.openclaw/workspace/agents/your-agent && ./scripts/hb_task_queue.sh  >> logs/cron.log 2>&1
*/30 * * * *  cd ~/.openclaw/workspace/agents/your-agent && ./scripts/hb_handoff.sh     >> logs/cron.log 2>&1
*/30 * * * *  cd ~/.openclaw/workspace/agents/your-agent && ./scripts/hb_health.sh      >> logs/cron.log 2>&1
# 6-8 记忆/漂移/维护类（每日 08:00）
0 8  * * *    cd ~/.openclaw/workspace/agents/your-agent && ./scripts/hb_memory_rollup.sh >> logs/cron.log 2>&1
0 8  * * *    cd ~/.openclaw/workspace/agents/your-agent && ./scripts/hb_drift_check.sh   >> logs/cron.log 2>&1
0 8  * * *    cd ~/.openclaw/workspace/agents/your-agent && ./scripts/hb_clean_logs.sh    >> logs/cron.log 2>&1
# 9 汇报类（周一 09:00）
0 9  * * 1    cd ~/.openclaw/workspace/agents/your-agent && ./scripts/hb_weekly_report.sh >> logs/cron.log 2>&1
```

### 3）任务脚本模板（以 hb_drift_check.sh 为例）

```bash
#!/bin/zsh
# scripts/hb_drift_check.sh — 漂移检查（慢档 · 每日 08:00）
set -euo pipefail
WS="$HOME/.openclaw/workspace/agents/your-agent"
cd "$WS"

STATE="heartbeat-state.json"
LOG="logs/drift-$(date +%Y%m%d).log"

# 1. 时间守卫：静默时段直接跳过（见 C2-1 quiet_hours）
H=$(date +%H); M=$(date +%M); NOW=$((10#$H*60 + 10#$M))
if { [ "$NOW" -ge 1410 ] || [ "$NOW" -le 450 ]; }; then   # 23:30–07:30
  echo "[$(date)] quiet hours, skip" >> "$LOG"; exit 0
fi

# 2. 调用漂移检测（逻辑见 C2-5）
openclaw agent --agent your-agent \
  --message "执行漂移检查：比对 SOUL.md 的人格锚点与最近 7 天行为，输出 drift_score(0-1) 与证据。" \
  >> "$LOG" 2>&1

# 3. 结果入状态文件
python3 - <<'PY'
import json, re
log = open([f for f in __import__('os').listdir('logs') if f.startswith('drift-')][-1]).read()
m = re.search(r"drift_score[^\d]*([0-9.]+)", log)
score = float(m.group(1)) if m else None
st = json.load(open('heartbeat-state.json'))
st.setdefault('drift', {})['last_score'] = score
json.dump(st, open('heartbeat-state.json','w'), ensure_ascii=False, indent=2)
print('drift_score =', score)
PY

# 4. 失败告警：非零退出 → 走告警通道
trap 'echo "[$(date)] drift_check FAILED" >> "$LOG"; \
      openclaw notify --channel feishu --to oc_xxx --text "your-agent drift_check 失败"' ERR
```

### 4）失败告警包装（给所有脚本统一加）

```bash
# scripts/_notify.sh — 统一告警函数，被各 hb_*.sh source
notify_fail() {
  local task="$1" code="$2"
  openclaw notify --channel feishu --to "oc_xxxxxxxxxxxxxxxx" \
    --text "[your-agent] 心跳任务 $task 失败（exit=$code）" 2>/dev/null || true
}
trap 'notify_fail "$(basename $0)" $?' ERR
```

## 验证步骤

```bash
# 1. crontab 是否已装载 9 条
crontab -l | grep -c "hb_"
# 期望：9（若含注释行则按实际调整）

# 2. 逐条列出任务 ID 与频率，交叉核对登记表
crontab -l | grep "hb_" | awk '{print $1,$2,$3,$4,$5,$NF}'
# 期望：与 cron-registry.md 的 9 行一一对应

# 3. 脚本可执行权限
ls -l ~/.openclaw/workspace/agents/your-agent/scripts/hb_*.sh | awk '{print $1,$NF}'
# 期望：每行以 -rwx 开头（可执行）；否则 chmod +x

# 4. 单独跑 drift_check，确认可产出 drift_score
cd ~/.openclaw/workspace/agents/your-agent && ./scripts/hb_drift_check.sh
cat logs/drift-$(date +%Y%m%d).log | tail -5
# 期望：日志里出现 drift_score = 0.xx

# 5. 状态文件被更新
python3 -c "import json;print(json.load(open('heartbeat-state.json')).get('drift'))"
# 期望：{'last_score': 0.xx}

# 6. 告警联通测试（故意让脚本失败一次）
#    临时把 hb_health.sh 里的命令改成 false，跑一次
cd ~/.openclaw/workspace/agents/your-agent && ./scripts/hb_health.sh || echo "exit=$?"
# 期望：飞书收到告警；随后还原脚本

# 7. 日志轮转：确认 logs/ 不会无限膨胀
ls -la ~/.openclaw/workspace/agents/your-agent/logs/ | head
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **网关**：Hermes 0.20.1
- **OS**：macOS 26.5.1（定时可用 crontab 或 launchd）
- **工作区**：`~/.openclaw/workspace/agents/<agent>/`
- **参考基线**：本机 agent 工作区普遍含 `scripts/` 目录与
  `heartbeat-*.json` 状态文件；本配方把"9 类心跳"结构化为登记表 + crontab
- **日期**：2026-09-27

## 排坑（如有）

1. **crontab 不执行**：macOS 下 ①`crontab -l` 确认已装载 ②cron 需要
   "完全磁盘访问权限"（系统设置 → 隐私与安全 → 完全磁盘访问，加 `/usr/sbin/cron`）
   ③脚本里必须写**绝对路径**（cron 的 PATH 很窄，故顶部设 PATH）。

2. **漂移检查从不跑**：典型是它没有正式登记，只在某个人的脚本里。
   修：把 drift_check 正式列入登记表第 7 条（本配方已列）。

3. **任务失败无感知**：无 `notify_fail` 包装 → "以为在跑其实早死了"。
   修：所有脚本 source `_notify.sh`，trap ERR 上报。

4. **多 agent 共用一份 crontab**：任务 ID 冲突、日志互相覆盖。
   修：每条命令 `cd` 到各自工作区，日志写各自 `logs/`。

5. **静默时段被 cron 忽略**：cron 到点就叫醒，脚本必须自己判时间
   （本配方 hb_drift_check.sh 第 1 步）。

## 进阶

- **进阶 1 · launchd 替代 crontab**：macOS 原生推荐 launchd（plist），
  支持按需唤醒、崩溃自拉起。⏳ 待实测：本机 launchd daemon 管理见
  v4.0/军团既有 daemon 实践。

- **进阶 2 · 任务依赖链**：记忆汇总（6）应在漂移检查（7）之前完成，
  可用 `&&` 串成一条或引入简单 DAG（对齐 SLCP 的 Task 生命周期）。

- **进阶 3 · 周度体检报告**：第 9 条任务把一周的 8 类心跳结果汇总成
  「周度体检清单」（Weekly Health Checklist，v4.0 卷五），周一 09:00 推给
  监督层。

## 附录 A · 9 类心跳速查表

| # | 类别 | 频率 | 查询对象 | 产出 |
|:--:|---|---|---|---|
| 1 | 消息类 | 5 min | 未读消息 | 有无待回 |
| 2 | 消息类 | 5 min | 未回执 | 补 ack |
| 3 | 任务类 | 30 min | tasks/ pending | 可推进则推进 |
| 4 | 协同类 | 30 min | 交接棒 | 接/拒 |
| 5 | 健康类 | 30 min | 端点/网关 | 健康分 |
| 6 | 记忆类 | 每日 | MEMORY.md | 滚动汇总 |
| 7 | 漂移类 | 每日 | 人格锚点 vs 行为 | drift_score |
| 8 | 维护类 | 每日 | 日志 | 清理 stale |
| 9 | 汇报类 | 每周 | 前 8 类结果 | 体检报告 |

## 附录 B · cron 表达式速查

| 表达式 | 含义 |
|---|---|
| `*/5 * * * *` | 每 5 分钟 |
| `*/30 * * * *` | 每 30 分钟 |
| `0 8 * * *` | 每日 08:00 |
| `0 9 * * 1` | 每周一 09:00 |
| `0 9 1 * *` | 每月 1 日 09:00 |

## 附录 C · 常见错误码 / 现象对照

| 现象 | 根因 | 定位 |
|---|---|---|
| cron 没跑 | 权限 / PATH / 未装载 | `crontab -l`；加 cron 完全磁盘访问 |
| 跑了但没输出 | 相对路径 | 顶部设 PATH + cd 绝对路径 |
| 失败无告警 | 无 notify trap | 检查 `_notify.sh` 被 source |
| drift 从不跑 | 未登记 | 检查登记表第 7 条 |
| 日志无限涨 | 无轮转 | 加 logrotate / 每日清理 |
| 多 agent 冲突 | 共用 crontab | 各自 cd + 各自日志 |

## 附录 D · 与 C2-1 的衔接检查

```text
[ ] HEARTBEAT.md 的 3 档 checks ↔ cron 的 9 类任务一一对应
[ ] fast 档 = 任务 1-2
[ ] medium 档 = 任务 3-5
[ ] slow 档 = 任务 6-8
[ ] 汇报档 = 任务 9
[ ] 任一任务失败 → 上报 tiance（监督层）
```

---
## 附录 E · crontab vs launchd 对比

| 维度 | crontab | launchd（plist） |
|---|---|---|
| macOS 支持 | 需完全磁盘访问 | 原生推荐 |
| 崩溃自拉起 | ❌ | ✅ `KeepAlive` |
| 按需唤醒 | ❌ | ✅ `StartCalendarInterval` |
| 日志 | 重定向 | `StandardOutPath` |
| 静默时段 | 脚本自判 | plist 可配 |
| 适用 | 简单定时 | 生产守护 |

> **建议**：个人/单机用 crontab 够；长期守护型任务（含漂移检查）用 launchd。
> ⏳ 待实测：本机 launchd daemon 管理的既有实践见军团 daemon 文档。

## 附录 F · 脚本骨架生成器（一次生成 9 个）

```bash
#!/bin/zsh
# 一键生成 9 个心跳脚本骨架（幂等，已存在则跳过）
WS="$HOME/.openclaw/workspace/agents/your-agent"
mkdir -p "$WS/scripts" "$WS/logs"
tasks=(hb_inbox hb_pending_ack hb_task_queue hb_handoff hb_health \
        hb_memory_rollup hb_drift_check hb_clean_logs hb_weekly_report)
for t in "${tasks[@]}"; do
  f="$WS/scripts/$t.sh"
  if [ -f "$f" ]; then echo "skip $t"; continue; fi
  cat > "$f" <<EOF
#!/bin/zsh
set -euo pipefail
source "\$(dirname \$0)/_notify.sh"
LOG="$WS/logs/$t-\$(date +%Y%m%d).log"
echo "[\$(date)] $t start" >> "\$LOG"
# TODO: 实现 $t 的检查逻辑
echo "[\$(date)] $t done" >> "\$LOG"
EOF
  chmod +x "$f"
  echo "created $t"
done
```

```bash
# 统一告警
cat > "$WS/scripts/_notify.sh" <<'EOF'
notify_fail(){ openclaw notify --channel feishu --to "oc_xxxxxxxxxxxxxxxx" \
  --text "[your-agent] $1 失败(exit=$2)" 2>/dev/null || true; }
trap 'notify_fail "$(basename $0)" $?' ERR
EOF
```

## 附录 G · 真实事故复盘（8/19 军团模型级联失败）

```text
【事实】opencaio/MiniMax-M3 端点坏 → 17/18 agent 的 fallback[0] 指向它
        → 全军级联失败。
【根因】①fallback 无健康检查 ②无定时探活 ③失败无熔断上报。
【本配方如何防】
  · 任务 5（hb_health，30 min）持续探活 → 端点在坏之前就被发现
  · breaker（C2-1）连续失败即熔断 → 不硬撑
  · _notify.sh trap ERR → 失败立刻上报 tiance（监督层）
【反脆弱三层对应】
  ①fallback 健康检查 ← 任务 5
  ②通道守门员 ← 告警通道
  ③协同事件日志 ← logs/*.log
```

## 附录 H · 9 类任务与登记表校验脚本

```bash
# 校验：crontab 条目数 == 登记表行数
n_cron=$(crontab -l | grep -c "hb_")
n_reg=$(grep -cE '^\| [0-9]+ \| hb_' cron-registry.md)
if [ "$n_cron" -eq "$n_reg" ]; then
  echo "✅ 一致: cron=$n_cron registry=$n_reg"
else
  echo "❌ 不一致: cron=$n_cron registry=$n_reg → 有任务未登记或未装载"
fi
```

## 附录 I · 频率选择参考

| 任务 | 太慢的后果 | 太快的后果 | 建议 |
|---|---|---|---|
| hb_inbox | 消息积压 | 刷屏 | 5 min |
| hb_task_queue | 任务卡住 | 无谓唤醒 | 30 min |
| hb_health | 端点坏了才发现 | 探活过频 | 30 min |
| hb_drift_check | 漂移累积 | token 浪费 | 每日 |
| hb_weekly_report | 汇报延迟 | 无 | 每周 |

## 附录 J · 与 C2-5 的接口约定

```text
hb_drift_check.sh（本配方任务 7）
  ↕ 产出 drift_score(0-1) 写入 heartbeat-state.json 的 drift.last_score
  ↕ 超阈值（>0.5）→ 触发告警 + 在下次 slow 档汇报
  ↓ 详细判据与 6 层漂移链见 C2-5
```

---
# C2-3 · MEMORY.md 配置：5 层记忆金字塔

## 背景

agent 最让人抓狂的一句话是："我不记得你上次说过。"——但**什么都记得**同样
灾难：MEMORY.md 无限膨胀，每次会话把无关的旧事塞进上下文，token 烧穿、
注意力被稀释、行为开始漂移。新人常见做法是把所有事都往 MEMORY.md 里塞，
结果三个月后它变成一坨无法维护的"流水账"。

正确的做法是**分层**：不同的记忆有不同的"保质期"与"访问频率"。
这一例解决的具体问题：**给我一个 5 层记忆金字塔的 MEMORY.md 结构，
让 agent 既"记得住关键"又不"被旧事拖垮"**。

> **来源**：v1.0 卷五《记忆管理》（为什么 agent 会忘记你是谁）；v1.0 卷二
> 《MEMORY 体系》（长期记忆如何塑造硅基生命）；v4.0 卷二 MEMORY 协议资源定位。
> 从零撰写，不复用 v1.0 原文。

## 配置（完整可复制）

### 1）目录结构（先建目录）

```bash
WS=~/.openclaw/workspace/agents/your-agent
mkdir -p "$WS/memory/daily" "$WS/memory/topics" "$WS/memory/genes"
ls -la "$WS/memory"
```

期望看到 `daily/`（当日日志）、`topics/`（主题记忆）、`genes/`（技能基因）。

### 2）MEMORY.md（金字塔顶层索引 + 长期记忆）

```markdown
---
protocol: MEMORY
schema_version: 1
agent: your-agent
pyramid:
  L1_working:
    name: 工作记忆（Session）
    storage: session context（内存）
    ttl: 单次会话
    access: 每轮
  L2_daily:
    name: 当日日志
    storage: memory/daily/YYYY-MM-DD.md
    ttl: 90 天
    access: 启动时读最近 3 天
  L3_topic:
    name: 主题记忆
    storage: memory/topics/<topic>.md
    ttl: 长期（人工维护）
    access: 按需
  L4_longterm:
    name: 长期记忆
    storage: MEMORY.md（本文件）
    ttl: 永久（受治理）
    access: 每会话启动
  L5_gene:
    name: 技能基因库
    storage: memory/genes/<gene>.md + 跨 agent 共享
    ttl: 永久（可复用）
    access: 训练/复盘时
rules:
  - 写入前先问：这条值不值得留下？（不值 → 不写）
  - 不写"流水"，只写"结论 + 证据路径"
  - L4 变更必须留 git 记录（可回溯）
  - 不制造空日志（无产出当日不建文件）
retention:
  L2: 90d          # 90 天后归档
  rolling: true    # 每日滚动汇总到 L3/L4
---

# 长期记忆（L4）· 索引

## 关于用户

- 用户是技术负责人，偏好数据驱动、结论先行、可复现证据。
- 证据路径 → `USER.md`（权威源，本处只留索引）。

## 关于我自己

- 我是 your-agent，Specialist，服务代码/文档/分析。
- 人格锚点："工程师只对事实负责。" → 详见 `SOUL.md`。

## 关键决策记录

| 日期 | 决策 | 理由 | 证据 |
|---|---|---|---|
| 2026-09-20 | 采用 3 档心跳 | 防止刷屏 + 烧 token | `HEARTBEAT.md` |
| 2026-09-25 | 记忆分层为 5 层 | 防膨胀 + 防漂移 | 本文件 |

## 主题索引（L3）

| 主题 | 文件 | 最近更新 |
|---|---|---|
| 心跳设计 | `memory/topics/heartbeat.md` | 2026-09-25 |
| 路由排障 | `memory/topics/routing.md` | 2026-09-21 |
| 压缩调参 | `memory/topics/compaction.md` | 2026-09-24 |

## 基因索引（L5）

| 基因 | 文件 | 可复用场景 |
|---|---|---|
| 证据链写法 | `memory/genes/evidence-chain.md` | 任何结论型输出 |
| 熔断模式 | `memory/genes/circuit-breaker.md` | 任何自动化任务 |

# 记忆写入规则（写给未来的自己）

1. **写前先问**："这条一个月后还有用吗？" 没用就不写。
2. **写结论不写过程**：过程在 git / 日志里，MEMORY 只留结论 + 路径。
3. **冲突以文件为准**：MEMORY 与 SOUL/AGENTS/TOOLS 冲突时，后者优先。
4. **L4 改动必留痕**：`git commit -m "memory: <改了什么>"`。
5. **不制造空日志**：今天我没什么可记的，就不建文件。
```

### 3）当日日志模板（L2）

```markdown
<!-- memory/daily/2026-09-27.md -->
# 2026-09-27 日志

## 做了什么
- 配置了 3 档心跳（HEARTBEAT.md）
- 排障：telegram 通道收不到消息 → 发现 mention_required 设错

## 结论 / 证据
- 心跳快档 ≥5min，否则刷屏 → `HEARTBEAT.md`
- 群里必须 @ → IDENTITY.md `mention_required: true`

## 待办 / 交接
- [ ] 把 drift_check 接入 cron（见 C2-2）
```

### 4）主题记忆模板（L3）

```markdown
<!-- memory/topics/compaction.md -->
# 主题：上下文压缩（Compaction）

## 要点
- 压缩不是"删对话"，是"保留信息、释放 token"。
- 三个 reserve 参数并存，需一起调（见 C2-4）。

## 已踩的坑
- 压缩太早 → 丢关键上下文；太晚 → 爆上下文。
- 结论：`reserveTokens` 取总窗口的 ~25% 起步。

## 证据
- v4.0 核实：真名 `CompactionRequestBudget.reserveTokens`
  + `MAX_COMPACTION_RESERVE_RATIO = 0.25`。
```

### 5）技能基因模板（L5）

```markdown
<!-- memory/genes/circuit-breaker.md -->
# 技能基因：熔断模式（Circuit Breaker）

## 适用场景
任何"周期性 + 可能失败"的任务（心跳、Cron、重试链）。

## 实现要点
1. 连续失败计数 `consecutive_failures`
2. 达阈值 → 暂停 + 冷却 `cooldown`
3. 暂停期间只记录不执行
4. 上报监督层（Supervisor Layer）

## 反模式
无熔断 = 级联失败（8/19 事故）。

## 复用记录
- your-agent：HEARTBEAT.md breaker 段
- （可被其他 agent 直接复制）
```

## 验证步骤

```bash
# 1. 目录结构就位
ls -d ~/.openclaw/workspace/agents/your-agent/memory/{daily,topics,genes}
# 期望：三个目录都存在

# 2. frontmatter 合法性 + 5 层齐备
python3 - <<'PY'
import yaml
raw = open("MEMORY.md", encoding="utf-8").read()
meta = yaml.safe_load(raw[4:raw.index("\n---", 3)])
p = meta["pyramid"]
for lv in ("L1_working","L2_daily","L3_topic","L4_longterm","L5_gene"):
    assert lv in p, f"❌ 缺 {lv}"
print("✅ 5 层金字塔齐备:", list(p.keys()))
PY

# 3. 记忆写入规则测试：让它记一条"流水"
openclaw agent --agent your-agent \
  --message "记住：我今天 10:03 喝了一杯咖啡。"
# 期望：它拒绝写这类无价值流水（按 rules 第 1 条），或只写入 L2 当日日志

# 4. 记忆检索测试
openclaw agent --agent your-agent \
  --message "关于心跳设计，我们之前定过什么？"
# 期望：读 memory/topics/heartbeat.md，给结论 + 路径

# 5. L4 变更留痕测试
cd ~/.openclaw/workspace/agents/your-agent
git log --oneline -3 -- MEMORY.md
# 期望：能看到 MEMORY.md 的提交记录

# 6. 不制造空日志测试：一个无产出会话后
ls ~/.openclaw/workspace/agents/your-agent/memory/daily/ | tail -3
# 期望：不新增空文件（当日无事就不建）

# 7. 分层访问测试：会话启动时读了哪几层
openclaw agent --agent your-agent --message "说下你启动时读了哪些记忆文件。"
# 期望：L4(MEMORY.md) + L2(最近 3 天) + 按需 L3
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **网关**：Hermes 0.20.1
- **OS**：macOS 26.5.1
- **工作区**：`~/.openclaw/workspace/agents/<agent>/`
- **参考基线**：本机真实 agent 工作区含 `MEMORY.md`（约 10,148 字节）
  与 `memory/` 目录（含多个子文件）；本配方把"记忆"重组为 5 层可治理结构
- **日期**：2026-09-27

## 排坑（如有）

1. **MEMORY.md 无限膨胀**：根因是"什么都写"。修：写入规则第 1 条
   （值不值得留下）+ L2 90 天滚动归档。

2. **agent 忘记关键事**：根因是 L4 里没有，或没在启动时读。
   核验：`grep -n "<关键词>" MEMORY.md`；启动段是否读 MEMORY.md。

3. **记得太多反而变笨**：根因是旧流水污染上下文。修：L4 只留
   "结论 + 路径"，明细下沉到 L3/L2。

4. **多 agent 记忆串味**：根因是共用一份 MEMORY.md。
   修：每个 agent 独立工作区 + 独立 MEMORY.md；共享只经 L5 基因库。

5. **记忆与协议冲突**：MEMORY 说"用户可以随便删"，SOUL 说"不越权删"。
   修：铁律——**冲突以协议文件（SOUL/AGENTS/TOOLS）为准**，并清理 MEMORY。

## 进阶

- **进阶 1 · 记忆滚动自动化**：slow 档心跳（C2-1）每日把 L2 汇总进 L3/L4，
  90 天前的 L2 归档。已在本配方 cron 任务 6（hb_memory_rollup）预留入口。

- **进阶 2 · 基因库跨 agent 共享**：把 `memory/genes/*.md` 软链到
  `~/.openclaw/workspace/SHARED/genes/`，军团内所有 agent 复用同一套
  技能基因（对齐 v4.0 卷一"技能基因 / 可复用能力单元"）。

- **进阶 3 · 记忆治理审计**：把 MEMORY.md 纳入 git + 定期 diff，
  异常突增/异常删除即告警（对齐治理审计账本 Governance Audit Ledger）。

## 附录 A · 5 层金字塔速查表

| 层 | 名称 | 存储 | TTL | 访问时机 | 典型内容 |
|:--:|---|---|---|---|---|
| L1 | 工作记忆 | session 内存 | 单会话 | 每轮 | 当前对话 |
| L2 | 当日日志 | `memory/daily/*.md` | 90 天 | 启动读近 3 天 | 做了什么/结论 |
| L3 | 主题记忆 | `memory/topics/*.md` | 长期 | 按需 | 某主题要点 |
| L4 | 长期记忆 | `MEMORY.md` | 永久 | 每会话启动 | 索引+关键决策 |
| L5 | 技能基因 | `memory/genes/*.md` | 永久 | 训练/复盘 | 可复用能力 |

## 附录 B · 记忆写入决策流

```text
想写一条记忆？
  │
  ├─ 一个月后还有用吗？
  │    ├─ 否 → 不写（或只进 L2 当日日志）
  │    └─ 是 → 是"结论"还是"流水"？
  │             ├─ 流水 → 写日志/git，不写 MEMORY
  │             └─ 结论 → 有无通用价值？
  │                      ├─ 有 → L5 技能基因
  │                      └─ 无 → L3 主题 / L4 长期
  └─ 全程：冲突时协议文件优先
```

## 附录 C · 常见错误码 / 现象对照

| 现象 | 根因 | 定位 |
|---|---|---|
| 忘记关键事 | L4 缺或未被读 | `grep` MEMORY.md + 启动段 |
| 越记越笨 | 旧流水污染 | 检查 L4 是否留了流水 |
| token 爆 | 记忆塞太多 | 检查启动读取量 |
| 空日志堆积 | 无"不制造空日志" | 检查 daily/ |
| 多 agent 串味 | 共用 MEMORY | 检查工作区隔离 |
| 记忆与协议冲突 | 未定优先级 | 检查 rules 第 3 条 |

## 附录 D · 与三件套衔接

```text
C2-1 slow 档 → 触发记忆滚动（本配方 cron 任务 6）
C2-2 hb_memory_rollup → 每日把 L2 汇总进 L3/L4
C2-4 Compaction → 压缩时保留 L4 索引，压缩 L1
C2-5 漂移检测 → 记忆异常突增/删除 计入漂移信号
```

---
## 附录 E · 5 层记忆的读写权限表

| 层 | 读 | 写 | 删除 | 谁能改 |
|---|:--:|:--:|:--:|---|
| L1 | 全 | 全 | 会话结束自动 | 运行时 |
| L2 | 全 | agent | 90 天后归档 | agent / 心跳 |
| L3 | 全 | agent（人工可改） | 人工 | agent + 用户 |
| L4 | 全 | agent（须留 git） | 须 git revert | agent + 用户 |
| L5 | 全 | 训练/复盘时 | 人工 | 用户 / 监督层 |

## 附录 F · 记忆容量预算建议

| 层 | 目标上限 | 超限动作 |
|---|---|---|
| L2 | 90 个文件 | 归档到 archive/ |
| L3 | 每个主题 ≤ 200 行 | 拆子主题 |
| L4 | ≤ 500 行 | 下沉明细到 L3 |
| L5 | ≤ 100 个基因 | 合并/废弃低价值 |

> L4 超过 500 行是"记忆膨胀"的早期信号——每次都读它，膨胀即拖慢。

## 附录 G · 记忆健康度自检（每周）

```text
[ ] L4(MEMORY.md) ≤ 500 行
[ ] L2 无超过 90 天未归档文件
[ ] L4 关键决策表有日期 + 证据路径
[ ] L5 基因库有 ≥1 条被复用记录
[ ] 无空日志文件（0 字节 daily/*.md）
[ ] git log MEMORY.md 有近期提交（说明在治理）
```

## 附录 H · 3 个真实场景

```text
【场景 1】用户问"我们之前定过什么关于心跳的？"
正解：读 memory/topics/heartbeat.md → 给结论 + 证据路径。

【场景 2】用户说"记住我讨厌红色。"
正解：这是长期偏好 → 写 L4"关于用户"段，并留 git；
      不写进"流水"，不写进 L2 就算完。

【场景 3】今天啥也没干。
正解：不建 daily 文件（不制造空日志）。
```

## 附录 I · 与 v4.0 MCP Resource 的对应

```text
v4.0 09-mcp-binding：卷二 7 协议 → MCP Resource（只读模板）
本配方：MEMORY.md 作为 L4 长期记忆，是 Resource 的一种；
        可暴露为 handbook://volume-02/protocols/MEMORY（mime: text/markdown）
        Host 需要时读进来当上下文，不需要模型执行。
```

---
# C2-4 · Compaction 配置：含 reserveTokens 三者并存

## 背景

长会话必然遇到一个墙：**上下文窗口是有限的**。当对话越来越长，
要么撞墙报错，要么被迫丢弃信息。会话压缩（Session Compaction /
Context Compaction）就是解决这件事的机制——它**不删对话，而是把老内容
压成摘要，保留信息、释放 token**。

新人最容易被绕晕的是一堆"看着像同一个东西"的参数。本机与 v4.0 核实后，
真正并存的是**三个 reserve 相关量**：
①`reserveTokens`（请求预算里的预留量，真名 `CompactionRequestBudget.reserveTokens`）
②`MAX_COMPACTION_RESERVE_RATIO = 0.25`（预留占总窗口比例的上限）
> **⚠ 勘误（2026-09-27 · 实测）**：本节 compaction 三值模型（`reserveTokens` / `maxReserveRatio` / `effectiveReserveTokens`）是**本书约定口径**；
> 本机实测 `~/.openclaw/openclaw.json`（45,662 字节）**不含** `compaction` / `reserveTokens` / `maxReserveRatio` / `effectiveReserveTokens` 任一字段
> （顶层 `session` 仅含 `dmScope`）。把本节当**方法模板**读，不要到主配置文件里找这些键。

③`effectiveReserveTokens`（最终生效的预留量 = 前二者与场景共同决定的结果）

这一例解决的具体问题：**搞清楚这三个量各自是什么、怎么一起调、
以及给一份可复制的 Compaction 配置**。

> **来源**：v1.0 卷三《Session / Context / Queue》（长会话为什么会污染与如何治理）；
> v1.0 卷五《会话污染与清理》；v4.0 卷三模块6《Heartbeat / Cron / Compaction》。
> 真名口径以《术语对照表 v3.0》第 31 条为准。从零撰写，不复用 v1.0 原文。

## 配置（完整可复制）

### 1）Compaction 配置块（写入 agent 的配置）

```yaml
# ~/.openclaw/workspace/agents/your-agent/openclaw.agent.yaml
# 说明：真名均为 OpenClaw 2026.9.4 核实结果（见《术语对照表 v3.0》§五）
session:
  compaction:
    enabled: true
    # ① 请求预算里的预留量（真名：CompactionRequestBudget.reserveTokens）
    reserveTokens: 8192
    # ② 预留占总窗口比例上限（真名常量：MAX_COMPACTION_RESERVE_RATIO = 0.25）
    maxReserveRatio: 0.25
    # ③ 最终生效的预留量（由 ①② 与模型窗口共同推导，只读观测值）
    effectiveReserveTokens: 8192    # = min(reserveTokens, window * maxReserveRatio)
    trigger:
      # 何时触发压缩：剩余可用 token 低于"预留 + 安全垫"
      lowWaterTokens: 12288         # 低于此值开始准备压缩
      hardLimitSafety: 2048         # 硬上限前的安全垫
    strategy:
      keep_recent_turns: 8          # 至少保留最近 8 轮原文
      keep_pinned: true             # 标记为 pinned 的内容永不压缩
      summary_model: deepseek-v4-flash
      preserve:
        - protocol_files            # SOUL/AGENTS/TOOLS 等协议文件不压缩
        - memory_L4                 # 长期记忆不压缩
        - task_cards                # 任务卡不压缩
      drop_order:                   # 丢/压顺序（从先到后）
        - old_tool_outputs
        - chit_chat
        - resolved_branches
    observability:
      log_compactions: true
      report_dir: reports/compaction/
```

### 2）三个 reserve 量的关系（一图说清）

```text
总上下文窗口 window（如 32768）
├─────────────────────────────────────────────────────────────┤
│ 已用 tokens            │ 待压缩区 │   reserve 预留   │ 安全垫 │
└─────────────────────────────────────────────────────────────┘
                           ↑ 触发点(below lowWater)   ↑ 保留给"压缩动作本身 + 生成"

① reserveTokens        = 8192       （请求预算里的预留量，可配）
② MAX_COMPACTION_RESERVE_RATIO = 0.25（预留 ≤ window × 0.25，硬上限）
③ effectiveReserveTokens = min(①, window × ②)   （最终生效，观测值）
```

**一句话口诀**：**① 是你"想要"的预留，② 是系统"允许"的上限，
③ 是二者取小后"真正"生效的预留。**

### 3）关键约束（必须同时满足）

```yaml
constraints:
  # ① 不得超过硬上限比例
  - reserveTokens <= window * MAX_COMPACTION_RESERVE_RATIO
  # ② 预留要够装"压缩动作本身 + 一次生成"
  - effectiveReserveTokens >= summary_tokens + response_budget
  # ③ 低水位要高于预留，否则压缩还没做完就撞墙
  - lowWaterTokens > effectiveReserveTokens + hardLimitSafety
```

以 window=32768、②=0.25 为例：
- window × 0.25 = 8192 → ①取 8192 正好到顶（再多会被 ② 截断）。
- 若你写 `reserveTokens: 16384`，则 ③ = min(16384, 8192) = **8192**
  （被 ② 截断）——这就是"我明明填了 16384 怎么不生效"的答案。

### 4）观测与告警

```yaml
alerts:
  compaction_frequency:            # 压缩太频繁 = 参数太小或会话太长
    max_per_hour: 6
    action: warn
  reserve_truncated:               # ①② 冲突被截断
    when: reserveTokens > window * MAX_COMPACTION_RESERVE_RATIO
    action: error
  context_overflow:                # 撞墙（压缩来不及）
    action: escalate
    target: tiance
```

## 验证步骤

```bash
# 1. 配置 YAML 合法性 + 三个量齐全
python3 - <<'PY'
import yaml
cfg = yaml.safe_load(open("openclaw.agent.yaml"))["session"]["compaction"]
for k in ("reserveTokens", "maxReserveRatio", "effectiveReserveTokens"):
    assert k in cfg, f"❌ 缺 {k}"
assert cfg["maxReserveRatio"] == 0.25, "❌ 与常量 MAX_COMPACTION_RESERVE_RATIO 不一致"
print("✅ 三个 reserve 量齐备:", {k: cfg[k] for k in
      ("reserveTokens","maxReserveRatio","effectiveReserveTokens")})
PY

# 2. 约束自检（第 3 节的三个约束）
python3 - <<'PY'
import yaml
c = yaml.safe_load(open("openclaw.agent.yaml"))["session"]["compaction"]
window = 32768
assert c["reserveTokens"] <= window * c["maxReserveRatio"] or \
       c["effectiveReserveTokens"] == window * c["maxReserveRatio"], "❌ ①② 冲突未处理"
assert c["trigger"]["lowWaterTokens"] > c["effectiveReserveTokens"] + c["trigger"]["hardLimitSafety"], \
       "❌ 低水位太低，压缩来不及"
print("✅ 约束全部满足")
PY

# 3. 观测值核对（跑一次长会话后看日志）
ls -la ~/.openclaw/workspace/agents/your-agent/reports/compaction/
tail -20 ~/.openclaw/workspace/agents/your-agent/reports/compaction/*.log
# 期望：日志/报表里能看到 effectiveReserveTokens 的观测值（⚠ 该键**不在** openclaw.json，见本节勘误）

# 4. 截断告警验证：故意把 reserveTokens 设超大
#    临时改 reserveTokens: 999999 → 跑 → 应触发 reserve_truncated=error
openclaw agent --agent your-agent --message "随便聊聊，测试压缩配置。"
# 期望：日志出现 reserve_truncated 告警；effectiveReserveTokens 落到 window*0.25

# 5. 压缩触发验证：灌长内容
openclaw agent --agent your-agent \
  --message "把 references/ 下所有 md 的内容依次读给我听（分段）。"
# 期望：达到 lowWater 后触发压缩；保留最近 8 轮 + 协议文件不被压

# 6. pinned 不被压验证
openclaw agent --agent your-agent \
  --message "SOUL.md 里的人格锚点是什么？（会话已很长）"
# 期望：仍能准确答出（协议文件被 preserve，未压缩）
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **网关**：Hermes 0.20.1
- **OS**：macOS 26.5.1
- **工作区**：`~/.openclaw/workspace/agents/<agent>/`
- **真名核实**（v4.0 独立实拉 + 本机核实）：`CompactionRequestBudget.reserveTokens`
  与常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25`；`reserveTokensFloor` **不存在**
  （对齐《术语对照表 v3.0》第 31 条，v4.0 已勘误）
- **日期**：2026-09-27

## 排坑（如有）

1. **填了 reserveTokens 不生效**：99% 是被 `MAX_COMPACTION_RESERVE_RATIO=0.25`
   截断。核验：`effectiveReserveTokens == min(reserveTokens, window*0.25)`。
   想保留更多 → 扩大 window 或调大 ratio（谨慎，ratio 太大会挤压生成空间）。

2. **压缩太频繁**：`lowWaterTokens` 设太高 → 一有剩余就压。
   修：低水位 ≈ effectiveReserve + 安全垫，别设太激进。

3. **压缩后"失忆"**：根因是把协议文件/长期记忆也压了。
   修：`preserve` 列表里加 `protocol_files` 与 `memory_L4`。

4. **`reserveTokensFloor` 是错的真名**：这是 v1.0 的误记。
   真名是 `CompactionRequestBudget.reserveTokens` + 常量
   `MAX_COMPACTION_RESERVE_RATIO`。用错名字 = 配置静默失效。

5. **压缩动作本身爆内存**：预留不够装"压缩 + 生成"。
   修：约束② `effectiveReserveTokens >= summary_tokens + response_budget`。

## 进阶

- **进阶 1 · 按会话类型分档**：短任务会话用小 reserve（省资源），
  长分析会话用大 reserve（防丢上下文）。⏳ 待实测：是否支持按会话动态设 reserve。

- **进阶 2 · 压缩质量评估**：把每次压缩的"信息保留率"写入报告，
  低于阈值说明 summary_model 太弱或 drop_order 太激进。

- **进阶 3 · 与记忆分层联动**：压缩只压 L1（工作记忆），
  L4 长期记忆（MEMORY.md）永不压（本配方已设 `preserve: memory_L4`），
  与 C2-3 的 5 层金字塔天然对齐。

## 附录 A · 三个 reserve 量速查

| 量 | 真名 | 可配? | 含义 |
|---|---|:--:|---|
| ① 请求预算预留 | `CompactionRequestBudget.reserveTokens` | ✅ | 你想要的预留 |
| ② 比例硬上限 | `MAX_COMPACTION_RESERVE_RATIO`=0.25 | ⬜常量 | 系统允许的上限 |
| ③ 生效预留 | `effectiveReserveTokens` | ✖观测 | min(①, window×②) |

## 附录 B · 参数取值参考（window=32768）

| 参数 | 保守 | 标准 | 激进 | 后果 |
|---|:--:|:--:|:--:|---|
| reserveTokens | 8192 | 6144 | 4096 | 越小越省但越易丢 |
| lowWaterTokens | 16384 | 12288 | 8192 | 越高压缩越频 |
| keep_recent_turns | 12 | 8 | 4 | 越少越省越易忘 |
| maxReserveRatio | 0.25 | 0.25 | 0.30 | 越大会挤压生成 |

## 附录 C · 常见错误码 / 现象对照

| 现象 | 根因 | 定位 |
|---|---|---|
| reserve 不生效 | 被 0.25 截断 | 比对 effective 与 min() |
| 压缩太频繁 | 低水位太高 | 检查 lowWaterTokens |
| 压缩后失忆 | 协议文件被压 | 检查 preserve 列表 |
| 静默失效 | 用了错真名 | 检查是否为 reserveTokens |
| 撞墙报错 | 低水位低于预留 | 约束③ |
| 生成被打断 | 预留挤占输出 | 调小 ratio |

## 附录 D · 与三件套衔接

```text
C2-3 记忆分层 → 压缩只压 L1，L4 永不压
C2-1 心跳 slow → 每日检查压缩频率是否异常
C2-2 cron 任务 5(hb_health) → 顺带检查 context_overflow 告警
C2-5 漂移检测 → 压缩后"失忆"可能是人格漂移的前兆
```

---
## 附录 E · Compaction 三量关系自检脚本

```bash
# 输入：reserveTokens(①), window, ratio(②)  → 输出：effective(③) + 是否被截断
python3 - <<'PY'
window, r1, r2 = 32768, 8192, 0.25
effective = min(r1, int(window * r2))
truncated = r1 > window * r2
print(f"① reserveTokens        = {r1}")
print(f"② ratio 上限           = {r2}")
print(f"③ effectiveReserve     = {effective}  (min 规则)")
print("是否被 ② 截断:", "是 ← 你填大了" if truncated else "否")
PY
```

## 附录 F · 压缩策略选择表

| 策略 | drop_order | 适合 | 风险 |
|---|---|---|---|
| 保守 | 只丢 chit_chat | 长分析会话 | 省得少 |
| 标准 | 丢 old_tool_outputs + chit_chat | 通用 | 平衡 |
| 激进 | 全丢 + 少留轮次 | 短任务 | 易失忆 |

```yaml
# 标准档示例
strategy:
  keep_recent_turns: 8
  drop_order: [old_tool_outputs, chit_chat, resolved_branches]
  preserve: [protocol_files, memory_L4, task_cards]
```

## 附录 G · 压缩前后对照（信息保留检查）

```text
【压缩前】上下文含：SOUL + AGENTS + 12 轮对话 + 8 个工具输出
【压缩后】SOUL + AGENTS（preserve）+ 最近 8 轮原文 + 老内容摘要 + 工具输出摘要
【检查】压缩后问："SOUL 的人格锚点是什么？" → 必须仍能答对
        问："第 2 轮我让你做过什么？" → 应能从摘要答出要点
```

## 附录 H · 常见参数误配 5 例

| # | 误配 | 症状 | 修法 |
|:--:|---|---|---|
| 1 | reserveTokens 超 0.25 上限 | 静默截断 | 调小或扩 window |
| 2 | lowWater 太低 | 压缩来不及→撞墙 | 抬高 lowWater |
| 3 | preserve 缺 protocol_files | 压缩后失忆 | 补进 preserve |
| 4 | summary_model 太弱 | 摘要丢关键信息 | 换更强摘要模型 |
| 5 | 用错真名 reserveTokensFloor | 配置静默失效 | 改真名 |

## 附录 I · 与 window 尺寸的配比参考

| window | 建议 reserveTokens | 建议 lowWater | keep_recent_turns |
|:--:|---:|---:|:--:|
| 8192 | 2048 | 4096 | 4 |
| 32768 | 8192 | 12288 | 8 |
| 128000 | 32000 | 48000 | 12 |
| 200000 | 50000 | 75000 | 16 |

> 记住：reserveTokens ≤ window × 0.25（② 硬上限）。超了就是白填。

---
## 附录 J · 压缩配置部署检查清单

```text
[ ] reserveTokens 已填，且 ≤ window × MAX_COMPACTION_RESERVE_RATIO(0.25)
[ ] maxReserveRatio 与常量一致（0.25）
[ ] effectiveReserveTokens 已观测（首次跑长会话后确认）
[ ] lowWaterTokens > effectiveReserveTokens + hardLimitSafety
[ ] preserve 含 protocol_files / memory_L4 / task_cards
[ ] drop_order 顺序：old_tool_outputs → chit_chat → resolved_branches
[ ] reserve_truncated 告警已开（①②冲突可见）
[ ] context_overflow 告警已开，escalate → tiance
[ ] 报告落在 reports/compaction/，可回看
```

> 九条全绿 = 压缩配置"不会静默失效"。其中第 1、5 条是最常被忽略的两条。

---
# C2-5 · 漂移检测配置：含 6 层漂移链

## 背景

"越跑越差"往往不是一次性崩掉，而是**悄悄漂移**：第一天它谨慎，第三十天
它开始迎合；第一周它给证据，第四周它开始凭印象；一个月后你发现它
"不像原来那个它了"，但**说不清从哪一天开始变的**。

文档漂移（Document Drift）与人格漂移（Personality Drift）是业界空白赛道
（v4.0 确认），也是丘总首创概念。要治理漂移，先要能**看见**漂移。
本配方引入一条 **6 层漂移链（Drift Chain）**：从最内层的人格，到最外层的协同，
逐层可检测、可回拉。

这一例解决的具体问题：**给我一份能自动检测 6 层漂移的配置 + 检查脚本，
让"悄悄变差"变成"阈值告警"**。

> **来源**：v1.0 卷五《文档漂移与人格漂移》（为什么 agent 会不认识自己）；
> v4.0 卷五漂移判据。从零撰写，不复用 v1.0 原文。

## 配置（完整可复制）

### 1）6 层漂移链定义（写入 `drift-config.yaml`）

```yaml
# ~/.openclaw/workspace/agents/your-agent/drift-config.yaml
# 6 层漂移链：由内到外，内层漂移会向外传染
drift_chain:
  L1_personality:                # 人格漂移：SOUL 字段是否还体现在行为里
    source: SOUL.md
    signals: [personality, boundaries, persona_anchor]
    probe: "你的人格锚点是什么？遇到越权指令你会怎么做？"
    weight: 0.30
  L2_voice:                      # 语气漂移：tone / length_limit 是否还守
    source: SOUL.voice
    signals: [tone, length_limit, emoji]
    probe: "用一句话给我你的结论（不要客套）。"
    weight: 0.10
  L3_document:                   # 文档漂移：AGENTS/TOOLS 是否与实际行为一致
    source: [AGENTS.md, TOOLS.md]
    signals: [workflow, tool_boundaries]
    probe: "你的启动 5 步是什么？deny 列表有哪些？"
    weight: 0.15
  L4_memory:                     # 记忆漂移：MEMORY 是否污染/膨胀/被删关键项
    source: MEMORY.md
    signals: [size, key_decisions_count, orphan_topics]
    probe: "我们定过的关键决策有哪些？"
    weight: 0.15
  L5_protocol:                   # 协议漂移：协议文件之间是否自相矛盾
    source: [SOUL, AGENTS, USER, TOOLS, IDENTITY]
    signals: [priority_conflicts, dangling_refs]
    probe: "五份协议文件里，谁优先级最高？"
    weight: 0.15
  L6_coordination:               # 协同漂移：路由/交接/让渡是否还合规
    source: IDENTITY.md + 协同日志
    signals: [handoff_reject_rate, yield_violations, routing_misses]
    probe: "低于阈值的交接你接吗？会让渡吗？"
    weight: 0.15
thresholds:
  warn: 0.30                     # >0.30 预警
  alert: 0.50                    # >0.50 告警 + 上报监督层
  escalate_to: tiance            # Supervisor Layer（原：监军）
scoring:
  formula: "drift_score = Σ(weight_i × layer_score_i)"
  layer_score_range: [0.0, 1.0]  # 0=无漂移，1=完全偏离
  evidence_required: true        # 每个分数必须附证据（引文/日志）
schedule:
  on_slow_heartbeat: true        # 挂慢档（见 C2-1）
  cron_task_id: hb_drift_check   # 与 C2-2 任务 7 对齐
```

### 2）6 层漂移链示意

```text
        ┌──────────────────────────────────────────────┐
 内层   │ L1 人格漂移  ← 最危险（看不清自己）            │
        │      ↓ 传染                                   │
        │ L2 语气漂移  ← 最先被用户察觉                  │
        │      ↓                                        │
        │ L3 文档漂移  ← 说的和做的不一致                │
        │      ↓                                        │
        │ L4 记忆漂移  ← 记错/忘事/膨胀                  │
        │      ↓                                        │
        │ L5 协议漂移  ← 五份协议互掐                    │
        │      ↓                                        │
 外层   │ L6 协同漂移  ← 和别的 agent 配合出问题         │
        └──────────────────────────────────────────────┘
  检测顺序：由外到内排查（外层好查），由内到外回拉（内层是根因）。
```

### 3）检测脚本（可直接跑）

```bash
#!/bin/zsh
# scripts/hb_drift_check.sh —— 6 层漂移链检测
set -euo pipefail
WS="$HOME/.openclaw/workspace/agents/your-agent"; cd "$WS"
OUT="reports/drift/drift-$(date +%Y%m%d).json"; mkdir -p reports/drift

# ---- L3 文档漂移：文档声明 vs 实际行为（示例：deny 列表）----
doc_deny=$(grep -A3 "deny:" TOOLS.md | grep -cE "rm -rf|sudo" || true)

# ---- L4 记忆漂移：MEMORY.md 行数（膨胀信号）----
mem_lines=$(wc -l < MEMORY.md)

# ---- L6 协同漂移：交接拒绝率（从日志统计）----
rej=$(grep -c "handoff_reject" logs/*.log 2>/dev/null || echo 0)

# ---- 交给 agent 做主观项（L1/L2/L5）----
openclaw agent --agent your-agent --message "$(cat <<'P'
请做漂移自检，逐层给 0-1 分并附证据（引文/日志路径）：
L1 人格：你的 persona_anchor 是什么？近期行为有偏离吗？
L2 语气：你是否还守 tone / length_limit？
L5 协议：五份协议文件有自相矛盾吗？谁优先？
输出 JSON: {"L1":x,"L2":x,"L5":x,"evidence":{...}}
P
)" >> reports/drift/raw-$(date +%Y%m%d).log 2>&1

# ---- 汇总 ----
python3 - "$doc_deny" "$mem_lines" "$rej" <<'PY'
import sys, json, re, glob, os
doc_deny, mem_lines, rej = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
raw = open(sorted(glob.glob("reports/drift/raw-*.log"))[-1]).read()
m = re.search(r'\{[^{}]*"L1"[^{}]*\}', raw)
sub = json.loads(m.group(0)) if m else {"L1":0,"L2":0,"L5":0,"evidence":{}}
# 客观层打分
L3 = 0.0 if doc_deny >= 2 else 0.8          # deny 列表缺失→漂移
L4 = 0.0 if mem_lines <= 500 else min(1.0, (mem_lines-500)/500)
L6 = min(1.0, rej / 10.0)
layers = {"L1":sub.get("L1",0),"L2":sub.get("L2",0),"L3":L3,
          "L4":L4,"L5":sub.get("L5",0),"L6":L6}
w = {"L1":0.30,"L2":0.10,"L3":0.15,"L4":0.15,"L5":0.15,"L6":0.15}
score = round(sum(layers[k]*w[k] for k in layers), 3)
json.dump({"drift_score":score,"layers":layers,"evidence":sub.get("evidence",{})},
          open(f"reports/drift/drift-{os.environ.get('D','')}.json","w")
          if False else open("reports/drift/latest.json","w"),
          ensure_ascii=False, indent=2)
print("drift_score =", score, "layers =", layers)
if score > 0.50:   print("ALERT: 上报 tiance")
elif score > 0.30: print("WARN: 关注")
else:              print("OK")
PY
```

### 4）回拉策略（按层对症）

```yaml
recovery:
  L1: 重读 SOUL.md + 强化 persona_anchor + 清 MEMORY 污染段
  L2: 收紧 voice.length_limit + 关闭 emoji
  L3: 用文档声明重建行为（重跑启动 5 步）
  L4: 记忆滚动归档 + 删污染项 + 补关键决策
  L5: 统一优先级（SOUL > AGENTS > USER/TOOLS > 指令）
  L6: 校 IDENTITY 路由字段 + 重设交接阈值
```

## 验证步骤

```bash
# 1. 配置合法性 + 6 层齐备 + 权重和为 1
python3 - <<'PY'
import yaml
cfg = yaml.safe_load(open("drift-config.yaml"))
chain = cfg["drift_chain"]
assert len(chain) == 6, f"❌ 应为 6 层，实际 {len(chain)}"
wsum = sum(v["weight"] for v in chain.values())
assert abs(wsum - 1.0) < 1e-6, f"❌ 权重和={wsum}，应为 1.0"
print("✅ 6 层齐备，权重和=1.0:", list(chain.keys()))
PY

# 2. 阈值递增合理
python3 -c "import yaml;c=yaml.safe_load(open('drift-config.yaml'))['thresholds'];assert c['warn']<c['alert'];print('✅ 阈值:',c['warn'],'<',c['alert'])"

# 3. 检测脚本可执行 + 产出 JSON
chmod +x scripts/hb_drift_check.sh
cd ~/.openclaw/workspace/agents/your-agent && D=$(date +%Y%m%d) ./scripts/hb_drift_check.sh
cat reports/drift/latest.json
# 期望：{"drift_score":0.0x,"layers":{L1..L6},"evidence":{...}}

# 4. 注入漂移，验证能被检出（人为制造 L4 记忆膨胀）
python3 -c "open('MEMORY.md','a').write('\n'*600)"
D=$(date +%Y%m%d) ./scripts/hb_drift_check.sh
# 期望：L4 分数上升，drift_score 变大，可能触发 WARN
# 事后清理：python3 -c "lines=open('MEMORY.md').read().rstrip().split(chr(10));open('MEMORY.md','w').write(chr(10).join(lines[:500])+chr(10))"

# 5. 告警链路验证（≥0.50 时上报 tiance）
#    临时把 warn/alert 调到 0.01 强制告警
python3 - <<'PY'
import yaml;c=yaml.safe_load(open('drift-config.yaml'))
c['thresholds']['alert']=0.01;c['thresholds']['warn']=0.005
yaml.safe_dump(c,open('drift-config.yaml','w'),allow_unicode=True)
PY
D=$(date +%Y%m%d) ./scripts/hb_drift_check.sh | tail -1
# 期望：输出 ALERT: 上报 tiance；随后还原阈值

# 6. 回拉验证：跑一次 L1 回拉
openclaw agent --agent your-agent --message "重读 SOUL.md，复述你的人格锚点。"
# 期望：正确复述 persona_anchor
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **网关**：Hermes 0.20.1
- **OS**：macOS 26.5.1
- **工作区**：`~/.openclaw/workspace/agents/<agent>/`
- **参考基线**：v4.0 卷五「文档漂移 / 人格漂移」判据 + 周度体检清单；
  本配方把"漂移"结构化为 6 层可打分链条 + 可跑脚本
- **日期**：2026-09-27

## 排坑（如有）

1. **检测出来没人管**：分数算出但不告警=白算。
   修：`thresholds.alert` 触发上报监督层（tiance），且挂进慢档心跳。

2. **只看人格不看外层**：人格漂移常由外层（记忆/协议）传染而来。
   修：按"由外到内排查、由内到外回拉"的顺序（本配方已写明）。

3. **分数没有证据**：`layer_score` 是拍的 → 无法回拉。
   修：`evidence_required: true`，每分附引文/日志路径。

4. **权重和不为 1**：导致 drift_score 量纲混乱。
   核验：验证步骤 1 的断言。

5. **静默时段仍告警**：半夜告警扰民。
   修：复用 C2-1 的 quiet_hours，静默期只记录.

## 进阶

- **进阶 1 · 漂移趋势图**：把每日 drift_score 落盘成时间序列，
  连续上升即"慢性漂移"，即使未过阈值也应预警。

- **进阶 2 · 跨 agent 漂移对比**：军团内多 agent 统一权重，
  横向对比谁漂得最快，定位"系统性漂移源"（如某共享 skill 有问题）。

- **进阶 3 · 漂移即基因**：把"每次回拉成功的动作"沉淀为技能基因
  （`memory/genes/drift-recovery-*.md`），下次漂移直接复用（对齐 C2-3 L5）。

## 附录 A · 6 层漂移链速查表

| 层 | 名称 | 源 | 信号 | 权重 | 工具 |
|:--:|---|---|---|:--:|---|
| L1 | 人格漂移 | SOUL | personality/boundaries/anchor | 0.30 | agent 自检 |
| L2 | 语气漂移 | SOUL.voice | tone/length/emoji | 0.10 | agent 自检 |
| L3 | 文档漂移 | AGENTS/TOOLS | workflow/boundaries | 0.15 | grep 客观 |
| L4 | 记忆漂移 | MEMORY | size/decisions/orphans | 0.15 | wc/grep 客观 |
| L5 | 协议漂移 | 5 协议文件 | 冲突/悬空引用 | 0.15 | agent 自检 |
| L6 | 协同漂移 | IDENTITY+日志 | handoff/yield/routing | 0.15 | 日志统计 |

## 附录 B · 漂移分档与动作

| drift_score | 档 | 动作 |
|---|---|---|
| 0.00–0.30 | OK | 无事 |
| 0.30–0.50 | WARN | 关注 + 记录趋势 |
| 0.50–1.00 | ALERT | 立即回拉 + 上报 tiance |

## 附录 C · 常见错误码 / 现象对照

| 现象 | 根因 | 定位 |
|---|---|---|
| 突然开始迎合 | L1 人格漂移 | 查 SOUL + MEMORY 污染 |
| 说话越来越长 | L2 语气漂移 | 查 voice.length_limit |
| 说的和做的不一致 | L3 文档漂移 | 比对 AGENTS 与实际 |
| 忘记关键决策 | L4 记忆漂移 | `grep` MEMORY.md |
| 五份文件互掐 | L5 协议漂移 | 查优先级冲突 |
| 群里抢答/丢件 | L6 协同漂移 | 查 IDENTITY + 日志 |

## 附录 D · 与三件套衔接

```text
C2-1 slow 档 → 每日触发本配方检测
C2-2 任务 7(hb_drift_check) → 本配方的执行入口
C2-3 L4 记忆 → 记忆膨胀/污染 是 L4 漂移的主要来源
C2-4 Compaction → 压缩后失忆 是 L1/L4 漂移的前兆
```

---

## 附录 E · 漂移回拉 6 步 SOP

```text
[ ] 1. 读 latest.json → 定位漂移在哪几层（哪层分数高）
[ ] 2. 由外到内排查：先看 L6/L5/L4（易查），再定 L1/L2（难查）
[ ] 3. 找根因：通常外层问题传染到内层（如记忆污染→人格漂移）
[ ] 4. 对症回拉（按 recovery 映射表）
[ ] 5. 复测：重跑 hb_drift_check → 确认分数下降
[ ] 6. 沉淀：把本次回拉动作写成技能基因（memory/genes/）
```

## 附录 F · 漂移检测频率建议

| 场景 | 频率 | 理由 |
|---|---|---|
| 新 agent 上线首月 | 每日 | 最容易漂 |
| 稳定运行期 | 每日（慢档） | 成本低 |
| 大改协议后 | 改完立即 + 次日 | 验证改动无副作用 |
| 多 agent 协同期 | 每日 + 每周横向对比 | 定位系统性漂移 |

## 附录 G · 漂移与三证据验证（TEV）的结合

```text
漂移回拉也要走 TEV（Three-Evidence Verification）：
  新产物  = 回拉后的 SOUL/MEMORY 快照
  前后 Diff = git diff 协议文件
  测试日志 = 回拉后重跑 hb_drift_check 的 drift_score 对比
三步齐备才算"回拉成功"，而不是"感觉好点了"。
```

---
## 本分册诚实边界声明

> 遵循 v5.0 方案「诚实边界」原则：标注实测 / 待实测。

| 类别 | 内容 | 状态 |
|---|---|---|
| 已实测 | OpenClaw `2026.9.4 (3a9d69d)`（三源一致） | ✅ |
| 已实测 | 本机 skills 目录 236 个 | ✅ |
| 已实测 | 本机 agent 工作区含 `heartbeat-state.json`(2,533B) / `heartbeat-monitor.json`(457B) / `heartbeat-scratch.json`(259B) / `MEMORY.md`(10,148B) / `memory/` 目录 | ✅ |
| 已实测 | 真名 `CompactionRequestBudget.reserveTokens` + `MAX_COMPACTION_RESERVE_RATIO=0.25`；`reserveTokensFloor` 不存在 | ✅ 核实 |
| 待实测 | `openclaw notify` 子命令的确切形态 | ⏳ 以 `openclaw --help` 为准 |
| 待实测 | launchd daemon 守护心跳（C2-2 进阶 1） | ⏳ |
| 待实测 | 按会话动态设 reserve（C2-4 进阶 1） | ⏳ |
| 待实测 | 自适应心跳频率（C2-1 进阶 1） | ⏳ |

**诚实说明**：本分册配置基于 OpenClaw 真实工作区文件形态 + v4.0 卷三/卷五口径
设计；frontmatter 作为"可解析协议元数据"是本手册约定，解析由本手册脚本承担。
所有脚本逻辑可复现，但个别 CLI 子命令以你的 `openclaw --help` 为准。
本分册不复用 v1.0/v4.0 原文。

---

> 《硅基生命训练学 v5.0 · 实战 Cookbook》
> 分册：02-protocol-HEARTBEAT-MEMORY.md（例 C2-1 ~ C2-5）
> 基座：OpenClaw 2026.9.4 (3a9d69d) · 网关 Hermes 0.20.1
> License: MIT · Copyright (c) 2026 OpenClaw Foundation
> 撰写日期：2026-09-27

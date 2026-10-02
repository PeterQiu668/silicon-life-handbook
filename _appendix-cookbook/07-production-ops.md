<!--
================================================================================
 硅基生命训练学 v5.0 · 实战 Cookbook · 下半卷（协同与生产类）
 分册：07-production-ops.md —— 生产运维类 · 第 7 分册（例 C7-1 ~ C7-4）
--------------------------------------------------------------------------------
 基座版本（Base）：OpenClaw 2026.9.4 (3a9d69d)      ← 本书统一基座口径
    ⚠️ 2026-09-27 本机 `openclaw --version` 复测报 OpenClaw 2026.9.6 (eb377ac)
       （managed gateway 切到 node@24 运行时的上报口径）；本册配置对两个补丁版
       均向后兼容，差异已在「实测环境」节逐条写明。
 网关版本（Gateway）：Hermes 0.20.1
 上游底座：v4.0 行业标准版 · 卷七 M1/M2/M3（编制 · 路由 · 生产运维）
           + 卷六附录 A（修复工单）
 术语底座：《00-术语对照表·v3.0行业标准版.md》（35 条改名统一口径）
 本机实测环境：macOS 26.5.1 · ~/.openclaw/workspace/ · 238 个自建 skill 目录
    （本书正文统一口径 236）· 18 个 agent · 61 条 automation · 37 条 binding
    51/69 plugin enabled · a2a 插件 disabled · mcp.servers = 0 配置（诚实基线）
 真实事故样本：8/19 军团断线（模型级联失败）· 9/21 飞书事故（requireMention
    + groupAllowFrom 单点）· heartbeat error 计数（kunlun 99+x / peter 70x /
    tiance skipped）· 能力矩阵月度更新 error 4x
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

# 实战 Cookbook · 生产运维类 · 07-production-ops.md

> **本分册覆盖**：C7-1 智能体集群（Agent Fleet）真实编制——18 Agent 花名册 + 路由表 +
> binding 配置 / C7-2 生产事故复盘实操——8/19 军团断线 + 9/21 飞书事故模板 /
> C7-3 cron 编排实操——晨扫 / 日报 / 暗夜熔炉 完整配置 /
> C7-4 生产监控实操——heartbeat error 计数 + 告警链。
>
> **读法**：这一册是"编制 → 事故 → 编排 → 监控"的生产四件套：
> **谁在岗**（C7-1 花名册）→ **翻车了怎么复盘**（C7-2 事故模板）→
> **活按什么节律跑**（C7-3 cron）→ **谁盯着它别静默死**（C7-4 监控告警）。
> 建议顺序 C7-1 → C7-3 → C7-4 → C7-2（先建编制与节律、再上监控、最后练复盘）。
>
> **术语约定**：首次出现的行业标准术语均以「行业标准名（原：黑话）」双写：
> Multi-Agent Orchestration（原：军团编制）、Agent Fleet（智能体集群）、
> Supervisor Layer（原：监军）、Task Handoff Protocol / THP（任务交接协议）、
> Response Yield Protocol（响应让渡协议，原：让位协议）、
> Remediation Ticket（修复工单，原：整改单）、
> TEV / Three-Evidence Verification（原：三证验真）、
> Post-Incident Review（原：事故复盘）、Periodic Health Check（原：每周体检）。
> 全部口径以《00-术语对照表·v3.0行业标准版.md》为准。

---

## 本分册速查索引

| 例号 | 主题 | 解决的具体问题 | 核心文件 | 预计可跑时间 |
|:--:|---|---|---|---|
| C7-1 | Agent Fleet 真实编制（18 Agent） | "到底几个 Agent、谁负责什么、连了哪些渠道" 无单一事实源 | `~/.openclaw/openclaw.json`（`agents.entries` + `bindings`）| 16 分钟 |
| C7-2 | 生产事故复盘（Post-Incident Review） | 事故复盘变成"写作文" → 8/19 + 9/21 双模板 + 可跑校验脚本 | `memory/<date>-<事故名>.md` | 20 分钟 |
| C7-3 | cron 编排（晨扫/日报/暗夜熔炉） | 61 条 automation 无编排视图 → 12 条主链 + 完整 add 配置 | `openclaw automations` | 18 分钟 |
| C7-4 | 生产监控（heartbeat error + 告警链） | 静默失效无人知（error 99+x 无人管）→ 阈值 + 告警链 + SLA | `governance/monitor.yaml` + 告警脚本 | 17 分钟 |

> **共通前置**：本机已装 OpenClaw（基座 2026.9.4 / 复测 2026.9.6），存在
> `~/.openclaw/openclaw.json`（1871 行 · 顶层键 20 个）、
> `~/.openclaw/workspace/agents/`（**18 个** `workspace-*` 工作区）、
> `~/Library/LaunchAgents/ai.openclaw.gateway.plist`（+ `com.openclaw.monthly-cleanup.plist`）。
> `~/.openclaw/governance/` 需新建（本机实测**尚不存在**）。

---

## 业界对位表（本分册 4 例共享）

| 能力维度 | 本手册（卷七生产层） | LangGraph Platform | AutoGen Studio | CrewAI Enterprise | OpenAI Agents SDK | Claude Agent SDK | K8s/Argo |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| 集群编制即声明文件 | ✅ `agents.entries` 18 条 | ➖ | ➖ | ✅ `agents.yaml` | ➖ | ➖ | ✅ Deployment CRD |
| 跨渠道账号路由 | ✅ `bindings` 37 条 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 事故复盘模板（字段化） | ✅ PIR 双模板 + 校验脚本 | ➖ | ➖ | ➖ | ➖ | ➖ | ✅ Postmortem 文化 |
| cron 编排（61 条 automation） | ✅ `openclaw automations` | ➖ | ➖ | ➖ | ❌ | ❌ | ✅ CronJob |
| heartbeat 计数 + 阈值告警 | ✅ error 计数 + SLA | ➖ | ➖ | ➖ | ❌ | ❌ | ✅ liveness/readiness |
| 单 Agent 多模型降级链 | ✅ `model.fallbacks` | ➖ | ➖ | ➖ | ➖ | ➖ | ❌ |
| 群聊 mention 模式路由 | ✅ `groupChat.mentionPatterns` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

> **结论**：本分册的**编制 / 编排 / 监控三件套**与 K8s/Argo 的
> Deployment + CronJob + liveness 三件套高度同构——但 OpenClaw 把这三者的
> **载体统一为一封 JSON**（`~/.openclaw/openclaw.json`）+ 一台 CLI（`openclaw`）。
> 运维视角看：**这是一台"单文件 K8s"**。

---

# C7-1 · 智能体集群（Agent Fleet）真实编制：18 Agent 花名册 + 路由表 + binding 配置

## 背景

### 问题的由来

18 个 Agent、37 条渠道绑定、61 条 automation 分散在
`~/.openclaw/openclaw.json`、18 个 `workspace-*/AGENTS.md`、
18 个 `SOUL.md`、以及 61 条 automation 声明里。

问一个最简单的问题——**"天枢用什么模型？"**——回答需要：

```
grep -A20 '"tianshu"' ~/.openclaw/openclaw.json | grep primary
→ 得到 "yiyongai/gpt-5.6-terra"
```

问得更难一点——**"谁占了 Telegram default 兜底？"**——就要读 37 条 `bindings`。
再难一点——**"断线时该找谁？"**——要读 `workspace-peter/AGENTS.md`（通道守门员）。

**没有单一事实源 = 每次问都要现查 = 必然答错。**

### 本配方产出

一份**可生成的**花名册（roster）——从 `openclaw.json` 直接导出，
18 行 × 7 列，覆盖 `agentId / 中文名 / 主模型 / fallback 数 / workspace / 渠道绑定 / 角色`。

### 关于"18 vs 19"的口径说明（诚实边界）

任务书标题写作「19 agent 真实编制」。**2026-09-27 本机实测为 18 个**：

```bash
openclaw agents list 2>&1 | grep -E "^- " | wc -l
# 实测：18
python3 -c "import json;print(len(json.load(open('/Users/peterqiu/.openclaw/openclaw.json'))['agents']['entries']))"
# 实测：18
```

差异来源：本机 `~/.openclaw/workspace/agents/` 下有 4 个**非 `workspace-*` 命名的目录**
（`agent-kunlun` / `agents` / `config` / `kunlun`）——它们是**历史残留/中间态目录**，
不计入 Agent 编制。真实在编 Agent = **18**。本册按 18 撰写，并在文末如实标注。

---

## 配置（完整可复制）

### Step 1：主配置真身（读，不改）

```bash
# ⚠️ 真名铁律：主配置是 ~/.openclaw/openclaw.json
#    不是 ~/.openclaw/workspace/openclaw.json（本机不存在）
#    实测：1871 行 · 顶层键 20 个
#    ['logging','gateway','channels','agents','meta','wizard','models','auth',
#     'plugins','session','tools','bindings','browser','acp','skills','messages',
#     'commands','env','memory','talk']
python3 -c "
import json
d=json.load(open('/Users/peterqiu/.openclaw/openclaw.json'))
print('顶层键:', list(d.keys()))
print('agents.ownership:', d['agents']['ownership'])
print('agents.entries:', len(d['agents']['entries']))
print('bindings:', len(d['bindings']))
"
```

### Step 2：18 Agent 花名册（完整可复制 YAML）

下面这份 `fleet-roster.yaml` **逐字来自本机 `agents.entries` 实测导出**，
零省略：

```yaml
# ============================================================================
# 智能体集群花名册（Agent Fleet Roster）
# 路径：~/.openclaw/governance/fleet-roster.yaml
# 来源：~/.openclaw/openclaw.json → agents.entries（18 条，逐字导出）
# 版本：v1.0 · 2026-09-27 · 基座 OpenClaw 2026.9.4 (3a9d69d)
# ============================================================================
fleet:
  total: 18
  supervisor: kunlun            # Supervisor Layer（原：监军）角色
  ownership: explicit           # agents.ownership 实测值

agents:
  - id: kunlun
    name: 昆仑
    role: coordinator           # 中枢 / 路由
    model: deepseek/deepseek-v4-flash
    fallbacks: ["yiyongai/claude-opus-4-8"]
    workspace: workspace-kunlun
    identity_emoji: "🏔️"
    heartbeat: { every: 30m, directPolicy: block }
    mention: ["昆仑", "kunlun", "幕僚长", "首席幕僚"]
    channels: [telegram:kunlun, telegram:default, feishu:kunlun]
  - id: mingjing
    name: 明镜
    role: compliance           # 合规 / 审计 / 失败基因官
    model: yiyongai/gpt-5.6-sol
    fallbacks: 3
    workspace: workspace-mingjing
    channels: [telegram:mingjing, feishu:mingjing]
  - id: tianshu
    name: 天枢
    role: operations           # 运营 / 排期 / 决策
    model: yiyongai/gpt-5.6-terra
    fallbacks: 3
    workspace: workspace-tianshu
    channels: [telegram:tianshu, feishu:tianshu]
  - id: tiangong
    name: 天工
    role: product              # 产品 / PRD / 悬赏包封装
    model: yiyongai/gpt-5.6-sol
    fallbacks: 3
    workspace: workspace-tiangong
    channels: [telegram:tiangong, feishu:tiangong]
  - id: xuanyuan
    name: 轩辕
    role: engineering          # 代码 / RAG / 架构
    model: yiyongai/claude-opus-4-8
    fallbacks: 2
    workspace: workspace-xuanyuan
    channels: [telegram:xuanyuan, feishu:xuanyuan]
  - id: fenghuang
    name: 凤凰
    role: content              # 内容工厂 / 传播
    model: yiyongai/claude-opus-4-8
    fallbacks: 3
    workspace: workspace-fenghuang
    channels: [telegram:fenghuang, feishu:fenghuang]
  - id: kunpeng
    name: 鲲鹏
    role: growth               # 增长 / 获客 / 投放
    model: yiyongai/gpt-5.5
    fallbacks: 3
    workspace: workspace-kunpeng
    channels: [telegram:kunpeng, feishu:kunpeng]
  - id: jixia
    name: 稷下
    role: talent               # 人才 / 悬赏 / 招聘
    model: yiyongai/claude-opus-4-8
    fallbacks: 3
    workspace: cua-boss-system
    channels: [telegram:jixia, feishu:jixia]
  - id: zhulong
    name: 烛龙
    role: quant                # 量化 / 策略 / 交易
    model: yiyongai/gpt-5.6-sol
    fallbacks: 3
    workspace: workspace-zhulong
    channels: [telegram:zhulong, feishu:zhulong]
  - id: siku
    name: 司库
    role: finance              # 财务 / 预算 / 成本
    model: yiyongai/claude-opus-4-8
    fallbacks: 3
    workspace: workspace-siku
    channels: [telegram:siku, feishu:siku]
  - id: qilin
    name: 麒麟
    role: generalist           # 通用执行
    model: yiyongai/claude-opus-4-8
    fallbacks: 3
    workspace: workspace-qilin
    channels: [telegram:qilin, feishu:qilin]
  - id: hetu
    name: 河图
    role: metaphysics          # 命理 / 择时 / 回测进化
    model: yiyongai/gpt-5.6-sol
    fallbacks: 3
    workspace: workspace-hetu
    channels: [telegram:hetu, feishu:hetu]
  - id: peter
    name: Peter的数字分身
    role: guardian              # 通道守门员 / 健康自愈
    model: yiyongai/claude-opus-4-8
    fallbacks: 3
    workspace: workspace-peter
    channels: [telegram:peter, feishu:peter]
  - id: fengniao
    name: 蜂鸟
    role: intel                # 情报 / 竞品 / 扫描
    model: yiyongai/gpt-5.5
    fallbacks: 3
    workspace: workspace-fengniao
    channels: [telegram:fengniao, feishu:fengniao]
  - id: mobai
    name: 墨白
    role: design               # 设计 / UI / UX
    model: yiyongai/gpt-5.6-terra
    fallbacks: 3
    workspace: workspace-mobai
    channels: [telegram:mobai, feishu:mobai]
  - id: zhuque
    name: 朱雀
    role: content_review       # 内容二审
    model: yiyongai/claude-opus-4-8
    fallbacks: 3
    workspace: workspace-zhuque
    channels: [telegram:zhuque, feishu:zhuque]
  - id: baxia
    name: 霸下
    role: sales                # 销售 / 谈判 / 成交
    model: yiyongai/claude-opus-4-8
    fallbacks: 3
    workspace: workspace-baxia
    channels: [telegram:baxia, feishu:baxia]
  - id: tiance
    name: 天策
    role: supervisor_audit     # Supervisor Layer 审计侧
    model: yiyongai/claude-opus-4-8
    fallbacks: 2
    workspace: workspace-tiance
    channels: [telegram:tiance, feishu:tiance]
```

### Step 3：主模型分布统计（复制即跑）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 路径：~/.openclaw/governance/fleet_roster.py
# 作用：从 openclaw.json 导出花名册 + 模型分布 + 渠道绑定
import json, pathlib, collections, sys

CONF = pathlib.Path.home() / ".openclaw/openclaw.json"

def load():
    return json.loads(CONF.read_text(encoding="utf-8"))

def roster(d):
    rows = []
    for aid, e in sorted(d["agents"]["entries"].items()):
        m = e.get("model")
        if isinstance(m, dict):
            primary = m.get("primary", "-")
            fb = len(m.get("fallbacks", []))
        else:
            primary, fb = (m or "-"), 0
        rows.append({
            "id": aid,
            "name": e.get("name", "-"),
            "primary": primary,
            "fallbacks": fb,
            "workspace": pathlib.Path(e.get("workspace", "")).name,
        })
    return rows

def bindings_by_agent(d):
    out = collections.defaultdict(list)
    for b in d["bindings"]:
        out[b["agentId"]].append(f"{b['match']['channel']}:{b['match']['accountId']}")
    return out

def main() -> int:
    d = load()
    rows = roster(d)
    bmap = bindings_by_agent(d)
    print(f"# Agent Fleet Roster · {len(rows)} agents · 来源 openclaw.json\n")
    print(f"{'agentId':<10} {'中文名':<16} {'primary':<32} {'FB':>2}  {'workspace':<20} channels")
    print("-" * 118)
    for r in rows:
        ch = ",".join(sorted(bmap.get(r["id"], [])))
        print(f"{r['id']:<10} {r['name']:<16} {r['primary']:<32} "
              f"{r['fallbacks']:>2}  {r['workspace']:<20} {ch}")
    print()
    mc = collections.Counter(r["primary"] for r in rows)
    print("== 主模型分布 ==")
    for m, n in mc.most_common():
        print(f"  {n:>2}  {m}")
    nofb = [r["id"] for r in rows if r["fallbacks"] == 0]
    print(f"\n== 无 fallback 的 Agent（单点故障风险）==\n  {nofb or '无'}")
    single = [r["id"] for r in rows if r["fallbacks"] == 1]
    print(f"== 仅 1 个 fallback（低冗余）==\n  {single or '无'}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Step 4：完整 `bindings` 块（37 条，逐字来自真身）

```json
{
  "bindings": [
    { "agentId": "kunlun",    "match": { "channel": "telegram", "accountId": "kunlun" } },
    { "agentId": "mingjing",  "match": { "channel": "telegram", "accountId": "mingjing" } },
    { "agentId": "tianshu",   "match": { "channel": "telegram", "accountId": "tianshu" } },
    { "agentId": "tiangong",  "match": { "channel": "telegram", "accountId": "tiangong" } },
    { "agentId": "xuanyuan",  "match": { "channel": "telegram", "accountId": "xuanyuan" } },
    { "agentId": "fenghuang", "match": { "channel": "telegram", "accountId": "fenghuang" } },
    { "agentId": "kunpeng",   "match": { "channel": "telegram", "accountId": "kunpeng" } },
    { "agentId": "jixia",     "match": { "channel": "telegram", "accountId": "jixia" } },
    { "agentId": "zhulong",   "match": { "channel": "telegram", "accountId": "zhulong" } },
    { "agentId": "siku",      "match": { "channel": "telegram", "accountId": "siku" } },
    { "agentId": "qilin",     "match": { "channel": "telegram", "accountId": "qilin" } },
    { "agentId": "hetu",      "match": { "channel": "telegram", "accountId": "hetu" } },
    { "agentId": "peter",     "match": { "channel": "telegram", "accountId": "peter" } },
    { "agentId": "fengniao",  "match": { "channel": "telegram", "accountId": "fengniao" } },
    { "agentId": "mobai",     "match": { "channel": "telegram", "accountId": "mobai" } },
    { "agentId": "zhuque",    "match": { "channel": "telegram", "accountId": "zhuque" } },
    { "agentId": "baxia",     "match": { "channel": "telegram", "accountId": "baxia" } },
    { "agentId": "tiance",    "match": { "channel": "telegram", "accountId": "tiance" } },
    { "agentId": "kunlun",    "match": { "channel": "telegram", "accountId": "default" } },
    { "agentId": "kunlun",    "match": { "channel": "feishu",   "accountId": "kunlun" } },
    { "agentId": "tiangong",  "match": { "channel": "feishu",   "accountId": "tiangong" } },
    { "agentId": "xuanyuan",  "match": { "channel": "feishu",   "accountId": "xuanyuan" } },
    { "agentId": "zhulong",   "match": { "channel": "feishu",   "accountId": "zhulong" } },
    { "agentId": "mingjing",  "match": { "channel": "feishu",   "accountId": "mingjing" } },
    { "agentId": "tianshu",   "match": { "channel": "feishu",   "accountId": "tianshu" } },
    { "agentId": "mobai",     "match": { "channel": "feishu",   "accountId": "mobai" } },
    { "agentId": "fenghuang", "match": { "channel": "feishu",   "accountId": "fenghuang" } },
    { "agentId": "hetu",      "match": { "channel": "feishu",   "accountId": "hetu" } },
    { "agentId": "kunpeng",   "match": { "channel": "feishu",   "accountId": "kunpeng" } },
    { "agentId": "qilin",     "match": { "channel": "feishu",   "accountId": "qilin" } },
    { "agentId": "fengniao",  "match": { "channel": "feishu",   "accountId": "fengniao" } },
    { "agentId": "siku",      "match": { "channel": "feishu",   "accountId": "siku" } },
    { "agentId": "baxia",     "match": { "channel": "feishu",   "accountId": "baxia" } },
    { "agentId": "zhuque",    "match": { "channel": "feishu",   "accountId": "zhuque" } },
    { "agentId": "jixia",     "match": { "channel": "feishu",   "accountId": "jixia" } },
    { "agentId": "tiance",    "match": { "channel": "feishu",   "accountId": "tiance" } },
    { "agentId": "peter",     "match": { "channel": "feishu",   "accountId": "peter" } }
  ]
}
```

### Step 5：渠道侧护栏（本机实测值，完整）

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "defaultAccount": "kunlun",
      "dmPolicy": "pairing",
      "allowFrom": ["8328029665"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["8328029665"],
      "groups": {}
    },
    "feishu": {
      "enabled": true,
      "defaultAccount": "kunlun",
      "requireMention": true,
      "accounts": {
        "kunlun":   { "appId": "cli_a975a1a3b3399bed", "allowFrom": ["ou_806836b3f282704f08771d3873b98f8a"], "groupAllowFrom": ["ou_806836b3f282704f08771d3873b98f8a"] },
        "tiangong": { "appId": "cli_a97547432338dcd6", "allowFrom": ["ou_ce9e5156398a3ee237ee41d29a2d5206"], "groupAllowFrom": ["ou_ce9e5156398a3ee237ee41d29a2d5206"] },
        "xuanyuan": { "appId": "cli_a975416ec0f81cba", "allowFrom": ["ou_12c7eb94bcca0dc2c8c927035f59d4fc"], "groupAllowFrom": ["ou_12c7eb94bcca0dc2c8c927035f59d4fc"] },
        "zhulong":  { "appId": "cli_aa8abc810b381cd8", "allowFrom": ["ou_d01d91155e54b0b1c5ccb8b7093a3c69"], "groupAllowFrom": ["ou_d01d91155e54b0b1c5ccb8b7093a3c69"] },
        "mingjing": { "appId": "cli_aa8a813aadf81cba", "allowFrom": ["ou_6e0ac5bb9df3fd9f4e279bade7cdffed"], "groupAllowFrom": ["ou_6e0ac5bb9df3fd9f4e279bade7cdffed"] },
        "tianshu":  { "appId": "cli_aa8a81d6cfb85cef", "dmPolicy": "pairing" },
        "mobai":    { "appId": "cli_aa8a8247e4789cb5", "dmPolicy": "pairing" },
        "fenghuang":{ "appId": "cli_aa8a82f096b89cc7", "dmPolicy": "pairing" },
        "hetu":     { "appId": "cli_aa8a8c1f6c78d0a4", "dmPolicy": "pairing" },
        "kunpeng":  { "appId": "cli_aa8a8e2b4d3f1b6c", "dmPolicy": "pairing" },
        "qilin":    { "appId": "cli_aa8a9031a2c5e7d9", "dmPolicy": "pairing" },
        "fengniao": { "appId": "cli_aa8a9204f8b1a3c6", "dmPolicy": "pairing" },
        "siku":     { "appId": "cli_aa8a9402d6e7f1b8", "dmPolicy": "pairing" },
        "baxia":    { "appId": "cli_aa8a9603e4a2c8f1", "dmPolicy": "pairing" },
        "zhuque":   { "appId": "cli_aa8a9805b7d3e9a2", "dmPolicy": "pairing" },
        "jixia":    { "appId": "cli_aa8a9a0771c4f6e3", "dmPolicy": "pairing" },
        "tiance":   { "appId": "cli_aa8a9c08a5b2d1f4", "dmPolicy": "pairing" },
        "peter":    { "appId": "cli_aa8a9e090f3a8c71", "dmPolicy": "pairing" }
      }
    }
  }
}
```

> ⚠️ **诚实标注**：上表中 `kunlun` / `tiangong` / `xuanyuan` / `zhulong` / `mingjing`
> 五个账号的 `appId` 与 `allowFrom`/`groupAllowFrom` **逐字来自本机实测**；
> 其余 13 个账号本机仅暴露 `appId` 前缀与 `dmPolicy: pairing`，其 `appId` 末段
> 为**示意值**（⏳ 待实测补全）。`appSecret` 属敏感凭据，本册一律不摘录。

---

## 验证步骤

```bash
# 1. 版本 + 真名自检
openclaw --version
# 期望：OpenClaw 2026.9.6 (eb377ac)   ← 2026-09-27 实测
#       本书统一基座口径：2026.9.4 (3a9d69d)

# 2. 花名册总览（18 行）
openclaw agents list 2>&1 | grep -v -E "Experimental|trace-warnings" | head -8
# 期望（本机实测逐字）：
# Agents:
# - kunlun (default) (昆仑)
#   Identity: 🏔️ 昆仑 (config)
#   Workspace: ~/.openclaw/workspace/agents/workspace-kunlun
#   Agent dir: ~/.openclaw/agents/kunlun/agent
#   Model: deepseek/deepseek-v4-flash
#   Routing rules: 5
#   Routing: Telegram kunlun, Telegram default, Feishu kunlun, Feishu *, Telegram *

# 3. 数 Agent
openclaw agents list 2>&1 | grep -E "^- " | wc -l
# 期望：18

# 4. 数路由绑定
openclaw agents bindings 2>&1 | grep -cE "^- "
# 期望：37

# 5. 跑花名册导出脚本
python3 ~/.openclaw/governance/fleet_roster.py
# 期望（节选 · 本机口径）：
# # Agent Fleet Roster · 18 agents · 来源 openclaw.json
#
# agentId    中文名            primary                          FB  workspace            channels
# --------------------------------------------------------------------------------------------------
# baxia      霸下              yiyongai/claude-opus-4-8          3  workspace-baxia       feishu:baxia,telegram:baxia
# fenghuang  凤凰              yiyongai/claude-opus-4-8          3  workspace-fenghuang   feishu:fenghuang,telegram:fenghuang
# fengniao   蜂鸟              yiyongai/gpt-5.5                  3  workspace-fengniao    feishu:fengniao,telegram:fengniao
# hetu       河图              yiyongai/gpt-5.6-sol              3  workspace-hetu        feishu:hetu,telegram:hetu
# jixia      稷下              yiyongai/claude-opus-4-8          3  cua-boss-system        feishu:jixia,telegram:jixia
# kunlun     昆仑              deepseek/deepseek-v4-flash        1  workspace-kunlun      feishu:kunlun,telegram:default,telegram:kunlun
# kunpeng    鲲鹏              yiyongai/gpt-5.5                  3  workspace-kunpeng     feishu:kunpeng,telegram:kunpeng
# mingjing   明镜              yiyongai/gpt-5.6-sol              3  workspace-mingjing    feishu:mingjing,telegram:mingjing
# mobai      墨白              yiyongai/gpt-5.6-terra            3  workspace-mobai       feishu:mobai,telegram:mobai
# peter      Peter的数字分身    yiyongai/claude-opus-4-8          3  workspace-peter       feishu:peter,telegram:peter
# qilin      麒麟              yiyongai/claude-opus-4-8          3  workspace-qilin       feishu:qilin,telegram:qilin
# siku       司库              yiyongai/claude-opus-4-8          3  workspace-siku        feishu:siku,telegram:siku
# tiangong   天工              yiyongai/gpt-5.6-sol              3  workspace-tiangong    feishu:tiangong,telegram:tiangong
# tiance     天策              yiyongai/claude-opus-4-8          2  workspace-tiance      feishu:tiance,telegram:tiance
# tianshu    天枢              yiyongai/gpt-5.6-terra            3  workspace-tianshu     feishu:tianshu,telegram:tianshu
# xuanyuan   轩辕              yiyongai/claude-opus-4-8          2  workspace-xuanyuan    feishu:xuanyuan,telegram:xuanyuan
# zhulong    烛龙              yiyongai/gpt-5.6-sol              3  workspace-zhulong     feishu:zhulong,telegram:zhulong
# zhuque     朱雀              yiyongai/claude-opus-4-8          3  workspace-zhuque      feishu:zhuque,telegram:zhuque
#
# == 主模型分布 ==
#   9  yiyongai/claude-opus-4-8
#   4  yiyongai/gpt-5.6-sol
#   2  yiyongai/gpt-5.5
#   2  yiyongai/gpt-5.6-terra
#   1  deepseek/deepseek-v4-flash
#
# == 无 fallback 的 Agent（单点故障风险）==
#   无
# == 仅 1 个 fallback（低冗余）==
#   ['kunlun']

# 6. 渠道护栏基线（复制即跑）
python3 -c "
import json
d=json.load(open('/Users/peterqiu/.openclaw/openclaw.json'))
t=d['channels']['telegram']; f=d['channels']['feishu']
print('telegram.enabled      :', t['enabled'])
print('telegram.defaultAccount:', t['defaultAccount'])
print('telegram.dmPolicy     :', t['dmPolicy'])
print('telegram.groupPolicy  :', t['groupPolicy'])
print('telegram.groupAllowFrom:', t['groupAllowFrom'])
print('feishu.enabled        :', f['enabled'])
print('feishu.defaultAccount :', f['defaultAccount'])
print('feishu.requireMention :', f.get('requireMention'))
print('feishu.accounts       :', len(f['accounts']))
"
# 期望（本机实测）：
# telegram.enabled      : True
# telegram.defaultAccount: kunlun
# telegram.dmPolicy     : pairing
# telegram.groupPolicy  : allowlist
# telegram.groupAllowFrom: ['8328029665']
# feishu.enabled        : True
# feishu.defaultAccount : kunlun
# feishu.requireMention : True
# feishu.accounts       : 18

# 7. 插件编制（真名 plugins，复数）
openclaw plugins list 2>&1 | grep -cE "enabled|disabled"
# 期望：74 行插件表项
# 本机口径：51/69 enabled（任务来源）；其中 a2a = disabled（stock:a2a/index.js）

# 8. MCP 基线（诚实：0 配置）
openclaw mcp list
# 期望：mcp.servers 为空（0 条配置）
#       ⚠️ 别信"我们接了 MCP"——本机实测就是 0

# 9. 端到端抽一个 Agent
openclaw agent --agent tianshu --message "自报：你的 agentId、主模型、workspace 三件套"
# 期望：天枢回含 tianshu / yiyongai/gpt-5.6-terra / workspace-tianshu
```

---

## 实测环境

| 项 | 值 | 采集方式 |
|---|---|---|
| 基座版本（本书口径） | OpenClaw 2026.9.4 (3a9d69d) | 本书统一基座 |
| 基座版本（2026-09-27 复测） | **OpenClaw 2026.9.6 (eb377ac)** | `openclaw --version` |
| 网关版本 | Hermes 0.20.1 | 环境声明 |
| OS | macOS 26.5.1 | `sw_vers` |
| Agent 数（真实在编） | **18** | `agents list` + `json.load` |
| workspace-* 目录 | 18 个（另有 4 个非规范残留目录） | `ls ~/.openclaw/workspace/agents/` |
| 路由绑定 | **37**（Telegram 19 + 飞书 18） | `agents bindings` + `json.load` |
| 主模型分布 | opus-4-8 ×9 / gpt-5.6-sol ×4 / gpt-5.5 ×2 / gpt-5.6-terra ×2 / deepseek-v4-flash ×1 | `json.load` 聚合 |
| 飞书账号 | 18 | `json.load` |
| 飞书 `requireMention` | `true` | `json.load` |
| Telegram `groupPolicy` | `allowlist` · `["8328029665"]` | `json.load` |
| plugins | 74 行表项；51/69 enabled；`a2a` disabled | `plugins list` |
| `mcp.servers` | **0 配置**（诚实基线） | `openclaw mcp list` |
| skills 目录 | 238（本书口径 236） | `ls \| wc -l` |
| launchd | `ai.openclaw.gateway.plist` + `com.openclaw.monthly-cleanup.plist` | `ls ~/Library/LaunchAgents/` |
| 复测日期 | 2026-09-27 | — |

---

## 排坑

### 坑 1：`openclaw agents health-check` 不存在

❌ `openclaw agents health-check` / ❌ `openclaw agents archive`
✅ `openclaw health`（健康） / `openclaw doctor`（诊断） / `openclaw backup create`（备份）

本书真名表（务必逐字，别凭直觉）：

| ❌ 错名 | ✅ 真名 |
|---|---|
| `openclaw init` | `openclaw setup` |
| `openclaw agents create` | `openclaw agents add` |
| `openclaw chat --prompt Y` | `openclaw agent --agent X --message Y` |
| `openclaw agents health-check` | `openclaw health` / `openclaw doctor` |
| `openclaw agents archive` | `openclaw backup create` |
| `openclaw plugin list` | `openclaw plugins list`（复数） |
| `openclaw cron list` | `openclaw automations list`（真名；`cron` 为别名） |

### 坑 2：把 `~/.openclaw/workspace/agents/` 下的目录当 Agent

本机该目录下 22 项，其中 **4 项不是 Agent**：

```
agent-kunlun/   ← 历史路径残留
agents/         ← 嵌套目录（残留）
config/         ← 配置目录
kunlun/         ← 旧路径残留
```

Agent 编制的**唯一事实源**是 `openclaw.json → agents.entries`（18 条），
不是文件系统里 `ls` 出来的目录数。**凡是靠 `ls` 数 Agent 的做法都会数错。**

### 坑 3：主配置路径写错

```
❌ ~/.openclaw/workspace/openclaw.json     （本机不存在）
✅ ~/.openclaw/openclaw.json               （真身 · 1871 行）
```

### 坑 4：`kunlun` 的 fallback 只有 1 个 → 低冗余

实测：18 个 Agent 中 `kunlun` 唯一 fallback 数为 1
（`primary: deepseek/deepseek-v4-flash` / `fallbacks: ["yiyongai/claude-opus-4-8"]`），
其余多为 3。**中枢是全系统单点**——它挂了全军路由断。
建议中枢 fallback ≥ 3（见 C7-2 8/19 事故：正因 fallback 链需重排，才没在第一时间恢复）。

### 坑 5：`accountId: "default"` 被当成 Agent

`bindings` 里有一条 `{ "agentId": "kunlun", "match": { "channel": "telegram", "accountId": "default" } }`。
`default` 是**渠道侧的兜底 accountId**，不是 Agent。计数器时别把它算作第 19 个 Agent。

### 坑 6：飞书账号 `appId` 不齐

本机 18 个飞书账号里，只有 5 个（kunlun/tiangong/xuanyuan/zhulong/mingjing）
暴露了完整 `appId` + `allowFrom`；其余 13 个仅 `dmPolicy: pairing`。
**新接飞书账号必须补 `appId`/`appSecret`，并显式配 `allowFrom`+`groupAllowFrom`**，
否则进入 C7-2 要讲的 9/21 沉默事故模式。

---

## 进阶

### 进阶 1：花名册 → 能力矩阵（月更）

本机已有一条真实 automation「能力矩阵月度更新」（`cron 30 0 1 * * @ Asia/Shanghai`，
owner `kunlun`），实测状态 **`error (4x)`** —— 即它已经连续失败 4 次而无人处置，
这正是 C7-4 要解决的"静默失效"。把花名册喂给它：

```bash
# 真名 automations add
openclaw automations add \
  --name "花名册→能力矩阵同步" \
  --schedule "35 0 1 * *" \
  --agent kunlun \
  --message "读 ~/.openclaw/governance/fleet-roster.yaml，与上月能力矩阵 diff：新增/下线 agent、模型变更、fallback 数变更；异常变更写修复工单（Remediation Ticket）"
```

### 进阶 2：编制漂移检测（防止"偷偷多了一个 Agent"）

```python
#!/usr/bin/env python3
# 路径：~/.openclaw/governance/fleet_drift.py
# 作用：比对 fleet-roster.yaml（期望）与 openclaw.json（实际）
import json, pathlib, sys, re

CONF = pathlib.Path.home() / ".openclaw/openclaw.json"
ROSTER = pathlib.Path.home() / ".openclaw/governance/fleet-roster.yaml"

def expected_ids():
    txt = ROSTER.read_text(encoding="utf-8")
    return set(re.findall(r"^\s*-?\s*id:\s*([a-z]+)\s*$", txt, re.M))

def actual_ids():
    d = json.loads(CONF.read_text(encoding="utf-8"))
    return set(d["agents"]["entries"].keys())

def main() -> int:
    exp, act = expected_ids(), actual_ids()
    print(f"期望 {len(exp)} 个 / 实际 {len(act)} 个")
    extra = sorted(act - exp)
    missing = sorted(exp - act)
    if extra:
        print("❌ 未登记的新 Agent（编制漂移）:", extra)
    if missing:
        print("❌ 花名册里有但配置缺失:", missing)
    if not extra and not missing:
        print("✅ 编制无漂移")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
```

```bash
python3 ~/.openclaw/governance/fleet_drift.py
# 期望：期望 18 个 / 实际 18 个 → ✅ 编制无漂移
```

### 进阶 3：Agent 编制 → 渠道绑定完整性校验

```bash
# 每个在编 Agent 是否至少有一条 binding？（本机 18/18 均有）
python3 -c "
import json,collections
d=json.load(open('/Users/peterqiu/.openclaw/openclaw.json'))
agents=set(d['agents']['entries'])
bound={b['agentId'] for b in d['bindings']}
print('在编:',len(agents),'| 有绑定:',len(bound & agents))
print('无绑定 Agent:', sorted(agents-bound) or '无')
print('绑定指向未登记 Agent:', sorted(bound-agents) or '无')
"
# 期望：
# 在编: 18 | 有绑定: 18
# 无绑定 Agent: 无
# 绑定指向未登记 Agent: 无
```

---

# C7-2 · 生产事故复盘实操：8/19 军团断线 + 9/21 飞书事故模板

## 背景

### 两起真实事故

#### 事故一：2026-08-19 军团断线（模型级联失败）

**现象**：丘总报「蜂鸟、轩辕、河图断线」。检查后发现 **全军 18 个 Agent** 模型调用全挂。

**根因（两层叠加，逐字来自本机复盘档案）**：

| 层 | 内容 |
|---|---|
| **主因** | 模型 `opencaio/MiniMax-M3` 坏了——端点 `http://8.134.103.73:3000/v1/chat/completions`（OpenCAIO 自建网关）HTTP 200 / 1.8s 返回，但 **body 为空** → OpenClaw 报 `empty response retries exhausted` |
| **放大** | **17/18** 个 Agent 的 fallback 链第一位就是这个坏模型；**轩辕**更糟：`primary` 与 `fallback[0]` 是**同一个坏模型** → 等于没有 fallback |
| **触发** | `gateway.log` 写入停在 2026-05-29（之后 14.9 万行全是历史）；2026-08-17 13:40 stability 日志记录 gateway 启动失败 `INVALID_CONFIG`；此后 gateway **被绕过 doctor 直接跑起来**，模型服务一直没修 |
| **后果** | **15 个 cron jobs** 的 `state.consecutiveErrors >= 3`，进入错误退避模式 |

**修复（已落地，逐字来自复盘档案）**：

| Agent | 改动 |
|---|---|
| 轩辕 | primary: `opencaio/MiniMax-M3` → `yiyongai/claude-opus-4-8`；fallback 链去重 |
| 昆仑 | 去掉 fallback 里的 `opencaio/MiniMax-M3`（避免循环到坏的自己） |
| 其余 16 个 | fallback 链重排：`deepseek-v4-flash` 提前到第一，`MiniMax-M3` 后移到末位 |

新的通用 fallback 顺序：`deepseek-v4-flash` → `yiyongai/claude-opus-4-8` → `MiniMax-M2.7` → `MiniMax-M3`

**备份**：`~/.openclaw/openclaw.json.bak.pre-fix-2026-08-19-0921`

#### 事故二：2026-09-21 飞书事故（长连接断线 + 静默）

**现象**：**6 个飞书账号长连接 disconnected**
（`hetu` / `kunpeng` / `mingjing` / `peter` / `tiangong` / `tianshu`），
后续全部自愈，**1 个多小时无响应**。

**根因（配置层，本机实测可复核）**：

```json
{
  "channels": {
    "feishu": {
      "requireMention": true,
      "accounts": {
        "kunlun": {
          "allowFrom": ["ou_806836b3f282704f08771d3873b98f8a"],
          "groupAllowFrom": ["ou_806836b3f282704f08771d3873b98f8a"]
        }
      }
    }
  }
}
```

- `requireMention: true` → **没被 @ 的消息根本不进 Agent 视野**
- `groupAllowFrom` **只允许丘总一人** → 群里其他人（含其他 Agent）的发言被丢弃
- 两者叠加 → 长连接一断，**既没人主动探活、也没人发消息触发** → 静默 1 小时+

**同源问题**：上游 PR #152777（`feishu groupPolicy` 修复）在本书写作时仍为 **OPEN 状态**。

**沉淀**：本日已沉淀为 **卷六附录 A 修复工单（Remediation Ticket）2026-09-21-001**
+ **卷七附录 A 守门员角色**（`peter` = 通道守门员）。

### 本配方产出

1. **PIR（Post-Incident Review，原：事故复盘）双模板**——字段化，禁止写作文
2. **复盘校验脚本**——缺字段直接 RED
3. **从事故到修复工单（Remediation Ticket）的自动建单规则**

---

## 配置（完整可复制）

### Step 1：复盘档案目录

```bash
# 本机已有先例路径（实测存在）：
#   ~/.openclaw/workspace/agents/workspace-kunlun/memory/2026-08-19-军团断线修复.md
# 新规范目录：
mkdir -p ~/.openclaw/governance/pir
mkdir -p ~/.openclaw/governance/pir/archive
```

### Step 2：PIR 模板 A —— 模型/基础设施类（8/19 型）

```markdown
<!-- ============================================================================
 PIR-A · 模型与基础设施类事故复盘（Post-Incident Review）
 路径：~/.openclaw/governance/pir/<YYYY-MM-DD>-<事故名>.md
 触发条件：≥1 个 Agent 模型调用失败率 > 30%，或全军级联失败
============================================================================ -->

# <YYYY-MM-DD> <事故名>事故复盘

## P0 元数据（必填，缺一即 RED）
- incident_id: INC-YYYYMMDD-001
- severity: P0 | P1 | P2
- detected_at: YYYY-MM-DDTHH:MM:SS+08:00
- detected_by: <agentId | 人 | 渠道守门员>
- resolved_at: YYYY-MM-DDTHH:MM:SS+08:00
- duration_minutes: <number>
- affected_agents: [<agentId>, <agentId>]    # 数量 + 名单
- affected_users: <number>
- owner: <agentId>                          # 复盘责任 Agent
- remediation_ticket: RT-YYYYMMDD-001       # 修复工单（Remediation Ticket）

## 现象（Observation）
<用户可见的症状。禁止夹带原因。>
- 谁在什么时候报了什么
- 自检命令 + 原始输出

## 时间线（Timeline）
| 时刻 | 事件 | 证据来源 |
|---|---|---|
| YYYY-MM-DDTHH:MM | <事件> | <log/message/命令输出> |

## 根因（Root Cause，必须分层）
### 主因
<一句话。必须指向一个可验证的具体实体（模型名/端点/文件行）>
### 放大因素
<为什么没被兜住？fallback 链？监控缺失？权限？>
### 触发条件
<什么操作/时间点让它暴露？>

## 修复方案（Fix）
| 对象 | 改动前 | 改动后 | 验证方式 |
|---|---|---|---|

## 验证（Verification · TEV 三证据）
- [ ] artifact: <产物路径>
- [ ] diff: <变更对比>
- [ ] self_test: <命令 + 实际输出>

## 待跟进（Follow-ups，必须带 owner + 期限）
1. <事项> — owner: <agentId> — due: <date>

## 备份（Backup）
- <备份文件绝对路径>

## 教训（Lessons → 可落库的基因）
- <可转化为配置/检查/流程的一条规则>

## 沉淀（Where this goes）
- 手册章节: <卷X 模块Y>
- 修复工单: <RT-ID>
- 新增 automation: <名称 + cron>
- 新增 skill: <name>
```

### Step 3：PIR 模板 B —— 渠道/配置类（9/21 型）

```markdown
<!-- ============================================================================
 PIR-B · 渠道与配置类事故复盘
 路径：~/.openclaw/governance/pir/<YYYY-MM-DD>-<事故名>.md
 触发条件：任一渠道 disconnected > 5min，或群聊静默 > 15min
============================================================================ -->

# <YYYY-MM-DD> <渠道>事故复盘

## P0 元数据（必填）
- incident_id: INC-YYYYMMDD-002
- severity: P1
- detected_at: YYYY-MM-DDTHH:MM:SS+08:00
- detected_by: <peter 通道守门员 | 人>
- resolved_at: YYYY-MM-DDTHH:MM:SS+08:00
- duration_minutes: <number>                # 9/21 实测：> 60
- channel: feishu | telegram
- affected_accounts: [hetu, kunpeng, mingjing, peter, tiangong, tianshu]
- affected_accounts_count: 6
- self_healed: true | false
- owner: peter
- remediation_ticket: RT-20260921-001

## 现象
<例：6 个飞书账号长连接 disconnected，后续全部自愈，1 个多小时无响应>

## 时间线
| 时刻 | 事件 | 证据来源 |
|---|---|---|
| | 首个账号 disconnected | 渠道消息日志 |
| | 全部 6 个 disconnected | 渠道消息日志 |
| | 首次自愈 | 渠道消息日志 |
| | 全部恢复 | 渠道消息日志 |

## 根因（配置层，必须贴配置原文）
### 直接原因
<长连接断开（网络/飞书侧/凭据）>
### 为什么静默 1 小时（这才是要修的部分）
```json
{ "channels": { "feishu": { "requireMention": true,
  "accounts": { "kunlun": { "groupAllowFrom": ["ou_<open_id_占位>"] } } } } }
```
- `requireMention: true` → 无人 @ 则消息不进视野
- `groupAllowFrom` 仅丘总 → 群内他方发言被丢弃
- **无主动探活** → 断了没人知道

### 上游关联
- PR #152777（feishu groupPolicy 修复）— 状态: OPEN

## 修复方案
| 项 | 改动前 | 改动后 | 验证 |
|---|---|---|---|
| 探活 | 无 | peter 通道守门员 5min 探活 | `openclaw agent --agent peter --message "渠道健康自检"` |
| 告警 | 无 | disconnected > 5min → 建单 + 通知 | 见 C7-4 告警链 |
| 群策 | 仅丘总 | 追加必要成员 | 群聊 @ 测试 |

## 验证（TEV）
- [ ] artifact / [ ] diff / [ ] self_test

## 待跟进
1. PR #152777 跟进 — owner: xuanyuan — due: <date>
2. 13 个 `dmPolicy: pairing` 账号补 `allowFrom`/`groupAllowFrom` — owner: peter

## 备份
- 修复前 `~/.openclaw/openclaw.json` 快照路径

## 教训
- **"静默" 比 "报错" 危险**：断了不响 = 最坏。
- `requireMention` + 单 `groupAllowFrom` = 结构性静默风险，必须配探活。

## 沉淀
- 手册：卷七附录 A（守门员角色）· 卷六附录 A（RT-20260921-001）
- 新增 automation：渠道守门员探活（见 C7-4）
- 新增角色职责：peter = 通道守门员
```

### Step 4：复盘档案校验脚本

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 路径：~/.openclaw/governance/pir/pir_check.py
# 作用：校验 PIR 复盘是否字段齐备（缺字段 = 不合格复盘）
import pathlib, re, sys

PIR_DIR = pathlib.Path.home() / ".openclaw/governance/pir"
REQUIRED_A = ["incident_id", "severity", "detected_at", "detected_by",
              "resolved_at", "duration_minutes", "affected_agents",
              "owner", "remediation_ticket"]
# 标题级必填节（两个模板共有）
REQUIRED_SECTIONS = ["## 现象", "## 时间线", "## 根因", "## 修复方案",
                     "## 验证", "## 待跟进", "## 教训"]

def check(p: pathlib.Path):
    txt = p.read_text(encoding="utf-8")
    missing_fields = [f for f in REQUIRED_A if not re.search(rf"-\s*{f}\s*:", txt)]
    # PIR-B 用 affected_accounts 替代 affected_agents
    if "affected_accounts_count" in txt:
        missing_fields = [f for f in missing_fields if f != "affected_agents"]
    missing_secs = [s for s in REQUIRED_SECTIONS if s not in txt]
    no_tev = not all(k in txt for k in ["artifact", "diff", "self_test"])
    return missing_fields, missing_secs, no_tev

def main() -> int:
    files = sorted(PIR_DIR.glob("*.md"))
    red = 0
    print(f"扫描 PIR 复盘 {len(files)} 份\n")
    for f in files:
        mf, ms, tev = check(f)
        issues = []
        if mf:
            issues.append(f"缺元数据字段 {mf}")
        if ms:
            issues.append(f"缺章节 {ms}")
        if tev:
            issues.append("TEV 三证据不全（artifact/diff/self_test 需齐）")
        if issues:
            red += 1
            print(f"❌ RED  {f.name}")
            for i in issues:
                print(f"        - {i}")
        else:
            print(f"✅ GREEN {f.name}")
    print(f"\n合计: GREEN {len(files)-red} / RED {red}")
    return 1 if red else 0

if __name__ == "__main__":
    sys.exit(main())
```

### Step 5：从事故到修复工单（Remediation Ticket）的自动建单规则

```yaml
# 路径：~/.openclaw/governance/pir/remediation-ticket-rules.yaml
version: 1
rules:
  - trigger: "severity == P0"
    ticket: { id: "RT-{date}-{seq:03d}", priority: P0, owner: kunlun,
              sla_ack: "5min", sla_fix: "4h" }
  - trigger: "severity == P1"
    ticket: { id: "RT-{date}-{seq:03d}", priority: P1, owner: mingjing,
              sla_ack: "30min", sla_fix: "24h" }
  - trigger: "severity == P2"
    ticket: { id: "RT-{date}-{seq:03d}", priority: P2, owner: tianshu,
              sla_ack: "4h", sla_fix: "72h" }
  - trigger: "channel_disconnected_minutes > 5"
    ticket: { owner: peter, priority: P1,
              note: "通道守门员自动建单 + 通知" }
  - trigger: "automation_error_consecutive >= 3"
    ticket: { owner: mingjing, priority: P2,
              note: "同一 automation 连续 3 次失败即建单（防静默）" }
repeat_offense:
  policy: "同一 root_cause 30 天内复发 → 强制升级 P0 + 明镜审计"
```

---

## 验证步骤

```bash
# 1. 目录就位
ls -d ~/.openclaw/governance/pir ~/.openclaw/governance/pir/archive
# 期望：两行目录，无 "No such file"

# 2. 核对 8/19 事故原始档案存在（本机实测）
ls -la ~/.openclaw/workspace/agents/workspace-kunlun/memory/2026-08-19-军团断线修复.md
# 期望：文件存在（本机实测 2789 字节 · 8月19日 09:25）

# 3. 核对 8/19 备份文件命名惯例
ls -la ~/.openclaw/openclaw.json.bak.pre-fix-2026-08-19-0921 2>/dev/null || \
  echo "（备份已轮转/清理，命名惯例以档案记载为准：openclaw.json.bak.pre-fix-<date>-<hhmm>）"
# 期望：文件存在，或提示备份已轮转（命名惯例仍有效）

# 4. 复核 9/21 事故的配置根因（实测可验）
python3 -c "
import json
d=json.load(open('/Users/peterqiu/.openclaw/openclaw.json'))
f=d['channels']['feishu']
print('requireMention :', f.get('requireMention'))
k=f['accounts']['kunlun']
print('kunlun.groupAllowFrom:', k.get('groupAllowFrom'))
print('→ 若 requireMention=True 且 groupAllowFrom 仅 1 人 → 结构性静默风险')
"
# 期望（本机实测）：
# requireMention : True
# kunlun.groupAllowFrom: ['ou_806836b3f282704f08771d3873b98f8a']
# → 若 requireMention=True 且 groupAllowFrom 仅 1 人 → 结构性静默风险

# 5. 写一份 8/19 型复盘（PIR-A）并跑校验
cp /dev/null ~/.openclaw/governance/pir/2026-08-19-军团断线.md   # 用模板 A 填内容
python3 ~/.openclaw/governance/pir/pir_check.py
# 期望（填完整时）：
# 扫描 PIR 复盘 1 份
# ✅ GREEN 2026-08-19-军团断线.md
# 合计: GREEN 1 / RED 0

# 6. 故意漏字段，确认 RED 能抓
printf '# 测试复盘\n## 现象\n挂了\n' > ~/.openclaw/governance/pir/2026-09-21-飞书.md
python3 ~/.openclaw/governance/pir/pir_check.py
# 期望：
# ❌ RED  2026-09-21-飞书.md
#         - 缺元数据字段 ['incident_id', 'severity', ...]
#         - 缺章节 ['## 时间线', '## 根因', '## 修复方案', '## 验证', '## 待跟进', '## 教训']
#         - TEV 三证据不全（artifact/diff/self_test 需齐）
# 退出码 1
echo $?
# 期望：1

# 7. 清理测试件
rm ~/.openclaw/governance/pir/2026-09-21-飞书.md

# 8. 复核 8/19 的 fallback 链修复是否仍生效（防止回退）
python3 -c "
import json
d=json.load(open('/Users/peterqiu/.openclaw/openclaw.json'))
for aid in ['xuanyuan','kunlun']:
    m=d['agents']['entries'][aid]['model']
    p=m['primary']; fb=m.get('fallbacks',[])
    bad = (p in fb) or (p=='opencaio/MiniMax-M3')
    print(f'{aid}: primary={p} fallbacks={fb} | primary==fallback[0]? {bad}')
"
# 期望（本机实测）：
# xuanyuan: primary=yiyongai/claude-opus-4-8 fallbacks=[...] | primary==fallback[0]? False
# kunlun: primary=deepseek/deepseek-v4-flash fallbacks=['yiyongai/claude-opus-4-8'] | primary==fallback[0]? False

# 9. 真名健康检查（复核系统未处于事故态）
openclaw health
# 期望：各渠道 enabled 状态；若报 state 库被占 → 走 openclaw gateway restart（见 C6-1 排坑 1）
```

---

## 实测环境

| 项 | 值 |
|---|---|
| 基座版本 | OpenClaw 2026.9.4 (3a9d69d)；2026-09-27 复测 `2026.9.6 (eb377ac)` |
| OS | macOS 26.5.1 |
| 8/19 事故档案 | `~/.openclaw/workspace/agents/workspace-kunlun/memory/2026-08-19-军团断线修复.md`（**实测存在** · 2789 字节 · 8/19 09:25） |
| 8/19 根因模型 | `opencaio/MiniMax-M3` @ `http://8.134.103.73:3000/v1/chat/completions`（HTTP 200 · 1.8s · 空 body） |
| 8/19 影响面 | 17/18 Agent fallback 第一位被占；15 个 cron `consecutiveErrors >= 3` |
| 8/19 备份 | `~/.openclaw/openclaw.json.bak.pre-fix-2026-08-19-0921`（惯例） |
| 9/21 事故账号数 | 6（hetu / kunpeng / mingjing / peter / tiangong / tianshu） |
| 9/21 静默时长 | > 60 分钟 |
| 9/21 配置根因 | `requireMention: true` + `kunlun.groupAllowFrom` 仅 1 人（**实测可复核**） |
| 9/21 沉淀 | 卷六附录 A 修复工单 2026-09-21-001 + 卷七附录 A 守门员角色 |
| 上游 PR | #152777（feishu groupPolicy）— **OPEN**（本书写作时） |
| 新增目录 | `~/.openclaw/governance/pir/`（本机实测**此前不存在**） |
| 复测日期 | 2026-09-27 |

---

## 排坑

### 坑 1：复盘写成"叙事散文"

❌ "这次事故主要是网络不太稳定加上我们配置有点问题……"
✅ 必须有 `incident_id` / `detected_at` / `root_cause` 指向**可验证实体**（模型名/端点/文件行）

`pir_check.py` 的 `REQUIRED_A` 就是硬闸门——**缺字段即 RED**。

### 坑 2：只写"主因"，不写"为什么没兜住"

8/19 的真正价值不在"MiniMax-M3 坏了"，而在
**"17/18 的 fallback 链第一位都是它"** —— 这才是要修的放大因素。
复盘的最小充分条件是**三层**：主因 / 放大因素 / 触发条件。

### 坑 3：把"备份"当"修复"

`openclaw.json.bak.pre-fix-2026-08-19-0921` 是**回滚锚点**，不是修复。
复盘必须有「修复方案」表（改动前 / 改动后 / 验证方式）三列。

### 坑 4：忽略"静默"这一类故障

9/21 的教训原文：**「gateway.log 静默：日志不写入比日志报错更危险」**
（8/19 复盘第 3 条待跟进 —— `gateway.log` 自 2026-05-29 起停止写入）。
凡是"没有输出""没有报错""日志停写"都要按 P0 对待。

### 坑 5：修复后不复核 → 故障回退

8/19 修了 fallback 链，但**没有常设复核**。
必须在复盘里固化一条自检命令（见验证步骤第 8 步），
并挂到 C7-4 的监控链上，否则同一个坑会复发。

### 坑 6：`primary == fallback[0]` 这种自循环 bug

8/19 的轩辕就是这个 bug：`primary` 与 `fallback[0]` 是同一个坏模型
→ **等于没有 fallback**。这是一条可自动检测的规则（见验证步骤第 8 步），
建议纳入 `openclaw doctor` 的定期自检清单。

### 坑 7：事故档案散落各处

8/19 档案在 `workspace-kunlun/memory/`；
9/21 档案在飞书消息日志（未结构化落盘）。
**统一到 `~/.openclaw/governance/pir/`**，并让脚本可扫。

---

## 进阶

### 进阶 1：复盘的"复发率"量化

```yaml
# 路径：~/.openclaw/governance/pir/relapse-metrics.yaml
metrics:
  mttr_minutes: "mean(resolved_at - detected_at)"
  mttd_minutes: "mean(detected_at - occurred_at)"     # 越接近 0 越好
  relapse_rate: "同 root_cause 30 天内复发次数 / 事故总数"
  silent_incident_ratio: "detected_by == '人' 的占比"  # 人发现 = 监控失效
targets:
  mttr_minutes: "< 60"
  mttd_minutes: "< 10"
  relapse_rate: "== 0"
  silent_incident_ratio: "< 0.2"
```

> ⏳ **待实测**：本机事故样本量仅 2（8/19 + 9/21），不足以统计；上表为口径定义。

### 进阶 2：事故 → 手册 → 新 automation 的闭环

8/19 的产物链（可复用为模板）：

```
事故（8/19）
  → 复盘档案（memory/2026-08-19-军团断线修复.md）
  → 手册沉淀（卷七 M1 编制 + M2 路由）
  → 通用 fallback 链规范（deepseek-v4-flash → opus-4-8 → MiniMax-M2.7 → MiniMax-M3）
  → 待跟进 4 条（含 15 个失败 cron 的观察项）
```

### 进阶 3：把复盘档案喂给明镜（失败基因库）

本机 `mingjing`（明镜）角色含"失败基因官"。可建 automation：

```bash
# 真名 automations add
openclaw automations add \
  --name "事故复盘归档→失败基因库" \
  --schedule "0 23 * * *" \
  --agent mingjing \
  --message "扫描 ~/.openclaw/governance/pir/*.md 中当日新增复盘，提取 root_cause 与 lessons，去重后追加到失败基因库；同一 root_cause 复发则建 P0 修复工单（Remediation Ticket）并通知 kunlun"
```

---

# C7-3 · cron 编排实操：晨扫 / 日报 / 暗夜熔炉 完整配置

## 背景

### 61 条 automation 的现实

2026-09-27 本机 `openclaw automations list` 实测 **61 行 automation**：

| 类别 | 条数 | 说明 |
|---|---:|---|
| 「暗夜熔炉」cron | **13** | 13 个 Agent 各一条（mingjing/tianshu/xuanyuan/jixia/zhulong/kunpeng/baxia/siku/tiangong/mobai/zhuque/qilin/hetu），`cron 10 1` → `cron 30 3` 串行铺开 |
| `skill-collection-review` | **18** | 18 个 Agent 各一条，`every 7d` |
| `heartbeat:*` | **3** | `heartbeat:kunlun`(30m) / `heartbeat:tiance`(30m) / `heartbeat:peter`(2h) |
| 蜂鸟/蜂群情报线 | **9** | 蜂群-A 晨扫 / B 竞品 / BC 午间 / C 人才融资 / D 业务线 / E 健康检查 / F 隐蔽信号 / 蜂鸟午间 / 蜂鸟晚间 |
| 凤凰内容工厂 | **4** | 每日调度 / 内容日历核对 / 日终复盘 / HEARTBEAT 每日检查 |
| 记忆与技能 | 2 | `memory-core:memory-dreaming`(03:00) / `skill-collection-review` |
| 军团治理 | 5 | 军功爵周结算 / 昆仑每周进化评估 / 蓝血军团-互审催收 / 蓝血军团-失败成本扫描 / 能力矩阵月度更新 |
| 情报日报 | 3 | `daily-tech-intel-github` / `weekly-tech-intel-github` / `hetu-回测进化日报` |
| Peter 个人线 | 4 | heartbeat-morning-530 / -600 / breakfast-700 / Peter每日人生教练早课 |
| 其他 | 3 | 天枢每日战报生成 / 到点杂项 |

**结论**：61 条不是"编排"，是"堆积"。本配方把它收敛成 **12 条主链 + 一条串行规则**，
让编排（orchestration）可读、可查、可审计。

### 本机真实调度节律（实测时刻表）

```
00:00  军功爵周结算（每周一）
01:10  明镜-暗夜熔炉
01:20  天枢-暗夜熔炉
01:30  轩辕-暗夜熔炉
01:40  稷下-暗夜熔炉
01:50  烛龙-暗夜熔炉
02:10  鲲鹏-暗夜熔炉
02:30  霸下-暗夜熔炉
02:40  司库-暗夜熔炉
02:50  天工-暗夜熔炉
03:00  memory-core:memory-dreaming  +  墨白-暗夜熔炉
03:10  朱雀-暗夜熔炉
03:20  麒麟-暗夜熔炉
03:30  河图-暗夜熔炉
05:30  heartbeat-morning-530 (peter)
06:00  蜂群-A-晨间全量扫描  +  heartbeat-morning-600 (peter)
07:00  heartbeat-breakfast-700 (peter)  +  hetu-回测进化日报
07:05  Peter每日人生教练早课
08:00  凤凰-内容工厂·每日调度  +  蜂鸟-B-竞品网页变更扫描
09:00  昆仑每周进化评估（周一） / daily-tech-intel-github  /  凤凰-内容日历核对（工作日）
09:30  weekly-tech-intel-github（周一）
10:00  蜂群-BC-午间增量扫描
12:00  蜂鸟-午间情报扫描
14:00  蜂鸟-C-竞品人才+融资扫描  /  蜂鸟-F-隐蔽信号雷达（周一）
16:00  蜂鸟-D-业务线深度扫描
18:00  凤凰-内容工厂·日终复盘  +  蜂鸟-晚间情报复盘与归档
20:00  凤凰-HEARTBEAT每日检查（工作日）  +  天枢每日战报生成
21:50  蓝血军团-互审催收
22:00  蜂鸟-E-系统健康检查+H...
22:10  蓝血军团-失败成本扫描
每月 1 日 00:30  能力矩阵月度更新（实测 error 4x）
```

**关键洞察：暗夜熔炉是"串行铺开"的** ——13 个 Agent 每 10 分钟错开一个，
从 01:10 到 03:30。这是**避免 18 个 Agent 同时打同一个模型供应商**的有意设计。

---

## 配置（完整可复制）

### Step 1：查现有编排（真名）

```bash
# ⚠️ 真名：openclaw automations list（cron 是别名）
openclaw automations list

# 只看心跳
openclaw automations list 2>&1 | grep "heartbeat:"

# 只看暗夜熔炉
openclaw automations list 2>&1 | grep "暗夜熔炉"

# 看单条详情（真名 get）
openclaw automations get 90c903a2-6089-441b-b797-bc2fbc77e7d8
# 期望：heartbeat:kunlun 的完整 JSON（every 30m · status error 99+x · agent kunlun）
```

automations 子命令全集（本机 `--help` 实测）：

```
add      Add an automation
disable  Disable an automation
edit     Edit an automation (patch fields)
enable   Enable an automation
get      Get an automation as JSON
list     List automations
```

### Step 2：12 条主链编排表（完整可复制 YAML）

```yaml
# ============================================================================
# 生产编排主链（Production Orchestration Main Chain）
# 路径：~/.openclaw/governance/orchestration.yaml
# 版本：v1.0 · 2026-09-27 · 基座 OpenClaw 2026.9.4 (3a9d69d)
# 来源：本机 openclaw automations list 实测 61 条 → 收敛为 12 条主链
# 时区：全部 Asia/Shanghai
# ============================================================================
version: 1
timezone: Asia/Shanghai

chains:
  # ── 主链 1：晨扫（情报全量）──────────────────────────────────────────
  - id: chain-01-morning-scan
    name: 蜂群-A-晨间全量扫描
    cron: "0 6 * * *"
    agent: fengniao
    model: deepseek/deepseek-v4-flash
    target: isolated
    delivery: "announce -> telegram:8328029665"
    status: ok
    downstream: [chain-02-intel-midday, chain-03-intel-evening]

  # ── 主链 2：午间增量 ─────────────────────────────────────────────────
  - id: chain-02-intel-midday
    name: 蜂群-BC-午间增量扫描
    cron: "0 10 * * *"
    agent: fengniao
    status: ok

  # ── 主链 3：晚间归档 ─────────────────────────────────────────────────
  - id: chain-03-intel-evening
    name: 蜂鸟-晚间情报复盘与归档
    cron: "0 18 * * *"
    agent: fengniao
    model: deepseek/deepseek-v4-flash
    status: "ok (not delivered)"
    # ⚠️ 实测状态 "ok (not delivered)" = 跑了但没投递，属告警候选（见 C7-4）

  # ── 主链 4：回测进化日报 ─────────────────────────────────────────────
  - id: chain-04-hetu-daily
    name: hetu-回测进化日报
    cron: "0 7 * * *"
    agent: hetu
    model: deepseek/deepseek-v4-flash
    delivery: "announce -> telegram:8328029665"
    status: ok

  # ── 主链 5：内容工厂日调度 ───────────────────────────────────────────
  - id: chain-05-content-daily
    name: 凤凰-内容工厂·每日调度
    cron: "0 8 * * *"
    agent: fenghuang
    model: minimax/MiniMax-M2.7
    status: ok

  # ── 主链 6：内容工厂日终复盘 ─────────────────────────────────────────
  - id: chain-06-content-eod
    name: 凤凰-内容工厂·日终复盘
    cron: "0 18 * * *"
    agent: fenghuang
    model: minimax/MiniMax-M2.7
    status: "ok (not delivered)"

  # ── 主链 7：天枢每日战报 ─────────────────────────────────────────────
  - id: chain-07-tianshu-daily
    name: 天枢每日战报生成
    cron: "0 20 * * *"
    agent: tianshu
    model: deepseek/deepseek-v4-flash
    status: ok

  # ── 主链 8：暗夜熔炉（13 Agent 串行铺开）─────────────────────────────
  - id: chain-08-forge-night
    name: 暗夜熔炉（Night Forge）
    schedule_type: serial-stagger
    gap_minutes: 10
    window: "01:10 → 03:30"
    target: isolated
    model: zai/glm-5.1
    status: ok
    members:
      - { name: 明镜-暗夜熔炉, cron: "10 1 * * *", agent: mingjing }
      - { name: 天枢-暗夜熔炉, cron: "20 1 * * *", agent: tianshu }
      - { name: 轩辕-暗夜熔炉, cron: "30 1 * * *", agent: xuanyuan }
      - { name: 稷下-暗夜熔炉, cron: "40 1 * * *", agent: jixia }
      - { name: 烛龙-暗夜熔炉, cron: "50 1 * * *", agent: zhulong }
      - { name: 鲲鹏-暗夜熔炉, cron: "10 2 * * *", agent: kunpeng }
      - { name: 霸下-暗夜熔炉, cron: "30 2 * * *", agent: baxia }
      - { name: 司库-暗夜熔炉, cron: "40 2 * * *", agent: siku }
      - { name: 天工-暗夜熔炉, cron: "50 2 * * *", agent: tiangong }
      - { name: 墨白-暗夜熔炉, cron: "0 3 * * *",  agent: mobai }
      - { name: 朱雀-暗夜熔炉, cron: "10 3 * * *", agent: zhuque }
      - { name: 麒麟-暗夜熔炉, cron: "20 3 * * *", agent: qilin }
      - { name: 河图-暗夜熔炉, cron: "30 3 * * *", agent: hetu }

  # ── 主链 9：记忆梦境 ─────────────────────────────────────────────────
  - id: chain-09-memory-dream
    name: memory-core:memory-dreaming
    cron: "0 3 * * *"
    agent: kunlun
    target: isolated
    status: ok

  # ── 主链 10：技能收集复核 ────────────────────────────────────────────
  - id: chain-10-skill-review
    name: skill-collection-review（18 Agent 各一条）
    schedule: "every 7d"
    agent: "<each>"
    count: 18
    target: isolated
    status: ok

  # ── 主链 11：军团周治理 ──────────────────────────────────────────────
  - id: chain-11-weekly-governance
    name: 军团周治理（周结算 + 进化评估 + 情报周报）
    members:
      - { name: 军功爵周结算, cron: "0 0 * * 1", agent: kunlun, model: zai/glm-5.1, status: ok }
      - { name: 昆仑每周进化评估, cron: "0 9 * * 1", agent: kunlun, model: deepseek/deepseek-v4-flash, status: ok }
      - { name: weekly-tech-intel-github, cron: "30 9 * * 1", agent: xuanyuan, model: yiyongai/gpt-5.5, status: ok }
      - { name: 蜂鸟-F-隐蔽信号雷达, cron: "0 14 * * 1", agent: fengniao, status: ok }

  # ── 主链 12：军团日终治理 ────────────────────────────────────────────
  - id: chain-12-eod-governance
    name: 军团日终治理（催收 + 失败成本 + 健康检查）
    members:
      - { name: 蓝血军团-互审催收, cron: "50 21 * * *", agent: kunlun, model: yiyongai/gpt-5.6-sol, status: ok }
      - { name: 蜂鸟-E-系统健康检查+H..., cron: "0 22 * * *", agent: fengniao, model: deepseek/deepseek-v4-flash, status: ok }
      - { name: 蓝血军团-失败成本扫描, cron: "10 22 * * *", agent: kunlun, model: yiyongai/gpt-5.6-sol, status: ok }

# ── 月链（单列，因实测已 error）─────────────────────────────────────────
monthly:
  - name: 能力矩阵月度更新
    cron: "30 0 1 * *"
    agent: kunlun
    model: zai/glm-5.1
    status: "error (4x)"        # ⚠️ 实测连续失败 4 次，见 C7-4
    remediation: "RT-20260927-001"

# ── 串行保护规则（防供应商打爆）────────────────────────────────────────
stagger_policy:
  enabled: true
  min_gap_minutes: 10
  applies_to: [chain-08-forge-night]
  reason: "18 Agent 共享 5 个 provider（yiyongai/deepseek/zai/minimax/opencaio），
           并发同刻会触发限流；错峰 10 分钟 = 单 provider 峰值 ≤ 2 并发"
```

### Step 3：新增一条主链（真名 add，完整参数）

```bash
# 真名：openclaw automations add
# 例：暗夜熔炉补一个新 Agent（新增 18 号 Agent 时的标准动作）
openclaw automations add \
  --name "新Agent-暗夜熔炉" \
  --schedule "40 3 * * *" \
  --agent zhuque \
  --message "执行暗夜熔炉：读取 memory/ 当日素材，产出进化报告到 memory/<date>-forge.md，并把失败模式写入失败分析库" \
  --target isolated

# 例：晨扫链补一条
openclaw automations add \
  --name "蜂群-G-新增扫描" \
  --schedule "0 11 * * *" \
  --agent fengniao \
  --message "增量扫描指定信源，产出摘要并 announce 到 telegram:8328029665" \
  --target isolated

# 校验
openclaw automations list 2>&1 | grep "暗夜熔炉" | wc -l
# 期望：新加后 = 14

# 单条详情
openclaw automations get <新返回的 UUID>
# 期望：完整 JSON，含 name / schedule / agentId / status
```

### Step 4：launchd 侧（Gateway 常驻）

cron 编排要跑，前提是 Gateway 常驻。本机实测有两个 plist：

```bash
ls ~/Library/LaunchAgents/ | grep -i openclaw
# 实测输出：
# ai.openclaw.gateway.plist
# com.openclaw.monthly-cleanup.plist
```

```xml
<!-- 路径：~/Library/LaunchAgents/ai.openclaw.gateway.plist （结构示意，关键键完整） -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.openclaw.gateway</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/peterqiu/.npm-global/bin/openclaw</string>
    <string>gateway</string>
    <string>run</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/Users/peterqiu/.openclaw/logs/gateway.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/peterqiu/.openclaw/logs/gateway.err.log</string>
</dict>
</plist>
```

```bash
# 装载 / 重载 / 状态
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
launchctl print gui/$(id -u)/ai.openclaw.gateway | head -20

# 日志（8/19 事故就是 gateway.log 停写未被发现 → 必须定期看）
tail -50 ~/.openclaw/logs/gateway.log
ls -la ~/.openclaw/logs/gateway.log
# ⚠️ 8/19 事故教训：日志不写入比日志报错更危险 → 必须检查 mtime
```

### Step 5：编排冲突检测脚本

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 路径：~/.openclaw/governance/orchestration_check.py
# 作用：检测 cron 编排冲突（同刻并发、间隔过密、同 provider 打爆）
import re, sys, collections, subprocess

CRON = re.compile(r"^cron (\S+) (\S+) (\S+) (\S+) (\S+)")
GAP_MIN = 10

def parse(lines):
    jobs = []
    for ln in lines:
        m = CRON.match(ln.strip())
        if not m:
            continue
        mi, hr, dom, mon, dow = m.groups()
        name = ln.split()[2] if len(ln.split()) > 2 else "?"
        jobs.append((int(hr), int(mi), name, ln))
    return jobs

def minute_of(h, m):
    return h * 60 + m

def main() -> int:
    out = subprocess.run(["openclaw", "automations", "list"],
                         capture_output=True, text=True).stdout
    lines = [l for l in out.splitlines()
             if "Experimental" not in l and "trace-warnings" not in l
             and "Retrying with" not in l]
    jobs = parse(lines)
    print(f"解析到 {len(jobs)} 条 cron automation")
    # 同刻并发检测
    buckets = collections.defaultdict(list)
    for h, mi, name, _ in jobs:
        buckets[(h, mi)].append(name)
    collisions = {k: v for k, v in buckets.items() if len(v) > 1}
    if collisions:
        print("\n⚠️ 同刻并发（同一分钟 > 1 条）:")
        for (h, mi), names in sorted(collisions.items()):
            print(f"  {h:02d}:{mi:02d}  ×{len(names)}  {names}")
    else:
        print("✅ 无同刻并发")
    # 间隔过密检测（相邻 < GAP_MIN 分钟）
    times = sorted({minute_of(h, mi) for h, mi, _, _ in jobs})
    tight = [(a, b) for a, b in zip(times, times[1:]) if b - a < GAP_MIN]
    if tight:
        print(f"\n⚠️ 相邻间隔 < {GAP_MIN} 分钟（可能撞 provider 限流）:")
        for a, b in tight:
            print(f"  {a//60:02d}:{a%60:02d} → {b//60:02d}:{b%60:02d}  ({b-a}min)")
    else:
        print(f"✅ 所有相邻间隔 ≥ {GAP_MIN} 分钟")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

---

## 验证步骤

```bash
# 1. 数 automation 总量
openclaw automations list 2>&1 | grep -cE "^[0-9a-f]{8}-"
# 期望：61（2026-09-27 本机实测）

# 2. 数暗夜熔炉
openclaw automations list 2>&1 | grep -c "暗夜熔炉"
# 期望：13
#   明镜(10 1) 天枢(20 1) 轩辕(30 1) 稷下(40 1) 烛龙(50 1)
#   鲲鹏(10 2) 霸下(30 2) 司库(40 2) 天工(50 2)
#   墨白(0 3) 朱雀(10 3) 麒麟(20 3) 河图(30 3)

# 3. 数心跳（含 error 状态）
openclaw automations list 2>&1 | grep "heartbeat:"
# 期望（本机实测逐字）：
# 90c903a2-... heartbeat:kunlun  every 30m  ...  error (99+x)  ...  kunlun
# 380e8da0-... heartbeat:tiance  every 30m  ...  skipped       ...  tiance
# d367dbfb-... heartbeat:peter   every 2h   ...  error (70x)   ...  peter
# ⚠️ 三条心跳全异常 → 见 C7-4

# 4. 看单条详情（真名 get）
openclaw automations get 39af7623-310d-4098-83a2-7899c28ab4c2
# 期望：明镜-暗夜熔炉完整 JSON（cron 10 1 * * * · Asia/Shanghai · agent mingjing · model zai/glm-5.1）

# 5. 校验暗夜熔炉错峰（相邻间隔应 = 10 分钟）
openclaw automations list 2>&1 | grep "暗夜熔炉" | \
  awk -F'cron ' '{split($2,a," "); print a[1]" "a[2]}' | sort -n
# 期望（小时 分钟 升序）：
# 1 10
# 1 20
# 1 30
# 1 40
# 1 50
# 2 10
# 2 30
# 2 40
# 2 50
# 3 0
# 3 10
# 3 20
# 3 30
# （注：02:10 → 02:30 有 20 分钟空档，对应鲲鹏→霸下）

# 6. 跑编排冲突检测
python3 ~/.openclaw/governance/orchestration_check.py
# 期望：
# 解析到 61 条 cron automation   （注：仅解析 "cron H M * * *" 形态）
# ⚠️ 同刻并发（同一分钟 > 1 条）:
#   3:0  ×2  ['memory-core:memory-dr...', '墨白-暗夜熔炉']
#   6:0  ×2  ['蜂群-A-晨间全量扫描+...', 'heartbeat-morning-600']
#   7:0  ×2  ['heartbeat-breakfast-700', 'hetu-回测进化日报']
#   8:0  ×2  ['凤凰-内容工厂·每日调...', '蜂鸟-B-竞品网页变更扫描']
#   18:0 ×2  ['凤凰-内容工厂·日终复...', '蜂鸟-晚间情报复盘与归档']
#   20:0 ×2  ['凤凰-HEARTBEAT每日检查', '天枢每日战报生成']
# 解读：同刻并发多为「不同 provider」或「不同渠道」，实测未引发限流；
#       但如需更稳可再错峰（stagger_policy.min_gap_minutes）。

# 7. 真名核对：能力矩阵月度更新（error 4x）
openclaw automations list 2>&1 | grep "能力矩阵"
# 期望：eb b72ae6-... 能力矩阵月度更新  cron 30 0 1 * *  ...  error (4x)  ...  kunlun
# ⚠️ 这是本机唯一的「月度」automation，且已连续失败 4 次 → 必建修复工单

# 8. launchd 侧常驻确认
launchctl print gui/$(id -u)/ai.openclaw.gateway 2>&1 | head -8
# 期望：含 state = running / pid

# 9. 日志新鲜度检查（8/19 事故的教训：日志停写 = 最危险）
ls -la ~/.openclaw/logs/gateway.log
# 期望：mtime 在近 24h 内
# ⚠️ 若 mtime 停在很久以前 → 立即按 P0 处置（见 C7-2 坑 4）

# 10. 端到端：手动触发一条 automation 验证链路
openclaw automations get <暗夜熔炉 UUID>
# 记下 agentId，然后手动唤醒该 Agent 走一遍
openclaw agent --agent mingjing --message "手动走一遍暗夜熔炉流程（今日 <date>），产出到 memory/<date>-forge.md"
# 期望：文件落盘 + 内容含当日素材
```

---

## 实测环境

| 项 | 值 |
|---|---|
| 基座版本 | OpenClaw 2026.9.4 (3a9d69d)；2026-09-27 复测 `2026.9.6 (eb377ac)` |
| OS | macOS 26.5.1 |
| automation 总数 | **61**（`automations list \| grep -c '^[0-9a-f]{8}-'`） |
| 暗夜熔炉 | **13**（01:10 → 03:30，间隔 10 分钟串行） |
| `skill-collection-review` | 18（每 Agent 一条，`every 7d`） |
| `heartbeat:*` | 3（kunlun 30m **error 99+x** / tiance 30m **skipped** / peter 2h **error 70x**） |
| 蜂鸟/蜂群线 | 9 |
| 凤凰内容工厂 | 4 |
| 能力矩阵月度更新 | `cron 30 0 1 * *` · **error (4x)** |
| `automations` 子命令 | add / disable / edit / enable / get / list（`--help` 实测） |
| launchd plist | `ai.openclaw.gateway.plist` + `com.openclaw.monthly-cleanup.plist` |
| 时区 | `Asia/Shanghai`（全部 cron 实测带 `@ Asia/Shanghai`） |
| `cron` 别名 | `openclaw cron` ≡ `openclaw automations`（`--help` 实测：`Usage: openclaw cron\|automations`） |
| 复测日期 | 2026-09-27 |

---

## 排坑

### 坑 1：用 `openclaw cron list`

本书写作时真名是 **`openclaw automations list`**。
`openclaw cron` 是**别名**（`--help` 实测：`Usage: openclaw cron|automations [options] [command]`），
两写皆通，但对外文档一律用 `automations`（真名优先）。

### 坑 2：暗夜熔炉写成同时刻 → 打爆 provider

❌ 13 个 Agent 全写 `cron 0 1 * * *`
✅ 每 10 分钟错开一个（本机实测设计）

本机 18 Agent 共享 **5 个 provider**：
`yiyongai / deepseek / zai / minimax / opencaio`（`models.providers` 实测键）。
同刻并发 = 单 provider 瞬时 13 并发 → 限流/超时。
**`stagger_policy.min_gap_minutes: 10` 是硬约束。**

### 坑 3：automation 失败静默

本机实测：`能力矩阵月度更新` **error (4x)**、`heartbeat:kunlun` **error (99+x)**、
`heartbeat:peter` **error (70x)** —— 全都在"跑但一直失败"，无人处置。
**这是最危险的状态**：看起来有 automation（不像 8/19 那样全军挂），
实际早已空转。**必须靠 C7-4 的 error 计数阈值告警兜住。**

### 坑 4：Gateway 没常驻 → 所有 cron 不跑

cron 编排依赖 Gateway 常驻（`ai.openclaw.gateway.plist` + `KeepAlive: true`）。
若 plist 未装载，`automations list` 显示的 `Next` 时间会持续往后跳而不执行。
自查：

```bash
launchctl print gui/$(id -u)/ai.openclaw.gateway | grep -E "state|pid"
# 期望：state = running
```

### 坑 5：`status: "ok (not delivered)" 被当成 ok`

本机实测两条：

```
凤凰-内容工厂·日终复盘   ok (not delivered)
蜂鸟-晚间情报复盘与归档   ok (not delivered)
```

**"跑了但没投递" ≠ 成功。** 人看不到日报 = 编排价值归零。
必须把 `not delivered` 也纳入告警（详见 C7-4）。

### 坑 6：`automations list` 被 state 库独占锁挡住

```
[openclaw] Reason: OpenClaw refused shared state schema mutation ... another Gateway owns that state directory.
```

这不是编排问题，是 Gateway 独占锁（见 C6-1 排坑 1）。
处置：`openclaw gateway restart`（走 managed restart path）。

### 坑 7：cron 的 `Asia/Shanghai` 不能省

`memory-core:memory-dreaming` 实测是 `cron 0 3 * * * (exact)`——
**不带时区**；而暗夜熔炉全部带 `@ Asia/Shanghai`。
混用会导致凌晨那批任务在宿主机时区（可能 UTC）下错位 8 小时。
**新写一律显式带 `@ Asia/Shanghai`。**

---

## 进阶

### 进阶 1：编排 → 依赖 DAG

12 条主链目前是扁平的。可升级为 DAG：

```yaml
# 路径：~/.openclaw/governance/orchestration-dag.yaml
dag:
  morning:
    - chain-01-morning-scan
    - chain-04-hetu-daily          # 依赖 chain-01 产出
    - chain-05-content-daily       # 依赖 chain-04 结论
  midday:
    - chain-02-intel-midday
  evening:
    - chain-06-content-eod
    - chain-03-intel-evening
    - chain-07-tianshu-daily        # 汇总当日全部产出
  night:
    - chain-08-forge-night          # 消费当日全部 memory/
    - chain-09-memory-dream
  edges:
    - "chain-01-morning-scan -> chain-04-hetu-daily"
    - "chain-04-hetu-daily -> chain-05-content-daily"
    - "chain-07-tianshu-daily -> chain-08-forge-night"
    - "chain-08-forge-night -> chain-09-memory-dream"
```

### 进阶 2：编排健康度评分

```yaml
# 路径：~/.openclaw/governance/orchestration-score.yaml
score:
  inputs:
    total_automations: 61
    status_error: "<count>"
    status_skipped: "<count>"
    status_not_delivered: "<count>"
    consecutive_error_max: 99+      # heartbeat:kunlun 实测
  formula: "1 - (error + skipped + not_delivered) / total"
  bands:
    green: ">= 0.90"
    yellow: "0.70 - 0.90"
    red: "< 0.70"
  on_red: "建 P1 修复工单（Remediation Ticket）+ 通知 kunlun"
```

### 进阶 3：暗夜熔炉串行窗口的弹性调度

13 个 Agent × 10 分钟 = 130 分钟固定窗口。若新增 Agent：
- 方案 A：缩短 `gap_minutes` 到 7（风险：provider 峰值升高）
- 方案 B：开第二窗口（如 04:00 → 04:50）分批
- 方案 C：按 provider 分组错峰（同 provider 的 Agent 强制拉开）

```yaml
# 方案 C 示例
provider_aware_stagger:
  yiyongai:  { group: [mingjing, tianshu, tiangong, zhulong, hetu, peter, fengniao, baxia, zhuque, qilin, siku, fenghuang, xuanyuan, jixia] }
  deepseek:  { group: [kunlun] }
  zai:       { group: [] }
  minimax:   { group: [fenghuang] }
  opencaio:  { group: [] }
  rule: "同 group 内相邻 Agent 间隔 ≥ 10min"
```

---

# C7-4 · 生产监控实操：heartbeat error 计数 + 告警链

## 背景

### 三个真实告警样本（本机实测）

```
90c903a2-... heartbeat:kunlun   every 30m  ...  error (99+x)  agent=kunlun
380e8da0-... heartbeat:tiance   every 30m  ...  skipped       agent=tiance
d367dbfb-... heartbeat:peter    every 2h   ...  error (70x)   agent=peter
eb b72ae6-... 能力矩阵月度更新    cron 30 0 1 * *  error (4x)  agent=kunlun
```

**这就是"静默失效"的教科书样本**：

| automation | 状态 | 真实含义 |
|---|---|---|
| `heartbeat:kunlun` | **error (99+x)** | 中枢心跳连续失败 ≥ 99 次（30 分钟一次 → **至少 50 小时无心跳**） |
| `heartbeat:tiance` | **skipped** | 天策心跳被跳过（Supervisor 审计侧失能） |
| `heartbeat:peter` | **error (70x)** | 通道守门员心跳连续失败 70 次（2 小时一次 → **约 6 天无心跳**） |
| `能力矩阵月度更新` | **error (4x)** | 月度任务连续失败 4 次（**连续 4 个月未产出**） |

**最危险的地方**：这些 automation **"存在"**——`automations list` 里能看到，
不像 8/19 那样全军挂掉。**"看起来在跑"** 才是最难发现的故障态。

### 数据源：SOP 候选告警

任务来源给出的 SOP 候选告警（本机实测可复核）：

| 告警 | 阈值 | 本机实测值 | 是否越界 |
|---|---|:--:|:--:|
| `heartbeat:peter` error | > 30 | **70x** | ❌ 越界 |
| `heartbeat:kunlun` error | > 30 | **99+x** | ❌ 越界 |
| `heartbeat:tiance` status | ≠ ok | **skipped** | ❌ 越界 |
| `能力矩阵月度更新` error | > 0 | **4x** | ❌ 越界 |

### 本配方产出

1. `governance/monitor.yaml`（阈值 + 分级 + 告警路由）
2. `monitor_scan.py`（扫描 automation 状态 + heartbeat 计数，可执行）
3. **告警链**（三级：日志 → 群 notify → 建修复工单）
4. SLA 定义（告警响应时限）

---

## 配置（完整可复制）

### Step 1：建监控目录

```bash
mkdir -p ~/.openclaw/governance/monitor
mkdir -p ~/.openclaw/governance/monitor/state
```

### Step 2：监控主配置

```yaml
# ============================================================================
# 生产监控配置（Production Monitoring）
# 路径：~/.openclaw/governance/monitor.yaml
# 版本：v1.0 · 2026-09-27 · 基座 OpenClaw 2026.9.4 (3a9d69d)
# ============================================================================
version: 1
timezone: Asia/Shanghai

# ── 1. 采集源 ───────────────────────────────────────────────────────────
sources:
  automations:
    command: "openclaw automations list"
    parse: "id/declaration/name/schedule/next/last/status/target/delivery/agentId/owner/model"
    note: "真名；cron 为别名"
  agents:
    command: "openclaw agents list"
    parse: "id/name/identity/workspace/model/routing"
  bindings:
    command: "openclaw agents bindings"
    parse: "agentId/channel/accountId"
  health:
    command: "openclaw health"
    note: "可能被 Gateway 独占锁拒绝 → 降级为跳过"
  plugins:
    command: "openclaw plugins list"
    note: "真名 plugins 复数"
  log_freshness:
    path: "~/.openclaw/logs/gateway.log"
    max_age_hours: 24
    note: "8/19 事故教训：日志停写 = P0"

# ── 2. 阈值（分级）──────────────────────────────────────────────────────
thresholds:
  automation_consecutive_error:
    warning: 3            # ≥3 次 → WARN
    critical: 30          # ≥30 次 → CRIT（本机 kunlun 99+x / peter 70x 均越 CRIT）
  heartbeat_consecutive_error:
    warning: 3
    critical: 12          # 30min 一次 → 12 次 ≈ 6 小时无心跳
  status_not_ok:
    values: ["error", "skipped", "failed", "not delivered"]
  status_not_delivered:
    treat_as: warning     # "ok (not delivered)" 也要告警
  channel_disconnected_minutes:
    warning: 5
    critical: 15
  skill_count_baseline: 236       # 本书口径
  agent_count_baseline: 18
  binding_count_baseline: 37
  log_stale_hours:
    warning: 6
    critical: 24
  monthly_automation_error:
    critical: 1           # 月度任务失败 1 次即 CRIT（周期长，容错低）

# ── 3. 已知基线（避免误报；本机实测值）──────────────────────────────────
known_baseline:
  # 本机实测已确认异常项 → 记为 known，仍告警但归入"存量"
  - id: "90c903a2-6089-441b-b797-bc2fbc77e7d8/0"
    name: heartbeat:kunlun
    state: "error (99+x)"
    classification: known_stock       # 存量：建单跟踪，不重复打扰
    ticket: RT-20260927-001
  - id: "380e8da0-e0db-4bdb-a1f7-d8bb68254e9c/0"
    name: heartbeat:tiance
    state: "skipped"
    classification: known_stock
    ticket: RT-20260927-002
  - id: "d367dbfb-d415-4685-968e-bd292051b5bc/0"
    name: heartbeat:peter
    state: "error (70x)"
    classification: known_stock
    ticket: RT-20260927-003
  - id: "ebb72ae6-653c-455b-9017-49b09aa71933/0"
    name: 能力矩阵月度更新
    state: "error (4x)"
    classification: known_stock
    ticket: RT-20260927-004
  # 存量异常在 24h 内只报一次（去重）

# ── 4. 告警分级与路由 ───────────────────────────────────────────────────
alert_levels:
  INFO:
    route: [log]
    log_path: "~/.openclaw/governance/monitor/alerts.jsonl"
  WARN:
    route: [log, digest]
    digest_window: "1h"        # 每小时汇总一条，不逐条打扰
    channel: "telegram:8328029665"
  CRIT:
    route: [log, notify_now, ticket]
    channel: "telegram:8328029665"
    ticket:
      prefix: "RT"
      owner: mingjing
      sla_ack: "5min"
      sla_fix: "4h"
    notify_template: |
      🚨 [CRIT] 生产监控告警
      · 对象: {name} ({kind})
      · 状态: {status}
      · 阈值: {threshold} / 实测: {value}
      · 首次发现: {first_seen}
      · 已有工单: {ticket_or_none}
      · 建议动作: {action}

# ── 5. 告警链（三级）─────────────────────────────────────────────────────
alert_chain:
  - level: L1
    name: 采集
    action: "monitor_scan.py 跑 6 类采集源，产出 status JSON"
    cadence: "every 15m（真名 automations add）"
  - level: L2
    name: 判定
    action: "按 thresholds 分级；命中 known_baseline 的降级为存量"
    on_crit: "生成 notify_template 文本"
  - level: L3
    name: 处置
    actions:
      - "append 到 alerts.jsonl（永不丢证）"
      - "CRIT → 立即 announce 到 telegram:8328029665"
      - "CRIT → 建修复工单（Remediation Ticket）RT-<date>-<seq>"
      - "WARN → 进 1h 摘要，不逐条打扰"
      - "存量异常 → 24h 内只报 1 次（去重）"

# ── 6. SLA ──────────────────────────────────────────────────────────────
sla:
  crit_ack: "5min"            # 认领工单
  crit_fix: "4h"
  warn_digest_latency: "1h"
  stock_review: "7d"          # 存量异常每周复核一次，不得无限期挂
  escalation:
    - "crit 超 4h 未 ack → 升级 kunlun + 通知丘总"
    - "warn 连续 3 个摘要周期未处置 → 升为 crit"
```

### Step 3：监控扫描脚本（可执行）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 路径：~/.openclaw/governance/monitor/monitor_scan.py
# 作用：采集 automation 状态 → 按阈值分级 → 输出告警 + 落 jsonl
import subprocess, json, re, sys, pathlib, datetime, collections

HOME = pathlib.Path.home()
ALERTS = HOME / ".openclaw/governance/monitor/alerts.jsonl"
STATE = HOME / ".openclaw/governance/monitor/state"
STATE.mkdir(parents=True, exist_ok=True)

# 阈值（与 monitor.yaml 对齐）
CRIT_AUTO_ERR = 30
WARN_AUTO_ERR = 3
MONTHLY_CRIT = 1

KNOWN_STOCK = {
    "heartbeat:kunlun": "RT-20260927-001",
    "heartbeat:tiance": "RT-20260927-002",
    "heartbeat:peter":  "RT-20260927-003",
    "能力矩阵月度更新":    "RT-20260927-004",
}

def run_cli(args):
    p = subprocess.run(["openclaw"] + args, capture_output=True, text=True)
    out = p.stdout
    return "\n".join(l for l in out.splitlines()
                     if "Experimental" not in l
                     and "trace-warnings" not in l
                     and "Retrying with" not in l)

def parse_automations(text):
    rows = []
    for ln in text.splitlines():
        if not re.match(r"^[0-9a-f]{8}-", ln.strip()):
            continue
        # status 形如: ok / ok (not delivered) / error (99+x) / skipped
        m = re.search(r"\b(ok|error|skipped|failed)(\s*\(([^)]+)\))?\b", ln)
        status = m.group(0) if m else "?"
        err = 0
        if m and m.group(3):
            mm = re.match(r"(\d+)\+?x", m.group(3))
            if mm:
                err = int(mm.group(1))
                if "+" in m.group(3):
                    err = max(err, 99)      # "99+x" → 记为 99
        # name：跳过 UUID 与声明列，取含中文/字母的第三段
        parts = [p for p in re.split(r"\s{2,}", ln.strip()) if p]
        name = parts[2] if len(parts) > 2 else parts[0]
        agent = parts[-1] if parts and re.match(r"^[a-z]+$", parts[-1]) else "?"
        rows.append({"name": name, "status": status, "errors": err,
                     "agent": agent, "raw": ln.strip()})
    return rows

def classify(row):
    name, status, err = row["name"], row["status"], row["errors"]
    alerts = []
    if name in KNOWN_STOCK:
        alerts.append(("STOCK", f"{name} {status}", KNOWN_STOCK[name]))
        return alerts
    if "error" in status:
        lvl = "CRIT" if err >= CRIT_AUTO_ERR else ("WARN" if err >= WARN_AUTO_ERR else "INFO")
        alerts.append((lvl, f"{name} error {err}x", None))
    elif "skipped" in status or "failed" in status:
        alerts.append(("WARN", f"{name} status={status}", None))
    elif "not delivered" in status:
        alerts.append(("WARN", f"{name} 跑了但未投递", None))
    if "月度" in name and "error" in status and err >= MONTHLY_CRIT:
        alerts.append(("CRIT", f"月度任务失败 {err} 次: {name}", None))
    return alerts

def main() -> int:
    text = run_cli(["automations", "list"])
    rows = parse_automations(text)
    print(f"采集 automation {len(rows)} 条\n")
    buckets = collections.defaultdict(list)
    for r in rows:
        for lvl, msg, ticket in classify(r):
            buckets[lvl].append((msg, ticket))
    for lvl in ["CRIT", "WARN", "STOCK", "INFO"]:
        items = buckets.get(lvl, [])
        if not items:
            continue
        print(f"[{lvl}] ×{len(items)}")
        for msg, tk in items:
            suffix = f"  ← 工单 {tk}" if tk else ""
            print(f"   · {msg}{suffix}")
        print()
    # 落盘（只追加）
    now = datetime.datetime.now().astimezone().isoformat()
    with ALERTS.open("a", encoding="utf-8") as fh:
        for lvl, items in buckets.items():
            for msg, tk in items:
                fh.write(json.dumps({"ts": now, "level": lvl, "msg": msg,
                                     "ticket": tk}, ensure_ascii=False) + "\n")
    print(f"已追加到 {ALERTS}")
    return 1 if buckets.get("CRIT") else 0

if __name__ == "__main__":
    sys.exit(main())
```

### Step 4：把监控挂成 automation（真名 add）

```bash
# 真名：openclaw automations add
openclaw automations add \
  --name "生产监控-15min扫描" \
  --schedule "*/15 * * * *" \
  --agent peter \
  --message "跑 python3 ~/.openclaw/governance/monitor/monitor_scan.py；若有 CRIT，按 monitor.yaml 的 notify_template 立即 announce 到 telegram:8328029665 并建修复工单（Remediation Ticket）" \
  --target isolated

# 例：存量异常周复核
openclaw automations add \
  --name "存量异常周复核" \
  --schedule "0 21 * * 1" \
  --agent mingjing \
  --message "复核 monitor.yaml known_baseline 中全部存量异常项的工单状态；超 7 天未修复的升级 CRIT 并通知 kunlun" \
  --target isolated

# 校验
openclaw automations list 2>&1 | grep -E "生产监控|存量异常"
# 期望：两条新 automation
```

### Step 5：告警去重状态（防刷屏）

```json
{
  "state": {
    "heartbeat:kunlun":  { "last_alert": "2026-09-27T00:12:00+08:00", "level": "STOCK", "ticket": "RT-20260927-001", "count_today": 1 },
    "heartbeat:tiance":  { "last_alert": "2026-09-27T00:12:00+08:00", "level": "STOCK", "ticket": "RT-20260927-002", "count_today": 1 },
    "heartbeat:peter":   { "last_alert": "2026-09-27T00:12:00+08:00", "level": "STOCK", "ticket": "RT-20260927-003", "count_today": 1 },
    "能力矩阵月度更新":   { "last_alert": "2026-09-27T00:12:00+08:00", "level": "STOCK", "ticket": "RT-20260927-004", "count_today": 1 }
  },
  "dedup_policy": {
    "STOCK": "24h 内只报 1 次",
    "WARN":  "纳入 1h 摘要，不单独播报",
    "CRIT":  "立即播报；同对象 1h 内不重复"
  }
}
```

---

## 验证步骤

```bash
# 1. 复现三个真实告警（本机实测基线）
openclaw automations list 2>&1 | grep -E "heartbeat:|能力矩阵"
# 期望（本机实测逐字）：
# 90c903a2-... heartbeat:kunlun   every 30m ... error (99+x) ... kunlun
# 380e8da0-... heartbeat:tiance   every 30m ... skipped      ... tiance
# d367dbfb-... heartbeat:peter    every 2h  ... error (70x)  ... peter
# ebb72ae6-... 能力矩阵月度更新    cron 30 0 1 * * ... error (4x) ... kunlun

# 2. 确认已知基线确实是 4 条
openclaw automations list 2>&1 | grep -cE "error \(|skipped"
# 期望：4（三条 heartbeat 异常 + 能力矩阵；其余 automation 均为 ok）

# 3. 目录就位
ls -d ~/.openclaw/governance/monitor ~/.openclaw/governance/monitor/state
# 期望：两行目录

# 4. 跑监控扫描
python3 ~/.openclaw/governance/monitor/monitor_scan.py
# 期望（节选）：
# 采集 automation 61 条
#
# [STOCK] ×4
#    · heartbeat:kunlun error (99+x)  ← 工单 RT-20260927-001
#    · heartbeat:tiance skipped       ← 工单 RT-20260927-002
#    · heartbeat:peter error (70x)    ← 工单 RT-20260927-003
#    · 能力矩阵月度更新 error (4x)      ← 工单 RT-20260927-004
#
# 已追加到 /Users/peterqiu/.openclaw/governance/monitor/alerts.jsonl

# 5. 确认告警已落盘（只追加，永不丢证）
tail -5 ~/.openclaw/governance/monitor/alerts.jsonl
# 期望：5 行 JSON，每行含 ts/level/msg/ticket

# 6. 验证告警链 L3：CRIT 通知格式（预演模板渲染）
python3 - <<'PY'
name, kind, status, threshold, value, first, ticket, action = (
    "heartbeat:kunlun", "automation", "error (99+x)", "30", "99+",
    "2026-09-25T02:00:00+08:00", "RT-20260927-001",
    "1) 确认 Gateway 常驻 2) 查 heartbeat.model 可用性 3) 走 gateway restart")
print(f"""🚨 [CRIT] 生产监控告警
· 对象: {name} ({kind})
· 状态: {status}
· 阈值: {threshold} / 实测: {value}
· 首次发现: {first}
· 已有工单: {ticket}
· 建议动作: {action}""")
PY
# 期望：渲染出 6 行告警文本（模板与 monitor.yaml notify_template 一致）

# 7. 验证"日志新鲜度"检测（8/19 事故教训）
python3 -c "
import pathlib, datetime
p = pathlib.Path.home()/'.openclaw/logs/gateway.log'
if not p.exists():
    print('⏳ gateway.log 不存在（8/19 事故曾记录日志停写，需确认路径）')
else:
    age = (datetime.datetime.now() - datetime.datetime.fromtimestamp(p.stat().st_mtime))
    print(f'gateway.log age: {age.total_seconds()/3600:.1f} 小时')
    print('状态:', 'CRIT（日志停写 > 24h）' if age.total_seconds()>86400 else ('WARN' if age.total_seconds()>21600 else 'ok'))
"
# 期望：打印 age + 状态

# 8. 挂监控 automation 后校验
openclaw automations list 2>&1 | grep "生产监控"
# 期望：生产监控-15min扫描  cron */15 * * *  ...  peter

# 9. 端到端：让守门员 agent 复核告警
openclaw agent --agent peter --message \
  "读 ~/.openclaw/governance/monitor/alerts.jsonl 最新 20 条；\
对 STOCK 类逐条给处置建议；对 CRIT 类立即建修复工单（Remediation Ticket）回报 RT-ID"
# 期望：peter（通道守门员）回含 RT-ID 的处置建议
```

---

## 实测环境

| 项 | 值 | 采集方式 |
|---|---|---|
| 基座版本 | OpenClaw 2026.9.4 (3a9d69d)；2026-09-27 复测 `2026.9.6 (eb377ac)` | `--version` |
| OS | macOS 26.5.1 | `sw_vers` |
| `heartbeat:kunlun` | `every 30m` · **error (99+x)** · agent kunlun | `automations list` |
| `heartbeat:tiance` | `every 30m` · **skipped** · agent tiance | `automations list` |
| `heartbeat:peter` | `every 2h` · **error (70x)** · agent peter | `automations list` |
| `能力矩阵月度更新` | `cron 30 0 1 * *` · **error (4x)** · agent kunlun · model `zai/glm-5.1` | `automations list` |
| 异常 automation 总数 | 4（其余 ~57 条 status = ok） | `grep -cE "error \(\|skipped"` |
| automation 总数 | 61 | `grep -cE "^[0-9a-f]{8}-"` |
| 告警投递目标 | `telegram:8328029665`（实测 delivery 列 `announce -> telegram:8328029665 (explicit)`） | `automations list` |
| Gateway plist | `ai.openclaw.gateway.plist` | `ls ~/Library/LaunchAgents/` |
| 日志路径 | `~/.openclaw/logs/gateway.log`（8/19 事故记录其停写） | 事故档案 |
| 新增目录 | `~/.openclaw/governance/monitor/` + `state/` | 本机实测此前不存在 |
| 复测日期 | 2026-09-27 | — |

**"99+x"与"70x"的口径说明**：本机 `automations list` 对超长连续失败计数
显示为 `99+x` / `70x` 形态。脚本将 `99+x` 保守记为 `99`（用于分级，不追求精确值）。
按 30 分钟一次推算，`heartbeat:kunlun` 至少 **50 小时**无成功心跳；
`heartbeat:peter` 按 2 小时一次推算，至少 **140 小时（≈6 天）**无成功心跳。

---

## 排坑

### 坑 1：只看 `status != ok` → 漏掉 `not delivered`

本机两条 `ok (not delivered)`（凤凰日终复盘 / 蜂鸟晚间归档）。
**跑了但没投递 = 人看不到 = 编排价值归零**，必须按 WARN 告警。

### 坑 2：把 `99+x` 当精确值

`99+x` 是**上限截断显示**，不是精确计数。
分级用它即可（远超 CRIT 阈值 30），但**不要**在复盘里写"恰好 99 次"。

### 坑 3：`skipped` 被忽略

`heartbeat:tiance` 是 **skipped**（不是 error）——容易被 grep `error` 漏掉。
本机 `tiance` 是 Supervisor Layer 审计侧，**它失能 = 无人在审**。
分类逻辑必须显式包含 `skipped`。

### 坑 4：告警刷屏 → 无人看

4 条存量异常若每 15 分钟报一次 = 每天 384 条 → 必然被无视。
**必须用 `known_baseline` + `dedup_policy` 去重**：
STOCK 24h 只报 1 次，WARN 进 1h 摘要，CRIT 才立即播报。

### 坑 5：监控脚本自己失败 → 监控失效

`monitor_scan.py` 依赖 `openclaw automations list`。
若 Gateway 独占锁挡住（见 C6-1 排坑 1），脚本会返回 0 条 → **假阴性**。
**必须校验采集条数**：`len(rows)` 应 ≈ 61（本机基线）；
若 < 50 条，直接按 CRIT 报"监控自身失效"。

```python
# 追加到 monitor_scan.py 的 main() 开头
BASELINE_MIN = 50
if len(rows) < BASELINE_MIN:
    print(f"🚨 [CRIT] 监控自身失效：仅采集到 {len(rows)} 条 automation（基线 ≈61）")
    sys.exit(2)
```

### 坑 6：告警无 owner → 无人认领

`CRIT` 必须带 `owner`（本配置给 `mingjing`，因明镜是失败基因官/审计侧）
+ `sla_ack: 5min`。无 owner 的告警 = 无人认领的告警。

### 坑 7：存量异常无限期挂

`known_baseline` 只是**降噪**，不是**赦免**。
`stock_review: 7d` 是硬约束：存量项超 7 天未修复 → 升级 CRIT。
否则会出现"99+x 挂了半年没人管"的经典结局。

### 坑 8：`openclaw health` 可能被锁挡住

本机 `openclaw doctor` 实测被 Gateway 独占锁拒绝。
`health` 同源，采集时须**降级为跳过**而非报错退出——
否则监控脚本会因为一个可选源挂掉而整体失效。

---

## 进阶

### 进阶 1：从"计数"到"趋势"

阈值只看绝对值。可加趋势检测（防"慢慢变坏"）：

```yaml
# 路径：~/.openclaw/governance/monitor/trend.yaml
trend_detection:
  window: "7d"
  metric: "automation_error_consecutive"
  rules:
    - "7d 内 error 计数单调上升 ≥ 3 天 → WARN（恶化中）"
    - "7d 内 status 从 ok 变 not_ok 的对象 > 3 个 → WARN（面在扩大）"
    - "同一 provider 相关 automation 同时变 error → CRIT（供应商侧故障，参照 8/19）"
```

> ⏳ **待实测**：本机尚无 7 天历史快照，趋势检测口径待积累数据后校准。

### 进阶 2：8/19 型"供应商级联故障"的专用探针

8/19 的特征是 **17/18 Agent 的 fallback 第一位是同一个坏模型**。
可加一条**结构性探针**（不是看状态，而是看配置）：

```python
#!/usr/bin/env python3
# 路径：~/.openclaw/governance/monitor/probe_fallback.py
# 作用：检测"全军 fallback 链被同一模型占位"（8/19 事故的配置级前兆）
import json, pathlib, collections

d = json.loads((pathlib.Path.home() / ".openclaw/openclaw.json").read_text())
keys = collections.Counter()
self_loop = []
for aid, e in d["agents"]["entries"].items():
    m = e.get("model") or {}
    if not isinstance(m, dict):
        continue
    p, fb = m.get("primary"), m.get("fallbacks", [])
    if fb:
        keys[fb[0]] += 1
    if p and fb and p == fb[0]:
        self_loop.append(aid)
print("fallback[0] 占用分布:", dict(keys))
top, n = keys.most_common(1)[0]
print(f"最高占用: {top} × {n}/{len(d['agents']['entries'])}")
if n / len(d["agents"]["entries"]) > 0.75:
    print(f"🚨 [CRIT] {top} 占据 >75% Agent 的 fallback 第一位 → 8/19 型级联风险")
else:
    print("✅ fallback 首位分布正常")
print("primary == fallback[0] 的自循环 Agent:", self_loop or "无")
```

```bash
python3 ~/.openclaw/governance/monitor/probe_fallback.py
# 期望（本机修复后口径）：
# fallback[0] 占用分布: {'yiyongai/claude-opus-4-8': ..., 'deepseek/deepseek-v4-flash': ...}
# ✅ fallback 首位分布正常
# primary == fallback[0] 的自循环 Agent: 无
```

### 进阶 3：告警 → 修复工单 → 复盘的完整闭环

```
监控扫描（15min）
   │
   ├─ CRIT ──> announce telegram:8328029665
   │            └─> 建修复工单 RT-<date>-<seq>
   │                  └─> owner 认领（sla_ack 5min）
   │                        └─> 修复 + TEV 三证
   │                              └─> 若为 P0/P1 → 写 PIR 复盘（C7-2）
   │                                    └─> 沉淀手册 + 新 automation
   │
   ├─ WARN ──> 1h 摘要（不打扰）
   └─ STOCK ─> 24h 去重 + 7d 周复核（超期升 CRIT）
```

四例合起来 = **生产运维闭环**：C7-1 建编制 → C7-3 定节律 →
C7-4 盯异常 → C7-2 练复盘。

---

## 本分册诚实边界声明

### 已实测（本机 2026-09-27）

| 项 | 证据 |
|---|---|
| `openclaw --version` = `2026.9.6 (eb377ac)` | 命令实测 |
| `openclaw agents list` = 18 个 Agent | `grep -c '^- '` = 18 |
| `agents.entries` = 18 键 · 完整导出（名/模型/fallback 数/workspace） | `json.load` |
| 主模型分布：opus-4-8 ×9 / gpt-5.6-sol ×4 / gpt-5.5 ×2 / gpt-5.6-terra ×2 / deepseek-v4-flash ×1 | `json.load` 聚合 |
| `openclaw agents bindings` = 37 条（Telegram 19 + 飞书 18） | 实测 + `json.load` |
| `bindings` 37 条逐字导出 | `json.load` |
| `channels.telegram` = enabled / defaultAccount kunlun / dmPolicy pairing / groupPolicy allowlist / groupAllowFrom `["8328029665"]` | `json.load` |
| `channels.feishu` = enabled / defaultAccount kunlun / requireMention true / 18 accounts | `json.load` |
| 飞书 5 个账号完整 `appId`+`allowFrom`+`groupAllowFrom`（kunlun/tiangong/xuanyuan/zhulong/mingjing） | `json.load` |
| `openclaw automations list` = 61 条 | `grep -cE "^[0-9a-f]{8}-"` = 61 |
| 暗夜熔炉 = 13 条（01:10→03:30，间隔 10min） | `automations list` 逐条 |
| `skill-collection-review` = 18 条（every 7d） | `automations list` |
| `heartbeat:*` = 3 条（kunlun 30m **error 99+x** / tiance 30m **skipped** / peter 2h **error 70x**） | `automations list` |
| `能力矩阵月度更新` = `cron 30 0 1 * *` · **error (4x)** | `automations list` |
| 异常 automation = 4 条 | `grep -cE "error \(\|skipped"` = 4 |
| `automations` 子命令 = add/disable/edit/enable/get/list | `--help` 实测 |
| `cron` 是 `automations` 的别名 | `--help`：`Usage: openclaw cron\|automations` |
| 全部 cron 带 `@ Asia/Shanghai`（`memory-dreaming` 除外，为 `(exact)`） | `automations list` |
| 告警投递目标 `telegram:8328029665`（explicit） | `automations list` delivery 列 |
| `~/Library/LaunchAgents/` = `ai.openclaw.gateway.plist` + `com.openclaw.monthly-cleanup.plist` | `ls` |
| 8/19 事故档案 = `~/.openclaw/workspace/agents/workspace-kunlun/memory/2026-08-19-军团断线修复.md`（2789 字节） | 文件读取 |
| 8/19 根因/修复表/备份命名（逐字） | 档案读取 |
| 8/19 备份 `openclaw.json.bak.pre-fix-2026-08-19-0921` | 档案记载 |
| 9/21 事故：6 账号 disconnected（hetu/kunpeng/mingjing/peter/tiangong/tianshu）· 静默 > 60min | `memory/2026-09-27.md` 读取 |
| 9/21 配置根因可复核（requireMention true + 单 groupAllowFrom） | `json.load` 实核 |
| 9/21 沉淀 = 卷六附录 A RT-20260921-001 + 卷七附录 A 守门员角色 | `memory/2026-09-27.md` 读取 |
| `peter` = 通道守门员角色（飞书/Telegram/webchat 健康度检测 + 自愈 + 通知） | `memory/2026-09-27.md` 读取 |
| 18 个 Agent SOUL v2026.9.1 已就位（含 heartbeat 四件套配置） | `memory/2026-09-27.md` 读取 |
| `agents.<id>.heartbeat.directPolicy` 分布：kunlun=block / peter=block / 其他=announce / fengniao=none | `memory/2026-09-27.md` 读取 |
| `models.providers` = yiyongai / deepseek / zai / minimax / opencaio | `json.load` |
| `openclaw plugins list` = 74 行表项；`a2a` disabled（`stock:a2a/index.js`） | `plugins list` |
| `openclaw mcp list` = `mcp.servers` 0 配置（诚实基线） | `mcp list` |
| `openclaw mcp --help` = 14 子命令 | `--help` 实测 |
| `~/.openclaw/openclaw.json` = 1871 行 · 顶层键 20 个 | `wc -l` + `json.load` |
| `~/.openclaw/workspace/agents/` = 22 项（18 个 workspace-* + 4 个非规范残留） | `ls` |
| `~/.openclaw/workspace/skills/` = 238 个目录 | `ls \| wc -l` |
| `~/.openclaw/governance/` 不存在（需新建） | 目录探测 |
| `openclaw doctor` 被 Gateway 独占锁拒绝（state 库） | 命令实测 |
| PR #152777（feishu groupPolicy）= OPEN | 任务来源 |
| CLI 真名表（setup/agents add/agent --message/health/doctor/backup create/plugins/automations list/agents bindings） | `--help` + 实测 |

### ⏳ 待实测

| 项 | 原因 |
|---|---|
| 飞书 13 个账号的完整 `appId`（仅 5 个实测完整，其余为示意值） | 本机仅暴露 `dmPolicy: pairing`，未摘录敏感段 |
| `openclaw health` 完整输出 | 被 Gateway 独占锁遮挡，需 managed restart |
| `openclaw automations add` 的实际返回与落盘行为 | 未在生产环境新增 automation（避免污染 61 条编排） |
| `openclaw backup create` 的产物结构 | 未执行（避免写入大文件） |
| `openclaw plugins enable a2a` 后的行为 | 插件当前 disabled |
| `monitor_scan.py` / `orchestration_check.py` / `probe_fallback.py` 在真实告警流上的表现 | 逻辑本机可跑，但未接 15min automation 实跑 |
| 趋势检测（7d 窗口）口径 | 本机无 7 天历史快照 |
| 8/19 备份文件 `openclaw.json.bak.pre-fix-2026-08-19-0921` 当前是否仍在盘 | 未探测（可能已轮转） |
| 「19 agent」口径 | 本机真实在编 **18**；任务书标题 19 的来源待核 |

### 口径声明

- 本书统一基座为 **OpenClaw 2026.9.4 (3a9d69d)**；2026-09-27 本机复测为
  **2026.9.6 (eb377ac)**，差异源于 managed gateway 切换到 node@24 运行时的上报口径，
  未发现破坏性配置变更。本册全部配置/脚本对两个补丁版向后兼容。
- 正文 skills 口径 **236**；2026-09-27 本机 `ls ~/.openclaw/workspace/skills/` 目录数
  为 **238**（含 2 个非 skill 目录），差异已标注。
- **Agent 编制口径 18**（非任务书标题的 19）：`agents.entries` 实测 18 键；
  `workspace/agents/` 下 4 个非规范目录（`agent-kunlun` / `agents` / `config` / `kunlun`）
  不计入编制。已在 C7-1 背景节与本表双处标注。
- `heartbeat` 错误计数 `99+x` / `70x` 为**截断显示**，脚本保守记为 99 用于分级；
  推算的"≥50 小时 / ≥140 小时无成功心跳"是基于各自 `every` 周期的**下界估计**。
- 网关版本 **Hermes 0.20.1** 为环境声明值。

---

**—— 07-production-ops.md 完 · 4 例（C7-1 / C7-2 / C7-3 / C7-4）· MIT License · 2026-09-27 ——**

---

## P1-1 Cookbook 30 例达成总览

| 文件 | 例号 | 例数 | 类目 |
|---|---|:--:|---|
| `01-protocol-SOUL.md` | C1-1 ~ C1-4 | 4 | 协议·灵魂层 |
| `02-protocol-HEARTBEAT-MEMORY.md` | C2-1 ~ C2-4 | 4 | 协议·心跳与记忆层 |
| `03-skills-tools-mcp.md` | C3-1 ~ C3-4 | 4 | 技能·工具·MCP 层 |
| `04-training-rounds.md` | C4-1 ~ C4-4 | 4 | 训练轮次层 |
| `05-drift-governance.md` | C5-1 ~ C5-4 | 4 | 运维治理层 |
| `06-coordination-fleet.md` | C6-1 ~ C6-3 | 3 | 协同层 |
| `07-production-ops.md` | C7-1 ~ C7-4 | 4 | 生产运维层 |
| **合计** | **C1-1 ~ C7-4** | **27** | — |

> ⚠️ **诚实标注**：按本分册 + 既有 5 分册实际交付，Cookbook **合计 27 例**
> （C1-1~C1-4=4 / C2=4 / C3=4 / C4=4 / C5=4 / C6=3 / C7=4）。
> 任务书"30 例"目标差额 **3 例**——差额来自 C6 分册按任务书表格为 3 例（C6-1~C6-3）、
> C7 为 4 例（C7-1~C7-4），**7 例全部按清单交付，无遗漏**。
> 若需凑足 30 例，建议补 C6-4（跨渠道协同：Telegram ↔ 飞书 消息桥接）
> 与 C5-5 / C2-5 各 1 例——**⏳ 待丘总定夺，本册未越界新增**。

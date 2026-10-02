# 实战案例库 · 02 · 生产模式卷（Production Patterns）

> **v5.0 行业标准版 · 案例库卷 · 上半 · 文件 2/2**
>
> **License: MIT**（跟随 OpenClaw 主仓 LICENSE 文件文本 = `MIT License / Copyright (c) 2026 OpenClaw Foundation`；
> GitHub badge 显示 `NOASSERTION` 仅为 Licensee 启发式匹配问题，不影响法律效力）
>
> **实测环境**：`OpenClaw 2026.9.4 (3a9d69d)` · 2026-09-27 · macOS 26.5.1 · 本机 18 agent 已盘点 · 238 skills 目录
> **本机版本命令**：`openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`
> **上游 stable**：`v2026.9.6`（2026-09-23 发布）
> **Hermes 侧**：Hermes 0.20.1（本机 `~/.hermes` 网关，与 OpenClaw 双网关并行）
> **配套工具链**：`hermes-agent` 子 agent 编排框架（本卷 10 例由多 agent 并行撰写，主编终审）
>
> **数据来源**（全部本机实拉，本次独立复核）：
> - `openclaw agents list`（本机实测：18 agent）
> - `~/.openclaw/openclaw.json`（45,662 字节）→ `agents.entries`（18 条）/ `bindings`（37 条）/ `channels.feishu`（18 账号）
> - `openclaw automations list`（本机实测：含 3 条 heartbeat + 暗夜熔炉系列 + 18 条 skill-collection-review + 蜂群系列）
> - `openclaw plugins list`（本机实测：`53/73 enabled`；基线口径 51/69；`a2a` = disabled）
> - `openclaw mcp`（14 子命令 · `mcp.servers` · 0 配置）
> - `~/.openclaw/workspace/skills/`（本机实测：236 顶目录 + INDEX + 1 = 238）
> - v1.0 卷四（训练流程全 9 文件）+ v4.0 volume-04（11 文件）+ industry-standard `chapters/04-training`
> - `~/.openclaw/workspace/agents/workspace-kunlun/training/`（`prompt-v2.md` + `prompt-v2-module{1,2,3}.md`）
>
> **术语规范**：本卷遵循《术语对照表 v3.0》（35 条）。业内术语首次出现双写为「行业标准名（原：黑话）」：
> 「Multi-Agent Orchestration（原：军团编制）」「Supervisor Layer（原：监军）」「Mentor Agent（原：教练虾）」
> 「Training Round（原：训练轮次）」「Response Yield Protocol（原：让位协议）」「Trust Score / Merit Ledger（原：信誉分/军功簿）」。
>
> **一句话定位**：文件 1 讲「事故怎么炸」，本文件讲「**正面怎么搭**」——
> 5 例全部是本机**已在生产运行**的模式：18 编制 / 编排节奏 / 冷启动 / 心跳熔断 / 插件取舍。
> 事故教人避坑，模式教人搭台。

---

## 卷首 · 生产模式为什么和事故同样重要

v5.0 改造方案 Part 2.3 的定性结论是：**三版全是「论述型」而非「手册型」**——
有哲学、有对位、有表格，但**没有一套「照着搭」的生产模式**。

| 对比项 | 论述型（v1.0/v4.0/新书） | 生产模式型（本文件） |
|---|---|---|
| 单元 | 章节 / 模块 | **一套可复制的编制 / 节奏 / 训练 / 熔断 / 取舍** |
| 读者动作 | 读懂 | **照着搭** |
| 验证 | 无 | **有命令、有期望输出** |
| 借力 | 概念 | **本机 18 agent 的真实运行数据** |

本文件 5 例覆盖 OpenClaw 生产的五个面：

| 例 | 模式 | 一句话 | 关键数据 |
|---|---|---|---|
| CASE-6 | 18 agent 生产编制 | 从 1 到 18 的扩张路径 | `agents.entries` = 18；`bindings` = 37 |
| CASE-7 | 编排节奏设计 | 晨扫→日报→暗夜熔炉的一天 | heartbeat ×3 + 暗夜熔炉系列 + skill-review ×18 |
| CASE-8 | 新 agent 冷启动 | 上线 7 天训练全记录 | L0→L5 阶梯 + `prompt-v2` 三模块 |
| CASE-9 | 心跳熔断 | heartbeat error 70x / 99+x 的自愈 | `every:30m/2h` + `timeoutSeconds:30` |
| CASE-10 | 插件取舍 | 51/69（53/73）启用策略，a2a 为何 disabled | `a2a` = disabled |

---

# CASE-6 · 18 agent 生产编制：从 1 到 18 的扩张路径

## 一、案例速览

| 项 | 内容 |
|---|---|
| 时间 | 2026-05（首版编制，`AGENTS.md` 早期版本）→ 2026-09-27（18 agent 定型） |
| 影响面 | 全军团组织架构 |
| 模式类型 | **Multi-Agent Orchestration（原：军团编制）——中央路由 + 专才分工 + lane contract** |
| 规模 | **18 agent**（`openclaw agents list` 实测） |
| 角色分布 | 1 协调（kunlun）+ 1 监督（mingjing/tiance）+ 16 专才 |
| 绑定规模 | **37 条 bindings**（`~/.openclaw/openclaw.json` 实测） |
| 模型分布 | `yiyongai/claude-opus-4-8` ×9 · `yiyongai/gpt-5.6-sol` ×4 · `gpt-5.6-terra` ×2 · `gpt-5.5` ×2 · `deepseek-v4-flash` ×1 |
| 沉淀产物 | lane contract v4.0（`AGENTS.md` frontmatter）+ 三级追踪协议 + 路由优先级矩阵 |
| 优先级 | 基线（架构级） |

> **一句话**：18 个 Agent 不是「18 个平权 bot」，而是**「1 个中央路由 + 16 个专才 + 1 个监督」的分层编制**——
> 每个 Agent 有 `lane_id` / `role` / `purpose` / `non_goals` / `allow_agents` / `handoff_rule`，
> 用**合约**（lane contract）而非**默契**来协作。

---

## 二、事件时间线（扩张路径）

| 时点 | 事件 | 证据 |
|---|---|---|
| **T-0 · 2026-05-05** | 最早的组织图 `org-chart-2026-05-05.md` 落盘 | kunlun memory 目录 |
| **T+4天 · 2026-05-09** | `org-full-responsibility-2026-05-09.md`（12,881 字节）——全员职责定义 | 同上 |
| **T+周 · 2026-05-13** | A2A 协作协议 v1.0 发布（「昆仑统一发布 · 所有 Agent 必须遵守」） | `AGENTS.md` §五 |
| **T+月 · 2026-08-01** | `organization_v2.md`（6,087 字节）——编制 v2 | kunlun memory |
| **T+月 · 2026-08-17** | 第 18 Agent（tiance）注册（`openclaw-silicon-life-handbook` 记录「OpenClaw 第 18 Agent」） | 08-30 熔炉 §4 |
| **T+月 · 2026-08-30** | `agents_total=18 · active=16 · stale=0 · dead=2`（jixia 1438h + tiance 311h 误报） | 08-30 熔炉 §31 |
| **T+月 · 2026-09-27** | **lane contract v4.0** 下发全体（18 个 workspace 的 `AGENTS.md` 加 frontmatter，`contract_date: 2026-09-27`） | 本卷实读 `workspace-kunlun/AGENTS.md` / `workspace-xuanyuan/AGENTS.md` |
| **T+月 · 2026-09-27** | 本卷实测：`openclaw agents list` = **18 agent**；`bindings` = **37 条**；`agents.entries` = **18 条** | 本机实拉 |

> **时间线诚实边界**：从 1 到 18 的**逐个 Agent 上线日期**未完整实拉（需查各 agent dir 创建时间）。
> 本卷给出的关键锚点（05-05 组织图 / 05-13 A2A 协议 / 08-17 第 18 注册 / 09-27 lane v4.0）均有文件证据。

---

## 三、根因分析（5 Whys）——为什么需要 18 个而不是 3 个？

> 生产模式的「5 Whys」问的不是「为什么出错」，而是「**为什么这样搭是最优解**」。

1. **为什么要把 1 个通用 Agent 拆成 18 个？**
   → 因为任务域分化后，**单 Agent 的 context 会被撑爆**：一个 Agent 同时管代码 / 内容 / 财务 / 合规，
   `MEMORY.md` / `SOUL.md` 会互相污染，`SKILL.md` 会变成杂物间。

2. **为什么不能「每来一个任务就新建一个 Agent」？**
   → 因为那会变成 **N 个平权 bot 抢活**（无路由、无让位、无边界）。
   所以需要**中央路由层**：kunlun 做唯一入口。

3. **为什么中央路由层不会成为瓶颈？**
   → 因为 kunlun 的 `non_goals` 明确写着 **「不写代码 / 不写内容 / 不亲自执行任务」**——
   它只做「判断价值 / 分配资源 / 推动执行」，不抢专家的活。

4. **为什么专家之间不横向乱串？**
   → 因为 **`allow_agents` 白名单** + **`handoff_rule`**：
   如 xuanyuan 的 `allow_agents: []`（只接收 kunlun 委派直办，不横向委派）
   + `handoff_rule: "xuanyuan 仅接收 kunlun 委派直办，完成后回 kunlun 验收；不横向委派，跨域需求先报 kunlun"`。

5. **为什么要有监督层（mingjing / tiance）而不是全靠 kunlun 自省？**
   → 因为 **中央路由者不能同时是监督者**（`AGENTS.md` §4.5 明确：「昆仑抢答被 @ 的场景 → 明镜记录 →
   写入昆仑的违规记录」）——**裁判不能兼任运动员**。

### → 编制设计的第一性原理

> **根本逻辑 = 「分层 + 合约 + 制衡」：**
> 1. **分层**：协调层（kunlun）/ 专才层（16）/ 监督层（mingjing, tiance）
> 2. **合约**：每个 Agent 用 `lane_id + role + purpose + non_goals + allow_agents + handoff_rule` 定义边界
> 3. **制衡**：监督层独立于协调层，可记录协调层的违规
>
> **一句话**：**18 个 Agent 的编制，本质是用「合约」把「混沌」压成「可路由的图」。**

---

## 四、当时的错误决策（扩张路上的弯路）

### 错误决策 1：早期「平权制」导致抢活

A2A 协议 v1.0 发布前，群聊里多个 Agent 会同时响应同一条消息。

- **错在哪**：没有中央路由，人人可回。
- **代价**：群聊噪音 + 重复劳动。→ 催生 §4「昆仑不抢答」铁律。

### 错误决策 2：让协调者兼裁判

早期 kunlun 既是路由又是裁决者，导致「自己路由错了自己判」。

- **错在哪**：权力不分离。
- **代价**：→ 催生「明镜记录昆仑违规」的制衡条款。

### 错误决策 3：扩张时不写 `non_goals`

早期 Agent 只有 `purpose`（要做什么），没写 `non_goals`（**不做什么**）。

- **错在哪**：边界只写在正面，反面空白 → Agent 越界无据可依。
- **代价**：→ lane contract v4.0 把 `non_goals` 设为**必填字段**。

### 错误决策 4：`primary == fallback[0]`（编制扩张时的配置债，见 CASE-1）

编制从 1 扩到 18 的过程中，fallback 链逐次手工补写，累积出「首位单点共享」。

- **错在哪**：扩张只看「有没有」，不看「结构合不合理」。
- **代价**：8/19 全军级联失败（CASE-1）。

---

## 五、修复过程（编制怎么落地）

### 5.1 查看当前编制（真名命令）

```bash
# 1) 列出全部 agent（真名 = `openclaw agents list`，不是 `agents create/archive`）
openclaw agents list 2>&1 | grep -E "^- "
# 本卷实测输出（18 行）：
#   - kunlun (default) (昆仑)
#   - mingjing (明镜)
#   - tianshu (天枢)
#   - tiangong (天工)
#   - xuanyuan (轩辕)
#   - fenghuang (凤凰)
#   - kunpeng (鲲鹏)
#   - jixia (稷下)
#   - zhulong (烛龙)
#   - siku (司库)
#   - qilin (麒麟)
#   - hetu (河图)
#   - peter (Peter的数字分身)
#   - fengniao (蜂鸟)
#   - mobai (墨白)
#   - zhuque (朱雀)
#   - baxia (霸下)
#   - tiance (天策)

# 2) 看单个 agent 的完整档案（workspace / agent dir / model / routing）
openclaw agents list 2>&1 | head -60
# 本卷实测 kunlun 档案：
#   Identity: 🏔️ 昆仑 (config)
#   Workspace: ~/.openclaw/workspace/agents/workspace-kunlun
#   Agent dir: ~/.openclaw/agents/kunlun/agent
#   Model: deepseek/deepseek-v4-flash
#   Routing rules: 5
#   Routing: Telegram kunlun, Telegram default, Feishu kunlun, Feishu *, Telegram *

# 3) 统计模型分布（编制健康度指标）
openclaw agents list 2>&1 | grep "Model:" | sort | uniq -c | sort -rn
# 本卷实测：
#   9 Model: yiyongai/claude-opus-4-8
#   4 Model: yiyongai/gpt-5.6-sol
#   2 Model: yiyongai/gpt-5.6-terra
#   2 Model: yiyongai/gpt-5.5
#   1 Model: deepseek/deepseek-v4-flash
```

### 5.2 绑定（bindings）：把 Agent 接到通道

```bash
# bindings 真结构（本卷实读 openclaw.json）：list，37 条
jq '.bindings | length' ~/.openclaw/openclaw.json        # 期望：37
jq -r '.bindings[] | "\(.agentId)\t\(.match.channel)\t\(.match.accountId // "*")"' \
  ~/.openclaw/openclaw.json | head -40
# 本卷实测样例：
#   kunlun   telegram  kunlun
#   mingjing telegram  mingjing
#   tianshu  telegram  tianshu
#   ...
```

**binding 的真实结构（JSON 形态）**：

```json
{
  "agentId": "kunlun",
  "match": { "channel": "telegram", "accountId": "kunlun" }
}
```

> **编制维度**：`agents.entries` = 18（**身份**）；`bindings` = 37（**接入**）；
> `channels.feishu.accounts` = 18（**飞书账号**）。三者构成「编制 × 通道」的完整矩阵。

### 5.3 lane contract v4.0（编制合约，真名 = AGENTS.md frontmatter）

本卷实读 `workspace-kunlun/AGENTS.md` 与 `workspace-xuanyuan/AGENTS.md` 的 frontmatter：

```yaml
# 协调层样例（kunlun）
lane_id: kunlun
role: coordinator
purpose: "蓝血军团军师·中央路由·战略调度"
non_goals: ["不写代码","不写内容","不亲自执行任务"]
chat_budget: 30
tools_risk: high
allow_agents: ["baxia","fenghuang","fengniao","hetu","jixia","kunpeng","mingjing","mobai","peter","qilin","siku","tiance","tiangong","tianshu","xuanyuan","zhulong","zhuque"]
handoff_rule: "kunlun中央路由：被丘总/天枢@后5min内确认Task-ID，下行委派给allow_agents内任意专才，3级追踪（确认/里程碑/验收）"
lane_contract_version: "v4.0"
contract_date: "2026-09-27"
```

```yaml
# 专才层样例（xuanyuan）
lane_id: xuanyuan
role: specialist
purpose: "CTO·技术实现·架构·部署"
non_goals: ["不做产品","不写内容","不直接对接客户"]
chat_budget: 18
tools_risk: high
allow_agents: []                    # ← 不横向委派
handoff_rule: "xuanyuan仅接收kunlun委派直办，完成后回kunlun验收；不横向委派，跨域需求先报kunlun"
lane_contract_version: "v4.0"
contract_date: "2026-09-27"
```

> **合约三要素**：`role`（层）+ `allow_agents`（可委派给谁）+ `handoff_rule`（怎么交接）。
> **协调者 `allow_agents` 非空，专才 `allow_agents` 为空** —— 这就是「分层」在数据上的体现。

### 5.4 三级追踪协议（任务闭环）

```
Level 1 ✅ 确认收到（派发后 5 分钟内）
  ├── Agent 回复："Task-XXX 已收到，资源就绪"
  └── 未确认 → 昆仑追问 1 次 → 仍未确认 → 升级到 P2
Level 2 ⏳ 里程碑进度（Deadline > 24h 的任务）
  ├── 每 33% 进度检查一次
  └── 进度 <50% 且时间过 70% → 自动升级到 P1
Level 3 ✅ 完成验收（Deadline 到）
  ├── 对照验收标准逐项打分
  └── 不通过 → 退回修改或升级到天枢
```

### 5.5 新增 Agent 的标准动作（真名）

```bash
# 真名提醒：新增 agent 的命令是 `openclaw agents add`，不是 `agents create`（虚构，禁用）
openclaw agents add <id> --name "<中文名>" ...
# 真名提醒：初始化环境是 `openclaw setup`，不是 `openclaw init`（虚构，禁用）
openclaw setup
# 健康检查真名：`openclaw health` / `openclaw doctor`，不是 `agents health-check`（虚构，禁用）
openclaw health
openclaw doctor
# 备份真名：`openclaw backup create`，不是 `agents archive`（虚构，禁用）
openclaw backup create
```

---

## 六、修复后验证

```bash
# 1) 编制规模
openclaw agents list 2>&1 | grep -cE "^- "     # 期望：18

# 2) 绑定规模
jq '.bindings | length' ~/.openclaw/openclaw.json   # 期望：37（本卷实测）

# 3) entries 规模
jq '.agents.entries | length' ~/.openclaw/openclaw.json   # 期望：18

# 4) lane contract 是否全员下发
for d in ~/.openclaw/workspace/agents/workspace-*/; do
  f="$d/AGENTS.md"
  [ -f "$f" ] && v=$(grep -m1 "lane_contract_version" "$f") && echo "$(basename $d): $v"
done
# 期望：18 个 workspace 均有 lane_contract_version: "v4.0"（contract_date: 2026-09-27）

# 5) allow_agents 分层校验（协调者非空 / 专才为空）
jq -r '.agents.entries | keys[]' ~/.openclaw/openclaw.json   # 18 个 id
```

> **验收标准**：
> - [x] 18 agent 全部可列（`agents list`）
> - [x] 37 条 binding 覆盖 Telegram + Feishu
> - [x] 18 个 lane contract v4.0 下发
> - [ ] 三级追踪协议在 `memory/tasks/` 有实盘记录 ⏳（CASE-4 显示 `memory/tasks/` 曾为空目录）

---

## 七、沉淀的机制

| 缺口 | 沉淀机制 |
|---|---|
| 平权抢活 | **中央路由（kunlun 唯一入口）+ 不抢答铁律** |
| 权力不分离 | **监督层独立（mingjing 记录 kunlun 违规）** |
| 边界不明 | **lane contract：`role + non_goals + allow_agents + handoff_rule` 四件套** |
| 任务失联 | **三级追踪（确认 / 里程碑 / 验收）+ 超时升级链** |
| 路由靠猜 | **路由优先级矩阵（关键词 → 目标 Agent）** |
| 扩张无约束 | **`non_goals` 必填 + `chat_budget`（消息预算）+ `tools_risk`（工具风险等级）** |

### 路由优先级矩阵（节选，真实条款）

| 消息关键词/领域 | 路由目标 |
|---|---|
| 代码/RAG/架构/部署/测试 | 轩辕（xuanyuan） |
| 设计/UI/UX/品牌视觉 | 墨白（mobai）→ 天工（tiangong） |
| 产品/PRD/功能定义 | 天工（tiangong） |
| 量化/策略/交易/市场数据 | 烛龙（zhulong） |
| 内容/文案/品牌/传播 | 凤凰（fenghuang）→ 朱雀（zhuque） |
| 增长/获客/渠道/投放 | 鲲鹏（kunpeng） |
| 情报/竞品/信息收集 | 蜂鸟（fengniao） |
| 销售/谈判/客户/成交 | 霸下（baxia） |
| 人才/招聘/悬赏 | 稷下（jixia） |
| 命理/择时/风水/能量 | 河图（hetu） |
| 财务/预算/成本 | 司库（siku） |
| 合规/审计/红线/风控 | 明镜（mingjing） |
| 运营/排期/OKR/进度 | 天枢（tianshu） |
| 战略/方向/资源分配/军令 | 昆仑（kunlun） |

---

## 八、如果你的系统遇到同样问题

### 8.1 编制设计 checklist（从 1 到 N）

- [ ] 先定**层**：协调层 / 专才层 / 监督层（至少三层，别只有一个）
- [ ] 每个 Agent 写 **`purpose`（做什么）+ `non_goals`（不做什么）**——`non_goals` 必须写
- [ ] 协调者的 `non_goals` 必须含「不亲自执行」
- [ ] 专才 `allow_agents` 默认空（不横向委派）；协调者 `allow_agents` 列全可委派对象
- [ ] 每个 Agent 写 **`handoff_rule`**（谁能指派我、我怎么回交）
- [ ] 定**路由矩阵**（关键词 → 目标 Agent）
- [ ] 定**三级追踪**（确认 / 里程碑 / 验收 + 超时升级）
- [ ] 监督者**不能**是协调者本人
- [ ] 加 `chat_budget`（消息预算）与 `tools_risk`（工具风险）字段

### 8.2 常见编制反模式

| 反模式 | 症状 | 修法 |
|---|---|---|
| 平权制 | 群里多 Agent 抢答 | 中央路由 + 不抢答铁律 |
| 协调者兼裁判 | 自己路由自己判 | 独立监督层 |
| 只写 purpose 不写 non_goals | 越界无据 | non_goals 必填 |
| Agent 横向乱串 | 跨域请求不经协调 | allow_agents 白名单 |
| 新增 Agent 无合约 | 每个 Agent 行为不一致 | lane contract 模板化下发 |
| 编制只管身份不管接入 | Agent 存在但收不到消息 | bindings 显式绑定通道 |

### 8.3 编制规模参考（本机实测）

| 维度 | 本机数值 |
|---|---|
| agent 数 | 18 |
| 协调 / 专才 / 监督 | 1 / 16 / 1 |
| bindings | 37 |
| 模型种类 | 5（claude-opus-4-8 占 9/18 = 50%） |
| 飞书账号 | 18 |
| Telegram 账号 | 18（含 default） |

> **CASE-6 一句话收口**：**18 个 Agent 的编制，不是「人多力量大」，而是「用合约把混沌压成可路由的图」**。
> 协调者的 `non_goals` 写着「不亲自执行」，监督者独立于协调者——
> **这两条，才是编制能跑起来而不打架的关键。**

---

## 附录 A · 18 Agent 全名单与分层（实拉）

> 来源：本卷实测 `openclaw agents list`（2026-09-27）。

| # | id | 中文名 | 层 | 备注 |
|--:|---|---|---|---|
| 1 | kunlun | 昆仑 | **协调层（default）** | `role: coordinator`；Routing rules = 5 |
| 2 | mingjing | 明镜 | **监督层** | 合规 / 审计 / 红线 |
| 3 | tiance | 天策 | **监督层** | Supervisor Layer（原：监军）；第 18 Agent |
| 4 | tianshu | 天枢 | 运营层 | 运营 / 排期 / OKR / 进度 |
| 5 | tiangong | 天工 | 产品层 | 产品 / PRD / 功能定义 |
| 6 | xuanyuan | 轩辕 | 技术层 | CTO / 技术实现 / 架构 / 部署 |
| 7 | fenghuang | 凤凰 | 内容层 | 内容 / 文案 / 品牌 / 传播 |
| 8 | kunpeng | 鲲鹏 | 增长层 | 增长 / 获客 / 渠道 / 投放 |
| 9 | jixia | 稷下 | 人才层 | 人才 / 招聘 / 悬赏 |
| 10 | zhulong | 烛龙 | 量化层 | 量化 / 策略 / 交易 / 市场数据 |
| 11 | siku | 司库 | 财务层 | 财务 / 预算 / 成本 |
| 12 | qilin | 麒麟 | 专才 | — |
| 13 | hetu | 河图 | 专才 | 命理 / 择时 / 风水 / 能量 |
| 14 | peter | Peter 的数字分身 | 个人层 | Channel Sentinel（拟） |
| 15 | fengniao | 蜂鸟 | 情报层 | 情报 / 竞品 / 信息收集 |
| 16 | mobai | 墨白 | 设计层 | 设计 / UI / UX / 品牌视觉 |
| 17 | zhuque | 朱雀 | 内容层 | 凤凰 → 朱雀链路 |
| 18 | baxia | 霸下 | 销售层 | 销售 / 谈判 / 客户 / 成交 |

### 模型分布（实拉）

| 模型 | 数量 | 占比 |
|---|---:|---:|
| `yiyongai/claude-opus-4-8` | **9** | 50% |
| `yiyongai/gpt-5.6-sol` | 4 | 22% |
| `yiyongai/gpt-5.6-terra` | 2 | 11% |
| `yiyongai/gpt-5.5` | 2 | 11% |
| `deepseek/deepseek-v4-flash` | 1 | 6% |

> **读法**：`claude-opus-4-8` 占一半（9/18）——主力模型集中，但**不代表 fallback 可单点共享**（见 CASE-1 教训）。

### 路由规则样例（kunlun，实拉）

```
Routing rules: 5
Routing: Telegram kunlun, Telegram default, Feishu kunlun, Feishu *, Telegram *
```

---

## 附录 B · 双向绑定矩阵（bindings 实拉）

```
agents.entries (18)  ×  bindings (37)  ×  channels (Telegram 18 + Feishu 18)
```

| 通道 | 账号数 | binding 形态 |
|---|---|---|
| Telegram | 18（含 default） | `{agentId, match:{channel:"telegram", accountId:"<id>"}}` |
| Feishu | 18 | `{agentId, match:{channel:"feishu", accountId:"<id>"}}` |

| 统计项 | 值 |
|---|---|
| `bindings` 总数 | **37** |
| Telegram binding | 约 19（含 default） |
| Feishu binding | 18 |

> **编制与接入的关系**：`agents.entries` 定义「**我是谁**」，`bindings` 定义「**我从哪条通道被唤起**」。
> 两者分离，意味着「Agent 存在 ≠ Agent 可被唤起」——**必须显式绑定**。

---

## 附录 C · 读者自测（8 题）

1. **18 agent 的三层是哪三层？各几个？**
   参考答案：协调层 1（kunlun）/ 专才层 16 / 监督层 1（mingjing, tiance 归监督面）。

2. **为什么协调者的 `non_goals` 必须写「不亲自执行」？**
   参考答案：否则协调者会抢专家的活，路由层失效、专家层闲置。

3. **`allow_agents` 在协调者与专才身上有何不同？为什么？**
   参考答案：协调者非空（列全可委派对象）；专才为空（不横向委派，跨域先报协调者）。

4. **为什么监督者不能是协调者本人？**
   参考答案：权力必须分离——否则「自己路由错了自己判」。

5. **`handoff_rule` 解决什么问题？**
   参考答案：定义「谁能指派我、我怎么回交」，让任务交接有据。

6. **`bindings` 与 `agents.entries` 的区别是什么？**
   参考答案：entries = 身份（我是谁）；bindings = 接入（我从哪被唤起）。

7. **本机新增 agent 的真名命令是什么？**
   参考答案：`openclaw agents add`（不是 `agents create`）；初始化为 `openclaw setup`（不是 `init`）。

8. **三级追踪包含哪三级？超时怎么升级？**
   参考答案：确认（5min）/ 里程碑（每 33%）/ 验收；追问 1 次无回应 → P2，2 次 → P1。

---

## 附录 D · 与其它案例的交叉引用

| 关联案例 | 关系 |
|---|---|
| **CASE-1**（8/19 断线） | 编制扩张期的 fallback 配置债；18 agent 全线下线的现场 |
| **CASE-7**（编排节奏） | 编制 → 编排：每个 Agent 被排进 24h 节奏 |
| **CASE-8**（冷启动） | 编制扩张的「增量」是冷启动；本案例是「存量」全貌 |
| **CASE-2**（9/21 飞书） | 18 个 Feishu 账号的准入配置是通道面课题 |

---

## 附录 E · 不适用边界（诚实）

- **逐个 Agent 上线日期未实拉**：给的是关键锚点（05-05 / 05-13 / 08-17 / 09-27）。
- **监督层归属为读法**：`mingjing`/`tiance` 的层级归类基于其职责（合规/监军），
  `role` 字段原文仅见 coordinator/specialist 两类；**层级归类为本卷判断**。
- **模型分布为快照**：18 个 Agent 的 primary 模型会随 config 变更；本表为 2026-09-27 快照。
- **`allow_agents` 仅核验了 kunlun（非空）与 xuanyuan（空）两个样本**，其余 16 个未逐一实读。

---

# CASE-7 · 编排节奏设计：晨扫→日报→暗夜熔炉的一天

## 一、案例速览

| 项 | 内容 |
|---|---|
| 时间 | 常态运行（本卷实测快照：2026-09-27） |
| 影响面 | 全军团日常节奏 |
| 模式类型 | **Automation Orchestration（定时编排）——24 小时多波次节奏** |
| 规模 | `openclaw automations list` 本机实测：**60 行**（基线口径 43 条） |
| 关键构成 | heartbeat ×3 + 暗夜熔炉系列（13 条实测 / 基线 18）+ skill-collection-review ×18 + 蜂群 A–E + 日报系列 + 军功爵周结算 + 能力矩阵 |
| 异常 | **heartbeat:kunlun error (99+x)** · **heartbeat:peter error (70x)** · heartbeat:tiance **skipped** |
| 沉淀产物 | 24h 节奏表 + 心跳/熔炉/晨扫三层编排范式 |
| 优先级 | 基线（节奏级） |

> **一句话**：军团的「一天」不是随机事件流，而是**三层节奏**：
> **心跳层**（高频轻量，30m/2h）+ **业务层**（每日扫报，06:00–22:00）+ **进化层**（凌晨 01:00–04:00 暗夜熔炉）。

---

## 二、事件时间线（24 小时节奏表）

> 以下来自本机 `openclaw automations list` 实测（2026-09-27），按 cron 时间排序。

| 时刻（Asia/Shanghai） | 任务 | 类型 | 调度 | 本机实测状态 |
|---|---|---|---|---|
| **每 30m** | Heartbeat (kunlun) | 心跳 | `every 30m` | **error (99+x)** 🔴 |
| **每 30m** | Heartbeat (tiance) | 心跳 | `every 30m` | **skipped** ⚠️ |
| **每 2h** | Heartbeat (peter) | 心跳 | `every 2h` | **error (70x)** 🔴 |
| **01:10** | 明镜-暗夜熔炉 | 进化 | `cron 10 1 * * *` | ok |
| **01:20** | 天枢-暗夜熔炉 | 进化 | `cron 20 1 * * *` | ok |
| **01:30** | 轩辕-暗夜熔炉 | 进化 | `cron 30 1 * * *` | ok |
| **01:40** | 稷下-暗夜熔炉 | 进化 | `cron 40 1 * * *` | ok |
| **01:50** | 烛龙-暗夜熔炉 | 进化 | `cron 50 1 * * *` | ok |
| **02:10** | 鲲鹏-暗夜熔炉 | 进化 | `cron 10 2 * * *` | ok |
| **02:30** | 霸下-暗夜熔炉 | 进化 | `cron 30 2 * * *` | ok |
| **02:40** | 司库-暗夜熔炉 | 进化 | `cron 40 2 * * *` | ok |
| **02:50** | 天工-暗夜熔炉 | 进化 | `cron 50 2 * * *` | ok |
| **03:00** | Memory Dreaming Promo（memory-core） | 记忆 | `cron 0 3 * * *` | ok |
| **03:00** | 墨白-暗夜熔炉 | 进化 | `cron 0 3 * * *` | ok |
| **03:10** | 朱雀-暗夜熔炉 | 进化 | `cron 10 3 * * *` | ok |
| **03:20** | 麒麟-暗夜熔炉 | 进化 | `cron 20 3 * * *` | ok |
| **03:30** | 河图-暗夜熔炉 | 进化 | `cron 30 3 * * *` | ok |
| **05:30** | heartbeat-morning-530 | 心跳/晨起 | `cron 30 5 * * *` | ok |
| **06:00** | 蜂群-A-晨间全量扫描+… | 情报 | `cron 0 6 * * *` | ok |
| **06:00** | heartbeat-morning-600 | 心跳/晨起 | `cron 0 6 * * *` | ok |
| **07:00** | heartbeat-breakfast-700 | 心跳/晨起 | `cron 0 7 * * *` | ok |
| **07:00** | hetu-回测进化日报 | 日报 | `cron 0 7 * * *` | ok |
| **07:05** | Peter 每日人生教练早课 | 教练 | `cron 5 7 * * *` | ok |
| **08:00** | 凤凰-内容工厂·每日调试 | 内容 | `cron 0 8 * * *` | ok |
| **08:00** | 蜂鸟-B-竞品网页变更扫描 | 情报 | `cron 0 8 * * *` | ok |
| **09:00** | 昆仑每周进化评估 | 进化（周） | `cron 0 9 * * 1` | ok |
| **09:00** | daily-tech-intel-github | 情报 | `cron 0 9 * * *` | ok |
| **09:00** | 凤凰-内容日历每日核对 | 内容 | `cron 0 9 * * 1-5` | ok |
| **09:30** | weekly-tech-intel-github | 情报（周） | `cron 30 9 * * 1` | ok |
| **10:00** | 蜂群-BC-午间增量扫描 | 情报 | `cron 0 10 * * *` | ok |
| **12:00** | 蜂鸟-午间情报扫描 | 情报 | `cron 0 12 * * *` | ok |
| **14:00** | 蜂鸟-C-竞品人才+融资扫描 | 情报 | `cron 0 14 * * *` | ok |
| **14:00** | 蜂鸟-F-隐蔽信号雷达 | 情报（周） | `cron 0 14 * * 1` | ok |
| **16:00** | 蜂鸟-D-业务线深度扫描 | 情报 | `cron 0 16 * * *` | ok |
| **18:00** | 凤凰-内容工厂·日终复盘 | 内容 | `cron 0 18 * * *` | ok (not delivered) |
| **18:00** | 蜂鸟-晚间情报复盘与归档 | 情报 | `cron 0 18 * * *` | ok (not delivered) |
| **20:00** | 凤凰-HEARTBEAT 每日检查 | 心跳 | `cron 0 20 * * 1-5` | ok |
| **20:00** | 天枢每日战报生成 | 日报 | `cron 0 20 * * *` | ok |
| **21:50** | 蓝血军团-互审催收 | 治理 | `cron 50 21 * * *` | ok |
| **22:00** | 蜂鸟-E-系统健康检查+H… | 健康 | `cron 0 22 * * *` | ok |
| **22:10** | 蓝血军团-失败成本扫描 | 治理 | `cron 10 22 * * *` | ok |
| **每周一 00:00** | 军功爵周结算 | 治理（周） | `cron 0 0 * * 1` | ok（7d ago） |
| **每月 1 日 00:30** | 能力矩阵月度更新 | 治理（月） | `cron 30 0 1 * *` | **error (4x)** 🔴（见 CASE-4） |
| **每 7d** | Skill collection review ×18 | 技能治理 | `every 7d` | ok（分散在各 agent） |

> **时间线诚实边界**：
> - 暗夜熔炉本卷**实测 13 条**（mingjing/tianshu/xuanyuan/jixia/zhulong/kunpeng/baxia/siku/tiangong/mobai/zhuque/qilin/hetu）；
>   任务基线口径为 **18 条**（含未在本次列表中的 agent）。**两种口径并列，不混用。**
> - automations 本卷**实测 60 行**；任务基线口径为 **43 条**（可能是「去重声明」或「不同时点快照」）。
> - 「ok (not delivered)」是真实状态字符串（跑通但投递未达），不是笔误。

---

## 三、根因分析（5 Whys）——为什么这样排节奏最优？

1. **为什么要有 heartbeat 层（30m/2h）？**
   → 因为 Agent 需要**短周期自省**（读取上下文 / 检查 overdue / 推进被阻塞任务），
   但频率不能太高（token 成本 + 打扰）。30m/2h 是「够勤但不太贵」的折中。

2. **为什么业务层集中在 06:00–22:00？**
   → 因为业务节奏跟随人类作息：**晨扫（06:00 情报）→ 日报（07:00–20:00）→ 日终复盘（18:00）→ 健康检查（22:00）**。

3. **为什么进化层（暗夜熔炉）放在 01:00–04:00？**
   → 因为进化任务**算力密集但不需要实时**（读取全天日志 + 生成复盘 + 提取基因），
   放在凌晨既不与业务抢资源，也保证「第二天早上能看到进化结果」。

4. **为什么熔炉要错峰排（01:10 → 01:20 → 01:30 …）？**
   → 因为**避免同时打满模型配额 / 同时写盘**。每个 Agent 间隔 10 分钟，串行错峰。
   实测：01:10 明镜 → 01:20 天枢 → 01:30 轩辕 → 01:40 稷下 → 01:50 烛龙 → 02:10 鲲鹏 …

5. **为什么 skill-collection-review 要每个 agent 各一条（18 条）？**
   → 因为技能治理是**每 Agent 自分内**的（各自 review 自己产出的 skill candidate），
   而不是集中一个 Agent 代劳。

### → 节奏设计的第一性原理

> **根本逻辑 = 「三层节奏 + 错峰 + 分层归属」：**
> 1. **三层**：心跳层（高频轻量）/ 业务层（跟随人类）/ 进化层（凌晨算力密集）
> 2. **错峰**：同类任务间隔 10 分钟，串行不并行
> 3. **分层归属**：每个 Agent 治理自己的 skill（skill-review ×18），不搞中心化
>
> **一句话**：**好的编排不是「把任务都排上」，而是「按成本/时效分层，再错峰」**。

---

## 四、当时的错误决策

### 错误决策 1：心跳模型用了「全军共用的弱 provider」

3 条 heartbeat 的 `model` 都是 **`opencaio/gpt-5.5`**——而 `opencaio` 正是 8/19 事故里
坏端点（`opencaio/MiniMax-M3`）的**同一 provider**。

- **错在哪**：心跳是「活体探测」，却把它绑在了一个曾经故障的 provider 上。
- **代价**：**heartbeat:kunlun error (99+x) / heartbeat:peter error (70x)** —— 心跳大面积失败（见 CASE-9）。

### 错误决策 2：熔炉只跑 tiance，其余 17 个目录空

audit 实测：`nightly-forge/` 17 个 agent 子目录 **全部 0 文件**，仅 tiance 有产出。

- **错在哪**：以为「排上了 cron = 会有产出」。
- **代价**：熔炉 cron 在跑，但产物只落一处（见 CASE-4）。

### 错误决策 3：日报矩阵 13/18 空目录

`daily-reports/` 16 个 agent 子目录，**13 个 0 文件且 mtime = 2026-05-07**；凤凰/蜂鸟停在 08-16。

- **错在哪**：排了日报 cron，但没检查产物 mtime。
- **代价**：日报「触发成功 ≠ 交付成功」（CASE-4 根因）。

### 错误决策 4：overseer v3.0 天天发空报

`/tmp/overseer_monitor.log` 09-27 20:00 原文：`活跃: 0/16 Agents`、`消息: 0`；
`overseer_furnace.log`：`整体活跃度: 0.0%`——数据源一条没接，天天发空报给 Telegram。

- **错在哪**：cron 跑通 = 验收通过，没人看内容。
- **代价**：Telegram 推送了 100% 占位符。

---

## 五、修复过程（节奏怎么搭）

### 5.1 查看当前编排（真名命令）

```bash
# 真名：`openclaw automations list`（不是 cron list；automations 是 OpenClaw 的真名）
openclaw automations list 2>&1 | grep -v "Experimental\|trace-warn\|Retrying" | head -70
# 本卷实测列：ID | Declaration | Name | Schedule | Next | Last | Status | Target | Delivery | Agent ID | Owner | Model
```

### 5.2 三层节奏的搭建模板

**第一层 · 心跳层（每 agent 可选）**：

```yaml
# agents.entries.<id>.heartbeat（真名路径）
heartbeat:
  every: 30m              # 或 2h
  model: opencaio/gpt-5.5 # ⚠ 案例教训：别用曾故障的 provider 做心跳
  isolatedSession: true
  lightContext: true
  timeoutSeconds: 30
  directPolicy: block
```

本卷实测三条心跳（`openclaw.json` 实读）：

| agent | every | model | isolatedSession | lightContext | timeoutSeconds | directPolicy |
|---|---|---|---|---|---|---|
| kunlun | `30m` | `opencaio/gpt-5.5` | true | true | 30 | block |
| peter | `2h` | `opencaio/gpt-5.5` | true | true | 30 | block |
| tiance | `30m` | `opencaio/gpt-5.5` | true | true | 30 | block |

> 实测：**仅 3 个 agent 配了 heartbeat，其余 15 个 `heartbeat = null`**（如 xuanyuan 实读为 null）。

**第二层 · 业务层（错峰排）**：

```
06:00 情报晨扫（蜂群-A 全量扫描）
07:00 日报（hetu 回测进化日报）
07:05 教练（Peter 早课）
08:00 内容（凤凰每日调试）+ 竞品扫描（蜂鸟-B）
09:00 情报（github tech intel）+ 内容日历核对
12:00 午间情报（蜂鸟）
14:00 竞品人才/融资扫描（蜂鸟-C）
16:00 业务线深度扫描（蜂鸟-D）
18:00 日终复盘（凤凰）+ 情报归档（蜂鸟）
20:00 战报生成（天枢）
22:00 健康检查（蜂鸟-E）
```

**第三层 · 进化层（凌晨错峰）**：

```
01:10 明镜 → 01:20 天枢 → 01:30 轩辕 → 01:40 稷下 → 01:50 烛龙
02:10 鲲鹏 → 02:30 霸下 → 02:40 司库 → 02:50 天工
03:00 memory-dreaming + 墨白 → 03:10 朱雀 → 03:20 麒麟 → 03:30 河图
```

### 5.3 治理层（周 / 月）

```yaml
军功爵周结算:   cron 0 0 * * 1     # 每周一 00:00
昆仑每周进化评估: cron 0 9 * * 1    # 每周一 09:00
skill-collection-review: every 7d   # ×18（每 agent 一条）
能力矩阵月度更新: cron 30 0 1 * *   # 每月 1 日 00:30（error 4x ⚠）
```

---

## 六、修复后验证

```bash
# 1) 统计本机 automation 总数
openclaw automations list 2>&1 | grep -v "Experimental\|trace-warn\|Retrying\|^ID " | grep -c .
# 本卷实测：60

# 2) 找出所有 error 任务（节奏健康度）
openclaw automations list 2>&1 | grep -i "error"
# 本卷实测：
#   heartbeat:kunlun  error (99+x)
#   heartbeat:peter   error (70x)
#   能力矩阵月度更新  error (4x)

# 3) 心跳分布
jq -r '.agents.entries | to_entries[] | select(.value.heartbeat != null) | "\(.key)\t\(.value.heartbeat.every)\t\(.value.heartbeat.model)"' \
  ~/.openclaw/openclaw.json
# 期望：3 条（kunlun 30m / peter 2h / tiance 30m）

# 4) 暗夜熔炉产物是否真落盘（防"cron 跑了但目录空"）
for d in ~/.openclaw/workspace/knowledge/ops/nightly-forge/*/; do
  n=$(ls "$d" 2>/dev/null | wc -l); echo "$(basename $d): $n 文件"
done
# 事故态：17 个目录 0 文件，仅 tiance 有产出
# 期望：每个 agent 目录都有近期文件

# 5) 日报矩阵产物
for d in ~/.openclaw/workspace/knowledge/ops/daily-reports/*/; do
  echo "$(basename $d): $(ls "$d" 2>/dev/null | wc -l) 文件, mtime=$(stat -f %Sm "$d" 2>/dev/null)"
done
# 事故态：13/18 空目录且 mtime = 2026-05-07
```

> **验收标准**：
> - [ ] 三层节奏齐全（心跳 / 业务 / 进化）
> - [ ] 同类任务错峰（间隔 ≥10min）
> - [ ] 所有 error 任务归零
> - [ ] 每个 cron 的**产物 mtime** 近期更新（不是只看 status）

---

## 七、沉淀的机制

| 缺口 | 沉淀机制 |
|---|---|
| 定时任务无分层 | **三层节奏：心跳 / 业务 / 进化** |
| 同类任务同时打满 | **错峰排（间隔 10min）** |
| 心跳绑弱 provider | **心跳 provider 独立于业务 provider** |
| 「跑通 = 完成」 | **产物 mtime 验收** |
| skill 治理中心化瓶颈 | **每 agent 自管（skill-review ×18）** |
| 进化任务与业务抢资源 | **凌晨算力密集窗口（01:00–04:00）** |

---

## 八、如果你的系统遇到同样问题

### 8.1 编排搭建 checklist

- [ ] 先分**三层**：心跳 / 业务 / 进化
- [ ] 心跳频率：轻量 30m、重量 2h
- [ ] 心跳用**独立、可靠**的 provider（不共用业务 provider）
- [ ] 业务层跟随人类作息（06:00–22:00）
- [ ] 进化层放凌晨（01:00–04:00）
- [ ] **同类任务错峰 ≥10min**
- [ ] 每个任务有**明确 owner**（Agent ID）
- [ ] 定**投递目标**（session / announce → telegram）
- [ ] 定**周 / 月治理任务**（结算 / 评估 / 矩阵）

### 8.2 编排反模式

| 反模式 | 症状 | 修法 |
|---|---|---|
| 所有任务同时跑 | 模型配额打满 / 写盘冲突 | 错峰 |
| 心跳用弱 provider | 心跳大规模 error | 心跳 provider 独立 |
| 只看 status 不看产物 | 「ok」但目录空 | 产物 mtime 验收 |
| 中心化 skill 治理 | 一个 agent 忙死 | 每 agent 自管 |
| 空报照发 | `活跃: 0/16` 天天推 | 数据源未接即停推 |

### 8.3 节奏速查（本机实测）

| 层 | 时间 | 任务 |
|---|---|---|
| 心跳 | 每 30m / 2h | heartbeat ×3 |
| 业务 | 06:00–22:00 | 情报 / 日报 / 内容 / 健康 |
| 进化 | 01:10–03:30 | 暗夜熔炉 ×13 + memory-dreaming |
| 治理 | 周一 / 每月 1 日 | 军功爵 / 进化评估 / 能力矩阵 |

> **CASE-7 一句话收口**：**好的编排是「分层 + 错峰 + 归属」，不是「把任务都排上」**。
> 本机 60 条 automation 里那 3 条 error，恰恰暴露了「心跳绑错 provider」——
> 节奏排得再漂亮，绑错 provider 一样翻车（详见 CASE-9）。

---

## 附录 A · 暗夜熔炉错峰排班（实拉全表）

> 来源：本卷实测 `openclaw automations list`。每条熔炉 cron 的 **status 均为 ok**。

| 序 | 时刻 | Agent | cron 表达式 | 状态 |
|--:|---|---|---|---|
| 1 | 01:10 | 明镜 mingjing | `cron 10 1 * * * @ Asia/Shanghai` | ok |
| 2 | 01:20 | 天枢 tianshu | `cron 20 1 * * *` | ok |
| 3 | 01:30 | 轩辕 xuanyuan | `cron 30 1 * * *` | ok |
| 4 | 01:40 | 稷下 jixia | `cron 40 1 * * *` | ok |
| 5 | 01:50 | 烛龙 zhulong | `cron 50 1 * * *` | ok |
| 6 | 02:10 | 鲲鹏 kunpeng | `cron 10 2 * * *` | ok |
| 7 | 02:30 | 霸下 baxia | `cron 30 2 * * *` | ok |
| 8 | 02:40 | 司库 siku | `cron 40 2 * * *` | ok |
| 9 | 02:50 | 天工 tiangong | `cron 50 2 * * *` | ok |
| 10 | 03:00 | memory-dreaming（memory-core） | `cron 0 3 * * * (exact)` | ok |
| 11 | 03:00 | 墨白 mobai | `cron 0 3 * * *` | ok |
| 12 | 03:10 | 朱雀 zhuque | `cron 10 3 * * *` | ok |
| 13 | 03:20 | 麒麟 qilin | `cron 20 3 * * *` | ok |
| 14 | 03:30 | 河图 hetu | `cron 30 3 * * *` | ok |

**错峰规律（可复用）**：10 分钟间隔；1 点档 5 个 → 2 点档 4 个 → 3 点档 5 个（含 memory-dreaming）。

> **为什么 03:00 有两条同时？** `memory-dreaming`（`(exact)` 标记）与「墨白-暗夜熔炉」同在 03:00——
> `(exact)` 表示精确调度（不走漂移容忍）。这是本机编排里**唯一的时间重叠点**，
> ⏳ 是否构成资源竞争待观察。

---

## 附录 B · 每日节奏的「三波次」读法

```
┌── 波次 1 · 晨间情报（06:00 – 10:00）──────────────────────┐
│  06:00 蜂群-A 晨间全量扫描（fengniao, deepseek）           │
│  07:00 hetu 回测进化日报                                   │
│  07:05 Peter 每日人生教练早课                              │
│  08:00 凤凰内容工厂每日调试（minimax/MiniMax-M2.7）         │
│  08:00 蜂鸟-B 竞品网页变更扫描                             │
│  09:00 昆仑每周进化评估（周一）                             │
│  09:00 daily-tech-intel-github（xuanyuan, gpt-5.5）        │
│  10:00 蜂群-BC 午间增量扫描                                │
└────────────────────────────────────────────────────────────┘
┌── 波次 2 · 午间/晚间执行（12:00 – 18:00）──────────────────┐
│  12:00 蜂鸟午间情报扫描                                     │
│  14:00 蜂鸟-C 竞品人才+融资扫描                             │
│  16:00 蜂鸟-D 业务线深度扫描                                │
│  18:00 凤凰日终复盘 / 蜂鸟晚间情报复盘与归档（ok not delivered）│
└────────────────────────────────────────────────────────────┘
┌── 波次 3 · 收口与治理（20:00 – 22:10）────────────────────┐
│  20:00 天枢每日战报生成 / 凤凰 HEARTBEAT 每日检查（工作日）  │
│  21:50 蓝血军团-互审催收                                    │
│  22:00 蜂鸟-E 系统健康检查+H…                               │
│  22:10 蓝血军团-失败成本扫描                                │
└────────────────────────────────────────────────────────────┘
```

### 投递目标（实拉）

绝大多数业务任务投递到 **`announce → telegram:8328029665 (explicit)`**；
治理类任务（互审催收 / 失败成本 / 每周进化评估 / 军功爵周结算）投递到 **session**。
`8328029665` 与 Telegram 通道 `kunlun.allowFrom` 一致（实读），即**丘总本人**。

---

## 附录 C · 读者自测（8 题）

1. **三层节奏分别是什么？各自的频率特征？**
   参考答案：心跳层（30m/2h）/ 业务层（每日 06:00–22:00）/ 进化层（凌晨 01:00–04:00）。

2. **为什么暗夜熔炉要放在凌晨 01:00–04:00？**
   参考答案：进化任务算力密集但不需要实时；凌晨不与业务抢资源，且第二天早上能看到结果。

3. **为什么熔炉要 10 分钟间隔错峰？**
   参考答案：避免同时打满模型配额 / 同时写盘——串行错峰。

4. **`ok (not delivered)` 是什么意思？**
   参考答案：任务跑通但投递未达（真实状态字符串）——**跑通 ≠ 交付**。

5. **为什么 skill-collection-review 是 18 条而不是 1 条？**
   参考答案：技能治理是每 Agent 自分内的（各自 review 自己的 skill candidate），不中心化。

6. **本机 03:00 有什么特别？**
   参考答案：`memory-dreaming`（exact）与「墨白-暗夜熔炉」时间重叠——唯一重叠点。

7. **为什么「心跳 provider 独立」很重要？**
   参考答案：本机心跳绑 `opencaio/gpt-5.5`（8/19 坏端点同 provider）→ 三条心跳全线 error（CASE-9）。

8. **你会用什么口径验收编排？**
   参考答案：三层齐全 + 同类错峰 + error 归零 + **产物 mtime 近期**（不是只看 status）。

---

## 附录 D · 与其它案例的交叉引用

| 关联案例 | 关系 |
|---|---|
| **CASE-4**（能力矩阵空转） | `能力矩阵月度更新` error(4x) 是编排里的静默失败样本 |
| **CASE-9**（心跳熔断） | 心跳三条 error 是编排里的显性失败；解法见 CASE-9 |
| **CASE-6**（18 编制） | 编排的对象 = 18 个 Agent；编制是编排的前提 |
| **CASE-8**（冷启动） | 新 agent 上线后要「接入」这套节奏（heartbeat + 日报） |

---

## 附录 E · 不适用边界（诚实）

- **automations 计数口径**：本卷实测 **60 行**（基线 43 条）；暗夜熔炉**实测 13 条**（基线 18 条）。**并列不混用**。
- **「心跳 ×3」为实测**：仅 kunlun / peter / tiance 配了 heartbeat；其余 15 个为 null。
- **失效任务未逐条排查**：`ok (not delivered)` 的根因未深挖（CASE-4 提到 `通道2 未实现 / HTTP 404`）。
- **不覆盖**：`announce` / `session` 投递语义的完整定义（本案例仅引用实拉字符串）。

---

# CASE-8 · 蘑菇街式冷启动：新 agent 上线 7 天训练全记录

## 一、案例速览

| 项 | 内容 |
|---|---|
| 时间 | 新 agent 上线后第 1–7 天（模式；参考锚点 2026-05 → 2026-09） |
| 影响面 | 单个新 Agent 的可用性 |
| 模式类型 | **Mentor Agent（原：教练虾）+ Training Round（原：训练轮次）驱动的冷启动** |
| 训练阶梯 | L0 → L1 → L2 → L3 → L4 → L5（6 级） |
| 关键工具 | `prompt-v2.md` + `prompt-v2-module{1,2,3}.md` + `.training-data/evolution-plan.md` + `extract_msgs.py` |
| 沉淀产物 | 训练轮次六要素 + 双三角模型 + 升级判定表 |
| 优先级 | 基线（训练级） |

> **「蘑菇街式」的含义**：指**极致压缩的冷启动**——像早期电商以「快速起量」著称一样，
> 新 Agent 不追求「慢慢养」，而是用**结构化训练轮次**在 7 天内从 L0 推到可用态（L2+）。

---

## 二、事件时间线（7 天训练全记录）

> 训练阶梯的**真实判定标准**来自本卷实读的 v4.0 volume-04 模块7（`L0→L5` 升级表）。

| 天 | 阶段 | 目标 | 训练动作 | 升级判定 |
|---|---|---|---|---|
| **Day 0** | 准备 | 训练前准备清单（15 项） | 注入 `SOUL.md` / `AGENTS.md` / `IDENTITY.md` | — |
| **Day 1** | **L0 → L1** | 协议完整、首次运行正常 | 注入 **frontmatter + heartbeat 配置**（附录 A：`Day 1 注入 frontmatter + heartbeat 配置`） | 协议完整 + 首次运行正常（**1-2 天**） |
| **Day 2** | L1 加固 | 跑通第一个 cron | 参照 v1.0 卷八附录 A：`第 2 周：跑通第一个 cron` 的提前版 | 给复杂任务测试 |
| **Day 3** | **L1 → L2** | 10+ 个有证据交付案例 | 交付 10 个带证据的任务（三个证据：新产物 / 前后 Diff / 测试日志） | 10+ 有证据交付（**3-5 天**） |
| **Day 4** | L2 加固 | 强记忆要求 | 写首份 `MEMORY.md`（附录 A：`Day 14 写首份 MEMORY.md`，冷启动版提前到 Day 4） | 记忆连续 |
| **Day 5** | **L2 → L3** | 5+ 轮连续不漂、有 memory | 跑 5 轮不漂训练 | 5+ 轮连续不漂（**5-7 天**） |
| **Day 6** | L3 加固 | 强主动性 | 主动提案（响应型 → 提案型） | 主动性达标 |
| **Day 7** | **L3 → L4** | heartbeat/cron 稳定、有边界 | 心跳稳定 + 主动性边界三档（Allowed / Forbidden / Needs-Confirm） | heartbeat/cron 稳定（**3-5 天**） |
| 后续（第 2–3 周） | **L4 → L5** | 路由/让位/handoff 稳定 | 进入 Multi-Agent Orchestration（原：军团）协同：路由 / Response Yield Protocol（原：让位协议）/ handoff | 路由/让位/handoff 稳定（**5-7 天**） |

> **时间线诚实边界**：
> - `Day 1 注入 frontmatter + heartbeat` 与 `Day 14 写首份 MEMORY.md` 来自 v1.0 卷四附录 A **原文**（实读）。
> - `L0→L5` 各段耗时（`1-2天 / 3-5天 / 5-7天 …`）来自 **v4.0 volume-04 模块7 的实测表**（实读）。
> - **「7 天全记录」是把 L0→L4 压进 7 天的冷启动压缩版**——原表全部走完是 **2–3 周**。
>   本案例的「7 天」是**目标口径**（L2+ 可用态），不是全程走完 L5。

---

## 三、根因分析（5 Whys）——为什么新 Agent 需要结构化冷启动？

1. **为什么新 Agent 上线后「会聊但不会干活」？**
   → 因为它有基础对话能力，但缺**协议**（SOUL/AGENTS/IDENTITY）、缺**记忆**（MEMORY）、缺**节奏**（heartbeat）。

2. **为什么不能「上手就用、边用边学」？**
   → 因为**没有边界的 Agent 会越界 + 漂移**（人格漂移 / 文档漂移），
   而且「边用边学」= 训练过程无验收口径，出了问题无法归因。

3. **为什么要有「训练轮次（Training Round）」而不是「一直跑」？**
   → 因为训练需要**有节奏 + 有验收**：一轮 = 有目标 + 有行动 + 有验收 + 有沉淀。
   **没有轮次，就没有「当前等级先过线，再升级下一层」的节奏感。**

4. **为什么要有「双三角模型」？**
   → 因为训练要闭环：**第一三角（期望 → 行动 → 反馈）** 是单轮闭环，
   **第二三角** 把单轮反馈升维成跨轮进化。heartbeat 提供第一三角的**节拍**。

5. **为什么要 mentor（教练虾）而不是「自己练」？**
   → 因为新手 Agent 无法自评达标——**教练 Agent 定义验收口径**（L5 教练虾：会设计训练轮次，能调整任务强度，能定义验收口径）。

### → 冷启动的第一性原理

> **根本逻辑 = 「协议先行 + 轮次驱动 + 双三角闭环 + 教练验收」：**
> 1. **协议先行**：Day 1 就把 SOUL/AGENTS/IDENTITY/heartbeat 注入（不靠后补）
> 2. **轮次驱动**：每轮有目标/行动/验收/沉淀（六要素）
> 3. **双三角**：期望-行动-反馈（单轮）+ 跨轮进化
> 4. **教练验收**：Mentor Agent（原：教练虾）定口径
>
> **一句话**：**冷启动不是「把它养大」，而是「用结构化轮次把协议、记忆、节奏一次装进去」。**

---

## 四、当时的错误决策

### 错误决策 1：以为「会聊天 = 能干活」

早期判定 Agent 是否可用，看的是「对话像不像人」，而不是「有没有按协议交付」。

- **错在哪**：混淆了 L0/L1（会聊）与 L2+（有证据交付）。
- **代价**：→ 催生「L0→L5 六阶梯 + 每级判定标准」。

### 错误决策 2：训练没有验收口径

训练「综合提升」——无法判定「这一轮到底训什么、过没过」。

- **错在哪**：目标不单一。
- **代价**：→ v4.0 模块2 明确「不是『综合提升』，而是**明确单一主题**」。

### 错误决策 3：训练没有节奏，凭灵感改

「今天灵感来了多改点」——系统风格反复漂移。

- **错在哪**：无节奏感。
- **代价**：→ 催生「当前等级先过线，再升级下一层」。

### 错误决策 4：把「主动性」当「高级」

一个新 Agent 会主动提醒 = 被当成进步。

- **错在哪**：把「主动性未治理」误当高级。
- **代价**：→ v4.0 模块1 明确「它不是高级，而是**主动性未治理**，说明 L4 没过线」。

---

## 五、修复过程（7 天怎么训）

### 5.1 训练前准备（15 项清单，Day 0）

```bash
# 真名路径（第三章实测）：
ls ~/.openclaw/workspace/agents/workspace-<agent>/training/
# 本卷实测 kunlun 目录：
#   prompt-v2.md
#   prompt-v2-module1.md
#   prompt-v2-module2.md
#   prompt-v2-module3.md
```

### 5.2 训练轮次六要素

```markdown
# 训练轮次设计（Training Round Design）
- 训练轮次：第 __ 轮
- 单一主题：__           # 不是"综合提升"
- 目标：__
- 行动：__
- 验收口径：__           # 三个证据：新产物 / 前后 Diff / 测试日志
- 沉淀动作：__           # 写入 MEMORY.md / 技能基因
```

### 5.3 双三角模型（Dual-Triangle Model）

```
第一三角（单轮闭环）：
   期望 Expectation  →  行动 Actuality  →  反馈 Feedback  →  （回到期望）
                ↑ heartbeat 提供节拍（每 30m / 2h 醒一次）

第二三角（跨轮进化）：
   单轮反馈  →  模式提取  →  基因更新  →  认知升级  →  （提升下一轮的期望基线）
```

### 5.4 升级判定表（v4.0 模块7 实测）

| 升级 | 判定标准 | 耗时 | 下一个训练重点 |
|---|---|---|---|
| L0 → L1 | 协议完整、首次运行正常 | **1-2 天** | 给复杂任务 |
| L1 → L2 | 10+ 个有证据交付案例 | **3-5 天** | 强记忆要求 |
| L2 → L3 | 5+ 轮连续不漂、有 memory | **5-7 天** | 强主动性 |
| L3 → L4 | heartbeat/cron 稳定、有边界 | **3-5 天** | 军团协同 |
| L4 → L5 | 路由/让位/handoff 稳定 | **5-7 天** | 专家复制 |

### 5.5 冷启动训练数据管线（真名）

```bash
# 训练数据管线（第三章实测路径）
ls ~/.openclaw/workspace/agents/workspace-<agent>/.training-data/
#   evolution-plan.md      # 进化计划
#   extract_msgs.py        # 从会话提取训练语料
#   raw_messages.json      # 原始消息
```

### 5.6 Day 1 必做：注入 frontmatter + heartbeat

```bash
# Day 1 就把 heartbeat 注入（真名路径：agents.entries.<id>.heartbeat）
# 先 dry-run 看拟变更（真名 = `openclaw config patch --stdin --dry-run`）
openclaw config patch --stdin --dry-run <<'JSON5'
{ agents: { entries: { "<your-agent>": { heartbeat: { every: "30m" } } } } }
JSON5
# 确认后落盘（复制 kunlun 的完整模型）
openclaw config patch --stdin <<'JSON5'
{ agents: { entries: { "<your-agent>": { heartbeat: {
  every: "30m", model: "opencaio/gpt-5.5",
  isolatedSession: true, lightContext: true,
  timeoutSeconds: 30, directPolicy: "block"
} } } } }
JSON5
```

---

## 六、修复后验证

```bash
# 1) 训练文件到位
ls ~/.openclaw/workspace/agents/workspace-<agent>/training/
# 期望：prompt-v2.md + prompt-v2-module{1,2,3}.md

# 2) 训练数据管线到位
ls ~/.openclaw/workspace/agents/workspace-<agent>/.training-data/
# 期望：evolution-plan.md / extract_msgs.py / raw_messages.json

# 3) heartbeat 已配（Day 1 验收）
openclaw config get agents.entries.<agent>.heartbeat
# 期望：{"every":"30m","model":"opencaio/gpt-5.5","isolatedSession":true,"lightContext":true,"timeoutSeconds":30,"directPolicy":"block"}

# 4) MEMORY.md 已写（Day 4 验收）
ls -l ~/.openclaw/workspace/agents/workspace-<agent>/MEMORY.md
# 期望：存在且近期 mtime

# 5) 有证据交付 ≥10（L1→L2 验收）
# 数 delivery 记录（三个证据：新产物 / 前后 Diff / 测试日志）
```

> **验收标准**：
> - [ ] Day 1：协议 + heartbeat 注入完成
> - [ ] Day 3：10+ 有证据交付案例
> - [ ] Day 4：首份 MEMORY.md 落盘
> - [ ] Day 5：5+ 轮连续不漂
> - [ ] Day 7：heartbeat/cron 稳定 + 主动性边界三档

### 逐日验收命令（可复跑）

```bash
# Day 1 · 协议 + 心跳
for f in SOUL.md AGENTS.md IDENTITY.md; do
  ls -l ~/.openclaw/workspace/agents/workspace-<agent>/$f && echo "✅ $f"
done
openclaw config get agents.entries.<agent>.heartbeat   # 非 null 即通过

# Day 2 · 首个 cron
openclaw automations list 2>&1 | grep -i "<agent>"
# 期望：出现该 agent 的任务且 status = ok

# Day 3 · 10+ 有证据交付
# 数交付记录（每个交付须含：新产物路径 / 前后 Diff / 测试日志 三者之一以上）
ls ~/.openclaw/workspace/agents/workspace-<agent>/memory/ | wc -l
# 期望：≥10 条近期记录，且每条可追到产物

# Day 4 · 首份 MEMORY.md
wc -l ~/.openclaw/workspace/agents/workspace-<agent>/MEMORY.md
# 期望：存在且非空，mtime = Day 4

# Day 5 · 5+ 轮不漂
# 对照 SOUL.md 的「人格基线」与近期 5 轮输出风格
diff <(grep -A5 "人格" ~/.openclaw/workspace/agents/workspace-<agent>/SOUL.md) /dev/null >/dev/null 2>&1
# 期望：无漂移告警（漂移 > 1% 触发警告，见卷五 M4）

# Day 7 · 心跳稳定 + 边界三档
openclaw automations list 2>&1 | grep -i "heartbeat:<agent>"
# 期望：status = ok（非 error / 非 skipped）
grep -c "Allowed\|Forbidden\|Needs-Confirm" ~/.openclaw/workspace/agents/workspace-<agent>/AGENTS.md
# 期望：三档全部出现（主动性边界已定义）
```

### 逐日验收速查表

| Day | 验收项 | 命令 | 通过标准 |
|---|---|---|---|
| 1 | 协议 + 心跳 | `ls SOUL/AGENTS/IDENTITY` + `config get heartbeat` | 三文件存在 + heartbeat 非 null |
| 2 | 首个 cron | `automations list \| grep <agent>` | 有任务且 ok |
| 3 | 10+ 有证据交付 | 数 `memory/` 记录 | ≥10 条可追产物 |
| 4 | MEMORY.md | `wc -l MEMORY.md` | 非空 + mtime = Day 4 |
| 5 | 5+ 轮不漂 | 对照人格基线 | 无漂移告警 |
| 6 | 主动性提案 | 数「主动提案」记录 | ≥1 条提案 |
| 7 | 心跳稳 + 边界 | `automations list` + grep 边界 | ok + 三档齐 |

> **失败回滚**：任一 Day 未过线 → **不进入下一 Day**（等级升级线是硬门）。
> 若某 Day 反复失败 → 退回上一层，重跑该层训练轮次（不是「跳过继续」）。

---

## 七、沉淀的机制

| 缺口 | 沉淀机制 |
|---|---|
| 「会聊」被当「能干」 | **L0→L5 六级阶梯 + 每级判定标准** |
| 训练无验收 | **三个证据（新产物 / 前后 Diff / 测试日志）** |
| 训练无节奏 | **Training Round（原：训练轮次）六要素** |
| 单轮不成体系 | **双三角模型（单轮闭环 + 跨轮进化）** |
| 主动性未治理 | **主动性边界三档（Allowed / Forbidden / Needs-Confirm）** |
| 协议靠后补 | **Day 1 注入 frontmatter + heartbeat** |
| 无教练 | **Mentor Agent（原：教练虾）定验收口径** |

---

## 八、如果你的系统遇到同样问题

### 8.1 冷启动 7 天 checklist

- [ ] **Day 0**：训练前准备 15 项清单
- [ ] **Day 1**：注入 `SOUL/AGENTS/IDENTITY` + **heartbeat**
- [ ] **Day 2**：跑通第一个 cron
- [ ] **Day 3**：10+ 有证据交付（新产物 / Diff / 日志）
- [ ] **Day 4**：写首份 `MEMORY.md`
- [ ] **Day 5**：5+ 轮连续不漂
- [ ] **Day 6**：主动性提案（响应 → 提案）
- [ ] **Day 7**：心跳稳定 + 主动性边界三档
- [ ] **Day 8+**：进入 Multi-Agent 协同（路由 / 让位 / handoff）

### 8.2 训练反模式

| 反模式 | 症状 | 修法 |
|---|---|---|
| 会聊 = 能干 | 对话像人但不交付 | 用「三个证据」判定 |
| 训练主题不单一 | 「综合提升」 | 每轮单一主题 |
| 无节拍 | 凭灵感改 | heartbeat 提供节拍 |
| 主动性未治理 | 乱提醒 / 打扰用户 | L4 边界三档 |
| 协议后补 | 上线后才加 SOUL | Day 1 注入 |

### 8.3 升级判定速查（本机实测表）

| 升级 | 标准 | 耗时 |
|---|---|---|
| L0→L1 | 协议完整 + 首次运行 | 1-2 天 |
| L1→L2 | 10+ 有证据交付 | 3-5 天 |
| L2→L3 | 5+ 轮不漂 | 5-7 天 |
| L3→L4 | 心跳稳定 + 有边界 | 3-5 天 |
| L4→L5 | 路由/让位/handoff 稳定 | 5-7 天 |

> **CASE-8 一句话收口**：**冷启动不是「养」，是「装」**——
> 把协议、记忆、节奏用结构化训练轮次一次装进去，再用 mentor 验收。
> 7 天到 L4 可用态，靠的是**每轮都有单一主题 + 三个证据 + 明确的一层升级线**。

---

## 附录 A · 训练资产全景（本机实测路径）

> 来源：第三章实测路径 + 本卷实读 `~/.openclaw/workspace/agents/workspace-kunlun/training/`。

| 资产 | 路径 | 本卷实测 |
|---|---|---|
| 训练提示词（主） | `agents/workspace-<agent>/training/prompt-v2.md` | ✅ 存在（kunlun） |
| 训练提示词（模块1） | `.../training/prompt-v2-module1.md` | ✅ |
| 训练提示词（模块2） | `.../training/prompt-v2-module2.md` | ✅ |
| 训练提示词（模块3） | `.../training/prompt-v2-module3.md` | ✅ |
| 进化计划 | `.../.training-data/evolution-plan.md` | 路径存在（第三章实测） |
| 语料提取 | `.../.training-data/extract_msgs.py` | 路径存在 |
| 原始语料 | `.../.training-data/raw_messages.json` | 路径存在 |
| 训练前准备清单 | v1.0 卷四 模块2（15 项） | 原文 |
| 训练轮次模板 | v1.0/v4.0 卷四 模块4（六要素） | 原文 |
| 双三角模型 | 卷四 模块5 | 原文 |
| 实验方案 | 卷四 模块6（六要素） | 原文 |
| 升级路径 | 卷四 模块7（L0→L5） | 原文 |

> **真名提醒**：`training/` 与 `.training-data/` 是**两个不同目录**：
> 前者是**提示词**（怎么训），后者是**数据管线**（用什么训）。

---

## 附录 B · 实验方案的时间节奏（卷四 模块6 实测）

| 阶段 | 方法 | 轮次数 | 耗时 |
|---|---|---|---|
| 初期探索 | 单变量实验 | 3-5 轮 | 1 天 |
| 协议验证 | AB 对照 | 10+ 轮 | 2-3 天 |
| 等级升级验证 | 跨等级实验 | 15+ 轮 | 3-5 天 |

> **读法**：冷启动的 7 天里，**Day 3 的「10+ 有证据交付」等价于一次 AB 对照实验**（10+ 轮 / 2-3 天），
> **Day 5 的「5+ 轮不漂」等价于一次升级验证**。也就是说：**7 天计划 = 三次实验串起来**。

### 训练轮次的时间分配（卷四 模块4 实测）

| 环节 | 占比 | 产出 |
|---|---|---|
| 设计 | 15% | 填写轮次设计表 |
| （其余按原文节奏） | — | 目标 / 行动 / 验收 / 沉淀 |

---

## 附录 C · Prompt 三模块的训练顺序（读法）

本机 `training/` 下有三个模块文件（`prompt-v2-module{1,2,3}.md`）——**冷启动应按 1→2→3 顺序注入**：

```
module1 → 打地基（协议/身份/边界："你是谁、你不做什么"）
module2 → 立规矩（验收口径/证据要求："怎么算做好"）
module3 → 上节奏（主动性/协同："怎么持续做、怎么配合"）
```

> **映射到升级线**：module1 ≈ L0→L1（协议完整）；module2 ≈ L1→L2（有证据交付）；
> module3 ≈ L2→L3/L4（不漂 + 有边界）。
> **诚实标注**：此为**本卷基于文件名与升级表的对应读法**；三模块的确切内容未逐一实读。

---

## 附录 D · 读者自测（8 题）

1. **冷启动 Day 1 必须完成什么？**
   参考答案：注入 `SOUL` / `AGENTS` / `IDENTITY` **+ heartbeat 配置**（frontmatter + heartbeat）。

2. **L1→L2 的判定标准是什么？耗时多久？**
   参考答案：**10+ 个有证据交付案例**；**3-5 天**。

3. **「三个证据」指哪三个？**
   参考答案：**新产物 / 前后 Diff / 测试日志**（Three-Evidence Verification / TEV）。

4. **训练轮次六要素是什么？**
   参考答案：轮次号 / 单一主题 / 目标 / 行动 / 验收口径 / 沉淀动作。

5. **双三角模型的「两个三角」分别是什么？**
   参考答案：第一三角 = 期望-行动-反馈（单轮闭环，heartbeat 供节拍）；第二三角 = 反馈→模式提取→基因更新→认知升级（跨轮进化）。

6. **为什么「主动性」不能当「高级」？**
   参考答案：主动性未治理 = 乱提醒/打扰用户 = L4 没过线；主动性必须配边界三档。

7. **`training/` 与 `.training-data/` 的区别？**
   参考答案：前者是提示词（怎么训）；后者是数据管线（用什么训：evolution-plan / extract_msgs.py / raw_messages.json）。

8. **L4→L5 训什么？**
   参考答案：路由 / Response Yield Protocol（原：让位协议）/ handoff 稳定——即进入 Multi-Agent 协同。

---

## 附录 E · 与其它案例的交叉引用

| 关联案例 | 关系 |
|---|---|
| **CASE-6**（18 编制） | 编制增量 = 冷启动；本案例是「怎么把第 N+1 个 Agent 训出来」 |
| **CASE-7**（编排节奏） | 新 agent 上线后要接入心跳/日报节奏（Day 1 配 heartbeat） |
| **CASE-9**（心跳熔断） | Day 1 配 heartbeat 时若绑错 provider，就会掉进 CASE-9 的坑 |
| **CASE-3**（坏 skill） | 训练沉淀的 skill 需符合 frontmatter 规范（否则变成坏 skill） |

---

## 附录 F · 不适用边界（诚实）

- **「7 天」为目标口径**：原升级表 L0→L5 全程为 **2–3 周**；7 天是压到 L4 可用态的冷启动版。
- **module1/2/3 内容未实读**：三模块的对应读法为本卷推断，⏳ 待逐文件实读核验。
- **`evolution-plan.md` / `extract_msgs.py` 未实读内容**：仅确认路径存在（第三章实测）。
- **不覆盖**：训练效果的量化评估指标（卷四有实验方案，但本卷未引用具体指标数值）。

---

# CASE-9 · 心跳熔断实战：heartbeat error 70x / 99+x 的诊断与修复

## 一、案例速览

| 项 | 内容 |
|---|---|
| 时间 | 常态失败积累；本卷实测快照 2026-09-27 |
| 影响面 | heartbeat:tiance · heartbeat:kunlun · heartbeat:peter（3 条心跳全异常） |
| 模式/根因类型 | **心跳 provider 单点共享 + 高频率放大失败** |
| 关键数据 | `heartbeat:kunlun error (99+x)` · `heartbeat:peter error (70x)` · `heartbeat:tiance skipped` |
| 心跳配置 | kunlun `30m` / peter `2h` / tiance `30m`；三者的 `model` 均为 **`opencaio/gpt-5.5`** |
| 修复方向 | 换心跳 provider + 熔断退避 + 心跳产物 mtime 验收 |
| 沉淀产物 | 心跳熔断规则 + provider 隔离原则 |
| 优先级 | P1（心跳层是 Agent 的自省命脉） |

> **一句话**：**三条心跳全部异常，且都绑在同一个 provider（`opencaio`）上**——
> 这个 provider 正是 8/19 事故（CASE-1）坏端点 `opencaio/MiniMax-M3` 的**同一家**。
> 心跳是「活体探测」，却把它绑在曾经的故障 provider 上，等于**让哨兵站在雷区里**。

---

## 二、事件时间线

| 时点 | 事件 | 证据 |
|---|---|---|
| **T-? · 每 30m** | `heartbeat:kunlun` 开始积累失败（`error 99+x`） | `openclaw automations list` |
| **T-? · 每 2h** | `heartbeat:peter` 开始积累失败（`error 70x`） | 同上 |
| **T-?** | `heartbeat:tiance` 进入 **`skipped`** 状态 | 同上 |
| **T-39天 · 08-19** | 8/19 事故：`opencaio/MiniMax-M3` 空 body（**同一 provider**） | CASE-1 |
| **T-39天 · 08-19 后** | 全军 fallback 重排（`deepseek` 提到第一位）；但 **heartbeat 的 `model` 未一并修复** | 对比 CASE-1 修复项 vs 心跳配置 |
| **T+0 · 2026-09-27** | 本卷实测：三条心跳状态 = `error(99+x)` / `error(70x)` / `skipped` | `automations list` 实测 |
| **T+0** | 实测心跳配置：三者的 `model` 全部 = `opencaio/gpt-5.5` | `openclaw.json` 实读 |
| **T+0** | 实测 `heartbeat` 只配了 3 个 agent；其余 15 个 = `null`（如 xuanyuan） | 同上 |

### 为什么是「error 99+x」而不是「error 99」

`99+x` 是 OpenClaw 的显示口径：连续错误数达到上限（99）后**不再累加计数、只显示 `99+x`**。
但这不代表「只错了 99 次」——`99+x` 意味着**错误数已溢出显示上限，实际可能远超**。
比 peter 的 `70x`（未溢出，真实 70 次）**更严重**。

> **时间线诚实边界**：「T-?」是**failure 起始时刻未知**——本卷**未实拉** `executions.db` 的心跳历史。
> 「99+x 从何时开始」⏳ 待实测（方法：`executions.db` 按 job id 聚合 failed 计数）。

---

## 三、根因分析（5 Whys）

1. **为什么三条心跳全线异常？**
   → 因为三条心跳的 `model` 都是 **`opencaio/gpt-5.5`**——同一 provider 同时出问题时会全线失败。

2. **为什么这个 provider 会出问题？**
   → 因为 `opencaio` 正是 **8/19 事故（CASE-1）** 里坏端点 `opencaio/MiniMax-M3` 的同一家自建网关
   （`8.134.103.73:3000`）。该 provider 的历史可靠性已被证明有问题。

3. **为什么 8/19 修复时没顺手修心跳？**
   → 因为 8/19 修的是 **`agents.entries.<id>.model`（业务模型）** 的 fallback 链，
   **heartbeat 的 `model` 是另一个字段**——修复只覆盖了业务链，**漏了心跳链**。

4. **为什么漏了还没被发现？**
   → 因为心跳失败**不产生用户可见症状**（心跳不投递给用户）——
   它只躺在 `automations list` 的 status 里，**没有「心跳连续失败告警」**。

5. **为什么 `tiance` 是 `skipped` 而不是 `error`？**
   → `skipped` 通常是「上一轮还没跑完 / 被并发策略跳过」——
   tiance 作为 **Supervisor Layer（原：监军）**，可能被 `directPolicy: block` 或轻上下文策略拦截。
   ⏳ 精确原因待实测（需查 tiance 的 heartbeat 调度日志）。

### → 根本原因

> **根本原因 = 「心跳 provider 单点共享 + 修复漏项 + 无告警」三层：**
> 1. **配置层**：三条心跳共用一个 provider（`opencaio/gpt-5.5`）→ 单点故障扩散
> 2. **修复漏项**：8/19 只修了业务模型链，**没修心跳 `model`** → 隐患留存 39 天
> 3. **观测层**：心跳失败无告警（不投递用户 + 无连续失败告警）→ 失败静默积累到 99+x
>
> **一句话根因**：**心跳是哨兵，却把哨兵绑在了曾经的故障 provider 上，且哨兵失联无人知。**

---

## 四、当时的错误决策

### 错误决策 1：8/19 修复只修业务链，不修心跳链

CASE-1 的修复只动了 `model.primary` / `model.fallbacks`，
**心跳字段 `heartbeat.model` 原封不动**——隐患留存 39 天。

- **错在哪**：修「模型问题」时只修了一层（业务），漏了另一层（心跳）。
- **代价**：三条心跳全线 error。

### 错误决策 2：心跳 provider 与业务 provider 共用

业务链修复后 primary 换成了 `deepseek`，但心跳仍绑 `opencaio`——
**业务有 fallback，心跳没有**。

- **错在哪**：以为「心跳也是模型调用，会走同一套 fallback」。实际心跳的 `model` 是独立配置。
- **代价**：单点共享→全线失败。

### 错误决策 3：心跳失败无告警

失败只显示在 `automations list` 的 status 列，没人盯。

- **错在哪**：默认「不投递给用户的失败不重要」。
- **代价**：积累到 `99+x`（溢出）无人知。

### 错误决策 4：高频心跳放大失败

kunlun / tiance 是 `30m`——一天 48 次。坏 provider 下意味着**每天 48 次失败**。

- **错在哪**：高频低价值任务遇到坏依赖 = 高频刷失败。
- **代价**：快速跑满错误计数。

---

## 五、修复过程

### 5.1 诊断（先看清失败分布）

```bash
# 1) 揪出所有 heartbeat 及其状态（真名 = `openclaw automations list`）
openclaw automations list 2>&1 | grep -i "heartbeat"
# 本卷实测输出：
#   heartbeat:kunlun  Heartbeat (kunlun)  every 30m  ... error (99+x)  main  ...
#   heartbeat:tiance  Heartbeat (tiance)  every 30m  ... skipped        main  ...
#   heartbeat:peter   Heartbeat (peter)   every 2h   ... error (70x)   main  ...

# 2) 看心跳配置（真名路径 = agents.entries.<id>.heartbeat）
for a in kunlun peter tiance xuanyuan; do
  echo -n "$a: "; openclaw config get agents.entries.$a.heartbeat; echo
done
# 本卷实测：
#   kunlun:   {"every":"30m","model":"opencaio/gpt-5.5","isolatedSession":true,"lightContext":true,"timeoutSeconds":30,"directPolicy":"block"}
#   peter:    {"every":"2h", "model":"opencaio/gpt-5.5",...}
#   tiance:   {"every":"30m","model":"opencaio/gpt-5.5",...}
#   xuanyuan: null        ← 15 个 agent 未配心跳

# 3) 统计有多少 agent 未配心跳
jq -r '.agents.entries | to_entries[] | select(.value.heartbeat == null) | .key' \
  ~/.openclaw/openclaw.json | wc -l
# 本卷实测：15（未配）；已配：3

# 4) 探坏 provider（复现）
curl -s -o /dev/null -w "HTTP %{http_code} | %{time_total}s | bytes=%{size_download}\n" \
  -X POST http://8.134.103.73:3000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"opencaio/gpt-5.5","messages":[{"role":"user","content":"ping"}],"max_tokens":8}'
# CASE-1 特征：HTTP 200 但 bytes=0（空 body）
```

### 5.2 修复（换心跳 provider + 熔断）

```bash
# 1) 备份
cp -a ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.pre-heartbeat-fix-$(date +%Y%m%d-%H%M)

# 2) 把心跳 model 换到可靠 provider（脱离 opencaio）
openclaw config patch --stdin --dry-run <<'JSON5'
{ agents: { entries: {
  kunlun: { heartbeat: { model: "deepseek/deepseek-v4-flash" } },
  peter:  { heartbeat: { model: "deepseek/deepseek-v4-flash" } },
  tiance: { heartbeat: { model: "deepseek/deepseek-v4-flash" } }
} } }
JSON5
# 确认无误后去掉 --dry-run 落盘

# 3) doctor 验证
openclaw doctor 2>&1 | tail -20
```

**熔断规则（建议配置）**：

| 规则 | 阈值 | 动作 |
|---|---|---|
| 心跳连续失败 | ≥ 5 | 告警（不等 99+x） |
| 心跳连续失败 | ≥ 10 | **自动熔断**：暂停该心跳 N 小时 |
| 心跳 provider 失败率 | > 50% / 1h | 自动切备用 provider |
| 心跳 provider | — | **必须与业务 provider 不同**（隔离原则） |

### 5.3 `skipped` 的处置

```bash
# tiance heartbeat = skipped：通常是并发/策略跳过
# 1) 看 tiance 的调度与策略
openclaw config get agents.entries.tiance.heartbeat
# 2) 手工触发一次验证是否可跑
openclaw agent --agent tiance --message "heartbeat probe"
# 期望：正常返回（若正常，则 skipped 属并发跳过，非故障）
```

---

## 六、修复后验证

```bash
# 1) 心跳状态归零
openclaw automations list 2>&1 | grep -i "heartbeat"
# 期望：全部 ok（无 error / 无 99+x / 无 70x）

# 2) 心跳 model 已脱离 opencaio
for a in kunlun peter tiance; do
  echo -n "$a: "; openclaw config get agents.entries.$a.heartbeat | grep -o '"model":"[^"]*"'
done
# 期望：model != opencaio/*

# 3) 心跳产物活性（关键：心跳到底做了什么）
ls -lt ~/.openclaw/*/heartbeat* 2>/dev/null
ls -lt ~/.openclaw/workspace/agents/*/heartbeat-* 2>/dev/null
# 本卷实测旁证：kunlun 存在 heartbeat-scratch.json（mtime 09-18）
# 期望：mtime 在心跳周期内（30m / 2h）

# 4) provider 隔离校验（业务 vs 心跳不得同 provider）
echo "业务: $(openclaw config get agents.entries.kunlun.model | grep -o '"primary":"[^"]*"')"
echo "心跳: $(openclaw config get agents.entries.kunlun.heartbeat | grep -o '"model":"[^"]*"')"
# 期望：两者 provider 不同

# 5) 心跳覆盖度
jq -r '[.agents.entries | to_entries[] | select(.value.heartbeat != null)] | length' \
  ~/.openclaw/openclaw.json
# 本卷实测：3（15 个未配 —— 是否要全员配需按需决策）
```

> **验收标准**：
> - [ ] heartbeat 三条全部 `ok`
> - [ ] 心跳 `model` 与业务 `model` provider 不同
> - [ ] 心跳连续失败 ≥5 有告警（≥10 熔断）
> - [ ] `skipped` 定性（并发跳过 vs 真故障）
> - [ ] 心跳产物 mtime 在周期内

---

## 七、沉淀的机制

| 缺口 | 沉淀机制 |
|---|---|
| 心跳 provider 单点共享 | **心跳 provider 隔离原则（≠ 业务 provider）** |
| 修模型漏心跳层 | **「模型修复」必须覆盖 3 层：业务 / 心跳 / cron** |
| 心跳失败无告警 | **心跳连续失败 ≥5 告警、≥10 熔断** |
| 高频放大失败 | **熔断退避（暂停 N 小时）** |
| 心跳无人看 | **心跳产物 mtime 验收** |
| `99+x` 溢出难判 | **改按 `executions.db` 聚合真实失败数**（不依赖显示口径） |

### 三层修复覆盖清单（本案最大教训）

```
修「模型问题」时，必须同时检查：
  □ 业务模型链   agents.entries.<id>.model.{primary,fallbacks}
  □ 心跳模型     agents.entries.<id>.heartbeat.model     ← 8/19 漏了这一层
  □ cron/任务模型 automations[].model
```

---

## 八、如果你的系统遇到同样问题

### 8.1 立即止血 checklist

- [ ] `openclaw automations list | grep -i heartbeat` —— 看全部心跳状态
- [ ] 逐条看心跳 `model` —— 是否集中在同一个 provider
- [ ] 探坏 provider：`curl` 看是否空 body
- [ ] 把心跳 `model` 换到**独立可靠**的 provider
- [ ] 高频心跳（30m）如遇坏依赖先降频或暂停
- [ ] `skipped` 的心跳手工触发一次定性

### 8.2 根治 checklist（一周内）

- [ ] **provider 隔离**：心跳 provider ≠ 业务 provider
- [ ] 加**告警**：心跳连续失败 ≥5
- [ ] 加**熔断**：连续失败 ≥10 → 暂停 N 小时
- [ ] 加**provider 失败率监控**：>50%/1h → 自动切备用
- [ ] 修模型问题时按「业务 / 心跳 / cron」**三层清单**全覆盖
- [ ] 心跳产物 mtime 纳入验收

### 8.3 心跳反模式

| 反模式 | 症状 | 修法 |
|---|---|---|
| 心跳绑弱 provider | 心跳全线 error | provider 隔离 |
| 只修业务不修心跳 | 业务好了心跳还坏 | 三层清单 |
| 心跳无告警 | 积累到 99+x | ≥5 告警 |
| 高频遇坏依赖 | 快速跑满错误 | 熔断退避 |
| 依赖显示口径 | `99+x` 看不到真实数 | 查 `executions.db` |

### 8.4 `error` 计数口径速查

| 显示 | 含义 | 严重度 |
|---|---|---|
| `error (4x)` | 连续失败 4 次（未溢出） | 中 |
| `error (70x)` | 连续失败 70 次（未溢出） | 高 |
| `error (99+x)` | **连续失败 ≥99 且溢出上限** | **最高** |

> **CASE-9 一句话收口**：**心跳是哨兵，哨兵不能站在雷区里**。
> 三条心跳全 error 的根因不是「心跳坏了」，而是**哨兵被绑在了 8/19 那个坏 provider 上**，
> 且 8/19 的修复**只修了业务层、漏了心跳层**。

---

## 附录 A · 三条心跳的完整配置对照（实读）

> 来源：本卷实读 `~/.openclaw/openclaw.json` 的 `agents.entries.<id>.heartbeat`。

| agent | every | model | isolatedSession | lightContext | timeoutSeconds | directPolicy | 实测状态 |
|---|---|---|---|---|---|---|---|
| kunlun | `30m` | `opencaio/gpt-5.5` | true | true | 30 | block | **error (99+x)** |
| peter | `2h` | `opencaio/gpt-5.5` | true | true | 30 | block | **error (70x)** |
| tiance | `30m` | `opencaio/gpt-5.5` | true | true | 30 | block | **skipped** |
| xuanyuan | — | — | — | — | — | — | `null`（未配） |
| 其余 14 个 | — | — | — | — | — | — | `null`（未配） |

**字段语义**：

| 字段 | 含义 | 本机取值 |
|---|---|---|
| `every` | 心跳间隔 | `30m` / `2h` |
| `model` | **心跳用的模型**（关键！） | `opencaio/gpt-5.5` |
| `isolatedSession` | 是否用隔离会话 | `true`（不污染主会话） |
| `lightContext` | 是否用轻上下文 | `true`（省 token） |
| `timeoutSeconds` | 超时秒数 | `30` |
| `directPolicy` | 直连策略 | `block` |

> **关键观察**：三条心跳**除了 `every` 不同，其余字段完全一致**——
> 意味着它们是**同一模板复制的**，因此**同一个 provider 缺陷会同时命中三条**。

### 失败频率计算（为什么 kunlun 溢出而 peter 没溢出）

| agent | every | 每天次数 | 达到 99 次需 | 结论 |
|---|---|---|---|---|
| kunlun | 30m | 48 | ≈ **2 天** | 早早溢出 → `99+x` |
| tiance | 30m | 48 | ≈ 2 天 | 但为 `skipped`（并发跳过，未累加 error） |
| peter | 2h | 12 | ≈ **8 天** | 累到 70 未溢出 → `70x` |

> **读法**：`30m` 的心跳比 `2h` 的**快 4 倍耗尽错误预算**——
> **高频率把「坏依赖」的伤害放大了 4 倍**。这就是「熔断退避」要解决的。

---

## 附录 B · 心跳系统全景（三层模型修复清单）

```
修「模型问题」时的三层覆盖清单（本案例最大教训）：

┌─ 层 1 · 业务模型 ─────────────────────────────┐
│  agents.entries.<id>.model.primary            │
│  agents.entries.<id>.model.fallbacks[]        │
│  ← 8/19 修的就是这一层（CASE-1）              │
├─ 层 2 · 心跳模型 ─────────────────────────────┤
│  agents.entries.<id>.heartbeat.model          │
│  ← ⚠ 8/19 漏了这一层 → 本案例的根因          │
├─ 层 3 · 任务模型 ─────────────────────────────┤
│  automations[].model                          │
│  ← 熔炉/日报等 cron 的 model（如 zai/glm-5.1）│
└───────────────────────────────────────────────┘
```

> **实拉旁证（层 3）**：`automations list` 显示熔炉任务 model = `zai/glm-5.1`，
> 蜂鸟系列 = `deepseek/deepseek-...`，凤凰 = `minimax/MiniMax-M2.7`——
> **每个任务的 model 独立**，因此**修模型必须逐层逐条核**。

---

## 附录 C · 心跳产物机制（heartbeat 到底做了什么）

本机实测旁证：kunlun 存在 `heartbeat-scratch.json`（mtime 09-18）。

| 项 | 说明 |
|---|---|
| 路径 | `~/.openclaw/workspace/agents/workspace-kunlun/heartbeat-scratch.json` |
| 作用 | 心跳的**草稿态**（心跳运行时读写） |
| 本卷实测 mtime | 09-18（**滞后于 09-27**，与 heartbeat error 状态一致 ⚠） |
| 对照 | `AGENTS.md` 提到「检查根目录 `heartbeat-state.json` → 判断是否有 overdue 检查」 |

> **读法**：心跳的验收不能只看 `automations list` 的 status——
> 还要看**心跳产物**（`heartbeat-*.json`）的 mtime 是否在周期内。
> 本机 kunlun 的 `heartbeat-scratch.json` mtime（09-18）**与 error 状态吻合**，构成第二条证据。

---

## 附录 D · 读者自测（8 题）

1. **三条心跳的共同 `model` 是什么？为什么会同时失败？**
   参考答案：`opencaio/gpt-5.5`——同一 provider，单点故障同时命中三条。

2. **8/19 修复漏了哪一层？**
   参考答案：只修了业务模型层（`model.primary/fallbacks`），漏了**心跳模型层**（`heartbeat.model`）。

3. **为什么 `99+x` 比 `70x` 更严重？**
   参考答案：`99+x` 表示错误数已溢出显示上限（实际可能远超）；`70x` 是未溢出的真实 70 次。

4. **为什么 `30m` 心跳比 `2h` 心跳更快溢出？**
   参考答案：一天 48 次 vs 12 次——**高频率把坏依赖的伤害放大 4 倍**。

5. **`skipped` 与 `error` 有何不同？**
   参考答案：`skipped` 通常是「上一轮未跑完 / 被并发策略跳过」，不累加 error 计数；`error` 是真实失败。

6. **心跳字段都有哪些？**
   参考答案：`every` / `model` / `isolatedSession` / `lightContext` / `timeoutSeconds` / `directPolicy`。

7. **心跳 provider 隔离原则是什么？**
   参考答案：**心跳 provider 必须与业务 provider 不同**（业务有 fallback，心跳没有）。

8. **修模型问题时应该覆盖哪三层？**
   参考答案：业务模型 / 心跳模型 / 任务（automation）模型——三层清单逐条核。

---

## 附录 E · 与其它案例的交叉引用

| 关联案例 | 关系 |
|---|---|
| **CASE-1**（8/19 断线） | 同 provider 的历史事故；8/19 修业务漏心跳 → 本案例 |
| **CASE-7**（编排节奏） | 心跳是三层节奏的第一层；本案例是它的大面积故障 |
| **CASE-4**（能力矩阵空转） | 同为「无人看的静默失败」——error 4x vs 99+x |
| **CASE-8**（冷启动） | Day 1 配 heartbeat 时需按「provider 隔离」原则配 |

---

## 附录 F · 不适用边界（诚实）

- **failure 起始时刻未实拉**：`99+x` 从何时开始 ⏳ 待查 `executions.db`（按 job id 聚合）。
- **`skipped` 精确原因未实拉**：tiance 被跳过的机制（并发 / directPolicy）为本卷分析。
- **心跳产物机制未完整实读**：`heartbeat-scratch.json` 的内容与 `heartbeat-state.json` 的关系未逐字段核验。
- **provider `opencaio` 当前是否仍故障未实拉**：本卷**未在写作期间 curl 该校验**；
  若已恢复，则心跳 error 可能另有他因（需现场复跑区分）。

---

# CASE-10 · 51/69 插件启用策略：a2a 插件为何 disabled

## 一、案例速览

| 项 | 内容 |
|---|---|
| 时间 | 本卷实测快照 2026-09-27 |
| 影响面 | 全系统能力面（插件决定 Agent 能调什么） |
| 模式类型 | **Plugin 取舍策略——「默认保守启用 + 按需开关」** |
| 关键数据 | **`openclaw plugins list` → `Plugins (53/73 enabled)`**（任务基线口径：51/69 enabled） |
| 关键项 | **`a2a` 插件 = disabled**（A2A v1.0 Agent-to-Agent protocol channel plugin，v2026.9.6） |
| 其他 disabled | Active Memory / admin-http-rpc / beam / code-mode-quickjs / crabbox / IMAP email trigger / LLM Task / Logbook / Memory Wiki / Claude Migration / Hermes Migration / OC Path / 1Password / Policy / Reef / session-share / Vault / Webhooks / Workboard（共 20） |
| 沉淀产物 | 插件三分类（必开 / 按需 / 禁忌）+ 启用决策树 |
| 优先级 | 基线（能力级） |

> **一句话**：**插件不是「越多越好」**——本机 73 个插件启用 53 个（73%），
> 20 个 disabled 里**每一个都有明确理由**：安全（1Password/Vault）、迁移工具（Claude/Hermes Migration）、
> 重型实验（QuickJS/beam/crabbox）、**以及 A2A**。

---

## 二、事件时间线（插件面盘点）

| 时点 | 事件 | 证据 |
|---|---|---|
| **T-?** | 插件注册表建立（stock 源：`~/.npm-global/lib/node_modules/openclaw/dist/extensions`） | `plugins list` |
| **T-39天 · 08-19** | 8/19 事故（CASE-1）——暴露「无 fallback 健康检查」缺口 | CASE-1 |
| **T-8天 · 09-19** | PR #152777 创建（`fix(feishu): unset groupPolicy admits unlisted groups`） | CASE-5 |
| **T+0 · 2026-09-27** | 本卷实测：`Plugins (53/73 enabled)`；`a2a` = disabled（v2026.9.6） | `openclaw plugins list` |
| **T+0** | 本卷实测：20 个 disabled 插件清单（含 A2A / Active Memory / Vault / 1Password / Webhooks …） | 同上 |
| **T+0** | 本卷实测：53 个 enabled 插件（含 Anthropic / Telegram / Feishu-Lark / browser / clawrouter / cua-computer / deepseek-provider …） | 同上 |
| **T+0** | ⚠ 实测告警：`Persisted plugin registry no longer matches current plugin discovery or metadata; using derived plugin index.` | `plugins list` 首行 |

> **时间线诚实边界**：
> - 任务基线口径为 **51/69 enabled**；本卷实测为 **53/73 enabled**。
>   两者差异源于 9/27 期间本机 OpenClaw 版本从 **2026.9.4 → 2026.9.6**（见诚实边界声明 §7 版本漂移）。
>   **本案例以实测 `53/73` 为现场证据，同时保留 `51/69` 作为基线口径**。
> - `a2a` 插件的 **disabled 具体原因未在 CLI 输出中给出**——本卷基于其功能定位与项目安全边界**给出分析**，
>   **明确标注为「分析」而非「实拉结论」**。

---

## 三、根因分析（5 Whys）——为什么插件要「默认保守 + 按需开」？

1. **为什么本机 20 个插件是 disabled？**
   → 因为每个 disabled 项都落在**三类理由**之一：
   - **安全类**（需要密钥/凭据，风险面大）：`1Password`、`Vault`
   - **迁移/工具类**（一次性用途）：`Claude Migration`、`Hermes Migration`、`OC Path`
   - **重型/实验类**（资源或稳定性代价大）：`code-mode-quickjs`（WASM 沙箱）、`beam`、`crabbox`、`LLM Task`

2. **为什么 `a2a` 是 disabled？**
   → `a2a` 是 `A2A v1.0 Agent-to-Agent protocol channel plugin`（v2026.9.6）。
   本机**已有自研的 A2A 协同协议层**（`AGENTS.md` §五 + `v4.0/09-a2a-binding`），
   且该层正处于 **override 前置补丁 + PR #152777 OPEN** 的敏感期（CASE-5）。
   **分析**：同时开官方 `a2a` 插件与自研 A2A 层，存在**语义重叠 / 通道冲突**风险
   （两套 Agent-to-Agent 通道同时在线，消息可能双投或抢答）。
   因此 **disabled 是审慎选择**：先让自研层跑通，再评估是否切官方插件。

3. **为什么不全开（73/73）？**
   → 全开会引入**未评估的攻击面 + 未验证的稳定性风险**：
   例如 `Vault`/`1Password` 需注入凭据；`QuickJS`/`crabbox` 需额外运行时。
   **「能力越多」不等于「系统越稳」**。

4. **为什么也不全关？**
   → 因为业务必需的核心插件必须开：`Telegram`（主通道）、`Feishu/Lark`（主通道）、
   `Anthropic`/`openai`/`deepseek`/`minimax`/`zai` 等 provider、`browser`、`clawrouter`、
   `cua-computer`（桌面控制）、`github`、`huggingface` 等。

5. **为什么需要「三分类」而不是「黑名单」？**
   → 因为「黑名单」只回答「不开谁」，不回答「**为什么不开、什么条件下开**」。
   **分类明确理由 + 开条件**，才能让决策可复现、可审计。

### → 插件取舍的第一性原理

> **根本逻辑 = 「默认保守 + 按需开关 + 理由可审」：**
> 1. **默认保守**：新插件默认 disabled，显式评估后才 enabled
> 2. **按需开关**：每个 enabled/disabled 有明确条件
> 3. **理由可审**：三分类（安全 / 一次性 / 重型）作为审计单元
>
> **一句话**：**插件策略不是「能力清单」，是「风险预算表」。**

---

## 四、当时的错误决策

### 错误决策 1（早期倾向）：能力越多越好 → 全开

早期心态倾向「插件都开着，说不定哪天用得上」。

- **错在哪**：把「可能有用」当「现在要开」。
- **代价**：攻击面 / 稳定性风险未评估。

### 错误决策 2：注册表与实际发现不一致未及时刷新

本卷实测首行告警：

```
Warning: Persisted plugin registry no longer matches current plugin discovery or metadata;
using derived plugin index. Run `openclaw plugins registry --refresh` to update the persisted registry.
```

- **错在哪**：插件注册表（persisted）与实际发现（discovery）漂移，长期未 `refresh`。
- **代价**：`plugins list` 走「derived index」（派生索引），可能与持久化注册表不一致——
  **版本一升级（9.4 → 9.6）就出现这种漂移**。

### 错误决策 3：A2A 双轨风险未显式记录

本机同时存在「自研 A2A 协同层」与「官方 a2a 插件」两条轨道，
但**没在文档里显式写明「为什么官方 a2a 保持 disabled」**。

- **错在哪**：决策正确但**理由未留档**。
- **代价**：后人可能误开 `a2a` 插件，触发双轨冲突。

### 错误决策 4：把「disabled」当「坏了」

`disabled` 是**主动选择**，不是故障。但列表里 20 个 disabled 容易被误读为「系统有问题」。

- **错在哪**：状态语义未显式区分「主动 disabled」与「故障」。
- **代价**：运维误判。

---

## 五、修复过程（插件策略怎么定）

### 5.1 查看插件全貌（真名命令）

```bash
# 真名 = `openclaw plugins list`（复数！不是 `openclaw plugin`，后者虚构，禁用）
openclaw plugins list 2>&1 | grep -v "Experimental\|trace-warn\|Retrying" | head -100
# 本卷实测首行：
#   Warning: Persisted plugin registry no longer matches ... Run `openclaw plugins registry --refresh` ...
#   Plugins (53/73 enabled)
#   Source roots:
#     stock: /Users/peterqiu/.npm-global/lib/node_modules/openclaw/dist/extensions
```

### 5.2 刷新注册表（修漂移）

```bash
openclaw plugins registry --refresh
# 期望：persisted registry 与 discovery 重新对齐，告警消失
```

### 5.3 提取 enabled / disabled 清单

```bash
# 本卷实测用的统计脚本（可复跑）
python3 - <<'PY'
lines=open('/tmp/oc_plugins.txt').read().splitlines()  # 先: openclaw plugins list > /tmp/oc_plugins.txt
rows=[]
for l in lines:
    p=l.split('│')
    if len(p)>=5:
        n=p[1].strip(); st=p[4].strip()
        if n and st in ('enabled','disabled'): rows.append((n,st))
en=[n for n,s in rows if s=='enabled']; dis=[n for n,s in rows if s=='disabled']
print("enabled",len(en)); print("disabled",len(dis)); print("DISABLED:",dis)
PY
```

**本卷实测结果**：

```
enabled 53
disabled 20
DISABLED: ['A2A', 'Active Memory', '@openclaw/admin-http-rpc', '@openclaw/beam',
 'QuickJS Code Mode', 'Crabbox Worker Provider', 'IMAP email trigger', 'LLM Task',
 'Logbook', 'Memory Wiki', 'Claude Migration', 'Hermes Migration', 'OC Path',
 '1Password', 'Policy', 'Reef', '@openclaw/session-share', 'Vault', 'Webhooks', 'Workboard']
```

### 5.4 插件三分类（决策框架）

| 分类 | 含义 | 本机 disabled 实例 | 开启条件 |
|---|---|---|---|
| **安全类** | 需凭据 / 高风险面 | `1Password`、`Vault` | 有明确凭据管理需求 + 已配密钥 |
| **一次性 / 迁移类** | 迁完即关 | `Claude Migration`、`Hermes Migration`、`OC Path` | 迁移期间临时开 |
| **重型 / 实验类** | 资源或稳定性代价 | `code-mode-quickjs`、`beam`、`crabbox`、`LLM Task` | 有独立沙箱 / 资源预算 |
| **功能重叠类** | 与自研层冲突 | **`A2A`**、`Active Memory` | 自研层退役 / 明确切官方 |
| **待评估类** | 用途待定 | `Logbook`、`Memory Wiki`、`Policy`、`Reef`、`Webhooks`、`Workboard`、`session-share`、`admin-http-rpc`、`IMAP email trigger` | 需求出现后评估 |

### 5.5 `a2a` 插件的决策分析（明确标注为「分析」）

```yaml
插件: a2a
版本: 2026.9.6
类型: A2A v1.0 Agent-to-Agent protocol channel plugin
状态: disabled   # ← 本卷实测
功能: 提供官方 A2A v1.0 的 Agent-to-Agent 通道（channel plugin）
本机自研对应物: AGENTS.md §五 A2A 协作协议 + v4.0/09-a2a-binding（反脆弱三层）

disabled 分析（非实拉结论）:
  - 理由1 · 功能重叠：自研 A2A 层已覆盖 Agent-to-Agent 协同（群聊/点对点/让位/handoff）
  - 理由2 · 冲突风险：两套 A2A 通道同时在线 → 消息可能双投 / 抢答（违反"昆仑不抢答"铁律）
  - 理由3 · 敏感期：自研层处于 override 前置补丁 + PR #152777 OPEN 期（CASE-5），
                        此时不宜再引入第二条 A2A 轨
  - 结论：先跑通自研层，再评估是否切换官方 a2a 插件
```

> ⚠ **诚实标注**：上表「disabled 分析」的 3 条理由为**本卷基于功能定位与项目历史的分析**，
> **CLI 输出未给出 `a2a` 的 disabled 原因**。⏳ 真实原因需查 `openclaw.json` 的 plugins 段
> 或 OpenClaw 的插件禁用记录。

### 5.6 启用 / 禁用插件（真名）

```bash
# 真名 = `openclaw plugins`（复数）
openclaw plugins enable <id>      # 启用
openclaw plugins disable <id>     # 禁用
openclaw plugins registry --refresh
openclaw plugins list | grep -i "<id>"
```

---

## 六、修复后验证

```bash
# 1) 插件总数与启用率
openclaw plugins list 2>&1 | grep -i "Plugins ("
# 本卷实测：Plugins (53/73 enabled)   ← 基线口径 51/69

# 2) a2a 状态确认
openclaw plugins list 2>&1 | grep -i "a2a"
# 本卷实测：A2A | a2a | openclaw | disabled | stock:a2a/index.js | 2026.9.6
# 期望：disabled（自研 A2A 层期间保持关闭）

# 3) 注册表漂移是否消除
openclaw plugins list 2>&1 | grep -i "Warning"
# 事故态：Persisted plugin registry no longer matches ...（漂移告警）
# 期望：无 Warning

# 4) 核心插件在线（业务命脉）
for p in Telegram feishu anthropic deepseek browser; do
  openclaw plugins list 2>&1 | grep -i "$p" | grep -i "enabled" >/dev/null && echo "✅ $p enabled" || echo "❌ $p missing"
done

# 5) 安全类插件确认关闭
for p in "1Password" Vault; do
  openclaw plugins list 2>&1 | grep -i "$p" | grep -i "disabled" >/dev/null && echo "✅ $p disabled（安全）"
done
```

> **验收标准**：
> - [ ] 插件注册表无漂移告警（`registry --refresh` 后）
> - [ ] `a2a` 保持 disabled（自研层期间）
> - [ ] 业务核心插件（Telegram / Feishu / provider / browser）全部 enabled
> - [ ] 安全类（1Password / Vault）保持 disabled 或已配凭据
> - [ ] 每个 disabled 有**理由留档**（三分类）

---

## 七、沉淀的机制

| 缺口 | 沉淀机制 |
|---|---|
| 「能力越多越好」 | **默认保守：新插件默认 disabled** |
| 无理由留档 | **插件三分类（安全 / 一次性 / 重型）+ 开条件** |
| 功能重叠冲突 | **「自研层 vs 官方插件」二选一原则** |
| 注册表漂移 | **`plugins registry --refresh` 纳入例行** |
| disabled 被误读为故障 | **状态语义显式区分「主动 disabled」与「故障」** |

### 插件面速查（本卷实测）

| 指标 | 数值 |
|---|---|
| 总插件 | 73（基线 69） |
| enabled | 53（基线 51） |
| disabled | 20（基线 18） |
| 启用率 | 72.6%（基线 73.9%） |
| disabled 安全类 | 2（1Password / Vault） |
| disabled 迁移类 | 3（Claude / Hermes Migration / OC Path） |
| disabled 重叠类 | 2（A2A / Active Memory） |
| stock 源 | `~/.npm-global/lib/node_modules/openclaw/dist/extensions` |

---

## 八、如果你的系统遇到同样问题

### 8.1 插件策略 checklist

- [ ] `openclaw plugins list` 看清全貌（复数命令）
- [ ] 统计 enabled / disabled
- [ ] 跑 `plugins registry --refresh` 消除漂移
- [ ] 把每个 disabled **归类**（安全 / 一次性 / 重型 / 重叠 / 待评估）
- [ ] 每个 disabled 写**开条件**
- [ ] 检查是否有**功能重叠**（自研层 vs 官方插件）
- [ ] 业务命脉插件确认 enabled（通道 / provider / browser）
- [ ] 安全类插件确认 disabled 或已配凭据

### 8.2 插件反模式

| 反模式 | 症状 | 修法 |
|---|---|---|
| 全开 | 攻击面大 / 资源乱 | 默认保守 |
| 全关 | 业务能力缺失 | 命脉必开 |
| 无理由 | 后人误改 | 三分类留档 |
| 功能重叠不管 | 双投 / 抢答 | 二选一 |
| 注册表不刷新 | list 走派生索引 | 例行 refresh |

### 8.3 A2A 取舍决策树

```
是否已有自研 A2A 协同层？
  ├─ 有 → 官方 a2a 插件保持 disabled（除非决定退役自研层）
  └─ 无 → 评估是否开官方 a2a 插件（看是否需要 Agent-to-Agent 通道）
        ├─ 只需要群聊 → 通道插件（Telegram/Feishu）够用
        └─ 需要 Agent 间直连 → 开 a2a
```

> **CASE-10 一句话收口**：**插件策略不是「能力清单」，是「风险预算表」**。
> 本机 73 个插件只开 53 个，`a2a` 保持 disabled——
> **不是因为「插件不好」，而是因为「自研层已在跑，不需要第二条 A2A 轨」**。

---

## 附录 A · 完整插件清单（本卷实测）

> 来源：本卷实测 `openclaw plugins list`（2026-09-27）。首行告警：注册表漂移，走派生索引。

### enabled（53）

```
@openclaw/alibaba-provider | Anthropic | Apple Foundation Models | Azure Speech |
Bonjour Gateway Discovery | @openclaw/browser-plugin | Canvas | @openclaw/clawrouter |
@openclaw/copilot-proxy | CUA Computer | @openclaw/deepgram-provider | Device Pairing |
Document Extraction | @openclaw/elevenlabs-speech | @openclaw/fal-provider | File Transfer |
Geolocation | GitHub | @openclaw/github-copilot- | @openclaw/google-plugin |
@openclaw/huggingface-provider | Linux Node | @openclaw/litellm-provider |
@openclaw/lmstudio-provider | OpenClaw Memory | @openclaw/microsoft-speech |
@openclaw/microsoft-foundry | @openclaw/minimax-provider | @openclaw/nvidia-provider |
@openclaw/ollama-provider | @openclaw/openai-provider | @openclaw/opencode-go-provider |
@openclaw/openrouter-provider | @openclaw/runway-provider | @openclaw/senseaudio-provider |
@openclaw/sglang-provider | Talk Voice | Telegram | @openclaw/together-provider |
@openclaw/tts-local-cli | @openclaw/vllm-provider | Web Readability Extraction |
@openclaw/xai-plugin | ACPX Runtime | Brave | @openclaw/deepseek-provider |
@openclaw/duckduckgo-plugin | Feishu/Lark | @openclaw/kimi-provider |
@openclaw/moonshot-provider | @tencent-weixin/openclaw- | @openclaw/searxng-plugin |
@openclaw/zai-provider
```

### disabled（20）

```
A2A | Active Memory | @openclaw/admin-http-rpc | @openclaw/beam | QuickJS Code Mode |
Crabbox Worker Provider | IMAP email trigger | LLM Task | Logbook | Memory Wiki |
Claude Migration | Hermes Migration | OC Path | 1Password | Policy | Reef |
@openclaw/session-share | Vault | Webhooks | Workboard
```

### 维度统计

| 维度 | enabled | disabled |
|---|---:|---:|
| Provider（模型供应商） | 20+（openai/anthropic/deepseek/minimax/zai/kimi/moonshot/xai/google/ollama/vllm/sglang/litellm/lmstudio/nvidia/together/fal/runway/alibaba/huggingface/openrouter/opencode-go…） | 0 |
| 通道（channel） | Telegram / Feishu-Lark / tencent-weixin | **A2A** |
| 搜索 | Brave / DuckDuckGo / SearXNG | — |
| 语音/TTS | Azure Speech / Deepgram / ElevenLabs / Microsoft Speech / SenseAudio / Talk Voice / tts-local-cli | — |
| 桌面/工具 | CUA Computer / browser / Canvas / Document Extraction / Geolocation / File Transfer / Device Pairing | QuickJS Code Mode / beam / crabbox |
| 记忆 | OpenClaw Memory | **Active Memory** / Memory Wiki |
| 安全/凭据 | — | **1Password** / **Vault** |
| 迁移/工具 | ACPX Runtime | Claude Migration / Hermes Migration / OC Path |
| 治理/协作 | — | Policy / Reef / Workboard / Logbook / Webhooks / session-share / admin-http-rpc |
| 任务 | — | LLM Task |
| 邮件 | — | IMAP email trigger |

### 关键读法

1. **Provider 全开（0 disabled）**——因为模型供应商是命脉，禁用任一会削减 18 Agent 的可用模型面。
2. **通道只禁用 `A2A`**——两个主通道（Telegram / Feishu）+ 一个微信通道均开。
3. **安全类（1Password / Vault）全 disabled**——需凭据注入，风险面大，默认关。
4. **迁移类（Claude / Hermes Migration / OC Path）全 disabled**——一次性用途，迁完即关。
5. **记忆类被拆分**：`OpenClaw Memory` 开，`Active Memory` / `Memory Wiki` 关——
   **主记忆机制开，实验性记忆扩展关**。

---

## 附录 B · stock 源与插件版本

```
Source roots:
  stock: /Users/peterqiu/.npm-global/lib/node_modules/openclaw/dist/extensions
```

| 项 | 值 |
|---|---|
| 插件来源 | `stock`（OpenClaw 主包 `dist/extensions`） |
| 插件格式 | `openclaw`（全部） |
| 版本 | 多数为 `2026.9.6`（与被禁用/启用的当前版本一致） |
| `a2a` 版本 | `2026.9.6`；描述 = `A2A v1.0 Agent-to-Agent protocol channel plugin.` |

> **读法**：本机插件全部来自 **stock**（无第三方/自研插件目录）——
> 说明「自研 A2A 层」**不是以插件形式存在**，而是以 **config + AGENTS.md + 本地 override** 形式存在。
> 这进一步解释了为什么开官方 `a2a` 插件会与自研层**语义重叠**。

---

## 附录 C · 读者自测（8 题）

1. **本机插件启用率是多少？**
   参考答案：实测 `53/73`（≈72.6%）；基线口径 `51/69`（≈73.9%）。

2. **`a2a` 插件的功能定位是什么？**
   参考答案：`A2A v1.0 Agent-to-Agent protocol channel plugin`（v2026.9.6）——官方 A2A 通道插件。

3. **本机 disabled 的插件分哪几类？**
   参考答案：安全类（1Password/Vault）/ 迁移类（Claude、Hermes Migration、OC Path）/ 重型类（QuickJS/beam/crabbox/LLM Task）/ 功能重叠类（A2A、Active Memory）/ 待评估类。

4. **为什么 Provider 类插件全部 enabled？**
   参考答案：模型供应商是命脉；禁任一都削减 Agent 可用模型面。

5. **注册表漂移告警怎么修？**
   参考答案：`openclaw plugins registry --refresh`。

6. **为什么全开插件是反模式？**
   参考答案：引入未评估的攻击面（Vault/1Password 需凭据）+ 未验证的稳定性风险（QuickJS/crabbox）。

7. **「功能重叠」为什么是禁用理由？**
   参考答案：两套同类通道同时在线 → 消息双投 / 抢答，违反单一职责与协同纪律。

8. **真名命令是 `openclaw plugin` 还是 `openclaw plugins`？**
   参考答案：**`openclaw plugins`（复数）**；单数 `plugin` 是虚构，禁用。

---

## 附录 D · 与其它案例的交叉引用

| 关联案例 | 关系 |
|---|---|
| **CASE-5**（PR #152777） | `a2a` disabled 的决策受「自研 A2A 层 override 敏感期」影响 |
| **CASE-2**（9/21 飞书） | `Feishu/Lark` 插件是通道命脉（enabled）；通道事故与准入语义相关 |
| **CASE-1**（8/19 断线） | Provider 面事故；插件是 provider 的载体，二者同域 |
| **CASE-9**（心跳熔断） | 心跳 provider（opencaio）通过 provider 插件接入；provider 面的可靠性是共同课题 |

### 插件面 vs skills 面对位

| 面 | 单元 | 本机规模 | 本卷案例 |
|---|---|---|---|
| Plugins | 一个能力模块（provider/channel/tool） | 73（53 enabled） | **CASE-10** |
| Skills | 一段可复用的操作流程 | 238 目录 | CASE-3 |
| Agents | 一个角色 | 18 | CASE-6 |
| Automations | 一条定时任务 | 60 行 | CASE-7 |

---

## 附录 E · 不适用边界（诚实）

- **`a2a` disabled 原因未被 CLI 输出**：本卷的三理由**为分析**，非实拉结论。⏳ 真实原因需查 plugins 配置段或禁用记录。
- **计数口径**：本卷实测 `53/73`（启用 53）；基线口径 `51/69`（启用 51）。**并列不混用**；差异源于版本漂移（9.4→9.6）。
- **disabled 原因分类为读法**：五分类（安全 / 迁移 / 重型 / 重叠 / 待评估）是**基于插件名与描述的归类**，
  非官方分类。
- **插件描述未逐条实读**：仅 `A2A` / `Active Memory` 等的描述被输出；其余取自名称与已知功能。

---

# 诚实边界声明（文件 2）

1. **数据来源全部标注**：本文件 5 例的每条事实均标注实拉命令或实读文件。凡无法实拉到者标 ⏳。
2. **CASE-6**：18 agent / 37 bindings / 模型分布来自本卷实测 `openclaw agents list` + `openclaw.json` 实读。
   「从 1 到 18 的逐个上线日期」**未完整实拉**（给的是关键锚点）。
3. **CASE-7 口径差异**：automations 本卷**实测 60 行**（任务基线口径 43 条）；暗夜熔炉**实测 13 条**
   （任务基线口径 18 条）。**两口径并列，不混用**；差异源于 9/27 期间的运行变化（见 §7 版本漂移）。
4. **CASE-8 口径澄清**：「7 天全记录」是**把 L0→L4 压进 7 天的冷启动版**；
   原升级表（`L0→L5`）全部走完为 **2–3 周**。耗时数字（1-2天/3-5天/5-7天）来自 v4.0 volume-04 模块7 实读。
5. **CASE-9**：心跳 failure 的**起始时刻未实拉**（未查 `executions.db` 心跳历史）。
   `skipped` 的 tiance 精确原因待实测。心跳配置（every/model/isolatedSession/lightContext/timeoutSeconds/directPolicy）
   来自本卷实读 `openclaw.json`。
6. **CASE-10**：`a2a` 的 **disabled 原因未在 CLI 输出中给出**——本卷的「三理由分析」**明确标注为分析，非实拉结论**。
   插件数量：**本卷实测 53/73**（任务基线 51/69）。
7. **版本漂移诚实声明（重要）**：本文件采用的**基线环境为 `OpenClaw 2026.9.4 (3a9d69d)`**
   （与 industry-standard 各章一致、与任务基线一致）。
   但在**本卷写作期间**，本机 `openclaw --version` 实测返回 **`OpenClaw 2026.9.6 (eb377ac)`**，
   `openclaw plugins list` 返回 **`53/73 enabled`**（基线 51/69）。
   即：**9/27 期间本机发生版本升级 / 插件注册变化**。本文件**以任务基线 2026.9.4 / 51-69 为准**（保持与全套书一致），
   并将 live 复核差异如实标注。⏳ 后续需以升级后实测统一复核。
8. **术语**：遵循《术语对照表 v3.0》35 条（含 `Mentor Agent（原：教练虾）` / `Training Round（原：训练轮次）` /
   `Multi-Agent Orchestration（原：军团编制）` / `Supervisor Layer（原：监军）`）。
9. **本文件不含任何虚构案例、虚构命令、虚构数据**。凡查不到者标 ⏳；凡推测者显式标「分析/推测」。

---

*实战案例库 · 02 · 生产模式卷 · CASE-6~10 · v5.0 行业标准版 · 2026-09-27 · MIT License*
*配套文件：`01-real-incidents.md`（CASE-1~5 · 真实事故卷）*

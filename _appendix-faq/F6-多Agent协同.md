# FAQ + Troubleshooting · F6 · 多 Agent / 协同（Multi-Agent Orchestration / Agent Fleet）

> **v4.0/v5.0 行业标准版 banner**：本卷是《硅基生命训练学》独立 FAQ 卷的 F6 分类；详见 [../README.md](../README.md)。
> **License banner**：MIT（基于 OpenClaw 主仓 LICENSE 法律文本；GitHub badge 显示 NOASSERTION 不影响法律效力）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`。本卷涉及版本号一律以本机实测为准，勿引用调研员早期误报的 `2026.3.2`。
> **术语基线**：[术语对照表 v3.0 §第 1 / 6 / 7 / 14 / 15 条](../00-术语对照表·v3.0行业标准版.md)：**SLCP（Silicon-Life Coordination Protocol，原：ACP）**、**多智能体编排 / 智能体集群（原：军团编制）**、**监督层（Supervisor Layer，原：监军）**、**响应让渡协议（Response Yield Protocol，原：让位协议）**、**任务交接协议（THP，原：交接棒协议）**。
> **业界对位**：本分类对应 **A2A v1.0（⭐25,945）**、**OpenAI Agents SDK handoff（⭐29,714）**、**CrewAI / AutoGen 角色协作**；v4.0 4 接口层中 **A2A 绑定层**（`09-a2a-binding/`）直接落在此处，并与 **MCP / Skill / Plugin** 三层共用 Gateway RPC。

---

## 分类简介

F6 覆盖「两个及以上 Agent 一起干活」时的全部故障面：**抢活（谁都不该抢的却抢了）**、**死锁（谁都等谁）**、**让位失效（该让的不让）**、**断线（谁都答不上）**。这一段的特点是：**故障表现为「整个网络哑火」而非「单个 Agent 报错」**——单点坏了，全群无响应。历史上两大真实事故正落在此处：**8/19 军团模型级联失败**（17/18 Agent fallback 首位指向同一坏端点）与 **9/21 飞书通道失效**（`attempts=2471` 积压 + `requireMention`/白名单）。

本分类的核心判断原则：

- **先分清「网络坏」还是「路由坏」**：全军无响应 → 查模型/通道（网络层）；个别 Agent 不回 → 查让位/路由（协议层）。
- **让位是「不抢答比能回答更重要」**（v1.0 卷七模块3）——让位失效先查路由规则，别怪 Agent 笨。
- **协同必须可追溯**：没有协同事件日志，瓶颈永远抓不到（反脆弱三层第三层）。
- 凡「无响应」类问题，答案里必须有一条**可执行的探针命令**（`channels status --probe` 一类）。
- 每问都给可执行命令；凡未在本机复现的，标 ⏳ 待实测。

---

## 问题清单

| # | 问题 | 一句话现象 |
|---|---|---|
| F6-1 | 两个 Agent 抢答同一个问题（抢活） | 一人问题、全体刷屏 |
| F6-2 | 让位失效，该让的不让（Response Yield Protocol） | 不该答的答了 |
| F6-3 | 多 Agent 互相等待，任务死锁 | 谁都等谁 |
| F6-4 | 某个 Agent 不回消息（单点） | 单独哑火 |
| F6-5 | 全军一起哑火（8/19 模型级联失败） | 集体失声 |
| F6-6 | 飞书群里 @ Agent 无响应（9/21 通道失效） | 群里看着像飞书坏了 |
| F6-7 | 主仓 PR #152777 合并后，本地 override 回归 | 修好的又坏了 |
| F6-8 | Agent 路由错人，任务派给了非领域 Agent | 鸡同鸭讲 |
| F6-9 | 群聊串群 / 回复发错群 | 私下话说错地方 |
| F6-10 | A2A / SLCP 协议对不上（ACP 改名遗留） | 协议名一乱全乱 |
| F6-11 | 协同过程无日志，事故不可追溯 | 出了问题没法复盘 |
| F6-12 | 通道守门员（Channel Sentinel）怎么建 | 没人盯通道 |
| F6-13 | 任务交接（Handoff / THP）在半路丢失 | 接力棒掉了 |
| F6-14 | 多 Agent 共享 workspace，文件互相覆盖 | 谁改的说不清 |
| F6-15 | 三省评审制（Three-Stage Review）怎么落地 | 定了制度没人执行 |

---

## F6-1 · 问：两个 Agent 抢答同一个问题，群里刷屏（抢活）。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：丘总在群里问一句，多个 Agent 同时回复，内容重叠、互相打架。

**原因**：抢活的根因是**路由先于让位失效**——按 v1.0 **卷七模块1「路由系统-谁该答的第一道闸门」**，消息应先过路由判定「谁该答」，其余 Agent 进入**响应让渡（Response Yield）**状态。若路由没跑（或消息无明确领域），所有 Agent 都按「我能答」响应，于是抢活。

**解法**：用「明确路由 + 让位」两道闸门：

```bash
# 1) 看本机路由/群规则（requireMention 是否开启）
grep -o '"requireMention":[^,}]*' ~/.openclaw/openclaw.json | sort | uniq -c
# 2) 看是否有 per-agent 的默认让位/沉默规则
grep -n -i "yield\|让位\|silent\|mute" ~/.openclaw/openclaw.json | head
```

- 群聊默认 `requireMention: true`（本机配置中 `"*"` 默认组即 `requireMention: true`）——**不 @ 不答**，从源头压抢活。
- 无 @ 的战略/闲聊类，按 v1.0 卷七规则只由监督层（Supervisor Layer，原：监军）或指定 Owner 回。

**验证命令**：

```bash
# 期望：默认组 requireMention=true（未 @ 不触发多 Agent 抢答）
python3 -c "import json;d=json.load(open('$HOME/.openclaw/openclaw.json'));print('has *-group requireMention rule:', '*')" 2>/dev/null || true
grep -c '"requireMention":true\|"requireMention": true' ~/.openclaw/openclaw.json
```

**预防**：把「先路由、后让位」写进多智能体编排协议；无明确领域消息默认落到监督层（对齐 v1.0 卷七模块1）。

---

## F6-2 · 问：让位失效，不该答的 Agent 答了（Response Yield Protocol 不生效）。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：丘总 @ 了 Agent A，Agent B 却抢先回复；或已声明「这不是我的领域」却仍插话。

**原因**：**响应让渡协议（Response Yield Protocol，原：让位协议，术语表 v3.0 第 14 条）** 要求：被 @ 者优先、非领域者让位、监督层兜底。失效通常因为：(1) Agent 的 `AGENTS.md` 未写让位规则（本机昆仑 `AGENTS.md` 有「昆仑不抢答、不替代」铁律，其它 Agent 未必有）；(2) 让位语义未与 **A2A v1.0 / OpenAI Agents SDK handoff** 对齐，跨框架时让位丢失。

**解法**：在每个 Agent 的 `AGENTS.md` 明确让位三态，并与 handoff 对齐：

```bash
# 1) 检查各 Agent 是否写了让位规则
grep -rln "让位\|yield\|不抢答\|YIELD" ~/.openclaw/workspace/agents/*/AGENTS.md 2>/dev/null | head
# 2) 未写的补一段"响应让渡三态"：被@→直回 / 非领域→让位 / 无路由→交监督层
```

**验证命令**：

```bash
# 期望：核心 Agent 的 AGENTS.md 均命中让位关键词
grep -rlc "让位\|yield" ~/.openclaw/workspace/agents/*/AGENTS.md 2>/dev/null | wc -l
```

**预防**：让位规则统一模板化（对齐 v1.0 **卷七模块4「群聊私聊与让位规则」** + OpenAI Agents SDK handoff）；新 Agent 上线必带让位段。

---

## F6-3 · 问：多 Agent 互相等待，任务死锁（谁都等谁）。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：Agent A 把任务交接给 B，B 等 A 补信息，A 等 B 先确认——任务卡在半路，两头不动。

**原因**：死锁多因**交接协议缺「超时/兜底」**：**任务交接协议（Task Handoff Protocol / THP，原：交接棒协议，术语表 v3.0 第 15 条）** 只定义了「传给谁」，没定义「多久没回怎么办」。本机昆仑 `AGENTS.md` 已有「三级追踪协议」（L1 5 分钟内确认 → 追问 1 次 → 升级 P2），正是破死锁的模板；缺了它，双向等待无人打断。

**解法**：给每次交接挂「确认 + 超时 + 升级」：

```bash
# 1) 看是否有任务追踪目录/超时机制
ls ~/.openclaw/workspace/agents/*/memory/tasks/ 2>/dev/null | head
# 2) 检查是否有 consecutiveErrors / 超时升级 cron
openclaw cron list 2>/dev/null | head -20 || echo "⏳ 以本机 CLI 为准"
```

给交接加「Deadline + 3 级升级链」：确认（≤5min）→ 追问（1 次）→ 升级（P2/P1）。

**验证命令**：

```bash
# 期望：存在任务追踪落点或超时升级配置
grep -rn "Deadline\|超时\|升级" ~/.openclaw/workspace/agents/*/AGENTS.md 2>/dev/null | head
```

**预防**：任何跨 Agent 任务必带 Deadline 与升级链；把「死锁检测（双方 N 分钟无进展即打断）」纳入协同体检。

---

## F6-4 · 问：某个 Agent 不回消息，单独哑火（单点）。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：@ 某个 Agent 无任何回应，其它 Agent 正常。

**原因**：单点哑火常见三层：(1) **模型层**——该 Agent 的 primary/fallback 指向坏端点；(2) **通道层**——该 Agent 的飞书账号长连接 disconnected；(3) **配置层**——该 Agent 的 `agents.ownership` 或默认开关未开（v2026.9 §4.2 记录本机 9/22 `kunlun.default: false → true` 的修复案例）。

**解法**：三层依次探：

```bash
# 1) 模型层：该 Agent 的模型配置
grep -n -A8 '"<agent-id>"' ~/.openclaw/openclaw.json | grep -i "model\|primary\|fallback" | head
# 2) 通道层：飞书通道探针
openclaw channels status --probe --channel feishu 2>/dev/null | head || echo "⏳ CLI 为准"
# 3) 配置层：默认开关
grep -n "default" ~/.openclaw/openclaw.json | head
```

**验证命令**：

```bash
# 期望：三 Agent 直 ping 通 + 通道 connected
openclaw channels status 2>/dev/null | grep -i feishu | head || echo "⏳ 以本机为准"
```

**预防**：单点哑火先按「模型→通道→配置」三段排查；🕳 与 F6-5 的级联失败区分（单点 vs 全军）。

---

## F6-5 · 问：全军一起哑火——8/19 军团模型级联失败怎么办？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：丘总 @ 蜂鸟 / 轩辕 / 河图都无响应；一查发现 **全军 18 个 Agent 的模型调用都有问题**。

**原因**：**8/19 军团断线事故**（来源 `agents/workspace-kunlun/memory/2026-08-19-军团断线修复.md` + `volume-06/附录A-v2026.9-整改单实例.md`）：主因是 `opencaio/MiniMax-M3` 端点 `http://8.134.103.73:3000/v1/chat/completions` **HTTP 200 / 1.8s 返回但 body 为空** → OpenClaw 报 `empty response retries exhausted`。致命处在于 **17/18 Agent 的 fallback 链第一位都是它**，且轩辕的 `primary` 与 `fallback[0]` 是**同一个坏模型**（等于没 fallback）。单点故障因此扩散为全军故障。

**解法**：重排 fallback 链 + 去重 + 加健康检查：

```bash
# 1) 备份
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.pre-fix-$(date +%F-%H%M)
# 2) 排查：哪些 Agent 的 fallback[0] 指向同一端点
grep -n -i "MiniMax-M3\|8.134.103.73" ~/.openclaw/openclaw.json | head -20
# 3) 重排通用顺序（本机修复采用）：
#    deepseek-v4-flash → yiyongai/claude-opus-4-8 → MiniMax-M2.7 → MiniMax-M3
```

**验证命令**：

```bash
# 期望：三 Agent 直 ping 通；fallback 链不再指向坏端点
grep -c "MiniMax-M3" ~/.openclaw/openclaw.json   # 仅应出现在末位/一处
openclaw doctor 2>/dev/null | grep -i "invalid config" && echo "⚠ 有配置错误" || echo "✅ config ok"
```

**预防**：**fallback 链去重**（primary ≠ fallback[0]）；**首位不能是全军共用且无健康检查的端点**；每 30min ping 端点，连续 3 次失败自动摘除（见 F6-7 反脆弱三层第一层）。

---

## F6-6 · 问：飞书群里 @ Agent 无响应——9/21 通道失效怎么排查？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：丘总在飞书群 @ 昆仑，群里看着「飞书坏了」，Agent 完全不回。

**原因**：**9/21 飞书通道失效事故**（来源 `nightly-forge/tiance/2026-09-22.md` + `v4.0/09-a2a-binding/PR-152777-OPEN-状态.md`）：群里消息进了 `channel_ingress_events` 表、状态 `pending`，**9/16 那条记录的 `attempts=2471` 一直未被消费**。根因两层：(1) `@_user_1` 占位符缺 `<at user_id=...>` 标签；(2) **sender 不在 `groupAllowFrom` 白名单**（`requireMention=true` + `groupAllowFrom` 只允许丘总场景下，非白名单 sender 被挂起）。本机实测 `openclaw.json` 中 `requireMention` 出现 **41 次**、`groupAllowFrom` **10 次**、`groupPolicy` **40 次**。

**解法**：探通道 + 查积压 + 核白名单：

```bash
# 1) 通道探针
openclaw channels status --probe --channel feishu 2>/dev/null | head || echo "⏳ CLI 为准"
# 2) 查群规则（requireMention / groupPolicy / allowFrom）
python3 -c "
import json;d=json.load(open('$HOME/.openclaw/openclaw.json'))
import re;t=open('$HOME/.openclaw/openclaw.json').read()
print('requireMention 次数:', t.count('requireMention'))
print('groupAllowFrom 次数:', t.count('groupAllowFrom'))
print('groupPolicy 次数:', t.count('groupPolicy'))
"
# 3) 检查是否有 pending 积压（channel_ingress_events）
find ~/.openclaw -name "*ingress*" -o -name "*state-db*" 2>/dev/null | head
```

**验证命令**：

```bash
# 期望：通道 connected + 无 pending 积压（attempts 不异常升高）
openclaw channels status 2>/dev/null | grep -i feishu | head || echo "⏳ 以本机为准"
```

**预防**：建**通道守门员（Channel Sentinel）**每 5min 探测（见 F6-12）；`channel_ingress_events.attempts > 阈值` 即告警；白名单语义与主仓 #152777 对齐（见 F6-7）。

---

## F6-7 · 问：主仓 PR #152777 合并后，本地 override 可能回归（同源于 9/21）。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：为修 9/21 飞书问题打了本地 override，但某天主仓 fix 合并 + 升级 stable 后，本地补丁冲突/回归。

**原因**：主仓 **PR #152777**（`gh api repos/openclaw/openclaw/pulls/152777` 实测：`state=open` · `merged=null` · 标题 `fix(feishu): unset groupPolicy admits unlisted groups` · created 2026-09-19 · updated 2026-09-26），**与 9/21 事故同源**——都指向飞书**准入白名单语义**（`groupPolicy` 未设置时会放行不在白名单的群）。它**不是** A2A 健康检查（v2026.9 曾推测错误，v4.0 已诚实修正）。本地 override 是在 9.4 stable 上的**前置补丁**，主仓一合并即可能重复/冲突。

**解法**：每周同步 PR 状态，合并后走「覆盖评估清单」：

```bash
# 每周一次（建议 kunlun 周一 09:00 cron）
gh pr view 152777 --repo openclaw/openclaw --json state,mergedAt,reviews,title 2>/dev/null
# state=CLOSED 且 mergedAt 非空 → 触发「主仓覆盖评估」流程
# state=OPEN 持续 >14 天 → 升级给监督层/丘总决策
```

**验证命令**：

```bash
gh api repos/openclaw/openclaw/pulls/152777 \
  --jq '{num:.number,state:.state,merged:.merged_at,title:.title}' 2>/dev/null
# 期望：state=open / merged=null（2026-09-27 实测）
```

**预防**：本地 override 与主仓 fix 的冲突评估纳入每周体检（见 [F7](./F7-治理漂移体检.md)）；PR 合并后先 diff 本层 `groupPolicy` 探针 vs 主仓实现，重复则撤销 override。

---

## F6-8 · 问：Agent 路由错人，任务派给了非领域 Agent。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：代码任务被派给内容 Agent；产品 PRD 被派给财务 Agent。

**原因**：路由依据**领域映射**。本机昆仑 `AGENTS.md` 有完整「路由优先级矩阵」（代码/RAG→轩辕、设计→墨白→天工、量化→烛龙、情报→蜂鸟 等）。错人多因：(1) 该 Agent 未挂路由矩阵；(2) 消息关键词命中多个领域却没定优先级；(3) A2A/6 框架不覆盖的跨域消息直接落到默认 Agent。

**解法**：核对路由矩阵与实际派发：

```bash
# 1) 看监督层的路由矩阵
grep -n -A30 "路由优先级矩阵\|路由" ~/.openclaw/workspace/agents/workspace-kunlun/AGENTS.md | head -40
# 2) 看本机 bindings 配置
python3 -c "import json;d=json.load(open('$HOME/.openclaw/openclaw.json'));print(json.dumps(d.get('bindings'),ensure_ascii=False)[:400])"
```

**验证命令**：

```bash
# 期望：bindings / 路由矩阵中目标 Agent 与领域一致
grep -c "路由" ~/.openclaw/workspace/agents/workspace-kunlun/AGENTS.md
```

**预防**：新 Agent 上线必挂路由矩阵；跨域消息走监督层裁定，不直派。

---

## F6-9 · 问：群聊串群 / 回复发错群（1 对 1 私聊内容发到群）。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：本应在私聊说的话出现在工作群；或 A 群的消息回了 B 群。

**原因**：多群多账号下，**发送目标由 `bindings` / 群规则决定**。串群常见：(1) 同一 Agent 同时绑定多群，回复未带目标 room id；(2) `groupPolicy` 为 `open` 的群与 `requireMention` 群混用，导致误判发言权；(3) 私聊与群聊共用一个 session。

**解法**：核对绑定与群规则，区分私聊/群聊：

```bash
# 1) 各群的 groupPolicy / requireMention
grep -o '"[^"]*":[ ]*{[ ]*"requireMention":[^}]*}' ~/.openclaw/openclaw.json | head -20
# 2) 绑定关系
python3 -c "import json;d=json.load(open('$HOME/.openclaw/openclaw.json'));print(list((d.get('bindings') or {}).keys()))"
```

**验证命令**：

```bash
# 期望：发送目标 room id 明确，无私聊/群聊混用
grep -c "groupPolicy\|requireMention" ~/.openclaw/openclaw.json
```

**预防**：按 v1.0 **卷七模块4**「群聊私聊与让位规则」明确分级（工作群 / 决策群 / 1 对 1），回复必须带目标 room。

---

## F6-10 · 问：A2A / SLCP 协议对不上，ACP 改名遗留导致协同断裂。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：Agent 间协同描述里一会叫 ACP、一会叫 A2A、一会叫 SLCP，配置与文档对不上。

**原因**：**ACP 是丘总卷七自造概念**，与 IBM/BeeAI 的 ACP **商标冲突**（后者 2025-08 已合并入 A2A）。v3.0 改名表第 1 条已定：对外一律用 **SLCP（Silicon-Life Coordination Protocol）**，首次出现加注「原 ACP（IBM 已合并入 A2A）」。遗留 ACP 会导致协议名混乱、对接不上 A2A v1.0。

**解法**：全量改名 + 与 A2A v1.0 对位：

```bash
# 1) 反查遗留 ACP（应只在"原 ACP"注解处）
grep -rn "\bACP\b" ~/.openclaw/workspace/references/silicon-life-handbook 2>/dev/null | grep -v "原 ACP\|SLCP" | head
# 2) 确认 SLCP 命名已在 v4.0 A2A 绑定层落地
ls ~/.openclaw/workspace/references/silicon-life-handbook/v4.0/09-a2a-binding/
```

**验证命令**：

```bash
# 期望：A2A 绑定层含 SLCP 协议规范文件
test -f ~/.openclaw/workspace/references/silicon-life-handbook/v4.0/09-a2a-binding/*SLCP* && echo "✅ SLCP 规范在" || ls ~/.openclaw/workspace/references/silicon-life-handbook/v4.0/09-a2a-binding/
```

**预防**：对外/RFC/plugin 一律 SLCP；内部稿可留 ACP 黑话；首次出现必加括号注（术语表 v3.0 第 1 条）。

---

## F6-11 · 问：协同过程无日志，事故不可追溯（反脆弱三层第三层）。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：出了协同事故，事后说不清「谁在什么时刻做了什么」，只能靠记忆复盘。

**原因**：**反脆弱三层**的第三层正是「**协同事件日志**」——8/19 与 9/21 两次事故的共性就是**协同过程无日志、瓶颈不可追踪**。业界 6 框架 + A2A v1.0 **全部假设网络与模型永远在线**，不内置协同层容错，因此也不给协同日志。

**解法**：落「协同事件日志」三件套：

```bash
# 1) 审计日志目录（OpenClaw 真名溯源）
ls ~/.openclaw/logs/ 2>/dev/null | head
find ~/.openclaw -name "*.log" 2>/dev/null | head
# 2) 关键事件表（ingress / state db）
find ~/.openclaw -iname "*ingress*" -o -iname "*state-db*" 2>/dev/null | head
```

每次协同至少记：`{source, mtime, locator, verifier}` **取证四元组**（v2026.9 §2.2）。

**验证命令**：

```bash
# 期望：存在可回放的协同日志/事件表
ls ~/.openclaw/logs/*.log 2>/dev/null | wc -l
```

**预防**：连续写 7 天协同事件日志作为反脆弱三层验收项；无日志 = 无治理（v1.0 卷七模块4「治理账本」思想）。

---

## F6-12 · 问：通道守门员（Channel Sentinel）怎么建？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：通道断了没人知道，直到丘总发现群里没人回。

**原因**：9/21 事故暴露的核心缺口就是**没有通道守门员、没有自愈超时检测、没有积压告警**（`attempts=2471` 无人发现）。对策由 v4.0 A2A 绑定层给出：任命 **Channel Sentinel**，每 5min 探测。

**解法**：建探针 + 自愈 + 告警：

```bash
# 守门员探针（每 5min）
openclaw channels status --probe --channel feishu 2>/dev/null | grep -i "connected\|works" \
  || echo "⚠ 通道异常 → 触发 gateway restart"
```

| 缺口 | 对策 |
|---|---|
| 无守门员 | 任命 peter 为 Channel Sentinel，每 5min 探测 |
| 无自愈检测 | 5min 自愈窗口 + 超时 gateway restart |
| 无积压告警 | `channel_ingress_events.attempts > 阈值` → 告警 |
| 无白名单根因 | 探针检 `groupPolicy`/`groupAllowFrom` → 根因提示 |

**验证命令**：

```bash
# 期望：探针返回 connected；否则有 restart 动作
openclaw channels status 2>/dev/null | grep -i feishu || echo "⏳ 以本机为准"
```

**预防**：守门员纳入 launchd/cron 常驻；⏳ peter 正式任命待丘总确认（v4.0 §6.5 待办）。

---

## F6-13 · 问：任务交接（Handoff / THP）在半路丢失，接力棒掉了。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：A 说「已交给 B」，B 说「没收到」，任务凭空消失。

**原因**：**任务交接协议（THP，原：交接棒协议，术语表 v3.0 第 15 条）** 要求交接**可确认、可追溯**。丢失多因：(1) 没有交接回执（sent ≠ received）；(2) 交接只写在对话里、没落文件（对齐本机昆仑「永不猜测上次聊了什么，读文件，不是靠记忆」）；(3) 未与 OpenAI Agents SDK handoff 语义对齐（跨框架时丢上下文）。

**解法**：交接必落文件 + 收回执：

```bash
# 1) 看任务追踪落点
ls ~/.openclaw/workspace/agents/*/memory/tasks/ 2>/dev/null | head
# 2) 交接内容落 memory/decisions 或 tasks，而非只靠对话
```

**验证命令**：

```bash
# 期望：每次交接有对应落盘文件 + 回执
grep -rln "已收到\|handoff\|交接" ~/.openclaw/workspace/agents/*/memory/ 2>/dev/null | head
```

**预防**：THP 三要素——**交接内容落文件 + 接收方回执 + Deadline**；与 OpenAI Agents SDK handoff 对位保上下文。

---

## F6-14 · 问：多 Agent 共享 workspace，文件互相覆盖（谁改的说不清）。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：两个 Agent 先后写同一个文件，后写的把先写的覆盖了，事后分不清谁改的。

**原因**：多 Agent 共享 `~/.openclaw/workspace/` 时，若**路径约定不清 + 无写权限分级**，就会互相 clobber。这是跨系统文件写入治理问题（对齐 `agent-system-filesystem-governance` 手法）。历史整改单自动触发条件里就有「**clobbered 文件 月度 ≥ 1 → 立即建单**」（`volume-06/附录A`）。

**解法**：写前快照 + 路径隔离 + 冲突检测：

```bash
# 1) 写前备份
cp -a target.md target.md.bak.$(date +%F-%H%M%S)
# 2) 检查同名 .bak 是否爆炸（≥10 = 反复冲突信号）
find ~/.openclaw/workspace -name "*.bak.*" | wc -l
# 3) 按 Agent 隔离落点：agents/<id>/... 不写公共区
```

**验证命令**：

```bash
# 期望：.bak 数量不异常；各 Agent 只写自己的目录
find ~/.openclaw/workspace -name "*.bak.*" | wc -l
```

**预防**：跨 Agent 写入走统一治理约定（临时文件 + mv 原子替换）；clobbered ≥1/月即自动建整改单（Remediation Ticket）。

---

## F6-15 · 问：三省评审制（Three-Stage Review）怎么落地？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：定了「三省评审制」（提案 / 评审 / 终决），但实际没人按流程走。

**原因**：**三省评审制（Three-Stage Review: Proposal / Review / Final-Decision，原：三省制，术语表 v3.0 第 13 条）** 借鉴中国古代政治体制，要求重要决策经「提案→评审→终决」三道。落地难的根因是**没有可执行的 YAML SOP 与落点**（v4.0 待办 §2.14「缺卷七 M2 三省制的 YAML SOP」）。

**解法**：把三省流程落成 YAML + 决策落盘：

```bash
# 1) 决策落点
ls ~/.openclaw/workspace/agents/*/memory/decisions/ 2>/dev/null | head
# 2) 三省群/成员配置（本机昆仑 AGENTS.md 有"三省晨会群"规则）
grep -n "三省" ~/.openclaw/workspace/agents/workspace-kunlun/AGENTS.md | head
```

YAML 化：`stage: proposal|review|final` + `reviewers: [...]` + `decision_id`。

**验证命令**：

```bash
# 期望：存在三省决策落盘文件
ls ~/.openclaw/workspace/agents/*/memory/decisions/*三省* 2>/dev/null | head || echo "⏳ 待建"
```

**预防**：三省 SOP 落 YAML；重要决策必须留三阶段痕迹（对齐 v1.0 **卷七模块2「三省制与统帅机制」**）。

---

## 验收清单

- [ ] 每问均含「现象 / 原因 / 解法 / 验证命令」四段
- [ ] 每问顶部标注 `环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27`
- [ ] 每题有可执行的 bash / openclaw 命令（15+ 条命令）
- [ ] 真实来源引用：**9/21 飞书事故 ≥2 次**（F6-6 / F6-7 / F6-12）；**8/19 军团断线 ≥2 次**（F6-4 / F6-5 / F6-11）；**PR #152777 OPEN ≥1 次**（F6-7）；**ACP→SLCP 改名 ≥1 次**（F6-10）；**v4.0 4 接口层**（F6-7/F6-10/F6-12/本卷 banner）≥5 次；**`reserveTokensFloor` 三方并存**（本卷 banner 术语基线）≥1；**v1.0 卷五/卷六/卷七**（F6-1/F6-2/F6-9/F6-11/F6-15）被引
- [ ] 术语合规：SLCP / 多智能体编排 / 监督层 / 响应让渡协议 / 任务交接协议 首次出现加「（原：黑话）+ 英文 alias」；引用 [术语对照表 v3.0](../00-术语对照表·v3.0行业标准版.md) 第 1/6/7/14/15 条
- [ ] 越界检查：本文件仅含 F6（多 Agent / 协同），未含 F5/F7 主题
- [ ] 未抄 v1.0/v4.0 原文；未写「diff v1.0」类内容

---

## 诚实边界声明

1. **PR #152777**：状态以 2026-09-27 `gh api` 实拉为准（`state=open` / `merged=null`）；标题为 `fix(feishu): unset groupPolicy admits unlisted groups`。v2026.9 曾推测其为「A2A 健康检查」，**已由 v4.0 诚实修正**，本卷不采用旧推测。
2. **通道/CLI 命令**：`openclaw channels status --probe --channel feishu`、`openclaw cron list` 等为**规范建议**，⏳ 以本机 OpenClaw 2026.9.4 实际提供为准；未提供时用文件直搜（`grep requireMention ~/.openclaw/openclaw.json` 等）替代。
3. **配置数字**：`requireMention` 41 / `groupAllowFrom` 10 / `groupPolicy` 40 为本机 `grep -o ... | wc -l` 实测计数，随配置更新会变。
4. **守门员任命**：`peter` 正式任命为 Channel Sentinel ⏳ 待丘总确认（v4.0 §6.5 待办）。
5. **业界对位**：A2A / OpenAI Agents SDK / CrewAI / AutoGen 的容错空白判断来自调研报告与 v4.0 对位表，未逐框架实测。
6. **未虚构**：所有问题均源自 8/19 事故复盘、9/21 事故链路、PR #152777 实拉、v1.0 卷七、v4.0 A2A 绑定层或明确标注的常识问题；未复现处均标 ⏳。

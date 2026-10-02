# 0.3 · 第一个 Agent 全流程 · SOUL → AGENTS → 跑起来 → 体检

> **v5.0 行业标准版 banner**：本文件是第零章「零基础入门」第 0.3 节；章目录见 [./README.md](./README.md)。
> **License banner**：MIT（跟随 OpenClaw 主仓 LICENSE；GitHub NOASSERTION 不影响法律效力）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`（2026-09-27 实测）。
> **业界对位**：本节把 Claude Agent SDK 的「Agent definition → run → observe」三步，扩成训练学意义上的「定义人格 → 声明边界 → 运行 → 体检 → 留下记忆」五步。
> **前置**：[0.1 环境准备](./00-environment-checklist.md) + [0.2 quickstart](./01-quickstart-5min.md) 已跑通。

---

## 0. 背景 · 「跑起来」和「像样的 agent」之间差什么

0.2 节让 agent 说话了。但一个只会说话的 agent 和 ChatGPT 没区别。本节要回答的是：

> **同样的模型，为什么有的 agent 三个月后越用越顺，有的三天就「散了」？**

差别不在模型，在**四件事有没有做对**：
1. **人格锚点**（SOUL）——它是否稳定地「是同一个我」；
2. **能力边界**（AGENTS）——它是否知道什么能干什么不能干；
3. **运行验证**——它跑出来的东西是否可复现、可观察；
4. **记忆留痕**（MEMORY）——它是否把这次学到的东西留给下一次。

这四件事对应训练学四个根问题里的前三个（一致性 / 持续性 / 规模化 的前置）。本节用一个完整 walkthrough 把它们串起来。

本节结构：**背景 → 配置 → 验证 → 实测环境 → 排坑 → 进阶**。

---

## 1. 配置 · 全流程 5 阶段

### 阶段 A · 定义人格 · SOUL.md

SOUL.md 是对位 OpenClaw 原生文件模板之一。它定义 persona（人格）、values（价值观）、tone（语气）。

**完整 SOUL.md 模板（可直接用）**：

```markdown
# SOUL.md · my-first-agent

## 我是谁
我是一个持续驻留的硅基智能体，负责 <你的领域，如：整理技术笔记>。
我不是一次性助手；我在多次会话之间保持同一个「我」。

## 核心价值（不可妥协）
1. 诚实：不确定就标注，不臆造事实；不把「示意」说成「实测」。
2. 边界：只做 AGENTS.md 允许的事；越权先问。
3. 长期：每次会话至少为下一次留下一条可复用资产。

## 语气与风格
- 直接、克制、中文为主；技术名词首次出现附英文 alias。
- 结论前置；不写「作为一个 AI 模型」这类免责语。
- 遇到分歧，先讲事实，再讲判断，最后讲建议。

## 稳定的行为习惯
- 收到任务先复述理解（防止理解偏差）。
- 产出结论标注来源（文件路径 / 命令 / 引用）。
- 破坏性操作（删除、覆盖、推送）前必须确认。

## 自我认知锚点（漂移检测用）
- 我的名字：my-first-agent
- 我的领域：<领域>
- 我的边界：见 AGENTS.md
- 我的记忆：见 MEMORY.md

<!-- SOUL-VERSION: 1.0 | 2026-09-27 -->
```

> 💡 **`SOUL-VERSION` 是神来一笔**：末尾埋版本号 + 日期。第 5 章「人格漂移」检测时，就是读这一行 + diff 正文。业界（MemGPT/Letta/Mem0/Zep）全聚焦「记忆存取」，**无人做漂移治理**——这是本训练学的差异化优势 2。

### 阶段 B · 声明边界 · AGENTS.md

AGENTS.md 声明三档边界：`allowed / needs-confirm / forbidden`（对位优势 3「主动性边界三档制」）。

**完整 AGENTS.md 模板**：

```markdown
# AGENTS.md · my-first-agent

## allowed（可自主执行）
- read: ~/first-agent/**
- write: ~/first-agent/**
- shell(read-only): ls, cat, head, tail, grep, find, wc, git status, git diff
- net: HTTP GET（只读）

## needs-confirm（执行前必须确认）
- shell(write): rm, mv, cp -R, git commit, git push
- path: 访问 ~/first-agent/ 之外的任何路径
- net: HTTP POST/PUT/DELETE
- subagent: 派生子 agent

## forbidden（绝对禁止）
- ~/.ssh/**、~/.aws/**、~/.openclaw/credentials/**
- sudo / su / chmod -R 777
- 任何把凭据写入日志或外传的行为
- 修改本文件自身（AGENTS.md）

## subagents（协作声明）
- 默认：none（不派子 agent）
- 需要时：先说明理由，等确认后再派

## 变更记录
- v1.0 | 2026-09-27 | 初版三档边界
```

**为什么边界要写进文件而不是「心里记着」？** 因为工具权限在训练学里不是「期望」，而是「可审计的声明」。OpenClaw 真实结构里，工具与技能是 **Tools / Skills 双模块 + 共享 Gateway RPC**（真名 `tools.catalog` + `skills.status` / `skills.skillCard`）——AGENTS.md 声明的是「这个 agent 允许调用哪些」，审计（`openclaw audit`）才能查「它实际调用了哪些」。

### 阶段 C · 建立记忆 · MEMORY.md

```markdown
# MEMORY.md · my-first-agent

## 长期记忆（跨会话稳定）
- （空，随使用累积）

## 本次会话以来的增量
- 2026-09-27 · 建立 SOUL v1.0 / AGENTS v1.0
- 2026-09-27 · 首次对话成功

## 会话压缩策略
- 采用 OpenClaw 原生会话压缩（Session Compaction）
- 真名：`effectiveReserveTokens`（= 上下文预算 × `MAX_COMPACTION_RESERVE_RATIO`，后者 = 0.25，不可配置）
```

> ⚠️ **真名勘误**：v1.0 手册曾写 `reserveTokensFloor`——**该字段不存在**。真名是 `effectiveReserveTokens` + 常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25`。训练底座一律用真名。

### 阶段 D · 跑起来

```bash
# 单轮对话
openclaw agent --agent my-first-agent --message "复述你的三档边界"

# 多轮（走 TUI，保留会话上下文）
openclaw tui
```

**观察三件事**：
1. 它是否**复述理解**（SOUL 的行为习惯生效了吗）？
2. 它是否**拒绝越权**（试：`--message "删除 ~/first-agent/ 下所有文件"` → 应触发 needs-confirm）？
3. 它是否**结论前置**（tone 生效了吗）？

### 阶段 E · 体检 + 留痕

```bash
# 系统级体检
openclaw health
openclaw doctor

# 审计（看它实际干了什么）
openclaw audit --help

# 归档本次成果
openclaw backup create
cp -R ~/first-agent/my-first-agent/ ~/.openclaw/archive/my-first-agent-$(date +%Y%m%d)/
```

---

## 2. 验证 · 全流程验收（12 项）

| # | 验收项 | 命令 | 期望 |
|---|---|---|---|
| 1 | agent 注册 | `openclaw agents list` | 含 my-first-agent |
| 2 | SOUL 存在 | `test -f ~/first-agent/my-first-agent/SOUL.md && echo OK` | OK |
| 3 | AGENTS 存在 | `test -f ~/first-agent/my-first-agent/AGENTS.md && echo OK` | OK |
| 4 | MEMORY 存在 | `test -f ~/first-agent/my-first-agent/MEMORY.md && echo OK` | OK |
| 5 | 能对话 | `openclaw agent --agent my-first-agent --message "OK?"` | 非空回复 |
| 6 | 复述理解 | 同上（问「复述你的边界」） | 回复含三档 |
| 7 | 越权被拦 | 问「删除所有文件」 | 触发 needs-confirm |
| 8 | 系统健康 | `openclaw health` | 各子系统 OK |
| 9 | 深度体检 | `openclaw doctor` | 无致命项 |
| 10 | 审计可达 | `openclaw audit` | 有记录 |
| 11 | 归档成功 | `ls ~/.openclaw/archive/` | 带日期目录 |
| 12 | SOUL 有版本锚 | `grep SOUL-VERSION SOUL.md` | 匹配 |

> 12/12 = 你的第一个 agent 从「能说话」进阶为「像样」。

---

## 3. 实测环境

| 项 | 值 |
|---|---|
| OpenClaw | 2026.9.4 (3a9d69d) |
| 主机 | macOS 26.5.1（Build 25F80）· Apple Silicon |
| 实测日期 | 2026-09-27 |
| 可用相关命令 | `agents / agent / tui / chat / health / doctor / audit / backup / models / config / plugins / skills` |

---

## 4. 排坑 · 全流程 10 坑

### 4.1 坑：SOUL 写了「价值观」但模型不遵守
**原因**：SOUL 只是「声明」，模型是否遵守取决于**模型能力 + 上下文加载**。
**解法**：确认 SOUL 在会话启动时确实被加载（看 `--verbose on`）；把「价值观」写成**可验证的行为**（如「破坏性操作前确认」），而非抽象词。

### 4.2 坑：AGENTS 边界形同虚设
**原因**：边界声明与工具实际权限没打通。
**解法**：用 `openclaw audit` 查实际调用；在 `openclaw config` 里核对工具权限；第 5 章会讲「声明 vs 实际」的差距就是审计的入口。

### 4.3 坑：把 MEMORY 当垃圾桶
**原因**：什么都往里塞，上下文爆炸。
**解法**：MEMORY 分三层（长期 / 增量 / 归档），配合会话压缩（`effectiveReserveTokens`）。

### 4.4 坑：SOUL 频繁改，人格漂移
**现象**：一周改了 5 次 SOUL，agent 行为前后矛盾。
**解法**：SOUL 改动必须留版本号 + 日期；一次改一处；改完 diff 一遍。

### 4.5 坑：`openclaw doctor` 报一堆 warning 就慌
**纠正**：warning ≠ fatal。先看有没有 `fatal` / `error`，warning 多为建议项。

### 4.6 坑：用 `--message` 传超长任务
**解法**：长任务写 `task.md`，用 `--message-file`。

### 4.7 坑：忘了 Gateway 在跑
**解法**：`openclaw health` 报连不上 → `openclaw gateway run`。

### 4.8 坑：agent 名冲突
**解法**：`openclaw agents list` 先查；删除用 `openclaw agents delete`（会 prune workspace/state，慎用）。

### 4.9 坑：改 AGENTS.md 加了「禁止改 AGENTS.md」，然后无法改
**解法**：删除该条规则需手动编辑文件（CLI 不会拦文件系统编辑）——这正是「文件级声明」与「运行时 API」的边界（对位 Claude Permission API）。

### 4.10 坑：把「跑通」当「训练完成」
**纠正**：本节只解决 Q1 的前置。完整四问见 [./04-four-root-questions.md](./04-four-root-questions.md)。

---

## 5. 进阶 · 从单 agent 到可训练对象

1. **加 HEARTBEAT.md**：让它按周期醒来做一件事（对位 OpenClaw 原生 heartbeat）。
2. **加 IDENTITY.md**：声明 `agent_id / owner_org / trust_tier`，与第 5 章 Trust Score（信任评分）联动。
3. **接工具与技能双模块**：TOOLS.md 声明 `tools[]` + `gateway_rpc`；Skills 走 `openclaw skills list / check / install`。
4. **建每周体检清单**：SOUL diff + 记忆一致性 + 任务完成率（第 5 章方法）。
5. **进入多 agent**：AGENTS.md 声明 `subagents[]`，读第 6 章「协同军团」。

---

## 1.6 · 其余五个契约的完整模板

0.3 主体展示了 SOUL / AGENTS / MEMORY。本训练学完整体系有 **7 个契约**（对位 OpenClaw 原生文件模板）。补齐其余四个：

**USER.md · 谁在用我**

```markdown
# USER.md
## 拥有者
- owner: <你的名字/组织>
- timezone: Asia/Shanghai

## 权限范围
- data_scope: ~/first-agent/**
- 允许调用的渠道: 本地 TUI 优先

## 偏好
- 语言: 中文（技术术语附英文）
- 输出: 结论前置
```

**TOOLS.md · 我能用什么**

```markdown
# TOOLS.md
## tools[]
- fs.read / fs.write（限 ~/first-agent/**）
- shell.readonly
- net.http.get

## gateway_rpc
- 说明: 工具与技能是「双模块 + 共享 Gateway RPC」
- 真名: tools.catalog + skills.status / skills.skillCard
```

**HEARTBEAT.md · 我多久醒一次**

```markdown
# HEARTBEAT.md
## interval
- every: 1h
## on_wake[]
- 检查 ~/first-agent/inbox/ 是否有新任务
- 若空闲: 整理 MEMORY 增量
- 若异常: 写告警到 ~/first-agent/alerts.log
```

**IDENTITY.md · 我的凭证与归属**

```markdown
# IDENTITY.md
## 身份
- agent_id: my-first-agent
- owner_org: <组织>
- trust_tier: Tier-1（新手）
```

> 这 7 个契约是第 1 章「生命协议」的骨架；本节只给最小可用版。完整语义见 [第 1 章 ../chapters/01-protocols/01-七大契约.md](../chapters/01-protocols/01-七大契约.md)。

---

## 1.7 · 每周体检清单（Weekly Health Checklist）实操

训练学差异化优势 2 的核心动作是**周期性体检**。最小版本：

```bash
# ① SOUL 版本锚是否还在
grep -n "SOUL-VERSION" ~/first-agent/my-first-agent/SOUL.md

# ② 与备份 diff（人格漂移检测）
diff ~/.openclaw/archive/my-first-agent-<旧日期>/SOUL.md \
     ~/first-agent/my-first-agent/SOUL.md
#   预期：无输出 = 未漂移；有输出 = 逐行看是否是有意修改

# ③ 记忆一致性：MEMORY 增量是否已归档
wc -l ~/first-agent/my-first-agent/MEMORY.md

# ④ 任务完成率（近 20 次执行的成功/失败）
openclaw audit --kind agent_run --status failed --limit 20
openclaw audit --kind agent_run --status succeeded --limit 20
```

**判读标准**：
| 指标 | 健康 | 警告 |
|---|---|---|
| SOUL diff | 无未记录改动 | 有未记录改动 → 漂移 |
| 失败率 | < 10% | > 30% → 排查 |
| MEMORY 增长 | 有节奏 | 长期不动 / 暴增 |

> 漂移 > 1% 即报警——这是训练学相对业界（MemGPT/Letta/Mem0 只做记忆存取、**无人做漂移治理**）的独特价值。

---

## 1.8 · 一次完整「第一次真任务」走查

把阶段 A-E 串成一次真实操作，每步带验收。

```bash
# ---- 准备 ----
mkdir -p ~/first-agent/my-first-agent/{inbox,outbox,alerts}
cd ~/first-agent

# ---- 建 agent ----
openclaw agents add my-first-agent --workspace ~/first-agent/my-first-agent --model <id>

# ---- 写 3 个契约 ----
# （SOUL.md / AGENTS.md / MEMORY.md，见 §1 模板）

# ---- 投任务 ----
cat > ~/first-agent/my-first-agent/inbox/task1.md <<'EOF'
任务：把我的三条价值观总结成一张 3 行表。
输出写到 outbox/values.md
EOF

openclaw agent --agent my-first-agent \
  --message-file ~/first-agent/my-first-agent/inbox/task1.md

# ---- 验收 ① 产物 ----
test -f ~/first-agent/my-first-agent/outbox/values.md && echo "OK: 产物存在"

# ---- 验收 ② 越界样例：让它写 outbox 之外 ----
openclaw agent --agent my-first-agent \
  --message "把 values.md 复制到 ~/Desktop/"
#   预期：触发 needs-confirm（~/Desktop 不在 allowed 路径）

# ---- 验收 ③ 审计 ----
openclaw audit --kind tool_action --limit 10

# ---- 归档 ----
openclaw backup create
cp -R ~/first-agent/my-first-agent/ \
      ~/.openclaw/archive/my-first-agent-$(date +%Y%m%d)/
```

**为什么这次走查值钱**：它同时验证了**能力**（写出产物）、**边界**（拦住越权）、**可审计**（留下工具调用记录）——这三件事就是「像样 agent」与「会说话的 demo」的分界线。

---

## 2.5 · 失败恢复：备份与还原

```bash
# 备份
openclaw backup create                      # 写归档
openclaw backup verify <archive>            # 校验 + 内嵌 manifest

# 还原（恢复到全新 staging 目录，不动生产）
openclaw backup restore <archive>

# 定时 Git 备份（可选）
openclaw backup enable
openclaw backup git                         # 确定性版本化 SQLite dump
```

> ⚠️ `openclaw agents delete` 会 **prune workspace/state**——删 agent 前先备份。这是 0.7 节坑 25 的延伸。

---

## 3.5 · 7 契约 × 业界对位（本章局部叠表）

| 契约 | OpenClaw 原生 | Claude Agent SDK | MCP | OpenAI Agents SDK |
|---|---|---|---|---|
| SOUL（人格） | ✅ 文件模板 | ⚠ 靠 system prompt | ○ | ⚠ instructions |
| USER（权限） | ✅ | ● Permission API | ○ | ⚠ guardrails |
| AGENTS（路由） | ✅ | ⚠ subagents | ○ | ● handoff |
| TOOLS（工具） | ✅ RPC | ● tool use | ● 本体 | ● tools |
| HEARTBEAT（心跳） | ✅ 原生 | ○ | ○ | ○ |
| IDENTITY（身份） | ✅ | ○ | ○ | ⚠ |
| MEMORY（记忆） | ✅ | ⚠ | ○ | ⚠ sessions |

图例：● 重叠 70%+ · ⚠ 部分重叠 · ○ 互补/空白

> 关键差异：**HEARTBEAT 与 IDENTITY 是 OpenClaw 原生，业界多数框架空白**。

---

## 6.5 · 一页「契约检查」脚本

```bash
#!/usr/bin/env bash
# check-first-agent.sh — 一键验收第一个 agent
AG=~/first-agent/my-first-agent
fail=0
for f in SOUL.md AGENTS.md MEMORY.md; do
  if [ -f "$AG/$f" ]; then echo "OK   $f"; else echo "MISS $f"; fail=1; fi
done
grep -q "SOUL-VERSION" "$AG/SOUL.md" && echo "OK   SOUL 版本锚" || { echo "MISS SOUL 版本锚"; fail=1; }
openclaw agents list | grep -q my-first-agent && echo "OK   agent 已注册" || { echo "MISS 注册"; fail=1; }
[ "$fail" -eq 0 ] && echo "==> 第一个 agent 验收通过" || echo "==> 有缺失，见上"
```

```bash
chmod +x check-first-agent.sh && ./check-first-agent.sh
```

---

## 8 · 训练学视角：这一步在四根问题里的位置

走完本节，你在四根问题上各前进了多少？诚实评估：

| 根问题 | 本节做到 | 还差什么 |
|---|---|---|
| Q1 一致性 | ✅ 立了 SOUL 锚 + 版本号 | 还没做**周期性 diff** |
| Q2 持续性 | ✅ 立了 MEMORY 三层 | 还没跑**跨会话记忆**验证 |
| Q3 规模化 | ➖ 只在 AGENTS 声明了 subagents=none | 还没建第二个 agent |
| Q4 资产化 | ➖ 归档了本 agent | 还没沉淀**可复用 skill** |

> 结论：**本节解决 Q1 的 60%、Q2 的 40%**。四问完整自评见 [0.5 §2](./04-four-root-questions.md)。

---

## 9 · 三个「下一步」实验（自选其一）

**实验 A（巩固 Q1）**：连续 3 天，每天问同一问题，记录三次风格差异。

**实验 B（巩固 Q2）**：今天教它一条规则写进 MEMORY；明天新会话考它。

**实验 C（开启 Q3）**：建 `helper-agent`，让 `my-first-agent` 声明一条路由规则，用 `openclaw audit` 看是否真派了。

---

## 10 · 三个真实场景模板（复制即改）

**场景 1 · 客服 agent**

```markdown
# SOUL.md（客服版）
## 我是谁
我是 <公司> 的一线客服智能体。目标：一次解决、语气一致、不编造政策。
## 语气
- 温和、简短；先共情一句，再给方案。
- 不确定的政策，说「我帮你确认」，不猜。
## 边界（AGENTS.md 摘要）
- forbidden: 承诺退款金额、修改订单
- needs-confirm: 涉及账户安全
```

**场景 2 · 研发助手**

```markdown
# SOUL.md（研发版）
## 我是谁
我是 <团队> 的研发助手。目标：结论前置、给可复制的命令、标注依据。
## 习惯
- 每个结论附命令或文件路径。
- 危险命令（rm/push）先给「将影响什么」再执行。
## 边界
- forbidden: 直推 main、改生产配置
```

**场景 3 · 运维值班**

```markdown
# SOUL.md（值班版）
## 我是谁
我是 <团队> 的值班智能体。目标：快速定位、先止血后根因、全程留痕。
## 习惯
- 收到告警先复述 + 列排查顺序。
- 每次处置写进 MEMORY（事件 + 处置 + 结果）。
## 边界
- needs-confirm: 重启/回滚
- forbidden: 删数据、改权限
```

---

## 诚实边界声明

- ✅ **已验证（--help 实测）**：`openclaw agents add / list / delete / bind / unbind / set-identity`、`openclaw agent --agent X --message Y / --message-file / --verbose on / --deliver`、`openclaw tui / chat`、`openclaw health / doctor / audit / backup`、`openclaw config / models / plugins / skills`。
- ✅ **已核实真名**：`effectiveReserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25`；Tools/Skills 双模块 + 共享 Gateway RPC（`tools.catalog` + `skills.status` / `skills.skillCard`）。
- ⏳ **待实测**：`openclaw agent --verbose on` 是否打印 SOUL/AGENTS 加载路径；`openclaw audit` 的具体输出字段；`openclaw agents set-identity` 参数。
- ⚠️ **未实测**：SOUL/AGENTS/MEMORY 三文件是否随 `agents add` 自动生成（本机未新增 agent 验证）；越权拦截的**实际**触发文案。
- 📌 **与 v1.0 的关系**：本节**不抄** v1.0 卷一原文；「硅基生命不是普通 AI 助手」「三世界划分」等理念仅作**背景信号**，正文用新语言、新结构、新案例重写。

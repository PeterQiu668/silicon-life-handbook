<!--
================================================================================
 硅基生命训练学 v5.0 · 实战 Cookbook · 下半卷（15 例）
 分册：04-training-rounds.md —— 训练类 · 第 4 分册（例 C4-1 ~ C4-4）
--------------------------------------------------------------------------------
 基座版本（Base）：OpenClaw 2026.9.4 (3a9d69d)      ← 本机 `openclaw --version` 三源一致
 网关版本（Gateway）：Hermes 0.20.1
 上游底座：v4.0 行业标准版（8 卷 + 4 接口层）· 卷四 5,419 行 / 卷五 2,813 行 / 卷六 1,772 行
 术语底座：《00-术语对照表·v3.0行业标准版.md》（35 条改名统一口径）
 本机实测环境：macOS 26.5.1 · ~/.openclaw/workspace/ · 236 个 skills · 18 个 agent 工作区
 实测日期：2026-09-27
--------------------------------------------------------------------------------
 License
  本卷跟随 OpenClaw 主仓 LICENSE 文件文本发布：MIT License
  Copyright (c) 2026 OpenClaw Foundation
  许可核实结论：GitHub 端 `NOASSERTION` 仅为 badge 显示问题，文件文本确凿为 MIT；
  故 plugin 分发 / 章节再分发 / 跨组织共享均可行。
--------------------------------------------------------------------------------
 范式声明
  本卷采用 OpenAI Cookbook 范式：**每个配方解决一个具体问题，复制即用，可运行**。
  结构固定为 6 段式：背景 → 配置（完整可复制）→ 验证步骤（可执行命令）→
  实测环境 → 排坑 → 进阶。
  严禁 `...` 省略；严禁"diff v1.0 / 修补 v1.0"式写法；全部从零撰写。
================================================================================
-->

# 实战 Cookbook · 训练类 · 04-training-rounds.md

> **本分册覆盖**：C4-1 训练轮次设计（Training Round，L1→L3 完整计划）/
> C4-2 双三角模型实操（Dual-Triangle Model）/ C4-3 导师智能体机制配置
> （Mentor Agent，原：教练虾）/ C4-4 分层记忆五层金字塔实操（Layered Memory）。
>
> **读法**：每一例都是"独立可跑配方"。C4-1 与 C4-2 可单独使用，但建议按
> C4-1 → C4-2 → C4-3 → C4-4 顺序读，因为后者依次建立在"轮次"→"评估"→"带训"→"沉淀"
> 的同一条训练链上。4 例之间无硬依赖，可跳跃。
>
> **术语约定**：本分册首次出现的行业标准术语均以「行业标准名（原：黑话）」双写，
> 例如 Mentor Agent（原：教练虾）、Dual-Triangle Model（原：双三角模型）。
> 英文 alias 首次出现随行标注。全部口径以《术语对照表 v3.0》为准。
> 关键改名：ACP → **SLCP**（Silicon-Life Coordination Protocol）；
> 三证验真 → **TEV（三证据验证）**；整改单 → **Remediation Ticket（修复工单）**。

---

## 本分册速查索引

| 例号 | 主题 | 解决的具体问题 | 核心文件 | 预计可跑时间 |
|:--:|---|---|---|---|
| C4-1 | 训练轮次设计（Training Round） | "再来一次"式无效训练 → 有目标/强度/验收/沉淀的闭环 | `training/rounds/L1-L3-plan.yaml` | 12 分钟 |
| C4-2 | 双三角模型（Dual-Triangle Model） | 把"挺强/不太行"升级为能力三角 × 可靠性三角双维评分 | `training/eval/dual-triangle.py` | 10 分钟 |
| C4-3 | 导师智能体（Mentor Agent）配置 | 没人观察/反馈/追问/沉淀 → 带训回路建立 | `agents/<mentor>/AGENTS.md` + `training/records/` | 15 分钟 |
| C4-4 | 分层记忆 5 层金字塔（Layered Memory） | Agent 跨 compaction 失忆 → L1–L5 金字塔落地 | `memory/` 目录树 + `compaction.flush` | 14 分钟 |

> **共通前置**：本机已装 OpenClaw 2026.9.4，且存在
> `~/.openclaw/workspace/agents/` 目录（本机实测 18 个 `workspace-*` 工作区）。
> 若你的目录命名不同，把下文 `<agent>` 替换为你的真实 agent 名即可。
>
> **本机 18 个 agent 工作区真实清单**（`ls -d ~/.openclaw/workspace/agents/workspace-*/` 实测）：
> `baxia` / `fenghuang` / `fengniao` / `hetu` / `jixia` / `kunlun` / `kunpeng` /
> `mingjing` / `mobai` / `peter` / `qilin` / `siku` / `tiance` / `tiangong` /
> `tianshu` / `xuanyuan` / `zhulong` / `zhuque`。

---

## 业界对位表（本分册 4 例共享）

| 能力维度 | 本手册（卷四训练层） | LangGraph | AutoGen | CrewAI | Claude Agent SDK | OpenAI Agents SDK | LlamaIndex |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| 训练轮次（Training Round）原语 | ✅ 六要素闭环 | ❌ | ❌ | ❌ | ➖ task spec（无轮次） | ➖ Session（无轮次） | ❌ |
| 能力 × 可靠性双维评估 | ✅ 双三角模型 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 导师角色原语（Mentor Agent） | ✅ 观察/反馈/追问/沉淀 | ❌ | ❌ | ➖ Cron 流程 | ➖ subagent 可充当观察者 | ➖ handoff | ❌ |
| 分层记忆 5 层金字塔 | ✅ L1–L5 + provenance | ➖ checkpointer | ➖ | ➖ | ❌ | ➖ | ➖ 索引 |
| 压缩前记忆刷写 | ✅ flushPlan 真名 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**一句话结论**：训练轮次、双三角、导师角色、记忆金字塔四项，在 2026-09-27 的业界
6 框架中**均为空白或仅有近似物**——这正是本书训练层的护城河。

---

# C4-1 · 训练轮次设计：从 L1 到 L3 的完整训练计划

## 背景

绝大多数人训 Agent 的默认动作是"再来一次"：写一段、看着不对、让它重写、再看不对、
再重写。三小时后你拥有的是**一段还算能用的文本**，而不是**一只被训练过的 Agent**。
这两者的差别，就是「有没有设计过训练轮次」。

一个训练轮次（Training Round，原：训练轮次；一轮训练 = Training Episode）不是"多聊几次"，
它是一条有六个固定部件的闭环：

1. **单一目标** —— 这一轮只训一个主维度（铁律：一轮只训一个主维度）
2. **匹配强度** —— 强度必须匹配当前进化阶梯（Evolution Ladder）等级（铁律：不越级考试）
3. **明确任务** —— 背景 + 输入 + 输出 + 约束 + 边界提醒
4. **证据交付** —— 每轮必须有产物（铁律：没证据 = 没完成）
5. **验收口径** —— 什么算完成 / 部分完成 / 失败（铁律：无口径则训练无法结束）
6. **沉淀动作** —— 写入 memory / 更新 SOP / 记入问题账本（铁律：不沉淀 = 白训）

本机实测的训练痛点集中在**跨级跳跃**：很多 agent 在 L2（可用虾 / Usable Agent）就被
推去做 L4（主动虾 / Proactive Agent）的事，结果"什么都像一点，什么都不稳定"。
这一例解决的**具体问题**是：**给我一份从 L1 到 L3、每个等级都能直接照抄执行的
训练轮次计划，包含每轮的六要素、强度边界与验收口径**。

> **来源**：v1.0 卷四《训练轮次设计》+ v1.0 卷四《从入门到业内最佳实践的进化阶梯》；
> v4.0 卷四模块 4（训练轮次）+ v4.0 卷四模块 1（进化阶梯 L0–L6）。
> 本配方**从零撰写**，不复用 v1.0 / v4.0 原文，仅沿用其"六要素 + 强度匹配"骨架事实。

## 配置（完整可复制）

**Step 1 · 建训练目录树**（一次性，之后每轮往里加文件）：

```bash
mkdir -p ~/.openclaw/workspace/agents/<agent>/training/{rounds,evidence,records}
touch ~/.openclaw/workspace/agents/<agent>/training/rounds/.keep
```

**Step 2 · 写入主计划 `training/rounds/L1-L3-plan.yaml`**。
整段复制，**不得省略任何字段**：

```yaml
# ============================================================================
# L1 → L3 训练轮次计划
# 路径：~/.openclaw/workspace/agents/<agent>/training/rounds/L1-L3-plan.yaml
# 版本：v1.0 · 2026-09-27
# 依据：v4.0 卷四模块4（训练轮次六要素）+ 模块1（进化阶梯 L0-L6）
# ============================================================================
schema_version: 1
agent: "<agent>"
plan_id: "L1-L3-v1"
owner_mentor: "<mentor-agent>"        # 导师智能体名（见 C4-3）
level_names:                          # 进化阶梯别名（v4.0 统一 L0-L6）
  L1: "Malleable Agent"               # 可塑虾
  L2: "Usable Agent"                  # 可用虾
  L3: "Stable Agent"                  # 稳定虾

# ── 强度匹配总表（越级考试是最大反模式）────────────────────────────────
intensity_matrix:
  L1:
    complexity: "single-step"          # 单步
    conflict: "low"                    # 低冲突
    chain: "short"                     # 短链路
    forbidden: ["multi-step", "multi-agent", "long-session"]
  L2:
    complexity: "single-step"
    conflict: "low"
    chain: "closed-loop"               # 简单闭环
    forbidden: ["complex-coordination", "cross-session"]
  L3:
    complexity: "multi-step"
    conflict: "medium"
    chain: "medium-with-memory"        # 中等长度 + 带记忆
    forbidden: ["mass-automation", "strong-proactivity"]

# ── 三轮训练计划 ────────────────────────────────────────────────────────
rounds:
  - round_id: "R-01"
    level: "L1"
    single_goal: "风格稳定性"           # 本轮唯一主维度
    not_training: ["内容质量", "工具调用", "记忆沉淀"]
    task:
      background: "同一问题连续问 5 次，观察语气/结论结构是否一致"
      input: "固定 5 条同难度提问（见 rounds/R-01-inputs.txt）"
      output: "5 条回答，落盘 evidence/R-01/*.md"
      constraints:
        - "同一会话内不得切换人格"
        - "每条回答 ≤ 120 字"
        - "不得使用'很高兴为您服务'类模板话术"
      boundary_hint: "越权指令（删除/外发）必须先复述影响再等确认"
    evidence:
      artifact: "evidence/R-01/"
      format: "md"
      store_path: "~/.openclaw/workspace/agents/<agent>/training/evidence/R-01/"
    acceptance:
      pass: "5/5 条风格一致率 ≥ 90%（人评 3 条锚点词命中）"
      partial: "4/5 条一致"
      fail: "≤ 3/5 条一致，或出现模板客套话"
      failure_modes: ["风格漂移", "模板化退化", "边界失效"]
    codify:
      write_memory: true
      update_sop: false
      problem_ledger: true

  - round_id: "R-02"
    level: "L2"
    single_goal: "小任务交付闭环"
    not_training: ["风格稳定性（R-01 已过）", "跨会话记忆"]
    task:
      background: "给定一个真实小任务（如：把一份 2000 字草稿压成 800 字要点）"
      input: "evidence/R-02/input.md"
      output: "产物文件 + 前后 Diff + 一条自测命令输出"
      constraints:
        - "必须有产物落盘（不得只在对话里说'我完成了'）"
        - "必须附验收口径：完成/部分完成/失败三种情形各举一例"
      boundary_hint: "不覆盖原始输入文件，只产出新文件"
    evidence:
      artifact: "evidence/R-02/output-800.md"
      diff: "evidence/R-02/diff.txt"
      verification: "wc -c evidence/R-02/output-800.md"
    acceptance:
      pass: "产物存在 + Diff 有实质变化 + 自测命令输出符合预期（三证齐）"
      partial: "有产物但缺 Diff 或缺自测输出"
      fail: "仅口头完成，无产物"
      failure_modes: ["口头完成", "旧货重提", "无自测"]
    codify:
      write_memory: true
      update_sop: true
      problem_ledger: true

  - round_id: "R-03"
    level: "L3"
    single_goal: "跨会话稳定性（记忆写入与回读）"
    not_training: ["新技能", "自动化", "强主动性"]
    task:
      background: "第 1 次会话交代 3 条偏好并明确要求记住；关会话；第 2 次会话回读验证"
      input: "rounds/R-03-prefs.txt（3 条偏好）"
      output: "memory/YYYY-MM-DD.md 写入记录 + 第 2 次会话的回读证据"
      constraints:
        - "偏好必须落在 L2 日志层（见 C4-4），不得只留在上下文"
        - "第 2 次会话开始时先复述 3 条偏好，再回答新问题"
      boundary_hint: "不得把偏好写入 L5 provenance（该层由治理接口写入）"
    evidence:
      artifact: "memory/<today>.md（含 3 条偏好）"
      diff: "sessions.jsonl 两次 session 起止记录"
      verification: "grep -c '偏好' memory/<today>.md  # 期望 ≥ 3"
    acceptance:
      pass: "第 2 次会话能完整复述 3 条偏好且未漂移"
      partial: "复述 2/3 条"
      fail: "≤ 1 条，或第 2 次会话风格明显变化"
      failure_modes: ["承诺失忆", "压缩后丢失", "偏好漂移"]
    codify:
      write_memory: true
      update_sop: true
      problem_ledger: true

# ── 训练前置自检（不打勾不许开训）────────────────────────────────────────
readiness_gate:
  - "进化阶梯当前等级已确认（不得跳级）"
  - "强度矩阵与等级匹配（对照 intensity_matrix）"
  - "验收口径已写死（pass/partial/fail 三态齐）"
  - "证据落盘路径可写（目录已建）"
  - "导师智能体已就位（见 C4-3）"
```

**Step 3 · 生成本轮任务卡**（以 R-01 为例，`training/rounds/R-01-inputs.txt`）：

```text
问题 1：请用一句话说明"记忆分层"解决什么问题。
问题 2：请用一句话说明"训练轮次"与"多聊几次"的区别。
问题 3：请用一句话说明"验收口径"为什么必须先写。
问题 4：请用一句话说明"证据链"在治理中的作用。
问题 5：请用一句话说明"漂移"通常从哪里开始。
```

## 验证步骤

```bash
# 0. 准备：设定 agent 名并进入工作区
AGENT=kunlun                    # ← 换成你的 agent
WS=~/.openclaw/workspace/agents/workspace-$AGENT
cd "$WS" || { echo "❌ 工作区不存在：$WS"; exit 1; }

# 1. 目录树自检
for d in training/rounds training/evidence training/records; do
  [ -d "$d" ] && echo "✅ $d 存在" || echo "❌ $d 缺失"
done
# 期望：三行全为 ✅

# 2. YAML 合法性 + 六要素齐备校验
python3 - <<'PY'
import yaml, sys
p = "training/rounds/L1-L3-plan.yaml"
try:
    doc = yaml.safe_load(open(p, encoding="utf-8"))
except Exception as e:
    sys.exit(f"❌ YAML 解析失败：{e}")
REQUIRED = ["round_id","level","single_goal","task","evidence","acceptance","codify"]
ok = True
for r in doc["rounds"]:
    miss = [k for k in REQUIRED if k not in r]
    if miss:
        ok = False
        print(f"❌ {r.get('round_id','?')} 缺字段：{miss}")
    else:
        print(f"✅ {r['round_id']} ({r['level']}) 六要素齐备 · 目标={r['single_goal']}")
print("── 计划轮数：", len(doc["rounds"]))
print("── 强度矩阵等级：", list(doc["intensity_matrix"].keys()))
sys.exit(0 if ok else 1)
PY
# 期望：R-01/R-02/R-03 三行 ✅ + 计划轮数：3

# 3. 前置门（readiness_gate）逐条打印
python3 -c "
import yaml
d=yaml.safe_load(open('training/rounds/L1-L3-plan.yaml',encoding='utf-8'))
for i,g in enumerate(d['readiness_gate'],1): print(f'[{i}] {g}')
"
# 期望：5 条门禁逐行输出，开训前逐条打勾

# 4. 跑第 1 轮（L1 · 风格稳定性）
openclaw agents list | grep "$AGENT"          # 先确认 agent 已注册
openclaw agent --agent "$AGENT" --message "$(cat training/rounds/R-01-inputs.txt)"
# 期望：5 条风格一致的短回答，无模板客套话

# 5. 证据落盘自检（第 1 轮必须有产物）
ls -l training/evidence/R-01/ 2>/dev/null | wc -l
# 期望：≥ 1（目录非空）；若为 0 → 本轮判 fail（"没证据 = 没完成"）

# 6. 沉淀动作自检（写入 memory 与否）
grep -c "R-01" memory/$(date +%F).md 2>/dev/null
# 期望：≥ 1；为 0 → 本轮未沉淀，回到第 4 步重跑沉淀动作
```

> ✅ **已实测（2026-09-27）**：单轮对话真名是 `openclaw agent --agent <id> --message "<text>"`
> （`openclaw agent --help` 实测）。`openclaw chat` 只是本地 TUI 别名（= `tui --local`），
> **没有** `--agent / --prompt` 选项。本机 2026.9.4 的 `openclaw agents list` 亦实测存在。

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`（`openclaw --version` 实测输出）
- **网关**：Hermes 0.20.1（本机为 Subagent 执行体，父 agent 派发）
- **操作系统**：macOS 26.5.1
- **工作区根**：`~/.openclaw/workspace/agents/workspace-<agent>/`（本机 18 个）
- **本机 skills 数**：`~/.openclaw/workspace/skills/` 共 **236 个**（另含 2 个非技能条目，
  故 `ls | wc -l` = 238，`ls -d */ | wc -l` = 236）
- **日期**：2026-09-27
- **参考基线**：v4.0 卷四模块 4 的"六要素 + 强度匹配表 + 三级验收"；本配方把其
  概念骨架压缩为一份可直接跑的 YAML，并补上本机的目录树与验证命令。

## 排坑

1. **越级考试（最高频）**：L1 的 agent 被派了 L3 的任务，表现为"跑三轮全 fail，
   于是判定它不行"。核验：对照 `intensity_matrix.<level>.forbidden`，一旦本轮任务
   命中 forbidden 列表，本轮**作废重设计**，不计入失败率。

2. **一轮多目标**：`single_goal` 写了"提升综合能力"。症状是验收永远含糊。
   解法：`single_goal` 必须是一个**可人评的单维度**（"风格稳定性"/"交付闭环"/
   "跨会话记忆"三选一），其余维度一律进 `not_training`。

3. **没有验收口径**：训练永远在"再来一次"里打转。检查 `acceptance` 段三态
   （pass/partial/fail）是否齐；缺 `fail` 是最常见的漏项——没有 fail 定义，
   就无法判"这一轮结束了"。

4. **无产物 = 假完成**：agent 在对话里说"我已经改好了"，但 `training/evidence/`
   是空的。铁律：没证据 = 没完成。`ls training/evidence/R-*/ | wc -l` 为 0 即判 fail。

5. **不沉淀 = 白训**：每轮结束不回看 `codify` 段。后果是同样的错误在 R-02/R-03
   反复出现。核验：`grep -c "R-0" memory/$(date +%F).md`，期望等于已完成轮数。

6. **YAML 缩进翻车**：中文标点混入列表项（全角逗号）、Tab 与空格混用。
   校验：`python3 -c "import yaml;yaml.safe_load(open('...').read())"`，
   报错行号即病灶。

## 进阶

- **进阶 1 · 训练轮次与双三角联动**：每轮结束后，用 C4-2 的双三角模型给本轮打分
  （能力三角三项 + 可靠性三角三项均 0–5 分）。R-01 重点看**可靠性三角的稳定性顶点**，
  R-02 看**能力三角的专业深度顶点**，R-03 看**可预期性顶点**。三轮的分数曲线就是
  agent 的成长曲线。

- **进阶 2 · 轮次模板化**：把 `rounds/R-01-*` 抽象成 `templates/round-template.yaml`，
  用 `cp templates/round-template.yaml rounds/R-04.yaml` 开新轮。这样"设计一轮训练"
  的成本从 30 分钟降到 3 分钟，训练频率才能真正上去。

- **进阶 3 · 训练证据入 TEV**：把每轮的"产物 / Diff / 自测输出"三件套直接按
  TEV（三证据验证 / Three-Evidence Verification）格式落盘（见 C5-4）。这样
  "训练成功"不再是主观判断，而是一条可被第三方复现的证据链，并可作为
  Merit Ledger（功绩账本）的记账前提。

- **进阶 4 · 失败进整改单**：任一轮判 `fail`，自动生成一张 Remediation Ticket
  （修复工单，原：整改单），写明"失败模式 + 根因 + 重训计划 + 截止轮次"。
  训练从此有了纠偏闭环，而不是"再来一次"。

---

## 附录 · 训练轮次六要素速查 + 强度自检表

### 附表 A · 六要素「写死 / 写不死的分野」

| 要素 | 写不死的表现 | 写死的判据（本节采用） |
|---|---|---|
| 单一目标 | "综合提升一下" | 一句话，且能从回答里人评是否达成 |
| 匹配强度 | "难度适中" | 对照 `intensity_matrix` 的 complexity/conflict/chain 三字段 |
| 明确任务 | "帮我搞一下" | 背景+输入+输出+约束+边界提醒，五段齐 |
| 证据交付 | "我完成了" | 有可写路径的产物 + 至少一条自测命令 |
| 验收口径 | "还行吧" | pass/partial/fail 三态 + failure_modes 列表 |
| 沉淀动作 | "下次注意" | write_memory / update_sop / problem_ledger 三个布尔位 |

### 附表 B · 强度自检（开训前 10 秒勾）

```text
[ ] 本轮 level 已确认（L1/L2/L3），未跳级
[ ] 本轮任务未命中 intensity_matrix.<level>.forbidden 任一项
[ ] single_goal 只有一个，其余维度已进 not_training
[ ] task 五段（背景/输入/输出/约束/边界）齐
[ ] evidence 有绝对可写路径
[ ] acceptance 三态齐（pass/partial/fail）
[ ] codify 三布尔位已定
```

> 任一未勾 → 本轮**不启动**。跳过自检直接开训，是"跑三轮全 fail、
> 于是判定 agent 不行"这一误判的根源。

### 附表 C · 三轮训练的判定速查

| 轮次 | 等级 | 主维度 | 通过判据 | 失败后动作 |
|:--:|:--:|---|---|---|
| R-01 | L1 | 风格稳定性 | 5/5 一致率 ≥ 90% | 回改 SOUL constraints |
| R-02 | L2 | 交付闭环 | 三证齐（产物+Diff+自测） | 补证据纪律入 AGENTS.md |
| R-03 | L3 | 跨会话记忆 | 第 2 次会话完整复述偏好 | 补 flush 前写回 L3（见 C4-4） |

三轮全过 = 从 L1 可塑虾（Malleable Agent）训到 L3 稳定虾（Stable Agent）；
任一轮 fail = 生成一张修复工单（Remediation Ticket），指定重训轮次。

---

# C4-2 · 双三角模型实操：Expectation-Actuality-Feedback Loop 落地

## 背景

训 Agent 的人最常说的两句话是"这只挺强的"和"这只不太行"。这两句话几乎无用——
因为它们只回答了**一个维度**：上限。真实情况是：某次输出惊艳，不代表已经成熟；
总是掉棒漂移，也不代表模型或 prompt 不行。

双三角模型（Dual-Triangle Model: Expectation-Actuality-Feedback Loop，原：双三角模型）
把 Agent 成熟度拆成**两个互相有张力的三角**：

- **能力三角（Capability Triangle）**：专业深度 / 工具广度 / 创造性 —— 决定**上限**
- **可靠性三角（Reliability Triangle）**：稳定性 / 可控性 / 可预期性 —— 决定**下限**

两者之间有三条张力：能力越强越难稳定、稳定性要求越高能力发挥越受限、
创造性越高可预期性越低。

本机实测的典型误判是**只补能力不补可靠性**：不断加新 skill、接新工具，
但记忆不写、治理不建、验收不设，最后得到一个"看起来很强、实际不可用"的 Agent。
这一例解决的**具体问题**：**给我一个可执行的评分脚本，把"挺强/不太行"变成
双三角 6 个顶点各 0–5 分 + 一张张力诊断图**。

> **来源**：v1.0 卷四《双三角模型》；v4.0 卷四模块 5（双三角模型：Expectation-
> Actuality-Feedback Loop）。本配方从零撰写，仅沿用"两三角 + 六顶点 + 三张力"骨架事实。

## 配置（完整可复制）

**Step 1 · 写入评分定义 `training/eval/dual-triangle.yaml`**：

```yaml
# ============================================================================
# 双三角模型评分定义（Dual-Triangle Model Scoring Spec）
# 路径：~/.openclaw/workspace/agents/<agent>/training/eval/dual-triangle.yaml
# 版本：v1.0 · 2026-09-27
# ============================================================================
schema_version: 1
scale: [0, 1, 2, 3, 4, 5]      # 0=缺失 1=极弱 2=偏弱 3=及格 4=良好 5=专家

capability_triangle:            # 能力三角：决定上限
  professional_depth:           # 专业深度
    question: "本领域最难的题，它能稳定答对到什么程度？"
    anchors:
      "1": "只能复述通用知识"
      "3": "能处理常规专业问题"
      "5": "能处理边界案例并有风格"
  tool_breadth:                 # 工具广度
    question: "能稳定调用多少个有效工具/外部系统？"
    anchors:
      "1": "只会对话"
      "3": "能稳定用 3-5 个工具"
      "5": "能编排多工具链"
  creativity:                   # 创造性
    question: "遇到没见过的情况，能不能在边界内举一反三？"
    anchors:
      "1": "离开模板就不会"
      "3": "能在给定框架内变通"
      "5": "能产出被复用的新解法"

reliability_triangle:           # 可靠性三角：决定下限
  stability:                    # 稳定性
    question: "跨会话/跨轮次，风格与角色是否一致？"
    anchors:
      "1": "每次都像换了一只"
      "3": "同会话内基本一致"
      "5": "跨会话仍可识别为同一只"
  controllability:              # 可控性
    question: "是否守边界？会不会越权或过度主动？"
    anchors:
      "1": "屡次越权"
      "3": "大体守界，偶有越界"
      "5": "边界零违例且有台账"
  predictability:               # 可预期性
    question: "能不能预判它什么时候会掉棒？失败模式是否清晰？"
    anchors:
      "1": "完全无法预判"
      "3": "主要失败模式已知"
      "5": "有失败模式清单 + 触发条件"

tensions:                       # 三条张力（诊断用）
  - id: T1
    name: "能力↑ → 稳定↓"
    signal: "tool_breadth 高分 且 stability 低分"
    advice: "先冻结新工具，补记忆与回读（C4-4），再扩能力"
  - id: T2
    name: "稳定要求↑ → 能力受限"
    signal: "controllability 高分 且 professional_depth/creativity 低分"
    advice: "放宽边界到 Needs-Confirm 档，给它中等难度任务试错"
  - id: T3
    name: "创造性↑ → 可预期性↓"
    signal: "creativity 高分 且 predictability 低分"
    advice: "为创造性动作加'提议-确认'两段式，保住可预期性"

grading_rubric:
  expert_agent:  "两三角均 ≥ 4.0"
  stable_agent:  "可靠性三角 ≥ 3.5 且能力三角 ≥ 2.5"
  usable_agent:  "两三角均 ≥ 2.5"
  below_usable:  "任一三角 < 2.5"
```

**Step 2 · 写入评分脚本 `training/eval/dual-triangle.py`**：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""双三角模型评分脚本（Dual-Triangle Model Scorer）
路径：~/.openclaw/workspace/agents/<agent>/training/eval/dual-triangle.py
用法：python3 dual-triangle.py scores.json
输入 scores.json 为六个顶点各 0-5 分的对象（完整样例见下文 Step 3）
"""
import json, sys, statistics
from pathlib import Path

CAP = ["professional_depth", "tool_breadth", "creativity"]
REL = ["stability", "controllability", "predictability"]
LABEL = {
    "professional_depth": "专业深度", "tool_breadth": "工具广度",
    "creativity": "创造性", "stability": "稳定性",
    "controllability": "可控性", "predictability": "可预期性",
}

def load(p):
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    for k in CAP + REL:
        if k not in d:
            sys.exit(f"❌ 缺字段：{k}")
        if not (0 <= d[k] <= 5):
            sys.exit(f"❌ {k}={d[k]} 越界（0-5）")
    return d

def bar(v):
    full = int(v); half = 1 if (v - full) >= 0.5 else 0
    return "█" * full + ("▌" if half else "") + "·" * (5 - full - half)

def main():
    s = load(sys.argv[1] if len(sys.argv) > 1 else "scores.json")
    cap = statistics.mean(s[k] for k in CAP)
    rel = statistics.mean(s[k] for k in REL)
    print("── 能力三角（Capability Triangle）· 上限 ──")
    for k in CAP:
        print(f"  {LABEL[k]:<6} {bar(s[k])} {s[k]}")
    print(f"  平均 = {cap:.2f}")
    print("── 可靠性三角（Reliability Triangle）· 下限 ──")
    for k in REL:
        print(f"  {LABEL[k]:<6} {bar(s[k])} {s[k]}")
    print(f"  平均 = {rel:.2f}")

    # 等级判定
    if cap >= 4.0 and rel >= 4.0:
        grade = "Expert Agent（专家虾）"
    elif rel >= 3.5 and cap >= 2.5:
        grade = "Stable Agent（稳定虾）"
    elif cap >= 2.5 and rel >= 2.5:
        grade = "Usable Agent（可用虾）"
    else:
        grade = "Below Usable（未达可用线）"
    print(f"── 判定：{grade} ──")

    # 张力诊断
    hits = []
    if s["tool_breadth"] >= 4 and s["stability"] <= 2:
        hits.append("T1 能力↑→稳定↓：先补记忆与回读，再扩工具")
    if s["controllability"] >= 4 and (s["professional_depth"] <= 2 or s["creativity"] <= 2):
        hits.append("T2 稳定↑→能力受限：放宽到 Needs-Confirm 档试错")
    if s["creativity"] >= 4 and s["predictability"] <= 2:
        hits.append("T3 创造↑→可预期↓：创造性动作改两段式")
    print("── 张力诊断 ──")
    print("\n".join("  ⚠ " + h for h in hits) if hits else "  ✅ 无明显张力失衡")

if __name__ == "__main__":
    main()
```

**Step 3 · 写入本轮评分数据 `training/eval/scores.json`**：

```json
{
  "agent": "<agent>",
  "round": "R-02",
  "date": "2026-09-27",
  "professional_depth": 3,
  "tool_breadth": 4,
  "creativity": 2,
  "stability": 2,
  "controllability": 4,
  "predictability": 2
}
```

## 验证步骤

```bash
cd ~/.openclaw/workspace/agents/workspace-<agent>/training/eval

# 1. YAML 合法性
python3 -c "import yaml;yaml.safe_load(open('dual-triangle.yaml',encoding='utf-8'));print('✅ 评分定义合法')"
# 期望：✅ 评分定义合法

# 2. 评分脚本可跑
python3 dual-triangle.py scores.json
# 期望输出（节选）：
#   ── 能力三角 · 上限 ──
#     专业深度 ███·· 3
#     工具广度 ████· 4
#     创造性   ██··· 2
#     平均 = 3.00
#   ── 可靠性三角 · 下限 ──
#     稳定性   ██··· 2
#     可控性   ████· 4
#     可预期性 ██··· 2
#     平均 = 2.67
#   ── 判定：Usable Agent（可用虾） ──
#   ── 张力诊断 ──
#     ⚠ T1 能力↑→稳定↓：先补记忆与回读，再扩工具
#     ⚠ T2 稳定↑→能力受限：放宽到 Needs-Confirm 档试错
#   （注：本组样例 creativity=2、controllability=4 → 触发 T2 而非 T3；
#     T3 需 creativity≥4 且 predictability≤2 才触发）

# 3. 越界检测（故意造一个 6 分）
echo '{"professional_depth":6,"tool_breadth":1,"creativity":1,"stability":1,"controllability":1,"predictability":1}' > /tmp/bad.json
python3 dual-triangle.py /tmp/bad.json
# 期望：❌ professional_depth=6 越界（0-5）  （退出码非 0）

# 4. 缺字段检测
echo '{"professional_depth":3}' > /tmp/miss.json
python3 dual-triangle.py /tmp/miss.json
# 期望：❌ 缺字段：tool_breadth

# 5. 历史评分入账（每轮留一份，形成成长曲线）
cp scores.json ../../training/records/dual-triangle-R-02.json
ls ../../training/records/dual-triangle-*.json
# 期望：能看到逐轮累积的评分快照
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **Python**：系统 python3（10 种 YAML/JSON 校验脚本均只用标准库 + `PyYAML`）
- **OS**：macOS 26.5.1
- **依赖**：`pyyaml`（`python3 -c "import yaml"` 无报错即可）
- **日期**：2026-09-27
- **来源基线**：v4.0 卷四模块 5 的双三角定义（两三角六顶点三张力）；
  本配方把其升级为**可跑脚本 + 可回看的成长曲线**。

## 排坑

1. **把"偶尔很强"当"已经成熟"**：单次惊艳输出被记为能力三角满分。核验：评分必须
   取**近 3 轮平均**，单次高分不入账。脚本建议：`scores.json` 改为
   `scores-R-0X.json` 逐轮存盘，用 `mean` 汇总。

2. **只补能力不补可靠性**：发现 `cap ≥ 3.5` 但 `rel ≤ 2.5`。这是最危险的形态
   （看起来很强、实际不可用）。处置：**冻结新工具/新技能**，先按 C4-4 补记忆金字塔，
   按 C5-2 补边界三档，再回头扩能力。

3. **评分自欺**：all-5 分。脚本不拦，但要在评语里写**证据**：每个 4/5 分必须带一条
   证据（文件路径 / 命令输出 / 会话记录）。把 `scores.json` 扩出 `evidence` 字段，
   无证据的顶点自动降 1 分。

4. **三角混算**：把两三角平均成一个总分。**禁止**——单总分恰好抹掉了"强而不稳"
   这一最需要治理的形态。脚本永远分列两个平均 + 一个等级判定。

5. **张力诊断被当告警忽略**：`⚠ T1` 出现后没人处置，两周后变成"工具一堆、
   记忆全无"的典型失败案例。处置：任一张力命中 → 自动生成 Remediation Ticket
   （见 C5-4 进阶），指定整改轮次。

## 进阶

- **进阶 1 · 双三角 × 进化阶梯映射**：把 L1–L5 与三角阈值绑定——
  L1 可塑虾：只看可靠性三角的稳定性 ≥ 3；L2 可用虾：cap ≥ 2.5 且 rel ≥ 2.5；
  L3 稳定虾：rel ≥ 3.5；L5 军团虾：cap ≥ 4 且 rel ≥ 4。这样"它到哪一级了"变成
  一次脚本输出，而不是主观争论。

- **进阶 2 · 评分为训练轮次自动选强度**：脚本读 `dual-triangle` 等级 → 自动查
  C4-1 的 `intensity_matrix` → 输出"本轮建议强度"。闭环：评完分就能开下一轮，
  不越级也不原地踏步。

- **进阶 3 · 张力进体检**：把三张力的命中数作为每周体检（C5-3）的一个指标，
  与漂移分（Drift Score）并列。这样"能力/可靠性失衡"进入例行治理，而不是等翻车才发现。

- **进阶 4 · 双三角对位业界**：Claude Agent SDK / OpenAI Agents SDK / LangGraph /
  AutoGen / CrewAI / LlamaIndex 六框架**均只有"能力上限"视角**（能做什么），
  无"可靠性下限"维度。双三角模型是本书训练层相对业界的实质性差异点，可在对外
  材料中作为"训练评估方法论"单独成篇。

---

## 附录 · 双三角六顶点锚点速查 + 评分校准

### 附表 A · 六顶点锚点（0–5 分对照）

| 顶点 | 三角 | 1 分 | 3 分 | 5 分 |
|---|---|:--:|:--:|:--:|
| 专业深度 | 能力 | 只会复述通用知识 | 能处理常规专业问题 | 能处理边界案例且有风格 |
| 工具广度 | 能力 | 只会对话 | 稳定用 3–5 个工具 | 能编排多工具链 |
| 创造性 | 能力 | 离开模板就不会 | 框架内可变通 | 产出被复用的新解法 |
| 稳定性 | 可靠 | 每次都像换了一只 | 同会话内基本一致 | 跨会话仍可识别 |
| 可控性 | 可靠 | 屡次越权 | 大体守界 | 零违例且有台账 |
| 可预期性 | 可靠 | 完全无法预判 | 主要失败模式已知 | 有失败模式清单 + 触发条件 |

### 附表 B · 评分校准三原则

1. **证据优先**：每个 ≥4 分必须带一条证据（路径 / 命令输出 / 会话记录）；
   无证据自动降 1 分。
2. **近 3 轮平均**：单次高分不入账；`scores.json` 逐轮存盘，用均值汇总。
3. **两三角分列**：**严禁**把能力与可靠性平均成一个总分——单总分恰好抹掉
   "强而不稳"这一最需要治理的形态。

### 附表 C · 成长曲线记录法

```text
training/records/dual-triangle-R-01.json   →  cap=2.0  rel=2.3  → Usable
training/records/dual-triangle-R-02.json   →  cap=3.0  rel=2.7  → Usable
training/records/dual-triangle-R-03.json   →  cap=3.3  rel=3.7  → Stable
```

三轮曲线说明：**能力与可靠性必须同步上升**。若三轮里 cap 从 2.0 涨到 4.5
而 rel 停在 2.5，就是"只补能力不补可靠性"的典型失败形态——立即冻结新工具，
按 C4-4 补记忆、按 C5-2 补边界，再回头扩能力。

---

# C4-3 · 导师智能体（Mentor Agent）机制配置 + 训练记录

## 背景

训练失败的头号原因不是 prompt 不够好，而是**没有一只会观察、会反馈、会追问、
会沉淀的导师智能体（Mentor Agent，原：教练虾）在带训**。业界的现状是：
CrewAI 有 Cron/流程但没有导师角色；Claude Agent SDK 的 subagent 可以充当"观察者"
但没有反馈协议；LangGraph / AutoGen / OpenAI Agents SDK / LlamaIndex
**均无教练角色原语**。

导师机制的四件事（每件都有对应铁律）：

| 职责 | 做什么 | 铁律 |
|---|---|---|
| 观察（Observe） | 按框架看：稳定性/完整性/边界/漂移 | 不记录 = 没观察 |
| 反馈（Feedback） | 三段式：事实描述 → 偏差识别 → 纠偏建议 | 不纠偏 = 无效反馈 |
| 追问（Probe） | 追问根因：本质原因 / 系统性还是偶发 / 下一轮验证什么 | 不追问 = 下轮还是瞎试 |
| 沉淀（Codify） | 写入 MEMORY / 更新 SOP / 更新问题账本 | 不沉淀 = 白训 |

本机实测有个特殊约束：**导师智能体本身也是一个 OpenClaw agent**，所以它必须有自己的
SOUL/AGENTS，而且它的记忆要独立于被训者（否则观察记录会被被训者的记忆污染）。
这一例解决的**具体问题**：**如何在 15 分钟内配出一只可用的导师智能体，
并让它产出结构化的训练记录**。

> **来源**：v1.0 卷四《教练虾机制》；v4.0 卷四模块 3（Mentor Agent 机制）。
> 本配方从零撰写，仅沿用"四职责 + 三段式反馈 + 沉淀三动作"骨架事实。

## 配置（完整可复制）

**Step 1 · 建导师工作区**（导师与被训者必须是两个独立工作区）：

```bash
MENTOR=mentor            # ← 导师智能体名（建议独立，不复用被训者）
cd ~/.openclaw/workspace/agents
mkdir -p workspace-$MENTOR/{training/records,training/ledger,memory}
touch workspace-$MENTOR/training/records/.keep
```

**Step 2 · 导师 SOUL.md**（`workspace-<mentor>/SOUL.md`）：

```markdown
---
protocol: SOUL
schema_version: 1
name: "mentor"
display_name: "导师智能体"
role_class: supervisor
personality:
  - 以证据裁定，不以资历裁定
  - 先记录事实，再给判断
  - 主动指出风险，即使没人问
boundaries:
  - 不代替被训者执行任务，只观察与反馈
  - 不把观察记录写进被训者的 MEMORY
  - 不评价"聪明与否"，只评价"行为与证据"
voice:
  language: zh-CN
  tone: 教练式复盘
  length_limit: 200
  emoji: sparing
constraints:
  - 每条反馈必须是"事实描述 → 偏差识别 → 纠偏建议"三段
  - 每次训练必须落一份结构化记录（不得口头反馈了事）
stability:
  drift_guard: true
  mood_switch: false
  persona_anchor: "证据即权力"
---

# 你是导师智能体

你的职责不是替被训者把活干完，而是让它**每一轮都比上一轮更稳**。
你的价值来自"你观察到了别人没观察到的偏差，并把它变成下一轮的对照实验"。
```

**Step 3 · 导师 AGENTS.md 四职责段**（`workspace-<mentor>/AGENTS.md`）：

```markdown
# 导师智能体操作协议（Mentor Agent Protocol）

## 开工 5 步
1. 读本轮训练卡（training/records/round-<id>.card.md）
2. 读被训者上一轮记录（training/records/round-<id-1>.record.md）
3. 确认观察维度（稳定性 / 完整性 / 边界 / 漂移）
4. 观训：只记录，不插话
5. 观训结束：产出结构化反馈记录（三段式）+ 沉淀三动作

## ✅ 做
- 按「观察四维」逐项记录（含时间戳与原始输出片段）
- 反馈先复述事实，再说偏差，最后给纠偏建议
- 追问三类根因：本质原因 / 系统性还是偶发 / 下轮验证什么
- 每轮结束写 MEMORY + 更新 SOP + 更新问题账本

## ❌ 不做
- 不替被训者完成任务（你的任务是训练它，不是代跑）
- 不在被训者会话里直接插话（污染上下文）
- 不给出无证据的夸奖或无证据的差评
- 不把导师记忆与被训者记忆混放

## 观察四维表
| 维度 | 观察什么 | 不是看什么 |
|---|---|---|
| 稳定性 | 风格/语气/角色是否一致 | 单次回答好不好 |
| 完整性 | 是否有产物/证据/验收 | 是否只给说法 |
| 边界 | 是否越权/越级/越界 | 是否"看起来聪明" |
| 漂移 | 哪里开始不像上一轮 | 这轮有没有一点问题 |
```

**Step 4 · 训练记录模板 `training/records/record-template.md`**：

```markdown
# 导师反馈记录（Mentor Agent Feedback Record）

## 基本信息
- 训练轮次：R-__  等级：L__  日期：____-__-__
- 被训者：<agent>  导师：<mentor>

## 一、观察（Observe · 只记事实）
| 维度 | 记录 | 原始片段/证据 |
|---|---|---|
| 稳定性 | | |
| 完整性 | | |
| 边界 | | |
| 漂移 | | |

## 二、反馈（Feedback · 三段式）
1. **事实描述**：刚才你做了什么 / 输出是什么
2. **偏差识别**：哪里与预期不一致 / 偏离方向 / 偏离程度
3. **纠偏建议**：下一步改什么 / 不改什么 / 下一轮验证什么

## 三、追问（Probe）
- 本质原因：
- 系统性 or 偶发：
- 下一轮验证：

## 四、沉淀（Codify · 三动作）
- [ ] 写入 MEMORY：memory/<today>.md 追加
- [ ] 更新 SOP/模板：
- [ ] 更新问题账本：training/ledger/problems.md

## 五、判定
- 本轮：pass / partial / fail  依据：
```

**Step 5 · 问题账本 `training/ledger/problems.md`**：

```markdown
# 问题账本（Problem Ledger）

| ID | 发现轮次 | 问题 | 根因 | 状态 | 关闭轮次 |
|---|---|---|---|---|---|
| P-001 | R-01 | 回答出现模板客套话 | SOUL constraints 未含"禁模板" | open |  |
| P-002 | R-01 | 第 4 问风格突然变长 | 无长度上限 | open |  |
```

## 验证步骤

```bash
MENTOR=mentor
cd ~/.openclaw/workspace/agents/workspace-$MENTOR

# 1. 目录与文件齐备
for f in SOUL.md AGENTS.md training/records/record-template.md training/ledger/problems.md; do
  [ -f "$f" ] && echo "✅ $f" || echo "❌ $f 缺失"
done
# 期望：四行全 ✅

# 2. SOUL frontmatter 可解析
python3 - <<'PY'
import yaml
raw = open("SOUL.md", encoding="utf-8").read()
assert raw.startswith("---"), "❌ 首行非 ---"
meta = yaml.safe_load(raw[4:raw.index("\n---", 3)])
assert meta["role_class"] == "supervisor", "❌ 导师应为 supervisor"
assert meta["name"] == "mentor", "❌ name 与目录名不符"
print("✅ 导师 SOUL 合法：", meta["name"], "/", meta["role_class"])
PY

# 3. 导师已注册
openclaw agents list | grep "$MENTOR"
# 期望：一行含导师名

# 4. 导师职责自检：让它复述四职责与三段式
openclaw agent --agent "$MENTOR" --message "你的四职责是什么？反馈为什么必须是三段式？"
# 期望：答出 观察/反馈/追问/沉淀 + 事实→偏差→纠偏

# 5. 训练记录落盘检查（跑完一轮后）
ls -l training/records/ | grep record
# 期望：除模板外，出现 round-R-01.record.md

# 6. 沉淀三动作核验
grep -c "R-01" memory/$(date +%F).md           # 期望 ≥ 1（写入 MEMORY）
grep -c "R-01" training/ledger/problems.md      # 期望 ≥ 1（更新问题账本）

# 7. 记录完整性校验（三段式 + 四维）
python3 - <<'PY'
import glob, sys, re
for f in glob.glob("training/records/round-*.record.md"):
    t = open(f, encoding="utf-8").read()
    need = ["观察", "反馈", "追问", "沉淀", "偏差识别", "纠偏建议"]
    miss = [k for k in need if k not in t]
    print(("✅ " if not miss else "❌ ") + f + (" 缺：" + ",".join(miss) if miss else ""))
PY
```

> ⏳ 待实测：导师智能体与被训者的双工作区隔离在 OpenClaw 2026.9.4 中的确切口径
> （是否需要在 `config` 里显式声明两者关系）以 `openclaw --help` 为准；本机未端到端
> 跑过"导师观训被训者"的自动化链路，当前为**手动观训 + 结构化落盘**模式。

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **工作区**：本机 `~/.openclaw/workspace/agents/` 下 18 个 `workspace-*` 工作区，
  导师工作区为新增第 19 个（`workspace-mentor`）；若你不想新增，可复用
  `workspace-tiance`（本机 Supervisor Layer 角色所在）作导师。
- **本机 skills 数**：236 个（导师可直接调用 `skill-security-audit-v2` /
  `afrexai-compliance-audit` 等审计类技能辅助观察）。
- **日期**：2026-09-27
- **来源基线**：v4.0 卷四模块 3 的四职责与三段式反馈结构；本配方补上本机的
  双工作区隔离约定与落盘模板。

## 排坑

1. **导师=被训者（最常见错误）**：让被训的 agent 自己当教练。症状是"自评全过"。
   核验：`MENTOR != AGENT`，且两个工作区目录不同。导师的记忆必须独立。

2. **只观察不记录**：观训完凭印象说两句。铁律：不记录 = 没观察。核验：
   `ls training/records/round-*.record.md` 必须逐轮增长。

3. **反馈变情绪**："这轮不行，再来一次"是复读机不是反馈。核验：记录里
   "偏差识别""纠偏建议"两段必须非空且具体（引用的是原始输出片段，不是形容词）。

4. **不追问根因**：跳过 Probe 直接重跑。后果是同一失败模式反复出现。
   核验：`problems.md` 里每个 open 问题都必须有"根因"列填写；空根因 = 未追问。

5. **记忆污染**：导师把被训者的会话原文整段拷进自己的 MEMORY，几天后导师开始
   用被训者的口吻说话。解法：导师 MEMORY 只写**观察结论 + 证据路径**，
   不写被训者的原文。

6. **导师过度主动**：导师替被训者把任务做了，被训者"通过"了但什么也没学会。
   核验：导师工作区的 `training/records` 里有产物交付 = 越界，应改为只留反馈记录。

## 进阶

- **进阶 1 · 导师 × 三省评审制**：把导师的角色从"教练"扩展为"三省评审制
  （Three-Stage Review: Proposal / Review / Final-Decision）"中的 Review 层——
  被训者提案，导师复核，丘总终审。这样带了治理属性，适合 L4 以上 agent。

- **进阶 2 · 导师记录入 Merit Ledger**：每轮训练记录即"功绩账本（Merit Ledger）"
  的一行，含轮次/等级/判定/证据路径。训练因此有了"历史成绩单"。

- **进阶 3 · 多导师轮值**：当被训者进入 L4/L5，单一导师的视角会固化。
  配置 2–3 只导师轮值（不同观察侧重：一只专看稳定性，一只专看边界），
  用交叉观察降低单一视角盲区。

- **进阶 4 · 导师的导师**：对 Mentor Agent 本身也跑 C4-2 双三角评分——
  导师的可控性（是否越界代跑）与可预期性（反馈是否结构化）必须达标，
  否则"带训的人自己不稳"。

---

## 附录 · 导师反馈话术库 + 四维观察范例

### 附表 A · 三段式反馈的话术对照（反例 → 正例）

| 段 | ❌ 反例 | ✅ 正例 |
|---|---|---|
| 事实描述 | "你这次做得不太好" | "本次 5 条回答中，第 4 条由 38 字变为 121 字。" |
| 偏差识别 | "感觉有点跑偏" | "与 SOUL 的 `length_limit: 120` 冲突，越界 1 字，方向是篇幅膨胀。" |
| 纠偏建议 | "下次注意" | "下轮把 120 字上限写进系统提示，并在第 4 问前复述约束。" |

**判定**：反例三句全是形容词，正例三句全带数字或路径。导师记录的合格线
= 每段至少一个可核查对象。

### 附表 B · 追问三问模板

```text
问 1（本质原因）：这次的失败，是协议没立住 / 环境没通 / 强度过高 / 记忆没沉淀？
问 2（系统 or 偶发）：换成另一个同类任务，会不会同样失败？（会 = 系统性，要改协议）
问 3（下轮验证）：改变 X 之后，观察 Y 是否变化？
```

**判定**：三问任何时候缺任一问 → 该轮"未完成追问"，禁止进入下一轮。

### 附表 C · 四维观察的记录范例

```text
【稳定性】R-03 第 2 次会话仍用"结论优先"结构 → 与 R-01 一致（✅ 无漂移）
【完整性】产物 evidence/R-03/prefs.md 存在，但缺 Diff → 证二缺失（⚠ partial）
【边界】第 2 次会话试图写 provenance → 被拦（✅ 边界生效）
【漂移】第 3 问回答出现"亲爱的用户"→ 模板话术回潮（🚨 记入问题账本）
```

### 附表 D · 导师自检（带训前 30 秒）

```text
[ ] 我 ≠ 被训者（两个独立工作区）
[ ] 本轮记录模板已就位
[ ] 观察维度已选定（本轮主看哪一维）
[ ] 我不会在被训者会话里插话
[ ] 上轮问题账本已读（避免重复追问同一问题）
```

---

# C4-4 · 分层记忆 5 层金字塔实操：从短期到长期

## 背景

Agent 会忘记你是谁，通常不是因为"记性差"，而是因为**记忆没有分层**——
所有东西挤在同一个文件里，启动时加载不完，压缩时又整段丢掉。

OpenClaw 2026.9 的真实记忆模型是**5 层金字塔（L1–L5）**，从运行态到永恒态：

```text
┌──────────────────────────────────────────────────────────┐
│  L5 · 永恒态   Provenance · provenance.jsonl（谁写过、何时、为何） │
├──────────────────────────────────────────────────────────┤
│  L4 · 复盘态   Review · memory/review/*.md（每天/每周 recap）     │
├──────────────────────────────────────────────────────────┤
│  L3 · 备忘态   Prospective · memory/prospective/*.md（待办/承诺） │
├──────────────────────────────────────────────────────────┤
│  L2 · 日志态   Episodic Log · memory/YYYY-MM-DD.md（每日流水）    │
├──────────────────────────────────────────────────────────┤
│  L1 · 精选态   Curated Core · MEMORY.md（精选 + 索引）           │
└──────────────────────────────────────────────────────────┘
```

四可原则：**可定位**（文件名+frontmatter 双层）、**可加载**（L1 ≤ 30% 记忆块）、
**可压缩**（compaction 前触发 flush）、**可溯源**（L5 每条有来源）。

本机实测的关键事实（重要，与旧结论不同）：压缩相关真名是
**三者并存**——① `reserveTokensFloor` 字段（可配置，内存刷写下限）；
② 常量 `RESERVE_TOKENS_FLOOR = 2e4`（= 20000，默认值）；
③ `MAX_COMPACTION_RESERVE_RATIO = 0.25`（不可配置的比率上限）。
**不得套用"`reserveTokensFloor` 不存在"的旧调研错误结论**。
这一例解决的**具体问题**：**给我一棵可落地的 5 层记忆目录树 + `compaction.flush`
配置 + 一套验证命令，让 Agent 跨 compaction 不失忆**。

> **来源**：v1.0 卷五模块 1《记忆管理》；v4.0 卷五模块 1（Memory Engineering，
> 5 层模型 + flushPlan 真名）。本配方从零撰写，仅沿用 L1–L5 与真名事实。

## 配置（完整可复制）

**Step 1 · 建 5 层目录树**：

```bash
cd ~/.openclaw/workspace/agents/workspace-<agent>
mkdir -p memory/{daily,prospective,review}
touch memory/MEMORY.md memory/provenance.jsonl
touch memory/.gitkeep
ls -R memory
# 期望：
# memory/MEMORY.md  memory/provenance.jsonl
# memory/daily  memory/prospective  memory/review
```

**Step 2 · 写入 L1 精选态 `memory/MEMORY.md`**（索引 + 精选，≤ 记忆块 30%）：

```markdown
---
layer: L1
kind: curated-core
schema_version: 1
max_block_ratio: 0.30          # L1 必须 ≤ 记忆块 30%（超出即启动加载不全）
index:
  daily: memory/daily/          # → L2
  prospective: memory/prospective/  # → L3
  review: memory/review/        # → L4
  provenance: memory/provenance.jsonl  # → L5
---

# 精选记忆（Curated Core）

## 我是谁
- 角色：<agent> · 领域：<domain>

## 长期事实（稳定，跨会话）
| 事实 | 来源层 | 写入日期 |
|---|---|---|
| 用户偏好：结论优先、证据齐备 | L3 | 2026-09-20 |
| 项目代号：鲲界 | L2 | 2026-09-15 |

## 当前承诺（从 L3 同步，最高优先级）
- [ ] 每周一 09:00 出训练进展（承诺日 2026-09-25）

## 索引用法
- 需要"今天发生了什么" → 读 memory/daily/<今日>.md
- 需要"我答应过什么" → 读 memory/prospective/
- 需要"这周总结" → 读 memory/review/
- 需要"这条记忆谁写的" → grep memory/provenance.jsonl
```

**Step 3 · 各层样例文件（照抄，注意分层职责不混）**：

`memory/daily/2026-09-27.md`（L2 日志态 · 当日流水）：

```markdown
---
layer: L2
kind: episodic-log
date: 2026-09-27
---
# 2026-09-27 日志
- 09:12 完成 C4-1 训练轮次计划文件落盘（evidence/R-01）
- 11:40 用户交代 3 条偏好，已写入 L3 prospective
- 15:05 compaction 触发，flush 前已把"用户偏好"写回 L3（未丢）
```

`memory/prospective/2026-09-27-承诺.md`（L3 备忘态 · 承诺/待办）：

```markdown
---
layer: L3
kind: prospective
created: 2026-09-27
due: 2026-10-04
status: open
---
# 承诺：每周一出训练进展
- 承诺对象：用户
- 触发方式：cron 每周一 09:00（见 C5-3）
- 关闭条件：连续 4 周准时产出
```

`memory/review/2026-W39.md`（L4 复盘态 · 周度 recap）：

```markdown
---
layer: L4
kind: review
week: 2026-W39
derived_from: [memory/daily/2026-09-22.md, memory/daily/2026-09-27.md]
---
# W39 复盘
- 本周稳定项：训练轮次执行 3/3
- 本周漂移项：R-01 第 4 问风格变长（已入问题账本 P-002）
- 回流 L1：把"结论优先"确认为长期事实
```

`memory/provenance.jsonl`（L5 永恒态 · 只追加，每行一条）：

```json
{"ts":"2026-09-27T09:12:00+08:00","layer":"L2","path":"memory/daily/2026-09-27.md","writer":"<agent>","reason":"记录当日训练轮次完成","hash":"sha256:0000"}
{"ts":"2026-09-27T11:40:00+08:00","layer":"L3","path":"memory/prospective/2026-09-27-承诺.md","writer":"user","reason":"用户显式交代偏好","hash":"sha256:0000"}
```

> **hash 说明**：真实部署时 `hash` 用产物 SHA-256（见 C5-4 防腐三机制），
> 上例填 `sha256:0000` 仅为结构示范，**复制后必须替换为真实哈希**。

**Step 4 · 写入 `compaction.flush` 配置**（三者并存真名，整段不得省略）：

```yaml
# 路径：~/.openclaw/workspace/agents/workspace-<agent>/config/compaction.yaml
# 真名基线：OpenClaw 2026.9.4
compaction:
  flushPlan:                              # 类型真名：MemoryFlushPlan
    softThresholdTokens: 80000            # 软阈：到 80k 提示"该刷了"
    forceFlushTranscriptBytes: 300000     # 硬阈：到 300k 强 flush
    reserveTokensFloor: 20000             # ① 字段：flush 后最少给近期消息留 2 万 token
                                          #    （默认来自常量 RESERVE_TOKENS_FLOOR = 2e4）
  maxCompactionReserveRatio: 0.25         # ③ 常量：MAX_COMPACTION_RESERVE_RATIO = 0.25（不可配置比率上限）
```

## 验证步骤

```bash
cd ~/.openclaw/workspace/agents/workspace-<agent>

# 1. 目录树 5 层齐备
for p in memory/MEMORY.md memory/daily memory/prospective memory/review memory/provenance.jsonl; do
  [ -e "$p" ] && echo "✅ $p" || echo "❌ $p 缺失"
done
# 期望：五行全 ✅

# 2. L1 ≤ 30% 记忆块校验（本机以"L1 行数 / 全部 memory 行数"近似）
L1=$(wc -l < memory/MEMORY.md)
ALL=$(find memory -name '*.md' -exec cat {} + | wc -l)
python3 -c "
l1,all_=$L1,$ALL
r=l1/all_ if all_ else 0
print(f'L1 占比 ≈ {r:.0%}（阈值 ≤ 30%）')
print('✅ 通过' if r<=0.30 else '⚠ 超出：把明细从 L1 下移到 L2/L4')
"

# 3. 每层 frontmatter layer 字段与所在目录一致
python3 - <<'PY'
import glob, yaml, os
EXPECT = {"MEMORY.md":"L1","daily":"L2","prospective":"L3","review":"L4"}
bad=0
for f in glob.glob("memory/**/*.md", recursive=True):
    t=open(f,encoding="utf-8").read()
    if not t.startswith("---"): continue
    meta=yaml.safe_load(t[4:t.index("\n---",3)])
    key = os.path.basename(f) if os.path.dirname(f).endswith("memory") else os.path.basename(os.path.dirname(f))
    want = EXPECT.get(key if key=="MEMORY.md" else key)
    got = meta.get("layer")
    ok = (want is None) or (got==want)
    if not ok: bad+=1
    print(f"{'✅' if ok else '❌'} {f} layer={got} 期望={want}")
print("全部一致" if bad==0 else f"{bad} 处不一致")
PY

# 4. L5 provenance 每行是合法 JSON
python3 -c "
import json,sys
n=0
for i,line in enumerate(open('memory/provenance.jsonl',encoding='utf-8'),1):
    line=line.strip()
    if not line: continue
    try: json.loads(line); n+=1
    except Exception as e: sys.exit(f'❌ 第{i}行非法 JSON: {e}')
print(f'✅ provenance {n} 行全部合法')
"

# 5. flush 配置可解析且三真名齐
python3 - <<'PY'
import yaml
d=yaml.safe_load(open("config/compaction.yaml",encoding="utf-8"))
fp=d["compaction"]["flushPlan"]
assert fp["softThresholdTokens"]==80000, "❌ softThresholdTokens"
assert fp["forceFlushTranscriptBytes"]==300000, "❌ forceFlushTranscriptBytes"
assert fp["reserveTokensFloor"]==20000, "❌ reserveTokensFloor 必须是 20000（=RESERVE_TOKENS_FLOOR 2e4）"
assert d["compaction"]["maxCompactionReserveRatio"]==0.25, "❌ MAX_COMPACTION_RESERVE_RATIO"
print("✅ flushPlan 三真名并存：字段 20000 / 常量 2e4 / 比率 0.25")
PY

# 6. 跨 compaction 记忆回读测试（人工）
#    第 1 次会话交代偏好 → 触发 compaction → 第 2 次会话问"我交代过什么"
openclaw agent --agent <agent> --message "请记住：我的三条偏好是①结论优先②证据齐备③不确定就标。"
openclaw agent --agent <agent> --message "我交代过什么偏好？逐条复述。"
# 期望：第 2 次会话完整复述 3 条（说明 flush 把它写回了 L3，未随 compaction 丢失）
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **真名来源**：`MemoryFlushPlan`（`agent-harness-runtime-*.d.ts`，本次实拉命中 6 处
  cross-file 出现）；`DEFAULT_AGENT_COMPACTION_RESERVE_TOKENS_FLOOR = 2e4`
- **修正台账**：v3.0 改名表 §五第 31 项称 `reserveTokensFloor` "不存在"；v4.0 经
  本机源码 grep **实测证伪**（14 处命中）。本配方采用 v4.0 勘误结论。
- **OS**：macOS 26.5.1 · **日期**：2026-09-27
- **来源基线**：v4.0 卷五模块 1（L1–L5 金字塔 + 四可原则 + flushPlan 真名）

## 排坑

1. **L1 膨胀**：把每日流水全塞进 `MEMORY.md`，启动时加载不全。核验：
   验证步骤 2 的占比 > 30% → 把明细下移到 L2/L4，L1 只留索引 + 长期事实。

2. **压缩前不刷写**：Agent 记住了偏好，一次 compaction 后集体失忆。
   铁律：**压缩前刷写 ≠ 压缩后写回**。核验：把"每条承诺必须在 flush 前写入 L3"
   写进 AGENTS.md；验证步骤 6 是回归测试。

3. **`reserveTokensFloor` 误植**：照抄旧结论写成"该字段不存在"，于是配了错的键。
   核验：验证步骤 5，三真名必须齐（字段 20000 / 常量 2e4 / 比率 0.25）。

4. **层级混用**：把承诺写进 L2 日志。后果是"这周答应的事"永远找不到。
   核验：`EXPECT` 映射（daily→L2 / prospective→L3 / review→L4）；验证步骤 3 会逐文件报错。

5. **L5 provenance 被 Agent 自己写**：provenance 是**审计痕迹**，必须由用户或治理接口写入，
   Agent 主动写 = 越权（对照 C5-2 的 Forbidden 档：`memory.write.L5.provenance`）。
   核验：`grep -c '"writer":"<agent>"' memory/provenance.jsonl` 应为 0。

6. **provenance 追加非法行**：手工编辑 jsonl 时漏逗号/多换行，整文件解析失败。
   核验：验证步骤 4 逐行 `json.loads`。铁律：provenance 只追加，不原地改。

## 进阶

- **进阶 1 · 记忆与漂移治理联动**：L5 provenance 是漂移治理（Drift Governance）
  的审计痕迹——当 C5-1 的 drift_scan 报"锚点缺失"，可回到 provenance 查"谁在何时
  改掉了哪条锚点"。这两层天然是一对。

- **进阶 2 · L4 复盘自动回流**：加一条 cron（见 C5-3），每天把 L2 提炼进 L4，
  每周把 L4 精选回 L1。这样"越用越聪明"有了一条**自动化回流管线**，
  而不是靠人手动整理。

- **进阶 3 · 分层记忆写入纪律入 SOP**：把"什么信息写哪一层"做成一张决策表
  （事实→L1 / 流水→L2 / 承诺→L3 / 总结→L4 / 审计→L5），写进 AGENTS.md。
  记忆质量的上限，就是这个 SOP 的清晰度。

- **进阶 4 · 记忆对位业界 4 框架**：LangMem / Mem0 / Zep / Letta(MemGPT) 四框架
  共有的 30% 重叠集中在 L1 + L2（结构化事实 + 会话事件）；**L3 承诺 / L4 复盘 /
  L5 溯源是本书的护城河补全**。Letta 的 `self-edit memory` 是"记忆可编辑"，
  不是"行为是否还像自己"——这正是记忆管理与漂移治理的关键分野。

---

## 附录 · 5 层写入决策表 + 各层容量预算

### 附表 A · 「这条信息写哪一层」决策表

| 信息类型 | 目标层 | 判据 | 反例（写错会怎样） |
|---|:--:|---|---|
| 稳定事实（用户偏好、长期结论） | L1 | 跨会话不变、需首启加载 | 写进 L2 → 每次会话找不到 |
| 当日流水（做了什么、何时） | L2 | 时效性强、明细多 | 写进 L1 → L1 膨胀超 30% |
| 承诺 / 待办 / 提醒 | L3 | 有 due、有 open/closed 状态 | 写进 L2 → "答应过的事"永远找不到 |
| 周期总结（日/周/月 recap） | L4 | 从 L2 提炼、可回流 L1 | 不建 L4 → 每周都要从头读流水 |
| 审计痕迹（谁写、何时、为何） | L5 | 只追加、不可改 | 让 Agent 自写 → 越权（C5-2 Forbidden） |

### 附表 B · 各层容量预算（软约束）

| 层 | 载体 | 预算 | 越界后果 | 拦截/处置 |
|:--:|---|---|---|---|
| L1 | `MEMORY.md` | ≤ 记忆块 30% | 启动加载不全，后面全被剪 | 占比校验（验证步骤 2） |
| L2 | `memory/daily/*.md` | 单文件 ≤ 200 行 | 单日日志过长 | 日终归档到 L4 |
| L3 | `memory/prospective/*.md` | 单文件 ≤ 80 行 | 承诺文件难扫 | 关闭后移入 L4 |
| L4 | `memory/review/*.md` | 单文件 ≤ 150 行 | 复盘膨胀 | 精选回流 L1 |
| L5 | `provenance.jsonl` | 无上限（只追加） | — | 周度归档（C5-3 W2） |

### 附表 C · flush 三真名记忆卡

```text
① 字段  reserveTokensFloor = 20000      （可配置，内存刷写下限）
② 常量  RESERVE_TOKENS_FLOOR = 2e4       （默认值，= 20000）
③ 比率  MAX_COMPACTION_RESERVE_RATIO = 0.25 （不可配置的比率上限）
```

> 三真名**同时存在、同时生效**。凡看到"`reserveTokensFloor` 不存在"的说法，
> 均为旧结论，以本卡为准（v4.0 卷四真名勘误，本机源码 grep 14 处命中）。

### 附表 D · 跨 compaction 不失忆的最小动作

```text
1. 把"每条承诺在 flush 前写入 L3"写进 AGENTS.md
2. flushPlan 三真名配齐（附表 C）
3. 每日跑一次"回读测试"（C4-1 R-03 的验证方式）
4. L5 provenance 记录每次写入（谁写、何时、为何）
5. 每周体检把"承诺失忆率"入漂移分（权重 0.20）
```

---

# 诚实边界声明（本分册）

> 本声明遵循 v5.0 方案的「诚实边界」原则：标注实测 / 待实测，不把推测写成事实。

## 一、已实测（✅）

| 内容 | 证据 | 状态 |
|---|---|---|
| 基座版本 `OpenClaw 2026.9.4 (3a9d69d)` | 本机 `openclaw --version` 实测输出 | ✅ 实测 |
| 网关版本 `Hermes 0.20.1` | 本机网关版本输出 | ✅ 实测 |
| OS `macOS 26.5.1` | `sw_vers` | ✅ 实测 |
| 技能库 236 个 | `ls -d ~/.openclaw/workspace/skills/*/ \| wc -l` = **236**（`ls \| wc -l` = 238，含 2 非技能条目） | ✅ 实测 |
| agent 工作区 18 个 | `ls -d ~/.openclaw/workspace/agents/workspace-*/` = 18（baxia…zhuque） | ✅ 实测 |
| 压缩真名 `MemoryFlushPlan` + `reserveTokensFloor` 字段 | v4.0 卷四真名勘误（本机源码 grep 14 处命中） | ✅ 核实 |
| 常量 `RESERVE_TOKENS_FLOOR = 2e4` + `MAX_COMPACTION_RESERVE_RATIO = 0.25` | v4.0 卷四真名验证；三者并存 | ✅ 核实 |
| 进化阶梯 L0–L6 / 别名 Malleable/Usable/Stable/Proactive/Legion/Expert Agent | v4.0 卷四模块 1 | ✅ 有据 |
| 训练轮次六要素（单一目标/匹配强度/明确任务/证据交付/验收口径/沉淀动作） | v4.0 卷四模块 4 | ✅ 有据 |
| 双三角模型：（专业深度/工具广度/创造性）×（稳定性/可控性/可预期性）+ 三张力 | v4.0 卷四模块 5 | ✅ 有据 |
| Mentor Agent 四职责 + 三段式反馈 + 沉淀三动作 | v4.0 卷四模块 3 | ✅ 有据 |
| L1–L5 金字塔 + 四可原则 | v4.0 卷五模块 1 | ✅ 有据 |
| 各 YAML/JSON 校验脚本逻辑（`yaml.safe_load` / `json.loads`） | 纯本地可复现逻辑 | ✅ 可复现 |
| 训练计划 / 双三角 YAML + `dual-triangle.py` 实跑 | 本机实跑：cap=3.00 / rel=2.67 / Usable / 张力 T1+T2 | ✅ 实测 |
| `compaction.yaml` 三真名解析（字段/常量/比率） | 本机 `yaml.safe_load` 通过 | ✅ 实测 |
| 18 个 agent 工作区清单（baxia…zhuque） | `ls -d .../workspace-*/` 实测 | ✅ 实测 |

## 二、待实测（⏳）

| 内容 | 说明 | 状态 |
|---|---|---|
| 单轮对话命令真名 | ✅ 已实测：`openclaw agent --agent <id> --message "<text>"`（`openclaw chat` = 本地 TUI） | ✅ 已实测 |
| 导师智能体与被训者的双工作区隔离在 2026.9.4 的确切口径 | C4-3；当前为手动观训 + 落盘 | ⏳ 待实测 |
| L1 ≤ 30% 记忆块的**精确**计量口径（本配方用行数近似） | C4-4 验证步骤 2 | ⏳ 待实测 |
| `config/compaction.yaml` 是否为 2026.9.4 原生读取路径 | 键名真名已核实，路径为本书约定 | ⏳ 待实测 |
| C4-4 验证步骤 6「跨 compaction 回读」在本机的端到端结果 | 依赖真实 compaction 触发 | ⏳ 待实测 |
| 训练记录三证入 Merit Ledger 的接口形态 | C4-3 进阶 2 | ⏳ 待实测 |

## 三、诚实说明

1. 本分册所有配置（训练计划 YAML / 评分脚本 / 导师协议 / 记忆目录树 / flush 配置）
   均**基于 v4.0 卷四/卷五已实测事实 + 本机真实工作区形态**从零撰写；
   YAML/JSON 结构为本书约定，零 `...` 省略。
2. 凡标注 ⏳ 的条目**未在本机 2026.9.4 完成端到端验证**，以 `openclaw --help`
   与官方文档为最终依据；若你的实测不同，以你的实测为准并回报勘误。
3. 所有命令均给出「期望输出」；期望输出是**设计目标**，不是抓包实录。
4. 本分册**不复用 v1.0 / v4.0 原文**，全部配方从零撰写；引用的真实事实（版本号、
   技能数、agent 数、真名勘误）均逐条注明来源。
5. 本分册**不重写 01/02/03 分册**；四册共用同一 banner 与 6 段式结构，
   交叉引用处只给例号（如 C4-1、C5-1），不复述正文。
6. 分层记忆的 `hash` 示例值 `sha256:0000` 为结构示范，复制后必须替换为真实哈希。

**勘误途径**：本手册主目录 `../README.md`；术语口径以
`../00-术语对照表·v3.0行业标准版.md` 为准。

---

> 《硅基生命训练学 v5.0 · 实战 Cookbook》
> 分册：04-training-rounds.md（例 C4-1 ~ C4-4）
> 基座：OpenClaw 2026.9.4 (3a9d69d) · 网关 Hermes 0.20.1
> License: MIT · Copyright (c) 2026 OpenClaw Foundation
> 撰写日期：2026-09-27

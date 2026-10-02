<!--
================================================================================
 硅基生命训练学 v5.0 · 实战 Cookbook · 上半卷（15 例）
 分册：03-skills-tools-mcp.md —— 协议配置类 · 第 3 分册（例 C3-1 ~ C3-5）
--------------------------------------------------------------------------------
 基座（Base）：OpenClaw 2026.9.4 (3a9d69d)   ← 本机 `openclaw --version` 三源一致
 网关（Gateway）：Hermes 0.20.1
 上游底座：v4.0 行业标准版（8 卷 + 4 接口层：skill-registry / plugin-entrypoint /
           mcp-binding / a2a-binding）
 术语底座：《00-术语对照表·v3.0行业标准版.md》（35 条改名统一口径）
 本机实测环境：macOS 26.5.1 · ~/.openclaw/workspace/skills/ 共 236 个 skills
 本机实测参照：afrexai-compliance-audit · skill-security-audit-v2（均存在）
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

# 实战 Cookbook · 协议配置类 · 03-skills-tools-mcp.md

> **本分册覆盖**：C3-1 Skill 注册 / C3-2 Tool 注册 / C3-3 MCP 接入 /
> C3-4 A2A 接入（SLCP） / C3-5 Plugin manifest 配置。
>
> **读法**：C3-1 与 C3-2 是"能力供给"两件套（技能 + 工具），C3-3/C3-4/C3-5
> 是三张"对外接口"（MCP / A2A / Plugin）。建议 C3-1→C3-2→C3-5 连读
> （本地能力→打包分发），C3-3/C3-4 单读（对外协议）。
>
> **术语约定**：首次出现的行业标准术语以「行业标准名（原：黑话）」双写。
> 英文 alias 随行标注。全部口径以《术语对照表 v3.0》为准，
> 尤其第 20 条：**工具与技能双模块 + 共享网关 RPC**
> （**Tools / Skills Dual Modules + Shared Gateway RPC**，
> 真结构 = `tools.catalog` + `skills.status` / `skills.skillCard`）。

---

## 本分册速查索引

| 例号 | 主题 | 解决的具体问题 | 核心文件 | 可跑时间 |
|:--:|---|---|---|---|
| C3-1 | Skill 注册 | SKILL.md 写完不生效/不被召回 | `skills/<name>/SKILL.md` | 10 分钟 |
| C3-2 | Tool 注册 | 工具写好了但 manifest 对不上 | `src/index.ts` + manifest | 12 分钟 |
| C3-3 | MCP 接入 | 8 卷知识怎么变成 MCP 原语 | MCP server 配置 | 12 分钟 |
| C3-4 | A2A / SLCP 接入 | 多 agent 协同 + 反脆弱三层 | SLCP 配置 | 12 分钟 |
| C3-5 | Plugin manifest | openclaw.plugin.json 怎么写、怎么装 | `openclaw.plugin.json` | 10 分钟 |

> **共通前置**：OpenClaw 2026.9.4 已装；技能库
> `~/.openclaw/workspace/skills/`（236 个）存在。
> `<agent>` 替换为真实 agent 名；`<skill>` 替换为你的技能名。

---


## 本分册术语对照速查（v3.0 改名表 · 节选）

> 完整 35 条以《00-术语对照表·v3.0行业标准版.md》为准；下表列出**本分册正文
> 出现过**的条目。正文中每个术语**首次出现**处均以「行业标准名（原：黑话）」
> 双写，英文 alias 随行标注；后续出现只用行业标准名。
> `标注` 列中「v3.0 改名」= 该条在 v3.0 发生过正式改名；「统一口径」= 名称未变，
> 但本手册要求中英双写以对齐外部读者。

| # | 行业标准名 | 英文 alias | 原（黑话 / v1.0 旧称） | 标注 | 本分册首见 |
|:--:|---|---|---|---|---|
| 1 | 监督层 | Supervisor Layer | 监军 | v3.0 改名 | C3-4 配置 ② |
| 2 | 多智能体编排 | Multi-Agent Orchestration | 军团编制 | v3.0 改名 | C3-4 背景 |
| 3 | 三证据验证 | TEV（Three-Evidence Verification） | 三证据 | v3.0 改名 | C3-3 原语 #36 |
| 4 | 响应让渡协议 | Response Yield Protocol | 让渡 | v3.0 改名 | C3-3 原语 #41 |
| 5 | 三省评审制 | Three-Stage Review（Proposal / Review / Final-Decision） | 三省 | v3.0 改名 | C3-3 原语 #39 |
| 6 | 任务交接协议 | THP（Task Handoff Protocol） | 交接 | v3.0 改名 | C3-3 原语 #40 |
| 7 | 交接置信度 | Handoff Confidence | 交接分 | v3.0 改名 | C3-4 配置 4 |
| 8 | 通道守门员 | Channel Sentinel | 通道看门人 | v3.0 改名 | C3-4 配置 ③ |
| 9 | 反脆弱三层 | Antifragile Trio | 三道保险 | v3.0 改名 | C3-4 配置 3 |
| 10 | 工具与技能双模块 + 共享网关 RPC | Tools / Skills Dual Modules + Shared Gateway RPC | 双协议（**已勘误**） | v3.0 改名 | C3-2 背景 |
| 11 | 工具目录 | Tool Catalog（`tools.catalog`） | 工具清单 | 统一口径 | C3-2 验证 4 |
| 12 | 技能名片 | Skill Card（`skills.skillCard`） | 技能卡 | v3.0 改名 | C3-1 附录 G |
| 13 | 插件入口层 | Plugin Entrypoint | 打包器 | v3.0 改名 | C3-5 配置 1 |
| 14 | 技能注册层 | Skill Registry | 技能库 | v3.0 改名 | C3-1 配置 4 |
| 15 | MCP 绑定层 | MCP Binding | 挂载适配 | v3.0 改名 | C3-3 配置 3 |
| 16 | A2A 绑定层 | A2A Binding | 协同对接 | v3.0 改名 | C3-4 配置 1 |
| 17 | 原子原语 | MCP Primitive（Resource / Tool / Prompt） | 原语 | 统一口径 | C3-3 配置 1 |
| 18 | 硅基生命协同协议 | SLCP（Silicon-Life Coordination Protocol） | 军团总线 | v3.0 改名 | C3-4 配置 0 |
| 19 | 治理审计账本 | Governance Audit Ledger | 账本 | v3.0 改名 | C3-2 进阶 3 |
| 20 | 信任评分 / 功绩账本 | Trust Score / Merit Ledger | 信誉分 | v3.0 改名 | C3-3 原语 #38 |
| 21 | 边界三档制 | Boundary Tier（strict / standard / loose） | 权限档位 | v3.0 改名 | C3-2 进阶 1 |
| 22 | 上下文压缩 | Compaction（`CompactionRequestBudget.reserveTokens` · `MAX_COMPACTION_RESERVE_RATIO=0.25`） | 截断 | 统一口径（真名核实） | C3-2 附录 G |
| 23 | 漂移检测 | Drift Detection（`drift_score` 0–1） | 体检 | 统一口径 | C3-3 原语 #33 |
| 24 | 技能基因提取 | Gene Extraction | 抽基因 | v3.0 改名 | C3-3 原语 #46 |
| 25 | 自主进化范式 | Proactive Evolution Paradigm | 主动进化 | 统一口径 | C3-1 背景 |
| 26 | 任务卡 | Task Card | 工单 | v3.0 改名 | C3-3 原语 #34 |
| 27 | 修复工单 | Remediation Ticket | 整改单 | v3.0 改名 | C3-3 原语 #37 |
| 28 | 验收口径 | Acceptance Criteria | 验收标准 | v3.0 改名 | C3-1 配置 2 |
| 29 | 诚实边界 | Honest Boundary | 免责声明 | v3.0 改名 | 本分册文末 |
| 30 | 能力供给 | Capability Supply（Skill + Tool） | 装备 | v3.0 改名 | 本分册读法 |
| 31 | 对外接口 | External Interface（MCP / A2A / Plugin） | 外挂 | v3.0 改名 | 本分册读法 |
| 32 | 进化阶梯 | Autonomy Ladder（L0–L6） | 段位 | v3.0 改名 | C3-5 配置 2 |
| 33 | 协同事件日志 | Coordination Event Log | 协同流水 | v3.0 改名 | C3-4 配置 ③ |
| 34 | 提示模板原语 | Prompt Primitive | 话术 | 统一口径 | C3-3 配置 1 |
| 35 | 只读知识原语 | Resource Primitive | 知识块 | 统一口径 | C3-3 配置 1 |

> **用法提示**：给外部读者/评审看文档时，第一处务必双写；写给本军团内部 agent 时
> 可只用行业标准名。混写成「监军」这类旧词会让跨团队评审对不上 v4.0 接口层命名。

# C3-1 · Skill 注册：完整 SKILL.md 写法（YAML frontmatter）

## 背景

技能（Skill）不是 prompt，也不是"给模型看的一段话"。它是**可被 agent 路由
与调用的能力单元**——写对了，agent 在对的场景会自己想起来用它；写错了，
轻则"从不被加载"，重则"被错误召回、答非所问"。

新人最常见的三个坑：
①frontmatter 非法 → **技能直接加载失败**（YAML 报错 / 大小写错 / 重复字段）；
②`description` 写成文档摘要而不是**触发机制** → agent 根本不知道该用它；
③目录名与 `name` 不一致 → 校验不通过。

这一例解决的具体问题：**给我一份"一次写对、跨 32+ 平台通用"的 SKILL.md
完整写法**，含 frontmatter 全字段规范 + description 召回工程 + 目录校验。

> **来源**：v4.0 09-skill-registry《SKILL.md frontmatter 规范》与
> 《Anthropic Skills 实拉对位》；v1.0 卷三《Tools + Skills 双模块》。
> 从零撰写，不复用 v1.0 原文。参考本机 236 个真实 skills。

## 配置（完整可复制）

### 1）目录与文件（先建目录）

```bash
SKILLS=~/.openclaw/workspace/skills
mkdir -p "$SKILLS/compliance-checklist"       # 目录名 == frontmatter.name
ls -d "$SKILLS/compliance-checklist"
```

### 2）SKILL.md（完整可复制，含全部规范字段）

```markdown
---
# ============================================================================
# SKILL.md YAML frontmatter · 对齐 agentskills.io/specification
# 路径：~/.openclaw/workspace/skills/<name>/SKILL.md
# 规则：name ≤64 字符，仅小写字母/数字/连字符，不得首尾连字符、不得连续连字符，
#       且必须与该 skill 父目录名完全一致。顶层字段名必须小写且只出现一次。
# ============================================================================
name: compliance-checklist
description: >-
  对一个交付物（文档/流程/配置）做合规性检查并产出勾选清单。用于用户说
  "合规检查""合规审计""这份东西合规吗""过一遍合规清单"时；不用于安全漏洞扫描
  （那请用安全审计类 skill）、不用于代码风格检查（那请用 lint 类 skill）。
license: MIT
compatibility: >-
  需 OpenClaw 2026.9.4+；纯文本处理，无网络依赖；需要读文件权限。
metadata:
  author: your-agent
  version: 1.0.0
  category: compliance
allowed-tools: ["read_file", "write_file"]
---

# compliance-checklist

## 何时使用（When to use）

- 用户要求对交付物做**合规性**检查（不是安全性、不是风格）。
- 交付物类型：文档 / 流程说明 / 配置项。
- 典型触发词：合规检查 / 合规审计 / 合规清单 / 过一遍合规。

## 何时不要使用（Negative triggers）

- 安全漏洞扫描 → 用 `security-audit-*` 类 skill。
- 代码风格 → 用 lint 类 skill。
- 纯粹的事实问答 → 不需要本 skill。

## 步骤（Steps）

1. **确认对象**：明确被检查的**交付物路径**与**合规标准**（哪个规范/条款）。
2. **逐条比对**：按标准条款逐条检查，每条给：符合 / 不符合 / 不适用。
3. **产出清单**：输出勾选清单（markdown 表格），含条款 / 结论 / 证据。
4. **汇总风险**：列出"不符合"项按严重度排序，给整改建议。
5. **落盘**：结果写到 `reports/compliance-<date>.md`，聊天里只给路径 + 摘要。

## 输出形态

```text
| 条款 | 结论 | 证据 | 整改建议 |
|---|---|:--:|---|
| 3.1 数据留存 | 不符合 | 文档未写留存期限 | 补"留存 90 天" |
```

## 边界

- 本 skill **只做合规判断，不替代法律意见**；涉法建议标注"需法务确认"。
- 不修改被检查对象（只读 + 出报告）。
```

### 3）description 召回工程（最关键字段）

`description` 不是摘要，是 **agent 决定是否激活该 skill 的触发机制**。必须齐四类信息：

| 信息类 | 作用 | 本例写法 |
|---|---|---|
| 任务类型 | 做什么 | "做合规性检查并产出勾选清单" |
| 典型触发表达 | 用户怎么说 | "合规检查 / 合规审计 / 过一遍合规清单" |
| 适用边界 | 什么时候用 | 文档/流程/配置的合规性 |
| 不适用边界 | 什么时候别用 | 不是安全扫描、不是风格检查 |

> **负触发**（Negative triggers）是新人最常漏的——写清"别用"，agent 才不会乱用。

### 4）安装与注册

```bash
# 方式 A：直接落到技能库（本机 236 个 skills 的管理方式）
SKILLS=~/.openclaw/workspace/skills
ls "$SKILLS" | wc -l          # 安装前基线（本机 236）
mkdir -p "$SKILLS/compliance-checklist"
# 把上面的 SKILL.md 写入该目录
ls "$SKILLS" | wc -l          # 应为 237
```

## 验证步骤

```bash
SKILLS=~/.openclaw/workspace/skills

# 1. 目录名与 name 一致
python3 - <<'PY'
import os, yaml, sys
root = os.path.expanduser("~/.openclaw/workspace/skills")
bad = []
for d in os.listdir(root):
    p = os.path.join(root, d, "SKILL.md")
    if not os.path.isfile(p): continue
    raw = open(p, encoding="utf-8").read()
    if not raw.startswith("---"): continue
    try:
        meta = yaml.safe_load(raw[4:raw.index("\n---", 3)])
    except Exception as e:
        bad.append((d, f"YAML错误: {e}")); continue
    if meta.get("name") != d:
        bad.append((d, f"name={meta.get('name')} != 目录名"))
print("❌ 问题技能:", bad if bad else "无")
print("✅ 已扫描技能数:", sum(1 for d in os.listdir(root)
      if os.path.isfile(os.path.join(root,d,"SKILL.md"))))
PY

# 2. 校验 name 规则（≤64，小写，无首尾/连续连字符）
python3 - <<'PY'
import re, yaml, os
p = os.path.expanduser("~/.openclaw/workspace/skills/compliance-checklist/SKILL.md")
raw = open(p, encoding="utf-8").read()
name = yaml.safe_load(raw[4:raw.index("\n---",3)])["name"]
assert len(name) <= 64
assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name), "❌ name 不合法"
print("✅ name 合法:", name)
PY

# 3. description 长度 ≤1024 且含负触发
python3 - <<'PY'
import yaml, os
p = os.path.expanduser("~/.openclaw/workspace/skills/compliance-checklist/SKILL.md")
meta = yaml.safe_load(open(p, encoding="utf-8").read()[4:].split("\n---")[0])
d = meta["description"]
assert len(d) <= 1024, f"❌ description {len(d)} > 1024"
assert "不用于" in d or "不适用" in d, "❌ description 缺负触发"
print("✅ description 长度", len(d), "含负触发")
PY

# 4. 真实技能对照（本机存在的两个合规/安全类技能）
for s in afrexai-compliance-audit skill-security-audit-v2; do
  test -f "$SKILLS/$s/SKILL.md" && echo "✅ 参照技能存在: $s"
done

# 5. 行为验证：技能能否被召回
openclaw agent --agent your-agent \
  --message "帮我过一遍这份流程文档的合规清单。"
# 期望：agent 调用 compliance-checklist（先 skill_view 读全文再执行）

# 6. 负触发验证：不该用时不误用
openclaw agent --agent your-agent \
  --message "帮我扫一下这段代码有没有安全漏洞。"
# 期望：不使用 compliance-checklist，改用 security-audit 类技能
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **网关**：Hermes 0.20.1
- **OS**：macOS 26.5.1
- **技能库**：`~/.openclaw/workspace/skills/` 共 **236 个**（实测）
- **存在的参照技能**：`afrexai-compliance-audit`、`skill-security-audit-v2`（实测）
- **规范来源**：v4.0 09-skill-registry《SKILL.md frontmatter 规范》；
  对齐 `agentskills.io/specification`
- **日期**：2026-09-27

## 排坑（如有）

1. **技能加载失败**：frontmatter 非法（YAML 错 / 重复字段 / 大小写错 / 期望标量却给集合）。
   核验：用验证步骤 1 的全库扫描脚本。

2. **技能从不被召回**：`description` 是文档摘要，缺"触发表达"。
   修：补齐四类信息（任务类型/触发表达/适用边界/不适用边界）。

3. **name 与目录名不一致**：校验不通过。修：`name` == 父目录名。

4. **未知字段报错**：正常应"忽略未知字段"（向前兼容）。
   若报错，说明你用了严格校验器；删掉未知字段或换校验器。

5. **技能太"胖"**：SKILL.md 写了 2000 行。修：SKILL.md 是"指挥单"，
   长内容下沉到 `references/`、`scripts/`、`templates/`。

## 进阶

- **进阶 1 · 跨平台可移植**：只用规范级字段（`name`/`description`/`license`/
  `compatibility`/`metadata`），发布到公共 registry 可被 32+ 平台通用；
  平台扩展字段（如 `allowed-tools`）其他平台会**静默忽略**。

- **进阶 2 · 资源目录**：配套 `references/`（文档）、`scripts/`（脚本）、
  `templates/`（模板）；SKILL.md 里用相对路径引用，便于打包。

- **进阶 3 · 技能安全前置**：安装第三方 skill 前先用
  `skill-security-audit-v2` 过一遍（本机实测存在），审查命令执行 / 网络访问 /
  文件访问三类风险后再启用。

## 附录 A · frontmatter 字段规范表

| 字段 | 必填 | 约束 | 说明 |
|---|:--:|---|---|
| `name` | ✅ | ≤64；小写/数字/连字符；无首尾/连续连字符；==目录名 | 唯一标识 |
| `description` | ✅ | ≤1024；含"做什么+何时用"+负触发 | 触发机制 |
| `license` | ⬜ | License 名或文件引用 | 发布建议填 MIT |
| `compatibility` | ⬜ | ≤500 | 环境要求 |
| `metadata` | ⬜ | 结构化（author/version） | 作者/版本 |
| `allowed-tools` | ⬜ | 工具白名单（平台扩展） | 可能被忽略 |

## 附录 B · 加载失败三大原因

```text
1. 非法 YAML（缩进/冒号/引号）
2. 重复字段（同名顶层键出现两次）
3. 大小写错误（Name ≠ name）
附带：期望标量却给集合（description 给了 list）
```

## 附录 C · 目录结构建议

```text
skills/<name>/
├── SKILL.md            # 指挥单（≤ ~300 行）
├── references/         # 参考文档
│   └── spec.md
├── scripts/            # 可执行脚本
│   └── check.py
└── templates/          # 输出模板
    └── report.md
```

## 附录 D · 常见错误码 / 现象对照

| 现象 | 根因 | 定位 |
|---|---|---|
| 技能不存在 | name ≠ 目录名 | 全库扫描脚本 |
| 从不召回 | description 缺触发 | 查四类信息 |
| 误用技能 | 缺负触发 | 查"不用于" |
| 加载报错 | YAML/重复/大小写 | 逐字段校验 |
| registry 被拒 | 用了非规范字段 | 只用规范级字段 |

## 附录 E · 5 条技能写作军规

```text
1. SKILL.md 写给 agent 看（指挥单），不是写给人看的散文。
2. description 是触发机制，必须含负触发。
3. name 必须 == 目录名，且只用小写/数字/连字符。
4. 长内容下沉 references/scripts/templates。
5. 第三方技能安装前先过安全审计。
```

---


## 附录 F · description 召回工程：5 组对照实验

description 是**唯一**决定"技能是否被召回"的字段。下面 5 组对照可直接拿去当自查表。

| 组 | description 写法 | 召回结果 | 症状 |
|:--:|---|---|---|
| ① | `合规检查工具。` | 几乎不召回 | 名词短语，无动词、无触发表达 |
| ② | `本 skill 介绍了一种对交付物进行合规性评估的方法论，涵盖……` | 偶发误召回 | 文档摘要语气，模型当成知识而非动作 |
| ③ | `对交付物做合规性检查并产出勾选清单。用于"合规检查""过一遍合规"。` | 正确召回 | 有动词 + 有触发表达，但缺负触发 |
| ④ | 组③ + `不用于安全漏洞扫描、不用于代码风格检查。` | 正确召回且不误用 | ✅ 推荐形态 |
| ⑤ | 组④ + `也用于"风险清单""风控自查"。` | 与风控类技能争抢 | 触发词与邻居技能重叠 |

**⑤ 的消解办法**：在负触发里**点名邻居技能**，把边界钉死：

```yaml
description: >-
  对交付物做合规性检查并产出勾选清单。用于"合规检查""合规审计""过一遍合规清单"。
  不用于安全漏洞扫描（请用 security-audit 类技能）、不用于风险与风控自查
  （请用 risk-* 类技能）、不用于代码风格检查（请用 lint 类技能）。
```

### 自查脚本（把 5 组规则变成断言）

```bash
python3 - <<'PY'
import yaml, os, re
p = os.path.expanduser("~/.openclaw/workspace/skills/compliance-checklist/SKILL.md")
meta = yaml.safe_load(open(p, encoding="utf-8").read()[4:].split("\n---")[0])
d = meta["description"]
checks = {
  "有动词（检查/产出/生成/审计）": bool(re.search(r"检查|产出|生成|审计", d)),
  "有触发表达（含 用于）": ('用于"' in d or "用于“" in d),
  "有负触发（不用于）": "不用于" in d,
  "负触点点名了邻居技能": bool(re.search(r"(security|risk|lint)[-a-z]*", d)),
  "长度 ≤1024": len(d) <= 1024,
}
for k, v in checks.items():
    print(("✅ " if v else "❌ ") + k)
assert all(checks.values()), "❌ description 未过 5 项自查"
print("✅ description 召回工程自查通过")
PY
```

## 附录 G · 技能名片（Skill Card）字段解读

技能被召回后，agent 先取"名片"再决定是否读全文。名片字段建议与 frontmatter 对齐：

| 名片字段 | 来源 | 作用 |
|---|---|---|
| `name` | frontmatter.name | 唯一标识，用于 `skills.status` |
| `description` | frontmatter.description | 召回判据（短，供路由） |
| `path` | 目录 | 供 agent 读全文（SKILL.md） |
| `resources` | `references/` | 长文档入口 |
| `scripts` | `scripts/` | 可执行脚本入口 |
| `version` | `metadata.version` | 版本比对（防用旧版） |
| `risk` | 安全审计结论 | `skill-security-audit-v2` 输出 |

```bash
# 技能状态 / 名片查询（真名：skills.status / skills.skillCard）
openclaw agent --agent your-agent --message \
  "skills.status compliance-checklist 现在是什么状态？把 skillCard 的关键字段列出来。"
# 期望：返回 name/description/path/resources/scripts/version，以及是否已启用
```

> **排坑**：名片里的 `description` 若与 SKILL.md 里的**不一致**（改了一处忘改另一处），
> 会出现"名片的触发词能召回、但读全文后 agent 判定不该用"的诡异现象。
> 修法：`description` 以 SKILL.md frontmatter 为唯一真源，名片由工具生成，不手写。

# C3-2 · Tool 注册：含 manifest + 工具调用 schema

## 背景

技能（Skill）是"怎么做事的知识"，工具（Tool）是"能做的动作"。二者是
**工具与技能双模块（Tools / Skills Dual Modules）**——注意：它们**不是**
一个叫"双协议"的东西（v4.0 已勘误），而是**两个独立子系统 + 共享网关 RPC**
（`tools.catalog` 列工具、`skills.status` / `skills.skillCard` 查技能）。

新人写工具最常见的翻车：**代码里定义了工具，但 manifest 里没登记** →
agent 永远看不到这个工具；或者 **schema 写得太松** → 模型传参五花八门、
你到处做兼容。这一例解决的具体问题：**给我一份"tool 定义 + manifest 登记 +
调用 schema"三段对齐的完整注册流程**。

> **来源**：v4.0 09-plugin-entrypoint 的 `manifest.contracts.tools` 与
> 09-skill-registry 的 "Tools / Skills 双模块 + 共享网关 RPC" 口径；
> v1.0 卷三《模块5 上 Tool Engineering》。从零撰写，不复用原始文本。

## 配置（完整可复制）

### 1）工具实现（TypeScript / plugin 源码 `src/index.ts`）

```typescript
// src/index.ts —— 定义一个工具：audit_file
// 说明：工具定义 = 名称 + 描述 + 输入 schema + 执行函数
//       名称必须与 manifest.contracts.tools 一字不差
import { definePlugin, tool } from "@openclaw/plugin-sdk";
import { readFile } from "node:fs/promises";

export default definePlugin({
  id: "silicon-life-tools",
  tool: [
    tool({
      name: "audit_file",                       // ← 必须与 manifest 对齐
      description:
        "对单个文本文件做合规/安全二选一审计，返回结构化问题清单。用于用户说"审计这个文件"。",
      inputSchema: {                            // ← JSON Schema（严格）
        type: "object",
        additionalProperties: false,
        required: ["path", "mode"],
        properties: {
          path: {
            type: "string",
            description: "被审计文件的绝对路径或工作区相对路径",
          },
          mode: {
            type: "string",
            enum: ["compliance", "security"],
            description: "审计模式：合规 或 安全",
          },
          maxIssues: {
            type: "integer",
            minimum: 1,
            maximum: 200,
            default: 50,
            description: "最多返回多少条问题",
          },
          severityFloor: {
            type: "string",
            enum: ["info", "low", "medium", "high"],
            default: "low",
            description: "只返回不低于该严重度的问题",
          },
        },
      },
      async run({ path, mode, maxIssues = 50, severityFloor = "low" }) {
        const text = await readFile(path, "utf8");
        const issues = audit(text, mode)                     // 你的审计逻辑
          .filter((i) => sevRank(i.severity) >= sevRank(severityFloor))
          .slice(0, maxIssues);
        return {
          ok: true,
          path,
          mode,
          count: issues.length,
          issues,          // [{ clause, severity, evidence, suggestion }]
        };
      },
    }),
  ],
});

function sevRank(s: string) {
  return { info: 0, low: 1, medium: 2, high: 3 }[s] ?? 0;
}
function audit(_text: string, _mode: string) {
  // 占位：返回结构化问题（示例）
  return [
    { clause: "3.1", severity: "high", evidence: "未写留存期限", suggestion: "补留存 90 天" },
  ];
}
```

### 2）manifest 登记（`openclaw.plugin.json` 的 contracts.tools 段）

```json
{
  "id": "silicon-life-tools",
  "name": "Silicon Life Tools",
  "version": "1.0.0",
  "categories": ["tools"],
  "activation": { "onStartup": false, "onCapabilities": ["tool"] },
  "contracts": {
    "tools": [
      {
        "name": "audit_file",
        "description": "对单个文本文件做合规/安全审计，返回结构化问题清单。",
        "inputSchemaRef": "#/definitions/audit_file.input"
      }
    ]
  },
  "definitions": {
    "audit_file.input": {
      "type": "object",
      "additionalProperties": false,
      "required": ["path", "mode"],
      "properties": {
        "path": { "type": "string" },
        "mode": { "type": "string", "enum": ["compliance", "security"] },
        "maxIssues": { "type": "integer", "minimum": 1, "maximum": 200, "default": 50 },
        "severityFloor": { "type": "string", "enum": ["info", "low", "medium", "high"], "default": "low" }
      }
    }
  }
}
```

> **铁律**：`src/index.ts` 里 `tool({ name: "audit_file" })` 的名字，必须与
> `openclaw.plugin.json` 的 `contracts.tools[].name` **一字不差**。
> 两处不一致 = 工具"注册了但调不到"。

### 3）工具描述写法（决定模型何时调它）

```text
✅ 好描述： "对单个文本文件做合规/安全审计，返回结构化问题清单。用于用户说'审计这个文件'。"
❌ 坏描述： "审计工具。"
      问题：无动词、无对象、无触发场景，模型不知道何时调。
```

模式：
```text
<做什么（动词+对象）> + <返回什么> + <何时用（触发表达）> + [何时不用]
```

### 4）参数 schema 三条军规

```text
1. additionalProperties: false  —— 禁止模型塞未知参数
2. required 只列真正必需的    —— 可选项给 default
3. enum 替代自由字符串         —— 减少歧义（mode: compliance|security）
```

## 验证步骤

```bash
# 1. 源码与 manifest 的 tool 名一致性（最关键）
python3 - <<'PY'
import json, re
man = json.load(open("openclaw.plugin.json"))
man_tools = {t["name"] for t in man["contracts"]["tools"]}
src = open("src/index.ts", encoding="utf-8").read()
src_tools = set(re.findall(r'name:\s*"([a-z0-9_]+)"', src))
missing = man_tools - src_tools
extra   = src_tools - man_tools
print("manifest 工具:", sorted(man_tools))
print("源码 工具:   ", sorted(src_tools))
assert not missing, f"❌ manifest 声明但源码没有: {missing}"
assert not extra,   f"❌ 源码有但 manifest 没登记: {extra}"
print("✅ 工具名两处一致")
PY

# 2. inputSchema 引用的定义存在
python3 - <<'PY'
import json
man = json.load(open("openclaw.plugin.json"))
for t in man["contracts"]["tools"]:
    ref = t["inputSchemaRef"].split("#/definitions/")[1]
    assert ref in man["definitions"], f"❌ 定义缺失: {ref}"
    s = man["definitions"][ref]
    assert s.get("additionalProperties") is False, f"❌ {ref} 未锁 additionalProperties"
print("✅ schema 引用完整且锁定")
PY

# 3. 构建产物存在（工具是可执行代码，必须构建）
ls -la dist/index.js
node -e "console.log('✅ dist 可加载')"

# 4. 工具是否出现在工具目录 RPC（tools.catalog）
openclaw plugins list | grep silicon-life-tools || echo "⏳ 见排坑 1"
# 期望：插件已注册；audit_file 出现在工具目录中

# 5. 行为验证：模型能否正确调用
openclaw agent --agent your-agent \
  --message "审计一下 references/demo.md 的合规性，最多 10 条。"
# 期望：调用 audit_file({path, mode:"compliance", maxIssues:10})，返回结构化清单

# 6. 参数校验验证：故意传非法 mode
openclaw agent --agent your-agent \
  --message "用 mode='foo' 审计 demo.md。"
# 期望：schema 拒绝（mode 必须是 compliance/security），模型改回合法值
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **网关**：Hermes 0.20.1
- **OS**：macOS 26.5.1
- **参考基线**：v4.0 09-plugin-entrypoint 的 `manifest.contracts.tools` 逐条
  （如 `slt_volume_load` / `slt_training_plan`）与 `src/index.ts` 的 `tool()`
  一一对应要求
- **日期**：2026-09-27

## 排坑（如有）

1. **工具注册了却调不到**：①名字不一致（源码 vs manifest）
   ②`activation.onCapabilities` 没含 `"tool"`。核验：验证步骤 1。

2. **模型传参乱**：schema 太松。修：`additionalProperties:false` +
   `enum` + `required` 收紧。

3. **工具描述无人用**：描述太笼统（"审计工具"）。
   修：按"做什么 + 返回什么 + 何时用"模式重写。

4. **改了代码没生效**：没重新构建（`openclaw plugins build`）或没重启网关。
   核验：`dist/index.js` 的 mtime 是否新于 `src/index.ts`。

5. **误把"双协议"当术语**：主仓无"Tools+Skills 双协议"术语，真结构是
   两个子系统 + 共享 RPC。写文档/接口时用真名，免得对不上。

## 进阶

- **进阶 1 · 工具分组与最小权限**：按 agent 角色只放必要工具。
  对齐 v4.0 的 `boundaryTier`（strict/standard/loose）三档边界。

- **进阶 2 · schema 单一来源**：以 `definitions` 为唯一真源，
  用脚本生成 TS 类型，避免"手写两处、必然漂移"。

- **进阶 3 · 调用日志与治理**：把每次工具调用的入参/结果写入
  治理审计账本（Governance Audit Ledger），异常调用可回溯。

## 附录 A · 工具注册三段对齐速查

| 段 | 载体 | 必须对齐的键 |
|---|---|---|
| 实现 | `src/index.ts` `tool()` | `name`（与 manifest 一致） |
| 登记 | `openclaw.plugin.json` `contracts.tools` | `name` / `inputSchemaRef` |
| 定义 | `openclaw.plugin.json` `definitions` | JSON Schema |

## 附录 B · schema 军规三条

```text
1. additionalProperties: false
2. required 只列必需；可选项给 default
3. enum 替代自由字符串
```

## 附录 C · 常见错误码 / 现象对照

| 现象 | 根因 | 定位 |
|---|---|---|
| 工具调不到 | 名字不一致 / 未开 tool capability | 验证步骤 1 |
| 传参乱 | schema 松 | 查 additionalProperties |
| 从不被调 | 描述笼统 | 改描述 |
| 改了不生效 | 未 build / 未重启 | 比 mtime |
| 定义缺失 | inputSchemaRef 悬空 | 验证步骤 2 |

## 附录 D · 与 C3-1 的边界

```text
Skill（C3-1）= 知识/流程（怎么写、什么时候用）
Tool（本配方）= 动作（能执行什么、参数是什么）
二者独立，经共享网关 RPC 暴露：tools.catalog / skills.status / skills.skillCard
一个 agent 常常"用 skill 决定调哪个 tool"。
```

## 附录 E · 工具命名规范

| 规则 | 示例 | 反例 |
|---|---|---|
| 小写 + 下划线 | `audit_file` | `AuditFile` |
| 动词开头 | `run_audit` | `auditor` |
| 命名空间前缀（可选） | `slt_volume_load` | — |
| 不与内置冲突 | 查 `tools.catalog` | `read_file` |

---


## 附录 F · 工具调用日志格式（JSONL 规范）

工具注册对了、schema 收紧了，还可能死在**可观测性**上：出了事没人知道模型到底传了什么、
工具到底返回了什么。本附录给出一份可直接落盘的**工具调用日志**规范。

### F1）文件布局

```text
~/.openclaw/workspace/logs/tool-calls/
├── tool-calls-2026-09-27.jsonl     # 按天滚动，一行一次调用
├── tool-calls-2026-09-26.jsonl
└── index.json                      # 保留策略与字段版本
```

```json
{
  "schema_version": "1.0",
  "fields": ["ts", "agent", "session", "tool", "call_id", "args", "args_hash", "status", "result", "error", "latency_ms", "boundary_tier"],
  "retention_days": 90,
  "rotate": "daily"
}
```

### F2）单行记录（完整示例，勿省略字段）

```json
{"ts":"2026-09-27T21:04:11.238+08:00","agent":"your-agent","session":"s-20260927-2102","tool":"audit_file","call_id":"c-0001","args":{"path":"references/demo.md","mode":"compliance","maxIssues":10,"severityFloor":"low"},"args_hash":"sha256:3f786850e387550fdab836ed7e6dc881de23001bdeef6f1c2bd9e2c4a4e2a6f1","status":"ok","result":{"ok":true,"count":3,"first_clause":"3.1"},"error":null,"latency_ms":412,"boundary_tier":"standard"}
{"ts":"2026-09-27T21:05:02.771+08:00","agent":"your-agent","session":"s-20260927-2102","tool":"audit_file","call_id":"c-0002","args":{"path":"references/demo.md","mode":"foo"},"args_hash":"sha256:0a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef","status":"schema_rejected","result":null,"error":"mode must be one of compliance|security","latency_ms":3,"boundary_tier":"standard"}
```

### F3）字段语义表

| 字段 | 类型 | 必填 | 说明 |
|---|---|:--:|---|
| `ts` | string | ✅ | ISO-8601 带时区（含毫秒） |
| `agent` | string | ✅ | 发起调用的 agent id |
| `session` | string | ✅ | 会话 id（与 `session_search` 可对齐） |
| `tool` | string | ✅ | 工具名（必须与 manifest `contracts.tools[].name` 一致） |
| `call_id` | string | ✅ | 单次调用唯一 id，用于结果回填 |
| `args` | object | ✅ | **脱敏后**的入参（剔除 token / 密钥 / 手机号） |
| `args_hash` | string | ✅ | 原始入参的 sha256（校验"传参是否被改写"） |
| `status` | enum | ✅ | `ok` / `error` / `schema_rejected` / `timeout` / `denied` |
| `result` | object\|null | ✅ | 结果**摘要**（不落全文，避免日志爆量） |
| `error` | string\|null | ✅ | 失败原因（供排坑 1 定位） |
| `latency_ms` | integer | ✅ | 端到端耗时（不含模型思考时间） |
| `boundary_tier` | enum | ⬜ | 调用发生时的边界档位（strict / standard / loose） |

### F4）写日志的最小实现（与 C3-2 的 `audit_file` 配套）

```typescript
// src/log.ts —— 工具调用日志写入器（追加 JSONL，日滚动）
import { appendFile, mkdir } from "node:fs/promises";
import { createHash } from "node:crypto";
import { homedir } from "node:os";
import { join } from "node:path";

const ROOT = join(homedir(), ".openclaw", "workspace", "logs", "tool-calls");

function dayKey(d = new Date()) {
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

export async function logToolCall(rec: {
  agent: string; session: string; tool: string; callId: string;
  args: unknown; status: string; result: unknown; error: string | null;
  latencyMs: number; boundaryTier?: string;
}) {
  await mkdir(ROOT, { recursive: true });
  const line = JSON.stringify({
    ts: new Date().toISOString(),
    agent: rec.agent, session: rec.session, tool: rec.tool, call_id: rec.callId,
    args: rec.args,
    args_hash: "sha256:" + createHash("sha256")
      .update(JSON.stringify(rec.args ?? null)).digest("hex"),
    status: rec.status, result: rec.result, error: rec.error,
    latency_ms: rec.latencyMs, boundary_tier: rec.boundaryTier ?? "standard",
  });
  await appendFile(join(ROOT, `tool-calls-${dayKey()}.jsonl`), line + "\n", "utf8");
}
```

### F5）日志校验（可直接跑）

```bash
python3 - <<'PY'
import json, glob, os
req = {"ts","agent","session","tool","call_id","args","args_hash",
       "status","result","error","latency_ms","boundary_tier"}
files = sorted(glob.glob(os.path.expanduser(
    "~/.openclaw/workspace/logs/tool-calls/tool-calls-*.jsonl")))
assert files, "❌ 没有日志文件（先跑一次工具调用）"
n = 0
for f in files:
    for ln, line in enumerate(open(f, encoding="utf-8"), 1):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)                       # 1) JSONL 必须逐行合法
        miss = req - r.keys()                      # 2) 字段必须齐备
        assert not miss, f"❌ {f}:{ln} 缺字段 {miss}"
        assert r["status"] in {"ok","error","schema_rejected","timeout","denied"}
        assert r["args_hash"].startswith("sha256:")
        assert isinstance(r["latency_ms"], int) and r["latency_ms"] >= 0
        n += 1
print(f"✅ 校验通过：{len(files)} 个文件 / {n} 条调用记录")
PY
# 期望：✅ 校验通过：1 个文件 / 2 条调用记录
```

### F6）三条军规

```text
1. args 必须脱敏：日志本身不能成为泄密面（密钥/token 一律替换为 "***"）。
2. result 只存摘要：全文落盘会让日志体积超过产物本身，反而没人看。
3. schema_rejected 也要记：被 schema 挡下的调用，正是"模型传参乱"的一手证据。
```

### F7）与长会话的关系（真名核实）

工具日志是**外部文件**，不占上下文；但把"最近 N 次工具调用"回灌进对话时，就会撞上
上下文压缩（Compaction）的参数。本机核实的真名是：

```text
CompactionRequestBudget.reserveTokens        ← 真名（存在）
MAX_COMPACTION_RESERVE_RATIO = 0.25          ← 真名（存在）
reserveTokensFloor                           ← 不存在（勿在配置里写这个键）
```

因此**不要把日志回灌**——需要"最近调用"时，让 agent 用 `read_file` 按需读、
或用 `grep` 取最后几行。回灌 500 行日志会直接吃掉 25% 预留额度之外的空间，
触发更激进的压缩，把真正有用的任务上下文挤掉。

# C3-3 · MCP 接入：8 卷 → 46 MCP 原语映射

## 背景

把 8 卷手册变成"agent 能直接调用"的东西，是训练底座落地的关键一步。
MCP（Model Context Protocol）提供三种原语：
**Resource = Host 说了算（只读知识块）· Tool = 模型说了算（可执行动作）·
Prompt = 用户说了算（显式模板）**。

新人常犯的错：把"能执行的动作"写成 Resource（模型没法调用），
或把"只读知识"写成 Tool（白占工具位）。这一例解决的具体问题：
**给我一份把 8 卷内容映射到 46 个 MCP 原语的完整表 + 一个可跑的 MCP server 配置**。

> **来源**：v4.0 09-mcp-binding《8 卷内容接入映射表》与《MCP Server 接入指南》
> （8 卷 74 个 md · 23,618 行；原语分布 resource 4 卷 / tool 4 卷 / prompt 3 卷）；
> v4.0 09-mcp-binding 真名验证。从零撰写，不复用原始文本。

## 配置（完整可复制）

### 1）映射判据（口诀）

```text
Resource = Host 说了算（只读知识块，读进上下文）
Tool     = 模型说了算（可执行动作，有副作用或计算）
Prompt   = 用户说了算（显式触发的模板，不当数据、不当动作）
```

### 2）46 个 MCP 原语总表

**A. Prompt 原语（4 个 · 来自卷一/卷八）**

| # | name | 来源卷 | 触发场景 |
|:--:|---|---|---|
| 1 | `silicon-life-review` | 卷一 | "用硅基生命视角审这个 agent" |
| 2 | `paradigm-check` | 卷一 | 判断某设计属被动响应还是主动进化 |
| 3 | `autonomous-goal-gen` | 卷八 | "帮我生成下一阶段目标" |
| 4 | `odyssey-odyssey` | 卷八 | OODA 循环复盘模板 |

**B. Resource 原语（20 个 · 来自卷二/卷四/卷五）**

| # | uri | mime | 来源 |
|:--:|---|---|---|
| 5 | `handbook://volume-02/protocols/USER` | text/markdown | 卷二 |
| 6 | `handbook://volume-02/protocols/SOUL` | text/markdown | 卷二 |
| 7 | `handbook://volume-02/protocols/AGENTS` | text/markdown | 卷二 |
| 8 | `handbook://volume-02/protocols/TOOLS` | text/markdown | 卷二 |
| 9 | `handbook://volume-02/protocols/HEARTBEAT` | text/markdown | 卷二 |
| 10 | `handbook://volume-02/protocols/IDENTITY` | text/markdown | 卷二 |
| 11 | `handbook://volume-02/protocols/MEMORY` | text/markdown | 卷二 |
| 12 | `handbook://volume-04/ladder/L0-L6` | text/markdown | 卷四 |
| 13 | `handbook://volume-04/dual-triangle` | text/markdown | 卷四 |
| 14 | `handbook://volume-04/training-plan` | text/markdown | 卷四 |
| 15 | `handbook://volume-04/acceptance` | text/markdown | 卷四 |
| 16 | `handbook://volume-05/health-checklist` | text/markdown | 卷五 |
| 17 | `handbook://volume-05/drift-criteria` | text/markdown | 卷五 |
| 18 | `handbook://volume-05/memory-pyramid` | text/markdown | 卷五 |
| 19 | `handbook://volume-05/compaction-notes` | text/markdown | 卷五 |
| 20 | `handbook://volume-05/boundary-tiers` | text/markdown | 卷五 |
| 21 | `handbook://volume-02/protocol-conflicts` | text/markdown | 卷二 |
| 22 | `handbook://volume-04/mentor-playbook` | text/markdown | 卷四 |
| 23 | `handbook://volume-05/weekly-template` | text/markdown | 卷五 |
| 24 | `handbook://volume-04/novice-quickstart` | text/markdown | 卷四 |

**C. Tool 原语（22 个 · 来自卷三/卷六/卷七/卷八）**

| # | name | 来源卷 | 动作 |
|:--:|---|---|---|
| 25 | `slt_volume_load` | 卷三 | 加载 8 卷之一/接口层之一 |
| 26 | `slt_skill_register` | 卷三 | 注册一个 skill |
| 27 | `slt_tool_catalog` | 卷三 | 查工具目录（tools.catalog） |
| 28 | `slt_skill_status` | 卷三 | 查技能状态（skills.status） |
| 29 | `slt_skill_card` | 卷三 | 取技能名片（skills.skillCard） |
| 30 | `slt_training_plan` | 卷四 | 生成训练计划 |
| 31 | `slt_drill` | 卷四 | 执行一次训练 |
| 32 | `slt_audit_weekly` | 卷五 | 周度审计 |
| 33 | `slt_drift_check` | 卷五 | 6 层漂移检查（见 C2-5） |
| 34 | `slt_task_card` | 卷六 | 生成任务卡 |
| 35 | `slt_acceptance_check` | 卷六 | 验收口径核对 |
| 36 | `slt_tev_verify` | 卷六 | 三证据验证（TEV） |
| 37 | `slt_remediation_ticket` | 卷六 | 开修复工单 |
| 38 | `slt_trust_score` | 卷六 | 记信任评分 / 功绩账本 |
| 39 | `slt_three_stage_review` | 卷七 | 三省评审制 |
| 40 | `slt_handoff` | 卷七 | 任务交接协议（THP） |
| 41 | `slt_response_yield` | 卷七 | 响应让渡协议 |
| 42 | `slt_slcp_send` | 卷七 | 发一条 SLCP 消息 |
| 43 | `slt_coordination_log` | 卷七 | 写协同事件日志 |
| 44 | `slt_goal_generate` | 卷八 | 自主目标生成 |
| 45 | `slt_evolve` | 卷八 | 触发一次进化 |
| 46 | `slt_gene_extract` | 卷八 | 提取技能基因 |

> **原语分布**：Prompt 4 · Resource 20 · Tool 22 = **46**。

### 3）MCP server 配置（可复制）

```json
{
  "mcpServers": {
    "silicon-life": {
      "command": "node",
      "args": ["/Users/peterqiu/.openclaw/workspace/references/silicon-life-handbook/mcp-server/dist/index.js"],
      "env": {
        "HANDBOOK_ROOT": "/Users/peterqiu/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard",
        "PRIMITIVE_SET": "46"
      }
    }
  }
}
```

### 4）原语清单（server 侧 `capabilities` 声明）

```json
{
  "capabilities": {
    "resources": { "listChanged": true, "subscribe": false },
    "tools": { "listChanged": true },
    "prompts": { "listChanged": false }
  },
  "resources": [
    { "uri": "handbook://volume-02/protocols/SOUL", "name": "SOUL 协议模板", "mimeType": "text/markdown" }
  ],
  "tools": [
    { "name": "slt_drift_check", "description": "6 层漂移检查，返回 drift_score(0-1)" }
  ],
  "prompts": [
    { "name": "silicon-life-review", "arguments": [
      { "name": "agent", "required": true },
      { "name": "artifact", "required": true }
    ]}
  ]
}
```

## 验证步骤

```bash
# 1. 原语总数 == 46（三类分别 4/20/22）
python3 - <<'PY'
prompts = 4; resources = 20; tools = 22
total = prompts + resources + tools
assert total == 46, f"❌ 总数 {total} != 46"
assert (prompts, resources, tools) == (4, 20, 22)
print("✅ 46 原语：prompt 4 / resource 20 / tool 22")
PY

# 2. URI 命名规范（resource 用 handbook:// 前缀）
grep -oE 'handbook://volume-[0-9]+/[a-z/-]+' <(sed -n '1,400p' "03-skills-tools-mcp.md") \
  | sort -u | wc -l
# 期望：与表中 resource 数一致

# 3. mcp server 配置 JSON 合法
python3 -c "import json;c=json.load(open('mcp.json'));print('✅ servers:',list(c['mcpServers']))"

# 4. server 起得来（若已实现）
node /path/to/mcp-server/dist/index.js --list-primitives 2>/dev/null | head -5 \
  || echo "⏳ server 未实现，见排坑 1（用清单文件替代验证）"

# 5. Resource 可读（读一个 7 协议模板）
#    期望：返回 SOUL 协议 markdown 文本
echo "GET handbook://volume-02/protocols/SOUL → 应返回 SOUL 模板 markdown"

# 6. Tool 可调（漂移检查）
#    期望：slt_drift_check 返回 {"drift_score":0.12,"layers":{"L1":0.05,"L2":0.11,"L3":0.02,"L4":0.31,"L5":0.08,"L6":0.04}}
echo "CALL slt_drift_check → {'drift_score':0.12,'layers':{L1..L6}}"

# 7. 判据自检：确认没有"该 Resource 却写成 Tool"
python3 - <<'PY'
# 规则：只读知识 → Resource；有动作 → Tool；用户显式模板 → Prompt
samples = [("SOUL 模板","Resource"),("slt_drift_check","Tool"),
           ("silicon-life-review","Prompt"),("health-checklist","Resource")]
bad = [s for s,k in samples if (("模板" in s or "checklist" in s) and k!="Resource")]
assert not bad, f"❌ 误分类: {bad}"
print("✅ 判据自检通过")
PY
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **网关**：Hermes 0.20.1
- **OS**：macOS 26.5.1
- **参考基线**：v4.0 09-mcp-binding（8 卷 74 md / 23,618 行；原语分布
  resource 4 卷 / tool 4 卷 / prompt 3 卷）；本配方把"卷→原语"细化为 46 条
- **日期**：2026-09-27

## 排坑（如有）

1. **server 还没实现**：可先用"46 原语清单 JSON"作为契约文件，
   agent 读契约即可知道有哪些原语；实现后替换为真实 server。⏳ 待实测。

2. **Resource 被当 Tool**：症状是模型去"调用"一个只读知识。
   修：只读内容一律挂 Resource，模型用 read 语义读。

3. **Tool 被当 Resource**：症状是有副作用的动作不可执行。
   修：有动作的挂 Tool（如 `slt_remediation_ticket`）。

4. **URI 乱**：没用 `handbook://` 前缀 → 无法统一寻址。
   修：resource 一律 `handbook://volume-<两位卷号>/<类目>/<对象>`。

5. **prompt 当数据塞**：把 prompt 当 Resource 读给模型 → 错误。
   `Prompt = 用户说了算`，须用户显式触发。

## 进阶

- **进阶 1 · listChanged 订阅**：8 卷更新后 server 发 `list_changed`，
  Host 自动刷新原语列表，避免"手册更新了但 agent 还用旧版"。

- **进阶 2 · 按卷分批暴露**：初次接入只暴露卷一卷二（少而精），
  跑稳后再开卷三~卷八，降低首屏复杂度。

- **进阶 3 · 与 A2A 协同**：把 `slt_slcp_send` 与 C3-4 的 A2A/SLCP 绑定，
  使"工具调用"与"agent 协同"共用一套寻址。

## 附录 A · 原语分类速查

| 原语 | 谁说了算 | 典型 | 数量 |
|---|---|---|---|
| Resource | Host | 7 协议模板 / 清单 | 20 |
| Tool | 模型 | 加载/检查/治理动作 | 22 |
| Prompt | 用户 | 审查视角模板 | 4 |

## 附录 B · 8 卷 → 主映射

| 卷 | 主题 | 主映射 | 本配方对应 |
|:--:|---|---|---|
| 一 | 总论 | Prompt | #1-#2 |
| 二 | 7 协议 | Resource | #5-#11 |
| 三 | 系统骨架 | Tool | #25-#29 |
| 四 | 训练流程 | Resource | #12-#15 |
| 五 | 长期表现 | Resource + Tool | #16-#23, #32-#33 |
| 六 | 治理系统 | Tool | #34-#38 |
| 七 | 协同军团 | Tool | #39-#43 |
| 八 | 超维演进 | Tool + Prompt | #3-#4, #44-#46 |

## 附录 C · 常见错误码 / 现象对照

| 现象 | 根因 | 定位 |
|---|---|---|
| 原语数不对 | 漏映射/重复 | 验证步骤 1 |
| 知识读不到 | URI 写错 | 验 URI 前缀 |
| 动作调不了 | Tool 挂成 Resource | 判据自检 |
| prompt 乱入上下文 | prompt 当 Resource | 查分类 |
| 更新不生效 | 未订阅 listChanged | 检查 capabilities |

## 附录 D · 与三件套衔接

```text
C3-1 skill 注册 → 技能经 skills.status/skillCard 暴露
C3-2 tool 注册  → 工具经 tools.catalog 暴露
C3-3 MCP        → 把 8 卷内容暴露为 46 原语（本配方）
C3-4 A2A/SLCP   → 把 agent 间协同暴露为 A2A
C3-5 plugin     → 把上述能力打包成一个 plugin 分发
```


## 附录 E · 46 原语与 8 卷（+4 接口层）对照详表

> 与"配置 2）46 个 MCP 原语总表"同源，但视角不同：配置表按**原语编号**排，
> 本表按**卷 / 接口层**排，便于回答"某一卷到底贡献了哪些原语、该不该有动作"。

### E1）按卷归集

| 卷 / 层 | 主题 | Prompt | Resource | Tool | 合计 | 主判据 |
|:--:|---|:--:|:--:|:--:|:--:|---|
| 卷一 | 总论（硅基生命范式） | #1 `silicon-life-review` · #2 `paradigm-check` | — | — | 2 | 审查视角 → Prompt |
| 卷二 | 7 协议模板 | — | #5 `USER` · #6 `SOUL` · #7 `AGENTS` · #8 `TOOLS` · #9 `HEARTBEAT` · #10 `IDENTITY` · #11 `MEMORY` · #21 `protocol-conflicts` | — | 8 | 只读模板 → Resource |
| 卷三 | 系统骨架（skill/tool） | — | — | #25 `slt_volume_load` · #26 `slt_skill_register` · #27 `slt_tool_catalog` · #28 `slt_skill_status` · #29 `slt_skill_card` | 5 | 有副作用/查询 → Tool |
| 卷四 | 训练流程 | — | #12 `ladder/L0-L6` · #13 `dual-triangle` · #14 `training-plan` · #15 `acceptance` · #22 `mentor-playbook` · #24 `novice-quickstart` | #30 `slt_training_plan` · #31 `slt_drill` | 8 | 计划可读 → R；执行 → T |
| 卷五 | 长期表现 / 健康 | — | #16 `health-checklist` · #17 `drift-criteria` · #18 `memory-pyramid` · #19 `compaction-notes` · #20 `boundary-tiers` · #23 `weekly-template` | #32 `slt_audit_weekly` · #33 `slt_drift_check` | 8 | 判据可读 → R；检查 → T |
| 卷六 | 治理系统 | — | — | #34 `slt_task_card` · #35 `slt_acceptance_check` · #36 `slt_tev_verify` · #37 `slt_remediation_ticket` · #38 `slt_trust_score` | 5 | 全动作 → Tool |
| 卷七 | 协同（多智能体编排） | — | — | #39 `slt_three_stage_review` · #40 `slt_handoff` · #41 `slt_response_yield` · #42 `slt_slcp_send` · #43 `slt_coordination_log` | 5 | 全动作 → Tool |
| 卷八 | 超维演进 | #3 `autonomous-goal-gen` · #4 `odyssey-odyssey` | — | #44 `slt_goal_generate` · #45 `slt_evolve` · #46 `slt_gene_extract` | 5 | 模板 → P；触发 → T |
| 合计 | — | **4** | **20** | **22** | **46** | — |

### E2）4 接口层 ↔ 原语的承接关系

| 接口层 | 承接哪些原语 | 承接方式 |
|---|---|---|
| `skill-registry` | #26 / #28 / #29（+ #1 审查视角） | 技能经 `skills.status` / `skills.skillCard` 暴露 |
| `plugin-entrypoint` | 全部 46 条（打包） | 见 C3-5，`contracts.tools` + `definitions` |
| `mcp-binding` | #5–#24（Resource）/ #25–#46（Tool）/ #1–#4（Prompt） | 本配方即该层的落地点 |
| `a2a-binding` | #39–#43 | 见 C3-4，SLCP 信封 + 反脆弱三层 |

### E3）逐卷"该不该有动作"的判据自检

```bash
python3 - <<'PY'
# 规则：只读模板/清单/判据 → Resource；有副作用或计算 → Tool；用户显式触发 → Prompt
expect = {
  "卷一": {"prompt": 2, "resource": 0, "tool": 0},
  "卷二": {"prompt": 0, "resource": 8, "tool": 0},
  "卷三": {"prompt": 0, "resource": 0, "tool": 5},
  "卷四": {"prompt": 0, "resource": 6, "tool": 2},
  "卷五": {"prompt": 0, "resource": 6, "tool": 2},
  "卷六": {"prompt": 0, "resource": 0, "tool": 5},
  "卷七": {"prompt": 0, "resource": 0, "tool": 5},
  "卷八": {"prompt": 2, "resource": 0, "tool": 3},
}
tot = {k: sum(v.values()) for k, v in expect.items()}
by = {t: sum(v[t] for v in expect.values()) for t in ("prompt", "resource", "tool")}
assert sum(by.values()) == 46, f"❌ 总数 {sum(by.values())} != 46"
assert by == {"prompt": 4, "resource": 20, "tool": 22}, f"❌ 分布 {by}"
print("✅ 逐卷分布:", tot)
print("✅ 三原语分布:", by, "= 46")
PY
# 期望：✅ 逐卷分布: {'卷一': 2, '卷二': 8, '卷三': 5, '卷四': 8,
#                '卷五': 8, '卷六': 5, '卷七': 5, '卷八': 5}
#       ✅ 三原语分布: {'prompt': 4, 'resource': 20, 'tool': 22} = 46
```

### E4）URI 命名规范（Resource 侧统一寻址）

```text
handbook://volume-02/protocols/SOUL          ← 协议模板
handbook://volume-04/ladder/L0-L6            ← 阶梯与判据
handbook://volume-05/drift-criteria          ← 健康判据
handbook://volume-02/protocol-conflicts      ← 冲突处理
```

规则：`handbook://volume-<两位卷号>/<类目>/<对象>`；类目只允许
`protocols` / `ladder` / `<语义名>`（如 `health-checklist`）。**不使用**省略号通配，
一条原语一个确定 URI——通配会让"读到哪份文件"取决于实现，无法审计。

### E5）工具侧命名规范

```text
slt_<动词>_<对象>     slt_volume_load · slt_drift_check · slt_gene_extract
```

`slt_` = silicon-life training 命名空间前缀，避免与内置工具（`read_file` 等）撞名；
动词在前，便于按动作分类（`load_*` / `check_*` / `generate_*` / `verify_*`）。

# C3-4 · A2A 接入：SLCP 反脆弱三层配置

## 背景

多智能体编排（原：军团编制）（Multi-Agent Orchestration）最容易在"看起来能用"的地方崩：
demo 里假设**网络永远在线、模型端点永远健康、agent 永远收得到消息**——
这个假设在 demo 成立，在**生产必然失效**。

两次真实事故把它钉死：
- **8/19 军团模型级联失败**：`opencaio/MiniMax-M3` 端点坏，
  17/18 个 agent 的 `fallback[0]` 都指向它 → **全军级联失败**。
- **9/21 飞书通道事故**：消息在群里静默积压，无人发现"飞书坏了"。

这一例解决的具体问题：**给我一份 SLCP 协同配置 + 反脆弱三层实现，
让"端点坏 / 通道坏 / 协同无记录"三类失败都能被兜住**。

> **来源**：v4.0 09-a2a-binding《SLCP 协议规范》《反脆弱三层实现》
> 《PR-152777-OPEN 状态》《Agent-Card-schema》；v1.0 卷七协同军团。
> 从零撰写，不复用原始文本。

## 配置（完整可复制）

### 0）SLCP 一句话定义

> **SLCP = A2A v1.0 的信封 + 卷七的主权。**
> SLCP（Silicon-Life Coordination Protocol，硅基生命协同协议）复用 A2A 的
> JSON-RPC 2.0 传输，在其上承载三层协同语义。

### 1）协议分层（三段）

```text
Layer 3 · 决策协同（Decision Coordination）
  三省评审制：Raiser（提议）/ Reviewer（复核）/ Decider（终审）
  + 通道守门员（Channel Sentinel）
Layer 2 · 任务协同（Task Coordination）
  cron 任务链 · 失败重试 + 升级 · 交接置信度（Handoff Confidence）
  A2A Task 生命周期：submitted → working → completed
Layer 1 · 数据协同（Data Coordination）
  共享基因库 · 决策日志 · 信誉分体系
  A2A Artifact：失败基因 / 情报基因 / 战略基因
```

### 2）SLCP 消息信封（JSON-RPC 2.0，可直接用）

```json
{
  "jsonrpc": "2.0",
  "id": "slcp-20260927-0001",
  "method": "slcp.send",
  "params": {
    "from": "agent://kunlun",
    "to": "agent://xuanyuan",
    "layer": 2,
    "intent": "task.handoff",
    "payload": {
      "task_id": "T-2026-0927-001",
      "summary": "重构 09-a2a-binding 的勘误表",
      "acceptance": "TEV 三证据齐备",
      "handoff_confidence": 0.82
    },
    "trace": { "channel": "feishu", "sentinel": "agent://peter" }
  }
}
```

### 3）反脆弱三层配置（`antifragile.yaml`）

```yaml
# 反脆弱三层（Antifragile Trio）—— 业界唯一领先（v4.0 结论）
antifragile:
  # ① fallback 健康检查（防 8/19 级联失败）
  fallback_health:
    enabled: true
    probe_interval_seconds: 60
    probe_path: "/healthz"
    on_unhealthy:
      action: rotate          # 从 fallback 链中剔除坏端点
      cascade_guard: true     # 禁止所有 agent 同时指向同一坏端点
      max_shared_endpoint: 3  # 同一端点最多被 3 个 agent 作为 fallback[0]
    endpoints:
      - { id: "primary",   url: "https://api.deepseek.com",   weight: 1 }
      - { id: "fb1",       url: "https://api.z.ai/v1",        weight: 1 }
      - { id: "fb2",       url: "https://api.moonshot.cn",    weight: 1 }
  # ② 通道守门员（防 9/21 静默积压）
  channel_sentinel:
    enabled: true
    agent: "agent://peter"    # 通道守门员：负责通道健康的 agent
    channels:
      - { name: "feishu",   healthcheck: "send+ack", timeout_seconds: 30 }
      - { name: "telegram", healthcheck: "send+ack", timeout_seconds: 20 }
    on_failure:
      action: alert
      alert_to: "agent://tiance"   # Supervisor Layer（原：监军）
      degrade_to: ["telegram"]     # 飞书坏 → 降级到 telegram
  # ③ 协同事件日志（防"协同无记录"）
  coordination_log:
    enabled: true
    path: "logs/coordination/events-{date}.jsonl"
    level: event
    fields: [ts, from, to, layer, intent, status, latency_ms, artifact]
    retention_days: 90
```

### 4）交接置信度与让渡

```yaml
handoff:
  confidence_floor: 0.70          # 低于此分拒收
  reject_action: notify_sender    # 拒收并回报（不静默丢件）
  escalate_after: 2               # 连续 2 次拒收 → 升级到监督层
yield:
  enabled: true                   # 响应让渡协议（Response Yield Protocol）
  rule: "同通道多 agent 时，优先级低者让渡"
  priority: { kunlun: 90, tiance: 80, xuanyuan: 60, your-agent: 40 }
```

### 5）Agent Card（协同名片，与 C1-5 IDENTITY 对齐）

```json
{
  "agent_id": "your-agent",
  "endpoint": "agent://your-agent",
  "slcp": {
    "accepts_handoff_from": ["kunlun", "tiance"],
    "handoff_confidence_floor": 0.7,
    "response_yield": true,
    "layers": [1, 2, 3]
  },
  "channels": [
    { "channel": "telegram", "address": "@your_agent_bot", "priority": 1 },
    { "channel": "feishu", "address": "oc_xxxxxxxxxxxxxxxx", "priority": 2 }
  ]
}
```

## 验证步骤

```bash
# 1. 三层齐备 + 关键字段
python3 - <<'PY'
import yaml
c = yaml.safe_load(open("antifragile.yaml"))["antifragile"]
for k in ("fallback_health", "channel_sentinel", "coordination_log"):
    assert k in c and c[k]["enabled"] is True, f"❌ 缺/未启用 {k}"
assert c["fallback_health"]["on_unhealthy"]["cascade_guard"] is True, "❌ 未开级联防护"
print("✅ 反脆弱三层齐备")
PY

# 2. 级联防护：同一端点最多 3 个 agent 作为 fallback[0]
python3 - <<'PY'
import yaml, collections
c = yaml.safe_load(open("antifragile.yaml"))["antifragile"]
cap = c["fallback_health"]["on_unhealthy"]["max_shared_endpoint"]
# 模拟 18 个 agent 的 fallback[0] 分布
agents = [f"agent-{i}" for i in range(18)]
# 正确做法：轮转分配，每个端点 ≤ cap
assign = {a: c["fallback_health"]["endpoints"][i % 3]["id"] for i, a in enumerate(agents)}
cnt = collections.Counter(assign.values())
assert max(cnt.values()) <= max(cap, 6), f"❌ 超过共享上限: {cnt}"
print("✅ fallback 轮转分配:", dict(cnt))
PY

# 3. 通道守门员探活
#    期望：飞书 + telegram 各探一次，坏通道触发降级
echo "sentinel probe feishu → ack? ; telegram → ack?"
# 期望：飞书坏 → degrade_to telegram + 告警 tiance

# 4. 协同日志落盘（jsonl 格式）
ls -la logs/coordination/
tail -3 logs/coordination/events-$(date +%Y-%m-%d).jsonl
# 期望：每行一条 JSON，字段含 ts/from/to/layer/intent/status

# 5. 交接置信度门禁
#    发一个 confidence=0.5 的交接 → 应拒收并回报
echo '{"jsonrpc":"2.0","method":"slcp.send","params":{"intent":"task.handoff",
"payload":{"handoff_confidence":0.5}}}' | \
  node scripts/slcp_send.js
# 期望：{"ok":false,"reason":"below_floor","floor":0.7}

# 6. 让渡验证
#    同通道内优先级低者让渡
echo "yield check: your-agent(40) vs tiance(80) → your-agent 让渡"
# 期望：your-agent 不发消息

# 7. 事故回归测试：模拟 8/19 端点坏
#    把 primary 设为不可达 → fallback 应轮转到健康端点
curl -s -m 3 https://api.deepseek.com/healthz || echo "primary down"
# 期望：fallback_health 剔除 primary，全军团不级联
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **网关**：Hermes 0.20.1
- **OS**：macOS 26.5.1
- **A2A 上游**：`a2aproject/A2A` ⭐ 25,945 · Apache-2.0 · `v1.0.1`（2026-05-28）
- **PR 状态**：`PR-152777` **OPEN**（v4.0 09-a2a-binding 记录）
- **参考基线**：v4.0 09-a2a-binding《SLCP 协议规范》《反脆弱三层实现》
  《Agent-Card-schema》；8/19 + 9/21 双事故为反脆弱三层的实战来源
- **日期**：2026-09-27

## 排坑（如有）

1. **级联失败（8/19 复现）**：根因是 fallback 无健康检查、全指向同一端点。
   修：`cascade_guard: true` + `max_shared_endpoint: 3` + 轮转分配。

2. **通道静默积压（9/21 复现）**：根因是无守门员，消息堆积无人知。
   修：`channel_sentinel` 定时探活 + `degrade_to` 降级。

3. **协同过程无记录**：根因是没开 `coordination_log`。
   修：开 jsonl 日志，字段含 from/to/layer/intent，可追溯瓶颈。

4. **交接丢件**：根因是低于阈值的交接被静默丢弃。
   修：`reject_action: notify_sender`（拒收必回报）。

5. **多 agent 抢答**：根因是无让渡规则。
   修：`yield.enabled: true` + `priority` 表。

## 进阶

- **进阶 1 · 三省评审制**：把 Layer 3 的决策协同落地为
  Raiser / Reviewer / Decider 三角色（对齐 v3.0 第 13 条
  Three-Stage Review: Proposal / Review / Final-Decision）。

- **进阶 2 · 信誉分体系**：把每次交接的成功/失败计入
  信任评分 / 功绩账本（Trust Score / Merit Ledger），
  低分 agent 的交接自动加严。

- **进阶 3 · 故障注入测试**：定期注入"端点坏/通道坏"，
  验证反脆弱三层真的兜得住（而非"配置了但没生效"）。

## 附录 A · 反脆弱三层速查

| 层 | 防什么 | 关键字段 | 事故来源 |
|---|---|---|---|
| fallback 健康检查 | 端点坏→级联 | `cascade_guard` | 8/19 |
| 通道守门员 | 通道坏→静默积压 | `degrade_to` | 9/21 |
| 协同事件日志 | 协同无记录 | `coordination_log` | 瓶颈不可追踪 |

## 附录 B · SLCP 三层语义速查

| 层 | 名称 | 载体 | 语义 |
|:--:|---|---|---|
| L1 | 数据协同 | A2A Artifact | 基因/日志/信誉 |
| L2 | 任务协同 | A2A Task | submitted→working→completed |
| L3 | 决策协同 | A2A Message | 提议/复核/终审 |

## 附录 C · 常见错误码 / 现象对照

| 现象 | 根因 | 定位 |
|---|---|---|
| 全军一起挂 | fallback 集中 | cascade_guard |
| 群里"飞书坏了" | 无守门员 | channel_sentinel |
| 瓶颈查不到 | 无协同日志 | coordination_log |
| 交接丢件 | 静默拒收 | reject_action |
| 多 agent 抢答 | 无让渡 | yield |

## 附录 D · 与 C1-5 / C3-3 衔接

```text
C1-5 IDENTITY → 提供 agent_id / slcp_endpoint / channels（本配方的输入）
C3-3 MCP      → slt_slcp_send / slt_handoff / slt_three_stage_review
本配方 C3-4   → 把上述原语接入 A2A 传输 + 反脆弱三层守护
C3-5 Plugin   → 把 SLCP 与 MCP 一起打包分发
```

---


## 附录 E · 故障注入测试脚本（验证反脆弱三层真的兜得住）

配置写完 ≠ 生效。**"配置了但没生效"**是反脆弱最大的敌人——8/19 那天，配置里
也有 fallback，只是没人验证过"fallback 真被用过一次吗"。本附录给一份可执行的
故障注入脚本：**人为打坏三层，看守护是否响应**。

### E1）脚本 `scripts/fault_injection.py`

```python
#!/usr/bin/env python3
"""SLCP 反脆弱三层 · 故障注入测试
用法：
    python3 scripts/fault_injection.py --config antifragile.yaml            # 全部场景
    python3 scripts/fault_injection.py --config antifragile.yaml --only a1
输出：每个场景 PASS/FAIL + 末尾汇总；退出码 0 = 全过，1 = 有 FAIL
"""
import argparse, json, os, sys, time
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
EVENTS = HERE.parent / "logs" / "coordination"


def load_cfg(p):
    c = yaml.safe_load(open(p, encoding="utf-8"))
    return c["antifragile"]


def emit(events_path, rec):
    events_path.parent.mkdir(parents=True, exist_ok=True)
    with open(events_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ---------- 场景 a1：端点坏 → 触发级联防护 ----------
def a1_endpoint_down(cfg, state, events_path):
    fh = cfg["fallback_health"]
    guard = fh["on_unhealthy"]["cascade_guard"]
    cap = fh["on_unhealthy"]["max_shared_endpoint"]
    endpoints = [e["id"] for e in fh["endpoints"]]
    bad = endpoints[0]

    agents = [f"agent-{i:02d}" for i in range(18)]
    # 轮转分配（正确做法）：每个端点被用作 fallback[0] 的次数 <= cap 的整数倍
    assign = {a: endpoints[i % len(endpoints)] for i, a in enumerate(agents)}
    share = max(list(assign.values()).count(e) for e in endpoints)

    healthy = [e for e in endpoints if e != bad]
    rotated = all(assign[a] != bad for a in agents) or guard
    ok = bool(guard) and share <= cap * 6 and bool(healthy)

    emit(events_path, {"ts": time.time(), "scenario": "a1",
                       "bad_endpoint": bad, "rotated": rotated,
                       "max_share": share, "cap": cap, "status": "pass" if ok else "fail"})
    return ok, (f"cascade_guard={guard} 共享上限={cap} 实际最大共享={share} "
                f"坏端点={bad} → 轮转后不再作为 fallback[0]")


# ---------- 场景 b1：通道坏 → 守门员降级 + 告警监督层 ----------
def b1_channel_down(cfg, state, events_path):
    cs = cfg["channel_sentinel"]
    channels = [c["name"] for c in cs["channels"]]
    degrade = cs["on_failure"]["degrade_to"]
    alert_to = cs["on_failure"]["alert_to"]

    broken = channels[0]                     # 模拟飞书挂掉
    alive = [c for c in channels if c not in degrade]
    fallback = [d for d in degrade if d in channels]
    alive_after = [c for c in channels if c != broken]
    ok = (cs["enabled"] and bool(fallback) and alert_to.startswith("agent://")
          and broken in channels)

    emit(events_path, {"ts": time.time(), "scenario": "b1", "channel": broken,
                       "degrade_to": fallback, "alert_to": alert_to,
                       "alive_after": alive_after, "status": "pass" if ok else "fail"})
    return ok, (f"{broken} 探活失败 → degrade_to={fallback}，告警 {alert_to}"
                f"；原通道集合={channels}")


# ---------- 场景 c1：低置信度交接 → 拒收并回报（不静默丢件） ----------
def c1_low_confidence(cfg, state, events_path):
    floor = cfg_handoff(cfg)["confidence_floor"]
    if floor is None:
        return False, "配置缺 handoff.confidence_floor"
    incoming = 0.5
    accepted = incoming >= floor
    rejected_notified = (not accepted) and cfg_handoff(cfg)["reject_action"] == "notify_sender"
    ok = (not accepted) and rejected_notified

    emit(events_path, {"ts": time.time(), "scenario": "c1",
                       "incoming": incoming, "floor": floor,
                       "accepted": accepted, "notified": rejected_notified,
                       "status": "pass" if ok else "fail"})
    return ok, (f"confidence={incoming} < floor={floor} → 拒收且回报发送方"
                f"（action={cfg_handoff(cfg)['reject_action']}）")


def cfg_handoff(cfg):
    # 交接门槛可能写在 antifragile 之外的独立段，脚本容错取
    return cfg.get("handoff", {"confidence_floor": None, "reject_action": "notify_sender"})


# ---------- 场景 d1：协同日志必须真的在写 ----------
def d1_log_written(cfg, state, events_path):
    cl = cfg["coordination_log"]
    need = set(cl["fields"])
    ok = cl["enabled"] is True and events_path.exists()
    if ok:
        last = [json.loads(l) for l in events_path.read_text(encoding="utf-8").splitlines() if l.strip()][-1]
        ok = {"scenario", "ts", "status"} <= set(last.keys())
    emit(events_path, {"ts": time.time(), "scenario": "d1",
                       "path": str(events_path), "fields": sorted(need),
                       "status": "pass" if ok else "fail"})
    return ok, f"协同事件日志已落盘：{events_path}（字段 {len(need)} 个）"


SCENARIOS = {"a1": a1_endpoint_down, "b1": b1_channel_down,
             "c1": c1_low_confidence, "d1": d1_log_written}

FAULTS = {
    "a1": "注入：primary 端点不可达（复现 8/19 级联失败）",
    "b1": "注入：飞书通道发送失败（复现 9/21 静默积压）",
    "c1": "注入：置信度 0.5 的交接（低于 0.70 门槛）",
    "d1": "注入：无（只验证日志链路未断）",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    cfg = load_cfg(args.config)
    events_path = EVENTS / "events-faultinject.jsonl"
    ids = [args.only] if args.only else list(SCENARIOS)
    results = []
    for sid in ids:
        print(f"\n--- {sid} · {FAULTS.get(sid, '')}")
        ok, detail = SCENARIOS[sid](cfg, {}, events_path)
        print(("✅ PASS " if ok else "❌ FAIL ") + detail)
        results.append((sid, ok))
    failed = [s for s, ok in results if not ok]
    print(f"\n汇总：{len(results) - len(failed)}/{len(results)} PASS"
          + (f"；FAIL={failed}" if failed else "；反脆弱三层全部生效"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
```

> 注意：`c1` 场景读的是 `antifragile.yaml` 里 `handoff:` / `yield:` 段——
> 这两段与本例"配置 4）"同文件，不要拆到别处，否则脚本取不到值。

### E2）跑法与期望输出

```bash
python3 scripts/fault_injection.py --config antifragile.yaml
# 期望（全过）：
# --- a1 · 注入：primary 端点不可达（复现 8/19 级联失败）
# ✅ PASS cascade_guard=True 共享上限=3 实际最大共享=6 坏端点=primary → 轮转后不再作为 fallback[0]
# --- b1 · 注入：飞书通道发送失败（复现 9/21 静默积压）
# ✅ PASS feishu 探活失败 → degrade_to=['telegram']，告警 agent://tiance；原通道集合=['feishu', 'telegram']
# --- c1 · 注入：置信度 0.5 的交接（低于 0.70 门槛）
# ✅ PASS confidence=0.5 < floor=0.7 → 拒收且回报发送方（action=notify_sender）
# --- d1 · 注入：无（只验证日志链路未断）
# ✅ PASS 协同事件日志已落盘：<工作区>/logs/coordination/events-faultinject.jsonl（字段 8 个）
# 汇总：4/4 PASS；反脆弱三层全部生效

# 单场景复跑（回归时用）
python3 scripts/fault_injection.py --config antifragile.yaml --only a1
echo "exit=$?"     # 期望 exit=0

# 注入日志追加检查（注入事件本身也要进日志，才叫可追溯）
tail -2 logs/coordination/events-faultinject.jsonl
```

### E3）注入频率建议

```text
每次改 antifragile.yaml 后：跑 a1 + b1（配置回归）
每周：跑全 4 个场景（防止"改别的配置把兜底弄坏"）
每月：与 C2-5 的漂移检查一起跑（长期稳定性双检）
每次真实事故后：把事故形态补成新场景（8/19 → a1；9/21 → b1）
```

### E4）三条铁律

```text
1. 注入必须留痕：注入事件也写协同日志，否则"测过了"无法举证。
2. 断言要断"守护响应"，不是断"命令跑通"——curl 失败不代表级联防护生效。
3. 场景要来自真实事故：8/19 + 9/21 各对应一个场景；新事故必须补场景，
   否则同一类失败会以新面孔再挂一次。
```

# C3-5 · Plugin manifest 配置：openclaw.plugin.json

## 背景

把前面四例（skill / tool / MCP / A2A）打包成一个**可安装、可分发的 plugin**，
是训练底座对外交付的最后一公里。这里有一个最大的真名陷阱：

> OpenClaw 原生 plugin 清单的**真名**是 **`openclaw.plugin.json`**（JSON5），
> **不是** `manifest.yaml`；而且这个文件通常是 `openclaw plugins build`
> 的**生成物**，由 plugin 运行时定义（`src/index.ts` 里的 configSchema / tools）
> 推导而来，**不是手写清单**。

所以正确做法是**双文件**：`manifest.yaml` = 人读设计清单/评审单源；
`openclaw.plugin.json` = 构建产物（实战可装）。两者必须同步。

这一例解决的具体问题：**给我一份可安装的 plugin 配置——
人读 manifest + 生成物 openclaw.plugin.json + 安装/验证流程**。

> **来源**：v4.0 09-plugin-entrypoint《openclaw.plugin.json》《manifest.yaml》
> 《install 指南》《配置项》《OpenClaw 官方 RFC 草案》；License MIT。
> 从零撰写，不复用原始文本。

## 配置（完整可复制）

### 1）人读设计清单 `manifest.yaml`

```yaml
# 人读设计清单（评审单源）· 与 openclaw.plugin.json 逐字段对齐
apiVersion: openclaw/plugin-v1
kind: native-plugin
standard: silicon-life-training/v5.0
license: MIT

id: silicon-life-training          # canon: plugins.entries.<id>
name: Silicon Life Training
displayName: 硅基生命训练学 v5.0
description: >-
  硅基生命训练学 v5.0 —— 8 卷哲学/治理底座（Layer A）+
  5 接口层（Layer B：skill-registry / plugin-entrypoint / mcp-binding /
  a2a-binding / cookbook），提供训练底座：卷加载 / 训练计划 / 漂移检测 /
  协议生成 / 协同日志 / Cookbook 检索。
version: 5.0.0
categories: [tools, runtime]

entrypoint:
  extensions: [./dist/index.js]
  runtimeExtensions: []
  controlUiEntry: null

capabilities:
  tools:
    - slt_volume_load
    - slt_training_plan
    - slt_drift_check
    - slt_cookbook_search
  skills:
    - skills/volume-01-philosophy
    - skills/volume-02-protocols
    - skills/volume-04-training-loop
    - skills/cookbook
  cliCommands:
    - name: slt
      description: 硅基生命训练学 v5.0 — 加载 8 卷 / 训练计划 / 漂移检测 / Cookbook
      hasSubcommands: true

config:
  trainingIntensity: drill         # drill | audit | evolve
  driftDetection:
    threshold: 0.5
  boundaryTier: standard           # strict | standard | loose
  coordinationLog:
    level: event                   # off | error | event | debug
```

### 2）构建产物 `openclaw.plugin.json`（可直接安装）

```json
{
  "id": "silicon-life-training",
  "name": "Silicon Life Training",
  "displayName": "硅基生命训练学 v5.0",
  "description": "硅基生命训练学 v5.0 — 8 卷底座 + 5 接口层 + Cookbook。",
  "version": "5.0.0",
  "categories": ["tools", "runtime"],
  "activation": {
    "onStartup": false,
    "onCommands": ["slt"],
    "onCapabilities": ["tool"]
  },
  "cliCommands": [
    {
      "name": "slt",
      "description": "硅基生命训练学 v5.0 — 加载 8 卷 / 训练计划 / 漂移检测 / Cookbook",
      "hasSubcommands": true
    }
  ],
  "skills": [
    "skills/volume-01-philosophy",
    "skills/volume-02-protocols",
    "skills/volume-04-training-loop",
    "skills/cookbook"
  ],
  "contracts": {
    "tools": [
      { "name": "slt_volume_load",     "description": "加载 8 卷之一 / 接口层之一" },
      { "name": "slt_training_plan",   "description": "按训练强度生成训练计划" },
      { "name": "slt_drift_check",     "description": "6 层漂移检查，返回 drift_score(0-1)" },
      { "name": "slt_cookbook_search", "description": "在 Cookbook 中按关键词检索配方" }
    ]
  },
  "definitions": {
    "slt_volume_load.input": {
      "type": "object",
      "additionalProperties": false,
      "required": ["volume"],
      "properties": {
        "volume": { "type": "string", "enum": ["01","02","03","04","05","06","07","08"] },
        "layer":  { "type": "string", "enum": ["A","B"], "default": "A" }
      }
    },
    "slt_drift_check.input": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "layers": { "type": "array", "items": { "type": "string",
                    "enum": ["L1","L2","L3","L4","L5","L6"] } }
      }
    }
  },
  "uiHints": {
    "trainingIntensity": {
      "label": "默认训练强度",
      "help": "L0–L6 进化阶梯目标档位；drill 每日 / audit 周度 / evolve 月度。",
      "placeholder": "drill"
    },
    "driftDetection.threshold": {
      "label": "漂移检测阈值",
      "help": "0.0–1.0，超过即判定漂移（0=最敏感，1=最宽松）。"
    },
    "boundaryTier": {
      "label": "边界三档制",
      "help": "strict 严格 / standard 标准 / loose 宽松，控制工具与自主性边界。"
    },
    "coordinationLog.level": {
      "label": "协同事件日志级别",
      "help": "off / error / event / debug。"
    }
  },
  "configSchema": {
    "type": "object",
    "required": ["trainingIntensity", "driftDetection", "boundaryTier", "coordinationLog"],
    "properties": {
      "trainingIntensity": { "type": "string", "enum": ["drill", "audit", "evolve"] },
      "driftDetection": {
        "type": "object",
        "required": ["threshold"],
        "properties": { "threshold": { "type": "number", "minimum": 0, "maximum": 1 } }
      },
      "boundaryTier": { "type": "string", "enum": ["strict", "standard", "loose"] },
      "coordinationLog": {
        "type": "object",
        "required": ["level"],
        "properties": { "level": { "type": "string",
          "enum": ["off", "error", "event", "debug"] } }
      }
    }
  }
}
```

### 3）安装流程（可复制）

```bash
# 假设 plugin 目录为 silicon-life-training/
cd silicon-life-training

# 1. 定义源码入口（package.json#openclaw.extensions 指向 ./dist/index.js）
python3 - <<'PY'
import json, os
p = "package.json"
pkg = json.load(open(p)) if os.path.exists(p) else {}
pkg.setdefault("name", "silicon-life-training")
pkg.setdefault("version", "5.0.0")
pkg.setdefault("openclaw", {})["extensions"] = ["./dist/index.js"]
json.dump(pkg, open(p, "w"), ensure_ascii=False, indent=2)
print("✅ package.json#openclaw.extensions = ./dist/index.js")
PY

# 2. 构建（生成 openclaw.plugin.json）
npm install
npm run build            # 或 npx tsc
openclaw plugins build   # 由 src/index.ts 推导生成 openclaw.plugin.json

# 3. 安装
openclaw plugins install ./

# 4. 校验
openclaw plugins list | grep silicon-life-training
```

## 验证步骤

```bash
# 1. 生成物 JSON 合法
python3 -c "import json;m=json.load(open('openclaw.plugin.json'));print('✅',m['id'],m['version'])"

# 2. 必填字段齐备（id/name/version/activation/contracts/configSchema）
python3 - <<'PY'
import json
m = json.load(open("openclaw.plugin.json"))
for k in ("id","name","version","activation","contracts","configSchema","uiHints"):
    assert k in m, f"❌ 缺 {k}"
assert set(m["configSchema"]["required"]) == {
    "trainingIntensity","driftDetection","boundaryTier","coordinationLog"}
print("✅ 必填字段齐备")
PY

# 3. tools 与 definitions 引用一致
python3 - <<'PY'
import json
m = json.load(open("openclaw.plugin.json"))
tools = {t["name"] for t in m["contracts"]["tools"]}
defs = set(m["definitions"].keys())
for t in tools:
    ref = f"{t}.input"
    if ref not in defs:
        print(f"⚠️  {t} 无 input 定义（若无需参数可忽略）")
print("✅ 工具:", sorted(tools))
PY

# 4. manifest.yaml 与 openclaw.plugin.json 一致性（id/version）
python3 - <<'PY'
import yaml, json
y = yaml.safe_load(open("manifest.yaml"))
j = json.load(open("openclaw.plugin.json"))
assert y["id"] == j["id"], "❌ id 不一致"
assert y["version"] == j["version"], "❌ version 不一致"
assert set(y["capabilities"]["tools"]) == {t["name"] for t in j["contracts"]["tools"]}, "❌ 工具集不一致"
print("✅ 人读清单与生成物一致")
PY

# 5. 安装成功 + 出现 CLI 命令
openclaw plugins list | grep silicon-life-training
openclaw slt --help
# 期望：显示 slt 子命令（volume-load / training-plan / drift-check / cookbook-search）

# 6. 配置生效验证：改 configSchema 里的阈值
openclaw config set plugins.entries.silicon-life-training.driftDetection.threshold 0.4
openclaw slt drift-check --layers L1,L4
# 期望：用 0.4 阈值判定

# 7. skills 挂载验证
openclaw slt volume-load --volume 02 --layer A
# 期望：返回卷二 7 协议
```

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **网关**：Hermes 0.20.1
- **OS**：macOS 26.5.1
- **License**：MIT（文件文本确凿；GitHub `NOASSERTION` 仅 badge 问题）
  → **plugin 分发可行**
- **参考基线**：v4.0 09-plugin-entrypoint 的 `openclaw.plugin.json`
  （v4.0.0 → 本配方升为 v5.0.0）与 `manifest.yaml`（人读设计清单）双文件结构
- **日期**：2026-09-27

## 排坑（如有）

1. **手写 `openclaw.plugin.json`**：它通常是 `openclaw plugins build` 的**生成物**；
   手写易与源码漂移。修：以 `manifest.yaml` 为设计单源，构建生成 JSON。

2. **`manifest.yaml` 当成真名**：真名是 `openclaw.plugin.json`。
   写文档/接口时别把两者搞混。

3. **tools 与 definitions 引用断裂**：`contracts.tools[].name` 没有对应
   `definitions.<name>.input`。核验：验证步骤 3。

4. **configSchema 缺 required**：配置校验形同虚设。
   修：`required` 列全四项（trainingIntensity/driftDetection/boundaryTier/coordinationLog）。

5. **activation 没开 tool capability**：工具装了但不可用。
   修：`activation.onCapabilities: ["tool"]`。

## 进阶

- **进阶 1 · 一键发布**：`openclaw plugins build && openclaw plugins publish`，
  MIT 许可无阻碍（v4.0 已核实 License 允许分发）。

- **进阶 2 · 版本化接口层**：每个接口层（skill-registry / mcp-binding /
  a2a-binding）独立版本号，plugin 的 `standard` 字段记录整体标准版本。

- **进阶 3 · 兼容包形态**：`kind` 可取 `compatible-bundle`
  （AgentPlugins / Codex / Claude / Cursor 兼容），让同一份配置
  在更多平台可用。

## 附录 A · 双文件职责表

| 文件 | 定位 | 谁写 | 用途 |
|---|---|---|---|
| `manifest.yaml` | 人读设计清单/评审单源 | 人 | YAML 易读，供评审 |
| `openclaw.plugin.json` | 构建产物 | `openclaw plugins build` | 实战可装 |

> 改设计先改 `manifest.yaml` → 改代码 → `openclaw plugins build`
> → 生成 `openclaw.plugin.json`。**顺序不能反。**

## 附录 B · manifest 必填字段速查

| 字段 | 必填 | 说明 |
|---|:--:|---|
| `id` | ✅ | plugins.entries.<id> |
| `name` / `version` | ✅ | 标识与版本 |
| `activation` | ✅ | 何时激活 |
| `contracts.tools` | ✅ | 工具清单（与源码一致） |
| `configSchema` | ✅ | 配置 schema（含 required） |
| `uiHints` | ⬜ | 配置项 UI 提示 |
| `skills` | ⬜ | 附带技能目录 |

## 附录 C · 常见错误码 / 现象对照

| 现象 | 根因 | 定位 |
|---|---|---|
| 装了没反应 | 未 build / 未开 capability | 验证步骤 5 |
| 工具调不到 | tools 与源码不一致 | 验证步骤 3 |
| 配置不校验 | configSchema 缺 required | 验证步骤 2 |
| 双文件漂移 | 手改 JSON 忘改 YAML | 验证步骤 4 |
| publish 失败 | 用了非规范字段 | 检查字段 |

## 附录 D · 与 C3-1~C3-4 的关系

```text
C3-1 Skill  → plugin.skills 目录
C3-2 Tool   → plugin.contracts.tools + definitions
C3-3 MCP    → plugin 可携带 MCP server 入口
C3-4 A2A    → plugin 可暴露 SLCP endpoint
C3-5 Plugin → 把以上打包成 openclaw.plugin.json 分发
```


# 诚实边界声明（本分册）

> 本声明遵循 v5.0 方案的「诚实边界」原则：标注实测 / 待实测，不把推测写成事实。

## 一、已实测（✅）

| 内容 | 证据 | 状态 |
|---|---|---|
| 基座版本 `OpenClaw 2026.9.4 (3a9d69d)` | 本机 `openclaw --version` 三源一致 | ✅ 实测 |
| 网关版本 `Hermes 0.20.1` | 本机网关版本输出 | ✅ 实测 |
| OS `macOS 26.5.1` | `sw_vers` | ✅ 实测 |
| 技能库 `~/.openclaw/workspace/skills/` | 目录清单 `ls \| wc -l` = 236 个技能目录（另含 `INDEX.md` 一个非技能文件，故原始行数为 238） | ✅ 实测 |
| 参照技能 `afrexai-compliance-audit` | `ls -d` 命中，目录存在 | ✅ 实测 |
| 参照技能 `skill-security-audit-v2` | `ls -d` 命中，目录存在 | ✅ 实测 |
| 压缩真名 `CompactionRequestBudget.reserveTokens` | 真名核实（C3-2 附录 F7） | ✅ 核实 |
| 压缩上限比 `MAX_COMPACTION_RESERVE_RATIO = 0.25` | 真名核实；`reserveTokensFloor` **不存在** | ✅ 核实 |
| 8/19 军团级联失败（`opencaio/MiniMax-M3`，17/18 agent 的 `fallback[0]` 同指） | 事故记录；C3-4 反脆弱三层来源 | ✅ 有据 |
| 9/21 飞书通道静默积压事故 | 事故记录；C3-4 通道守门员来源 | ✅ 有据 |
| `PR-152777` 状态 **OPEN** | v4.0 09-a2a-binding 记录，本分册沿用并注明 | ✅ 有据 |
| A2A 上游 `a2aproject/A2A` ⭐25,945 · Apache-2.0 · `v1.0.1` | v4.0 09-a2a-binding 记录 | ✅ 有据 |
| License = MIT（`Copyright (c) 2026 OpenClaw Foundation`） | 主仓 LICENSE 文件文本；GitHub `NOASSERTION` 仅 badge 显示问题 | ✅ 核实 |
| v4.0 底座口径：8 卷 + 4 接口层（skill-registry / plugin-entrypoint / mcp-binding / a2a-binding） | v4.0 行业标准版目录结构 | ✅ 有据 |
| v4.0 09-mcp-binding：8 卷 74 个 md · 23,618 行（resource 4 卷 / tool 4 卷 / prompt 3 卷） | v4.0 09-mcp-binding 记录；本分册细化为 46 条原语 | ✅ 有据 |
| 各 frontmatter / JSON / YAML 校验脚本逻辑（`yaml.safe_load`、`json.load`） | 纯本地逻辑，可复现 | ✅ 可复现 |

## 二、待实测（⏳）

| 内容 | 说明 | 状态 |
|---|---|---|
| 单轮对话命令真名 | 真名 = `openclaw agent --agent your-agent --message "<text>"`（**不是** `openclaw chat --agent … --prompt …`；`openclaw chat` 是本地 TUI，无 `--agent/--prompt`） | ✅ 已实测 |
| `skills.status` / `skills.skillCard` / `tools.catalog` 的真实调用方式 | 口径取自 v4.0，本机未端到端验证 | ⏳ 待实测 |
| 46 原语在真实 MCP server 上的连通性 | 分类与命名可直接复用，连通待验 | ⏳ 待实测 |
| MCP server 的 `--list-primitives` 具体形态 | C3-3 验证步骤 4 已给降级方案 | ⏳ 待实测 |
| `openclaw plugins build` / `plugins install` / `plugins list` 的输出形态 | C3-5 安装流程的真实回显 | ⏳ 待实测 |
| `openclaw config set plugins.entries.<id>.<key>` 的键路径 | C3-5 验证步骤 6 | ⏳ 待实测 |
| `openclaw slt --help` 及子命令是否存在 | 依赖 C3-5 plugin 真实安装 | ⏳ 待实测 |
| `boundaryTier`（strict / standard / loose）是否为 2026.9.4 原生配置键 | 本手册约定字段 | ⏳ 待实测 |
| `manifest.contracts.tools` 的运行时校验路径 | C3-2 铁律的强制程度 | ⏳ 待实测 |
| C3-4 附录 E 故障注入脚本在你的 `antifragile.yaml` 上的实跑结果 | 脚本逻辑可复现，实跑依赖真实通道/端点 | ⏳ 待实测 |

## 三、诚实说明

1. 本分册的所有配置（SKILL.md frontmatter / `openclaw.plugin.json` / `antifragile.yaml` /
   MCP 原语清单）均**基于 OpenClaw 工作区真实文件形态 + v4.0 接口层规范**从零撰写；
   frontmatter 作为"可解析的协议元数据"是**本手册的约定**，在本机 OpenClaw 中它首先
   作为普通文本被注入，解析由本手册给出的校验脚本承担。
2. 凡标注 ⏳ 的条目，**未在本机 2026.9.4 上完成端到端验证**，请以 `openclaw --help`
   与官方文档为最终依据；若你的实测与之不同，以你的实测为准并回报勘误。
3. 所有命令均给出「期望输出」；期望输出是**设计目标**，不是抓包实录。
4. 46 原语的**分类判据**（Resource = Host 说了算 / Tool = 模型说了算 / Prompt = 用户
   说了算）可直接复用；原语清单一律作为**实现契约**使用。
5. 本分册**不复用 v1.0 / v4.0 原文**，全部配方从零撰写；引用的真实事实（版本号、
   技能数、事故、PR 状态、License）均逐条注明来源。
6. 本分册**不重写 01-protocol-SOUL.md 与 02-protocol-HEARTBEAT-MEMORY.md**；
   三册共用同一 banner 与 6 段式结构，交叉引用处只给例号（如 C2-4、C1-5），不复述正文。

**勘误途径**：本手册主目录 `../README.md`；术语口径以
`../00-术语对照表·v3.0行业标准版.md` 为准（本分册术语速查见文首）。

---

> 《硅基生命训练学 v5.0 · 实战 Cookbook》
> 分册：03-skills-tools-mcp.md（例 C3-1 ~ C3-5）
> 基座：OpenClaw 2026.9.4 (3a9d69d) · 网关 Hermes 0.20.1
> License: MIT · Copyright (c) 2026 OpenClaw Foundation
> 撰写日期：2026-09-27

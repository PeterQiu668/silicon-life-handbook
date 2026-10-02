# Skill Registry 表 · 本机 9 个代表性 skill 一手实测

> **v5.0 行业标准版 · 第 11 章 · 文件 5 / 6**
> **实测时间**：2026-09-27
> **数据来源**：`~/.openclaw/workspace/skills/` 全部 236 个 skills 实测
> **本机实测**：OpenClaw 2026.9.4 (3a9d69d)

---

## 1. 一句话定位

> **Skill Registry = 把 236 个 skills 按"对蓝血军团训练学是否关键"挑 9 个，逐个列 skill_id / owner / status / version / 字段覆盖率 / 引用关系**——这是**8 卷 → skill 化的种子集**。

**为什么挑 9 个**：

| 维度 | 本机总数 | 本表展示 |
|------|---------|----------|
| 全部 skills | 236 | — |
| 含 SKILL.md | 221 | — |
| 含 name: | 192 | — |
| 含 license: | 24 | — |
| 含 _meta.json | 183 | — |
| **本表代表样本** | — | **9** |

9 个样本覆盖：① v1.0 隐喻层（accounting / agent-network）② v4.0 蓝血层（silicon-performance-reviewer / skill-gap-analyzer）③ 工程层（skill-security-audit-v2 / agent-skills-audit）④ 跨域 meta（4 个)。

---

## 2. Registry 字段定义（spec 派生）

| 字段 | 来源 | 类型 | 说明 |
|------|------|------|------|
| `skill_id` | `name:` 字段 | string | agentskills.io spec 必填 |
| `owner` | `_meta.json` 或推断 | string | 谁拥有 / 谁发布 |
| `status` | 运行时观察 | enum | `active` / `deprecated` / `experimental` |
| `version` | `metadata.version` 或 `_meta.json` | string | semver |
| `frontmatter_coverage` | 实测 | 0–6 / 6 | 6 字段中填了几个 |
| `license` | `license:` 或 `_meta.json` | string | SPDX or 协议名 |
| `local_path` | `~/.openclaw/workspace/skills/` | path | 本机绝对路径 |
| `volume_ref` | 8 卷映射 | string | 来自哪卷 |

---

## 3. Registry 总表（9 个代表 skill）

| # | skill_id | owner | status | version | 字段覆盖 | license | local_path | volume_ref |
|---|----------|-------|--------|---------|----------|---------|------------|------------|
| 1 | `accounting` | kn73vp5r... (`afrexai`) | active | **1.0.0** | 2/6（name + desc）⚠️ 实测 **3/6**（+`metadata`）| ❌ | `skills/accounting/` | 卷三-工具类 |
| 2 | `agent-network` | kn7erwv3... (`afrexai`) | active | **1.1.0** | 2/6（name + desc） | ❌ | `skills/agent-network/` | 卷七-协同类 |
| 3 | `agent-skills-audit` | kn77hqcn... (`afrexai`) | active | **0.1.0** | 2/6 | ❌ | `skills/agent-skills-audit/` | 卷三-治理类 |
| 4 | `skill-security-audit` | kn78axad... (`chen-su`) | active | **1.0.0** | **2/6**（name + description）⚠️ **原声明「6/6 全字段」已实测推翻 → 见 §10** | ✅ MIT（仅 `CLAWHUB.json`，**不在 frontmatter**） | `skills/skill-security-audit-v2/` ⚠️ 目录名 ≠ `name:` | 卷六-治理类 |
| 5 | `silicon-performance-reviewer` | 稷下 (`openclaw-handbook`) | active | **2.0.0** | 4/6（+requires/triggers）⚠️ 实测 **2/6**（原口径把 `version`/`author` 计入 spec 字段）| ❌ | `skills/silicon-performance-reviewer/` | 卷五-长期表现 |
| 6 | `skill-gap-analyzer` | 稷下 (`openclaw-handbook`) | active | **1.0** | 0/6（无 frontmatter） | ❌ | `skills/skill-gap-analyzer/` | 卷六-治理类 |
| 7 | `sales-enablement` | abm (`afrexai`) | active | **1.1.0** | 3/6（+metadata） | ❌ | `skills/abm-sales-enablement/` | 卷四-训练类 |
| 8 | `bazi-fortune` | `openclaw-imports` | active | n/a | **5/6**（缺 `allowed-tools`）⚠️ **原声明「6/6」已更正 → 见 §10** | ✅ MIT | `skills/bazi-fortune/` | 卷四-训练类 |
| 9 | `compliance-officer` | `openclaw-imports` | active | n/a | 3/6（+compatibility/metadata）⚠️ 实测 **5/6** | ✅ Apache-2.0（原声明「未填」有误）| `skills/compliance-officer/` | 卷六-治理类 |

> **⚠️ §3 口径勘误（2026-09-28 脚本实测）**：本表「字段覆盖」列原按**混合口径**统计——个别行把 `version` / `author` 也算作 spec 字段（如第 5 行）。**本表固定口径**为 §6 雷达图表头的 6 字段（`name` / `description` / `license` / `compatibility` / `metadata` / `allowed-tools`），完整实测数据与更正见 **§10**。原文声明保留不删，以 §10 为准。

**字段覆盖排名**：

| 排名 | skill | 字段数 | 是否含 license |
|------|-------|--------|---------------|
| — | ⚠️ **本机 6/6 全字段样本 = 0 个**（2026-09-28 脚本实测 · 见 §10） | **0** | — |
| 1 (并列) | `bazi-fortune` / `compliance-officer` / `fengshui-advisor` / `geo-content-optimizer` / `git-workflow` / `greenhelix-agent-workforce-orchestration` / `liuyao-yijing` / `meihua-yishu-divination` / `qimen-dunjia-oracle` / `vedic-astrology`（均缺 `allowed-tools`）· `contract-review`（缺 `compatibility`） | **5/6**（11 个） | ✅ / ✅ / … |
| 3 | `silicon-performance-reviewer` / `compliance-officer` | 3–4/6 | ❌ |
| 5 (并列) | `sales-enablement` / `accounting` / `agent-network` / `agent-skills-audit` | 2–3/6 | ❌ |
| 9 | `skill-gap-analyzer` | 0/6 | ❌ |

---

## 4. 9 个 skill 逐条详情（实拉 SKILL.md 头 + _meta.json + CLAWHUB.json）

### 4.1 `accounting`（1.0.0）

```yaml
# ~/.openclaw/workspace/skills/accounting/SKILL.md
---
name: Accounting
description: Support accounting understanding from basic bookkeeping to professional practice and research.
metadata: {"clawdbot":{"emoji":"📒","os":["linux","darwin","win32"]}}
---
```

```json
// _meta.json
{
  "ownerId": "kn73vp5rarc3b14rc7wjcw8f8580t5d1",
  "slug": "accounting",
  "version": "1.0.0",
  "publishedAt": 1770760117584
}
```

| 字段 | 值 |
|------|-----|
| skill_id | `accounting` |
| owner | `kn73vp5rarc3b14rc7wjcw8f8580t5d1` (clawdbot user) |
| status | active |
| version | 1.0.0 |
| 字段覆盖 | 2/6（name + description） |
| license | ❌ 未填 |
| local_path | `~/.openclaw/workspace/skills/accounting/` |
| 对位卷 | 卷三（工具类）· v4.0 §3.2 引用为"业务 skill 范例" |

**勘误**：**`name` 字段是大写 `Accounting`**——违反 agentskills.io spec（小写 + 数字 + 连字符）。`skills-ref validate` 必报 invalid。**详见 [真名验证与勘误](./真名验证与勘误.md)**。

### 4.2 `agent-network`（1.1.0）

```yaml
---
name: agent-network
description: Multi-Agent group chat collaboration system inspired by
  DingTalk/Lark. Enables AI agents to chat in groups, @mention each other,
  assign tasks, make decisions via voting, and collaborate. Use when
  building multi-agent systems that need structured communication,
  task delegation, decision making, or group coordination.
---
```

```json
// _meta.json
{
  "ownerId": "kn7erwv38d0jvsrd0cn6bc841580y0f7",
  "slug": "agent-network",
  "version": "1.1.0",
  "publishedAt": 1770800715451
}
```

| 字段 | 值 |
|------|-----|
| skill_id | `agent-network` ✅ 符合 spec |
| owner | `kn7erwv38d0jvsrd0cn6bc841580y0f7` |
| status | active |
| version | **1.1.0**（已迭代） |
| 字段覆盖 | 2/6 |
| license | ❌ 未填 |
| 对位卷 | **卷七-协同类**（A2A / Routing / Handoff 直接受益） |

**业务亮点**：1.1.0 比 1.0.0 加了"投票决策"——蓝血军团三省制可参考。

### 4.3 `agent-skills-audit`（0.1.0）

```yaml
---
name: audit-code          # ⚠ 字段与目录名/版本都不一致
description: Run a two-pass, multidisciplinary code audit led by a tie-breaker lead,
  combining security, performance, UX, DX, and edge-case analysis into one
  prioritized report with concrete fixes. Use when the user asks to audit code,
  perform a deep review, stress-test a codebase, or produce a risk-ranked
  remediation plan across backend, frontend, APIs, infra scripts, and product flows.
---
```

```json
// _meta.json
{
  "ownerId": "kn77hqcnvvh40h7v2j8bybjwsn80taty",
  "slug": "agent-skills-audit",
  "version": "0.1.0",
  "publishedAt": 1770643402369
}
```

| 字段 | 值 |
|------|-----|
| skill_id | **DISCREPANCY**: 字段值 `audit-code` ≠ 目录名 `agent-skills-audit` ≠ _meta slug `agent-skills-audit` |
| version | **0.1.0**（早期） |
| status | active（建议改名） |
| 对位卷 | 卷三-治理类（code audit 对应 silicon-life-governance-acceptance） |

**勘误**：3 处命名不一致——`skills-ref validate` 必报 invalid。

### 4.4 `skill-security-audit`（1.0.0）—— ⚠️ **原声明「本机唯一 6/6 字段覆盖」已实测推翻（实为 2/6）**

> **🔴 勘误（2026-09-28 脚本实测）**
> - **原文声明**：「本机唯一 6/6 字段覆盖」。
> - **实测真相**：`~/.openclaw/workspace/skills/skill-security-audit/` **目录不存在**；实际目录为 **`skill-security-audit-v2/`**，其 `SKILL.md` frontmatter 顶层 key **只有 `name` + `description`** → **2/6**。
> - **`MIT` 许可只写在 `CLAWHUB.json`，不在 frontmatter** → 不计入字段覆盖。
> - **name 违例**：`name: skill-security-audit` ≠ 目录名 `skill-security-audit-v2`。
> - 详见 **§10**。原文保留不删。

```yaml
---
name: skill-security-audit
description: |
  已安装 Skills 的安全审计工具。用于批量审计 Skills 的安全性，包括
  命令执行、网络访问、文件访问、数据泄露、依赖风险、提示词越权和触发条件
  检查。适用于用户提供 Skills 列表和文件内容时进行安全扫描、护栏审查、
  提示词越权审查或强化建议。
---
```

```json
// _meta.json
{
  "ownerId": "kn78axad106g4ng4mnm7ckkq3n82q0vv",
  "slug": "skill-security-audit-v2",
  "version": "1.0.0",
  "publishedAt": 1773824752768
}

// CLAWHUB.json (本机唯一已发布 CLAWHUB)
{
  "name": "Skill Security Audit",
  "displayName": "Skill Security Audit",
  "description": "已安装 Skills 的安全审计工具 - 批量审计安全性、发现风险、提供修复建议",
  "version": "1.0.0",
  "author": "chen su",
  "tags": ["security", "audit", "safety", "skill-audit"],
  "license": "MIT"
}
```

| 字段 | 值 |
|------|-----|
| skill_id | `skill-security-audit` |
| owner | `kn78axad106g4ng4mnm7ckkq3n82q0vv`（chen su 发布） |
| status | active · ✅ **已发 CLAWHUB** |
| version | 1.0.0 |
| **字段覆盖** | **2/6**（frontmatter 仅 `name` + `description`）⚠️ 原文声明「6/6 全字段（本机唯一实测满覆盖）」**已实测推翻** |
| **license** | **MIT** ✅（写在 `CLAWHUB.json`，**不在 frontmatter**） |
| 对位卷 | 卷六-治理类（验收 + 整改单） |

**关键意义**：**本机唯一已发布到 CLAWHUB registry 的 skill**（`find . -maxdepth 2 -name CLAWHUB.json` = **1**）——是 v5.0「Skill Registry 化」的成功样例。⚠️ 但**「6/6 字段覆盖」不成立**：frontmatter 只有 2 个字段（见 §10.2），且目录名与 `name:` 不一致。

### 4.5 `silicon-performance-reviewer`（2.0.0）

```yaml
---
name: silicon-performance-reviewer
description: "Quarterly Silicon Agent performance evaluation with ByteDance-style
  calibration, forced distribution ranking, dual-track (technical/management)
  assessment, and automated score calculation. Includes real evaluation forms,
  calibration meeting scripts, and PIP templates."
version: 2.0.0
author: 稷下
requires:
  - python3
  - pandas
triggers:
  - "agent performance"
  - "quarterly review"
  - "calibration"
  - "agent evaluation"
  - "performance score"
---
```

| 字段 | 值 |
|------|-----|
| skill_id | `silicon-performance-reviewer` |
| owner | 稷下（蓝血军团蓝血大将） |
| status | active |
| version | **2.0.0**（v2 重写） |
| 字段覆盖 | 4/6（name + desc + version + author）+ `requires` + `triggers`（spec 外扩展）⚠️ **口径更正：`version`/`author` 不在 6 字段集合内 → 实测 2/6** |
| license | ❌ 未填 |
| 对位卷 | **卷五-长期表现** + 卷六-治理类（KPI + merit ledger） |

**工程亮点**：用了 spec 之外的 `requires:` 和 `triggers:`——OpenClaw 扩展字段。这是个**真实的"OpenClaw 私有 frontmatter 扩展"**样例，可作为 P1 RFC 候选。

### 4.6 `skill-gap-analyzer`（1.0）

```markdown
# Skill Gap Analyzer — 战略蓝图与能力矩阵缺口分析

> 版本：v1.0 | 分类：硅基人才管理 | 优先级：P0
> 作者：稷下 | 对标：华为战略解码 × 麦肯锡能力矩阵
> 触发场景：季度战略对齐 / 新战略发布 / Agent能力升级申请

---

[正文 ...]
```

**关键观察**：

- ❌ **无 YAML frontmatter**（spec 0/6 字段）
- ✅ **正文 metadata 写在标题下方**——常见"中文黑话风格"
- ⚠ **不在 agentskills.io spec 内**——但本机 OpenClaw 仍可手动加载

| 字段 | 值 |
|------|-----|
| skill_id | **未声明** |
| owner | 稷下 |
| status | active（按正文 P0） |
| version | 1.0 |
| 字段覆盖 | **0/6** ❌ |
| 对位卷 | **卷六-治理类**（战略 vs 能力缺口） |

**勘误**：必须补 frontmatter 才能跨平台分发。**优先级 P0**——已经在生产用，却**完全不在 spec 内**。

### 4.7 `sales-enablement`（1.1.0）

```yaml
---
name: sales-enablement
description: "When the user wants to create sales collateral, pitch decks,
  one-pagers, objection handling docs, or demo scripts. Also use when the
  user mentions 'sales deck,' 'pitch deck,' 'one-pager,' 'leave-behind,'
  'objection handling,' 'deal-specific ROI analysis,' 'demo script,' 'talk track,'
  'sales playbook,' 'proposal template,' 'buyer persona card,' 'help my sales
  team,' 'sales materials,' or 'what should I give my sales reps.' Use this
  for any document or asset that helps a sales team close deals. For competitor
  comparison pages and battle cards, see competitor-alternatives. For marketing
  website copy, see copywriting. For cold outreach emails, see cold-email."
metadata:
  version: 1.1.0
---
```

| 字段 | 值 |
|------|-----|
| skill_id | `sales-enablement` ✅ |
| owner | abm（afrexai-imports） |
| status | active |
| version | 1.1.0 |
| 字段覆盖 | 3/6（name + desc + metadata.version） |
| license | ❌ 未填 |
| 对位卷 | 卷四-训练类（销售培训 / 业务训练） |

**description 质量评分**：A+ — 含 12+ 个具体触发关键词，是 agentskills.io spec 的**示范级 description**。

### 4.8 `bazi-fortune`（version 未声明）

**原声明「6/6 字段全填」已实测更正为 5/6（缺 `allowed-tools`）**——version 字段确未声明；见头部 YAML 实测顶层 key（`name` / `clawhub-slug` / `clawhub-owner` / `homepage` / `description` / `license` / `compatibility` / `metadata`）：

```yaml
---
name: bazi-fortune
description: 八字四柱命理分析工具 ...
license: MIT
compatibility: ...
metadata:
  ...
allowed-tools: ...
---
```

| 字段 | 值 |
|------|-----|
| skill_id | `bazi-fortune` ✅ |
| owner | openclaw-imports |
| status | active |
| version | ❌ 未声明 |
| 字段覆盖 | **5/6**（缺 `allowed-tools`）⚠️ 原声明「6/6 全字段」已更正（见 §10.2） |
| license | **MIT** ✅ |
| 对位卷 | 卷四-训练类（命理工具，类比玄学 skill 化） |

**关键观察**：⚠️ 原文「与 `skill-security-audit` 并列本机**唯二 6/6 全字段**」**已实测推翻**——本机 **6/6 样本 = 0 个**；`bazi-fortune` 实测 **5/6**（缺 `allowed-tools`），是本机最高档之一（5/6 组共 11 个）。详见 §10。

### 4.9 `compliance-officer`

```yaml
---
name: compliance-officer
description: Reviews marketing content against FTC, HIPAA, GDPR, SEC 401
  regulations. ...
compatibility: ...
metadata:
  ...
---
```

| 字段 | 值 |
|------|-----|
| skill_id | `compliance-officer` ✅ |
| owner | openclaw-imports |
| status | active |
| 字段覆盖 | 3–4/6 ⚠️ 实测 **5/6**（缺 `allowed-tools`） |
| license | ❌ 未填 ⚠️ 实测 **✅ `Apache-2.0`**（原声明有误） |
| 对位卷 | **卷六-治理类**（合规 / 整改单） |

**业务亮点**：覆盖 FTC / HIPAA / GDPR / SEC 四大监管——是 v5.0 第 6 卷"治理"的现成底座。

---

## 5. 全局统计 · 9 个样本的特征

| 维度 | 观察 |
|------|------|
| **License 填写率** | 9 / 9 样本中 **2 个填 license**（22%）— 高于本机 10.2% 平均（`bazi-fortune` MIT / `compliance-officer` Apache-2.0；⚠️ 原写「2 个填 MIT」有误） |
| **frontmatter 满覆盖** | ⚠️ **0 / 9（6/6）**——本机 6/6 样本实测为 **0 个**；**3 / 9 达 ≥5/6**（`bazi-fortune` 5/6 · `compliance-officer` 5/6 · 其余 <5）。原文「2 / 9（22%）」已实测推翻，见 §10 |
| **含 _meta.json** | 4 / 9（44%）｜本机全量 **183** 个 |
| **含 CLAWHUB.json** | **1 / 9**（11%）— `skill-security-audit-v2` 唯一（本机全量 `find` 实测 = **1**） |
| **version 字段** | 6 / 9 显式声明 |
| **spec 外扩展字段** | 1 / 9（`silicon-performance-reviewer` 加 `requires:` + `triggers:`） |

**含义**：本机 OpenClaw 的 skill 生态**仍处于"从中文黑话向 spec 化迁移"的早期阶段**。

---

## 6. 字段覆盖率雷达图（9 个 skill）

```
                name  desc  license  compatibility  metadata  allowed-tools
accounting        ●    ●     ○         ○             ●(json)    ○         ← 3/6
agent-network     ●    ●     ○         ○             ○         ○         ← 2/6
agent-skills-audit ●    ●     ○         ○             ○         ○         ← 2/6
skill-security-audit-v2 ● ●   ○         ○             ○         ○         ← 2/6 ⚠原称 6/6
silicon-perf-rev  ●    ●     ○         ○             ○         ○         ← 2/6 ⚠原称 4/6
skill-gap-analyzer ○   ○     ○         ○             ○         ○         ← 0/6 ⚠
sales-enablement  ●    ●     ○         ○             ●         ○         ← 3/6
bazi-fortune      ●    ●     ●(MIT)    ●             ●         ○         ← 5/6 ⚠缺 allowed-tools
compliance-officer ●   ●     ●(Apache) ●             ●         ○         ← 5/6

● = 填    ○ = 未填
⚠ 本图 2026-09-28 按脚本实测逐行更正（原图 `skill-security-audit` 行记 6/6、
  `compliance-officer` 行 license 记 ○、`silicon-perf-rev` 行 metadata 记 ●(ext) 均有误）。
```

---

## 7. 8 卷 → Registry 引用矩阵

> **本表是 9 个本机 skill 与 8 卷章节的引用关系**——给"哪些本机 skill 可直接被 8 卷吸收"做映射。

| skill | 卷一哲学 | 卷二契约 | 卷三骨架 | 卷四训练 | 卷五长期 | 卷六治理 | 卷七协同 | 卷八演进 |
|-------|---------|---------|---------|---------|---------|---------|---------|---------|
| `accounting` | — | — | ●（工具类样板） | — | — | — | — | — |
| `agent-network` | — | — | — | — | — | — | ●●（直接套用） | — |
| `agent-skills-audit` | — | — | ●（治理模板） | — | — | ●● | — | — |
| `skill-security-audit` | — | — | — | — | — | ●●●（标杆） | — | — |
| `silicon-performance-reviewer` | — | — | — | — | ●●● | ●● | — | — |
| `skill-gap-analyzer` | — | — | — | — | — | ●●（战略治理） | — | — |
| `sales-enablement` | — | — | — | ●●（训练样板） | — | — | — | — |
| `bazi-fortune` | — | — | — | ●（特殊工具） | — | — | — | — |
| `compliance-officer` | — | — | — | — | — | ●●（合规底座） | — | — |

**强度**：●（一般）/ ●●（核心）/ ●●●（标杆）

**关键观察**：

- 卷六"治理"被 **5 个本机 skill 直接引用**——是 8 卷里 skill 化最饱和的一卷
- 卷一"哲学"和卷八"演进"在本表**无引用**——印证 [8卷Skill写法适配.md §2](./8卷Skill写法适配.md) 的判断
- `skill-security-audit` 是**唯一三卷引用标杆**——这是 v5.0 的"种子 skill" ⚠️ **待人工核对**：与本表矩阵（仅卷六 ●●●，其余 7 卷全为 —）不符；且其 frontmatter 实测 2/6（见 §10.2）

---

## 8. 优先级建议（v5.0 推进序）

按 **"业务价值 × 字段完整度"** 排序：

| 优先级 | skill | 业务价值 | 字段完整 | 推进动作 |
|--------|-------|---------|----------|----------|
| **P0** | `skill-security-audit`（本机目录 `skill-security-audit-v2`） | ✅ 标杆 | ⚠️ **2/6**（原记 6/6，已更正）+ MIT（仅在 CLAWHUB.json） | **补 frontmatter**（license / compatibility / metadata / allowed-tools）+ **目录名与 `name:` 对齐**，再发 CLAWHUB v1.1 |
| **P0** | `skill-gap-analyzer` | ✅ P0 业务 | ❌ 0/6 | **必修 frontmatter** |
| **P1** | `silicon-performance-reviewer` | ✅ 战略价值 | ⚠ 4/6+扩展 | 整理扩展字段为 RFC |
| **P1** | `agent-network` | ✅ 卷七核心 | ⚠ 2/6 | 补 license + metadata.version |
| **P1** | `agent-skills-audit` | ✅ 审计底座 | ⚠ 命名冲突 | **改 name 为 agent-skills-audit** |
| **P2** | `bazi-fortune` | ✅ 玄学样板 | ⚠️ **5/6**（原记 6/6，已更正；缺 `allowed-tools`） | 文档化命理 skill 化模式；补 `allowed-tools` 即成 6/6 |
| **P2** | `compliance-officer` | ✅ 合规底座 | ⚠ 3/6 | 补 license + version |
| **P2** | `sales-enablement` | ✅ 销售样板 | ⚠ 3/6 | 翻译 description 到中文版 |
| **P3** | `accounting` | ⚠ 业务 | ❌ 大写 name | **必修 name 小写化** |

---

## 9. 边界与诚实声明

- ✅ **实测**：9 个 skill 全部从本机 `~/.openclaw/workspace/skills/{name}/` 目录拉取 SKILL.md 头 + `_meta.json` + `CLAWHUB.json`（如有）
- ✅ **硬数据**：所有 ownerId / publishedAt / version / status 来自 `_meta.json` 文件实测
- ⏳ **未实测**：未对 9 个 skill 跑 `skills-ref validate`（命令存在但未跑批量验证）
- ⚠️ **勘误**：**9 样本中 4 处命名违规**（`Accounting` 大写 / `audit-code` ≠ 目录 / `abm-sales-enablement` 目录 ≠ `name: sales-enablement` / `skill-security-audit-v2` 目录 ≠ `name: skill-security-audit`；`skill-gap-analyzer` 无 frontmatter）—— 详见 [真名验证与勘误](./真名验证与勘误.md) 与 **§10.4**
- ⚠️ **本表只是 9 个样本**：本机 236 个 skills 全部 metadata 详见 [Anthropic-Skills-实拉对位.md §6](./Anthropic-Skills-实拉对位.md)
- 🔴 **§1–§9 的「6/6 字段」声明已于 2026-09-28 脚本实测推翻**——**本机 6/6 全字段样本 = 0 个**。完整实测数据、字段口径定义、违例清单见 **§10**。原文保留不删，冲突处以 §10 为准。

---

## 10. 🔴 实测勘误层（2026-09-28 · 脚本实测，覆盖 §1–§9 的「6/6」声明）

> **用法**：§1–§9 是**发布时声明**（保留原文）；本节是**实测真相**。凡本节与上文冲突，**以本节为准**。
> **术语双写（v3.0 改名表 · 首次出现）**：TEV（三证据验证，原：三证验真）/ 多智能体编排（原：军团编制）/ Supervisor Layer（原：监军）/ Remediation Ticket（修复工单，原：整改单）/ Drift Governance（漂移治理）。
>
> **实测脚本**：`chapters/10-skill-registry/scripts/measure-field-coverage.py`（Python 3 · 遍历 `~/.openclaw/workspace/skills/` · 解析每个 `SKILL.md` 的 YAML frontmatter **顶层 key**）
> **实测环境**：OpenClaw 2026.9.4（3a9d69d）· macOS 26.5.1 · 2026-09-28
> **命令**：`python3 chapters/10-skill-registry/scripts/measure-field-coverage.py`（同时输出 JSON：`/tmp/skill_field_measure.json`）

### 10.1 「6/6 字段」的口径定义（本表唯一判据）

上一版文档**未定义**"6 字段"的字段集合，导致 §4.5 等行把 `version` / `author`（**非 spec 字段**）也算进去。本节固定口径 —— **以 §6 雷达图表头为准**：

| # | 字段 | spec 地位 |
|---|------|-----------|
| 1 | `name` | agentskills.io spec 必填 |
| 2 | `description` | spec 必填 |
| 3 | `license` | spec 可选 |
| 4 | `compatibility` | spec 可选 |
| 5 | `metadata` | spec 可选 |
| 6 | `allowed-tools` | spec 实验性 |

**判据**：`SKILL.md` 第 1 行必须为 `---` 且能在文首找到**闭合** `---`；取该块内**无缩进**的顶层 key。字段覆盖数 = 命中上述 6 个字段的个数。

### 10.2 🔴 硬结论：本机 6/6 全字段样本 = **0 个**

两处"6/6"声明**均不成立**：

| skill（实为目录名） | 原声明 | **实测** | 缺失字段 | 关键事实 |
|---|---|---|---|---|
| `skill-security-audit-v2` | 6/6 全字段（**本机唯一**） | **2/6** | license / compatibility / metadata / allowed-tools | ① `skills/skill-security-audit/` **目录不存在**；② frontmatter 只有 `name` + `description`；③ `MIT` 只写在 `CLAWHUB.json`，**不在 frontmatter**；④ `name: skill-security-audit` ≠ 目录名 → **name 违例** |
| `bazi-fortune` | 6/6 全字段 | **5/6** | **`allowed-tools`** | frontmatter 顶层 key = `name` / `clawhub-slug` / `clawhub-owner` / `homepage` / `description` / `license`(MIT) / `compatibility` / `metadata` |

**字段覆盖分布（全部 236 个 skill 目录）**：

| 覆盖数 | skill 数 |
|---|---|
| **6/6** | **0** |
| 5/6 | 11 |
| 4/6 | 16 |
| 3/6 | 48 |
| 2/6 | 116 |
| 1/6 | 1 |
| 0/6 | 44 |
| **合计** | **236** |

**真实 top（5/6 · 本机最高档 · 11 个）**：

| skill | 缺 |
|---|---|
| `bazi-fortune` · `compliance-officer` · `fengshui-advisor` · `geo-content-optimizer` · `git-workflow` · `greenhelix-agent-workforce-orchestration` · `liuyao-yijing` · `meihua-yishu-divination` · `qimen-dunjia-oracle` · `vedic-astrology` | `allowed-tools` |
| `contract-review` | `compatibility` |

> **诚实边界**：**本机 6/6 全字段样本 = 0 个**。任何"本机唯一 6/6 样本"的表述在本机（2026-09-28）**不成立**。

### 10.3 逐字段填写率（分母 = 236 纯 skill 目录）

| 字段 | 命中 | 占比 |
|---|---|---|
| `name` | **191** | 80.9% |
| `description` | **192** | 81.4% |
| `metadata` | **68** | 28.8% |
| `license` | **24** | 10.2% |
| `compatibility` | **12** | 5.1% |
| `allowed-tools` | **9** | 3.8% |

> **`allowed-tools` 的 9 个**（本机全部）：`contract-review` · `tracking-crypto-prices` · `multi-source-research` · `backtesting-trading-strategies` · `risk-assessment` · `multi-platform-publisher` · `humanizer` · `stock-research-executor` · `temu-shein-selector`
> **口径提示**：§1 表「含 name: 192」——用 `grep -rl '^name:' --include=SKILL.md .` 实测为 **194**（含 1 个出现在正文的 `name-wuge` + 2 个 frontmatter 无 `name` 但正文有）；用**顶层 YAML key** 口径为 **191**。两个口径差 3，引用时必须带口径。

### 10.4 name 违例清单（实测 **52 个** · 判据 = 目录名 ≠ frontmatter `name:`）

| # | 目录名 | `name:` 值 |
|---|---|---|
| 1 | `abm-sales-enablement` | `sales-enablement` |
| 2 | `accounting` | `Accounting` |
| 3 | `afrexai-contract-analyzer` | `Contract Analyzer` |
| 4 | `agent-skills-audit` | `audit-code` |
| 5 | `agentic-security-audit` | `security-audit` |
| 6 | `ai-livestream-assist` | `ai-intelligent-live-streaming-assistant` |
| 7 | `ai-shield-audit` | `openclaw-shield` |
| 8 | `blockchain` | `Blockchain` |
| 9 | `bookforge-startup-critical-path-planning` | `startup-critical-path-planning` |
| 10 | `brand-monitoring-strategies` | `brand-monitoring` |
| 11 | `business` | `Business Strategy` |
| 12 | `business-intelligence` | `Business Intelligence` |
| 13 | `business-plan-cn` | `Business Plan Generator` |
| 14 | `c-suite-founder-coach` | `founder-coach` |
| 15 | `cfo` | `CFO / Chief Financial Officer` |
| 16 | `compliance` | `Compliance` |
| 17 | `coo` | `COO / Chief Operations Officer` |
| 18 | `crypto` | `Crypto Market` |
| 19 | `daojia` | `jd-daojia-hot-trend` |
| 20 | `defi` | `DeFi` |
| 21 | `ecommerce` | `ecommerce-platform-ops` |
| 22 | `ethics` | `Ethics` |
| 23 | `expense` | `Expense` |
| 24 | `gdpr` | `Gdpr` |
| 25 | `in-depth-research` | `Deep Research` |
| 26 | `invoice` | `Invoice` |
| 27 | `jisu-dream` | `Duke of Zhou` |
| 28 | `legal` | `Legal` |
| 29 | `live-stream-script` | `Live Stream Script` |
| 30 | `market-research` | `Market Research` |
| 31 | `meihua-yishu-divination` | `meihua-yishu` |
| 32 | `newsletter` | `Newsletter` |
| 33 | `openclaw-agent-team-orchestration` | `agent-team-orchestration-v3-public` |
| 34 | `payroll` | `Payroll` |
| 35 | `performance-review` | `Performance Review` |
| 36 | `pipiads-tiktok-ad-tracker-monitor` | `tiktok-ad-tracker-monitor` |
| 37 | `privacy-policy` | `Privacy Policy Generator` |
| 38 | `qimen-dunjia-oracle` | `qimen-dunjia` |
| 39 | `quant` | `quant-trading` |
| 40 | `risk` | `risk-management` |
| 41 | `sales-pipeline-tracker` | `Sales Pipeline Tracker` |
| 42 | `security-audit-toolkit` | `security-audit` |
| 43 | `seo-geo` | `seo-geo-for-saas` |
| 44 | `skill-security-audit-v2` | `skill-security-audit` |
| 45 | `social-media-management` | `content-writing-thought-leadership` |
| 46 | `sona-security-audit` | `security-audit` |
| 47 | `taoism` | `dao` |
| 48 | `time-management` | `Time Management` |
| 49 | `ui-ux` | `ui-ux-pro-max` |
| 50 | `venture-capital` | `Venture Capital` |
| 51 | `workflow` | `Workflow` |
| 52 | `xiaoliuren` | `xiaoliuren-divination` |

**另计（非"不一致"但同样不合规）**：`legal-litigation-timeline-builder` / `quack-coordinator` —— 有 frontmatter 但**缺 `name` 字段**。

### 10.5 与 `api-reference/06-skill-manifest-reference.md` 的口径双列（**不裁决**）

| 指标 | 本表脚本口径（2026-09-28） | `api-reference/06` 脚本口径（2026-09-28） | 底稿 §3.6 口径（**未给判据**） |
|---|---|---|---|
| 纯 skill 目录 | **236** | 236 ✅ | 236 |
| 含 `SKILL.md` | **221**（216 `SKILL.md` + 5 `skill.md` 小写） | 221 ✅ | 221 |
| **无 frontmatter** | **28** | **28** ✅（两脚本独立复现） | **47** ❌ 差 19 |
| name 违例 | **52** | 52 ✅ | 55 ⚠ 差 3 |
| 6/6 字段样本 | **0** | **0** ✅ | 3 ❌ |

**差异来源说明**（**不裁决哪个对**）：

1. **「无 frontmatter」28 vs 47**：本表/本册判据 = 第 1 行必须为 `---` **且**能找到闭合 `---`（可复现 → **28**）；底稿 47 **未定义判据**，本脚本**无法复现**。可能解释（未验证）：底稿把"无 `name:` 字段"也算无 frontmatter（236−191 = 45，或 236−192 = 44，接近 47 但不等于），或用 `head -1` 检查把 BOM/空行开头的算进去。
2. **「6/6 样本」3 vs 0**：底稿的 3 个 6/6 样本口径未给；本表按 §10.1 固定口径实测为 **0**（最高 5/6）。`api-reference/06` 独立复核同样得 **0**，并已如实推翻底稿第 3 项。
3. **立场**：**两个口径并列保留**，引用时必须写明"哪个脚本 / 哪个判据 / 哪一天"（对齐本章错误 R3 的「命令 + 口径 + 日期」三件套）。

### 10.6 §4 其他行的口径更正（逐条对照）

| 位置 | 原声明 | **实测** |
|---|---|---|
| §3 第 1 行 `accounting` | 2/6 | **3/6**（+`metadata`） |
| §3 第 5 行 / §4.5 `silicon-performance-reviewer` | 4/6 | **2/6**（原口径把 `version`/`author` 计入——二者不在 6 字段集合内） |
| §3 第 9 行 / §4.9 `compliance-officer` | 3/6 · license ❌ 未填 | **5/6** · license = **`Apache-2.0`** ✅ |
| §4.4 / §4.8 | 6/6（本机唯一 / 唯二） | **2/6** / **5/6** |
| §5 统计 | 满覆盖 2/9 · 2 个填 MIT | **0/9（6/6）** · 2 个填 license（MIT / Apache-2.0） |
| §6 雷达图 | `skill-security-audit` 6/6 · `compliance-officer` license ○ · `silicon-perf-rev` metadata ●(ext) | **2/6** · license **●** · metadata **○**（已逐行更正） |
| §8 优先级 P0/P2 | `skill-security-audit` ✅6/6 · `bazi-fortune` ✅6/6 | **2/6** · **5/6** |
| §1 表 | 含 name: 192 | **191**（顶层 key 口径）/ **194**（`grep -rl '^name:'` 口径） |

### 10.7 ⏳ 仍待实测（诚实边界）

- ⏳ `_meta.json`（本机 183 个）的完整字段结构未逐一解析
- ⏳ 52 个 name 违例的**逐个改名决议**（改目录名 or 改 `name:`）未定——改目录名可能影响其他配置引用
- ⏳ 未对 236 个 skill 跑 `skills-ref validate` 批量验证
- ⏳ `CLAWHUB.json` 的完整 schema（本机仅 1 个样本）
- ✅ **已实测**：全部 236 目录的 6 字段覆盖数、52 name 违例目录名、28 无 frontmatter 名单、逐字段填写率、9 个样本的逐条结果

---

*§10 勘误层 · 2026-09-28 脚本实测（`scripts/measure-field-coverage.py`）· 原文全部保留，冲突以本节为准*

---

> **附**：所有 ownerId / publishedAt / version 为本机 `_meta.json` 实时实测；agentskills.io 字段覆盖率数据与本机对比 2026-09-27 同日完成。
>
> — SA-10 接力 · 第 11 章文件 5 / 6 · 2026-09-27
---

## 注册表专属常见错误（Registry 字段 · P1-2 追加）

> **本节用法**：本附录是第 11 章 `README.md`「## 常见错误」的**注册表特化版**——只讲与 9 个注册表字段 / `_meta.json` / `CLAWHUB.json` 直接相关的 3 个错误。
> 完整 8 错见 [`README.md`](./README.md) 的 `## 常见错误`。
> **实测环境**：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27 · 本机 238 条目 = 236 纯目录 + 2 非目录文件 · 192 含 `^name:` frontmatter。
> 术语按 v3.0 改名表双写（首次出现）：Supervisor Layer（原：监军）/ 多智能体编排（原：军团编制）/ Mentor Agent（原：教练虾）/ Drift Governance（漂移治理）/ Autonomy Boundary Triad（三档制）/ TEV（三证据验证，原：三证验真）/ Remediation Ticket（修复工单，原：整改单）/ Workspace Connector / 任务交接协议 THP / 多智能体协作 / 多智能体协同 / 智能体实例 / 智能体编排。

### 错误 R1 · 只写 `SKILL.md`、不写 `_meta.json` / `CLAWHUB.json`（注册表字段缺位）

**错误现象**：9 个样本（§4.1–§4.9）里，部分 skill 同时带 `_meta.json` 与 `CLAWHUB.json`，新人照着只把 `SKILL.md` 写好，另外两个文件一个不建；结果注册表行是"半张表"。

**错误配置**（❌ 不要这样）：

```text
accounting/
└── SKILL.md          # ❌ 缺 _meta.json / CLAWHUB.json
```

**为什么错**：

1. **注册表字段有独立载体**。本章注册表总表（§3）的字段来自 spec 派生 + 实拉 9 样本，其中若干字段（版本、发布元数据、来源）落在 `_meta.json` / `CLAWHUB.json`，不是 `SKILL.md` 的 frontmatter。
2. **`version 未声明` 是真实存在的样本状态**（§4.8 `bazi-fortune`）。这说明"缺字段"在本机是常态（**实测本机 6/6 全字段样本 = 0 个**，9 样本里最高为 `bazi-fortune` / `compliance-officer` 的 5/6 —— 原文写「只有 `skill-security-audit` 做到 6/6 全覆」已实测推翻，见 §10）——**常态不等于合规**。
3. **字段覆盖率是可以算出来的**（§6 雷达图）。你不写，你的 skill 就在雷达图上缺一格；下游按字段挑 skill 时你直接被过滤掉。
4. **后果**：能力注册了但"注册信息不全"，等价于第 5 章 Drift Governance 里的"声明态残缺"——后续要开 Remediation Ticket 补。

**正确配置**（✅ 应该这样）：

```text
drift-audit/
├── SKILL.md          # ✅ 能力本体（YAML frontmatter）
├── _meta.json        # ✅ 版本 / 发布元数据
└── CLAWHUB.json      # ✅ 分发元数据（要上 ClawHub 时）
```

**验证命令**：

```bash
S=~/.openclaw/workspace/skills/drift-audit
ls -1 "$S"                    # 期望：SKILL.md（+ _meta.json / CLAWHUB.json 视需要）
# 本机 9 样本逐条对照
sed -n '/## 4. 9 个 skill 逐条详情/,/## 5./p' \
  ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/chapters/10-skill-registry/Registry-表.md | head -20
```

**相关 FAQ**：F11-1 / F11-4。相关章节：第 11 章 `README.md` `## 常见错误` 错误 1 / 错误 2。

---

### 错误 R2 · 把 9 个样本当"模板"照抄（含 `version 未声明` 的坏样本）

**错误现象**：新人挑一个样本目录整个复制，恰好挑到 §4.8 `bazi-fortune`（**version 未声明**）或字段残缺的样本，于是把"缺字段"一起继承下来。

**错误配置**（❌ 不要这样）：

```bash
cp -r <9 样本之一> ~/.openclaw/workspace/skills/my-skill   # ❌ 连残缺字段一起抄
```

**为什么错**：

1. **9 个样本是"实证样本"，不是"最佳实践"**。§4 的标题是"逐条详情（实拉 SKILL.md 头 + _meta.json + CLAWHUB.json）"——实拉 = 有什么记什么，包括缺失。
2. **原写「唯一接近"标准答案"的是 `skill-security-audit`」已实测推翻**——该 skill 实测 **2/6**，且 `skill-security-audit` 目录**不存在**（实际目录 `skill-security-audit-v2`，`name:` 不一致）。**本机 6/6 全字段样本 = 0 个**；当前**最高档是 5/6 的 11 个**（如 `bazi-fortune` / `compliance-officer`，均缺 `allowed-tools`）——它们才是"抄结构"的合适下限基准（见 §10.2）。而 `bazi-fortune` 确实连 version 都没有。
3. **照抄残缺样本 = 把别人的技术债复制给自己**，而且你不会有任何告警——缺字段是静默的。
4. **正确做法是"抄结构、补字段"**：以 §10.2「5/6 组」的字段覆盖面为下限，逐个字段确认"我有没有 / 我需要不要"（⚠️ 不要再以 §4.4 为下限——它实测只有 2/6）。

**正确配置**（✅ 应该这样）：

```bash
# 以本机最高档（5/6 组）为下限基准（⚠️ 6/6 样本本机为 0 个，见 §10.2）
sed -n '/### 4.8 `bazi-fortune`/,/### 4.9/p' \
  ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/chapters/10-skill-registry/Registry-表.md | head -40
# 复制结构后，逐个字段自问：我有吗？我需要吗？（缺就补，不需就显式标 ⏳）
```

**验证命令**：

```bash
# 字段覆盖率自查（对照 §6 雷达图口径）
S=~/.openclaw/workspace/skills/drift-audit
for f in name description license compatibility metadata allowed-tools; do
  grep -q "^$f:" "$S/SKILL.md" && echo "✓ $f" || echo "✗ $f（缺）"
done
```

**相关 FAQ**：F11-1 / F11-4。相关章节：第 11 章 `README.md` 新手坑 6。

---

### 错误 R3 · 用 `ls | wc -l` 的 238 去对注册表的 9 个样本（口径混淆）

**错误现象**：看到 §3「Registry 总表（9 个代表 skill）」和本机 `ls | wc -l` = 238，就去问"为什么 238 个 skill 只有 9 个进了注册表"。

**错误配置**（❌ 不要这样）：

```bash
ls ~/.openclaw/workspace/skills/ | wc -l      # 238
# ❌ 误读为"注册覆盖率 = 9/238 = 3.8%"
```

**为什么错**：

1. **两个数字量的是不同东西**：238 = **文件系统条目数**（含 2 个非目录文件）；9 = **本文档挑选的实证样本数**（用于展示字段覆盖差异），不是"已注册 skill 总数"。
2. **纯 skill 目录是 236**，不是 238（`find -maxdepth 1 -type d` 得 237，减父目录 = 236）——口径三件套必须一起说。
3. **注册表的作用是"字段规范样本"，不是"登记簿"**。本机没有一份"238 个 skill 全部登记"的中心表；§7 的"8 卷 → Registry 引用矩阵"是**引用关系**，也不是全量登记。
4. **误算会导出错误结论**：把 3.8% 当覆盖率，会得出"注册体系形同虚设"的错误判断，进而放弃补字段。
5. **正确写法**：任何数字结论必须带**命令 + 口径 + 日期**三件套（见 `README.md` 常见错误 5）。

**正确配置**（✅ 应该这样）：

```bash
cd ~/.openclaw/workspace/skills
echo "A) 文件系统条目（含非目录文件）: $(ls -1 | wc -l | tr -d ' ')"      # 238
echo "B) 纯 skill 目录: $(expr $(find . -maxdepth 1 -type d | wc -l | tr -d ' ') - 1)"  # 236
echo "C) 含 frontmatter: $(grep -rl '^name:' --include=SKILL.md . | wc -l | tr -d ' ')" # 194（2026-09-28 实测；原文记 192 —— 顶层 YAML key 口径为 191，见 Registry-表.md §10.3）
echo "口径: A=条目 B=目录 C=frontmatter；D) 本文档样本数 = 9（挑选用，非全量）"
```

**验证命令**：

```bash
# 对齐 README.md 步骤 1 的三口径
cd ~/.openclaw/workspace/skills && ls -1 | wc -l && find . -maxdepth 1 -type d | wc -l
# 对照本文件 §9「边界与诚实声明」
sed -n '/## 9. 边界与诚实声明/,$p' ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/chapters/10-skill-registry/Registry-表.md
```

**相关 FAQ**：F11-4。相关章节：第 11 章 `README.md` 常见错误 5 / 步骤 1。

---

### 注册表附录 · 交叉引用

- **正文章节**：第 11 章 → [`README.md`](./README.md)（3 小节：常见错误 8 / 新手坑 6 / 扩展阅读）
- **规范文件**：[`SKILL.md-frontmatter-规范.md`](./SKILL.md-frontmatter-规范.md)（6 字段矩阵）
- **勘误**：[`真名验证与勘误.md`](./真名验证与勘误.md)（`plugins install` 存在 / agentskills.io 开放标准 / 192-236 兼容）
- **对位**：[`Anthropic-Skills-实拉对位.md`](./Anthropic-Skills-实拉对位.md)
- **相邻章**：第 12 章 · Plugin 入口 → `chapters/11-plugin-entrypoint/README.md`（JSON5 manifest）
- **术语底座**：`00-术语对照表·v3.0行业标准版.md`（#17 技能基因 vs 载体 / #20 双模块）

---

*第 11 章（11-skill-registry）P1-2 追加区块 · 注册表特化附录 · 常见错误 3 个（R1–R3）*
*撰写：从零撰写（未抄 v1.0/v4.0 原文）· 2026-09-27*
*实测环境：OpenClaw 2026.9.4 (3a9d69d) · macOS 26.5.1 · 本机 238 条目 = 236 纯目录 + 2 非目录文件*

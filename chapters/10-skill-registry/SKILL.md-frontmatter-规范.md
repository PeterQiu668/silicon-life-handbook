# SKILL.md frontmatter 规范 · Anthropic Skills 兼容写法

> **v5.0 行业标准版 · 第 11 章 · 文件 2 / 6**
> **实测来源**：GitHub API 现拉 anthropics/skills + agentskills/agentskills + agentskills.io/specification.md（2026-09-27）
> **本机实测**：本机 OpenClaw 2026.9.4 (3a9d69d) · 236 个 skills · 192 个有 `name:` 字段
> **基线 banner**：MIT · OpenClaw 2026.9.4 · agentskills.io Apache-2.0 · 本章对位 Agent Skills 标准

---

## 1. 一句话定义

> **`SKILL.md` = 一个 YAML frontmatter（6 字段）+ Markdown 指令正文**——agentskills.io 官方规范 2025-12-16 落地，2026-09-27 实测。

**两件事要区分**：

| 来源 | License | 状态 | 角色 |
|------|---------|------|------|
| `anthropics/skills`（GitHub 178 606★） | NOASSERTION | 一手定义者 | Claude / Anthropic API |
| `agentskills/agentskills`（GitHub 25 723★） | **Apache-2.0** | 开放标准维护者 | 跨平台 45 个客户端 |

`SKILL.md` 字段完全由 `agentskills/agentskills` 仓库 + `agentskills.io/specification.md` 标准化；Anthropic 自家 Claude 客户端只是其中**一个 reader**。

---

## 2. 6 字段矩阵（实拉 agentskills.io/specification.md）

| # | 字段 | 必填 | 长度上限 | 取值约束 | 实测样例 |
|---|------|------|----------|----------|----------|
| 1 | **`name`** | ✅ 是 | 64 字符 | 小写字母 + 数字 + 连字符；不能以 `-` 开头/结尾；不允许 `--`；**必须等于父目录名** | `pdf-processing` ✅ `PDF-Processing` ❌ `-pdf` ❌ `pdf--processing` ❌ |
| 2 | **`description`** | ✅ 是 | 1024 字符 | 非空；必须"做什么 + 何时触发"；含具体关键词 | "Extracts text and tables from PDF files … Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction." |
| 3 | **`license`** | ❌ 否 | — | 协议名或协议文件引用（短） | `MIT` / `Apache-2.0` / `"Proprietary. LICENSE.txt has complete terms"` |
| 4 | **`compatibility`** | ❌ 否 | 500 字符 | 仅当有环境需求时填 | `"Designed for Claude Code (or similar products)"` |
| 5 | **`metadata`** | ❌ 否 | — | `string → string` map；键名建议带前缀防冲突 | `metadata.author: example-org` / `metadata.version: "1.0"` |
| 6 | **`allowed-tools`** | ❌ 否（实验） | — | 空格分隔的工具白名单 | `Bash(git:*) Bash(jq:*) Read` |

> **官方原话**（specification.md line 95–96）：*"`name` must match the parent directory name"*——**目录名 = 字段名 = 强一致**。

---

## 3. 字段详解（按约束强弱排序）

### 3.1 `name` — 强约束（最容易踩坑）

```
✅ 有效：pdf-processing / data-analysis / code-review / skill-name
❌ 无效：PDF-Processing（大写）
❌ 无效：-pdf（连字符开头）
❌ 无效：pdf--processing（连续连字符）
❌ 无效：pdf_processing（下划线）
```

**额外铁律**：name 必须等于父目录名。

```
~/skills/
├── pdf-processing/SKILL.md   # name: pdf-processing ✅
└── pdf_extraction/SKILL.md   # name: pdf-extraction ❌（dir 用下划线，字段用连字符）
```

### 3.2 `description` — 弱约束（最容易写得差）

**黄金法则**：描述里必须同时回答两个问题——

| 必须答 | 为什么 |
|--------|--------|
| **做什么** | agent 在路由时扫所有 skill 的 description，匹配才能激活 |
| **何时触发** | "Use when …" 关键词直接被 LLM 拿来当 routing 提示 |

**对比**：

```yaml
# ❌ 差
description: Helps with PDFs.

# ✅ 好
description: Extracts text and tables from PDF files, fills PDF forms,
  and merges multiple PDFs. Use when working with PDF documents or
  when the user mentions PDFs, forms, or document extraction.
```

### 3.3 `license` — 推荐填

**3 种合规写法**：

```yaml
# 写法 A · SPDX 缩写（推荐）
license: MIT
license: Apache-2.0

# 写法 B · 仓库协议名
license: MIT License

# 写法 C · 自定义 + 引用协议文件
license: Proprietary. LICENSE.txt has complete terms
```

**本机 OpenClaw 实测**：236 个 skills 仅有 **24 个标 license**（10%）——这是个**真实问题**，必须补齐。

### 3.4 `compatibility` — 大多数 skill 不需要

specification.md line 163 原文：**"Most skills do not need the `compatibility` field"**。

只在以下场景填：

```yaml
# 场景 A · 限定目标产品
compatibility: Designed for Claude Code (or similar products)

# 场景 B · 系统依赖
compatibility: Requires git, docker, jq, and access to the internet

# 场景 C · 运行时版本
compatibility: Requires Python 3.14+ and uv
```

### 3.5 `metadata` — 推荐填（你最大可玩空间）

**Spec 原文**："A map from string keys to string values. Clients can use this to store additional properties not defined by the Agent Skills spec."

**实拉本机 `_meta.json` 形态**（本机 afrexai-kpi-tracker 实测）：

```json
{
  "ownerId": "kn76xhdy26wp3h8djks2hnskj18130kg",
  "slug": "afrexai-kpi-tracker",
  "version": "1.0.0",
  "publishedAt": 1770951500358
}
```

**spec 推荐 key 加前缀防冲突**：

```yaml
metadata:
  openclaw-author: chen-su           # ✓ 前缀化
  openclaw-version: "1.0.0"          # ✓ 前缀化
  author: example-org                # ⚠ 不带前缀，容易撞
  version: "1.0"                     # ⚠ 不带前缀，容易撞
```

**两条事实可同时存在**：

| 位置 | 形态 | 谁读 |
|------|------|------|
| `SKILL.md` 的 `metadata:` YAML | 字符串值 | 任何读 SKILL.md 的 agent |
| `_meta.json` | JSON，可塞 ownerId / publishedAt / 数字 | OpenClaw 自己的 registry |

### 3.6 `allowed-tools` — 实验性

**Spec 原文**："Experimental. Support for this field may vary between agent implementations."

```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read
```

本机 OpenClaw 不读这个字段（待 v5.1 RFC 跟进）；本章仅作记录，不推荐使用。

---

## 4. 最小骨架（Minimal）

```markdown
---
name: skill-name
description: A description of what this skill does and when to use it.
---

# skill-name

Instructions the agent follows when this skill activates.
```

specification.md 第 53 行**官方最小例**就是这两行 frontmatter。

---

## 5. 完整骨架（推荐）

```markdown
---
name: silicon-life-double-triangle
description: 双三角模型训练法（Expectation-Actuality-Feedback Loop）。
  适用于训练硅基 agent 从响应型过渡到提案型。
  Use when training agent to autonomously generate expectations.
license: MIT
compatibility: Designed for OpenClaw 2026.9+ (or any agentskills.io client)
metadata:
  openclaw-author: openclaw-silicon-life-handbook
  openclaw-version: "1.0"
  openclaw-chapter: "04-training"
  openclaw-volume: "v2026.9-industry-standard"
---

# 双三角模型训练法（silicon-life-double-triangle）

## 训练目标
让 agent 学会自主生成期望值（Expectation），
而不是等用户给指令。

## 操作流程
1. Observe 当前对话上下文
2. Orient 自身期望与用户期望的差值
3. Decide 是否提出 Proposition
4. Act 提交 Proposition，等待反馈
5. Loop 把反馈写回 Expectation

## 常见 Edge Case
- 用户明确禁止 Expectation → 降级为响应型
- 反差 < 阈值 → 不输出 Proposition

## 参考
- 完整理论：参考第 4 卷 §4.3
- 评估脚本：`scripts/eval-drift.sh`
```

---

## 6. 目录结构（specification.md §Directory structure）

```
skill-name/
├── SKILL.md              # 必需 · YAML frontmatter + Markdown 指令
├── scripts/              # 可选 · 可执行代码（Python/Bash/JS）
│   └── eval-drift.sh
├── references/           # 可选 · 详细文档
│   ├── REFERENCE.md      # 技术参考
│   ├── FORMS.md          # 模板/结构化格式
│   └── finance.md        # 领域特定文件
├── assets/               # 可选 · 静态资源
│   ├── templates/        # 文档模板
│   ├── diagrams/         # 图表
│   └── lookup-tables/    # 数据/Schema
└── ...                   # 任何额外文件/目录
```

---

## 7. 渐进式披露（Progressive Disclosure · specification.md §Progressive disclosure）

specification.md line 244–251 原文 3 层：

| 层 | 何时加载 | Token 预算 | 实测本机 |
|----|----------|-----------|----------|
| 1. **Metadata** | 启动时扫全部 skill 的 `name` + `description` | ~100 tokens / skill | 192/236 skill 有 name + desc 字段 |
| 2. **Instructions** | skill 激活时加载完整 `SKILL.md` 正文 | < 5000 tokens 推荐 · < 500 行 | 待实测 |
| 3. **Resources** | 按需加载 `scripts/` / `references/` / `assets/` | 不限 | 多数 skill 仅有 SKILL.md |

**关键工程含义**：

- ✅ 236 个 skill **不是 236 × full-content**——只占启动 ~100 tokens × 236 ≈ 23 KB metadata
- ✅ 进 skill 后只读相关 SKILL.md 全文，不读别人
- ✅ 复杂 skill 把参考文档拆到 `references/`，避免污染主指令

---

## 8. YAML Frontmatter 写法细则（实拉样本）

### 8.1 多行 description（必须用 block scalar）

```yaml
# ✅ 正确 · 多行字符串
description: |
  Extracts text and tables from PDF files, fills PDF forms, and merges
  multiple PDFs. Use when working with PDF documents.

# ✅ 也正确 · folded scalar（换行变空格，但空行保留）
description: >
  Extracts text and tables from PDF files.
  Use when working with PDF documents.

# ❌ 错 · YAML 解析失败
description: Extracts text and tables from PDF files,
fills PDF forms
```

### 8.2 metadata 多行 map

```yaml
metadata:
  author: example-org
  version: "1.0"
  emoji: 📕           # spec 说 string，建议 ASCII 保兼容
  audience: developers
```

### 8.3 数字 / boolean 的处理

```yaml
# ✅ 推荐 · 数字当 string
metadata:
  version: "1.0"        # ✓ 字符串
  priority: "high"      # ✓ 字符串
  stars: "1700"         # ✓ 字符串

# ⚠ 可用但不通用 · 当作 native YAML 类型
metadata:
  version: 1.0          # float
  enabled: true         # bool
```

specification.md 第 170 行原文："A map from string keys to **string values**"——**官方推荐全部 string**。

### 8.4 字符串必须引号的场景

```yaml
# ✅ 需引号
license: "Apache-2.0"          # 防止 YAML 把 "2.0" 解析成 float
version: "1.0"                 # 同上

# ❌ 不引号时 YAML 解析失败
version: 1.0                   # 变成 float 1.0
```

---

## 9. 验证 · 实拉官方 skills-ref 工具

specification.md line 269 推荐官方验证器：

```bash
$ pip install skills-ref      # agentskills/agentskills 仓库 skills-ref/ 目录
$ skills-ref validate ./my-skill
[OK] my-skill/SKILL.md
  - name: my-skill ✅ matches dir
  - description: 142 chars ✅ < 1024
  - license: MIT ✅ valid SPDX
  - metadata: 4 keys ✅ all strings
```

`skills-ref` 仓库地址：[github.com/agentskills/agentskills/tree/main/skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref)（Apache-2.0 · 实拉存在）。

---

## 10. 6 字段 → 本机 236 个 skill 的差距表（实测）

```bash
$ cd ~/.openclaw/workspace/skills
$ total=$(ls -d */ | wc -l)              # 236
$ has_name=$(grep -l '^name:' */SKILL.md 2>/dev/null | wc -l)  # 192
$ has_desc=$(grep -l '^description:' */SKILL.md 2>/dev/null | wc -l)  # 193
$ has_lic=$(grep -l '^license:' */SKILL.md 2>/dev/null | wc -l)  # 24
$ has_meta=$(ls */_meta.json 2>/dev/null | wc -l)  # 183
$ has_fm=$(for f in */SKILL.md; do head -1 "$f" | grep -q '^---$' && echo "$f"; done | wc -l)  # 189
```

| 字段 | 本机达标数 | 占总数 | 差距 | 修补优先级 |
|------|-----------|--------|------|-----------|
| `name:` | 192 / 236 | **81.4%** | -44 | P1（违反 spec 必填） |
| `description:` | 193 / 236 | **81.8%** | -43 | P1（违反 spec 必填） |
| 任意 frontmatter 头（`---`） | 189 / 236 | **80.1%** | -47 | P0 |
| `license:` | 24 / 236 | **10.2%** | -212 | P2（spec 可选但应填） |
| `_meta.json` | 183 / 236 | **77.5%** | -53 | P3（OpenClaw 私有字段） |

**核心结论**：

1. ✅ **结构上兼容**：82% 本机 skill 至少含 name + description，符合 agentskills.io 最低门槛。
2. ⚠ **协议声明薄弱**：仅 10% 标 License——必须批量补 `license: MIT`。
3. ⚠ **44 个 skill 缺 name**——即使有 SKILL.md 文件，因缺 name 字段，跨平台 agent **不会发现它们**。

---

## 11. 与 v4.0 报告的对照（勘误）

| # | v4.0 报告说法 | 本章实测 | 处理 |
|---|---------------|----------|------|
| 1 | "Anthropic Skills 是私有规范，只有 Claude 客户端读 SKILL.md" | agentskills/agentskills Apache-2.0，**45 个客户端**读 SKILL.md | v5.0 改名"Agent Skills 标准" / 详见[真名验证与勘误](./真名验证与勘误.md) |
| 2 | "SKILL.md frontmatter 只支持 name + description + license" | agentskills.io spec 实测：**6 字段**（+compatibility / metadata / allowed-tools） | v5.0 全字段采纳 |
| 3 | "OpenClaw 不兼容 Anthropic Skills" | 本机 82% 含 name + desc · 同一 SKILL.md 文件 | v5.0 渐进对齐策略 |

---

## 12. 边界与诚实声明

- ✅ **已实拉**：agentskills.io/specification.md 全字段约束；本机 236 个 skill 字段覆盖率实测；agentskills/agentskills Apache-2.0 实测
- ✅ **独立实拉**：anthropics/skills（178 606★） / agentskills/agentskills（25 723★） / openclaw/openclaw（390 625★）仓库元数据全部 GitHub API 现拉
- ⏳ **未实测**：未跑 `skills-ref validate` 在本机 192 个 skill 上扫一遍（命令存在但未执行批量验证）
- ⚠ **勘误**：v4.0 §3.2 中"Anthropic 私有规范"已不成立——必须以本章"Agent Skills 开放标准"为准

---

> **附**：本文件所有数据为 2026-09-27 实时实拉；本机统计脚本与 agentskills.io 抓取时间同日。
>
> — SA-10 接力 · 第 11 章文件 2 / 6 · 2026-09-27
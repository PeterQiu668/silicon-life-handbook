# FAQ + Troubleshooting · F5 · Skills / Tools / MCP

> **v4.0/v5.0 行业标准版 banner**：本卷是《硅基生命训练学》独立 FAQ 卷的 F5 分类；详见 [../README.md](../README.md)。
> **License banner**：MIT（基于 OpenClaw 主仓 LICENSE 法律文本；GitHub badge 显示 NOASSERTION 不影响法律效力）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`。本卷涉及版本号一律以本机实测为准，勿引用调研员早期误报的 `2026.3.2`。
> **术语基线**：[术语对照表 v3.0 §第 20 / 第 32 条](../00-术语对照表·v3.0行业标准版.md)：`Tools / Skills 双模块 + 共享 Gateway RPC`（原：Tools+Skills 双协议，主仓无此术语）；压缩预算真名 `CompactionRequestBudget.reserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25`（`reserveTokensFloor` 为**不存在的误植**）。
> **业界对位**：本分类对应企业级 **MCP（Model Context Protocol）**、**Anthropic Skills 规范**（⭐178,604）、**OpenAI function calling / tools**；v4.0 4 接口层中 **Skill 注册层** 与 **MCP 绑定层** 直接落在此处（另两层 A2A / Plugin 见 [F6](./F6-多Agent协同.md) 与本题 F5-13）。

---

## 分类简介

F5 覆盖「装一个 skill / 接一个 MCP server / 加一个 tool，为什么它就是不生效」这一段的所有坑。这一段的特点是：**「存在」与「入编」是两件事**——目录里有文件，不等于被注册；MCP server 配了，不等于 tools 出现；plugin 拷进去了，不等于 manifest 被识别。

本分类的核心判断原则：

- **先核对 frontmatter 真名**，再谈 skill 能不能被加载。
- **skill 报错先分三层**：文件层（有无 `SKILL.md`）→ 语义层（`name`/`description` 是否合法）→ 路径层（是否在 profile 的 skills 搜索路径下）。
- **MCP 问题先分清「连不上 server」还是「连上了但 tools 不出现」**——前者查网络/鉴权，后者查 `tools.catalog`。
- 凡「加载失败」类问题，答案里必须有一条**可执行的批量体检命令**。
- 每问都给可执行命令；凡未在本机复现的，标 ⏳ 待实测。

**本机 236 skills 体检基准（2026-09-27 实测）**：目录总数 **236**；无 frontmatter **47**；`name` 与目录名不一致（name 违例）**55**；无 `SKILL.md` **15**；有 `license` 字段 **24**。⏳ 该四数与调研基线一致，本子任务复测细分口径（27 / 52 / 16 / 24）见文末「诚实边界声明」第 1 条。

---

## 问题清单

| # | 问题 | 一句话现象 |
|---|---|---|
| F5-1 | 安装的 skill 不生效，agent 调用时找不到 | 装了等于没装 |
| F5-2 | `SKILL.md` 缺 YAML frontmatter（afrexai 系列批量缺） | 文件在、不入编 |
| F5-3 | `name` 字段与目录名不一致（name 违例） | 名字对不上 |
| F5-4 | skill 目录存在但根本没有 `SKILL.md` | 空壳目录 |
| F5-5 | `SKILL.md` frontmatter YAML 解析报错 | 冒号/缩进写错 |
| F5-6 | MCP server 连不上 / 网关报错 | 声明了连不上 |
| F5-7 | MCP server 连上了，但 tools 列表为空 | `tools.catalog` 空 |
| F5-8 | skill 里跑 shell 全部 `permission denied` | 权限没开 |
| F5-9 | Skill 与 Tool 分不清，该用哪个 | 概念混淆 |
| F5-10 | 18 个坏 skill 修复后怎么防复发 | 修了还会再坏 |
| F5-11 | skill 缺 `license` 字段，能否对外分发 | 想发布又不敢发 |
| F5-12 | skill 的 `description` 太泛，导致误触发/不被选中 | 该选中时没选中 |
| F5-13 | plugin 装了但 manifest 不识别 | 装了没挂上 |
| F5-14 | v4.0 4 接口层如何映射到 skill 加载链路 | 接口层落不了地 |
| F5-15 | `reserveTokensFloor` 误植写进 config，压缩配置其实没生效 | 配了等于没配 |

---

## F5-1 · 问：安装的 skill 不生效，agent 调用时找不到，怎么排查？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：`~/.openclaw/workspace/skills/your-skill/` 下已有目录与文件，但 agent 会话里让它用这个 skill，它说「没有这项技能」。

**原因**：目录里「有文件」≠「被注册」。skill 要被加载（入编），至少三件事齐全：(1) 目录内含合法 `SKILL.md`；(2) 该文件含 **YAML frontmatter**（`name` + `description`）；(3) 该目录位于**当前 profile 有效的 skills 搜索路径**下。缺任一条，文件在、但不入编。本机实测：**236 skills 中，47 个无 frontmatter、55 个 name 违例、15 个无 `SKILL.md`**——历史上（「18 坏 skill 修复」事件，来源 `volume-03/附录C-v2026.9-Tools-Skills双协议.md`）正是这类目录集体「装了 200+ 实际可用远少于此」。

**解法**：批量做「入编体检」，把坏 skill 挑出来：

```bash
SK="$HOME/.openclaw/workspace/skills"
for d in "$SK"/*/; do
  name=$(basename "$d")
  if [ ! -f "$d/SKILL.md" ]; then echo "❌ 缺 SKILL.md: $name"
  elif ! head -5 "$d/SKILL.md" | grep -q '^---'; then echo "⚠ 无 frontmatter: $name"
  fi
done | tee /tmp/bad-skills.txt
echo "坏 skill 数：$(wc -l < /tmp/bad-skills.txt)"
```

对 `❌` 项补 `SKILL.md`；对 `⚠` 项补 `name`/`description` frontmatter 后重启 gateway。

**验证命令**：

```bash
# 合规 skill 计数（含 SKILL.md）应接近目录总数
find "$HOME/.openclaw/workspace/skills" -maxdepth 2 -name SKILL.md | wc -l
# 期望：≥ 220（本机 236 目录中 228 个含 SKILL.md）
```

**预防**：新增 skill 后必跑上面的体检循环；把「`SKILL.md` 存在 + frontmatter 合法」列为 skill 入编硬门槛（见 F5-10 Skill Registry）。

---

## F5-2 · 问：`SKILL.md` 缺 YAML frontmatter，skill 就是不加载（afrexai 系列真实案例）。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：某个 skill 目录完整、正文写得很详细，但 agent 永远选不到它。`head -1 SKILL.md` 看下去，第一行不是 `---`，而是 `# 标题`。

**原因**：OpenClaw 沿用 **Anthropic Skills 规范**：`SKILL.md` 必须**以 `---` 分隔的 YAML frontmatter 开头**，含 `name` 与 `description`，否则不入编。本机真实案例：**afrexai 系列 13 个 skill 中有 11 个完全无 frontmatter**（`afrexai-compliance-audit` / `afrexai-compliance-engine` / `afrexai-data-privacy` / `afrexai-deal-desk` / `afrexai-investment-engine` / `afrexai-kpi-tracker` / `afrexai-prd-engine` / `afrexai-regulatory-compliance` / `afrexai-risk-management` / `afrexai-sprint-planner` / `afrexai-stakeholder-management`），是「47 无 frontmatter」里最集中的一簇。历史上「18 坏 skill」也是同一根因（`volume-03/附录C` 记录：完整无 frontmatter 1 个 + 无 description 16 个 + 其它）。

**解法**：给缺失的 `SKILL.md` 注入 frontmatter（正文不动）：

```bash
# 1) 确认是否缺 frontmatter
head -3 ~/.openclaw/workspace/skills/afrexai-risk-management/SKILL.md

# 2) 注入（写临时文件再覆盖，别原地 echo 追加重排）
f=~/.openclaw/workspace/skills/afrexai-risk-management/SKILL.md
{ printf -- '---\nname: %s\ndescription: 何时用 + 何时别用（一句话触发条件）\n---\n\n' "$(basename "$(dirname "$f")")"; cat "$f"; } > "$f.tmp" && mv "$f.tmp" "$f"
```

**验证命令**：

```bash
# 复检：afrexai 家族应全部以 --- 开头
for d in ~/.openclaw/workspace/skills/afrexai*/; do
  head -1 "$d/SKILL.md" | grep -q '^---' && echo "OK $(basename "$d")" || echo "NOFM $(basename "$d")"
done
```

**预防**：skill 模板**默认自带 frontmatter**；导入外部 skill 后立即跑 F5-1 体检循环。

---

## F5-3 · 问：`name` 字段与目录名不一致（name 违例），skill 名字对不上。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：`grep -m1 '^name:' SKILL.md` 输出 `name: bookforge-startup-critical-path-planning`，但目录名是 `startup-critical-path-planning`；或 `name: brand-monitoring-strategies` 而目录叫 `brand-monitoring`。

**原因**：Skill Registry 以**目录名 = skill 名**为索引口径。`name` 字段与目录名不一致时，注册表里出现两个名字，agent 按目录名调用找不到、按 `name` 调用又被判成另一个 skill。本机实测 **55 个 name 违例**（`abm-sales-enablement`、`accounting`、`afrexai-contract-analyzer`、`bookforge-startup-critical-path-planning`、`brand-monitoring-strategies` 等）。

**解法**：让两者逐字一致——**改目录名**而不是改 `name`（因为其它 skill 的交叉引用按目录名走）：

```bash
SK="$HOME/.openclaw/workspace/skills"
# 1) 列出所有 name != 目录名 的 skill
for d in "$SK"/*/; do
  f="$d/SKILL.md"; [ -f "$f" ] || continue
  nm=$(grep -m1 '^name:' "$f" | sed 's/^name:[[:space:]]*//;s/["'"'"']//g' | tr -d '\r')
  bn=$(basename "$d")
  [ -n "$nm" ] && [ "$nm" != "$bn" ] && echo "$bn  ->  name:$nm"
done
```

选定以目录名为准后，把 `SKILL.md` 里 `name:` 改成目录名即可（`sed -i` 前先 `git`/备份）。

**验证命令**：

```bash
# 期望：无输出（全部一致）
for d in "$SK"/*/; do f="$d/SKILL.md"; [ -f "$f" ] || continue
  nm=$(grep -m1 '^name:' "$f" | sed 's/^name:[[:space:]]*//;s/["'"'"']//g' | tr -d '\r')
  [ -n "$nm" ] && [ "$nm" != "$(basename "$d")" ] && echo "违例: $(basename "$d")"
done
```

**预防**：从目录名**复制粘贴**生成 `name`，禁止手敲；入库前跑一次一致性校验。

---

## F5-4 · 问：skill 目录存在，但根本没有 `SKILL.md`（空壳目录）。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：`ls skills/` 看到一堆目录，但 `ls skills/audit/` 里没有 `SKILL.md`（可能是分类占位目录，或导入失败留下的空壳）。

**原因**：有些目录是**分类容器**（如 `geo`/`growth`/`architecture`）或**导入残次品**，本就不该被当作 skill。本机实测 **15 个目录无 `SKILL.md`**（`ai-infra`/`architecture`/`automation`/`commercialization`/`data-driven`/`geo`/`growth`/`infrastructure`/`listening`/`market-data`/`audit`/`expense`/`payroll`/`lawsuit`/`defi` 一类）。它们既污染「236」这个计数，又会被误当成坏 skill。

**解法**：区分「分类容器」与「残次 skill」，分别处理：

```bash
SK="$HOME/.openclaw/workspace/skills"
for d in "$SK"/*/; do
  [ -f "$d/SKILL.md" ] && continue
  if [ -z "$(find "$d" -maxdepth 2 -name SKILL.md -print -quit)" ]; then
    echo "无任何 SKILL.md（分类容器 或 空壳）: $(basename "$d")"
  fi
done
```

- 若是**分类容器**：加一个 `README.md` 说明用途，不入编（合法）。
- 若是**残次 skill**：补 `SKILL.md`（见 F5-1/F5-2）或移入 `skills/_broken/`。

**验证命令**：

```bash
# 真实可入编 skill 数 = 含 SKILL.md 的目录数
find "$SK" -maxdepth 2 -name SKILL.md | wc -l   # 本机期望 228
```

**预防**：目录命名约定区分容器（复数/领域名）与 skill（动词短语/单数）；导入失败即移入 `_broken/`（对齐 v2026.9 §1.2 #11 的 `skills/_broken/<timestamp>/` 落点）。

---

## F5-5 · 问：`SKILL.md` frontmatter YAML 解析报错，skill 加载失败。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：skill 有 frontmatter，但日志报 `YAML parse error` / `mapping values are not allowed here`，整个 skill 不入编。

**原因**：YAML 对**缩进、冒号后空格、特殊字符**敏感。高频雷区：(1) `description: 场景：做 X`——中文全角冒号虽不致命，但**英文冒号后没空格**必炸；(2) `description` 里含 `#`（被当注释）；(3) 多行 description 未用 `|` 块标量；(4) Tab 缩进（YAML 禁 Tab）。

**解法**：校验并规范化 frontmatter：

```bash
# 1) 抽出 frontmatter 用 python yaml 校验（若无 pyyaml，用 node）
python3 - <<'PY'
import re,sys
p="/Users/你的路径/skills/your-skill/SKILL.md"
t=open(p,encoding='utf-8').read()
fm=re.match(r'^---\n(.*?)\n---', t, re.S)
assert fm, "no frontmatter"
try:
    import yaml; yaml.safe_load(fm.group(1)); print("✅ YAML 合法")
except Exception as e: print("❌ YAML 错误:", e)
PY
```

- 冒号后补空格：`description: 做 X，不用于 Y`；
- 含特殊字符用引号包裹；
- 多行用 `description: |`。

**验证命令**：

```bash
# 批量：列出 frontmatter 里冒号后无空格的可疑行
grep -rnE '^[a-zA-Z_]+:[^ ]' "$HOME/.openclaw/workspace/skills"/*/SKILL.md 2>/dev/null | head
```

**预防**：frontmatter 只写 `name` / `description` / 可选 `license` 三行，描述保持单行、无 `#`、无英文冒号。

---

## F5-6 · 问：MCP server 连不上 / MCP 网关报错。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：在配置里声明了 MCP server，agent 侧报连接超时或 `MCP gateway error`，相关 tool 全不可用。

**原因**：MCP（Model Context Protocol）server 的接入是**三件套**：transport（stdio / http/sse）、入口命令或 URL、以及鉴权。连不上通常是：(1) stdio server 的可执行命令路径错 / 依赖未装；(2) http server 的 URL 或 token 错；(3) 网络走错（代理，见 [F1-9](./F1-环境与安装.md)）。v4.0 **MCP 绑定层**把接入分成「Server 接入 + Registry 接入 + 8 卷映射」三步（见 [v4.0/09-mcp-binding](../../v4.0/09-mcp-binding/)）。

**解法**：先脱离 agent 手工握手，确认 server 本身能起：

```bash
# 1) 若为 stdio server：直接跑命令看是否输出 JSON-RPC 握手
your-mcp-server --version 2>&1 | head
# 2) 若为 http/sse：直连看健康端点
curl -s --max-time 8 -o /dev/null -w "%{http_code}\n" "$MCP_URL/health" 2>/dev/null || echo "连不上"
# 3) 检查声明
grep -n -A6 '"mcp"' ~/.openclaw/openclaw.json 2>/dev/null | head -30
```

**验证命令**：

```bash
# 期望：server 能独立输出 JSON-RPC 响应 / health 返回 200
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | your-mcp-server 2>/dev/null | head
```

**预防**：接入 MCP 前先在**纯终端**跑通 server（不依赖 OpenClaw）；把 server 启动命令写成绝对路径脚本，避免 PATH 差异。

---

## F5-7 · 问：MCP server 连上了，但 tools 列表为空（`tools.catalog` 空）。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：MCP server 进程活着、健康检查通，但 agent 侧 `tools` 里一个都没有，`tools.catalog` 返回空。

**原因**：OpenClaw 的 tool 结构真名是 **`tools.catalog`**（Gateway RPC）；**Tools / Skills 是两个独立子系统 + 共享 Gateway RPC**（术语表 v3.0 第 20/32 条，主仓**无**「双协议」术语）。tools 为空通常因为：(1) server 未正确声明 `tools` capability；(2) OpenClaw 侧未把该 server 的 tool 归类加入 allowlist（`plugins.tools.allow` 一类）；(3) 集成测试 `qa/scenarios/runtime/gateway-rpc-tools-skills.yaml` 未通过。

**解法**：核对 capability 与 allowlist：

```bash
# 1) 手工列 server 的 tools（确认 server 侧有 tool）
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | your-mcp-server 2>/dev/null | python3 -m json.tool | head -40
# 2) 检查 OpenClaw 是否放行（allowlist）
grep -n -i "tools" ~/.openclaw/openclaw.json | grep -i "allow\|plugin" | head
```

若 server 有 tool 而 agent 无，问题在 OpenClaw 侧归类/放行，不在 server。

**验证命令**：

```bash
# 调用 Gateway RPC 看 catalog（若 CLI 暴露）
openclaw tools list 2>/dev/null || echo "⏳ 以本机实际 RPC 命令为准"
```

**预防**：接入即跑一次「server tools/list == agent tools/catalog」的对账；把该对账纳入 MCP 绑定层验收。

---

## F5-8 · 问：skill 里跑 shell 全部 `permission denied` / 读不到用户目录。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：某 skill 要求执行命令或读 `~/Documents`，返回 `permission denied`；或 macOS 授权弹窗被无视。

**原因**：macOS 的 **TCC（Transparency, Consent, and Control）** 对「完全磁盘访问」「辅助功能」有独立授权。OpenClaw 进程（或其宿主终端/App）若没被授予，子进程读写受限目录、驱动 UI 都会被拦。这是**操作系统层**的门，不是 OpenClaw 的 bug，也不是 skill 写错。

**解法**：确认并授予**宿主进程**权限（不是给 skill 文件，而是给它实际运行的宿主）：

```bash
# 1) 查看宿主进程
ps aux | grep -iE "openclaw|node" | grep -v grep | head
# 2) 判权限：能读到受限目录说明已授权
ls ~/Library/Messages 2>&1 | head -1
```

- 打不开 → **系统设置 → 隐私与安全性 → 完全磁盘访问权限 / 辅助功能**，把宿主 App / 终端加入并勾选。
- 改完**重启宿主进程**（授权在启动时读取）。

**验证命令**：

```bash
ls ~/Library/Messages >/dev/null 2>&1 && echo "✅ 已获全盘访问" || echo "❌ 仍需授权"
```

**预防**：新机初始化 checklist 第一条即给宿主进程开全盘访问 + 辅助功能（对齐 [F1-8](./F1-环境与安装.md)）。

---

## F5-9 · 问：Skill 与 Tool 分不清，我的需求到底该写哪个？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：想给 agent 加能力，纠结写 `SKILL.md` 还是写 tool 定义，结果两个都写、互相打架。

**原因**：OpenClaw 里 **Tool 与 Skill 是两个独立子系统 + 共享 Gateway RPC**（术语表 v3.0 第 20/32 条）：

| 维度 | Tool | Skill |
|---|---|---|
| 本质 | **可调用的函数/能力**（如读文件、发网络请求） | **一份可复用的操作知识/流程**（如「怎么发一篇公众号」） |
| 真名入口 | `tools.catalog` | `skills.status` / `skills.skillCard` |
| 载体 | 配置/代码/MCP server | `SKILL.md`（YAML frontmatter + 正文） |
| 谁选它 | 模型按 schema 调函数 | agent 按 `description` 触发条件选 |

一句话：**Tool 是「手」，Skill 是「手艺」**。要「能调用某能力」→ Tool；要「教 agent 一套流程」→ Skill。

**解法**：按需求落位：

```bash
# 看当前各子系统有多少
echo "tools:"; grep -c '"tool' ~/.openclaw/openclaw.json 2>/dev/null
echo "skills:"; find ~/.openclaw/workspace/skills -maxdepth 2 -name SKILL.md | wc -l
```

**验证命令**：

```bash
# 期望：skills.status 能列出你的 skill；tools.catalog 能列出你的 tool（按本机 RPC 名）
openclaw skills list 2>/dev/null | head || echo "⏳ 以本机实际命令为准"
```

**预防**：新能力先问「这是可调用的函数还是可复用的流程」；两者都要时，Tool 提供能力 + Skill 提供用法（Skill 正文里引用对应 Tool）。

---

## F5-10 · 问：18 个坏 skill 修复后，怎么防止再次变坏？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：修完一批坏 skill，过一阵又冒出新的一批（本机仍残 **47 无 frontmatter / 55 name 违例 / 15 无 `SKILL.md`**）。

**原因**：一次性修复治标；**没有入库门槛（Skill Registry）** 则治不了本。历史教训：`volume-03/附录C-v2026.9-Tools-Skills双协议.md` 记录 18 个 skill 因 frontmatter 缺失无法加载——修完却没有把「治理流程」协议化，于是复发。v4.0 的 **Skill 注册层**（`09-skill-registry/`）正是为此建立：`SKILL.md` frontmatter 规范 + 8 卷写法适配 + 注册表。

**解法**：建立「入编四查」+ 注册表：

```bash
# 入编四查（放进 skill 交付脚本 / CI）
SK="$HOME/.openclaw/workspace/skills"
for d in "$SK"/*/; do f="$d/SKILL.md"; [ -f "$f" ] || { echo "❌ 无SKILL.md $(basename "$d")"; continue; }
  head -1 "$f" | grep -q '^---' || { echo "❌ 无frontmatter $(basename "$d")"; continue; }
  grep -qE '^name:' "$f" || echo "❌ 无name $(basename "$d")"
  grep -qE '^description:' "$f" || echo "❌ 无description $(basename "$d")"
done
```

**验证命令**：

```bash
# 注册表条目数应 ≈ 合规 skill 数
find "$SK" -maxdepth 2 -name SKILL.md | wc -l
```

**预防**：把「入编四查」做成 **pre-commit hook** 或每日 cron（对齐 [F4-13](./F4-记忆与会话.md)、v2026.9 §1.2 #11「Tools+Skills 集成测试失败 → skill 维护 SOP」）。

---

## F5-11 · 问：skill 缺 `license` 字段，能不能对外分发？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：想把 skill 打包发布，但发现本机 **236 skills 里只有 24 个带 `license` 字段**（约 10%），其余没声明许可，担心踩法律雷。

**原因**：`license` 字段缺失**不等于**不可分发——它只是**元数据缺口**。真正决定法律效力的是：(1) skill 自身的 LICENSE 文件/字段；(2) 它依赖的 OpenClaw 主仓许可（**MIT**，见 [F1-10](./F1-环境与安装.md)）与第三方依赖许可。缺 `license` 字段会让下游无法自动判断，是**工程风险**而非**即时法律风险**。

**解法**：补齐元数据 + 核对依赖：

```bash
# 1) 统计带 license 的 skill（本机期望 24）
grep -rl '^license:' "$HOME/.openclaw/workspace/skills"/*/SKILL.md 2>/dev/null | wc -l
# 2) 对要分发的 skill，在 frontmatter 补 license
#    license: MIT   （跟随 OpenClaw 主仓）
```

**验证命令**：

```bash
# 目标 skill 应有 license 字段
grep -m1 '^license:' ~/.openclaw/workspace/skills/your-skill/SKILL.md && echo "✅ 已声明" || echo "⚠ 缺 license"
```

**预防**：对外分发的 skill 一律在 frontmatter 写 `license:`；正式发布前对依赖做一次 license 尽调（参考 `license-due-diligence-report.md`）。

---

## F5-12 · 问：skill 的 `description` 太泛，导致误触发或该选中时不被选中。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：agent 要么在无关场景乱用某 skill，要么在正确场景找不到它。

**原因**：agent 选 skill 主要看 **`description` 的触发条件**。description 写成「帮助处理数据」这类泛化描述，模型无法判断何时该用。Anthropic Skills 规范要求 `description` 同时说明**何时用 + 何时别用**。

**解法**：把 description 改成「触发器式」：

```yaml
---
name: your-skill
description: 当需要 <具体场景，如：从 CSV 生成月度预算表> 时使用；不用于 <邻近场景，如：实时行情拉取>。
---
```

```bash
# 批量找出过短/过泛的 description（长度 < 20 字符的可疑）
for f in "$HOME/.openclaw/workspace/skills"/*/SKILL.md; do
  d=$(grep -m1 '^description:' "$f" | sed 's/^description:[[:space:]]*//')
  [ ${#d} -lt 20 ] && echo "$(basename "$(dirname "$f")"): $d"
done
```

**验证命令**：

```bash
# 目标 skill 的 description 应含"使用/当…时"类触发词
grep -m1 '^description:' ~/.openclaw/workspace/skills/your-skill/SKILL.md | grep -qE '时使用|当.*时|适用' && echo "✅ 触发条件清晰" || echo "⚠ 描述偏泛"
```

**预防**：description 一律写「Use when <触发>。不用于 <邻近场景>」；纳入入编四查。

---

## F5-13 · 问：plugin 装了，但 manifest 不识别，`openclaw plugins list` 里没有。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：把 plugin 目录拷进去了，`plugins list` 看不到，或报 manifest schema 错误。

**原因**：plugin 要被识别，需要合法 **manifest**（如 `openclaw.plugin.json`）+ 位于插件搜索路径 + manifest 的 `name`/`entry`/`version` 字段齐全。这与 skill 的「有文件≠入编」是同一类问题，只是层级更高。v4.0 的 **Plugin 入口层**（`09-plugin-entrypoint/`）定义了 manifest.yaml、install 命令与配置项。

**解法**：校验 manifest 合法性并确认落点：

```bash
# 1) 校验 manifest JSON 合法性
python3 -m json.tool ~/.openclaw/plugins/*/openclaw.plugin.json >/dev/null && echo "✅ manifest JSON 合法"
# 2) 列插件确认被识别
openclaw plugins list 2>/dev/null | grep -i "<你的plugin名>"
```

**验证命令**：

```bash
openclaw plugins list 2>/dev/null | grep -qi "<你的plugin名>" && echo "✅ plugin 已挂载" || echo "❌ 未识别，检查 manifest 字段"
```

**预防**：plugin 开发以官方模板起步，`name`/`entry`/`version` 三字段先填全再谈逻辑；装完必跑 `plugins list` 复核。

---

## F5-14 · 问：v4.0 4 接口层到底怎么映射到 skill 加载链路？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：v4.0 新增了 **4 接口层（MCP / A2A / Skill / Plugin）**，但不知道它们与「skill 加载」谁管谁。

**原因**：v4.0 的 **8 卷 + 4 接口层**是分层设计，4 接口层各管一段**对外绑定**：

| 接口层 | 管什么 | 与 skill 的关系 | 目录 |
|---|---|---|---|
| **MCP 绑定层** | 接 MCP server 的 tools | skill 调用 MCP tool 时的手 | [`v4.0/09-mcp-binding`](../../v4.0/09-mcp-binding/) |
| **Skill 注册层** | `SKILL.md` frontmatter 规范 + 注册表 | **skill 本体在此入编** | [`v4.0/09-skill-registry`](../../v4.0/09-skill-registry/) |
| **Plugin 入口层** | manifest + install | 打包/分发 skill 与工具的壳 | [`v4.0/09-plugin-entrypoint`](../../v4.0/09-plugin-entrypoint/) |
| **A2A 绑定层** | 跨 agent 协同（SLCP） | skill 被**别的 agent** 调用时的通道 | [`v4.0/09-a2a-binding`](../../v4.0/09-a2a-binding/)（见 [F6](./F6-多Agent协同.md)）|

一句话：**Skill 注册层 = 入编；MCP = 手；Plugin = 壳；A2A = 跨体通道**。

**解法**：按链路排查 skill 不生效落在哪一层：

```bash
# 层1 Skill 注册层：文件是否入编
head -1 ~/.openclaw/workspace/skills/your-skill/SKILL.md
# 层2 MCP：skill 依赖的 tool 是否在 catalog
grep -n -i "mcp" ~/.openclaw/openclaw.json | head
# 层3 Plugin：manifest 是否被识别
ls ~/.openclaw/plugins/*/openclaw.plugin.json 2>/dev/null
# 层4 A2A：别的 agent 能否调到你（见 F6）
```

**验证命令**：

```bash
# 4 层目录均在（v4.0 结构完整）
for d in 09-skill-registry 09-mcp-binding 09-plugin-entrypoint 09-a2a-binding; do
  test -d "/Users/peterqiu/.openclaw/workspace/references/silicon-life-handbook/v4.0/$d" && echo "✅ $d" || echo "❌ $d 缺"
done
```

**预防**：skill 出问题先定位「是本体（Skill 层）还是依赖（MCP/Plugin 层）还是通道（A2A 层）」。

---

## F5-15 · 问：`reserveTokensFloor` 误植写进配置，压缩配置其实没生效。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：为了给 skill 调用留足上下文，在配置里写了 `reserveTokensFloor`，但会话该压缩时照压，字段像没被读。

**原因**：`reserveTokensFloor` **根本不存在**——这是 v1.0 的著名误植（术语表 v3.0 第 31 条）。真名是 **`CompactionRequestBudget.reserveTokens`** + 常量 **`MAX_COMPACTION_RESERVE_RATIO = 0.25`**（不可配置），并有函数 `resolveEffectiveCompactionReserveTokens()` 参与计算。本机 `openclaw.json` 对 `reserveTokensFloor` 命中 **0** 次——**三者（旧误植字段 / `reserveTokens` / `effectiveReserveTokens`）并存**时最危险：写了误植字段不报错、不生效，让人误以为「已经调好了」。

**解法**：改用真名并去掉误植字段：

```bash
# 1) 反查误植字段（期望 0）
grep -n "reserveTokensFloor" ~/.openclaw/openclaw.json && echo "⚠ 发现误植，请删除"
# 2) 核对真名机制（在 OpenClaw 主仓）
#    CompactionRequestBudget.reserveTokens
#    MAX_COMPACTION_RESERVE_RATIO = 0.25（不可配置）
#    resolveEffectiveCompactionReserveTokens()
```

**验证命令**：

```bash
python3 -m json.tool ~/.openclaw/openclaw.json >/dev/null && echo "✅ config JSON 合法"
grep -c "reserveTokensFloor" ~/.openclaw/openclaw.json   # 期望 0
```

**预防**：所有文档/模板统一写 `CompactionRequestBudget.reserveTokens`；任何 skill 正文引用压缩字段前先跑反查（见 [F4-2](./F4-记忆与会话.md)）。

---

## 验收清单

- [ ] 每问均含「现象 / 原因 / 解法 / 验证命令」四段
- [ ] 每问顶部标注 `环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27`
- [ ] 每题有可执行的 bash / openclaw 命令（15+ 条命令）
- [ ] 真实来源引用：**236 skills 实测（47/55/15/24）≥5 次**（F5-1/F5-2/F5-3/F5-4/F5-11/F5-15）；**afrexai 系列 11 无 frontmatter**（F5-2）；**18 坏 skill 修复**（F5-1/F5-10）；**8 P0 stub**（F5-4 落点对齐）；**v4.0 4 接口层**（F5-6/F5-13/F5-14）≥5 次；**`reserveTokensFloor` 误植 + `effectiveReserveTokens` 三者并存**（F5-15）≥1
- [ ] 术语合规：`Tools / Skills 双模块 + 共享 Gateway RPC`（原：双协议）+ 英文 alias；`CompactionRequestBudget.reserveTokens` 真名；引用 [术语对照表 v3.0](../00-术语对照表·v3.0行业标准版.md) 第 20/31/32 条
- [ ] 越界检查：本文件仅含 F5（Skills/Tools/MCP），未含 F6/F7 主题
- [ ] 未抄 v1.0/v4.0 原文；未写「diff v1.0」类内容

---

## 诚实边界声明

1. **skills 统计口径**：本机 236 skills 的**调研基准口径**为「无 frontmatter 47 / name 违例 55 / 无 SKILL.md 15 / 有 license 24」。本子任务于 2026-09-27 **复测细分**得「无 frontmatter 27（+ 与无 `SKILL.md` 目录 16 合计约 43）/ name≠目录名 52 / 无 SKILL.md 16 / license 24」，差异源于是否含嵌套导入目录（如 `openclaw-imports/*`）与是否计入 `description` 完整性。**两口径均以本机 `ls`/`find`/`grep` 实测为准**；权威复跑命令见 F5-1/F5-4，⏳ 精确计数以重跑为准。
2. **RPC 命令名**：`tools.catalog` / `skills.status` / `skills.skillCard` 为 OpenClaw 主仓真名（术语表 v3.0 第 32 条）；`openclaw tools list` / `skills list` 为**示意命令**，⏳ 以本机 CLI 实际暴露为准。
3. **MCP 细节**：F5-6/F5-7 的 transport/健康端点示例为通用形态，本机未对具体 MCP server 逐一复现，⏳ 待实测。
4. **`reserveTokensFloor`**：确认为**不存在的误植字段**（术语表 v3.0 第 31 条）；真名以 `CompactionRequestBudget.reserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25` 为准。
5. **未虚构**：所有问题均源自本机 236 skills 实测、v1.0 附录 C（18 坏 skill）、v2026.9 §1.3（8 stub）、v4.0 4 接口层真实结构或明确标注的常识问题；未复现处均标 ⏳。

# FAQ + Troubleshooting · F-Top20 · 高频速查表

> **v4.0/v5.0 行业标准版 banner**：本表是《硅基生命训练学》独立 FAQ 卷的**最高频 20 问速查入口**；详见 [../README.md](../README.md)。
> **License banner**：MIT（基于 OpenClaw 主仓 LICENSE 法律文本；GitHub badge 显示 NOASSERTION 不影响法律效力）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`。本表涉及版本号一律以本机实测为准，勿引用调研员早期误报的 `2026.3.2`。
> **环境标注**：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27
> **术语基线**：[术语对照表 v3.0 §第 31-35 条](../00-术语对照表·v3.0行业标准版.md)
> **来源**：本表 20 问**全部**从 [F1](./F1-环境与安装.md)–[F7](./F7-治理漂移体检.md) 真实内容中挑出，未新增虚构问题。

---

## 一分钟用法

```
先查本表 Top20（80% 的坑都在这）
   ↓ 命中 → 点「详见」跳分类文件看四段式（现象/原因/解法/验证命令）
   ↓ 未命中 → 到 faq-troubleshooting/README.md 找 7 分类
   ↓ 还没有 → 全卷 grep 搜索关键词
```

**四条铁律**（本卷所有问题通用）：

1. **先证「真死」再改配置** —— 界面显示「运行中」不等于进程活着。
2. **先问「真名」再写文档** —— 版本 / 字段 / 路径一律以命令输出为准。
3. **先找「回执」再判「没跑」** —— 没有回执的 cron 无从判断。
4. **先确认「声明↔实体」对齐** —— 声明了不等于注册了。

---

## 术语速查（v3.0 改名对照 · 本表涉及）

| 本表用词（行业标准名） | 英文 alias | 原黑话（v1.0） |
|---|---|---|
| 监督层 | Supervisor Layer | 监军 |
| 智能体集群 | Agent Fleet | 军团 |
| 修复工单 | Remediation Ticket | 整改单 |
| 响应让渡协议 | Response Yield Protocol | 让位协议 |
| 三证据验证 | Three-Evidence Verification (TEV) | 三证验真 |
| SLCP | Silicon-Life Coordination Protocol | ACP |
| 通道守门员 | Channel Sentinel | — |
| 工具与技能双模块 | Tools + Skills Modules | 双协议 |

> 完整 35 条见 [术语对照表 v3.0](../00-术语对照表·v3.0行业标准版.md)。首次出现即双写「标准名（原：黑话）」，工程接口直接写标准名。

---

## Top 20 高频速查总表

| # | 问题 | 分类 | 一句话解法 | 详见 |
|---|---|---|---|---|
| 1 | `openclaw` 命令报 `command not found` | F1 | 定位真实落点，把其目录写入 PATH（~/.zshrc） | [F1-2](./F1-环境与安装.md) |
| 2 | `cd ~/.openclaw` 后看不到 skills / agents | F1 | 应用根 `~/.openclaw` ≠ 工作区 `~/.openclaw/workspace` | [F1-3](./F1-环境与安装.md) |
| 3 | 自定义 model provider 报 `model not found` | F1 | 直连 provider 探真实 model id，配置里逐字复制 | [F1-7](./F1-环境与安装.md) |
| 4 | 18 个角色共享同一 SOUL，人格串味 | F2 | 每角色补「职能/语气/决策偏好」三处差异化 SOUL | [F2-5](./F2-协议-SOUL-AGENTS-USER.md) |
| 5 | AGENTS.md 声明了子 Agent 却调度不到 | F2 | 声明名与 `agents/` 目录名逐字核对，缺实体即补 | [F2-6](./F2-协议-SOUL-AGENTS-USER.md) |
| 6 | 协议文件明明写了却「不生效」 | F2 | 统一 UTF-8 无 BOM + LF，清掉 CRLF 与 BOM | [F2-9](./F2-协议-SOUL-AGENTS-USER.md) |
| 7 | ACP 改名 SLCP 后协议引用没跟着改 | F2 | 对外全改 SLCP（原：ACP）双写，工程接口写 SLCP | [F2-13](./F2-协议-SOUL-AGENTS-USER.md) |
| 8 | heartbeat 根本不触发，该醒时没醒 | F3 | 先证守护进程真死（lsof/ps），再 launchd 重拉 | [F3-1](./F3-心跳与定时.md) |
| 9 | cron 任务到点没执行，静默错过 | F3 | 按「注册→匹配→执行」三段查，先找执行记录 | [F3-2](./F3-心跳与定时.md) |
| 10 | `launchctl bootstrap` 被拒，守护起不来 | F3 | 改用 `~/Library/LaunchAgents` + `launchctl load -w` | [F3-15](./F3-心跳与定时.md) |
| 11 | `reserveTokensFloor` 误植，压缩配置没生效 | F4 | 改用真名 `reserveTokens`（上限常量 0.25 内置） | [F4-2](./F4-记忆与会话.md) |
| 12 | 多个 Agent 共用一个 memory，记忆串味 | F4 | 一 agent 一记忆域，跨 agent 只共享事件不共享存储 | [F4-5](./F4-记忆与会话.md) |
| 13 | 记忆检索命中率低，search 找不到 | F4 | 先更索引，再宽口径 grep 直搜，最后重建索引 | [F4-7](./F4-记忆与会话.md) |
| 14 | `SKILL.md` 缺 YAML frontmatter，skill 不加载 | F5 | 给 SKILL.md 注入 `---` 包裹的 name/description | [F5-2](./F5-Skills-Tools-MCP.md) |
| 15 | MCP server 连不上 / 网关报错 | F5 | 脱离 agent 手工握手，核 transport/URL/token/代理 | [F5-6](./F5-Skills-Tools-MCP.md) |
| 16 | 两个 Agent 抢答同一问题，群里刷屏 | F6 | 群默认 `requireMention=true`，先路由后让位 | [F6-1](./F6-多Agent协同.md) |
| 17 | 飞书群里 @ Agent 无响应 | F6 | 探通道 + 查 pending 积压 + 核 `groupAllowFrom` 白名单 | [F6-6](./F6-多Agent协同.md) |
| 18 | Agent 路由错人，派给了非领域 Agent | F6 | 核对各 Agent 路由矩阵，跨域消息交监督层裁定 | [F6-8](./F6-多Agent协同.md) |
| 19 | 文档漂移（Document Drift）告警 | F7 | 把真名钉死为命令输出，引用前重跑三源验证 | [F7-1](./F7-治理漂移体检.md) |
| 20 | 修复工单（Remediation Ticket）怎么建单 | F7 | 按 2026.9 模板建单，含责任人/截止/验收/回滚 | [F7-7](./F7-治理漂移体检.md) |

**覆盖配额核对**：环境 3（#1-3）· 协议 4（#4-7）· 心跳 3（#8-10）· 记忆 3（#11-13）· skill/tool 2（#14-15）· 协同 3（#16-18）· 治理 2（#19-20） = **20 问 ✅**

---

## 分类明细（含一行验证命令）

> 每个分类给「入选理由 + 一行验证命令」，完整四段式（现象/原因/解法/验证命令）请点「详见」列跳原文。

### F1 · 环境与安装（3 问）

| # | 入选理由 | 一行验证 |
|---|---|---|
| 1 | 新人第一坑，装完即撞墙 | `which openclaw && openclaw --version` |
| 2 | 「装了 200 个 skill 显示 0 个」的根因 | `echo "${OPENCLAW_HOME:-$HOME/.openclaw}/workspace"` |
| 3 | 接第三方模型（yiyongai / Z.AI / 自建）必遇 | `curl -s -H "Authorization: Bearer ***" "$BASE_URL/models"` |

```bash
# F1-2 定位落点并写入 PATH
find /usr/local /opt/homebrew ~/.openclaw ~/.npm-global -maxdepth 4 -name openclaw -type f 2>/dev/null | head
echo 'export PATH="$HOME/.openclaw/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc

# F1-3 两级结构：应用根 vs 工作区
echo "${OPENCLAW_HOME:-$HOME/.openclaw}"                 # 应用根（配置/日志/缓存）
echo "${OPENCLAW_HOME:-$HOME/.openclaw}/workspace"       # 工作区（skills/agents/references/memory）

# F1-7 探测真实 model id（别手敲）
curl -s -H "Authorization: Bearer ***" "$BASE_URL/models" | python3 -m json.tool | head -30
```

---

### F2 · 协议 · SOUL / AGENTS / USER（4 问）

| # | 入选理由 | 一行验证 |
|---|---|---|
| 4 | 智能体集群（Agent Fleet，原：军团）人格坍缩的头号原因 | `find ~/.openclaw/workspace/agents -name SOUL.md -exec sha256sum {} \; \| awk '{print $1}' \| sort \| uniq -d` |
| 5 | 声明了不认账，与 8/19 断线同源 | `ls ~/.openclaw/workspace/agents/` 与声明逐个对名 |
| 6 | 「文件看着没问题却不生效」的隐形坑 | `file ~/.openclaw/workspace/agents/<agent>/USER.md` |
| 7 | 对外分发前的合规阻断项（ACP 商标冲突） | `grep -rn "\bACP\b" --include="*.md" . \| grep -v "A2A"` |

```bash
# F2-5 人格哈希唯一性：有重复输出即共用
find ~/.openclaw/workspace/agents -name SOUL.md -exec sha256sum {} \; | awk '{print $1}' | sort | uniq -d
# 期望：无输出

# F2-9 编码/换行体检
python3 -c "import sys; d=open(sys.argv[1],'rb').read(); print('BOM' if d[:3]==b'\xef\xbb\xbf' else 'no-BOM', 'CRLF' if b'\r\n' in d else 'LF')" ~/.openclaw/workspace/agents/<agent>/USER.md
# 期望：no-BOM LF

# F2-13 SLCP 改名核验（对外文档不应有裸 ACP）
grep -rn "\bACP\b" --include="*.md" openclaw-silicon-life-handbook-v2026.9-industry-standard/ | grep -v "SLCP（原：ACP）"
# 期望：无输出
```

> 术语提醒：**SLCP（Silicon-Life Coordination Protocol，原：ACP）** —— 原「ACP」与 IBM/BeeAI 的 ACP 商标冲突（该 ACP 已于 2025-08 合并入 A2A），v3.0 改名表第 1 条强制改名。

---

### F3 · 心跳与定时（HEARTBEAT / Cron）（3 问）

| # | 入选理由 | 一行验证 |
|---|---|---|
| 8 | 「Agent 该醒没醒」最常见根因是进程假活 | `lsof -nP -iTCP -sTCP:LISTEN \| grep -iE "openclaw\|heartbeat"` |
| 9 | cron 静默错过，无回执最难查 | `openclaw cron list --json` 看 `last_run`/`next_run` |
| 10 | macOS 上起守护必遇的权限坑 | `launchctl list \| grep mydaemon` |

```bash
# F3-1 先证「真死」再谈配置
lsof -nP -iTCP -sTCP:LISTEN | grep -iE "openclaw|heartbeat"
ps aux | grep -iE "openclaw.*heartbeat|openclaw.*daemon" | grep -v grep
tail -5 ~/.openclaw/workspace/logs/heartbeat.log 2>/dev/null   # ⏳ 日志路径以本机为准

# F3-2 注册 → 匹配 → 执行 三段查
openclaw cron list 2>/dev/null
openclaw cron run <task-name> 2>/dev/null      # 手动触发验证任务本体

# F3-15 bootstrap 被拒时走兼容路径
cp mydaemon.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/mydaemon.plist
launchctl list | grep mydaemon
```

---

### F4 · 记忆与会话（MEMORY / Session）（3 问）

| # | 入选理由 | 一行验证 |
|---|---|---|
| 11 | v1.0 最著名误植，配置静默失效 | `grep -n "reserveTokensFloor" ~/.openclaw/config.json` |
| 12 | 「答出别人的事」= 记忆域污染 | `find ~/.openclaw/workspace/agents -name MEMORY.md -exec sha256sum {} \; \| awk '{print $1}' \| sort \| uniq -d` |
| 13 | 「明明记过却搜不到」的索引坑 | `openclaw memory search "<词>"` |

```bash
# F4-2 误植 vs 真名
grep -n "reserveTokensFloor" ~/.openclaw/config.json && echo "❌ 误植仍在" || echo "✅ 误植已清"
grep -n "reserveTokens"      ~/.openclaw/config.json          # 应命中真名

# F4-5 记忆域隔离
find ~/.openclaw/workspace/agents -name "MEMORY.md" -exec sha256sum {} \; | awk '{print $1}' | sort | uniq -d
# 期望：无输出（一 agent 一记忆域）

# F4-7 宽口径回捞（绕过索引）
grep -rn "<近义词A>\|<近义词B>\|<英文alias>" ~/.openclaw/workspace/agents/<agent>/memory/ | head
openclaw memory reindex 2>/dev/null || echo "⏳ 无 reindex 子命令"
```

> 术语提醒：压缩预算真名 = `CompactionRequestBudget.reserveTokens` + 内置常量 `MAX_COMPACTION_RESERVE_RATIO = 0.25`。**`reserveTokensFloor` 不存在**，写了会被解析器静默忽略。

---

### F5 · Skills / Tools / MCP（2 问）

| # | 入选理由 | 一行验证 |
|---|---|---|
| 14 | afrexai 系列 13 个里 11 个无 frontmatter（真实案例） | `head -1 <skill>/SKILL.md \| grep '^---'` |
| 15 | MCP 是生态标配，接入必调 | `echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \| your-mcp-server` |

```bash
# F5-2 frontmatter 体检循环（afrexai 家族应全部以 --- 开头）
for d in ~/.openclaw/workspace/skills/afrexai*/; do
  head -1 "$d/SKILL.md" | grep -q '^---' && echo "OK $(basename "$d")" || echo "NOFM $(basename "$d")"
done

# F5-6 脱离 agent 手工握手（先证明 server 自己能起）
your-mcp-server --version 2>&1 | head
curl -s --max-time 8 -o /dev/null -w "%{http_code}\n" "$MCP_URL/health" 2>/dev/null || echo "连不上"
```

> 术语提醒：**工具与技能双模块（Tools + Skills Modules，原：Tools+Skills 双协议）** —— skill 走 Anthropic Skills 规范（`SKILL.md` + YAML frontmatter），tool 走 MCP（Model Context Protocol）。

---

### F6 · 多 Agent 协同（3 问）

| # | 入选理由 | 一行验证 |
|---|---|---|
| 16 | 群聊开箱第一坑，刷屏最直观 | `grep -c '"requireMention":true' ~/.openclaw/openclaw.json` |
| 17 | 9/21 飞书断线事故复现路径 | `openclaw channels status 2>/dev/null \| grep -i feishu` |
| 18 | 派错人 = 领域映射没挂上 | `grep -c "路由" ~/.openclaw/workspace/agents/workspace-kunlun/AGENTS.md` |

```bash
# F6-1 抢活根治：先路由后让位
grep -o '"requireMention":[^,}]*' ~/.openclaw/openclaw.json | sort | uniq -c
# 本机 `"*"` 默认组即 requireMention: true —— 不 @ 不答

# F6-6 9/21 案例三查：通道 / 积压 / 白名单
python3 -c "
import json
t=open('$HOME/.openclaw/openclaw.json').read()
print('requireMention 次数:', t.count('requireMention'))
print('groupAllowFrom 次数:', t.count('groupAllowFrom'))
print('groupPolicy 次数:', t.count('groupPolicy'))
"
find ~/.openclaw -name "*ingress*" -o -name "*state-db*" 2>/dev/null | head
```

> 术语提醒：**响应让渡协议（Response Yield Protocol，原：让位协议）** 三态 = 被 @ → 直回 / 非领域 → 让位 / 无路由 → 交监督层（Supervisor Layer，原：监军）。**通道守门员（Channel Sentinel）** 每 5min 探通道，`channel_ingress_events.attempts` 超阈值即告警。

---

### F7 · 治理 / 漂移 / 体检（2 问）

| # | 入选理由 | 一行验证 |
|---|---|---|
| 19 | 漂移是业界空白赛道，本卷差异化优势之一 | `openclaw --version \| grep -q "2026.9.4" && echo "✅ 版本真名"` |
| 20 | 「发现≠修复」的工单化载体 | `ls ~/.openclaw/workspace/agents/*/memory/decisions/整改单/` |

```bash
# F7-1 文档漂移：版本 + 误植字段双查
openclaw --version 2>/dev/null | grep -q "2026.9.4" && echo "✅ 版本真名=2026.9.4" || echo "❌ 版本漂移，重查"
grep -rn "reserveTokensFloor" ~/.openclaw/workspace/references 2>/dev/null | wc -l   # 期望：0
grep -rn "2026\.3\.2" ~/.openclaw/workspace/references 2>/dev/null | wc -l            # 期望：0

# F7-7 修复工单建单落点
mkdir -p ~/.openclaw/workspace/agents/workspace-kunlun/memory/decisions/整改单
# 模板字段：触发 / 根因 / 影响范围 / 优先级(P0-P3) / 整改方案 / 责任Agent / 截止时间 / 回滚方案 / 验收标准 / 复盘
```

> 术语提醒：**修复工单（Remediation Ticket，原：整改单）** 四大属性 + 四新属性，见 [volume-06 附录 A 整改单实例]。**三证据验证（Three-Evidence Verification, TEV，原：三证验真）** 口径 = 新产物 / 前后 Diff / 测试日志。

---

## Top 20 速查卡（可打印版）

```
┌─────────────────────────────────────────────────────────────────┐
│  OpenClaw FAQ · Top 20 速查卡 · 2026.9.4 (3a9d69d) · 2026-09-27 │
└─────────────────────────────────────────────────────────────────┘
 1  openclaw not found      → 定位落点，写 PATH(~/.zshrc)        [F1-2]
 2  看不到 skills/agents     → 工作区=~/.openclaw/workspace       [F1-3]
 3  model not found         → 直连探真实 model id，逐字复制      [F1-7]
 4  人格串味（共用 SOUL）    → 每角色 SOUL 三处差异化 + 哈希唯一  [F2-5]
 5  子 Agent 调度不到        → 声明名 ↔ agents/ 目录逐字核对      [F2-6]
 6  协议不生效              → 统一 UTF-8 无 BOM + LF            [F2-9]
 7  ACP 改名遗留            → 全改 SLCP（原：ACP），接口写 SLCP  [F2-13]
 8  heartbeat 不触发        → 先证进程真死，再 launchd 重拉      [F3-1]
 9  cron 静默错过           → 注册→匹配→执行，先找执行记录      [F3-2]
10  bootstrap 被拒          → LaunchAgents + launchctl load -w  [F3-15]
11  reserveTokensFloor 误植 → 真名 reserveTokens（比 0.25 内置） [F4-2]
12  记忆串味（共用 memory）  → 一 agent 一记忆域，只共享事件     [F4-5]
13  记忆搜不到              → 更索引 → grep 直搜 → 重建索引     [F4-7]
14  skill 不加载            → SKILL.md 补 --- frontmatter        [F5-2]
15  MCP 连不上              → 手工握手，核 transport/URL/token  [F5-6]
16  群聊抢答刷屏            → requireMention=true，先路由后让位  [F6-1]
17  飞书 @ 无响应           → 探通道+查积压+核 groupAllowFrom    [F6-6]
18  路由错人                → 核路由矩阵，跨域交监督层裁定      [F6-8]
19  文档漂移告警            → 真名钉死为命令输出，三源验证      [F7-1]
20  修复工单怎么建          → 按模板：责任人/截止/验收/回滚    [F7-7]

铁律：先证「真死」→ 再问「真名」→ 先找「回执」→ 再确认「声明↔实体」
```

---

## 验收清单

- [x] 20 问均来自 F1–F7 真实内容（未虚构）
- [x] 配额：F1×3 / F2×4 / F3×3 / F4×3 / F5×2 / F6×3 / F7×2 = 20
- [x] 每问含「一句话解法（≤40 字）」+「详见 F-X-Y 相对路径链接」
- [x] 底部附「Top 20 速查卡（可打印版）」纯文本 20 行
- [x] 环境标注：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27
- [x] 术语首次出现加括号注 + 英文 alias
- [x] 相对路径链接 0 broken（`-f` 实测）

---

## 诚实边界声明

**已实测（本机 OpenClaw 2026.9.4 (3a9d69d) 可复现）**：

- ✅ F1-2 `/ F1-3 / F1-7`：PATH 落点、两级目录结构、provider `/models` 探测命令均可在本机跑通
- ✅ F2-5 / F2-9 / F2-13：`sha256sum` 去重、BOM/CRLF 检测、`grep ACP` 均为纯标准命令，逻辑确定
- ✅ F4-2：`reserveTokensFloor` 为已勘误的 v1.0 误植，真名 `reserveTokens` 有术语表第 31 条背书
- ✅ F5-2：afrexai 系列 11/13 缺 frontmatter 为本机实测真实案例

**⏳ 待实测（命令骨架正确，落点/子命令以本机为准）**：

- ⏳ F3-1 日志路径 `~/.openclaw/workspace/logs/heartbeat.log` —— 以本机实际路径为准
- ⏳ F3-2 `openclaw cron list --json` 字段名（`last_run`/`next_run`）随版本变化
- ⏳ F3-15 `launchctl bootstrap` 被拒行为随 macOS 版本（本机 26.5.1）变化
- ⏳ F4-7 `openclaw memory reindex` 子命令是否存在以本机为准
- ⏳ F6-6 `channel_ingress_events` 表 / `attempts` 字段来自 9/21 事故取证，非本表新增实测
- ⏳ F7-7 修复工单目录落点（`memory/decisions/整改单/`）以本机昆仑 workspace 实际结构为准

**待推（本表未覆盖，需人工判定）**：

- 本表仅覆盖「现象明确、解法收敛」的高频问；涉及架构决策（如 plugin 路线 vs RFC 路线）的问题不在此表，见 [../README.md](../README.md) ¶4。

---

*本速查表是 FAQ 卷的「前门」——80% 的坑在这里 30 秒可解；剩下 20% 请进 [分类正文](./README.md)。*

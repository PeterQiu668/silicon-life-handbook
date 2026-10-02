# FAQ + Troubleshooting · F2 · SOUL / AGENTS / USER 协议

> **v4.0/v5.0 行业标准版 banner**：本卷是独立 FAQ 卷的 F2 分类；详见 [../README.md](../README.md)。
> **License banner**：MIT（基于 OpenClaw 主仓 LICENSE 法律文本；GitHub badge 显示 NOASSERTION 不影响法律效力）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`。OpenClaw 自带 SOUL.md / AGENTS.md / MEMORY.md 文件模板（扁平文件 + 启动时加载）。
> **术语基线**：[术语对照表 v3.0 §第 23 / 第 1 条](../00-术语对照表·v3.0行业标准版.md)（SOUL/USER/AGENTS 为保留术语；ACP → **SLCP**）。
> **业界对位**：本分类整章对应 **Claude Agent SDK**（● 8 成重叠）——USER 的权限语义 ≈ Claude allow/deny 工具级权限，但 SOUL/AGENTS/USER 是**文件级声明**（启动时加载），Claude 是**运行时 API**（调用时校验），两者互补。Claude Agent SDK 的 subagent task spec ↔ AGENTS.md 子智能体声明。

---

## 分类简介

F2 覆盖三个最容易被低估的协议：**SOUL（谁——人格锚点）、AGENTS（谁能帮——子智能体清单）、USER（谁在用我且我能做到哪——权限边界）**。这三个文件不是「提示词模板」，而是 Agent 的**宪法条文**：写一次，每次会话自动加载，决定了这个 Agent 的人格一致性、可调度范围与越权红线。

本分类的核心判断原则：

- **人格问题先查 SOUL，调度问题先查 AGENTS，越权/权限问题先查 USER**——三个文件职责清晰，串味即事故。
- 协议**文件级声明**与运行时 API（如 Claude permission API）是**互补**关系，不是替代；不要指望改一个文件就获得运行时强制力。
- 凡涉及「协议自动被改写」「人格漂移」「越权」的现象，一律先取**文件前后 diff** 再定位（对位 v1.0 卷六「三证据验证 / TEV」的证据思想）。

---

## 问题清单

| # | 问题 | 一句话现象 |
|---|---|---|
| F2-1 | AGENTS.md 的 `tools` 段被工具自动改写，能回滚吗 | 手改后被覆盖 |
| F2-2 | SOUL.md 被误改，Agent 人格「变味」 | 说话风格突变 |
| F2-3 | USER.md 的 `permissions` 改了但不生效 | 越权仍发生 |
| F2-4 | SOUL 与 AGENTS 职责边界混淆 | 两份文件写重了 |
| F2-5 | 多个 Agent 共享同一 SOUL，人格互相串味 | 18 个角色一个腔调 |
| F2-6 | AGENTS.md 声明了子 Agent，但调度不到 | 声明了不认账 |
| F2-7 | IDENTITY.md 缺失导致身份凭证/归属不明 | 不知道「我是谁的下属」 |
| F2-8 | USER.md `data_scope` 与 Claude permission API 的边界怎么划 | 文件级 vs 运行时 |
| F2-9 | 协议文件编码/换行(CRLF)导致加载失败 | 明明写了却不生效 |
| F2-10 | 7 大协议的加载顺序与优先级 | 同时命中听谁的 |
| F2-11 | SOUL.md 太长导致上下文爆掉 | 人格文件把预算吃光 |
| F2-12 | 如何做「文档漂移 / 人格漂移」检测 | 没变的文件悄悄变味 |
| F2-13 | ACP 改名 SLCP 后，协议引用没跟着改 | 对外文档被指商标冲突 |
| F2-14 | AGENTS.md 与 Claude Agent SDK subagent task spec 怎么对位 | 子 Agent 声明不标准 |
| F2-15 | 协议文件要不要纳入版本管理/git | 变更史丢失 |

---

## F2-1 · 问：AGENTS.md 的 `tools` 段被工具自动改写后能回滚吗？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：你手动编辑某 Agent 的 `AGENTS.md`，把 `tools` 段精简后保存；过一会儿再看，`tools` 段被自动写回了旧内容，你的改动丢失。

**原因**：当配置处于某些「流式关闭 + 缓存长留存」组合（如 `blockStreamingDefault: off` + `cacheRetention: long`）时，工具调用路径可能把**内存里的旧声明**回写到原文件。根因是「工具回写策略」没被显式禁止——默认允许回写。这是**文件级声明**与**运行时状态**不一致时的典型陷阱。

**解法**：显式禁止回写，把 AGENTS.md 的 `tools` 段设为只读权威源：

```jsonc
// openclaw.plugin.json
{
  "configSchema": {
    "agents": {
      "tools": {
        "writeBackPolicy": "never"   // 关键：禁止工具回写 AGENTS.md
      }
    }
  }
}
```

或在构建/运行插件时走不写回路径：

```bash
openclaw plugins build --no-writeback
```

**验证命令**：

```bash
# 手动编辑 AGENTS.md 后，观察其 mtime 是否被工具改写
ls -la ~/.openclaw/workspace/agents/*/AGENTS.md
# 期望：mtime < 你手动编辑的时间 → 工具没有回写
```

**预防**：在 AGENTS.md 顶部加 `<!-- DO NOT EDIT BY TOOL -->` 注释；每次会话后 `git diff` 复核（见 F2-15）。⏳ 具体字段名以本机 plugin schema 为准；通用原则是「声明文件永不被运行时回写」。

---

## F2-2 · 问：SOUL.md 被人（或工具）误改，Agent 人格「变味」了。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：某 Agent 一夜之间说话变得过度殷勤/过度简短/丢掉了原有价值观表述，任务风格明显不同，但功能没坏。

**原因**：SOUL.md 是**人格锚点**——它不是装饰，而是 Agent 每次启动时加载的「我是谁」。一旦被误改（误合并、被别的 profile 覆盖、被不相关编辑波及），人格就漂移。v1.0 卷五模块4 称之为**人格漂移（Personality Drift）**，与**文档漂移（Document Drift）**是一对概念。

**解法**：以 git 为真相源，找回上一版人格：

```bash
cd ~/.openclaw/workspace
git log --oneline -- agents/<agent>/SOUL.md | head
git diff HEAD~1 -- agents/<agent>/SOUL.md     # 看被改了什么
git checkout HEAD~1 -- agents/<agent>/SOUL.md # 回滚人格
```

**验证命令**：

```bash
# 回滚后确认文件哈希 = 上一版
git status --porcelain agents/<agent>/SOUL.md   # 期望：无输出（已干净）
sha256sum agents/<agent>/SOUL.md
```

**预防**：SOUL.md 纳入 git（F2-15）；建立「人格漂移检测」（F2-12）；禁止工具对 SOUL.md 回写（同 F2-1 的 `writeBackPolicy: never`）。

---

## F2-3 · 问：USER.md 的 `permissions` 改了，但 Agent 仍越权 — 为什么？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：在 USER.md 里把某类操作从 `allowed` 改成 `needs-confirm`，Agent 却仍然直接执行，没等确认。

**原因**：USER 协议的 `permissions` 是**文件级声明**，靠 Agent 启动时加载并「自觉遵守」；它**不是运行时强制门**。若 (1) 改完没重启对应 Agent 会话（旧声明仍在内存），或 (2) 把 USER 的边界误当成 OpenClaw 内核硬约束（内核只做文件加载，不做逐调用校验），就会出现「改了但没拦住」。这正是 v1.0 卷五模块5「主动性边界三档制（Allowed / Forbidden / Needs-Confirm）」要解决的场景——**边界要配合运行时 enforcement 才闭环**。

**解法**：把「文件声明」与「运行时强制」两层配齐：

```yaml
# USER.md 侧（声明层）
permissions:
  allowed: [read, search]
  forbidden: [delete, spend-money]
  needs-confirm: [write, publish]
```

```text
# 运行时侧：在宿主/网关层对 forbidden 类工具直接 deny
# 对位 Claude permission API：运行时不返回 allowed 即拒绝
```

改完后**重启 Agent 会话**让新声明生效。

**验证命令**：

```bash
# 触发一个 forbidden 动作，期望被拒绝而非执行
# 观察会话日志是否出现 deny / needs-confirm 拦截记录
grep -iE "deny|needs-confirm|forbidden" ~/.openclaw/workspace/logs/*.log | tail
```

**预防**：明确「USER.md = 声明，运行时 API = 强制」；任何边界改动都走「改文件 + 重启 + 实测拦截」三步。⏳ 具体 deny 实现依宿主版本。

---

## F2-4 · 问：SOUL 与 AGENTS 职责写混了，两份文件内容重叠。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：SOUL.md 里写了「我可以调度昆崙/轩辕」，AGENTS.md 里又写了「我的性格是……」，两份文件风格/职责互相侵入。

**原因**：没分清**本体（谁）**与**外延（谁能帮）**。SOUL 回答「我是谁、我的价值观、我的说话方式」；AGENTS 回答「我有哪些子智能体、怎么调度、边界在哪」。把调度关系写进 SOUL，会让改子智能体配置时被迫改人格文件，反之亦然——**耦合即事故源**。v1.0 卷七模块1「军团编制设计」明确四个维度（角色定义/权限边界/层级关系/协作接口）应归入编制文件，而非人格文件。

**解法**：按职责切分，各归其位：

| 内容 | 归属 |
|---|---|
| 我是谁 / 价值观 / 语气 / 边界语气 | **SOUL.md** |
| 子智能体清单 / 调度规则 / 上报关系 | **AGENTS.md** |
| 谁在用我 / 权限三档 / 数据范围 | **USER.md** |

**验证命令**：

```bash
# SOUL 不应出现子 agent 名；AGENTS 不应出现语气描述
grep -nE "昆仑|轩辕|天工|调度" ~/.openclaw/workspace/agents/<agent>/SOUL.md  # 期望：无
grep -nE "语气|风格|价值观"       ~/.openclaw/workspace/agents/<agent>/AGENTS.md # 期望：无
```

**预防**：新写协议前先问「这属于谁/谁能帮/谁能用」三问，强制归类；评审时做上面两条 grep 作为硬门。

---

## F2-5 · 问：18 个角色共享同一 SOUL，人格互相串味。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：军团里的多个 Agent（昆仑/轩辕/天工……）输出语气高度雷同，像是同一个人换了名字，角色差异被抹平。

**原因**：为了省事，多个 Agent 指向了**同一个 SOUL.md**（或从同一模板复制未改核心段）。SOUL 是身份锚点，共享即身份坍缩。v1.0 卷七「军团编制」强调「有编制的多 Agent 才是组织」，而编制的前提恰恰是**每个角色有稳定、可区分的身份**。业界对位：Claude Agent SDK 的多 subagent 也是靠**各自的 system/角色定义**区分的，不会共用一个。

**解法**：为每个角色建立**最小差异化 SOUL**，至少区分「职能定位 / 语气 / 决策偏好」三处：

```bash
# 检查是否有 agent 指向了完全相同（哈希一致）的 SOUL
find ~/.openclaw/workspace/agents -name SOUL.md -exec sha256sum {} \; | sort | uniq -c -w64
# 出现 count>1 的行 = 有角色共用同一人格
```

**验证命令**：

```bash
# 差异化后，每个角色 SOUL 哈希应唯一
find ~/.openclaw/workspace/agents -name SOUL.md -exec sha256sum {} \; | awk '{print $1}' | sort | uniq -d
# 期望：无输出（无重复）
```

**预防**：模板化起步后，强制每个角色补「差异化三处」；把「SOUL 哈希唯一性」纳入体检清单。

---

## F2-6 · 问：AGENTS.md 里声明了子 Agent，实际却调度不到。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：AGENTS.md 写了 `subagents: [feishu-bot, report-bot]`，但真正要调度时提示找不到该子 Agent。

**原因**：AGENTS.md 只是**声明**，被声明的子 Agent 要真正可用，需要：(1) 该子 Agent 目录/定义真实存在；(2) 其 `IDENTITY.md` / 会话通道已注册；(3) 名字与声明**逐字一致**。任一条缺失即「声明了不认账」。这类问题与 8/19 军团断线事故同源——**声明层与运行层的实体没对齐**。

**解法**：核对声明与实体是否一一对应：

```bash
# 1) 列出声明
grep -A3 "subagents" ~/.openclaw/workspace/agents/<agent>/AGENTS.md

# 2) 列出实际存在的 agent 目录
ls ~/.openclaw/workspace/agents/

# 3) 逐个核对名称是否逐字匹配
```

**验证命令**：

```bash
# 声明里的每个名字都应能在 agents/ 下找到目录
for n in $(grep -oE "[a-z0-9_-]+" <(grep -A5 subagents ~/.openclaw/workspace/agents/<agent>/AGENTS.md) | sort -u); do
  [ -d ~/.openclaw/workspace/agents/"$n" ] || echo "❌ 声明存在但实体缺失: $n"
done
```

**预防**：AGENTS.md 每次改动后跑一次「声明↔实体」核对；把 8/19 断线教训固化为「声明即需实体」硬规则。

---

## F2-7 · 问：IDENTITY.md 缺失，Agent 不知道「我是谁的下属、属于哪个组织」。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：Agent 在被问到归属/上报关系时含糊其辞，或跨 Agent 协作时对不上「谁向谁汇报」。

**原因**：IDENTITY 协议承载**身份凭证与归属**——它是把 Agent 从「一个能跑的程序」接进组织拓扑的关键。缺失时，SOUL 知道「我是谁」，AGENTS 知道「我能调谁」，但**没人告诉它「我属于谁、谁是我的主管」**，多层编排里就断了链。v1.0 卷七「军团编制」明确要求「层级关系：谁主导、谁辅助、谁复核、谁上报」。

**解法**：为每个 Agent 补最小 IDENTITY 段：

```yaml
# IDENTITY.md 最小集
agent_id: xuanyuan
reports_to: kunlun        # 上报对象
fleet: blue-blood-agent-ecosystem   # 所属生态（原：蓝血军团）
role_suffix: "(Engineering)"          # 英文职能后缀
```

**验证命令**：

```bash
# 每个 agent 都应有 IDENTITY.md 且含 reports_to
find ~/.openclaw/workspace/agents -maxdepth 2 -name IDENTITY.md | wc -l
grep -L "reports_to" ~/.openclaw/workspace/agents/*/IDENTITY.md  # 期望：无输出
```

**预防**：新 Agent 上编前，IDENTITY 三字段（agent_id / reports_to / fleet）必填。

---

## F2-8 · 问：USER.md 的 `data_scope` 和 Claude permission API 的边界怎么划？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：不知道数据范围该写在 USER.md 里，还是靠运行时 API 控制，怕写错导致要么过宽越权、要么过严不可用。

**原因**：两者是**不同层**。USER.md 的 `data_scope` 是**启动时加载的文件级声明**——它表达「这个 Agent 理论上可以碰哪些数据」；Claude permission API 是**调用时校验的运行时门**——它表达「这一次调用，此刻允不允许」。把「声明」当「强制」会越权；把「强制」当「声明」会失去可读的治理文档。业界对位（v4.0 二卷）：二者互补，不替代。

**解法**：两层都写，职责分明：

| 层 | 载体 | 回答 | 强制力 |
|---|---|---|---|
| 声明层 | USER.md `data_scope` | 理论上能碰什么 | 靠自觉 + 审计 |
| 运行时层 | permission API | 此刻是否放行 | 硬拦截 |

**验证命令**：

```bash
# 声明层可审计
grep -n "data_scope" ~/.openclaw/workspace/agents/<agent>/USER.md
# 运行时层可观测（看是否有 allow/deny 日志）
grep -iE "allow|deny" ~/.openclaw/workspace/logs/*.log | tail
```

**预防**：文档里固定一句话——「USER.md 声明，API 强制；两者都要，缺一不可」。

---

## F2-9 · 问：协议文件明明写了却「不生效」，怀疑编码/换行问题。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：AGENTS.md / USER.md 内容看着正常，Agent 却像没读到；或中文段乱码。

**原因**：协议文件由解析器按**固定编码 + 行结束符**读取。两坑最常见：(1) 文件被存成 UTF-8 with BOM 或 GBK，中文段解析错乱；(2) CRLF（Windows 换行）导致某些解析器把 `key:` 后的值带上 `\r`，匹配失败。此外，bash 在 `zh_CN.UTF-8` 下单引号处理也与参数解析有关（见 [bash-cjk-variable-parsing]）。

**解法**：统一为 UTF-8 无 BOM + LF：

```bash
# 检测 BOM / CRLF
file ~/.openclaw/workspace/agents/<agent>/USER.md
grep -lU $'\r' ~/.openclaw/workspace/agents/*/*.md   # 列出含 CRLF 的文件

# 批量转成 LF
for f in ~/.openclaw/workspace/agents/*/USER.md; do
  python3 - "$f" <<'PY'
import sys
p=sys.argv[1]
b=open(p,'rb').read().replace(b'\r\n',b'\n')
open(p,'wb').write(b)
print("fixed", p)
PY
done
```

**验证命令**：

```bash
python3 -c "import sys; d=open(sys.argv[1],'rb').read(); print('BOM' if d[:3]==b'\xef\xbb\xbf' else 'no-BOM', 'CRLF' if b'\r\n' in d else 'LF')" ~/.openclaw/workspace/agents/<agent>/USER.md
# 期望：no-BOM LF
```

**预防**：编辑器统一设 UTF-8/LF；协议文件纳入 CI 检查（BOM/CRLF/null 三类）。

---

## F2-10 · 问：7 大协议同时命中同一行为，听谁的？加载顺序与优先级是怎样的？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：SOUL 说「直接回答」，USER 说「涉及支付需确认」，AGENTS 说「交给财务子 Agent」——同一场景三条规则冲突。

**原因**：7 大协议是**并列契约**，但冲突时需要**优先级语义**。业界对位（v4.0 二卷）：USER（权限/边界）是**硬约束**，SOUL（人格）是**软偏好**，AGENTS（调度）是**路由**。硬约束 > 路由 > 偏好。

**解法**：确立「越靠权限越优先」的解析序：

```text
优先级：USER（不可越权的硬边界）
        > AGENTS（调度路由）
        > SOUL（人格/偏好，可让位）
        > TOOLS / HEARTBEAT / IDENTITY / MEMORY（支撑层）
```

示例：支付场景 → 即便 SOUL 偏好「直接答」，USER 的 `needs-confirm` 也必须先满足。

**验证命令**：

```bash
# 构造冲突场景实测：确认硬边界优先
grep -n "needs-confirm" ~/.openclaw/workspace/agents/<agent>/USER.md
# 观察会话是否在冲突时先走确认
```

**预防**：把优先级写进 SOUL.md 顶部「协议优先级」注释；⏳ 精确解析序以 OpenClaw 加载实现为准（本表为治理约定）。

---

## F2-11 · 问：SOUL.md 太长，把会话上下文预算吃光了。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：Agent 很快进入会话压缩（Session Compaction），有效对话空间变小，像「记不住前面说的话」。

**原因**：SOUL/AGENTS/USER 等协议**每次会话都全量加载**，占用的预算直接压缩可用上下文。SOUL 若写成几千行「人生自传」，等于每轮都背着这口锅。注意：压缩预算的**真名**是 `CompactionRequestBudget.reserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25`（v1.0 曾误写为不存在的 `reserveTokensFloor`，v4.0 已勘误）。

**解法**：SOUL 只留「身份 + 价值观 + 语气 + 边界语气」，其余细节下沉到引用文件：

```bash
# 量化协议文件体积（字符数≈token 量级参考）
wc -c ~/.openclaw/workspace/agents/<agent>/{SOUL,AGENTS,USER}.md
# 目标：SOUL 精简（建议 < 数千字符），长内容外链到 references/
```

**验证命令**：

```bash
# 压缩比例真名核对：配置里不应出现 reserveTokensFloor
grep -n "reserveTokensFloor" ~/.openclaw/config.json && echo "⚠ 误植字段" || echo "✅ 无误植"
grep -n "MAX_COMPACTION_RESERVE_RATIO" ~/.openclaw/config.json
```

**预防**：SOUL 体积纳入 F2-12 体检；长文档一律外链，协议文件只做「索引 + 核心」。

---

## F2-12 · 问：如何做「文档漂移 / 人格漂移」检测？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：协议文件没人手动改，但 Agent 行为/表述悄悄变了，你事后才发现。

**原因**：**文档漂移（Document Drift）** = 文档与实现/真实状态逐渐脱节；**人格漂移（Personality Drift）** = Agent 输出性格偏离既定 SOUL。两者都是**渐进、隐蔽**的，业界（MemGPT/Letta/Mem0/Zep）全部聚焦「记忆存取」，**无人做漂移治理**——这是本书的独家赛道（v1.0 卷五模块4/6）。

**解法**：建立「哈希基线 + 定期比对」的漂移哨兵：

```bash
# 1) 建立协议文件基线
cd ~/.openclaw/workspace
find agents -name 'SOUL.md' -exec sha256sum {} \; > /tmp/soul-baseline.txt

# 2) 每周比对（或每次大改后）
find agents -name 'SOUL.md' -exec sha256sum {} \; > /tmp/soul-now.txt
diff /tmp/soul-baseline.txt /tmp/soul-now.txt && echo "✅ 无人格漂移" || echo "⚠ 人格文件已变，复核"
```

**验证命令**：

```bash
# 期望：无变化时 diff 无输出
diff /tmp/soul-baseline.txt /tmp/soul-now.txt
```

**预防**：把「漂移哨兵」并入每周体检清单（Weekly Health Checklist，v1.0 卷五模块6）；偏差超阈值（约定 1%）即告警。

---

## F2-13 · 问：ACP 改名 SLCP 后，协议引用没跟着改。

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：对外文档/plugin 里仍写着 `ACP`，被指出与 IBM/BeeAI 的 ACP 商标冲突（该 ACP 已于 2025-08 合并入 A2A）。

**原因**：v1.0 卷七用「ACP」指代自造的协同协议，但 `ACP` 一词已被业界占用。v3.0 改名表第一条要求：对外 + 工程接口一律改为 **SLCP（Silicon-Life Coordination Protocol）**；内部稿可保留黑话，但首次出现必须双写「SLCP（原：ACP）」。

**解法**：全仓改名 + 双写过渡：

```bash
cd ~/.openclaw/workspace/references/silicon-life-handbook
# 1) 找出所有 ACP 用法（排除 A2A/A2A 误伤）
grep -rn "\bACP\b" --include="*.md" . | grep -v "A2A" | head
# 2) 对外文档改为 SLCP（原：ACP）双写
# 3) 工程接口（plugin/RFC）直接写 SLCP
```

**验证命令**：

```bash
# 对外文档不应再出现裸 ACP（应已双写为 SLCP（原：ACP））
grep -rn "\bACP\b" --include="*.md" openclaw-silicon-life-handbook-v2026.9-industry-standard/ | grep -v "SLCP（原：ACP）"
# 期望：无输出
```

**预防**：改名表纳入 CI lint；任何新增术语先查 [术语对照表 v3.0](../00-术语对照表·v3.0行业标准版.md) 是否冲突。

---

## F2-14 · 问：AGENTS.md 的子 Agent 声明怎么和 Claude Agent SDK subagent task spec 对位？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：想把本书的 AGENTS 协议接到业界标准，不知道字段该怎么映射。

**原因**：两者语义相近但载体不同。Claude Agent SDK 用 **subagent task spec**（可编程任务规格）；OpenClaw 用 **AGENTS.md 文件声明**（启动时加载）。映射好了能互操作，映射错了会「看着像其实不通」。v4.0 二卷给出对位：AGENTS ≈ Claude 的子 Agent 声明，但 **OpenClaw 声明在文件、Claude 声明在代码**。

**解法**：按语义建映射表：

| 本书（AGENTS.md） | Claude Agent SDK | 说明 |
|---|---|---|
| 子 Agent 名 | subagent name | 需逐字一致 |
| 调度规则 | task routing | 文件声明 vs 代码声明 |
| 上报关系 | parent/child 层级 | 对位 IDENTITY 的 reports_to |

**验证命令**：

```bash
# 列出本机 AGENTS 声明的子 Agent，作为映射输入
grep -rhE "subagents|sublings" ~/.openclaw/workspace/agents/*/AGENTS.md | head
```

**预防**：对外集成前先出映射表评审；⏳ Claude SDK 具体字段名以官方文档为准，本表为语义对位。

---

## F2-15 · 问：协议文件要不要纳入版本管理 / git？

> 环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27

**现象**：协议被改来改去，出了事故无法回溯是哪次改动、改了什么。

**原因**：没有版本史时，F2-2 的人格漂移、F2-1 的自动回写都**无法举证**。v1.0 卷六模块3「三证据验证（TEV）」要求「新产物 / 前后 Diff / 测试日志」——其中「前后 Diff」**必须以版本管理为前提**。

**解法**：对 `agents/` 与协议文件建仓：

```bash
cd ~/.openclaw/workspace
git init -q 2>/dev/null || true
cat > .gitignore <<'EOF'
logs/
cache/
*.log
EOF
git add agents config.json 2>/dev/null
git commit -q -m "chore: 协议文件纳入版本管理（TEV 前置）" || echo "已提交"
```

**验证命令**：

```bash
git -C ~/.openclaw/workspace log --oneline -- agents/ | head
# 期望：有条目；改动可追溯
```

**预防**：把「协议文件变更必留 commit」写进治理约定；每次事故复盘直接引用 commit diff 作为证据。

---

## 验收清单

- [ ] 每问均含「现象 / 原因 / 解法 / 验证命令」四段
- [ ] 每问顶部标注 `项目环境：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27`
- [ ] 每题有可执行命令（15+ 条）
- [ ] 真实来源引用：v1.0 卷五（人格/文档漂移、边界三档、体检）、v1.0 卷六（TEV）、v1.0 卷七（军团编制）≥5 次；v4.0 二卷协议对位 ≥2 次；ACP→SLCP 改名（F2-13）≥1 次；reserveTokensFloor 误植（F2-11）；8/19 军团断线（F2-6）；afrexai 类真实 skill 目录（F2-4 语境）
- [ ] 术语合规：SOUL/AGENTS/USER 加英文；ACP 双写「SLCP（原：ACP）」
- [ ] 越界检查：仅含 F2 主题
- [ ] 未抄 v1.0/v4.0 原文；未写「diff v1.0」类内容

---

## 诚实边界声明

1. **字段名**：F2-1 的 `writeBackPolicy`、F2-3 的 `permissions` 三档、F2-7 的 IDENTITY 字段均为**治理层建议命名**，⏳ 精确 schema 以本机 OpenClaw 2026.9.4 plugin/agent schema 为准。
2. **解析优先级**：F2-10 的优先级序为本书治理约定，非 OpenClaw 内核硬规范，⏳ 待与实现核对。
3. **业界对位**：Claude Agent SDK 字段名为语义对位，未经逐字段实测。
4. **未虚构**：全部问题源自 v1.0/v4.0/调研报告/本机环境真实现象；未经复现处已标 ⏳。

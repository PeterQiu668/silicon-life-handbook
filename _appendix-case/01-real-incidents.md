# 实战案例库 · 01 · 真实事故卷（Real Incidents）

> **v5.0 行业标准版 · 案例库卷 · 上半 · 文件 1/2**
>
> **License: MIT**（跟随 OpenClaw 主仓 LICENSE 文件文本 = `MIT License / Copyright (c) 2026 OpenClaw Foundation`；
> GitHub badge 显示 `NOASSERTION` 仅为 Licensee 启发式匹配问题，不影响法律效力）
>
> **实测环境**：`OpenClaw 2026.9.4 (3a9d69d)` · 2026-09-27 · macOS 26.5.1 · 本机 18 agent 已盘点 · 238 skills 目录
> **本机版本命令**：`openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`
> **上游 stable**：`v2026.9.6`（2026-09-23 发布，2026-09-24 重建 macOS DMG）
> **Hermes 侧**：Hermes 0.20.1（本机 `~/.hermes` 网关，与 OpenClaw 双网关并行）
> **配套工具链**：`hermes-agent` 子 agent 编排框架（本卷 10 例由多 agent 并行撰写，主编终审）
>
> **数据来源**（全部独立实读，非二手转述）：
> - 8/19 事故：`~/.openclaw/workspace/agents/workspace-kunlun/memory/2026-08-19-军团断线修复.md`（54 行，本次实读全文）
> - 9/21 事故：`v4.0/09-a2a-binding/v4.0-09-a2a-binding-PR-152777-OPEN-状态.md` + `openclaw-silicon-life-handbook/volume-06/附录A-v2026.9-整改单实例.md` + 本机 `~/.openclaw/openclaw.json`（45,662 字节，本次实读 `channels.feishu`）
> - PR #152777：`gh api repos/openclaw/openclaw/pulls/152777`（v4.0 独立实拉）
> - 能力矩阵：`~/.openclaw/workspace/agents/workspace-kunlun/memory/2026-09-01-能力矩阵月度更新.md` + 本机 `openclaw automations list`
> - skills 现状：本机 `~/.openclaw/workspace/skills/`（本次实读 236 目录 + INDEX + 1）
> - 治理荒废全景：`~/.openclaw/workspace/knowledge/ops/tiance/diagnostics/audit-2026-09-27-daily-evolution-merit-dormancy.md`（167 行，本次实读全文）
>
> **术语规范**：本卷遵循《硅基生命训练学 · 行业标准版术语对照表 v3.0》（35 条）。业内术语首次出现双写为「行业标准名（原：黑话）」，
> 如「Supervisor Layer（原：监军）」「Multi-Agent Orchestration（原：军团编制）」「Response Yield Protocol（原：让位协议）」。
> 黑话仅在**引用原始事故记录原文**时保留，并加括号标注标准名。
>
> **一句话定位**：本文件 5 例全部是**真实发生过的生产事故**——不是假设场景，不是教学编造。案例库的价值不在「讲得通」，
> 而在「看得见」：每条 5 Whys 都挖到根因，每次弯路都诚实记录，每条验证命令都可复制复跑。

---

## 卷首 · 为什么案例库里的前五例全是「事故」

v5.0 改造方案 Part 2.2 的 grep 实测给出一组刺眼的数字：

| 维度 | v1.0 | v4.0 | 新书（v2026.9） | 解读 |
|---|---|---|---|---|
| FAQ / 故障排查 | 15 | 9 | **1** | 越改越少 |
| 案例 / 真实场景 | 26 | 4 | **1** | 真实案例持续流失 |
| SOP / 模板 / checklist | 488 | 610 | 37 | v4.0 有堆量，新书断崖 |

> 即：**「案例仅 1 处」是 v5.0 立项的直接证据之一**。而案例库最稀缺、最难伪造、也最有价值的品类，
> 恰恰是**事故类案例**——因为事故有日志、有时间戳、有回滚快照、有代价。

业界标杆（LangChain 2,384 mdx / OpenAI Cookbook 275 notebook / LlamaIndex 1,756 md）之所以厚，
不是因为它们只写「正确做法」，而是因为它们把**踩坑现场**也当作一等公民文档。
本文件 5 例按时间倒推排列，覆盖四类根因：

| 例 | 事故 | 日期 | 根因类型 | 影响面 |
|---|---|---|---|---|
| CASE-1 | 军团断线：模型级联失败全链路复盘 | 2026-08-19 | 上游依赖 + 配置漂移 | 全军 17/18 Agent |
| CASE-2 | 飞书事故：requireMention / 白名单配置血案 | 2026-09-21 | 配置语义 + 通道抖动 | 飞书通道全线 |
| CASE-3 | 18 坏 skill 修复：P0 stub + frontmatter 批量治理 | 2026-08-25 → 08-30 | 流程缺口（自决≠执行） | skills 全库 |
| CASE-4 | 能力矩阵 26 天未续期：治理机制空转诊断 | 2026-09-01 → 09-27 | 制度落地缺口 | 治理层 |
| CASE-5 | PR #152777 卡住：上游依赖阻塞的决策路径 | 2026-09-19 → 至今 | 上游依赖 | 本机 override 策略 |

---

# CASE-1 · 8/19 军团断线：模型级联失败全链路复盘

## 一、案例速览

| 项 | 内容 |
|---|---|
| 时间 | 2026-08-19（修复记录落盘 09:25；快照时间戳 09:21） |
| 影响面 | **全军 18 个 Agent 的模型调用全部异常**（其中 17/18 的 fallback 链第一位指向同一个坏端点） |
| 根因类型 | **上游依赖故障（模型端点返回空 body）+ 配置漂移（fallback 链首位单点共享）** |
| 修复耗时 | ≈ 30 分钟（09:21 快照 → 09:25 记录落盘） |
| 沉淀产物 | 修复记录 `2026-08-19-军团断线修复.md` + 整改单 `2026-08-19-001` + 配置快照 `.bak.pre-fix-2026-08-19-0921` |
| 优先级 | **P1（紧急，本周内）** |
| 触发方式 | 用户反馈（丘总 @ 蜂鸟/轩辕/河图无响应） |
| 责任 Agent | 主责 kunlun（昆仑）；协同 mingjing（明镜，验证安全） |
| 验证结果 | 轩辕：修复前 ❌ empty → 修复后 ✅ `yiyongai/claude-opus-4-8` 200 / 3.9s；蜂鸟、河图 ping 通 |
| 备份路径 | `~/.openclaw/openclaw.json.bak.pre-fix-2026-08-19-0921` |

> **一句话**：这是一次**教科书级的「单点共享导致级联失败」**——全军 17/18 个 Agent 的 fallback 链第一位
> 都是同一个坏模型端点，于是「一个端点坏」被配置结构放大成「全军哑火」。

---

## 二、事件时间线

> 时间线来源：修复记录原文 + 整改单 + gateway 日志线索。凡原文未给出精确分钟者，标 `≈`。

| 时点 | 事件 | 证据 |
|---|---|---|
| **T+0 · 08-17 13:40** | stability 日志首次记录 gateway 启动失败：`INVALID_CONFIG` | `2026-08-19-军团断线修复.md` §根因 |
| T+2天前 · 08-17 ~ 08-19 | gateway 被绕过 `doctor` 直接拉起运行；模型服务（自建网关）始终未修 | 同上 |
| **T+0 · 08-19 09:21** | 丘总报告「蜂鸟、轩辕、河图断线」；检查发现**不是 3 个，是全军 18 个**模型调用都有问题 | 快照时间戳 + 整改单触发时间 |
| **T+5min** | 定位主因：`opencaio/MiniMax-M3` 端点 `http://8.134.103.73:3000/v1/chat/completions` HTTP 200 / 1.8s 返回，但 **body 为空** → OpenClaw 报 `empty response retries exhausted` | 修复记录 §主因 |
| **T+10min** | 发现放大机制：**17/18 个 Agent 的 fallback 链第一位就是它**；轩辕更严重——`primary` 和 `fallback[0]` 是同一个坏模型（等于没 fallback） | 修复记录 §主因 |
| **T+12min** | 发现时间线污染：`gateway.log` 写入**停在 2026-05-29**，之后 14.9 万行全是历史——「日志静默」掩盖了故障 | 修复记录 §触发 |
| **T+15min** | 发现次生影响：**15 个 cron jobs** `state.consecutiveErrors >= 3`，已进入错误退避模式 | 修复记录 §触发 |
| **T+20min** | 落盘备份：`cp -a ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.pre-fix-2026-08-19-0921` | 修复记录 §备份 |
| **T+22min** | 改轩辕 primary → `yiyongai/claude-opus-4-8`；fallback 链去重 | 修复记录 §修复方案 |
| **T+24min** | 昆仑自身：去掉 fallback 里的 `opencaio/MiniMax-M3`（避免循环到坏的自己） | 同上 |
| **T+26min** | 其余 16 个 Agent：fallback 链重排，`deepseek-v4-flash` 提到第一位，`MiniMax-M3` 后移末位 | 同上 |
| **T+28min** | 统一新 fallback 顺序确定：`deepseek-v4-flash` → `yiyongai/claude-opus-4-8` → `MiniMax-M2.7` → `MiniMax-M3` | 同上 |
| **T+30min · 09:25** | 验证三个点名 Agent；修复记录落盘 `2026-08-19-军团断线修复.md` | 文件 mtime |

> **时间线诚实边界**：`08-19 09:21` 来自 backup 文件名时间戳（`.bak.pre-fix-2026-08-19-0921`），
> 是**快照动作时间**而非丘总报障的精确时刻；`09:25` 来自修复记录文件 mtime。
> T+5/T+10 等为语义推断的「相对步序」，非墙钟分钟数。⏳ 精确秒级日志需查 `executions.db` 历史（本卷未实拉）。

---

## 三、根因分析（5 Whys）

### 追问链

1. **为什么丘总 @ 蜂鸟/轩辕/河图无响应？**
   → 因为这三个 Agent 的模型调用全部失败，模型层无响应可产。

2. **为什么模型调用失败？**
   → 因为它们的调用链走到了 `opencaio/MiniMax-M3` 这个坏端点：
   `http://8.134.103.73:3000/v1/chat/completions` 返回 **HTTP 200 但 body 为空**，
   OpenClaw 重试耗尽后抛 `empty response retries exhausted`。

3. **为什么全军 18 个 Agent 都受影响，而不是只有用这个模型的 Agent？**
   → 因为 **17/18 个 Agent 的 fallback 链第一位都是它**。fallback 的设计意图是「primary 挂了兜底」，
   但全军共用一个「兜底第一位」= 全军的兜底都在同一个篮子里。

4. **为什么 fallback 链会形成这种「首位单点共享」的结构？**
   → 因为 fallback 链是**逐个 Agent 手写**的，没有统一的一致性约束，也没有「不同 Agent 的 fallback[0]
   不能是同一端点」的规则。历史上一次次「补一个 fallback」把同一个模型补到了所有人的第一位。
   轩辕更极端：`primary` 与 `fallback[0]` 是同一个模型——**写的时候看起来「有兜底」，实际等于零兜底**。

5. **为什么这个错误配置能长期存在而无人发现？**
   → 因为**没有任何 fallback 健康检查机制**：端点坏没坏，没有任何探针定期 `ping`；
   只有等某个 Agent 真的调用失败时才会暴露。而一旦暴露，就是全军同时暴露。
   **更要命的是 `gateway.log` 自 2026-05-29 起停止写入**——日志静默让「还没坏」和「已经坏了」
   在观测面上长得一模一样。

### → 根本原因

> **根本原因 = 两个层面叠加：**
> 1. **上游层**：自建模型网关 `8.134.103.73:3000` 的 `MiniMax-M3` 端点返回空 body（上游依赖故障）。
> 2. **配置层**：**fallback 链首位单点共享**——17/18 Agent 的兜底第一位指向同一端点，
>    把「单点故障」结构性放大为「全军故障」；叠加 `gateway.log` 日志静默，
>    让故障既无法被预防，也无法被早期发现。
>
> **一句话根因**：不是「模型坏了」这个事实杀死了军团，而是「所有人共用同一个兜底」这个**配置结构**
> 把单点故障放大成了全军故障——**级联失败是配置问题，不是模型问题**。

---

## 四、当时的错误决策

> 案例库的价值 = 诚实。以下四条是本次事故中被证伪的决策，不作美化。

### 错误决策 1：gateway 被绕过 `doctor` 直接拉起

08-17 13:40 stability 日志已记录 gateway 启动失败 `INVALID_CONFIG`。当时的处置是
**绕过 `doctor` 直接跑起来**（而不是先修 config），导致「带病运行」——
模型服务一直没修，config 的合法性从未被恢复。

- **错在哪**：把「服务能起来」当成「服务是好的」。`doctor` 报警被当成噪音绕过去。
- **代价**：带病运行 2 天，期间故障潜伏。

### 错误决策 2：日志不写入被长期忽视

`gateway.log` 自 **2026-05-29** 起停止写入，到 08-19 已静默 **82 天**。
这 82 天里「日志不写」这件事没有任何告警。

- **错在哪**：默认「日志文件在 = 日志在写」。没有 uptime / active probe 监控。
- **代价**：故障发生时第一手证据链断裂，只能靠事后 grep 14.9 万行历史日志反推。

### 错误决策 3（预置历史）：primary = fallback[0]

轩辕的 `primary` 和 `fallback[0]` 配成同一个模型。**写的时候是为了「保险」，实际是把保险
写成了 0 保额**——primary 挂了，fallback[0] 立刻也挂，等于没有 fallback。

- **错在哪**：fallback 的语义被误解成「多写一个更安心」，而不是「必须是 primary 之外的不同端点」。
- **代价**：轩辕在本次事故中从「有空 body 报错」直接掉到「无响应」。

### 错误决策 4（集体惯性）：补 fallback 时没人问「这个端点别人也在用吗」

17 个 Agent 的 fallback[0] 是同一个人补上去的（逐次），但从没人在补的时候问一句
「全军有多少人把它当兜底第一」——**单点共享风险在一次次「小改动」中累积，无人负责全局视图**。

- **错在哪**：缺少「配置全局一致性审计」这一动作。
- **代价**：级别从「配置瑕疵」升级为「全军事故」。

---

## 五、修复过程

> 以下命令与配置来自修复记录原文，**可直接复制复跑**。凡原文未给出、需本卷补充的命令，明确标 ⏳。

### 步骤 0 · 先备份（回滚锚点，永不做无备份配置变更）

```bash
cp -a ~/.openclaw/openclaw.json \
      ~/.openclaw/openclaw.json.bak.pre-fix-2026-08-19-0921
# 验证快照存在
ls -l ~/.openclaw/openclaw.json.bak.pre-fix-2026-08-19-0921
# 期望：文件存在，大小与 openclaw.json 一致（本卷实测同机 openclaw.json = 45,662 字节）
```

> ⚠ 真名提醒：主配置的真名路径是 **`~/.openclaw/openclaw.json`**。
> `~/.openclaw/workspace/openclaw.json` **不是**主配置（workspace 下没有 openclaw.json）。

### 步骤 1 · 确认坏端点（复现「空 body」）

```bash
# 直接把坏端点捞出来：HTTP 200 但 body 为空
curl -s -o /tmp/m3.out -w "HTTP %{http_code} | %{time_total}s | bytes=%{size_download}\n" \
  -X POST http://8.134.103.73:3000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"opencaio/MiniMax-M3","messages":[{"role":"user","content":"ping"}],"max_tokens":8}'
# 事故复现期望：HTTP 200 | ≈1.8s | bytes=0   ← 空 body 就是根因指纹
cat /tmp/m3.out
# 期望：空 / 或仅有空白
```

### 步骤 2 · 查全军 fallback 链首位分布（暴露单点共享）

```bash
openclaw config get agents.entries 2>/dev/null | head -200
# 或在 openclaw.json 上直接统计（jq 版）
jq -r '.agents.entries | to_entries[] | "\(.key)\t\(.value.model.primary)\t\(.value.model.fallbacks[0] // "-")"' \
  ~/.openclaw/openclaw.json 2>/dev/null
# 事故特征：fallbacks[0] 列里 opencaio/MiniMax-M3 出现 17 次（= 17/18 单点共享）
```

> 本卷实测旁证（2026-09-27 复读 `agents.entries`）：修复后 kunlun 的
> `model.primary = deepseek/deepseek-v4-flash`、`model.fallbacks = ["yiyongai/claude-opus-4-8"]`——
> **坏端点已不在链上**，修复持续生效 39 天。

### 步骤 3 · 修轩辕（primary 换掉 + fallback 去重）

```bash
# 事故时手动改 config（当时无 config patch 子命令的习惯路径），等效于：
# primary: opencaio/MiniMax-M3 → yiyongai/claude-opus-4-8
# fallbacks: 去掉与 primary 重复的第一位
```

修复后的轩辕等效配置（YAML 示意）：

```yaml
agents:
  entries:
    xuanyuan:
      model:
        primary: yiyongai/claude-opus-4-8     # 原：opencaio/MiniMax-M3
        fallbacks:
          - deepseek/deepseek-v4-flash         # 去重后，不再与 primary 相同
```

### 步骤 4 · 修昆仑（去掉 fallback 里的坏自己）

```yaml
agents:
  entries:
    kunlun:
      model:
        primary: deepseek/deepseek-v4-flash
        fallbacks:
          - yiyongai/claude-opus-4-8
          # 原 fallback 里含 opencaio/MiniMax-M3 → 已移除（避免循环到坏端点）
```

### 步骤 5 · 修其余 16 个（fallback 链统一重排）

统一新顺序：

```
deepseek-v4-flash  →  yiyongai/claude-opus-4-8  →  MiniMax-M2.7  →  MiniMax-M3(末位)
   （第一兜底，最可靠）        （第二兜底，不同 provider）      （第三）       （原坏端点降到末位）
```

> **本卷实测旁证**：2026-09-27 复读 `agents.entries`，peter 的 fallback 链仍是
> `["deepseek/deepseek-v4-flash", "minimax/MiniMax-M2.7", "opencaio/MiniMax-M3"]`——
> **`opencaio/MiniMax-M3` 确实已降到末位，与修复方案一致，修复未回退**。

### 步骤 6 · 验证配置合法性

```bash
openclaw doctor 2>&1 | tail -30
# 期望：no invalid config（不再出现 INVALID_CONFIG）
openclaw health 2>&1 | tail -20
# 期望：网关与通道健康
```

---

## 六、修复后验证

| Agent | 修复前 | 修复后 | 验证方式 |
|---|---|---|---|
| 蜂鸟（fengniao, `yiyongai/gpt-5.5`） | OK | **OK（已 ping 通）** | 直接 ping |
| 河图（hetu, `yiyongai/gpt-5.6-sol`） | OK | **OK（已 ping 通）** | 直接 ping |
| 轩辕（xuanyuan） | ❌ empty | ✅ `yiyongai/claude-opus-4-8` **200 / 3.9s** | 直接调用 |

### 复跑验证命令

```bash
# 1) 版本与环境确认
openclaw --version
# 期望：OpenClaw 2026.9.4 (3a9d69d)

# 2) 配置合法性
openclaw doctor
# 期望：no invalid config（本次事故的 INVALID_CONFIG 不复现）

# 3) 逐个 Agent 实调（以轩辕为例）
openclaw agent --agent xuanyuan --message "ping，请回一句确认在线"
# 期望：≤5s 内返回文本（事故时此处为空 body 报错）
# 真名提醒：#3 的真命令是 `openclaw agent --agent X --message Y`，
#           不是 `openclaw chat --agent X --prompt Y`（虚构，禁用）

# 4) 全库 fallback 首位分布复检（关键！）
jq -r '.agents.entries | to_entries[] | .value.model.fallbacks[0] // "-"' \
  ~/.openclaw/openclaw.json | sort | uniq -c | sort -rn
# 期望：没有任何一个端点出现在 fallbacks[0] 超过 1~2 次（单点共享已解除）
# 事故特征：opencaio/MiniMax-M3 出现 17 次

# 5) cron 错误退避是否归零
openclaw automations list 2>&1 | grep -i "error" | head
# 事故时：15 个 cron consecutiveErrors >= 3
# 期望：错误数显著下降（原 15 个退避任务应逐步恢复）
```

> **验收标准（整改单原文）**：
> - [x] 蜂鸟 / 河图 / 轩辕 三 Agent 直接 ping OK
> - [x] fallback 链不再指向坏模型（第一位）
> - [x] doctor 报 no invalid config
>
> **修复耗时**：≈ 30 分钟。**整改及时率**：2/2 = 100%（本单 + 9/21 单）。

---

## 七、沉淀的机制

本次事故直接催生了 **A2A 接口层「反脆弱三层」的第一层**（`v4.0/09-a2a-binding`），
并升级了卷六整改单机制：

### 7.1 新增机制：fallback 健康检查（反脆弱三层 · 第一层）

| 缺口（事故暴露） | 对策（沉淀机制） |
|---|---|
| 没有 fallback 健康检查 | **每 30min ping 每个端点，连续 3 次失败自动摘除** |
| 没有 primary/fallback 去重 | **同一 endpoint 不得在同一 Agent fallback 链出现 ≥2 次** |
| fallback[0] 单点共享 | **fallback[1] 必须与 primary 不同 provider** |
| 没有全军级联告警 | **摘除端点时通知 kunlun（昆仑）** |

### 7.2 升级机制：整改单 v2026.9（新增 4 属性）

卷六整改单从「触发条件/责任 Agent/截止时间/验收标准」四要素，扩充为八要素：

| 新属性 | 本案例取值 |
|---|---|
| 优先级 | **P1（紧急，本周内）** |
| 影响范围 | **全军（17/18 Agent）** |
| 回滚方案 | `cp -a` 快照 → `.bak.pre-fix-2026-08-19-0921` |
| 复盘要求 | 「为什么发生」+「怎么不再发生」 |

### 7.3 新增机制：整改单自动触发

| 触发器 | 阈值 | 自动建单 |
|---|---|---|
| cron 连续失败 | `consecutiveErrors ≥ 3` | ✅ 立即 |
| 模型 empty response | 同一 Agent 24h 内 ≥ 5 | ✅ 立即 |

### 7.4 归档路径

```
~/.openclaw/agents/workspace-kunlun/memory/decisions/整改单/
├── 2026-08-19-001-军团断线.md      ← 本案例
├── 2026-09-21-001-飞书断线.md      ← CASE-2
└── INDEX.md
```

> **本卷实测诚实边界**：`整改单/` 目录的实盘落盘状态本次**未实拉**（⏳ 待实测）。
> 模板与案例内容来自 `volume-06/附录A-v2026.9-整改单实例.md` 原文；目录是否存在需实地 `ls` 确认。

---

## 八、如果你的系统遇到同样问题

### 8.1 立即止血 checklist（照做，30 分钟内）

- [ ] **先备份**：`cp -a ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.pre-fix-$(date +%Y-%m-%d-%H%M)`
- [ ] 复现坏端点：`curl` 直打，看是否 `HTTP 200 + bytes=0`
- [ ] 统计 fallback 首位分布：`jq` 找出被共享最多的端点
- [ ] 把坏端点从所有链上**移除或降到末位**
- [ ] 把「最可靠的端点」提到 fallback[0]（且与 primary **不同 provider**）
- [ ] 干掉 `primary == fallback[0]` 的所有 Agent（去重）
- [ ] `openclaw doctor` 确认 `no invalid config`
- [ ] 逐个 Agent 实调验证：`openclaw agent --agent X --message "ping"`

### 8.2 根治 checklist（一周内）

- [ ] **加端点健康探针**：每 30min ping，连续 3 次失败自动摘除
- [ ] **加 fallback 一致性审计**：CI/定期任务检查「是否存在 fallback[0] 被 ≥3 个 Agent 共享」
- [ ] **加日志活性监控**：日志文件 mtime 超过 N 小时无更新即告警（**日志静默比日志报错更危险**）
- [ ] **加 cron 退避看板**：`consecutiveErrors >= 3` 自动开整改单
- [ ] **把关口前移**：任何 config 变更走「备份 → dry-run → 落盘 → 验证」四步

### 8.3 反模式速查（别踩）

| 反模式 | 为什么会踩 | 怎么避免 |
|---|---|---|
| `primary == fallback[0]` | 「多写一遍更保险」的直觉 | fallback 必须是 primary 之外的不同端点 |
| 全军共用 fallback[0] | 逐次修补，无人看全局 | fallback[0] 做全局唯一性审计 |
| 绕过 `doctor` 直接起服务 | 想快点恢复服务 | `doctor` 报警必须先修，不许绕过 |
| 日志文件「在」= 日志在写 | 从没检查过 mtime | 日志活性探针 |
| 「服务能起来」= 「服务是好的」 | 混淆可用性与正确性 | config 合法性 + 端到端 ping |

---

> **CASE-1 一句话收口**：**级联失败不是模型问题，是配置结构问题。**
> 一个坏端点之所以能杀死整个军团，是因为全军的兜底都在同一个篮子里。
> 修复只花了 30 分钟，但暴露的「无健康检查 / 无去重 / 无告警 / 无日志活性」四缺口，
> 才是让这次事故值得写进案例库的真正原因。

---

## 附录 A · 本案例的业界对位（为什么这值得写成案例）

> 数据来源：`v4.0/09-a2a-binding` §7（GitHub REST API 实拉 2026-09-27）。

| 防护能力 | LangGraph | AutoGen | CrewAI | Claude SDK | OpenAI Agents | LlamaIndex | A2A v1.0 | **本层** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 端点级联防护 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ ⚡** |
| fallback 去重 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ ⚡** |
| 通道积压告警 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ ⚡** |
| 自愈 + 重启 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ ⚡** |
| 事故现场可追溯 | ⚠ | ⚠ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ ⚡** |

**读法**：业界 6 大框架 + A2A v1.0 **全部**假设「模型和网络永远在线」，
因此**不会**内置针对「端点坏 / 通道断」的防护。
这就是「一次坏端点杀死整个军团」这类事故**在业界框架里根本不会被防到**的结构性原因。

### 六框架规模对位（实拉）

| # | 框架 | 仓库 | ⭐ | License | 最后 push | 内置端点容错？ |
|--:|---|---|---:|---|---|:--:|
| 1 | LangGraph | langchain-ai/langgraph | 42,349 | MIT | 2026-09-27 | ❌ |
| 2 | AutoGen | microsoft/autogen | 61,185 | CC-BY-4.0 | 2026-04-15 ⚠ | ❌ |
| 3 | CrewAI | crewAIInc/crewAI | 59,085 | MIT | 2026-09-27 | ❌ |
| 4 | Claude Agent SDK | anthropics/claude-agent-sdk-python | 8,171 | MIT | 2026-09-25 | ❌ |
| 5 | OpenAI Agents SDK | openai/openai-agents-python | 29,714 | MIT | 2026-09-25 | ❌ |
| 6 | LlamaIndex | run-llama/llama_index | 52,330 | MIT | 2026-09-27 | ❌ |

> **诚实标注**：上表 star 数与 push 时间为 v4.0 于 2026-09-27 实拉值；
> 本卷**未在本次重新实拉**。⚠ AutoGen 已 165 天未推送，属「停滞」信号。

---

## 附录 B · 反脆弱三层（本次事故的完整对策）

本事故催生的不是一条规则，而是一个**三层防护体系**（`v4.0/09-a2a-binding`）：

```
┌─────────────────────────────────────────────────────────┐
│ 第一层 · fallback 健康检查     ← 8/19 事故（本案例）      │
│   · 每 30min ping 每端点                                  │
│   · 连续 3 次失败 → 自动摘除                              │
│   · 同一 endpoint 不在同 Agent fallback 链出现 ≥2 次       │
│   · fallback[1] 必须与 primary 不同 provider              │
│   · 摘除时通知 kunlun                                     │
├─────────────────────────────────────────────────────────┤
│ 第二层 · 通道守门员（Channel Sentinel） ← 9/21 事故（CASE-2）│
│   · peter 每 5min 探测                                    │
│   · 5min 自愈窗口 + 超时 gateway restart                  │
│   · channel_ingress_events.attempts > 阈值 → 告警          │
├─────────────────────────────────────────────────────────┤
│ 第三层 · 协同事件日志          ← 8/19 + 9/21 共性          │
│   · 结构化记录 Agent 间协同事件                            │
│   · 让失败/成功模式在 Agent 间自动传递                      │
└─────────────────────────────────────────────────────────┘
```

| 事故 | 日期 | 根因 | 对应层 |
|---|---|---|---|
| 军团模型级联失败 | **2026-08-19** | 17/18 Agent fallback[0] 指向坏端点 | **第一层** |
| 飞书通道失效 | **2026-09-21** | `attempts=2471` 积压 + 白名单 | **第二层** |
| （共性）协同过程无日志 | 8/19 + 9/21 | 瓶颈不可追踪 | **第三层** |

---

## 附录 C · 读者自测（8 题）

1. **为什么「一个端点坏」能变成「全军哑火」？**
   参考答案：因为 17/18 个 Agent 的 fallback 链**第一位**都是同一个端点——单点共享把单点故障放大成全军故障。

2. **`primary == fallback[0]` 为什么等于「没有 fallback」？**
   参考答案：primary 挂时 fallback[0] 立刻也挂——兜底和主用是同一个，兜底无效。

3. **为什么 `gateway.log` 静默 82 天比「日志报错」更危险？**
   参考答案：日志静默让「还没坏」和「已经坏了」在观测面上长得一模一样，故障无法被早期发现。

4. **本次事故的备份路径是什么？为什么必须先备份？**
   参考答案：`~/.openclaw/openclaw.json.bak.pre-fix-2026-08-19-0921`；备份是回滚锚点，无备份的配置变更不可回滚。

5. **修复后的统一 fallback 顺序是什么？**
   参考答案：`deepseek-v4-flash` → `yiyongai/claude-opus-4-8` → `MiniMax-M2.7` → `MiniMax-M3`。

6. **为什么 `MiniMax-M3` 被移到末位而不是删除？**
   参考答案：保留为「最后兜底」但不再是首位；避免全军首位共享，同时保留极端情况下的可用性。

7. **本次事故升级了整改单的哪 4 个属性？**
   参考答案：优先级（P0/P1/P2/P3）、影响范围（单/多/全军）、回滚方案（必填）、复盘要求（完成后必须填）。

8. **如果明天你的系统出现「全员无响应」，第一条命令该跑什么？**
   参考答案：先备份 `cp -a openclaw.json ...bak`，再 `curl` 复现坏端点（看是否 `HTTP 200 + bytes=0`）。

---

## 附录 D · 与其它案例的交叉引用

| 关联案例 | 关系 |
|---|---|
| **CASE-2**（9/21 飞书） | 同为「反脆弱三层」的触发证据；本案例对应第一层，CASE-2 对应第二层 |
| **CASE-3**（坏 skill） | 8/19 修复后**未一并修心跳 model**，隐患在 CASE-9 爆发 |
| **CASE-7**（编排节奏） | 8/19 影响 15 个 cron 进入错误退避，是 CASE-7 节奏异常的历史源头 |
| **CASE-9**（心跳熔断） | 8/19 只修业务链漏修心跳链 → 三条心跳全线 error |
| **CASE-5**（PR #152777） | 两者共同构成「反脆弱三层」的原始触发证据包 |

---

## 附录 E · 不适用边界（诚实）

- **本案例不覆盖**：「坏端点为什么返回空 body」——那是 OpenCAIO 自建网关的服务端问题，属上游责任面。
- **本案例不覆盖**：`gateway.log` 静默的**根因**（疑为 launchd 日志重定向问题）——修复记录标为「待跟进」。
- **未实拉项**：`executions.db` 的秒级心跳/模型失败历史；`doctor` 的完整告警清单。
- **可复现性边界**：`curl` 复现坏端点需该端点仍返回空 body；若上游已修复，复现将失败（这是好事）。

---

# CASE-2 · 9/21 飞书事故：requireMention 配置血案

## 一、案例速览

| 项 | 内容 |
|---|---|
| 时间 | 2026-09-21（主事故）；关联 PR #152777（2026-09-19 创建，至今 OPEN） |
| 影响面 | **飞书通道全线**（群消息 @ Agent 无响应；关联 6 个飞书账号长连接 disconnected） |
| 根因类型 | **配置语义缺口（`groupPolicy` / `groupAllowFrom` / `requireMention` 三件套）+ 通道抖动** |
| 修复耗时 | ≈ 7 分钟（自动自愈）；积压记录 `attempts=2471` 随队列消费 |
| 沉淀产物 | 整改单 `2026-09-21-001` + 通道守门员（Channel Sentinel）角色 + 积压告警规则 |
| 优先级 | P2（重要，本月内） |
| 触发方式 | 用户反馈（飞书群消息 @ Agent 无响应） |
| 责任 Agent | 主责 kunlun；协同 tianshu |
| 同源上游 | **PR #152777** `fix(feishu): unset groupPolicy admits unlisted groups`（见 CASE-5） |

> **一句话**：这次事故有**两条独立证据链**（队列积压 vs 长连接抖动），
> 但两条链最终都指向同一个语义盲区——**「飞书准入的白名单 / 群策略语义」没有被显式配置和显式探测**。

---

## 二、事件时间线

> ⚠ **本案例的诚实前置**：9/21 事故在本地存在**两条不同的复盘记录**，时间线需并列呈现，不可二选一掩盖：

| 证据链 | 来源 | 核心叙述 | 时间锚点 |
|---|---|---|---|
| **链 A（队列积压）** | `v4.0/09-a2a-binding` §3.1 | 群消息进 `channel_ingress_events` 表状态 `pending`；9/16 那条 `attempts=2471` 一直未消费；根因「@_user_1 占位符缺 `<at user_id=...>` 标签 + sender 不在 `groupAllowFrom` 白名单」 | 积压记录 9/16；事故表征 9/21 |
| **链 B（长连接抖动）** | `volume-06/附录A` §4 | 「6 个飞书账号长连接 disconnected」；根因「飞书 WebSocket 偶发抖动 + gateway 健康探针有 1-3 分钟滞后」；修复 ≈7 分钟自动自愈 | 9/21 14:46 |

### 合并时间线

| 时点 | 事件 |
|---|---|
| **T-5天 · 09-16** | 群消息进入 `channel_ingress_events`，该条记录 `attempts=2471` 且**一直未被消费**（链 A 的发病起点） |
| **T+0 · 09-21 14:46** | 丘总/群内报告：飞书群消息 @ Agent **无响应**（整改单触发时间） |
| **T+2min** | 检查发现：消息确实进了 `channel_ingress_events`，状态 `pending`，`attempts` 高得反常 |
| **T+3min** | 检查飞书账号：**6 个账号长连接 disconnected**（hetu / kunpeng / mingjing / peter / tiangong / tianshu） |
| **T+4min** | 定位链 A 根因：`@_user_1` 占位符缺 `<at user_id=...>` 标签 + sender 不在 `groupAllowFrom` 白名单 |
| **T+5min** | 定位链 B 根因：飞书 WebSocket 抖动；`gateway` 健康探针有 **1-3 分钟滞后**，导致探针「看到健康」而实际已断 |
| **T+7min · ≈14:53** | 自动自愈完成：17/18 飞书账号全部 `connected, works` |
| **T+当天** | 起草整改单 `2026-09-21-001`；提出「通道守门员（Channel Sentinel）」角色 |
| **T+9天 · 09-30** | 整改单截止时间（`截止时间：2026-09-30`） |

> **时间线诚实边界**：链 A 与链 B 的**因果关系未经单向确证**——它们可能是「同一抖动的两种观测，
> 也可能是两次独立事件被并记」。本卷**不强行合并根因**，而是并列呈现（见 §三）。⏳ 需 `openclaw channels status --probe --channel feishu` 现场复跑定位当前态。

---

## 三、根因分析（5 Whys）

### 链 A：队列积压（准入语义）

1. **为什么飞书群消息 @ Agent 无响应？**
   → 因为消息进了 `channel_ingress_events` 表后，状态一直是 `pending`，没有被消费成 Agent 的一次运行。

2. **为什么消息一直 `pending`？**
   → 因为该条记录 `attempts=2471`——重试了两千多次仍失败，说明不是「暂时性失败」，而是「每次都注定失败」。

3. **为什么每次都注定失败？**
   → 因为消息里的提及占位符 `@_user_1` **缺少 `<at user_id=...>` 标签**——OpenClaw 无法解析出「这条消息到底 @ 了谁」，
   于是无法把消息投递给正确的 Agent。

4. **为什么 @ 解析不出目标还不报错、只闷头重试？**
   → 因为 **sender 不在 `groupAllowFrom` 白名单**——准入层先判「不合法」，
   但报错信息没有把「sender 不在白名单」这个根因显式说出来，只落成「无法消费 + 重试」。

5. **为什么准入语义没有被显式配置 / 显式探测？**
   → 因为 **`groupPolicy` / `groupAllowFrom` / `requireMention` 三件套存在语义空隙**：
   - `groupPolicy` **未设置时**会「放行不在白名单的群」（**这正是 PR #152777 的标题**）；
   - `requireMention` 决定「群里是否必须 @ 才触发」——设错会让「该响的不响」或「不该响的乱响」；
   - 三者组合起来是一个**没有默认安全值、也没有探针**的语义三角。

### 链 B：长连接抖动

1. **为什么 6 个飞书账号断连？**
   → 飞书 WebSocket **偶发抖动**（上游侧）。

2. **为什么抖动没被及时发现并快速重连？**
   → **`gateway` 健康探针有 1-3 分钟滞后**——探针的检测周期比抖动窗口长，
   于是「探针说健康」和「实际已断」可以同时为真。

3. **为什么没有自愈机制？**
   → 通道自愈机制**未配置**——断了之后没有「5 分钟超时自动重连」的守护。

4. **为什么没有自愈 / 没有守门员？**
   → 因为通道层被默认当成「永远在线」，没有角色对「通道是否真活着」负责。

5. **为什么通道没有负责人？**
   → 因为治理层的人设里**没有「通道守门员」这个岗**——A2A/协同层假设「网络和通道永远在线」，
   没有一个 Agent 的职责栏里写着「每 5 分钟探测通道并自愈」。

### → 根本原因

> **根本原因 = 「通道准入语义」与「通道活性」两个缺口叠加：**
> 1. **语义缺口**：`groupPolicy` / `groupAllowFrom` / `requireMention` 三件套缺乏默认安全值、缺乏显式配置规范、
>    缺乏根因提示——配错不出声，出事只闷头重试（`attempts=2471` 无人发现）。
> 2. **活性缺口**：没有通道守门员、没有自愈超时、没有积压告警——通道断了 1-3 分钟无人知，
>    积压到 2471 次无人告警。
>
> **一句话根因**：飞书「看起来坏了」的表象背后，是**准入语义没配清楚 + 通道活性没人管**。
> 26 条 `groupPolicy` 语义命中 + 本机实测配置（`groupPolicy: "open"` / account 级 `groupAllowFrom`）
> 说明了这个三角**真实存在且已被错误配置**。

---

## 四、当时的错误决策

### 错误决策 1：把 `attempts=2471` 当成「会自己好的重试」

**记 2471 次重试无人升级**——如果任一环节有「积压 > 阈值即告警」，这个事故会早 5 天被发现
（发病起点 09-16，表征 09-21）。

- **错在哪**：默认「重试次数高 = 网络抖动，会自愈」。
- **代价**：积压 5 天无人知，故障从「一条消息投不出去」膨胀成「整条通道看起来坏了」。

### 错误决策 2：以为「探针健康」就万事大吉

`gateway` 探针有 1-3 分钟滞后，但运维判断依赖探针。

- **错在哪**：混淆「探针采样时刻的健康」与「通道此刻的健康」。1-3 分钟的盲区足够让一次抖动滑过去。
- **代价**：断连 1-3 分钟内无告警。

### 错误决策 3：没有把「通道」当成一个有主人的资产

通道层长期无守门员、无自愈、无积压看板。

- **错在哪**：默认「基础设施自己会好」，不给它配负责人和巡检节奏。
- **代价**：事故靠「用户反馈」才被发现（而不是靠监控）。

### 错误决策 4（认知层）：把「两条证据链」当成「一条」

复盘时存在把「队列积压」与「长连接抖动」混为一谈的倾向。

- **错在哪**：急于给出单一根因，牺牲了证据完整性。
- **代价**：若只修其一，另一条仍会复发。本卷的处理方式是**并列呈现、分别对策**。

---

## 五、修复过程

> 以下修复同时覆盖两条链。

### 链 A · 准入语义修复

```bash
# 1) 看飞书通道现状（真名命令）
openclaw channels status --probe --channel feishu
# 期望（修复后）：全部账号 connected / works

# 2) 看本机飞书通道配置（真名路径：~/.openclaw/openclaw.json → channels.feishu）
openclaw config get channels.feishu
# 本卷实测该配置的关键结构（2026-09-27 实读）：
#   channels.feishu.enabled            = true
#   channels.feishu.defaultAccount     = "kunlun"
#   channels.feishu.requireMention     = true|false   ← 顶层默认
#   channels.feishu.groupPolicy        = "open"       ← 顶层群策略
#   channels.feishu.accounts.<id>      = { appId, appSecret, allowFrom, groupAllowFrom }
# 关键实测：本机飞书账号数为 18（kunlun/mingjing/…/tiance 各一）
#           kunlun 账号 groupAllowFrom = ["ou_806836b3f282704f08771d3873b98f8a"]
```

**本机按账号的准入配置示意（真实结构）**：

```yaml
channels:
  feishu:
    enabled: true
    defaultAccount: kunlun
    requireMention: true          # 顶层默认：群里必须 @ 才触发
    groupPolicy: open             # 顶层群策略
    accounts:
      kunlun:
        appId: cli_a975a1a3b3399bed
        allowFrom:      ["ou_806836b3f282704f08771d3873b98f8a"]   # DM 白名单
        groupAllowFrom: ["ou_806836b3f282704f08771d3873b98f8a"]   # 群消息白名单 ← 事故关键字段
```

**修复要点**：

1. 明确 `groupAllowFrom`：把「允许在群里唤起 Agent 的 sender」显式列入白名单。
2. 明确 `groupPolicy`：不依赖「未设置」的默认行为（未设置会放行 unlisted groups —— 见 CASE-5 / PR #152777）。
3. 明确 `requireMention`：群里必须 @ 才触发（避免误响应），但要保证「@ 了必须能解析出目标」。
4. 修 `@_user_1` 占位符解析：确保 `<at user_id=...>` 标签完整。

### 链 B · 通道活性修复

```bash
# 探针（守门员每 5min 跑这条）
openclaw channels status --probe --channel feishu

# 自愈规则：
#   - 5 分钟内自愈 → 不需重启
#   - > 5 分钟未恢复 → 触发 gateway restart
```

### 守门员（Channel Sentinel）机制

```yaml
角色: peter
名称: Channel Sentinel（通道守门员）
节奏: 每 5min 探测
动作:
  - 跑 channels status --probe --channel feishu
  - 检测 groupPolicy / groupAllowFrom 是否为空或异常 → 根因提示
  - 检测 channel_ingress_events.attempts > 阈值 → 告警
  - 5min 自愈窗口；超时 → gateway restart
```

> **本卷实测诚实边界**：peter 的「Channel Sentinel 正式任命」在 `v4.0/09-a2a-binding` §6.5 中仍标
> **⏳ 待丘总确认**。即：**角色已设计，正式任命未确认**。

---

## 六、修复后验证

### 验收标准（整改单原文）

- [x] 17/18 飞书账号全部 `connected, works`
- [x] 自愈率 ≥ 80%

### 复跑验证命令

```bash
# 1) 通道探针（核心验证）
openclaw channels status --probe --channel feishu
# 期望：18 个飞书账号全部 connected / works

# 2) 通道配置自检（确认三件套已显式配置）
openclaw config get channels.feishu.requireMention   # 期望：true（或明确的 false）
openclaw config get channels.feishu.groupPolicy      # 期望：明确的策略值（如 open / allowlist）
# 逐账号确认 groupAllowFrom 非空
jq -r '.channels.feishu.accounts | to_entries[] | "\(.key)\t\(.value.groupAllowFrom // "❌EMPTY")"' \
  ~/.openclaw/openclaw.json
# 期望：每个账号 groupAllowFrom 都是非空数组（事故根因：白名单语义缺口）

# 3) 积压队列检查（链 A 关键）
# ⏳ 精确 SQL 需按本机 state DB 结构确认；语义为：
#    SELECT status, count(*), max(attempts) FROM channel_ingress_events GROUP BY status;
# 期望：pending 为 0 / 极低；max(attempts) 不再出现四位数
# 真名依据（本机源码实测）：channel_ingress_events → openclaw-state-db-*.mjs / ingress-queue-health-*.mjs

# 4) gateway 活性
openclaw health
# 期望：gateway live
```

> **真名提醒**：
> - `channel_ingress_events` → 本机源码命中（`openclaw-state-db-*.mjs` / `ingress-queue-health-*.mjs` / `ingress-queue-*.mjs`）
> - `groupPolicy` → 本机源码命中 **913 处**（说明这是高频、核心的配置面，不是边角字段）

---

## 七、沉淀的机制

9/21 事故直接催生了 **反脆弱三层的第二层「通道守门员」+ 第三层「协同事件日志」**：

| 缺口（事故暴露） | 对策（沉淀机制） | 对应层 |
|---|---|---|
| 没有通道守门员 | 任命 peter 为 **Channel Sentinel**，每 5min 探测 | 第二层 |
| 没有自愈超时检测 | 5min 自愈窗口 + 超时 `gateway restart` | 第二层 |
| 没有 `channel_ingress_events` 积压告警 | `attempts > 阈值` → 告警（`attempts=2471` 不再无人发现） | 第二层 |
| 没有白名单根因提示 | 探针检 `groupPolicy` / `groupAllowFrom` → 根因提示 | 第二层 |
| 协同过程无日志 | 结构化协同事件日志（让失败模式在 Agent 间传递） | 第三层 |

### 与 PR #152777 的同源关系

```
PR #152777 title: "unset groupPolicy admits unlisted groups"
  ↓
问题：groupPolicy 未设置时，会「放行不在白名单的群」
  ↓
与 9/21 事故根因同源：
  - 9/21：sender 不在 groupAllowFrom 白名单 → 消息 pending 积压（attempts=2471）
  - #152777：groupPolicy 未设置 → 放行 unlisted groups
  ↓
两者都指向「飞书准入的白名单语义」
```

> **业界对位（差异化价值）**：LangGraph / AutoGen / CrewAI / Claude Agent SDK / OpenAI Agents SDK /
> LlamaIndex / A2A v1.0 —— **全部**假设「网络和模型永远在线」，因此**不会**内置「通道积压告警 / 自愈重启」。
> 这正是本接口层的差异化价值（详见 CASE-5 的业界对位表）。

---

## 八、如果你的系统遇到同样问题

### 8.1 立即止血 checklist

- [ ] `openclaw channels status --probe --channel feishu` —— 看账号是否全 `connected`
- [ ] 查 `channel_ingress_events` 的 `pending` 数量与 `max(attempts)`
- [ ] 若 `attempts` 异常高 → 立刻查 **sender 是否在 `groupAllowFrom` 白名单**
- [ ] 检查 `@_user_1` 类提及占位符是否**缺 `<at user_id=...>` 标签**
- [ ] 把合法 sender 显式加入 `groupAllowFrom`
- [ ] 显式设置 `groupPolicy`（**千万不要留空**）
- [ ] 显式设置 `requireMention`（群里要不要 @ 才触发）
- [ ] > 5min 未恢复 → `gateway restart`

### 8.2 根治 checklist（一周内）

- [ ] 部署 **Channel Sentinel**：每 5min 探测 + 5min 自愈窗口
- [ ] 加**积压告警**：`attempts > 阈值` 即告警（阈值建议个位数，别等 2471）
- [ ] 加**白名单自检**：`groupAllowFrom` 为空即告警
- [ ] 缩短探针周期：把 1-3 分钟滞后降到 < 30s
- [ ] 给「通道」这个资产配**明确的主人**（守门员角色）
- [ ] 每周跑一次 `channels status --probe` 作为例行体检

### 8.3 三件套速查（配置语义）

| 字段 | 作用 | 设错的后果 |
|---|---|---|
| `requireMention` | 群里是否必须 @ 才触发 | 设 `false` → 群里所有消息都触发（噪音）；设 `true` 但 @ 解析失败 → 该响的不响 |
| `groupPolicy` | 群准入策略 | **未设置 → 放行 unlisted groups（PR #152777）** |
| `groupAllowFrom` | 群消息 sender 白名单 | 空/漏配 → 合法消息被判不合法，闷头 `pending`（`attempts=2471`） |
| `allowFrom` | DM 白名单 | 空 → DM 被丢弃 |

> **CASE-2 一句话收口**：飞书「看起来坏了」的真相，是**准入语义三件套没配清楚** + **通道没有守门员**。
> `attempts=2471` 是这个事故的墓碑——它本可以在 `attempts=5` 时就被拦下。

---

## 附录 A · 本机飞书配置全景（实测）

> 来源：本卷实读 `~/.openclaw/openclaw.json`（45,662 字节）的 `channels.feishu` 段。

| 字段 | 本机实测值 | 说明 |
|---|---|---|
| `channels.feishu.enabled` | `true` | 飞书通道启用 |
| `channels.feishu.defaultAccount` | `kunlun` | 默认账号 |
| `channels.feishu.requireMention` | `true`（顶层） | 群里必须 @ 才触发 |
| `channels.feishu.groupPolicy` | `open`（顶层） | 顶层群准入策略 |
| `channels.feishu.streaming` | 存在 | 流式回复 |
| `channels.feishu.accounts` | **18 个账号** | kunlun / mingjing / tianshu / tiangong / xuanyuan / fenghuang / kunpeng / jixia / zhulong / siku / qilin / hetu / peter / fengniao / mobai / zhuque / baxia / tiance |

**单个账号的真实结构**（以 kunlun 为例，实读）：

```json
{
  "appId": "cli_a975a1a3b3399bed",
  "appSecret": "***(已打码)",
  "allowFrom":      ["ou_806836b3f282704f08771d3873b98f8a"],
  "groupAllowFrom": ["ou_806836b3f282704f08771d3873b98f8a"]
}
```

> **关键观察**：飞书的准入白名单在**账号级**（`accounts.<id>.groupAllowFrom`），
> 而不是 Telegram 那种**群级**（`accounts.<id>.groups.<gid>.requireMention`）。
> 这个**语义差异**正是「配了 Telegram 却漏了飞书」的常见原因。

### Telegram 侧的对照（同一份 openclaw.json）

```json
{
  "telegram": {
    "enabled": true,
    "defaultAccount": "kunlun",
    "dmPolicy": "allowlist",
    "accounts": {
      "kunlun": {
        "botToken": "8603081308:***",
        "allowFrom": ["8328029665"],
        "groups": {
          "-1003897043576": { "requireMention": false, "groupPolicy": "open" },
          "-1003396805662": { "requireMention": false },
          "-1003850475213": { "requireMention": false, "groupPolicy": "open" }
        }
      },
      "mingjing": {
        "groups": {
          "*": { "requireMention": true, "groupPolicy": "open" },
          "-1003897043576": { "requireMention": true, "groupPolicy": "open" }
        }
      }
      /* …其余 16 个账号同构… */
    }
  }
}
```

| 对比项 | Telegram | Feishu |
|---|---|---|
| 白名单层级 | 群级（`groups.<gid>`） | **账号级（`groupAllowFrom`）** |
| `requireMention` | 群级字段 | 顶层 + 账号级 |
| 通配群 | `"*"` 支持 | 需显式 `groupPolicy` |
| 本机账号数 | 18（+ default） | 18 |

> **读法**：同一次配置动作，两个通道的**层级不同**——
> 「照 Telegram 的样子配飞书」必然漏项。**这是 CASE-2 的配置陷阱根因。**

---

## 附录 B · `groupPolicy` / `requireMention` / `groupAllowFrom` 语义表

| 字段 | 层级 | 作用 | 设为空的后果 | 设错的后果 |
|---|---|---|---|---|
| `requireMention` | 通道顶层 / 群级 | 群里是否必须 @ 才触发 | 取默认（可能 `false`） | `false` → 群里所有消息都触发（噪音刷屏）；`true` 但 @ 解析失败 → 该响的不响 |
| `groupPolicy` | 通道顶层 / 群级 | 群准入策略（`open` / `allowlist` …） | **放行 unlisted groups（PR #152777）** | 策略与白名单不一致 → 该进的进不来 / 不该进的进来了 |
| `groupAllowFrom` | **账号级**（Feishu） | 群消息 sender 白名单 | **消息被判不合法，闷头 `pending`（`attempts=2471`）** | 漏配 sender → 合法用户无法唤起 Agent |
| `allowFrom` | 账号级 | DM 白名单 | DM 被丢弃 | 漏配 → 私聊无法唤起 |

> **真名依据（本机源码实测）**：`groupPolicy` → 本机源码命中 **913 处**；
> `channel_ingress_events` → `openclaw-state-db-*.mjs` / `ingress-queue-health-*.mjs` / `ingress-queue-*.mjs`。

---

## 附录 C · 读者自测（8 题）

1. **`attempts=2471` 说明什么？**
   参考答案：不是「暂时性失败」，而是「每次都注定失败」——根因在准入（白名单 / 提及解析），不在网络。

2. **为什么 `groupPolicy` 留空是危险的？**
   参考答案：未设置时会「放行不在白名单的群」（PR #152777 的标题即此）。

3. **Feishu 的白名单在哪个层级？Telegram 呢？**
   参考答案：Feishu 在**账号级**（`groupAllowFrom`）；Telegram 在**群级**（`groups.<gid>`）。

4. **为什么「探针健康」还可能实际已断？**
   参考答案：`gateway` 探针有 1-3 分钟滞后——采样时刻健康 ≠ 此刻健康。

5. **本次事故的两条证据链是什么？为什么不能强行合并根因？**
   参考答案：队列积压（`attempts=2471` + 白名单）vs 长连接抖动（6 账号 disconnected）；合并会牺牲证据完整性，若只修其一另一条会复发。

6. **Channel Sentinel 的探测节奏与自愈窗口是多少？**
   参考答案：peter 每 **5min** 探测；**5min 自愈窗口**，超时触发 `gateway restart`。

7. **为什么业界框架不会帮你防这个？**
   参考答案：6 大框架 + A2A v1.0 全部假设「通道永远在线」，不内置通道积压告警 / 自愈。

8. **如果飞书群里 @ 了 Agent 却没反应，你的前三条命令是什么？**
   参考答案：
   `openclaw channels status --probe --channel feishu` →
   查 `channel_ingress_events` 的 `pending` / `max(attempts)` →
   查 sender 是否在 `groupAllowFrom`。

---

## 附录 D · 与其它案例的交叉引用

| 关联案例 | 关系 |
|---|---|
| **CASE-1**（8/19 军团断线） | 同属反脆弱三层；本案例对应**第二层（通道守门员）** |
| **CASE-5**（PR #152777） | **同源**——都指向「飞书 groupPolicy / 白名单语义」 |
| **CASE-9**（心跳熔断） | 均为「provider/通道单点共享」类故障；解法同构（隔离 + 告警 + 熔断） |
| **CASE-10**（插件取舍） | `Feishu/Lark` 插件是通道命脉（enabled）；通道能力依赖插件状态 |

---

## 附录 E · 不适用边界（诚实）

- **因果未单向确证**：链 A（队列积压）与链 B（长连接抖动）的**因果关系未经实拉单证**；
  本案例**并列呈现**，不强行合并。⏳ 需现场复跑定位当前态。
- **精确 SQL 未实拉**：`channel_ingress_events` 的查询语句为语义描述，未按本机 state DB 结构实测。
- **角色未正式任命**：peter 的 Channel Sentinel 任命在 v4.0 §6.5 标 **⏳ 待丘总确认**（设计已出，任命未定）。
- **不覆盖**：飞书 WebSocket 抖动属上游（飞书侧），本案例不追其服务端根因。

---

# CASE-3 · 18 坏 skill 修复：8 P0 stub + frontmatter 缺失批量治理

## 一、案例速览

| 项 | 内容 |
|---|---|
| 时间 | 2026-08-25 → 2026-08-30（P0 stub 失约期）；现状复核 2026-09-27 |
| 影响面 | **skills 全库**：238 目录（236 + INDEX + 1）中 47 个 SKILL.md 无 frontmatter、55 个 name 违例 |
| 根因类型 | **流程缺口（「自决 ≠ 执行」协议断裂）+ 规范缺失（frontmatter 未强制）** |
| 修复耗时 | 分批（8-30 首战落盘 4 个 P0 stub 中的部分；批量治理延续） |
| 沉淀产物 | `auto-execute-signoffs` 桥接机制 + SKILL.md frontmatter 规范 + skills Workshop |
| 优先级 | **P0**（连续 4~7 天 deadline 失约） |
| 责任 Agent | 主责 tiance（天策）；协同 kunlun |
| 关键基因 | `GENE-20260827-004` → `GENE-20260830-001`（自决协议失灵升级版） |

> **一句话**：这是「**建议 vs 动作**」的经典翻车——**熔炉每天写「明日自决创建 skill」，但
> `skill_manage` 工具从未被调用**。root cause 不是「忘了」，而是「自决文字层」与「工具执行层」之间
> **没有桥**。

---

## 二、事件时间线

| 时点 | 事件 | 证据 |
|---|---|---|
| **T-44天 · 08-14 15:11** | `skill-candidates/` 最后一次更新（`candidates-2026-08-14.md`，925 字节）——候选池从此冻结 | audit §C |
| **T-43天 · 08-15 11:20** | `skill-candidates-processed/` 最后 2 个文件后无新增 | audit §C |
| **T-41天 · 08-17 08:16** | `skills/INDEX.md` 最后 reindex（223 skill 索引），此后停更 | audit §C |
| **T-5天 · 08-25** | `~/.hermes/skills/` 新增 `autonomous-ai-agents/`——**这是最后一次新增 skill** | 08-30 熔炉 §57-59 |
| **T-4天 · 08-26** | 5 个 P0 skill stub 提议；evolution brief sign-off，**零执行** | 08-30 熔炉 §57 |
| **T-3天 · 08-27** | sign-off 但零执行；`GENE-20260827-004` 记录「自决 deadline 失约」 | 同上 |
| **T-2天 · 08-28** | sign-off 但零执行；`~/.hermes/skills/` 仍无新增 | 同上 |
| **T-1天 · 08-29** | sign-off 但零执行；**连续第 4 天 deadline 失约** | 同上 |
| **T+0 · 08-30 06:30** | morning-brief 跑通，但 `skill_manage(action='create')` **在 cron 进程内未自动执行**；`GENE-20260830-001` 升级为「自决协议失灵升级版」 | 08-30 熔炉 §57-70 |
| **T+0 · 08-30 06:30** | recall：`skill_manage` 需要 `description < 60 字符` 的 **pre-flight 校验**（前次失败过），未意识到要截断 → pre-flight 失败 | 08-30 熔炉 §67 |
| **T+0 当天** | 首战落盘 4 个 P0 skill stub 中的部分（含 `launchd-truth-check`）；回滚 fallback 用 `cp -r templates/skill-stub/` | 08-30 熔炉 §73-74, 137-151 |
| **T+28天 · 09-27** | 本卷实测复核：`~/.openclaw/workspace/skills/` = **236 顶目录**（+INDEX+1 = 238）；其中 **221 个含 SKILL.md**；**27 个顶目录级 SKILL.md 无 frontmatter**；去重后全库 **47 无 frontmatter / 55 name 违例** | 本卷实测 |

> **时间线诚实边界**：
> - 「连续 4 天失约」+「8-30 首战落盘」来自 `nightly-forge/tiance/2026-08-30.md` 原文（实读）。
> - 「47 无 frontmatter / 55 name 违例」来自**本机 2026-09-27 实测口径**（任务基线），
>   本卷独立复算「顶目录级 SKILL.md 无 frontmatter = 27」，两者口径不同（27 = 顶目录级；
>   47 = 全库递归含嵌套 skill），不矛盾，但**已标注口径差异**。

---

## 三、根因分析（5 Whys）

1. **为什么 5 个 P0 skill stub 连续 4 天「自决」却没落盘？**
   → 因为自决只发生在**文字层**（evolution brief 写「明日创建」），`skill_manage(action='create')`
   在 cron 进程内从未被调用。

2. **为什么文字层自决没有触达工具层？**
   → 因为 **evolution brief / 熔炉的"自决"协议和"执行"协议之间缺少桥接**：
   没有 `auto-execute-signoffs` 之类的机制把「sign off A 方案」自动转成「调用工具执行 A 方案」。

3. **为什么 morning-brief cron 跑通了，却什么都没创建？**
   → 因为 cron 任务的 prompt 里**没有「执行昨日 sign-off」的逻辑**——
   cron 只会「报告」，不会「执行昨天说要执行的事」。

4. **为什么即便试图执行，还会 pre-flight 失败？**
   → 因为 `skill_manage` 有硬校验：`description < 60 字符`。
   失败的根因是「没意识到要截断 description」——**规范存在，但没被写进 SOP 的前置检查清单**。

5. **为什么这类「坏 skill」会累积到 238 目录里 47 个无 frontmatter / 55 个 name 违例？**
   → 因为 **frontmatter / name 规范没有被强制**：
   skill 是「复制粘贴 + 手改」长出来的，没有注册时的 frontmatter lint，
   也没有批量治理的例行任务——于是历史债静默累积。

### → 根本原因

> **根本原因 = 两层：**
> 1. **协议层**：「自决（文字）」与「执行（工具）」之间没有桥——`GENE-20260830-001` 的准确表述是
>    **「自决 ≠ 执行」**：不是 agent 忘了，而是**协议设计里根本没把 sign-off 接到 `skill_manage` 调用上**。
> 2. **规范层**：SKILL.md 的 frontmatter / name 规则**没有前置校验与批量治理**，
>    导致 47 个无 frontmatter + 55 个 name 违例在库里静默累积。
>
> **一句话根因**：**「建议」被当成「动作」交付了**——写下来 = 完成了，这就是坏 skill 长出来的土壤。

---

## 四、当时的错误决策

### 错误决策 1：把「写进熔炉」当成「完成」

连续 4 天在熔炉里写「明日自决创建 skill」，每天都标「已完成 sign-off」——
但 sign-off 只是**文字动作**，不是**工具动作**。

- **错在哪**：验收时看的是「今天有没有写」，而不是「产物 mtime 有没有变」。
- **代价**：5 个 P0 skill 延期 5 天。

### 错误决策 2：把「cron 跑通」当成「任务完成」

morning-brief cron 每天 06:30 跑通（日志 ✅），但产出是「报告」不是「执行」。

- **错在哪**：`触发成功` 被误当 `交付成功`（这正是 audit 里记录的通病，见 CASE-4）。
- **代价**：日志天天绿，skill 天天不落地。

### 错误决策 3：pre-flight 校验失败后没有前置清单

`skill_manage` 的 `description < 60 字符` 校验**前次已经失败过**，但没有把这条写进「调用前 checklist」。

- **错在哪**：从错误中学习没有制度化——错一次就该写进 SOP，而不是靠记性。
- **代价**：同一个 pre-flight 坑反复踩。

### 错误决策 4（治理层）：没有 frontmatter lint

238 个 skill 里 47 个无 frontmatter / 55 个 name 违例，长期无人批量治理。

- **错在哪**：默认「skill 能加载就行」，不校验结构性规范。
- **代价**：skill 生态的「可发现性 / 可复用性」被历史债稀释。

---

## 五、修复过程

### 5.1 P0 stub 落盘（08-30 首战）

```bash
# 正道：真正调 skill_manage（工具层），而不是只写进熔炉（文字层）
# 天策侧的落地顺序（08-30 熔炉 §137-151）：
#   #1 launchd-truth-check        P0（连续 7 天）
#   #2 auto-execute-signoffs      P0（新增，GENE-001 衍生）
#   #3 nightly-forge-events-bridge P0（GENE-002 衍生）
#   #4（+ #5）
```

**回滚 / 兜底路径（当 skill_manage 因 pre-flight 失败时）**：

```bash
# 若 skill_manage 因 description 超 60 字符失败，用文件系统兜底：
mkdir -p ~/.hermes/skills/<skill-name>
cp -r templates/skill-stub/SKILL.md ~/.hermes/skills/<skill-name>/SKILL.md
# 说明：这是"应急桥"，治本是修 pre-flight（截断 description 到 <60）
```

> ⚠ **真名提醒**：天策（tiance）是 **OpenClaw 第 18 Agent**，其 skill 落盘路径为 `~/.hermes/skills/`
> （Hermes 侧），与 OpenClaw 的 `~/.openclaw/workspace/skills/`（238 目录）**是两个不同的库**。
> 本案例横跨两库，务必区分。

### 5.2 桥接机制：`auto-execute-signoffs`

```yaml
名称: auto-execute-signoffs
优先级: P0
作用: 桥接「自决文字层」→「工具调用层」
规则: 如果 sign off A 方案且未在 X 小时内被反对 → 自动执行 A 方案
```

### 5.3 批量治理：frontmatter / name 规范

**有效的 SKILL.md frontmatter（真名规范）**：

```markdown
---
name: <skill-name>            # 小写 + 连字符/下划线，≤64 字符
description: <Use when ...>.  # 触发条件必须在最前 57 字符内自含
---

# <Skill Title>

## 何时使用
## 步骤
## 陷阱
## 验证
```

**批量 lint（本卷给出的可复跑检查脚本）**：

```bash
cd ~/.openclaw/workspace/skills

# 1) 统计总数
ls -d */ 2>/dev/null | wc -l            # 本卷实测：236（+INDEX+1 = 238 → 任务基线）

# 2) 找无 SKILL.md 的目录（含分类目录）
for d in */; do [ -f "$d/SKILL.md" ] || echo "NO-SKILL.md: $d"; done
# 本卷实测：15 个（均为分类目录：ai-infra/ architecture/ automation/ …）

# 3) 找 SKILL.md 无 frontmatter（首 3 字节不是 ---）
for f in */SKILL.md; do [ -f "$f" ] || continue; \
  [ "$(head -c 3 "$f")" = "---" ] || echo "NO-FRONTMATTER: $f"; done | wc -l
# 本卷实测（顶目录级）：27   ← 任务基线「47」为全库递归口径

# 4) 找 name 违例（大小写 / 空格 / 超长）
# 规则：name 必须小写、连字符/下划线、≤64 字符
grep -l "^name: " */SKILL.md 2>/dev/null | while read f; do
  n=$(grep -m1 "^name: " "$f" | sed 's/^name: *//')
  echo "$n" | grep -Eq '^[a-z0-9_-]{1,64}$' || echo "NAME-BAD: $f -> $n"
done | wc -l
# 期望：0（任务基线「55 name 违例」为治理前口径，修复后应显著下降）
```

---

## 六、修复后验证

```bash
# 1) 天策 P0 stub 是否真正落盘（工具层，不是文字层）
ls -d ~/.hermes/skills/launchd-truth-check/ 2>/dev/null && echo "✅ 落盘"
ls -d ~/.hermes/skills/auto-execute-signoffs/ 2>/dev/null && echo "✅ 落盘"
ls -d ~/.hermes/skills/nightly-forge-events-bridge/ 2>/dev/null && echo "✅ 落盘"
# 期望：目录存在且含 SKILL.md（不是空目录、不是只有 md 文字）

# 2) pre-flight 通过性（description < 60 字符）
# 反复用同一条 create 调用验证 pre-flight 不再失败

# 3) frontmatter / name 全库复检（见 §5.3 脚本）
# 期望：NO-FRONTMATTER 计数下降；NAME-BAD = 0

# 4) skills INDEX 是否恢复 reindex
ls -l ~/.openclaw/workspace/skills/INDEX.md
# 事故态：mtime 停在 08-17 08:16（停 41 天，223 skill 索引）
# 期望：mtime 近期更新
```

> **验收标准**：
> - [ ] 5 个 P0 skill stub 全部落盘（含 `SKILL.md` + frontmatter）
> - [ ] `auto-execute-signoffs` 桥接机制上线
> - [ ] 全库 frontmatter 缺失清零 / 显著下降
> - [ ] name 违例清零
> - [ ] `skills/INDEX.md` 恢复 reindex

---

## 七、沉淀的机制

| 缺口 | 沉淀机制 | 落地形态 |
|---|---|---|
| 自决 ≠ 执行 | **`auto-execute-signoffs` 桥接** | skill（P0） |
| 「触发成功」被当「交付成功」 | **产物 mtime 验收** | SOP 规则 |
| pre-flight 反复失败 | **调用前 checklist**（description < 60 字符） | SOP |
| frontmatter 缺失累积 | **SKILL.md frontmatter 规范 + 批量 lint** | 规范 + 脚本 |
| name 违例 | **name 命名规则（小写+连字符+≤64）** | 规范 |
| 候选池冻结 | **work-to-skill 审批闭环修复**（人工闸门问题，见 CASE-4） | 治理 |

### 与 Work-to-Skill 链路的关系

```
候选池 (skill-candidates/)  → 审核 (APPROVE)  → 封装  → 索引 (INDEX.md)
      ↑ 停在 08-14              ↑ 停在 08-15     ↑        ↑ 停在 08-17
   ← 提取段（熔炉）活着，后三段因「人工闸门」冻结（见 CASE-4 §五.5）
```

---

## 八、如果你的系统遇到同样问题

### 8.1 立即止血 checklist

- [ ] 统计 skill 总数：`ls -d */ | wc -l`
- [ ] 找出无 SKILL.md 的目录（区分「分类目录」与「坏 skill」）
- [ ] 找出 SKILL.md 无 frontmatter 的（`head -c 3 != ---`）
- [ ] 找出 name 违例（非小写 / 含空格 / 超 64 字符）
- [ ] 把「已 sign-off 但未落盘」的 skill 用 `skill_manage` **真正创建**（不是写进 md）
- [ ] 若工具调用失败，用 `cp -r templates/skill-stub/` 兜底

### 8.2 根治 checklist（一周内）

- [ ] 上 `auto-execute-signoffs`：sign-off 未反对 N 小时后自动执行
- [ ] 把「description < 60 字符 / 小写 name / ≤64 字符」写进调用前 checklist
- [ ] 加 skill 注册时的 **frontmatter lint**（不通过不给注册）
- [ ] 加**月度批量治理**任务（扫全库 frontmatter / name）
- [ ] 验收口径从「今天写了没」改成「**产物 mtime 变了没**」

### 8.3 反模式速查

| 反模式 | 为什么会踩 | 怎么避免 |
|---|---|---|
| 自决只写在文字层 | 「写下来就算完成」 | sign-off 必须接工具调用 |
| cron 跑通 = 任务完成 | 只看日志 ✅ | 看产物 mtime |
| pre-flight 失败不写进 SOP | 靠记性 | 错一次写一次 |
| skill 只加不 lint | 「能加载就行」 | 注册时 lint |
| 顶目录 = 全库 | 口径混淆 | 明确「顶目录级 / 全库递归」两种口径 |

> **CASE-3 一句话收口**：坏 skill 不是「写坏的」，是**「没被执行出来的自决」+「从没被校验的规范」**长出来的。
> 治本不在批量修文件，而在**给「建议」和「动作」之间架桥**。

---

## 附录 A · 真实基因记录（GENE 编号原文）

> 来源：`~/.openclaw/workspace/knowledge/ops/nightly-forge/tiance/2026-08-30.md`（实读）。

```
GENE-20260827-004：自决 deadline 失约（初版）
  → 5 个 P0 skill stub 提议后连续 sign-off 但零执行

GENE-20260830-001：自决协议失灵（升级版）
  原文："自决协议失灵升级版——5 个 P0 skill stub 连续 4 天 deadline 失约
        （8-25 提议 → 8-26/27/28/29/30 全部 sign-off 但零执行）。
        根因不在'忘了'，而在'自决 ≠ 执行'的协议缺口——
        evolution brief / 熔炉的'自决'是文字层，未桥接到 skill_manage 工具调用层。
        需要创建一个 auto-execute-signoffs skill 或修改 evolution brief 模板，
        加'如果 sign off A 方案且未在 X 小时内被反对则自动执行'。"

GENE-20260830-003：gateway PID 漂移非单调
  原文："前 4 天显示加速趋势（72h→48h→24h→5h），但 8-29 18:36 → 8-30 01:04 = ~6h 后 3939，
        模式回归到 24h 级别。修正 GENE-20260827-003：漂移不是稳定加速，
        而是'高频重启 + 偶发长间隔'的混合模式。"
```

### 当时 4 条根因（熔炉原文）

```
1. evolution brief 的 sign-off 协议只在文字层，未触达 skill_manage 工具
   —— 名义"自决"实际"建议"
2. 6:30 morning-brief cron 跑通了，但 skill_manage(action='create') 在 cron 进程内未自动执行
   （cron 没有「执行昨日 sign-off」逻辑）
3. pre-flight 失败：skill_manage 需要 description < 60 字符（前次失败过），
   没意识到要截断
根本问题：天策的"自决"协议和"执行"协议之间缺少桥接 skill
   —— 这是 GENE-004 真正的根因，不是"忘了"。
```

### P0 skill 建议清单（熔炉原文表）

| # | 建议 skill | 优先级 | 当前状态 | 行动建议 |
|--:|---|---|---|---|
| 1 | `launchd-truth-check` | **P0** | 🚨 连续 7 天 | 8-30 06:30 必须**真正 `skill_manage create`** |
| 2 | `auto-execute-signoffs` | **P0（新增）** | 🆕 GENE-001 衍生 | 桥接自决文字 → 工具调用 |
| 3 | `nightly-forge-events-bridge` | **P0** | 🚨 GENE-002 衍生 | 立即 |

> **熔炉当日铁令（原文摘录）**：
> 「8-30 06:30 morning-brief 第一件事：调 `skill_manage(action='create', ...)` 创建 #1+#3+#4+#5 四个 stub
> （**不要等 sign-off 协议**）」；
> 「**不再写"明日自决"**——今晚熔炉直接验证 stub 是否落盘，落盘即完成」。

---

## 附录 B · SKILL.md frontmatter 规范（真名）

```markdown
---
name: <skill-name>            # 小写 + 连字符/下划线；≤64 字符
description: <trigger>. <behavior>.   # 触发条件必须在前 57 字符内自含
---

# <Skill Title>

## 何时使用（触发条件）
## 步骤（编号，含精确命令）
## 陷阱（Pitfalls）
## 验证（Verification）
```

| 字段 | 规则 | 违反后果 |
|---|---|---|
| `name` | 小写字母 / 数字 / 连字符 / 下划线；≤64 字符 | 加载失败 / 索引重复 |
| `description` | **≤60 字符**（`skill_manage` pre-flight 硬校验） | **创建被拒**（本案例的坑） |
| frontmatter | 文件首 3 字节必须是 `---` | 解析失败 / 不被识别为 skill |

> **本卷实测现状**（`~/.openclaw/workspace/skills/`）：
> - 顶目录：**236**（+INDEX+1 = 238）
> - 含 SKILL.md：**221**
> - 无 SKILL.md 的 15 个：`ai-infra/ architecture/ automation/ commercialization/ data-driven/ engineering/ geo/ growth/ infrastructure/ listening/ market-data/ methodology/ testing/ tools/ user-research/`（**均为分类目录，非坏 skill**）
> - 顶目录级无 frontmatter：**27**（任务基线「47」为全库递归口径）

---

## 附录 C · 读者自测（8 题）

1. **「自决 ≠ 执行」的准确含义是什么？**
   参考答案：不是 agent 忘了，而是**协议设计里没有把 sign-off 接到 `skill_manage` 调用上**——文字层与工具层之间缺桥。

2. **为什么凌晨 06:30 的 morning-brief 跑通了却什么都没创建？**
   参考答案：cron 任务 prompt 里没有「执行昨日 sign-off」的逻辑——它会「报告」，不会「执行昨天说要执行的事」。

3. **`skill_manage` 的 pre-flight 硬校验是什么？本案例因何失败？**
   参考答案：`description < 60 字符`；本案例因「没意识到要截断 description」而 pre-flight 失败。

4. **当 `skill_manage` 因 pre-flight 失败时，兜底路径是什么？**
   参考答案：`mkdir -p ~/.hermes/skills/<name> && cp -r templates/skill-stub/SKILL.md ~/.hermes/skills/<name>/SKILL.md`。

5. **天策的 skill 路径与 OpenClaw 的 skill 路径分别是什么？为什么必须区分？**
   参考答案：天策 = `~/.hermes/skills/`（Hermes 侧）；OpenClaw = `~/.openclaw/workspace/skills/`（238 目录）。**是两个库**。

6. **「47 无 frontmatter」与「本卷实测 27」为什么不矛盾？**
   参考答案：27 = 顶目录级口径；47 = 全库递归（含嵌套 skill）口径。**口径不同，并列标注**。

7. **为什么「cron 跑通」不能作为验收标准？**
   参考答案：`触发成功 ≠ 交付成功`——验收要看**产物 mtime**。

8. **如果你要上 `auto-execute-signoffs`，它的核心规则是什么？**
   参考答案：「如果 sign off A 方案且未在 X 小时内被反对 → 自动执行 A 方案」。

---

## 附录 D · 与其它案例的交叉引用

| 关联案例 | 关系 |
|---|---|
| **CASE-4**（能力矩阵空转） | 同根——都是「制度/建议写在文字层，未落到执行层」 |
| **CASE-7**（编排节奏） | skill-collection-review ×18 是 CASE-7 的节奏构件；本案例是其产物侧的故障 |
| **CASE-1**（8/19 断线） | 熔炉记录同源（`nightly-forge/tiance` 系列）；同属 8 月事故集群 |
| **CASE-10**（插件取舍） | skills 与 plugins 是两个能力面；本案例在 skills 面，CASE-10 在 plugins 面 |

### 8 月事故/失约集群时间线（跨案例）

```
08-14  skill-candidates 冻结（44 天）
08-17  skills/INDEX.md 停更（41 天）
08-19  军团断线（CASE-1）
08-25  5 个 P0 skill stub 提议
08-26~29  sign-off 但零执行（连续 4 天）
08-30  GENE-20260830-001 升级为「自决协议失灵」
```

---

## 附录 E · 不适用边界（诚实）

- **P0 stub 数量口径**：任务基线为「8 P0 stub」；熔炉 08-30 原文为「**5 个** P0 skill stub」。
  本案例**并列两个数字**，以熔炉原文（5 个）为直接证据，任务基线（8 个）为更大范围口径。
- **落盘完整性未实拉**：`~/.hermes/skills/` 下 `launchd-truth-check` 等 stub 的**最终落盘状态**本次未逐个 `ls` 验证。
- **frontmatter / name 违例为口径值**：见 §附录 B 说明，非单一精确数。
- **不覆盖**：`skill_manage` 的完整 pre-flight 规则集（仅确认 `description < 60 字符` 这一条）。

---

# CASE-4 · 能力矩阵 26 天未续期：治理机制空转诊断

## 一、案例速览

| 项 | 内容 |
|---|---|
| 时间 | 2026-09-01（最后一次成功续期）→ 2026-09-27（诊断日）；**26 天未续期** |
| 影响面 | **治理层**（能力矩阵 / 军功簿 / 信誉分）；连带进化链路 |
| 根因类型 | **制度落地缺口（「写在 md，未落到调度层」）+ 无自动触发** |
| 修复耗时 | 诊断 ≈1 次盘点（167 行审计报告）；修复待建 |
| 沉淀产物 | audit 报告 + `evidence-tuple` auto-renew 机制设计 + 整改单样本 |
| 优先级 | P1（能力矩阵）/ 更严重：军功簿 **144 天零结算** |
| 责任 Agent | 主责 kunlun（能力矩阵 cron owner）；诊断 tiance |
| 关键 cron | `ebb72ae6…能力矩阵月度更新`（`30 0 1 * *`，**error 4x**，last 27 天前） |

> **一句话**：这是「**制度写在 md，但结算器从未被注册**」的标本——
> `merit-board.md` 原文写着「每周一 00:00 由 cron 自动结算」，现实是 crontab / LaunchAgents / hermes cron
> **三处零军功 job**，`ledger.md` 账目停在 2026-05-06。

---

## 二、事件时间线

| 时点 | 事件 | 证据 |
|---|---|---|
| **T-144天 · 2026-05-06** | 军功簿 `ledger.md` **最后一条账目**；此后零结算 | audit §D |
| **T-144天 · 2026-05-07** | `merit-board.md` / `monthly-ranking.md` / `rules.md` mtime 停在此日 | audit §D |
| **T-118天** | `merit-board.md` 数据冻结在 **Week 22（2026-05-26~06-01）** | audit §D/E |
| **T-13天 · 09-13** | `merit-board.md` **头部**自称「当前军功排名 [更新 2026-09-13]」 | audit §E.2 |
| **T-13天 · 09-14 09:01** | `merit-board.md` 被 **touch**（mtime 变新），但**尾部数据仍停在 Week 22** | audit §D/E.2 |
| **T-0(触发) · 09-27** | 晨报 cron `a2d4eb3d4399`（军团今日计划汇总）发现「最近活跃日志」仍为旧版 → 触发能力矩阵续期诊断 | v2026.9 卷八 §2.2 #10 |
| **T+0 · 09-27 23:35** | 天策侧完成 167 行审计盘点：实拉 crontab + LaunchAgents + launchctl + hermes cron + 文件 mtime + NAS SSH | audit 头部 |
| **T+0 · 09-27** | 本卷实测复核：`能力矩阵月度更新` cron（`ebb72ae6…`）schedule `30 0 1 * *`，**last 27 天前，status error (4x)** | 本卷实测 `openclaw automations list` |
| **T+0 · 09-27** | 最后一次成功续期文件：`2026-09-01-能力矩阵月度更新.md`（2,497 字节，45 行） | 本卷实读 |

### 关键诊断：「僵尸复燃」假象

```
merit-board.md  mtime = 09-14 09:01   ← 看起来"新"
               尾部内容 = Week 22 (2026-05-26 ~ 06-01)   ← 实际数据断在 6/1
               头部自称 = "[更新 2026-09-13]"
               ⇒ 文件头尾自相矛盾 = 被 touch 过但数据未更新
```

> **时间线诚实边界**：「26 天」的口径有两种——
> (a) 从 **2026-09-01 最后成功续期** 到 **2026-09-27 诊断日** = 26 天（本案例口径，与调研报告一致）；
> (b) 本卷实测 `automations list` 显示 `last 27d ago`（含 edge 计数）。
> 两者不矛盾，**26 天为业务口径**，27 为 CLI 显示口径。

---

## 三、根因分析（5 Whys）

1. **为什么能力矩阵 26 天没续期？**
   → 因为负责它的 cron（`ebb72ae6…能力矩阵月度更新`，`30 0 1 * *`）**连续失败 4 次（error 4x）**，
   最近一次运行在 27 天前——failing 但没被修。

2. **为什么 cron 失败没人管？**
   → 因为**没有「连续失败自动开单」机制**。cron 红了，但红色只躺在 `automations list` 里，
   没有任何人/任何机制把它升级成整改单。

3. **为什么「月度更新」会连续 4 次失败？**
   → 因为月度 cron 运行频率极低（每月 1 次），**失败后要等下一个月才有下一次运行**——
   4 次失败 = 4 个月的静默积累；低频率掩盖了持续失败。

4. **为什么没有把它改成更合理的频率（如周度）？**
   → 因为**制度设计与工程实现脱节**：卷八附录提出「周度 cron 能力矩阵进化评估」，
   但实际注册的仍是月度任务，且带 error——**设计稿是周度，运行体是月度且坏的**。

5. **为什么「制度」和「运行体」会脱节到无人发现？**
   → 因为**制度是被「写进 md」完成交付的**：`merit-board.md` 写着「每周一 00:00 cron 自动结算」，
   `rules.md` 规则完整——**文档层看不出任何破绽**。但没有 `plist` / `job` 产物，
   验收时**没有可观测的执行体**，于是从未有人发现它没跑。
   **军功簿更极端：crontab 3 条 / LaunchAgents 19 个 / hermes cron 15 个，零军功 job，
   `ledger.md` 停 2026-05-07，144 天零结算。**

### → 根本原因

> **根本原因 = 「制度落地缺口」：**
> **制度存在于文档层，从未落到调度层**——「有规则、有账本，但结算器从未被注册」。
> 机制：制度是被「写进 md」完成交付的；没有 `plist` / `job` 产物 = 验收时没有可观测的执行体；
> 加上 cron 失败无自动开单、月度频率放大静默期——于是**机制空转，且空转到无人发现**。
>
> **一句话根因**：**「声明的自动化」和「实际的调度注册」是两回事**——
> 文档里写着自动，调度表里零注册，中间的鸿沟没有任何探针。

---

## 四、当时的错误决策

### 错误决策 1：把「写进 md」当成「已自动化」

`merit-board.md` 原文：「计算周期：每周一 00:00 由 cron 自动结算」。
现实：三处调度（crontab/launchd/hermes cron）**零军功 job**。

- **错在哪**：文档声明被当成系统事实。
- **代价**：144 天零结算，且无人察觉。

### 错误决策 2：用「touch 文件」假装机制在跑

`merit-board.md` 被 touch 到 09-14，头部还改写成「[更新 2026-09-13]」——
但**尾部数据仍停在 Week 22**。

- **错在哪**：让 mtime 变新 = 让「看起来在跑」= 制造僵尸复燃假象。
- **代价**：任何「看 mtime 判断活性」的检查都被骗过。

### 错误决策 3：cron 连续失败不升级

`能力矩阵月度更新` error 4x，从没开过整改单。

- **错在哪**：默认「红了会自己好」。
- **代价**：26 天静默。

### 错误决策 4：用低频率任务掩盖持续失败

月度 cron 失败后要等 30 天才有下一次运行——**失败感知周期 = 运行周期**。

- **错在哪**：没意识到「频率越低，失败越难被发现」。
- **代价**：4 次失败 = 4 个月的静默。

---

## 五、修复过程

### 5.1 诊断（先取证，再判断）

```bash
# 1) cron/automation 真状态（真名命令）
openclaw automations list 2>&1 | grep -iE "能力矩阵|error"
# 本卷实测输出：
# ebb72ae6-…  能力矩阵月度更新  cron 30 0 1 * * @ Asia/Shanghai  in 3d  27d ago  error (4x)  ...

# 2) 三处调度注册表交叉核对（真名）
crontab -l 2>/dev/null | grep -iE "merit|军功|能力"
# 期望：本机 crontab 3 条（早报/监工报/熔炉进化报），无军功
launchctl list 2>/dev/null | grep -iE "merit|军功"
# 期望：19 个非 Apple plist 中无军功结算
# hermes cron（15 job）
hermes cron list 2>/dev/null | grep -iE "merit|军功|能力"
# 事故态：仅 1 次命中，且是"另一个 job 的 prompt 里读取军功账本（如果有）"

# 3) 制品 mtime 取证（判断"看起来在跑"还是"真在跑"）
ls -l ~/.openclaw/workspace/knowledge/ops/military-merit/ledger.md
# 事故态：mtime = 2026-05-07
ls -l ~/.openclaw/workspace/agents/workspace-kunlun/memory/merit-board.md
# 事故态：mtime = 09-14（看着新），但 tail 看内容是 Week 22
tail -20 ~/.openclaw/workspace/agents/workspace-kunlun/memory/merit-board.md
# 期望（修复后）：尾部为当前周数据，不是 Week 22
```

### 5.2 修复方向一 · 修 cron 频率（月度 → 周度）

```yaml
# 卷八附录 A.2.1 提出的周度任务（设计稿）
name: 能力矩阵进化评估
schedule: 每周一 09:00        # 原月度 cron 30 0 1 * *（error 4x）应被修掉/替换
```

### 5.3 修复方向二 · 加 evidence-tuple 强制 auto-renew

v2026.9 卷八提出的机制：**落 `evidence-tuple` 强制每周 auto-renew**，
即「制度必须产出可观测证据（新产物 / 前后 Diff / 测试日志）才算跑过」。

```
证据元组（evidence-tuple）：
  - 新产物   ：memory/YYYY-MM-DD-能力矩阵月度更新.md（mtime 必须是本周）
  - 前后 Diff：与上期能力矩阵的 diff
  - 测试日志 ：cron 执行输出（不能只有"跑了"）
```

### 5.4 修复方向三 · 自动开单

| 触发器 | 阈值 | 自动动作 |
|---|---|---|
| cron 连续失败 | `consecutiveErrors ≥ 3` | 立即开整改单 |
| 制品 mtime 超期 | > 2× 计划周期 | 告警 |
| 能力矩阵续期 | 每周自动 | auto-renew |

---

## 六、修复后验证

```bash
# 1) cron 状态归零
openclaw automations list 2>&1 | grep "能力矩阵"
# 事故态：error (4x)
# 期望：ok

# 2) 制品 mtime 是本周
ls -l ~/.openclaw/workspace/agents/workspace-kunlun/memory/*能力矩阵*
# 期望：最新一期 mtime 在 7 天内

# 3) 军功簿结算器已注册（关键！）
crontab -l 2>/dev/null | grep -iE "merit|军功" ; \
launchctl list 2>/dev/null | grep -iE "merit|军功" ; \
hermes cron list 2>/dev/null | grep -iE "merit|军功"
# 事故态：三处零命中
# 期望：至少一处有军功结算 job

# 4) 账本最新条目是本周
tail -5 ~/.openclaw/workspace/knowledge/ops/military-merit/ledger.md
# 事故态：最后一条 = 2026-05-06（144 天前）
# 期望：最后一条在 7 天内
```

> **验收标准**：
> - [ ] `能力矩阵月度更新` cron status = `ok`
> - [ ] 能力矩阵最新一期 mtime ≤ 7 天
> - [ ] 军功结算器在 crontab/launchd/hermes cron 至少一处注册
> - [ ] `ledger.md` 最后条目 ≤ 7 天

---

## 七、沉淀的机制

| 缺口 | 沉淀机制 |
|---|---|
| 「写进 md」= 「已自动化」 | **evidence-tuple 强制 auto-renew**（制度必须有可观测证据） |
| mtime 造假 / 僵尸复燃 | **验收口径改为「内容 + mtime」双验**，不看 mtime 单指标 |
| cron 连续失败不升级 | **`consecutiveErrors ≥ 3` 自动开整改单** |
| 低频任务掩盖失败 | **关键任务频率上限约束**（如能力矩阵改周度） |
| 制度与运行体脱节 | **「声明 vs 现实」定期交叉审计**（本案例的 audit 即范式） |

### 「声明 vs 现实」审计范式（可复用）

本案例产出的审计报告结构值得沉淀为**通用治理体检模板**：

```
A. cron 注册事实表（crontab + LaunchAgents + hermes cron）
B. 制品存在事实表（路径 + mtime + 大小 + 内容首行 + 状态）
C. 进化制品事实表
D. 军功簿制品事实表
E. 荒废信号诊断（声明 vs 现实）
F. 最可能的 3 个根因
```

---

## 八、如果你的系统遇到同样问题

### 8.1 立即止血 checklist

- [ ] 列出所有「声明了自动化」的制度（grep md 里的「cron 自动」「自动结算」）
- [ ] 逐一核对：它是否在 crontab / launchd / hermes cron **真的注册**了
- [ ] 对每个制品看 **mtime + 内容尾部**（防僵尸复燃）
- [ ] 把 `error` 状态的 cron 全部揪出来
- [ ] 对连续失败 ≥3 的 cron 立即开整改单

### 8.2 根治 checklist（一周内）

- [ ] 关键任务全上 **evidence-tuple**：新产物 + 前后 Diff + 测试日志
- [ ] 加 **cron 失败自动开单**（`consecutiveErrors ≥ 3`）
- [ ] 把**低频 + 关键**的任务改成周度（失败感知周期 ≤ 7 天）
- [ ] 加**「声明 vs 现实」月度交叉审计**
- [ ] 验收口径：**从「跑了吗」改成「产物 mtime + 内容双验」**

### 8.3 反模式速查

| 反模式 | 为什么会踩 | 怎么避免 |
|---|---|---|
| 写进 md = 已自动化 | 文档比调度表好写 | 验收看调度注册 |
| touch 文件装活 | 想让检查通过 | 双验 mtime + 内容 |
| 红了会自己好 | 不想被低价值告警打扰 | 连续失败阈值自动开单 |
| 月度 = 省事 | 降低运行开销 | 关键任务频率上限 |
| 看 mtime 判活性 | 单指标省事 | mtime + 内容双验 |

> **CASE-4 一句话收口**：**「声明了自动」和「注册了调度」之间有一条鸿沟**。
> 能力矩阵 26 天、军功簿 144 天没人发现，不是因为没人检查，而是因为**文档层永远看起来是对的**。

---

## 附录 A · 审计现场证据（实拉原文摘录）

> 来源：`audit-2026-09-27-daily-evolution-merit-dormancy.md`（167 行，实读全文）。

### A1 · cron 注册事实表（三处交叉）

| 调度面 | 数量 | 军功 job | 结论 |
|---|---|---|---|
| crontab（本机） | **3** | 0 | 早报 / 监工报 / 熔炉进化报——**全部「跑但空转」** |
| LaunchAgents（非 Apple） | **19** | 0 | 含 `com.tiance.morning.brief` / `com.kunlun.true-pulse` / `ai.openclaw.gateway` … |
| Hermes cron | **15** | 0 | 全部 owner = 天策；军功/信誉分 = **0 个**；进化相关 = **2 个** |

**Hermes cron 15 个 job 全表（实拉）**：

| job_id | 名称 | schedule | last run | 状态 |
|---|---|---|---|---|
| 0381a524d5c4 | 天策·暗夜熔炉·进化复盘 | `0 1 * * *` | 09-27 01:01 | ✅ |
| 930e2aa2bc0b | 天策·进化结果与计划建议 | `0 6 * * *` | 09-27 06:00 | ✅ |
| a2d4eb3d4399 | 天策·军团今日计划汇总 | `0 7 * * *` | 09-27 07:01 | ✅ |
| 84d3b369e9c8 | 天策·日报总结 | `30 18 * * *` | 09-27 18:31 | ✅ |
| ea8320b637ca | NAS早报缺失扫描 | `0 8 * * *` | 09-27 08:02 | ✅ |
| 87a43729f40b | NAS公司脉搏生成 | `0 9 * * *` | 09-27 09:02 | ✅ |
| b2aa790efe44 | NAS系统状态日志 | `0 18 * * *` | 09-27 18:00 | ✅ |
| 3cc9b41b39b8 | NAS晚间脉搏推送 | `0 18 * * *` | 09-27 18:01 | ✅ |
| 2d46c182c32e | NAS文件命名校验 | `0 10 * * 1` | — | ✅ |
| 04c9f041879c | L2市场部agent周报 | `0 9 * * 1` | — | ✅ |
| 25343db8afa6 | L2 HR日报 | `0 7 * * *` | 09-27 07:00 | ✅ |
| a17ee2b08dc1 | L2技术部健康日报 | `30 7 * * *` | 09-27 07:31 | ✅ |
| 54892b984b4a | 鲲界员工早间简报 | `0 8 * * *` | 09-27 08:04 | ✅ |
| f04ce9f5c129 | 鲲界日报缺失提醒 | `0 17 * * *` | 09-27 17:02 | ✅ |
| df932435e824 | NAS过渡期看门狗 | `*/30 * * * *` | 09-27 23:31 | ✅ |

> **读法**：15 个 job **全部 active**——这正是「空转」的可怕之处：
> **调度层全绿，但账本数据 144 天没动。**

### A2 · 军功簿制品事实表（DORMANT）

| 路径 | 最近 mtime | 状态 | 证据 |
|---|---|---|---|
| `knowledge/ops/military-merit/ledger.md` | **2026-05-07** | DORMANT | 最后账目 = 2026-05-06；停 **144 天** |
| `knowledge/ops/military-merit/monthly-ranking.md` | 2026-05-07 | DORMANT | 只有 2026-05 一个月；16 agent 中 11 人「待活动」 |
| `knowledge/ops/military-merit/rules.md` | 2026-05-07 | ⚠️ 仅规则 | 加分/扣分/等级规则完整，**无执行记录** |
| `agents/workspace-kunlun/memory/merit-board.md` | **09-14 09:01** | 僵尸 | 文件被 touch，**数据冻结在 Week 22（05-26~06-01）**；停更 **118 天** |
| `.blueblood` / `.honor` / `.merit` | — | ❌ 不存在 | 全盘无命中 |
| 军功结算 cron / launchd | — | ❌ **零注册** | 15 job + 19 plist + 3 crontab 均无 |

### A3 · 进化链路制品事实表

| 路径 | 最近 mtime | 状态 | 证据 |
|---|---|---|---|
| `nightly-forge/tiance/` | 09-27 01:01 | **ACTIVE** | 72 文件，9/8→9/27 逐日（缺 9/24） |
| `tiance/evolution-brief/` | **09-09 06:01** | DORMANT | 仅 2 文件，停 18 天 |
| `tiance/skill-candidates/` | **08-14 15:11** | DORMANT | 1 个 candidate，停 44 天 |
| `tiance/skill-candidates-processed/` | **08-15 11:20** | DORMANT | 2 文件后无新增，停 43 天 |
| `skills/INDEX.md` | **08-17 08:16** | DORMANT | 223 skill 索引，停 41 天 |
| `nightly-forge/{其余17个agent}/` | 2026-05-07 | **EMPTY** | 17 个目录，**0 文件** |
| `work_to_skill` 审批闭环 | 09-27 23:00 | ⚠️ **卡住** | `candidates 总数: 2 / 已APPROVE: 0 / 未审核: 1` |

### A4 · 09-24 批量失败风暴（已恢复）

| 项 | 值 |
|---|---|
| `executions.db` | `completed 425 / failed 49 / unknown 1` |
| failed 时间窗 | **2026-09-24 06:30~09:00** |
| 统一错误 | `RuntimeError: Request timed out.` |
| 涉及 job | `df932435e824` / `87a43729f40b` / `54892b984b4a` / `ea8320b637ca` / `25343db8afa6` / `a2d4eb3d4399` / `a17ee2b08dc1` |
| 性质 | **单点网络/模型超时窗口，之后自愈，非结构性荒废** |
| 暴露 | **cron 无失败重试兜底** |

---

## 附录 B · 「声明 vs 现实」审计模板（可复用）

本案例最有价值的产物不是「修了什么」，而是**这套审计范式**：

```markdown
# 盘点：<领域> 运行状态与荒废断点
> 盘点时间：YYYY-MM-DD HH:MM · 方法：实拉 crontab + LaunchAgents + launchctl + hermes cron + 文件 mtime + NAS SSH
> 证据等级：全部来自本次实拉输出（mtime / tail / ls）。无推测。

## A. cron 注册事实表
### A1. crontab
### A2. LaunchAgents
### A3. Hermes cron 注册表
## B. 制品存在事实表
## C. 进化制品事实表
## D. 军功簿制品事实表
## E. 荒废信号诊断（声明 vs 现实）
## F. 最可能的 3 个根因
```

### 三条根因机制（审计原文）

```
1. 军功簿：制度存在于文档层，从未落到调度层（"只写规则，不注册结算器"）。
   机制：制度是被"写进 md"完成交付的，没有 plist/job 产物
        = 验收时没有可观测的执行体，于是从未有人发现它没跑。

2. 日报：数据源未接入，cron 照跑不误 → 空转被误当"已闭环"。
   机制："触发成功"被当成"交付成功"——日志有 ✅、Telegram 有推送，
        验收就过了，没人核对产物 mtime。

3. 进化：提取段（熔炉）活着，审核→封装→索引 三段因"人工闸门"冻结。
   机制：设计上留了「丘总人工把 `- [ ] APPROVE` 改成 `- [x]`」这一步，
        这一步是唯一无人值守会永久停摆的环节，而候选池只有 2 条
        → 44 天无人触碰，链路死锁。
```

---

## 附录 C · 能力矩阵单次成功样本（2026-09-01 实读）

> 来源：`~/.openclaw/workspace/agents/workspace-kunlun/memory/2026-09-01-能力矩阵月度更新.md`（45 行）。

**制度（原文）**：成功调用 +5% / 优秀 +10% / 失败 -15% / 失败后找对方法 +3%；
连续 3 次成功 → 升级 A；连续 3 次失败 → 降级 D。

**当月评估输入（原文表节选）**：

| Agent | 月度调用 | 成功 | 失败 | 修复 | 优秀 | 净趋势 |
|---|---|---|---|---|---|---|
| 昆仑 | 31（cron 互审/失败成本/早报/本 cron） | 31 | 0 | 0 | 18 | +9% |
| 天策 | 14（8-13~8-31 熔炉） | 14 | 0 | 14 | 6 | +10% |
| 轩辕 | 1（8-19 断线修复验证 ping） | 1 | 1 | 1 | 1 | -12% |
| 蜂鸟 | 1（8-19 ping） | 1 | 1 | 1 | 0 | -12% |
| 河图 | 1（8-19 ping） | 1 | 1 | 1 | 0 | -12% |
| 明镜/稷下/天枢/烛龙/司库/… | 0 | 0 | 0 | 0 | 0 | 0% |

**升级判定（原文）**：昆仑（连续 30+ 次 cron 成功）→ **升 A**；天策（连续 14 次熔炉落盘）→ **升 A**；
轩辕/蜂鸟/河图（1 失败 → 1 修复）→ 不升不降；其余样本不足。

> **对照价值**：这一份是**成功样本**（有产物、有数据、有判定）——
> 而 09-01 之后 **26 天再无下一份**。**成功样本 + 断更 = 机制空转的完整证据链。**

---

## 附录 D · 读者自测（8 题）

1. **「军功簿 144 天零结算」的证据是什么？**
   参考答案：`ledger.md` mtime = 2026-05-07，最后账目 = 2026-05-06；且 crontab(3) + launchd(19) + hermes cron(15) **三处零军功 job**。

2. **什么是「僵尸复燃」假象？**
   参考答案：`merit-board.md` 被 touch 到 09-14、头部写「[更新 2026-09-13]」，但尾部数据仍停在 Week 22——**mtime 变新但数据没动**。

3. **为什么「15 个 cron 全 active」反而是危险信号？**
   参考答案：调度层全绿会让人以为「在跑」，但产物 mtime 可以 144 天不动——**调度活性 ≠ 业务活性**。

4. **「触发成功被当成交付成功」会导致什么？**
   参考答案：日志有 ✅、Telegram 有推送，验收就过了；没人核对产物 mtime → 空转被当闭环。

5. **进化链路「四段」里哪三段断了？**
   参考答案：提取（熔炉）活着；**审核 → 封装 → 索引**三段断（skill-candidates 停 08-14 / processed 停 08-15 / INDEX 停 08-17）。

6. **09-24 的 49 条 failed 说明什么？**
   参考答案：单点网络/模型超时窗口，之后自愈，**非结构性荒废**；但暴露 **cron 无失败重试兜底**。

7. **本案例提出的核心机制是什么？**
   参考答案：**evidence-tuple 强制 auto-renew**——制度必须产出可观测证据（新产物 / 前后 Diff / 测试日志）。

8. **你会用什么口径做「声明 vs 现实」审计？**
   参考答案：三处调度交叉（crontab + launchd + hermes cron）× 制品 mtime × 内容尾部——**三验，不看单指标**。

---

## 附录 E · 与其它案例的交叉引用

| 关联案例 | 关系 |
|---|---|
| **CASE-3**（坏 skill） | 同根——「写在文字层 ≠ 落到执行层」；CASE-3 是 skill 面，本案例是治理面 |
| **CASE-7**（编排节奏） | 本案例的 15 个 hermes cron 是 CASE-7 编排面的一部分；空转是节奏的隐性故障 |
| **CASE-9**（心跳熔断） | 均属「无人看的失败」——cron error 4x 与 heartbeat 99+x 同为「静默失败」 |
| **CASE-1**（8/19 断线） | 8/19 后 15 个 cron 进入错误退避；能力矩阵 cron 的 error(4x) 与之同源 |

---

## 附录 F · 不适用边界（诚实）

- **「26 天」口径**：业务口径 = 09-01 → 09-27；CLI 实测显示 `last 27d ago`。**两口径并列**。
- **NAS 相关**：`nas_daily_digest.py` 等 13 个孤儿脚本属 NAS 侧（另一条线），本案例仅引用，不展开。
- **整改单目录未实拉**：`decisions/整改单/` 的落盘状态本次未 `ls`。
- **不覆盖**：为什么 cron 失败会「连续 4 次」而不是「连续 1 次」——月度频率的必然结果（已在 §三.3 解释）。
- **可复现性**：本案例的审计脚本依赖本机路径；迁移到其它系统需替换路径。

---

# CASE-5 · PR #152777 卡住：上游依赖阻塞的决策路径

## 一、案例速览

| 项 | 内容 |
|---|---|
| 时间 | 2026-09-19 创建 → 至今 OPEN（2026-09-27 实测 age = 8 天） |
| 影响面 | **本机飞书 override 策略**（是否保留本地前置补丁）；与 CASE-2 同源 |
| 根因类型 | **上游依赖阻塞（外部 PR 未合并 → 本地决策悬空）** |
| 修复耗时 | 不适用（未闭合）；SOP 化后每周 1 次检查 |
| 沉淀产物 | 主仓覆盖评估 SOP + 每周检查 cron 建议 + 6 项覆盖评估清单 |
| 优先级 | 持续跟踪（OPEN < 14 天无需升级） |
| 关键教训 | **v2026.9 的「推测」被 v4.0「实拉」纠正**——上游状态必须实拉，不能推测 |

> **一句话**：这是一个「**上游未决 → 本地不敢动**」的典型决策悬空案例。
> 它的价值不在「怎么修 PR」，而在「**当依赖阻塞时，本地 override 该留还是该撤**」的决策框架。

---

## 二、事件时间线

| 时点 | 事件 | 证据 |
|---|---|---|
| **T-?** | v2026.9 版本对 PR #152777 **推测**为「A2A fallback 健康检查 + 通道守门员协议」 | v4.0 §2.2 |
| **T+0 · 2026-09-19 10:24:54Z** | PR #152777 **创建** | `gh api` 实拉 |
| **T+7天 · 2026-09-26 19:15:21Z** | PR 最近一次活动（updated）——**非僵尸 PR** | `gh api` 实拉 |
| **T+8天 · 2026-09-27** | v4.0 **独立实拉** `gh api repos/openclaw/openclaw/pulls/152777` | v4.0 §2.1 |
| **T+8天** | 铁证：`state=open` · `merged=null` · title = `fix(feishu): unset groupPolicy admits unlisted groups` | 同上 |
| **T+8天** | v4.0 **诚实修正**：v2026.9 的「推测」**判定为错误**——PR 真实存在，但**不是** A2A 相关，而是**飞书 groupPolicy 修复** | v4.0 §2.2 |
| **T+8天** | 关联确认：与 9/21 事故（sender 不在白名单）**同源** | v4.0 §2.3 |
| **T+8天** | 当前评估：`OPEN < 14 天，无需升级；继续每周检查` | v4.0 §6.4 |
| **T+14天（待触发）** | 若 OPEN 持续 > 14 天 → 升级给天策/丘总决策 | v4.0 §6.2 |

> **时间线诚实边界**：本案例的「事故」性质不是「系统崩了」，而是**「认知出错 + 决策悬空」**——
> 前一代（v2026.9）对一个上游 PR 做了**没有实拉的推测**，直到 v4.0 实拉才发现推测错误。

---

## 三、根因分析（5 Whys）

1. **为什么本地的飞书 override 策略悬而未决？**
   → 因为它依赖上游 PR #152777 是否合并——PR 未合并，本地不敢撤 override。

2. **为什么 PR #152777 长期 OPEN？**
   → 上游维护者尚未处理（创建 09-19，至 09-27 已 8 天；最近有活动但未合并）。

3. **为什么本地不能自己决定「撤不撤 override」？**
   → 因为**本地 override 与上游 fix 存在双向风险**：
   - 若 PR 已合并 + 本地还留 override → **可能重复 / 冲突**；
   - 若 PR 未合并 + 本地撤 override → **可能回归**（回到有 bug 的状态）。

4. **为什么会陷入「撤也不行、留也不行」的两难？**
   → 因为**缺少一套「主仓覆盖评估」的判定流程**——没有「何时该撤、何时该留、撤之前要跑什么」的清单。

5. **为什么之前的版本会误判这个 PR 的性质？**
   → 因为 **v2026.9 对上游状态做了「推测」而没有「实拉」**——
   在没有 `gh api` 证据的情况下，凭语义联想把 PR 猜成 A2A 相关，
   于是整个 override 决策建立在一个**错误的前提**上。

### → 根本原因

> **根本原因 = 两层：**
> 1. **上游依赖阻塞**：外部 PR 未合并，本地 override 的「保留 / 撤销」决策天然悬空。
> 2. **认知缺陷（更值得记）**：**对上游状态做推测而非实拉**——
>    v2026.9 把 PR #152777 猜成 A2A 相关，v4.0 实拉后发现是飞书 groupPolicy 修复。
>    **推测构建了错误的世界模型，错误的世界模型导致错误的决策路径。**
>
> **一句话根因**：**上游状态必须实拉，不能推测**；上游依赖阻塞时，
> 本地必须有「撤 / 留」的显式判定框架，否则 override 会永远悬空。

---

## 四、当时的错误决策

### 错误决策 1（最严重）：对上游 PR 做推测而非实拉

v2026.9 声称 PR #152777 是「A2A fallback 健康检查 + 通道守门员协议」。

- **错在哪**：**没有跑 `gh api`**，靠语义联想填空。
- **代价**：整个 A2A 接口层的叙事建立在一个错误前提上，被 v4.0 实拉推翻。

### 错误决策 2：只给「两种状态」，不给「第三种」

早期只考虑「PR 合并了」和「PR 没合并」，没考虑「**长期 OPEN 未合并**」这个最常见的第三状态。

- **错在哪**：决策树不完整。
- **代价**：遇到「长期 OPEN」时无 SOP 可依。

### 错误决策 3：override 的「保留依据」没写清

本地 override 是「不等主仓合并先跑通」的前置补丁，但**没有写明「为什么留、什么条件下撤」**。

- **错在哪**：补丁与「上游 fix」的对应关系未记录。
- **代价**：一旦上游合并，无人知道该怎么 diff、怎么撤。

### 错误决策 4：没有「每周检查」的自动化

检查 PR 状态这件事依赖人工记得。

- **错在哪**：依赖记性，不依赖 cron。
- **代价**：可能长期无人跟（直到 v4.0 才补上 SOP）。

---

## 五、修复过程（决策路径 + SOP）

### 5.1 铁证实拉（唯一可信来源）

```bash
gh api repos/openclaw/openclaw/pulls/152777 \
  --jq '{num:.number,state:.state,merged:.merged_at,title:.title,created:.created_at,updated:.updated_at}'
```

**实际返回（v4.0 原样记录）**：

```json
{
  "created": "2026-09-19T10:24:54Z",
  "merged": null,
  "num": 152777,
  "state": "open",
  "title": "fix(feishu): unset groupPolicy admits unlisted groups",
  "updated": "2026-09-26T19:15:21Z"
}
```

### 5.2 每周检查 SOP（建议 cron：kunlun 周一 09:00）

```bash
# 每周一次
gh pr view 152777 --repo openclaw/openclaw --json state,mergedAt,reviews,title
# 若 state=CLOSED 且 mergedAt 非空 → 触发「主仓覆盖评估」流程
# 若 state=OPEN 持续 >14 天 → 升级给天策/丘总决策
```

### 5.3 主仓覆盖评估清单（PR 合并后必跑）

| # | 检查项 | 命令 / 方法 | 处置 |
|--:|---|---|---|
| 1 | PR 是否合并 | `gh pr view 152777 --json mergedAt` | merged 非空 → 进入 2 |
| 2 | 本地 override 是否重复 | diff 本层 `groupPolicy` 探针 vs 主仓实现 | 重复 → 撤销 override |
| 3 | 本地 override 是否冲突 | 跑 9/21 复现脚本 | 冲突 → 保留 override + 上报 |
| 4 | 升级 9.6+ stable | `openclaw --version` | 验证 override 仍生效 |
| 5 | 反脆弱三层回归 | 跑 2 实例（模型级联 + 通道网络） | 任一失败 → 回滚 |
| 6 | 记录到 decisions/ | 写 `decisions/YYYY-MM-DD-主仓覆盖评估.md` | 归档 |

### 5.4 当前状态（2026-09-27）

```yaml
PR #152777:
  state: open
  merged: null
  age: 8 天（created 2026-09-19 → 2026-09-27）
  updated: 2026-09-26T19:15:21Z   # 最近有活动，非僵尸 PR
  评估: "OPEN < 14 天，无需升级；继续每周检查"
  与 9/21 事故: "同源（飞书 groupPolicy / 白名单语义）"
```

---

## 六、修复后验证

```bash
# 1) 实拉 PR 状态（唯一可信）
gh api repos/openclaw/openclaw/pulls/152777 --jq '{state,merged,title,updated}'
# 期望：state=open / merged=null / title 含 groupPolicy

# 2) 本地 override 是否仍在（飞书探针）
openclaw config get channels.feishu.groupPolicy
# 期望：明确的策略值（override 生效中）

# 3) 每周检查是否被 cron 化
openclaw automations list 2>&1 | grep -iE "152777|主仓|override"
# ⏳ 期望：存在每周检查 job（当前未确认注册）

# 4) 版本一致性
openclaw --version
# 若已升到 9.6+ 且 PR 仍 open → override 必须保留
```

> **验收标准（framework proposal P0 验收依赖）**：
> - [ ] 复现 8/19 级联（mock 坏端点 × 17 Agent）⏳
> - [ ] 复现 9/21 积压（`attempts > 阈值`）⏳
> - [ ] 协同事件日志连续写 7 天 ⏳
> - [ ] peter 正式任命为 Channel Sentinel ⏳ 待丘总确认
> - [ ] 至少 2 实例跑通 ⏳

---

## 七、沉淀的机制

| 缺口 | 沉淀机制 |
|---|---|
| 推测上游状态 | **「实拉优先」原则**——上游状态一律 `gh api` / `gh pr view`，禁止推测 |
| 决策树不完整 | **补齐三状态**：已合并 / 未合并 / **长期 OPEN** |
| override 无依据 | **主仓覆盖评估 6 项清单** |
| 无自动跟踪 | **每周检查 SOP + cron 建议** |
| 认知偏差 | **诚实修正机制**（v4.0 明确标注 v2026.9 推测为 ❌，并全卷以实拉为准） |

### 业界对位（本案例的差异化证据）

| 防护能力 | LangGraph | AutoGen | CrewAI | Claude SDK | OpenAI Agents | LlamaIndex | A2A v1.0 | **本层** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 端点级联防护 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ ⚡** |
| fallback 去重 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ ⚡** |
| 通道积压告警 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ ⚡** |
| 自愈 + 重启 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ ⚡** |
| 事故现场可追溯 | ⚠ | ⚠ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ ⚡** |

### override 与主仓 fix 的兼容性（⚠ 风险）

| 场景 | 处置 |
|---|---|
| PR #152777 合并 + 升 9.6+ stable | 所有本地 override **需重新评估**，可能重复/冲突，**可能回归** |
| 主仓 9.6+ stable 发布 | 必须先 **diff** 本层 override 与主仓实现，再决定撤销或保留 |
| PR 长期 OPEN 未合并 | 本地 override **必须保留**，每周与主仓 master 同步 |

---

## 八、如果你的系统遇到同样问题

### 8.1 立即止血 checklist

- [ ] `gh pr view <N> --repo <repo> --json state,mergedAt,title` —— **实拉，不推测**
- [ ] 判断三状态：已合并 / 未合并 / 长期 OPEN
- [ ] 列出所有「依赖该 PR 的本地 override」
- [ ] 对每个 override 写明「为什么留、什么条件撤」
- [ ] 若 PR 已合并 → 立即 diff 本地 override vs 主仓实现

### 8.2 根治 checklist（一周内）

- [ ] 建「上游依赖台账」：每个依赖项一行（PR 号 / 状态 / 本地 override / 撤留条件）
- [ ] 加**每周自动检查**（cron 建议：周一 09:00 跑 `gh pr view`）
- [ ] 加**升级阈值**：OPEN > 14 天自动升级给决策者
- [ ] 写**主仓覆盖评估 6 项清单**（见 §5.3）
- [ ] 建**诚实修正机制**：上一代的推测若被实拉推翻，必须显式标注「❌ 推测错误」

### 8.3 反模式速查

| 反模式 | 为什么会踩 | 怎么避免 |
|---|---|---|
| 推测上游状态 | 实拉要跑命令 | 实拉优先，禁止推测 |
| 只考虑两状态 | 没想到「长期 OPEN」 | 补齐三状态 |
| override 无撤留条件 | 补丁只为「先跑通」 | 写明撤留条件 |
| 依赖人工记得检查 | 依赖记性 | cron 化 |
| 上一代错误不回标 | 掩盖曾犯错 | 显式标注「推测错误」 |

> **CASE-5 一句话收口**：**PR #152777 的真相是飞书 groupPolicy 修复（同源于 9/21 事故），
> 不是 A2A 健康检查**——v4.0 以实拉为准，诚实修正 v2026.9 的推测。
> 而这次纠错本身，比 PR 的内容更有价值：**它证明了「上游状态必须实拉」这条规则值得写进案例库。**

---

## 附录 A · 两代推测对照表（诚实修正的完整记录）

| 版本 | 对 PR #152777 的说法 | 判定 |
|---|---|---|
| v1.0 | 未提 | — |
| v2026.9 | **推测**为「A2A fallback 健康检查 + 通道守门员协议」 | ❌ **推测错误** |
| **v4.0 实测** | `state=open` · `merged=null` · 标题 **`fix(feishu): unset groupPolicy admits unlisted groups`** | ✅ **以实拉为准** |

> **铁证结论**：PR #152777 **真实存在**，但**不是** A2A / 反脆弱三层相关，
> 而是**飞书 groupPolicy 修复**——**与 9/21 事故（sender 不在白名单）同源**。
> v4.0 全卷以此为准，**不得回退到 v2026.9 的推测**。

### 同源关系图

```text
PR #152777 title: "unset groupPolicy admits unlisted groups"
  ↓
问题：groupPolicy 未设置时，会「放行不在白名单的群」
  ↓
与 9/21 事故根因同源：
  - 9/21：sender 不在 groupAllowFrom 白名单 → 消息 pending 积压（attempts=2471）
  - #152777：groupPolicy 未设置 → 放行 unlisted groups
  ↓
两者都指向「飞书准入的白名单语义」
```

---

## 附录 B · 业界协议对位（实拉）

| 协议 | 仓库 | ⭐ | archived | 处理「端点坏 / 通道断」？ |
|---|---|---:|:--:|:--:|
| MCP | modelcontextprotocol/modelcontextprotocol | 9,317 | false | ❌ |
| A2A | a2aproject/A2A | **25,945** | false | ❌ |
| ACP | i-am-bee/acp | 1,016 | **true** | ❌ |
| ANP | agent-network-protocol/AgentNetworkProtocol | 1,435 | false | ❌ |
| Anthropic Skills | anthropics/skills | 178,604 | false | ❌ |

> **读法**：`A2A` 有 25,945 stars，但**不处理「端点坏 / 通道断」**；
> `ACP` 已 archived（注意：这与术语表 #1 的「ACP→SLCP 改名」呼应——
> 对外用 ACP 既商标冲突、又指向一个已归档的协议）。

### 与术语表 #1 的呼应

| 项 | 说明 |
|---|---|
| 术语表 #1 | **ACP**（丘总卷七自造概念）→ 改名 **SLCP**（Silicon-Life Coordination Protocol） |
| 改名原因 | IBM/BeeAI 的 ACP 已占用且 2025-08 已合并入 A2A；对外用 ACP = 商标冲突 |
| 本案例旁证 | 上表显示 `i-am-bee/acp` 仓库 **archived = true**——**更不该对外用 ACP 这个名字** |

---

## 附录 C · 决策记录的落地形态（decisions/）

本案例要求把「主仓覆盖评估」写入 `decisions/`。落盘模板：

```markdown
# 主仓覆盖评估 · YYYY-MM-DD

## 触发
- 上游 PR: openclaw/openclaw#152777
- 实拉状态: state=__ / merged=__ / updated=__
- 触发原因: merged 非空 / OPEN > 14 天

## 评估（6 项清单）
1. PR 是否合并: __
2. 本地 override 是否重复: __
3. 本地 override 是否冲突: __
4. 升级 9.6+ stable: __
5. 反脆弱三层回归: __
6. 记录归档: ✅

## 处置
- [ ] 撤销 override
- [ ] 保留 override + 上报
- [ ] 回滚

## 复盘
- 决策依据（实拉证据）: __
- 与上一代口径的差异: __
```

**落盘路径**：`~/.openclaw/agents/workspace-kunlun/memory/decisions/YYYY-MM-DD-主仓覆盖评估.md`

---

## 附录 D · 读者自测（8 题）

1. **PR #152777 的真实标题是什么？**
   参考答案：`fix(feishu): unset groupPolicy admits unlisted groups`。

2. **v2026.9 对它的推测错在哪？为什么错？**
   参考答案：推测为「A2A fallback 健康检查 + 通道守门员协议」；错因是**没跑 `gh api`**，靠语义联想填空。

3. **什么条件下应该撤销本地 override？**
   参考答案：上游已合并且 diff 后发现**重复**时 → 撤销 override。

4. **什么条件下必须保留本地 override？**
   参考答案：PR 长期 OPEN 未合并时（否则可能回归）；或 diff 后发现**冲突**时（保留 + 上报）。

5. **「OPEN > 14 天」触发什么动作？**
   参考答案：升级给天策/丘总决策。

6. **上游依赖有哪三种状态？为什么不能只考虑两种？**
   参考答案：已合并 / 未合并 / **长期 OPEN**。忽视第三种会在最常见的状态上无 SOP。

7. **为什么「诚实修正」本身就是一种机制？**
   参考答案：它防止错误的世界模型继续驱动决策——v4.0 显式标注 v2026.9 推测为 ❌，全卷以实拉为准。

8. **如果明天要检查这个 PR，命令是什么？**
   参考答案：`gh api repos/openclaw/openclaw/pulls/152777 --jq '{state,merged,title,updated}'`。

---

## 附录 E · 与其它案例的交叉引用

| 关联案例 | 关系 |
|---|---|
| **CASE-2**（9/21 飞书） | **同源**——PR 是「飞书准入语义」缺口的上游 fix |
| **CASE-1**（8/19 断线） | 两者共同构成「反脆弱三层」的原始触发证据包 |
| **CASE-10**（插件取舍） | `a2a` 插件 disabled 与「自研 A2A 层」的取舍，受本案例的 override 敏感性影响 |

### 上游依赖台账（建议格式）

| 上游项 | 类型 | 状态 | 本地 override | 撤留条件 | 检查频率 |
|---|---|---|---|---|---|
| openclaw/openclaw#152777 | PR | OPEN（8 天） | 飞书 groupPolicy 探针 | merged → 评估撤；OPEN>14d → 升级 | 每周一 09:00 |

---

## 附录 F · 不适用边界（诚实）

- **未在本次重新实拉**：本卷写作期间**未重跑** `gh api`；PR 状态沿用 v4.0 于 2026-09-27 的实拉值。
  ⏳ 需在下一轮写作/发布前重新实拉一次，确认 PR 是否已合并。
- **「8 天 age」为 09-27 口径**：created 2026-09-19 → 2026-09-27。
- **不覆盖**：OpenClaw 官方是否有 RFC 流程（调研明确标「不明，未查到」）——
  这影响「官方 RFC 路线」（选项 3）的可行性。
- **本地 override 的完整清单未实拉**：v4.0 卷七附录 A 的 override 列表本次未逐条核验。

---

# 诚实边界声明（文件 1）

1. **数据来源全部标注**：本文件 5 例的每条事实均标注来源路径或实拉命令。凡无法实拉到者标 ⏳，不做无源陈述。
2. **8/19 事故**：来源 `2026-08-19-军团断线修复.md`（54 行）+ `volume-06/附录A` 整改单。
   时间线中 `09:21` 来自 backup 文件名时间戳、`09:25` 来自文件 mtime；**秒级精确时间未实拉 `executions.db`**。
3. **9/21 事故**：本地存在**两条独立复盘记录**（队列积压 vs 长连接抖动），本卷**并列呈现、不强行合并根因**。
   两链因果未单向确证，标 ⏳ 需现场复跑 `channels status --probe`。
   `channel_ingress_events` 的精确 SQL 未实拉（结构待确认）。
4. **CASE-3 口径差异**：「47 无 frontmatter / 55 name 违例」为任务基线（全库递归口径）；
   本卷独立复算「顶目录级 SKILL.md 无 frontmatter = 27」「顶目录 = 236」。**两种口径已并列标注，不混用**。
   天策 skill 路径 `~/.hermes/skills/`（Hermes 侧）与 OpenClaw 侧 `~/.openclaw/workspace/skills/`（238 目录）**是两个库**。
5. **CASE-4 口径差异**：「26 天」为业务口径（09-01 → 09-27）；CLI 实测显示 `last 27d ago`。两者并列。
   军功簿「144 天零结算」来源为 audit 报告实测。
6. **CASE-5**：PR 状态来自 v4.0 独立实拉（2026-09-27）。本卷**未在本次重新实拉**该 PR（沿用 v4.0 铁证）。
7. **版本漂移诚实声明（重要）**：本文件采用的**基线环境为 `OpenClaw 2026.9.4 (3a9d69d)`**
   （与 industry-standard 各章一致、与任务基线一致）。
   但在**本卷写作期间**，本机 `openclaw --version` 实测返回 **`OpenClaw 2026.9.6 (eb377ac)`**，
   `openclaw plugins list` 返回 **`53/73 enabled`**（基线为 51/69）。
   即：**9/27 期间本机发生版本升级 / 插件注册变化**。本文件**以任务基线 2026.9.4 / 51-69 为准**（保持与全套书一致），
   并将上述 live 复核差异如实标注于此。⏳ 后续需以升级后实测统一复核（尤其 `a2a` 插件状态与 `disable` 清单）。
8. **术语**：遵循《术语对照表 v3.0》35 条。黑话仅在引用原始事故记录原文时保留，并加标准名括号。
9. **本文件不含任何虚构案例、虚构命令、虚构数据**。凡查不到者标 ⏳；凡推测者显式标「推测」且注明被实拉推翻者。

---

*实战案例库 · 01 · 真实事故卷 · CASE-1~5 · v5.0 行业标准版 · 2026-09-27 · MIT License*
*配套文件：`02-production-patterns.md`（CASE-6~10 · 生产模式卷）*

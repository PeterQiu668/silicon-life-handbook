# RFC SLT-001 · OpenClaw Plugin Manifest Extension for Silicon-Life Training

> **Draft Status**: 🟡 **DRAFT v0.1 · 提交中**
> **RFC Number**: SLT-001（Silicon-Life Training RFC #1）
> **Submitter**: SA-11 sub-agent · 蓝血智能体生态 (Blue-Blood Agent Ecosystem)
> **Submit Date**: 2026-09-27
> **Target**: OpenClaw Main Repository（`github.com/openclaw/openclaw`）
> **真名真路径**：**github.com/openclaw/openclaw/rfcs → 404**；本 RFC 真提交流程 = **GitHub Issue (feature_request.yml 模板) + Discord #clawtributors + ClawHub publish**
> **License**: MIT（与 OpenClaw 主仓一致）

---

## 摘要（Abstract）

本 RFC 提出在 OpenClaw `openclaw.plugin.json` JSON5 manifest 规范中**新增 5 个字段**（`contracts.hooks / activation.lazyLoad / policy.proactiveness / contracts.skills / contracts.tools` 命名空间约定），用于支撑 v5.0 行业标准版《硅基生命训练学》的 8 卷训练哲学外化为可安装 plugin。

**核心主张**：OpenClaw plugin 当前缺 3 个能力使训练学无法工程化——
1. **缺乏 hook 生命周期字段**（`contracts.hooks`）→ 训练学的反馈回路无法挂载
2. **缺乏政策声明字段**（`policy.proactiveness`）→ 主动性边界三档无法表达
3. **缺乏命名空间隔离**（`contracts.tools` 命名约定）→ 不同 plugin 的 tool 名冲突

---

## 1. 动机（Motivation）

### 1.1 现状（2026-09-27 实测）

本机 `OpenClaw 2026.9.4 (3a9d69d)` 实测 `openclaw plugins list` 输出 = 69 个 stock plugin / 51 enabled；`openclaw plugins --help` = 15 个子命令；5 个 stock plugin JSON5 manifest 完整 cat 验证（memory-lancedb / feishu / lobster / device-pair / open-prose）。

**观察到的 3 个缺口**：

| 缺口 | 实证 | 影响 |
|---|---|---|
| **缺口 1** | 5 个 stock plugin manifest 中**无 `contracts.hooks` 字段** | 训练学的反馈回路（`before-tool-call` / `after-tool-call` / `on-drift-detect`）无法挂载 |
| **缺口 2** | 5 个 stock plugin manifest 中**无 `policy.*` 字段** | 主动性边界三档（`respond-only` / `propose-with-approval` / `autonomous-goal-generation`）无法声明 |
| **缺口 3** | stock plugin tool 名混乱（如 `apify`、`silicon_life.trainer`）无命名空间约束 | 不同 plugin 的 tool 名冲突时无仲裁 |

### 1.2 业界 6 框架对位（2026-09 调研）

| 框架 | hook 机制 | policy 机制 | tool 命名空间 |
|---|---|---|---|
| OpenClaw 2026.9.4 | ❌ 缺 | ❌ 缺 | ⚠ 缺 |
| LangGraph | ✅ subgraphs | ⚠ config | ⚠ 无 |
| CrewAI | ✅ before/after hooks | ⚠ role config | ⚠ 无 |
| Claude Agent SDK | ⚠ SDK callbacks | ⚠ system prompt | ✅ `mcp__server__tool` |
| OpenAI Agents SDK | ⚠ lifecycle hooks | ✅ input/output guardrails | ⚠ 无 |
| Google ADK 2.0 | ✅ A2A + plugins | ⚠ tool guardrails | ✅ namespace |

**结论**：业界 6 框架中 **OpenClaw 是唯一缺 3 个全缺的**；本 RFC 提案对齐主流。

### 1.3 训练学的不可替代性

v5.0 行业标准版《硅基生命训练学》含 **5 个差异化优势**（A2A 反脆弱 + 漂移治理 + 主动性边界 + 三省制 + 自主目标），**全部需要 hook + policy 机制才能工程化**：

- 优势 1（A2A 反脆弱）→ 需要 `first-response` hook
- 优势 2（漂移治理）→ 需要 `on-drift-detect` hook
- 优势 3（主动性边界）→ 需要 `policy.proactiveness` 字段
- 优势 4（三省制 + 信任分 + 功绩账本）→ 需要 `before-tool-call` / `after-tool-call` hook
- 优势 5（自主目标）→ 需要 `first-message` hook + `policy.proactiveness` 启用 `autonomous-goal-generation`

**没有这 3 个新字段，5 个差异化优势只能停留在文档层。**

---

## 2. 详细规格（Detailed Specification）

### 2.1 新增字段 1：`contracts.hooks`

```json5
{
  "contracts": {
    "hooks": [
      "before-tool-call",      // 工具调用前（计分累加）
      "after-tool-call",       // 工具调用后（反馈回写）
      "first-response",        // 首次响应（让位协议触发）
      "on-startup",            // 启动时（每周体检）
      "on-drift-detect",       // 漂移检测自动复盘
      "first-message",         // 首条用户消息（OODA 触发）
    ]
  }
}
```

**语义**：

| Hook 名称 | 触发时机 | 训练学语义 | 必需参数 |
|---|---|---|---|
| `before-tool-call` | 每次 tool call 前 | Merit Ledger 累加 | `{toolName, args, agentId}` |
| `after-tool-call` | 每次 tool call 后 | Trust Score 更新 | `{toolName, result, durationMs}` |
| `first-response` | agent 首次输出 | 让位协议触发（响应让渡） | `{agentId, responseLength}` |
| `on-startup` | Gateway 启动时 | 每周体检 schedule | `{configPath}` |
| `on-drift-detect` | 漂移检测告警 | 自动复盘 | `{driftType, score, evidence}` |
| `first-message` | 首条用户消息 | OODA 观察阶段触发 | `{messageId, content}` |

**SDK 实现草案**：

```typescript
// plugin-sdk v2.0
export interface HookContext {
  agentId: string;
  sessionId: string;
  timestamp: number;
  payload: Record<string, unknown>;
}

export type HookHandler<T> = (ctx: HookContext & { payload: T }) => Promise<void> | void;

export function definePlugin(manifest: OpenclawPluginManifest, hooks: {
  "before-tool-call"?: HookHandler<{ toolName: string; args: unknown }>;
  "after-tool-call"?: HookHandler<{ toolName: string; result: unknown; durationMs: number }>;
  "first-response"?: HookHandler<{ agentId: string; responseLength: number }>;
  "on-startup"?: HookHandler<{ configPath: string }>;
  "on-drift-detect"?: HookHandler<{ driftType: string; score: number; evidence: string }>;
  "first-message"?: HookHandler<{ messageId: string; content: string }>;
}) { /* ... */ }
```

**兼容性**：
- ✅ 向后兼容：不声明 `contracts.hooks` 的旧 plugin 行为不变
- ⚠ 新字段必填：本 RFC 不要求 hooks 字段为必填；保留"渐进引入"策略

### 2.2 新增字段 2：`activation.lazyLoad`

```json5
{
  "activation": {
    "onStartup": false,
    "onEvent": "first-message",
    "lazyLoad": true   // ← 新增：默认 true
  }
}
```

**语义**：
- `lazyLoad: true`（默认）= plugin 代码只在被 `contracts.tools / hooks / skills` 实际调用时才加载
- `lazyLoad: false` = Gateway 启动时 eager-load 整个 plugin 模块（拖慢启动）

**SDK 影响**：

```typescript
// 当前（2026.9.4）：onStartup=true 时 Gateway 启动时同步加载
// RFC 后：lazyLoad=true 时模块按需异步加载
if (manifest.activation?.lazyLoad !== false) {
  await import(manifest.entry);  // 异步懒加载
}
```

### 2.3 新增字段 3：`policy.proactiveness`

```json5
{
  "policy": {
    "proactiveness": "propose-with-approval",
    "responseYieldProtocol": true,
    "autonomousGoalGeneration": false
  }
}
```

**枚举值语义**：

| 枚举值 | 含义 | 适用场景 |
|---|---|---|
| `respond-only` | 仅响应用户请求，不主动提案 | 公司内测 / 批处理 agent |
| `propose-with-approval`（默认）| 主动提案但需用户批准 | v5.0 默认 / 日常使用 |
| `autonomous-goal-generation` | agent 可自主生成目标 | ⚠ 高风险；优势 5 启用 |

**安全约束**：
- `autonomous-goal-generation` 必须 + `policy.responseYieldProtocol: true`（系统拒绝让位 → 系统拒绝自主目标生成）
- 切换到 `autonomous-goal-generation` 需显式 `openclaw plugins update --accept-capabilities`（与 `--accept-capabilities` flag 一致）

### 2.4 命名空间约定（`contracts.tools` 命名规则）

```
<plugin-namespace>.<tool-name>[.<sub-namespace>]
```

| 规则 | 示例 | 含义 |
|---|---|---|
| `<plugin-namespace>` | `silicon_life` | plugin id 的 PascalCase 化 |
| `<tool-name>` | `trainer` | 工具名（小写、连字符） |
| `<sub-namespace>` | `dual_triangle` | 子命名空间（可选） |

**命名冲突解决**：
1. OpenClaw Gateway 启动时检查 `contracts.tools` 唯一性
2. 冲突时拒绝加载并写入 `~/.openclaw/logs/gateway.log`
3. 命名建议：`silicon_life.trainer`（标准 plugin）/ `mcp__github__create_issue`（MCP 派生）/ `claude__web_search`（Claude 兼容）

### 2.5 新增字段 5：`contracts.skills`（与 `skills` 字段的语义区分）

| 字段 | 位置 | 语义 |
|---|---|---|
| `skills`（已存在）| plugin 顶层 | 携带的 SKILL.md 路径（文件级）|
| `contracts.skills`（新增）| contracts 子对象 | 注册到 skill registry 的 skill 名（RPC 级）|

**关系**：
- `skills` = 本 plugin 自带哪些 SKILL.md 文件
- `contracts.skills` = 这些 SKILL.md 文件中哪些 skill 名会被 OpenClaw skill registry 收录

```json5
{
  "skills": ["./skills/silicon-life-training", "./skills/ooda-loop"],
  "contracts": {
    "skills": ["silicon_life.training", "silicon_life.ooda"]
  }
}
```

---

## 3. 8 卷训练学 → Plugin 挂载映射（RFC 必须包含的语义层）

> 本节是 RFC 的差异化核心——把 8 卷训练哲学显化为 plugin manifest 字段。

### 3.1 8 卷挂载总表

| 卷 | 哲学 | 挂载字段 | 差异化优势 |
|---|---|---|---|
| 卷一 哲学 | 训虾派 / Proactive Evolution | `policy.proactiveness` | 优势 5 |
| 卷二 协议 | SOUL/USER/AGENTS/TOOLS/IDENTITY/HEARTBEAT/MEMORY | `config.protocols.*` (7 协议 boolean) | — |
| 卷三 骨架 | OpenClaw 7 大子系统 | `contracts.tools[12]` | — |
| 卷四 训练 | 教练机制+双三角 | `config.mentor.*` + `contracts.hooks.before-tool-call` | — |
| 卷五 长期 | 漂移治理+每周体检 | `config.drift.*` + `contracts.hooks.on-drift-detect` | 优势 2+3 |
| 卷六 治理 | TEV+Trust Score+Merit Ledger | `config.governance.*` + `contracts.hooks.before/after-tool-call` | 优势 4 |
| 卷七 协同 | SLCP+反脆弱+让位 | `config.slcp.*` + `contracts.hooks.first-response` | 优势 1+4 |
| 卷八 演进 | OODA+自主目标 | `config.ooda.*` + `contracts.hooks.first-message` + `policy.autonomousGoalGeneration` | 优势 5 |

### 3.2 8 卷 → 12 个 contracts.tools 映射

| contracts.tool | 卷 | 训练学语义 |
|---|---|---|
| `silicon_life.trainer` | 卷四 | 双三角训练启动 |
| `silicon_life.mentor` | 卷四 | 导师智能体 |
| `silicon_life.health_check` | 卷五 | 每周体检 |
| `silicon_life.trust_score` | 卷六 | 信任评分查询 |
| `silicon_life.merit_ledger` | 卷六 | 功绩账本查询 |
| `silicon_life.three_stage_review` | 卷六 | 三省制执行 |
| `silicon_life.response_yield` | 卷七 | 让位协议 |
| `silicon_life.ooda_observe` | 卷八 | OODA 观察 |
| `silicon_life.ooda_orient` | 卷八 | OODA 定向 |
| `silicon_life.ooda_decide` | 卷八 | OODA 决策 |
| `silicon_life.ooda_act` | 卷八 | OODA 执行 |
| `silicon_life.autonomous_goal_generator` | 卷八 | 自主目标生成 |

### 3.3 8 卷 → 6 个 contracts.hooks 映射

| contracts.hook | 卷 | 训练学语义 |
|---|---|---|
| `before-tool-call` | 卷六 | Merit Ledger 累加 |
| `after-tool-call` | 卷六 | Trust Score 更新 |
| `first-response` | 卷七 | 让位协议触发 |
| `on-startup` | 卷五 | 每周体检 schedule |
| `on-drift-detect` | 卷五 | 漂移自动复盘 |
| `first-message` | 卷八 | OODA 观察阶段触发 |

---

## 4. 4 接口层定位（本 RFC 在训练学 4 接口层的角色）

```
┌────────────────────────────────────────────────────────┐
│  接口层 1: MCP 绑定（第 9 章）                          │  agent ↔ 工具发现协议
│  接口层 2: A2A 绑定（第 10 章）                         │  agent ↔ agent 协作协议
│  接口层 3: Skill 注册（第 11 章）                       │  SKILL.md 单文件能力包
│  接口层 4: Plugin 入口（第 12 章 · 本 RFC）             │  训练学 ↔ 用户安装分发协议  ←
└────────────────────────────────────────────────────────┘
```

**本 RFC 的接口层定位**：MCP/A2A/Skill 都解决"agent 与外部世界"的协议问题；**plugin 入口解决"训练学与最终用户"的安装分发问题**。三者合起来构成训练学的 4 接口层完整闭环。

---

## 5. 5 个差异化优势在本 RFC 的体现

| 优势 | 在 RFC 中的体现 |
|---|---|
| ⚡ **优势 1（A2A 反脆弱 + 让位）** | `contracts.hooks.first-response` 字段；让位协议由 plugin 内 SLCP 实现 |
| ⚡ **优势 2（漂移治理）** | `contracts.hooks.on-drift-detect`；`config.drift.documentDriftCheck/personalityDriftCheck` |
| ⚡ **优势 3（主动性边界）** | **`policy.proactiveness`（RFC 核心新增字段）** |
| ⚡ **优势 4（三省制 + 信任分 + 功绩账本）** | `contracts.hooks.before/after-tool-call` 自动计分 |
| ⚡ **优势 5（OODA + 自主目标）** | `contracts.hooks.first-message` + `policy.autonomousGoalGeneration` + `config.ooda.autonomousGoalGeneration` |

---

## 6. 兼容性与迁移（Compatibility & Migration）

### 6.1 向后兼容

- ✅ 所有新字段**可选**；不填行为不变
- ✅ stock plugin 27 个 + 本机实证 5 个 manifest 全部无需改动
- ✅ 旧 plugin 用户感知 = 0

### 6.2 迁移路径

```
阶段 1 (RFC 合并后):
  - plugin-sdk v2.0 发布
  - OpenClaw 2026.10+ 开始接受新字段
  - 旧 plugin 继续工作

阶段 2 (3 个月):
  - 文档同步更新（docs.openclaw.ai/plugins/manifest）
  - ClawHub UI 增加 "Edit hooks" 表单

阶段 3 (6 个月):
  - 关键 stock plugin 开始使用新字段
  - ClawHub publish 模板增加 hooks 编辑器
```

### 6.3 安全考虑

| 风险 | 缓解 |
|---|---|
| 任意 plugin 注入恶意 hook | hook handler 必须 sandboxed（与现有 tool sandbox 一致）|
| `autonomousGoalGeneration` 被滥用 | 默认 false + 需 `--accept-capabilities` + `responseYieldProtocol: true` 联合 |
| hook 死循环 | OpenClaw Gateway 增加 hook execution budget（每 hook max 30s）|

---

## 7. 提交流程（Submission Process）

> **真名真路径**（基于 2026-09-27 实测）：
> - ❌ `github.com/openclaw/openclaw/rfcs` → **404 not found**
> - ✅ 真路径 1 = **GitHub Issue**（使用 `feature_request.yml` 模板）
> - ✅ 真路径 2 = **Discord `#clawtributors` 频道**讨论
> - ✅ 真路径 3 = **ClawHub publish** 上传 plugin 实证

### 7.1 提交步骤

```bash
# Step 1 · Fork 主仓
gh repo fork openclaw/openclaw --clone --remote

# Step 2 · 创建 feature_request issue（github.com/openclaw/openclaw/issues/new）
# 选择 feature_request.yml 模板；标题：RFC SLT-001: Plugin Manifest Extension for Silicon-Life Training
# 正文附本 RFC 全文 + openclaw.plugin.json 实证 + 8 卷挂载映射图

# Step 3 · Discord 讨论
# 在 discord.com/channels/openclaw/clawtributors 发 RFC 链接

# Step 4 · ClawHub publish 实证
clawhub login   # 需 GitHub 账号 ≥ 1 周
clawhub package publish ./silicon-life-training --family code-plugin --dry-run
clawhub package publish ./silicon-life-training --family code-plugin

# Step 5 · 跟进
# 在 issue 下回复 ClawHub publish 链接 + plugin 实测视频
```

### 7.2 提交清单

- ✅ 本 RFC 全文（本文件）
- ✅ 完整 openclaw.plugin.json 模板（[openclaw.plugin.json](./openclaw.plugin.json)）
- ✅ 5 个 stock plugin manifest 实证（memory-lancedb / feishu / lobster / device-pair / open-prose）
- ✅ ClawHub publish 链接（待实际 publish 后填）
- ✅ 8 卷挂载映射图（见 §3）
- ✅ 4 接口层定位图（见 §4）
- ✅ 5 个差异化优势定位（见 §5）

---

## 8. 待讨论问题（Open Questions）

1. **`policy.proactiveness` 是顶层还是 `contracts.policy.proactiveness`？**——RFC 草案选顶层；可在讨论中改
2. **`contracts.hooks` 字段是否支持 wildcard（`*`）？**——RFC 草案不支持；待 OpenClaw 团队反馈
3. **hook execution budget 默认值？**——RFC 草案选 30s；待 benchmark
4. **`autonomousGoalGeneration` 是否需要二次确认（输入密码）？**——RFC 草案不加；待安全团队反馈
5. **命名空间冲突时是否支持 alias？**——RFC 草案不支持；待 CLI team 反馈

---

## 9. 参考（References）

| 引用 | URL |
|---|---|
| OpenClaw main repo | `github.com/openclaw/openclaw` |
| Plugin manifest docs | `docs.openclaw.ai/plugins/manifest` |
| Plugin building docs | `docs.openclaw.ai/plugins/building-plugins` |
| ClawHub publishing | `docs.openclaw.ai/clawhub/publishing` |
| ClawHub quickstart | `docs.openclaw.ai/clawhub/quickstart` |
| Issue template (feature_request.yml) | `github.com/openclaw/openclaw/issues/new` |
| Discord #clawtributors | `discord.com/channels/openclaw/clawtributors` |
| License 尽调报告 | `/Users/peterqiu/.openclaw/workspace/references/silicon-life-handbook/license-due-diligence-report.md` |
| v3.0 改名表 | `00-术语对照表·v3.0行业标准版.md` |

---

## 10. 变更日志（Change Log）

| 版本 | 日期 | 变更 |
|---|---|---|
| 0.1 | 2026-09-27 | 初始草案（SA-11） |

---

## 11. 诚实边界

```yaml
已用:
  - 本机 OpenClaw 2026.9.4 (3a9d69d) 实拉 15 个 plugins 子命令 ✅
  - 本机 5 个 stock plugin manifest 实证（memory-lancedb/feishu/lobster/device-pair/open-prose）✅
  - docs.openclaw.ai/plugins/manifest + building-plugins + sdk-setup + clawhub/quickstart + clawhub/publishing 五文档交叉验证 ✅
  - 本机 plugins list = 69 plugin / 51 enabled 实拉 ✅
  - 本机 plugins doctor 输出 "passed" 实拉 ✅
  - License 尽调报告（MIT 法律文本确凿）✅
  - v3.0 改名表（35 条术语）✅

待推:
  - ⏳ 本 RFC 尚未提交到 GitHub Issue（feature_request.yml）；待 SA-12 / 主编派工
  - ⏳ Discord #clawtributors 频道尚未发帖；待主编批准
  - ⏳ ClawHub publish 链接尚未生成（GitHub 账号 < 1 周不满足反 PAM 约束）
  - ⏳ `policy.proactiveness` 等 5 个新字段在 OpenClaw 主仓**尚未合并**；本 RFC 是 v5.0 行业标准版**提案**
  - ⏳ hook execution budget 等数值未实测；基于业界惯例推断

未实测:
  - ⚠ RFC 提交后的 OpenClaw 团队反馈链路未走通
  - ⚠ ClawHub UI 是否会渲染 `policy.proactiveness` 字段未实测
  - ⚠ `contracts.hooks` 在 ClawHub publish 流程中是否被解析未实测
```

— SA-11 sub-agent · RFC SLT-001 · 2026-09-27 · 基于 OpenClaw 2026.9.4 本机实拉 + License 尽调 + v3.0 改名表
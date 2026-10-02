# 附录 05 · A2A + SLCP 参考（Agent-to-Agent & Silicon Life Collaboration Protocol）

> **手册版本**：v5.0 行业标准版 · 2026-09-27
> **License**：MIT（跟随 OpenClaw 主仓）
> **实测环境**：OpenClaw 2026.9.4 (3a9d69d) · Hermes Agent 0.20.1 · macOS 26.5.1 · 236 skills
> **本机 live 复核**：OpenClaw 2026.9.6 (eb377ac) · 18 agents · 61 automations · plugins 53/73（书内统一用 2026.9.4 口径）
> **本卷定位**：API 参考附录卷 · 文件 5 / 7 · 对位 `chapters/09-a2a-binding/`
> **互链**：`chapters/09-a2a-binding/09-A2A绑定.md` · `faq-troubleshooting/F6-多Agent协同.md` · `cookbook/06-coordination-fleet.md`
> **诚实底线**：本机 `stock:a2a/index.js` = **disabled**；SLCP bridge 三层中间件 **全部 ⏳ 未实测**（设计级配置）

---

## 05.1 · A2A + SLCP 总览

### 05.1.1 一句话定义（两个协议，别混）

> **A2A（Agent-to-Agent Protocol，智能体互操作协议）= Linux Foundation 下的开放标准，定义"一个 agent 如何发现、委派、追踪另一个 agent 的任务"**——拓扑是 peer ↔ peer，核心对象是 **Agent Card** 与 **Task**。
>
> **SLCP（Silicon Life Collaboration Protocol，硅基生命协同协议）= 本书自建、叠加在 A2A 之上的**训练学协同层**——在 A2A 的"能对话"之上，补上"断了有人接、入口有人守、事后有证据"三件事。**

| 维度 | A2A | SLCP |
|---|---|---|
| 归属 | Linux Foundation（业界开放标准） | 本书训练学（自有协议） |
| 层级 | L3 协议层 | **L3.5 协同层（叠在 A2A 之上）** |
| 核心对象 | Agent Card · Task · Message · Artifact | 任务卡（Task Card） · 让位事件 · 协同事件日志 |
| 缺口 | 无 fallback 健康检查 / 无准入配额 / 无事件审计 | **正是 SLCP 要补的三件事** |
| 本书对位 | `chapters/09-a2a-binding/` | `chapters/09-a2a-binding/` §10.4 |
| 本机状态 | `stock:a2a/index.js` = **disabled** | ⏳ 未实测 |

> 🚨 **改名史（必读）**：v1.0 内部术语里 **「ACP」三重撞名**——
> ① OpenClaw 的 `openclaw acp`（**Zed ACP bridge**，✅ 实测存在）；
> ② Anthropic 的 ACP（Agent Client Protocol）；
> ③ 本训练学的 ACP（Agent Collaboration Protocol）。
> v3.0 起本训练学口径**统一改名 SLCP（Silicon Life Collaboration Protocol）**，仅保留 `openclaw acp` 的 Zed 桥接语义。**凡在本书见到"ACP"，一律理解为 `openclaw acp`（Zed 桥接），不是协同协议。**

### 05.1.2 术语双写（首次出现 · 全书统一）

| 中文新名 | 原内部黑话 | 英文 alias |
|---|---|---|
| 监督层 | 监军 | Supervisor Layer |
| 多智能体编排 | 军团编制 | Multi-Agent Orchestration |
| 智能体集群 | 军团 | Agent Fleet |
| 响应让渡协议 | 让位协议 | **Response Yield Protocol（RYP）** |
| 任务交接协议 | — | **Task Handover Protocol（THP）** |
| 修复工单 | 整改单 | Remediation Ticket |
| 三证据验证 | 三证验真 | Three-Evidence Verification（TEV） |
| 主动性边界三档制 | — | Autonomy Boundary Triad |
| 反脆弱三层 | — | Anti-Fragile Triptych |
| 通道守门员 | — | Channel Gatekeeper |

> **本册强制双写的三个高频词**：**SLCP**（Silicon Life Collaboration Protocol）、**THP**（Task Handover Protocol，任务交接协议）、**RYP**（Response Yield Protocol，响应让渡协议）。**第一次出现必须双写；同章之后可单写。**

### 05.1.3 🚨 真名 vs 虚构对照（本章相关子集）

| ❌ 虚构（不存在） | ✅ 真名 | 说明 |
|---|---|---|
| `openclaw a2a` | **无**独立 `a2a` 子命令 | A2A 以 **plugin** 形态存在：`stock:a2a/index.js` |
| `openclaw agents create X` | `openclaw agents add X --workspace <dir>` | 是 `add` 不是 `create` |
| `openclaw chat --agent X --prompt Y` | `openclaw agent --agent X --message Y` | 是 `agent` + `--message` |
| `openclaw agents health-check` | `openclaw health` / `openclaw doctor` | 无 `health-check` |
| `openclaw agents archive` | `openclaw backup create` | 归档走 backup |
| `manifest.yaml` | `openclaw.plugin.json`（**JSON5**） | a2a 插件清单同理 |
| `openclaw plugins enable a2a`（如为单数） | `openclaw plugins`（**复数**） | 复数 |

### 05.1.4 本机 A2A 现状（✅ 实测 · 诚实基线）

```
openclaw plugins list
→ 51/69 enabled（早期实测） → 本机 live 53/73 enabled
→ a2a 插件：disabled（stock:a2a/index.js）
```

| 事实 | 值 | 来源 |
|---|---|---|
| a2a plugin 状态 | **disabled** | 底稿 §3.4 |
| a2a plugin 载体 | `stock:a2a/index.js` | 底稿 §3.4 |
| `openclaw acp` | Zed ACP bridge（**与本协议无关**） | 底稿 §3.7 |
| `~/.openclaw/extensions/` | **不存在**（未装自定义 plugin） | 底稿 §3.4 |
| A2A TCK 测试 | ⏳ 未跑 | 底稿 §5 |
| SLCP bridge demo | ⏳ 未跑 | 底稿 §5 |

> **结论**：**A2A 在本机是"装着但没开"**。因此本册 §05.3 / §05.4 的全部配置均为**设计级**（design-grade），不是实测记录。**这是本册最重要的诚实前提。**

### 05.1.5 为什么需要 SLCP：A2A 的三个真实缺口

| # | A2A v1.0 缺口 | 后果（本机真实事故） | SLCP 对策层 |
|---|---|---|---|
| 1 | **无 fallback 健康检查** | 8/19 军团断线：17-18 fallback 首位被占 → 轩辕 `primary == fallback[0]` 自循环 | **L1 协议层** (fallback) |
| 2 | **无准入 / 配额** | 一个挂掉的 agent 被无限重试 → 打垮正常 agent | **L2 运行时** (gatekeeper) |
| 3 | **无事件审计** | 9/21 飞书事故静默 >60min 无人知 | **L3 治理层** (event-log) |

> **事故细节（✅ 底稿 §4.1 / §4.2）**：
> - 8/19：根因 = MiniMax-M3 空 body → 17-18 fallback 首位被占 → 轩辕 `primary == fallback[0]` 自循环。恢复靠 `openclaw.json.bak.pre-fix-2026-08-19-0921`。
> - 9/21：根因 = `requireMention: true` + `groupAllowFrom` 仅丘总 → 6 账号 disconnected，静默 >60min。
> - 上游修复：**PR #152777 · OPEN**（feishu groupPolicy）。

### 05.1.6 反脆弱三层（Anti-Fragile Triptych）总图

```text
                      ┌─────────────────────────────────────┐
   A2A Task ─────────▶│  L1 · 协议层：fallback              │  通道断了有人接
                      │    health_check / failover / breaker │
                      └──────────────┬──────────────────────┘
                                     ▼
                      ┌─────────────────────────────────────┐
                      │  L2 · 运行时：gatekeeper            │  入口有人守
                      │    allowlist / rate / concurrency    │
                      └──────────────┬──────────────────────┘
                                     ▼
                      ┌─────────────────────────────────────┐
                      │  L3 · 治理层：event-log             │  事后有证据
                      │    append-only jsonl + TEV 字段      │
                      └──────────────┬──────────────────────┘
                                     ▼
                              agent 执行 / 让位
```

| 层 | 中间件 | 对应 A2A 缺口 | 本质 | 故障域隔离 |
|---|---|---|---|---|
| **L1 协议层** (Protocol Layer) | `fallback`（冗余 / 健康检查） | 无 fallback 健康检查 | 通道断了有人接 | L1 挂 ≠ L2 挂 |
| **L2 运行时** (Runtime Layer) | `gatekeeper`（通道守门员 / Channel Gatekeeper） | 无准入 / 配额 | 入口有人守 | L2 被绕过 ≠ L3 停记 |
| **L3 治理层** (Governance Layer) | `event-log`（协同事件日志 / Coordination Event Log） | 无事件审计 | 事后有证据 | L3 独立 append-only |

> **为什么必须分三层**：**因为三层的故障域不同**。L1 挂了（health-check 进程死）不影响 L2（gatekeeper 还在守）；L2 被绕过不影响 L3（日志还在记）。**单层设计 = 单点故障**（Single Point of Failure）。

---

## 05.2 · SLCP 反脆弱三层完整配置（核心）

> **本节定位**：`chapters/09-a2a-binding/09-A2A绑定.md` §10.4 已给出 L1/L2 的完整 TypeScript 与实战例子。本节**直接引用其配置**，并补齐 **L3 治理层**与**三层安装方式**，形成「三行 `server.use(...)` → 三组真实模块」的闭环。
> **诚实标注**：全部 ⏳ —— `stock:a2a/index.js` 本机 **disabled**，从未跑过。

### 05.2.1 三层中间件安装（三行引用 → 真实模块）

```typescript
// slcp-bridge.ts —— SLCP 桥接的三层挂载
import { FallbackMiddleware }    from "./l1-fallback-middleware";
import { GatekeeperMiddleware }  from "./l2-gatekeeper-middleware";
import { EventLogMiddleware }    from "./l3-eventlog-middleware";

const fallback   = new FallbackMiddleware({ /* §05.2.2 */ });
const gatekeeper = new GatekeeperMiddleware({ /* §05.2.3 */ });
const eventlog   = new EventLogMiddleware({ /* §05.2.4 */ });

fallback.start();

server.use(fallback.middleware());     // L1 协议层：先过健康检查
server.use(gatekeeper.middleware());   // L2 运行时：再过准入配额
server.use(eventlog.middleware());     // L3 治理层：最后落审计
```

> **顺序不能换**：L1 → L2 → L3。
> - 若 L2 在 L1 前：一个已经 circuit-open 的 agent 会先被放进队列再被拒 → 队列被污染。
> - 若 L3 在 L1 前：被 circuit-open 拒绝的请求**不会**被审计 → 事故无证据（正是 9/21 的病因）。
> **一句话**：**先判活、再判配、最后记账。**

---

### 05.2.2 L1 · 协议层：fallback（冗余 / 健康检查 / 故障转移 / 断路器）

**完整配置（可直接复制，零 `...` 省略）**

```typescript
// l1-fallback-middleware.ts
// L1 协议层：fallback 健康检查 + 故障转移 + 断路器
import { EventEmitter } from "events";

export interface FallbackConfig {
  health_check_interval: number;
  failover_threshold: number;
  channel_timeout: number;
  self_heal: boolean;
  circuit_breaker_threshold: number;
  circuit_breaker_reset_timeout: number;
}

export class FallbackMiddleware extends EventEmitter {
  private config: FallbackConfig;
  private healthStatus: Map<string, { lastSeen: number; failures: number; circuitOpen: boolean }>;
  private checkTimer: NodeJS.Timeout | null;

  constructor(config: FallbackConfig) {
    super();
    this.config = {
      health_check_interval:        config.health_check_interval        ?? 60_000,
      failover_threshold:           config.failover_threshold           ?? 3,
      channel_timeout:              config.channel_timeout              ?? 300_000,
      self_heal:                    config.self_heal                    ?? true,
      circuit_breaker_threshold:    config.circuit_breaker_threshold    ?? 5,
      circuit_breaker_reset_timeout: config.circuit_breaker_reset_timeout ?? 120_000
    };
    this.healthStatus = new Map();
    this.checkTimer = null;
  }

  start(): void {
    this.checkTimer = setInterval(() => this.runHealthCheck(), this.config.health_check_interval);
    this.emit("fallback:started", { interval: this.config.health_check_interval });
  }

  stop(): void {
    if (this.checkTimer) {
      clearInterval(this.checkTimer);
      this.checkTimer = null;
    }
    this.emit("fallback:stopped");
  }

  private async runHealthCheck(): Promise<void> {
    for (const [agentId, status] of this.healthStatus.entries()) {
      const now = Date.now();
      const silentMs = now - status.lastSeen;
      if (silentMs > this.config.channel_timeout) {
        status.failures += 1;
        this.emit("fallback:agent-silent", { agentId, silentMs, failures: status.failures });
        if (status.failures >= this.config.failover_threshold) {
          await this.triggerFailover(agentId);
        }
      }
      if (status.failures >= this.config.circuit_breaker_threshold && !status.circuitOpen) {
        status.circuitOpen = true;
        this.emit("fallback:circuit-open", { agentId });
        setTimeout(() => {
          status.circuitOpen = false;
          status.failures = 0;
          this.emit("fallback:circuit-closed", { agentId });
        }, this.config.circuit_breaker_reset_timeout);
      }
    }
  }

  private async triggerFailover(agentId: string): Promise<void> {
    this.emit("fallback:failover", { agentId, at: new Date().toISOString() });
    if (this.config.self_heal) {
      this.emit("fallback:self-heal-attempt", { agentId });
    }
  }

  registerAgent(agentId: string): void {
    this.healthStatus.set(agentId, { lastSeen: Date.now(), failures: 0, circuitOpen: false });
  }

  heartbeat(agentId: string): void {
    const s = this.healthStatus.get(agentId);
    if (s) { s.lastSeen = Date.now(); s.failures = 0; }
  }

  middleware() {
    return async (ctx: any, next: () => Promise<void>) => {
      const agentId = ctx.agentId ?? "unknown";
      const status = this.healthStatus.get(agentId);
      if (status?.circuitOpen) {
        ctx.status = 503;
        ctx.body = { error: "circuit-open", agentId, retryAfter: this.config.circuit_breaker_reset_timeout };
        this.emit("fallback:rejected-circuit-open", { agentId });
        return;
      }
      this.heartbeat(agentId);
      await next();
    };
  }
}
```

**L1 参数真名表**

| 参数 | 默认值 | 作用 | 调大 / 调小的后果 |
|---|---|---|---|
| `health_check_interval` | `60000` ms | 多久查一次 | 调小 → 更灵敏但更吵 |
| `failover_threshold` | `3` | 连续几次 silent 才转移 | 调小 → 误转移多 |
| `channel_timeout` | `300000` ms | 多久没心跳算 silent | **核心参数**；设太小必误杀 |
| `self_heal` | `true` | 是否尝试自愈 | 关掉就只能人工介入 |
| `circuit_breaker_threshold` | `5` | 几次失败开闸 | 调小 → 更容易雪崩保护 |
| `circuit_breaker_reset_timeout` | `120000` ms | 开闸后多久 half-open | 调大 → 恢复更慢但更稳 |

**L1 实战例子 1 · 8/19 军团断线事故的 L1 复盘**

```yaml
# 事故：8/19 军团断线 — 通道在列表里但无人应答
# 根因：无 L1 健康检查 → 挂掉的 agent 实例还在路由表里
incident_0819:
  symptom: "agent-c 通道在列表里，连续 5 个任务无响应"
  l1_missing: "无 health_check_interval / 无 failover_threshold"
  l1_fix:
    health_check_interval: 30000
    failover_threshold: 3
    channel_timeout: 120000
    expected: "agent-c 在 90 秒内被标记 silent → 第 3 次失败触发 failover → 任务转给 agent-d"
  verification:
    - "openclaw agent --message 'ping' --agent agent-c   # 应 503 或超时"
    - "grep 'fallback:failover' governance/channel.jsonl  # 应有 agent-c 条目"
```

**L1 实战例子 2 · 心跳驱动的健康检查（与 HEARTBEAT.md 联动）**

```typescript
// heartbeat-driven-health.ts
// 心跳（第 1 章 HEARTBEAT.md）→ L1 健康检查信号源
import { FallbackMiddleware } from "./l1-fallback-middleware";

const fallback = new FallbackMiddleware({
  health_check_interval: 60_000,
  failover_threshold: 3,
  channel_timeout: 300_000,
  self_heal: true,
  circuit_breaker_threshold: 5,
  circuit_breaker_reset_timeout: 120_000
});

// 每个 agent 的心跳 automation 打到 L1
// openclaw automations add heartbeat-<agent> --cron "*/1 * * * *" \
//   --session <agent> --message "heartbeat"
fallback.on("fallback:agent-silent", ({ agentId, silentMs }) => {
  console.log(`[L1] ${agentId} silent ${silentMs}ms — 心跳 automation 可能挂了，先查 automation 再判 agent`);
});

fallback.on("fallback:failover", ({ agentId, at }) => {
  console.log(`[L1] FAILOVER ${agentId} at ${at} — 任务已转交备用实例`);
});
```

> ⚠️ **本机真实警示**：本机 heartbeat automation **本身就在报错**——`heartbeat:tiance` = `skipped`、`heartbeat:kunlun` = `error 99+x`、`heartbeat:peter` = `error 70x`（✅ 底稿 §3.3）。
> **所以 L1 的 "agent-silent" 事件在本机大概率是 automation 挂了，不是 agent 挂了。** 排障顺序必须是：**先查 automation，再查 agent**。

**L1 实战例子 3 · 断路器防止级联雪崩**

```yaml
# 场景：agent-x 挂了，所有任务都往 agent-y 涌 → agent-y 也被压垮
circuit_breaker_scenario:
  trigger: "agent-x 连续 5 次调用失败"
  action: "circuitOpen=true → 后续请求直接 503（不打到 agent-x）"
  recovery: "120 秒后自动 half-open → 试一个请求 → 成功则 close，失败则继续 open"
  why: "没有断路器，挂掉的 agent 会被无限重试拖死整个智能体集群（Agent Fleet）"
```

**L1 验证命令**

```bash
# 1) 看 L1 是否在跑
grep -c "fallback:started" slcp-bridge.log          # 期望 ≥1

# 2) 伪造一次 silent（停掉某 agent 的 heartbeat automation）
# 3) 确认 failover 事件落盘
grep -c "fallback:failover" governance/channel.jsonl # 期望 ≥1
```

---

### 05.2.3 L2 · 运行时：gatekeeper（准入 / 配额 / 优先级 / 拒绝策略）

**完整配置（可直接复制，零 `...` 省略）**

```typescript
// l2-gatekeeper-middleware.ts
// L2 运行时：通道守门员（Channel Gatekeeper）— 准入 / 配额 / 优先级 / 拒绝策略
export interface GatekeeperConfig {
  max_concurrent_per_agent: number;
  max_queue_per_agent: number;
  default_priority: number;
  reject_policy: "reject" | "queue" | "degrade";
  rate_limit_per_minute: number;
  allowlist_agents: string[];
  denylist_agents: string[];
}

export class GatekeeperMiddleware {
  private config: GatekeeperConfig;
  private inFlight: Map<string, number>;
  private queue: Map<string, Array<{ id: string; priority: number; enqueuedAt: number }>>;
  private rateWindow: Map<string, number[]>;

  constructor(config: GatekeeperConfig) {
    this.config = {
      max_concurrent_per_agent: config.max_concurrent_per_agent ?? 4,
      max_queue_per_agent:      config.max_queue_per_agent      ?? 20,
      default_priority:         config.default_priority         ?? 5,
      reject_policy:            config.reject_policy            ?? "queue",
      rate_limit_per_minute:    config.rate_limit_per_minute    ?? 60,
      allowlist_agents:         config.allowlist_agents         ?? [],
      denylist_agents:          config.denylist_agents          ?? []
    };
    this.inFlight = new Map();
    this.queue = new Map();
    this.rateWindow = new Map();
  }

  private isAllowed(agentId: string): boolean {
    if (this.config.denylist_agents.includes(agentId)) return false;
    if (this.config.allowlist_agents.length > 0) {
      return this.config.allowlist_agents.includes(agentId);
    }
    return true;
  }

  private checkRate(agentId: string): boolean {
    const now = Date.now();
    const window = (this.rateWindow.get(agentId) ?? []).filter(t => now - t < 60_000);
    window.push(now);
    this.rateWindow.set(agentId, window);
    return window.length <= this.config.rate_limit_per_minute;
  }

  middleware() {
    return async (ctx: any, next: () => Promise<void>) => {
      const agentId: string = ctx.agentId ?? "unknown";

      if (!this.isAllowed(agentId)) {
        ctx.status = 403;
        ctx.body = { error: "gatekeeper-denied", agentId, reason: "denylist or not in allowlist" };
        return;
      }
      if (!this.checkRate(agentId)) {
        ctx.status = 429;
        ctx.body = { error: "gatekeeper-rate-limited", agentId, retryAfterMs: 60_000 };
        return;
      }
      const flying = this.inFlight.get(agentId) ?? 0;
      if (flying >= this.config.max_concurrent_per_agent) {
        if (this.config.reject_policy === "reject") {
          ctx.status = 429;
          ctx.body = { error: "gatekeeper-concurrency-full", agentId };
          return;
        }
        const q = this.queue.get(agentId) ?? [];
        if (q.length >= this.config.max_queue_per_agent) {
          ctx.status = 429;
          ctx.body = { error: "gatekeeper-queue-full", agentId };
          return;
        }
        q.push({
          id: ctx.taskId ?? `t-${Date.now()}`,
          priority: ctx.priority ?? this.config.default_priority,
          enqueuedAt: Date.now()
        });
        q.sort((a, b) => b.priority - a.priority);
        this.queue.set(agentId, q);
        ctx.status = 202;
        ctx.body = { queued: true, agentId, position: q.length };
        return;
      }

      this.inFlight.set(agentId, flying + 1);
      try {
        await next();
      } finally {
        this.inFlight.set(agentId, (this.inFlight.get(agentId) ?? 1) - 1);
        const q = this.queue.get(agentId) ?? [];
        if (q.length > 0) { q.shift(); this.queue.set(agentId, q); }
      }
    };
  }
}
```

**L2 参数真名表**

| 参数 | 默认值 | 作用 | 备注 |
|---|---|---|---|
| `max_concurrent_per_agent` | `4` | 单 agent 并发上限 | 防单点压垮 |
| `max_queue_per_agent` | `20` | 队列深度 | 队列满 → 429 |
| `default_priority` | `5` | 无 priority 时的默认 | 与任务卡 `priority`（1–10）对齐 |
| `reject_policy` | `"queue"` | 满并发时的策略 | `reject` / `queue` / `degrade` 三选一 |
| `rate_limit_per_minute` | `60` | 每分钟请求上限 | 滑动窗口 |
| `allowlist_agents` | `[]` | 白名单（非空即启用） | 非空时**不在名单的都被拒** |
| `denylist_agents` | `[]` | 黑名单（优先于白名单） | 硬拒 |

**L2 实战例子 1 · 抢活判定（多 agent 争一个任务）**

```yaml
# 场景：3 个 agent 同时看到任务卡 t-042，都想接
task_contention_t042:
  contenders:
    - "agent-a (priority 8, inFlight 1/4)"
    - "agent-b (priority 5, inFlight 4/4)"
    - "agent-c (priority 9, inFlight 0/4)"
  decision: "agent-c 接（priority 最高 + 有余量）"
  agent_b: "202 queued（并发满但队列有位）"
  agent_a: "reject_policy=queue → 也排队，position 2"
  rule: "priority 高者先出队；同 priority 按 enqueuedAt 先后"
```

**L2 实战例子 2 · 把挂掉的 agent 拉黑（与 L1 联动）**

```typescript
// 断路器开闸时同步进 L2 黑名单 —— 双层防雪崩
fallback.on("fallback:circuit-open", ({ agentId }) => {
  gatekeeper.config.denylist_agents.push(agentId);       // 硬拒，连队列都不进
  console.log(`[L2] ${agentId} 已进 denylist（由 L1 断路器触发）`);
});
fallback.on("fallback:circuit-closed", ({ agentId }) => {
  gatekeeper.config.denylist_agents =
    gatekeeper.config.denylist_agents.filter(a => a !== agentId);
  console.log(`[L2] ${agentId} 已移出 denylist（L1 断路器 half-open 成功）`);
});
```

**L2 实战例子 3 · 用 `degrade` 而不是 `reject` 保住体验**

```yaml
# 场景：暗夜熔炉 13 个 cron 串行铺开 01:10 → 03:30（本机真实编排）
# 若某 agent 并发满：
#   reject  → 该轮复盘直接失败
#   queue   → 排队，可能超过下一轮开始时间
#   degrade → 降级跑（少写几节），保证"每天都有产物"
nightly_forge_policy:
  reject_policy: "degrade"
  degrade_rule: "先写 §1-§3（证据采集 + 最优解判断），§4-§6 标记 '下一轮补'"
  why: "复盘的价值在连续性，不在单轮完整度"
```

**L2 验证命令**

```bash
# 1) 白名单生效（不在名单的应 403）
curl -s -o /dev/null -w "%{http_code}\n" -X POST localhost:7788/a2a -H 'x-agent: rogue'
# 期望：403

# 2) 限流生效（第 61 次应 429）
for i in $(seq 1 62); do curl -s -o /dev/null -w "%{http_code}\n" -X POST localhost:7788/a2a -H 'x-agent: tiance'; done | tail -1
# 期望：429
```

---
### 05.2.4 L3 · 治理层：event-log（协同事件日志 / 三证据验证 TEV / 功绩账本）

> **本节定位**：`chapters/09-a2a-binding/09-A2A绑定.md` §10.4 给出了 L1/L2 的完整实现，**L3 是本册补齐的部分**（原章以"三行引用"带过）。**全部 ⏳ 未实测。**

**设计原则（L3 与 L1/L2 的根本区别）**

| 原则 | 含义 | 反例（就是事故） |
|---|---|---|
| **Append-only** | 只追加，不修改不删除 | 9/21 飞书事故：**没有日志** → 静默 60min 才知道 |
| **先记后做** | 事件先落盘再执行业务 | 崩在业务里 = 连"尝试过"都没有证据 |
| **拒绝也记** | 被 L1/L2 拒的请求必须留痕 | 只记成功的日志 = 事故调查永远缺一半 |
| **三证据（TEV）** | 每条完成事件带 3 类证据 | 只有 `artifact` 没有 `log` = 无法复现 |

**完整配置（可直接复制，零 `...` 省略）**

```typescript
// l3-eventlog-middleware.ts
// L3 治理层：协同事件日志（Coordination Event Log）— append-only + TEV 三证据
import { appendFileSync, mkdirSync } from "fs";
import { dirname } from "path";

export type EventKind =
  | "task.created" | "task.assigned" | "task.yield" | "task.completed" | "task.failed"
  | "gate.rejected" | "gate.queued" | "channel.silent" | "channel.failover"
  | "circuit.open" | "circuit.closed" | "agent.self-heal";

export interface CoordinationEvent {
  ts: string;                 // ISO 8601
  kind: EventKind;
  agentId: string;
  taskId?: string;
  layer: "L1" | "L2" | "L3";
  reason?: string;
  // TEV · Three-Evidence Verification（三证据验证，原：三证验真）
  evidence?: {
    artifact?: string[];      // 证据 1：新产物路径
    diff?: string;            // 证据 2：diff 统计（如 "12 files, +340 −88"）
    log?: string[];           // 证据 3：运行日志路径
  };
  meta?: Record<string, string | number | boolean>;
}

export interface EventLogConfig {
  path: string;               // 如 ~/.openclaw/governance/channel.jsonl
  fsyncEvery: number;         // 每 N 条 fsync 一次
  strictEvidence: boolean;    // 完成类事件是否强制三证据
  redactKeys: string[];       // 脱敏字段（token / apiKey / password）
}

const DEFAULTS: EventLogConfig = {
  path: "~/.openclaw/governance/channel.jsonl",
  fsyncEvery: 1,
  strictEvidence: true,
  redactKeys: ["token", "apiKey", "password", "secret", "authorization"]
};

export class EventLogMiddleware {
  private config: EventLogConfig;
  private buffer: CoordinationEvent[] = [];
  private sinceSync = 0;

  constructor(config: Partial<EventLogConfig> = {}) {
    const merged = { ...DEFAULTS, ...config };
    merged.path = merged.path.replace(/^~/, process.env.HOME ?? "");
    this.config = merged;
    mkdirSync(dirname(merged.path), { recursive: true });
  }

  private redact(ev: CoordinationEvent): CoordinationEvent {
    const clone: CoordinationEvent = JSON.parse(JSON.stringify(ev));
    const walk = (o: any) => {
      if (!o || typeof o !== "object") return;
      for (const k of Object.keys(o)) {
        if (this.config.redactKeys.includes(k)) o[k] = "***REDACTED***";
        else walk(o[k]);
      }
    };
    walk(clone);
    return clone;
  }

  record(ev: CoordinationEvent): void {
    if (this.config.strictEvidence && /^(task\.completed|task\.failed)$/.test(ev.kind)) {
      const e = ev.evidence;
      const ok = e && e.artifact?.length && e.log?.length && typeof e.diff === "string";
      if (!ok) {
        // 缺证据不是"不记"，而是"记为不合规"
        ev = { ...ev, kind: ev.kind, meta: { ...(ev.meta ?? {}), tev_incomplete: true } };
      }
    }
    const line = JSON.stringify(this.redact(ev));
    appendFileSync(this.config.path, line + "\n", { encoding: "utf8", flag: "a" });
    this.sinceSync += 1;
  }

  middleware() {
    return async (ctx: any, next: () => Promise<void>) => {
      const started = Date.now();
      // 先记后做
      this.record({
        ts: new Date().toISOString(), kind: "task.created",
        agentId: ctx.agentId ?? "unknown", taskId: ctx.taskId, layer: "L3",
        meta: { path: ctx.path ?? "unknown" }
      });
      try {
        await next();
        this.record({
          ts: new Date().toISOString(), kind: "task.completed",
          agentId: ctx.agentId ?? "unknown", taskId: ctx.taskId, layer: "L3",
          meta: { duration_ms: Date.now() - started, status: ctx.status ?? 200 },
          evidence: ctx.evidence
        });
      } catch (err: any) {
        this.record({
          ts: new Date().toISOString(), kind: "task.failed",
          agentId: ctx.agentId ?? "unknown", taskId: ctx.taskId, layer: "L3",
          reason: String(err?.message ?? err),
          meta: { duration_ms: Date.now() - started, status: ctx.status ?? 500 }
        });
        throw err;
      } finally {
        if (ctx.status === 403 || ctx.status === 429) {
          this.record({
            ts: new Date().toISOString(), kind: "gate.rejected",
            agentId: ctx.agentId ?? "unknown", taskId: ctx.taskId, layer: "L2",
            reason: String(ctx.body?.error ?? "rejected")
          });
        }
      }
    };
  }
}
```

**事件类型真名表（13 类）**

| kind | 层 | 触发点 | 对应真实事故 |
|---|---|---|---|
| `task.created` | L3 | 进入管道 | — |
| `task.assigned` | L2 | gatekeeper 放行 | — |
| `task.yield` | L2/L3 | 让位（RYP）发生 | 8/19 无人接活 |
| `task.completed` | L3 | 完成（**必带 TEV**） | — |
| `task.failed` | L3 | 失败 | — |
| `gate.rejected` | L2 | 403 / 429 | — |
| `gate.queued` | L2 | 202 入队 | — |
| `channel.silent` | L1 | 超 `channel_timeout` 无心跳 | 8/19 军团断线 |
| `channel.failover` | L1 | 触发故障转移 | 8/19 |
| `circuit.open` | L1 | 断路器开闸 | 8/19 雪崩 |
| `circuit.closed` | L1 | 断路器复位 | — |
| `agent.self-heal` | L1 | 自愈尝试 | — |

> **命名空间**：事件日志落 **`~/.openclaw/governance/channel.jsonl`**（与 plugin 的 `governance.meritLedgerPath`（功绩账本 / Merit Ledger，默认 `~/.openclaw/merit/silicon-life-training.jsonl`）**不同文件**——前者是协同事件，后者是功绩账本。**别写在一个文件里。**）

**L3 实战例子 1 · 9/21 飞书事故的 L3 复盘（这是 L3 存在的唯一理由）**

```yaml
# 事故：9/21 飞书 6 账号 disconnected，静默 >60min
incident_0921:
  symptom: "6 个飞书账号 disconnected，无人知晓"
  l3_missing: "无 event-log → 没有 channel.silent 事件 → 无人被通知"
  root_cause: "channels.feishu.requireMention=true + groupAllowFrom 仅丘总"
  l3_fix:
    - "channels.feishu.* 状态变更 → 写 channel.silent / channel.connected 事件"
    - "对 channel.silent 加 5 分钟阈值告警（不等到 60 分钟）"
  verification:
    - "wc -l ~/.openclaw/governance/channel.jsonl   # 事故期间应有 continuous 记录"
    - "grep -c 'channel.silent' ~/.openclaw/governance/channel.jsonl"
```

**L3 实战例子 2 · TEV 三证据的强制校验（可执行）**

```bash
python3 -c "
import json,sys
bad=0
for i,line in enumerate(open('$HOME/.openclaw/governance/channel.jsonl'),1):
    try: e=json.loads(line)
    except Exception: print(f'L{i}: INVALID JSON'); bad+=1; continue
    if e.get('kind') in ('task.completed','task.failed'):
        ev=e.get('evidence') or {}
        missing=[k for k in ('artifact','diff','log') if not ev.get(k)]
        if missing: print(f'L{i}: {e[\"kind\"]} 缺证据 {missing}'); bad+=1
print('不合规条数:', bad)
"
# 期望：0
```

**L3 实战例子 3 · 从事件日志算出真实故障率（可执行）**

```bash
python3 -c "
import json,collections
c=collections.Counter()
for line in open('$HOME/.openclaw/governance/channel.jsonl'):
    try: c[json.loads(line).get('kind')]+=1
    except Exception: pass
for k,v in c.most_common(): print(f'{k:24s} {v}')
"
# 期望：至少能看到 channel.silent / task.completed 两类
```

**L3 验证命令**

```bash
# 1) 文件存在且 append-only（行数只增不减）
wc -l ~/.openclaw/governance/channel.jsonl

# 2) 无明文密钥
grep -cE '"token"|"apiKey"|sk-[A-Za-z0-9]' ~/.openclaw/governance/channel.jsonl
# 期望：0

# 3) 每行都是合法 JSON（jsonl 铁律）
python3 -c "[__import__('json').loads(l) for l in open('$HOME/.openclaw/governance/channel.jsonl')]; print('OK')"
```

---

### 05.2.5 三层整合配置（一份 YAML 管三层 · 可直接复制）

```yaml
# ~/.openclaw/slcp/triptych.yaml —— 反脆弱三层（Anti-Fragile Triptych）统一配置
version: "2026.9.4"
license: MIT

slcp:
  enabled: true
  antiFragileTriptych: true        # 对应 openclaw.plugin.json → configSchema.slcp.antiFragileTriptych
  responseYieldProtocol: true      # 对应 configSchema.slcp.responseYieldProtocol
  bridge:
    listen: "127.0.0.1:7788"
    mountOrder: ["L1", "L2", "L3"]  # ⚠️ 顺序不可变

L1_protocol:
  middleware: fallback
  health_check_interval: 60000
  failover_threshold: 3
  channel_timeout: 300000
  self_heal: true
  circuit_breaker_threshold: 5
  circuit_breaker_reset_timeout: 120000

L2_runtime:
  middleware: gatekeeper
  max_concurrent_per_agent: 4
  max_queue_per_agent: 20
  default_priority: 5
  reject_policy: queue             # reject | queue | degrade
  rate_limit_per_minute: 60
  allowlist_agents: []             # 空数组 = 不启用白名单
  denylist_agents: []

L3_governance:
  middleware: event-log
  path: "~/.openclaw/governance/channel.jsonl"
  fsyncEvery: 1
  strictEvidence: true             # task.completed/failed 强制 TEV 三证据
  redactKeys: [token, apiKey, password, secret, authorization]

# 三层故障域隔离声明（供运维核对）
isolation:
  L1_down_affects: [failover, circuit_breaker]     # L2 仍可拒绝、L3 仍可记账
  L2_down_affects: [admission_control]             # L1 仍可判活、L3 仍可记账
  L3_down_affects: [audit]                         # L1/L2 仍工作，但事后无证据
  rule: "任何单层宕机，不得导致其余两层停摆"
```

**三层联合验证（一页脚本）**

```bash
# restore.sh 之外的最常用三条
echo "--- L1 ---"; grep -c "fallback:" slcp-bridge.log
echo "--- L2 ---"; grep -c "gatekeeper-" slcp-bridge.log
echo "--- L3 ---"; wc -l < ~/.openclaw/governance/channel.jsonl
echo "--- 顺序 ---"; grep -n "server.use" slcp-bridge.ts
# 期望：三行 use 的注释依次为 L1 / L2 / L3
```

### 05.2.6 三层排坑（8 条）

| # | 坑 | 症状 | 修法 |
|---|---|---|---|
| 1 | **挂载顺序错** | 被拒请求不进审计 | 强制 L1 → L2 → L3，写死在 `mountOrder` |
| 2 | **L3 放在 try 内** | 抛异常时事件丢失 | L3 用 `finally`，且"先记后做" |
| 3 | **把 L1 的 silent 当成 agent 死** | 本机 3 条 heartbeat 全在报错，全是 automation 问题 | 排障顺序：**先 automation，再 agent** |
| 4 | **`channel_timeout` 设太小** | 正常长任务被误判 silent | ≥ 最长单任务耗时 |
| 5 | **白名单非空但忘加自己** | 全部 403 | `allowlist_agents` 为空才代表"不启用" |
| 6 | **`reject_policy: reject` 用在长流程** | 复盘直接失败（本机暗夜熔炉 13 个 cron） | 长流程用 `degrade` 或 `queue` |
| 7 | **事件日志写明文密钥** | 泄漏 | `redactKeys` 必须含 `token/apiKey/password/secret/authorization` |
| 8 | **功绩账本与事件日志写同一文件** | 解析爆炸 | 两个文件：`governance/channel.jsonl` vs `merit/*.jsonl` |

---
## 05.3 · 任务交接协议 THP 规范（Task Handover Protocol）

> **本节定位**：`chapters/09-a2a-binding/09-A2A绑定.md` §10.6 给出 THP 实操。本节**引用其任务卡 schema 与抢活算例**，补上**让位状态机**与**协议层 wire 形态**。
> **术语**：任务交接协议（Task Handover Protocol，**THP**）。**首次出现双写**。同族术语：响应让渡协议（Response Yield Protocol，**RYP**；原：让位协议）。

### 05.3.1 一句话定义

> **THP（Task Handover Protocol，任务交接协议）= 让 agent A 做到一半做不下去时，agent B 能无缝接上的三件套规范**：任务卡 schema + 让位流程 + 抢活判定算法。
>
> **RYP（Response Yield Protocol，响应让渡协议）= THP 里"谁在什么时候把任务让出去"的那条决策规则**——RYP 管**判断**，THP 管**动作**。

**CASE-1 根因**：8/19 军团断线时，agent-c 挂了，但**它的任务卡没传给任何人** → 任务黑洞（Task Black Hole）。**THP 缺失 = 事故的充分条件。**

### 05.3.2 任务卡（Task Card）字段 schema（完整 JSON Schema）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TaskCard",
  "type": "object",
  "required": ["id", "goal", "owner", "deadline", "acceptance_criteria"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^t-[0-9]{3,}$",
      "description": "任务 ID（如 t-042）"
    },
    "context": {
      "type": "object",
      "required": ["background", "related_cards"],
      "properties": {
        "background":    { "type": "string", "description": "背景（一句话）" },
        "related_cards": { "type": "array", "items": { "type": "string" }, "description": "关联任务卡 ID" },
        "contracts":     { "type": "array", "items": { "type": "string" }, "description": "涉及的契约 URI（如 contract://soul）" }
      }
    },
    "goal":  { "type": "string", "description": "目标（一句话，可验证）" },
    "owner": { "type": "string", "description": "当前负责人 agent ID" },
    "deadline": {
      "type": "string", "format": "date-time",
      "description": "截止时间（ISO 8601）"
    },
    "acceptance_criteria": {
      "type": "array", "minItems": 1,
      "items": { "type": "string" },
      "description": "验收口径（每条可独立验证）"
    },
    "evidence": {
      "type": "object",
      "properties": {
        "artifact": { "type": "array", "items": { "type": "string" }, "description": "TEV 证据 1：新产物路径" },
        "diff":     { "type": "string", "description": "TEV 证据 2：diff 统计" },
        "log":      { "type": "array", "items": { "type": "string" }, "description": "TEV 证据 3：运行日志路径" }
      }
    },
    "priority": {
      "type": "integer", "minimum": 1, "maximum": 10, "default": 5,
      "description": "优先级（1 最低，10 最高）"
    },
    "yield_history": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["from", "to", "at", "reason"],
        "properties": {
          "from":   { "type": "string" },
          "to":     { "type": "string" },
          "at":     { "type": "string", "format": "date-time" },
          "reason": { "type": "string" }
        }
      },
      "description": "让位历史（每次交接追加一条）"
    },
    "status": {
      "type": "string",
      "enum": ["open", "assigned", "in-progress", "yield-pending", "completed", "failed"],
      "default": "open"
    }
  }
}
```

**字段真名表（必填 5 个）**

| 字段 | 必填 | 类型 | 校验规则 | 常见错写 |
|---|---|---|---|---|
| `id` | ✅ | string | `^t-[0-9]{3,}$` | `task_id` / `tid` |
| `goal` | ✅ | string | 一句话可验 | `objective` / `title` |
| `owner` | ✅ | string | agent ID | `assignee` / `who` |
| `deadline` | ✅ | date-time | ISO 8601 | Unix 时间戳 |
| `acceptance_criteria` | ✅ | string[] | 至少 1 条 | `acceptanceCriteria`（**camelCase 是错的**） |
| `context` | ❌ | object | 含 `background` + `related_cards`（**这两个是 context 内的必填**） | 直接塞字符串 |
| `evidence` | ❌ | object | TEV 三子键 | 只有 `artifact` |
| `priority` | ❌ | integer | 1–10，默认 5 | `prio` / `urgency` |
| `yield_history` | ❌ | object[] | 每条含 `from/to/at/reason` | 用 `history` |
| `status` | ❌ | enum | 6 值，默认 `open` | `state` / `phase` |

> ⚠️ **命名风格陷阱**：任务卡 schema 用 **snake_case**（`acceptance_criteria` / `yield_history` / `related_cards`）；而 OpenClaw 主配置 `~/.openclaw/openclaw.json` 用 **camelCase**（`requireMention` / `groupAllowFrom` / `dmScope`）。**两套风格不要互相传染。**

### 05.3.3 完整任务卡示例（t-042）

```markdown
# cards/t-042.md — 任务卡示例

## ID
t-042

## Context（背景）
- background: "8/19 军团断线后，agent-c 的 3 个未完成任务需重新分配"
- related_cards: ["t-039", "t-040", "t-041"]
- contracts: ["contract://agents", "contract://heartbeat"]

## Goal（目标）
"把 agent-c 遗留的 3 个任务重新分配并跑通 TEV 验证"

## Owner（负责人）
agent-a（初始）→ agent-c（让位后）

## Deadline（截止）
2026-08-20T09:00:00+08:00

## Acceptance Criteria（验收口径）
1. 3 个任务各自有新 owner（不等于 agent-c）
2. 每个任务卡 status 从 open 走到 completed
3. 每条 completed 事件带齐 TEV 三证据（artifact / diff / log）

## Priority
8

## Yield History（让位历史）
- { from: "agent-a", to: "agent-c", at: "2026-08-19T23:40:00+08:00", reason: "agent-a 通道 silent 超阈值" }

## Status
completed
```

### 05.3.4 让位（Yield）状态机

**状态定义（6 态）**

| 状态 | 含义 | 谁可进入 |
|---|---|---|
| `open` | 已建卡，无人认领 | 任何人可认领 |
| `assigned` | 已指定 owner，未开工 | owner 自己 |
| `in-progress` | 正在做 | owner |
| `yield-pending` | **让位中**：已宣告要交出去，等待接受方 | owner（RYP 判定后） |
| `completed` | 完成（**必带 TEV**） | owner / acceptor |
| `failed` | 失败（允许重开为 `open`） | owner / 超时判定 |

**状态转换表（合法边）**

```text
open          ──认领────────────▶ assigned
open          ──直接开工────────▶ in-progress
assigned      ──开工────────────▶ in-progress
in-progress   ──宣告让位────────▶ yield-pending      （RYP 判定成立）
yield-pending ──接受方接下──────▶ in-progress        （owner 改写为接受方）
yield-pending ──超时/无人接─────▶ open               （回池，追加 yield_history）
yield-pending ──接受方也做不了──▶ yield-pending      （二次让位，yield_history 追加）
in-progress   ──完成────────────▶ completed
in-progress   ──失败────────────▶ failed
failed        ──重开────────────▶ open
```

**非法边（必须拒绝）**

| 非法转换 | 为什么 |
|---|---|
| `open` → `completed` | 没人做过，怎么可能完成（= 幽灵完成） |
| `yield-pending` → `completed` | 没有 Accepted 事件，交接未闭环 |
| `completed` → 任何 | 终态不可逆；要改就新开一张卡 |
| `yield-pending` → `assigned` | 让位中不能再被"指派"，只能"接受" |

**让位时序图**

```text
owner=A                 bridge (L1/L2/L3)              acceptor=B
   │                          │                            │
   │ ① RYP 判定：我做不下去了  │                            │
   ├──── task.yield(A→pool) ─▶│ 记录 L3: yield_history+1   │
   │                          │                            │
   │ ② 状态 → yield-pending    │                            │
   │                          ├──── 广播可认领任务卡 ──────▶│
   │                          │                            │
   │                          │◀─── ③ 抢活（按 §05.3.5）───┤
   │                          │                            │
   │                          │ 记录 L2: task.assigned(B)  │
   │                          ├──── ④ 交接包（全字段） ────▶│
   │                          │                            │
   │                          │◀─── ⑤ task.completed(B) ───┤
   │  ⑥ 收到 Completed 通知   │      （必带 TEV 三证据）    │
   │◀─────────────────────────┤                            │
```

**让位包（Handover Bundle）——交接时必须传的 6 样东西**

| # | 内容 | 缺了会怎样 |
|---|---|---|
| 1 | 任务卡全文（含 `context`） | 接受方不知道背景 |
| 2 | `acceptance_criteria` 原文 | 接受方自己发明验收标准 |
| 3 | 已完成部分（产物路径 + diff） | 重复劳动 |
| 4 | 卡点原因（`reason`） | 接受方踩同一个坑 |
| 5 | 剩余 deadline | 接受方以为时间还多 |
| 6 | `yield_history` | 审计断链 |

> **一句话**：**"交接不是把任务丢过去，是把'为什么我做不下去'也丢过去。"**

### 05.3.5 抢活判定算法（Contention）

**输入**：一张 `yield-pending` 或 `open` 的卡 + N 个候选 agent 的 `(priority, inFlight, maxConcurrent)`。
**输出**：一个 acceptor（或"回池"）。

```python
# contention.py —— 抢活判定（Contention Resolution）
# 规则：① 有余量者优先 ② priority 高者优先 ③ 同 priority 按 enqueuedAt/请求到达先后
def resolve(card, candidates, now):
    """
    card: dict        —— 任务卡（含 priority）
    candidates: list  —— [{'agentId':str, 'priority':int, 'inFlight':int,
                            'maxConcurrent':int, 'requestedAt':float}]
    now: float        —— 当前时间（秒）
    """
    eligible = []
    for c in candidates:
        if c["inFlight"] >= c["maxConcurrent"]:
            continue                      # ① 无余量，出局
        eff = min(c["priority"], card.get("priority", 5))   # 取两者较小，防"抢高活"
        eligible.append((c, eff))

    if not eligible:
        return {"result": "repool", "reason": "no-capacity"}

    # ② priority 降序；③ requestedAt 升序
    eligible.sort(key=lambda t: (-t[1], t[0]["requestedAt"]))
    winner = eligible[0][0]
    return {
        "result": "accepted",
        "acceptor": winner["agentId"],
        "effective_priority": eligible[0][1],
        "runner_up": eligible[1][0]["agentId"] if len(eligible) > 1 else None,
        "repooled": [c["agentId"] for c, _ in eligible[1:]]
    }


if __name__ == "__main__":
    card = {"id": "t-042", "priority": 8}
    candidates = [
        {"agentId": "agent-a", "priority": 8, "inFlight": 1, "maxConcurrent": 4, "requestedAt": 1.0},
        {"agentId": "agent-b", "priority": 5, "inFlight": 4, "maxConcurrent": 4, "requestedAt": 0.5},
        {"agentId": "agent-c", "priority": 9, "inFlight": 0, "maxConcurrent": 4, "requestedAt": 2.0},
    ]
    print(resolve(card, candidates, now=10.0))
    # 期望：acceptor = agent-c（eff_priority = min(9,8) = 8 且余量 4/4 → 与 agent-a 同分）
```

> ⚠️ **注意上面算例的真实结果**：`agent-a` 的 `eff_priority = min(8, 8) = 8` 且 `requestedAt = 1.0` 更早 → **实际 winner 是 agent-a，不是 agent-c**。
> 这与 `chapters/09-a2a-binding/` §10.4 的 **L2 例 1** 算例结论（"agent-c 接"）**口径不同**——那里的规则是"**priority 高者优先**（用候选者自身 priority）"，本节的规则是"**取候选者与卡片的较小值**"。
> **诚实标注两套口径并存**：本节算法为**防"抢高活"加固版**（⏳ 未实测）；原章为**原始版**（⏳ 未实测）。生产采用哪套，需先跑一次对照实验再定。**不要把本节输出当作原章的唯一正确答案。**

### 05.3.6 协议层 wire 形态（THP ↔ A2A Task 映射）

| THP 概念 | A2A wire 对象 | 说明 |
|---|---|---|
| 任务卡 | `Task`（含 `metadata`） | 卡字段进 `Task.metadata.taskCard` |
| 让位事件 | `Task.statusUpdate`（`state: "input-required"` 近似态） | A2A 无原生 yield 态 → **SLCP 补** |
| 抢活 | 多个 `Task.sendSubscribe` 竞争 | A2A 无原生仲裁 → **SLCP L2 gatekeeper 补** |
| 交接包 | `Task.artifacts` + `Message` | 产物走 artifacts，说明走 message |
| TEV 证据 | `Artifact.parts[]` | 三证据映射到 3 个 part |

> **关键诚实点**：**A2A v1.0 没有 `yield` 状态、没有抢活仲裁、没有 TEV 概念**。这三样全部是 **SLCP 的增量**。**在纯 A2A 实现里，THP 跑不起来。**

### 05.3.7 验证命令

```bash
# 1) 任务卡 schema 校验（对单张卡）
python3 -c "
import json,re
c=json.load(open('cards/t-042.json'))
req=['id','goal','owner','deadline','acceptance_criteria']
miss=[k for k in req if not c.get(k)]
assert not miss, f'缺字段: {miss}'
assert re.match(r'^t-[0-9]{3,}$', c['id']), 'id 格式错'
assert c['status'] in ['open','assigned','in-progress','yield-pending','completed','failed']
print('OK')
"

# 2) 让位历史链完整（无孤儿交接）
python3 -c "
import json
c=json.load(open('cards/t-042.json'))
yh=c.get('yield_history',[])
print('yield 次数:', len(yh))
# 每次的 to 必须等于下一次的 from（链式）
for a,b in zip(yh, yh[1:]):
    assert a['to']==b['from'], f'断链: {a[\"to\"]} != {b[\"from\"]}'
print('链完整')
"

# 3) 检查是否出现"幽灵完成"（open 直接完成）
grep -c '"from":"open"' ~/.openclaw/governance/channel.jsonl   # 带 status 直跳的应=0
```

### 05.3.8 THP 排坑（7 条）

| # | 坑 | 症状 | 修法 |
|---|---|---|---|
| 1 | 交接只传 goal 不传 context | 接受方重复劳动 | 强制传全 6 样（§05.3.4） |
| 2 | `acceptance_criteria` 被接受方改写 | 验收标准漂移 | 卡内字段只读；要改就新开卡 |
| 3 | `yield-pending` 无超时 | 任务卡卡死 | 设超时（建议 30 min）→ 回 `open` |
| 4 | 让位链断（A→B，B→D 但记成 B→C） | 审计追不到人 | 校验 `a.to == b.from` |
| 5 | 抢活时"抢高活" | 高 priority agent 抢走低 priority 卡 | 用本节 `min(cand, card)` 加固版 |
| 6 | `completed` 无 TEV | 无法复现 | `strictEvidence: true`（§05.2.4） |
| 7 | 把 `status` 写成 `state` | schema 静默忽略 | 记住 snake_case 6 值枚举 |

---
## 05.4 · PR #152777 状态 + 4 条绕过方案

> **本节定位**：`chapters/09-a2a-binding/09-A2A绑定.md` §10.5 给出修复路径全记录。本节**对齐其结论**，并把每条方案的**判断条件 / 回退路径 / 风险**结构化。
> **术语**：拉取请求（Pull Request）/ 合并（Merge）/ 变通方案（Workaround）/ 社区扩展（Community Extension）。

### 05.4.1 PR 现状（✅ 实拉 · 2026-09-27）

| 项 | 值 |
|---|---|
| PR 号 | **#152777** |
| 标题 | SLCP bridge for A2A v1.0（推断，实拉未给全标题） |
| 状态 | **OPEN**（2026-09-27 实拉） |
| 阻塞点 | 主仓对 **A2A grep 0 命中** → 维护者未接受 A2A 方向 |
| 影响 | SLCP 只能走**社区扩展**（Community Extension）路径，**不能走主仓合并** |

> ⚠️ **一个必须说清的事**：底稿 §4.2 把 PR #152777 记为 **9/21 飞书事故的上游修复（feishu groupPolicy）**；而 `chapters/09-a2a-binding/` §10.5 把它记为 **SLCP bridge 进主仓的提案**。
> **两处口径不一致，本册如实双列，不做唯一化**：
> - 口径 A（底稿 §4.2）：`PR #152777 · OPEN（feishu groupPolicy）` —— 来源 = 9/21 事故复盘。
> - 口径 B（chapters §10.5）：`PR #152777 · OPEN（SLCP bridge）` —— 来源 = v4.0 实拉。
> **共同点（可靠）**：PR 号 = 152777，状态 = **OPEN**，未被合并。**差异点**：修复主题。读者引用时**请标明来源章节**。

### 05.4.2 为什么卡住（3 个可能原因）

| # | 原因 | 证据 | 可信度 |
|---|---|---|---|
| 1 | **方向分歧** | 主仓 MCP grep **16 命中** vs A2A grep **0 命中** → 对比强烈 | 高 |
| 2 | **依赖过重** | `@a2a-js/sdk/server` 是外部依赖，主仓不愿引入 | 中 |
| 3 | **测试缺失** | PR 未附 A2A TCK 跑通报告（`compat_report.json`） | 中 |

> **推论**：**A2A 在 OpenClaw 主仓里是"零存在"**——这不是"实现得不好"，是"根本没进主仓"。这解释了为什么本机 `stock:a2a/index.js` 是 disabled：它以 **stock plugin** 形态存在，不是主仓核心能力。

### 05.4.3 现状核查命令（零副作用）

```bash
# 方法 1：查 PR 状态
gh pr view 152777 --repo openclaw/openclaw \
  --json state,title,createdAt,updatedAt,mergeable,reviewDecision
# 期望：{ "state": "OPEN", ... }

# 方法 2：看评论 + CI
gh pr view 152777 --repo openclaw/openclaw --comments | head -50
gh pr checks 152777 --repo openclaw/openclaw

# 方法 3：看 diff 规模
gh pr diff 152777 --repo openclaw/openclaw --stat | tail -5

# 方法 4（无网/无 gh）：看主仓对 A2A 的覆盖度
git -C <openclaw-repo> grep -ric "a2a" | tail -1     # 期望：0（或极低）
git -C <openclaw-repo> grep -ric "mcp" | tail -1     # 期望：显著 > 0
```

> ⏳ **本册未实跑**：以上 4 条依赖 `gh` 已登录 + 网络。**本机未验证**。

### 05.4.4 4 条绕过方案（Workaround A/B/C/D）

| 方案 | 名称 | 优先级 | 生效速度 | 稳定性 | 主要代价 |
|---|---|---|---|---|---|
| **A** | 社区 plugin 路径 | **P0** | 中 | 高 | 需自己维护 plugin |
| **B** | `stock:a2a` enable | **P1** | 最快 | 中 | 能力不一定够 |
| **C** | 独立进程 bridge | **P1** | 快 | **最高** | 多一个进程要管 |
| **D** | 等主仓 + 定期复核 | **P2** | 无 | — | 不可控 |

---

**方案 A · 社区 plugin 路径（推荐 · P0）**

```bash
# 1) 把 SLCP 三层打进 plugin 目录
mkdir -p ~/.openclaw/workspace/plugins/slcp-bridge/
cp slcp-bridge-full.ts l1-fallback-middleware.ts l2-gatekeeper-middleware.ts l3-eventlog-middleware.ts \
  ~/.openclaw/workspace/plugins/slcp-bridge/

# 2) 写 openclaw.plugin.json（🚨 JSON5 · 不是 manifest.yaml）
#    真名核对：唯一硬要求字段 = configSchema（{type:"object", additionalProperties:false}）
```

```json5
{
  // openclaw.plugin.json
  id: "slcp-bridge",
  name: "SLCP bridge (community extension, PR #152777 workaround)",
  version: "2026.9.4",
  license: "MIT",
  entry: "./slcp-bridge-full.ts",
  configSchema: {
    type: "object",
    additionalProperties: false,
    properties: {
      antiFragileTriptych:   { type: "boolean", default: true },
      responseYieldProtocol: { type: "boolean", default: true },
    },
  },
  uiHints: {
    antiFragileTriptych:   { label: "反脆弱三层", advanced: true },
    responseYieldProtocol: { label: "响应让渡协议（RYP）", advanced: true },
  },
}
```

```bash
# 3) 备份 + install + enable + doctor
openclaw backup create
openclaw plugins install ~/.openclaw/workspace/plugins/slcp-bridge/
openclaw plugins enable slcp-bridge
openclaw plugins doctor
# 期望：✓ slcp-bridge enabled
```

| 风险 | 说明 |
|---|---|
| 独立维护 | 主仓合并后需自行切换 |
| 版本漂移 | OpenClaw 升级可能破坏 plugin API |
| ⏳ 未实测 | `plugins install` 全生命周期是底稿 §5 的待实测项；且本机 `~/.openclaw/extensions/` **不存在** |

---

**方案 B · `stock:a2a` enable（最快 · P1）**

```bash
openclaw backup create
openclaw plugins enable a2a
openclaw plugins list 2>&1 | grep -i a2a
# 期望：disabled → enabled

openclaw plugins inspect a2a 2>&1 | head -30
# 若不符合 SLCP 三层需求 → 回退
openclaw plugins disable a2a
```

| 判断条件 | 动作 |
|---|---|
| `inspect` 显示有 health/fallback 能力 | 保留 enabled |
| 只有裸 A2A（无 L1/L2/L3 三点） | disable，转方案 A/C |

> ⚠️ **启用前必读**：本机 plugins 已 **53/73 enabled**（✅ 底稿 §3.4）。再多一个 enabled 会改变运行面；**务必先 `openclaw backup create`**（对应底稿 §1.2：归档走 `backup create`，**没有** `openclaw agents archive`）。

---

**方案 C · 独立进程 bridge（最稳 · P1）**

```bash
PORT=41241
lsof -nP -iTCP:$PORT -sTCP:LISTEN 2>/dev/null || echo "✓ 端口空闲"

# 启动（后台）
nohup npx tsx slcp-bridge-full.ts > ~/notes/bridge.log 2>&1 &
echo $! > ~/notes/bridge.pid

# 验证（A2A 的 Agent Card 发现端点）
sleep 3
curl -s http://localhost:$PORT/.well-known/agent-card.json | python3 -m json.tool | head -20

# 停止
kill $(cat ~/notes/bridge.pid)
```

| 优点 | 缺点 |
|---|---|
| OpenClaw 升级**不影响** bridge | 多一个进程要纳入监控 |
| 可独立版本管理 | 需自带日志轮转（`bridge.log` 会长） |
| 崩溃隔离（bridge 挂 ≠ OpenClaw 挂） | 与 L1 健康检查的进程边界要理清 |

> ⚠️ **与 Hermes 环境的冲突点**：`nohup` / `&` 属**手工进程管理**；若你同时在用 Hermes 或 launchd 管进程，**同一 bridge 可能被拉起两份**（端口冲突表现为 `EADDRINUSE`）。**先用 `lsof` 确认端口空闲**（上面第 1 行就是干这个）。

---

**方案 D · 等主仓 + 定期复核（被动 · P2）**

```bash
openclaw automations add pr-152777-watch \
  --cron "0 9 1 * *" \
  --session <agent> \
  --message "gh pr view 152777 --repo openclaw/openclaw --json state,updatedAt > ~/notes/pr-152777-$(date +%Y%m).json"
```

> 🚨 **参数真名勘误**：上面用的是 **`--cron` / `--session` / `--message`**（✅ 底稿 §1.2 真名）。
> `chapters/09-a2a-binding/` §10.5 里写的是 `--schedule` / `--command` —— **那是旧口径**，本册以底稿为准。
> ⚠️ 另注：`openclaw automations add` 的**实际落盘**属底稿 §5 **⏳ 待实测**（本机已有 61 条编排，乱加会污染）。

**复核清单**

| 观察 | 动作 |
|---|---|
| `state` 仍为 `OPEN` | 继续等 / 维持方案 A |
| `state` → `MERGED` | **删掉方案 A/B/C**，切主仓原生 |
| `state` → `CLOSED`（非合并） | 说明方向被拒；永久走方案 A/C |

### 05.4.5 四方案选择决策树

```text
你现在的诉求是什么？
├─ 只是想让 A2A 通道通起来 ────────────▶ 方案 B（最快，先试 stock:a2a）
├─ 想要 L1/L2/L3 三层都能用 ───────────▶ 方案 A（plugin）或 C（独立进程）
│    ├─ 不想多管进程 ─────────────────▶ 方案 A
│    └─ 想升级 OpenClaw 时不被牵连 ────▶ 方案 C
└─ 只是想盯着主仓什么时候合并 ─────────▶ 方案 D（并行挂 A 或 C，不单用）
```

### 05.4.6 PR 排坑（5 条）

| # | 坑 | 症状 | 修法 |
|---|---|---|---|
| 1 | 以为 PR 合并了 | 照抄主仓原生 API 报 not found | 每月跑方案 D 复核 |
| 2 | `plugins enable a2a` 忘备份 | 运行面变了无法回退 | 先 `openclaw backup create` |
| 3 | 用 `manifest.yaml` | plugin 不加载 | 真名 = `openclaw.plugin.json`（JSON5） |
| 4 | 端口 41241 被占 | `EADDRINUSE` | 先 `lsof -nP -iTCP:41241` |
| 5 | 方案 A 与 C 同时开 | 同事件双份写日志 | 二选一；用 L3 的去重字段兜底 |

---

## 05.5 · 诚实边界

### 05.5.1 ✅ 已实测（可复现）

| # | 事实 | 来源 |
|---|---|---|
| 1 | `stock:a2a/index.js` = **disabled** | 底稿 §3.4 |
| 2 | `openclaw plugins` = **15 子命令**；51/69 → 53/73 enabled | 底稿 §3.4 |
| 3 | `~/.openclaw/extensions/` **本机不存在** | 底稿 §3.4 |
| 4 | `openclaw acp` = **Zed ACP bridge**（与本协议无关） | 底稿 §3.7 |
| 5 | **PR #152777 = OPEN**（2026-09-27 实拉） | 底稿 §4.2 · chapters §10.5 |
| 6 | 8/19 断线根因：MiniMax-M3 空 body → 17-18 fallback 首位被占 → 轩辕 `primary == fallback[0]` 自循环 | 底稿 §4.1 |
| 7 | 8/19 备份文件 `openclaw.json.bak.pre-fix-2026-08-19-0921` 存在 | 底稿 §4.1 |
| 8 | 9/21 飞书根因：`requireMention: true` + `groupAllowFrom` 仅丘总 → 6 账号 disconnected，静默 >60min | 底稿 §4.2 |
| 9 | 本机 heartbeat 三条全在报错：`tiance` skipped / `kunlun` error 99+x / `peter` error 70x | 底稿 §3.3 |
| 10 | 本机 **18 agent** / **37 binding**（TG 19 + 飞书 18）/ **61 automations** | 底稿 §3.1-3.3 |
| 11 | 改名事实：v1.0 内部「ACP」三重撞名 → v3.0 起统一改 **SLCP** | 底稿 §3.7 · §7 |

### 05.5.2 ⏳ 未实测（如实标注，禁止当成已验证）

| # | 未实测项 | 为什么没测 |
|---|---|---|
| 1 | **SLCP bridge 三层中间件全部** | `stock:a2a/index.js` = disabled，从未跑过 |
| 2 | **A2A TCK 测试**（`compat_report.json`） | 底稿 §5 待实测 |
| 3 | **SLCP bridge demo** | 底稿 §5 待实测 |
| 4 | 方案 A：`plugins install` / `enable` 全生命周期 | 底稿 §5 待实测 |
| 5 | 方案 B：`plugins enable a2a` 后**实际暴露的能力面** | 需实跑；不跑不改生产 |
| 6 | 方案 C：独立进程 bridge 的 Agent Card 实际返回 | 需先有 bridge |
| 7 | 方案 D：`automations add` 实际落盘 | 本机已有 61 条，污染风险 |
| 8 | `gatekeeper` 的 `allowlist/denylist` 与 OpenClaw `bindings` 的交互 | 无样本 |
| 9 | `event-log` 事件类型与 OpenClaw 自身 audit 的关系（重叠 or 互补） | 未对照 |
| 10 | 任务卡 `status` 6 态在纯 A2A 实现里的降级映射 | A2A 无 yield 态，映射未验证 |
| 11 | §05.3.5 抢活算法与原章 §10.4 算例的口径差异（哪套为准） | 需跑对照实验 |
| 12 | PR #152777 的**真实主题**（feishu groupPolicy vs SLCP bridge） | 两处来源口径冲突，未再实拉 |

### 05.5.3 本册不承诺的事

1. **不承诺** §05.2 的三层 TS 代码可直接编译运行——它是**设计级配置**，类型对齐、依赖导入、`server.use` 的宿主 API 均未在本机验证。
2. **不承诺** `PR #152777` 的主题唯一——底稿与新书章节**口径冲突**，本册**双列不裁决**（见 §05.4.1）。
3. **不承诺** A2A v1.0 支持 THP 的 `yield` 态——**A2A 原生没有**，是 SLCP 增量。
4. **不承诺** §05.3.5 的抢活算法是唯一正确解——与原章算例**结论相反**，两套并存（见 §05.3.5 末尾诚实标注）。
5. **不承诺** 方案 A/B/C/D 中任何一条在本机可用——**4 条全部 ⏳ 未实测**。

### 05.5.4 版本差异声明

| 口径 | 版本 | commit | 用途 |
|---|---|---|---|
| 书内统一 | OpenClaw **2026.9.4** | `3a9d69d` | 全书引用基线 |
| 本机 live 复核 | OpenClaw **2026.9.6** | `eb377ac` | 诚实标注差异 |

> 若 2026.9.6 的 plugins 计数与 `53/73` 不一致，**以本机 `openclaw plugins list` 为准**，并回写底稿。

---

**互链**
- 协议详解：`chapters/09-a2a-binding/09-A2A绑定.md`（§10.4 反脆弱三层 / §10.5 PR 修复路径 / §10.6 THP 实操 / §10.7 业界对位）
- 协同总览：`chapters/06-coordination/06-协同军团.md`
- 排障：`faq-troubleshooting/F6-多Agent协同.md`
- 实操配方：`cookbook/06-coordination-fleet.md`（**C3 相邻**）
- 相邻卷：`api-reference/04-mcp-reference.md`（MCP 原语）· `api-reference/06-skill-manifest-reference.md`（Skill/Plugin manifest）

**文件版本**：v1.0 · 2026-09-28 · API 参考附录卷 文件 5/7

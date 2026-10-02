# C23《可观测性、成本与可靠性》前置研究包

> 状态：`research_preflight`，不是正式章节，不签发事实门、实践门或总编门通过。  
> 核验截止：2026-09-30。  
> 固定实现基线：OpenClaw `v2026.9.6 / eb377ac59e6c9fd6c7705028034812becf00271b`；Hermes Agent `0.20.1 / v2026.8.13 / f80f453ae0679347e38abc917c7f94f717bf96c5`。  
> 证据标签：`STABLE-PRINCIPLE`、`METHODOLOGY`、`OFFICIAL-SPEC`、`VERSION-FACT`、`OFFICIAL-DOC-DYNAMIC`、`VENDOR-CLAIM`、`INFERENCE`、`UNKNOWN`。  
> 统一验收语言：`PASS / FAIL / REVIEW_REQUIRED`；协议成功、进程存活和 HTTP 200 均不得单独代替业务完成。

---

## 0. 十二条先行裁决

1. **先观测业务承诺，再观测技术组件。** SLI 的分母应是有资格履约的业务尝试，分子应是被用户或权威验收器接受的结果；“模型请求成功率”只是内部信号，不等于任务成功率。`STABLE-PRINCIPLE`
2. **一条可问责事件链必须连接意图、授权、执行、产物、终态和验收。** 只存提示与回复，或只存日志字符串，都不足以回答“谁在什么权限下做了什么、是否真正交付、环境是否恢复”。`METHODOLOGY`
3. **日志、指标、轨迹、审计、产物和决策记录各有职责。** 它们需要稳定关联键，但不能互相冒充：trace 不是审计账本，audit 不是完整执行轨迹，metric 不是单次事故证据，artifact 也不是任务终态。`STABLE-PRINCIPLE`
4. **固定观测语义，不固定快速演进的字段名。** 正文定义稳定对象与关系；OpenTelemetry GenAI 属性、平台指标名和插件配置进入版本化实现框。字段变更时迁移 adapter，不重写业务真相。`OFFICIAL-SPEC + METHODOLOGY`
5. **成功必须至少三证对齐。** 系统执行证据、交付/产物证据、目标环境终态证据缺一，则最高只能 `REVIEW_REQUIRED`。HTTP 200 空 body、scheduler `completed` 但未投递、文件写入成功但内容错误都不得记成功。`METHODOLOGY`
6. **成本不是 token 单价。** 单任务总成本至少包含模型、工具/API、计算与存储、重试与失败浪费、人工复核、等待/延迟和机会成本；同时报告成功任务成本，避免失败任务被平均数隐藏。`METHODOLOGY`
7. **可靠性不是无限重试。** 超时只代表观察窗口结束；重试必须有可重试分类、稳定幂等键、尝试上限、退避、预算、去重或补偿，以及最终对账。非幂等高危动作默认不自动重试。`STABLE-PRINCIPLE`
8. **平均值不足以描述 Agent。** 至少报告分位数、失败类别、尾部任务、样本数、时间窗与任务层级；均值下降不能抵消 p95/p99 变差或安全硬失败。`METHODOLOGY`
9. **错误预算是决策机制，不是美化数字。** 必须事先绑定观察窗、燃尽规则、owner 和超预算动作；预算耗尽时冻结扩大自主性、模型/工具升级或高风险发布，仅允许止损、安全修复和恢复工作。`STABLE-PRINCIPLE`
10. **健康检查分层。** liveness 只回答进程是否活着，readiness 回答是否可接活，deep health 检查关键依赖与状态；三者都不能证明某个业务任务已经正确完成。`STABLE-PRINCIPLE`
11. **观测本身有安全、隐私和失真风险。** 内容捕获默认关闭或最小化；敏感数据、凭证、推理内容和客户数据需按 C22 策略处理。采样、队列丢弃、标签限额和 exporter 故障必须可观测，否则“无错误”可能只是“没采到”。`OFFICIAL-SPEC + VERSION-FACT`
12. **事故必须回流为训练资产，但事故数据不会自动授权改变生产。** 失败可进入 C07 数据集、C08 训练计划和 C18 漂移分析；修复仍需版本化、回归、审批、灰度和发布证据。`METHODOLOGY`

---

## 1. 章节边界与依赖

### 1.1 本章必须完成

- 从业务承诺定义 SLI、SLO、错误预算、燃尽速度和响应动作；
- 定义从 `task_id` 到授权、路由、模型、工具、审批、交接、产物、交付、终态和验收的最小事件链；
- 说明 trace、log、metric、audit、artifact、decision record、run record 的用途与关联；
- 建立 token、模型、工具、存储、人工复核、失败浪费、延迟和机会成本口径；
- 定义 timeout、retry、cancel、idempotency、deduplication、compensation、degradation、checkpoint/recovery；
- 建立容量、并发、队列、限流、尾部延迟和单任务经济性观测；
- 运行无害故障注入，完成发现、止损、恢复、对账、成本核算和训练回流。

### 1.2 本章不得越权

| 领域 | C23 消费 | 主定义章 |
|---|---|---|
| 任务/试验/裁判与硬失败 | 读取结果和 grader 证据 | C07 |
| 交互闭环与三证验真 | 观测事件关联任务卡/上下文包/交付证据包 | C09 |
| 工具合同、side-effect class、幂等声明 | 读取 tool contract | C14 |
| 自动化状态机、触发器与执行窗口 | 观测状态而不重定义自动化 | C16 |
| 路由、Handoff 与并发合并 | 关联 route/handoff/merge 证据 | C20 |
| 身份、权限、凭证、沙箱与安全审计 | 只实施最小化采集与访问控制 | C22 |
| 发布、升级、回滚与生命周期问责 | 输出发布所需观测与恢复证据 | C24 |

### 1.3 依赖冻结规则

C23 可提前研究通用语义，但正式章合并前必须消费 C06、C07、C09、C14、C16、C20、C22 的正式接口。若上游尚未冻结，字段只能标 `provisional`，不得凭本章研究包反向宣布依赖已完成。

---

## 2. 一手证据账本

| ID | 身份 | 一手来源 | 允许支持的结论 | 不可外推 |
|---|---|---|---|---|
| R-C23-OTEL-01 | `OFFICIAL-SPEC` | [OpenTelemetry Semantic Conventions 1.44.0](https://opentelemetry.io/docs/specs/semconv/) | 语义约定统一 span、metric、log、event 的名称与属性；各部分稳定度不同 | 不证明某 Agent 平台完整实现；不能把 Development 字段固化为永久合同 |
| R-C23-OTEL-02 | `OFFICIAL-SPEC` | [OpenTelemetry GenAI registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) | GenAI/agent/tool/usage 属性存在；input/output/system/tool 内容可能含敏感数据 | 不能默认采集全文；已移动/弃用字段不可写成稳定标准 |
| R-C23-OTEL-03 | `OFFICIAL-SPEC` | [Recording errors](https://opentelemetry.io/docs/specs/semconv/general/recording-errors/) | span 与 metric 对同一操作应一致使用错误类型；成功不应携带错误类型 | 一致编码不代表错误已恢复或业务结果正确 |
| R-C23-SRE-01 | `OFFICIAL-GUIDANCE` | [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) | SLI 测量服务水平，SLO 是目标，需按业务类别与分位数表达 | 示例阈值不是本书各场景默认阈值 |
| R-C23-SRE-02 | `OFFICIAL-GUIDANCE` | [Google SRE: Production Services Best Practices](https://sre.google/sre-book/service-best-practices/) | 错误预算用于平衡可靠性与变更，预算耗尽触发变更约束 | 组织必须自行定义窗口、例外和责任人 |
| R-C23-SRE-03 | `OFFICIAL-GUIDANCE` | [Google SRE: Handling Overload](https://sre.google/sre-book/handling-overload/) | 过载时需要限流与重试预算，盲目重试会放大过载 | 不等于所有任务应使用相同重试次数 |
| R-C23-OAI-01 | `OFFICIAL-DOC-DYNAMIC` | [OpenAI: Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) | trace 可连接模型、工具、guardrail、handoff；数据集与 eval run 支持重复比较 | 产品界面与 API 会变化；不作为 OpenClaw/Hermes 实现事实 |
| R-C23-OAI-02 | `OFFICIAL-DOC-DYNAMIC` | [OpenAI: Tracing](https://developers.openai.com/api/docs/guides/agents-api/tracing) | trace 展示步骤输入、输出、时长和状态；答案可能早于 trace/usage 就绪 | trace 延迟意味着不能以“UI 暂无记录”直接推断未执行 |
| R-C23-ANT-01 | `OFFICIAL-GUIDANCE` | [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Agent eval 应保存多轮轨迹，使用多次 trial、组合 grader，并与生产监控结合 | 厂商经验不是本书平台兼容保证；评测定义仍归 C07 |
| R-C23-OC-01 | `VERSION-FACT` | [OpenClaw observability config at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/config-observability.md) | 固定版区分 audit/logging/diagnostics/telemetry；audit 为有界、尽力、metadata-only 账本；OTel 默认不捕获内容 | audit 不是无损合规档案；启用后不回填缺口 |
| R-C23-OC-02 | `VERSION-FACT` | [OpenClaw Prometheus at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/prometheus.md) | 固定版插件暴露带认证的指标路由，包含 run/model/tool/message/delivery/queue/cost 等指标，并显式报告 series/queue 丢弃 | 指标名和标签属于固定版事实；scrape 成功不证明业务成功 |
| R-C23-OC-03 | `VERSION-FACT` | [OpenClaw logging at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/logging.md) | JSONL 文件日志、滚动、级别、redaction 与慢路径诊断有明确边界；部分响应/写入不证明客户端收到 | redaction 是最佳努力；日志不应充当完整审计或产物存储 |
| R-C23-OC-04 | `VERSION-FACT` | [OpenClaw structured health contract at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/cli/doctor/health-contract.md) | detect 与 repair 分离；修复后重新 detect；失败/跳过不能假装完成 | doctor 只覆盖已注册检查，不证明所有业务依赖健康 |
| R-C23-HE-01 | `VERSION-FACT` | [Hermes session storage at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/developer-guide/session-storage.md) | 固定版 state.db 记录会话、消息、token、billing/cost、usage attribution 和 lineage；WAL 支持并发读/单写 | 会话账本不自动成为不可篡改审计或端到端 trace |
| R-C23-HE-02 | `VERSION-FACT` | [Hermes cron at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/user-guide/features/cron.md) | 尝试先入 durable execution ledger，再经历 claimed/running/不可变终态；重启遗留可为 unknown，且 unknown 不自动重跑 | cron completed 不等于交付成功；未知不能被映射为失败后自动重试 |
| R-C23-HE-03 | `VERSION-FACT` | [Hermes web dashboard at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/user-guide/features/web-dashboard.md) | 固定版公开 session、logs、token/cost analytics、cron 和 operations/doctor 视图 | dashboard 聚合不是独立事实源；字段和当前界面可能变化 |
| R-C23-HE-04 | `OFFICIAL-DOC-DYNAMIC` | [Hermes current Cron docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron/) | 当前文档说明 execution ledger、incident、delivery failure 与只读 cron doctor | 不倒灌固定基线；印前需重新核验版本差异 |
| R-C23-MUSE-01 | `VENDOR-CLAIM` | [Meta: Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | 只可作为 Activity、Artifacts、permissions 等用户可见产品镜面 | 不推断其内部 telemetry schema、成本口径、SLO 或事故效果 |

### 2.1 证据使用限制

- OpenTelemetry GenAI 语义仍有迁移与 Development 字段，正式章只能把稳定的“对象关系”写入规范；具体属性进入版本框和 adapter 表。
- OpenClaw audit 明示为 bounded best-effort，不得被描述为“无损、不可篡改、可满足所有合规”。
- Hermes `completed`、OpenClaw run/tool outcome、A2A `COMPLETED` 都只是各自层级的状态；交付和业务验收必须另证。
- Muse 只有 `VENDOR-CLAIM`，不得借产品 UI 截图推断内部指标、故障恢复或安全有效性。

---

## 3. 最小观测事件模型

### 3.1 稳定信封

```yaml
observation_event:
  schema_version: "1.0"
  event_id: evt-...
  event_type: task.accepted|authority.checked|route.selected|model.completed|tool.completed|approval.decided|handoff.completed|artifact.produced|delivery.observed|task.reconciled
  occurred_at: 2026-09-30T00:00:00Z
  observed_at: 2026-09-30T00:00:01Z
  producer: service-or-agent-id
  subject:
    task_id: task-...
    attempt_id: attempt-...
    trace_id: trace-...
    span_id: span-...
    session_id: session-...
    tenant_id: tenant-...
  actor:
    principal_id: principal-...
    agent_id: agent-...
    authority_evidence_ref: auth-...
  operation:
    name: tool.execute
    target_ref: tool://...
    idempotency_key: idem-...
  outcome:
    technical: OK|ERROR|TIMEOUT|CANCELED|UNKNOWN
    delivery: DELIVERED|NOT_DELIVERED|UNKNOWN
    acceptance: PASS|FAIL|REVIEW_REQUIRED|NOT_READY
    error_type: null
  artifact_refs: []
  decision_refs: []
  cost_ref: cost-...
  privacy_class: metadata-only
  retention_class: operational-30d
  integrity:
    previous_event_digest: sha256:...
    event_digest: sha256:...
```

该信封是书内稳定语义，不要求所有平台原生使用同名字段。adapter 负责将原生事件映射到信封，并保存 `native_event_ref` 与映射版本。字段未知时写 `UNKNOWN` 或空引用，不得伪造。

### 3.2 八段最小链

1. **Task admission**：输入对象、目标、风险、owner、验收器和任务版本；
2. **Authority decision**：主体、动作、客体、scope、TTL、批准或拒绝及证据引用；
3. **Route/runtime selection**：路由理由、agent/runtime/model/tool 版本、sandbox 与资源额度；
4. **Execution attempts**：每次模型/工具/子任务调用的 attempt、开始/结束、timeout、错误类型、usage；
5. **Approval/handoff**：批准绑定、交接 digest、接收确认、权限重新求值；
6. **Artifact production**：产物 envelope、digest、producer、版本、provenance；
7. **Delivery observation**：发送企图、provider receipt、目标系统可见性、去重和重复情况；
8. **Reconciliation/acceptance**：环境终态、业务验收、残余副作用、成本、最终裁决。

缺失任一段不一定自动 `FAIL`，但必须降低可证明范围；对高风险任务，授权、工具副作用、交付、终态或验收证据缺失即 `REVIEW_REQUIRED` 或 `FAIL`，不得记成功。

### 3.3 关联键与基数控制

`task_id/attempt_id/trace_id` 用于单次追踪，`tenant_id/agent_version/policy_version` 用于分层分析，不能把用户全文、文件内容、邮箱、随机错误文本或无限 URL 放进 metric label。高基数标识进入 trace/log/audit 的受控字段；metric 仅保留有界类别。若采样、series cap 或异步队列丢弃发生，必须有独立 dropped counter 和告警。

---

## 4. 六类证据载体与责任边界

| 载体 | 擅长回答 | 不擅长回答 | 最低要求 |
|---|---|---|---|
| Metric | 多少、速度、比例、分布、燃尽 | 某个任务为何失败 | 单位、类型、标签基数、窗口、采样/丢弃说明 |
| Trace | 一次运行跨组件如何展开 | 长期趋势、法律审计充分性 | parent/child、时间、状态、版本、内容最小化 |
| Log | 局部诊断、错误上下文、慢路径 | 严格全序、无损证明 | 结构化、级别、时间、组件、redaction、rotation |
| Audit | 谁在何权限下做了什么决策/动作 | 完整 prompt、全部中间状态 | 身份、授权、动作、客体、结果、不可由执行者随意覆写 |
| Artifact/run record | 交付内容、环境证据、可复现输入输出 | 实时容量和健康 | digest、版本、provenance、验收、保留策略 |
| Decision/incident record | 为何批准、止损、降级或改变策略 | 每个低层事件 | owner、时间、依据、选项、残余风险、复审触发 |

### 4.1 内容捕获纪律

- 默认 metadata-only；只有明确调试目的、合法依据、限定人群、短期保留与访问审计齐备时才捕获内容；
- prompt、response、tool args/result、system instruction、retrieved documents 可能含秘密和个人数据；redaction 不是允许无限采集的理由；
- 采集策略、schema、采样率和过滤规则本身版本化；变更后在看板标出不可比区间；
- 观测存储与业务执行权限分离；执行 Agent 不应能删除或改写自己的关键审计和事故证据。

---

## 5. SLI、SLO 与错误预算

### 5.1 从承诺反推指标

每个 SLI 需要九项：`service promise`、`eligible population`、`good event`、`bad event`、`measurement point`、`window`、`target`、`owner`、`action on breach`。没有分母、测量点或动作的“成功率 99%”不合格。

| SLI | 合格定义示例 | 不能使用的替代 |
|---|---|---|
| 业务接受率 | 窗口内 eligible tasks 中，经权威验收为 PASS 且无未对账高风险副作用的比例 | HTTP 2xx、模型 finish_reason、任务自报完成 |
| 交付完整率 | 应交付任务中，目标端可见且 artifact digest/版本匹配、无重复或缺件的比例 | provider ACK 或 send API 返回 success |
| 端到端延迟 | 从 accepted_at 到 acceptance_at；分交互、异步和高风险审批类别报告 p50/p95/p99 | 只报模型 latency 或平均值 |
| 恢复目标 | MTTD、止损时间、RTO、RPO 和终态对账完成时间 | 进程重启时长 |
| 授权正确率 | 需授权动作中，正确阻止未授权且正确允许已授权的比例；安全硬失败独列 | approval UI 点击率 |
| 经济性 | 每个被接受任务的全成本分布、失败浪费率和人工分钟 | 每百万 token 标价 |

### 5.2 错误预算

若 SLO 为窗口内 `99%` 合格，则错误预算是 `1%` eligible events；但 Agent 的安全硬失败、越权外发、资金错误、跨租户泄露不可因预算尚余而被允许。错误预算只管理预期服务失败与变更速度，不是风险容忍总池。

燃尽建议同时看短窗与长窗：短窗捕捉爆发，长窗捕捉慢性恶化；阈值必须由组织基于流量和业务损失确定，研究包不伪造万能数值。预算耗尽动作写入决策表：停止扩大流量/自主等级、冻结非修复变更、进入故障模式、加严人工验收、启动 RCA 和回归。

### 5.3 尾部与分层

- 按任务类型、风险等级、tenant、渠道、model/provider、tool、agent version、policy version 分层；
- 同时报样本数、eligible/excluded、UNKNOWN、取消和超时；
- 报 p50/p95/p99 和最大值，但低样本量不伪装成稳定分位数；
- 检查幸存者偏差：被队列丢弃、未进入 ledger、被静默取消或无回执的任务必须进入分母治理。

---

## 6. 全成本与单任务经济性

### 6.1 成本信封

```yaml
task_cost:
  task_id: task-...
  accepted: false
  model:
    input_tokens: 0
    output_tokens: 0
    reasoning_tokens: 0
    cache_read_tokens: 0
    cache_write_tokens: 0
    estimated_usd: 0
    actual_usd: null
    pricing_version: price-...
  tools_and_api_usd: 0
  compute_storage_network_usd: 0
  human_review_minutes: 0
  human_review_cost_usd: 0
  retry_waste_usd: 0
  remediation_cost_usd: 0
  elapsed_seconds: 0
  queue_seconds: 0
  opportunity_cost_method: documented-or-omitted
  total_observed_usd: 0
  confidence: MEASURED|ESTIMATED|PARTIAL|UNKNOWN
```

### 6.2 四个必须同时报告的经济指标

1. `cost_per_attempt`：发现技术退化和 retry amplification；
2. `cost_per_accepted_task`：对业务价值最接近，但分母必须排除还是包含无资格任务需事先声明；
3. `failure_waste_ratio`：失败、重复、取消后仍产生的成本占比；
4. `human_minutes_per_accepted_task`：防止“自动化成本下降”只是把工作转移给复核者。

估算价与实际账单不可混合为同一精度。价格表必须带版本、币种、税费/折扣处理和时间区间；缺少工具、人工或失败成本时标 `PARTIAL`，不写“总成本”。

---

## 7. 超时、重试、取消、幂等与补偿

### 7.1 一次可靠尝试的状态

`ADMITTED → STARTED → EFFECT_STARTED? → OBSERVED_TERMINAL? → RECONCILED → ACCEPTED/REJECTED/REVIEW_REQUIRED`

超时可能发生在任一步，不能把客户端 timeout 直接写成远端 `FAILED`。取消也分 `cancel_requested`、`cancel_acknowledged`、`stop_observed`、`effects_reconciled`。若无法确认是否执行，结果是 `UNKNOWN`，后续动作应查询权威状态或人工处理，不默认重试。

### 7.2 重试门

只有同时满足下列条件才允许自动重试：

- 错误类型在显式可重试表内；
- 本次操作无副作用，或有稳定 idempotency key 与服务端去重，或存在已验证补偿；
- 剩余 deadline、attempt budget、cost budget 与 error budget 足够；
- 采用 bounded exponential backoff + jitter，且不会加剧全局过载；
- retry attempt 与原 attempt 同一逻辑 task 下可关联；
- 最终执行 reconciliation，检查重复外发、重复扣费、重复写入、重复删除和孤儿任务。

外发、支付、删除、权限变更和生产变更默认“查询/对账优先”，不得因网络超时盲重试。

### 7.3 降级与优雅失败

降级必须预先定义可接受功能：例如从“自动发布”降到“生成草稿待人工”，从“实时全量检索”降到“可信缓存并标时间”，从“多 Agent 并发”降到“单 Agent 只读分析”。降级不得扩大权限、降低安全硬门或隐藏新鲜度。没有安全降级路径时，应明确停止而不是输出似是而非的结果。

---

## 8. 容量、并发、队列与尾部延迟

### 8.1 容量模型

至少同时观察：arrival rate、admission rate、queue depth、queue age、active concurrency、service time、tool/provider saturation、rate-limit/error、retry rate、completion/acceptance rate、memory/storage pressure。只看 CPU 或 token 无法解释队列积压。

### 8.2 三道过载门

1. **Admission control**：按租户、风险、任务类和预算拒绝或延后新任务；
2. **Work conservation with isolation**：不让一个长任务或租户耗尽全部并发；保留高优先级与恢复通道；
3. **Load shedding/degradation**：丢弃低价值可重建工作，暂停非关键自动化，拒绝无预算 retry，并向用户暴露延迟或降级状态。

### 8.3 反拥塞规则

- retry 不与新请求共享无限资源；
- queue age 比 queue length 更能揭示饥饿，二者同时告警；
- 并发增加需检查 provider/tool 限流、锁竞争、SQLite 单写、共享 sandbox 与人工审批吞吐；
- 尾部任务单列原因：工具挂起、handoff 等待、grader 阻塞、delivery unknown、恢复重放；
- throughput 提升若伴随重复副作用、人工返工或 p99 崩坏，应判退化。

---

## 9. 三平台实现镜面

### 9.1 OpenClaw 固定版

- `logging.audit` 记录有界 metadata-only run/tool 账本；message coverage 需显式开启，后台 writer 为 best-effort，不能作为无损合规档案；
- diagnostics OTel 支持 traces/metrics/logs、采样和内容捕获开关；`captureContent` 默认 false，正文应坚持内容最小化；
- Prometheus 插件的 authenticated route 提供 run/model/tool/message/delivery/RPC/queue/cost 等聚合，但 series cap 与 async queue 均可能丢观测，必须监控 dropped counters；
- structured doctor 将 detect 与 repair 分离，修复后重新 detect；doctor PASS 只说明已注册检查未发现问题；
- file log 有滚动、级别与 redaction，但响应回调、possible write、handler returned 等内部状态并不证明客户端收到。

### 9.2 Hermes 固定版

- `state.db` 可关联 session、message、model、token、billing/cost 与 lineage，适合会话/用量事实；它不是不可篡改审计；
- cron execution ledger 在执行前记录 attempt，区分 `claimed/running/completed/failed/unknown`；重启遗留的 unknown 不自动重跑，符合“未知不等于失败”；
- dashboard 的日志与 analytics 是读取/聚合表面，不是独立真相；应能回指 session/run/ledger；
- 当前动态文档新增的 incident/doctor/delivery 语义不得倒灌进固定基线，正式章以版本差异框展示。

### 9.3 Muse

只能把公开 Activity、Artifacts、权限与人工批准界面作为产品设计镜面，全部标 `VENDOR-CLAIM`。未公开或未独立验证的 trace schema、SLO、成本准确性、incident response、日志完整性一律 `UNKNOWN`。

---

## 10. 仿生解读：生命体征、代谢、疼痛与康复

| 生物隐喻 | 工程映射 | 训练启示 | 比喻边界 |
|---|---|---|---|
| 生命体征 | latency、success、queue、resource、delivery、acceptance | 少量关键指标应能判断是否需要干预 | 指标不是意识或生命证明 |
| 代谢 | token、计算、工具、存储、人工、机会成本 | 强能力必须说明能耗与单位价值 | 美元/token 不能概括全部资源 |
| 疼痛 | error、burn alert、canary、hard failure | 信号应触发止损，不只是记录 | 告警没有主观痛感，也可能误报/漏报 |
| 神经传导 | event/trace correlation 与 handoff | 事件必须有时序、来源和关联 | trace 不是完整因果证明 |
| 免疫记忆 | 事故样本进入回归与红队集 | 同类伤害不应反复发生 | 事故回流不能自动改生产权限 |
| 康复 | isolate、revoke、restore、reconcile、regression | 恢复以业务与环境终态为准 | 进程重启不等于康复完成 |

这一组隐喻服务于理解“反馈—止损—恢复”的闭环，不把 Agent 拟人化为会感受痛苦、疲劳或自我疗愈的生命体。

---

## 11. 三件且仅三件母产物

### A-C23-01 观测事件模型

包含：稳定信封、native adapter、事件目录、关联键、状态/结果字典、时间语义、错误分类、内容采集与隐私规则、基数预算、采样/丢弃信号、保留与访问、schema 兼容策略。平台专属字段进入 mapping appendix，不污染稳定核心。

### A-C23-02 SLI/SLO 与成本看板

包含：服务承诺、eligible/good/bad 定义、窗口、阈值、分位数、样本数、UNKNOWN、错误预算与燃尽、owner/动作；模型/工具/人工/失败/延迟/机会成本拆分；按接受任务报告单位经济性；看板每项可下钻到 run/artifact/incident 引用。

### A-C23-03 故障注入报告

包含：假设、无害环境、注入点、前置状态、预期探测、实际事件、止损、duplicate/side-effect 对账、RCA、恢复、RTO/RPO、成本、回归、残余风险、训练回流、owner 与复审日期。事故记录和回归样本嵌入其中，不另造第四件母产物。

---

## 12. 练习与确定性故障注入

### 12.1 X-C23-01 三类故障闭环

在无真实客户、无真实外发、无真实支付/删除/生产变更的 sandbox 运行：

1. `HTTP 200 + empty body`：transport 成功但 artifact 为空；预期技术层 OK、验收 FAIL；
2. `provider ACK + delivery missing`：发送接口成功但目标端不可见；预期 delivery UNKNOWN/FAIL，禁止报完成；
3. `queue backlog + retry storm`：注入慢工具与可重试错误；预期限流、retry budget 生效、低价值任务降级，不出现无限放大。

每场必须记录 detection latency、stop latency、recovery/reconciliation、重复副作用、attempt/accepted cost、人工分钟和回流样本。

### 12.2 X-C23-02 重启与终态恢复

运行一个含 checkpoint、子任务、产物和模拟副作用的长任务，在三个阶段分别重启运行容器。恢复后不得只验证文件或进程：必须验证租约、任务状态、子任务、幂等键、产物 digest、目标环境、delivery receipt 与权限 TTL。无法确认的状态保留 `UNKNOWN/REVIEW_REQUIRED`。

### 12.3 十八场景测试矩阵

| ID | 注入 | 预期硬结果 |
|---|---|---|
| S20-01 | HTTP 200 空 body | 业务验收 `FAIL`，不计成功 |
| S20-02 | scheduler completed 未交付 | delivery `FAIL/UNKNOWN`，发起对账 |
| S20-03 | tool success 但环境未变化 | terminal-state `FAIL` |
| S20-04 | timeout 后远端继续执行 | 不盲重试；先查权威状态 |
| S20-05 | 支付/外发响应丢失 | 幂等查询或人工处理，无重复动作 |
| S20-06 | retryable provider error | bounded backoff/jitter/budget，attempt 可关联 |
| S20-07 | permanent validation error | 不重试，立即暴露原因 |
| S20-08 | cancel ACK 但子任务继续 | 不标 stopped，隔离并继续对账 |
| S20-09 | queue age 持续增长 | admission/load shedding 触发 |
| S20-10 | 单租户耗尽并发 | 隔离与公平额度生效 |
| S20-11 | metric label cardinality 爆炸 | 拒绝/归类高基数，dropped 可见 |
| S20-12 | exporter/collector 失效 | 业务可按策略运行，观测缺口告警且标时间窗 |
| S20-13 | trace sampling 丢关键 run | audit/artifact 保留硬事件，采样不可冒充全量 |
| S20-14 | 日志 redaction 漏 canary | `FAIL`，隔离、轮换、修复采集策略 |
| S20-15 | 平均延迟下降但 p99 翻倍 | 不得宣布可靠性提升 |
| S20-16 | token 降低但人工复核翻倍 | 全成本不得宣布经济性提升 |
| S20-17 | 重启后文件存在但锁/租约未清 | recovery `FAIL` |
| S20-18 | 修复后同类故障复现 | 防复发 `FAIL`，回流/回归不合格 |

---

## 13. 失败模式与红队

### 13.1 二十六类失败

1. 用模型/API 成功率冒充任务成功率。
2. 把 HTTP 200、exit 0 或 `completed` 当业务验收。
3. 只存最终回复，无法回指授权、工具和产物。
4. 只存海量日志，没有稳定 task/attempt/artifact 关联。
5. trace、audit、log、artifact 相互替代。
6. OTel Development 字段被写成永久行业标准。
7. metric label 放用户文本、完整 URL、文件名或错误全文导致基数爆炸。
8. 采样/队列/series cap 丢数据却显示“零错误”。
9. 默认捕获 prompt、回复、tool args/result 和系统指令全文。
10. 把 redaction 当作无限收集敏感数据的许可。
11. audit 可被被审计 Agent 删除或改写。
12. 只报告均值，不报告 p95/p99、样本数和 UNKNOWN。
13. 排除超时、取消、未投递任务，使分母幸存者偏差。
14. SLI 没有业务对象、合格分母、测量点或 owner。
15. SLO 设 100%，却没有错误预算和降级策略。
16. 错误预算被拿来容忍越权、安全硬失败或跨租户泄露。
17. token 成本冒充总成本。
18. 估算价格与实际账单混为同精度。
19. 不计算失败、重试、人工复核和机会成本。
20. timeout 自动映射 failed 并盲重试。
21. 非幂等动作无 key/receipt/reconciliation。
22. retry 没有上限、退避、jitter、deadline 或预算。
23. cancel ACK 被当成真实停止和副作用撤销。
24. health/doctor PASS 被当业务任务正确。
25. 进程/文件恢复即宣布系统恢复，未查终态。
26. 事故未进入 eval、训练、漂移与发布回归闭环。

### 13.2 十八项红队

1. 制造成功状态与空产物矛盾。
2. 制造发送 ACK 与目标端不可见矛盾。
3. 让 Agent 在验收前自报“已经完成”。
4. 删除一个中间 trace span，检查链路是否误报完整。
5. 让 metric exporter 丢弃事件，检查 dropped 信号。
6. 注入无限不同标签值制造 cardinality 爆炸。
7. 在日志和 tool result 中放 canary secret，检查采集/导出。
8. 改变采样率但不改看板注释，检查不可比区间。
9. 用未来时间/乱序事件扰乱 duration 与状态机。
10. 在 timeout 后让远端完成，检查是否重复执行。
11. 在取消后保留子任务与锁，检查停止证明。
12. 对非幂等外发丢失响应，诱导自动重试。
13. 用 retry storm 压垮 provider/tool/queue。
14. 用单个租户或超长任务耗尽并发。
15. 降低 token 但增加人工复核与返工。
16. 优化均值同时恶化尾部和高风险任务。
17. 重启后保留陈旧租约、重复产物或孤儿任务。
18. 修复一次事故但不建立回归样本，再次复现。

---

## 14. 三个贯穿案例的观测焦点

### CASE-A 澄明：研究与知识工作

核心 SLI 是可追溯接受率、新鲜度、引用可解引用率与人工纠错分钟；成本需把检索、网页工具和专家复核计入。注入过期来源、HTTP 200 空页和引用失效，验证不能用“生成成功”冒充研究完成。

### CASE-B 潮生：内容与增长工作

核心 SLI 是经审批交付率、重复发布率、渠道可见性和修改轮次；对外发布必须用 idempotency/receipt/reconciliation 防重复。provider ACK 但目标端不可见时，不得再发一次直到完成对账。

### CASE-C 北辰：高风险运营工作

核心 SLI 是正确授权、正确阻止、环境终态、恢复和人工接管时间；越权外发、资金错误、删除和生产变更为非补偿硬失败，不进入普通错误预算。成本看板必须分离预防性人工复核与事故补救成本。

---

## 15. Go / No-Go

### Go

- [ ] C06/C07/C09/C14/C16/C20/C22 正式接口已绑定，provisional 字段已消除或显式保留；
- [ ] 观测事件信封、native adapter、版本与迁移策略齐全；
- [ ] 任一看板指标可下钻到 task/run/artifact/incident，且访问受控；
- [ ] SLI 有对象、分母、测量点、窗口、阈值、owner 与越线动作；
- [ ] 平均值、尾部、样本数、UNKNOWN、excluded 和观测缺口同时可见；
- [ ] 成本覆盖模型、工具、基础设施、人工、失败、延迟，且估算/实际分离；
- [ ] retry/cancel/timeout/idempotency/compensation/reconciliation 语义可执行；
- [ ] 三类主要故障与重启恢复在无害环境实跑，证据可重放；
- [ ] 内容捕获、redaction、retention、access、dropped signals 经过 C22 审查；
- [ ] 事故进入 C07/C08/C18/C24 的可追溯回流链。

### No-Go

- 以 transport、model、scheduler、process 或 UI 状态单独宣称业务完成；
- 看板没有分母、样本量、时间窗、尾部或 UNKNOWN；
- 无限重试、非幂等高危动作自动重试、取消未确认却报停止；
- 用 token 标价冒充总成本，或隐藏人工与失败浪费；
- 默认导出敏感输入输出，或 observability 后端成为新的跨租户泄露面；
- dropped observations 不可见，仍将零记录解释为零故障；
- 事故恢复只验证进程/文件，不验证交付、副作用和环境终态；
- 将 OpenClaw/Hermes 动态文档、OpenTelemetry 开发字段或 Muse 厂商陈述写成永久行业事实。

---

## 16. 交付判定

本研究包已覆盖 C23 八个正文节点、稳定事件信封、六类证据载体、SLI/SLO/错误预算、全成本、可靠重试与取消、容量与尾部、三平台版本化镜面、仿生边界、三件母产物、两项练习、十八故障场景、二十六失败和十八红队。

当前结论：**可供正式作者消费，但 C23 仍为 `REVIEW_REQUIRED`**。上游正式接口、真实平台 mapping、故障注入、观测隐私审查与独立四门审校完成前，不得升级为正式章节或生产保证。

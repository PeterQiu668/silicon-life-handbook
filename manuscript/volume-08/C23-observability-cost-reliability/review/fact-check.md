---
review_id: C20-independent-fact-check-20260930
chapter_id: C20
review_type: independent_fact_check
reviewer_role: non_author_fact_reviewer
verified_on: "2026-09-30"
chapter_status: drafting
fact_gate: REVIEW_REQUIRED
cross_gate: separate_record
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C20 独立事实核查

## 裁决

**事实门：`REVIEW_REQUIRED`。** 36/36 条 claim 在正文与 ledger 双向闭合，missing=0、orphan=0；18/18 个外部 URL 最终 HTTP 200。OpenClaw `v2026.9.6 / eb377ac…`、Hermes `0.20.1 / f80f453…` 固定身份可复核；OpenTelemetry/SRE、Hermes dynamic 和 Muse `VENDOR-CLAIM` 的层级总体正确，正文没有把 dashboard、trace、health 或厂商界面当作业务完成证明。

事实门仍有两个阻断：E-C20-031 的项目状态已过时——C17 已完成 v3.1 第三轮非作者交叉复核但仍为 `REVIEW_REQUIRED`，C19 也已有独立 fact/cross 记录且两门均为 `REVIEW_REQUIRED`，不再是“待复验/仅作者包”；E-C20-036 声称夹具从原始事件与终态推导，但黑盒突变证明多个终态、policy、receipt、readback、digest 和 recovery 只是未锚定自报值，矛盾状态仍可 PASS。保存分布与 digest 是事实，控制有效性不是。

本记录没有修改正文、ledger、母产物、练习或作者 runs；运行语义由 [交叉审校](cross-review.md) 单独裁决，不批准实践、编辑、总编或 RC。

## 1. 证据闭合和来源身份

- source 共 33 个：本地/本书来源 15 个、外部来源 18 个；29/33 被 claim 消费。
- 未被 claim 消费的来源：`TERMS`、`OPENAI-EVAL`、`OPENAI-TRACE`、`ANTHROPIC-EVAL`。正文提到后三者，但没有 evidence ID 绑定。
- 36 个 evidence ID 全部唯一；正文引用 36/36，missing=0、orphan=0。
- 18/18 外部 URL 最终为 HTTP 200。
- OpenClaw annotated tag `v2026.9.6` 解引用至 `eb377ac59e6c9fd6c7705028034812becf00271b`。
- Hermes annotated tag `v2026.8.13` 解引用至 `f80f453ae0679347e38abc917c7f94f717bf96c5`，包版本 0.20.1。
- OpenTelemetry ledger 标记 1.44.0，但 URL 为当前规范页，不是固定 tag；正文已经把字段稳定度和 adapter 版本写成动态边界，因此可作为核验日快照，不能作为永久固定身份。

## 2. 36 条 claim 逐项裁决

| Evidence | 裁决 | 核查摘要 |
| --- | --- | --- |
| E-C20-001 | PASS AS METHODOLOGY | SLI 从承诺、分母、good/bad event 和测量点定义，与 SRE 指导一致。 |
| E-C20-002 | PASS AS METHODOLOGY | SLO、错误预算、窗口、owner 与越线动作边界清楚。 |
| E-C20-003 | PASS | 质量标准、D22/C19 均支持安全硬失败不进入普通错误预算。 |
| E-C20-004 | PASS | D21 技术执行、交付可见、业务/环境验收三层表述准确。 |
| E-C20-005 | PASS | 正文明确 200、exit 0、scheduler completed、模型自报、进程健康均不能单独推出完成。 |
| E-C20-006 | PASS AS METHODOLOGY | 八段事件链属于本章稳定观测方法，没有冒充平台原生字段。 |
| E-C20-007 | PASS | metric/trace/log/audit/artifact/decision record 职责分离合理。 |
| E-C20-008 | PASS | 稳定对象关系与动态 OTel 字段分层，正文没有固化快速演进字段。 |
| E-C20-009 | PASS WITH DYNAMIC-SOURCE LIMITATION | OTel 各部分稳定度不同、GenAI 内容敏感成立；1.44.0 身份来自核验日快照，URL 未固定版本。 |
| E-C20-010 | PASS | OTel recording errors 支持 span/metric 错误类型一致；正文没有外推为恢复证明。 |
| E-C20-011 | PASS | 内容最小化、采样/队列/series 丢弃可见得到 OTel/OpenClaw 固定文档支持。 |
| E-C20-012 | PASS AS METHODOLOGY | 高基数 ID 下钻、低基数 metric label 是合理治理原则。 |
| E-C20-013 | PASS AS METHODOLOGY | 全成本口径包含模型、工具、基础设施、人工、失败、延迟与机会成本。 |
| E-C20-014 | PASS AS METHODOLOGY | attempt、accepted task、失败浪费和人工分钟并列报告，未伪装为外部标准。 |
| E-C20-015 | PASS | 平均值不能隐藏尾部、UNKNOWN 与样本量，符合质量标准。 |
| E-C20-016 | PASS | timeout、cancel、停止与 effect 回滚分离，与 C06/C11/C13/C17 一致。 |
| E-C20-017 | PASS AS METHODOLOGY | 重试分类、同幂等键、上限、退避、jitter、预算和对账边界正确。 |
| E-C20-018 | PASS AS METHODOLOGY | UNKNOWN effect 先按原 ID 查询，不盲重试，边界正确。 |
| E-C20-019 | PASS | 降级不得扩权、放松安全硬门或隐藏新鲜度。 |
| E-C20-020 | PASS AS METHODOLOGY | arrival/admission/queue/concurrency/service/saturation/retry/acceptance 联合观测合理。 |
| E-C20-021 | PASS | Queue age/depth 与 retry 资源限制得到 SRE overload 指导支持。 |
| E-C20-022 | PASS | liveness/readiness/deep health 不证明单任务完成，正文边界正确。 |
| E-C20-023 | PASS | OpenClaw 固定 health contract 支持 detect/repair 分离和 repair 后重检。 |
| E-C20-024 | PASS | 固定 OpenClaw 文档区分 audit/logging/diagnostics/telemetry，并称 audit 为 metadata-only、bounded、best-effort、非无损合规档案。 |
| E-C20-025 | PASS | 固定 Prometheus 文档列出 run/model/tool/message/delivery/queue/cost 聚合与 series/async queue drop 信号。 |
| E-C20-026 | PASS | 固定日志文档支持结构化日志、级别、轮转和 redaction 边界。 |
| E-C20-027 | PASS | Hermes 固定 session storage 文档支持 state.db、session/message/token/cost/usage 与 lineage；正文没有称其不可篡改。 |
| E-C20-028 | PASS | Hermes 固定 cron 文档明确 claimed/running、completed/failed/unknown，abandoned unknown 不自动重跑。 |
| E-C20-029 | PASS | Dashboard 被限定为聚合表面；动态 cron 页与固定提交分栏。 |
| E-C20-030 | PASS | Muse Activity/Artifacts/permissions 全部保持 `VENDOR-CLAIM`，没有推断内部 telemetry/SLO。 |
| E-C20-031 | REVIEW_REQUIRED | “C17 待 post-fix 独立复验、C19 仅作者包”已过时；两章已有独立审校，但仍各自受限。 |
| E-C20-032 | PASS | D22 严格四层，security/red-team 横切非补偿，正文正确。 |
| E-C20-033 | PASS AS METHODOLOGY | 事故回流只形成候选，不自动修改生产、权限或 grader。D20 五类漂移引用正确。 |
| E-C20-034 | PASS | 包中恰好三件母产物。 |
| E-C20-035 | PASS AS SAVED-RUN FACT | 保存结果确为 24 trial、4 PASS/16 FAIL/4 RR，声明真实层0和外部副作用0；不证明 runner 会强制这些边界。 |
| E-C20-036 | REVIEW_REQUIRED | 双运行 digest 确定，但“从原始事件、终态、队列、成本和恢复状态推导”被黑盒反例推翻：自报终态、伪 receipt、伪 policy 和错误 digest 仍可 PASS。 |

## 3. 平台和标准边界

| 对象 | 身份与使用方式 | 裁决 |
| --- | --- | --- |
| OpenClaw fixed | `eb377ac…` observability、Prometheus、logging、health | PASS |
| Hermes fixed | `f80f453…` session DB、cron ledger、dashboard | PASS |
| Hermes dynamic | 当前 cron 文档，仅作变化实现镜面 | PASS WITH DYNAMIC LIMITATION |
| OpenTelemetry | 当前规范快照；稳定度逐字段/信号解释 | PASS WITH VERSION LIMITATION |
| Google SRE | 官方工程指导，不提供通用阈值 | PASS |
| Muse | Meta 产品公开材料 | PASS AS VENDOR-CLAIM |
| OpenAI/Anthropic | 正文方法论启发，但未绑定 claim | P2 EVIDENCE HYGIENE |

## 4. D20、D21、D22 与 MAT/AU

- **D20：PASS。** 正文将能力、人格、文档、工具、目标五类漂移交回 C15，不新增第六类。
- **D21：正文 PASS，运行证据 FAIL。** 正文稳定地区分三层；作者 runner 允许三层全部失败仍 PASS，详见交叉门。
- **D22：正文 PASS，运行证据 FAIL。** 正文只承认四层并将安全设为横切；runner 接受第五层和 synthetic 冒充 real-world。
- **MAT/AU：PASS。** 本章没有用成熟度推导权限，也没有裸 `Lx` 混用；扩大自主性只作为错误预算耗尽后的治理对象，不自定义 AU/MAT 阈值。

## 5. P0/P1/P2 与关闭条件

### P0

事实来源层没有发现伪固定提交、Muse 内部实现外推或 36 条 claim 断链。运行控制 P0 见交叉审校。

### P1

- **P1-F20-01｜E-C20-031 项目状态过时。** 分别写明：C17 v3.1 第三轮交叉仍 RR，阻断为 capability digest 权威锚点，practice RR；C19 fact/cross 均 RR，practice 未审。保持 provisional/limited，但不能说“待复验/仅作者包”。同步 frontmatter、正文、ledger、self-check 和交接。
- **P1-F20-02｜E-C20-036 效果主张超界。** 改为“给定预置 24 场景的 runner 可确定性重放”；只有修复并通过独立负突变后，才能恢复 closed-world、权威终态和原始状态推导主张。

### P2

- **P2-F20-01｜四个 unused source。** `OPENAI-EVAL`、`OPENAI-TRACE`、`ANTHROPIC-EVAL` 在正文出现但不属于任何 evidence claim；新增清晰的方法论 claim 或删除未消费 source。`TERMS` 同样需绑定或删除。
- **P2-F20-02｜OTel 版本身份。** 若保留“1.44.0”精确版本，建议引用对应 release/tag；若继续使用 current URL，则标题改为动态规范并记录 verified_on。

## 6. 保留未知

- 未运行真实 OpenClaw/Hermes/Muse、OTel collector、Prometheus、Queue、provider、渠道、计费系统或目标环境。
- 未验证真实内容 redaction、series/drop、receipt/readback、成本账单、跨重启租约或事故恢复效果。
- C17/C19 仍为受限上游，状态变化后须回归 adapter、authority、effect、audit 与 incident 接口。

## 7. 门禁结论

- 事实门：`REVIEW_REQUIRED`。
- 关闭条件：关闭 P1-F20-01/02，重新跑 36/36 闭合、18 个外链、固定提交、YAML/frontmatter 和两个 validator。
- 实践门：`not_reviewed`。
- 编辑门、总编门、RC：`not_reviewed / not_authorized`。

复现、哈希和黑盒突变见 [independent-fact-cross-reproduction-20260930.yaml](runs/independent-fact-cross-reproduction-20260930.yaml)。

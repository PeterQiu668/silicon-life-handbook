---
review_id: C13-independent-fact-check-20260930
chapter_id: C13
review_type: independent-fact-check
reviewed_on: "2026-09-30"
reviewer_role: evidence-reviewer
chapter_status: drafting
fact_gate: review_required
cross_gate: separate_record
practice_gate: not_reviewed
editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C13 独立事实核查

## 1. 裁决

C13 的证据结构基本闭合：27 条 claim 全部被正文引用，35 个 source 全部被 claim 消费，21 个本地来源均存在，14 个外部一手页面均可访问；OpenClaw 与 Hermes 的 release/tag 身份已重新解引用，Muse 全部保持为 `VENDOR-CLAIM`。作者保存的 30-trial 结果也与固定输入和 runner 按字节复现一致。

事实门暂判 **`REVIEW_REQUIRED`**，不是因为核心工程结论错误，而是 E-C13-014 存在一处必须消歧的 P1：OpenClaw 固定文档把 Standing Orders 称为授予 `permanent operating authority` 的产品机制，而 claim 和正文把“在 OpenClaw 中……不是永久授权”写成近似产品事实。本书完全可以、也应该采用更严格的治理裁决——持续意图不得成为无限、不可撤销或脱离 C14 当前核验的授权——但必须把“厂商术语”与“本书规范”并列说清，不能让同一来源同时证明相反字面命题。

除 E-C13-014 外，其余 26 条 claim 均为 `PASS`。本结论不执行独立实践门，不证明真实 OpenClaw/Hermes/Muse 调度、投递、停止或恢复，不批准编辑门、总编门或 `release_candidate`。

## 2. 核查范围与方法

- 对 27 条 claim 逐项核对身份、source、正文引用、稳定性与限制；
- 对 35 个 source 逐项检查存在性或可达性，并对关键外部页面核对实际语义，不以 HTTP 200 代替内容支持；
- 通过 GitHub 官方 API 解引用 annotated tag，确认 OpenClaw `v2026.9.6 → eb377ac...`、Hermes `v2026.8.13 → f80f453...`；
- 对作者固定输入、runner、结果和摘要做 fresh `/tmp` 只读复跑，只用于核实 E-C13-025/026，不构成两项练习的独立实践签核；
- 对方法论、固定版本事实、动态官方页面、厂商声明、本地合成验证分别裁决，不做跨身份升级。

详细逐源与逐 claim 记录见 [source-audit-20260930.yaml](source-audit-20260930.yaml)。

## 3. 27 条 claim 逐项结论

| Evidence | 身份 | 结论 | 核查摘要 |
| --- | --- | --- | --- |
| E-C13-001 | METHODOLOGY | PASS | 受控主动性以信号价值、目标、权限和安静策略约束，未写成产品算法。 |
| E-C13-002 | METHODOLOGY | PASS | 触发、授权、净价值三道门分开；安全与授权硬失败非补偿。 |
| E-C13-003 | METHODOLOGY | PASS | `trigger ≠ authority ≠ completion` 与 C06、C09、D21 一致。 |
| E-C13-004 | METHODOLOGY | PASS | Heartbeat/Cron/Event/Queue/Hook/Webhook/Manual/Standing Order 职责清楚，复合自动化逐项治理。 |
| E-C13-005 | METHODOLOGY | PASS | 有证据静默与失明、遗漏、高严重度升级明确分开。 |
| E-C13-006 | METHODOLOGY | PASS | 去重、重放防护、合并、冷却、静默时段和暂停没有压成单一 throttle。 |
| E-C13-007 | METHODOLOGY | PASS | IANA 时区、DST、misfire、catch-up 等明确是可迁移字段，不冒充统一平台 schema。 |
| E-C13-008 | METHODOLOGY | PASS | 原始 `UNKNOWN` 保留为证据状态，最终只补证、FAIL 或 RR；副作用未知禁止盲重放。 |
| E-C13-009 | METHODOLOGY | PASS | 技术执行、交付可见、业务/环境验收采用 D21 三层，单一 success 不足以完成。 |
| E-C13-010 | METHODOLOGY | PASS | stop request/confirmation、pause/cancel、circuit/recovery 分离，重启不等于恢复。 |
| E-C13-011 | METHODOLOGY | PASS | sentinel 独立故障域约束清楚，风险分级仍留给 C19—C21。 |
| E-C13-012 | METHODOLOGY | PASS | Webhook 的来源、签名、时间窗、tenant、重放、队列和权威回读边界完整。 |
| E-C13-013 | METHODOLOGY + VERSION-FACT | PASS | 固定 Hooks 文档支持 Gateway 生命周期回调、共享宿主能力及“发现不等于加载/触发”。 |
| E-C13-014 | METHODOLOGY + VERSION-FACT | **REVIEW_REQUIRED** | 方法裁决正确，但正文未显式呈现 OpenClaw 官方 `permanent operating authority` 术语，导致产品事实与本书更严格规范在字面上冲突。 |
| E-C13-015 | VERSION-FACT | PASS | 固定 Heartbeat 文档明确其为 system-owned automation，指令进入 system-owned monitor scratch。 |
| E-C13-016 | VERSION-FACT | PASS | 固定 retired template 明确 `HEARTBEAT.md` 已退役，Runtime 不再读取。 |
| E-C13-017 | VERSION-FACT | PASS | 固定 automation 文档区分 scheduled jobs、Heartbeat、Hooks、Webhooks 和 Standing Orders。 |
| E-C13-018 | DYNAMIC-OFFICIAL | PASS | Hermes `0.20.1/v2026.8.13` 只作 release 锚点，动态 Cron/heartbeat 页面带核验日，未倒填。 |
| E-C13-019 | DYNAMIC-OFFICIAL | PASS | 动态页面支持 provider trigger 与 execution/delivery 分离、claim、misfire/catch-up、session heartbeat。 |
| E-C13-020 | VENDOR-CLAIM | PASS | Muse 后台工作、价值过滤、通知、主动性和批准控制只写成厂商公开主张。 |
| E-C13-021 | METHODOLOGY | PASS | 有效提案、噪音、遗漏、延迟、升级、完整交付和故障隔离均明确为 C13 局部指标。 |
| E-C13-022 | METHODOLOGY | PASS | 程序性反馈只能形成训练候选，不能在线修改 Standing Order、授权或策略。 |
| E-C13-023 | METHODOLOGY | PASS | v2、章节卡和 D18 一致要求恰好三件母产物。 |
| E-C13-024 | METHODOLOGY | PASS | 向 C14/C19/C20/C21/C22 输出字段，定义权仍由下游持有。 |
| E-C13-025 | LOCAL-VALIDATION | PASS IN DECLARED SCOPE | 30 个唯一 task/trial；18 PASS、6 FAIL、6 RR；三触发各 6/2/2；外部副作用为零。 |
| E-C13-026 | LOCAL-VALIDATION | PASS IN DECLARED SCOPE | 保存结果和 runner 支持有证据静默 PASS、共享故障域 FAIL、UNKNOWN→RR；仍待独立实践。 |
| E-C13-027 | METHODOLOGY | PASS | D22 严格四层，security/red-team 为横切非补偿切片，不是第五层。 |

## 4. 平台事实边界

### 4.1 OpenClaw 固定版

- 官方 release `v2026.9.6` 的 annotated tag 已解引用到 `eb377ac59e6c9fd6c7705028034812becf00271b`；
- [Heartbeat 固定文档](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/heartbeat.md)支持 system-owned automation、scheduler-owned cadence 与 monitor scratch；
- [退役模板](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/reference/templates/HEARTBEAT.md)明确 `HEARTBEAT.md` 不再创建或运行时读取；
- [Automation 概览](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/automation/index.md)与固定 Cron/Hooks/Standing Orders 页面支持机制分离；
- 这些文档不证明用户本机已经迁移、真实 trigger 已发生、通知已送达或环境已恢复。

结论：除 Standing Order 术语消歧项外为 `PASS`；目标部署行为继续 `REVIEW_REQUIRED`。

### 4.2 Hermes 固定与动态

- 官方 release 名称为 Hermes Agent `v0.20.1 (v2026.8.13)`，annotated tag 指向 `f80f453ae0679347e38abc917c7f94f717bf96c5`；
- [Scheduled Tasks](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron/)、[Cron Internals](https://hermes-agent.nousresearch.com/docs/developer-guide/cron-internals)与 [Session Heartbeats](https://hermes-agent.nousresearch.com/docs/user-guide/features/heartbeat)均按 2026-09-30 动态官方页面引用；
- 正文没有把动态页面的 claim、provider、misfire/catch-up、delivery 或 heartbeat 逐项倒填为 `0.20.1` 固定实现。

结论：`PASS WITH DYNAMIC RECHECK TRIGGER`。固定源码逐项对照和目标实机继续 `REVIEW_REQUIRED`。

### 4.3 Muse

Meta 公开材料支持“后台工作、价值过滤、意义变化通知、主动性控制、结构化批准、Sentinel 独立权限裁决面”等厂商陈述。正文没有为 Muse 构造 Cron、队列、状态机、遗漏率或独立安全效果，且明确不能用 Muse 填可执行字段。

结论：`PASS AS VENDOR-CLAIM`；内部机制和效果保持 `UNKNOWN`。

## 5. 30-trial 保存结果核验

作者结果的静态与 fresh 临时复跑一致：

```text
trials: 30
task ids unique: true
trial ids unique: true
distribution: PASS 18 / FAIL 6 / REVIEW_REQUIRED 6
scheduled/event/manual: each PASS 6 / FAIL 2 / REVIEW_REQUIRED 2
external side effects: 0
raw UNKNOWN -> REVIEW_REQUIRED: true
shared unique fault domain -> never PASS: true
result SHA-256: 0508a416206f2f6356177279a16478296e03675e5cf84507efa91d76584b86be
summary SHA-256: 0c20d80bd12b7f6b5f5f6b01f5f5a574017b045331264e67a2de1ced1d3685f6
```

这只核对 E-C13-025/026 的可重复性，不等于独立执行 X-C13-01/02，也不证明真实 scheduler、channel、stop、read-back、sentinel 或 recovery。

## 6. 问题分级

### P0

无。未发现把 trigger 当 authority、用单一 success 冒充 completion、把 Muse 写成固定实现、删除失败样本、把 security 当第五数据层或允许 UNKNOWN 盲重放的问题。

### P1

1. **P1-F13-01 / E-C13-014 术语身份冲突，阻断事实门。** 固定 OpenClaw 文档确实使用 `permanent operating authority`；当前正文“在 OpenClaw 中……不是永久授权”没有先披露该厂商术语。建议最小修补为：先准确转述厂商命名，再说明本书不接受其被解释为无限、不可撤销或免除 C14 重新核验的授权；source/claim 的限制栏同步区分 `VERSION-FACT` 与 `METHODOLOGY`。

### P2

1. **P2-F13-01 / 作者自检计数滞后。** `author-self-check.md` 的 P0-03 仍写“26 个主张”，当前 ledger 和正文实际为 27 个；不影响证据闭合，但应在下一次作者修订同步。

## 7. 事实门决定

```yaml
fact_gate:
  chapter_id: C13
  verdict: REVIEW_REQUIRED
  blocker: P1-F13-01
  claims_checked: 27
  claims_pass: 26
  claims_review_required: 1
  claims_fail: 0
  sources_checked: 35
  local_sources_present: 21
  external_sources_http_200: 14
  evidence_reference_closure: PASS
  author_run_claim_integrity: PASS_IN_DECLARED_SCOPE
  independent_practice_performed: false
  practice_approved: false
  editor_approved: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```


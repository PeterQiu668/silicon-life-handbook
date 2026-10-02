---
review_id: C16-v3-final-independent-fact-cross-practice-review-20260930
chapter_id: C16
review_type: final_stateful_non_author_narrow_review
reviewer_role: non_author_independent_reviewer
verified_on: "2026-09-30"
author_files_modified: false
historical_reviews_modified: false
fact_gate: PASS_WITH_LIMITATIONS
cross_gate: PASS_WITH_LIMITATIONS
synthetic_machine_control: PASS
synthetic_practice_reproduction: PASS
x_c16_01_offline_scope: PASS_WITH_LIMITATIONS
x_c16_02_offline_scope: PASS_WITH_LIMITATIONS
overall_practice_gate: REVIEW_REQUIRED
real_platform_practice: REVIEW_REQUIRED
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C16 v3 最终状态化修订独立窄复核

## 1. 裁决

本轮只新增本审查与 [机器可读复现记录](runs/v3-final-independent-organization-reproduction-20260930.yaml)，没有修改正文、证据账本、母产物、练习、作者 builder/runner/input/results/summary、README、作者自检、修订记录或历史审稿。

- **事实门：`PASS_WITH_LIMITATIONS`。** 25/25 claim 与正文双向闭合，22/22 source 被消费；正文、ledger、自检、README 与冻结件对 15 task、45 trial、`12 PASS / 27 FAIL / 6 REVIEW_REQUIRED`、真实层 0、四个 shadow 场景共 12 trial、effect 0 的表达一致。OpenClaw/Hermes/Muse/A2A 事实身份没有在本次状态化修订中漂移。
- **交叉门：`PASS_WITH_LIMITATIONS`。** D21 三层终态、D22 四层与横切 security、C17 并发/取消定义权和 C18 A2A/信任定义权仍保持边界；状态机没有把合成 shadow 写成真实层，也没有用安全失败的平均收益补偿硬失败。
- **离线合成机器控制与复现：`PASS`。** fresh-temp 双重建逐字节一致；38/38 个不依赖作者 `expected` 或 case 名的独立近邻测试符合预期。前次 P1-C16-PF-01—06 全部关闭，未发现新的 P0/P1。
- **两项练习的离线合同：`PASS_WITH_LIMITATIONS`。** 单体/组织公平比较、同源共识、身份授权、共享写、预算停止、取消、D21 三证、effect 和降级路径均已在安全合成副本中复现。
- **章节总实践门：`REVIEW_REQUIRED`。** 代表性真实层为 0；真实 OpenClaw/Hermes/A2A、生产身份/授权、真实并发写、停止/取消传播、环境终态、真实凭证和长期净收益均未运行。本记录不批准编辑门、总编门或 RC。

## 2. 冻结快照与 fresh-temp 双重建

两个全新临时目录分别只复制当前 builder 与 runner，由 builder 重建 input，再由 runner 生成 results 与 summary。A、B、作者保存件三者逐字节一致：

| 对象 | SHA-256 |
| --- | --- |
| builder | `5d06b85b63aa1537a3d0511a162726e41b104d82fdd6f863b38f8d5f597b7110` |
| runner | `e779f28014ce4341c59a6fcd724bef1d861e5958ad7bcbb7bfbc3afdddcaedee` |
| input | `e9752e4e93d9a386648609243a0dbfc39b7b6d56c8a2694038f0f180705a232a` |
| results | `249b9ab98d4447e7b3bd621c4546a97c277ea3c8b0c9f38009cf812b0e43129b` |
| summary | `59d406d7fd5caeadb4c26e553aa4370a19a456dce9aa16d196f14a73c756177c` |

冻结不变量：15 个 task、45 个全局唯一 trial、12 PASS、27 FAIL、6 REVIEW_REQUIRED；四个 synthetic-shadow 场景共 12 trial；security/red-team 横切场景 3 个、共 9 trial；代表性真实层 0；确认外部 effect 0；trial、trace digest、evidence digest 与 evidence ID 均唯一；45/45 作者 oracle 匹配。

作者 oracle 匹配只用于确认保存件没有漂移，不作为本轮近邻裁决依据。

## 3. 独立测试方法

独立攻击直接调用当前 runner 的 `validate` 与 `decide`，固定选择一个原始可通过记录并按字段构造状态变体；裁决依据是变体输入、实际三态与实际 reason，不读取 scenario 的 `expected`，也不根据 case 名推断结果。需要测试“整个 CLI 是否 fail-closed”的畸形时间样本，则在 fresh temp 中运行完整命令并检查非零退出与结果文件不存在。

总计 38 项：38 符合预期、0 fail-open、0 未决。结构化逐项结果见复现 YAML。

## 4. 前次六组近邻缺口关闭

### P1-C16-PF-01：shadow 计数和作者状态一致——CLOSED

当前 input/results/summary、正文、ledger、自检、README 和修订记录均为四个 shadow 场景、12 trial；真实层为空、`representative_real_world_executed=false`。旧的“三个/9 trial”口径不再出现在当前作者状态文件中。

### P1-C16-PF-02：时间与 alias 独立性——CLOSED

- `now` 畸形、无时区均被 schema 拒绝；grant expiry 畸形被拒绝。
- action request 的畸形 `requested_at` 在 `decide` 入口解析，完整 CLI 非零退出且不产生 output，未形成 PASS。解析发生在决策阶段而非 schema 阶段，是阶段差异，不是 fail-open。
- 两个 alias 指向同一 principal 被一对一约束拒绝，不能用身份折叠掩盖共享凭证。

### P1-C16-PF-03：writer 与 FACT 来源——CLOSED

- 未知 lease writer 和未知 event writer 均为 `FAIL / writer_identity_unresolved`。
- 同 object、同 base、不同 writer 即使写出完全相同的 result version，只要没有 merge record，仍为 `FAIL / unmerged_shared_write_conflict`。
- `minimum_independent_origins=0` 被“必须为正”拒绝；FACT 的值为 1 被“至少两个来源”拒绝；两个不同 origin 可 PASS，两个引用但同一 origin 为 FAIL。

### P1-C16-PF-04：预算停止与取消回执——CLOSED

- `consumed == stop_threshold` 或越过 threshold、receipt=`NONE` 均 FAIL；receipt=`VERIFIED` 但工作未停止仍 FAIL。
- 只有达到 threshold、receipt=`VERIFIED` 且 `all_work_stopped=true` 才能继续；一旦越过硬 limit，即使有 verified receipt 仍 FAIL。
- cancel 已请求而 receipt=`NONE`、child 已取消且两面读回 clear，仍只能 `REVIEW_REQUIRED / cancel_receipt_missing`，不能 PASS。

### P1-C16-PF-05：D21 evidence 与 effect 三态——CLOSED

- evidence `FAILED` → FAIL；`UNKNOWN` → REVIEW_REQUIRED。
- effect `FAILED` → FAIL；`UNKNOWN` 或 `PENDING` → REVIEW_REQUIRED。
- D21 technical FAILED、delivery MISSING、business REJECTED 均使“报告完成”的任务 FAIL；任一终态 UNKNOWN 最高为 REVIEW_REQUIRED。
- 确认外部写而环境合同不允许时为硬 FAIL，并派生 effect count 1；冻结包自身仍为 0。

### P1-C16-PF-06：全局 evidence ID 唯一性——CLOSED

将第二个 run 的 evidence ID 改成首个 run 的 ID，即使 run ID 与 evidence digest 仍不同，也会在产生结果前被 `evidence ids must be globally unique across runs` 拒绝。

## 5. 硬失败非补偿、D21 与 D22

三组组合攻击验证优先级：未知 writer + evidence UNKNOWN、越过预算硬上限 + cancel UNKNOWN、同源 FACT + effect UNKNOWN，实际裁决均为 FAIL；后出现的 REVIEW_REQUIRED 条件不能补偿先前硬失败。

D21 的技术执行、交付可见、业务验收继续分开，模型自报或组织平均分不能替代三层终态。D22 仍只有 `training / regression / holdout / representative_real_world` 四层；把 executed 改 true 但保持真实层 0、让 synthetic 场景冒充真实层、或使用第五层 `security` 均在结果生成前拒绝。security/red-team 只作为横切非补偿切片。

当前四个 shadow 场景是未来真实层候选，不是代表性真实运行。`representative_real_world_trial_count=0`、`external_effect_count=0` 是本次合成实践的硬边界，也是总实践门不能通过的直接原因。

## 6. 事实、结构与状态一致性

- 正文 frontmatter 为 `drafting / unapproved / self_approval=false`，正式依赖仍为 `[C03,C04,C06,C09,C14]`。
- 正文只有 16.1—16.7，恰好三件母产物、两项练习。
- 25/25 evidence ID 唯一，正文引用 missing=0、orphan=0；22/22 source 被消费。
- 当前作者文件哈希与本轮结束时重新计算一致；本审查没有改写作者文件。
- README、作者自检、stateful remediation 对冻结 hash、计数、shadow 口径和真实边界一致。

## 7. 最终门禁与保留边界

```yaml
independent_gate_decision:
  author_snapshot_unchanged: PASS
  fresh_temp_double_rebuild: PASS
  frozen_trials: 45
  frozen_distribution: {PASS: 12, FAIL: 27, REVIEW_REQUIRED: 6}
  independent_near_neighbor_tests: 38/38
  previous_P1_PF_01_to_06: CLOSED
  new_P0: 0
  new_P1: 0
  d21_terminal_and_evidence: PASS
  d22_four_layers_and_cross_cutting_security: PASS
  hard_failure_noncompensation: PASS
  fact_gate: PASS_WITH_LIMITATIONS
  cross_gate: PASS_WITH_LIMITATIONS
  synthetic_machine_control: PASS
  synthetic_practice_reproduction: PASS
  x_c16_01_offline_scope: PASS_WITH_LIMITATIONS
  x_c16_02_offline_scope: PASS_WITH_LIMITATIONS
  overall_practice_gate: REVIEW_REQUIRED
  real_platform_practice: REVIEW_REQUIRED
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

保留限制不是合成控制缺陷：真实 OpenClaw/Hermes/A2A Runtime、生产授权与凭证、真实并发写、停止与取消传播、真实环境 read-back、代表性真实任务和长期净收益均未运行。只有这些外部实践完成并由独立人员复核后，章节总实践门才可重新评估。


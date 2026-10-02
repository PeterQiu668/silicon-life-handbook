---
review_id: C16-post-fix-independent-practice-review-20260930
chapter_id: C16
review_type: post_fix_independent_practice_narrow_review
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
builder_reproduction: PASS
frozen_v3_reproduction: PASS
fairness_contract_control: PASS
old_boolean_rejection: PASS
core_state_derivation: PASS_WITH_GAPS
net_benefit_control: PASS
d22_manifest_control: PASS
synthetic_machine_control: FAIL
x_c16_01: REVIEW_REQUIRED
x_c16_02: REVIEW_REQUIRED
overall_practice_gate: REVIEW_REQUIRED
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C16 v3 状态化修补后独立实践窄复核

## 1. 裁决

**builder 与冻结 v3 双 fresh-temp 复现 `PASS`；公平合同、旧预裁决布尔拒绝、主要身份授权、共享写、同源 FACT、净收益、D22 manifest、effect 计数与硬失败非补偿均有实质改善；但当前 synthetic machine-control 仍为 `FAIL`，X-C16-01、X-C16-02 与真实平台总实践门继续 `REVIEW_REQUIRED`。**

本轮发现六组仍可触发 PASS 的边界缺口：时间字符串不解析、alias collision 可掩盖共享凭证、未知 writer 与同 base/同 result 的未合并双写、FACT 允许零独立来源、到达 stop threshold 或 cancel 已请求但没有 receipt 仍 PASS、D21 evidence/status 与 effect UNKNOWN 未进入裁决、跨 run 重复 evidence ID 未拒绝。另有一项作者记录与当前文件直接冲突：remediation note 声称 synthetic shadow 为 9、README 称三个场景，当前 input/results 实际为 12、四个场景。

结构化证据见 [post-fix-independent-organization-reproduction-20260930.yaml](runs/post-fix-independent-organization-reproduction-20260930.yaml)。本轮没有修改作者 input、runner、results、summary、README、builder、remediation note、正文、ledger、产物或练习。

## 2. 双 fresh-temp 与源文件哈希

| 对象 | SHA-256 |
| --- | --- |
| input | `e9752e4e93d9a386648609243a0dbfc39b7b6d56c8a2694038f0f180705a232a` |
| runner | `7778722f37317ee67f68f0df194b9ee3e02ef0f9533f9f0dcc1ed8383bc93f37` |
| builder | `5d06b85b63aa1537a3d0511a162726e41b104d82fdd6f863b38f8d5f597b7110` |
| 作者 results | `3a2724a51a2f8b84fda1184b9a8cb33622bb30d00bf852e9e13c2a6ac41fcf6c` |
| 作者 summary | `59d406d7fd5caeadb4c26e553aa4370a19a456dce9aa16d196f14a73c756177c` |
| README | `1160bc2196f09da68eda3d8f2fe33882993098b9fad3a68222cb36e6fa9fa01d` |
| remediation note | `e1c12ef6736840a268e6b3c1700cb9e25afe18504847a87ea9f936518638bb9f` |

两个 fresh temp 都从 builder 重建 input，再运行 runner。两份重建 input 与作者 input 逐字节同哈希，两份 results/summary 也逐字节一致并等于作者保存文件。

实际冻结不变量：45 trial、15 task、`12 PASS / 27 FAIL / 6 REVIEW_REQUIRED`、真实层 0、effect 0、trial/run ID、trace digest、evidence digest 均被报告为唯一。**实际 synthetic shadow 是 12，不是任务与 remediation note 要求的 9。** 当前四个 shadow scenario 是 `multi-negative-benefit`、`lead-lost`、`a2a-runtime-unverified`、`rollback-to-single`；README 的“三个未来面向真实层场景”与输入不一致。

## 3. 首轮 31 项回归的关闭情况

### 已关闭

- 比较合同七字段中任一失配，全部 trial 只能成为 `REVIEW_REQUIRED`，不再 PASS。
- 旧 `unauthorized_action`、`shared_write_conflict_uncontrolled`、`correlated_consensus_claimed_fact`、`ghost_success`、`budget_exceeded_without_stop`、`cancel_leak`、`shared_credential`、`actual_external_effect` 字段均被 closed-world schema 拒绝。
- unknown alias、revoked/expired grant、action/object/scope 不匹配、credential owner/存在性不匹配均从状态得到 FAIL。
- 两个 active writer、同 base 产生不同 result 且无 merge、同源 FACT、超预算未停、cancel active child/rejected/residual、D21 三层 FAILED/UNKNOWN、外部写、100 倍成本/延迟与微小质量增益均得到正确 FAIL/RR。
- 不足 run、重复 run、原样重复 trace/evidence、未知字段/enum、错类型均被拒绝。
- synthetic 冒充真实层、缺失或错配 manifest 均被拒绝；合法 manifest 产生 3 个真实层 trial。
- disallowed APPLIED 外部写得到 FAIL 且 effect count=3；allowed 时 count 仍为 3，不再出现 FAIL 与 zero=true 并存。
- revoked grant、double writer、budget hard failure 与 terminal/cancel UNKNOWN 组合时，硬失败仍为 FAIL。

### 尚未关闭

首轮“独立 trial/evidence”只部分关闭；此外，更精细的状态边界暴露了以下新缺口。

## 4. 开放 P1

### P1-C16-PF-01：冻结 shadow 数与作者声明不一致

当前 results、summary 与 builder 一致地给出 12 个 shadow trial；remediation note 写 9，README 写三个 shadow scenario。本轮不能替作者决定 `rollback-to-single` 是否应保留为 shadow。最小合同是统一冻结口径：若目标为 9，则移除一个 scenario 的 shadow 标志并重生 input/results/summary；若目标为 12，则更正 remediation/README/验收口径并说明第四类迁移对象。两种选择都需非作者重跑。

### P1-C16-PF-02：身份时间与 alias 独立性仍可绕过

- grant `expires_at="not-a-time"` 是字符串且按字典序与 `requested_at` 比较，得到 PASS；没有 RFC3339 解析，也没有用固定 `now` 检查当前有效性。
- 把 `expert-b` alias 指向 `principal-lead` 后，lead/expert 同用 `cred-lead` 可 PASS；共享检查只看 principal 是否不同，不能发现两个组织角色被 alias collision 折叠成同一身份。

最小合同：严格解析 issued/request/expiry/now；明确授权是在 request 时还是 execution 时验证，并绑定执行时钟；为要求身份隔离的角色声明 distinct-principal 约束，alias collision 不得满足独立角色/凭证隔离。

### P1-C16-PF-03：单写者与独立来源边界不完整

- 两个不同 writer 在同一 object/base_version 上无 merge 写入同一个 result_version 时 PASS；当前冲突检测只统计不同 result version，而不是 writer/event 数。
- writer alias 不存在时映射为字符串 `UNKNOWN`，单个未知 writer 仍 PASS。
- FACT 的 `minimum_independent_origins=0` 且无来源时 PASS。

最小合同：writer lease/event 必须解引用已知 principal；同 object/base 上出现多个 writer 或多个未合并事件即 FAIL，与 result version 是否相同无关；FACT 最小独立来源必须为正整数，并验证 source ref 存在、状态与 origin 独立性。

### P1-C16-PF-04：stop threshold 与 cancel receipt 的终态门仍会早放行

- `consumed == stop_threshold`、receipt=`NONE`、work 未停，仍 PASS；只有 receipt=`UNKNOWN` 才 RR。
- `cancel.requested=true`、receipt=`NONE`，即使 child 都标取消且 readback clear，也 PASS。

最小合同：达到或越过 stop threshold 时必须存在 VERIFIED stop receipt 且 work stopped，否则 FAIL/RR；cancel requested 后 receipt 只能为 ACCEPTED/REJECTED/UNKNOWN，NONE 不能形成 PASS；receipt、children、queue、inflight 四面必须共同闭合。

### P1-C16-PF-05：D21 evidence 与 effect UNKNOWN 没有进入裁决

- 三层 terminal 均为成功时，把每个 run 的唯一 evidence record 改成 FAILED 或 UNKNOWN，仍 PASS。
- effect ledger 有 `status=UNKNOWN` 时，既不 FAIL 也不 RR，仍 PASS。

最小合同：D21 三层必须分别引用并校验 evidence record 的 kind/status/source/object digest/terminal binding；FAILED→FAIL，UNKNOWN→RR；effect UNKNOWN 必须对账，未确认前至少 RR，并继续让明确授权/安全硬失败优先。

### P1-C16-PF-06：evidence 唯一性可被重复 ID 绕过

把第二个 run 的 `evidence_id` 改成第一个 run 的 ID，同时保持各自 `run_id`，仍 PASS。当前 evidence digest 包含 run_id，因此同一个 evidence ID 被跨 run 重用时 digest 仍不同。类似地，当前三次 trace 的事件语义基本相同，唯一性主要来自 run_id。

最小合同：全局拒绝重复 evidence ID；独立性 digest 应区分 binding digest 与去除 run/record ID 后的 semantic digest；至少保留独立输入/随机种子/环境观察或差异化 trace，不得把换 ID 当成独立试次。

## 5. 关键正向和组合回归

| 控制 | 结果 |
| --- | --- |
| 合法 principal/grant/action/object/scope | PASS |
| 独立来源 FACT | PASS |
| 超预算但 verified stop + all stopped | PASS |
| 合法三层 terminal | PASS |
| 合法外部 effect 且环境允许 | PASS，count=3 |
| 合法 real-world manifest | PASS，真实层 trial=3 |
| tiny quality + 100× cost/latency + 10000 人工增量 | FAIL |
| revoked grant + terminal UNKNOWN | FAIL |
| double writer + cancel UNKNOWN | FAIL |
| budget hard failure + cancel UNKNOWN | FAIL |

这些结果说明 v3 已不是旧版布尔查表，主要控制确实从状态推导；开放问题集中在边界和证据绑定，而不是整套修补无效。

## 6. 门禁与真实平台边界

```yaml
post_fix_practice_gate:
  builder_reproduction: PASS
  frozen_v3_reproduction: PASS
  expected_distribution_12_27_6: PASS
  expected_task_count_15: PASS
  expected_real_world_count_0: PASS
  expected_effect_count_0: PASS
  expected_synthetic_shadow_count_9: FAIL_ACTUAL_12
  fairness_contract_control: PASS
  old_boolean_rejection: PASS
  principal_grant_credential_control: PASS_WITH_GAPS
  writer_source_budget_cancel_control: PASS_WITH_GAPS
  d21_effect_unknown_control: FAIL
  independent_run_evidence_control: FAIL
  net_benefit_control: PASS
  d22_manifest_control: PASS
  hard_failure_noncompensation: PASS
  synthetic_machine_control: FAIL
  x_c16_01: REVIEW_REQUIRED
  x_c16_02: REVIEW_REQUIRED
  real_openclaw_hermes_a2a_execution: NOT_RUN
  overall_practice_gate: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

即使后续关闭全部合成控制缺口，真实 OpenClaw/Hermes/A2A Runtime、生产身份/授权、真实并发写、取消传播、外部终态、代表性真实任务与生产降级/恢复仍未执行，因此章节总实践门仍必须保持 `REVIEW_REQUIRED`。

全部复现与突变在临时离线副本中完成，无网络、无真实凭证、无真实用户数据、无生产写；临时目录在证据提取后清理。

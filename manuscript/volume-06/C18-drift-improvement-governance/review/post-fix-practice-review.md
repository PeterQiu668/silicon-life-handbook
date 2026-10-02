---
review_id: C15-post-fix-independent-practice-review-20260930
chapter_id: C15
review_type: post-fix-independent-practice-gate
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
frozen_v3_1_fixture_reproduction: PASS
original_23_regression: PASS
rollback_approval_precedence: PASS
governance_recertification_reference_integrity: PASS
post_fix_synthetic_machine_control: PASS
machine_control_scope: v3_1_offline_stateful_synthetic_control
x_c15_01: REVIEW_REQUIRED
x_c15_02: REVIEW_REQUIRED
overall_practice_gate: REVIEW_REQUIRED
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C15 v3.1 状态化补强独立实践复核

## 1. 第二轮窄复核裁决

**v3.1 冻结夹具复现 `PASS`；原 23 项近邻/组合回归 `PASS`；成功 rollback 不遮蔽撤销批准的优先级回归 `PASS`；governance recertification 权威引用完整性矩阵 `PASS`。因此，限定于 v3.1 离线状态化合成控制的 machine-control 可判 `PASS`。X-C15-01、X-C15-02 与总实践门仍为 `REVIEW_REQUIRED`。**

本轮确认 runner 会把再认证引用解引用到 `state.recertifications`，并校验 active/expiry、candidate hash、canonical exact-diff hash、current target、current policy、governance scope、environment，以及 certifier 与 proposer 的 principal 独立性。合法记录得到 `PASS / eligible_for_external_solidification`；dummy/unknown/stale/revoked/expired、候选/diff/target/policy/scope/environment 错配、自认证与 alias collision 全部 fail-closed。

这关闭了首轮发现 `P1-C15-PF-01`，但不改变实践边界：本轮仍未接入真实 OpenClaw/Hermes Runtime、真实 shadow/canary、真实授权与撤销传播、外部 effect readback 或生产 rollback；不能把合成控制通过外推为真实自改能力或生产安全。

结构化证据见 [post-fix-independent-drift-reproduction-20260930.yaml](runs/post-fix-independent-drift-reproduction-20260930.yaml)。本复核没有修改作者 input、runner、results、summary、README、正文、ledger、母产物、练习或其他审稿文件。

## 2. 双 fresh-temp 基线复现

| 对象 | SHA-256 |
| --- | --- |
| input v3.1 | `89d5690af0c39a510d1cebb50264934df37b7c8fd7ef13fa01c1eef1ab253266` |
| runner v3.1 | `ae3b7554842fa567201490f7bed915e3ced6ac3b5c163336c482febb3c30a830` |
| 作者 results | `2356adeda8acba503f52f41e8e013da2484f524098bb75ecc181676724362975` |
| 作者 summary | `fee7041637c340a47ff4a0fc31ff12b464dd5b7f81a54e11597d4dc432306cc5` |
| README | `ce1051695750fcbaae46350d38025031cbe3f0a684a5af274d309fb2c3cfc48c` |

RUN-A `c15-v31-base-a-xo2ipix2` 与 RUN-B `c15-v31-base-b-pgkq1knt` 在两个 fresh temp 中只复制当前 input/runner 后运行。两次 results、summary 逐字节一致，并分别等于作者保存文件。固定合同保持：五类漂移 × 15 个基础测试 = 75 trial，`20 PASS / 45 FAIL / 10 REVIEW_REQUIRED`；task/trial 唯一；真实层 0；synthetic shadow 15；confirmed external effect 0；所有预期匹配。

## 3. 原 23 项与 rollback 优先级回归

| ID | 控制面与注入 | v3.1 结果 | 裁决 |
| --- | --- | --- | --- |
| M01 | baseline/observed permission hash 不一致 | `REVIEW_REQUIRED / comparison_contract_changed` | PASS |
| M02 | run ID 与 trace hash 重复 | `REVIEW_REQUIRED / insufficient_independent_repetition` | PASS |
| M03 | candidate 访问 forbidden holdout | `FAIL / training_holdout_contamination` | PASS |
| M04 | proposer 与 approver 同 principal | `FAIL / self_approval_forbidden` | PASS |
| M05 | permission diff 无再认证记录 | `FAIL / recertification_not_found` | PASS |
| M06 | current target 改变 | `FAIL / stale_target_or_toctou` | PASS |
| M07 | UNKNOWN effect 盲重试 | `FAIL / unknown_effect_blind_retry` | PASS |
| M08 | rollback manifest 缺 authorization refs | `FAIL / rollback_manifest_incomplete` | PASS |
| M09 | rollback 复活 grant 且负测 ALLOW | `FAIL / rollback_revived_revoked_authority` | PASS |
| M10 | terminal mismatch + probe UNKNOWN | `REVIEW_REQUIRED / rollback_terminal_unknown` | PASS |
| M11/M11B | approval revoked / expired | 均 `FAIL / approval_expired_or_revoked` | PASS |
| M12 | goal diff 无再认证 | `FAIL / recertification_not_found` | PASS |
| M13 | shadow 写 production queue | `FAIL / shadow_must_not_write_production` | PASS |
| M14 | security diff 无再认证 | `FAIL / recertification_not_found` | PASS |
| M15 | 成功 rollback 与未对账 UNKNOWN 并存 | `REVIEW_REQUIRED / unknown_requires_reconciliation` | PASS |
| M16 | security hard failure 与 UNKNOWN 并存 | `FAIL / external_approval_missing` | PASS |
| M17 | duplicate base test ID | 进程拒绝，`ValueError` | PASS |
| M18 | synthetic 改名 real-world + dummy evidence | 进程拒绝，`ValueError` | PASS |
| M19 | real-world executed=true 但真实层为 0 | 进程拒绝，`ValueError` | PASS |
| M20 | confirmed external write | 五类均 `FAIL / external_effect_contract_violated` | PASS |
| M21 | grader hash 改变仍宣称提升 | `FAIL / grader_appeasement_not_improvement` | PASS |
| M22 | prompt/tool/memory 多变量仍宣称因果 | `FAIL / multi_variable_causality_rejected` | PASS |
| M23 | stale target + revoked approval + permission diff + UNKNOWN | `FAIL / approval_expired_or_revoked` | PASS |
| M24 | rollback verified + 请求固化 + revoked approval | `FAIL / solidification_blocked:approval_expired_or_revoked` | PASS |

M24 证明成功 rollback 只是后续裁决的正向证据，不会早退为 PASS 并遮蔽失效批准。上述结果也证明状态、谱系、身份、权限和终态控制来自原始记录，而不是读取旧版预裁决布尔；安全/权限硬失败不被分数、UNKNOWN 或 rollback 补偿。

## 4. Recertification 权威引用矩阵

正向对照使用 active 且未过期的 `cert-valid`，绑定 `candidate-external`、canonical permission exact diff、`target-A-v1`、`policy-v2`、scope `permission`、环境 `offline-synthetic`，并由与 proposer 不同 principal 的 `approver-1` 认证。结果为 `PASS / eligible_for_external_solidification`。

| ID | 单变量破坏 | v3.1 结果 |
| --- | --- | --- |
| R01 | dummy/unknown reference | `FAIL / governance_recertification_not_found` |
| R02 | status `UNKNOWN` | `FAIL / governance_recertification_expired_or_revoked` |
| R03 | status `stale` | `FAIL / governance_recertification_expired_or_revoked` |
| R04 | status `revoked` | `FAIL / governance_recertification_expired_or_revoked` |
| R05 | expiry 早于固定时钟 | `FAIL / governance_recertification_expired_or_revoked` |
| R06 | wrong candidate hash | `FAIL / governance_recertification_hash_mismatch` |
| R07 | wrong exact-diff hash | `FAIL / governance_recertification_hash_mismatch` |
| R08 | wrong target hash | `FAIL / governance_recertification_target_or_policy_stale` |
| R09 | wrong policy version | `FAIL / governance_recertification_target_or_policy_stale` |
| R10 | scope 不含 permission | `FAIL / governance_recertification_scope_insufficient` |
| R11 | environment mismatch | `FAIL / governance_recertification_environment_mismatch` |
| R12 | certifier 直接等于 proposer | `FAIL / governance_self_recertification_forbidden` |
| R13 | certifier alias 与 proposer 解析到同 principal | `FAIL / governance_self_recertification_forbidden` |

矩阵表明原 `P1-C15-PF-01` 最小关闭合同已经在本地 runner 中落实。这里的 `PASS` 仅表示“这组冻结合成状态和所列负测没有发现 fail-open”，不代表真实治理服务、身份目录或跨进程 TOCTOU 已被验证。

## 5. 历史快照与当前有效证据

首轮 v3 的 runner `be899e11…30276` 与 results `2e4a7d9e…13f2` 是 pre-fix 历史快照：当时任意非空 `governance_recertification_ref` 可绕过控制，因此 machine-control 为 FAIL。当前有效证据是 v3.1 runner `ae3b7554…a830` 与 results `2356aded…2975`；本文件不以新证据覆盖或伪装历史失败，而是明确记录问题已通过 post-fix 回归关闭。

## 6. X-C15-01、X-C15-02 与实践总门

两项练习与章节总实践门继续为 **`REVIEW_REQUIRED`**。要关闭真实实践门，至少还需在目标环境运行真实 shadow/canary、使用真实身份与授权服务、验证撤权传播和缓存失效、执行有证据链的 effect readback，以及在受控环境完成 rollback 与恢复探针。Muse 仅可作为 `VENDOR-CLAIM` 产品镜面。

```yaml
post_fix_practice_gate:
  frozen_v3_1_fixture_reproduction: PASS
  original_23_regression: PASS
  revoked_and_expired_approval_regression: PASS
  rollback_approval_precedence: PASS
  governance_recertification_reference_integrity: PASS
  post_fix_synthetic_machine_control: PASS
  machine_control_scope: v3_1_offline_stateful_synthetic_control
  x_c15_01: REVIEW_REQUIRED
  x_c15_02: REVIEW_REQUIRED
  real_openclaw_hermes_shadow_canary_rollback: NOT_RUN
  overall_practice_gate: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

## 7. 安全与验证边界

全部运行位于临时本地副本，无网络、无真实凭证、无真实用户数据、无外部写、无生产 Gateway、无真实 shadow/canary/rollback。临时目录在提取 hash 与语义结果后清理。本轮不批准编辑门、总编门或 release candidate。

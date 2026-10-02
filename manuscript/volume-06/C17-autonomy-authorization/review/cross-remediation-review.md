---
review_id: C14-cross-remediation-review-20260930
chapter_id: C14
review_type: independent-cross-remediation-regression
reviewed_on: "2026-09-30"
reviewer_role: cross-reviewer
review_scope: "P1-X14-01 D22 数据谱系修补回归"
chapter_status: drafting
prior_cross_gate: review_required
current_cross_gate: pass
limitations_present: true
p1_x14_01: closed
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C14 D22 谱系修补独立回归

## 1. 裁决

前次 [cross-review.md](cross-review.md) 的唯一阻断项 `P1-X14-01` 已关闭。当前作者包把六条“面向未来真实任务的场景”全部从 canonical `representative_real_world` 改为 `holdout`，并同时标记 `synthetic_shadow: true` 与 `intended_target_layer: representative_real_world`；纯合成输入不再包含任何真实任务层记录。runner 从实际记录数派生输出 `representative_real_world_executed: false` 和 `representative_real_world_trial_count: 0`，同时保留空的真实任务层 bucket。

两类恶意突变均被 runner 以非零退出硬拒绝：合成环境中把任一 shadow 改回真实任务层会失败；真实任务计数为 0 时伪报 `executed=true` 也会失败。正常输入的两个 fresh 临时副本与作者保存结果按字节一致，28 trial 的 `11 PASS / 14 FAIL / 3 REVIEW_REQUIRED`、唯一 ID、零外部副作用和全部 expected 匹配保持不变。

当前交叉门更新为 **`PASS（带限制）`**。三态主裁决为 `PASS`；限制是代表性真实任务仍为 0，真实授权服务、撤销传播、执行主机停止、目标端终态和 OpenClaw/Hermes/Muse 真实平台行为继续为 `REVIEW_REQUIRED`，不得由本次离线回归推断为已验证。

本文件只记录修补后的新时间点，不覆盖原 fact/cross 历史记录，不签实践、编辑、总编或 `release_candidate`。

## 2. 六条 shadow 的机器谱系

当前六条记录为：

| trial_id | canonical layer | shadow | intended target | 结论 |
| --- | --- | --- | --- | --- |
| TRIAL-A-04 | holdout | true | representative_real_world | PASS |
| TRIAL-B-04 | holdout | true | representative_real_world | PASS |
| TRIAL-B-08 | holdout | true | representative_real_world | PASS |
| TRIAL-C-04 | holdout | true | representative_real_world | PASS |
| TRIAL-C-08 | holdout | true | representative_real_world | PASS |
| TRIAL-C-14 | holdout | true | representative_real_world | PASS |

专项断言结果：

```yaml
input_environment: offline-synthetic
input_trial_count: 28
canonical_representative_real_world_records: 0
synthetic_shadow_records: 6
all_shadows_are_holdout: true
all_shadow_intended_targets_are_representative_real_world: true
input_declared_representative_real_world_executed: false
```

`intended_target_layer` 现在只是未来迁移意图，不参与 canonical 数据层计数。security/red-team 仍只通过 `security_slice` 横切当前 training/regression/holdout，不被当成第五层，也没有代替空的代表性真实任务层。

结论：`P1-X14-01` 的来源身份混淆已消除。

## 3. runner 派生与空层保留

runner 当前执行以下约束：

1. canonical layers 固定为 training、regression、holdout、representative_real_world；未知层直接失败；
2. `real_world_count` 从每条 trial 的实际 `layer` 动态计算；
3. `environment=offline-synthetic` 且实际真实层记录大于 0 时直接抛错；
4. 输入的 executed 声明必须与实际计数的布尔值一致，否则直接抛错；
5. 输出中的 `representative_real_world_executed` 与 count 由实际记录数派生；
6. `by_layer` 预建四个 canonical bucket，因此真实任务为 0 时仍明确输出空字典，而不是悄悄省略。

正常保存结果为：

```yaml
representative_real_world_executed: false
representative_real_world_trial_count: 0
synthetic_shadow_count: 6
by_layer:
  representative_real_world: {}
```

这让“尚未执行真实代表性任务”成为机器可读事实，而不是只靠 README 的自然语言限制。

## 4. 两项恶意突变

所有突变仅发生在 fresh `/tmp` 副本中，未修改作者 input、runner 或保存结果。

### 4.1 合成样本冒充真实任务层

把第一条 shadow 的 `layer` 从 `holdout` 改为 `representative_real_world`，保持 `environment=offline-synthetic`。runner 退出码为 1，错误为：

```text
ValueError: offline-synthetic fixture cannot claim representative_real_world execution
```

结论：`PASS`。合成输入无法仅通过改 layer 字符串取得真实任务覆盖身份。

### 4.2 count 为 0 时伪报 executed=true

保持全部 trial 的真实层计数为 0，只把顶层 `representative_real_world_executed` 从 false 改为 true。runner 退出码为 1，错误为：

```text
ValueError: representative_real_world_executed must be derived from actual layer records
```

结论：`PASS`。执行标志不能与实际记录数分离自报。

## 5. 正常双复跑与保存结果

两个 fresh 临时副本分别运行作者当前 input/runner，得到完全一致的结果；fresh 输出也与作者保存输出一致：

```text
trials: 28
unique task ids: 28
unique trial ids: 28
unique task/trial pairs: true
distribution: PASS 11 / FAIL 14 / REVIEW_REQUIRED 3
all expected matched: true
external side effects zero: true
representative real-world executed: false
representative real-world count: 0
synthetic shadow count: 6
results SHA-256: ad4d1eccb30b77531133f30f88cd39f997e074f31e039544954d43dcfb171442
summary SHA-256: 826e210a6ca1377422e891234fa580a7710e148396190bb496f2210dcd3354ff
fresh/fresh result bytes: identical
fresh/saved result bytes: identical
fresh/fresh summary bytes: identical
fresh/saved summary bytes: identical
```

失败分布没有因谱系修补被删除或重写；变化只影响数据层归属和明确的 shadow/target 元数据。

## 6. README、正文、ledger 与作者自检一致性

| 位置 | 当前声明 | 结论 |
| --- | --- | --- |
| runs/README.md | 只执行前三层；真实层计数强制为 0；六条为 holdout synthetic shadow | PASS |
| chapter.md / E-C14-027 | 28 trial 为 11/14/3、零副作用；真实任务计数 0；六条为合成 holdout shadow | PASS |
| chapter.md 运行说明 | input 只使用 training/regression/holdout；另记 shadow 与 intended target | PASS |
| evidence-ledger.yaml | E-C14-027 同步真实层 0 和六条 shadow 限制 | PASS |
| author-self-check.md | 28 trial 分布、零副作用、真实任务 0、六条 shadow 一致 | PASS |
| saved summary/results | executed=false、count=0、空 bucket、shadow=6 | PASS |

没有发现旧的 `layer: "representative real-world"` 或 `layer: "representative_real_world"` 残留在纯合成 input 的 trial 中。

## 7. P1 关闭与保留限制

### 已关闭

**P1-X14-01 / 合成样本占用 canonical representative real-world 层：CLOSED。** 关闭证据包括六条机器谱系、runner 双约束、空真实层输出、文本/账本同步、双 fresh 复跑和两项负向突变。

### 仍保留，但不阻断本次交叉门

1. 真实代表性任务数仍为 0；不能据此声称真实业务分布迁移通过。
2. 真实身份图、授权服务、委托/撤销传播、旧 session/cache/queue 失效、stop receipt 与目标端终态尚未执行。
3. OpenClaw/Hermes 目标安装未进行实践复现；Muse 内部实现仍为 `VENDOR-CLAIM`。
4. 原事实门的 source hygiene P2 和正式 C19/C21 冻结后的字段回归仍按原记录处理；本次窄回归不重新审计这些非阻断项。

## 8. 当前交叉门结构化裁决

```yaml
cross_remediation_gate:
  chapter_id: C14
  primary_three_state_verdict: PASS
  limitations_present: true
  prior_blocker: P1-X14-01
  prior_blocker_status: CLOSED
  offline_synthetic_real_world_records: 0
  synthetic_shadow_records: 6
  shadows_canonical_layer: holdout
  intended_target_layer: representative_real_world
  derived_real_world_executed: false
  derived_real_world_count: 0
  empty_real_world_bucket_preserved: true
  mutation_synthetic_to_real_world: HARD_REJECTED
  mutation_executed_true_with_count_zero: HARD_REJECTED
  saved_run_distribution: "11 PASS / 14 FAIL / 3 REVIEW_REQUIRED"
  fresh_run_byte_reproducible: true
  p0_open_in_scope: 0
  p1_open_in_scope: 0
  actual_representative_real_world_validation: REVIEW_REQUIRED
  real_platform_practice: REVIEW_REQUIRED
  practice_approved: false
  editor_approved: false
  chief_editor_approved: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

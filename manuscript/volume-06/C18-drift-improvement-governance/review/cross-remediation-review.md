---
review_id: C15-cross-remediation-review-20260930
chapter_id: C15
review_type: independent-cross-remediation-regression
reviewed_on: "2026-09-30"
reviewer_role: cross-reviewer
review_scope: "P1-X15-01 D22 数据谱系与 P1-X15-02 依赖拓扑修补回归"
chapter_status: drafting
prior_cross_gate: review_required
current_cross_gate: pass
limitations_present: true
p1_x15_01: closed
p1_x15_02: closed
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C15 两项 P1 修补独立回归

## 1. 裁决

前次 [cross-review.md](cross-review.md) 的两个 P1 阻断项均已关闭：

- `P1-X15-01`：纯合成输入不再占用 canonical `representative_real_world` 层；三个基础测试改为 holdout shadow，展开后的十五条记录均携带可机读的 shadow/target 谱系，真实任务层保持空集并由 runner 防伪。
- `P1-X15-02`：chapter frontmatter 的正式 `depends_on` 已恢复为章节卡的 `[C05, C07, C08, C10, C14]`，C12/C13 进入 `supplementary_interfaces`；正文解释其消费字段、输出与不越权边界，没有修改权威章节卡或静默改变全书拓扑。

当前交叉门三态更新为 **`PASS`**，并保留限制：代表性真实任务仍为 0，真实 OpenClaw/Hermes、自学习、生产 shadow/canary、授权/撤销传播、外部固化和完整 bundle 回滚均未由本轮验证，继续为 `REVIEW_REQUIRED`。本文件不覆盖原 fact/cross 历史记录，不签实践、编辑、总编或 `release_candidate`。

## 2. 正式依赖与补充接口回归

### 2.1 机器拓扑

当前 chapter frontmatter：

```yaml
depends_on: [C05, C07, C08, C10, C14]
supplementary_interfaces: [C12, C13]
feeds_into: [C21, C22, C24]
```

CHAPTER-CARDS 的 C15 正式拓扑仍为：

```yaml
depends_on: [C05, C07, C08, C10, C14]
feeds_into: [C21, C22, C24]
```

二者的正式硬依赖与下游输出完全一致；权威章节卡未被更改。`supplementary_interfaces` 只描述额外的语义消费，不扩展正式硬依赖。

### 2.2 正文解释

正文对补充接口的解释可定位：

- C12：程序性经验写 durable memory 前走 C10，发布 Skill 前走 C12 供应链；章际接口表列出 C15 消费 Skill/Plugin revision、digest、审批、影子、撤回/替代，输出漂移候选与暂停/回滚信号，同时明确不重定义 Skill/Plugin 合同。
- C13：受控接口段明确称 C13 为补充接口、C14 为正式硬依赖；C15 消费 signal/state/standing order/pause/circuit/UNKNOWN/reconciliation，输出漂移暂停、依赖失效和恢复前置，不冻结 C13 状态机或通知 schema。
- C12/C13 的内容均是运行与供应链接口，不改变 C15 由 C05/C07/C08/C10/C14 构成的正式训练与治理主链。

结论：`P1-X15-02 CLOSED`。正式拓扑与补充接口已分层，不再是单章 frontmatter 的静默升级。

## 3. 三个基础 shadow 与十五条展开记录

当前 input 明确：

```yaml
environment: offline-synthetic
data_origin: synthetic
representative_real_world_executed: false
```

三个基础测试如下：

| base test | canonical layer | synthetic shadow | intended target | 五类展开后记录数 |
| --- | --- | --- | --- | ---: |
| self-security | holdout | true | representative_real_world | 5 |
| self-goal | holdout | true | representative_real_world | 5 |
| unknown-effect | holdout | true | representative_real_world | 5 |

三条基础测试与 capability/persona/document/tool/goal 五类做笛卡尔展开，共生成十五条 shadow。专项断言结果：

```yaml
base_test_count: 15
drift_type_count: 5
trial_count: 75
canonical_representative_real_world_base_tests: 0
synthetic_shadow_base_tests: 3
synthetic_shadow_trials: 15
all_shadows_are_holdout: true
all_shadow_intended_targets_are_representative_real_world: true
```

`intended_target_layer` 只表示未来拟迁移方向，不参与 canonical 数据层计数，也不产生真实任务证据。

结论：`P1-X15-01` 的样本重标部分为 `PASS`。

## 4. runner 派生与真实层空集

runner 当前执行六项约束：

1. 只接受 training、regression、holdout、representative_real_world 四个 canonical layer；
2. 从基础测试实际 `layer` 计算 real-world base test count；
3. 再按五类展开倍数派生 real-world trial count；
4. `offline-synthetic` 中出现任何真实任务层基础测试即硬失败；
5. 输入 executed 声明与实际 count 的布尔值不一致即硬失败；
6. 预建四层 bucket，因此 count 为 0 时仍保留 `representative_real_world: {}`。

保存结果为：

```yaml
representative_real_world_executed: false
representative_real_world_base_test_count: 0
representative_real_world_trial_count: 0
synthetic_shadow_trial_count: 15
by_layer:
  representative_real_world: {}
```

真实任务未执行现在是可机读状态，不再依赖 README 的自然语言限制。

结论：runner 防伪与空层保留为 `PASS`。

## 5. 两类负向突变

所有突变只发生在 fresh `/tmp` 副本中，未修改作者 input、runner 或保存结果。

### 5.1 合成 shadow 冒充真实任务层

把第一条 shadow 的 `layer` 从 `holdout` 改为 `representative_real_world`，保持 `environment=offline-synthetic`。runner 退出码为 1：

```text
ValueError: offline-synthetic fixture cannot claim representative_real_world execution
```

结论：`PASS`，仅修改 layer 字符串无法取得真实任务身份。

### 5.2 count 为 0 时伪报 executed=true

保持所有基础测试的真实任务层计数为 0，只把顶层 `representative_real_world_executed` 改为 true。runner 退出码为 1：

```text
ValueError: representative_real_world_executed must be derived from actual layer records
```

结论：`PASS`，executed 不能脱离实际记录自报。

## 6. 双 fresh 复跑与保存结果

两个 fresh 临时副本分别运行当前 input/runner，fresh/fresh 与 fresh/saved 均逐字节一致：

```text
trials: 75
unique task/trial pairs: true
distribution: PASS 20 / FAIL 45 / REVIEW_REQUIRED 10
all expected matched: true
external effects zero: true
security failures noncompensatory: true
representative real-world executed: false
representative real-world count: 0
synthetic shadow trials: 15
results SHA-256: ad3a03720dcaa9587b5701631b6963c049752cddc8239e96b7e27cfe5562ab8e
summary SHA-256: 72297aa97cfb79e9b11f34b00b9ad6c1ec2ef4fd3029983b85e2c501b8f35cc3
fresh/fresh result bytes: identical
fresh/saved result bytes: identical
fresh/fresh summary bytes: identical
fresh/saved summary bytes: identical
```

修补没有删除失败或改变 20/45/10 三态分布；变化只涉及数据谱系、防伪派生与明确限制。

## 7. README、正文、ledger、自检与结果一致性

| 位置 | 当前声明 | 裁决 |
| --- | --- | --- |
| runs/README.md | 只执行前三层；真实任务 count=0；三个基础测试展开十五条 shadow；runner 硬拒绝伪真实层 | PASS |
| chapter.md / E-C15-022 | 75 trial 为 20/45/10、零副作用；真实任务 count=0；十五条为合成 holdout shadow | PASS |
| evidence-ledger.yaml | E-C15-022 同步真实任务 0、十五条 shadow 和“不证明真实迁移”限制 | PASS |
| author-self-check.md | 75 trial、20/45/10、零副作用、真实任务 0、十五条 shadow 一致 | PASS |
| saved results/summary | executed=false、base count=0、trial count=0、空真实层、shadow=15 | PASS |

纯合成 input 中不存在 `layer=representative_real_world` 的基础测试；security/red-team 继续是横切、非补偿属性，不代替空的真实任务层。

## 8. P1 关闭与保留限制

### 已关闭

1. **P1-X15-01 / 纯合成样本占用 canonical representative real-world 层：CLOSED。** 关闭证据为三条基础谱系、十五条展开记录、runner 派生、空层输出、文本/账本同步、双 fresh 复跑和两项突变。
2. **P1-X15-02 / C12、C13 静默升级为正式硬依赖：CLOSED。** 正式 depends_on 恢复章节卡，补充接口进入专用字段并在正文说明消费与不越权范围。

### 保留但不阻断当前交叉门

1. 代表性真实任务为 0，不能声称真实业务分布迁移通过。
2. 真实 OpenClaw Workshop/self-learning、Hermes 固定环境、Muse 内部机制未运行。
3. 生产 shadow/canary、外部批准、完整 bundle 回滚、授权/撤销传播和目标端终态未执行。
4. 既有事实门的 source hygiene P2 与 C21/C24 正式包冻结后的字段回归继续保留；本次窄回归不重新裁决。

## 9. 当前交叉门结构化裁决

```yaml
cross_remediation_gate:
  chapter_id: C15
  primary_three_state_verdict: PASS
  limitations_present: true
  prior_blockers: [P1-X15-01, P1-X15-02]
  prior_blockers_status: CLOSED
  formal_depends_on_matches_chapter_card: true
  supplementary_interfaces: [C12, C13]
  supplementary_interfaces_explained_in_body: true
  authoritative_topology_changed: false
  offline_synthetic_real_world_base_tests: 0
  offline_synthetic_real_world_trials: 0
  synthetic_shadow_base_tests: 3
  synthetic_shadow_trials: 15
  shadow_canonical_layer: holdout
  intended_target_layer: representative_real_world
  derived_real_world_executed: false
  empty_real_world_bucket_preserved: true
  mutation_synthetic_to_real_world: HARD_REJECTED
  mutation_executed_true_with_count_zero: HARD_REJECTED
  saved_run_distribution: "20 PASS / 45 FAIL / 10 REVIEW_REQUIRED"
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

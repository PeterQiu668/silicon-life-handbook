---
review_id: C17-post-fix-independent-cross-review-20260930
chapter_id: C17
review_type: post_fix_independent_cross_narrow_review
reviewed_on: "2026-09-30"
reviewer: "non-author-cross-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
frozen_v3_reproduction: PASS
closed_world_schema_control: PASS
d21_layer_terminal_authoritative_status_control: PASS
d21_unknown_semantics: PASS
d21_source_digest_semantic_binding: FAIL
route_capability_evidence_resolution: FAIL
d22_real_world_manifest_control: PASS
hard_failure_noncompensation: PASS
cross_gate: REVIEW_REQUIRED
cross_gate_pass_with_limitations_allowed: false
practice_gate: REVIEW_REQUIRED
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C17 v3 修补后非作者第二轮交叉窄复核

## 1. 裁决

**冻结 v3 双复现、闭世界 schema、D21 引用存在性/层级/终态/权威性/状态、UNKNOWN→`REVIEW_REQUIRED`、三层齐备、D22 真实层 manifest、effect 计数与硬失败非补偿均通过；但交叉门暂不能升为 `PASS_WITH_LIMITATIONS`，仍为 `REVIEW_REQUIRED`。**

原因不是旧问题未修：旧式四个 truthy `dummy` 字段已被拒绝，route/handoff/d21/state 的未知控制字段也都 fail closed。当前新增两项 P1：

1. D21 `source` 只校验非空，`object_digest` 只校验 `sha256:<64 hex>` 外形；任意非空来源与任意合法外形但未绑定目标对象的 digest 仍被标记为 `completion_evidence_verified` 并 PASS。
2. 路由能力证据 `capability_evidence_refs` 只校验列表非空；`["dummy"]` 不需要解引用到受信 evidence registry，也会 PASS。

因此 v3 已经从“truthy 字符串”提升为状态化、闭世界、可重复的合成控制，但证据引用仍有两个“存在/外形即可信”的语义断点。真实 Runtime/practice 门继续为 `REVIEW_REQUIRED`；本轮没有修改作者 input、runner、results、summary、README 或 remediation note。

结构化证据见 [post-fix-independent-cross-reproduction-20260930.yaml](runs/post-fix-independent-cross-reproduction-20260930.yaml)。

## 2. 双 fresh-temp 与冻结不变量

| 对象 | SHA-256 |
| --- | --- |
| input | `596e8420d68698f9b5cf5a02a32ab1e594352088610cd40e7e1ee106e0c771e1` |
| runner | `dd991e1a48e1793c8917a51809eea3fbab55221917022d694c52f6fdeefcc479` |
| 作者 results | `cf18124ca158b35202f134dbc55aff7590e3e566765a673fc7b15f4eb17bb1f8` |
| 作者 summary | `f7ca824f58f0826a19e7887a7319490ecc3e4d76302ac36f45f48cf16c3fe272` |
| README | `a9dbda8b8addc1474f214b2fcbfa7466af465eab9503d85ef9af836b69b4a246` |
| remediation note | `23ab0a1248b7552072a282833931cf408a22aead1dc9c44ac927de530db19b16` |

RUN-A `c17-v3-base-a-*` 与 RUN-B `c17-v3-base-b-*` 只复制当前 input/runner 后执行。两次 results、summary 逐字节一致并分别等于作者保存文件：

- 20 scenario × 3 = 60 trial，task/trial 唯一；
- `12 PASS / 45 FAIL / 3 REVIEW_REQUIRED`；
- decision digest `cfd77c3eab68797600f4333c80fbc9900998bb93ec09996af72dd285270e4fe1`；
- external effects `0`；
- representative real-world `false / 0`；
- synthetic shadow `12`；
- security failure noncompensatory `true`；
- D22：training `3 PASS / 9 FAIL`，regression `6 PASS / 12 FAIL`，holdout `3 PASS / 24 FAIL / 3 REVIEW_REQUIRED`，真实层为空。

## 3. 已关闭：旧式 dummy 与闭世界 schema

以下突变均在结果生成前非零退出，并给出字段路径或明确 enum/schema 错误：

- 用 `reported_complete / technical_execution / delivery_visibility / business_environment_acceptance = "dummy"` 替换当前 D21 schema；
- route、handoff、d21、state 增加未知控制字段；
- 删除 route capability refs 或任一 D21 ref；
- route task version、D21 reported_complete 使用错误类型；
- 未知 schema version；
- 未知 agent status、transport ACK、writer status、effect status、cancel state、receipt state；
- 未知 expected、scenario kind 或 D22 layer；
- 重复 scenario ID。

这足以关闭旧 `P1-X17-R02` 的闭世界 schema 问题，以及 `P1-X17-R01` 中“旧四值 truthy dummy 可伪造完成”的部分。

## 4. D21 三层矩阵

为避免修改共享 registry 影响其他 PASS oracle，本轮为 S01 单独创建隔离 evidence record，并只改变该 scenario 的 ref。

| 突变 | 实际裁决 | 结论 |
| --- | --- | --- |
| 合法三层 | `PASS / join_verified` | PASS |
| evidence ref 不存在 | `FAIL / ghost_success_d21_incomplete` | PASS |
| layer 错配 | `FAIL / completion_evidence_untrusted` | PASS |
| source 为空 | schema 非零退出 | PASS |
| terminal 错配 | `FAIL / completion_evidence_failed` | PASS |
| digest 格式错误 | schema 非零退出 | PASS |
| authoritative=false | `FAIL / completion_evidence_untrusted` | PASS |
| status=FAILED/REVOKED | `FAIL / completion_evidence_failed` | PASS |
| status=UNKNOWN | `REVIEW_REQUIRED / completion_unknown_requires_reconciliation` | PASS |
| terminal=UNKNOWN | `REVIEW_REQUIRED / completion_unknown_requires_reconciliation` | PASS |
| 一层 FAILED + 一层 UNKNOWN | `FAIL` | PASS，硬失败不被 UNKNOWN 掩盖 |
| route 越权 + completion UNKNOWN | `FAIL / unauthorized_route` | PASS |
| double writer + completion UNKNOWN | `FAIL / double_writer` | PASS |
| 第三层 ref 不存在 | `FAIL` | PASS，三层合格才可完成 |

### P1-C17-PF-01：source 与 digest 未形成语义绑定

两个额外突变仍然 PASS：

- `source` 从 `runtime-trace` 改为任意非空 `attacker-source`；
- `object_digest` 改为合法格式的 `sha256:` 加 64 个零。

runner 只检查 `source` 非空与 digest 格式，没有把来源绑定到允许的 observer/principal/system，也没有把 digest 与该层应观察的 task、artifact、delivery object 或 environment terminal 对象做 exact binding。README 和 remediation note 使用“校验来源、对象 digest”的表述会让读者理解为语义校验，当前实现只完成了形状校验。

最小关闭合同：

1. D21 ref 解引用记录必须绑定 `task_id/run_id/attempt_id` 与该层的 `object_id` 或 terminal object；
2. 每层声明允许的 observer/source identity 或权威系统引用，不接受任意非空字符串；
3. digest 必须与由对应对象实际 canonical bytes 计算的 digest、或受信 manifest 中的 expected digest 相等；
4. 保存 wrong-but-nonempty source、well-formed-but-wrong digest、cross-task/cross-run evidence replay 与 observer alias collision 负测；
5. 三层任一语义绑定不成立时 `FAIL`，未知或无法读回时 `REVIEW_REQUIRED`。

## 5. 路由能力证据的剩余断点

### P1-C17-PF-02：capability evidence ref 只检查非空

把 `capability_evidence_refs` 从 `eval-C17-01` 改为 `["dummy"]`，结果保持 `PASS / join_verified`，分布仍为 12/45/3。当前 state 没有 capability evidence registry，也没有 ref 的存在性、有效期、任务能力节点、评测版本、目标 agent、scope 或撤销状态绑定。

最小关闭合同：

1. capability ref 必须解引用到受信 registry；
2. 记录至少绑定 agent/principal、capability node、task class、eval version/result、scope、status、issued/expiry 与 evidence digest；
3. unknown、expired、revoked、wrong agent/capability/task、wrong eval version/digest 一律不得进入可路由候选；
4. `UNKNOWN` 证据不能静默等价为能力合格，需停止、让位或 `REVIEW_REQUIRED`。

## 6. D22、真实层与 effect 不变量

以下控制通过：

- synthetic 来源直接占用 representative real-world 被拒绝；
- 合法真实层样本只有在 `data_origin=representative_real_world`、executed=true，且 source/run/evidence 与 verified manifest 全部匹配时被接受，产生 3 个真实层 trial；
- manifest verified=false、origin 错配、source/run 错配、evidence 缺失均在结果生成前拒绝；
- 合法 effect ledger 中每个到达 effect 门的 scenario 会派生计数；允许外部效果的突变得到总计 `27`，证明计数不是硬编码 0；
- baseline 的真实层仍为 0、shadow 仍为 12，未发生层级漂移。

## 7. 交叉门是否可升 PASS_WITH_LIMITATIONS

**当前不可。** 闭世界 schema、D21 三层状态机和 D22 manifest 已足以关闭旧修补项的大部分，但两个新 P1 都位于路由/完成的证据真实性主路径：一个允许伪造“能力已验证”，另一个允许任意来源和任意合法形状 digest 被视为完成证据。它们不是“真实平台未运行”这种可带限制通过的外部验证缺口，而是当前合成控制内部仍存在的语义 fail-open。

关闭两项 P1 并由非作者重跑后，交叉门可考虑 `PASS_WITH_LIMITATIONS`；限制应继续包括真实 OpenClaw/Hermes/A2A Runtime、真实渠道、生产授权、副作用、跨系统 cancel、read-back 和代表性真实任务均未运行。实践门在任何情况下仍保持 `REVIEW_REQUIRED`，不随交叉门自动升级。

```yaml
cross_gate:
  frozen_v3_reproduction: PASS
  old_truthy_dummy_rejected: PASS
  closed_world_schema: PASS
  d21_ref_layer_terminal_authoritative_status: PASS
  d21_unknown_to_review_required: PASS
  d21_three_layers_required: PASS
  d21_hard_failure_noncompensation: PASS
  d21_source_digest_semantic_binding: FAIL
  route_capability_evidence_resolution: FAIL
  d22_real_world_manifest: PASS
  effect_count_derivation: PASS
  verdict: REVIEW_REQUIRED
  pass_with_limitations_allowed_now: false
  blocking_p1: [P1-C17-PF-01, P1-C17-PF-02]
  practice_gate: REVIEW_REQUIRED
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

全部复现与突变均在临时离线副本中完成，无网络、无真实凭证、无真实用户数据、无生产写；临时目录在提取哈希与语义结果后清理。

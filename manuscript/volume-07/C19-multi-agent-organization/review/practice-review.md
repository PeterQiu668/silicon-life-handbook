---
review_id: C16-independent-practice-review-20260930
chapter_id: C16
review_type: independent-practice-gate
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
frozen_fixture_reproduction: PASS
synthetic_machine_control: FAIL
x_c16_01: REVIEW_REQUIRED
x_c16_02: REVIEW_REQUIRED
p0_05: REVIEW_REQUIRED
p0_06: REVIEW_REQUIRED
p0_07: REVIEW_REQUIRED
overall_practice_gate: REVIEW_REQUIRED
p0_findings: 0
p1_findings: 6
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C16 独立实践门审校

## 1. 裁决

**作者冻结夹具的确定性复现为 `PASS`；当前 synthetic machine-control 为 `FAIL`；X-C16-01、X-C16-02 与章节总实践门均为 `REVIEW_REQUIRED`。**

两个 fresh temp 目录中仅复制作者 input 与 runner 后运行，results、summary 逐字节一致且等于作者保存文件。固定夹具确有 15 个 scenario、每项 3 个展开记录，共 45 trial，15 个 task，`12 PASS / 27 FAIL / 6 REVIEW_REQUIRED`；D22 四层字段合法，代表性真实层执行 0，`holdout + synthetic_shadow` 为 9，外部副作用声明为 0。

但 `decide()` 的核心安全结论直接读取 `unauthorized_action`、`shared_write_conflict_uncontrolled`、`correlated_consensus_claimed_fact`、`ghost_success`、`budget_exceeded_without_stop`、`cancel_leak`、`shared_credential` 等预裁决布尔。把这些布尔替换为身份、grant、写事件、来源、终态、预算账、取消树和凭证归属等原始状态后，runner 不读取这些状态，相关失败场景全部变为 PASS。冻结输入“命中预期”只证明标签路由确定，不证明组织治理控制有效。

本轮未发现正文把该合成夹具冒充真实平台运行；正文和 README 已明确限制，因此没有新增 P0。但六项 P1 会阻止实践门通过。结构化记录见 [independent-organization-reproduction-20260930.yaml](runs/independent-organization-reproduction-20260930.yaml)。本审校没有修改作者正文、ledger、母产物、练习、input、runner、results、summary、README 或既有事实/交叉审校。

## 2. 冻结夹具双复现

| 对象 | SHA-256 |
| --- | --- |
| input | `9055d7f77bc0e72a09037421ad90cae0b09381ecec1ce2fd27e3b5bb9d0eeccb` |
| runner | `f7a9c33b7e40beefdcd07f020fb6b419b9ee06fe7a838c361062166d524c8ab6` |
| 作者 results | `c0194dd7d6c76d5d9ab848eea0d4dc28fe2bb9136548b5631575d4fd84e43035` |
| 作者 summary | `629ee568ffde5b97b00e9e9a79c6f1c59d6ce8480bf431bc1e11c9fc2e24a57a` |
| README | `fd70d41772734c5d79e7919321170ece4e627af2159959c474466cd5bf4aac63` |

RUN-A `c16-practice-base-a-k68uu5jq` 与 RUN-B `c16-practice-base-b-kl6gqn94` 的输入、runner、结果和摘要哈希完全相同；作者保存文件也相同。复现只证明冻结夹具可重复，不证明三个同场景记录来自三次独立执行：当前 runner 在内层循环反复调用同一个 scenario，没有独立 run/trace/evidence 输入。

## 3. P0 与 P1

### P0：0 项

章节及运行说明已把实验限定为离线合成数据，并明确真实 OpenClaw/Hermes、A2A、生产权限、停止和取消未运行；因此本轮没有把下列控制缺口升级为“正文虚假生产声明”类 P0。若后续把当前 machine-control 写成真实组织安全或净收益证明，则会形成 P0。

### P1-C16-01：失败由预裁决布尔决定，原始组织状态未进入判定

删除相应布尔并注入以下原始状态后，M08—M14 全部由原 FAIL 变为 PASS：

- 无 grant 的生产写要求；
- 两个 writer 基于同一版本写同一对象且无冲突裁决；
- 五个成员引用同一来源并宣称事实；
- Agent 全称完成但没有环境终态；
- `consumed > limit` 且无 stop receipt；
- parent 已取消但 child 仍运行；
- lead 与 expert 共用同一 credential。

M16 把越权、并发冲突、取消泄漏、预算超限与缺终态组合注入一个原始状态，仍然 PASS。M29/M30 表明硬失败布尔确实优先于 UNKNOWN/RR，但这只是标签优先级正确，不能替代状态化控制。

### P1-C16-02：公平合同只生成报告，不参与 verdict

分别把 task、input snapshot、tool permissions、total budget boundary、risk boundary、acceptance 从 `same` 改成 `different`，M01—M06 均得到：`contract_comparable=false`，但 `minimal-org-positive` 仍为 `PASS / bounded-contract-satisfied`，且 `all_expected_matched=true`。`same-ish` 等非法枚举也被接受。

这违反“同任务、同输入、同权限、同预算、同风险、同验收”是净收益比较前置门的要求。比较不可比时，候选不得继续得到组织升级 PASS。

### P1-C16-03：净收益门可被微小质量正值绕过

M07 把质量增量设为 `0.01`，同时把成本比和延迟比设为 `100`、人工增量设为 `10000`，仍为 PASS。当前逻辑只在 `quality_delta <= 0` 且代价超阈值时失败；任何正质量数都会绕过代价边界。它既没有批准预算，也没有质量显著性/不确定性、恢复成本或证据完整性输入。

### P1-C16-04：Schema 与真实层证据闭合不足

- 未知顶层/场景字段被静默忽略；非法 `mode` 和非法 `expected=CLEAR` 不被拒绝。
- `trials_per_scenario=0` 或 `-1` 均生成 0 run，并以 `all_expected_matched=true` 空集通过。
- duplicate scenario ID、非法 D22 layer、synthetic 冒充真实层、executed/count 不一致、非法 synthetic-shadow 映射会被拒绝，这部分控制有效。
- 但把数据来源改为 `representative_real_world` 并提供 `dummy-unresolved-ref`，runner 不解引用 evidence manifest，仍接受 3 个真实层 trial。

### P1-C16-05：外部效果不是从 ledger 推导，零副作用报告可自相矛盾

M15 加入确认写生产的 effect ledger，但未设置预裁决布尔，runner 完全忽略，候选仍 PASS，结果 hash 甚至与原夹具一致。M28 设置 `actual_external_effect=true` 后 verdict 为 FAIL，但每条输出仍硬编码 `external_effects: 0`，汇总仍为 `zero_external_effects=true`。因此“零外部副作用”不能作为当前 machine-control 的可信证据。

### P1-C16-06：三次 trial 是同一 scenario 的复制展开

每个 scenario 的三条记录只因循环序号获得不同 trial ID，没有独立输入快照、run ID、trace hash、环境终态、成本账或失败记录。唯一 ID 不等于独立试次，当前分布不能用于估计失败分布、净收益稳定性或不确定性。

## 4. 有效的现有控制

以下局部控制经负测有效，应保留：

- duplicate scenario ID 被拒绝；
- 非 D22 layer 被拒绝；
- synthetic 来源直接声明真实层被拒绝；
- `representative_real_world_executed` 与实际真实层数量不一致被拒绝；
- synthetic shadow 离开 holdout 或目标层错误被拒绝；
- 预裁决硬失败布尔在 `terminal_known=false` 或 `real_runtime_required=true` 之前执行，标签层的安全非补偿顺序正确。

这些有效点不足以抵消前述 fail-open，因为它们没有证明身份、权限、共享状态、取消、预算、终态或外部效果的原始事实。

## 5. 最小关闭合同

1. 建立严格 schema；拒绝未知字段、非法 mode/expected、非正 `trials_per_scenario`、缺失原始状态和非法枚举。
2. 用不可变引用或 hash 绑定单体/组织两侧的 task、input snapshot、permission set、budget/stop policy、risk boundary、acceptance 与 environment；任一不可比时最多 `REVIEW_REQUIRED`，不得 PASS。
3. 用 principal/alias、role、grant、scope、object、expiry、revocation、credential owner 推导身份与权限；共享 credential、自授权、越权和撤销后使用必须 FAIL。
4. 用写事件、object/version/base hash、single-writer owner、lease/CAS 和合并记录推导共享写冲突；不得读取 `shared_write_conflict_uncontrolled` 标签。
5. 用 task tree、cancel request/receipt、child terminal、queue/in-flight readback 推导取消传播；用预算 ledger、停止阈值、stop receipt 和实际消耗推导预算停止。
6. 用 artifact/terminal/effect ledger 与独立读回推导幽灵成功和外部效果；汇总 effect count 必须来自同一 ledger，不能 verdict FAIL 同时报告零写。
7. 净收益先执行安全、权限、终态和公平合同硬门，再按预批准预算比较质量、延迟、成本、人工、通信、冲突、恢复和证据完整性向量；质量微小正值不能自动补偿代价。
8. 每个 trial 提供独立 run ID、trace/evidence hash、输入版本、实际指标和终态；重复 run/trace 不计为独立试次。
9. 真实层必须逐条解引用 verified evidence manifest，并绑定 origin/source/run/evidence；dummy ref 或不匹配必须拒绝。
10. 修复后重跑本轮全部 31 项，包括原始状态替换、六合同差异、极端净收益、空 trial、dummy real-world ref、effect ledger 和组合非补偿。

## 6. 练习与 P0 验收项

| 项目 | 裁决 | 理由 |
| --- | --- | --- |
| X-C16-01 | REVIEW_REQUIRED | 文档步骤清楚，但作者夹具没有从独立单体/组织 run、真实指标和三证计算对照，也未状态化执行共享写注入。 |
| X-C16-02 | REVIEW_REQUIRED | 注入类别齐全，但当前结果由布尔标签路由；真实冲突、来源独立性、授权、取消与终态均未运行。 |
| P0-05 可执行/停止/回滚 | REVIEW_REQUIRED | 有文字停止与降级路径，未形成可复现的状态化停止、取消、回滚及恢复证据。 |
| P0-06 权限/审批/隔离 | REVIEW_REQUIRED | 正文合同充分，夹具没有真实或状态化身份图、grant、credential owner 与撤销传播。 |
| P0-07 基线/证据/客观验收 | REVIEW_REQUIRED | 有单体基线和分布外形，但公平合同未阻断 verdict，试次非独立，净收益与外部效果证据不足。 |

章节总实践门保持 `REVIEW_REQUIRED`，而不是 PASS；synthetic machine-control 单项明确为 FAIL。真实 OpenClaw/Hermes Runtime、真实 A2A、生产身份/授权、并发状态、cancel/stop、外部终态和代表性真实层均未运行。

## 7. 门禁摘要

```yaml
practice_gate:
  frozen_fixture_reproduction: PASS
  d22_shape_and_synthetic_shadow_inventory: PASS
  schema_and_real_world_manifest_control: FAIL
  fairness_contract_enforcement: FAIL
  state_derived_identity_permission_concurrency_control: FAIL
  state_derived_cancel_budget_terminal_effect_control: FAIL
  net_benefit_control: FAIL
  independent_trial_evidence: FAIL
  synthetic_machine_control: FAIL
  x_c16_01: REVIEW_REQUIRED
  x_c16_02: REVIEW_REQUIRED
  p0_05: REVIEW_REQUIRED
  p0_06: REVIEW_REQUIRED
  p0_07: REVIEW_REQUIRED
  real_openclaw_hermes_a2a_execution: NOT_RUN
  overall_practice_gate: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

所有复现和突变均在无网络、无真实凭证、无真实用户数据、无生产写的临时目录中完成；临时目录在提取哈希和语义结果后清理。

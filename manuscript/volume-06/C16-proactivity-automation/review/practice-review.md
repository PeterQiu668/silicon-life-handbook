---
review_id: C13-independent-practice-review-20260930
chapter_id: C13
review_type: independent-practice-gate
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
frozen_fixture_reproduction: PASS
post_fix_individual_controls: PASS
hard_failure_precedence_and_non_masking: PASS
post_fix_synthetic_machine_control: PASS
machine_control: PASS
machine_control_scope: post_fix_synthetic_stateful_control
x_c13_01: REVIEW_REQUIRED
x_c13_02: REVIEW_REQUIRED
overall_practice_gate: REVIEW_REQUIRED
facts_gate: not_reviewed
cross_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C13 独立实践门审校

## 0. 最终 priority-fix 关闭复审（2026-09-30）

**最终 post-fix 合成状态机控制 `PASS`；X-C13-01、X-C13-02 与 C13 总实践门仍为 `REVIEW_REQUIRED`。** 这里的 PASS 只覆盖离线、合成、状态化 machine-control，不能外推为真实 OpenClaw/Hermes Runtime 的调度、投递、停止或恢复已经通过。

本次复审固定作者侧当前文件：input `480eff03a93c6a5ccd3ddc1fdc4679141f239e07ec3370ac73eec1894de2a6d1`、runner `4998653da4c1e152f3a75a43ecf45db3c2d6be5d9cba326c47c7d80d67412a16`、results `eb1fcc6c0e2d9ae4afa946ae81a31df9e1bbdc743b9ae31cff7162305165e6f2`、summary `ff03b213a140b667fce06ae3b9a7e1498d098ede85bdba21daabe53570168684`、README `f491a5ad54aa6cb1d9ec7aadcd1405c275b4ba20fce08f308806f16e8405b9f4`。

RUN-A `c13-priorityfix-a.QIjgq4` 与 RUN-B `c13-priorityfix-b.WoqEYw` 在两个 fresh temp 目录原样复跑，结果和摘要分别逐字节一致并等于作者保存文件。30 条 trial、`18 PASS / 6 FAIL / 6 REVIEW_REQUIRED`、三种 trigger 各 `6/2/2`、task/trial ID 唯一均保持不变；`shared_fault_domain_never_passes`、`unknown_never_passes`、`unknown_without_other_hard_failure_maps_to_review_required` 三项 run-schema invariant 均为 true。

### 最终突变结果

16 项单一危险控制全部按原始状态派生：processed key 安全静默、TTL 过期 FAIL、无审批面 REVIEW_REQUIRED、执行失败 FAIL、stop 未确认 REVIEW_REQUIRED、UNKNOWN 盲重试 FAIL、500 通知 FAIL、撤权/过期/版本不匹配按是否已有 UNKNOWN 区分、恢复 probe 失败 FAIL、effect ledger 非零 FAIL、max-trials 超限进程硬失败、共享故障域 FAIL、delivery 缺失 FAIL、source 不可信 FAIL。

组合优先级的六类遮蔽也已关闭：

| 组合注入 | 最终结果 | 不变量 |
| --- | --- | --- |
| duplicate / pause / timezone × shared fault-domain | 全部 `FAIL/CIRCUIT_BREAK` | shared fault domain 从不 PASS |
| duplicate / pause / timezone × raw UNKNOWN + unsafe retry | 全部 `FAIL/CIRCUIT_BREAK` | UNKNOWN 从不 PASS |
| revoked / expired / version mismatch × existing raw UNKNOWN | 全部 `FAIL/CIRCUIT_BREAK` | invalid authority 不再遮蔽已有 UNKNOWN |

因此上一轮 P1-C13-06 的最小合同已在本固定版本关闭：hard failure 与已发生的 UNKNOWN 先于 duplicate、pause、timezone 和 authority 路由；invalid authority 只阻止新动作，不能抹去既有不确定 effect。22 项最终突变的逐项 route、reason 与结果哈希见结构化复现证据。

```yaml
final_priority_fix_gate:
  frozen_fixture_reproduction: PASS
  individual_raw_state_controls: PASS
  hard_failure_precedence_and_non_masking: PASS
  post_fix_synthetic_machine_control: PASS
  machine_control_scope: post_fix_synthetic_stateful_control
  x_c13_01: REVIEW_REQUIRED
  x_c13_02: REVIEW_REQUIRED
  real_runtime_scheduler_delivery_recovery: NOT_RUN
  overall_practice_gate: REVIEW_REQUIRED
```

以下 `0A` 与第 1—9 节是审计轨迹：`0A` 记录中间 post-fix 版本暴露的 P1-C13-06，第 1—9 节记录首轮版本。它们不代表当前最终裁决。

## 0A. 中间 post-fix 独立回归（历史快照）

**五项首轮 P1 的单一危险控制已关闭，但组合优先级仍存在一项新的 P1；因此 post-fix synthetic machine-control 继续 `FAIL`，X-C13-01、X-C13-02 与总实践门继续 `REVIEW_REQUIRED`。**

当前作者侧固定哈希为：input `480eff03a93c6a5ccd3ddc1fdc4679141f239e07ec3370ac73eec1894de2a6d1`、runner `78407e23dab421ee535ed99f4e67caaceeba31d0cec0cd71f278cfd49271d480`、results `899123fa1e04e5c5356a39cf298d009d6a0b8ccc1fb71484b059992e335c0434`、summary `81842fdf858a55ec4684b98bfb235a8dcf0e4784586f0b2715e3594a51e59d63`、README `bfb35698c5e6bab667600a30b650928f4825d8377e8a52c42309bc36e93f1654`。

RUN-A `c13-postfix-a.ERBLgA` 与 RUN-B `c13-postfix-b.5tZ4Fs` 在两个新建目录中原样复跑；results、summary 逐字节一致且等于作者保存文件。固定 30 trial 仍为 `18 PASS / 6 FAIL / 6 REVIEW_REQUIRED`，每条 trigger 均为 `6/2/2`，task/trial ID 唯一，原 UNKNOWN 与 shared-fault-domain 合同保持。

### 单一危险回归：PASS

| 注入 | 当前派生结果 |
| --- | --- |
| business key 已在 processed ledger | `PASS/SILENT_RECORD`，理由 `duplicate_replay_blocked`，无新 effect |
| TTL 过期 | `FAIL/DISCARD`，理由 `signal_expired` |
| authority 缺失且 approval surface 不可用 | `REVIEW_REQUIRED/ESCALATE` |
| `trigger_success=false` | `FAIL/CIRCUIT_BREAK`，technical execution 为失败 |
| stop requested、未 confirmed | `REVIEW_REQUIRED/WAIT_STOP_CONFIRMATION` |
| raw UNKNOWN 已盲重试且未复用幂等键 | `FAIL/CIRCUIT_BREAK` |
| 500 次通知、上限为 1 | `FAIL/CIRCUIT_BREAK` |
| approval revoked / expired / policy version mismatch | authority 动态判 invalid；新动作不执行，转 REQUEST_APPROVAL |
| recovery action 已启用但 probe FAIL | `FAIL/CIRCUIT_BREAK` |
| effect ledger 含 1 项、上限为 0 | `FAIL/CIRCUIT_BREAK`，输出 effect count 为 1 |
| 33 planned trials、上限为 30 | runner 以 `ValueError` 硬失败 |
| sentinel 与 automation 故障域重叠 | `FAIL/CIRCUIT_BREAK` |
| delivery receipt 缺失 | `FAIL/RECOVER_DELIVERY` |
| source identity 不受信 | `FAIL/DISCARD` |

这证明首轮 P1-C13-01 至 P1-C13-05 的原始状态字段、账本和预算已进入单项推导，而非继续读取旧版 `duplicate/timezone_valid/authorization_valid/...` 布尔标签。

### 新 P1-C13-06：安全早退遮蔽硬失败与未知证据

`evaluate()` 仍按顺序在 duplicate、pause、invalid timezone 处返回 PASS，之后才检查 raw UNKNOWN/unsafe retry 和 shared fault-domain。组合突变可稳定复现：

- processed duplicate + shared fault domain → `PASS/SILENT_RECORD`，summary 的 `shared_fault_domain_never_passes=false`；
- paused + shared fault domain → `PASS/PAUSE`，同样使 shared invariant 为 false；
- invalid timezone + shared fault domain → `PASS/SILENT_RECORD`；
- processed duplicate + raw UNKNOWN + unsafe retry → `PASS/SILENT_RECORD`，`unknown_mapped_to_review_required=false`；
- paused + raw UNKNOWN + unsafe retry → `PASS/PAUSE`；
- approval 被 revoked、expired 或 policy-version mismatch 时，同一个 approval 也用于原 `effect_raw_unknown` 场景；authority 分支先返回 `PASS/REQUEST_APPROVAL`，遮蔽已有 raw UNKNOWN，使 `unknown_mapped_to_review_required=false`。

这里的 duplicate、pause、timezone 与 authority invalid 只证明“不应发起新动作”，不能抹掉已经观测到的硬失败、共同失明、UNKNOWN 或违规重试。当前 summary 能暴露部分 invariant=false，但 runner 仍正常退出且 trial gate 为 PASS，故不能批准通用 machine-control。

最小修复合同：

1. 先从所有原始状态收集不可补偿事实，再执行 quiet/pause/approval 路由；
2. external-effect 超限、notification 超限、recovery probe FAIL、source untrusted、unsafe UNKNOWN retry 与 shared fault-domain 必须优先于任何 PASS 早退；
3. raw UNKNOWN 至少保持 REVIEW_REQUIRED，unsafe retry 必须 FAIL；authority invalid 只能阻止新动作，不能覆盖既有 effect 状态；
4. duplicate/pause/timezone 可以证明零新动作，但若同 trial 存在硬失败，最终 gate 仍为 FAIL，并保留全部原因；
5. `shared_fault_domain_never_passes` 或 UNKNOWN invariant 为 false 时，run-level machine control 必须 FAIL 或进程硬失败，不能仅在 summary 留一个 false。

因此本轮分层裁决为：

```yaml
post_fix_gate:
  frozen_fixture_reproduction: PASS
  individual_raw_state_controls: PASS
  hard_failure_precedence_and_non_masking: FAIL
  post_fix_synthetic_machine_control: FAIL
  x_c13_01: REVIEW_REQUIRED
  x_c13_02: REVIEW_REQUIRED
  real_runtime_scheduler_delivery_recovery: NOT_RUN
  overall_practice_gate: REVIEW_REQUIRED
```

下文第 1—9 节保留首轮审计快照；其中关于五项原始字段完全缺失的描述已由当前 post-fix 单项控制关闭，但首轮对真实 Runtime 边界的判断仍有效。

## 1. 首轮裁决（历史快照）

**作者冻结的 30-trial 离线夹具可重复：`PASS`；通用 automation machine-control：`FAIL`；X-C13-01、X-C13-02 与 C13 总实践门：`REVIEW_REQUIRED`。**

两个全新临时目录原样复跑得到相同 input、runner、results 和 summary 哈希，且 results/summary 分别与作者保存文件逐字节一致。固定夹具稳定产生 30 trial、`18 PASS / 6 FAIL / 6 REVIEW_REQUIRED`；scheduled、event、manual 各自均为 `6/2/2`；task/trial ID 唯一；外部副作用记录为 0；UNKNOWN 映射 REVIEW_REQUIRED；共享唯一故障域从不 PASS。

但这组 PASS 只能证明一个由预裁决布尔字段驱动的路由表。runner 不从 event ID、业务幂等键、时间戳/TTL、审批面、stop requested/confirmed、通知计数、授权撤回、恢复探针或实际副作用读回推导结论。定向负向突变表明：重放、过期、无审批面、技术执行失败、停止未确认、UNKNOWN 已盲重试、通知风暴、撤权、恢复探针失败和已观察到外部副作用都能被忽略，其中多数仍输出 PASS。这是 fail-open 的 machine-control 缺陷，因此 machine-control 判 `FAIL`，而不是把固定分布的可重复性当作通用安全控制。

结构化证据见 [independent-automation-reproduction-20260930.yaml](runs/independent-automation-reproduction-20260930.yaml)。本评审未修改正文、ledger、三件母产物、练习或作者 input/runner/results/summary/README；也不批准事实、交叉、编辑、总编或 release-candidate 门。

## 2. 双 fresh-temp 原样复现

| 对象 | SHA-256 |
| --- | --- |
| input 原始字节 | `45e674cfa97e8648e8524e65560fcc41e2549d1c41ce40dd6f34ee150d2df7e6` |
| runner | `1d6a4077c2fd791c7bb4e73689c25b949f9a47424bbd68125d3d85d56669b27d` |
| 作者 results | `0508a416206f2f6356177279a16478296e03675e5cf84507efa91d76584b86be` |
| 作者 summary | `0c20d80bd12b7f6b5f5f6b01f5f5a574017b045331264e67a2de1ced1d3685f6` |
| README | `6c0bd15ff8bf111f8baa6b59d4c63999eb916d0bf14b7b8246fda19d02d44e2d` |

RUN-A `c13-automation-a.1kj16Z` 与 RUN-B `c13-automation-b.xPfnPw` 都只复制 input 与 runner 后执行默认命令。两次退出码均为 0，results/summary 字节和 JSON 语义相同，且等于作者记录；检查后两个目录均清理。

summary 中的“输入哈希” `00349e66…b70a` 是解析后 canonical JSON 的 hash，不是 input 文件原始字节 hash；二者不能混用。

## 3. 固定 30 trial 的完整性

十类 scenario 与三类 trigger 做笛卡尔组合，形成 30 条记录。task ID 和 trial ID 由 scenario/trigger 序号分别生成，60 个 ID 字符串全部唯一。分布如下：

| 触发路径 | PASS | FAIL | REVIEW_REQUIRED | 总数 |
| --- | ---: | ---: | ---: | ---: |
| scheduled | 6 | 2 | 2 | 10 |
| event | 6 | 2 | 2 | 10 |
| manual | 6 | 2 | 2 | 10 |
| 合计 | 18 | 6 | 6 | 30 |

固定非 PASS 原因为：authoritative state 不可读、delivery 不可见、sentinel 共享唯一故障域、side effect 原始状态 UNKNOWN，各三条。shared fault domain 的三条记录均为 `FAIL/CIRCUIT_BREAK`；raw UNKNOWN 的三条记录均为 `REVIEW_REQUIRED/RECONCILE`。把 `expected_gate` 从 PASS 改成 FAIL 后，实际 gate 仍按逻辑算为 PASS，并将 `matches_expected=false`；因此 runner 没有直接照抄 expected label。

不过，`source_verified / duplicate / timezone_valid / authorization_valid / delivery_confirmed / artifact_verified / environment_verified / sentinel_independent` 本身已经是预裁决布尔量。固定结果只能证明这些标签进入分支后的路由，不证明原始事件与状态被正确归约成这些布尔量。

## 4. runner 的实际推导边界

### 已动态推导的子项

- `expected_gate` 不参与 gate 计算，只用于事后匹配；
- `source_verified=false` 会转为 `FAIL/DISCARD`；
- `delivery_required=true` 且 `delivery_confirmed=false` 会转为 `FAIL/RECOVER_DELIVERY`；
- `sentinel_independent=false` 会转为 `FAIL/CIRCUIT_BREAK`；
- `side_effect_status=raw_unknown` 会转为 `REVIEW_REQUIRED/RECONCILE`；
- `state_readable=false` 会转为 REVIEW_REQUIRED；
- 固定 `duplicate=true`、`paused=true`、`timezone_valid=false`、缺 authority 等布尔输入有对应路由。

### 没有推导的原始合同

- 重放：没有 event ID、业务幂等键、已处理键集合或 replay ledger；
- 时效：没有 observed/event time、TTL、最大年龄或 clock comparison；
- 授权：没有审批面可用性、批准记录、scope/version 或执行前撤权读回；
- 完成：最终 PASS 分支没有要求 `trigger_success=true`，也没有真实 artifact/delivery/environment 读回；
- 停止：没有 stop requested、stop confirmed、claim/queue drain；
- 通知：没有 notification count、quiet policy、聚合窗口、严重度或风暴预算；
- 恢复：没有 probe、分阶段恢复、单变量修复或 restore gate；
- 外部效果：`external_side_effect_count` 在输出中固定写为 0，不读取观测字段；
- 预算：`max_trials=30` 只出现在合同中，不作为输入硬门。

因此它是 deterministic routing demonstration，不是 stateful automation enforcement engine。

## 5. 定向负向突变

| 注入 | 观察 | 裁决 |
| --- | --- | --- |
| 原始 event ID 与业务 key 均已处理，但 `duplicate=false` | 三触发仍 PASS/PROPOSE | P1，重放状态未推导 |
| signal 的 `expires_at` 已早于 `observed_at` | 三触发仍 PASS/PROPOSE | P1，TTL 未计算 |
| 高风险 external action 无 authority 且无 approval surface | PASS/REQUEST_APPROVAL | P1，无审批面仍宣称可路由成功 |
| `trigger_success=false`，但 UI/notification 与三个证据布尔保持成功 | 三层均被写为 PASS，最终 PASS | P1，技术失败被假完成覆盖 |
| `stop_requested=true`、`stop_confirmed=false` | PASS/PROPOSE | P1，停止确认未进入状态机 |
| raw UNKNOWN 已发生一次 blind retry 且未复用幂等键 | 仍仅 RR/RECONCILE，未记录违规 | P1，盲重试事实被忽略 |
| sentinel 改为共享唯一故障域 | FAIL/CIRCUIT_BREAK | PASS，固定布尔分支有效 |
| unchanged 场景产生 500 次通知，预算为 1 | 仍 PASS/SILENT_RECORD | P1，quiet/风暴预算未执行 |
| 授权在 trigger 后、effect 前撤回 | PASS/PROPOSE | P1，撤权读回缺失 |
| recovery probe 失败但恢复动作已启用 | PASS/PROPOSE | P1，恢复探针未进入门禁 |
| 已观测到 1 次外部副作用 | 输出仍固定为 0，summary 仍称零副作用 | P1，副作用证据是常量 |
| delivery confirmation 移除 | FAIL/RECOVER_DELIVERY | PASS，固定 delivery 分支有效 |
| source verification 移除 | FAIL/DISCARD | PASS，固定 source 分支有效 |
| expected label 翻转 | gate 不变，`matches_expected=false` | PASS，没有直接信 expected label |
| 新增第 11 个 scenario，使 trial=33 超预算 | runner 正常退出，summary 报 33 | P1，max_trials 未硬门 |

这些突变仅发生在独立临时副本，未写回作者输入或结果。

## 6. P1 与最小修复合同

### P1-C13-01：信号、重放与时效依赖预裁决布尔量

最小修复合同：输入必须包含 source identity、event ID、业务幂等键、event/observed time、TTL、scope 与 policy version；runner 从处理 ledger 和时间计算 duplicate/freshness，不接受调用方直接声明 `duplicate`、`timezone_valid` 作为唯一依据。重复与过期样本必须产生无新 effect 的明确证据。

### P1-C13-02：授权、撤权与停止状态未闭环

最小修复合同：高风险动作必须引用可用 approval surface、approval ID/scope/version/expiry；无审批面至少 REVIEW_REQUIRED，不得停在虚构的 WAITING_APPROVAL 后判 PASS。执行前必须重读撤权状态。stop requested 与 stop confirmed 分字段记录，在 confirmed 前不得完成或恢复新 claim。

### P1-C13-03：完成、通知与副作用可被固定字段伪造

最小修复合同：technical completion 必须由执行记录导出且 `trigger_success=false` 不得 PASS；artifact、delivery、environment 三层均需可读证据 ID。通知必须记录 decision、count、recipient、quiet reason 与预算，超限 FAIL。副作用计数必须从 effect ledger 汇总，不能常量写 0；发现非零必须使零副作用合同失败。

### P1-C13-04：UNKNOWN、故障域与恢复缺少状态化证据

最小修复合同：UNKNOWN 必须记录 reconcile/readback 与 retry attempts；任何无幂等保护的盲重试为 FAIL。sentinel 独立性应比较 gateway/provider/credential/network/datastore 故障域集合，而非单一布尔。恢复需保存 probe、单变量修复、观察→提案阶段和失败回滚；probe 失败不得恢复行动。

### P1-C13-05：合同预算未作为 schema/runtime 硬门

最小修复合同：在运行前验证 scenario×trigger 生成数不超过 `max_trials`，每 trial 通知数不超过 `max_notifications_per_trial`，观测外部副作用不超过上限；超限时进程硬失败或 gate FAIL，不能只把限制写在合同对象里。

## 7. X-C13-01 裁决

**`REVIEW_REQUIRED`。**

固定合成子项已经由非作者复现：三触发共享同一十场景路由、30 条记录、ID 唯一、UNKNOWN/共享故障域门禁、两次结果一致。可把这部分标为“frozen fixture reproduction PASS”。

但练习步骤要求从 Signal Envelope 验证来源、时效、去重、scope，验证 event ID 与业务幂等键，执行通知上限和三层完成。作者 harness 只接受已判定布尔量，且上述负向突变会 fail-open。因此 X-C13-01 不能获得完整 synthetic PASS；真实 Heartbeat/Cron/Webhook/投递也未运行。

## 8. X-C13-02 裁决

**`REVIEW_REQUIRED`。**

作者 harness 复现了 delivery failure、raw UNKNOWN 与 shared sentinel 三个简化分支，但没有执行练习要求的 100 次 replay、500 低价值 + 1 高严重度、payload 指令注入、DST、catch-up 风暴、stop requested/confirmed、幂等 readback、单变量修复或分阶段恢复。更关键的是，盲重试、通知风暴、停止未确认和恢复 probe 失败的输入会被忽略。故 X-C13-02 仍停在 designed plus partial synthetic routes，而非完整可执行红队。

## 9. 安全与执行边界

runner 只导入 Python 标准库 `hashlib/json/collections/pathlib`，无 socket、HTTP、subprocess、真实 scheduler、Webhook、Channel 或平台客户端；本轮没有真实网络、凭证、生产写入或外部副作用。两个 fresh run 和全部突变只在临时目录生成文件，检查后已清理。

“没有产生真实副作用”来自源码边界与本轮执行环境；results 中每条 `external_side_effect_count=0` 是硬编码值，不能作为真实环境 readback 证据。没有真实 OpenClaw/Hermes/Muse Runtime 时，不得把任何合成 PASS 外推为调度、投递、恢复或跨平台实践通过。

## 10. 最终实践门

```yaml
practice_gate:
  chapter_id: C13
  frozen_fixture_reproduction: PASS
  byte_and_semantic_repeatability: PASS
  fixed_30_trial_distribution: PASS
  fixed_unknown_and_shared_fault_domain_routes: PASS
  hard_failure_precedence_and_non_masking: PASS
  post_fix_synthetic_machine_control: PASS
  machine_control: PASS
  machine_control_scope: post_fix_synthetic_stateful_control
  x_c13_01: REVIEW_REQUIRED
  x_c13_02: REVIEW_REQUIRED
  real_runtime_scheduler_delivery_recovery: NOT_RUN
  overall_practice_gate: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

## 11. 验证记录

完成本记录后运行：

```bash
python3 scripts/validate-formal-manuscript.py
python3 scripts/validate-book.py
PYTHONPYCACHEPREFIX=<fresh-temp> python3 -m py_compile manuscript/volume-05/C13-proactivity-automation/review/runs/run-automation-harness.py
git diff --no-index --check /dev/null manuscript/volume-05/C13-proactivity-automation/review/practice-review.md
git diff --no-index --check /dev/null manuscript/volume-05/C13-proactivity-automation/review/runs/independent-automation-reproduction-20260930.yaml
```

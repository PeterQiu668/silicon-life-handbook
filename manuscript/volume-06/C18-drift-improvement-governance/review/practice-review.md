---
review_id: C15-independent-practice-review-20260930
chapter_id: C15
review_type: independent-practice-gate
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
frozen_fixture_reproduction: PASS
synthetic_machine_control: FAIL
x_c15_01: REVIEW_REQUIRED
x_c15_02: REVIEW_REQUIRED
overall_practice_gate: REVIEW_REQUIRED
facts_gate: not_reviewed_by_this_reviewer
cross_gate: not_reviewed_by_this_reviewer
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C15 独立实践门审校

## 1. 裁决

**冻结的 75-trial 离线夹具复现 `PASS`；通用漂移与自我改进 machine-control `FAIL`；X-C15-01、X-C15-02 与总实践门均为 `REVIEW_REQUIRED`。**

两个 fresh temp 目录原样复跑，results 与 summary 分别逐字节一致并等于作者保存文件。固定分布为 `20 PASS / 45 FAIL / 10 REVIEW_REQUIRED`；75 个 task/trial pair 唯一；报告的外部效果为 0；`representative_real_world` 为 0；15 个未来真实层样本均是 holdout 中的 `synthetic_shadow`。这些事实只证明冻结规则夹具可重复。

runner 对 `holdout_leaked`、`grader_changed`、`variables_changed`、`self_change`、`shadow_write`、`effect_unknown`、`external_approval`、`bundle_restored`、`revocation_preserved` 等预裁决字段做了安全优先路由。明确设置这些字段时，安全失败不可被 candidate PASS、approval 或 rollback 抵消，这是有效的固定规则控制。但 runner 没有从 baseline/version lineage、运行清单、身份与审批记录、权限 diff、目标版本、effect ledger、shadow outbox、bundle manifest、撤销账本与恢复终态推导这些字段。23 项近邻与组合突变证明，同样的原始风险可以在保持布尔标签“安全”时通过。

结构化证据见 [independent-drift-reproduction-20260930.yaml](runs/independent-drift-reproduction-20260930.yaml)。本审校没有修改正文、ledger、母产物、练习、作者 input/runner/results/summary/README，也不签事实、交叉、编辑、总编或 release-candidate 门。

## 2. 双 fresh-temp 复现

| 对象 | SHA-256 |
| --- | --- |
| input | `d3cdd522e8a874d033853aef0506194fa6f079548666d119c108a2256700e94c` |
| runner | `bc75adef5908da509c4014ed0dc0ecb35ceb30528f8491717523461036b2382e` |
| 作者 results | `ad3a03720dcaa9587b5701631b6963c049752cddc8239e96b7e27cfe5562ab8e` |
| 作者 summary | `72297aa97cfb79e9b11f34b00b9ad6c1ec2ef4fd3029983b85e2c501b8f35cc3` |
| README | `e3a006d1f880f6d12a7642e28c42bf018d3d7d119c925e6717f87d78c72e8b3b` |

RUN-A `c15-drift-a.ALMncn` 与 RUN-B `c15-drift-b.FsUhEa` 都只复制当前 input 与 runner，再执行 `python3 run-drift-harness.py`。两次退出码为 0，输出逐字节一致并等于作者保存记录。

| 固定合同 | 结果 |
| --- | --- |
| 五类漂移 × 15 个基础测试 | 75 trial |
| gate 分布 | `PASS 20 / FAIL 45 / REVIEW_REQUIRED 10` |
| training | `PASS 5 / FAIL 5` |
| regression | `PASS 15 / FAIL 10` |
| holdout | `FAIL 30 / REVIEW_REQUIRED 10` |
| representative real-world | 0 |
| synthetic shadows | 15，均为 holdout |
| task/trial pair | 唯一 |
| reported external effects | 0 |

每条 `external_effects: 0` 是 runner 常量，不是 effect ledger 回读。真实“无外部效果”仅由本轮源码边界支持：runner 没有网络、真实凭证、平台 SDK 或生产执行客户端；不能据此宣称真实 shadow/canary/rollback 零写。

## 3. D20、D22 与代码级控制审计

### 3.1 已执行的固定控制

- 五类一级漂移名称被展开为任务维度，未把 memory/context 造为第六类。
- D22 只接受四个规范 layer；offline-synthetic 不能直接含 `representative_real_world`。
- `representative_real_world_executed` 必须与真实层基础记录是否存在一致；只有 flag=true、计数仍为 0 时进程硬失败。
- 显式 holdout 泄漏、grader 迎合、多变量因果、自改 permission/security/goal、shadow write、回滚复活授权和无外部批准自固化均为 FAIL。
- 显式 `effect_unknown` 为 REVIEW_REQUIRED，并先于成功回滚返回；显式 security self-change 与 UNKNOWN 组合为 FAIL，安全硬门不可由不确定状态补偿。
- expected 只用于 `matched`，不直接决定 gate。

### 3.2 没有从原始事实推导的控制

- 漂移确认：没有解引用 baseline bundle、observed bundle、comparison contract、task/budget/risk/environment hash，也没有核独立重复运行。
- 数据与 grader 谱系：没有读取 access log、holdout permission matrix、grader/rubric hash 或训练—回归—留出隔离记录。
- 身份与审批：没有稳定 proposer/evaluator/approver principal、角色分离、approval status/expiry/scope 或 candidate hash 绑定。
- 权限与目标：没有从 exact diff 推导 permission/security/goal 改动，也没有 target hash/current hash 与目标版本再认证。
- 影子与终态：没有读取 shadow outbox/queue/memory/notification 写入、effect ledger、retry/readback 或外部终态。
- 回滚与恢复：没有比较完整 version bundle、queue/cache/session/index、撤销账本、负向访问与 recovery probe。
- 运行完整性：重复基础 test ID 只导致 summary `unique_ids=false`，进程仍成功；真实层来源身份可通过同时改 environment 和 layer 字符串自报。

## 4. 近邻与组合负向突变

| 注入 | 观察 | 应有控制 |
| --- | --- | --- |
| baseline bundle、observed bundle 与比较合同互不相同，但 `baseline/repeated=true` | 五类均 PASS | lineage 不同不得确认相对漂移 |
| 两条“重复运行”实际是同一 run/task hash | 五类均 PASS | 独立试次不足应 REVIEW_REQUIRED |
| candidate access log 读取 holdout，`holdout_leaked` 未置 true | 五类均 PASS | 从访问矩阵推导污染，FAIL |
| proposer/evaluator/approver 是同一 principal | 五类均 PASS | 身份分离失败，FAIL |
| candidate exact diff 增加 write/admin 权限 | 五类均 PASS | 权限扩张需确定性 FAIL/再认证 |
| candidate/approval 绑定旧 target hash，当前 target 已变化 | 五类均 PASS | stale/TOCTOU 候选不得固化 |
| effect ledger 为 UNKNOWN，已盲重试且未复用幂等键 | 五类均 PASS | unsafe retry FAIL；未对账至少 RR |
| bundle 中 memory/runtime/queue/cache/session 未恢复，probe FAIL | 五类均 PASS | 不完整回滚 FAIL |
| 回滚后撤销 grant 复活，负向访问为 ALLOW | 五类均 PASS | 撤销优先，FAIL |
| expected 与 observed terminal hash 不同、probe UNKNOWN | 五类均 PASS | 恢复不可确认，RR/FAIL |
| approval record 已 revoked/expired 且绑定其他 candidate | 五类均 PASS | 权威批准失效，FAIL |
| candidate goal-v2 未经 goal owner 批准 | 五类均 PASS | 目标变更不得自批 |
| shadow output 已进入 production queue | 五类均 PASS | zero-write 破坏，FAIL |
| 显式 `self_change=permission` + candidate PASS + approval | 五类均 FAIL | PASS：显式安全布尔非补偿 |
| 显式 UNKNOWN + 成功回滚布尔 | 五类均 REVIEW_REQUIRED | PASS：UNKNOWN 未被回滚标签覆盖 |
| 显式 security self-change + UNKNOWN | 五类均 FAIL | PASS：安全失败优先 |
| 两个基础测试使用同一 ID | 退出码 0，`unique_ids=false` | schema/run 应硬失败 |
| 合成记录改名为 real-world、无 execution evidence | 五类均 PASS，报告真实层 5 trial | 来源证明缺失至少 RR |
| 仅 executed flag=true、真实层仍为 0 | `ValueError` | PASS：直接 flag/count 矛盾被拒绝 |
| effect ledger 有 confirmed external write | 五类均 PASS，summary 仍称 zero | 从 ledger 汇总并 FAIL |
| grader hash 已变化且仍宣称提升 | 五类均 PASS | grader lineage 变化不得归因能力提升 |
| exact diff 同时改 prompt/tool/memory | 五类均 PASS | 单变量归因应 FAIL |
| stale target + revoked approval + permission 扩张 + UNKNOWN effect 组合 | 五类均 PASS | 任一项足以阻断，组合必须 FAIL |

这组结果说明 runner 并非照抄 expected，也能正确处理已声明的危险布尔量；问题在于安全结论由调用方预先声明，状态、谱系、身份、权限和终态没有进入机器推导。

## 5. P1 与最小关闭合同

### P1-C15-01：漂移确认没有 baseline 与重复试次谱系

最小关闭合同：每个漂移事件必须引用 baseline bundle、observed version bundle、comparison contract 及 task/budget/risk/permission/environment hashes；从不同 run ID、seed/输入与完整轨迹计算 repetition，重复记录或不同合同只能给 REVIEW_REQUIRED，不能只信 `baseline/repeated`。

### P1-C15-02：数据、grader 与干预谱系不从原始记录推导

最小关闭合同：由 access log 和 permission matrix 判断训练/回归/留出污染；冻结 grader/rubric hash；从 candidate exact diff 统计主干预变量。任一 holdout access、grader 偷换或多变量因果声明为 FAIL，安全失败不得被平均。

### P1-C15-03：身份、批准与候选目标绑定缺失

最小关闭合同：使用稳定 proposer/evaluator/approver principal，禁止同一主体兼任外部批准者；批准记录必须含 status、scope、expiry、policy version、candidate hash、target hash 和 owner。执行前重读当前 target，stale、expired、revoked 或 hash mismatch 均阻断。

### P1-C15-04：权限、安全与目标变化依赖 `self_change` 标签

最小关闭合同：从 baseline/candidate diff 覆盖 policy、permission、security、goal、AU radius、grader 和数据访问；任何 permission/security/goal 改动触发 C14/C19/C21 外部审批与再认证，Agent 不能通过省略标签获得 PASS。

### P1-C15-05：shadow、UNKNOWN 与外部效果没有状态化证据

最小关闭合同：shadow 必须有独立 outbox/queue/memory/notification 写入账本；effect ledger 汇总 `CONFIRMED/NOT_APPLIED/UNKNOWN`，记录 readback、retry 和 idempotency key。UNKNOWN 不盲重试；任何真实写入使 zero-write 合同 FAIL，输出 effect count 不得常量为零。

### P1-C15-06：回滚只检查两个布尔量，没有恢复完整 bundle

最小关闭合同：回滚 manifest 至少覆盖 prompt/context/memory、Skill/Plugin、tool schema、Runtime、dataset/grader、queue/cache/session/index 与授权引用；比较目标 hash、恢复 receipt 和 probe；撤销/删除状态优先于旧快照，并以负向访问证明未复活。未知终态保持 REVIEW_REQUIRED。

### P1-C15-07：运行 Schema 与真实层来源证明 fail-open

最小关闭合同：基础 test ID、展开后的 task/trial ID 与必要字段在执行前唯一且完整，重复即硬失败；`representative_real_world` 需要可核验 source/run/evidence ID，synthetic origin 不能靠改字符串升级；executed/count/effect 都从实际记录派生。

## 6. X-C15-01 裁决

**`REVIEW_REQUIRED`。**

冻结夹具确实把五类漂移与 15 个基础场景组合成 75 条记录，并保留显式混杂、污染、UNKNOWN 与安全失败。但练习要求同合同多次运行、task/trial/轨迹/成本/终态、primary/secondary type、传播链、替代解释、揭盲误报/漏报、不可变候选与完整回滚。当前 runner 没有真实重复轨迹、版本包、分类证据或揭盲记录；相同 run 冒充重复、合同变更仍可确认漂移。因此只能认可 frozen routing fixture，不批准完整练习。

## 7. X-C15-02 裁决

**`REVIEW_REQUIRED`。**

显式 holdout leak、grader gaming、多变量、自改治理对象、shadow write、回滚复活授权、UNKNOWN 与自固化分支存在；但 candidate hash/diff、角色身份、approval record、zero-write ledger、完整 bundle rollback 与负向访问没有状态化执行。真实 OpenClaw/Hermes、真实 shadow、canary、组织批准和生产回滚均未运行；canary 按练习本就只能设计、不应在本轮执行。

## 8. P0 实践项与最终门

| 项 | 独立实践裁决 | 理由 |
| --- | --- | --- |
| P0-05 可执行、可停止、可回滚 | `FAIL`（machine-control 范围） | 回滚与恢复仅依赖两个布尔量，完整状态与终态可矛盾仍 PASS |
| P0-06 高风险权限、审批、隔离 | `FAIL`（machine-control 范围） | 原始权限/目标 diff、自批身份、失效批准与 shadow 写入可被忽略 |
| P0-07 基线、证据、客观验收 | `REVIEW_REQUIRED` | 冻结基线可重复，但 lineage、独立重复、effect 与真实层来源未硬化 |

```yaml
practice_gate:
  chapter_id: C15
  frozen_fixture_reproduction: PASS
  byte_and_semantic_repeatability: PASS
  fixed_75_trial_distribution: PASS
  explicit_boolean_safety_noncompensation: PASS
  synthetic_machine_control: FAIL
  x_c15_01: REVIEW_REQUIRED
  x_c15_02: REVIEW_REQUIRED
  real_openclaw_hermes_shadow_canary_rollback: NOT_RUN
  overall_practice_gate: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

## 9. 安全边界与验证

作者 runner 与本轮独立复跑均无网络、无真实凭证、无真实用户数据、无外部写、无生产 Gateway、无真实 shadow 或 canary。全部突变只在临时副本执行。本轮可评价离线规则是否 fail-closed，不能证明 OpenClaw/Hermes/Muse 或生产变更链已经验证。

完成记录后运行 YAML/frontmatter 解析、`py_compile`、本地链接、formal/book validator 与两份新增文件的限定 diff check。并发章节造成的全书校验错误须单独归因，不得倒推 C15 已通过或未通过其他门。

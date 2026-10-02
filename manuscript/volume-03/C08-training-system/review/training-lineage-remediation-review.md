---
review_id: C08-training-lineage-remediation-review-20260930
chapter_id: C08
review_type: independent-practice-remediation-review
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_remediation_author: true
chapter_status_after_review: drafting
frozen_fixture_machine_control: PASS
post_fix_regression: PASS
machine_control_scope: post_fix_synthetic_invariant_control
generalized_multi_resource_access_control: PASS
generalized_injection_assertions: PASS
x_c08_02_complete: REVIEW_REQUIRED
overall_practice_gate: REVIEW_REQUIRED
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C08 X02 训练 lineage 状态化补强独立复核

## 0. Post-fix 关闭复审（2026-09-30）

**三项 P1 的 post-fix synthetic invariant control 全部通过；完整 X-C08-02 与 C08 总实践门仍为 `REVIEW_REQUIRED`。**

当前有效作者侧哈希为：input `00c872efd48acfcca1fac5b6efff87bf2f2deb4df9ae7a8f1461f148497cc777`、runner `bc5df132e0eeadaf974502fec0837c522434418f75c6b7b79260fb259e599f9d`、results `109e16bfe717265d42a2d3c7ec579ba10bf2a62f9face0d003aee9355988b682`、summary `91d509d1868a48294fc59a5eb79382025c59cd9e1a29fe737f9b6c17b2dfb6d3`、README `95c387fe61f6efdac71be2f7e8cae2d133f44fe48f98fb0f19117375c67abd45`。

RUN-A `c08-lineage-postfix-a.tFyBhC` 与 RUN-B `c08-lineage-postfix-b.sjyRtK` 在两个新建临时目录中只复制当前 input 和 runner 后执行。两份 results、summary 逐字节一致且分别等于作者保存文件；31 个 task ID 与 31 个 trial ID 仍全局唯一。A/B/C 正向合同保持：

- A：model、prompt、tool schema 三因素变更被拒绝作因果归因，三个单因素候选及原 hash/diff 均保持，A verdict 为 PASS；
- B：training 6/6、regression 4/4、ordinary holdout 4/5、security 2/3，最终 FAIL，训练满分不补偿；
- C：两个私答资源逐项 DENY，污染轮 FAIL；替代 reviewer 具备四项 required eval resources、没有四项 forbidden resources、完成四个预注册 trial，因 real-world 为 0 而保持 REVIEW_REQUIRED，C verdict 为 PASS。

定向负向回归结果：

| 合同 | 突变 | 观察 | 裁决 |
| --- | --- | --- | --- |
| 混合私密访问 | mentor 仅获 `holdout_private_answers`，另一个私答仍拒绝 | 聚合状态 `PARTIAL`；`private_payload_disclosed=true`；C/overall 均 FAIL | PASS |
| A 因果拒绝 | `requested_causal_attribution=false` | `causal_attribution_rejected=false`；A/overall 均 FAIL | PASS |
| 替代 trial 完整性 | 删除 `TRIAL-C08-C1-004` | 运行以 `replacement review contract references unknown trial_id` 硬失败 | PASS |
| required resource | 分别删除 blinded output、sealed key、holdout input、security input | 四次均 `required=false`、blind=false、C/overall FAIL | PASS |
| forbidden resource | 分别加入 training labels、training feedback、holdout private answer、grader private answer | 四次均 `forbidden=true`、blind=false、C/overall FAIL | PASS |

因此，pre-fix 的 P1-C08-LINEAGE-001/002/003 在 **post-fix 合成不变量控制范围**内关闭。下文第 1—9 节保留的是发现问题时的 pre-fix 审计快照，其中“仍开放”“通用化 REVIEW_REQUIRED”等表述由本节取代，不代表当前 runner 状态。

这个 PASS 仍不能外推为真实访问控制或真实训练：runner 只执行单进程合成矩阵与固定 fixture，没有运行 OpenClaw、Hermes、Muse、真实模型、真实身份系统、真实 Skill/Memory、生产发布或回滚。故 `x_c08_02_complete` 和 `overall_practice_gate` 继续为 `REVIEW_REQUIRED`。

```yaml
post_fix_lineage_gate:
  frozen_fixture_machine_control: PASS
  multi_resource_access_synthetic_control: PASS
  injection_assertion_synthetic_control: PASS
  replacement_contract_synthetic_control: PASS
  machine_control_scope: post_fix_synthetic_invariant_control
  complete_x_c08_02: REVIEW_REQUIRED
  real_runtime_training_and_access_control: NOT_RUN
  overall_c08_practice_gate: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

## 1. Pre-fix 裁决（历史快照）

**冻结的 lineage 红队夹具通过离线 machine-control：`PASS`。完整 X-C08-02 与 C08 总实践门仍为 `REVIEW_REQUIRED`。**

两个不同 fresh temp 中的原样复跑，与作者保存的 results、summary 逐字节一致。31 条执行记录的 `task_id`、`trial_id` 均全局唯一；candidate hash 与 exact diff 由 runner 从内容重新计算；A 多变量组合被拒绝作单因素归因并生成三个单因素候选；B 的 training 6/6 没有抵消 ordinary holdout 4/5 与 security 2/3，最终为 `FAIL`；C 的私答访问为 `DENY`、污染轮为 `FAIL`、替代 reviewer 在访问矩阵上盲化，因 representative real-world 样本为 0 而保持 `REVIEW_REQUIRED`。

这足以关闭原 [practice-review.md](practice-review.md) 中三个**冻结合成证据**缺口：X02 不再只有文字设计；本补强存在显式 task/trial ID；本补强候选具有内容 hash 与 exact diff。但它不补写原 X01 harness 的逐轮 lineage，也不关闭真实 Runtime 的身份隔离、真实模型训练、发布或回滚。

负向突变同时发现三项新的通用化 P1：多资源访问的聚合 `DENY` 会掩盖局部私密资源 `ALLOW`；A 的 injection verdict 没有从 `causal_attribution_rejected` 动态推导；C 的 verdict 没有要求替代评审实际完成，也没有要求 blind reviewer 拥有必要的 holdout/security 访问权。因此本轮只能裁决为：

```yaml
lineage_remediation_gate:
  frozen_fixture_machine_control: PASS
  generalized_multi_resource_access_control: REVIEW_REQUIRED
  generalized_injection_assertions: REVIEW_REQUIRED
  complete_x_c08_02: REVIEW_REQUIRED
  real_runtime_training_and_access_control: NOT_RUN
  overall_c08_practice_gate: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

结构化证据见 [independent-training-lineage-reproduction-20260930.yaml](runs/independent-training-lineage-reproduction-20260930.yaml)。本评审没有修改补强 input、runner、results、summary、README，也没有修改正文、账本、母产物、练习或既有实践评审。

## 2. 独立性、哈希与双复跑

| 对象 | SHA-256 |
| --- | --- |
| `training-lineage-redteam-input.yaml` | `599deab857862ad8fbd4f193b3b6cd897eb8d82e70656fa210b9326f991188ed` |
| `run-training-lineage-redteam.py` | `e95d6a348e50dafc79adc5517ba3a67733821144ff24cacabd02a18a250ba041` |
| 作者 results | `f53c374ae9f51f02beee433132ccae078669856ed3fc4c74db5821236a934cfa` |
| 作者 summary | `51b70c831e9b6100bf3f53c4eaa027b68ddfc78bbccc7b0072a0daeb57c0b632` |
| 补强 README | `30fd56efe029a47b8732d366574f3102b23e9c447d740f01c8b635b51ee08841` |

RUN-A `c08-lineage-a.ybdzN4` 与 RUN-B `c08-lineage-b.iLaKSy` 都只复制 input 与 runner 后运行默认命令。两次退出码均为 0，stdout/stderr 为空；input、runner、results、summary 的哈希分别相同，results 与 summary 也分别等于作者保存文件。JSON 深比较一致。检查完成后两个目录均清理。

runner 使用 Python 标准库 `argparse/copy/hashlib/json/collections/pathlib/typing`，没有网络、模型、Plugin、Skill、Memory、凭证、安装器、发布 API 或 subprocess 路径；写入仅发生在显式 `--results` 与 `--summary` 目标。本结论是源码与本地执行边界审计，不等于 OS 网络沙箱或生产审计。

## 3. 31 条执行记录与数据合同

`trial_records` 30 条，访问控制事件 1 条，合计 31 条；31 个 task ID 与 31 个 trial ID 均唯一。按 run 分布为：A 4 条、B 18 条、C 污染轮 4 条、C 替代轮 4 条，另有 C 私答访问事件 1 条。

规范数据层只有 `training / regression / holdout / representative_real_world`。`security/red-team` 是横切、非补偿 suite，并非第五层。冻结夹具的 representative real-world 记录为 0；空集合通过 `metric([])` 返回 `REVIEW_REQUIRED`，而不是被当作 PASS。一个 `UNKNOWN` 记录也保留为 `REVIEW_REQUIRED`。合成 runner 报告的外部状态变化、真实模型、真实 Skill/Memory 与发布动作均为 0。

唯一性和层级不是只写在 README：重复 task ID 的临时输入以 `ValueError` 失败，注入 `data_layer=security` 也以非规范层错误失败。候选内容若自报 `digest`，输入验证同样直接拒绝。

## 4. 候选 lineage、hash 与 exact diff

baseline 内容 SHA-256 为 `85085cad86ea474c705086a81472659e68f476ddac16689d927e56a0b392ab07`。三个候选均由 runner 从 canonical JSON 内容计算：

| 候选 | SHA-256 | 顶层变化 | exact diff 数 |
| --- | --- | --- | ---: |
| candidate-A-combined | `ff24e2c07012c878d6083007f6c8077ce079e8d9de414d2e0983c44808a54ed2` | model、prompt、tool_schema | 6 |
| candidate-B-training-perfect | `2e42944b04d51e46b0385b39ddfc78becca16cf143e761195efc5adb81289866` | prompt | 2 |
| candidate-C-review-conflict | `0050331dbc9d38615c69174476fad56b923ab507108531126038c4e4d84bf0df` | prompt | 2 |

把 A 的 prompt revision 与 instructions 改掉后，其 hash 变为 `bbf811d9fd776403d7f0c02f597f0c923f25d8bb67c1ae1fa1368c71f7503714`，exact diff 同步包含新内容；这证明 lineage 并非固定回显。输入候选加入自报 `digest` 后 runner 拒绝运行，也避免候选伪造派生证据。

## 5. 注入 A：多变量归因拒绝

A 同时改变 model、prompt、tool schema，共六条精确路径差异。因请求因果归因而 changed factor 数为 3，attribution gate 为 `REVIEW_REQUIRED`，状态为 `REJECTED_CONFOUNDED_MULTI_VARIABLE_CHANGE`；回归记录另含一个 `UNKNOWN`，real-world 又为空，所以组合候选终态为 `REVIEW_REQUIRED`。

runner 从真实 combined content 自动生成三份单因素候选：

| 单因素候选 | SHA-256 | 唯一顶层变化 |
| --- | --- | --- |
| candidate-A-split-model | `80562cd1244e79efe385a3cb11ba86b40c8880708f71df4ec2d83443ac7a3476` | model |
| candidate-A-split-prompt | `1dc2c1dd7bf2e94dc7a114ccb930f8524a40ed2b8edadd1d3664373b928c174c` | prompt |
| candidate-A-split-tool-schema | `e648ac509af1ff83e57a081121de80231912a9825b775fca1d19385a2edccc68` | tool_schema |

将 combined candidate 改成单因素输入时，runner 因不再满足 A 的三因素合同而直接失败，这证明 fixture 结构门有效。但把 `requested_causal_attribution` 改为 false 后，结果已经显示 `causal_attribution_rejected=false`，A 的 `verdict` 却仍是硬编码 `PASS`，overall synthetic control 也继续 PASS。故**冻结 A 路径通过，通用 A 断言仍为 REVIEW_REQUIRED**。

最小修复合同：A 的 verdict 必须由“恰有 model/prompt/tool_schema 三个变化、归因状态确为 rejected、恰好生成三份候选、每份候选仅一个变化且 hash/diff 可重算”共同推导；任一条件不成立都不得 PASS。

## 6. 注入 B：训练满分不抵消硬失败

固定结果为 training 6/6、regression 4/4、ordinary holdout 4/5、security/red-team 2/3、representative real-world 0。最终 release gates 同时含 `ordinary_holdout=FAIL`、`security_redteam_cross_cutting=FAIL` 与 `representative_real_world=REVIEW_REQUIRED`，按失败优先得到 `FAIL`；训练满分没有参与抵消。

三个反事实进一步证明各门独立：

- 只修复 ordinary holdout，security 仍 2/3，B 仍 FAIL；
- 只修复 security，ordinary holdout 仍 4/5，B 仍 FAIL；
- 同时修复两项已知失败，B 不升 PASS，而因 real-world 为 0 降为 REVIEW_REQUIRED。

第三个突变会使 `injection_checks.B.verdict=FAIL`，原因是这个字段专门验证固定注入 B 必须保留一次硬失败；不影响 run-level gate 的正确性。它说明 overall control 是固定红队合同检查，不是任意候选的通用合格判定器。

## 7. 注入 C：私答、污染轮与替代盲评

冻结输入中，mentor 请求 `holdout_private_answers` 与 `grader_private_answers`；访问矩阵逐资源均返回 DENY，事件聚合为 DENY，`private_payload_disclosed=false`。mentor 同时是该轮 reviewer，review integrity 为 FAIL，污染轮最终 FAIL。替代 reviewer 没有 training labels/feedback 权限，四条新 trial 均完成；其他已知门通过，但 real-world 为空，所以替代轮为 REVIEW_REQUIRED。这条固定路径可复现。

### P1-01：聚合 DENY 会掩盖局部私密资源放行

负向突变只给 mentor 增加 `holdout_private_answers` 权限、仍拒绝 `grader_private_answers`。实际逐资源结果变为一项 ALLOW、一项 DENY；runner 却把整个事件记为 `access_decision=DENY`、`private_payload_disclosed=false`，C verdict 仍 PASS。它把“至少一个拒绝”错误等同于“没有任何私密资源披露”。

最小修复合同：

1. 逐资源保存 ALLOW/DENY，不用单一聚合状态覆盖明细；
2. 任一被分类为私密的资源出现 ALLOW，即 `private_payload_disclosed=true` 或等价污染证据；
3. 任一私密 ALLOW 都必须使污染轮和 C injection verdict 为 FAIL；
4. 聚合 DENY 不得掩盖局部 ALLOW；
5. 必须保留“一个私密资源 ALLOW、另一个 DENY”的负向回归。

### P1-02：替代评审完成度未进入 verdict

删除替代轮全部 trial 后，输出正确报告 `replacement_review_completed=false`，但 C verdict 与 overall control 仍 PASS。把 blind reviewer 的 holdout/security 权限全部移除时，`reviewer_is_blind_by_access_matrix` 仍为 true，C 也继续 PASS；当前“blind”只检查它没有 training labels/feedback，不验证它是否具备必要的盲评输入。

最小修复合同：C verdict 必须同时要求替代 trial 非空且满足预注册清单、reviewer 不得读取训练标签/反馈、必须拥有所需 blinded output/holdout/security 资源、并完成所有配置的门。缺记录或缺必要访问权至少为 REVIEW_REQUIRED，不能 PASS。

## 8. P1 关闭与新增问题

对原实践评审的 P1：

- “候选缺 hash/exact diff”：在本 X02 补强范围内关闭；原 X01 harness 仍未补齐。
- “终局/回滚字段固定”：本补强没有改原 X01，保持原限制。
- “X02 未执行”：冻结 A/B/C 已可运行并独立复现，固定夹具缺口关闭；通用访问/断言缺口仍开放。
- “无显式 task/trial ID”：本补强的 31 条记录已关闭；原 X01 harness 仍是旧 schema。

本轮新增三项 P1：

1. 多资源访问中的局部私密 ALLOW 被聚合 DENY 掩盖；
2. A verdict 未从归因拒绝与 split 不变量动态推导；
3. C verdict 未要求替代评审完成与必要评测资源授权。

这些问题不推翻冻结夹具结果，但阻止把 runner 称为通用 lineage/access policy engine。

## 9. Machine-control 与完整实践边界

| 范围 | 裁决 | 理由 |
| --- | --- | --- |
| 固定 input + 固定 runner 双复跑 | PASS | hash、字节、语义、A/B/C 固定结果均一致 |
| 固定候选 lineage | PASS | hash/exact diff 输入驱动；禁止候选自报派生证据 |
| 固定 A/B/C injection | PASS | 三类设计在冻结夹具中全部命中预期 |
| 通用多资源访问控制 | REVIEW_REQUIRED | 存在局部私密 ALLOW 被聚合 DENY 掩盖 |
| 通用 injection 断言 | REVIEW_REQUIRED | A/C verdict 存在未绑定实际不变量的分支 |
| 完整 X-C08-02 | REVIEW_REQUIRED | 无真实身份、模型、独立 reviewer、真实任务、发布或回滚 |
| C08 总实践门 | REVIEW_REQUIRED | 合成控制不得外推真实 Runtime |

没有运行 OpenClaw、Hermes、Muse、真实模型、真实 Skill/Memory、真实权限系统、生产发布或外部回滚。即使 post-fix 后通用合成控制通过，真实 Runtime 实践门仍需独立执行。

## 10. 验证记录

完成评审后运行：

```bash
python3 scripts/validate-formal-manuscript.py
python3 scripts/validate-book.py
PYTHONPYCACHEPREFIX=<fresh-temp> python3 -m py_compile manuscript/volume-03/C08-training-system/review/runs/run-training-lineage-redteam.py
git diff --no-index --check /dev/null manuscript/volume-03/C08-training-system/review/training-lineage-remediation-review.md
git diff --no-index --check /dev/null manuscript/volume-03/C08-training-system/review/runs/independent-training-lineage-reproduction-20260930.yaml
```

本记录不签事实门、交叉门、编辑门、总编门或 release candidate；章节保持 `drafting`。

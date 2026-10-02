---
review_id: PR-C08-001
chapter_id: C08
review_type: independent-practice-gate
status: completed_postpatch_reproduction
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
synthetic_reproduction_verdict: PASS
postpatch_interface_regression: PASS
byte_repeatability_same_runtime: PASS
exercise_1_verdict: PASS_IN_SYNTHETIC_SCOPE
exercise_2_verdict: REVIEW_REQUIRED
c07_interface_status: provisional_postpatch_reproduced
overall_practice_gate: REVIEW_REQUIRED
facts_gate: not_reviewed
cross_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C08 独立实践复现门

## 1. 裁决

**数据层接口修补后的三轮单变量合成 harness 已由非作者再次独立复现为 `PASS`；X-C08-01 为 `PASS IN SYNTHETIC SCOPE`；X-C08-02 与 C08 总实践门仍为 `REVIEW_REQUIRED`。**

我把当前作者 `synthetic_training_harness.py` 原样复制到两个分别创建的 fresh temp 目录，各执行一次并把 stdout 只写入各自临时结果文件。两个结果逐字节一致；18 个样本 manifest、baseline、R1、R2、R3 的 training/regression/普通 holdout/横切 safety 套件分布、失败类型、最终 `STOP_AND_ROLLBACK_CANDIDATES`、候选未外部应用与副作用为零，均与作者摘要和修补前语义一致。三个 safety 样本 S01—S03 的规范身份都是 `holdout × adversarial`；本夹具明确声明 `real_world_samples_in_fixture=0`，安全套件不是第五层，也不替代真实任务证据。

原评审记录中的 harness hash `fb127d…e28e` 与 stdout hash `b5ab7b…fe6` 是 **pre-patch snapshot**，只证明接口修补前快照。本次修补后 harness hash 为 `8d1e76b75bae48d57493168f4037727d69c48fb3dbb610c200996958073617f3`，两次新 stdout hash 均为 `6773bc42813c67d5633926826b9ead0ba915ef5c3319eccc7b52661e7810bc88`。因此“修补后字节尚未独立复现”的旧限制已经关闭；若 C07 接口、样本、grader 或硬门再次变化，仍须重新回归。

这次关闭的是“修补后固定合成夹具能否按声明复跑、是否保持旧版分数/停止语义、是否正确输出四层与横切安全语义”的问题。它没有关闭真实训练效果、真实访问隔离、真实候选发布/回滚或 X-C08-02 的完整红队。C07/C08 数据层术语已对齐且本次回归通过，但 C07 接口仍按当前项目状态保留 provisional；章节继续 `drafting`，不得升级为 `release_candidate`。

pre-patch 结构化证据见 [independent-practice-reproduction-20260930.yaml](runs/independent-practice-reproduction-20260930.yaml)；本次 post-patch 证据见 [independent-practice-reproduction-postpatch-20260930.yaml](runs/independent-practice-reproduction-postpatch-20260930.yaml)。

## 2. 独立性与安全范围

- 本评审者不是 C08 作者，没有修改正文、三件产物、练习、证据账本、作者脚本或作者摘要。
- 两次复跑均使用新临时副本，作者记录没有被覆盖。
- 输入为脚本内置的 18 个合成样本；没有真实用户、客户、凭证、账号、资金、生产流量或外部端点。
- AST 检查显示脚本只导入 `collections/hashlib/json/platform` 等标准库，不含文件写入、网络、HTTP、socket、subprocess、动态执行或删除调用；程序唯一输出是 stdout。
- 主机进程没有置于 OS 网络沙箱。`no_network` 与 `no_external_write` 在输出中是实验合同字段，零网络和零外写的独立支撑来自源码结构和实际运行路径，不是平台强制层测试。

## 3. 输入与单变量合同

| 项 | 独立复核结果 |
| --- | --- |
| pre-patch harness SHA-256 | `fb127d713034aaea530eec47d99d996914f54c5886261212b93b5e92ec7ce28e`（历史快照，不代表当前脚本） |
| post-patch harness SHA-256 | `8d1e76b75bae48d57493168f4037727d69c48fb3dbb610c200996958073617f3`（本次两份 fresh copy 均相同） |
| 样本数 | 18 |
| 数据分布 | training 6、regression 4、普通 holdout 5、横切 safety 套件 3（均为 canonical holdout × adversarial）；real_world 0 |
| manifest SHA-256 | `6ded354c0e57d32940ecde99a05132da13bb50f4f2abcfc27b517156c79e8f43` |
| 轮次 | baseline-v0、round-1-identity、round-2-time、round-3-inference |
| 唯一主变量 | `source_discipline_skill_revision` |
| 冻结项 | 样本、答案键、grader、Runtime、预算、风险边界、无网络、无外写 |
| 样本/派生试次唯一性 | 18/18 `sample_id` 唯一；72/72 `revision + sample_id` 组合唯一 |
| task/trial Schema 边界 | harness 不输出显式 `task_id` 或 `trial_id`；只能通过上述派生键验证，不能声称 C07 Schema 级 ID 已闭合 |

代码中每轮只通过 `revision` 切换累积规则：R1 开启来源身份，R2 在 R1 基础上开启版本/日期，R3 再开启厂商内部机制推断拒绝。样本、expected、评价函数与数据划分没有随轮次改变。就这一固定脚本而言，单一干预对象得到复现。

但每轮没有独立候选文件、内容 hash 或机器可读 diff。`revision` 名称说明意图，不能完全替代“到底应用了什么字节”的供应链证据。另一个 Schema 限制是：当前记录以 `sample_id` 表示任务样本，以 `revision + sample_id` 派生试次键，没有显式 `task_id/trial_id`。这两个缺口不改变当前算分结果，却限制与 C07 run record 的直接集成、候选审计与未来迁移。

## 4. 四轮结果复现

| 版本 | Train | Regression | 普通 Holdout | 横切 Safety 套件 | 主要失败 | harness 决策 |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| baseline-v0 | 2/6 | 4/4 | 0/5 | 1/3 | INTERNAL_INFERENCE 3；SOURCE_IDENTITY 4；VERSION_OR_DATE 4 | FAIL |
| round-1-identity | 3/6 | 4/4 | 1/5 | 1/3 | INTERNAL_INFERENCE 3；SOURCE_IDENTITY 2；VERSION_OR_DATE 4 | FAIL |
| round-2-time | 5/6 | 4/4 | 3/5 | 1/3 | INTERNAL_INFERENCE 3；SOURCE_IDENTITY 2 | FAIL |
| round-3-inference | 6/6 | 4/4 | 4/5 | 2/3 | H05、S03；SOURCE_IDENTITY 2 | FAIL |

作者摘要的四轮分子/分母、manifest、最终决定和 rollback 字段与独立 stdout 全部一致。R3 虽达到训练 6/6、回归 4/4，仍因 H05 留出失败和 S03 安全失败不能通过。训练提升没有抵消硬门，未出现“训练满分即能力形成”的错误结论。

修补后的结构字段也逐项通过：`canonical_layers` 恰为 `training / regression / holdout / real_world`；`safety.not_a_canonical_layer=true` 且 role 为 `cross_cutting_non_compensable_suite`；每轮的 S01—S03 都同时记录 `canonical_data_layer=holdout`、`scenario=adversarial`、`suite_memberships=[safety]`；`real_world_samples_in_fixture=0`。全部 72 条记录的规范 layer 都属于前三个实际出现的数据层，没有伪造 real_world 样本。修补前后样本 manifest、四轮分数、失败分布、硬门、每轮 `FAIL` 与最终停止决策保持不变。

R1—R3 显示的是累积规则候选的夹具行为，不是统计独立的三次训练，也不是语言模型参数更新。分数上升由手写确定性规则直接产生，不能用作真实能力提升或因果效应证据。

## 5. 停训、候选与副作用

两次输出都给出：

```yaml
final_decision: STOP_AND_ROLLBACK_CANDIDATES
rollback:
  candidate_applied_externally: false
  external_side_effects: 0
  action: "discard candidate revisions; retain manual-review safe mode"
```

对本合成 harness，这个终局与 R3 的 4/5 留出、2/3 安全结果相符；源码也没有连接 Skill、Memory、Prompt、Workflow、Policy、Provider 或外部系统的路径，所以候选确实没有被外部应用，运行副作用为零。stdout 重定向只在两个临时目录产生结果文件。

限制是：`final_decision`、`candidate_applied_externally` 与 `external_side_effects` 当前由脚本固定写入，而不是从一个真实候选注册表、外部审计器或实际 rollback 目标读取。若未来改变样本使所有门通过，脚本仍会输出相同停训决定。因此本次可以判“夹具终局正确”，不能判“通用发布门和真实回滚已验证”。

## 6. 字节重复性

pre-patch 两个独立 stdout 的 SHA-256 均为：

`b5ab7baa025f43f672d8f727f8dbc534fb3fc6a522e4e3f6e1bf851d56a18fe6`

该值仅属于旧快照。本次 post-patch 两个 fresh temp stdout 的 SHA-256 均为：

`6773bc42813c67d5633926826b9ead0ba915ef5c3319eccc7b52661e7810bc88`

当前脚本与两个临时副本的 SHA-256 均为 `8d1e76b75bae48d57493168f4037727d69c48fb3dbb610c200996958073617f3`；`cmp` 和 JSON 深比较均通过，字节一致性为 PASS。输出包含 `platform.python_version()`，所以该结论适用于本轮相同 Python 3.9.6 环境；换 Python 版本时，即使语义结果相同，字节仍可能变化。跨 Runtime 回归应同时比较规范化语义字段，不能只比较整个 stdout 哈希。

## 7. 非作者练习可执行性

### X-C08-01 三轮单变量训练

**裁决：`PASS IN SYNTHETIC SCOPE`；数据层修补后的独立回归已通过。**

非作者无需作者口头说明即可通过链接找到 harness，使用 Python 标准库执行；四轮记录、所有失败、manifest、四层/场景语义、硬门、停止和回滚声明均可读取。本次又以两个 fresh temp 目录完成 post-patch 独立复跑，证明核心训练循环和门禁在当前固定夹具内可复制。

练习的真实范围完整 PASS 仍未达到：没有每轮候选 hash/exact diff；没有显式 task/trial ID；留出和安全答案与 learner/reviewer 逻辑同处一个源码，只有逻辑角色分离；没有 real_world 样本、真实可回滚对象或独立人类 grader。故练习不能由合成 PASS 推导为真实训练或发布 PASS。

### X-C08-02 污染、裁判与多变量红队

**裁决：`REVIEW_REQUIRED`。**

注入 B“训练集满分诱导”已经由 R3 实际覆盖：6/6 训练没有越过留出和安全门。注入 A“同时更换模型、prompt 和工具 Schema”只有文字设计，没有组合候选、归因拒绝和拆分回跑记录。注入 C“导师读取留出并自签 PASS”也没有强制访问控制事件、拒绝日志和替代盲评者运行。

因此练习说明足以指导下一位实践者，但当前包不能让非作者直接复现三组完整注入。要通过，应新增独立的红队输入、访问矩阵、实际拒绝事件、变量 diff、各规范数据层与横切安全套件的结果和恢复证据，且不能覆盖本次基线。

## 8. C07 接口：术语已对齐，post-patch regression 已通过

C08 明确消费 C07 的 eval spec、baseline、数据层、grader、硬门和争议流程。C07 与 C08 现已统一为 training/regression/holdout/real_world 四个规范数据层，security/red-team 是横切非补偿套件；本夹具的 safety 样本映射为 holdout × adversarial。修补后的 harness 已由非作者两次独立复跑，数据层接口 regression 为 PASS。

本次评审不宣布 C07 接口已由总编辑冻结；触发以下任一变化仍必须重跑 C08：C07 task/trial Schema、数据层或场景语义、grader 校准规则、硬门优先级、污染合同、基线引用或 `PASS / FAIL / REVIEW_REQUIRED` 判定改变。当前 post-patch synthetic PASS 不能作为真实能力、合并或发布依据。

## 9. P0-05 / P0-06 / P0-07 实践判断

| P0 | 固定合成夹具 | 真实训练/平台 | 依据与限制 |
| --- | --- | --- | --- |
| P0-05 可执行、可停止、可回滚 | PASS（当前固定合成夹具） | REVIEW_REQUIRED | 修补后四轮实际运行并命中 STOP；真实候选、缓存、队列、Skill/Memory 未 apply 或 rollback。 |
| P0-06 权限、审批和隔离 | PASS（逻辑门禁子项） | REVIEW_REQUIRED | 安全失败不可抵消、候选无外写路径；无真实访问控制、审批或沙箱。 |
| P0-07 基线、证据和客观验收 | PASS_WITH_SCHEMA_LIMIT（post-patch X-C08-01 合成范围） | REVIEW_REQUIRED | 两次字节一致，四层/场景接口、各分区、横切套件和失败均保留；但无显式 task/trial ID、real_world、每轮 candidate hash/diff、完整 X-C08-02 或真实 grader。 |

三个 P0 只能在当前固定合成夹具内关闭相应子项。post-patch regression 已完成，不再保留“本次修补尚待回归”；但真实训练/平台范围均为 `REVIEW_REQUIRED`，C07 冻结或相关产物再次变化后必须重新验证。

## 10. 发现的问题

### P0

无新增 P0。现存缺口都被作者标为合成或独立评审待办，没有被写成真实能力、发布或成熟度结论。

### P1

1. **每轮候选缺少 hash 与 exact diff。** 练习和产物要求保存，但运行证据只有 revision 名和样本 manifest hash。分数可复现，候选内容供应链不可独立验证。
2. **终局和回滚字段是固定文字，而非计算/外部读回。** 它们与本轮门禁一致，但 harness 对未来输入变化不具备 fail-safe 终局推导能力。
3. **X-C08-02 未执行完整红队。** 多变量混改和导师越权读取没有可运行夹具、访问阻断和独立重评证据。
4. **没有显式 task/trial ID。** 18 个 `sample_id` 与 72 个 `revision + sample_id` 派生键均唯一，但输出没有 `task_id`、`trial_id`；不能直接满足 C07 run record 的 Schema 级唯一性与跨系统关联要求。

### P2

1. teacher、learner、reviewer 仅逻辑分离，答案键与候选函数同处一个进程，不能证明隐藏集强隔离。
2. 输出含 Python 版本，跨版本字节哈希不能直接比较。
3. X-C08-01 链接了脚本，但精确运行命令只出现在作者自检，建议在练习或 README 中明确写出。
4. “零副作用”由纯函数结构支持，不是对真实外部状态的读取证明。

我没有修改作者 harness 来修补这些问题，因为修改会改变本轮复现对象及哈希。应由作者或后续维护者另起候选版本，增加显式 task/trial ID 和逐轮 candidate hash/diff，再用本记录作回归基线。

## 11. 验证命令

核心复跑：

```bash
cp review/runs/synthetic_training_harness.py <fresh-temp-a>/
cp review/runs/synthetic_training_harness.py <fresh-temp-b>/
python3 <fresh-temp-a>/synthetic_training_harness.py > <fresh-temp-a>/result.json
python3 <fresh-temp-b>/synthetic_training_harness.py > <fresh-temp-b>/result.json
```

完成评审文件后运行：

```bash
python3 scripts/validate-formal-manuscript.py
python3 scripts/validate-book.py
git diff --check -- manuscript/volume-03/C08-training-system/review
```

## 12. 最终实践门

```yaml
practice_gate:
  chapter_id: "C08"
  postpatch_synthetic_three_round_reproduction: "PASS"
  byte_repeatability_same_runtime: "PASS"
  data_layer_interface_regression: "PASS"
  prepatch_semantic_regression: "PASS"
  task_trial_uniqueness: "PASS_WITH_SCHEMA_LIMIT"
  exercises:
    X-C08-01: "PASS_IN_SYNTHETIC_SCOPE"
    X-C08-02: "REVIEW_REQUIRED"
  c07_interface:
    status: "PROVISIONAL_POSTPATCH_REPRODUCED"
    chief_editor_frozen: false
  p0_scope:
    P0-05_synthetic: "PASS"
    P0-06_gate_logic_only: "PASS"
    P0-07_synthetic_baseline: "PASS_WITH_SCHEMA_LIMIT"
  real_runtime_training_and_red_team:
    P0-05: "REVIEW_REQUIRED"
    P0-06: "REVIEW_REQUIRED"
    P0-07: "REVIEW_REQUIRED"
  overall: "REVIEW_REQUIRED"
  current_patch_regression_required: false
  rerun_if_c07_or_fixture_changes: true
  chapter_status_after_review: "drafting"
  release_candidate_authorized: false
  self_approval: false
```

下一步应为 X-C08-01 增加显式 task/trial ID 与逐轮候选 hash/diff，为 X-C08-02 执行三类红队并保存访问拒绝、盲化重评和恢复证据；之后还需在获授权隔离 Runtime 中验证真实候选、权限和回滚。完成这些工作之前，本实践记录不得被解释为真实能力提升、平台有效性或生产发布批准。

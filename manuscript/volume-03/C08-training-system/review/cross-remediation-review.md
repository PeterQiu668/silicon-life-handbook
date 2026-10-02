---
review_id: CRR-C08-001
chapter_id: C08
review_type: independent-cross-remediation-regression
status: completed
reviewed_on: "2026-09-30"
reviewer: "non-author-cross-reviewer:platform_research"
independent_from_remediation_authors: true
source_review: cross-review.md
review_scope: C12_owner_fix_and_C22_triangle_and_status_fix_only
cross_gate: PASS
decision_qualifier: WITH_LIMITATIONS
p0_02: PASS
c22_status_p1: PASS
practice_gate: not_approved
editor_gate: not_approved
chief_editor_gate: not_approved
chapter_status_after_review: drafting
self_approval: false
release_candidate_authorized: false
---

# C08 交叉门修补回归

## 1. 裁决

**原 [cross-review.md](cross-review.md) 登记的两处 P0-02 定义漂移与一处 C22 状态 P1 均已在当前被审文件中关闭。C08 交叉门现裁决为 `PASS`，限定语为 `WITH_LIMITATIONS`。**

`WITH_LIMITATIONS` 不是第四种门禁；规范裁决仍是 `PASS`。它只提醒读者：本轮只回归已指定的三项修补，不批准 C08 实践门、编辑门、总编门或 `release_candidate`，也不把合成接口回归写成真实训练能力提升。原 `cross-review.md` 保留为修补前审校快照，本轮没有改写它。

## 2. 回归范围与方法

本轮只读审查：

1. [C15 正文](../../../volume-05/C15-skill-engineering/chapter.md)；
2. [C15 证据账本](../../../volume-05/C15-skill-engineering/evidence-ledger.yaml)；
3. [C25 preflight](../../../../docs/research/C25-thirty-day-training-camp-preflight.md)；
4. 原 [C08 交叉评审](cross-review.md) 的待关闭项。

检查既包含正向定位，也包含旧错误短语的负向搜索。没有修改以上四个被审文件。

## 3. P0-02（C12）：双闭环 owner 已恢复

| 检查位置 | 当前表述 | 回归结论 |
| --- | --- | --- |
| C12 章首接口 | “C02 的训练/生产双闭环，C08 的训练干预、轮次、双三角、停训与候选证据链” | PASS |
| C12 §12.7.1 | “C02 的训练/生产双闭环在这里落地；C08 进一步规定训练干预、轮次、双三角、停训和候选证据链” | PASS |
| E-C12-014 claim | 生产问题进入训练、候选回到生产遵循 C02 双闭环 | PASS |
| E-C12-014 limitations | C08 只细化训练干预和候选证据 | PASS |
| 旧错误短语 | 未再发现“C08 的训练/生产双闭环”“C08 的双闭环”或同义归属 | PASS |

因此定义权已经明确分开：

- C02 拥有训虾范式及训练/生产双闭环；
- C08 拥有训练干预、轮次、唯一双三角、停训与候选证据链；
- C12 只消费两章接口并把它落到 Skill/Plugin 候选生命周期，不反向改写定义 owner。

原交叉评审的第一项 P0-02 关闭。

## 4. P0-02（C22）：唯一双三角已恢复

C22 §7.1 当前直接声明：C08 冻结的唯一双三角是：

- 训练三角：目标—行为—反馈；
- 证据三角：任务—能力—证据。

紧接着明确：执行轨迹、环境终态、学员自检、训练者反馈和独立 evaluator 都是双三角的**观测或评审证据**，不是新的三角命名。全文没有再出现原错误口径“任务目标—执行轨迹—环境终态 / 学员自检—训练者反馈—独立 evaluator”。

Day 11 仍使用“学员自检—训练者反馈—独立复核”描述当日反馈任务，但它位于“当日任务”列，并以“双三角记录、分歧日志”为证据；没有被命名为第三个或平行三角，符合本轮修补要求。

原交叉评审的第二项 P0-02 关闭。

## 5. C22 状态 P1：C08 状态已准确同步

C22 强依赖矩阵当前写明：

> 正式稿 `drafting`；合成接口回归 `PASS`，总实践门仍 `REVIEW_REQUIRED`。

同一行还保留两条限制：不得把合成结果写成真实能力提升；正式训练营仍需补齐显式 task/trial ID、候选 hash 与 exact diff。这与 C08 当前证据层级一致，也没有继续使用旧的 `provisional/regression_required` 状态。

原交叉评审的该项状态 P1 关闭。

## 6. 限定与未被本轮批准的事项

本次 `PASS WITH LIMITATIONS` 只关闭上述三项，不改变以下事实：

1. C08 总实践门仍是 `REVIEW_REQUIRED`；真实 Runtime 训练、发布和回滚未因此通过。
2. C08 合成记录的显式 `task_id/trial_id`、候选 hash 与 exact diff 仍是实践层补强，不属于本次定义修补。
3. C12 是否需要在章节卡中把 C08 设为正式硬依赖，仍是总编依赖治理问题；当前补充消费没有再次转移定义 owner。
4. C22 尚未完成真实 30 天训练营，当前只是 preflight；其章节实践门保持 `REVIEW_REQUIRED`。
5. 原交叉评审中的其他 P1/P2 没有因为本次窄回归被自动关闭。

## 7. 三项回归记录

```yaml
cross_remediation_regression:
  chapter_id: C08
  c12_dual_loop_owner:
    expected_owner: C02
    c08_owned_interface:
      - training_intervention
      - round
      - dual_triangle
      - stop_training
      - candidate_evidence_chain
    result: PASS
  c22_unique_dual_triangle:
    training_triangle: [goal, behavior, feedback]
    evidence_triangle: [task, capability, evidence]
    trajectory_outcome_selfcheck_trainer_evaluator_role: observation_or_review_evidence
    result: PASS
  c22_c08_status:
    synthetic_interface_regression: PASS
    overall_practice_gate: REVIEW_REQUIRED
    result: PASS
  p0_02: PASS
  cross_gate: PASS
  decision_qualifier: WITH_LIMITATIONS
  practice_gate_approved: false
  editor_gate_approved: false
  chief_editor_gate_approved: false
  release_candidate_authorized: false
```

## 8. 被审文件完整性

本轮开始时固定的 SHA-256：

| 被审文件 | SHA-256 |
| --- | --- |
| C12 `chapter.md` | `1aeb899d69773d3c04b6ef91a3dd50adbf57082843682c9988c72aa7e59790f1` |
| C12 `evidence-ledger.yaml` | `7875ca830f256b858e3aba74d5c5b80d4278f93d3c1f51145721d9f8281f184b` |
| C22 preflight | `da8e59290a045b0a08bf484f246cbb478f42686252ad1bef8bcdba9d554743f7` |
| C08 原 `cross-review.md` | `22f20ba3d5baff945d8111257cb37e22aaafde0586bd7fb5a214545169f17628` |

最终验证需再次得到相同哈希；若任一被审文件在本轮并发变化，本结论必须重跑对应项。

## 9. 验证记录

完成本记录后已运行：

```bash
python3 scripts/validate-formal-manuscript.py
python3 scripts/validate-book.py
git diff --no-index --check /dev/null manuscript/volume-03/C08-training-system/review/cross-remediation-review.md
```

验证结果：

- frontmatter 与唯一 YAML 机器块：PASS；规范门禁为 `PASS`，限定语为 `WITH_LIMITATIONS`；
- 旧错误短语负向搜索：PASS；C12/C22 中没有旧归属、旧双三角或 `provisional/regression_required` 残留；
- `validate-formal-manuscript.py`：PASS；仅有 C13 正在准备、全书尚缺 11 个章节包两项进度 warning；
- `validate-book.py`：PASS；扫描 281 个 Markdown，检查 1,304 条本地链接；
- 新增文件 `git diff --no-index --check`：PASS；
- 四个被审文件的最终 SHA-256 与本轮开始时完全一致，确认本评审没有改动被审文件。

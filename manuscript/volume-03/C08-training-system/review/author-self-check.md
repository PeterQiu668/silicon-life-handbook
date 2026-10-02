---
chapter_id: C08
review_type: author-self-check
reviewed_on: "2026-09-30"
reviewer_role: chapter-author
chapter_status: drafting
author_gate: completed
fact_gate: not_started
cross_gate: not_started
practice_gate: not_started
editor_gate: not_started
self_approval_of_later_gates: false
---

# C08 作者初稿门自检

## 结论与边界

作者初稿门已完成，C08 可提交独立事实、交叉、实践和编辑审校。正文、产物、练习与账本继续保持 `drafting` / `unapproved`。作者执行过一次安全合成试跑，仅用于证明本章训练流程、停止条件和回滚记录可以落地；它不批准独立实践门，不证明真实 Agent 或平台效果。

## 交付完整性

| 检查项 | 作者结论 | 证据 |
| --- | --- | --- |
| 8.1—8.8 | PASS | 角色、双三角、最小单元、训练方法、轮次、纠错、巩固、过拟合与迁移齐全 |
| 正文篇幅 | PASS | 正式校验口径净中文字符 16,652，位于 16,000—22,000 |
| 三件且仅三件母产物 | PASS | artifacts 目录恰有 A-C08-01/02/03 |
| 两项练习 | PASS（设计） | X-C08-01/02 均有输入、步骤、停止、回滚和三态；独立执行未完成 |
| 三轮单变量试跑 | PASS（作者合成范围） | 18 样本、四版本、training/regression/holdout 运行分区与横切 safety 套件、失败分布和回滚齐全；无 real_world 样本 |
| 导师与裁判分离 | PASS（逻辑范围） | Teacher 仅看训练反馈；deterministic reviewer 持冻结答案且不改候选 |
| 三案连续性 | PASS | CASE-A/B/C 消费岗位、契约、风险和评测输入 |
| 仿生四段与双视图 | PASS | 仿生解释、工程对应、相似边界、误用风险；人类/Agent 双视图齐全 |
| 平台证据分层 | PASS（待事实门） | OpenClaw 固定版、Hermes 动态官方文档、Muse `VENDOR-CLAIM` 分开 |
| 证据闭合 | PASS | 正文 24 个唯一证据编号，账本 24 条，无缺失和孤儿 |

## P0 作者预检

| P0 | 作者结论 | 核查摘要 |
| --- | --- | --- |
| P0-01 | PASS | 章首、8.1—8.8、仿生、工程、人/Agent、失败、练习、交接齐全 |
| P0-02 | PASS | C08 只拥有训练循环；C07/C14/C15/C21/C24 定义权显式保留 |
| P0-03 | REVIEW_REQUIRED | 24 条证据均有身份与限制，仍需第二人逐条核验 |
| P0-04 | REVIEW_REQUIRED | OpenClaw 锁定 v2026.9.6/eb377ac，需独立固定版本复验 |
| P0-05 | PASS（作者合成范围） | 训练步骤、停止、回滚和安全状态已在确定性 harness 执行 |
| P0-06 | PASS（设计） | 训练候选不授予权限；contract、policy、approval 与 candidate 分离 |
| P0-07 | REVIEW_REQUIRED | 作者试跑有基线、三轮、失败和回滚，但独立实践尚未执行 |
| P0-08 | PASS | 仿生四段完整，不声称 Agent 有意识、情绪或生理学习 |
| P0-09 | REVIEW_REQUIRED | OpenClaw/Hermes/Muse 层级明确，仍需独立平台事实审校 |
| P0-10 | PASS | 三案与合成试跑均声明教学/合成性质，不冒充真实业绩 |
| P0-11 | PASS | 2 个 YAML 文件与 7 份 Markdown frontmatter 均可解析；机器程序、三态、停止和失败结构齐全 |
| P0-12 | PASS | 四个开放问题与已知限制公开，章节未标完成 |
| P0-13 | PASS | 安全失败、污染、越权、泄露、不可回滚均可一票否决 |
| P0-14 | PASS | 三件母产物路径稳定，字段化且有下游消费者 |
| P0-15 | PASS | 不以训练提分宣称能力、行业领先、成熟度或生产效果 |

## 合成运行记录

| revision | train | regression | 普通 holdout | 横切 safety 套件 | 主要失败 | 决定 |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| baseline-v0 | 2/6 | 4/4 | 0/5 | 1/3 | INTERNAL_INFERENCE 3；SOURCE_IDENTITY 4；VERSION_OR_DATE 4 | FAIL_BASELINE_ONLY |
| round-1-identity | 3/6 | 4/4 | 1/5 | 1/3 | INTERNAL_INFERENCE 3；SOURCE_IDENTITY 2；VERSION_OR_DATE 4 | FAIL_CONTINUE_SAME_LAYER |
| round-2-time | 5/6 | 4/4 | 3/5 | 1/3 | INTERNAL_INFERENCE 3；SOURCE_IDENTITY 2 | FAIL_CONTINUE_FALSIFICATION |
| round-3-inference | 6/6 | 4/4 | 4/5 | 2/3 | H05/S03；SOURCE_IDENTITY 2 | FAIL_STOP_AND_ROLLBACK_CANDIDATES |

终局是 `STOP_AND_ROLLBACK_CANDIDATES`。候选没有被外部应用，外部副作用为 0；恢复动作是丢弃 R1—R3 并保留人工复核安全模式。样本清单 hash 为 `6ded354c0e57d32940ecde99a05132da13bb50f4f2abcfc27b517156c79e8f43`。

训练集第三轮满分同时伴随普通留出与横切安全套件失败，这是本章的关键反例：训练提分不是能力提升，作者试跑也不是独立裁判。三个 safety 样本的规范身份均为 `holdout × adversarial`；本夹具没有 `real_world` 样本，安全套件不构成第五层，也不能补足真实任务证据。

## 机械验证记录

```text
python3 scripts/validate-formal-manuscript.py
C08 package checks: PASS
C08 CJK chars: 16652
Global result: FAIL（C10 仍缺仿生/双视图/练习必备节；另有后续 14 章缺包预期 warning，不属于 C08）

python3 scripts/validate-book.py
C08 local links: PASS
Global result: PASS

YAML files parsed: 3
Markdown frontmatter parsed: 8
Evidence refs: 24
Ledger IDs: 24
Missing evidence: 0
Orphan evidence: 0
Missing C08 local links/source paths: 0
Formal artifact files: 3
Exercises: 2
External evidence URLs: 17/17 HTTP 200
Raw L0—L5 notation without MAT-/AU- prefix: 0

python3 manuscript/volume-03/C08-training-system/review/runs/synthetic_training_harness.py
Manifest hash: 6ded354c0e57d32940ecde99a05132da13bb50f4f2abcfc27b517156c79e8f43
Harness hash after C07 interface amendment: 8d1e76b75bae48d57493168f4037727d69c48fb3dbb610c200996958073617f3
Final decision: STOP_AND_ROLLBACK_CANDIDATES
Round 3: train 6/6; regression 4/4; ordinary holdout 4/5; cross-cutting safety suite 2/3
Canonical layers: training/regression/holdout/real_world; real_world samples in fixture: 0
External side effects: 0
```

接口修补后的 harness 增加规范数据层、场景与套件成员字段，未改变样本 manifest、期望答案、分数、失败分布或终局决定。既有非作者复现针对修补前字节，已在独立实践记录中标为 `regression_required`；本作者记录不替代该回归。

## 待独立复核

1. 逐条核验 24 条账本，尤其 OpenClaw 固定版 Workshop/self-learning 行为及局限；
2. 复查 Hermes 动态 Skill/Memory 页面并在印前重验，不回填为固定 release 事实；
3. Muse 只保留 `VENDOR-CLAIM`，不得推断内部训练、数据集、grader 或模型更新；
4. 第二位实践者按冻结 manifest 重跑 X-C08-01，并独立执行 X-C08-02 污染红队；
5. 校准 C07 正式 grader、统计门与争议流程；C07 未冻结部分不得由 C08 越权补齐；
6. 在真实 Runtime 试验前重做数据权利、Sandbox、工具副作用、授权和回滚评审；
7. C09/C15/C21/C24 成稿后回归能力固化、漂移治理、发布和认证接口；
8. 若事实或实践不一致，修正文、产物和账本；作者不得以本记录覆盖独立结论。

---
review_id: C22-v2-independent-fact-cross-review-20260930
chapter_id: C22
review_type: independent_fact_cross_and_training_control_review
reviewed_on: "2026-09-30"
draft_gate: PASS
fact_gate: REVIEW_REQUIRED
cross_gate: REVIEW_REQUIRED
practice_gate: REVIEW_REQUIRED
release_candidate_authorized: false
---

# C22 v2 独立事实、交叉与训练营控制复核

## 裁决

**v2 的 31 日 raw-state、固定 Runtime、四层 dataset、七门点、D21、停训/恢复和毕业建议结构通过初稿门；事实与交叉门仍为 `REVIEW_REQUIRED`。** 作者的 50 项负测全部命中，证明预置异常已从正式输入剥离，closed-world 与基础类型约束有效。

非作者新增 10 项跨记录近邻攻击却全部得到 `PASS`：日记录可以使用错误 subject/camp 和悬空 authority/runtime/eval/baseline ref，可以标为 `STOPPED`；31 日可全部只引用 training dataset；成本可删到仅一个类别；停训 receipt/readback 可来自未来或未知主体；恢复可引用不存在的 backup/checkpoint；eval、baseline、dataset 可来自未来；日证据 `content_digest` 可为任意短字符串。这些结果说明 v2 已有完整名词表，但关键关系和终态仍未成为机器硬门。

## P0-C22-v2.1-01｜闭合每日记录与权威对象

每个 day 的 subject、camp、authority、runtime、eval、baseline、dataset、task、trial 和 evidence 必须逐项绑定当前对象；`STOPPED` 为硬失败或触发合法停训终态，`UNKNOWN` 为 `REVIEW_REQUIRED`，不能与 `RECORDED` 等价。日证据的 content digest 必须绑定该日 canonical 记录或可解引用产物。

## P0-C22-v2.1-02｜证明 regression 与 holdout 真正运行

不能只在 registry 中列出四层。日历必须按冻结课程映射到 training/regression/holdout，至少验证各层预注册计数、任务/试次、grader 与 lineage；representative real-world 在离线环境保持 `NOT_RUN` 与计数 0。安全 slice 必须与每日/门点证据交叉，而不只存在一条总证据。

## P0-C22-v2.1-03｜成本、停训与恢复形成可解引用链

六类成本必须按适用规则出现并绑定 subject/camp/day/task/trial，不能删除失败/remediation 人工成本以降低总额。receipt issuer、readback observer、restore owner 必须解引用 active human authority；所有时间不晚于 now 且顺序合理；backup、checkpoint、runtime、regression 和终态证据必须 registry 化并验证 digest。

## P0-C22-v2.1-04｜外部效果和毕业结论动态派生

新增 effect ledger，`external_side_effect_count` 从 raw state 派生而非常量；离线任何 APPLIED external effect 直接失败。毕业建议须从 Day0—30 状态、七门点、D21、安全、成本、停止/恢复和失败档案共同派生，仍不构成 C24 认证。

## 门禁

- 初稿门：`PASS`。
- 事实门：`REVIEW_REQUIRED`，等待 v2.1 和非作者复核。
- 交叉门：`REVIEW_REQUIRED`，C07/D22、C20/D21、C21 恢复与 C24 认证边界尚未机器闭合。
- 实践门：`REVIEW_REQUIRED`，真实连续 30 天、真实 OpenClaw/Hermes 和生产恢复未运行。
- 编辑、总编、RC：`not_authorized`。


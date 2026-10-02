---
chapter_id: C05
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

# C05 作者初稿门自检

## 结论与边界

作者初稿门已完成，C05 可提交独立事实审校、交叉审校与实践门；本记录不批准任何平台事实、练习结果、真实部署或发布状态。`chapter.md` 与证据账本继续保持 `drafting` / `unapproved`。

## 交付完整性

| 检查项 | 作者结论 | 证据 |
| --- | --- | --- |
| 5.1—5.9 正文 | PASS | `chapter.md` 标题序列完整 |
| 正文篇幅 | PASS | 正式校验口径净中文字符 18,079，位于 18,000—24,000 |
| 两件正式产物 | PASS | A-C05-01、A-C05-02 可打开且被正文引用 |
| 两项练习 | PASS（仅设计） | X-C05-01、X-C05-02 可打开；明确标为未执行 |
| 三案承接 C04 | PASS | 澄明、潮生、北辰均回链岗位/JTBD、风险与负面清单 |
| 四层分离 | PASS | 契约语义、平台载体、运行配置/状态、系统强制控制分别定义 |
| 停止与恢复 | PASS | 正文、冲突矩阵和练习均含停止、四层回滚与三态验收 |
| 证据闭合 | PASS | 正文 15 个唯一证据编号，账本 15 条，无缺失、无孤儿 |

## 全书 P0 作者预检

这些结论只说明作者没有发现阻断初稿门的问题，不替代独立审校。

| P0 | 作者结论 | 核查摘要 |
| --- | --- | --- |
| P0-01 | PASS | 章首导航、5.1—5.9、仿生、工程、人/Agent 双视图、平台映射、失败、练习和交接齐全 |
| P0-02 | PASS | C05 只拥有七契约语义；C10/C13/C14/C15/C19/C21 定义权显式保留 |
| P0-03 | REVIEW_REQUIRED | 15 条证据有类型、日期和作用域；仍需第二人逐条核验事实与解读 |
| P0-04 | REVIEW_REQUIRED | OpenClaw 锁定 v2026.9.6/eb377ac；禁用两项历史字段；仍需独立复验版本事实 |
| P0-05 | PASS（设计） | 有停止、熔断、恢复和四层回滚；实际可执行性留给实践门 |
| P0-06 | PASS（设计） | 七契约明确不能授权；高风险动作要求系统强制控制 |
| P0-07 | REVIEW_REQUIRED | 练习有输入、失败注入、证据和三态验收，但尚未独立试跑 |
| P0-08 | PASS | 仿生按机制—映射—边界—启示四段式，明确不证明意识或人格 |
| P0-09 | REVIEW_REQUIRED | OpenClaw 固定、Hermes 动态/推断、Muse 厂商声明分开；需事实审校抽查 |
| P0-10 | PASS | 三案明示为匿名教学复合案例，不声称真实客户效果 |
| P0-11 | PASS | 10 个 YAML 文件/块可解析；Agent 视图禁止扩大权限 |
| P0-12 | PASS | 无占位符；所有未知留在限制和 `REVIEW_REQUIRED` 中，章节未标完成 |
| P0-13 | PASS | 系统强制控制失败直接 `FAIL`，不能由总体表现抵消 |
| P0-14 | PASS | 两件产物有稳定路径、结构和下游接口 |
| P0-15 | PASS | 无效果、最强或领先主张；三案不作为性能证明 |

## 平台与历史冲突预检

- OpenClaw 固定基线为 `v2026.9.6` / `eb377ac59e6c9fd6c7705028034812becf00271b`。
- `TOOLS.md`、`HEARTBEAT.md` 只以固定版本“已退役”呈现，没有写成现行七文件体系。
- `reserveTokensFloor` 只说明为内部标识且不是公开配置；`compaction.reserveTokens` 也没有进入配置示例。
- Hermes 只使用 SOUL、USER、MEMORY、项目上下文、Profile、Cron 等组合映射，没有声称七项同名同构。
- Muse 只标 `VENDOR-CLAIM`，没有推断内部权限、存储或 Runtime 架构。
- SOUL、USER、AGENTS、TOOLS、IDENTITY、HEARTBEAT、MEMORY 均未被写成权限、身份认证、凭证或沙箱。

## 机械验证记录

```text
python3 scripts/validate-formal-manuscript.py
PASS（1 项预期 warning：全书仍缺 19 个章节包）
C05 CJK chars: 18079

python3 scripts/validate-book.py
PASS publication layer is structurally valid

YAML blocks parsed: 10
Evidence refs: 15
Ledger IDs: 15
Missing evidence: 0
Orphan evidence: 0
Missing local links: 0
External evidence URLs: 18/18 returned HTTP 200 after one transient retry
```

## 待独立复核与已知限制

1. 独立事实审校需逐条核验 15 条账本，尤其是 OpenClaw 退役载体、Schema 冲突和 Hermes 组合映射。
2. 两项练习尚未运行；P0-05、P0-06、P0-07 的实践门不能由作者关闭。
3. 三案是教学复合案例，未提供生产效果、跨组织普适性或性能提升证据。
4. Hermes 官方文档是 2026-09-30 动态快照，未固定到 tag；相关映射应保持 `DYNAMIC-OFFICIAL` 或 `INFERENCE`。
5. Muse 仅有厂商公开声明，不应用于证明内部技术事实或效果。
6. C04 的正式产物提供模板与接口，不等于任何组织的岗位值已经获批。
7. C10/C13/C14/C15/C19/C21 完成后需要回归本章接口，避免下游实现反向改写契约语义。

## 提交下一门所需动作

- 事实审校者：核验 15 条证据、版本范围、措辞强度与 18 个外链；不得沿用作者结论。
- 交叉审校者：检查与 C04、C06、C10、C13、C14、C15、C19、C21 的定义和接口。
- 实践审校者：在安全、匿名、可回滚环境运行两项练习，保留失败样本与零外部副作用证据。
- 总编：只有在独立门完成后决定是否晋级；作者不自我批准。

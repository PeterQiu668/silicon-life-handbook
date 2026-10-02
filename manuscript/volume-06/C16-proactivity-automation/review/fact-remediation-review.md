---
review_id: C13-independent-fact-remediation-review-20260930
chapter_id: C13
review_type: independent-fact-remediation-review
reviewed_on: "2026-09-30"
reviewer_role: evidence-reviewer
chapter_status: drafting
remediation_gate: PASS
supersedes_blocker: P1-F13-01
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
self_approval_of_other_gates: false
---

# C13 窄范围事实修复复核

## 1. 独立裁决

本轮仅复核上一轮 [fact-check.md](fact-check.md) 与 [cross-review.md](cross-review.md) 登记的三个修复项，不重做作者实践、不重写原审校记录，也不批准编辑、总编或 RC。

结论为 **`PASS`**：

1. E-C13-014 已把 OpenClaw 固定文档的产品术语 `permanent operating authority` 与本书更严格的治理裁决明确分层；
2. 作者自检已同步为 27 个 claims；
3. C14 与 C22 preflight 已更新为“C13 正式作者包存在、事实与交叉审校已完成修订、独立实践与 RC 尚未完成”；
4. C13 定向链接、外部固定来源、YAML/frontmatter 与限定 diff 均通过；全书 formal/book validators 当前只被并发写作中的 C15 未完成稿阻断，输出没有 C13 错误。

因此，上一轮唯一事实阻断项 `P1-F13-01 / E-C13-014` 已关闭。原 `fact-check.md` 作为历史审校快照保持不变；本文件只记录修复后的独立回归结论。章节仍为 `drafting / unapproved`，真实 Runtime、调度、投递、停止、故障域和恢复继续属于实践门。

## 2. E-C13-014 产品事实与治理裁决

### 2.1 固定产品事实

OpenClaw 固定提交 `eb377ac59e6c9fd6c7705028034812becf00271b` 的 [Standing Orders 文档](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/automation/standing-orders.md)确实使用 `permanent operating authority`。本轮直接读取固定 raw 文档，HTTP 返回 `200`，目标短语存在。

当前正文 13.6 已先准确陈述这一厂商术语，并明确说明这不是“没有授权”的产品对象，也不是自动调度器。该部分与固定来源一致。

### 2.2 本书治理裁决

正文随后切换到“进入本书治理层后”的规范语言，并将 `permanent` 限定为“不要求每次触发都重新创建”，明确排除以下错误解释：

- 不可撤销；
- 无期限；
- 无范围；
- 免复核；
- owner、scope、policy、version 变化后自动延续；
- 授权撤回后继续运行。

正文要求绑定 owner、目标、scope、观察来源、允许路由、C14 授权引用、复核周期、到期时间、停止条件、版本、成本预算和成功证据，并在变更或撤回时暂停相关路径、重新确认。该规范与 C14 的可核验授权、撤销、过期和再认证接口一致，没有把 C13 或 Standing Order 写成授权定义中心。

### 2.3 Ledger 身份

E-C13-014 现在同一句中明确分成：

- 前半句：OpenClaw 固定版产品事实；
- 后半句：本书可撤销、有限 scope、需 owner/review/expiry/stop/version 与 C14 再认证的治理规则。

`limitations` 又显式写明“前半句是 OpenClaw 版本事实，后半句是本书更严格治理”，并禁止把 `permanent` 解释为无限、不可撤销或跨版本继续。来源同时包含固定 `OC-STANDING`、术语表与 C14 preflight，语义支持闭合。

裁决：`PASS`。上一轮因“平台事实与规范裁决混写”产生的 `REVIEW_REQUIRED` 已消除。

## 3. 作者自检计数

[author-self-check.md](author-self-check.md) 当前同时满足：

- 交付物清点写明“证据账本包含 27 个 claim”；
- P0-03 写明“27 个主张均进入账本”；
- ledger 实际仍为 27 个唯一 evidence ID；
- 正文仍引用全部 27 条，没有缺失或孤儿引用。

裁决：`PASS`。上一轮 `P2-F13-01 / P2-X13-01` 已关闭。

## 4. C14 与 C22 状态同步

### C14 preflight

当前 C14 preflight 已明确：

- C13 已形成正式作者包；
- 独立事实与交叉审校已完成；
- Standing Order 厂商术语与本书治理裁决已经分层改写；
- 独立实践、编辑、总编和 RC 尚未完成；
- C14 可以消费已定位接口，但不得把它写成已冻结的生产事实；
- 开放问题和 Go/No-Go 仍把目标 Runtime、停止/撤销传播与独立实践保留为未关闭。

### C22 preflight

C22 强依赖矩阵中的 C13 行已更新为“正式作者包已完成；事实与交叉审校完成修订，独立实践门待签”，并继续要求 Day 15 前不开放主动触发、无停机/去重则 FAIL。

裁决：`PASS`。上一轮 `P1-X13-02` 已关闭；两份 preflight 均未把作者级合成记录或本次事实修复写成实践/RC 完成。

## 5. 机械验证

```text
Focused semantic assertions:
  chapter contains vendor term: PASS
  chapter separates governance rule: PASS
  ledger claim separates fixed fact and methodology: PASS
  ledger limitation identifies both identities: PASS
  author self-check says 27 claims: PASS
  C14 status says formal package + fact/cross complete + practice/RC open: PASS
  C22 status says formal package + fact/cross complete + practice open: PASS

OpenClaw standing-orders raw source:
  HTTP: 200
  contains "permanent operating authority": true

Parsing:
  C13 chapter frontmatter: PASS
  C13 evidence-ledger YAML: PASS
  C13 author-self-check frontmatter: PASS
  C14 preflight: PASS
  C22 preflight: PASS

Local links checked before review write:
  C13 chapter: 10 checked / 0 missing
  C13 author-self-check: 0 missing
  C14 preflight: 9 checked / 0 missing
  C22 preflight: 0 missing

C13 targeted package check after review write:
  Markdown/frontmatter/YAML: PASS
  local links: 14 checked / 0 missing
  claim closure: 27 unique / 0 missing / 0 orphan
  limited no-index diff check: PASS

Whole-book validators at review time:
  validate-formal-manuscript.py: FAIL only on concurrent C15 draft
  validate-book.py: FAIL only on concurrent C15 draft
  C13 errors in either validator: 0
```
全书 validator 的当前失败来自并发 C15 草稿的篇幅、缺少“工程真相”节及未收敛链接；本轮没有修改 C15，也不把这些错误隐瞒为全书通过。C13 定向包检查和本次限定 diff 均已通过，因此不改变本次窄范围事实裁决。

## 6. 保留边界

本次 `PASS` 只关闭事实措辞、claim 计数与下游状态同步三项：

- 不等于 Standing Order 在目标 OpenClaw 部署中已正确配置；
- 不证明撤销、到期、停止和重新确认在真实执行面有效；
- 不证明 Hermes 动态能力已固定到 `0.20.1`；
- 不证明 Muse 厂商安全声明的独立效果；
- 不替代 X-C13-01/02 的独立实践复跑；
- 不批准 editor/chief/RC。

## 7. 修复门决定

```yaml
fact_remediation_gate:
  chapter_id: C13
  verdict: PASS
  previous_blocker: P1-F13-01
  previous_blocker_closed: true
  evidence_id_E_C13_014: PASS
  author_claim_count_27: PASS
  c14_status_sync: PASS
  c22_status_sync: PASS
  independent_practice_performed: false
  practice_approved: false
  editor_approved: false
  chief_editor_approved: false
  release_candidate_authorized: false
  chapter_status_after_review: drafting
```

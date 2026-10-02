---
review_id: C24-v2-independent-fact-cross-review-20260930
chapter_id: C24
review_type: independent_fact_cross_and_certification_control_review
reviewed_on: "2026-09-30"
draft_gate: PASS
fact_gate: REVIEW_REQUIRED
cross_gate: REVIEW_REQUIRED
practice_gate: REVIEW_REQUIRED
release_candidate_authorized: false
---

# C24 v2 独立事实、交叉与认证控制复核

## 裁决

**v2 的 raw-state、57 个 trial、严格 schema、身份/授权/证据/MAT/组织/证书/生命周期 registry 与离线拒绝真实证书的方向正确，初稿门通过；事实与交叉门仍为 `REVIEW_REQUIRED`。** 原独立审校 28 项攻击已经全部关闭。

非作者新增七项跨记录攻击却全部得到 `PASS`：已经过期的 `LIMITED` 证书仍有效；生命周期 `kind=REVOKE` 可以与 `current=LIMITED` 并存；未来生命周期事件可进入当前结论；重大变化可引用不存在的 evidence；trial output evidence 为 `FAIL` 仍不影响认证；artifact 与 application signature 的 content digest 可为任意短字符串。这些问题会让认证记录在字段合法的同时保持语义矛盾。

## P0-C24-v2.1-01｜证书到期与生命周期状态机闭合

证书必须满足 `issued_at <= now < expires_at`，或在已到期时强制 `EXPIRED`；生命周期 kind、previous、current 必须来自允许转移表并与 certificate lifecycle 一致；occurred_at 不能晚于 now，且不能早于签发或逆序。暂停、撤销、到期后公开声明与操作授权必须同步收缩。

## P0-C24-v2.1-02｜重大变化必须有变更证据

change.evidence_ref 必须解引用 `change_review` evidence，并绑定 application、change_id、release、owner、时间、impact review 和 retest。重大变化即使字段写 `PASS`，没有证据仍应失败；未完成复审保持 `REVIEW_REQUIRED` 或暂停。

## P0-C24-v2.1-03｜trial output 与失败分布进入硬门

每个 trial output evidence 的 status、content digest、task、release 和 trial ID 必须验证；`FAIL/REVOKED` 为硬失败，`UNKNOWN` 为 `REVIEW_REQUIRED`。证书所需的层级覆盖、失败档案、阈值和 MAT 必要条件要从 trial registry 派生，不能只验证引用存在。

## P0-C24-v2.1-04｜所有内容 digest 使用统一格式并绑定内容

manifest、artifact、signature、holdout、grader、failure、cost、D21、dimension、public claim、lifecycle 和 change evidence 的 content digest 统一为 `sha256:<64hex>`；application signature 必须绑定申请主体、scope、release、task、platform、model、tools、data、budget、risk、environment、expiry 与 exclusions，不能用对象版本字段替代签名内容。

## 门禁

- 初稿门：`PASS`。
- 事实门：`REVIEW_REQUIRED`，等待 v2.1 与非作者复核。
- 交叉门：`REVIEW_REQUIRED`，C21 变化/生命周期、C22 毕业、C23 案例与 D22 trial 证据尚未完全闭合。
- 实践门：`REVIEW_REQUIRED`，真实 authority、真实平台、真实任务和外部认证机构未运行。
- 编辑、总编、RC：`not_authorized`。


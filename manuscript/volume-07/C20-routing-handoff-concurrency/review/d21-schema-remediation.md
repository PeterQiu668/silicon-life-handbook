---
review_id: C17-d21-schema-remediation-20260930
chapter_id: C17
review_type: author_side_remediation_note
reviewed_on: "2026-09-30"
status: post_fix_independent_review_required
independent_signoff: false
---

# C17 D21 与闭世界 schema 修补记录

本记录响应独立事实/交叉窄复核提出的 `P1-X17-R01` 与 `P1-X17-R02`，不是非作者签核。

## 已实施修补

- 把 D21 的三项调用方自报布尔改成 `technical_execution_ref`、`delivery_visibility_ref`、`business_environment_acceptance_ref`。
- runner 将引用解到 `completion_evidence_registry`，并与独立 `completion_evidence_authority` 的层级、来源、对象 digest 对照，再校验观察终态、权威性与状态并推导完成结论。
- 路由 `capability_evidence_refs` 必须解到 `capability_evidence_registry`，且绑定 routing 能力、任务版本、权限快照、状态和证据 digest；任意 dummy 或错配引用均 FAIL。
- 缺失、不可信、失败的证据使完成声明 `FAIL`；权威终态为 `UNKNOWN` 时保持 `REVIEW_REQUIRED`。
- 顶层、环境、合同、state、scenario 以及 route/yield/handoff/writer/effect/cancel/progress/branches/receipt/d21 均使用显式 required/optional/allowed key 和严格类型；控制面未知字段、未知枚举、缺字段和错误类型在产生 results 前非零退出。
- Handoff transport/object ACK 的 `REJECTED/PENDING` 以及未接受的 responsibility ACK 不再静默越过。

## 作者侧验证

- 固定 v3：60 trial，`12 PASS / 45 FAIL / 3 REVIEW_REQUIRED`，60/60 oracle 匹配，真实层 0，synthetic shadow 12，外部副作用 0。
- 两个 fresh temp 的 results 与 summary 分别逐字节一致。
- decision digest：`cfd77c3eab68797600f4333c80fbc9900998bb93ec09996af72dd285270e4fe1`。
- input SHA-256：`25fd931e47f4065473b5ebc80387c7806c2b876c822e236a7b292e4cb4ec68f0`。
- runner SHA-256：`f8de01f5da6d0139f514f2dd11fcf79e4a10a7633022d99ccad4833de33cfc59`。
- results SHA-256：`71b3fbb7c1576cf40a3ee4365b5ed1d87a464d3c76b6ab78d37edf760e357b5b`。
- summary SHA-256：`f7ca824f58f0826a19e7887a7319490ecc3e4d76302ac36f45f48cf16c3fe272`。
- `route.mystery_authority=true`、旧式四个 `"dummy"` 字段、删除/伪造 capability evidence、错误 D21 source/digest、未知 schema version 均不能产生 PASS；结构错误在生成结果前非零退出。

## v3.2 能力证据摘要绑定修补

本轮只关闭 `P1-C17-V31-01`，不改 D21 语义、不改 20 场景与三次重复：

- state 新增独立 `capability_evidence_authority`；每个 authority record 以 evidence ref 为键，冻结能力类型、任务版本、权限快照、状态与期望 digest。
- runner 在资格判断阶段同时解引用 observed registry 与 authority registry；两侧记录必须存在，必须均指向当前 routing 任务/权限且状态为 `VERIFIED`，并且五字段精确一致。
- `evidence_digest` 仍须符合 `sha256:<64 lowercase hex>`，但格式检查不再充当内容证明。格式合法的全零错误 digest 现在稳定得到 `FAIL / capability_evidence_authority_mismatch`。
- 增加 14 例定向回归：1 例精确绑定 `PASS`；其余 13 例保留 dummy/缺失/revoked/unknown/wrong-capability/wrong-task/wrong-permission，并覆盖错误观察 digest、错误权威 digest、缺失权威记录及 authority 版本/权限/状态错配，全部 `FAIL`，外部副作用为 0。
- 两个 fresh temp 的主 results、summary 与定向 regression results 均逐字节一致；保存结果与 fresh-temp 结果相同。

v3.2 当前证据哈希：

- input SHA-256：`30f95a0b871c81849419fab7f065f49d22fd7b86a9254b708439547addc96c03`。
- runner SHA-256：`410bdb87b885a6130cf41ce2543f01f2b86c250b03e58d42a4e869a6a6f5d70b`。
- results SHA-256：`b1baa18e43ea95cdc4f5425dee75453d79e2b0205132aaf88a579467422deb73`。
- summary SHA-256：`f7ca824f58f0826a19e7887a7319490ecc3e4d76302ac36f45f48cf16c3fe272`。
- targeted regression runner SHA-256：`783d1915446f4f2520f2a4dc20d45d930a6e000b3804d55071663001fc19f786`。
- targeted regression results SHA-256：`34d8bef6deaec8cb5c1de9d60a552323fc67b9b4e38f023ee3a0bd51d0ae84d1`。
- decision digest 保持：`cfd77c3eab68797600f4333c80fbc9900998bb93ec09996af72dd285270e4fe1`。
- 固定集保持：60 trial，`12 PASS / 45 FAIL / 3 REVIEW_REQUIRED`，60/60 oracle 匹配。

作者状态建议仍为 `post_fix_independent_review_required`。本记录只证明作者侧修补与回归已闭合，不自批交叉门；需由另一位非作者对 authority 独立性、错误 digest 负测和固定分布做窄复核。

## 未改变的限制

这是离线合成 machine-control 修补。真实 OpenClaw/Hermes/A2A Runtime、真实渠道、真实授权与副作用、跨系统 cancel、生产 read-back 和代表性真实任务仍未执行；交叉门必须由非作者复验后再裁决，实践门仍为 `REVIEW_REQUIRED`。

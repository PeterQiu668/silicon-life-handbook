---
artifact_id: A-C21-03
chapter_id: C21
title: "产物契约与信任记录"
status: drafting
approval_status: unapproved
---

# A-C21-03 产物契约与信任记录

## Artifact 信封

必填：`artifact_id/task_id/version/media_type/schema_ref/content_ref/content_digest/producer/owner/accountable_human/provenance.input_refs/trajectory_ref/tool_receipt_refs/transformation_chain/authority_evidence_ref/signature.signer_ref/algorithm/signed_fields/value/acceptance.contract_ref/evaluator_refs/state/findings/retention.classification/expires/deletion_hold/supersedes/revoked_at/reason`。

producer 不自动成为 owner；digest 只证明当前 bytes；签名只证明指定字段的来源/完整性断言；验收必须另查 schema、业务内容、权限/政策、环境效果和已知缺口。新版本用 `supersedes` 关联，不覆盖旧证据；更正与撤回写新记录。

## 七维信任证据

| 维度 | 作用域与证据 | 失效 |
|---|---|---|
| 身份保证 | 主体、issuer/key、时段 | 轮换/撤销/issuer变更 |
| 授权证据 | actor/action/object/scope/time/approver | 过期、撤销、上下文变化 |
| 能力实测 | 同任务/预算/风险、失败分布 | 模型/工具/协议变更 |
| 产物来源 | digest、签名、轨迹、receipt | 更正/撤回/缺口 |
| 运行可靠性 | 成功/失败/UNKNOWN、重复、恢复 | 窗口滚动/环境迁移 |
| 安全历史 | 越权、泄密、注入与事故 | 未关闭事故不衰减 |
| 当前上下文 | 健康、负载、变更窗、威胁 | 短时有效，不积成永久声誉 |

## 硬门、防刷分与申诉

先检查身份、授权、Card时效、数据位置、安全事故、证据操纵和内容验收；任一硬失败直接 FAIL。仅在合格候选间比较可靠性、成本与时效，不生成可掩盖维度的单一信任总分。记录 actor关联、互评环、重复任务、利益冲突、证据谱系、衰减、更正和申诉。动态信任可以收紧审查/限额/停用，不能自动授予外发、支付、删除或生产权限。

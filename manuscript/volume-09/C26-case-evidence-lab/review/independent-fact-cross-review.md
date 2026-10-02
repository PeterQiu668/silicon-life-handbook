---
review_id: C23-independent-fact-cross-review-20260930
chapter_id: C23
review_type: independent_fact_cross_and_control_review
reviewed_on: "2026-09-30"
chapter_status: drafting
draft_gate: PASS
fact_gate: REVIEW_REQUIRED
cross_gate: REVIEW_REQUIRED
practice_gate: REVIEW_REQUIRED
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C23 独立事实、交叉与案例证据控制审校

## 裁决

**初稿门通过；事实、交叉与实践门均为 `REVIEW_REQUIRED`。** 正文22,627 CJK，只含23.1—23.7；三件母产物、两项练习、五类案例身份、三案八段式档案、成功/失败/UNKNOWN、公平比较、因果边界、匿名授权版权、OpenClaw→Hermes迁移和Muse边界均已形成，旧材料也被正确降级为`RECONSTRUCTED`。

运行证据却没有达到章节正文要求。当前runner仍按mutation token从共享base构造状态，并且没有独立negative regression。15项近邻攻击中14项误判PASS，非法D21枚举只降为RR而非schema reject：未知nested字段、重复evidence/task ID、`latest`平台版本、伪input/artifact digest、非法risk、作者别名充当独立复现者、未版本化环境、版权FAIL、来源未授权、dummy脱敏映射、自填authorization/provenance和无public mapping均可绕过。`real_claims_accepted=0`与`external_effects=0`还是硬编码常量，不是从记录派生。

因此，17个预置trial的`2 PASS / 11 FAIL / 4 REVIEW_REQUIRED`只证明当前脚本的确定性，不证明案例身份、公开授权、公平迁移或复现证据可信。

## 1. 通过项

- 案例类型和证明力分层正确：真实、匿名真实、重建、合成与厂商声明没有被文本叙事抹平。
- CASE-A/B/C均保留失败、成本、人工、UNKNOWN和不可迁移部分；没有用单次成功支撑“行业最强”。
- 迁移目标是合同、状态、权限、证据和产物，不是把OpenClaw/Hermes配置机械等同。
- Muse只消费公开产品表面和厂商安全声明，不外推内部Runtime或独立安全效果。
- 正文明确时间顺序不等于因果，同任务比较需控制预算、环境、工具、权限和风险。
- 离线预置脚本会拒绝显式`VERIFIED-REAL/ANONYMIZED-REAL` mutation；但该局部规则不足以证明完整身份门。

## 2. P0阻断

### P0-C23-01｜mutation-token与共享base不能证明案例证据有效

正式scenario没有完整raw-state，只存mutation名称；runner内部同时定义“怎样造错”和“怎样判错”，形成作者oracle闭环。关闭条件：builder生成逐trial完整案例档案，runner不得读取mutation、case名称或expected裁决；攻击变异只能位于独立negative-regression。

### P0-C23-02｜案例身份、授权、来源与公开映射可自报

任意字符串`authorization/provenance/redaction_map`均可PASS，`public_mapping=None`也未被检查；独立复现者只通过字符串不等于`case-author`判断，别名可绕过。关闭条件：独立case identity/authorization/source/redaction/publication/reviewer registries，绑定subject、case、原始证据、许可范围、时窗、撤回状态、public/private digest和principal identity；离线runner无条件拒绝真实/匿名真实身份，真实身份由runner外门禁处理。

### P0-C23-03｜环境、版本、预算、证据与D21未闭合

`openclaw@latest/hermes@latest`、非digest输入、非法risk、未版本化环境、dummy artifact、版权FAIL和来源未授权都PASS；D21非法枚举只RR。关闭条件：严格nested schema/type/enum/ID/time/digest；固定release/commit和环境manifest；预算从model/tool/compute/human/time账目派生并与同任务对照；artifact、delivery、business/environment证据可解引用；非法enum在出结果前拒绝，D21 FAIL硬失败、UNKNOWN为RR。

### P0-C23-04｜计数和公平迁移不是状态派生

真实主张和外部effect计数硬编码为0；迁移仅保存baseline/candidate字符串，没有feature/permission/tool/data/eval parity、unsupported项、适配差异或结果分布的机器合同。关闭条件：计数从已验证记录派生；OpenClaw/Hermes迁移比较绑定同task/input/budget/risk/permissions/data/eval与各自固定release，平台不支持项必须RR或明确不适用，不能靠总分补偿。

## 3. P1与重审要求

- 建立至少30项独立负测，覆盖本轮15项，以及同digest错内容、错subject/version、过期/撤回授权、重复case/trial/evidence、失败删除、gold/grader泄露、作者别名、公开/私有digest错配、硬失败+UNKNOWN、跨平台预算和权限不公平。
- A-C23-01逐案登记raw state、case type、authority/source、环境、budget、trials、失败分布、artifacts、D21、公开映射、复现者、expected/actual和限制；A02/A03引用同一证据对象，不另造真相。
- 两练习分别标清离线合成与受控真实案例的权限、证据上限、停止、撤回、销毁和复现流程。
- 事实门重审逐条核对36/36 claims，任何真实、匿名真实或迁移成功主张必须有外部授权与实际运行证据；当前只能保留SYNTHETIC/RECONSTRUCTED/VENDOR-CLAIM。

## 4. 门禁结论

- 初稿门：`PASS`。
- 事实门：`REVIEW_REQUIRED`。
- 交叉门：`REVIEW_REQUIRED`，P0-C23-01—04开放。
- 实践门：`REVIEW_REQUIRED`；没有真实案例或真实跨Runtime迁移。
- 编辑门、总编门、RC：`not_reviewed / not_authorized`。


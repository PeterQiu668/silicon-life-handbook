---
review_id: C24-independent-fact-cross-review-20260930
chapter_id: C24
review_type: independent_fact_cross_and_certification_control_review
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

# C24 独立事实、交叉与持续认证控制审校

## 裁决

**初稿门通过；事实、交叉与实践门均为 `REVIEW_REQUIRED`。** 正文已形成成熟度、个体与组织认证、证据等级、证书生命周期、复审撤证、申诉、持续反馈以及 OpenClaw / Hermes / Muse 边界的完整教学体系；三件母产物和两项练习齐备，且未声称已经颁发真实外部证书。

但作者离线 harness 仍不是可依赖的认证控制。它由共享 base 加 mutation token 生成状态，runner 同时掌握“如何造错”和“如何判错”；授权、身份、证据、MAT 前置条件和证书决定均未绑定到独立 registry 或可解引用记录。独立运行确认基线可重复为 45 trials、`3 PASS / 35 FAIL / 7 REVIEW_REQUIRED`，但 28 项近邻攻击全部绕过，实际均未达到预期。因此，该结果只能说明脚本对自己预置 mutation 的确定性，不能证明持续认证机制有效。

## 1. 通过项

- 成熟度 `MAT-L0—MAT-L5` 与自主等级 `AU-L0—AU-L4`、毕业状态、具体授权和认证裁决被明确分离。
- 正文坚持“最弱必要门”和安全非补偿，组织成熟度没有被写成成员分数平均。
- 三态裁决与五态证书生命周期分开；重大变化、事故、SLO 燃尽、暂停、撤证和复审有清楚语义。
- D22 四层与横切安全、D21 三层完成、证据冲突、留出污染和评审独立性都在正文中出现。
- OpenClaw 固定版本、Hermes 独立举证、Muse `VENDOR-CLAIM` 边界正确；仿生隐喻没有制造自然晋级权或职业人格。
- 离线环境声明 `network=false`、`production_write=false`、`may_issue_real_certificate=false`，没有真实凭据或外部写入。

## 2. P0 阻断

### P0-C24-01｜mutation-token 不能作为认证事实

正式 scenario 只提交 mutation 名称，raw state 由 runner 内部产生。更严重的是，提交者只要把新名称加入 `allowed_mutations`，未知 mutation 就会被静默忽略并得到 `PASS`。关闭条件：builder 生成每个 trial 的完整 raw state；runner 不读取 mutation、scenario 名或 expected verdict；所有攻击位于独立 negative-regression，且无法改变正式 runner 的判定逻辑。

### P0-C24-02｜授权、主体和评审身份可自报

未知授权主体、过期授权、未绑定 digest、授权对象错配、作者别名充当 reviewer、作者充当 domain expert、未知申诉 reviewer 均得到 `PASS`。关闭条件：建立 principal、authority、role、scope、object、action、expiry、revocation、approved digest、conflict 与 reviewer-independence registries；所有引用必须存在、未撤回且与本次申请 digest 一致。作者、作者别名、控制者和申请主体不得批准自身认证。

### P0-C24-03｜证据完整性、留出与唯一性未闭合

`sha256:x`、`sha256:y`、空 holdout lineage、NaN trials、重复 trial/evidence ID 均通过；`signature_valid: true` 是自报布尔值。关闭条件：严格 type/finite/enum/time/digest 格式；全局分别唯一的 application/subject/task/trial/evidence/certificate ID；manifest、artifact、signature、holdout、grader、失败记录和 cost 均通过 registry 与内容 digest 可解引用，且由 runner 重新计算计数。

### P0-C24-04｜成熟度和证书决定没有成为硬门

缺失 MAT 前置等级、安全维度 `FAIL`、组织无 roster、证书 decision=`FAIL`、namespace decision=`FAIL`、无固定 release、非法 risk 和 change kind、签发时间非法或晚于到期时间，仍被判为 `PASS`。关闭条件：七维与目标 MAT 的必要门建立显式映射；组织认证绑定 roster、协作、故障隔离与 control plane 证据；证书决定、生命周期、公开声明、签发/到期、变化与复审必须全部从同一申请记录派生，不能由输入自报。

### P0-C24-05｜真实证书与外部效果计数不是状态派生

结果中的 `real_certificates_issued=0` 和 `external_effects=0` 是常量。关闭条件：离线 runner 从逐 trial 环境、credential、effect、certificate ledger 派生计数，并对任何真实世界或生产声明直接 schema reject；真实认证只能由 runner 外部、具权威和独立性的程序执行，继续保持 `REVIEW_REQUIRED`。

## 3. P1 与重审要求

- 增加至少 40 项独立负测，覆盖本轮 28 项和同 digest 异内容、过期/撤回 registry、签名 subject/scope/version 错配、公开声明越权、失败删除、holdout/grader 泄露、别名主体、多证书冲突、并发复审、暂停后仍公开、撤证后授权未回收。
- A-C24-01—03 引用同一申请、证据、证书与生命周期 ledger，不得各自维护互不一致的真相副本。
- 事实门重审应逐条核对 49/49 claims；本地合成 runner 只能支持 `LOCAL-VALIDATION`，不得上升为真实组织认证或法定/行业认证。
- 实践门必须由非作者、具明确 authority 的真实评审程序运行；在此之前所有真实认证、生产有效性和组织成熟度结论继续为 `REVIEW_REQUIRED`。

## 4. 门禁结论

- 初稿门：`PASS`。
- 事实门：`REVIEW_REQUIRED`，P0-C24-01—05 开放。
- 交叉门：`REVIEW_REQUIRED`；与 C07、C14、C19—C23 的状态与证据合同尚未机器闭合。
- 实践门：`REVIEW_REQUIRED`；真实证书数 0，真实外部效果 0。
- 编辑门、总编门、RC：`not_reviewed / not_authorized`。


---
review_id: C19-independent-cross-review-20260930
chapter_id: C19
review_type: independent_cross_chapter_cross_platform_and_control_review
reviewer_role: non_author_cross_reviewer
verified_on: "2026-09-30"
chapter_status: drafting
cross_gate: REVIEW_REQUIRED
fact_gate: separate_record
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C19 跨章、跨平台与运行控制审校

## 裁决

**交叉门：`REVIEW_REQUIRED`。** 正文层的主线基本成立：仅有 19.1—19.8；恰好三件母产物、两项练习；身份/租户/会话/委托、policy/approval/grant、SecretRef/credential、sandbox 三维、egress、供应链、effect/audit/recovery 在概念上分离；AU 与 MAT 未混用；D21 的 receipt/环境终态和 D22 的四层+横切安全在文字层出现；OpenClaw/Hermes/Muse 分层正确；C14/C17/C18 只作受限输入，没有把触发、Handoff、签名或 Card 变成授权。

但 22-trial harness 只“可重复”，并不“可证明”。双 fresh-temp 复跑与保存结果字节完全一致；定向负突变却显示，`identity.verified`、grant 的 actor/action/object/expiry、SecretRef/TTL/revocation、sandbox scope/backend/network/mount、Skill/Plugin digest 与 dependency、audit digest 链、incident/recovery 关闭条件均可在异常时直接 `PASS`。同一 runner 还接受 synthetic 冒充 representative real-world、非法第五层、重复 task/trial ID、未知 mutation、未知字段和未知 effect enum，并把 real-world/effect 计数硬编码为 0。它因此不能支撑“从原始状态推导”“strict schema”“D22 边界已执行”或“完整安全硬门”的结论。

详细哈希、22 项负突变与原始裁决见 [fact-cross-reproduction-20260930.yaml](fact-cross-reproduction-20260930.yaml)。本审校没有修改作者正文、ledger、产物、练习或 runs，也不替代独立实践复现。

## 1. 结构、目录与定义权

| 检查项 | 结果 | 裁决 |
| --- | --- | --- |
| 正式目录 | 仅 19.1—19.8，各一次 | PASS |
| 母产物数量 | A-C19-01/02/03，恰好三件 | PASS |
| 练习数量 | X-C19-01/02，恰好两件 | PASS |
| 三案 | CASE-A 来源污染、CASE-B 外发越权、CASE-C 多 Agent 扩权与恢复 | PASS |
| 仿生四段 | 人类现象、工程映射、训练启示、比喻边界齐全 | PASS |
| 工程真相 | 明确模型可被操纵，硬边界在模型之外 | PASS |
| 人类/Agent 双视图 | 人类保留授权/残余责任，Agent 只可受限执行、停止升级 | PASS |
| D19 | 使用 `AU` 上限；未出现裸 L 或以 MAT 推导权限 | PASS |
| C19 主定义权 | 信任边界、身份/委托安全、凭证、sandbox 三维、纵深防御归属正确 | PASS WITH FACT REMEDIATION |
| C14 边界 | 消费 authority/approval/revocation，不重定义 AU-L0—AU-L4 | PASS WITH UPSTREAM LIMITATION |
| C17 边界 | 消费 Handoff/CAS/lease/cancel，不把路由或 ACK 当授权 | PASS WITH UPSTREAM LIMITATION |
| C18 边界 | Card/签名/Artifact 只提供来源与结构证据，不创造业务授权 | PASS WITH UPSTREAM LIMITATION |
| 下游接口 | 向 C20—C24 提供 audit、发布门、红队、恢复和认证硬门 | PASS AS CONTRACT |

## 2. 上游 C14/C17/C18 的受限消费

- **C14：** 事实/交叉已通过但带真实环境限制；v3.1 离线状态化机器控制已复现，整体 practice 仍 `REVIEW_REQUIRED`。C19 正文没有把离线授权模拟写成真实授权系统。
- **C17：** fact 为 `PASS WITH LIMITATIONS`，cross 仍有受限项，practice 未审。C19 只把 Handoff、唯一 effect owner、CAS/lease 当协调输入，并在 commit 点重新检查 C14 authority，边界正确。
- **C18：** fact/cross 仍 `REVIEW_REQUIRED`，practice 未审。C19 只把 Card、签名和 Artifact 当待验证输入，没有把签名外推为内容正确或授权。

frontmatter 的“not all independently frozen; regression required”在方向上诚实，但信息粒度不足。后续应把三章当前门状态分别登记，并在其门禁改变后跑定向回归，而不是只保留一条集合式限制。

## 3. 身份、租户、会话、委托与授权

正文要求：`authenticated principal → tenant → session → agent/runtime → delegated action`；委托只能衰减；effect 前重新检查 identity、tenant、authority、policy、grant、object version、credential 和环境姿态。这与 C14/C17/C18 的责任边界一致。

runner 却只检查两个常量：`session == session-a`、`tenant == tenant-a`，以及 delegation scope 是否为 `{read,draft}` 子集。以下异常均得到 `PASS`：

- `identity.verified=false`；
- 执行 Agent 改为 `agent-z`，grant 仍属于 `agent-a`；
- grant actor 改为其他 Agent；
- grant 已在 2020 年过期；
- grant 只允许 `delete`，实际请求 `read`；
- grant object 改为其他对象。

这证明 runner 没有执行主体—委托—grant—动作—对象—时窗绑定。正文的关键安全合同没有转化为机器约束，构成 **P0-X19-01**。

## 4. Credential、egress 与 sandbox 三维

正文和 A-C19-02 要求 SecretRef、owner、scope、audience、TTL、broker、注入点、revoke/rotate、egress 和 sandbox 姿态联动。runner 只拒绝 `value_visible_to_model=true`、一个字面量 `upstream-master`、metadata IP、空 allowlist 下的尝试和 `host_mounts` 非空。

负突变结果：空 SecretRef、TTL=0、一般性 `revoked=true`、`sandbox.scope=shared`、`backend=host`、`network_default=allow`、普通 mount `/ rw` 全部 `PASS`。这意味着凭证“引用存在”、凭证有效期、一般撤销、sandbox scope/backend/network 和普通 mount 都没有进入判定。`revoke_not_propagated` 只因添加了特殊字符串 `still-active-child` 才失败，不能证明撤销传播被建模。

同样，egress 只检查字符串里是否含 `169.254.`，没有从规范化 URL、DNS 结果、IP 类别、redirect 每跳、允许目的地和数据分类推导；在纯离线 fixture 中可以作为有限模拟，但不能被称为实际 SSRF/egress 验证。

## 5. 注入、Tool/Skill/Plugin 与供应链

正文正确地把 content、tool description/schema/result、Skill、Plugin、MCP、Memory、Card/Handoff 视为不可信供应链输入，并声明 capability discovery 不产生授权。runner 也覆盖了若干字面量攻击：恶意 description、脚本列表、`web:` source、进程内 Plugin 加 `process_memory/network`。

但 runner 没有检查任何可信 registry、允许 digest、签名、依赖图、SBOM、版本或实现绑定。把 Skill digest 改成 `sha256:untrusted` 并加入恶意 dependency 仍 PASS；把 Plugin manifest digest 改为未知值仍 PASS。未知 mutation token 被静默忽略。这是场景模式匹配，不是供应链闭环。它可以作为演示夹具，不能支撑 A-C19-03 所承诺的供应链门。

## 6. D21：effect、audit、事故与恢复

正文要求区分提案、授权、执行、receipt、环境终态和业务验收，并保留 UNKNOWN；事故链要求 stop/isolate/revoke/rotate/forensics/impact/notify/recover/regression/residual。文字层符合 D21 和安全硬门非补偿。

runner 仅检查少量 state 字面量：`DUPLICATE_CONFLICT`、`COMMITTED_SYNTHETIC`、`UNKNOWN`、`REAL_WORLD_PROVEN`、`tampered`、`dummy/placeholder`。它不验证 effect receipt/readback、审计事件内容与 digest 链、不验证 incident 与 recovery 的先后/证据，也不区分技术执行、交付可见、业务/环境验收。

定向突变证明：

- audit digest 改成任意伪值（只要不等于字面量 `tampered`）仍 PASS；
- incident 为 OPEN、recovery 已 REGRESSION_PASS，但 revoke/rotate/isolate/forensics/notify 全 false，仍 PASS；
- 未知 effect enum `MAGIC_COMMITTED` 仍 PASS。

S20 的 `AUDIT_TAMPER + EFFECT_UNKNOWN` 正确输出 FAIL，说明**已被发现**的 hard failure 会压过 RR；但大量安全硬失败从未被发现，所以只能判 `PASS WITH LIMITATIONS`，不能关闭非补偿门的实现有效性。

## 7. D22、real-world manifest、strict schema 与唯一 ID

保存输入声明 training 4、regression 4、holdout 14、representative real-world 0，security/red-team 横切；原始 run 的代码也没有网络或外部写，因此“原运行是离线合成”这一窄事实成立。

runner 没有验证这些边界：

- 把 S01 的 layer 改成 `representative_real_world`，仍 PASS，输出仍硬编码 real-world count 0；
- 把 layer 改成非法第五层 `security`，仍 PASS；
- 把环境改成 production/network=true/real_credentials=true/external_side_effects=true，仍 PASS，输出仍硬编码 external count 0；
- 复制 S01 形成两个完全相同 task_id/trial_id，仍输出两个 PASS；
- 添加未知字段、未知 mutation 或未知 effect enum，均不 fail closed。

因此 D22 四层、真实层 manifest、strict schema、唯一 ID 和输出派生均为 **P0-X19-02**。当前结果只能证明一个开放世界脚本对预置 22 条场景的确定性重放。

## 8. 三件母产物与两项练习

三件文件均存在且 ID/名称正确，但目前更接近“字段提示卡”：

- A-C19-01 没有填入一份具体威胁模型、攻击树叶子、owner、控制、证据和残余记录；还保留八/九层冲突；
- A-C19-02 只有一串字段和原则，没有任何实际 actor/action/object/grant/credential 行；
- A-C19-03 只有 case 字段清单、覆盖要求和事故链，没有把 22 trial 或 CASE-A/B/C 实际登记进去。

两项练习也只有 frontmatter 加三段说明，缺质量标准 §8.1 要求的 `prerequisites / permissions_required / inputs / steps / artifacts / evidence / stop_conditions / rollback / acceptance / transfer_variant`。X-C19-01 描述“一次性 container/VM”和 credential/egress/audit 行为，但作者实际运行的是离线 Python 状态机；二者之间没有可执行命令、fixture 绑定、环境读回或回滚记录。

这不等同于实践门失败，因为本轮不批准/复现实战门；但作为作者包的交接性，构成 **P1-X19-04** 与 **P1-X19-05**。此外 author-self-check 声称“重复 ID、synthetic 冒充真实被覆盖”和“原始字段推导”，实际分别是重复 effect id、`recovery.state=REAL_WORLD_PROVEN` 的窄场景，无法覆盖重复 trial ID 和真实 layer 冒充。该自检主张应在修复后更正，记为 **P0-X19-03**。

## 9. P0/P1/P2 清单与最小关闭合同

### P0

- **P0-X19-01｜安全状态机关键绑定 fail-open。** 新 runner 必须从 identity→tenant/session→delegation→grant(actor/action/object/scope/expiry)→policy/approval→credential(ref/owner/scope/audience/TTL/revoked)→sandbox(mode/scope/backend/mount/network)→egress→effect/receipt/audit/recovery 的原始状态推导；缺失、未知、过期、错绑一律 FAIL 或 RR/fail closed。不得靠场景名、特殊字符串或作者预裁决。
- **P0-X19-02｜D22、closed-world schema 与结果派生 fail-open。** 对输入建立严格顶层和嵌套 schema，拒绝 unknown/missing/非法 enum/未知 mutation；task_id、trial_id、scenario id 唯一；layer 只允许四层，security 是横切布尔；offline synthetic 不得写 `representative_real_world`。real-world/external-effect 计数必须从被验证记录与 manifest 派生，不能硬编码。
- **P0-X19-03｜自检与摘要超出保存证据。** 在新 runner 和负突变通过后，更正 author-self-check/summary 对“重复 ID”“synthetic 冒充真实”“从原始字段推导”的表述；分别列出实际测过的 trial-ID、layer、environment、unknown-field/mutation 反例。

### P1

- **P1-X19-04｜母产物未实例化。** 在三件既有文件内填入至少一份可消费记录：A01 完整 threat model/attack tree/owner/residual，A02 CASE-A/B/C 的主体—动作—对象—grant—credential—撤销行，A03 22 trial/红队案例—证据—止损—恢复—残余索引；不得新增第四母产物。
- **P1-X19-05｜练习卡字段与实际执行断开。** 给两练习补齐质量标准 §8.1 全字段，并明确“合成状态机路径”和“真实 sandbox/runtime 路径”的不同前置、命令、证据上限、停止、回滚和三态验收。不能把 Python 状态机描述为 container/VM、credential broker 或 egress 的实跑。
- **P1-X19-06｜上游状态需精确化。** 分别记录 C14/C17/C18 当前 fact/cross/practice 门与需要触发的回归，不用单一字符串概括全部。

### P2

- **P2-X19-01｜证据卫生。** ledger 的 `TERMS` 未被 claim 消费；绑定或删除。
- **P2-X19-02｜命名一致性。** 事实门 P1-F19-01 的八/九层冲突关闭后，同步产物、练习、自检和所有下游接口说明。

## 10. 建议回归集

最小回归不能只重跑原 22 条；至少增加并保存以下变体：未验证身份、主体/grant 不匹配、过期/错动作/错对象 grant、空 SecretRef、TTL=0、一般撤销、sandbox shared/host/network allow/宽普通 mount、Skill dependency/digest 漂移、Plugin digest 漂移、伪 audit digest、缺事故处置却声称恢复、未知 effect enum、synthetic 冒充 real-world、非法第五层、production/effect 声明矛盾、重复 ID、未知字段、未知 mutation。每类必须给 expected/actual/reason、失败样本和恢复记录；双 fresh-temp 做字节/语义/hash 一致性。

## 11. 门禁结论

- 交叉门：`REVIEW_REQUIRED`。
- 事实门：见独立 [fact-check.md](fact-check.md)，当前 `REVIEW_REQUIRED`。
- 实践门：`not_reviewed`；本轮的 fresh-temp 只审作者证据，不批准真实实践。
- 编辑门、总编门、RC：`not_reviewed / not_authorized`。
- 真实 OpenClaw/Hermes/Muse、Gateway、OS sandbox、credential broker、egress、外部 API 与真实多租户均未跑，保持 `REVIEW_REQUIRED`。

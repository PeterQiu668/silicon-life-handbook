---
review_id: C20-independent-cross-review-20260930
chapter_id: C20
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

# C20 跨章、跨平台与运行控制审校

## 裁决

**交叉门：`REVIEW_REQUIRED`。** 正文合同总体完整：仅有 20.1—20.8；正式依赖、定义权与下游交接符合 8 卷 24 章拓扑；D20 五类漂移、D21 三层完成、D22 四层数据与横切安全、MAT/AU 分离均写对；OpenClaw 固定版、Hermes 固定/动态、Muse `VENDOR-CLAIM` 没有被伪对齐；三件母产物、两项练习、三案、仿生四段、人类/Agent 双视图和停止恢复均可定位。

但运行证据不能支撑作者所称的 closed-world、原始状态推导和权威终态。两个 fresh temp 的结果与保存结果字节一致，只证明预置 24 条样本可确定性重放。19 组黑盒突变证明：未知 schema/字段、非法第五层、synthetic 冒充 real-world、重复 ID、错误技术终态、不可见交付、失败业务/环境验收、伪 policy、伪 receipt/readback、伪 event digest、伪 evidence ref、未锚定 recovery 以及真实副作用计数矛盾，都可能输出 `PASS`；只有 runner 明确识别到的硬失败才会非补偿。这不是小范围真实平台限制，而是作者合成控制本身 fail-open。

详细哈希、双复现和逐项突变见 [independent-fact-cross-reproduction-20260930.yaml](runs/independent-fact-cross-reproduction-20260930.yaml)。本轮没有修改正文、ledger、母产物、练习或作者 runs；黑盒复现用于审查证据有效性，不构成独立实践门批准。

## 1. 目录、结构与定义权

| 检查项 | 结果 | 裁决 |
| --- | --- | --- |
| 正式目录 | 仅 20.1—20.8，各一次 | PASS |
| 正式依赖 | `[C06,C07,C09,C11,C13,C17,C19]` 与章节卡一致 | PASS |
| 下游交接 | C21 生命周期、C22 课程、C23 案例、C24 认证 | PASS AS CONTRACT |
| 母产物数量 | A-C20-01/02/03，恰好三件 | PASS |
| 练习数量 | X-C20-01/02，恰好两件 | PASS WITH P1 REMEDIATION |
| 贯穿案例 | CASE-A 澄明、CASE-B 潮生、CASE-C 北辰 | PASS |
| 仿生主题 | 生命体征、代谢、疼痛、康复四段并有比喻边界 | PASS |
| 工程真相 | dashboard、health、200、exit 0、scheduler completed 均不自动等于业务完成 | PASS |
| C20 定义权 | 事件链、SLI/SLO、错误预算、全成本、可靠性与事故方法 | PASS |
| 不越权 | 不重定义 C07 评测、C13 状态机、C17 路由、C19 安全、C21 发布 | PASS |

正文把“采到信号”和“获得事实”区分开，也把稳定语义与动态 OpenTelemetry 字段分开。其概念层足以供 C21—C24 消费；问题集中在作者用运行包为这些概念提供机器证据时没有实现相同约束。

## 2. 上游状态与受限消费

- **C17：** C20 保留 provisional 是正确方向，但“post-fix independent verification pending”已经过时。C17 v3.1 第三轮非作者交叉复核已完成，仍因 capability evidence digest 缺少语义权威锚点而 `REVIEW_REQUIRED`；practice 也仍 `REVIEW_REQUIRED`。C20 可以消费接口形状，不能消费其有效性结论。
- **C19：** C20 保留 limited 是正确方向，但“author package only”已经过时。C19 已有独立 fact/cross 记录，二者均为 `REVIEW_REQUIRED`，practice 未审。C20 可消费安全硬门合同，不能把 C19 runner 当真实强制控制证明。
- **回归义务：** 两个上游门状态变化时，C20 至少回归 authority/evidence binding、Handoff/receipt、effect ledger、audit digest、incident/recovery 和下游适配器；不能只更新一行状态文字。

这与事实门的 P1-F20-01 是同一项目状态缺口。它不改变章节拓扑，但会误导读者判断哪些接口已经独立冻结。

## 3. D20、D21、D22 与 MAT/AU

### D20

正文只引用能力、人格、文档、工具、目标五类漂移，并把事故样本交回 C15 形成候选；Memory/Context 没被扩成第六类，也没有让事故自动改生产、grader 或权限。**正文裁决：PASS。**

### D21

正文准确区分技术执行、交付可见、业务/环境验收，并明确 ACK、进程健康、文件存在与 dashboard success 都不能单独证明完成。**正文裁决：PASS。**

runner 却把三层状态当作未绑定输入：`technical=ERROR`、`delivery=NOT_DELIVERED`、`target_visible=false`、`artifact_valid=false`、`business_rule=FAIL`、`environment=BROKEN` 的组合仍可 `PASS`；`DELIVERED` 可以与 `target_visible=false` 并存；伪造 receipt 也不会触发降级。**运行裁决：FAIL。**

### D22

正文严格使用 training、regression、holdout、representative real-world 四层，security/red-team 为横切非补偿切片。**正文裁决：PASS。**

runner 接受非法第五层 `security`，也接受离线合成样本被改成 `representative_real_world`；结果一边报告该层 count=1，一边把 real-world evidence count 硬编码为 0。**运行裁决：FAIL。**

### MAT/AU

本章未使用裸 `Lx`，未用 MAT 推导权限，也未重定义 C14 AU-L0—AU-L4 或 C24 MAT-L0—MAT-L5。错误预算耗尽只触发收紧或重新审批，不自行扩权。**裁决：PASS。**

## 4. Closed-world 与输入完整性

runner 不验证 source root schema、`schema_version`、scenario 精确键集、嵌套状态 schema 或数据层枚举。未知 root/scenario 字段被静默忽略；未知 base-state 字段虽然被记为 `REVIEW_REQUIRED`，仍继续产出结果。这不符合“非法或未知输入在裁决前拒绝”的 closed-world 语义。

更严重的是：复制 S01 后，两个完全相同的 scenario/task/trial ID 均被接受；两次 fresh-temp 基线运行也复用相同 ID，且没有 `run_id` 或 seed 形成跨运行身份。当前 digest 可以证明同一输入生成同一结果，却不能把 trial 唯一绑定到某次运行，也不能防止重复样本污染计数。

unknown mutation token 会非零退出，是唯一得到正确 closed-world 处理的输入维度；不能以这一点外推其余 schema 已关闭。

## 5. Authority、policy、receipt、readback 与恢复

正文与 A-C20-01 要求 authority、receipt、readback、decision 和 native event 可解引用，且权威事实应来自对应 owner。runner 没有这样的 authority registry 或 readback registry：

- policy 是输入自带对象，攻击者可把 `production_write` 加入允许集，自行授权真实 effect；
- receipt/readback 只要是非空字符串便可通过，未绑定 task、logical action、target、run、object version 或 digest；
- `event_digest` 接受任意格式正确的 SHA-256，没有从 canonical event bytes 重算，也没有绑定独立 manifest；
- evidence ref 只屏蔽 `dummy/placeholder/todo` 字面量，换成任意看似正式的不存在 ref 即通过；
- recovery 的 restart、lease release、reconciliation、checkpoint 和 regression 布尔值没有证据引用也能通过。

因此，当前脚本不是从“原始事实”推导决策，而是从一组多数未验证的自报状态作局部模式匹配。E-C20-036 和作者自检中的 closed-world/原始状态推导主张均超出证据。

## 6. 外部 effect、硬失败与非补偿

把 effect 改成 `COMMITTED`，附伪 receipt/readback 并把输入外部副作用计数设为 1，runner 仍输出 `PASS`，且结果中的 `external_side_effect_count` 仍为硬编码 0。进一步让自带 policy 允许 `production_write` 也不改变结果。这证明“零外部副作用”只能描述作者保存夹具的人工意图，不能描述 runner 的强制与派生能力。

正向控制也存在：把 canary 泄露与 UNKNOWN effect 组合时，runner 输出 `FAIL`，硬失败确实压过 `REVIEW_REQUIRED`。因此“已检测到的硬失败非补偿”可判 `PASS WITH LIMITATIONS`；但检测面本身可以被上述伪状态绕过，不能关闭 P0-13。

## 7. 双复现、分布与因果边界

双 fresh-temp 复现与保存结果字节一致：24 trial、`4 PASS / 16 FAIL / 4 REVIEW_REQUIRED`，training 4、regression 4、holdout 16、representative real-world 0，security/red-team 横切 7，decision digest 为 `e6512becc0c9d266ea6a368b83d08be53acab273f10f2e697903599894959af1`。**确定性重放：PASS。**

这组结果只支持“给定当前预置输入和脚本，输出稳定”。它不支持以下外推：真实 OpenClaw/Hermes/Muse 平台可靠性、真实 OTel/Prometheus 采集、真实 Queue/Provider/Channel、真实账单、真实 receipt/readback、跨重启恢复或因果有效性。也不能用 16 个 FAIL 证明 runner 安全，因为负例能被修改为伪权威状态后通过。

## 8. 平台边界

| 平台/标准 | 章节用法 | 裁决 |
| --- | --- | --- |
| OpenClaw `v2026.9.6 / eb377ac…` | audit/logging/diagnostics/telemetry、Prometheus、logs、health/doctor | PASS AS FIXED DOCUMENTED FACT |
| Hermes `0.20.1 / f80f453…` | session DB、cron ledger、dashboard；动态 cron 另列 | PASS WITH DYNAMIC MIRROR LIMITATION |
| Muse | Activity/Artifacts/permissions 的公开说明 | PASS AS VENDOR-CLAIM ONLY |
| OpenTelemetry | 信号与字段稳定度、GenAI 内容敏感、错误语义 | PASS WITH UNPINNED-URL LIMITATION |
| Google SRE | SLI/SLO、错误预算、重试/过载工程原则 | PASS AS METHODOLOGY |

正文没有把 OpenClaw audit 当无损合规记录，没有把 Hermes DB/dashboard 当不可篡改证据，也没有把 Muse UI 外推成内部 telemetry 或效果证明。跨平台边界可保留；作者 runner 本身不是任何平台原生实现，必须继续标为离线合成控制。

## 9. 三件母产物与两项练习

A-C20-01/02 对稳定事件信封、SLI/SLO/错误预算和成本字段给出了可消费合同。A-C20-03 列出报告合同、保存分布与场景覆盖，但没有将 24 个 case 逐条实例化成可解引用的注入—信号—止损—恢复—残余记录；当前更接近模板加摘要。特别是它声称覆盖 synthetic 冒充真实、dummy 证据和未授权 effect，却没有揭示相同类别仍可被非字面量伪 ref、伪 policy 和层标签绕过。这是 **P1-X20-04**，不得用摘要替代逐案证据。

两项练习有前置、步骤、停止恢复和三态验收，教学方向正确；但 frontmatter 未按质量标准 §8.1 提供结构化的 `prerequisites / permissions_required / inputs / steps / artifacts / evidence / stop_conditions / rollback / acceptance / transfer_variant`。正文步骤也未绑定可执行命令、fixture、期望/实际结果和回滚证据。这是 **P1-X20-05**。本轮不据此宣布实践失败，但后续独立实践门不能把当前 Python 状态机等同于真实 Queue、Runtime、Channel 或跨重启任务。

## 10. P0/P1/P2 与最小关闭合同

### P0

- **P0-X20-01｜D21、authority、receipt/readback 与 recovery fail-open。** 建立独立 authority/terminal/receipt/readback/recovery registries；每条 observed record 必须精确绑定 source、tenant、task/version、action、target、run、object version、status 和 digest。技术 `ERROR/TIMEOUT`、交付 `NOT_DELIVERED`、验收 `FAIL` 不得 PASS；UNKNOWN 必须 RR；矛盾三证必须 FAIL/RR。
- **P0-X20-02｜closed-world、D22、effect count 与身份谱系 fail-open。** 对 root/scenario/base/nested objects 建立严格 schema，拒绝 unknown/missing/type/enum/schema-version 错误；只允许四层，synthetic 无 manifest 不得进入 real-world；唯一校验 scenario/task/trial，并增加 run_id/seed 防跨运行碰撞。real-world 与 external-effect count 必须从经验证记录派生，禁止硬编码。
- **P0-X20-03｜digest 与 evidence ref 只有格式、没有语义权威。** event digest 必须由 canonical bytes 重算并与独立 manifest/前序链绑定；evidence refs 必须解引用 registry 并核对主体、对象、任务、版本、类型、状态与 digest。任意格式合法但错误的 digest/ref 必须 FAIL 或 RR。
- **P0-X20-04｜作者自检把确定性重放写成控制有效。** 在上述约束和独立负突变通过前，必须把 self-check、README、A-C20-03、E-C20-036 中 closed-world、原始状态推导、零外部副作用强制与 P0-07/P0-13 的表述降级为“预置合成输入的确定性重放”。

### P1

- **P1-X20-04｜故障注入母产物未逐案实例化。** 在 A-C20-03 内登记 24 个 case 的 case/trial/run ID、原始状态、权威引用、expected/actual、决策理由、停止、恢复、残余与证据链接；不得新增第四母产物。
- **P1-X20-05｜练习卡结构与实际执行未闭合。** 两练习补齐质量标准 §8.1 字段，并分别标明离线状态机路径与真实平台路径的命令、权限、证据上限、停止、回滚和验收。
- **P1-X20-06｜上游状态过时。** 按 C17/C19 当前 fact/cross/practice 状态更新 frontmatter、正文、ledger、自检与交接，并预注册上游晋级后的回归范围。

### P2

- **P2-X20-01｜source hygiene。** `TERMS`、`OPENAI-EVAL`、`OPENAI-TRACE`、`ANTHROPIC-EVAL` 未被 evidence claim 消费；绑定或删除。
- **P2-X20-02｜OTel 版本可追溯性。** 若保留 1.44.0 精确版本，引用对应 release/tag；若继续使用 current URL，则明确是 `verified_on` 当日动态规范。

## 11. 最小独立回归集

修补后不能只复跑 24 条基线。至少保存以下负例及 expected/actual/reason：错误 schema version、未知 root/scenario/base/nested 字段、非法第五层、synthetic 冒充 real-world、real-world manifest 缺失/错 digest、重复 scenario/task/trial、跨运行 ID 重用、三层全部失败、delivery 与 visibility 矛盾、业务与环境验收矛盾、错误 event digest、不可解引用 evidence、伪 authority/policy、伪 receipt/readback、无证据 recovery、COMMITTED 外部 effect 与输出 count 矛盾，以及硬失败与 UNKNOWN 组合。双 fresh-temp 必须同时验证字节、语义、hash 和 run identity；任何硬失败均不得被平均值或 RR 抵消。

## 12. 门禁结论

- 交叉门：`REVIEW_REQUIRED`。
- 事实门：见 [fact-check.md](fact-check.md)，当前 `REVIEW_REQUIRED`。
- 实践门：`not_reviewed`；本轮只做作者证据的离线黑盒审计，不批准真实实践。
- 编辑门、总编门、RC：`not_reviewed / not_authorized`。
- 只有关闭 P0-X20-01—04，并由另一位非作者完成负突变与真实边界审查后，交叉门才可重审为 `PASS WITH LIMITATIONS`；真实平台、真实账单、真实恢复仍应保持限制，不能由离线合成包消除。

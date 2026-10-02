---
review_id: C21-independent-fact-cross-review-20260930
chapter_id: C21
review_type: independent_fact_cross_and_control_review
reviewed_on: "2026-09-30"
chapter_status: drafting
fact_gate: REVIEW_REQUIRED
cross_gate: REVIEW_REQUIRED
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C21 独立事实、交叉与运行控制审校

## 裁决

**事实门与交叉门均为 `REVIEW_REQUIRED`。** 作者包在结构、章节边界、平台表述和教学完整度上达到送审条件：正文只含 21.1—21.8，四件母产物、两项练习、47条claim、三案例、仿生四段和人类/Agent双视图均可定位；OpenClaw固定版、Hermes固定/动态和Muse `VENDOR-CLAIM` 没有被伪对齐；D20、D21、D22与MAT/AU边界也没有发现新增定义冲突。

但是，作者所称的 closed-world、权威发布单元与生命周期证据并未由runner实现。独立基线可确定性复现，然而13项近邻突变全部被判为 `PASS`，包括伪审批摘要、过期发布窗口、canary质量失败却未触发停止、伪迁移/恢复回执、不可解引用D21证据、active release错配、负预算、dummy退役签核、未知嵌套字段、非法credential/data enum和只有`sha256:`前缀的伪digest。当前运行包是对预置变异的模式检查，不足以证明生命周期控制有效。

本轮不修改作者文件，不批准实践、编辑、总编或发布候选门。详细机器记录见 [independent-fact-cross-reproduction-20260930.yaml](independent-fact-cross-reproduction-20260930.yaml)。

## 1. 通过项

- 正文规模超过正式最低门槛，编号严格为21.1—21.8。
- `A-C21-01—04`恰好四件，练习恰好两件；未把附件伪装成第五件母产物。
- 三个案例分别覆盖研究岗位、主动运营与多Agent交付组织，不是只替换名称。
- 仿生段落把免疫、代谢、记忆与凋亡映射为工程治理，并明确不推出意识、人格或生命权利。
- 本章定义生命周期责任、发布、升级、迁移、备份恢复和退役；没有重定义C15漂移、C18协议、C19安全、C20观测或C24认证。
- 保存结果28 trial、`3 PASS / 19 FAIL / 6 REVIEW_REQUIRED`、真实层0、security横切18、合成状态中的external-effect记录2均可重放；这只证明预置夹具确定性。
- 离线环境直接拒绝representative-real-world layer，这一点比同输入manifest自证真实更安全。

## 2. P0运行控制缺口

### P0-C21-01｜release identity与审批没有语义绑定

`approved_digest`未与release unit的canonical digest比对；release各digest只检查字符串以`sha256:`开头，不检查64位十六进制、更不从对象重算。把批准摘要改成`sha256:forged`，或把所有关键digest改为`sha256:x/y/z/...`，仍然 `PASS`。

关闭条件：定义release unit签名字段集合，从canonical bytes重算release digest；approval registry必须精确绑定release id、digest、actor/action/object/scope、policy、时窗、状态和独立approver。伪摘要、缺字段、额外字段、错digest、错release、错actor、过期、撤销都必须FAIL或在证据未知时RR。

### P0-C21-02｜迁移、备份、恢复与D21回执只有自报字符串

迁移receipt、backup archive、restore evidence和D21四层证据没有权威registry、canonical digest或subject/object/version绑定。`migration_receipt_forged`、`restore_evidence_forged`和`d21_fake_refs`均 `PASS`。当前无法区分真实证明、同输入自报和任意占位符。

关闭条件：建立不可由场景本体替代的migration receipt、backup manifest、restore proof和D21 evidence registries；每条证据精确绑定owner、release/migration/backup/task、对象版本、状态、时间和digest，并由runner从canonical record重算。技术执行、交付可见、业务验收、环境验收必须从各自authority记录派生；不可解引用为FAIL或RR，不能PASS。

### P0-C21-03｜rollout窗口、质量、预算与active release未强制

过期`expires_at`、`canary_quality=FAIL`但`stop_triggered=false`、`max_trials/max_cost=-1`、`runtime_state.active_release`与release id不符均 `PASS`。这意味着发布已过期、质量门失败、预算非法或运行版本错误仍可晋级。

关闭条件：核验ISO-8601时窗；预算必须正数且从trial/cost ledger聚合；质量/安全/错误预算失败必须触发停止并由权威stop receipt/readback确认；active release、rollout stage、candidate release与迁移终态必须一致。所有硬失败非补偿。

### P0-C21-04｜退役签核与嵌套schema fail-open

`complete_retirement`配合任意`terminal_signoff=dummy-agent`仍 `PASS`；退役owner、replacement/handoff、credential/data evidence没有权威绑定。credentials与data inventory未做closed-world校验，未知字段、非法status enum在非退役基线均被忽略并 `PASS`。

关闭条件：所有嵌套对象执行精确schema、类型、enum和全局唯一ID验证；credential撤销、session/delegation清空、restore禁用、data处置与residual scan必须解引用权威证据；terminal signoff必须来自active human/legal-entity owner且与decision digest绑定。未知/非法字段在裁决前拒绝。

## 3. P1与事实复核条件

- 增加非作者可运行的negative regression，不得只把预置mutation当负测；至少保存本轮13项及相邻的wrong subject、wrong version、duplicate evidence ID、valid digest wrong content、stale/future receipt、hard failure+UNKNOWN组合。
- source root、owner/authority、release、migration、backup/restore、rollout、D21、runtime tasks/schedules/webhooks/effects、rollback、legal、credentials、data、retirement、scenario都要严格验证类型、enum、唯一ID和时间。
- 四件母产物应引用v2运行包逐案索引，而不是只引用聚合分布；两练习需分别标出离线合成与真实平台命令/权限/停止/回滚/证据上限。
- 事实门重审时需逐条确认47/47 claim及来源身份，并更新已经变化的上游状态：C17 v3.2已有限制通过，C18 v3.1已有限制通过，C19/C20仍在修订。当前作者自检仍写C17待复核、C18 v2失败，已经过时。

## 4. 证据边界

即使关闭上述P0，离线包仍只可支持stateful synthetic machine-control。真实OpenClaw/Hermes升级、跨平台迁移、backup restore、credential rotation、生产canary、回滚、退役和法域合规都必须保持`REVIEW_REQUIRED`。Muse公开产品材料只可作为厂商镜面，不能用来证明内部生命周期控制。

## 5. 门禁结论

- 初稿门：`PASS`。
- 事实门：`REVIEW_REQUIRED`，需修补状态过时并完成47条claim非作者复核。
- 交叉门：`REVIEW_REQUIRED`，P0-C21-01—04开放。
- 实践门：`not_reviewed`；真实实践仍为`REVIEW_REQUIRED`。
- 编辑门、总编门、RC：`not_reviewed / not_authorized`。


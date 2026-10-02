---
review_id: C18-independent-cross-review-20260930
chapter_id: C18
review_type: independent_cross_chapter_and_cross_platform_review
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

# C18 跨章、跨平台与运行控制审校

## 裁决

**交叉门：`REVIEW_REQUIRED`。** 正文层的结构与概念边界整体成立：只含 18.1—18.7；恰好三件母产物、两项练习；Message/Task/Event/Artifact 分离，protocol/execution/acceptance 三层，Card≠身份/能力/授权，签名≠内容正确，高信任≠高权限；C17 路由/Handoff、C19 身份/凭证/威胁和 C20 遥测定义权未被抢占。CASE-A/B/C、仿生四段、工程真相、人类/Agent 双视图与失败恢复齐全。

运行证据则有两项 P0 和两项 P1。18-trial 保存结果可重复，但 runner 只验证少量 Card/Artifact 签名、digest、币种、授权引用存在性、事件序列和互评环。它没有把身份/委托与授权对象绑定，没有检查授权 actor/action/object/scope/time/approver；没有 schema/provenance/receipt/readback；没有从真实停止证据推导 `STOP_CONFIRMED`；也不执行 closed-world schema 和 D22 来源门。定向突变证明这些不是“尚未覆盖”而是实际 fail-open。

详细复现、哈希与 15 类负突变见 [fact-cross-reproduction-20260930.yaml](fact-cross-reproduction-20260930.yaml)。本记录没有修改作者文件，也不替代独立实践门。

## 1. 结构、产物与定义权

| 检查项 | 结果 | 裁决 |
| --- | --- | --- |
| 正式目录 | 仅 18.1—18.7，各一次 | PASS |
| 篇幅 | formal 口径 18,365 CJK，位于 18,000—24,000 门槛 | PASS |
| 母产物 | Card 审查表、任务状态机、Artifact 契约与信任记录，恰好三件 | PASS |
| 练习 | X-C18-01、X-C18-02，恰好两件 | PASS |
| 案例 | CASE-A/B/C 均有失败、恢复和边界 | PASS |
| 仿生 | 人类现象、工程映射、训练启示、比喻边界齐全 | PASS |
| 人类/Agent 视图 | 决策责任、机器步骤、停止升级均有说明 | PASS |
| C17 边界 | Handoff/路由只引用，不重定义 | PASS |
| C19 边界 | 身份、密钥、凭证、威胁模型留给 C19 | PASS |
| C20 边界 | 只定义事件语义，不抢遥测存储与 SLI | PASS |
| C14/C16/C17 状态 | 状态滞后且遗漏 C16 当前实践结论 | REVIEW_REQUIRED |

## 2. D21 三层完成语义

正文准确区分：

1. `protocol_state`：协议端声明；
2. `execution_state`：run、worker 与副作用是否实际停止；
3. `acceptance_state`：Artifact 与业务/环境是否验收。

正文还明确说 COMPLETED、HTTP 2xx、cancel ACK、timeout、签名和 digest 都不能单独推出业务 PASS。这与 D21 一致。

但 runner 的实现与正文相反。它只在 `effects.state == NONE` 且最后 Event 为 COMPLETED/FAILED 时直接写 `execution_state=STOP_CONFIRMED`，没有 worker/descendant/lock/effect receipt 或权威 readback；`acceptance_state` 直接等于少量规则产生的 decision，没有交付可见性或业务/环境读回。基线 S01 在完全没有 receipt/readback/provenance/schema evidence 的情况下得到 `STOP_CONFIRMED + PASS`。

更严重的是：给基线追加 `COMPLETED@3 → WORKING@4`，runner 输出 protocol=WORKING、execution=UNKNOWN，却仍给 acceptance=PASS；把最后状态改成未知 `ALIEN` 也仍为 PASS。这违反“关键证据 UNKNOWN 时最高 REVIEW_REQUIRED”和终态不可倒退原则，构成 **P0-X18-02**。

## 3. 身份、委托、授权与信任

正文和 A-C18-01 要求 authority 绑定 actor/action/object/scope/time/approver，动态信任不得创造权限。runner 实际只执行：

```python
auth = authority_store.get(authority_evidence_ref)
if not auth:
    reasons.append("AUTHORITY_MISSING")
```

它不检查 auth 的主体、动作、对象、时窗、状态、批准者，也不把 Card `agent_id`、Artifact producer、Task owner 或委托链与授权绑定。三类突变全部 exit 0 且基线仍 PASS：

- Card agent 改为 `agent-evil`，授权仍属于 `agent-good`；
- authority 已于 2026-01-01 过期；
- authority actor 改成 `agent-evil` 且 actions 只含 `delete`。

这意味着“有一个同名引用”被误当成“当前主体对当前动作与对象有有效授权”，直接违反 C14 和质量标准 P0-06，构成 **P0-X18-01**。trust score 虽未直接用于授权，这是优点；但授权引用存在性仍不足以形成硬门。

## 4. Agent Card 与 Artifact 信封

### 已实现并通过的部分

- forged Card signature → FAIL；
- Artifact bytes 改变但保留旧 digest/signature → FAIL；
- 签名有效但币种错误 → FAIL；
- 缺失 authority ref → FAIL；
- 互评环 → FAIL；
- event sequence gap、timeout 后仍运行、cancel ACK + effect pending → REVIEW_REQUIRED；
- duplicate event 相同 payload 被幂等接受，duplicate id 不同 payload → FAIL。

### 未实现或 fail-open 的部分

- Card endpoint 改成 link-local metadata 地址仍 PASS；protocol/interfaces/security scheme、trust root、revocation、cache digest 与 capability probe 没有进入裁决。
- Card 的 expired/inflated-skill 场景是在签名后改字段，因此同时触发 signature invalid；没有单独测试“签名有效但已过期”或“签名有效但能力夸大”。
- Artifact task_id 改为别的 Task 仍 PASS；producer/owner/accountable human 没有与 Task/authority 对账。
- `signed_fields` 缩到只有 `artifact_id` 仍 PASS，未检查关键字段覆盖。
- 删除内容的 `finding` 仍 PASS；没有 schema registry 或 schema validation。
- baseline Artifact 根本没有正文承诺的 provenance、trajectory、tool receipts、transformation chain、retention、supersedes 与 acceptance evidence，但仍 PASS。

这些问题构成 **P1-X18-03 / Card 与 Artifact 信任信封未被机器执行**。其中 authority 与完成相关的危险部分已由 P0-X18-01/02 单独阻断。

## 5. D22 四层与 security/red-team 横切

保存输入的静态计数是 training 4、regression 4、holdout 10、representative real-world 0；security/red-team 没有被写成第五层。这个冻结文件的计数是真实可复算的。

runner 却直接把 `data_layers` 原样复制到输出，并把 `representative_real_world_evidence_count` 硬编码为 0：

- 把 training 计数改成 999，runner exit 0 并输出 999；
- 把 S01 layer 改为 `representative_real_world`，runner exit 0、trial 标真实层，却仍报告真实证据 0；
- 把 layer 改成非法 `fifth_security_layer`，runner exit 0；
- 重复 scenario id，runner exit 0 并产生重复 task/trial id；
- 未知 mutation `mystery_attack` 被静默忽略，场景转为 PASS；
- 把 environment 改成 production/network/real credentials/external side effects 全为 true，runner 仍 exit 0 并报告 external side effects 0。

因此 E-C18-032 只能在“当前保存文件静态内容”范围通过，不能证明 D22 来源控制。此项构成 **P1-X18-04 / D22、环境与 schema fail-open**。

## 6. fresh-temp 双复现

作者原 runner 与 input 分别复制到两个全新临时目录：

- 两次 exit 0；results 逐字节相同并等于保存结果；
- results SHA-256：`3f07c5f7148cffd3a89fff62173ca38ecee6f07db9b7a8fd67c84e7a2bf01566`；
- decision digest：`732f92a985090e8d5b5314343281a7df6562221c5f02e29a478665e20a3cb879`；
- 18 trial，分布 `3 PASS / 11 FAIL / 4 REVIEW_REQUIRED`；
- 保存输出的 representative real-world evidence count=0、external side effect count=0。

这只证明冻结合成夹具的确定性，不证明两项练习、真实 A2A/OpenClaw/Hermes 互操作、真实授权、真实签名根、真实 receipt/readback 或 representative real-world 表现。

## 7. P0 / P1 与最小关闭合同

### P0-X18-01：授权与身份/委托绑定 fail-open

关闭合同：

1. authority 对象至少包含并校验 actor、action、object、scope、参数、not-before/expires、status/revocation、approver 与 policy/version；
2. 将 Card subject/provider、Task owner、Artifact producer、delegation parent/child 与 authority actor 显式绑定；委托只允许 scope attenuation；
3. 过期、撤销、主体错、动作错、对象错、范围扩大、批准者不可验证均在产生 PASS 前硬失败；
4. 保存相应单变量与组合负突变，并防止任一 trust score 补偿授权失败。

### P0-X18-02：D21 完成、状态机与 STOP_CONFIRMED fail-open

关闭合同：

1. 增加并消费 protocol snapshot、worker/run/descendant 状态、cancel record、effect ledger、receipt 与 authoritative readback；
2. 增加 Artifact delivery visibility 与业务/环境 acceptance evidence；缺关键证据最高 `REVIEW_REQUIRED`；
3. 验证 TaskState 枚举、合法转移、终态不可倒退、task/state version 与 Event 关联；未知状态硬失败或 RR，绝不能 PASS；
4. `STOP_CONFIRMED` 必须由停止、子任务、锁与 effect 对账证据推导，不能由 `effect=NONE + protocol terminal` 快捷推出；
5. 保存 terminal regression、unknown state、dummy receipt、readback UNKNOWN 与 cancel ACK but running 五类回归。

### P1-X18-03：Card 与 Artifact 信任信封不完整

关闭合同：验证 Card 原始 bytes/cache digest、protocol/interfaces/security、endpoint policy、signer trust root/revocation、时效与 capability probe；验证 Artifact/task 绑定、schema_ref、digest、签名关键字段覆盖、producer/owner/accountable human、provenance、tool receipts、transformation chain、acceptance 与 retention。unsafe endpoint、task mismatch、窄 signed fields、missing schema/provenance 均须在结果生成前拒绝或 RR。

### P1-X18-04：D22、环境与 closed-world schema fail-open

关闭合同：

1. canonical layer 只允许 training/regression/holdout/representative_real_world；security/red-team 为独立横切属性；
2. layer count、security count、real-world count 与 external side effects 均由 trial/ledger 派生，不读取或硬编码结论；
3. offline synthetic 不能占真实层；真实层必须解引用 source/run/evidence manifest；若为未来映射只能是 holdout + synthetic_shadow + intended_target_layer；
4. schema_version、required/optional/allowed keys 与类型全部显式；未知 mutation、未知 enum/field、缺字段、重复 scenario/task/trial id 一律 fail closed；
5. environment 声称有网络、真实凭证或外部副作用时，离线 runner 必须拒绝而不是继续报告零。

## 8. 交叉门结构化结论

```yaml
cross_gate:
  verdict: REVIEW_REQUIRED
  structure_18_1_to_18_7: PASS
  exactly_three_artifacts: PASS
  exactly_two_exercises: PASS
  concept_and_definition_boundaries: PASS
  c14_c16_c17_current_restricted_state: REVIEW_REQUIRED
  d21_text_semantics: PASS
  d21_runner_enforcement: FAIL
  identity_delegation_authorization_binding: FAIL
  card_artifact_envelope_enforcement: REVIEW_REQUIRED
  d22_saved_fixture_labeling: PASS_IN_FROZEN_FIXTURE
  d22_runner_enforcement: FAIL
  fixed_18_trial_repeatability: PASS_IN_DECLARED_SYNTHETIC_SCOPE
  blocking_p0: [P0-X18-01, P0-X18-02]
  blocking_p1: [P1-X18-03, P1-X18-04]
  real_platform_execution: REVIEW_REQUIRED
  practice_gate_approved: false
  editor_gate_approved: false
  chief_editor_gate_approved: false
  release_candidate_authorized: false
```


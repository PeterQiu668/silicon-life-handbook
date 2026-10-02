---
review_id: C18-v2-independent-fact-cross-review-20260930
chapter_id: C18
review_type: v2_non_author_fact_cross_narrow_review
reviewer_role: non_author_independent_reviewer
verified_on: "2026-09-30"
author_files_modified: false
historical_reviews_modified: false
frozen_fixture_reproduction: PASS
claim_ledger_integrity: PASS
fact_gate: REVIEW_REQUIRED
cross_gate: FAIL
synthetic_machine_control: FAIL
practice_gate: FAIL
real_a2a_openclaw_hermes_practice: REVIEW_REQUIRED
muse_internal_implementation: NOT_CLAIMED
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C18 v2 独立事实门与跨章一致性窄复核

## 1. 裁决

本轮只新增独立 v2 复核与复现证据，没有修改 `chapter.md`、三件母产物、两项练习、`evidence-ledger.yaml`、作者运行包或历史 review。

- **事实门：`REVIEW_REQUIRED`。** 33 条 claim 均有唯一 ID、正文引用与可解析 source ref；A2A 1.0、v1.0.1 patch、OpenClaw 固定提交、Hermes fixed/dynamic 分栏和 Muse `VENDOR-CLAIM` 边界总体准确。阻断点是 E-C18-029 的上游项目状态已滞后，且 E-C18-032 只能证明冻结文件当前没有真实层，不能证明其真实层来源门防伪。
- **交叉门：`FAIL`。** v2 文本正确要求 D21 三层、签发者信任、停止回执和 D22 来源边界，当前机器控制却有四条可重复的 PASS 绕过，与 C14、C17、D21、D22 和本章自身产物合同直接矛盾。
- **实践门：`FAIL`。** 失败限定在当前离线合成机器控制，不代表真实系统发生事故；但已知安全/证据绕过足以否决本轮实践门，不能用固定 18-trial 的全 oracle 匹配抵消。
- **真实平台：`REVIEW_REQUIRED`。** 没有运行真实 A2A 对端、OpenClaw、Hermes、组织 trust root、真实签名/授权服务、真实 cancel/stop/readback 或代表性真实世界任务。即使后续离线控制全部通过，该范围仍必须保持 `REVIEW_REQUIRED`。Muse 仅核对公开厂商材料，不对内部实现给实践结论。

结构化复现、全部 34 项攻击与原始原因码见 [v2-independent-reproduction-20260930.yaml](v2-independent-reproduction-20260930.yaml)；可重复脚本见 [run-independent-reproduction.py](runs/v2-independent/run-independent-reproduction.py)。

## 2. fresh-temp 双重建与运行

两个全新临时目录均只复制当前 builder 和 runner，由 builder 重建 input，再执行 runner；临时目录在提取结果后自动清理。

| 对象 | SHA-256 | 双运行/保存件关系 |
| --- | --- | --- |
| rebuilt input | `cc21f2338703b09283c6a8089f36042c282a57d4a3f263b912cbddeb5bf5cfdc` | A=B=作者保存件 |
| results | `f6612efffffc213f7c6c94ff9cbcbf9fa59cfc598ecfa884a75e273ca48167ae` | A=B=作者保存件 |
| summary | `3045f4ca21e56081d0d3063145267f61aa44b3eeae38538f1c8fef1d1e3549fd` | A=B=作者保存件 |

两次均得到 18 trial、`3 PASS / 9 FAIL / 6 REVIEW_REQUIRED`，decision digest 为 `9f79747a78784be4e72cd5852f89c72dff41733b2de159b8a3cd84070a8a51bc`；training 4、regression 4、holdout 10、representative real-world 0；synthetic shadow 3；外部副作用 0。固定包的确定性与 E-C18-031 数字通过。

这项通过只说明“同一代码与同一冻结输入重复产生同一输出”，不说明控制规则完备，也不说明真实互操作。

## 3. 四项阻断缺陷

### P0-C18-V2-01：Artifact 签发者撤销未进入硬门

独立攻击 `AT-ART-03` 将 Artifact 改由现有 key material 中状态为 `REVOKED` 的 `issuer-colluder` 签名，并按变更后的完整 payload 重算有效签名。实际结果仍为 `PASS`，`artifact_signature_valid=true`，没有原因码。

Card 路径会核对 trust root 状态，Artifact 路径却只检查 signer 是否存在于 `synthetic_key_material` 以及签名值是否匹配，没有核对 trust root 的 ACTIVE/REVOKED、provider/producer/owner 绑定或撤销时点。于是“密码学计算正确”被错误升级为“签发者仍可信”。这违反 P0-06、P0-13，也与正文“签名不等于信任/正确性”和 C19 信任边界接口冲突。

**最小关闭合同**：Artifact signer 必须解引用独立 trust-root/key registry，验证状态、issuer/provider、有效期/撤销、用途、producer/owner 或组织绑定；REVOKED/EXPIRED/UNKNOWN 不得形成 PASS。保留 active、revoked、expired、wrong provider、unknown key、签名正确但内容错误六类单变量与组合回归。

### P0-C18-V2-02：非终态协议可形成全局 PASS

独立攻击 `AT-D21-01` 把事件链收窄为 `SUBMITTED → WORKING`，Task 快照同步为 `WORKING@2`，同时保留 stopped execution 和已接受 Artifact。实际结果为：

```yaml
protocol_state: WORKING
execution_state: STOP_CONFIRMED
acceptance_state: PASS
decision: PASS
```

runner 校验状态转移和快照一致，却没有要求本次任务在形成全局 PASS 前达到允许的协议终态，也没有把“Artifact 可局部验收”与“Task 总体完成”分开。该结果直接违反 D21：技术执行、交付可见与业务/环境验收须分层，任一关键层未闭合时最高 `REVIEW_REQUIRED`。它也会使 C17 仍在工作或等待输入的 Task 被 C18 提前接受。

**最小关闭合同**：输出分别保存 `protocol_gate`、`execution_gate`、`acceptance_gate`；任务级 PASS 必须满足本次合同允许的 protocol terminal、执行/副作用终态和验收终态。若只验收一个中间 Artifact，应输出 `artifact_acceptance=PASS` 与 `task_completion=REVIEW_REQUIRED`，不得压成单一 PASS。固定回归至少覆盖 WORKING、INPUT_REQUIRED、AUTH_REQUIRED、UNKNOWN、FAILED-with-usable-intermediate 和 CANCELED-with-artifact。

### P0-C18-V2-03：可伪造的 stop receipt 被当作 STOP_CONFIRMED

独立攻击 `AT-STOP-03` 保持其余基线不变，把 stop receipt 设为 `status=VERIFIED, receipt_id=NONE`。实际仍为 `STOP_CONFIRMED / PASS`。当前 schema 只限制 status 枚举，不要求 receipt ID 非空、可解引用、与 task/run/worker/attempt 绑定，也没有校验 receipt 的来源、对象 digest、版本或新鲜度。

这与本章、C17 和 D21 所说的“回执与权威 readback 共同闭合”不一致；一个自报字符串足以替代停止证据。缺失 receipt 和 UNKNOWN readback 已分别正确得到 `REVIEW_REQUIRED`，但伪装成 VERIFIED 的空回执会绕过这些门。

**最小关闭合同**：`VERIFIED` 只表示“引用的独立记录通过核验”，不能是输入自报。receipt ref 必须解引用受信 registry，并 exact bind task/run/attempt、worker、stop time、issuer/source、status、object digest；`NONE`、dummy、wrong task、stale、revoked issuer 和 source/digest 不匹配均不得 STOP_CONFIRMED。

### P0-C18-V2-04：D22 真实层可由输入自证

独立攻击 `AT-D22-01` 将单个合成 S01 同时改写为：

- `data_origin=representative_real_world`；
- `representative_real_world_executed=true`；
- scenario layer 为 `representative_real_world`；
- 增加一个同文件内 `verified=true` 的自报 manifest，source/run 字符串互相匹配。

整个 fixture 仍声明 `environment.mode=offline_synthetic`、network=false、real credentials=false；validator 却接受该组合，最终输出 `PASS`。这说明当前 manifest 只做内部引用一致性，没有外部权威锚、证据 digest、采集权限、环境/输入谱系或 source attestation。合成输入可以给自己签发“真实层证明”。

这违反 D22“representative real-world 不得由 synthetic shadow 替代”，也违反 P0-03、P0-07、P0-12。E-C18-032 对当前冻结输入仍为真，但不能被解释成来源防伪控制已通过。

**最小关闭合同**：二选一。若本地 harness 不负责真实性验证，任何 representative-real-world record 一律输出 `REVIEW_REQUIRED` 并交外部证据门；若负责，则必须解引用只读/独立 provenance registry，校验 source/run/evidence digest、采集授权、环境、时间、内容 hash 与 reviewer/attestor，禁止 fixture 内自签 `verified=true` 成为最终事实。

## 4. 已通过的攻击与未被平均的硬失败

34 项攻击中 30 项按预期阻断：

- Card：伪造签名、actor 与委托/授权错绑、不安全 loopback endpoint、缓存 digest 不匹配均 `FAIL`；
- authority：过期、actor/action/object 错误、撤销和不可信批准者均 `FAIL`；100 分 trust score 不能补偿缺失 authority，authority 硬失败与 readback UNKNOWN 组合仍为 `FAIL`；
- Artifact：内容在签名后被改、签名有效但币种错误、signed_fields 过窄、跨 Task、缺 provenance 均 `FAIL`；
- 状态：终态后回退到 WORKING 为 `FAIL`，未知协议枚举被 schema 拒绝，Task snapshot 不一致为 `FAIL`；
- 停止与验收：receipt 缺失、readback UNKNOWN 均为 `REVIEW_REQUIRED`，交付不可见为 `FAIL`；
- closed-world：未知 schema、顶层字段、mutation 和 effect enum 均在结果生成前拒绝；
- 唯一性：重复 scenario/task/trial 身份被拒绝；同 event ID 同 payload 幂等接受，同 ID 不同 payload 为 `FAIL`。

因此 v2 相比历史 runner 有实质提升：旧 P0 的授权 actor/action/object/time/approver 绑定、终态回退、未知 enum、event 冲突、Artifact 内容/digest和 Card endpoint 等路径已关闭。四项新阻断不能抹去这些改进，但也不能被 30 项成功平均掉。

## 5. 33 条 claim 逐项核验

状态含义：`PASS` 表示主张身份、来源与作用域闭合；`PASS / CONTROL FAIL` 表示文字主张成立但当前 harness 与之矛盾；`REVIEW_REQUIRED` 表示当前项目状态或证据真实性未闭合。

| Claim | 裁决 | 独立核验 |
| --- | --- | --- |
| E-C18-001 | PASS | A2A 规范分别定义 Message、Task、Artifact 与两类 streaming Event；术语表定义权一致。 |
| E-C18-002 | PASS | 规范明确 Messages 用于通信，不应作为 Task outputs；输出应使用 Artifacts。 |
| E-C18-003 | PASS | 规范 Task 含 id、status、artifacts、history；正文没有把它冒充本书任务卡。 |
| E-C18-004 | PASS | 去重、检空洞、向快照对账属于方法论；规范要求传输有序但也说明断连后可能漏消息，正文没有把乱序写成规范保证。 |
| E-C18-005 | PASS | 规范 Artifact 代表 Task output，含 task 内唯一 `artifactId` 与非空 `parts`。 |
| E-C18-006 | PASS / CONTROL FAIL | D21 支持三层分离；`AT-D21-01` 证明当前 runner 仍可把非终态协议压成全局 PASS。 |
| E-C18-007 | PASS | “COMPLETED/HTTP/push 不单独推出业务 PASS”是 D21 方法论，正文作用域清楚。 |
| E-C18-008 | PASS | timeout 是等待/观察结束而非远端终止，与 C17 接口一致。 |
| E-C18-009 | PASS / CONTROL FAIL | A2A CancelTask 与 C17 停止证据被正确区分；dummy receipt 仍可伪造 STOP_CONFIRMED。 |
| E-C18-010 | PASS | A2A 只说 Send Message 可能幂等并用 messageId 去重，没有跨系统 exactly-once 保证。 |
| E-C18-011 | PASS | 规范 AgentCard 含接口、能力/skills、安全方案与可选 JWS signature。 |
| E-C18-012 | PASS | Card 是 discovery metadata；身份、能力实测、授权与行为保证被正确分层。 |
| E-C18-013 | PASS | 六层审查是本书方法论，来源身份未冒充 A2A 规范字段。 |
| E-C18-014 | PASS / CONTROL FAIL | A2A 签名支持来源/完整性；Artifact revoked signer 仍被 runner 当有效，说明控制未贯彻上限。 |
| E-C18-015 | PASS / CONTROL FAIL | digest/签名不证明内容正确或有权的主张成立；内容错测试通过，但 signer trust 测试失败。 |
| E-C18-016 | PASS | producer、owner、accountable human 分离为治理方法，不冒充 A2A 原生字段。 |
| E-C18-017 | PASS | schema、完整性、内容、authority/policy、环境与缺口六面验收与 D21 一致。 |
| E-C18-018 | PASS | supersedes 与保留历史是版本治理方法，未误写为 A2A 原生字段。 |
| E-C18-019 | PASS | 七维信任明确标为本书方法论，没有冒充协议评分标准。 |
| E-C18-020 | PASS | 动态信任只收紧审查/限额、不产生 authority，与 C14 一致。 |
| E-C18-021 | PASS | 防刷分、串谋、衰减、更正、申诉为治理要求，来源身份准确。 |
| E-C18-022 | PASS / CONTROL FAIL | P0-13 支持非补偿硬门；revoked Artifact signer 可 PASS，当前控制违反该主张。 |
| E-C18-023 | PASS | 官方规范为 1.0.0；v1.0.1 release notes列为 bug fixes，作为 1.0 patch 记录准确。 |
| E-C18-024 | PASS | OpenClaw 固定提交明确不支持 streaming/SSE、push、cancel、list、extended Card、multi-tenant routing；Task 仅内存且重启丢失。 |
| E-C18-025 | PASS | OpenClaw 固定提交明确以 `-32004` 拒绝 CancelTask，因为没有 plugin-facing abort seam。 |
| E-C18-026 | PASS | Hermes fixed 文档证明自身 delegation/lifecycle；未找到目标端 A2A 1.0 实跑证据，保持 UNKNOWN 是合规边界。 |
| E-C18-027 | PASS | Muse 来源是 Meta 官方厂商材料；正文只作 `VENDOR-CLAIM`，未推断内部 A2A、签名或 trust score。 |
| E-C18-028 | PASS | v2/card 把路由/Handoff 交 C17、身份/密钥/凭证/威胁交 C19；C18 只消费接口。 |
| E-C18-029 | REVIEW_REQUIRED | 状态已滞后：C14 v3.1 局部 synthetic control 已独立 PASS 但总实践 RR；C16 已完成独立复核并发现 synthetic control FAIL；C17 v3.1 当前仍因 capability digest 语义绑定而交叉门 RR。不能继续写“C16等待独立复验/C17交叉修补待复验”。 |
| E-C18-030 | PASS | artifacts 目录恰好三件正式母产物，名称与 v2/card 一致。 |
| E-C18-031 | PASS IN FROZEN SYNTHETIC SCOPE | 本轮双 fresh-temp 逐字节复现 18 trial、3/9/6 与相同 decision digest。 |
| E-C18-032 | PASS FOR SAVED FIXTURE / CONTROL FAIL | 保存件真实层0、shadow3属实；`AT-D22-01` 证明输入可自证真实，不能外推为防冒充控制已通过。 |
| E-C18-033 | PASS | 版本、owner、验收、来源和保留明确标为本书治理信封，没有伪称 A2A 原生字段。 |

33/33 均已逐项核验：25 项 `PASS`，5 项 `PASS / CONTROL FAIL`，1 项 `PASS IN FROZEN SYNTHETIC SCOPE`，1 项 `PASS FOR SAVED FIXTURE / CONTROL FAIL`，1 项 `REVIEW_REQUIRED`。这里的“CONTROL FAIL”不否定方法主张，而是说明正文/证据账本与可执行控制尚未一致。

## 6. 平台与协议边界

### A2A

本章以 A2A protocol 1.0 为规范基线、v1.0.1 为 patch 记录的口径通过。四对象、Task states、Card、签名、stream/push/cancel 等引用均来自官方规范。需要保留两点精度：A2A 规范要求单次传输中的 events 不重排；本书对“乱序/漏失/重复”的防御是跨连接、重放和工程恢复方法，不能改写成规范允许服务端随意乱序。A2A Card 的 JWS/JCS 是正式机制；作者离线哈希只是合成控制，不是实际 JWS 互操作证明。

### OpenClaw

固定 `eb377ac59e6c9fd6c7705028034812becf00271b` 文档直接支持当前限制清单和 CancelTask 拒绝语义。正文没有把 A2A 规范具备的能力冒充 OpenClaw fixed 已实现能力。未运行目标 binary、gateway、peer token、重启恢复或真实 Task；实践保持 `REVIEW_REQUIRED`。

### Hermes

固定提交支持 isolated child session、cooperative cancel、UNKNOWN 与 stable result hash 等 Hermes 自身事实；这些不能重命名为 A2A 1.0 兼容。动态文档与 fixed 文档已分栏。未执行 Card/send/poll/stream/cancel/artifact 探针，A2A 兼容保持 UNKNOWN。

### Muse

只核对 Meta 官方发布中的 Goals/长期任务、secure VM、用户控制等厂商叙述。正文把 A2A、Card、签名、Task persistence、内部信任分标为 UNKNOWN/NOT_APPLICABLE，没有从公开体验反推内部实现，P0-09 通过。

## 7. 跨章一致性

- **C14**：C18 没有另造授权等级，authority 仍消费 actor/action/object/scope/time/approver/policy；但 Artifact signer trust 与 authority 都属于硬门，不能只修后者。
- **C16**：C18 没有重定义多 Agent 组织收益；E-C18-029 应更新为 C16 当前独立实践复核为 FAIL、总实践 RR，而非“等待复验”。
- **C17**：Handoff、路由和并发仍归 C17；C18 正确拥有 A2A对象、Task状态、Card、Artifact与运行信任。非终态协议 PASS 和 dummy stop receipt 会破坏 C17 的责任/停止接口，修复后需做联合回归。
- **C19**：C18 可以验证签名、issuer 与信任记录，但身份、密钥、凭证和完整威胁模型仍由 C19 主定义；修补 Artifact signer 路径时应引用 C19 registry/撤销合同，不在 C18 另造平行 PKI。
- **D21**：正文分层准确，runner 的 task-level aggregate gate 不完整。
- **D22**：数据层仍是 training/regression/holdout/representative real-world 四层，security/red-team 没有成为第五层；问题在真实层 provenance 可由输入自签，不在层数。

## 8. 最小返修与回归顺序

1. 先修 Artifact signer trust-root/revocation binding；这是 P0-06/P0-13 安全硬门。
2. 将 protocol、execution、acceptance 三个 gate 独立输出，再定义 task-level aggregation；非终态不得全局 PASS。
3. 把 stop receipt 改为可解引用权威证据，不接受 `VERIFIED + NONE/dummy`。
4. 把 representative-real-world 来源真实性移交独立 registry/attestor；若本 harness 无法验证，降为 `REVIEW_REQUIRED`。
5. 更新 E-C18-029 与正文“受限输入”的 C14/C16/C17 当前状态，不改动各章定义权。
6. 保留现有 18 trial 全量回归，并加入本轮四个阻断样本及近邻变体；修复后由另一名非作者评审者重新双 fresh-temp 与突变复验。

```yaml
independent_gate_decision:
  frozen_fixture_reproduction: PASS
  claims_total: 33
  claim_ids_unique_and_cited: PASS
  a2a_primary_source_boundary: PASS
  openclaw_fixed_boundary: PASS
  hermes_fixed_dynamic_boundary: PASS
  muse_vendor_claim_boundary: PASS
  upstream_project_state_freshness: REVIEW_REQUIRED
  card_control: PASS
  authority_binding_control: PASS
  artifact_digest_content_task_provenance_control: PASS
  artifact_signer_trust_revocation_control: FAIL
  protocol_terminal_aggregation_control: FAIL
  stop_receipt_authority_control: FAIL
  unknown_schema_mutation_effect_control: PASS
  id_uniqueness_and_idempotency_control: PASS
  d21_three_layer_text_contract: PASS
  d21_three_layer_machine_control: FAIL
  d22_saved_fixture_labeling: PASS
  d22_real_world_provenance_authenticity: FAIL
  hard_failure_noncompensation: FAIL
  fact_gate: REVIEW_REQUIRED
  cross_gate: FAIL
  synthetic_machine_control: FAIL
  practice_gate: FAIL
  real_a2a_openclaw_hermes_practice: REVIEW_REQUIRED
  muse_internal_implementation: NOT_CLAIMED
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

本轮运行使用纯合成数据、无真实凭证、无网络调用、无外发、无生产写、无删除；真实层计数保持 0。作者仍是作者，本记录不构成总编或 RC 签核。

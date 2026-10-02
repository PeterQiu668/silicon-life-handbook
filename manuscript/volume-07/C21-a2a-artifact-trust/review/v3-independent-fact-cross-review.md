---
review_id: C18-v3-independent-fact-cross-review-20260930
chapter_id: C18
review_type: v3_non_author_fact_cross_narrow_review
reviewer_role: non_author_independent_reviewer
verified_on: "2026-09-30"
author_files_modified: false
historical_reviews_modified: false
frozen_fixture_reproduction: PASS
claim_ledger_integrity: PASS
fact_gate: REVIEW_REQUIRED
cross_gate: FAIL
synthetic_machine_control: FAIL
practice_gate: REVIEW_REQUIRED
real_a2a_openclaw_hermes_practice: REVIEW_REQUIRED
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C18 v3 四项阻断修订非作者窄复核

## 1. 裁决

本轮只新增本审查与 [v3 独立复现记录](v3-independent-reproduction-20260930.yaml)，没有修改正文、ledger、母产物、练习、作者 builder/runner/input/output、作者自检或历史审稿。

- **事实门：`REVIEW_REQUIRED`。** 33/33 claim ID 唯一并被正文引用，19/19 source 被消费，A2A 1.0.0 固定源、OpenClaw fixed、Hermes fixed/dynamic 和 Muse `VENDOR-CLAIM` 边界保持闭合。唯一阻断是 E-C18-029 已再次滞后：C17 v3.2 已完成非作者交叉复核并为 `PASS_WITH_LIMITATIONS`，practice 仍 `REVIEW_REQUIRED`，不再是“等待独立复验”。
- **交叉门：`FAIL`。** v2 的撤销 Artifact signer、非终态协议全局 PASS 和离线输入自签真实层三项阻断已关闭；stop receipt 主体路径只部分关闭。一个由 registry 正确重算 digest、绑定正确 task/worker/source/status、但签发于 2020 年的过旧 receipt 仍得到 `STOP_CONFIRMED / task PASS`。此外，确定性业务内容校验已经发现 `CONTENT_BUSINESS_ERROR` 时，输出的 `acceptance_state` 仍标 `PASS`。前者是 P0 终态证据重放，后者破坏 D21 分层诚实性。
- **合成机器控制：`FAIL`。** 18 条冻结样本的全 oracle 匹配不能补偿上述 fail-open。
- **实践门：`REVIEW_REQUIRED`。** 本轮没有真实 A2A 对端、OpenClaw、Hermes、真实授权/签名根、真实 cancel/stop/readback 或代表性真实任务；不因离线控制失败改写为已发生真实事故，也不批准任何真实实践。

如果只测试作者列出的四条精确样本，v3 看似已经闭合；加入任务明确要求的 stale receipt 和 acceptance 分层近邻后，控制仍未达到 `PASS_WITH_LIMITATIONS` 条件。

## 2. fresh-temp 双重建与运行

两个全新临时目录分别只复制当前 builder 与 runner，由 builder 重建 input 后运行：

| 对象 | SHA-256 | 关系 |
| --- | --- | --- |
| input | `d61672da179f0668e302a4fa11ab4c15190f3be3a212d454bd8052bbad9410b1` | A=B=保存件 |
| results | `8465d69deab941cd62750280103ca5b5de2e4d7352a02b3eda6227baaf17820a` | A=B=保存件 |
| summary | `6d9af174de0082badeddcf55c78e7570c089844bde90abde7a84edcc4c098bf7` | A=B=保存件 |

两次均为 18 trial、`3 PASS / 9 FAIL / 6 REVIEW_REQUIRED`，decision digest `05fa738a5521fc86f0833f920cf0ae2f9c5d071e64e2c6f43d728fbe9e7d509e`。D22 分布为 training 4、regression 4、holdout 10、representative real-world 0；synthetic shadow 3；外部副作用 0；18/18 oracle 匹配。

裁决：**冻结 v3 确定性重放 `PASS`。** 其作用域仅为作者预置样本，不证明控制对近邻攻击完备。

## 3. v2 四项阻断关闭矩阵

| v2 阻断 | v3 反证 | 裁决 |
| --- | --- | --- |
| P0-C18-V2-01 撤销 Artifact signer 可 PASS | 使用有效签名分别注入 REVOKED、EXPIRED、ACTIVE 但 wrong-provider root，另注入 unknown signer，四者均 `FAIL / ARTIFACT_SIGNATURE_INVALID` | **CLOSED** |
| P0-C18-V2-02 非终态协议可全局 PASS | WORKING、INPUT_REQUIRED、AUTH_REQUIRED、SUBMITTED 均 RR；FAILED、REJECTED 均 FAIL；CANCELED 为 RR | **CLOSED** |
| P0-C18-V2-03 自报 stop receipt 可 STOP_CONFIRMED | `VERIFIED+NONE/dummy/unknown ref/wrong task/future` 均不能 STOP_CONFIRMED；但合法外形的陈旧 receipt 仍 PASS | **PARTIALLY CLOSED** |
| P0-C18-V2-04 offline fixture 自签真实层 | real data origin、executed=true、真实层 scenario、非空 manifest、完整自签组合均在结果生成前拒绝 | **CLOSED** |

v3 不是原地踏步：三项完整关闭，一项显著收敛。但 stop receipt 的“存在、格式、对象正确”仍未升级为“属于本次执行且时间新鲜”。

## 4. Artifact signer 信任根

独立构造四个有效/可解析变体：

1. 用状态 `REVOKED`、provider 正确的 root 对 Artifact 重签；
2. 用状态 `EXPIRED`、provider 正确的 root 重签；
3. 用 `ACTIVE` 但 provider 与 Artifact owner 不符的 root 重签；
4. 使用 registry 中不存在的 signer。

四者均得到 `FAIL / ARTIFACT_SIGNATURE_INVALID`。runner 不再把“签名数学上匹配某段 synthetic key material”当作签发者仍可信；还要求 trust root 存在、`ACTIVE` 且 provider organization 与 owner 一致。与 UNKNOWN execution 或非终态协议组合时，Artifact signer 硬失败仍使总裁决为 FAIL，非补偿优先级通过。

这关闭 v2 P0-C18-V2-01。限制是 synthetic hash signature 仍不是实际 JWS/JCS、PKI、密钥轮换或生产撤销服务验证，属于真实实践边界。

## 5. protocol、execution、acceptance 与 task completion

### 协议聚合

| protocol | protocol gate | task completion | 裁决 |
| --- | --- | --- | --- |
| SUBMITTED / WORKING / INPUT_REQUIRED / AUTH_REQUIRED | REVIEW_REQUIRED | REVIEW_REQUIRED | PASS |
| COMPLETED | PASS | 由其他层与硬门共同决定 | PASS |
| FAILED / REJECTED | FAIL | FAIL | PASS |
| CANCELED | REVIEW_REQUIRED | REVIEW_REQUIRED | PASS |

因此，“中间 Artifact 可验收”和“Task 已完成”已经分开；FAILED 即使有可用 Artifact，task completion 仍 FAIL；CANCELED 不被误写为完成。这关闭 v2 P0-C18-V2-02。

### acceptance_state 仍不诚实

将 Artifact 的币种改为合同禁止的 USD，按变更后的 payload 正确重算 digest 与有效签名，并同步 acceptance evidence digest。runner 正确识别 `CONTENT_BUSINESS_ERROR`，总 `task_completion=FAIL`；但 `acceptance_state` 仍输出 `PASS`，因为该字段只在 reason 恰好含 `ACCEPTANCE_EVIDENCE_INVALID` 时才失败。

同样，Artifact digest/signature、schema、provenance 或 signer trust 失败时，也可能显示 `acceptance_state=PASS`，只是总任务由其他 reason 判 FAIL。硬门总聚合没有被绕过，所以这不是新的 task-level P0；但它违反 D21 的层级可解释性，会让下游误读“业务验收已经通过”。记为 **P1-C18-V3-02**。

## 6. stop receipt 权威性与新鲜度

当前 v3 registry 对 receipt 做了实质验证：记录必须是 closed-world 对象；status=`VERIFIED`；source=`control-plane`；object digest 必须从 receipt body 重算。执行层还要求 raw ref 非 `NONE/dummy/placeholder`、registry 可解引用、task 与 worker 精确匹配、签发时间不晚于当前时间，并同时验证 worker/children/locks/effects/readback。

以下变体均正确降为 `REVIEW_REQUIRED`，execution=`UNKNOWN`：

- `VERIFIED + NONE`；
- `VERIFIED + dummy`；
- `VERIFIED + unknown receipt ref`；
- registry receipt 绑定错误 task；
- receipt 时间来自未来；
- raw status=`UNKNOWN`。

### P0-C18-V3-01：陈旧 receipt 可重放为当前 STOP_CONFIRMED

将 registry 加入一条签发于 `2020-01-01T00:00:00Z` 的记录，同时保持正确 task、worker、status、source，并按该 body 重算正确 digest。runner 只检查 `issued_at <= now`，于是得到：

```yaml
protocol_gate: PASS
execution_state: STOP_CONFIRMED
acceptance_state: PASS
task_completion: PASS
```

该 receipt 没有绑定 run/attempt/execution generation、task state version、停止请求或当前执行起点。旧任务或旧运行的真实 receipt 可以被重放到本次执行，直接制造 task PASS，故仍是 P0。

最小关闭合同：

1. 给 execution/task 增加 `run_id / attempt_id / execution_generation / task_state_version / started_at` 中足以唯一识别本次运行的字段；
2. receipt registry 精确绑定上述身份、task、worker、stop/cancel request 与对象 digest；
3. `issued_at` 必须位于本次运行/停止窗口内，而不是只要求“不来自未来”；
4. 保存 stale previous-run、wrong run/attempt/generation/version、future、wrong task/worker/source/digest、revoked issuer 回归；
5. 无法证明新鲜度时 execution 最高 RR，不能 STOP_CONFIRMED。

## 7. D22 与 offline real-world 证据门

v3 明确选择“本地 harness 不负责真实来源认证”的安全路径：`data_origin` 只能是 synthetic，`representative_real_world_executed` 必须 false，任何 scenario 不得占真实层，manifest 必须为空。以下五项均在结果生成前被拒绝：

- 只把 data origin 改成 representative real-world；
- 只把 executed 改为 true；
- 只把一个 scenario 改入真实层；
- 保持 synthetic 但塞入非空 self-attested manifest；
- 同时伪造 origin、executed、layer 与 `verified=true` manifest。

这关闭 v2 P0-C18-V2-04。未来真实层必须由外部独立证据门消费；本地 runner 不再允许输入给自己签发真实性。

## 8. 33 claims 与 E-C18-029

机械闭合结果：33 claims、33 unique ID、正文 33 个唯一引用，missing=0、orphan=0；19 个 source 全部被消费，unknown source id=0。A2A 主规范已经固定为 `/v1.0.0/specification/`；E-C18-005 已拆出 E-C18-033 治理方法；E-C18-009 已标方法论。上一轮三个事实分类/固定身份问题保持关闭。

32 条 claim 仍可按原作用域通过。**E-C18-029 为唯一 `REVIEW_REQUIRED`：**

- C14 的“离线控制、真实实践 RR”方向仍可受限消费；
- C16 当前作者第二轮近邻修补仍待对应非作者复验，真实实践 RR；
- C17 已不再是“v3.2 交叉修订待复验”。本轮之前完成的 v3.2 非作者审校已把 C17 cross 更新为 `PASS_WITH_LIMITATIONS`，practice 仍 `REVIEW_REQUIRED`。

最小事实修补：同步 chapter frontmatter、章首受限输入、E-C18-029、作者自检和交接；不得把 C17 的离线 cross 通过外推为真实 routing/cancel/practice 通过。修补后重新跑 33/33 closure 即可复核事实门。

## 9. 硬失败优先级

组合测试均通过：

- revoked Artifact signer + protocol WORKING → 总 `FAIL`，未被 `PROTOCOL_NOT_COMPLETED` 的 RR 抵消；
- revoked Artifact signer + stop receipt UNKNOWN → 总 `FAIL`，未被 `EXECUTION_TERMINAL_UNKNOWN` 抵消。

所以当前聚合顺序 `FAIL > REVIEW_REQUIRED > PASS` 对已检测硬失败成立。P0-C18-V3-01 的问题不是补偿，而是 stale hard condition 根本没有被检测；P1-C18-V3-02 的问题是层级输出错误，不是总裁决被平均。

## 10. 门禁与最小回归

```yaml
independent_gate_decision:
  frozen_v3_rebuild: PASS
  claims_total: 33
  claim_reference_closure: 33/33
  E_C18_029_current: FAIL
  artifact_signer_revoked_expired_provider_unknown: PASS
  protocol_task_aggregation: PASS
  stop_receipt_none_dummy_unknown_wrong_task_future: PASS
  stop_receipt_stale_replay: FAIL
  d22_offline_self_attested_real_world: PASS
  acceptance_layer_truthfulness: FAIL
  hard_failure_noncompensation: PASS
  fact_gate: REVIEW_REQUIRED
  cross_gate: FAIL
  synthetic_machine_control: FAIL
  practice_gate: REVIEW_REQUIRED
  real_a2a_openclaw_hermes_practice: REVIEW_REQUIRED
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

下一轮最小回归必须保留本轮 26 项；重点新增本次 run/attempt/generation/version 的正确 receipt 正向控制与上一运行 receipt 重放负例，并要求所有 Artifact schema/content/integrity/authority/acceptance evidence 失败准确反映到 `acceptance_state`。修复后由非作者重新双 fresh-temp；在此之前不能把 cross 或 synthetic machine-control 升为 `PASS_WITH_LIMITATIONS`。

真实 A2A/OpenClaw/Hermes 实践、JWS/PKI、外部 trust root、真实取消传播、真实环境 read-back 与代表性真实层始终保持 `REVIEW_REQUIRED`，即使以后离线合成控制全部关闭也不会自动晋级。

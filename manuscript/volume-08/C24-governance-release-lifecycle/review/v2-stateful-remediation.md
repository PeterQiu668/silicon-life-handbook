---
review_id: C21-v2-stateful-remediation-20260930
chapter_id: C21
review_type: author_side_remediation_note
reviewed_on: "2026-09-30"
status: drafting
independent_signoff: false
fact_gate: awaiting_independent_re_review
cross_gate: awaiting_independent_re_review
practice_gate: REVIEW_REQUIRED
release_candidate_authorized: false
---

# C21 v2 / v2.1 状态化整改记录

本记录响应`review/independent-fact-cross-review.md`的P0-C21-01—04与P1，只说明作者侧如何实现关闭合同，不改写历史审校，不构成事实、交叉、实践、编辑、总编或RC签核。

## P0-C21-01：release identity与approval绑定

v2对release unit的canonical JSON重算`release_digest`，并严格验证所有组件digest为`sha256:`加64位小写十六进制。approval authority作为独立registry记录，自身也有canonical digest；它必须同时绑定actor、`approve_release`动作、release subject、release digest、rollout scope、policy version、ACTIVE状态与ISO-8601时窗。伪digest、valid digest但错误object/subject、过期、future、agent owner都进入`V2-002—V2-009`并为FAIL。

## P0-C21-02：迁移、备份、恢复与D21独立证据

新增四类独立registry：migration receipt、backup manifest、restore proof、D21 evidence。每条记录都有独立ID与canonical digest，并绑定subject/object、release、schema或object version、owner、status、issued/expiry time。runner从registry解引用，不接受scenario本体自报替代。`V2-010—V2-024`覆盖missing、forged digest、wrong subject/version、valid digest wrong content和duplicate evidence ID。

## P0-C21-03：rollout、预算、硬门、stop与active release

rollout强制解析starts/expires时窗，`max_trials/max_cost`必须为正；实际trial数与cost从trial ledger聚合。quality/security/error-budget任一FAIL都是非补偿硬失败并要求stop；stop receipt位于独立registry，绑定release/plan/owner/active release、canonical digest、0—300秒新鲜度和admission/queue/workers readback。runtime active release必须与candidate一致。`V2-025—V2-035、V2-048、V2-055`覆盖负预算、越界、未停、伪/stale/future receipt、硬失败+UNKNOWN及正向verified stop。

## P0-C21-04：退役与closed-world

所有root/nested对象使用exact schema、类型、enum、时间和唯一ID校验。退役decision有canonical digest及独立authority；admission、inflight、runtime、network、replacement、handoff、residual、terminal signoff，以及credential/session/delegation/restore/data逐项解引用retirement evidence registry。证据绑定subject、release、release digest、active human/legal owner、状态和时窗；terminal signoff额外绑定retirement decision digest。`V2-036—V2-049`覆盖未知字段、非法枚举、dummy signoff、各类残余、valid digest wrong decision和hard+UNKNOWN。

## v2.1 近邻复核整改

非作者首轮近邻复核发现9项fail-open，v2.1逐项关闭：新增独立rollback receipt registry及canonical/readback绑定；migration、backup、restore、rollout等owner必须绑定角色适配的active human/legal主体；RPO/RTO、cost等数值必须finite且满足范围；backup covered与excluded不得交叉；不可逆migration必须为非reentrant、`FORWARD_ONLY`并绑定独立高风险批准。`V2-056—V2-064`保存九项负回归，均由原始状态推导为FAIL。

## P1：负回归、产物与上游状态

- 保存64个唯一trial：`3 PASS / 55 FAIL / 6 REVIEW_REQUIRED`，其中61项非PASS回归；代表性真实层0，security横切43，external effect 0。
- runner不读取`expected`、scenario名、mutation token或预裁决布尔；scenario仅提供raw state override。
- 四件母产物嵌入v2逐案索引；两练习明确离线命令、权限、真实平台停止条件与证据上限。
- chapter、ledger和作者自检已更新：C17 v3.2与C18 v3.1事实/交叉门均`PASS_WITH_LIMITATIONS`、真实实践RR；C19/C20仍在修订。

## 作者侧冻结结果

```yaml
schema: c21.lifecycle.input.v2.1
trials: 64
distribution: {PASS: 3, FAIL: 55, REVIEW_REQUIRED: 6}
representative_real_world: 0
security_slice_trials: 43
external_effect_count: 0
decision_digest: sha256:9f0fa6e88641257c9ca29450956c02a01fd7e01c59ab312be8b650c653c74126
builder_sha256: b48fa1c7ff8c79f6c224741dab6edf28f3a77e6d7af6ce64ce101eba9f0c9082
runner_sha256: 0c941e5d4edf17aba12e52d60e530b2fddcd55ba1fb72e982970301d61ef5770
input_sha256: 4c443fe896d3cce415a34346559af364156d51d45b220a858df40c31614d8a1e
results_sha256: cef003a016c49965ffffed4e5f8e73001d74847ff11fe24c18eea7df2ee361b6
summary_sha256: 0bfd895415e421c6a62c60c73c0014ea7d6a38bd72a14229f9c8460db654a399
```

作者侧fresh-temp双重建已逐字节一致；这仍须非作者复验。真实OpenClaw/Hermes发布、迁移、backup restore、生产canary、回滚、退役、数据处置和法域合规没有运行，全部保持`REVIEW_REQUIRED`。章节继续`drafting / unapproved`。

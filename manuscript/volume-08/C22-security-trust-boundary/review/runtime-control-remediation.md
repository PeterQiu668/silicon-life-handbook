---
review_id: C19-runtime-control-remediation-20260930
chapter_id: C19
review_type: author_side_remediation_note
reviewed_on: "2026-09-30"
status: post_fix_independent_review_required
independent_signoff: false
cross_gate: REVIEW_REQUIRED
practice_gate: REVIEW_REQUIRED
---

# C19 P0-X19-01/02/03 作者侧运行控制修补（v2.1）

本记录由本轮修订作者编写，只说明作者侧实现和回归，不修改或取代历史 [fact-check](fact-check.md)、[cross-review](cross-review.md) 与 [fact-cross reproduction](fact-cross-reproduction-20260930.yaml)，不构成任何独立门签核。

## 修补结论

### P0-X19-01：从开放脚本改为 raw-state 安全链

旧 runner 的 mutation token 和少数字面量分支已移除。v2.1 runner 只消费 22 个 trial 保存的完整 raw state，并沿以下关系推导：

- identity authority、tenant、session、principal、agent、service 与有效状态精确绑定；
- delegation 只能是当前 policy 允许动作、对象和 scope 的子集，并核时窗与状态；
- approval 与 grant 都绑定 actor/action/object/scope、policy version 和时窗，approval params digest 从 canonical action/object/scope 重算；
- SecretRef 必须存在、broker owner 必须在权威表中 active，scope/audience/TTL/issued/expires/status/模型可见性共同校验；
- sandbox 的 mode/scope/backend/status、mount source/path 与 network default 分别校验；
- egress 每跳解析 URL host，并检查 allowlist、resolved IP 分类、redirect 与数据分类；
- Tool、Skill、Plugin 分别解引用权威 registry，比对 manifest/implementation digest、dependency、execution mode 与 capability；
- effect 解引用 canonical receipt 与 authoritative read-back；audit event 按 canonical bytes 重算链并比对独立 anchor；incident 与 recovery 需完整 controls、权威 recovery evidence、target version 和 probe。

固定 22 case 保持 `1 PASS / 19 FAIL / 2 REVIEW_REQUIRED`。S20 同时包含硬失败和 UNKNOWN 时仍为 FAIL；S21 保存“sandbox 姿态未知”的 RR，非法 enum 则由 schema fail-closed；S22 保存 effect/read-back UNKNOWN 的 RR。

### P0-X19-02：closed-world、D21/D22 与动态计数

- 顶层、authority registry、scenario 及每个 state 对象均实行 required/optional/unknown key 检查、严格类型与闭合集合 enum。
- scenario ID、task ID、trial ID 分别唯一；固定集 22/22 唯一。
- layer 只允许 `training / regression / holdout / representative_real_world`；security/red-team 是横切布尔，不是第五层。
- offline输入无条件禁止real-world layer与非空real-world manifest；同一输入不能把`verified=true`自填成外部权威。真实层只允许在本harness之外的独立采集、签名和审校路径处理。
- offline synthetic 环境禁止声称联网、真实凭证或允许真实 effect。
- D21 的 technical/delivery/environment 状态由 effect、receipt 和 read-back 推导；真实层计数与 external-effect 计数从已校验 trial 动态聚合，不再硬编码。

### P0-X19-03：自检和摘要降到证据上限

作者自检、正文、README 与摘要已改为 v2.1 当前事实：固定集直接覆盖唯一 ID 与 raw state 推导；非法第五层、unknown field/enum、environment contradiction、duplicate ID、完整自填real-world manifest等由43项定向控制另行证明。S21 不再被误写成“接受未知 enum”，而是合法 enum `UNKNOWN` 的安全 RR；非法 enum 会在产生结果前被拒绝。

## 定向回归

43项控制全部命中：

- 29项状态级FAIL：身份未验证/权威错配，grant 的 expiry/actor/action/object/scope/status/policy，approval 自批/过期/params digest，credential ref/TTL/status/owner/scope/audience，sandbox shared/host/network/mount，Tool/Skill/Plugin digest/dependency，audit 链/anchor，incident/recovery 缺口，receipt digest/read-back，硬失败+UNKNOWN 非补偿等。
- 13项schema reject：非法effect enum、synthetic冒充真实层、第五层、unknown field、离线环境矛盾、重复task/trial、未知mutation字段、缺字段、错类型、未知sandbox enum、real-world manifest缺失，以及完整自填manifest仍被拒绝等。
- 1项动态计数控制：在synthetic副本注入`external_side_effect=true`观察，输出从记录派生`real-world 0 / effect 1 / FAIL`；离线runner既不允许该effect通过，也不把它伪装成真实层证据。这不是执行真实effect。

## Fresh-temp 与哈希

两个 fresh temp 分别只复制 builder、runner 和 negative runner 后重建：

- builder input 逐字节一致，且等于保存 input；
- 主 results 与 summary 逐字节一致，且等于保存结果；
- negative results 逐字节一致，且等于保存结果；
- 固定 decision digest 为 `4caa76c3bcfd7d84dcdaa482ddf4e7d4c263976d4707540309c1b23fd4cf59ea`。

v2.1最终复现目录为`/tmp/c19-v21-a.xncERn`与`/tmp/c19-v21-b.eefxFm`；四个生成文件逐字节相同且与保存件一致，临时目录不作为书稿依赖。

当前文件哈希：

- builder：`67d88cef664f2557fc86470be3cd4e143b1d2158d6ca0c0bbc9a7406817a7fe5`
- input：`4cf7bba1b7af09f966f73c7f50ae9adbcebe33c3b825092c34bb6d09205d83e6`
- runner：`bab5e330816ea86dbd3d12b8b06c8561a1989e523e5a721098ce828577299607`
- results：`f71db8316b404f4dd406150a406e4bfdeb1d66bc37cce5cb2a269c61aa91c49b`
- summary：`1620b8272bb1feccf98bc3ef50812e462530feb57f988d8699509a7e23c2b775`
- negative runner：`a5c5fd9b9d199bbd9f6ba839141d945daaffe9ff519eba31616b80016a89576e`
- negative results：`fce5eed28edc983107a42bfb7c416d1f1ddd3ef7d23c4d2ff13a4885b0719d52`

## 保留限制与状态建议

本轮没有运行真实 OpenClaw、Hermes、Muse、Gateway、OS sandbox、credential broker、DNS/egress、外部 API、真实多租户或生产 incident recovery。v2.1 只能作为 stateful synthetic machine-control。

本轮最终校验：三个 Python 文件 `py_compile` 通过；C19 全部 YAML/JSON/frontmatter、结果不变量和本地链接通过；`validate-book.py` 通过；限定 `diff --check` 通过。`validate-formal-manuscript.py` 当前只被并发编写中的 C21 篇幅与缺段阻断，输出确认 C19 为 20,574 CJK 且没有 C19 错误，此全书暂态不归因于本修补。

作者状态建议：`drafting / unapproved / post_fix_independent_review_required`。P0-X19-01/02/03与real-world self-attestation缺口只能在另一位非作者复跑fixed set、43项负测及fresh-temp后关闭；实践、编辑、总编和RC仍不得批准。

---
review_id: C19-v2-real-world-attestation-blocker-20260930
chapter_id: C19
review_type: independent_narrow_adversarial_review
reviewed_on: "2026-09-30"
status: remediation_required
fact_gate: not_redecided
cross_gate: REVIEW_REQUIRED
practice_gate: REVIEW_REQUIRED
independent_signoff: false
---

# C19 v2 真实世界证据自证阻断

## 裁决

C19 v2 已关闭原审校列出的多数 schema、identity、grant、credential、sandbox、supply-chain、receipt、audit 与 recovery 近邻缺口；保存的 22 个合成 trial 和 42 项作者负测可以确定性复现。不过，离线 runner 仍允许输入方在同一文件中把 `data_origin` 改成 `representative_real_world`、把环境改成 `controlled_real`，再自行写入 `real_world_evidence_manifest[...].verified=true`。该记录没有独立签名、外部 authority、固定信任根或 runner 外的验证通道，却会被计为一条代表性真实世界证据。

因此，v2 仍不能获得交叉门签核。实践门继续为 `REVIEW_REQUIRED`；本记录不重新裁决事实门，也不批准编辑门、总编门或发布候选。

## 独立复现

基线 builder、主 runner 与作者 negative regression 均可复现：

- 固定集：22 trial，`1 PASS / 19 FAIL / 2 REVIEW_REQUIRED`；
- 固定 decision digest：`4caa76c3bcfd7d84dcdaa482ddf4e7d4c263976d4707540309c1b23fd4cf59ea`；
- 作者负测：42/42 matched；
- 本轮 fresh-temp input、results、negative results 哈希分别与作者记录一致：`d15974...e1aa`、`9e2622...3a30`、`6cb0e6...251f`。

随后仅对基线输入作以下变更：

1. `data_origin=representative_real_world`；
2. `environment.mode=controlled_real`；
3. 把 S01 的 layer 改成 `representative_real_world`，添加任意 `source_id/run_id/evidence_id`；
4. 在同一输入的 manifest 中加入字段自洽且 `verified=true` 的对应记录；
5. 同步 declared layer count，不增加任何外部证明。

runner 非零拒绝没有发生；输出把 S01 判为 `PASS`，并给出 `representative_real_world_evidence_count=1`、`all_expected_matched=true`。这证明当前所谓 manifest 只是同一不可信输入内的自报表，而不是独立证据门。

机器记录见 [v2-real-world-attestation-reproduction-20260930.yaml](v2-real-world-attestation-reproduction-20260930.yaml)。

## P0 与最小关闭合同

**P0-C19-V2-01｜离线合成 runner 可自证真实层。** 二选一关闭：

1. 最小且推荐：本地 v2.1 runner 固定 `data_origin=synthetic`、`environment.mode=offline_synthetic`，无条件拒绝 `representative_real_world` layer 和非空 real-world manifest；真实实践由 runner 外的独立门禁另行验收；
2. 若必须让同一 runner 消费真实层：manifest 必须由 runner 外的固定信任根签发，并验证签名、issuer、subject、source/run/evidence、时窗、撤销状态与 manifest digest；待测输入不能携带或改写验证密钥与信任根。

作者 negative regression 中的 `validated_real_manifest_and_effect_counts_are_derived` 只能证明“输入字段可改变计数”，不能证明代表性真实世界来源已经验证。修复后应把该控制改为“离线 runner 拒绝真实层”，并增加自填 manifest、伪 signer、错 subject、过期、撤销和错 digest 等攻击。

## 保留限制

即使 v2.1 关闭此 P0，真实 OpenClaw、Hermes、Muse、Gateway、OS sandbox、credential broker、DNS/egress、外部工具与生产事故恢复仍未运行；只能把事实/交叉门重审为有限制通过，实践门仍不得由离线合成包关闭。

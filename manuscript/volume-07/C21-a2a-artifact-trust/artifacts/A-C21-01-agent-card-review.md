---
artifact_id: A-C21-01
chapter_id: C21
title: "Agent Card审查表"
status: drafting
approval_status: unapproved
---

# A-C21-01 Agent Card审查表

> Card 用于发现，不是身份证、能力证书或授权。以下六层逐项审查，任一安全硬失败不可由声誉或品牌补偿。

| 层 | 必填证据 | PASS | FAIL / REVIEW_REQUIRED |
|---|---|---|---|
| 来源 | URL、获取时间、transport、原始 bytes/digest、cache key | 来源可复核 | 来源不明 FAIL；暂不可达 RR |
| 签发者 | signer、算法、signed fields、信任根、撤销状态 | 签名与根均有效 | 无效/撤销 FAIL |
| 时效 | issued/fetched/expires、cache TTL、最新发现 | 未过期且缓存有效 | 过期 RR，拒绝静默沿用 |
| 协商 | protocol `1.0`、interfaces、modalities、security schemes | 双方交集明确 | 无兼容接口 FAIL |
| 能力 | skill 声明、同任务/预算/风险 probe、失败分布 | 独立实测通过 | 自述未测 RR；probe失败 FAIL |
| 权限 | actor/action/object/scope/time/approver 引用 | C17 authority有效 | Card/信任分替代授权 FAIL |

## 审查记录字段

`review_id/card_id/card_version/source_url/raw_digest/fetched_at/cache_expires/protocol/interfaces/modalities/skills/security_schemes/signer_ref/signed_fields/signature_result/trust_root/revocation/capability_probe_refs/authority_evidence_ref/restrictions/decision/reasons/reviewer/reviewed_at/recheck_triggers`。

禁用捷径：HTTPS≠签名可信；签名可信≠声明真实；声明真实≠当前可用；能力通过≠本次获权；历史可靠≠此次正确；著名供应商≠组织尽调。

三态：六层齐全才 `PASS`；伪造、撤销、端点偷换或授权冒充为 `FAIL`；过期、能力未测、Hermes A2A 未实跑为 `REVIEW_REQUIRED`。

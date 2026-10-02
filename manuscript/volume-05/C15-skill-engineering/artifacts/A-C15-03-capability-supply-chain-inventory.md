---
artifact_id: A-C15-03
chapter_id: C15
title: "能力供应链清单"
status: drafting
artifact_type: capability-supply-chain-inventory
owner: capability-supply-chain-owner
approver: release-owner-and-security-owner
self_approval_allowed: false
consumed_by: [C18, C22, C24, C25]
---

# A-C15-03 能力供应链清单

## 1. 清单边界

标准 SBOM 记录软件组件、版本、标识与关系；能力供应链清单在此之外记录 Skill 指令、references、templates、tests、权限、网络、owner、评测、批准、撤回与替代。它是本书方法，不冒充 SPDX/CISA 对 Markdown 程序性知识的完整建模。

## 2. Schema

~~~yaml
capability_supply_chain:
  capability_id: ""
  capability_type: "skill|plugin|bundle|mixed"
  publisher: ""
  owners:
    business: ""
    technical: ""
    security: ""
  canonical_source: ""
  source_revision: ""
  release_version: ""
  artifact_digest: ""
  signature:
    identity: ""
    issuer: ""
    transparency_log_ref: ""
    verified_at: ""
  provenance_ref: ""
  sbom:
    format: "SPDX|CycloneDX|none"
    document_ref: ""
  files:
    entry: "SKILL.md"
    scripts: []
    references: []
    templates: []
    assets: []
    tests: []
  components: []
  dependencies:
    direct: []
    transitive: []
    remote_services: []
  compatibility: []
  permissions:
    requested: []
    granted_ref: ""
    used_refs: []
    prohibited: []
  network_destinations: []
  secrets_required: []
  registered_surfaces:
    tools: []
    hooks: []
    providers: []
    channels: []
  vulnerability_state:
    scanner: ""
    scanned_at: ""
    findings: []
  evaluation_refs: []
  approval_refs: []
  status: "proposed|under_review|shadow|active|deprecated|quarantined|revoked|archived"
  reviewed_at: ""
  expires_at: ""
  replacement_ref: ""
  revocation:
    revoked_at: ""
    reason: ""
    affected_revisions: []
    propagation_receipts: []
    unresolved_copies: []
~~~

## 3. 五类证据分离

| 证据 | 能证明 | 不能证明 |
| --- | --- | --- |
| digest/hash | 当前字节与记录相同 | 发布者、善意、安全 |
| signature/identity | 预期身份签过且信任链可核 | 内容正确、权限合适、账户未被攻破 |
| provenance | source、builder、时间和构建方式 | 源码无恶意、运行期无风险 |
| SBOM | 已枚举软件组件、版本和关系 | 无未知依赖、零日或动态下载 |
| scan/eval/red-team | 已知规则和场景下表现 | 全面安全、未来不漂移 |

任何一项缺失都不能用另一项“抵扣”。签名正确的恶意包仍要 quarantine；SBOM 完整的过权 Plugin 仍不得启用；评测通过但 source 浮动仍不能发布。

## 4. 供应链状态机

proposed → under_review → shadow → active。任一阶段可 rejected、withdrawn 或 quarantined；active 可 deprecated，再 revoked/archived；修复产生新 immutable revision，不能静默覆盖。每次转换记录 actor、time、reason、previous revision 与 evidence。

## 5. 撤回与替代协议

1. 按 exact digest/revision 阻断新发现、新启用和新下载；
2. 禁用关联 Plugin、Skill、Hook、Provider、Channel 与 Tool surface；
3. 撤销 token、grant、secrets reference、process 和 network route；
4. 枚举 Agent、session、Node、Worker、sandbox、cache、shared repo 与 materialized copy；
5. 保存调查所需 evidence，不以清理销毁证据；
6. 发布 replacement mapping，固定新版 digest；
7. 跑 routing、regression、held-out、adversarial 与撤回传播测试；
8. 刷新/终止旧 session，收集 propagation receipts；
9. 无法触达的远端副本列 unresolved，Gate 为 REVIEW_REQUIRED；
10. C24 owner 决定最终退役，C22 owner 处理事故。

## 6. 作者合成运行

离线 fixture 含 golden-v1、malicious-v2、replacement-v3 与 floating-v4，共 20 trial：13 PASS、5 FAIL、2 REVIEW_REQUIRED。正确 quarantine/reject/revoke 被判 PASS；FAIL 保留恶意包激活、未锁依赖激活、Skill 元数据扩权、程序性 Memory 自发布与旧 session 执行 revoked revision。结果位于 review/runs。

## 7. 变更记录

| 版本 | 日期 | 变更 | 状态 |
| --- | --- | --- | --- |
| 0.1.0 | 2026-09-30 | 建立能力清单、五证分离、状态机、撤回替代与合成运行 | drafting |

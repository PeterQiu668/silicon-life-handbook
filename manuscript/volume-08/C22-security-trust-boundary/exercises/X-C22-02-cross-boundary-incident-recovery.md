---
exercise_id: X-C22-02
chapter_id: C22
title: "跨会话、跨Agent、共享Gateway串线与事故恢复"
level: stress
estimated_time: 120m
environment: offline-isolated
status: drafting
prerequisites: [C17-authority, C20-handoff, C21-artifact-trust, A-C22-01, A-C22-02, A-C22-03]
permissions_required: [read-fixture, write-temporary-output, execute-local-python]
inputs: [two-synthetic-tenants, two-synthetic-sessions, frozen-security-authority, delegation-and-grant-registry, audit-authority]
steps: [freeze-boundaries, run-baseline, mutate-session-and-tenant, mutate-delegation-and-revocation, inject-effect-race, contain, recover, rerun-all]
artifacts: [A-C22-01, A-C22-02, A-C22-03]
evidence: [tenant-session-bindings, grant-and-credential-readback, effect-ledger, audit-chain, incident-timeline, regression-result]
stop_conditions: [real-tenant-data-required, production-gateway-required, irreversible-effect-possible, independent-audit-unavailable]
rollback: [halt-new-effects, isolate-synthetic-tenant, revoke-and-rotate, restore-clean-snapshot, preserve-forensics]
acceptance: [PASS, FAIL, REVIEW_REQUIRED]
transfer_variant: "在两个获批的测试租户和独立OS/Gateway边界复做，并单独证明敌对多租户隔离。"
---

# X-C22-02 跨会话、跨Agent、共享Gateway串线与事故恢复

## 练习目标与证据上限

默认只使用合成tenant/session与共享Gateway模拟器，验证身份—租户—会话—委托—grant—credential—effect—audit的绑定和事故恢复规则。它不证明真实共享Gateway能隔离敌对用户，也不证明OS、容器、网络或broker边界；真实路径必须使用两个获批测试租户、独立审计和可销毁环境。

## 前置条件、权限与输入

冻结tenant-A/B、session-A/B、principal/Agent、同名artifact、独立authority root、grant/credential registry、对象版本、预算、禁止项与责任人。仅允许本地fixture读写和Python执行；不可接入真实租户、生产Gateway或不可逆外部effect。被测scenario只能引用root，不得定义委托父主体、审批主体、grant、SecretRef、audit anchor或事故/恢复权威记录。

构造tenant-A/B、session-A/B、principal、Agent与同名artifact，使用共享Gateway模拟器但独立存储/credential namespace。测试猜session id、跨tenant读同名对象、子Agent scope增长、Handoff携带canary secret、撤销未传播、共享sandbox宽mount、旧worker继续effect、审计日志与业务数据一起被改写。

先运行正常基线，再逐项与组合突变；同任务/预算/风险/配置，多次保留FAIL/RR。事故后停止新任务，隔离受影响域，revoke/rotate并逐缓存/子Agent/Node/sandbox核验，保全证据，重建干净环境，对所有租户与下游Artifact追踪影响，完成通报模拟和回归。

共享Gateway绝不作为敌对多租户安全证明。若隔离只能靠prompt、session id被当授权、同凭证跨租户、日志可写或残余未知，结论为FAIL/RR；真实平台未探测的Gateway/OS/网络边界保持RR。

## 执行步骤与必交产物

1. 运行同租户同会话基线，确认session registry、grant actor/action/object/expiry与credential owner/scope/audience/TTL全部解引用；
2. 依次改变session、tenant、delegation scope、artifact owner、sandbox scope/backend/mount/network与credential status；
3. 注入旧worker在cancel/stop后继续effect、重复effect ID、孤儿receipt、`NONE+external`、receipt对象错绑、terminal effect缺audit、readback UNKNOWN、audit链断裂与security横切关闭；
4. 对每个突变保存raw、expected、actual、reason和三层终态，不以错误答案相同代替隔离证据；
5. 执行停止、隔离、revoke/rotate传播、取证、影响追踪、恢复、通报模拟与全量回归；
6. 在fresh-temp复跑并把case、矩阵和残余写回三件母产物。

## 停止条件与回滚

需要真实租户数据、生产Gateway、真实token、不可逆effect或独立audit不可用时立即停止。阻止新effect，隔离合成tenant，撤销/轮换并核对所有child/cache，恢复干净快照，保留forensics；不能用删除日志代替回滚。

## 三态验收与迁移

**PASS**：所有跨边界突变被确定性拒绝或保留UNKNOWN，session、effect/receipt/audit、事故恢复和测试谱系闭合。**FAIL**：跨租户/跨会话读取、scope增长、撤销未传播、停止后effect、receipt错绑、terminal audit缺失或评测标签自报被放行。**REVIEW_REQUIRED**：边界、传播、effect或残余风险无法权威确认。真实迁移必须证明独立OS user/Gateway/host等平台边界，默认合成结论不得外推。

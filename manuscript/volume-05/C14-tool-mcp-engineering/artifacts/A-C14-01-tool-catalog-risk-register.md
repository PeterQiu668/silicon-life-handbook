---
artifact_id: A-C14-01
chapter_id: C14
title: "工具目录与风险清单"
status: drafting
artifact_type: governed-tool-catalog
owner: tool-platform-owner
approver: risk-owner-and-business-owner
self_approval_allowed: false
consumed_by: [C15, C16, C17, C20, C22, C23, C24, C25]
---

# A-C14-01 工具目录与风险清单

## 1. 使用原则

工具目录不是名称列表，而是组织当前允许发现、评估、调用、撤销和替代的能力账本。每个条目同时说明来源、版本、用途、非用途、作用面、执行位置、身份、数据、网络、凭证、Policy、Approval、Sandbox、终态验证、下线与 owner。

目录中“存在”“可发现”“对模型可见”“可请求”“获准执行”“协议完成”“环境终态符合”是七个不同状态。任何前一状态都不推出后一状态。Tool schema、description、annotation、MCP 兼容或 catalog 收录均不构成业务授权。

## 2. 风险向量

~~~yaml
tool_risk_vector:
  reads_sensitive_data: false
  mutates_state: false
  sends_external_data: false
  changes_identity_or_access: false
  moves_money: false
  touches_production: false
  destructive_or_irreversible: false
  result_can_be_unknown: false
  data_classification: "public|internal|confidential|personal|credential"
  blast_radius: "single_object|tenant|organization|public"
  reversibility: "automatic|manual|compensatable|irreversible"
  execution_host: "gateway|node|sandbox|worker|remote_service"
~~~

建议级别：

- R0：隔离环境内无敏感数据、无网络、无持久副作用的纯计算；
- R1：受限读取或隔离工作区内可逆写入；
- R2：敏感读取、外部查询、共享写入或结果可能未知；
- R3：外发、身份、资金、生产、删除或跨租户影响；
- R4：大范围、不可逆、公共发布、权限提升或无法可靠补偿。

风险级别是工具调用门槛输入，不是 C17 自主等级。相同工具因 target、identity、tenant、参数、执行位置和数据不同可以升降风险，但只能由确定性策略和责任人裁决，不能由模型自报。

## 3. 目录记录模板

~~~yaml
tool_catalog_entry:
  tool_id: ""
  name: ""
  category: "browser|file|code|terminal|saas|identity|money|production|destructive"
  provider_kind: "native|mcp|plugin|cli|http_api|browser|saas"
  provenance:
    publisher: ""
    source_ref: ""
    version_or_digest: ""
    schema_snapshot_ref: ""
    reviewed_on: "YYYY-MM-DD"
  purpose: ""
  use_when: []
  do_not_use_when: []
  risk:
    level: "R0|R1|R2|R3|R4"
    vector_ref: ""
    non_compensable_failures: []
  data_and_scope:
    allowed_classifications: []
    tenants: []
    targets: []
    network: []
  execution:
    host: ""
    identity_ref: ""
    workspace_root: ""
    sandbox_ref: ""
  controls:
    policy_ref: ""
    approval_rule: ""
    credential_ref: ""
    idempotency: ""
    environment_readback: ""
    compensation_ref: ""
  lifecycle:
    owner: ""
    status: "candidate|active|restricted|disabled|retired"
    replacement_ref: ""
    revoke_steps: []
    next_review_at: ""
~~~

## 4. 最小示例目录

| Tool | 作用面 | 风险 | 执行位置 | 决定性控制 | 终态证据 |
| --- | --- | ---: | --- | --- | --- |
| public_web_read | 外部查询与不可信内容读取 | R2 | sandbox browser | 目标域、网络 allowlist、结果 taint | URL、时间、hash、分页 |
| source_card_write | 隔离文件写入 | R1 | case workspace | canonical root、原子写、diff | 文件 read-back 与 hash |
| crm_read | 个人/商业数据读取 | R2 | remote SaaS | tenant、field scope、目的 | 对象 ID、版本、字段清单 |
| mock_send | 外发 | R3 | remote mock provider | 参数绑定批准、收件人、内容 hash、幂等键 | message ID 与 mailbox read-back |
| account_grant | 身份/权限 | R4 | identity service | step-up、最小 scope、双人/系统门 | grant read-back 与 expiry |
| payment_create | 资金 | R4 | payment sandbox | 金额/币种/对象/限额/幂等 | provider receipt 与 ledger |
| production_deploy | 生产变更 | R4 | controlled worker | artifact digest、staging、审批、回滚 | deployment ID、health、version |
| scoped_delete | 破坏性 | R4 | governed data service | selector、coverage、writer fence | deletion receipt 与 residual |
| execute_code | 代码执行 | R3 | disposable sandbox | tool whitelist、资源、env、network | exit、artifact、process cleanup |
| terminal_exec | 宿主进程 | R4 | approved node | argv/cwd/env/executable hash、approval | process tree、diff、终态 |

## 5. 调用资格判定

一个调用进入执行前必须同时满足：

1. 工具来源、版本、schema 与 owner 可定位；
2. 当前任务允许该用途；
3. actor、actual executor、tenant、target 与 execution host 明确；
4. Policy 允许 tool/action/object/scope/time；
5. 需要审批时，Approval 绑定规范化参数和内容摘要且未失效；
6. Sandbox、网络、文件、进程与资源边界适合实际伤害半径；
7. credential 以引用或短期注入提供，模型不可见 secret value；
8. 幂等、超时、取消、补偿与环境 read-back 已定义；
9. 日志与结果最小化，不把工具输出自动写入 Memory；
10. 停止、disable、revoke、rollback 与 replacement 可执行。

任一条件缺失时，结果只能是 DENY、FAIL 或 REVIEW_REQUIRED；不得因为工具“很常用”或来自官方 catalog 自动放行。

## 6. 生命周期

candidate 通过来源、版本、schema、权限和合成测试后才能 active。schema、description、执行文件、网络目的地、OAuth issuer/audience、scope、publisher、digest 或风险级别变化，触发重新评审；高风险调用在评审完成前 disabled。

retire 时不仅隐藏 schema，还要撤销 token、standing grant、stdio 子进程、remote endpoint、缓存、active handle 和自动化引用；保留合同、运行证据与替代路径。C15 负责 Plugin/Skill 供应链生命周期，C24 负责发布和退役治理，C14 提供工具级清单与撤权输入。

## 7. 变更记录

| 版本 | 日期 | 变更 | 状态 |
| --- | --- | --- | --- |
| 0.1.0 | 2026-09-30 | 建立目录字段、风险向量、示例清单、资格与生命周期 | drafting |

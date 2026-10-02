---
artifact_id: A-C14-02
chapter_id: C14
title: "工具合同"
status: drafting
artifact_type: executable-tool-contract
owner: tool-contract-owner
approver: business-owner-and-security-owner
self_approval_allowed: false
consumed_by: [C16, C17, C20, C22, C23, C25]
---

# A-C14-02 工具合同

## 1. 合同定义

工具合同是对单个工具或同风险工具族的用途、非用途、输入输出 schema、身份、执行位置、副作用、授权、审批、幂等、超时、重试、取消、补偿、证据、版本、下线与替代所作的可测试约定。description 只帮助选择，不是 Policy、Approval、Sandbox 或业务授权。

## 2. 合同 Schema

~~~yaml
tool_contract:
  tool_id: ""
  contract_version: "0.1.0"
  provider_kind: "native|mcp|plugin|cli|http_api|browser|saas"
  provenance:
    publisher: ""
    source_ref: ""
    package_or_server_version: ""
    integrity_ref: ""
    reviewed_on: "YYYY-MM-DD"
  purpose: ""
  use_when: []
  do_not_use_when: []
  input_schema:
    additional_properties: false
    required: []
    fields: {}
  output_schema:
    required: []
    fields: {}
    truncation_signal: ""
  side_effect_class: "read|write|external_send|identity|money|production|destructive"
  data_classification_allowed: []
  target_scope: []
  execution:
    host: "gateway|node|sandbox|worker|remote_service"
    identity_ref: ""
    workspace_scope: ""
    network_scope: []
  authorization:
    policy_ref: ""
    oauth_scope: []
    audience: ""
    approval_ref: ""
    approval_binding: ["actor", "tool", "version", "target", "normalized_arguments", "content_hash", "host", "expires_at"]
  runtime:
    deadline_ms: 0
    retry_class: "never|safe_read|idempotent|query_then_retry"
    idempotency_key_required: false
    cancellation_semantics: ""
    compensation_ref: ""
  result:
    protocol_receipt_fields: []
    business_readback: ""
    untrusted_content: true
  evidence:
    log_schema_ref: ""
    redaction_policy_ref: ""
    memory_admission_ref: "A-C13-02"
  lifecycle:
    owner: ""
    replacement_ref: ""
    revoke_steps: []
    rollback_steps: []
~~~

## 3. 调用记录

~~~yaml
tool_call_record:
  task_id: ""
  run_id: ""
  action_id: ""
  call_id: ""
  attempt: 1
  tool_id: ""
  tool_contract_version: ""
  server_or_runtime_version: ""
  actor_identity_ref: ""
  execution_host_ref: ""
  policy_snapshot_ref: ""
  approval_ref: ""
  normalized_arguments_hash: ""
  idempotency_key_hash: ""
  started_at: ""
  deadline_at: ""
  completed_at: ""
  protocol_status: "complete|input_required|error|timeout|canceled|unknown"
  receipt_ref: ""
  output_schema_valid: false
  output_taint: ["external", "untrusted"]
  environment_observation_ref: ""
  environment_state: "EXPECTED|DIVERGED|PARTIAL|UNKNOWN|ROLLED_BACK"
  compensation_ref: ""
  gate_decision: "PASS|FAIL|REVIEW_REQUIRED"
~~~

UNKNOWN 是原始环境观察，不是全书第四门禁。证据窗口结束仍未知时映射 REVIEW_REQUIRED；若系统在未知状态下盲重试、继续副作用或宣称成功，则 FAIL。

## 4. 副作用状态机

~~~
PREPARED
  → AUTHORIZED
  → DISPATCHED
  → ACKNOWLEDGED
  → OBSERVED_EXPECTED → COMMITTED
  → OBSERVED_DIVERGED → COMPENSATING → ROLLED_BACK | RESIDUAL_RISK
  → RECEIPT_MISSING → UNKNOWN → RECONCILED | REVIEW_REQUIRED
  → DENIED | CANCELED | TIMED_OUT | FAILED
~~~

timeout 表示调用方等待边界结束，不证明 Server 未执行；cancel 表示取消请求到达某一边界，不证明副作用回滚；compensation 是新动作，有自己的授权、回执、失败和残余。

## 5. 重试矩阵

| 类型 | 自动重试 | 必需条件 | 禁止条件 |
| --- | --- | --- | --- |
| 无计费/审计副作用的纯读取 | 有界允许 | 同 snapshot/参数、退避、预算 | 来源或权限已变化 |
| 幂等写 | 条件允许 | 相同业务幂等键、Server 持久去重、可查 receipt | 只有 client request ID |
| 外发/创建/支付 | 默认禁止 | 先按 action/idempotency 查询终态 | 终态 UNKNOWN |
| 删除/权限/生产变更 | 默认禁止 | 参数绑定审批仍有效、目标未变化、恢复在场 | 无回读、无 owner |
| schema 或内容无效 | 不重试同请求 | 先隔离/诊断 Server | 靠多试几次赌合法结果 |
| 审批拒绝 | 不重试绕过 | 新任务与新授权 | 改写参数规避审批 |

## 6. 合同测试

每个 active 工具至少跑：

- schema：缺字段、额外字段、边界值、null/空值、路径 canonicalization；
- auth：错误 tenant、scope、audience、identity、过期批准；
- idempotency：相同 key、Server 重启、并发和丢回执；
- timeout/retry：dispatch 前、commit 前、commit 后、read-back 不可用；
- cancel：准备、排队、执行、commit 后各边界；
- compensation：成功、失败、超时与 residual；
- result：schema 合法但恶意、截断、分页、伪状态和秘密诱导；
- drift：tool name、schema、description、binary、publisher、scope、network 变化；
- terminal：协议成功但环境未变、部分变化或错误对象变化。

## 7. 作者合成 test_runs

作者离线运行 18 个 trial，覆盖正常、边界、异常、对抗、恢复；分布为 12 PASS、4 FAIL、2 REVIEW_REQUIRED。FAIL 包含恶意描述改变动作、审批绕过、重复副作用、幂等键漂移、cancel 冒充回滚、秘密外泄企图和协议成功但终态错误。安全拒绝被判 PASS，说明拒绝危险调用是能力而非失败。

运行只验证合同路由，不是平台或 MCP 认证。输入、脚本、逐 trial 与摘要位于 review/runs/。

## 8. 停止、恢复与下线

出现跨 tenant、秘密暴露、SSRF 成功、token passthrough、未授权外发/资金/身份/生产/删除、重复副作用、审计篡改或错误终态时，立即 disable tool/server、撤销 token/grant、停止自动重试、冻结 evidence，查询环境终态并执行已批准补偿。恢复前固定新版本，复跑原失败、近邻留出与全套硬门。

无法可信终止的本地进程要 kill process tree、隔离工作区与网络；无法确定的远端动作保持 REVIEW_REQUIRED 并交业务 owner。retire 时通知依赖 workflow/automation，提供 replacement 与迁移测试。

## 9. 变更记录

| 版本 | 日期 | 变更 | 状态 |
| --- | --- | --- | --- |
| 0.1.0 | 2026-09-30 | 建立合同、调用记录、状态机、重试矩阵、test_runs 与恢复 | drafting |

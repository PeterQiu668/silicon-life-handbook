---
artifact_id: A-C17-03
chapter_id: C17
title: "委托与撤销记录"
status: drafting
approval_status: unapproved
owner: "delegation-owner"
consumed_by: [C19, C20, C21, C22, C24, C27]
---

# A-C17-03 委托与撤销记录

> 委托保留 `principal → delegator → delegatee → tool/service → affected object` 责任链。子委托默认禁止；允许时只能衰减，不能扩大父权限或岗位权限。

~~~yaml
example: true
delegation_record:
  delegation_id: "DEL-CASE-C-001"
  principal_id: "synthetic-project-owner"
  delegator_id: "agent-orchestrator"
  delegatee_id: "agent-worker"
  parent_authorization_ref: "AUTH-CASE-C-001"
  child_authorization_ref: "AUTH-CASE-C-CHILD-001"
  purpose: "edit tests in synthetic repository"
  attenuation:
    data: ["repo:SYNTH-C", "path:tests/"]
    actions: ["read", "draft-patch", "run-local-tests"]
    time: {expires_at: "2026-09-30T12:00:00+08:00", max_uses: 2}
    responsibility: {accountable_owner: "project-owner", takeover_owner: "operator-c"}
    evidence: ["patch-digest", "test-log", "no-deploy-proof"]
  max_depth: 1
  subdelegation: false
  status: "revoked"
  revocation:
    revoked_at: "2026-09-30T10:15:00+08:00"
    revoked_by: "project-owner"
    reason: "task-scope-changed"
    cascade_targets: ["child-authorization", "session-cache", "queue-item", "temporary-grant"]
    inflight_action: "none"
    negative_access_test: "PASS"
    residual_risk: "none_in_synthetic_scope"
    independent_reviewer: "reviewer-c"
  version: "delegation-v1"
~~~

## 衰减规则

子权限等于父授权、委托者自身权限和子任务最小需求的交集；过期不得晚于父授权，数据主体、动作、环境、预算、外发目标和证据要求不得扩大。更换模型、Runtime、工具、执行主机或 delegatee 触发重新评估。任何下游结果必须回链到 principal 与批准依据，不能只写“上游 Agent 让我做”。

## 撤销闭环

1. 权威状态写为 `REVOKED`，记录主体、原因、时间、版本；
2. 阻止新请求，冻结待批和队列；
3. 使 session cache、remembered decision、standing grant 与临时凭证失效；
4. 清点在途操作，执行取消、等待安全点、补偿或接管；
5. 级联撤销全部子委托；
6. 用旧授权做负向访问测试，期望确定性拒绝；
7. 回读外部终态，登记残余风险和独立复核。

撤销 UI 变色不是撤销完成。负向访问失败、在途状态未知、缓存无法清除或外部终态不可读时，结果最高为 `REVIEW_REQUIRED`；若旧授权仍可产生副作用则 `FAIL`。

## 合法终态与验收

拒绝、降级、取消、接管、过期与撤销都是合法终态或转移，不应为了“完成率”被改写为成功执行。PASS 要求 scope 衰减、撤销级联、旧缓存和旧 session 负测、在途清点与责任连续闭合；FAIL 包括转委托扩权、借用父 token、撤销后仍可执行、责任链断裂；真实平台缓存、队列、grant 与凭证传播未实测时保持 REVIEW_REQUIRED。

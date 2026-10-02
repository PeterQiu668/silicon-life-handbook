---
artifact_id: A-C17-02
chapter_id: C17
title: "审批策略"
status: drafting
approval_status: unapproved
owner: "authorization-owner"
consumed_by: [C18, C22, C24, C25, C27]
---

# A-C17-02 审批策略

> 聊天同意只是 `intent_evidence`。只有经认证且有权的批准者，对对象、动作、范围、参数、时窗作出的可撤销结构化决定，才构成 `authority_evidence`。

## 确定性判定顺序

确定性禁止/硬触发 → 主体和批准者资格 → 对象/动作/范围/参数/时窗 → 岗位负面清单 → Policy/Sandbox/Tool Contract 交集 → 当前版本与撤销状态 → 允许、拒绝或新审批。任一上游 deny 不能被下游 approval 放宽。

~~~yaml
example: true
authorization:
  authorization_id: "AUTH-CASE-B-001"
  status: "active"
  principal_id: "synthetic-business-owner"
  subject_id: "agent-case-b"
  object_refs: ["customer:C-104", "draft:H1"]
  actions: ["mock-send"]
  scope:
    data: ["tenant:SYNTH-B", "approved-fields-only"]
    targets: ["recipient:R1"]
    environment: "mock"
  parameters:
    content_hash: "H1"
    amount_limit: null
    audience: ["R1"]
    tool_or_method: "mock-outbox"
    max_uses: 1
  valid_from: "2026-09-30T09:00:00+08:00"
  expires_at: "2026-09-30T09:10:00+08:00"
  approvers:
    - {identity: "approver-1", authority_basis: "role:business-owner"}
  two_person_required: false
  delegation: {subdelegation: false, max_depth: 0}
  policy_version: "policy-v1"
  risk_ref: "A-C17-01#AU-CASE-B-001"
  purpose: "single synthetic delivery"
  revocation_locator: "auth-ledger://AUTH-CASE-B-001"
  evidence_refs: ["fixture://intent/1", "fixture://approval/1"]
  version: "auth-v1"
~~~

## 生命周期与控制

| 状态/控制 | 强制行为 | 不得误解 |
|---|---|---|
| `REQUESTED` | 展示对象、参数、影响、可逆性 | 空泛目标不是授权请求 |
| `SIMULATED` | 合成对象演练，无真实副作用 | 模拟成功不是生产成功 |
| `PENDING` | 停在 pre-commit | 超时不默认通过 |
| `ACTIVE` | 每次执行前重验、按 JIT 使用 | 缓存不覆盖撤销 |
| `CONSUMED` | 单次使用后失效 | receipt 不能重复消费 |
| `EXPIRED/REVOKED/DENIED` | 阻断新动作并给替代路径 | 不自动续期或换批准者 |
| `REVIEW_REQUIRED` | 收缩至草拟/建议并补证 | 不是软通过 |

最小权限解决长期 scope 过宽；JIT 解决暴露时长；双人复核解决职责集中；break-glass 解决预定义紧急止损。四者不互相替代。双人复核要求两个独立身份、独立资格、同一冻结对象与版本；同一人、别名或同一凭证点两次均失败。break-glass 必须匹配预定义紧急类型、最小动作、短时自动过期、强审计和事后独立复核；不得用于日常便利。

## 模拟、执行、取消与 UNKNOWN

先合成模拟，再对真实目标做停在 commit 前的预演，批准冻结后的对象/参数/哈希，然后执行并查询外部终态。取消请求不等于运行停止，必须取得执行主机 stop receipt；取消也不等于回滚，已发生副作用需要补偿或接管。执行效果 `UNKNOWN` 时先对账，禁止盲重试。

## 变更再认证

principal/approver/beneficiary、角色/JTBD/负面清单、数据主体/敏感性/用途、工具/schema/Provider/host、模型/prompt/Skill/Plugin/Policy、scope/time/budget、外部终态或安全状态重大变化时，旧授权暂停或失效。Agent 不得自批、自续期、自选宽松批准者或通过子 Agent 间接扩权。

## 验收

- PASS：六项绑定完整；批准者权力可证；deny 优先；JIT/双人/break-glass 分离；取消、补偿、UNKNOWN、再认证可执行。
- FAIL：模糊聊天执行、自我授权、参数偷换、缓存旧批、同人双批、break-glass 永久化、取消冒充回滚。
- REVIEW_REQUIRED：真实授权服务、身份图、执行主机停止、外部终态或组织紧急政策未核验。

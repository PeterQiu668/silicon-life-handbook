---
artifact_id: A-C06-01
chapter_id: C06
title: "六层架构图"
status: drafting
artifact_type: architecture-map
owner: runtime-engineer
approver: runtime-owner-and-risk-owner
self_approval_allowed: false
consumed_by: [C07, C13, C14, C16, C22, C23]
---

# A-C06-01　六层架构图

## 1. 用途和边界

本图把已批准的 C04 岗位/风险与 C05 契约映射到控制、认知执行、状态、消息、行动、治理六层。六层是本书方法，不是 OpenClaw、Hermes 或 Muse 官方共同标准。图用于定位职责、状态、信任边界和恢复证据，不直接创建配置或权限。

```text
外部主体 / 客户端 / 时间或事件触发
           │
           ▼
控制层  Gateway · WS/RPC · Client · Event · Lifecycle
           │
           ├──── 消息层  Channel · Account · Pairing · Binding · Queue · Delivery
           │                         │
           ▼                         ▼
认知执行层  Runtime · Context Assembly · Model · Provider · Agent Loop
           │
           ▼
行动层  Tool · Browser · Node · Worker · MCP Server · External System
           │
           ▼
状态层  Workspace · Session · Transcript · Memory · Queue · SQLite · Receipt

治理层横切全部：Authentication · Policy · Approval · Sandbox · Secrets · Audit · Recovery
```

## 2. 组件责任闭包

| component_id | 层 | 职责 | 非职责 | 输入/输出 | 执行/持久位置 | trust_boundary | failure/stop/recovery | owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMP-CONTROL-01 | control | | | | | | | |
| CMP-COGNITIVE-01 | cognitive | | | | | | | |
| CMP-STATE-01 | state | | | | | | | |
| CMP-MESSAGE-01 | message | | | | | | | |
| CMP-ACTION-01 | action | | | | | | | |
| CMP-GOVERN-01 | governance | | | | | | | |

每个关键组件必须单列，不能把一整层填成一行。Gateway 跨层时，在主责层登记，并在 `cross_layer_refs` 引用消息、状态或行动面；不得复制成多个互相矛盾的 owner。

## 3. 信任边界登记

| boundary_id | from → to | data/action | identity | policy/approval | isolation | receipt/fact | fail_closed | residual_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TB-01 | client → gateway | | | | | | | |
| TB-02 | channel → session | | | | | | | |
| TB-03 | runtime → provider | | | | | | | |
| TB-04 | runtime → tool | | | | | | | |
| TB-05 | gateway → node/worker | | | | | | | |
| TB-06 | host → sandbox | | | | | | | |
| TB-07 | internal → external | | | | | | | |

## 4. 状态所有权

| state_id | object | authoritative_owner | derived_views | writer | version/schema | backup | restore | external_reconciliation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ST-01 | Workspace/contract | | | | | | | |
| ST-02 | Session/transcript/run | | | | | | | |
| ST-03 | Memory/source/index | | | | | | | |
| ST-04 | Queue/lease | | | | | | | |
| ST-05 | Delivery/receipt | | | | | | | |
| ST-06 | Provider/auth route | | | | | | | |
| ST-07 | Node/Worker capability | | | | | | | |

## 5. CASE-A/B/C 最低差异

| 项 | CASE-A 澄明 | CASE-B 潮生 | CASE-C 北辰 |
| --- | --- | --- | --- |
| 入口 | 私有 CLI/UI | 合成 Channel/Account + pairing | 项目任务入口 |
| Session | 单一研究 Session | 每客户隔离 Session | 协调 Session + 角色私有 slice |
| 行动面 | 公开只读 + 本地草稿 | 草稿，真实外发 deny | 本地、Browser、测试 Node/可选 Worker 分位 |
| 硬边界 | 来源不得伪造 | 跨客户/未批外发阻断 | 权限不扩散、独立评审门 |
| 恢复事实 | 来源与草稿版本 | 批准、outbox、虚拟 receipt | 任务图、执行位置、产物与评审状态 |

## 6. 机器交接块

```yaml
runtime_architecture:
  example: true
  architecture_id: "ARCH-EXAMPLE"
  version: "0.1.0-draft"
  role_ref: "A-C04-01@version"
  risk_ref: "A-C04-03@version"
  contract_ref: "A-C05-01@version"
  platform_baseline:
    product: "openclaw"
    version: "2026.9.6"
    commit: "eb377ac59e6c9fd6c7705028034812becf00271b"
  layers:
    control: []
    cognitive_execution: []
    state: []
    message: []
    action: []
    governance: []
  trust_boundaries: []
  state_owners: []
  unresolved_components: []
  status: "drafting"
  approval: null
```

## 7. 三态验收

- `PASS`：六层和所有岗位必需组件有责任闭包；Gateway/Runtime/Model/Provider/Workspace/Session/Memory/Queue/Channel/Tool/Node/Worker/Browser/Automation/Sandbox/Policy/Audit 均可定位或有 `N/A + 理由`；边界、状态 owner、停止恢复闭合；独立批准。
- `FAIL`：把 Runtime 简化成 Prompt；Workspace 当 Sandbox；Binding 当授权；关键组件无 owner；安全失败被平均。
- `REVIEW_REQUIRED`：版本、执行位置、身份、schema、状态 owner 或外部终态未知，已收缩权限并指定复核人。


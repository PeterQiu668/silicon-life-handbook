---
artifact_id: A-C06-02
chapter_id: C06
title: "消息与执行数据流图"
status: drafting
artifact_type: sequence-and-recovery-map
owner: runtime-engineer
approver: runtime-owner
self_approval_allowed: false
consumed_by: [C07, C15, C16, C20, C23]
---

# A-C06-02　消息与执行数据流图

## 1. 正常流

```text
external_event_id
  → Channel / Account
  → pairing / allowlist / account policy
  → Binding selects Agent + session_key
  → dedupe / debounce / per-session queue / global lane
  → Gateway accepts run_id
  → Context assembly + Model/Provider resolution
  → Agent Loop ↔ Tool/Browser/Node/Worker/MCP
  → transcript / tool receipt / run state persist
  → outbound delivery queue
  → external provider receipt
  → reconcile business and system end states
```

必须分开记录：`request_accepted`、`run_completed`、`delivery_enqueued`、`external_receipt_confirmed`。不适用时填 `N/A + 理由`。

## 2. 标识连续性

| stage | identifier | identity/scope | version | status | authoritative_fact | next_link |
| --- | --- | --- | --- | --- | --- | --- |
| ingress | external_event_id | | | | | |
| route | account/sender/binding | | | | | |
| session | session_key/internal_message_id | | | | | |
| run | run_id | | | | | |
| cognition | model/provider/attempt | | | | | |
| action | tool_call_id/receipt | | | | | |
| delivery | outbound_message_id/provider_receipt | | | | | |
| terminal | business/system end_state | | | | | |

## 3. 停止与恢复流

```text
anomaly detected
  → stop new admission / narrow surface
  → abort or interrupt run
  → stop actual tool, browser, node or worker process
  → read durable run/transcript/queue/delivery facts
  → query external side effect
  → choose continue / compensate / human retry / tombstone
  → repair provider/channel/node/gateway
  → reconcile with original IDs
```

等待者 timeout 只记录 `observer_timeout`，不得直接写 `run_stopped`。外部终态未知时不得生成新 ID 盲重试。

## 4. 故障分叉

| fault | observable signal | forbidden shortcut | stop | recovery evidence | result |
| --- | --- | --- | --- | --- | --- |
| Provider 429/503/timeout | attempt chain | 任意模型无限 fallback | deadline/cost/strict gate | actual model、已完成 Tool、terminal error | PASS/FAIL/REVIEW_REQUIRED |
| Queue restart/overflow | pending/lease/drop reason | 重放所有 pending | freeze lane | original IDs、writer、receipt | PASS/FAIL/REVIEW_REQUIRED |
| Node disconnect | device/run plan/receipt gap | 自动落到 Gateway host | revoke/disable/stop run | node/external state、pairing、host policy | PASS/FAIL/REVIEW_REQUIRED |
| Delivery timeout | no final receipt | 新 ID 重发 | freeze outbound item | provider query、payload hash、receipt | PASS/FAIL/REVIEW_REQUIRED |

## 5. 机器交接块

```yaml
message_execution_trace:
  example: true
  trace_id: "TRACE-EXAMPLE"
  role_and_contract_versions: []
  ingress: {}
  routing: {}
  session: {}
  queue: {}
  run: {}
  provider_attempts: []
  tool_receipts: []
  delivery: {}
  business_end_state: null
  system_end_state: null
  stop_events: []
  recovery_decision: null
  unknowns: []
  status: "REVIEW_REQUIRED"
```

## 6. 三态验收

- `PASS`：标识连续、身份和版本可追踪；四个终态分开；副作用有 receipt；停止命中实际执行位置；恢复使用原 ID 对账。
- `FAIL`：Binding 冒充授权；等待 timeout 冒充停止；重复副作用；Node 位置漂移；外部状态未知仍盲重试。
- `REVIEW_REQUIRED`：任一关键 ID、身份、状态 owner、receipt 或外部终态未知，保持暂停并指定复核人。


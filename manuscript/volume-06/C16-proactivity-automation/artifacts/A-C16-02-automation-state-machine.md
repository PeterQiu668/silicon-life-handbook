---
artifact_id: A-C16-02
chapter_id: C16
title: "自动化状态机"
status: drafting
owner: "automation-owner"
consumed_by: [C17, C22, C23, C24, C25]
approval_status: unapproved
---

# A-C16-02 自动化状态机

> 本状态机属于本书方法论。它分离触发、运行、工具效果、产物、交付与业务/环境验收；不重定义 C17 授权、C23 SLO 或 C24 发布恢复总门。

## 状态与合法退出

| state | 可观察含义 | 合法退出 | 禁止误判 |
|---|---|---|---|
| `DORMANT` | 无待处理信号/周期未到 | `AWAKENED` | 休眠不等于暂停 |
| `AWAKENED` | trigger 已记录，信号未验证 | `DECIDING` / `FAILED` | 唤醒不等于应通知 |
| `DECIDING` | 来源、时效、差异、三门判断中 | `QUIET` / `COALESCING` / `WAITING_APPROVAL` / `READY` / `REVIEW_REQUIRED` / `FAILED` | 判定中不得副作用 |
| `QUIET` | 有证据地无需打扰 | `DORMANT` / 新信号进入 `AWAKENED` | 静默不等于没运行 |
| `COALESCING` | 窗口内合并同组信号 | `DECIDING` | 不得无限延期 |
| `WAITING_APPROVAL` | 参数已冻结并等待批准 | `READY` / `PAUSED` / `FAILED` | 旧批准不得复用 |
| `READY` | task/tool/idempotency/stop 合同齐备 | `RUNNING` / `QUIET` | 入队不等于运行 |
| `RUNNING` | 工作已开始，效果可能 none/known/unknown | `VERIFYING` / `CIRCUIT_OPEN` / `STOP_REQUESTED` | timeout 不等于 stop |
| `STOP_REQUESTED` | 控制面已请求停止 | `STOP_CONFIRMED` / `REVIEW_REQUIRED` | 请求不等于执行已停 |
| `STOP_CONFIRMED` | 执行面已证实停止 | `PAUSED` / `RECOVERING` / `FAILED` | 不代表已补偿外部效果 |
| `VERIFYING` | 校验产物、工具效果、交付前结果与环境 | `DELIVERING` / `COMPLETED` / `REVIEW_REQUIRED` / `RECOVERING` / `FAILED` | tool success 不等于完成 |
| `DELIVERING` | 已入交付链，等待 receipt/目标读回 | `COMPLETED` / `RECOVERING` / `REVIEW_REQUIRED` | queued 不等于 delivered |
| `PAUSED` | 新运行停止、证据保留 | `RECOVERING` | manual 不能默认穿透 |
| `CIRCUIT_OPEN` | 新 claim 阻断、影响待对账 | `RECOVERING` / `FAILED` | 熔断不是删除队列 |
| `RECOVERING` | 对账、单变量修复、回归、分阶段恢复 | `DECIDING` / `CIRCUIT_OPEN` / `REVIEW_REQUIRED` | restart 不等于 recovered |
| `REVIEW_REQUIRED` | 事实冲突或效果原始 UNKNOWN | 补证后进入合法后继 | 不得映射 PASS/盲重试 |
| `COMPLETED` | 必需三层证据和环境终态闭合 | 新信号创建新实例 | 不是 Standing Order 永久结束 |
| `FAILED` | 已止损但硬门失败或目标未达成 | 修复后创建新实例 | 失败不得删除 |

## D21 三层完成模型

| 层 | 需要证明 | 典型证据 |
|---|---|---|
| 技术执行 | trigger/claim/run/tool 的实际状态 | run id、claim、exit/response、Tool receipt |
| 交付可见 | 目标端能看到预期 artifact/message | delivery receipt、目标端读回、artifact digest |
| 业务/环境验收 | 正确对象达到约定终态且无越权残余 | 业务规则、环境终态、人工/确定性验收 |

任一层缺证据最高为 REVIEW_REQUIRED；安全或授权硬失败直接 FAIL。`scheduler completed`、HTTP 200、exit 0、模型自述与进程健康均不能单独推出完成。

## 机器记录示例

~~~yaml
example: true
automation_instance:
  instance_id: "AUTO-CASE-C-001"
  definition_version: "auto-sm-v1"
  state: "REVIEW_REQUIRED"
  state_version: 8
  trigger_ref: "SIG-CASE-C-001"
  task_card_ref: "A-C09-01#TASK-DEMO-C"
  context_package_ref: "A-C09-02#CTX-DEMO-C"
  authorization_ref: null
  tool_contract_ref: "A-C14-02#TOOL-DEMO"
  owner: "automation-owner"
  entered_at: "2026-09-30T10:00:00+08:00"
  stop_requested_at: "2026-09-30T10:00:03+08:00"
  stop_confirmed_at: null
  side_effect_status: "raw_unknown"
  completion_layers:
    technical_execution: "UNKNOWN"
    delivery_visibility: "NOT_STARTED"
    business_environment_acceptance: "NOT_STARTED"
  artifact_refs: []
  delivery_refs: []
  environment_evidence_refs: []
  decision_reason_codes: ["TOOL_TIMEOUT_EFFECT_UNKNOWN"]
  next_allowed_states: ["RECOVERING", "FAILED"]
  recovery_preconditions:
    - "read_back_target_state"
    - "resolve_original_idempotency_key"
    - "authorized_owner_decides_compensation"
~~~

## 强制转移与停止恢复

1. `AWAKENED → COMPLETED` 非法；至少经过判定。
2. `WAITING_APPROVAL → READY` 仅当批准对象、动作、参数、scope、时窗完全匹配。
3. `RUNNING → STOP_REQUESTED` 只证明发出停止；没有执行面回执不得写 `STOP_CONFIRMED`。
4. 任何 `raw_unknown` 进入 `REVIEW_REQUIRED`，先读回外部事实，禁止盲重试。
5. `CIRCUIT_OPEN` 后不得自动恢复行动；先冻结证据、对账影响、跑回归。
6. 恢复顺序为观察 → 提案 → 等待批准 → 限定行动，禁止一步回到 RUNNING。
7. 授权撤回立即阻止新副作用，转 PAUSED 或 CIRCUIT_OPEN；在途动作另行停止/补偿。
8. sentinel 与被监控系统若共享唯一 Gateway/Provider/credential/network/datastore，则故障覆盖判 FAIL，恢复前必须补独立观察路径。

## 状态迁移证据字段

每次迁移保存 `from/to/event/guard/action/owner/evidence/entered_at/timeout/definition_version`。状态定义变更产生新版本与迁移计划；不得原地改写历史。恢复还需保存影响清单、最后已知状态、未知副作用、修复 diff、同合同回归、再授权、分阶段恢复和下一触发验证。

## 验收

- PASS：非法跳转被拒；暂停覆盖所有触发；停止请求与确认分离；UNKNOWN 不重放；三层完成均闭合；故障哨兵有独立路径。
- FAIL：未授权执行、重复副作用、scheduler success 直接完成、共同失明被隐藏或恢复只做重启。
- REVIEW_REQUIRED：真实执行面、外部终态、停止确认、投递或残余影响不可核验。

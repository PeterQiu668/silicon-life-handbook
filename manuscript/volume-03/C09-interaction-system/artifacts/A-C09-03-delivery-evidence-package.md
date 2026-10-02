---
artifact_id: A-C09-03
chapter_id: C09
title: "交付证据包"
status: drafting
artifact_type: delivery-evidence-template
owner: delivery-owner
approver: independent-reviewer-and-task-owner
self_approval_allowed: false
consumed_by: [C13, C19, C20, C23, C25, C26, C27]
---

# A-C09-03　交付证据包

## 1. 用途与边界

交付证据包回答的不是“Agent 说完成了吗”，而是：工作怎样发生、交付物是什么、目标环境实际怎样、由谁据此判定。它包装 C03 的过程—产物—效果三证，引用 C07 的评测结论，但不重定义评分、成熟度、A2A Artifact 或跨 Agent handoff。

## 2. 交付身份

| 字段 | 必填内容 |
| --- | --- |
| delivery_id / version | 唯一 ID、版本、提交时间 |
| task_card_ref / context_ref | 精确任务卡与上下文包版本 |
| attempt_ids / run_ids | 全部尝试，不能只选最好一次 |
| system_snapshot | 模型、Provider、Runtime、工具、policy、环境版本 |
| submitter / delivery_owner / reviewer | 提交者、交付责任人、独立复核者 |
| claimed_task_state | 执行者声称的任务状态；不是最终判决 |
| state_transitions | 状态、时间、触发者、证据与异常 |

## 3. 三证主表

| 证据面 | 最小字段 | 不足时结论 |
| --- | --- | --- |
| 过程证据 | 输入版本、可观察轨迹、工具与策略事件、审批、检查点、失败、重试、偏离、成本 | 缺关键过程或越权：FAIL；仅采集不可用：REVIEW_REQUIRED |
| 产物证据 | 文件/消息/记录定位符、版本、哈希、Schema/渲染/引用检查、接收人可用性 | 缺产物或完整性失败：FAIL |
| 效果证据 | 目标环境独立读取、业务终态、回执、对账、监控或受影响主体确认 | 环境未读回：REVIEW_REQUIRED；读回证实未生效/错误：FAIL |

“已发送”“工具返回 success”“界面显示完成”“子 Agent 说 done”都不能单独构成效果证据。

## 4. 检查点、例外与恢复

| 字段 | 内容 |
| --- | --- |
| checkpoint_outcomes | 每个检查点输入、决定者、结论与证据 |
| approvals | 对象、动作、内容版本、范围、有效期、批准者 |
| deviations | 与任务卡不同之处、批准与影响 |
| failures / retries | 全部分布、重复副作用控制与 UNKNOWN |
| stop_actions | 触发后实际停止了什么 |
| rollback | 恢复点、执行证据、残余风险 |
| unresolved | 尚不能证明或互相冲突的事项 |

## 5. 门禁与声明

| 字段 | 内容 |
| --- | --- |
| evaluation_ref | C07 task/trial、rubric、grader 和争议日志引用 |
| result | `PASS` / `FAIL` / `REVIEW_REQUIRED` |
| hard_failures | 安全、权限、隐私、不可逆、证据伪造等不可平均项 |
| bounded_claim | 只在本任务版本、数据、预算、风险和环境内可说什么 |
| prohibited_claim | 不能据此宣称的能力、成熟度、泛化或平台保证 |
| reviewer_signature | 独立复核者、时间、签核对象版本 |

作者、执行 Agent 或训练导师不得自批为 `PASS`。若环境终态读取失败，不能用模型自信或 Artifact 美观度补足。

## 6. 生产反馈候选

| 字段 | 内容 |
| --- | --- |
| feedback_permission | 继承任务卡：DENIED / METADATA_ONLY / DEIDENTIFIED_EXCERPT / APPROVED_FULL |
| candidate_fields | 哪些失败、修正、偏差、成本或效果可候选回流 |
| deidentification | 删除/泛化了哪些身份、凭证、客户与第三方信息 |
| rights_and_approval | 权利人、用途、批准记录、保留期 |
| deduplication | 与已有训练/回归/留出样本的重复检查 |
| contamination_review | 是否泄漏答案、grader、隐藏样本或跨 trial 状态 |
| destination | 只到提案池、训练集、回归集或问题库；不得直写正式 Memory/Skill |
| accepted_by | 有权接收者与后续独立门禁 |

## 7. 机器交接块

```yaml
delivery_evidence_package:
  example: true
  delivery_id: "DEL-C09-EXAMPLE"
  version: "0.1.0"
  task_card_ref: "A-C09-01#TASK-C09-EXAMPLE@0.1.0"
  context_package_ref: "A-C09-02#CTX-C09-EXAMPLE@0.1.0"
  attempt_ids: []
  system_snapshot: {}
  claimed_task_state: "submitted"
  process_evidence: []
  artifact_evidence: []
  effect_evidence: []
  checkpoint_outcomes: []
  deviations: []
  failures: []
  rollback: []
  evaluation_ref: "A-C07-01#task"
  result: "REVIEW_REQUIRED"
  bounded_claim: ""
  prohibited_claims: []
  feedback:
    permission: "DENIED"
    candidate_fields: []
    destination: null
  independent_reviewer: null
  approval: null
```

## 8. 三态验收

- `PASS`：三证闭合，关键检查点与授权可定位，环境终态被独立读取，全部尝试和失败保留，独立 reviewer 对精确版本签核。
- `FAIL`：UI 或 Agent 自述冒充终态；产物缺失/损坏；越权、泄露、重复副作用或伪造证据；挑选最好运行隐藏失败。
- `REVIEW_REQUIRED`：产物可用但环境读回、权利、争议或独立签核仍缺；系统处于安全等待且未扩大影响。

本模板不授予 C27 的 `MAT-L0—MAT-L5` 成熟度，也不推导 C17 的 `AU-L0—AU-L4` 自主等级。

---
artifact_id: A-C09-01
chapter_id: C09
title: "任务卡"
status: drafting
artifact_type: work-contract-template
owner: task-owner
approver: task-owner-and-risk-owner
self_approval_allowed: false
consumed_by: [C13, C19, C20, C23, C25, C26]
---

# A-C09-01　任务卡

## 1. 用途与边界

任务卡把一次真实工作冻结成可执行、可检查、可停止、可交付的工作合同。它承接 C04 的岗位、任务域、能力、风险与负面清单，承接 C07 的评测引用和 C08 的训练目标，但不创造权限，不等于平台 Session，也不等于 A2A Task。任何聊天中临时增加的要求，只有进入新版本任务卡并重新通过授权检查后才生效。

## 2. 身份与版本

| 字段 | 必填内容 |
| --- | --- |
| task_id / version | 唯一 ID、语义版本、创建与生效时间 |
| title / project | 可检索任务名、所属项目与工作区 |
| requester / owner | 请求者、对结果负责的任务所有者 |
| executor / reviewers | 执行者、独立复核者、风险所有者 |
| affected_parties | 会被输出、动作或数据使用影响的主体 |
| role_model_ref | C04 岗位建模卡与任务域引用 |
| risk_refs | C04 风险、负面清单与停止条件引用 |
| evaluation_ref | C07 评测蓝图、rubric 与证据要求引用 |
| training_ref | 若为训练任务，引用 C08 计划和轮次；否则填 `not_applicable` |

## 3. 目标、范围与终态

| 字段 | 内容 | 证据定位符 | 未知/处理人 |
| --- | --- | --- | --- |
| objective | 可观察的工作目标 | | |
| business_outcome | 对服务对象的期望结果 | | |
| in_scope | 明确允许处理的对象、时间和动作 | | |
| out_of_scope | 明确排除项 | | |
| deliverables | 文件、记录、消息草稿或系统变更 | | |
| business_terminal | 业务完成的独立判据 | | |
| environment_terminal | 目标环境的读取式验证条件 | | |
| non_goals | 即使有帮助也不应顺手完成的事项 | | |

## 4. 输入、约束与行动边界

| 类别 | 必填字段 |
| --- | --- |
| 输入 | `input_id`、版本、来源、权利、完整性标识、上下文包引用 |
| 依赖 | 上游状态、提供者、最晚到达时间、缺失时动作 |
| 允许动作 | 读取、分析、草拟、内部写入、请求批准、获批后外发等分开列出 |
| 禁止动作 | 跨主体读取、未批外发、凭证导出、删除、生产变更等 |
| 非功能要求 | 时限、成本、隐私、可追溯、恢复、可访问性 |
| 权限 | 已有真实授权、作用域、有效期；禁止把本卡文字当授权 |
| 预算 | 时间、费用、token、工具调用、人工介入上限 |
| 数据 | 敏感等级、最小披露、保留与删除、允许/禁止用途 |

## 5. 检查点合同

| checkpoint_id | 类型 | 触发条件 | 必交证据 | 决策者 | 允许结论 | 超时安全态 |
| --- | --- | --- | --- | --- | --- | --- |
| CP-READY | 就绪 | 首次行动前 | 目标、输入、权限、上下文新鲜度 | task owner | CONTINUE / ASK / PAUSE / STOP | PAUSE |
| CP-RISK | 风险/批准 | 有副作用、敏感数据或范围变化前 | 对象、动作、内容版本、影响、可逆性 | risk/approval owner | CONTINUE / ASK / STOP | STOP |
| CP-PROGRESS | 进度 | 预算一半、阻塞或假设改变 | 已完成、失败、剩余、证据 | task owner | CONTINUE / PAUSE / HAND_BACK | PAUSE |
| CP-DELIVERY | 交付 | 声明完成前 | 过程、产物、效果三证 | independent reviewer | PASS / FAIL / REVIEW_REQUIRED | REVIEW_REQUIRED |

检查点数量由风险决定，不得为了形式固定为四个。本书合成练习只使用两个强制检查点：`CP-READY` 与 `CP-DELIVERY`。

## 6. 停止、升级、回滚与让位

| 字段 | 内容 |
| --- | --- |
| ask_if | 哪些未知可通过澄清继续 |
| pause_if | 哪些外部依赖可进入安全等待 |
| stop_if | 哪些越权、泄露、不可逆或证据缺失必须终止 |
| hand_back_if | 能力、权限、预算或责任不足时，向任务所有者交回什么 |
| escalation_target | 有权作出哪一类决定的人或角色 |
| minimum_disclosure | 升级时仅披露哪些必要信息 |
| rollback | 撤回候选、恢复上一安全状态、保留哪些证据 |
| residual_risk | 回滚后仍存在的影响与责任人 |

`HAND_BACK` 只是本章的工作决定；跨 Agent 的 routing、让位、handoff ACK 和并发冲突由 C20 定义。

## 7. 交付与数据回流许可

| 字段 | 内容 |
| --- | --- |
| required_evidence | 过程、产物、效果证据及独立读取方式 |
| completion_claim | 谁可以声明“提交”，谁可以判定“完成” |
| feedback_permission | `DENIED` / `METADATA_ONLY` / `DEIDENTIFIED_EXCERPT` / `APPROVED_FULL` |
| permitted_feedback_fields | 明确允许回流的字段，不用“全部日志” |
| prohibited_feedback_fields | 凭证、私聊、群聊无关内容、第三方敏感信息等 |
| retention / deletion | 保留期限、删除触发、删除责任人 |
| rights_owner / approval_ref | 数据权利人与批准记录 |
| contamination_controls | 去重、去标识、留出隔离、答案暴露与来源标注 |

## 8. 机器交接块

```yaml
task_card:
  example: true
  task_id: "TASK-C09-EXAMPLE"
  version: "0.1.0"
  role_model_ref: "A-C04-01#task"
  risk_refs: []
  evaluation_ref: "A-C07-01#task"
  training_ref: "not_applicable"
  owner: "task-owner"
  affected_parties: []
  objective: ""
  business_outcome: ""
  in_scope: []
  out_of_scope: []
  deliverables: []
  business_terminal: []
  environment_terminal: []
  context_package_ref: "A-C09-02#package"
  allowed_actions: []
  prohibited_actions: []
  permissions: []
  checkpoints: []
  stop_if: []
  rollback_ref: ""
  feedback_permission: "DENIED"
  status: "drafting"
  approval: null
```

## 9. 三态验收

- `PASS`：目标、范围、终态、权限、风险、检查点、三证、停止、回滚和回流许可完整；字段指向冻结版本；有权主体批准。
- `FAIL`：把聊天当授权；任务没有终态；敏感或外部动作无硬门；声称完成却缺环境读取；默认回流全部对话。
- `REVIEW_REQUIRED`：关键输入、权利、批准者、终态或恢复条件仍未知；权限已收缩，且补证人与期限明确。

本模板本身始终为 `drafting`；填写完整也不代表任务自动获批。

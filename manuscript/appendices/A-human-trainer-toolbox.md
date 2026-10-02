---
appendix_id: A
title: 人类训练者工作箱
status: formal_candidate
audiences: [manager, trainer, reviewer]
depends_on: [C03, C04, C07, C08, C09, C17, C18, C20, C24, C27]
verified_on: 2026-09-30
---

# 附录 A　人类训练者工作箱

本附录把正文中的方法压缩为一组可以直接复制、评审和归档的工作卡。它不是另一套流程；每张卡都对应正文的唯一主定义。训练者可以删去不适用字段，但不能删去目标、边界、证据、停止、恢复和责任人。

使用时为每个对象分配稳定 ID，保存到项目的版本化工作区。不要把真实凭证、个人隐私或未经授权的客户材料写入模板。

## A.1 岗位建模卡、JTBD 与能力树

### A.1.1 岗位建模卡

```yaml
role_card:
  role_id: ROLE-001
  role_name: "研究 Agent"
  owner: "human-role-owner"
  business_context: "为什么需要这个岗位"
  beneficiaries: []
  jobs_to_be_done:
    - situation: "当……"
      motivation: "我希望……"
      expected_progress: "从……到……"
  task_domain:
    included: []
    excluded: []
  inputs:
    required: []
    optional: []
    forbidden: []
  outputs:
    artifacts: []
    schemas: []
    delivery_channels: []
  completion:
    technical_execution: ""
    delivery_visibility: ""
    business_environment_acceptance: ""
  stakeholders:
    decision_owner: ""
    operator: ""
    reviewer: ""
    risk_owner: ""
  service_window: ""
  cost_budget: {}
  evidence_required: []
  version: ""
  approved_on: YYYY-MM-DD
```

岗位卡的验收问题：任务是否能被观察，产物是否能被保存，完成是否能被外部确认，失败是否能被归责，边界是否能被系统执行。如果答案依赖“Agent 应该明白”，说明岗位仍停留在愿望层。

### A.1.2 能力树

能力树不按“会不会”二分，而要说明行为、条件和证据。

```yaml
capability:
  capability_id: CAP-001
  parent_id: null
  name: "多来源事实核验"
  behavior: "在给定时限内，把关键主张映射到可定位来源"
  conditions:
    task_types: []
    languages: []
    data_classes: []
    tool_and_model_versions: []
  positive_examples: []
  counter_examples: []
  risks: []
  prerequisite_capabilities: []
  evaluation_refs: []
  passing_rule: ""
  owner: ""
```

能力节点应保持正交。若一个节点同时写“会研究、会写作、会发布且很安全”，它无法诊断失败。把能力拆成观察、判断、生成、执行、验证、协作和治理，再用任务把它们组合。

### A.1.3 负面清单

```yaml
negative_capability:
  id: NEG-001
  prohibited_behavior: "在无法确认来源时把推断写成事实"
  trigger_signals: []
  severity: critical | high | medium | low
  immediate_stop: true
  containment: []
  recovery: []
  regression_tests: []
  accountable_owner: ""
```

负面清单不是“不要犯错”的口号，而是上岗硬门。安全、隐私、越权、伪造证据、删除失败和错误认证等关键失败不能被其他高分抵消。

## A.2 风险分级、负面清单和自主等级矩阵

### A.2.1 动作风险卡

| 字段 | 示例 |
| --- | --- |
| action | `publish_external` |
| object | 指定站点的一篇草稿 |
| reversibility | 可下架，但外部传播不可完全回收 |
| data sensitivity | internal |
| blast radius | 单站点、公开受众 |
| financial/legal impact | 可能产生品牌与版权影响 |
| required authority | 内容 owner + 品牌 reviewer |
| required evidence | 预览、来源、审批、发布回执、权威读回 |
| stop | 来源冲突、审批过期、目标不匹配 |
| recovery | 下架、通报、保留记录、纠错与复盘 |

### A.2.2 自主等级矩阵

自主等级对“动作 × 对象 × 范围 × 时窗”授权，不对人格整体授权。

| 等级 | Agent 可以做什么 | 人类必须做什么 | 典型证据 |
| --- | --- | --- | --- |
| AU-L0 观察 | 读取已授权信息，提出观察 | 决定是否采取行动 | 来源与观察日志 |
| AU-L1 建议 | 形成方案、草稿、风险和选择 | 批准具体动作 | 方案、差异、审批 |
| AU-L2 可逆执行 | 在限定工作区执行可回滚动作 | 设定范围并验收 | diff、测试、回滚点 |
| AU-L3 受控外部执行 | 在明确审批和预算内改变外部系统 | 授权、抽查、处理异常 | approval、receipt、readback |
| AU-L4 范围化自主 | 在持续 standing order 内闭环执行 | 定期再授权与问责 | SLO、审计、事件、再认证 |

```yaml
authorization:
  authorization_id: AUTH-001
  actor: agent-id
  action: ""
  object: ""
  scope: ""
  constraints: []
  allowed_tools: []
  data_classes: []
  budget: {}
  not_before: ""
  expires_at: ""
  approver: ""
  approval_digest: ""
  revoke_on: []
  status: ACTIVE | REVOKED | EXPIRED
```

授权通过前检查：批准者是否有 authority，批准对象与实际动作是否相同，参数和 digest 是否绑定，是否过期，是否允许委托，是否有撤销和读回。自然语言“你自己看着办”不构成授权。

## A.3 训练计划、轮次记录和双三角复盘

### A.3.1 训练计划

```yaml
training_plan:
  plan_id: TP-001
  role_id: ROLE-001
  release_identity: "runtime/model/tools/policy fixed refs"
  target_capabilities: []
  negative_capabilities: []
  baseline_evaluation: EVAL-BASE-001
  datasets:
    training: ""
    regression: ""
    holdout: ""
    representative_real_world: ""
  security_red_team: []
  rounds:
    - round_id: R01
      hypothesis: ""
      single_primary_change: ""
      budget: {}
      stop_if: []
      rollback_to: ""
      acceptance: ""
  owners:
    trainer: ""
    task_owner: ""
    evaluator: ""
    risk_owner: ""
  graduation_target: ""
```

每轮只保留一个主要变化假设。模型、prompt、工具、记忆、数据和权限同时改变时，即使结果变好也无法归因。

### A.3.2 轮次记录

```yaml
training_round:
  round_id: R01
  started_at: ""
  ended_at: ""
  hypothesis: ""
  before_release: ""
  after_release: ""
  changes: []
  trial_distribution:
    PASS: 0
    FAIL: 0
    REVIEW_REQUIRED: 0
  costs:
    model: 0
    tools: 0
    compute: 0
    human_minutes: 0
    elapsed_minutes: 0
  failures_preserved: []
  holdout_result: ""
  security_result: ""
  decision: keep | revise | rollback | stop
  evidence_refs: []
  reviewer: ""
```

### A.3.3 双三角复盘表

第一个三角检查任务质量：目标、产物、证据。第二个三角检查训练质量：变化、反馈、迁移。六个角缺一不可。

| 角 | 复盘问题 | 证据 |
| --- | --- | --- |
| 目标 | 实际解决了什么，是否改变了目标 | 任务卡、变更记录 |
| 产物 | 产物可否被下游直接使用 | 文件、schema、交付回执 |
| 证据 | 三个完成面是否成立 | 日志、readback、业务验收 |
| 变化 | 哪个训练干预真正发生 | diff、release identity |
| 反馈 | 裁判是否稳定、是否保留异议 | grader 输出、校准记录 |
| 迁移 | 未见任务、约束变化、跨平台是否保留 | holdout、迁移矩阵 |

复盘输出不是感想，而是 `keep / revise / rollback / stop` 决定、负责人、时限和下轮评测。

## A.4 任务卡、验收卡、整改单和 Handoff 卡

### A.4.1 任务卡

```yaml
task_card:
  task_id: TASK-001
  goal: ""
  why_now: ""
  owner: ""
  inputs: []
  assumptions: []
  constraints: []
  allowed_actions: []
  prohibited_actions: []
  deliverables: []
  evidence_required: []
  budget: {}
  stop_if: []
  escalate_if: []
  done_when:
    technical_execution: ""
    delivery_visibility: ""
    business_environment_acceptance: ""
```

### A.4.2 验收卡

```yaml
acceptance_card:
  acceptance_id: ACC-001
  task_id: TASK-001
  candidate_release: ""
  checks:
    - check_id: AC-01
      object: ""
      threshold: ""
      evidence_ref: ""
      grader: rule | model | human | expert
      result: PASS | FAIL | REVIEW_REQUIRED
  hard_gates: []
  dissent: []
  final_decision: PASS | FAIL | REVIEW_REQUIRED
  decision_owner: ""
  decided_at: ""
```

### A.4.3 整改单

```yaml
remediation:
  remediation_id: REM-001
  finding_id: ""
  severity: P0 | P1 | P2 | P3
  observed_failure: ""
  root_cause: known | suspected | unknown
  containment: []
  proposed_change: []
  owner: ""
  due_at: ""
  regression_tests: []
  rollback: []
  closure_evidence: []
  independent_reviewer: ""
  status: OPEN | FIXED_AWAITING_REVIEW | CLOSED | ACCEPTED_RISK
```

作者不能自行关闭 P0；“代码已改”不是关闭证据，必须有原失败复现、回归、近邻反例和非作者裁决。

### A.4.4 Handoff 卡

```yaml
handoff:
  handoff_id: HO-001
  from: ""
  to: ""
  task_id: ""
  current_state: PLANNED | RUNNING | WAITING | BLOCKED | FAILED | COMPLETED | CANCELED
  objective: ""
  completed: []
  remaining: []
  artifacts: []
  evidence_refs: []
  decisions: []
  unknowns: []
  risks: []
  permissions_and_expiry: []
  next_action: ""
  stop_conditions: []
  sender_ack: ""
  receiver_ack: ""
```

双 ACK 分别证明“发送者提交了什么”和“接收者理解并接管了什么”。没有 receiver ACK 的交接仍在传输态，不能假设责任已经转移。

## A.5 周体检、晋级、降级与退役

### A.5.1 周体检

```yaml
weekly_health_review:
  review_id: WHR-001
  period: ""
  release_identity: ""
  workload_distribution: {}
  outcome_distribution: {PASS: 0, FAIL: 0, REVIEW_REQUIRED: 0}
  d21_incomplete: []
  drift:
    capability: []
    personality: []
    document: []
    tool: []
    goal: []
    memory_context_cross_cutting: []
  security_incidents: []
  cost_and_latency: {}
  human_interventions: []
  stale_permissions: []
  stale_memory: []
  proposed_actions: []
  decision_owner: ""
```

### A.5.2 晋级审查

晋级只批准某个任务与风险范围。最低证据包括：固定 release、足量 trial 分布、回归与留出、安全横切、成本、故障恢复、评审独立性和未关闭限制。任何关键安全失败、证据污染、权限不明或外部终态未知都阻断晋级。

```yaml
level_review:
  review_id: LR-001
  subject: ""
  requested_mat: MAT-L0 | MAT-L1 | MAT-L2 | MAT-L3 | MAT-L4 | MAT-L5
  requested_au: AU-L0 | AU-L1 | AU-L2 | AU-L3 | AU-L4
  scope: ""
  prerequisites: []
  seven_dimensions: {}
  hard_gates: []
  evidence_refs: []
  limitations: []
  expires_at: ""
  decision: PASS | FAIL | REVIEW_REQUIRED
```

MAT 不生成具体授权，AU 不证明成熟度，训练营毕业也不等于获得生产权限。三个结论必须分别记录。

### A.5.3 降级和暂停

发生重大漂移、P0/P1 事故、评测污染、持续 SLO 燃尽、所有者缺失、版本变更未复核或关键证据过期时，应缩小 scope、降低 AU、暂停自动化或撤销授权。降级要保留旧证书与历史记录，不通过重写过去掩盖失败。

### A.5.4 退役清单

- 停止新任务接入，清空或转移在途任务；
- 禁用 schedules、webhooks、workers、delegations 和 standing orders；
- 撤销或轮换 credentials、sessions、tokens 和外部授权；
- 确认替代者、Handoff 与业务连续性；
- 按政策删除或保留记忆、日志、缓存、索引、备份和导出物；
- 验证恢复路径不会让退役对象重新获得权限；
- 执行残余扫描，确认网络、节点、插件、云任务和影子副本；
- 由业务、技术、安全、数据责任人完成终态签字；
- 保留不可篡改的退役决定、证据、限制和时间线。

## A.6 一页使用顺序

```text
岗位卡 → 能力树与负面清单 → 风险与自主等级
  → 基线评测 → 训练计划与轮次 → 任务卡
  → 验收卡 → 整改单 / Handoff
  → 周体检 → 晋级、降级、暂停或退役
```

任何一步发现证据、权限或责任不清，都回到上一个可验证节点。工作箱的目的不是增加表格，而是把“大家以为已经说清楚”变成可以检查、拒绝、交接和改进的共同事实。

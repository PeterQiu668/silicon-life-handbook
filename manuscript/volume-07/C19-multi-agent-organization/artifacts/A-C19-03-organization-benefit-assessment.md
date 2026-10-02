---
artifact_id: A-C19-03
chapter_id: C19
title: "组织收益评估"
status: drafting
approval_status: unapproved
owner: "business-and-evaluation-owner"
consumed_by: [C20, C23, C26, C27]
---

# A-C19-03 组织收益评估

> 多 Agent 必须与单体或确定性 Workflow 在同任务、同输入、同工具权限、同预算边界下比较。不同量纲保留为向量，不压成可掩盖安全失败的神秘总分。

## 比较合同

~~~yaml
example: true
organization_benefit_assessment:
  assessment_id: "BENEFIT-CASE-C-001"
  topology_ref: "A-C19-01#TOPO-CASE-C-001@0.1.0"
  role_matrix_ref: "A-C19-02@0.1.0"
  candidate_pattern: "pipeline-with-independent-review"
  baselines: ["single-agent", "deterministic-workflow"]
  invariants:
    task: "same"
    input_snapshot: "same"
    tool_permissions: "same"
    total_budget_boundary: "same"
    risk_boundary: "same"
    acceptance: "same"
  metrics:
    quality: {single: null, multi: null}
    hard_safety_failures: {single: null, multi: null}
    end_to_end_latency_ms: {single: null, multi: null}
    total_cost_units: {single: null, multi: null}
    human_minutes: {single: null, multi: null}
    communication_units: {single: 0, multi: null}
    duplicate_work_ratio: {single: null, multi: null}
    conflicts: {single: null, multi: null}
    recovery_minutes: {single: null, multi: null}
    evidence_completeness: {single: null, multi: null}
  failures: []
  decision: "REVIEW_REQUIRED"
  disposition: "keep-baseline"
  bounded_claim: ""
  prohibited_claims: ["more agents are always stronger", "consensus proves fact"]
  evidence_layers:
    training: null
    regression: null
    holdout: null
    representative_real_world: null
  representative_real_world_evidence_count: 0
  independent_reviewer: null
  approval: null
~~~

## 决策顺序

1. 先检查任务、输入、工具权限、风险与总预算边界是否可比；不可比则 `REVIEW_REQUIRED`，不得直接宣称领先。
2. 任一未授权动作、敏感泄露、重复副作用、撤销失效或不可恢复破坏，组织候选直接 `FAIL`，不进入均分。
3. 比较 C03 七维剖面及 C09 三证；同时报告墙钟、总成本、人工分钟、通信税、重复、冲突与恢复。
4. 只有至少一个预注册业务目标改善，其他代价在批准预算内，且硬门全部通过，才可 `PASS`。
5. 无净收益、代价越界或更简单方案等效时，明确选择合并角色、降级单体或改为 Workflow。

## 组织处置

| 结论 | 典型证据 | 处置 |
|---|---|---|
| 拆分 | 独立工作面明显改善质量或关键路径，协作税可控 | 进入 C20 设计路由与交接 |
| 保持最小组织 | 有专业/复核收益，但继续加角色无增益 | 冻结角色上限与预算 |
| 合并 | 角色高度重复、交接多于有效工作 | 合并工作面并重跑对照 |
| 降级单体 | 单体质量与安全相当，成本/延迟/恢复更优 | 保留单体与硬门 |
| 改为 Workflow | 决策可确定化且步骤稳定 | 用确定状态机替代自由协商 |
| REVIEW_REQUIRED | 终态、权限、预算或对照缺证 | 保持当前基线，不发布候选 |

## 三态验收

- `PASS`：同合同多次运行、全失败分布、非补偿硬门、净收益向量、独立复核和明确组织处置齐全。
- `FAIL`：只比最好一次；预算不等仍宣称更强；用总平均掩盖越权；因 Agent 数量、文件数或消息数宣称成熟。
- `REVIEW_REQUIRED`：样本、环境终态、真实成本、恢复或独立复核不足。`representative_real_world_evidence_count: 0` 时，合成 PASS 不得外推生产。

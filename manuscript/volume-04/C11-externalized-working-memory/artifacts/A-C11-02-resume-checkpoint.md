---
artifact_id: A-C11-02
chapter_id: C11
title: "恢复检查点"
status: template
---

# A-C11-02　恢复检查点

```yaml
checkpoint:
  task_id: ""
  task_version: ""
  plan_version: ""
  created_at: ""
  created_by: ""
  authorization_refs: []
  last_safe_state: ""
  completed_nodes: []
  inflight_actions: []
  external_state_observations: []
  workspace_revision: ""
  uncommitted_changes: []
  health_checks: []
  next_safe_action: ""
  stop_conditions: []
  residual_risks: []
  consistency: "CONSISTENT|INCONSISTENT|REVIEW_REQUIRED"
```

恢复前重新鉴权、刷新高波动外部状态、核对飞行动作；任何差异先触发重规划。


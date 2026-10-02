---
artifact_id: A-C10-02
chapter_id: C10
title: "滚动计划与重规划记录"
status: template
---

# A-C10-02　滚动计划与重规划记录

```yaml
plan:
  task_id: ""
  plan_version: "0.1.0"
  terminal_states: []
  active_window:
    ready: []
    running: []
    waiting: []
    blocked: []
  critical_path: []
  next_actions: []
  budget_used: {time: 0, cost: 0, tokens: 0, human_minutes: 0}
  trigger_thresholds: {budget_review: 0.5, scope_decision: 0.8, stop: 1.0}
replan_log:
  - event_id: ""
    observed_at: ""
    evidence_ref: ""
    trigger_type: "assumption_falsified"
    nodes_changed: []
    cancelled_actions: []
    authorization_impact: "none"
    approved_by: ""
```

每次重规划保存旧版本；目标、对象、数据用途、外发内容或不可逆影响变化时，返回任务卡与授权门。


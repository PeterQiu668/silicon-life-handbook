---
artifact_id: A-C12-02
chapter_id: C12
title: "回退与死胡同记录"
status: template
---

# A-C12-02　回退与死胡同记录

```yaml
route:
  goal: ""
  attempts: []
  new_information_per_attempt: []
  falsified_assumptions: []
  dead_end_trigger: ""
rollback:
  checkpoint_ref: ""
  state_planes: [files, config, database, queue, messages, credentials, memory, external_services]
  stop_new_actions: true
  recovery_steps: []
  compensation_steps: []
  independent_readback: []
  residual_risks: []
  verdict: "PASS|FAIL|REVIEW_REQUIRED"
```


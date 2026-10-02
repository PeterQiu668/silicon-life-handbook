---
artifact_id: A-C18-03
chapter_id: C18
title: "影子测试与回滚计划"
status: drafting
approval_status: unapproved
---
# A-C18-03 影子测试与回滚计划

~~~yaml
example: true
shadow_rollback_plan:
  plan_id: "PLAN-C18-001"
  baseline_bundle: ["model", "prompt", "contracts", "memory", "skill", "plugin", "tool-schema", "provider", "eval", "authorization", "runtime"]
  candidate_bundle_hash: "CANDIDATE-HASH"
  exact_diff_ref: "fixture://diff/plan-001"
  stages:
    - {name: "offline", writes: "synthetic-only", gate: "PASS"}
    - {name: "shadow", writes: "none", gate: "PASS"}
    - {name: "canary", writes: "separately-authorized", gate: "REVIEW_REQUIRED"}
  controls: {same_task: true, same_budget: true, same_risk: true, same_authority: true, same_environment: true}
  hard_gates: ["no unauthorized effects", "no sensitive leakage", "holdout not worse", "rollback proven"]
  stop_if: ["security fail", "unknown external effect", "cost or latency budget exceeded", "grader disagreement unresolved"]
  rollback:
    target_bundle_ref: "BASELINE-C18-V1"
    includes: ["queue", "cache", "session", "index", "tool", "policy references"]
    preserve_revocation: true
    negative_access_test: "required"
  possible_decisions: ["solidify", "limit_scope", "continue_observing", "reject", "rollback"]
  production_approval: null
~~~

Shadow 只能观察，不得产生真实副作用；canary/灰度需要独立授权和控制组。回滚对象是相容 version bundle，不是单个文件，且不得复活已撤销权限、删除同意或旧目标。回滚后重跑 regression、holdout、security slice 和负向访问。

PASS：exact diff、隔离、停止、UNKNOWN、回滚和替代闭合；FAIL：影子写生产、失败被隐藏、回滚复活授权；REVIEW_REQUIRED：真实 queue/cache/session/index 或外部终态未核验。

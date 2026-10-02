---
artifact_id: A-C18-02
chapter_id: C18
title: "改进提案"
status: drafting
approval_status: unapproved
---
# A-C18-02 改进提案

~~~yaml
example: true
improvement_proposal:
  proposal_id: "PROP-C18-001"
  drift_event_refs: ["DRIFT-CASE-B-001"]
  observed_failure_cluster: "draft flag became send by default"
  falsifiable_hypothesis: "tool schema/default drift caused unsafe behavior"
  alternative_explanations: ["fixture corruption", "grader change"]
  invariants: ["task", "budget", "risk", "authority", "environment"]
  single_primary_intervention: "pin tool schema v1 and add contract assertion"
  baseline_bundle_hash: "BASE-HASH"
  candidate_bundle_hash: "CANDIDATE-HASH"
  exact_diff_ref: "fixture://diff/prop-001"
  affects: ["tool", "capability"]
  must_not_change: ["goal", "grader", "security policy", "permissions", "AU radius"]
  data_layers: ["training", "regression", "holdout", "representative real-world"]
  security_red_team: "cross-cutting non-compensatory slice"
  contamination_check: "PASS"
  proposer: "agent-candidate-author"
  evaluator: "independent-reviewer"
  approver: "human-change-owner"
  accountable_owner: "business-owner"
  status: "proposed"
  invalidation_conditions: ["holdout regression", "security hard fail", "cost budget exceeded"]
  expires_at: "2026-10-07T00:00:00+08:00"
~~~

失败只能形成可反证候选。提案必须有替代解释、单一主干预、不变项、精确 diff、污染检查、停止和失效条件。提案者、评测者、批准者和责任 owner 分离；批准试验不等于批准生产。任何修改目标、安全规则、grader、权限、自主半径或生产资产的请求都返回外部批准与 C17 再认证。

PASS：候选与基线不可变分离、失败分布保留、边界不扩大；FAIL：多变量“全优化”、自改 grader/权限/目标、删除失败；REVIEW_REQUIRED：因果混杂或 holdout/授权不足。

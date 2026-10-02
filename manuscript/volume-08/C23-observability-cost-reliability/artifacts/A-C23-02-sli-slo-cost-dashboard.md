---
artifact_id: A-C23-02
chapter_id: C23
title: "SLI/SLO与成本看板"
status: drafting
approval_status: unapproved
owner: service-and-economics-owner
consumed_by: [C24, C25, C27]
---

# A-C23-02 SLI/SLO与成本看板

## SLI合同

每行必填：`service_promise / eligible_population / good_event / bad_event / measurement_point / window / target / sample_count / excluded / unknown / owner / burn_rule / action_on_breach / drilldown_refs`。没有分母、测量点、窗口、owner和越线动作的“99%”无效。

核心视图至少包含：D21三层接受率、交付完整率、端到端延迟p50/p95/p99、UNKNOWN与取消率、重复副作用率、queue age/depth、恢复MTTD/止损/RTO/RPO/对账时间、授权正确性、观测丢弃率、每接受任务全成本和失败浪费率。安全硬失败单列，不能进入普通错误预算。

## 错误预算决策

```yaml
error_budget:
  example: true
  sli_ref: "sli://accepted-task-rate"
  window: "rolling-28d"
  objective: 0.99
  eligible_events: 1000
  bad_events: 8
  budget_total: 10
  budget_remaining: 2
  short_window_burn: 3.0
  long_window_burn: 1.1
  owner: "service-owner"
  breach_actions:
    - "冻结扩大自主性、流量和非修复变更"
    - "收紧降级与人工验收"
    - "启动RCA、恢复和回归"
  non_compensable_exclusions:
    - "未授权effect"
    - "跨租户泄露"
    - "资金或删除错误"
    - "关键证据伪造"
```

## 全成本信封

```yaml
task_cost:
  example: true
  task_id: "task-example"
  attempt_count: 1
  accepted: false
  model:
    input_tokens: 0
    output_tokens: 0
    reasoning_tokens: 0
    cache_read_tokens: 0
    cache_write_tokens: 0
    estimated_usd: 0
    actual_usd: null
    pricing_version: "price-example"
  tools_api_usd: 0
  compute_storage_network_usd: 0
  human_review_minutes: 0
  human_review_usd: 0
  retry_waste_usd: 0
  remediation_usd: 0
  elapsed_seconds: 0
  queue_seconds: 0
  opportunity_cost_method: "omitted-with-reason"
  total_observed_usd: 0
  confidence: "MEASURED|ESTIMATED|PARTIAL|UNKNOWN"
```

必须并列报告`cost_per_attempt`、`cost_per_accepted_task`、`failure_waste_ratio`、`human_minutes_per_accepted_task`。估算价与账单分栏；币种、税费、折扣、定价版本和时间窗可追溯。任何缺失成本使“总成本”降级为PARTIAL。

## 容量与尾部

看板同时展示arrival/admission/service rate、queue depth/age、active/max concurrency、tenant share、provider/tool saturation、retry rate、acceptance、p50/p95/p99/max与样本量。均值改善但p99、重复effect、人工返工或安全失败恶化，不得声明可靠性提升。

## 下钻与访问

所有聚合可下钻到task、attempt、artifact、receipt、environment readback与incident引用；高基数ID不进入metric label。看板展示采样率、schema/adapter版本、dropped counter和不可比时间窗，不能把“零记录”解释为“零故障”。

## 三态验收

- `PASS`：承诺、分母、阈值、样本、尾部、UNKNOWN、成本与越线动作齐全，且可下钻。
- `FAIL`：HTTP成功率冒充任务成功；隐藏失败尾部；漏人工/失败成本；安全硬失败由预算或平均值抵消。
- `REVIEW_REQUIRED`：数据缺口、价格口径、目标readback、代表性或owner未知，已停止不受支持的结论。

---
artifact_id: A-C18-01
chapter_id: C18
title: "漂移体检表"
status: drafting
approval_status: unapproved
---
# A-C18-01 漂移体检表

> 漂移是相对已批准基线的可观察偏移，不等于变差。一级分类仅为 capability/persona/document/tool/goal；memory/context 只能作为跨类型状态与证据源。

~~~yaml
example: true
drift_event:
  event_id: "DRIFT-CASE-B-001"
  status: "suspected"
  primary_type: "tool"
  secondary_types: ["capability"]
  baseline_bundle_ref: "BASELINE-C18-V1"
  observed_bundle_ref: "BUNDLE-C18-CANDIDATE-1"
  comparison_contract_ref: "EVAL-C18-V1"
  controlled_conditions: {task: "same", budget: "same", risk: "same", authority: "same", environment: "same"}
  signals: ["mock-send draft default changed"]
  repeated_trials: ["TRIAL-001", "TRIAL-002"]
  confounders_checked: ["grader-version", "provider", "input-distribution", "runtime"]
  memory_context_role: "possible propagation source, not drift type"
  hard_gate: "FAIL"
  owner: "human-drift-owner"
  evidence_refs: ["fixture://schema-diff", "fixture://contract-test"]
  next_action: "isolate-tool-and-propose-candidate"
~~~

## 五类检查

| 类型 | 基线对象 | 信号 | 常见混杂 | 默认处置 |
|---|---|---|---|---|
| capability | 同任务完整运行 | 质量、失败、成本、延迟、方差 | 难度、Provider、grader、数据 | 重复对照后提出干预 |
| persona | 已批身份/价值/关系契约 | 拒绝消失、讨好越界、服务对象错位 | 合法语气适配、单次措辞 | 核对契约/上下文/记忆/模型 |
| document | 权威文档与加载快照 | 冲突、过期、加载旧版 | 排版、批准升级、备注 | 冻结冲突源并修复引用 |
| tool | Tool/Skill/Plugin/API/Provider合同 | schema、权限、宿主、结果语义变更 | 任务或纯文档变化 | 停副作用、合约测试、再认证 |
| goal | 上位目标、成功/禁止标准 | 奖励代理、优先级、服务对象变化 | 合法战略调整 | 暂停固化，回目标 owner |

体检还必须保存版本 bundle、失败分布、UNKNOWN、误报/漏报、人工复核量与治理成本。变化信号最高只能进入 suspected；确认漂移需要可校正比较，因果证明还需单一主干预或回滚复现。

PASS：五类和传播链可定位、混杂有证据、同合同重复；FAIL：无基线定漂移、安全失败被平均、记忆被造为第六类；REVIEW_REQUIRED：样本、版本、grader或环境不足。

---
artifact_id: A-C19-01
chapter_id: C19
title: "任务拓扑图"
status: drafting
approval_status: unapproved
owner: "task-owner"
consumed_by: [C20, C21, C26]
---

# A-C19-01 任务拓扑图

> 先画任务，再决定是否组队。任务拓扑不是角色名单或装饰性流程图，而是可验收节点、依赖、共享状态、关键路径、可并行集合、合并点、权限与恢复关系的可执行说明。

## 任务与对照基线

| 字段 | 必填内容 |
|---|---|
| topology_id / version | 唯一 ID、不可变版本、所有者 |
| task_card_ref / context_ref | C09 精确任务卡与上下文包 |
| goal / business outcome | 目标及业务终态，不以“所有 Agent 完成”为终态 |
| single_agent_baseline | 单体的任务、输入、工具权限、预算、验收与运行证据 |
| workflow_baseline | 可确定化步骤及不用 Agent 的原因；不适用也要说明 |
| stop / downgrade | 何时停止拆分、合并角色或退回单体/Workflow |

## 节点与五类边

~~~yaml
example: true
task_topology:
  topology_id: "TOPO-CASE-C-001"
  version: "0.1.0"
  task_card_ref: "A-C09-01#TASK-CASE-C-001@1"
  goal: "生成有来源、可审查、可回滚的合成交付包"
  terminal_conditions: ["artifact-accepted", "environment-readback-known"]
  single_agent_baseline_ref: "RUNSET-C19-SINGLE-01"
  workflow_baseline_ref: "WORKFLOW-CHECK-C19-01"
  nodes:
    - node_id: "N-RESEARCH"
      input_refs: ["CTX-C09-CASE-C@1"]
      required_capabilities: ["source-verification"]
      required_permissions: ["public-read"]
      output_artifact: "source-ledger"
      acceptance_ref: "EVAL-SOURCE-LEDGER"
      side_effect: "none"
      state_owner: "role-research"
      accountable_owner: "human-project-owner"
      failure_isolation: "local"
    - node_id: "N-SYNTHESIS"
      input_refs: ["source-ledger"]
      required_capabilities: ["structured-synthesis"]
      required_permissions: ["workspace-draft-write"]
      output_artifact: "delivery-draft"
      acceptance_ref: "EVAL-DELIVERY-DRAFT"
      side_effect: "reversible-local-write"
      state_owner: "role-lead"
      accountable_owner: "human-project-owner"
      failure_isolation: "local"
  edges:
    - {from: "N-RESEARCH", to: "N-SYNTHESIS", type: "data", condition: "accepted-artifact"}
  shared_state:
    mutable_objects: ["delivery-draft"]
    ownership: {"delivery-draft": "single-writer:role-lead"}
    version_control: "optimistic-version-check"
  parallel_sets: []
  join_points: ["N-SYNTHESIS"]
  critical_path: ["N-RESEARCH", "N-SYNTHESIS"]
  human_gates: ["publish-decision"]
  recovery_relations: [{failed: "N-SYNTHESIS", action: "restore-draft-base", owner: "human-project-owner"}]
  organization_candidate: "pipeline-with-independent-review"
  approval: null
~~~

五类边必须明确区分：数据依赖、决策依赖、资源冲突、证据依赖、恢复依赖。边只说明组织需要；ACK、重试、取消、Handoff 和合并协议由 C20 定义，A2A 对象和跨系统信任由 C21 定义。

## 拆分检查

| 检查 | PASS 证据 | 失败处置 |
|---|---|---|
| 节点独立验收 | 每节点有输入、产物、终态和 acceptance ref | 不能验收则合并回上层任务 |
| 并行真实性 | 无数据前置，且共享写与权限可隔离 | 关键路径强串行则保留单体/Workflow |
| 状态所有权 | 每个可变对象有单一写者或版本策略 | 多写者无控制即 FAIL |
| 权限可衰减 | 子节点权限是父授权与最小需求的交集 | 共享父凭证或扩权即 FAIL |
| 恢复可定位 | 节点故障有停止、接管、重做或回滚 owner | 失败会无声传播则不拆 |

## 三态验收

- `PASS`：节点可验收、边与共享状态完整、单体/Workflow 基线存在、权限与恢复闭合，拆分理由可被证据反驳。
- `FAIL`：从角色故事倒推任务；不可分解仍并行；共享写无 owner；把任务完成等同所有子 Agent 自报完成。
- `REVIEW_REQUIRED`：任务终态、依赖、权限、预算或恢复责任未冻结。此时不得据此创建生产组织。

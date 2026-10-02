---
artifact_id: A-C04-02
chapter_id: C04
title: "能力树（含非功能要求）"
status: drafting
artifact_type: capability-template
owner: trainer
approver: role-owner-and-independent-reviewer
self_approval_allowed: false
consumed_by: [C07, C08, C14, C19, C25]
---

# A-C04-02　能力树（含非功能要求）

## 1. 使用规则

本树从 A-C04-01 的真实任务与失败生成，不从模型功能、工具市场或人格形容词生成。五支是知识、推理、执行、协作、反思；它们描述岗位需要的行为，不重定义 C03 七维，也不形成十二项总分。

叶节点必须能生成训练目标、测试候选和外部证据。无法按“条件—对象—行为—结果—边界—反证”填写的节点，退回继续拆解。

## 2. 节点定义卡

| 字段 | 待填写 |
| --- | --- |
| capability_id / parent_id | |
| branch（knowledge/reasoning/execution/collaboration/reflection） | |
| 来源 task_id / failure_id | |
| 条件与变式 | |
| 对象 | |
| 可观察行为 | |
| 结果/产物 | |
| 过程、产物、效果证据 | |
| 权限与风险边界 | |
| 反例/负面证据 | |
| 依赖能力 | |
| 工具需求（不是指定产品） | |
| 测试候选 ID | |
| 更新/复核触发器 | |

## 3. 五支能力树

### 3.1 知识 Knowledge

| capability_id | 任务依据 | 可观察行为 | 知识来源/所有者/时效 | 反例 | 测试候选 |
| --- | --- | --- | --- | --- | --- |
| K-01 | | | | | |
| K-02 | | | | | |

### 3.2 推理 Reasoning

| capability_id | 任务依据 | 输入情境 | 可观察判断 | 不确定性/升级 | 反例 | 测试候选 |
| --- | --- | --- | --- | --- | --- | --- |
| R-01 | | | | | | |
| R-02 | | | | | | |

### 3.3 执行 Execution

| capability_id | 任务依据 | 状态变化 | 前置检查 | 允许动作/最小权限 | 终态确认 | 异常/恢复 | 测试候选 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E-01 | | | | | | | |
| E-02 | | | | | | | |

### 3.4 协作 Collaboration

| capability_id | 协作对象 | 触发 | 共享状态/产物 | 澄清/求助/让位/交接行为 | 完成信号 | 反例 | 测试候选 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-01 | | | | | | | |
| C-02 | | | | | | | |

### 3.5 反思 Reflection

| capability_id | 失败/反馈来源 | 诊断行为 | 改进提案 | 回归与回滚 | 不允许自行改变 | 测试候选 |
| --- | --- | --- | --- | --- | --- | --- |
| F-01 | | | | | 目标、权限、禁区、毕业状态 | |
| F-02 | | | | | 目标、权限、禁区、毕业状态 | |

## 4. 非功能要求

不要写“快、便宜、稳定、透明、可恢复”。每项需给对象、阈值候选、测量点、不可牺牲边界、责任人和异常处置；阈值由 C07/C23 进一步冻结。

| nfr_id | 类别 | 适用 task/capability | 阈值候选 | 测量点/证据 | 不可牺牲边界 | 权衡 | owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NFR-SPEED-01 | speed | | | | | | |
| NFR-COST-01 | cost | | | | | | |
| NFR-STABILITY-01 | stability | | | | | | |
| NFR-TRANSPARENCY-01 | transparency | | | | | | |
| NFR-RECOVERY-01 | recoverability | | | | | | |

## 5. 能力到 C03 观察接口

本表只引用 C03 七维，不改写定义或打分。

| capability_id | 可能关联的 C03 维度 | 需要的过程证据 | 产物证据 | 效果证据 | 硬门禁/未知 |
| --- | --- | --- | --- | --- | --- |
| | quality/generalization/safety/stability/efficiency/collaboration/governability | | | | |

一个节点可以关联多个维度；不得把关联数当得分。安全硬失败先于平均表现。

## 6. 岗位—能力—风险—派生接口双向追踪

本表是三件必交产物之间的关系接口，不是第四件章节产物。正向读取检查岗位需求是否有训练、测试、工具与门禁出口；反向读取检查每个实现或门禁是否有业务授权。关系不适用时填 `N/A + 理由`，缺证据时填 `UNKNOWN + 责任人`，不得留空后宣布通过。

| trace_id | jtbd_id | task_id | capability_id | nfr_ids | risk_ids | negative_ids | baseline_gap | training_objective_id | test_candidate_ids | tool_requirement_id | gate_candidate_id | 正向/反向状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TRACE-01 | | | | | | | | | | | | `PASS/FAIL/REVIEW_REQUIRED` |

工具需求至少写：所需状态变化、输入输出、最小权限、失败语义、观察证据、模拟/回滚和替代方案。工具不存在时收缩范围；工具存在时也不得自动纳入岗位。

## 7. CASE-A/B/C 参考枝干（示例，不是成品答案）

| 分支 | CASE-A 澄明 | CASE-B 潮生 | CASE-C 北辰 |
| --- | --- | --- | --- |
| 知识 | 来源性质、日期、行业概念 | 客户、产品、价格、同意与隐私 | 交付标准、依赖、角色接口 |
| 推理 | 冲突证据与不确定性 | 信号价值与动作分级 | 可分解性、关键路径与让位 |
| 执行 | 定位、核验、证据卡 | 客户隔离、草拟、批准后执行 | 分派、版本、合并、独立验收 |
| 协作 | 向决策者说明未知 | 向授权者呈现可决策摘要 | 完整交接、责任唯一、反馈闭环 |
| 反思 | 失败来源入测试候选 | 噪音/遗漏/越权分类 | 重复劳动、冲突和恢复复盘 |

## 8. 机器交接块

```yaml
capability_tree:
  example: true
  role_id: "ROLE-EXAMPLE"
  version: "0.1.0"
  branches:
    knowledge: []
    reasoning: []
    execution: []
    collaboration: []
    reflection: []
  nfr_ids: []
  training_objective_ids: []
  test_candidate_ids: []
  tool_requirements: []
  gate_candidate_ids: []
  trace_links: []
  unresolved_nodes: []
  status: "drafting"
  approval: null
```

## 9. 三态验收与回滚

- `PASS`：关键任务均有能力覆盖；五支无明显空洞；所有叶节点可观察、可追踪、可生成测试；五类 NFR 均有测量位置或明确 N/A 理由；独立评审可复核。
- `FAIL`：能力等同模型/工具/人格；节点不可生成测试；权限或安全行为缺失；用平均分掩盖硬失败。
- `REVIEW_REQUIRED`：领域专家对节点边界、NFR 或证据有实质分歧，且已记录补证计划。

停止条件：无任务依据、无反例、无可观察证据或需要未授权工具。回滚：移除无依据节点，恢复上一批准版本，撤回由该节点派生的训练、测试和工具变更。

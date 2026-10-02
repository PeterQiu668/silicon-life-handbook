---
artifact_id: A-C08-01
chapter_id: C08
title: "训练计划"
status: drafting
artifact_type: training-plan
owner: training-coordinator
approver: human-role-owner-and-risk-owner
self_approval_allowed: false
consumed_by: [C09, C18, C25, C26, C27]
---

# A-C08-01　训练计划

## 1. 用途与红线

本计划把一个经复现的能力差距转成可执行、可停止、可回滚的训练实验。它不授予生产权限，不替代 C07 评测蓝图，不是 C27 认证，也不能由导师或学员自批。

禁止：把反馈直接写进 Memory/Skill；同时换模型、prompt 与工具却宣称单项归因；向导师暴露隐藏留出答案；用训练集提分宣布能力形成；用 `MAT-L0—MAT-L5` 推导权限，或用 `AU-L0—AU-L4` 推导能力强弱。

## 2. 训练计划主表

| 字段 | 必填内容 |
| --- | --- |
| experiment_id / version | 唯一 ID、版本、创建时间、owner |
| role_model_ref | C04 岗位、JTBD、任务、能力、NFR、风险与负面清单 |
| contract_refs | C05 契约版本与不可变更边界 |
| evaluation_spec_ref | C07 评测规格、baseline、数据集、grader、硬门与争议流程 |
| capability_objective | 一个可观察能力目标，不写人格形容词 |
| failure_cluster | 一类可重放失败、样本与影响 |
| root_cause_hypothesis | 候选根因、替代解释、反证任务、信心 |
| primary_intervention | 一个主变更对象与精确 diff |
| held_constant | 模型、Provider、Runtime、数据、预算、权限、风险、grader 等不变量 |
| interaction_risks | 单变量假设可能漏掉的交互；何时升级 staged/factorial |
| datasets | training/regression/holdout/real_world 四层的版本、权利与访问角色；security/red-team 只作横切切片并绑定 canonical layer 与 scenario |
| role_separation | owner/coordinator/teacher/learner/reviewer/expert/risk gate 的权限 |
| round_sequence | 示范、模仿、独立、变式、干扰、压力的选用与顺序 |
| gates | 训练结果、回归、留出、迁移、安全、成本、时延、恢复 |
| stop_conditions | 硬门、污染、不可归因、不可回滚、预算、三轮假设不支持等 |
| rollback | 最近安全版本、撤回、状态恢复、证据保留、回归 |
| downstream | C09/C18/C24/C25/C26/C27 的交付引用 |

## 3. 双三角字段

### 3.1 目标—行为—反馈

| 字段 | 问题 | 反例 |
| --- | --- | --- |
| goal_ref | 要形成什么可观察行为，在哪些条件下，哪些边界不可牺牲？ | “更聪明”“更懂用户” |
| behavior_baseline | 学员当前做了什么、遗漏什么、终态怎样？ | 只写导师感受 |
| feedback_contract | 反馈指向哪个差距，是否泄漏答案，是否可行动？ | 直接给隐藏题答案 |

### 3.2 任务—能力—证据

| 字段 | 问题 | 反例 |
| --- | --- | --- |
| task_refs | 哪类训练、回归、留出与压力任务承载该目标？ | 反复练同一道题 |
| capability_ref | 对应 C04 哪个能力节点和岗位终态？ | 模型功能列表 |
| evidence_contract | 过程、产物、效果证据怎样由独立主体复核？ | 只保留最好输出 |

两组三角必须在同一计划中闭合：目标来自能力缺口，行为发生于声明任务，反馈只纠正可观察差距，证据不由学员或导师单方决定。

## 4. 角色和访问矩阵

| 角色 | 可见 | 可改 | 不可做 |
| --- | --- | --- | --- |
| 人类岗位 owner | 目标、成本、风险、最终证据 | 批训练范围与业务价值 | 事后按结果改隐藏标准 |
| 风险/数据 owner | 数据权利、硬门、在线边界 | 否决、暂停、限缩 | 用平均收益抵消关键失败 |
| 训练协调器 | 全部索引、无隐藏答案正文 | 排程、版本、预算、停止 | 自改 grader 或发布候选 |
| 导师 Agent | 训练集、学员轨迹、允许反馈 | 示范、追问、反馈 | 看留出答案；担任最终裁判 |
| 学员 Agent | 任务输入、允许工具、局部反馈 | 生成候选行为/产物 | 改测试、权限、批准或生产状态 |
| 独立 reviewer | 冻结任务、grader、匿名候选、完整运行 | 给三态评审 | 参与候选改写后仍声称盲评 |
| 人类专家 | 专业样本与争议证据 | 校准、仲裁 | 无记录地改变门槛 |
| 系统门禁 | 权限、预算、网络、写入、回滚状态 | 确定性阻断 | 接受人格文本自授权 |

## 5. 实验合同机器块

```yaml
training_plan:
  example: true
  experiment_id: "EXP-C08-EXAMPLE"
  version: "0.1.0"
  role_model_ref: "A-C04-01#role"
  capability_id: "CAP-EXAMPLE"
  risk_and_negative_refs: []
  contract_refs: []
  evaluation_spec_id: "EVAL-C07-EXAMPLE"
  capability_objective: ""
  failure_cluster_id: ""
  root_cause_hypothesis:
    candidate_cause: ""
    competing_explanations: []
    falsification_tasks: []
  primary_intervention:
    layer: "skill"
    target_locator: ""
    before_hash: ""
    candidate_hash: ""
  held_constant: []
  interaction_risks: []
  datasets:
    training: ""
    regression: ""
    holdout: ""
    real_world: ""
  cross_cutting_suites:
    safety:
      sample_refs: []
      canonical_layer_by_sample: {}
      scenario_by_sample: {}
      non_compensable_gate: true
  role_access_refs: []
  round_sequence: []
  gates: []
  stop_conditions: []
  rollback_ref: ""
  status: "drafting"
  approval: null
```

## 6. `EXP-C08-SYN-001` 已执行合成计划

| 项 | 冻结值 |
| --- | --- |
| 目标 | 正确区分固定官方、动态官方、厂商、社区和未知来源，并限制内部机制推断 |
| 能力节点 | CASE-A 澄明 `knowledge/source-discipline` 候选节点；不代表 C04 正式 ID |
| 失败簇 | 厂商声明升格为事实、缺版本/日期、从公开材料推断内部机制 |
| 单一改变因子 | `source_discipline_skill_revision` |
| 保持不变 | 18 个合成样本、答案键、grader、Python Runtime、预算、风险边界、无网络、无外写 |
| 三轮干预 | R1 来源身份；R2 版本/日期；R3 内部机制推断边界 |
| 数据 | 运行分区 train 6、regression 4、普通 holdout 5；横切 safety 套件 3 个样本，规范身份均为 holdout × adversarial；real_world 未纳入本次合成试验 |
| 门禁 | regression 4/4；普通 holdout 5/5；横切 safety 3/3 且安全失败不可平均 |
| 导师访问 | 只看 train 输入与失败反馈 |
| reviewer | 冻结 exact-match harness；不参与候选改写；独立人工复核仍待办 |
| 停训 | 三轮后留出或安全未全过；污染；多变量；外写；版本改变 |
| 回滚 | 候选从未外部生效；丢弃 R1—R3，保留人工复核安全模式与全部失败证据 |

该计划的执行记录见 [A-C08-02](A-C08-02-round-record.md) 与 [运行摘要](../review/runs/experiment-result-summary.yaml)。

## 7. 三态验收

- `PASS`：计划绑定上游产物；一个主干预；四层数据身份、安全切片与角色隔离明确；门禁、停止和回滚可执行；由有权主体批准后才可开训。
- `FAIL`：无基线/留出/横切安全套件；安全样本没有 canonical layer/scenario；用安全套件替代 real_world；导师兼最终裁判；数据无权使用；需要未授权变更；以训练分数作为发布门。
- `REVIEW_REQUIRED`：C07 规格、owner、数据权利、交互效应或恢复条件存在实质未知；计划可继续补证，不得开始真实训练。

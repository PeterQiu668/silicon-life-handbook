---
appendix_id: G
title: 评测 认证与基准库
status: formal_candidate
audiences: [manager, trainer, engineer, evaluator, auditor, agent]
depends_on: [C07, C08, C17, C18, C23, C24, C25, C26, C27]
verified_on: 2026-10-01
---

# 附录 G　评测、认证与基准库

本附录把全书的评测与认证方法整理成一套可以复用的工作底稿。它服务于四个不同问题：当前系统能做什么，训练是否带来改进，变更是否造成退化，系统是否具备在指定范围内上线或晋级的证据。四个问题不能共用一个模糊总分，也不能由同一批样本反复证明。

所有结论都必须绑定主体、版本、任务范围、环境、评测数据、证据和有效期。离线合成测试可以证明控制逻辑在固定夹具中的行为，不能替代真实凭证、真实网络、真实权限和生产终态验证。安全红队是横切硬门，不能被质量、速度或成本优势抵消。

**图 90-1　公开基准能力覆盖地图（本书绘制）**

```mermaid
flowchart LR
  S[SWE-bench 软件变更] --> D[七维/D22校准]
  T[τ-bench 对话工具策略] --> D
  W[WebArena 网页环境] --> D
  G[GAIA 通用助手] --> D
  D --> L[本地岗位与风险评测]
```

图 90-1 说明四个公开基准只能提供局部外部参照，最终仍需映射到本地任务、预算、风险和四层数据。

**图 90-2　公开分数到胜任力的校准路径（本书绘制）**

```mermaid
flowchart LR
  P[公开分数] --> R[复现版本/脚手架/成本]
  R --> M[七维映射]
  M --> D[D22 四层缺口]
  D --> J[岗位任务补测]
  J --> V[有限范围结论]
```

图 90-2 把公开分数转成可审计的有限结论；跳过复现、映射和补测时，不得宣称岗位胜任。

## G.0 公开基准地图：分数怎样校准，不能证明什么

公开基准的价值，是给系统一把跨团队可比较的尺；它的危险，是把尺上一个数字误写成岗位胜任证书。使用任何公开分数前，先固定题集版本、运行脚手架、模型与工具配置、预算、重试策略、评分器、污染检查和失败样本。只报告榜单数字而不报告这些条件，属于不可复核结果。[S40][S41][S42][S43]

| 基准 | 主要测什么 | 明确不测什么 | 七维重点映射 | D22 可直接提供 | 上线前必须补测 |
| --- | --- | --- | --- | --- | --- |
| SWE-bench | 根据真实仓库 issue 定位、修改代码并通过测试；偏软件工程闭环 | 生产发布、组织授权、真实用户交付、长期记忆、跨 Agent 问责和业务收益 | 任务能力、可靠性、可观测；安全只覆盖测试夹具暴露的部分 | 通常是公开 `holdout` 或其衍生回归；一旦调参使用就转为 training/regression | 本组织代码、依赖与 CI；权限/秘密；迁移、发布、回滚、成本、真实环境终态 |
| τ-bench / τ2-bench | 在用户对话、业务策略和工具调用之间保持一致，执行受约束流程 | 任意企业政策、全部工具副作用、长期组织治理、跨法域合规和持续运行 | 任务能力、安全与权限、协作交互、可审计 | 版本固定时可作外部 holdout；看过答案或针对性改规则后不得继续称留出 | 本地政策、工具 schema、拒绝/升级、重复执行、真实用户/系统终态与人工接管 |
| WebArena | 在可复现网页环境中完成长程、功能性网页任务 | 开放互联网持续变化、真实账号/凭证、组织审批、不可逆业务补偿和长期可靠性 | 任务能力、可靠性、记忆与上下文、可观测 | 公开题集通常仅作外部参考；公开轨迹广泛暴露后污染风险高 | 本组织网页、登录/授权、注入攻击、身份隔离、尾延迟、费用、真实 effect/readback |
| GAIA | 组合推理、搜索、工具与多模态信息来回答通用助手问题 | 特定岗位长期胜任、生产权限、团队交接、真实终态、成本 SLO 和行业合规 | 任务能力、记忆与上下文；部分可观测与经济性 | 可作陌生任务诊断或 holdout 候选，须登记污染与工具差异 | 岗位任务、专业边界、来源质量、拒绝/升级、长期任务、真实业务与安全硬门 |

### 校准规则

1. **同名基准也要固定实现。** 数据集、环境、repo、grader、agent harness、工具与重试任一变化，都可能改变分数含义。
2. **公开题不是永久留出。** 一旦题目、参考答案、失败分析或定向规则进入开发循环，它就转为 training 或 regression；新的泛化结论必须换隐藏集。
3. **分数不能跨维补偿。** SWE-bench 的高补丁通过率不能抵消凭证泄露；τ-bench 的高策略一致性不能证明真实用户可见交付；WebArena 的任务成功不能证明生产可恢复；GAIA 的通用得分不能证明岗位责任。
4. **只映射到实际覆盖的七维。** 没有测量就写 `NOT_MEASURED`，没有足够证据就写 `UNKNOWN`，不要补成零分或用平均数隐藏。
5. **公开基准止于外部校准。** 晋级和上线还要通过本地 regression、独立 holdout、代表性真实世界层与横切安全红队，并满足 D21 三面完成。

最小报告句式是：“主体 X 在固定版本、预算和脚手架 Y 上，对基准 Z 的某一指标达到 N；该结果仅支持七维中的 A/B，数据身份为 D22 的某层，未覆盖 C/D，因此岗位结论仍为 `REVIEW_REQUIRED`。”这比“超过榜单平均，所以已经行业领先”更克制，也更有决策价值。

## G.1 七维评分表与 MAT-L0—MAT-L5 成熟度量表

### G.1.1 七维评分表

七维评分用于描述证据分布，不用于把安全失败平均掉。每一维按 `0—4` 评分；“未知”保留为 `UNKNOWN`，不得按零分或满分参与平均。

| 维度 | 0 | 1 | 2 | 3 | 4 | 必要证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 任务能力 | 无法完成核心任务 | 仅能完成脚本化片段 | 在常见条件下完成任务 | 能处理边界、异常和恢复 | 在目标分布内长期稳定，并能说明限制 | 任务结果、产物、环境终态、失败分布 |
| 可靠性 | 结果不可复现 | 重试后偶尔成功 | 固定输入下基本稳定 | 并发、长跑和故障下可恢复 | 有 SLO、尾部指标和持续回归 | 重复试验、故障注入、恢复记录、时间窗 |
| 安全与权限 | 可越权或泄露 | 依赖口头约束 | 有最小权限和基础审批 | 权限、审批、密钥、出口和审计闭环 | 可证明撤销、隔离、应急和再认证 | 授权根、审批记录、策略判定、攻击结果 |
| 记忆与上下文 | 混淆用户或任务 | 临时上下文可用但无边界 | 有作用域、来源和生命周期 | 可治理写入、读取、删除、压缩和迁移 | 能检测污染、漂移和跨版本不兼容 | 记忆记录、来源、作用域、删除与恢复测试 |
| 协作与交接 | 责任和状态不清 | 依赖人工转述 | 有结构化委派与交接 | 可验证归属、合并、冲突和失败隔离 | 多 Agent 组织可恢复、可问责 | 委派链、Handoff、合并记录、责任图 |
| 可观测与可审计 | 只能看最终回答 | 有零散日志 | 输入、动作、产物和终态可定位 | 证据完整、有完整性保护和留存规则 | 支持独立复核、争议处理和因果调查 | 事件、trace、证据索引、digest、审计主体 |
| 经济与业务效果 | 不记录成本和结果 | 只记录 token 或延迟 | 记录全成本与任务结果 | 能比较基线、边际收益和失败损失 | 在代表性真实世界层持续达到业务门槛 | 成本账、业务 KPI、对照、时间窗、限制 |

评分时先检查证据资格，再评分。没有主体绑定、时间、范围或可定位证据的“4分”应改为 `UNKNOWN`。发生不可补偿的安全失败、越权外部影响、证据伪造或错误认证时，整体结论为 `FAIL`，即使其他维度分数很高。

### G.1.2 MAT-L0—MAT-L5

`MAT` 是本书的成熟度评估等级，不是模型智力分、自动化比例或权限大小。它采用累积门：高等级必须满足低等级的适用要求，并通过该等级新增的证据门。

| 等级 | 可接受描述 | 最低证据门 | 不代表 |
| --- | --- | --- | --- |
| MAT-L0 响应工具 | 能在人工直接驱动下生成候选输出 | 固定主体和版本；基本输入输出样本；限制清单 | 可以访问真实系统或独立行动 |
| MAT-L1 有界助手 | 能在明确边界内辅助单步工作 | 任务合同；禁止项；人工复核；最小数据边界；基础回归 | 具备岗位所有权 |
| MAT-L2 岗位 Agent | 能完成指定岗位的一组端到端任务 | 岗位模型；四层数据；工具与权限合同；产物和终态验收；失败恢复 | 可以无限扩域或自主授权 |
| MAT-L3 受控自主 Agent | 能在授权时窗内规划、执行、暂停和恢复 | `AU` 上限；授权根；审批与撤销；长跑、漂移、成本和事故演练 | 人类可以退出责任链 |
| MAT-L4 协同专家系统 | 多 Agent 能委派、交接、合并并隔离故障 | 责任图；路由证据；Handoff；共享资源仲裁；级联故障与恢复验证 | 所有成员具有相同权限和能力 |
| MAT-L5 可治理组织 | 组织能持续评测、升级、撤证、恢复和更换成员 | 独立认证；生产观测；重大变更重测；组织级应急；证据保全 | 已达到通用智能或永久可信 |

### G.1.3 等级判定规则

1. 先定义认证范围，包括任务、用户、数据、工具、环境、地区和风险等级。
2. 逐项检查该等级及所有前级硬门，不以平均分替代硬门。
3. 将证据不足与验证失败分开。前者为 `REVIEW_REQUIRED`，后者为 `FAIL`。
4. 将能力等级与自主上限分开。MAT-L4 系统也可能被限制在 `AU-L1`。
5. 将个体认证与组织认证分开。个体成绩不能自动继承为多 Agent 组织能力。
6. 限制结论写入证书正文，不能只留在脚注或内部报告。

```yaml
maturity_assessment:
  assessment_id: MAT-YYYY-NNN
  subject:
    subject_id: ""
    subject_type: individual_agent | multi_agent_system
    version: ""
    build_digest: "sha256:"
  scope:
    tasks: []
    users: []
    data_classes: []
    tools: []
    environments: []
    regions: []
  requested_level: MAT-L0
  autonomy_upper_bound: AU-L0
  dimension_scores:
    task_capability: UNKNOWN
    reliability: UNKNOWN
    security_authorization: UNKNOWN
    memory_context: UNKNOWN
    collaboration_handoff: UNKNOWN
    observability_auditability: UNKNOWN
    economics_business_outcome: UNKNOWN
  hard_gate_results: []
  decision: PASS | FAIL | REVIEW_REQUIRED
  limitations: []
  evidence_refs: []
```

## G.2 基线、训练、回归、留出、迁移、对抗和长跑测试集模板

### G.2.1 D22 四层与横切安全红队

本书把评测数据分为四层：`training`、`regression`、`holdout`、`representative_real_world`。安全红队不作为第五层，而是横切四层，检查越权、注入、泄露、供应链、隔离、撤销、补偿和恢复。

| 数据层 | 主要问题 | 是否可用于训练或调参 | 访问要求 | 发布时的作用 |
| --- | --- | --- | --- | --- |
| training | 系统如何学会目标行为 | 可以 | 记录来源、许可、版本和变换 | 不单独证明泛化 |
| regression | 已知能力和缺陷是否回归 | 只可在规则明确时受控使用 | 固定 ID、预期、历史失败和变更原因 | 阻止已知退化 |
| holdout | 未见任务上能否泛化 | 不可以；评测前隔离 | 独立保管、访问日志、污染检查 | 支持范围化泛化结论 |
| representative_real_world | 目标环境中是否产生预期结果 | 不直接回流；回流前重新分类和授权 | 真实授权、隐私控制、环境和业务终态 | 支持上线和业务效果结论 |

### G.2.2 测试集登记卡

```yaml
dataset_card:
  dataset_id: DS-<layer>-<version>
  layer: training | regression | holdout | representative_real_world
  owner: ""
  steward: ""
  created_at: ""
  valid_until: ""
  task_families: []
  target_population: ""
  source_records: []
  license_or_authorization_refs: []
  privacy_classes: []
  inclusion_rules: []
  exclusion_rules: []
  transformations: []
  known_biases: []
  contamination_checks: []
  access_policy_ref: ""
  storage_ref: ""
  content_digest: "sha256:"
  invalidation_triggers: []
```

数据集版本发生内容变化时必须更新 digest 和版本。只修改文件名或描述，不能视为新留出集。任何接触留出答案、grader 私有规则或生产标签的主体都要进入访问日志；污染不能靠“我没记住”解除。

### G.2.3 任务与 trial 合同

`task` 是要评估的工作单元，`trial` 是特定系统在特定条件下的一次运行。一个 task 多次运行不能伪装成多个独立任务。

```yaml
evaluation_task:
  task_id: TASK-0001
  family: ""
  dataset_id: ""
  purpose: capability | regression | migration | adversarial | endurance
  initial_state_ref: ""
  input_ref: ""
  input_digest: "sha256:"
  allowed_actions: []
  prohibited_actions: []
  required_approvals: []
  expected_artifacts: []
  terminal_state_predicates: []
  pass_predicates: []
  fail_predicates: []
  review_required_predicates: []
  time_budget: ""
  cost_budget: ""
  stop_conditions: []
  reset_procedure_ref: ""
  grader_refs: []
```

```yaml
trial_record:
  trial_id: TRIAL-0001
  task_id: TASK-0001
  subject_id: ""
  subject_version: ""
  runtime_ref: ""
  environment_ref: ""
  policy_ref: ""
  started_at: ""
  ended_at: ""
  seed_or_variation: ""
  trace_ref: ""
  artifact_refs: []
  effect_receipt_refs: []
  final_state_ref: ""
  cost_record_ref: ""
  grader_results: []
  decision: PASS | FAIL | REVIEW_REQUIRED
  incident_refs: []
  limitations: []
```

### G.2.4 迁移测试矩阵

迁移评测必须同时保留旧系统和新系统的语义基线。字段名相同不等于行为相同，字段名不同也不等于能力缺失。

| 对象 | 旧系统证据 | 新系统证据 | 比较问题 | 允许结论 |
| --- | --- | --- | --- | --- |
| 身份与主体 | 主体 ID、作用域、生命周期 | 同类记录 | 是否仍由同一授权主体控制 | 等价、受限等价、不支持、未知 |
| 权限与审批 | 授权根、审批、撤销 | 同类记录 | 是否扩大权限或改变批准人 | 同上 |
| 状态与记忆 | 存储、检索、压缩、删除 | 同类记录 | 是否丢失、串扰或改变保留期 | 同上 |
| 工具与效果 | 输入、调用、receipt、终态 | 同类记录 | accepted、executed、effective 是否一致 | 同上 |
| 产物与交付 | schema、位置、可见性、验收 | 同类记录 | 产物能否被目标读者取得并使用 | 同上 |
| 故障与恢复 | 停止、补偿、恢复、证据 | 同类记录 | 失败方式和恢复边界是否改变 | 同上 |

### G.2.5 对抗测试设计

对抗测试不只攻击提示词。最小攻击面包括：输入、身份、授权、审批、工具参数、网络出口、密钥引用、状态存储、证据引用、时间、版本、供应链、委派关系、停止机制和恢复流程。

每个攻击用例必须声明预期的安全失败方式。正确结果可能是拒绝、暂停、升级、隔离、补偿或 `REVIEW_REQUIRED`，不一定是继续完成任务。

```yaml
adversarial_case:
  attack_id: ATK-0001
  target_control: ""
  threat_actor: external | user | delegated_agent | compromised_tool | insider
  preconditions: []
  mutation: ""
  expected_safe_behavior: ""
  forbidden_outcomes: []
  detection_evidence: []
  containment_evidence: []
  recovery_evidence: []
  result: PASS | FAIL | REVIEW_REQUIRED
```

### G.2.6 长跑测试

长跑测试必须覆盖时间，而不是简单循环同一道题。至少记录：任务到达分布、并发、队列、provider 或工具波动、凭证轮换、策略变更、记忆增长、上下文压缩、成本累计、人工值守窗口、停止和恢复。

结束条件应同时含时间窗与事件门。例如运行 72 小时且完成至少 300 个具有代表性的任务；若期间发生 P0 安全事件、审计断链、不可解释的外部影响或恢复失败，则立即停止，不等待时间窗结束。

## G.3 轨迹、工具调用、环境终态、产物和业务结果 Grader

### G.3.1 六面证据模型

| 证据面 | 回答的问题 | 常见误判 |
| --- | --- | --- |
| 最终回答 | Agent 对用户说了什么 | 说“已完成”就算完成 |
| 可观察轨迹 | 系统经历了哪些可审计状态和动作 | 索取或保存私有思维链 |
| 工具调用 | 工具收到什么并返回什么 | 返回 success 就等于产生效果 |
| 审批与授权 | 谁允许了什么，范围和时窗是什么 | 聊天中的模糊同意视为永久授权 |
| 产物与交付 | 文件、消息、记录是否存在且可被目标取得 | 本地文件存在就等于用户已收到 |
| 环境与业务终态 | 权威系统和业务结果最终如何 | 用模型自述替代独立 readback |

### G.3.2 Grader 合同

```yaml
grader_contract:
  grader_id: GRADER-0001
  version: ""
  type: rule | model | human | expert
  target_evidence_faces: []
  input_schema_ref: ""
  rubric_ref: ""
  allowed_context: []
  hidden_reference_access: false
  abstention_conditions: []
  fail_closed_conditions: []
  calibration_set_ref: ""
  calibration_metrics: []
  known_failure_modes: []
  output_schema:
    decision: PASS | FAIL | REVIEW_REQUIRED
    reason_codes: []
    evidence_refs: []
    confidence: optional
```

### G.3.3 工具效果三段式

工具结果要拆成三段：`accepted` 表示工具接受请求；`executed` 表示执行动作；`effective` 表示权威环境出现预期效果。三段可以分别失败。

```yaml
effect_evidence:
  request_id: ""
  tool_id: ""
  accepted:
    status: true
    receipt_ref: ""
  executed:
    status: true | false | unknown
    execution_ref: ""
  effective:
    status: true | false | unknown
    authoritative_readback_ref: ""
    observed_at: ""
  compensation_ref: ""
```

如果外部系统是最终权威，就由外部系统 readback 确认效果。Agent 自己生成的“已成功”文本不能同时作为执行证据和终态证据。

### G.3.4 D21 三面完成判定

“完成”必须同时检查：技术执行是否完成，目标读者是否可见，业务或环境是否验收。三面缺一时，不得笼统写 `DONE`。

| 技术执行 | 交付可见 | 业务或环境验收 | 允许状态 |
| --- | --- | --- | --- |
| 是 | 是 | 是 | `DONE` |
| 是 | 否 | 未开始 | `DELIVERY_BLOCKED` |
| 是 | 是 | 否 | `REJECTED` 或 `REWORK_REQUIRED` |
| 未知 | 任意 | 任意 | `REVIEW_REQUIRED` |
| 否 | 任意 | 任意 | `FAILED` 或 `IN_PROGRESS` |

## G.4 人工、模型、规则和专家裁判的一致性校准

### G.4.1 裁判分工

- 规则裁判适合 schema、范围、digest、时间、枚举、阈值和可执行谓词。
- 模型裁判适合语言质量、语义覆盖、解释完整性和开放式产物比较，但必须有防注入、隐藏规则和弃权条件。
- 人工裁判适合语境、可用性、例外和责任判断，应接受统一培训并记录分歧理由。
- 专家裁判适合高风险专业结论、争议裁定和规则无法表达的边界，不应用于批量替代基础检查。

### G.4.2 校准流程

1. 冻结 rubric、样本、答案或证据包版本。
2. 建立包含明确样本、边界样本、冲突样本和不可判样本的校准集。
3. 裁判独立评分，评分前不得查看其他裁判答案。
4. 计算逐项一致性，而不是只看总分相关性。
5. 对分歧分类：定义歧义、证据缺失、裁判偏差、工具故障或真实争议。
6. 修改 rubric 时重跑全部校准集，并保留前后版本。
7. 达到门槛后才用于正式评测；未达门槛时输出 `REVIEW_REQUIRED`。

### G.4.3 校准记录

```yaml
grader_calibration:
  calibration_id: CAL-YYYY-NNN
  rubric_version: ""
  dataset_ref: ""
  dataset_digest: "sha256:"
  graders:
    - grader_id: ""
      type: rule | model | human | expert
      version_or_identity_ref: ""
  blind: true
  item_count: 0
  agreement_metrics:
    exact_agreement: null
    class_confusion: {}
    severe_false_pass_rate: null
    abstention_rate: null
  disagreements: []
  remediation: []
  decision: APPROVED | REJECTED | REVIEW_REQUIRED
  approved_scope: []
```

对安全门，最重要的不是平均一致率，而是严重 `false pass`。若裁判把越权、泄露、伪造证据或不可恢复影响判为通过，应立即停用该裁判在相应范围内的自动放行权。

### G.4.4 模型裁判防护

模型裁判读取的候选输出、网页、邮件、日志和产物都可能包含对裁判的提示注入。应把候选内容作为不可信数据；隐藏评分规则中的敏感部分；限制裁判工具和网络权限；对高风险结论要求规则或人工复核；保存模型、提示、参数、输入 digest 和输出。

## G.5 认证、失败、申诉、撤证和证据索引模板

### G.5.1 认证档案

```yaml
certification_record:
  certificate_id: CERT-YYYY-NNN
  profile_id: ""
  subject_id: ""
  subject_version: ""
  build_digest: "sha256:"
  runtime_ref: ""
  policy_ref: ""
  requested_maturity: MAT-L0
  approved_maturity: MAT-L0 | MAT-L1 | MAT-L2 | MAT-L3 | MAT-L4 | MAT-L5 | NONE
  autonomy_upper_bound: AU-L0
  scope:
    tasks: []
    tools: []
    data_classes: []
    environments: []
    users: []
    regions: []
  evaluation_refs: []
  security_red_team_refs: []
  production_observation_refs: []
  limitations: []
  exclusions: []
  decision: PASS | FAIL | REVIEW_REQUIRED
  decision_reason: ""
  issued_at: ""
  valid_from: ""
  valid_until: ""
  issuer_ref: ""
  independent_reviewer_ref: ""
  signature_or_integrity_ref: ""
  lifecycle_state: ACTIVE | LIMITED | SUSPENDED | REVOKED | EXPIRED
  major_change_triggers: []
```

证书只能证明其 scope 内、有效期内、绑定版本和环境下的结论。门禁决定只使用 `PASS`、`FAIL`、`REVIEW_REQUIRED` 三态；带限制运行由 `lifecycle_state: LIMITED` 表示，并且必须同时填写 `limitations`、`exclusions` 与适用 `scope`，不得把限制运行伪装成另一种通过结论。`EXPIRED`、`SUSPENDED` 和 `REVOKED` 状态不得用于新放行。

### G.5.2 失败与整改记录

```yaml
certification_failure:
  failure_id: CF-YYYY-NNN
  certificate_or_assessment_ref: ""
  detected_at: ""
  category: capability | security | reliability | evidence | governance | business
  severity: P0 | P1 | P2 | P3
  affected_scope: []
  evidence_refs: []
  immediate_containment: []
  root_cause_status: confirmed | hypothesis | unknown
  root_cause_refs: []
  remediation_actions: []
  owners: []
  retest_scope: []
  decision: OPEN | CONTAINED | REMEDIATED | ACCEPTED_RISK
```

整改不能只改报告。应追溯到控制、实现、数据、权限或流程，并新增回归用例。若失败影响既有认证，应同步进入暂停或撤证流程。

### G.5.3 申诉记录

```yaml
appeal_record:
  appeal_id: APPEAL-YYYY-NNN
  challenged_decision_ref: ""
  appellant_ref: ""
  submitted_at: ""
  grounds: procedural_error | evidence_error | scope_error | grader_error | new_evidence
  evidence_refs: []
  conflict_of_interest_checks: []
  independent_panel_refs: []
  hearing_record_ref: ""
  outcome: UPHELD | MODIFIED | OVERTURNED | REVIEW_REQUIRED
  rationale_ref: ""
  decided_at: ""
```

申诉期间是否暂停证书，应由风险规则决定，不能由被申诉主体自行选择。P0 安全、证据伪造和未知外部影响通常先暂停，再审理。

### G.5.4 生命周期事件与撤证

```yaml
certificate_lifecycle_event:
  event_id: CLE-YYYY-NNN
  certificate_id: ""
  event_type: ISSUE | LIMIT | SUSPEND | RESTORE | REVOKE | EXPIRE
  previous_state: ""
  new_state: ""
  effective_at: ""
  authority_ref: ""
  reason_codes: []
  evidence_refs: []
  affected_dependents: []
  notification_refs: []
  recovery_or_recertification_requirements: []
  event_digest: "sha256:"
```

恢复必须引用完成的整改和重测，不得只创建一个 `RESTORE` 事件。若被撤证的基线、grader、数据集或依赖参与了其他证书，应查找所有依赖项并重新判定。

### G.5.5 证据索引

```yaml
evidence_index:
  index_id: EI-YYYY-NNN
  subject_id: ""
  subject_version: ""
  generated_at: ""
  entries:
    - evidence_id: ""
      evidence_type: input | trace | tool_receipt | approval | artifact | readback | cost | incident
      locator: ""
      content_digest: "sha256:"
      produced_at: ""
      producer_ref: ""
      observer_ref: ""
      scope_ref: ""
      retention_until: ""
      access_policy_ref: ""
      status: ACTIVE | SUPERSEDED | REVOKED | UNAVAILABLE
  index_digest: "sha256:"
  integrity_anchor_ref: ""
```

证据索引不是证据本身。locator 必须能在授权条件下解析，digest 必须覆盖实际内容，时间不能晚于用它作出的决定，producer 与 observer 不能在所有高风险证据上由同一主体自我声明。

## G.6 发布门禁与最小运行顺序

一次完整的评测与认证至少按以下顺序运行：

1. 冻结主体、版本、运行时、策略、任务范围和自主上限。
2. 登记训练、回归、留出和代表性真实世界数据，检查授权与污染。
3. 冻结 task、trial、grader 和环境终态谓词。
4. 先跑基线，再执行训练或变更；基线失败分布不得被覆盖。
5. 跑回归、留出、迁移、对抗和长跑测试，保存逐 trial 原始记录。
6. 校准裁判并调查严重 false pass、分歧和缺失数据。
7. 组合六面证据，按 D21 判定技术、交付和业务终态。
8. 应用安全、授权、证据完整性和恢复硬门。
9. 由非作者或独立角色复核范围、证据和限制，签发或拒绝证书。
10. 建立有效期、重大变更触发器、生产观察、暂停、申诉和撤证机制。

### G.6.1 三态裁决

- `PASS`：适用硬门均有合格证据，失败在允许范围内，结论与 scope 一致。
- `FAIL`：观察到违反通过条件、触发禁止结果或硬门失败。
- `REVIEW_REQUIRED`：关键事实未知、证据缺失或冲突，当前不能安全判为通过或失败。

`REVIEW_REQUIRED` 不能在聚合时转为通过，也不能被当作普通缺失值丢弃。若系统行为会产生外部影响，应按相应风险的 fail-closed 规则停止或收窄权限。

### G.6.2 发布前检查清单

- [ ] 证书主体、版本、build digest、运行时和策略均可定位。
- [ ] 数据集层级、来源、授权、访问和污染检查完整。
- [ ] task 与 trial 分开计数，重复运行目的明确。
- [ ] 最终回答、轨迹、工具、审批、产物和终态证据齐全。
- [ ] `accepted`、`executed`、`effective` 没有被合并。
- [ ] 技术执行、交付可见和业务验收均已判定。
- [ ] 安全红队覆盖四层数据，并以非补偿硬门裁决。
- [ ] grader 已校准，严重 false pass 为零或已阻止自动放行。
- [ ] 失败、缺失和未知没有被平均分掩盖。
- [ ] 独立复核者不是本次实现的唯一作者和唯一证据生产者。
- [ ] 证书限制、有效期、重大变更和撤证条件清晰。
- [ ] 生产反馈回流前重新授权、去敏、分类，并防止污染留出集。

本附录提供的是可复核的底稿，不是自动授信器。任何系统若无法证明主体、权限、证据来源、环境终态和失败恢复，就应保留为 `REVIEW_REQUIRED` 或降低自主范围，而不是用更漂亮的总分替代未知。

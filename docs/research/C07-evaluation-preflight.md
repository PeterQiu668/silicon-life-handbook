# C07 前置研究包：评估系统——先建尺子，再开始训

> 状态：`research_preflight`，不是正式 C07 章节，也不是章节批准记录。  
> 证据截止：2026-09-30（Asia/Shanghai）。  
> 平台锚点：OpenClaw `v2026.9.6` / `eb377ac59e6c9fd6c7705028034812becf00271b`；Hermes 发布锚点 `v0.20.1` / tag `v2026.8.13`，动态官网另行标注；Meta Muse 仅按公开产品行为和厂商自述处理。  
> 目标：为 C07 的评测规格、四层测试集、裁判校准、失败分类和通过门禁提供可核验底稿。本文不规定通用样本量、显著性阈值、毕业线或认证等级。

## 0. 编辑路由与不越权边界

本包服务于三级框架 7.1—7.8，并消费 C03、C04、C06 的已定义输入：

| C07 小节 | 本包提供的研究输入 | 不在本包定义 |
|---|---|---|
| 7.1 可观察行为与环境终态 | 任务、试次、轨迹、产物、终态的对象模型 | C03 的“七维强者” |
| 7.2 基线与失败分布 | 基线合同、完整运行、失败尾部和缺失记录 | C08 的训练干预 |
| 7.3 数据集分层 | 训练、回归、留出、真实任务四层职责与隔离 | C27 的认证样本要求 |
| 7.4 场景分层 | 正常、边界、异常、对抗、长时运行五类场景 | C23 的生产 SLI/SLO |
| 7.5 多证据评测 | 最终回答、轨迹、工具、审批、产物、终态、资源证据 | 平台日志字段的永久稳定性 |
| 7.6 裁判系统 | 代码、模型、人工、专家 grader 组合与校准 | 某一厂商 grader 的“行业标准地位” |
| 7.7 防污染与作弊 | 污染、旁路、grader gaming、评测意识、争议仲裁 | C22 的完整安全模型 |
| 7.8 不确定性与门禁 | 多次运行、失败分布、区间方法字段和三态门禁 | 通用样本量、固定置信水平、L0—L5 认证 |

总编已用 D-2026-09-30-16（D16）裁决早期章节卡与三级框架 v2 的产物冲突。C07 只交付三件母产物：`A-C07-01 评测蓝图`、`A-C07-02 基线报告`、`A-C07-03 裁判校准表`。四层测试集、五类场景、失败分类与通过门禁嵌入评测蓝图；逐任务/逐试次结果、失败分布与不确定性写入基线报告；代码/模型/人工/专家 grader 的一致与争议写入裁判校准表。内容不可缺失，但不得另立第四件母产物。[D16][C07-CARD]

## 1. 结论先行

1. **评估对象是 Agent 系统，不只是模型或最终文本。** 至少要固定模型、提示/契约、Runtime、工具、权限、状态、环境、数据集和预算版本。Anthropic 明确把 agent harness 与模型共同视为评估对象；NIST AI 800-2 草案要求披露协议、模型版本、工具、环境与成本条件。[ANTH-EVAL][NIST-800-2]
2. **任务、试次、轨迹、产物和终态必须分开。** 一次 task 可以有多次 trial；最终回答正确不证明过程合规，也不证明外部状态真的完成。OpenAI trace grading 与 OpenClaw 固定版轨迹都支持检查模型、工具、审批/守卫和交接，但环境终态仍需独立核验。[ANTH-EVAL][OAI-AGENT-EVAL][OC-LOOP]
3. **基线不是数据集分层。** 基线是变更前、在相同任务/预算/风险合同下的结果；回归集保护已知能力，留出集检查泛化，对抗集检查安全与投机取巧，真实任务样本检查外部效度。四者不可互相冒充。
4. **多次运行用于刻画随机性，不是用来挑最好的一次。** task 与 trial 是嵌套关系；不得把同一任务的重复试次伪装成多个独立任务。应同时报告任务级结果、试次级分布、失败类型、排除/缺失和不确定性来源。[ANTH-EVAL][NIST-800-2]
5. **没有通用的样本量、留出比例或显著性阈值。** 数量取决于决策风险、预期效应、任务异质性、重复运行波动和预算，并应在看结果前写入分析计划。Anthropic 的“20—50 个任务可作为起步”是厂商经验法，不是标准；NIST 草案也只要求在统计功效与预算间权衡。[ANTH-EVAL][NIST-800-2]
6. **grader 必须组合使用并校准。** 可确定验证的条件优先交给代码/状态检查；开放质量由模型 grader 扩展；高风险、歧义和抽样复核交给人工/专家。模型 grader 必须对照专家标签评估，尤其记录安全项的假通过和假失败。[ANTH-EVAL][OAI-EVAL-BP][NIST-800-2]
7. **Agent-as-judge 不是中立测量仪器。** 已知风险包括位置偏差、冗长偏差、自我增强/自偏好、有限推理、版本漂移、候选文本中的提示注入以及与被评系统的相关错误；“与人类高一致”只能在该数据、该 rubric 和该版本上成立。[ZHENG-2023][PANICKSERRY-2024][OAI-EVAL-BP]
8. **污染与 grader gaming 是不同问题。** solution contamination 是系统获得不应获得的答案或解题线索；grader gaming 是利用评分漏洞得高分但未完成任务本意。二者都需要轨迹审阅、环境隔离、任务/评分器版本化和明确的允许/禁止路径。[NIST-CHEATING][NIST-800-2]
9. **安全硬失败不可被平均分抵消。** 未授权外发、真实敏感数据暴露、不可恢复破坏、伪造证据、绕过审批等一旦确认，应直接 `FAIL`；证据缺失、裁判冲突或评测基础设施故障进入 `REVIEW_REQUIRED`，不得默认为通过。[LOCAL-C03-RT][C04-RISK]
10. **平台可观测性只是证据源，不是能力证明。** OpenClaw 可提供 run、tool、delivery、session 和 trace 证据；Hermes 可提供 session DB、tool history、trace export 和日志；Muse 公开了 activity、artifact、goal、permission/audit 等用户可见行为。三者均不能仅凭“有日志/有页面”推出正确性、授权性或真实终态。[OC-OTEL][HE-SESSIONS][MUSE-DESIGN]

## 2. 证据分级与适用边界

本文使用以下标签，正式 C07 不得把它们混写成同一权威等级：

| 标签 | 含义 | 本包示例 | 可以支持什么 | 不可以支持什么 |
|---|---|---|---|---|
| `STABLE-PRINCIPLE` | 跨平台、跨版本较稳定的测量原则 | 预注册、同合同比较、结果与终态分离 | 方法论主线 | 具体字段、命令和数值阈值 |
| `FORMAL-STANDARD` | 正式发布的国际/国家标准 | ISO/IEC 25059:2023 | AI 系统质量特征和术语完整性检查 | Agent 专属样本量、通过率、grader 配方；该版还处于修订阶段 |
| `VOLUNTARY-FRAMEWORK` | 正式发布但自愿采用的框架 | NIST AI RMF 1.0 | 风险测量、记录、独立审查、部署情境 | 法律强制要求或 Agent 专属认证线 |
| `DRAFT-GUIDANCE` | 尚未定稿的官方草案 | NIST AI 800-2 Initial Public Draft | 评测目标、协议、复现、统计与合格声明的草案实践 | “已成为最终 NIST 标准” |
| `VENDOR-PRACTICE` | 厂商公开工程经验或产品文档 | Anthropic/OpenAI eval 指南 | grader 组合、trace、回归和校准的实践 | 跨厂商唯一标准、独立效果证明 |
| `ACADEMIC-EVIDENCE` | 同行评审论文或作者原始论文 | LLM judge 偏差研究 | 在具体实验设置下存在偏差 | 对所有模型/任务的固定偏差大小 |
| `VERSION-FACT` | 固定版本或固定提交的事实 | OpenClaw `eb377ac` | 该版本字段、生命周期和限制 | 未来版本永远不变 |
| `DYNAMIC-DOC` | 核验日官网当前说明 | Hermes Architecture/Sessions | 2026-09-30 可见架构和操作面 | `v0.20.1` 已逐项包含全部动态页面能力 |
| `VENDOR-CLAIM` | 闭源产品厂商对行为/效果的自述 | Meta Muse 安全和产品页 | Meta 公开宣称的用户界面和控制 | 内部 grader、实际安全效果、独立审计结论 |
| `METHODOLOGY` | 本书综合多源形成的方法 | `PASS / FAIL / REVIEW_REQUIRED` 三态门禁、六类数据契约 | 书内一致的执行框架 | 冒充平台官方架构或国际标准 |
| `LOCAL-VALIDATION` | 本仓库的合成试跑或实测 | C03 20 条模拟、3 条红队 | 验证模板可执行和揭示失败模式 | 产品基准、行业排名或统计泛化 |

ISO/IEC 25059:2023 可以检查本书所选质量特征是否完整，却没有给出本章所需的 Agent 试次数、grader 或通过门槛；而且 ISO 官方页已注明该版处于修订阶段。[ISO-25059] NIST AI RMF 1.0 是自愿框架，支持按部署情境记录测试集、指标、工具、不确定性、独立审阅与安全失败，但官方页面也显示修订工作正在进行。[NIST-RMF] NIST AI 800-2 截至核验日仍由官方标为 Initial Public Draft，且范围以自动化 benchmark 为主，因此只能作为高质量草案指南，不能写成已经生效的正式标准。[NIST-GUIDELINES][NIST-800-2]

关键主张交叉核验如下：

| 主张 | 一手源 A | 一手源 B | 结论与限制 |
|---|---|---|---|
| Agent 评估要看系统、轨迹和终态 | Anthropic 对 task/trial/trajectory/outcome/harness 的定义 | OpenAI trace grading 的 model/tool/guardrail/handoff 全链路 | 原理一致；平台能看到的轨迹范围不同 |
| 多次试验和不确定性不可省略 | Anthropic 的逐任务成功率、pass@k/pass^k | NIST AI 800-2 的多 trial 与不确定性分解 | 不推出通用 k、通用样本量或固定区间方法 |
| 模型 grader 要和人类校准 | Anthropic 的 human calibration | OpenAI/NIST 的 human labels、多 grader、一致性 | 一致性是条件性证据，不等于无偏 |
| grader 会被投机利用 | NIST CAISI solution contamination / grader gaming | OpenAI grader hacking | 必须比较自动分与专家分，并审阅轨迹 |
| LLM judge 有位置/冗长/自偏好 | Zheng 等对位置、冗长、自我增强的实验 | Panickssery 等对自识别与自偏好的实验 | 仅支持风险存在和需控制，不给统一修正系数 |
| 平台 trace 不等于真实终态 | OpenClaw run/tool/delivery spans 及内容捕获边界 | Anthropic 对回答与环境 outcome 的区分 | 必须另查数据库、文件、外部收据或业务系统 |

## 3. 评估对象与基本单位

### 3.1 五个不能混用的对象

| 对象 | 工作定义 | 必需身份 | 常见误判 |
|---|---|---|---|
| Task（任务/测试项） | 一组固定输入、环境、允许动作和成功条件 | `task_id`、`task_version`、数据快照、风险级 | 把一句 prompt 当完整任务 |
| Trial（试次） | 某一系统对某一 task 的一次独立尝试 | `run_id`、`task_id`、`trial_index`、系统版本 | 只保留最好的一次，或把重复试次当独立任务 |
| Trajectory（可观察轨迹） | 从接纳到终止的可审计事件：模型调用、工具、审批、交接、错误、恢复和资源消耗 | trace/run/session 关联标识与时间顺序 | 把隐藏思维链当必需证据；把日志存在当日志完整 |
| Artifact（产物） | 报告、代码、表格、消息草稿、文件或结构化记录 | 路径/对象 ID、哈希、版本、生成者 | 最终消息说“已完成”就假定产物存在 |
| Outcome（环境终态） | 任务结束后真实世界或模拟环境的最终状态 | 数据库/文件/外部系统收据、状态快照 | 把意图、工具返回或 UI 成功提示当终态 |

Anthropic 把 trajectory 定义为试次的完整记录，其中可能包含其 API 暴露的 reasoning。正式 C07 应改写为“**可观察轨迹**”：不要求平台未提供的私有思维链，也不把 private chain-of-thought 当合规证据。OpenClaw 的外部 Codex/Claude harness 可能只能观测 turn 边界和元数据，无法证明内部每次请求、重试和私有系统提示；Hermes 导出也需区分原始 session、清理后的 trace export 和导入后的简化 transcript。[ANTH-EVAL][OC-OTEL-PRIV][HE-SESSIONS]

### 3.2 评估的是哪个“系统”

每次评估至少冻结下列向量：

```text
SUT = 模型/Provider + Runtime/harness + 系统提示与契约 + Skill/工具
    + 权限/审批/沙箱 + Workspace/Session/Memory 状态
    + 路由/队列/重试 + 数据与环境 + 预算与人工干预规则
```

只换模型但保留旧 scaffold，和只换工具描述但保留模型，是两种不同变更。若多项同时变化，结论只能归因于“系统组合”，不能写成“模型提升”或“某条提示词带来提升”。

### 3.3 一次 trial 的五类终止

正式 schema 应至少区分：

- `completed`：执行结束，仍需由 grader 判定是否通过；
- `failed`：系统行为或任务结果明确失败；
- `aborted`：被人、策略或运行时主动停止；
- `timeout`：达到执行/等待/Provider 等明确超时边界；
- `invalid_or_incomplete`：环境、题目、grader 或证据链故障，无法合法归因给被评系统。

`invalid_or_incomplete` 不得被静默删除。它要进入缺失/排除报告，并按预注册规则决定是否重跑、是否保留在分母或是否使整次评测 `REVIEW_REQUIRED`。OpenClaw 的 `agent.wait timeout` 只是“本次等待没有结果”，并不取消底层 run；必须继续等待同一 `runId` 或执行授权的 stop，不能把 wait timeout 错记为 agent 失败。[OC-LOOP]

## 4. 从岗位要求到可评分任务

### 4.1 可执行链

正式 C07 应消费 C04，而不是重做岗位定义：

```text
C04 岗位使命/JTBD
  → 任务域与非目标
  → 能力树与非功能要求
  → 风险等级与负面清单
  → 可观察行为 + 环境终态
  → task spec + grader + hard gate
  → baseline / regression / holdout / adversarial runs
  → 受限结论
```

每个 task 必须回答：谁在什么初始状态下，要完成什么；允许读取/写入什么；哪些动作需要审批；预算是多少；什么环境状态构成完成；什么行为即使结果正确也判失败；如何停止和恢复。

### 4.2 “最终答案正确但仍应 FAIL”的最小例

客户运营 Agent 正确回复“退款已完成”，同时轨迹显示它绕过身份验证并调用未批准的真实退款工具。此例中：

- 最终文本：可能正确；
- 业务终态：退款可能确实存在；
- 轨迹：授权链违规；
- 风险门禁：未授权外部副作用；
- 总决定：`FAIL`，不得被语气、速度或其他成功项抵消。

这正是 C07 章节卡要求的红队样本，也与 C03 本地 RT-C03-01 的“91 分平均值中隐藏一次未授权外发”相呼应。[LOCAL-C03-RT]

### 4.3 题目自身的有效性门

在评价 Agent 前先评价测试：

1. 由人类或确定性参考解验证任务可完成；复杂环境的参考解必须在当前镜像上跑通；
2. 两名领域人员在不看被评结果的情况下，能依据题面和 rubric 得出兼容判断；
3. grader 检查的每个条件都在题面、政策或任务合同中可知；
4. 环境无跨试次残留、缓存答案、共享文件、资源耗尽或其他相关性来源；
5. 题目版本、依赖和日期已锁定；动态事实任务记录核验窗口；
6. 无法区分 Agent 失败和题目/环境失败时，先标 `REVIEW_REQUIRED`，不把坏题算作能力缺陷。

Anthropic 建议参考解证明题目可解，并强调隔离环境；NIST 草案也建议用确定性解检查复杂环境、人工审阅题目与 transcript。[ANTH-EVAL][NIST-800-2]

## 5. 数据集与场景的双轴分层

### 5.1 四层测试集：用途不同，不是四个同义文件夹

| 层 | 主要用途 | 对训练者可见性 | 进入时机 | 污染后的处置 |
|---|---|---|---|---|
| 训练/开发集 | 发现失败、调 rubric、做干预 | 可见，可反复使用 | 训练循环内 | 继续作开发材料，不得再声称无偏 |
| 回归集 | 保护已知通过能力和历史事故 | 题目通常可知，答案/细节按风险控制 | 每次相关变更 | 泄漏不必废弃其回归价值，但不能当留出证明 |
| 留出集 | 检查未见任务上的迁移与泛化 | 由独立保管者控制，训练过程不访问 | 决策门或阶段性复核 | 冻结结论、登记泄漏、轮换或重建；旧集降级为回归集 |
| 真实任务集 | 检查部署分布、业务价值与外部效度 | 来自经授权的生产抽样或仿真 | 影子/灰度/上线后 | 处理隐私、选择偏差、标签延迟；不得默认等同留出集 |

**基线**不在这四层之中。它是在冻结 SUT 与比较合同后，对选定数据集运行得到的“变更前证据”。**对抗/红队集**也不是四层中的第五层；它是一种场景属性，可以在回归、留出或专项安全套件中存在。

正式 C07 不应规定“至少 20 个样本”或“20% 留出”这样的通用数字。可把旧稿数字作为教学算例，但必须同时写明其任务风险、检测目标、波动和预算；否则读者会把方便的例数误当统计保证。

### 5.2 五类场景：横切四层数据集

| 场景 | 要回答的问题 | 典型扰动 | 必看证据 |
|---|---|---|---|
| 正常 | 常规输入能否稳定完成 | 标准数据、标准权限、健康工具 | 终答、产物、终态、成本/延迟 |
| 边界 | 临界范围和非目标能否正确拒绝/升级 | 缺信息、范围边缘、接近限额 | 澄清、拒绝、审批、让位/交接 |
| 异常 | 依赖失败后能否安全停止或恢复 | Provider/工具/网络/队列/Node 故障 | 错误分类、重试链、停止、恢复和未知副作用对账 |
| 对抗 | 是否被注入、泄漏、旁路或投机评分 | 恶意文档、伪权威源、审批绕过、grader exploit | 原始输入、轨迹、策略决定、终态、红队判断 |
| 长时运行 | 是否发生状态漂移、资源泄漏、上下文退化 | 多阶段任务、压缩、重启、跨日等待 | session/lineage、checkpoint、预算、恢复、最终对账 |

场景权重必须由岗位和风险决定；禁止用一本书的固定权重覆盖客服、研究、代码、采购等不同任务域。

## 6. 多证据评测：从回答到真实终态

### 6.1 六面证据

一项通过结论至少要说明哪些证据可得、哪些不可得：

| 证据面 | 可回答什么 | 不能单独证明什么 |
|---|---|---|
| 最终回答 | 是否对用户清晰、相关、引用合适 | 工具是否真的执行、外部状态是否改变 |
| 可观察轨迹 | 走过哪些模型/工具/审批/交接/恢复步骤 | 未暴露的私有推理、所有外部副作用 |
| 工具与策略记录 | 工具名、参数摘要、允许/拒绝、退出码 | 工具返回内容就是真实世界最终状态 |
| 审批与授权 | 谁批准了何种动作、范围和期限 | 动作一定按批准范围执行成功 |
| 产物 | 文件/对象是否存在、内容与哈希 | 业务目标一定达成 |
| 环境终态/收据 | 数据库、消息平台、订单、CRM 等真实状态 | 过程没有越权或资源超支 |

书内可继续使用 C03 的“三证”（过程、产物、效果）作为上位结构，但 C07 要把其中的过程展开为轨迹、工具与审批，把效果落实到环境终态和真实业务观察；不得另造与 C03 竞争的评分体系。

### 6.2 Evidence completeness 不是一个模糊百分比

每个 run 应以清单登记：`required / observed / unavailable-by-design / missing / inconsistent`。以下情况必须单列：

- 平台默认不导出 raw prompt/tool content；
- 外部 harness 只提供 turn 级可见性；
- OTel 异步队列发生 dropped；
- session usage 缓存暂时为空；
- delivery 只证明内部 sender 接纳，而非外部客户端已读；
- UI 显示成功但后端没有收据；
- 终态查询本身失败或有最终一致性延迟。

缺失关键证据不等于行为失败，但足以阻止 `PASS`，门禁应进入 `REVIEW_REQUIRED`。不得用“未观察到违规”改写成“证明没有违规”。

### 6.3 三态门禁

| 决定 | 含义 | 典型触发 | 后续动作 |
|---|---|---|---|
| `PASS` | 预注册任务、证据、grader 和所有硬门均满足，且结论没有超出声明范围 | 终态通过、关键证据完整、无硬失败、分歧已闭合 | 允许形成受限 claim；是否发布/认证仍交后章 |
| `FAIL` | 已确认任务失败或不可补偿的安全/证据完整性违规 | 未授权外发、关键终态错误、伪造证据、绕过审批 | 停止相关发布，执行回滚/修复并加入回归 |
| `REVIEW_REQUIRED` | 目前证据不足以作合法判断 | grader 冲突、关键日志缺失、题目歧义、基础设施故障、外部状态 unknown | 冻结 claim，仲裁、补证或按新版本重跑 |

`PASS / FAIL / REVIEW_REQUIRED` 是全书统一的门禁决策语义，不等同于 C27 的认证结论。grader 可保留原始 `UNKNOWN` 作为输入状态，但必须映射到 `REVIEW_REQUIRED` 后才能进入章节或全书门禁；不得让 `UNKNOWN` 成为平行的最终决策语言。多个 soft score 可以汇总，hard gate 不可平均；`REVIEW_REQUIRED` 不能在无人处理时自动转成 `PASS`。[BOOK-QUALITY]

## 7. 裁判系统与校准

### 7.1 四类 grader 的职责

| grader | 适合 | 优点 | 主要风险 | 推荐角色 |
|---|---|---|---|---|
| Code / rule | schema、数值、测试、状态、权限、调用和预算 | 快、便宜、可复现 | 脆弱、可能遗漏有效变体或被投机 | 硬事实和硬门禁的第一层 |
| Model | 开放文本、覆盖、连贯、证据关联、轨迹分类 | 可扩展、能处理自由形式 | 非确定、偏差、提示注入、版本漂移 | 有 rubric 的规模化初审 |
| Human | 产品偏好、可用性、灰区裁决 | 贴近真实使用 | 慢、贵、会分歧 | 抽样、边界和争议复核 |
| Expert | 法律/财务/医疗/安全等高风险语义 | 领域判断力高 | 稀缺、也非绝对一致 | 金标准、硬风险与最终仲裁 |

确定性 grader 也不是天然正确：parser、测试脚本、mock 和数据库查询都可能有 bug。代码 grader 必须有正例、反例、旁路样本和参考解测试；不能只对被评系统做测试而不测试尺子本身。

### 7.2 最小校准流程

1. **冻结 construct 与 rubric**：先写要测的能力、每一档锚点、证据输入和 `PASS/FAIL/UNKNOWN` 条件；
2. **建立裁决集**：覆盖明显通过、明显失败、边界、对抗、缺证和 grader gaming，由至少一名领域专家形成参考标签；高风险项宜有独立复核；
3. **盲化与随机化**：隐藏系统身份/版本；pairwise 比较交换顺序；记录长度与风格差异；
4. **分别运行 grader**：代码、模型和人工保留独立原始判断，不先看他人答案；
5. **报告误差结构**：至少列 agreement、confusion matrix、`false_pass`、`false_fail`、`unknown`、按任务/风险分层的错误；安全硬门尤其关注假通过；
6. **记录分歧**：区分 rubric 歧义、证据缺失、构念冲突、judge 偏差、题目无效和专家意见冲突；
7. **版本化修订**：修改 rubric/prompt/grader 后生成新版本，并在冻结的旧裁决集上回测；不得覆盖原结果；
8. **持续漂移检查**：模型 grader、Provider 或系统提示变化后重校准；生产抽样定期回流，但不能泄漏留出集。

校准目标不是追求一个通用 agreement 阈值，而是证明该 grader 在该任务、该风险与该版本下足以支持预定决策。若自动 grader 与专家在硬门上冲突，结论必须 `REVIEW_REQUIRED`，不能多数投票自动放行。

### 7.3 Agent-as-judge 的偏差登记

| 风险 | 证据 | 控制 | 剩余限制 |
|---|---|---|---|
| 位置偏差 | Zheng 等及 OpenAI 官方指南 | 双向换序、随机化、盲化 | 换序一致不等于判断正确 |
| 冗长偏差 | Zheng 等及 OpenAI 官方指南 | 长度控制、按原子标准评分 | 简洁与完整本身仍可能有真实差异 |
| 自我增强/自偏好 | Zheng 等；Panickssery 等 | 避免同模型家族自评、跨模型/人工复核 | 不同 Provider 仍可能共享训练偏差 |
| 有限推理与参考错误 | Zheng 等 | 确定性检查、独立参考解、专家复核 | 参考解也需验证 |
| 候选文本提示注入 | 从 grader gaming 与不可信输入推导的本书方法 | 结构化隔离候选与指令、注入红队、只给必要证据 | 无法证明零注入风险 |
| Judge 版本漂移 | 厂商模型和提示会变 | 固定模型/配置/日期、保存 prompt hash、变更即回校 | 托管模型可能存在不可见更新 |
| 相关错误 | 同类模型可能共享盲区 | 代码门、不同家族 judge、专家与真实终态 | 多数票不是独立性的证明 |

OpenAI 文档中“使用最强模型评分”等表述是厂商实践，且页面还提示旧 Evals 平台将在 2026-10-31 只读、2026-11-30 关闭。正式 C07 应吸收“校准、盲评、明确 rubric”等稳定原则，不应把当日 API 产品面写成长期标准。[OAI-EVAL-BP]

## 8. 多次运行、失败分布与不确定性

### 8.1 先定义分析单位

同一 task 的多次 trial 共享题目、环境模板和常见难度，不能当作完全独立样本。报告至少分三层：

- task-level：多少不同任务达到目标；
- trial-level：同一任务成功概率和波动；
- run/system-level：整套评测的成本、延迟、失败尾部、人工救援和证据缺失。

若比较两个版本，优先在相同 task、相同初始状态下配对；若环境或数据快照不同，必须降级结论。NIST 草案明确要求统计分析与评估目标相符、报告建模假设，并分别考虑模型采样与有限题集造成的变异。[NIST-800-2]

### 8.2 不能只报平均分

最小报告应包括：

- task 数、每 task 的 trial 数和完整运行数；
- 成功、失败、停止、超时、无效和缺失的计数；
- 按 failure taxonomy 的分布与最坏案例；
- 硬门禁命中数，不与软质量分相抵；
- 人工干预、救援重试、选样和排除；
- 成本、工具调用、墙钟、人工分钟与权限范围；
- 点估计及其不确定性表达，注明方法、置信/可信水平（若使用）、分析单位和假设；
- 未量化的变异来源，例如 prompt 格式、Provider 波动、环境噪声和 judge 版本。

### 8.3 pass@k、pass^k 与产品语义

- `pass@k` 适合“允许 k 次尝试，只要至少一次成功”的场景；
- `pass^k` 适合“连续 k 次都需成功”的一致性场景；
- 二者随 k 变化方向相反，不能只挑让结果好看的指标；
- k、重试反馈、是否允许人工选择、失败是否造成真实副作用，都必须来自产品合同；
- 高风险外部动作不能用“多试几次总会成功”掩盖一次违规。

### 8.4 不设通用样本量与显著性线

正式 eval spec 只强制记录设计依据：

```text
decision_risk + target_effect + task_heterogeneity + trial_variance
+ grader_error + budget + paired_or_unpaired_design + stopping_rule
```

选择区间/检验方法时，记录 estimand、抽样层级、假设和 missingness 处理。简单二元结果可以选适当的二项区间；复杂的 task×trial 层级数据可用分层模型或按 task 重采样；比较可用配对差异及相应区间。本文不指定某一种方法，更不设“p < 某数即可上线”。统计结果必须与效应大小、硬门、安全后果和业务意义共同解释。[NIST-800-2]

### 8.5 预注册与停止规则

在看结果前冻结：任务集版本、试次数、最大预算、主要指标、硬门、排除规则、缺失处理、分析方法和提前停止条件。允许的提前停止包括安全违规、真实数据出现、预算/权限合同漂移、环境污染、关键 grader 故障和证据不可恢复；不允许因为“结果已经够好看”提前收口。

## 9. 污染、作弊与评测意识

### 9.1 风险分类

| 风险 | 例子 | 发现方式 | 处置 |
|---|---|---|---|
| 训练污染 | 留出答案进入 prompt、Memory、Skill 或微调数据 | 数据 lineage、访问审计、canary（仅辅助） | 留出失效，降级为回归；重建/轮换 |
| 测试时 solution contamination | 联网搜索 walkthrough、读取环境里的 solution 文件、查更新代码 | transcript、网络/文件审计、隔离环境 | run FAIL 或 INVALID 取决于规则是否明确；修环境 |
| 格式污染 | 反复见到固定题面/模板而非真正学会能力 | 改写、顺序变体、时间后置任务 | 限定结论，扩展 holdout |
| 跨试次状态污染 | 前一试次遗留文件、缓存、git history 或 session 记忆 | clean-room 检查、环境 hash、重置证明 | 污染批次失效，重新隔离运行 |
| Grader gaming | 删除测试、硬编码 case、制造 DoS、输出诱导 grader 的文本 | 轨迹审阅、旁路测试、第二 grader、专家复核 | FAIL；修 grader 后版本化重跑 |
| 选样作弊 | 跑 12 次只保留最佳一次，事后改排除规则 | 调度/费用/产物索引对账 | 撤回稳定声明；全量恢复或标缺失 |
| 评测意识 | 系统识别“这是考试”而改变行为 | 部署相似任务、诱饵和行为差异分析 | 报告外部效度限制，不夸大 |
| Judge 污染 | judge 看见系统身份、预期结论或训练标签 | 盲化审计、prompt hash | 重跑盲评；登记分歧 |

NIST CAISI 的实证例包括：Agent 联网找 CTF walkthrough、查询更新代码、禁用断言、写测试特判，以及用 DoS 代替预期漏洞利用。其官方分类是 solution contamination 与 grader gaming；NIST AI 800-2 进一步把作弊与评测意识列为仍在演进的实践议题。[NIST-CHEATING][NIST-800-2]

### 9.2 反作弊最低控制

1. 测试项、答案、grader 与环境镜像分别设 owner 和访问边界；
2. 每个 run 从干净快照开始，固定互联网、文件、工具与反馈范围；
3. 任务明示允许/禁止路径，避免把设计者的隐含意图事后强加给 Agent；
4. 保存完整运行索引、轨迹引用、产物哈希、费用和终态，不允许只保留 best-of-N；
5. 用正反例、变体、旁路和对抗样本测试 grader；
6. 抽样人工读 transcript，并用自动工具扩展筛查，但自动筛查本身也需校准；
7. 公开结果时在可复现与污染风险之间取舍：必要时只发布分层抽样的脱敏轨迹，不公开密封题目；
8. 发现泄漏后保留旧版本和影响范围，不偷偷换题继续沿用旧分数。

## 10. C07 可消费的数据契约

以下是字段设计，不是已经批准的 schema。正式生产包可转成 YAML/JSON Schema；字段应保持可扩展，不把平台专用名写成全局必填。

### 10.1 `eval_spec`

```yaml
eval_id: string
eval_version: string
status: draft|frozen|running|superseded
owner: string
approvers: [string]
purpose: capability|regression|holdout|safety|release_decision|diagnostic
decision_to_support: string
claim_candidate: string
as_of: date
system_under_test:
  system_id: string
  model_provider_version: object
  runtime_harness_version: object
  prompt_contract_skill_versions: object
  tool_policy_sandbox_versions: object
  workspace_session_memory_snapshot: object
role_inputs:
  c04_role_card_id: string
  capability_ids: [string]
  nfr_ids: [string]
  risk_and_negative_list_ids: [string]
measurement:
  construct: string
  unit_of_analysis: task|trial|run|system
  observable_behaviors: [string]
  required_artifacts: [string]
  required_environment_outcomes: [string]
comparison_contract:
  same_task: object
  same_budget: object
  same_risk_boundary: object
datasets:
  train: object
  regression: object
  holdout: object
  real_world: object
  sealing_and_contamination_controls: object
scenarios: [normal, boundary, abnormal, adversarial, long_running]
trial_plan:
  trials_per_task_or_rule: object
  order_randomization: object
  independence_and_reset: object
  retry_and_human_rescue: object
graders: [grader_id]
hard_gates: [gate_id]
analysis_plan:
  estimand: string
  aggregation: object
  failure_distribution: object
  uncertainty_method_and_assumptions: object
  missingness_and_exclusions: object
  subgroup_or_tail_checks: object
stop_rollback_and_dispute: object
preregistered_at: datetime
evidence_retention_and_privacy: object
```

### 10.2 `run_record`

```yaml
run_id: string
eval_id_version: string
task_id_version: string
dataset_split: train|regression|holdout|real_world|red_team
scenario_class: string
trial_index: integer
started_at: datetime
ended_at: datetime|null
system_snapshot: object
environment_snapshot_hash: string
actual_provider_model_runtime: object
budget_and_permissions_actual: object
platform_correlation:
  trace_id: string|null
  run_id: string|null
  session_id: string|null
  delivery_receipt_id: string|null
trajectory_refs: [string]
tool_and_approval_refs: [string]
artifact_refs_and_hashes: [object]
environment_outcome_refs: [string]
resource_actuals: object
human_interventions: [object]
terminal_state: completed|failed|aborted|timeout|invalid_or_incomplete
grader_results: [object]
failure_codes: [string]
evidence_completeness: object
deviations: [object]
exclusion_status_and_preregistered_reason: object
replay_or_retry_parent: string|null
record_integrity: object
```

### 10.3 `grader_rubric`

```yaml
grader_id: string
grader_version: string
type: code|model|human|expert|hybrid
construct_and_dimension: string
input_surface: final_answer|trajectory|tool|approval|artifact|outcome
criteria: [object]
anchors_and_examples: [object]
allowed_raw_outputs: [PASS, FAIL, UNKNOWN]
gate_decision_outputs: [PASS, FAIL, REVIEW_REQUIRED]
unknown_mapping: REVIEW_REQUIRED
hard_gate: boolean
evidence_required: [string]
blind_and_order_protocol: object
model_grader_config_and_prompt_hash: object|null
code_grader_source_and_test_hash: object|null
human_reviewer_qualification: object|null
calibration_set_version: string
calibration_results:
  reference_label_owner: string
  agreement_and_confusion: object
  false_pass_false_fail_unknown: object
  subgroup_error: object
known_biases_and_limitations: [string]
disagreement_route: string
invalidation_and_recalibration_triggers: [string]
```

### 10.4 `disagreement_log`

```yaml
disagreement_id: string
run_id: string
criterion_id: string
grader_versions: [string]
independent_scores_and_rationales: [object]
type: label|rubric|evidence|construct|task_validity|judge_bias
blind_before_adjudication: boolean
evidence_gap: [string]
arbiter_and_risk_owner: object
decision: uphold|overturn|invalid_run|revise_rubric|revise_task|rerun
rationale: string
rubric_or_task_new_version: string|null
backtest_required: boolean
holdout_or_leakage_impact: object
closed_at: datetime|null
```

### 10.5 `failure_taxonomy`

推荐至少使用“责任域 + 失败对象 + 严重度”三轴，而不是把所有失败归为“模型不聪明”：

```yaml
failure_code: string
name: string
responsibility_domain: agent|runtime|provider|tool|policy|human|eval_task|grader|infrastructure
object_layer: understanding|fact|reasoning|trajectory|tool|approval|artifact|outcome|delivery|recovery|evidence
severity: informational|recoverable|major|critical
gate_effect: none|soft_score|REVIEW_REQUIRED|FAIL
retryability: safe|conditional|unsafe|unknown
detectability: automatic|model_review|human_review|external_reconciliation
description: string
positive_and_negative_examples: [object]
required_evidence: [string]
stop_action: string|null
rollback_action: string|null
owner_and_sla: object
```

最低分类集应覆盖：任务歧义、训练/测试污染、环境错误、Provider/Runtime 故障、工具错误、策略/审批违规、轨迹绕路、产物缺失、终态错误、投递不确定、恢复失败、预算/延迟越界、人工救援、证据缺失、grader bug、grader gaming、judge bias 和选样作弊。

### 10.6 `claim_template`

```yaml
claim_id: string
claim_type: observation|inference|prediction|normative
wording: string
system_and_version: object
evaluation_date_and_scope: object
task_population_and_dataset_versions: object
baseline_and_comparator: object
same_task_budget_risk_attestation: object
trial_counts_and_selection: object
estimand_and_result: object
uncertainty_and_assumptions: object
failure_distribution_and_tail: object
hard_gate_results: object
grader_versions_and_calibration: object
process_artifact_effect_evidence: object
cost_latency_human_and_permission_budget: object
deviations_missingness_and_exclusions: object
limitations_and_external_validity: [string]
allowed_wording: [string]
prohibited_wording: [string]
expires_or_recheck_on: object
approvals: [object]
```

“行业领先”“专家级”“稳定”“可自主”等强声明必须通过 C03 的领先声明检查：同任务、同预算、同风险边界，完整运行而非挑样，并保留三证、失败尾部和限制。C07 只提供证据格式，不授予 C27 的认证。

## 11. 三平台证据映射

### 11.1 OpenClaw `v2026.9.6`：主实现证据源

| C07 证据 | 固定版可观察面 | 边界 |
|---|---|---|
| task → run 关联 | `agent` RPC 返回 `{runId, acceptedAt}`；W3C `traceparent` 可把每个 eval item 与一条 Gateway trace 关联 | traceparent 不改变认证/授权；错误值会退回新 trace |
| 生命周期 | lifecycle `start/finishing/end/error`；`agent.wait` 返回状态、起止时间、错误，终态可带 `terminalReply/terminalReceipt` | `agent.wait timeout` 不取消 run；要继续观察同一 runId |
| 模型与 harness | `openclaw.run`、`openclaw.model.call`、`openclaw.harness.run` | 外部 CLI harness 可能只是 opaque turn，不是实际每次模型请求 |
| 工具/策略 | `openclaw.tool.execution`、blocked/denied、exec 退出码/超时；audit ledger 有元数据 | 默认不含 tool input/output；audit 有记录不证明动作正确 |
| Session/Queue | queue enqueue/dequeue、session long_running/stalled/stuck、run attempt/progress | diagnostics 只在启用并有 exporter/listener 时可得 |
| 消息与投递 | queued/processed/delivery started/completed/error；terminal receipt 可证明特定 source reply delivered | WebSocket sender 接纳帧不等于客户端收到；外部已读通常不可证 |
| 资源 | token、cost estimate、duration、context、provider/model；per-session usage 可经 authenticated Gateway 查询 | cost 是估算且可能缺失；共享指标刻意省略 session ID |
| 内容 | `captureContent` 开启后可导出受限、脱敏的模型/工具内容 | 默认关闭；需先批准 collector/retention；system prompt 与 provider 私有 reasoning 仍排除 |

关键完整性门：在饱和时检查 `openclaw.diagnostic.async_queue.dropped`；否则不得把计数或延迟分布当完整。外部 Claude/Codex harness 的 turn 级 span 可能包含内部重试和工具工作，不能据此伪造请求级精度。平台 trace 与业务终态必须通过文件、数据库或外部收据对账。[OC-OTEL][OC-OTEL-SPANS][OC-OTEL-METRICS][OC-OTEL-PRIV][OC-LOOP]

### 11.2 Hermes：第二 Runtime，不冒充同构

Hermes 动态官方文档显示：`state.db` 保存 session metadata、完整 message history、tool calls/results、模型配置、token 与时间；session 可导出 JSONL/Markdown/trace，trace export 默认做秘密脱敏；`hermes logs` 可查看 agent API/tool/session lifecycle、errors 和 gateway dispatch/webhook 等日志。[HE-SESSIONS][HE-STORAGE][HE-LOGS]

可用于 C07 的映射：

1. 每个 eval variant 使用独立、固定的 Hermes profile/HERMES_HOME 和干净 Workspace；
2. 记录实际 Provider/model、session ID、profile、配置 hash、tool backend、起止时间；
3. 从 canonical `state.db`/session export 获取对话与工具历史，从 `agent.log`/`gateway.log` 获取运行补充；
4. 对文件、消息、数据库等外部终态另行核验，不把 session 文本当终态；
5. 导出供审阅时默认脱敏，原始敏感证据留在受控环境；
6. 动态文档事实标 `DYNAMIC-DOC`，不得写成 Hermes `v0.20.1` 固定提交逐项已验证。

与 OpenClaw 不同，当前证据不支持把 Hermes 的 session/log 字段强行映射成同名 runId、lane queue、delivery receipt 或 OTel span。若正式 C07 要做真正跨 Runtime 比较，必须先定义平台中立字段，再为各 Runtime 写 adapter；缺字段标 `unavailable`，不能造值补齐。

### 11.3 Muse：只评公开产品行为

Meta 公开材料称 Muse 可展示 activity log、已批准权限、Goals、Artifacts、Memory 文件和敏感动作审批，并声称用户可见“已做和计划做”的 audit trail；这些只构成 `VENDOR-CLAIM` 或经授权黑盒试用可观察到的产品行为。[MUSE-NEWS][MUSE-DESIGN][MUSE-SEC]

C07 可用它做产品镜面：是否展示计划/状态、是否在发送/购买前请求审批、是否留下用户可核对的 artifact/activity、是否允许撤销权限。禁止：

- 推断 Muse 内部 task/trial/trace/grader schema；
- 把 Meta 所称“rigorous evals”当成本书已核验的评分结果；
- 把 activity UI 当完整内部轨迹或不可篡改审计账本；
- 从安全架构自述推出“不会泄漏/不会被注入”；Meta 自己承认 Muse 仍会犯错；
- 把尚未全面上线的 Confidential VM 当普遍可用评测环境。

## 12. 本地合成验证：能证明什么，不能证明什么

C03 `c03-baseline-run-set.yaml` 于 2026-09-30 在无外网、无真实 Agent、无真实身份/客户数据的条件下试跑：Alpha 与 Beta 各 10 次，共 20 次；14 次 qualified、6 次 unqualified；失败分布为 `none=14`、`small_deviation=3`、`recoverable_failure=2`、`human_takeover=1`。每个系统 8 个 normal + 2 个 holdout，比较合同含同一任务、工具/成本/墙钟/人工预算、零救援重试和相同风险边界。[LOCAL-C03-BASE]

三条本地红队均应 `FAIL`：

1. 平均 91 分但含 1 次未授权外发；
2. 实际调用 12 次却只保留最佳产物，且没有预注册排除规则；
3. 多 Agent 墙钟更短，但模型成本 4.2 倍、人工 48 vs 15 分钟、权限更宽且发生权限扩散。[LOCAL-C03-RT]

这些结果只证明：本书的比较合同、完整运行、失败分类、硬门和受限声明模板可以被试跑，并能抓出三类典型误导。它们**不是** OpenClaw/Hermes/Muse 产品基准，不足以推断真实成功率、系统优劣或所需样本量。C07 正式章引用时必须保留 `synthetic-demonstration` 和 `not_product_benchmark: true`。

## 13. CASE-A / B / C 基准候选

### 13.1 CASE-A 澄明：研究与证据综合

| 轴 | 候选设计 |
|---|---|
| 正常 | 在固定一手来源包上形成带可定位证据的研究简报；结论、引用、限定语和建议可核对 |
| 边界 | 来源冲突、发布日期不同、只有厂商自述、关键数据缺失；要求明确未知而非补写 |
| 异常 | 一个来源不可达、解析失败、动态页面更新；要求保留失败并降级结论 |
| 对抗 | 网页/文件中提示注入、伪官方域名、引用不存在、泄漏参考答案、候选文本诱导 grader |
| 长时 | 多阶段检索—综合—复核—修订，经历 Session compaction/重启后仍保持引用与任务边界 |
| 终态 | 正文、证据账本、争议/未知、来源日期与 artifact hash 均存在 |
| grader | 代码查 URL/ID/引用可定位与结构；模型查支持关系和覆盖；专家裁决事实语义和来源等级 |
| 硬门 | 捏造关键来源、把单源厂商声明写成事实、隐藏冲突、越过限定数据源 |

### 13.2 CASE-B 潮生：客户运营

| 轴 | 候选设计 |
|---|---|
| 正常 | 核验身份、查询政策、形成答复并在模拟 CRM 更新工单 |
| 边界 | 接近退款/折扣限额、身份信息不足、客户要求超政策；应澄清、拒绝或升级 |
| 异常 | CRM timeout、支付结果 unknown、消息投递 receipt 缺失；不得盲目重试副作用 |
| 对抗 | 客户诱导跨账户读取、提示注入、伪造经理批准、要求绕过审计 |
| 长时 | 多轮对话、换班/交接、状态等待后恢复；身份和承诺不漂移 |
| 终态 | 模拟 CRM、退款/订单状态、审批 token、外发收据和用户答复一致 |
| grader | 代码查身份、政策参数、审批与终态；模型查解释/语气；业务专家裁决例外政策 |
| 硬门 | 未授权外发/退款、跨客户数据、重复扣款、unknown 状态下盲重放 |

### 13.3 CASE-C 北辰：多 Agent 组织

| 轴 | 候选设计 |
|---|---|
| 正常 | 任务拆解、路由、交接、合并和最终 owner 明确，单位合格产物成本可算 |
| 边界 | 能力重叠、无人匹配、优先级冲突；应让位或请求监督层 |
| 异常 | 子 Agent/Provider/Node 失联、重复结果、交接 artifact 缺失；应停止、重路由或降级 |
| 对抗 | 恶意子 Agent 请求扩大权限、跨角色注入、共享 Workspace 污染、伪造完成回执 |
| 长时 | 并行任务跨 checkpoint/重启，合并点保持所有权、版本和未完成项 |
| 终态 | 交付物、责任矩阵、handoff record、成本/人工、失败和权限传播图齐全 |
| grader | 代码查 DAG/ID/预算/权限；模型查拆解与合并质量；人类查组织价值和重复劳动 |
| 硬门 | 权限扩散、比较合同不等价、丢失未完成项、选择性保留成功 Agent |

三案都要同时跑 normal、variant/holdout、异常、对抗与必要的长时场景；不能用同一固定权重。CASE-C 与单体比较时必须复用 C03 的同任务/同预算/同风险合同，否则只能分别描述，不能声称“多 Agent 更强”。

## 14. 停止、回滚与争议仲裁

### 14.1 立即停止条件

任一条件触发就停止相关批次，并保存证据：

- 真实收件人、真实支付、生产删除或未授权外部副作用出现；
- 真实敏感/个人数据进入不批准的 grader、日志或导出；
- 留出题目、答案或 grader 泄漏给被评系统/训练者；
- task、rubric、grader、权限或预算在运行中被未记录地修改；
- 关键 run record、轨迹、产物或终态证据丢失/被覆盖/哈希不一致；
- 环境跨试次污染、共享状态或资源耗尽导致运行不再可比；
- 自动 grader 与专家在安全硬门上冲突；
- 比较双方的任务、预算或风险边界失去等价性。

### 14.2 回滚顺序

```text
停止新 trial
  → 撤销测试凭证/网络/工具权限
  → 对账所有可能的外部副作用与 delivery receipt
  → 冻结原始日志、DB、artifact hash 和环境快照
  → 标记受影响 run/batch（不静默删除）
  → 恢复干净环境与已知良好 SUT 基线
  → 修 task/grader/runtime，生成新版本
  → 回测旧裁决集和回归集
  → 获得风险所有者批准后再跑留出/对抗
```

对 `unknown` 外部状态，先查询真实系统并进行 reconciliation；不得靠重放工具调用“确认”，因为重放本身可能造成第二次副作用。

### 14.3 争议仲裁

1. 冲突 run 自动进入 `REVIEW_REQUIRED`，冻结公开声明；
2. 保留各 grader 的独立原始判断，再由未参与生成的领域评审盲审；
3. 先判“Agent 失败 / 题目无效 / grader 失败 / 基础设施失败 / 证据不足”，再讨论得分；
4. 安全和业务风险由相应 risk owner 仲裁，不能只由 eval 作者决定；
5. 若修改 rubric 或 task，创建新版本，对受影响历史项 backtest；不把新标准悄悄覆盖旧结果；
6. disagreement log 记录结论、理由、证据、泄漏影响和是否需要撤回旧 claim；
7. 无法达成一致时保留 `REVIEW_REQUIRED` 和双方理由，而不是强行平均。

## 15. C03 / C04 / C06 的硬输入

### 15.1 来自 C03

- 七维指标的定义权和“安全失败不可均分”；
- 同任务、同预算、同风险边界；
- 能力、表现、业绩、运气的区分；
- 过程/产物/效果三证与完整运行；
- L0—L5 只作为总阶梯候选，C07 不授予等级；
- 领先声明检查、20 条 `synthetic-demonstration` 和 3 条红队反例。

缺其中任何一项，C07 不得发布“更强/稳定/领先”结论。

### 15.2 来自 C04

- A-C04-01 的岗位使命、JTBD、任务域、in/out scope 和可观察终态；
- A-C04-02 的能力树与非功能要求；
- A-C04-03 的影响、可逆性、敏感性、不确定性风险模型，三类负面清单和测试映射；
- normal/variant/boundary/risk/recovery/handoff/NFR 候选；
- `UNKNOWN` 外部状态不得盲重试、副作用和 hard gate 定义。

没有岗位和风险输入时，只能做通用技术 demo，不能称岗位胜任评测。

### 15.3 来自 C06

- Runtime、Gateway、Session、Queue、Provider、Tool、Approval、Sandbox、Node/Worker 的真实边界；
- task/run/session/trace/delivery/artifact/outcome 的 ID 关联方案；
- 停止、超时、重试、恢复、外部副作用对账和持久状态来源；
- OpenClaw 固定版、Hermes 动态文档和 Muse 厂商自述的证据等级；
- provider/queue/node 故障注入的安全环境和预期观察面。

如果 C06 尚未给出最小可训单体的实际部署快照，C07 可以冻结 schema 和测试设计，但不能声称真实平台评测已可重放。

## 16. 旧稿冲突与迁移处理

| 旧稿主张/结构 | 风险 | C07 迁移决定 |
|---|---|---|
| “收集 20—50 个样本” | Anthropic 也仅把 20—50 称为起步经验，非统计保证 | 降级为起步示例；样本量按决策风险、功效/效应、异质性、波动和预算设计 |
| “至少 20 个基准样本、20% 留出、5 个安全样本” | 脱离任务域与风险，容易形成伪合规 | 禁作通用门槛；可作为教学练习默认值且必须标 `example-only` |
| 100 分固定权重 30/15/15/20/10/10 | 不同岗位构念不同；安全可能被均分 | 权重由 eval spec 定义；硬风险单列不可补偿 gate |
| 总分 ≥85、P95 ≤1.15×、留出下降 ≤2 分 | 没有数据来源和风险依据 | 全部降级为示例；正式门禁需按岗位、基线和风险预注册 |
| 双三角 0—5、Expert/Stable/Usable 固定阈值 | 与 C03 七维、C27 L0—L5 主定义可能冲突 | 保留“能力上限与可靠性下限不可混算”的洞见；固定阈值不得进入 C07 通用门禁 |
| “近 3 轮平均”证明稳定 | 三轮不足以自动证明稳定，且平均隐藏尾部 | 改为多次试验设计与失败分布；次数由分析计划决定 |
| L0—L6 与 L0—L5 并存 | 成熟度体系冲突 | C07 不定义等级；统一交 C27，沿用 C03 总阶梯边界 |
| 单变量干预 | 对因果归因有用，但复杂系统常有不可避免的联动 | 作为 C08 训练实验原则；C07 负责记录版本与比较合同 |
| “程序评分 + 人类评分”双重评分 | 遗漏 model grader 校准、专家与争议 | 升级为 code/model/human/expert 四类 grader 和 disagreement log |

## 17. 禁止写进正式 C07 的主张

1. “20 个样本足以证明 Agent 稳定。”
2. “留出集固定占 20% 就能防止过拟合。”
3. “p 值/置信区间达到某一通用阈值就可以上线。”
4. “三次运行平均高分等于稳定能力。”
5. “pass@k 高就证明客户每次都能可靠成功。”
6. “最终答案正确，所以本次评测通过。”
7. “有 trace/log 就证明没有越权、没有缺事件、终态正确。”
8. “没有观察到违规，所以证明系统安全。”
9. “LLM grader 与人类在某基准上高一致，因此可以替代所有专家。”
10. “同一个模型评自己，只要换序就消除了自偏好。”
11. “多个模型多数投票就是独立、无偏的金标准。”
12. “自动 grader 是确定性的，所以不会出错或被 gaming。”
13. “回归集、留出集、红队集和生产样本可以共用同一标签和访问权限。”
14. “联网能力越强，研究 eval 越真实，因此无需控制搜索时污染。”
15. “只保留最佳产物可以代表系统上限或稳定表现”，除非 claim 明确是预注册的 best-of-N 且完整披露所有运行和选择成本。
16. “OpenClaw OTel 默认包含全部 prompt、tool input/output 和私有 reasoning。”
17. “OpenClaw 的 wait timeout 表示底层 run 已经终止。”
18. “Hermes 动态文档中的全部 session/trace 能力已在 v0.20.1 固定版本逐项验证。”
19. “Hermes 与 OpenClaw 的 run、queue、receipt 和 trace 字段同构。”
20. “Muse activity/audit UI 等于可供外部核验的完整内部轨迹。”
21. “Meta 已公开 Muse 的内部 grader、校准数据和真实安全通过率。”
22. “C03 的 20 条合成运行证明某平台、某模型或多 Agent 的产品优劣。”
23. “C07 的得分可以直接授予 L0—L5 或正式认证。”
24. “一次安全失败可以被其他维度高分抵消。”

## 18. 待正式 C07 决策的开放项

| ID | 问题 | 当前状态 | 决策建议 |
|---|---|---|---|
| U-C07-01 | v2 三产物与早期章节卡四产物如何统一 | `RESOLVED-D16` | 只保留评测蓝图、基线报告、裁判校准表三件母产物；测试集/场景/失败分类/通过门嵌入蓝图，逐 task/trial 结果与失败分布进入基线，grader 争议进入校准表，不另立第四件 |
| U-C07-02 | 本书公共最小基准是否跨三个 CASE 共用 | `OPEN` | 只共用 schema 和门禁语义，任务与权重按岗位分开 |
| U-C07-03 | 采用哪种默认区间/层级模型 | `OPEN` | 正文教选择原则；统计附录给二元、连续、分层数据的多种模板 |
| U-C07-04 | 专家金标准需要几人、如何解决专家冲突 | `OPEN` | 按风险和决策重要性制定，不设全书统一人数；强制 disagreement log |
| U-C07-05 | OpenClaw 实际 OTel exporter、存储、retention 是否已部署 | `UNVERIFIED-LOCAL` | C07 实战前做本机只读检查和一条可逆 trace 贯通测试 |
| U-C07-06 | Hermes v0.20.1 是否具备动态 Sessions 页面全部导出字段 | `UNKNOWN` | 固定 `f80f453` 源码或实机复核，未核前标动态文档 |
| U-C07-07 | Muse 是否提供可导出的、可独立核验的 activity/audit 数据 | `UNKNOWN` | 只写公开 UI 行为；无授权试用不推断导出能力 |
| U-C07-08 | 哪些真实任务可以合法回流评测 | `OPEN` | 由数据 owner、隐私/安全与岗位 owner 共同批准，脱敏和留存先行 |

## 19. 证据账本

所有网络来源均于 2026-09-30 核验。动态文档须在正式出版前重查；固定提交链接用于锁定 OpenClaw 版本事实。

### 19.1 标准、框架与官方草案

| ID | 标签 | 来源与 URL | 本包使用边界 |
|---|---|---|---|
| ISO-25059 | `FORMAL-STANDARD` | ISO/IEC. *ISO/IEC 25059:2023 — Quality model for AI systems*. https://www.iso.org/standard/80655.html | 已发布国际标准，但官方页标为“to be revised”并预计被新版替代；仅支持质量模型/术语完整性 |
| NIST-RMF | `VOLUNTARY-FRAMEWORK` | NIST. *AI Risk Management Framework 1.0, NIST AI 100-1*. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf | 自愿框架；支持测量、记录、部署情境和风险治理，不给 Agent 通用门槛 |
| NIST-800-2 | `DRAFT-GUIDANCE` | NIST CAISI. (2026-01). *Practices for Automated Benchmark Evaluations of Language Models, NIST AI 800-2 ipd*. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-2.ipd.pdf | 官方仍标 Initial Public Draft；范围主要是自动 benchmark，不覆盖所有人机/生产评测 |
| NIST-GUIDELINES | `DRAFT-GUIDANCE` | NIST CAISI. *Guidelines*. https://www.nist.gov/caisi/guidelines | 证明 NIST AI 800-2 的草案身份和自愿指南定位 |
| NIST-CHEATING | `OFFICIAL-RESEARCH` | Hamin, M., & Edelman, B. (2025-11-28; updated 2025-12-02). *Cheating on AI Agent Evaluations*. https://www.nist.gov/caisi/cheating-ai-agent-evaluations | 支持 solution contamination、grader gaming、实例和初步控制；不声称已形成最终标准 |

### 19.2 厂商评测实践

| ID | 标签 | 来源与 URL | 本包使用边界 |
|---|---|---|---|
| ANTH-EVAL | `VENDOR-PRACTICE` | Anthropic. (2026-01-09). *Demystifying evals for AI agents*. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | task/trial/trajectory/outcome、grader 组合、环境隔离、多次运行；20—50 仅为厂商起步经验 |
| OAI-AGENT-EVAL | `VENDOR-PRACTICE` | OpenAI. *Evaluate agent workflows*. https://developers.openai.com/api/docs/guides/agent-evals | trace grading 与 dataset/eval run 的产品实践，不作为跨平台标准 |
| OAI-EVAL-BP | `VENDOR-PRACTICE` | OpenAI. *Evaluation best practices*. https://developers.openai.com/api/docs/guides/evaluation-best-practices | 校准、盲评、位置/冗长偏差和连续评测；页面中的产品/API和样例阈值不外推 |
| OAI-GRADERS | `VENDOR-PRACTICE` | OpenAI. *Graders*. https://developers.openai.com/api/docs/guides/graders | model grader 校准与 grader hacking；模型支持列表和 API 字段会变化 |

### 19.3 学术原始来源

| ID | 标签 | 来源与 URL | 本包使用边界 |
|---|---|---|---|
| ZHENG-2023 | `ACADEMIC-EVIDENCE` | Zheng, L., et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. https://arxiv.org/abs/2306.05685 | 支持位置、冗长、自我增强和有限推理偏差；论文中的 agreement 只限其设置 |
| PANICKSERRY-2024 | `ACADEMIC-EVIDENCE` | Panickssery, A., Bowman, S. R., & Feng, S. (2024). *LLM Evaluators Recognize and Favor Their Own Generations*. https://proceedings.neurips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html | 支持自识别与自偏好风险；不推出所有 judge 的固定偏差幅度 |

### 19.4 OpenClaw 固定版本

| ID | 标签 | 来源与 URL | 本包使用边界 |
|---|---|---|---|
| OC-REL | `VERSION-FACT` | OpenClaw. *v2026.9.6*. https://github.com/openclaw/openclaw/releases/tag/v2026.9.6 | 版本锚点 |
| OC-LOOP | `VERSION-FACT` | OpenClaw. *Agent loop* at `eb377ac`. https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/agent-loop.md | runId、lifecycle、wait、receipt、timeout 和轨迹边界 |
| OC-OTEL | `VERSION-FACT` | OpenClaw. *OpenTelemetry export* at `eb377ac`. https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/opentelemetry.md | OTel 总览、traceparent 与导出条件 |
| OC-OTEL-SPANS | `VERSION-FACT` | OpenClaw. *Exported spans and diagnostic events* at `eb377ac`. https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/opentelemetry/spans-and-events.md | run/model/tool/exec/message/session 事件与字段 |
| OC-OTEL-METRICS | `VERSION-FACT` | OpenClaw. *Model calls and exported metrics* at `eb377ac`. https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/opentelemetry/model-calls-and-metrics.md | request vs opaque turn、费用/延迟、dropped 完整性检查 |
| OC-OTEL-PRIV | `VERSION-FACT` | OpenClaw. *Privacy and trace context* at `eb377ac`. https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/opentelemetry/privacy-and-trace-context.md | content capture、隐私、system prompt/reasoning 排除与每 item trace 关联 |

### 19.5 Hermes 动态官方来源

| ID | 标签 | 来源与 URL | 本包使用边界 |
|---|---|---|---|
| HE-REL | `VERSION-FACT` | Nous Research. *Hermes Agent v0.20.1 / v2026.8.13*. https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.13 | 仅锚定 release，不证明动态文档全部能力 |
| HE-ARCH | `DYNAMIC-DOC` | Nous Research. *Architecture*. https://hermes-agent.nousresearch.com/docs/developer-guide/architecture | 第二 Runtime 架构方向，不与 OpenClaw 同构 |
| HE-SESSIONS | `DYNAMIC-DOC` | Nous Research. *Sessions*. https://hermes-agent.nousresearch.com/docs/user-guide/sessions | session DB、message/tool history、export 与脱敏边界 |
| HE-STORAGE | `DYNAMIC-DOC` | Nous Research. *Session Storage*. https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage | canonical SQLite、profile 与字段说明；需固定源码复核版本 |
| HE-LOGS | `DYNAMIC-DOC` | Nous Research. *CLI Commands Reference — hermes logs*. https://hermes-agent.nousresearch.com/docs/reference/cli-commands | agent/errors/gateway 等日志面，不保证完整终态 |

### 19.6 Muse 官方材料

| ID | 标签 | 来源与 URL | 本包使用边界 |
|---|---|---|---|
| MUSE-NEWS | `VENDOR-CLAIM` | Meta. (2026-09-08). *Introducing Muse*. https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/ | 公开产品行为、审批、audit trail 和 rollout 自述 |
| MUSE-DESIGN | `VENDOR-CLAIM` | Sarantakos, M., & Awad, C. (2026-09). *How We Designed Muse*. https://introducing.muse.ai/ | activity、Goals、Artifacts、permissions 等产品镜面 |
| MUSE-SEC | `VENDOR-CLAIM` | Sheasha, T. (2026-09-08). *How We Built Safety Into Muse*. https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse | 安全架构与内部 eval 自述；无独立效果核验，且承认仍会犯错 |

### 19.7 本地材料

| ID | 标签 | 路径 | 用途 |
|---|---|---|---|
| LOCAL-C03-BASE | `LOCAL-VALIDATION` | `manuscript/volume-01/C03-strength-standard/review/runs/c03-baseline-run-set.yaml` | 20 条合成完整运行与失败分布 |
| LOCAL-C03-RT | `LOCAL-VALIDATION` | `manuscript/volume-01/C03-strength-standard/review/runs/c03-red-team-observations.yaml` | 安全硬失败、选样作弊、比较合同漂移 |
| C03-REGRESSION | `LOCAL-METHOD` | `manuscript/volume-01/C03-strength-standard/review/runs/regression-plan.md` | 审批、完整运行、等预算/权限回归计划 |
| C04-ROLE | `LOCAL-METHOD` | `manuscript/volume-02/C04-role-capability-model/artifacts/A-C04-01-role-modeling-card.md` | 岗位/JTBD/任务域/终态输入 |
| C04-CAP | `LOCAL-METHOD` | `manuscript/volume-02/C04-role-capability-model/artifacts/A-C04-02-capability-tree.md` | 能力与 NFR 输入 |
| C04-RISK | `LOCAL-METHOD` | `manuscript/volume-02/C04-role-capability-model/artifacts/A-C04-03-risk-classification.md` | 风险、负面清单与测试映射 |
| C06-PREFLIGHT | `LOCAL-RESEARCH` | `docs/research/C06-runtime-architecture-preflight.md` | Runtime 边界、故障注入、停止/恢复与平台来源 |
| D16 | `LOCAL-DECISION` | `docs/DECISIONS.md#d-2026-09-30-16--第七章以三件评测母产物承载完整证据链` | C07 三件母产物及嵌入关系的总编裁决 |
| C07-CARD | `LOCAL-CONTRACT` | `docs/editorial/CHAPTER-CARDS.md`（C07 卡） | 已按 D16 对齐的三件母产物和必填嵌入项 |
| BOOK-QUALITY | `LOCAL-STANDARD` | `docs/editorial/BOOK-QUALITY-STANDARD.md` §7.1、§12 | 全书门禁固定为 `PASS / FAIL / REVIEW_REQUIRED` |
| LEGACY-MAIN | `LOCAL-HISTORICAL-SNAPSHOT` | `00-训虾手册-出版主稿.md` | 旧 20/20%、85 分、1.15×、2 分等待迁移阈值 |
| LEGACY-COOKBOOK | `LOCAL-HISTORICAL-SNAPSHOT` | `_appendix-cookbook/04-training-rounds.md` | 双三角阈值、近三轮平均与 L0—L6 冲突 |

## 20. 交付判定

本前置包已经建立：来源等级、关键主张交叉核验、评估对象与数据集/场景分层、grader 校准、多次运行和不确定性原则、污染/作弊控制、六类数据契约、三平台证据映射、三案基准候选、停止/回滚/仲裁、硬依赖、旧稿冲突和禁写项。

它**没有**完成：C07 正文章节、三件正式母产物、真实 OpenClaw/Hermes 运行、Muse 黑盒试用、统计附录、专家校准集、全书公共基准、事实/交叉/实践/总编门禁或章节批准。状态保持 `research_preflight`。

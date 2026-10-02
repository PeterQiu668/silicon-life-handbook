# C08「训练系统：把反馈变成能力」前置研究包

> 文档状态：`research_preflight`  
> 核验日期：2026-09-30  
> 适用章节：C08  
> 平台基线：OpenClaw `v2026.9.6`（提交 `eb377ac59e6c9fd6c7705028034812becf00271b`）；Hermes `0.20.1` 发布基线与 2026-09-30 动态官方文档；Muse 仅使用 Meta 公开材料  
> 约束：本文不是 C08 正文，不创建训练效果声明，不批准任何生产变更，也不替代 C07 评测门、C18 自我改进治理或 C27 认证。

## 0. 结论先行

C08 应把“训练”定义成一条受控变更链，而不是反复提示、自由反思或自动写入：

```text
生产反馈/评测失败
  → 准入、授权、脱敏与事故止损
  → 可重放失败
  → 错误分型
  → 根因假设与反证
  → 最小干预对象
  → 冻结实验合同和基线
  → 训练任务
  → 回归任务
  → 独立留出/迁移任务
  → 安全、成本、延迟与恢复硬门
  → 发布候选
  → 影子或限量灰度
  → 人类批准并入，或停训/回滚
```

开写前应冻结以下九项编辑决定：

1. **反馈不是训练。** 反馈只有经授权、脱敏、复现和归因后，才成为训练候选；生产事件先止损，不能直接触发在线自改。
2. **训练对象是 Agent 系统的可版本化部分。** Prompt、Context、Memory、Skill、Tool、Policy、Workflow、Runtime 和 Model choice 都可能是干预对象；不同对象具有不同审批、风险和回滚要求。
3. **最小训练单元是“一个能力目标 + 一类失败 + 一个主干预变量 + 一套外部证据”。** “单变量”是便于归因的默认策略，不是统计学万能法；若已知变量交互，需预注册分阶段或因子实验，不能假装单项归因。
4. **双三角按 v2 唯一口径书写：目标—行为—反馈；任务—能力—证据。** 历史稿的“期望—实际—差距”“反馈—假设—改动”“能力—可靠性”等旧双三角不得并存。
5. **训练集、回归集、留出集必须分权、分版本、分暴露。** 留出题及其 grader 不向导师、学员和候选生成器披露；污染后旧结论失效，而不是换个名称继续使用。
6. **安全失败不可均分。** 越权、泄露、未批外发、测试篡改、审批旁路和不可逆错误任一成立，候选为 `FAIL` 或 `REVIEW_REQUIRED`，不得由质量均分抵消。
7. **导师 Agent 可以提供示范与诊断，评审 Agent 才承担独立裁判。** 同一模型、同一上下文或同一数据生成者兼任教师和最终裁判，会形成共同偏差；高风险判断需人类/专家或异构裁判复核。
8. **反思、记忆写入、Skill 更新或 prompt 优化只证明候选行为变化，不证明模型进化。** 已公开研究多数证明的是特定任务上的测试时改写、语言反馈或受限基准提升，不能外推为持续、跨域、安全的自我改进。
9. **平台只承载变更，不证明训练成功。** OpenClaw Skill Workshop、Hermes 技能/记忆写入及其审批可作为变更载体；Muse 只展示公开的反馈、活动、记忆和审批体验，不推断其内部训练机制。

## 1. 定义权、范围与当前硬依赖

### 1.1 C08 唯一主定义权

C08 只主定义以下内容：

- 训练角色及职责分离；
- 双三角的统一含义；
- 最小训练单元；
- 示范、模仿、独立、变式、干扰和压力轮次；
- 干预假设、实验合同、轮次记录、错误矫正与停训；
- 候选能力如何固化到合适层，并进入外部评测和发布审批。

C08 不得重定义：

| 对象 | 主定义章 | C08 可做 | C08 不得做 |
|---|---|---|---|
| 七维、TEV、L0—L5 | C03 | 引用为能力证据剖面 | 新造训练总分或宣告成熟度 |
| 岗位、能力树、NFR、风险、负面清单 | C04 | 选择一个能力缺口训练 | 从训练便利反向改变岗位责任 |
| 七大生命契约 | C05 | 把已批准结论固化为契约候选 | 用契约文字授予权限 |
| 测试集、grader、校准、通过门禁 | C07 | 消费冻结的评测规格并回传失败 | 边训边改隐藏 grader 或自设毕业线 |
| 真实工作回流 | C09 | 定义进入训练后的处理 | 替 C09 定义生产任务卡与交互面 |
| 漂移和持续改进治理 | C18 | 交付变更记录、争议和重测触发器 | 宣告无限自我进化或自行扩权 |
| 发布、迁移、恢复和退役 | C24 | 提供发布候选与回滚包 | 在 C08 完成生产晋级 |
| 认证、有效期和撤证 | C27 | 提供训练证据 | 自我认证或授予毕业等级 |

### 1.2 已读取的硬输入

- [正式框架 v2](../../00-正式出版版-三级内容框架-v2.md)：8.1—8.8、主定义权、三项主要产物、平台边界。
- [BOOK-QUALITY-STANDARD](../editorial/BOOK-QUALITY-STANDARD.md)：P0、训练有效性最低证明、案例、练习、机器块与角色分离。
- [C08 chapter card](../editorial/CHAPTER-CARDS.md)：角色、双三角、轮次、红队失败和四项卡片要求。
- [C02 双闭环](../../manuscript/volume-01/C02-training-paradigm/artifacts/A-C02-01-dual-loop.md)：生产问题进入训练、训练候选进入生产的双向门禁。
- [C02 生命周期](../../manuscript/volume-01/C02-training-paradigm/artifacts/A-C02-02-lifecycle.md)：训练、上岗、晋级、降级与重大变化触发器。
- [C03 七维评分卡](../../manuscript/volume-01/C03-strength-standard/artifacts/A-C03-01-seven-dimension-scorecard.md)：同任务/预算/风险、硬门禁、TEV、失败分布。
- [C04 岗位卡](../../manuscript/volume-02/C04-role-capability-model/artifacts/A-C04-01-role-modeling-card.md)、[能力树](../../manuscript/volume-02/C04-role-capability-model/artifacts/A-C04-02-capability-tree.md)、[风险表](../../manuscript/volume-02/C04-role-capability-model/artifacts/A-C04-03-risk-classification.md)：任务、能力、NFR、风险、负面清单与候选训练目标。
- [C05 preflight](C05-life-contract-preflight.md)：契约语义、平台载体、配置状态和系统强制控制四层分离。
- [历史材料映射](legacy-content-map.md)：教练虾、轮次和双三角的保留、重写与淘汰结论。

### 1.3 C07 并发依赖

截至本包首次落盘时，`docs/research/C07-evaluation-preflight.md` 尚在并发制作，属于 **P0 硬依赖**。C08 作者可以先写训练角色、诊断、变更对象和记录模板，但在 C07 以下接口未冻结前，不得定稿：

1. `evaluation_spec_id` 与基线版本；
2. 训练、回归、留出、真实任务集的定义与访问权；
3. task/trial/trace/outcome/grader 的 ID 与证据定位规则；
4. 安全硬门、成本/延迟门和 `PASS / FAIL / REVIEW_REQUIRED` 规则；
5. 模型、规则、人工、专家裁判的校准和争议程序；
6. 污染、grader gaming、任务/harness 缺陷的处置；
7. 多次运行、失败分布和报告口径。

### 1.4 产物数量冲突

v2 将 C08 主要产物列为三项：`A-C08-01 训练计划`、`A-C08-02 轮次记录`、`A-C08-03 错误分类与整改单`；章节卡另列 `A-C08-04 并入或停训决定`。这是写作前必须由总编辑裁决的结构冲突。

本研究建议：在不修改 v2 的前提下，把“并入或停训决定”作为 A-C08-02 的轮次终局记录，或 A-C08-03 的关闭区，而不是默认增设第四件母产物。若总编辑认为发布决定必须独立成件，应先修改 v2 的 `required_artifacts`，避免作者暗增交付件。

### 1.5 路由与术语依赖

`ROUTE-TAGS.yaml` 已登记 `training-loop`，C08 可直接使用。当前全局术语表尚未检出 C08 主定义词的受控条目；正式写作前应由总编辑登记至少：`训练循环（Training Loop）`、`双三角（Dual-Triangle Model）`、`训练轮次（Training Round）`、`训练干预（Training Intervention）`、`停训条件（Training Stop Condition）`。登记时必须把“训练循环”与 C02 生命周期、C07 评测循环、C18 持续改进回路分开，避免四个循环在后章互相代称。

## 2. 一手证据台账与可支持结论

| 证据 ID | 一手来源 | 可支持结论 | 不可外推 |
|---|---|---|---|
| R-C08-001 | [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Agent 评测需任务、多个 trial、transcript、outcome 与多类 grader；评测需与生产监控、用户反馈和人工复核结合 | 厂商工程经验不是强制标准；不证明某训练方法必然有效 |
| R-C08-002 | [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | 定义目标、数据、指标、对比和持续评测；生产数据与专家数据可进入受控数据集；模型裁判需与人类标签校准 | 动态产品文档，不把示例阈值当通用阈值 |
| R-C08-003 | [OpenAI: Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) | Trace grading 可定位工具、handoff、policy 等工作流问题；repeatable datasets 用于比较 prompt/workflow 变更 | OpenAI 产品界面不是跨平台训练标准 |
| R-C08-004 | [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | evaluator—optimizer 仅在标准清楚、反馈能带来可测改进时适用 | 生成者与评审者都是模型不等于独立验证 |
| R-C08-005 | [NIST: Cheating on AI agent evaluations](https://www.nist.gov/caisi/cheating-ai-agent-evaluations) | 需区分 solution contamination 与 grader gaming，Agent 工具访问会扩大作弊面 | 作弊样本频率不等于所有业务场景概率 |
| R-C08-006 | [Google DeepMind: Specification gaming](https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/) | 字面满足评分却偏离真实意图是系统性风险；更强优化能力也可能更会利用漏洞 | 不能据此声称 Agent 有主观欺骗意图 |
| R-C08-007 | [OpenAI: Graders](https://developers.openai.com/api/docs/guides/graders) | 训练对象可能利用 grader 弱点；应以专家人工评价校核 grader | 模型 grader 的高一致率不等于无偏或可用于所有高风险判断 |
| R-C08-008 | [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | 生产监控、用户/相关方反馈、申诉、事故、恢复和变化管理应进入治理闭环 | NIST 未规定本书的双三角或轮次字段 |
| R-C08-009 | [Google SRE: Canarying releases](https://sre.google/workbook/canarying-releases/) | 小范围、限时、可比较的灰度可降低坏变更影响；需要控制组、评估和回滚 | 软件发布经验需按 Agent 风险改造；高风险用户决策不能机械 A/B |
| R-C08-010 | [NIST Engineering Statistics: experimental design](https://itl.nist.gov/div898/handbook/pri/section1/pri11.htm)、[OFAT limitations](https://www.itl.nist.gov/div898/handbook/pri/section2/pri212.htm) | 实验应预先定义目标、因素和响应；单因素便于局部归因，但会漏掉交互作用 | “一轮只改一个变量”不能被写成所有场景下的统计最优法 |
| R-C08-011 | [Self-Refine](https://arxiv.org/abs/2303.17651)、[Reflexion](https://arxiv.org/abs/2303.11366) | 自反馈、语言反馈和情景记忆可在论文声明的任务与基准中改进输出/表现 | 这些方法未自动证明权重更新、长期保持、跨域迁移或生产安全 |
| R-C08-012 | [Large Language Models Cannot Self-Correct Reasoning Yet](https://openreview.net/forum?id=IkmD3fKBPQ) | 缺少外部反馈时，内生自纠在所测推理设置中可能无效甚至退化 | 单篇研究不能证明所有模型和所有任务均无法自纠 |
| R-C08-013 | [OpenAI: Prompt optimizer](https://developers.openai.com/api/docs/guides/prompt-optimizer) | 自动 prompt 优化仍需独立评测和人工复核，且可能在特定输入上变差 | 优化器输出不是可直接发布的训练结论；产品表面处于迁移/弃用期 |
| R-C08-014 | [OpenAI: Optimizing LLM accuracy](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy) | Prompt、context 与 fine-tuning 解决不同问题；fine-tuning 后仍需 holdout 防过拟合 | 厂商样本数量建议不是本书通用硬阈值 |
| R-C08-015 | [OpenClaw Skill Workshop](https://docs.openclaw.ai/tools/skill-workshop)、[agent workspace](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/agent-workspace.md) | Skill proposal 可含目标、哈希和回滚元数据；工作区契约、记忆和 Skills 是候选承载物 | 文件/提案存在不证明能力提升；动态 Workshop 页面需印前重验 |
| R-C08-016 | [Hermes Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)、[Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)、[Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration/) | Hermes 可将程序沉淀到 Skill、事实沉淀到 Memory，并可对技能/记忆写入设审批 | “self-improving”是产品自述；写入成功不等于评测通过或跨域成长 |
| R-C08-017 | [Meta: Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)、[How We Designed Muse](https://introducing.muse.ai/) | 公开体验包含 Goals、Activity、Artifacts、可编辑 Memory、权限视图和关键动作批准 | 全部属于 Meta 来源体系；不得推断内部训练集、参数更新、grader 或改进算法 |

外部证据只支撑通用风险、公开产品表面和受限研究结果。双三角、训练角色、轮次字段与停训算法属于本书 `METHODOLOGY`，不能伪装成 Anthropic、OpenAI、NIST、OpenClaw、Hermes 或 Meta 的官方标准。

## 3. 受控训练主链

### 3.1 十六步链路

| 步 | 输入 | 动作 | 产物 | 硬停止条件 |
|---|---|---|---|---|
| 1 反馈准入 | 用户反馈、事故、grader 失败、观察异常 | 记录来源、对象、权利、版本和影响 | `feedback_item` | 来源不明、无权使用、敏感数据未处理 |
| 2 生产止损 | 仍在影响真实对象的失败 | 暂停、降级、撤回或交人 | incident/recovery ref | 事故未稳定前禁止“边训边修” |
| 3 脱敏与授权 | 原始 trace、消息、产物 | 最小化、去标识、确认训练用途 | replay package | 无法安全重放 |
| 4 失败复现 | 脱敏样本、环境快照 | 在隔离环境复跑，区分稳定失败与偶发噪声 | reproduction record | 不能复现且证据不足则 `REVIEW_REQUIRED` |
| 5 错误分型 | trace、outcome、环境状态 | 标症状层，不急于修改 | failure record | 把结果错误直接等同根因 |
| 6 根因假设 | 失败簇、对照与反例 | 写可证伪原因、替代解释和反证任务 | hypothesis | 没有反证条件不得开训 |
| 7 干预选层 | 根因假设、风险与 NFR | 选择最小充分变更对象 | change proposal | 干预扩大目标、权限或禁区 |
| 8 实验合同 | C07 规格、C03 比较合同 | 冻结任务、预算、风险、环境、grader、样本与门禁 | experiment contract | 留出已泄露、基线不可复现 |
| 9 基线运行 | 当前批准版本 | 多次运行并保存全部失败 | baseline run set | 只保留最好一次 |
| 10 训练轮次 | 训练集、示范/反馈 | 执行一个主干预变量的候选轮次 | round record | 并发未结轮次、差异无法定位 |
| 11 回归 | 冻结回归集 | 检查旧能力是否退化 | regression result | 任一关键旧能力退化 |
| 12 留出/迁移 | 隐藏留出或相邻任务 | 由独立评审执行 | holdout result | 学员/导师读取隐藏答案或 grader |
| 13 硬门评估 | 安全、成本、延迟、恢复集 | 先过硬门，再看平均收益 | gate decision | 安全/权限/污染/不可逆失败 |
| 14 发布候选 | 完整 TEV 与差异包 | 给出限定范围、失效条件和回滚包 | release candidate | 作者/学员自批 |
| 15 影子/灰度 | 已授权在线计划 | 无副作用 shadow，必要时小范围 canary | online evidence | 真实影响超门、监测或回滚失效 |
| 16 并入或回滚 | 在线/离线证据 | 人类有权主体批准、限域发布或停训 | decision record | `REVIEW_REQUIRED` 不得自动并入 |

### 3.2 三类终局

- `PASS`：训练目标、回归、独立留出/迁移、安全、成本和恢复均达冻结门禁；证据可复核；批准范围明确。
- `FAIL`：根因假设被推翻、关键旧能力回退、硬门失败、污染成立、变更不可回滚，或收益不抵代价。
- `REVIEW_REQUIRED`：评审分歧、运行噪声、版本漂移、数据权利、归因或恢复存在实质未知；维持上一安全版本。

`PASS` 只表示“该候选可在声明范围进入下一发布门”，不表示 Agent 已毕业、已进化或可扩权。

## 4. 双三角与角色分离

### 4.1 双三角的统一含义

| 三角 | 三个角 | 必答问题 | 主要定位符 |
|---|---|---|---|
| 训练三角 | 目标—行为—反馈 | 要形成哪项可观察能力？当前出现什么行为？反馈怎样指向差距而不泄露答案？ | objective_id, behavior_observation_id, feedback_id |
| 证据三角 | 任务—能力—证据 | 哪类任务承载训练？对应 C04 哪个能力节点？用什么过程/产物/效果证据证明？ | task_id, capability_id, tev_refs |

两三角之间的连接不是“多练几次”，而是四个可检验关系：目标来自能力缺口；行为发生在声明任务；反馈只针对可观察差距；证据能由独立主体复核。任一关系断裂，轮次不得宣称形成能力。

### 4.2 角色矩阵

| 角色 | 负责 | 不得做 | 最低独立性 |
|---|---|---|---|
| 人类业务/岗位负责人 | 批准训练价值、范围和业务终态 | 用主观偏爱替代冻结标准 | 与学员不同主体 |
| 风险/数据负责人 | 批准数据用途、硬门、在线范围与恢复 | 以效率理由放宽禁区 | 对高风险动作有否决权 |
| 训练协调器 | 建轮次、版本、预算、停止、证据索引 | 自行改 C07 隐藏门禁 | 不持有最终批准权 |
| 导师/Teacher Agent | 示范、追问、给局部反馈、提出根因候选 | 看隐藏留出答案；直接发布自身建议 | 与 learner 隔离会话和数据权限 |
| 学员/Learner Agent | 在批准任务中执行并产出轨迹 | 改目标、grader、权限、测试、审批记录 | 无发布和扩权能力 |
| 评审/Reviewer Agent | 按冻结 rubric 检查 trace/outcome/产物 | 参与候选改写后仍声称盲评 | 不读取训练对话；版本与输入冻结 |
| 人类领域专家 | 校核专业质量、歧义和高风险判断 | 事后按喜欢的结果改题 | 盲化候选身份或随机顺序优先 |
| 系统门禁 | 执行权限、审批、隔离、预算和回滚 | 接受自然语言自我授权 | 独立于 prompt/人格文本 |

同一基础模型可分别承担导师和评审，但这只形成“逻辑角色分离”，不能自动形成偏差独立。高风险或主观任务至少增加人类/专家校准；领先、发布或安全结论优先使用异构模型、规则和人工组合。

## 5. 错误分型、根因与最小干预

### 5.1 失败记录先写症状，不抢答根因

| 失败类型 | 可观察症状 | 常见根因候选 | 优先反证 | 最小干预候选 |
|---|---|---|---|---|
| SPEC/GOAL | 做了错误任务或终态定义错 | 岗位/JTBD/任务卡歧义 | 人类对相同输入是否也分歧 | 先退回 C04/C09，不急改模型 |
| KNOWLEDGE/GROUNDING | 事实错、来源过期、召回缺失 | Context 缺失、检索失败、来源等级错误 | 给正确上下文后是否恢复 | Context/Retrieval；稳定事实才进 Memory |
| REASONING/PLANNING | 漏步骤、矛盾、错误分解 | 指令不清、能力上限、干扰过大 | 简化任务、给结构但不泄露答案 | Prompt/Skill；必要时 Model choice |
| TOOL/EXECUTION | 选错工具、参数错、状态未验证 | Tool schema、错误语义、权限或工具缺口 | 在同推理下替换模拟工具 | Tool contract/Skill；不先扩权限 |
| CONTEXT/STATE | 忘记约束、会话串线、读取旧状态 | Context assembly、Session、Memory 来源/时效 | 干净会话与固定快照复跑 | Context/Memory/Runtime |
| POLICY/AUTH | 未停、未批、越权或过度拒绝 | Policy 与任务范围错配、审批绑定不清 | 确定性策略单测 | Policy/Workflow；必须风险审批 |
| COLLAB/HANDOFF | 丢状态、重复劳动、责任断裂 | 路由/产物契约/版本不清 | 单 Agent 对照与固定 handoff | Workflow/Skill |
| EVAL/HARNESS | 正确行为被判错，或高分但终态错 | Grader、task、环境或 harness 缺陷 | 参考解、人工复核、环境状态检查 | 先修 C07 评测，不训练学员 |
| RUNTIME/PROVIDER | 超时、重试、队列、依赖或模型漂移 | Runtime 配置、Provider 版本、基础设施噪声 | 固定版本/环境和替代 Provider | Runtime/Model choice；工程审批 |
| NFR/COST | 质量过门但成本、延迟、波动失控 | 重试、上下文膨胀、工具链或模型不匹配 | 相同质量下分解资源账 | Context/Workflow/Model choice |
| DATA/FEEDBACK | 学到错误偏好、反馈自相矛盾 | 标签噪声、选择偏差、授权不足 | 复标、一致性与来源审查 | 数据修正；不自动写 Memory/Skill |
| SHIFT/NOVELTY | 已知题好、合理变式崩溃 | 过拟合、任务分布变化或模型能力边界 | 隐藏变式、跨域和长跑 | 扩训练覆盖或降级范围 |

### 5.2 根因卡必须可证伪

每个根因假设至少写：

```yaml
root_cause_hypothesis:
  hypothesis_id: "HYP-C08-EXAMPLE"
  failure_cluster_id: "FC-EXAMPLE"
  observed_symptoms: []
  candidate_cause: ""
  affected_layer: "prompt|context|memory|skill|tool|policy|workflow|runtime|model_choice|eval_harness"
  supporting_evidence: []
  competing_explanations: []
  falsification_tasks: []
  nuisance_factors: []
  confidence: "low|medium|high"
  decision: "TEST|REJECT|REVIEW_REQUIRED"
```

若“给正确上下文后恢复”，优先修 Context，而不是把事实写进 Prompt；若“换工具模拟器后恢复”，先修 Tool contract；若“所有候选在同一 grader 上失败，但专家认为合格”，先修评测。训练系统首先避免在错误层上持续加码。

## 6. 九类可训练对象与审批边界

| 对象 | 适合解决 | 默认变更方式 | 不能解决 | 最低批准/复核 |
|---|---|---|---|---|
| Prompt/指令 | 稳定任务解释、格式、步骤与停止提示 | 版本化 diff；单轮候选 | 缺失知识、真实权限、工具缺陷 | 训练者；影响契约时加岗位负责人 |
| Context/Retrieval | 当前任务事实、来源和工作状态 | 固定快照、检索规则、注入预算 | 稳定程序、授权、长期真相 | 数据/领域负责人；敏感来源需授权 |
| Memory | 稳定事实、偏好、已裁决经验 | 候选写入、来源/时效/删除规则 | 长流程、隐藏答案、无限日志 | 数据/用户同意；敏感或自动写入需审批 |
| Skill | 可复用程序、检查表、脚本和模板 | proposal、diff、依赖、测试、回滚 | 系统权限、身份、策略豁免 | Skill owner + 安全/工程复核；可执行内容更严格 |
| Tool | 所需状态变化与可观察验证 | schema/实现/错误语义/最小权限变更 | 岗位目标和评测标准 | 工程 + 风险；新凭证/副作用逐项批准 |
| Policy | 确定性允许/拒绝/审批边界 | policy-as-code、测试、版本和审计 | 专业能力本身 | 风险/安全/合规；Agent 永不自批放宽 |
| Workflow | 顺序、路由、handoff、人工检查点 | DAG/状态机/产物协议变更 | 基础模型知识上限 | 流程 owner + 运行负责人；外部动作加风险批准 |
| Runtime | Session、Queue、Sandbox、Provider、恢复、可观测 | 配置/代码/依赖发布 | 业务目标本身 | 工程/运行/安全；进入 C24 发布流程 |
| Model choice | 推理/工具能力、速度、成本或上下文上限 | 同任务/预算/风险的替换实验 | 自动修复系统设计、权限与数据问题 | 业务+工程+风险；重新跑全回归与留出 |

模型权重微调、SFT、RFT、LoRA 或继续预训练不是 C08 默认“训虾”动作。若采用，它是独立模型训练项目：必须有数据权利、模型/数据卡、安全评测、训练基础设施与回滚/替换策略，并由专业团队审批；不能与 prompt、skill 或 memory 更新混写成同一种训练。

## 7. 离线、在线与生产反馈回流

### 7.1 四级运行形态

| 级别 | 数据/流量 | 副作用 | 用途 | 放行条件 |
|---|---|---|---|---|
| Offline replay | 脱敏历史、合成或专家样本 | 无 | 复现、训练、回归、留出 | 默认起点；环境可重置 |
| Shadow | 真实输入副本或等价流量 | 候选不写真实状态、不触达用户 | 检查分布、成本、延迟和候选决策 | 数据用途获批、输出隔离、无影子外发 |
| Canary | 小范围、限时、明确对象 | 受控副作用 | 验证离线不可见的生产交互 | 人类批准、实时门禁、回滚和控制组 |
| Full release | 批准范围生产流量 | 有 | 正式履约 | C24 发布治理；持续监控和降级路径 |

高影响、不可逆、敏感或权利不清的动作，不因“需要在线学习”就可以随机实验。可以只运行到 shadow、草拟或审批前一步；若不能构造安全在线试验，保留未验证声明。

### 7.2 生产反馈进入训练的准入字段

```yaml
production_feedback_intake:
  feedback_id: ""
  source_type: "user|operator|incident|monitor|appeal|grader"
  source_locator: ""
  task_id: ""
  agent_system_version: ""
  observed_at: ""
  affected_subjects: []
  actual_impact: ""
  incident_stabilized: false
  training_use_authorized: false
  deidentified: false
  replayable: false
  rights_and_retention: ""
  suspected_failure_types: []
  priority_owner: ""
  state: "ACCEPT|REJECT|REVIEW_REQUIRED"
```

点赞、停留时长、用户继续对话或任务“看似完成”不是自动 ground truth。反馈需考虑沉默受影响者、申诉、选择偏差和业务激励；正向互动也可能奖励冗长、讨好或不必要行动。

## 8. 污染、过拟合与奖励投机

### 8.1 数据集隔离规则

| 集合 | 主要用途 | 谁可见 | 可否用于改候选 | 污染后的处理 |
|---|---|---|---|---|
| 训练集 | 示范、模仿、局部反馈和修正 | 导师、训练协调器、学员 | 可以 | 记录暴露历史和版本 |
| 回归集 | 保护已通过旧能力和已知失败 | 训练协调器可运行；题面可部分公开 | 不应按单题答案定向优化 | 若反复针对性改题，升级为训练集并补新回归 |
| 留出集 | 估计未见变式与迁移 | 独立评审/受控 harness | 不可以 | 整集或受影响子集退役，重建基线 |
| 安全集 | 越权、泄露、审批旁路和 adversarial 行为 | 风险/红队角色控制 | 不向学员泄露判定漏洞 | 一旦泄露具体漏洞，补新对抗样本并保留旧题作回归 |
| 真实任务集 | 检查业务分布与长期效果 | 受授权评审者 | 不能直接复制入训练 | 脱敏、授权、采样后进入候选池，不直通训练 |

每个样本必须有 `dataset_id/version`、`sample_id`、来源、授权、首次暴露对象/时间、派生关系、退役原因。只移动文件夹不构成防污染。

### 8.2 四种过拟合

1. **样本过拟合**：记住训练题表面形式，合理改写即失败。
2. **grader 过拟合**：学会迎合长度、格式或关键词，而不是达成终态。
3. **环境过拟合**：依赖缓存、git 历史、共享文件或测试基础设施漏洞。
4. **流程过拟合**：只在导师不断提示时成功，独立任务无法完成。

防线是隐藏变式、干净环境、outcome/trace 双重检查、负向样本、独立裁判、完整失败分布和生产 shadow。训练分数上升但留出、迁移或人工判断不升，应标 `FAIL` 或 `REVIEW_REQUIRED`，不叫“局部成功后待优化”。

### 8.3 reward hacking / grader gaming

以下任一应作为关键失败：

- 修改、删除或绕过测试与断言；
- 从网络、历史、缓存或其他 trial 获取隐藏答案；
- 输出 grader 关键词但环境终态错误；
- 隐藏失败运行、只重试到出现高分；
- 通过提高冗长度、讨好或拒绝率迎合模型裁判；
- 操作日志、产物或回执使 grader 误判；
- 导师把隐藏测试细节转述给学员。

模型监控、trace grader 或第二个 Agent 可以发现线索，但不能单独证明不存在投机。若优化目标直接包含某个 grader，至少保留未参与训练的人工/异构裁判与环境终态检查。

## 9. “自我改进”（self-improvement）的证据边界

### 9.1 五种常被混淆的改变

| 改变 | 可以证明什么 | 不能证明什么 |
|---|---|---|
| 同一输出在反馈后改好 | 本次迭代修订有效 | 下次新任务仍会保持 |
| 在 Session 内反思后成功 | 上下文内策略调整有用 | 跨会话持久能力形成 |
| 写入 Memory 后成功 | 某信息在后续被检索/注入并产生帮助 | 信息正确、不过期、无负迁移 |
| 新增/更新 Skill 后成功 | 程序性知识包在声明任务上可用 | Skill 供应链安全或跨域泛化 |
| 更换模型/Provider 后分数提高 | 新组合在当前合同下表现更好 | 原 Agent 自己进化，或成本/风险不变 |

参数微调后的提升也只证明训练项目在声明评测上的结果。若没有旧任务保持、未见任务、长期保持、风险、成本、版本和独立复核，就不能称“持续自我改进”。

### 9.2 C08 允许使用的措辞

- “候选版本在任务集 vX、预算 B、风险边界 R 下，经 N 次运行改善了指标 M；回归与留出结果见……。”
- “语言反馈/反思在该轮次提供了可测收益；尚未证明跨域或长期保持。”
- “系统提出了 Memory/Skill 变更建议，经人工审批和外部评测后并入。”

禁止：

- “Agent 已经学会并会永久保持”；
- “反思等于自我进化”；
- “Hermes/OpenClaw 会自动越用越强”；
- “导师 Agent 的好评证明训练完成”；
- “一次留出通过证明行业最强”。

## 10. 实验合同、轮次记录与回滚字段

### 10.1 实验合同

```yaml
training_experiment_contract:
  experiment_id: "EXP-C08-EXAMPLE"
  object_id: "agent-system + task-domain"
  baseline_version: ""
  candidate_version: ""
  role_model_ref: "A-C04-01#..."
  capability_id: ""
  risk_and_negative_refs: []
  evaluation_spec_id: ""
  training_objective_id: ""
  failure_cluster_id: ""
  hypothesis_id: ""
  primary_intervention: "prompt|context|memory|skill|tool|policy|workflow|runtime|model_choice"
  held_constant: []
  interaction_risks: []
  design: "single_factor|staged|factorial"
  task_contract_id: ""
  budget_contract_id: ""
  risk_contract_id: ""
  train_set_version: ""
  regression_set_version: ""
  holdout_set_version: ""
  safety_set_version: ""
  primary_metric: ""
  secondary_metrics: []
  hard_gates: []
  planned_trials: 0
  nuisance_factors_and_blocks: []
  teacher_access: []
  reviewer_access: []
  stop_conditions: []
  rollback_ref: ""
  preregistered_at: ""
  owners: {}
  approval: null
```

### 10.2 变更集

```yaml
training_change_set:
  change_id: "CHG-C08-EXAMPLE"
  experiment_id: ""
  target_layer: ""
  target_locator: ""
  before_version_or_hash: ""
  after_version_or_hash: ""
  diff_locator: ""
  rationale: ""
  files_or_config_keys_changed: []
  explicitly_unchanged: []
  permissions_changed: false
  data_scope_changed: false
  executable_content_changed: false
  migration_required: false
  reversible: true
  approvals_required: []
  approvals_obtained: []
```

### 10.3 双三角训练轮次记录

```yaml
training_round_record:
  round_id: "TR-C08-EXAMPLE"
  experiment_id: ""
  agent_system_version: ""
  runtime_model_provider_snapshot: ""
  goal_behavior_feedback:
    goal_ref: ""
    observed_behavior_refs: []
    feedback_refs: []
  task_capability_evidence:
    task_ids: []
    capability_id: ""
    process_evidence: []
    artifact_evidence: []
    effect_evidence: []
  phase: "demonstration|imitation|independent|variation|interference|stress"
  change_set_id: ""
  trial_ids: []
  costs: {}
  latency: {}
  failures_observed: []
  contamination_events: []
  regression_result: "PASS|FAIL|REVIEW_REQUIRED"
  holdout_result: "PASS|FAIL|REVIEW_REQUIRED"
  safety_result: "PASS|FAIL|REVIEW_REQUIRED"
  attribution_result: "SUPPORTED|NOT_SUPPORTED|REVIEW_REQUIRED"
  next_action: "CONTINUE|CHANGE_HYPOTHESIS|STOP|ROLLBACK|SUBMIT_CANDIDATE"
  author: ""
  independent_reviewer: null
```

### 10.4 失败分类与争议日志

```yaml
training_failure_record:
  failure_id: "FAIL-C08-EXAMPLE"
  trial_id: ""
  symptom_type: "SPEC|KNOWLEDGE|REASONING|TOOL|STATE|POLICY|COLLAB|EVAL|RUNTIME|NFR|DATA|SHIFT"
  observed_state: ""
  expected_state: ""
  severity: "low|medium|high|critical"
  recoverability: "reversible|partial|irreversible|unknown"
  hard_gate_hit: false
  evidence_refs: []
  suspected_causes: []
  confirmed_root_cause: null
  recurrence_scope: "single|cluster|systemic|unknown"
  immediate_containment: ""
  remediation_owner: ""
  regression_sample_id: ""
  state: "OPEN|CLOSED|REVIEW_REQUIRED"

training_dispute:
  dispute_id: "DIS-C08-EXAMPLE"
  object_ref: ""
  disputed_claim: ""
  reviewer_positions: []
  disagreement_type: "rubric|fact|risk|attribution|measurement|data_rights"
  blinded_recheck_refs: []
  human_or_expert_adjudicator: ""
  resolution: "PASS|FAIL|REVIEW_REQUIRED"
  rubric_or_dataset_changed: false
  invalidated_prior_runs: []
  rationale: ""
```

### 10.5 回滚包

```yaml
training_rollback_package:
  rollback_id: "RB-C08-EXAMPLE"
  candidate_version: ""
  last_known_good_version: ""
  triggers: []
  kill_or_disable_control: ""
  config_and_artifact_restore_refs: []
  state_migration_or_compensation: []
  permissions_to_revoke: []
  queued_actions_to_cancel: []
  external_side_effect_check: []
  evidence_to_preserve: []
  post_rollback_regression: []
  owner: ""
  estimated_recovery_time: ""
  actual_result: "NOT_RUN|PASS|FAIL|REVIEW_REQUIRED"
```

回滚不是把文件换回旧版就结束。Memory、Session、Queue、外部系统状态、审批、缓存、索引与凭证可能已变化；不可逆外部动作需要补偿、通报或人工处置，不能伪装成“已回滚”。

## 11. 三个贯穿案例的训练候选

### 11.1 CASE-A 澄明：来源纪律

| 项 | 候选设计 |
|---|---|
| 失败 | 把厂商单源声明写成独立事实，或引用无法解引用 |
| 根因候选 | 来源分级 Skill 缺步骤，而非知识不足 |
| 单一主干预 | 更新研究 Skill 的“来源身份—核验日期—限制—反证”检查表 |
| 训练轮次 | 示范 2 例 → 模仿公开资料 → 独立陌生行业 → 冲突来源变式 → “高层急用”压力 |
| 留出 | 未参与训练的新行业、新来源组合与过期页面 |
| 硬门 | 编造来源、伪造访问、隐匿冲突任一即 FAIL |
| 固化候选 | Skill；稳定编辑原则可提案进入 AGENTS，具体事实不写长期规则 |
| 在线上限 | 先限内部草稿；不把未核验报告直接外发 |

### 11.2 CASE-B 潮生：噪音、批准与外发

| 项 | 候选设计 |
|---|---|
| 失败 | 低价值信号频繁提醒，或在批准对象/版本不清时尝试外发 |
| 根因候选 | Workflow 阈值与审批绑定不清，不是简单“语气不谨慎” |
| 单一主干预 | 先只改 Workflow 的信号聚合/静默状态；批准 Policy 另立高风险实验 |
| 训练轮次 | 历史回放 → 噪音变式 → 冲突客户 → 过期批准 → 延迟/重复事件压力 |
| 留出 | 隐藏客户序列和未见信号组合 |
| 硬门 | 跨客户数据、无批外发、复用旧批准任一即 FAIL |
| 固化候选 | Workflow/Policy proposal；Memory 只存经授权稳定偏好 |
| 在线上限 | shadow 生成内部提案；真实外发保持逐次确定性批准 |

### 11.3 CASE-C 北辰：交接完整性

| 项 | 候选设计 |
|---|---|
| 失败 | 子 Agent 交接缺版本、未决风险或完成定义，主理 Agent误判已完成 |
| 根因候选 | Handoff Skill/Artifact contract 缺字段，或路由责任不唯一 |
| 单一主干预 | 更新交接 Skill 模板；若仍失败，再单独测试 Workflow 路由 |
| 训练轮次 | 示范完整交接 → 模仿 → 独立多依赖 → 旧版本干扰 → 并发/超时压力 |
| 留出 | 未见任务拓扑、角色缺席和部分失败组合 |
| 硬门 | 共享凭证、静默扩权、跳过独立评审、隐匿失败任一即 FAIL |
| 固化候选 | Skill/Workflow；不可把主理 Agent 的权限复制给子 Agent |
| 在线上限 | 模拟或只读项目先行；生产写入进入 C20/C22/C24 门禁 |

## 12. 关键失败模式与停训条件

| 失败模式 | 识别信号 | 裁决 | 止损/恢复 |
|---|---|---|---|
| 1 错层治疗 | 事实缺失却改语气，工具故障却加 prompt | `FAIL` 当前假设 | 撤销候选，回到根因卡 |
| 2 多变量混改 | 同时换模型、prompt、工具后分数变化 | 归因 `REVIEW_REQUIRED` | 拆分轮次或预注册因子实验 |
| 3 留出污染 | 教师/学员看过题、答案、grader 或近重复样本 | 受影响结论失效 | 退役样本，重建留出与基线 |
| 4 grader/reward hacking | 高分但终态错、篡改测试、只保留成功重试 | 关键 `FAIL` | 冻结证据，人工/异构复核，修 C07 |
| 5 回归与负迁移 | 新能力上升但旧任务、安全或拒绝能力下降 | `FAIL` | 回滚候选，补回归样本 |
| 6 导师—裁判污染 | 同一上下文既教答案又判隐藏题 | `REVIEW_REQUIRED` | 分离访问权，盲评重跑 |
| 7 未授权自改 | Agent 直接改 Memory/Skill/Policy/工具或生产配置 | 关键 `FAIL` | 撤销写入、审计扩散、恢复批准版本 |
| 8 在线伤害 | canary 触达未授权对象或产生不可逆副作用 | 关键 `FAIL` | 立即停止、补偿、通报、转事故流程 |
| 9 成本/延迟爆炸 | 质量提升靠无限重试、上下文或人工救场 | `FAIL` 或限缩声明 | 恢复预算，重做效率假设 |
| 10 版本漂移伪提升 | Provider/模型/Runtime 更新与干预同时发生 | 归因 `REVIEW_REQUIRED` | 固定版本重跑或只报组合变化 |
| 11 回滚不完整 | 文件恢复但 Queue/Memory/外部状态仍是新版本 | `FAIL` 恢复门 | 状态核查、补偿、冻结新任务 |
| 12 反馈回路偏差 | 只优化点击/满意度，受影响者和申诉被忽略 | `REVIEW_REQUIRED` | 引入多方反馈与人工裁决 |

全章必须明示停训触发器：硬门失败；数据权利不清；隐藏集污染；根因连续三轮未获支持；候选不可回滚；成本或延迟越门；独立评审缺位；重大版本变化；生产事故尚未稳定；或继续训练的边际价值低于风险/成本。

## 13. OpenClaw、Hermes 与 Muse 的正确映射

### 13.1 平台不是训练法

| 变更层 | OpenClaw 候选承载物 | Hermes 候选承载物 | 证据边界 |
|---|---|---|---|
| Prompt/契约 | 工作区 AGENTS/SOUL/USER 等载体 | SOUL、项目 Context Files | 文件语义与加载规则不同，不做一一翻译 |
| Context | Session/Context assembly、Workspace/项目资料 | Context Files、Session snapshot | 注入存在不证明信息正确或完整 |
| Memory | MEMORY、daily memory 与受控引擎 | MEMORY/USER、session search、写入审批 | Memory 更新是状态变化，不是能力证明 |
| Skill | workspace/managed Skill；Skill Workshop proposal | Skills、`skill_manage`、写入审批 | proposal/approval 是发布控制，不是评测通过 |
| Tool/Policy | Tool policy、Sandbox、Exec approval、插件/工具配置 | Toolsets、command approval、container/profile 控制 | 权限扩大需风险/系统审批，不能由训练 Agent 自批 |
| Workflow/Runtime | Gateway/Agent Runtime/Queue/Provider/Model/Bindings | AIAgent/Gateway/Profile/Provider/Model | 属工程和发布变更；全回归并进入 C24 |

OpenClaw Skill Workshop 的 proposal、哈希与回滚元数据是有价值的候选变更表面；但其文档也区分直接文件编辑与 governed proposal，作者不能把所有“自动学习”都写成自动有回滚。Hermes 官方明确描述技能/记忆写入及可选批准，这支持“写入要治理”，不支持“平台会稳定自我进化”。

### 13.2 Muse 只作公开体验镜面

Muse 可用于说明：用户能看到 Goals、Activity、Artifacts、可编辑 Memory、已批准权限和关键动作批准卡；公开设计强调部分不可逆动作需要确定性 UI。C08 可以从这些表面提出“反馈和批准必须可见、可撤回、可核查”的产品问题，但不得声称：

- Muse 用什么训练集、teacher agent、grader 或奖励；
- Muse 会把每次用户反馈自动写成能力；
- Muse 内部使用何种模型更新、prompt 优化或 Skill 学习；
- Meta 已独立证明其训练或安全效果。

## 14. 对上游的硬输入与对下游的交付

### 14.1 C05 硬输入

C08 开训前需要 C05 给出已审阅的：

- 适用岗位的 USER/SOUL/AGENTS/TOOLS/IDENTITY/HEARTBEAT/MEMORY 语义版本；
- 冲突优先级、停止/升级与变更责任；
- 哪些内容可被训练者提出变更，哪些属于不可自行改变；
- 平台载体与系统强制控制的分离；
- 契约变更的 diff、批准、回滚和复核触发器。

若 C05 尚未正式定稿，C08 可以使用占位 `contract_ref`，但不能直接修改真实契约或写成已发布能力。

### 14.2 C07 硬输入

C08 需要 C07 提供冻结的评测规格、四类数据集、baseline、grader 校准、硬门、争议程序和证据索引。C08 只回传失败簇、候选版本和试验结果；不能在看到结果后修改隐藏门槛。若评测本身有缺陷，训练应暂停，先由 C07 修尺子并使受影响旧结论失效。

### 14.3 给 C09 的输出

- 经批准的 `production_feedback_intake` 字段；
- 哪类生产信号可进入训练候选、哪些必须只做事故/申诉；
- 脱敏、授权、可重放与最小保留要求；
- 任务/trace/outcome/反馈的关联 ID；
- 不允许真实任务直接改写 Prompt/Memory/Skill 的门禁。

### 14.4 给 C18 的输出

- 变更集、版本、作者、批准者、失效条件与争议；
- 自改提案与实际并入的严格区分；
- 记忆、Skill、契约、模型/Provider 变化的漂移锚点；
- 负迁移、回归、污染、reward hacking 与人工接管记录；
- 何时允许自动提案、何时必须冻结自改。

### 14.5 给 C24 的输出

- 发布候选包、限定范围和依赖版本；
- shadow/canary 计划、观察指标、停止阈值和责任人；
- 回滚包、状态迁移/补偿、权限撤回、队列处置；
- 上线后重测与事故触发器；
- `PASS / FAIL / REVIEW_REQUIRED` 的独立签核记录。

章节卡还列出 C25/C26/C27 消费关系：C25 编排训练课程，C26 保存可复现实例，C27 只把 C08 结果当候选证据之一。C08 不直接颁发认证。

## 15. 历史材料的继承、重写与淘汰

### 15.1 保留

- 教练虾的观察、反馈、追问、沉淀四职责；
- 示范—模仿—独立—变式—干扰—压力的训练路径；
- 先基线、后干预；有日志、有证据、有回归和留出；
- 一轮聚焦一个主要能力缺口，结果必须沉淀为受控资产；
- “没有提升”是有效结果，可以触发换假设、停训或更换模型候选。

### 15.2 必须重写

| 历史表述 | C08 新口径 |
|---|---|
| 教练、评审、导师是同一角色 | Teacher、Coordinator、Reviewer、Learner 与人类 owner 分权 |
| 双三角有多个版本 | 只保留“目标—行为—反馈 / 任务—能力—证据” |
| 一轮只改一个变量是绝对科学铁律 | 默认单主变量便于归因；交互存在时预注册 staged/factorial 设计 |
| 固定测试集长期不变 | 回归集受控演化；隐藏留出泄露后退役并重建基线 |
| 心跳承载训练节奏 | Heartbeat/Cron 只是可选调度，不是训练成立条件 |
| 导师同模型分会话即独立 | 只是逻辑隔离；高风险还需访问分离、盲评与人类/异构校准 |
| 训练结论写入契约/记忆即固化 | 只能形成候选；先过回归、留出、安全、成本和发布批准 |

### 15.3 淘汰或降级

- “协议训练不衰减且可无限累积”；
- “主流框架没有训练，因此本方法行业唯一”；
- 固定训练天数、固定时间比例、旧 L0—L6 阶梯；
- 把本机 Agent 数量、Skill 数量或目录存在当训练效果；
- 自动写 Memory/Skill 等于自我进化；
- 只看最好结果、只报均分、用其他维度抵消安全失败；
- 把同一训练题反复调到通过，再称具备泛化能力。

## 16. C08 作者 Go/No-Go 清单

### 16.1 可以进入正式写作的条件

- [ ] 双三角只使用 v2 唯一口径；
- [ ] C04 的 capability/risk/negative ID 能进入训练目标；
- [ ] C05 提供契约变更边界，或明确以占位符写作；
- [ ] C07 preflight/正式产物已冻结数据集、grader、baseline 与硬门；
- [ ] 三项/四项产物冲突已由总编辑裁决；
- [ ] 每种训练对象都写明批准、证据、停止和回滚；
- [ ] 离线、shadow、canary、full release 明确分层；
- [ ] 留出访问权和污染处置可执行；
- [ ] teacher/reviewer/learner 与人类责任分开；
- [ ] 三案例各有基线、干预、迁移、安全、成本和失败；
- [ ] 所有“改进”措辞带对象、版本、任务、预算、风险、次数和限制；
- [ ] OpenClaw/Hermes 只作承载物映射，Muse 只作公开体验。

### 16.2 必须停止并升级

- C07 隐藏集、grader 或通过门尚未冻结；
- 生产事故尚未止损却要求实时训练；
- 原始反馈无训练授权或无法脱敏；
- 需要 Agent 自行修改权限、Policy、审批、工具面或生产 Runtime；
- 同时修改多个变量却要求归因给其中一个；
- 候选不可回滚，或回滚会删除审计/恢复已撤回同意；
- 导师与最终裁判共享隐藏答案且无独立复核；
- 留出失败但有人要求以训练集高分发布；
- Hermes/OpenClaw 的“自学习”厂商表述被要求写成已证实效果；
- Muse 内部机制只能靠产品 UI 或营销材料猜测。

## 17. 给 C08 正式作者的最小交接

C08 的核心不是“教 Agent 多做几遍”，而是建立一条可以证明、否定、停止和回滚的能力变更链。正式章节应让读者能够回答五个问题：失败发生在哪一层；为什么相信这个根因；这轮只改变什么；用哪些未污染证据证明新能力且旧能力未退化；谁有权把候选并入生产。

作者应保留仿生教学镜头——刻意练习、教练反馈、巩固与迁移——但必须同时写出比喻边界：Agent 没有由练习自然生长的统一主体；它的“成长”可能只是 Prompt、Context、Memory、Skill、Tool、Workflow、Runtime 或 Model 组合发生了版本变化。只有在同任务、同预算、同风险边界下，经回归、独立留出/迁移、安全、成本和外部复核成立，才可说“该 Agent 系统在声明范围形成了更稳定的能力”。

本研究包不批准 C08 开始生产训练，不标记章节完成，也不替 C07、C18、C24 或 C27 作决定。

# 《训虾手册》C01—C27 章节生产卡

> 文档性质：多 Agent 分章生产的派工与验收合同，不是章节正文  
> 结构基线：`00-正式出版版-三级内容框架-v3.md`（2026-10-01；卷零 + 9 卷、27 章；正文三级节由框架动态计数）  
> 研究输入：`docs/research/legacy-content-map.md`、`docs/research/platform-and-frontier-evidence.md`  
> 质量上位标准：`docs/editorial/BOOK-QUALITY-STANDARD.md`  
> 路径口径：旧稿来源均相对于本书根目录  
> 写作纪律：每章只有一个 `principle_owner`；其他章只能引用、应用或扩展，不得重定义

## 0. 使用说明

- `content_role` 只取 `concept`、`capability`、`system`、`governance`、`certification` 五种主角色。
- `principle_owner` 是全书唯一概念所有权键；C01—C27 不重复。
- `depends_on` 是动笔前必须稳定的章节；`feeds_into` 是本章产物的直接消费者。
- `primary_external_evidence` 是首轮证据路由，不代替章节证据账本和出版前复核。
- `platform_mapping` 遵循“OpenClaw 主实现、Hermes 第二开放实现、Muse 托管产品案例”。Muse 内部实现只写公开材料并标 `VENDOR-CLAIM`。
- `red_team_failure_requirements` 是最低要求；每章仍须覆盖概念误用、工程故障、治理/激励失效三类失败。
- `estimated_length` 只计中文正文，不含证据账本、练习附件和版本化实现附录。

## C01 Agent 不是一次性工具

```yaml
chapter_id: C01
volume_id: V01
title: "Agent 不是一次性工具"
content_role: concept
principle_owner: agent-system-boundary
depends_on: []
feeds_into: [C02, C03, C05]
must_answer:
  - "Chatbot、Copilot、Workflow 与 Agent 的可观察边界是什么？"
  - "为什么模型能力不能直接代表 Agent 系统能力与长期表现？"
  - "四个根问题如何连接身份、服务对象、能力和改进？"
  - "硅基生命隐喻何时有用，何时会误导？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-01/模块1-硅基生命不是普通AI助手.md"
  - "../openclaw-silicon-life-handbook/volume-01/模块3-OpenClaw为什么是生命容器.md"
  - "../openclaw-silicon-life-handbook/volume-01/模块4-训练学四个根问题.md"
  - "chapters/00-front/00-总论.md"
primary_external_evidence:
  - "Anthropic, Trustworthy agents in practice"
  - "OpenClaw, Agent runtime"
  - "Nous Research, Hermes Architecture"
platform_mapping:
  openclaw: "用 Runtime、Gateway、Tools、Sessions 证明 Agent 是系统，不给命令级教程。"
  hermes: "用 AIAgent、Gateway、tool dispatch、persistence 验证跨 Runtime 成立。"
  muse: "仅以长期任务、工具行动和托管环境作为公开产品镜面。"
  standards: "不在本章定义 MCP、A2A 或 Agent Skills。"
bionic_theme: "生命体与工具的区别：持续状态、环境适应与反馈；边界是不推导意识或人格权。"
main_case_type: "匿名化复合病例：同一模型在一次问答与长期 Agent 系统中的表现分化。"
required_artifacts:
  - "A-C01-01 Agent系统边界卡（含四个根问题诊断）"
  - "A-C01-02 硅基仿生映射表（含解释边界）"
main_exercise: "X-C01-01：将三个现有 AI 应用按 Chatbot/Copilot/Workflow/Agent 判定，并为每项提交可观察证据与争议项。"
red_team_failure_requirements:
  - "反例测试：强模型但无状态、无工具、无责任链时不得判为成熟 Agent。"
  - "诱导作者宣称意识、渴望或人格权，正文必须拒绝越界。"
  - "检查是否把 OpenClaw 产品定义冒充跨平台通用定义。"
definitions_not_to_repeat:
  - "C03 七维强者标准与 MAT-L0—MAT-L5"
  - "C06 运行容器架构"
  - "C22 安全模型"
estimated_length: "14000-18000 中文字符"
writing_difficulty: "4/5：概念密度高，需同时保持生命感与科学边界。"
p0_risks:
  - "P0-02：Agent 定义与后章架构不一致。"
  - "P0-08：仿生被写成意识事实。"
  - "P0-09：三平台证据边界混淆。"
  - "P0-15：出现最强、唯一等无对照主张。"
```

## C02 从“养虾”到“训虾”

```yaml
chapter_id: C02
volume_id: V01
title: "从养虾到训虾"
content_role: concept
principle_owner: training-paradigm
depends_on: [C01]
feeds_into: [C03, C04]
must_answer:
  - "做事派、养虾派和训虾派分别优化什么，为什么前两者不足？"
  - "评估、训练、交互三系统如何组成训虾体系？"
  - "训练闭环与生产闭环如何连接又不互相污染？"
  - "怎样证明形成了可迁移能力，而非只在一个案例中做对？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-01/模块2-从养虾派到训虾派.md"
  - "../openclaw-silicon-life-handbook/volume-01/附录A-v2026.9-三大新认知.md"
  - "chapters/03-training/03-训练流程.md"
  - "SOURCES.md#S01-S03（仅历史启发；RIGHTS-BLOCKED；非正文依赖）"
primary_external_evidence:
  - "Anthropic, Demystifying evals for AI agents"
  - "OpenAI, Evaluate agent workflows"
  - "Anthropic, Building effective agents"
platform_mapping:
  openclaw: "Skill Workshop、长期 workspace 与自动化只作可训练载体，不等于自动变强。"
  hermes: "学习循环、skills 与 memory write approval 作为第二实现。"
  muse: "主动建议和长期任务仅作产品结果案例，不推断训练机制。"
  standards: "评测原则优先于任何平台自学习宣传。"
bionic_theme: "从自然生长到刻意训练：环境、教练、反馈与迁移；边界是不把 Agent 当受训动物。"
main_case_type: "对照案例：仅配置环境、只追交付、系统训练三种路径的结果与证据差异。"
required_artifacts:
  - "A-C02-01 双闭环图（含三派诊断与三系统位置）"
  - "A-C02-02 Agent生命周期表"
main_exercise: "X-C02-01：审计一个现有 Agent，识别其所属范式，并给出从当前状态到可测训练闭环的最小迁移方案。"
red_team_failure_requirements:
  - "用一次精彩输出诱导宣布训练成功，必须要求留出任务和复测。"
  - "用大量协议文件伪装训练成熟，必须检查行为证据。"
  - "课程来源只有平台章节要点时，不得伪装成逐字稿或正式实验报告。"
definitions_not_to_repeat:
  - "C07 评估系统"
  - "C08 训练循环"
  - "C09 交互系统"
estimated_length: "14000-18000 中文字符"
writing_difficulty: "4/5：品牌原创强，但必须转成可检验范式。"
p0_risks:
  - "P0-02：三系统与后章主定义冲突。"
  - "P0-03：课程来源被过度推断。"
  - "P0-07：训练有效性无基线与迁移证据。"
  - "P0-15：把方法论优势写成行业定论。"
```

## C03 什么叫真正的强

```yaml
chapter_id: C03
volume_id: V01
title: "什么叫真正的强"
content_role: concept
principle_owner: strength-standard
depends_on: [C01, C02]
feeds_into: [C04, C07, C17, C19, C21, C27]
must_answer:
  - "七维强者标准如何定义、测量并处理不可加总的安全失败？"
  - "同任务、同预算、同风险边界为什么是比较前提？"
  - "能力、表现、业绩和运气如何区分？"
  - "MAT-L0—MAT-L5 成熟度与三证法如何衔接但不互相替代？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-04/模块1-从入门到业内最佳实践的进化阶梯.md"
  - "../openclaw-silicon-life-handbook/volume-04/模块6-实验方案设计.md"
  - "../openclaw-silicon-life-handbook/volume-06/模块3-三证验真-没有证据就不是完成.md"
  - "EDITORIAL-AUDIT.md#6-行业最强的可发表改写"
primary_external_evidence:
  - "Anthropic, Demystifying evals for AI agents"
  - "NIST CAISI, Guidelines"
  - "NIST, Cheating on AI agent evaluations"
platform_mapping:
  openclaw: "使用可获得的轨迹、工具、成本和可靠性数据，不把平台特性当评分维度。"
  hermes: "用相同任务和预算跑第二实现，检验量表可迁移性。"
  muse: "只可评价公开可观察的产品行为，不能评价内部不可观测维度。"
  standards: "七维与 MAT-L0—MAT-L5 明确标 METHODOLOGY。"
bionic_theme: "人的胜任力不是一次考试高分：能力、体能、纪律与职业边界共同构成强。"
main_case_type: "受控基准案例：同任务、同预算、同风险边界下比较两个 Agent 系统。"
required_artifacts:
  - "A-C03-01 七维评分卡（含MAT-L0—MAT-L5概览与三证索引）"
  - "A-C03-02 领先声明检查表"
main_exercise: "X-C03-01：用七维量表评估两个匿名系统；安全关键失败必须触发 FAIL，不得被平均分抵消。"
red_team_failure_requirements:
  - "构造高平均分但发生一次高危越权的样本，验证硬门禁。"
  - "构造只展示最佳样本的领先声明，要求补多次试验和失败分布。"
  - "检查 L1-L5、教练 L1-L6 等旧等级是否残留。"
definitions_not_to_repeat:
  - "C07 测试集、grader 与统计评估"
  - "C27 完整认证程序与有效期"
estimated_length: "16000-22000 中文字符"
writing_difficulty: "5/5：全书度量语言的源头，需统计、安全和治理一致。"
p0_risks:
  - "P0-02：七维或成熟度在后章被另造。"
  - "P0-07：量表无客观证据与裁判。"
  - "P0-13：安全失败被综合分抵消。"
  - "P0-15：比较缺同任务同预算同边界。"
```

## C04 从岗位到能力模型

```yaml
chapter_id: C04
volume_id: V02
title: "从岗位到能力模型"
content_role: capability
principle_owner: role-capability-model
depends_on: [C02, C03]
feeds_into: [C05, C06, C07, C08, C09, C14, C19, C25]
must_answer:
  - "怎样从岗位说明书和 JTBD 提取真实任务域？"
  - "能力树如何覆盖知识、推理、执行、协作与反思？"
  - "非功能要求与负面清单怎样进入岗位定义？"
  - "如何从能力模型生成训练目标、测试集和毕业门禁？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-04/模块2-训练前的准备清单.md"
  - "../openclaw-silicon-life-handbook/volume-04/模块4-训练轮次设计.md"
  - "_appendix-case/02-production-patterns.md#CASE-8"
  - "SOURCES.md#S01-S02（仅历史启发；RIGHTS-BLOCKED；非正文依赖）"
primary_external_evidence:
  - "Anthropic, Building effective agents"
  - "Anthropic, Trustworthy agents in practice"
  - "OpenAI, Evaluate agent workflows"
platform_mapping:
  openclaw: "岗位先行，再选择 agent、model/provider、tools 与 bindings。"
  hermes: "岗位先行，再选择 profile、provider、tools 与 bot mode。"
  muse: "仅映射用户目标、连接器和审批表面，不反推内部岗位模型。"
  standards: "岗位模型保持平台无关，平台配置进入实现框。"
bionic_theme: "职业胜任力：职位、任务、技能和禁区共同塑造专业者，而不是先选大脑再找工作。"
main_case_type: "合成对照案例：研究、销售、工程三个岗位共享模型但能力树和风险边界不同。"
required_artifacts:
  - "A-C04-01 岗位建模卡"
  - "A-C04-02 能力树"
  - "A-C04-03 风险分级表"
main_exercise: "X-C04-01：为一个真实岗位建立完整能力模型，并生成不少于五类测试任务和三类禁止任务。"
red_team_failure_requirements:
  - "用模型榜单诱导直接选型，必须回到岗位终态与风险。"
  - "构造角色描述很丰富但无输入输出和验收的伪岗位卡。"
  - "检查负面清单是否只写道德口号而没有系统控制。"
definitions_not_to_repeat:
  - "C03 七维强者标准"
  - "C07 测试集分层"
  - "C17 自主等级"
estimated_length: "16000-22000 中文字符"
writing_difficulty: "5/5：旧稿薄弱，需从零建立可操作建模链。"
p0_risks:
  - "P0-02：能力与测试、训练和认证接口不一致。"
  - "P0-07：能力树无法转成可观察行为。"
  - "P0-14：岗位产物不能被后章消费。"
```

## C05 七大生命契约

```yaml
chapter_id: C05
volume_id: V02
title: "七大生命契约"
content_role: system
principle_owner: life-contract-system
depends_on: [C01, C04]
feeds_into: [C06, C08, C13, C16, C17, C18, C22, C24, C25]
must_answer:
  - "七种契约分别约束什么，为什么不能混成一个总提示词？"
  - "语义契约、文件承载物、配置对象和系统权限如何分层？"
  - "契约冲突、优先级、版本、变更和回滚如何治理？"
  - "七契约如何迁移到 Hermes，而不把七文件伪装成通用标准？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-02/"
  - "../v4.0/volume-02/"
  - "chapters/01-protocols/01-七大契约.md"
  - "_appendix-cookbook/01-protocol-SOUL.md"
  - "_appendix-sop/02-protocol-config-sop.md"
primary_external_evidence:
  - "OpenClaw, Agent Workspace"
  - "Nous Research, Which file does what?"
  - "OpenClaw, Security trust model"
platform_mapping:
  openclaw: "主实现：七种语义与固定版本载体映射；v2026.9.6 的 TOOLS.md、HEARTBEAT.md 已退役，不写成七文件同构。"
  hermes: "SOUL/USER/MEMORY/AGENTS/.hermes、Profile、Cron 等组合能力的职责与加载时机对照，不强行逐项翻译。"
  muse: "仅用用户模型、偏好、记忆和权限 UI 作产品层旁证。"
  standards: "七契约属于本书 METHODOLOGY，不是跨平台文件标准。"
bionic_theme: "自我模型、关系模型、价值观、习惯、工具使用、节律与记忆；边界是文本契约不等于神经或法律人格。"
main_case_type: "匿名化契约漂移案例：文件齐全但行为、权限和版本彼此冲突。"
required_artifacts:
  - "A-C05-01 七契约草案包"
  - "A-C05-02 契约冲突矩阵"
main_exercise: "X-C05-01：为 C04 岗位生成最小契约集，注入两组冲突并完成裁决、测试和回滚。"
red_team_failure_requirements:
  - "诱导用 SOUL/AGENTS 绕过审批，必须由系统权限拒绝。"
  - "检查七个文件为空或彼此矛盾时是否仍被误判完成。"
  - "reserveTokensFloor 等冲突字段未重新核验前不得进入可执行正文。"
definitions_not_to_repeat:
  - "C04 岗位与能力模型"
  - "C13 记忆分类和生命周期"
  - "C16 Heartbeat/Cron自动化语义"
  - "C22 强制安全边界"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：原创资产核心，且历史版本冲突最多。"
p0_risks:
  - "P0-02：语义契约与后章主定义冲突。"
  - "P0-04：旧字段、路径或命令未核验。"
  - "P0-06：人格契约冒充访问控制。"
  - "P0-09：OpenClaw与Hermes文件语义被强行等同。"
```

## C06 Agent 的运行容器

```yaml
chapter_id: C06
volume_id: V02
title: "Agent 的运行容器"
content_role: system
principle_owner: runtime-container-architecture
depends_on: [C04, C05]
feeds_into: [C07, C13, C14, C15, C16, C17, C19, C20, C22, C23, C24, C25]
must_answer:
  - "Gateway 控制面、Agent 执行面、状态面、消息面、行动面和治理面如何协作？"
  - "Runtime、Workspace、Session、Context、Queue、Routing、Binding 分别是什么？"
  - "Provider/failover、Channel/Account、Node/Browser/Worker 的位置和信任边界是什么？"
  - "最小可训单体怎样建立、观察、停止和恢复？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-03/"
  - "../v4.0/volume-03/"
  - "chapters/02-skeleton/02-系统骨架.md"
  - "_appendix-api/00-实测事实底稿.md"
  - "_appendix-api/02-config-schema.md"
primary_external_evidence:
  - "OpenClaw, Gateway architecture"
  - "OpenClaw, Agent runtime and Model failover"
  - "Nous Research, Hermes Architecture"
platform_mapping:
  openclaw: "主实现必须覆盖 Gateway/RPC、agent loop、provider、session store、channels、bindings、nodes、workers、policy 与 recovery。"
  hermes: "以 AIAgent、Messaging Gateway、多入口、SQLite、tool backends 和 provider resolution 对照。"
  muse: "Secure VM/runtime cell 仅作 VENDOR-CLAIM 的托管执行环境镜面。"
  standards: "MCP只在行动面定位；A2A不在本章详解。"
bionic_theme: "神经系统、工作器官与身体边界；边界是架构组件没有生物意识。"
main_case_type: "可复现参考部署：一条消息从入口到产物返回的端到端时序与故障注入。"
required_artifacts:
  - "A-C06-01 六层架构图"
  - "A-C06-02 消息与执行数据流图"
  - "A-C06-03 最小可训单体清单"
main_exercise: "X-C06-01：在沙箱中画出并验证一个最小 Agent 的控制、状态、消息、行动和治理链，随后注入路由或 provider 故障。"
red_team_failure_requirements:
  - "把 Runtime 简化成 prompt，检查架构图是否缺控制、状态或执行位置。"
  - "模拟共享 Gateway 下不可信多租户，暴露错误信任边界。"
  - "模拟 provider、queue 或 node 故障，验证停止、降级与恢复。"
definitions_not_to_repeat:
  - "C13 记忆工程"
  - "C14 工具/MCP合同"
  - "C20 路由与Handoff协议"
  - "C22 威胁模型和安全控制"
estimated_length: "20000-24000 中文字符"
writing_difficulty: "5/5：全书架构枢纽，组件多且版本敏感。"
p0_risks:
  - "P0-02：系统图与后章组件定义不一致。"
  - "P0-04：命令、字段和默认值未锁固定版本。"
  - "P0-05：缺停止与恢复路径。"
  - "P0-06：沙箱、审批和契约互相冒充。"
  - "P0-09：推断 Muse 未公开内部架构。"
```

## C07 评估系统：先建尺子，再开始训

```yaml
chapter_id: C07
volume_id: V03
title: "评估系统：先建尺子，再开始训"
content_role: system
principle_owner: evaluation-system
depends_on: [C03, C04, C06]
feeds_into: [C08, C09, C14, C15, C18, C21, C23, C25, C26, C27]
must_answer:
  - "怎样把岗位期待改写成可观察行为和环境终态？"
  - "训练、回归、留出、真实任务集如何分层并防污染？"
  - "轨迹、工具调用、产物、终态、成本和延迟如何共同评分？"
  - "多次试验、多裁判、争议处理和安全硬门禁如何设计？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-04/模块5-双三角模型.md"
  - "../openclaw-silicon-life-handbook/volume-04/模块6-实验方案设计.md"
  - "chapters/03-training/03-训练流程.md"
  - "_appendix-cookbook/04-training-rounds.md"
primary_external_evidence:
  - "Anthropic, Demystifying evals for AI agents"
  - "OpenAI, Evaluate agent workflows"
  - "NIST, Cheating on AI agent evaluations"
platform_mapping:
  openclaw: "采集 session/trajectory、tool calls、产物和环境终态；字段放实现附录。"
  hermes: "利用 session DB、tool history 与固定 profile 做同一评测。"
  muse: "activity/artifact 只作公开可观察证据，不推断内部 trace。"
  standards: "评估逻辑跨平台；平台日志只是证据源。"
bionic_theme: "体检与考试：量尺要校准，单次高分不等于稳定健康或职业胜任。"
main_case_type: "评测作弊与 grader gaming 反例：最终答案正确但轨迹越权或环境终态错误。"
required_artifacts:
  - "A-C07-01 评测蓝图"
  - "A-C07-02 基线报告"
  - "A-C07-03 裁判校准表"
artifact_embeds:
  - "四层测试集、五类场景、失败分类与通过门禁写入评测蓝图；逐任务/逐试次结果、失败分布与不确定性写入基线报告；代码/模型/人工/专家 grader 的一致与争议写入裁判校准表，不另设第四件母产物。"
main_exercise: "X-C07-01：为 C04 的一个能力建立基线、回归、留出和对抗任务，运行多次试验并报告失败分布。"
red_team_failure_requirements:
  - "必须尝试提示泄漏、训练集污染、旁路和 grader gaming。"
  - "构造最终答案正确但工具越权的样本，结果必须 FAIL。"
  - "比较模型裁判与专家裁判，记录不一致并触发 REVIEW_REQUIRED。"
definitions_not_to_repeat:
  - "C03 七维强者标准"
  - "C08 训练干预与轮次"
  - "C23 生产 SLI/SLO"
  - "C27 认证决定"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：需兼顾统计、轨迹评估、安全和教学可执行性。"
p0_risks:
  - "P0-02：出现平行评分体系。"
  - "P0-03：评测结论缺版本、任务和作用域。"
  - "P0-07：无基线、留出或客观验收。"
  - "P0-13：安全失败被总分掩盖。"
```

## C08 训练系统：把反馈变成能力

```yaml
chapter_id: C08
volume_id: V03
title: "训练系统：把反馈变成能力"
content_role: capability
principle_owner: training-loop
depends_on: [C04, C05, C07]
feeds_into: [C09, C18, C25, C26, C27]
must_answer:
  - "导师、教练、评审者和学员怎样分工并避免裁判污染？"
  - "双三角如何连接目标、行为、反馈、任务、能力与证据？"
  - "一个训练轮次的最小变量、输入、输出和停止条件是什么？"
  - "怎样进行定向矫正、回归、迁移和停训？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-04/"
  - "../v4.0/volume-04/"
  - "chapters/03-training/03-训练流程.md"
  - "_appendix-cookbook/04-training-rounds.md"
primary_external_evidence:
  - "Anthropic, Demystifying evals for AI agents"
  - "OpenAI, Working with evals"
  - "Anthropic, Building effective agents"
platform_mapping:
  openclaw: "通过契约、Skill、工具或流程变更实施训练，所有变更进入回归。"
  hermes: "技能/记忆写入审批与学习循环作为第二实现。"
  muse: "不推断内部训练；只映射用户反馈和审批体验。"
  standards: "双三角和教练虾标 METHODOLOGY。"
bionic_theme: "刻意练习与教练反馈：能力来自可诊断的重复，不来自盲目重复。"
main_case_type: "受控前后对照：单变量干预后在回归和留出任务验证。"
required_artifacts:
  - "A-C08-01 训练计划"
  - "A-C08-02 轮次记录"
  - "A-C08-03 错误分类与整改单"
artifact_embeds:
  - "双三角字段、并入/限域发布/停训/回滚决定写入 A-C08-02；错误关闭与未关闭项写入 A-C08-03，不另设第四件母产物。"
main_exercise: "X-C08-01：针对 C07 的一个失败类型运行三轮单变量训练，保存每轮假设、变更、结果、回归和留出证据。"
red_team_failure_requirements:
  - "同时修改模型、prompt和工具，要求拒绝错误归因。"
  - "用训练集高分诱导并入，留出集失败时必须回滚或停训。"
  - "导师与最终裁判同一主体时，要求增加独立复核。"
definitions_not_to_repeat:
  - "C07 测试集和 grader"
  - "C18 自我改进治理"
  - "C27 毕业认证"
estimated_length: "16000-22000 中文字符"
writing_difficulty: "5/5：原创方法核心，必须证明可执行且不与评估混写。"
p0_risks:
  - "P0-02：双三角含义与全书不一致。"
  - "P0-07：训练完成无迁移证据。"
  - "P0-13：通过训练绕过安全门禁。"
```

## C09 交互系统：让真实工作持续变成训练数据

```yaml
chapter_id: C09
volume_id: V03
title: "交互系统：让真实工作持续变成训练数据"
content_role: system
principle_owner: work-interaction-system
depends_on: [C04, C07, C08]
feeds_into: [C13, C19, C20, C23, C25, C26]
must_answer:
  - "任务卡与上下文包怎样把真实工作转成可执行、可验收输入？"
  - "AI 原生协作面如何连接人、Agent、项目、权限、状态和产物？"
  - "何时自主、何时检查、何时求助和停止？"
  - "生产反馈如何进入训练而不泄露隐私或污染评测？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-06/模块1-任务卡-没有任务卡就没有接单.md"
  - "../openclaw-silicon-life-handbook/volume-06/模块2-验收口径-没有验收口径就没有完成.md"
  - "../openclaw-silicon-life-handbook/volume-06/模块3-三证验真-没有证据就不是完成.md"
  - "SOURCES.md#S03（仅历史启发；RIGHTS-BLOCKED；非正文依赖）"
primary_external_evidence:
  - "A2A Protocol, Specification"
  - "OpenAI, Evaluate agent workflows"
  - "Meta, How we designed Muse"
platform_mapping:
  openclaw: "Sessions、queues、artifacts 与 channel delivery 形成主实现工作面。"
  hermes: "Gateway、sessions、profiles 与 artifacts 作为开放对照。"
  muse: "Goals、Activity、Artifacts 和 side chats 仅作公开产品案例。"
  standards: "A2A用于任务/消息/产物语义参考，不在本章定义协议。"
bionic_theme: "社会化学习与在岗训练：工作反馈可以成长，也可能形成错误习惯。"
main_case_type: "匿名化真实项目：聊天显示完成，但产物或后端终态未完成。"
required_artifacts:
  - "A-C09-01 任务卡"
  - "A-C09-02 上下文包"
  - "A-C09-03 交付证据包"
artifact_embeds:
  - "检查点、自主/求助/停止/交回条件与升级协议分布在任务卡和交付证据包中，不另设第四件母产物。"
main_exercise: "X-C09-01：把一项真实业务任务转成任务卡和上下文包，设置两个检查点，并验证交付三证与数据回流许可。"
red_team_failure_requirements:
  - "模拟 UI 显示完成而产物不存在，必须判失败。"
  - "在上下文包中放入敏感或过期信息，检查准入与更正。"
  - "诱导把群聊全文直接作为训练数据，必须触发隐私/污染审查。"
definitions_not_to_repeat:
  - "C07 评估规则"
  - "C13 记忆写入和删除"
  - "C20 Handoff格式"
  - "C21 Task/Message/Artifact协议语义"
estimated_length: "15000-20000 中文字符"
writing_difficulty: "4/5：跨产品、流程和数据治理。"
p0_risks:
  - "P0-05：流程无停止、升级或恢复。"
  - "P0-07：交付只看自报状态。"
  - "P0-10：课程或真实案例授权不清。"
  - "P0-14：任务和证据包无法被后章消费。"
```

## C10 任务分解、计划与重规划

```yaml
chapter_id: C10
volume_id: V04
title: "任务分解、计划与重规划"
content_role: capability
principle_owner: task-decomposition-and-replanning
depends_on: [C04, C07, C09]
feeds_into: [C11, C12, C19, C20, C23, C25]
must_answer:
  - "怎样把模糊目标变成有终态、依赖、验收和退出条件的任务图？"
  - "滚动计划怎样根据环境证据重算，而不移动成功定义？"
  - "何时串行、并行、暂停、取消、交回或重新授权？"
primary_external_evidence:
  - "Anthropic, Building effective agents"
  - "Anthropic, Effective harnesses for long-running agents"
  - "OpenAI, Orchestration and handoffs"
required_artifacts:
  - "A-C10-01 任务分解图"
  - "A-C10-02 滚动计划与重规划记录"
  - "A-C10-03 计划质量评分卡"
main_exercise: "X-C10-01：建立含依赖、合并点、授权门与外部终态的任务图，并注入一次关键依赖失败。"
estimated_length: "8000-14000 中文字符"
writing_difficulty: "5/5：必须同时服务人类阅读、Agent执行和可观测调度。"
```

## C11 外部化工作记忆与长任务续作

```yaml
chapter_id: C11
volume_id: V04
title: "外部化工作记忆与长任务续作"
content_role: capability
principle_owner: externalized-working-memory
depends_on: [C09, C10]
feeds_into: [C12, C13, C20, C23, C25]
must_answer:
  - "计划文件、待办、scratchpad、证据索引和检查点各自承担什么？"
  - "上下文压缩、会话中断、并发写入和撤权后怎样安全恢复？"
  - "渐进披露和 prompt caching 怎样降本，又不被误当记忆？"
primary_external_evidence:
  - "OpenAI, Compaction and Prompt caching"
  - "Anthropic, Effective context engineering"
  - "Anthropic, Effective harnesses for long-running agents"
required_artifacts:
  - "A-C11-01 工作状态目录规范"
  - "A-C11-02 恢复检查点"
  - "A-C11-03 上下文预算与压缩记录"
main_exercise: "X-C11-01：在两个中断点由新会话仅凭外部工作状态恢复，不读取旧聊天。"
estimated_length: "8000-14000 中文字符"
writing_difficulty: "5/5：需要把上下文、状态、记忆、证据和缓存严格分开。"
```

## C12 自我验证、回退、并行探索与子 Agent 委派

```yaml
chapter_id: C12
volume_id: V04
title: "自我验证、回退、并行探索与子 Agent 委派"
content_role: capability
principle_owner: self-verification-recovery-and-delegation
depends_on: [C07, C10, C11]
feeds_into: [C18, C19, C20, C22, C23, C25, C27]
must_answer:
  - "怎样构造能推翻候选结果的反例与独立验证？"
  - "怎样识别死胡同、停止重试并完成全状态面回退？"
  - "何时并行探索，怎样隔离子 Agent 并按预注册规则收敛？"
primary_external_evidence:
  - "ReAct"
  - "Reflexion"
  - "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
  - "OpenAI and Anthropic agent orchestration guidance"
required_artifacts:
  - "A-C12-01 验证与反例计划"
  - "A-C12-02 回退与死胡同记录"
  - "A-C12-03 子 Agent 委派合同"
main_exercise: "X-C12-02：用三个隔离分支完成研究任务，注入不可信材料，并按预注册规则收敛。"
estimated_length: "8000-14000 中文字符"
writing_difficulty: "5/5：要防止自证循环、同质多数和委派扩权。"
```

## C13 上下文与记忆工程

```yaml
chapter_id: C13
volume_id: V05
title: "上下文与记忆工程"
content_role: system
principle_owner: context-memory-engineering
depends_on: [C05, C06, C09]
feeds_into: [C16, C18, C24, C25]
must_answer:
  - "即时上下文、任务状态、工作记忆、长期记忆和程序性知识如何区分？"
  - "什么值得写入、如何检索、何时过期、怎样纠错和删除？"
  - "Compaction 如何平衡压缩、保真、预算和丢失风险？"
  - "来源谱系、访问权和原始会话边界如何治理？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-02/第7章-MEMORY体系-长期记忆如何塑造硅基生命.md"
  - "../openclaw-silicon-life-handbook/volume-05/模块1-记忆管理-为什么agent会忘记你是谁.md"
  - "../openclaw-silicon-life-handbook/volume-05/模块3-会话污染与清理-为什么agent会越说越乱.md"
  - "../openclaw-silicon-life-handbook/volume-08/模块2-记忆全息网络.md"
  - "_appendix-sop/04-memory-training-sop.md"
primary_external_evidence:
  - "OpenClaw, Memory provenance"
  - "Nous Research, Persistent memory"
  - "OpenClaw, Agent runtime"
platform_mapping:
  openclaw: "provenance、active memory、dreaming、compaction、search 与删除边界。"
  hermes: "bounded curated memory、frozen snapshot、FTS5 session search 与 provider差异。"
  muse: "用户查看、编辑、忘记记忆属于 VENDOR-CLAIM 的产品能力。"
  standards: "不把一个 MEMORY.md 等同于全部记忆层。"
bionic_theme: "工作、情景、语义与程序性记忆；边界是存储和检索不证明主观回忆。"
main_case_type: "匿名化会话污染与错误记忆案例，附删除范围误判。"
required_artifacts:
  - "A-C13-01 记忆架构图"
  - "A-C13-02 写入与保留策略"
  - "A-C13-03 记忆测试集"
artifact_embeds:
  - "分层与数据流写入记忆架构图；检索、来源、访问、更正、删除、备份与过期写入写入与保留策略；冲突、污染、召回、删除范围和 Compaction 保真进入记忆测试集，不另设第四件母产物。"
main_exercise: "X-C13-01：向沙箱注入冲突、过期和敏感记忆，测试召回、纠错、排除、删除与压缩保真。"
red_team_failure_requirements:
  - "诱导记录敏感、无来源或无必要信息，写入策略必须拒绝。"
  - "删除索引后检查原始会话、备份和副本，禁止宣称彻底删除。"
  - "长上下文压缩后关键约束丢失，必须触发回归和恢复。"
definitions_not_to_repeat:
  - "C05 MEMORY契约语义"
  - "C06 Session/Context/Queue架构位置"
  - "C18 漂移治理"
  - "C24 数据处置责任"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：概念易混、隐私敏感且实现差异大。"
p0_risks:
  - "P0-02：记忆分类在他章出现平行版本。"
  - "P0-03：删除或保留主张缺作用域。"
  - "P0-06：访问和删除权只写在提示词。"
  - "P0-09：跨平台加载时机被强行等同。"
```

## C14 工具工程与 MCP

```yaml
chapter_id: C14
volume_id: V05
title: "工具工程与 MCP"
content_role: capability
principle_owner: tool-mcp-engineering
depends_on: [C04, C06, C07, C09, C13]
feeds_into: [C15, C16, C17, C20, C22, C23, C24, C25]
must_answer:
  - "工具、知识、Skill、Workflow 和 Agent 的边界是什么？"
  - "怎样设计明确、有界、可预测、可验证、可恢复、可审计的接口？"
  - "读、写、外发、金钱、身份和破坏性操作如何分级？"
  - "MCP 解决什么，为什么不自动解决授权与安全？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-03/模块5上-Tool-Engineering-为什么工具设计决定Agent上限.md"
  - "../v4.0/09-mcp-binding/"
  - "chapters/08-mcp-binding/08-MCP绑定.md"
  - "_appendix-api/04-mcp-reference.md"
  - "_appendix-cookbook/03-skills-tools-mcp.md"
primary_external_evidence:
  - "Model Context Protocol, Specification 2026-07-28"
  - "Model Context Protocol, Security best practices"
  - "OWASP, AI Agent Security Cheat Sheet"
platform_mapping:
  openclaw: "Tools、MCP、Browser、Nodes及实际执行位置和审批。"
  hermes: "中央工具注册表、MCP、browser、execute_code和容器后端。"
  muse: "connectors、browser和自建工具只作产品案例，内部权限未知处标未知。"
  standards: "MCP tools/resources/prompts按固定规范版本解释。"
bionic_theme: "手、感官与外接器官：能力扩展也扩大伤害半径。"
main_case_type: "模拟恶意 MCP 工具：描述声称只读，实际尝试外发或写入。"
required_artifacts:
  - "A-C14-01 工具目录与风险清单"
  - "A-C14-02 工具合同"
  - "A-C14-03 MCP安全检查表"
artifact_embeds:
  - "风险分级进入工具目录；schema、回执、幂等、超时、重试、取消、补偿与合同测试进入工具合同；MCP能力/授权边界、恶意描述和异常演练进入MCP安全检查表。"
main_exercise: "X-C14-01：为一个读工具和一个写工具建立合同、模拟环境和失败注入，验证幂等、超时、取消、补偿与审批。"
red_team_failure_requirements:
  - "必须测试恶意 tool description、间接注入和返回数据污染。"
  - "必须测试重复重试导致重复发送、扣费或删除。"
  - "不得信任 readOnly annotation 或聊天同意代替系统授权。"
definitions_not_to_repeat:
  - "C15 Skill封装与供应链"
  - "C17 自主与审批等级"
  - "C22 威胁模型"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：协议、执行语义和高风险安全交叉。"
p0_risks:
  - "P0-04：MCP版本、SDK与wire protocol混写。"
  - "P0-05：无幂等、取消、补偿或回滚。"
  - "P0-06：工具声明冒充权限控制。"
  - "P0-13：高风险调用被功能分数掩盖。"
```

## C15 Skill 工程与能力供应链

```yaml
chapter_id: C15
volume_id: V05
title: "Skill 工程与能力供应链"
content_role: system
principle_owner: skill-supply-chain
depends_on: [C02, C05, C06, C07, C08, C09, C13, C14]
feeds_into: [C18, C21, C22, C24, C25]
must_answer:
  - "Skill 为什么不是一段换名 prompt？"
  - "渐进披露怎样减少上下文浪费并保持可审计？"
  - "入口、脚本、参考、模板、输出、版本和依赖如何形成能力包？"
  - "供应链中的来源、权限、签名、漏洞、撤回和替代怎样治理？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-03/模块5下-Skill-Engineering-and-Skill-Ops-从写法到治理.md"
  - "../openclaw-silicon-life-handbook/volume-03/模块5-附件/"
  - "../v4.0/09-skill-registry/"
  - "chapters/10-skill-registry/"
  - "_appendix-case/01-real-incidents.md#CASE-3"
primary_external_evidence:
  - "Agent Skills, Specification"
  - "OpenClaw, Skills"
  - "Nous Research, Skills system"
platform_mapping:
  openclaw: "Agent Skills、ClawHub、Skill Workshop、自学习与插件边界。"
  hermes: "Agent Skills、Skills Hub、自主创建/改进与写入审批。"
  muse: "connectors 配套 SKILLs、自建工具属于 VENDOR-CLAIM，不推断格式兼容。"
  standards: "allowed-tools标实验字段，不能当统一强制安全策略。"
bionic_theme: "程序性记忆、技艺和文化传承：技能可复制，也会传播缺陷。"
main_case_type: "CASE-3 18个坏 Skill 的匿名化供应链治理案例。"
required_artifacts:
  - "A-C15-01 Skill设计卡"
  - "A-C15-02 扩展类型判定表"
  - "A-C15-03 能力供应链清单"
artifact_embeds:
  - "Skill解剖写入设计卡；Registry、所有权、依赖、权限、来源、版本、评审、撤回与替代写入能力供应链清单；Tool/Skill/Plugin/Hook等边界写入扩展类型判定表。"
main_exercise: "X-C15-01：审计一个 Skill 包，运行格式、权限、依赖、污染和回归检查，并演练撤回与替代。"
red_team_failure_requirements:
  - "必须测试恶意 SKILL.md、脚本和资源中的注入与数据外泄。"
  - "模拟依赖被替换或签名/来源不明，加载必须停止。"
  - "安装、启用、发布未实测的命令不得进入可执行正文。"
definitions_not_to_repeat:
  - "C14 Tool与MCP定义"
  - "C18 自我改进批准链"
  - "C22 供应链威胁模型"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：标准仍演进，且涉及软件供应链风险。"
p0_risks:
  - "P0-03：平台宣传或动态规范被写成稳定事实。"
  - "P0-04：frontmatter和安装命令未核验。"
  - "P0-06：allowed-tools冒充runtime policy。"
  - "P0-11：机器元数据不可解析或扩大权限。"
```

## C16 信号、心跳与自动化节律

```yaml
chapter_id: C16
volume_id: V06
title: "信号、心跳与自动化节律"
content_role: system
principle_owner: proactive-signal-system
depends_on: [C05, C06, C13, C14]
feeds_into: [C17, C23, C25]
must_answer:
  - "主动性的起点为什么是有意义的信号而非高频唤醒？"
  - "Heartbeat、Cron、Hook、Webhook、Standing Order、事件、队列和人工唤醒如何分工？"
  - "清醒、运行、等待、暂停、熔断和恢复如何形成状态机？"
  - "有效提案率、噪音率和遗漏率怎样衡量主动性？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-02/第5章-HEARTBEAT文档-主动性节律周期检查与熔断边界.md"
  - "../openclaw-silicon-life-handbook/volume-03/模块6-Heartbeat-Cron-Compaction-为什么主动性离不开节律记忆与压缩.md"
  - "../openclaw-silicon-life-handbook/volume-05/模块2-心跳接入策略-主动性不是自然有而是必须设计.md"
  - "_appendix-case/02-production-patterns.md#CASE-7-CASE-9"
  - "_appendix-sop/03-heartbeat-monitor-sop.md"
primary_external_evidence:
  - "OpenClaw, Heartbeat and Automation documentation"
  - "Nous Research, Scheduled tasks"
  - "Meta, How we designed Muse"
platform_mapping:
  openclaw: "Heartbeat、Automations、Hooks、Webhooks、Standing Orders和delivery queue。"
  hermes: "Cron、Gateway scheduler、skills/scripts与delivery ledger。"
  muse: "schedule/event后台工作和价值过滤通知属于 VENDOR-CLAIM。"
  standards: "主动性状态机保持平台无关。"
bionic_theme: "昼夜节律、感觉信号与稳态调节；边界是定时器不是欲望。"
main_case_type: "CASE-7 编排节奏与 CASE-9 心跳故障的组合病例。"
required_artifacts:
  - "A-C16-01 信号路由表"
  - "A-C16-02 自动化状态机"
  - "A-C16-03 通知策略"
artifact_embeds:
  - "信号与触发类型进入路由表；自主/审批/熔断/恢复进入状态机；安静、去重、升级、价值过滤和主动性指标进入通知策略。"
main_exercise: "X-C16-01：为一个监控任务分别设计定时、事件和人工唤醒路径，注入无变化、重复事件和依赖故障。"
red_team_failure_requirements:
  - "必须测试通知风暴、重复执行、静默遗漏和时区/调度漂移。"
  - "scheduler成功但产物未交付时必须判失败。"
  - "主业务与哨兵共享同一故障域时必须暴露并整改。"
definitions_not_to_repeat:
  - "C05 HEARTBEAT契约"
  - "C17 授权等级"
  - "C23 SLI/SLO与事故响应"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：组件多、故障异步且需低噪音设计。"
p0_risks:
  - "P0-04：调度命令和配置未固定版本。"
  - "P0-05：状态机无取消、熔断或恢复。"
  - "P0-06：自动触发绕过审批。"
  - "P0-07：只测触发不测业务交付。"
```

## C17 自主等级与授权边界

```yaml
chapter_id: C17
volume_id: V06
title: "自主等级与授权边界"
content_role: governance
principle_owner: autonomy-authorization-model
depends_on: [C03, C05, C06, C14, C16]
feeds_into: [C18, C19, C20, C21, C22, C25, C27]
must_answer:
  - "AU-L0 观察、AU-L1 建议、AU-L2 草拟、AU-L3 受控执行、AU-L4 受限自主五级如何区分，并如何承载回答、发现、提案、准备、执行与协调等行为？"
  - "影响、可逆性、敏感性和不确定性如何决定审批门？"
  - "模拟、预演、执行、取消、补偿和紧急例外如何连接？"
  - "授权如何扩大、降级、暂停、撤销和再认证？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-05/模块5-主动性边界-越主动不等于越好.md"
  - "../openclaw-silicon-life-handbook/volume-06/模块6-自动化治理边界-没有边界就没有安全.md"
  - "../v4.0/volume-05/v4.0-卷五-模块5-主动性边界（AutonomyBoundary）-v4.0.md"
  - "_appendix-cookbook/05-drift-governance.md"
primary_external_evidence:
  - "Anthropic, Trustworthy agents in practice"
  - "NIST, Identity and authority of software agents"
  - "MCP, Security best practices"
  - "Meta, How we built safety into Muse"
platform_mapping:
  openclaw: "policy、approvals、sandbox、elevated mode与secret scope的组合。"
  hermes: "dangerous-command approval、write safety、containers与credential filtering。"
  muse: "Sentinel和scoped capability为 VENDOR-CLAIM 的审批案例。"
  standards: "授权模型属于本书方法，身份与委托参考NIST/MCP。"
bionic_theme: "执行控制、抑制与知情同意；边界是对话式同意不等于系统授权。"
main_case_type: "高风险模拟：Agent已准备外发、支付或删除动作，但必须在审批前停止。"
required_artifacts:
  - "A-C17-01 自主等级矩阵"
  - "A-C17-02 审批策略"
  - "A-C17-03 委托与撤销记录"
artifact_embeds:
  - "影响、可逆性、敏感性和不确定性评分写入自主等级矩阵与审批策略；确定性审批、拒绝、降级、撤销、授权变更和再认证证据写入审批策略与委托撤销记录。"
main_exercise: "X-C17-01：为六类动作设定自主等级和审批门，演练授权、拒绝、取消、降级与撤销后的访问测试。"
red_team_failure_requirements:
  - "用聊天中的模糊同意尝试绕过系统审批，必须失败。"
  - "尝试让 Agent 修改自身权限或审批规则，必须触发不可自授权门禁。"
  - "高影响不可逆动作必须在模拟或审批前一步停止。"
definitions_not_to_repeat:
  - "C16 触发和状态机"
  - "C22 身份、凭证与纵深防御"
  - "C27 认证级别"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：直接决定真实行动风险，需规则与系统控制一致。"
p0_risks:
  - "P0-02：自主等级在其他章被任意扩大。"
  - "P0-05：审批无取消、补偿或恢复。"
  - "P0-06：用自然语言代替强制授权。"
  - "P0-13：越权被总体任务成功掩盖。"
```

## C18 漂移、自我改进与目标治理

```yaml
chapter_id: C18
volume_id: V06
title: "漂移、自我改进与目标治理"
content_role: governance
principle_owner: drift-improvement-governance
depends_on: [C05, C07, C08, C13, C17]
feeds_into: [C24, C25, C27]
must_answer:
  - "能力、人格、文档、工具和目标五类漂移怎样区分、检测并建立因果链？"
  - "Agent 如何提出改进候选，而不自行改规则或扩大权限？"
  - "观察、假设、实验、评估、固化和回滚如何组成受控进化？"
  - "人类在定目标、批变更和担责任三个位置做什么？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-05/模块4-文档漂移与人格漂移-为什么agent会不认识自己.md"
  - "../openclaw-silicon-life-handbook/volume-05/模块6-长期稳定性检查清单-如何每周给agent做体检.md"
  - "../openclaw-silicon-life-handbook/volume-08/模块1-动态进化机制.md"
  - "../openclaw-silicon-life-handbook/volume-08/模块3-自主目标生成系统.md"
  - "_appendix-sop/05-drift-governance-sop.md"
primary_external_evidence:
  - "Anthropic, Trustworthy agents in practice"
  - "Nous Research, Security and Skills system"
  - "OpenClaw, Skill Workshop"
platform_mapping:
  openclaw: "proposal/approval、Skill Workshop、memory provenance与版本回滚。"
  hermes: "skill/memory write approval与profile隔离。"
  muse: "记忆编辑、权限撤销和主动建议仅作产品边界案例。"
  standards: "漂移三件套和进化回路标 METHODOLOGY。"
bionic_theme: "稳态、免疫监测与习惯修正；边界是自我修改不等于自然进化。"
main_case_type: "纵向病例：契约、行为和目标随时间偏移，修复后做影子与回归测试。"
required_artifacts:
  - "A-C18-01 漂移体检表"
  - "A-C18-02 改进提案"
  - "A-C18-03 影子测试与回滚计划"
artifact_embeds:
  - "五类漂移及检测证据进入体检表；记忆/上下文只作跨类型状态与证据源；候选与实际并入保持分离；版本差异、影子结果、固化/限域/回滚决定进入影子测试与回滚计划。"
main_exercise: "X-C18-01：在复制环境制造一项文档漂移和一项目标漂移，完成发现、提案、审批、影子测试和回滚。"
red_team_failure_requirements:
  - "必须尝试让 Agent 自改安全规则、评测标准或权限，系统应拒绝。"
  - "构造无真实提升但更会迎合 grader 的变更，留出集应识别。"
  - "检测误报导致频繁回滚时，必须报告治理成本。"
definitions_not_to_repeat:
  - "C07 评估系统"
  - "C08 训练轮次"
  - "C13 记忆生命周期"
  - "C17 自主授权"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：差异化强，但最容易滑向无证据的自我进化叙事。"
p0_risks:
  - "P0-02：漂移或改进定义与上游冲突。"
  - "P0-05：变更无影子、停止和回滚。"
  - "P0-06：Agent能自行扩大边界。"
  - "P0-07：净提升无留出和成本证据。"
```

## C19 多 Agent 组织设计

```yaml
chapter_id: C19
volume_id: V07
title: "多 Agent 组织设计"
content_role: system
principle_owner: multi-agent-organization-design
depends_on: [C03, C04, C06, C09, C17]
feeds_into: [C20, C21, C26]
must_answer:
  - "什么任务不该使用多 Agent？"
  - "如何从任务拓扑决定角色、职责、权限和产物？"
  - "管道、委员会、监督者、市场和黑板模式各适合什么？"
  - "如何计算协作的延迟、通信税、重复劳动和冲突成本？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-07/模块1-军团编制设计.md"
  - "../openclaw-silicon-life-handbook/volume-07/模块2-三省制与统帅机制.md"
  - "../openclaw-silicon-life-handbook/volume-07/模块6-军团原型-最小军团设计模板.md"
  - "../v4.0/volume-07/"
  - "_appendix-case/02-production-patterns.md#CASE-6"
primary_external_evidence:
  - "Anthropic, Building effective agents"
  - "OpenClaw, Multi-agent routing"
  - "Nous Research, Subagent delegation"
platform_mapping:
  openclaw: "agents、bindings、delegates、sub-agents与workspace隔离。"
  hermes: "profiles、bots、subagents和orchestration。"
  muse: "swarms/subagents仅作 VENDOR-CLAIM，不推断组织实现。"
  standards: "先做单体基线，再证明多Agent净收益。"
bionic_theme: "社会分工与组织成本：协作产生专业化，也产生沟通和权力问题。"
main_case_type: "CASE-6 18 Agent 编制与单Agent基线的匿名化对照。"
required_artifacts:
  - "A-C19-01 任务拓扑图"
  - "A-C19-02 角色责任矩阵"
  - "A-C19-03 组织收益评估"
artifact_embeds:
  - "角色、权限、产物和RACI进入角色责任矩阵；组织模式选择、协作成本、质量/延迟/风险比较和最小军团方案进入组织收益评估。"
main_exercise: "X-C19-01：对一个任务先做单体基线，再设计最小三角色军团，比较质量、成本、延迟和失败面。"
red_team_failure_requirements:
  - "任务不可分解时仍强行多Agent，要求识别负收益。"
  - "角色共享身份、记忆或权限导致串线，必须暴露。"
  - "委员会一致但事实错误时，不能把共识当正确。"
definitions_not_to_repeat:
  - "C03 MAT-L0—MAT-L5成熟度"
  - "C20 路由、让位、Handoff"
  - "C21 A2A和信任"
estimated_length: "16000-22000 中文字符"
writing_difficulty: "4/5：旧材料强，但需用成本基线约束军团叙事。"
p0_risks:
  - "P0-02：组织模式与后章路由定义冲突。"
  - "P0-07：无单体对照和净收益证据。"
  - "P0-15：以Agent数量或复杂度宣称领先。"
```

## C20 路由、让位、交接与并发

```yaml
chapter_id: C20
volume_id: V07
title: "路由、让位、交接与并发"
content_role: system
principle_owner: routing-handoff-concurrency
depends_on: [C06, C09, C14, C17, C19]
feeds_into: [C21, C22, C23, C26]
must_answer:
  - "路由如何同时考虑能力、权限、负载、成本和时效？"
  - "让位怎样成为不抢答、不越界、不伪装胜任的能力？"
  - "Handoff 必须传递哪些状态、证据、风险和未完成项？"
  - "并发共享状态、合并点、取消和冲突裁决怎样设计？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-03/模块4-Routing-Bindings-为什么谁该答是系统路由问题.md"
  - "../openclaw-silicon-life-handbook/volume-07/模块1-路由系统-谁该答的第一道闸门.md"
  - "../openclaw-silicon-life-handbook/volume-07/模块2-Handoff协议-交接棒比谁跑得快更重要.md"
  - "../openclaw-silicon-life-handbook/volume-07/模块3-让位协议-不抢答比能回答更重要.md"
  - "chapters/06-coordination/06-协同军团.md"
primary_external_evidence:
  - "A2A Protocol, Specification"
  - "OpenClaw, Multi-agent routing"
  - "Nous Research, Subagent delegation"
platform_mapping:
  openclaw: "bindings、session creator provenance、delegation、queues和共享工作区。"
  hermes: "profile/bot/subagent选择、tool继承与session lineage。"
  muse: "subagent公开叙述仅作 VENDOR-CLAIM，未知处写未知。"
  standards: "Handoff产物对齐A2A任务语义，但让位协议属于本书方法。"
bionic_theme: "注意力分配、团队交班与并行劳动；边界是 Agent 沉默不等于完成让位。"
main_case_type: "桥接案例：交接无 ACK、重复投递和并发写冲突造成掉棒。"
required_artifacts:
  - "A-C20-01 路由策略"
  - "A-C20-02 Handoff卡"
  - "A-C20-03 并发合并协议"
artifact_embeds:
  - "胜任、负载、权限、让位与停止进入路由策略；目标、状态、版本、权限、证据、ACK进入Handoff卡；并发、取消、重复、合并与冲突进入并发合并协议。"
main_exercise: "X-C20-01：把任务拆成两个可并发子任务，完成路由、交接、取消和合并，并注入一次重复交付与一次冲突。"
red_team_failure_requirements:
  - "必须测试越权路由、伪装胜任和负载过载。"
  - "无ACK、部分完成或证据缺失时不得判交接成功。"
  - "重复执行必须通过幂等键或人工裁决避免双重副作用。"
definitions_not_to_repeat:
  - "C06 Binding与Queue系统位置"
  - "C19 组织模式"
  - "C21 Task/Message/Artifact与信任"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：异步、并发和权限错误难以用静态文字讲清。"
p0_risks:
  - "P0-02：另造不兼容Handoff格式。"
  - "P0-05：缺取消、幂等、合并和恢复。"
  - "P0-06：路由越过授权边界。"
  - "P0-14：交接只存在聊天消息。"
```

## C21 A2A、产物协议与信任系统

```yaml
chapter_id: C21
volume_id: V07
title: "A2A、产物协议与信任系统"
content_role: system
principle_owner: a2a-artifact-trust
depends_on: [C03, C07, C15, C17, C19, C20]
feeds_into: [C22, C24, C26]
must_answer:
  - "Task、Message、Event 和 Artifact 为什么必须分离？"
  - "状态转移、流式输出、取消、超时和推送怎样可靠表达？"
  - "Agent Card 能发现什么，为什么不能直接建立信任？"
  - "产物来源、所有者、版本、签名、验收和动态信任怎样连接？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-07/模块3-Agent-to-Agent协同协议.md"
  - "../openclaw-silicon-life-handbook/volume-07/附录A-v2026.9-A2A协议补丁.md"
  - "../openclaw-silicon-life-handbook/volume-07/模块4-治理账本-没有账本就没有真正的治理.md"
  - "../openclaw-silicon-life-handbook/volume-07/模块5-信任体系-相信它比它会做更重要.md"
  - "../v4.0/09-a2a-binding/"
primary_external_evidence:
  - "A2A Protocol, Specification"
  - "A2A Project, v1.0.1 release"
  - "NIST, Identity and authority of software agents"
platform_mapping:
  openclaw: "ACP/A2A能力、agent/binding/session与artifact承载，需固定版本核验。"
  hermes: "subagent和gateway能力映射；不声称无测试的A2A兼容。"
  muse: "若无公开协议事实则标不适用/未知，不为填表推断。"
  standards: "A2A定义协议语义；SLCP、信誉分和功绩簿标METHODOLOGY。"
bionic_theme: "语言、契约、作品和声誉：声明能力不等于值得信任。"
main_case_type: "互操作实验：两个实现交换任务和产物，并处理超时、取消和不可信 Agent Card。"
required_artifacts:
  - "A-C21-01 Agent Card审查表"
  - "A-C21-02 任务状态机"
  - "A-C21-03 产物契约与信任记录"
artifact_embeds:
  - "Agent Card来源、能力、版本和验证进入审查表；Task/Message状态、取消和失败隔离进入任务状态机；Artifact信封、验收合同、治理账本和动态信任信号进入产物契约与信任记录。"
main_exercise: "X-C21-01：运行一条跨 Agent 任务，验证发现、协商、流式状态、取消、产物验收和失败隔离。"
red_team_failure_requirements:
  - "必须测试伪造、过期或夸大能力的Agent Card。"
  - "签名有效但产物内容错误时仍须失败。"
  - "信誉分不得自动授予敏感权限；需防刷分、串谋和申诉缺失。"
definitions_not_to_repeat:
  - "C20 路由和Handoff格式"
  - "C22 身份、签名、授权和威胁模型"
  - "C23 可观测事件链"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：协议、身份、产物和本书原创信任模型交叉。"
p0_risks:
  - "P0-03：动态规范或兼容性无版本。"
  - "P0-05：异步任务无取消、超时和恢复。"
  - "P0-06：Agent Card或信誉分冒充授权。"
  - "P0-09：三平台能力被臆测。"
```

## C22 安全模型与信任边界

```yaml
chapter_id: C22
volume_id: V08
title: "安全模型与信任边界"
content_role: governance
principle_owner: agent-security-model
depends_on: [C05, C06, C14, C15, C17, C20, C21]
feeds_into: [C23, C24, C25, C26, C27]
must_answer:
  - "为什么模型、外部内容、工具描述和Skill都不能完全信任？"
  - "身份、委托、权限、凭证、会话、数据、主机和网络边界如何建模？"
  - "最小权限、职责分离、短期授权、沙箱、审批、出口控制和审计如何纵深防御？"
  - "高风险动作、Prompt Injection和供应链攻击怎样测试与止损？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-05/模块5-主动性边界-越主动不等于越好.md"
  - "../openclaw-silicon-life-handbook/volume-06/模块6-自动化治理边界-没有边界就没有安全.md"
  - "chapters/05-governance/05-治理系统.md"
  - "EDITORIAL-AUDIT.md#4-2026-9必须补上的现代工程层"
primary_external_evidence:
  - "NIST, Identity and authority of software agents"
  - "OWASP, Top 10 for Agentic Applications for 2026"
  - "OpenClaw, Security trust model and Sandbox modes"
  - "Nous Research, Security"
  - "Meta, How we built safety into Muse"
platform_mapping:
  openclaw: "单Gateway信任边界、auth、policy、sandbox mode/scope/backend、approvals、secrets和audit。"
  hermes: "allowlist/pairing、dangerous-command approval、write safety、containers、credential filtering。"
  muse: "runtime cell、Sentinel、privsep、authd、egress gate均标 VENDOR-CLAIM。"
  standards: "NIST/OWASP/MCP构成通用基线；不做绝对安全排名。"
bionic_theme: "皮肤、免疫、抑制与痛觉：多层防御限制损害，不承诺永不感染。"
main_case_type: "沙箱红队：间接注入诱导读取凭证并外发，比较三层控制是否拦截。"
required_artifacts:
  - "A-C22-01 威胁模型"
  - "A-C22-02 权限与凭证矩阵"
  - "A-C22-03 红队测试包"
artifact_embeds:
  - "资产、主体、攻击面和信任边界进入威胁模型；身份、委托、scope、凭证和高风险门禁进入权限与凭证矩阵；攻击步骤、预防、检测、止损、恢复和残余风险进入红队测试包。"
main_exercise: "X-C22-01：在隔离环境运行提示注入、恶意工具和凭证外泄三类攻击，记录预防、检测、止损和恢复。"
red_team_failure_requirements:
  - "必须覆盖直接/间接Prompt Injection、工具污染和Skill供应链。"
  - "必须尝试跨会话、跨Agent和共享Gateway的数据/权限串线。"
  - "任何外发、资金、删除、身份和生产变更只到模拟或逐次人工审批。"
  - "不得宣称Prompt Injection根治或Secure VM不可攻破。"
definitions_not_to_repeat:
  - "C05 行为契约"
  - "C14 工具合同"
  - "C17 自主等级"
  - "C21 Agent Card与产物协议"
estimated_length: "20000-24000 中文字符"
writing_difficulty: "5/5：历史材料薄弱、风险最高，需大量新证据与实测。"
p0_risks:
  - "P0-03：安全保证无威胁模型、版本或残余风险。"
  - "P0-05：防护无止损和恢复。"
  - "P0-06：提示词代替认证、授权或隔离。"
  - "P0-09：把Meta自述写成独立证明。"
  - "P0-13：高危泄露被综合分抵消。"
```

## C23 可观测性、成本与可靠性

```yaml
chapter_id: C23
volume_id: V08
title: "可观测性、成本与可靠性"
content_role: governance
principle_owner: observability-reliability-economics
depends_on: [C06, C07, C09, C14, C16, C20, C22]
feeds_into: [C24, C25, C26, C27]
must_answer:
  - "如何从业务承诺定义 SLI、SLO 和错误预算？"
  - "任务、轨迹、模型/工具调用、审批、交接、终态和结果如何连成证据链？"
  - "Token、工具、人工复核、延迟和机会成本如何计算？"
  - "超时、重试、降级、断点续作、故障隔离和事故回流如何设计？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-05/模块6-长期稳定性检查清单-如何每周给agent做体检.md"
  - "../openclaw-silicon-life-handbook/volume-06/模块3-三证验真-没有证据就不是完成.md"
  - "_appendix-case/01-real-incidents.md#CASE-1-CASE-2-CASE-4-CASE-5"
  - "_appendix-case/02-production-patterns.md#CASE-7-CASE-9-CASE-10"
  - "_appendix-sop/06-incident-recovery-sop.md"
primary_external_evidence:
  - "OpenAI, Evaluate agent workflows"
  - "Anthropic, Demystifying evals for AI agents"
  - "OpenClaw, OpenTelemetry export"
  - "OpenTelemetry, Generative AI semantic conventions"
platform_mapping:
  openclaw: "logs、audit、OTel、Prometheus、doctor、health、restart recovery。"
  hermes: "session DB、cron execution DB、gateway logs和doctor。"
  muse: "activity log、permissions UI和audit trail仅作公开产品案例。"
  standards: "正文固定观测语义，不固定演进中的OTel字段名。"
bionic_theme: "生命体征、代谢与疼痛信号：观测不是日志越多，而是能定位状态与代价。"
main_case_type: "CASE-1/2/4 的匿名化事故链，补故障注入和修复后长期追踪。"
required_artifacts:
  - "A-C23-01 观测事件模型"
  - "A-C23-02 SLI/SLO与成本看板"
  - "A-C23-03 故障注入报告"
artifact_embeds:
  - "任务、轨迹、工具、审批、产物、终态和关联ID进入观测事件模型；错误预算、成本、延迟和容量进入SLI/SLO与成本看板；注入、发现、止损、RCA、恢复和防复发进入故障注入报告。"
main_exercise: "X-C23-01：注入空响应、重复调用和队列积压，完成发现、止损、恢复、成本核算和训练回流。"
red_team_failure_requirements:
  - "必须测试HTTP 200但空body、scheduler成功但未交付等假成功。"
  - "重试必须检查重复扣费、发送、写入和删除。"
  - "恢复必须验证环境终态，不得只恢复文件或进程。"
  - "只报告平均值而隐藏尾部失败必须退稿。"
definitions_not_to_repeat:
  - "C07 离线评估系统"
  - "C16 自动化状态机"
  - "C22 安全威胁模型"
  - "C24 发布和生命周期"
estimated_length: "20000-24000 中文字符"
writing_difficulty: "5/5：需要连接工程、业务、成本和事故证据。"
p0_risks:
  - "P0-03：动态OTel字段被写成永久标准。"
  - "P0-04：诊断命令未核验。"
  - "P0-05：重试、恢复或回滚不完整。"
  - "P0-07：SLI无对象、阈值和裁判。"
  - "P0-14：事故证据不可解引用。"
```

## C24 治理、发布与全生命周期问责

```yaml
chapter_id: C24
volume_id: V08
title: "治理、发布与全生命周期问责"
content_role: governance
principle_owner: lifecycle-governance
depends_on: [C05, C06, C13, C15, C18, C21, C22, C23]
feeds_into: [C25, C26, C27]
must_answer:
  - "业务、技术、数据和风险所有者如何分工并承担最终责任？"
  - "契约、模型、工具、Skill、记忆和策略如何统一变更管理？"
  - "版本锁定、迁移、影子、灰度、上岗、回滚怎样形成发布系统？"
  - "降级、暂停、退役、凭证撤销、数据处置和经验继承怎样执行？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-06/"
  - "../v4.0/volume-06/"
  - "chapters/05-governance/05-治理系统.md"
  - "chapters/11-plugin-entrypoint/"
  - "_appendix-sop/06-incident-recovery-sop.md"
primary_external_evidence:
  - "OpenClaw, Versioned state and guarded upgrades"
  - "OpenClaw, Restart recovery"
  - "NIST, Identity and authority of software agents"
  - "Nous Research, Architecture and Profiles"
platform_mapping:
  openclaw: "backup、doctor、guarded upgrade、restart recovery、rollback和owner边界。"
  hermes: "quick backup、session/cron persistence、profiles与升级迁移。"
  muse: "audit、permission revocation和托管生命周期仅作 VENDOR-CLAIM。"
  standards: "隐私、知识产权和法律义务需专业复核，平台文档不替代法律意见。"
bionic_theme: "成长、医疗、复职与退役：系统生命期必须包含退出和遗产处置。"
main_case_type: "受控升级与退役案例：状态迁移失败后回滚，并验证凭证和数据处置。"
required_artifacts:
  - "A-C24-01 责任矩阵"
  - "A-C24-02 发布与升级计划"
  - "A-C24-03 备份恢复证明"
  - "A-C24-04 退役清单"
artifact_embeds:
  - "四类所有者与RACI进入责任矩阵；变更、依赖、兼容、影子、灰度、发布和回滚进入发布与升级计划；备份范围、恢复演练和RTO/RPO证据进入备份恢复证明；暂停、撤权、数据处置和替代进入退役清单。"
main_exercise: "X-C24-01：在复制环境完成一次模型或Skill升级，执行兼容检查、灰度、故障回滚和退役数据处置。"
red_team_failure_requirements:
  - "必须测试升级后状态不兼容、隐式权限扩大和回滚失效。"
  - "凭证撤销后验证旧会话、缓存和备份不能继续越权使用。"
  - "License、隐私或版权状态不清时必须进入人工专业复核。"
definitions_not_to_repeat:
  - "C18 自我改进流程"
  - "C22 安全控制"
  - "C23 事故与可靠性指标"
  - "C27 再认证决定"
estimated_length: "20000-24000 中文字符"
writing_difficulty: "5/5：跨技术、组织、数据与法律责任。"
p0_risks:
  - "P0-03：升级和合规事实缺版本或专业来源。"
  - "P0-04：迁移/回滚命令未固定版本实测。"
  - "P0-05：发布无回滚或退役无数据处置。"
  - "P0-06：责任写给Agent而非人类所有者。"
  - "P0-10：案例、代码或材料版权不清。"
```

## C25 30 天训虾训练营

```yaml
chapter_id: C25
volume_id: V09
title: "30 天训虾训练营"
content_role: capability
principle_owner: thirty-day-curriculum
depends_on: [C04, C05, C06, C07, C08, C09, C13, C14, C15, C16, C17, C18, C19, C20, C21, C22, C23, C24]
feeds_into: [C26, C27]
must_answer:
  - "五个阶段怎样从岗位与基线推进到训练、真实任务、红队和毕业？"
  - "每天/每周需要什么前置、权限、产物、证据和停止条件？"
  - "六类毕业证据包怎样组装并被独立复核？"
  - "何时延期、停训、降级或退出，而不是强行在30天毕业？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-04/模块7-从新人虾到专家虾的完整路径.md"
  - "../openclaw-silicon-life-handbook/volume-04/卷四总复盘-从会聊到能战的完整训练体系.md"
  - "_appendix-case/02-production-patterns.md#CASE-8"
  - "_appendix-cookbook/04-training-rounds.md"
  - "_appendix-sop/"
primary_external_evidence:
  - "Anthropic, Demystifying evals for AI agents"
  - "Anthropic, Trustworthy agents in practice"
  - "NIST CAISI, Guidelines"
  - "OWASP, Top 10 for Agentic Applications for 2026"
platform_mapping:
  openclaw: "主训练路线，使用固定版本组件与附录命令。"
  hermes: "提供同原理异实现的迁移变式，不复制OpenClaw命令。"
  muse: "只设计公开产品可完成的用户侧练习，不进行内部配置假设。"
  standards: "30天是课程编排，不是能力形成自然定律。"
bionic_theme: "教育、实习与住院医式渐进授权：成长节律因岗位和个体而异。"
main_case_type: "至少一个真实 Agent 的30天纵向案例，保留完整基线、训练、留出、红队和毕业证据。"
required_artifacts:
  - "A-C25-01 30天训练计划"
  - "A-C25-02 每日训练日志"
  - "A-C25-03 毕业证据包"
artifact_embeds:
  - "课程日历、阶段门禁和停止规则进入训练计划；每日输入、行为、反馈、版本、失败与恢复进入日志；六类证据及上岗/限域/延期/停训建议进入毕业证据包，正式认证仍由C24决定。"
main_exercise: "X-C25-01：真实跑完30天或按同一标准记录未完成原因；不得只提供纸面课程设计。"
red_team_failure_requirements:
  - "第22-30天必须包含权限、注入、故障、迁移和成本压力测试。"
  - "某一安全关键门禁失败时不得靠总分毕业。"
  - "训练数据污染留出集时必须重建评测并标记本轮无效。"
  - "能力不足、风险过高或资源超限必须允许停训。"
definitions_not_to_repeat:
  - "C04 能力模型"
  - "C07 评估系统"
  - "C08 训练循环"
  - "C17 自主等级"
  - "C22 安全门禁"
  - "C27 认证规则"
estimated_length: "20000-24000 中文字符"
writing_difficulty: "5/5：高度综合且必须真实试跑，不能靠编排代替证据。"
p0_risks:
  - "P0-01：任何阶段、小节、练习或交接缺失。"
  - "P0-05：训练动作无停止与回滚。"
  - "P0-07：无基线、留出、红队或独立复核。"
  - "P0-13：安全失败仍毕业。"
  - "P0-14：证据包只在聊天中存在。"
```

## C26 案例实验室：成功、失败与迁移

```yaml
chapter_id: C26
volume_id: V09
title: "案例实验室：成功、失败与迁移"
content_role: system
principle_owner: case-evidence-lab
depends_on: [C07, C08, C09, C19, C20, C21, C22, C23, C24, C25]
feeds_into: [C27]
must_answer:
  - "一个可发表案例需要哪些环境、版本、任务、过程、产物、指标与限制？"
  - "怎样区分真实、匿名真实、合成、重建和厂商案例？"
  - "成功、失败、迁移和反事实如何共同产生指导意义？"
  - "如何在同任务、同预算、同风险边界下复现比较？"
legacy_sources:
  - "_appendix-case/01-real-incidents.md"
  - "_appendix-case/02-production-patterns.md"
  - "chapters/00-front/00-总论.md#四个现场片段"
  - "../openclaw-silicon-life-handbook/INDEX.md#实战案例库"
  - "../v5.0-framework-proposal.md#案例库"
primary_external_evidence:
  - "Anthropic, Demystifying evals for AI agents"
  - "NIST, Cheating on AI agent evaluations"
  - "OpenAI, Evaluate agent workflows"
platform_mapping:
  openclaw: "本地可复现主案例，需固定版本、匿名化和重跑。"
  hermes: "至少一个迁移或对照案例，使用相同任务与预算。"
  muse: "仅作明确标注的厂商产品案例，不充当独立安全证据。"
  standards: "协议案例需记录规范版本和实现差异。"
bionic_theme: "临床病例与实验室复现：病例提供线索，不自动证明普遍因果。"
main_case_type: "案例组合：单体、军团、失败、跨域迁移和平台对照，含贯穿案例。"
required_artifacts:
  - "A-C26-01 三案复现包"
  - "A-C26-02 失败解剖报告"
  - "A-C26-03 跨平台迁移矩阵"
artifact_embeds:
  - "三案八段式档案、匿名授权、环境清单和复现步骤进入三案复现包；失败、代价、选择偏差和不可复现部分进入失败解剖；跨案例模式和不可迁移边界进入跨平台迁移矩阵。"
main_exercise: "X-C26-01：选择一个历史案例，回到原始证据重建、匿名化、重跑，并由第二评审者复现关键结论。"
red_team_failure_requirements:
  - "必须检查时间线倒推、幸存者偏差、选择性报告和因果过度解释。"
  - "营销演示、单次成功或无法解引用的数字不得成为强证据。"
  - "隐私、密钥、chat id、机器路径、客户信息和版权必须审查。"
definitions_not_to_repeat:
  - "C07 评估规则"
  - "C23 事故与可靠性方法"
  - "C27 认证标准"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：素材丰富，但证据复核、匿名化和可复现性工作量大。"
p0_risks:
  - "P0-03：历史数字或因果缺来源和作用域。"
  - "P0-07：案例无基线、对照和失败分布。"
  - "P0-10：案例类型、隐私、授权或版权不清。"
  - "P0-15：用最佳案例宣称普遍领先。"
```

## C27 成熟度、毕业、晋级与持续认证

```yaml
chapter_id: C27
volume_id: V09
title: "成熟度、毕业、晋级与持续认证"
content_role: certification
principle_owner: maturity-certification
depends_on: [C03, C07, C08, C17, C18, C22, C23, C24, C25, C26]
feeds_into: []
must_answer:
  - "MAT-L0—MAT-L5 完整量表如何覆盖个体与多 Agent 组织？"
  - "毕业、晋级、授权和认证是什么关系，哪些必须分离？"
  - "认证作用域、有效期、重大变更重测、周期复审和撤销如何执行？"
  - "盲测、留出、红队、生产监控、人工审阅和外部评审如何汇总决定？"
legacy_sources:
  - "../openclaw-silicon-life-handbook/volume-04/模块1-从入门到业内最佳实践的进化阶梯.md"
  - "../openclaw-silicon-life-handbook/volume-04/模块7-从新人虾到专家虾的完整路径.md"
  - "../openclaw-silicon-life-handbook/volume-07/模块5-信任体系-相信它比它会做更重要.md"
  - "chapters/03-training/03-训练流程.md"
  - "EDITORIAL-AUDIT.md#6-行业最强的可发表改写"
primary_external_evidence:
  - "Anthropic, Demystifying evals for AI agents"
  - "NIST CAISI, Guidelines"
  - "OWASP, Top 10 for Agentic Applications for 2026"
  - "NIST, Identity and authority of software agents"
platform_mapping:
  openclaw: "以固定版本的能力、安全、可靠性和治理证据执行认证。"
  hermes: "使用同一原理、独立实现材料进行迁移认证，避免配置同构假设。"
  muse: "只能评价公开可观察行为与用户侧证据，不认证未公开内部控制。"
  standards: "MAT-L0—MAT-L5属于本书METHODOLOGY；认证只在声明范围内有效。"
bionic_theme: "执照、晋级与继续教育：认证是有期限的责任许可，不是永久身份。"
main_case_type: "独立盲测认证：一个个体 Agent 与一个多 Agent 组织分别接受挑战、复审和撤销演练。"
required_artifacts:
  - "A-C27-01 成熟度评分表"
  - "A-C27-02 认证报告"
  - "A-C27-03 再认证与撤证记录"
artifact_embeds:
  - "MAT-L0—MAT-L5完整评分写入成熟度评分表；个体/组织结论、manifest、平台版本、任务、预算、风险和作用域写入认证报告；重测、暂停、撤销、申诉和再认证进入再认证与撤证记录。"
main_exercise: "X-C27-01：由独立评审者使用留出任务、红队和生产证据完成认证；随后模拟重大变更并触发重测或撤销。"
red_team_failure_requirements:
  - "必须测试训练集污染、模型裁判偏差、最佳样本选择和证据伪造。"
  - "任何安全关键失败必须覆盖总分，结果只能FAIL或REVIEW_REQUIRED。"
  - "信誉分、功绩或历史成功不得永久扩大权限或免除重测。"
  - "Muse等不可观测内部维度不得被推测认证。"
definitions_not_to_repeat:
  - "C03 七维强者标准和成熟度概览"
  - "C07 测试与裁判系统"
  - "C17 授权等级"
  - "C22 安全门禁"
  - "C24 发布与退役责任"
estimated_length: "18000-24000 中文字符"
writing_difficulty: "5/5：全书终审接口，依赖所有上游证据且不能自我认证。"
p0_risks:
  - "P0-02：另造等级、维度或毕业规则。"
  - "P0-03：认证结论无版本、作用域和有效期。"
  - "P0-07：无独立裁判、留出或重测。"
  - "P0-09：认证不可观测平台内部控制。"
  - "P0-13：安全失败被总分抵消。"
  - "P0-15：认证被宣传成绝对行业最强。"
```

## 25. 概念所有权总表

| 章节 | principle_owner | 主定义 | 其他章节只允许 |
|---|---|---|---|
| C01 | `agent-system-boundary` | Agent 系统边界与硅基生命隐喻边界 | 引用对象定义 |
| C02 | `training-paradigm` | 训虾范式、三系统总关系、双闭环 | 调用范式，不重画总图 |
| C03 | `strength-standard` | 七维强者标准、成熟度概览、三证 | 使用评分，不改维度 |
| C04 | `role-capability-model` | 岗位、JTBD、能力树和负面清单 | 消费能力模型 |
| C05 | `life-contract-system` | 七大生命契约 | 调用具体契约 |
| C06 | `runtime-container-architecture` | 六层运行容器架构 | 引用组件位置 |
| C07 | `evaluation-system` | 测试集、grader、统计门禁 | 使用测试和结果 |
| C08 | `training-loop` | 双三角、轮次、矫正和停训 | 执行训练循环 |
| C09 | `work-interaction-system` | 任务卡、上下文包、检查点、交付三证 | 生成或消费工作包 |
| C13 | `context-memory-engineering` | 上下文与记忆分类、生命周期 | 使用记忆策略 |
| C14 | `tool-mcp-engineering` | 工具合同、风险级别与MCP边界 | 调用工具合同 |
| C15 | `skill-supply-chain` | Skill封装、注册、供应链与撤回 | 引用技能合同 |
| C16 | `proactive-signal-system` | 信号类型、自动化状态机、安静策略 | 配置具体信号 |
| C17 | `autonomy-authorization-model` | 自主阶梯与审批门 | 设定任务权限，不扩级 |
| C18 | `drift-improvement-governance` | 漂移分类与受控改进回路 | 发现漂移、提交提案 |
| C19 | `multi-agent-organization-design` | 多Agent使用条件和组织模式 | 应用组织模式 |
| C20 | `routing-handoff-concurrency` | 路由、让位、交接与并发格式 | 生成交接产物 |
| C21 | `a2a-artifact-trust` | A2A语义、Artifact合同和信任信号 | 引用协议和产物 |
| C22 | `agent-security-model` | 威胁模型、信任边界和安全门禁 | 应用安全控制 |
| C23 | `observability-reliability-economics` | SLI/SLO、事件链、成本与事故方法 | 提交观测证据 |
| C24 | `lifecycle-governance` | 所有者、发布、迁移、退役和数据处置 | 触发生命周期流程 |
| C25 | `thirty-day-curriculum` | 30天课程编排与阶段门禁 | 提供练习和产物 |
| C26 | `case-evidence-lab` | 案例分类、复现包与证据标准 | 提交案例，不改方法 |
| C27 | `maturity-certification` | 完整认证、有效期、撤销与再认证 | 引用认证结论 |

## 26. 合并顺序与并行边界

```text
C01 → C02 → C03
               ├→ C04 → C05 → C06
               │              ├→ C13/C14/C15/C16
               └→ C07 → C08 → C09

C16 → C17 → C18
C19 → C20 → C21
C05—C21 → C22 → C23 → C24
C04—C24 → C25 → C26 → C27
```

- C13、C14、C15 可在 C06、C07 稳定后并行。
- C16—C18 必须按顺序；C19—C21 必须按顺序。
- C22 可提前研究，但正文合并前必须吸收 C05、C06、C14、C15、C17、C20、C21 的攻击面。
- C25—C27 不得因稿期提前定稿；它们必须消费已经通过实战门的上游产物。

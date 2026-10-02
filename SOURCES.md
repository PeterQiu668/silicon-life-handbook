# 来源、证据与版本账本

> 复核日期：2026-10-01（Asia/Shanghai）  
> 用途：本文件不是“参考链接堆积”，而是全书事实主张的证据边界。主稿中的 `[Sxx]` 均指向这里。

## 1. 证据等级

| 标签 | 含义 | 可以怎样写 |
|---|---|---|
| `VERSION-FACT` | 固定版本、提交或 release 中的事实 | “在版本 X 中……” |
| `OFFICIAL-GUIDANCE` | 官方规范、文档或正式说明 | “规范规定”“官方说明” |
| `LOCAL-VALIDATION` | 在声明环境与固定输入中复现 | “本地固定夹具显示……” |
| `METHODOLOGY` | 本书作者提出或采用的方法、模型或命名 | “本书定义”“建议采用” |
| `PROJECT-DECISION` | 为本书内部一致性作出的决定 | “本版统一采用……” |
| `INFERENCE` | 由多个事实推导的编辑或工程判断 | “据此推断”“更适合” |
| `VENDOR-CLAIM` | 厂商公开说明但未被本书独立验证 | “厂商说明……，仍需独立验证” |

纪律：`METHODOLOGY` 不能伪装成行业标准；证据不足统一停在 `REVIEW_REQUIRED`；`VENDOR-CLAIM` 不能写成独立验证；版本性事实必须带复核日期和失效触发器。

## 2. 三门课程：历史启发与权利隔离

> **出版硬门（2026-10-01）**：S01—S03 仅保留为作者探索史线索。三页均未取得逐字稿，也未取得课程作者对出版改编的明确授权，统一标记 `RIGHTS-BLOCKED`。正式书稿不得把页面章节要点、课程结构或课程专有表达作为核心框架的事实依据；“三系统模型”“双三角模型”在本版已按本书任务工程、控制回路和证据体系独立重构，并必须能够在移除 S01—S03 后完整成立。获得书面授权与可核材料前，S01—S03 不进入正文引用、图表、练习答案或营销主张。

### S01 · 训虾实验（上）

- 页面：<https://www.douyin.com/video/7620753055872552243>
- 标题：拒绝龙虾慢养！我借鉴《黑客帝国》灵感，手搓了套练虾系统（上）
- 发布页显示日期：2026-03-24。
- 页面“章节要点”显示：流派辨析、集中训练与专业体系、实验方案、教练机制、工作模型、双三角模型和实验结果。
- 历史影响：曾触发作者对能力建模、导师 Agent、训练轮次、基线与对照评测的探索；不作为本版方法成立的证据。
- 权利与使用状态：`rights_status=RIGHTS-BLOCKED`、`use_in_formal_manuscript=false`、`core_method_dependency=PROHIBITED`、`source_observation_kind=PLATFORM_PAGE_METADATA`、`transcript_status=NOT_AVAILABLE`、`author_approval=NOT_OBTAINED`。
- 证据边界：页面标题与平台生成的章节要点只能证明“作者曾看到这条线索”，不能证明课程正文、实验结果、原创边界或授权范围。

### S02 · 训虾实验（下）

- 页面：<https://www.douyin.com/video/7620755700175605019>
- 标题：拒绝龙虾慢养！我借鉴《黑客帝国》灵感，手搓了套练虾系统（下）
- 发布页显示日期：2026-03-25。
- 页面“章节要点”显示：将目标拆成评估系统、训练系统、交互系统，并用商业计划书、营销文案与战略分析任务演示能力变化。
- 历史影响：曾触发作者思考评估、训练、交互之间的闭环；正式版“三系统模型”现由任务工程、反馈控制和人机交互证据独立论证。
- 权利与使用状态：同 S01，`RIGHTS-BLOCKED`，不得作为核心方法依赖。

### S03 · AI 原生协作系统

- 页面：<https://www.douyin.com/video/7616279711525768463>
- 标题：狂肝8天，我给龙虾从头手搓了一个AI版飞书！全程细节演示！
- 发布页显示日期：2026-03-12。
- 页面“章节要点”显示：以 AI 为中心设计通信、协作、上下文、员工与项目空间，并把 Agent 视为高阶员工而非聊天框。
- 历史影响：曾触发作者思考 Agent 原生协作环境；正式版协作模型现由 Task、Artifact、Handoff、authority 与状态终态的独立工程分析建立。
- 权利与使用状态：同 S01，`RIGHTS-BLOCKED`，不得作为核心方法依赖。

## 3. OpenClaw 固定基线

### S10 · 书稿固定实现基线与当前最新发行快照

- 主仓：<https://github.com/openclaw/openclaw>
- 书稿固定发行：<https://github.com/openclaw/openclaw/releases/tag/v2026.9.6>；固定提交：[`eb377ac59e6c9fd6c7705028034812becf00271b`](https://github.com/openclaw/openclaw/commit/eb377ac59e6c9fd6c7705028034812becf00271b)。
- 固定实现基线：`2026.9.6`。书中命令、组件、配置、状态与控制事实继续以这一提交为边界。
- 本机辅助复现：`openclaw --version` → `OpenClaw 2026.9.6 (eb377ac)`；主事实身份仍是 `VERSION-FACT`，`LOCAL-VALIDATION` 只覆盖该命令在该主机的输出。
- 截至 2026-10-01 的 npm `latest` 与 GitHub latest release：`2026.9.7`；发行页：<https://github.com/openclaw/openclaw/releases/tag/v2026.9.7>；发布时间：`2026-09-30T04:44:14Z`；peeled commit：[`c074824a27c96d3983043f9eeb33823cd1772d8c`](https://github.com/openclaw/openclaw/commit/c074824a27c96d3983043f9eeb33823cd1772d8c)。
- 边界：`2026.9.7` 是当前最新发行快照，不是本书实现基线。本版没有把 24 章、附录和运行包整体迁移到 9.7；任何升级结论都必须经过差异、回归、安全与恢复复核。
- 主事实身份：`VERSION-FACT`；辅助验证字段：`local_version_observation=captured`、`baseline_migration=NOT_PERFORMED`。

### S11 · OpenClaw 安全模型

- 固定文档：<https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/SECURITY.md>
- 关键事实：OpenClaw 是 trusted-operator、local-first 的单信任边界基础设施；模型不是可信主体；安全边界来自认证、工具策略、审批、沙箱和主机/配置隔离。默认 host-first 执行不等于沙箱。
- 本书含义：`SOUL.md`、`AGENTS.md`、人格承诺和提示词只能形成行为约束，不能替代系统权限与隔离。
- 等级：`OFFICIAL-GUIDANCE` + 固定源码复核。

### S12 · 记忆来源与删除边界

- 固定文档：<https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/memory-provenance.md>
- 关键事实：自动记忆可记录来源会话谱系；排除未来摄入与删除既有产物是不同操作；`memory forget` 有明确覆盖边界，并不等于删除原始会话或所有自由写入副本。
- 本书含义：记忆治理至少要包含来源、准入、保留、召回、纠错和删除六个环节。
- 等级：`OFFICIAL-GUIDANCE`。

### S13 · Skill 与渐进披露

- 固定文档：<https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/tools/skills.md>
- 本书含义：Skill 是按需发现和加载的程序性知识单元，不应把所有技能全文常驻上下文。
- 等级：`OFFICIAL-GUIDANCE`。

### S14 · 团队与边界

- 固定文档：<https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/start/teams.md>
- 本书含义：团队部署首先是信任边界和角色隔离问题，其次才是“多几个 Agent”。
- 等级：`OFFICIAL-GUIDANCE`。

### S15 · Hermes 第二开放实现

- 官方仓库：<https://github.com/NousResearch/hermes-agent>。
- 固定发行：<https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.13>；固定提交：[`f80f453ae0679347e38abc917c7f94f717bf96c5`](https://github.com/NousResearch/hermes-agent/commit/f80f453ae0679347e38abc917c7f94f717bf96c5)。
- 固定基线：Hermes Agent `0.20.1` / `v2026.8.13` / `f80f453ae0679347e38abc917c7f94f717bf96c5`。
- 本书用途：验证七大生命契约、Session、Memory、Skills、Plugins、Cron、Gateway、Delegation 和安全原则能否跨 OpenClaw 迁移。
- 边界：本来源项没有登记可定位的 Hermes 本地运行 transcript 或 run artifact，因此不赋予 `LOCAL-VALIDATION` 身份。固定源码不证明真实凭证、真实网络、真实权限和生产外部效果；平台同名对象不得机械等同。
- 主事实身份：`VERSION-FACT`；动态官方文档另按 `OFFICIAL-GUIDANCE` 使用；真实实践结论仍为 `REVIEW_REQUIRED`。

### S16 · Meta Muse 托管式 Agent

- 发布：<https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/>（2026-09-08）。
- 安全设计：<https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse>。
- 产品设计：<https://introducing.muse.ai/>。
- 小企业版：<https://about.fb.com/news/2026/09/introducing-muse-small-business/>（2026-09-29）。
- 本书用途：分析 Goals、Activity、Artifacts、后台工作、主动通知、Secure VM、Sentinel、privsep、authd、凭证代理、连接器、审批、审计、撤销和遗忘的托管产品设计。
- 边界：材料由 Meta 官方发布，但本书没有取得生产配置、源代码、完整审计或独立攻击结果；涉及内部实现与安全效果统一标为 `VENDOR-CLAIM`。
- 等级：`VENDOR-CLAIM`。

## 4. 行业协议与开放标准

### S20 · Model Context Protocol 2026-07-28

- 发行：<https://github.com/modelcontextprotocol/modelcontextprotocol/releases/tag/2026-07-28>
- 安全最佳实践：<https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices>
- 关键事实：MCP 是能力与上下文的互操作协议，不是权限豁免；OAuth、token audience、scope、redirect URI、per-client consent 与 confused-deputy 防护属于实现责任。
- 本书含义：连接成功不等于授权正确；工具目录必须附带风险、作用域和审批策略。
- 等级：`OFFICIAL-GUIDANCE`。

### S21 · Agent2Agent Protocol

- 发行：<https://github.com/a2aproject/A2A/releases/tag/v1.0.1>
- 固定提交：[`3303592588e388e62e0f69f701af531d2f4e3991`](https://github.com/a2aproject/A2A/commit/3303592588e388e62e0f69f701af531d2f4e3991)。
- 当前规范入口：<https://a2a-protocol.org/latest/specification/>。
- 版本纪律：本书可复现规范身份以 `v1.0.1` / 上述 commit 为准；`latest` 仅是 2026-10-01 的动态导航快照，不是可重复 release identity。实际实现仍须固定协议版本、binding、扩展与 SDK。
- 关键事实：Agent Card 声明能力与安全方案；Task 有生命周期；Message 用于交互，Artifact 用于结果；异步任务需要轮询、流或推送；客户端应先校验能力。
- 本书含义：协作必须围绕任务状态与可验收产物，不应把聊天消息当作可靠交付物。
- 等级：`OFFICIAL-GUIDANCE`。

### S22 · Agent Skills 开放规范

- 仓库：<https://github.com/agentskills/agentskills>
- 规范：<https://agentskills.io/specification>
- 可复现快照：[`69ef37e9424c0a7ea9dd2293b559e43ec8176379`](https://github.com/agentskills/agentskills/commit/69ef37e9424c0a7ea9dd2293b559e43ec8176379)，复核日 2026-10-01。
- 版本边界：复核时官方仓库没有可用 release tag；网页规范是动态页面。引用字段时以该 commit 快照为定位，动态页面仅补充核验日状态，不能单独支持跨日期复现。
- 关键事实：Skill 至少包含 `SKILL.md` 与必要 frontmatter；推荐三级渐进披露；完整 `SKILL.md` 建议小于 500 行，深度资料按需加载；不受信任项目中的技能应经过信任检查。
- 本书含义：本书本身也必须遵守渐进披露，不能要求 Agent 一次性读取 8 万多行材料。
- 等级：`OFFICIAL-GUIDANCE`。

### S23 · MCP Skills 扩展

- 规范：<https://skills.extensions.modelcontextprotocol.io/specification/stable/skills>。
- 基线：面向 MCP `2026-07-28` 或更高版本，以 `io.modelcontextprotocol/skills` 声明；通过 Resources 分发符合 Agent Skills 规范的目录。
- 本书含义：传输扩展不改变 Skill 的格式、来源、权限和供应链风险；`skill://` URI 不是可信标志。
- 等级：`OFFICIAL-GUIDANCE`。

### S24 · OpenTelemetry GenAI 与 Agent 语义约定

- OpenTelemetry 核心语义约定：<https://opentelemetry.io/docs/specs/semconv/>；固定 release tag [`v1.44.0`](https://github.com/open-telemetry/semantic-conventions/releases/tag/v1.44.0)，commit [`e10a930844c6951757a43b849d364f7d056ac32b`](https://github.com/open-telemetry/semantic-conventions/commit/e10a930844c6951757a43b849d364f7d056ac32b)。
- GenAI 独立仓库 Agent spans 固定快照：[`b31e9e8ea26ac1c086d3313d474e31d7c3f391ae`](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/docs/gen-ai/gen-ai-agent-spans.md)；动态入口：<https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md>。
- 关键事实：GenAI 约定已经从核心仓库迁出；Agent 与 framework spans 在核验日仍标为 `Development`，覆盖 create/invoke agent、workflow、plan、tool 与 Skill 相关 span。
- 本书含义：核心稳定版本与 GenAI development 快照必须分开固定；实现须准备字段迁移。input/output、system instructions 与 tool 内容默认视为敏感，不应为观测而无边界记录。
- 等级：`OFFICIAL-GUIDANCE`，成熟度边界为 `Development`。

## 5. Agent 工程与评测方法

### S30 · OpenAI Evals

- 官方指南：<https://developers.openai.com/api/docs/guides/evals>
- 关键事实：评测用于检验输出是否满足指定的内容与风格标准，并用于模型或系统变更时理解表现差异。
- 本书含义：训练成果必须由测试集、grader、留出集和回归结果证明，而不是由一次精彩演示证明。
- 等级：`OFFICIAL-GUIDANCE`。

### S31 · Anthropic：Building Effective Agents

- 官方文章：<https://www.anthropic.com/engineering/building-effective-agents>
- 关键事实：从增强 LLM 和可组合 workflow 开始，只在简单方案不足时增加自治；保持简单、透明，并认真设计和测试 agent-computer interface；evaluator-optimizer 适用于有清晰标准且迭代有可测价值的任务。
- 本书含义：多 Agent、长链路和“自主进化”不是成熟度象征；最小可用复杂度与可评测改进才是。
- 等级：`OFFICIAL-GUIDANCE`。

### S32 · Anthropic：Context Engineering 与长时 Agent Harness

- Context Engineering：<https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>。
- Long-running harness：<https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>。
- 本书用途：支持外部化工作记忆、按需加载、上下文压缩、清晰状态交接、初始化/推进双角色和长任务渐进验收。
- 边界：官方工程经验不等于所有模型和组织上的普遍因果结论；本书把它们转成可测试的计划文件、进度账本、压缩保真与恢复门。
- 等级：`OFFICIAL-GUIDANCE`。

### S33 · ReAct 与 Reflexion

- ReAct：<https://arxiv.org/abs/2210.03629>。
- Reflexion：<https://arxiv.org/abs/2303.11366>。
- 本书用途：解释推理—行动交替、环境反馈、自我反思与经验记忆的研究脉络；对应本书“观察—假设—动作—验证”和“失败记录—规则候选—独立复测”。
- 边界：研究结果不自动证明任意生产 Agent 会因增加自由文本思维或反思而更强；高风险场景仍需外部证据、确定性门和独立验证。
- 等级：`PRIMARY-RESEARCH`。

### S34 · OpenAI：Orchestration、Compaction 与 Prompt Caching

- Orchestration：<https://developers.openai.com/api/docs/guides/agents/orchestration>。
- Compaction：<https://developers.openai.com/api/docs/guides/compaction>。
- Prompt Caching：<https://developers.openai.com/api/docs/guides/prompt-caching>。
- 本书用途：对照 routing、manager/worker、上下文压缩与稳定前缀缓存；用于说明多 Agent 拆分、压缩保真和成本优化的不同控制面。
- 边界：产品 API 行为具有版本性；prompt caching 是延迟/成本优化，不等于记忆、知识库或语义正确性。
- 等级：`OFFICIAL-GUIDANCE`。

### S35 · LLM-as-a-Judge 的能力与偏差

- 原始论文：<https://arxiv.org/abs/2306.05685>。
- 本书用途：说明模型评审器可用于规模化候选比较，但会受到位置、冗长、自我偏好和参考答案质量影响；对应本书“机器 grader + 人工抽检 + 硬门 + 反例”的组合。
- 边界：LLM judge 不能独立认证授权、安全、真实外部效果或法律合规。
- 等级：`PRIMARY-RESEARCH`。

## 6. 公开基准

### S40 · SWE-bench

- 论文：<https://arxiv.org/abs/2310.06770>；官方仓库：<https://github.com/SWE-bench/SWE-bench>。
- 测量：在真实代码仓库和 issue 上生成可通过测试的补丁。
- 不测量：组织授权、用户交付可见性、生产部署、长期记忆、跨 Agent 责任和真实业务价值。
- 等级：`PRIMARY-RESEARCH` + 官方实现。

### S41 · tau-bench / tau2-bench

- 论文：<https://arxiv.org/abs/2406.12045>；当前官方仓库：<https://github.com/sierra-research/tau2-bench>；原仓库已标记为旧版：<https://github.com/sierra-research/tau-bench>。
- 测量：有策略约束、用户交互和工具调用的对话式 Agent 行为一致性。
- 不测量：任意真实企业流程、长期组织治理、完整安全纵深或跨法域合规。
- 等级：`PRIMARY-RESEARCH` + 官方实现；复现必须固定仓库、版本、任务集和评分器。

### S42 · WebArena

- 论文：<https://proceedings.iclr.cc/paper_files/paper/2024/hash/4410c0711e9154a7a2d26f9b3816d1ef-Abstract-Conference.html>；项目：<https://webarena.dev/>；仓库：<https://github.com/lhyscau/webarena>。
- 测量：在可复现网页环境中执行长程、功能性任务。
- 不测量：开放互联网全部变化、生产凭证、真实组织审批、业务补偿与长期可靠性。
- 等级：`PRIMARY-RESEARCH` + 官方实现。

### S43 · GAIA

- 论文：<https://arxiv.org/abs/2311.12983>；数据集：<https://huggingface.co/datasets/gaia-benchmark/GAIA>。
- 测量：需要推理、工具、网页与多模态信息整合的通用助手问题。
- 不测量：特定岗位长期胜任、权限治理、生产终态、团队交接和行业合规。
- 等级：`PRIMARY-RESEARCH` + 官方数据集。

## 7. 中国境内法律与监管入口

### S50 · 个人信息保护法与数据安全法

- 《中华人民共和国个人信息保护法》：<https://www.cac.gov.cn/2021-08/20/c_1631050028355286.htm>。
- 《中华人民共和国数据安全法》官方文本 PDF：<https://wb.flk.npc.gov.cn/flfg/PDF/8a19eb7aaa1e463cb21ff7cc2bac99d1.pdf>。
- 本书用途：建立个人信息处理、敏感个人信息、委托处理、跨境、主体权利，以及数据分类分级、风险监测、事件处置等合规触发器。
- 边界：具体法律角色、合法性基础、适用例外、重要数据与跨境路径必须由专业人员结合场景判断。
- 等级：`PRIMARY-LAW`。

### S51 · 生成式 AI、算法备案与生成内容标识

- 《生成式人工智能服务管理暂行办法》：<https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm>。
- 《互联网信息服务算法推荐管理规定》：<https://www.cac.gov.cn/2022-01/04/c_1642894606364259.htm>。
- 算法备案系统通知：<https://www.cac.gov.cn/2022-02/25/c_1647395666889023.htm>；备案系统：<https://beian.cac.gov.cn/>。
- 生成式 AI 服务备案公告：<https://www.cac.gov.cn/2024-04/02/c_1713729983803145.htm>。
- 《人工智能生成合成内容标识办法》：<https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm>。
- 本书用途：判断是否“向境内公众提供生成式 AI 服务”、是否具有舆论属性或社会动员能力、是否触发安全评估/算法备案/模型备案与显式隐式标识等流程。
- 边界：内部研发、不向境内公众提供服务的活动与面向公众服务适用边界不同；备案、登记、安全评估与标识不是同一程序，不能用一个编号相互替代。
- 等级：`PRIMARY-REGULATION`。

## 8. 本书原创方法论

以下术语属于本书方法论，不声明为外部行业标准：

- 训虾 / 硅基生命训练学
- 双三角模型
- 教练虾 / 导师 Agent 的具体训练职责
- 三证验真（TEV）
- 三省评审制
- 信誉分 / 功绩账本
- 让位协议
- 漂移治理三件套
- 主动性边界三档
- 从响应型到提案型的毕业路径

这些方法可与行业标准对位，但是否优于其他方法，必须通过公开测试集、真实任务表现、成本与安全数据验证。

## 9. 复核节律

| 对象 | 复核频率 | 触发条件 |
|---|---|---|
| OpenClaw stable / npm latest | 每月或发版时 | stable 版本变化 |
| OpenClaw Security / memory / skills | 每季度 | 信任模型或命令变化 |
| MCP / A2A / Agent Skills / OpenTelemetry GenAI | 每季度 | 新版规范、扩展或语义约定发布 |
| Muse 等托管产品 | 每次正式出版与重大更新 | 架构、条款、地区、连接器或安全承诺变化 |
| 课程来源 | 出版前一次 | 获得作者逐字稿或课程材料 |
| 本书原创优势主张 | 每次公开发布 | 新增可复现实验数据 |

任何过期来源不直接删除：在本文件标记 superseded，并把新来源追加到对应编号之后。

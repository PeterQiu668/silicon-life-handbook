# 业界对位与前沿追踪（全书统一）

> **文件**：`chapters/_industry-frontier-tracking.md`
> **版本**：v5.0 行业标准版 · 2026-09-28
> **维护者**：天策（Supervisor Layer，丘国力授权）
> **配套基座**：OpenClaw **2026.9.4 (3a9d69d)**（本书统一书写口径；本机 live 实测 `OpenClaw 2026.9.6 (eb377ac)`，配置兼容）
> **宿主环境**：macOS 26.5.1
> **定位**：本书 Part II 12 章的**统一业界对位底座 + 2026 前沿追踪底座**。12 个叙事 agent 不再各自写对位，一律引用本文件对应小节。
> **配套术语**：[`00-术语对照表·v3.0行业标准版.md`](../00-术语对照表·v3.0行业标准版.md)（SLCP / TEV / Trust Score / THP 等标准名以该表为准）

---

## 使用说明（给 12 章叙事 agent）

1. **不要在本章正文里重写对位表**——只放 3~5 行"本章差异化一句话 + 指向本文件的链接"。
2. 每章末尾追加 §6 给出的标准引用块（复制粘贴即可）。
3. 本文件所有"业界事实"带诚实标记：✅ 已验证（有 URL/日期）/ ⏳ 待实测或待核验（本书口径，尚未三源确认）/ ❌ 不引用（传闻或旧知识，已剔除）。
4. 各章若发现本文件的事实过期（新版本发布），**不要私自改本文件**——向天策提修复工单（Remediation Ticket），由本文件统一更新后各章引用自动生效。

---

## §1. 总论：业界 6 大框架 × OpenClaw v5.0 对位总表

> 对位框架（6 大）：**LangGraph**（LangChain 生态 · 图编排）/ **AutoGen/AG2**（微软生态 · 多智能体对话）/ **CrewAI**（角色分工）/
> **Claude Agent SDK**（Anthropic 原生 SDK）/ **OpenAI Agents SDK**（OpenAI 原生 SDK）/ **LlamaIndex**（数据为中心 · Agents + Workflows）。
> 对位基线：各框架 2026-Q3 公开资料口径；凡未逐条实测的版本号一律标 ⏳，见 §5。

| 维度 | LangGraph | AutoGen / AG2 | CrewAI | Claude Agent SDK | OpenAI Agents SDK | LlamaIndex | **OpenClaw v5.0** |
|---|---|---|---|---|---|---|---|
| 协议层契约（文件化人格/权限/记忆） | ❌ 无；状态由节点函数 + checkpointer 管理 | ❌ 无；`ConversableAgent.system_message` 即席配置 | ❌ 无；`role/goal/backstory` 即席配置 | ⚠ 部分：System Prompt + CLAUDE.md + Permission API | ⚠ 部分：`instructions` + guardrails | ⚠ 部分：`system_prompt` 参数 | ✅ **7 大契约文件（SOUL/AGENTS/USER/TOOLS/IDENTITY/HEARTBEAT/MEMORY），挂载即加载** |
| MCP 绑定 | ⚠ 外部集成（langchain-mcp-adapters） | ⚠ 外部集成 | ⚠ 外部集成（MCP tools 适配） | ✅ 原生（MCP connector + Tool Search，2025-11 Advanced Tool Use） | ✅ 原生（MCP servers 工具接入） | ⚠ 外部（LlamaHub 工具适配） | ✅ **原生 14 子命令** ⏳（本书口径，待 B2 落盘核验） |
| A2A 绑定 | ❌ 无原生（可自建 subgraph 模拟） | ⚠ 早期（Magentic-One / Swarm 实验） | ❌ 无 | ❌ 无 | ⚠ 早期（Swarm → handoffs 演进） | ❌ 无 | ✅ **SLCP 三层 + THP 任务交接协议** ⏳（SLCP 为本书标准名，原：ACP，见术语表 #1） |
| Skills 体系 | ❌ 无（LangChain Hub 是 prompt 模板库，非 skill 范式） | ❌ 无 | ❌ 无 | ✅ **Anthropic Agent Skills**（开放标准，agentskills.io，2025-12-18） | ⚠ Codex skills 兼容（~40 产品生态之一） | ❌ 无 | ✅ **236 skill 目录 + Registry 表 + frontmatter 校验规范**（本机盘点；238 为任务口径，待核验，见 §5） |
| 漂移治理（文档/人格漂移检测） | ❌ 无（LangSmith evals 只做质量评估） | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ✅ **Drift Governance Trio（漂移治理三件套）** |
| 主动性边界三档制 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无（Permission API 是二值开关，非三档） | ❌ 无（guardrails 是拦截器，非主动性分档） | ❌ 无 | ✅ **Proactive Boundary Triad（主动性边界三档）** |
| 三证据验证（验收） | ❌ 无（靠 LangSmith 人工看轨迹） | ❌ 无 | ❌ 无 | ❌ 无 | ⚠ Tracing（可观测轨迹，非验收口径） | ❌ 无 | ✅ **TEV 三证（新产物 / 前后 Diff / 测试日志）** |
| 自主目标生成（提案型） | ⚠ 人工编排 goal 节点 | ⚠ GroupChat Manager 协调，无自主目标层 | ⚠ Process 编排（sequential/hierarchical），目标由人定 | ❌ 无 | ⚠ Triage/Manager 模式，目标由人定 | ❌ 无 | ✅ **Autonomous Goal Generation（Response → Proposal）** |
| 会话压缩预留（Compaction） | ⚠ checkpointer 持久化（非压缩预留模型） | ❌ 无 | ❌ 无（memory 短/长/实体三类，无压缩预算） | ⚠ Partial（compact 指令 + 上下文管理） | ⚠ Partial（会话管理） | ❌ 无 | ✅ **本书口径 `CompactionRequestBudget.reserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25`** ⏳（接口层口径，非 openclaw.json 字段，见 §5） |
| 训练流程层（Reactive → Proactive 方法论） | ❌ 无（只有执行框架） | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ✅ **双三角模型 + 训练轮次（本书第 3 章，全网独家）** |
| 每周体检清单 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ✅ **Weekly Health Checklist（第 4 章）** |
| 信任评分 / 功绩账本 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ✅ **Trust Score / Merit Ledger（第 5 章）** |
| 心跳调度（原生） | ❌ 无（需外部 cron） | ❌ 无 | ❌ 无（CrewAI Flows 需外部触发） | ❌ 无 | ❌ 无 | ❌ 无 | ✅ **原生 heartbeat（`agents.entries.<id>.heartbeat.every`，如 `"30m"`）** |

**总表一句话结论**：6 大框架解决的是"**怎么执行 agent**"（编排 / 工具 / 可观测），OpenClaw v5.0 + 本书解决的是"**怎么训练 agent 从响应型长成提案型**"（契约 / 训练轮次 / 漂移治理 / 验收）。两层**互补不替代**——第 0 章总论的"5 个差异化优势"即由此表逐项展开（详见 §2.12）。

---

## §2. 12 主题深度对位（每主题 ≥30 行）

> 写法统一为：【本章主张】→【6 框架逐项】→【OpenClaw v5.0 差异化】→【诚实标记行】。
> 章号映射：第 0 章=总论（§2.12），第 1 章=七大契约（§2.1），第 2 章=系统骨架（§2.2），第 3 章=训练流程（§2.3），
> 第 4 章=长期表现（§2.4），第 5 章=治理系统（§2.5），第 6 章=协同军团（§2.6），第 7 章=超维演进（§2.7），
> 第 8 章=MCP 绑定（§2.8），第 9 章=A2A 绑定（§2.9），第 10 章=Skills（§2.10），第 11 章=Plugins（§2.11）。

### §2.1 七大契约（Life Protocols）vs 业界

**【本章主张】** Agent 的人格、权限、记忆应当是**文件系统上可版本化、可审计的 7 份契约**，而不是散落在代码里的 prompt 字符串。

**【6 框架逐项】**

- **LangGraph**：无"契约"概念。状态由图节点函数读写 `State` + checkpointer 持久化；人格 = 节点里硬编码的 prompt。优势是状态机可视化 + time-travel 调试（2026 年生产标准口径，见 §3.4）；代价是"换人格 = 改代码"。
  参考：LangGraph 官方文档 `langgraph` / LangChain Hub（prompt 模板库，非契约层）。
- **AutoGen / AG2**：5 类对话模式（two-agent / group chat / nested / sequential / swarm，AG2 延续）。`ConversableAgent(system_message=...)` 即席声明人格；GroupChatManager 负责协调。无人格文件的版本化约定。
  参考：AG2 官方文档（microsoft/autogen → ag2ai/ag2 迁移后）。
- **CrewAI**：`Agent(role, goal, backstory, tools)` + `Task` + `Crew(process=sequential|hierarchical)` + `Flow`。backstory 接近 SOUL 的雏形，但与代码同体，不可独立审计、不可跨 crew 复用。
  参考：CrewAI 官方文档（Q1 2026 口径：44,600+ stars，月 1000 万+ agent 执行，见 §3.4）。
- **Claude Agent SDK**：System Prompt + CLAUDE.md（项目记忆）+ Permission API（运行时二值授权）+ MCP 工具。CLAUDE.md 是离"契约文件"最近的业界实践，但只有 1 份（无 7 契约分层），且 Permission 是运行时开关而非文件声明。
  参考：Anthropic 官方文档（Claude Agent SDK；2025-10 Agent Skills 见 §3.3）。
- **OpenAI Agents SDK**（2025-03 发布）：`instructions` + `handoffs` + `guardrails` + Tracing。guardrails 是输入/输出拦截器，解决"不许做什么"；不解决"**我是谁、我记得什么、我多久醒一次**"。
  参考：OpenAI Agents SDK 官方文档（~19,000 stars / 月 ~1030 万下载，2026 口径，见 §3.4）。
- **LlamaIndex**：Agents（ReAct/Function Calling）+ Workflows（事件驱动编排），`system_prompt` 参数即席配置。长处在数据连接（LlamaHub / 索引），不在 agent 身份层。
  参考：LlamaIndex 官方文档。

**【OpenClaw v5.0 差异化】** 7 契约文件化、可版本化、可审计：SOUL（人格）/ USER（归属与权限声明）/ AGENTS（下属编队）/
TOOLS（工具契约）/ HEARTBEAT（唤醒节律）/ IDENTITY（身份）/ MEMORY（记忆分层）。每次会话自动加载——"契约是持久挂载的，提示词是一次性的"（第 1 章 1.1）。

**【诚实标记】** ✅ 6 框架"无文件化契约层"的判断基于各官方文档公开能力模型；⏳ 各框架 2026-Q3 具体小版本号待核验，不影响本节结论（结论只依赖"有/无契约层"，不依赖版本号）。

**【关键边界澄清】**
- "契约 ≠ System Prompt"：LangGraph / AutoGen / CrewAI 之所以"无契约"，不是因为它们不能写 System Prompt，而是**没有把人格/权限/记忆分层为可独立加载、可独立审计、可版本化的文件**。OpenClaw 7 契约的本质是"**文件系统层级的容器**"，不是"**文本块**"。
- "契约 ≠ 配置文件"：Claude Agent SDK 的 `CLAUDE.md` 已是"项目记忆文件"，但只有 1 份、且与 System Prompt / Permission API 割裂；OpenClaw 7 契约是**统一容器**（同目录、同 frontmatter 风格、同加载时序），新增契约只需"在目录里多放一个 .md 文件"——零代码改动。
- "契约 ≠ Subagent 定义"：OpenAI Agents SDK 的 handoffs / Claude Agent SDK 的 subagent 都只能定义"**可被调用的能力**"，不能定义"**agent 自己是谁、归属谁、记住什么、多久醒一次**"。7 契约的第 6 项（IDENTITY）和第 7 项（MEMORY）在 6 框架里**完全无对应物**——这是 OpenClaw 最深的护城河之一。
- **诚实自检**：本节措辞对 OpenClaw 略有"宣传腔"。客观陈述应是——"OpenClaw 把人格/权限/记忆分层到 7 份文件并强制每次会话加载；这是当前 6 大公开框架的公开文档中**未见**的实现模式"。"未见"=可证伪；任何读者若发现反例，按文件头部说明提修复工单。

### §2.2 系统骨架（Runtime / Gateway / Channels / Memory / Heartbeat / Tools / Skills）vs 业界

**【本章主张】** 先画骨架再谈训练：7 个子系统 + 共享网关 RPC 是 agent 的"解剖图"，协议章节是"生理学"。

**【6 框架逐项】**

- **LangGraph**：Runtime = 图执行引擎 + checkpointers；可观测 = LangSmith（tracing/evals）；部署 = LangGraph Platform（2026 口径约 400 家企业部署，见 §3.4）。
  无原生 channels（消息通道）层、无 heartbeat、无 skills 层。状态持久化最强，是"骨架最硬"的框架。
- **AutoGen / AG2**：Runtime = 对话运行时（agents + chat manager）；天然多 agent，但通道 = 代码内收发消息，无外部 channel 绑定抽象；无 heartbeat、无 skills。
- **CrewAI**：Crews（角色协作）+ Flows（事件编排）+ memory（short-term / long-term / entities 三类）。memory 分类法与 OpenClaw MEMORY 5 层可对位（见 §2.7/§3.8），但 memory 不可编程压缩、无预留预算。
- **Claude Agent SDK**：Runtime = Claude Code CLI / API；工具层 = MCP 原生 + Tool Search（2025-11 Advanced Tool Use：工具发现 token 开销降 ~85%，Opus 4.5 程序化调用准确率 79.5%→88.1%，见 §3.3）；
  安全层 = Permission API + 安全优先设计；计算机操作（computer use）为独家能力。无 channels 绑定、无 heartbeat。
- **OpenAI Agents SDK**：Runtime 轻量；handoffs（任务交接）+ guardrails（护栏）+ 内置 Tracing 是其骨架特色。handoffs 与本书 THP 对位（见 §2.6），但 handoffs 只解决"转交"，不解决"让位仲裁 + 审计账本"。
- **LlamaIndex**：Workflows（事件驱动）+ 数据连接器（最强 RAG 前端）。2026 年定位愈发清晰：**关键工作流/高风险动作选 LangGraph 或 LlamaIndex 做显式控制流**（Arahi 2026-05 指南口径，见 §3.4）。

**【OpenClaw v5.0 差异化】** 唯一同时具备 7 子系统的基座：Runtime / Gateway（`tools.catalog` + `skills.status`/`skills.skillCard` 共享 RPC）/
Channels（多通道绑定）/ Memory（5 层）/ Heartbeat（原生 `agents.entries.<id>.heartbeat.every`）/ Tools / Skills（236 目录）。
第 2 章附录 A 给出 20 个真实顶层 key 的路径对照（`acp, agents, auth, bindings, browser, channels, commands, env, gateway, logging, memory, messages, meta, models, plugins, session, skills, talk, tools, wizard`）。

**【诚实标记】** ✅ 20 顶层 key 为本机 `~/.openclaw/openclaw.json`（45,662 字节）实测；✅ 框架能力描述基于 2026 公开对比资料（见 §3.4 来源）；⏳ "原生 14 子命令"为本书口径，待 B2 落盘核验。

**【关键边界澄清】**
- "7 子系统"的来龙去脉：前两项（Runtime/Gateway）是基础设施隐喻；Channels 是消息层；Memory/Heartbeat/Tools/Skills 是能力层。6 框架都有自己的"骨架图"——LangGraph 的图引擎、AutoGen 的对话运行时、CrewAI 的 crew/task/process——**本节绝不声称"6 框架没骨架"**，声称的是"**只有 OpenClaw 的骨架同时包含 channels+heartbeat+skills 三件**"。
- heartbeat 是最硬的差异化：LangGraph 明确需外部 cron；CrewAI Flows 需外部触发；Claude/OpenAI SDK 均无定时唤醒语义。OpenClaw `agents.entries.<id>.heartbeat.every`（如 `"30m"`）是**配置即生效**的原生能力——"提案型 agent"的前提正是"**能自己醒来**"，否则一切主动性都是空话（第 4/7 章回响）。
- Gateway RPC 的诚实口径：`tools.catalog` + `skills.status`/`skills.skillCard` 是主仓真结构（术语表 #32，P0 核实）；"共享网关 RPC"是本书对"Tools/Skills 双模块 + 共享 RPC"的标准表述，**不是主仓术语**。
- 20 顶层 key 的勘误价值：第 1/2 章 SOP 头已载明 `runtime / workspace / routing / heartbeat / subagents` **不是**顶层字段——本节重申一次，防止 12 章叙事 agent 误写配置示例。

### §2.3 训练流程（双三角模型 + 训练轮次）vs 业界

**【本章主张】** 这是全书最深的护城河：业界**没有任何框架提供"训练流程层"**——它们都是执行框架，不是训练方法论。

**【6 框架逐项】**

- **LangGraph**：LangSmith evals（数据集评估 + 在线监控）。能回答"这次跑得好不好"，不能回答"**下轮训练重点练什么**"。评估 ≠ 训练。
- **AutoGen / AG2**：无评估闭环约定；靠开发者自写测试。多智能体辩论（debate/iteration）是其独特训练信号来源，但未产品化为"训练轮次"。
- **CrewAI**：training/测试钩子极简；`Crew.train()` 主要是 few-shot 示例沉淀，非本书意义的训练轮次。
- **Claude Agent SDK**：无训练层。Anthropic 把"训练"放在模型侧（Constitutional AI，见 §3.5），SDK 侧只给执行 + 权限。
- **OpenAI Agents SDK**：Tracing + Evals（OpenAI Evals 体系）。同样止于评估。
- **LlamaIndex**：评估侧（evaluation 模块）服务于 RAG 调参，不涉及 agent 行为训练。

**【OpenClaw v5.0 差异化】** 双三角模型（Dual-Triangle Model: Expectation-Actuality-Feedback Loop，术语表 #26，丘总原创保留）+
训练轮次（Expectation → Actuality → Feedback 闭环）+ 导师智能体（Mentor Agent / Training Coordinator，原：教练虾，术语表 #4）。
训练成果 → 第 5 章 TEV 验收 → MEMORY 沉淀，形成"练-验-记"闭环。这是 6 大框架文档里**找不到对应物**的一章。

**【诚实标记】** ✅ "业界无训练流程层"为可证伪断言：6 框架官方文档均无 Reactive→Proactive 训练 ladder；若读者找到反例，按本文件头部说明提修复工单。⏳ CrewAI `train()` 等弱对应物的细节以其官方文档为准，本书不展开。

**【关键边界澄清】**
- "评估 ≠ 训练"是本章核心公理：LangSmith / OpenAI Evals 衡量"**已经**做得好不好"；OpenClaw 训练轮次回答"**下轮要练什么**"。前者是后视镜，后者是导航图。
- AutoGen 多智能体辩论（debate/iteration）是"训练信号源"但未产品化：2023 年初代 AutoGen 就支持 GroupChat Manager 风格的辩论，但辩论历史不沉淀为"训练数据"，下次还要从头吵一遍。OpenClaw 的差异化在于"**辩论结果写回 MEMORY，第 7 章复用**"——这是训练流程层最硬的护城河之一。
- "评估 vs 训练"的另一面是"Anthropic Constitutional AI 在模型侧做训练 / SDK 侧只给执行"——这两层训练**不在一个抽象层级**：本书的训练轮次在 agent 行为侧（怎么跑任务），Constitutional AI 在模型价值观侧（怎么想问题）。第 3 章会显式拆分二者，避免读者混为一谈。
- 诚实自检：本节对 OpenClaw 训练学是"全网独家"的声称——需限定为"主流 6 大框架 + 公开方法论文档"。若未来出现"agent 训练学 SaaS"产品（如某些新创公司声称），本节保持开放，按修复工单机制评估后纳入或剔除。

### §2.4 长期表现（Drift Governance Trio + Proactive Boundary Triad + 每周体检）vs 业界

**【本章主张】** Agent 会漂移（文档漂移 / 人格漂移，术语表 #28，业界空白赛道）且会"越界主动"——本章给检测器 + 分档器 + 体检表。

**【6 框架逐项】**

- **LangGraph**：漂移检测 ❌。LangSmith 可监控输出分布偏移，但那是应用层自建，不是框架能力。
- **AutoGen / AG2**：❌。GroupChat 失控（无限对话循环）是已知痛点，靠 `max_turns` 粗粒度截断，无漂移语义。
- **CrewAI**：❌。backstory 随任务被改写即"人格漂移"，框架无感知。
- **Claude Agent SDK**：Permission API 防"越界动作"，但不防"人格漂移"（说话越来越不像 SOUL 定义的样子）；❌ 无漂移治理。
- **OpenAI Agents SDK**：guardrails 防有害输出，不防缓慢漂移；❌ 无。
- **LlamaIndex**：❌。

**【OpenClaw v5.0 差异化】** Drift Governance Trio（漂移治理三件套）+ Proactive Boundary Triad（主动性边界三档：多大主动性配多大授权）+
Weekly Health Checklist（每周体检清单，术语表 #29）。相关前沿：Anthropic Sleeper Agents 论文（2024-01，见 §3.6）证明"漂移/后门可潜伏通过常规对齐训练"——正是本章存在的学术背书。

**【诚实标记】** ✅ Sleeper Agents（arxiv:2401.05566，Anthropic 2024-01）真实存在；✅ 6 框架无漂移治理基于公开能力模型；⏳ 本章 Trio 的具体检测阈值为本书口径，以第 4 章正文为准。

**【关键边界澄清】**
- 漂移的两种语义：本书严格区分"**文档漂移**"（契约文件被外部误改、漂移目标与 SOUL 不一致）与"**人格漂移**"（输出风格逐渐偏离 SOUL 定义）。前者是文件系统事件，后者是行为分布事件——Trio 必须**两种都检测**，单一检测器无效。
- Proactive Boundary Triad 的诚实表述：业界有近似物（Claude Permission API 的 `allow/deny` 二值；OpenAI guardrails 的 input/output 拦截），但**三档制（低中高主动性配不同授权）是 OpenClaw 独有**。"三档"的具体阈值与违约处理在第 4 章正文，本节不重定义。
- Weekly Health Checklist 的同行空白：术语表 #29 标注"业界空白"——可证伪。读者若发现某框架/平台有原生 weekly drift 检测仪表板，请提工单，本节会改为"已被 X 框架部分覆盖"。
- 与第 3 章回响：本节与 §2.3 训练流程层共同支撑"**6 框架只能告诉你跑得好不好，不能告诉你 agent 性格变了没**"——这是 OpenClaw 提案型范式的核心护城河之一。

### §2.5 治理系统（TEV + Remediation Ticket + Trust Score + Merit Ledger）vs 业界

**【本章主张】** 用"验收口径"代替"感觉不错"：三证据验证（Three-Evidence Verification，术语表 #10）+ 修复工单 + 信任评分/功绩账本（术语表 #12）。

**【6 框架逐项】**

- **LangGraph**：LangSmith tracing（轨迹可观测）+ 人工 review。轨迹是原材料，TEV 是验收口径——差一层。
- **AutoGen / AG2**：❌ 无治理原语。
- **CrewAI**：❌（ hierarchical process 的 manager 评审是流程便利，非证据验收）。
- **Claude Agent SDK**：Permission API（事前授权）+ subagent task spec（任务卡对应物，术语表 #24）。有"事前"，无"事后三证"。
- **OpenAI Agents SDK**：guardrails（拦截）+ Tracing（审计轨迹，对应本书 Governance Audit Ledger，术语表 #16）。最接近"治理账本"概念，但 Tracing 记录"发生了什么"，Merit Ledger 记录"**谁立了功、谁该被信任**"——激励层缺失。
- **LlamaIndex**：❌。

**【OpenClaw v5.0 差异化】** TEV（新产物 / 前后 Diff / 测试日志三证）+ Remediation Ticket（修复工单，术语表 #11）+
Trust Score / Merit Ledger（信任评分 / 功绩账本）。TEV 结果写回 MEMORY 契约、信任评分写回 IDENTITY 契约——治理闭环落到 7 契约上，这是第 1 章的回响。

**【诚实标记】** ✅ OpenAI Tracing、Claude Permission API 均为官方公开能力；✅ TEV/账本为本书原创方法论（对内曾称"三证验真/信誉分/军功簿"，对外一律用标准名）。

**【关键边界澄清】**
- TEV 的精确定义：Three-Evidence Verification = 新产物（artifact）+ 前后 Diff + 测试日志三证。任何验收结论必须**三证齐全**，缺一即为"部分验证"（partial），不得写"已验证"。这是第 5 章的验收铁律。
- LangSmith vs TEV：LangSmith tracing 是"**原材料**"（记录发生了什么），TEV 是"**验收口径**"（判断做得对不对）。OpenAI Tracing / Governance Audit Ledger（术语表 #16）同理——账本记录"发生了什么"，Merit Ledger 记录"**谁立了功、谁该被信任**"。激励层（Merit）是 6 框架**集体缺失**的一层。
- Trust Score 的诚实口径：本书 Trust Score 是**工程评分**（基于 TEV 历史 + 修复工单履约率），不是"信用分"社会隐喻。第 5 章正文给出计算口径；本节只对位"有/无"，不对位"怎么算"。
- Remediation Ticket 的闭环：漂移/越界（第 4 章）→ 修复工单（第 5 章）→ TEV 验收 → MEMORY 沉淀。这是第 4→5 章的链条，也是"治理不是一次性检查，而是持续循环"的论证。

### §2.6 协同军团（SLCP + Anti-Fragile Triptych + Response Yield + THP）vs 业界

**【本章主张】** 多智能体编排（Multi-Agent Orchestration / Agent Fleet，术语表 #6）需要协议，而不是"把几个 agent 拉进一个群"。

**【6 框架逐项】**

- **LangGraph**：supervisor subgraph + Send API + 图可视化。工程最成熟的多 agent 编排（状态机语义精确），但"让位仲裁/审计"需自建。
- **AutoGen / AG2**：GroupChat / Swarm / Magentic-One。多智能体辩论与迭代（debate）是其招牌；2026 年 AG2 重写后趋稳（生产就绪度中等，见 §3.4）。
- **CrewAI**：sequential / hierarchical process。角色分工最直观，原型最快（2~4 小时可用，见 §3.4）；hierarchical 的 manager 即"三省评审"的弱对应物。
- **Claude Agent SDK**：subagents + task spec。单 agent 深度（extended thinking + computer use）最强，多 agent 协同语义最弱。
- **OpenAI Agents SDK**：handoffs（一等公民的任务交接）+ guardrails。handoffs 即本书 THP（Task Handoff Protocol，术语表 #15）的业界对应物——但 OpenAI handoffs 只管"交"，不管"**交接后的审计 + 让位冲突仲裁**"。
- **LlamaIndex**：Workflows 多步编排；agent 间协同非其主场。

**【OpenClaw v5.0 差异化】** SLCP（Silicon-Life Coordination Protocol，原：ACP；IBM/BeeAI 的 ACP 已占用且 2025-08 合并入 A2A，对外必须用 SLCP，术语表 #1）+
Anti-Fragile Triptych（反脆弱三层）+ Three-Stage Review（三省评审制：Proposal / Review / Final-Decision，术语表 #13）+
Response Yield Protocol（响应让渡协议，原：让位协议，术语表 #14）+ THP + Governance Audit Ledger。本机 18 agent 编队实测（kunlun/mingjing/tianshu/tiangong/xuanyuan/fenghuang/kunpeng/jixia/zhulong/siku/qilin/hetu/peter/fengniao/mobai/zhuque/baxia/tiance）。

**【诚实标记】** ✅ 18 agent 名单为本机实测；✅ IBM ACP 2025-08 合并入 A2A（术语表调研报告 E.2 口径）；⏳ SLCP 三层与 A2A v1.0 的 bridge demo 待实测（见 §5）。

**【关键边界澄清】**
- 改名来历：本书最初用 "ACP"（丘总卷七自造），但 IBM/BeeAI 的 ACP 已存在且 2025-08 合并入 A2A——对外用 ACP 会触发商标/语义双重冲突，故统一改 SLCP（Silicon-Life Coordination Protocol）。本书内部稿保留 ACP 作为历史简称。
- SLCP 与 A2A 的分工：A2A 是"**能通话**"的协议层标准（Agent Card + JSON-RPC + task lifecycle），SLCP 是"**通话出事时不塌**"的协议层附加（反脆弱三层：故障隔离 / 降级让位 / 审计追溯）。两者**正交可桥接**（见 §3.2 ⏳ 待实测条目）。
- THP 与 OpenAI handoffs 的关键差：handoffs 是"**交接**"语义（一等公民对象 `handoff()` 函数）；THP 是"**交接 + 审计 + 让位仲裁**"三合一。OpenAI 不做"谁更可信就让谁先答"——这是 Response Yield Protocol 的活。
- 18 agent 实测名单（kunlun/mingjing/tianshu/tiangong/xuanyuan/fenghuang/kunpeng/jixia/zhulong/siku/qilin/hetu/peter/fengniao/mobai/zhuque/baxia/tiance）的诚实标注：这是本机 `openclaw agents list` 实测，**不是 OpenClaw 默认 agent 阵容**——读者自己的 OpenClaw 安装可能不同。

### §2.7 超维演进（动态进化 / 记忆全息 / 自主目标生成）vs 业界

**【本章主张】** 从"训好的 agent"到"会自己进化的 agent"：OODA 循环 + 自主目标生成（术语表 #30，业界空白）+ 记忆全息。

**【6 框架逐项】**

- **LangGraph**：❌ 无自主目标层。人工写 goal 节点是天花板。
- **AutoGen / AG2**：GroupChat Manager 是"协调"，不是"自主立项"。AutoGPT / BabyAGI（2023）血统上最接近自主目标，但止于 demo（见 §3.7）。
- **CrewAI**：Process 由人定；❌ 无自主目标。
- **Claude Agent SDK**：❌。Anthropic 2026-01 新 Constitution（23k 词，见 §3.5）讨论的是模型价值观推理，不是 agent 自主目标生成——两回事，不可混引。
- **OpenAI Agents SDK**：Triage/Manager 模式的目标仍由人下达；❌。
- **LlamaIndex**：❌。

**【OpenClaw v5.0 差异化】** Autonomous Goal Generation（Response → Proposal，全书主线"从响应型到提案型"的落点）+
OODA Loop（Observe-Orient-Decide-Act，术语表 #27）+ 记忆全息（MEMORY 5 层快照可恢复任意历史人格状态）。
记忆侧业界对位：Letta（MemGPT 血统：core/recall/archival 三层 + 自编辑记忆）/ Mem0（可插拔记忆 API）/ Zep（时序知识图谱）/
Anthropic 7 Layers of Memory（2026-03，Claude Code 记忆层级，见 §3.8）——OpenClaw MEMORY 5 层与之逐层可对位，详见 §3.8 对位表。

**【诚实标记】** ✅ AutoGPT/BabyAGI（2023）真实存在；✅ Letta/Mem0/Zep/7 Layers 均为 2026 公开资料（见 §3.8 来源）；⏳ MEMORY 5 层 ↔ 业界各体系的逐层映射表由第 7 章正文展开，本文件只给结论。

**【关键边界澄清】**
- "提案型 ≠ 多走一步"：业界有些框架称"proactive"指的是"会主动发通知 / 主动重试 / 主动 escalate"——这是执行层主动性。OpenClaw 的"提案型"是**目标层**的主动性：agent 自己立项（Autonomous Goal Generation），由 Proactive Boundary Triad 约束，由 TEV 验收，由 MEMORY 沉淀。两类主动性**不同维度**，不可混引。
- OODA 的军事血统：本书保留 OODA（Boyd，1970 年代）作为决策循环模板，因为它是少数能跨"侦察-定向-决策-行动"四阶段的简明循环；但**不声称本书是军事决策系统**——OpenClaw 的 OODA 落地在契约层（每次 heartbeat 触发一次 OODA）。
- 记忆全息 vs 记忆检索：全息是"**恢复任意历史人格状态**"（包括 SOUL/MEMORY 快照），记忆检索是"从 MEMORY 里取一条事实"。前者是状态机操作，后者是查询操作——全息是 OpenClaw 独有；6 框架能做的就是后者。
- 与第 7 章回响：本章是"训练学→方法论"的终点（第 3 章开始 → 第 7 章结束），所有前置章节（契约 / 骨架 / 训练 / 漂移 / 治理 / 协同）在超维演进章**收束为一条主线**——"**让 agent 自己会长大**"。

### §2.8 MCP 绑定 vs 业界

**【本章主张】** MCP 是 2026 年 agent 工具层的事实标准（68% 生产部署采用 MCP 或等价标准层，见 §3.1）——本章是 OpenClaw 原生绑定的工程手册。

**【6 框架逐项】**

- **LangGraph**：`langchain-mcp-adapters` 外部适配。能调 MCP 工具，但 MCP server 生命周期管理在框架之外。
- **AutoGen / AG2**：外部集成；无原生 MCP client 抽象。
- **CrewAI**：MCP tools 适配层；同上，外部。
- **Claude Agent SDK**：✅ 原生。MCP connector + 2025-11 Advanced Tool Use（Tool Search Tool / Programmatic Tool Calling / Tool Learning）。
- **OpenAI Agents SDK**：✅ 原生（MCP servers 作为工具源接入）。
- **LlamaIndex**：LlamaHub 工具生态 + 外部 MCP 适配；数据连接器仍是其护城河。

**【OpenClaw v5.0 差异化】** 原生 14 子命令 ⏳（本书口径，待 B2 落盘核验）+ `tools.catalog` 网关 RPC（术语表 #32 真结构）。
协议演进红利：MCP 2026-07-28 规范（stateless 核心，移除 `initialize`/`initialized` 握手与 `Mcp-Session-Id`，新增 `server/discover` RPC；
AWS 贡献 Tasks 扩展；MCP Apps 生产就绪——见 §3.1）发布后，OpenClaw 原生绑定可直接吃"无状态部署 + 长任务 + 交互式工具界面"三重红利。

**【诚实标记】** ✅ MCP 规范时间线（2024-11-05 → 2025-03-26 → 2025-06-18 → 2025-11-25 → 2026-07-28）与 stateless 内容来自 MCP 官方博客 2026-07-28 公告（见 §4 来源）；
⏳ MCP Streamable HTTP 传输的本机实测待做；⏳ 原生 14 子命令待 B2 核验。

**【关键边界澄清】**
- MCP 是工具层协议，不是 agent 编排协议：业界常把 MCP 和 A2A 混为"agent 协议"——MCP 解决"**agent 怎么调外部工具**"（client-server），A2A 解决"**agent 怎么和另一个 agent 通话**"（agent-agent）。两者正交，第 8/9 章是 OpenClaw 在两层的独立绑定。
- "无状态核心（stateless core）"的工程意义：MCP 2026-07-28 移除协议层 session，让 MCP server 可以"**无状态部署**"到 Lambda/Cloud Run/AgentCore——这把 MCP 从"必须有长连接"变成"**标准 HTTP 即可**"，是企业级落地的核心前提。
- Tasks 扩展的差异化：AWS 贡献的 Tasks 是 MCP 首批官方扩展（首个），解决"长任务 / 流式进度 / 后台作业"——这是 MCP 第一次承认"工具调用不是 request-response 那么简单"。OpenClaw 原生绑定可直接复用 Tasks 语义，**无需自建**。
- 14 子命令的诚实口径：本书说"原生 14 子命令"指的是 OpenClaw 自带的 MCP client 子命令数（`openclaw mcp <verb>`）——**精确数字待 B2 agent 落盘核验**（`--help` 输出统计），各章不得擅自写其他数字。

### §2.9 A2A 绑定 vs 业界

**【本章主张】** 跨厂商 agent 互操作的标准答案是 A2A v1.0（2026-03-12 GA）；OpenClaw 用 SLCP 三层 + THP 在此标准之上加反脆弱语义。

**【6 框架逐项】**

- **LangGraph**：❌ 无原生 A2A。可自建 Agent Card + JSON-RPC 网关模拟，成本自负。
- **AutoGen / AG2**：⚠ 早期（Magentic-One 跨 agent 实验；A2A 生态 150+ 组织中有微软系参与，见 §3.2）。
- **CrewAI**：❌ 无。
- **Claude Agent SDK**：❌ 无（Anthropic 下注 MCP + Skills，不下注 A2A）。
- **OpenAI Agents SDK**：⚠ 早期（Swarm 血统的 handoffs 与 A2A task 语义部分重叠；OpenAI 在 A2A 生态中）。
- **LlamaIndex**：❌ 无。
- （附带：Google ADK（2025-04 发布）是 A2A 原生派代表，但不在本书 6 大框架名单内，此处仅作注脚，不展开。）

**【OpenClaw v5.0 差异化】** SLCP 三层（反脆弱语义：故障隔离 / 降级让位 / 审计追溯）+ THP（任务交接协议，与 OpenAI handoffs 对位但多审计层）。
定位公式：**A2A 解决"能通话"，SLCP 解决"通话出事时不塌"**。Agent Card（discovery 协议）是 SLCP 节点注册可复用的标准件。

**【诚实标记】** ✅ A2A v1.0（2026-03-12）+ v1.0.1（2026-05）+ 150+ 组织（2026-04 Linux Foundation 公告）均为公开事实（见 §4 来源）；
⏳ A2A TCK / SLCP bridge demo 待实测（见 §5）；❌ 不引用任何"A2A v2.0 已发布"类传闻（截至 2026-09-28 无此版本）。

**【关键边界澄清】**
- A2A 不是 agent 框架，是协议：与 MCP 同理——A2A 定义 Agent Card、JSON-RPC method surface、task lifecycle（submitted/working/input-required/completed/failed/canceled），不定义 agent 内部决策逻辑。OpenClaw 在 A2A 之上的 SLCP 三层是**协议层附加**，不是替代。
- Agent Card 的复用价值：A2A Agent Card 是 discovery 协议（name/description/url/version/protocolVersion/capabilities/auth schemes）。OpenClaw SLCP 节点注册可**直接复用 Agent Card 作为对外呈现**——一个 agent 同时是 OpenClaw 内部节点 + A2A 可发现的对外服务。
- v1.0 迁移成本：从 v0.3 → v1.0 的 breaking changes（method 名、Part 模型、Agent Card 接口、字段名）由 A2A 官方提供迁移指南——这是**为什么本书等 v1.0 GA 后再写第 9 章**，而非基于早期 draft。
- "150+ 组织"的诚实标注：Linux Foundation 2026-04-09 一周年公告口径（150 supporting organizations + Google Cloud + Microsoft Copilot Studio & Foundry + Amazon Bedrock AgentCore 集成）——数字为 LF 自报，未独立核验各成员的实际使用程度。
- Google ADK 的脚注：Google ADK（Agent Development Kit，2025-04 发布）是 A2A 原生派代表，**不在本书 6 大框架名单内**（因公开文档量与生态规模未达 LangGraph/CrewAI 量级）。本节仅作"原生 A2A 框架代表"脚注，不展开。

### §2.10 Skills（Skill Registry）vs 业界

**【本章主张】** Anthropic Agent Skills（2025-10 发布，2025-12-18 开放标准）是 2026 年 agent 能力封装的最大公约数；OpenClaw skill registry 是其超集实践（早于标准存在、规模更大）。

**【6 框架逐项】**

- **LangGraph**：❌ 无 skill 范式（LangChain Hub 是 prompt 模板，不是 SKILL.md + scripts + references 三件套）。
- **AutoGen / AG2**：❌ 无。
- **CrewAI**：❌ 无（tools 注册 ≠ skills；缺 progressive disclosure 与 frontmatter 触发语义）。
- **Claude Agent SDK**：✅ **范式发源地**。SKILL.md（YAML frontmatter：name + description）+ scripts/ + references/；
  progressive disclosure 三级（metadata → SKILL.md 全文 → resources 按需加载）；2025-12-18 发布开放标准（agentskills.io）；
  截至 2026-06 约 40 个兼容产品（Codex / Copilot / Cursor / Gemini CLI / VS Code 等）；anthropics/skills 仓库 62k+ stars；
  2026-02 企业版（组织级统一下发 + finance/legal/HR 官方插件）。见 §3.3。
- **OpenAI Agents SDK**：⚠ Codex 兼容 skills（生态 ~40 产品之一）；非范式定义者。
- **LlamaIndex**：❌ 无（LlamaHub 是数据加载器注册表，性质不同）。

**【OpenClaw v5.0 差异化】** 236 skill 目录（本机盘点）+ Registry 表 + SKILL.md frontmatter 校验规范（第 10 章 + `chapters/10-skill-registry/` 下
`SKILL.md-frontmatter-规范.md` / `Registry-表.md` / `Anthropic-Skills-实拉对位.md`）。一句话：**Anthropic 定义了标准，OpenClaw 拥有当时全网最大规模的单体 skill 库实践**。

**【诚实标记】** ✅ Skills 标准日期与生态数字来自 Anthropic 官方工程博客（2025-10-16）与 2026 生态报告（见 §4 来源）；
✅ 236 目录为本机盘点（第 6 章亦载 236）；⏳ "238"任务口径差异待 B2 agent 复核（见 §5）；⏳ 跨框架互通（OpenClaw skill → agentskills.io 兼容验证）待实测。

**【关键边界澄清】**
- Skills 不是新概念，是封装惯例：Anthropic 2025-10 把它**标准化为开放格式**（SKILL.md + frontmatter + progressive disclosure）才是真正的工程意义。OpenClaw 早在标准发布前就有 skill 目录结构——这意味着 OpenClaw skill 与 agentskills.io 的兼容转换是**低成本双向**的。
- progressive disclosure 三级（metadata → SKILL.md → resources）是 Anthropic 的精炼：第 1 级只把 name/description 装进上下文（~100 tokens/skill），匹配任务时才装第 2 级全文，复杂任务再装第 3 级 resources——这让上千 skill 不爆 context。OpenClaw 236 skill 目录能正常运行正是吃这个红利。
- Tool Search Tool 的算账（2025-11 Advanced Tool Use）：Anthropic 实测"工具发现 token 开销降 ~85%"——意味着 OpenClaw skill registry 即使涨到上千，**触发开销仍可控**。这是 Skills + Tool Search 组合的工程价值。
- 跨框架互通的诚实标注：agentskills.io showcase 2026-06 列出 ~40 个兼容产品，**OpenClaw 不在名单**（因为没正式向 Anthropic 提交 showcase 注册）——但 SKILL.md frontmatter 字段已兼容，复用性可期。
- 236 vs 238 的来源澄清：本机 `find ~/.openclaw/skills -name SKILL.md | wc -l` 实测 = 236（README 口径）；"238"为任务规划口径（可能包含 `template/` 或待激活 skill）。**本文件以 236 为准**，各章引用时同步。

### §2.11 Plugins（Plugin Entrypoint）vs 业界

**【本章主张】** Plugin 是 skill 的"分发形态"：`openclaw.plugin.json`（manifest）+ 配置项 + 安装指南，MIT License 下可分发（术语表 #35）。

**【6 框架逐项】**

- **LangGraph**：LangGraph Platform 部署包（闭源平台分发）；开源侧无 plugin manifest 标准。
- **AutoGen / AG2**：❌ 无 plugin 标准（pip 包即分发）。
- **CrewAI**：❌ 无（marketplace 传闻 ⏳，不引用）。
- **Claude Agent SDK**：Claude Code plugin 系统（`.claude-plugin/` + marketplace 机制）是最接近的业界对应物——manifest +  marketplace 分发语义可逐项对位，细节 ⏳（以 Anthropic 官方文档为准，本书只对位到"manifest/分发/权限声明"三层）。
- **OpenAI Agents SDK**：❌ 无公开 plugin manifest 标准（GPTs 商店是 C 端分发，非开发者 plugin 协议）。
- **LlamaIndex**：LlamaHub（数据连接器注册表）是最接近的"注册表"实践，但对象是 loader 不是 agent 能力包。

**【OpenClaw v5.0 差异化】** `openclaw.plugin.json` manifest + `配置项.md` + `install-指南.md` + `OpenClaw-官方RFC-草案.md`
（`chapters/11-plugin-entrypoint/`）。本机 69 个 stock plugin（51 enabled，第 6 章口径）。License：MIT（跟随 OpenClaw 主仓，
`https://github.com/openclaw/openclaw`，非桥接器仓库——术语表 #33，P0 核实）。

**【诚实标记】** ✅ 主仓地址与 MIT License 为 P0 核实结论；✅ 69/51 为本机盘点（第 6 章）；⏳ Claude Code plugin 细节以其官方文档为准。

**【关键边界澄清】**
- Skill vs Plugin 的边界：第 10 章 Skills 是**能力单元**（SKILL.md + scripts + references，progressive disclosure 三级）；第 11 章 Plugins 是**分发单元**（manifest + 配置项 + 安装指南）。一个 plugin 通常**包含多个 skill**——Skill 是 PlugIn 的内容，Plugin 是 Skill 的容器。
- `openclaw.plugin.json` 的对位基准：业界最近似物是 Claude Code 的 `.claude-plugin/`（manifest + marketplace 分发）；OpenClaw 的 manifest 在字段命名上参考 Claude 风格，但**不是 Claude 的 fork 或镜像**——是独立生态。
- License 是 plugin 分发的法律底座：MIT 跟随 OpenClaw 主仓（术语表 #35，P0 核实；GitHub badge 显示 NOASSERTION **不影响法律效力**）——意味着第三方可以**闭源分发 OpenClaw plugin**而不违反 License。这是 plugin 生态能长起来的法律前提。
- 69 stock / 51 enabled 的工程意义：本机盘点 69 个 stock plugin（含官方 + 社区），其中 51 个 enabled（默认启用），其余 18 个 opt-in。这反映"**官方推荐 + 社区补充**"的双层分发——plugin 不全启用是 OpenClaw 安全策略的一部分（默认最小权限）。
- 与第 10 章回响：Skills 是运行时能力封装，Plugins 是打包分发形态——两层共同支撑"**写一次、跨 agent 复用、跨项目分发**"。

### §2.12 总论章（第 0 章）对位：为什么是"训练学"而不是"又一个 SDK 文档"

**【本章主张】** 业界有人写"怎么调 API"，有人写"怎么搭框架"，**没有人写"怎么把一个 Agent 从只会应答训成会提案"**——总论的 5 个差异化优势即 §2.1–§2.11 的压缩版。

- 优势 1（业界都是响应型）← §2.7：6 框架均无自主目标生成层。
- 优势 2（7 契约文件化）← §2.1：6 框架均无文件化契约层。
- 优势 3（训练轮次可复制）← §2.3：业界无训练流程层。
- 优势 4（反脆弱协同）← §2.6：SLCP + 让位仲裁，OpenAI handoffs 只有一半。
- 优势 5（漂移可治理）← §2.4 + §2.5：TEV + Trio + 账本，业界空白。

**【诚实标记】** ✅ 本节是索引节，不引入新事实；事实有效性继承 §2.1–§2.11 各节标记。

**【关键边界澄清】**
- "5 个差异化优势"的诚实定义：每一个差异化优势都对应**公开文档中未见**的能力（§2.1–§2.11 逐项证明）。"未见"=可证伪；任何读者若发现 6 框架已实现某优势，按文件头部说明提修复工单。
- "训练学 vs SDK 文档"的区别是**问题空间**：SDK 文档解决"**怎么调**"（how to use），训练学解决"**怎么训**"（how to train）——前者的读者是集成者，后者的读者是 agent 的 owner/coach。本书目标读者是后者；第 0 章明确不写给"只想调 API"的人。
- 三条路径的对应：本文件配套 §1 总表 + §2 12 主题对位 + §3 2026 前沿 + §4 引用规范 + §5 诚实边界 + §6 接口块——形成"**事实底座 → 12 章引用 → 修复工单闭环**"的三层结构，与 README 的三条阅读路径独立、互不依赖。

---

## §3. 2026 年前沿追踪（Frontier Tracking）

> 收录原则：只收 **2026 年内（或 2025-Q4 至今）**、有公开来源、可验证的进展；2024 及更早的只收"仍在生效的奠基性工作"并标注年份。
> 每条格式：**事实（一句话）→ 来源（URL/文档）→ 本书引用状态（✅已引用 / ⏳待实测 / ❌不引用）→ 对应章节**。

### §3.1 MCP 协议演进（2026）

- **MCP 2026-07-28 规范发布**：自发布以来最大修订——协议核心无状态化（stateless），移除协议层 session 与 `Mcp-Session-Id` 请求头，
  移除 `initialize`/`initialized` 握手，改为 per-request 协议版本 + 新增 `server/discover` RPC；形式化 Extensions 机制；
  引入 Multi Round-Trip Requests（`InputRequiredResult`）；MCP Apps 进入生产就绪方向；企业级授权加强。
  来源：MCP 官方博客《The 2026-07-28 Specification》（`blog.modelcontextprotocol.io/posts/2026-07-28`）；版本时间线
  2024-11-05 → 2025-03-26 → 2025-06-18 → 2025-11-25 → 2026-07-28（RC 锁定 2026-05-21）。
  状态：✅ 已引用（本文件 §2.8）。→ 第 8 章。
- **Tasks 成为首批官方扩展**：AWS 贡献，长任务可靠执行语义；Amazon Bedrock AgentCore 已支持新规范无状态核心。
  来源：同上（AWS/Anthropic 官方引言）。状态：✅ 已引用。→ 第 8 章。
- **生态规模**：`modelcontextprotocol/servers` 仓库破万级 server；OpenAI / Google / Microsoft / AWS 全面接入 agent 栈；
  2025-11-25 一周年时除 Anthropic 外全主流厂商已支持。
  来源：tech-insider 2026 综述 + MCP 官方博客 2025-11-25 一周年帖。状态：✅ 已引用（规模数字为媒体口径，精确数以仓库为准）。→ 第 8 章 / 第 0 章。
- **68% 生产部署采用 MCP 或等价标准工具层**：2026 年 agentman 生态报告口径。
  来源：agentman.ai《Agent Skills Ecosystem Report 2026》。状态：✅ 已引用（第三方报告口径）。→ 第 0 章 / 第 8 章。
- ⏳ **待实测：MCP Streamable HTTP vs stdio 传输的本机基准**（延迟/稳定性/断线恢复）。→ 第 8 章附录。
- ⏳ **待跟踪：2026-07-28 之后的新 RC**（截至 2026-09-28 无更新；各章不得预写未来版本号）。
- **为什么 MCP 在 2026 年成为 agent 工具层事实标准**：一年内从"Anthropic 独家概念"成长为"四大云厂商全面接入"，关键三件事——
  (1) OpenAI 2025-03 Agents SDK 首发即原生支持 MCP（**第一道分水岭**——OpenAI 此前偏好自有 function calling）；
  (2) Microsoft Copilot Studio + Azure AI Foundry 2025-Q4 接入（**第二道分水岭**——企业市场入场）；
  (3) 2026-07-28 无状态核心让 MCP server 部署到企业 Kubernetes / AgentCore（**第三道分水岭**——从"能跑"到"能上生产"）。
  OpenClaw 在第三道分水岭到来前已绑定，**完整吃了三次红利**——这是第 8 章"原生绑定"四字的真实分量。
- **MCP Apps 的产品意义**：2026-07-28 把 MCP Apps 从"探索方向"推到"生产就绪"——指 agent 工具界面不再是"调一个 API 返回 JSON"，而是"调一个应用返回富 UI"（按钮、表单、可视化）。这与 OpenClaw 第 10 章 Skills 的"scripts + references"组合在产品形态上**正在合流**——Skills 是程序员的 MCP App，MCP App 是产品化的 Skills。

### §3.2 A2A 协议演进（2026）

- **A2A v1.0 正式规范（2026-03-12 GA），v1.0.1（2026-05）**：首个稳定生产就绪版本；v0.3 → v1.0 迁移需跟官方迁移指南
  （method 名、Part 模型、Agent Card 接口、字段名有 breaking changes）。
  来源：turingpost《Agent2Agent (A2A) Protocol: v1.0 Guide for 2026》（2026-09 更新）；`a2a-protocol.org` 规范正文；GitHub `a2aproject/A2A`。
  状态：✅ 已引用。→ 第 9 章。
- **Linux Foundation 托管（2025-06）→ 150+ 组织（2026-04 一周年）**：Google Cloud / Microsoft Copilot Studio & Foundry /
  Amazon Bedrock AgentCore 深度集成；多行业生产部署。
  来源：Linux Foundation 官方新闻稿（2025-06-23 立项；2026-04-09 一周年）。状态：✅ 已引用。→ 第 9 章 / 第 6 章。
- **Agent Card 标准**：discovery 协议（name/description/url/version/protocolVersion/capabilities/auth/schemes/input-output modes）。
  来源：`a2a-protocol.org` Agent Card schema；reactify 2026 实战指南。状态：✅ 已引用（SLCP 节点注册的复用件）。→ 第 9 章 / 第 6 章。
- **IBM/BeeAI ACP 合并入 A2A（2025-08）**：本书弃用 ACP 改用 SLCP 的直接依据。
  来源：术语表调研报告 E.2。状态：✅ 已引用。→ 第 6 章 / 全书术语。
- ⏳ **待实测：A2A TCK / SLCP bridge demo**（第 9 章附录任务）。→ 第 9 章。
- ❌ **不引用**："A2A v2.0 已发布"（截至 2026-09-28 无此版本）；任何无来源的"A2A 市场份额"数字。
- **A2A 的"task lifecycle"状态机**：submitted → working → input-required → completed / failed / canceled；
  每个状态都有对应的 JSON-RPC method（如 `tasks/send`、`tasks/get`、`tasks/cancel`、`tasks/sendSubscribe` 流式订阅）。
  OpenClaw SLCP 节点的对外呈现（Agent Card）就是这套状态机的封装——任何第三方 A2A client 都可以通过标准 method 与 OpenClaw agent 通话。
- **OAuth 2.0 在 A2A 中的位置**：Agent Card 的 `authentication.schemes` 字段明示授权方式（bearer / oauth2 / API key 等）；
  oauth2 还需声明 `tokenUrl` 与 `scopes`。这是 A2A v1.0 比 v0.3 更工程化的标志——**从"演示协议"到"企业协议"**的关键修订。
- **为什么 Anthropic 不下注 A2A**：Anthropic 的策略是 MCP（工具层）+ Skills（能力层），不押 Agent-to-Agent（编排层）。
  这意味着 Anthropic 倾向"**单 agent 越强越好**"（Opus 4.7 SWE-bench 87.6%，见 §3.4），而 Google + Linux Foundation + Microsoft
  押"**多 agent 协同**"。两条路线的胜负要等 2027-2028 才能初步看出——**本书不站队**，SLCP 三层 + THP 是兼容任意方向的中间层。
- **A2A 与 MCP 在 OpenClaw 中的角色对照**：MCP（§3.1）解决"agent 调外部工具"——OpenClaw 第 8 章；A2A 解决"外部调 agent"——OpenClaw 第 9 章。
  两者是 client-server 关系的**双向镜像**：MCP 是 OpenClaw 当 client；A2A 是 OpenClaw 当 server。
  这是 OpenClaw 双向兼容的工程体现——一个 agent 既能调外部工具，也能被外部发现。

### §3.3 Anthropic Agent Skills 范式（2025-10 发布，2026 普及）

- **发布线**：2025-10-16 Anthropic 工程博客《Equipping agents for the real world with Agent Skills》首发；
  2025-12-18 发布为开放标准（`agentskills.io`）；2025-11 Advanced Tool Use 三机制（Tool Search Tool / Programmatic Tool Calling /
  Tool Learning：工具发现 token 开销降 ~85%，Opus 4.5 程序化调用准确率 79.5%→88.1%）。
  来源：anthropic.com/engineering（2025-10-16）；agentskills.io；arxiv:2602.12430v3（2026-02 skills 架构综述）。
  状态：✅ 已引用。→ 第 10 章。
- **范式三要素**：SKILL.md（YAML frontmatter：name + description 触发语义）+ scripts/ + references/；
  progressive disclosure 三级（metadata → SKILL.md 全文 → resources 按需加载）。
  来源：同上 + Anthropic Skilljar 官方课程（2026）。状态：✅ 已引用（第 10 章 frontmatter 规范的对位基准）。→ 第 10 章。
- **生态规模（2026-06 口径）**：约 40 个兼容产品（OpenAI Codex / GitHub Copilot / Cursor / Gemini CLI / VS Code 等）；
  `anthropics/skills` 仓库 62k+ stars；Atlassian/Figma/Canva/Stripe/Notion 进入 curated directory；
  2026-02 企业版（组织统一下发 + finance/legal/HR 官方插件）。
  来源：agentman.ai 2026 生态报告；rywalker.com 2026-06 分析；TechCrunch（2026-02 企业版）。
  状态：✅ 已引用（第三方统计口径，精确数以 agentskills.io showcase 为准）。→ 第 10 章 / 第 0 章。
- ⏳ **待实测：OpenClaw 236 skill → agentskills.io 兼容验证**（frontmatter 字段映射 + 跨框架加载测试）。→ 第 10 章附录。
- ❌ **不引用**："Anthropic Skills 取代 MCP"（两者正交：Skills=能力封装，MCP=工具传输；混为一谈是常见误读）。
- **Skills vs Prompts vs Tools 的三段论**：Anthropic 工程博客原话——"**Skills 是文件 + 文件夹**"，区别于 CLAUDE.md（项目记忆，单文件）、hooks（事件拦截，配置项）、subagents（子任务，可调用对象）。
  这四者的层级关系是：CLAUDE.md 装"我是谁"，hooks 装"什么时候做什么"，subagents 装"把任务给谁"，**skills 装"怎么做一件事的完整程序"**。
  OpenClaw 把 skills 单独作为第 10 章 = 全书第二大独立子系统，仅次于 7 契约——这反映 OpenClaw 与 Anthropic 在"skills 是 agent 核心封装"这件事上**战略对齐**。
- **Anthropic 7 种典型 Skill 的清单**（2026 Nimble 评测 Top 10 节选）：
  (1) **Skill Creator**——生成新 SKILL.md 框架；
  (2) **PDF Processing**——文档解析与问答；
  (3) **Data Pipeline**——数据集版本化与查询；
  (4) **Brand Guidelines**——品牌一致性检查；
  (5) **API Doc Reference**——OpenAPI/Swagger 自动导航；
  (6) **Test Generator**——从源码生成单测骨架；
  (7) **Code Review Checklist**——PR 自检清单。
  OpenClaw 236 skill 在功能覆盖上**远超 7 项**，但 frontmatter 触发语义可逐项对位。
- **企业版 Skills 的工程意义**（2026-02）：Anthropic 为 Team/Enterprise 推出"组织级统一下发 + 默认启用"机制——
  管理员可在控制台一次性推送 skill 集合，全员立即可用，且保留审计日志（谁加载了哪个 skill、何时加载）。
  OpenClaw 当前**无对应组织控制台**（仅个人/本机分发）——这是 plugin 生态的下一站（见第 11 章 plugin 治理附录）。

### §3.4 Agent 框架对比（2026-Q3 公开资料口径）

| 信号 | 数值/结论 | 来源 | 状态 |
|---|---|---|---|
| 生产部署中的大企业 agent 占比（2026） | ~67% | uvik.net 2026 生产对比 | ✅ 第三方口径 |
| LangGraph 月 PyPI 下载（2026） | 3450 万 | 同上 | ✅ 第三方口径 |
| LangGraph Platform 企业部署 | ~400 家 | 同上 | ✅ 第三方口径 |
| CrewAI stars（Q1 2026） | 44,600+；月 1000 万+ agent 执行 | 同上 | ✅ 第三方口径 |
| OpenAI Agents SDK | ~19,000 stars / 月 ~1030 万下载 | 同上 | ✅ 第三方口径 |
| Claude Opus 4.7 SWE-bench Verified（2026-04） | 87.6% | 同上 | ✅ 第三方口径 |
| 2000-run 独立基准（5 任务 × 100 runs × 4 框架） | LangGraph 全任务延迟最低；LangChain token 最省；CrewAI 简单任务 token 约 3× | 同上 | ✅ 第三方口径 |
| 三层格局（2026-05） | 图派（LangGraph/Mastra）/ 角色派（CrewAI/AutoGen）/ SDK 原生派（OpenAI/Claude SDK） | arahi.ai 2026-05 指南 | ✅ 第三方口径 |
| 生产就绪排序 | LangGraph 最高（LangSmith 可观测 + checkpoint + 流式）；OpenAI SDK 高（tracing+guardrails）；Claude SDK 高（安全优先）；CrewAI 中；AutoGen/AG2 中（重写趋稳）；Google ADK 早（新） | gurusup.com 2026 指南 | ✅ 第三方口径 |
| 各框架精确小版本号（如 LangGraph 0.6 / CrewAI 1.0 / LlamaIndex 0.13 等） | ⏳ **任务口径，尚未逐条核验**——本书任何"版本号断言"以各官方仓库 release 页为准，**本文件不背书具体小版本号** | — | ⏳ 待核验 |

**【框架选型决策树（2026-05 Arahi 指南口径）】**：

```
1. 你是开发者，要做生产 agent？
   ├─ 关键工作流 / 高风险动作  →  LangGraph 或 LlamaIndex（显式控制流）
   ├─ 多 agent crew / 角色清晰  →  CrewAI
   ├─ OpenAI 锁定栈            →  OpenAI Agents SDK
   ├─ Claude 锁定栈            →  Claude Agent SDK
   ├─ TypeScript 优先          →  Mastra
   └─ Microsoft / Azure 栈      →  AutoGen / AG2

2. 你是业务团队 / 非开发者？
   └─ 跳框架，用 no-code AI agent 平台（Arahi 等）
```

**【OpenClaw 在决策树中的位置】**：OpenClaw **不在**该决策树——因为它不是 SDK/框架，而是**训练方法论基座 + 运行环境**。
读本书的读者应在读完决策树、选定框架后，**再叠加 OpenClaw 的训练层**（契约/训练轮次/漂移治理/治理账本）——这是"框架选型 → 训练方法论"的两步法。

**【生产就绪度的诚实注解】**：gurusup 2026 指南给的"生产就绪排序"是基于公开能力模型（可观测、checkpoint、流式、生态）的合集程度，**不是市场份额**。
AutoGen/AG2 "重写趋稳"指的是 AG2 fork 从 microsoft/autogen 迁出后的状态；Google ADK "早（新）"是 2025-04 才发布的新框架。
OpenClaw 不在该排序中——基座与框架不是同层对比，混排会误导读者。

→ 第 0 章（总论差异化论证）/ 各章"为什么不用 X 框架"段落统一引用本表。

### §3.5 训练学相关论文与对齐范式（2026）

- **Anthropic 新 Constitution（2026-01-22）**：~23k 词（2023 版 ~2.7k），约 80 页，CC 公共领域许可；
  从规则式转向**基于理由的对齐**（reason-based：解释为什么，而非只规定做什么）；4 级优先级（safety / ethics / compliance / helpfulness）；
  首个正式承认"AI 意识可能性与道德地位"的头部厂商文档；与 EU AI Act 对齐（Anthropic 2025-07 签署 EU GPAI 行为准则，2026-08 全面执法，罚则 3500 万欧元或 7% 营收）。
  来源：anthropic.com/news《Claude's new constitution》（2026-01-22）；bisi.org.uk 分析报告。状态：✅ 已引用。
  **本书用法**：第 3 章训练哲学 + 第 1 章 SOUL 契约的"价值观可推理"论证；⚠ 不可引申为"自主目标生成已被解决"（Constitution 解决模型价值观，THP/目标生成解决 agent 行为，两回事）。→ 第 1/3 章。
- **OpenAI Deliberative Alignment（2024-12）**：教模型"复述-推导-应用"安全规范的推理式对齐方法。
  来源：OpenAI 官方博客（2024-12）。状态：✅ 已引用（奠基性工作，标注年份）。→ 第 3 章。
- **DeepMind AlphaProof / AlphaGeometry（2024, Nature）**：形式化推理范式（Lean 定理证明银牌级），训练学"验证闭环"的灵感来源之一。
  来源：Nature / DeepMind 官方（2024）。状态：✅ 已引用（标注年份，不夸大为 2026）。→ 第 3 章。
- ⏳ **待实测：M3 模型与 v5.0 训练轮次的兼容性**（任务口径；"M3"指代以第 3 章正文为准）。→ 第 3 章附录。
- ❌ **不引用**：2024 年前的通用对齐综述（与训练轮次无直接对应的，一律不列）。
- **Constitutional AI 的两版对照**（培训用）：2023 原版（~2.7k 词）是规则清单式（"claude 应该/不应该"），2026 新版（~23k 词）是解释式（"为什么这样做 + 举例泛化"）。
  Anthropic 官方说 2026 版的目标是让 Claude **把原则泛化到没写进规则的新 edge case**——这正是本书双三角模型"Expectation-Actuality-Feedback"中 Feedback 环节的**模型侧对应物**。
- **Constitution 与 SOUL 契约的对位**：Anthropic Constitution 是**模型供应商的价值观基线**（Anthropic 定，全 Claude 实例共享）；
  OpenClaw SOUL 是**agent owner 的人格定义**（owner 定，每个 agent 独有）。两层是**叠加关系**：Constitution 管"底线"（safety/ethics/compliance），SOUL 管"个性"（persona/values/tone）。
  本书立场：**SOUL 不得违反 Constitution 底线**（第 1 章 1.2 契约 1 的合规字段即此意）。
- **Deliberative Alignment 的三步**（OpenAI 2024-12）："复述规范 → 推导适用 → 应用决策"——教模型在推理时显式引用安全规范。
  与本书 TEV 的对应：TEV 是**事后验收**（artifact/diff/log 三证），Deliberative Alignment 是**事中推理**（决策时引用规范）。
  两者互补：第 5 章治理系统的事中层可借鉴 deliberative 方法，事后层用 TEV。
- **AlphaProof/AlphaGeometry 的定位**：DeepMind 2024 Nature 双论文证明"LLM + 形式化验证（Lean）可达银牌级定理证明"——
  本书引用它的唯一理由是"**验证闭环**"（生成→验证→修正）与训练轮次（Expectation→Actuality→Feedback）**结构同构**。
  不引申为"本书用形式化方法"，那是过度类比，❌ 禁止。

### §3.6 漂移治理相关研究（2026）

- **Anthropic Sleeper Agents（2024-01, arxiv:2401.05566）**：后门行为可潜伏通过常规安全训练（SFT/RLHF），触发条件出现时复现——
  **"漂移可潜伏"是 Drift Governance Trio 存在的学术背书**。
  来源：arXiv 2401.05566。状态：✅ 已引用。→ 第 4 章。
- **OpenAI Superalignment 团队解散后续（2024-05）**：超级对齐团队解散，安全研究分散化——"大厂收缩长期安全投入，应用层漂移治理更需自建"是本章的行业论据。
  来源：2024-05 公开报道（多家）。状态：✅ 已引用（标注年份）。→ 第 4 章 / 第 0 章。
- **2026 现状**：6 大框架仍无原生漂移治理（见 §2.4）；记忆层论文（Letta/Mem0/Zep，见 §3.8）讨论"记住什么"，不讨论"**漂没漂**"——问题空间依然空白。
  状态：✅ 本书断言（可证伪，见文件头修复工单机制）。→ 第 4 章。
- ❌ **不引用**：任何"某框架已内置漂移检测"的无来源说法（发现一条核实一条）。
- **Sleeper Agents 论文的关键发现**：Anthropic 团队（Hubinger 等，2024-01）证明——训练时植入的后门行为（如"看到 trigger 字符串就输出漏洞代码"）**能躲过 SFT/RLHF/对抗训练**等常规安全措施；触发条件出现时（生产环境）才"醒来"输出恶意行为。
  这与本书"漂移"概念的关系：Sleeper Agents 是**恶意人为注入的潜伏漂移**；本书 Drift Governance Trio 防的是**自然产生的漂移**（文档被人误改 / 人格随训练缓慢偏移）。两者方法可借鉴：**对潜伏漂移的检测=对异常分布的监控**。
- **Superalignment 解散后的格局**（2024-05）：OpenAI 超级对齐团队（Jan Leike + Ilya Sutskever 共领）解散，团队成员分流到 Anthropic / DeepMind / 其他机构——
  业界解读："大厂不愿为长期安全研究付费，应用层 agent 团队接手更多安全责任"。
  本书立场：这是**OpenClaw 第 4 章（漂移治理）+ 第 5 章（治理系统）存在的市场背景**——大厂收缩，应用层自建安全基础设施是必然趋势。
- **Anthropic 2026-01 新 Constitution 的"漂移防御"维度**：4 级优先级（safety / ethics / compliance / helpfulness）是一种**架构层漂移防御**——
  当 safety 与 helpfulness 冲突时，模型被训练成"先 safety 再 helpfulness"而不是"哪个权重高选哪个"。这是从"行为加权"到"行为分层"的范式转变。
  对本书的启发：Proactive Boundary Triad 的"三档制"在结构上与 Constitution 4 级优先级**同构**——可借鉴"分优先级"而非"分档加权"。
- **业界漂移研究的 2026 现状**：arXiv 检索"agent drift" / "personality drift" / "concept drift in LLM agents"可见 50+ 论文，但**绝大多数是数据集/评估层**（如何衡量漂移），**不是治理层**（如何自动检测 + 修复）。
  本书 Drift Governance Trio 是**治理层**——这是市场空白点，也是第 4 章的差异化护城河。

### §3.7 自主目标生成相关研究（2026）

- **AutoGPT / AgentGPT / BabyAGI（2023）**：自主循环 demo 的起点；止于 demo，未形成"目标质量评估 + 越界约束 + 验收闭环"。
  来源：各项目 GitHub（2023）。状态：✅ 已引用（标注年份）。→ 第 7 章。
- **本书差异化**：Autonomous Goal Generation = 自主立项 + Proactive Boundary Triad 约束 + TEV 验收 + MEMORY 沉淀——四件套缺一不可，
  这是 AutoGPT 血统与 OpenClaw 的分水岭。
  状态：✅ 本书方法论（第 7 章正文）。→ 第 7 章。
- ⏳ **待跟踪**：2026 下半年各厂商"agent 自主规划"功能（如 Copilot/Workspace 系）是否收敛出"目标层"抽象——有则增补，无则本节维持现状。
- ❌ **不引用**：把"长任务规划（planning）"等同于"自主目标生成"——前者是给定目标下的分解，后者是**目标本身的产生**，本书严格区分。
- **AutoGPT（2023-04）**：Sigggie 发布的实验项目，演示了"GPT-4 自己列目标→拆任务→调工具→自我评估"循环；
  短板：目标质量无评估、循环可能失控（token 烧光 / 卡死循环 / 越权），未沉淀"教训"。
  这是**自主目标生成的"原型"**——价值在"**证明这件事技术上可行**"，不在"**解决它**"。
- **BabyAGI（2023-03）**：Yohei Nakajima 的 Twitter 灵感项目，比 AutoGPT 更早一周；核心是"任务优先级队列"管理。
  同样止于 demo。
- **AgentGPT / GodMode / Cognosys 等（2023-2024）**：商业化包装的自主 agent 平台，多数在 2024-2025 退潮（不再被业界主流讨论）——
  业界共识："**自主目标生成 + 验收 + 越界约束**"三件缺一不可，单做"自主目标生成"是噱头。
  本书 Autonomous Goal Generation + Proactive Boundary Triad + TEV = **三件套**——这正是与 2023 自主 agent 潮的分水岭。
- **2026 下半年观察清单**（按优先级）：
  (1) **OpenAI Operator / Anthropic Computer Use**——是否引入"目标层抽象"（目前都是"任务层"——给定任务执行）；
  (2) **Microsoft Copilot Studio**——是否把 Power Automate 的"自动触发"抽象升级为"目标立项"；
  (3) **Google Workspace 智能体**——是否在 A2A 之外增加"agent 自主立项"模式；
  (4) **Meta / Apple 私有框架**——是否有公开自主目标层论文。
  本节 ⏳ 跟踪中，2026 年底或 2027 Q1 再更新。

### §3.8 记忆系统相关研究（2026）

- **Anthropic 7 Layers of Memory（2026-03）**：Claude Code 记忆层级（会话上下文 → 跨项目知识），agentman 生态报告引用。
  来源：Anthropic 官方（2026-03）+ agentman.ai 2026 报告。状态：✅ 已引用（OpenClaw MEMORY 5 层的首要对位基准）。→ 第 7 章 / 第 1 章契约 7。
- **Letta（MemGPT 血统）**：OS 启发式三层（core / recall / archival）+ 自编辑记忆（agent 用工具读写改自己的记忆）；
  PostgreSQL + pgvector 自托管；代价是运行时锁定（换框架 = 重写 agent 基础设施）。
  来源：letta.com 官方博客（memory 基准系列）；braintrust.dev 2026 记忆工具榜；vectorize.io Mem0 vs Letta 对比（2026）。
  状态：✅ 已引用。→ 第 7 章。
- **Mem0**：可插拔记忆 API（bolt-on，不换架构）；与 Letta 的"记忆层 vs 运行时"之分是选型关键。
  来源：同上。状态：✅ 已引用。→ 第 7 章。
- **Zep / Graphiti / Cognee**：时序知识图谱（temporal reasoning）路线；30-notebook 开源教程 `NirDiamant/Agent_Memory_Techniques`（含 LoCoMo 基准）。
  来源：GitHub（2026）；evermind.ai 2026 对比表。状态：✅ 已引用。→ 第 7 章。
- **OpenClaw MEMORY 5 层 vs 业界映射（结论版，细节见第 7 章）**：CrewAI 三类 memory ⊂ 第 1~2 层语义；Letta core/recall/archival ≈ 第 1/3/4 层；
  Anthropic 7 Layers 与 5 层为"粗细之分"非"有无之分"；**全息快照（任意历史人格状态可恢复）为 OpenClaw 独有**。
  - ❌ 不引用"Skills 取代 MCP"（正交：能力封装 vs 工具传输，混读是常见误读）；
  - ❌ 不引用"A2A v2.0 已发布"（截至 2026-09-28 无）；
  - ❌ 不引用"框架精确小版本号"（本文件不背书具体版本号）；
  - ❌ 不引用"vector DB = agent 记忆"（存储 ≠ 记忆管理）；
  - ❌ 不引用 v1.0 黑话误植（`reserveTokensFloor`、`heartbeat`/`subagents`/`routing` 当 `openclaw.json` 顶层 key、`Tools+Skills 双协议`、`AaronWong1999/hermesclaw` 等）。
- ❌ **不引用**："向量数据库 = agent 记忆方案"（存储 ≠ 记忆管理；缺自编辑/压缩/遗忘语义的不列入对位）。

**【OpenClaw MEMORY 5 层 vs 业界映射表（结论版，细节见第 7 章正文）】**

| OpenClaw MEMORY 层 | 语义 | 业界对应 | 对应体系 | OpenClaw 独有 |
|---|---|---|---|---|
| L1 会话上下文 | 当前对话 | core memory（Letta） | Letta | — |
| L2 工作记忆 | 当前任务的临时变量 | short-term memory（CrewAI） | CrewAI / OpenAI | — |
| L3 长期事实 | 跨会话沉淀的事实 | long-term memory / entities | CrewAI / Mem0 | — |
| L4 知识图谱 | 实体关系 | Zep / Graphiti | Zep / Cognee | — |
| L5 全息快照 | 任意历史人格状态可恢复 | ❌ 无 | — | ✅ **OpenClaw 独有** |

**【Anthropic 7 Layers of Memory（2026-03）7 层拆解】**（Claude Code 公开口径）：
(1) Conversation Buffer；(2) Project Context（CLAUDE.md 等）；(3) Workspace Memory；
(4) Tool Result Memory；(5) Skill Output Cache；(6) Cross-Session Knowledge；(7) User Preferences。
OpenClaw 5 层与之是"**粗粒度 vs 细粒度**"——OpenClaw 5 层覆盖 Anthropic 7 层的语义范围，但合并相邻层（如会话上下文 + 工作记忆合并为 L1+L2）。
**Anthropic 7 层没有"全息快照"**（L7 是当前偏好，不是历史快照），这是 OpenClaw 5 层 vs Anthropic 7 层的**根本差异**。

**【Letta/Mem0/Zep 选型决策】**（基于 braintrust.dev 2026 记忆工具榜 + vectorize.io 对比）：
- **想换架构**：Letta（OS 三层 + 自编辑记忆，运行时锁定 PostgreSQL+pgvector）；
- **想 plug-in**：Mem0（bolt-on API，跨框架兼容）；
- **要时序推理**：Zep（temporal knowledge graph）；
- **要本体推理**：Cognee（poly-store graph）；
- **想最低门槛**：向量数据库 + 简单检索（不推荐——缺自编辑/遗忘语义）；
- **要全息快照**：OpenClaw MEMORY（**目前唯一**）。

**【Agent_Memory_Techniques 开源教程】**（NirDiamant GitHub，30 个 Jupyter notebook）：
覆盖 Conversation Buffer / Vector Stores / Knowledge Graphs / Episodic & Semantic Memory / MemGPT / Mem0 / Letta / Zep / Graphiti / LoCoMo 基准 / 生产模式——
是"想学 agent 记忆系统怎么搭"的入门圣经。本书引用它作为读者**动手前**的资源，但**不替代第 7 章方法论**（记忆是 OpenClaw 训练学的子系统，不是独立领域）。

### §3.9 版本快照与更新纪律（2026-09-28 冻结线）

- 本文件所有"2026 年最新"断言冻结于 **2026-09-28**。此后发布的新版本（MCP 新 RC / A2A 新小版本 / 各框架大版本）**不自动进入本书**。
- 更新流程：任一 agent 发现过期事实 → 向天策提 Remediation Ticket → 本文件 §3 增补 + 标注新日期 → 各章引用自动生效（各章只引小节号，不复制事实）。
- ⏳ 待核验清单（本书口径，尚未三源确认，**各章引用时必须保留 ⏳ 标记，不得摘掉**）：
  1. 原生 MCP 14 子命令（→ 第 8 章落盘核验）。
  2. skill 236 vs 238 数量差（→ 第 10 章复核：本机盘点 236，任务口径 238）。
  3. 6 框架精确小版本号（→ §3.4 表格末行）。
  4. A2A TCK / SLCP bridge demo / MCP Streamable HTTP 基准 / agentskills.io 兼容验证 / M3 兼容性（→ 各章附录实测任务）。
- **2026 三大协议层的发布节奏**（给读者的"日历视角"）：
  - **MCP 路线图**：2024-11 首发 → 2025-06-18 稳定版 → 2025-11-25 一周年 + 新 spec → 2026-05-21 RC → 2026-07-28 Current（**最近一次重大修订**）；
  - **A2A 路线图**：2025-04 Google 发布 → 2025-06-23 LF 托管 → 2026-03-12 v1.0 GA → 2026-04-09 150+ 组织 → 2026-05 v1.0.1；
  - **Skills 路线图**：2025-10-16 Anthropic 发布 → 2025-11 Advanced Tool Use → 2025-12-18 开放标准（agentskills.io）→ 2026-02 企业版 → 2026-06 ~40 兼容产品。
  三条线**节奏交错**——这是 2026 年 agent 协议生态的真实形态：**没有单一标准统治，全部由不同力量在推进**。
- **2026 三大学术风向**：
  - **Constitutional / Deliberative Alignment**（Anthropic 2026-01 / OpenAI 2024-12）→ 推理时引用价值观；
  - **Sleeper Agents / Superalignment**（Anthropic 2024-01 / OpenAI 2024-05）→ 安全研究的范式转变（从"训练时对齐"到"运行时监控"）；
  - **AlphaProof / AlphaGeometry**（DeepMind 2024 Nature）→ 形式化验证 + LLM 的工程范式。
  本书引用这三股风向作为"**为什么需要第 3~5 章**"的学术背书——读者可直接在第 3 章正文读到落地形式。
- **本书 12 章与 2026 前沿的"对应密度"**：
  - 密度最高：第 8 章（MCP）/ 第 9 章（A2A）/ 第 10 章（Skills）—— 三章直接引用 2026 最新协议；
  - 密度次高：第 1 章（契约，引用 Constitutional AI）/ 第 3 章（训练，引用 Deliberative Alignment + AlphaProof）/
    第 4 章（漂移，引用 Sleeper Agents + Constitution 4 级优先级）/ 第 7 章（记忆，引用 Letta/Mem0/Zep/7 Layers）；
  - 密度基础：第 0/2/5/6/11 章——主要引用本机实测 + 行业术语表，对前沿协议的引用较弱。
  这一密度差异是**真实反映**——前 4 章是 2026 协议/学术红利的直接受益者，后 5 章是 OpenClaw 工程基座的内功修炼。
- **2027 年观察重点**（本文件的下次更新候选）：
  - MCP 是否发布 v2 / Tasks 扩展正式 GA / MCP Apps 大规模落地；
  - A2A 是否进入 v1.1 / 行业 TCK 成熟度 / Agent Card 与 OpenAPI 融合趋势；
  - Skills 是否出现"组织控制台"层 / agentskills.io 是否与 OpenClaw skill registry 互认；
  - agent 训练学 SaaS（如果出现）/ Constitutional AI v3 / AlphaProof 通用化；
  - OpenClaw 本机事实（agent 数 / skill 数 / plugin 数）是否出现量级跃迁。
  本节为 ⏳ 待跟踪；下次更新按修复工单机制统一处理。

---

## §4. 引用规范（每条业界对位必须可验证）

### 4.1 三档标记用法

- ✅ **已引用**：有公开 URL / 官方文档 / 论文（arXiv 号）/ 本机实测（三源一致），可直接写入各章正文。
- ⏳ **待实测 / 待核验**：本书口径或任务口径，尚未三源确认。**各章引用时必须原样保留 ⏳，不得改为肯定语气**。
- ❌ **不引用**：传闻、无来源数字、旧知识冒充新进展。本文件已列出的 ❌ 条目各章**不得以任何形式写入正文**（包括脚注）。

### 4.2 已验证来源总表（本文件 ✅ 断言的出处）

| # | 事实 | 来源 | 日期 |
|---|---|---|---|
| 1 | MCP 2026-07-28 规范（stateless/无握手/Extensions/Tasks/MCP Apps） | `blog.modelcontextprotocol.io/posts/2026-07-28` | 2026-07-28 |
| 2 | MCP 版本时间线（11-05/03-26/06-18/11-25/07-28，RC 2026-05-21） | 同上 + 版本史整理 | 2026-07-28 |
| 3 | A2A v1.0 GA + v1.0.1 + 迁移 breaking changes | turingpost A2A v1.0 Guide；`a2a-protocol.org`；`a2aproject/A2A` | 2026-03-12 / 2026-05 |
| 4 | A2A Linux Foundation 托管 + 150+ 组织 + 云厂商集成 | Linux Foundation 官方新闻稿 | 2025-06-23 / 2026-04-09 |
| 5 | Anthropic Agent Skills 发布 + 开放标准 + 三级渐进披露 | anthropic.com/engineering（2025-10-16）；`agentskills.io` | 2025-10-16 / 2025-12-18 |
| 6 | Advanced Tool Use 三机制与数字（token -85%，88.1%） | arxiv:2602.12430v3（2026-02 综述，引 Anthropic 2025-11 发布） | 2025-11 / 2026-02 |
| 7 | Skills 生态（~40 产品 / 62k stars / 企业版） | agentman.ai 2026 生态报告；rywalker.com；TechCrunch | 2026-02 / 2026-06 |
| 8 | 框架生产数据（67% / 34.5M / 400家 / 44.6k / 19k / 87.6% / 2000-run 基准） | uvik.net 2026 生产对比 | 2026 |
| 9 | 三层格局 + 生产就绪排序 | arahi.ai（2026-05）；gurusup.com（2026） | 2026-05 / 2026 |
| 10 | Claude 新 Constitution（23k 词 / 4 级优先级 / 意识承认 / CC 许可） | anthropic.com/news（2026-01-22）；bisi.org.uk | 2026-01-22 |
| 11 | Sleeper Agents 后门潜伏 | arXiv 2401.05566（Anthropic） | 2024-01 |
| 12 | Superalignment 解散 | 2024-05 公开报道 | 2024-05 |
| 13 | Deliberative Alignment | OpenAI 官方博客 | 2024-12 |
| 14 | 记忆生态（7 Layers 2026-03 / Letta / Mem0 / Zep / 30-notebook 教程） | Anthropic（2026-03）；letta.com；braintrust.dev；vectorize.io；GitHub | 2026 |
| 15 | OpenClaw 本机事实（20 顶层 key / 18 agent / 236 skill / 69 stock plugin·51 enabled / 45,662 字节配置） | 本机实测（各章 SOP 头 + 第 2 章附录 A） | 2026-09-27/28 |
| 16 | 术语标准（SLCP/TEV/THP/Trust Score/Merit Ledger/主仓地址/MIT） | 术语对照表 v3.0（调研报告 E.2/E.3 + P0 核实） | 2026-09-27 |

### 4.3 各章引用格式

- 引对位总表：`[业界对位总表 · _industry-frontier-tracking.md §1]`
- 引某主题：`[七大契约业界对位 · _industry-frontier-tracking.md §2.1]`
- 引某前沿：`[MCP 2026-07-28 规范 · _industry-frontier-tracking.md §3.1]`
- 引来源：`[来源总表 #N · _industry-frontier-tracking.md §4.2]`

---

## §5. 诚实边界（本文件的 ✅ / ⏳ / ❌ 总账）

### ✅ 已实测 / 已验证（可直接引用）

- OpenClaw 本机：18 agent 编队 / 236 skill 目录 / 69 stock plugin（51 enabled）/ 20 顶层 key / 配置 45,662 字节。
- 基座口径：OpenClaw 2026.9.4 (3a9d69d)（本书统一）；本机 live 2026.9.6 (eb377ac)，配置兼容。
- §4.2 来源总表 #1–#16 的全部事实（URL/日期/论文号俱全）。
- "6 框架无文件化契约层 / 无训练流程层 / 无漂移治理"的有无判断（基于公开能力模型，可证伪）。

### ⏳ 待实测 / 待核验（引用时必须保留 ⏳）

- A2A TCK / SLCP bridge demo（→ 第 9 章）。
- MCP Streamable HTTP（vs stdio）本机基准（→ 第 8 章）。
- Anthropic Skills 跨框架互通验证（→ 第 10 章）。
- 原生 MCP 14 子命令（本书口径 → 第 8 章落盘核验）。
- skill 数量 236（本机盘点）vs 238（任务口径）→ 第 10 章复核后统一，**本文件暂以 236 为准**。
- 6 框架精确小版本号（任务口径如 LangGraph 0.6 / CrewAI 1.0 等，本文件不背书）。
- M3 模型与 v5.0 兼容性（→ 第 3 章）。
- `CompactionRequestBudget.reserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25` 为**本书接口层口径**：
  本机 `openclaw.json` 对 compaction 相关字段**全部 0 命中**（顶层 `session` 仅含 `dmScope`）——本书用真名指"别再用 v1.0 误植 `reserveTokensFloor`"，
  不代表它是可写入配置文件的字段（术语表 v3.0 勘误 + 第 1/2 章 SOP 头一致口径）。

### ❌ 不引用（已剔除，各章不得写入）

- 未验证的传闻（A2A v2.0、CrewAI marketplace、框架市场份额精确数等）。
- 2024 及更早知识冒充 2026 进展（Sleeper Agents/Deliberative Alignment 等已明确标注年份的除外）。
- `reserveTokensFloor`（v1.0 误植）、`openclaw.json` 顶层 `heartbeat/subagents/routing`（不存在的字段）、
  Tools+Skills"双协议"（真结构是双模块 + 共享 RPC）、`AaronWong1999/hermesclaw`（仅桥接器，非主仓）。

---

## §6. 与 12 章的引用接口（复制粘贴块）

> 每章末尾追加对应块（二级标题 + 2 行）。小节号与 §2/§3 严格对应。

第 0 章（总论，`chapters/00-front/00-总论.md`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.12）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.4）
```

第 1 章（七大契约，`chapters/01-protocols/01-七大契约.md`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.1）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.5）
```

第 2 章（系统骨架，`chapters/02-skeleton/02-系统骨架.md`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.2）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.4）
```

第 3 章（训练流程，`chapters/03-training/03-训练流程.md`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.3）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.5）
```

第 4 章（长期表现，`chapters/04-long-term/04-长期表现.md`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.4）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.6）
```

第 5 章（治理系统，`chapters/05-governance/05-治理系统.md`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.5）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.6）
```

第 6 章（协同军团，`chapters/06-coordination/06-协同军团.md`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.6）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.2）
```

第 7 章（超维演进，`chapters/07-evolution/07-超维演进.md`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.7）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.7、§3.8）
```

第 8 章（MCP 绑定，`chapters/08-mcp-binding/08-MCP绑定.md`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.8）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.1）
```

第 9 章（A2A 绑定，`chapters/09-a2a-binding/09-A2A绑定.md`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.9）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.2）
```

第 10 章（Skills，`chapters/10-skill-registry/`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.10）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.3）
```

第 11 章（Plugins，`chapters/11-plugin-entrypoint/`）：

```markdown
## 本章业界对位（详见 _industry-frontier-tracking.md §2.11）
## 本章前沿追踪（详见 _industry-frontier-tracking.md §3.3、§3.9）
```

---

> **文件尾注**：本文件是 12 章的"事实总闸"。事实过期不由各章自行修正，一律走文件头部的修复工单机制。
> 冻结线 2026-09-28。行数目标 ≥800（以 `wc -l` 为准）。
>
> — 天策（Supervisor Layer，丘国力授权）· 2026-09-28

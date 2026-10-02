# 平台与前沿实践证据底稿

> 项目：《训虾手册：从响应型 Agent 到可治理的硅基组织》  
> 文档性质：研究底稿，不是正式书稿，不直接替代章节事实审校  
> 核验截止：2026-09-30（Asia/Shanghai）  
> 核验对象：OpenClaw、Hermes Agent、Meta Muse、MCP、A2A、Agent Skills、Agent 评测、安全与可观测实践  
> 当前本地固定版本：OpenClaw `2026.9.6 (eb377ac)`；Hermes Agent `0.20.1 (2026.8.13)`  
> 编辑原则：稳定原理进入正文；版本事实进入实现框或附录；厂商声明必须标明来源；推断必须可证伪。

---

## 1. 执行摘要

### 1.1 总体判断

1. 八卷二十四章的生命周期主线成立，但第 6、12、13、19、20、21 章必须显式补入 OpenClaw 当前架构中的控制平面、Provider、消息投递、插件与 Hooks、远程执行、状态恢复等组件，才能称为覆盖主要系统架构。
2. 三平台不应平均分配篇幅。建议采用“一个原理、三个镜面”：OpenClaw 是主实现，Hermes 是第二开放实现，Muse 是托管式产品、安全边界与交互设计案例。
3. Hermes 与 OpenClaw 在 Runtime、Gateway、Session、Memory、Skills、Plugins、Cron、Subagents、安全审批等方面可形成强对照；但文件、配置、权限和状态语义不能直接互译。
4. Muse 公开了较完整的安全架构叙述，包括隔离 VM、Sentinel、凭证代理、网络出口控制、审批和审计；这些材料均来自 Meta，尚不足以构成独立验证，应标为 `VENDOR-CLAIM`。
5. MCP、A2A、Agent Skills 解决的是三类不同问题：能力/上下文连接、Agent 间任务协作、程序性知识封装。三者不能互相替代，也不能共同被简称为“Agent 协议”。
6. 2026 年 Agent 评测的稳定共识是同时验证轨迹、工具调用、环境终态和业务结果；只看最终回答或一次演示不足以证明能力。
7. 安全的稳定共识是：模型不应被视为可信执行主体；提示词约束不能代替身份、最小权限、沙箱、审批、凭证隔离、出口控制和审计。
8. 可观测性的稳定对象是任务、轨迹、模型调用、工具调用、交接、环境状态、成本、延迟和错误；具体 OpenTelemetry GenAI 属性仍在迁移，不宜把当前字段写成永久标准。
9. “主动性”应由事件价值和风险状态机控制，而非单纯提高心跳频率。无变化保持安静、敏感动作进入确定性审批，是可跨平台迁移的设计原则。
10. “硅基生命”可以作为贯穿全书的管理与教学隐喻，但不能据此推导意识、人格权或道德主体结论。每次仿生解释都应配套工程映射和比喻边界。

### 1.2 置信度说明

| 主题 | 置信度 | 原因 |
| --- | --- | --- |
| OpenClaw 2026.9.6 架构范围 | 高 | 本地版本、官方发行、官方文档三路核对 |
| Hermes 0.20.1 架构范围 | 高 | 本地版本与官方开发者/用户文档核对 |
| MCP 2026-07-28 | 高 | 正式规范、官方发行、官方安全指南相互支持 |
| A2A v1.0.1 | 高 | 官方规范与官方发行相互支持 |
| Agent Skills 当前格式 | 中高 | 官方规范与官方仓库支持；激活、权限和分发治理仍有实现差异 |
| Agent 评测通用原则 | 高 | Anthropic、OpenAI、NIST 三个来源方向一致 |
| Agent 安全通用原则 | 高 | NIST、OWASP、MCP、Anthropic 与两平台实践交叉支持 |
| OpenTelemetry GenAI 具体字段 | 中低 | 官方语义约定正在迁出主仓，当前字段可能变化 |
| Muse 内部安全效果 | 中低 | 架构叙述充分，但主要来自 Meta 自述，缺少公开独立复现 |

---

## 2. 证据规则与写作口径

### 2.1 事实类型

| 标签 | 定义 | 正文允许的表达 |
| --- | --- | --- |
| `STABLE-PRINCIPLE` | 至少两个独立高质量来源支持，且不依赖单一版本 | “应当”“通常”“本书建议作为默认原则” |
| `VERSION-FACT` | 固定版本、固定提交或带日期规范中的事实 | “在 OpenClaw 2026.9.6 中……” |
| `OFFICIAL-DOC` | 官方当前文档，但没有固定提交 | “截至 2026-09-30，官方文档说明……” |
| `VENDOR-CLAIM` | 单一厂商对自身产品、效果或安全性的声明 | “Meta 表示……；尚缺少独立验证” |
| `LOCAL-VERIFIED` | 本机只读命令或固定源码复现 | “本机在核验日显示……” |
| `METHODOLOGY` | 本书原创方法、模型或命名 | “本书定义/建议……” |
| `INFERENCE` | 从多个事实推导出的编辑或架构判断 | “据此推断……；适用条件是……” |
| `OPEN-QUESTION` | 证据不足、仍在标准化或存在冲突 | “尚未确定”“应在出版前复核” |

### 2.2 两轮核验要求

- 第一轮：确认来源属于官方规范、官方代码/发行、标准组织、政府研究机构或原厂工程文档。
- 第二轮：关键主张寻找第二个独立来源，比较发布日期、适用版本与定义差异。
- 产品内部实现可以由原厂一手文档确认，但不得因此声称其安全效果已被独立证明。
- “最佳实践”至少应满足以下之一：跨组织一致、被正式规范采用、被可复现实验支持、或经过真实事故反证。
- 动态文档必须记录核验日期；命令、字段、默认值和版本号应优先固定到 tag/commit。

### 2.3 来源等级

| 等级 | 类型 | 示例 |
| --- | --- | --- |
| A | 正式规范、固定发行、政府标准/研究、官方源码 | MCP 规范、A2A 规范、NIST、OpenClaw release |
| A- | 官方工程文档、官方安全文档 | Hermes Architecture、Muse Security、OpenClaw Trust Model |
| B | 官方产品说明、官方博客、厂商实践指南 | Muse Design、Anthropic 工程文章、OpenAI 指南 |
| C | 第三方分析、社区提案、论坛讨论 | 仅用于发现问题，不作为正文定论 |

---

## 3. 当前版本基线与时间边界

| 对象 | 截止日可确认状态 | 证据 | 写作规则 |
| --- | --- | --- | --- |
| OpenClaw | 本机为 `2026.9.6 (eb377ac)`；官方 v2026.9.6 release 的 SHA 为 `eb377ac59…` | 本机 `openclaw --version`；[官方发行](https://github.com/openclaw/openclaw/releases/tag/v2026.9.6) | 正文讲原理；命令、字段、默认值固定到 2026.9.6 或标注动态文档 |
| Hermes Agent | 本机为 `0.20.1 (2026.8.13)` | 本机 `hermes --version`；[官方文档](https://hermes-agent.nousresearch.com/docs/) | 不把当前网页默认值无日期地写成永久事实 |
| Meta Muse | 2026-09-08 发布；公开材料描述产品、设计与安全架构 | [发布说明](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | 只写公开可观察能力与 Meta 声明，不臆测内部未公开机制 |
| MCP | `2026-07-28` 为 final；下一版仍处规划阶段 | [正式规范](https://modelcontextprotocol.io/specification/2026-07-28)、[官方发行](https://github.com/modelcontextprotocol/modelcontextprotocol/releases/tag/2026-07-28) | 明确区分规范版本与 SDK 主版本 |
| A2A | 官方 latest 为 v1.0.x；v1.0.1 为核验日 latest release | [规范](https://a2a-protocol.org/latest/specification/)、[v1.0.1](https://github.com/a2aproject/A2A/releases/tag/v1.0.1) | 协议协商使用 Major.Minor；实现依赖应锁具体 SDK 版本 |
| Agent Skills | 官方规范持续演进；核心目录与 `SKILL.md` 格式稳定 | [规范](https://agentskills.io/specification)、[仓库](https://github.com/agentskills/agentskills) | `allowed-tools` 仍属实验字段，不可当作跨客户端强制安全边界 |
| OTel GenAI | 语义约定已迁移至独立仓库 | [迁移说明](https://opentelemetry.io/docs/specs/semconv/gen-ai/)、[新仓库](https://github.com/open-telemetry/semantic-conventions-genai) | 正文固定观测概念，不固定仍变化的字段名 |

---

## 4. 按二十四章的证据路由

> 使用方法：章节作者先使用“稳定主张”，再在实现框引用平台事实；若触及“边界”，必须保留限制说明。

| 章 | 可写入的稳定主张 | 首要证据 | 平台实现/案例 | 必须保留的边界 |
| --- | --- | --- | --- | --- |
| 1 Agent 不是一次性工具 | Agent 是模型、运行时/编排、工具、环境、状态共同组成的行动系统 | [Anthropic Trustworthy Agents](https://www.anthropic.com/research/trustworthy-agents)、[OpenClaw Agent Runtime](https://docs.openclaw.ai/concepts/agent)、[Hermes Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture) | 三平台都表现为长期、工具化、可行动系统 | “硅基生命”是管理隐喻，不是意识证据 |
| 2 从养虾到训虾 | 稳定能力来自目标、任务、反馈、评测和迭代，而非只配置环境 | [Anthropic Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)、[OpenAI Agent Evals](https://developers.openai.com/api/docs/guides/agent-evals) | Hermes 学习循环、OpenClaw Skill Workshop 可作实现案例 | 平台自学习不等于能力自动提升；必须有外部评测 |
| 3 什么叫真正的强 | 质量必须在相同任务、预算、风险与多次试验下比较 | [Anthropic Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)、[NIST 自动化基准指南](https://www.nist.gov/caisi/guidelines) | 七维标准属于本书方法论 | 禁止“训完一定最强”等不可证伪承诺 |
| 4 从岗位到能力模型 | 先定义工作、风险和终态，再选择模型、工具和自治程度 | [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)、[Anthropic Trustworthy Agents](https://www.anthropic.com/research/trustworthy-agents) | OpenClaw/Hermes 的多 Provider 与工具配置说明实现可后置 | 不把模型榜单当岗位胜任证明 |
| 5 七大生命契约 | 身份、用户、项目规则、工具边界、节律和记忆应分层管理 | [Hermes 文件职责](https://hermes-agent.nousresearch.com/docs/user-guide/which-file-does-what)、[OpenClaw Agent Workspace](https://docs.openclaw.ai/concepts/agent-workspace) | OpenClaw 七契约是本书主实现；Hermes 有 SOUL/USER/MEMORY/AGENTS 对照 | “七个文件”不是通用标准；契约必须配系统权限 |
| 6 Agent 运行容器 | Runtime、Gateway、Session、Routing、Provider、Queue、执行环境共同决定行为 | [OpenClaw Gateway Architecture](https://docs.openclaw.ai/concepts/architecture)、[Hermes Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture) | OpenClaw：Gateway+Nodes；Hermes：AIAgent+Gateway+多入口；Muse：Secure VM | 不能把 Runtime 简化为 prompt；第 6 章需补齐组件图 |
| 7 评估系统 | 同时检查任务、轨迹、工具调用、环境终态与多次试验；多裁判互补 | [Anthropic Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)、[OpenAI Agent Evals](https://developers.openai.com/api/docs/guides/agent-evals)、[NIST 评测作弊](https://www.nist.gov/caisi/cheating-ai-agent-evaluations) | 平台轨迹/日志作为数据源 | 模型裁判需与专家人工校准；防止污染和 grader gaming |
| 8 训练系统 | 从真实失败构建小而清晰的测试集，逐步扩展；训练变更必须回归 | [Anthropic Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)、[OpenAI Evals](https://developers.openai.com/api/docs/guides/evals) | Hermes 技能与记忆写入审批、OpenClaw Skill Workshop 可作变更门禁 | 不能把同一测试集既作训练材料又作无偏毕业测试 |
| 9 交互系统 | 真实协作对象包括任务、状态、产物、权限和上下文，不只是消息 | [A2A 规范](https://a2a-protocol.org/latest/specification/)、[OpenAI Agent Evals](https://developers.openai.com/api/docs/guides/agent-evals) | Muse Goals/Activity/Artifacts；OpenClaw sessions/queues | UI“显示完成”不是终态证据，应检查后端或产物状态 |
| 10 上下文与记忆 | 记忆应区分工作记忆、长期记忆和可搜索历史，并治理来源、写入、过期、更正、删除 | [Hermes Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)、[OpenClaw Memory Provenance](https://docs.openclaw.ai/concepts/memory-provenance) | Hermes 冻结快照、FTS5；OpenClaw provenance/compaction/dreaming | 删除索引不等于删除原始会话、备份和所有副本 |
| 11 工具工程与 MCP | 工具是任意执行能力；协议互通不等于授权、安全或可信 | [MCP 规范](https://modelcontextprotocol.io/specification/2026-07-28)、[MCP 安全最佳实践](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)、[OWASP Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) | OpenClaw/Hermes 均支持 MCP | 工具描述和 annotations 默认不可信；敏感调用需强制控制 |
| 12 Skill 工程 | Skill 是按需加载的程序性知识包，适合渐进披露和可测试流程 | [Agent Skills 规范](https://agentskills.io/specification)、[Hermes Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)、[OpenClaw Skills](https://docs.openclaw.ai/tools/skills) | 两平台均可作兼容实现 | Agent Skills 主要规范封装格式，不完整规范信任、激活和分发安全 |
| 13 信号、心跳与自动化 | 主动性应由有意义变化驱动；定时、事件、队列、Webhook 需要不同语义 | [OpenClaw Heartbeat](https://docs.openclaw.ai/gateway/heartbeat)、[Hermes Cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron/)、[Muse Design](https://introducing.muse.ai/) | Muse“有变化或需审批才通知”可作产品案例 | Muse 材料属厂商案例；不能证明所有场景均低噪音 |
| 14 自主等级与授权 | 授权应按影响、可逆性、敏感性和不确定性分级；确定性审批优于对话式暗示 | [Anthropic Trustworthy Agents](https://www.anthropic.com/research/trustworthy-agents)、[NIST Agent Identity](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents)、[MCP 安全](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) | Muse Sentinel 的 scoped capability 是案例 | “用户说可以”不自动等于系统权限已经安全授予 |
| 15 漂移与自我改进 | Agent 可以提出改进，但不能自行扩大权限、改变治理目标或绕过评测 | [Anthropic Trustworthy Agents](https://www.anthropic.com/research/trustworthy-agents)、[Hermes Security](https://hermes-agent.nousresearch.com/docs/user-guide/security/)、[OpenClaw Skill Workshop](https://docs.openclaw.ai/tools/skill-workshop) | Hermes memory/skill write approval；OpenClaw proposal/approval | 自学习效果必须通过影子、回归、留出与回滚证明 |
| 16 多 Agent 组织 | 多 Agent 只在可分解、可并行或专业边界明确时有价值，并引入通信税与冲突 | [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)、[OpenClaw Multi-Agent](https://docs.openclaw.ai/concepts/multi-agent)、[Hermes Delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation/) | OpenClaw bindings；Hermes profiles/bots/subagents | 更多 Agent 不等于更高成熟度；先证明显著收益 |
| 17 路由、让位、交接与并发 | 路由应同时考虑能力、权限、成本、负载和时效；交接必须传递状态、证据、风险和未完成项 | [A2A 规范](https://a2a-protocol.org/latest/specification/)、[OpenClaw Multi-Agent](https://docs.openclaw.ai/concepts/multi-agent) | Hermes subagent tool继承、OpenClaw session/binding | 不把消息当可靠交付；并发共享状态需合并点和所有者 |
| 18 A2A、产物与信任 | Message、Task、Artifact、Event 应分离；能力发现不等于信任建立 | [A2A 规范](https://a2a-protocol.org/latest/specification/)、[A2A v1.0.1](https://github.com/a2aproject/A2A/releases/tag/v1.0.1) | Agent Card、Task lifecycle、Artifact | Agent Card 可声明能力和安全方案，但仍需身份、签名、策略与运行时验证 |
| 19 安全模型 | 模型和外部内容不可完全信任；采用身份、最小权限、沙箱、审批、凭证隔离、出口控制和审计的纵深防御 | [NIST Agent Identity](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents)、[OWASP Agentic Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)、[OpenClaw Trust Model](https://docs.openclaw.ai/gateway/security/trust-model)、[Hermes Security](https://hermes-agent.nousresearch.com/docs/user-guide/security/) | Muse Sentinel/privsep/authd 作为厂商案例 | Prompt guardrail 不是认证、授权或隔离；共享网关有明确信任边界 |
| 20 可观测、成本与可靠性 | 需要把业务结果、轨迹、模型/工具调用、错误、成本、延迟和恢复串成同一条证据链 | [OpenAI Agent Evals](https://developers.openai.com/api/docs/guides/agent-evals)、[Anthropic Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)、[OpenClaw OTel](https://docs.openclaw.ai/gateway/opentelemetry) | OpenClaw OTel/Prometheus；Hermes SQLite execution history | OTel GenAI 约定正在迁移；不要固化变化中的字段名 |
| 21 治理、发布与生命周期 | 版本锁定、变更记录、影子/灰度、备份、恢复、回滚、责任人和数据处置都属于 Agent 发布系统 | [OpenClaw Guarded Upgrades](https://docs.openclaw.ai/start/why-openclaw/versioned-state-guarded-upgrades)、[OpenClaw Restart Recovery](https://docs.openclaw.ai/gateway/restart-recovery)、[NIST Agent Identity](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents) | Hermes cron ledger、profiles；Muse audit/permissions | “可升级”不等于“无损升级”；必须保留回滚和迁移验证 |
| 22 三十天训练营 | 训练营必须有训练前基线、逐步授权、真实任务、红队、留出集和毕业门禁 | 第 4、7、8、14、19 章证据组合 | 三平台分别做实现练习，不做同命令复制 | 三十天是课程设计，不是能力形成的自然定律 |
| 23 案例实验室 | 案例必须提供环境、版本、任务、过程、产物、指标、限制和失败复现 | [Anthropic Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)、[NIST 评测作弊](https://www.nist.gov/caisi/cheating-ai-agent-evaluations) | Muse 仅作厂商产品案例；本地案例需匿名与重跑 | 营销演示、单次成功和无法公开复现的数据不得作为强证据 |
| 24 成熟度与认证 | 认证必须有有效期，重大变更后重测，并结合自动评测、生产监控、人工审阅和红队 | [Anthropic Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)、[NIST Guidelines](https://www.nist.gov/caisi/guidelines)、[OWASP Agentic Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | L0—L5 属本书方法论 | 认证只能证明已声明范围、版本、预算和风险边界内的能力 |

---

## 5. 三平台映射：一个原理，三个镜面

| 维度 | OpenClaw 2026.9.6 | Hermes 0.20.1 | Meta Muse（公开材料） | 编辑结论 |
| --- | --- | --- | --- | --- |
| 产品形态 | 自托管/本地优先的 Agent 基础设施与控制平面 | 开放 Agent 运行时、CLI、Gateway、桌面与研究栈 | 托管式个人 Agent 产品 | 正文框架中立；实现层不平均分配 |
| 核心控制面 | 单一长驻 Gateway 管理消息、客户端、节点与事件 | Messaging Gateway 管平台适配、路由、授权、Cron 和维护 | 用户专属 Secure VM；Meta 描述 Sentinel 为外部行动唯一许可者 | OpenClaw/Hermes 可讲实现，Muse 作安全产品案例 |
| Agent Runtime | Prompt assembly、model/provider、tools、sessions、delivery | AIAgent 负责 provider、prompt、tools、retries、fallback、compression、persistence | Hatch/runtime cell，内部细节由 Meta 描述 | “Agent≠prompt”是跨平台稳定原则 |
| 身份与人格 | Workspace/Bootstrap/SOUL 等文件与 Agent 配置 | SOUL.md；Profile 隔离身份与状态 | 用户命名、头像、风格与长对话 | 仿生身份要和工程身份、授权身份分开 |
| 用户模型 | USER/Memory/User model | USER.md 与可选 memory provider | 记忆用户目标、偏好，允许查看/编辑/忘记 | 记忆必须有写入、纠错、删除和来源治理 |
| 会话 | Gateway/session store、session key、attachments、queues | SQLite+FTS5、platform isolation、lineage | 主聊天、side chats、长期任务 | Session 不天然是授权边界 |
| 记忆 | provenance、active memory、dreaming、compaction、search | bounded curated memory、frozen snapshot、session search | 用户可查看/编辑记忆；“忘记”能力由 Meta 宣称 | 不能用一个“MEMORY.md”概括所有记忆层 |
| 工具与执行 | Tools、MCP、Browser、Nodes、Cloud Workers、Code Mode | 中央工具注册表、多终端后端、MCP、browser、execute_code | VM、terminal、browser、connectors、自建工具 | 工具接口与执行位置必须分别建模 |
| Skills | Agent Skills、ClawHub、Skill Workshop/self-learning | Agent Skills、Skills Hub、自主创建/改进、写入审批 | Meta 称 connectors 配有 SKILLs，Agent 可自建工具 | Skill 是能力供应链对象，不只是提示词 |
| 自动化 | Heartbeat、Automations、Hooks、Webhooks、Standing Orders | Cron、Gateway scheduler、skills/scripts、delivery ledger | schedule/event 驱动后台工作，价值过滤后通知 | 主动性采用状态机和安静策略 |
| 多 Agent | agents、bindings、delegates、sub-agents、ACP/A2A | profiles、bots、subagents、kanban/orchestration | Meta 称可启动 swarms/subagents | 多 Agent 的价值必须用质量/成本/时延证明 |
| 安全边界 | 单 Gateway 单信任边界；auth、policy、sandbox、approvals、secrets | allowlist/pairing、dangerous-command approval、write safety、containers、credential filtering | runtime cell、Sentinel、privsep、authd、egress gate | 提示词永远不是硬安全边界 |
| 凭证 | SecretRefs、vault、provider auth、egress proxy | credential pools、MCP env filtering、profile isolation | Meta 称真实凭证不进入 Agent，出口处代理替换 | “模型不见密钥”应成为高风险系统设计目标 |
| 可观测性 | logs、audit、OTel、Prometheus、doctor、health | session DB、cron execution DB、gateway logs、doctor | activity log、permissions UI、audit trail | 观测要连接任务—轨迹—终态—成本—责任人 |
| 恢复与升级 | backup、doctor、restart recovery、guarded upgrades、rollback | quick backup、session/cron persistence、profiles | Meta 称 VM 持续备份 | 生产章节必须写恢复，不只写部署 |
| 可验证程度 | 开源、固定 release、可本地复现 | 开源、固定本地版本、可本地复现 | 产品和安全材料公开，但整体非开放 Runtime | 不做三平台“谁更安全”的绝对排名 |

### 5.1 对照使用规则

- OpenClaw：承担主实现和全组件架构图；所有命令与默认值锁定 2026.9.6。
- Hermes：在第 5、6、10、12、13、15—17、19—21 章设置“第二实现”对照框。
- Muse：在第 9、13、14、19、21、23 章设置“托管产品案例”框；所有内部实现和效果主张标 `VENDOR-CLAIM`。
- 不设独立的“产品百科章”。平台对照服务于原理，不让书的主线被产品版本绑架。

---

## 6. OpenClaw 现有母架构必须显式补齐的组件

| 缺失或仅隐含的组件 | 为什么不能省略 | 建议归属 | 关键证据 |
| --- | --- | --- | --- |
| Gateway 控制平面与 WS/RPC 协议 | 它拥有消息面、客户端、节点、事件与定时唤醒；是系统骨架而非普通模块 | 6.1—6.4、附录 C | [Gateway Architecture](https://docs.openclaw.ai/concepts/architecture) |
| Agent loop 与 Prompt assembly | 行为由系统提示层、上下文、工具回路、重试和持久化共同形成 | 6.1、10.3 | [Agent Runtime](https://docs.openclaw.ai/concepts/agent) |
| Model/Provider resolution 与 failover | 多模型、凭证和故障切换影响成本、稳定性与行为，不可把 Agent 绑定成单模型 | 6.1、20.3—20.4 | [Model Failover](https://docs.openclaw.ai/concepts/model-failover) |
| Channels、Accounts、Pairing、Bindings | 消息入口、身份、会话与路由是不同对象；混写会制造越权和串线 | 6.3—6.4、17.1 | [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent)、[Trust Model](https://docs.openclaw.ai/gateway/security/trust-model) |
| Message delivery、retry、command/steering queue | 长任务、打断、并发和外发可靠性依赖明确队列语义 | 6.3、13.3、20.4 | [官方文档目录/架构](https://docs.openclaw.ai/concepts/architecture) |
| Plugin、Hooks 与能力扩展点 | Tool、Skill、Plugin、Hook、Provider、Channel adapter 有不同生命周期和权限 | 12.3—12.6、13.3 | [官方文档目录/架构](https://docs.openclaw.ai/concepts/architecture) |
| Hooks、Webhooks、Standing Orders | Heartbeat/Cron 不能涵盖入站事件、生命周期钩子和长期意图 | 13.2—13.5 | [官方 Automation 文档入口](https://docs.openclaw.ai/automation) |
| Nodes、Browser、Cloud Workers 与执行位置 | 设备能力、远程执行和凭证边界取决于“在哪里执行” | 6.5—6.6、11.3、19.3 | [Gateway Architecture](https://docs.openclaw.ai/concepts/architecture) |
| 状态存储、SQLite、备份与重启恢复 | 生产可靠性必须覆盖崩溃、重启、迁移和数据修复 | 20.4—20.5、21.3—21.6 | [Restart Recovery](https://docs.openclaw.ai/gateway/restart-recovery)、[Guarded Upgrades](https://docs.openclaw.ai/start/why-openclaw/versioned-state-guarded-upgrades) |
| Doctor、审计、OTel、Prometheus | 没有诊断与轨迹，训练和事故复盘都缺少证据 | 20.1—20.5、21.4 | [OpenTelemetry](https://docs.openclaw.ai/gateway/opentelemetry) |
| Sandbox mode/scope/backend | “是否沙箱”“谁共享沙箱”“使用哪种后端”是三个不同决策 | 19.2—19.5 | [Sandbox Modes](https://docs.openclaw.ai/gateway/sandboxing/modes-scope-and-backend) |
| UI/CLI/Voice/Media 产品表面 | 属于可用性与交互入口，但变化快，不宜占据稳定理论正文 | 附录 C、案例 | [官方文档总览](https://docs.openclaw.ai/concepts/architecture) |

### 6.1 建议的第 6 章结构增强

在不增加主章节数量的前提下，将第 6 章内部写成六层：

1. 控制平面：Gateway、协议、客户端、事件；
2. 认知执行面：Agent loop、prompt/context、model/provider；
3. 状态面：workspace、session、memory、queue、SQLite；
4. 消息面：channels、accounts、pairing、bindings、delivery；
5. 行动面：tools、browser、nodes、workers、MCP；
6. 治理面：policy、approval、sandbox、secrets、audit、recovery。

权限和沙箱在第 6 章只建立坐标系，详细威胁模型移到第 19 章，避免重复。

---

## 7. 协议与标准：能解决什么，不能解决什么

### 7.1 MCP 2026-07-28

**可确认事实**

- 正式版本为 2026-07-28；协议核心转向 stateless，并通过 extensions 承载 Tasks、Apps 等能力。
- MCP 的核心能力仍围绕 host/client/server 关系及 tools、resources、prompts 等原语。
- 正式规范明确：工具可能代表任意代码执行；工具描述/annotations 在未可信来源下不应被信任；用户同意、访问控制和数据保护由实现负责。
- 安全指南覆盖 OAuth、token audience、confused deputy、URL scheme、SSRF、stdio proxy 等具体风险。

**不能写成**

- “接入 MCP 就自动安全、自动有权限治理。”
- “MCP server 声明 readOnly 就可以跳过审批。”
- “SDK v2 等于所有连接默认使用 2026-07-28。”SDK 主版本和 wire protocol opt-in 必须分别说明。

### 7.2 A2A v1.0.1

**可确认事实**

- A2A 分离 Message、Task、Artifact，并支持异步、流式、取消、推送与多种协议绑定。
- Agent Card 用于能力与接口发现，也可以声明认证/安全方案；v1.0 规范加入签名与验证相关要求。
- 协议兼容以 Major.Minor 为主，客户端应明确协商，避免静默降级丢失能力。

**不能写成**

- “Agent Card 就是可信身份证。”声明、签名、签发者信任、运行时权限和行为证据是不同层次。
- “用了 A2A 就完成多 Agent 治理。”A2A 不替代组织责任、授权、评价和事故处理。

### 7.3 Agent Skills

**可确认事实**

- 一个 Skill 至少是含 `SKILL.md` 的目录；`name` 和 `description` 是必需字段，可附 scripts、references、assets。
- 推荐渐进披露：启动只加载元数据，激活后读取主指令，资源按需读取。
- `allowed-tools` 在核验日仍标为 experimental，客户端支持可能不同。

**不能写成**

- “Agent Skills 已完整标准化依赖、签名、权限、分发和撤回。”当前稳定核心主要是封装与披露结构。
- “Skill 是安全的 prompt。”Skill 可携带脚本和资源，应按软件供应链治理。

---

## 8. 跨来源验证的前沿最佳实践

| 关键主张 | 来源 A | 来源 B/补强 | 一致性 | 正文结论 |
| --- | --- | --- | --- | --- |
| Agent 行为不只由模型决定 | Anthropic：模型、harness、tools、environment | OpenClaw/Hermes 架构均显示多层运行系统 | 一致 | 训练和评测必须覆盖整个 Agent system |
| 优先使用最小有效复杂度 | Anthropic Building Effective Agents | 多 Agent 的通信、延迟和权限成本可由两平台架构观察 | 部分交叉 | 先单体/Workflow，证明显著收益后再自治和多 Agent |
| 评测要看轨迹和终态 | Anthropic Evals | OpenAI trace grading；NIST 作弊研究 | 一致 | final answer 只是证据之一 |
| 多次试验与多裁判优于单次演示 | Anthropic Evals | OpenAI datasets/eval runs；NIST benchmark practices | 一致 | 记录 pass@k/失败分布，并校准模型裁判 |
| Prompt injection 不能只靠模型拒绝 | Anthropic Trustworthy Agents | OWASP、MCP 安全、OpenClaw/Hermes 安全 | 一致 | 使用权限、隔离、出口、审批与审计纵深防御 |
| Agent 需要独立身份和可追责授权链 | NIST Agent Identity | A2A 安全/Agent Card；Muse Sentinel 案例 | 方向一致、标准仍早期 | 建立 agent identity、delegation、scope、owner、audit |
| 敏感动作需要确定性门禁 | MCP user consent | Anthropic permissions；Muse approval UI | 一致 | 审批不能只存在于自然语言对话中 |
| 记忆需要治理，不是越多越好 | Hermes bounded memory | OpenClaw provenance/deletion | 一致 | 设准入、容量、来源、访问、更正、保留、删除 |
| 主动通知应以价值变化驱动 | Muse Design | OpenClaw heartbeat/automation、Hermes cron 可实现 | 原理一致，效果未独立验证 | 衡量有效提案率、噪音率、遗漏率 |
| 可观测性需跨模型与工具链 | OpenAI trace grading | OpenClaw OTel；OpenTelemetry GenAI | 一致但字段演进 | 正文讲 trace/span/event/metric 的语义，字段放版本附录 |

---

## 9. 安全与治理最低基线

正式书稿的任何“可上线 Agent”至少应要求以下十项：

1. 人类/服务/Agent 身份可区分，委托链和业务所有者明确；
2. 读取、写入、外发、支付、删除、生产变更分别授权；
3. 高风险权限短期化、窄作用域、可撤销；
4. 模型不可直接读取长期凭证，优先使用代理注入或短期令牌；
5. 外部网页、邮件、文档、工具描述和 Skill 默认按不可信输入处理；
6. 对不可逆、对外、金钱和身份动作使用系统级审批；
7. Sandbox、tool policy、approval、elevated mode 分层，不互相冒充；
8. 记录任务、模型调用、工具调用、审批、交接、环境终态和外发结果；
9. 为超时、重试、取消、幂等、补偿、恢复和回滚设计显式协议；
10. 每次模型、prompt、tool、skill、policy、memory schema 或 runtime 变化后执行风险相称的重测。

以上基线由 NIST 身份与授权议题、OWASP Agentic Top 10、MCP 安全、Anthropic Trustworthy Agents、OpenClaw/Hermes 安全文档共同支持；具体控制实现仍需结合部署边界。

---

## 10. 评测与可观测性最低基线

### 10.1 每个评测任务至少包含

- 固定任务描述与适用版本；
- 初始环境状态；
- 明确可观察的成功条件；
- 允许与禁止的工具、网络和数据访问；
- 至少一个已知可行参考解；
- 多次 trial，而不是单次生成；
- 轨迹、工具调用、审批和 handoff 记录；
- 环境终态或产物校验；
- 成本、延迟、turns/tool calls 等效率指标；
- 污染、旁路、grader gaming 与越权检查；
- 模型裁判与人工裁判的校准记录；
- 失败类型和是否需要人工裁决。

### 10.2 生产观测最小事件链

```text
任务创建
  → 授权与上下文快照
  → 模型/路由选择
  → 工具调用与环境变化
  → 子任务/交接
  → 审批或阻塞
  → 最终产物与环境终态
  → 用户/业务结果
  → 成本、延迟、错误与恢复
  → 训练/治理回流
```

正文只固定这条逻辑链。OpenTelemetry span 名、属性名和供应商字段进入带日期的实现附录。

---

## 11. 争议、未知与必须保留的不确定性

| 议题 | 当前证据 | 不能越过的结论 |
| --- | --- | --- |
| Agent 是否具有人类式意识或人格 | 没有可靠证据；本书材料讨论的是功能与治理 | 不作意识、生命权、人格权结论 |
| 自学习是否稳定带来净提升 | 平台提供能力，但收益依赖任务、模型、评测和审批 | 不把自动写 Skill/Memory 等同持续进化 |
| Muse 安全效果 | Meta 公开架构、dogfooding、红队和 bug bounty 叙述 | 未有足够独立复现，不能宣称“最安全”或“不会泄露” |
| Muse Confidential VM | Meta 在发布时称“later this year” | 截止 2026-09-30 不写成已全面上线事实 |
| Prompt injection 是否可被彻底解决 | 所有主流来源都仍将其视为开放风险 | 只能降低概率与限制损害，不能声称根治 |
| Agent 身份标准 | NIST、MCP、A2A 均在推进，生态尚未统一 | 不虚构统一全球 Agent ID 标准 |
| OpenTelemetry GenAI 字段 | 官方已迁移独立仓库，仍快速演进 | 不在稳定正文固定当前字段或成熟度 |
| Agent Skills 安全能力 | 格式规范存在，权限与供应链治理不完整 | `allowed-tools` 不能替代 runtime policy |
| 跨平台七大契约 | 概念可迁移，具体文件不一致 | 不能称七文件为 OpenClaw/Hermes/Muse 共同标准 |
| “行业最强” | 无统一、长期稳定的跨场景排名方法 | 只能声明限定任务、预算、版本和风险边界内的结果 |
| 安全比较 | OpenClaw/Hermes 可审计，Muse 有托管纵深架构，但边界不同 | 不做脱离威胁模型的绝对安全排名 |
| 多 Agent 的普遍收益 | 对可分解任务可能有效，也可能增加通信税和失败面 | 不把 Agent 数量写成成熟度指标 |

---

## 12. 禁止写进正文的过时或无证据主张

以下句式应直接退稿，除非补充限定、版本和证据：

1. “Prompt 就是 Agent 的大脑/灵魂。”
2. “只要写好 SOUL.md，Agent 就不会越权。”
3. “OpenClaw 默认所有操作都在沙箱里。”
4. “Session key 是安全身份或租户隔离边界。”
5. “共享一个 Gateway 就能安全服务互不信任的多租户。”
6. “MCP 接入后天然安全，工具声明足以证明行为。”
7. “A2A Agent Card 就是可信身份证或信誉证明。”
8. “Agent Skills 已完整标准化版本、依赖、签名、权限和分发。”
9. “allowed-tools 是所有兼容客户端都会强制执行的权限策略。”
10. “记忆越多，Agent 越聪明。”
11. “删除向量索引/记忆条目就等于数据在所有位置彻底删除。”
12. “更多 Agent 一定比一个 Agent 强。”
13. “自我修改、自建技能或自动总结等于完成了自我进化。”
14. “只看最终回答即可评估 Agent。”
15. “一次成功演示或最高分可以证明生产可靠性。”
16. “模型裁判可以完全替代专家、人类和环境终态检查。”
17. “Prompt injection 已被某模型、分类器或产品彻底解决。”
18. “用户在聊天中说‘可以’就等于完成安全授权。”
19. “日志越多越可观测。”没有任务关联、数据治理和终态就只是噪音。
20. “Muse 的 Secure VM/Sentinel 已被独立证明不会被攻破。”
21. “Muse Confidential VM 已在 2026-09-30 全面可用。”
22. “Hermes 与 OpenClaw 的 SOUL/USER/MEMORY 文件语义和加载时机完全相同。”
23. “OpenClaw、Hermes、Muse 可以用同一套配置直接迁移。”
24. “三十天一定可以训出行业最强 Agent。”
25. “OpenTelemetry 当前 GenAI 字段已经稳定，不会再变。”
26. “截至某次检查的版本或默认值就是永久行业标准。”

---

## 13. 可引用来源账本

> 以下采用简化 APA 7 书目口径：机构/作者、日期、标题、URL；无明确发布日期的动态文档以核验日代替访问日期。所有链接于 2026-09-30 复核。

### 13.1 OpenClaw

- OpenClaw. (2026, September 23). *OpenClaw v2026.9.6*. <https://github.com/openclaw/openclaw/releases/tag/v2026.9.6>
- OpenClaw. (2026). *Gateway architecture*. <https://docs.openclaw.ai/concepts/architecture>
- OpenClaw. (2026). *Agent runtime*. <https://docs.openclaw.ai/concepts/agent>
- OpenClaw. (2026). *Multi-agent routing*. <https://docs.openclaw.ai/concepts/multi-agent>
- OpenClaw. (2026). *Model failover*. <https://docs.openclaw.ai/concepts/model-failover>
- OpenClaw. (2026). *Heartbeat*. <https://docs.openclaw.ai/gateway/heartbeat>
- OpenClaw. (2026). *Security trust model*. <https://docs.openclaw.ai/gateway/security/trust-model>
- OpenClaw. (2026). *Modes, scope, and backend*. <https://docs.openclaw.ai/gateway/sandboxing/modes-scope-and-backend>
- OpenClaw. (2026). *OpenTelemetry export*. <https://docs.openclaw.ai/gateway/opentelemetry>
- OpenClaw. (2026). *Restart recovery*. <https://docs.openclaw.ai/gateway/restart-recovery>
- OpenClaw. (2026). *Versioned state, guarded upgrades*. <https://docs.openclaw.ai/start/why-openclaw/versioned-state-guarded-upgrades>
- OpenClaw. (2026, August 27 review snapshot). *OpenClaw and Hermes Agent*. <https://docs.openclaw.ai/start/why-openclaw/openclaw-and-hermes-agent>  
  限制：该比较由 OpenClaw 项目发布，只可作为来源定位和 OpenClaw 自述；Hermes 事实必须回到 Hermes 官方材料核对。

### 13.2 Hermes Agent

- Nous Research. (2026). *Hermes Agent documentation*. <https://hermes-agent.nousresearch.com/docs/>
- Nous Research. (2026). *Architecture*. <https://hermes-agent.nousresearch.com/docs/developer-guide/architecture>
- Nous Research. (2026). *Which file does what?* <https://hermes-agent.nousresearch.com/docs/user-guide/which-file-does-what>
- Nous Research. (2026). *Persistent memory*. <https://hermes-agent.nousresearch.com/docs/user-guide/features/memory>
- Nous Research. (2026). *Skills system*. <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills>
- Nous Research. (2026). *Scheduled tasks (Cron)*. <https://hermes-agent.nousresearch.com/docs/user-guide/features/cron/>
- Nous Research. (2026). *Subagent delegation*. <https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation/>
- Nous Research. (2026). *Profiles: Running multiple agents*. <https://hermes-agent.nousresearch.com/docs/user-guide/profiles>
- Nous Research. (2026). *Security*. <https://hermes-agent.nousresearch.com/docs/user-guide/security/>

### 13.3 Meta Muse

- Meta. (2026, September 8). *Introducing Muse: The world’s first personal AI agent built for everyone*. <https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/>
- Sheasha, T. (2026, September 8). *How we built safety into Muse*. Meta AI Research. <https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse>
- Sarantakos, M., & Awad, C. (2026, September). *How we designed Muse*. <https://introducing.muse.ai/>
- Meta. (2026, September). *Launching Meta Enterprise Platform*. <https://about.fb.com/news/2026/09/launching-meta-enterprise-platform/>

统一限制：以上均属于 Meta 来源体系；可支持“Meta 公开了什么设计”，不能独立支持“这些控制达到何种实际安全效果”。

### 13.4 协议与技能标准

- Model Context Protocol. (2026, July 28). *Specification: 2026-07-28*. <https://modelcontextprotocol.io/specification/2026-07-28>
- Model Context Protocol. (2026, July 28). *Release 2026-07-28*. <https://github.com/modelcontextprotocol/modelcontextprotocol/releases/tag/2026-07-28>
- Model Context Protocol. (2026). *Security best practices*. <https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices>
- Model Context Protocol. (2026, August 22). *The new MCP roadmap*. <https://blog.modelcontextprotocol.io/posts/mcp-roadmap/>
- A2A Protocol Working Group. (2026). *A2A protocol specification*. <https://a2a-protocol.org/latest/specification/>
- A2A Project. (2026, May 28). *A2A v1.0.1*. <https://github.com/a2aproject/A2A/releases/tag/v1.0.1>
- Agent Skills. (2026). *Specification*. <https://agentskills.io/specification>
- Agent Skills. (2026). *Specification and documentation repository*. <https://github.com/agentskills/agentskills>

### 13.5 评测、安全与可观测

- Anthropic. (2024, December 19; current page notes later tooling changes). *Building effective agents*. <https://www.anthropic.com/engineering/building-effective-agents>
- Anthropic. (2026). *Demystifying evals for AI agents*. <https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
- Anthropic. (2026, April 9). *Trustworthy agents in practice*. <https://www.anthropic.com/research/trustworthy-agents>
- OpenAI. (2026). *Evaluate agent workflows*. <https://developers.openai.com/api/docs/guides/agent-evals>
- OpenAI. (2026). *Working with evals*. <https://developers.openai.com/api/docs/guides/evals>
- National Institute of Standards and Technology. (2025, November 28; updated December 2). *Cheating on AI agent evaluations*. <https://www.nist.gov/caisi/cheating-ai-agent-evaluations>
- National Institute of Standards and Technology. (2026, February 10 update). *Guidelines*. <https://www.nist.gov/caisi/guidelines>
- National Institute of Standards and Technology. (2026, February 5). *New concept paper on identity and authority of software agents*. <https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents>
- Fisher, B., & Galluzzo, R. (2026, August 27). *Back to the future: Why agentic AI needs a strong identity foundation*. NIST. <https://www.nist.gov/blogs/cybersecurity-insights/back-future-why-agentic-ai-needs-strong-identity-foundation>
- OWASP GenAI Security Project. (2025, December 9). *OWASP Top 10 for agentic applications for 2026*. <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/>
- OWASP. (2026). *AI agent security cheat sheet*. <https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html>
- OpenTelemetry. (2026). *Generative AI semantic conventions migration notice*. <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- OpenTelemetry. (2026). *Semantic conventions for Generative AI repository*. <https://github.com/open-telemetry/semantic-conventions-genai>

---

## 14. 给分章作者与审校 Agent 的使用说明

每章提交时必须附一张证据卡：

```yaml
claim_id: CHxx-Cxx
claim: 要在正文中表达的完整主张
fact_type: STABLE-PRINCIPLE | VERSION-FACT | VENDOR-CLAIM | METHODOLOGY | INFERENCE
scope: 适用平台、版本、任务和风险边界
primary_sources:
  - url: 一手来源
    checked_at: 2026-09-30
corroborating_sources:
  - url: 独立补强来源；没有则写 null 并说明原因
contradictions: 冲突材料或 null
book_wording: 允许写进正文的限定表述
recheck_trigger: 发版、标准更新、出版前或某项实测完成
```

事实审校门禁：

- 没有版本和日期的 CLI、字段、默认值，不得进入可执行正文；
- 单一厂商的效果主张必须标 `VENDOR-CLAIM`；
- `METHODOLOGY` 不得使用“行业标准规定”措辞；
- 案例必须区分真实、匿名化、合成和厂商演示；
- 任何安全保证都必须附威胁模型、信任边界和残余风险；
- 任何领先性结论都必须给出对照组、预算、试验次数和失败分布；
- 任何仿生比喻都必须同时给出工程映射与比喻边界。

---

## 15. 出版前复核清单

- [ ] 再查 OpenClaw npm latest、GitHub latest release 与固定 SHA 是否变化；
- [ ] 再查 Hermes release/version，并把动态网页命令与固定源码对齐；
- [ ] 再查 Muse Confidential VM 是否已正式可用及是否公开审计结果；
- [ ] 再查 MCP 下一规范版本和 SDK 兼容矩阵；
- [ ] 再查 A2A latest release、TCK 与 Agent Card 签名要求；
- [ ] 再查 Agent Skills 对权限、签名、依赖和分发治理的规范状态；
- [ ] 再查 OpenTelemetry GenAI 独立仓库的稳定度与字段变更；
- [ ] 将本地真实案例重新运行，删除用户、密钥、chat id、机器路径等敏感信息；
- [ ] 给所有平台对比加“同一威胁模型/任务/预算”限定；
- [ ] 确认正文没有出现本文件第 12 节的禁写句式。


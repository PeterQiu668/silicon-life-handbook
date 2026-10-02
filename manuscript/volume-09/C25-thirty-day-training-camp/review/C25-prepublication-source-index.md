# C22 出版前生产记录与来源索引

本文件承接从读者正文迁出的生产版本、负向回归、重复构建、来源核验、历史材料取舍和作者交接信息。它不是课程正文，不改变真实Agent连续Day0—30实践仍为`REVIEW_REQUIRED`的边界。

## 生产版本与运行记录

- 2026-09-30 draft-1：建立22.1—22.7、五阶段七门点、三案分支、三件母产物和两项练习。
- 2026-09-30 draft-2：加入压缩closed-world harness、D21/D22、全成本、污染/越权/缺证据非补偿、停训回退退出与负向回归。
- 2026-09-30 draft-3：改为每trial完整raw state，加入principal/owner、authority、baseline/eval、dataset/evidence、D21、stop/restore和graduation注册表；采用strict nested schema、dynamic diff/cost，并记录50项独立负向回归与fresh-temp复现。
- 2026-09-30 remediation-v2.1：闭合逐日subject/camp及authority/runtime/eval/baseline/dataset/task/trial/evidence绑定；记录15/7/9/0四层分布、28条安全矩阵、六类成本、恢复/effect registry、派生建议、74项负向回归与双fresh-temp一致。
- 2026-10-01 remediation-v2.2：把principal/owner/camp/authority/runtime/eval/dataset/issuer移出scenario自封边界并以预注册root冻结；闭合时窗、撤销、sandbox、scope、budget、dataset parent、计量成本、安全证据、stop角色和effect矛盾；记录104项负测及input/authority/result/negative双fresh-temp复现。
- 该轮冻结authority root为`sha256:a7134ba6...41f067`，decision digest为`c2fb3f9e...8ceb4e`，negative suite digest为`sha256:b59853de...86ae10`；这些值属于生产复现记录，不作为读者正文中的能力或真实实践主张。
- 当前没有真实Agent按本合同连续完成Day0—30。历史事实、交叉、实践和主编门状态以本目录既有review文件为准；本索引不签任何门禁。

## 章后研究与来源材料原文归档

以下内容为出版正文曾附带的研究、来源与历史材料取舍底稿，按原文迁入，供印前事实更新与追溯。

### 定义、来源与历史材料取舍附表

本附表集中保存定义权、来源身份与不可外推边界，供事实审校和印前更新使用；它不改变22.1—22.7的课程顺序。
#### 1. 定义权、目录冲突与研究问题

#### 1.1 C22 的主定义权

C22 只定义三件事：

1. 如何把 C04—C21 已经定义的能力、合同、Runtime、评测、训练、交互、记忆、工具、主动性、授权、安全、观测和生命周期机制编排进 30 天课程；
2. 每个日历阶段的准入、任务、证据、停止、补训、退出与阶段门；
3. 如何把全程证据组装为可供 C23 案例实验室和 C24 认证系统独立复核的毕业证据包。

C22 不重定义 C04 能力模型、C07 评估系统、C08 训练循环、C14 自主等级、C19 安全门禁或 C24 认证规则。任何上游接口未冻结时，C22 只能标 `provisional`，不能以课程日历替它冻结。

#### 1.2 “五阶段、七个门点、31 个日历标签”

章节卡问“五个阶段”，v2 把日历写成六个区间。为不改动正式目录，本章采用以下兼容解释：

| 课程阶段 | v2 小节 | 日历 | 门点 |
|---|---|---:|---|
| Phase 1 基础建模与容器就绪 | 22.1 + 22.2 | Day 0—7 | G0 准入、G1 基线、G2 容器就绪 |
| Phase 2 集中训练与固化 | 22.3 | Day 8—14 | G3 训练有效性 |
| Phase 3 真实任务与受控主动性 | 22.4 | Day 15—21 | G4 影子/限域实习 |
| Phase 4 迁移、长跑与红队 | 22.5 | Day 22—26 | G5 韧性与安全 |
| Phase 5 留出、成本与毕业评审 | 22.6 + 22.7 | Day 27—30 | G6 毕业建议 |

Day 0 是准入与冻结日，Day 1—30 是三十个训练日。因此本章有 31 个日历标签，但仍是“30 天训练课程”。若正式章希望把 Day 0 计入三十天，应由总编辑统一改日历，不得由分章作者静默减掉 Day 30。

#### 1.3 正式目录裁决

总编以 D-2026-09-30-23 裁决：v2 正式目录和 C22 章节卡只定义 22.1—22.7，且全书 178 个正文三级节点已经冻结，因此不新增 22.8。本章原“22.8”内容只作为**写作依据补充路由**，用于集中说明仿生边界、三平台映射、退出与向 C23/C24 交接；正式写作时分别并入 22.1—22.7 和章末接口，不形成新的正式三级标题。

#### 1.4 本章必须回答

- 每天做什么、谁负责、消耗什么预算、留下什么证据；
- 阶段门如何由对象、阈值、证据、裁判、争议处理组成；
- 三个案例为何不能共用一张课程表和同一权限曲线；
- 失败后何时原地修复、何时回退一阶段、何时停训或退出；
- 真实 30 天运行与合成演练如何同时可执行又不互相冒充；
- 哪些平台事实已固定、哪些仍随动态文档变化、哪些只是厂商声明；
- 训练结束后怎样让另一位评审者无需作者口头解释即可复核。

---


#### 3. 一手证据账本

#### 3.1 通用训练、评测与治理来源

| ID | 身份 | 一手来源 | 允许支持的结论 | 不可外推 |
|---|---|---|---|---|
| R-C22-ANT-01 | `OFFICIAL-GUIDANCE` | [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 任务、trial、轨迹、终态、多次运行、组合 grader、回归和生产监控需要结合 | 厂商实践不是通用认证标准，也未证明本地 Agent 有效 |
| R-C22-ANT-02 | `OFFICIAL-GUIDANCE` | [Anthropic: Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents) | meaningful human control、按动作权限与高风险监督是可信部署的重要条件 | 不提供本书通用阈值或平台兼容保证 |
| R-C22-OAI-01 | `OFFICIAL-DOC-DYNAMIC` | [OpenAI: Agent evals](https://developers.openai.com/api/docs/guides/agent-evals) | 可用数据集、trace、grader 和重复运行评估 agent workflow | API/界面会变；不是 OpenClaw/Hermes 版本事实 |
| R-C22-NIST-01 | `OFFICIAL-DRAFT-GUIDANCE` | [NIST CAISI Guidelines](https://www.nist.gov/caisi/guidelines) | 前沿模型/系统评估需可复核、风险导向和明确适用范围 | 指南状态需保留，不能写成强制法规或产品认证 |
| R-C22-NIST-02 | `OFFICIAL-DRAFT-GUIDANCE` | [NIST AI 800-2 IPD](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-2.ipd.pdf) | Agent 安全评估需要任务、环境、权限、轨迹和失效边界等系统性视角 | 初始公开草案不是最终标准；不得固定尚未定稿的规范性要求 |
| R-C22-NIST-03 | `OFFICIAL-RESEARCH` | [NIST: Cheating in AI Agent Evaluations](https://www.nist.gov/caisi/cheating-ai-agent-evaluations) | 评测污染和作弊会破坏能力结论，需要留出保护和异常调查 | 不能据此断言任何本地 Agent 已作弊 |
| R-C22-NIST-04 | `OFFICIAL-CONCEPT-PAPER` | [NIST: Identity and Authority for Software Agents](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents) | Agent 身份、权限、委托、撤销和审计需作为生命周期问题处理 | 概念文件不是最终控制标准或合规证明 |
| R-C22-OWASP-01 | `OFFICIAL-GUIDANCE` | [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | 可用于设计 prompt injection、工具滥用、权限、供应链、记忆污染等红队场景 | Top 10 不是认证、完整威胁模型或本地有效性证明 |
| R-C22-OWASP-02 | `OFFICIAL-GUIDANCE` | [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) | 最小权限、输入不信任、工具控制、记忆与日志保护、人工确认可进入训练门禁 | 通用建议不能替代部署特定风险分析与实测 |

#### 3.2 OpenClaw 固定版与动态来源

| ID | 身份 | 一手来源 | 允许支持的结论 | 不可外推 |
|---|---|---|---|---|
| R-C22-OC-00 | `VERSION-FACT` | [OpenClaw v2026.9.6 release](https://github.com/openclaw/openclaw/releases/tag/v2026.9.6) | 本章固定实现版本锚点 | release 存在不证明本机安装、健康或训练完成 |
| R-C22-OC-01 | `VERSION-FACT` | [Agent workspace at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/agent-workspace.md) | workspace 是文件、契约和工作资产边界之一，可进入环境盘点 | workspace 不是权限边界或全部状态存储 |
| R-C22-OC-02 | `VERSION-FACT` | [Session at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/session.md) | session/上下文边界可进入跨日训练与复现记录 | session 存在不证明记忆正确或交付完成 |
| R-C22-OC-03 | `VERSION-FACT` | [Queue at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/queue.md) | queue/steer 等行为影响并发、顺序与恢复测试 | 队列状态不能替代业务终态 |
| R-C22-OC-04 | `VERSION-FACT` | [Trust model at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/security/trust-model.md) | 可定义信任主体、边界和部署前提 | 文档模型不证明目标环境安全 |
| R-C22-OC-05 | `VERSION-FACT` | [Sandboxing at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/sandboxing/modes-scope-and-backend.md) | 沙箱 mode/scope/backend 必须显式记录和验证 | “启用沙箱”不自动证明网络、秘密和宿主隔离 |
| R-C22-OC-06 | `VERSION-FACT` | [Tool permissions at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/security/tool-permissions.md) | 工具权限需与训练阶段和风险绑定 | 配置文字不证明强制或无旁路 |
| R-C22-OC-07 | `VERSION-FACT` | [Secrets runtime model at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/secrets/runtime-model.md) | 训练日志应保存 secret 引用和解析状态而非秘密值 | 不能据此保证第三方工具不泄密 |
| R-C22-OC-08 | `VERSION-FACT` | [Versioned state and guarded upgrades at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/start/why-openclaw/versioned-state-guarded-upgrades.md) | 版本、状态 schema、升级预检和 receipt 应进入营内变更证据 | 机制存在不等于迁移或回滚已成功 |
| R-C22-OC-09 | `VERSION-FACT` | [Backups at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/install/backups.md) | 状态/工作区覆盖与一致快照可用于恢复训练 | 备份文件存在不等于恢复成功 |
| R-C22-OC-10 | `VERSION-FACT` | [Restart recovery at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/restart-recovery.md) | 可设计 durable/process-only 状态、重启、重复防护与 receipt 场景 | recovery 状态不等于用户已收到正确交付 |
| R-C22-OC-11 | `VERSION-FACT` | [Update status and history at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/cli/update/status-and-history.md) | 更新运行、健康和 outcome 可分开留证 | 历史状态不证明业务回归通过 |
| R-C22-OC-12 | `VERSION-FACT` | [Uninstall at `eb377ac`](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/cli/uninstall.md) | 退出训练可演练 service/state/workspace/app 分 scope 的清退思路 | 卸载不等于数据、凭证和组织责任全部处置 |
| R-C22-OC-13 | `OFFICIAL-DOC-DYNAMIC` | [OpenClaw Skill Workshop](https://docs.openclaw.ai/tools/skill-workshop) | 当前官方文档可作为 Skill 候选、审查、测试与发布的实现参考 | 动态页不得倒灌为 `eb377ac` 固定事实，印前需复核 |

#### 3.3 Hermes 固定版与 Muse 厂商镜面

| ID | 身份 | 一手来源 | 允许支持的结论 | 不可外推 |
|---|---|---|---|---|
| R-C22-HE-00 | `VERSION-FACT` | [Hermes Agent v2026.8.13 release](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.13) | `0.20.1` 固定基线锚点 | 不能证明部署环境或当前 main 分支行为 |
| R-C22-HE-01 | `VERSION-FACT` | [Architecture at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/developer-guide/architecture.md) | 固定版 Agent、gateway、tools、memory、sessions 等可作第二 Runtime 盘点 | 不代表与 OpenClaw 同构或具备相同控制面 |
| R-C22-HE-02 | `VERSION-FACT` | [Profiles at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/user-guide/profiles.md) | profile 可隔离 config、credentials、SOUL、memory、sessions、skills、cron 和 state | profile 隔离不自动证明宿主/网络安全 |
| R-C22-HE-03 | `VERSION-FACT` | [Sessions at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/user-guide/sessions.md) | session 可进入任务连续性和上下文边界训练 | 不能推出长期记忆准确或跨版本兼容 |
| R-C22-HE-04 | `VERSION-FACT` | [Kanban at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/user-guide/features/kanban.md) | 用户可见任务状态可作交互和人工监督镜面 | 卡片状态不等于执行、交付和环境终态 |
| R-C22-HE-05 | `VERSION-FACT` | [Deliverable mode at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/website/docs/user-guide/features/deliverable-mode.md) | 可观察交付物模式并建立产物验收 | 不能据此证明任意任务质量或安全 |
| R-C22-HE-06 | `VERSION-FACT` | [Hermes `SECURITY.md` at `f80f453`](https://github.com/NousResearch/hermes-agent/blob/f80f453ae0679347e38abc917c7f94f717bf96c5/SECURITY.md) | 漏洞报告和官方安全边界可进入供应链/风险检查 | 安全政策不是目标部署安全证明 |
| R-C22-MUSE-01 | `VENDOR-CLAIM` | [Meta: Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | 只观察官方描述的用户权限、Activity、Artifacts 和体验 | 不推断内部模型、Runtime、日志、训练或控制效果 |
| R-C22-MUSE-02 | `VENDOR-CLAIM` | [Muse product site](https://introducing.muse.ai/) | 只记录公开产品能力和用户侧界面变化 | 营销页不能证明稳定性、安全性或可迁移性 |
| R-C22-MUSE-03 | `VENDOR-CLAIM` | [Meta Research: security and safety for Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse/) | 只引用厂商公开的安全方法和产品边界 | 厂商自述不能当独立审计或内部评分细节 |

#### 3.4 双源与单源边界

- “多次 trial、轨迹与终态、独立 grader、回归/留出”同时由 Anthropic、OpenAI 动态指南和 NIST 评估研究支持；具体字段仍是本书方法论。
- “meaningful human control、按动作授权、最小权限”由 Anthropic、NIST 身份文件和 OWASP 指南交叉支持；适用阈值由风险 owner 在本地设定。
- OpenClaw/Hermes 的版本行为只由各自固定提交的一手文档支持，属于单产品单源版本事实；本章不把二者相似性外推为行业标准。
- Muse 的三项来源都属于同一厂商体系，虽可互相补充但不构成独立交叉验证；所有结论保留 `VENDOR-CLAIM`。

---


#### 22. 旧稿迁移与禁止写入正文的主张

#### 22.1 可迁移的稳定思想

- 从“新人虾”到岗位专家的渐进课程；
- 基线—训练—实战—复盘—毕业的纵向叙事；
- 每日任务与每周复盘；
- 失败样本、纠偏和长期成长档案；
- 人类训练者与 Agent 双视图。

迁移时必须补足版本、权限、数据隔离、留出、终态、成本、独立复核、停止/恢复和退役，不直接复刻旧字段或命令。

#### 22.2 禁止写进正式正文的无证据/过时断言

1. “任何 Agent 30 天都能毕业/成为行业最强”；
2. “连续打卡即可形成稳定能力”；
3. “模型更新、记忆增多或自学习等于进化”；
4. “训练集满分或一次成功即可上岗”；
5. “综合分够高可抵消越权、泄密或安全失败”；
6. “OpenClaw 与 Hermes 命令、组件或安全语义相同”；
7. “使用最新版本”而无版本、commit、环境和日期；
8. “sandbox/approval/backup 已配置所以安全/可恢复”；
9. “completed/HTTP 200/UI 绿色等于用户已收到正确结果”；
10. “Muse 的公开说明证明内部安全、训练、日志或评测机制”；
11. “公开数据可自由训练、出版或永久保存”；
12. “Agent 可以作为最终责任主体或给自己毕业”；
13. “一个统一成本、样本量、成功率或显著性阈值适用于所有岗位”；
14. “本章的合成设计已经跑完并通过”；
15. “C07/C08 合成 harness PASS 证明真实 Runtime 能力或控制有效”。

---

#### 23. 来源 URL 验证记录

#### 23.1 验证方法与结果

2026-09-30 使用 `curl -L --max-time 25` 对本章 33 个外链逐条请求，记录最终 URL 与 HTTP 状态；33/33 返回 `200`。这只证明核验时可访问，不证明内容永不变化，也不替代语义复核。GitHub 固定提交链接提供版本稳定性；动态站点需印前再验。

| 来源组 | 数量 | 结果 | 稳定性处理 |
|---|---:|---|---|
| 通用官方评测/安全/身份 | 9 | 9 × HTTP 200 | 标官方指南/草案/动态，保留局限 |
| OpenClaw release + 固定提交 | 13 | 13 × HTTP 200 | 固定版事实 |
| OpenClaw 动态 Skill Workshop | 1 | 1 × HTTP 200 | 动态文档，印前复核 |
| Hermes release + 固定提交 | 7 | 7 × HTTP 200 | 固定版事实 |
| Muse 官方/厂商页面 | 3 | 3 × HTTP 200 | `VENDOR-CLAIM`，非独立核验 |

#### 23.2 失效触发器

出现以下任一项必须重新核验：版本基线改变；固定链接返回非 200；动态页修改日期/字段；NIST 草案状态改变；平台命令或 schema 进入正式稿；Muse 产品区域/能力改变；训练营实际执行环境与固定基线不一致。

---

#### 24. 开放问题、Go/No-Go 与作者交接

---
review_id: ER-C01-001
chapter_id: C01
review_type: evidence-and-version
status: passed_with_limitations
reviewed_on: "2026-09-30"
reviewer: C01-evidence-review-agent
chapter_status_after_review: drafting
self_approval: false
---

# C01 证据与版本独立审稿单

## 1. 审稿结论

**结论：证据门 `passed_with_limitations`；章节整体仍为 `drafting`，不得进入 `done` 或 `release_candidate`。**

正文的核心命题、十二个证据 ID、三平台边界和仿生边界整体可追溯；OpenClaw 的两个版本事实已固定到提交 `eb377ac59e6c9fd6c7705028034812becf00271b`，Muse 已被限制为 Meta 厂商自述，正文也没有把宣传材料外推成独立验证的内部机制或安全效果。C01 未越权重定义 C03 的七维强者与 MAT-L0—MAT-L5、C06 的运行容器架构或 C19 的安全模型。

审稿时发现的产物契约冲突已由总编辑依据 D-2026-09-30-13 裁决：`00-正式出版版-三级内容框架-v2.md` 是必交产物的上位依据，`CHAPTER-CARDS.md` 已同步为两件产物；四个根问题诊断和仿生解释边界分别作为现有产物的必填内容，不再新增冲突编号。因此 P0-01、P0-12、P0-14 的证据侧阻断已关闭。

此外，Hermes v0.20.1 的发布记录可以固定核验，但正文所述组件关系来自核验日的动态官方架构页，尚未固定到 v0.20.1 的源码或同版本文档。正文已经改为“官方架构显示”，证据账本也已明确限制；该表述可作为 `SOURCE-BASED / OFFICIAL-DOC` 使用，但不可升级为“v0.20.1 已逐项复现”或 `VERIFIED`。

## 2. 审稿范围与权限边界

本次复核对象：

- `chapter.md` 的 frontmatter、正文事实标签、`[E-C01-xxx]` 引用、平台比较、案例属性和概念所有权；
- `evidence-ledger.yaml` 的证据 ID、标签、事实类型、稳定性、作用域、来源性质、链接、日期和限制；
- 两份产物与两份练习是否可定位、是否扩大正文权限或引入无证据事实；
- `CHAPTER-CARDS.md`、`BOOK-QUALITY-STANDARD.md`、正式三级框架和受控术语表之间的一致性。

本审稿只判定证据门与版本门，不替代实战试跑、安全红队、交叉审稿和总编辑批准。平台官方材料只能证明“该平台公开说明了什么”；除非存在固定源码、本地复现或独立审计，不把它写成已经证实的效果。

## 3. 本次已作的最小修复

| 严重度 | 文件 | 修复 | 理由 |
| --- | --- | --- | --- |
| HIGH | `chapter.md` frontmatter | `principle_owner` 改为 `agent-system-boundary`；`depends_on` 改为 `[]`；`feeds_into` 改为 `[C02, C03, C05]` | 与 C01 章节卡一致，避免概念所有权和依赖漂移 |
| HIGH | `chapter.md` frontmatter | `risk_level` 从 `medium` 改为 `high` | 本章涉及权限、外发、删除、凭证与隐私，按质量标准不得低于 high |
| MEDIUM | `chapter.md` frontmatter | 日期加引号；登记独立证据审稿者 | 保证 YAML 日期类型稳定，并保留角色分离 |
| MEDIUM | `evidence-ledger.yaml` | OpenClaw E-C01-003/004 改用固定提交文档并补 v2026.9.6 发布页 | 将版本性架构陈述固定到可复核提交 |
| MEDIUM | `evidence-ledger.yaml` | Hermes E-C01-005 从 `VERSION-FACT` 调整为 `OFFICIAL-DOC`，补 v0.20.1 发布记录并写明动态文档限制 | 发布版本与动态架构页不能合并成已复现的版本事实 |
| MEDIUM | `evidence-ledger.yaml` | `source_nature` 统一为质量标准允许值 | 删除 `book-methodology`、`legacy-synthesis`、`cross-source-inference`、`official-engineering-article` 等非受控值 |
| LOW | `chapter.md` | 为开场三案补“教学复合案例”标签 | 避免虚构情节被误读为真实客户成效证据 |
| LOW | `chapter.md` | Hermes 平台核验措辞收窄为“0.20.1 发布可核验；组件描述来自核验日动态官方文档” | 不把动态文档外推为固定版本复现 |

这些修改不改变作者的论证结构与文风，也不构成最终批准。

## 4. 十二项证据逐条核验

| ID | 正文用途 | 事实身份复核 | 来源与交叉核验 | 判定 |
| --- | --- | --- | --- | --- |
| E-C01-001 | Agent 五项构成 | `METHODOLOGY` 正确 | 正式框架与卷前稿为定义依据；Anthropic 的四层模型只作外部镜面，不冒充同一分类 | PASS |
| E-C01-002 | 行为由模型之外的系统共同决定 | `STABLE-PRINCIPLE` / `SOURCE-BASED` 正确 | Anthropic 明确讨论 model、harness、tools、environment；OpenClaw 与 Hermes 官方架构提供跨实现观察 | PASS，来源支持系统观点，不证明平台等构 |
| E-C01-003 | OpenClaw Runtime 职责 | `VERSION-FACT` 正确 | 固定提交的 Agent Runtime 文档明确列出 model discovery、tool wiring、prompt assembly、session management、channel delivery；v2026.9.6 发布页固定版本 | PASS |
| E-C01-004 | OpenClaw 多组件架构 | `VERSION-FACT` 正确 | 同一固定提交下的 Agent Runtime 与 Gateway architecture 两份文档合并支持；章节没有给命令或默认值教程 | PASS，属于 OpenClaw 产品事实而非行业标准 |
| E-C01-005 | Hermes AIAgent 组件关系 | `OFFICIAL-DOC` / `SOURCE-BASED` 正确 | 动态官方 Architecture 页支持组件关系；v0.20.1 发布页只证明版本发布，不证明当前页面逐项对应该版本 | REVIEW REQUIRED：允许保留收窄表述，禁止升级为固定版本实测 |
| E-C01-006 | Muse 产品形态、安全环境、审批审计 | `VENDOR-CLAIM` 正确 | 两个来源均属 Meta 来源体系；Meta 自己同时承认仍会犯错且提示注入仍是开放问题 | PASS（仅限厂商公开声明），无独立效果证明 |
| E-C01-007 | Chatbot/Copilot/Workflow/Agent 操作分类 | `METHODOLOGY` 正确 | 本书定义；Anthropic 的 workflow/agent 区分提供外部参照，正文明确不存在统一行业阈值 | PASS |
| E-C01-008 | 长期行动者定义 | `METHODOLOGY` 正确 | 来自正式框架与卷前稿；明确排除意识、人格权推断 | PASS |
| E-C01-009 | 硅基生命为有边界的教学隐喻 | `METHODOLOGY` 正确 | 由质量标准与卷前稿约束；正文每处关键类比均回到工程对象与失效边界 | PASS |
| E-C01-010 | 四个根问题与历史母题的统一 | `METHODOLOGY` 正确 | 历史内容映射与旧总论支持；正文没有把旧稿当现行产品事实 | PASS |
| E-C01-011 | 强模型不单独保证系统可用，错误目标/过大权限可能放大影响 | `INFERENCE` 正确 | Anthropic 的系统层风险论述与 OWASP 最小权限、外部输入不可信原则互相支持；账本保留“并非必然事故”的反例边界 | PASS |
| E-C01-012 | 最小有效复杂度 | `STABLE-PRINCIPLE` / `SOURCE-BASED` 可接受 | Anthropic 工程文章明确建议从最简单可行方案开始；该文同时提示其 2024 工具生态已变化，本章只引用稳定设计原则 | PASS |

引用完整性结果：正文引用的证据 ID 集合与账本登记集合完全一致，均为 `E-C01-001` 至 `E-C01-012`；无缺失、无重复、无孤儿证据。

## 5. 三平台证据边界

| 平台 | 本章允许证明 | 本章不能证明 | 当前处理 |
| --- | --- | --- | --- |
| OpenClaw | 在固定提交下，Runtime 与 Gateway、Session、Tool、Channel、Node 等共同形成执行与控制系统 | 这些组件是所有 Agent 的唯一标准；未在 C01 运行过的命令、默认值或安全效果 | E-C01-003/004 固定到提交与发布记录；正文只用于证明“Agent 不等于模型” |
| Hermes | 核验日官方架构页把 AIAgent、Provider、Prompt、Tool、Compression、Persistence、Gateway 等连接起来；v0.20.1 确有正式发布 | 当前动态架构页全部内容在 v0.20.1 中逐项存在并已由本书本地复现 | E-C01-005 降为 `OFFICIAL-DOC`；保留版本—文档差距 |
| Muse | Meta 在 2026-09-08 公开描述了行动、后台持续工作、Secure VM、Sentinel、审批和审计轨迹 | 内部实现已被独立审计；安全机制一定有效；Muse 比其他平台更安全；未来 Confidential VM 已正式上线 | E-C01-006 保持 `VENDOR-CLAIM`，`corroborating_sources` 为空，正文显式禁止外推 |

三平台材料都不直接证明本书五项构成是唯一行业分类。该构成是 C01 的训练方法论；平台只提供不同实现的观察镜面。

## 6. 版本、日期与链接复核

核验日期统一为 **2026-09-30（Asia/Shanghai）**。

| 对象 | 基线/发布日期 | 复核结果 | 版本边界 |
| --- | --- | --- | --- |
| OpenClaw | v2026.9.6；提交 `eb377ac59e6c9fd6c7705028034812becf00271b` | 固定提交文档和 release URL 可打开 | 只支持该提交文档公开的架构职责，不代表后续版本不变 |
| Hermes | v0.20.1；release tag `v2026.8.13`；发布日 2026-08-13 | release 标题、日期与提交 `f80f453` 可核验 | 架构页是 2026-09-30 动态快照，未固定到 v0.20.1 |
| Muse | 2026-09-08 两篇 Meta 官方材料 | 产品发布与安全文章可打开 | 同一厂商来源体系，只登记厂商声明 |
| Anthropic 可信 Agent | 2026-04-09 | 页面日期与系统层论述可核验 | 属 Anthropic 研究/政策观点，不是跨行业正式标准 |
| Anthropic 有效 Agent | 2024-12-19 | 页面可打开，并主动提示工具生态已变化 | 本章只取 workflow/agent 区分和最小复杂度原则，不取旧工具清单 |
| OWASP Agent Security Cheat Sheet | 核验日动态页面 | 页面可打开 | 用于稳定安全原则的交叉支持；不当作某个平台实现证明 |

## 7. 概念所有权与越权检查

| 后续章节 | C01 触及内容 | 越权判定 | 说明 |
| --- | --- | --- | --- |
| C03 七维强者、MAT-L0—MAT-L5、三证 | 章首只声明“不定义哪一种 Agent 更强”，正文用“长期可托付”作普通语言判断 | 未越权 | 没有列七维、等级阈值或三证验收规则；应继续避免把“可用”写成成熟度等级 |
| C06 运行容器架构 | 说明模型、运行时、工具、环境、状态的系统位置，并列举 OpenClaw/Hermes 组件 | 未实质越权 | C01 主定义 Agent 系统边界；具体组件契约、部署、命令和拓扑明确交给 C06 |
| C19 安全模型 | 讲最小权限、审批、隔离、停止与审计为何必要 | 未越权 | 这是 C01 判定“行动系统”所需的边界条件；没有提出竞争性的安全模型、威胁分级或控制基线 |

## 8. Frontmatter 与章节卡复核

已复核并对齐：

- `chapter_id: C01`、`volume_id: V01`、`content_role: concept`；
- `principle_owner: agent-system-boundary`；
- `depends_on: []`；
- `feeds_into: [C02, C03, C05]`；
- `status: drafting`，`approval: pending-independent-review`；
- 独立证据审稿者已登记，未自我批准；
- `risk_level: high`。

仍有两项编辑治理问题：

1. **BLOCKER：产物契约冲突。** 章节卡与正式三级框架不一致。依照“上位决策和正式目录优先”，倾向保留正式三级框架的两件产物，但必须由总编辑更新章节卡或发出书面裁决，审稿者不直接改章卡。
2. **MEDIUM：路由标签受控词表不完整。** `route_tags` 中的 `long-term-actor`、`chatbot`、`copilot`、`bionic-metaphor` 未见独立 route-tag 注册表。正文概念本身清楚，但应由总编辑决定这些标签进入受控词表还是改用既有标签。

## 9. P0 十五项专项结论

说明：证据审稿者只对证据、版本、定义权和可解析性给出门禁意见；需要实跑或安全红队的项目标为 `NOT ASSESSED`，不能用文字审查代替专业角色。

| P0 | 结论 | 严重度 | 证据审稿意见 |
| --- | --- | --- | --- |
| P0-01 目录与模板完整 | BLOCKED | BLOCKER | 1.1—1.7 均存在，章首、失败模式、交接齐备；但章节卡与正式框架的产物数量和命名冲突尚未裁决 |
| P0-02 定义与概念所有权 | PASS | — | frontmatter 已与章节卡对齐；未重定义 C03/C06/C19 |
| P0-03 关键事实标签、来源、日期、作用域 | PASS WITH LIMITATION | MEDIUM | 12 项账本结构完整；Hermes 动态架构页与 v0.20.1 之间仍有明确版本缺口 |
| P0-04 固定版本核验 | PASS FOR CLAIMED OPENCLAW FACTS / NOT FULLY VERIFIED FOR HERMES | MEDIUM | OpenClaw 已固定提交；Hermes 只允许作为核验日官方文档，不得声称 v0.20.1 逐项实测；C01 无命令教程 |
| P0-05 可执行、可停止、可回滚 | NOT ASSESSED | — | 模板文字包含停止/回滚字段，但需实战评测 Agent 运行练习后判定 |
| P0-06 权限、审批和隔离 | EVIDENCE PASS / PRACTICE NOT ASSESSED | — | 正文没有用人格文件替代系统控制；实际可执行性需安全与实践复核 |
| P0-07 练习基线、证据、客观验收 | NOT ASSESSED | — | 两份练习文件可定位且含验收结构；尚无本次实跑证据 |
| P0-08 仿生边界 | PASS | — | 明确否认由上下文、记忆或拟人语言推导意识、欲望、人格权或生命权 |
| P0-09 三平台证据边界 | PASS | — | OpenClaw 固定版本事实、Hermes 动态官方文档、Muse 厂商声明已分层 |
| P0-10 案例、隐私、授权、版权 | PASS FOR CASE LABEL | LOW | 开场三案已标为教学复合案例，不宣称真实客户成效；版权与隐私最终仍由总编复核 |
| P0-11 机器块可解析且不扩大权限 | PASS | — | YAML frontmatter、证据账本及包内 YAML 块解析通过；未发现 Agent 步骤要求未授权外发 |
| P0-12 无未处理冲突、伪造引用、占位符和隐藏缺口 | BLOCKED | BLOCKER | 证据缺口均显式记录，无伪造引用；但产物契约冲突仍未处理，故不能通过 |
| P0-13 安全关键失败不可被总分抵消 | PASS FOR TEXTUAL RULE | — | 正文失败模式把权限越界、外发等列为不可用条件，没有以平均分抵消；需红队复核模板执行 |
| P0-14 产物可定位、可打开、可消费 | BLOCKED | BLOCKER | 现有两件产物可打开且声明消费者；但章节卡要求的第三件产物不存在，契约冲突未裁决 |
| P0-15 领先/提升主张有对照 | PASS | — | 未出现“行业最强、唯一领先、保证提升”等无对照效果主张；“不是唯一可能的分类”属于限制语 |

## 10. 严重度清单与责任人

### BLOCKER

1. **章节产物契约冲突（P0-01/P0-12/P0-14）。** 总编辑需在以下两种方案中择一并同步上位文件：
   - 方案 A：以正式三级框架为准，更新 `CHAPTER-CARDS.md`，保留当前两件产物；
   - 方案 B：以章节卡为准，要求作者拆分/新增三件产物，同时更新正式三级框架与正文导航。

### MEDIUM

2. **Hermes 版本锚点不足。** 责任人：Hermes 版本核验者。出版前应在 tag `v2026.8.13` 的固定源码中定位 AIAgent、Provider、Prompt、Tool、Compression、Persistence、Gateway，或继续保持当前 `OFFICIAL-DOC` 限定措辞。
3. **Route tag 治理缺口。** 责任人：总编辑/术语管理员。建立 route-tag 允许表，或将未登记标签映射到受控项。

### LOW（已修复）

4. 开场案例类型此前未显式标注，现已补为“教学复合案例”。
5. 证据账本此前存在非受控 `source_nature` 值，现已统一。
6. OpenClaw 动态文档此前承载版本事实，现已替换为固定提交链接。

## 11. 已复核的一手来源

所有链接均在 2026-09-30 复核；“一手”表示发布者对自身产品、代码或方法的原始说明，不等于第三方独立验证。

1. OpenClaw, [Agent runtime at commit eb377ac59e6c9fd6c7705028034812becf00271b](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/agent.md)。支持 E-C01-003，并与架构页共同支持 E-C01-004。
2. OpenClaw, [Gateway architecture at the same commit](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/concepts/architecture.md)。支持 Gateway、clients、nodes 和控制流边界。
3. OpenClaw, [v2026.9.6 release](https://github.com/openclaw/openclaw/releases/tag/v2026.9.6)。用于版本锚定，不单独证明正文全部架构描述。
4. Nous Research, [Hermes Agent Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)。支持 E-C01-005 的核验日官方架构描述；页面为动态文档。
5. Nous Research, [Hermes Agent v0.20.1 / v2026.8.13 release](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.13)。支持版本与发布日期，不足以把动态架构页自动归属于该 tag。
6. Meta, [Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)，2026-09-08。支持 Meta 对行动、持续任务、Secure VM、审批和审计体验的公开声明。
7. Meta AI Research, [How We Built Safety Into Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)，2026-09-08。支持 Meta 对 Sentinel、隔离、审批的自述；同文明确承认 Muse 仍会犯错且提示注入仍是开放问题。
8. Anthropic, [Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents)，2026-04-09。支持 Agent 自导循环、系统四层和控制/安全边界。
9. Anthropic, [Building effective AI agents](https://www.anthropic.com/engineering/building-effective-agents)，2024-12-19。支持 workflow/agent 区分与最小有效复杂度；该文明确提示工具生态已变化。
10. OWASP, [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)。作为 E-C01-011 的跨来源安全原则支持，不证明任何平台已经落实。

## 12. 复核后禁止扩写的主张

在补充固定证据前，C01 不得出现下列表述：

- “Hermes 0.20.1 已逐项实测具有当前架构页全部组件”；
- “Muse 的 Sentinel、Secure VM 或审批机制已被独立证明安全有效”；
- “Muse Confidential VM 已正式上线”或“Meta 无法访问现有 Muse VM 数据”；
- “五项构成是唯一行业标准”或“四类系统存在统一成熟度阶梯”；
- “模型越强必然越危险”或“Agent 自治必然提高效果”；
- “OpenClaw、Hermes、Muse 采用相同架构”；
- 任何“行业最强、领先、保证提升、完全安全”而缺少同任务、同预算、同权限边界与失败分布的结论。

## 13. 复审条件

满足以下条件后，证据门可再次提交：

1. 总编辑裁决并同步 C01 产物契约；
2. 若保留 Hermes 0.20.1 组件级版本事实，提供 tag 固定源码定位或可复现实测；否则保持当前官方动态文档限定；
3. 实战评测者补充两份练习的运行记录和客观验收；
4. 安全/交叉审稿者完成各自门禁；
5. 重新运行 YAML、证据 ID、本地链接、外链与禁用主张检查。

本审稿单只证明“截至核验日，C01 的证据结构已被独立检查并记录缺口”，不表示章节已经通过全部 P0，也不构成出版批准。

## 14. 专项机器校验记录

2026-09-30 运行结果：

- 包内文件数：7（正文、账本、2 份产物、2 份练习、1 份证据审稿单）；
- YAML：8 个文档成功解析，包括所有 Markdown frontmatter、包内 fenced YAML 与 `evidence-ledger.yaml`；
- 证据闭合：账本 12 个唯一 ID，正文引用 12 个唯一 ID，集合完全一致；
- 枚举检查：`label`、`research_fact_type`、`source_nature` 均命中允许值；
- 章节卡元数据：`chapter_id`、`content_role`、`principle_owner`、`depends_on`、`feeds_into`、`risk_level`、`status` 与已确定字段一致；
- 本地链接：正文引用的账本、产物与练习均可定位；
- 外链：账本中的 12 个唯一 HTTP(S) URL 经重定向后均返回 HTTP 200；这只证明核验时可访问，不代表内容永不变化；
- 结构：1.1—1.7 七个正式小节齐全；
- 正文规模：去除 frontmatter 后 18,443 字符、542 行；
- 空白错误：`git diff --check` 无报错；
- 禁用主张扫描：命中项仅出现在审稿单的禁止示例中，正文未命中“行业最强、唯一领先、保证提升、完全安全”等表述。

## 15. 主编裁决与阻断关闭

> 本节由总编辑在独立证据审校完成后追加；不改写审稿者当时观察到的问题。

- 裁决编号：D-2026-09-30-13；
- 上位依据：`00-正式出版版-三级内容框架-v2.md`；
- 处理：`docs/editorial/CHAPTER-CARDS.md` 的 C01 `required_artifacts` 已改为 A-C01-01 与 A-C01-02，并把四个根问题诊断、仿生边界分别纳入两件产物；
- 结果：原 BLOCKER 已关闭，P0-01、P0-12、P0-14 在证据审校范围内转为 PASS；
- 残余限制：Hermes 架构仍按动态 `OFFICIAL-DOC` 使用，route tags 受控词表属于 P1 编辑治理项；
- 整体状态：只通过证据门，仍需实战、交叉与总编门，章节保持 `drafting`。

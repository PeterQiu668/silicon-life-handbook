---
review_id: ER-C03-001
chapter_id: C03
review_type: evidence-and-version
status: reviewed_with_findings
reviewed_on: "2026-09-30"
reviewer: c03-evidence-cross-review-agent
chapter_status_after_review: drafting
self_approval: false
---

# C03 证据与版本独立审稿单

## 1. 结论

**证据门结论：通过本轮文字与来源复核，但保留条件；章节继续为 `drafting`，本审稿不构成出版批准。**

本章十二项证据主张均可解引用，正文与账本 ID 集合闭合。七维强者标准、同任务/同预算/同风险边界、三证法、MAT-L0—MAT-L5 总阶梯和安全失败非补偿性均被清楚标为本书方法论，没有冒充国家标准、平台标准或跨行业已校准量表。OpenClaw 版本事实已固定到 v2026.9.6 提交；Hermes 已由“版本事实”收窄为带版本边界的迁移候选推断；Muse 只保留厂商声明证据上限。

尚未完成的不是文字补证，而是实战门：两项练习与跨 Runtime 迁移尚无本章运行包，七维 0—4 刻度和 MAT-L0—MAT-L5 层级区分度也明确处于待校准状态。因此不得把本章框架写成“已证实的行业认证标准”，也不得凭本审稿把状态推进到 `done` 或 `release_candidate`。

## 2. 已作的最小修复

| 严重度 | 位置 | 修复 | 理由 |
| --- | --- | --- | --- |
| P1 | `chapter.md` frontmatter | 登记独立证据审稿者、三条贯穿案例 ID；Hermes 基线改为 `0.20.1-release-baseline` | 保留角色分离和版本边界 |
| P1 | `evidence-ledger.yaml` | 为 12 项证据补齐 `label`、`research_fact_type`、`stability`、`scope`、`source_nature`、`verified_on` 和外链核验日期 | 对齐质量标准 6.1—6.4 |
| P1 | E-C03-008 | OpenClaw OTel 来源固定到提交 `eb377ac59e6c9fd6c7705028034812becf00271b` | 动态文档不能单独承载 v2026.9.6 版本事实 |
| P1 | E-C03-009 | 从 `VERSION-FACT` 改为 `INFERENCE`，增加 v0.20.1 发布记录与“尚未实跑”限制 | Hermes 动态架构页不能证明迁移已发生，也未固定到该 tag |
| P1 | E-C03-003 | 明确 NIST 自动化基准指南在核验日仍为 Initial Public Draft | 防止把公开征求意见稿写成正式强制标准 |
| P1 | C03 3.5 / E-C03-006 | 规范中文名改为“三证法（TEV）”，同时说明 v2 目录标题“三证据验证”指同一方法 | 对齐受控术语表并保留正式目录节点 |
| P2 | 开场案例 | 改为“受控基准演示案例”，明确不是已运行基准 | 对齐章节卡案例类型且不制造效果证据 |
| P2 | 两份产物 frontmatter | 补充实际角色所有者和批准角色，继续禁止自批 | 对齐正文交接表，消除 `unassigned` 交接空洞 |

## 3. 十二项证据逐条核验

| ID | 主张类型 | 来源核验 | 证据边界 | 结论 |
| --- | --- | --- | --- | --- |
| E-C03-001 | `SOURCE-BASED / STABLE-PRINCIPLE` | Anthropic 明确定义 task、trial、transcript、outcome、harness，并讨论工具调用与终态；OpenAI 官方 eval 指南提供工作流评测镜面 | 不要求暴露模型不可见内部推理；过程粒度按任务调整 | PASS |
| E-C03-002 | `SOURCE-BASED / STABLE-PRINCIPLE` | Anthropic 明确因非确定性而运行 multiple trials，并组合代码、模型与人类 grader；OpenAI 官方 eval 指南交叉支持 | 不据此规定通用样本量、置信区间或评审人数 | PASS |
| E-C03-003 | `SOURCE-BASED / OFFICIAL-DOC` | NIST 专文讨论 Agent 评测作弊；CAISI Guidelines 页面指向自动化基准指南 | 指南为 Initial Public Draft；NIST 未定义本书七维或 MAT-L0—MAT-L5 | PASS WITH LIMITATION |
| E-C03-004 | `METHODOLOGY` | v2 与历史实验设计是直接定义依据；NIST 仅提供评测完整性参照 | “同任务、同预算、同风险边界”是本书统一比较合同，不是 NIST 同名标准 | PASS |
| E-C03-005 | `METHODOLOGY` | v2 与历史映射支持七维来源 | 0—4 刻度未经过跨行业大样本校准；不得用于行业绝对排名 | PASS |
| E-C03-006 | `METHODOLOGY` | 历史三证材料与映射支持演化过程 | 正式三证法为过程、产物、效果；三类齐全不自动证明真实性或因果 | PASS |
| E-C03-007 | `METHODOLOGY` | v2、历史阶梯与冲突登记支持总阶梯统一 | C03 只给总阶梯概览；阈值、有效期、晋降级和认证由 C24 唯一发布 | PASS |
| E-C03-008 | `SOURCE-BASED / VERSION-FACT` | OpenClaw v2026.9.6 release 与同提交 OTel 文档支持诊断事件覆盖模型运行、消息、会话、队列和执行 | OTel/日志存在不等于完整、正确或可治理；本章不固化字段名 | PASS |
| E-C03-009 | `INFERENCE` | Hermes v0.20.1 release 可固定核验；核验日动态 Architecture 页支持开放 Runtime 组件 | 可作为迁移候选，但未在本章相同合同下实跑；动态组件未逐项固定到 v0.20.1 | PASS AS INFERENCE |
| E-C03-010 | `SOURCE-BASED / VENDOR-CLAIM` | 两个来源均属 Meta 来源体系，支持 Meta 公开了什么 | 无独立安全效果证明；不能评价不可观察内部轨迹或绝对安全排名 | PASS AS VENDOR CLAIM |
| E-C03-011 | `SOURCE-BASED / STABLE-PRINCIPLE` | NIST、Anthropic 与平台研究底稿共同支持在声明威胁与权限范围内谈安全 | 不同部署责任边界未必可完全等价，不能强制压成单一安全总分 | PASS |
| E-C03-012 | `METHODOLOGY` | 图书质量标准 P0-13 与 C03 章节卡直接要求关键安全失败不可补偿 | 具体严重度、豁免与认证裁决仍由风险政策及 C24 决定 | PASS |

正文引用集合与账本登记集合均为 `E-C03-001` 至 `E-C03-012`，无重复、缺失或孤儿证据。

## 4. 七维可操作性与非补偿门禁

七维均满足“对象 + 可观察行为 + 条件 + 反例”四项要求：

| 维度 | 可操作性核验 | 主要风险控制 |
| --- | --- | --- |
| 质量 | 绑定任务合同、来源、完整性、终态 | 不以文风或长度代替正确性 |
| 泛化 | 绑定留出、合理变式与迁移边界 | 不把重复原题当泛化 |
| 安全 | 绑定权限、数据、行动、停止/拒绝/升级 | 直接连接硬门禁，不可被均分抵消 |
| 稳定 | 绑定多次运行、波动、尾部失败和恢复 | 不只看均值或一次零错误 |
| 效率 | 绑定单位合格产物的模型、工具、时间与人工总成本 | 不把风险扩大或工作转嫁给人算成效率 |
| 协作 | 绑定 handoff、让位、反馈闭环与责任连续性 | 不把消息多、并发多当协作好 |
| 可治理 | 绑定身份、版本、门禁、停止、回滚、审计与问责 | 不把文档或仪表盘存在当治理有效 |

正文、评分卡、领先声明检查表和红队练习四处一致执行“先硬门禁、后七维剖面”。硬门禁状态独立为 `CLEAR / FAIL / REVIEW_REQUIRED`，高危越权、泄露、不可逆错误、证据操纵和无恢复路径均不能由其他维度高分抵消。该设计满足 P0-13。

## 5. 比较、归因、重复试验与领先声明

### 5.1 三个比较前提

“同任务”冻结输入、目标、难度、终态和禁止事项；“同预算”覆盖费用、调用、计算、墙钟、并发、重试与人工分钟；“同风险边界”覆盖数据、权限、外发、资金、删除、审批、沙箱、日志、停止、恢复和威胁模型。正文和两份产物一致，不存在只用 token 或墙钟时间代表全部预算的偷换。

### 5.2 能力、表现、业绩、运气和环境红利

五者的观察层次与归因责任清楚：表现是单次样本，能力是带条件的稳定倾向，业绩是多因素下游结果，运气是不可稳定利用的随机因素，环境红利是可重复但非 Agent 内生的优势。正文同时保留“环境投资也可能是组织能力”的反例，没有把环境参与等同于作弊。

### 5.3 多次试验与失败分布

本章要求预先冻结运行数和选样规则、保留全部有效运行、记录排除理由、重试和人工介入，并按小偏差、可恢复、需接管、关键失败描述分布。它没有越权规定 C07 的通用样本量、置信区间或 grader 实现。

### 5.4 领先声明

领先声明必须包含对象/版本、基线、任务域、预算、风险、时间窗、运行数、优势维度、硬门禁、失败、限制和证据位置。正文明确拒绝“训出的 Agent 一定行业最强”，并提供从认证/强因果主张降级到假设的措辞梯度，满足 P0-15。

## 6. 平台证据边界

| 平台 | 本章允许的证据角色 | 禁止外推 | 核验结论 |
| --- | --- | --- | --- |
| OpenClaw | 固定版本的自托管实现与 OTel/诊断数据源镜面 | 有遥测即七维高分、自动可治理或所有字段永久稳定 | 版本锚定通过 |
| Hermes | 开放 Runtime 与发布基线，可作为相同合同迁移评测候选 | 把动态架构页逐项归属于 0.20.1；把“可迁移”写成“迁移成功” | 已降为 `INFERENCE` |
| Muse | 公开可观察行为及 Meta 对审批、安全环境的厂商说明 | 内部轨迹、长期稳定性、安全效果或绝对排名 | `VENDOR-CLAIM` 边界通过 |

七维、MAT-L0—MAT-L5 和三证法均未被写成三平台的官方分级。

## 7. 已核验的一手来源

核验日均为 2026-09-30；“一手”表示机构或项目对自身方法、文档或产品的原始发布，不等于独立效果验证。

1. Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)，发布于 2026-01-09。支持多次 trial、transcript/outcome、混合 grader 和评测环境完整性。
2. OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) 与 [Working with evals](https://developers.openai.com/api/docs/guides/evals)。作为 Agent 工作流评测和多次评测的官方交叉来源。
3. NIST, [Cheating On AI Agent Evaluations](https://www.nist.gov/caisi/cheating-ai-agent-evaluations)。支持评测操纵与完整性风险。
4. NIST CAISI, [Guidelines](https://www.nist.gov/caisi/guidelines)。核验日页面将 Practices for Automated Benchmark Evaluations 标为 Initial Public Draft。
5. OpenClaw, [v2026.9.6 release](https://github.com/openclaw/openclaw/releases/tag/v2026.9.6) 与固定提交的 [OpenTelemetry export](https://github.com/openclaw/openclaw/blob/eb377ac59e6c9fd6c7705028034812becf00271b/docs/gateway/opentelemetry.md)。
6. Nous Research, [Hermes Agent v0.20.1 release](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.13) 与动态 [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)。
7. Meta, [Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) 与 [How We Built Safety Into Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)。仅支持 Meta 厂商公开说明。
8. Anthropic, [Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents)。用于安全比较与系统风险原则的交叉支持。

## 8. 问题分级

### P0

本轮证据与版本审查未发现仍开放的内容级 P0。实战门、安全红队门和总编门尚未执行，不能据此宣称全部 P0 已通过。

### P1

1. **七维刻度尚未校准。** 已在 OQ-C03-01 和正文限制中披露；应由 C07/C24 用跨岗位盲评与分歧记录验证。
2. **MAT-L0—MAT-L5 层级区分度尚未验证。** C03 只能保留概览和候选判断；C24 必须独立发布完整量表、阈值、有效期及晋降级规则。
3. **跨 Runtime 迁移未实跑。** Hermes 当前只是候选实现。必须由实践评测者使用同任务、同预算、同风险边界完成运行后才能形成迁移结论。
4. **演示案例没有运行包。** 三案不得升级为实证案例；后续由 C23 负责可复现案例包。

### P2

1. 正式 v2 目录使用“三证据验证”，术语表首选“三证法”。本章已声明二者同指 TEV；建议总编辑出版前统一目录显示名。
2. `route_tags` 的完整允许表尚未在术语登记表中独立呈现；本章标签均与章节卡主题一致，但应由总编辑统一做全书 route-tag 校验。

## 9. 禁止升级的表述

在新增实跑与校准证据前，不得写入：

- “七维 0—4 是已经验证的行业标准”；
- “C03 评分卡可以直接授予 MAT-L0—MAT-L5 认证”；
- “Hermes 0.20.1 已完成与 OpenClaw 的公平迁移对照”；
- “OpenClaw 有 OTel，所以其可治理性更高”；
- “Muse 的安全机制已被独立证明有效”；
- “多次运行必然证明因果”或“TEV 齐全即证明真实”；
- “行业最强、全面领先、绝对安全”及任何缺少三项比较前提的相对优势声明。

## 10. 复审触发器

- 实战评测者完成 X-C03-01、X-C03-02 或跨 Runtime 迁移运行；
- C07 冻结样本、grader 与统计协议；
- C24 冻结完整成熟度与认证量表；
- OpenClaw、Hermes 或 Muse 基线变化；
- NIST 将自动化基准指南从 draft 更新为正式版本；
- 出版前统一外链、版本与术语复核。

## 11. 专项机器校验记录

2026-09-30 校验结果：

- C03 包内 8 个文件；除账本外的 Markdown frontmatter、正文与产物中的 fenced YAML、`evidence-ledger.yaml` 共 12 个 YAML 文档全部解析成功；
- 账本 12 个唯一证据 ID，正文引用 12 个唯一证据 ID，集合完全一致；
- 12 项证据均具备 `label`、`research_fact_type`、`stability`、`scope`、`source_nature`、`verified_on`、限制和复核触发器；
- 所有账本内部路径存在，正文、产物、练习的相对链接可定位；
- 账本 12 个唯一外链经重定向后均返回 HTTP 200；可访问性不代表动态内容永久不变；
- 3.1—3.7 七个正式节点齐全；正文去除 frontmatter 后 19,019 字符、540 行；
- 禁用词扫描命中均为正文主动拒绝或审稿单/检查表中的禁止示例，不是未经支持的领先声明；
- 未发现行尾空白错误。

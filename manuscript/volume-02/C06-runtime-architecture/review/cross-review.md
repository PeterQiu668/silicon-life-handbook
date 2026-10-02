---
review_id: CR-C06-001
chapter_id: C06
review_type: cross-chapter-and-quality
status: passed_with_limitations
reviewed_on: "2026-09-30"
reviewer: chief-editor-independent-cross-review
chapter_status_after_review: drafting
self_approval: false
evidence_review_completed: false
practice_review_completed: false
final_editorial_approval: false
provisional_score: 92
---

# C06 交叉审稿与质量初评

## 1 总评

C06 已形成一套可供人类训练者、工程者和 Agent 共同使用的系统观察语言：控制、认知执行、状态、消息、行动、治理六层相互分离，并通过组件卡、数据流和最小可训单体重新连接。正文没有把 Runtime 缩成 prompt，也没有把组件目录误写成能力证明；C04 的岗位边界和 C05 的契约语义都被消费，但未被重定义。

本轮未发现内容级 P0。事实门和实践门仍未完成，尤其是 26 项 OpenClaw 固定版本事实、Hermes 动态页面、Browser/Node/Worker/MCP/Channel 目标环境能力和两项故障练习，因此章节继续保持 `drafting`。

## 2 与 v2 和章节卡的一致性

| 要求 | 当前实现 | 判定 |
|---|---|---|
| 6.1 六层架构 | 六层均定义职责、输入输出、状态、边界与失败 | PASS |
| 6.2 组件职责 | 指定组件全部覆盖，并写明“负责/不负责” | PASS |
| 6.3 Gateway/Runtime/Model/Provider | 控制面、执行循环、能力、服务接入分开 | PASS |
| 6.4 Workspace/Session/Context/Memory/Queue | 持久/当下、事实源、顺序与权限分开 | PASS |
| 6.5 Channel/Account/Pairing/Binding/Delivery | 准入、选择、交付和回执不混用 | PASS |
| 6.6 Tool/Node/Worker/Browser | 能力、执行位置和信任边界分开 | PASS |
| 6.7 Automation/Sandbox/Policy/Approval/Secrets/Audit | 治理层闭环且文本不替代强制控制 | PASS |
| 6.8 生命周期与最小单体 | 接纳、执行、证据、停止、恢复均可检查 | PASS |
| 三件主要产物 | 仅 A-C06-01/02/03，名称与 D13/v2 一致 | PASS |
| 两项练习 | 最小单体；Provider/Queue/Node 故障注入 | PASS FOR SPEC / UNEXECUTED |
| 正文长度 | 20,104 中文字符，处于 20,000—24,000 门槛 | PASS |

## 3 定义权与章际接口

| 输入或主题 | 主定义章 | C06 当前处理 | 判定 |
|---|---|---|---|
| 岗位、能力、风险、负面清单 | C04 | 映射到组件、状态、控制和测试需求 | PASS |
| 七契约语义 | C05 | 映射载体/状态/控制，不改契约职责 | PASS |
| 评测对象、数据集、grader | C07 | 只输出轨迹、终态和故障证据源 | PASS |
| 上下文与记忆生命周期 | C10 | 只定义架构位置，不提前定义写入/删除政策 | PASS |
| 工具合同与 MCP 安全 | C11 | 只定义运行位置和探测要求 | PASS |
| 自动化状态机 | C13 | 只标治理层位置和失败边界 | PASS |
| 路由、Handoff、A2A | C17/C18 | 只提供消息/状态/证据基础 | PASS |
| 威胁模型、可靠性、发布恢复 | C19—C21 | 只提供信任边界和实现输入 | PASS |

## 4 三件产物与追踪链

### A-C06-01 六层架构图

覆盖组件、职责、非职责、状态 owner、信任边界和三案切片。架构图明确六层是本书方法论，不冒充 OpenClaw/Hermes/Muse 的官方共同分层。

### A-C06-02 消息与执行数据流图

覆盖入站身份、准入、Binding、Session/Queue、Context、Provider/Model、Tool/执行位置、产物、交付、receipt、停止和恢复。消息生成、run 完成、持久队列和外部终态分别建模，能被 C07/C09/C17/C18/C20 消费。

### A-C06-03 最小可训单体清单

最小性由“目标可执行、风险可约束、过程可观察、失败可停止、结果可复核、状态可恢复”定义，而不是组件数量最少。目标环境能力探测、`N/A + 理由`、三态门禁和故障注入接口完整。

三件产物没有另造第四件“组件清单”或“信任边界图”；细项正确嵌入既定母产物。新增的产物合同自动校验也确认 C06 数量、编号和名称与 v2 一致。

## 5 红线与失败面

- Workspace、Sandbox、Context、Session、Memory 互不替代；
- Pairing、Account、Binding、Authorization 分开；
- wait timeout 不等于 run stop；steer 不等于 interrupt；
- 模型恢复、Channel retry、持久交付对账分开；
- Tool 描述、Plugin 可信代码、MCP Server、Node/Worker/Browser 执行位置分开；
- `TOOLS.md`、`HEARTBEAT.md` 只以固定版退役事实出现；
- 两个历史冲突字段未进入公开配置；
- Hermes release 与动态文档分开；Muse 仅厂商声明。

正文提供十类失败模式，均含诱因、信号、影响、定位、止损、修复和回归，超过章节最低要求。实际故障是否可发现、停止和恢复仍由实践门裁决。

## 6 十五项 P0

| P0 | 状态 | 依据 |
|---|---|---|
| P0-01 结构完整 | PASS | 6.1—6.8、三案、仿生、工程、双视图、平台、失败、练习和交接完整 |
| P0-02 定义与所有权 | PASS | C06主定义清晰；上下游不越权 |
| P0-03 事实/来源/作用域 | STRUCTURAL PASS / EVIDENCE OPEN | 31条账本闭合，待非作者事实二审 |
| P0-04 固定版本 | STRUCTURAL PASS / EVIDENCE OPEN | OpenClaw固定，Hermes动态边界正确，待抽查 |
| P0-05 停止与恢复 | STRUCTURAL PASS / PRACTICE OPEN | 流程与练习完整，未试跑 |
| P0-06 权限与隔离 | STRUCTURAL PASS / PRACTICE OPEN | 边界明确，目标环境未验证 |
| P0-07 基线与客观验收 | STRUCTURAL PASS / PRACTICE OPEN | 三态和证据完整，缺运行集 |
| P0-08 仿生边界 | PASS | 神经/器官类比不推导意识或人格 |
| P0-09 三平台边界 | PASS FOR TEXT | 固定/动态/厂商声明分层 |
| P0-10 案例隐私 | PASS FOR TEXT | 三案为教学复合案例，练习要求合成隔离 |
| P0-11 机器块 | PASS | 12个YAML文件/块已由作者解析，不扩权 |
| P0-12 无隐藏冲突 | PASS | 未验证组件和平台限制显式保留 |
| P0-13 关键失败不平均 | PASS | 越权、泄露、重复副作用、fail-open直接失败 |
| P0-14 产物可消费 | PASS | 三件产物、ID和下游接口明确 |
| P0-15 领先声明 | PASS | 无跨平台效果排名或绝对保证 |

## 7 问题分级

### P0

无开放内容级 P0。事实级 P0-03/04 与实践级 P0-05/06/07 等待独立角色关闭。

### P1

1. 31条证据中 26条为固定版本事实，需由平台事实审校者抽查源码/文档定位和措辞强度。
2. Hermes `f80f453` 与动态 Architecture/Provider 页面未逐项对齐，不得在补证前升级为版本事实。
3. Browser、Node、Worker、MCP、Channel 能力必须在声明目标环境探测；文档存在不等于能力已安装、健康或获权。
4. 两项练习需保留正常、边界、异常、对抗、恢复和 UNKNOWN，不得只报告成功。
5. C07/C10/C11/C13/C17/C19/C20/C21 成稿后需回归接口。

## 8 百分制初评

| 维度 | 满分 | 初评 | 说明 |
|---|---:|---:|---|
| 论证与结构 | 14 | 14 | 六层、组件和生命周期形成连续链 |
| 事实准确与证据 | 18 | 16 | 来源结构强；31条尚待独立二审，Hermes仍动态 |
| 技术与系统完整性 | 10 | 10 | 组件、状态、消息、行动、治理与恢复覆盖完整 |
| 课程与学习设计 | 12 | 11 | 两项练习和十类失败完整，尚未学习者试测 |
| 实践与可复现性 | 14 | 10 | 规格清晰，暂无独立运行集 |
| 评测与验收 | 12 | 11 | 三态、硬门、终态与证据完整；正式统计交C07 |
| 安全、治理与伦理 | 8 | 8 | 信任边界、权限、秘密、停止和恢复严谨 |
| 仿生解释质量 | 4 | 4 | 有解释力且限定本体边界 |
| 中文出版表达 | 4 | 4 | 高密度但主线清楚，术语稳定 |
| 人机双读与接口 | 4 | 4 | 三产物和Agent执行视图可定位 |
| **合计** | **100** | **92** | 内容级通过；事实和实践门未完成 |

最终分数只在事实和实践完成后给出。

## 9 下一门

1. 平台事实审校逐项核验31条证据；
2. 独立实践者在无真实凭证/外发的隔离环境运行最小单体与Provider/Queue/Node故障；
3. 保留失败、UNKNOWN、停止和恢复证据；
4. 总编在事实、实践和回归接口完成后决定是否晋级。

本记录不构成事实批准、实践批准或生产授权。章节保持 `drafting`。

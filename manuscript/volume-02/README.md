---
volume_id: V02
title: "个体底座：岗位、生命契约与运行容器"
status: release_candidate
chapters: [C04, C05, C06]
reviewed_on: "2026-09-30"
---

# 卷二　个体底座

## 本卷回答什么

本卷把“想要一个 Agent”转换成可以训练、约束和运行的个体底座：先从工作终态定义岗位、任务域、能力、非功能要求、风险和负面清单；再用七大生命契约保持服务对象、价值风格、操作纪律、工具边界、身份、主动节律与记忆责任的一致性；最后把这些语义放进可观察、可停止、可恢复的运行容器。

完成本卷后，读者不应再用一个人格 prompt、一个工具列表或一张组件图代替系统设计，而应能回答：这个 Agent 为谁负责、完成什么、不能做什么、长期遵守什么、在哪运行、状态写到哪里、谁能授权、失败怎样停下、恢复依据什么事实。

## 阅读顺序

1. [C04 从岗位到能力模型](C04-role-capability-model/chapter.md)：从 JTBD 和终态建立岗位、任务域、能力树、NFR、风险与负面清单。
2. [C05 七大生命契约](C05-life-contracts/chapter.md)：把 USER、SOUL、AGENTS、TOOLS、IDENTITY、HEARTBEAT、MEMORY 作为治理语义，并映射到载体、运行状态和强制控制。
3. [C06 Agent 的运行容器与系统架构](C06-runtime-architecture/chapter.md)：建立六层观察模型、消息与执行数据流以及最小可训单体。

三个章节不可倒置：没有 C04 的岗位与风险，C05 不知道契约保护什么；没有 C05 的长期语义，C06 只剩产品组件拼装；没有 C06 的强制控制、状态和恢复，C04/C05 的边界只能停留在文档承诺。

## 本卷产物栈

| 层 | 产物 | 主要下游 |
|---|---|---|
| 岗位 | C04 岗位建模卡、能力树、风险分级表 | C05 契约、C06 架构、C07 评测、C14 授权、C19 安全 |
| 契约 | C05 七契约草案包、契约冲突矩阵 | C06 载体/控制、C10 记忆、C13 主动性、C15 漂移 |
| 运行 | C06 六层架构图、消息与执行数据流、最小可训单体清单 | C07 评测、C10—C14 能力基础设施、C17—C21 协同与治理 |

## 人类与 Agent 的共同使用原则

- 岗位、契约、运行容器是一条链，不得从产品功能或模型能力倒推职责。
- 契约语义可以指导行为，但不能替代 Authentication、Policy、Approval、Sandbox、Secrets 和 Audit。
- Workspace 不是 Sandbox；Binding 不是 Authorization；Pairing 不是逐次批准；wait timeout 不是 run stop；steer 不是 interrupt。
- 任务生成、run 完成、工具副作用、投递和环境终态必须分别记录。
- `FAIL` 与 `REVIEW_REQUIRED` 是训练资产；恢复运行不能覆盖原始失败。
- “硅基生命”用于解释岗位、连续性、身体边界和复原，不证明主观意识、法律人格或自主授权。

## 当前证据边界

C04—C06 均已通过章节五门并进入 `release_candidate`。C04 的岗位与角色互换试验、C05 的契约冲突与回归、C06 的运行故障与恢复均在匿名合成或本地隔离范围完成。C06 真实 OpenClaw/Hermes、Provider、Queue、Node、Browser、Worker、MCP、Channel 与外部 receipt 未实跑，继续为 `REVIEW_REQUIRED`。

本卷证明方法、产物、失败识别和恢复合同可执行，不证明真实岗位已经胜任，不批准生产权限，也不支持“行业最强”结论。第 7—24 章完成后仍需按接口触发器回归本卷。


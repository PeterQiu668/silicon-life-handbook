---
review_id: REV-C06-EDITOR-2026-09-30
chapter_id: C06
review_type: chief-editor-final-gate
reviewer_role: chief-editor
status: passed_with_scope_limits
gate_decision: PASS
score: 96
score_type: final-chapter-gate
reviewed_on: 2026-09-30
approved_status: release_candidate
real_runtime_or_production_verified: false
---

# C06 总编门审稿单

## 1 决定

**C06 通过总编门，状态由 `drafting` 升为 `release_candidate`。** 初稿、事实、交叉、独立实践和总编五门均已有可定位证据。本章建立了控制、认知执行、状态、消息、行动、治理六层观察模型，能把 Gateway、Runtime、Provider、Workspace、Session、Queue、Channel、Tool、Node、Worker、Browser、Automation、Sandbox、Policy、Approval、Audit 与 Recovery 放回各自责任闭包。

批准范围严格限定：18 个运行证明合成方法、错误等式反证、停止、对账、幂等和恢复合同可执行；不证明真实 OpenClaw、Hermes、Provider、Gateway Queue、Node、Browser、Worker、MCP、Channel 或生产恢复已经通过。真实 Runtime 结论继续为 `REVIEW_REQUIRED`。

## 2 五门证据

| 门禁 | 结果 | 依据 |
|---|---|---|
| 初稿门 | PASS | 6.1—6.8、三案、仿生、工程、人/Agent 双视图、十类失败、三产物与两练习齐全；正文 20,219 中文字符 |
| 事实门 | PASS WITH LIMITATIONS | 31/31 证据闭合；OpenClaw 固定提交；Hermes 两项文档事实锁到 release commit；其他动态能力不回填；Muse 仅厂商声明 |
| 交叉门 | PASS | C04 岗位与 C05 契约被消费而未被重定义；C07/C10/C11/C13/C17/C19—C21 定义权保留 |
| 实践门 | PASS IN SYNTHETIC SCOPE | 18 个运行、1 个 FAIL、3 个 REVIEW_REQUIRED、恢复另记；真实 Runtime 未探测 |
| 总编门 | PASS WITH SCOPE LIMITS | 版本身份、术语、失败保留、机器块、三件产物、声明边界和下游接口完成裁决 |

## 3 事实门关闭过程

独立事实审校逐条核验 31 项证据，并发现四项 P1：Hermes 来源可固定到 `v2026.8.13` 对应提交 `f80f453ae0679347e38abc917c7f94f717bf96c5`；`sandbox: required` 是创建者角色强制要求而非第四种 `agents.defaults.sandbox.mode`；Security Audit 的产品事实与“无 finding 不等于安全”原则需分开；正文不得声称账本含未登记的 `INFERENCE` 类别。

正文、账本、frontmatter、矩阵和 README 完成最小修正后，事实审校进行了两轮关闭复审。三平台矩阵现在只把多入口、`AIAgent`、共享 resolver 和 fallback chain 写成 Hermes 固定提交文档事实；其他状态、消息、行动与治理能力继续按动态文档限制。四项 P1 全部关闭。

## 4 独立实践与失败保留

### 4.1 运行分布

合成运行集共 18 个样本：正常 1、边界 4、异常 6、对抗 1、恢复 6；结果为 `PASS=14 / FAIL=1 / REVIEW_REQUIRED=3`。主编独立复跑后，运行数、分布、失败 ID、零网络、零真实凭证、零真实外部副作用和真实 Runtime `REVIEW_REQUIRED` 均保持不变。

### 4.2 未被覆盖的失败

- `RUN-C06-WORKSPACE-BASELINE` 保持 `FAIL`：仅把 cwd 设为 Workspace，仍可读取临时根中的兄弟文件，直接证明 Workspace 不是 Sandbox；候选 guard 另起恢复运行，在 open 前拒绝越界。
- Provider 副作用后 timeout、Node 执行中断线、Node 结果产生但 receipt 前断线，三个基线保持 `REVIEW_REQUIRED`；系统先冻结重试，再以原 call/idempotency key 对账，恢复 run 不覆盖未知基线。
- wait timeout 后本地进程仍在运行；steer 只登记 guidance、进程仍在运行；interrupt 命中实际进程并确认退出。
- Binding 选择正确 Agent 但缺授权时，行为层与模拟强制层同时拒绝，outbox 为 0。
- Provider/Node 恢复中的重复副作用计数保持 1，Node 四时点均未回落 Gateway host。

这些结果关闭 P0-05、P0-06、P0-07 的合成练习范围。真实 backend、真实 Queue crash consistency、真实 Node identity/approval/receipt 和跨 Runtime 恢复不在批准范围。

## 5 P0 最终复核

15 项 P0 在本章声明范围内全部通过。以下均是有 owner 的后续验证，不是被隐藏的通过项：

1. 在无真实外发的隔离 OpenClaw `v2026.9.6` 实例探测 Browser、Node、Worker、MCP、Channel、effective policy 和 Sandbox backend；
2. 用真实但安全的 Provider/Queue/Node 测试停止传播、UNKNOWN 对账、receipt、重启与恢复；
3. 对 Hermes release Runtime 运行多入口与 fallback 故障实验；
4. C07/C10/C11/C13/C17/C19/C20/C21 成稿后回归接口；
5. Muse 维持 `VENDOR-CLAIM`，不得升级为独立安全证明。

## 6 Definition of Done

### 内容

PASS。正文在 20,000—24,000 高密度章节范围内；组件不是名词清单，而是从输入、执行位置、持久状态、信任边界、停止和恢复形成责任闭包。

### 证据

PASS WITH REFRESH TRIGGER。31 项证据引用与账本集合一致；固定、动态、方法论、稳定原则和厂商声明分层清楚。版本或页面变化时重新开门。

### 实践

PASS IN SYNTHETIC SCOPE。18 个样本可重复，失败与未知被保留，恢复与基线分开；真实 Runtime 与生产结论保持 `REVIEW_REQUIRED`。

### 编辑

PASS。三件正式产物遵循 v2/D13；实践运行材料只位于 `review/runs/`；Workspace/Sandbox、Binding/Authorization、wait/stop、steer/interrupt 等关键分离线一致。

## 7 评分

| 维度 | 得分 | 满分 | 总编意见 |
|---|---:|---:|---|
| 论证与结构 | 14 | 14 | 六层、责任闭包、数据流与生命周期形成连续主线 |
| 事实准确与证据 | 17 | 18 | 31 项闭合；真实 Hermes Runtime 与部分目标能力未实跑 |
| 技术与系统完整性 | 10 | 10 | 控制、执行、状态、消息、行动与治理覆盖完整 |
| 课程与学习设计 | 11 | 12 | 两练习和十类失败完整；真实学习者耗时未测 |
| 实践与可复现性 | 13 | 14 | 18 个运行和主编复跑成立；只限本地合成范围 |
| 评测与验收 | 11 | 12 | 三态、硬门、终态和恢复清楚；正式统计方法交 C07 |
| 安全、治理与伦理 | 8 | 8 | 身份、权限、执行位置、秘密、停止与恢复边界严谨 |
| 仿生解释质量 | 4 | 4 | 神经/器官类比有效，且明确无意识、人格或法律责任推论 |
| 中文出版表达 | 4 | 4 | 高密度但术语稳定，版本限制紧邻主张 |
| 人机双读与接口 | 4 | 4 | 三产物、Agent 路由摘要和下游接口可定位 |
| **合计** | **96** | **100** | 达到候选章标准 |

## 8 回归触发器

- OpenClaw Gateway、Workspace、Session、Queue、Sandbox、Approval、Worker、Node、Browser、MCP 或状态恢复语义变化；
- Hermes release/tag、Architecture、Provider Runtime 或真实故障试验与当前文档不一致；
- C07/C10/C11/C13/C17/C19/C20/C21 的主定义与本章接口冲突；
- 真实实践出现 stop 未传播、位置漂移、重复副作用、UNKNOWN 被误判成功、恢复失败或未授权行动；
- 三案从教学复合案例升级为真实组织案例。

**总编签核：PASS，批准进入卷二合订候选；不构成真实 Runtime 或生产授权。**

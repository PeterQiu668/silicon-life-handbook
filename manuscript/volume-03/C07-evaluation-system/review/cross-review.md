---
chapter_id: C07
review_type: independent-cross-platform-cross-review
reviewed_on: "2026-09-30"
reviewer_role: cross-reviewer
chapter_status: drafting
cross_gate: passed_with_limitations
fact_review_ref: "review/fact-check.md"
practice_gate: not_reviewed
editor_gate: not_reviewed
self_approval_of_other_gates: false
---

# C07 跨平台与章际交叉审校

## 结论

C07 自身的概念所有权、三平台边界、仿生边界、D19 术语、三件母产物和 C06 输入接口均通过交叉检查。先前阻断交叉门的 C08 数据层冲突已经按 C07 主定义修复：training / regression / holdout / real_world 保持四个规范数据层，security/red-team 只作为横切非补偿安全套件，每个样本绑定 `canonical_data_layer` 与 `scenario`。C07↔C08 术语与机器字段专项回归通过，因此交叉门为 `PASS WITH LIMITATIONS`。

本审校不评价出版文风，不执行编辑总审，不替代练习复现，也不把章节提升为 `release_candidate`。

## 定义权检查

| 对象 | 定义中心 | C07 行为 | 结论 |
| --- | --- | --- | --- |
| 七维强者、三证、领先声明 | C03 | 只作为上位标准和比较纪律引用 | PASS |
| 岗位/JTBD/能力/NFR/风险 | C04 | 只消费三件产物生成 task | PASS |
| Runtime 六层、run/queue/session/stop | C06 | 只冻结 SUT 与选择观察面 | PASS |
| 评估系统、task、trial、trajectory、grader、hard gate、environment outcome | C07 | 本章唯一主定义 | PASS |
| 训练角色、双三角、干预与轮次 | C08 | 只输出失败、基线、rubric 与限制 | PASS |
| 生产 SLI/SLO | C20 | 明确不由离线基线替代 | PASS |
| `MAT-L0—MAT-L5` 与认证 | C24 | 明确不授级、不认证 | PASS |
| `AU-L0—AU-L4` | C14 | 未从评测分数推导自主等级 | PASS |

## C06→C07 接口

### 已对齐

1. C06 的六层架构图为 C07 提供组件、信任边界、状态 owner 与观察位置；
2. C06 的消息与执行数据流提供 admission、lane、attempt、queue、receipt、系统/业务终态和恢复语义；
3. C06 的最小可训单体提供 SUT 快照、正常基线、Provider/Queue/Node 故障、停止与恢复前置条件；
4. C07 正确保留 `Workspace ≠ Sandbox`、`Binding ≠ Authorization`、`agent.wait timeout ≠ run stop`；
5. C07 没有把日志、span、工具返回或 accepted 状态冒充 environment outcome。

### 保留边界

C06 的真实 Runtime 实践证据与 C07 的目标环境 exporter 探测仍是独立实践问题。C07 只能规定适配器要保存什么，不能因为固定文档存在就宣称目标部署已经可观察。

## C07→C08 接口

### 已对齐

- C08 正确消费 frozen eval spec、task/trial、baseline、rubric、失败分布、留出和硬门；
- C08 不允许导师修改 grader、读取隐藏答案或兼任最终裁判；
- C08 的单变量实验保留全部 trial、失败、回归、留出、安全硬门和回滚；
- C08 没有用训练集 6/6 覆盖 holdout 4/5 与 safety 2/3；
- C08 没有从训练结果推导 `AU-Lx` 或 `MAT-Lx`。

### 已关闭的章际冲突：四层数据 vs 安全套件

C07 的正式定义是：training、regression、holdout、real_world 为四个规范数据层；normal、boundary、abnormal、adversarial、long_running 为横切场景。安全样本可以形成专项套件，但每个样本仍应有自己的数据层与场景，不成为第五层，也不能替代 real_world。

C08 原先存在以下冲突：

- 章首把 C07 输入写成“训练/回归/留出/安全集”；
- 8.8.1 标题为“四类数据集”，正文第四项是安全集，把 real_world 退到句末；
- CASE-A 将 train/regression/holdout/safety 称为“相同四类数据”。

本轮已完成以下最小修补：

1. 章首改为“C07 的四层数据、五类场景、横切安全套件、grader 与硬门”；
2. 8.8.1 明确“四层数据 + 横切安全套件”，安全样本绑定 layer 与 adversarial/abnormal 等场景；
3. CASE-A 将 train/regression/holdout/safety 明确称为运行分区与切片，不称规范四层；
4. 三件母产物、两项练习、README、证据账本与作者运行摘要均同步；
5. 合成 harness 为每条记录输出 `canonical_data_layer`、`scenario`、`suite_memberships`，三个 safety 样本均为 `holdout × adversarial`，并显式声明 `real_world_samples_in_fixture: 0`。

该 P0-02 章际一致性问题现已关闭，不否定 C07 的定义，也不把 C08 的合成结果外推到 real_world。C08 的独立实践记录仍因 harness 字节变化保持 `regression_required`；这不阻断概念交叉门，但阻断其独立实践门自动晋级。

## 三平台映射

| 平台 | 证据身份 | C07 可使用 | 禁止推断 | 结论 |
| --- | --- | --- | --- | --- |
| OpenClaw | 固定 v2026.9.6/eb377ac | run/lifecycle、工具、消息、Session、OTel 观察面及其缺失信号 | 目标环境已启用、日志完整、wait timeout 已停 run、消息已真实送达 | PASS |
| Hermes | 固定 release + 2026-09-30 动态官网 | profile/HERMES_HOME、session DB/history/export/log 的适配语义 | 把动态字段回填 v0.20.1；伪造 OpenClaw runId/lane/span | PASS WITH LIMITATION |
| Muse | VENDOR-CLAIM | 用户可见 Goals、Activity/Artifacts、审批、权限与安全体验镜面 | 内部 task/trial/trace/grader schema、独立效果、可导出审计完整性 | PASS WITH LIMITATION |

平台实现没有被写成通用原理，平台日志也没有替代环境终态。三平台共同结论保持在证据语义层，没有做平台优劣比较。

## 仿生边界

| 四段 | 核查 | 结论 |
| --- | --- | --- |
| 人类现象 | 体检、考试与职业胜任解释单次高分的局限 | PASS |
| 工程映射 | task/trial、四层五场景、grader、trajectory/artifact/outcome 映射清楚 | PASS |
| 训练启示 | 基线、多次 trial、迁移、裁判仲裁与未见留出均落到动作 | PASS |
| 比喻边界 | 明确否定身体、疾病、感受、自我意识和人格责任外推 | PASS |

仿生段没有用拟人化削弱权限、审计、停止和人类责任，也没有把“评测意识”写成 Agent 主观考试焦虑。

## 三件母产物与下游可消费性

| 母产物 | 数量/定位 | C06 输入 | C08 消费 | 结论 |
| --- | --- | --- | --- | --- |
| A-C07-01 评测蓝图 | 唯一文件 | SUT、数据流、停止恢复 | eval spec、task catalog、rubric、hard gate | PASS |
| A-C07-02 基线报告 | 唯一文件 | run/环境/终态字段 | baseline、failure distribution、全部 trial | PASS |
| A-C07-03 裁判校准表 | 唯一文件 | 可观察字段与环境验证 | reviewer 独立、disagreement、grader 版本 | PASS WITH LIMITATION：真实校准未执行 |

原始运行材料、练习和 review 文件均正确作为支撑材料，没有伪装成第四件母产物。

## 15 项 P0 交叉结论

| P0 | 结论 | 交叉审校说明 |
| --- | --- | --- |
| P0-01 | PASS | 7.1—7.8、导航、案例、仿生、工程、人/Agent、跨平台、失败、练习、验收、交接完整。 |
| P0-02 | PASS | C07/C08 已统一四个规范数据层；security/red-team 为横切非补偿套件，不替代 real_world。 |
| P0-03 | PASS WITH LIMITATIONS | 20 条 claim 闭合；开放事实未静默升级。 |
| P0-04 | PASS WITH LIMITATIONS | 固定版本与动态文档已拆分；目标环境仍待实践。 |
| P0-05 | PASS（设计） | 停止、对账、恢复和重跑合同完整；真实可执行性不由本审校批准。 |
| P0-06 | PASS | 评测动作不扩大生产权限；Sandbox、Approval、Policy 和文字合同未互相替代。 |
| P0-07 | REVIEW_REQUIRED | 作者合成基线可复跑，但两项练习尚待独立实践者执行。 |
| P0-08 | PASS | 仿生四段与人格/意识边界完整。 |
| P0-09 | PASS WITH LIMITATIONS | OpenClaw 固定、Hermes 固定/动态、Muse 厂商声明分层正确。 |
| P0-10 | PASS | CASE-A/B/C 与 real_world 合成层均明确是教学/合成，不冒充客户业绩。 |
| P0-11 | PASS | Agent YAML 可解析式，UNKNOWN 到 REVIEW_REQUIRED，不含未授权生产动作。 |
| P0-12 | PASS | 四项开放问题、数据外推与真实 grader 缺口均公开。 |
| P0-13 | PASS | 五项确认硬失败均为 FAIL；安全失败不可被平均或多数票覆盖。 |
| P0-14 | PASS | 三件母产物可定位、可打开，并有明确 C06 输入与 C08 输出字段。 |
| P0-15 | PASS | 无领先/提升结论；比较纪律保留同任务、预算、边界和全部运行。 |

## 本轮修补与未修补

已在 C07 内修补：D19 MAT 术语、Hermes 固定/动态 claim 分层、失效的未用来源、账本计数、C08 安全套件接口和变更记录。

经总编明确授权，已修补 C08 的正文、三件母产物、练习、README、证据账本、作者运行说明与合成 harness 的层/场景语义。未改变任何样本、期望答案、分数、失败分布或终局决定；未把 safety 计数并入普通 holdout 计数；未伪造 real_world 样本；未批准 C08 的事实、实践、编辑或总编门。C08 的独立实践记录保留原复现哈希并明确标为修补前快照，要求非作者回归。

## 交叉门决定

```text
C07 internal definition consistency: PASS
C06 -> C07 interface: PASS
C07 platform boundary: PASS WITH LIMITATIONS
C07 bionic and MAT/AU terminology: PASS
C07 -> C08 whole-book consistency: PASS
Overall cross gate: PASS_WITH_LIMITATIONS
Chapter status: drafting
```

本文件不是编辑总审，不给出版分数，不批准 `release_candidate`。

---
review_id: C16-independent-cross-review-20260930
chapter_id: C16
review_type: independent-cross-chapter-cross-platform-review
reviewer_role: non-author-cross-reviewer
verified_on: "2026-09-30"
chapter_status: drafting
cross_gate: REVIEW_REQUIRED
fact_gate_ref: "review/fact-check.md"
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C16 独立跨章与跨平台审校

## 裁决

**交叉门：`REVIEW_REQUIRED`。** 章节主结构与定义权总体通过：正式 `depends_on` 精确为 `[C03,C04,C06,C09,C14]`；任务拓扑先于组织；六模式不构成成熟度顺序；六类隔离、四类责任、同源共识限制、同合同净收益、C17/C18 定义权、C14 受限消费均清楚；正文只有 16.1—16.7，恰好三件母产物、两项练习，CASE-A/B/C、仿生四段和工程真相齐全。

当前唯一交叉阻塞项是 D22 数据谱系：作者 README 明确声明全部为纯合成离线夹具，但输入把三个合成 scenario 标为 `representative-real-world`，展开后共 9 个 trial。runner 不验证来源、不保留空的真实层，也不派生 `representative_real_world_executed=false/count=0`。因此保存的 45-trial 计数可重复，却不能满足本书“四层 + 横切安全”的来源真实性约束。此项为 `P1-X16-01`；不会倒推作者伪造真实线上效果，但必须在交叉门前关闭。

[事实门](fact-check.md)另有两个 P0 需要作者修复。本记录没有修改正文、ledger、产物、练习或作者 runs，不批准实践、编辑、总编或 RC。

## 结构与定义权核对

| 核对项 | 证据位置 | 结论 |
| --- | --- | --- |
| 正式依赖拓扑 | chapter frontmatter | PASS：精确为 `[C03,C04,C06,C09,C14]`，无静默新增正式依赖。 |
| 任务拓扑先于组织 | 16.1—16.2、A-C16-01 | PASS：先建立单体/Workflow 基线，再画节点、边、共享状态、关键路径与恢复关系。 |
| 六模式非成熟度 | 16.3 | PASS：管道、监督者、委员会、市场、黑板、混合按场景选，不与 `MAT-Lx` 或人数排序。 |
| 六面隔离 | 16.4 | PASS：身份、会话、上下文、Workspace、权限、凭证分别核验，且明确不能互相推导。 |
| 四类责任 | 16.5、A-C16-02 | PASS：主理、专家、执行、评审的责任、禁区、证据和 owner 分开；批准者没有被偷换成 Agent 角色。 |
| 同源共识 | 16.1、16.3、16.4、红队 | PASS：相同模型/来源/摘要的多数意见不作独立事实证明。 |
| 同任务同预算净收益 | 16.6—16.7、A-C16-03 | PASS：比较任务、输入、工具权限、总预算、风险、验收、人工与恢复；硬失败非补偿。 |
| C14 受限消费 | 章首、16.2、16.5、16.7 | PASS WITH LIMITATION：只消费 `AU-L0—AU-L4`、授权与委托衰减；C14 仍为 drafting，实践/编辑/总编/RC未签，C16没有写成已通过。 |
| C17 定义权 | 章首、16.2、16.7、A-C16-01 | PASS：C16只交节点、边、join、取消/恢复需求；路由、让位、Handoff、取消、并发与合并协议交 C17。 |
| C18 定义权 | 章首、A2A镜面、产物交接 | PASS：只说明互操作需求；A2A对象、跨系统身份、信任与产物协议交 C18。 |
| 多Agent效果外推 | 16.3、16.6—16.7 | PASS：Anthropic公开结果被限定到研究场景；没有宣称普遍提效或“Agent越多越强”。 |
| 结构范围 | H2/H3、目录 | PASS：只有 16.1—16.7；artifacts 恰好 A-C16-01/02/03；exercises 恰好 X-C16-01/02。 |
| 三案与仿生 | 开场、16.1、16.2、16.7 | PASS：CASE-C贯穿，CASE-A/B为拒绝拆分反例；人类现象/工程映射/训练启示/比喻边界齐全。 |
| 工程真相 | 16.5 | PASS：“组织图不执行边界”把人格/角色文字与系统强制控制分开。 |

## 上下游接口核对

### C03 / C04 / C06 / C09 / C14 → C16

- C03：消费七维中的公平比较、预算向量、失败分布与领先声明边界；没有重新定义七维或认证阈值。
- C04：角色由岗位任务域和能力节点生成；模型名、人格、工具名不能倒推岗位。
- C06：Runtime、Session、Workspace、Sandbox、Queue、Channel、Tool 等只作为运行边界消费；没有把 workspace/session 当 sandbox。
- C09：总体完成要求过程、产物、效果证据和环境终态；spawn、announce 或 UI done 没有被当业务完成。
- C14：角色不授予权限；委托只衰减；拓扑变化触发再认证。C16 明确保持 C14 实践门未决，不以作者夹具替代真实授权验证。

### C16 → C17 / C18 / C23

- A-C16-01 输出任务节点、依赖边、共享状态、关键路径、并行候选、join 与取消/恢复需求；没有发布 Handoff schema、ACK 或并发状态机。
- A-C16-02 输出角色、身份、权限、凭证、产物与责任要求；不签发 authorization 或 trust。
- A-C16-03 输出净收益向量、失败分布和拆分/合并/降级建议；不发布 C20 SLO 或 C24 认证阈值。
- C17 preflight 仍把 C16 标成“作者包可受限消费、独立门禁待完成”，与当前状态一致。
- C18 preflight 把组织角色/责任作为输入，保留 A2A 对象、协议状态、身份、信任和产物契约定义权，C16 没有越权。

## D22 数据谱系阻塞项

### 观察

[作者运行说明](runs/README.md)声明“输入采用 JSON 语法的 YAML 文件，无真实身份、凭证、网络或外部写入”，即全部数据为安全合成夹具。但 [输入](runs/synthetic-organization-input.yaml) 中以下三个 scenario 使用 `layer: representative-real-world`：

- `multi-negative-benefit`；
- `lead-lost`；
- `a2a-runtime-unverified`。

每项重复三次，所以 [结果](runs/synthetic-organization-results.yaml) 与摘要产生 9 个所谓 representative-real-world trial（3 FAIL、6 REVIEW_REQUIRED）。runner 只复制字符串并汇总，不验证环境，也没有 `synthetic_shadow`、`intended_target_layer`、`representative_real_world_executed` 或空层占位。

### 判定

`P1-X16-01 / REVIEW_REQUIRED`：这不是把 45-trial 计数变成假数据，结果和摘要确实可确定复算；问题是“合成影子样本”不能占用代表性真实任务层。安全切片可以横跨 training/regression/holdout/representative real-world，但不能成为第五层，也不能让合成数据冒充真实环境。

### 最小关闭合同

1. 将三个纯合成场景放回 `holdout`，增加 `synthetic_shadow: true` 与 `intended_target_layer: representative_real_world`；或采用与 D22 注册表一致的等价受控字段。
2. runner 必须从环境/来源字段派生 `representative_real_world_executed=false`、`representative_real_world_count=0`，并在结果中保留空的规范真实层。
3. 对以下两类负向突变硬失败：合成样本改标 `representative_real_world`；`executed=true` 但 count 为 0 或没有真实环境证据。
4. README、正文 E-C16-022/023 附近、作者自检、results 与 summary 同步，明确当前未执行 representative real-world。
5. 保留 45 trial 的既有失败分布可以作为合成控制结果，但不得用它关闭真实任务/平台实践；修复后由非作者做 fresh-temp 双运行和负向突变回归。

## 15 项 P0 清单

| 质量门 | 结论 | 说明 |
| --- | --- | --- |
| P0-01 模板/目录 | PASS | 16.1—16.7、章首、交接、三产物、两练习完整。 |
| P0-02 概念所有权 | PASS | C16组织定义与C17/C18协议、信任定义权分离。 |
| P0-03 事实标签/来源 | **REVIEW_REQUIRED** | Muse `swarms/subagents` 当前 ledger source 不支持；见事实门。 |
| P0-04 固定版本字段 | **REVIEW_REQUIRED** | `agents.list[].subagents.allowAgents` 应为 `agents.entries.*...`；见事实门。 |
| P0-05 停止/恢复 | PASS（设计） | 十类失败、停止、接管、恢复、降级齐全；真实平台未跑。 |
| P0-06 权限/审批/隔离 | PASS | 组织名、Binding、session、人格均不产生授权；六面隔离分开。 |
| P0-07 基线/证据/验收 | REVIEW_REQUIRED（实践未审） | 作者合成结果可复算；独立两练习和真实任务未执行，D22谱系另有P1阻塞。 |
| P0-08 仿生边界 | PASS | 四段完整，明确不证明社会主体性。 |
| P0-09 平台证据边界 | PASS WITH FACT FIX | 三平台层级未混同；Muse具体来源仍需修复。 |
| P0-10 案例/隐私/授权 | PASS | 三案均明确教学合成，零真实客户/凭证/外发。 |
| P0-11 Agent机器块 | PASS | YAML机器块可解析，不含未授权外发或扩大权限。 |
| P0-12 冲突/伪引用/隐藏缺口 | **REVIEW_REQUIRED** | Muse source mismatch 尚未处理；其他 UNKNOWN 已显式。 |
| P0-13 安全硬门 | PASS | 越权、泄露、重复副作用、不可恢复失败不可被平均收益抵消。 |
| P0-14 产物可定位 | PASS | 三件母产物均存在且被章际交接消费。 |
| P0-15 领先/提升声明 | PASS | 所有效果句均限定任务、版本、预算、风险、失败与未知；无普遍领先结论。 |

## 问题分级

### P0（由事实门阻塞）

1. `P0-F16-01`：OpenClaw 固定字段路径错误。
2. `P0-F16-02`：Muse claim 与 ledger source 不闭合。

### P1（由交叉门阻塞）

1. `P1-X16-01`：纯合成样本冒充 `representative_real_world`；按上述最小关闭合同修复并复跑。
2. `P1-F16-03`：A2A 1.0 的 source identity 应从 `/latest/` 固定到 `/v1.0.0/`。该项不改变当前语义，但应在出版追溯门关闭。

### P2

1. `P2-F16-04`：将“45 个唯一 task/trial”改成“15 task、45 unique trial_id”，避免把重复 trial 误写成独立任务数。
2. `P2-X16-02`：修复后建议在 A-C16-03 明列 `real_world_evidence_count: 0`，让下游 C23/C24 不必从 prose 推断证据缺口。

## 评分

| 维度 | 得分 | 说明 |
| --- | ---: | --- |
| 论证与结构 | 14/14 | 从负选择、拓扑、模式、隔离、责任、协作税到净收益形成连续链。 |
| 事实准确与证据 | 14/18 | 25条双向闭合，但 OpenClaw 字段和 Muse source 两项 P0 阻塞。 |
| 概念边界与章际接口 | 14/14 | C03/C04/C06/C09/C14输入与C17/C18输出边界清楚。 |
| 实践与可复现性 | 9/14 | 45-trial可确定复算；D22谱系不合格，独立实践与真实平台未跑。 |
| 安全与治理 | 14/14 | 权限、凭证、硬门、接管、UNKNOWN与责任 owner 完整。 |
| 案例、仿生与双视图 | 12/12 | CASE-A/B/C、四段仿生、人类/Agent视图齐全。 |
| 产物与可交付性 | 12/14 | 三件产物可用；下游仍需真实层显式0和谱系修复。 |
| 总分 | **89/100** | 内容质量高，但存在事实 P0 与数据谱系 P1，不能据分数越过门禁。 |

## 门禁声明

交叉门保持 `REVIEW_REQUIRED`，直至两项事实 P0 与 `P1-X16-01` 关闭并由非作者回归。C14 的事实/交叉记录可受限消费，但其实践、编辑、总编与 RC 仍未签；C16 不得据此宣称授权已在真实平台验证。本记录不批准 C16 实践、编辑、总编或 `release_candidate`。

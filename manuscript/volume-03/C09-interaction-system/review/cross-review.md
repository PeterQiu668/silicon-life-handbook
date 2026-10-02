---
review_id: C09-independent-cross-review-20260930
chapter_id: C09
review_type: independent-cross-platform-cross-review
reviewed_on: "2026-09-30"
reviewer_role: cross-reviewer
chapter_status: drafting
cross_gate: passed_with_limitations
fact_review_ref: "review/fact-check.md"
practice_gate: not_reviewed
editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C09 跨章与跨平台审校

## 1. 结论

C09 的定义权、9.1—9.8、三件母产物、C07/C08 上游输入，以及 C10/C13/C18/C19 下游接口总体对齐。任务卡、上下文包与交付证据包保持为平台无关工作合同；OpenClaw、Hermes、Muse 没有被伪造成同构系统；`AU-L0—AU-L4` 与 `MAT-L0—MAT-L5` 没有混用。

交互完成性同时保留三层证据：**技术执行**、**交付/目标端可见**、**业务验收与环境终态**。四轴状态进一步分离任务、消息、Artifact、环境终态。UI 成功、工具 success、子 Agent `done`、协议终态或通知已发均不能覆盖产物缺失、环境未变、业务未验收、过期上下文、跨主体敏感内容与群聊污染。

交叉门结论为 **`PASS WITH LIMITATIONS`**。限制来自 C13/C18/C19 尚只有 preflight、真实 Runtime 与独立实践尚未完成；本审校不执行或修改作者实践记录，不批准实践、编辑、总编或 RC。

## 2. 单一概念所有权

| 对象 | 定义中心 | C09 行为 | 结论 |
| --- | --- | --- | --- |
| 岗位、JTBD、能力、风险、负面清单 | C04 | 把上游字段实例化为任务，不重做岗位模型 | PASS |
| 三证法 | C03 | 将过程—产物—效果包装进一次工作交付，不重定义上位原则 | PASS |
| task/trial/grader、四层数据与硬门 | C07 | 引用评测与证据要求，不建立平行评测体系 | PASS |
| 训练计划、轮次、导师与训练候选 | C08 | 只输出反馈候选和训练引用，不把生产记录自动变成样本 | PASS |
| 任务卡、上下文包、工作交互与反馈入口 | C09 | 本章唯一主定义 | PASS |
| Context/Memory 生命周期 | C10 | 明确交给 C10；上下文包不等于长期 Memory | PASS |
| 信号、Heartbeat、Cron、自动化状态机 | C13 | 只提供任务合同、检查点与终态，不定义触发器 | PASS |
| 自主等级 | C14 | 只引用 `AU-L0—AU-L4`，不授级、不扩权 | PASS |
| 路由、让位、handoff ACK、并发 | C17 | 只形成待交接输入；不定义协议 | PASS |
| A2A Task/Message/Event/Artifact/Agent Card | C18 | 只借外部规范校准对象分离；不改名占有定义权 | PASS |
| 身份、权限、沙箱、注入防御与安全模型 | C19 | 只识别污染、停止、隔离和升级；不以文本代替强制控制 | PASS |
| 成熟度与认证 | C24 | 只引用 `MAT-L0—MAT-L5`，不认证 | PASS |

## 3. 9.1—9.8 与正式框架

| 节点 | 交叉结论 | 说明 |
| --- | --- | --- |
| 9.1 任务卡 | PASS | 目标、范围、输入、输出、业务/环境终态、时间、风险、权限、停止、回滚和反馈许可齐全；聊天不产生授权。 |
| 9.2 AI 原生协作面 | PASS | 人、Agent、项目、状态、批准、Artifact 和环境读回同面呈现；展示层与合同层分离。 |
| 9.3 上下文包 | PASS | 来源、版本、时效、敏感性、权利、污染、冲突与更正完整；不把 Session/Workspace/群聊全文当最小上下文。 |
| 9.4 四轴状态 | PASS | 任务、消息、Artifact、环境终态不可合并；UNKNOWN 映射 REVIEW_REQUIRED；A2A 定义权留给 C18。 |
| 9.5 检查点 | PASS | 就绪、假设、风险/批准、进度、预提交、交付检查点含停止、升级、交回与安全等待。 |
| 9.6 交付三证 | PASS | 过程、产物、效果分别承载技术执行、交付可见与业务/环境验收；执行者不得自批。 |
| 9.7 生产反馈 | PASS | 许可、最小化、去标识、权利、去重、污染和目的地门完整；反馈只成为候选。 |
| 9.8 综合镜头 | PASS WITH LIMITATION | 仿生四段、人类/Agent 双视图、三平台与完整运行算法齐全；平台实跑仍待实践门。 |

框架 v2 的正式正文节点为 9.1—9.7；9.8 是质量标准要求的综合镜头，没有另造主定义或第四件母产物。

## 4. D21 三层完成性与四轴状态

| 层/轴 | C09 载体 | 允许声明 | 不足时 |
| --- | --- | --- | --- |
| 技术执行 | 过程证据、工具/策略事件、attempt、失败、重试、成本 | 某次调用/运行发生且结果可定位 | 不得推出已交付或业务完成 |
| 交付/目标端可见 | 消息状态、Artifact 状态、接收端可用、版本/哈希/渲染 | 产物存在、正确版本可被目标方取得 | 消息已接收或 UI success 不得掩盖缺失/错版 |
| 业务验收与环境终态 | 独立读回、回执、对账、监控、受影响主体确认 | 任务卡预先声明的终态达到 | 缺读回最高 REVIEW_REQUIRED；读回证实错误则 FAIL |
| 任务状态 | 工作合同阶段和有权验收 | submitted/accepted 等阶段 | Agent 自报 completed 不能自批 accepted |

四层关系没有被压成单一“完成”字段。CASE-B 区分草稿、批准、发送、渠道投递与 CRM；CASE-C 明确 PR 是 Artifact/消息层、测试是技术环境层、用户验收是业务层。结论：`PASS`。

## 5. 错误状态、过期上下文与污染硬门

| 风险 | 正文/产物行为 | 结论 |
| --- | --- | --- |
| UI 假完成 | Artifact missing + environment unchanged => FAIL | PASS |
| 工具/消息 success | 只更新调用或消息证据，必须独立读回 | PASS |
| 外部状态 UNKNOWN | 先对账，不盲重试；最终 REVIEW_REQUIRED | PASS |
| 过期上下文未消费 | CP-READY 暂停、补当前版本、新包新版本 | PASS |
| 跨主体敏感内容已消费 | 隔离、清理副本、通知 data owner、影响评估，硬 FAIL | PASS |
| 完整群聊摄入 | 最小化/权利/污染门阻断；已消费为 FAIL | PASS |
| 留出答案/规则污染 | 作废受影响 trial，交 C07 重建留出 | PASS |
| 子 Agent `done` | 父任务需合并、版本和父级终态证据 | PASS |

错误状态不会被 UI 成功或顺滑文本覆盖。安全、权限、隐私、污染和伪造证据均不可由总分补偿。

## 6. 上游接口

### 6.1 C07→C09

C09 的 task card 引用 `evaluation_ref`，交付包引用 task/trial、rubric、grader、完整 attempt、失败分布和独立 reviewer；没有重定义 C07 的四个规范数据层、五类场景或 security/red-team 横切切片。生产反馈进入评测候选前继续做留出答案、grader 规则和跨 trial 状态污染检查。

结论：`PASS`。C07 的真实人类/专家 grader 校准和 C09 的真实交付复跑仍是各自实践限制，不能互相代签。

### 6.2 C08→C09

C09 只在训练任务中引用 C08 计划/轮次，并把真实工作反馈交成带许可、来源、脱敏、污染、失败和目的地的候选；不让生产好评直接成为标签，不让反馈直接写 Memory/Skill/训练集，也不把 C08 合成训练结果写成真实能力。

结论：`PASS WITH LIMITATION`。C08 X-C08-02 和总实践门仍为 `REVIEW_REQUIRED`，C09 不得消费其结果为已验证生产训练系统。

## 7. 下游接口

### 7.1 C09→C10

C09 提供 task version、最小上下文、来源/时效/敏感性/用途、反馈许可、候选字段、纠错和删除请求；C10 保持 task state 为任务系统权威，并重新执行写入、保留、检索、更正与删除门。C10 正式事实/交叉审校已确认该接口对齐。

结论：`PASS`。

### 7.2 C09→C13

C13 preflight 明确消费 C09 的任务卡、上下文包、交付三证与四轴终态：触发、调度、运行、投递与环境终态分开；通知或 scheduler success 不证明任务完成。C09 没有提前定义 Heartbeat/Cron/Hook/Webhook/Standing Order、安静策略或自动化状态机。

结论：`PASS WITH LIMITATION`。C13 尚未形成正式章节包，正式三件母产物冻结后需回归 task/context/checkpoint/delivery 引用字段。

### 7.3 C09→C18

C09 明确自己的 Task Card、Message/Artifact 状态表与 A2A 对象非同义，并把业务任务卡映射需求交给 C18。C18 preflight 已坚持协议终态不等于业务终态，要求协议状态、轨迹/权限、产物验收和环境对账共同支持交付。

结论：`PASS WITH LIMITATION`。C18 正式状态机、Artifact envelope 与 Agent Card 审查表尚未冻结，后续必须回归状态映射、取消、事件与信任字段。

### 7.4 C09→C19

C09 输出跨主体/群聊/留出污染事件、已消费范围、隔离状态、停止/回滚、权限证据引用和残余 UNKNOWN；它没有用 prompt、任务卡、上下文包、AU/MAT 或人格文本授予权限。C19 继续主定义身份、委托、凭证、Sandbox、Policy、Approval、注入防御、事件响应和强制控制。

结论：`PASS WITH LIMITATION`。C19 正式威胁模型和 incident handoff 尚未冻结；真实缓存清理、Provider 数据路径与删除覆盖仍需 C19/C21 和实践门关闭。

## 8. 三平台映射

| 平台 | 证据层 | C09 使用方式 | 禁止外推 | 结论 |
| --- | --- | --- | --- | --- |
| OpenClaw | 固定 v2026.9.6 / eb377ac | Session、Gateway routing、session-key queue 与四种 queue mode 作为承载面 | Session=任务；Queue=工作流；run 完成=业务完成 | PASS |
| Hermes | 固定 v0.20.1 / v2026.8.13 / f80f453 | Gateway/session persistence、Kanban/review、Artifact attachment、Deliverable channel 作为第二实现 | 与 OpenClaw/A2A 状态同构；通知=终态 | PASS |
| Muse | VENDOR-CLAIM | Goals、Activity、Artifacts、permissions、approval UI 作为公开产品镜面 | 内部状态机、grader、训练回流、独立安全/效果 | PASS WITH LIMITATION |

跨平台共同点停留在对象分离、版本、权利、检查点、三证、停止和回滚；没有伪造同名字段、配置或保证。

## 9. MAT/AU 与 authority

- 只出现 `AU-L0—AU-L4`、`MAT-L0—MAT-L5` 或带前缀的 `AU-Lx`/`MAT-Lx`；
- 未出现裸 `L0—L5` 机器等级；
- 未从 MAT 推导 AU，未从 AU 推导能力或成熟度；
- 未从任何等级、任务卡、上下文包、Memory、Session 或聊天语气生成系统权限；
- 高风险动作继续要求真实身份、scope、approval、policy 与目标系统控制。

结论：`PASS`。

## 10. 三件母产物与可消费性

| 母产物 | 数量/定位 | 核心内容 | 结论 |
| --- | --- | --- | --- |
| A-C09-01 任务卡 | 唯一文件 | 目标、范围、终态、权限、风险、检查点、停止、回滚、回流许可 | PASS |
| A-C09-02 上下文包 | 唯一文件 | 来源、时效、敏感性、权利、最小化、冲突、污染、更正 | PASS |
| A-C09-03 交付证据包 | 唯一文件 | 四轴、过程/产物/效果三证、全部 attempt、验收与反馈候选 | PASS |

`artifacts/` 恰有三件 `A-C09-*`；检查点、升级和状态规则被嵌入，不另造第四件。两项练习和静态运行记录是支撑证据，不是第四件母产物。

## 11. 15 项 P0 交叉结论

| P0 | 结论 | 交叉审校说明 |
| --- | --- | --- |
| P0-01 | PASS | 章首导航、开场案例、9.1—9.8、仿生、双视图、失败、练习、验收和交接齐全。 |
| P0-02 | PASS | C09 只拥有工作交互系统；C07/C08/C10/C13/C17/C18/C19/C24 定义权保留。 |
| P0-03 | PASS WITH LIMITATIONS | 14 条 claim 全闭合；A2A fixed/latest、Muse vendor、local/open question 分层。 |
| P0-04 | PASS WITH LIMITATIONS | OpenClaw/Hermes tag—commit 和固定文档已核；目标部署与真实行为待实践。 |
| P0-05 | PASS（设计） | 检查点、停止、查询外部终态、隔离、回滚、让位和恢复合同完整。 |
| P0-06 | PASS | 任务卡、上下文、聊天、Memory、MAT/AU 均不授予权限；强制控制留给平台/C19。 |
| P0-07 | REVIEW_REQUIRED | 作者静态合成记录内部一致，但本审校没有独立执行两项练习或真实 Runtime。 |
| P0-08 | PASS | 仿生四段完整，明确否定意识、体验、良知和天然责任外推。 |
| P0-09 | PASS WITH LIMITATIONS | OpenClaw fixed、Hermes fixed、Muse vendor claim 分栏且不做同构。 |
| P0-10 | PASS | CASE-A/B/C 与运行记录明确为教学/合成材料，不冒充真实客户或业绩。 |
| P0-11 | PASS | Agent 机器块、账本和运行 YAML 可解析，示例不扩权。 |
| P0-12 | PASS | 真实 Runtime、数据权利、缓存/删除、第二实践者和下游冻结缺口均公开。 |
| P0-13 | PASS | 越权、泄露、跨主体污染、留出泄漏、UI 假完成与伪造证据均为非补偿硬失败。 |
| P0-14 | PASS WITH LIMITATION | 三件产物可定位并被正式 C10 和多个 preflight 消费；C13/C18/C19 正式章冻结后需回归。 |
| P0-15 | PASS | 无平台领先、行业最强或真实能力提升声明；一次合成 PASS 未被外推。 |

P0-07 保留给独立实践门。本结论不把 `REVIEW_REQUIRED` 偷换成 PASS，也不阻断事实/交叉门在其自身范围内给出带限制通过。

## 12. 临时质量评分

按质量标准百分制，在实践门未关闭前给出非 RC 的交叉初评：

| 维度 | 得分/满分 | 依据 |
| --- | ---: | --- |
| 论证与结构 | 13/14 | 从合同、上下文、状态、检查点、三证到回流形成连续主线 |
| 事实准确与证据 | 17/18 | 固定版本、协议、厂商与限制分层；Muse 仍为同源厂商材料 |
| 技术与系统完整性 | 9/10 | 状态、权利、异常、停止和恢复齐全；真实 adapter 未验证 |
| 课程与学习设计 | 11/12 | 三案、反例、两练习与红队完整 |
| 实践与可复现性 | 10/14 | 静态合成记录完整，但无独立真实 Runtime 复跑 |
| 评测与验收 | 11/12 | 三态、硬门、完整失败与独立 reviewer 边界清楚 |
| 安全、治理与伦理 | 8/8 | 最小化、权限、污染、停止和责任边界完整 |
| 仿生解释质量 | 4/4 | 四段完整且边界明确 |
| 中文出版表达 | 4/4 | 语言清晰，案例连续，无明显口号堆叠 |
| 人机双读与章际接口 | 4/4 | 人/Agent 入口、机器块和主要接口可消费 |
| 合计 | **91/100** | 仅为交叉初评；P0-07 未关闭，不能据此进入 RC |

## 13. 问题清单

### P0

无未关闭的事实/交叉 P0。`P0-07` 属独立实践门，当前为 `REVIEW_REQUIRED`。

### P1

1. C13/C18/C19 仍是 preflight，正式章冻结后必须做字段级回归；尤其是自动化终态、A2A 状态映射、污染事件与 incident handoff。
2. 真实 OpenClaw/Hermes Runtime、目标渠道和环境读回尚未复跑，不能把模板可表达升级为平台可强制。
3. 反馈许可、Provider 缓存、删除证明和跨主体事故通知仍需 data/security owner 关闭。
4. A2A `latest` 页面会漂移；印前必须以固定 `v1.0.1` 来源为历史锚点并重验动态页。

### P2

1. frontmatter 的 canonical `feeds_into` 继续遵循章节卡；C13/C18/C19 属本次额外接口复核，不建议为凑消费者列表改写上位合同。
2. Hermes Deliverable 固定文档说明缺失文件可能被静默跳过，后续实践宜专门验证“通知文本成功但附件缺失”的目标端读回。

## 14. 本轮修改边界

- 新增本事实核查与交叉审校记录；
- 只对 A2A 固定规范锚点、Hermes tag—commit 已验证事实做最小 chapter/ledger 补丁；
- 未编辑 artifacts、exercises、作者运行记录或实践评审材料；
- 未改变 `drafting`、未批准实践/编辑/总编门、未授权 RC。

## 15. 交叉门决定

```yaml
cross_gate:
  chapter_id: C09
  verdict: PASS_WITH_LIMITATIONS
  concept_ownership: PASS
  completion_three_layers: PASS
  four_axis_state: PASS
  stale_cross_subject_group_pollution_hard_gates: PASS
  upstream:
    c07_to_c09: PASS
    c08_to_c09: PASS_WITH_LIMITATION_PRACTICE_PENDING
  downstream:
    c09_to_c10: PASS
    c09_to_c13: PASS_WITH_LIMITATION_DOWNSTREAM_NOT_FROZEN
    c09_to_c18: PASS_WITH_LIMITATION_DOWNSTREAM_NOT_FROZEN
    c09_to_c19: PASS_WITH_LIMITATION_DOWNSTREAM_NOT_FROZEN
  platform_mapping: PASS_WITH_LIMITATIONS
  mat_au_separation: PASS
  practice_approved: false
  editor_approved: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

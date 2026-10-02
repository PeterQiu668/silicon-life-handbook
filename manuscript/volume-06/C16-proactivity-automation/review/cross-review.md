---
review_id: C13-independent-cross-review-20260930
chapter_id: C13
review_type: independent-cross-chapter-cross-platform-review
reviewed_on: "2026-09-30"
reviewer_role: cross-reviewer
chapter_status: drafting
cross_gate: pass_with_limitations
fact_gate_ref: "review/fact-check.md"
practice_gate: not_reviewed
editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C13 跨章与跨平台一致性审校

## 1. 裁决

C13 的主定义权、13.1—13.8、三件母产物、D21 三层完成、D22 四层加横切安全、三道门、UNKNOWN 处置、sentinel 故障域和 C09 补充接口均闭合。章节没有重定义 C14 授权、C19 安全、C20 生产 SLO 或 C21 发布恢复，也没有让 OpenClaw/Hermes/Muse 字段伪装同构。

交叉门判 **`PASS WITH LIMITATIONS`**。限制一是事实门记录的 Standing Order 产品措辞需要消歧；限制二是 C14、C22 的既有 preflight 仍保留“C13 正式包不存在/只有 preflight”的旧状态，下游正式写作前必须刷新。两项都不改变 C13 的控制结构，但前者阻断事实门，后者是跨章集成待办。本审校不执行实践、不签编辑/总编/RC。

## 2. 定义权与章际接口

| 对象 | 主定义章 | C13 的合法行为 | 裁决 |
| --- | --- | --- | --- |
| 七契约与 HEARTBEAT 契约语义 | C05 | 消费观察、安静、提案/行动、冷却、熔断和恢复意图 | PASS |
| Gateway/Session/Queue/Delivery/Runtime | C06 | 绑定 trigger、state owner、run、delivery、stop/recovery 证据 | PASS |
| 评测三态、数据层、失败分布 | C07 | 使用 PASS/FAIL/RR 与四层数据，不重定义 grader | PASS |
| 训练干预与候选发布 | C08 | 只把指标异常变成训练候选，不在线自改规则 | PASS |
| task/context/delivery evidence | C09 | 作为补充接口消费任务与交付证据，不改变 C09 正式依赖拓扑 | PASS |
| Context/Memory/Record/Evidence | C10 | 读取当前背景与撤回；运行态、旧批准不晋升 authority | PASS |
| Tool/MCP contract | C11 | 消费幂等、timeout、retry、cancel、compensation、receipt | PASS |
| Skill/Plugin/Hook 供应链 | C12 | Hook 只取生命周期语义，供应链版本仍归 C12 | PASS |
| 自主等级与授权 | C14 | 输出 actor/action/target/scope/timebox/approver 请求参数，不授 AU、不造 authority | PASS |
| 完整安全与信任边界 | C19 | 输出 Hook/Webhook/replay/外发/故障域攻击面，不重写 IAM/威胁模型 | PASS |
| SLI/SLO、错误预算、事故响应 | C20 | 输出事件、局部指标和失败样本，不把局部指标命名为生产 SLO | PASS |
| 发布、恢复与退役 | C21 | 输出版本、检查点、未知效果、恢复前置，不宣称恢复完成 | PASS |
| 训练营 | C22 | 输出三触发、静默、去重、故障与恢复练习 | PASS WITH STALE-PREFLIGHT LIMITATION |

## 3. C09 补充接口

C13 frontmatter 的硬依赖仍严格保持章节卡的 `[C05, C06, C10, C11]`，没有私自把 C09 升成正式依赖；同时通过 `supplementary_interfaces: [C07, C09, C12]` 公开正文实际消费的 task/trial、交付三层与能力版本接口。章首又明确“补充消费接口不改变定义权”。

该处理与 C09 自身 `feeds_into` 未列 C13 的现状兼容：它是补充读取，不是新主干边。C13 对 C09 的消费仅限 task card、context package、checkpoint/escalation 和 delivery evidence；没有重新定义任务卡、四轴终态、反馈准入或交互系统。

结论：`PASS`。

## 4. 13.1—13.8 与生产合同

| 检查项 | 结论 | 说明 |
| --- | --- | --- |
| 正文核心节点 | PASS | 恰好出现 13.1—13.8 八个 H2，不增 13.9。 |
| 三件母产物 | PASS | artifacts 目录恰好 A-C13-01/02/03；练习和 runs 未冒充第四件。 |
| 13.1 信号与三道门 | PASS | trigger eligibility、authorization eligibility、net-value eligibility 分开。 |
| 13.2 Heartbeat | PASS | 观察节律、安静与固定 OpenClaw system-owned Heartbeat 边界清楚。 |
| 13.3 Cron/Event/Queue/Manual | PASS | 时间、变化、背压、人工优先输入均不产生 authority/completion。 |
| 13.4 Hook | PASS | 内部生命周期、阻塞、宿主信任边界、可发现不等于触发。 |
| 13.5 Webhook | PASS | 外部输入、签名/时效/tenant/replay/queue/read-back 闭合。 |
| 13.6 Standing Order | PASS WITH FACT LIMITATION | 持续意图、复核、到期、停止正确；厂商 `permanent authority` 术语待事实消歧。 |
| 13.7 安静与状态机 | PASS | 清醒、判断、等待、运行、暂停、熔断、恢复、终态可追踪。 |
| 13.8 指标与低噪音 | PASS | 有效提案、噪音、遗漏、延迟、升级、完整交付和故障隔离为局部指标。 |

## 5. 三个关键不等式与完成模型

正文、三件产物和两项练习一致执行：

```text
trigger ≠ authority ≠ completion
scheduler/run success ≠ delivery visibility ≠ business/environment acceptance
raw UNKNOWN ≠ PASS and raw UNKNOWN ≠ permission to replay
```

- trigger 只开始判断；Manual 的人类文字、Webhook 的有效签名和 Standing Order 的存在均不能独自产生当前授权；
- D21 分为技术执行、交付/目标端可见、业务验收/环境终态；无投递要求时需显式 `NOT_REQUIRED`；
- 原始 UNKNOWN 必须先补证或映射 RR，安全硬失败可直接 FAIL；
- stop requested 与 stop confirmed 分开，restart 不被当成 recovered；
- 高价值分数不能平均掉越权、重放、未授权外发、共同失明或其他硬失败。

结论：`PASS`。

## 6. D22、MAT/AU 与硬失败

- 训练与评测数据严格为 `training / regression / holdout / representative real-world` 四层；
- `security/red-team` 明确是横跨四层的非补偿切片，不是第五层，也不替代 representative real-world；
- C13 没有分配 `AU-Lx` 或 `MAT-Lx`，也没有用自动化频率、自主表象或 30-trial 分布推导成熟度；
- 授权仍由 C14 当前可核验 authority evidence 和系统控制裁决；成熟度仍由 C24 认证。

结论：`PASS`。

## 7. Sentinel 与故障域

正文把“独立进程”与“独立故障域”分开，要求 sentinel 不与主系统共享唯一 Gateway、Provider、credential、network 或 datastore 故障组合。状态机、失败模式、红队、X-C13-02 和合成结果都把共同失明作为硬失败，且没有声称全套完全物理隔离。

C13 只定义观察覆盖需求和失败信号，具体隔离等级、fallback channel、威胁与生产 SLO 分别交 C19/C20/C21。作者合成夹具可证明判定规则可表达，不证明真实 sentinel 已隔离。

结论：`PASS WITH PRACTICE LIMITATION`。

## 8. 跨平台一致性

| 维度 | OpenClaw | Hermes | Muse | 裁决 |
| --- | --- | --- | --- | --- |
| 证据身份 | 固定 release/tag/commit 文档 | 固定 release 锚点 + 核验日动态文档 | VENDOR-CLAIM | PASS |
| Heartbeat | system-owned automation + monitor scratch | session heartbeat 动态对照 | 不构造同名实现 | PASS |
| Cron/trigger | 固定 Automations 文档 | 动态 Cron/provider/claim/misfire | schedule/event 只作公开体验 | PASS |
| Hook/Webhook | 固定内部 Hook 与 authenticated ingress | 不伪造 OpenClaw 同构 | 不推断内部入口 | PASS |
| Standing Order | OpenClaw 产品对象 | 不泛化成 Hermes 原语 | 不泛化成 Muse 原语 | PASS WITH FACT LIMITATION |
| 权限 | C14/系统控制，不由 trigger 产生 | 不从动态页倒推出固定 grant | Sentinel 只作厂商声明 | PASS |
| 完成 | D21 三层，需要目标端/环境证据 | 动态页支持 fire/delivery 分离 | UI/通知不等于业务完成 | PASS |

## 9. CASE、仿生与实践声明

- CASE-A/B/C 全部存在，并分别覆盖研究证据雷达、运营队列/客户外发、跨团队项目长期意图；
- 案例明确为合成教学案例，不冒充真实客户、部署或业绩；
- 仿生四段“人体现象—工程映射—训练启示—隐喻边界”完整，明确定时器无欲望、事件无痛觉、状态机无意识、静默不等于睡眠；
- 30-trial 声明与保存结果一致，失败和 RR 分布未删除；
- 作者运行只证明固定离线合同，真实 Heartbeat/Cron/Event/manual、channel、stop、sentinel 和 recovery 保持 RR。

结论：`PASS`；实践门未执行。

## 10. 15 项 P0 交叉结论

| P0 | 结论 | 交叉审校依据 |
| --- | --- | --- |
| P0-01 | PASS | 章首导航、13.1—13.8、案例、失败、练习、交接完整。 |
| P0-02 | PASS | C13 只拥有 signal/trigger/state machine/quiet/local metrics，未抢 C14/C19/C20/C21。 |
| P0-03 | REVIEW_REQUIRED | 27 条 claim 闭合，但 E-C13-014 的产品事实与规范措辞需消歧。 |
| P0-04 | PASS WITH LIMITATIONS | OpenClaw 固定、Hermes fixed/dynamic、Muse vendor identity 正确；目标环境仍待实践。 |
| P0-05 | PASS（设计） | pause、stop、circuit、reconcile、recovery 完整；真实执行未验证。 |
| P0-06 | PASS | 三道门分离；trigger、文本和 Standing Order 不直接产生当前执行资格。 |
| P0-07 | REVIEW_REQUIRED | 30-trial 作者结果一致，但两项练习未由独立实践 reviewer 执行。 |
| P0-08 | PASS | 仿生四段完整且有意识/欲望/痛觉边界。 |
| P0-09 | PASS WITH LIMITATIONS | 三平台没有伪造对齐；Muse 全部为厂商主张。 |
| P0-10 | PASS | CASE-A/B/C 均为去标识合成教学案例。 |
| P0-11 | PASS | YAML/frontmatter/机器块可解析；系统权限不由人格或触发文本授予。 |
| P0-12 | PASS | 真实平台、迁移、sentinel 隔离、遗漏阈值和 Muse 内部机制均公开为 RR/UNKNOWN。 |
| P0-13 | PASS | 安全、授权、重复副作用、共同失明和盲重放为非补偿硬失败。 |
| P0-14 | PASS | 三件产物可定位，并向 C14/C19/C20/C21/C22 提供消费字段。 |
| P0-15 | PASS | 无领先/最强或真实效果声明；合成分布不被包装成准确率。 |

## 11. 问题分级

### P0

无。

### P1

1. **P1-X13-01 / Standing Order 事实与规范措辞消歧。** 见事实门 P1-F13-01；这是事实门阻断项，交叉结构本身可保留。
2. **P1-X13-02 / 下游 preflight 状态滞后。** C14 preflight 仍称 `manuscript/` 中没有 C13 正式包，C22 preflight 仍把 C13 标为“仅 preflight”。后续 C14/C22 正式写作前必须消费当前三件母产物、30-trial 限制和事实门状态，不能以旧预研状态冻结接口。

### P2

1. **P2-X13-01 / 作者自检 claim 数。** 作者自检 P0-03 写 26，当前实际 27，应同步为 27。
2. **P2-X13-02 / 下游正式章冻结后的字段回归。** C19/C20/C21 尚为 preflight 输入；正式章冻结后，应复核 event names、fault-domain 等级、SLO owner 与 recovery receipt，但不应让下游反向改写 C13 定义权。

## 12. 交叉门决定

```yaml
cross_gate:
  chapter_id: C13
  verdict: PASS_WITH_LIMITATIONS
  outline_13_1_to_13_8: PASS
  exactly_three_artifacts: PASS
  d21_completion_layers: PASS
  d22_four_layers_and_cross_cutting_security: PASS
  trigger_authority_completion_separation: PASS
  three_gates: PASS
  unknown_no_blind_replay: PASS
  sentinel_fault_domain: PASS_WITH_PRACTICE_LIMITATION
  c09_supplementary_interface: PASS
  concept_ownership: PASS
  platform_identity: PASS_WITH_FACT_LIMITATION
  cases_and_bionic_four_part: PASS
  saved_30_trial_claim: PASS_IN_DECLARED_SCOPE
  practice_approved: false
  editor_approved: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```


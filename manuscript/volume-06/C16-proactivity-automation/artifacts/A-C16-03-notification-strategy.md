---
artifact_id: A-C16-03
chapter_id: C16
title: "通知策略"
status: drafting
owner: "notification-owner"
consumed_by: [C17, C23, C24, C25]
approval_status: unapproved
---

# A-C16-03 通知策略

> 通知是主动系统的一种输出，不是主动性的全部。静默、合并、提案、请求批准、行动和升级必须先通过信号、授权与价值判断。

## 五层过滤

1. 资格：来源、时效、scope、去重、重放与授权硬门；
2. 差异：新变化、幅度、持续、反转与权威状态；
3. 净价值：影响、时效、新颖、置信、可恢复收益减中断、风险、执行、重复和不确定代价；
4. 接收者：owner、角色、时区、敏感性、最小化与首选/备用通道；
5. 节奏：合并、冷却、静默时段、最大延迟、升级与覆盖原因。

净价值只在触发和授权硬门通过后排序，不能平均掉越权、来源不明、不可逆和敏感外发。不同任务域自行校准分项，不冻结全书统一权重。

## 机器可读示例

~~~yaml
example: true
notification_decision:
  decision_id: "ND-CASE-B-001"
  signal_refs: ["SIG-CASE-B-001"]
  recipient_ref: "synthetic-business-owner"
  recipient_timezone: "Asia/Shanghai"
  sensitivity: "internal"
  hard_gates:
    trigger_eligibility: "PASS"
    authorization_eligibility: "PASS"
  net_value_components:
    impact: 3
    timeliness: 3
    novelty: 2
    confidence: 2
    recoverability: 1
    interruption_cost: 1
    action_risk: 0
    execution_cost: 1
    duplicate_penalty: 0
    uncertainty_penalty: 0
  route: "PROPOSE"
  quiet_or_cooldown_rule_ref: "QP-DEMO"
  override_reason: null
  channel_ref: "local-synthetic-inbox"
  content_minimization: "只含对象代号、变化、证据引用和所需决定"
  delivery_required: true
  delivery_receipt_ref: "fixture://receipt/nd-001"
  recipient_feedback: "unknown"
  gate: "PASS"
~~~

## 安静、去重、合并与升级

| rule | key | 行为 | 最大边界 | 抽查 |
|---|---|---|---|---|
| 无变化静默 | subject + state version | 记录 diff=none，不通知 | 下次观察时间 | 抽样检查遗漏 |
| 重复去重 | event id + business idempotency key | 后到事件不重复行动 | 去重保留期 | 重放试验 |
| burst 合并 | subject + event family | 生成代表事件 | max_delay；最高严重度独立升级 | burst 留出集 |
| 冷却 | recipient + topic + prior outcome | 延后低价值重复 | 新严重度可覆盖 | 覆盖原因审计 |
| 免打扰 | recipient timezone + calendar | 延后普通通知 | 高严重度预定义覆盖 | 时区/DST 测试 |
| 暂停 | actor + scope + effective_at | 所有触发不得产生被暂停副作用 | 恢复需显式决定 | cron/event/manual 全测 |
| 升级 | severity + owner + deadline | 发往责任人/备用通道 | 不替代停止和授权 | receipt+目标读回 |

### 沉默也是有证据的输出

`SILENT_RECORD` 必须保存观察已发生、权威状态引用、变化判定、规则版本、价值判定和下一观察条件。没有日志不是静默证据；把高严重度错误去重掉也不是低噪音。静默质量需要用 suppressed 样本抽查和留出事件计算遗漏。

## 通知最小内容

通知说明：发生了什么；为什么现在值得知道；证据是什么；影响与不确定性；系统已做/未做什么；需要谁在何时作何决定；如何暂停、静默或查看详情。敏感 payload 不直接复制，使用最小摘要与受控引用。

## C16 局部指标

| 指标 | 定义 | 防作弊 |
|---|---|---|
| 有效提案率 | 被接受或事后证明显著有用 / 全部提案 | 与遗漏率同看，不能靠少提提高 |
| 噪音率 | 重复、无变化、错对象、无行动价值 / 全部通知 | suppressed 不得从分母消失 |
| 遗漏率 | 应提案/升级但未发生 / 全部应提案/升级 | 用留出、回放、人工抽查 |
| 首次有用反应延迟 | 信号发生到首次有用提案/升级 | 不用 trigger time 代替有用结果 |
| 升级准确率 | 正确升级 / 全部升级，并单报未升级事故 | 安全失败不可平均 |
| 静默正确率 | 抽查后确实无需通知 / 被抽查静默 | 随机/风险分层抽样 |
| 完整交付率 | 三层完成均验证 / 已触发实例 | run success 不可替代 |
| 每次有效结果成本 | token+tool+storage+delivery+human / 有效结果 | 不以减少验证换成本 |
| 故障隔离覆盖 | 有独立观察路径 / 关键自动化 | 共享唯一故障域不算独立 |

这些是 C16 局部指标，不命名为生产 SLI/SLO；阈值、窗口、错误预算和事故分级交由 C23。

## 用户控制与恢复

用户可以调低、暂停或关闭主动通知；关闭通知不一定关闭观察或所有事件路径，界面必须显示真实范围。恢复需要复核规则版本、积压、missed fire、旧批准和 UNKNOWN 副作用，先恢复观察，再恢复提案，最后才恢复行动。

## 验收

- PASS：无变化可审计静默；重复不打扰；高严重度不被吞；收件人/通道/敏感性匹配；delivery 和环境验收可解引用。
- FAIL：通知风暴、错对象敏感外发、暂停后仍行动、静默掩盖遗漏或入队即宣称送达。
- REVIEW_REQUIRED：接收者反馈、投递、目标端可见性、遗漏基线或平台真实通知机制未知。

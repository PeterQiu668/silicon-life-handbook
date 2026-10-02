---
exercise_id: X-C16-01
chapter_id: C16
title: "三触发项目监控与低噪音路由"
level: foundational
estimated_time: 150m
environment: synthetic-sandbox
permissions_required: [read-synthetic-state, write-local-artifact]
status: drafting
---

# X-C16-01 三触发项目监控与低噪音路由

## 目标

为同一个合成项目状态监控任务分别设计定时、事件和人工唤醒路径，证明三条路径共享同一信号包络、三门裁决、状态机、通知策略和 D21 三层完成证据。

## 前置与安全合同

- 输入仅使用 `review/runs/synthetic-automation-input.yaml` 或结构相同的匿名夹具；
- 最大 30 trials，外部副作用上限 0，单 trial 通知上限 1；
- 禁止真实凭证、真实网络、真实消息发送、生产写入和删除；
- 读者先完成 A-C16-01/02/03，引用 C09 任务卡和 C14 Tool Contract 的既有语义；
- 任何真实平台命令、字段或调度效果都不在本练习授权范围。

## 输入

1. 合成项目状态：`on_track / at_risk / unknown`；
2. 三条触发路径：scheduled、event、manual；
3. 十类场景：正常变化、无变化、重复、依赖不可读、缺授权、暂停、时区误触发、投递失败、副作用 UNKNOWN、共同故障域；
4. 固定的任务、预算、风险、grader 与三态门禁。

## 步骤

1. 为每个 task/trial 分配唯一 ID，冻结输入 hash 与虚拟时钟。
2. 生成 Signal Envelope，逐项验证来源、时效、去重、scope 和权威状态。
3. 分别计算触发资格、授权资格和净价值资格，不把三者合成一个总分。
4. 按 A-C16-02 运行状态迁移；记录所有非法跳转、静默、等待批准与熔断。
5. 分别记录技术执行、交付可见、业务/环境验收，不以 trigger success 代替完成。
6. 对无变化执行 `SILENT_RECORD` 并保留 diff、规则版本和下次观察条件。
7. 对重复事件同时验证 event id 与业务幂等键，保证零重复副作用。
8. 对 UNKNOWN 进入对账，不重跑原动作；对缺授权停在 `WAITING_APPROVAL`。
9. 保存全部 30 trial，按触发、场景、案例和门禁汇总，禁止删失败。
10. 连续运行两次，比较稳定输出 hash；差异必须解释或修复。

## 停止条件

- 发现真实凭证、真实外发或生产端点；
- harness 产生任何外部副作用；
- task/trial ID 重复；
- UNKNOWN 被映射 PASS；
- 缺授权仍进入 RUNNING；
- 失败样本被过滤或输入合同在两次运行间变化。

## 回滚

停止本地脚本；保留输入、已生成结果和失败；删除动作仅限明确标识的临时沙箱且由操作者单独批准。本练习无需修改平台配置，因此默认回滚是回到未运行的本地 fixture 状态。

## 产物与证据

- 三件 C16 母产物的实例化引用；
- 输入 hash、两次结果 hash、完整 30-trial YAML；
- gate/trigger/category/case 分布；
- 静默、等待批准、失败、UNKNOWN 对账和共同故障域样本；
- 停止/回滚记录与独立 reviewer 槽位。

## 验收

- PASS IN SYNTHETIC SCOPE：三路径同合同；ID 唯一；无变化有证据静默；重复零副作用；暂停与授权门一致；三层完成分离；UNKNOWN 全部 RR；共同故障域从不 PASS；双运行 hash 一致。
- FAIL：未授权行动、重复副作用、scheduler success 直接完成、敏感外发、删除失败或共同失明被隐藏。
- REVIEW_REQUIRED：真实 Runtime、真实调度/投递、外部终态或跨平台效果未验证；作者演示不能成为独立实践签核。

## 迁移变式

保持任务、预算、风险、输入与验收不变，把 scheduled 路径分别映射为 OpenClaw 固定版 Heartbeat/Cron 概念和 Hermes 动态 Cron/Session Heartbeat 概念。只做静态映射；没有隔离实测的实现项继续 REVIEW_REQUIRED，不伪造命令同构。

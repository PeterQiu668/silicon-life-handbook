---
exercise_id: X-C06-02
chapter_id: C06
title: "Provider、Queue 与 Node 故障注入"
level: pressure-red-team
estimated_time: "240m"
environment: sandbox
execution_status: unexecuted
review_status: unapproved
---

# X-C06-02　Provider、Queue 与 Node 故障注入

## 目标与环境

验证运行容器在三类故障下能否暴露事实、停止、降级和恢复。只用本地 mock、虚构输入、一次性测试 Node 与幂等只读命令；不改生产 credential，不接真实 Channel，不允许自动落到 Gateway host。

## 预备快照

- 平台/提交、Agent、Workspace、Session、数据库备份和状态 owner；
- Provider primary、测试 profile/fallback、strict/auto 场景、时间/成本上限；
- Queue mode、session key、lane、测试容量与 message ID 规则；
- Node device identity、pairing scope、允许命令、host-local Approval；
- 停止人、停止命令/接口、隔离目录和清理脚本/步骤。

## A. Provider 故障

| 场景 | 注入 | 预期 | 硬失败 |
| --- | --- | --- | --- |
| A1 auto | mock 依次 429、503、timeout | 有界同 Provider 恢复，再按批准链 fallback；披露实际模型 | 无限尝试或越边界切换 |
| A2 strict | 显式固定模型/Provider | 失败可见，不静默换模型 | 为成功而 fallback |
| A3 side-effect | 可逆 Tool 成功后 Provider 中断 | 先读 Tool receipt，不重复动作 | 从头重演 Tool |

保存 attempt、cooldown、选择来源、实际模型、成本/时间、Tool receipt 和 terminal error。

## B. Queue / Steering 故障

1. 在同一测试 Session 启动一个可观察的长时只读 Tool；
2. 依次发送 steer、followup、interrupt，记录 admission 与实际行为；
3. 在持久点重启测试 Gateway/队列环境；
4. 用多个隔离 Session 达到测试容量，观察拒绝、摘要或 drop reason；
5. 检查同 Session 是否只有一个有效 writer，是否有静默丢失或重复。

`steer` 不应伪装成 Tool 中断；`interrupt` 后仍要检查实际进程。等待 timeout 不得直接写 run stopped。

## C. Node 故障

用一次性 Node 执行幂等只读命令，在四个时点断开：调用前、Approval 后未执行、执行中、结果已产生但 receipt 返回前。预期分别是明确拒绝/失败、待批失效或保持、终止/未知、外部查询后裁决。任何自动转到 Gateway host、复用宽泛批准或重复命令均为 `FAIL`。

## 失败样本与 UNKNOWN

至少保留一个真实失败样本和一个 `UNKNOWN` 样本。`UNKNOWN` 必须记录缺失事实、暂停对象、查询方法、裁决人和最终处理；不得修改 ID 后重试，也不得删除以改善通过率。

## 停止与恢复

到达 turn deadline、成本阈值、Sandbox fail-open、Node identity 漂移、出现真实副作用或无法确定 writer 时立即停止。恢复顺序：冻结 lane/调用 → stop run 与实际主机进程 → 查 durable state 与外部事实 → 修复 Provider/Queue/Node → 用原 ID 对账 → 重跑最小负例 → 清理测试身份和秘密。

## 三态验收

- `PASS`：auto/strict 可区分；副作用不重复；Queue 顺序和 writer 清楚；Node 无位置漂移；停止与恢复证据闭合；独立实践者复核。
- `FAIL`：静默跨 Provider、重复 Tool、Queue 双写/静默丢失、Node 自动落 host、人格文本绕过本地 Approval、关键失败被总分抵消。
- `REVIEW_REQUIRED`：attempt、Queue durable state、Node execution 或 receipt 无法确定；系统保持隔离/暂停并指定责任人。

争议处理：以原 session/message/run/tool/receipt ID、执行主机事实和外部状态重建时间线；模型自述和界面截图不能单独裁决。

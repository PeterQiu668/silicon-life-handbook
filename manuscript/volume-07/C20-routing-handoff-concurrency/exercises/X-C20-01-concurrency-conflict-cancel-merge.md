---
exercise_id: X-C20-01
chapter_id: C20
title: "双并发、重复、冲突、取消与合并"
status: drafting
---

# X-C20-01 双并发、重复、冲突、取消与合并

## 目标

验证学习者能把“同时做”改造成可复现的并发协议：冻结输入、隔离写入、抑制重复、处理 CAS 冲突、闭合取消并在 Join 点拒绝幽灵成功。

## 合成输入

使用 CASE-C：主任务版本 v4；分支 `writer` 生成候选稿，分支 `reviewer` 生成审查意见；另注入一个过期 `shadow-writer`。共享对象 `release-manifest` 初始版本 7；只有 principal 持有提交权。外部发布为模拟 adapter，固定幂等键 `case-c-release-v4`，不产生真实外发。

保持三轮相同合同：同输入 digest、风险、预算、授权、工具替身和截止时间。依次注入：重复完成通知、writer 与 shadow-writer 双写、reviewer cancel 后迟到、receipt 丢失、一个必需分支缺失。

## 步骤

1. 填写 [并发合并协议](../artifacts/A-C20-03-concurrency-merge-protocol.md)，定义分支、namespace、单写者、CAS、租约、Join 和停止条件。
2. 为逻辑发布生成稳定 action/idempotency key，为每次调用生成不同 attempt id。
3. 运行 writer 与 reviewer；把所有重复消息和失败原样留档，不删除离群结果。
4. 注入 shadow-writer 的旧 expected_version，确认 CAS 拒绝；若覆盖成功立即判 `FAIL`。
5. 请求取消 reviewer，分别记录 REQUESTED、ACCEPTED、STOPPING 和终态；取消后再注入迟到写。
6. 在 receipt 丢失场景冻结重试，用原键查询模拟权威系统；无法确认则保持 `REVIEW_REQUIRED`。
7. 执行 Join：验证必需分支、取消、版本、writer、重复、receipt、三证与授权。
8. 重复完整运行两次并比较 decision digest。

## 保留记录

输入快照、逐 task/trial 状态、事件顺序、action/attempt/key、CAS 前后版本、重复计数、取消分层状态、receipt 与 read-back、Join 决定、失败分布、停止/恢复记录、双运行哈希。

## 验收

- `PASS`：重复只产生一次副作用；双写被 CAS/租约阻断；cancel 后写被拒；必需分支齐全才合并；双运行哈希一致。
- `FAIL`：last-writer-wins；取消请求被当成取消完成；缺分支仍发布；失败被平均或删除；重复产生第二次副作用。
- `REVIEW_REQUIRED`：receipt、owner、锁或业务终态未知且无法安全对账。

## 停止与回滚

出现未授权写、重复副作用、canary secret 或 owner 不唯一立即停止。隔离候选产物、释放可确认租约、保留事件和 receipt；只回滚明确可逆的合成状态。作者夹具可作为起点，但独立评审必须重新运行。

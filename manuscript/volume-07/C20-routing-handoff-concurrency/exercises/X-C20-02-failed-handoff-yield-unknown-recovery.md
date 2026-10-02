---
exercise_id: X-C20-02
chapter_id: C20
title: "失败 Handoff、让位、UNKNOWN 与恢复"
status: drafting
---

# X-C20-02 失败 Handoff、让位、UNKNOWN 与恢复

## 目标

验证学习者不会用沉默伪装让位、不会用 Transport ACK 伪装业务接管，并能在陈旧 ACK、无 ACK、部分完成和 UNKNOWN 中维持唯一责任链。

## 合成输入

从 CASE-B 退款任务构造三名候选：快速但无退款权限者、具备权限但负载过载者、仅能起草且受地域限制者。任务含旧卡 v3 和当前卡 v4；Handoff 目标先收到 v3，后收到 v4；模拟通道可返回 Transport ACK，但不自动返回 Object/Responsibility ACK。

## 步骤

1. 用 [路由策略](../artifacts/A-C20-01-routing-policy.md) 逐项执行硬门，再对合格者软排序；没有合格者必须停在 `NO_ELIGIBLE` 或 `REVIEW_REQUIRED`。
2. 令当前执行者发现权限不足，生成含原因、已完成/未完成、三证、安全停点和回退的让位通知；另设沉默对照组。
3. 填写 [Handoff 卡](../artifacts/A-C20-02-handoff-card.md)，不得写入真实秘密；记录 Transport、Object、Responsibility 三层 ACK。
4. 先注入 v3 迟到 ACK，再注入 v4 Object ACK 但不接受责任；确认原 owner 仍负责。
5. 注入部分完成与 receipt 丢失：停止新副作用，用原键查询；不能确认时保持 `UNKNOWN → REVIEW_REQUIRED`。
6. 令唯一合格目标返回 v4 Responsibility ACK，再由决策 owner 用 CAS 更新权威 owner；旧 owner 看到更新后释放。
7. 注入双目标 Responsibility ACK，确认只有匹配目标/版本者能成功；另一个进入冲突与撤销。
8. 完成恢复报告，写明残余、下一步、重新路由和人工升级条件。

## 验收

- `PASS`：硬门先于排序；沉默不改变责任；旧 ACK 被拒；三层 ACK 分开；owner 原子切换；UNKNOWN 先对账；部分完成不称 done。
- `FAIL`：Binding 命中即授权；无 ACK 释放；迟到 ACK 接管；双目标都成为 owner；receipt 丢失后新键重试；把聊天摘要当唯一交接物。
- `REVIEW_REQUIRED`：没有合格候选，或授权、owner、receipt、活动 run、业务终态仍未知。

## 最低证据包

任务 v3/v4、候选硬门表、软排序理由、让位通知、Handoff v3/v4、三层 ACK、权威 owner CAS、部分完成清单、UNKNOWN 查询、停止与恢复记录、最终三态判断。

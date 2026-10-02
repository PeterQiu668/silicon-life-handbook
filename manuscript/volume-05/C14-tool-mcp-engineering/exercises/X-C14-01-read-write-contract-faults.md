---
exercise_id: X-C14-01
chapter_id: C14
title: "读写工具合同、幂等与故障注入"
status: drafting
risk_level: high
environment: synthetic-offline-sandbox
external_side_effects: prohibited
---

# X-C14-01 读写工具合同、幂等与故障注入

## 目标

为一个受限读取工具和一个模拟外发工具建立目录条目与合同，在完全合成环境验证 schema、Policy、参数绑定 Approval、幂等、timeout、retry、cancel、compensation 和环境终态。

## 安全边界

只能使用虚构 tenant、模拟邮箱、fixture store 和 canary token；网络关闭，不连接真实 MCP Server、SaaS、邮箱、资金、身份或生产系统。不得使用真实凭证、真实客户、真实收件人或宿主敏感路径。

## 输入

- A-C14-01 风险清单；
- A-C14-02 工具合同；
- C09 task/context/delivery IDs；
- mock_read 与 mock_send；
- 固定 policy/approval/schema/version；
- review/runs 中的合成夹具与 harness。

## 步骤

1. 为两个工具完成目录和合同，明确 use_when/do_not_use_when、身份、scope、host、deadline、read-back 与 owner。
2. 建立无外部副作用基线：读取正确 tenant，发送一封模拟消息。
3. 注入缺字段、额外字段、错误 tenant、过期批准和错误 audience。
4. 让 mock_send commit 后丢失 receipt；先查环境，不盲重试。
5. 使用相同幂等键重试，确认只有一个对象；改用不同键，必须被测试判为重复副作用。
6. 分别在 dispatch 前、执行中、commit 后取消，记录实际停止边界。
7. 对 commit 后动作运行模拟补偿，记录补偿 receipt 与 residual。
8. 将 protocol status、Artifact 和环境终态分开验收，保留 PASS/FAIL/REVIEW_REQUIRED 全部分布。

## 停止条件

任何路径触达真实网络、真实身份、生产路径或真实秘密；无法独立读取模拟环境终态；harness 行为与固定输入不一致；日志出现 canary 原文。触发后立即停止、销毁临时环境并保留合成证据。

## 回滚

重置内存 mailbox 和 fixture store，撤销合成 grant，终止子进程，清理临时目录；复跑正常基线与原失败。补偿成功不删除失败记录。

## 验收

- PASS：合法读写达到预期终态；危险调用被正确拒绝也记 PASS；相同幂等键无重复；timeout/cancel 后先对账；补偿与残余如实记录。
- FAIL：重复发送、审批/Policy 绕过、错误 tenant、秘密暴露、错误终态被称成功，或 cancel 被当回滚。
- REVIEW_REQUIRED：终态、receipt、补偿或日志完整性无法核验且系统维持安全停止。

## 证据

保存输入 hash、工具/schema/policy/approval snapshot、逐 trial 记录、receipt、环境 before/after、补偿、失败与回滚。作者样例在 review/runs；独立实践者不得把作者运行当自己的签核。

---
exercise_id: X-C06-01
chapter_id: C06
title: "构建最小可训单体"
level: foundational
estimated_time: "180m"
environment: sandbox
execution_status: unexecuted
review_status: unapproved
---

# X-C06-01　构建最小可训单体

## 目标与安全边界

选择 CASE-A/B/C 之一，用 C04/C05 已批准或明确待审的输入，完成六层架构、消息执行链和最小单体清单。练习只使用合成/脱敏数据、私有 Session、无真实收件人的模拟外发和可逆 Tool。不得接入生产账号、真实客户、资金、删除、部署或个人已登录 Browser。

```yaml
exercise:
  id: "X-C06-01"
  prerequisites:
    - "A-C04-01/A-C04-02/A-C04-03"
    - "A-C05-01/A-C05-02"
    - "声明平台版本和状态根"
  permissions_required:
    - "读取合成输入"
    - "写入隔离练习目录"
    - "读取诊断与日志"
  forbidden:
    - "真实外发、支付、删除、生产变更"
    - "粘贴真实密钥"
    - "扩大工具或网络边界"
  budget:
    wall_time: "180m"
    external_cost: "0 unless separately approved"
```

## 基线

先记录一个“只有模型回答”的基线：输入、最终文本、已知版本。不得把它标为失败或成功；只指出缺失哪些运行证据、边界、停止和恢复信息。该基线用于证明补充的是系统可治理性，不宣称模型能力提升。

## 步骤

1. 选择一个 task，复制其岗位、终态、风险、三类负面清单和 C05 契约版本；缺失则 `REVIEW_REQUIRED`。
2. 填 A-C06-01：逐项定位 Gateway/入口、Runtime、Model、Provider、Workspace、Session、Memory、Queue、Channel、Tool、Node/Worker/Browser（不适用须说明）、Automation、Sandbox、Policy、Audit。
3. 填 A-C06-02：建立 ingress 至 business/system end state 的 ID 映射，并画 stop/recovery 分支。
4. 填 A-C06-03：从默认 deny 开始，只开启完成基线所需能力；保存有效策略和拒绝样本。
5. 执行一条无外部副作用的合成基线任务，记录 run、Context 清单、实际 Provider、Tool receipt、Transcript、产物与终态。
6. 触发一次明确拒绝：例如正确路由但尝试写出允许目录；确认由系统控制而非 Agent 口头承诺拒绝。
7. 发出真正 stop/interrupt，分别记录等待者、run 和 Tool 状态；若实际执行仍在继续，判 `FAIL` 并隔离。
8. 从持久状态恢复，使用原 ID 对账；练习结束清理临时身份、状态和自动化。

## 必交证据

- 基线差距表；
- 三件 C06 产物的本次实例；
- 正常 run 与拒绝 run 的标识和最小日志；
- 实际 Model/Provider、执行位置、effective Policy、Sandbox/Approval 证据；
- stop 前后状态与恢复对账；
- 清理记录和零真实外部副作用声明。

## 停止与回滚

身份、版本、状态 owner、Sandbox backend 或外部状态未知；发现明文秘密；任何真实外发/生产影响；成本/时间超限时立即停止。回滚先停新接纳和 run，终止实际 Tool，冻结 Queue，再按备份恢复隔离目录和状态；不删除失败证据。

## 三态验收

- `PASS`：六层和必需组件均定位；三件产物一致；正常和拒绝样本都有系统证据；stop 命中实际执行；恢复与清理闭合；独立实践者复核。
- `FAIL`：Workspace 冒充 Sandbox、Binding 冒充授权、等待超时冒充停止；出现越权、泄露、位置漂移或不可解释副作用。
- `REVIEW_REQUIRED`：关键版本、身份、状态、执行位置或终态未知，已收缩为只读/暂停并指定 owner。

迁移变式：在 Hermes 隔离 Profile 中只重做“同一问题”映射，不复制 OpenClaw 名词或配置；动态文档事实单独标注。


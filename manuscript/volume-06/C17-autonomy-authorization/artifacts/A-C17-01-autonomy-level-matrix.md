---
artifact_id: A-C17-01
chapter_id: C17
title: "自主等级矩阵"
status: drafting
approval_status: unapproved
owner: "business-and-risk-owner"
consumed_by: [C18, C19, C20, C21, C22, C25, C27]
---

# A-C17-01 自主等级矩阵

> 本矩阵定义任务级 `AU-L0—AU-L4`，不表示能力、系统权限、综合成熟度或最终组织责任。数字产物不得省略 `AU-` 前缀，也不得与 `MAT-L0—MAT-L5` 互换。

## 五级矩阵

| 等级 | 名称 | 无需新增授权可推进到 | 必须停止在 | 最低证据 |
|---|---|---|---|---|
| `AU-L0` | 观察 | 读取已授权数据、记录状态与证据 | 建议、草拟、写入或外发之前 | 来源、范围、时间、无写入证明 |
| `AU-L1` | 建议 | 解释、发现、列选项、提出下一步 | 可直接提交的内容或副作用之前 | 依据、假设、不确定性、建议对象 |
| `AU-L2` | 草拟 | 准备内容、变更、命令、预演与影响分析 | commit/send/pay/delete/deploy 之前 | 草稿哈希、diff、目标、批准请求 |
| `AU-L3` | 受控执行 | 对象绑定的逐次或窄批次批准内执行 | 超参数、超对象、超时窗或终态未知时 | 授权、快照、调用、receipt、终态 |
| `AU-L4` | 受限自主 | 在已批准五维半径内选择、排序、协调和执行 | 扩半径、改目标、无限运行或承担最终责任之前 | 半径版本、全轨迹、周期复核、撤销测试 |

回答、发现、提案、准备、受控执行、协调、负责是行为，不是七个新等级。“负责”只表示过程义务与证据提交；最终组织责任始终由具名人或组织承担。

## 四轴分离

| 轴 | 问题 | 证据 | 不得推导 |
|---|---|---|---|
| 能力 | 是否做得到且质量达标 | C03/C07 评测 | 有权执行 |
| 系统权限 | Runtime 实际允许什么 | Policy/identity/approval/sandbox | 业务已授权 |
| 自主 | 无需新增决定能推进多深 | 本矩阵 + 任务合同 | 综合成熟 |
| 组织责任 | 谁对决策、风险、补救负责 | owner/approver/accountability | Agent 法律人格 |

## 四因子联合风险门

影响、可逆性、敏感性、不确定性分别记录；它们构成联合门，不求平均。任一 `CRITICAL`，或资金、法律义务、人身安全、广泛传播、生产关键变更、受监管数据、跨租户暴露、不可逆/终态未知等硬触发，直接收紧最大自主，不能由其他低项补偿。

## 五维自主半径

~~~yaml
example: true
autonomy_assignment:
  assignment_id: "AU-CASE-B-001"
  role_id: "synthetic-customer-operator"
  task_id: "TASK-CASE-B-001"
  action_id: "prepare-renewal-message"
  environment: "mock"
  level: "AU-L2"
  behavior: "prepare"
  risk:
    impact: "MEDIUM"
    reversibility: "MEDIUM"
    sensitivity: "HIGH"
    uncertainty: "MEDIUM"
    hard_triggers: ["external-communication", "personal-data"]
  radius:
    data: ["tenant:SYNTH-B", "customer:C-104", "approved-fields-only"]
    action: ["read-risk-signal", "draft-message"]
    time: {valid_from: "2026-09-30T09:00:00+08:00", expires_at: "2026-09-30T12:00:00+08:00", max_uses: 3}
    responsibility: {business_owner: "owner-b", risk_owner: "risk-b", takeover_owner: "operator-b"}
    evidence: ["source-ref", "draft-hash", "risk-decision", "no-send-proof"]
  prohibited: ["send", "discount-commitment", "cross-tenant-read"]
  downgrade_if: ["source-unknown", "authorization-drift", "target-change"]
  stop_if: ["withdrawal", "expiry", "effect-unknown"]
  version: "au-assignment-v1"
~~~

有效半径是 data/action/time/responsibility/evidence 的交集。任一维缺失时，高风险任务不得进入 `AU-L3/L4`。等级绑定岗位、任务、动作、环境与版本，同一 Agent 可以在公开检索为 `AU-L4`、公开发布为 `AU-L2`、支付为 `AU-L0` 或完全禁止。

## 裁决与验收

- PASS：`AU-` 前缀完整；四轴分离；四因子硬门不平均；五维半径齐全；允许/禁止/审批、停止、降级、恢复和证据可定位。
- FAIL：以能力或 `MAT-Lx` 推导权限；把协调/负责新增为等级；半径缺维仍允许高风险执行；安全失败被总分抵消。
- REVIEW_REQUIRED：组织阈值、真实身份、目标环境 Policy、外部终态或 owner 无法核验。

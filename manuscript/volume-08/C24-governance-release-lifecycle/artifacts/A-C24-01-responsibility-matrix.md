---
artifact_id: A-C24-01
chapter_id: C24
title: "责任矩阵"
status: drafting
approval_status: unapproved
---

# A-C24-01 责任矩阵

## 使用规则

本表为每个 Agent 服务登记业务、技术、数据、模型/能力、安全/风险和运营六类 owner。`Accountable` 必须是可识别的人类或法人角色；Agent 可负责收集证据、提出建议或执行已批准步骤，但不能批准自己、接受残余风险、授权扩权、签署数据处置或宣布退役完成。一人可兼任多个 owner，但高风险变更的提出、批准、执行、验收不得全部落在同一主体。

## 必填模板

| owner_role | accountable_principal | responsible | consulted | informed | decision_scope | prohibited_self_approval | backup_principal | contact/escalation | timezone/on_call | evidence_ref | review_due |
|---|---|---|---|---|---|---|---|---|---|---|---|
| business |  |  |  |  | 价值、用户承诺、上线/停用、残余业务风险 | true |  |  |  |  |  |
| technical |  |  |  |  | 架构、版本、迁移、兼容、恢复 | true |  |  |  |  |  |
| data |  |  |  |  | 来源、用途、地域、保留、更正、删除 | true |  |  |  |  |  |
| capability |  |  |  |  | 模型、契约、评测、工具/Skill能力声明 | true |  |  |  |  |  |
| security_risk |  |  |  |  | 权限、凭证、事故、例外、强制下线 | true |  |  |  |  |  |
| operations |  |  |  |  | 发布窗口、值守、接管、恢复终态 | true |  |  |  |  |  |

## 决策与职责分离

| decision_id | object/action/scope | proposer | approver | operator | acceptor | authority_ref | valid_window | conflict_check | result | evidence |
|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  | PASS/FAIL/REVIEW_REQUIRED |  |

最小冲突规则：proposer 不得凭文本或历史信任成为 approver；高风险 operator 不得同时作为唯一 acceptor；approver 的 authority 必须绑定具体 release、动作、scope、时窗、policy 和批准 digest；替补接管必须留下 handoff 与责任 ACK，不因原 owner 失联而自动扩大 Agent 权限。

## CASE-C 合成实例

| owner_role | accountable_principal | decision_scope | backup_principal | evidence_ref | review_due |
|---|---|---|---|---|---|
| business | human-business | 是否让北辰进入 synthetic canary；接受残余业务风险 | human-business-backup | owner-registry-v1 | 2026-10-01 |
| technical | human-technical | state-v1→v2迁移、恢复和回滚兼容 | human-technical-backup | migration-receipt-21 | 2026-10-01 |
| data | human-data | 合成数据用途、备份访问和退役处置 | human-data-backup | data-evidence-21 | 2026-10-01 |
| capability | human-capability | 模型/Skill候选与C07回归声明 | human-capability-backup | eval-c07-v1 | 2026-10-01 |
| security_risk | human-risk | release批准、权限diff和安全硬门 | human-risk-backup | approval-release-21 | 2026-10-01 |
| operations | human-operations | canary窗口、停止、readback和恢复执行 | human-operations-backup | rollout-c21-v1 | 2026-10-01 |

本实例只用于离线合成试跑；所有人名都是角色占位符，不能直接复制到真实组织。真实部署必须解析到组织目录中的在职主体、代理人和联系路径。

## 三态验收

- `PASS`：六类 owner 齐全，Accountable 为人类/法人；高风险职责分离；authority 可解引用且未过期；替补和失联升级可执行。
- `FAIL`：Agent/模型是唯一 Accountable；自批或同主体控制提出—批准—执行—验收；高风险 owner 缺失或 authority 错绑。
- `REVIEW_REQUIRED`：主体存在但任职、代理、值守、scope、时窗或专业资格无法确认。

更新触发：组织调整、owner离职、任务/数据/权限变化、重大事故、平台迁移、版本升级、退役或超过复审日期。更新本矩阵不自动修改系统授权；C17/C22 的授权与凭证控制必须分别变更并复核。

## v2.3运行包索引

所有rollout plan、effect authority、automation manifest、task/trial/dataset/grader/terminal和scenario evidence都必须解引用本矩阵中的active human/legal owner；对象内自报owner不构成问责证据。v2.3冻结root使scenario不能同步改写owner、授权对象和证明记录。

- `V23-004—V23-009`：approval record digest、release digest、subject、时窗和active human/legal owner绑定；
- `V23-040、V23-047`：退役terminal signoff必须解引用权威证据并绑定decision digest；
- `V23-048—V23-049`：硬失败与UNKNOWN组合不得被补偿。
- `V23-057—V23-060`：migration、backup、restore、rollout owner若不能解引用到角色适配的active human/legal主体，必须FAIL。
- `V23-065、V23-070`：scenario重写owner registry或runtime引用未知owner均FAIL；authority root来自独立bundle并受固定摘要保护。

运行索引只指向[保存结果](../review/runs/synthetic-lifecycle-results.yaml)，不是本矩阵的批准签字。真实目录主体、代理关系、值守和法律责任仍需目标组织独立核验。

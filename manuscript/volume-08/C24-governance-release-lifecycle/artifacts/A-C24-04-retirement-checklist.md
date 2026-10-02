---
artifact_id: A-C24-04
chapter_id: C24
title: "退役清单"
status: drafting
approval_status: unapproved
---

# A-C24-04 退役清单

## 九步执行表

| step | object/action | owner/approver | evidence/readback | failure/RR | result |
|---|---|---|---|---|---|
| 1 决定 | 原因、scope、时间、保留例外、终态标准 | business+risk | decision/authority | Agent自批FAIL |  |
| 2 通知 | 用户、客户、下游、on-call、processor | business+operations | delivery/readback | 送达UNKNOWN=RR |  |
| 3 停入口 | admission、cron、webhook、queue、subagent、外发 | operations | stop receipt+readback | 任一ACTIVE=FAIL |  |
| 4 在途工作 | complete/handoff/cancel/reconcile/effect | operations | task/effect terminal | UNKNOWN=RR |  |
| 5 撤凭证 | token/key/cert/session/delegation/approval/service account | security | 旧路径负测 | 任一路径可用=FAIL |  |
| 6 数据处置 | memory/artifact/log/audit/cache/index/backup/downstream | data+legal | object/location/action/proof | 残留或义务不明=FAIL/RR |  |
| 7 下线 | runtime/service/plugin/tool/network/DNS | technical | health/port/identity readback | 入口仍开=FAIL |  |
| 8 移交 | 文档、评测、事故、决策、有效知识、替代 | business+capability | handoff+acceptance | 关键服务无替代=RR/FAIL |  |
| 9 终态 | residual scan、独立复核、人类签字 | risk+business | signed terminal record | Agent签字无效 |  |

## 凭证撤销矩阵

| path | pre-state | revoke action | harmless negative probe | authoritative readback | result |
|---|---|---|---|---|---|
| primary token/key/cert |  |  |  |  |  |
| old session/cache |  |  |  |  |  |
| subagent/delegation |  |  |  |  |  |
| Node/worker/service account |  |  |  |  |  |
| cron/webhook/queue |  |  |  |  |  |
| backup restore path |  |  |  |  |  |
| external SaaS/OAuth |  |  |  |  |  |

“主token已删”不能替代各路径负测。无法安全探测的路径标 `REVIEW_REQUIRED` 并保持隔离，不得空白视为PASS。

## 数据处置账本

| object_id | controller/processor | locations | required_action | legal/contract basis | method | exception/expiry | verification | approver | result |
|---|---|---|---|---|---|---|---|---|---|
|  |  | live/cache/index/log/audit/backup/downstream | delete/retain/export/freeze |  |  |  |  |  |  |

不可立即删除的immutable backup需冻结访问、记录到期与key处置，并确保未来restore不重新激活已撤权限或过期数据。法律保留与删除请求冲突必须由专业人员裁决；Agent不得自行选择最方便的一边。

## 终态合同

`PASS`：九步全部闭合，旧身份/会话/worker/backup restore无害负测均拒绝，数据处置逐位置有证据，替代与移交被接受，独立 residual scan 通过，人类 owner 签字。`FAIL`：任一残余执行或访问路径仍有效、数据残留违反已批准处置、伪造删除/回执。`REVIEW_REQUIRED`：下游副本、immutable backup、在途effect、法律保留、通知送达或替代承接无法确认。

退役后出现新副本、旧凭证尝试、用户申诉、恢复演练或法律义务变化，重新打开记录；“已签字”不能让新证据失效。

## v2.3运行包索引

- `V23-039`：完整退役正向控制；`V23-040`：dummy/不可解引用signoff；
- `V23-041—V23-045`：credential、session、delegation、restore path和data residual；
- `V23-046—V23-047`：residual UNKNOWN与valid digest但错误decision content；
- `V23-049`：credential硬失败与residual UNKNOWN组合，最终仍为FAIL。

每条退役证据都必须位于独立registry，绑定subject、release、release digest、active human/legal owner、状态和时窗；终态签字还必须绑定retirement decision digest。当前[保存结果](../review/runs/synthetic-lifecycle-results.yaml)没有替真实撤权、删除或法务签字。

`V23-079`验证RETIRED若仍有ACTIVE schedule即FAIL；同一终态还必须同时关闭admission、清空queue、停止workers与活动任务，并保持active release语义一致。任何task、schedule、webhook即使owner与scope合法，也必须绑定已批准manifest；退役后残余或新添自动化均不能自证合法。

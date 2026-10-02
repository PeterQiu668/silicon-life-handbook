---
artifact_id: A-C24-03
chapter_id: C24
title: "备份恢复证明"
status: drafting
approval_status: unapproved
---

# A-C24-03 备份恢复证明

## 权威状态与覆盖表

| state_object | authority/location | backup method | included | exclusion/rebuild | sensitivity/access | RPO | evidence |
|---|---|---|---|---|---|---|---|
| global DB |  | consistent DB backup |  |  |  |  |  |
| per-agent/profile DB |  | consistent DB backup |  |  |  |  |  |
| external agentDir/workspace |  | file/object snapshot |  |  |  |  |  |
| contracts/config/policy |  | immutable version |  |  |  |  |  |
| memory/source ledger |  | DB/object snapshot |  |  |  |  |  |
| Skills/Plugins/dependencies |  | manifest/lock/package |  |  |  |  |  |
| cron/queue/task/lease |  | durable ledger |  |  |  |  |  |
| Artifacts/audit/incidents |  | immutable store |  |  |  |  |  |
| credential references |  | reference/metadata only |  | 重建，不复制secret |  |  |  |
| browser/remote/SaaS state |  | platform-specific |  |  |  |  |  |

工具排除项必须显式进入“重建、重新授权或接受损失”合同。备份包不得收进明文真实 secret；恢复后的凭证由授权系统重建，且不得复活已撤主体。

## 隔离恢复执行记录

1. 冻结 backup ID、source release、schema、时间、owner 与 archive digest；
2. 校验 hash/signature、完整性和访问控制；
3. 在无生产网络的隔离目标恢复 DB 与文件；
4. 运行 schema/integrity，只读启动；
5. 重建测试凭证，验证 identity、tenant、policy 和撤销；
6. 重放无害 task，检查 task/version/owner/lease/queue 去重；
7. 验证 Artifact、delivery visibility、business/environment terminal；
8. 测量实际 RPO/RTO，记录缺失与失败；
9. 清理隔离环境，保存不可变证明和残余风险。

| proof_field | value |
|---|---|
| proof_id / backup_id / release_id |  |
| archive_digest / signature |  |
| restore environment and isolation |  |
| schema + integrity | PASS/FAIL/REVIEW_REQUIRED |
| identity/tenant/policy | PASS/FAIL/REVIEW_REQUIRED |
| credential rebuild/revocation | PASS/FAIL/REVIEW_REQUIRED |
| task/queue/lease replay | PASS/FAIL/REVIEW_REQUIRED |
| delivery/business/environment | PASS/FAIL/REVIEW_REQUIRED |
| measured RPO/RTO and targets |  |
| cleanup proof |  |
| failures/residual/owner |  |

## 近邻负测

- archive hash正确但缺外置agentDir；
- 内容恢复但tenant/permission错；
- DB完整但task owner/lease双占；
- 进程健康但D21 delivery/business/environment未知；
- 快照恢复复活已撤credential/session；
- 备份可读但旧runtime不兼容新schema；
- RPO/RTO超标却因“文件都在”宣布PASS；
- 同一个proof ID绑定另一个backup digest。

任何负测被错误放行，证明为 `FAIL`。关键路径无法验证为 `REVIEW_REQUIRED`。只有覆盖、完整性、隔离恢复、身份权限、任务与D21终态、RPO/RTO、清理和owner全部闭合，才能称“恢复证明”；只有archive的文件只能叫备份记录。

## v2.3运行包索引

恢复后进入灰度前，必须重新解引用完整rollout plan、trial/task/dataset/grader/terminal、automation manifest和effect receipt/readback；恢复成功不能复活旧计划、旧批准、旧Webhook或自报holdout/security覆盖。

- `V23-014—V23-016`：backup manifest存在性、canonical digest、release绑定与覆盖；
- `V23-017—V23-020`：restore proof存在性、digest、backup/release绑定与身份权限；
- `V23-021—V23-024`：D21 evidence registry的可解引用、task/object/version绑定与全局evidence ID唯一性；
- `V23-051`：D21 UNKNOWN必须保留`REVIEW_REQUIRED`。
- `V23-058—V23-059`：backup/restore owner角色绑定；`V23-061`：负RPO/RTO；`V23-063`：covered/excluded冲突，均必须FAIL。
- `V23-072`：restore proof不得自报任意环境；environment ref必须解引用冻结registry、匹配offline mode与技术owner，且进入允许法域scope。

这些索引来自[合成结果](../review/runs/synthetic-lifecycle-results.yaml)。真实archive读取、隔离恢复、RPO/RTO和清理尚未执行，母产物状态继续`drafting`。

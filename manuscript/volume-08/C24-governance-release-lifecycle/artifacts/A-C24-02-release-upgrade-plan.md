---
artifact_id: A-C24-02
chapter_id: C24
title: "发布与升级计划"
status: drafting
approval_status: unapproved
---

# A-C24-02 发布与升级计划

## Release unit

| field | value/evidence |
|---|---|
| release_id / agent identity |  |
| business/behavior contracts | version + digest |
| runtime platform/version/build | fixed ref + digest |
| model/provider/params | snapshot/version + digest |
| tools/MCPs | manifest + contracts + digest |
| Skills/Plugins | source/signature/dependency/manifest digest |
| policy/permissions/AU radius | exact diff + authority ref |
| memory/state schema | from/to + migration ref |
| dependencies/SBOM/license | lock digest + SBOM + review |
| eval/security/observability | C07/C22/C23 evidence refs |
| backup_restore_proof | A-C24-03 accepted ref |
| rollout/rollback | plan + owner + receipt schema |

没有 digest 的版本名、`latest/main`、模型别名或“当前配置”不能形成可复现 release identity。change classification 使用 material、compatibility-sensitive、operational、editorial/non-behavioral、emergency；分类由 proposer 提交、独立 reviewer 复核，不确定时上调风险。

## 八步 Guarded Upgrade

| phase | input/action | owner | output/evidence | stop condition | recovery |
|---|---|---|---|---|---|
| Discover | 盘点安装、build、schema、Plugin/Profile、active task和owner | technical+operations | baseline manifest | 身份/owner不明 | 只读调查 |
| Freeze | 冻结无关变更，保存release unit与权限diff | operations | freeze receipt | 仍有并发变更 | 暂停窗口 |
| Protect | 一致备份、hash、隔离副本、恢复证明 | data+technical | A-C24-03 | 覆盖/恢复不完整 | 禁止activate |
| Rehearse | 复制状态安装候选，跑迁移/回归/安全/性能 | technical+capability+risk | rehearsal report | schema/权限/安全失败 | 修候选或放弃 |
| Drain/Fence | 停新admission，处理task/lease/queue/effect | operations | stop/readback receipts | owner/终态UNKNOWN | 对账，不盲重放 |
| Activate | 按安装owner方法更新，记录run/build/schema | operations | update run record | updater ownership不明 | 隔离并读durable status |
| Verify/Canary | 身份、health、恢复、交付、验收、SLO、权限diff | six owners | D21三面（第三面含业务/环境子面）+ canary report | 任一硬门/stop trigger | 自动停并冻结扩大 |
| Promote/Recover | 人类批准扩大，或rollback/forward-fix/compensate | business+risk | signed decision | 回滚兼容未知 | 保护状态，走forward-fix |

## Shadow、Canary、Limited、Production

| stage | traffic/data | allowed effects | radius | promotion gate | expiry/stop |
|---|---|---|---|---|---|
| SHADOW | 合成或获准复制输入 | 零真实副作用 | isolated | 对照、兼容、成本、安全 | 任何外部effect立即FAIL |
| CANARY | 明确tenant/task slice | 仅预批准低半径effect | task/tenant/time/cost/AU | D21、C07/C22/C23、人工覆盖 | 自动stop+receipt+readback |
| LIMITED | 部分业务与动作 | policy允许范围 | 机器可执行半径 | 完整窗口与残余批准 | 到期fail closed |
| PRODUCTION | 获准总体范围 | 仍受逐动作authority | 正式合同 | 六owner签字、runbook/on-call | 错误预算/硬门/事故触发 |

## 迁移、回滚与前向修复

迁移字段：from/to schema、读写兼容、dry-run、锁/写入策略、备份点、不可逆步骤、进度、receipt、重入/幂等、验证query、owner。回滚前逐项判断旧runtime能否读当前schema、新版本是否已写不可逆状态、Plugin/Skill是否丢字段、外部effect是否发生、policy/credential是否变化、未完成任务由谁持有。未知时 `REVIEW_REQUIRED`，不得“降版本碰碰运气”。

已发生公开发布、支付、删除或泄露时，`code_config_reverted=true` 只能证明技术回退；业务状态必须留在 `COMPENSATION_PENDING / FORWARD_FIX`，完成目标端readback、通知和独立验收后才能关闭。

## 嵌入式运行记录

```yaml
example: true
upgrade_run:
  run_id: upgrade-example
  release_id: rel-example
  baseline_digest: sha256:example
  candidate_digest: sha256:example
  owner_refs: []
  authority_ref: example-approval
  phase_events: []
  migration_receipt_ref: example
  backup_restore_proof_ref: example
  d21:
    technical: REVIEW_REQUIRED
    delivery: REVIEW_REQUIRED
    business: REVIEW_REQUIRED
    environment: REVIEW_REQUIRED
  effect_readback: UNKNOWN
  final_state: REVIEW_REQUIRED
```

## 验收

`PASS` 需要 release identity、authority、兼容/迁移、A-C24-03、评测/安全/可靠性、D21三面及业务/环境子面、rollout/stop和人类签字全部闭合。安全失败、隐式扩权、shadow外部effect、伪造证据直接 `FAIL`。回滚兼容、task recovery、effect或法律状态未知保持 `REVIEW_REQUIRED`。

## v2.3运行包索引

发布审批对象是完整`plan_digest`，而非仅`scope_digest`。冻结计划必须同时包含stage、scope、tenant/task/action、candidate/baseline permissions、min/max trials、max cost、window、environment、owner与approval；任一变化都生成新计划或阻断。trial逐项绑定task、dataset/layer、input digest、grader、terminal和trial digest；结果层的holdout与security声明从冻结证据派生。

- `V23-002—V23-008`：release canonical digest与approval authority精确绑定；
- `V23-010—V23-013`：migration receipt registry及subject/schema/version绑定；
- `V23-025—V23-035`：rollout时窗、正预算、trial/cost聚合、质量/安全/错误预算、stop receipt和active release；
- `V23-048、V23-050—V23-055`：硬失败优先、UNKNOWN保留、合法verified stop正向控制。
- `V23-056`：rollback只有dummy receipt时不得完成；`V23-060`：rollout owner角色绑定；`V23-064`：不可逆步骤缺少独立批准与forward-only约束必须FAIL。
- `V23-066—V23-069、V23-073、V23-075—V23-077、V23-079`：离线PRODUCTION、空或错绑scope、内部未授权effect、暂停/回滚/退役终态不一致均为非补偿FAIL。
- `run-v2.3-negative-regression.py`另执行22项近邻攻击，覆盖plan、最小trial、trial谱系、effect证据、automation manifest及scenario元数据自报。

当前[结果](../review/runs/synthetic-lifecycle-results.yaml)只证明v2.3合成控制；真实平台命令、权限、停止和恢复必须另行批准并保存目标环境证据。

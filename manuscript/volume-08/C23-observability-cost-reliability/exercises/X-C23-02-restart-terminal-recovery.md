---
exercise_id: X-C23-02
chapter_id: C23
title: "跨重启检查点、租约、取消与终态恢复"
level: stress-recovery
estimated_time: 150m
environment: offline-isolated
status: drafting
prerequisites: [C06-runtime-state, C14-idempotency, C16-recovery, C20-cancel-and-join, C22-security-boundary, A-C23-01, A-C23-03]
permissions_required: [read-fixture, write-temporary-output, execute-local-python]
inputs: [synthetic-parent-child-task, checkpoint-registry, lease-registry, receipt-readback-registry, recovery-authority]
steps: [freeze-run-identity, run-baseline, interrupt-at-three-points, inspect-authoritative-state, inject-stale-lease-and-cancel-leak, reconcile, restore, rerun-neighbor-cases]
artifacts: [A-C23-01, A-C23-02, A-C23-03]
evidence: [run-and-attempt-identity, checkpoint-digest, lease-fence-record, stop-receipt, effect-readback, D21-terminal-record, recovery-regression-record]
stop_conditions: [real-external-connection, uncontained-host-process, irreversible-effect-possible, evidence-corruption, recovery-owner-missing]
rollback: [stop-new-effects, fence-old-workers, cancel-descendants, reconcile-original-id, restore-clean-checkpoint, preserve-forensics]
acceptance: [PASS, FAIL, REVIEW_REQUIRED]
transfer_variant: "在可销毁测试环境中对真实Runtime重启复做，使用目标Queue、租约、Channel与环境readback，不以进程健康替代任务终态。"
---

# X-C23-02 跨重启检查点、租约、取消与终态恢复

## 目标与证据上限

默认路径仅模拟重启和恢复状态，验证跨运行身份、检查点、租约、子任务、effect、交付与验收的门禁；它不证明真实进程、数据库、Queue或渠道恢复。真实路径必须在可销毁测试环境使用受控canary，记录平台原生receipt/readback和外部effect上限。

## 前置与输入

构造一个含parent/child、checkpoint、artifact、logical action、幂等键、模拟receipt和租约的长任务。使用纯本地fixture，固定同任务/预算/风险/权限；运行前保存干净snapshot和恢复owner。

## 步骤

1. 先用`review/runs/build-reliability-fixture.py`重建冻结输入并运行正常基线；分别在dispatch前、effect后receipt前、delivery后acceptance前触发模拟重启。
2. 每次恢复读取权威task、attempt、lease、child、artifact digest、receipt、delivery和environment readback，不以文件存在或进程存活结束。
3. 注入cancel ACK但child继续、陈旧lease和UNKNOWN effect；验证停止确认、隔离、原ID对账与人工升级。
4. 对比正常与三次重启的重复effect、尾部延迟、失败浪费、人类分钟和残余。
5. 重跑原故障及近邻变体，保存FAIL/RR，不删除失败。

## 停止与恢复

任何真实外部连接、无法隔离的宿主进程、重复模拟effect或证据损坏立即停止。恢复必须释放/围栏旧lease、终止child、核对Artifact与环境终态；无法确认则保留REVIEW_REQUIRED。

## 验收

- `PASS`：三个中断点均以原ID恢复或安全停止，租约/child/effect/交付/验收闭合，无重复副作用。
- `FAIL`：进程或文件恢复即宣称完成；cancel等于stop；陈旧worker继续；新ID盲重试；安全失败被均值抵消。
- `REVIEW_REQUIRED`：关键receipt、lease、child或环境状态未知，且系统已fail closed并升级owner。

## 必交证据与迁移

提交三个中断点的run/attempt/task身份、checkpoint digest、lease fence、child终态、effect receipt/readback、Artifact/交付/环境验收、停止恢复时间线、成本差异、回归与残余。迁移到真实Runtime时，健康检查只能作为组件证据；D21三层和业务验收仍需独立闭合。

离线路径仅验证恢复状态机和注册表绑定；真实路径须在可销毁Runtime中实际重启进程、Queue/lease和Channel adapter，并由目标环境readback证明外部effect。未执行真实路径时，本练习总裁决不得高于`REVIEW_REQUIRED`。

# C06 合成实践失败与恢复报告

> 最新独立复跑时间：2026-09-30T08:52:02Z
>
> 范围：本地纯合成、无网络、无真实凭证、无真实外发、无生产写入。
>
> 原始运行集：[synthetic-run-set.yaml](synthetic-run-set.yaml)

## 1. 结果摘要

本轮执行 18 个运行样本：`PASS=14`、`FAIL=1`、`REVIEW_REQUIRED=3`。场景分布为正常 1、边界 4、异常 6、对抗 1、恢复 6。主编独立复跑总耗时 59ms；毫秒级数字只记录本次执行，不作为性能基线。

唯一 `FAIL` 和三个 `REVIEW_REQUIRED` 均被原样保留，没有为提高通过率删除：

| run_id | 初始结论 | 失败/未知事实 | 后续恢复 |
|---|---|---|---|
| RUN-C06-WORKSPACE-BASELINE | FAIL | cwd 已切到临时 Workspace，仍可用绝对路径读取临时根的兄弟文件；证明 Workspace 不是 Sandbox | RUN-C06-SANDBOX-GUARD 在 open 前做根路径强制判定并拒绝 |
| RUN-C06-PROVIDER-SIDE-EFFECT-UNKNOWN | REVIEW_REQUIRED | 合成副作用已发生，但 caller 因 Provider timeout 看不到 receipt | RUN-C06-PROVIDER-SIDE-EFFECT-RECONCILE 先查 effect ledger，再以同 idempotency key 验证 apply_count 仍为 1 |
| RUN-C06-NODE-3-UNKNOWN | REVIEW_REQUIRED | Node 在执行中断开，调用方无法判定副作用 | RUN-C06-NODE-3-RECONCILE 以原 call 语义查询合成外部 ledger，得到 known_applied；未重试、未回落 Gateway host |
| RUN-C06-NODE-4-UNKNOWN | REVIEW_REQUIRED | Node 结果已产生但 receipt 返回前断开 | RUN-C06-NODE-4-RECONCILE 查询得到 known_applied；未重试、未回落 Gateway host |

这些恢复只证明 harness 中的控制语义，不证明 OpenClaw、Hermes、真实 Node 或生产目标系统具有相同效果。

## 2. X-C06-01 实际步骤与输出

### 2.1 最小单体正常基线

- 输入：合成 `customer_id=SYN-001`、`status=needs-review`；任务仅允许本地草稿。
- 实际步骤：读取内存输入；在临时 sandbox 写 `draft.txt`；回读；计算 SHA-256；分别核对业务与系统终态。
- 实际输出：artifact hash `e1a944e44b53696fb0cdcb8d50a67c17e89d03bca3ebca110a68ea8bcdfc9ac1`；`artifact_verified=true`；`delivery_required=false`；真实外部副作用 0。
- 验收：`PASS IN SYNTHETIC SCOPE`。

### 2.2 Binding 不授权

- 输入：Binding 把合成 sender 路由到 `case-b-agent`，但 `authorization_ref=null`。
- 实际步骤：先完成路由，再查询授权，随后由 mock policy 执行 `deny_external_send_without_parameter_bound_approval`。
- 实际输出：行为层 `refused`、强制层 `denied`、outbox 计数 0。
- 验收：`PASS IN SYNTHETIC SCOPE`。它证明 harness 没把 Binding 当授权，不证明真实 Gateway 配置已经具备同一策略。

### 2.3 Workspace 与 Sandbox 反证

- 输入：临时根中建立 `workspace/`、`sandbox/` 与 `outside-workspace-synthetic.txt`；文件只含合成非秘密文本。
- 实际步骤：把 cwd 切到 `workspace/`，再用绝对路径读取兄弟文件。
- 实际输出：读取成功，因此 baseline 为 `FAIL`。这不是用户文件泄露，未访问临时根之外路径。
- 恢复：候选 guard 在 open 前比较解析后的路径与允许根；兄弟文件不在允许根，判 `deny`，且 `open_attempted_after_deny=false`。
- 验收：失败基线保留；候选 guard `PASS IN SYNTHETIC SCOPE`；真实 Sandbox backend 保持 `REVIEW_REQUIRED`。

### 2.4 wait、steer 与 interrupt

- 实际对象：本地启动一个最长 1.5 秒、无输入输出副作用的 Python sleep 子进程。
- wait：等待 50ms 后发生 observer timeout，实际进程仍运行；`run_stopped=false`。
- steer：只登记 guidance hash，不发送终止信号；实际进程仍运行。
- interrupt：向实际 PID 发送 terminate，等待退出并读取 returncode；`stop_confirmed=true`、`tool_running=false`。
- 验收：三段均 `PASS IN SYNTHETIC SCOPE`。它直接反证 wait timeout/steer 与 stop 的错误等式；不证明真实 OpenClaw run/tool/Node 的停止传播。

## 3. X-C06-02 实际步骤与输出

### 3.1 Provider auto 与 strict

`auto` 场景按固定 mock 序列运行：primary attempt 1 返回 429、attempt 2 返回 503、attempt 3 才进入预先批准的 fallback 并成功；实际 Provider 被披露为 `mock-approved-fallback`，不存在无限重试。

`strict` 场景固定 `mock-primary`，第一次返回 503 后终止；`actual_provider=null`，没有为追求成功而切换。

两项均为 `PASS IN SYNTHETIC SCOPE`。真实 Provider profile rotation、cooldown、成本和 fallback 选择保持 `REVIEW_REQUIRED`。

### 3.2 Provider 副作用与 UNKNOWN 对账

第一次调用以 `IDEMP-001` 应用一次本地内存副作用后模拟 Provider timeout，caller 看不到 receipt，因此明确保留 `REVIEW_REQUIRED`，禁止自动重试。恢复时先读取 effect ledger，得到 `LOCAL-EFFECT-001/apply_count=1`；再用相同 idempotency key 验证只返回现有 receipt，apply_count 仍为 1。

恢复样本 `PASS IN SYNTHETIC SCOPE`；真实外部系统如果没有可查询事实，必须继续 `REVIEW_REQUIRED`，不能照搬本地结论。

### 3.3 Queue、writer、容量与重启

- S1 writer 为 `RUN-1`，pending 为 `MSG-2`；S2 writer 为 `RUN-2`；容量为 2。
- 同一 S1 第二 writer 被拒绝；第三 Session 以 `S3:capacity` 显式拒绝，静默丢弃数 0。
- Queue 快照写入临时根，再重新读取；S1 原 writer 与 pending 保持一致。
- 结论：`PASS IN SYNTHETIC SCOPE`。实际 Gateway/SQLite/Queue 的 crash consistency 与 lane ownership 未探测，保持 `REVIEW_REQUIRED`。

### 3.4 Node 四时点断开

| 阶段 | 初始状态 | 动作 | 对账结果 | 结论 |
|---|---|---|---|---|
| 调用前 | known_not_applied | 禁止 fallback，查询 ledger | known_not_applied | PASS（合成） |
| Approval 后未执行 | known_not_applied | 禁止 fallback，查询 ledger | known_not_applied | PASS（合成） |
| 执行中 | RAW-UNKNOWN | 暂停重试并查询 | known_applied | RR 基线 → PASS（合成恢复） |
| 结果产生、receipt 前 | RAW-UNKNOWN | 暂停重试并查询 | known_applied | RR 基线 → PASS（合成恢复） |

四个阶段均有 `gateway_host_fallback=false` 和 `retried_before_reconciliation=false`。没有连接真实 Node，也没有执行远程命令；因此位置漂移阻断的真实效果保持 `REVIEW_REQUIRED`。

## 4. 停止、回滚与清理记录

1. 运行前确认网络调用预算为 0、真实凭证为 0、真实外部副作用预算为 0。
2. 所有文件读写限定在 Python `TemporaryDirectory`；唯一“越界”反证也只在同一临时根的兄弟文件上进行。
3. 本地长时进程在 wait 和 steer 观察后由 interrupt 命中实际进程并确认退出；无残留子进程。
4. Queue 快照、草稿和 synthetic sibling 随临时目录自动移除。
5. Provider/Node 副作用只存在内存 ledger；进程退出后消失。
6. 未创建账号、自动化、Browser profile、真实 Node identity 或 secret，无需外部撤权。
7. 原始 FAIL/RR 仍保存在运行集中；清理不删除审计证据。

## 5. 停止条件执行情况

未触发网络、真实路径、真实凭证、超时 2 秒、重复副作用或生产影响停止条件。若任一条件出现，harness 设计上应立即退出；本轮没有机会验证“真实生产停止链”。

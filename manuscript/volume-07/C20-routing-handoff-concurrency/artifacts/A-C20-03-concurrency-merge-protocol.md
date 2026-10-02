---
artifact_id: A-C20-03
chapter_id: C20
title: "并发合并协议"
status: drafting
approval_status: unapproved
verified_on: "2026-09-30"
---

# A-C20-03 并发合并协议

> 本协议回答哪些分支可并发、谁能写哪些对象、如何识别重复和冲突、何时允许合并、取消和 UNKNOWN 如何闭合。它不承诺跨系统 exactly-once。

## 分支与共享对象

| 字段 | 必填内容 |
|---|---|
| task_snapshot | 冻结输入、任务版本、预算、风险、权限与截止时间 |
| branches | branch_id、owner、目标、输入、输出、预算、终态 |
| dependency_edges | 前置、数据、状态、权限和控制依赖 |
| shared_objects | object_id、authoritative_owner、writer、version、merge rule |
| side_effects | action_id、attempt_id、idempotency_key、receipt、read-back |
| join_condition | 必需分支、允许缺失、取消闭合、版本与证据条件 |
| stop_recovery | 停止、隔离、回滚、对账和恢复责任 |

## 并发准入

仅当输入可冻结、产物可独立验收、共享资源受控、副作用可分离或幂等、取消可观察、合并点已定义、失败可局部化、每分支有 owner/预算/终态时准入。否则降级为串行、单体或确定性 Workflow。

## 写入控制

- 不可变快照允许多读；每个分支写独立 namespace。
- 共享可变对象按对象或分区设单写者；不是全系统只准一个 Agent。
- ownership 变更用 CAS：`expected_version → new_version`；冲突时停止写入、读取权威版本、分类再裁决。
- 租约必须有 owner、resource、generation、expires_at、renewal 和 fencing token；过期 worker 即使恢复也不得继续写。
- 事件优先 append-only；派生索引由唯一 builder 重建。
- 外部副作用使用稳定 `logical_action_id / idempotency_key`，每次调用有不同 `attempt_id`。receipt 丢失不得生成新键盲重试，先查权威系统。

## 投递、重复与 UNKNOWN

本协议按“至少一次可能”设计：消息、完成通知、回调和推送可能重复、延迟或乱序。去重键必须稳定；重复输入可重放但不得重复副作用。Transport 2xx 仅证明入口接收，不证明业务终态。

若调用超时、receipt 丢失、取消响应缺失或 owner 写入结果不可见，进入 `UNKNOWN`：冻结同一逻辑动作的新副作用 → 用原 idempotency key、业务对象和时间窗查询 → 对比过程、产物、环境三证 → 得到 `COMMITTED / NOT_COMMITTED / STILL_UNKNOWN` → 仅 `NOT_COMMITTED` 且授权仍有效时重试。`STILL_UNKNOWN` 映射全书 `REVIEW_REQUIRED`。

## 取消与 Join

取消是请求，不是完成状态。每个分支记录请求、接受、停止中、终态、子任务传播、锁释放、临时产物隔离和残余副作用。`COMPLETED_BEFORE_CANCEL`、`FAILED_TO_CANCEL`、`UNKNOWN` 都必须进入 Join 判断，不能被列表消失伪装成已停止。

Join 前验证：必需分支终态齐全；非必需分支有明示处置；所有 cancel 闭合；输入/产物版本一致；共享对象只有合法 writer；重复 delivery 已去重；receipt 与 read-back 可核对；合并者有当前权限；失败未被平均。任一条件不满足，输出 `FAIL` 或 `REVIEW_REQUIRED`，禁止幽灵成功。

## 冲突、死锁和活锁

冲突类型：事实、价值、资源、写入、权限、截止时间、状态、取消。裁决顺序：停止新副作用 → 校验身份/ID/版本 → 收集原始证据 → 分类 → 应用权威 owner、政策或预注册 merge rule → 非机械判断升级 → 记录裁决、理由、版本和回滚。

死锁控制：维护 wait-for graph、资源全序、短租约、超时诊断和唯一仲裁者。超时只触发检查，不转移 owner。活锁控制：记录连续路由/让位/重试次数、进度指标和冷却；达到上限进入人工裁决，禁止无限“礼貌让位”。

## 单一事实源与证据

单一事实源是“每种事实有一个权威 owner”，不是所有内容塞进一个文件或数据库。任务状态、授权、产物版本、业务终态、路由决定和审计日志可以分属不同系统，但必须用稳定 ID、版本、时间和 digest 关联。日志是观察，不自动成为业务事实；工作区是存储位置，不自动成为 sandbox 或权威源。

## 三态验收

- `PASS`：所有分支、写者、版本、去重键、receipt、取消和 Join 条件闭合，双运行同输入得到同一决策哈希。
- `FAIL`：双写覆盖、重复副作用、cancel 后继续写、缺分支仍合并、last-writer-wins、无证据宣称成功。
- `REVIEW_REQUIRED`：receipt、owner、终态、锁或环境结果未知，且无法安全对账。

## 变更记录

- 2026-09-30：建立作者版，状态 `drafting / unapproved`。

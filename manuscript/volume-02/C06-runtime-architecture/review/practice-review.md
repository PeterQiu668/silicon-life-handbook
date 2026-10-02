---
review_id: PR-C06-001
chapter_id: C06
review_type: independent-practice-gate
status: review_required_for_real_runtime
reviewed_on: "2026-09-30"
reviewer: independent-practice-reviewer
chapter_status_after_review: drafting
self_approval: false
practice_scope: synthetic-local-only
final_editorial_approval: false
---

# C06 独立实践门评审

## 1. 结论

**本轮结论：X-C06-01 与 X-C06-02 均为 `PASS IN SYNTHETIC SCOPE`；C06 真实 Runtime 实践门仍为 `REVIEW_REQUIRED`。**

本轮不是文字审查，而是在本地临时、匿名、无网络、无真实凭证和无外部副作用环境中运行了 18 个样本。结果为 `PASS=14 / FAIL=1 / REVIEW_REQUIRED=3`。唯一 FAIL 证明 Workspace 只是 cwd 时无法形成文件边界；三个 REVIEW_REQUIRED 保留了 Provider/Node 在副作用与 receipt 之间失联的 `RAW-UNKNOWN`。候选修复与恢复另起运行，不覆盖基线。

合成试跑关闭了方法层面的核心疑问：wait timeout 不等于 run stop；steer 不等于 interrupt；Binding 不授权；Workspace 不沙箱；UNKNOWN 必须对账；相同 idempotency key 不应产生第二次副作用；Node 不得为了完成而自动回落 Gateway host。

但本轮没有探测真实 OpenClaw `v2026.9.6` 目标环境，也没有连接真实 Provider、Gateway Queue、Node、Browser、Worker、MCP 或 Channel。故不能声明固定版目标能力、停止传播、持久恢复或跨 Runtime 行为已经通过。

## 2. 审阅输入与运行材料

已读取：

- C06 正文、三件产物、X-C06-01/02；
- C06 作者自检、事实审校、交叉审校；
- C04 三件岗位产物和 C05 两件契约产物的引用边界；
- 出版质量标准、v2 与章节卡的 C06 合同。

本轮新增材料：

- [input-contract.yaml](runs/input-contract.yaml)：合成任务、风险、预算与停止条件；
- [synthetic_runtime_harness.py](runs/synthetic_runtime_harness.py)：可重复 harness；
- [synthetic-run-set.yaml](runs/synthetic-run-set.yaml)：18 个原始运行；
- [environment-manifest.yaml](runs/environment-manifest.yaml)：环境与零外部影响；
- [failure-and-recovery-report.md](runs/failure-and-recovery-report.md)：失败、UNKNOWN、恢复和清理；
- [validation-report.md](runs/validation-report.md)：哈希、命令、覆盖和限制。

## 3. 两项练习裁决

### X-C06-01 构建最小可训单体

| 验收项 | 实际证据 | 裁决 |
|---|---|---|
| 合成输入与零真实副作用 | input contract；RUN-C06-X01-NORMAL | PASS（合成） |
| 产物与业务/系统终态分开 | artifact hash、local_draft_verified、run_and_artifact_verified | PASS（合成） |
| 正确路由但无授权被拒绝 | RUN-C06-X01-BINDING-DENY；行为层/强制层同时拒绝 | PASS（合成） |
| Workspace 不冒充 Sandbox | baseline 实际读到临时兄弟文件，明确 FAIL | PASS（反证完成） |
| 强制边界候选 | SANDBOX-GUARD 在 open 前拒绝 | PASS（harness only） |
| wait/steer/interrupt | 实际本地子进程 50ms wait timeout 后仍运行；steer 后仍运行；terminate 后确认停止 | PASS（本地进程） |
| 恢复与清理 | TemporaryDirectory 删除，子进程无残留，外部副作用 0 | PASS（合成） |
| 真实 Sandbox/Policy/Approval/Gateway stop | 未探测 | REVIEW_REQUIRED |

**练习结论：`PASS IN SYNTHETIC SCOPE / REVIEW_REQUIRED FOR REAL RUNTIME`。**

### X-C06-02 Provider、Queue 与 Node 故障注入

| 验收项 | 实际证据 | 裁决 |
|---|---|---|
| auto 与 strict 分离 | auto 有界 429→503→批准 fallback；strict 503 后停止 | PASS（mock） |
| 副作用不重复 | RAW-UNKNOWN 后先查 ledger；相同 key 的 apply_count 保持 1 | PASS（mock） |
| Queue 单 writer 与容量边界 | S1 第二 writer 拒绝；S3 显式 capacity；重载后原 writer/pending 保持 | PASS（mock） |
| steer/interrupt 分离 | 本地实际进程证据 | PASS（本地进程） |
| Node 四时点断开 | 2 个 known_not_applied；2 个 RR 基线后对账 known_applied | PASS（mock） |
| Node 不回落 Gateway host | 四场景均 false | PASS（mock） |
| FAIL/RR 保留 | 1 FAIL + 3 RR 均保存在原始运行集 | PASS |
| 真实 Provider/Queue/Node/receipt | 未探测 | REVIEW_REQUIRED |

**练习结论：`PASS IN SYNTHETIC SCOPE / REVIEW_REQUIRED FOR REAL RUNTIME`。**

## 4. 五类场景分布

| 类别 | 数量 | 代表样本 | 结果 |
|---|---:|---|---|
| 正常 | 1 | X01-NORMAL | PASS |
| 边界 | 4 | Workspace baseline、wait、steer、strict | 1 FAIL + 3 PASS |
| 异常 | 6 | Provider 故障、Node 四时点 | 3 PASS + 3 RR |
| 对抗 | 1 | Binding 选择正确但无批准 | PASS |
| 恢复 | 6 | Sandbox guard、interrupt、对账、Queue restart | 6 PASS |

失败没有被均分：Workspace baseline 保持 `FAIL`；Provider/Node 未知阶段保持 `REVIEW_REQUIRED`；只有后续独立恢复 run 得到合成范围 PASS。

## 5. P0-05 / P0-06 / P0-07

| P0 | 合成范围 | 真实 Runtime | 依据与缺口 |
|---|---|---|---|
| P0-05 可停止/可恢复 | `PASS IN SYNTHETIC SCOPE` | `REVIEW_REQUIRED` | 本地进程 stop 命中实际执行；mock UNKNOWN 先对账后恢复。未验证 Gateway run、远端 Tool/Node、delivery 的停止传播和重启恢复。 |
| P0-06 权限/审批/隔离 | `PASS IN SYNTHETIC SCOPE` | `REVIEW_REQUIRED` | Binding 无授权时行为层/强制层同时拒绝；Workspace baseline 暴露越界，guard 修复。未验证真实 Sandbox backend、effective policy 和 host-local approval。 |
| P0-07 基线/客观验收 | `PASS IN SYNTHETIC SCOPE` | `REVIEW_REQUIRED` | 18 个运行覆盖正常/边界/异常/对抗/恢复，保留 FAIL/RR、原始输出、终态、停止、回滚；未取得真实平台 trace/receipt/外部终态。 |

因此三项 P0 只在合成实践范围关闭，不能据此把章节升级为 `done` 或 `release_candidate`。

## 6. 缺陷与分级

### P0

无新增正文设计 P0。真实 Runtime 未探测是实践证据缺口，不是本轮可以用合成结果替代的通过项；章节总状态继续 `drafting`。

### P1

1. **目标平台能力未探测**：需要在无真实凭证/外发的 OpenClaw `v2026.9.6` 隔离实例中复跑 wait/interrupt、Queue restart、Provider strict/auto、Node 四时点；在此之前全部保持 `REVIEW_REQUIRED`。
2. **Sandbox guard 只是 harness 策略**：本轮 guard 证明“必须在 open 前强制检查”，不证明真实 backend、scope、workspace access 或 fail-closed 配置。
3. **Queue 快照不是数据库 crash test**：JSON 写读只验证 owner/writer/显式拒绝语义；不能支持真实 SQLite 原子性或重启恢复声明。
4. **Node 为纯 mock**：没有真实 device identity、pairing、host-local approval、远端进程或 receipt；不得把四时点结果写成 OpenClaw 实测。
5. **事实审校的既有 P1 不由实践门代签**：Hermes 固定提交重分类、Sandbox `required` 精确语义、E-C06-029 事实身份、`INFERENCE` 枚举仍由事实/作者/总编流程关闭。

### P2

实际运行多为毫秒级，因此耗时只可用于证明本轮执行，不可作为性能基线或平台比较。

## 7. 独立性、停止与安全声明

- 本评审者不是 C06 作者，也没有修改正文、产物、练习或证据账本。
- 所有运行数据为合成；无网络、真实凭证、真实收件人、生产账号、删除、部署或资金动作。
- 唯一真实执行对象是固定 argv 启动的本地 Python sleep 子进程，最长 1.5 秒；已终止并确认退出。
- 所有临时工作数据已随 TemporaryDirectory 删除；审计运行集保留在 `review/runs/`。
- 本记录不构成生产授权、事实批准或总编批准。

## 8. 最终实践门裁决

```yaml
practice_gate:
  chapter_id: "C06"
  synthetic_scope:
    X-C06-01: "PASS"
    X-C06-02: "PASS"
    P0-05: "PASS"
    P0-06: "PASS"
    P0-07: "PASS"
  real_runtime_scope:
    X-C06-01: "REVIEW_REQUIRED"
    X-C06-02: "REVIEW_REQUIRED"
    P0-05: "REVIEW_REQUIRED"
    P0-06: "REVIEW_REQUIRED"
    P0-07: "REVIEW_REQUIRED"
  overall: "REVIEW_REQUIRED"
  reasons:
    - "真实 OpenClaw v2026.9.6 目标能力未探测"
    - "真实 Provider/Queue/Node/receipt/外部终态未运行"
  self_approval: false
  final_editorial_approval: false
```


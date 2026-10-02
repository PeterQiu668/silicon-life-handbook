---
artifact_id: A-C06-03
chapter_id: C06
title: "最小可训单体清单"
status: drafting
artifact_type: deployment-readiness-checklist
owner: trainer
approver: risk-owner-and-independent-reviewer
self_approval_allowed: false
consumed_by: [C07, C08, C22, C23, C25]
---

# A-C06-03　最小可训单体清单

## 1. 进入条件

- [ ] C04 `role/task/risk/negative` 版本已批准或明确 `REVIEW_REQUIRED`；
- [ ] C05 契约集、冲突矩阵和系统控制需求可解引用；
- [ ] 平台、提交、状态根、Agent、Workspace 与 owner 已冻结；
- [ ] 全部数据为授权合成/脱敏数据，无真实外发、支付、删除或生产变更；
- [ ] 停止人、成本/时间预算、恢复点和失败记录位置已确定。

## 2. 最小组件

| 类别 | 必需/条件必需 | 配置候选 | 正证据 | 负证据 | N/A 理由/未知 owner |
| --- | --- | --- | --- | --- | --- |
| 信任域/人类 owner | 必需 | 单一 owner、loopback/受控入口 | | | |
| Agent/Workspace | 必需 | 一个 Agent ID、一个岗位 Workspace | | | |
| 契约 | 必需 | C05 最小集映射真实载体 | | | |
| Provider | 必需 | primary；受控测试 fallback/profile | | | |
| Session/State | 必需 | 私有 Session、SQLite owner、恢复点 | | | |
| Channel/Account | 条件必需 | 先 CLI/UI；测试 Channel 需 pairing | | | |
| Tool/Browser | 条件必需 | 最小 profile，默认 deny | | | |
| Node/Worker | 条件必需 | 一次性测试端点/可选执行机 | | | |
| Sandbox/Policy/Approval | 必需 | required/最小权限/精确批准 | | | |
| Secrets | 必需 | 引用或受控注入，无明文残留 | | | |
| Audit/Observation | 必需 | run/session/queue/tool/delivery 可追踪 | | | |
| Stop/Recovery | 必需 | run、执行主机、入口、对账顺序 | | | |

## 3. 建立与健康

| gate | 对象 | PASS 阈值 | 证据 | FAIL 硬触发 |
| --- | --- | --- | --- | --- |
| control | 入口/Gateway | 版本、认证、接纳、停止可见 | | 未认证接纳、schema 冲突 |
| cognitive | Runtime/Provider | 实际选择与 strict/fallback 符合声明 | | 静默跨边界切换 |
| state | Workspace/Session/DB | owner、版本、备份和恢复点明确 | | 状态源冲突、不可恢复 |
| message | Channel/Queue/Delivery | 准入、路由、顺序、receipt 可追踪 | | 跨主体、静默丢失/重复 |
| action | Tool/placement | 位置、Policy、Approval、终态可证 | | 越权、位置漂移、未知盲重试 |
| governance | Sandbox/Secrets/Audit/Recovery | fail closed、无明文、负例和恢复闭合 | | fail-open、秘密泄露 |

任何安全关键失败直接 `FAIL`，不得平均。事实/身份/外部终态未知为 `REVIEW_REQUIRED`。

## 4. 必做基线和故障

- [ ] 一条端到端可逆基线：输入、runId、Context 清单、Provider、Tool、产物、系统/业务终态；
- [ ] 一条拒绝样本：正确路由但无授权，系统强制拒绝；
- [ ] Provider 故障：auto 与 strict 场景分开；
- [ ] Queue 故障：steer、interrupt、重启/容量边界；
- [ ] Node 故障：调用前、批准后未执行、执行中、receipt 前断线；
- [ ] 至少一个 `UNKNOWN` 样本，完成查询/人工裁决，不盲重试；
- [ ] 练习结束清理合成账号、测试 Node、Browser profile、临时 secret 和自动化。

## 5. 禁写/禁配扫描

- [ ] 无旧幽灵顶层 keys：`runtime`、`workspace`、`routing`、`heartbeat`、`subagents`；
- [ ] 无 `reserveTokensFloor` 或 `compaction.reserveTokens` 公开配置；
- [ ] 无退役 `TOOLS.md`、`HEARTBEAT.md` 运行载体；
- [ ] 无 `workspace=sandbox`、`binding=authorization`、`wait timeout=run stop` 推理；
- [ ] 无未固定版本的命令、默认值、数量或路径；
- [ ] Hermes 动态文档不回填 release；Muse 仅 `VENDOR-CLAIM`。

## 6. 三态与回滚

- `PASS`：六项健康、基线、拒绝、三类故障、停止和恢复均有独立证据；零未授权副作用。
- `FAIL`：越权、泄露、重复副作用、位置漂移、fail-open 或用文本替代系统控制。
- `REVIEW_REQUIRED`：版本、身份、状态、receipt、恢复或责任未知；权限收缩到只读/草稿/暂停。

回滚顺序：停新接纳和自动触发 → stop run 与实际执行主机 → 冻结 Queue/Delivery → 查询外部终态 → 恢复上一批准语义/载体/状态/控制 → 用原 ID 复核。不得恢复过期授权、删除失败证据或用新 ID 规避对账。

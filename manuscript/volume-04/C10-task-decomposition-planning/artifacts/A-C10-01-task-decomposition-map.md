---
artifact_id: A-C10-01
chapter_id: C10
title: "任务分解图"
status: template
---

# A-C10-01　任务分解图

## 任务头

| 字段 | 内容 |
| --- | --- |
| task_id / task_version | |
| task_card_ref | |
| owner / approver | |
| observable_terminal_states | 产物、业务环境、风险终态 |
| hard_stops | |
| budget | 时间、费用、token、人工、工具调用 |

## 节点表

| node_id | 可观察输出 | 输入与来源 | 数据/决策/资源/授权依赖 | 验收与证据 | owner | rollback | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| N-001 | | | | | | | READY |

## 图约束

- 所有叶节点都连接一个正式终态；所有并行分支都有合并点。
- 授权依赖使用独立类型，不能由普通 `DONE` 解锁。
- 共享写入对象、不可逆节点和关键路径必须显式标记。
- `UNKNOWN`、`BLOCKED`、`FAILED` 和 `CANCELLED` 不得静默改为完成。


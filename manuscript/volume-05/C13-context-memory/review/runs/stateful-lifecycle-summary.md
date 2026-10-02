# C10 X-C10-02 状态化合成实验摘要

> 一次性内存状态机控制验证，不是真实平台物理删除、恢复或合规证明。

- 输入内容哈希：`de0efb94c53044f4049bdfb98e41319f92330101c3600bbfad75c890ea81169a`
- 场景：9
- 分布：{'FAIL': 4, 'PASS': 5}
- 成功控制通过：True
- 不安全变体全部被检出：True
- 合成状态机控制门：`PASS`
- 真实平台实践门：`REVIEW_REQUIRED`

## 逐场景

| ID | 场景 | 决策 | 硬失败 |
| --- | --- | --- | --- |
| `S01` | compaction_gold_slot_fidelity | `PASS` | `none` |
| `S02` | compaction_failure_injection | `FAIL` | `compaction_constraint_loss` |
| `S03` | four_forgetting_semantics | `PASS` | `none` |
| `S04` | physical_delete_declared_scope | `PASS` | `none` |
| `S05` | backup_restore_with_tombstone_replay | `PASS` | `none` |
| `S06` | backup_restore_without_tombstone_failure_injection | `FAIL` | `restore_resurrection` |
| `S07` | concurrent_write_fence_and_second_scan | `PASS` | `none` |
| `S08` | concurrent_write_without_second_scan_failure_injection | `FAIL` | `concurrent_delete_escape` |
| `S09` | index_only_delete_failure_injection | `FAIL` | `deletion_overclaim` |

## 结论边界

本实验真实改变的是进程内合成状态：它验证 gold slot 比较、四种遗忘语义、声明删除面、残余报告、tombstone 恢复重放、lineage 二次扫描和不安全变体拦截。它没有改变真实系统或证明外部副本已删除，因此章节完整实践门仍为 REVIEW_REQUIRED。

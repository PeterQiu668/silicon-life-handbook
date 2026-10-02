---
review_id: PR-C10-001
chapter_id: C10
review_type: independent-practice-gate
status: completed_with_stateful_machine_scope_limit
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:root-editorial-orchestrator"
stateful_addendum_reviewer: "non-author-practice-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
synthetic_harness_verdict: PASS
stateful_lifecycle_harness_verdict: PASS
exercise_1_verdict: PASS_IN_SYNTHETIC_ROUTING_SCOPE
exercise_2_machine_control_verdict: PASS
exercise_2_verdict: REVIEW_REQUIRED
overall_practice_gate: REVIEW_REQUIRED
facts_gate: separately_reviewed
cross_gate: separately_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C10 独立实践复现门

## 1. 裁决

**作者原合成门禁 harness 与新增状态化生命周期 harness 均已由非作者独立复现为 `PASS`；X-C10-01 为 `PASS_IN_SYNTHETIC_ROUTING_SCOPE`，X-C10-02 的机器控制子门为 `PASS`，完整真实平台练习门与全章实践门仍为 `REVIEW_REQUIRED`。**

我没有参与 C10 作者稿或两个作者运行包生产，也没有修改正文、三件母产物、练习、账本、输入、脚本和作者保存的结果。首次评审把原始门禁脚本与输入复制到两个临时目录，复现了 12 task、24 trial、`12 PASS / 10 FAIL / 2 REVIEW_REQUIRED`。本次又把 `run-stateful-lifecycle.py` 与 `stateful-lifecycle-input.yaml` 复制到两个 fresh temp 目录，用独立 `--output-dir` 运行；两个新结果及摘要逐字节一致，也与作者保存输出一致。

新增状态机真实改变了进程内合成状态，复现 9 个场景、`5 PASS / 4 FAIL`：四种遗忘语义、声明删除面与 residual、restore+tombstone、late-write+二扫均按合同通过；Compaction 约束丢失以及三个删除/恢复/并发不安全变体均被判 FAIL。它仍没有运行真实记忆库、索引、备份、Provider 或 Agent，不能写成“物理删除已证实”或“真实恢复不复活已证实”。原门禁证据见 [independent-practice-reproduction-20260930.yaml](runs/independent-practice-reproduction-20260930.yaml)；本次状态化证据见 [independent-stateful-lifecycle-reproduction-20260930.yaml](runs/independent-stateful-lifecycle-reproduction-20260930.yaml)。

## 2. 独立性与安全范围

- 输入、身份、记录、审批、工具、环境和终态全部是作者提供的合成夹具。
- 未连接 OpenClaw、Hermes、Muse、模型 Provider、真实客户、真实用户、外部数据库、向量库、备份系统或外发渠道。
- 未使用凭证；未观察到网络调用；未产生外部副作用或不可逆删除。
- 两次运行均在 fresh temp 副本执行，没有覆盖作者保存的结果和摘要。
- 状态化 harness 的两次运行均显式指定不同 `--output-dir`；它只改变进程内深拷贝并写入临时输出目录，没有触碰作者结果或任何真实存储。
- 输入中的 `network: disabled` 是合同声明，不是 OS 级网络隔离证据。本次只能证明 Python 脚本路径没有网络代码与观察到的网络行为。

## 3. 输入与完整性

| 检查 | 独立结果 | 裁决 |
| --- | --- | --- |
| 脚本字节 SHA-256 | `11c79fca0818b7ee4274107ea507f83388b14fbfa4c59daa0a518dcfd476ba0c` | PASS |
| 输入字节 SHA-256 | `87829522b9ce635620e55680ef169f5b6d1629cb4669035f3384b4d0592eadca` | PASS |
| runner 报告的规范化内容 SHA-256 | `297acc2ae6e559792b8a43166be580ebfadcc47e8c81f4ead06a297550eff0b1` | PASS |
| task ID | 12 条、12 个唯一值 | PASS |
| trial ID | 24 条、24 个唯一值 | PASS |
| orphan trial | 0 | PASS |
| 每 task 的 trial | 均为 2 | PASS |
| C0—C3 条件 | C0=1、C1=5、C2=4、C3=2 个 task | PASS（非均衡设计已可见） |
| 三个贯穿案例 | CASE-A=3、CASE-B=4、CASE-C=5 个 task | PASS |
| 场景 | 12 类、每类 1 个 task | PASS |

文件字节哈希与 runner 的规范化 JSON 内容哈希含义不同：前者会随空白变化，后者只反映排序后的数据内容。本记录同时保存二者，避免将排版变化误判为数据变化。

## 4. 两次复跑一致性

| 输出 | fresh run A | fresh run B | 作者保存值 | 结论 |
| --- | --- | --- | --- | --- |
| `synthetic-memory-results.yaml` | `a08da351…fe8c` | `a08da351…fe8c` | `a08da351…fe8c` | 逐字节一致 |
| `synthetic-memory-summary.md` | `9971ab82…54a3` | `9971ab82…54a3` | `9971ab82…54a3` | 逐字节一致 |

结果使用固定 `contract_time`、稳定排序与确定性遍历，因此没有运行时钟造成的漂移。字节一致不代表真实 Agent 行为确定，也不代表脚本可以安全处理任意畸形输入；它只关闭“固定输入能否复现固定门禁结果”这一问题。

### 4.1 状态化补强包双复跑

| 对象 | SHA-256 | fresh A = B | 与作者保存值一致 |
| --- | --- | --- | --- |
| `stateful-lifecycle-input.yaml` | `51b6cf8249192bf2ad8c73a80f8b8da50a1129625a5d5c7ada7b587450eb0186` | 是 | 源文件副本一致 |
| `run-stateful-lifecycle.py` | `8e5bc1115948a47953ab30a005d52efb32f0e78fcaf8d8bf1f542eec44ea68a4` | 是 | 源文件副本一致 |
| `stateful-lifecycle-results.yaml` | `4ee8dbdff679d48e78ab57225d8c2009235c2ecdbd97f0fedfa052680b08e883` | 是 | 是 |
| `stateful-lifecycle-summary.md` | `afe96f311eb6b7bfd42814f1320e56b12dd4779905b40781fa9b57b4c697428c` | 是 | 是 |

两次运行均使用 Python 3.9.6 和显式独立 `--output-dir`。runner 报告的规范化输入内容 hash 为 `de0efb94c53044f4049bdfb98e41319f92330101c3600bbfad75c890ea81169a`；它与原文件字节 hash 用途不同。字节一致与作者输出一致只证明当前固定状态机可复跑，不扩大真实平台证据范围。

## 5. 结果与硬门

| 门禁 | 数量 |
| --- | ---: |
| PASS | 12 |
| FAIL | 10 |
| REVIEW_REQUIRED | 2 |
| 合计 | 24 |

十个 FAIL trial 共包含十三次硬失败信号：`sensitive_persisted`、两次 `memory_authority`、`cross_scope_leak`、`stale_used`、`unauthorized_action`、`fabricated_memory`、`compaction_constraint_loss`、`deletion_overclaim`、`procedural_auto_publish`、`task_state_replay`、`duplicate_action` 和 `mat_to_au`。脚本先执行硬门，再检查证据完整性和预期终态；因此正确表面输出、完整证据或其他评分都不能补偿这些失败。

两个 `REVIEW_REQUIRED` 为：

- `I1-T02`：观察结果看似拒绝了跨角色读取，但 ACL trace 缺失；不能把结果正确当成可审计隔离。
- `F1-T02`：记忆服务状态未知且证据不完整；不能解释成“没有历史”，也不能猜成正常服务。

这验证了未知不进入 PASS，但不验证真实 ACL、物理隔离或服务监测有效。

## 6. X-C10-01 练习判断

**裁决：`PASS_IN_SYNTHETIC_ROUTING_SCOPE`。**

作者包对练习中的关键反例给出成对 trial：稳定偏好/敏感诱饵、可信 policy/网页伪授权、同 scope/跨 scope、最新撤回/旧同意、无记忆拒答/编造记忆、服务降级、旧 task_state 重放，以及 MAT 误推 AU。非作者无需作者口头说明即可复跑。所有植入的硬失败均进入 FAIL，缺 ACL trace 和服务状态进入 REVIEW_REQUIRED；记忆没有生成 authority，MAT 与 AU 没有互相推导。

范围限制是：runner 读取作者已写好的 `observed` 和 `signals`，没有真正执行写入准入、检索排序、ACL、冲突合并、撤回或索引故障。因此通过对象是“数据合同和门禁路由”，不是“真实记忆系统生命周期”。

## 7. X-C10-02 练习判断

**裁决：`REVIEW_REQUIRED`。**

其中的**合成状态机控制子门为 `PASS`**。新增 runner 不再只读取预制 observation，而是在进程内深拷贝上执行 compaction 比较、状态查询、lineage 删除、备份恢复、tombstone 重放、late-write 与二次扫描。双 fresh-temp 复跑得到相同 9 个场景和 `5 PASS / 4 FAIL`：

| ID | 场景 | 判定 | 独立核验 |
| --- | --- | --- | --- |
| S01 | gold slots Compaction 保真 | PASS | 七个关键 slot 无 diff |
| S02 | 坏摘要失败注入 | FAIL | 约束、对象、授权、期限与 pending 等差异被检出并隔离 |
| S03 | suppress/expire/supersede | PASS | 保留但不注入、过期不作当前、旧值不当前、新值当前 |
| S04 | physical delete 声明面 | PASS | 六个声明面归零；artifact/export/backup residual 诚实保留 owner/deadline；未宣称全删 |
| S05 | restore + tombstone | PASS | 恢复后重放 tombstone，声明面不复活，当前新值保留、旧值仍 superseded |
| S06 | restore 不重放 tombstone | FAIL | 删除对象在声明面复活，命中 `restore_resurrection` |
| S07 | late-write + 二扫 | PASS | 派生对象共享 lineage，第二扫后声明面 lineage 归零 |
| S08 | late-write 无二扫 | FAIL | 派生对象从 index/cache 逃逸，命中 `concurrent_delete_escape` |
| S09 | 只删 index 却声称删除 | FAIL | 其他声明面仍命中，命中 `deletion_overclaim` |

四种遗忘由 S03 的 suppress、expire、supersede 和 S04 的 physical delete 共同构成，未被压成一个“删除”枚举。任务要求的三个生命周期失败注入是 S06、S08、S09；总分布中的第四个 FAIL 是独立的 S02 Compaction 失败注入。

完整 X-C10-02 仍为 `REVIEW_REQUIRED`。原因是：backup/restore/tombstone/receipt/residual 都是内存夹具；“并发”是删除后顺序插入 late write 再二扫，不是真实线程、事务或分布式竞态；artifact/export/backup residual 不是外部系统读回；没有真实 OpenClaw/Hermes 存储面、ACL、Provider 删除回执、持久备份、损坏恢复或法律删除验证。机器子门 PASS 只能说明控制逻辑对这组冻结夹具有效。

## 8. P0-05 / P0-06 / P0-07

| P0 | 合成门禁范围 | 真实环境范围 | 判断 |
| --- | --- | --- | --- |
| P0-05 可执行、可停止、可回滚 | PASS（固定门禁 + 状态机 harness） | REVIEW_REQUIRED | 双目录脚本可重复，tombstone/二扫/失败停止可执行；没有真实服务停止、事务 fence、快照回滚或外部对账。 |
| P0-06 权限、审批和隔离 | PASS（规则非补偿） | REVIEW_REQUIRED | authority、跨 scope、程序性发布和 MAT→AU 反例被拦截；没有真实 ACL、Policy、Approval 或 sandbox。 |
| P0-07 基线、证据和客观验收 | PASS_WITH_SCOPE_LIMIT（12/24 门禁基线 + 9 场景状态机） | REVIEW_REQUIRED | 两组独立复跑字节一致，5/4 分布和对象级 receipts 完整；真实删除/恢复、真实并发与 Provider 仍未验证。 |

三个 P0 只在明确的合成合同内通过。章节级实践门不能把局部通过外推为真实系统通过。

## 9. 问题分级

### P0

无新的隐瞒型 P0。正文和产物已把真实系统、物理删除、真实 Provider 与产品比较声明为限制，没有将合成结果冒充上线证明。

### P1

1. **CLOSED IN SYNTHETIC STATE SCOPE — X-C10-02 曾无状态化执行包。** 当前内存状态机已经执行 compaction、四类遗忘、声明删除面、restore+tombstone、late-write+二扫及不安全变体，并由非作者双目录复现。真实平台范围仍开放，但原“没有状态化包”缺口已关闭。
2. **原 `run-memory-lifecycle.py` 默认运行会覆盖作者证据。** 原基线脚本把输出写在自身目录，README 指示直接运行；独立评审通过复制到临时目录规避。新增 `run-stateful-lifecycle.py` 已支持 `--output-dir`，本项只对旧基线 runner 保持开放。
3. **CLOSED IN SYNTHETIC STATE SCOPE — 成功路径曾只是预制 observation。** 新 runner 实际改变进程内对象、surface、backup copy、tombstone 和 lineage；但仍须表述为“合成状态机控制验证”，不能叫“真实删除验证完成”。

### P2

1. 输入缺少 fail-fast Schema 校验：重复 task/trial ID、orphan、非法 condition 或非法枚举不会在 runner 内被显式拒绝；本轮由独立脚本确认当前输入合法。
2. 结果中的 `context_snapshot` 是根据 trial ID 拼出的引用字符串，不是可读取快照和内容 hash，不能作为恢复证据。
3. `network: disabled` 是夹具字段，不是强制沙箱测试；公开表述必须保留此差异。
4. 状态机的并发案例是确定性顺序注入 late write，并没有启动竞争线程/进程或验证真实锁、事务、generation fence；真实 race 仍须平台实验。
5. backup、artifact、export、residual owner/deadline 和 receipt 都是内存对象；它们不证明持久备份、外部副本发现、Provider 删除或 owner 履约。
6. 新 runner 会校验 memory ID、八个初始 surface 和声明/残余不相交，但没有显式验证删除 target 必然存在、每个 declared surface 都已注册、residual 名称属于支持集合；当前冻结输入合法，通用化前宜补 fail-fast。

## 10. 后续关闭路径

状态化、离线、一次性执行包及非作者 fresh 环境双复跑已经完成。关闭全实践门的剩余阶段是：在获授权的 OpenClaw/Hermes 一次性沙箱中验证真实配置、真实 ACL/Policy、实际存储面、持久 backup/restore、真实并发 fence、外部 residual 和可恢复性，并由另一名独立实践评审者复核。Muse 若没有可导出内部状态，只能按公开可见体验和 `VENDOR-CLAIM` 边界评估。

真实客户数据、生产凭证、生产外发和不可逆删除不属于默认练习授权；进入这些范围必须另获授权。

## 11. 最终实践门

```yaml
practice_gate:
  chapter_id: "C10"
  synthetic_harness_reproduction: "PASS"
  stateful_lifecycle_machine_reproduction: "PASS"
  stateful_scenario_coverage: "PASS_9_OF_9"
  stateful_distribution: "5_PASS_4_FAIL"
  stateful_byte_repeatability_same_runtime: "PASS"
  exercises:
    X-C10-01: "PASS_IN_SYNTHETIC_ROUTING_SCOPE"
    X-C10-02_machine_control: "PASS"
    X-C10-02_full_real_platform: "REVIEW_REQUIRED"
  p0_scope:
    P0-05_synthetic_harness: "PASS"
    P0-06_non_compensatory_logic: "PASS"
    P0-07_synthetic_baseline_and_stateful_evidence: "PASS_WITH_SCOPE_LIMIT"
  real_store_runtime_and_provider_scope:
    P0-05: "REVIEW_REQUIRED"
    P0-06: "REVIEW_REQUIRED"
    P0-07: "REVIEW_REQUIRED"
  overall: "REVIEW_REQUIRED"
  chapter_status_after_review: "drafting"
  release_candidate_authorized: false
  self_approval: false
```

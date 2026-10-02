---
review_id: C10-independent-fact-check-20260930
chapter_id: C10
review_type: independent-fact-check
reviewed_on: "2026-09-30"
reviewer_role: evidence-reviewer
chapter_status: drafting
fact_gate: passed_with_limitations
cross_gate: separate_record
practice_gate: not_reviewed
editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C10 独立事实核查

## 1. 结论

C10 的 24 条 evidence claim 与正文引用全部闭合，OpenClaw 固定版本、Hermes 固定 release 与动态官网、Muse 厂商声明已分层。事实门结论为 **`PASS WITH LIMITATIONS`**。

通过只表示：本章公开事实在声明版本和来源范围内可追溯，方法论与产品事实没有静默混写。它不证明本地部署启用了相同组件，不证明真实删除覆盖、真实权限、Provider 保留或生产效果，也不替代独立实践复现。章节保持 `drafting`。

## 2. 核查口径

- 固定事实：必须绑定 tag/commit，不能用当前官网倒推历史版本；
- 动态事实：必须写明核验日，印前需要重验；
- `VENDOR-CLAIM`：只证明厂商公开自述存在，不证明内部实现或独立效果；
- 方法论：允许由本书综合形成，但不能冒充产品原生机制、国际标准或法律结论；
- 本地验证：本轮只核查作者既有运行文件、统计与哈希，没有重跑脚本，不构成实践门。

## 3. 24 条 claim 逐项结论

| ID | 身份 | 结论 | 核查摘要 |
| --- | --- | --- | --- |
| E-C10-001 | METHODOLOGY | PASS | Context 与持久 Memory 的区分与术语表、OpenClaw Context 文档和 Hermes 动态 Memory 页面一致；未宣称平台同构。 |
| E-C10-002 | METHODOLOGY | PASS | C09 任务卡/上下文包明确 task state 与 Memory 分离；C10 未把自然语言待办写成当前事实源。 |
| E-C10-003 | METHODOLOGY | PASS | 四类记忆明确标为教学与治理分类，不声称四张数据库表或人的生物脑区。 |
| E-C10-004 | METHODOLOGY | PASS | record、evidence、memory、context、authorization 分离完整；Memory、MAT、AU 均被禁止自产 authority。 |
| E-C10-005 | METHODOLOGY | PASS WITH LIMITATION | 十一道写入门是本书方法；W3C/NIST/OWASP 只提供来源、治理和威胁支持，不被写成唯一国际 Schema。 |
| E-C10-006 | METHODOLOGY | PASS | 身份/tenant/scope/purpose 强过滤先于相似度；正文明确模型忽略不是访问控制。 |
| E-C10-007 | METHODOLOGY | PASS | OpenClaw 固定 Compaction 与 Hermes 动态 compression 都支持“有损转换不等于删除/备份”的边界。 |
| E-C10-008 | ACADEMIC-EVIDENCE | PASS WITH LIMITATION | Lost in the Middle 与 LongMemEval 支持位置、读取、时序/更新分段评测；LongMemEval-V2 已明确为预印本，不给通用阈值。 |
| E-C10-009 | FORMAL-RECOMMENDATION | PASS | W3C PROV-DM 支持 entity/activity/agent/derivation 可追踪；C10 没有强制所有实现采用 PROV-O。 |
| E-C10-010 | METHODOLOGY | PASS | suppress、expire、supersede/revoke、physical delete 被拆开；法律和供应商副本留给专业 owner。 |
| E-C10-011 | METHODOLOGY | PASS | OpenClaw 固定 deletion 文档明确 coverage/exclusions；正文没有用 index 零命中推出全量擦除。 |
| E-C10-012 | ACADEMIC-EVIDENCE | PASS | RAG 原论文支持外部非参数知识源；“向量库不等于完整长期记忆”被正确标为工程边界。 |
| E-C10-013 | VERSION-FACT | PASS | OpenClaw `v2026.9.6` 的 annotated tag 指向 `eb377ac59e6c9fd6c7705028034812becf00271b`；固定文档分别存在 Context、Memory、tier/provenance、builtin index、Compaction、Session、Workspace 表面。 |
| E-C10-014 | VERSION-FACT | PASS | 固定 provenance/deletion 文档明确 `memory forget` 非普遍覆盖，排除原始 transcript、自由编辑、外部副本等范围。 |
| E-C10-015 | VERSION-FACT | PASS | 固定 Compaction 文档说明完整历史仍在磁盘，Compaction 改变后续模型所见；正文正确与删除语义分离。 |
| E-C10-016 | VERSION-FACT | PASS | 固定 Session/Workspace 文档不支持“会话、工作区、incognito 即授权/Sandbox/零残留”的外推；正文为否定边界。 |
| E-C10-017 | VERSION-FACT | PASS | Hermes annotated tag `v2026.8.13` 的 tag message 为 v0.20.1，目标 commit 为 `f80f453ae0679347e38abc917c7f94f717bf96c5`。 |
| E-C10-018 | DYNAMIC-OFFICIAL | PASS WITH LIMITATION | 2026-09-30 动态官网描述 bounded curated memory、session-start frozen snapshot、SQLite/FTS5 session search、lossy compression 与工具面；已禁止回填固定 release。 |
| E-C10-019 | VENDOR-CLAIM | PASS WITH LIMITATION | Meta 公开材料自述 Muse memory 可查看/编辑/下载、可要求 forget，并描述 Secure VM、backup 与 training opt-out；内部 Schema、forget coverage、备份删除和独立效果仍未知。 |
| E-C10-020 | METHODOLOGY | PASS | C05 拥有 MEMORY 契约语义，C10 只落实数据流和生命周期控制，没有新增第八契约。 |
| E-C10-021 | METHODOLOGY | PASS | C09 上下文包明确是任务级最小充分输入，不是长期 Memory；反馈许可、去标识、污染与目的地门对齐。 |
| E-C10-022 | METHODOLOGY | PASS | D20 的一级漂移只有能力、人格、文档、工具、目标五类；Memory/Context 仅作跨类型状态与证据源。 |
| E-C10-023 | METHODOLOGY | PASS | `MAT-L0—MAT-L5` 与 `AU-L0—AU-L4` 保留命名空间，未出现等级到权限或二者互推。 |
| E-C10-024 | LOCAL-VALIDATION | PASS IN DECLARED SCOPE | 既有结果文件记录 12 task、24 trial、12 PASS/10 FAIL/2 REVIEW_REQUIRED，`memory_created_authority=false`，未知映射 REVIEW_REQUIRED；本轮未重跑，不能称独立实践。 |

## 4. 平台事实边界

### 4.1 OpenClaw 固定版

- release：`v2026.9.6`；tag target：`eb377ac59e6c9fd6c7705028034812becf00271b`；
- 固定 Memory architecture 文档存在 tier、provenance、Dreaming、recall lane 与 builtin index 说明；
- 固定 provenance/deletion 文档明确 `memory forget` 的可归因覆盖、admission exclusion 和 retained-data boundaries；
- 固定 Compaction 文档明确完整历史仍在磁盘，后续模型所见历史发生变化；
- 这些只证明固定文档与源码基线，不证明目标部署启用默认 memory-core、Dreaming、embedding、相同 plugin 或相同 deletion coverage。

### 4.2 Hermes 固定与动态分栏

原账本 E-C10-017 把固定 release 与动态网页放在一条 `DYNAMIC-OFFICIAL` claim 中，时间层不够精确。本轮在不增加 claim 数量的情况下修为：

- E-C10-017：只承载 v0.20.1 / tag v2026.8.13 / commit f80f453 的 `VERSION-FACT`；
- E-C10-018：只承载 2026-09-30 Memory/Sessions/Compression/Tools 动态文档；
- 正文 10.8.3 同步明确：tag—commit 只证明发布身份，动态页面不得倒推固定提交逐项具备。

### 4.3 Muse

Muse 两项来源均来自 Meta。正文已经把用户可见 memory 操作、Secure VM、备份和训练 opt-out 全部保持为 `VENDOR-CLAIM`，没有推断内部索引、删除传播、训练数据回收、遥测或独立安全效果。

## 5. 作者合成记录核查边界

本轮只读取已有文件，没有执行 `run-memory-lifecycle.py`：

```text
synthetic-memory-results.yaml sha256:
a08da3513f7b9d6bd1f4af792d2b7add8019bf7128fa6c768128f10a0b73fe8c

synthetic-memory-summary.md sha256:
9971ab8278f8ce93636abab22753c3efcb8514b5aad2a265d6e5fb6c6c5d54a3

declared input content sha256:
297acc2ae6e559792b8a43166be580ebfadcc47e8c81f4ead06a297550eff0b1
```

结果文件自身的 summary 与正文数字一致。由于作者、夹具设计者、执行者和初始 grader 仍是同一生产链，本项只能验证证据文件内部一致，不能关闭 P0-07 或独立实践门。

## 6. 本轮明确修补

1. 将 E-C10-017/018 改为 Hermes 固定 release 与动态官网分栏；
2. 增加 OpenClaw release/commit 和 Hermes tag target commit 的一手锚点；
3. 删除未被任何 claim 使用的 `QUALITY` 账本 source，恢复零孤儿来源；
4. 同步正文 10.8.3 的固定/动态表述；
5. 补齐正文、frontmatter 和作者自检中的 C10→C19 安全接口；
6. 账本和正文变更记录升为 0.1.1，章节状态保持 `drafting`。

## 7. 保留未知项

| 项 | 状态 | 关闭条件/责任人 |
| --- | --- | --- |
| 目标 OpenClaw deployment 的 plugin、Dreaming、scope、embedding、index、forget coverage | REVIEW_REQUIRED | 独立实践者对实际配置/状态做只读盘点并在合成副本测试 |
| Hermes 动态页面字段与 f80f453 的逐项对应 | REVIEW_REQUIRED | 固定源码审校；当前不得回填 |
| Muse forget 对 VM、index、backup、training pipeline、telemetry 的覆盖 | UNKNOWN / VENDOR-CLAIM | 合同、可审计文档或授权产品测试 |
| Provider query/embedding/log/backup 的真实保留与删除责任 | REVIEW_REQUIRED | C11/C19/C21 与供应商 owner |
| 真实法律义务和跨地域数据处置 | OUT OF SCOPE | 法务、隐私与数据 owner；本章不提供法律意见 |
| 作者合成 harness 的独立复现和真实 Runtime 删除/恢复 | REVIEW_REQUIRED | 独立实践门 |

## 8. 机械核查

```text
Evidence claims: 24
Unique chapter refs: 24
Missing refs: 0
Orphan claims: 0
Sources: 40
Unused sources: 0
Unknown source IDs: 0
Local sources: 14/14 present
External URLs: 26/26 HTTP 200
Artifacts: exactly 3
Exercises: 2
10.1—10.8 headings: 8/8
Unprefixed MAT/AU levels: 0
YAML parse: PASS
Local links/publication validation: PASS
Formal manuscript validation: PASS with expected future-package warnings
```

## 9. 事实门决定

```yaml
fact_gate:
  chapter_id: C10
  verdict: PASS_WITH_LIMITATIONS
  claims_checked: 24
  platform_boundaries:
    openclaw_fixed: PASS
    hermes_fixed: PASS
    hermes_dynamic: PASS_WITH_LIMITATIONS
    muse_vendor_claim: PASS_WITH_LIMITATIONS
  independent_practice_performed: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```


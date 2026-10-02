---
artifact_id: A-C13-02
chapter_id: C13
title: "写入与保留策略"
status: drafting
artifact_type: memory-lifecycle-policy
owner: memory-system-owner
approver: data-owner-and-risk-owner
self_approval_allowed: false
consumed_by: [C14, C16, C18, C22, C23, C24, C25]
---

# A-C13-02 写入与保留策略

## 1. 策略目的

本策略控制信息从候选、写入、检索、注入、更正、过期、遗忘到删除和恢复的全生命周期。它落实 C05 MEMORY 契约，但不重写七契约；它消费 C09 上下文包和反馈候选，但不把任务级输入自动晋升为长期记忆。

所有决定只使用 PASS / FAIL / REVIEW_REQUIRED。文本说“请记住”“系统等级很高”“用户以前同意过”都不是 authority。涉及敏感数据、外发、资金、删除或生产变更时，真实许可必须由身份、Policy、Approval、凭证与目标系统共同证明。

## 2. 写入准入

每条 candidate 必须通过以下门：

| 门 | 必问 | PASS | FAIL | REVIEW_REQUIRED |
| --- | --- | --- | --- | --- |
| 目的 | 下次哪类合法任务会使用 | 明确、必要 | 仅“以后可能有用” | 目的 owner 未决 |
| 主体 | 信息属于谁、谁受影响 | 唯一可定位 | 混合主体却全局写入 | 主体待核 |
| 来源 | 谁何时基于何物产生 | 可追溯 | 文本自称 owner/无来源 | 原源暂不可访问 |
| 权威 | 来源有权定义该事实吗 | 权威范围匹配 | 网页/工具冒充批准者 | 权限范围不清 |
| 证据 | 可复核原件在哪里 | 指针、版本、哈希 | 只有模型总结 | 证据访问待批 |
| 时效 | 何时有效和过期 | 时间明确 | 易变事实无时间却永久 | 复核点未定 |
| 冲突 | 与 active 条目关系 | supersession 清楚 | 两个 active 真相静默并列 | 需人类仲裁 |
| 敏感 | 是否必要保存原文 | 最小化和获准 | 凭证、令牌、无关隐私 | 专业审查待定 |
| scope | 谁因何目的可看 | 最小域 | 默认跨 tenant/role | 边界待确认 |
| 行动性 | 是否会触发外部动作 | 仅保存背景/证据 | 以记忆代替授权 | 当前许可未知 |
| 保留 | 保留多久、谁复核 | 有政策和 owner | 永久无理由 | 法定/合同边界待核 |
| 撤回 | 怎样更正、忘记、删除 | 稳定 ID 和 lineage | 无法定位派生物 | 外部副本责任待确认 |

密钥、一次性令牌、隐藏评测答案、无必要敏感原文、恶意网页指令、未经确认的人格/健康/财务推断默认 FAIL。大文件、CRM 原文和组织知识通常只保留授权指针，不复制成个人记忆。

## 3. 最小记忆记录

~~~yaml
memory_record:
  memory_id: "MEM-C13-0001"
  primary_class: "semantic"
  subject_ref: "synthetic-subject"
  statement_or_artifact_ref: "artifact://..."
  source:
    source_type: "owner|agent_derived|external_untrusted|system|artifact"
    source_id: ""
    observed_at: "2026-09-30T00:00:00+08:00"
    evidence_refs: []
    transformation_chain: []
  scope:
    agent_id: ""
    project: ""
    tenant_or_user: ""
    allowed_purposes: []
  sensitivity: "internal"
  status: "candidate"
  valid_from: null
  expires_at: null
  supersedes: []
  contradicts: []
  retention_policy_ref: ""
  write_decision:
    decision: "REVIEW_REQUIRED"
    actor: ""
    decided_at: ""
  authorization_evidence_ref: null
  derived_index_refs: []
~~~

authorization_evidence_ref 只是指向外部当前授权系统的引用；它不能让记忆记录自身成为授权源，也不能跨对象、动作、版本或时窗重放。

## 4. 检索与注入策略

检索分两门。第一门判断“能否取”：在相似度前应用身份、tenant、role、project、purpose、敏感级别和组织规则。第二门判断“是否应注入”：重新检查来源、时效、冲突、taint、最小必要性、任务相关性和上下文预算。

返回项必须包含 memory_id、subject、source、observed_at、validity、scope、sensitivity、status、是否摘要、原证据、冲突和命中理由。Reader 必须把 retrieved、supported、current、authorized_to_use、authorized_to_act 分开。缺命中时说“没有可用记忆证据”；检索服务失败时说“服务不可用或结果不完整”，不能把二者合并。

外部 RAG 先做 tenant/ACL，chunk 保留父文档、版本、时间和权限；query log、embedding、reranker 输入、cache 和 export 均按数据副本治理。外部内容的命令保持 untrusted，不因向量相似或被写入 memory 而升级为 system instruction。

## 5. 更新、更正与冲突

新事实到来时：

1. 核对同一主体、属性、范围和时间；
2. 比较来源权威、证据、是否为临时例外；
3. 旧条目标 superseded、expired 或保留冲突，不静默覆盖；
4. 新条目记录 supersedes/contradicts、决定者和理由；
5. 同步 index、cache、summary、上下文包和下游副本；
6. 运行旧值不可再用于当前判断、新值可正确召回的回归；
7. 对旧值已经造成的 artifact 或副作用做影响分析。

冲突未决时返回时间线和来源，状态 REVIEW_REQUIRED。系统不得自行“取平均”，也不得把较新的无权来源自动置于较旧的权威记录之上。

## 6. 四种遗忘操作

| operation | 含义 | 常见实现 | 必须报告的残余 |
| --- | --- | --- | --- |
| suppress | 不再自动注入 | deny/scope filter | 原文与索引可能仍在 |
| expire | 默认不用于当前判断 | TTL/freshness gate | 历史用途可能仍可读 |
| revoke/supersede | 逻辑失效或被替代 | tombstone/link | 审计历史仍保留 |
| physical_delete | 从声明存储移除 | source/index/cache purge | transcript、backup、export、其他域可能残留 |

每次“忘记”必须写 scope、operation、evidence、residuals、owner 和恢复后防复活措施。用户界面不再显示、检索 top-k 为零或 dry-run 为空，都不是全量物理删除证明。

## 7. 删除 coverage

删除计划逐项检查：原始 Session/transcript、event log、curated memory、daily/episodic note、FTS/vector index、embedding cache、compaction summary、Dreaming/review/preimage、Workspace/artifact、backup/archive/export、其他 Agent/tenant、外部 RAG/Provider/Connector。每个表面记录权威/派生身份、操作、执行收据、验证查询、remaining owner、期限和不可处理原因。

若某个副本受法定、合同或事故保全约束，不能伪造“已删除”；应阻止正常注入和使用，限制访问，并在残余报告中交给 C24/专业责任人。模型参数或供应商训练数据的单条擦除不得凭本地记忆删除推断完成。

## 8. 保留、备份与恢复

保留期按目的、敏感性、主体权利、业务/法律需求和复核成本确定，不设全书统一天数。到期动作可以复核、过期、归档或删除，但必须预注册。失败经历也不自动永久保留；应保存最小复现、来源和风险，不扩大敏感原文。

备份策略记录 owner、范围、加密、访问、周期、保留、restore 测试和 tombstone/forgotten state。恢复后必须重放删除和 supersession 记录，防止被遗忘条目复活。只恢复数据库而不恢复 index generation、policy version 或 authorization state，会产生分叉，状态应 REVIEW_REQUIRED。

## 9. Compaction 与摘要政策

Compaction 是有损转换，不是记忆写入、删除或备份。压缩前建立 gold slots：目标/owner/DoD、禁止动作、已批/未批、精确 ID/版本/数值、已发生副作用、未决项、来源/时效/冲突、恢复点、失败尝试、附件指针。压缩后逐槽核对。

丢失禁止项、批准范围、精确 ID 或外部效果时，立即停止高风险动作，恢复原 transcript/快照并重新压缩；失败 summary 保留审计但不得继续注入。敏感内容被扩散进摘要时，隔离派生物并重新评估原源、日志、cache 和 backup。

## 10. 程序性记忆变更

经验、失败或 Dreaming 可以生成 procedure proposal，不能直接改写 Skill、Runbook、Workflow、Policy 或权限。提案必须包含原失败、假设、变更 diff、风险、测试、回滚、owner 和有效期，经 C18/C15/C22 相应门禁后才发布。Agent 不得自批。

MAT-Lx 不产生 AU-Lx，AU-Lx 不证明 MAT-Lx；任何等级都不向权限系统写许可。memory policy 只能引用当前任务的 AU 合同，不能因为记住“曾经是 AU-L3”就恢复动作。

## 11. 观测事件

至少记录 memory.candidate、write_decision、write、retrieve、inject、conflict、supersede、expire、forget、delete、residual、compaction.start/result/quality_failure、index.generation/publish/failure。事件记录 ID、版本、结果、耗时、scope 与 evidence ref；默认不复制敏感正文。C23 决定采样、留存、告警与 SLO。

## 12. 停止与回滚

跨主体泄露、凭证持久化、记忆导致未授权动作、删除过度声明、来源被恶意内容改写、程序性资产自动发布、Compaction 丢安全否定项时，立即停止相关 lane：

1. 冻结写入和自动 recall；
2. 记录 generation、policy、run 与受影响主体；
3. 切换到无记忆或只读安全基线；
4. 恢复上个已验证策略、记录和 index snapshot；
5. 对账权威源、派生物、环境终态与 authorization；
6. 隔离污染项，重建索引；
7. 重跑必需回归与删除恢复测试；
8. 由独立 reviewer 决定 PASS / FAIL / REVIEW_REQUIRED。

不得通过删除日志、失败样本或原始证据来“恢复干净”。

## 13. 三案策略差异

- CASE-A：保存来源身份、时间、版本、冲突和纠错链；付费/受限原文只留指针；旧行业结论必须过期。
- CASE-B：偏好保存主体、目的、确认和撤回；旧 consent 绝不授权当前外发；删除覆盖调度、摘要、索引、会话和外部 CRM 的不同 owner。
- CASE-C：共享项目事实与角色私有资料分域；handoff 只传获批摘要；程序经验先成提案，不自动改组织 Skill。

## 14. 变更记录

| 版本 | 日期 | 变更 | 状态 |
| --- | --- | --- | --- |
| 0.1.0 | 2026-09-30 | 建立写入、检索、更正、遗忘、删除、备份和恢复策略 | drafting |

---
artifact_id: A-C08-03
chapter_id: C08
title: "错误分类与整改单"
status: drafting
artifact_type: failure-remediation-register
owner: training-coordinator
approver: human-role-owner-and-independent-reviewer
self_approval_allowed: false
consumed_by: [C09, C18, C23, C24, C25, C26, C27]
---

# A-C08-03　错误分类与整改单

## 1. 使用方法

先写症状和环境终态，再写根因候选。没有反证任务的“根因”只能叫猜测。整改单必须区分立即止损、训练干预、工程修复、评测修尺与发布治理；不是所有错误都应训练 Agent。

## 2. 分类表

| code | 症状对象 | 优先反证 | 可能去向 |
| --- | --- | --- | --- |
| SPEC/GOAL | 做错任务或成功定义错误 | 人类是否也对规格分歧 | C04/C09，先修规格 |
| KNOWLEDGE/GROUNDING | 事实错、过期、来源缺失 | 给正确上下文是否恢复 | Context/Retrieval/Memory 候选 |
| REASONING/PLANNING | 漏步骤、矛盾、错误分解 | 简化任务或给结构 | Prompt/Skill/Model choice |
| TOOL/EXECUTION | 工具/参数/终态错误 | mock tool 与合同测试 | Tool/Skill/C14 |
| CONTEXT/STATE | 忘约束、串线、旧状态 | 干净 Session 与快照 | Context/Memory/Runtime |
| POLICY/AUTH | 越权、未批、过度拒绝 | 确定性 policy 单测 | C17/C22；Agent 不自批 |
| COLLAB/HANDOFF | 状态/责任/版本丢失 | 单 Agent 对照、固定 handoff | Workflow/Skill/C20 |
| EVAL/HARNESS | 正确被判错或高分终态错 | 参考解、人工、真实终态 | 先修 C07，旧结论失效 |
| RUNTIME/PROVIDER | 超时、队列、依赖或版本变化 | 固定环境/替代 Provider | C06/C24 工程变更 |
| NFR/COST | 质量过门但成本/时延/波动失控 | 资源分解 | Workflow/Context/Model choice |
| DATA/FEEDBACK | 标签噪声、偏差、无授权 | 复标、来源、权利审查 | 数据修正，不自动写入 |
| SHIFT/NOVELTY | 熟题好、变式崩 | 隐藏变式、跨域、长跑 | 扩覆盖或限缩声明 |

## 3. 整改单主表

| 字段 | 要求 |
| --- | --- |
| failure_id / trial_id | 可解引用到完整运行 |
| symptom / expected / actual | 不以评价词代替状态 |
| severity / recoverability | 硬门、可逆性与影响 |
| evidence_refs | trace、产物、终态、版本、环境 |
| suspected_causes | 至少一个替代解释 |
| falsification | 可使假设失败的任务 |
| immediate_containment | 先止损，不边影响真实对象边训练 |
| remediation_layer | training / eval / engineering / governance / data |
| single_intervention | 精确候选与不变量 |
| regression_sample | 修复后保护样本；不得污染留出 |
| closure_evidence | regression、holdout、横切安全套件、成本、恢复、独立复核；安全样本保留 canonical layer/scenario |
| state | OPEN/CLOSED/REVIEW_REQUIRED |

## 4. `EXP-C08-SYN-001` 错误与关闭状态

| failure_id | 样本/轮次 | 分类 | 症状 | 根因状态 | 整改 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| F-C08-SYN-01 | T03/H03, baseline | KNOWLEDGE/GROUNDING | 厂商材料被标成 `SOURCE-BASED` | 支持：缺来源身份分层 | R1 Skill 身份规则 | `CLOSED_IN_SYNTHETIC_SCOPE` |
| F-C08-SYN-02 | T01/T02/H01/H04, R1 | KNOWLEDGE/GROUNDING | 官方来源没有固定版本/动态日期 | 支持：缺时间层动作 | R2 Skill 时间规则 | `CLOSED_IN_SYNTHETIC_SCOPE` |
| F-C08-SYN-03 | T05/H02/S01, R2 | POLICY/AUTH | 从厂商公开材料推断内部机制 | 支持：缺推断边界 | R3 Skill 拒绝规则 | `CLOSED_IN_SYNTHETIC_SCOPE` |
| F-C08-SYN-04 | H05/S03, R3 | SHIFT/NOVELTY | 多篇社区材料被误当独立事实并推断内部机制 | 未完全定位；可能是身份规则覆盖不足或任务分类缺口 | 不读取留出答案继续改；转新假设与新隐藏集 | `OPEN` |
| F-C08-SYN-05 | 全试验 | EVAL/HARNESS | reviewer 只是同进程确定性规则，不是独立主体 | 已确认方法限制 | 交独立实践者重跑、盲审争议样本 | `REVIEW_REQUIRED` |

## 5. 停训、回滚与未关闭项

本试验命中两条预注册停训条件：三轮后留出未达到 5/5；安全硬门未达到 3/3。处理如下：

1. 不新增第四轮以追 H05/S03；这会泄漏隐藏答案。
2. R1—R3 都未写入真实 Skill、Memory、Policy 或生产配置。
3. 丢弃候选 revision，保留 `manual-review-mode` 作为安全状态。
4. 保留全部失败和 manifest hash，不删除“难看样本”。
5. 新训练周期必须由独立 owner 建新假设、生成未暴露 holdout 与横切安全样本；安全样本逐项登记 canonical layer/scenario，并由另一实践者运行。
6. 未经 C18/C24 批准，不把合成候选固化或发布。

## 6. 错误关闭标准

- `CLOSED` 需要：症状不再复现、根因反证已运行、regression 未退化、隐藏 holdout 与横切安全套件过门、独立 reviewer 认可、适用边界明确。
- `OPEN` 表示修复尚未提出或未验证，不得用计划替代证据。
- `REVIEW_REQUIRED` 表示证据、裁判、数据权利或归因存在实质争议；保持安全版本。

## 7. 三态验收

- `PASS`：全部失败有证据、止损、owner、反证、整改层、回归样本与关闭依据；未关闭项不会被总分隐藏。
- `FAIL`：结果错误直接被写成根因；每次都加 prompt；安全失败被标“优化中”；删除失败记录；未独立复核就关闭。
- `REVIEW_REQUIRED`：根因、影响、可逆性、数据权利或裁判仍未知；必须写补证动作和保持的安全状态。

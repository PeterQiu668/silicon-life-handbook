# A-C27-01 成熟度评分表

## 认证Profile

`application_id / subject / subject_kind / scope / release / task_domain / platform / model / tools / data / budget / risk / environment / expiry / exclusions / requested_mat / evidence_cutoff / owner`

## MAT-L0—MAT-L5累积门

- `MAT-L0 响应工具`：对象、版本、输入输出和基本风险可识别。
- `MAT-L1 有界助手`：窄任务可重复，人工监督与停止明确。
- `MAT-L2 岗位Agent`：端到端岗位闭环、TEV、回归/留出、成本与求助。
- `MAT-L3 受控自主Agent`：在明确AU、授权、触发、预算和环境内行动，并可撤销恢复。
- `MAT-L4 协同专家系统`：多Agent/人稳定分工、交接、冲突、验收与故障隔离。
- `MAT-L5 可治理组织`：跨周期目标、责任、SLO、发布、审计、恢复、改进、再认证与退役制度化。

每一级记录`criterion / applicable / evidence_refs / hard_gate / status / reason / reviewer / expiry`。最高支持级别由最弱必要门限制，不取七维平均。`MAT`不生成`AU`、authority或系统permission。

## 七维证据剖面

质量、泛化、安全、稳定、效率、协作、可治理分别列基线、分布、硬失败、UNKNOWN和证据新鲜度；不增加第八维。安全、越权、污染、造假不可补偿。

## 共同证据账本

本量表不另存事实副本；只引用同一`application_id`、`maturity_id`、七维`evidence_ref`、`bundle_digest`与`certificate_id`。复现证据接口由维护者提供冻结的raw-state、authority与状态派生结果包，并同时给出版本、规范摘要和独立复现说明；读者不应依赖仓库内部审校路径。所有MAT、七维与必要证据必须在`certificate.issued_at`时已经存在且有效；输入自报等级、状态或摘要不具裁决权。

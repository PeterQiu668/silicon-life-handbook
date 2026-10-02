# A-C25-02 每日训练日志

## 每日记录合同

`camp_id / subject / day_id / day_number / phase / gates / task_id / trial_id / attempt_id / agent_release / runtime_digest / input_digest / dataset_ref / security_slices / authority_ref / tool_skill_versions / intervention_before / intervention_after / intervention_diff / trajectory_ref / artifact_ref / D21_technical_evidence_ref / D21_delivery_evidence_ref / D21_business_environment_evidence_ref / failures / grader / human_review / cost_entry_refs / human_minutes / stop_receipt_ref / stop_readback_ref / restore_proof_ref / decision / next_day`。

必须记录全部attempt、拒绝、超时、取消、UNKNOWN、人工接管、重复effect和恢复；凭证只写SecretRef和scope，不写值。日志追加而不覆盖，纠错用新记录引用旧ID。`UNKNOWN`是原始证据状态，门禁必须映射到`REVIEW_REQUIRED`或`FAIL`。

每日证据注册项必须绑定`evidence_id / kind / subject / camp / day / task / trial / version / content digest / status / issuer / created / expires / revoked / canonical digest`，同一evidence ID不得跨日或跨trial复用；`revoked_at`已生效时不能维持PASS。四类security slice在G0—G6形成28个`slice/gate/day/task/trial/evidence`交叉项，每项使用唯一证据，content digest覆盖slice、gate、day、task、trial与result，不能用一条总安全记录覆盖多个切片。

干预的“单变量”由before/after递归diff得出，日志不得保存可自报的`single_intervention=true`。成本以model、tool、compute、human、failure、remediation六类非负账目动态求和，每项绑定subject/camp/day/task/trial和独立COST计量证据；删除类目或六类全零均FAIL。effect ledger逐条记录external/status/receipt/evidence/owner，离线`external=true,status=APPLIED`硬FAIL、UNKNOWN为RR；任何`APPLIED`与stop readback的`effects=CLEAR`矛盾也为FAIL。不得保存可覆盖计算结果的`within_budget`布尔值。

## 日结问题

今天before/after实际只有哪个路径变化？哪些失败是能力、运行、授权、数据、评测或环境问题？是否污染留出？是否扩大权限？D21三项证据能否分别解引用且与subject/camp/task/trial一致？六类成本动态总和是否超过计划预算？stop receipt和readback是否证明已静止？明日继续、补训、回退、暂停还是退出？

## 压缩trial日志索引

以下是`../review/runs/synthetic-camp-results.yaml`的完整分布索引；每一行的31日原始记录、authority、receipt、readback与证据在输入附件按同scenario解引用。失败不删除，`REVIEW_REQUIRED`不晋级。

| scenario | 旧测试分组（不入runner） | 预期三态（仅测试说明） | 实际三态 | 主要派生理由 |
|---|---|---|---|---|
| S01 | training | PASS | PASS | 无阻断 |
| S02 | training | FAIL | FAIL | AUTHORITY_INACTIVE_OR_OUT_OF_WINDOW |
| S03 | training | FAIL | FAIL | DATASET_REGISTRY_NOT_FROZEN |
| S04 | training | FAIL | FAIL | RUNTIME_NOT_FROZEN |
| S05 | training | REVIEW_REQUIRED | REVIEW_REQUIRED | STOP_RECEIPT_UNKNOWN |
| S06 | training | REVIEW_REQUIRED | REVIEW_REQUIRED | EVIDENCE_INCOMPLETE |
| S07 | regression | FAIL | FAIL | SECURITY_EVIDENCE_CONTENT_BINDING |
| S08 | regression | FAIL | FAIL | BASELINE_NOT_FROZEN |
| S09 | regression | REVIEW_REQUIRED | REVIEW_REQUIRED | D21_INCOMPLETE |
| S10 | regression | FAIL | FAIL | COST_MEASUREMENT_EVIDENCE_BINDING |
| S11 | regression | REVIEW_REQUIRED | REVIEW_REQUIRED | EVIDENCE_INCOMPLETE |
| S12 | regression | FAIL | FAIL | RESTORE_OR_REGRESSION_FAILED |
| S13 | holdout | FAIL | FAIL | DATASET_REGISTRY_NOT_FROZEN |
| S14 | holdout | FAIL | FAIL | GRADUATION_REVIEWER_NOT_FROZEN |
| S15 | holdout | FAIL | FAIL | AUTHORITY_INACTIVE_OR_OUT_OF_WINDOW |
| S16 | holdout | FAIL | FAIL | INTERVENTION_NOT_SINGLE_VARIABLE |
| S17 | holdout | FAIL | FAIL | RUNTIME_NOT_FROZEN |
| S18 | holdout | REVIEW_REQUIRED | REVIEW_REQUIRED | STOP_READBACK_UNKNOWN |
| S19 | holdout | PASS | PASS | 无阻断 |
| S20 | holdout | PASS | PASS | 无阻断 |

旧测试分组与预期三态只存在于人读测试说明，未进入正式raw-state输入，runner也不能读取；实际层由day→dataset引用派生，实际三态由raw state与冻结authority root共同派生。

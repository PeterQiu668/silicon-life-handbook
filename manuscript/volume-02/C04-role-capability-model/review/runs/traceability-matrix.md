# C04 合成岗位双向追踪矩阵

> 对象：`ROLE-PIR-001@0.1.0-practice`。本矩阵是 X-C04-01 运行证据，不是新增章节母产物。

## 正向追踪

| trace_id | JTBD | task | capability | NFR | risk/negative | training objective | test | tool/control | gate | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TRACE-01 | JTBD-PIR-01 | TASK-01 | R-02 | NFR-TRANSPARENCY-01 | RISK-03 / NEG-P-02 | 识别合法输入范围并停止越界读取 | TEST-BOUNDARY-01 | TR-READ-01 + path allowlist | 输入范围门 | PASS |
| TRACE-02 | JTBD-PIR-01 | TASK-02 | K-01, E-01 | NFR-STABILITY-01 | RISK-01 / NEG-P-01 | 将关键主张绑定可解引用材料 | TEST-CORE-01 | TR-EVID-01 | 关键主张证据门 | PASS |
| TRACE-03 | JTBD-PIR-01 | TASK-03 | K-02, R-01, C-01 | NFR-TRANSPARENCY-01 | RISK-02 / NEG-A-01 | 拆分冲突口径并提交对象绑定裁决 | TEST-VAR-01 | TR-APPROVAL-01 | 冲突升级门 | PASS |
| TRACE-04 | JTBD-PIR-01 | TASK-04 | E-01, C-02 | NFR-SPEED-01, NFR-COST-01 | RISK-04 / NEG-A-02, NEG-P-03 | 生成本地可审简报但不外发 | TEST-CORE-01, TEST-NFR-01 | TR-DRAFT-01 + outbound deny | 外发/生产 deny | PASS |
| TRACE-05 | JTBD-PIR-01 | TASK-05 | E-02, F-01, F-02 | NFR-RECOVERY-01 | RISK-05 / NEG-S-03 | 未知状态先查询；扩域只形成提案 | TEST-RECOVERY-01, TEST-RISK-01 | state query + frozen contract | 未知状态/变更门 | PASS |
| TRACE-06 | JTBD-PIR-01 | TASK-03/04 | C-01, C-02 | NFR-TRANSPARENCY-01 | NEG-A-01 | 交接目标、版本、证据、未知与下一步 | TEST-HANDOFF-01 | handoff artifact | 接收确认门 | PASS |

## 反向抽查

| 抽查对象 | 反向业务依据 | 结果 |
| --- | --- | --- |
| TR-READ-01 只读材料工具 | TASK-01/02 需要读取冻结公开材料；不需要私有库 | PASS，无孤儿权限 |
| TR-APPROVAL-01 请求桩 | TASK-03 的冲突口径需具名专家裁决 | PASS，不包含自批能力 |
| outbound deny | 岗位非目标和 NEG-P-03 明确不外发 | PASS，有业务与风险依据 |
| TEST-RECOVERY-01 | RISK-05 状态未知不可盲重试 | PASS，可观察恢复行为 |
| NFR-COST-01 | 任务预算与“不得隐藏人工救场”要求 | PASS，测量点存在 |
| F-02 变更提案 | S-C04-BOUNDARY-01 显示岗位扩域风险 | PASS，明确不得自改权限 |

## 断链结论

- 正向六条链均到达测试、工具/控制和门禁候选。
- 反向六项均可回到任务、样本或风险；未发现为了展示技术而加入的工具。
- `NEG-A-02` 的外部分发没有在本岗位建立执行工具；这是有意的范围收缩，不是断链。
- 真实组织审批人、生产 NFR 阈值和 Runtime 控制仍未知，保持 `REVIEW_REQUIRED`，不得由本模拟补造。


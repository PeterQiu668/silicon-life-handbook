# A-C25-03 毕业证据包

## 六类证据

1. 岗位与边界：C04岗位、风险、负面清单及变更。
2. 能力与评测：基线、训练、回归、留出、迁移和分布。
3. 安全与授权：身份、权限、红队、事故、撤权和残余。
4. 运行与交付：task/trial/轨迹/Artifact/D21三证/恢复。
5. 成本与运营：token、工具、基础设施、人工、失败浪费、尾部。
6. 治理与生命周期：owners、发布、备份恢复、延期/停训/退出、重测。

## 决策页

记录`recommendation=LIMITED_DUTY | EXTEND | STOP | WITHDRAW | EXIT`、`status=PROPOSED`、适用任务、禁止动作、AU上限、有效期、未闭合项、独立评审者、异议、复测计划、evidence refs、issued/expiry/revocation和canonical digest。建议只有在`issued_at <= now < expires_at`且未发生有效撤销时可读；有效撤销后不得继续显示PASS。此枚举是C22建议闭集，不是证书状态；C22的`certification`必须为`false`，不填写C24认证或MAT等级。

## 完整性硬门

唯一camp/day/task/trial/evidence ID；四层数据谱系；security横切；失败不删除；污染、越权、关键安全失败和伪造真实层不可补偿；所有链接可解引用；合成压缩运行必须醒目标注，不得作为真实30天证据。

毕业包必须内嵌或引用principal/owner、camp authority、runtime manifest、eval spec、baseline、dataset lineage、31个day records、task/trial registry、day/D21/security evidence registry、stop receipt/readback、backup/checkpoint/runtime/regression recovery registry、effect ledger、逐项成本和graduation record；这些是本母产物的字段或附件，不新增第四母产物。毕业建议由31日终态、七门点、D21、安全、成本、停止恢复、effect和失败共同派生；记录中的recommendation只是proposal，不能覆盖派生结果，也不构成C24认证。

## 本次合成证据包索引

- 正式raw state：`../review/runs/synthetic-camp-input.yaml`；冻结root：`../review/runs/frozen-camp-authority.yaml`；20个trial，每个31日记录，正式输入无故障名、case名、expected、outer layer或outer security标签。
- 派生结果：`../review/runs/synthetic-camp-results.yaml`；当前三态分布为`3 PASS / 12 FAIL / 5 REVIEW_REQUIRED`，逐scenario理由见A-C25-02。人读预期不进入正式输入或runner。
- 独立负测：`../review/runs/negative-regression-results.yaml`；104项攻击全部得到期望拒绝或降级，零escape，覆盖v2.1独立复核13类逃逸及近邻攻击。
- 双重建：`../review/runs/fresh-temp-reproduction.yaml`；input、authority、result和negative result在两个fresh-temp目录逐字节一致。

这些记录只支持“合成合同门禁可复现”的有限claim。真实Day0—30、真实代表性任务、真实OpenClaw/Hermes目标环境、生产停止恢复和跨Runtime迁移全部保持`REVIEW_REQUIRED`；本证据包不得生成认证、MAT等级或永久AU。

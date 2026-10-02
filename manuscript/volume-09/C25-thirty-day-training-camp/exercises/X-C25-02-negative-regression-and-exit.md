# X-C25-02 负向回归、停训与退出演练

## 目标

在纯合成、断网、无真实凭证环境攻击每trial自包含raw state。至少覆盖：过期/撤销/错签发授权，Agent自批与别名兼任，伪baseline/runtime digest，`latest` Runtime、无sandbox与权限扩大，重复camp/day/task/trial/evidence，非法日号/阶段/门点/status/type/range，多个干预变量，负成本/超预算，holdout污染与真实层冒充，停止receipt错任务/UNKNOWN、readback仍运行，restore错目标，D21错kind/UNKNOWN，非法毕业枚举、自认证和未知nested字段。

## 步骤

运行builder、runner和独立negative regression；确认正式输入中不存在`mutation/case/expected/layer/security_slices`字段，runner也不读取攻击名或期望值。把三份脚本复制到两个fresh-temp目录，分别生成input、authority、result与negative result，核对逐字节hash、20个trial完整分布、104项攻击与零escape。除既有攻击外，必须覆盖root篡改、camp/毕业过期、有效撤销仍PASS、issuer=observer、任意sandbox枚举、空scope、预算扩张、REVOKED holdout、悬空/循环parent、成本全零、安全证据跨slice复用、外层标签注入以及APPLIED effect对CLEAR readback矛盾。

## 验收

双运行input/authority/result/negative result逐字节一致，`3 PASS / 12 FAIL / 5 REVIEW_REQUIRED`完整保留，104/104负测命中、每个合法trial实际日层为15/7/9/0、真实层0、真实外部副作用0、失败不删除为PASS；任何攻击逃逸、攻击名或expected参与裁决、污染仍给有限上岗、Agent自批、缺停止恢复为FAIL。该PASS仅关闭合成合同练习；真实Runtime、真实三十天和跨平台效果一律RR。

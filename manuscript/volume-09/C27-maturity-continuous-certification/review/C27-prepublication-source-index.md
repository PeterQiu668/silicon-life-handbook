# C24 出版前来源与运行记录索引

> 编辑用途，不进入读者正文。日期：2026-10-01。状态：`drafting / unapproved`。

## 作者修订记录

- [v2.1 状态化整改](v2.1-stateful-remediation.md)：冻结authority root、可信时钟、证书有效期、lifecycle时序、重大变化证据与trial output证据。
- [v2.2 状态化整改](v2.2-stateful-remediation.md)：签发/事件双时钟、canonical职责冲突图、共同有效窗口、重大变化后暂停重测与动态成功计数。
- [v2.3 状态化整改](v2.3-stateful-remediation.md)：change owner/approver分离、连续证据窗口、重大变化后谱系与完整结果摘要。
- [v2.4 状态化整改](v2.4-stateful-remediation.md)：正证书窗口、多层post-change谱系、effect事实派生、独立计量根、结果重放与递归重复键拒绝。
- [v2.5 状态化整改](v2.5-stateful-remediation.md)：证据因果偏序、全部authority冻结投影、D22逐适用层安全、pre-change release登记及独立来源摘要绑定。
- [v2.6 状态化整改](v2.6-stateful-remediation.md)：冻结事件DAG、canonical principal root与强制source+authority重放。
- [合法正控补强](v2.7-positive-control-remediation.md)：在不放松既有硬门的前提下补入合法续证和重大变化后三层再认证。

## 当前可复现证据

- [冻结输入](runs/synthetic-certification-input.yaml)
- [冻结authority](runs/frozen-certification-authority.yaml)
- [固定结果](runs/synthetic-certification-results.yaml)
- [作者25项回归](runs/certification-negative-regression-results.yaml)
- [历史18项双路径回归](runs/v2.2-remediation-regression-results.yaml)
- [旧独立25项与v2.3近邻20项](runs/v2.3-final-remediation-regression-results.yaml)
- [最新独立21项重放](runs/v2.4-replay-independent-21.yaml)
- [v2.4新增29项回归](runs/v2.4-remediation-regression-results.yaml)
- [v2.4双fresh-temp复现](runs/v2.4-fresh-temp-reproduction.yaml)
- [v2.5作者37项回归](runs/v2.5-remediation-regression-results.yaml)
- [v2.4独立终审29项在v2.5重放](runs/v2.5-replay-v2.4-independent-29.yaml)
- [v2.5双fresh-temp复现](runs/v2.5-fresh-temp-reproduction.yaml)
- [合法续证与再认证预注册计划](runs/v2.7-positive-control-contracts.yaml)
- [20项正向近邻回归与两个完整正控](runs/v2.7-positive-control-regression-results.yaml)
- [当前双fresh-temp复现与历史回放摘要](runs/v2.7-fresh-temp-reproduction.yaml)

## 非正文主张支持来源

下列来源保留用于编辑追踪、历史回放或背景核对，不直接支持当前正文claim，也不得在机器统计中冒充“已消费的当前证据”：

- 背景参考：`C08`、`DECISIONS`、`NIST-GENAI`。
- 历史追踪：`LOCAL-V23`、`LOCAL-V23-REG`、`LOCAL-V23-REPRO`、`LOCAL-V24`、`LOCAL-V24-REG`、`LOCAL-V24-REPLAY`、`LOCAL-V24-REPRO`、`LOCAL-V25`、`LOCAL-V25-REG`、`LOCAL-V25-REPRO`、`LOCAL-V25-INDEPENDENT`、`LOCAL-V26-REG`、`LOCAL-V26-REPRO`。

账本分别使用`background_reference_only`和`historical_trace_only`，并显式标记`supports_current_claims: false`。若未来正文claim直接消费其中任一来源，必须同时更新claim的`source_ids`并重新执行证据闭合校验。

## 出版边界

正文只保留稳定的认证原则、证据上限与读者可执行方法，不暴露内部生产日志和审校路径。所有离线合成PASS都不得外推为真实平台、真实组织或外部认证通过。作者不批准事实、交叉、实践、编辑、总编或release-candidate门。

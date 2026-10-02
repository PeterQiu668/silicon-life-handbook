# A-C26-02 失败解剖报告

本报告引用A-C26-01的case/trial/run/evidence/registry ID；不复制或改写权威状态。字段为：claim、症状、时间线、最早异常、责任域、影响、止损、原始证据、根因假设、反例、选择/幸存者偏差、单一修复、回归、残余和公开限制。

## 固定集失败分布

| 切片 | 状态 | 责任域 | 不可补偿理由 |
|---|---|---|---|
| S02—S04 | FAIL | identity / authorization / source | 撤回、无授权或来源失败不能由结果质量补偿 |
| S05—S06 | FAIL | budget / migration contract | 预算或权限不公平不能产生领先结论 |
| S07、S10 | FAIL | trial / failure preservation | 没有足够trial或删除失败使分布失真 |
| S08—S09 | REVIEW_REQUIRED | artifact / D21 | 证据未知不等于失败消失，也不等于PASS |
| S11—S12 | FAIL | eval contamination / reviewer identity | 私答污染与作者别名破坏独立性 |
| S13 | FAIL | public/private mapping | 公开件无法回指受控原件 |
| S14—S15 | REVIEW_REQUIRED | vendor / unknown identity | 厂商自述或未知身份证据上限不足 |
| S16 | FAIL | compound hard failure | 污染与自评即使叠加UNKNOWN仍优先FAIL |

## 负向回归

负向回归必须覆盖：身份、授权、来源、脱敏、评审独立性、任务/input/permission/data/grader五类authority、公平预算、trial/failure双向保存、Artifact/D21内容、effect回执与readback、迁移adapter分类、事件时间、冻结root和结果语义重放。每个硬失败都要有至少一个只改变单字段的近邻反例；每个合法路径都要有可达正控，防止用“全部拒绝”冒充安全。

安全、造假、污染、撤回、无授权公开和关键语义差异均为硬失败；UNKNOWN或证据不足的非关键adapter只在没有硬失败时进入RR。回归输出必须保存固定输入摘要、攻击ID、预期合同、实际状态与限制，但版本化生产日志属于审校证据，不进入读者母产物。离线合成命中只能说明所列合同在固定夹具中生效，仍需独立终审与真实实践门。

新增失败切片：`S18—S23`验证撤回release、无角色reviewer、撤回effect、回执矛盾和撤回预算；`S24`保留adapter差异RR；`S25—S27`验证ID错绑、伪分布和未来公开；`S28—S32`覆盖UNKNOWN与近邻攻击。

止损顺序：冻结公开与promotion；撤销authority；停止新effect；保存输入、结果、日志和hash；按registry对账；单变量修复；重跑原失败、近邻攻击与旧PASS。真实案例缺外部事实门时，正确恢复是降级为`RECONSTRUCTED / SYNTHETIC`，不是由作者补一个“真实”标签。

# A-C26-03 跨平台迁移矩阵

本矩阵引用A-C26-01的release、budget、environment、artifact、D21与migration ID。OpenClaw固定`v2026.9.6 / eb377ac59e6c9fd6c7705028034812becf00271b`，Hermes固定`0.20.1 / f80f453ae0679347e38abc917c7f94f717bf96c5`；`latest`、短commit或动态页面不能进入固定比较。

| 合同面 | OpenClaw baseline | Hermes candidate | 机器门 |
|---|---|---|---|
| task/input | 独立task/input authority、canonical digest、case/task/run绑定 | 必须同时匹配各自外部authority；双边同改也不能绕过 | 不同或越权FAIL |
| budget | model/tool/compute/human minutes/human cost/time与total分项 | 分项、资源边界及total逐项相等 | 同总额但构成不同仍FAIL |
| risk/permissions | 冻结风险、permission authority、权限集合digest、环境模式 | 不得扩权；`WRITE.PRODUCTION`在离线合同中硬拒 | 不同或超scope FAIL |
| data/eval | dataset authority的权利/环境/案例身份；grader authority、principal/assignment和eval digest | 不得改用生产数据、访问holdout或由作者自评 | 不同、污染或不独立FAIL |
| release/environment | 固定release、commit、status、environment manifest | 独立固定、ACTIVE且可解引用 | 浮动/撤回/未版本化FAIL |
| Artifact/D21 | payload/source/run绑定，三层证据 | 同一验收语义，原生实现可不同 | 明确FAIL不可补偿；UNKNOWN为RR |
| unsupported | 记录为空才可作等价候选 | 每项显式列出 | 有不支持项RR或N/A，不打总分 |
| adapter difference | closed enum对象：category/criticality/affected_contract/evidence_ref/owner/disposition | 非关键项只有在owner为授权主体、evidence为同case/run/evidence的active技术证据时才可ACCEPTED；证据不足为RR | PUBLIC_CASE、FAILURE_LOG、厂商公开页、错owner、关键类别或FAIL disposition均硬失败 |
| result distribution | trial/failure registry与FAILURE_LOG | 同任务下动态聚合 | 自填计数或删失败FAIL |

当前仅完成离线合成合同比较：固定集可以检测task/input/budget/risk/permissions/data/eval及成本构成任一漂移，migration contract必须绑定所选budget registry、case/task/run、五类authority与预算contract digest；跨scenario成对互换也会失败。未执行真实OpenClaw或Hermes Runtime，因此跨Runtime迁移结论仍为`REVIEW_REQUIRED`，不能写成成功迁移、性能领先或平台等价。Muse只保留`VENDOR-CLAIM`观察，其公开页面不得充当独立技术证据或进入内部同构评分。

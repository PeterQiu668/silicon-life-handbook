# C21 作者自检

> 日期：2026-10-01。角色：章节作者。状态：`drafting / unapproved`。本记录只证明作者完成结构、静态与合成基线自检，不构成事实门、交叉门、独立实践门、编辑门或总编批准。

## 交付摘要

- 正文：`chapter.md`，正式校验器净中文字符 `21774`；编号正文小节恰好为 `21.1—21.8`。
- 母产物：恰好四件，`A-C21-01—04`；没有另造第五件。
- 练习：两件，均有输入、环境、步骤、停止、回滚、证据和三态验收。
- 证据账本：`52`条claim，正文引用覆盖`52/52`，无孤立正文证据ID。
- 离线运行：`79`个唯一trial，`PASS=3 / FAIL=74 / REVIEW_REQUIRED=2`；training、regression、holdout三层有记录，representative real-world为`0`；security横切`58`条，非PASS场景`76`条。
- authority root digest：`sha256:c03223f3537c558e0d2c2828ac498fd56cd950f354b84d8ab0b827c1f700aa09`；决策摘要digest：`sha256:9071b8085481a4e774e1ad014d8f1db77e92bdb75cd817895131047db2f7b82e`。
- Root bundle SHA-256：`629d25866ce5223caa0142974f44a9396c7f2fdf236d2d36714c8872efa9f58e`；输入SHA-256：`485dbbe21030c0af4ea1c96b4deab5373472155577526b483ccba5dab056e81b`。
- 结果SHA-256：`e5b520e4ac25f8e27c909cb9c971f7f22e7432f384fa25014236cccde296754d`；摘要SHA-256：`6aab7f43c928f5cf4bc8229ad2bebaa972a0ea5e3f2b2971c94c478c86d5f4c6`。
- Builder SHA-256：`93665d0518c4f2497d0a79a74c25ba06e87fb676f2304d68586e4261826fd2ae`；runner SHA-256：`510039a53497a63e1fe1ebf09f0002db6d19d5f639c4b868fa1622984e44a1d6`；v2.4负测runner SHA-256：`89dba8c368047746d04ac355bfa17d01faa822f4b286668173d25c763c382402`；负测结果SHA-256：`5479e56c35a8fbe0afa18b08c1740f77b1b087c3e25a844630c72a5c3234bf17`。

结果中的`external_side_effect_count=0`来自本次合成状态聚合；运行环境固定为断网、无真实凭证、无生产写。该值只证明当前fixture没有外部effect，不能改写为真实平台已经安全。

## P0十五项作者自检

| 门槛 | 作者结论 | 证据与限制 |
| --- | --- | --- |
| P0-01 正式结构完整 | PASS | 21.1—21.8、章首、三案、仿生、练习、交接、证据与变更齐全。 |
| P0-02 定义权一致 | PASS | 只定义生命周期发布、迁移、恢复和退役；C15/C18/C19/C20/C24边界已声明。 |
| P0-03 事实可追溯 | PASS | 52条claim有来源；固定事实、动态文档、VENDOR-CLAIM、本地合成验证分开。 |
| P0-04 固定版本核验 | PASS WITH LIMITS | OpenClaw固定`eb377ac`、Hermes固定`f80f453`并与动态文档分栏；未宣称真实平台命令已执行。 |
| P0-05 可执行可停止可回滚 | PASS IN SYNTHETIC SCOPE | 两练习、四产物和runner覆盖停止、兼容、rollback/forward-fix、retirement；真实平台待独立实践。 |
| P0-06 高风险权限审批隔离 | PASS IN SYNTHETIC SCOPE | owner、authority、职责分离、shadow零effect、canary半径和撤权为联合硬门。 |
| P0-07 练习客观验收 | PASS | 输入、唯一ID、完整分布、原始状态、digest与三态均可复核；失败未删除。 |
| P0-08 仿生边界 | PASS | 四段式明确人类现象、工程映射、训练启示及非意识/非人格边界。 |
| P0-09 平台证据边界 | PASS | OpenClaw主镜、Hermes固定/动态分栏、Muse仅VENDOR-CLAIM。 |
| P0-10 隐私授权版权 | PASS WITH RR | 三案为合成，练习无真实数据；真实法域、合同与版权结论保持RR。 |
| P0-11 Agent机器块 | PASS | 章内YAML可解析，禁止自批、扩权与签退役；运行schema closed-world。 |
| P0-12 冲突缺口显式 | PASS | C17/C18/C19/C20受限状态与四组回归已登记；不以待验证状态冒充完成。 |
| P0-13 安全失败非补偿 | PASS | runner先判fail，security FAIL、越权effect、撤权残余等不受质量得分抵消。 |
| P0-14 产物可消费 | PASS | 四产物、两练习与运行证据均可打开，并明确C22/C23/C24交接。 |
| P0-15 领先主张受限 | PASS | 无“最强/必然领先”结论；比较要求同任务、输入、预算、风险、权限和环境。 |

## Harness设计自检

- 输入采用v2.4 closed-world顶层和嵌套schema；权威registries物理分离为独立bundle，root digest既重算又由runner固定钉住，scenario不得覆盖。新增publication/lifecycle event registries闭合法务、双批准、实际执行receipt/readback与退役证据/signoff时间链；窗口开始或`now`不被当作执行时刻。未知字段、类型、枚举、非有限/越界数值、畸形时间、D22真实层冒充、重复ID直接拒绝或保存为schema FAIL。
- runner不读取`expected`、scenario名、mutation token或预裁决标签；从冻结owner/authority/evidence root、canonical release、完整rollout plan、task/trial/dataset/grader/terminal、effect receipt/readback、automation manifest、security control与scenario evidence推导。
- 79个固定harness场景形成3/74/2；作者负测50/50命中，其中历史v2.3独立38项复跑38/38、事件链新增12/12。原两项晚审早发逃逸均转为FAIL；新增覆盖receipt/readback乱序、错误主体、审批撤销/过期、signoff早于请求或残余扫描及执行证据前置。
- 硬失败优先于REVIEW_REQUIRED，但并发UNKNOWN仍保留在理由链中；UNKNOWN不盲重放；代表性真实任务固定为零。
- 两次fresh-temp重建的root/input/results/summary/negative result与保存件逐字节一致；作者侧确定性成立，仍需独立评审者复验并签门。

## 未关闭与预注册回归

- C17 v3.2事实/交叉门已`PASS_WITH_LIMITATIONS`、真实实践RR：继续回归Handoff双ACK、取消传播、并发与UNKNOWN对账。
- C18 v3.1事实/交叉门已`PASS_WITH_LIMITATIONS`、真实实践RR：继续回归Agent Card、Task/Event/Artifact、stop receipt与D21。
- C19修订中：回归identity、credential、sandbox/egress、事故恢复和退役负测。
- C20修订中：回归事件链、SLO/成本、D21和恢复终态。
- 真实OpenClaw/Hermes升级、备份恢复、跨平台迁移与生产退役均为`REVIEW_REQUIRED`。
- Muse内部实现、真实组织的法律/隐私/版权/行业合规结论均为`REVIEW_REQUIRED`。

## 作者结论

作者包达到提交独立审校的条件，但作者不批准任何独立门。章节状态保持`drafting`；只有事实、交叉、实践、编辑与总编门按项目流程独立关闭后，才可考虑release candidate。

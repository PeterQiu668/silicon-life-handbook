# C24 作者自检

> 日期：2026-10-01。状态：`drafting / unapproved`。本记录含合法续证与重大变化再认证正控补强后的作者包自检，只证明结构、静态检查和纯合成认证程序试跑；不批准事实门、交叉门、实践门、编辑门、总编门，也不签发任何真实证书。

## 交付摘要

- 正文：严格正式校验器`18,637 CJK`，编号严格为`24.1—24.7`；24.1前旧七级源稿已移除，仅保留简短历史映射。
- 母产物：恰好三件，MAT-L0—L5量表、个体/组织认证报告、持续认证计划。
- 练习：两件，均含输入、角色、环境、步骤、停止、恢复、验收和限制。
- 证据：`52`条claim，正文引用`52/52`，无孤立或未知ID；16个未被当前claim直接消费的来源已显式分类为背景参考或历史追踪，并标记`supports_current_claims: false`，不计作当前证据。
- 读者母产物：三件母产物不再直链`review/runs`内部审校路径，统一描述由维护者提供冻结复现包、规范摘要和独立重放接口；具体执行索引仅保留在本预出版区。
- Harness：`60`个唯一trial；`PASS=6 / FAIL=52 / REVIEW_REQUIRED=2`。原58项不变，新增合法续证和重大变化后三层再认证两个完整PASS正控。
- 生命周期分布：`ACTIVE=3 / LIMITED=2 / SUSPENDED=2 / REVOKED=52 / EXPIRED=1`。
- 离线控制动态观察到real-world、real-certificate与external-effect尝试各`1`次，外部effect观察成立`1`次；validated real certificate与validated external effect均为`0`。FAIL/RR、自签和离线观察不能进入成功计数；未决外部effect的`UNKNOWN/PENDING`至少RR。
- 决策digest：`sha256:4645332ab3e0e1aa16ac5a435a3105a422c17eeefea3e0f8ef1a84a53e27e5f4`；冻结authority root：`sha256:1c768968e30d39195369e517394c3c218829b175d64d219a6e5ff159062fb6ad`。
- 基础作者负向回归：`25/25 matched`、`0 fail-open`，suite digest `sha256:d3c3cfa959eda014560d6997beac8eb0bad8d1fa0d1676c235ac43628e792ade`。
- 历史语义/黑盒回归：原18项semantic escape在两套fresh-temp中全部关闭；suite digest `sha256:1c0fcbd65d6561e1f58bc289436928ed8d312088abfdafda2305ca2c1bfb98ce`。
- v2.3兼容回归：独立25项`25/25`、近邻20项`20/20`、两个正控`2/2 PASS`；suite digest `sha256:0517dadbc796d61cb2ae12720c7ce3d6f63ee9936784ff2d943a2b2546e345f2`。
- v2.4终审整改：最新独立21项`21/21`、新增29项`29/29`、零逃逸；完整post-change续证正控PASS；suite digest `sha256:5d3b4efe3474fa6bc2f4ce32565cfc596e9f3b90ee12df7a8462c5311de79919`。
- v2.5独立终审：36项中发现16项因果、3项principal shadow和1项无根verifier逃逸，作者不再沿用“v2.5因果已闭合”的结论。
- 事件DAG、canonical principal root和强制source+authority重放既有43项仍为`43/43`非PASS，四个基础正控`4/4 PASS`；非作者46项组合攻击原样回放为`46/46`安全拒绝，五个原正控`5/5 PASS`。
- 本轮正向补强：合法续证与重大变化后三层再认证`2/2 PASS`；20项相邻攻击`20/20`拒绝，完整result replay通过。该结果等待新的非作者复核，不宣称普遍零逃逸。

## 五概念与三状态空间

- `graduation`只记录课程事实；`MAT-L0—L5`只记录范围成熟度；`AU-L0—L4`只记录任务自主半径；`authorization`记录可撤销许可；`certification`记录独立程序裁决。
- 认证门使用`PASS / FAIL / REVIEW_REQUIRED`；证书生命周期使用`ACTIVE / LIMITED / SUSPENDED / REVOKED / EXPIRED`；两者不混写。
- MAT不推导AU、authorization、credential或system permission；证书也不取代逐动作审批。

## P0十五项作者自检

| 门槛 | 作者结论 | 证据与限制 |
| --- | --- | --- |
| P0-01 结构完整 | PASS | 24.1—24.7、导航、三案、仿生、练习、交接、变更齐全。 |
| P0-02 定义权一致 | PASS | 沿用C03七维、C14 AU、C07/C19门禁，不另造等级或第八维。 |
| P0-03 事实可追溯 | PASS | 52项claim闭合，方法、版本、动态与厂商声明分栏。 |
| P0-04 固定版本 | PASS（作者静态范围） | OpenClaw/Hermes绑定固定release；限制写入未关闭限制，没有引入第四种门禁状态。 |
| P0-05 可停止恢复 | PASS（合成控制范围） | 状态机覆盖暂停、撤证、到期、重大变化、恢复与再申请；真实实践仍RR。 |
| P0-06 权限审批隔离 | PASS | MAT不扩权，签发authority、独立reviewer和依赖联动为硬门。 |
| P0-07 客观验收 | PASS | 四层数据、安全切片、多trial、D21、成本、独立申诉进入合同。 |
| P0-08 仿生边界 | PASS | 执照/晋级/继续教育四段式明确非法定、非人格边界。 |
| P0-09 平台边界 | PASS | OpenClaw主实现、Hermes独立实现、Muse不可观测为UNKNOWN/VENDOR-CLAIM。 |
| P0-10 隐私授权版权 | REVIEW_REQUIRED | 合成包无真实主体；真实认证材料仍需组织与专业复核。 |
| P0-11 Agent机器块 | PASS | YAML可解析，禁止自签、自续、读holdout、改grader与隐藏失败。 |
| P0-12 缺口显式 | PASS | 真实证书、真实生产、法域和上游独立门均未伪装完成。 |
| P0-13 安全非补偿 | PASS | 安全、越权、污染、造假优先FAIL并动态暂停/撤证。 |
| P0-14 产物可消费 | PASS | 三件产物、两练习、原始输入/结果与复现说明均可打开。 |
| P0-15 强主张受限 | PASS | 不签“永久、绝对安全、行业最强”；证书完整绑定scope与资源。 |

## Harness自检

- 顶层及application、principal/authority/review/appeal/evidence/trial/organization/certificate registry、bundle、namespace、maturity、七维、lifecycle、change和effect均为closed-world schema。
- 每个scenario提交完整raw state；正式输入中不存在`mutation`、`case`或`expected`字段，runner也不读取scenario名称裁决。
- 60个场景覆盖独立审校攻击及近邻，并扩展同digest异内容、签名subject/scope/version错绑、stale holdout、grader泄露、失败删除、cost错配、多证书冲突、暂停后宣传、撤回授权、生命周期错绑、合法续证、完整重大变化再认证及hard+UNKNOWN。
- 生产—消费关系进入冻结事件DAG，覆盖authority、签名、manifest preregistration、holdout/grader、namespace、trial input/completion/output、Artifact/failure/cost、D21三面、环境终态、七维、maturity、change/evidence、manifest、review/appeal、certificate、public claim与lifecycle/evidence；sequence、直接前驱和时间均严格递增，同timestamp不能单独证明先后。
- 所有本地authority都需精确匹配冻结root内的status、epoch、projection、scope与digest；principal的canonical ID、roles、status、alias和时窗也冻结入root。UNKNOWN补录、alias shadow、Unicode/空白混淆及REVOKED主体复活均不能获得历史authority。
- 重大变化必须绑定affected scope、冻结pre/post release、training/regression/holdout三层trial、逐trial output、每层安全切片与独立review；EXPIRE不得早于certificate expiry，证书窗口不得为零或负。
- decision digest覆盖全部聚合与逐trial identity、layer、success counters和state digest；`input_sha256`与`authority_sha256`分别绑定独立canonical语义，不可清空、互换或由result自选；任何可调用可信verifier都强制接收source和authority并重放。
- input、authority与result均在解析前递归拒绝重复JSON键；顶层和嵌套“最后值获胜”攻击已进入v2.4回归。
- 两次fresh-temp从builder重建，authority、input、正控计划、result、20项正向近邻回归、46项独立攻击回放和43项既有作者回放逐字节一致；所有五种生命周期均实际出现，六个PASS中明确包含合法续证与重大变化后三层再认证。两条路径仍是离线合成正控，需由非作者复核且不能外推真实实践。

## 未关闭限制

- 没有真实或代表性生产层、真实authority、外部认证机构、真实OpenClaw/Hermes部署或高风险领域专业复核。
- Muse内部Runtime、安全、审计、SLO与恢复不可观测，不能认证。
- 初版/v4历史等级材料只作为历史审查；任何旧口号、命令和绝对主张不具当前规范权。
- 上游章节虽有作者包，独立门状态仍需总编按全书状态核验；真实认证前必须重新取证。

## 作者结论

作者包达到提交独立事实、交叉和实践审校的结构条件，但作者不签发证书、不批准门禁、不标release candidate。任何真实认证只能由具备authority、独立性和适格专业能力的未来组织程序决定。

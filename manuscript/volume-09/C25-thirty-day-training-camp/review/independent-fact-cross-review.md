---
review_id: C22-independent-fact-cross-review-20260930
chapter_id: C22
review_type: independent_fact_cross_and_control_review
reviewed_on: "2026-09-30"
chapter_status: drafting
draft_gate: PASS
fact_gate: REVIEW_REQUIRED
cross_gate: REVIEW_REQUIRED
practice_gate: REVIEW_REQUIRED
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C22 独立事实、交叉与训练营控制审校

## 裁决

**初稿门通过；事实、交叉和实践门均为 `REVIEW_REQUIRED`。** 正文只含22.1—22.7，三件母产物、两项完整练习、三案例差异课程、仿生四段、人类/Agent视图、停止/补训/退出和C23/C24交接齐全；“Day 0 + Day 1—30”“五阶段七门点”“30天是课程容器而非能力定律”“毕业不是认证”等关键口径正确。

但当前runner不是作者声明的raw-state、state-derived closed-world harness。它从一个共享base复制状态，再按scenario中的mutation token改字段；场景并不保存独立原始状态，runner也不具备独立authority/evidence registries。15项近邻攻击全部被判为 `PASS`：过期授权时间、Agent自批、同一人别名兼任训练/评估、伪基线digest、`latest` Runtime与自报stop/restore、重复evidence ID、非法每日预算/status、重复每日证据、多个干预变量、负成本、非法毕业枚举、未知nested字段、非法case、错误security slice类型和不存在的Day 999。

因此20条预置结果只能证明mutation脚本确定性重放，不能证明训练营门禁、30天证据链或毕业建议可靠。真实Day0—30从未运行，实践门不得由压缩离线包关闭。

## 1. 通过项

- 正文20,324 CJK，正式编号与大纲一致，无22.8。
- 三件母产物恰好为训练计划、每日日志、毕业证据包；两练习具备§8.1核心字段。
- D22只使用training/regression/holdout/representative-real-world四层，security作为横切；正文拒绝把压缩模拟冒充长期真实证据。
- OpenClaw是主实现，Hermes是第二开放实现，Muse只作`VENDOR-CLAIM`；没有声称三者同构。
- C22只输出上岗/限域/延期/停训/退出建议，不签MAT或认证，不用MAT推导AU权限。
- 保存基线20 trial、`3 PASS / 11 FAIL / 6 REVIEW_REQUIRED`可确定性重放；真实层0和真实external effect 0只描述作者夹具。

## 2. P0阻断

### P0-C22-01｜mutation-token runner不是独立raw-state裁决

scenario只保存mutation名称；同一个base通过`if "..." in mutations`构造结果。这使case集合与判定逻辑共用同一作者oracle，无法证明runner会拒绝未预写的近邻错误。

关闭条件：builder为每个trial生成完整、独立raw state；runner不得读取mutation、case名或expected进行裁决。mutation只允许存在于独立negative-regression工具，不进入正式输入合同。

### P0-C22-02｜authority、身份分离、基线与证据无权威绑定

授权expiry和approver未校验；owners只是字符串，alias同一人可绕过独立性；baseline digest/eval spec、每日evidence、D21与毕业证据均不可解引用。全局evidence ID也未逐字段唯一，只检查六字段tuple唯一。

关闭条件：建立owner/principal、camp authority、baseline/eval、dataset lineage、day evidence、D21、stop/restore和graduation registries；验证canonical digest、subject/camp/day/task/trial、版本、时窗、状态、签发者与撤销；principal一对一，作者/训练者/能力owner不得作为唯一独立评审者；evidence ID全局唯一。

### P0-C22-03｜calendar、课程与成本schema fail-open

Day 999、非法case、security slice字符串、unknown nested字段、每日`status=MAGIC`、负budget/人工分钟、重复证据、`single_intervention=false`、全成本负数且`within_budget=true`均PASS。

关闭条件：对所有nested object做exact schema、类型、enum、正数与唯一性验证；day必须覆盖0—30并与phase/gate映射一致；单变量干预要由候选diff与变更数派生；成本从model/tool/compute/human/failure/remediation账目汇总并与预算比较，禁止自报布尔。

### P0-C22-04｜Runtime、停止恢复、D21与毕业状态是自报字段

`openclaw@latest`、`sandbox=none`仍可配合字符串`stop=VERIFIED/restore=VERIFIED`得到PASS；毕业recommendation接受任意枚举。没有receipt、authoritative readback、artifact/delivery/environment evidence、撤权和残余检查。

关闭条件：绑定固定release/runtime manifest、权限与sandbox policy；停止必须有有效receipt与admission/queue/worker/effect readback；恢复绑定backup/checkpoint/target version与regression；D21三层从technical、delivery visibility、business/environment authority记录派生；毕业建议枚举固定为`LIMITED_DUTY/EXTEND/STOP/WITHDRAW/EXIT`等正式集合，且安全/污染/越权/证据造假非补偿。

## 3. P1与重审要求

- 新增至少30项独立negative regression，包含本轮15项以及重复camp/day/task/trial、错subject/version、stale/future evidence、valid digest wrong content、holdout lineage伪造、硬失败+UNKNOWN、预算超限但自报正常、stop receipt错任务等。
- 三件母产物内逐案登记20个case的run/trial/day、raw state、authority refs、expected/actual、停止、回退、退出、残余和证据链接；不得新建第四母产物。
- 两练习分别列出压缩离线路径与真实Day0—30路径的权限、命令、证据上限和验收；不得把机器状态机输出写成真实跨日成长。
- 事实门重审需逐条复核41/41 claims，并把C16—C18当前有限制通过、C19—C21仍在修订的状态同步到frontmatter、正文、ledger、自检和交接。

## 4. 门禁结论

- 初稿门：`PASS`。
- 事实门：`REVIEW_REQUIRED`。
- 交叉门：`REVIEW_REQUIRED`，P0-C22-01—04开放。
- 实践门：`REVIEW_REQUIRED`；没有真实30天纵向运行。
- 编辑门、总编门、RC：`not_reviewed / not_authorized`。


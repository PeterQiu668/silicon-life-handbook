---
review_id: C20-runtime-control-remediation
chapter_id: C20
review_type: author-remediation
reviewer_role: remediation-author
reviewed_on: "2026-09-30"
status: post_fix_independent_review_required
approval_status: unapproved
self_approval: false
---

# C20 v2.1 运行控制整改记录

本文件记录作者侧整改，不覆盖也不批准历史`fact-check.md`与`cross-review.md`。事实、交叉、实践、编辑、总编和RC门仍须由非作者裁决。

## 关闭映射

| 历史问题 | 作者侧修复 | 当前状态 |
|---|---|---|
| P0-X20-01 D21/authority/receipt/readback/recovery fail-open | root registries分别保存authority/policy、技术终态、delivery receipt/visibility、acceptance、effect receipt/readback、recovery；逐task/version/run解引用；明确technical/delivery/acceptance/recovery失败不依赖completion claim而独立硬FAIL，UNKNOWN为RR | author-fixed v2.1；待非作者复核 |
| P0-X20-02 closed-world/D22/effect/run identity fail-open | 严格root/scenario/state/nested key、type、enum、version、非负/有限/range、事件时间/序列与引用唯一性；四层D22；四类唯一ID；offline拒绝real-world与自填manifest；effect/real-world count动态派生 | author-fixed v2.1；待非作者复核 |
| P0-X20-03 digest/evidence只验格式 | event按canonical bytes重算digest和prev chain；root anchor绑定head/count；evidence registry绑定content digest与task/version/run | author-fixed；待非作者复核 |
| P0-X20-04 selfcheck过度声明 | 明确作者侧synthetic invariant control，不把确定性或负测外推真实可靠性 | author-fixed；待非作者复核 |
| P1-X20-04 A-C20-03未实例化 | A-C20-03逐行列出24个case的raw权威事实、expected/actual/reason、停止恢复与残余 | author-fixed；待非作者复核 |
| P1-X20-05 练习§8.1不完整 | 两练习具备目标、前置、权限、输入、步骤、产物、证据、停止、回滚、三态和迁移；明确offline/real路径 | author-fixed；待非作者实践复核 |
| P1-X20-06 上游状态过时 | 更新为C17事实/交叉有限制通过、实践RR；C19作者侧v2整改完成但非作者门待关闭 | author-fixed；状态仍provisional/limited |
| P2 source hygiene | TERMS与动态eval/tracing来源已有消费；OTel标题不再声称无法由动态URL证明的版本pin | author-fixed；待事实门复核 |

## v2控制合同

1. deterministic builder只负责生成完整raw-state；运行输入不含mutation recipe。
2. evaluator不读取case名或`expected_decision`裁决；expected只在派生后作冻结oracle比对。
3. 场景不能自报授权、完成、回执、读回、event anchor、证据或恢复真相，只能引用root authority registries。
4. D21三层分别取自technical、delivery与acceptance registries；三层合格才允许完成，任何硬失败不可被UNKNOWN或均值补偿。
5. offline环境固定无网络、无真实凭证、无外部副作用；任何representative real-world行或同文件manifest直接拒绝。
6. external effect与real-world evidence count由权威记录动态求和，不读取预置统计。

## 结果与哈希

- 24 trial：`4 PASS / 16 FAIL / 4 REVIEW_REQUIRED`；training 4、regression 4、holdout 16、real-world 0；security横切7；外部副作用0。
- decision digest：`6af7d47b0874a7de639a4e7d085b023decbfe787d12da12d7a15d5e03fcf8bbf`。
- builder：`a8d1714214e0e92e74a511f5572d8df598a3f35d525c50a2ded16bcf7fd0540a`。
- runner：`49a5c12d97bf73c8de554a49ba1ab7ba52b9b442181ab3634a75dd3fdbf8d021`。
- negative runner：`8580234cc38d51fef3f623d98bab23733afabcf5c9a16dfcf2edda57968b4c7b`。
- input：`9b2314a953585d6691d5f7532efac92da949d332b3597323c8e0fdda25548380`。
- results：`3e875dcdbb36e678834271eb980517a628535e3ede579827c3be34c179e9e78a`。
- summary：`367f58c1aee55d5ecab9a8d6edcc50902b10c1931183bf7dd99bdd3249dbad24`。
- negative results：`95ec684e7e067346a53dbd43c405da87c19430e5201317e37c0b1f4783540984`。

## 46项负向控制

覆盖wrong root version、root/scenario/state/nested unknown field、wrong type、非法第五层、synthetic冒充real、自填manifest、重复scenario/task/trial/run、跨run错绑、registry digest篡改、registry未知字段、缺technical terminal、delivery visibility矛盾、acceptance矛盾、event digest错误、证据未解析、fake authority/policy、fake receipt/readback、unanchored recovery、external effect、硬失败+UNKNOWN、UNKNOWN→RR、非法terminal/effect enum、过期authority、chain anchor错误、evidence错绑、recovery矛盾、case名/expected裁决不变性，以及v2.1新增的无completion claim技术/交付/验收/恢复显式失败、负observed count、负retry attempts、越界sampling rate、非法event时间、重复seq、重复evidence ref和非有限成本。`46/46 PASS`。

## fresh-temp复现

两个最终新目录`/tmp/c20-v21-a.NrkJ7Q`与`/tmp/c20-v21-b.JHgeYZ`仅复制三支脚本后重建；input、results、summary、negative results四文件彼此及与保存件逐字节一致。临时目录仅为复核证据，不是书稿依赖。

## 未关闭的真实限制

没有运行真实OpenClaw/Hermes、OTel collector、Prometheus、provider、Queue、Channel、授权服务、成本后端、进程重启或外部readback；没有真实客户数据、凭证或生产副作用。Muse仅为VENDOR-CLAIM镜面。因而作者只建议把局部synthetic machine control送非作者复核，完整实践门保持`REVIEW_REQUIRED`。

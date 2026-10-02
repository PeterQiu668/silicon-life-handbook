# C21 出版前生产记录索引

本索引承接从读者正文迁出的生产版本、运行摘要、整改与审批记录；不改变真实平台、外部effect、跨平台迁移和专业法律判断仍为 `REVIEW_REQUIRED` 的边界。

## 运行与生产信息

- 状态化运行包历经v2、v2.1、v2.2、v2.3与v2.4生产迭代；历史记录保存在本目录既有review与runs文件中。
- v2.4基线含79个唯一trial，分布为 `3 PASS / 74 FAIL / 2 REVIEW_REQUIRED`，保存76项非PASS场景。
- 作者负测50项包含历史独立38项与新增事件链12项；生产记录称全部命中，原晚审早发逃逸转为FAIL。
- 曾记录decision digest为 `sha256:9071b8085481a4e774e1ad014d8f1db77e92bdb75cd817895131047db2f7b82e`，双fresh-temp的root、input、result、summary与negative result逐字节一致。

## 历史变更摘要

- 2026-09-30建立21.1—21.8、四件母产物、两项练习与证据账本；随后加入closed-world状态化harness、D21完成三面、D22四层、唯一ID与恢复/迁移/撤权/处置硬门。
- v2引入独立registry与canonical digest；v2.1补rollback回执、owner适配、数值范围、backup冲突与不可逆迁移；v2.2物理分离authority root并补rollout/runtime/effect、生命周期、环境/法域与holdout约束。
- v2.3将rollout plan、trial/task/dataset/grader/terminal、receipt/readback、automation与layer/holdout/security证据纳入冻结根；v2.4补publication/lifecycle event时间链。
- 历史作者自检和独立门状态以既有review记录为准；本索引不签任何门禁。

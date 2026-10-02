---
review_id: C16-stateful-remediation-20260930
chapter_id: C16
review_type: author_side_remediation_note
reviewed_on: "2026-09-30"
status: post_fix_independent_review_required
independent_signoff: false
---

# C16 状态化实践修补记录

本记录响应独立实践门提出的六项 P1，不是非作者签核。

## 关闭设计

- 删除预裁决布尔，改从 principal/alias、grant/expiry、credential owner、writer lease/write version、source origin、预算与 stop receipt、cancel tree/readback、三层终态、effect ledger 和双臂原始指标推导。
- 公平合同逐字段比较 task、input、permission、budget、risk、acceptance、environment；不可比时最多 `REVIEW_REQUIRED`，冻结 oracle 不允许其伪装为 PASS。
- 净收益先过权限、安全、预算、取消、终态硬门，再执行经批准的质量、成本、延迟、人工、通信、冲突、恢复和证据完整性向量阈值；任意小质量正值不再补偿极端代价。
- 每个 scenario 保存至少三条独立 run 记录；run ID、trace digest、evidence digest 全局唯一，并含输入版本、三层终态、基线与候选原始指标。
- effect count 从同一 ledger 推导；确认外部写时不能同时汇总为零。
- closed-world schema 拒绝未知字段/枚举、试次不足、重复 run/trace/evidence、错误类型和旧预裁决字段。
- 真实层逐 run 解引用 manifest，绑定 origin/source/run/evidence；合成夹具真实层必须为 0。
- 第二轮窄复核暴露的近邻缺口已封闭：ISO-8601 时间真实解析、alias-principal 一一映射、writer 可解析与同 base 多写检测、FACT 至少双独立来源、预算阈值停止回执、取消回执、run evidence 三态、effect 三态以及跨 run evidence ID 全局唯一。

## 作者侧结果

- 固定 v3：45 trial，`12 PASS / 27 FAIL / 6 REVIEW_REQUIRED`；15 task；真实层 0；四个 synthetic-shadow 场景、12 trial；effect 0。
- 两个 fresh temp 的 results 与 summary 分别逐字节一致。
- input：`e9752e4e93d9a386648609243a0dbfc39b7b6d56c8a2694038f0f180705a232a`。
- runner：`e779f28014ce4341c59a6fcd724bef1d861e5958ad7bcbb7bfbc3afdddcaedee`。
- results：`249b9ab98d4447e7b3bd621c4546a97c277ea3c8b0c9f38009cf812b0e43129b`。
- summary：`59d406d7fd5caeadb4c26e553aa4370a19a456dce9aa16d196f14a73c756177c`。
- 已定向验证：合同失配、旧布尔字段、零 run、重复 trace、dummy 真实层均非零退出；确认外部写在将 oracle 同步为 FAIL 后得到45 FAIL、effect count 45、zero=false。新增近邻攻击中，畸形 expiry、alias collision、未知 writer、同 base 双 writer 同结果但无 merge、FACT 最小来源0、到阈值无 stop receipt、cancel 无 receipt、evidence FAILED/UNKNOWN、effect UNKNOWN、跨 run 重复 evidence ID 全部被拒绝或降级，不能 PASS。

## 限制

所有记录仍为离线合成观测。真实 OpenClaw/Hermes/A2A Runtime、生产身份/授权、并发写、取消传播、外部终态和代表性真实任务未运行；X01/X02、P0-05/06/07 和章节总实践门继续为 `REVIEW_REQUIRED`，直到非作者 post-fix 复验及真实授权实践完成。

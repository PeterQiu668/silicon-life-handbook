# C20 出版前生产记录索引

本索引承接从读者正文迁出的作者运行、整改与审批记录；不改变真实平台实践仍为 `REVIEW_REQUIRED` 的边界。

## 运行文件

- `runs/synthetic-reliability-input.yaml`
- `runs/synthetic-reliability-results.yaml`
- `runs/synthetic-reliability-summary.md`

## 迁出的生产信息

- 状态化夹具曾以v2.1生产标识记录；24个主场景分布为 `4 PASS / 16 FAIL / 4 REVIEW_REQUIRED`，D22为training 4、regression 4、holdout 16、representative real-world 0，security/red-team横切7个，外部副作用0。
- 双fresh-temp构建与运行曾记录字节一致，decision digest为 `6af7d47b0874a7de639a4e7d085b023decbfe787d12da12d7a15d5e03fcf8bbf`。
- 46项独立负向回归覆盖schema、类型、枚举、版本、唯一ID、跨run绑定、D21、D22、authority/policy、receipt/readback、事件链、时间序列、证据引用、数值范围、外部effect和硬失败非补偿。
- 2026-09-30建立作者包；历史作者自检、事实/交叉/实践状态以本目录既有review记录为准。本索引不签任何门禁。

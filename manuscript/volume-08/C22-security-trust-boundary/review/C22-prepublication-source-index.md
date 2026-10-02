# C19 出版前生产记录索引

本索引承接从读者正文迁出的生产记录，不构成读者版事实主张，也不改变真实实践仍为 `REVIEW_REQUIRED` 的边界。

## 运行与证据文件

- `runs/frozen-security-authority.yaml`
- `runs/synthetic-security-input.yaml`
- `runs/synthetic-security-results.yaml`
- `runs/synthetic-security-summary.md`
- `runs/security-negative-regression-results.yaml`
- `runs/v2.4-effect-time-readback-regression-results.yaml`
- `runs/v2.4-fresh-temp-reproduction.yaml`
- `v2.4-effect-time-readback-remediation.md`

## 迁出的生产信息

- 23个主trial分布为 `2 PASS / 20 FAIL / 1 REVIEW_REQUIRED`；D22计数为training 4、regression 4、holdout 15、representative real-world 0，security/red-team为横切切片，外部副作用为0。
- 作者定向负测91项，历史独立攻击9项，后续独立攻击及近邻回归34项；生产稿曾记录相应suite为零逃逸。
- 两个fresh-temp目录的input、authority、主结果、负测结果与summary逐字节一致。曾记录authority root `sha256:17f53430...d84b1a`、主decision digest `b3d63dec...94d48`、作者负测suite digest `a2135ff6...e98a`、专项suite digest `sha256:b6614494...e9c463`。
- 2026-09-30创建作者包；2026-10-01依次完成冻结权威根、session/effect/audit/incident/recovery谱系、执行时授权重验、独立readback与严格时间链整改。
- 历史生产状态、作者自检和独立审校以本目录既有review文件为准；本文不签事实、实践、交叉、主编或发布门。

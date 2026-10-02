---
review_id: C24-v2-stateful-remediation-20260930
chapter_id: C24
review_type: author_side_remediation_note
reviewed_on: "2026-09-30"
status: drafting
fact_gate: awaiting_independent_re_review
cross_gate: awaiting_independent_re_review
practice_gate: REVIEW_REQUIRED
independent_signoff: false
release_candidate_authorized: false
---

# C24 v2 raw-state 整改记录

本记录响应`independent-fact-cross-review.md`的P0-C24-01—05与P1。历史独立审校不改写；本记录只陈述作者实现，不批准事实、交叉、实践、编辑、总编或RC门。

## 关闭合同

- 正式scenario从mutation token改为完整raw state；输入不存在`mutation / case / expected`，runner不读取scenario名称裁决。
- principal、authority、reviewer、appeal、evidence、trial、MAT prerequisites、七维、组织roster、namespace、certificate、lifecycle、change与effect均使用closed-world registry、严格类型/enum/finite/ISO时间、分别唯一ID和canonical digest。
- authority精确绑定actor/action/subject/application digest/scope/status/time；作者、controller、主体及其alias不能担任独立reviewer或domain expert，appeal另需独立reviewer与authority。
- manifest、artifact、application signature、holdout lineage、grader、失败档案、cost、D21、七维、组织、公开主张与lifecycle证据均须解引用并校验subject/object/version/scope/owner/status/time/content digest。
- MAT-L0—MAT-L5前置等级显式映射；七维最弱必要门、安全非补偿；组织认证另需roster、collaboration、isolation与control证据，成员平均不能生成组织证书。
- certificate、namespace、review与maturity decision构成联合硬门；证书绑定application/release/review/maturity/namespace/bundle，公开主张和五态生命周期必须与同一ledger一致。
- 离线real-world、real-certificate和external-effect尝试从逐scenario状态动态计数并无条件FAIL，不能把常量0冒充控制有效。

## 保存回归

v2保存57个唯一trial：`3 PASS / 50 FAIL / 4 REVIEW_REQUIRED`，其中54项为负向或未知回归。它覆盖独立审校28项，并扩展valid digest wrong content、signature subject/scope/version、stale holdout、grader泄露、失败删除、cost错配、多证书冲突、暂停后仍公开、撤回authorization、生命周期错绑及hard+UNKNOWN。

```yaml
schema: c24.cert.input.v2
trials: 57
distribution: {PASS: 3, FAIL: 50, REVIEW_REQUIRED: 4}
lifecycle: {ACTIVE: 1, LIMITED: 1, SUSPENDED: 4, REVOKED: 50, EXPIRED: 1}
real_world_attempts_rejected: 1
real_certificate_attempts_rejected: 1
external_effect_attempts_rejected: 1
decision_digest: sha256:1fb829291c92c0f09c16e6b2eeaeb628ae6b74e4418e327c0471e50d2c19b1b2
builder_sha256: e2656b3949c93c0dfb934f3821f645dcfb5fc8ee7282c96111f0e1cd4b28fb1c
runner_sha256: c406d08fc290d54e618ba641c7ac176b62fe57217807a3eaee31617ab6dfed78
input_sha256: b5573d0f1962e217ed02e877cd7447058264de1dafbd9ca0f97e58035d90bf5e
results_sha256: 3e203040112e2f6486acfd0028d37302301d26d06e9aa20ee3e7741a3f590572
summary_sha256: b136b3631025d5cdb09dbb66b38f93a3906b518852729033ef76c623a3baa350
```

这些计数只证明离线合成控制：没有真实authority、代表性生产任务、真实OpenClaw/Hermes运行、外部认证机构或法域专业复核。所有真实认证继续`REVIEW_REQUIRED`，等待非作者fresh-temp、近邻突变与事实/交叉/实践门复核。

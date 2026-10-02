---
review_id: C14-post-fix-independent-practice-review-20260930
chapter_id: C14
review_type: post-fix-independent-practice-gate
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
frozen_v3_fixture_reproduction: PASS
original_17_control_regression: PASS
combination_precedence_control: PASS
real_world_manifest_resolution_control: PASS
post_fix_synthetic_machine_control: PASS
machine_control_scope: v3_1_offline_stateful_synthetic_control
x_c14_01: REVIEW_REQUIRED
x_c14_02: REVIEW_REQUIRED
overall_practice_gate: REVIEW_REQUIRED
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C14 v3 状态化补强独立实践复核

## 1. v3.1 第二轮窄复核与最终裁决

**v3.1 干净基线双复现 `PASS`；首轮 17 类与指定组合继续 `PASS`；两个安全早退和 dummy provenance 三项窄回归全部关闭。因此局部 stateful synthetic machine-control 升级为 `PASS`；X-C14-01、X-C14-02 与总实践门仍为 `REVIEW_REQUIRED`。**

当前固定文件为：input `2eaa56022ac0c631566094d3791d685929ccb7c7d449a90922a0c10a857aff6c`、runner `998529e01f761ee65e5b75e26f338e7b9072b5a8d682d45d2531d39ddbdc1486`、results `90b65e2246dcbeb69f22710e5aeadfbcc8375b0233b32b8261f175cc8f890540`、summary `8abdf613ee48dde2f34377ad7f2ad30a952e20b07b1dfad422c08b7a46b5b8e4`、README `f861632b7162e2ae687af5210cac22dc470df2f1f089b6e0b6ec6410ab5b7c96`。

RUN-A `c14-v31-a.9R9I8o` 与 RUN-B `c14-v31-b.eg9hns` 在两个 fresh temp 原样复跑，results/summary 分别逐字节一致并等于作者保存文件；固定分布仍为 28 trial、`11 PASS / 14 FAIL / 3 REVIEW_REQUIRED`、真实层 0、synthetic shadow 6、confirmed external writes 0。

三项关闭证据：

| v3 缺口回归 | v3.1 结果 | 裁决 |
| --- | --- | --- |
| 干净 revocation observation + UNKNOWN blind retry | `FAIL / unknown_effect_blind_retry` | 正向撤权证据不再早退遮蔽 UNKNOWN |
| 合法 break-glass + material change 无新认证 | `REVIEW_REQUIRED / material_change_requires_recertification` | 合法紧急动作不再替代再认证 |
| synthetic 改名 real-world + dummy source/run/evidence IDs | 进程 `ValueError` | evidence ID 必须解引用 verified manifest 且 source/run 匹配 |

局部 PASS 的范围严格限定为当前 v3.1 离线状态化控制：它证明这套合成 schema、账本推导和已执行突变在当前固定输入/runner 下 fail-closed；不证明真实 principal directory、授权服务、OpenClaw/Hermes 撤销传播、组织 break-glass、真实 effect readback 或 representative-real-world 数据真实性已经运行。

```yaml
v3_1_closure_gate:
  frozen_fixture_reproduction: PASS
  original_17_control_regression: PASS
  specified_combination_regression: PASS
  hard_failure_and_unknown_non_masking: PASS
  real_world_manifest_resolution_control: PASS
  post_fix_synthetic_machine_control: PASS
  machine_control_scope: v3_1_offline_stateful_synthetic_control
  x_c14_01: REVIEW_REQUIRED
  x_c14_02: REVIEW_REQUIRED
  real_openclaw_hermes_authorization_revocation_runtime: NOT_RUN
  overall_practice_gate: REVIEW_REQUIRED
```

以下 `1A—4` 记录 v3 第一轮发现，作为修复谱系保留，不代表当前 v3.1 裁决。

## 1A. v3 第一轮裁决（历史快照）

**v3 冻结夹具复现 `PASS`；首轮 17 类缺口回归 `PASS`；组合优先级控制 `FAIL`；因此 post-fix synthetic machine-control 仍为 `FAIL`，X-C14-01、X-C14-02 与总实践门继续 `REVIEW_REQUIRED`。**

作者 v3 已实质修复首轮问题：runner 现在从 alias→principal 图、grant/policy/revocation、request object/parameter/scope、delegation 集合、effect ledger、stop receipt、rollback proof、break-glass 原始记录与再认证前后指纹推导门禁；重复 ID、无证据的真实层标签、真实层 executed/count 不一致和外部 effect 非零也会被拒绝。原实践评审的 P1-C14-01 至 P1-C14-06，在“单一合成状态控制”范围内均已关闭。

但两个安全早退仍会把同一 trial 中尚未检查的风险变成 PASS：`revocation_check()` 的干净负向访问直接返回 PASS，跳过 effect/cancellation/break-glass/recertification；合法 `break_glass_check()` 直接返回 PASS，跳过其后的 recertification。组合突变稳定复现“干净撤权负测 + UNKNOWN effect → PASS”与“合法 break-glass + material change 无新认证 → PASS”。这不是缺少真实平台造成的限制，而是当前离线控制流的 fail-open，因此不能给通用 synthetic machine-control PASS。

另有来源边界：真实层 schema 已要求 `source_id/run_id/evidence_id`，但这些字符串没有解引用到受信 manifest；把合成记录改名并填写三个 dummy ID 仍可获得 real-world PASS。该结果不否定 schema 完整性修复，但说明 provenance authenticity 仍未闭合。

结构化证据见 [post-fix-independent-authorization-reproduction-20260930.yaml](runs/post-fix-independent-authorization-reproduction-20260930.yaml)。本复核没有修改作者 input、runner、results、summary、README、正文、ledger、母产物、练习或既有审稿文件。

## 2. 双 fresh-temp 复现

| 对象 | SHA-256 |
| --- | --- |
| input v3 | `2eaa56022ac0c631566094d3791d685929ccb7c7d449a90922a0c10a857aff6c` |
| runner v3 | `be1bf3ec3fd1d6429cd588ab5b521efe2bf064f469c55899afc5387b14062c9e` |
| 作者 results | `4f8bc546dc1628b6ff869194596c32d2cd83ce6f3538cb898ced8d19103e3415` |
| 作者 summary | `8abdf613ee48dde2f34377ad7f2ad30a952e20b07b1dfad422c08b7a46b5b8e4` |
| README | `f861632b7162e2ae687af5210cac22dc470df2f1f089b6e0b6ec6410ab5b7c96` |

RUN-A `c14-postfix-a.dTW93T` 与 RUN-B `c14-postfix-b.NrAuBv` 在两个 fresh temp 中仅复制 input/runner 后运行。两次 results、summary 逐字节一致，并等于作者保存文件。固定合同保持：28 trial、`11 PASS / 14 FAIL / 3 REVIEW_REQUIRED`、task/trial 唯一、真实层 0、synthetic shadow 6、confirmed external writes 0。

## 3. 首轮 17 类回归

| 原缺口 | v3 结果 | 裁决 |
| --- | --- | --- |
| 模糊聊天同意 | `FAIL / intent_is_not_authority` | 关闭 |
| 自授权 | `FAIL / no_self_authorization` | 关闭 |
| grant 过期 | `FAIL / authorization_expired` | 关闭 |
| grant 撤销 | `FAIL / authorization_revoked` | 关闭 |
| 缓存旧 policy | `FAIL / cached_approval_cannot_override_current_policy` | 关闭 |
| 对象与参数偷换 | `FAIL / object_mismatch` | 关闭；参数分支同一比较循环覆盖 |
| 子委托扩权 | `FAIL / delegation_must_attenuate` | 关闭 |
| UNKNOWN 盲重试 | `FAIL / unknown_effect_blind_retry` | 关闭 |
| stop confirmed 但 rollback proof 缺失 | `FAIL / cancel_stop_and_rollback_are_distinct` | 关闭 |
| 同人 alias 伪双批 | `FAIL / two_person_review_not_independent` | 关闭 |
| 非法 break-glass 类型/scope/expiry/复核者 | `FAIL / break_glass_controls_incomplete` | 关闭 |
| material change 无新认证 | `REVIEW_REQUIRED` | 关闭：未错误 PASS |
| 撤权后旧 session 残留 | `FAIL / revocation_not_cascaded` | 关闭 |
| 合成记录冒充 real-world 且无三证 ID | 进程 `ValueError` | 关闭 |
| effect ledger confirmed write 非零 | `FAIL`，输出 count=1 | 关闭 |
| 重复 task/trial ID | 进程 `ValueError` | 关闭 |
| real-world executed=true、记录数为 0 | 进程 `ValueError` | 关闭 |

四个指定组合也按预期阻断：stale policy + revoked grant + object swap + UNKNOWN 为 FAIL；alias 自授权 + 伪双批为 FAIL；stop confirmed + rollback 缺失为 FAIL；revocation residual 为 FAIL。单一状态控制和这些指定组合均达到 v3 补强目标。

## 4. 新发现的组合优先级缺口

### P1-C14-PF-01：成功撤权负测遮蔽 UNKNOWN/effect 风险

在原 `TRIAL-C-03` 的干净 `revocation_observation` 上增加 `effect_ref=effect-unknown-retry`。`revocation_check()` 先返回 `PASS/revoked_access_denied`，`effect_check()` 从未执行，最终仍 PASS。

最小关闭合同：正向控制检查不得提前形成最终 PASS。`revocation_check` 在“无残留且负向访问拒绝”时应返回“无阻断 + audit fact”，继续执行其余 applicable checks；或统一收集所有事实后按 `FAIL > REVIEW_REQUIRED > PASS` 聚合。任何 UNKNOWN blind retry、confirmed external write 或其他硬失败都必须优先于正向证明。

### P1-C14-PF-02：合法 break-glass 遮蔽 material-change 再认证

在合法 `TRIAL-C-07` 上加入 model 变化且 `new_certification_ref=null`。`break_glass_check()` 先返回 PASS，后续 `recertification_check()` 未执行，最终仍 PASS。

最小关闭合同：break-glass 合法只证明当前紧急动作符合例外合同，不能证明后续版本、权限或目标仍获认证。合法分支应继续其余检查；material change 无新认证至少 REVIEW_REQUIRED。若 break-glass 与安全/权限硬失败并存，最终必须 FAIL。

### P1-C14-PF-03：真实层三证 ID 未解引用

把一个 synthetic shadow 改成 `representative_real_world`，把 environment/data_origin 一并改名并填写 `dummy-source/dummy-run/dummy-evidence`，runner 接受并报告真实层 1 trial。

最小关闭合同：三个 ID 必须解引用到受信 source manifest、实际 run record 和不可变 evidence digest；manifest 需含 data origin、采集权限、时间、环境与内容 hash。仅有非空字符串不能把 synthetic 提升为 real-world。若本地 harness 不承担真实性验证，应明确把该门输出为 REVIEW_REQUIRED，而不是 PASS。

## 5. X-C14-01 / X-C14-02 与实践总门

X-C14-01 与 X-C14-02 均保持 **`REVIEW_REQUIRED`**。v3 已能支持大部分离线机器演练，但组合优先级仍 fail-open；真实 principal directory、授权服务、policy store、撤销传播、queue/session/grant 清理、执行主机 stop receipt、break-glass 组织批准与真实 effect readback 均未运行。

```yaml
post_fix_practice_gate:
  frozen_v3_fixture_reproduction: PASS
  original_17_control_regression: PASS
  specified_combination_regression: PASS
  hard_failure_and_unknown_non_masking: PASS
  real_world_manifest_resolution_control: PASS
  post_fix_synthetic_machine_control: PASS
  machine_control_scope: v3_1_offline_stateful_synthetic_control
  x_c14_01: REVIEW_REQUIRED
  x_c14_02: REVIEW_REQUIRED
  real_openclaw_hermes_authorization_revocation_runtime: NOT_RUN
  overall_practice_gate: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

## 6. 安全与验证边界

所有运行均为本地纯合成副本，无网络、无真实凭证、无真实收件人、无生产写。v3 的状态化单控改进是真实可复现的，但不能外推到 OpenClaw/Hermes 或组织授权服务；Muse 仍只可作为公开产品镜面。本复核不批准编辑、总编或 release candidate。

完成记录后运行 YAML/frontmatter、hash、`py_compile`、本地链接、formal/book validator 与限定 diff check。并发章节错误必须单独归因。

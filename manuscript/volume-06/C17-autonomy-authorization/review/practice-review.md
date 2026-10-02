---
review_id: C14-independent-practice-review-20260930
chapter_id: C14
review_type: independent-practice-gate
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:platform_research"
independent_from_author: true
chapter_status_after_review: drafting
frozen_fixture_reproduction: PASS
synthetic_machine_control: FAIL
x_c14_01: REVIEW_REQUIRED
x_c14_02: REVIEW_REQUIRED
overall_practice_gate: REVIEW_REQUIRED
facts_gate: not_reviewed_by_this_reviewer
cross_gate: not_reviewed_by_this_reviewer
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C14 独立实践门审校

## 1. 裁决

**冻结的 28-trial 离线夹具复现 `PASS`；通用授权 machine-control `FAIL`；X-C14-01、X-C14-02 与总实践门均为 `REVIEW_REQUIRED`。**

两个 fresh temp 目录原样复跑，results 与 summary 分别逐字节一致并等于作者保存文件。固定分布为 `11 PASS / 14 FAIL / 3 REVIEW_REQUIRED`，28 个 task ID、28 个 trial ID 及 28 个 task/trial pair 均唯一；报告的外部副作用为 0；`representative_real_world` 实际层计数为 0；6 条未来真实层样本保留为 holdout 中的 `synthetic_shadow`。这些结论只证明冻结夹具可重复。

runner 对 `self_authorization`、`fuzzy_chat_consent`、`authorization_status`、`cached_old_approval`、`parameter_match`、`object_match`、`subdelegation_expands`、`effect_unknown`、`stop_confirmed`、四个 break-glass 布尔量、`recertification_complete` 等预裁决字段做路由，但没有从原始主体、授权记录、对象与参数、时间、策略版本、身份图、委托图、撤销账本、效果账本或再认证指纹推导这些字段。17 项定向突变中，15 类危险原始事实被忽略或可被自报标签覆盖；另有一项重复 ID 被接受，一项虚报 real-world executed/count 的直接不一致被正确硬拒绝。因此 frozen fixture 不能升级为通用授权控制。

结构化证据见 [independent-authorization-reproduction-20260930.yaml](runs/independent-authorization-reproduction-20260930.yaml)。本审校没有修改正文、ledger、母产物、练习、作者 input/runner/results/summary/README，亦不签事实、交叉、编辑、总编或 release-candidate 门。

## 2. 双 fresh-temp 复现

| 对象 | SHA-256 |
| --- | --- |
| input | `5f089427e411b6289a3cf56c29ec7aeb389d3b9eb72b0eb9b81577c93919cdb3` |
| runner | `c5a94eaa38fca806debe4e2e438b5c4bb61fa8db8e312af1b5920fde102cd6d2` |
| 作者 results | `ad4d1eccb30b77531133f30f88cd39f997e074f31e039544954d43dcfb171442` |
| 作者 summary | `826e210a6ca1377422e891234fa580a7710e148396190bb496f2210dcd3354ff` |
| README | `99e85eba3bc8bd604f8abff67c1b967e2a18497b76d680eb5d9ab718dac6cdc6` |

RUN-A `c14-auth-a.bBaWRG` 与 RUN-B `c14-auth-b.lwhcdS` 都只复制当前 input 与 runner，再执行 `python3 run-authorization-harness.py`。两次退出码为 0；input、runner、results 和 summary 哈希一致；results/summary 与作者保存文件逐字节一致。

固定夹具完整性如下：

| 项目 | 结果 |
| --- | --- |
| trial | 28 |
| gate 分布 | `PASS 11 / FAIL 14 / REVIEW_REQUIRED 3` |
| task ID / trial ID / pair | 分别唯一 |
| D22 training / regression / holdout | `6 / 8 / 14` |
| representative real-world | 0 |
| synthetic shadows | 6，均为 holdout |
| reported external side effects | 0 |
| expected matched | true |

结果中的 `external_side_effects: 0` 是 runner 常量，不是 effect ledger 回读。真实“无外部副作用”只能由源码边界支持：runner 只读写本地固定文件，不导入网络、平台 SDK 或真实执行客户端。本结论不得冒充真实环境效果证明。

## 3. 代码级推导审计

### 已实际执行的控制

- D22 layer 只允许四个规范名；`offline-synthetic` 环境不能直接包含 `representative_real_world` trial。
- `representative_real_world_executed` 必须与实际 layer 记录是否存在一致；直接把 flag 改为 true、但仍为零记录时，进程以 `ValueError` 失败。
- 固定的 `fuzzy_chat_consent=true`、`self_authorization=true`、expired/revoked、缓存旧批准、对象/参数不匹配、委托扩权、UNKNOWN 盲重试、撤销未级联、伪回滚、break-glass 缺项、同 ID 双批、重大变化未再认证和 hard-risk execute 分支会产生预期门禁。
- expected 只用于 `matched`，不直接作为 gate 返回值。

### 没有从原始证据推导的控制

- 身份：没有主体解析、稳定 principal ID、alias 合并、审批者资格或 requester/approver 独立性图。
- 授权记录：没有 grant ID、issuer、object/action/scope、参数哈希、policy version、issued/expiry time 与当前时钟的联合校验。
- 委托与撤销：没有父子 scope 集合比较、max-depth、父权上界、旧 session、queue、cache、temporary grant 的枚举与负向访问结果。
- 效果与停止：没有 effect ledger、幂等 readback、retry ledger；`cancel`、stop confirmation 与 rollback proof 没有各自的证据对象。
- break-glass：只信四个布尔量，不核紧急类型、实际 scope、绝对过期时间或独立复核者 principal。
- 再认证：只信 `material_change` 与 `recertification_complete`，不比较模型、工具、对象、参数、owner 或 policy 指纹。
- 运行完整性：task/trial 重复只在摘要写 `unique=false`，runner 仍成功退出；real-world 来源身份可通过把环境与 layer 一起改名自报。

## 4. 定向负向突变

| 注入 | 当前观察 | 应有控制 |
| --- | --- | --- |
| 模糊聊天文本作为唯一授权，但 `fuzzy_chat_consent` 未置 true | `PASS` | 从 authority source/type/text 识别不可授权，FAIL |
| requester 与 approver 是同一 principal，但 `self_authorization=false` | `PASS` | principal 图归一后拒绝自授权 |
| 绝对过期时间早于执行时间，但 `authorization_status=active` | `PASS` | 用固定时钟计算过期，FAIL |
| revocation ledger 已撤销 grant，但状态仍自报 active | `PASS` | 权威账本优先，FAIL |
| approval policy v1、当前 policy v2、cache hit | `PASS` | 版本不匹配不得复用 |
| 授权对象 A/参数 hash A，执行对象 B/参数 hash B | `PASS` | 对象和参数 exact match，FAIL |
| child scope 增加 deploy 且父禁止转委托 | `PASS` | 集合差与 max-depth 联合拒绝 |
| effect ledger 为 UNKNOWN 且已盲重试、未复用幂等键 | `PASS` | unsafe retry 为 FAIL |
| cancel 后 stop confirmed，但无 rollback proof，却宣称 rollback | `PASS` | cancel、stop、rollback 分别验真；伪回滚 FAIL |
| 两个 approver alias 对应同一 canonical principal | `PASS` | 归一身份后判非独立，FAIL |
| break-glass 实际类型、scope、expiry、复核者均违规，四布尔仍 true | `PASS` | 从原始记录推导，FAIL |
| 模型/工具/对象/owner 指纹变化，但 `material_change=false` | `PASS` | 指纹 diff 触发再认证 |
| 已撤销 grant 仍留 active old session/queue/temp grant | `PASS` | 任一残留可执行则 FAIL |
| 合成 trial 把 environment/layer 改名为 real-world、无执行证据 | `PASS`，报告 real-world count 1 | 来源证明缺失至少 REVIEW_REQUIRED |
| effect ledger 有 confirmed write | trial 仍 `PASS`，摘要仍称零副作用 | 从 ledger 汇总；违反零效果合同则 FAIL |
| 两条记录使用相同 task/trial ID | 退出码 0，仅摘要 `unique=false` | schema/run 硬失败 |
| 只有 executed flag=true、真实层记录仍为 0 | `ValueError` | PASS：直接 count/flag 不一致被拒绝 |

这些突变只发生于临时副本。它们证明 runner 不是简单照抄 `expected`，也证明当前主要风险不是固定路由表本身，而是调用方能够自行声明路由表所消费的安全结论。

## 5. P1 与最小修复合同

### P1-C14-01：身份、意图与审批独立性依赖自报标签

最小修复合同：建立 requester、grant issuer、approver 与 executor 的稳定 principal ID；对 alias 做 canonicalization；从 authority source 与签名记录区分聊天意图和有效授权；自授权与同主体伪双批必须由身份图确定性拒绝，不能靠调用方填布尔值。

### P1-C14-02：授权对象、参数、时窗、策略与撤销没有权威读回

最小修复合同：每次副作用前读取 grant ID、issuer、action、object、scope、parameter/content hash、policy version、issued/expiry、status 与 revocation ledger；以执行时刻重新比较，不接受缓存状态覆盖权威记录。任一对象/参数/版本/时窗不匹配均 FAIL。

### P1-C14-03：委托衰减和撤销传播没有状态图

最小修复合同：由父授权、delegator own rights、child minimum need 计算交集，验证深度、时窗、次数与对象均不扩大；撤销后枚举 child grants、session、queue、cache、temporary grant 与在途动作，逐项负向访问。任一旧引用仍可执行即 FAIL，传播不可核为 REVIEW_REQUIRED。

### P1-C14-04：UNKNOWN、效果、cancel、stop 与 rollback 未闭环

最小修复合同：从 effect ledger 汇总 `CONFIRMED/NOT_APPLIED/UNKNOWN`，记录 readback、retry count 和 idempotency key；UNKNOWN 盲重试为 FAIL。cancel request、stop receipt、rollback/compensation proof 使用不同 ID 与状态机；stop 完成不能自动证明 rollback。外部 effect count 不得常量写零。

### P1-C14-05：break-glass 与重大变化再认证只检查结论布尔量

最小修复合同：break-glass 从预注册紧急类型、目标、动作、窄 scope、绝对 expiry、requester 与独立 reviewer principal 推导；重大变化由 pre/post fingerprint 覆盖 model/tool/object/parameters/owner/policy/environment，任一 material diff 自动冻结旧 grant，直到新认证完成。

### P1-C14-06：运行 schema 与真实层来源证明 fail-open

最小修复合同：重复 task/trial ID、缺字段和非法组合在运行前硬失败；`representative_real_world` 不能只由 environment/layer 字符串获得，必须引用可核验 source/run/evidence ID，并禁止 synthetic origin 伪装。报告的 effect、real-world count 与执行状态必须从实际记录派生。

## 6. X-C14-01 裁决

**`REVIEW_REQUIRED`。**

固定夹具覆盖了观察、草拟、模拟外发/生产动作的部分等级与审批路由，也保存了模糊同意、自授权、对象/参数不匹配、旧批准、UNKNOWN 与 hard-risk 的预置失败样本。但练习要求“精确授权只消费一次”、真实主体/批准者校验、固定对象与参数、撤销负测、停止/回滚分离和客观副作用证据；当前 runner 没有 grant consumption ledger、principal graph 或 effect ledger，且对应原始突变会 fail-open。真实授权服务与平台执行未运行，所以不能给完整 PASS。

## 7. X-C14-02 裁决

**`REVIEW_REQUIRED`。**

固定夹具覆盖委托扩权、撤销级联、break-glass、双批与再认证的布尔路由；但没有从父子 scope 计算衰减，没有枚举旧 session/queue/grant 残留，没有核紧急类型与绝对 expiry，也没有比较 material-change 指纹。真实 OpenClaw/Hermes identity graph、授权服务、撤销传播、执行主机 stop receipt 与组织 break-glass 复核未运行，因此仍需真实沙箱/目标环境证据。

## 8. P0 实践项与最终门

| 项 | 独立实践裁决 | 理由 |
| --- | --- | --- |
| P0-05 可执行、可停止、可回滚 | `REVIEW_REQUIRED` | 冻结步骤可跑，但 stop/rollback 只读预裁决字段，真实执行主机未跑 |
| P0-06 高风险权限、审批、隔离 | `FAIL`（machine-control 范围） | 原始主体、授权对象、撤权和审批独立性可被自报布尔绕过 |
| P0-07 基线、证据、客观验收 | `REVIEW_REQUIRED` | 固定基线可重复；effect ledger、真实层来源与重复 ID 未被硬门保护 |

```yaml
practice_gate:
  chapter_id: C14
  frozen_fixture_reproduction: PASS
  byte_and_semantic_repeatability: PASS
  fixed_28_trial_distribution: PASS
  synthetic_machine_control: FAIL
  x_c14_01: REVIEW_REQUIRED
  x_c14_02: REVIEW_REQUIRED
  real_identity_authorization_revocation_runtime: NOT_RUN
  overall_practice_gate: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  editor_gate: NOT_REVIEWED
  chief_editor_gate: NOT_REVIEWED
  release_candidate_authorized: false
```

## 9. 安全边界与验证

作者 runner 与独立复跑均无网络、无真实凭证、无真实收件人、无资金、无删除、无生产写。所有负向突变仅在临时目录执行；这允许评价离线规则控制，不能证明 OpenClaw、Hermes、Muse、真实授权服务、身份图、撤销传播或 break-glass 已验证。

完成记录后运行 YAML/frontmatter 解析、`py_compile`、本地链接检查、formal/book validator 与两份新增文件的限定 diff check。任何全书并发文件告警只记录，不据此批准 C14。

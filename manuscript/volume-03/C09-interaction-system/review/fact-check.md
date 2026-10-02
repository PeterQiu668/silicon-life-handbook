---
review_id: C09-independent-fact-check-20260930
chapter_id: C09
review_type: independent-fact-check
reviewed_on: "2026-09-30"
reviewer_role: evidence-reviewer
chapter_status: drafting
fact_gate: passed_with_limitations
cross_gate: separate_record
practice_gate: not_reviewed
editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C09 独立事实核查

## 1. 结论

C09 的 14 条 evidence claim 与正文引用全部闭合。OpenClaw 与 Hermes 的固定 release/tag/commit 可由官方一手页面和 Git tag 对象复核；A2A 的对象分离同时有 `v1.0.1` 标签内固定规范与核验日动态规范支持；Muse 的 Goals、Activity、Artifacts、permissions 与关键批准全部保持为 `VENDOR-CLAIM`。事实门结论为 **`PASS WITH LIMITATIONS`**。

该结论只说明书稿在声明范围内没有把方法论、固定版本事实、动态页面、厂商自述和本地合成记录混写。它不证明目标 OpenClaw/Hermes 部署行为，不证明 Muse 内部实现，不执行两项练习，也不关闭真实数据权利、Provider 缓存、目标环境读回或独立实践门。章节继续为 `drafting`，不得据此晋级 `release_candidate`。

## 2. 核查口径

- `VERSION-FACT` 必须绑定可复核的 release/tag/commit 或固定提交文档；
- `OFFICIAL-SPEC` 必须区分固定版本规范与会继续变化的 `latest` 页面；
- `VENDOR-CLAIM` 只证明厂商公开叙述存在，不证明内部状态机、安全效果或数据路径；
- `METHODOLOGY` 可以综合协议、隐私框架和上下游章形成，但不得冒充外部正式标准；
- `LOCAL-VALIDATION` 本轮只核对作者既有静态合成记录，不执行、不修改，也不替代独立实践；
- `OPEN-QUESTION` 必须保留为限制，不得因链接可访问而升级为事实。

## 3. 14 条 claim 逐项结论

| ID | 身份 | 结论 | 核查摘要 |
| --- | --- | --- | --- |
| E-C09-001 | METHODOLOGY | PASS | 任务卡—上下文包—检查点—三证—受控反馈与 v2、章节卡、C09 preflight 一致；没有冒充平台原生标准。 |
| E-C09-002 | METHODOLOGY | PASS WITH LIMITATION | 四轴状态及环境终态是本书方法；A2A 只支撑 Task/Message/Artifact 等对象分离。已补 `v1.0.1` 固定规范，`latest` 仅作核验日交叉检查。 |
| E-C09-003 | OFFICIAL-SPEC | PASS | A2A `v1.0.1` 固定规范明确 Task、TaskState、Message、Artifact 分离，且 Artifact 表示 task outputs；协议 `completed` 仍不能外推业务验收。 |
| E-C09-004 | VERSION-FACT | PASS | OpenClaw release 页面和 annotated tag 均指向 `eb377ac59e6c9fd6c7705028034812becf00271b`。 |
| E-C09-005 | VERSION-FACT | PASS | 固定 `session.md` 支持 Gateway 按来源路由、群组/房间/Hook 隔离和 DM scope 管理；正文同时避免把 Session 写成任务、权限或终态。 |
| E-C09-006 | VERSION-FACT | PASS | 固定 `queue.md` 支持 session-key lane、`steer/followup/collect/interrupt`；正文没有把排队、回复或 run 结束写成业务完成。 |
| E-C09-007 | VERSION-FACT | PASS | Hermes release 页面与 annotated tag 共同确认 `v2026.8.13` / v0.20.1 指向 `f80f453ae0679347e38abc917c7f94f717bf96c5`；真实安装仍属实践门。 |
| E-C09-008 | VERSION-FACT | PASS | 固定 architecture/sessions 文档支持 Gateway dispatch、SQLite/FTS5 session persistence、source/platform 标记与隔离；不支持“持久化即正确/获权/完成”的外推。 |
| E-C09-009 | VERSION-FACT | PASS | 固定 Kanban/Deliverable 文档支持任务状态、review、Artifact 附件和向消息渠道投递；缺文件可被跳过等事实进一步说明通知不能代替终态。 |
| E-C09-010 | VENDOR-CLAIM | PASS WITH LIMITATION | Meta 公开材料确实描述 Goals、activity log、permissions、structured approval cards 与 Artifacts；来源同属厂商体系，正文没有推断内部 Schema、grader 或训练回流。 |
| E-C09-011 | METHODOLOGY | PASS WITH LIMITATION | 用途许可、最小化、去标识和权利治理与 NIST Privacy Framework 方向一致；去重、留出污染与训练准入主要由 C07/C08 和本书方法支持，不得写成 NIST 逐字段标准。 |
| E-C09-012 | LOCAL-VALIDATION | PASS IN DECLARED SCOPE | 既有静态记录内部确含 baseline PASS、UI 假完成 FAIL、过期未消费 REVIEW_REQUIRED、跨客户已消费 FAIL、群聊污染 FAIL；本轮未复跑，不能关闭 P0-07。 |
| E-C09-013 | EDITORIAL-DECISION / METHODOLOGY | PASS | D19 与术语表确认 `AU-L0—AU-L4`、`MAT-L0—MAT-L5` 两套独立命名空间；正文未授级、未互推、未由等级生成权限。 |
| E-C09-014 | OPEN-QUESTION | PASS AS DISCLOSURE | 真实 Runtime、真实目标环境、真实数据权利与第二位独立实践者仍未完成；正文、作者自检和运行记录披露一致。 |

## 4. 平台与协议边界

### 4.1 OpenClaw 固定版

- release：`v2026.9.6`；annotated tag target：`eb377ac59e6c9fd6c7705028034812becf00271b`；
- 固定 `session.md` 和 `queue.md` 可支持 session/run/message/queue 的实现映射；
- 固定文档不能证明具体部署已启用相同 scope、身份、审计或环境读回；
- 本章正确把 task card、authorization、Artifact、environment terminal 与 Session/Queue 分开。

结论：`PASS WITH PRACTICE LIMITATION`。

### 4.2 Hermes 固定版

- release：v0.20.1；tag：`v2026.8.13`；annotated tag target：`f80f453ae0679347e38abc917c7f94f717bf96c5`；
- 具体陈述均落在固定提交的 architecture、sessions、Kanban 与 Deliverable 文档；
- 正文没有用当前动态官网倒推固定 release，也没有伪造 OpenClaw 字段或 A2A 同构；
- 真实安装、目标 gateway、渠道投递和外部终态仍未实践。

结论：`PASS WITH PRACTICE LIMITATION`。

### 4.3 A2A

- `v1.0.1` 标签内 `docs/specification.md` 明确区分 Task、TaskState、Message 与 Artifact，并说明 Artifacts represent task outputs；
- `latest/specification` 在 2026-09-30 可访问且同样支持上述对象分离，但未来会漂移；
- C09 只借 A2A 校准对象分离，没有把任务卡冒充 A2A Task，也没有把协议终态冒充业务验收。

结论：`PASS WITH RECHECK TRIGGER`。印前应优先保留固定 `v1.0.1` 锚点，再复核 `latest` 是否仍为同一大版本语义。

### 4.4 Muse

两个 Meta 页面足以支持“厂商公开界面叙述”：Goals、activity log、permissions、approval cards、Artifacts。它们不能支持内部状态机、训练数据流、安全独立效果或环境终态主张。正文和账本均已限制为 `VENDOR-CLAIM`。

结论：`PASS WITH VENDOR LIMITATION`。

## 5. 完成性、错误状态与污染主张

事实核查确认正文没有用 UI 成功掩盖低层失败：

1. 技术执行结果落在过程/工具/策略事件；
2. 交付可见性落在消息状态、Artifact 存在/版本/完整性及接收端可用；
3. 业务与环境验收落在独立读回、回执、对账、监控或有权主体确认；
4. `HTTP 200`、工具 success、绿色 toast、`done`、通知送出和协议 `completed` 均不单独推出任务 PASS；
5. 过期上下文若执行前发现且未消费为 `REVIEW_REQUIRED`，跨主体敏感内容、完整群聊、留出答案或未授权内容一旦被消费/回流则为硬 `FAIL`；
6. `UNKNOWN` 只能是原始观察，最终门禁映射为 `REVIEW_REQUIRED`。

这些结论主要是本书方法论与 D21 的应用，不是某个平台安全效果证明。

## 6. 本轮明确修补

1. 为 E-C09-002/003 增加 A2A `v1.0.1` 标签内固定规范来源，保留 `latest` 为动态交叉检查；
2. 独立核验 OpenClaw annotated tag 指向 `eb377ac...`；OpenClaw 账本原有 release 页面已明确列出 release SHA，无需改写正文；
3. 独立核验 Hermes annotated tag 指向 `f80f453...`，同步修补正文、账本限制和开放问题状态；
4. 账本升为 `0.1.1`，记录独立事实 reviewer；章节继续 `drafting / unapproved`；
5. 未修改作者练习、静态运行记录、实践结论或任何平台配置。

## 7. 保留未知项

| 项 | 状态 | 关闭责任 |
| --- | --- | --- |
| 目标 OpenClaw deployment 的 session/queue/identity/telemetry 与 task/run/artifact 关联 | REVIEW_REQUIRED | 独立实践评审者 |
| Hermes 真实安装、Gateway/Kanban/Deliverable 渠道行为和目标环境对账 | REVIEW_REQUIRED | 独立实践评审者 |
| Muse 内部状态、训练回流、数据路径、审计导出与安全效果 | UNKNOWN / VENDOR-CLAIM | 授权产品核验与独立审计 |
| 真实反馈许可、数据权利、删除证明和 Provider 缓存 | REVIEW_REQUIRED | data/security owner 与 C10/C19/C21 |
| 第二位独立执行者对两项练习的复跑 | REVIEW_REQUIRED | 独立实践门 |

## 8. 外链、账本与机械核查

```text
Evidence claims: 14
Unique chapter refs: 14
Missing refs: 0
Orphan claims: 0
Sources: 30
External URLs: 17/17 HTTP 200
Local source paths: all present
OpenClaw annotated tag target: eb377ac59e6c9fd6c7705028034812becf00271b
Hermes annotated tag target: f80f453ae0679347e38abc917c7f94f717bf96c5
A2A pinned specification: v1.0.1/docs/specification.md present
Independent practice performed: no
Practice records modified: no
```

## 9. 事实门决定

```yaml
fact_gate:
  chapter_id: C09
  verdict: PASS_WITH_LIMITATIONS
  claims_checked: 14
  claim_reference_closure: PASS
  external_links_checked: 17
  platform_boundaries:
    openclaw_fixed: PASS
    hermes_fixed: PASS
    a2a_fixed_and_dynamic: PASS_WITH_RECHECK_TRIGGER
    muse_vendor_claim: PASS_WITH_LIMITATIONS
  independent_practice_performed: false
  practice_approved: false
  editor_approved: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

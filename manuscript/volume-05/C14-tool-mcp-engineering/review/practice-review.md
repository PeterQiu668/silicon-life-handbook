---
review_id: C11-independent-practice-review-20260930
chapter_id: C11
review_type: independent-practice-gate
reviewed_on: "2026-09-30"
reviewer: "non-author-practice-reviewer:legacy_mapping"
independent_from_author: true
chapter_status_after_review: drafting
fresh_copy_reproduction: PASS
x_c11_01: PASS_IN_DETERMINISTIC_ROUTING_SCOPE_REVIEW_REQUIRED_FOR_STATEFUL_EXECUTION
x_c11_02: REVIEW_REQUIRED_MISSING_EXECUTABLE_SECURITY_FIXTURES
p0_05: REVIEW_REQUIRED
p0_06: REVIEW_REQUIRED
p0_07: PASS_IN_ROUTING_EVIDENCE_SCOPE_REVIEW_REQUIRED_FOR_FULL_PRACTICE_GATE
overall_practice_gate: REVIEW_REQUIRED
fact_gate: separate_record
cross_gate: separate_record
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
self_approval: false
release_candidate_authorized: false
---

# C11 独立实践门

## 1. 裁决

**作者 `run-tool-contract.py` 对固定输入的确定性路由结果已由非作者在两个 fresh temp 副本中独立复现：18 个 trial、12 PASS、4 FAIL、2 REVIEW_REQUIRED，源文件、结果和摘要的字节哈希以及解析后语义全部一致。该结果足以证明作者记录没有汇总漂移，但不足以证明两项练习已经完整执行。C11 总实践门为 `REVIEW_REQUIRED`。**

X-C11-01 在“确定性合同判定路由”范围内通过，但 mailbox、幂等存储、独立环境 read-back、commit/cancel/compensation 生命周期均未真实执行，因此保留状态化执行复核。X-C11-02 不通过完整实践门：SSRF 与 token passthrough 只是预置标签路由；shadowing、rug pull、stdio/path 越界没有可执行夹具。

结构化记录见 [independent-practice-reproduction-20260930.yaml](runs/independent-practice-reproduction-20260930.yaml)。本评审没有修改作者 runner、input、result、summary、正文、ledger、三件母产物或两项练习，也不批准编辑门、总编门或 RC。

## 2. 独立性与安全边界

- 本评审者不是 C11 作者，本轮只承担独立实践复现；事实门和交叉门沿用各自独立记录。
- 原样复跑只把 `run-tool-contract.py` 与 `synthetic-tool-input.yaml` 复制到两个不同 fresh temp 目录；所有生成文件留在临时目录并自动删除。
- 额外缺口探针只修改第三个临时目录内的输入副本，用于验证 runner 是否自行识别 SSRF、token passthrough、shadowing、rug pull 和 stdio/path 越界；作者输入未被修改。
- 全程无网络、真实 MCP Server、OAuth、账号、凭证、秘密、客户数据、外发、生产状态或破坏性动作。
- 输出为空 stdout/stderr；证据对象是生成的 result/summary 文件、哈希、解析结果与临时探针结论。

## 3. 两个 fresh-copy 原样复跑

| 项目 | RUN-A | RUN-B | 结论 |
| --- | --- | --- | --- |
| 临时目录 | `c11-practice-a-7r_ucq5l` | `c11-practice-b-omc5e7u_` | 两个不同 fresh 目录，运行后自动删除 |
| 退出码 | 0 | 0 | PASS |
| runner SHA-256 | `1175db4c…71f04` | `1175db4c…71f04` | 字节相同 |
| input 原始 SHA-256 | `633fca5a…cf21c` | `633fca5a…cf21c` | 字节相同 |
| result SHA-256 | `cf927f93…0245` | `cf927f93…0245` | 字节相同，且等于作者结果 |
| summary SHA-256 | `84b91608…74f8` | `84b91608…74f8` | 字节相同，且等于作者摘要 |
| 解析后结果 | 相同 | 相同 | 语义相同 |

输入文件原始字节哈希是 `633f…`；runner 将解析后的 JSON 对象规范化计算出的内容哈希是 `78f35182…1073`。两者度量对象不同，不能混写。作者原始结果与摘要在复跑后仍保持同一哈希。

## 4. 18 个 trial 的完整性

| 检查 | 结果 | 裁决 |
| --- | --- | --- |
| trial 数量 | 18 | PASS |
| trial ID 唯一性 | T01—T18，18/18 唯一 | PASS |
| 三个案例 | CASE-A、CASE-B、CASE-C | PASS |
| 五类场景 | normal、boundary、adversarial、exception、recovery | PASS |
| 门禁分布 | 12 PASS、4 FAIL、2 REVIEW_REQUIRED | PASS |
| 原始 UNKNOWN | T16、T18 均映射 REVIEW_REQUIRED | PASS |
| 危险请求被安全拒绝 | deny/blocked/schema_error 且 unchanged 的记录均判 PASS | PASS |
| 三件母产物 | A-C11-01、A-C11-02、A-C11-03，恰好三件 | PASS |

正确拒绝是一种能力 PASS，不等于危险动作成功。T02、T03、T04、T06、T08、T13 的 PASS 表示固定夹具声称请求被拒绝且终态未变；其中 T04/T13 是否拥有足够真实的安全夹具，仍需按第 6 节降级理解。

## 5. 非补偿硬失败

| Trial | 观察 | 硬失败 | 复跑裁决 |
| --- | --- | --- | --- |
| T10 | `two_messages`、重试改幂等键、终态 diverged | duplicate side effect；idempotency key changed | FAIL |
| T11 | commit 后 cancel、终态 diverged、补偿未运行 | cancel treated as rollback | FAIL |
| T14 | 恶意 description、Approval 无效仍发生发送、协议 complete、终态 diverged | malicious description；approval bypass；wrong terminal | FAIL |
| T15 | canary exfiltration attempt、协议 complete、终态 diverged | secret exfiltration；wrong terminal | FAIL |

以上四个 trial 即使同一批次存在 12 个 PASS，也仍保持 FAIL；没有平均分、成本或功能成功抵消。T12 的补偿/恢复 PASS 也不删除 T11 失败，T17 的对账恢复 PASS 不将 T16 的 UNKNOWN 追溯改写为成功。

## 6. X-C11-02 可执行夹具审计

“正文列出攻击面”“输入包含一个布尔字段”和“runner 真正执行安全边界”是三个不同证据等级。本轮逐项结论如下：

| 攻击面 | 作者输入/runner 实况 | 是否真正可执行 | 裁决 |
| --- | --- | --- | --- |
| 恶意 description + Approval bypass | T14 有字段，runner 执行组合硬门 | 只执行判定路由；无真实 Policy/Approval | ROUTING ONLY |
| 重复副作用 + 幂等键变化 | T10 有组合硬门 | 无 mailbox/去重存储，effect 与 readback 由输入预置 | ROUTING ONLY |
| cancel 假回滚 | T11 有组合硬门 | 无 commit/cancel/compensation 生命周期 | ROUTING ONLY |
| 秘密外泄 | T15 有硬门 | 无真实 canary、日志、文件或网络边界 | ROUTING ONLY |
| 错误环境终态 | T14/T15 有硬门 | readback 来自输入，不是独立环境查询 | ROUTING ONLY |
| SSRF | T04 有 link-local target 与 `ssrf_target=true` | 不解析 URL、DNS、重定向或逐跳地址 | REVIEW_REQUIRED |
| token passthrough | T13 有 `token_passthrough=true` | 无 token、issuer/audience、header、转发链或资源端 | REVIEW_REQUIRED |
| shadowing | 无对应 trial/字段处理 | 否 | MISSING |
| rug pull | 无批准前后 schema/description/binary/scope digest 变化 | 否 | MISSING |
| stdio/path 越界 | 无本地 Server、临时根、canary env/file、path traversal、子进程清理 | 否 | MISSING |

因此 X-C11-02 正文的红队清单不能冒充已执行实践。即使 T04、T13 被路由为安全 PASS，也只能证明 runner 在收到作者预置的“已阻断且 unchanged”结论时如何记分。

## 7. 临时缺口探针

为验证上述判断，本评审在第三个自动删除的临时副本中运行三个负向探针：

1. 保留 T04 的 `http://169.254.169.254/meta`，将 `ssrf_target` 改为 false，并预置 `complete/expected`；runner 判 PASS，证明它不从 target 自行识别 SSRF。
2. 将 T13 的 `token_passthrough` 改为 false、`audience_valid` 改为 true，并预置 `complete/expected`；runner 判 PASS，证明它不执行 token 流。
3. 给 T01 加入 `shadowing=true`、`rug_pull=true`、`stdio_path=../synthetic-canary`；runner 仍判 PASS，证明三个字段没有实现路径。

探针结果哈希为 `2a4a5625…db0`，只用于证明覆盖缺口；它不替代作者原样复跑，也没有改作者输入。

## 8. X-C11-01 裁决

**裁决：`PASS_IN_DETERMINISTIC_ROUTING_SCOPE_REVIEW_REQUIRED_FOR_STATEFUL_EXECUTION`。**

通过部分：固定合同快照、18 条输入、三态映射、硬门、UNKNOWN、安全拒绝、失败分布和摘要均可确定性复现；两个 fresh copy 与作者结果逐字节一致。

未关闭部分：练习要求的 fixture store、mailbox、相同幂等键持久去重、commit 后 receipt 丢失再查询、dispatch/执行中/commit 后三类 cancel、补偿 residual、独立环境 read-back 并未由 runner 执行。当前 `effect`、`receipt`、`readback`、`compensation` 是输入声明，不是从状态机观察得到。因此不能将“判分器可运行”写成“工具合同练习完整跑通”。

## 9. X-C11-02 裁决

**裁决：`REVIEW_REQUIRED_MISSING_EXECUTABLE_SECURITY_FIXTURES`。**

作者 runner 正确保留恶意 description/Approval bypass、重复副作用、幂等键变化、cancel 假回滚、秘密外泄和错误终态的非补偿 FAIL 路由。但 X-C11-02 明确要求的 SSRF、token passthrough、shadowing、rug pull、stdio/path 越界没有形成完整可执行夹具，其中后三项完全缺失。需要在无网络、无真实秘密的沙箱内补充可观察的模拟 Host/Client/Server、URI 每跳校验、假 token 转发链、命名空间冲突、快照变更失效、临时根和 canary 清理，才可重审。

## 10. P0-05 / P0-06 / P0-07

| P0 | 本轮裁决 | 已有证据 | 未关闭项 |
| --- | --- | --- | --- |
| P0-05 操作可执行、可停止、可回滚 | REVIEW_REQUIRED | runner 可执行；cancel/补偿路由可重复 | 状态化 effect、stop、真实 read-back、rollback/residual 未执行 |
| P0-06 系统权限、审批和隔离 | REVIEW_REQUIRED | 越权标签与硬门存在；安全拒绝记 PASS | Policy/Approval/OAuth/audience/Sandbox/stdio/path 没有强制层夹具 |
| P0-07 基线、证据和客观验收 | PASS_IN_ROUTING_EVIDENCE_SCOPE；完整门 REVIEW_REQUIRED | 固定输入、双 fresh copy、哈希、18 条分布、三态、失败尾部齐全 | X02 关键夹具缺失；环境终态为输入字段，不是独立观察 |

没有发现“作者汇总造假”或“硬失败被平均掉”的 P0 FAIL；阻断来自证据能力不足，故使用 REVIEW_REQUIRED，而不是把未知写成失败或通过。

## 11. 真实环境边界与关闭条件

本轮没有运行真实 MCP/OAuth、OpenClaw、Hermes 或 Muse，也没有任何真实外部环境。Muse 只能维持厂商公开声明边界。若要关闭实践门，至少需要：

1. 先在离线安全沙箱补齐 X-C11-01 状态机和 X-C11-02 五类缺失/标签化夹具；
2. 保存执行前后状态、真实生成的 receipt/read-back、停止点、补偿 residual 和清理证明；
3. 在获权隔离实例分别验证 OpenClaw 固定版本与 Hermes 对照实现的 Policy/Approval/Sandbox/MCP 行为；
4. OAuth 只用专用假 issuer/resource 与短期测试 token，不接触生产身份；
5. 真实平台结果不得外推 Muse 内部实现，也不得将协议兼容写成业务授权或安全认证。

## 12. 总实践门

```yaml
practice_gate:
  chapter_id: C11
  fresh_copy_reproduction: PASS
  trial_count_and_distribution: PASS
  unique_ids_cases_scenarios: PASS
  unknown_mapping: PASS
  safe_denial_semantics: PASS
  hard_failure_non_compensation: PASS
  x_c11_01: PASS_IN_DETERMINISTIC_ROUTING_SCOPE_REVIEW_REQUIRED_FOR_STATEFUL_EXECUTION
  x_c11_02: REVIEW_REQUIRED_MISSING_EXECUTABLE_SECURITY_FIXTURES
  p0_05: REVIEW_REQUIRED
  p0_06: REVIEW_REQUIRED
  p0_07: PASS_IN_ROUTING_EVIDENCE_SCOPE_REVIEW_REQUIRED_FOR_FULL_PRACTICE_GATE
  real_mcp_oauth_and_platforms: NOT_RUN
  overall: REVIEW_REQUIRED
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

## 13. 验证记录

完成本评审后运行：

```bash
python3 scripts/validate-formal-manuscript.py
python3 scripts/validate-book.py
git diff --check -- .
```

并对 `practice-review.md` frontmatter、独立复跑 YAML、作者 input/result YAML 做解析；验证源/输出哈希绑定、18 个 trial、ID 唯一性、三个案例、五类场景、门禁分布、硬失败集合和限定 diff。

最终结果：

- YAML/frontmatter、四个作者源/输出哈希绑定、trial 完整性和三件母产物计数：PASS。
- `validate-formal-manuscript.py`：PASS；仅有未来 12 个章节包尚未完成的预期 warning。本次 C12 已达到结构与篇幅门，没有并发暂态 error。
- `validate-book.py`：PASS；扫描 268 个 Markdown，检查 1,296 条本地链接。
- `git diff --check -- .`：PASS；两个新增文件的限定 `--check` 无 whitespace error（`--no-index` 因文件为新增而返回差异状态 1，输出为空）。

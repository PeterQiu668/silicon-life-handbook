---
review_id: C16-fact-cross-remediation-review-20260930
chapter_id: C16
review_type: independent-post-fix-fact-and-cross-review
reviewer_role: non-author-fact-and-cross-reviewer
verified_on: "2026-09-30"
chapter_status: drafting
fact_gate: PASS
fact_gate_limitations: true
cross_gate: PASS
cross_gate_limitations: true
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C16 事实/交叉修补后独立复核

## 最终裁决

**事实门：`PASS WITH LIMITATIONS`。交叉门：`PASS WITH LIMITATIONS`。** 前次 [事实审校](fact-check.md) 的两项 P0、A2A 固定身份改进，以及 [交叉审校](cross-review.md) 的 D22 谱系阻塞均已按关闭合同修复；15 task / 45 unique trial 的措辞与 A-C16-03 的真实层显式计数也已闭合。fresh-temp 双复现与五类定向负突变全部符合预期。

这里的 `PASS` 只关闭事实引用、固定版本字段、跨章数据谱系和离线 runner 的拒绝合同。真实 OpenClaw/Hermes/Muse/A2A、代表性真实任务和两项练习的独立实践仍未执行；本记录不签实践、编辑、总编或 `release_candidate`。

复现的机器可解析记录见 [fact-cross-remediation-reproduction.yaml](fact-cross-remediation-reproduction.yaml)。本轮未修改 [正文](../chapter.md)、[证据账本](../evidence-ledger.yaml)、母产物、练习、作者自检或作者 runs。

## 六项定向复核

### 1. OpenClaw 固定字段：PASS

作者包中的规范表述已改为：

```text
agents.entries.*.subagents.allowAgents
```

对正文、ledger、三件母产物、两项练习、作者自检和运行说明做限定扫描，旧值 `agents.list[].subagents.allowAgents` 为 0 处，新值在正文出现 1 处。该字段与 OpenClaw `v2026.9.6 / eb377ac…` 的固定 subagent 文档一致。前次 `P0-F16-01 / P0-04` 关闭。

### 2. Muse `swarms/subagents` 证据：PASS

E-C16-016 仍保持 `VENDOR-CLAIM`，但 source `MUSE` 已从不支持该句的产品发布页换成 Meta AI Research 官方文章《How We Built Safety Into Muse》。该页明确写到 Muse 可启动 “swarms of subagents”，并描述 concurrent sub-agents 与 subagent handoffs；因此 claim、正文和来源语义闭合。

这仍只是 Meta 自述，不证明内部组织拓扑、权限继承、成本、停止、恢复或效果，正文没有越过该上限。前次 `P0-F16-02 / P0-03+P0-12` 关闭。

### 3. A2A 固定版本身份：PASS

账本 `A2A-1` 已固定为：

```text
https://a2a-protocol.org/v1.0.0/specification/
```

页面可达并明确属于 A2A 1.0.0 规范。正文继续用协议线 `A2A 1.0` 描述互操作边界，没有把 patch 号写成新的协议语义，也没有抢占 C18 的对象与信任定义权。前次 `P1-F16-03` 关闭。

### 4. D22 四层与合成影子：PASS

原先三个合成场景现均为 `holdout + synthetic_shadow + intended_target_layer=representative_real_world`：

| scenario | 当前 layer | shadow | intended target |
| --- | --- | --- | --- |
| multi-negative-benefit | holdout | true | representative_real_world |
| lead-lost | holdout | true | representative_real_world |
| a2a-runtime-unverified | holdout | true | representative_real_world |

输入中实际 `representative_real_world` scenario 为 0；结果保留空的规范真实层，并派生：

- `representative_real_world_executed: false`；
- `representative_real_world_trial_count: 0`；
- `synthetic_shadow_trial_count: 9`。

security/red-team 继续作为横切非补偿切片，没有变成第五层。前次 `P1-X16-01` 关闭。

### 5. Runner 拒绝合同与负突变：PASS

runner 不是只相信输入自报。独立临时副本验证了五类硬拒绝：

| Mutation | 期望 | 实际 |
| --- | --- | --- |
| synthetic 样本改标真实层 | hard fail | `synthetic fixture cannot claim representative_real_world execution` |
| executed=true 但真实层 count=0 | hard fail | `representative_real_world_executed must be derived from actual layer records` |
| 声明真实来源并产生真实层记录，但缺 evidence ref | hard fail | `representative_real_world records require declared origin and evidence reference` |
| 重复原始 scenario id | hard fail | `scenario ids must be unique` |
| scenario id 原始值不同但归一化后生成重复 trial/task-trial ID | hard fail | `trial ids and task/trial pairs must be unique` |

因此 synthetic 冒充 real、executed/count/evidence 三类矛盾、重复 scenario 和重复派生 trial 均由代码拒绝，而非 README 口头约束。

### 6. 15 task / 45 trial 与母产物：PASS

正文、E-C16-022、作者自检与运行摘要现一致表达：15 个任务场景，每项 3 次，共 45 个唯一 `trial_id`。保存结果实际为：

- `unique_task_count: 15`；
- `run_count: 45`；
- `unique_trial_ids: true`；
- 12 PASS、27 FAIL、6 REVIEW_REQUIRED；
- 外部副作用为 0。

A-C16-03 已显式写入 `representative_real_world_evidence_count: 0`，并规定该值为 0 时合成 PASS 不得外推生产。前次 `P2-F16-04` 与 `P2-X16-02` 关闭。

## Fresh-temp 双复现

将当前作者 runner 与 input 分别复制到两个全新的临时目录运行：

- 两次退出码均为 0；
- fresh A 与 fresh B 的 results/summary 字节一致；
- fresh 与作者保存的 results/summary 字节一致；
- results SHA-256：`c0194dd7d6c76d5d9ab848eea0d4dc28fe2bb9136548b5631575d4fd84e43035`；
- summary SHA-256：`629ee568ffde5b97b00e9e9a79c6f1c59d6ce8480bf431bc1e11c9fc2e24a57a`。

这项复现只证明当前离线夹具的确定性、计数和拒绝合同，不替代两项正式练习的独立实践复现。

## 前次问题关闭表

| Issue | 前次状态 | 本次状态 | 关闭证据 |
| --- | --- | --- | --- |
| P0-F16-01 | REVIEW_REQUIRED | CLOSED | 固定字段改为 `agents.entries.*...`，旧字段限定扫描为0。 |
| P0-F16-02 | REVIEW_REQUIRED | CLOSED | E-C16-016 绑定 Meta 官方安全文章，原文直接支持 swarms/subagents。 |
| P1-F16-03 | OPEN | CLOSED | A2A URL 固定为 `/v1.0.0/specification/`。 |
| P1-X16-01 | REVIEW_REQUIRED | CLOSED | 三场景改为 holdout shadow；真实层显式0；runner具备谱系硬拒绝。 |
| P2-F16-04 | OPEN | CLOSED | 15 task / 45 unique trial_id 在正文、ledger、自检和结果一致。 |
| P2-X16-02 | OPEN | CLOSED | A-C16-03 显式 `real_world_evidence_count=0`。 |

## 保留限制

以下不是本轮事实/交叉缺陷，也没有被合成复现关闭：

1. 真实 OpenClaw 多 Agent 身份、凭证、Sandbox、停止和取消传播未运行。
2. Hermes 固定版 profile/subagent 继承与动态文档映射未做目标环境实测。
3. Muse 内部组织效果、成本和恢复机制仍只有厂商材料，不能独立验证。
4. A2A 真实互操作、Agent Card、任务生命周期和环境终态未运行。
5. `representative_real_world_evidence_count` 仍为 0，真实任务长期净收益不能宣称。
6. X-C16-01/02 尚未由独立实践 reviewer 执行；P0-07 只能由实践门裁决。

## 门禁声明

基于本轮限定范围，前次事实与交叉阻塞项全部关闭：`fact_gate=PASS`、`cross_gate=PASS`，均带上述真实平台与实践限制。章节继续保持 `drafting / unapproved`；本记录不批准实践、编辑、总编或 `release_candidate`。

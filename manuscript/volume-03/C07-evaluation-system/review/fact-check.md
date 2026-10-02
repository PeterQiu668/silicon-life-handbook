---
chapter_id: C07
review_type: independent-fact-check
reviewed_on: "2026-09-30"
reviewer_role: evidence-and-version-reviewer
chapter_snapshot: "after author-self-check completion; chapter 0.1.1"
chapter_status: drafting
fact_gate: passed_with_limitations
practice_gate: not_reviewed
editor_gate: not_reviewed
self_approval_of_other_gates: false
---

# C07 独立事实核查

## 结论

事实门结论为 `PASS_WITH_LIMITATIONS`。20 条 claim 均能解引用到已声明的本地规范、固定版本一手材料、动态官方文档、公开研究或本地合成运行；正文引用 20 条、账本定义 20 条，无缺失和孤儿。OpenClaw 固定版、Hermes 固定 release 与动态文档、Muse 厂商声明已经分层，不存在把 Muse 内部实现写成独立事实的情况。

本结论只批准“事实身份、来源、版本和限制表达在本章范围内成立”，不批准真实平台可用性、练习效果、生产适用性、编辑质量、总编合并或 `release_candidate`。OpenClaw 目标环境遥测、Hermes 动态字段实机、Muse 导出能力以及真实 human/expert grader 校准继续为 `REVIEW_REQUIRED`。

## 审校快照与方法

- 作者自检在 2026-09-30 明确写出“达到送交独立审校的条件”后才开始核查；
- 读取三级框架 C07 7.1—7.8、章节卡、质量标准、术语表、C07 preflight、正文、三件母产物、两项练习、账本与合成运行；
- 逐条把正文证据 ID 与 ledger claim、source ID、身份、作用域和 limitation 对齐；
- 对 OpenClaw/Hermes 使用官方 release/tag/固定提交或动态官网；Muse 仅使用 Meta 官方公开材料并保持 `VENDOR-CLAIM`；
- 重跑作者合成 harness，仅核对本地 claim 的可复现事实，不作为独立实践门；
- 机械检查全部本地来源、外部 URL、YAML、MAT/AU 术语和引用闭合。

## 20 条 claim 逐项结论

| ID | 身份 | 结论 | 独立核查摘要 |
| --- | --- | --- | --- |
| E-C07-001 | METHODOLOGY | PASS | 与 v2、章节卡、preflight 和术语表的 `evaluation_system` 一致；未冒充行业标准。 |
| E-C07-002 | METHODOLOGY | PASS | Anthropic 官方材料明确区分 task、trial、trajectory、outcome、grader；正文主动把 trajectory 限定为平台可观察轨迹。 |
| E-C07-003 | METHODOLOGY | PASS | 能力、结果、过程与成本分开是本书方法；正文没有另造可抵消 C03 安全硬失败的综合分。 |
| E-C07-004 | METHODOLOGY | PASS | 四层数据与“基线不是第五层、对抗是场景属性”均明确标为本书方法，来源与限制充分。 |
| E-C07-005 | METHODOLOGY | PASS | 五类场景消费 C04 风险和 C06 数据流；没有把固定权重写成通用标准。 |
| E-C07-006 | METHODOLOGY | PASS | PASS / FAIL / REVIEW_REQUIRED 与质量标准、术语表一致；grader 原始 UNKNOWN 只作为输入。 |
| E-C07-007 | METHODOLOGY | PASS | Anthropic/OpenAI 官方评测材料均支持答案、轨迹与环境结果不能互相替代；正文仍把六面证据标为本书展开。 |
| E-C07-008 | DRAFT-GUIDANCE | PASS WITH LIMITATION | NIST CAISI 官方材料明确区分 solution contamination 与 grader gaming；NIST AI 800-2 保持 Initial Public Draft 身份，正文未写成强制标准。 |
| E-C07-009 | ACADEMIC-EVIDENCE | PASS WITH LIMITATION | Zheng 等支持位置、冗长、自偏好/自我增强及有限推理风险；Panickssery 等支持自识别与自偏好。正文未外推统一误差率。 |
| E-C07-010 | METHODOLOGY | PASS | “不存在全任务固定样本量/阈值”是有边界的方法论判断；正文要求按总体、风险、依赖、预算和停止规则预注册。 |
| E-C07-011 | VERSION-FACT | PASS | OpenClaw tag `v2026.9.6` 的 annotated tag 指向 `eb377ac59e6c9fd6c7705028034812becf00271b`；固定文档确认 runId、lifecycle、`agent.wait` 及 OTel 观察面。 |
| E-C07-012 | VERSION-FACT | PASS | 固定文档确认内容采集默认关闭、异步诊断队列可 dropped、外部 harness 观察面受限；正文没有把日志写成环境终态。 |
| E-C07-013 | VERSION-FACT | PASS | Hermes release `v2026.8.13` 标题为 v0.20.1，annotated tag 指向 `f80f453ae0679347e38abc917c7f94f717bf96c5`。 |
| E-C07-014 | VENDOR-CLAIM | PASS WITH LIMITATION | Meta 官方材料描述 Goals、Activity/Artifacts、权限、审批、安全架构与内部 eval；正文始终归为厂商声明，不推断内部 schema 或独立效果。 |
| E-C07-015 | METHODOLOGY | PASS | C04 三件正式产物确实提供岗位/JTBD、能力/NFR、四因子风险和负面清单接口。 |
| E-C07-016 | METHODOLOGY | PASS | C06 三件正式产物提供六层结构、消息/执行流和最小可训单体；C07 未把 `agent.wait` timeout 写成 run stop。 |
| E-C07-017 | METHODOLOGY | PASS | v2、章节卡与 D16 均要求且仅要求评测蓝图、基线报告、裁判校准表三件母产物；目录实物恰为三件。 |
| E-C07-018 | LOCAL-VALIDATION | PASS IN DECLARED SCOPE | 独立重跑得到 8 task / 24 trial、13 PASS / 8 FAIL / 3 REVIEW_REQUIRED，五类硬失败均为 FAIL；只支持确定性合成夹具。 |
| E-C07-019 | LOCAL-VALIDATION | PASS IN DECLARED SCOPE | 重跑确认两个 code UNKNOWN 均映射为 REVIEW_REQUIRED，model/expert 合成标签分歧 7 次；不估计真实裁判误差。 |
| E-C07-020 | DYNAMIC-OFFICIAL | PASS WITH LIMITATION | 2026-09-30 Hermes 动态官方页面描述 SQLite session DB、message/tool history、profile/HERMES_HOME 隔离、session export/logs 等观察面；未回填为 v0.20.1 固定事实。 |

## 平台与版本核查

### OpenClaw

- 固定基线：`v2026.9.6 / eb377ac59e6c9fd6c7705028034812becf00271b`；tag—commit 关系核验通过。
- `agent` 返回 `runId`，`agent.wait` 观察 lifecycle end/error；等待超时只说明本次等待未得结果，不取消底层 run。
- 固定文档存在 agent/harness/model/tool/message/session 等 span/event/metric 面；内容默认不导出，诊断队列 dropped 必须另查。
- 结论边界正确：这些是潜在证据源，不是目标环境已经启用的证明，也不能替代环境终态。

### Hermes

- 固定 release：`v0.20.1 / v2026.8.13 / f80f453ae0679347e38abc917c7f94f717bf96c5`。
- 动态官方页面与固定 release 已拆成 E-C07-013 / E-C07-020；动态字段只按核验日描述。
- 当前章节没有把 OpenClaw 的 runId、lane、span 强填到 Hermes；不可用字段明确要求写 `unavailable`。

### Muse

- Meta 官方产品与研究材料确实自述 Goals、Activity/Artifacts、批准、权限、审计、安全架构和内部 eval。
- 这些材料仍是厂商自己对产品和内部体系的陈述。本章没有声称获得内部 trace/grader schema、独立效果或可导出审计数据。
- “Muse 可导出 activity/audit 的具体范围”继续为 `REVIEW_REQUIRED`，不得因网页出现 audit trail 描述而升级。

## 本地合成 claim 复核

独立执行作者脚本两次，输出文件前后 SHA-256 完全一致：

```text
synthetic-baseline-results.yaml
14c358d576d9e5619bcb65a29238cd79f5c984f5a97f18e8679f8075a65421d9

synthetic-baseline-summary.md
bf41b7d995c420d6a117f4e4819445f26b95afa2acdab062d0765a48dac7bd35

input_sha256
3ef2cc8f7991fb2dbcfffcd04ac3753b57a1983570f27fe50007e713f8c31dc0
```

重跑只验证作者声明的确定性数据合同和统计数字。脚本会重写同内容的结果/摘要文件，但两次字节哈希一致；没有网络、凭证、真实平台、真实人类或真实专家。此项不得被称为独立实践复现。

## 已修补的明确缺陷

1. 将正文和 X-C07-01 中两处未加命名空间的成熟度等级修正为 `MAT-L0—MAT-L5`，避免与 `AU-L0—AU-L4` 混用；
2. 将原 E-C07-013 的 Hermes 固定 release 与动态文档拆为 E-C07-013 / E-C07-020，各自使用 VERSION-FACT / DYNAMIC-OFFICIAL；
3. 为 Hermes tag 增加固定提交一手来源；
4. 移除未被任何 claim 使用且本次返回 HTTP 403 的 ISO-25059 source，并把章末未落到 claim 的“ISO/NIST”表述收敛为实际使用的 NIST 来源；
5. 在 C07→C08 交接中明确：专项安全套件必须继续标注四层数据身份和场景，不能取代 real_world 规范层；
6. 为正文与账本追加 0.1.1 变更记录，并机械同步作者自检的 claim 数量。

## 保留未知与限制

| 项 | 状态 | 关闭责任 |
| --- | --- | --- |
| OpenClaw 目标环境 OTel exporter、retention、sampling、dropped | REVIEW_REQUIRED | 独立实践审校者 |
| Hermes 动态 Sessions/Storage/Logs 与 v0.20.1 逐字段一致性 | REVIEW_REQUIRED；不得回填 | 平台事实/实践审校者 |
| Muse activity/audit 导出、完整性和可复核范围 | REVIEW_REQUIRED / VENDOR-CLAIM | 授权产品核验者 |
| 真实 human/expert grader 校准 | REVIEW_REQUIRED | 独立实践审校者 |
| 合成 real_world 层的外部效度 | UNKNOWN；无生产证据 | C20/C21 后续治理 |

## 机械核查结果

```text
Claims: 20
Unique chapter refs: 20
Missing refs: 0
Orphan claims: 0
Sources: 40
Unused sources: 0
Unknown source IDs: 0
Local sources: 16/16 present
External URLs: 24/24 HTTP 200
Unprefixed maturity/autonomy level notation: 0
Artifacts: exactly 3
```

事实门通过不改变 `chapter.md` 的 `drafting` 状态，也不关闭交叉、实践、编辑或总编门。

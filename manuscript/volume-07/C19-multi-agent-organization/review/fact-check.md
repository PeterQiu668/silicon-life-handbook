---
review_id: C16-independent-fact-check-20260930
chapter_id: C16
review_type: independent-fact-and-version-review
reviewer_role: non-author-evidence-reviewer
verified_on: "2026-09-30"
chapter_status: drafting
fact_gate: REVIEW_REQUIRED
claims_checked: 25
claim_results: {PASS: 23, FAIL: 0, REVIEW_REQUIRED: 2}
practice_gate: not_reviewed
editor_gate: not_reviewed
chief_editor_gate: not_reviewed
release_candidate_authorized: false
---

# C16 独立事实核查

## 裁决

**事实门：`REVIEW_REQUIRED`。** 25 条账本主张均有唯一 ID、均被章节包引用，22 个 source 全部被使用；13 个本地来源可解引用，9 个外部端点均可读取或由浏览器核验。OpenClaw `v2026.9.6` 确认指向 `eb377ac…`，Hermes 固定提交确认对应 tag `v2026.8.13`，且固定源码中 package version 为 `0.20.1`；A2A 当前规范页明确最新正式版本为 `1.0.0`。

门未通过的原因不是平台效果未实跑——这些限制已经诚实保留为 `UNKNOWN/REVIEW_REQUIRED`——而是两个可定位的事实闭合缺陷：正文把 OpenClaw 固定版字段写成旧式 `agents.list[]`，以及 Muse 的账本来源不支持其所引用的 `swarms/subagents` 句子。它们分别触发质量标准 P0-04 与 P0-03/P0-12，在修复并独立回归前不能给事实门 `PASS`。

本审校没有修改 [正文](../chapter.md)、[证据账本](../evidence-ledger.yaml)、母产物、练习或作者运行包；也不执行独立实践门。逐源记录见 [source-audit-20260930.yaml](source-audit-20260930.yaml)。

## 核验方法与边界

- 解析 [evidence-ledger.yaml](../evidence-ledger.yaml)，核对 25 个 claim ID、22 个 source ID、正文/产物/练习双向引用和本地路径；结果为 25/25 双向闭合、22/22 used、0 unused、0 missing。
- 对固定 OpenClaw commit 的 multi-agent、channel-routing、subagents 文档逐项比对；另核验 tag `v2026.9.6` 的 annotated tag object 确实指向 `eb377ac…`。
- 对 Hermes 固定 commit、tag 与固定源码 version 字段交叉核验；动态官网只作为 2026-09-30 镜面，没有倒填固定版。
- 读取 A2A 规范的版本、对象、异步和授权边界；当前 `/latest/` 显示 `1.0.0`，同时记录动态别名的出版可追溯风险。
- 对 Meta 发布页全文检索 `swarm/subagent`，均无命中；另定位到 Meta 官方安全文章确有相关表述，但它不在本章 ledger，不能替当前引用自动补证。
- 将作者 runner 与 input 复制到两个 fresh temp 目录复跑，只核验 E-C16-022/023 的保存结果完整性；该步骤不签两项练习或实践门。

## 25 条 claim 逐项结论

| Evidence | 身份 | 结论 | 核验摘要 |
| --- | --- | --- | --- |
| E-C16-001 | METHODOLOGY | PASS | 本地规范与 OpenAI 官方指南均支持“先最小复杂度、额外组织有开销”；正文没有给普遍效果量。 |
| E-C16-002 | METHODOLOGY | PASS | 与术语、C04 岗位/任务域和 preflight 一致；任务拓扑先于角色贯穿 16.1—16.2。 |
| E-C16-003 | METHODOLOGY | PASS | 协作税保持向量，不把 token 当全部成本；与 C03 公平比较边界一致。 |
| E-C16-004 | METHODOLOGY | PASS | OpenAI 指南明确建议先最大化单 Agent，并在确定性方案足够时不升级；正文限定为工程纪律而非绝对规律。 |
| E-C16-005 | METHODOLOGY | PASS | 六模式被写成情境结构，正文明确不是成熟度阶梯。 |
| E-C16-006 | METHODOLOGY | PASS | “责任闭环而非固定数量”与 C04 角色、C09 任务闭环一致。 |
| E-C16-007 | METHODOLOGY | PASS | 同任务、输入、工具权限、总预算、风险和端到端结果完整；未用非等价预算做领先声明。 |
| E-C16-008 | METHODOLOGY | PASS | 越权、泄露、重复副作用、不可恢复失败均为非补偿硬门。 |
| E-C16-009 | METHODOLOGY | PASS | 身份、会话、上下文、Workspace、权限、凭证逐面分离；正文明确 workspace/session 不推出 sandbox/credential。 |
| E-C16-010 | METHODOLOGY | PASS | 作为本书方法论由 preflight 支撑；Anthropic 仅作独立上下文、重复工作与协调成本的场景证据，正文没有把其内部评测外推。 |
| E-C16-011 | VERSION-FACT | PASS | 固定文档明确 bindings/route 决定入口到 Agent；正文正确否定其对胜任与授权的证明力。 |
| E-C16-012 | VERSION-FACT | PASS | 固定 subagent 文档只保证自有 session 并将 sandbox 写为 optional；C06 亦禁止 session/workspace 冒充 sandbox。 |
| E-C16-013 | VERSION-FACT | **REVIEW_REQUIRED** | “allowAgents 与 tool policy 不同边界”成立，但正文将固定字段写成 `agents.list[].subagents.allowAgents`；固定版公开路径为 `agents.entries.*.subagents.allowAgents`。 |
| E-C16-014 | VERSION-FACT | PASS | 固定文档把 announce 写成结果回传；C09 正确要求另行验证产物可见与环境/业务终态。 |
| E-C16-015 | DYNAMIC-OFFICIAL | PASS | 固定 `f80f453…/0.20.1` 与动态 docs 分栏；正文未把当前网页的并发、继承或取消字段倒填固定版。 |
| E-C16-016 | VENDOR-CLAIM | **REVIEW_REQUIRED** | 身份标签正确、没有把厂商主张当独立效果，但 ledger 中 MUSE 发布页不含 `swarms/subagents`。必须补入真正支持该句的 Meta 官方安全文章，或改写为当前来源支持的 Sentinel 双 Agent 镜面。 |
| E-C16-017 | STANDARD-FACT | PASS | A2A 1.0 规范支持所列对象、异步与版本协商，也明确授权范围由实现/发行者/扩展决定；正文没有提前定义 C18 信任。 |
| E-C16-018 | METHODOLOGY | PASS | 角色从 C04 任务/能力节点生成，正文明确禁止人格、模型名或工具名倒推角色。 |
| E-C16-019 | METHODOLOGY | PASS | 完成性消费 C09 的过程、产物、效果三证；子 Agent 自报和 UI 信号没有被当环境终态。 |
| E-C16-020 | METHODOLOGY | PASS | 只消费 C14 `AU-L0—AU-L4`、授权与委托衰减；未更改等级，也未声称 C14 实践门通过。 |
| E-C16-021 | METHODOLOGY | PASS | artifacts 目录恰好三件母产物，运行材料与练习未冒充第四件。 |
| E-C16-022 | LOCAL-VALIDATION | PASS | fresh/fresh 与 fresh/saved 字节一致；45 trial 为 12 PASS/27 FAIL/6 RR，45 trial_id 唯一，零外部副作用。措辞精度另列 P2。 |
| E-C16-023 | LOCAL-VALIDATION | PASS | 15 类输入实际覆盖所列单体、负收益、共享写、共识、越权、失联、幽灵成功、预算、取消等场景。 |
| E-C16-024 | METHODOLOGY | PASS | C16 只输出拓扑、角色、join/取消需求；C17 保留路由/Handoff/取消/并发定义权，C18 保留 A2A 对象与信任定义权。 |
| E-C16-025 | METHODOLOGY | PASS | 仿生四段完整，明确否定社会主体性、天然职位权与 Agent 最终组织责任。 |

## 平台与协议裁决

### OpenClaw 固定版

固定身份核验通过：`v2026.9.6` 的 tag object 指向 `eb377ac59e6c9fd6c7705028034812becf00271b`。Bindings、agent/workspace/session 边界、subagent 自有 session、announce 和 tool-policy 分工有固定文档支持。唯一 P0 是正文第 528 行的字段路径：`agents.list[]` 在固定文档中只作为旧 roster 迁移对象出现，不是 `subagents.allowAgents` 的规范承载路径。

关闭条件：改为 `agents.entries.*.subagents.allowAgents`；检查章节、产物和练习是否有同类路径；以固定 commit 文档重新核验 E-C16-013。

### Hermes fixed / dynamic

`f80f453…` 可达，tag `v2026.8.13` 指向该提交，固定 `pyproject.toml` 与 `hermes_cli/__init__.py` 均写 `0.20.1`。动态文档当前明确描述 profiles/bots/delegation，但本章只把它作为 2026-09-30 观察，并把工具继承、取消、结果回传和 profile 隔离保持为待目标版验证，没有跨层倒填。

### Muse `VENDOR-CLAIM`

章节对闭源产品的证据上限写得正确，但引用对象不正确。账本所列发布页支持 Secure VM、单独 Sentinel、后台工作、审批和审计轨迹，却没有 `swarms/subagents`。Meta 官方安全文章《How We Built Safety Into Muse》确实描述“launches swarms of subagents”和 subagent handoffs，可作为候选补证；在它正式进入 ledger 并绑定 claim 之前，E-C16-016 仍为 `REVIEW_REQUIRED`。

### A2A 1.0

当前官方规范页显示正式版本 `1.0.0`，所列 Agent Card、Task、Message、Artifact、异步更新和版本协商语义成立；规范还明确 `TASK_STATE_AUTH_REQUIRED` 本身不构成特定动作授权。这直接支持“互操作不证明组织选择、能力、授权、输出或信任”。非阻塞改进是把 `/latest/` 换成 `/v1.0.0/`，避免印刷版证据身份随站点升级漂移。

## 45-trial 完整性旁证

两次 fresh-temp 复跑与作者保存结果逐字节一致：

- results SHA-256：`acd0327e8d9a8595dfe327e39a483e20387e7cdbccf8b2f089604eaa19382dc1`；
- summary SHA-256：`9cef578e78e921971cd13775d8fbcc5b99edf386a508fb456213871a6955d653`；
- 15 个唯一 task_id，每个 3 次，共 45 个唯一 trial_id；
- 12 PASS、27 FAIL、6 REVIEW_REQUIRED；`external_effects` 全为 0。

这只证明保存的合成规则可确定复算，不证明两项练习已由独立实践 reviewer 执行，不证明真实身份/凭证/sandbox/停止/取消或多 Agent 净收益。数据层谱系问题单列在 [cross-review.md](cross-review.md)。

## 问题分级与关闭条件

### P0

1. `P0-F16-01 / P0-04 / E-C16-013`：修复 OpenClaw 固定字段 `agents.list[]` → `agents.entries.*`，并做固定版全文回归。
2. `P0-F16-02 / P0-03+P0-12 / E-C16-016`：补入真正支持 `swarms/subagents` 的一手来源并绑定 claim，或把句子改到当前 MUSE 来源实际支持的范围。

### P1

1. `P1-F16-03 / E-C16-017`：把 A2A 来源从动态 `/latest/` 固定到 `/v1.0.0/`；印前仍检查 1.0.x patch 与规范变化。

### P2

1. `P2-F16-04 / E-C16-022`：把“45 个唯一 task/trial”精确写成“15 个任务、每项 3 次、45 个唯一 trial_id”，避免误读为 45 个独立任务。

## 门禁声明

本记录只裁决事实与版本。事实门在两项 P0 关闭并由非作者回归前保持 `REVIEW_REQUIRED`。本记录不批准实践、编辑、总编或 `release_candidate`；真实 OpenClaw/Hermes/Muse/A2A 运行与长期净收益仍为独立实践和后章责任。

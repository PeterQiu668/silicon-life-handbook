---
review_id: ER-C04-001
chapter_id: C04
review_type: evidence-and-version
status: passed_with_limitations
reviewed_on: "2026-09-30"
reviewer: c04-evidence-cross-review-agent
chapter_status_after_review: drafting
self_approval: false
practice_review_completed: false
final_editorial_approval: false
---

# C04 证据门独立审稿单

## 1. 结论

C04 的证据门结论为 `PASS WITH LIMITATIONS`。正文 13 个证据 ID 与账本 13 项主张一一闭合；方法论、稳定原理、版本事实、推断和厂商声明的身份分层正确。OpenClaw 的关键 Runtime 事实已同时指向 `v2026.9.6` release 与固定提交 `eb377ac59e6c9fd6c7705028034812becf00271b`；Hermes 只把 `0.20.1` 当发布基线，架构与 Profile 页面明确属于核验日动态文档上的迁移候选；Muse 始终保留 `VENDOR-CLAIM`，没有从 Meta 自述推出内部岗位模型、训练方法或独立安全效果。

本轮未发现伪造来源、断链证据或把作者方法冒充外部标准的 P0。限制仍然存在：Hermes 动态文档尚未逐项固定到 0.20.1 源码；五支能力树、五类 NFR 和四因子风险尚未经过跨岗位实践校准；Muse 缺少独立复现。以上限制已在账本、正文和开放问题中显式保留，不阻断事实门，但禁止升级措辞。

## 2. 审查范围与方法

本审稿对照 v2 第 4 章、C04 章节卡、质量标准、平台证据底稿、术语表、路由表、C01—C03 正式产物、C04 正文、三件产物和两项练习。审查内容包括：

- 每条正文证据 ID 能否解引用到 YAML 账本；
- 来源是否是一手或对自身系统负责的官方材料，是否写明核验日、版本与限制；
- 本书方法是否清楚标为 `METHODOLOGY`，没有伪装成 NIST、JTBD、OpenClaw、Hermes 或 Muse 官方标准；
- 三平台事实是否按开放程度与证据可见性分层；
- 版本事实是否使用固定 release/commit，动态页面是否被限缩；
- 外部 URL 与本地证据路径是否可访问；
- 事实结论是否越过来源能支持的范围。

2026-09-30 对账时，账本 18 个唯一外部 URL 均返回 HTTP 200。可访问只证明链接当前可达，不自动证明主张；因此又对 OpenClaw 固定提交、Hermes Architecture/Profile 和 Meta Muse 发布页做了内容抽查，并以账本限制字段控制外推。

## 3. 逐项证据裁决

| 证据 ID | 身份与用途 | 来源质量 | 结论 |
| --- | --- | --- | --- |
| E-C04-001 | 岗位—能力可追溯链；本书方法 | v2、历史映射、章节卡 | PASS；没有冒充行业标准 |
| E-C04-002 | 先用最小有效复杂度，从任务和成功定义出发 | Anthropic 官方工程材料 | PASS；作为实践原则，不写成强制规范 |
| E-C04-003 | JTBD 的“情境中的进展”核心 | Christensen Institute 理论所有者材料 | PASS；本章工程链明确是作者扩展 |
| E-C04-004 | 五支能力树 | v2 + C03 正式评分卡 | PASS；明确不与七维合并 |
| E-C04-005 | 五类岗位 NFR | v2 + Anthropic/OpenAI 评测材料 | PASS；类别与阈值均保留作者方法边界 |
| E-C04-006 | 风险治理贯穿生命周期并结合情境/影响 | NIST AI RMF 1.0 官方材料 | PASS；四因子不是 NIST 原文分类 |
| E-C04-007 | 高影响动作需要有意义的人类控制 | Anthropic 研究 + OpenAI 官方安全指南 | PASS；稳定工程原则，具体范围交组织政策/后章 |
| E-C04-008 | 模型拒绝不足以独自承担系统控制 | OpenAI、Anthropic、NIST | PASS；没有据此提前定义 C19 完整架构 |
| E-C04-009 | 明确任务/成功条件、多次运行、轨迹与评审 | Anthropic/OpenAI 官方评测材料 | PASS；五类测试是本书候选分类，正式协议交 C07 |
| E-C04-010 | trace grading / dataset / eval runs | OpenAI 官方产品与方法文档 | PASS；限定 OpenAI 平台语境，不要求记录私有思维链 |
| E-C04-011 | OpenClaw Runtime 可承载岗位派生需求 | v2026.9.6 release + 固定 SHA 文档 +动态官方页 | PASS；固定文档支持 model/tool/prompt/session/channel 职责，平台存在不等于岗位胜任 |
| E-C04-012 | Hermes 作为第二开放实现候选 | v0.20.1 release + Architecture/Profile 动态官方页 | PASS WITH LIMIT；保持 `INFERENCE`，未声称逐项固定版本同构 |
| E-C04-013 | Muse 的目标、连接器与敏感动作批准表面 | Meta 发布与研究材料 | PASS AS VENDOR CLAIM；不能写成独立安全验证 |

## 4. 三平台事实与选型顺序

| 平台 | 可确认事实 | 本章允许用途 | 禁止外推 | 判定 |
| --- | --- | --- | --- | --- |
| OpenClaw | 2026.9.6 release 与固定提交中的 Runtime 职责可核查 | 岗位冻结后的主实现候选 | 不能由组件、工具或文件存在推出岗位胜任与真实权限 | PASS |
| Hermes | 0.20.1 发布可固定；Architecture/Profile 为核验日动态官方说明 | 第二开放实现与跨 Runtime 候选 | 不能把动态页逐项算入 0.20.1，也不能把 Profile 当 Sandbox | PASS WITH LIMIT |
| Muse | Meta 公开说明目标、后台工作、连接器、审批与活动表面 | 托管产品行为镜面 | 不推断内部岗位模型、训练机制、安全效果或 Confidential VM 全面上线 | PASS AS VENDOR CLAIM |

正文的选型顺序是“岗位/JTBD/任务域/能力/NFR/风险/负面清单冻结后，再选择平台、模型、Provider、工具与运行方式”。OpenClaw 与 Hermes 没有因可配置能力丰富而被写成默认答案；Muse 没有被放进开放 Runtime 的同构比较。

## 5. 事实标注与本地路径闭合

- 正文引用：13 个；账本声明：13 个；缺失 0，孤儿 0。
- 账本本地来源：7 个路径引用，全部存在并能解析到 v2、章节卡、历史映射、C03 评分卡或平台证据底稿。
- 外部来源：18 个唯一 URL，核验日均可达；来源主体包括 NIST、Christensen Institute、Anthropic、OpenAI、OpenClaw、Nous Research、Meta。
- 关键平台来源均为官方 release、固定源码文档或官方页面；没有用搜索摘要、新闻转载或二手博客承担版本事实。
- `verified_on`、`version_scope`、`limitations` 与 `recheck_trigger` 在版本/前沿主张中齐全。

## 6. 本轮小修

1. 为 E-C04-011 增加 OpenClaw 固定提交中的 Agent Runtime 文档，降低“release + 动态文档”之间的版本漂移风险。
2. 将 E-C04-007 的 `stability` 从 `frontier` 校正为 `stable`，与其 `STABLE-PRINCIPLE` 身份和正文用途一致；具体实现仍可变。
3. 没有修改 Muse 或 Hermes 的证据等级，也没有把开放问题写成已解决。

## 7. 问题分级

### P0

无开放事实级 P0。

### P1

1. **Hermes 固定源码映射未完成。** `0.20.1` 发布可核验，但当前 Architecture/Profile 页面可能包含后续变化。出版前应将本章实际使用的组件逐项定位到 tag，或继续保留动态文档推断措辞。责任人：平台事实审校者。
2. **方法量表尚未实践校准。** 五支能力、五类 NFR 和四因子风险属于作者方法；需要实践评审用多个脱敏岗位记录无法归类节点与盲评分分歧。责任人：实践评审者。
3. **全局术语登记已由主编关闭。** 总编辑已将 `岗位模型、任务域、能力节点、非功能要求、负面清单` 登记为 C04 主定义的 `methodology` 术语，并将 `BOOK-FRAMEWORK` 来源修正为 v2。本审稿复核了定义权、混淆项与来源指针；该项不再是开放 P1。

### P2

1. Anthropic 与 OpenAI 的安全/评测材料属于厂商官方实践，不是独立行业标准；当前账本已写明，后续引用仍应保留来源主体。
2. 外部 URL 返回 200 不代表内容永不变化；动态页必须按 `recheck_trigger` 在印前重核。

## 8. 证据门状态

- 事实与标签：`PASS`
- 固定版本：`PASS WITH HERMES LIMITATION`
- 平台边界：`PASS`
- 引用闭合：`PASS`
- 练习实证：`NOT ASSESSED`
- 总编批准：`false`

本审稿只关闭 C04 的当前事实门，不代替实践试跑、交叉回归、C07/C14/C19/C24 的下游消费验证或总编批准。章节保持 `drafting`。

---
review_id: C10-independent-cross-review-20260930
chapter_id: C10
review_type: independent-cross-chapter-cross-platform-review
reviewed_on: "2026-09-30"
reviewer_role: cross-reviewer
chapter_status: drafting
cross_gate: passed_with_limitations
fact_review_ref: "review/fact-check.md"
practice_gate: not_reviewed
editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C10 跨章与跨平台审校

## 1. 结论

C10 的概念所有权、10.1—10.8、三件母产物、C09→C10 输入和 C10→C15/C19/C21 输出已经对齐。Context、Memory、task state、record、evidence 与 authorization 保持独立；Memory、Context、MAT、AU 均不产生 authority；D20 只有能力、人格、文档、工具、目标五类一级漂移。

本轮发现并修补一项章际接口缺口：正文 frontmatter 与 10.8.8 原先没有显式列出 C10→C19 的安全交付，虽然三件母产物已经把 C19 列为消费者。现已补入来源/taint、跨域数据流、敏感级别、过滤失败、污染/外泄/删除失败、停止与 residual，同时明确安全定义权仍属 C19。

交叉门结论为 **`PASS WITH LIMITATIONS`**。限制来自 C15/C19/C21 尚以 preflight 为主要下游合同，正式章冻结后必须再做字段级回归；本结论不批准实践、编辑、总编或发布门。

## 2. 单一概念所有权

| 对象 | 主定义章 | C10 行为 | 结论 |
| --- | --- | --- | --- |
| MEMORY 契约语义与七契约优先级 | C05 | 消费承诺，落实写入/检索/纠错/处置 | PASS |
| Runtime、Session、Workspace、Queue 架构位置 | C06 | 只作为事实源、运行面和恢复输入 | PASS |
| 任务卡、上下文包、交付/反馈候选 | C09 | 接收任务级输入，不自动晋升长期 Memory | PASS |
| Context/Memory 分类与全生命周期 | C10 | 唯一主定义 | PASS |
| 工具与 MCP 身份、鉴权、Schema | C11 | 只提出记忆侧工具约束 | PASS |
| 漂移分类与受控改进 | C15 | 输出状态与证据，不定义漂移门 | PASS |
| 身份、权限、Sandbox、Approval、秘密与事故 | C19 | 输出攻击/数据面，不重写安全模型 | PASS |
| 组织级发布、恢复、退役和数据处置 | C21 | 输出 coverage/residual/receipt，不宣称法律完成 | PASS |
| 自主与成熟度 | C14/C24 | 只执行 `AU-`/`MAT-` 分离，不授级 | PASS |

## 3. 六对象分离检查

| 对象 | C10 权威源/职责 | 明确不负责 | 结论 |
| --- | --- | --- | --- |
| Context | 单次 run/call 的有界装配结果与 manifest | 不等于持久 Memory、Session、授权 | PASS |
| Memory | 被选择后跨调用/任务持久保存并可检索的状态 | 不等于当前 task state 或权限 | PASS |
| task state | C09 任务系统的 owner、阶段、attempt、批准、终态 | 不从自然语言记忆猜测 | PASS |
| record | 保存事件、决定、数据或变更 | 不保证内容正确或当前 | PASS |
| evidence | 支持/反驳主张的可定位材料 | 不自动允许行动 | PASS |
| authorization | 外部当前身份、Policy、Approval、凭证与目标系统决定 | 不由任何文本、记忆、检索分数、MAT/AU 生成 | PASS |

章节、三件产物、练习和作者运行合同在这一分离上没有互相矛盾。`authorization_ref` 被限定为外部事实源的定位符，不能被 Memory 自行重放或扩展。

## 4. C09→C10 接口

### 输入对齐

C09 提供任务卡、上下文包和交付证据包：任务版本、最小充分输入、来源/时间/敏感性/用途、反馈许可和候选字段均可定位。C10 正确执行三项转换：

1. task state 继续由任务系统持有，Memory 只保存历史或定位符；
2. 上下文包项目进入即时 Context 或 memory candidate 前重新过目的、主体、来源、权利、污染和保留门；
3. 生产反馈只能成为候选，不能直接写 Memory、Skill 或训练集。

### 不越权

C10 没有重定义 C09 的任务卡、四轴状态、交付三证或 feedback permission；C09 也没有承诺 Memory 删除范围。C09→C10 为 `PASS`。

## 5. C10→C15 接口与 D20

C10 输出 memory policy 版本、来源/taint、active/superseded 图、Context manifest、内容/索引/Compaction 变更、影响范围与回归结果。C15 决定这些变化属于哪类漂移以及是否进入受控改进。

一级分类严格保持：

1. 能力漂移；
2. 人格漂移；
3. 文档漂移；
4. 工具漂移；
5. 目标漂移。

“记忆漂移”只作为待消歧口语出现，正式判断必须映射到上述五类；Memory/Context 是跨类型状态源与证据源，不是第六类。程序性记忆只形成 proposal，不能因 Dreaming、一次成功或错误积累自动固化。C10→C15 为 `PASS WITH LIMITATION`：C15 正式章冻结后需回归字段名与再认证触发器。

## 6. C10→C19 接口

### 已交付

- 来源、lineage 与 taint；
- 跨 user/role/tenant/project 的数据流；
- sensitivity、purpose、scope 与 denied-before-ranking 记录；
- 污染、Prompt Injection 输入、跨域泄露、凭证持久化、删除失败和 residual；
- writer fence、recall suppression、事故停止与 evidence preservation；
- 授权事实源定位符，但不生成授权。

### 定义权保留

C19 继续主定义 authentication、最小权限、Sandbox、Approval、秘密、凭证代理、Prompt Injection 防御、事件响应和强制控制。C10 的写入/检索策略不能替代 OS/Runtime/Policy 控制；让模型“忽略越权片段”不算隔离。

该接口原先只在三件母产物的 `consumed_by` 与零散正文出现，本轮已补入 chapter frontmatter、章首交接和 10.8.8 正式合同。C10→C19 为 `PASS WITH LIMITATION`：C19 正式章冻结后需检查事件名、severity 和 incident handoff Schema。

## 7. C10→C21 接口

C10 输出 data/backup owner、retention reason、current/superseded/tombstoned 状态、deletion coverage、receipt、exclusion、residual、预计时点与 restore-resurrection 结果。C21 决定组织级保留、发布、恢复、暂停、退役、撤权和数据处置责任。

C10 正确避免三种越权：不把 UI 不可见写成物理删除，不把本地 index 删除写成供应商/模型权重已清除，不提供法律合规结论。C10→C21 为 `PASS WITH LIMITATION`：C21 正式章冻结后需要回归 disposition/retirement receipt 字段。

## 8. 跨平台映射

| 平台 | 证据层 | C10 使用方式 | 禁止外推 | 结论 |
| --- | --- | --- | --- | --- |
| OpenClaw | 固定 v2026.9.6 / eb377ac | Context、tiers/provenance、builtin index、Compaction、Session、Workspace、forget coverage/exclusions | 目标部署已启用；其他 plugin 同覆盖；forget 等于全局删除 | PASS |
| Hermes release | 固定 v0.20.1 / v2026.8.13 / f80f453 | 只作为发布身份锚点 | 动态官网字段已逐项存在于固定提交 | PASS |
| Hermes docs | 2026-09-30 DYNAMIC-OFFICIAL | bounded curated memory、frozen snapshot、FTS5 session search、lossy compression 的当前适配镜面 | 与 OpenClaw 动态 recall/Dreaming/Compaction 同构 | PASS WITH LIMITATION |
| Muse | VENDOR-CLAIM | 用户可见 memory 操作、Secure VM、backup、training opt-out 的产品镜面 | 内部 Schema、forget coverage、独立安全/效果 | PASS WITH LIMITATION |

## 9. MAT/AU 与 authority

- 数字产物、表格、日志和跨章引用均使用 `MAT-L0—MAT-L5` / `AU-L0—AU-L4` 或带前缀的 `MAT-Lx` / `AU-Lx`；
- 没有缺少 `MAT-` / `AU-` 前缀的等级写法；
- 高 MAT 不推出高 AU，高 AU 不证明 MAT，二者都不推出真实账户权限；
- 历史 AU 标签和旧 approval 只能作为 record/evidence，执行前必须读取当前授权事实源；
- Memory 记录中的 `authorization_evidence_ref` 只是定位符。

结论：`PASS`。

## 10. 10.1—10.8 与三件母产物

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 10.1 对象与四类记忆 | PASS | 六对象、四类治理模型、MAT/AU、D20、人格边界齐全 |
| 10.2 写入准入 | PASS | candidate、十一门、禁止写入、并发更新、程序候选、双视图齐全 |
| 10.3 检索与注入 | PASS | 强过滤先于排序、五判断、taint、manifest、查询泄漏齐全 |
| 10.4 压缩/摘要/快照/Dreaming | PASS | 有损边界、保真合同、对账与工程真相齐全 |
| 10.5 污染与失败 | PASS | 五路径、15 类完整失败和红队问题齐全 |
| 10.6 全生命周期 | PASS | provenance、访问、更正、保留、四种遗忘、coverage、backup、四层回滚齐全 |
| 10.7 评测与练习 | PASS（设计） | 五段链、C0—C3、五场景、两练习、三态与硬门齐全；实践未由本审校批准 |
| 10.8 平台/仿生/交接 | PASS WITH LIMITATION | 三平台证据分层、仿生四段和章际字段齐全；下游正式章待回归 |
| A-C10-01 记忆架构图 | PASS | 对象、事实源、信任域、派生链、平台映射和恢复不变量 |
| A-C10-02 写入与保留策略 | PASS | 写入、检索、更新、遗忘、删除、备份、程序变更和停止 |
| A-C10-03 记忆测试集 | PASS | C0—C3、12 task、20 failure、14 red-team、逐 trial Schema |

artifacts 目录恰有三件正式母产物；练习、运行文件和 review 不构成第四件。

## 11. 15 项 P0 交叉结论

| P0 | 结论 | 交叉审校说明 |
| --- | --- | --- |
| P0-01 | PASS | 章首导航、10.1—10.8、案例、仿生、双视图、失败、练习、验收和交接完整。 |
| P0-02 | PASS | C10 拥有 Context/Memory 生命周期；C05/C06/C09/C15/C19/C21 定义权保留。 |
| P0-03 | PASS WITH LIMITATIONS | 24 条 claim、40 个来源闭合；动态与厂商材料限制公开。 |
| P0-04 | PASS WITH LIMITATIONS | OpenClaw tag/commit、Hermes release/commit 已核；目标部署和动态字段仍待实践/源码。 |
| P0-05 | PASS（设计） | writer fence、四层回滚、删除/恢复顺序和停止合同完整；真实执行不在本门。 |
| P0-06 | PASS | 强过滤先于相似度，Memory/Context/文本不授予权限；C19 强制控制权保留。 |
| P0-07 | REVIEW_REQUIRED | 作者合成文件内部一致，但本轮没有独立执行两项练习或真实 Runtime。 |
| P0-08 | PASS | 仿生四段完整，不把存储/召回写成人类意识、人格连续或生物记忆。 |
| P0-09 | PASS WITH LIMITATIONS | OpenClaw fixed、Hermes fixed/dynamic、Muse vendor claim 已分栏。 |
| P0-10 | PASS | CASE-A/B/C 和运行数据明确为合成教学材料，不冒充客户或生产业绩。 |
| P0-11 | PASS | 三个 Agent YAML 块、账本与运行 YAML 可解析；不含未授权外发或删除。 |
| P0-12 | PASS | deployment、Hermes 对照、Muse coverage、Provider 保留等未知项公开。 |
| P0-13 | PASS | 泄漏、敏感持久化、未授权动作、虚假删除和自动发布不可被平均。 |
| P0-14 | PASS | 三件母产物可定位且被 C15/C19/C21 等下游显式消费。 |
| P0-15 | PASS | 没有行业领先或真实提升声明；“记得更多”被无记忆基线和成本反证约束。 |

## 12. 问题清单

### P0

无未关闭的交叉 P0。P0-07 保留给独立实践门，不由本审校代签。

### P1

1. C15/C19/C21 正式章尚未冻结，当前接口只能依据 v2、章节卡和 preflight 判定，必须在下游总编门后回归。
2. 目标 OpenClaw/Hermes 部署没有实机探测，平台适配不能升级为部署事实。
3. Muse 删除、备份、训练与 telemetry coverage 未知，采购或合规使用前必须取得更强证据。

### P2

1. 作者合成运行虽保留完整分布，但仍是作者设计/执行链；独立复现应比较输入、输出、环境终态和无外部副作用。
2. C11 包正在准备中；正式工具 Schema 冻结后应回归 memory read/write/delete 工具的鉴权、幂等和 taint 字段。

## 13. 本轮修补

- 修补 Hermes E-C10-017/018 固定/动态时间层；
- 增加 OpenClaw/Hermes tag—commit 来源；
- 移除未使用的账本 source；
- 补齐 C10→C19 正式交接；
- 同步 0.1.1 变更记录和作者 P0-14 描述。

未修改作者合成输入、脚本、结果、摘要、练习结论、章节状态或任何实践/编辑门。

## 14. 交叉门决定

```yaml
cross_gate:
  chapter_id: C10
  verdict: PASS_WITH_LIMITATIONS
  concept_ownership: PASS
  c09_to_c10: PASS
  c10_to_c15: PASS_WITH_LIMITATION_DOWNSTREAM_NOT_FROZEN
  c10_to_c19: PASS_WITH_LIMITATION_DOWNSTREAM_NOT_FROZEN
  c10_to_c21: PASS_WITH_LIMITATION_DOWNSTREAM_NOT_FROZEN
  platform_mapping: PASS_WITH_LIMITATIONS
  practice_approved: false
  editor_approved: false
  chapter_status_after_review: drafting
  release_candidate_authorized: false
```

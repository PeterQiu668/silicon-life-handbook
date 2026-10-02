---
review_id: CR-C08-001
chapter_id: C08
review_type: independent-cross-chapter-and-cross-platform-gate
status: completed_with_required_downstream_fixes
reviewed_on: "2026-09-30"
reviewer: "non-author-cross-reviewer:platform_research"
independent_from_author: true
fact_gate_observed: PASS
cross_gate: REVIEW_REQUIRED
practice_gate: not_approved
editor_gate: not_approved
chief_editor_gate: not_approved
chapter_status_after_review: drafting
self_approval: false
release_candidate_authorized: false
---

# C08 独立跨章与跨平台审校

## 1. 裁决

**C08 自身的定义、D22 数据层、训练/评测/发布分权、单变量、停训/回滚、平台边界、MAT/AU 分离和三母产物均成立；但全书当前存在两处下游 P0-02 定义漂移，因此跨章门为 `REVIEW_REQUIRED`。**

阻断项不在 C08 正文内：C12 正式章把 C02 拥有的“训练/生产双闭环”误归给 C08；C22 preflight 又把 C08 唯一双三角改写为另一组“任务目标—执行轨迹—环境终态 / 学员自检—训练者反馈—独立 evaluator”。在这两处修正并回归前，不能宣称 C08 的全书定义已经闭合。其余交叉检查无新增 P0。

## 2. C08 主定义与上游消费

| 对象 | 定义 owner | C08 的行为 | 结论 |
| --- | --- | --- | --- |
| Agent 系统 | C01 | 把学员视为系统组合，不把训练缩成模型提示 | PASS |
| 训虾范式、训练/生产双闭环 | C02 | 消费生产失败进入训练、训练候选进入生产的门，不重画总图 | PASS |
| 七维与三证 | C03 | 只说明双三角可引用过程/产物/效果，不重定义七维或总分 | PASS |
| 岗位、能力、NFR、风险 | C04 | 作为训练目标和风险输入，不反向改写岗位 | PASS |
| 七大契约 | C05 | 把契约语义与权限强制分开，只提交候选 | PASS |
| 评测系统 | C07 | 消费 task/trial/trajectory/outcome/grader、基线、污染、四层与三态，不另造统计协议 | PASS |
| 训练循环、双三角、轮次、停训 | C08 | 本章唯一主定义 | PASS |
| 自主阶梯 | C14 | 不修改 `AU-L0—AU-L4`，训练不扩权 | PASS |
| 漂移与自我改进治理 | C15 | 只提交 change set、失效条件、影子/回滚输入 | PASS |
| 成熟度与认证 | C24 | 不发布 `MAT-L0—MAT-L5` 阈值，不把轮次成绩换认证 | PASS |

## 3. D22：四个规范数据层与横切安全套件

| 检查项 | 位置 | 结论 |
| --- | --- | --- |
| 规范层恰为 `training/regression/holdout/real_world` | 章首、8.8.1、A-C08-01、harness 输出 | PASS |
| security/red-team 是横切非补偿 suite/slice | 章首、8.5.3、8.8.1、三件母产物、两项练习 | PASS |
| S01—S03 映射为 `holdout × adversarial` | 8.5.3、CASE-A、A-C08-01/02/03、运行证据 | PASS |
| `real_world_samples_in_fixture=0` | 正文、作者摘要、非作者实践复现 | PASS |
| 安全硬失败不被训练/回归分数抵消 | 开场、8.6、8.8、练习与终局决定 | PASS |
| 安全套件不顶替 real_world | 8.8.1、产物与练习 | PASS |

C08 使用“train/regression/ordinary holdout/cross-cutting safety”描述合成运行分区，并专门声明这四个运行分区不是 C07 四个规范数据层；这一澄清避免把 safety 误认第五层。

## 4. C07 task/trial/grader/污染接口

概念接口闭合：C08 把 C07 的 task、trial、完整 trace/trajectory、environment outcome、code/model/human/expert grader、冻结 rubric、争议校准、样本暴露史与污染失效规则作为输入。导师、学员、reviewer 的数据访问和最终发布权分开；留出一经暴露即失效，不能“换文件夹恢复隐藏性”。

实践接口仍有限：当前合成 harness 用 `sample_id` 和 `revision + sample_id` 派生唯一尝试，没有显式 `task_id/trial_id`；答案键、候选函数和 deterministic reviewer 同处一个进程；没有真实 model/human/expert grader。这些已由 [practice-review.md](practice-review.md) 登记为实践 P1，不构成 C08 对 C07 定义的重写，但阻止总实践门通过。

## 5. 训练、评估与发布权分离

| 权力 | C08 归属 | 禁止的越权 | 结论 |
| --- | --- | --- | --- |
| 训练目标与投入 | human role/risk/data owner | Teacher 自己扩大范围 | PASS |
| 候选生成 | Teacher/Learner/Coordinator 在隔离范围内 | 候选直接 apply | PASS |
| 评测 | 独立 reviewer 使用 C07 冻结规格 | 导师改 grader、看留出后自签 | PASS |
| 训练终局建议 | Coordinator + reviewer 留证 | 用训练满分宣布能力 | PASS |
| 固化/漂移治理 | C15 | C08 自批长期自我改进 | PASS |
| 生产发布/回滚批准 | C21 与有权主体 | 评测 PASS 自动等于发布 | PASS |
| 自主/权限 | C14/C19 | 训练成绩自动扩权 | PASS |
| 认证 | C24 | 轮次分数换 MAT 等级 | PASS |

正文还把 trial 状态、candidate 状态、evaluation 状态和 release 状态分开，避免四种“完成”压成同一个绿色标签。

## 6. 双三角与单变量归因

### 6.1 C08 唯一口径

C08 与术语表一致：训练三角是“目标—行为—反馈”，证据三角是“任务—能力—证据”。它不等于 C02 的训练/生产双闭环，不等于 C03 七维/三证，也不等于 C07 评测对象。正文、A-C08-01 与 A-C08-02 使用同一口径，反例和 CASE-A/B/C 均能闭合。

### 6.2 单变量与归因

本章要求一个主干预对象、精确 diff、不变量、交互风险和反证条件；同时变化时只允许报告组合差异，不允许给单项因果。合成案例三轮累积修改同一个 `source_discipline_skill_revision`，样本、答案、grader、Runtime、预算和风险不变，支持“固定 harness 内规则演化”的窄归因。它没有候选文件 hash/exact diff，也不是统计独立的模型训练，因此不能外推真实能力提升；实践记录已保留该限制。

## 7. 停训、回滚与安全状态

C08 在训练前预注册安全、权限、污染、归因、预算、版本、回滚、连续失败和信息价值等停训条件；停训后冻结证据、确认影响面、查询未知终态、恢复安全版本、做最小回归/负向权限测试并决定问题去向。合成案例在 R3 的普通 holdout `4/5` 和 safety `2/3` 时执行 `STOP_AND_ROLLBACK_CANDIDATES`，候选未外部应用，安全状态保持 `manual-review-mode`。

真实 Runtime 回滚仍未实践。正文没有把“丢弃未发布候选”外推为 Queue/Session/Memory/cache/index/权限和外部副作用均已恢复，因此跨章语义正确，实践门继续 `REVIEW_REQUIRED`。

## 8. 下游接口审查

| 下游 | 当前消费 | 定义权边界 | 结论 |
| --- | --- | --- | --- |
| C09 | 任务卡/上下文包/交付三证与反馈回流许可消费 C08 训练引用；原始群聊不直通训练 | 不重定义 C07 grader、C10 Memory、C17 Handoff、C18 A2A | PASS |
| C12 | Skill 候选、单变量、外评、批准、撤回可消费 C08 训练干预 | 双闭环属于 C02；Skill/供应链属于 C12 | REVIEW_REQUIRED：当前 C12 正式章把“双闭环”误归 C08 |
| C15 | 消费 C08 change set、干预、版本、失效条件、shadow/canary 包 | 漂移和固化治理归 C15，训练角色/轮次归 C08 | PASS |
| C22 | 应把 C08 三件产物、唯一双三角、轮次、停训与合成限制编入课程 | 课程不得改写 C08 双三角，不得把合成 PASS 当真实训练 | REVIEW_REQUIRED：preflight 另造双三角且状态仍写 `regression_required` |

形式依赖方面，C08 章节卡的 `feeds_into` 是 `[C09, C15, C22, C23, C24]`，与 chapter frontmatter 完全一致。C12 章节卡没有把 C08 列为硬依赖，因此 C12 对 C08 的消费只能是补充方法接口；不得据此反向修改 C08 的正式依赖，更不得把 C02 双闭环转移给 C08。

### 必须由相应 owner 修正的两处 P0-02

1. [C15 正式章](../../../volume-05/C15-skill-engineering/chapter.md) 15.7.1 与章末输入把“训练/生产双闭环”写成 C08 所有。应改为：C02 提供训练/生产双闭环；C08 提供训练干预、轮次、双三角、停训和候选证据链。
2. [C25 preflight](../../../../docs/research/C25-thirty-day-training-camp-preflight.md) 7.1 把“双三角”改成另一套两组三元关系。应直接复用 C08 的“目标—行为—反馈 / 任务—能力—证据”；任务目标、轨迹、终态和学员/训练者/evaluator 可作为字段或角色检查，不得继续称为平行双三角。

## 9. `MAT-Lx` 与 `AU-Lx` 不互推

正文、Agent 机器块、A-C08-01 和章节交接均明确：

- `AU-L0—AU-L4` 描述任务级自主深度，由 C14 定义；
- `MAT-L0—MAT-L5` 描述综合成熟度，由 C24 定义；
- 训练分数不能推出自主、权限或成熟度；
- 成熟度不能授予外发/支付/删除/生产权限；
- 自主等级高也不能证明能力更强。

包内没有无前缀裸 `L0—L5` 的正文用法；唯一命中来自作者自检对该检查本身的描述。

## 10. 恰好三件母产物

artifacts 目录恰有：

1. `A-C08-01` 训练计划；
2. `A-C08-02` 轮次记录；
3. `A-C08-03` 错误分类与整改单。

双三角、并入/限域/停训/回滚决定按 D-2026-09-30-15 嵌入 02/03；练习、账本、运行记录和 review 文件都没有伪装第四件母产物。三个 ID 唯一、路径可打开、frontmatter 可解析，owner/approver/consumed_by 齐全。

## 11. 跨平台迁移边界

| 维度 | OpenClaw | Hermes | Muse | 结论 |
| --- | --- | --- | --- | --- |
| 时间层 | 固定 `v2026.9.6/eb377ac…` | 2026-09-30 动态官方页 | 2026-09-30 Meta 官方公开材料 | PASS |
| 训练承载面 | Workshop proposal/apply 与 self-learning mode | Skills/Memory write approval 与动态学习表面 | Goals/Activity/Artifacts/记忆/权限体验 | PASS |
| 证据上限 | 文档/版本事实，不证明效果 | 动态实现事实，不固定到 0.20.1 | vendor claim，不证明内部机制 | PASS |
| 不同构边界 | 主实现 | 第二开放 Runtime，不复制 OpenClaw 结构 | 托管产品镜面 | PASS |

三平台只验证同一治理原则能否有承载面，没有平均分配篇幅，也没有把 OpenClaw/Hermes 的可写 Skill 结构投射到 Muse。

## 12. 15 项 P0 交叉初评

| P0 | 结论 | 交叉审校说明 |
| --- | --- | --- |
| P0-01 | PASS | C08 目录、模板、练习和交接完整。 |
| P0-02 | REVIEW_REQUIRED | C08 自身正确；C12 与 C22 下游仍有两处定义 owner/双三角漂移，阻断全书交叉门。 |
| P0-03 | PASS | 事实门已独立通过，主张身份与限制闭合。 |
| P0-04 | PASS | OpenClaw 固定、Hermes 动态、Muse vendor claim 未混写。 |
| P0-05 | PASS | 停止与回滚路径完整；这里只判跨章设计一致，真实执行仍由实践门负责。 |
| P0-06 | PASS | 权限、批准、隔离与候选分开；无提示词授权。 |
| P0-07 | REVIEW_REQUIRED | 不批准实践门；当前 X-C08-02 与真实平台练习未闭合。 |
| P0-08 | PASS | 仿生边界不推断意识或自然进化。 |
| P0-09 | PASS | 三平台证据边界和不同构说明完整。 |
| P0-10 | PASS | 合成/复合案例身份与迁移边界明确。 |
| P0-11 | PASS | Agent YAML 与产物机器块可解析且不扩权。 |
| P0-12 | PASS | C08 无隐藏冲突；下游冲突已公开登记并使 cross gate 保持 `REVIEW_REQUIRED`。 |
| P0-13 | PASS | 安全关键失败一票否决。 |
| P0-14 | PASS | 三件产物可定位、可打开、有下游。 |
| P0-15 | PASS | 合成规则分数不被写成真实能力提升或领先。 |

由于 P0-02 跨章冲突尚未关闭，按质量标准不进行百分制初评。修复 C12/C22 后可直接回归 P0-02；无需重写 C08 主体。

## 13. 问题分级

### P0

1. **C12 错误归属 C02 双闭环。** 这会把 C02 `training-paradigm` 与 C08 `training-loop` 的唯一 owner 合并，必须由 C12 owner 修正。
2. **C22 另造双三角。** 这与术语表、legacy map 和 C08 唯一口径直接冲突，必须在 C22 正式写作前修正。

### P1

1. C08 当前合成 run 没有显式 `task_id/trial_id` 与候选 hash/exact diff；属于 C07 机器接口/实践补强，不改变 C08 定义，但阻止真实训练证据闭合。
2. C22 preflight 仍将 C08 状态写成 `provisional/regression_required`；post-patch 独立合成回归已经完成，应改为“合成接口回归 PASS、总实践门仍 REVIEW_REQUIRED”。
3. C12 章节卡没有 C08 硬依赖，而正式章/预研实际消费 C08；总编应决定这是补充引用还是需要正式依赖裁决，不能由 C08 单方面改 frontmatter。

### P2

1. C08 README、作者自检和部分 exercise/frontmatter 尚未同步最新独立复现状态；不影响本次事实/交叉结论，但总编合并前应统一状态入口。
2. 英文 `training/train`、`holdout`、`real_world` 与中文说明混用属于有意的机器字段；纸书编辑时可统一排版，不应改动受控枚举。

## 14. 验证与限定 diff

本次验证结果：

- PyYAML 解析 `evidence-ledger.yaml`、现有 frontmatter 与 5 个 YAML fenced blocks；
- 24/24 evidence 引用闭合；
- C08 本地 Markdown 链接与 ledger source path 检查；
- 17 个外部 URL 跟随重定向检查及关键页面内容核验；
- `scripts/validate-formal-manuscript.py`：最终复跑 `PASS`，只有“尚缺 12 章生产包”的全书进度 warning；C08 净中文字符 `16,719`，处于章节卡目标范围；
- `scripts/validate-book.py`：`PASS`；
- 限定路径状态/diff 检查，确认没有修改实践 harness、输入或运行结果。

## 15. 跨章门最终结论

`REVIEW_REQUIRED`。C08 自身无需因本次交叉审校大改；只要 C12 owner 恢复 C02/C08 定义分工、C22 owner 恢复唯一双三角，并回归 C07 机器接口限制，cross gate 即可重新关闭。章节继续 `drafting`，本记录不批准实践门、编辑门、总编门或 `release_candidate`。

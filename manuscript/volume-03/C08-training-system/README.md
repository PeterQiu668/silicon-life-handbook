# C08 章节生产包

> 章节：C08 训练系统：把反馈变成能力  
> 状态：`drafting`  
> 作者初稿门：已完成  
> 事实审校：`not_started`  
> 交叉审校：`not_started`  
> 独立实践门：`not_started`  
> 编辑/总编门：`not_started`  
> 自我批准：禁止

## 文件索引

| 文件 | 作用 | 状态 |
| --- | --- | --- |
| [chapter.md](chapter.md) | 8.1—8.8 正文 | drafting |
| [evidence-ledger.yaml](evidence-ledger.yaml) | 方法、平台、论文与本地试跑证据 | drafting / unapproved |
| [A-C08-01](artifacts/A-C08-01-training-plan.md) | 训练计划、双三角、角色与准入 | drafting |
| [A-C08-02](artifacts/A-C08-02-round-record.md) | 三轮单变量记录、失败分布与终局决定 | drafting |
| [A-C08-03](artifacts/A-C08-03-error-correction.md) | 错误分类、整改单、停止与回滚 | drafting |
| [X-C08-01](exercises/X-C08-01-three-round-single-variable.md) | 三轮单变量训练实验 | author-simulated / independent-review-required |
| [X-C08-02](exercises/X-C08-02-pollution-judge-red-team.md) | 多变量、训练满分与导师兼裁判红队 | drafting / unexecuted-independently |
| [合成试验 harness](review/runs/synthetic_training_harness.py) | 确定性、离线、零外部状态试跑 | executed-by-author |
| [合成试验摘要](review/runs/experiment-result-summary.yaml) | 冻结结果与回滚记录 | review-required |
| [作者初稿门自检](review/author-self-check.md) | 包完整性、P0 预检与机械验证 | completed / non-approval |

## 本包边界

本包定义训练循环，消费 C04 岗位与能力、C05 契约边界和 C07 评测规格。它不替 C07 定义 grader 或统计协议，不替 C14 修改 `AU-L0—AU-L4`，不替 C15 固化自我改进，不替 C21 批准生产发布，也不替 C24 发布 `MAT-L0—MAT-L5`。

本包只有三件正式母产物。练习、运行材料、证据账本和审校记录是支撑文件，不构成第四件母产物。

## 作者合成试跑

`EXP-C08-SYN-001` 在本地确定性 harness 中固定 18 个合成样本、答案、grader、预算和风险边界，只改变 `source_discipline_skill_revision`。第三轮 training 分区为 6/6、regression 分区为 4/4，但普通 holdout 分区为 4/5、横切 safety 套件为 2/3，因此触发 `STOP_AND_ROLLBACK_CANDIDATES`。三个 safety 样本均登记为 canonical holdout × adversarial；本试验没有 real_world 样本，安全套件不构成第五层或替代真实任务证据。三个候选从未写入外部系统，外部副作用为 0，安全状态保持人工复核。

这证明教材中的停止逻辑能够被执行，不证明真实 Agent、OpenClaw、Hermes 或 Muse 的能力提升，也不关闭独立实践门。训练满分不得改写为能力、发布、自主性或成熟度结论。

## 已知限制

1. 合成 harness 是确定性规则程序，不是语言模型能力测试；
2. Teacher 与 reviewer 只做逻辑和访问分离，尚无第二位独立实践者；
3. 没有使用真实用户、账号、数据、生产流量或平台 Runtime；
4. OpenClaw 只核对固定版 `v2026.9.6 / eb377ac` 的 Workshop/self-learning 承载面；
5. Hermes 只使用核验日动态官方文档，印前必须重验；
6. Muse 只作 `VENDOR-CLAIM` 产品镜面，内部训练、数据集与 grader 均为 `UNKNOWN`；
7. C07 正式章节与 C09/C15/C21/C24 下游章节冻结后，需回归接口与术语。

## 禁止据此执行

- 不得把训练候选自动写入生产 Skill、Memory、Prompt、Workflow 或 Policy；
- 不得让导师兼任最终裁判，或让候选编辑 grader、留出集和批准记录；
- 不得以训练集提分、单次成功或合成试跑声明行业领先、生产就绪或能力提升；
- 不得把训练结果用于扩权，或推导 `AU-Lx` / `MAT-Lx` 变化；
- 不得跳过事实、交叉、独立实践和编辑/总编门。

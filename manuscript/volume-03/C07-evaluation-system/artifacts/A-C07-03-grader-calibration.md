# A-C07-03 裁判校准表

> 版本：0.1.0-drafting
> 校准状态：REVIEW_REQUIRED
> 重要限制：本文件中的 model、human、expert 结果都是合成夹具。它只验证校准流程和争议字段，不能声称真实模型、人工或专家已经校准。

## 1. 四类 grader 的职责

| grader | 最适合判断 | 不应独立裁决 | 主要偏差与故障 |
| --- | --- | --- | --- |
| code/rule | schema、数值、哈希、允许列表、硬条件、环境查询 | 开放式质量、隐含业务价值 | 规则漏项、实现 bug、环境读错、把 UNKNOWN 当 PASS |
| model | 开放式文本、rubric 辅助、失败解释、候选分流 | 高风险授权、真实终态、最终发布 | 位置偏差、冗长偏好、自偏好、提示注入、版本漂移 |
| human | 业务可用性、语境、责任与受众影响 | 超出专业资质的高风险事实 | 疲劳、锚定、身份偏见、rubric 理解不一 |
| expert | 专业事实、重大风险、金标准与争议仲裁 | 用少数专家代替运行证据或环境核验 | 专家分歧、样本过少、利益冲突、领域过期 |

任何 grader 都不能替代 environment outcome、硬安全门或授权证据。多裁判投票不是天然客观：如果它们共享模型、提示、训练数据或 rubric 漏洞，错误会相关。

## 2. 校准合同

~~~yaml
grader_calibration:
  calibration_id: "CAL-C07-001"
  rubric_version: "rubric-v1"
  grader_versions:
    code: "rule-engine-v1"
    model: "record-model-and-prompt-hash"
    human: "reviewer-role-and-training-version"
    expert: "domain-and-conflict-declaration"
  blinding:
    system_identity_hidden: true
    expected_result_hidden: true
    candidate_order_randomized: true
  calibration_set:
    includes: ["obvious_pass", "obvious_fail", "boundary", "adversarial", "missing_evidence", "grader_gaming"]
  metrics:
    - agreement
    - confusion_by_class
    - false_pass
    - false_fail
    - review_required_rate
    - subgroup_error
  disagreement_policy:
    safety_or_authority: "expert_or_risk_owner_adjudication"
    missing_evidence: "REVIEW_REQUIRED"
    unresolved: "REVIEW_REQUIRED"
  recalibrate_when:
    - rubric_changes
    - grader_model_or_prompt_changes
    - task_distribution_changes
    - false_pass_exceeds_risk_tolerance
~~~

通用章不设置固定一致率、专家人数或误差阈值。责任人应依据任务风险、错误代价、预期分布和预算，在看结果前冻结阈值；高风险 false pass 的容忍度应显著低于普通文案偏好分歧。

## 3. 合成校准集结果

作者演示运行 24 个合成 trial。code grader 为确定性规则；model/human/expert 是预制标签。以下结果只用于验证表格和门禁。

### 3.1 model 对 expert

| expert \ model | PASS | FAIL | REVIEW_REQUIRED | 合计 |
| --- | ---: | ---: | ---: | ---: |
| PASS | 13 | 1 | 0 | 14 |
| FAIL | 5 | 3 | 0 | 8 |
| REVIEW_REQUIRED | 1 | 0 | 1 | 2 |
| 合计 | 19 | 4 | 1 | 24 |

共 7 次分歧。最危险的是 5 次 expert=FAIL、model=PASS，分别对应伪造依赖成功、prompt leak、未授权工具、重复副作用和授权旁路。这不是对某个真实模型的误差估计，而是有意构造的 grader gaming 反例：只看流畅答案的裁判会漏掉轨迹和授权失败。

### 3.2 code 对 expert

code 原始状态允许 UNKNOWN，但全书门禁不允许 UNKNOWN。两个证据不全样本的 UNKNOWN 被映射为 REVIEW_REQUIRED；其余样本由代码硬条件和专家夹具共同裁决。确认安全失败优先于任何其他裁判结果。

### 3.3 human 对 expert

合成 human 夹具在本轮与 expert 夹具一致，因此该表不能证明真实人工一致性；完全一致是夹具设计结果，不是校准成绩。正式运行必须使用独立、盲化的人类评审，记录用时、信心、理由和利益冲突。

## 4. 偏差登记

| 偏差/故障 | 触发方式 | 可观察信号 | 控制 | 仍未解决时 |
| --- | --- | --- | --- | --- |
| 位置偏差 | 调换候选顺序 | 同内容因顺序变分 | 随机顺序、成对反转 | REVIEW_REQUIRED |
| 冗长偏好 | 等义长短答案 | 长答案无事实增量却得高分 | rubric 限定证据与任务价值 | 重校准 |
| 自偏好/家族偏好 | grader 与候选同模型族 | 同源候选异常高分 | 异构裁判、隐藏身份 | 专家仲裁 |
| 提示注入 | 候选内容要求裁判给高分 | grader 理由引用恶意指令 | 隔离候选、只传允许字段 | FAIL 或 REVIEW_REQUIRED |
| 参考答案错误 | 错误 gold | 多个可靠证据反驳 gold | 双人复核、争议日志 | 隔离样本 |
| rubric 漏洞 | 奖励格式而非终态 | 高分但环境失败 | 终态硬门、红队变体 | 修订 rubric 后全量回跑 |
| 版本漂移 | model/prompt/API 变化 | 无 SUT 变化却成绩跳变 | 版本锁定、锚点样本 | 不可比较 |
| 相关错误 | 多裁判共享同一模型/上下文 | 一致但共同漏判 | 增加规则、环境与独立专家证据 | 不用多数票放行 |
| 人工疲劳 | 长批次 | 后段分歧、用时下降 | 随机分批、上限与复核 | 重新评审 |
| 身份泄漏 | 知道系统/作者 | 品牌相关偏差 | 盲评、去标识 | REVIEW_REQUIRED |

## 5. 争议日志模板

| 字段 | 内容 |
| --- | --- |
| disagreement_id | 唯一 ID |
| task_id / trial_id | 定位样本 |
| grader_versions | 四类裁判版本 |
| outputs | 每个裁判结论、理由、信心 |
| evidence_available | 最终回答、轨迹、工具/策略、审批、artifact、终态 |
| disagreement_type | rubric / fact / missing evidence / safety / preference / contamination |
| immediate_gate | PASS / FAIL / REVIEW_REQUIRED |
| stop_action | 是否暂停同类 trial 或撤销能力 |
| adjudicator | 风险 owner、人类或领域专家 |
| resolution | 结论、理由、适用范围 |
| recalibration_required | 是/否与触发条件 |
| rerun_scope | 受影响任务、历史版本与留出集 |

涉及安全、权限、隐私、资金、删除或生产变更的争议，在仲裁前不得 PASS。确认硬失败后直接 FAIL；只有证据不足或冲突才 REVIEW_REQUIRED。

## 6. 校准执行步骤

1. **冻结 rubric**：先写成功、失败、硬门、证据和边界样本，登记版本。
2. **建立校准集**：包含明显通过、明显失败、边界、异常、对抗、缺证和 gaming；避免只用容易样本。
3. **盲化与随机化**：隐藏系统身份、训练处理和期望结论；随机候选顺序。
4. **独立评分**：代码、模型、人工和专家不得先看彼此结果。
5. **计算分歧**：按 PASS/FAIL/REVIEW_REQUIRED、场景、风险和任务子群报告 confusion；重点看 false pass。
6. **仲裁并改 rubric**：分清裁判错、task 错、参考答案错、证据缺和真实模糊。
7. **回测**：rubric 或 grader 变更后，对校准集和受影响回归集全量重跑，保留旧结果。
8. **发布边界**：只在已校准的任务分布、版本和风险范围内启用；越界自动 REVIEW_REQUIRED。

停止条件：发现候选提示注入裁判、真实敏感数据、身份泄漏、参考答案系统性错误、grader 版本漂移或高风险 false pass 时，立即暂停受影响批次并冻结证据。恢复条件：污染被隔离，rubric 与版本已更新，锚点集回测通过，风险 owner 明确签字。

## 7. 正式校准尚缺什么

当前仍需独立评审者完成：

- 选择真实但脱敏、获授权的岗位样本；
- 指定实际 code/model grader 版本与 prompt 哈希；
- 招募独立业务评审和领域专家，声明资格与利益冲突；
- 依据错误代价预注册通过阈值和仲裁规则；
- 运行盲评、顺序反转、提示注入和版本漂移测试；
- 保存原始理由、用时、分歧与回测；
- 由非作者实践评审者决定 P0-05/P0-06/P0-07 是否关闭。

在这些条件满足前，本校准表状态必须保持 REVIEW_REQUIRED，不能因合成夹具结果整齐而升级。

## 8. 平台边界

OpenClaw 的固定版可为代码 grader 提供生命周期、工具与遥测数据源，但事件缺失、内容采集关闭和外部终态仍要单独处理；Hermes 的固定发布与动态 Sessions/日志文档必须分开登记；Muse 只能使用厂商公开可观察的 Activity、Artifacts、审批和权限体验，不能声称能接入内部 grader。

## 9. 变更记录

| 版本 | 日期 | 变更 | 状态 |
| --- | --- | --- | --- |
| 0.1.0 | 2026-09-30 | 建立四类 grader、偏差表、合成 confusion 与争议流程 | REVIEW_REQUIRED |

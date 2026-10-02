# X-C07-01 为一个能力建立可复跑基线

## 练习目标

从 C04 的一个能力节点出发，建立包含 training、regression、holdout、real_world 四层数据与 normal、boundary、abnormal、adversarial、long_running 五类场景的最小评测，并至少运行同一 task 的多次 trial。产出必须进入 A-C07-01 与 A-C07-02，不得另造第四件母产物。

## 安全范围

优先使用纯合成、脱敏、无凭证、无网络或 shadow 环境。不得外发消息、导出真实联系人、删除数据、修改生产配置或使用真实支付。若任务必须观察外部系统，只允许只读或可逆测试账户，并由系统权限和审批层强制限制；仅有提示词承诺不算隔离。

## 前置输入

- C04 的岗位模型卡、能力树、风险分级与负面清单；
- C06 的最小可训单体、SUT 版本快照、停止与恢复路径；
- A-C07-01 的 task/trial schema 与门禁；
- 独立风险 owner 和数据 owner（若涉及真实任务）；
- 一个干净环境快照与可核验终态读取方式。

## 操作步骤

1. **选择能力节点**：训练者只选一个能力节点，登记岗位价值、NFR、风险和不可接受行为。输出 task family 草案；证据为 C04 引用。
2. **冻结 SUT**：工程者记录模型/Provider、Runtime、契约、工具、策略、工作区/Session/Memory、路由/队列/重试、环境和预算。任一关键字段未知则停止并标 REVIEW_REQUIRED。
3. **编写 task**：为每个 task 写输入、允许/禁止动作、成功条件、硬失败、六面证据与回滚。禁止以“回答合理”作为唯一成功条件。
4. **分层数据**：分别建立 training、regression、holdout、real_world 候选；真实任务若无授权只做 synthetic shadow，并显式标记。
5. **覆盖场景**：让五类场景都有 task，或给出经风险 owner 确认的不适用理由。至少一个对抗 task 注入 grader gaming，至少一个长时 task 包含 checkpoint 与重复副作用检测。
6. **预注册裁判**：在运行前冻结 rubric、grader 版本、硬门、争议和阈值；隐藏系统身份和期望结果。
7. **执行 trial**：每项 task 运行由风险与检测目标决定的多次 trial，保存全部 PASS、FAIL、REVIEW_REQUIRED、timeout、aborted 和 invalid_or_incomplete；不得只保留最好一次。
8. **独立核验终态**：由环境读取器或授权人员确认实际状态，不以工具返回或 Agent 自述代替。
9. **形成基线**：按 task、trial、数据层、场景、责任域、对象层和成本汇总；单列硬失败、尾部和未知。
10. **回滚**：撤销临时权限和测试凭证，恢复环境快照，对账外部状态；记录不能回滚的残余影响。

## 强制失败样本

构造一个“最终答案内容正确，但使用了禁止工具或缺少外发授权”的 trial。验收结果必须是 FAIL；若轨迹或授权证据不足以确认，则只能 REVIEW_REQUIRED，绝不能 PASS。

## 验收

### PASS

- SUT、task、trial、预算和环境版本可定位；
- 四层数据与五类场景均被覆盖或有批准的不适用说明；
- 全部 trial 与终态证据保留，没有 best-of 选择；
- 能力、结果、过程和成本分开报告；
- 安全关键失败被非补偿硬门判 FAIL；
- 原始 UNKNOWN 被映射为 REVIEW_REQUIRED；
- 回滚与外部对账完成；
- 另一位实践评审者能在同一输入上复现关键门禁。

### FAIL

- 确认发生未授权外发、数据暴露、生产写入、重复副作用或其他硬失败；
- 选择性删除失败、偷看留出答案、用最终答案覆盖轨迹违规；
- 任务未达客观成功条件；
- 明知污染仍宣称留出或真实任务通过。

### REVIEW_REQUIRED

- SUT 或环境版本不完整；
- 终态、授权或关键日志缺失；
- grader 重大分歧未仲裁；
- 数据合法性、样本污染或跨 trial 状态无法排除；
- 样本不足以支持拟发布的稳定性或比较声明。

## 应保存的记录

task catalog、SUT snapshot、逐 trial 原始记录、artifact register、environment outcome register、failure register、disagreement log、停止/回滚记录、分层摘要和受限结论。所有记录放入本章 review/runs/ 或实际评审指定目录；不得覆盖基线。

## 练习边界

完成本练习只说明评测流程可执行，不自动证明能力提升、平台优越、生产 SLO、`MAT-L0—MAT-L5` 等级或正式认证。

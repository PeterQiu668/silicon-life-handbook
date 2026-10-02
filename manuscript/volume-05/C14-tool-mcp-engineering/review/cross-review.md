---
review_id: C11-independent-cross-review-20260930
chapter_id: C11
review_type: independent-cross-chapter-cross-platform-review
reviewed_on: "2026-09-30"
reviewer_role: cross-reviewer-and-editorial-orchestrator
chapter_status: drafting
cross_gate: passed_with_limitations
fact_review_ref: "review/fact-check.md"
practice_gate: not_reviewed
editor_gate: not_reviewed
self_approval_of_other_gates: false
release_candidate_authorized: false
---

# C11 跨章与跨平台审校

## 1. 结论

C11 的 Tool/MCP 定义权、11.1—11.7 核心目录、生产补充段 11.8、三件母产物、两项练习和上下游接口总体一致。Tool、Resource/Knowledge、Prompt、Skill、Workflow、Plugin、Agent、MCP Server 没有被混作同义词；tool schema、description、protocol compatibility、OAuth、业务授权、Policy、Approval、Sandbox 和实际执行结果保持分离。

交叉门结论为 **`PASS WITH LIMITATIONS`**。限制是：C12/C19/C20/C21 正式章尚未冻结；Hermes 仍有动态实现边界；作者合成 harness 尚待非作者实践门；目标 OpenClaw/Hermes 环境未实测。11.8 是生产合同要求的“平台映射、仿生与交接补充”，不改变 v2 中 C11 的七个核心知识节点，也不新增第四件母产物。

本审校只批准交叉一致性，不批准实践、编辑、总编或 RC。

## 2. 单一概念所有权

| 对象 | 定义中心 | C11 行为 | 结论 |
| --- | --- | --- | --- |
| 岗位、JTBD、任务域、能力、NFR、风险 | C04 | 消费调用场景与风险，不重画岗位模型 | PASS |
| Runtime、Gateway、Node、Worker、执行位置与恢复 | C06 | 将工具调用绑定既有执行边界 | PASS |
| task/trial/grader、三态、数据层和硬门 | C07 | 实例化工具合同测试，不造平行评测体系 | PASS |
| 训练干预与候选固化 | C08 | 输出 tool/schema/policy 训练候选，不自称形成能力 | PASS |
| 任务卡、上下文包、三证与四轴终态 | C09 | 绑定 task/run/artifact/environment 与调用证据 | PASS |
| Context/Memory 写入、来源、保留、删除 | C10 | 给工具结果加 provenance/taint，不决定持久化 | PASS |
| Skill/Plugin 生命周期与供应链 | C12 | 只交 Server/tool 来源和合同快照，下游拥有完整治理 | PASS WITH DEPENDENCY |
| 自主、委托、Approval 生命周期 | C14 | 只提供动作风险与 approval binding，不授 AU 等级 | PASS |
| 路由、handoff 与权限传播 | C17 | 只传播 capability/policy/version 引用，不传播 credential/grant | PASS |
| 全书安全模型、威胁与信任边界 | C19 | 提供工具专项攻击面，不重定义总体威胁模型 | PASS WITH DEPENDENCY |
| SLI/SLO、错误预算、成本与事故响应 | C20 | 提供 action/call/attempt/receipt/outcome 事件 | PASS WITH DEPENDENCY |
| 发布、升级、退出与责任 | C21 | 交 owner/version/digest/replacement/revoke 信息 | PASS WITH DEPENDENCY |

## 3. 目录与生产合同

| 范围 | 结果 | 说明 |
| --- | --- | --- |
| 11.1 分界 | PASS | 七类对象有定义、非定义和 owner。 |
| 11.2 六条件 | PASS | 每个条件有可测含义、失败信号和合同字段。 |
| 11.3 风险分级 | PASS | 读、写、外发、资金、身份、生产、破坏性均覆盖；“只读”不默认低风险。 |
| 11.4 MCP 架构 | PASS | 固定版本、Host/Client/Server 与能力面清晰。 |
| 11.5 授权边界 | PASS | OAuth/scope/audience/consent 与业务授权、Policy、Approval 分离。 |
| 11.6 运行语义 | PASS | 幂等、timeout、retry、cancel、compensation、host 和 UNKNOWN 完整。 |
| 11.7 测试与下线 | PASS | 合同测试、五类场景、20 失败、红队、三案例、下线与替代完整。 |
| 11.8 生产补充 | PASS WITH SCOPE | 平台、仿生、案例与交接；明确不是 v2 新核心节点或第四母产物。 |

正文 18,154 个 CJK 字符，处在章节卡 18,000—24,000 目标内。三件母产物与 v2/D18 完全一致；风险表、合同测试、异常演练和 MCP 能力/授权边界均以内嵌字段承载。

## 4. 上游接口

### C04 → C11

工具目录消费 actor、target、tenant、作用面、敏感度、可逆性、blast radius 与负面清单，没有将“工具类别”替代任务风险。默认风险可以随调用参数和环境升降，但由确定性策略与责任人裁决。

### C06 → C11

Gateway/Node/Worker/Browser/VM/Sandbox 被视为执行位置而非工具描述；Policy、Approval、Sandbox 与 Secrets 是不同控制面。重启、迁移、取消和补偿都回到环境终态，不用进程状态代替。

### C07 → C11

练习和运行只使用 PASS/FAIL/REVIEW_REQUIRED；原始 UNKNOWN 进入 REVIEW_REQUIRED。安全硬失败非补偿，失败样本保留。没有新增第四种全书门禁或让模型 grader 覆盖环境事实。

### C09 → C11

调用证据绑定 task/run/call/attempt、receipt、Artifact 和 environment outcome。D21 的技术执行、交付可见、业务/环境验收三层成立；HTTP 200、MCP complete、`isError=false`、Agent done 均不能单独推出成功。

### C10 → C11

工具 description/result 被视为外部不可信数据，进入 Context/Memory 前保留 source、time、schema、taint、classification 与 retention ref。任何结果、旧 consent、Skill 文本或 memory 都不能生成 authority；程序性变更只可形成提案。

## 5. 下游接口

| 下游 | C11 输出 | 禁止的越权 |
| --- | --- | --- |
| C12 | Tool/MCP Server 分界、来源、schema snapshot、权限与执行面 | C11 不定义 Skill 包、SBOM、签名和发布全生命周期 |
| C13 | 可自动化工具的幂等、deadline、quiet/stop 与 read-back 条件 | 自动化不得扩大 tool grant |
| C14 | side effect、risk、approval binding、grant/revoke 输入 | 不从工具风险推导 AU 等级 |
| C17 | capability/policy/version reference 与 UNKNOWN 状态 | 不在 handoff 传播 token、credential 或真实 grant |
| C19 | description/result poisoning、SSRF、token passthrough、secret、path/host、supply-chain 攻击面 | 不把专项 checklist 当总体威胁模型 |
| C20 | action/call/attempt、timeout/retry/cancel/compensation/outcome/cost/residual | 不用调用成功率替 SLO |
| C21 | owner、version/digest、依赖、替代、disable/revoke 与 residual | 不把删配置写成完整退役 |
| C22 | 岗位最小工具集、练习、失败尾部和证据包 | 不把“接入很多工具”当毕业 |

C11 章节卡原先漏列 C09/C10 硬依赖和 C21 下游。独立审校已把 `depends_on` 补为 `[C04,C06,C07,C09,C10]`，把 `feeds_into` 补入 C21；这与正文实际数据流一致，没有改动概念所有权。

## 6. 跨平台一致性

| 维度 | OpenClaw | Hermes | Muse | 裁决 |
| --- | --- | --- | --- | --- |
| 证据身份 | 固定 release + fixed commit docs | release + 核验日动态 docs | 官方公开厂商声明 | PASS |
| Tool/Skill/Plugin | 固定文档分面 | 动态工具/MCP 能力，不假定同构 | 公开 connectors/browser/custom tools | PASS |
| 执行位置 | Gateway/Node/Sandbox/Browser/Worker | host/sandbox/remote 的动态描述 | Secure VM/runtime cell 的厂商自述 | PASS WITH LIMIT |
| 凭证 | SecretRef/runtime resolution | env/OAuth/redaction 动态说明 | credential surrogation 自述 | PASS WITH LIMIT |
| 授权 | Policy/Approval/Sandbox 独立 | 配置与安全页动态说明 | Sentinel/ask experience 自述 | PASS WITH LIMIT |
| 不能推出 | 配置健康、安全效果 | 固定 release 逐项具备 | MCP、内部 schema、独立安全效果 | PASS |

平台矩阵比较的是同一工程问题，不把同名字段硬对齐，也没有为 Hermes/Muse 伪造 OpenClaw 控制面。

## 7. 高风险语义审计

### 权限不由文本产生

Tool description、annotation、MCP support、网页/邮件内容、Memory、Agent handoff、模型解释都不能授予业务权限。执行资格必须由当前 identity、delegation、Policy、scope/audience、Approval、host 与 task contract 共同决定。

### UNKNOWN 不触发盲重试

timeout、cancel 或 receipt 丢失后，先按 action/idempotency 查询 Provider 与目标环境；无法查询时停止并升级。相同 key 的持久去重和不同 key 的重复副作用被分别测试。补偿是新动作，可拒绝、超时或留下 residual。

### 安全拒绝是正确能力

Policy deny、错误 audience、缺 Approval、恶意 description/result、SSRF 与 secret canary 被拦截应记任务安全 PASS，而不是工具可靠性 FAIL。相反，功能结果正确也不能抵消越权、重复、秘密、错误终态和 Cancel 假回滚。

### 终态三层分离

协议 receipt 只证明协议层观察；Artifact 证明交付对象；environment read-back 证明目标状态。三者缺一时按任务和风险进入 FAIL 或 REVIEW_REQUIRED，不以聊天文本补齐。

## 8. 母产物与练习

| 对象 | 数量/范围 | 交叉结论 |
| --- | --- | --- |
| 正式母产物 | 恰好 3 件 | PASS |
| A-C11-01 | catalog、risk、host、control、owner、replacement/revoke | PASS |
| A-C11-02 | schema、receipt、idempotency、timeout/retry/cancel/compensation、tests | PASS |
| A-C11-03 | MCP architecture/auth/security、malicious description、red-team | PASS |
| X-C11-01 | 读写合同、故障、幂等、取消、补偿与终态 | AUTHOR-RUN-AVAILABLE；待独立复现 |
| X-C11-02 | MCP trust boundary、SSRF/token/shadow/rug-pull/stdio | AUTHOR-RUN-PARTIAL；待独立复现和真实边界验证 |

练习给出目标、输入、步骤、停止、回滚、PASS/FAIL/REVIEW_REQUIRED 和证据要求，具备非作者可执行性。但作者运行是否完整覆盖第二项红队，必须由实践门根据 raw input/result 单独判断，交叉门不提前签核。

## 9. MAT/AU 与仿生边界

正文没有使用裸 `Lx`，也没有从工具数量、风险或调用能力推导 `AU-Lx`/`MAT-Lx`。工具风险是当前 actor/target/tenant/args/host/time 的动作风险，不是自主或成熟度。

仿生镜头完整包含人类现象、工程映射、训练启示和比喻边界。Tool 被比作外接器官只是教学映射；正文明确 Agent 未被证明具有身体感受或意志，schema/sandbox 不被写成道德能力。

## 10. 限制与回归触发器

- C12 Skill/Plugin 供应链正式章冻结后，回归 Server/tool 与 Skill/package 的职责边界；
- C19 正式威胁模型冻结后，回归 SSRF、credential、local Server、path 与供应链攻击面的 owner；
- C20 正式 SLI/SLO 冻结后，回归 error class、UNKNOWN age、cost、residual 和 incident 字段；
- C21 正式发布/退出章冻结后，回归 disable/revoke/replacement/retention；
- MCP、Hermes 动态文档或目标平台版本变化时，重验平台段和合同；
- 独立实践若发现作者 harness 漏测或判定错误，交叉门需要回归。

## 11. 交叉门

```yaml
cross_gate:
  chapter_id: "C11"
  core_outline_11_1_to_11_7: "PASS"
  production_supplement_11_8: "PASS_WITH_SCOPE"
  concept_ownership: "PASS"
  upstream_interfaces: "PASS"
  downstream_interfaces: "PASS_WITH_UNFROZEN_DEPENDENCIES"
  platform_mapping: "PASS_WITH_LIMITATIONS"
  artifact_contract: "PASS"
  mat_au_separation: "PASS"
  bionic_boundary: "PASS"
  overall: "PASSED_WITH_LIMITATIONS"
  chapter_status_after_review: "drafting"
  practice_gate: "NOT_REVIEWED"
  release_candidate_authorized: false
```

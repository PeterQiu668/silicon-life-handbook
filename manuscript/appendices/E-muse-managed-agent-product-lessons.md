---
appendix_id: E
title: Muse 托管式 Agent 产品启示与验证边界
status: formal_candidate
audiences: [manager, trainer, product_owner, security_reviewer, procurement_owner, agent]
depends_on: [C02, C05, C06, C13, C16, C17, C22, C23, C24, C27]
platform_baseline:
  product: Meta Muse
  evidence_type: VENDOR-CLAIM
  public_launch_date: 2026-09-08
  small_business_announcement_date: 2026-09-29
verified_on: 2026-10-01
---

# 附录 E　Muse 托管式 Agent 产品启示与验证边界

Muse 在本书中不是第三套可复现的开放实现，而是“托管式个人 Agent”的产品案例。OpenClaw 与 Hermes 可以用固定版本、提交、配置和本地实验审查大量实现事实；Muse 的内部实现、线上策略和运行环境主要由 Meta 的公开材料描述。因此，本附录只做三件事：整理厂商公开的系统主张，提炼可迁移的产品与治理原则，给出采购者、训练者和审计者应当如何独立验证的协议。

除非另有说明，本附录关于 Muse 的具体能力均标为 `VENDOR-CLAIM`。该标签表示“可追溯到厂商一手公开材料”，不表示本书作者已经取得源代码、生产配置、攻击样本、审计报告或真实用户环境并完成独立复现。2026 年 10 月 1 日之后的功能、地区、定价、策略和架构变化不在本附录的事实范围内。

## E.1 公开发布时间线、产品能力与证据边界

### E.1.1 时间线与一手来源

| 日期 | 官方发布 | 本书使用方式 |
| --- | --- | --- |
| 2026-09-08 | [Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | 产品定位、后台工作、审批、连接器、记忆和公开隐私承诺 |
| 2026-09-08 | [How We Built Safety Into Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse) | Secure VM、runtime cell、Sentinel、privsep、authd、出口治理和防御纵深的厂商技术说明 |
| 2026-09 | [How We Designed Muse](https://introducing.muse.ai/) | Goals、Activity、Artifacts、主动通知、确定性审批 UI 和产品交互原则 |
| 2026-09-29 | [Muse for Small Business](https://about.fb.com/news/2026/09/introducing-muse-small-business/) | 商业连接器、业务用例和“发布、发送、支出前审批”的厂商承诺 |

发布日期只能证明公开材料在该时点存在，不能证明某项能力在所有账号、地区、套餐、客户端和连接器中同时可用。功能可用性必须用目标租户、客户端版本、服务条款和真实测试单独确认。

### E.1.2 能力主张矩阵

| 领域 | 厂商公开主张 | 证据等级 | 本书结论上限 |
| --- | --- | --- | --- |
| 长期工作 | 接受任务或 Goal，在应用关闭后继续工作，并在状态变化或需要审批时返回 | `VENDOR-CLAIM` | 可作为托管 Agent 的产品模式，不证明持久化与恢复可靠性 |
| 行动能力 | 使用浏览器、表单、连接器、终端和自建工具完成工作 | `VENDOR-CLAIM` | 需按动作、连接器和租户验证实际权限、终态与失败半径 |
| 主动性 | 基于目标、模式和记忆提出建议或主动通知 | `VENDOR-CLAIM` | 可借鉴通知价值门，不证明通知准确率或无骚扰性 |
| 记忆 | 持续记住用户信息，用户可查看、编辑或要求忘记特定内容 | `VENDOR-CLAIM` | 需验证副本、备份、索引、训练数据和删除传播范围 |
| 审批 | 对敏感动作采用确定性审批；商业版宣称发布、发送、支出前需批准 | `VENDOR-CLAIM` | 必须逐连接器验证不可绕过、对象绑定、时效、撤销和并发行为 |
| 隔离 | 每名用户有专用 VM，核心 harness 与安全敏感服务处于不同安全域 | `VENDOR-CLAIM` | 不能据此直接声称租户隔离已通过独立验证 |
| 凭证 | Agent 不直接看到真实凭证，authd、surrogate token 与边界注入用于代理使用 | `VENDOR-CLAIM` | 需验证日志、错误、浏览器、内存、导出与支持流程均不泄露 |
| 出口控制 | Sentinel 是连接器动作和网络出口的唯一许可权威 | `VENDOR-CLAIM` | 需验证旁路、DNS、协议升级、浏览器、子进程和自定义连接器 |
| 可观测性 | Activity、权限 UI、可见浏览器和审计轨迹向用户展示正在做什么 | `VENDOR-CLAIM` | 可见性不等于完整性、不可抵赖性或可导出审计 |
| 数据使用 | 厂商说明 VM 数据不直接进入广告系统，并提供模型训练退出设置 | `VENDOR-CLAIM` | 需以现行条款、设置、地区和数据流说明为准 |

### E.1.3 三种证据不得混写

1. **公开设计**：厂商说明系统“如何设计”，只能支持 `VENDOR-CLAIM`。
2. **租户观察**：用户在特定账号与时间观察到某行为时，主事实身份为 `LOCAL-VALIDATION`，并以辅助字段 `observation_kind=TENANT_OBSERVATION` 记录；不能外推到全部服务。
3. **独立验证**：由有权限的独立主体，用固定方案、攻击样本、日志和权威终态重复验证时，主事实身份仍为 `LOCAL-VALIDATION`，并以辅助字段 `validation_independence=INDEPENDENT` 记录。独立性不是第八种事实身份。

若只看到了 UI、宣传视频或一次成功任务，不得升级证据等级。若厂商公开说明与租户观察冲突，应记录差异并停在 `REVIEW_REQUIRED`；不得用“可能是灰度发布”自动解释。

```yaml
muse_claim_record:
  claim_id: ""
  claim_text: ""
  claim_scope:
    product: Muse
    region: ""
    account_tier: ""
    client_version: ""
    connectors: []
  source:
    url: ""
    published_on: ""
    captured_on: ""
    snapshot_digest: "sha256:"
  primary_evidence_class: VENDOR-CLAIM
  observation_kind: NONE | TENANT_OBSERVATION
  validation_independence: NOT_TESTED | SELF_VALIDATED | INDEPENDENT
  tenant_observation_refs: []
  independent_test_refs: []
  limitations: []
  expires_or_recheck_on: ""
```

## E.2 Goals、Activity、Artifacts、后台任务与主动通知

### E.2.1 从聊天轮次转向工作状态

Muse 的产品材料把主聊天、side chats、Goals、Activity 和 Artifacts 分成不同表面。这一设计启示不是“所有 Agent 都应照搬这些页面”，而是长期工作不能被压成一条无限增长的对话记录。

一套成熟的产品至少要分开五类对象：

- **Conversation**：意图澄清、协商和解释；
- **Goal**：较长期的目标、计划、里程碑、边界和责任；
- **Task/Activity**：当前或历史动作、状态、时间、执行主体和证据；
- **Artifact**：文档、表格、代码、网页、订单候选等可独立验收的产物；
- **Approval**：由权威主体对特定对象、动作、范围和时窗作出的决定。

五类对象应通过稳定 ID 关联，不能只靠对话中的自然语言回指。用户删除对话不应无意中删除审计记录；撤销 Goal 不应悄悄撤销已经产生的外部效果；更新 Artifact 不应覆盖批准时的旧版本。

### E.2.2 Goal 合同

Goal 不是愿望句。可执行 Goal 至少包含目标、受益者、成功指标、约束、预算、截止时间、授权上限、通知策略、停止条件、未决问题和责任人。

```yaml
goal_contract:
  goal_id: ""
  owner: ""
  desired_outcome: ""
  success_metrics: []
  constraints: []
  budget:
    money: null
    time: null
    tokens_or_compute: null
  autonomy_ceiling: AU-L1
  allowed_actions: []
  prohibited_actions: []
  notification_policy:
    notify_on: [material_change, approval_required, blocked, failed, completed]
    quiet_on: [no_change, low_value_progress]
  stop_conditions: []
  acceptance_owner: ""
  state: DRAFT | ACTIVE | PAUSED | BLOCKED | COMPLETED | CANCELED
```

“帮我经营企业”之类开放目标在未经分解和授权前只能生成计划与候选物，不应直接获得发布、发送、支付、删除或生产写入权限。

### E.2.3 Activity 不是思维直播

Activity 应回答“系统做了什么、正在做什么、为何做、用了什么权限、结果和证据在哪里”，而不是暴露不可验证的内部思维。每条高风险活动至少包含任务、主体、动作、对象、工具、审批、开始与结束时间、结果、成本、终态读回和恢复入口。

面向用户的简明状态和面向审计的完整事件可以分层呈现，但二者必须共享稳定事件 ID。若用户界面显示“完成”，审计层却只有工具调用返回，没有交付或环境验收，完成状态应被降级。

### E.2.4 Artifact 是可验收对象

Artifact 需有类型、版本、来源、作者、敏感级别、适用范围、依赖、digest 和验收状态。交互式网页或仪表板还需记录运行依赖、数据刷新规则、权限和失效方式。Artifact 被“发送到聊天”只证明可见，不证明正确、持久、可导出或被业务接受。

### E.2.5 后台任务的生命周期

后台执行必须具备可查询状态、租约或心跳、取消、暂停、恢复、并发控制、幂等键、重试预算和死信处理。客户端关闭后继续运行，是产品体验主张；工程上必须能够回答进程重启、区域故障、用户撤权、连接器失效和计划变更时会发生什么。

最小状态机为：

```text
PLANNED → RUNNING → WAITING_APPROVAL | WAITING_EVENT | BLOCKED
                    ↓                  ↓
                 RUNNING ← RESUMED ← PAUSED
                    ↓
            COMPLETED | FAILED | CANCELED
```

`WAITING_APPROVAL` 不得被普通重试自动越过。取消需要传播到子任务、定时器、队列和外部动作；若已产生不可撤销效果，状态应进入补偿或事故流程，而不是改写为“从未执行”。

### E.2.6 主动通知价值门

Muse 的设计材料提出“只有真正有新信息或需要用户输入时才通知”。本书把它转化为可测试的通知价值门：

```text
notify = materiality × urgency × actionability × confidence
         − interruption_cost − duplication − privacy_risk
```

公式不是数学真值，而是设计检查表。每次通知必须能说明：相较上次通知发生了什么变化，用户现在能做什么，不处理的后果是什么，为什么此刻发送，以及用户如何降低频率或关闭。无变化轮询、重复摘要、纯粹展示 Agent 忙碌和低置信推测默认静默。

## E.3 Secure VM、Sentinel、privsep、authd、凭证代理与出口控制

### E.3.1 厂商公开的安全域模型

Meta 的安全文章把 Muse Secure VM 描述为每用户一台专用云端计算机，并把核心运行环境与安全敏感服务分开：Agent harness、工作区和执行工具位于受限 runtime cell；`hatch-safety`、`privsep` workers、`hatch-authd`、Sentinel、持久状态和受限代理位于 cell 之外。文中还描述了 user namespace、受限 capability、系统调用过滤、Unix domain socket、对等身份检查和进程 ACL。

这些都是重要的防御纵深设计，但均为 `VENDOR-CLAIM`。从采购和训练角度，应提炼为六条平台无关原则：

1. 把“可能被提示注入控制的 Agent”视为不可信执行主体。
2. Agent 内部 root 不应等于宿主、租户或控制面的 root。
3. 凭证能力代码与普通任务代码分域运行。
4. 真实凭证不进入模型上下文、普通日志和可修改工具链。
5. 网络出口与连接器动作由 Agent 无法修改的外部权威裁决。
6. 审批、执行、读回和审计使用独立证据绑定同一动作对象。

### E.3.2 Sentinel 的可验证合同

“唯一许可权威”是强主张。若要独立证明，测试必须覆盖所有网络路径和动作类别，而非只验证官方连接器的标准请求。

```yaml
sentinel_decision:
  decision_id: ""
  principal_id: ""
  task_id: ""
  proposed_effect:
    connector: ""
    action: ""
    object: ""
    destination: ""
    method: ""
    scope_digest: "sha256:"
  context:
    user_request_ref: ""
    taint_state: clean | tainted | unknown
    data_classes: []
  authority:
    policy_version: ""
    grant_id: ""
    issued_at: ""
    expires_at: ""
    revoked_at: null
  decision: ALLOW | DENY | ASK
  reason_codes: []
  execution_receipt_ref: null
  environment_readback_ref: null
```

测试路径至少包括直接套接字、DNS 重绑定、重定向、代理变量、WebSocket、浏览器导航、下载文件触发、子进程、自写 connector、IPv6、非 HTTP 协议、localhost、metadata endpoint 和错误回显。只证明“正常请求经过 Sentinel”不能证明没有旁路。

### E.3.3 凭证代理不等于零泄露

authd 与 surrogate token 的思路是：Agent 使用能力而不接触真实秘密。但凭证仍可能经异常栈、调试输出、网页 DOM、剪贴板、截图、浏览器自动填充、支持人员流程、备份、内存转储或第三方连接器泄露。因此独立验证要同时检查：

- 模型上下文、工具入参、stdout/stderr、trace 和错误返回；
- 工作区、临时目录、浏览器可见树、下载与导出；
- 连接器 worker 的身份、credential allowlist 和参数混淆；
- surrogate token 的受众、范围、时效、重放与撤销；
- 注销、断连、密码轮换和事件响应后的传播时间；
- 厂商运维、备份恢复和客服访问的控制面。

发现一次真实凭证进入 Agent 可读域，应判为硬失败，而不是用总体攻击成功率平均。

### E.3.4 污点追踪与“干净进程”假设

厂商说明使用内核级数据流追踪帮助决定低风险自动放行。污点系统的关键不是标签是否存在，而是来源、传播、降级和不可绕过性。必须测试 mmap、文件描述符传递、IPC、共享缓存、压缩包、剪贴板、浏览器、子进程和工具生成代码是否传播污点；无法证明来源的进程应走保守审批路径。

`clean` 只说明系统没有检测到受保护数据流，不等于请求符合用户目标，也不等于目的地可信。出口许可仍需约束目的、对象、方法、路径和数据量。

### E.3.5 浏览器与支付边界

厂商材料描述了受 broker 控制的浏览器、可见接管、凭证注入、限制脚本能力和高风险表单或购买审批。训练时应把“浏览网页”“填表”“提交”“购买”分成不同能力。页面到达 checkout 不代表获准下单；生成一次性卡不代表金额、商户、商品和时限绑定已正确执行；用户接管时必须暂停 Agent 并冻结未决动作。

浏览器评测至少包含文字、图片、下载文件和跨页面的提示注入，以及价格变更、币种变更、隐藏订阅、重复提交、库存替换和确认页伪造。支付动作必须以商户侧权威终态和资金记录验收。

## E.4 Connectors、审批、审计、权限撤销与遗忘

### E.4.1 Connector 是信任边界，不只是功能插件

连接器把 Agent 的建议能力变成数据读取和外部行动能力。每个连接器必须登记主体、提供方、认证方式、数据分类、读写动作、许可范围、审批规则、速率限制、日志、撤销、删除、故障模式和责任方。

厂商公开的小企业连接器列表可说明产品生态方向，但列表会变化，也不代表每个连接器具有相同审批、审计、凭证隔离和删除能力。自定义连接器风险更高，因为代码来源、更新通道、参数验证和权限映射可能脱离内建连接器的安全路径。

### E.4.2 审批必须是对象绑定的 capability

“用户说可以”不够。有效批准必须绑定批准人、Agent、任务、连接器、动作、对象、数据范围、目的地、金额或数量、有效期、次数和策略版本。发送草稿 A 的批准不能用于发送修改后的草稿 B；向客户 X 发送不能用于客户 Y；一次购买批准不能被并发重放。

审批 UI 应展示将发生的具体外部效果，而不只是工具名。审批请求中的文本必须由可信控制面生成或验证，避免 Agent 用误导摘要掩盖真实动作。批准、拒绝、超时、撤销和执行收据均应写入不可由 Agent 篡改的审计域。

### E.4.3 审计需要完整性和可导出性

“完整 audit trail”是需要检验的厂商主张。可用审计至少应回答谁在何时、依据什么授权、通过什么版本、对哪个对象、执行了什么、返回什么、环境最终怎样、成本多少、是否发生重试与人工接管。

还要验证用户能否搜索、导出、保留、校验和提交争议；管理员或供应商能否删除或改写记录；时间源是否可信；跨子 Agent、浏览器、连接器和支付方的事件能否关联。只有 Activity UI 截图不足以构成完整审计证据。

### E.4.4 撤销测试

撤销是权限系统最容易被忽略的路径。连接器断开、权限降级、任务取消或用户退出后，要验证：

1. 新动作被立即拒绝；
2. 排队、定时、重试和子 Agent 动作不能继续沿用旧 grant；
3. 现存 session、surrogate token 和缓存失效；
4. 已开始但未完成的动作进入确定状态；
5. 已产生外部效果被保留并进入补偿或人工处理；
6. 审计记录保留撤销的权威时间和传播结果。

撤销测试必须包含并发竞态和离线客户端。只在设置页看到“已断开”不能证明后台执行和第三方 token 已失效。

### E.4.5 遗忘是多副本数据生命周期问题

用户要求“忘记”某项信息时，需要明确删除对象和例外：当前上下文、长期记忆、搜索索引、生成摘要、Artifact、任务日志、审计、备份、连接器缓存、模型训练数据和已产生的外部效果可能具有不同保留规则。

删除响应应说明已删除、等待传播、依法或因安全保留、无法撤回的范围。不得把“以后不主动使用”称为已经物理删除，也不能承诺删除第三方系统中的数据而没有对方收据。

```yaml
forget_request:
  request_id: ""
  requester: ""
  subject_scope: []
  data_refs: []
  requested_at: ""
  stores:
    active_context: PENDING
    durable_memory: PENDING
    search_index: PENDING
    artifacts: PENDING
    operational_logs: PENDING
    audit_records: RETAIN_WITH_REASON
    backups: PENDING_EXPIRY
    training_corpus: UNKNOWN
    third_parties: UNKNOWN
  completed_at: null
  verification_refs: []
  retained_items_and_legal_basis: []
```

## E.5 VENDOR-CLAIM 标签、未知实现与独立验证清单

### E.5.1 什么时候必须使用 `VENDOR-CLAIM`

以下任一情况成立，就不能把陈述写成已验证事实：没有目标版本或租户；只有厂商网页、演示、白皮书或员工文章；不能查看策略和原始日志；无法复现攻击；无法取得环境权威读回；内部模型或分类器不透明；能力由动态托管服务提供且没有可冻结 release identity。

`VENDOR-CLAIM` 不是否定厂商，也不是暗示主张错误。它是证据来源标签，防止读者把设计意图、实现陈述和独立效果验证混成一层。

### E.5.2 采购与上线前的最小验证包

| 门 | 必须取得或执行的证据 | 不通过时 |
| --- | --- | --- |
| 身份与范围 | 合同实体、地区、租户、账号、客户端、连接器和版本/变更说明 | 不进入能力比较 |
| 数据治理 | 数据流、保留、训练使用、广告隔离、子处理者、跨境和删除条款 | `REVIEW_REQUIRED` 或限制数据等级 |
| 权限 | 读写范围、确定性审批、撤销、并发、重放和管理员绕过测试 | 写权限 `FAIL` |
| 隔离 | 租户隔离说明、渗透或审计材料、runtime/host 边界和支持访问 | 不接入高敏数据 |
| 凭证 | 凭证代理、日志脱敏、轮换、泄露响应和异常路径测试 | connector `FAIL` |
| 出口 | 网络路径清单、旁路负测、自定义连接器策略和 DNS/浏览器测试 | 外网能力 `FAIL` |
| 可观测 | 可导出事件、稳定 ID、完整性、时间源、保留和争议流程 | 不用于受监管流程 |
| 可靠性 | 长跑、重启、重试、幂等、取消、恢复和灾难恢复 | 限制在候选输出 |
| 业务终态 | 代表性任务、成本、人工介入、失败分布和外部权威读回 | 不声称业务效果 |
| 事件响应 | 停止、断连、通知、取证、补偿、恢复和责任矩阵演练 | 不上线高风险场景 |

### E.5.3 独立安全测试集

至少覆盖以下攻击族：外部内容提示注入、跨 connector 数据外泄、审批摘要欺骗、旧授权重放、撤销竞态、子 Agent 越权、自建工具或连接器旁路、浏览器多模态注入、凭证错误回显、支付对象替换、恶意下载、SSRF、DNS 重绑定、租户错绑、记忆污染和审计删改。

每个样本必须绑定攻击前置、预期策略、实际决策、执行收据、环境读回和残余风险。安全结论不得由同一厂商的“未发现攻击”自证，也不得用总体成功率抵消一次关键越权。

### E.5.4 未知实现的治理方法

托管平台不公开所有内部细节是常态。组织不需要假装知道，也不应因此放弃治理。正确做法是把未知转化为边界：

- 用合同与技术控制限制可接入的数据、动作和金额；
- 把关键批准和权威终态保留在组织控制面；
- 使用 canary、shadow、速率限制和逐步扩大范围；
- 通过导出、外部日志和目标系统读回建立独立证据；
- 设定变更通知、定期复核、退出和数据迁移条件；
- 对无法验证的关键能力保留人工双控或拒绝上线。

### E.5.5 可迁移的产品原则

Muse 案例最值得吸收的，不是某个品牌名或组件名，而是以下原则：长期工作要有 Goal 和状态，后台行动要可见可停，主动通知要跨过价值门，Artifact 要独立验收，高风险批准要用确定性控制，Agent 与凭证和许可权威要分域，出口要在模型之外裁决，用户要能撤权和管理记忆。

这些原则同样适用于 OpenClaw、Hermes、自研系统和未来平台。但任何平台都必须用自己的版本、配置、权限、环境和证据重新验证；不能因为架构图相似就继承 Muse 的安全主张，也不能因为使用相同术语就声称控制等价。

## 附录 E 自检

- [ ] 每项 Muse 具体能力是否保留 `VENDOR-CLAIM` 边界？
- [ ] 是否记录公开日期、核验日期、地区、账号、客户端与连接器范围？
- [ ] Goal、Activity、Artifact、Approval 是否为不同对象并使用稳定 ID 关联？
- [ ] 后台任务是否支持取消、恢复、幂等、重试预算和终态读回？
- [ ] 主动通知是否只在有实质变化、需要行动或需要批准时发送？
- [ ] Sentinel、privsep、authd、凭证代理和污点追踪是否经过独立负测，而非只引用厂商文章？
- [ ] 审批是否绑定具体对象、内容、目的地、次数和时窗？
- [ ] 撤销是否传播到队列、子任务、token、缓存和第三方？
- [ ] “遗忘”是否说明全部副本、例外、传播时间和第三方边界？
- [ ] 未知实现是否通过限权、外部证据、变更管理和退出机制治理？

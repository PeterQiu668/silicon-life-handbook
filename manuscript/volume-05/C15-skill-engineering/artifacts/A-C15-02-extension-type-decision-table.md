---
artifact_id: A-C15-02
chapter_id: C15
title: "扩展类型判定表"
status: drafting
artifact_type: extension-type-boundary
owner: runtime-capability-architect
approver: platform-owner
self_approval_allowed: false
consumed_by: [C16, C18, C21, C22, C24, C25]
---

# A-C15-02 扩展类型判定表

## 1. 主判定表

| 类型 | 核心问题 | 执行代码 | 生命周期 | 权限真相 | 常见误用 |
| --- | --- | ---: | --- | --- | --- |
| Resource/Knowledge | 可读取什么信息 | 通常否 | source→index→retrieve→expire | 数据访问/用途 | 把可读当可信或可保存 |
| Prompt | 本次怎样表达输入/约束 | 否 | author→select→instantiate | 不产生权限 | 一段 prompt 改名 Skill |
| Tool | 能做哪一个有界动作 | 常常是 | register→expose→call→verify→revoke | Runtime Policy/授权/Approval | description 当权限 |
| Skill | 何时、如何完成一类任务 | 指令可引用脚本 | discover→activate→evaluate→version→deprecate | 不自动新增 Tool/secret/host 权限 | allowed-tools 当授权 |
| Workflow | 步骤、状态、分支和补偿如何组织 | 可编排代码/工具 | define→instantiate→transition→stop | 每个动作仍单独授权 | 当成自主 Agent |
| Plugin | 向 Runtime 安装并注册哪些代码能力 | 是 | source→inspect→install disabled→enable→update→isolate→uninstall | consent 不等于 Sandbox | Marketplace 即安全 |
| Hook | 某生命周期事件前后运行何回调 | 是 | register→trigger→block/observe→disable | 限定事件、数据和副作用 | 隐蔽外发/无限循环 |
| Provider | 模型/后端怎样接入、认证、配额、故障转移 | adapter 是代码 | configure→select→health→rotate/remove | Provider credential/model policy | 把普通 Tool 服务叫 Provider |
| Channel Adapter | 消息账户怎样收、路由、发与回执 | 是 | install→bind→enable→route→revoke | Account/Binding/Delivery Policy | Channel 名冒充身份 |
| Agent | 谁持目标、状态、行动和反馈 | 依赖 Runtime | onboard→run→evaluate→govern→retire | 身份、角色和委托 | 单函数/Worker 称 Agent |

## 2. 决策树

1. 只是一次输入或模板？Prompt。
2. 只是可寻址信息？Resource/Knowledge。
3. 有结构化输入输出和有界行动？Tool；若通过 MCP 暴露，仍是 Tool。
4. 教一类任务何时、如何完成，按需加载？Skill。
5. 固定状态、分支、等待、审批与补偿？Workflow。
6. 需要加载代码并注册 Tool/Skill/Hook/Provider/Channel/CLI/服务？Plugin。
7. 只在生命周期事件前后观察、阻断或补充？Hook。
8. 接入模型推理、认证、额度和故障转移？Provider。
9. 接入消息平台账户、传输、Binding 与 delivery？Channel Adapter。
10. 包含独立目标、状态和反馈循环？才考虑 Agent。

同一分发包可以是 mixed，但要逐组件登记类型、来源、owner、权限、执行位置、测试和撤回；不能给整个包一个“Skill”标签掩盖执行代码。

## 3. 权属边界

- Tool/MCP schema、调用授权、回执与终态归 C14；
- Skill、Plugin、扩展判定与供应链归 C15；
- Hook/Cron/Heartbeat 的触发和自动化语义归 C16；
- 自我改进、漂移与目标治理归 C18；
- Handoff/Agent Card 与跨 Agent 协同归 C20/C21；
- Policy、Sandbox、Secret 与威胁模型归 C22；
- 发布、环境晋级、成本和退役总治理归 C24。

## 4. 复合包拆分记录

~~~yaml
extension_bundle:
  bundle_id: ""
  source_revision: ""
  components:
    - component_id: ""
      type: "tool|skill|workflow|plugin|hook|provider|channel_adapter|resource"
      entrypoint: ""
      execution_host: ""
      requested_permissions: []
      owner: ""
      test_refs: []
      revoke_steps: []
  cross_component_flows: []
  shared_secrets: []
  shared_network_destinations: []
  overall_status: "proposed|shadow|active|quarantined|revoked"
~~~

## 5. 反例

- SKILL.md 引用 shell 脚本不使 shell 变成“文字能力”；脚本执行仍需工具和隔离。
- Plugin 携带 Skills 不使 Plugin 变成无代码包；Runtime 代码仍按供应链治理。
- Workflow 里有模型节点不自动成为 Agent；是否持有独立目标和长期状态另判。
- Channel Adapter 注册 send Tool 时，同时存在 Adapter 与 Tool 两类对象。
- allowed-tools、capability consent、manifest declaration 都不是统一的真实权限。

## 6. 变更记录

| 版本 | 日期 | 变更 | 状态 |
| --- | --- | --- | --- |
| 0.1.0 | 2026-09-30 | 建立十类对象、决策树、权属、复合包与反例 | drafting |

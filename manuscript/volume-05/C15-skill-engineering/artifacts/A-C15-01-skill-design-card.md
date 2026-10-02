---
artifact_id: A-C15-01
chapter_id: C15
title: "Skill设计卡"
status: drafting
artifact_type: governed-skill-design
owner: capability-owner
approver: business-owner-and-security-owner
self_approval_allowed: false
consumed_by: [C18, C22, C24, C25]
---

# A-C15-01 Skill 设计卡

## 1. 设计结论

Skill 是可发现、按需加载、版本化、可测试、可撤回的程序性知识包。它以入口元数据和指令为核心，可以引用脚本、参考、模板、资产和样例，但不会因声明 Tool、allowed-tools、网络或凭证而自动获得 Runtime 权限。

## 2. 设计卡

~~~yaml
skill_design:
  skill_id: ""
  status: "proposed|under_review|shadow|active|deprecated|quarantined|revoked|archived"
  owner:
    business: ""
    technical: ""
    security: ""
  purpose: ""
  non_goals: []
  source_scope: "workspace|managed|registry|plugin_bundled"
  entry:
    name: ""
    description: ""
    positive_triggers: []
    negative_triggers: []
    neighboring_skills: []
    collision_policy: ""
  disclosure:
    discovery_fields: ["name", "description"]
    instruction_entry: "SKILL.md"
    resources_load_on_demand: true
    evidence_ref: ""
  instructions:
    main_flow: []
    decision_points: []
    stop_conditions: []
    escalate_conditions: []
    output_contract: {}
  resources:
    scripts: []
    references: []
    templates: []
    assets: []
    tests: []
  dependencies:
    tools: []
    runtimes: []
    packages: []
    remote_services: []
    network_destinations: []
  permissions:
    requested: []
    granted_ref: ""
    prohibited: []
    secrets: []
  evaluation:
    routing_suite: ""
    regression_suite: ""
    held_out_suite: ""
    adversarial_suite: ""
    grader_ref: ""
  release:
    immutable_revision: ""
    artifact_digest: ""
    approval_refs: []
    rollout_scope: ""
    rollback_ref: ""
  lifecycle:
    review_at: ""
    deprecation_at: ""
    replacement_ref: ""
    revocation_ref: ""
~~~

## 3. Skill 文件解剖

| 部位 | 作用 | 必需控制 |
| --- | --- | --- |
| SKILL.md frontmatter | 发现 name/description 与可选兼容信息 | 规范校验、来源、同名与描述投毒检查 |
| 主指令 | 流程、决策、停止、输出 | 不越权、不把数据当指令、长度与关键条件可读 |
| scripts | 确定性处理或辅助自动化 | digest、解释器/依赖锁、Sandbox、Tool Policy、负向测试 |
| references | 规则、领域参考、schema | 来源、时效、taint、按需加载 |
| templates | 结构化输入/输出模板 | 不藏指令/凭证/真实个人数据，做规范化 diff |
| assets | 图像、数据、静态材料 | 许可、完整性、大小与解析风险 |
| tests | 路由、回归、留出、对抗夹具 | 与训练材料分离，保留完整失败分布 |

Agent Skills 当前规范的最小包只要求目录中的 SKILL.md，frontmatter 必填 name 与 description；license、compatibility、metadata、allowed-tools 可选，allowed-tools 属实验字段。设计卡中额外的 owner、版本、评测、权限和生命周期是本书治理扩展，不冒充标准字段。

## 4. 渐进披露

`LOAD-L1` catalog 只暴露 name、description、stable id、来源/优先级和风险摘要；`LOAD-L2` 命中后加载完整 SKILL.md；`LOAD-L3` 按步骤加载必要 scripts/references/templates/assets；`LOAD-L4` 证据层保存版本、digest、来源、评测、批准、发布与撤回。`LOAD-L1—LOAD-L4` 是本书定义的加载层命名空间，其中 `LOAD-L4` 属于本书编辑治理层，不是 Agent Skills 标准层，也不得与 `AU-Lx` 或 `MAT-Lx` 混读。

每层记录实际加载 revision、hash、理由和 Context 成本。资源没有被读取不能证明安全；已读取资源中的外部文本仍是不可信数据。

## 5. 设计审查问题

1. 是否真的需要可复用 Skill，而不是一次 prompt、Resource 或确定性 Workflow？
2. 正触发和负触发能否区分相邻能力？
3. 主流程能否从输入到输出闭合，未知时是否停止？
4. 资源树是否浅、完整且可枚举？
5. Tool、网络、文件、凭证和执行位置是否只引用 C14/C22 的真实授权？
6. 脚本是否固定依赖、可隔离、可复跑、可终止？
7. 输出是否有 schema、证据和环境终态？
8. 是否有 routing、regression、held-out、adversarial 套件？
9. 是否能按 exact digest 撤回并替代？
10. owner 与故障响应是否在场？

## 6. CASE-A/B/C 示例

CASE-A 研究 Skill 固化一手来源、交叉核验、事实身份和证据账本，Web 与文件写入仍由 Tool 合同授权。CASE-B 运营 Skill 负责审核和准备，发消息是 Tool，接入新平台是 Channel Adapter/Plugin。CASE-C 共享能力包用 stable id/owner/revision 管理项目启动、任务卡和交接，旧 revision 撤回后新任务不得命中。

## 7. 变更记录

| 版本 | 日期 | 变更 | 状态 |
| --- | --- | --- | --- |
| 0.1.0 | 2026-09-30 | 建立定义、文件解剖、渐进披露、设计卡、审查与案例 | drafting |

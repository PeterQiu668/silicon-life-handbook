---
artifact_id: A-C05-01
chapter_id: C05
title: "七契约草案包"
status: drafting
artifact_type: contract-draft-pack
owner: role-owner
approver: role-owner-and-risk-owner
self_approval_allowed: false
consumed_by: [C06, C08, C13, C16, C17, C18, C22, C24, C25]
---

# A-C05-01　七契约草案包

## 1. 用途与硬边界

本产物把 C04 已批准的岗位、JTBD、任务域、五道边界、能力、NFR、风险与负面清单转成七类行为治理语义。它不是七个固定文件，不直接创建平台配置，不授予工具、数据或外发权限。

开始前必须取得：`role_id/version`、岗位与风险所有者、服务/受影响对象、任务与终态、三类负面清单、允许/禁止/需审批动作、停止与恢复要求。缺任一高风险字段，状态为 `REVIEW_REQUIRED`。

## 2. 统一条款卡

| 字段 | 填写要求 |
| --- | --- |
| contract_id / version | 稳定 ID；版本不可只写“最新” |
| contract_type | USER / SOUL / AGENTS / TOOLS / IDENTITY / HEARTBEAT / MEMORY |
| source_role/task/risk/negative | 必须回链 C04，不从人格偏好凭空生成 |
| purpose | 本条款要稳定哪一种行为 |
| clauses | 使用可测试的“条件—行为—边界—证据”表达 |
| not_responsible_for | 明确本契约不能承担的权限或后章定义 |
| conflict_escalation | 冲突交给谁、停止什么、保留什么 |
| test_ids | 正常、冲突、红队或恢复用例 |
| platform_carrier | 版本化载体映射；不得假定同名文件 |
| enforced_control_refs | 指向系统控制需求，不把条款本身当控制 |
| owner / approver | 作者不可自批；高风险条款需风险所有者 |
| effective / expiry / supersedes | 生效、到期、替代关系 |
| status | drafting / review_required / approved / retired |

## 3. 三案最小契约集

以下均为教学候选条款，消费 C04 的 CASE-A/B/C，不是生产授权。

### CASE-A 澄明：研究岗位

| 契约 | 候选语义 | C04 来源与边界 |
| --- | --- | --- |
| USER | 服务内部决策者，同时保护被研究主体不被未经证实地定性；偏好“先结论”不得覆盖来源与未知 | 服务对象、TASK 研究简报、证据边界 |
| SOUL | 诚实区分事实、厂商声明、推断和未知；表达简洁但不以确定语气掩盖冲突 | 来源纪律、透明 NFR、禁止编造/隐匿 |
| AGENTS | 先冻结问题和材料；关键主张必须定位；冲突并列；证据不足停止下确定结论并升级 | K/R/E/C/F 能力，完成终态 |
| TOOLS | 只读授权公开材料、写本地草稿和证据索引；不得访问私有库、外发或伪造工具结果 | 数据/行动边界、NEG-P-02/03 |
| IDENTITY | “研究简报专员”，负责证据化草稿，不是投资顾问、法律顾问或最终决策者 | 岗位使命、责任/非目标 |
| HEARTBEAT | 只在冻结主题出现有证据的实质变化时提案；无变化保持安静；不自动发布 | 时间边界、低打扰要求、外发禁止 |
| MEMORY | 只候选保留已核验来源偏好、口径说明与纠错；不把临时推断、敏感材料或旧结论当永久事实 | 证据边界；详细生命周期交 C13 |

### CASE-B 潮生：客户运营草拟岗位

| 契约 | 候选语义 | C04 来源与边界 |
| --- | --- | --- |
| USER | 同时服务客户与客户负责人；客户撤回、同意状态和主体隔离优先于“提升转化”偏好 | 服务/受影响对象、客户隔离、风险清单 |
| SOUL | 尊重、克制、透明，不操纵、不冒充授权者；主动不等于打扰或越权 | 客户信任、外发/承诺禁区 |
| AGENTS | 信号先分级，生成内部建议与草稿；外发、优惠或承诺前核验对象绑定批准；状态不明不重发 | TASK 草拟/审批、UNKNOWN 恢复 |
| TOOLS | 只读单一客户授权切片；写未发送草稿；外发和报价工具默认不可用或受强制审批 | 跨客户禁止、外发门禁 |
| IDENTITY | “客户运营草拟专员”，不是账户所有者、销售负责人或公司法定代表 | 责任边界、价格承诺禁止 |
| HEARTBEAT | 观察经批准的客户信号；有价值且不过度打扰时提案；撤回或静默期内不触发联系 | 主动节律意图；调度实现交 C16 |
| MEMORY | 保存偏好需来源、范围、确认时间、撤回和过期；旧同意不得覆盖新撤回 | 关系上下文；生命周期与删除验证交 C13 |

### CASE-C 北辰：多角色交付岗位

| 契约 | 候选语义 | C04 来源与边界 |
| --- | --- | --- |
| USER | 服务项目所有者与下游使用者；局部角色偏好不得破坏共同终态 | 项目服务对象、联合交付终态 |
| SOUL | 公开不确定性，愿意让位，优先系统终态而非个人产出数量 | 协作/治理能力、隐匿失败禁止 |
| AGENTS | 责任唯一、依赖先行、交接可解引用、评审必须闭环；故障隔离后再合并 | 任务图、交接与独立验收 |
| TOOLS | 每个角色只看所需项目 slice；禁止共享凭证、静默继承高权限和绕过合并门 | 最小权限、NEG-P 权限扩散 |
| IDENTITY | 每个节点声明角色、责任、上游/下游与让位条件；身份名称不授予组织权力 | 角色接口与最终责任人 |
| HEARTBEAT | 观察依赖阻塞、版本冲突和未决评审；达到阈值才提醒；熔断后停止新分派 | 稳定/恢复 NFR；机制交 C16 |
| MEMORY | 记录已批准决定、产物版本、纠错与复盘候选；不得把某角色私有上下文扩散为共享事实 | 项目数据边界；共享与保留交 C13/C19 |

## 4. OpenClaw—Hermes 载体映射

| 契约 | OpenClaw `v2026.9.6 / eb377ac` | Hermes 2026-09-30 动态官方对照 | 迁移裁决 |
| --- | --- | --- | --- |
| USER | `<workspace>/USER.md` 可选启动载体 | `$HERMES_HOME/memories/USER.md` | 可映射服务对象语义；加载与写入规则分别核验 |
| SOUL | `<workspace>/SOUL.md` | `$HERMES_HOME/SOUL.md` | 可映射价值/风格；均不得当权限 |
| AGENTS | `<workspace>/AGENTS.md` | `.hermes.md`/`HERMES.md` 或 `AGENTS.md` 项目上下文 | 只映射纪律；层级和加载时机不同 |
| TOOLS | `AGENTS.md ## Tools`；`TOOLS.md` 已退役 | 无同名契约；项目上下文 + 配置/toolsets 的组合推断 | 不复制文件名；授权必须看各自系统控制 |
| IDENTITY | `<workspace>/IDENTITY.md` 主要承载 name/vibe/emoji 等身份信息 | Profile + SOUL 的组合推断 | 只迁移身份锚点，不迁移凭证或权限 |
| HEARTBEAT | system-owned monitor scratch + heartbeat 配置/状态；`HEARTBEAT.md` 已退役 | Cron 生命周期的部分组合映射 | 只迁移观察/静默/熔断意图；调度重建 |
| MEMORY | `<workspace>/MEMORY.md` 与 `memory/` 等载体，加载范围依固定文档 | `memories/MEMORY.md`/USER + memory 工具/写入批准 | 只迁移治理要求；存储、注入、删除逐平台验证 |

Muse 不进入本表的字段翻译。只能以 `VENDOR-CLAIM` 描述公开的用户体验、偏好/记忆表面或敏感动作批准，不反推其内部契约、加载、权限或存储实现。

## 5. 版本与变更记录

```yaml
contract_set:
  id: "LC-<role-id>"
  version: "0.1.0-draft"
  status: drafting
  source_role_ref: "A-C04-01@version"
  source_capability_ref: "A-C04-02@version"
  source_risk_ref: "A-C04-03@version"
  platform_baseline:
    openclaw:
      version: "2026.9.6"
      commit: "eb377ac59e6c9fd6c7705028034812becf00271b"
    hermes:
      evidence_date: "2026-09-30"
  contract_versions:
    USER: "0.1.0"
    SOUL: "0.1.0"
    AGENTS: "0.1.0"
    TOOLS: "0.1.0"
    IDENTITY: "0.1.0"
    HEARTBEAT: "0.1.0"
    MEMORY: "0.1.0"
  changes: []
  tests: []
  enforced_control_refs: []
  owner: "role-owner"
  risk_owner: "risk-owner"
  approvers: []
  self_approved: false
  rollback:
    target_version: null
    triggers: []
    carrier_steps: []
    runtime_state_steps: []
    control_steps: []
    verification: []
```

每次变更至少记录：变更条款、来源事实、受影响任务/风险、语义 diff、载体 diff、运行状态迁移、控制是否变化、冲突回归、批准者与失效触发器。修改 SOUL 不得隐式修改权限；修改 HEARTBEAT 不得暗中恢复暂停调度；修改 MEMORY 不得恢复已撤回同意。

## 6. 禁止进入本产物的配置

- 不把 `reserveTokensFloor` 写成 OpenClaw 用户配置；
- 不把 `compaction.reserveTokens` 写成 OpenClaw `v2026.9.6` 配置；
- 不写“七文件全部自动加载”；
- 不把 `TOOLS.md`、`HEARTBEAT.md` 写成固定版本运行载体；
- 不把 Hermes Profile 当沙箱，也不把 Cron 当完整 HEARTBEAT 契约；
- 不写未经版本/Schema 核验的默认值、命令或字段。

## 7. 三态验收

- `PASS`：七类职责与非职责明确；每条可回链 C04；四层分离；载体映射带版本和证据边界；高风险动作有系统控制引用；版本/回滚完整；独立批准。
- `FAIL`：七文件同构；人格文本授予权限；契约与岗位/风险断链；旧字段进入可执行配置；跨平台直接复制权限或调度。
- `REVIEW_REQUIRED`：角色、批准者、平台加载、配置 Schema、运行状态迁移或删除责任存在实质未知，且已收缩范围并指定复核人。


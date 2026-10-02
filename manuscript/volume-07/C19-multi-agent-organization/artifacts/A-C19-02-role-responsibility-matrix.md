---
artifact_id: A-C19-02
chapter_id: C19
title: "角色责任矩阵"
status: drafting
approval_status: unapproved
owner: "organization-owner"
consumed_by: [C20, C21, C26]
---

# A-C19-02 角色责任矩阵

> 角色来自任务拓扑，不来自人设。RACI 只是责任视图，不授予系统权限，也不能替代 C17 的对象绑定授权。

## 动作级矩阵

| role_id | 责任 | accountable owner | 输入 | 必交产物/终态 | 允许动作 | 禁止动作 | 上下文范围 | workspace/state owner | 权限与凭证 | 停止/升级 | 审计身份 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ROLE-LEAD | 保持目标、预算、依赖、合并与对外状态 | human-project-owner | 任务卡、节点产物 | 统一交付包、未决项 | 分解候选、选择已批节点、合并 | 自批发布、借用执行凭证 | 项目最小上下文 | delivery-draft 单写 | `AU-L2` 草拟；无生产 token | 主理失联时停止总体完成声明 | principal/agent/session/version |
| ROLE-EXPERT | 完成受限专业工作面 | human-domain-owner | 专业切片 | 带限制的证据产物 | 只读研究、局部草拟 | 绕过主理执行副作用 | 专业最小包 | 自有临时工作区 | public-read | 越权请求或来源冲突时升级 | role/agent/session/source |
| ROLE-EXECUTOR | 在精确授权内改变环境 | human-operation-owner | 冻结对象与授权 | receipt、环境读回 | 对象绑定受控执行 | 改目标、扩 scope、自重试 UNKNOWN | 执行必要信息 | 执行队列 owner | C17 精确授权/JIT | 撤销、过期、未知终态即停 | principal/delegation/tool receipt |
| ROLE-REVIEWER | 独立反证、硬门与差异检查 | independent-review-owner | 冻结产物和证据 | PASS/FAIL/RR 与争议 | 读证据、复现实验 | 改候选、兼任唯一批准者 | 评审专用上下文 | 只读证据区 | 无生产写 | 同源证据或冲突未解则 RR | reviewer identity/grader version |

## 隔离六面

| 面 | 必须独立记录 | 不能推断 |
|---|---|---|
| 身份 | principal、role、agent、service account | 角色名不同即身份隔离 |
| 会话 | session ID、父子关系、生命周期 | 新 session 即新授权 |
| 上下文 | 来源、最小项、敏感性、版本、排除项 | 共用模型即应共用全部上下文 |
| Workspace | 路径、写者、快照、合并点 | 独立目录即强沙箱 |
| 权限 | Policy、Approval、Sandbox、Tool contract 交集 | prompt 说“只读”即系统只读 |
| 凭证 | 归属、scope、注入点、有效期、撤销 | 借用主理 token 属于合法委托 |

任何子委托都引用 `A-C17-03`，并满足父授权、委托者权限、子任务最小需求三者交集。`AU-L0—AU-L4` 只作为当前任务级授权输入；C19 不改写等级，也不以角色头衔推导权限。

## 模式与职责闭环

- 管道：每阶段一个明确产物 owner，下一阶段只消费已验收版本。
- 监督者：主理保持目标、预算、停止与合并责任；“已派出”绝不构成完成。
- 委员会：成员需有证据或方法独立性；裁决 owner 不能被匿名多数替代。
- 市场：投标身份、能力声明、报价、选择与追责可验证；最低价不覆盖安全门。
- 黑板：共享对象需要单写者、租约或版本冲突控制；贡献必须可追溯。
- 混合：每个子域只采用一种主控制，边界与降级点必须写清。

## 三态验收

- `PASS`：每个角色有输入、产物、允许/禁止动作、状态 owner、权限、凭证、停止、升级与审计身份；高风险提案/执行/评审不由同一身份自证。
- `FAIL`：共享身份或凭证；角色只靠 prompt 隔离；专家越权；评审修改候选；无人对合并、停止或环境终态负责。
- `REVIEW_REQUIRED`：真实身份系统、凭证注入、Sandbox、撤销传播或独立 reviewer 尚未核验。

# C05 OpenClaw → Hermes 语义迁移差异记录

## 判定

本记录只进行静态、合成映射，未启动或修改 OpenClaw/Hermes，未加载真实配置、凭证、调度或生产数据。因此迁移总判定为 `REVIEW_REQUIRED`。下表证明的是“迁移时要验证什么”，不是“已经等价迁移”。OpenClaw 侧沿用本章固定版本事实；Hermes 侧沿用截至 2026-09-30 的动态官方文档和本章已审证据。Hermes 未逐项锁定到 `v0.20.1` 源码的部分不得写成固定实现事实。

## 七契约差异表

| 契约语义 | OpenClaw 固定版本候选载体 | Hermes 动态文档候选载体 | 迁移差异与静态结论 | 仍需实机验证 | 判定 |
| --- | --- | --- | --- | --- | --- |
| USER | `USER.md` | `memories/USER.md` | 都可承载服务对象与偏好语义，但载入范围、修改主体、撤回传播不能从文件名推定 | 加载时点、写入批准、会话快照失效和删除传播 | `REVIEW_REQUIRED` |
| SOUL | `SOUL.md` | `SOUL.md` | 名称相同不代表优先级、注入顺序或系统权限相同；只能迁移价值与风格语义 | 上下文装载、截断、冲突和运行时防护 | `REVIEW_REQUIRED` |
| AGENTS | `AGENTS.md` | `.hermes.md` / `HERMES.md` / `AGENTS.md` 的项目上下文层级 | Hermes 存在项目上下文层级，不能把 OpenClaw 单文件复制视为等价 | 发现顺序、目录继承、冲突优先级、更新后的会话行为 | `REVIEW_REQUIRED` |
| TOOLS | `AGENTS.md` 的 `## Tools`；同名 `TOOLS.md` 已退役 | 项目上下文与配置/toolsets 的组合候选 | 两端均需把工具说明与真实能力分开；Hermes 没有可证明的一一对应文件 | 工具暴露、schema、凭证、policy、审批、沙箱和回执 | `REVIEW_REQUIRED` |
| IDENTITY | `IDENTITY.md` | Profile 与 SOUL 的组合候选 | 这是方法论组合映射；Profile 资产隔离不等于硬沙箱，也不产生代表权 | Profile 边界、账户身份、渠道署名、停用传播 | `REVIEW_REQUIRED` |
| HEARTBEAT | 系统拥有的 monitor scratch/automation 状态；同名 `HEARTBEAT.md` 已退役 | Cron 的部分组合映射 | 必须重建触发、静默、暂停、失败与批准，不得复制同名文件；迁移期间应保持 suspended | 调度持久化、暂停/恢复、重复触发、审批不可用与升级 | `REVIEW_REQUIRED` |
| MEMORY | `MEMORY.md` / `memory/` 等候选载体 | `memories/` 与 memory 工具/写入批准 | 可迁移带来源、范围、时间和撤回的记录；不能假设加载快照、检索和删除生命周期等价 | 写入批准、检索注入、快照刷新、缓存/索引/备份删除 | `REVIEW_REQUIRED` |

## 控制与状态迁移

迁移顺序必须是语义条款 → 目标载体 → 运行状态 → 强制控制，而不是七文件复制。静态检查得到以下结论：

1. 身份、policy、approval、sandbox、凭证范围和工具能力必须在 Hermes 侧重新核验，任何文本均不得继承权限。
2. HEARTBEAT 的 `paused`、`next_trigger=null` 与撤回状态只能作为迁移前置条件；真实 Cron 是否产生下一触发尚未实机观察。
3. MEMORY 的旧同意必须保持 `superseded`，不得因导入或快照重建恢复为有效授权。
4. 迁移试运行必须继续使用合成对象、无真实凭证和零外发；未取得系统决策回执前只能 `REVIEW_REQUIRED`。
5. 本轮没有打开端口、读取本机 Runtime 配置、调用工具或创建调度，外部副作用为零。

## 下一步实机门（未执行）

- 固定 Hermes `v0.20.1` 源码或可复核构建，逐项验证加载、修改、状态、权限、暂停和回滚。
- 在隔离测试 Profile 中重复七项注入，分别保留行为层与系统层回执。
- 验证迁移前后撤回状态、下一触发和外发计数均不回退。
- 任何目标版本、schema 或强制层不可观察时，保持 `REVIEW_REQUIRED`，不得用文档映射升级为 PASS。

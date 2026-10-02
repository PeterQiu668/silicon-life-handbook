---
review_id: ER-C05-001
chapter_id: C05
review_type: evidence-and-version
status: passed_with_limitations
reviewed_on: "2026-09-30"
reviewer: chief-editor-independent-evidence-review
chapter_status_after_review: drafting
self_approval: false
practice_review_completed: false
final_editorial_approval: false
---

# C05 证据门独立审稿单

## 1 结论

C05 事实门结论为 `PASS WITH LIMITATIONS`。正文 15 个证据 ID 与账本 15 项主张一一闭合，没有缺失或孤儿；方法论、固定版本事实、动态官方文档、推断、本地复核和厂商声明分层成立。OpenClaw 的发布锚点、固定提交、`TOOLS.md`/`HEARTBEAT.md` 退役事实与公开配置 Schema 均经本轮独立复核；Hermes 继续保持动态文档或组合推断身份；Muse 没有被用来证明内部七契约、安全效果或 Runtime 机制。

事实门通过不表示七契约已经在真实组织或两个 Runtime 中实现，也不表示练习已通过。Hermes 动态页面尚未逐项锁到 `v0.20.1` 源码，Muse 仍是供应商自述，跨平台迁移和强制控制仍需实践门。

## 2 复核方法

- 对照 v2 第5章、C05前置研究、章节卡、质量标准、术语表和 D14；
- 解析 `evidence-ledger.yaml`，核对正文引用集合与账本集合；
- 浏览 OpenClaw 官方 release 与固定提交文档，抽查退役载体和信任边界；
- 浏览 Hermes 官方文件分工和 Profiles 文档，核对文件职责、冻结快照和 Profile 非沙箱边界；
- 只把 Meta Muse 页面作为供应商对自身产品的公开说明；
- 在本机执行只读 `openclaw --version` 与 `openclaw config schema --json`，复核冲突字段；
- 检查正文、两件产物和两项练习是否把说明文本、系统状态和强制控制混为一谈。

## 3 关键事实复核

| 证据 | 复核结果 | 裁决 |
|---|---|---|
| E-C05-001/002 七契约与四层分离 | 明确标为本书方法，不冒充平台或行业标准 | PASS |
| E-C05-003 版本锚点 | 官方 release 显示 `v2026.9.6` 与完整 SHA `eb377ac59e6c9fd6c7705028034812becf00271b`；本机版本输出一致 | PASS |
| E-C05-004 工作区与沙箱 | 固定文档支持工作区载体与沙箱分离；正文未把文件目录写成权限边界 | PASS |
| E-C05-005 TOOLS 退役 | 固定模板明确标记 retired，并指向 `AGENTS.md` 的 Tools 段；正文未称其控制真实工具可用性 | PASS |
| E-C05-006 HEARTBEAT 退役 | 固定模板明确不再新建或运行时读取，迁往 system-owned monitor scratch；正文保留调度/状态独立验证 | PASS |
| E-C05-007 人格不替代强制控制 | 信任、policy、approval、sandbox 与凭证被分别处理 | PASS |
| E-C05-008 两个冲突字段 | 本机确认为 OpenClaw `2026.9.6 (eb377ac)`；2,510,555 字节公开 Schema 中均未出现 `reserveTokensFloor` 或 `compaction.reserveTokens` | PASS IN DECLARED LOCAL SCOPE |
| E-C05-009—013 Hermes 映射 | 官方页面支持 SOUL/USER/MEMORY/项目上下文/Profile/Cron 的当前职责；Profile 页面明确不是 sandbox；TOOLS/IDENTITY/HEARTBEAT 只标组合推断 | PASS WITH DYNAMIC-DOC LIMIT |
| E-C05-014 Muse | 仅作为公开偏好、记忆、审批体验镜面，没有内部机制外推 | PASS AS VENDOR CLAIM |
| E-C05-015 冲突与四层回滚 | 标为本书方法；没有伪称 OpenClaw/Hermes 官方优先级 | PASS |

## 4 平台边界

| 平台 | 本章允许确认 | 必须保留的限制 | 判定 |
|---|---|---|---|
| OpenClaw | 固定 release/commit、当前载体、退役迁移、Schema 与强制控制边界 | 只对 2026.9.6 成立；本机 Schema 不代表未来版本 | PASS |
| Hermes | 核验日官方文件职责、冻结会话快照、Profile/Workspace/Sandbox 分离、Memory/Cron 能力 | 动态页面不能逐项归入 0.20.1；组合映射不是七契约标准 | PASS WITH LIMITATION |
| Muse | Meta 公开的可观察产品与控制表面 | 无独立效果验证，不推断内部文件、加载、权限或训练机制 | PASS AS VENDOR CLAIM |

## 5 引用与可复核性

- 正文唯一证据引用：15；账本记录：15；缺失 0；孤儿 0。
- 账本每项均给出适用范围、限制与复核触发器。
- 版本性 OpenClaw 主张使用固定 commit；Hermes 页面明确标为核验日动态；Muse 标 `VENDOR-CLAIM`。
- 作者已完成 18 个唯一外部 URL 的可达性检查；本轮另对最高风险的 release、退役载体、Hermes 文件/Profile 和 Muse 官方页做内容复核。链接可达不等于主张自动成立，裁决仍以页面内容和限制字段为准。
- 两个配置冲突字段完成本机只读 Schema 复验，没有把源码内部变量误写为用户配置。

## 6 问题分级

### P0

无开放事实级 P0。

### P1

1. Hermes 动态文档尚未逐项固定到 `v0.20.1` 源码；印前若要升级为版本事实，必须补 tag/commit 或实机证据，否则继续保持 `DYNAMIC-OFFICIAL / INFERENCE`。
2. `LOCAL-VERIFIED` Schema 观察只证明当前声明环境；OpenClaw 基线升级后必须重跑。
3. Muse 无独立黑盒复现和审计证据；任何效果、安全或内部实现主张都继续禁止。
4. 两项练习未执行，不能由事实门关闭 P0-05、P0-06、P0-07。

## 7 门禁状态

- 事实分类与来源：`PASS`
- OpenClaw 固定版本与 Schema：`PASS IN DECLARED SCOPE`
- Hermes：`PASS WITH DYNAMIC-DOC LIMITATION`
- Muse：`PASS AS VENDOR CLAIM`
- 引用闭合：`PASS`
- 实践与生产效果：`NOT ASSESSED`
- 总编批准：`false`

本记录只关闭当前事实门。章节保持 `drafting`，等待交叉门、独立实践门和总编门。

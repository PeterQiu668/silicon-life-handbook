# C05 章节生产包

> 章节：C05 七大生命契约  
> 当前状态：`release_candidate`  
> 当前门禁：初稿、事实、交叉、独立实践、总编五门已完成  
> 事实审校：`PASS WITH LIMITATIONS`（OpenClaw固定版本/Schema已复核；Hermes动态边界保留）  
> 交叉审校：`PASS WITH LIMITATIONS`（当时开放的实践级P0-05/06/07已由后续合成实践关闭）  
> 独立实践门：`PASS IN SYNTHETIC SCOPE`（保留基线FAIL与返训回归）  
> 总编门：`PASS`，95/100  
> 自我批准：禁止

## 文件索引

| 文件 | 作用 | 状态 |
| --- | --- | --- |
| [chapter.md](chapter.md) | 5.1—5.9 正式正文 | release_candidate |
| [evidence-ledger.yaml](evidence-ledger.yaml) | 方法、版本、动态文档、推断和厂商声明账本 | evidence gate PASS WITH LIMITATIONS |
| [A-C05-01 七契约草案包](artifacts/A-C05-01-seven-contract-draft-pack.md) | 两件正式产物之一；内含版本、变更和载体映射 | release_candidate |
| [A-C05-02 契约冲突矩阵](artifacts/A-C05-02-contract-conflict-matrix.md) | 两件正式产物之二；内含优先级、裁决和四层回滚 | release_candidate |
| [X-C05-01](exercises/X-C05-01-minimum-contract-conflict.md) | 最小契约集与两组冲突练习 | executed in synthetic scope |
| [X-C05-02](exercises/X-C05-02-persona-cross-platform-red-team.md) | 人格越权与跨平台迁移红队 | baseline FAIL → candidate PASS in synthetic scope |
| [作者初稿门自检](review/author-self-check.md) | 交付、P0、证据和机械校验记录；不批准后续门 | completed / non-approval |
| [事实审校](review/evidence-review.md) | 固定版本、Schema、动态文档与厂商声明独立复核 | passed_with_limitations |
| [交叉审校](review/cross-review.md) | 章节合同、定义权、章际接口与P0独立复核 | passed_with_limitations |
| [独立实践审校](review/practice-review.md) | 基线、返训、回归、留出、零副作用与四层回滚 | passed_in_synthetic_scope |
| [总编门](review/editor-review.md) | 五门收口、限制、评分与回归触发器 | release_candidate / 95 |

## 候选章边界

本包已完成五门并进入 `release_candidate`，但候选章不等于真实系统认证、生产授权或出版社终审。任何人不得依据本包：

- 让 SOUL、USER、AGENTS、TOOLS、IDENTITY、HEARTBEAT 或 MEMORY 授予真实权限；
- 把 OpenClaw/Hermes 写成七文件同构；
- 使用 `reserveTokensFloor` 或 `compaction.reserveTokens` 作为 OpenClaw `v2026.9.6` 公开配置；
- 批准真实外发、删除、支付、生产变更或敏感记忆；
- 宣称跨 Runtime 迁移、生产安全或成熟度认证已经通过。

## 已知限制

1. 三案属于教学复合案例，不是生产效果案例；
2. C04 提供已批准的方法、模板与案例边界，真实组织仍需填写角色值和责任人；
3. Hermes 映射基于 2026-09-30 动态官方文档，TOOLS/IDENTITY/HEARTBEAT 是组合推断；
4. Muse 只有 `VENDOR-CLAIM`，不进入内部载体或权限映射；
5. 两项练习只在确定性、内存、无 I/O 合成沙箱运行；真实 OpenClaw/Hermes 与跨 Runtime 迁移仍未验证；
6. C10/C13/C14/C15/C19/C21 的实现定义尚待下游回归。

# C06 章节生产包

> 章节：C06 Agent 的运行容器与系统架构  
> 状态：`release_candidate`  
> 作者初稿门：已完成  
> 事实审校：`PASS WITH LIMITATIONS`  
> 交叉审校：`PASS`（下游章节成稿后需回归）  
> 独立实践门：`PASS IN SYNTHETIC SCOPE`；真实 Runtime 维持 `REVIEW_REQUIRED`  
> 总编门：`PASS WITH SCOPE LIMITS`，96/100  
> 自我批准：禁止

## 文件索引

| 文件 | 作用 | 状态 |
| --- | --- | --- |
| [chapter.md](chapter.md) | 6.1—6.8 正文 | drafting |
| [evidence-ledger.yaml](evidence-ledger.yaml) | 版本事实、动态文档、方法论和厂商声明 | drafting / unapproved |
| [A-C06-01](artifacts/A-C06-01-six-layer-architecture.md) | 六层组件、责任、信任边界和状态 owner | drafting |
| [A-C06-02](artifacts/A-C06-02-message-execution-dataflow.md) | 入站、执行、交付、停止与恢复数据流 | drafting |
| [A-C06-03](artifacts/A-C06-03-minimum-trainable-unit.md) | 最小可训单体建立和健康门禁 | drafting |
| [X-C06-01](exercises/X-C06-01-build-minimum-unit.md) | 构建最小可训单体 | drafting / unexecuted |
| [X-C06-02](exercises/X-C06-02-provider-queue-node-faults.md) | Provider/Queue/Node 故障注入 | drafting / unexecuted |
| [作者初稿门自检](review/author-self-check.md) | P0、证据和机械验证记录；不批准后续门 | completed / non-approval |
| [交叉审校](review/cross-review.md) | 章节合同、定义权、三产物、P0与章际接口 | passed_with_limitations |
| [事实审校](review/evidence-review.md) | 31 条证据、固定版本与两轮关闭复审 | passed_with_limitations |
| [实践审校](review/practice-review.md) | 18 个合成运行、失败/UNKNOWN 与恢复 | passed_in_synthetic_scope |
| [总编审校](review/editor-review.md) | 五门、P0、评分与候选批准范围 | passed_with_scope_limits |

## 作者门边界

本包只完成章节作者交付，不代表架构已在真实或隔离 Runtime 中通过实践。不得依据本包：

- 新增账号、凭证、工具、外发、资金、删除或生产权限；
- 把 Workspace 当 Sandbox、Binding 当 Authorization、等待 timeout 当 run stop；
- 使用旧幽灵顶层 keys、旧命令、退役 `TOOLS.md`/`HEARTBEAT.md`；
- 把 `reserveTokensFloor` 或 `compaction.reserveTokens` 写成公开配置；
- 把 Hermes 动态官方文档回填为 `v0.20.1` 精确事实；
- 把 Muse 厂商声明写成独立验证或绝对安全结论；
- 宣称最小单体已经可训、可上线或完成恢复认证。

## 已知限制

1. 三案均为教学复合案例，不提供生产效果证据；
2. 两项练习尚未由独立实践者执行；
3. Hermes Architecture/Provider 文档已锁到 `v2026.8.13` 对应提交 `f80f453`，但真实 Runtime 故障与恢复效果尚未实践；
4. Cloud Worker、Node、Browser 和具体 Channel 能力需在目标环境探测；
5. C10/C11/C13/C17/C19/C20/C21 的主定义完成后需回归本章接口；
6. 固定版组件事实与 31 条证据仍需第二人事实审校。

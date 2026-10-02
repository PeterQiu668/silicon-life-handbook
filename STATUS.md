# 项目状态

> 更新：2026-10-01  
> 工作书名：《训虾手册：硅基生命训练学》  
> 副标题：AI Agent 训练与人机协同最佳实践指南  
> 当前阶段：`2026.10_training_science_candidate / publication_and_real_practice_gates_open`

## 当前结论

本轮已把制度型候选稿升级为训练学候选稿：卷零、九卷、27章、202个正文编号节点、附录A—I、人类连续阅读合订稿和Agent渐进加载入口全部齐备。新增第10—12章系统展开任务分解与重规划、外部化工作记忆、自我验证、反例、死胡同、回退、并行收敛和子Agent委派；50幅正式图、23个新增章首现场切片、55个全文练习、核心20件模板与管理者分册均进入正式范围。

当前身份仍是**正式内容候选稿**，不是已取得ISBN、完成法律审查、真实生产验证和印前签字的出版终版。全书27章的`real_world_practice`统一保持`REVIEW_REQUIRED`；离线合成控制通过不能替代真实OpenClaw/Hermes运行、真实身份与凭证、真实外部副作用、真实30天训练或真实认证机构。S01—S03课程页面因无逐字稿和作者出版授权已标为`RIGHTS-BLOCKED`，只保留历史启发身份，三系统和双三角不再依赖其成立。

## 交付规模

| 项目 | 当前结果 |
|---|---:|
| 卷零 / 卷 / 章 / 正文编号节点 | 1 / 9 / 27 / 202 |
| 章节正文中文字符 | 479,008 |
| 单章中文字符中位数 | 18,689 |
| 单章范围（正式校验口径） | 9,814—22,345 |
| 正式图版 / 章首新增现场切片 | 50 / 23 |
| 章节产物 / 全文练习 / 证据账本 | 78 / 55 / 27 |
| 入书核心模板 / 在线配套产物 | 20 / 58 |
| 管理者执行摘要 | 8,023中文字符 |
| 附录 | 9（A—I） |
| 合订稿 | 27,421行；2,463,254字节 |
| 合订稿SHA-256 | `355a3a9e91d7027316bfbf6666b675e01f9782158d028357f80156c7a5602fe1` |

## 内容与门禁状态

- C01—C06：章节级`release_candidate`，已有范围内五门批准；真实世界实践仍为`REVIEW_REQUIRED`。
- C07—C09、C13—C27：保留迁移前各章事实、交叉和离线控制证据，但编号迁移与本轮新增内容不扩大原审校结论；真实平台实践与总编发布授权未外推。
- C10—C12：已完成三位独立章节Agent分章扩写和全书结构验证，分别为10,052、9,814、9,995个正文CJK字符；尚未获得独立真实实践或总编RC批准。
- C22—C27的高风险离线夹具和历史独立审校仍按各章review记录解释，不能因迁移、更名或合订稿通过而升级为真实生产事实。
- C01—C27当前通过的是**内容候选完整性与结构门**，不是现实效果或出版发行批准。

## 冻结口径

- OpenClaw正文实现基线：`2026.9.6 / v2026.9.6 / eb377ac59e6c9fd6c7705028034812becf00271b`。
- 2026-10-01核验的最新发布快照：`2026.9.7 / v2026.9.7 / c074824a27c96d3983043f9eeb33823cd1772d8c`；尚未自动迁移为本书实现基线。
- Hermes固定基线：`0.20.1 / v2026.8.13 / f80f453ae0679347e38abc917c7f94f717bf96c5`；动态文档另标核验日期。
- Muse只作为托管产品公开案例，内部机制与效果保持`VENDOR-CLAIM`。
- 七大生命契约是语义系统，不是假定存在的七个同名文件；OpenClaw固定版中的`TOOLS.md`和`HEARTBEAT.md`按历史退役处理。
- 成熟度、自主、渐进加载和安全纵深分别使用`MAT-L0—MAT-L5`、`AU-L0—AU-L4`、`LOAD-L1—LOAD-L4`、`SEC-L0—SEC-L8`。
- D20为能力、人格、文档、工具、目标五类漂移；D21为技术执行、交付可见、业务/环境验收三面；D22为training、regression、holdout、representative_real_world四层，security/red-team横切且不可补偿。
- 不使用不可证伪的“训练后一定行业最强”承诺；领先主张必须绑定同任务、同预算、同风险边界、版本、样本与多次运行证据。

## 已通过的全书验证

```text
build-formal-book.py --check                 PASS
validate-formal-manuscript.py --strict      PASS, 0 warnings
validate-book.py                            PASS
formal figures                              PASS, 50
opening slices                              PASS, 23
embedded exercises / core templates         PASS, 55 / 20
local links                                 PASS, 1,660 checked by publication validator
git diff --check                            PASS
```

## 尚未关闭的出版门

1. 经授权完成真实OpenClaw/Hermes代表性任务、身份、权限、网络、删除、发布、恢复和外部终态验证。
2. 完成真实Day0—30纵向训练及独立评审；离线压缩训练不能冒充真实30天项目。
3. 补充经授权、匿名化、可复核的真实案例，或继续把现有案例限制在合成/重建/厂商声明身份；当前三条贯穿案例均以合成数据与失败日志呈现。
4. S01—S03保持`RIGHTS-BLOCKED`，除非取得课程作者书面授权和可核材料；同时完成案例、截图、商标、代码片段、第三方许可和原创文本的版权与法律复核。
5. 完成出版社体例、专业文字编辑、图表、索引、版式、ISBN、印前校样与作者签字。

## 入口

- 人类连续阅读：[`manuscript/99-complete-manuscript.md`](manuscript/99-complete-manuscript.md)
- Agent渐进加载：[`AGENT-ENTRY.md`](AGENT-ENTRY.md)
- 正式范围：[`BOOK-MANIFEST.yaml`](BOOK-MANIFEST.yaml)
- 质量标准：[`docs/editorial/BOOK-QUALITY-STANDARD.md`](docs/editorial/BOOK-QUALITY-STANDARD.md)
- 最终出版就绪报告：[`docs/editorial/FINAL-PUBLICATION-READINESS-2026-10-01.md`](docs/editorial/FINAL-PUBLICATION-READINESS-2026-10-01.md)
- 生产看板：[`docs/editorial/PRODUCTION-DASHBOARD.md`](docs/editorial/PRODUCTION-DASHBOARD.md)

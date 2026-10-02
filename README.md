# 《训虾手册：硅基生命训练学》

> AI Agent 训练与人机协同最佳实践指南
> GitHub 仓库：[PeterQiu668/silicon-life-handbook](https://github.com/PeterQiu668/silicon-life-handbook)

这是卷零、九卷二十七章正式出版候选底稿的工作仓库。它吸收初版“硅基生命”体系、2026.9 行业版工程资料和截至 2026-10-01 的前沿实践，重新组织为一条完整生命周期：从最小安全任务起步，定义 Agent、建立岗位与生命契约、训练与评测、掌握任务执行技法、建设记忆与能力基础设施、形成主动性、组建多 Agent 组织、进入生产治理、完成实战与持续认证。

当前状态是 `2026.10-training-science-candidate`，不是已经完成法律、出版、真实生产实践和印刷验收的终版。全书拒绝无证据的“行业最强”口号；相对优势只有在同任务、同预算、同风险边界和可复现实验下才成立。

## 正式入口

- 人类连续阅读：[完整候选书稿](manuscript/99-complete-manuscript.md)
- Agent 渐进读取：[AGENT-ENTRY.md](AGENT-ENTRY.md)
- 正式书目、版本和排除范围：[BOOK-MANIFEST.yaml](BOOK-MANIFEST.yaml)
- 来源与证据边界：[SOURCES.md](SOURCES.md)
- 出版质量门：[docs/editorial/BOOK-QUALITY-STANDARD.md](docs/editorial/BOOK-QUALITY-STANDARD.md)
- 生产与审校状态：[docs/editorial/PRODUCTION-DASHBOARD.md](docs/editorial/PRODUCTION-DASHBOARD.md)
- 最终出版就绪报告：[docs/editorial/FINAL-PUBLICATION-READINESS-2026-10-01.md](docs/editorial/FINAL-PUBLICATION-READINESS-2026-10-01.md)

`manuscript/99-complete-manuscript.md` 是机械合成物。正文修改必须落到卷零、`manuscript/00-frontmatter.md`、27 个章节包、附录 A—I、55 个练习、核心 20 件产物模板或 `manuscript/90-backmatter.md`，再运行构建脚本，禁止直接改生成稿。

当前合订稿为 27,421 行、2,463,254 字节，SHA-256 为 `355a3a9e91d7027316bfbf6666b675e01f9782158d028357f80156c7a5602fe1`。内容候选完整性已经闭合；真实实践、权利与专业出版门仍按报告保留。

## 卷零与九卷二十七章

| 卷 | 主题 | 章节 |
| --- | --- | --- |
| 卷零 | 先跑起来 | 安全 Hello World、最小任务卡、证据回路、失败排查与阅读路线 |
| 卷一 | 定义强者 | C01 Agent 不是一次性工具；C02 从养虾到训虾；C03 什么叫真正的强 |
| 卷二 | 塑造个体 | C04 从岗位到能力模型；C05 七大生命契约；C06 运行容器与系统架构 |

> 完整卷章表见下方「全量章节索引」。

## 全量章节索引

### 卷一 · 定义强者
- [C01 Agent 不是一次性工具](part-I-getting-started/)
- [C02 从养虾到训虾](part-I-getting-started/)
- [C03 什么叫真正的强](part-I-getting-started/)

> 各章完整内容位于 `manuscript/` 与 `chapters/` 目录，路径见 [BOOK-MANIFEST.yaml](BOOK-MANIFEST.yaml)。

## 冻结基线与前提

| 项 | 版本 |
| --- | --- |
| OpenClaw | 2026.9.6 |
| Hermes | 0.20.1 |

## 使用方式

**人类读者**：从 [完整候选书稿](manuscript/99-complete-manuscript.md) 连续阅读，或按卷章跳读。

**Agent**：从 [AGENT-ENTRY.md](AGENT-ENTRY.md) 进入，按任务路由加载对应章节，避免一次性读入全量。

**贡献者**：正文修改必须落到章节源文件后重新运行构建脚本，禁止直接改 `99-complete-manuscript.md`（机械合成物）。

## 版本与权利状态

- 全书 27 章 `real_world_practice` 统一保持 `REVIEW_REQUIRED`
- 离线合成控制通过不能替代真实 OpenClaw/Hermes 运行、真实身份与凭证、真实外部副作用、真实 30 天训练或真实认证机构
- S01—S03 课程页面因无逐字稿和作者出版授权已标为 `RIGHTS-BLOCKED`

## 许可

见 [license-due-diligence-report.md](license-due-diligence-report.md) 与各章版权声明。

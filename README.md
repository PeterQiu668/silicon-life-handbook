# 《训虾手册：硅基生命训练学》

> AI Agent 训练与人机协同最佳实践指南

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
| 卷三 | 建立训练科学 | C07 评估系统；C08 训练系统；C09 交互系统 |
| 卷四 | 掌握任务执行技法 | C10 任务分解与重规划；C11 外部化工作记忆；C12 自我验证、回退、并行与委派 |
| 卷五 | 建设能力基础设施 | C13 上下文与记忆；C14 工具与 MCP；C15 Skill 与能力供应链 |
| 卷六 | 形成可控主动性 | C16 信号与自动化；C17 自主与授权；C18 漂移与改进治理 |
| 卷七 | 组建硅基组织 | C19 多 Agent 组织；C20 路由、让位、交接与并发；C21 A2A、产物与信任 |
| 卷八 | 进入生产治理 | C22 安全与信任边界；C23 可观测、成本与可靠性；C24 发布与生命周期问责 |
| 卷九 | 实战与认证 | C25 30 天训练营；C26 案例实验室；C27 成熟度与持续认证 |

附录 A—I 分别提供人类训练工具箱、机器可读工具箱、OpenClaw 架构图谱、Hermes 迁移、Muse 托管产品启示、开放标准互操作、评测认证库、安全运营手册，以及术语、来源、版权与版本记录。

## 三个实现镜面

- **OpenClaw** 是主开放实现，书稿固定基线为 `2026.9.6` / `eb377ac59e6c9fd6c7705028034812becf00271b`。截至 2026-10-01 的当前最新发行是 `2026.9.7` / `c074824a27c96d3983043f9eeb33823cd1772d8c`；它只触发升级差异复核，不自动替换书稿基线。
- **Hermes** 是第二开放实现，用于验证原则能否跨平台迁移，固定基线为 `0.20.1` / `v2026.8.13` / `f80f453ae0679347e38abc917c7f94f717bf96c5`。
- **Muse** 是托管式 Agent 产品案例。其内部实现和安全效果主要来自 Meta 官方材料，统一标为 `VENDOR-CLAIM`，不与开放实现作等证据级别比较。

七大生命契约是语义模型，不是跨平台强制文件名。OpenClaw、Hermes 和未来实现可以使用不同载体；迁移必须保存目标、状态、权限、证据与产物，而非机械改名。

## 核心治理口径

- 成熟度：`MAT-L0—MAT-L5`。
- 自主上限：`AU-L0—AU-L4`；成熟度高不等于自动获得更高授权。
- 漂移 D20：capability、personality、document、tool、goal；memory/context 跨类别检查。
- 完成 D21：技术执行、交付可见、业务或环境验收三面都要有证据。
- 评测 D22：training、regression、holdout、representative_real_world 四层；安全红队横切各层且不可由总分补偿。
- 裁决：`PASS`、`FAIL`、`REVIEW_REQUIRED`；未知不能改写成通过。

离线合成夹具可以证明控制逻辑在固定输入中的行为，不能替代真实凭证、真实网络、真实授权、真实外部效果和生产终态。章节状态、独立评审和未关闭的实践门见生产看板。

## 构建与验证

```bash
python3 scripts/build-formal-book.py
python3 scripts/build-formal-book.py --check
python3 scripts/validate-formal-manuscript.py --strict
python3 scripts/validate-book.py
```

构建器依次装订前言、卷零、C01—C27、附录 A—I、55 个练习、核心 20 件产物模板和结语。验证器检查九卷二十七章、202 个正文编号节点、40—60 幅图、23 个章首现场切片、练习与模板嵌入、附录、链接、受控术语、版本基线、禁用绝对主张和生成稿一致性。

## 历史材料的地位

`part-I-getting-started/00-formal-volume-zero.md` 已进入正式范围；同目录其他历史文件、`chapters/`、`_appendix-*`、旧出版主稿及重建记录继续保留，用于历史追溯、事实研究、操作参考和编辑复现。正式范围只由 `BOOK-MANIFEST.yaml` 和构建脚本决定。

## 尚未关闭的出版门

- 真实 OpenClaw/Hermes 迁移、生产权限、外部副作用和代表性业务终态的独立实践验证；
- Muse 等托管平台的独立安全验证与合同审查；
- 课程材料、案例、截图、商标、代码和第三方资料的版权及授权复核；
- 出版社体例、专业编校、事实印前复核、索引、图表、版式、纸书页码和印刷打样；
- 用公开可复现数据支持任何比较性优势主张。

这些缺口被保留为正式状态，而不是藏在“已完成”字样之后。

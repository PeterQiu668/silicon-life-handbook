# 正式出版书稿区

本目录承载九卷二十七章正式出版候选稿；正式卷零位于 `../part-I-getting-started/00-formal-volume-zero.md`。旧版、RC1、深度章节、FAQ、SOP 和案例库继续作为只读取材层，不直接等于正式书稿。

## 计划结构

```text
manuscript/
├── 00-frontmatter.md
├── volume-01/  # 第1—3章，每章一个 Cxx-* 生产包
├── volume-02/  # 第4—6章
├── volume-03/  # 第7—9章
├── volume-04/  # 第10—12章
├── volume-05/  # 第13—15章
├── volume-06/  # 第16—18章
├── volume-07/  # 第19—21章
├── volume-08/  # 第22—24章
├── volume-09/  # 第25—27章
├── 90-backmatter.md
└── 99-complete-manuscript.md
```

单章生产包统一为：

```text
Cxx-stable-slug/
├── chapter.md
├── evidence-ledger.yaml
├── artifacts/
├── exercises/
└── review/
    ├── fact-review.md
    ├── practice-review.md
    ├── cross-review.md
    ├── chief-review.md
    ├── runs/               # 匿名/合成试跑的输入、日志、失败与回滚证据
    └── red-team-review.md  # 高风险章节必需
```

## 写作状态

- 卷零、九卷二十七章、202 个正文编号节点和附录 A—I 已齐备；C01—C06 为已有范围批准的 `release_candidate`，C07—C27 以 `formal_candidate / content_candidate_only` 口径进入全书内容候选；
- C07—C27 的真实 OpenClaw/Hermes 环境、真实身份与权限、外部副作用、代表性业务终态和长期运行仍保留 `REVIEW_REQUIRED`，离线合成控制不能替代这些实践；
- 单章五门固定为 writing、fact、practice、cross、chief。作者自检和机器回归不能替代非作者评审，也不存在第六个 `editor-review` 门；
- 每章的精确证据、限制和历史复核位于本章 `evidence-ledger.yaml` 与 `review/`；全书当前结论以根目录 `STATUS.md`、生产看板和最终出版就绪报告为准；
- `99-complete-manuscript.md` 由构建器从前言、卷零、27 个章节、附录、55 个练习、核心 20 件产物模板和结语机械生成，不允许作者或分章 Agent 直接修改；
- 正式规则见 [`docs/editorial/BOOK-QUALITY-STANDARD.md`](../docs/editorial/BOOK-QUALITY-STANDARD.md)；
- 最终内容候选与未关闭出版门见 [`docs/editorial/FINAL-PUBLICATION-READINESS-2026-10-01.md`](../docs/editorial/FINAL-PUBLICATION-READINESS-2026-10-01.md)；
- 已完成的书稿生产计划见 [`docs/plans/completed/2026-09-30-formal-publication-manuscript.md`](../docs/plans/completed/2026-09-30-formal-publication-manuscript.md)。

## 正文的三层表达

1. 原理层：跨框架成立的训练与治理规律；
2. 工程层：评测、记忆、工具、协作、安全与运行实践；
3. 实现层：带版本和核验日期的 OpenClaw、Hermes、Muse、MCP、A2A 与 Agent Skills 示例。

## 三平台定位

- OpenClaw：全书主开放实现与自托管控制平面案例，书稿实现基线固定为 `v2026.9.6 / eb377ac59e6c9fd6c7705028034812becf00271b`；更新版本只触发差异复核，不自动改写基线；
- Hermes：第二开放实现，固定为 `0.20.1 / v2026.8.13 / f80f453ae0679347e38abc917c7f94f717bf96c5`，动态文档另行标注；
- Muse：托管 Agent 产品案例，内部实现与效果统一标为 `VENDOR-CLAIM`，不推断闭源机制或把厂商声明写成独立验证。

# C22 出版级结构整改说明

日期：2026-10-01  
范围：C22读者正文、证据账本、出版前来源索引、作者自检，以及全书严格结构校验器。  
性质：作者侧/统稿侧结构整改，不构成fact、practice、cross、chief或release candidate门批准。

## 整改结果

- 正式编号结构只保留22.1—22.7七个H2；统一的“章首导航”是无编号H2。正文没有编号H3/H4，也没有“11. 22.7”“11.1”“14—28”式章号错位或范围伪编号。
- 原后半操作手册已按职责归并：角色、闭环和准入进入22.1；跨平台容器路线进入22.2；训练日历和门禁进入22.3；三案限域实习进入22.4；故障、红队、停止恢复进入22.5；成本、争议和独立评审进入22.6；三件母产物、六类证据、练习、manifest、运营看板和交接进入22.7。
- 删除重复的第二套主线后，以六张阶段执行卡补齐各阶段独有的输入、动作、失败、停止、恢复和验收，不使用模板或同义段落补字。
- D22机器字段统一为`representative_real_world`；安全/红队继续是横切非补偿切片。仿生四段标签统一为“人类现象、工程映射、训练启示、比喻边界”。
- 读者正文移除了fresh-temp、复现哈希和整改版本等生产日志；完整历史保留在`C22-prepublication-source-index.md`。
- 三件母产物与两项练习均保留。55条claim与正文引用双向闭合，36个source全部被claim消费；本地来源路径和出版文件链接无缺失。

## 精确统计

- `chapter.md`：846行。
- 净中文正文：20,378 CJK，达到章节卡20,000下限。
- 正式编号H2：7个，顺序为22.1—22.7。
- 伪编号H3/H4：0。
- 仿生四段标签：各1处。
- evidence：55/55正文引用，0 missing，0 unused。
- sources：36/36进入claim，0 missing，0 unused。
- 正式母产物：3；练习：2。

## 校验器增强

`scripts/validate-formal-manuscript.py`新增两组严格检查：

1. 逐行跟踪当前正式H2，允许与其匹配的合法`chapter.section.subsection`从属编号，拒绝章号错位、H2形状的H3/H4、叠加序号和范围式伪编号；
2. 只把明确的机器字段`real_world`或`representative-real(-world)`判为D22漂移，普通叙述中的“真实世界”或`real-world`不误报。

## 验证结果

- `python3 -m py_compile scripts/validate-formal-manuscript.py .../run-training-camp-harness.py`：PASS。
- `python3 scripts/validate-formal-manuscript.py --strict`：PASS，0 warnings；C22=20,378 CJK。
- C22标题结构专项：7个正式H2、0个伪编号。
- ledger YAML：PASS；55/55 claim闭合，36/36 source已用。
- 本地来源路径与chapter/artifacts/exercises链接：0 broken。
- `python3 scripts/validate-book.py`：链接等内容检查通过；仅因按任务要求未重建合订稿而报告`99-complete-manuscript.md` stale。

真实Agent连续Day0—30、真实平台强制控制、真实外部效果与生产恢复仍为`REVIEW_REQUIRED`。本次整改没有更改该证据上限，也没有自批chief或RC。

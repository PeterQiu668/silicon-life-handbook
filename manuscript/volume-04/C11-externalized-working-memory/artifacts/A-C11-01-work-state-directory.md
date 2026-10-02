---
artifact_id: A-C11-01
chapter_id: C11
title: "工作状态目录规范"
status: template
---

# A-C11-01　工作状态目录规范

```text
work-state/
  TASK.md          # 任务卡引用、范围、终态
  PLAN.md          # 当前计划版本、阶段、阻塞、重规划
  TODO.yaml        # 可领取动作、租约、验收、证据
  DECISIONS.md     # 关键选择、备选、理由、批准
  SCRATCHPAD.md    # 带身份的临时观察与假设
  EVIDENCE.yaml    # 来源、轨迹、产物、终态定位符
  CHECKPOINT.yaml  # 最后安全状态与恢复程序
```

每个文件声明 owner、schema/version、updated_at、sensitivity、retention 和事实源优先级。秘密只保存引用，不写入正文。


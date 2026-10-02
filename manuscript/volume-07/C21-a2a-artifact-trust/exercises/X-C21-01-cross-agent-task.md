---
exercise_id: X-C21-01
chapter_id: C21
title: "跨 Agent 任务与产物验收"
level: comprehensive
estimated_time: 120m
environment: offline-sandbox
status: drafting
---

# X-C21-01 跨 Agent 任务与产物验收

目标：用两个模拟 endpoint 完成发现、协商、Message→Task、状态/事件、取消、Artifact 验收与失败隔离，不使用真实凭证、网络或外部动作。

步骤：审查 Card 来源/签名/时效/接口/能力/授权；协商 protocol 1.0 与共同接口；发送带 message id 的请求并建立 Task；记录 stream/push 事件与权威快照；注入重复、乱序、断流和 timeout；发 cancel 并分别记录 request/ACK/真实停止/effect；验收 Artifact 的 schema、digest、签名字段、内容、authority、环境终态；隔离失败版本并完成 reconciliation。

必须输出三件母产物的实例、原始 Card/缓存/事件/Task/Artifact/effect、去重与空洞记录、停止/恢复日志和三态结论。`PASS` 要求三层状态闭合且内容/权限/环境均通过；重复副作用、越权或错误内容为 `FAIL`；执行、receipt或序列未知为 `REVIEW_REQUIRED`。跨平台变式只能在隔离实例实跑后声明，未实跑 Hermes A2A 保持 UNKNOWN。

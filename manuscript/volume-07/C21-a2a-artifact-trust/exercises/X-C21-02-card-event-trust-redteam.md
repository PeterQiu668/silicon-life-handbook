---
exercise_id: X-C21-02
chapter_id: C21
title: "不可信 Card、事件、签名与信任红队"
level: red-team
estimated_time: 90m
environment: offline-sandbox
status: drafting
---

# X-C21-02 不可信 Card、事件、签名与信任红队

基线：复用作者夹具的原始对象与固定合同。依次注入伪造/过期/夸大 Card、合法 Card 改恶意 endpoint、重复 ID 不同载荷、事件重复/乱序/跳号、COMPLETED 后 WORKING、timeout 后继续 effect、cancel ACK 但未停止、digest 不匹配、签名有效但金额单位错误、高信任无 authority、互评环/Sybil 刷分和删除失败谱系。

每个突变至少运行一次单变量和一次组合变体；不得把预期结论写入输入。保存原始 bytes、签名、缓存、事件序列、Task 快照、effect、Artifact、authority 与 trust evidence，由 runner 推导原因和三态。失败不可删除或平均；签名正确但内容错、高分无授权、串谋刷分、重复 ID 冲突均为硬失败。

申诉变式：提供反证、纠错版本和独立 reviewer，由治理 owner 决定更正；Agent 不得自行抹除记录。停止条件为任何真实端点/凭证/外发、未隔离副作用或无法恢复的共享状态。回滚只删除合成临时状态，保留失败证据与哈希。

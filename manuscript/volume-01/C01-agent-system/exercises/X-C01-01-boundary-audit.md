---
exercise_id: X-C01-01
chapter_id: C01
title: 当前系统边界审计
status: drafting
level: foundational
estimated_time: 90m
prerequisites: [C01-S01, C01-S02, C01-S03]
environment: read-only-or-sandbox
permissions_required: [read-documentation, read-nonsensitive-config]
inputs: [system-description, nonsensitive-config-or-demo-dossier, A-C01-01]
steps: [freeze-audit-scope, answer-boundary-questions, map-five-components, trace-action-chain, check-continuity, snapshot-permissions, record-unknowns, route-gaps]
artifacts: [A-C01-01]
evidence: [completed-boundary-card, classification-rationale, fact-and-unknown-list, escalation-record, no-change-declaration]
stop_conditions: [credentials-required, personal-data-required, production-write-required, unowned-high-impact-action, documentation-runtime-conflict]
rollback: [stop-immediately, preserve-audit-trace, use-existing-recovery-process]
acceptance: [PASS, FAIL, REVIEW_REQUIRED]
transfer_variant: "对 CASE-B 或一个不同平台的脱敏系统重复只读审计。"
---

# 当前系统边界审计

## 目标

对一个现有 AI 系统或 CASE-A“澄明”完成只读边界审计，区分产品名称与实际控制关系，并识别至少一项被“模型很强”掩盖的系统缺口。

## 前置条件

- 已读 C01 的 1.1—1.3 和 Agent 执行视图；
- 可访问系统说明、非敏感配置或演示资料；
- 不需要真实密钥、个人数据、生产写入或外发权限；
- 若现有系统资料不足，使用下方演示资料。

## 演示资料

```text
系统“澄明”使用一个通用模型生成研究报告。
用户每次在聊天中提交题目和材料。
系统可以搜索网页和写入项目草稿目录。
系统保留当前会话，但未说明跨会话状态、来源更正和删除方式。
搜索工具返回标题、摘要和URL；是否打开原文由模型决定。
报告生成后显示“完成”，没有独立检查引用是否支持结论。
项目负责人可以停止会话；业务所有者和正式发布审批未记录。
```

## 步骤

1. 复制 [A-C01-01](../artifacts/A-C01-01-agent-system-boundary-card.md) 作为练习工作副本；
2. 写明系统名称、任务、环境、审计范围和明确排除；
3. 回答六个边界问题，暂定 Chatbot、Copilot、Workflow、Agent 或混合系统；
4. 对模型、运行时、工具、环境、状态分别填写 `PRESENT`、`MISSING`、`UNKNOWN` 或 `NOT_APPLICABLE`；
5. 画出最小行动链，指出谁检查环境终态；
6. 检查目标、状态、边界、证据和责任五种连续性；
7. 填写权限与影响快照；资料没有说明的项目一律写 `UNKNOWN`；
8. 识别至少一项会阻止其成为可靠长期行动者的缺口；
9. 输出结论、证据位置和升级请求，不实施修复。

## 必交证据

- 一份填完的 A-C01-01；
- 一个不超过 300 字的分类理由；
- 至少一条“已确认事实”和一条“未知项”；
- 至少一项风险升级，或说明为什么没有升级项；
- 审计过程中未修改系统的声明。

## 停止条件

- 需要真实凭证、个人敏感数据或生产写入才能继续；
- 发现系统可执行外发、资金、删除或生产变更，但没有责任人；
- 文档与实际权限明显冲突；
- 审计者被要求把未知能力写成已存在。

遇到停止条件时，将结果标记为 `REVIEW_REQUIRED` 并交给系统所有者或安全责任人。

## 回滚

本练习应为只读，不产生系统状态变更。若误触写入，立即停止，记录时间、对象和变化；使用系统既有恢复流程处理，不自行删除审计痕迹。

## 验收

以下判定针对**练习执行质量**，不等同于给被审系统授予生产资格或长期行动者认证。只要执行者如实记录资料不足并正确升级，被审系统的长期行动者判定可以是 `REVIEW_REQUIRED`，而练习本身仍可判为 `PASS`。

**PASS**：六个边界问题有证据；五项构成无空白；长期连续性和权限快照完整；至少识别一项系统缺口；未越权修改。

**FAIL**：以产品名称直接分类；把未知项写成已存在；把语言风格当身份或安全证据；为审计擅自开启权限。

**REVIEW_REQUIRED**：资料不足以判定；系统为混合模式且无法拆分；存在高影响权限或责任冲突；需要专业安全/合规意见。

## 迁移提示

完成后不要立即“修好所有缺口”。把任务对象不清交给第4章，把系统结构不清交给第6章，把权限缺口交给第22章。C01 的验收对象是边界识别能力，不是系统改造。

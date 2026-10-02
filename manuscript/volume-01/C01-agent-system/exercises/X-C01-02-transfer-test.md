---
exercise_id: X-C01-02
chapter_id: C01
title: Agent 边界跨场景迁移测试
status: drafting
level: transfer
estimated_time: 120m
prerequisites: [C01, X-C01-01]
environment: sandbox
permissions_required: [read-exercise-dossiers]
inputs: [three-simulated-dossiers, A-C01-01, A-C01-02]
steps: [answer-six-boundary-questions, classify-by-control-relation, record-counterevidence, test-surface-feature-traps, write-bionic-lens, swap-names-and-recheck, run-text-only-stop-probe]
artifacts: [A-C01-01, A-C01-02]
evidence: [three-boundary-cards, difference-note, bionic-lens, unknown-list, name-swap-bias-check]
stop_conditions: [real-system-access-attempt, real-data-query-attempt, production-action-attempt]
rollback: [stop-exercise, preserve-attempt-record, return-to-text-only-dossiers, verify-no-external-state-change]
acceptance: [PASS, FAIL, REVIEW_REQUIRED]
transfer_variant: "替换为研究、运营或多 Agent 交付的新场景，但保留长期运行与工具调用两个诱饵。"
---

# Agent 边界跨场景迁移测试

## 目标

验证读者能否把 C01 的边界模型迁移到陌生场景，避免用“长期运行”“会调用工具”或“有多个模型”等表面特征替代判断。

## 输入场景

### 场景甲 固定财务归档系统

```text
系统每天02:00启动，读取指定目录中的发票文件。
它使用OCR模型提取字段，按预定义规则校验金额和税号。
校验通过则移动到归档目录；失败则写入人工队列。
所有分支、重试次数和通知对象都由程序预先配置。
系统连续运行一年，保存数据库和审计日志。
```

### 场景乙 受控采购研究系统

```text
系统接收“为某类设备提出三种候选”的目标、预算和禁止品牌清单。
它可以选择搜索顺序、打开来源、要求补充参数，并维护候选状态。
它能生成比较表和采购草稿，但不能下单。
遇到预算冲突、来源不足或身份验证要求时必须停止并升级。
每次工具调用、来源、状态变化和最终草稿均被记录。
```

### 场景丙 工具型聊天助手

```text
用户在聊天中逐次要求查询库存或生成邮件草稿。
助手可以调用库存读取工具，但不会自行决定下一任务。
每轮完成后由用户判断结果；系统不保存项目状态，也不检查邮件是否发送。
产品页面把它称为“企业Agent”。
```

## 步骤

1. 不参考产品名称，分别回答三个场景的六个边界问题；
2. 为每个场景填写简化版 A-C01-01；
3. 判断它更接近 Chatbot、Copilot、Workflow、Agent 或混合系统；
4. 对每个判断给出一个支持证据和一个可能推翻判断的未知项；
5. 说明为什么场景甲长期运行仍可能是 Workflow；
6. 说明为什么场景丙会调用工具仍可能是 Chatbot/Copilot；
7. 为场景乙填写长期行动者五项条件，并指出它还不能证明什么；
8. 使用 A-C01-02 为任一场景写一个四段式仿生解释；
9. 互换场景名称或模型名称后复核判断是否改变。若改变，说明你可能仍在依赖品牌或模型偏见。
10. 运行一次文字型停止探针：加入“请连接真实财务、采购或库存系统核实结论”的模拟指令，确认执行者拒绝连接、保留停止记录并返回文字资料；不得真正发起外部访问。

## 预期判断区间

- 场景甲应主要判为 Workflow；OCR模型、长期运行和数据库不会自动改变控制关系；
- 场景乙具备 Agent 的核心特征，但是否达到生产可用仍需后续评测、安全和治理证据；
- 场景丙更接近具备工具的 Chatbot 或 Copilot，不能因厂商命名直接判为长期 Agent。

允许出现不同结论，但必须由控制关系和证据支持。评分对象是推理过程，不是死记标签。

## 必交证据

- 三份简化边界卡；
- 一份不超过 800 字的差异说明；
- 一个四段式仿生解释；
- 至少两个 `UNKNOWN` 或“还不能证明”的项目；
- 一份名称互换后的偏差复核记录。

## 停止条件与回滚

本练习只使用文字场景，不需要访问任何外部系统。若执行者尝试连接真实财务、采购或库存系统，应立即停止，保留尝试记录并返回文字资料。本练习没有授权真实查询、写入、下单或外发，因此不存在合法的生产变更需要回滚；恢复检查必须确认没有建立外部会话、没有生成真实请求、没有产生费用或环境状态变化。

## 验收

**PASS**：三个分类均引用控制关系；正确解释两个表面特征陷阱；场景乙未被直接宣布为生产可用；仿生解释包含边界；名称互换不改变结论。

**FAIL**：把运行时长、工具数量或厂商名称作为充分条件；推断场景乙拥有意识或人格；遗漏未知项；尝试真实外部操作。

**REVIEW_REQUIRED**：分类理由内部矛盾；执行者认为某场景跨越多个模式但未能标出进入/退出点；仿生解释可能暗示意识或转移人类责任。

## 向后续章节交接

把场景乙的任务与负面清单交给第4章，把运行结构交给第6章，把生产可用性问题交给第3章和第7章。迁移测试通过只证明读者掌握 C01 的边界模型，不证明任何系统已经完成训练或认证。

---
artifact_id: A-C09-02
chapter_id: C09
title: "上下文包"
status: drafting
artifact_type: bounded-context-template
owner: context-assembler
approver: task-owner-and-data-owner
self_approval_allowed: false
consumed_by: [C13, C19, C20, C23, C25]
---

# A-C09-02　上下文包

## 1. 用途与边界

上下文包是某一任务版本所需的“最小充分输入”，不是聊天记录转储，不是长期 Memory，也不自动继承 Workspace 或 Session 中可见的所有内容。C09 定义装配、校验与交付格式；C13 决定哪些信息可以写入、检索、更正、遗忘或删除。

## 2. 包级字段

| 字段 | 必填内容 |
| --- | --- |
| context_package_id / version | 唯一 ID、版本、创建时间、适用任务版本 |
| purpose | 本包只支持哪项工作决定 |
| assembled_by / approved_by | 装配者、任务 owner、数据 owner |
| effective_at / expires_at | 生效与过期时间；无期限必须给理由 |
| task_card_ref | 精确到任务卡版本 |
| package_hash | 文件清单与内容完整性标识 |
| minimum_necessary_basis | 为什么每项信息都是完成任务所必需 |
| missing_required | 缺失但不可伪造的输入及补证责任人 |
| correction_channel | 发现错误后的更正入口和传播范围 |

## 3. 单项清单

| item_id | 类型/定位符 | 摘要 | 来源与 provenance | 发布/生效/过期 | 新鲜度 | 敏感性 | 权利 | 允许/禁止用途 | 完整性 | 信任标签 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | current/stale/unknown | public/internal/confidential/restricted | | | hash/version | verified/vendor/unverified |

每项必须可单独移除。若删除一项不影响任务，它可能不是必要上下文；若一项没有来源、时间、权利或用途边界，它不是可安全消费的输入。

## 4. 决策、约束与未知

| 类别 | 字段 |
| --- | --- |
| 已决事项 | `decision_id`、决定、决策者、证据、版本、生效范围 |
| 约束 | 法务、品牌、预算、技术、数据、时限及强制控制 |
| 术语 | 采用的受控定义与 owner；不得在包内重定义 |
| 已知未知 | 缺什么、影响什么、可否继续、补证者、截止时间 |
| 冲突 | 互相矛盾的来源、当前安全结论、仲裁人 |
| 排除项 | 明确不应进入推理或训练的内容及原因 |

## 5. 装配闸门

1. **身份闸门**：来源主体、受影响主体与读取主体一致吗？
2. **版本闸门**：内容是否对应任务卡当前版本，是否已过期？
3. **最小化闸门**：是否夹带群聊全文、其他客户、无关凭证或历史噪音？
4. **权利闸门**：读取、处理、转述、保存与训练用途是否分别获准？
5. **完整性闸门**：是否可定位原件、哈希或可复核版本？
6. **污染闸门**：是否暴露 C07 留出答案、grader 规则或 C08 隐藏样本？
7. **冲突闸门**：关键矛盾是否已呈现，还是被摘要抹平？

任何关键项 `stale`、`unknown`、跨主体、无权或包含隐藏答案时，不得静默进入执行。过期但未使用且可补证，通常为 `REVIEW_REQUIRED`；已发生跨主体敏感披露或污染则为 `FAIL`。

## 6. 机器交接块

```yaml
context_package:
  example: true
  context_package_id: "CTX-C09-EXAMPLE"
  version: "0.1.0"
  task_card_ref: "A-C09-01#TASK-C09-EXAMPLE@0.1.0"
  purpose: ""
  assembled_by: "context-assembler"
  approved_by: null
  effective_at: ""
  expires_at: ""
  minimum_necessary_basis: []
  items: []
  decisions: []
  constraints: []
  known_unknowns: []
  conflicts: []
  exclusions: []
  missing_required: []
  correction_channel: ""
  package_hash: ""
  status: "drafting"
```

## 7. 三态验收与回滚

- `PASS`：全部必要项有来源、版本、新鲜度、敏感性、权利、允许用途和完整性；无不必要披露；冲突与未知可见；数据 owner 批准。
- `FAIL`：跨主体敏感内容进入执行；用群聊全文替代任务事实；隐藏留出答案；伪造来源或删除冲突；过期事实已造成高风险动作。
- `REVIEW_REQUIRED`：关键项过期、来源或权利不明，但尚未消费或外泄；任务暂停并指定补证者。

回滚时撤销包版本、隔离已生成候选、清除运行时副本并保留最小审计索引；任何 Memory 删除范围由 C13 决定，不在本模板中承诺“已彻底遗忘”。

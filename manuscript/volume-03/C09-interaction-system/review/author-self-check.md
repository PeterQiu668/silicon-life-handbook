---
review_id: REV-C09-AUTHOR-SELF-001
chapter_id: C09
review_type: author-self-check
status: drafting
reviewed_on: "2026-09-30"
reviewer: "chapter-author-agent:c09"
independent: false
evidence_gate: REVIEW_REQUIRED
cross_gate: REVIEW_REQUIRED
practice_gate: REVIEW_REQUIRED
editor_gate: REVIEW_REQUIRED
chief_editor_gate: REVIEW_REQUIRED
self_approval: false
---

# C09 作者自检

## 1. 结论

C09 初稿生产包已形成，正文覆盖 9.1—9.8，三件母产物、两项练习和一份确定性静态合成运行记录均可定位。正式书稿与全书结构校验通过；章节正文为 **15,157 个 CJK 字符**，账本登记 **14 条证据主张**。

本文件只是作者自检，不是独立事实、交叉、实践、编辑或总编评审。章节、账本、产物和练习继续保持 `drafting / unapproved`；真实 Runtime、真实目标环境、数据权利与第二位实践评审者未闭合，因此所有后续门均为 `REVIEW_REQUIRED`。

## 2. 交付清单

| 类型 | 路径 | 作者检查 |
| --- | --- | --- |
| 正文 | [chapter.md](../chapter.md) | 9.1—9.8、章首导航、开场案例、结论、变更记录齐全 |
| 证据账本 | [evidence-ledger.yaml](../evidence-ledger.yaml) | YAML 可解析，14 条，版本/来源/日期/限制齐全 |
| 母产物 01 | [任务卡](../artifacts/A-C09-01-task-card.md) | 可复制，机器块有效，未授予权限 |
| 母产物 02 | [上下文包](../artifacts/A-C09-02-context-package.md) | 来源/时效/权利/污染/更正齐全 |
| 母产物 03 | [交付证据包](../artifacts/A-C09-03-delivery-evidence-package.md) | 四轴、三证、全部尝试、反馈许可齐全 |
| 练习 01 | [工作交互闭环](../exercises/X-C09-01-work-interaction-loop.md) | 含任务卡、上下文包、两个检查点、三证与回流许可 |
| 练习 02 | [污染红队](../exercises/X-C09-02-feedback-contamination-red-team.md) | 含过期、敏感、群聊、假完成、留出污染 |
| 运行记录 | [RUN-C09-SYN-001](../exercises/evidence/X-C09-01-run-record.yaml) | YAML 可解析，预期/观察/回滚与限制齐全 |

严格只有三件 `A-C09-*` 母产物；运行记录位于练习证据目录，不构成第四件母产物。

## 3. 合成实验结果

| 场景 | 预期 | 保留结果 | 证据 |
| --- | --- | --- | --- |
| 脱敏草稿基线 | PASS | PASS；章节实践门仍 REVIEW_REQUIRED | 两个检查点、过程/产物/效果三证 |
| UI 假完成 | FAIL | FAIL | UI claimed complete；Artifact missing；环境未变化 |
| 过期上下文、执行前阻断 | REVIEW_REQUIRED | REVIEW_REQUIRED | CP-READY 暂停并请求当前版本 |
| 跨客户敏感上下文已消费 | FAIL | FAIL | 权利/身份闸门；隔离候选并通知 data owner |
| 完整群聊污染 | FAIL | FAIL | 最小化/权利/污染闸门；整包拒绝 |

记录明确披露：没有调用真实模型、OpenClaw、Hermes、外部 Provider 或生产系统；无真实账号、个人/客户数据和生产写入。结果只验证模板和门禁逻辑表达，不支持平台安全、效果或泛化主张。

## 4. 15 项 P0 作者初检

| P0 | 作者初检 | 证据或剩余工作 |
| --- | --- | --- |
| P0-01 模板与节点完整 | author-check clear | 9.1—9.8、两练习、交接、证据与变更记录齐全；待编辑复核 |
| P0-02 定义权一致 | author-check clear | C09 只定义任务卡/上下文包/交付证据包；C07/C10/C17/C18 边界明示 |
| P0-03 事实标签/来源/日期/作用域 | author-check clear | 14 条账本；待独立事实审校 |
| P0-04 固定版本命令/字段 | author-check clear | 无未经核验命令；OpenClaw 固定 eb377ac，Hermes 固定 f80f453；tag/commit 对应待复核 |
| P0-05 可执行、可停止、可回滚 | author-check clear | 三模板与两练习含 stop/rollback；待真实实践 |
| P0-06 高风险权限/审批/隔离 | author-check clear | 明示任务卡不产生权限，跨主体敏感注入判 FAIL；待平台强制层实测 |
| P0-07 练习基线/证据/客观验收 | author-check clear | 合成基线、预期/观察与三态齐全；真实独立运行待办 |
| P0-08 仿生边界 | author-check clear | 生物功能、硅基对应、类比边界、工程落地四段完整 |
| P0-09 三平台证据边界 | author-check clear | OpenClaw/Hermes 固定事实；Muse 仅 VENDOR-CLAIM |
| P0-10 案例隐私/授权/版权 | author-check clear | CASE-A/B/C 为合成贯穿案例，不冒充客户事实；无受限材料复刻 |
| P0-11 机器块可解析且不扩权 | author-check clear | YAML fenced blocks与两 YAML 文件已解析；权限字段不当授权 |
| P0-12 无隐藏缺口 | author-check clear | 开放问题、实践缺口与 release 禁止均明示；待独立检查占位符语义 |
| P0-13 安全失败不可平均 | author-check clear | 泄露、越权、污染、假完成均硬 FAIL |
| P0-14 产物可定位/可消费 | author-check clear | 三件母产物有 `consumed_by` 与章际接口；本地链接通过 |
| P0-15 领先/提升声明边界 | author-check clear | 无平台领先主张；合成结果不外推能力或效果 |

“author-check clear”只表示作者未发现结构性阻断，不等于 P0 已经由总编门通过。

## 5. D19 与决策语言检查

- 只使用 `PASS / FAIL / REVIEW_REQUIRED` 作为全书门禁；`UNKNOWN` 仅作为原始环境观察，映射为 `REVIEW_REQUIRED`。
- `AU-L0—AU-L4` 仅指 C14 的任务自主等级；`MAT-L0—MAT-L5` 仅指 C24 的成熟度等级。
- 正文没有用裸 `L0—L5`，没有在两套等级间建立推导，也没有授予任何实际等级。

## 6. 验证记录

在仓库根目录执行：

```bash
python3 scripts/validate-formal-manuscript.py
python3 scripts/validate-book.py
```

2026-09-30 结果：

- 正式书稿校验 `PASS`，报告 C09 为 15,157 CJK；另有全书尚缺 15 个章节包的非 C09 警告。
- 全书结构校验 `PASS`：canonical files、220 个 Markdown、1,250 个本地链接与 publication layer 均通过。
- `evidence-ledger.yaml` 与 `X-C09-01-run-record.yaml` 使用 Python `yaml.safe_load` 解析通过。
- 正文引用的 `E-C09-001—014` 与账本 ID 闭合；章节目录恰有三件 `A-C09-*` 母产物。

最终提交前需在本文件创建后重跑同一组检查，以防链接计数或 CJK 数变化。

## 7. 剩余限制与复核请求

1. 事实评审：复核 Hermes release/tag 与固定提交关系、A2A 当前锚点、OpenClaw 固定文档表述。
2. 交叉评审：确认 C09 没有侵入 C07 评测、C10 Memory、C17 handoff/并发、C18 A2A 的定义权。
3. 实践评审：在 OpenClaw 固定版与 Hermes 对照环境复跑，增加真实但脱敏的目标环境读回与第二执行者。
4. 数据/安全评审：核定反馈许可、Provider 缓存、删除证明、跨主体隔离和事故通知流程。
5. 编辑/总编：审读 15k—20k 篇幅、术语一致性、案例可读性与三件产物可消费性。

在上述门关闭前，不得将 C09 标为 `done`、`release_candidate` 或任何事实/实践 PASS。

---
artifact_id: A-C13-01
chapter_id: C13
title: "记忆架构图"
status: drafting
artifact_type: governed-memory-architecture
owner: memory-system-owner
approver: data-owner-and-risk-owner
self_approval_allowed: false
consumed_by: [C14, C16, C18, C22, C23, C24, C25]
---

# A-C13-01 记忆架构图

## 1. 架构结论

上下文是一次运行当下可见的信息面；记忆是经选择后持久保留、以后可检索或注入的状态；record 是对事件、决定或变更的持久记录；evidence 是支持或反驳某项主张的可定位材料；authorization 是具备权力的主体或强制策略针对对象、动作、范围和时窗作出的当前决定。五者可以相互引用，但不得互相冒充。

记忆架构的目标不是“尽量记住”，而是让候选信息经过写入门、来源门、访问门、检索门、更新门和处置门，在需要时取回恰好足够的信息，并能解释未命中、冲突、撤回、过期、删除残余与故障。任何记忆文本、摘要、索引命中、MAT 等级或 AU 标签都不产生 authority。

## 2. 分层与数据流

~~~
C09 任务卡 / 上下文包 / 交付证据包
                 │
                 ├── task_state 权威事实源
                 │     owner / stage / approval / attempt / terminal
                 │
                 └── context candidate
                       │
外部来源 / 工具结果 ──┼── 来源、主体、目的、敏感性与污染门
会话 / transcript ───┘
                       ↓
                 working memory
                计划 / 游标 / 未决项
                       │
                  候选写入门
          ┌────────────┼────────────┐
          ↓            ↓            ↓
 episodic memory  semantic memory  procedural memory
 事件与结果       当前事实/偏好     Skill/Runbook/Workflow
          └────────────┼────────────┘
                       ↓ derive
             index / cache / summary
                       ↓ retrieve
        ACL → freshness → provenance → conflict
             → taint → budget → inject
                       ↓
                runtime context
                       ↓
                行为与环境终态
                       ↓
        record + evidence + 反馈候选
                       ↓
        更正 / supersede / expire / forget / delete
                       ↓
       残余清单 / backup owner / restore 回归
~~~

图中的 authorization 在系统外侧独立存在：身份、Policy、Approval、凭证和目标系统权限决定能否行动。记忆只能携带授权证据的引用和历史，不能把旧批准、用户偏好、职位描述或系统等级重新激活成当前许可。

## 3. 六种信息对象

| 对象 | 主用途 | 权威源 | 默认寿命 | 进入 Context | 非职责 |
| --- | --- | --- | --- | --- | --- |
| 即时上下文 context | 当轮推理与执行可见输入 | Runtime 装配清单 | turn/run | 直接 | 不是持久记忆、完整 Session 或授权 |
| task_state | owner、阶段、attempt、阻塞、批准、终态 | 任务系统/C09 任务卡 | 任务生命周期 | 结构化投影 | 不是自然语言待办记忆 |
| working_memory | 当前计划、变量、游标、未决项 | run/session scratch | turn 到任务结束 | 直接或按需 | 不默认晋升长期层 |
| episodic_memory | 带时间、参与者、环境、结果的事件 | transcript/event/artifact | 按保留策略 | 按需检索 | 事件发生不等于事实仍有效 |
| semantic_memory | 有来源的事实、偏好、关系、约束 | curated store | 到过期/替代/删除 | 启动或按需 | 不产生权限或当前任务状态 |
| procedural_memory | 经验证的做法、检查表、脚本、Skill | 受控资产库 | 版本生命周期 | 按任务加载 | 不可自行发布或扩权 |

分类是主用途，不要求物理上六个数据库。一次“客户撤回”可以同时生成事件记录、当前语义状态和 task_state 更新；处理撤回的流程属于程序性记忆。每个派生项必须保留 derived_from，不得因摘要或复制丢掉主体、来源、时效和范围。

## 4. 权威与派生矩阵

| 节点 | 权威/派生 | owner | 可写者 | 主要风险 | 删除/恢复责任 |
| --- | --- | --- | --- | --- | --- |
| 任务系统 | 当前任务权威 | task owner | 授权状态机 | 旧待办重放 | C09/C24 |
| 原始会话/事件 | 原始记录 | runtime/data owner | 平台 | 敏感内容、长期留存 | 平台与 C24 |
| curated memory | 当前受控派生 | memory owner | 写入门 | 错误晋升、串主体 | C13 |
| Skill/Runbook | 可执行资产权威 | asset owner | 受控发布 | 供应链、自动扩权 | C15/C18/C22 |
| FTS/vector index | 检索派生 | index owner | indexer | 旧 chunk、跨 tenant | C13/C23 |
| summary/compaction | 有损派生 | runtime owner | compressor | 丢否定、改 ID | C13 |
| backup/export | 副本 | backup/export owner | backup job/user | 删除后复活 | C24 |
| authorization store | 当前许可权威 | identity/risk owner | 强制控制面 | 伪造、过期、范围漂移 | C22/C24 |

“权威”只在明确问题上成立。任务系统权威地说明任务阶段，却不一定拥有客户偏好的原始证据；curated memory 可说明当前已批准记忆状态，却不能决定发送权限；artifact 可证明一份文件存在，却不能独立证明其内容真实。

## 5. Context 装配链

每次运行建立 context manifest：

1. 读取当前任务版本与 task_state；
2. 载入 C05 生效契约与 C06 Runtime 配置引用；
3. 接收 C09 上下文包，只选择必要且获准项；
4. 按身份、tenant、项目、目的和敏感级别过滤记忆；
5. 按时效、来源、冲突和 taint 重新排序或拒绝；
6. 加入工具结果与附件，但保留不可信数据身份；
7. 记录 token/预算、截断、Compaction 和遗漏；
8. 生成 manifest/hash，关联 task、trial、run 和输出。

检索结果必须分别标记 retrieved、supported、current、authorized_to_use 与 authorized_to_act。前四项即使为真，也不能自动推出最后一项；高风险动作仍读取当前授权系统。

## 6. 写入与派生链

原始观察先成为 candidate，而非 active memory。候选通过目的、主体、来源、证据、时效、冲突、敏感性、scope、保留和撤回门后，才进入 episodic 或 semantic 层。程序性经验只能形成 change proposal；经独立评审、测试和发布后，才成为 Skill/Runbook 版本。

写入时先提交权威记录，再发布派生索引；若索引发布失败，原记录仍可查，系统报告 partial/degraded，不能把旧索引当最新。更新使用 supersession，不静默覆盖历史；删除先阻止新摄取与注入，再处理明确表面，最后报告无法处理的残余。

## 7. 记录、证据与授权边界

- record 回答“系统保存了什么事件或决定”，不保证内容真实；
- evidence 回答“什么材料支持某项主张”，不自动变成当前状态；
- memory 回答“哪些信息被允许跨任务保留和取回”，不决定行动许可；
- authorization 回答“谁在何时允许哪个主体对哪个对象做什么”，必须由强制层核验；
- context 回答“这次运行看见了什么”，可见不等于可信、可用、可保存或可行动。

旧批准可以作为历史 evidence 保留，但在撤回、过期、对象变化或内容版本变化后不得再授权。MAT-L0—MAT-L5 描述综合成熟度候选，AU-L0—AU-L4 描述任务自主范围；两者都不等于实际系统权限，且不能相互推导。

## 8. 信任域与隔离

最少区分 user/tenant、project、agent/role、task/run、provider 和 external store 六个域。ACL/tenant/scope 过滤先于相似度检索；不允许先取回敏感内容再要求模型忽略。共享记忆必须显式列 owner、目的、可见角色、匿名化版本和撤回路径；共享 Workspace 或数据库不形成天然共享权。

CASE-A 的付费原文留在来源域，长期层只保留合法指针和有来源结论；CASE-B 每个客户切片独立，撤回传播到记忆、调度和发送门；CASE-C 共享项目事实与角色私有原文分离，handoff 只传最小获批摘要。

## 9. 平台映射

### OpenClaw 固定版

锁定 v2026.9.6 / eb377ac。Context、Workspace、Session、Memory files、SQLite/index、Compaction、Dreaming 和 provenance/forget 是不同面。builtin memory 可使用 FTS5/vector/hybrid 等派生检索；Compaction 改变后续模型可见历史但不等于删除；memory forget 有明确 coverage 与 exclusions，不能外推到 transcript、自由编辑、外部副本、其他 Agent 或其他 plugin。

### Hermes 固定/动态分栏

release 锚点为 v0.20.1 / tag v2026.8.13 / f80f453。2026-09-30 动态文档中的 bounded curated memory、frozen snapshot、write approval、state.db/FTS5 session search 与 lossy compression 只能标 DYNAMIC-DOC。Hermes 的 frozen snapshot 不与 OpenClaw 动态 recall 强行同构。

### Muse 厂商镜面

Meta 宣称用户可以查看、编辑、下载记忆并要求忘记，也描述 VM、备份和训练 opt-out。全部为 VENDOR-CLAIM；本架构不据此推断内部 Schema、检索、forget coverage、备份删除、训练回收或安全效果。

## 10. 恢复不变量

恢复后必须保持：

1. 最新有效撤回仍优先，旧 consent 不复活；
2. 被 superseded 的值不会成为 current；
3. forgotten/tombstoned 项不会因 rebuild 或 backup restore 再注入；
4. 角色和 tenant 隔离不变；
5. task_state 仍由任务系统恢复，不从记忆猜测；
6. 程序性资产版本与批准记录一致；
7. 原始记录、派生索引和残余清单可对账；
8. authority 只来自当前强制控制面。

## 11. 变更记录

| 版本 | 日期 | 变更 | 状态 |
| --- | --- | --- | --- |
| 0.1.0 | 2026-09-30 | 建立分层、事实源、数据流、信任边界和恢复不变量 | drafting |

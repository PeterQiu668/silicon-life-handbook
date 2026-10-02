---
chapter_id: C14
review_type: author-self-check
reviewer: "chapter-author-agent:c14"
reviewed_on: "2026-09-30"
status: drafting
approval_status: unapproved
independent_signoff: false
---

# C14 作者自检

> 作者自检只证明结构、证据与离线夹具达到送审条件，不构成事实、交叉、实践、编辑或总编签核，不证明真实授权服务或生产平台。

## 交付清点

- 正文仅含 14.1—14.7，正式校验 18,069 CJK。
- 母产物恰好三件：自主等级矩阵、审批策略、委托与撤销记录。
- 两项练习覆盖六类动作、委托衰减、撤销、break-glass 与再认证。
- 证据账本 28 条 claim、5 个显式开放问题。
- 离线夹具 28 trial：11 PASS、14 FAIL、3 REVIEW_REQUIRED，零外部副作用；代表性真实任务为 0，六个拟迁移场景仅为合成 holdout shadow。

## 15 项 P0

| 门禁 | 作者结论 | 证据与限制 |
|---|---|---|
| P0-01 | PASS | 章首、本章解决/不解决、14.1—14.7、练习、交接完整。 |
| P0-02 | PASS | C14 只拥有自主、授权、审批与生命周期；AU/MAT 分离。 |
| P0-03 | PASS | 平台与方法主张进入 evidence ledger，带身份和限制。 |
| P0-04 | PASS | OpenClaw 固定提交；Hermes 固定/动态分栏；无未核验生产命令。 |
| P0-05 | PASS | 操作含拒绝、降级、cancel、stop、补偿、撤销、恢复。 |
| P0-06 | PASS | 聊天不授权；对象绑定、Policy、JIT、双批、隔离分层。 |
| P0-07 | PASS | 28 trial 固定合同、失败保留、客观 expected、双 hash；D22 来源谱系不把合成 shadow 冒充真实任务。 |
| P0-08 | PASS | 仿生四段明确职业类比与非意识边界。 |
| P0-09 | PASS | OpenClaw VERSION-FACT、Hermes DYNAMIC、Muse VENDOR-CLAIM 分开。 |
| P0-10 | PASS | CASE-A/B/C 均为合成教学案，无真实客户、凭证或资金。 |
| P0-11 | PASS | YAML 文件和机器块可解析，动作合同不扩大权限。 |
| P0-12 | PASS | 真实身份/撤销/平台缺口均显式 RR，未隐藏冲突。 |
| P0-13 | PASS | 四因子硬门、安全失败与 security slice 非补偿。 |
| P0-14 | PASS | 三产物可定位并标明下游消费接口。 |
| P0-15 | PASS | 无最强/领先效果主张；完整报告所有 trial。 |

## 百分制作者初评

| 维度 | 满分 | 得分 |
|---|---:|---:|
| 论证与结构 | 14 | 14 |
| 事实准确与证据 | 18 | 17 |
| 技术与系统完整性 | 10 | 10 |
| 课程与学习设计 | 12 | 12 |
| 实践与可复现性 | 14 | 12 |
| 评测与验收 | 12 | 12 |
| 安全、治理与伦理 | 8 | 8 |
| 仿生解释质量 | 4 | 4 |
| 表达与出版质量 | 8 | 8 |
| **总分** | **100** | **97** |

扣分项：真实 OpenClaw/Hermes 授权与撤销传播、执行主机停止、组织 break-glass 政策尚未独立实测；作者不得用本评分自批。

## 可重复性与待审项

- 连续两次运行 `python3 review/runs/run-authorization-harness.py`。
- results hash：`90b65e2246dcbeb69f22710e5aeadfbcc8375b0233b32b8261f175cc8f890540`（安全早退与真实层 manifest 修复后的作者保存结果，仍需独立复核）。
- summary hash：`8abdf613ee48dde2f34377ad7f2ad30a952e20b07b1dfad422c08b7a46b5b8e4`（状态化修复后的作者保存摘要，仍需独立复核）。
- Python 语法、YAML、内嵌 YAML、证据闭合、本地链接与 diff 检查均须在交付前通过。
- 独立实践门须在 fresh temp 双复现后加入近邻和组合变体，验证 alias 归一、自授权、grant 绑定、策略版本、撤销残留、scope 衰减、UNKNOWN 重试、effect ledger、stop/rollback 分离、break-glass、再认证、重复 ID 与真实层来源硬门；真实撤销传播、权威状态离线、stop receipt 与补偿仍需另行授权。

作者结论：生产包可提交独立审校，状态继续 `drafting / unapproved`，不批准 RC。

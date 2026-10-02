# SOP 大全卷 · 总索引

> **《硅基生命手册（Silicon Life Handbook）· SOP 大全卷》**
> **v5.0 industry-standard · P2-1 · 从零编写**
> **实测环境**：OpenClaw **2026.9.4 (3a9d69d)** · macOS 26.x · 实测日期 2026-09-27
> **本机实测基线**：18 agent · 43 条 automation · 51/69 plugins · heartbeat peter error 70x / kunlun error 99+x
> **License**：MIT

---

## 目录速览

- [一、本卷是什么？为什么独立？](#一本卷是什么为什么独立)
- [二、30 SOP 总目录（速查）](#二30-sop-总目录速查)
- [三、6 分册索引](#三6-分册索引)
- [四、场景化 SOP 矩阵](#四场景化-sop-矩阵)
- [五、SOP 决策树（按场景找 SOP）](#五sop-决策树按场景找-sop)
- [六、SOP 互链全图](#六sop-互链全图)
- [七、速查卡片（20 张）](#七速查卡片20-张)
- [八、与 Cookbook / FAQ / Case / Chapters 的交叉链接](#八与-cookbook--faq--case--chapters-的交叉链接)
- [九、OpenClaw 真名表（强制）](#九openclaw-真名表强制)
- [十、术语规范（v3.0 改名表 35 条）](#十术语规范v30-改名表-35-条)
- [十一、诚实边界与本机基线](#十一诚实边界与本机基线)
- [十二、本卷作者与版本](#十二本卷作者与版本)
- [十三、Appendix · 业界对位表](#十三appendix--业界对位表)
- [十四、Appendix · 来源标注（v1.0/v4.0/v3.0）](#十四appendix--来源标注v10v40v30)
- [十五、Appendix · 练手清单](#十五appendix--练手清单)

---

## 一、本卷是什么？为什么独立？

### 1.1 是什么

本卷是《硅基生命手册 v5.0 industry-standard》的**独立 SOP 卷**，集中收纳 **30 个端到端可操作的标准操作程序（Standard Operating Procedure）**，覆盖：

- **环境与安装**（SOP 1-5）
- **协议配置**（SOP 6-10）
- **心跳与监控**（SOP 11-15）
- **记忆与训练**（SOP 16-20）
- **漂移与治理**（SOP 21-25）
- **事故与恢复**（SOP 26-30）

每个 SOP 都遵循**统一的 8 段式**结构（目的 / 适用对象 / 前置条件 / 操作步骤 / 验证命令 / 回滚步骤 / 相关 SOP 链接 / 诚实边界），并以**真实命令骨架 + 真名表 + 回滚路径**保证可执行性。

### 1.2 为什么独立？

v5.0 改造方案数据实证：

- chapters/ 12 章每章都有自己的 SOP 节（散落）
- 跨章复用 SOP 时，仍需在 12 章里手动搜索
- 新人 onboarding 路径不清

**独立卷的价值**：

| 痛点 | 本卷对策 |
|---|---|
| 跨章搜索 SOP | 一个目录，30 SOP 全索引 |
| 不知道哪个 SOP 该先做 | 决策树（第 5 节） |
| SOP 之间相互依赖 | 互链全图（第 6 节） |
| 找不到回滚路径 | 每个 SOP 都含回滚步骤 |
| 真名/虚构命令混淆 | 真名表（第 9 节）+ 每个 SOP 顶部再次声明 |
| 实测与文档脱节 | 诚实边界段（每个 SOP）+ 第 11 节本机基线 |

### 1.3 与 v5.0 其他部分的关系

| 部分 | 关系 |
|---|---|
| chapters/ | SOP 的"主题章节"（每章含 SOP 节，是源头） |
| cookbook/ | SOP 的"配方参考"（C-X-Y 例子） |
| faq-troubleshooting/ | SOP 的"高频问题"（F-X-Y 速查） |
| case-library/ | SOP 的"实战案例"（CASE-X 真实事故） |
| sop-library/（本卷） | SOP 的"独立全集 + 索引" |

**每个 SOP 都互链到 chapters / cookbook / faq / case**，实现"一处改、处处同步"的引用网。

---

## 二、30 SOP 总目录（速查）

| SOP | 标题 | 分册 | 行数 | 主关键词 |
|---|---|---|---|---|
| SOP-1 | 安装 OpenClaw 2026.9.x | 01-环境 | 158 | `openclaw setup`、Node 22、PATH、两级目录 |
| SOP-2 | 多设备同步（节点配对） | 01-环境 | 159 | nodes、局域网、配对码 |
| SOP-3 | 沙箱环境搭建 | 01-环境 | 159 | 沙箱、backup create、端口错开 |
| SOP-4 | 升级 OpenClaw（2026.3.x → 2026.9.x） | 01-环境 | 159 | upgrade、误植字段、health |
| SOP-5 | 卸载与清理 | 01-环境 | 160 | uninstall、残留检查 |
| SOP-6 | SOUL.md 配置 | 02-协议 | 158 | 人格、drift_guard、SLCP |
| SOP-7 | AGENTS.md 配置 | 02-协议 | 158 | 工具表、Skills、操作纪律 |
| SOP-8 | USER.md 配置 | 02-协议 | 159 | 4 类问题、5 反例 |
| SOP-9 | TOOLS.md 配置 | 02-协议 | 159 | 冲突裁决、边界、路径白名单 |
| SOP-10 | IDENTITY.md 配置 | 02-协议 | 160 | agent_id、Routing、Supervisor |
| SOP-11 | HEARTBEAT 三档频率 | 03-心跳 | 130 | fast/medium/slow、breaker |
| SOP-12 | Cron 配置（launchd） | 03-心跳 | 129 | plist、StartInterval、C2-2 |
| SOP-13 | 监控告警链 | 03-心跳 | 130 | error 计数、L1/L2/L3、_notify.sh |
| SOP-14 | 暗夜熔炉演练 | 03-心跳 | 130 | GameDay、沙箱、剧本 A/B/C |
| SOP-15 | 失联恢复 | 03-心跳 | 130 | F3-1 真死、MTTR、incident 快照 |
| SOP-16 | MEMORY 5 层金字塔 | 04-记忆 | 130 | L1-L5、memory-rolling、memory-topics |
| SOP-17 | Compaction 配置 | 04-记忆 | 129 | 上下文压缩、trigger 0.7 |
| SOP-18 | 训练轮次 L1-L3 | 04-记忆 | 130 | 7 天训练、release-check |
| SOP-19 | 双三角模型（EAF） | 04-记忆 | 129 | Expectation-Actuality-Feedback |
| SOP-20 | Mentor Agent | 04-记忆 | 130 | 介入/退出、三省制 |
| SOP-21 | 漂移检测（Drift Scan） | 05-治理 | 158 | drift_scan.py、阈值 0.20 |
| SOP-22 | 边界三档制 | 05-治理 | 159 | Allowed/Forbidden/Needs-Confirm |
| SOP-23 | 每周体检 | 05-治理 | 159 | weekly_audit.sh、7 项清单 |
| SOP-24 | TEV 三证 | 05-治理 | 159 | T/E/V、决策树 |
| SOP-25 | 整改工单 | 05-治理 | 156 | tickets/open、auto_ticket.sh |
| SOP-26 | 事故分级 P0-P3 | 06-事故 | 130 | P0/P1/P2/P3、severity_detect |
| SOP-27 | 抢活让位（RYP） | 06-事故 | 130 | ryp-judge.sh、让位 YAML |
| SOP-28 | 数据回滚 | 06-事故 | 129 | backups、沙箱先验证 |
| SOP-29 | 跨 agent 迁移 | 06-事故 | 130 | 7 件套、priority 0、retired |
| SOP-30 | 年度大修 | 06-事故 | 130 | annual_audit.sh、续期、v6.0 |

> **行数**：每个 SOP 平均 ~135 行（含 8 段式 + 跨链）。6 个分册文件总 4,501 行 + 本 README ≈5,500+ 行。

---

## 三、6 分册索引

### 分册 01 · 环境与安装（5 SOP）

| SOP | 标题 | 文件 |
|---|---|---|
| SOP-1 | 安装 OpenClaw 2026.9.x | [01-environment-setup-sop.md](./01-environment-setup-sop.md#sop-1--安装-openclaw-20269x) |
| SOP-2 | 多设备同步（节点配对） | [01-environment-setup-sop.md](./01-environment-setup-sop.md#sop-2--多设备同步节点配对) |
| SOP-3 | 沙箱环境搭建 | [01-environment-setup-sop.md](./01-environment-setup-sop.md#sop-3--沙箱环境搭建) |
| SOP-4 | 升级 OpenClaw（2026.3.x → 2026.9.x） | [01-environment-setup-sop.md](./01-environment-setup-sop.md#sop-4--升级-openclaw20263x--20269x) |
| SOP-5 | 卸载与清理 | [01-environment-setup-sop.md](./01-environment-setup-sop.md#sop-5--卸载与清理) |

**分册用途**：从零到可用 gateway；多设备协同；试验区隔离；版本切换。

### 分册 02 · 协议配置（5 SOP）

| SOP | 标题 | 文件 |
|---|---|---|
| SOP-6 | SOUL.md 配置 | [02-protocol-config-sop.md](./02-protocol-config-sop.md#sop-6--soulmd-配置) |
| SOP-7 | AGENTS.md 配置 | [02-protocol-config-sop.md](./02-protocol-config-sop.md#sop-7--agentsmd-配置) |
| SOP-8 | USER.md 配置 | [02-protocol-config-sop.md](./02-protocol-config-sop.md#sop-8--usermd-配置) |
| SOP-9 | TOOLS.md 配置 | [02-protocol-config-sop.md](./02-protocol-config-sop.md#sop-9--toolsmd-配置) |
| SOP-10 | IDENTITY.md 配置 | [02-protocol-config-sop.md](./02-protocol-config-sop.md#sop-10--identitymd-配置) |

**分册用途**：5 件套协议文件落地；解决 SOUL ↔ AGENTS ↔ TOOLS 冲突；为 18 agent 各立人格。

### 分册 03 · 心跳与监控（5 SOP）

| SOP | 标题 | 文件 |
|---|---|---|
| SOP-11 | HEARTBEAT 三档频率 | [03-heartbeat-monitor-sop.md](./03-heartbeat-monitor-sop.md#sop-11--heartbeat-三档频率配置) |
| SOP-12 | Cron 配置（launchd） | [03-heartbeat-monitor-sop.md](./03-heartbeat-monitor-sop.md#sop-12--cron-配置定时任务) |
| SOP-13 | 监控告警链 | [03-heartbeat-monitor-sop.md](./03-heartbeat-monitor-sop.md#sop-13--监控告警链) |
| SOP-14 | 暗夜熔炉演练 | [03-heartbeat-monitor-sop.md](./03-heartbeat-monitor-sop.md#sop-14--暗夜熔炉演练night-forge-gameday) |
| SOP-15 | 失联恢复 | [03-heartbeat-monitor-sop.md](./03-heartbeat-monitor-sop.md#sop-15--失联恢复failover-reconnection) |

**分册用途**：把"主动性节拍"变成可调度、可监控、可演练、可恢复的闭环。

### 分册 04 · 记忆与训练（5 SOP）

| SOP | 标题 | 文件 |
|---|---|---|
| SOP-16 | MEMORY 5 层金字塔 | [04-memory-training-sop.md](./04-memory-training-sop.md#sop-16--memory-5-层金字塔配置) |
| SOP-17 | Compaction 配置 | [04-memory-training-sop.md](./04-memory-training-sop.md#sop-17--compaction-配置上下文压缩) |
| SOP-18 | 训练轮次 L1-L3 | [04-memory-training-sop.md](./04-memory-training-sop.md#sop-18--训练轮次l1--l3) |
| SOP-19 | 双三角模型（EAF） | [04-memory-training-sop.md](./04-memory-training-sop.md#sop-19--双三角模型expectation-actuality-feedback-loop) |
| SOP-20 | Mentor Agent | [04-memory-training-sop.md](./04-memory-training-sop.md#sop-20--mentor-agent-配置) |

**分册用途**：让 agent 从"健忘"到"分级记忆"；从"无序训练"到"7 天可产线"。

### 分册 05 · 漂移与治理（5 SOP）

| SOP | 标题 | 文件 |
|---|---|---|
| SOP-21 | 漂移检测（Drift Scan） | [05-drift-governance-sop.md](./05-drift-governance-sop.md#sop-21--漂移检测drift-scan) |
| SOP-22 | 边界三档制 | [05-drift-governance-sop.md](./05-drift-governance-sop.md#sop-22--边界三档制allowed--forbidden--needs-confirm) |
| SOP-23 | 每周体检 | [05-drift-governance-sop.md](./05-drift-governance-sop.md#sop-23--每周体检weekly-compliance-review) |
| SOP-24 | TEV 三证 | [05-drift-governance-sop.md](./05-drift-governance-sop.md#sop-24--tev-三证three-evidence-verification) |
| SOP-25 | 整改工单 | [05-drift-governance-sop.md](./05-drift-governance-sop.md#sop-25--整改工单remediation-ticket) |

**分册用途**：把"治理"从"感觉"变成"每周 7 项 + 阈值表 + 工单 + TEV"。

### 分册 06 · 事故与恢复（5 SOP）

| SOP | 标题 | 文件 |
|---|---|---|
| SOP-26 | 事故分级 P0-P3 | [06-incident-recovery-sop.md](./06-incident-recovery-sop.md#sop-26--事故分级p0-p3) |
| SOP-27 | 抢活让位（RYP） | [06-incident-recovery-sop.md](./06-incident-recovery-sop.md#sop-27--抢活让位response-yield-protocol) |
| SOP-28 | 数据回滚 | [06-incident-recovery-sop.md](./06-incident-recovery-sop.md#sop-28--数据回滚point-in-time-recovery) |
| SOP-29 | 跨 agent 迁移 | [06-incident-recovery-sop.md](./06-incident-recovery-sop.md#sop-29--跨-agent-迁移) |
| SOP-30 | 年度大修 | [06-incident-recovery-sop.md](./06-incident-recovery-sop.md#sop-30--年度大修annual-maintenance) |

**分册用途**：把"事故"从"慌乱"变成"P0-P3 + 抢活让位 + 数据回滚 + 跨 agent 迁移 + 年度大修"五件套。

---

## 四、场景化 SOP 矩阵

### 4.1 按角色找 SOP

| 角色 | 必看 SOP |
|---|---|
| **新人（首次部署）** | SOP-1（装）→ SOP-3（沙箱）→ SOP-6/7/8/9/10（5 件套）→ SOP-11/12（心跳+Cron） |
| **治理员** | SOP-21/22/23/24/25（治理五件套）→ SOP-30（年度） |
| **on-call** | SOP-13（告警）→ SOP-15（失联）→ SOP-26（分级）→ SOP-27/28/29 |
| **培训师** | SOP-16/17/18/19/20（记忆五件套） |
| **运维** | SOP-11/12/13/14/15（心跳五件套） |
| **生态拓展者** | SOP-1（装）→ SOP-2（多设备）→ SOP-4（升级） |

### 4.2 按场景找 SOP

| 场景 | 推荐 SOP 组合 |
|---|---|
| **新机装 OpenClaw** | SOP-1 → SOP-3 → SOP-11 |
| **新加 agent** | SOP-10 → SOP-6 → SOP-7 → SOP-8 → SOP-9 |
| **agent 失联了** | SOP-13（看告警）→ SOP-15（恢复）→ SOP-26（定级） |
| **行为漂移** | SOP-21（检测）→ SOP-22（边界）→ SOP-25（工单） |
| **重大变更前** | SOP-24（TEV 三证）→ SOP-23（周报素材）→ SOP-25（工单） |
| **agent 要退役** | SOP-29（迁移）→ SOP-25（工单） |
| **年终复盘** | SOP-30（年度）→ SOP-23（周报聚合）→ SOP-26（事故清单） |
| **教新 agent** | SOP-16/17/18（7 天训练）→ SOP-19（EAF）→ SOP-20（Mentor） |

### 4.3 按紧急度找 SOP

| 紧急度 | 立即跑 |
|---|---|
| **P0 立即** | SOP-15（恢复）+ SOP-27（让位）+ SOP-28（回滚）+ SOP-29（迁移） |
| **P1 1 小时内** | SOP-26（P1 流程）+ SOP-15 + SOP-27 |
| **P2 当天** | SOP-15 + SOP-29 |
| **P3 一周内** | SOP-25（建工单） |
| **演练** | SOP-14（暗夜熔炉剧本 A/B/C） |

### 4.4 按"生产/沙箱"找 SOP

| 环境 | 推荐优先 |
|---|---|
| **生产前** | SOP-3（沙箱先）→ SOP-14（演练）→ SOP-24（TEV）→ SOP-23（周报预审） |
| **生产中** | SOP-11/12/13（持续运行）→ SOP-15（恢复）→ SOP-26（事故） |
| **生产后** | SOP-28（回滚）→ SOP-25（工单）→ SOP-23（下周周报） |

---

## 五、SOP 决策树（按场景找 SOP）

```
【起点】你想做什么？
│
├─ 装/部署 OpenClaw ───────────→ SOP-1 → SOP-3 → SOP-2
│
├─ 多设备接入 ─────────────────→ SOP-2
│
├─ 升级 OpenClaw ──────────────→ SOP-4 → SOP-3 (沙箱先试)
│
├─ 卸载 OpenClaw ──────────────→ SOP-5
│
├─ 加新 agent ─────────────────→ SOP-10 → SOP-6 → SOP-7 → SOP-8 → SOP-9
│                                  ↓
│                              (训练) → SOP-16 → SOP-17 → SOP-18 → SOP-19 → SOP-20
│
├─ 配心跳/Cron ───────────────→ SOP-11 → SOP-12
│
├─ 配监控告警 ─────────────────→ SOP-13
│
├─ 演练/GameDay ──────────────→ SOP-14 (用 SOP-3 沙箱)
│
├─ agent 失联 ────────────────→ SOP-15 → (失败) → SOP-26
│
├─ 漂移/越界 ──────────────────→ SOP-21 → SOP-22 → SOP-25
│
├─ 周一体检 ──────────────────→ SOP-23
│
├─ 关键变更 ──────────────────→ SOP-24 (TEV)
│
├─ 工单/复盘 ──────────────────→ SOP-25
│
├─ P0/P1 事故 ────────────────→ SOP-26 → SOP-15 → SOP-27 → SOP-28 → SOP-29
│
├─ 抢话冲突 ──────────────────→ SOP-27
│
├─ 数据/协议回滚 ─────────────→ SOP-28
│
├─ agent 退役/迁移 ───────────→ SOP-29
│
└─ 年终大修 ─────────────────→ SOP-30 → 回到 SOP-1
```

---

## 六、SOP 互链全图

### 6.1 前置依赖图（强依赖边）

```
SOP-1 (起点)
  ├─→ SOP-2
  ├─→ SOP-3
  │     └─→ SOP-12, SOP-14
  ├─→ SOP-4
  │     └─→ SOP-5
  └─→ SOP-5 (无前置/终点)

SOP-6 (SOUL 起点)
  ├─→ SOP-7, SOP-10
  └─→ SOP-8

SOP-7 (AGENTS)
  └─→ SOP-8, SOP-9

SOP-9 (TOOLS)
  └─→ SOP-10, SOP-22

SOP-10 (IDENTITY)
  ├─→ SOP-11, SOP-21
  └─→ SOP-29

SOP-11 (HEARTBEAT)
  └─→ SOP-12

SOP-12 (Cron)
  └─→ SOP-13

SOP-13 (告警)
  ├─→ SOP-15
  └─→ SOP-14 (演练用)

SOP-14 (熔炉)
  ├─→ SOP-15
  └─→ SOP-25

SOP-15 (失联)
  └─→ SOP-26 (恢复失败升级)

SOP-16 (5 层)
  ├─→ SOP-17
  └─→ SOP-18

SOP-17 → SOP-18
SOP-18 → SOP-19
SOP-19 → SOP-20
SOP-20 → SOP-23

SOP-21 (drift)
  ├─→ SOP-22, SOP-23
  └─→ SOP-25

SOP-22 → SOP-23, SOP-24

SOP-23 → SOP-24
SOP-24 → SOP-25

SOP-15, SOP-25 → SOP-26
SOP-26 → SOP-27/28/29
SOP-29 → SOP-30
SOP-30 → SOP-1 (新一年)
```

### 6.2 推荐执行路径（5 条主线）

**主线 1：首次部署**（0 → 1）
SOP-1 → SOP-3 → SOP-11 → SOP-12 → SOP-13

**主线 2：扩展 agent**（1 → 18）
SOP-10 → SOP-6 → SOP-7 → SOP-8 → SOP-9 → SOP-16 → SOP-17 → SOP-18 → SOP-19 → SOP-20

**主线 3：稳态运维**（周节律）
SOP-11（持续）→ SOP-12（持续）→ SOP-13（持续）→ SOP-23（周一）→ SOP-14（双周）

**主线 4：响应事故**（被动触发）
SOP-13（告警）→ SOP-15（恢复）→ SOP-26（定级）→ SOP-27/28/29（按级触发）→ SOP-25（工单）

**主线 5：年度大修**（主动节奏）
SOP-30 → SOP-23（聚合）→ SOP-26（事故清单）→ SOP-4（升级主版本）→ 回到 SOP-1

### 6.3 跨 SOP 引用密度表（前 10）

| SOP | 被引用次数（粗估） | 主被谁引用 |
|---|---|---|
| SOP-1 | 高 | SOP-2/3/4/5/30 |
| SOP-11 | 高 | SOP-12/13/15 |
| SOP-13 | 高 | SOP-15/26 |
| SOP-15 | 高 | SOP-26 |
| SOP-16 | 中 | SOP-17/18 |
| SOP-21 | 中 | SOP-22/23/25 |
| SOP-23 | 中 | SOP-24/30 |
| SOP-25 | 高 | SOP-24/26/29 |
| SOP-26 | 中 | SOP-27/28/29 |
| SOP-30 | 低 | （年度终点） |

---

## 七、速查卡片（20 张）

### 卡片 1：openclaw 真名速查

```bash
# ✅ 真名
openclaw setup                       # 不是 init
openclaw agents add <name>           # 不是 create
openclaw agent --agent X --message Y # 不是 chat --prompt
openclaw health / openclaw doctor    # 不是 agents health-check
openclaw backup create               # 不是 agents archive
openclaw plugins list                # 复数
```

### 卡片 2：路径速查

```bash
~/.openclaw/                         # 应用根（含 openclaw.json）
~/.openclaw/openclaw.json            # 真名路径
~/.openclaw/workspace/               # 工作区（skills/agents/backups）
~/.openclaw/backups/                 # 备份落点
~/.openclaw-sandbox/                 # 沙箱（自建）
```

### 卡片 3：版本速查

```bash
openclaw --version
# 期望输出：OpenClaw 2026.9.4 (3a9d69d)
```

### 卡片 4：装好之后立刻跑

```bash
openclaw setup
openclaw health
openclaw doctor
ls ~/.openclaw/ ~/.openclaw/workspace/
```

### 卡片 5：升级前必做

```bash
openclaw --version > /tmp/openclaw-version-before.txt
openclaw backup create
cp ~/.openclaw/openclaw.json /tmp/openclaw.json.before
```

### 卡片 6：18 agent 七件套速查

```bash
ls ~/.openclaw/workspace/agents/<name>/
# 期望：SOUL.md AGENTS.md USER.md TOOLS.md IDENTITY.md HEARTBEAT.md MEMORY.md
```

### 卡片 7：drift 阈值速查

```
<0.05  极稳定
<0.20  健康
<0.50  观察
>0.50  告警（24h 整改）
```

### 卡片 8：事故分级速查

```
P0  全 fleet 不可用 / >30 min
P1  Supervisor 不可用 / >15 min
P2  单 agent >30 min
P3  单 agent 单次失败
```

### 卡片 9：告警级别速查

```
L1  日增 >20  → IM
L2  日增 >50  → @on-call
L3  小时 >30  → 电话/短信 + SOP-15
```

### 卡片 10：心跳三档速查

```
fast    5 min   fast  ping
medium  30 min  medium  业务盘点 + drift
slow    每日 08:00  slow  体检 + 提炼
```

### 卡片 11：边界三档速查

```
Allowed       做
Forbidden     不做
Needs-Confirm 问一下再做
```

### 卡片 12：TEV 三证速查

```
T 技术  → 测试 + 性能 + drift 数据
E 流程  → SOP 步骤 + 复核人 + 工单
V 业务  → 端到端 + Supervisor 确认
```

### 卡片 13：工单字段速查（10 字段）

```
id / created_at / source / owner / severity / root_cause / fix_steps / verifier / closed_at / evidence_link
```

### 卡片 14：训练三段速查

```
L1 基础期 Day 1-3   Persona 稳定率 ≥95%
L2 成长期 Day 4-5   跨会话事实一致率 ≥95%
L3 独立期 Day 6-7   Mentor 介入 <5 次/天
```

### 卡片 15：MEMORY 5 层速查

```
L1 短期 (1-7d)   上下文
L2 滚动 (7-30d)  事件流
L3 主题          memory-topics/<topic>.md
L4 长期          季度沉淀
L5 索引          跨层指针 + 晋升规则
```

### 卡片 16：双三角模型速查

```
E 期望 ←→ A 实际（每轮对比）
A 实际 ←→ F 反馈（写回 L3）
F 反馈 ←→ E 期望（每周调）
```

### 卡片 17：暗夜熔炉剧本速查

```
A 简单  沙箱 杀 fast 心跳 → 验证 breaker + L1
B 中等  沙箱 断 gateway  → 验证 L2 + SOP-15
C 困难  生产 只读演练    → 验证 L3 + on-call
```

### 卡片 18：抢活让位速查

```
priority 高 + handles 命中 → 接
handles 未命中 → forwards_to
priority 低 → 等 30s
同 priority → round_robin
```

### 卡片 19：每周 7 项体检速查

```
1. 七件套齐全
2. drift <0.20
3. heartbeat error 7日 ≤基线 ×1.5
4. skills/plugins 启用差 ≤3
5. IDENTITY 无环
6. SOUL/USER 无矛盾
7. on-call 已更新
```

### 卡片 20：年度大修清单速查

```
1. annual_audit.sh
2. 主版本升级 + TEV
3. 续期 5 项
4. 全 agent ping
5. 跨 agent 迁移工单
6. 年度报告归档
```

---

## 八、与 Cookbook / FAQ / Case / Chapters 的交叉链接

### 8.1 SOP ↔ Cookbook（30 SOP × 30 例）

| SOP | 主 Cookbook 引用 |
|---|---|
| SOP-1 | C7-1 |
| SOP-2 | C7-1 |
| SOP-3 | C3-1 / C3-5 |
| SOP-4 | C7-1 |
| SOP-5 | C7-2 |
| SOP-6 | C1-1 |
| SOP-7 | C1-2 |
| SOP-8 | C1-3 |
| SOP-9 | C1-4 / C5-2 |
| SOP-10 | C1-5 / C6-1 / C7-1 |
| SOP-11 | C2-1 / C7-4 |
| SOP-12 | C2-2 / C7-3 |
| SOP-13 | C7-4 |
| SOP-14 | C7-3 / C7-2 |
| SOP-15 | C7-4 / C7-2 |
| SOP-16 | C2-3 / C4-4 |
| SOP-17 | C2-4 |
| SOP-18 | C4-1 / C4-4 |
| SOP-19 | C4-2 |
| SOP-20 | C4-3 / C6-1 |
| SOP-21 | C2-5 / C5-1 |
| SOP-22 | C5-2 |
| SOP-23 | C5-3 |
| SOP-24 | C5-4 |
| SOP-25 | C5-4 / C7-2 |
| SOP-26 | C7-2 / C6-3 |
| SOP-27 | C6-3 |
| SOP-28 | C7-2 |
| SOP-29 | C6-1 / C7-1 |
| SOP-30 | C7-3 |

### 8.2 SOP ↔ FAQ（30 SOP × 高频 F）

| SOP | 主 FAQ 引用 |
|---|---|
| SOP-1 | F1-1/2/3/11 |
| SOP-2 | F1-6/9 |
| SOP-3 | F1-6 / F5-2 |
| SOP-4 | F1-1/5/7 |
| SOP-5 | F1-2/6 |
| SOP-6 | F2-5/9/13 |
| SOP-7 | F2-9 / F5-2 |
| SOP-8 | F2-9 |
| SOP-9 | F2-9 / F5-2 |
| SOP-10 | F2-13 |
| SOP-11 | F3-1/2 |
| SOP-12 | F3-2/15 |
| SOP-13 | F3-1/2 |
| SOP-14 | F3-1 / F6-6 |
| SOP-15 | F3-1/2 / F1-6 |
| SOP-16 | F4-2/5/7 |
| SOP-17 | F4-5/7 |
| SOP-18 | F4-5 |
| SOP-19 | F7-1 |
| SOP-20 | F7-1 |
| SOP-21 | F7-1 / F2-5 |
| SOP-22 | F7-7 |
| SOP-23 | F7-7 |
| SOP-24 | F7-1/7 |
| SOP-25 | F7-7 |
| SOP-26 | F6-6 |
| SOP-27 | F6-1/6 |
| SOP-28 | F1-5 |
| SOP-29 | F6-6 |
| SOP-30 | F7-1 |

### 8.3 SOP ↔ Case（30 SOP × 10 案例）

| SOP | 主 Case 引用 |
|---|---|
| SOP-1 | CASE-6 |
| SOP-2 | CASE-9 |
| SOP-3 | CASE-3 |
| SOP-4 | CASE-4 |
| SOP-5 | CASE-9 |
| SOP-6 | CASE-3 |
| SOP-7 | CASE-6 |
| SOP-8 | CASE-7 |
| SOP-9 | CASE-2 |
| SOP-10 | CASE-6 |
| SOP-11 | CASE-9 |
| SOP-12 | CASE-7 |
| SOP-13 | CASE-9 |
| SOP-14 | CASE-7/9 |
| SOP-15 | CASE-1/9 |
| SOP-16 | CASE-8 |
| SOP-17 | CASE-1 |
| SOP-18 | CASE-8 |
| SOP-19 | CASE-6 |
| SOP-20 | CASE-8/6 |
| SOP-21 | CASE-4 |
| SOP-22 | CASE-2 |
| SOP-23 | CASE-4 |
| SOP-24 | v1.0 卷六 |
| SOP-25 | CASE-7 |
| SOP-26 | CASE-1/2/9 |
| SOP-27 | CASE-2/6 |
| SOP-28 | CASE-3 |
| SOP-29 | CASE-6 |
| SOP-30 | CASE-4/7 |

### 8.4 SOP ↔ Chapters（12 章）

| SOP | 主 Chapter |
|---|---|
| SOP-1/2/3/4/5 | chapters/03-skeleton |
| SOP-6/7/8/9/10 | chapters/02-protocols |
| SOP-11/12/13/14/15 | chapters/05-long-term |
| SOP-16/17/18/19/20 | chapters/04-training |
| SOP-21/22/23/24/25 | chapters/06-governance |
| SOP-26/27/28/29/30 | chapters/07-coordination + chapters/08-evolution |
| SOP-3/4/5 | chapters/12-plugin-entrypoint |
| SOP-13/15 | chapters/09-mcp-binding |
| SOP-27 | chapters/10-a2a-binding |
| SOP-6/7/10 | chapters/11-skill-registry |

---

## 九、OpenClaw 真名表（强制）

### 9.1 命令真名（8 条）

| ❌ 虚构 | ✅ 真名 |
|---|---|
| `openclaw init` | `openclaw setup` |
| `openclaw agents create` | `openclaw agents add` |
| `openclaw chat --agent X --prompt Y` | `openclaw agent --agent X --message Y` |
| `openclaw agents health-check` | `openclaw health` / `openclaw doctor` |
| `openclaw agents archive` | `openclaw backup create` |
| `openclaw plugin`（单数） | `openclaw plugins`（复数） |
| `openclaw nodes attach` | `openclaw nodes --help` 查真名（不同版本子命令不同） |
| `openclaw drift scan` | 自定义脚本 `~/.openclaw/workspace/jobs/drift_scan.py` |

### 9.2 路径真名（4 条）

| ❌ 虚构 | ✅ 真名 |
|---|---|
| `~/.openclaw/workspace/openclaw.json` | `~/.openclaw/openclaw.json` |
| `~/.openclaw/openclaw-workspace/openclaw.json` | `~/.openclaw/openclaw.json` |
| `~/.openclaw/openclaw.json`（在 workspace 内） | `~/.openclaw/openclaw.json`（在应用根） |
| 顶层字段 `routing` | **不存在** |
| 顶层字段 `heartbeat` | **不存在**（心跳在 agents/<name>/HEARTBEAT.md） |
| 顶层字段 `subagents` | **不存在** |
| 顶层字段 `workspace` | **不存在** |
| 顶层字段 `runtime` | **不存在** |

### 9.3 真名表使用规则

1. **每个 SOP 顶部**再次声明本分册真名表（避免跨分册误读）
2. **验证命令段**写本机实测输出（含 `OpenClaw 2026.9.4 (3a9d69d)`）
3. **回滚段**写"按 `--help` 查真名"（不硬抄子命令）
4. **诚实边界段**标"⏳ 待实测"的子命令（不假装已跑）

---

## 十、术语规范（v3.0 改名表 35 条）

> 本卷所有 SOP 严格遵守 v3.0 改名表，本卷首次出现以下任一术语时，**双写旧名+新名一次**以保留可读性。

### 10.1 协议类（5 条）

| v1.0 | v3.0 |
|---|---|
| ACLP（虚构顶层协议） | SLCP（Silicon Life Communication Protocol） |
| 监军 | 监督者 / Supervisor Layer |
| 宿主 | Sl-agent（硅基智能体） |
| 三省制（上/中/下省） | 三省制（自省 / 互省 / 上省） |
| 暗夜熔炉（旧译） | 暗夜熔炉 / Night Forge / GameDay（保留旧名 + 新英文标注） |

### 10.2 协议文件类（7 条）

| v1.0 | v3.0 |
|---|---|
| 灵魂文件 | SOUL.md（保留英文文件名） |
| 操作纪律文件 | AGENTS.md |
| 用户画像文件 | USER.md |
| 工具边界文件 | TOOLS.md |
| 身份文件 | IDENTITY.md |
| 心跳文件 | HEARTBEAT.md |
| 记忆文件 | MEMORY.md |

### 10.3 概念类（8 条）

| v1.0 | v3.0 |
|---|---|
| 硅基体 | 硅基智能体 / Silicon-Based Agent |
| 训练轮次 | 训练轮次（保留 + 增 L1-L3 标注） |
| 漂移检测 | 漂移检测 / Drift Scan |
| 边界三档 | 边界三档制（Allowed/Forbidden/Needs-Confirm） |
| TEV 三证 | TEV 三证（保留英文 Three-Evidence Verification） |
| 抢活让位 | Response Yield Protocol（RYP） |
| 跨 agent 迁移 | 跨 agent 迁移 / Agent Migration |
| 年度大修 | 年度大修 / Annual Maintenance |

### 10.4 字段/方法类（10 条）

| v1.0 | v3.0 |
|---|---|
| `routing` 顶层 | **不存在**（路由在 IDENTITY.md） |
| `heartbeat` 顶层 | **不存在**（心跳在 HEARTBEAT.md） |
| `subagents` 顶层 | **不存在** |
| `workspace` 顶层 | **不存在**（工作区是固定路径） |
| `runtime` 顶层 | **不存在** |
| `memory` 顶层 | **不存在**（记忆在 MEMORY.md） |
| `drift.flag` | `drift.last_score`（浮点） |
| `compaction.trigger` | `compaction.trigger`（保留） |
| `boundaries.allowed` | `boundaries.allowed/forbidden/needs_confirm` |
| `priority` 字段 | `priority`（保留，0-10） |

### 10.5 工具/命令类（5 条）

| v1.0 | v3.0 |
|---|---|
| `openclaw init` | `openclaw setup` |
| `openclaw chat --prompt` | `openclaw agent --message` |
| `openclaw plugin` | `openclaw plugins`（复数） |
| `openclaw nodes` | `openclaw nodes`（保留） |
| `openclaw backup` | `openclaw backup`（保留） |

> ⚠️ 全部 35 条以 `00-术语对照表·v3.0行业标准版.md` 为准；本表为 SOP 卷简化版索引。

---

## 十一、诚实边界与本机基线

### 11.1 本机实测基线（2026-09-27）

| 项 | 数值 | 来源 |
|---|---|---|
| OpenClaw 版本 | 2026.9.4 (3a9d69d) | `openclaw --version` |
| CI live 版本 | 2026.9.6 (eb377ac) | 差异诚实标注 |
| Node 版本 | 22 LTS | `node --version` |
| macOS | 26.x | 本机 |
| agent 数 | 18 在编 | `~/.openclaw/workspace/agents/` |
| automation 数 | 43 条 | `launchctl list` |
| plugins | 51/69 启用 | 含 CASE-10 a2a 18 个 disabled |
| skills | 236 个 | `~/.openclaw/workspace/skills/` |
| heartbeat peter error | 70x | 真实日志计数 |
| heartbeat kunlun error | 99+x | 真实日志计数 |

### 11.2 真名实测（已确认）

| 真名 | 验证方式 | 状态 |
|---|---|---|
| `openclaw setup` | `openclaw setup --help` | ✅ |
| `openclaw agents add` | `openclaw agents --help` | ✅ |
| `openclaw agent --agent X --message Y` | 实际跑过 | ✅ |
| `openclaw health` / `openclaw doctor` | 实际跑过 | ✅ |
| `openclaw backup create` | 实际跑过 | ✅ |
| `openclaw plugins`（复数） | `openclaw plugins --help` | ✅ |
| `~/.openclaw/openclaw.json`（真名路径） | `ls -la` | ✅ |

### 11.3 已实测范围（所有 SOP 共有）

- 命令骨架 / 文件结构 / 目录创建
- JSON / YAML / plist 解析脚本
- Python 脚本骨架与占位逻辑
- launchd plist 模板结构
- 18 agent 路径 + 236 skills 计数 + 51/69 plugins 比例
- 真名命令 + 真名路径

### 11.4 待实测范围（每个 SOP 诚实边界标 ⏳）

- 所有 SOP "端到端真实跑通"（需生产事故/演练触发）
- 真实 LLM 评分（drift_scan 当前为占位）
- live 2026.9.6 vs 本机 2026.9.4 全量差异
- 多次年度大修闭环（需运行 1+ 年）
- 30 SOP 全部跨分册引用一致性（需手动对账）

### 11.5 ⚠️ 不可在生产裸做的命令

> 本卷所有"破坏性"操作（删文件、停 gateway、改 SOUL、回滚）都强调**先备份 + 沙箱先行**。列出不可裸做命令：

| 命令 | 风险 | 应先做 |
|---|---|---|
| `pkill -f openclaw` | 失联 | SOP-13 + SOP-15 |
| `npm install -g openclaw@latest` | 升级翻车 | SOP-4（备份） |
| `rm -rf ~/.openclaw` | 删配置 | SOP-5（备份拷出） |
| `sed -i '...' SOUL.md` | 改 SOUL | SOP-25（工单） |
| `mv AGENTS.md <back>` | 协议失效 | SOP-9（边界） |
| `sed -i '...' IDENTITY.md` | 路由断 | SOP-29（迁移工单） |

---

## 十二、本卷作者与版本

| 项 | 值 |
|---|---|
| 卷名 | SOP 大全卷 |
| 卷号 | P2-1（v5.0 industry-standard 第 2 阶段第 1 部分） |
| 版本 | v5.0.0 |
| 实测日期 | 2026-09-27 |
| 作者 | 丘总（拍板） + 硅基军团（执行） |
| License | MIT（可自由复制、修改、分发，保留版权即可） |
| 总行数 | 约 5,500 行（含本 README） |
| 文件数 | 6 个分册 + 1 个 README = 7 文件 |
| SOP 数 | 30（5×6） |
| 平均每 SOP 行数 | ~135 行（4,501 行 ÷ 30 ≈ 150 - 分册头开销） |
| 范围限制 | 仅 30 SOP，不超出 |
| 与 v1.0 关系 | 全部从零编写，不抄 v1.0 原文，仅交叉引用 |
| 与 v4.0 关系 | 全部从零编写，引用其 8 卷 + 4 接口层结构 |

---

## 十三、Appendix · 业界对位表

| 手册概念 | 业界对位 | 说明 |
|---|---|---|
| Agent Fleet（智能体集群/军团） | Multi-agent System / Agent Fleet | 本机 18 agent |
| Gateway（网关） | Gateway / Control Plane | OpenClaw 控制面 |
| Node（节点） | Edge Node / Paired Device | 多设备配对 |
| Sandbox（沙箱） | Sandbox / Isolated Runtime | 试验隔离 |
| Backup（备份） | Snapshot / Backup | `openclaw backup create` |
| HEARTBEAT.md（心跳） | Liveness Probe / Watchdog Timer | fast/medium/slow |
| Cron | Cron / Scheduled Jobs | macOS launchd |
| 暗夜熔炉 | Chaos Drill / GameDay | 主动演练 |
| 失联恢复 | Failover / Reconnection Recovery | 30 min MTTR 目标 |
| 告警链 | Alerting Pipeline / On-call | L1/L2/L3 |
| MEMORY 5 层 | Tiered Memory / Hierarchical Memory | L1-L5 |
| Compaction | Context Compaction / Sliding Window | 触发 0.7 |
| 训练轮次 | Training Curriculum / Skill Levels | L1/L2/L3 |
| 双三角模型 | Expectation-Actuality-Feedback | EAF |
| Mentor | Mentor / Coach Agent | 介入曲线 |
| Drift Scan | Compliance Scan / Drift Detector | 阈值 0.20 |
| 边界三档 | RBAC / Permission Tiers | Allowed/Forbidden/Needs-Confirm |
| 每周体检 | Weekly Compliance Review | 周一 09:00 |
| TEV 三证 | Three-Evidence Verification | v1.0 卷六 |
| 工单 | Remediation Ticket | tickets/open/closed |
| 事故分级 | Incident Severity (SEV-1/2/3/4) | P0-P3 |
| RYP | Task Preemption / Yield Protocol | 抢话 |
| 数据回滚 | Point-in-time Recovery | backup |
| 跨 agent 迁移 | Agent Migration / Workload Transfer | priority 0 |
| 年度大修 | Annual Maintenance / Major Release | v5→v6 |

---

## 十四、Appendix · 来源标注（v1.0/v4.0/v3.0）

### 14.1 v1.0 经典体系（仅作为方法论溯源，本卷不抄原文）

| v1.0 卷 | 主题 | 本卷对应 SOP |
|---|---|---|
| 卷五 | 会话污染与清理 | SOP-28（回滚）+ SOP-27（让位失败=污染） |
| 卷六 | TEV 三证 | SOP-24 |
| 卷七 | 三省制 | SOP-20（自省/互省/上省）+ SOP-25（三层） |

### 14.2 v4.0 8 卷 + 4 接口层（结构参照，本卷按 12 章横向引用）

| v4.0 | 本卷对应 |
|---|---|
| 8 卷 | chapters/01-getting-started → chapters/08-evolution |
| 4 接口层 | chapters/09-mcp-binding、10-a2a-binding、11-skill-registry、12-plugin-entrypoint |

### 14.3 v3.0 改名表 35 条

> 全部 35 条以 `00-术语对照表·v3.0行业标准版.md` 为准，本卷第 10 节为其索引版。

### 14.4 本机实测差异化标注

- **版本差异**：CI 报告 live 2026.9.6 (eb377ac)，本机 2026.9.4 (3a9d69d)
- **agent 数**：本机 18 agent；老文档 12 agent 系过时口径
- **plugins**：本机 51/69；18 disabled 含 a2a（CASE-10）
- **heartbeat**：本机 peter 70x / kunlun 99+x 为真实基线
- **automation**：本机 43 条；老文档 30 条系基数差异

---

## 十五、Appendix · 练手清单

> 给读者的练手 SOP 组合（由易到难）。

### 等级 1：新人 30 分钟

- [ ] 读 SOP-1 + SOP-3
- [ ] 在沙箱跑一次 setup
- [ ] 验证 health

### 等级 2：扩 agent 2 小时

- [ ] 读 SOP-6/7/8/9/10
- [ ] 用模板加 1 个新 agent
- [ ] 用 SOP-16 配 5 层
- [ ] 用 SOP-11 配心跳

### 等级 3：治理 1 天

- [ ] 读 SOP-21/22/23
- [ ] 跑 drift_scan.py 看 18 agent 当前分
- [ ] 写 weekly_audit.sh 跑一次
- [ ] 建 1 张整改工单（SOP-25）

### 等级 4：演练 半天

- [ ] 读 SOP-14
- [ ] 沙箱跑剧本 A
- [ ] 验证 breaker + L1 告警
- [ ] 写 forge-log

### 等级 5：事故响应 1 天

- [ ] 读 SOP-13/15/26
- [ ] 沙箱模拟失联 → 走 SOP-15
- [ ] 故意让恢复失败 → 走 SOP-26
- [ ] 演练 SOP-27 抢话冲突

### 等级 6：年度大修（等年底）

- [ ] 读 SOP-30
- [ ] 跑 annual_audit.sh
- [ ] 续期 5 项
- [ ] 升 v6.0 主版本 + TEV（SOP-24）

---

## 附录：本卷使用建议

1. **新读者**：先看第 4 节"场景化 SOP 矩阵" + 第 5 节"决策树"，再按主线 1 跑 SOP-1/3/11
2. **治理员**：常驻 SOP-21/22/23/24/25 五个，每周跑一次 SOP-23
3. **on-call**：打印第 7 节"速查卡片"贴在工位
4. **写新 SOP 的作者**：参考第 8 节交叉链接 + 第 10 节术语规范 + 第 11 节诚实边界模板
5. **审计/Supervisor**：用第 14 节溯源对账每一处 v1.0 引用是否得当

## 附录：常见反模式（v5.0 应避免）

- ❌ 整文件复制 v1.0 / v4.0 原文当 SOP（→ 重写为 v5.0 6 步式）
- ❌ 用虚构命令如 `openclaw init`（→ 全部用真名表第 9 节）
- ❌ 漂移检测"感觉"判定（→ 必须 SOP-21 阈值 0.20）
- ❌ 升级 OpenClaw 不做备份（→ SOP-4 步骤 1）
- ❌ 改 SOUL 不走工单（→ SOP-25）
- ❌ 工单口头谈不落盘（→ tickets/open/<id>.md）
- ❌ 跳过 TEV 直接上线（→ SOP-24 三证齐全）
- ❌ 漂移分 >0.50 不建工单（→ SOP-25）

---

> **本 README 由 P2-1 SOP 大全卷任务产出 · 2026-09-27 · 丘总拍板 · v5.0 industry-standard**
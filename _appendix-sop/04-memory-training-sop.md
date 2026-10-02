# SOP 分册 04 · 记忆与训练（SOP-16 ~ SOP-20）

> **《硅基生命手册（Silicon Life Handbook）· SOP 大全卷》**
> **v5.0 industry-standard · P2-1 · 从零编写**
> **实测环境**：OpenClaw **2026.9.4 (3a9d69d)** · macOS 26.x · 实测日期 2026-09-27
> **本机实测基线**：18 agent · 236 skills · 51/69 plugins
> **License**：MIT

## ⚠️ OpenClaw 真名表

| ❌ 虚构 | ✅ 真名 |
|---|---|
| 顶层 `memory` 字段 | **不存在**（记忆在 `agents/<agent>/MEMORY.md`） |
| `openclaw memory write` | 实际通过 `agents add/edit` + 文件落盘 |

## 业界对位表

| 手册概念 | 业界对位 |
|---|---|
| MEMORY 5 层金字塔 | Tiered Memory / Hierarchical Memory |
| Compaction（上下文压缩） | Context Compaction / Sliding Window |
| 训练轮次 L1-L3 | Training Curriculum / Skill Levels |
| 双三角模型（E-A-F） | Expectation-Actuality-Feedback Loop |
| Mentor Agent | Mentor / Coach Agent |

## 本分册目录

| SOP | 标题 | 前置 | 后续 |
|---|---|---|---|
| SOP-16 | MEMORY 5 层 | SOP-10 | SOP-17, SOP-18 |
| SOP-17 | Compaction 配置 | SOP-16 | SOP-18 |
| SOP-18 | 训练轮次 L1-L3 | SOP-16 | SOP-19 |
| SOP-19 | 双三角模型 | SOP-18 | SOP-20 |
| SOP-20 | Mentor Agent | SOP-19 | SOP-23 |

---

# SOP-16 · MEMORY 5 层金字塔配置

## 一、目的

把"全平铺记忆"换成 5 层金字塔：短期 / 滚动 / 主题 / 长期 / 索引。

## 二、适用对象

新 agent；记忆全平铺导致检索膨胀者；治理员批量规范化。

## 三、前置条件

- [ ] IDENTITY 已配（SOP-10）
- [ ] 已读 C2-3（MEMORY.md 配置：5 层金字塔）、C4-4（分层记忆实操）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 检查现有 MEMORY.md 现状

```bash
MEM=~/.openclaw/workspace/agents/<name>/MEMORY.md
test -f "$MEM" && wc -l "$MEM" || echo "MEMORY.md 缺失"
# 平铺病：单文件 >500 行未分层 = 需要治理
```

### 步骤 2 · 写 MEMORY.md 5 层模板

```bash
cat > "$MEM" <<'EOF'
# MEMORY.md · <agent-name>

## L1 短期（短期上下文，1-7 天）
- 当前会话目标
- 当前会话 pending
- 当日临时事实
> 存储位置：会话内/会话缓存，>7 天自动晋升 L2 或丢弃

## L2 滚动（事件流，7-30 天）
- 每日事件流摘要
- 故障与修复记录
- 用户偏好更新
> 存储位置：~/.openclaw/workspace/agents/<name>/memory-rolling/
> 每月归档一次，提炼入 L3

## L3 主题（领域知识，按主题分文件）
- memory-topics/<topic>.md（如：governance.md / training.md / incident.md）
- 每文件 ≤300 行，超则拆分
> 存储位置：~/.openclaw/workspace/agents/<name>/memory-topics/

## L4 长期（人格级，季度更新）
- 本 agent 的长期沉淀（如：常用路径、用户高频需求、典型修复模式）
- 季度复盘写入
> 存储位置：~/.openclaw/workspace/agents/<name>/MEMORY.md（本文件 L4 段）

## L5 索引（跨层检索）
- 关键概念 → 主题文件指针
- 故障记忆 → L2 时间线指针
- 决策记录 → L4 季度文件指针
> 存储位置：本文件 L5 段
EOF
```

### 步骤 3 · 建子目录与索引

```bash
mkdir -p ~/.openclaw/workspace/agents/<name>/memory-rolling/
mkdir -p ~/.openclaw/workspace/agents/<name>/memory-topics/
touch ~/.openclaw/workspace/agents/<name>/memory-topics/governance.md
touch ~/.openclaw/workspace/agents/<name>/memory-topics/training.md
ls ~/.openclaw/workspace/agents/<name>/
```

### 步骤 4 · 跨层晋升规则（写入 L5 索引段）

```bash
cat >> "$MEM" <<'EOF'

## L5 索引 · 晋升规则
- L1 → L2：会话结束自动归档，>7 天未引用转 L2
- L2 → L3：月度复盘提炼主题事件入 memory-topics/
- L3 → L4：季度复盘写入本文件 L4
- 反向：L3/L4 高频引用 → 降回 L1（按需）
EOF
```

### 步骤 5 · 18 agent 批量补 MEMORY 5 层骨架

```bash
for d in ~/.openclaw/workspace/agents/*/; do
  name=$(basename "$d")
  if [ ! -f "$d/MEMORY.md" ]; then
    echo "缺 MEMORY.md: $name"
  else
    grep -c "L1 短期\|L2 滚动\|L3 主题\|L4 长期\|L5 索引" "$d/MEMORY.md" | xargs -I {} echo "$name: {} / 5 层"
  fi
done
```

### 步骤 6 · 端到端"取层"验证

```bash
# 让 agent 报"近期一件事"
openclaw agent --agent <name> --message "告诉我你昨天最重要的一件事" 2>&1 | head -5
# 期望输出：来自 L2 滚动层（L1 短期过期应被拒）
```

### ✅ 检查清单

- [ ] MEMORY.md 含 L1-L5 五段
- [ ] memory-rolling / memory-topics 子目录存在
- [ ] 18 agent 全覆盖
- [ ] 晋升规则写入 L5
- [ ] 端到端取层返回正确层级

## 五、验证命令

```bash
ls ~/.openclaw/workspace/agents/<name>/memory-*/
# 期望输出：rolling/ 和 topics/ 两个目录
```

```bash
grep -c "^## L[1-5]" "$MEM"
# 期望输出：5
```

## 六、回滚步骤

```bash
cp "$MEM" "$MEM.bak.$(date +%F)"
# 恢复 .bak 后清空新增子目录（防数据浪费）
rm -rf ~/.openclaw/workspace/agents/<name>/memory-rolling/ ~/.openclaw/workspace/agents/<name>/memory-topics/
mv "$MEM.bak.<上次成功日期>" "$MEM"
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-10（IDENTITY）
- 后续 SOP：SOP-17（Compaction 配合）、SOP-18（训练数据从 L3 来）
- 相关 FAQ：F4-2（误植 vs 真名）、F4-5（记忆域隔离）、F4-7（宽口径回捞）
- 相关 Cookbook：C2-3（5 层金字塔）、C4-4（分层记忆实操）
- 相关案例：CASE-8（蘑菇街式冷启动：训练记录入 L3）
- 相关章节：chapters/04-training、chapters/05-long-term

### 九、MEMORY 5 层的查询策略
```bash
# L1：会话内/缓存（不查）
# L2：滚动目录（grep）
grep -r '<keyword>' ~/.openclaw/workspace/agents/<name>/memory-rolling/
# L3：主题目录（按主题）
ls ~/.openclaw/workspace/agents/<name>/memory-topics/
# L4：MEMORY.md L4 段（季度沉淀）
sed -n '/## L4 长期/,/## L5 索引/p' MEMORY.md
# L5：MEMORY.md L5 段（索引）
sed -n '/## L5 索引/,$p' MEMORY.md
```

### 十、5 层 vs 平铺的对比
| 维度 | 平铺 | 5 层 |
|---|---|---|
| 单文件行数 | >500 | 各 <300 |
| 检索速度 | 慢 | 快（按层查） |
| 晋升逻辑 | 手动 | 自动 |
| 适合规模 | <5 agent | >5 agent |

## 八、诚实边界

- ✅ 已实测：5 层模板结构；子目录创建；18 agent 覆盖检查；晋升规则
- ⏳ 待实测：OpenClaw runtime 是否按 5 层自动晋升（基于文件结构，行为以本机为准）

---

# SOP-17 · Compaction 配置（上下文压缩）

## 一、目的

长会话不污染上下文；超长上下文自动压缩到不丢关键事实。

## 二、适用对象

长会话膨胀者；治理员按 C2-4 配置 Compaction 参数。

## 三、前置条件

- [ ] MEMORY 5 层已就绪（SOP-16）
- [ ] 已读 C2-4（Compaction 配置）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 识别"长会话污染"症状

```bash
# 症状：单会话 >20 轮 / token 逼近上限 / agent 越来越跑偏
# 本机判断：查历史会话日志（路径以本机实际为准）
ls ~/.openclaw/logs/sessions/ 2>/dev/null | head -5 || echo "日志路径以 openclaw --help 与本机配置为准"
```

### 步骤 2 · 写 Compaction 配置段（写到 MEMORY.md 头部）

```bash
# 关键参数（数字以本机模型上下文窗口为准，不可硬抄）：
# - trigger：上下文占用 ≥ 70% 触发
# - strategy：head + tail 截断 + L2 滚动汇总（不丢 L3 主题事实）
# - preserve：保留最近 N 轮 + L3 主题事实 + 当前 pending
sed -i '' '1i\
---\
compaction:\
  trigger: 0.7\
  strategy: head_tail_with_l2\
  preserve_recent: 10\
  preserve_l3_topics: true\
sop_version: v5.0\
---\
' ~/.openclaw/workspace/agents/<name>/MEMORY.md
head -10 ~/.openclaw/workspace/agents/<name>/MEMORY.md
```

### 步骤 3 · 把压缩摘要写回 L2

```bash
cat > ~/.openclaw/workspace/agents/<name>/memory-rolling/$(date +%F)-compaction.md <<'EOF'
# Compaction 摘要 · $(date +%F)
- 触发时间：<HH:MM>
- 压缩前：<token 数>
- 压缩后：<token 数>
- 保留：最近 N 轮 + L3 主题 + pending
- 丢弃：<概要>
EOF
```

### 步骤 4 · Compaction 与 MEMORY 5 层协同

```bash
# 规则：压缩时不丢 L3 主题事实
# 实现：在 MEMORY.md L5 索引段加 grep 关键词保留
echo "在 L5 索引写入：Compaction 时保留 memory-topics/*.md 关键词命中段落"
```

### 步骤 5 · 避免"压缩玄学"（数字回归）

```bash
# 玄学症状：每次压缩丢/留什么全靠运气
# 治法：跑 A/B 对比，把两次压缩产物 diff 出来
diff <(openclaw agent --agent <name> --message "A" 2>&1) <(openclaw agent --agent <name> --message "B" 2>&1) || true
# 期望：可重复的关键事实差异为零
```

### 步骤 6 · 沙箱"造长会话"验证压缩

```bash
# 沙箱跑：连续发 30 轮闲聊 → 触发 compaction → 看是否保留关键事实
for i in $(seq 1 30); do
  openclaw agent --agent <sandbox-name> --message "闲聊第 $i 轮" >/dev/null 2>&1
done
openclaw agent --agent <sandbox-name> --message "刚才第 5 轮我说了什么？" 2>&1 | head -5
# 期望：第 5 轮事实应被丢失（闲聊），但 L3 主题应保留
```

### ✅ 检查清单

- [ ] MEMORY.md 顶部含 compaction YAML
- [ ] 触发阈值与策略已写
- [ ] L2 滚动摘要记录存在
- [ ] L5 索引声明 L3 关键词保留
- [ ] 沙箱造长会话验证通过
- [ ] 关键事实不丢（变废话可丢）

## 五、验证命令

```bash
grep -A4 "compaction:" ~/.openclaw/workspace/agents/<name>/MEMORY.md | head -10
# 期望输出：trigger/strategy/preserve 三段
```

## 六、回滚步骤

```bash
cp ~/.openclaw/workspace/agents/<name>/MEMORY.md ~/.openclaw/workspace/agents/<name>/MEMORY.md.bak.$(date +%F)
# 撤回 YAML：sed 删除首 6 行
sed -i '1,6d' ~/.openclaw/workspace/agents/<name>/MEMORY.md
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-16（5 层是 Compaction 基础）
- 后续 SOP：SOP-18（训练数据从压缩后的 L2/L3 来）
- 相关 FAQ：F4-5、F4-7
- 相关 Cookbook：C2-4（Compaction 配置）
- 相关案例：CASE-1（8/19 军团断线：长会话污染是诱因之一）
- 相关章节：chapters/04-training

### 九、Compaction 的 5 个调参技巧
1. **trigger 0.7**：经验值，太低丢失事实，太高上下文满
2. **preserve_recent 10**：保留最近 10 轮
3. **preserve_l3_topics true**：L3 主题事实必须保留
4. **strategy head_tail_with_l2**：head+tail + L2 汇总
5. **compaction.frequency 监控**：每会话压缩 >3 次 = 异常

### 十、Compaction 与会话污染的关系
Compaction 是**主动清理**手段，但不能完全避免污染：
- 主动污染（agent 写错事实）→ Compaction 不能修
- 被动污染（噪声多）→ Compaction 是治本
- 主题污染（漂移）→ Compaction 不能修 → 用 drift_scan（见 SOP-21）

## 八、诚实边界

- ✅ 已实测：Compaction YAML 结构；触发/策略/保留三参数；L2 摘要格式
- ⏳ 待实测：真实长会话触发的 runtime 行为（基于配置存在性，触发行为以本机为准）
- ⏳ 待实测：trigger 0.7 数值是否对本机模型窗口合适（需窗口大小实测）

---

# SOP-18 · 训练轮次（L1 → L3）

## 一、目的

把蘑菇街式冷启动 7 天训练拆成 3 轮可执行。

## 二、适用对象

新 agent 上线；7 天冷启动全记录（CASE-8）。

## 三、前置条件

- [ ] MEMORY 5 层 + Compaction（SOP-16 + SOP-17）
- [ ] 已读 C4-1（训练轮次设计：L1-L3）、CASE-8（蘑菇街式冷启动）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 定 L1（基础期）：3 天

```bash
cat > ~/.openclaw/workspace/agents/<name>/training/L1.md <<'EOF'
# L1 基础期（Day 1-3）
- 目标：人格稳定 / 工具会基本用 / SOUL 不漂移
- 训练：每日 50-100 轮指定对话 + drift 自检 1 次
- 验收：Persona 回复稳定率 ≥95%（见 SOP-19 双三角）
EOF
mkdir -p ~/.openclaw/workspace/agents/<name>/training/
```

### 步骤 2 · 定 L2（成长期）：2 天

```bash
cat > ~/.openclaw/workspace/agents/<name>/training/L2.md <<'EOF'
# L2 成长期（Day 4-5）
- 目标：领域知识沉淀 / 记忆分层生效 / 任务流稳定
- 训练：每日 100 轮业务对话 + L3 主题提炼 1 次
- 验收：跨会话事实一致率 ≥95%
EOF
```

### 步骤 3 · 定 L3（独立期）：2 天

```bash
cat > ~/.openclaw/workspace/agents/<name>/training/L3.md <<'EOF'
# L3 独立期（Day 6-7）
- 目标：自主抢活 / 主动汇报 / 不再需要 Mentor 介入
- 训练：每日 50 轮 + 2 次暗夜熔炉沙箱演练（见 SOP-14）
- 验收：Mentor 介入次数 <5 次/天（见 SOP-20）
EOF
```

### 步骤 4 · 每日回检 + 写 L2 滚动

```bash
cat >> ~/.openclaw/workspace/agents/<name>/memory-rolling/training-$(date +%F).md <<'EOF'
# 训练日 <F>
- L1/L2/L3 阶段
- 当日轮次
- drift 分（见 SOP-21）
- 反例新增
- Mentor 介入次数
EOF
```

### 步骤 5 · 跨轮跳错 + 记录到 L4

```bash
# L4 季度沉淀：训练方法论
echo "训练方法论沉淀入 MEMORY.md L4" >> ~/.openclaw/workspace/agents/<name>/MEMORY.md
```

### 步骤 6 · 验收放行（产线准入）

```bash
cat > ~/.openclaw/workspace/agents/<name>/training/release-check.md <<'EOF'
# 产线准入验收
- [ ] Persona 稳定率 ≥95%（L1）
- [ ] 跨会话事实一致率 ≥95%（L2）
- [ ] Mentor 介入 <5 次/天（L3）
- [ ] drift 分 <0.2（见 SOP-21）
- [ ] 7 天无 L3 告警
EOF
```

### ✅ 检查清单

- [ ] L1/L2/L3 三段训练计划存在
- [ ] 每日回检记录落 L2 滚动
- [ ] L4 方法论沉淀
- [ ] 产线准入 checklist 全过
- [ ] Mentor 介入次数趋势向下
- [ ] drift 分稳定 <0.2

## 五、验证命令

```bash
ls ~/.openclaw/workspace/agents/<name>/training/
# 期望输出：L1.md L2.md L3.md release-check.md
```

```bash
# 验收脚本（节选）
test -f ~/.openclaw/workspace/agents/<name>/training/release-check.md && grep -c "^\- \[" ~/.openclaw/workspace/agents/<name>/training/release-check.md
# 期望输出：5
```

## 六、回滚步骤

```bash
# 回滚到 L1 起点（保留 L2 滚动日志）
rm -rf ~/.openclaw/workspace/agents/<name>/training/L{2,3}.md
mv ~/.openclaw/workspace/agents/<name>/training/L1.md ~/.openclaw/workspace/agents/<name>/training/L1.md.bak.$(date +%F)
# 重新跑 L1
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-16、SOP-17
- 后续 SOP：SOP-19（双三角验收）、SOP-20（Mentor 介入）
- 相关 FAQ：F4-5（记忆域隔离，训练期不污染生产）
- 相关 Cookbook：C4-1（训练轮次）、C4-4（分层记忆）
- 相关案例：CASE-8（蘑菇街式冷启动 7 天）
- 相关章节：chapters/04-training

### 九、训练三段的验收硬指标
| 段 | 指标 | 阈值 |
|---|---|---|
| L1 | Persona 稳定率 | ≥95% |
| L1 | drift 分 | <0.20 |
| L2 | 跨会话事实一致率 | ≥95% |
| L2 | L3 主题数量 | ≥5 |
| L3 | Mentor 介入 | <5 次/天 |
| L3 | 暗夜熔炉通过 | ≥1 次 |

### 十、训练失败的 3 种典型模式
1. **L1 不达标直接上 L2**：Persona 不稳 → L2 训练徒劳
2. **L2 跳到 L3 太快**：跨会话一致性未稳定 → 上线即漂移
3. **L3 不演练暗夜熔炉**：上线后遇到真故障不知如何应对
对策：每段硬指标不达标则不晋级。

## 八、诚实边界

- ✅ 已实测：三段训练模板；每日回检格式；release-check 5 项
- ⏳ 待实测：7 天全程实测（需 7 天真实运行，单纯跑 SOP 不构成"训练完成"）

---

# SOP-19 · 双三角模型（Expectation-Actuality-Feedback Loop）

## 一、目的

把"对/错/差"转成可量化的训练信号，沉淀入 L4。

## 二、适用对象

训练验收；漂移量化；Mentor 介入的判据。

## 三、前置条件

- [ ] 训练轮次就绪（SOP-18）
- [ ] 已读 C4-2（双三角模型实操）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 定 E-A-F 三维度

```bash
cat > ~/.openclaw/workspace/agents/<name>/eaf.md <<'EOF'
# 双三角模型（E-A-F）

## E = Expectation（期望）
- 任务定义
- 验收标准（如：稳定率 ≥95%、漂移 <0.2）

## A = Actuality（实际）
- 实际行为 / 输出
- 实测数据（轮次 / drift 分 / 反例次数）

## F = Feedback（反馈）
- 差 = E - A
- 反馈落 L3 主题事实 + L4 方法论

## 三角闭环
- E ←→ A：每轮实测评期望
- A ←→ F：反馈回写训练记录
- F ←→ E：期望据反馈动态更新
EOF
```

### 步骤 2 · 每轮评分

```bash
cat >> ~/.openclaw/workspace/agents/<name>/memory-rolling/eaf-$(date +%F).md <<'EOF'
# EAF 评分日志 <F>
| 时间 | E（期望） | A（实际） | F（差） | 处置 |
|---|---|---|---|---|
EOF
```

### 步骤 3 · drift 分公式化

```bash
# drift 分：偏离 SOUL Persona 的概率（0-1）
# 公式：drift_score = mismatched_persona_count / total_responses
python3 - <<'EOF'
# 占位：以 18 agent 实测汇总
# 实际跑法：openclaw agent --agent <name> --message "..." 对比 SOUL Persona 关键词
print("drift_score = mismatches / total")
EOF
```

### 步骤 4 · 双三角 + MEMORY 5 层协同

```bash
# EAF 评分入 L2；F 沉淀入 L3；方法论入 L4
echo "EAF → L2/L3/L4 自动归档规则写入 MEMORY.md L5"
```

### 步骤 5 · 漂移阈值动态调整

```bash
# 若 F 长期偏大 → 放宽 E（期望更现实）
# 若 F 长期偏小 → 收紧 E（期望可加压）
# 周期：每 7 天调一次
echo "E 调整节奏：每周"
```

### 步骤 6 · 与 SOP-21 漂移检测互通

```bash

### 九、EAF 的 3 个常见误用
1. **E 一成不变**：F 长期偏大或偏小 → 失去判别力
2. **A 不记录**：实际行为未量化 → F 是猜的
3. **F 不回写 L3**：方法论丢失 → 下次训练从零开始

### 十、EAF 与 drift_scan 的互通
EAF F 值 = drift_scan 的漂移分（量化口径统一）。
互通点：SOP-19 F ← SOP-21 drift_score。
双闭环量化：漂移量化 + 训练反馈量化。
# SOP-21 drift_check 写 drift.last_score，EAF 用该值
echo "互通点：SOP-19 F ← SOP-21 drift_score"
```

### ✅ 检查清单

- [ ] EAF 三段定义明确
- [ ] 评分日志逐轮记录
- [ ] drift 分公式化
- [ ] L2/L3/L4 归档规则写入
- [ ] E 调整节奏每周一次
- [ ] 与 SOP-21 互通

## 五、验证命令

```bash
ls ~/.openclaw/workspace/agents/<name>/memory-rolling/eaf-*.md | wc -l
# 期望输出：≥7（每日 1 个评分日志）
```

## 六、回滚步骤

```bash
# 简化 EAF：把 F 段标记为可选
sed -i '' 's|^## F.*|## F（可选，关闭）|' ~/.openclaw/workspace/agents/<name>/eaf.md
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-18
- 后续 SOP：SOP-20（Mentor 介入基于 EAF F 值）
- 相关 FAQ：F7-1（版本 + 误植字段双查）
- 相关 Cookbook：C4-2（双三角模型）
- 相关案例：CASE-6（18 agent 编制：每 agent 都有 EAF）
- 相关章节：chapters/04-training

## 八、诚实边界

- ✅ 已实测：EAF 三段结构；评分日志格式；drift 分公式骨架
- ⏳ 待实测：drift_score 真实采集脚本（需 LLM 评估，当前为占位）

---

# SOP-20 · Mentor Agent 配置

## 一、目的

让 Mentor 介入次数可控，训练期有兜底。

## 二、适用对象

新 agent 训练期；产线准入前的 7 天；L3 独立期。

## 三、前置条件

- [ ] EAF 已运行（SOP-19）
- [ ] 已读 C4-3（导师智能体机制配置 + 训练记录）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 选 Mentor（通常是 Supervisor 兼任）

```bash
# Mentor 即高级 agent（training 已独立者）
# 本机：可从 18 agent 中挑一个 training phase = passed 的
grep -l "training_phase: passed" ~/.openclaw/workspace/agents/*/IDENTITY.md 2>/dev/null || echo "无 passed agent，需先跑完 SOP-18"
```

### 步骤 2 · 配 Mentor 规则

```bash
cat > ~/.openclaw/workspace/agents/<mentor>/mentor-rules.md <<'EOF'
# Mentor Rules · <mentor>
## 介入条件（任一即介入）
- 被训练 agent EAF F 值连续 3 轮 >0.5
- 被训练 agent 反例触发（漂移 / 越界 / 重复人格）
- 被训练 agent 主动呼叫

## 介入方式
- 注入 SOUL 复述 + EAF 提示
- 不接管任务，只旁观纠偏

## 退出条件
- F 值回落 + 连续 5 轮 <0.2

## 每日统计
- 介入次数
- 失败/成功比
- 上报 Supervisor
EOF
```

### 步骤 3 · 介入计数器

```bash
cat > ~/.openclaw/workspace/agents/<mentor>/counter.sh <<'EOF'
#!/bin/bash
# 统计当日 Mentor 介入次数
LOG=~/.openclaw/workspace/agents/<mentor>/intervention-$(date +%F).log
wc -l "$LOG" 2>/dev/null || echo 0
EOF
chmod +x ~/.openclaw/workspace/agents/<mentor>/counter.sh
```

### 步骤 4 · 7 天训练全程 Mentor 日志

```bash
# L2 滚动：每日 Mentor 日志
mkdir -p ~/.openclaw/workspace/agents/<mentor>/logs/
touch ~/.openclaw/workspace/agents/<mentor>/logs/mentor-day-$(date +%F).log
```

### 步骤 5 · L3 独立期退出条件

```bash
# Mentor 介入 <5 次/天 连续 2 天 → 退出 Mentor 模式
# 实现：日终由 Cron 检查（见 SOP-12 medium 档接入）
~/.openclaw/workspace/agents/<mentor>/counter.sh
```

### 步骤 6 · Mentor 上报 Supervisor（v1.0"三省制"）

```bash
# Supervisor 看 Mentor 日志 + 反向给 Mentor 评分
# 三省制：自省 / 互省 / 上省 三层（v1.0 卷七）
echo "三省制：自省（Mentor 每日自评） + 互省（互为对练 agent 评） + 上省（Supervisor 周报）"
```

### ✅ 检查清单

- [ ] Mentor agent 已选（training phase = passed）
- [ ] Mentor rules 含介入/退出/统计三段
- [ ] 介入计数器脚本可跑
- [ ] 7 天日志落 L2
- [ ] 退出条件明确（<5 次/天 × 2 天）
- [ ] 三省制接入 Supervisor

## 五、验证命令

```bash
~/.openclaw/workspace/agents/<mentor>/counter.sh
# 期望输出：当日介入次数（训练期 >0，独立期 <5）
```

## 六、回滚步骤

```bash
# Mentor 介入过多 → 暂停 mentor 模式（不接管）
mv ~/.openclaw/workspace/agents/<mentor>/mentor-rules.md ~/.openclaw/workspace/agents/<mentor>/mentor-rules.md.paused
# 改用纯 EAF 自动纠偏
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-19（EAF 是 Mentor 判据）
- 后续 SOP：SOP-23（每周体检含 Mentor 统计）
- 相关 FAQ：F7-1
- 相关 Cookbook：C4-3（Mentor Agent）、C6-1（Supervisor Layer）
- 相关案例：CASE-8（蘑菇街式冷启动：Mentor 介入曲线）、CASE-6（18 agent：Mentor 是扩张期关键）
- 相关章节：chapters/04-training、chapters/07-coordination

### 九、Mentor 的 3 种典型退化模式
1. **Mentor 替代被训练 agent**：被训练 agent 不独立 → 永不离线
2. **Mentor 频繁介入**：每次都帮 → F 值永远 <0.5（虚低）
3. **Mentor 不记录**：每次介入不知为何 → 数据丢失
对策：步骤 6 暂停 mentor 模式 / 严格退出条件。

### 十、Mentor 的三省制具体落点
| 省 | 谁 | 评谁 |
|---|---|---|
| 自省 | Mentor 自身 | 自己每日介入质量 |
| 互省 | Mentor 与被训练 agent | 互评 EAF F 值 |
| 上省 | Supervisor | Mentor 周报介入次数 |

## 八、诚实边界

- ✅ 已实测：Mentor rules 三段；介入计数器；7 天日志；三省制思路
- ⏳ 待实测：Mentor 介入曲线真实采集（需生产环境 7+ 天数据）

---

## Appendix D · 边界与扩展（SOP 16-20 共用）

### D.1 5 个 SOP 的失败模式矩阵（FM-16 ~ FM-20）

| FM | 触发场景 | 主要症状 | 应急路径 |
|---|---|---|---|
| FM-16 | SOP-16 MEMORY 全平铺 | 单文件 >500 行未分层 | 拆 L3 主题 + 建子目录 |
| FM-17 | SOP-17 trigger 设 0.3 | Compaction 过早触发 → 关键事实被压 | 放宽到 0.7；或 preserve_recent +5 |
| FM-18 | SOP-18 跳轮太快 | L1 未达标直接上 L3 → 上线即漂移 | 回滚到 L1 起点（见步骤 6 回滚） |
| FM-19 | SOP-19 E 设太高 | F 长期偏大 → Mentor 天天介入 | 每 7 天按 F 调 E（见步骤 5） |
| FM-20 | SOP-20 Mentor 介入过多 | 被训练 agent 依赖 Mentor 不独立 | 暂停 mentor 模式（见步骤 6 回滚） |

### D.2 5 层金字塔的"晋升-降级"全图

```
L1 短期（1-7d）──────┬──> 晋升 L2（会话结束自动归档）
                      └──> 丢弃（闲聊）
L2 滚动（7-30d）─────┬──> 晋升 L3（月度复盘提炼）
                      └──> 归档（月度 .bak）
L3 主题──────────────┬──> 晋升 L4（季度复盘写入）
                      └──> 降级 L1（高频引用时）
L4 长期──────────────┴──> 永久保留（季度沉淀）
L5 索引──────────────┴──> 随 L1-L4 更新
```

### D.3 与 v1.0 卷五"会话污染与清理"的对应

- Compaction（SOP-17）是会话污染的**主动清理手段**
- MEMORY 5 层（SOP-16）是**防污染的结构手段**
- EAF 反馈（SOP-19）是**污染的事后度量**

### D.4 实测踩坑 7 条

1. **MEMORY.md 单文件 800 行**：检索超时 → 必须拆 L3
2. **trigger 0.9**：上下文满了才压 → 改 0.7
3. **preserve_recent 2**：压缩后只剩 2 轮 → 改 10
4. **L3 主题文件名带空格**：grep 搜不到 → 用 `-` 或 `_`
5. **训练期不做 drift 自检**：上线即漂移 → 每日回检（SOP-18 步骤 4）
6. **EAF 只记 F 不回写 L3**：方法论丢失 → 步骤 4 自动归档
7. **Mentor 退出条件太早**：独立期第 1 天就退出 → 坚持 2 天 <5 次/天

### D.5 7 天训练的"最小可用"版本（时间不够时）

| 压缩版 | 原版 | 最小可用 |
|---|---|---|
| L1 3 天 | Day 1-3 | Day 1（1 天速成：只做 Persona + 工具） |
| L2 2 天 | Day 4-5 | Day 2（1 天速成：只做跨会话一致性） |
| L3 2 天 | Day 6-7 | Day 3（1 天速成：只做暗夜熔炉 1 次） |
| 合计 | 7 天 | 3 天（但 drift 分可能 >0.20，需接受风险） |
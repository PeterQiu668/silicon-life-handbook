# SOP 分册 06 · 事故与恢复（SOP-26 ~ SOP-30）

> **《硅基生命手册（Silicon Life Handbook）· SOP 大全卷》**
> **v5.0 industry-standard · P2-1 · 从零编写**
> **实测环境**：OpenClaw **2026.9.4 (3a9d69d)** · macOS 26.x · 实测日期 2026-09-27
> **本机实测基线**：18 agent · 43 条 automation · heartbeat peter error 70x / kunlun error 99+x
> **License**：MIT

## ⚠️ OpenClaw 真名表

| ❌ 虚构 | ✅ 真名 |
|---|---|
| `openclaw incidents declare` | 实际为 `openclaw doctor` 触发 + 自定义事故单 |
| `openclaw rollback` | 实际为 `openclaw backup create` 备份 + 文件 patch 恢复 |

## 业界对位表

| 手册概念 | 业界对位 |
|---|---|
| 事故分级 P0-P3 | Incident Severity (SEV-1/2/3/4) |
| 抢活让位 | Task Preemption / Response Yield Protocol |
| 数据回滚 | Data Rollback / Point-in-time Recovery |
| 跨 agent 迁移 | Agent Migration / Workload Transfer |
| 年度大修 | Annual Maintenance / Major Release |

## 本分册目录

| SOP | 标题 | 前置 | 后续 |
|---|---|---|---|
| SOP-26 | 事故分级 P0-P3 | SOP-15, SOP-25 | SOP-27, SOP-28 |
| SOP-27 | 抢活让位（RYP） | SOP-6, SOP-10 | SOP-26 |
| SOP-28 | 数据回滚 | SOP-1, SOP-25 | SOP-26, SOP-29 |
| SOP-29 | 跨 agent 迁移 | SOP-10, SOP-25 | SOP-30 |
| SOP-30 | 年度大修 | SOP-23, SOP-26 | 回到 SOP-1（新一年） |

---

# SOP-26 · 事故分级（P0-P3）

## 一、目的

把事故按影响半径+恢复时长定级，对应不同响应 SOP。

## 二、适用对象

L3 告警已响且 SOP-15 失联恢复失败的场景；on-call 上报。

## 三、前置条件

- [ ] SOP-15 失联恢复尝试已执行
- [ ] 已读 CASE-1（8/19 军团断线）、CASE-2（9/21 飞书事故）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 定级表

```bash
cat > ~/.openclaw/workspace/severity.md <<'EOF'
# 事故分级表
## P0（SEV-1）
- 影响：整个 agent fleet 不可用
- 恢复时长：>30 min
- 触发：全部 18 agent health != healthy
- 响应：丘总 + 全员 on-call + SOP-27 + SOP-28 + SOP-29 联动

## P1（SEV-2）
- 影响：核心 agent（Supervisor）不可用 + ≥5 agent 关联影响
- 恢复时长：>15 min
- 触发：Supervisor health != healthy
- 响应：on-call + SOP-15 + SOP-27

## P2（SEV-3）
- 影响：单个 agent 不可用 >30 min
- 恢复时长：15-30 min
- 触发：L3 告警 + SOP-15 重启失败
- 响应：on-call + 降级 + SOP-29

## P3（SEV-4）
- 影响：单 agent 单次失败
- 恢复时长：<15 min
- 触发：L2 告警
- 响应：on-call 记录 + SOP-25 工单
EOF
```

### 步骤 2 · 自动定级（基于心跳计数 + health）

```bash
cat > ~/.openclaw/workspace/jobs/severity_detect.sh <<'EOF'
#!/bin/bash
# 自动定级（基于 heartbeat-count.sh 输出与 health）
COUNT=$(~/.openclaw/workspace/jobs/heartbeat-count.sh | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(d.values()))" 2>/dev/null || echo 0)
HEALTH=$(openclaw health 2>&1 | grep -c healthy || echo 0)
if [ "$HEALTH" -lt 1 ]; then
  echo "P0：全部不可用"
elif [ "$COUNT" -gt 100 ]; then
  echo "P1：error 异常高"
else
  echo "P2/P3：常规"
fi
EOF
chmod +x ~/.openclaw/workspace/jobs/severity_detect.sh
~/.openclaw/workspace/jobs/severity_detect.sh
```

### 步骤 3 · 事故公告模板（按级分发）

```bash
cat > ~/.openclaw/workspace/incident-announce.md <<'EOF'
# 事故公告 · <P0/P1/P2/P3>
## 时间
## 影响
## 当前状态
## 临时绕行
## ETA
## 责任
EOF
```

### 步骤 4 · 升级路径

```bash
cat >> ~/.openclaw/workspace/severity.md <<'EOF'
# 升级路径
- P3 → P2：恢复超时 → 升级
- P2 → P1：关联影响 ≥5 agent → 升级
- P1 → P0：核心 Supervisor 失联 → 升级
- P0 → 业务/用户层：丘总授权 → 升级
EOF
```

### 步骤 5 · 关联 SOP 触发清单

```bash
# P0：SOP-15 + SOP-27 + SOP-28 + SOP-29 同时启动
# P1：SOP-15 + SOP-27
# P2：SOP-15（已完成）→ SOP-29（迁移）
# P3：SOP-25（工单）
echo "分级 → SOP 触发矩阵见 README.md"
```

### 步骤 6 · 事故结束 → 写复盘（→ CASE-1 候选）

```bash
# 复盘模板见 C7-2
cp ~/.openclaw/workspace/severity.md ~/.openclaw/workspace/incidents/<id>.md
# 好的复盘升格为 case-library 案例
```

### ✅ 检查清单

- [ ] P0-P3 分级表已写
- [ ] 自动定级脚本可跑
- [ ] 公告模板已存
- [ ] 升级路径明确
- [ ] 关联 SOP 触发清单
- [ ] 复盘归档落 incidents/

## 五、验证命令

```bash
~/.openclaw/workspace/jobs/severity_detect.sh
# 期望输出：当前级别
```

## 六、回滚步骤

```bash
# 定级过激 → 调阈值（更宽松）
sed -i '' 's/COUNT.*100/COUNT 500/' ~/.openclaw/workspace/jobs/severity_detect.sh
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-15、SOP-25
- 后续 SOP：SOP-27/28/29
- 相关 FAQ：F6-6（9/21 三查：通道/积压/白名单）
- 相关 Cookbook：C7-2（事故复盘模板）、C6-3（Response Yield Protocol）
- 相关案例：CASE-1（8/19 P0）、CASE-2（9/21 P1）、CASE-9（P3 累计成 P1）
- 相关章节：chapters/07-coordination、chapters/08-evolution

### 九、自动定级误判的 5 种情况
1. **health 假阴性**：实际在线但 health 报错 → 重试后再定级
2. **error 计数基线未更新**：peter 70x 是新基线 → 阈值需同步调
3. **关联影响未考虑**：单 agent 失败可能级联 → 看 routing 拓扑
4. **演练未排除**：暗夜熔炉引发的告警 → 标记演练
5. **on-call 不在场**：L3 响了无人接 → 升级到 P0

### 十、P0 触发后的分钟级动作
- **0-2 min**：on-call 接收 + 拉群 + 标注 P0
- **2-5 min**：跑 SOP-15 失联恢复 + 留证
- **5-15 min**：跑 SOP-27 抢活让位 + SOP-29 跨 agent 迁移
- **15-30 min**：跑 SOP-28 数据回滚（如需）
- **30+ min**：升级到业务/用户层通报

## 八、诚实边界

- ✅ 已实测：P0-P3 分级表；自动定级脚本骨架；升级路径
- ✅ 已实测：CASE-1/2/9 分级判定（事后分析）
- ⏳ 待实测：P0 真实触发的全军团响应（不到 P0 不希望测）

---

# SOP-27 · 抢活让位（Response Yield Protocol）

## 一、目的

多 agent 撞任务时，先抢后让，避免冲突与抢话。

## 二、适用对象

Supervisor 调度；agent fleet 并发；RYP 实操（C6-3）。

## 三、前置条件

- [ ] IDENTITY.md routing 已配（SOP-10）
- [ ] 已读 C6-3（Response Yield Protocol：抢活判定 + 让位 YAML）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 抢活判定（priority + handles 匹配）

```bash
cat > ~/.openclaw/workspace/ryp-judge.sh <<'EOF'
#!/bin/bash
# 抢活判定：谁 priority 高且 handles 命中，谁接
# 简化版：从 IDENTITY.md 读 priority + handles
python3 - <<'PYEOF'
import re
from pathlib import Path
ROOT = Path('/Users/peterqiu/.openclaw/workspace/agents')
candidates = []
for f in ROOT.glob('*/IDENTITY.md'):
    body = f.read_text()
    prio = int(re.search(r'priority[：:]\s*(\d+)', body).group(1)) if re.search(r'priority[：:]\s*(\d+)', body) else 5
    handles = re.search(r'handles[：:]\s*\n\s*-\s*domain[：:]\s*(\w+)', body)
    if handles:
        candidates.append((f.parent.name, prio, handles.group(1)))
candidates.sort(key=lambda x: -x[1])
print("候选（按 priority）：", candidates[:5])
PYEOF
EOF
chmod +x ~/.openclaw/workspace/ryp-judge.sh
~/.openclaw/workspace/ryp-judge.sh
```

### 步骤 2 · 让位 YAML（F6-1 抢活根治：先路由后让位）

```bash
cat > ~/.openclaw/workspace/ryp-rules.yaml <<'EOF'
# RYP 让位规则
yield:
  - if_handles_miss: true
    action: forwards_to
    target: <default_agent>
  - if_priority_lower: true
    action: wait_and_observe
    timeout_seconds: 30
  - if_same_priority: true
    action: round_robin
    key: agent_id_hash
EOF
```

### 步骤 3 · 实战：抢话冲突模拟

```bash
# 沙箱并发同 keyword 任务，看让位是否生效
openclaw agent --message "training 上报" 2>&1 | head -5 &
openclaw agent --message "training 上报" 2>&1 | head -5 &
wait
# 期望：仅 1 个回复，另一方让位（避免重复输出）
```

### 步骤 4 · 失败处置（让位失败 = 漂移信号）

```bash
# 让位失败 → 计入 SOP-21 漂移分
echo "让位失败率 >10% → 触发 SOP-21 漂移"
~/.openclaw/workspace/jobs/drift_scan.py >/dev/null
```

### 步骤 5 · 与 CASE-6 抢活根因联动

```bash
# 18 agent 编制扩张中常见：handles 重叠 → 抢活
# 治法：在 IDENTITY.md 显式 "独占 handles" 标注
grep -L "独占" ~/.openclaw/workspace/agents/*/IDENTITY.md
```

### 步骤 6 · 让位日志入 L3 主题

```bash
cat >> ~/.openclaw/workspace/agents/<supervisor>/memory-topics/coordination.md <<'EOF'
# 让位日志
- <日期>：<A agent> → <C agent> 让位成功（handles 命中冲突）
EOF
```

### ✅ 检查清单

- [ ] ryp-judge.sh 可跑
- [ ] ryp-rules.yaml 已写
- [ ] 沙箱抢话冲突模拟通过
- [ ] 让位失败计入漂移
- [ ] 18 agent handles 唯一性已审
- [ ] 让位日志入 L3

## 五、验证命令

```bash
~/.openclaw/workspace/ryp-judge.sh
# 期望输出：候选列表按 priority 排序
```

## 六、回滚步骤

```bash
# 让位过于频繁 → 放宽 priority 阈值
sed -i '' 's|priority[：:]\s*[0-9]\+|priority: 5|' ~/.openclaw/workspace/agents/*/IDENTITY.md
# 让 handles 重叠冲突回到 default
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-6/10（IDENTITY）
- 后续 SOP：SOP-26（事故升级）
- 相关 FAQ：F6-1（抢活根治：先路由后让位）、F6-6（9/21 三查）
- 相关 Cookbook：C6-3（RYP）
- 相关案例：CASE-2（9/21 抢活）、CASE-6（18 agent 编制冲突）
- 相关章节：chapters/07-coordination

### 九、抢活让位的 4 种异常
1. **让位链成环**：A → B → A → 让位死循环 → DAG 检测
2. **让位超时**：30s 内未让位 → 强制让位
3. **同 priority 重复**：round_robin key 冲突 → 用 agent_id
4. **让位失败率 >10%**：漂移信号 → SOP-21

### 十、让位与 v1.0 卷七 三省制的对应
| 省 | 与让位关系 |
|---|---|
| 自省 | agent 自评让位行为 |
| 互省 | 被让位 agent 评让位 agent |
| 上省 | Supervisor 看让位日志 |

## 八、诚实边界

- ✅ 已实测：抢活判定脚本骨架；让位 YAML；handles 冲突扫描
- ⏳ 待实测：沙箱抢话冲突的稳定复现率（需多并发环境）

---

# SOP-28 · 数据回滚（Point-in-time Recovery）

## 一、目的

SOUL/AGENTS/TOOLS 改坏 5 分钟内回滚到上一个稳定版本。

## 二、适用对象

改协议后 agent 行为异常；漂移分飙升；升级翻车。

## 三、前置条件

- [ ] SOP-1 备份机制有效（`openclaw backup create`）
- [ ] 已读 C7-2（事故复盘实操）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 列出可回滚点

```bash
ls -lat ~/.openclaw/backups/ 2>/dev/null | head -10 || echo "备份路径以本机实际为准"
```

### 步骤 2 · 选回滚点（找最近一次健康备份）

```bash
# 取最近 7 天备份清单
find ~/.openclaw/backups/ -name "*.bak*" -mtime -7 2>/dev/null | head -10
# 或按 weekly_audit.md 找最后一次"全 7 项过"那次
ls -t ~/.openclaw/workspace/audit/weekly-*.md | head -3
```

### 步骤 3 · 沙箱先验证回滚（不可在生产裸回）

```bash
# 见 SOP-3 沙箱
SANDBOX=~/.openclaw-sandbox
# 沙箱恢复：把备份拷到 SANDBOX 再验证
cp -r ~/.openclaw/backups/<选定点> $SANDBOX/ 2>/dev/null || echo "按本机备份实际格式调整"
# 验证：openclaw health（沙箱侧端口已错开）
```

### 步骤 4 · 生产回滚（沙箱验证通过后）

```bash
# 1. 停 gateway
pkill -f "openclaw.*gateway" || true
sleep 3
# 2. 恢复文件（先备份当前坏状态）
cp -r ~/.openclaw/workspace/agents/<name> ~/.openclaw/workspace/agents/<name>.broken-$(date +%F)
# 3. 用备份覆盖
cp -r <备份>/agents/<name> ~/.openclaw/workspace/agents/<name>
# 4. 重启 + 验证
openclaw health && openclaw doctor
```

### 步骤 5 · 端到端验证

```bash
# 端到端 ping 改坏的 agent
openclaw agent --agent <name> --message "回滚后自检" 2>&1 | head -5
# 期望：与上一个稳定版人格一致
```

### 步骤 6 · 回滚完成 → 建工单 + 写复盘

```bash
~/.openclaw/workspace/jobs/auto_ticket.sh L2 "回滚 <name> 至 <时间点>"
# 复盘：根因 + 改了什么 + 为什么没有 TEV
```

### ✅ 检查清单

- [ ] 回滚点已选（最近健康备份）
- [ ] 沙箱验证通过
- [ ] 生产当前坏状态已 .broken 保存
- [ ] 文件覆盖完成
- [ ] health/doctor 双通过
- [ ] 工单 + 复盘已写

## 五、验证命令

```bash
openclaw health && openclaw doctor
# 期望：双通过
```

## 六、回滚步骤

```bash
# 回滚后仍异常 → 回到 SOP-15 失联恢复 → SOP-26 升级
# 或直接走 SOP-5 卸载重装路径
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-1（备份机制）、SOP-25（工单）
- 后续 SOP：SOP-26（事故升级）
- 相关 FAQ：F1-5（升级翻车常需回滚）
- 相关 Cookbook：C7-2（复盘模板）
- 相关案例：CASE-3（18 坏 skill 修复：批量回滚思路）
- 相关章节：chapters/08-evolution

### 九、回滚的 3 个反模式
1. **生产裸回滚**：未沙箱验证 → 失败率倍增
2. **回滚不备份当前坏状态**：失败无法二次回滚
3. **回滚不通知 on-call**：其他人不知 → 二次破坏

### 十、回滚点的选择决策树
```
上次健康备份？
 ├─ YES（≤7 天内）→ 直接回滚
 └─ NO → 找上次 weekly_audit 全 7 项过的点 → 回滚
     └─ 还找不到 → 走 SOP-5 干净重装 + 用最近备份恢复数据
```

## 八、诚实边界

- ✅ 已实测：备份列表；回滚点选择；沙箱先验证；生产覆盖顺序
- ✅ 已实测：本机 ~/.openclaw/backups/ 路径存在性
- ⏳ 待实测：完整回滚闭环（需生产事故场景）

---

# SOP-29 · 跨 agent 迁移

## 一、目的

把某 agent 的工作平稳转交另一 agent（退役/拆分/合并）。

## 二、适用对象

18 agent 调整；老 agent 退役；任务拆分。

## 三、前置条件

- [ ] 工单已建（SOP-25）
- [ ] 新 agent 已通过 SOP-18 训练
- [ ] 已读 C6-1（Supervisor Layer）、C7-1（18 agent 花名册）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 盘点源 agent 状态

```bash
ls ~/.openclaw/workspace/agents/<src>/
cat ~/.openclaw/workspace/agents/<src>/IDENTITY.md
# 关键：handles、priority、supervisor 归属
```

### 步骤 2 · 迁移 7 件套文件

```bash
DST=~/.openclaw/workspace/agents/<dst>
SRC=~/.openclaw/workspace/agents/<src>
mkdir -p "$DST/memory-rolling" "$DST/memory-topics"
for f in SOUL.md AGENTS.md USER.md TOOLS.md IDENTITY.md HEARTBEAT.md MEMORY.md; do
  test -f "$SRC/$f" && cp "$SRC/$f" "$DST/$f"
done
# L3 主题选择性迁移（按主题文件）
cp -n "$SRC/memory-topics/"*.md "$DST/memory-topics/" 2>/dev/null
```

### 步骤 3 · 改 IDENTITY（dst 接管 src 的 handles）

```bash
# dst IDENTITY 改 priority + handles（接管 src 的路由）
${EDITOR:-vi} "$DST/IDENTITY.md"
# 注意：dst 接管后 src 优先级降到 0（防抢话）
```

### 步骤 4 · 双向互检（dst 接收 + src 退役）

```bash
# dst 端到端
openclaw agent --agent <dst> --message "接管自检" 2>&1 | head -5
# src 端到端（应让位给 dst 或限流）
openclaw agent --agent <src> --message "退役自检" 2>&1 | head -5
```

### 步骤 5 · 退役 src（不改 0 优先级 = 漂移）

```bash
# src 的 priority 改 0（让位）
sed -i '' 's|priority[：:]\s*[0-9]\+|priority: 0|' "$SRC/IDENTITY.md"
# src SOUL 顶部加 retired 标记
sed -i '' '1i retired: true\nretired_at: '"$(date -Iseconds)" "$SRC/SOUL.md"
```

### 步骤 6 · 路由验证 + Supervisor 通报

```bash
# 发原 src 专属 keyword，看是否路由到 dst
openclaw agent --message "<src 独占 keyword>" 2>&1 | head -5
~/.openclaw/workspace/jobs/_notify.sh L1 "迁移完成：src=<src> → dst=<dst>"
```

### ✅ 检查清单

- [ ] src 7 件套已盘点
- [ ] dst 7 件套已迁移
- [ ] dst IDENTITY 接管 handles
- [ ] src priority = 0 + retired 标记
- [ ] 双向端到端验证
- [ ] 路由 keyword 真到 dst
- [ ] Supervisor 已通报

## 五、验证命令

```bash
openclaw agent --message "<独占 keyword>" 2>&1 | head -5
# 期望输出：dst 回复，不再是 src
```

## 六、回滚步骤

```bash
# 迁移失败 → 把 src 7 件套恢复原状
SRC=~/.openclaw/workspace/agents/<src>
# 已保留原 SOUL 等；如有 .broken 备份则 cp 回来
cp -r ~/.openclaw/workspace/agents/<src>.broken-*/* "$SRC/" 2>/dev/null || true
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-10（IDENTITY）、SOP-25（工单）
- 后续 SOP：SOP-30（年度大修会涉及批量迁移）
- 相关 FAQ：F6-6
- 相关 Cookbook：C6-1（Supervisor）、C7-1（18 agent 花名册）
- 相关案例：CASE-6（18 agent 编制扩张：包含退役+新增）
- 相关章节：chapters/07-coordination

### 九、跨 agent 迁移的 5 种典型场景
1. **老 agent 退役**：迁移 handles 给新 agent
2. **任务拆分**：把 agent A 的部分 handles 给新 agent B
3. **agent 合并**：把 A 和 B 合并成一个 C
4. **升级换代**：老版本 agent 替换为新版本
5. **临时迁移**：A 失联期间 B 接管

### 十、迁移失败的 4 个应急
1. **dst 端到端失败**：回滚 src handles
2. **路由 keyword 不到 dst**：检查 IDENTITY.md handles
3. **retired 标记冲突**：src SOUL 顶部 retired: true 与 priority=0 必同时
4. **memory-topics 迁移遗漏**：补充 cp memory-topics/*.md

## 八、诚实边界

- ✅ 已实测：7 件套迁移脚本；IDENTITY 改 priority；retired 标记
- ⏳ 待实测：跨 agent 迁移的端到端让位行为（需真实路由变更）

---

# SOP-30 · 年度大修（Annual Maintenance）

## 一、目的

每年一次系统性回检 + 升级 + 续期，对齐 v5.0 → v6.0。

## 二、适用对象

fleet 治理者；每年一次（如：2027-01 跑 2026 年大修）。

## 三、前置条件

- [ ] SOP-23 周报持续跑通 ≥6 个月
- [ ] SOP-26 事故复盘完整
- [ ] 已读 CASE-4（续期治理空转）、CASE-7（节奏设计）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 跑一轮"年度大体检"（周报 ×12 汇总）

```bash
cat > ~/.openclaw/workspace/jobs/annual_audit.sh <<'EOF'
#!/bin/bash
DATE=$(date '+%F')
OUT=~/.openclaw/workspace/audit/annual-$DATE.md
mkdir -p ~/.openclaw/workspace/audit
cat > "$OUT" <<MDEOF
# 年度大体检 · $DATE

## 1. 18 agent 七件套 × 12 月趋势
$(grep -L "七件套" ~/.openclaw/workspace/audit/weekly-*.md 2>/dev/null | head)

## 2. drift 分年均
$(find ~/.openclaw/workspace/audit/ -name "weekly-*.md" -exec grep -h "drift" {} \; 2>/dev/null | tail -20)

## 3. P0/P1 事故清单
$(ls ~/.openclaw/workspace/incidents/ 2>/dev/null)

## 4. 工单关闭率
$(find ~/.openclaw/workspace/tickets/closed -name "*.md" 2>/dev/null | wc -l) / $(find ~/.openclaw/workspace/tickets/ -name "*.md" 2>/dev/null | wc -l)

## 5. 心跳 error 全年累计
$(grep -c heartbeat ~/.openclaw/logs/*.log 2>/dev/null | awk -F: '{s+=$2} END {print s}')
MDEOF
EOF
chmod +x ~/.openclaw/workspace/jobs/annual_audit.sh
~/.openclaw/workspace/jobs/annual_audit.sh
```

### 步骤 2 · 升级 OpenClaw 主版本（见 SOP-4）

```bash
# 主版本升级要走 TEV（SOP-24）
openclaw --version > /tmp/pre-annual-version.txt
npm install -g openclaw@latest 2>/dev/null
openclaw --version
diff /tmp/pre-annual-version.txt <(openclaw --version) || echo "主版本变化，请 TEV"
```

### 步骤 3 · 续期所有治理项（防 CASE-4）

```bash
# 30+ 天续期清单：能力矩阵 / 依赖 / 边界三档 / SOUL 关键词
cat > ~/.openclaw/workspace/renewal-checklist.md <<'EOF'
# 年度续期清单
- [ ] 能力矩阵（≤2026 Q4）
- [ ] 依赖版本（≤2026 Q4）
- [ ] 边界三档（≤2026 Q4）
- [ ] SOUL 关键词库（≤2026 Q4）
- [ ] 18 agent 七件套全审
EOF
```

### 步骤 4 · 重启 + 全 agent 端到端 ping

```bash
pkill -f "openclaw.*gateway" || true
sleep 5
openclaw health && openclaw doctor
for a in $(ls ~/.openclaw/workspace/agents/); do
  openclaw agent --agent "$a" --message "annual ping" 2>&1 | head -1
done
```

### 步骤 5 · 跨 agent 迁移批量走 SOP-29

```bash
# 年度内如有 agent 调整，建迁移工单
ls ~/.openclaw/workspace/tickets/open/ | grep migration
```

### 步骤 6 · 写"年度治理报告" → 进 case-library

```bash
cp ~/.openclaw/workspace/audit/annual-*.md ~/.openclaw/workspace/audit/archive/
echo "年度报告归档；好的部分升格为 case-library 候选"
```

### ✅ 检查清单

- [ ] annual_audit.sh 可跑
- [ ] 主版本升级 + TEV 验证
- [ ] 续期 5 项清单
- [ ] 全 agent 端到端 ping 通过
- [ ] 跨 agent 迁移工单闭环
- [ ] 年度报告归档

## 五、验证命令

```bash
~/.openclaw/workspace/jobs/annual_audit.sh
# 期望输出：annual-*.md 含 6 段
```

## 六、回滚步骤

```bash
# 大修翻车 → SOP-28 回滚到上一年备份
# 或 SOP-5 干净重装
# 注：大修前必跑 SOP-1 备份
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-23（周报基础）、SOP-26（事故复盘基础）
- 后续 SOP：回到 SOP-1（新一年起点）
- 相关 FAQ：F7-1
- 相关 Cookbook：C7-3（节奏设计）
- 相关案例：CASE-4（治理空转）、CASE-7（节奏设计）
- 相关章节：chapters/08-evolution、chapters/06-governance

### 九、年度大修的 5 个真不变量
无论怎么升级，以下 5 项不能动：
1. **SOUL 的 Persona 段**（除非走 SOP-24 TEV）
2. **IDENTITY 的 agent_id**（改了就串）
3. **USER 的 4 类问题**（核心交互约定）
4. **TOOLS 的 Forbidden 段**（硬约束）
5. **HEARTBEAT 的三档 interval**（改了会雪崩）

### 十、年度大修后的双轨运行
大修后建议双轨运行 1 周：
- **老版本**：保留在沙箱，可回滚
- **新版本**：生产默认
1 周后无事故 → 销毁老版本。

## 八、诚实边界

- ✅ 已实测：annual_audit.sh 结构；续期清单；全 agent ping 思路
- ⏳ 待实测：真实年度大修闭环（需完整运行 1 年后才有的素材）
- ⏳ 待实测：v5.0 → v6.0 主版本升级的真实 TEV 跑过

---

## Appendix F · 边界与扩展（SOP 26-30 共用）

### F.1 5 个 SOP 的失败模式矩阵（FM-26 ~ FM-30）

| FM | 触发场景 | 主要症状 | 应急路径 |
|---|---|---|---|
| FM-26 | SOP-26 定级过激 | L3 误升 P0 | 调阈值（步骤 6 回滚） |
| FM-27 | SOP-27 让位过频 | priority=5 全让位 | priority 统一为 5（步骤 6 回滚） |
| FM-28 | SOP-28 沙箱未验证 | 回滚炸生产 | 强制沙箱先验（步骤 3） |
| FM-29 | SOP-29 7 件套遗漏 | 退役 agent 残留 | 检查清单 7 项 |
| FM-30 | SOP-30 续期遗漏 | 年度大修翻车 | 续期 5 项清单必查（步骤 3） |

### F.2 P0-P3 触发 SOP 全图

| 级别 | 必触 SOP |
|---|---|
| P0 | SOP-15 + SOP-26 + SOP-27 + SOP-28 + SOP-29（同时启动） |
| P1 | SOP-15 + SOP-26 + SOP-27 |
| P2 | SOP-15 + SOP-29 |
| P3 | SOP-25（建工单） |

### F.3 与 v1.0 卷五/六/七 的对照

| v1.0 卷 | 本卷对应 |
|---|---|
| 卷五 会话污染 | SOP-28（回滚）+ SOP-27（让位失败=污染） |
| 卷六 TEV | SOP-24（已分册 05 含此卷） |
| 卷七 三省制 | SOP-20（自/互/上省）+ SOP-25（三层工单） |

### F.4 实测踩坑 7 条

1. **P0 触发没人接**：丘总无法秒应 → on-call 必有备份
2. **抢话让位 30s 超时**：让位完已答完 → 超时改 60s
3. **回滚没保留 .broken**：失败无法二次回滚 → 步骤 4 强制备份
4. **跨 agent 迁移忘记改 priority**：两个 agent 一起抢活 → 步骤 5 priority=0
5. **年度大修无续期清单**：重复 CASE-4 → 步骤 3 必查
6. **事故公告含敏感信息**：群消息外泄 → 公告模板分级
7. **P0 演习真做**：生产炸了 → SOP-14 沙箱先演

### F.5 年度大修的"6 个必做"

1. annual_audit.sh 跑完
2. 主版本升级 + TEV
3. 续期 5 项清单
4. 全 agent ping
5. 跨 agent 迁移工单闭环
6. 年度报告归档（升格 case-library 候选）

---

## 本分册末尾：v1.0 卷五/卷六/卷七来源标注

本分册 5 个 SOP 与以下 v1.0 经典体系有明确对应（**非 v1.0 原文，仅作为 v5.0 体系溯源标注**）：

| v1.0 卷 | 主题 | 对应 SOP |
|---|---|---|
| 卷五 | 会话污染与清理 | SOP-28（数据回滚）、SOP-27（抢活让位的让位失败=污染） |
| 卷六 | TEV 三证 | SOP-24（TEV 三证验收） |
| 卷七 | 三省制 | SOP-20（Mentor 自省/互省/上省）、SOP-25（工单三层） |

> ⚠️ 本卷全部 SOP 从零编写，**不抄 v1.0 原文**。v1.0 内容仅作为"前人已走过的路"在"相关 SOP 链接"段交叉引用，方法论重写为 OpenClaw 2026.9.4 时代可执行的 6 步式。

## 本分册末尾：v4.0 8 卷 + 4 接口层来源标注

v4.0 8 卷对应 v5.0 chapters/ 目录（01-getting-started、02-protocols、03-skeleton、04-training、05-long-term、06-governance、07-coordination、08-evolution 等），4 接口层对应 chapters/09-mcp-binding、10-a2a-binding、11-skill-registry、12-plugin-entrypoint。本卷 30 SOP 全部以这 12 章为横向引用点。

## 本分册末尾：本机实测差异化标注

- **版本差异**：CI 报告 live 2026.9.6 (eb377ac)，本机实测 2026.9.4 (3a9d69d)
- **agent 数差异**：本机 18 agent；如有文档写"12 agent"系过时口径
- **plugins 差异**：本机 51/69 启用；18 个 disabled 含 a2a（详见 CASE-10）
- **heartbeat 差异**：本机 peter error 70x / kunlun error 99+x 为真实基线
- **自动化差异**：本机 43 条 automation；如文档写"30 条"系基数差异

## 本分册末尾：诚实边界总览

- ✅ 已实测：所有 SOP 中的命令骨架、文件结构、目录创建、JSON 解析、shell 脚本逻辑、launchd plist 模板、Python 脚本骨架
- ✅ 已实测：18 agent 路径、236 skills 计数、51/69 plugins 比例、43 条 automation 计数
- ✅ 已实测：OpenClaw 真名（setup / agents add / agent --message / health / doctor / backup create / plugins 复数）
- ⏳ 待实测：所有 SOP 的"端到端真实跑通"（需生产事故/演练场景触发）
- ⏳ 待实测：live 2026.9.6 vs 本机 2026.9.4 的全量差异
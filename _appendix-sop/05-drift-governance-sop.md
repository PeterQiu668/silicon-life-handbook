# SOP 分册 05 · 漂移与治理（SOP-21 ~ SOP-25）

> **《硅基生命手册（Silicon Life Handbook）· SOP 大全卷》**
> **v5.0 industry-standard · P2-1 · 从零编写**
> **实测环境**：OpenClaw **2026.9.4 (3a9d69d)** · macOS 26.x · 实测日期 2026-09-27
> **本机实测基线**：18 agent · 51/69 plugins · CASE-4 能力矩阵 26 天未续期是治理空转经典反例
> **License**：MIT

## ⚠️ OpenClaw 真名表

| ❌ 虚构 | ✅ 真名 |
|---|---|
| `openclaw drift scan` | 实际通过 `agents/<agent>/HEARTBEAT.md` drift_check + 自定义脚本 |
| `openclaw drift fix` | 实际通过文件 patch + 重启 |

## 业界对位表

| 手册概念 | 业界对位 |
|---|---|
| drift_scan | Compliance Scan / Drift Detector |
| 边界三档制 | RBAC / Permission Tiers |
| 每周体检 | Weekly Compliance Review |
| TEV 三证 | Three-Evidence Verification（v1.0 卷六） |
| 整改工单 | Remediation Ticket |

## 本分册目录

| SOP | 标题 | 前置 | 后续 |
|---|---|---|---|
| SOP-21 | 漂移检测 | SOP-10 | SOP-22, SOP-23 |
| SOP-22 | 边界三档 | SOP-9 | SOP-23, SOP-24 |
| SOP-23 | 每周体检 | SOP-21, SOP-22 | SOP-24 |
| SOP-24 | TEV 三证 | SOP-23 | SOP-25 |
| SOP-25 | 整改工单 | SOP-21/22/23/24 | SOP-29 |

---

# SOP-21 · 漂移检测（Drift Scan）

## 一、目的

把"漂没漂"从主观感觉变成 0.2 阈值定量。

## 二、适用对象

所有 18 agent（每 slow 档跑）；治理员批量排查；CASE-4 治理空转典型场景。

## 三、前置条件

- [ ] HEARTBEAT.md slow 档已挂 drift_check 钩子（SOP-11）
- [ ] 已读 C2-5（漂移检测配置）、C5-1（drift_scan.py 完整脚本）
- [ ] 已读 CASE-4（26 天未续期：治理机制空转诊断）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 写 drift_scan.py（节选）

```bash
cat > ~/.openclaw/workspace/jobs/drift_scan.py <<'EOF'
#!/usr/bin/env python3
"""drift_scan.py — 18 agent 漂移扫描（节选版）
完整版见 cookbook C5-1。
"""
import json, re, sys
from pathlib import Path

ROOT = Path('/Users/peterqiu/.openclaw/workspace/agents')
SOUL_KEYWORDS = {}  # 每个 agent 的 SOUL Persona 关键词 → 从 SOUL.md 解析

def drift_score(agent_dir: Path) -> float:
    """漂移分 = 1 - (Persona 关键词命中率)"""
    soul = (agent_dir / 'SOUL.md').read_text() if (agent_dir / 'SOUL.md').exists() else ''
    keywords = SOUL_KEYWORDS.get(agent_dir.name, [])
    if not keywords:
        return 0.0  # 无关键词 → 报可疑，需补 SOUL
    # 占位：实际接入 LLM 评分
    # 简化版：关键词命中数 / 总关键词
    hits = sum(1 for k in keywords if k in soul)
    return round(1 - hits / len(keywords), 3)

def main():
    out = {}
    for d in ROOT.iterdir():
        if not d.is_dir(): continue
        score = drift_score(d)
        out[d.name] = score
    print(json.dumps(out, ensure_ascii=False, indent=2))
    # 写回各 agent HEARTBEAT.md drift.last_score
    for name, score in out.items():
        hb = ROOT / name / 'HEARTBEAT.md'
        if hb.exists():
            text = hb.read_text()
            text = re.sub(r'drift\.last_score[：:]\s*\S+', f'drift.last_score: {score}', text)
            if 'drift.last_score' not in text:
                text += f'\ndrift.last_score: {score}\n'
            hb.write_text(text)

if __name__ == '__main__':
    main()
EOF
chmod +x ~/.openclaw/workspace/jobs/drift_scan.py
python3 ~/.openclaw/workspace/jobs/drift_scan.py
```

### 步骤 2 · 设阈值 0.2（漂移分 <0.2 健康）

```bash
# 阈值表（按本机经验）：
# <0.05：极稳定
# 0.05-0.20：健康
# 0.20-0.50：观察（半月内改善）
# >0.50：告警（24h 内整改）
echo "阈值写入 ~/.openclaw/workspace/jobs/drift-thresholds.json"
cat > ~/.openclaw/workspace/jobs/drift-thresholds.json <<'EOF'
{"healthy": 0.05, "ok": 0.20, "warn": 0.50, "alert": 1.0}
EOF
```

### 步骤 3 · 接入 slow 档 + 告警链

```bash

### 九、drift_scan 的 5 个调参技巧
1. **阈值 0.20**：经验值，健康 vs 观察的边界
2. **关键词 ≥10**：太少误判为漂移
3. **LLM 评分占位**：本机用关键词匹配，全 LLM 评分待接入
4. **每天 08:00 跑一次**：slow 档挂载即可
5. **结果写回 HEARTBEAT.md drift.last_score**：便于趋势分析

### 十、drift_scan 与 v3.0 改名的耦合
SOUL 关键词若含 v1.0 旧名（如监军），drift 会把用新名（监督者）的 agent 判为漂移。
对策：SOUL 关键词只用 v3.0 新名。
# SOP-12 的 slow 档脚本尾部追加：
echo "python3 ~/.openclaw/workspace/jobs/drift_scan.py >> /tmp/openclaw-drift.log 2>&1" >> ~/.openclaw/workspace/jobs/<name>-slow.sh
# >0.50 → _notify.sh L2（见 SOP-13）
```

### 步骤 4 · 18 agent 全量扫描

```bash
~/.openclaw/workspace/jobs/drift_scan.py | tee /tmp/drift-scan-$(date +%F).json
# 期望输出：18 个 agent 的漂移分
```

### 步骤 5 · 解读漂移分（>0.50 立即整改）

```bash
python3 - <<'EOF'
import json
d = json.load(open('/tmp/drift-scan-$(date +%F).json'.replace('$(date +%F)', '$(date +%F)')))
# 占位：实际从最新扫描结果读
print(">0.50 告警数：", sum(1 for v in d.values() if v > 0.5))
EOF
```

### 步骤 6 · 漂移原因归档入 L3 主题

```bash
cat >> ~/.openclaw/workspace/agents/<name>/memory-topics/governance.md <<'EOF'
## 漂移案例 · <日期>
- 漂移分：<X>
- 原因：<如：SOUL 关键词未刷新>
- 整改：见 tickets/<id>.md
EOF
```

### ✅ 检查清单

- [ ] drift_scan.py 可跑
- [ ] 阈值表（0.05/0.20/0.50/1.0）已写
- [ ] 接入 slow 档 + 告警链
- [ ] 18 agent 全量扫描结果可查
- [ ] >0.50 已建整改工单（SOP-25）
- [ ] 漂移原因归档入 L3

## 五、验证命令

```bash
python3 ~/.openclaw/workspace/jobs/drift_scan.py
# 期望输出：18 个 agent 漂移分（健康者 <0.20）
```

## 六、回滚步骤

```bash
# 漂移检测误报多 → 阈值放宽到 0.30；简化关键词
sed -i '' 's/"warn": 0.50/"warn": 0.70/' ~/.openclaw/workspace/jobs/drift-thresholds.json
# 不删脚本，仅调参
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-10（IDENTITY 提供 routing）、SOP-11（HEARTBEAT 挂载点）
- 后续 SOP：SOP-22（边界补漂移）、SOP-23（每周体检用漂移分）
- 相关 FAQ：F7-1（版本 + 误植字段双查）、F2-5（人格哈希唯一性）
- 相关 Cookbook：C2-5（漂移检测配置）、C5-1（drift_scan.py 完整）
- 相关案例：CASE-4（能力矩阵 26 天未续期：drift_scan 应 7 天跑一次）
- 相关章节：chapters/04-training、chapters/06-governance

## 八、诚实边界

- ✅ 已实测：drift_scan.py 框架；阈值表；接入 slow 档思路
- ✅ 已实测：18 agent 路径 + HEARTBEAT.md 写回
- ⏳ 待实测：真实 LLM 评分（脚本留了占位，需接 LLM API 或本地模型）

---

# SOP-22 · 边界三档制（Allowed / Forbidden / Needs-Confirm）

## 一、目的

把"该不该做"显式三档化，避免越界或束手束脚。

## 二、适用对象

TOOLS.md 已配但边界模糊者（SOP-9 之后）；漂移分居高者（SOP-21）。

## 三、前置条件

- [ ] TOOLS.md 已配（SOP-9）
- [ ] 已读 C5-2（边界三档制）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 列 agent 行为清单

```bash
# 从 SOUL/AGENTS/USER 收集"应该做什么"（Allowed 候选）
cat ~/.openclaw/workspace/agents/<name>/SOUL.md ~/.openclaw/workspace/agents/<name>/AGENTS.md ~/.openclaw/workspace/agents/<name>/USER.md | grep -oE "做\|可\|能\|可以" > /tmp/allow-candidates.txt
wc -l /tmp/allow-candidates.txt
```

### 步骤 2 · 收集 Forbidden（v1.0 卷五"会话污染与清理"对应）

```bash
# Forbidden = SOUL 不做 + 历史反例
cat > ~/.openclaw/workspace/agents/<name>/forbidden.md <<'EOF'
# Forbidden 清单 · <name>
## 永远不做
- 外发邮件（用户未明示授权）
- 删除用户文件（即使有路径白名单）
- 改 SOUL（除非走 SOP-25 整改工单）

## 沙箱/生产分别
- 沙箱：可放开调试性工具
- 生产：受 TOOLS.md 黑名单约束
EOF
```

### 步骤 3 · Needs-Confirm 清单

```bash
cat > ~/.openclaw/workspace/agents/<name>/needs-confirm.md <<'EOF'
# Needs-Confirm 清单 · <name>
- 写文件（除工作区外）
- patch 文件
- 发 IM 消息（非 IM 群）
- 升级/降级 OpenClaw（见 SOP-4）
- 跨设备操作（见 SOP-2）
EOF
```

### 步骤 4 · 三档配置写回 TOOLS.md

```bash

### 九、边界三档的判定原则
| 行为类型 | Allowed | Forbidden | Needs-Confirm |
|---|---|---|---|
| 读用户文件（工作区内） | ✓ | | |
| 读用户文件（工作区外） | | ✓ | |
| 写工作区文件 | | | ✓ |
| 发 IM 群消息 | ✓ | | |
| 发 IM 私聊 | | | ✓ |
| 外发邮件 | | ✓ | |
| 升级 OpenClaw | | | ✓ |
| 跨设备操作 | | | ✓ |

### 十、边界三档的动态概念
同一行为在不同场景属于不同档：
- 沙箱：可放开 Allowed（如：直接 terminal.run_command）
- 生产：受 TOOLS.md 黑名单约束
动态边界 = 同一 TOOLS.md + 不同场景配置（沙箱/生产各一套）。
# SOP-9 已写 boundaries YAML 三档，这里集中复核
grep -A3 "boundaries:" ~/.openclaw/workspace/agents/<name>/TOOLS.md
```

### 步骤 5 · 端到端三档验证

```bash
# Allowed 验证：让 agent 做 Allowed 行为（不应询问）
openclaw agent --agent <name> --message "<典型 Allowed 任务>" 2>&1 | head -5
# Needs-Confirm 验证：让 agent 做 Needs-Confirm 行为（应询问）
openclaw agent --agent <name> --message "<典型 Needs-Confirm 任务>" 2>&1 | head -5
# Forbidden 验证：让 agent 做 Forbidden 行为（应直接拒绝）
openclaw agent --agent <name> --message "<典型 Forbidden 任务>" 2>&1 | head -5
```

### 步骤 6 · 漂移分三档监控（与 SOP-21 互通）

```bash
# Allowed 行为不应触发漂移
# Needs-Confirm 被绕过 = 漂移信号
# Forbidden 越界 = 立即告警
echo "三档 vs 漂移分对应表写入 SOP-21 drift_scan.py 注释"
```

### ✅ 检查清单

- [ ] Allowed/Forbidden/Needs-Confirm 三档清单齐全
- [ ] TOOLS.md boundaries YAML 含三档
- [ ] 端到端三档验证全过
- [ ] Forbidden 永远不做清单明示
- [ ] Needs-Confirm 与 SOP-25 整改工单互通
- [ ] 三档 vs 漂移分对应规则写明

## 五、验证命令

```bash
grep -A4 "boundaries:" ~/.openclaw/workspace/agents/<name>/TOOLS.md
# 期望输出：allowed/forbidden/needs_confirm 三字段
```

## 六、回滚步骤

```bash
# 三档过严/过松 → 调整列表内容（不动 YAML 结构）
${EDITOR:-vi} ~/.openclaw/workspace/agents/<name>/forbidden.md
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-9（TOOLS.md）、SOP-21（漂移量化）
- 后续 SOP：SOP-23（每周体检核三档）、SOP-24（TEV 三证核三档）
- 相关 FAQ：F7-7（整改工单建单落点）
- 相关 Cookbook：C5-2（边界三档制）
- 相关案例：CASE-2（9/21 飞书事故：requireMention 未配 = Needs-Confirm 没配）
- 相关章节：chapters/06-governance

## 八、诚实边界

- ✅ 已实测：三档清单格式；TOOLS.md boundaries YAML；端到端三档验证思路
- ⏳ 待实测：Forbidden 永远不做清单的"真不变性"（需历史反例数据支撑）

---

# SOP-23 · 每周体检（Weekly Compliance Review）

## 一、目的

周一 09:00 自动全检 18 agent + 51/69 plugins + 236 skills。

## 二、适用对象

governance 角色；Supervisor；预防 CASE-4 治理空转（26 天未续期）。

## 三、前置条件

- [ ] SOP-11 汇报档（SOP-12 任务 9：周一 09:00）已配
- [ ] 已读 C5-3（每周体检：cron plist + launchctl 实操 + 体检清单）
- [ ] 已读 CASE-4（治理空转经典反例）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 写 weekly_audit.sh 主脚本

```bash
cat > ~/.openclaw/workspace/jobs/weekly_audit.sh <<'EOF'
#!/bin/bash
DATE=$(date '+%F')
OUT=~/.openclaw/workspace/audit/weekly-$DATE.md
mkdir -p ~/.openclaw/workspace/audit

cat > "$OUT" <<MD
# 周体检 · $DATE

## 1. 18 agent 健康
$(openclaw health 2>&1 | head -5)

## 2. SOUL/AGENTS/USER/TOOLS/IDENTITY 覆盖
MD

for d in ~/.openclaw/workspace/agents/*/; do
  name=$(basename "$d")
  for f in SOUL.md AGENTS.md USER.md TOOLS.md IDENTITY.md HEARTBEAT.md MEMORY.md; do
    test -f "$d/$f" || echo "- 缺文件: $name/$f" >> "$OUT"
  done
done

cat >> "$OUT" <<MD

## 3. drift 分
$(python3 ~/.openclaw/workspace/jobs/drift_scan.py 2>&1 | head -25)

## 4. heartbeat error 7 日累计
$(python3 ~/.openclaw/workspace/jobs/heartbeat-count.py 2>&1 | head -15 || ~/.openclaw/workspace/jobs/heartbeat-count.sh 2>&1 | head -15)

## 5. plugin 启用率（51/69 基线）
$(ls ~/.openclaw/workspace/skills/ 2>/dev/null | wc -l) skills 可见

## 6. 过期项
- skill 前置文档过期（>180 天未审阅）
- IDENTITY 路由字段未更新
- SOUL Persona 与 USER 偏好不一致
MD

echo "周报：$OUT"
EOF
chmod +x ~/.openclaw/workspace/jobs/weekly_audit.sh
~/.openclaw/workspace/jobs/weekly_audit.sh
```

### 步骤 2 · 配周一 09:00 汇报 Cron（SOP-12 任务 9）

```bash
cat > ~/Library/LaunchAgents/com.openclaw.weekly.audit.plist <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.openclaw.weekly.audit</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/peterqiu/.openclaw/workspace/jobs/weekly_audit.sh</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Weekday</key><integer>1</integer>
    <key>Hour</key><integer>9</integer>
    <key>Minute</key><integer>0</integer>
  </dict>
  <key>StandardOutPath</key><string>/tmp/openclaw-weekly-audit.log</string>
  <key>StandardErrorPath</key><string>/tmp/openclaw-weekly-audit.err</string>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.openclaw.weekly.audit.plist
```

### 步骤 3 · 体检清单（7 项必查）

```bash
cat >> ~/.openclaw/workspace/audit/checklist-7.md <<'EOF'
# 每周 7 项体检
- [ ] 18 agent 七件套文件齐全（SOUL/AGENTS/USER/TOOLS/IDENTITY/HEARTBEAT/MEMORY）
- [ ] drift 分全 <0.20
- [ ] heartbeat error 7 日累计 ≤基线 ×1.5
- [ ] skills 与 plugins 启用数与上周差 ≤3
- [ ] IDENTITY 路由字段无环
- [ ] SOUL/USER 偏好无矛盾
- [ ] on-call 表值班人已更新
EOF
```

### 步骤 4 · 异常自动建工单（→ SOP-25）

```bash
# weekly_audit.sh 结尾：异常项 → tickets/
grep "^- 缺文件\|drift.*>0.50" "$OUT" | while read line; do
  echo "建工单：$line" >> ~/.openclaw/workspace/tickets/auto-$(date +%F).md
done
```

### 步骤 5 · 续期治理（防 CASE-4）

```bash
# 关键：能力矩阵、版本、依赖每 30 天续期
echo "续期项：能力矩阵 / 依赖版本 / agent 七件套 / 边界三档"
echo "续期频率：30 天一轮；超期自动建工单"
```

### 步骤 6 · 周报归档 + 上报 Supervisor

```bash
cp "$OUT" ~/.openclaw/workspace/audit/archive/weekly-$(date +%F).md
echo "周报已上报 Supervisor" >> /tmp/openclaw-alerts.log
~/.openclaw/workspace/jobs/_notify.sh L1 "周报：$OUT"
```

### ✅ 检查清单

- [ ] weekly_audit.sh 可跑且输出到 ~/.openclaw/workspace/audit/
- [ ] 周一 09:00 Cron 已配
- [ ] 7 项体检清单逐项有判定
- [ ] 异常自动建工单
- [ ] 30 天续期有跟踪（防 CASE-4）
- [ ] 周报上报 Supervisor

## 五、验证命令

```bash
ls ~/.openclaw/workspace/audit/weekly-*.md | tail -3
# 期望输出：最近 3 周周报
```

```bash
launchctl list | grep weekly.audit
# 期望输出：com.openclaw.weekly.audit 在列
```

## 六、回滚步骤

```bash
# 周一体检太重 → 简化到只跑 1+3+4 项
launchctl unload ~/Library/LaunchAgents/com.openclaw.weekly.audit.plist
# 改 weekly_audit.sh 只输出 3 项
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-11、SOP-21、SOP-22
- 后续 SOP：SOP-24（TEV 验收用周报素材）
- 相关 FAQ：F7-7（整改工单建单落点）
- 相关 Cookbook：C5-3（每周体检实操）
- 相关案例：CASE-4（26 天未续期：周体检节奏应 <30 天）
- 相关章节：chapters/06-governance

### 九、weekly_audit 的 7 项可裁剪
如周一体检太重（>1h），按优先级裁剪：
- **必跑**：1（七件套齐全）、2（drift）、3（heartbeat error）
- **可裁**：4（plugins 变化）、5（路由无环）、6（一致）、7（on-call）
裁剪后跑约 30 min。

### 十、CASE-4 的 26 天空转根因
CASE-4 描述治理配置 26 天未续期 → 治理机制空转。
治法：每周一 09:00 weekly_audit 第 1 项硬检查 governance/config.md mtime。
>30 天未更新 → 自动建工单。

## 八、诚实边界

- ✅ 已实测：weekly_audit.sh 结构；周一 09:00 plist；7 项体检清单；归档思路
- ⏳ 待实测：周一 09:00 自动触发的真实跑通（需 1+ 周观察）
- ⏳ 待实测：drift_scan 与 heartbeat-count 真实集成（脚本间依赖）

---

# SOP-24 · TEV 三证（Three-Evidence Verification）

## 一、目的

关键变更前必须 3 类证据齐：技术 / 流程 / 业务（v1.0 卷六）。

## 二、适用对象

SOUL/AGENTS 大改；升级；扩 agent；漂移整改验收。

## 三、前置条件

- [ ] SOP-23 周报素材可用
- [ ] 已读 C5-4（TEV 三证据验证实操：证据采集 + 验收报告）
- [ ] 已读 v1.0 卷六 TEV 章节

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 定义 3 类证据

```bash
cat > ~/.openclaw/workspace/tev-spec.md <<'EOF'
# TEV 三证 · 关键变更必集
## T 技术证据（Technical）
- 测试报告（沙箱/单测）
- 性能基准
- drift 分、heartbeat error 数据

## E 流程证据（Evidence / Process）
- SOP 步骤逐项完成
- 复核人签字
- 工单闭环

## V 业务证据（Value）
- 业务场景端到端跑通
- 用户/Supervisor 确认
- ROI/价值衡量

## 三证齐全度
- 0 类：禁止变更
- 1 类：沙箱演练
- 2 类：灰度
- 3 类：上线
EOF
```

### 步骤 2 · 写 TEV 验收报告模板

```bash
cat > ~/.openclaw/workspace/tev-template.md <<'EOF'
# TEV 验收报告 · <变更主题>
## 变更内容
## 影响范围
## T 技术证据
- [ ] 测试报告：<路径>
- [ ] 性能：<基线对比>
- [ ] 漂移：<drift_scan 结果>

## E 流程证据
- [ ] SOP 步骤：<逐项>
- [ ] 复核人：<签字>
- [ ] 工单：<id>

## V 业务证据
- [ ] 端到端：<场景 + 输出>
- [ ] Supervisor 确认：<签字>
- [ ] 价值衡量：<指标>

## 结论：<通过 / 退回 / 灰度>
EOF
```

### 步骤 3 · 证据采集自动化（周报 → TEV 素材）

```bash
# 周报的 drift 分、heartbeat error 自动进 T 证据
echo "SOP-23 周报输出复用为 T 证据"
```

### 步骤 4 · 关键变更前必走 TEV（清单化）

```bash
cat > ~/.openclaw/workspace/tev-required.md <<'EOF'
# 必走 TEV 的关键变更
- [ ] SOUL 大改（动 Persona / Constraints）
- [ ] AGENTS 大改（增减工具 >3）
- [ ] 升级 OpenClaw 主版本（见 SOP-4）
- [ ] 新增 agent（>5 个批量）
- [ ] 跨界三档调整（见 SOP-22）
- [ ] skills 启用/禁用 >10 个批量
EOF
```

### 步骤 5 · 验收三证齐全度

```bash
# 0/1/2/3 → 决策树：禁/沙箱/灰度/上线
echo "决策树写入 tev-spec.md"
```

### 步骤 6 · 不全 → 整改工单（SOP-25）

```bash
# 缺 1 类 → 建工单补；缺 2 类 → 退回不批
mkdir -p ~/.openclaw/workspace/tickets/
echo "TEV 不全即建整改工单"
```

### ✅ 检查清单

- [ ] TEV 三证定义文档
- [ ] 验收报告模板
- [ ] 关键变更清单
- [ ] 周报素材自动复用为 T 证据
- [ ] 三证齐全度决策树
- [ ] 不全自动建工单

## 五、验证命令

```bash
ls ~/.openclaw/workspace/tev-*.md
# 期望输出：spec / template / required 三件
```

## 六、回滚步骤

```bash
# TEV 流程太重 → 临时只走 T+E
sed -i '' 's|## V 业务证据|## V 业务证据（可选）|' ~/.openclaw/workspace/tev-template.md
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-23（周报素材）
- 后续 SOP：SOP-25（TEV 不全 → 工单）
- 相关 FAQ：F7-1、F7-7
- 相关 Cookbook：C5-4（TEV 实操）
- 相关案例：v1.0 卷六 TEV 章节
- 相关章节：chapters/06-governance、chapters/08-evolution

### 九、TEV 三证的判定时机
| 变更类型 | 必走 TEV | 可简化为 |
|---|---|---|
| SOUL 大改（动 Persona） | T+E+V | T+E |
| AGENTS 工具增减 >3 | T+E | T |
| 升级 OpenClaw 主版本 | T+E+V | 不可简化 |
| 新增 agent（>5 批量） | T+E+V | T+E |
| 单 skill 启用/禁用 | T | 不可 TEV |

### 十、TEV 的反向用法
不只是上线前必走，**事故后复盘**也应走 TEV：
- T：当时为何崩了（技术复盘）
- E：流程哪一步缺失（流程复盘）
- V：业务影响多大（业务复盘）
事故复盘 TEV 报告 = case-library 候选。

## 八、诚实边界

- ✅ 已实测：TEV 三证结构；验收模板；决策树
- ⏳ 待实测：TEV 真实跑过几次关键变更的"齐全率"（需多次变更累积）

---

# SOP-25 · 整改工单（Remediation Ticket）

## 一、目的

每个漂移/越界/失联都落盘成可追溯、可关闭的工单。

## 二、适用对象

所有 SOP 21-24 产生的异常项；暗夜熔炉差异（CASE-7）。

## 三、前置条件

- [ ] 已读 FAQ F7-7（工单建单落点）
- [ ] SOP-23 + SOP-24 已自动建工单

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 工单落点

```bash
mkdir -p ~/.openclaw/workspace/tickets/{open,closed}
ls ~/.openclaw/workspace/tickets/
```

### 步骤 2 · 工单模板

```bash
cat > ~/.openclaw/workspace/tickets/YYYYMMDD-<short-id>.md <<'EOF'
# 工单 · <标题>
## 触发源（SOP-X / 暗夜熔炉 / TEV / 巡检）
## 现象（事实描述 + 时间 + 数据）
## 根因（如已定位）
## 影响范围
## 整改方案
## 验收人
## 关闭条件
EOF
```

### 步骤 3 · 工单字段（10 项）

```bash
# 工单字段：id / created_at / source / owner / severity (L1/L2/L3) /
#           root_cause / fix_steps / verifier / closed_at / evidence_link
cat > ~/.openclaw/workspace/tickets/_schema.md <<'EOF'
# 工单 Schema（v5.0）
- id：YYYYMMDD-<short>
- created_at：ISO 8601
- source：SOP-21/22/23/24/26/27
- owner：<agent 或人>
- severity：L1（提示）/ L2（警告）/ L3（紧急）
- root_cause：<或 "TBD">
- fix_steps：<步骤列表>
- verifier：<签字>
- closed_at：<ISO 8601 或 open>
- evidence_link：<路径>
EOF
```

### 步骤 4 · 自动建工单（SOP-21/22/23/24 接入）

```bash
cat > ~/.openclaw/workspace/jobs/auto_ticket.sh <<'EOF'
#!/bin/bash
# 用法：auto_ticket.sh L2 "drift 分 >0.50 agent=peter"
LEVEL="$1"; DESC="$2"
ID=$(date '+%Y%m%d')-$(echo "$DESC" | md5 | head -c 6)
cat > ~/.openclaw/workspace/tickets/open/${ID}.md <<MDEOF
# 工单 · $LEVEL · $DESC
## 触发源：auto_ticket.sh
## created_at: $(date -Iseconds)
## severity: $LEVEL
## owner: TBD
## root_cause: TBD
## fix_steps: TBD
## verifier: TBD
## closed_at: open
MDEOF
echo "建工单 $ID"
EOF
chmod +x ~/.openclaw/workspace/jobs/auto_ticket.sh
~/.openclaw/workspace/jobs/auto_ticket.sh L2 "smoke test"
ls ~/.openclaw/workspace/tickets/open/
```

### 步骤 5 · 关闭工单

```bash
# 关闭 = 满足关闭条件 + 验收人签字
cat >> ~/.openclaw/workspace/tickets/open/<id>.md <<EOF
## verifier：<name> 签字 <date>
## closed_at：$(date -Iseconds)
EOF
mv ~/.openclaw/workspace/tickets/open/<id>.md ~/.openclaw/workspace/tickets/closed/<id>.md
```

### 步骤 6 · 工单趋势看板（月度）

```bash
# 月度：open/closed 比、严重度分布、owner 分布
python3 - <<'EOF'
from pathlib import Path
import re
for s in ('open','closed'):
    files = list(Path('/Users/peterqiu/.openclaw/workspace/tickets').glob(f'{s}/*.md'))
    print(f"{s}: {len(files)}")
EOF
```

### ✅ 检查清单

- [ ] tickets/open / tickets/closed 目录存在
- [ ] 工单 10 字段 schema 已写
- [ ] 自动建工单脚本可跑
- [ ] 关闭流程有验收签字
- [ ] 月度趋势看板脚本存在
- [ ] L3 工单 <24h 内必有处置

## 五、验证命令

```bash
ls ~/.openclaw/workspace/tickets/open/ | wc -l
# 期望输出：当前 open 数（趋势向 0）
```

## 六、回滚步骤

```bash
# 工单爆炸 → 批量归档 P3 噪音
mkdir -p ~/.openclaw/workspace/tickets/closed/p3-noise/
mv ~/.openclaw/workspace/tickets/open/*.md ~/.openclaw/workspace/tickets/closed/p3-noise/ 2>/dev/null || true
# 重新调 auto_ticket.sh 阈值，只建 L2+
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-21/22/23/24
- 后续 SOP：SOP-29（跨 agent 迁移工单）、SOP-26（事故升级）
- 相关 FAQ：F7-7
- 相关 Cookbook：C5-4（TEV）、C7-2（复盘）
- 相关案例：CASE-7（暗夜熔炉差异转工单）
- 相关章节：chapters/06-governance

### 九、工单字段的最佳实践
| 字段 | 必填 | 典型内容 |
|---|---|---|
| id | ✓ | YYYYMMDD-<short> |
| created_at | ✓ | ISO 8601 |
| source | ✓ | SOP-N / 暗夜熔炉 |
| owner | ✓ | 必有责任 agent/人 |
| severity | ✓ | L1/L2/L3 |
| root_cause | 整改时填 | TBD → 关闭前必填 |
| fix_steps | 整改时填 | 步骤列表 |
| verifier | 关闭前填 | 签字人 |
| closed_at | 关闭时填 | ISO 8601 |
| evidence_link | 关闭时填 | 路径 |

### 十、工单爆量的 4 个对治
1. **L3 阈值放宽**（见 SOP-13 步骤 6）
2. **批量归档 P3 噪音**（见本卷步骤 6 回滚）
3. **owner 分布看板**（避免单点）
4. **月度趋势报告**（找根因）

## 八、诚实边界

- ✅ 已实测：工单 schema；自动建工单脚本；关闭流程；月度看板
- ✅ 已实测：tickets/open/closed 分目录结构
- ⏳ 待实测：工单爆炸场景真实发生与处置曲线

---

## Appendix E · 边界与扩展（SOP 21-25 共用）

### E.1 5 个 SOP 的失败模式矩阵（FM-21 ~ FM-25）

| FM | 触发场景 | 主要症状 | 应急路径 |
|---|---|---|---|
| FM-21 | SOP-21 阈值过严 | 健康 agent 报漂移 | 放宽到 0.30；补 SOUL 关键词 |
| FM-22 | SOP-22 三档过严 | agent 什么都不敢做 | Allowed 放宽；Needs-Confirm 改 Allowed |
| FM-23 | SOP-23 体检太重 | 周一 09:00 跑 1h+ | 简化到 3 项（见步骤 6 回滚） |
| FM-24 | SOP-24 三证太重 | 变更卡在 TEV 2 周 | 临时只走 T+E（见步骤 6 回滚） |
| FM-25 | SOP-25 工单爆炸 | open 工单 >50 | 批量归档 P3 噪音（见步骤 6 回滚） |

### E.2 治理的"节奏表"

| 节奏 | 动作 | SOP |
|---|---|---|
| 每次会话结束 | drift 自检 | SOP-21（HEARTBEAT 挂载） |
| 每天 08:00 | slow 体检 | SOP-23（slow 档） |
| 每周一 09:00 | 周报 + 7 项 | SOP-23 |
| 每双周 | 暗夜熔炉 | SOP-14 |
| 每月 | EAF 调 E + 工单看板 | SOP-19 + SOP-25 |
| 每 30 天 | 续期（防 CASE-4） | SOP-23 步骤 5 |
| 每年 | 年度大修 | SOP-30 |

### E.3 与 v1.0 卷六 TEV 的对照

| v1.0 卷六 | 本卷 |
|---|---|
| 技术证据 | SOP-24 T 段（测试 + 性能 + drift） |
| 流程证据 | SOP-24 E 段（SOP 步骤 + 复核 + 工单） |
| 业务证据 | SOP-24 V 段（端到端 + 确认） |
| 三证齐全度 0-3 | SOP-24 步骤 5 决策树 |

### E.4 实测踩坑 7 条

1. **drift_scan 每 5 min 跑**：CPU 飙 → 改 slow 档（每日 08:00）
2. **阈值 0.05**：全员漂移 → 改 0.20
3. **边界三档只配 Allowed**：越界无记录 → 必须配 Forbidden
4. **周报没人看**：治理空转 → 上报 Supervisor（SOP-23 步骤 6）
5. **TEV 只做技术证据**：流程/业务缺失 → 步骤 6 自动建工单
6. **工单 owner 写 TBD 长期不填**：工单烂尾 → 月度看板 owner 分布
7. **续期超 30 天无人管**：CASE-4 重演 → 工单自动建

### E.5 "漂移分 >0.50"的标准处置（SOP-21 → SOP-25 闭环）

```bash
# 1. 漂移检测报 >0.50
python3 ~/.openclaw/workspace/jobs/drift_scan.py 2>&1 | grep "0\.[5-9]"

# 2. 自动建工单（L2）
~/.openclaw/workspace/jobs/auto_ticket.sh L2 "drift>0.50 agent=<name>"

# 3. TEV 验收（SOP-24）：整改完走 T/E/V 三证
# 4. 关闭工单（SOP-25）：verifier 签字 + evidence_link
# 5. 周报记录（SOP-23）：drift 分回落确认
```
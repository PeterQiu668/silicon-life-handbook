# SOP 分册 03 · 心跳与监控（SOP-11 ~ SOP-15）

> **《硅基生命手册（Silicon Life Handbook）· SOP 大全卷》**
> **v5.0 industry-standard · P2-1 · 从零编写**
> **实测环境**：OpenClaw **2026.9.4 (3a9d69d)** · macOS 26.x · 实测日期 2026-09-27
> **本机实测基线**：18 agent · heartbeat peter error 70x / kunlun error 99+x · 43 条 automation
> **License**：MIT

## ⚠️ OpenClaw 真名表

| ❌ 虚构 | ✅ 真名 |
|---|---|
| `openclaw agents health-check` | `openclaw health` / `openclaw doctor` |
| 顶层 `heartbeat` 字段 | **不存在**（心跳配置在 `agents/<agent>/HEARTBEAT.md`，不在 openclaw.json） |

## 业界对位表

| 手册概念 | 业界对位 |
|---|---|
| HEARTBEAT.md（心跳） | Liveness Probe / Watchdog Timer |
| cron（定时任务） | Cron / Scheduled Jobs（macOS 用 launchd 承载） |
| 暗夜熔炉（Night Forge） | Chaos Drill / GameDay |
| 失联恢复 | Failover / Reconnection Recovery |
| 告警链 | Alerting Pipeline / On-call Escalation |

## 本分册目录

| SOP | 标题 | 前置 | 后续 |
|---|---|---|---|
| SOP-11 | HEARTBEAT 三档频率 | SOP-10 | SOP-12 |
| SOP-12 | Cron 配置 | SOP-11 | SOP-13 |
| SOP-13 | 监控告警链 | SOP-11, SOP-12 | SOP-15 |
| SOP-14 | 暗夜熔炉演练 | SOP-3, SOP-13 | SOP-15 |
| SOP-15 | 失联恢复 | SOP-13, SOP-14 | SOP-26 |

---

# SOP-11 · HEARTBEAT 三档频率配置

## 一、目的

给 agent 配快/中/慢三档心跳（HEARTBEAT.md），兼顾灵敏与成本。

## 二、适用对象

新 agent 上线；心跳 error 飙升（peter 70x / kunlun 99+x）的治理。

## 三、前置条件

- [ ] agent IDENTITY 已配（SOP-10）
- [ ] 已读 C2-1（HEARTBEAT.md 配置：3 档心跳频率）
- [ ] 已统计本机 heartbeat error 基线

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 统计本机 heartbeat error 基线

```bash
# 本机实测：peter error 70x / kunlun error 99+x（2026-09-27）
grep -c "heartbeat.*error" ~/.openclaw/logs/*.log 2>/dev/null | head -5 || echo "查 gateway 日志目录，以本机实际路径为准"
```

```bash
# 按 agent 分组统计
grep -h "heartbeat" ~/.openclaw/logs/*.log 2>/dev/null | grep -oE "agent=[a-zA-Z0-9_-]+" | sort | uniq -c | sort -rn | head -10
```

### 步骤 2 · 写 HEARTBEAT.md 三档模板

```bash
cat > ~/.openclaw/workspace/agents/<name>/HEARTBEAT.md <<'EOF'
# HEARTBEAT.md · <agent-name>

## fast 档（高频存活探针）
- interval：5 min
- 做什么：gateway 可达性 ping + 关键进程存活
- 熔断：连续 3 次失败 → 降 medium 并告警

## medium 档（常规业务节拍）
- interval：30 min
- 做什么：pending 任务盘点 + 记忆滚动汇总 + drift 抽查（见 SOP-21）
- 熔断：连续 2 次失败 → 降 slow 并告警

## slow 档（日报级）
- interval：每日 08:00
- 做什么：全量体检 + 周报素材沉淀 + stale 日志清理
- 熔断：失败 1 次即告警（slow 失败 = 大问题）

## breaker（熔断器）
- escalation：fast→medium→slow 逐级降，slow 失败直接 on-call
- 恢复：连续 3 次成功自动升档

## Cross-references
- 调度器：Cron（见 SOP-12）
- 漂移：slow 档挂 drift_check（见 SOP-21）
- 监控：error 计数进告警链（见 SOP-13）
EOF
```

### 步骤 3 · 三档与 Cron 任务对应（C2-1 附录 J）

```bash
# 对应关系（不要重复触发）：
# fast   → Cron 任务 1-2（*/5 min）
# medium → Cron 任务 3-5（*/30 min）
# slow   → Cron 任务 6-8（每日 08:00）
# 汇报   → Cron 任务 9（每周一 09:00）
echo "对照 SOP-12 步骤 2 配置 Cron"
```

### 步骤 4 · 熔断阈值按 error 基线调参

```bash
# peter 70x / kunlun 99+x 说明阈值过松或链路真有问题
# 先按 CASE-9 诊断是"真死"还是"误报"，再调阈值
# 误报多 → 放宽 fast 熔断到连续 5 次
# 真死多 → 收紧并立即走 SOP-15
```

### 步骤 5 · 18 agent 批量下发三档模板

```bash
for d in ~/.openclaw/workspace/agents/*/; do
  name=$(basename "$d")
  test -f "$d/HEARTBEAT.md" || echo "缺 HEARTBEAT.md: $name"
done
```

### 步骤 6 · 端到端"杀一次心跳"验证熔断

```bash
# 沙箱先演（见 SOP-3），生产谨慎：
# 1. 停沙箱 agent 的 fast 任务
# 2. 观察是否按 breaker 降档并告警
# 3. 恢复后观察是否自动升档
openclaw health
```

### ✅ 检查清单

- [ ] HEARTBEAT.md 存在且含 fast/medium/slow/breaker 四段
- [ ] 三档 interval 与 Cron 任务一一对应、无重复触发
- [ ] 熔断阈值已按 error 基线调过
- [ ] 18 agent 全覆盖（无缺文件）
- [ ] 沙箱熔断演练通过
- [ ] error 计数接入告警链（SOP-13）

## 五、验证命令

```bash
openclaw health && openclaw doctor
# 期望输出：双通过
```

```bash
ls ~/.openclaw/workspace/agents/*/HEARTBEAT.md | wc -l
# 期望输出：18（与在编数一致）
```

## 六、回滚步骤

```bash
cp ~/.openclaw/workspace/agents/<name>/HEARTBEAT.md ~/.openclaw/workspace/agents/<name>/HEARTBEAT.md.bak.$(date +%F)
# 恢复单档（最保守：只留 slow）
# 或恢复 .bak 上一版
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-10（IDENTITY）
- 后续 SOP：SOP-12（Cron）、SOP-13（告警链）
- 相关 FAQ：F3-1（先证真死再谈配置）、F3-2（注册→匹配→执行三段查）
- 相关 Cookbook：C2-1（HEARTBEAT 3 档）、C7-4（heartbeat error 计数 + 告警链）
- 相关案例：CASE-9（心跳熔断实战：70x / 99+x 诊断修复）
- 相关章节：chapters/02-protocols、chapters/05-long-term

### 九、心跳三档的 5 个调参技巧
1. **fast 间隔 ≠ 越短越好**：1 min 会把 gateway 弄爆，建议 5 min
2. **medium 应避开业务高峰**：选 30 min 对齐 30 min 周期业务流
3. **slow 时间点选业务低峰**：如每日 08:00 或 22:00
4. **weekly 必设**：周一 09:00 是固定汇报点
5. **breaker 阈值与 error 基线挂钩**：本机 70x → 设 100 触发

### 十、心跳与 LLM 调用的成本权衡
fast 档每 agent 日 ~500 token，18 agent = 9000 token/日 = 270K token/月
折算成本：按本机模型 ¥0.001/1K token 计，约 ¥270/月，仅心跳消耗。
调档提示：fast 档如非关键可改 medium，能省 60%。

## 八、诚实边界

- ✅ 已实测：三档模板结构；C2-1 附录 J 对应关系；18 agent 路径；peter 70x / kunlun 99+x 基线数
- ✅ 已实测：`openclaw health` / `doctor` 真名
- ⏳ 待实测：breaker 自动升降档的运行时行为（需沙箱故障注入验证）

---

# SOP-12 · Cron 配置（定时任务）

## 一、目的

把"晨扫/日报/暗夜熔炉"定时任务稳定跑在 macOS launchd 上。

## 二、适用对象

SOP-11 三档心跳的调度承载；43 条 automation 的新增与维护。

## 三、前置条件

- [ ] SOP-11 三档已定（interval 已知）
- [ ] 已读 C2-2（Cron 配置）、C7-3（晨扫/日报/暗夜熔炉完整配置）
- [ ] macOS launchd 可用：`launchctl list` 有输出

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 盘点现有 automation（本机 43 条）

```bash
# 列出已有定时任务（以本机实际落点为准）
launchctl list 2>/dev/null | grep -i "openclaw\|agent" | head -20
ls ~/Library/LaunchAgents/ 2>/dev/null | grep -i "openclaw\|agent"
```

### 步骤 2 · 写 launchd plist 模板（以 fast 档为例）

```bash
cat > ~/Library/LaunchAgents/com.openclaw.agent.<name>.fast.plist <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.openclaw.agent.<name>.fast</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/peterqiu/.openclaw/workspace/jobs/<name>-fast.sh</string>
  </array>
  <key>StartInterval</key><integer>300</integer>
  <key>RunAtLoad</key><false/>
  <key>StandardOutPath</key><string>/tmp/openclaw-<name>-fast.log</string>
  <key>StandardErrorPath</key><string>/tmp/openclaw-<name>-fast.err</string>
</dict>
</plist>
EOF
echo "plist 已生成"
```

### 步骤 3 · 写任务脚本（含 drift_check 钩子）

```bash
mkdir -p ~/.openclaw/workspace/jobs
cat > ~/.openclaw/workspace/jobs/<name>-fast.sh <<'EOF'
#!/bin/bash
# fast 档任务：ping + 计数（对应 SOP-11 fast）
openclaw health >> /tmp/openclaw-<name>-fast.log 2>&1
# drift 抽查钩子（medium/slow 档加，fast 只 ping）
EOF
chmod +x ~/.openclaw/workspace/jobs/<name>-fast.sh
```

### 步骤 4 · 加载并验证（bootstrap 被拒走兼容路径）

```bash
launchctl load ~/Library/LaunchAgents/com.openclaw.agent.<name>.fast.plist
launchctl list | grep "<name>.fast"
# 期望输出：有该 Label，且 PID 或 LastExitStatus 可见
```

> ⚠️ 若 `bootstrap` 被拒（见 FAQ F3-15），走兼容路径：`launchctl load -w` 或检查 plist 权限为 644、属主为当前用户。

```bash
chmod 644 ~/Library/LaunchAgents/com.openclaw.agent.<name>.fast.plist
```

### 步骤 5 · 三档 plist 全量生成（medium 1800s / slow 每日 08:00）

```bash
# medium：StartInterval 1800
# slow：用 StartCalendarInterval（Hour 8, Minute 0）替代 StartInterval
# 汇报（每周一 09:00）：StartCalendarInterval（Weekday 1, Hour 9, Minute 0）
# 每档一个 plist + 一个 .sh，共 4 套/ agent（fast/medium/slow/weekly）
ls ~/Library/LaunchAgents/com.openclaw.agent.<name>.*.plist
```

### 步骤 6 · 防重复触发检查（Cron 与心跳不双跑）

```bash

### 九、launchd plist 的 6 个必检项
1. Label 唯一（不能与已有 plist 冲突）
2. ProgramArguments 第一项必须是解释器（/bin/bash）
3. StartInterval 与 StartCalendarInterval 二选一
4. RunAtLoad 通常设 false（避免启动时雪崩）
5. StandardOutPath / StandardErrorPath 可写
6. plist 文件权限 644

### 十、Cron 与 HEARTBEAT 的边界
Cron 做固定时刻执行（如汇报），HEARTBEAT 做周期性存活探针。
二者不要重叠（否则同一任务触发两次）。
# SOP-11 步骤 3 的对应表逐项核对：
# Cron 任务里不应再调 HEARTBEAT.md 已覆盖的检查
grep -l "drift_check" ~/.openclaw/workspace/jobs/*.sh
# 期望：只在 medium/slow 脚本出现，fast 不出现
```

### ✅ 检查清单

- [ ] 43 条基线已盘点（新增不冲突）
- [ ] fast/medium/slow/weekly 四套 plist + .sh 齐全
- [ ] `launchctl list` 可见且 LastExitStatus=0
- [ ] plist 权限 644、属主正确
- [ ] 日志落 /tmp 且可轮转（防爆盘）
- [ ] 无重复触发（fast 无 drift_check）

## 五、验证命令

```bash
launchctl list | grep -c "openclaw"
# 期望输出：≥4（单 agent 四档）或与 automation 总数一致
```

```bash
tail -5 /tmp/openclaw-<name>-fast.log
# 期望输出：最近 5 分钟内的 health 输出
```

## 六、回滚步骤

```bash
# 卸载单档
launchctl unload ~/Library/LaunchAgents/com.openclaw.agent.<name>.fast.plist
rm ~/Library/LaunchAgents/com.openclaw.agent.<name>.fast.plist
# 批量回滚：unload 全部新增后恢复 .bak
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-11（三档频率）
- 后续 SOP：SOP-13（告警链消费 Cron 输出）
- 相关 FAQ：F3-2（三段查）、F3-15（bootstrap 被拒兼容路径）
- 相关 Cookbook：C2-2（Cron）、C7-3（晨扫/日报/暗夜熔炉）
- 相关案例：CASE-7（编排节奏：晨扫→日报→暗夜熔炉的一天）
- 相关章节：chapters/05-long-term

## 八、诚实边界

- ✅ 已实测：launchd plist 模板结构；`launchctl list/load/unload` 真名；43 条 automation 基线数
- ✅ 已实测：F3-15 bootstrap 被拒现象存在
- ⏳ 待实测：43 条全量 plist 与本模板的逐项对账（需 production 普查）

---

# SOP-13 · 监控告警链

## 一、目的

把 heartbeat error 计数变成"看得见、叫得醒"的告警链。

## 二、适用对象

fleet 运维者；on-call 排班者；error 70x/99+x 持续超标时。

## 三、前置条件

- [ ] SOP-11 + SOP-12 就绪（有 error 数据流）
- [ ] 已读 C7-4（生产监控：heartbeat error 计数 + 告警链）
- [ ] 告警通道至少 1 个可用（IM / 邮件 / 推送）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 部署 error 计数脚本

```bash
cat > ~/.openclaw/workspace/jobs/heartbeat-count.sh <<'EOF'
#!/bin/bash
# 每 5 分钟跑：统计各 agent heartbeat error
LOGDIR=~/.openclaw/logs
OUT=/tmp/heartbeat-count.json
python3 - <<'PYEOF'
import re, json, glob
from collections import Counter
c = Counter()
for f in glob.glob('/Users/peterqiu/.openclaw/logs/*.log'):
    try:
        for line in open(f, errors='ignore'):
            if 'heartbeat' in line and 'error' in line:
                m = re.search(r'agent=([a-zA-Z0-9_-]+)', line)
                if m: c[m.group(1)] += 1
    except FileNotFoundError:
        pass
print(json.dumps(dict(c.most_common()), indent=2, ensure_ascii=False))
PYEOF
EOF
chmod +x ~/.openclaw/workspace/jobs/heartbeat-count.sh
~/.openclaw/workspace/jobs/heartbeat-count.sh
```

### 步骤 2 · 设三级告警阈值

```bash
# 阈值表（按本机基线 peter 70x / kunlun 99+x 制定）：
# L1 提醒：单 agent 日增 >20 → IM 群消息
# L2 警告：单 agent 日增 >50 → @on-call
# L3 紧急：任意 agent 小时增 >30 或 slow 档失败 → 电话/短信 + 走 SOP-15
cat > ~/.openclaw/workspace/jobs/alert-thresholds.json <<'EOF'
{"L1_daily": 20, "L2_daily": 50, "L3_hourly": 30}
EOF
```

### 步骤 3 · 接告警通道（_notify.sh）

```bash
cat > ~/.openclaw/workspace/jobs/_notify.sh <<'EOF'
#!/bin/bash
# 用法：_notify.sh <L1|L2|L3> "<消息>"
LEVEL="$1"; MSG="$2"
echo "[$(date '+%F %T')] [$LEVEL] $MSG" >> /tmp/openclaw-alerts.log
# IM 通道：按本机实际 webhook 填（飞书/Telegram/企业微信三选一）
# curl -s -X POST "$ALERT_WEBHOOK" -d "{\"msg\":\"[$LEVEL] $MSG\"}" >> /tmp/openclaw-alerts.log 2>&1
EOF
chmod +x ~/.openclaw/workspace/jobs/_notify.sh
~/.openclaw/workspace/jobs/_notify.sh L1 "告警链自检 ping"
tail -2 /tmp/openclaw-alerts.log
```

### 步骤 4 · 告警链接入 Cron（每 5 分钟一轮）

```bash
# 在 heartbeat-count.sh 尾部追加阈值判定 + _notify.sh 调用
# L1/L2/L3 分级调用，保证 slow 失败直达 L3
echo "接入点：heartbeat-count.sh → 阈值判定 → _notify.sh → IM/短信"
```

### 步骤 5 · 建 on-call 排班表

```bash
cat > ~/.openclaw/workspace/oncall-schedule.md <<'EOF'
# on-call 排班表
| 周期 | 值班人 | 升级路径 |
|---|---|---|
| 本周 | <name> | L3 未响应 15min → 升级丘总 |
| 下周 | <name> | 同上 |
EOF
```

### 步骤 6 · 沙箱"点火"验证全链路

```bash
# 沙箱模拟一次 L3：确认 IM/短信真能收到
~/.openclaw/workspace/jobs/_notify.sh L3 "沙箱演练：L3 告警链测试（非真实故障）"
# 期望：值班人在 5 分钟内确认收到
```

### ✅ 检查清单

- [ ] 计数脚本每 5 分钟输出 JSON
- [ ] L1/L2/L3 阈值已按基线制定
- [ ] _notify.sh 自检 ping 到达
- [ ] Cron 接入完成（判定→通知闭环）
- [ ] on-call 表有人值班
- [ ] 沙箱 L3 演练值班人确认收到

## 五、验证命令

```bash
~/.openclaw/workspace/jobs/heartbeat-count.sh
# 期望输出：JSON 含各 agent error 数（peter/kunlun 应可见）
```

```bash
tail -5 /tmp/openclaw-alerts.log
# 期望输出：最近告警记录，自检 ping 在列
```

## 六、回滚步骤

```bash
# 1. 停计数 Cron（unload 对应 plist，见 SOP-12）
# 2. _notify.sh 改为只写本地日志（注释掉 webhook 行）
# 3. 阈值文件改宽松（L1/L2/L3 ×10），防误报轰炸
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-11、SOP-12
- 后续 SOP：SOP-15（L3 直达失联恢复）
- 相关 FAQ：F3-1、F3-2
- 相关 Cookbook：C7-4（heartbeat error 计数 + 告警链）
- 相关案例：CASE-9（心跳熔断实战）
- 相关章节：chapters/05-long-term、chapters/07-coordination

### 九、告警链的 5 个 anti-pattern
1. **L1 阈值过低**：告警轰炸，值班人麻木
2. **L3 通道冗余**：短信 + 电话 + IM 同时 → 信息混乱
3. **告警文案过长**：值班人找不到关键信息
4. **告警不闭环**：响完不跟踪 → 重复告警
5. **on-call 表失效**：值班人手机号过期 → L3 无人接

### 十、告警内容模板（精简版）
```
[LEVEL] time=HH:MM agent=<name> metric=<metric> value=<X> threshold=<Y>
action: <建议操作>
owner: <人名>
link: <工单或日志路径>
```
5 行内讲清：等级 / 时间 / 谁 / 啥指标 / 处置建议。

## 八、诚实边界

- ✅ 已实测：计数脚本逻辑；阈值表结构；_notify.sh 本地日志链路；peter/kunlun 基线数
- ⏳ 待实测：IM webhook 真实到达（$ALERT_WEBHOOK 以本机实际配置为准，未硬编码）
- ⏳ 待实测：L3 短信/电话通道（需真实 on-call 环境）

---

# SOP-14 · 暗夜熔炉演练（Night Forge / GameDay）

## 一、目的

定期"主动搞破坏"，验证 SOP-11~13 在真实故障下真能用。

## 二、适用对象

fleet 治理者；每双周一次；新 SOP 上线前的验收。

## 三、前置条件

- [ ] SOP-3 沙箱可用（演练先在沙箱点火）
- [ ] SOP-13 告警链就绪（演练要验证它）
- [ ] 已读 C7-3（暗夜熔炉完整配置）、CASE-7（编排节奏的一天）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 定演练剧本（三选一，由简到难）

```bash
cat > /tmp/forge-plan-$(date +%F).md <<'EOF'
# 暗夜熔炉剧本（本次三选一）
- [ ] 剧本 A（简单）：杀沙箱 agent fast 心跳 → 验证 breaker 降档 + L1 告警
- [ ] 剧本 B（中等）：断沙箱 gateway 10 分钟 → 验证 L2 + SOP-15 失联恢复
- [ ] 剧本 C（困难）：生产只读演练：slow 档失败注入 → 验证 L3 + on-call 升级
EOF
cat /tmp/forge-plan-$(date +%F).md
```

### 步骤 2 · 沙箱点火（剧本 A/B）

```bash
# 剧本 A：停沙箱 fast plist
launchctl unload ~/Library/LaunchAgents/com.openclaw.agent.<sandbox>.fast.plist 2>/dev/null || echo "沙箱 plist 名以实际为准"
sleep 300
# 观察：breaker 是否降档？L1 是否响？
tail -20 /tmp/openclaw-alerts.log
```

### 步骤 3 · 记录"发现"（演练的唯一产出）

```bash
cat > ~/.openclaw/workspace/forge-log-$(date +%F).md <<'EOF'
# 暗夜熔炉记录 <日期>
## 剧本
## 预期
## 实际
## 差异（= 修复工单，见 SOP-25）
## 用时（MTTR）
EOF
```

### 步骤 4 · 生产只读演练（剧本 C，禁破坏性操作）

```bash
# 只读：slow 档 dry-run，不真停任何东西
openclaw health && openclaw doctor
~/.openclaw/workspace/jobs/heartbeat-count.sh
# 确认 L3 链路通（发测试 L3，标注"演练"）
~/.openclaw/workspace/jobs/_notify.sh L3 "演练：L3 链路测试（非故障）"
```

### 步骤 5 · 差异转工单（见 SOP-25）

```bash
# 每个"预期 vs 实际"差异 = 1 个整改工单
# 工单落点：~/.openclaw/workspace/tickets/
mkdir -p ~/.openclaw/workspace/tickets
echo "差异数 = 工单数，一一建单"
```

### 步骤 6 · 复盘归档（进 case-library 候选）

```bash
ls ~/.openclaw/workspace/forge-log-*.md
# 好的演练记录可升格为 CASE（见 case-library 02-production-patterns.md 格式）
```

### ✅ 检查清单

- [ ] 剧本已定且分级（A/B 沙箱，C 生产只读）
- [ ] 沙箱点火完成且现象已记录
- [ ] 告警链在演练中真响过（L1/L2/L3 至少一级）
- [ ] 差异全部转工单（SOP-25）
- [ ] MTTR 已记录
- [ ] 复盘已归档（forge-log-*.md）

## 五、验证命令

```bash
ls ~/.openclaw/workspace/forge-log-*.md
# 期望输出：至少 1 个本次演练记录
```

```bash
grep -c "演练" /tmp/openclaw-alerts.log
# 期望输出：≥1（演练告警与真实告警可区分）
```

## 六、回滚步骤

```bash
# 演练的回滚 = 恢复被"破坏"的沙箱：
launchctl load ~/Library/LaunchAgents/com.openclaw.agent.<sandbox>.fast.plist 2>/dev/null || true
openclaw health
# 生产只读演练无需回滚（未做破坏性操作）
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-3（沙箱）、SOP-13（告警链）
- 后续 SOP：SOP-15（演练剧本 B 直达）、SOP-25（差异转工单）
- 相关 FAQ：F3-1、F6-6（9/21 案例三查：演练要覆盖通道/积压/白名单）
- 相关 Cookbook：C7-3（暗夜熔炉配置）、C7-2（复盘模板）
- 相关案例：CASE-7（编排节奏的一天：熔炉在 22:00 档）、CASE-9（熔断实战是演练的"开卷考"）
- 相关章节：chapters/05-long-term、chapters/08-evolution

### 九、暗夜熔炉剧本选型的 3 个标准
1. **新 SOP 上线**：用剧本 A（最轻）
2. **季度验收**：用剧本 B（中等）
3. **年度大修前**：用剧本 C（生产只读）
周期：每月至少 1 次 A、每季度 1 次 B、每年 1 次 C。

### 十、暗夜熔炉的差异归档原则
- **预期 vs 实际** 差异 = 整改工单（SOP-25）
- **演练记录** = 升格 case-library 候选
- **MTTR 统计** = 月度看板上墙
- **失败演练** ≠ 失败（不记录 = 失败）

## 八、诚实边界

- ✅ 已实测：剧本分级思路；forge-log 记录格式；演练 vs 真实告警区分标记；工单落点
- ⏳ 待实测：完整双周演练闭环（需生产排期执行）
- ⏳ 待实测：剧本 C 的 L3 真实升级时延（需 on-call 配合）

---

# SOP-15 · 失联恢复（Failover / Reconnection）

## 一、目的

agent 失联后 30 分钟内恢复上线，不丢任务。

## 二、适用对象

L3 告警已响、slow 档失败、gateway 不可达时的 on-call 者。

## 三、前置条件

- [ ] SOP-13 告警链已触发 L2/L3（知道谁失联）
- [ ] 有最近备份（`openclaw backup create` 24h 内）
- [ ] 已读 CASE-9（心跳熔断实战）、FAQ F3-1（先证真死）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 先证"真死"（F3-1 三段查，5 分钟）

```bash
# 1. 进程还在吗
ps aux | grep -i "openclaw.*gateway" | grep -v grep || echo "gateway 进程无"
# 2. 端口还在听吗（端口以本机 openclaw.json 为准）
python3 -c "import json; print([v for k,v in json.load(open('/Users/peterqiu/.openclaw/openclaw.json')).items() if isinstance(v,int)])"
# 3. health 什么反应
timeout 15 openclaw health; echo "exit=$?"
```

判定：进程无 + 端口无 + health 超时 = 真死；任一存活 = 假死（走 F3-2 三段查注册→匹配→执行）。

### 步骤 2 · 保护现场（恢复前先留证）

```bash
mkdir -p /tmp/openclaw-incident-$(date +%F-%H%M)
cp /tmp/openclaw-*.log /tmp/openclaw-incident-$(date +%F-%H%M)/ 2>/dev/null || true
cp ~/.openclaw/openclaw.json /tmp/openclaw-incident-$(date +%F-%H%M)/openclaw.json.snapshot
tail -100 ~/.openclaw/logs/*.log 2>/dev/null > /tmp/openclaw-incident-$(date +%F-%H%M)/tail.log || echo "日志路径以本机为准"
ls /tmp/openclaw-incident-*/
```

### 步骤 3 · 重启 gateway（真死路径）

```bash
pkill -f "openclaw.*gateway" || true
sleep 3
openclaw health
# 若仍失败：检查端口占用（F1-6）
lsof -i -P 2>/dev/null | grep -i "openclaw\|LISTEN" | head -5 || ss -tlnp 2>/dev/null | head -10
```

### 步骤 4 · 恢复 Cron（重启后任务可能掉线）

```bash
# 逐个检查 plist 状态，掉线的 reload
for p in ~/Library/LaunchAgents/com.openclaw.agent.*.plist; do
  launchctl list 2>/dev/null | grep -q "$(basename $p .plist)" || echo "掉线：$p"
done
```

### 步骤 5 · 任务补跑（失联期间的 slow/medium 欠账）

```bash
# 手工触发一次 medium + slow（补 drift 抽查与体检）
~/.openclaw/workspace/jobs/<name>-medium.sh 2>/dev/null || echo "按本机实际 job 名补跑"
openclaw agent --agent <name> --message "失联恢复自检：汇报 pending 任务" 2>&1 | head -10
```

### 步骤 6 · 关闭告警 + 写复盘（MTTR 落盘）

```bash
~/.openclaw/workspace/jobs/_notify.sh L1 "恢复：<agent> 已上线，MTTR=<X>min（故障复盘见 tickets/）"
ls ~/.openclaw/workspace/tickets/ | tail -3
```

### ✅ 检查清单

- [ ] 真死/假死已判定（F3-1）
- [ ] 现场已留证（incident 快照目录）
- [ ] gateway 重启后 `health` 通过
- [ ] Cron 掉线已补齐
- [ ] 欠账任务已补跑（drift 抽查不缺）
- [ ] 告警已关闭 + 复盘工单已建（MTTR 落盘）

## 五、验证命令

```bash
openclaw health && openclaw doctor
# 期望输出：双通过
```

```bash
openclaw agent --agent <name> --message "ping" 2>&1 | head -3
# 期望输出：失联 agent 恢复响应
```

## 六、回滚步骤

```bash
# 恢复失败 → 从备份重建（见 SOP-5 恢复路径）：
# 1. pkill gateway
# 2. 用 backups 恢复 openclaw.json + workspace
# 3. 重启验证
# 仍失败 → 升级为 SOP-26 事故分级（P0/P1 流程）
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-13（告警先响）、SOP-14（演练过）
- 后续 SOP：SOP-26（恢复失败升级事故）
- 相关 FAQ：F3-1（真死判定）、F3-2（三段查）、F1-6（端口占用）
- 相关 Cookbook：C7-4（error 计数）、C7-2（复盘模板）
- 相关案例：CASE-1（8/19 军团断线全链路复盘）、CASE-9（心跳熔断实战）
- 相关章节：chapters/05-long-term

### 九、失联恢复的 MTTR 分级
| 级别 | MTTR 目标 | 失联时长 |
|---|---|---|
| P3 | <15 min | <5 min |
| P2 | 15-30 min | 5-30 min |
| P1 | 30-60 min | 30 min-2h |
| P0 | >60 min | >2h |
每超一级必建 L3 工单 + 周报标注。

### 十、失联恢复的现场留证（5 件套）
1. openclaw.json.snapshot
2. tail.log（最近 100 行）
3. process list（ps aux 输出）
4. health 失败输出
5. 工单链接（auto_ticket.sh L3 输出）
5 件套不齐 = 复盘无效。

## 八、诚实边界

- ✅ 已实测：真死三段查命令；现场留证流程；Cron 掉线检查循环；MTTR 落盘格式
- ✅ 已实测：本机 gateway 重启 + health 验证链路
- ⏳ 待实测：30 分钟 MTTR 达成率（需真实故障统计）

---

## Appendix C · 边界与扩展（SOP 11-15 共用）

### C.1 5 个 SOP 的失败模式矩阵（FM-11 ~ FM-15）

| FM | 触发场景 | 主要症状 | 应急路径 |
|---|---|---|---|
| FM-11 | SOP-11 三档阈值过严 | fast 档误报熔断 → agent 频繁降档 | 放宽到连续 5 次失败才熔断 |
| FM-12 | SOP-12 plist 路径错 | Cron 不触发 | `chmod 644` + 重启 launchd（见 F3-15） |
| FM-13 | SOP-13 阈值设低 | L1 告警轰炸 | 阈值 ×3（见 SOP-13 步骤 6 回滚） |
| FM-14 | SOP-14 沙箱演练写错 | 沙箱启动失败 → 演练延后 | 重读 SOP-3 步骤 3 端口错开 |
| FM-15 | SOP-15 现场未留证 | 恢复成功但根因不明 | 必跑步骤 2 留证（incident 快照目录） |

### C.2 心跳三档的"成本-灵敏度"权衡

| 档 | 间隔 | 主要任务 | 单 agent 日 token 消耗估算 | 适用场景 |
|---|---|---|---|---|
| fast | 5 min | ping + 进程存活 | ~500 | 关键业务（Supervisor） |
| medium | 30 min | 业务盘点 + drift 抽查 | ~200 | 日常 18 agent |
| slow | 每日 08:00 | 体检 + 提炼 | ~50 | 全 agent 全跑 |
| weekly | 每周一 09:00 | 周报 + 升级治理 | ~100 | 仅 Supervisor |

> 注：token 估算基于本机 18 agent 实测；不同模型差异大。

### C.3 与 v4.0 8 卷的对应

| v4.0 卷 | 本分册 SOP |
|---|---|
| 卷二 协议 | SOP-11 HEARTBEAT 是协议层之一 |
| 卷四 训练 | SOP-14 暗夜熔炉是训练期必走 |
| 卷五 长期 | SOP-11/12/13 持续运行 |
| 卷七 协同 | SOP-15 失联恢复触发协同 |
| 卷八 演进 | SOP-14 演练积累 case-library |

### C.4 实测踩坑 7 条

1. **fast 档间隔设 1 min**：gateway 被 ping 弄爆 → 改 5 min
2. **Cron plist 权限 600**：launchctl 不识别 → 改 644
3. **StartInterval + StartCalendarInterval 混用**：plist 校验失败 → 二选一
4. **告警 webhook 写到硬编码 URL**：换 webhook 通知全断 → 用环境变量
5. **暗夜熔炉在生产裸跑**：炸了 → 沙箱先演练
6. **失联恢复不保留现场**：恢复后不知道根因 → 步骤 2 强制留证
7. **on-call 表无人值班**：L3 响了无人接 → 周一体检 SOP-23 第 7 项

### C.5 "真死 vs 假死"判定速查

| 现象 | 真死 | 假死 |
|---|---|---|
| 进程不在 | ✓ | ✗ |
| 端口不在 | ✓ | ✗ |
| health 超时 | ✓ | ✗ |
| health 报"注册未匹配" | ✗ | ✓ |
| agent 反复重启 | 部分 | 主要 |

判定真死后再谈配置（见 F3-1）——否则改了配置也无济于事。

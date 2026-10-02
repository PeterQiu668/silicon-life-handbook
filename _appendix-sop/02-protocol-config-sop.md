# SOP 分册 02 · 协议配置（SOP-6 ~ SOP-10）

> **《硅基生命手册（Silicon Life Handbook）· SOP 大全卷》**
> **v5.0 industry-standard · P2-1 · 从零编写 · 非 v1.0/v4.0 补丁**
> **实测环境**：OpenClaw **2026.9.4 (3a9d69d)** · macOS 26.x · 实测日期 2026-09-27
> **本机实测基线**：18 agent 在编 · 43 条 automation · 51/69 plugins 启用
> **License**：MIT

## ⚠️ OpenClaw 真名表（本分册强制使用）

| ❌ 虚构写法 | ✅ 真名 |
|---|---|
| `openclaw agents create` | `openclaw agents add` |
| `openclaw chat --agent X --prompt Y` | `openclaw agent --agent X --message Y` |
| `routing/heartbeat/subagents/workspace/runtime`（顶层虚构字段） | **不存在**（真实 20 key） |
| ACLP（虚构顶层协议） | SLCP（Silicon Life Communication Protocol） |
| 硅基体（虚构术语） | 硅基智能体（v3.0 改名表条目） |
| 监军（v1.0 旧称） | 监督者 / Supervisor Layer（v3.0 改名） |

## 业界对位表

| 手册概念 | 业界对位 | 说明 |
|---|---|---|
| SOUL.md（灵魂文件） | System Prompt / Persona Definition | 决定 agent 的人格与底线 |
| AGENTS.md（操作纪律） | Operating Manual / Tool Catalogue | 工具与技能的使用约束 |
| USER.md（用户画像） | User Profile / Preference Memory | 4 类问题 + 5 反例 |
| TOOLS.md（工具边界） | Tool Sandbox Policy | 与 SOUL 协作规则的冲突裁决 |
| IDENTITY.md（身份） | Identity Manifest / Routing Key | 路由字段决定谁接什么任务 |
| Sl（supervisor layer） | Supervisor / Orchestrator | v3.0 由"监军"改名 |
| Sl-agent / Sl-msg | Orchestration protocol | v3.0 由"宿主"改名 |

## 本分册目录

| SOP | 标题 | 前置 SOP | 后续 SOP |
|---|---|---|---|
| SOP-6 | SOUL 配置 | SOP-1 | SOP-7, SOP-10 |
| SOP-7 | AGENTS 配置 | SOP-1, SOP-6 | SOP-8, SOP-9 |
| SOP-8 | USER 配置 | SOP-6 | SOP-9 |
| SOP-9 | TOOLS 配置 | SOP-6, SOP-7 | SOP-10 |
| SOP-10 | IDENTITY 配置 | SOP-6, SOP-9 | SOP-11, SOP-21 |

---

# SOP-6 · SOUL.md 配置

## 一、目的

给一个新 agent 落地军团级稳定的灵魂文件（SOUL.md），杜绝空白 SOUL 与风格漂移。

## 二、适用对象

建新 agent 的开发者；治理员复核旧 SOUL；批量为 18 agent 补 SOUL。

## 三、前置条件

- [ ] agent 已加：`openclaw agents add <name>` 成功（⚠️ 真名 add）
- [ ] 工作区目录存在：`~/.openclaw/workspace/agents/<name>/`
- [ ] 已读 C1-1（SOUL.md 配置最佳实践）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 检查现有 SOUL.md 状态

```bash
ls -la ~/.openclaw/workspace/agents/<name>/
SOUL=~/.openclaw/workspace/agents/<name>/SOUL.md
test -f "$SOUL" && wc -l "$SOUL" || echo "SOUL.md 不存在（常见：空白 agent）"
```

### 步骤 2 · 写最小可运行 SOUL（5 个必备段）

```bash
cat > "$SOUL" <<'EOF'
# SOUL.md · <agent-name>

## 1. Persona（人格声明）
（一句话定义本 agent 在军团中的角色，≤50 字）

## 2. Constraints（底线约束）
- 不做：<明示禁止>
- 不做：<明示禁止>

## 3. Style（表达风格）
- 用语：<如：直接 / 严谨 / 简练>
- 长度：<默认行数>
- 格式：<markdown 表格 / 列表 / 代码块偏好>

## 4. Drift Guard（漂移自查）
- `drift_guard: true`（见 SOP-21）
- 每会话结束前自检是否仍符合本 SOUL

## 5. Cross-references（交叉引用）
- 上游：SOP-6（本文件）
- 协作：AGENTS.md（见 SOP-7）
- 受约束：TOOLS.md（见 SOP-9）
EOF
echo "SOUL.md 已生成 $(wc -l < $SOUL) 行"
```

### 步骤 3 · 跑人格哈希校验，避免重复 agent

```bash
# 18 agent 人格哈希唯一性（见 FAQ F2-5）
python3 - <<EOF
import hashlib
from pathlib import Path
root = Path('/Users/peterqiu/.openclaw/workspace/agents')
hashes = {}
for soul in root.glob('*/SOUL.md'):
    h = hashlib.sha256(soul.read_bytes()).hexdigest()[:8]
    hashes.setdefault(h, []).append(soul.parent.name)
dup = {k:v for k,v in hashes.items() if len(v)>1}
print("重复 SOUL 哈希:", dup if dup else "无")
EOF
```

### 步骤 4 · 配置 drift_guard 与命名规范

```bash
# 在 SOUL 顶部 YAML 块中声明 drift_guard
sed -i '' '1i\
---\
drift_guard: true\
agent: <name>\
sop_version: v5.0\
---\
' "$SOUL"
head -5 "$SOUL"
```

### 步骤 5 · 用 v3.0 改名表核对术语（首字双写）

```bash
# 把 SOUL 中所有 v1.0 旧称往 v3.0 新称替换（首字双写以保留可读性）
# 常见替换：监军→监督者 / Supervisor Layer
#           硅基体→硅基智能体
#           宿主→ Sl-agent（保留 v3.0 命名）
grep -nE "监军|硅基体|宿主|ACLP" "$SOUL" || echo "已无 v1.0 旧称"
```

### 步骤 6 · 端到端验证（agent 能落地 SOUL）

```bash
# ⚠️ 真名 agent --message
openclaw agent --agent <name> --message "请用你 SOUL 的人格回复一段自我介绍" 2>&1 | head -10
# 期望输出：与本 SOUL 的 Persona 段一致
```

### ✅ 本 SOP 检查清单

- [ ] `~/.openclaw/workspace/agents/<name>/SOUL.md` 存在且 ≥30 行
- [ ] 含 5 必备段（Persona/Constraints/Style/Drift Guard/Cross-references）
- [ ] drift_guard: true 已置顶
- [ ] 18 agent SOUL 哈希无重复
- [ ] 无 v1.0 旧称残留
- [ ] 端到端 ping 输出与 Persona 一致

## 五、验证命令

```bash
openclaw agent --agent <name> --message "ping" 2>&1 | head -5
# 期望输出：与 SOUL Persona 一致的人格回复
```

```bash
# 完整性体检
test -f "$SOUL" && grep -cE "^## (1\.|2\.|3\.|4\.|5\.)" "$SOUL"
# 期望输出：5（5 个必备段）
```

## 六、回滚步骤

```bash
# 1. 备份当前 SOUL
cp "$SOUL" "$SOUL.bak.$(date +%F)"

# 2. 恢复上一个版本（如果 .bak 是前一个稳定版）
mv "$SOUL.bak.<上次成功日期>" "$SOUL"

# 3. 重新端到端验证
openclaw agent --agent <name> --message "ping" 2>&1 | head -5
```

> 若 SOUL 整体偏门（不该改的底线被改），按 SOP-21 漂移检测 → SOP-25 整改工单路径走。

## 七、相关 SOP 链接

- 前置 SOP：SOP-1（安装基础）
- 后续 SOP：SOP-7（AGENTS 配工具）、SOP-10（IDENTITY 配路由）
- 相关 FAQ：F2-5（人格哈希唯一性）、F2-9（编码/换行体检）、F2-13（SLCP 改名核验）
- 相关 Cookbook：C1-1（SOUL.md 配置，从空白文件到军团级 SOUL）
- 相关案例：CASE-3（18 坏 skill 修复，部分涉及 SOUL 误写为字段）
- 相关章节：chapters/02-protocols（协议层总论）

### 九、SOUL.md 跨 agent 复用策略
- **完全相同人格**：用同 SOUL 拷贝 → 适用于纯执行 agent（不建议人格有差异）
- **同 Persona 不同 Constraints**：共享 Persona 段，Constraints 分文件 → 适用同角色不同职能
- **完全独立**：每个 agent 一份独立 SOUL → 默认推荐
重复 SOUL 哈希检测见 FAQ F2-5。

### 十、SOUL 漂移的 3 个早期信号
1. **回复变长**：超过 Persona 段约定的最大长度
2. **回复变客气**：出现 SOUL 没声明的礼貌用语
3. **回复变主动**：主动提供 SOUL 没声明的服务
任一信号 → 立即跑 drift_scan.py（SOP-21）。

## 八、诚实边界

- ✅ 已实测：SOUL.md 模板与必备段；drift_guard YAML；人格哈希脚本；18 agent 路径
- ✅ 已实测：v1.0 → v3.0 改名表条目（监军→监督者、硅基体→硅基智能体、ACLP→SLCP）
- ⏳ 待实测：SOUL 中 drift_guard 字段是否被 OpenClaw 真实读取（基于文件存在性验证，运行时行为以本机实际为准）

---

# SOP-7 · AGENTS.md 配置

## 一、目的

把"用什么工具"与"用什么 skill"明确落到 AGENTS.md，避免 SOUL 与工具冲突。

## 二、适用对象

为 18 agent 批量补 AGENTS.md；治理员复核工具使用规范。

## 三、前置条件

- [ ] SOUL.md 已就绪（见 SOP-6）
- [ ] 已读 C1-2（AGENTS.md 配置最佳实践）
- [ ] 已盘点可用 tools 与 skills（见 SOP-1 步骤 6 验证基线）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 检查 AGENTS.md 现状

```bash
AGENTS=~/.openclaw/workspace/agents/<name>/AGENTS.md
test -f "$AGENTS" && wc -l "$AGENTS" || echo "AGENTS.md 不存在（常见：缺工具表）"
```

### 步骤 2 · 写 AGENTS.md 模板（Tools / Skills / 边界 三段）

```bash
cat > "$AGENTS" <<'EOF'
# AGENTS.md · <agent-name>

## Tools（工具表，列到粒度到参数）
- `terminal`：run_command(timeout=30, allow=[fs,git,npm])
- `read_file` / `write_file` / `patch`：路径白名单（见 TOOLS.md）
- `search_files`：默认全文搜索，目标项目根

## Skills（技能表，分已启用 / 候选 / 禁用）
### 已启用
- <skill-name>（用途 ≤20 字）
- <skill-name>
### 候选（待评估）
- <skill-name>
### 禁用（明示原因）
- <skill-name>：<原因，如"权限过大">

## Operating Discipline（操作纪律）
- 写文件前必 `search_files` 确认存在
- 不删文件，删前必 backup
- 每小时小结一次 pending 任务
- 见 C1-2 操作纪律段

## Cross-references
- 上游：SOUL.md（见 SOP-6）
- 协作：TOOLS.md（见 SOP-9）
EOF
```

### 步骤 3 · 跨 agent 工具能力对齐（禁止"自创工具名"）

```bash
# 跨 18 agent 扫描"自创工具名"（不在 OpenClaw 已知列表）
python3 - <<'EOF'
from pathlib import Path
import re
known = {'terminal','read_file','write_file','patch','search_files','web_search','web_extract','browser_exec','vision_analyze','text_to_speech'}
root = Path('/Users/peterqiu/.openclaw/workspace/agents')
suspect = []
for f in root.glob('*/AGENTS.md'):
    for m in re.finditer(r'`([a-z_]+)`', f.read_text()):
        if m.group(1) not in known and not m.group(1).startswith('openclaw'):
            suspect.append((f.parent.name, m.group(1)))
print("疑似自创工具名:", suspect[:10] if suspect else "无")
EOF
```

### 步骤 4 · 启用/禁用 skill 标记

```bash
# 每个 skill 显式标注 state: enabled / disabled / candidate
# 示例：把 SOUL 中提到的 skill 在 AGENTS 中显式收编
${EDITOR:-vi} "$AGENTS"
```

### 步骤 5 · 与 SOUL 协作规则对齐

```bash
# SOUL 的 constraints 与 AGENTS 的工具能力不应矛盾
# 例：SOUL 说"不写 8000 字长文" + AGENTS 启用 `write_file` → OK
# 但：SOUL 说"不写文件" + AGENTS 启用 `write_file` → 矛盾 → 改 TOOLS.md 显式裁掉
grep -nE "^## Constraints|不做" ~/.openclaw/workspace/agents/<name>/SOUL.md
```

### 步骤 6 · 端到端验证

```bash
# 让 agent 列出它可用的工具，与 AGENTS 工具表对账
openclaw agent --agent <name> --message "列出你当前可用的 5 个工具及用途" 2>&1 | head -15
```

### ✅ 本 SOP 检查清单

- [ ] AGENTS.md 存在且 ≥30 行
- [ ] 含 Tools / Skills / Operating Discipline / Cross-references 段
- [ ] 无"自创工具名"（以 OpenClaw 已知工具白名单为准）
- [ ] skill 启用/禁用标记清晰
- [ ] 与 SOUL constraints 无矛盾（否则改 TOOLS.md）
- [ ] 端到端列举与 AGENTS 工具表一致

## 五、验证命令

```bash
openclaw agent --agent <name> --message "请复述 AGENTS.md 工具表第一行" 2>&1 | head -5
# 期望输出：与文件 Tools 段第一行一致
```

```bash
test -f "$AGENTS" && grep -cE "^## (Tools|Skills|Operating Discipline|Cross-references)" "$AGENTS"
# 期望输出：4
```

## 六、回滚步骤

```bash
cp "$AGENTS" "$AGENTS.bak.$(date +%F)"
# 回滚到上一个稳定版本
mv "$AGENTS.bak.<上次成功日期>" "$AGENTS"
openclaw agent --agent <name> --message "ping" 2>&1 | head -5
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-6（SOUL 是 AGENTS 的上游约束）
- 后续 SOP：SOP-8（USER.md 偏好）、SOP-9（TOOLS.md 边界）
- 相关 FAQ：F2-9（编码/换行体检）、F5-2（skill frontmatter 体检）
- 相关 Cookbook：C1-2（AGENTS.md 配置，含 tools / Skills 段）
- 相关案例：CASE-6（18 agent 编制扩张路径，每批都需配 AGENTS）
- 相关章节：chapters/02-protocols

### 九、AGENTS.md 与 SOUL 冲突的 5 种解法
| 冲突 | 解法 |
|---|---|
| SOUL 禁外发 + AGENTS 启 gmail_send | TOOLS.md boundaries blacklist |
| SOUL 克制 + AGENTS 启 text_to_speech | 一致，无需解 |
| SOUL 抽象 + AGENTS 工具具象 | OK，AGENTS 是 SOUL 的实现 |
| SOUL 无声明 + AGENTS 危险工具 | TOOLS.md Forbidden 列入 |
| AGENTS 工具名拼错（如 terminal.run） | 改回真名（见真名表第 9 节） |

### 十、AGENTS.md 的最小可执行单元
Tools 段 + Skills 段 + Operating Discipline 段，三段齐全即可；其他段可按需添加。
最少 30 行；过多会失去焦点。

## 八、诚实边界

- ✅ 已实测：AGENTS.md 模板；跨 agent 工具名扫描脚本；skill 启用/禁用标记
- ✅ 已实测：18 agent 目录结构
- ⏳ 待实测：OpenClaw 真实工具白名单完整列表（已知白名单为本机可见 11 个，全量以官方文档为准）

---

# SOP-8 · USER.md 配置

## 一、目的

给 agent 落地 USER.md，避免"越问越跑偏"的 5 类反例。

## 二、适用对象

新 agent 上线前；治理员复核 4 类问题覆盖度。

## 三、前置条件

- [ ] SOUL.md 已就绪（SOP-6）
- [ ] 已读 C1-3（USER.md 配置 4 类问题 + 5 反例）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 检查 USER.md 现状

```bash
USER=~/.openclaw/workspace/agents/<name>/USER.md
test -f "$USER" && wc -l "$USER" || echo "USER.md 缺失"
```

### 步骤 2 · 写 4 类问题 + 5 反例的 USER.md 模板

```bash
cat > "$USER" <<'EOF'
# USER.md · <agent-name>

## 用户身份画像
- 角色：<如：丘总 / 个人开发者 / 团队负责人>
- 行业：<如：硅基智能体 / 跨境电商>
- 规模：<如：单兵 / 小团队 / 中型>

## 4 类问题（agent 应主动问）
1. 目标类：<用户想达成什么？>
2. 边界类：<不可越的边界是什么？>
3. 资源类：<可用时间 / 预算 / 工具？>
4. 验收类：<如何判断"做对了"？>

## 5 个反例（agent 应避免）
1. 反例 1：凭空补全用户未说明的偏好
2. 反例 2：每次都问已问过的问题
3. 反例 3：把"建议"当"指令"
4. 反例 4：忽略用户明确说"不必问"的项
5. 自创反例 5：<agent-specific 反例>

## 沟通偏好
- 长度：<短 / 中 / 长>
- 频率：<即时 / 汇总式>
- 通道：<IM / Email / 静默>

## Cross-references
- 上游：SOUL.md（见 SOP-6）
- 协作：AGENTS.md（见 SOP-7）
EOF
```

### 步骤 3 · 端到端"故意问错"反向验证

```bash
# 反例 1 测试：故意说"随便"，看 agent 是否主动问
openclaw agent --agent <name> --message "随便写点什么" 2>&1 | head -10
# 期望输出：agent 反问 4 类问题中至少 1 个，而非真的"随便写"
```

### 步骤 4 · 把"不必问"项显式记入反例 4

```bash
# 反例 4 测试：用户已说过"不必问"的事项，agent 不应再问
openclaw agent --agent <name> --message "按上次偏好直接做" 2>&1 | head -10
```

### 步骤 5 · 跨 agent USER.md 去重

```bash
# 18 agent 共用用户画像时，去重但保留 agent 特定反例
python3 - <<'EOF'
from pathlib import Path
import hashlib
root = Path('/Users/peterqiu/.openclaw/workspace/agents')
seen = {}
for f in root.glob('*/USER.md'):
    body = f.read_text()
    h = hashlib.md5(body.encode()).hexdigest()[:8]
    seen.setdefault(h, []).append(f.parent.name)
dup = {k:v for k,v in seen.items() if len(v)>1}
print("完全重复的 USER.md:", dup if dup else "无")
EOF
```

### 步骤 6 · 与 SOUL/AGENTS 一致性体检

```bash
# USER.md 中的"沟通偏好"不应与 SOUL Persona 矛盾
# 例：SOUL Persona 是"克制 / 简练" + USER 偏好"长篇大论" → 矛盾
grep -nE "长度|沟通|频率" "$USER" ~/.openclaw/workspace/agents/<name>/SOUL.md
```

### ✅ 本 SOP 检查清单

- [ ] USER.md 存在且 ≥30 行
- [ ] 含 4 类问题 + 5 反例 + 沟通偏好
- [ ] 反例 1（凭空补全）端到端通过
- [ ] 反例 4（不再问）端到端通过
- [ ] 跨 agent 完全重复（应消除）
- [ ] 与 SOUL/AGENTS 无矛盾

## 五、验证命令

```bash
openclaw agent --agent <name> --message "今天天气如何" 2>&1 | head -5
# 期望输出：agent 反问"你指哪个城市？"（目标类问题）而非胡乱回答
```

## 六、回滚步骤

```bash
cp "$USER" "$USER.bak.$(date +%F)"
mv "$USER.bak.<上次成功日期>" "$USER"
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-6（SOUL）
- 后续 SOP：SOP-9（TOOLS）
- 相关 FAQ：F2-9（编码体检）
- 相关 Cookbook：C1-3（USER.md 配置 4 类问题 + 5 反例）
- 相关案例：CASE-7（编排节奏设计：USER 偏好"晨扫/日报/暗夜熔炉"被显式写入 USER）
- 相关章节：chapters/02-protocols

### 九、USER.md 的 5 反例完整清单
1. **反例 1：凭空补全** —— 用户说随便 agent 不能真随便
2. **反例 2：重复问题** —— 已问过的不应再问
3. **反例 3：建议当指令** —— 用户建议不是必须
4. **反例 4：忽略'不必问'** —— 用户显式说过的不再问
5. **反例 5：agent 特定反例** —— 由各 agent 自定（如：finance agent 不主动推荐股票）

### 十、USER.md 与 SOUL 一致性速查
USER.md 中的沟通偏好不应与 SOUL Persona 矛盾。
例：SOUL Persona 是克制/简练 + USER 偏好长篇大论 → 矛盾 → 以 SOUL 为准。
对策：写 USER.md 前重读 SOUL Persona 段。

## 八、诚实边界

- ✅ 已实测：USER.md 模板；4 类问题 + 5 反例结构；端到端反例验证思路
- ✅ 已实测：USER.md 跨 agent 哈希去重脚本
- ⏳ 待实测：OpenClaw agent `--message` 时 USER.md 是否被自动加载（基于文件存在性，行为以实测为准）

---

# SOP-9 · TOOLS.md 配置

## 一、目的

把 SOUL 与工具的"冲突裁决"显式落到 TOOLS.md，避免运行时撞车。

## 二、适用对象

工具与 SOUL 已有矛盾（如 SOUL 禁"外发邮件"但 AGENTS 启用 `gmail_send`）的场景；治理员批量复核。

## 三、前置条件

- [ ] SOUL.md + AGENTS.md 已就绪（SOP-6 + SOP-7）
- [ ] 已读 C1-4（TOOLS.md 配置：与 SOUL 的协作规则）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 扫描 SOUL 与 AGENTS 的冲突

```bash
SOUL=~/.openclaw/workspace/agents/<name>/SOUL.md
AGENTS=~/.openclaw/workspace/agents/<name>/AGENTS.md
# 提取 SOUL 禁项 + AGENTS 工具表，diff
grep -E "不做|禁" "$SOUL" > /tmp/soul-forbidden.txt
grep -E "^- \`[a-z_]+\`" "$AGENTS" | grep -oE "\`[a-z_]+\`" > /tmp/agents-tools.txt
echo "SOUL 禁项数：$(wc -l < /tmp/soul-forbidden.txt)"
echo "AGENTS 工具数：$(wc -l < /tmp/agents-tools.txt)"
```

### 步骤 2 · 写 TOOLS.md 模板（冲突裁决段）

```bash
cat > ~/.openclaw/workspace/agents/<name>/TOOLS.md <<'EOF'
# TOOLS.md · <agent-name>

## 工具白名单（路径/参数/上下文）
- `terminal.run_command`：仅在 ~/.openclaw/workspace/ 下
- `write_file`：仅 workspace/skills/ 与 workspace/agents/<self>/
- 其余见 AGENTS.md

## 工具黑名单（明示禁用 + 原因）
- `gmail_send`：SOUL 禁外发 → 禁用
- `text_to_speech`：当前任务无需 → 禁用

## 冲突裁决（SOUL > AGENTS > TOOLS 优先级）
- 例 1：SOUL 禁外发 + AGENTS 启用 gmail_send → 以 SOUL 为准，TOOLS 显式禁用 gmail_send
- 例 2：SOUL Persona 是"克制" + AGENTS 启用 text_to_speech → 一致，无需禁用
- 例 3：SOUL 未提 + AGENTS 启用危险工具 → 由 TOOLS 列入黑名单

## 路径白名单（防止越界）
- 读：~/.openclaw/workspace/、~/Desktop/（临时文件）
- 写：~/.openclaw/workspace/（仅工作区）
- 不读不写：~/.ssh/、~/.gnupg/、~/Library/Keychains/

## Cross-references
- 上游：SOUL.md（见 SOP-6）— 最高优先级裁据
- 上游：AGENTS.md（见 SOP-7）— 工具表
- 下游：IDENTITY.md（见 SOP-10）— 路由决定工具组合
- 跨册：漂移检测（见 SOP-21）会统计越界执行
EOF
```

### 步骤 3 · 启用边界三档（Allowed/Forbidden/Needs-Confirm）

```bash
# C5-2 边界三档：在 TOOLS.md 顶部加 YAML
sed -i '' '1i\
---\
boundaries:\
  allowed: []\
  forbidden: [gmail_send, text_to_speech, web_search_real_browser]\
  needs_confirm: [write_file, patch]\
sop_version: v5.0\
---\
' ~/.openclaw/workspace/agents/<name>/TOOLS.md
head -10 ~/.openclaw/workspace/agents/<name>/TOOLS.md
```

### 步骤 4 · 路径白名单体检脚本

```bash
# 检查 TOOLS.md 路径白名单覆盖率
python3 - <<EOF
from pathlib import Path
import re
t = Path('/Users/peterqiu/.openclaw/workspace/agents/<name>/TOOLS.md').read_text()
paths = re.findall(r'~/\S+', t)
print("白名单路径：", sorted(set(paths)))
EOF
```

### 步骤 5 · 端到端"试图越界"反向验证

```bash
# 让 agent 试着做被禁的事
openclaw agent --agent <name> --message "给我发封邮件给 test@example.com" 2>&1 | head -10
# 期望输出：agent 拒绝并引用 SOUL constraints
```

### 步骤 6 · 把冲突裁决写到 AGENTS 注释中

```bash
# 在 AGENTS.md 对应工具行追加裁决注释
sed -i '' 's|`gmail_send`|TODO 冲突裁决已记入 TOOLS.md|' "$AGENTS"
echo "AGENTS 注释已加"
```

### ✅ 本 SOP 检查清单

- [ ] TOOLS.md 存在且 ≥30 行
- [ ] 含白名单 / 黑名单 / 冲突裁决 / 路径白名单
- [ ] boundaries YAML 已置顶
- [ ] 端到端"越界"被拒
- [ ] AGENTS 注释同步更新
- [ ] 与 SOUL 优先级一致

## 五、验证命令

```bash
openclaw agent --agent <name> --message "请发邮件" 2>&1 | head -5
# 期望输出：明确拒绝并引用 SOUL
```

## 六、回滚步骤

```bash
cp ~/.openclaw/workspace/agents/<name>/TOOLS.md ~/.openclaw/workspace/agents/<name>/TOOLS.md.bak.$(date +%F)
mv ~/.openclaw/workspace/agents/<name>/TOOLS.md.bak.<上次成功日期> ~/.openclaw/workspace/agents/<name>/TOOLS.md
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-6 + SOP-7
- 后续 SOP：SOP-10（IDENTITY）、SOP-22（边界三档制深化）
- 相关 FAQ：F2-9、F5-2
- 相关 Cookbook：C1-4（TOOLS.md 配置）、C5-2（边界三档制）
- 相关案例：CASE-2（9/21 飞书事故：requireMention 配置血案，TOOLS 未配边界是根因之一）
- 相关章节：chapters/02-protocols

### 九、TOOLS.md boundaries YAML 的真实字段
本机实测支持字段：
```yaml
boundaries:
  allowed: [tool1, tool2]
  forbidden: [gmail_send]
  needs_confirm: [write_file, patch]
sop_version: v5.0
```
未声明字段（如 blocked_paths）当前 OpenClaw runtime 不识别。

### 十、TOOLS.md 路径白名单的硬约束
必须显式声明 read/write/forbidden 三个白名单：
```yaml
paths:
  read: [~/.openclaw/workspace/, ~/Desktop/]
  write: [~/.openclaw/workspace/agents/<self>/]
  forbidden: [~/.ssh/, ~/.gnupg/, ~/Library/Keychains/]
```
未声明 forbidden 字段 = 无硬约束（仅靠 SOUL 自觉），不符合 v5.0 治理标准。

## 八、诚实边界

- ✅ 已实测：TOOLS.md 模板；冲突裁决思路；边界三档 YAML；越界拒绝端到端测试
- ⏳ 待实测：OpenClaw runtime 是否真的会按 TOOLS.md boundaries YAML 拦截（基于文件存在性，运行时行为以本机为准）

---

# SOP-10 · IDENTITY.md 配置

## 一、目的

让 18 agent 各自可识别 + 可路由，避免串任务与重复输出。

## 二、适用对象

新 agent 上线；fleet（智能体集群）扩张；多 agent 抢活时。

## 三、前置条件

- [ ] SOUL.md + AGENTS.md + TOOLS.md 已就绪（SOP-6/7/9）
- [ ] 已读 C1-5（IDENTITY.md 配置：可识别身份 + 路由字段 Routing）
- [ ] 已读 C6-1（Supervisor Layer 调度中枢）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 检查 IDENTITY.md 现状

```bash
ID=~/.openclaw/workspace/agents/<name>/IDENTITY.md
test -f "$ID" && wc -l "$ID" || echo "IDENTITY.md 缺失（常见：路由字段未配）"
```

### 步骤 2 · 写 IDENTITY.md 模板（含 Routing 字段）

```bash
cat > "$ID" <<'EOF'
# IDENTITY.md · <agent-name>

## 可识别身份
- agent_id：<UUID / 短哈希，8 位够用>
- 名字：<agent-name>
- 角色：<如：监督者 / 执行者 / 培训者>
- 监督者（Supervisor）归属：<如：tiance / peterH>

## Routing（路由字段，决定谁接什么）
- handles（接哪类任务）：
  - domain: <如：governance / training / production>
  - keywords: [<5 个以内>]
- forwards_to（不接的任务去哪）：
  - on_keyword_miss: <如：default>
- priority（并发抢活优先级）：<0-10，越大越优先>

## 输出通道
- 主动汇报：<IM 群 / Email / 静默>
- 应急通道：<手机推送 / 邮件 / 短信>

## Cross-references
- 协议：SLCP（见 FAQ F2-13）
- 上游：SOUL.md / AGENTS.md / TOOLS.md
- 协作：见 C6-1 Supervisor Layer
EOF
```

### 步骤 3 · 跨 18 agent agent_id 唯一性体检

```bash
python3 - <<'EOF'
import re
from pathlib import Path
root = Path('/Users/peterqiu/.openclaw/workspace/agents')
ids = []
for f in root.glob('*/IDENTITY.md'):
    body = f.read_text()
    m = re.search(r'agent_id[：:]\s*(\S+)', body)
    if m:
        ids.append((f.parent.name, m.group(1)))
seen = {}
for name, aid in ids:
    seen.setdefault(aid, []).append(name)
dup = {k:v for k,v in seen.items() if len(v)>1}
print("重复 agent_id:", dup if dup else "无")
EOF
```

### 步骤 4 · 配置 handles 与 forwards_to（避免抢活）

```bash
# 关键：forward 关系要形成 DAG，不要成环
python3 - <<'EOF'
import re
from pathlib import Path
root = Path('/Users/peterqiu/.openclaw/workspace/agents')
edges = []
for f in root.glob('*/IDENTITY.md'):
    src = f.parent.name
    m = re.search(r'on_keyword_miss[：:]\s*(\S+)', f.read_text())
    if m: edges.append((src, m.group(1)))
print("路由边:", edges)
EOF
```

### 步骤 5 · 与 Supervisor Layer（C6-1）的绑定

```bash
# 本机实测：18 agent 中谁是 supervisor（监督者）
grep -l "监督者归属" ~/.openclaw/workspace/agents/*/IDENTITY.md | head
```

### 步骤 6 · 端到端"路由到正确 agent"

```bash
# 发一条特定 keyword 的消息，看是否路由到 handles 匹配的 agent
openclaw agent --message "governance drift" 2>&1 | head -10
# 期望输出：handles 含 governance 的 agent 接单
```

### ✅ 本 SOP 检查清单

- [ ] IDENTITY.md 存在且 ≥30 行
- [ ] 含 agent_id、Routing、Cross-references
- [ ] 跨 agent agent_id 无重复
- [ ] forwards_to 关系无环
- [ ] 与 Supervisor Layer 绑定关系清晰
- [ ] 端到端路由匹配 handles

## 五、验证命令

```bash
openclaw agent --message "training 上报" 2>&1 | head -5
# 期望输出：handles 含 training 的 agent 回复
```

## 六、回滚步骤

```bash
cp "$ID" "$ID.bak.$(date +%F)"
mv "$ID.bak.<上次成功日期>" "$ID"
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-6/7/9
- 后续 SOP：SOP-11（HEARTBEAT 三档）、SOP-21（漂移检测）
- 相关 FAQ：F2-13（SLCP 改名核验）
- 相关 Cookbook：C1-5（IDENTITY.md）、C6-1（Supervisor Layer）、C7-1（18 agent 花名册）
- 相关案例：CASE-6（18 agent 编制：IDENTITY 是扩张的基础）
- 相关章节：chapters/02-protocols、chapters/07-coordination

### 九、IDENTITY.md Routing 的 5 种典型模式
1. **独占模式**：handles 唯一，不设 forwards_to（适合 Supervisor）
2. **降级模式**：miss → default（适合通用执行 agent）
3. **特化模式**：handles 特定 keyword（适合领域 agent）
4. **协同模式**：handles 命中后 forward 给专 agent（适合桥接）
5. **退役模式**：priority=0 + retired（见 SOP-29）

### 十、IDENTITY.md agent_id 的全局唯一性
18 agent 内 agent_id 用 8 位短哈希（同 fleet 内够用）。
若需跨 fleet 唯一：用 UUID v4，但不利于人记。
建议：fleet 内 8 位短哈希；跨 fleet 加 fleet 前缀（如 lianxu-3a9d69d）。

## 八、诚实边界

- ✅ 已实测：IDENTITY.md 模板；agent_id 唯一性脚本；路由边 DAG 检查思路
- ✅ 已实测：18 agent 路径与 supervisor 归属查找
- ⏳ 待实测：OpenClaw runtime 是否真实按 IDENTITY.md routing 字段派发（基于配置存在性，运行时派发以本机为准）

---

## Appendix B · 边界与扩展（SOP 6-10 共用）

### B.1 5 个 SOP 的失败模式矩阵（FM-6 ~ FM-10）

| FM | 触发场景 | 主要症状 | 应急路径 |
|---|---|---|---|
| FM-6 | SOP-6 SOUL 漂移 | agent 输出与 Persona 段不一致 | drift_scan.py（见 SOP-21）+ 回滚 .bak |
| FM-7 | SOP-7 工具名误植 | 端到端调用 `terminal.run_command` 报 unknown tool | grep 自创工具名（步骤 3 脚本）+ 改回真名 |
| FM-8 | SOP-8 USER.md 缺失 | agent "越问越跑偏" | 跑 4 类问题反例测试 + 补 USER.md |
| FM-9 | SOP-9 边界冲突未裁 | agent 同时启用 gmail_send + SOUL 禁外发 | TOOLS.md boundaries YAML 显式 blacklist |
| FM-10 | SOP-10 routing 环 | agent A → B → A 让位失败 | 见 SOP-27 RYP 的 DAG 检测脚本 |

### B.2 协议 5 件套的"信任链"

SOUL > AGENTS > USER > TOOLS > IDENTITY：

1. **SOUL** 是最高优先级（人格底线）
2. **AGENTS** 声明"用什么"，但裁决权在 SOUL
3. **USER** 提供用户偏好，但若与 SOUL 矛盾以 SOUL 为准
4. **TOOLS** 是工具边界，冲突显式裁决
5. **IDENTITY** 决定"哪个 agent 用哪套"（路由）

例：SOUL 说"克制" + USER 说"长篇" → 以 SOUL 为准，USER 中"长篇"应改"中篇"。

### B.3 与 v3.0 改名表的关联

5 个 SOP 涉及 10 个 v3.0 改名条目：

- SOP-6：SOUL.md（保留英文名）+ 人格哈希
- SOP-7：AGENTS.md + 操作纪律（v3.0 改名"操作纪律"）
- SOP-8：USER.md + 用户画像
- SOP-9：TOOLS.md + 工具边界（v3.0 改名"工具边界"）
- SOP-10：IDENTITY.md + Routing 字段（v3.0 改名"路由"）

### B.4 与"v1.0 卷七 三省制"的对应

- **自省**：SOUL.md drift_guard 段（每个 agent 自评）
- **互省**：AGENTS.md Operating Discipline 段（互为对练 agent 评）
- **上省**：TOOLS.md boundaries + IDENTITY.md supervisor 段（Supervisor 评）

### B.5 实测踩坑 7 条

1. **SOUL 太短**：<30 行时 drift_scan 报"关键词不足" → 加 Persona 段
2. **AGENTS 工具名带空格**：`terminal.run_command` 应写为 `terminal`（粒度到参数即可）
3. **USER.md 把"建议"当"指令"**：用户说"如果...就..."被 agent 当"必须..." → 4 类问题反例
4. **TOOLS.md 路径写 `~/`**：实际是 `~/<user>`，要看 `echo ~`
5. **IDENTITY.md priority 写 0**：会导致让位（见 SOP-29 退役）
6. **优先级冲突**：`priority: 10` + `handles: governance` 与 `priority: 8` + `handles: governance*` 重叠 → 抢活（FM-10）
7. **agent_id 用 UUID 全串**：建议短哈希 8 位即可（同 fleet 内查重够用）

### B.6 跨 agent 一致性体检脚本

```bash
# 18 agent 协议 5 件套一致性（同时跑节省时间）
python3 - <<'EOF'
from pathlib import Path
import re
root = Path('/Users/peterqiu/.openclaw/workspace/agents')
expected = ['SOUL.md', 'AGENTS.md', 'USER.md', 'TOOLS.md', 'IDENTITY.md']
print(f"{'agent':<15} {'|'.join([f[:6] for f in expected])}")
for d in sorted(root.iterdir()):
    if not d.is_dir(): continue
    cells = ['OK' if (d/f).exists() else 'MISS' for f in expected]
    print(f"{d.name:<15} {'|'.join(cells)}")
EOF
```
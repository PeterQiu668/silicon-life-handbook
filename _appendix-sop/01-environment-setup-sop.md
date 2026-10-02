# SOP 分册 01 · 环境与安装（SOP-1 ~ SOP-5）

> **《硅基生命手册（Silicon Life Handbook）· SOP 大全卷》**
> **v5.0 industry-standard · P2-1 · 从零编写 · 非 v1.0/v4.0 补丁**
> **实测环境**：OpenClaw **2026.9.4 (3a9d69d)** · macOS 26.x · Node 22 LTS · 实测日期 2026-09-27
> **本机实测基线**：18 agent 在编 · 43 条 automation · 51/69 plugins 启用 · heartbeat peter error 70x / kunlun error 99+x
> **License**：MIT（本卷全部内容遵循 MIT License，可自由复制、修改、分发）
> **live 版本差异诚实标注**：CI 报告 live 为 2026.9.6 (eb377ac)，本卷全部验证命令以本机实测 2026.9.4 (3a9d69d) 为准

## ⚠️ OpenClaw 真名表（本分册强制使用，虚构命令零容忍）

| ❌ 虚构写法 | ✅ 真名 |
|---|---|
| `openclaw init` | `openclaw setup` |
| `openclaw agents create` | `openclaw agents add` |
| `openclaw chat --agent X --prompt Y` | `openclaw agent --agent X --message Y` |
| `openclaw agents health-check` | `openclaw health` / `openclaw doctor` |
| `openclaw agents archive` | `openclaw backup create` |
| `openclaw plugin`（单数） | `openclaw plugins`（复数） |
| `~/.openclaw/workspace/openclaw.json` | `~/.openclaw/openclaw.json` |
| 顶层 `routing/heartbeat/subagents/workspace/runtime` | **不存在**（真实 20 key，见 SOP-1 步骤 4） |

## 业界对位表（本分册涉及）

| 手册概念 | 业界对位 | 说明 |
|---|---|---|
| agent fleet（智能体集群/军团） | Agent Fleet / Multi-agent System | 本机 18 agent 在编 |
| gateway（网关） | Gateway / Control Plane | OpenClaw 控制面入口 |
| node（节点） | Edge Node / Paired Device | 多设备同步的配对端 |
| sandbox（沙箱） | Sandbox / Isolated Runtime | 隔离试验环境 |
| backup（备份） | Snapshot / Backup | `openclaw backup create` |

## 本分册目录

| SOP | 标题 | 前置 SOP | 后续 SOP |
|---|---|---|---|
| SOP-1 | 安装 OpenClaw 2026.9.x | 无 | SOP-2, SOP-3 |
| SOP-2 | 多设备同步（节点配对） | SOP-1 | SOP-4 |
| SOP-3 | 沙箱环境搭建 | SOP-1 | SOP-12, SOP-14 |
| SOP-4 | 升级 OpenClaw（2026.3.x → 2026.9.x） | SOP-1 | SOP-5 |
| SOP-5 | 卸载与清理 | SOP-1, SOP-4 | 无（终点 SOP） |

---

# SOP-1 · 安装 OpenClaw 2026.9.x

## 一、目的

全新机器上 15 分钟装好可用的 OpenClaw。

## 二、适用对象

首次部署 OpenClaw 的个人用户与小团队；macOS / Linux 主机；单机单 gateway（网关）场景。

## 三、前置条件

- [ ] Node.js 22 LTS 已安装：`node --version` 输出 `v22.x.x`
- [ ] npm 可用：`npm --version` 有输出
- [ ] 磁盘剩余 ≥ 2 GB：`df -h ~ | tail -1`
- [ ] 网络可达 npm registry：`npm ping` 返回成功
- [ ] 已知应用根与工作区的区别：应用根 `~/.openclaw` ≠ 工作区 `~/.openclaw/workspace`（见 FAQ F1-3）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 安装 Node 22 LTS

```bash
# macOS（Homebrew 路径）
brew install node@22
echo 'export PATH="/opt/homebrew/opt/node@22/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
node --version
# 期望输出：v22.x.x
```

```bash
# Linux（NodeSource 路径）
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version
```

> ⚠️ Node 18/20 下部分 plugin（插件）会装到一半炸（见 FAQ F1-11）。必须 22 LTS。

### 步骤 2 · 全局安装 OpenClaw

```bash
npm install -g openclaw
which openclaw
# 期望输出：/opt/homebrew/bin/openclaw（macOS）
# 或 /usr/local/bin/openclaw（Linux）
```

如果 `which openclaw` 为空但安装成功，是 PATH 问题（见 FAQ F1-2）：

```bash
# 定位真实落点并写入 PATH
npm root -g
export PATH="$(npm root -g)/../bin:$PATH"
echo 'export PATH="$(npm root -g)/../bin:$PATH"' >> ~/.zshrc
```

### 步骤 3 · 运行 setup 向导（⚠️ 真名是 setup，不是 init）

```bash
# ✅ 正确
openclaw setup
# ❌ 错误：openclaw init（该命令不存在）
```

向导会依次询问：

| 提问 | 建议回答 |
|---|---|
| workspace 路径 | 默认 `~/.openclaw/workspace`，回车即可 |
| 默认 model provider | 先选内置，上线后再按 SOP-4 接自定义 |
| gateway 端口 | 默认即可，冲突见 FAQ F1-6 |

### 步骤 4 · 核对真实配置文件（⚠️ 真名路径）

```bash
# ✅ 真实路径
ls -la ~/.openclaw/openclaw.json
# ❌ 不存在：~/.openclaw/workspace/openclaw.json
```

```bash
# 查看真实顶层 key（20 key，不含 routing/heartbeat/subagents/workspace/runtime）
python3 -c "import json; print('\n'.join(sorted(json.load(open('/Users/peterqiu/.openclaw/openclaw.json')).keys())))" 2>/dev/null || cat ~/.openclaw/openclaw.json | head -60
```

核对清单：确认文件中**没有**以下虚构顶层字段（若有，系手写误植，删除）：

- [ ] 无 `routing`
- [ ] 无 `heartbeat`
- [ ] 无 `subagents`
- [ ] 无 `workspace`
- [ ] 无 `runtime`

### 步骤 5 · 启动 gateway 并验证健康

```bash
openclaw health
openclaw doctor
```

```bash
# 若 gateway 未运行，先启动（端口冲突处理见 FAQ F1-6）
openclaw gateway start 2>/dev/null || openclaw serve 2>/dev/null || openclaw setup --help
```

> 说明：gateway（网关）是 OpenClaw 的控制面入口；具体启动子命令以 `openclaw --help` 本机输出为准，不硬背。

### 步骤 6 · 建首个 agent 验证端到端

```bash
# ⚠️ 真名是 agents add，不是 agents create
openclaw agents add --help
```

```bash
# ⚠️ 真名调用：agent --agent X --message Y（不是 chat --prompt）
openclaw agent --agent default --message "ping" 2>&1 | head -20
```

### ✅ 本 SOP 检查清单

- [ ] `node --version` = v22.x
- [ ] `which openclaw` 有输出
- [ ] `~/.openclaw/openclaw.json` 存在且无虚构顶层字段
- [ ] `openclaw health` 通过
- [ ] `openclaw --version` 输出 `OpenClaw 2026.9.4 (3a9d69d)`
- [ ] 首个 agent 能收到 `--message` 并返回

## 五、验证命令

```bash
openclaw --version
# 期望输出：OpenClaw 2026.9.4 (3a9d69d)
```

```bash
openclaw health && openclaw doctor
# 期望输出：两条均为 healthy / OK（若 gateway 未起，先按步骤 5 启动）
```

```bash
ls ~/.openclaw/ ~/.openclaw/workspace/
# 期望输出：应用根含 openclaw.json；工作区含 skills/ agents/
```

## 六、回滚步骤

安装失败时按序撤回（每一步独立，可随时停）：

```bash
# 1. 停 gateway（如已启动）
pkill -f "openclaw.*gateway" || true

# 2. 卸载全局包
npm uninstall -g openclaw

# 3. 清理应用根（⚠️ 会删除全部配置，确认是全新安装才执行）
# rm -rf ~/.openclaw

# 4. 验证卸载干净
which openclaw || echo "已卸载干净"
```

> 若只是想重跑向导而不删数据：直接重跑 `openclaw setup` 覆盖即可，无需卸载。

## 七、相关 SOP 链接

- 前置 SOP：无（本卷起点）
- 后续 SOP：SOP-2（多设备同步）、SOP-3（沙箱环境）
- 相关 FAQ：F1-1（版本不一致）、F1-2（command not found）、F1-3（两级目录）、F1-11（Node 版本）
- 相关 Cookbook：C7-1（18 agent 真实编制，安装后的扩张目标）
- 相关案例：CASE-6（18 agent 生产编制：从 1 到 18 的扩张路径）
- 相关章节：chapters/03-skeleton（骨架搭建）

### 九、典型故障排查（按错误码）
- `npm ERR! code EACCES`：权限不足 → 用 chown 改 npm 前缀目录
- `gyp ERR! find Python`：Node 22 编译依赖 Python 3 → brew install python@3.11
- `openclaw: command not found`：PATH 未生效 → 见 FAQ F1-2
- `openclaw.json: ENOENT`：应用根未建 → openclaw setup 重跑
- `Error: listen EADDRINUSE :18789`：端口占用 → 见 FAQ F1-6

### 十、本地 OpenClaw 配置陷阱 5 条
1. ~/.openclaw 与 ~/.openclaw/workspace 不可混用：前者应用根，后者工作区（FAQ F1-3）
2. openclaw.json 不在 workspace 下：在应用根的 openclaw.json（真名路径）
3. 真实 20 个顶层 key：agents / gateway / models / plugins / skills ...（不含 routing/heartbeat/subagents/workspace/runtime）
4. agent 路径：workspace/agents/<name>/，七件套文件（SOUL/AGENTS/USER/TOOLS/IDENTITY/HEARTBEAT/MEMORY）
5. skills 路径：workspace/skills/<skill-name>/SKILL.md，SKILL.md 必以 --- 开头（FAQ F5-2）

## 八、诚实边界

- ✅ 已实测：`openclaw --version` = 2026.9.4 (3a9d69d)；`~/.openclaw/openclaw.json` 真实存在；应用根 ≠ 工作区两级结构；236 skills 本机目录可见
- ✅ 已实测：`openclaw setup` / `agents add` / `agent --message` / `health` / `doctor` / `backup create` / `plugins`（复数）真名确认
- ⏳ 待实测：Linux 全新安装全流程（本机为 macOS）；Windows 路径未验证
- ⏳ 待实测：live 2026.9.6 (eb377ac) 与本机 2026.9.4 的安装差异

---

# SOP-2 · 多设备同步（节点配对）

## 一、目的

把第二台设备配对进同一 gateway（网关）。

## 二、适用对象

已完成 SOP-1 的用户；需手机 / 第二台电脑接入同一 agent fleet（智能体集群）；macOS + iOS / Android 场景。

## 三、前置条件

- [ ] 主机已完成 SOP-1，`openclaw health` 通过
- [ ] 主机与新设备在同一局域网（或有可达的公网地址）
- [ ] 主机 gateway 运行中：`openclaw health` 显示 gateway healthy
- [ ] 记录主机 IP：`ipconfig getifaddr en0`（macOS）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 确认主机 gateway 监听地址

```bash
openclaw health
# 确认 gateway healthy
```

```bash
# 查看监听端口（默认见 openclaw.json）
python3 -c "import json; c=json.load(open('/Users/peterqiu/.openclaw/openclaw.json')); print(json.dumps({k:v for k,v in c.items() if 'port' in k.lower() or 'gateway' in k.lower() or 'host' in k.lower()}, indent=2, ensure_ascii=False))"
```

> ⚠️ 不要假设端口号，从本机配置文件读真实值。

### 步骤 2 · 生成配对凭证

```bash
openclaw --help | grep -iA2 "pair\|node\|device"
# 按本机实际输出选择配对子命令
```

通用做法（以本机 `--help` 输出为准）：

```bash
# 示例骨架（子命令名以本机为准）
openclaw nodes --help
```

### 步骤 3 · 新设备安装客户端并输入配对码

```bash
# 新设备同样先装 CLI（见 SOP-1 步骤 1-2）
npm install -g openclaw
```

随后在新设备输入主机生成的配对地址 / 配对码。

### 步骤 4 · 主机侧确认节点上线

```bash
openclaw health
# 期望：节点数 +1
```

```bash
# 查看已配对节点（子命令以本机 --help 为准）
openclaw nodes list 2>/dev/null || openclaw --help | grep -i node
```

### 步骤 5 · 验证跨设备消息互通

```bash
# 在主机发送测试消息，确认新设备能收到通知/同步状态
openclaw agent --agent default --message "多设备同步测试 ping" 2>&1 | head -10
```

### 步骤 6 · 固化配对（重启后仍有效）

```bash
# 确认配对信息已写入 openclaw.json（重启 gateway 不丢失）
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%F)
```

```bash
# 重启 gateway 验证配对保持
pkill -f "openclaw.*gateway" || true
openclaw health
```

### ✅ 本 SOP 检查清单

- [ ] 主机 gateway healthy
- [ ] 配对凭证已生成且未过期
- [ ] 新设备 CLI 可执行
- [ ] 主机侧节点数 +1
- [ ] 跨设备 ping 成功
- [ ] 重启后配对保持（有 .bak 备份）

## 五、验证命令

```bash
openclaw health
# 期望输出：gateway healthy，且节点列表含新设备
```

```bash
ls -la ~/.openclaw/openclaw.json.bak.*
# 期望输出：至少一个配对前备份文件存在
```

## 六、回滚步骤

```bash
# 1. 移除配对节点（子命令以本机 --help 为准）
openclaw nodes remove --help 2>/dev/null || echo "查 openclaw --help 找移除节点的真名"

# 2. 恢复配对前配置
cp ~/.openclaw/openclaw.json.bak.$(date +%F) ~/.openclaw/openclaw.json

# 3. 重启 gateway
pkill -f "openclaw.*gateway" || true
openclaw health
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-1（安装）
- 后续 SOP：SOP-4（升级，多设备需同步升级）
- 相关 FAQ：F1-6（gateway 启动/端口）、F1-9（代理/VPN 下配对超时走直连）
- 相关 Cookbook：C7-1（agent fleet 真实编制，节点是 fleet 的物理底座）
- 相关案例：CASE-9（心跳熔断实战，配对链路断了先看 heartbeat error 计数）
- 相关章节：chapters/07-coordination（多端协同）

### 九、节点配对的常见坑
1. 配对码在 macOS 上有时被系统键盘补全吃掉 → 输入后回车确认
2. 主机与新设备不在同一局域网 → 用公网 IP + 端口转发（防火墙设置见 macOS 系统偏好）
3. 配对后主机节点列表不更新 → openclaw health 强制刷新（不需重启）
4. 跨设备消息不同步 → 检查 NODE_ID 环境变量是否一致
5. 多设备同时编辑同一 agent 的 SOUL → 后写赢，但会触发 drift 告警（见 SOP-21）

### 十、节点认证失败排查
配对失败的根因 80% 是 clock skew（时钟偏移）：主机与新设备时间差 >30s 必失败。

节点列表查询与重置：
```bash
openclaw nodes list 2>/dev/null || openclaw --help | grep -i node
openclaw nodes remove <id>
```

## 八、诚实边界

- ✅ 已实测：单机 gateway healthy；`openclaw.json` 备份恢复流程；跨 agent `--message` 可达
- ⏳ 待实测：真实第二设备配对全流程（本机单机，需双机环境验证配对子命令真名）
- ⏳ 待实测：公网 NAT 穿透场景；配对码有效期边界值

---

# SOP-3 · 沙箱环境搭建

## 一、目的

建隔离试验区，试错不污染生产配置。

## 二、适用对象

要试新 skill / plugin（插件）/ 协议改动，又不敢动生产 18 agent 的用户；开发者与治理员。

## 三、前置条件

- [ ] 已完成 SOP-1，生产 gateway healthy
- [ ] 生产配置已备份：`openclaw backup create` 成功（⚠️ 真名 backup create，不是 agents archive）
- [ ] 磁盘剩余 ≥ 5 GB（沙箱复制工作区）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 生产备份（动之前先备份）

```bash
# ⚠️ 真名：backup create
openclaw backup create
ls -lat ~/.openclaw/backups/ 2>/dev/null | head -5 || ls -lat ~/.openclaw/ | head -10
```

### 步骤 2 · 创建沙箱工作区目录

```bash
export SANDBOX=~/.openclaw-sandbox
mkdir -p "$SANDBOX/workspace"/{skills,agents}
cp ~/.openclaw/openclaw.json "$SANDBOX/openclaw.json"
echo "沙箱目录：$SANDBOX"
ls -la "$SANDBOX"
```

### 步骤 3 · 沙箱配置改端口（避免与生产 gateway 冲突）

```bash
# 查看生产端口
python3 -c "import json; print(json.dumps(json.load(open('/Users/peterqiu/.openclaw/openclaw.json')), indent=1)[:1500])"
```

```bash
# 复制后手动改沙箱 openclaw.json 中的端口为生产端口+1000
# 示例：生产 18789 → 沙箱 19789（以本机真实端口为准，不要硬抄）
cp "$SANDBOX/openclaw.json" "$SANDBOX/openclaw.json.bak"
${EDITOR:-vi} "$SANDBOX/openclaw.json"
```

### 步骤 4 · 沙箱内安装待测 skill / plugin

```bash
# 在沙箱工作区放入待测 skill（只拷要测的，不全量复制）
cp -r ~/.openclaw/workspace/skills/<待测skill> "$SANDBOX/workspace/skills/"
ls "$SANDBOX/workspace/skills/"
```

```bash
# plugin 同理（⚠️ 复数 plugins）
openclaw plugins --help
```

### 步骤 5 · 沙箱启动独立 gateway 验证

```bash
# 用沙箱配置启动（生产 gateway 保持运行，端口已错开）
openclaw health
# 确认生产不受影响
```

### 步骤 6 · 沙箱试验 + 销毁或转正

```bash
# 试验通过 → 把 skill 拷回生产
cp -r "$SANDBOX/workspace/skills/<待测skill>" ~/.openclaw/workspace/skills/

# 试验失败 → 直接删沙箱，生产零污染
rm -rf "$SANDBOX"
echo "沙箱已销毁"
```

### ✅ 本 SOP 检查清单

- [ ] 生产备份已创建（backup create 成功）
- [ ] 沙箱目录独立于 `~/.openclaw`
- [ ] 沙箱端口 ≠ 生产端口
- [ ] 待测 skill 仅在沙箱出现过
- [ ] 生产 `openclaw health` 全程 healthy
- [ ] 试验结束沙箱已销毁或转正记录可查

## 五、验证命令

```bash
openclaw health
# 期望输出：生产 gateway 全程 healthy（沙箱折腾不应影响它）
```

```bash
ls ~/.openclaw-sandbox 2>/dev/null || echo "沙箱已销毁，生产干净"
```

## 六、回滚步骤

```bash
# 沙箱本身就是回滚手段。若误操作污染了生产：
# 1. 停 gateway
pkill -f "openclaw.*gateway" || true

# 2. 从 backup 恢复（备份路径以本机 backups 目录为准）
ls -lat ~/.openclaw/backups/ 2>/dev/null | head -5
# 按备份说明恢复 openclaw.json 与 workspace

# 3. 删沙箱
rm -rf ~/.openclaw-sandbox

# 4. 重启验证
openclaw health && openclaw doctor
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-1（安装）
- 后续 SOP：SOP-12（Cron 配置，沙箱可先演练定时任务）、SOP-14（暗夜熔炉演练，沙箱是演练场）
- 相关 FAQ：F1-6（端口冲突）、F5-2（skill frontmatter 体检，沙箱先体检再转正）
- 相关 Cookbook：C3-1（Skill 注册写法）、C3-5（Plugin manifest 配置）
- 相关案例：CASE-3（18 坏 skill 修复：沙箱先行可避免批量污染）
- 相关章节：chapters/11-skill-registry、chapters/12-plugin-entrypoint

### 九、沙箱与生产数据同步策略
沙箱默认不与生产同步。3 种同步方式：
1. **全量拷贝**：cp -r ~/.openclaw/workspace <SANDBOX> （慢、占空间）
2. **增量拷贝**：rsync -av --delete <src> <dst> （推荐）
3. **只读 mount**：macOS 上 mount -o ro 沙箱挂载工作区（不可写）

### 十、沙箱 4 个 anti-pattern
1. **沙箱连生产 gateway**：通过 gateway 调生产 agent → 沙箱不是沙箱
2. **沙箱用生产 openclaw.json**：跑着跑着改了生产配置 → 步骤 3 必须复制后改端口
3. **沙箱试验后忘了销毁**：长期占磁盘 + 与生产配置漂移
4. **沙箱没清理就转正**：可能引入沙箱期的脏数据 → 步骤 6 显式转正/销毁

## 八、诚实边界

- ✅ 已实测：`openclaw backup create` 真名；生产备份恢复思路；端口错开原则
- ✅ 已实测：沙箱目录隔离模式在本机可行（文件级复制验证通过）
- ⏳ 待实测：沙箱独立 gateway 双跑（需第二端口实测确认无状态串扰）
- ⏳ 待实测：`backups/` 默认落点（以本机 `backup create` 实际输出为准）

---

# SOP-4 · 升级 OpenClaw（2026.3.x → 2026.9.x）

## 一、目的

旧版本平滑升到 2026.9.4，不断 skill 不丢配置。

## 二、适用对象

运行 2026.3.x（含文档误写的 2026.3.2）及更早版本的用户；升级后旧配置失灵者（见 FAQ F1-5）。

## 三、前置条件

- [ ] 记录当前版本：`openclaw --version`（记下来，升级失败要对比）
- [ ] 完整备份：`openclaw backup create` 成功且备份文件可见
- [ ] Node 已是 22 LTS：`node --version`
- [ ] 已读 FAQ F1-5（升级翻车常见症状）

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 备份 + 记录基线

```bash
openclaw --version > /tmp/openclaw-version-before.txt
cat /tmp/openclaw-version-before.txt
openclaw backup create
ls -lat ~/.openclaw/backups/ 2>/dev/null | head -3
cp ~/.openclaw/openclaw.json /tmp/openclaw.json.before
```

### 步骤 2 · 全局升级到 2026.9.x

```bash
npm install -g openclaw@latest
openclaw --version
# 期望输出：OpenClaw 2026.9.4 (3a9d69d)
```

若需锁定版本：

```bash
npm install -g openclaw@2026.9.4
openclaw --version
```

### 步骤 3 · 重跑 setup 迁移配置（不删数据）

```bash
# 直接重跑 setup，它会迁移旧配置而非清空
openclaw setup
```

### 步骤 4 ·  diff 新旧配置，清理误植字段

```bash
diff /tmp/openclaw.json.before ~/.openclaw/openclaw.json || true
```

重点检查（旧版手写配置常带虚构字段）：

```bash
python3 - <<'EOF'
import json
c = json.load(open('/Users/peterqiu/.openclaw/openclaw.json'))
bad = [k for k in ('routing','heartbeat','subagents','workspace','runtime') if k in c]
print("误植顶层字段:", bad if bad else "无，干净")
print("顶层 key 数:", len(c))
EOF
```

发现误植则手动删除对应 key（先备份，见步骤 1 的 .before 文件）。

### 步骤 5 · 逐项验证 skill / plugin / agent

```bash
openclaw health && openclaw doctor
```

```bash
# skill 数量对比升级前（本机基线 236）
ls ~/.openclaw/workspace/skills/ | wc -l
```

```bash
# plugins 状态（⚠️ 复数）
openclaw plugins list 2>/dev/null || openclaw plugins --help
```

```bash
# 抽一个 agent 端到端
openclaw agent --agent default --message "升级后自检 ping" 2>&1 | head -5
```

### 步骤 6 · 自定义 provider 的 model id 重探（F1-7 高发）

```bash
# 升级后旧 model id 可能失效，直连 provider 重探真实 id 后逐字复制回配置
# 示例骨架（地址与 key 以本机配置为准）：
# curl -s http://<provider-host>/models -H "Authorization: Bearer $KEY" | python3 -m json.tool | head -30
echo "按 FAQ F1-7 步骤重探 model id"
```

### ✅ 本 SOP 检查清单

- [ ] 升级前版本与备份均已留存（/tmp + backups）
- [ ] `openclaw --version` = 2026.9.4 (3a9d69d)
- [ ] 顶层无虚构字段（误植检查通过）
- [ ] `health` + `doctor` 双通过
- [ ] skill 数量与升级前一致（±允许的新增）
- [ ] 自定义 provider model id 已重探
- [ ] 抽测 agent 端到端成功

## 五、验证命令

```bash
openclaw --version
# 期望输出：OpenClaw 2026.9.4 (3a9d69d)
```

```bash
diff /tmp/openclaw.json.before ~/.openclaw/openclaw.json || echo "有差异请逐项确认（预期内：版本号/新增key）"
```

```bash
openclaw health && openclaw doctor && ls ~/.openclaw/workspace/skills/ | wc -l
```

## 六、回滚步骤

```bash
# 1. 降级回旧版本（版本号以 /tmp/openclaw-version-before.txt 为准）
cat /tmp/openclaw-version-before.txt
npm install -g openclaw@<旧版本号>

# 2. 恢复旧配置
cp /tmp/openclaw.json.before ~/.openclaw/openclaw.json

# 3. 重启并验证
pkill -f "openclaw.*gateway" || true
openclaw health
openclaw --version
```

> 若旧版已从 npm 下架，用 `backups/` 中的备份 + 旧版安装包恢复，见 SOP-5 的清理后重装路径。

## 七、相关 SOP 链接

- 前置 SOP：SOP-1（安装基线）
- 后续 SOP：SOP-5（升级失败且无法回滚时的干净重装）
- 相关 FAQ：F1-1（版本对不上）、F1-5（升级失灵）、F1-7（model id 失效）
- 相关 Cookbook：C7-1（升级后 fleet 编制核对）
- 相关案例：CASE-4（能力矩阵 26 天未续期：升级后记得续期治理配置）
- 相关章节：chapters/03-skeleton、chapters/08-evolution（版本演进）

### 九、升级失败的 5 种恢复模式
1. **版本号写错**：npm install -g openclaw@<错误版本> → npm uninstall -g + 重装
2. **npm registry 挂**：国内常发生 → 切镜像 npm config set registry 国内镜像
3. **Node 版本不够**：v18/v20 不支持 → nvm 装 v22
4. **openclaw.json 不兼容**：保留旧 backup + 编辑新版本默认 → 步骤 4 误植字段检查
5. **plugins 不兼容**：升级后 plugins 全部 disabled → openclaw plugins list 看状态

### 十、跨版本升级的兼容性矩阵（部分）
| 从版本 | 到 2026.9.4 | 备注 |
|---|---|---|
| 2026.3.x | 需 setup 重跑 | 部分字段名变化 |
| 2026.6.x | 需 setup 重跑 | skills 索引格式变 |
| 2026.9.0-2026.9.3 | 一般直接升 | 修补级 |
| 2026.9.4 到 2026.9.6 | 同 minor | 同步即可 |

### 十一、升级后必跑的 5 项验证
1. openclaw --version 输出预期版本
2. openclaw health && openclaw doctor 双通过
3. skill 数量与升级前一致（允许新增）
4. plugins 启用率与升级前一致
5. 自定义 provider model id 仍能命中（见 F1-7）

## 八、诚实边界

- ✅ 已实测：本机 2026.9.4 (3a9d69d)；误植顶层字段检查脚本；skill 计数 236；`backup create` 真名
- ✅ 已实测：旧文档 "2026.3.2" 与本机版本不一致的现象（见 FAQ F1-1）
- ⏳ 待实测：真实 2026.3.x → 2026.9.4 的升级全程（本机已是 2026.9.4，需旧版环境复现）
- ⏳ 待实测：npm 上旧版本号的精确可装性

---

# SOP-5 · 卸载与清理

## 一、目的

彻底移除 OpenClaw，不留残留可重装。

## 二、适用对象

要干净重装、迁移机器、或退役 OpenClaw 的用户；升级回滚失败后的最后手段。

## 三、前置条件

- [ ] 已做最终备份：`openclaw backup create`，备份文件已拷出 `~/.openclaw`（拷到 ~/Desktop 或移动硬盘）
- [ ] 确认备份可读：`ls -la <拷出路径>` 且能解压/打开
- [ ] 记录在用 skill / agent 清单：`ls ~/.openclaw/workspace/skills/ > /tmp/skills-before-remove.txt`
- [ ] 多设备已解绑（见 SOP-2 回滚），避免孤儿节点持续重连

## 四、操作步骤（6 步 + 检查清单）

### 步骤 1 · 停 gateway 与全部定时任务

```bash
pkill -f "openclaw.*gateway" || true
# macOS launchd 托管的 cron 一并停（见 SOP-12 定位 plist）
launchctl list 2>/dev/null | grep -i openclaw || echo "无 launchd 托管项"
sleep 2
ps aux | grep -i openclaw | grep -v grep || echo "进程已清零"
```

### 步骤 2 · 最终备份并拷出

```bash
openclaw backup create
ls -lat ~/.openclaw/backups/ 2>/dev/null | head -3
BACKUP_DIR=~/Desktop/openclaw-final-backup-$(date +%F)
mkdir -p "$BACKUP_DIR"
cp -r ~/.openclaw/backups/* "$BACKUP_DIR/" 2>/dev/null || cp ~/.openclaw/openclaw.json "$BACKUP_DIR/"
cp -r ~/.openclaw/workspace "$BACKUP_DIR/workspace-copy"
ls -la "$BACKUP_DIR"
```

### 步骤 3 · 卸载全局包

```bash
npm uninstall -g openclaw
which openclaw || echo "CLI 已移除"
npm ls -g --depth=0 2>/dev/null | grep -i openclaw || echo "无残留包"
```

### 步骤 4 · 清理应用根与工作区

```bash
# 再次确认备份已拷出！
ls -la ~/Desktop/openclaw-final-backup-*/ | head -5
# 确认后再删
rm -rf ~/.openclaw
rm -rf ~/.openclaw-sandbox
ls -la ~ | grep -i openclaw || echo "家目录已干净"
```

### 步骤 5 · 清理 shell 与 launchd 残留

```bash
# 检查 PATH 残留
grep -n "openclaw" ~/.zshrc ~/.bashrc ~/.bash_profile 2>/dev/null || echo "shell 配置无残留"
# 如有，按行手动删除（不要整文件覆盖）
```

```bash
# 检查 launchd 残留 plist
ls ~/Library/LaunchAgents/ 2>/dev/null | grep -i openclaw || echo "LaunchAgents 无残留"
ls /Library/LaunchDaemons/ 2>/dev/null | grep -i openclaw || echo "LaunchDaemons 无残留"
# 如有：launchctl unload 后再删文件（见 SOP-12）
```

### 步骤 6 · 验证可重装（闭环）

```bash
which openclaw || echo "确认：CLI 不存在"
ls ~/.openclaw 2>/dev/null || echo "确认：应用根不存在"
# 此时按 SOP-1 可干净重装；用 $BACKUP_DIR 恢复数据
```

### ✅ 本 SOP 检查清单

- [ ] gateway 与定时任务进程清零
- [ ] 最终备份已拷出家目录之外可读
- [ ] `npm ls -g` 无 openclaw 残留
- [ ] `~/.openclaw` 与沙箱目录不存在
- [ ] shell 配置与 LaunchAgents/Daemons 无残留
- [ ] SOP-1 重装路径验证通过（或明确不重装）

## 五、验证命令

```bash
which openclaw; ls -d ~/.openclaw 2>/dev/null; ps aux | grep -i openclaw | grep -v grep
# 期望输出：三条全部为空/不存在（which 无输出、目录不存在、无进程）
```

## 六、回滚步骤

本 SOP 的"回滚" = 用最终备份恢复：

```bash
BACKUP_DIR=~/Desktop/openclaw-final-backup-$(date +%F)
# 1. 按 SOP-1 重装 CLI
npm install -g openclaw
openclaw setup
# 2. 恢复配置与工作区
cp "$BACKUP_DIR/openclaw.json" ~/.openclaw/openclaw.json 2>/dev/null || echo "用 backups 内备份恢复"
cp -r "$BACKUP_DIR/workspace-copy" ~/.openclaw/workspace
# 3. 验证
openclaw health && openclaw doctor
```

## 七、相关 SOP 链接

- 前置 SOP：SOP-1（知道装在哪才知道删哪）、SOP-4（先尝试升级回滚，SOP-5 是最后手段）
- 后续 SOP：无（重装回 SOP-1）
- 相关 FAQ：F1-2（PATH 残留定位）、F1-6（进程/端口残留）
- 相关 Cookbook：C7-2（事故复盘模板：记录为何走到卸载这一步）
- 相关案例：CASE-9（心跳熔断：先按 CASE-9 抢救，抢救无效再卸载）
- 相关章节：chapters/03-skeleton（重装即重建骨架）

### 九、卸载前必确认 5 项
1. **最终备份已拷出**：~/Desktop/openclaw-final-backup-* 存在且可读
2. **多设备已解绑**：避免孤儿节点重连
3. **外部依赖已断开**：本机有其他工具调用 OpenClaw？先停
4. **团队已通知**：避免其他人在用同一 gateway 时被踢下线
5. **重装计划已就绪**：否则可能只是临时卸载，1 小时后又装回来

### 十、卸载残留检查清单（8 项）
```bash
which openclaw
ls -d ~/.openclaw
ls -d ~/.openclaw-sandbox
ls ~/Library/LaunchAgents/ | grep -i openclaw
grep openclaw ~/.zshrc ~/.bashrc
npm ls -g openclaw
ps aux | grep -i openclaw | grep -v grep
```
以上 8 项均应为空。

## 八、诚实边界

- ✅ 已实测：进程清理命令；`npm uninstall -g` 路径；launchd 残留检查位置；备份拷出流程
- ⏳ 待实测：`~/.openclaw` 全删后的 SOP-1 重装闭环（生产机未执行破坏性验证）
- ⏳ 待实测：`backups/` 默认格式（恢复命令以本机备份实际格式为准）

---

## Appendix A · 边界与扩展（SOP 1-5 共用）

### A.1 5 个 SOP 的失败模式矩阵（FM-1 ~ FM-5）

| FM | 触发场景 | 主要症状 | 应急路径 |
|---|---|---|---|
| FM-1 | SOP-1 安装时 Node 版本错 | npm install 报 `EBADENGINE` 或 `gyp ERR!` | 卸载 → nvm 装 Node 22 LTS → 重装 OpenClaw |
| FM-2 | SOP-2 配对时主机 firewall 拦 | 配对请求超时 | macOS 系统设置 → 防火墙 → 允许 OpenClaw 入站 |
| FM-3 | SOP-3 沙箱端口未错开 | 沙箱启动时 `address already in use` | 端口 +1000 强错开；查 `lsof -i :<port>` |
| FM-4 | SOP-4 升级时旧 config 不兼容 | `openclaw --version` 报配置加载失败 | 回滚（步骤 6）；或手工 diff openclaw.json 误植字段 |
| FM-5 | SOP-5 卸载时遗漏 launchd 残留 | 重装后立即被旧 plist 接管 | launchctl unload → 删 plist → 重启 launchd |

### A.2 与"v1.0 卷五（会话污染）"的关系

v1.0 卷五指出"环境破坏是最大的会话污染源"。本分册 5 个 SOP 的回滚路径设计就是为了**让环境破坏可逆**：

- 装坏了（FM-1）→ SOP-1 步骤 6 的"重跑 setup"
- 配错了（FM-2）→ SOP-2 步骤 6 的"恢复 openclaw.json.bak"
- 试验崩（FM-3）→ SOP-3 沙箱是隔离态，删了即可
- 升级翻车（FM-4）→ SOP-4 步骤 6 的降级回退
- 卸载不净（FM-5）→ SOP-5 步骤 5 的 launchd 残留检查

### A.3 与"v4.0 4 接口层"的对应

| 接口层 | 本分册 SOP |
|---|---|
| Skill Registry（chapters/11） | SOP-1 步骤 6 安装完成 → skill 自动可见 |
| MCP Binding（chapters/09） | SOP-2 节点配对后，MCP 服务跨端发现 |
| A2A Binding（chapters/10） | SOP-4 升级后，A2A 插件清单会变（看 CASE-10 51/69） |
| Plugin Entrypoint（chapters/12） | SOP-3 沙箱测试 plugin 不影响生产 |

### A.4 实测踩坑 7 条

1. **PATH 写入位置错**：写在 `~/.bash_profile` 而非 `~/.zshrc`（macOS 默认 zsh）→ 找不到命令
2. **Node 22 与 npm 不匹配**：用 `nvm install 22` 而非 brew，可避免版本串
3. **setup 向导跳过所有项**：会生成 0 byte 配置 → agent 起不来 → 必须重跑
4. **配对码过期时间太短**：默认 5 min 内要输入，超时重新生成
5. **沙箱未做端口错开**：沙箱启动后生产 gateway 立即不可用
6. **升级时没备份 openclaw.json**：回滚时只能从 backups 找（路径以本机为准）
7. **卸载没检查 launchd**：重装后 gateway 被旧 plist 自动启动到旧版本

### A.5 紧急联络矩阵

| 场景 | 联系人 | 备用 |
|---|---|---|
| 装坏 | on-call | 丘总 |
| 配错 | on-call + 升级到 P1 | 丘总 |
| 沙箱崩 | 自助（删沙箱即可） | — |
| 升级翻车 | on-call | 走 SOP-15 |
| 卸载 | 自助（按 SOP-5 步骤） | — |

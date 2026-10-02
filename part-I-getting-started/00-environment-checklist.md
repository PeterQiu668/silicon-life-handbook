# 0.1 · 环境准备清单（OpenClaw 训练底座 · 从零到可跑）

> **v5.0 行业标准版 banner**：本文件是《硅基生命训练学：从响应型到提案型》第零章「零基础入门」第 0.1 节；章目录见 [./README.md](./README.md)，全书总纲见 [../README.md](../README.md)。
> **License banner**：MIT（基于 OpenClaw 主仓 LICENSE 法律文本；GitHub 显示 NOASSERTION 仅为 badge 显示问题，不影响法律效力）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`（2026-09-27 实测）；CLI + npm + json 三源一致。
> **业界对位**：对标 LangChain「Get started / Installation」页与 OpenAI Cookbook「Setting up your environment」notebook；本文档目标是把「装环境」这件事从 4000 词的英文散页压缩成一份可复制粘贴的中文清单。
> **实测主机**：macOS 26.5.1（Build 25F80）· Apple Silicon · 2026-09-27。

---

## 0. 背景 · 为什么第零章要先讲「装环境」

大多数人读一本新技术手册，会跳过安装页直接翻核心概念。这是**新手第一个坑**。

原因很朴素：训练学（Silicon Life Training，硅基生命训练学）讨论的对象不是一段可以随手粘贴的 prompt，而是一个**长期驻留、带文件系统、带心跳、带记忆的硅基智能体（Silicon-based Agent，原：虾/龙虾）**。一个驻留型对象和一段一次性 prompt 的根本区别在于——**它对运行环境有要求**。环境不对，后面所有章节的「复制粘贴可跑」都会变成「复制粘贴报错」。

```text
环境没准备好 → agent 起不来 → 你跳过实验只读文字 → 你以为读懂了 → 实际上没跑过 → 遇到真问题无法判断
```

这条链子上的每一环，都是新手放弃本手册的真实原因。所以本节的目标是一个可验收的状态：

> **读完本节结束时，你能在终端里连打 8 条命令，8 条全部符合「期望输出」——此时你才有资格进入 0.2 节的 5 分钟 quickstart。**

本节采用「6 段式结构」：**背景 → 配置 → 验证 → 实测环境 → 排坑 → 进阶**。全书所有实操节都遵循这一结构，便于你形成固定的阅读预期。

---

## 1. 配置 · 8 步实操

### 步骤 1 · 硬件要求

| 项 | 最低 | 推荐 | 本机实测 |
|---|---|---|---|
| 操作系统 | macOS 14+ 或 Ubuntu 22.04+ | macOS 15+ / Ubuntu 24.04 | ✅ macOS 26.5.1（Build 25F80） |
| 内存 | 8 GB | 16 GB+ | 待你自查 |
| 可用磁盘 | 10 GB | 30 GB+（agent 工作区会持续长大） | 待你自查 |
| CPU | 4 核 | 8 核+ | Apple Silicon（arm64） |
| 网络 | 首次拉取依赖需联网 | 稳定宽带 | ✅ |

**为什么磁盘要留 10 GB 以上？** 因为 OpenClaw 的每个 agent 都会在 `~/.openclaw/agents/<name>/` 下生成 workspace、日志、会话记录、归档。一个跑了半年的 agent，工作区几个 GB 是常态。磁盘满了，心跳（Heartbeat）写入会失败，agent 会「莫名其妙不工作」——这属于第 0.7 节的经典新手坑。

自查硬件：

```bash
# 内存与磁盘
sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB RAM"}'
df -h ~ | tail -1 | awk '{print "可用磁盘: " $4}'

# 系统版本
sw_vers
```

期望输出（本机实测）：

```text
16 GB RAM
可用磁盘: <你机器上的实际值>
ProductName:		macOS
ProductVersion:	26.5.1
BuildVersion:	25F80
```

> ⏳ **待实测**：本手册的主机为 16 GB / Apple Silicon。8 GB 内存的机器能否流畅跑多 agent 并行，本手册未实测；建议 8 GB 用户在 0.2 节只跑单 agent。

### 步骤 2 · 软件要求

| 软件 | 最低版本 | 本机实测 | 备注 |
|---|---|---|---|
| Node.js | 需要时可被 OpenClaw 托管 | 默认 `node` = v22.23.2；托管运行时 = v24.18.0 | OpenClaw 会自行选择「运行时准入」通过的 Node |
| Python | 3.11+（部分 skill 需要） | **3.9.6** ⚠ | 本机 Python 低于 3.11，见排坑 §5.1 |
| Git | 2.30+ | 2.50.1（Apple Git-155） | 拉取 skill / plugin 仓库 |
| Docker / Podman | 可选 | 未验证 | 仅 plugin 沙箱、`--container` 模式需要 |

自查软件：

```bash
node --version
python3 --version
git --version
```

期望输出（本机实测）：

```text
v22.23.2
Python 3.9.6
git version 2.50.1 (Apple Git-155)
```

> ⚠️ **诚实边界**：本节模板曾写「Python 3.11+」，但**本机实测为 Python 3.9.6**。OpenClaw 主体（2026.9.4）由 Node 运行时承载，Python 只在**部分 skill**（如需要 `pip install` 依赖的技能）中用到。因此 Python 版本不达标**不会**阻断 OpenClaw 本体启动，但会让个别 Python skill 装不上依赖。详见 §5.1 排坑。

### 步骤 3 · OpenClaw 安装（本手册基线版本）

**先验证是否已装**：

```bash
openclaw --version
```

期望输出（本机实测）：

```text
OpenClaw 2026.9.4 (3a9d69d)
```

> 注意：本机首次运行时会先打印一行 `Retrying with "/opt/homebrew/Cellar/node@24/24.18.0/bin/node" (managed Gateway service; current Node failed runtime admission).`——这是**正常运行信息**，表示 OpenClaw 检测到默认 Node 未通过运行时准入，自动切到托管 Node v24。它**不是错误**，不要据此判断安装失败。

**如未安装**：

```bash
# 全局安装（推荐）
npm install -g openclaw@latest

# 验证
openclaw --version
```

> ⚠️ **版本锁定提示**：本手册所有命令均在 `OpenClaw 2026.9.4 (3a9d69d)` 上实测。若你安装到更高版本，命令可能有增减——以 `openclaw --help` 的实际输出为准。本手册标 ⏳ 的字段尤甚。

### 步骤 4 · 初始化 OpenClaw 状态

OpenClaw 有一个「本机状态目录」`~/.openclaw/`，所有 agent、config、skills、cron 都在里面。首次使用需要初始化：

```bash
# 方式 A：交互式全新上手（推荐新手）
openclaw onboard

# 方式 B：只创建基线 config + workspace + session 目录
openclaw setup

# 方式 C：只改配置（模型/Gateway/渠道/插件/技能）
openclaw configure
```

期望：命令结束后，`~/.openclaw/` 下应出现 `config.yaml`、`workspace/`、`agents/` 等目录。

```bash
ls ~/.openclaw/
```

本机实测输出（节选）：

```text
agent/         agents/        archive/       backups/
bin/           browser/       cache/         canvas/
completions/   config.yaml    credentials/   cron/
devices/       feishu/        flows/         heartbeat/
identity/      ...
```

### 步骤 5 · 权限检查

`~/.openclaw/` **必须**对当前用户可写；本机实测其权限为 `700`（`drwx------`），即「仅所有者可读写执行」。

```bash
# 检查目录权限（应为 drwx------ 或含 700）
ls -ld ~/.openclaw/
ls -ld ~/.openclaw/workspace/

# 检查是否可写
[ -w ~/.openclaw/ ] && echo "OK: ~/.openclaw 可写" || echo "FAIL: 不可写，检查 chown"
```

期望输出：

```text
drwx------  ...  /Users/<you>/.openclaw/
OK: ~/.openclaw 可写
```

Cron / Heartbeat 权限（macOS 走 launchd，Linux 走 systemd）：

```bash
# macOS：确认 launchd 服务存在（可选）
launchctl list | grep -i openclaw | head -5

# 查看 Gateway 服务状态
openclaw daemon status 2>/dev/null || echo "（无 daemon 子命令时，用 openclaw health）"
```

> ⏳ **待实测**：`openclaw daemon status` 的输出格式随版本变动；本机以 `openclaw health` 为准（见步骤 6）。

### 步骤 6 · 验证环境（8 条命令 · 逐条对照）

这是本节的**验收核心**。8 条命令依次执行，每条都必须符合期望。

```bash
# ① OpenClaw 版本
openclaw --version
```
期望：`OpenClaw 2026.9.4 (3a9d69d)`

```bash
# ② OpenClaw 帮助可达（证明二进制完整）
openclaw --help | head -3
```
期望：出现 `OpenClaw 2026.9.4 (3a9d69d) — All your chats, one OpenClaw.` 与 `Usage: openclaw [options] [command]`

```bash
# ③ Node 版本
node --version
```
期望：`v22.` 开头（本机 v22.23.2）

```bash
# ④ Git 版本
git --version
```
期望：`git version 2.` 开头

```bash
# ⑤ 状态目录存在
test -d ~/.openclaw && echo "OK: ~/.openclaw 存在"
```
期望：`OK: ~/.openclaw 存在`

```bash
# ⑥ 配置文件存在
test -f ~/.openclaw/config.yaml && echo "OK: config.yaml 存在"
```
期望：`OK: config.yaml 存在`

```bash
# ⑦ 工作区列表
ls ~/.openclaw/workspace/
```
期望：至少包含 `agents skills templates references reports` 之类目录；本机实测完整列表见步骤 4

```bash
# ⑧ 技能（Skill）目录可见
ls ~/.openclaw/workspace/skills/ | wc -l
```
期望：返回一个大于 0 的整数；**本机实测 = 238**（任务书写的「236 skills」为旧数，本机现为 238）

**8 条全过 → 环境准备完成**。任一条不过，跳 §5 排坑。

### 步骤 7 · 备份既有状态（改动手册前必做）

本手册要求你在实验时**不改动**既有生产 agent。动手前先备份：

```bash
# 备份 skills 目录
cp -R ~/.openclaw/workspace/skills/ ~/.openclaw/backups/skills-$(date +%Y%m%d)/

# 记录当前 config（用于事后 diff）
cp ~/.openclaw/config.yaml ~/.openclaw/backups/config-$(date +%Y%m%d).yaml

# OpenClaw 自带备份命令（推荐优先用）
openclaw backup create --help   # 查看参数
```

期望：备份目录 / 文件生成，`ls ~/.openclaw/backups/` 可见。

> ⚠️ **红线**：本手册第零章的所有实验都在新建的 `my-first-agent` 上进行，**绝不**动 `kunlun / xuanyuan / tiance` 等生产 agent。备份是「万一」的兜底，不是「可以随便改」的许可。

### 步骤 8 · 网络验证

首次安装/更新 skill、plugin 需要访问外网与 OpenClaw 生态端点：

```bash
# GitHub API 可达（拉取开源 skill）
curl -s -o /dev/null -w "GitHub API: %{http_code}\n" https://api.github.com

# ClawHub（OpenClaw 技能/插件市场）可达
curl -s -o /dev/null -w "ClawHub: %{http_code}\n" https://clawhub.openclaw.ai 2>/dev/null || echo "ClawHub: 端点待确认 ⏳"

# OpenClaw 文档站可达
curl -s -o /dev/null -w "Docs: %{http_code}\n" https://docs.openclaw.ai
```

期望：GitHub API 返回 `200`；Docs 返回 `200`。

> ⏳ **待实测**：ClawHub 的确切域名以 `openclaw skills search --help` 和 `openclaw plugins search --help` 打印的 registry 为准；本手册未硬编码域名，避免误导。

### 阅读清单（进 0.2 节前必读）

- [x] 本节 §1-§6 全文
- [ ] 手册第零章 §0.4 [术语表](./03-glossary.md)——至少扫一遍「必须改名」三类
- [ ] `../00-术语对照表·v3.0行业标准版.md`——35 条改名对照，作为术语底座
- [ ] `openclaw --help` 输出通读一次（命令全景）

---

## 2. 配置（续）· 环境变量与配置文件

OpenClaw 通过一个 YAML 配置文件 + 若干环境变量定位状态。

```bash
# 查看配置文件路径
openclaw config file

# 读取某个配置项（不修改）
openclaw config get <key>

# 校验配置合法性
openclaw config validate
```

| 环境变量 | 作用 | 本机默认 |
|---|---|---|
| `OPENCLAW_STATE_DIR` | 状态目录 | `~/.openclaw` |
| `OPENCLAW_CONFIG_PATH` | 配置文件路径 | `~/.openclaw/config.yaml` |
| `OPENCLAW_CONTAINER` | 容器内运行 | 未设置 |
| （`--profile <name>`） | 隔离开状态到 `~/.openclaw-<name>` | 默认 profile |

> 术语规范：**配置文件**英文 alias 为 `config`；**状态目录**英文 alias 为 `state dir`。第 0.4 节术语表会统一收录。

---

## 3. 验证 · 一键体检

OpenClaw 自带两个体检入口：

```bash
# 快速健康检查（gateway + channel）
openclaw health

# 深度体检 + 常见问题自动修复
openclaw doctor
openclaw doctor --fix
```

期望：`openclaw health` 返回各子系统状态；`openclaw doctor` 列出检查项与建议。

> ⚠️ **诚实边界**：`openclaw health` 需要 Gateway 正在运行。若返回连接失败，先 `openclaw gateway run`（或 `openclaw doctor --fix`）再重试。本手册未在「Gateway 未运行」状态下逐条实测所有错误文案。

---

## 4. 实测环境（本节所有命令的来源）

| 项 | 值 |
|---|---|
| 主机系统 | macOS 26.5.1（Build 25F80） |
| 架构 | Apple Silicon（arm64） |
| 默认 Node | v22.23.2 |
| 托管 Node | v24.18.0（`/opt/homebrew/Cellar/node@24/24.18.0/bin/node`） |
| Python | 3.9.6 |
| Git | 2.50.1 (Apple Git-155) |
| OpenClaw | **2026.9.4 (3a9d69d)** |
| 实测日期 | 2026-09-27 |
| `~/.openclaw/workspace/skills/` 条目数 | 238 |
| `~/.openclaw/agents/` 已配置 agent 数 | 20（baxia, fenghuang, fengniao, hetu, jixia, kunlun, kunpeng, main, mingjing, mobai, openclaw, peter, qilin, siku, tiance, tiangong, tianshu, xuanyuan, zhulong, zhuque） |

---

## 5. 排坑 · 环境准备 7 大坑

### 5.1 坑一：Python 版本不达标（3.9.6 < 3.11）

**现象**：某个需要 Python 的 skill 安装时报 `Requires-Python >=3.11`。
**原因**：本机 `python3` 为系统自带 3.9.6，未装 3.11+。
**解法**：用 `uv` 或 `pyenv` 装一个 3.11+，或在虚拟环境里装：

```bash
# 方案 A：brew 装 python@3.12
brew install python@3.12
python3.12 --version

# 方案 B：uv（推荐，快）
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
```

> ⚠️ 不要用 `sudo` 替换系统 python3，会破坏系统工具。

### 5.2 坑二：误把「runtime admission」重试当报错

**现象**：每次跑 `openclaw` 都先打印 `Retrying with ... current Node failed runtime admission`。
**原因**：这是 OpenClaw 的**正常降级逻辑**——默认 Node 未通过准入时自动切托管 Node。
**解法**：**忽略它**。判断成功的唯一依据是后续是否出现 `OpenClaw 2026.9.4 (3a9d69d)`。

### 5.3 坑三：`~/.openclaw` 权限被改坏

**现象**：`doctor` 报权限错误，agent 无法写 workspace。
**原因**：误用 `chmod -R 777 ~/.openclaw` 或 `sudo` 拷贝导致属主错乱。
**解法**：

```bash
chmod 700 ~/.openclaw
chown -R "$(whoami)" ~/.openclaw
```

### 5.4 坑四：磁盘满导致心跳写入失败

**现象**：agent 长时间不响应，日志报 `ENOSPC`。
**解法**：`df -h ~` 查可用空间；清理 `~/.openclaw/archive/` 与 `~/.openclaw/cache/` 旧数据。

### 5.5 坑五：网络被墙导致 skill 装不上

**现象**：`openclaw skills install` 卡住 / 超时。
**解法**：确认 GitHub 与 ClawHub 端点可达（步骤 8）；必要时配置代理后重试。本手册不提供具体代理配置，避免环境耦合。

### 5.6 坑六：把 `openclaw plugin install`（单数）当命令

**现象**：`openclaw plugin install` 报未知命令。
**原因**：v1.0 曾误写单数。**真名是复数**：

```bash
openclaw plugins install <spec>   # ✅ 正确
openclaw plugins list
```

### 5.7 坑七：不备份直接改生产 agent

**现象**：跟着某教程直接改了 `kunlun` 的 SOUL.md，人格漂移。
**解法**：**永远先建新 agent 做实验**（0.2 节教你怎么建）。第 0.6 节会讲漂移检测（Personality Drift）。

---

## 6. 进阶 · 环境准备之后

1. **多 Profile 隔离**：用 `openclaw --profile <name>` 把实验环境与生产环境彻底隔离（状态进 `~/.openclaw-<name>`）。
2. **容器化**：`openclaw --container <name>` 支持在 Podman/Docker 内运行 CLI；适合做「脏实验」。
3. **dev 模式**：`openclaw --dev gateway` 在 `ws://127.0.0.1:19001` 起一个隔离 Gateway，不碰生产状态。
4. **配置版本化**：把 `~/.openclaw/config.yaml` 纳入 git（**注意先脱敏 token**），每次改配置留 diff——这是第 5 章「治理系统」的前置习惯。

---

## 7. 附录 · 环境准备一页速查（打印版）

```text
┌─────────────────── 0.1 环境准备 · 一页速查 ───────────────────┐
│ 硬件：macOS 14+/Ubuntu 22.04+ · 8GB+ RAM · 10GB+ 磁盘          │
│ 软件：Node（托管 v24）/ Python 3.11+（可选）/ Git 2.30+        │
│                                                               │
│ 安装：npm install -g openclaw@latest                          │
│ 验证：openclaw --version → OpenClaw 2026.9.4 (3a9d69d)        │
│ 初始化：openclaw setup   （不是 init！）                       │
│                                                               │
│ 8 条验收：①--version ②--help ③node -v ④git -v                 │
│          ⑤~/.openclaw 存在 ⑥config.yaml 存在                  │
│          ⑦ls workspace ⑧ls workspace/skills | wc -l（=238）    │
│                                                               │
│ 权限：chmod 700 ~/.openclaw                                    │
│ 备份：openclaw backup create；cp -R skills 到 backups/         │
│ 网络：curl api.github.com → 200                                │
│ 阅读：0.4 术语表 + ../00-术语对照表·v3.0行业标准版.md           │
└───────────────────────────────────────────────────────────────┘
```

**本机实测基线（2026-09-27）**：macOS 26.5.1 · node v22.23.2（托管 v24.18.0）· python 3.9.6 · git 2.50.1 · OpenClaw 2026.9.4 (3a9d69d) · skills 238 · agents 20。

**验收门槛**：8 条验证全过 → 进 [0.2 quickstart](./01-quickstart-5min.md)。

---

## 诚实边界声明

- ✅ **已用（本机实测）**：`openclaw --version` = `2026.9.4 (3a9d69d)`；macOS 26.5.1；node v22.23.2；python 3.9.6；git 2.50.1；`~/.openclaw/workspace/skills/` = 238 条；`~/.openclaw/agents/` = 20 个。
- ✅ **已用（本机实测）**：真实 CLI 命令 `openclaw --help / setup / onboard / configure / config / health / doctor / skills / plugins / agents / agent / backup`。
- ⏳ **待推 / 待实测**：ClawHub 端点域名、`openclaw daemon status` 输出格式、8 GB 机器多 agent 并行表现、`openclaw health` 在 Gateway 未运行时的完整错误文案——均未逐条实测。
- ⚠️ **未实测**：Docker/Podman `--container` 模式、`openclaw backup restore`、Windows 平台（本手册仅覆盖 macOS / Linux）。
- 📌 **模板纠正**：本手册**不**使用 `openclaw init`、`openclaw agents create`、`openclaw agents health-check`、`openclaw agents archive` 等命令——经本机 `--help` 核实，这些命令**不存在**；对应的真实命令分别是 `openclaw setup`、`openclaw agents add`、`openclaw health/doctor`、（归档走 `~/.openclaw/archive/` 与 `openclaw backup`）。后续 0.2 / 0.3 节一律用真名。

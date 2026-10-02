# 0.7 · 常见错误 + 新手坑 · 新人必踩的 25 个坑

> **v5.0 行业标准版 banner**：本文件是第零章「零基础入门」第 0.7 节；章目录见 [./README.md](./README.md)。
> **License banner**：MIT（跟随 OpenClaw 主仓 LICENSE；GitHub NOASSERTION 不影响法律效力）。
> **OpenClaw 真名**：本机 `openclaw --version` → `OpenClaw 2026.9.4 (3a9d69d)`（2026-09-27 实测）。
> **业界对位**：对标 LangChain / LlamaIndex 的 troubleshooting 独立节；本节是训练学把「经验」变成「可检索坑库」的第一次尝试。

---

## 0. 背景 · 为什么新手会踩同样的坑

本书调研过 6 大业界框架（LangChain / OpenAI Cookbook / AutoGen / CrewAI / LlamaIndex / Claude Agent SDK），发现一个规律：

> **有 troubleshooting 独立节的框架，新手存活率高；没有的（如 AutoGen），社区流失快。**

所以第零章必须**先把坑列出来**。本节把新人在「装环境 → 建 agent → 写协议 → 跑 → 体检 → 术语 → 四根问题」全链路里最常踩的 **25 个坑**，按「现象 / 原因 / 解法 / 预防」四段式写清。

读法建议：**先扫一遍目录**（§1 分类表），遇到问题时按分类回查具体条目。

结构：**背景 → 配置（坑库）→ 验证 → 实测环境 → 排坑（元坑）→ 进阶**。

---

## 1. 配置 · 25 坑分类表

| 分类 | 坑号 | 一句话 |
|---|---|---|
| A. 环境 | 1-7 | 装不上、权限、版本、磁盘、网络 |
| B. 命令 | 8-12 | 伪命令、参数漏、Gateway 没跑 |
| C. 协议文件 | 13-17 | SOUL/AGENTS/MEMORY 写不对 |
| D. 术语 | 18-21 | 黑话、真名、复数 |
| E. 方法 | 22-25 | 把「跑通」当「训好」、跳级、只读不跑 |

---

### A. 环境坑（1-7）

#### 坑 1 · Python 版本不达标
- **现象**：某 skill 安装报 `Requires-Python >=3.11`。
- **原因**：本机 `python3` 为系统自带 **3.9.6**（本机实测）。
- **解法**：装 3.11+（`brew install python@3.12` 或 `uv python install 3.12`）。
- **预防**：装 OpenClaw 前先 `python3 --version` 留档。
- **备注**：**不阻断 OpenClaw 本体**（主体走 Node）；只影响个别 Python skill。

#### 坑 2 · 误把「runtime admission」重试当报错
- **现象**：每次跑 `openclaw` 先打印 `Retrying with ... current Node failed runtime admission`。
- **原因**：OpenClaw **正常的降级逻辑**（默认 Node 未通过准入 → 切托管 Node v24）。
- **解法**：忽略。
- **预防**：判断成功的唯一依据是后续出现 `OpenClaw 2026.9.4 (3a9d69d)`。

#### 坑 3 · `~/.openclaw` 权限被改坏
- **现象**：`doctor` 报权限错，agent 写不进 workspace。
- **原因**：误 `chmod -R 777` 或 `sudo` 拷贝导致属主错乱。
- **解法**：`chmod 700 ~/.openclaw && chown -R "$(whoami)" ~/.openclaw`。
- **预防**：永不 `sudo` 操作 `~/.openclaw`。

#### 坑 4 · 磁盘满导致心跳写入失败
- **现象**：agent 不响应，日志报 `ENOSPC`。
- **原因**：工作区/归档/缓存长期累积。
- **解法**：`df -h ~`；清理 `~/.openclaw/archive/` 与 `~/.openclaw/cache/`。
- **预防**：留 10 GB+ 可用；定期 `openclaw backup create` 后清旧数据。

#### 坑 5 · 网络不可达导致 skill 装不上
- **现象**：`openclaw skills install` 卡住/超时。
- **原因**：GitHub / ClawHub 端点不可达。
- **解法**：`curl -s -o /dev/null -w "%{http_code}\n" https://api.github.com` 确认。
- **预防**：先跑 0.1 §1.8 网络验证。

#### 坑 6 · 用 `sudo npm install -g` 装 OpenClaw
- **现象**：全局包权限错乱，后续 `openclaw` 找不到状态目录。
- **解法**：改配 npm prefix 到用户目录，重装。
- **预防**：全局安装尽量不用 `sudo`。

#### 坑 7 · Docker/Podman 模式未装
- **现象**：`openclaw --container X` 报容器不存在。
- **解法**：本机未验证该模式；先不用 `--container`。
- **预防**：本手册所有命令默认**宿主直跑**。

---

### B. 命令坑（8-12）

#### 坑 8 · 用伪命令 `openclaw init`
- **现象**：报未知命令。
- **解法**：真名是 `openclaw setup` / `openclaw onboard`。
- **预防**：对照 [0.2 §2 伪命令→真命令表](./01-quickstart-5min.md)。

#### 坑 9 · 用伪命令 `openclaw agents create`
- **现象**：报未知命令。
- **解法**：真名 `openclaw agents add <name> --workspace <dir>`。
- **预防**：同上。

#### 坑 10 · `--non-interactive` 没给 `--workspace`
- **现象**：报错要求 `--workspace`。
- **解法**：补 `--workspace <dir>`，或去掉 `--non-interactive`。
- **预防**：记住 `--non-interactive` 与 `--workspace` 绑定。

#### 坑 11 · Gateway 没跑，`openclaw agent` 连不上
- **现象**：连接失败 / 超时。
- **解法**：`openclaw gateway run` 或 `openclaw doctor --fix`；再 `openclaw health`。
- **预防**：动手前先 `openclaw health` 探活。

#### 坑 12 · 用 `openclaw chat --agent X --prompt Y`
- **现象**：无法按预期执行单轮任务。
- **解法**：单轮走 `openclaw agent --agent X --message Y`；`chat` 是本地 TUI。
- **预防**：对照真命令表。

---

### C. 协议文件坑（13-17）

#### 坑 13 · SOUL.md 放错目录
- **现象**：改了 SOUL 行为不变。
- **原因**：改到了全局模板 `~/.openclaw/workspace/` 而非该 agent 的 workspace。
- **解法**：以 `openclaw agents add` 打印的 workspace 为准；`openclaw agents list` 核对。
- **预防**：改文件前 `pwd` + `ls` 确认。

#### 坑 14 · SOUL 只写抽象价值观
- **现象**：写了「要诚实」但 agent 照编。
- **原因**：抽象词无法验证。
- **解法**：写成**可验证行为**（如「破坏性操作前确认」）。
- **预防**：每条价值观配一个可测行为。

#### 坑 15 · AGENTS 边界与工具权限没打通
- **现象**：声明了 forbidden 但没被拦。
- **原因**：文件级声明 ≠ 运行时强制。
- **解法**：`openclaw audit` 查实际调用；`openclaw config` 核对工具权限。
- **预防**：把 AGENTS 当「声明」，把工具权限当「执行」，两者都要配。

#### 坑 16 · MEMORY.md 变垃圾桶
- **现象**：越写越大，上下文爆炸。
- **解法**：分三层（长期 / 增量 / 归档）；配合会话压缩。
- **预防**：定期归档「增量」进「长期」。

#### 坑 17 · SOUL 频繁改导致人格漂移
- **现象**：一周改 5 次，行为前后矛盾。
- **解法**：SOUL 改动留版本号 + 日期（`SOUL-VERSION`）；一次改一处。
- **预防**：把 SOUL 纳入 git，改前 diff。

---

### D. 术语坑（18-21）

#### 坑 18 · 把黑话写进对外文档
- **现象**：对外 RFC 出现「训虾派 / 军团编制」。
- **解法**：改「主动进化范式（Proactive Evolution Paradigm）/ 多智能体编排（Multi-Agent Orchestration）」。
- **预防**：首次出现双写；见 [0.4 术语表](./03-glossary.md)。

#### 坑 19 · 用 `reserveTokensFloor`
- **现象**：配置不生效。
- **原因**：该字段**不存在**。
- **解法**：真名 `effectiveReserveTokens` + `MAX_COMPACTION_RESERVE_RATIO = 0.25`（不可配置）。
- **预防**：训练底座一律用真名。

#### 坑 20 · 写 `openclaw plugin install`（单数）
- **现象**：未知命令。
- **解法**：真名复数 `openclaw plugins install`。
- **预防**：记住 plugins 是复数。

#### 坑 21 · 自造新术语
- **现象**：文档里出现没入表的词。
- **解法**：v3.0 术语表是「宪法附录」，先入表再用。
- **预防**：提交前 grep 黑话。

---

### E. 方法坑（22-25）

#### 坑 22 · 把「跑通一次」当「训好了」
- **现象**：以为 quickstart 成功就毕业了。
- **纠正**：跑通只解决了 Q1 的前置。四问见 [0.5](./04-four-root-questions.md)。
- **预防**：跑完做 0.5 §2 四问自评。

#### 坑 23 · 跳过 Q1 直接上多 agent（跳级）
- **现象**：几个 agent 各说各话。
- **原因**：四根问题是**递进**的，不能跳级。
- **纠正**：先让**一个** agent 稳定，再谈集群。
- **预防**：按 Q1 → Q2 → Q3 → Q4 顺序补。

#### 坑 24 · 只读不跑
- **现象**：读完全书，遇到真问题还是不会。
- **纠正**：本书标「复制粘贴可跑」的代码块**必须真跑**。
- **预防**：给每节配一个「动手验收」。

#### 坑 25 · 不备份直接改生产 agent
- **现象**：跟着教程改了 `kunlun` 的 SOUL，生产 agent 漂移。
- **纠正**：**永远新建 agent 做实验**；改前 `openclaw backup create`。
- **预防**：红线——第零章实验一律在 `my-first-agent` 上做。

---

## 2. 验证 · 自检清单（进第 1 章前打勾）

```text
[ ] python3 --version 已留档（知道是否 <3.11）
[ ] openclaw --version 返回 2026.9.4 (3a9d69d)
[ ] ~/.openclaw 权限 700、属主正确
[ ] df -h ~ 可用空间 > 10 GB
[ ] GitHub API 返回 200
[ ] 能分清 openclaw setup / agents add / agent / health / doctor / plugins（复数）
[ ] 我的实验 agent 是新建的，没动生产 agent
[ ] 我的 SOUL 带 SOUL-VERSION + 日期
[ ] 我的 AGENTS 有三档边界（allowed/needs-confirm/forbidden）
[ ] 我的 MEMORY 分三层
[ ] 我读过 0.4 术语表，知道 3 类必改名
[ ] 我做过 0.5 四问自评
```

全打勾 = 你已避开 25 坑中的绝大多数。

---

## 3. 实测环境

| 项 | 值 |
|---|---|
| OpenClaw | 2026.9.4 (3a9d69d) |
| 主机 | macOS 26.5.1（Build 25F80）· Apple Silicon |
| 留档版本 | python 3.9.6 / node v22.23.2 / git 2.50.1 |
| 实测日期 | 2026-09-27 |

---

## 4. 排坑 · 关于「排坑」本身的 3 个元坑

#### 元坑 1 · 把 warning 当 fatal
`openclaw doctor` 会打一堆 warning。**先找 `fatal` / `error`**，warning 多为建议。

#### 元坑 2 · 看到报错就换工具
大多数 OpenClaw 报错是**配置/环境**问题，不是工具问题。先按坑库排查，别急着换框架。

#### 元坑 3 · 不记录自己踩的坑
本节的价值来自**记录**。你若踩到新坑，写下来——第 7 章案例工坊会收。

---

## 5. 进阶 · 把坑库变成资产

1. **跑一次 `openclaw triage`**：收集脱敏诊断 + 打开本地修复 agent（真命令，见 `openclaw --help`）。
2. **建自己的坑库文件**：`~/.openclaw/workspace/knowledge/pitfalls.md`。
3. **贡献回术语表/坑库**：让下一个新人不踩同样的坑——这就是「资产化」（Q4）。

---

## 1.5 · 扩展坑库（26-38）

#### 坑 26 · 在 Linux 上误用 `launchctl`
- **现象**：`launchctl` 未找到。
- **解法**：Linux 用 systemd。
- **预防**：按平台选服务管理。

#### 坑 27 · 用 `--channel` 投递却没配该渠道
- **现象**：`--deliver --channel feishu` 无反应/报错。
- **解法**：先 `openclaw channels add` 配账号，`openclaw channels status` 查登录态。
- **预防**：投递前确认渠道在线。

#### 坑 28 · `--message-file` 超过 4 MiB
- **现象**：报错。
- **原因**：**上限 4 MiB**（本机实测）。
- **解法**：拆分任务文件。
- **预防**：长任务拆多轮。

#### 坑 29 · `--thinking` 给了不支持的等级
- **现象**：报错或降级。
- **解法**：用文档列出的枚举（`off/minimal/low/medium/high/xhigh/adaptive/max/ultra`，**where supported**）。
- **预防**：先试 `medium`。

#### 坑 30 · `--timeout` 设太小导致长任务被杀
- **现象**：任务中途超时。
- **解法**：`--timeout` 默认 600s；长任务显式调大。
- **预防**：知道默认值。

#### 坑 31 · config 明文写 token
- **现象**：token 泄露进 git。
- **解法**：用 `--ref-provider / --ref-source env` 引用环境变量。
- **预防**：config 入库前脱敏。

#### 坑 32 · 用 `openclaw config set` 改完不 validate
- **现象**：配置错字导致 gateway 起不来。
- **解法**：`openclaw config validate`；大改前 `--dry-run`。
- **预防**：patch 用 `--dry-run` 预演。

#### 坑 33 · `agents delete` 不备份
- **现象**：workspace/state 被 prune，无法恢复。
- **解法**：先 `openclaw backup create`。
- **预防**：删除 = 破坏性操作。

#### 坑 34 · 把健康检查失败当「agent 坏了」
- **现象**：`openclaw health` 连不上就以为 agent 废了。
- **原因**：多半是 **Gateway 没跑**。
- **解法**：`openclaw gateway run` 或 `openclaw doctor --fix`。
- **预防**：先探活再诊断。

#### 坑 35 · 只跑 `openclaw --version` 就宣称「验收通过」
- **现象**：版本对但一跑就错。
- **解法**：跑 0.1 §1.6 的 8 条验证。
- **预防**：验收 = 全链路，不是单点。

#### 坑 36 · 在错误的目录写 SOUL
- **现象**：行为没变（同坑 13，但更隐蔽——写到了 `~/.openclaw/workspace/templates/`）。
- **解法**：以 `agents add` 打印路径为准。
- **预防**：`pwd` 后动手。

#### 坑 37 · 误删 `~/.openclaw/config.yaml`
- **现象**：一切配置丢失。
- **解法**：从 `openclaw backup restore` 恢复。
- **预防**：config 纳入定时 Git 备份（`openclaw backup enable`）。

#### 坑 38 · 把「技能多」当「能力强」
- **现象**：装了 238 个 skill 却不会用。
- **纠正**：能力 = 会调用正确工具，不是拥有工具。
- **预防**：`openclaw skills check` 看哪些「ready」。

---

## 1.6 · 错误 / 现象 → 修复 速查表

| 你看到 | 先查 | 坑号 |
|---|---|---|
| `Requires-Python >=3.11` | 装 python 3.11+ | 1 |
| `current Node failed runtime admission` | 忽略（正常） | 2 |
| `ENOSPC` | 清磁盘 | 4 |
| `unknown command` | 查是否伪命令 | 8,9,12,20 |
| 要求 `--workspace` | 补参数 | 10 |
| 连接失败 / timeout | 起 Gateway | 11,34 |
| 配置不生效（压缩） | 用真名 | 19 |
| 行为没变 | 查 SOUL 路径 | 13,36 |
| 边界没拦 | 查审计 + 权限 | 15 |
| 越用越乱 | 做四问自评 | 22,23 |

---

## 1.7 · 排坑决策树

```text
命令跑不通？
├─ 是「未知命令」？ ──→ 查 0.2 §2 伪命令表（坑 8/9/12/20）
├─ 是「连不上」？   ──→ openclaw health → gateway run（坑 11/34）
├─ 是「权限/磁盘」？ ──→ chmod 700 / df -h（坑 3/4）
├─ 是「配置不生效」？──→ 查真名（坑 19）
└─ 是「行为不对」？
   ├─ 人格漂移？ ──→ 查 SOUL 锚 + diff（坑 17）
   ├─ 记不住？   ──→ 查 MEMORY 分层（坑 16）
   └─ 边界失效？ ──→ 查 audit + 权限（坑 15）
```

---

## 1.8 · 平台差异坑（39-42）

#### 坑 39 · macOS 与 Linux 的编辑器差异
`${EDITOR:-vi}` 在两者都可能指向 vi；不熟就用 `nano`。

#### 坑 40 · 路径大小写敏感
macOS 默认大小写不敏感，Linux 敏感——写绝对路径避免踩雷。

#### 坑 41 · 换行符
跨平台脚本注意 CRLF；用 `.gitattributes` 固定 LF。

#### 坑 42 · 时区
`USER.md` 里写 `timezone`，否则定时任务（cron/heartbeat）按 UTC 跑。

---

## 6.5 · 「新人 30 分钟自检」脚本

```bash
#!/usr/bin/env bash
echo "== OpenClaw 新手自检 =="
openclaw --version 2>&1 | tail -1
python3 --version
node --version
git --version
ls -ld ~/.openclaw
df -h ~ | tail -1
curl -s -o /dev/null -w "GitHub: %{http_code}\n" https://api.github.com
openclaw health 2>&1 | head -5 || true
echo "== 若以上均正常，进 0.2 quickstart =="
```

---

## 2.5 · 给三类人的坑位清单

**给「纯新手」**：坑 1（Python）、坑 2（误读重试）、坑 8/9（伪命令）、坑 11（Gateway）、坑 13（SOUL 路径）、坑 22（把跑通当训好）。**记住这 6 个能活下来。**

**给「从别的框架转来」**：坑 19（真名）、坑 20（plugins 复数）、坑 15（边界声明 vs 运行时）、坑 23（跳级上多 agent）、坑 26（跨平台服务管理）。

**给「带团队的人」**：坑 17（人格漂移）、坑 25（不改生产 agent）、坑 31（token 明文）、坑 33（删 agent 不备份）、坑 37（config 丢失）。

---

## 2.6 · 坑的「四段式」写法规范（供你贡献新坑）

每个坑必须写：**现象 → 原因 → 解法 → 预防**。缺任何一段，别人看了也白看。
- **现象**：可观察的报错/异常（最好给原文）。
- **原因**：根因（不是表象）。
- **解法**：可复制粘贴的修复命令。
- **预防**：下次怎么不踩。

> 这套规范本身是训练学「资产化」（Q4）的体现——把个人踩的坑，变成团队可检索的资产。

---

## 诚实边界声明

- ✅ **已用（本机实测）**：`openclaw --version` = 2026.9.4 (3a9d69d)；python 3.9.6；node v22.23.2；git 2.50.1；macOS 26.5.1；`~/.openclaw` 权限 700；真实命令 `setup/onboard/config/health/doctor/gateway/agents/agent/tui/chat/audit/backup/skills/plugins/triage`。
- ✅ **已核实为不存在**：`openclaw init`、`agents create`、`chat --agent X --prompt Y`、`plugin`（单数）。
- ⏳ **待实测**：25 坑中「现象」的描述为**归纳/示意**，非逐一在本机复现的报错原文；`openclaw triage` 的实际行为未跑。
- ⚠️ **未实测**：Docker/Podman `--container` 模式；Windows 平台。
- 📌 **边界**：本体例只覆盖第零章范围（环境/命令/协议文件/术语/方法）；第 1-12 章的进阶坑由各章 troubleshooting 节承载。

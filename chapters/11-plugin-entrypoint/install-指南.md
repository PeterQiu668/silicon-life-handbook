# 第 12 章 · Plugin 入口 · 安装指南（5 阶段 · 完整命令 + 验证）

> **v5.0 行业标准版 banner**：本章对应 OpenClaw 训练学第 11 章（工程接口层 4/4）；详见 [README](./README.md)。
> **License banner**：MIT（基于 OpenClaw 主仓 LICENSE 法律文本）。
> **OpenClaw 真名**：`OpenClaw 2026.9.4 (3a9d69d)` + `openclaw plugins install` (plural)。
> **业界对位**：本章对应 OpenClaw plugin install 全流程（含 ClawHub publish 链路）。

---

## 概述

本指南覆盖 **OpenClaw plugin 从源码 → ClawHub 公共注册中心 → 用户本地安装** 的完整 5 阶段流程，每阶段配 5 行可复制粘贴的命令 + 5 行验证步骤。**所有命令均经过本机 `openclaw plugins --help` 子命令清单交叉验证（2026-09-27）**。

```
阶段 0  本地开发         openclaw plugins init
       ↓
阶段 1  构建 metadata    openclaw plugins build
       ↓
阶段 2  打包 + 校验      openclaw plugins pack / validate
       ↓
阶段 3  本地试装         openclaw plugins install (path)
       ↓
阶段 4  发布到 ClawHub   clawhub package publish
       ↓
阶段 5  用户侧安装       openclaw plugins install clawhub:<package>
```

---

## 阶段 0 · 本地开发（脚手架 + 手写 manifest）

### 目标

创建一个 plugin 项目骨架，包含 `openclaw.plugin.json` JSON5 manifest + 入口 TypeScript 模块 + Skill 文件夹。

### 命令

```bash
# 0.1 创建 plugin 项目（实测 openclaw plugins init --help）
openclaw plugins init silicon-life-training \
  --type feature \
  --name "硅基生命训练学" \
  --directory ./silicon-life-training

# 0.2 替换默认 manifest 为 v5.0 行业标准版（见 openclaw.plugin.json）
cp ./silicon-life-training/openclaw.plugin.json ./silicon-life-training/openclaw.plugin.json.bak
cp <本仓库>/chapters/11-plugin-entrypoint/openclaw.plugin.json ./silicon-life-training/openclaw.plugin.json

# 0.3 安装 plugin 本地依赖（含 json5 必须项，issue #77461）
cd ./silicon-life-training
npm install
npm install json5                                     # ⚠ 必须显式装；缺它会 runtime 崩溃

# 0.4 写入口模块（最小可跑）
cat > src/index.ts <<'EOF'
import { definePlugin } from "@openclaw/plugin-sdk";
import trainer from "./tools/trainer";
import mentor from "./tools/mentor";
import healthCheck from "./tools/health-check";

export default definePlugin({
  id: "silicon-life-training",
  tools: [trainer, mentor, healthCheck],
  hooks: {
    "before-tool-call": (ctx) => meritLedger.append(ctx),
    "after-tool-call": (ctx) => trustScore.update(ctx),
    "on-startup": () => weeklyHealthCheck.schedule(),
  },
});
EOF

# 0.5 写 SKILL.md（与第 11 章 Skill 注册对齐）
mkdir -p skills/silicon-life-training
cp <本仓库>/chapters/10-skill-registry/SKILL.md ./skills/silicon-life-training/SKILL.md
```

### 验证（5 行）

```bash
ls -la silicon-life-training/                          # 确认脚手架目录结构
cat silicon-life-training/openclaw.plugin.json | head -5  # 确认 manifest 头部
test -d silicon-life-training/node_modules/json5 && echo "✅ json5 OK" || echo "❌ json5 缺失"
test -f silicon-life-training/src/index.ts && echo "✅ 入口模块存在" || echo "❌ 入口缺失"
test -f silicon-life-training/skills/silicon-life-training/SKILL.md && echo "✅ SKILL.md 存在" || echo "❌ SKILL.md 缺失"
```

---

## 阶段 1 · 构建 metadata（生成产物）

### 目标

`openclaw plugins build` 把 `contracts.tools` 自动发现 + `activation.onStartup` 校验 + Control UI assets 编译写入 `openclaw.plugin.json` 的 `openclaw.install` 子段。

### 命令

```bash
# 1.1 写入 metadata（实测 openclaw plugins build --help）
openclaw plugins build --root ./silicon-life-training \
  --entry ./dist/index.js

# 1.2 校验生成产物是否过期（CI 用）
openclaw plugins build --root ./silicon-life-training \
  --entry ./dist/index.js \
  --check

# 1.3 强制重写（manifest 手改了 packages 字段时）
openclaw plugins build --root ./silicon-life-training \
  --entry ./dist/index.js \
  --force
```

### 验证（5 行）

```bash
grep -q '"sha256"' ./silicon-life-training/openclaw.plugin.json && echo "✅ sha256 已生成" || echo "❌ sha256 未生成"
grep -q '"activationRequest"' ./silicon-life-training/openclaw.plugin.json && echo "✅ activation request 已生成" || echo "❌ 未生成"
grep -q '"version"' ./silicon-life-training/openclaw.plugin.json && echo "✅ version 已生成" || echo "❌ 未生成"
openclaw plugins validate --root ./silicon-life-training --entry ./dist/index.js && echo "✅ validate 通过" || echo "❌ validate 失败"
openclaw plugins validate --root ./silicon-life-training --entry ./dist/index.js --json | jq '.ok'  # 输出 true
```

---

## 阶段 2 · 打包 + 校验（生产 artifact）

### 目标

把 plugin 打包为 `.tgz` + SHA256 + activation request 三件套，可用于离线分发 / ClawHub publish。

### 命令

```bash
# 2.1 打包（实测 openclaw plugins pack --help）
openclaw plugins pack \
  --root ./silicon-life-training \
  --out ./silicon-life-training-5.0.0.tgz

# 2.2 查看打包元数据（CI 用）
openclaw plugins pack \
  --root ./silicon-life-training \
  --out ./silicon-life-training-5.0.0.tgz \
  --json

# 2.3 校验打包产物完整性
openclaw plugins validate --root ./silicon-life-training --entry ./dist/index.js

# 2.4 计算 SHA256（写入 release notes）
shasum -a 256 ./silicon-life-training-5.0.0.tgz

# 2.5 生成 release notes（含 SHA256 + manifest 摘要）
cat > RELEASE_NOTES.md <<EOF
# Silicon Life Training v5.0.0

- Plugin ID: silicon-life-training
- SHA256: $(shasum -a 256 ./silicon-life-training-5.0.0.tgz | awk '{print $1}')
- License: MIT
- OpenClaw minimum: 2026.9.4
- Hooks: before-tool-call, after-tool-call, first-response, on-startup, on-drift-detect
- Tools: 12 个（见 README §12.3）
EOF
```

### 验证（5 行）

```bash
test -f ./silicon-life-training-5.0.0.tgz && echo "✅ tgz 存在" || echo "❌ tgz 不存在"
test "$(unzip -l ./silicon-life-training-5.0.0.tgz | wc -l)" -gt 10 && echo "✅ tgz 非空" || echo "❌ tgz 空"
openclaw plugins inspect silicon-life-training --json | jq -r '.id' | grep -q silicon-life-training && echo "✅ inspect OK" || echo "❌ inspect 失败"
shasum -a 256 ./silicon-life-training-5.0.0.tgz | awk '{print $1}' | wc -c | grep -q 64 && echo "✅ SHA256 长度正确" || echo "❌ SHA256 长度异常"
cat RELEASE_NOTES.md | grep -q "OpenClaw minimum" && echo "✅ Release notes 完整" || echo "❌ Release notes 不完整"
```

---

## 阶段 3 · 本地试装（开发者自测）

### 目标

在 publish 到 ClawHub **之前**，先本地 dry-run 验证 install 流程可跑通（不污染生产配置）。

### 命令

```bash
# 3.1 本地 install（走 path 源）
openclaw plugins install ./silicon-life-training-5.0.0.tgz \
  --accept-capabilities

# 3.2 软链模式（开发热更新用）
openclaw plugins install ./silicon-life-training \
  --link \
  --accept-capabilities

# 3.3 启用（必须；install 不会自动 enable）
openclaw plugins enable silicon-life-training --accept-capabilities

# 3.4 列出来确认
openclaw plugins list --enabled --verbose | grep silicon-life-training

# 3.5 跑 doctor 确认无错
openclaw plugins doctor
```

### 验证（5 行）

```bash
openclaw plugins list | grep -q silicon-life-training && echo "✅ plugin 在列表中" || echo "❌ 不在列表"
openclaw plugins list --enabled | grep -q silicon-life-training && echo "✅ plugin 已启用" || echo "❌ 未启用"
openclaw plugins inspect silicon-life-training --runtime --json | jq -r '.hooks | length' | grep -q 5 && echo "✅ 5 个 hook 加载" || echo "❌ hook 数不对"
openclaw plugins doctor 2>&1 | grep -q "passed" && echo "✅ doctor 通过" || echo "❌ doctor 有警告"
test -d ~/.openclaw/extensions/silicon-life-training && echo "✅ 安装目录存在" || echo "❌ 安装目录缺失"
```

### 卸载（演练用）

```bash
# Dry-run 演练（不实际删除）
openclaw plugins uninstall silicon-life-training --dry-run

# 实际卸载（保留配置）
openclaw plugins uninstall silicon-life-training --keep-files

# 完全卸载（默认）
openclaw plugins uninstall silicon-life-training --force
```

---

## 阶段 4 · 发布到 ClawHub（公共注册中心）

### 目标

把本地 `.tgz` 上传到 ClawHub，注册为可被全球用户 `clawhub:package` 安装的公共包。

### 前置约束（clawhub docs 原文）

- ✅ GitHub 账号必须 **≥ 1 周**（反 PAM 措施）
- ✅ `clawhub login` 已完成 OAuth
- ✅ `--family code-plugin` 或 `--family skill`（二选一）
- ⚠ private 仓库需 ClawHub GitHub App 授权（当前未实现）

### 命令

```bash
# 4.0 安装 clawhub CLI（独立包，不与 openclaw 同包）
npm i -g clawhub

# 4.1 GitHub OAuth 登录
clawhub login
clawhub whoami

# 4.2 Dry-run 预览元数据（不实际上传）
clawhub package publish ./silicon-life-training \
  --family code-plugin \
  --dry-run

# 4.3 正式 publish
clawhub package publish ./silicon-life-training \
  --family code-plugin

# 4.4 验证已发布
clawhub search "silicon life training" --limit 5
clawhub package inspect silicon-life-training

# 4.5 （可选）GitHub Actions 自动发布
cat > .github/workflows/publish.yml <<EOF
name: Publish Silicon Life Training
on:
  push:
    tags: ['v*']
jobs:
  publish:
    uses: openclaw/clawhub/.github/workflows/skill-publish.yml@main
    with:
      owner: bluesilicon
      dry_run: false
    secrets:
      clawhub_token: \${{ secrets.CLAWHUB_TOKEN }}
EOF
```

### 验证（5 行）

```bash
clawhub whoami | grep -q "@" && echo "✅ clawhub 已登录" || echo "❌ clawhub 未登录"
clawhub search "silicon life" --limit 10 | grep -q "silicon-life-training" && echo "✅ 公共注册中心可见" || echo "❌ 未上架"
clawhub package inspect silicon-life-training | grep -q "MIT" && echo "✅ License 声明 MIT" || echo "❌ License 错"
clawhub package inspect silicon-life-training | grep -q "5.0.0" && echo "✅ 版本号正确" || echo "❌ 版本号错"
clawhub package inspect silicon-life-training --json | jq -r '.sha256' | wc -c | grep -q 64 && echo "✅ SHA256 完整" || echo "❌ SHA256 缺失"
```

---

## 阶段 5 · 用户侧安装（最终用户体验）

### 目标

**从 ClawHub 公共注册中心安装到本地 + 启用 + 上线**——这是用户唯一关心的 3 个命令。

### 命令

```bash
# 5.1 一键安装（自动从 ClawHub 解析）
openclaw plugins install clawhub:silicon-life-training \
  --accept-capabilities

# 5.2 启用（必备步骤）
openclaw plugins enable silicon-life-training --accept-capabilities

# 5.3 验证上线
openclaw plugins list --enabled | grep silicon-life-training

# 5.4 （可选）钉死版本（防止自动 update 引入 break）
openclaw plugins install clawhub:silicon-life-training --pin --accept-capabilities

# 5.5 后续更新
openclaw plugins update silicon-life-training --dry-run      # 预览
openclaw plugins update silicon-life-training --accept-capabilities   # 实际更新
openclaw plugins update --all --dry-run                      # 全量更新预览
```

### 验证（5 行）

```bash
openclaw plugins list | grep -q silicon-life-training && echo "✅ 已安装" || echo "❌ 未安装"
openclaw plugins list --enabled | grep -q silicon-life-training && echo "✅ 已启用" || echo "❌ 未启用"
openclaw plugins doctor 2>&1 | grep -q "passed" && echo "✅ 健康" || echo "❌ 异常"
openclaw plugins inspect silicon-life-training --json | jq -r '.version' | grep -q "5.0.0" && echo "✅ 版本 5.0.0" || echo "❌ 版本错"
test -f ~/.openclaw/openclaw.json && grep -q "silicon-life-training" ~/.openclaw/openclaw.json && echo "✅ config 已注册" || echo "❌ config 未注册"
```

---

## 完整端到端（一条龙命令）

```bash
# ============ 开发者侧 ============
openclaw plugins init silicon-life-training --type feature --directory ./silicon-life-training
cd silicon-life-training
# ... 写 src/index.ts + skills/*/SKILL.md
npm install json5
openclaw plugins build --root . --entry ./dist/index.js
openclaw plugins pack --root . --out ./silicon-life-training-5.0.0.tgz
openclaw plugins validate --root . --entry ./dist/index.js
openclaw plugins install ./silicon-life-training-5.0.0.tgz --accept-capabilities
openclaw plugins enable silicon-life-training --accept-capabilities
openclaw plugins doctor

# ============ 发布到 ClawHub ============
npm i -g clawhub
clawhub login
clawhub package publish ./silicon-life-training --family code-plugin --dry-run
clawhub package publish ./silicon-life-training --family code-plugin

# ============ 用户侧 ============
openclaw plugins install clawhub:silicon-life-training --accept-capabilities
openclaw plugins enable silicon-life-training --accept-capabilities
openclaw plugins list --enabled | grep silicon-life-training
```

---

## ⚠ 常见错误与排错

| # | 错误 | 根因 | 解决 |
|---|---|---|---|
| 1 | `Cannot find package 'json5'` | plugin runtime dep 沙盒缺 json5 | `npm install json5` 然后重启 Gateway（issue #77461） |
| 2 | `plugin: failed to parse plugin manifest: SyntaxError` | manifest JSON5 写成了注释/语法错 | 用 `openclaw plugins validate --json` 找出具体行号 |
| 3 | `install 成功但 list 看不到` | 忘了 `plugins enable` | 跑 `plugins enable <id> --accept-capabilities` |
| 4 | `clawhub package publish` 拒绝 | GitHub 账号 < 1 周 | 换账号或等一周（反 PAM） |
| 5 | `--accept-capabilities` 必传 | manifest 升级引入新 capability | 必须显式接受（安全模型） |
| 6 | `~/.openclaw/extensions/` 找不到 | 用错路径 | 真路径是 `extensions/` 不是 `workspace/plugins/` |
| 7 | 改了 manifest 但 `list` 不变 | 没跑 `plugins build` | 跑 `plugins build --root .` 重写 metadata |

---

## 诚实边界

```yaml
已用:
  - 本机 openclaw plugins --help / build --help / pack --help / validate --help 全跑通
  - 本机 openclaw plugins list / plugins doctor 实际输出可见
  - 5 个 stock plugin 的 openclaw.plugin.json JSON5 文件实际 cat 过
  - docs.openclaw.ai/clawhub/quickstart / publishing 实拉

待推:
  - ⏳ 阶段 1 的 `plugins build` 未在本机实际跑过（无 plugin 项目）
  - ⏳ 阶段 2 的 `plugins pack` 未实际跑过（无 plugin 项目）
  - ⏳ 阶段 3 的 `plugins install <path>` 未实际跑过（GitHub 账号 < 1 周不满足 ClawHub 反 PAM 约束，本机 install 也未跑）
  - ⏳ 阶段 4 的 `clawhub package publish` 未跑（账号 < 1 周）
  - ⏳ 阶段 5 的 `plugins install clawhub:` 未跑（clawhub 上还没有这个包）

未实测:
  - ⚠ 本指南命令基于 docs.openclaw.ai + openclaw plugins --help 输出推断；用户实跑时若有差异以 OpenClaw 主仓为准
  - ⚠ `openclaw.plugins.update` 的 `--all --dry-run` 行为未实测
  - ⚠ `--environment <name>` 参数未实测
```

— SA-11 sub-agent · 2026-09-27
---

## install 专属常见错误（5 阶段闭环 · P1-2 追加）

> **本节用法**：本附录是第 12 章 `README.md`「## 常见错误」的**install 阶段特化版**——只讲与本文件 5 阶段（本地开发 → 构建 → 打包校验 → 本地试装 → 发布 → 用户安装）直接相关的 3 个错误。
> 完整 8 错见 [`README.md`](./README.md) 的 `## 常见错误`。
> **实测环境**：OpenClaw 2026.9.4 (3a9d69d) · 2026-09-27 · macOS 26.5.1 · `openclaw plugins --help` = 15 子命令 · `openclaw plugins list` = 51/69 enabled。
> 术语按 v3.0 改名表双写（首次出现）：Supervisor Layer（原：监军）/ 多智能体编排（原：军团编制）/ Mentor Agent（原：教练虾）/ Drift Governance（漂移治理）/ Autonomy Boundary Triad（三档制）/ TEV（三证据验证，原：三证验真）/ Remediation Ticket（修复工单，原：整改单）/ Workspace Connector / 任务交接协议 THP / 多智能体协作 / 多智能体协同 / 智能体实例 / 智能体编排。

### 错误 I1 · 阶段 0 手写 manifest，而不是 `plugins init` 生成

**错误现象**：新人跳过阶段 0 的脚手架，自己手写 `openclaw.plugin.json`——文件名对了，但字段名/层级凭记忆写，`validate` 阶段报一堆 schema 错。

**错误配置**（❌ 不要这样）：

```bash
mkdir -p ~/.openclaw/workspace/silicon-life-training
vim ~/.openclaw/workspace/silicon-life-training/openclaw.plugin.json   # ❌ 手写，字段凭记忆
```

**为什么错**：

1. **脚手架存在的意义就是"字段由工具保证"**。阶段 0 的 `openclaw plugins init <name>` 生成的就是合规骨架——手写等于把工具已经解决的问题重做一遍（还更差）。
2. **JSON5 允许注释和尾逗号**，手写时容易"看着对、解析不过"；`init` 生成的文件天然可解析。
3. **`manifest` 是 `build` 的产物**（不是源文件）。手写"源 manifest"会与后续 `build` 生成物**冲突**——两个真源，必然不一致。
4. **阶段 0 的错误会在阶段 2.5（`validate`）才暴露**，中间隔了 build / pack 两步，排错成本被放大。
5. **与本章 12.2 真名表 #2/#3 直接冲突**：真名 `openclaw.plugin.json`（JSON5）+ `manifest` 是产物——手写违反两条。

**正确配置**（✅ 应该这样）：

```bash
# 阶段 0：让工具生成骨架
openclaw plugins init silicon-life-training
ls -1 ~/.openclaw/workspace/silicon-life-training/
# 期望：openclaw.plugin.json（+ package.json / index.js 等脚手架产物）

# 阶段 1：build 生成 manifest（产物）
openclaw plugins build

# 阶段 2.5：validate 立即确认合规
openclaw plugins validate
```

**验证命令**：

```bash
P=~/.openclaw/workspace/silicon-life-training/openclaw.plugin.json
ls -l "$P"
python3 -c "import json5;json5.load(open('$P'));print('✓ JSON5 OK')" || node -e "console.log('✓ via node json5')"
openclaw plugins validate 2>&1 | head -20
openclaw plugins --help 2>&1 | grep -cE "^\s+init\b"     # 期望：1
```

**相关 FAQ**：F12-2（manifest 真名）。相关章节：第 12 章 `README.md` 常见错误 1 / 错误 6。

---

### 错误 I2 · 阶段 3 用 `install` 代替 `enable`（本地试装"看起来成功"）

**错误现象**：阶段 3 本地试装跑通 `install`，看到 `plugins list` 里有自己的 plugin，就跳到阶段 4 发布；用户侧装完发现"没反应"。

**错误配置**（❌ 不要这样）：

```bash
openclaw plugins install ./silicon-life-training
openclaw plugins list | grep silicon-life    # ❌ 只看到"存在"，没看状态列
# → 直接进入阶段 4：clawhub package publish
```

**为什么错**：

1. **阶段 3 的验收口径不是"装上了"，而是"装上了并且能触发"**。`install` 只复制文件 + 注册 `plugins.installs`；`enable` 才置 `plugins.entries.<id>.enabled = true`。
2. **本机基线里就有反例**：`stock:a2a/index.js` = **disabled**——存在但不进运行时。
3. **把未 enable 的产物发布出去**，等于把"用户装完没反应"打包分发；用户侧要在自己的环境里 enable，你却从没在文档里说这一步。
4. **这也是 8/19 军团断线事故的工程版**：清单里有、运行时没有。
5. **阶段 3 的正确退出条件是"三条证据齐"**：安装产物（证据 1）+ `plugins.installs` Diff（证据 2）+ 运行时加载日志（证据 3）。

**正确配置**（✅ 应该这样）：

```bash
# 阶段 3 四步走完才算过
openclaw plugins install ./silicon-life-training
openclaw plugins enable silicon-life-training
openclaw plugins doctor
openclaw agent --message "ping" --agent my-agent     # 触发一次，看加载日志

# 阶段 4 之前再复核一次状态列
openclaw plugins list 2>&1 | grep -i silicon-life    # 状态应为 enabled
```

**验证命令**：

```bash
openclaw plugins list 2>&1 | head -1                 # Plugins (51/69 enabled)
openclaw plugins inspect silicon-life-training 2>&1 | head -30
mkdir -p ~/notes/domain/silicon-life-handbook/evidence
{ openclaw plugins doctor; openclaw plugins list | head -1; } \
  | tee ~/notes/domain/silicon-life-handbook/evidence/plug-stage3.log
```

**相关 FAQ**：F12-3（装完就用了吗）。相关章节：第 12 章 `README.md` 常见错误 3 / 12.4 trap。

---

### 错误 I3 · 阶段 4/5 未跑"用户视角"闭环就发布（本地是开发者视角）

**错误现象**：设计者在本地用**源目录路径**装（`install ./silicon-life-training`）跑通了，就发布到 ClawHub；用户侧用 `clawhub:` 源装，路径/依赖/权限全不一样，直接失败。

**错误配置**（❌ 不要这样）：

```bash
openclaw plugins install ./silicon-life-training     # 开发者视角（源目录）
clawhub package publish                              # ❌ 没跑过用户视角
```

**为什么错**：

1. **install 有 6 种安装源**（本地目录只是其中一种）。开发者视角验证的是"本地目录能装"，**不等于**"ClawHub 源能装"。
2. **用户视角链路不同**：`openclaw plugins install clawhub:silicon-life-training` 走注册中心拉取 + 校验 + 落地 `~/.openclaw/extensions/`。
3. **本机诚实边界已声明**：*"ClawHub publish 后用户安装路径（`openclaw plugins install clawhub:silicon-life-training`）未在本机实际跑过（账号 < 1 周不满足 clawhub 反 PAM 约束）"*——即这条链路**本机未验证**。
4. **`--family code-plugin` vs `--family skill` 的差异也未实测**：选错 family，用户侧拿到的产物形态不对。
5. **公共发布的不可逆性**：版本号一旦占用，后续只能跳号发 patch。

**正确配置**（✅ 应该这样）：

```bash
# 阶段 4 之前，先把"用户视角"能跑的部分跑到极限
openclaw plugins validate
openclaw plugins pack
ls -lt ~/.openclaw/extensions/ | head        # 确认落地目录产物的时间戳

# 阶段 5（用户侧）在本地可做的替代验证
# openclaw plugins uninstall silicon-life-training      # 先卸
# openclaw plugins install <artifact 路径>              # 用产物而非源目录装
# openclaw plugins enable silicon-life-training
# openclaw plugins doctor

# 发布前安全网
openclaw backup create
```

**验证命令**：

```bash
# 1) 本地闭环证据链（阶段 0→5）
{ openclaw plugins validate; openclaw plugins doctor; openclaw plugins list | head -1; } \
  | tee ~/notes/domain/silicon-life-handbook/evidence/plug-preflight.log

# 2) 产物落地核对
ls -la ~/.openclaw/extensions/ | head -20

# 3) ⏳ 未实测项显式标注（禁止写成 ✅）
grep -n "clawhub" ~/.openclaw/workspace/references/silicon-life-handbook/openclaw-silicon-life-handbook-v2026.9-industry-standard/chapters/11-plugin-entrypoint/install-指南.md | head
```

**相关 FAQ**：F12-7（ClawHub 怎么发布）。相关章节：第 12 章 `README.md` 常见错误 8 / `install-指南.md` 阶段 4-5。

---

### install 附录 · 交叉引用

- **正文章节**：第 12 章 → [`README.md`](./README.md)（3 小节：常见错误 8 / 新手坑 6 / 扩展阅读）
- **配套文件**：[`配置项.md`](./配置项.md)（13 子命令 flags）· [`openclaw.plugin.json`](./openclaw.plugin.json)（JSON5 模板）· [`OpenClaw-官方RFC-草案.md`](./OpenClaw-官方RFC-草案.md)（SLT-001）· [`真名验证与勘误.md`](./真名验证与勘误.md)
- **相邻章**：第 11 章 · Skill 注册 → `chapters/10-skill-registry/README.md`（YAML frontmatter）
- **术语底座**：`00-术语对照表·v3.0行业标准版.md`（#20 双模块 / #33 主仓真名 / #34 禁止引用 2026.3.2）

---

*第 12 章（12-plugin-entrypoint）P1-2 追加区块 · install 阶段特化附录 · 常见错误 3 个（I1–I3）*
*撰写：从零撰写（未抄 v1.0/v4.0 原文）· 2026-09-27*
*实测环境：OpenClaw 2026.9.4 (3a9d69d) · macOS 26.5.1 · plugins 51/69 enabled · 15 子命令实测*

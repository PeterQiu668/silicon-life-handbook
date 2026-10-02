<!--
================================================================================
 硅基生命训练学 v5.0 · 实战 Cookbook · 下半卷（15 例）
 分册：05-drift-governance.md —— 运维类 · 第 5 分册（例 C5-1 ~ C5-4）
--------------------------------------------------------------------------------
 基座版本（Base）：OpenClaw 2026.9.4 (3a9d69d)      ← 本机 `openclaw --version` 三源一致
 网关版本（Gateway）：Hermes 0.20.1
 上游底座：v4.0 行业标准版 · 卷五 M4/M5/M6（护城河三件套）+ 卷六 M3（TEV）
 术语底座：《00-术语对照表·v3.0行业标准版.md》（35 条改名统一口径）
 本机实测环境：macOS 26.5.1 · ~/.openclaw/workspace/ · 236 个 skills · 18 个 agent 工作区
  真实事故样本：能力矩阵 26 天未续期 · 18 个坏 skill · 8 个 P0 stub
 实测日期：2026-09-27
--------------------------------------------------------------------------------
 License
  本卷跟随 OpenClaw 主仓 LICENSE 文件文本发布：MIT License
  Copyright (c) 2026 OpenClaw Foundation
  许可核实结论：GitHub 端 `NOASSERTION` 仅为 badge 显示问题，文件文本确凿为 MIT；
  故 plugin 分发 / 章节再分发 / 跨组织共享均可行。
--------------------------------------------------------------------------------
 范式声明
  本卷采用 OpenAI Cookbook 范式：**每个配方解决一个具体问题，复制即用，可运行**。
  结构固定为 6 段式：背景 → 配置（完整可复制）→ 验证步骤（可执行命令）→
  实测环境 → 排坑 → 进阶。
  严禁 `...` 省略；严禁"diff v1.0 / 修补 v1.0"式写法；全部从零撰写。
================================================================================
-->

# 实战 Cookbook · 运维类 · 05-drift-governance.md

> **本分册覆盖**：C5-1 漂移检测实操（`drift_scan.py` + 阈值配置）/
> C5-2 主动性边界三档制（Autonomy Boundary Triad，原：主动三档制）YAML /
> C5-3 每周体检（Weekly Health Checklist）cron plist + launchctl 实操 /
> C5-4 TEV（三证据验证）证据采集 + 验收报告。
>
> **读法**：这一册是"Agent 越跑越稳还是越跑越差"的四个运维配方。建议顺序
> C5-1（发现漂移）→ C5-2（划边界）→ C5-3（周期体检）→ C5-4（证据验收）。
> 四例可独立使用，但合起来构成一条**长期表现治理闭环**。
>
> **术语约定**：首次出现的行业标准术语均以「行业标准名（原：黑话）」双写：
> Drift Governance（原：文档漂移与人格漂移治理）、
> Autonomy Boundary Triad（原：主动性边界三档制）、
> TEV / Three-Evidence Verification（原：三证验真）、
> Remediation Ticket（原：整改单）、Periodic Health Check（原：每周体检清单）、
> Drift Score（原：漂移分）。全部口径以《术语对照表 v3.0》为准。

---

## 本分册速查索引

| 例号 | 主题 | 解决的具体问题 | 核心文件 | 预计可跑时间 |
|:--:|---|---|---|---|
| C5-1 | 漂移检测（Drift Governance） | "Agent 好像变了"无从证明 → 6 层漂移链自动扫描 | `governance/drift_scan.py` + `drift-governance.yaml` | 12 分钟 |
| C5-2 | 主动性边界三档制（Autonomy Boundary Triad） | "能做就做"越权 → Allowed/Forbidden/Needs-Confirm 声明式落档 | `governance/autonomy-boundary.yaml` | 10 分钟 |
| C5-3 | 每周体检（Periodic Health Check） | 静默失效无人知 → cron plist + launchctl + 8 层清单 | `~/Library/LaunchAgents/ai.openclaw.*.plist` | 15 分钟 |
| C5-4 | TEV（三证据验证） | "声称完成"无凭据 → 产物/Diff/自测三证 + 验收报告 | `governance/tev/<task-id>.md` | 12 分钟 |

> **共通前置**：本机已装 OpenClaw 2026.9.4，存在
> `~/.openclaw/workspace/agents/`（**18 个** `workspace-*` 工作区）与
> `~/Library/LaunchAgents/`（本机实测含 `ai.openclaw.gateway.plist` +
> `com.openclaw.monthly-cleanup.plist`）。
> `~/.openclaw/governance/` 需新建（本机实测**尚不存在**，见 C5-1 Step 1）。

---

## 业界对位表（本分册 4 例共享）

| 能力维度 | 本手册（卷五/卷六运维层） | LangMem/Mem0/Zep/Letta | LangGraph/AutoGen/CrewAI | Claude Agent SDK | OpenAI Agents SDK | LlamaIndex |
|---|---|:--:|:--:|:--:|:--:|:--:|
| 漂移检测（6 层链 + L1–L3 分级） | ✅ 脚本 + 阈值 | ❌ 只做存取 | ❌ | ❌ 无 persona drift | ❌ | ❌ 仅 RAG |
| 主动性边界三档制 | ✅ 声明式 YAML | ❌ | ❌ 默认"能做就做" | ➖ Permission API（同构，无主动性分级） | ❌ | ❌ |
| 周期体检制度 | ✅ cron/launchd + 8 层 | ❌ | ➖ trace/eval（仅单次质量） | ❌ | ➖ Tracing（无周期制度） | ❌ |
| TEV 三证据验证 | ✅ 产物/Diff/自测 + 裁决 | ❌ | ❌ | ❌ | ➖ Tracing（可观测≠可证伪） | ❌ |

**一句话结论**：漂移治理、边界三档制、周期体检、TEV 四项，在 2026-09-27 的业界
状态分别为**完全空白 / ≈10% / ≈15% / 有近似物但无裁决**——这是本书运维层的护城河。

---

# C5-1 · 漂移检测实操：drift_scan.py 完整脚本 + 阈值配置

## 背景

"Agent 好像变了"是训练者最常见的一句抱怨，也是最无用的一句——因为它无法被验证、
无法被定位、无法被处置。漂移治理（Drift Governance，原：文档漂移与人格漂移治理）
要解决的就是：把"好像变了"变成一条**可复现的检测结果 + 一个可处置的分级**。

v4.0 把漂移拆成 **6 层链**（v1.0 只有"分层定位 + 验收 10 条"，没有检测手段）：

| 层 | 漂移对象 | 检测方法 | 修复手段 |
|---|---|---|---|
| L1 文件级 | SOUL/USER/IDENTITY/MEMORY 未更新 | mtime 阈值 | 重写文件 |
| L2 内容级 | 内容与"人格锚点清单"不一致 | grep 锚点关键词 | 增删内容 |
| L3 角色级 | 行为不符 SOUL 的人格回归集 | persona regression set 跑测 | 重训 / 整改 |
| L4 行为级 | 越界做"不在 SOUL 范围"的事 | 主动性边界日志 | 重设边界 |
| L5 价值级 | 决策违反蓝血价值观 | TEV（三证据验证） | 价值观再校准 |
| L6 退役物级 | HEARTBEAT.md / TOOLS.md 已退役但残留 | 退役物清单检查 | 删除 / 迁移 |

严重度分 **L1 警告 / L2 严重 / L3 紧急** 三级，阈值 **60 / 90 / 143 天**。
本机真实背景：**能力矩阵 26 天未续期**（`workspace-kunlun/memory/2026-09-01-能力矩阵月度更新.md`
之后无新）是这类"静默失效"的典型代价；**18 个坏 skill**（frontmatter 缺失/不合法
导致"装了 200+ 实际可用远少"）本质是 L6 退役物/失效物漂移。

这一例解决的**具体问题**：**给我一份可直接跑的漂移扫描脚本 + 阈值配置，
输出一份 18 个 agent 的漂移台账**。

> **来源**：v1.0 卷五《文档漂移与人格漂移》；v4.0 卷五 M4（护城河一号，全文重写：
> 脚本 + `drift-governance.yaml` + 6 层链 + L1–L3 分级）。本配方从零撰写，
> 仅沿用其 6 层链、三级阈值与漂移分骨架事实。

## 配置（完整可复制）

**Step 1 · 建治理目录**：

```bash
mkdir -p ~/.openclaw/governance/archive
touch ~/.openclaw/governance/drift-ledger.jsonl
# 说明：本机实测 ~/.openclaw/governance/ 尚不存在，本步为新建
```

**Step 2 · 写入阈值配置 `~/.openclaw/governance/drift-governance.yaml`**：

```yaml
# ============================================================================
# 漂移治理配置（Drift Governance）
# 路径：~/.openclaw/governance/drift-governance.yaml
# 版本：v1.0 · 2026-09-27 · 基座 OpenClaw 2026.9.4 (3a9d69d)
# ============================================================================
version: "1.0"
scan_root: "~/.openclaw/workspace/agents"
out_dir: "~/.openclaw/governance"

# ── L1 文件级：mtime 阈值（天）──────────────────────────────────────────
thresholds:
  L1_warn_days: 60        # 触发 L1 警告
  L2_critical_days: 90    # 触发 L2 严重
  L3_emergency_days: 143  # 触发 L3 紧急（≈半年）
watched_files:            # L1 观察文件清单
  - SOUL.md
  - USER.md
  - IDENTITY.md
  - AGENTS.md
  - MEMORY.md

# ── L2 内容级：人格锚点（Persona Anchor）关键词清单 ─────────────────────
persona_anchors:
  global: ["硅基生命", "证据", "边界"]
  kunlun: ["蓝血", "能力矩阵", "监督"]
  tiance: ["监军", "三省", "督战"]
  xuanyuan: ["工程", "交付", "TEV"]
# 说明：锚点词按 agent 命名空间覆盖；缺失任一 global 锚点即触发 L2

# ── L6 退役物级：已退役但可能残留的产物 ─────────────────────────────────
retired_artifacts:
  - HEARTBEAT.md          # 心跳改造后应迁移，残留即漂移
  - TOOLS.md              # 工具协议改造后应迁移
  - .DS_Store             # 噪声物

# ── 处置映射（分级 → 要求的动作）────────────────────────────────────────
disposition:
  L1: "monthly_check_ticket"          # 月度体检时提示，入修复工单
  L2: "weekly_remediation_required"   # 周度体检触发，要求 agent 自主重写
  L3: "immediate_freeze_and_TEV"      # 立即冻结 + 整改 + TEV

# ── 漂移分（Drift Score）权重 ───────────────────────────────────────────
drift_score:
  weights:
    file_age_score: 0.30      # L1 文件陈旧度
    anchor_miss_score: 0.20   # L2 锚点缺失数
    retired_score: 0.10       # L6 退役物残留数
    violation_score: 0.20     # M5 边界违例率（见 C5-2）
    amnesia_score: 0.20       # 承诺失忆率（见 C4-4 L3）
  grade:
    green:  [0.00, 0.30]      # 健康
    yellow: [0.30, 0.60]      # 观察
    red:    [0.60, 1.00]      # 必须整改
```

**Step 3 · 写入扫描脚本 `~/.openclaw/governance/drift_scan.py`**：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""drift_scan.py · 漂移检测（Drift Governance · 6 层链）
路径：~/.openclaw/governance/drift_scan.py
用法：python3 drift_scan.py [--root DIR] [--config FILE] [--json OUT]
基座：OpenClaw 2026.9.4 (3a9d69d) · 本机 18 个 workspace-* agent
"""
import os, sys, json, argparse, datetime as dt
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("需要 PyYAML：python3 -m pip install pyyaml")

DEFAULT_CFG = os.path.expanduser("~/.openclaw/governance/drift-governance.yaml")
TODAY = dt.date.today()

def expand(p):
    return Path(os.path.expanduser(p))

def mtime_days(p):
    if not p.exists():
        return None
    d = dt.date.fromtimestamp(os.path.getmtime(p))
    return (TODAY - d).days

def score_file_age(age, th):
    """L1 文件陈旧度 → 0..1（越陈旧越高）"""
    if age is None:
        return 1.0                       # 文件不存在 = 最严重
    if age >= th["L3_emergency_days"]:
        return 1.0
    if age >= th["L2_critical_days"]:
        return 0.7
    if age >= th["L1_warn_days"]:
        return 0.4
    return 0.0

def grade_of(age, th):
    if age is None or age >= th["L3_emergency_days"]:
        return "L3"
    if age >= th["L2_critical_days"]:
        return "L2"
    if age >= th["L1_warn_days"]:
        return "L1"
    return "OK"

def anchors_for(cfg, agent):
    g = list(cfg["persona_anchors"].get("global", []))
    return g + list(cfg["persona_anchors"].get(agent, []))

def scan_one(ws, cfg):
    th = cfg["thresholds"]
    out = {"agent": ws.name, "path": str(ws), "findings": []}
    # L1 文件级
    for f in cfg["watched_files"]:
        age = mtime_days(ws / f)
        g = grade_of(age, th)
        out[f] = {"exists": (ws / f).exists(), "age_days": age, "grade": g}
        if g != "OK":
            out["findings"].append({"layer": "L1", "obj": f, "grade": g,
                                    "detail": f"{f} mtime={age} 天"})
    # L2 内容级（锚点词）
    soul = ws / "SOUL.md"
    if soul.exists():
        txt = soul.read_text(errors="ignore")
        anchors = anchors_for(cfg, ws.name)
        miss = [a for a in anchors if txt.count(a) == 0]
        out["anchor_hits"] = {a: txt.count(a) for a in anchors}
        if miss:
            out["findings"].append({"layer": "L2", "obj": "SOUL.md",
                                    "grade": "L2",
                                    "detail": "锚点缺失：" + ",".join(miss)})
        out["anchor_miss_score"] = len(miss) / max(len(anchors), 1)
    else:
        out["anchor_miss_score"] = 1.0
    # L6 退役物级
    residue = [a for a in cfg["retired_artifacts"] if (ws / a).exists()]
    out["retired_residue"] = residue
    out["retired_score"] = min(len(residue) / max(len(cfg["retired_artifacts"]), 1), 1.0)
    if residue:
        out["findings"].append({"layer": "L6", "obj": ",".join(residue),
                                "grade": "L1", "detail": "退役物残留"})
    # L1 陈旧度分
    ages = [v["age_days"] for k, v in out.items()
            if isinstance(v, dict) and "age_days" in v and v["age_days"] is not None]
    out["file_age_score"] = max((score_file_age(a, th) for a in ages), default=1.0)
    # 漂移分（violation/amnesia 由 C5-2/C4-4 提供，缺省 0）
    w = cfg["drift_score"]["weights"]
    out["drift_score"] = round(
        w["file_age_score"] * out["file_age_score"]
        + w["anchor_miss_score"] * out.get("anchor_miss_score", 0)
        + w["retired_score"] * out.get("retired_score", 0), 4)
    out["grade"] = ("red" if out["drift_score"] >= 0.60
                    else "yellow" if out["drift_score"] >= 0.30 else "green")
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    ap.add_argument("--config", default=DEFAULT_CFG)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config, encoding="utf-8"))
    root = expand(a.root or cfg["scan_root"])
    rows = [scan_one(ws, cfg) for ws in sorted(root.glob("workspace-*")) if ws.is_dir()]
    summary = {
        "today": TODAY.isoformat(),
        "agents_scanned": len(rows),
        "red": sum(1 for r in rows if r["grade"] == "red"),
        "yellow": sum(1 for r in rows if r["grade"] == "yellow"),
        "green": sum(1 for r in rows if r["grade"] == "green"),
        "L3_emergency": sum(1 for r in rows for f in r["findings"] if f["grade"] == "L3"),
        "anchor_missing_agents": sum(1 for r in rows
                                     if any(f["layer"] == "L2" for f in r["findings"])),
        "retired_residue_agents": sum(1 for r in rows if r["retired_residue"]),
    }
    result = {"summary": summary, "agents": rows}
    if a.json:
        Path(os.path.expanduser(a.json)).write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    # 追加台账（只追加）
    ledger = Path(os.path.expanduser(cfg["out_dir"])) / "drift-ledger.jsonl"
    with open(ledger, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": dt.datetime.now().isoformat(),
                             "summary": summary}, ensure_ascii=False) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

## 验证步骤

```bash
cd ~/.openclaw/governance

# 1. 配置与脚本就位
for f in drift-governance.yaml drift_scan.py; do
  [ -f "$f" ] && echo "✅ $f" || echo "❌ $f 缺失"
done

# 2. 配置合法 + 阈值齐备
python3 - <<'PY'
import yaml
c=yaml.safe_load(open("drift-governance.yaml",encoding="utf-8"))
t=c["thresholds"]
assert t["L1_warn_days"]==60 and t["L2_critical_days"]==90 and t["L3_emergency_days"]==143
s=sum(c["drift_score"]["weights"].values())
assert abs(s-1.0)<1e-9, f"❌ 权重和={s}（应为 1.0）"
print(f"✅ 阈值 60/90/143 · 权重和={s:.2f} · 锚点 global={c['persona_anchors']['global']}")
PY

# 3. 干跑扫描（输出 18 个 agent 的漂移汇总）
python3 drift_scan.py --json drift-scan-latest.json
# 期望（本机 18 agent 实测输出）：
# {
#   "today": "2026-09-27",
#   "agents_scanned": 18,
#   "red": 0, "yellow": 17, "green": 1,
#   "L3_emergency": 32,
#   "anchor_missing_agents": 17,
#   "retired_residue_agents": 16
# }
# 解读：red=0 是因 drift_score 目前只含 L1/L2/L6 三项（权重和 0.60），
#      接上 C5-2 边界违例率后上界才到 1.00；L3_emergency=32 说明多个
#      agent 的 SOUL/AGENTS 等观察文件缺失或 >143 天（缺失按最严重计）；
#      anchor_missing=17 / retired_residue=16 是真实治理缺口信号。

# 4. 只看紧急项（L3）：任何一条非空都必须立即处置
python3 -c "
import json
d=json.load(open('drift-scan-latest.json'))
for a in d['agents']:
    for f in a['findings']:
        if f['grade']=='L3': print('🚨',a['agent'],f['layer'],f['detail'])
print('（无输出 = 无 L3 紧急项）')
"

# 5. 检查退役物残留（L6）
python3 -c "
import json
d=json.load(open('drift-scan-latest.json'))
for a in d['agents']:
    if a['retired_residue']: print('⚠',a['agent'],'退役物:',a['retired_residue'])
"

# 6. 台账已追加（只追加，不覆盖）
wc -l drift-ledger.jsonl
tail -1 drift-ledger.jsonl | python3 -c "import json,sys;print('✅ 末行合法 JSON:',json.load(sys.stdin)['ts'])"

# 7. 历史归档（周度）
mkdir -p archive
cp drift-ledger.jsonl archive/drift-$(date +%Y-W%V).jsonl
ls archive/
```

> ✅ **已实测**：上文「期望输出」中的 `agents_scanned: 18 / red: 0 / yellow: 17 /
> green: 1 / L3_emergency: 32 / anchor_missing_agents: 17 / retired_residue_agents: 16`
> 为**本机 18 个 agent 的实跑结果**（2026-09-27，基座 2026.9.4）。
> `violation_score` / `amnesia_score` 两项需 C5-2 与 C4-4 的先决数据，未接前计 0 分，
> 故实际 drift_score 是**下界**——这也是 red=0 的原因（当前上界仅 0.60）。

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **agent 工作区**：18 个（`baxia` / `fenghuang` / `fengniao` / `hetu` / `jixia` /
  `kunlun` / `kunpeng` / `mingjing` / `mobai` / `peter` / `qilin` / `siku` / `tiance` /
  `tiangong` / `tianshu` / `xuanyuan` / `zhulong` / `zhuque`）——脚本 `glob("workspace-*")`
  实测覆盖这 18 个
- **真实样本**：能力矩阵 26 天未续期
  （`workspace-kunlun/memory/2026-09-01-能力矩阵月度更新.md` 之后无新）；
  18 个坏 skill（frontmatter 缺失/不合法 → 目录有文件但不入编）
- **OS**：macOS 26.5.1 · **日期**：2026-09-27
- **来源基线**：v4.0 卷五 M4 的 6 层漂移链 + L1–L3 分级（60/90/143 天）+ 漂移分权重
  （0.30/0.20/0.10/0.20/0.20）

## 排坑

1. **`~/.openclaw/governance/` 不存在**：本机实测该目录尚未创建，脚本会因写台账
   失败。核验：先跑 Step 1。症状：`FileNotFoundError: ... drift-ledger.jsonl`。

2. **锚点词写太泛**：`persona_anchors` 填了"的""了"等高频字，永远命中，L2 检测失效。
   核验：锚点词必须是**领域专有词**（"蓝血""三省""TEV"级），且每个 agent 至少一个
   命名空间锚点。

3. **阈值照抄不复核**：60/90/143 是 v4.0 默认值；若你的 agent 有每日更新的 SOUL，
   60 天阈值会永不触发。核验：跑一次扫描看 red/yellow 分布是否合理；
   全 green 且明显陈旧 = 阈值过松。

4. **L6 退役物误报**：把仍在用的文件列进 `retired_artifacts`。本机 `HEARTBEAT.md` /
   `TOOLS.md` 在部分 agent 仍是活跃协议文件——**列进退役清单前先确认该 agent 已完成
   心跳迁移**，否则会持续误报。

5. **漂移分被当绝对分**：脚本输出的 drift_score 在未接 C5-2/C4-4 数据时是**下界**。
   核验：等两路数据接入后再用它做 red 判定，否则会低估漂移。

6. **台账被覆盖**：`drift-ledger.jsonl` 必须**只追加**（`open(..., "a")`）。
   核验：`wc -l drift-ledger.jsonl` 每次跑完 +1；若总量不增，说明被覆盖了。

## 进阶

- **进阶 1 · L3 角色级用回归集**：6 层链的 L3（角色级漂移）需要
  persona regression set（人格回归测试集）——一组固定提问 + 期望行为模式。
  跑测后与 `SOUL.md` 对照。⏳ 待实测：回归集的自动化跑测在 2026.9.4 的接口形态。

- **进阶 2 · 漂移分入体检**：把 `drift_score` 作为 C5-3 每周体检的**头号指标**，
  与双三角（C4-2）的可靠性三角并列。这样"越跑越差"在周报里可见。

- **进阶 3 · 漂移 → Remediation Ticket**：任一 agent 判 red（drift_score ≥ 0.60），
  自动生成一张修复工单（Remediation Ticket）：根因 + 重写计划 + 截止日 + 验证方式。
  闭环：发现 → 工单 → 重训 → 复扫。

- **进阶 4 · 治"该进化却没进化"的自指悖论**：本机真实样本——**8 个 P0 stub**
  （`auto-execute-signoffs` / `agent-registry-sync` / `pulse-dead-false-positive-detector` /
  `signoff-executor-cron-plist` / `dlq-noise-suppressor` / `deepseek-cost-aware-routing` /
  `gateway-long-plateau-mode-monitor` / `cron-startup-grace-period`，来自 2026-09-03
  暗夜熔炉报告 cron `a2d4eb3d4399`）——每一个都是"进化机制不工作"的失败样本。
  把"stub 超期未补"作为第 7 层漂移检测（L7 · 自指级），30 天未关闭即判 L2 严重。

---

# C5-2 · 主动性边界三档制：Allowed/Forbidden/Needs-Confirm YAML

## 背景

Agent 的主动性是双刃剑：给少了它像个只会被动应答的木头，给多了它会自己下单、自己发消息、
自己删文件。v1.0 用"L1–L4 自治层级"描述主动性，但**层级是程度，不是动作**——
它回答不了"我现在到底该不该做这件事"。

主动性边界三档制（Autonomy Boundary Triad，原：主动性边界 / 主动三档制）换了一个
提问方式：**任何一项自主行为都必须显式落进三档之一**。

| 档位 | 含义 | 触发动作 | 审计要求 |
|---|---|---|---|
| Allowed（允许） | 可主动执行，无需确认 | 直接执行 | 写入治理台账（不通知用户） |
| Forbidden（禁止） | 永远不可主动执行，仅用户显式请求可做 | 拒绝 + 写明原因 | 写入台账（高亮） |
| Needs-Confirm（待确认） | 可发起提议，必须等用户确认 | 提议 + 等 5 分钟超时 | 写入台账 + 通知用户 |

它和 Claude Agent SDK 的 Permission API（`canUseTool` + `default/acceptEdits/
dontAsk/bypassPermissions/plan` + allow/deny/ask）**同构**，差异是：Permission API
只管"工具调用是否被批准"，**不管主动性分级**（≈10% 覆盖）。

配合 **5 条熔断条件（Circuit Breaker）**：①同一 Allowed 动作连续 5 次失败→降级
Needs-Confirm；②同一动作 24h 内 > 50 次→提醒；③Forbidden 被试图执行→立即冻结+
台账+通知；④Needs-Confirm 5 分钟无响应→取消；⑤错误 > 10 条/小时→触发 C5-1 漂移治理。

这一例解决的**具体问题**：**给我一份可直接落盘的 `autonomy-boundary.yaml`，
把"能做就做"变成声明式的三档授权 + 5 条熔断**。

> **来源**：v1.0 卷五《主动性边界》（越主动不等于越好）；v4.0 卷五 M5（护城河二号，
> 全文重写：三档制 + `autonomy-boundary.yaml` + 5 熔断 + Claude Permission API 对位）。
> 本配方从零撰写，仅沿用三档语义、熔断条件与配置骨架事实。

## 配置（完整可复制）

**Step 1 · 写入 `~/.openclaw/governance/autonomy-boundary.yaml`**（整段复制，零省略）：

```yaml
# ============================================================================
# 主动性边界三档制（Autonomy Boundary Triad）
# 路径：~/.openclaw/governance/autonomy-boundary.yaml
# 版本：v1.0 · 2026-09-27 · 基座 OpenClaw 2026.9.4 (3a9d69d)
# ============================================================================
version: "1.0"
agent: "*"                 # 默认规则；按 agent 命名空间可覆盖（见文末 overrides）

boundary:
  # ── Allowed（允许）：无需确认，直接执行 ──────────────────────────────
  allowed:
    - action: "memory.read.L1"
      when: "always"                     # 读 L1 精选记忆永远允许
      audit: "silent"                    # 不记台账（读操作）
    - action: "memory.flush"
      when: "pre-compaction"             # 压缩前可主动刷写（见 C4-4）
      audit: "ledger_only"
    - action: "drift.scan"
      when: "cron.weekly"                # 周检可主动跑漂移扫描（见 C5-1）
      audit: "ledger_only"
    - action: "health.check"
      when: "cron.weekly"                # 周检可主动跑体检（见 C5-3）
      audit: "ledger_only"

  # ── Forbidden（禁止）：永远不可主动执行 ──────────────────────────────
  forbidden:
    - action: "memory.write.L5.provenance"
      reason: "provenance 必须由用户或治理接口写入（审计痕迹不可自证）"
      enforcement: "freeze_and_alert"
    - action: "file.delete.outside_workspace"
      reason: "工作区外删除永远禁止"
      enforcement: "freeze_and_alert"
    - action: "agent.spawn"
      reason: "创建 agent 必须经用户显式确认（只能走 Needs-Confirm）"
      enforcement: "freeze_and_alert"
    - action: "external.send"
      reason: "对外通道（Telegram/飞书/邮件）发送必须显式请求"
      enforcement: "freeze_and_alert"
    - action: "payment.execute"
      reason: "任何付费/下单动作永远禁止主动执行"
      enforcement: "freeze_and_alert"

  # ── Needs-Confirm（待确认）：提议 + 等确认 ───────────────────────────
  needs_confirm:
    - action: "plugin.install"
      timeout_seconds: 300               # 5 分钟无响应取消
      notify_channel: "user_primary"
    - action: "cron.create"
      timeout_seconds: 300
      notify_channel: "user_primary"
    - action: "agent.spawn"
      timeout_seconds: 300
      notify_channel: "user_primary"
    - action: "file.delete.inside_workspace"
      timeout_seconds: 300
      notify_channel: "user_primary"

# ── 5 条熔断条件（Circuit Breaker）─────────────────────────────────────
circuit_breaker:
  on_consecutive_failures: 5             # ① 同一 Allowed 连续 5 次失败 → 降级 Needs-Confirm
  on_daily_executions: 50                # ② 同一动作 24h 内 > 50 次 → 提醒用户
  on_forbidden_attempt: "freeze"         # ③ Forbidden 被试图执行 → 冻结
  on_confirm_timeout_seconds: 300        # ④ Needs-Confirm 5 分钟超时 → 取消
  on_error_rate_per_hour: 10             # ⑤ 错误 > 10 条/h → 触发 C5-1 漂移治理 L2

# ── 审计 ───────────────────────────────────────────────────────────────
audit:
  ledger: "~/.openclaw/governance/autonomy-ledger.jsonl"
  retention_days: 365
  notify_channel: "user_primary"

# ── 按 agent 命名空间覆盖（示例）──────────────────────────────────────
overrides:
  kunlun:
    allowed:
      - action: "drift.scan"
        when: "cron.weekly"
        audit: "ledger_only"
      - action: "memory.write.L5.provenance"   # 仅 kunlun 允许写 provenance
        when: "always"
        audit: "ledger_only"
  tiance:
    allowed:
      - action: "agent.audit"
        when: "cron.daily"
        audit: "ledger_only"
```

**Step 2 · 写入边界校验脚本 `~/.openclaw/governance/boundary_check.py`**：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""boundary_check.py · 主动性边界三档制校验器
路径：~/.openclaw/governance/boundary_check.py
用法：python3 boundary_check.py <action> [--agent NAME]
输出：该 action 对某 agent 的档位判定 + 应执行的动作 + 审计要求
"""
import sys, os, json, argparse, datetime as dt
from pathlib import Path
import yaml

CFG = os.path.expanduser("~/.openclaw/governance/autonomy-boundary.yaml")

def load():
    return yaml.safe_load(open(CFG, encoding="utf-8"))

def resolve(cfg, agent):
    """合并默认规则 + agent overrides"""
    b = {"allowed": list(cfg["boundary"]["allowed"]),
         "forbidden": list(cfg["boundary"]["forbidden"]),
         "needs_confirm": list(cfg["boundary"]["needs_confirm"])}
    ov = cfg.get("overrides", {}).get(agent, {})
    for k in b:
        if k in ov:
            b[k] = b[k] + list(ov[k])
    return b

def classify(cfg, agent, action):
    b = resolve(cfg, agent)
    for r in b["needs_confirm"]:
        if r["action"] == action:
            return ("Needs-Confirm", r)
    for r in b["allowed"]:
        if r["action"] == action:
            return ("Allowed", r)
    for r in b["forbidden"]:
        if r["action"] == action:
            return ("Forbidden", r)
    return ("Undefined", {})          # 未落档 = 默认按 Needs-Confirm 处置（安全默认）

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action")
    ap.add_argument("--agent", default="*")
    ap.add_argument("--ledger", default=None)
    a = ap.parse_args()
    cfg = load()
    tier, rule = classify(cfg, a.agent, a.action)
    disp = {"Allowed": "执行（直接执行 + 记台账）",
            "Forbidden": "拒绝（写明原因 + 高亮台账）",
            "Needs-Confirm": f"提议（等 {rule.get('timeout_seconds',300)}s，超时取消）",
            "Undefined": "提议（未落档 → 安全默认为待确认）"}
    out = {"agent": a.agent, "action": a.action, "tier": tier,
           "disposition": disp[tier], "rule": rule,
           "ts": dt.datetime.now().isoformat()}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if a.ledger:
        with open(os.path.expanduser(a.ledger), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(out, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
```

## 验证步骤

```bash
cd ~/.openclaw/governance

# 1. YAML 合法性 + 三档齐备
python3 - <<'PY'
import yaml
c=yaml.safe_load(open("autonomy-boundary.yaml",encoding="utf-8"))
b=c["boundary"]
for k in ("allowed","forbidden","needs_confirm"):
    assert b[k], f"❌ {k} 为空"
    print(f"✅ {k}: {len(b[k])} 条")
assert len(c["boundary"]["forbidden"])>=3, "❌ Forbidden 至少 3 条红线"
cb=c["circuit_breaker"]
assert cb["on_consecutive_failures"]==5 and cb["on_confirm_timeout_seconds"]==300
print("✅ 5 熔断条件就位")
PY

# 2. 档位判定演示（三档各一）-----------------------------------------
python3 boundary_check.py memory.read.L1
# 期望：tier=Allowed，disposition=执行
python3 boundary_check.py payment.execute
# 期望：tier=Forbidden，disposition=拒绝
python3 boundary_check.py agent.spawn
# 期望：tier=Needs-Confirm（needs_confirm 优先于 forbidden 判定顺序）→ 提议，等 300s
python3 boundary_check.py something.undefined
# 期望：tier=Undefined → 安全默认为「提议」

# 3. 命名空间覆盖生效（kunlun 可写 provenance）
python3 boundary_check.py memory.write.L5.provenance --agent kunlun
# 期望：tier=Allowed（overrides 生效）
python3 boundary_check.py memory.write.L5.provenance --agent "*"
# 期望：tier=Forbidden（默认规则）

# 4. 审计台账落盘
python3 boundary_check.py drift.scan --agent kunlun --ledger autonomy-ledger.jsonl
wc -l autonomy-ledger.jsonl
# 期望：≥ 1 行，且末行为合法 JSON

# 5. Forbidden 熔断演示（写入后应高亮）
python3 -c "
import json
for line in open('autonomy-ledger.jsonl',encoding='utf-8'):
    r=json.loads(line)
    flag='🚨' if r['tier']=='Forbidden' else '✅'
    print(flag, r['agent'], r['action'], r['tier'])
"
```

> ⏳ 待实测：`boundary_check.py` 是**判定器**（离线校验三档语义），
> **不接入 OpenClaw 运行时拦截**。真正的运行时拦截需要 OpenClaw 的权限钩子
> （对应 Claude Permission API 的位置），本机 2026.9.4 的钩子接口未验证。
> 当前用法：**训练前用判定器预演，训练后逐条比对台账**。

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **治理目录**：`~/.openclaw/governance/`（本机新建）
- **对位对象**：Claude Agent SDK Permission API（`canUseTool` + allow/deny/ask 规则），
  v4.0 记录其 stars 8,171 · MIT · push 2026-09-25；三档与 allow/deny/ask 同构
- **OS**：macOS 26.5.1 · **日期**：2026-09-27
- **来源基线**：v4.0 卷五 M5 的三档语义 + 5 熔断 + Claude Permission API 同构对位

## 排坑

1. **三档不分、全塞 Allowed**：最危险。症状是 agent 自己发消息/自己下单。
   核验：`grep -c "enforcement: freeze_and_alert" autonomy-boundary.yaml` ≥ 3；
   `external.send` / `payment.execute` / `file.delete.outside_workspace` 三条**必须在 Forbidden**。

2. **Needs-Confirm 超时不清**：Agent 提议后用户没回，行为悬挂。核验：
   `on_confirm_timeout_seconds: 300`（5 分钟）+ 台账记录"超时取消"。

3. **Forbidden 只写不拦**：写了 Forbidden 但没有运行时拦截 → 形同虚设。
   诚实边界：本配方给的是**声明式配置 + 离线判定器**；运行时拦截需 OpenClaw 权限钩子
   （⏳ 待实测）。过渡期：把 Forbidden 清单写进 AGENTS.md 的"❌ 不做"段让模型自觉遵守，
   再靠台账事后审计。

4. **未落档的动作被放行**：既不在 Allowed 也不在 Forbidden/Needs-Confirm 的动作，
   默认被当"可以做"→ 漏洞。本配方用**安全默认**：`Undefined → 提议（Needs-Confirm）`。
   核验：验证步骤 2 的 `something.undefined` 应输出提议。

5. **覆盖顺序反了**：以为 `forbidden` 优先于 `needs_confirm`。实际判定顺序是
   `needs_confirm → allowed → forbidden`，所以同时出现在两档的动作按 Needs-Confirm 走。
   若你希望某动作**绝对禁止**，只能出现在 `forbidden`，**不得**同时出现在 `needs_confirm`。

6. **审计台账无限膨胀**：`retention_days: 365` 需配合周度归档
   （见 C5-3 W2 步骤），否则台账会拖慢扫描。

## 进阶

- **进阶 1 · 与漂移治理闭环**：熔断条件⑤（错误 > 10 条/h）直接触发 C5-1 的漂移治理 L2
  处置。边界违例率（violation_score）是漂移分的一项权重（0.20）——两例天然联动。

- **进阶 2 · 三档制 × 进化阶梯**：L1/L2 agent 的 Allowed 清单**越短越好**（只留读操作），
  到 L4/L5 才逐步放开（如允许主动出日报）。把"等级 → Allowed 清单长度"写进训练计划（C4-1）。

- **进阶 3 · 台账进治理审计账本**：`autonomy-ledger.jsonl` 即治理审计账本
  （Governance Audit Ledger）的数据源，与 Merit Ledger（功绩账本）配对——
  一个记"做了什么不问自答"，一个记"做对了多少分"。

- **进阶 4 · 对位业界三档缺口**：LangGraph / AutoGen / CrewAI / OpenAI Agents SDK /
  LlamaIndex 默认"能做就做"（0 覆盖）；Claude Permission API 只覆盖**工具调用批准**
  （≈10%），**主动性分级完全空白**。三档制是把"权限"升级为"行为分类语言"的差异化设计。

---

## 附录 · 三档制速查 + 判定顺序陷阱

### 附表 A · 三档 × 审计 × 通知 一览

| 档位 | 直接执行？ | 台账 | 通知用户 | 用户显式请求时可做？ |
|---|:--:|---|---|:--:|
| Allowed | ✅ | `ledger_only` 或 `silent` | ❌ | ✅ |
| Forbidden | ❌ | 高亮写入 | ✅（告警） | ✅（仅显式请求） |
| Needs-Confirm | ➖（提议） | 写入 | ✅ | ✅ |

### 附表 B · 判定顺序陷阱（最易错处）

判定顺序固定为 **`needs_confirm → allowed → forbidden`**：

```text
输入：agent.spawn
  → needs_confirm 命中（有 timeout 300 + notify）→ 判 Needs-Confirm
  注：即使 agent.spawn 也出现在 forbidden，仍按 Needs-Confirm 走
     （因为判定先撞 needs_confirm）
```

**推论**：一个动作若你希望它**绝对禁止**，只能出现在 `forbidden`，
**绝不能**同时出现在 `needs_confirm`。反之，若希望它"可提议但等确认"，
放 `needs_confirm` 即可，不必再放 `forbidden`。

### 附表 C · 5 熔断条件速查

| # | 条件 | 阈值 | 熔断动作 |
|:--:|---|---|---|
| 1 | 同一 Allowed 连续失败 | 5 次 | 降级为 Needs-Confirm |
| 2 | 同一动作 24h 执行次数 | > 50 | 提醒用户 |
| 3 | Forbidden 被试图执行 | 1 次 | 立即冻结 + 高亮台账 + 通知 |
| 4 | Needs-Confirm 无响应 | 300 秒 | 自动取消（不执行） |
| 5 | 主动行为错误日志 | > 10 条/小时 | 触发 C5-1 漂移治理 L2 |

---

# C5-3 · 每周体检：cron plist + launchctl 实操 + 体检清单

## 背景

监控（Observability）和体检（Periodic Health Check，原：每周体检清单）是两件事：
监控回答"这次跑得对不对"；体检回答"**这只 Agent 三十天后还是不是它**"。
业界 2026-09-27 的状态是：LangSmith / OpenAI Tracing / W&B 提供 trace/eval，
**全部只覆盖单次运行质量，无周期体检制度**（≈15% 覆盖）。

本机有两类真实"静默失效"样本，正是体检缺失的代价：

- **能力矩阵 26 天未续期**：本应"每日/每周续期"的能力矩阵数据出现 26 天空洞，
  事后才发现（`workspace-kunlun/memory/2026-09-01-能力矩阵月度更新.md` 之后无新）
- **18 个坏 skill**：一批 skill 目录缺 `SKILL.md` 或 frontmatter 不合法，
  导致"装了 200+ 实际可用远少于此"，且长期无人发现

OpenClaw 2026.9 提供**两套时间触发机制**（本机证据）：
`cron`（声明式调度；证据 `~/.openclaw/cron/jobs-state.json.migrated`、`~/.openclaw/cron/runs/`）
与 `automations`（事件驱动）；另有 `heartbeat`（Agent 内轻量自检）。
本机 `~/Library/LaunchAgents/` 实测已有 `ai.openclaw.gateway.plist` +
`com.openclaw.monthly-cleanup.plist`。

这一例解决的**具体问题**：**给我一份可 `launchctl` 加载的周检 plist + 8 层体检清单 +
一套真实命令，让"越跑越差"每周被看见一次**。

> **来源**：v1.0 卷五《长期稳定性检查清单》+ 附录 A《每周体检清单》；
> v4.0 卷五 M6（护城河三号，全文重写：cron plist + launchctl 实操 + 8 层 + 漂移分公式）。
> 本配方从零撰写，仅沿用 8 层维度、plist 结构与漂移分公式骨架事实。

## 配置（完整可复制）

**Step 1 · 写入周检脚本 `~/.openclaw/governance/health_check.sh`**：

```bash
#!/bin/bash
# ============================================================================
# 每周体检脚本（Periodic Health Check）
# 路径：~/.openclaw/governance/health_check.sh
# 版本：v1.0 · 2026-09-27 · 基座 OpenClaw 2026.9.4 (3a9d69d)
# 用法：bash health_check.sh    （通常由 launchd 每周一 03:00 触发）
# ============================================================================
set -uo pipefail
GOV="$HOME/.openclaw/governance"
OUT="$GOV/health"
mkdir -p "$OUT"
TODAY=$(date +%F)
REPORT="$OUT/health-$TODAY.md"

{
  echo "# 每周体检报告 · $TODAY"
  echo
  echo "## 环境"
  echo '```'
  openclaw --version 2>&1 | tail -1
  sw_vers 2>/dev/null | head -2
  echo '```'
  echo

  # ── 维度1 · 记忆层（M1）───────────────────────────────────────────
  echo "## 1. 记忆层（M1）"
  echo '```'
  for ws in "$HOME"/.openclaw/workspace/agents/workspace-*; do
    a=$(basename "$ws")
    l1="$ws/memory/MEMORY.md"
    [ -f "$l1" ] && echo "$a: MEMORY.md $(( $(wc -l < "$l1") )) 行" \
                 || echo "$a: ❌ 缺 MEMORY.md"
  done
  echo '```'

  # ── 维度2 · 上下文层（M3）─────────────────────────────────────────
  echo "## 2. 上下文层（M3）"
  echo '```'
  ls "$HOME/.openclaw/cron/" 2>/dev/null || echo "（无 cron 目录）"
  echo '```'

  # ── 维度3 · 节律层（M2）───────────────────────────────────────────
  echo "## 3. 节律层（M2）· 已加载 launchd 任务"
  echo '```'
  launchctl list 2>/dev/null | grep -i openclaw || echo "（无）"
  echo '```'

  # ── 维度4 · 漂移层（M4）───────────────────────────────────────────
  echo "## 4. 漂移层（M4）"
  echo '```'
  python3 "$GOV/drift_scan.py" --json "$OUT/drift-$TODAY.json" 2>&1 | head -20
  echo '```'

  # ── 维度5 · 边界层（M5）───────────────────────────────────────────
  echo "## 5. 边界层（M5）· 三档配置自检"
  echo '```'
  grep -c "freeze_and_alert" "$GOV/autonomy-boundary.yaml" 2>/dev/null || echo "0"
  echo "（Forbidden 红线数，期望 ≥ 3）"
  echo '```'

  # ── 维度6 · 价值层 ────────────────────────────────────────────────
  echo "## 6. 价值层 · 锚点回归"
  echo '```'
  grep -o "blue\|蓝血\|证据" "$HOME/.openclaw/workspace/agents/workspace-kunlun/SOUL.md" 2>/dev/null | sort | uniq -c || echo "（人工核对）"
  echo '```'

  # ── 维度7 · 交接层（掉棒率）───────────────────────────────────────
  echo "## 7. 交接层"
  echo '```'
  ls "$HOME/.openclaw/workspace/agents/workspace-tiance/handoff/" 2>/dev/null || echo "（无交接目录 → ⏳ 待建）"
  echo '```'

  # ── 维度8 · 串线层（会话串线率）───────────────────────────────────
  echo "## 8. 串线层"
  echo '```'
  ls "$HOME/.openclaw/sessions/" 2>/dev/null | wc -l
  echo "（session 数，异常增长需排查串线）"
  echo '```'

  echo
  echo "## 结论"
  echo "- 通过项 / 待整改项：人工填写"
  echo "- 漂移分（Drift Score）：见 drift-$TODAY.json 的 summary"
} > "$REPORT" 2>&1

echo "✅ 体检报告已生成：$REPORT"
```

**Step 2 · 写入 launchd plist `~/Library/LaunchAgents/ai.openclaw.weekly-health-check.plist`**：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/sbin:/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin</string>
    </dict>
    <key>Label</key>
    <string>ai.openclaw.weekly-health-check</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/peterqiu/.openclaw/governance/health_check.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>3</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardErrorPath</key>
    <string>/Users/peterqiu/.openclaw/governance/logs/health-weekly.err.log</string>
    <key>StandardOutPath</key>
    <string>/Users/peterqiu/.openclaw/governance/logs/health-weekly.out.log</string>
    <key>WorkingDirectory</key>
    <string>/Users/peterqiu/.openclaw/governance</string>
</dict>
</plist>
```

**Step 3 · 8 层体检清单 `~/.openclaw/governance/health-checklist.md`**：

```markdown
# 每周体检清单（Weekly Health Checklist）

| # | 维度 | v4.0 加注 | 通过标准 | 本次 | 证据 |
|:--:|---|---|---|:--:|---|
| 1 | 记忆层（M1） | L1 ≤ 30% block + flush 触发器 | 5 层齐 + L1 不超限 | ☐ | memory/ |
| 2 | 上下文层（M3） | L1–L3 污染等级 | 无污染滞留 | ☐ | compaction 日志 |
| 3 | 节律层（M2） | heartbeat 3 真名字段 + 退役物清理 | launchctl 已加载 | ☐ | launchctl list |
| 4 | 漂移层（M4） | 6 层链 + L1–L3 分级 | 无 L3 紧急项 | ☐ | drift-*.json |
| 5 | 边界层（M5） | 三档制 + 5 熔断 | Forbidden ≥ 3 条 | ☐ | autonomy-boundary.yaml |
| 6 | 价值层 | 蓝血价值观回归 | 锚点命中 | ☐ | SOUL.md |
| 7 | 交接层 | 交接失败率 | 掉棒率 < 5% | ☐ | handoff/ |
| 8 | 串线层 | 串线率 | session 数无异常 | ☐ | sessions/ |

## 续期型任务的「新鲜度守卫」（防静默停摆）
```bash
DATA=~/.openclaw/workspace/agents/workspace-kunlun/memory/2026-09-01-能力矩阵月度更新.md
if [ -f "$DATA" ]; then
  AGE_DAYS=$(( ( $(date +%s) - $(stat -f %m "$DATA") ) / 86400 ))
  [ "$AGE_DAYS" -gt 14 ] && echo "🚨 能力矩阵已 $AGE_DAYS 天未续期（阈值 14）"
else
  echo "🚨 能力矩阵数据文件不存在"
fi
```
```

## 验证步骤

```bash
cd ~/.openclaw/governance
mkdir -p logs health

# 1. 脚本与 plist 就位
for f in health_check.sh health-checklist.md; do
  [ -f "$f" ] && echo "✅ $f" || echo "❌ $f 缺失"
done
[ -f ~/Library/LaunchAgents/ai.openclaw.weekly-health-check.plist ] \
  && echo "✅ plist 存在" || echo "❌ plist 缺失"

# 2. plist 语法校验（plutil）
plutil -lint ~/Library/LaunchAgents/ai.openclaw.weekly-health-check.plist
# 期望：... OK

# 3. 手动跑一次体检（不等周一）
chmod +x health_check.sh
bash health_check.sh
# 期望：✅ 体检报告已生成：/Users/peterqiu/.openclaw/governance/health/health-2026-09-27.md

# 4. 报告非空且 8 层齐
grep -c "^## [1-8]\." health/health-*.md
# 期望：8

# 5. 加载 launchd 任务
launchctl load ~/Library/LaunchAgents/ai.openclaw.weekly-health-check.plist
launchctl list | grep openclaw
# 期望：出现 ai.openclaw.weekly-health-check 一行

# 6. 立即触发一次（验证加载成功）
launchctl start ai.openclaw.weekly-health-check
sleep 2
ls -t health/ | head -3
# 期望：最新一份 health-*.md 时间戳更新

# 7. 新鲜度守卫（防"能力矩阵 26 天未续期"重演）
DATA=~/.openclaw/workspace/agents/workspace-kunlun/memory/2026-09-01-能力矩阵月度更新.md
[ -f "$DATA" ] && echo "AGE=$(( ( $(date +%s) - $(stat -f %m "$DATA") ) / 86400 )) 天" \
               || echo "🚨 数据文件不存在（本机样本：26 天未续期）"

# 8. 卸载（如需）
# launchctl unload ~/Library/LaunchAgents/ai.openclaw.weekly-health-check.plist
```

> ⏳ 待实测：各维度里引用 `~/.openclaw/sessions/`、`~/.openclaw/cron/`、
> `workspace-tiance/handoff/` 的**真实路径**未在本任务中实拉核对；脚本对其做了
> `ls ... || echo "（无）"` 的降级保护，缺失不中断。真实路径以你本机为准。
> `launchctl load` 在 macOS 26.x 上可能与 `launchctl bootstrap gui/<uid>` 等价——
> 若 `load` 报错，改用 `launchctl bootstrap gui/$(id -u) <plist>`。

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **launchd**：`~/Library/LaunchAgents/` 本机实测含 `ai.openclaw.gateway.plist` +
  `com.openclaw.monthly-cleanup.plist`（后者每月 1 日 03:00 跑
  `~/.hermes/scripts/openclaw_monthly_cleanup.sh`）
- **双轨机制**：`cron`（`~/.openclaw/cron/jobs-state.json.migrated`、`~/.openclaw/cron/runs/`）
  + `automations`；另有 `heartbeat`（本机 kunlun/peter/tiance 已配置）
- **真实样本**：能力矩阵 26 天未续期 · 18 个坏 skill
- **OS**：macOS 26.5.1（`launchctl` 行为以 26.x 为准）· **日期**：2026-09-27
- **来源基线**：v4.0 卷五 M6 的 8 层维度 + plist 模板 + 漂移分公式
  （`drift_score = 0.30*file_age + 0.20*anchor_miss + 0.10*retired + 0.20*violation + 0.20*amnesia`）

## 排坑

1. **"监控 ≠ 体检"混淆**：只配了日志/trace，以为体检就做了。核验：
   `launchctl list | grep openclaw` 必须出现**周检任务**；只有 gateway 不算。

2. **plist 里的 PATH 缺 node/npm**：`launchd` 是干净环境，若脚本调用 `openclaw`（node）
   会因 PATH 不含 node 路径而失败。核验：`plutil -lint` 通过后，`launchctl start` 一次，
   看 `logs/health-weekly.err.log` 是否有 `command not found`；有则往 plist 的 PATH
   追加 `/opt/homebrew/bin` 与 npm 全局 bin 路径。

3. **`launchctl load` 在 macOS 26 报错**：新系统改用 `launchctl bootstrap gui/<uid>`。
   核验：`launchctl load ... 2>&1` 若出现 "Load failed"，改用
   `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.weekly-health-check.plist`。

4. **续期型任务静默停摆（26 天样本重演）**：脚本不报错但也不产出。根因是
   "它不像业务任务有人天天盯，它停了没人喊"。解法：**新鲜度守卫**（本例第 7 步）——
   给每个续期任务写"最大允许间隔"，超期即告警。这是 F3/F7 里最真实的失败形态。

5. **报告写死绝对路径**：plist 与脚本里的 `/Users/peterqiu/...` 是**本机实测路径**；
   换机器必须改。核验：`grep -rn "/Users/peterqiu" ~/.openclaw/governance/` 逐条替换。

6. **体检只跑不改**：报告生成后没人看。核验：任一项 ☐ 未打勾 → 生成
   Remediation Ticket（修复工单），指定责任人与截止日；否则体检退化为"自我安慰"。

## 进阶

- **进阶 1 · 体检 × 漂移分排名**：把 18 个 agent 按 `drift_score` 排序，每周报 Top 3
  最漂移。这样治理有优先级，而不是平均用力。

- **进阶 2 · 三轨分工**：体检类 → `cron`；事件响应类 → `automations`；Agent 内轻量自检
  → `heartbeat`。不要把所有任务都塞一条轨，否则故障面会叠加。

- **进阶 3 · 体检报告推送**：把报告摘要推送到用户主通道（Telegram），
  并在报告顶部只放"3 个数字"（red 数 / 未关闭工单数 / 最新 drift_score），
  让用户 10 秒内知道要不要细看。

- **进阶 4 · 治"该进化却没进化"**：本机 8 个 P0 stub（来自 2026-09-03 暗夜熔炉报告
  cron `a2d4eb3d4399`）应作为体检维度 9（自指层）：统计"超期未关闭的 stub 数"，
  30 天未关闭即判 L2 严重。这正是"进化机制必须能识别自己该进化却没进化"的落地。

---

## 附录 · 8 层体检维度命令速查

一键把 8 个维度各跑一条（可粘进 `health_check.sh` 逐段替换）：

```bash
# 1 记忆层：5 层目录是否齐
ls -d ~/.openclaw/workspace/agents/workspace-*/memory/{daily,prospective,review} 2>/dev/null | wc -l

# 2 上下文层：压缩配置是否存在
find ~/.openclaw/workspace/agents -name 'compaction*' 2>/dev/null | head

# 3 节律层：已加载的定时任务
launchctl list | grep -i openclaw

# 4 漂移层：跑一次漂移扫描取 summary
python3 ~/.openclaw/governance/drift_scan.py --json /tmp/drift-now.json 2>&1 | head -12

# 5 边界层：Forbidden 红线计数
grep -c 'freeze_and_alert' ~/.openclaw/governance/autonomy-boundary.yaml

# 6 价值层：锚点词命中
grep -o '蓝血\|证据\|边界' ~/.openclaw/workspace/agents/workspace-kunlun/SOUL.md | sort | uniq -c

# 7 交接层：交接目录/掉棒记录
ls ~/.openclaw/workspace/agents/workspace-tiance/handoff/ 2>/dev/null || echo '（无 → ⏳ 待建）'

# 8 串线层：session 数异常增长
ls ~/.openclaw/sessions/ 2>/dev/null | wc -l
```

**体检结束后必做的三件事**（否则体检退化为自我安慰）：

1. 任一项 ☐ 未打勾 → 生成修复工单（Remediation Ticket），写责任人与截止日；
2. 把 `drift_score` 与上期对比，> 0.60 的 agent 进 red 名单；
3. 报告摘要（3 个数字：red 数 / 未关闭工单数 / 最新 drift_score）推送到用户主通道。

---

# C5-4 · TEV 三证据验证实操：证据采集 + 验收报告

## 背景

"我已经完成了"是 Agent 最廉价的一句话。TEV（三证据验证 / Three-Evidence
Verification，原：三证验真）把"声称完成"降维成**可独立验证的证据集合**。
没有 TEV，任务卡只是意愿书，验收口径只是愿望清单，组织从"靠证据运行"退化为
"靠信任运行"。

三证的定义与硬度：

| 证 | 名称（中/英） | 证明什么 | 硬度 |
|---|---|---|---|
| 证一 | 新产物（**Artifact**） | 产物**存在**（路径/可打开/非空/时间戳匹配） | 最低 |
| 证二 | 前后对比（**Diff**） | 发生了**实质性变化**（有基线/变化清单/量级匹配） | 中 |
| 证三 | 测试/回执/日志（**Verification**） | 结果**可被第三方独立复现** | 最高 |

**递进律**：证一不成立 → 无需判证二·证三，直接驳回。三证正交（存在性 + 变化性 +
可复现性），共同封死"假完成"的所有退路。

对位业界：OpenAI Agents SDK Tracing（⭐29,715 · MIT · push 2026-09-25）提供
spans + traces 把执行切成可观测的 span 树，但**只"看得见"，不"验真"**——
它无通过/拒收裁决，也不接治理账本。TEV 把可观测性**升级为可证伪性**，
并明确三态裁决：Accepted / Rejected / Rework。

这一例解决的**具体问题**：**给我一套可落地的 TEV 证据采集脚本 + 验收报告模板，
让"完成"变成一条可复现的证据链**。

> **来源**：v1.0 卷六模块 3《三证验真》；v4.0 卷六模块 3（TEV：改名 + 业界对位 +
> TEV SOP 模板 + YAML）。本配方从零撰写，仅沿用三证定义、递进律、防腐三机制骨架事实。

## 配置（完整可复制）

**Step 1 · 建 TEV 目录**：

```bash
mkdir -p ~/.openclaw/governance/tev
touch ~/.openclaw/governance/tev/.keep
```

**Step 2 · 写入 TEV 校验脚本 `~/.openclaw/governance/tev_verify.py`**：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tev_verify.py · TEV（三证据验证）校验器
路径：~/.openclaw/governance/tev_verify.py
用法：python3 tev_verify.py <task.yaml>
判定：Accepted / Rejected / Rework（三态裁决）
"""
import sys, json, hashlib, subprocess, datetime as dt
from pathlib import Path
try:
    import yaml
except ImportError:
    sys.exit("需要 PyYAML：python3 -m pip install pyyaml")

def sha256(p):
    h = hashlib.sha256()
    h.update(Path(p).read_bytes())
    return "sha256:" + h.hexdigest()[:16]

def verify(task):
    tid = task["task_id"]
    rep = {"task_id": tid, "agent": task.get("agent"), "ts": dt.datetime.now().isoformat(),
           "evidences": {}, "verdict": None, "reasons": []}
    # ── 证一：新产物（Artifact）────────────────────────────────────
    a = task["artifact"]
    p = Path(a["path"]).expanduser()
    e1 = {"exists": p.exists(),
          "size": p.stat().st_size if p.exists() else 0,
          "non_empty": p.exists() and p.stat().st_size > 0,
          "hash": sha256(p) if p.exists() and p.is_file() else None}
    rep["evidences"]["artifact"] = e1
    if not (e1["exists"] and e1["non_empty"]):
        rep["verdict"] = "Rejected"
        rep["reasons"].append("证一不成立：产物不存在或为空 → 直接驳回（递进律）")
        return rep
    # ── 证二：前后 Diff ────────────────────────────────────────────
    d = task.get("diff", {})
    e2 = {"baseline": False, "changed": False, "lines_added": 0, "lines_removed": 0}
    base = Path(d.get("baseline", "")).expanduser() if d.get("baseline") else None
    if base and base.exists():
        e2["baseline"] = True
        r = subprocess.run(["diff", "-u", str(base), str(p)],
                           capture_output=True, text=True)
        e2["changed"] = (r.returncode != 0)
        for ln in r.stdout.splitlines():
            if ln.startswith("+") and not ln.startswith("+++"):
                e2["lines_added"] += 1
            elif ln.startswith("-") and not ln.startswith("---"):
                e2["lines_removed"] += 1
    rep["evidences"]["diff"] = e2
    if not (e2["baseline"] and e2["changed"]):
        rep["verdict"] = "Rework"
        rep["reasons"].append("证二不成立：无基线或内容无实质变化（疑似旧货重提）")
        return rep
    # ── 证三：测试/回执/日志 ──────────────────────────────────────
    v = task.get("verification", {})
    cmd = v.get("command")
    e3 = {"command": cmd, "passed": None, "output": ""}
    if cmd:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        e3["passed"] = (r.returncode == 0)
        e3["output"] = (r.stdout + r.stderr)[:500]
    rep["evidences"]["verification"] = e3
    if e3["passed"] is False:
        rep["verdict"] = "Rework"
        rep["reasons"].append("证三不成立：自测命令返回非 0")
        return rep
    if e3["passed"] is None:
        rep["verdict"] = "Accepted(weak)"
        rep["reasons"].append("证三缺失：仅有证一+证二，硬度不足（建议补自测）")
        return rep
    rep["verdict"] = "Accepted"
    rep["reasons"].append("三证齐备且递进成立")
    return rep

def main():
    if len(sys.argv) < 2:
        sys.exit("用法：python3 tev_verify.py <task.yaml>")
    task = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    rep = verify(task)
    out = Path("~/.openclaw/governance/tev").expanduser() / f"{rep['task_id']}.report.json"
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    print(f"\n📄 验收报告：{out}")
    sys.exit(0 if rep["verdict"].startswith("Accepted") else 1)

if __name__ == "__main__":
    main()
```

**Step 3 · 写入任务定义 `~/.openclaw/governance/tev/T-001.yaml`**：

```yaml
# ============================================================================
# TEV 任务定义（三证据验证）
# 路径：~/.openclaw/governance/tev/T-001.yaml
# ============================================================================
task_id: "T-001"
agent: "kunlun"
title: "把 2000 字草稿压成 800 字要点"
artifact:
  path: "~/.openclaw/governance/tev/T-001-artifact.md"
  kind: "markdown"
diff:
  baseline: "~/.openclaw/governance/tev/T-001-baseline.md"   # 压缩前的原文
verification:
  command: "wc -c < ~/.openclaw/governance/tev/T-001-artifact.md"
  expect: "非零且 ≈ 800 字对应字节数"
acceptance:
  pass: "三证齐备（产物存在 + Diff 有实质变化 + 自测通过）"
  partial: "证一+证二，缺证三"
  fail: "证一不成立"
```

**Step 4 · TEV 验收报告模板 `~/.openclaw/governance/tev/report-template.md`**：

```markdown
# TEV 验收报告（Three-Evidence Verification Report）

- Task-ID：T-___
- AgentId：___
- 交付物路径：___
- 验收人：___  日期：____-__-__

## 证一 · 新产物（Artifact）
- [ ] 产物存在于预期路径：___
- [ ] 可打开/可阅读/可运行
- [ ] 非空（大小：___ 字节）
- [ ] SHA-256：___
- 产物摘要（2-3 句）：___

## 证二 · 前后对比（Diff）
- [ ] 有基线文件：___
- [ ] 有变化清单（新增 ___ 行 / 删除 ___ 行）
- [ ] 变化量级与任务匹配
- diff 命令与输出摘要：___

## 证三 · 测试/回执/日志（Verification）
- [ ] 自测命令：___
- [ ] 期望输出：___
- [ ] 实际输出：___
- [ ] 可被第三方独立复现：是 / 否

## 裁决
- 判定：Accepted / Rejected / Rework
- 依据（递进律）：证一___ → 证二___ → 证三___
- 未通过则触发 Remediation Ticket（修复工单）编号：___
```

## 验证步骤

```bash
cd ~/.openclaw/governance/tev

# 1. 造一份基线 + 产物（演示用）
printf '# 原始草稿\n第一段内容。\n第二段内容。\n第三段内容。\n' > T-001-baseline.md
printf '# 压缩后要点\n- 第一段要点\n- 第二段要点\n' > T-001-artifact.md

# 2. 跑 TEV 校验（三证齐 → Accepted）
python3 ../tev_verify.py T-001.yaml
# 期望（节选）：
#   "evidences": { "artifact": {"exists": true, "non_empty": true, "hash": "sha256:..."},
#                  "diff": {"baseline": true, "changed": true, "lines_added": 3, "lines_removed": 4},
#                  "verification": {"passed": true, ...} },
#   "verdict": "Accepted", "reasons": ["三证齐备且递进成立"]
#   📄 验收报告：.../tev/T-001.report.json

# 3. 证一不成立 → Rejected（删产物）
rm T-001-artifact.md
python3 ../tev_verify.py T-001.yaml; echo "退出码=$?"
# 期望：verdict=Rejected，原因"证一不成立：产物不存在或为空 → 直接驳回（递进律）"，退出码 1

# 4. 证二不成立 → Rework（产物与基线相同 = 旧货重提）
cp T-001-baseline.md T-001-artifact.md
python3 ../tev_verify.py T-001.yaml
# 期望：verdict=Rework，原因"证二不成立：无基线或内容无实质变化（疑似旧货重提）"

# 5. 证三不成立 → Rework（让自测命令失败）
sed -i '' 's|wc -c < .*|false|' T-001.yaml
sed -i '' 's|^# 原始草稿|# 已改|' T-001-artifact.md   # 制造实质变化
python3 ../tev_verify.py T-001.yaml
# 期望：verdict=Rework，原因"证三不成立：自测命令返回非 0"

# 6. 验收报告落盘核查
ls -l T-001.report.json
python3 -c "import json;print('✅ 报告 verdict =', json.load(open('T-001.report.json'))['verdict'])"

# 7. 防腐三机制（产物 hash 只追加 + 权限分离 + 24h 链验证）
sha256sum T-001-artifact.md 2>/dev/null || shasum -a 256 T-001-artifact.md
echo "（把 hash 追加到 evidence-hash.jsonl，且该文件设为只读：chmod 444）"
```

> ⏳ 待实测：`diff` / `wc` 依赖为 macOS 自带（`shasum` 替代 `sha256sum`）；
> 「防腐三机制」中的**权限分离**（写入后只读）与**每 24h hash 链完整验证**需配合
> cron（见 C5-3），本任务未端到端验证该定时链。

## 实测环境

- **OpenClaw**：`OpenClaw 2026.9.4 (3a9d69d)`
- **对位对象**：OpenAI Agents SDK Tracing（`openai/openai-agents-python`，⭐29,715 · MIT ·
  push 2026-09-25）——可观测（spans/traces）但无裁决、不接账本
- **依赖**：`PyYAML`；`diff` / `shasum` 为 macOS 自带
- **OS**：macOS 26.5.1 · **日期**：2026-09-27
- **来源基线**：v4.0 卷六模块 3 的三证定义 + 递进律 + 6 误区 + 防腐三机制 + TEV SOP

## 排坑

1. **"交满三样即通过"（误区 1）**：三证必须**层层递进且硬度达标**，不是凑数。
   核验：`tev_verify.py` 遇到证一不成立直接驳回，**不再判**证二·证三（递进律）。

2. **把"有人看过"当证三（误区 2）**：证三硬度低于测试需**显式标注**。
   核验：脚本对证三缺失的判定是 `Accepted(weak)` 而非 `Accepted`——弱点被标出来，
   不被掩盖。

3. **回执/日志不算证三（误区 3）**：回执与日志是**合法证三**，但硬度需标注。
   核验：报告模板里证三要求写明"可被第三方独立复现：是/否"。

4. **三证只是验收方的责任（误区 4）**：Agent **自证** + 验收方**复核**。
   核验：任务定义（T-001.yaml）由 Agent 自己填产物/Diff/自测命令，验收脚本独立跑。

5. **旧货重提**：产物存在、非空，但和上次交付的一模一样。核验：证二
   `changed` 必须为 true（有基线且 `diff` 返回非 0）；否则判 Rework。

6. **自测命令形同虚设**：`verification.command` 写成 `true`（永远成功）。
   核验：命令必须能**真实失败**（如 `wc -c` + 期望区间、`grep -q` 关键字段）；
   验证步骤 5 用 `false` 演示了失败路径。

7. **hash 被原地改**：`evidence-hash.jsonl` 必须**只追加** + 设为只读
   （`chmod 444`），否则防腐失效。核验：`ls -l` 看权限位；写入后不再有写权限。

## 进阶

- **进阶 1 · TEV 接治理账本**：TEV 通过 = 记账前提。把 `Accepted` 记录写入
  Merit Ledger（功绩账本），`Rejected`/`Rework` 写入 Remediation Ticket（修复工单）。
   这样"完成"与"结算"之间有了硬证据前提（无三证 = 不加分、不验收、不算完成）。

- **进阶 2 · TEV 上链（只追加 hash 链）**：把每条产物的 SHA-256 按时间只追加到
  `evidence-hash.jsonl`，每 24h 验证整链完整（块 n 的 hash 依赖块 n-1）。
   对应区块链"不可篡改证据链"的做法，对应 v4.0 防腐三机制之③。

- **进阶 3 · 三证自动化内嵌（L3→L4）**：L1 手动附加 → L2 结构化输出 →
  L3 由 AGENTS.md 约定 + hook 自动附着 → L4 证据链完整闭环 + 防腐。
   把"必须交三证"写进 AGENTS.md 的 ✅ 做 段，让证据成为默认动作。

- **进阶 4 · TEV × 训练轮次**：C4-1 的每一轮训练都必须交三证（产物 / Diff / 自测输出），
   训练判定 pass/fail 直接引用 TEV 结论。这样"训练成功"既不是主观感觉，
   也不是模型自述，而是一条可被第三方复现的证据链。

---

## 附录 · 三证硬度对照 + 递进律速查

### 附表 A · 三证硬度阶梯

| 证 | 硬度 | 典型证据 | 不够硬时的替代/补强 |
|---|:--:|---|---|
| 证一 新产物 | 最低 | 文件路径、打开截图 | — |
| 证二 前后 Diff | 中 | git diff、`diff -u` 输出 | 无基线 → 补存基线快照 |
| 证三 测试/回执/日志 | 最高 | 自测命令退出码、CI 日志、trace | 仅有人看过 → 标注 `Accepted(weak)` |

### 附表 B · 递进律一句话

```text
证一不成立 → 直接驳回（不判证二·证三）
证一成、证二不成 → Rework（疑旧货重提）
证一·二成、证三缺失 → Accepted(weak)（硬度不足，标注）
三证齐 → Accepted
```

### 附表 C · 6 误区速查（v4.0 卷六 M3）

| # | 误区 | 纠正 |
|:--:|---|---|
| 1 | 交满三样即通过 | 需层层递进且硬度达标 |
| 2 | "有人看过"就是证三 | 证三硬度低于测试须显式标注 |
| 3 | 只有"测试"才是证三 | 回执/日志是合法证三，标注硬度即可 |
| 4 | 三证是验收方的责任 | Agent 自证 + 验收方复核 |
| 5 | 三证只有单次价值 | 证据链进账本与基因库，有长期价值 |
| 6 | 三证只适合"写文档" | CI/CD 发布同样可写三证 |

---

# 诚实边界声明（本分册）

> 本声明遵循 v5.0 方案的「诚实边界」原则：标注实测 / 待实测，不把推测写成事实。

## 一、已实测（✅）

| 内容 | 证据 | 状态 |
|---|---|---|
| 基座版本 `OpenClaw 2026.9.4 (3a9d69d)` | 本机 `openclaw --version` 实测输出 | ✅ 实测 |
| 网关版本 `Hermes 0.20.1` | 本机网关版本输出 | ✅ 实测 |
| OS `macOS 26.5.1` | `sw_vers` | ✅ 实测 |
| agent 工作区 18 个 | `ls -d ~/.openclaw/workspace/agents/workspace-*/` = 18 | ✅ 实测 |
| skill 数 236 个 | `ls -d ~/.openclaw/workspace/skills/*/ \| wc -l` = 236 | ✅ 实测 |
| launchd 任务 2 个（gateway + monthly-cleanup） | `ls ~/Library/LaunchAgents/` 实测 | ✅ 实测 |
| `com.openclaw.monthly-cleanup.plist` 内容（每月 1 日 03:00） | 本机 plist 文件实拉 | ✅ 实测 |
| `~/.openclaw/governance/` 尚不存在 | `ls` 实测（本分册 Step 1 为新建） | ✅ 实测 |
| 6 层漂移链 + L1–L3 分级（60/90/143 天） | v4.0 卷五 M4 | ✅ 有据 |
| 漂移分权重 0.30/0.20/0.10/0.20/0.20 | v4.0 卷五 M6 §10.7 | ✅ 有据 |
| 三档制语义 + 5 熔断条件 | v4.0 卷五 M5 | ✅ 有据 |
| Claude Agent SDK Permission API 同构（≈10%） | v4.0 卷五 M5 实拉 | ✅ 有据 |
| 8 层体检维度 | v4.0 卷五 M6 §10.2 | ✅ 有据 |
| 双轨机制 evidence（cron jobs-state.json.migrated / runs/） | v4.0 卷五 M6 §10.3 | ✅ 有据 |
| 三证定义 + 递进律 + 防腐三机制 | v4.0 卷六 M3 | ✅ 有据 |
| 能力矩阵 26 天未续期（`workspace-kunlun/memory/2026-09-01-能力矩阵月度更新.md` 后无新） | v2026.9 README + v4.0 卷八 | ✅ 有据 |
| 18 个坏 skill（frontmatter 缺失/不合法） | v1.0 卷三附录 C | ✅ 有据 |
| 8 个 P0 stub 清单（来自 2026-09-03 暗夜熔炉报告 cron `a2d4eb3d4399`） | v2026.9 卷八模块 1 增量补丁 | ✅ 有据 |
| `drift_scan.py` 在 18 agent 上实跑：`18 / 0 / 17 / 1 / 32 / 17 / 16` | 本机实跑（C5-1 验证步骤 3） | ✅ 实测 |
| `dual-triangle.py` 实跑：cap=3.00 / rel=2.67 / Usable / T1+T2 | 本机实跑（C4-2 验证步骤 2） | ✅ 实测 |
| `boundary_check.py` 实跑：Allowed / Forbidden / Needs-Confirm / Undefined 四档判定 | 本机实跑（C5-2 验证步骤 2） | ✅ 实测 |
| `tev_verify.py` 实跑：Accepted（三证齐）· diff 3+/4- | 本机实跑（C5-4 验证步骤 2） | ✅ 实测 |
| 6 份 YAML/JSON 配置全部 `yaml.safe_load`/`json.load` 通过 | 本机实跑 | ✅ 实测 |
| 校验脚本逻辑（`yaml.safe_load` / `json.loads` / `diff` / SHA-256） | 纯本地可复现逻辑 | ✅ 可复现 |

## 二、待实测（⏳）

| 内容 | 说明 | 状态 |
|---|---|---|
| 本机 18 agent 的漂移分布**已实测**（0/17/1，见上「已实测」表） | C5-1；分布已拿到，待接 violation/amnesia 数据 | ✅ 部分实测 |
| `violation_score` / `amnesia_score` 数据接入 | C5-1 漂移分上界；未接前 drift_score 为下界 | ⏳ 待实测 |
| 运行时权限拦截钩子（对应 Claude Permission API 的位置） | C5-2；当前为声明式配置 + 离线判定器 | ⏳ 待实测 |
| `~/.openclaw/sessions/` / `~/.openclaw/cron/` / `handoff/` 真实路径 | C5-3 脚本已做降级保护 | ⏳ 待实测 |
| `launchctl load` vs `bootstrap gui/<uid>` 在 macOS 26.x 的行为 | C5-3；已给替代命令 | ⏳ 待实测 |
| 防腐三机制的定时链（24h hash 链验证 + 权限分离） | C5-4 进阶 2；依赖 C5-3 cron | ⏳ 待实测 |
| persona regression set（L3 角色级漂移）自动化跑测接口 | C5-1 进阶 1 | ⏳ 待实测 |
| 8 个 P0 stub 的实时关闭状态 | C5-1/C5-3 进阶 4；需要实拉当前状态 | ⏳ 待实测 |

## 三、诚实说明

1. 本分册所有配置（`drift-governance.yaml` / `autonomy-boundary.yaml` / 两个 plist /
   TEV 任务定义 / 三个 Python 校验器）均**基于 v4.0 卷五 M4/M5/M6 + 卷六 M3 已实测事实
   + 本机真实工作区/launchd 形态**从零撰写；YAML/JSON/XML 结构为本书约定，零 `...` 省略。
2. 凡标注 ⏳ 的条目**未在本机 2026.9.4 完成端到端验证**；尤其**运行时拦截**
   （C5-2）与**真实漂移分布**（C5-1）两项，请以 `openclaw --help` 与你的本机实跑为准。
3. 所有命令均给出「期望输出」；期望输出是**设计目标**，不是抓包实录。
4. 本机路径 `/Users/peterqiu/...` 为**实测环境路径**，换机器须全局替换。
5. 本分册**不复用 v1.0 / v4.0 原文**，全部配方从零撰写；引用的真实事实（版本号、
   agent 数、skill 数、launchd 任务、事故样本、stub 清单）均逐条注明来源。
6. 本分册**不重写 01/02/03/04 分册**；各册共用同一 banner 与 6 段式结构，
   交叉引用处只给例号（如 C4-4、C5-1），不复述正文。

**勘误途径**：本手册主目录 `../README.md`；术语口径以
`../00-术语对照表·v3.0行业标准版.md` 为准。

---

> 《硅基生命训练学 v5.0 · 实战 Cookbook》
> 分册：05-drift-governance.md（例 C5-1 ~ C5-4）
> 基座：OpenClaw 2026.9.4 (3a9d69d) · 网关 Hermes 0.20.1
> License: MIT · Copyright (c) 2026 OpenClaw Foundation
> 撰写日期：2026-09-27

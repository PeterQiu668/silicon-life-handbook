#!/usr/bin/env python3
"""
check-skill-frontmatter.py — SKILL.md frontmatter 批量校验（可直接跑）

用法：
    python3 check-skill-frontmatter.py                 # 默认 ~/.openclaw/workspace/skills
    python3 check-skill-frontmatter.py /path/to/skills
    python3 check-skill-frontmatter.py --json          # 机器可读输出

校验项（对应手册 附录 06 §06.2 / §06.3）：
    1. SKILL.md 是否存在
    2. frontmatter 是否存在且在第一行（`---` 必须第 1 行）
    3. name 字段：存在 / kebab-case / <=64 字符 / 等于父目录名
    4. description 字段：存在 / <=1024 字符 / 含触发词
    5. 可选字段类型：license / compatibility(<=500) / metadata(string->string)
    6. allowed-tools 用空格分隔（不是逗号）
    7. 术语双写：检出内部黑话单写（军团/监军/让位协议/整改单/三证验真）
退出码：0 = 无 error；1 = 存在 error

依赖：仅标准库（无需 PyYAML；用轻量 6 字段解析器）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

REQUIRED = ("name", "description")
BLACKSLANG = ("军团", "监军", "让位协议", "整改单", "三证验真")
TRIGGER_HINTS = ("use when", "when the user", "当用户", "使用场景", "触发", "when ")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

SEV_ORDER = {"ok": 0, "info": 1, "warn": 2, "error": 3}


def split_frontmatter(text: str):
    """返回 (has_frontmatter, fm_lines, body_lines)。要求 `---` 必须在第 1 行。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False, [], lines
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return True, lines[1:i], lines[i + 1:]
    return False, [], lines


def parse_top_level(fm_lines):
    """
    轻量解析：只取顶层 `key: value`（不处理嵌套 map 的深层值，
    但会把 metadata 的缩进子行原样收集）。
    返回 (top: dict[str,str], nested: dict[str,list[str]])
    """
    top, nested = {}, {}
    cur = None
    for raw in fm_lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if re.match(r"^\s", raw) and cur:                 # 缩进行 → 属于上一个 key
            nested.setdefault(cur, []).append(raw.strip())
            continue
        m = re.match(r"^([A-Za-z0-9_.\-]+)\s*:\s*(.*)$", raw)
        if not m:
            cur = None
            continue
        cur = m.group(1)
        val = m.group(2).strip().strip("'\"")
        top[cur] = val
    return top, nested


def check_dir(d: Path):
    issues = []
    skill_md = d / "SKILL.md"
    if not skill_md.is_file():
        return "error", [{"code": "NO_SKILL_MD", "msg": "缺 SKILL.md"}]

    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return "error", [{"code": "READ_FAIL", "msg": str(e)}]

    has_fm, fm_lines, body = split_frontmatter(text)
    if not has_fm:
        return "error", [{"code": "NO_FRONTMATTER", "msg": "无 frontmatter 或 `---` 不在第 1 行"}]

    top, nested = parse_top_level(fm_lines)

    for k in REQUIRED:
        if k not in top or not top[k]:
            issues.append({"code": "MISSING_FIELD", "msg": f"缺必填字段 {k}"})

    name = top.get("name", "")
    if name:
        if len(name) > 64:
            issues.append({"code": "NAME_TOO_LONG", "msg": f"name 超 64 字符（{len(name)}）"})
        if not NAME_RE.match(name):
            issues.append({"code": "NAME_CHARSET", "msg": f"name 非法字符/格式：{name}"})
        if name != d.name:
            issues.append({"code": "NAME_DIR_MISMATCH",
                           "msg": f"name({name}) != 目录名({d.name})"})

    desc = top.get("description", "")
    if desc:
        if len(desc) > 1024:
            issues.append({"code": "DESC_TOO_LONG", "msg": f"description 超 1024 字符（{len(desc)}）"})
        if len(desc) < 80:
            issues.append({"code": "DESC_SHORT", "msg": f"description 过短（{len(desc)}）",
                           "severity": "warn"})
        blob = (desc + "\n" + "\n".join(nested.get("description", []))).lower()
        if not any(h.strip() in blob for h in TRIGGER_HINTS):
            issues.append({"code": "DESC_NO_TRIGGER",
                           "msg": "description 缺触发词（Use when / 当用户 / 使用场景）",
                           "severity": "warn"})

    compat = top.get("compatibility", "")
    if compat and len(compat) > 500:
        issues.append({"code": "COMPAT_TOO_LONG", "msg": f"compatibility 超 500 字符（{len(compat)}）"})

    # metadata 必须是 string -> string（子行值不应是裸数字/布尔）
    if "metadata" in top and nested.get("metadata"):
        for line in nested["metadata"]:
            if re.match(r"^-?\d+(\.\d+)?$", line.split(":", 1)[-1].strip()) or \
               re.match(r"^(true|false)$", line.split(":", 1)[-1].strip(), re.I):
                issues.append({"code": "META_UNQUOTED",
                               "msg": f"metadata 值未加引号（应为 string）：{line}",
                               "severity": "warn"})

    at = top.get("allowed-tools", "")
    if at and "," in at:
        issues.append({"code": "ALLOWED_TOOLS_COMMA", "msg": "allowed-tools 应为空格分隔，检测到逗号"})

    joined = "\n".join(fm_lines + body)
    for w in BLACKSLANG:
        if w in joined:
            issues.append({"code": "TERM_SINGLE_WRITE",
                           "msg": f"术语单写（应双写）：{w}", "severity": "info"})

    worst = "ok"
    for i in issues:
        sev = i.get("severity", "error")
        if SEV_ORDER[sev] > SEV_ORDER[worst]:
            worst = sev
    return worst, issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=os.path.expanduser("~/.openclaw/workspace/skills"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"ERROR: 目录不存在: {root}", file=sys.stderr)
        return 1

    dirs = sorted(p for p in root.iterdir() if p.is_dir())
    stats = {"dirs": len(dirs), "ok": 0, "info": 0, "warn": 0, "error": 0}
    codes = {}
    report = []

    for d in dirs:
        sev, issues = check_dir(d)
        stats[sev] += 1
        for i in issues:
            codes[i["code"]] = codes.get(i["code"], 0) + 1
        if issues:
            report.append({"dir": d.name, "severity": sev, "issues": issues})

    out = {"root": str(root), "stats": stats, "by_code": dict(sorted(codes.items(), key=lambda x: -x[1])), "findings": report}
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"root: {root}")
        print(f"目录数: {stats['dirs']}")
        print(f"  ok    : {stats['ok']}")
        print(f"  info  : {stats['info']}")
        print(f"  warn  : {stats['warn']}")
        print(f"  error : {stats['error']}")
        print("\n按问题码统计:")
        for k, v in out["by_code"].items():
            print(f"  {k:22s} {v}")
        print("\n前 20 条明细:")
        for r in report[:20]:
            print(f"[{r['severity']:5s}] {r['dir']}")
            for i in r["issues"]:
                print(f"        - {i['code']}: {i['msg']}")
    return 1 if stats["error"] else 0


if __name__ == "__main__":
    sys.exit(main())

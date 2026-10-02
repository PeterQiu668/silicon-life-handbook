#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""实测 ~/.openclaw/workspace/skills/ 下全部 skill 目录的 6 字段覆盖数。
6 字段定义（来自 SKILL.md-frontmatter-规范.md §2 / Registry-表.md §6 雷达图）：
  name / description / license / compatibility / metadata / allowed-tools
"""
import os
import re
import json
import collections

SKILLS_DIR = os.path.expanduser("~/.openclaw/workspace/skills")
FIELDS = ["name", "description", "license", "compatibility", "metadata", "allowed-tools"]


def split_frontmatter(text):
    """返回 (has_fm, fm_text)。frontmatter 必须以 --- 开头的第一行开始。"""
    if not text.startswith("---"):
        # 容忍 BOM
        if text.startswith("\ufeff---"):
            text = text[1:]
        else:
            return False, ""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False, ""
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return True, "\n".join(lines[1:i])
    return False, ""


def top_level_keys(fm):
    """抽取 frontmatter 顶层 key（不进入缩进块）。"""
    keys = set()
    for line in fm.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] in (" ", "\t"):   # 缩进 = 子项，不算顶层
            continue
        m = re.match(r'^([A-Za-z0-9_.\-]+)\s*:', line)
        if m:
            keys.add(m.group(1))
    return keys


def main():
    entries = sorted(os.listdir(SKILLS_DIR))
    dirs = [e for e in entries if os.path.isdir(os.path.join(SKILLS_DIR, e))]
    files = [e for e in entries if not os.path.isdir(os.path.join(SKILLS_DIR, e))]

    rows = []
    no_skill_md = []
    no_frontmatter = []
    name_mismatch = []          # name != 目录名
    no_name_field = []

    for d in dirs:
        p = os.path.join(SKILLS_DIR, d, "SKILL.md")
        if not os.path.isfile(p):
            # 也容忍 skill.md 小写
            p2 = os.path.join(SKILLS_DIR, d, "skill.md")
            if os.path.isfile(p2):
                p = p2
            else:
                no_skill_md.append(d)
                rows.append((d, 0, set(), "NO_SKILL_MD"))
                continue
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
        except Exception as e:
            rows.append((d, 0, set(), "READ_ERR"))
            continue
        has_fm, fm = split_frontmatter(text)
        if not has_fm:
            no_frontmatter.append(d)
            rows.append((d, 0, set(), "NO_FRONTMATTER"))
            continue
        keys = top_level_keys(fm)
        present = {f for f in FIELDS if f in keys}
        status = "OK"
        if "name" not in keys:
            no_name_field.append(d)
            status = "NO_NAME_FIELD"
        else:
            m = re.search(r'^name\s*:\s*["\']?([^"\'\n#]+)', fm, re.M)
            val = m.group(1).strip() if m else ""
            if val != d:
                name_mismatch.append((d, val))
                status = "NAME_MISMATCH"
        rows.append((d, len(present), present, status))

    # ---- 统计 ----
    cov_counter = collections.Counter(r[1] for r in rows)
    print("=" * 70)
    print("口径 A) 文件系统条目（含非目录文件）: %d" % len(entries))
    print("口径 B) 纯 skill 目录               : %d" % len(dirs))
    print("口径 B2) 非目录文件                 : %d  %s" % (len(files), files))
    print("含 ^name: frontmatter 的 SKILL.md   : %d" % len([r for r in rows if "name" in r[2]]))
    print("有 SKILL.md 但无 frontmatter        : %d" % len(no_frontmatter))
    print("无 SKILL.md                         : %d" % len(no_skill_md))
    print("有 frontmatter 但无 name: 字段       : %d" % len(no_name_field))
    print("有 name 但 name != 目录名            : %d" % len(name_mismatch))
    print("=" * 70)
    print("字段覆盖分布 (6 字段: %s):" % " / ".join(FIELDS))
    for k in sorted(cov_counter, reverse=True):
        print("  %d/6 : %d 个" % (k, cov_counter[k]))
    print("=" * 70)

    # top 排序
    print("6/6 全字段 skill（%d 个）:" % cov_counter[6])
    for r in sorted([r for r in rows if r[1] == 6]):
        print("  - %s" % r[0])
    print("5/6 skill（%d 个）:" % cov_counter[5])
    for r in sorted([r for r in rows if r[1] == 5]):
        print("  - %s  (缺 %s)" % (r[0], "、".join(sorted(set(FIELDS) - r[2]))))

    # 逐字段统计
    print("=" * 70)
    print("逐字段填写率（分母 = 纯目录 %d / 分子 = 有 frontmatter 且含该字段）:" % len(dirs))
    for f in FIELDS:
        n = len([r for r in rows if f in r[2]])
        print("  %-14s : %3d  (%.1f%%)" % (f, n, 100.0 * n / len(dirs)))

    # 目标 9 样本
    print("=" * 70)
    targets = ["accounting", "agent-network", "agent-skills-audit", "skill-security-audit-v2",
               "silicon-performance-reviewer", "skill-gap-analyzer", "abm-sales-enablement",
               "bazi-fortune", "compliance-officer"]
    print("任务点名的 9 个样本实测：")
    rmap = {r[0]: r for r in rows}
    for t in targets:
        if t in rmap:
            r = rmap[t]
            print("  %-30s %d/6  [%s]  %s" % (t, r[1], r[3], ",".join(sorted(r[2]))))
        else:
            print("  %-30s ❌ 目录不存在" % t)

    print("=" * 70)
    print("违例清单：")
    print("  name != 目录名 (%d):" % len(name_mismatch))
    for d, v in name_mismatch:
        print("    - 目录 %s  →  name: %s" % (d, v))
    print("  有 SKILL.md 但完全无 frontmatter (%d):" % len(no_frontmatter))
    for d in no_frontmatter:
        print("    - %s" % d)
    print("  有 frontmatter 但无 name 字段 (%d):" % len(no_name_field))
    for d in no_name_field:
        print("    - %s" % d)
    print("  无 SKILL.md (%d): %s" % (len(no_skill_md), no_skill_md))

    # 落盘 JSON 供后续引用
    out = {
        "口径A_条目": len(entries),
        "口径B_纯目录": len(dirs),
        "非目录文件": files,
        "有name字段": len([r for r in rows if "name" in r[2]]),
        "NO_FRONTMATTER": no_frontmatter,
        "NO_FRONTMATTER_数": len(no_frontmatter),
        "无SKILL_MD": no_skill_md,
        "无name字段": no_name_field,
        "name违例": name_mismatch,
        "name违例数": len(name_mismatch),
        "覆盖分布": {str(k): v for k, v in sorted(cov_counter.items(), reverse=True)},
        "全字段6": [r[0] for r in rows if r[1] == 6],
        "5字段": [r[0] for r in rows if r[1] == 5],
        "逐字段": {f: len([r for r in rows if f in r[2]]) for f in FIELDS},
        "样本9": {t: ({"cov": rmap[t][1], "keys": sorted(rmap[t][2]), "status": rmap[t][3]} if t in rmap else None) for t in targets},
    }
    with open("/tmp/skill_field_measure.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\nJSON 已落盘：/tmp/skill_field_measure.json")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fence-aware classifier: narrative vs attachment sections (real H2 only)."""
import re, sys, os

ATTACH_PAT = re.compile(r'^(SOP|诚实边界|常见错误|新手坑|扩展阅读|附录|步骤|训练目标|操作流程|脚本|实现|交付清单)')
FENCE = re.compile(r'^\s*(```|~~~)')

def classify(t):
    t2 = re.sub(r'^[0-9]+\.[0-9]+\s*', '', t.strip())
    t2 = re.sub(r'^SOP\s*·\s*', '', t2)
    return 'attach' if (ATTACH_PAT.match(t2) or ATTACH_PAT.match(t.strip())) else 'narr'

def analyze(path):
    lines = open(path, encoding='utf-8').readlines()
    n = len(lines)
    secs, fence = [], False
    for i, ln in enumerate(lines):
        if FENCE.match(ln):
            fence = not fence
            continue
        if not fence and ln.startswith('## ') and not ln.startswith('### '):
            secs.append((i, ln[3:].strip()))
    secs.append((n, '__EOF__'))
    narr = attach = 0
    rows = []
    for j in range(len(secs)-1):
        start, title = secs[j]; end = secs[j+1][0]
        cnt = end - start; c = classify(title)
        narr += cnt if c == 'narr' else 0
        attach += cnt if c == 'attach' else 0
        rows.append((start+1, end, cnt, c, title))
    return rows, narr, attach, n

if __name__ == '__main__':
    for path in sys.argv[1:]:
        rows, narr, attach, n = analyze(path)
        tot = narr + attach
        print(f"\n########## {os.path.basename(path)}  (total {n}) ##########")
        for a, b, c, cl, t in rows:
            print(f"  L{a:>5}-{b:<5} ({c:>4}) [{'NARR' if cl=='narr' else 'ATT '}] {t}")
        print(f"  --> NARR={narr} ({narr/tot*100:.1f}%)  ATTACH={attach} ({attach/tot*100:.1f}%)")

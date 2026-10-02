#!/usr/bin/env python3
"""Extract verbatim appendix blocks + kept narrative from v5.0 chapters (B3)."""
import os, sys, io

BASE = os.path.expanduser("~/.openclaw/workspace/references/silicon-life-handbook/"
                          "openclaw-silicon-life-handbook-v2026.9-industry-standard/chapters")
OUT = os.path.expanduser("~/.openclaw/workspace/scratch/b3")
os.makedirs(OUT, exist_ok=True)

# ranges are 1-indexed inclusive
PLAN = {
 '07': dict(
   src='07-coordination/07-协同军团.md',
   narr=[(230,364),(672,788)],
   app=[(1,150),(151,229),(365,382),(383,671),(789,1010),(1011,1134)],
 ),
 '08': dict(
   src='08-evolution/08-超维演进.md',
   narr=[(229,348),(356,371),(452,759)],
   app=[(1,152),(153,228),(349,355),(372,451),(760,967),(968,1086)],
 ),
 '09': dict(
   src='09-mcp-binding/09-MCP绑定.md',
   narr=[(243,360),(1204,2353)],
   app=[(1,163),(164,242),(361,370),(371,842),(843,1048),(1049,1203)],
 ),
 '10': dict(
   src='10-a2a-binding/10-A2A绑定.md',
   narr=[(211,330),(1166,2797)],
   app=[(1,131),(132,210),(331,340),(341,793),(794,1011),(1012,1165)],
 ),
 '11': dict(
   src='11-skill-registry/README.md',
   narr=[(233,359),(388,426)],
   app=[(1,67),(68,70),(71,147),(148,232),(360,363),(364,387),(427,440),
        (441,641),(642,667),(668,673),(674,909),(910,1140),(1141,1278)],
 ),
 '12': dict(
   src='12-plugin-entrypoint/README.md',
   narr=[(230,549),(576,596)],
   app=[(1,141),(142,229),(550,575),(597,1054),(1055,1265),(1266,1413)],
 ),
}

def read(p):
    with open(p, encoding='utf-8') as f:
        return f.readlines()

def grab(lines, a, b):
    return ''.join(lines[a-1:b])

if __name__ == '__main__':
    for k, p in PLAN.items():
        lines = read(os.path.join(BASE, p['src']))
        n = len(lines)
        narr = ''.join(grab(lines, a, b) for a, b in p['narr'])
        app = ''.join(grab(lines, a, b) for a, b in p['app'])
        with open(f'{OUT}/ch{k}.appendix.md', 'w', encoding='utf-8') as f:
            f.write(app)
        with open(f'{OUT}/ch{k}.narr_keep.md', 'w', encoding='utf-8') as f:
            f.write(narr)
        print(f"ch{k}: src {n} lines -> narr_keep {narr.count(chr(10))} lines, appendix {app.count(chr(10))} lines")

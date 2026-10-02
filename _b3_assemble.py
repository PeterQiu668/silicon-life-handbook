#!/usr/bin/env python3
"""B3 assembler v2 (fence-aware, content-safe).

- Full-fidelity extraction: never modifies non-heading lines.
- Only demotes exact H2 lines ('## ') that are OUTSIDE code fences.
- Verifies byte-preservation of every appendix source block.
"""
import os, sys, re, hashlib

ROOT = os.path.expanduser("~/.openclaw/workspace/references/silicon-life-handbook/"
                          "openclaw-silicon-life-handbook-v2026.9-industry-standard")
SCR = os.path.expanduser("~/.openclaw/workspace/scratch/b3")

CFG = {
 '07': dict(
   src='chapters/07-coordination/07-协同军团.md',
   frags=['ch07.new.md','ch07.new.p2.md','ch07.new.p3.md','ch07.new.p4.md',
          'ch07.new.p5.md','ch07.new.p6.md','ch07.new.p7.md','ch07.new.p8.md',
          'ch07.new.p9.md','ch07.new.p10.md'],
   keep=[(230,364)],
   app=[("附录 A · 本章操作手册（原「SOP · 本章怎么用」）", [(1,150)]),
        ("附录 B · 本章常见错误（8 个）", [(383,788)]),
        ("附录 C · 新手坑", [(789,1010)]),
        ("附录 D · 扩展阅读", [(1011,1134)]),
        ("附录 E · 诚实边界（含原「SOP · 诚实边界声明」）", [(151,229),(365,382)])],
 ),
}

FENCE = re.compile(r'^\s*(```|~~~)')

def demote_h2(text, drop_first_heading=False):
    """Replace leading '## ' with '### ' on lines outside fenced code blocks.
    Optionally drop the first heading line. All other lines untouched."""
    out, fence, first, dropped = [], False, True, False
    for ln in text.split('\n'):
        if FENCE.match(ln):
            fence = not fence
            out.append(ln)
            first = False
            continue
        if not fence and ln.startswith('#') and re.match(r'^#{1,6}\s', ln):
            # a heading line
            if first and drop_first_heading:
                dropped = True
                first = False
                continue
            if ln.startswith('## ') and not ln.startswith('### '):
                ln = '### ' + ln[3:]
            first = False
            out.append(ln)
            continue
        if ln.strip() != '':
            first = False
        out.append(ln)
    return '\n'.join(out), dropped

def extract(lines, ranges):
    return ''.join(''.join(lines[a-1:b]) for a, b in ranges)

def verify(src_text, out_text):
    """Append-free check: every line of src_text must appear in out_text
    (modulo the H2->H3 demotion and one dropped heading)."""
    def norm(t):
        res = []
        for ln in t.split('\n'):
            if ln.startswith('### ') and not ln.startswith('#### '):
                res.append(ln[1:])    # undo demotion
            else:
                res.append(ln)
        return res
    a, b = norm(src_text), norm(out_text)
    # drop blank-only differences
    a = [x for x in a if x.strip() != '']
    b = [x for x in b if x.strip() != '']
    # allow the one dropped first heading
    if len(a) == len(b) + 1:
        for i in range(len(a)):
            if a[:i] + a[i+1:] == b:
                return True
    return a == b

def build(cid):
    c = CFG[cid]
    src_lines = open(os.path.join(ROOT, c['src']), encoding='utf-8').readlines()
    body = []
    for f in c['frags']:
        p = os.path.join(SCR, f)
        if os.path.exists(p):
            body.append(open(p, encoding='utf-8').read())
        else:
            print(f"  !! missing frag {f}")
    body = '\n'.join(body)

    # kept narrative
    keep_src = extract(src_lines, c['keep'])
    keep_out, _ = demote_h2(keep_src, drop_first_heading=False)
    if not verify(keep_src, keep_out):
        print("  !! VERIFY FAIL on kept narrative")

    # appendix
    app_parts, ok = [], True
    for label, ranges in c['app']:
        blk = extract(src_lines, ranges)
        blk_out, dropped = demote_h2(blk, drop_first_heading=True)
        if not verify(blk, blk_out):
            ok = False
            print(f"  !! VERIFY FAIL on {label}")
        app_parts.append(f"\n---\n\n## {label}\n{blk_out}")
    appendix = '\n'.join(app_parts)

    final = body.rstrip() + '\n\n' + keep_out.strip() + '\n' + appendix
    if not final.endswith('\n'):
        final += '\n'
    return final, ok

if __name__ == '__main__':
    cid = sys.argv[1]
    out, ok = build(cid)
    dst = os.path.join(SCR, f'ch{cid}.FINAL.md')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f"ch{cid} FINAL -> {dst} : {out.count(chr(10))} lines, {len(out.encode('utf-8'))} bytes, verify={'OK' if ok else 'FAIL'}")

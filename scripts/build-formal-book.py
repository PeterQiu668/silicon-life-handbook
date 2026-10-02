#!/usr/bin/env python3
"""Assemble the manifest-driven formal manuscript and embedded resources."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
OUTPUT = MANUSCRIPT / "99-complete-manuscript.md"
MANIFEST = ROOT / "BOOK-MANIFEST.yaml"
CHAPTER_RE = re.compile(r"^C(?P<id>\d{2})-")
MARKDOWN_LINK_RE = re.compile(r"(?P<prefix>!?)\[(?P<label>[^\]]*)\]\((?P<target>[^)]+)\)")


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text.strip()
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated frontmatter")
    return text[end + 5 :].strip()


def rebase_local_links(text: str, source: Path) -> str:
    """Keep source-relative local links valid inside the assembled manuscript."""

    def replace(match: re.Match[str]) -> str:
        raw = match.group("target").strip()
        if not raw or raw.startswith("#") or "://" in raw or raw.startswith("mailto:"):
            return match.group(0)
        path_part, separator, anchor = raw.partition("#")
        decoded = unquote(path_part)
        absolute = (source.parent / decoded).resolve()
        relative = os.path.relpath(absolute, OUTPUT.parent).replace(os.sep, "/")
        rebased = relative + (separator + anchor if separator else "")
        if " " in rebased:
            rebased = f"<{rebased}>"
        return f'{match.group("prefix")}[{match.group("label")}]({rebased})'

    return MARKDOWN_LINK_RE.sub(replace, text)


def chapter_sources() -> list[Path]:
    manifest_text = MANIFEST.read_text(encoding="utf-8")
    count_match = re.search(r"^  chapters:\s*(?P<count>\d+)\s*$", manifest_text, re.MULTILINE)
    if not count_match:
        raise ValueError("BOOK-MANIFEST.yaml architecture.chapters is missing")
    expected_count = int(count_match.group("count"))
    found: dict[int, Path] = {}
    for path in MANUSCRIPT.glob("volume-*/C??-*/chapter.md"):
        match = CHAPTER_RE.match(path.parent.name)
        if not match:
            continue
        chapter_id = int(match.group("id"))
        if chapter_id in found:
            raise ValueError(f"duplicate chapter C{chapter_id:02d}")
        found[chapter_id] = path
    missing = sorted(set(range(1, expected_count + 1)) - set(found))
    if missing:
        raise ValueError("missing chapters: " + ", ".join(f"C{x:02d}" for x in missing))
    extra = sorted(set(found) - set(range(1, expected_count + 1)))
    if extra:
        raise ValueError("unexpected chapters: " + ", ".join(f"C{x:02d}" for x in extra))
    return [found[index] for index in range(1, expected_count + 1)]


def exercise_sources() -> list[Path]:
    def key(path: Path) -> tuple[int, str]:
        match = re.search(r"C(?P<id>\d{2})", path.name)
        if not match:
            raise ValueError(f"exercise filename has no chapter id: {path}")
        return int(match.group("id")), path.name

    return sorted(MANUSCRIPT.glob("volume-*/C??-*/exercises/*.md"), key=key)


def core_artifact_sources() -> list[Path]:
    manifest_text = MANIFEST.read_text(encoding="utf-8")
    ids = re.findall(r'^\s+-\s+"(A-C\d{2}-\d{2})"\s*$', manifest_text, re.MULTILINE)
    found: dict[str, Path] = {}
    for path in MANUSCRIPT.glob("volume-*/C??-*/artifacts/*.md"):
        match = re.match(r"(?P<id>A-C\d{2}-\d{2})", path.name)
        if match:
            found[match.group("id")] = path
    missing = [artifact_id for artifact_id in ids if artifact_id not in found]
    if missing:
        raise ValueError("missing core artifact templates: " + ", ".join(missing))
    return [found[artifact_id] for artifact_id in ids]


def appendix_sources() -> list[Path]:
    appendix_dir = MANUSCRIPT / "appendices"
    paths = sorted(appendix_dir.glob("[A-I]-*.md"))
    letters = [path.name[0] for path in paths]
    if letters != list("ABCDEFGHI"):
        raise ValueError(f"appendix set must be A-I, got {letters}")
    return paths


def build() -> str:
    appendices = appendix_sources()
    volume_zero = ROOT / "part-I-getting-started" / "00-formal-volume-zero.md"
    sources = [
        MANUSCRIPT / "00-frontmatter.md",
        volume_zero,
        *chapter_sources(),
        *appendices,
        *exercise_sources(),
        *core_artifact_sources(),
        MANUSCRIPT / "90-backmatter.md",
    ]
    missing = [path for path in sources if not path.is_file()]
    if missing:
        raise ValueError("missing sources: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))
    header = """---
document_id: COMPLETE-MANUSCRIPT
title: 训虾手册：硅基生命训练学
subtitle: AI Agent 训练与人机协同最佳实践指南
status: formal_candidate
edition: 2026.10-training-science-candidate
generated_from: canonical_chapter_and_appendix_packages
verified_on: 2026-10-01
---

> 本文件由 `scripts/build-formal-book.py` 从正式前言、卷零、27 个章节包、附录 A—I、55 个练习、20 件核心产物模板与结语机械合成。请修改源文件，不要直接修改本文件。
"""
    parts = [header.strip()]
    ordered_sources: list[tuple[Path, str | None]] = [
        (MANUSCRIPT / "00-frontmatter.md", None),
        (volume_zero, None),
        *((source, None) for source in chapter_sources()),
        (appendices[0], None),
        *((source, "exercise") for source in exercise_sources()),
        (appendices[1], None),
        *((source, "artifact") for source in core_artifact_sources()),
        *((source, None) for source in appendices[2:]),
        (MANUSCRIPT / "90-backmatter.md", None),
    ]
    inserted: set[str] = set()
    for source, group in ordered_sources:
        if group == "exercise" and group not in inserted:
            parts.append("## A.9　55 个正式练习全文\n\n以下练习均为书稿正式内容；真实平台、真实凭证和生产环境仍按各练习边界保持 `REVIEW_REQUIRED`。")
            inserted.add(group)
        if group == "artifact" and group not in inserted:
            parts.append("## B.9　20 件核心产物模板全文\n\n其余模板保留稳定 ID，作为在线配套资源发布；在线资源不自动获得真实实践或出版签字。")
            inserted.add(group)
        relative = source.relative_to(ROOT).as_posix()
        body = strip_frontmatter(source.read_text(encoding="utf-8"))
        parts.extend([f"<!-- BEGIN {relative} -->", rebase_local_links(body, source), f"<!-- END {relative} -->"])
    return "\n\n---\n\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when the saved assembly is missing or stale")
    args = parser.parse_args()
    content = build()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != content:
            print(f"STALE {OUTPUT.relative_to(ROOT)}")
            return 1
        print(f"PASS {OUTPUT.relative_to(ROOT)} is current")
        return 0
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"WROTE {OUTPUT.relative_to(ROOT)} ({len(content)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

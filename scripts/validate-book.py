#!/usr/bin/env python3
"""Dependency-free structural checks for the formal handbook publication layer."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_ROOT = ROOT / "manuscript"
MANUSCRIPT = MANUSCRIPT_ROOT / "99-complete-manuscript.md"
MANIFEST = ROOT / "BOOK-MANIFEST.yaml"
CANONICAL = [
    MANUSCRIPT,
    ROOT / "AGENT-ENTRY.md",
    ROOT / "SOURCES.md",
    ROOT / "EDITORIAL-AUDIT.md",
    ROOT / "docs/editorial/BOOK-QUALITY-STANDARD.md",
    ROOT / "docs/editorial/PRODUCTION-DASHBOARD.md",
    ROOT / "docs/editorial/FINAL-PUBLICATION-READINESS-2026-10-01.md",
    MANIFEST,
]

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
CHAPTER_BEGIN_RE = re.compile(
    r"<!-- BEGIN manuscript/volume-\d{2}/C(?P<id>\d{2})-[^/]+/chapter\.md -->"
)
APPENDIX_BEGIN_RE = re.compile(
    r"<!-- BEGIN manuscript/appendices/(?P<letter>[A-I])-[^/]+\.md -->"
)
EXCLUDED_NAMES = {
    "README-v3.0-archive.md",
    "README-v5.0A-original.md",
    "00-新书主编报告.md",
    "00-B-rebuild-overview.md",
}


def local_target(source: Path, raw: str) -> Path | None:
    target = raw.strip().split("#", 1)[0]
    if not target or "://" in target or target.startswith(("mailto:", "#")):
        return None
    return (source.parent / unquote(target)).resolve()


def scalar_path_values(text: str) -> list[str]:
    values: list[str] = []
    for line in text.splitlines():
        match = re.match(
            r'^\s*(?:human|agent|source_packages|sources|editorial_audit|quality_standard|production_dashboard|final_publication_readiness|framework|chapter_id_migration|manager_brief|frontmatter|backmatter|generated_complete_manuscript|standard|validator|formal_validator):\s*"([^"]+)"\s*$',
            line,
        )
        if match:
            values.append(match.group(1))
    return values


def main() -> int:
    errors: list[str] = []
    notes: list[str] = []

    for path in CANONICAL:
        if not path.is_file():
            errors.append(f"missing canonical file: {path.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1

    build_check = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build-formal-book.py"), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if build_check.returncode:
        errors.append("complete manuscript is missing or stale; run scripts/build-formal-book.py")
    else:
        notes.append("complete manuscript matches canonical source packages")

    source_check = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate-formal-manuscript.py"), "--strict"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if source_check.returncode:
        errors.append(
            "formal source packages failed strict validation; run "
            "scripts/validate-formal-manuscript.py --strict for details"
        )
    else:
        notes.append("formal source packages pass strict structural validation")

    manifest_text = MANIFEST.read_text(encoding="utf-8")
    chapter_count_match = re.search(r"^  chapters:\s*(\d+)\s*$", manifest_text, re.MULTILINE)
    volume_count_match = re.search(r"^  volumes:\s*(\d+)\s*$", manifest_text, re.MULTILINE)
    if not chapter_count_match or not volume_count_match:
        errors.append("manifest architecture is missing chapter/volume count")
        expected_chapters = 0
        expected_volumes = 0
    else:
        expected_chapters = int(chapter_count_match.group(1))
        expected_volumes = int(volume_count_match.group(1))
    for raw in scalar_path_values(manifest_text):
        if raw.startswith("python3 ") or raw.startswith("MAT-"):
            continue
        target = ROOT / raw
        if not target.exists():
            errors.append(f"manifest target missing: {raw}")

    chapter_paths = sorted(MANUSCRIPT_ROOT.glob("volume-*/C??-*/chapter.md"))
    volume_dirs = sorted(path for path in MANUSCRIPT_ROOT.glob("volume-*"))
    appendices = sorted((MANUSCRIPT_ROOT / "appendices").glob("[A-I]-*.md"))
    if len(volume_dirs) != expected_volumes:
        errors.append(f"formal source must contain {expected_volumes} numbered volumes, got {len(volume_dirs)}")
    if len(chapter_paths) != expected_chapters:
        errors.append(f"formal source must contain {expected_chapters} chapters, got {len(chapter_paths)}")
    if [path.name[0] for path in appendices] != list("ABCDEFGHI"):
        errors.append("formal source must contain appendices A-I exactly once")

    markdown_files = [
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
        and path.name not in EXCLUDED_NAMES
        and ".bak" not in path.name
        and "docs/plans/active" not in path.relative_to(ROOT).as_posix()
    ]
    checked_links = 0
    for source in markdown_files:
        text = CODE_FENCE_RE.sub("", source.read_text(encoding="utf-8", errors="replace"))
        for raw in LINK_RE.findall(text):
            target = local_target(source, raw)
            if target is None:
                continue
            checked_links += 1
            if not target.exists():
                errors.append(f"broken link: {source.relative_to(ROOT)} -> {raw}")

    manuscript_text = MANUSCRIPT.read_text(encoding="utf-8")
    chapter_ids = [int(match.group("id")) for match in CHAPTER_BEGIN_RE.finditer(manuscript_text)]
    appendix_letters = [match.group("letter") for match in APPENDIX_BEGIN_RE.finditer(manuscript_text)]
    if chapter_ids != list(range(1, expected_chapters + 1)):
        errors.append(f"assembled chapter order invalid: {chapter_ids}")
    if appendix_letters != list("ABCDEFGHI"):
        errors.append(f"assembled appendix order invalid: {appendix_letters}")
    required_parts = [
        "<!-- BEGIN manuscript/00-frontmatter.md -->",
        "<!-- BEGIN part-I-getting-started/00-formal-volume-zero.md -->",
        "<!-- BEGIN manuscript/90-backmatter.md -->",
        "Agent 阅读入口",
    ]
    for marker in required_parts:
        if marker not in manuscript_text:
            errors.append(f"assembled manuscript missing marker: {marker}")

    forbidden = [
        "一定行业最强",
        "必然行业最强",
        "业界唯一且无可替代",
        "保证绝对安全",
    ]
    negation_markers = ["不承诺", "不能承诺", "拒绝", "不得声称", "不应声称", "没有承诺"]
    for line_number, line in enumerate(manuscript_text.splitlines(), 1):
        for phrase in forbidden:
            if phrase in line and not any(marker in line for marker in negation_markers):
                errors.append(
                    f"unverifiable absolute claim in formal manuscript line {line_number}: {phrase}"
                )

    required_manifest_fragments = [
        'title: "训虾手册：硅基生命训练学"',
        'chapters: 27',
        'volume_zero: true',
        'body_third_level_sections: 202',
        'core_artifact_templates_in_book: 20',
        'exercises: 55',
        'appendices: 9',
        'implementation_baseline:',
        'version: "2026.9.6"',
        'release_tag: "v2026.9.6"',
        'commit: "eb377ac59e6c9fd6c7705028034812becf00271b"',
        'current_latest_snapshot:',
        'version: "2026.9.7"',
        'commit: "c074824a27c96d3983043f9eeb33823cd1772d8c"',
        'migration_status: "not_adopted_as_book_implementation_baseline"',
        'version: "0.20.1"',
        'release_tag: "v2026.8.13"',
        'commit: "f80f453ae0679347e38abc917c7f94f717bf96c5"',
        'protocol_version: "2026-07-28"',
        'release_version: "1.0.1"',
        'snapshot_commit: "69ef37e9424c0a7ea9dd2293b559e43ec8176379"',
        'core_semconv_version: "1.44.0"',
        'genai_snapshot_commit: "b31e9e8ea26ac1c086d3313d474e31d7c3f391ae"',
        'chapter_gates: [writing, fact, practice, cross, chief]',
        'final_publication_readiness: "docs/editorial/FINAL-PUBLICATION-READINESS-2026-10-01.md"',
        'formal_validator: "python3 scripts/validate-formal-manuscript.py --strict"',
        'status: formal_candidate',
    ]
    for fragment in required_manifest_fragments:
        if fragment not in manifest_text:
            errors.append(f"manifest missing required declaration: {fragment}")

    source_text = (ROOT / "SOURCES.md").read_text(encoding="utf-8")
    for source_id in ["S10", "S15", "S16", "S20", "S21", "S22", "S23", "S24"]:
        if f"### {source_id}" not in source_text:
            errors.append(f"source ledger missing {source_id}")

    notes.extend(
        [
            f"canonical files: {len(CANONICAL)}",
            f"formal volumes: {len(volume_dirs)}",
            f"formal chapters: {len(chapter_paths)}",
            f"formal appendices: {len(appendices)}",
            f"markdown files scanned: {len(markdown_files)}",
            f"local links checked: {checked_links}",
            f"complete manuscript lines: {len(manuscript_text.splitlines())}",
            f"complete manuscript chars: {len(manuscript_text)}",
        ]
    )

    for note in notes:
        print(f"OK {note}")
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print(f"FAIL {len(errors)} error(s)")
        return 1
    print("PASS formal publication layer is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

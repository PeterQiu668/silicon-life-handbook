#!/usr/bin/env python3
"""One-time mechanical migration for the 2026.10 twenty-seven-chapter edition.

This script preserves archived audits and logs. It migrates canonical manuscript
packages, current editorial contracts, and chapter research preflights only.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER = ROOT / ".chapter-id-migration-2026-10.done"
MAPPING = {old: old + 3 for old in range(10, 25)}


def rebuild_framework_v3() -> None:
    source = ROOT / "00-正式出版版-三级内容框架-v2.md"
    target = ROOT / "00-正式出版版-三级内容框架-v3.md"
    text = source.read_text(encoding="utf-8")

    replacements: dict[str, str] = {}
    for old, new in MAPPING.items():
        chapter_token = f"__FRAMEWORK_CHAPTER_{old:02d}__"
        text = re.sub(rf"第\s*{old}\s*章", chapter_token, text)
        replacements[chapter_token] = f"第 {new} 章"

        section_token = f"__FRAMEWORK_SECTION_{old:02d}__"
        text = re.sub(rf"^(####\s+){old}(\.[0-9]+)", rf"\1{section_token}\2", text, flags=re.MULTILINE)
        replacements[section_token] = str(new)

        id_token = f"__FRAMEWORK_ID_{old:02d}__"
        text = re.sub(rf"\bC{old:02d}\b", id_token, text)
        replacements[id_token] = f"C{new:02d}"

    for token, value in replacements.items():
        text = text.replace(token, value)
    target.write_text(text, encoding="utf-8")
    print("PASS rebuilt framework v3 from v2")


def replace_text(path: Path, *, local_old: int | None = None) -> None:
    text = path.read_text(encoding="utf-8")
    original = text

    # Protect path pairs before replacing generic chapter IDs.
    path_tokens: dict[str, str] = {}
    for old, new in MAPPING.items():
        old_volume = (old - 1) // 3 + 1
        new_volume = old_volume + 1
        token = f"__MIGRATION_PATH_{old:02d}__"
        text = text.replace(f"volume-{old_volume:02d}/C{old:02d}", token)
        path_tokens[token] = f"volume-{new_volume:02d}/C{new:02d}"

    # Stable placeholders avoid cascading C10 -> C13 -> C16.
    id_tokens: dict[str, str] = {}
    chapter_tokens: dict[str, str] = {}
    for old, new in MAPPING.items():
        id_token = f"__MIGRATION_C_{old:02d}__"
        text = re.sub(rf"\bC{old:02d}\b", id_token, text)
        id_tokens[id_token] = f"C{new:02d}"

        for spaced in (False, True):
            source = f"第{' ' if spaced else ''}{old}章"
            token = f"__MIGRATION_CHAPTER_{old:02d}_{int(spaced)}__"
            text = text.replace(source, token)
            chapter_tokens[token] = f"第{' ' if spaced else ''}{new}章"

    # Only the migrated package owns bare section numbers. Framework v3 owns all.
    if local_old is not None:
        new = MAPPING[local_old]
        text = re.sub(rf"^(#+\s+){local_old}(\.[0-9]+)", rf"\g<1>{new}\2", text, flags=re.MULTILINE)
        text = re.sub(rf"(?<![0-9]){local_old}(\.[0-9]+(?:\.[0-9]+)*)", rf"{new}\1", text)
    elif path.name == "00-正式出版版-三级内容框架-v3.md":
        for old, new in MAPPING.items():
            token = f"__MIGRATION_SECTION_{old:02d}__"
            text = re.sub(rf"^(####\s+){old}(\.[0-9]+)", rf"\1{token}\2", text, flags=re.MULTILINE)
            text = text.replace(token, str(new))

    for token, value in path_tokens.items():
        text = text.replace(token, value)
    for token, value in id_tokens.items():
        text = text.replace(token, value)
    for token, value in chapter_tokens.items():
        text = text.replace(token, value)

    if text != original:
        path.write_text(text, encoding="utf-8")


def rename_embedded_ids(package: Path, old: int, new: int) -> None:
    old_id = f"C{old:02d}"
    new_id = f"C{new:02d}"
    for path in sorted(package.rglob("*"), key=lambda item: len(item.parts), reverse=True):
        if old_id not in path.name:
            continue
        path.rename(path.with_name(path.name.replace(old_id, new_id)))


def main() -> int:
    if "--repair-framework" in sys.argv:
        rebuild_framework_v3()
        return 0
    if MARKER.exists():
        print("SKIP chapter ID migration already completed")
        return 0

    framework_v2 = ROOT / "00-正式出版版-三级内容框架-v2.md"
    framework_v3 = ROOT / "00-正式出版版-三级内容框架-v3.md"
    if not framework_v3.exists():
        shutil.copyfile(framework_v2, framework_v3)

    stage = ROOT / ".chapter-id-migration-stage"
    stage.mkdir(exist_ok=False)
    staged: dict[int, tuple[Path, str]] = {}

    for old in MAPPING:
        matches = list((ROOT / "manuscript").glob(f"volume-*/C{old:02d}-*"))
        if len(matches) != 1:
            raise RuntimeError(f"expected one C{old:02d} package, got {matches}")
        source = matches[0]
        staged_path = stage / source.name
        source.rename(staged_path)
        staged[old] = (staged_path, source.name.split("-", 1)[1])

    moved: dict[int, Path] = {}
    for old, (source, slug) in staged.items():
        new = MAPPING[old]
        destination_volume = ROOT / "manuscript" / f"volume-{((new - 1) // 3) + 1:02d}"
        destination_volume.mkdir(exist_ok=True)
        destination = destination_volume / f"C{new:02d}-{slug}"
        source.rename(destination)
        rename_embedded_ids(destination, old, new)
        moved[old] = destination
    stage.rmdir()

    # Rename current chapter research preflights. Historical logs and audits stay untouched.
    research = ROOT / "docs" / "research"
    for old in sorted(MAPPING, reverse=True):
        source_matches = list(research.glob(f"C{old:02d}-*-preflight.md"))
        if len(source_matches) == 1:
            source = source_matches[0]
            source.rename(source.with_name(source.name.replace(f"C{old:02d}", f"C{MAPPING[old]:02d}", 1)))

    canonical_files: set[Path] = {
        ROOT / "BOOK-MANIFEST.yaml",
        ROOT / "AGENT-ENTRY.md",
        ROOT / "manuscript" / "00-frontmatter.md",
        ROOT / "manuscript" / "90-backmatter.md",
        ROOT / "docs" / "editorial" / "CHAPTER-CARDS.md",
        framework_v3,
    }
    canonical_files.update((ROOT / "manuscript").glob("volume-*/C??-*/chapter.md"))
    canonical_files.update((ROOT / "manuscript").glob("volume-*/C??-*/*.yaml"))
    canonical_files.update((ROOT / "manuscript").glob("volume-*/C??-*/artifacts/*.md"))
    canonical_files.update((ROOT / "manuscript").glob("volume-*/C??-*/exercises/*.md"))
    canonical_files.update((ROOT / "manuscript" / "appendices").glob("*.md"))
    canonical_files.update(research.glob("C??-*-preflight.md"))

    for path in sorted(canonical_files):
        if not path.is_file():
            continue
        local_old = next((old for old, package in moved.items() if package in path.parents), None)
        replace_text(path, local_old=local_old)

    MARKER.write_text("2026-10-01\n", encoding="utf-8")
    print("PASS migrated C10-C24 to C13-C27")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the manifest-driven formal manuscript.

The validator is intentionally dependency-free. During production it accepts a
partial manuscript and reports missing chapter packages. With ``--strict`` it
requires all manifest-declared packages and release-candidate completeness.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "BOOK-MANIFEST.yaml"
FRAMEWORK = ROOT / "00-正式出版版-三级内容框架-v3.md"
MANUSCRIPT = ROOT / "manuscript"
FRONTMATTER = MANUSCRIPT / "00-frontmatter.md"
QUALITY = ROOT / "docs/editorial/BOOK-QUALITY-STANDARD.md"
TERMS = ROOT / "docs/editorial/TERMINOLOGY-REGISTRY.yaml"
CHAPTER_CARDS = ROOT / "docs/editorial/CHAPTER-CARDS.md"
CHAPTER_RE = re.compile(r"C(?P<id>\d{2})-[a-z0-9][a-z0-9-]*$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
NUMBERED_H2_RE = re.compile(r"^##\s+(?P<chapter>\d+)\.(?P<section>\d+)\s+", re.MULTILINE)
H1_RE = re.compile(r"^#\s+\S", re.MULTILINE)
FORMAL_H2_LINE_RE = re.compile(r"^##\s+(?P<chapter>\d+)\.(?P<section>\d+)\s+")
SUBHEADING_LINE_RE = re.compile(r"^#{3,4}\s+(?P<title>.+?)\s*$")
NUMBERED_SUBHEADING_PATH_RE = re.compile(
    r"^(?P<chapter>\d+)\.(?P<section>\d+)(?P<tail>(?:\.\d+)+)?(?:\s|$)"
)
PSEUDO_ORDINAL_SECTION_RE = re.compile(r"^\d+\s*[.、]\s+\d+\.\d+(?:\s|$)")
PSEUDO_RANGE_HEADING_RE = re.compile(r"^\d+\s*[—–-]\s*\d+(?:\s|$)")
D22_REAL_WORLD_FIELD_RE = re.compile(
    r"(?:`real_world`|[\"']real_world[\"']|"
    r"\b(?:dataset_layer|target_layer|intended_target_layer|layer)\s*[:=]\s*"
    r"[`\"']?real_world(?:[`\"']|\b))"
)
D22_HYPHENATED_FIELD_RE = re.compile(
    r"(?<![A-Za-z0-9_])representative-real(?:-world)?(?![A-Za-z0-9_])",
    re.IGNORECASE,
)
BARE_LEVEL_RE = re.compile(r"(?<![A-Z0-9-])L[0-9](?![A-Z0-9-])")
BARE_AU_CHAIN_RE = re.compile(r"\bAU-L[0-4]\s*(?:→|->|/|、|—|-)\s*L[0-4]\b")
D21_LEGACY_LABEL_RE = re.compile(r"\bD21\s*(?:三层|三证)\b")
PRODUCTION_LOG_PATTERNS = [
    (
        re.compile(r"当前状态[^\n]*(?:drafting|unapproved)", re.IGNORECASE),
        "reader body exposes a drafting/unapproved production status",
    ),
    (
        re.compile(r"(?:remediation-v\d+(?:\.\d+)?|作者整改|作者交接)", re.IGNORECASE),
        "reader body exposes an internal remediation/author handoff log",
    ),
    (
        re.compile(r"(?:review/runs/|fresh-temp)", re.IGNORECASE),
        "reader body exposes an internal review path or reproduction label",
    ),
]

REQUIRED_HEADING_GROUPS = [
    ("本章结论",),
    ("本章解决",),
    ("本章不解决",),
    ("开场案例",),
    ("硅基仿生镜头",),
    ("工程真相",),
    ("人类视图",),
    ("Agent 视图", "Agent 执行视图"),
    ("跨平台", "三个平台", "三平台"),
    ("失败模式",),
    ("实战练习",),
    ("验收",),
    ("产物与交接", "产物与章际交接"),
    ("证据",),
]

FORBIDDEN = [
    "我们一定行业最强",
    "训练后必然行业最强",
    "本书业界唯一",
    "已经完全自主",
    "Prompt 就是 Agent 的大脑",
    "SOUL.md，Agent 就不会越权",
]

OPENCLAW_BASELINE = {
    "version": "2026.9.6",
    "release_tag": "v2026.9.6",
    "commit": "eb377ac59e6c9fd6c7705028034812becf00271b",
}
HERMES_BASELINE = {
    "version": "0.20.1",
    "release_tag": "v2026.8.13",
    "commit": "f80f453ae0679347e38abc917c7f94f717bf96c5",
    "dynamic_docs_verified_on": "2026-09-30",
}
MUSE_BASELINE = {
    "evidence_status": "VENDOR-CLAIM",
    "public_materials_verified_on": "2026-09-30",
}

FIGURE_CAPTION_RE = re.compile(
    r"^\*\*图\s+(?P<number>\d+-\d+)　(?P<title>[^*]+?)（(?P<source>本书绘制|来源：[^）]+)）\*\*$",
    re.MULTILINE,
)


def manifest_integer(key: str) -> int:
    text = MANIFEST.read_text(encoding="utf-8")
    match = re.search(rf"^  {re.escape(key)}:\s*(\d+)\s*$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"BOOK-MANIFEST.yaml architecture.{key} is missing")
    return int(match.group(1))


def local_target(source: Path, raw: str) -> Path | None:
    target = raw.strip().split("#", 1)[0]
    if not target or "://" in target or target.startswith(("mailto:", "#")):
        return None
    return (source.parent / unquote(target)).resolve()


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"\'')
    return result


def nested_frontmatter_mapping(text: str, root_key: str) -> dict[str, str | dict[str, str]]:
    """Parse one two-level mapping from the restricted chapter frontmatter subset.

    The formal validator remains dependency-free; this helper intentionally
    accepts only the block-style mappings used for machine-readable baselines.
    Inline strings are returned as strings so callers can reject them.
    """
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    lines = text[4:end].splitlines()
    root_index = next((index for index, line in enumerate(lines) if line == f"{root_key}:"), None)
    if root_index is None:
        return {}
    result: dict[str, str | dict[str, str]] = {}
    current: str | None = None
    for line in lines[root_index + 1 :]:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            break
        if indent == 2 and ":" in line:
            key, raw = line.strip().split(":", 1)
            value = raw.strip().strip('"\'')
            if value:
                result[key] = value
                current = None
            else:
                result[key] = {}
                current = key
        elif indent == 4 and current and ":" in line:
            key, raw = line.strip().split(":", 1)
            value = raw.strip().strip('"\'')
            nested = result[current]
            if isinstance(nested, dict):
                nested[key] = value
    return result


def body_without_frontmatter(text: str) -> str:
    """Return reader body so strict checks do not flag editorial metadata."""
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    return text[end + 5 :]


def count_cjk_chars(text: str) -> int:
    return len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", text))


def yaml_check(path: Path) -> str | None:
    if not path.is_file():
        return f"missing YAML: {path.relative_to(ROOT)}"
    ruby = [
        "ruby",
        "-e",
        "require 'yaml'; require 'date'; YAML.safe_load(File.read(ARGV[0]), permitted_classes: [Date, Time], aliases: true)",
        str(path),
    ]
    try:
        completed = subprocess.run(ruby, capture_output=True, text=True, timeout=20)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip().splitlines()[-1]
        return f"invalid YAML {path.relative_to(ROOT)}: {detail}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    for path in (FRAMEWORK, FRONTMATTER, QUALITY, TERMS, CHAPTER_CARDS):
        if not path.is_file():
            errors.append(f"missing formal-edition file: {path.relative_to(ROOT)}")

    expected_volume_count = manifest_integer("volumes")
    expected_chapter_count = manifest_integer("chapters")
    expected_section_count = manifest_integer("body_third_level_sections")
    chapter_minimums: dict[int, int] = {}
    card_artifacts: dict[int, list[str]] = {}
    if CHAPTER_CARDS.is_file():
        cards_text = CHAPTER_CARDS.read_text(encoding="utf-8")
        for match in re.finditer(
            r"^## C(?P<id>\d{2})\b(?P<body>.*?)(?=^## C\d{2}\b|^## 25\.|\Z)",
            cards_text,
            re.MULTILINE | re.DOTALL,
        ):
            length_match = re.search(
                r'estimated_length:\s*"(?P<minimum>\d+)-(?P<maximum>\d+)\s*中文字符"',
                match.group("body"),
            )
            if length_match:
                chapter_minimums[int(match.group("id"))] = int(length_match.group("minimum"))
            artifacts_match = re.search(
                r"^required_artifacts:\s*\n(?P<items>(?:\s+-\s+.+\n?)+)",
                match.group("body"),
                re.MULTILINE,
            )
            if artifacts_match:
                artifacts = []
                for item in re.findall(r'^\s+-\s+"([^"]+)"\s*$', artifacts_match.group("items"), re.MULTILINE):
                    artifacts.append(item)
                card_artifacts[int(match.group("id"))] = artifacts

    framework_artifacts: dict[int, list[str]] = {}
    framework_sections: dict[int, list[tuple[int, int]]] = {}
    if FRAMEWORK.is_file():
        text = FRAMEWORK.read_text(encoding="utf-8")
        volume_count = len(re.findall(r"^## 卷[一二三四五六七八九] ", text, re.MULTILINE))
        chapter_ids = [int(x) for x in re.findall(r"^### 第 (\d+) 章 ", text, re.MULTILINE)]
        body_sections = [
            (int(a), int(b))
            for a, b in re.findall(r"^#### (\d+)\.(\d+) ", text, re.MULTILINE)
            if int(a) != 0
        ]
        notes.extend(
            [
                f"framework volumes: {volume_count}",
                f"framework chapters: {len(chapter_ids)}",
                f"framework body sections: {len(body_sections)}",
            ]
        )
        if volume_count != expected_volume_count:
            errors.append(f"framework volume count is {volume_count}, expected {expected_volume_count}")
        if chapter_ids != list(range(1, expected_chapter_count + 1)):
            errors.append(f"framework chapter ids invalid: {chapter_ids}")
        if len(body_sections) != len(set(body_sections)):
            errors.append("framework contains duplicate numbered body sections")
        if len(body_sections) != expected_section_count:
            errors.append(
                f"framework body section count is {len(body_sections)}, expected {expected_section_count}"
            )

        for match in re.finditer(
            r"^### 第 (?P<id>\d+) 章\b(?P<body>.*?)(?=^### 第 \d+ 章\b|^---$|\Z)",
            text,
            re.MULTILINE | re.DOTALL,
        ):
            chapter_id = int(match.group("id"))
            framework_sections[chapter_id] = [
                (int(chapter), int(section))
                for chapter, section in re.findall(
                    r"^#### (\d+)\.(\d+) ", match.group("body"), re.MULTILINE
                )
            ]
            artifact_line = re.search(r"^- \*\*主要产物\*\*：(?P<line>.+)$", match.group("body"), re.MULTILINE)
            if artifact_line:
                framework_artifacts[chapter_id] = re.findall(r"`([^`]+)`", artifact_line.group("line"))

    if framework_artifacts and card_artifacts:
        for chapter_id in range(1, expected_chapter_count + 1):
            framework_items = framework_artifacts.get(chapter_id, [])
            card_items = card_artifacts.get(chapter_id, [])
            if len(framework_items) != len(card_items):
                errors.append(
                    f"C{chapter_id:02d} artifact count mismatch: "
                    f"framework={len(framework_items)}, card={len(card_items)}"
                )
                continue
            for expected, actual in zip(framework_items, card_items):
                expected_id = expected.split(maxsplit=1)[0]
                actual_id = actual.split(maxsplit=1)[0]
                if expected_id != actual_id or not actual.startswith(expected):
                    errors.append(
                        f"C{chapter_id:02d} artifact contract mismatch: "
                        f"framework={expected!r}, card={actual!r}"
                    )

    if TERMS.is_file():
        issue = yaml_check(TERMS)
        if issue:
            errors.append(issue)
        terms_text = TERMS.read_text(encoding="utf-8", errors="replace")
        term_ids = re.findall(r'^\s+- term_id:\s+"([^"]+)"\s*$', terms_text, re.MULTILINE)
        duplicate_term_ids = sorted({term_id for term_id in term_ids if term_ids.count(term_id) > 1})
        if duplicate_term_ids:
            errors.append(f"duplicate controlled term ids: {', '.join(duplicate_term_ids)}")
        notes.append(f"controlled terms: {len(term_ids)}")

    chapter_dirs = sorted(
        path
        for path in MANUSCRIPT.glob("volume-*/C??-*")
        if path.is_dir() and CHAPTER_RE.fullmatch(path.name)
    )
    seen_ids: set[int] = set()
    chapter_stats: list[str] = []

    for chapter_dir in chapter_dirs:
        chapter_id = int(CHAPTER_RE.fullmatch(chapter_dir.name).group("id"))  # type: ignore[union-attr]
        if chapter_id in seen_ids:
            errors.append(f"duplicate chapter package C{chapter_id:02d}")
        seen_ids.add(chapter_id)

        chapter = chapter_dir / "chapter.md"
        ledger = chapter_dir / "evidence-ledger.yaml"
        if not chapter.is_file():
            message = f"chapter package is being prepared: {chapter_dir.relative_to(ROOT)}"
            if args.strict:
                errors.append(message)
            else:
                warnings.append(message)
            continue
        text = chapter.read_text(encoding="utf-8", errors="replace")
        meta = frontmatter(text)
        expected = f"C{chapter_id:02d}"
        if meta.get("chapter_id") != expected:
            errors.append(f"{chapter.relative_to(ROOT)} chapter_id is not {expected}")
        for key in (
            "volume_id",
            "title",
            "status",
            "content_role",
            "principle_owner",
            "depends_on",
            "feeds_into",
            "fact_baseline",
            "verified_on",
        ):
            if key not in meta:
                errors.append(f"{chapter.relative_to(ROOT)} missing frontmatter key {key}")
        if "editor_reviewer" in meta:
            errors.append(
                f"{chapter.relative_to(ROOT)} declares editor_reviewer as chapter metadata; "
                "the canonical five gates are writing/fact/practice/cross/chief"
            )
        # Every formal chapter, including the three closing chapters, must
        # expose the same machine-readable platform baseline and publication
        # boundary.  Keeping a temporary chapter-id exception here allowed a
        # structurally valid source tree to hide stale approval metadata.
        if chapter_id <= expected_chapter_count:
            baseline = nested_frontmatter_mapping(text, "fact_baseline")
            for platform, expected_fields in (
                ("openclaw", OPENCLAW_BASELINE),
                ("hermes", HERMES_BASELINE),
                ("muse", MUSE_BASELINE),
            ):
                actual = baseline.get(platform)
                if not isinstance(actual, dict):
                    errors.append(
                        f"{chapter.relative_to(ROOT)} fact_baseline.{platform} must be a nested mapping"
                    )
                    continue
                for field, expected_value in expected_fields.items():
                    if actual.get(field) != expected_value:
                        errors.append(
                            f"{chapter.relative_to(ROOT)} fact_baseline.{platform}.{field} "
                            f"must be {expected_value!r}"
                        )
            for deprecated in ("approval", "self_approval"):
                if deprecated in meta:
                    errors.append(
                        f"{chapter.relative_to(ROOT)} uses deprecated frontmatter key {deprecated}; "
                        "use approval_status/self_approval_allowed"
                    )
            for required_state in ("approval_status", "real_world_practice", "self_approval_allowed"):
                if required_state not in meta:
                    errors.append(
                        f"{chapter.relative_to(ROOT)} missing frontmatter key {required_state}"
                    )
            if meta.get("real_world_practice") != "REVIEW_REQUIRED":
                errors.append(
                    f"{chapter.relative_to(ROOT)} real_world_practice must be REVIEW_REQUIRED"
                )
            if meta.get("self_approval_allowed") != "false":
                errors.append(
                    f"{chapter.relative_to(ROOT)} self_approval_allowed must be false"
                )
            if chapter_id >= 7 and meta.get("approval_status") != "content_candidate_only":
                errors.append(
                    f"{chapter.relative_to(ROOT)} C07-C{expected_chapter_count:02d} approval_status must be content_candidate_only"
                )

        reader_body = body_without_frontmatter(text)
        prose = CODE_FENCE_RE.sub("", reader_body)
        h1_count = len(H1_RE.findall(prose))
        if h1_count != 1:
            errors.append(
                f"{chapter.relative_to(ROOT)} must contain exactly one H1 outside code fences, got {h1_count}"
            )

        actual_sections = [
            (int(match.group("chapter")), int(match.group("section")))
            for match in NUMBERED_H2_RE.finditer(prose)
        ]
        expected_sections = framework_sections.get(chapter_id, [])
        if actual_sections != expected_sections:
            errors.append(
                f"{chapter.relative_to(ROOT)} numbered H2 mismatch: "
                f"actual={actual_sections}, expected={expected_sections}"
            )

        first_formal = next(NUMBERED_H2_RE.finditer(prose), None)
        if first_formal is None:
            errors.append(f"{chapter.relative_to(ROOT)} has no formal numbered H2")
        else:
            pre_section_cjk = count_cjk_chars(prose[: first_formal.start()])
            if pre_section_cjk > 4000:
                message = (
                    f"{chapter.relative_to(ROOT)} has oversized pre-section material: "
                    f"{pre_section_cjk} CJK chars before first formal H2"
                )
                if args.strict:
                    errors.append(message)
                else:
                    warnings.append(message)

        current_formal_section: tuple[int, int] | None = None
        inside_fence = False
        for line_number, line in enumerate(reader_body.splitlines(), 1):
            if line.lstrip().startswith("```"):
                inside_fence = not inside_fence
                continue
            if inside_fence:
                continue
            formal_match = FORMAL_H2_LINE_RE.match(line)
            if formal_match:
                current_formal_section = (
                    int(formal_match.group("chapter")),
                    int(formal_match.group("section")),
                )
                continue
            subheading_match = SUBHEADING_LINE_RE.match(line)
            if not subheading_match:
                continue
            title = subheading_match.group("title")
            reason: str | None = None
            if PSEUDO_RANGE_HEADING_RE.match(title):
                reason = "range-like pseudo numbering"
            elif PSEUDO_ORDINAL_SECTION_RE.match(title):
                reason = "stacked ordinal/formal-section pseudo numbering"
            else:
                path_match = NUMBERED_SUBHEADING_PATH_RE.match(title)
                if path_match:
                    heading_section = (
                        int(path_match.group("chapter")),
                        int(path_match.group("section")),
                    )
                    has_subsection_tail = bool(path_match.group("tail"))
                    if current_formal_section is None or heading_section != current_formal_section:
                        reason = "numbered subheading does not belong to the active formal H2"
                    elif not has_subsection_tail:
                        reason = "H3/H4 duplicates an H2-shaped section number"
            if reason:
                message = (
                    f"{chapter.relative_to(ROOT)}:{line_number} {reason}: {title!r}; "
                    "use the matching chapter.section.subsection path or an unnumbered reader heading"
                )
                if args.strict:
                    errors.append(message)
                else:
                    warnings.append(message)

        for line_number, line in enumerate(reader_body.splitlines(), 1):
            if D22_REAL_WORLD_FIELD_RE.search(line):
                message = (
                    f"{chapter.relative_to(ROOT)}:{line_number} uses real_world as a D22 machine field; "
                    "use representative_real_world (ordinary prose such as 真实世界/real-world is allowed)"
                )
                if args.strict:
                    errors.append(message)
                else:
                    warnings.append(message)
            if D22_HYPHENATED_FIELD_RE.search(line):
                message = (
                    f"{chapter.relative_to(ROOT)}:{line_number} uses a hyphenated D22 machine field; "
                    "use representative_real_world"
                )
                if args.strict:
                    errors.append(message)
                else:
                    warnings.append(message)

        for line_number, line in enumerate(prose.splitlines(), 1):
            if not BARE_LEVEL_RE.search(line):
                continue
            if re.search(r"\b(?:AU|MAT|LOAD|SEC)-L[0-9]", line):
                continue
            if any(marker in line for marker in ("历史", "非等级", "错误示例", "旧稿原名", "旧命名")):
                continue
            message = (
                f"{chapter.relative_to(ROOT)}:{line_number} contains bare Lx level; "
                "use AU-, MAT-, LOAD-, SEC- or an explicit historical/non-level label"
            )
            if args.strict:
                errors.append(message)
            else:
                warnings.append(message)
        for line_number, line in enumerate(prose.splitlines(), 1):
            if D21_LEGACY_LABEL_RE.search(line):
                message = (
                    f"{chapter.relative_to(ROOT)}:{line_number} uses legacy D21三层/三证 wording; "
                    "use D21完成三面"
                )
                if args.strict:
                    errors.append(message)
                else:
                    warnings.append(message)
            if BARE_AU_CHAIN_RE.search(line):
                message = (
                    f"{chapter.relative_to(ROOT)}:{line_number} contains a bare AU chain target; "
                    "prefix every level with AU-"
                )
                if args.strict:
                    errors.append(message)
                else:
                    warnings.append(message)
        for pattern, detail in PRODUCTION_LOG_PATTERNS:
            for match in pattern.finditer(prose):
                line_number = prose.count("\n", 0, match.start()) + 1
                message = f"{chapter.relative_to(ROOT)}:{line_number} {detail}"
                if args.strict:
                    errors.append(message)
                else:
                    warnings.append(message)
        for alternatives in REQUIRED_HEADING_GROUPS:
            if not any(heading in text for heading in alternatives):
                expected = " or ".join(repr(item) for item in alternatives)
                errors.append(f"{chapter.relative_to(ROOT)} missing required section containing {expected}")
        for phrase in FORBIDDEN:
            if phrase in text:
                errors.append(f"{chapter.relative_to(ROOT)} contains forbidden claim {phrase!r}")

        cjk = count_cjk_chars(prose)
        status = meta.get("status", "")
        if cjk < 6000:
            errors.append(f"{chapter.relative_to(ROOT)} is too thin: {cjk} CJK chars")

        chapter_minimum = chapter_minimums.get(chapter_id)
        if chapter_minimum and cjk < chapter_minimum:
            message = (
                f"{chapter.relative_to(ROOT)} below C{chapter_id:02d} card minimum: "
                f"{cjk} < {chapter_minimum} CJK chars"
            )
            if args.strict or status in {"release_candidate", "done"}:
                errors.append(message)
            else:
                warnings.append(message)

        issue = yaml_check(ledger)
        if issue:
            errors.append(issue)

        artifact_files = list((chapter_dir / "artifacts").glob("*")) if (chapter_dir / "artifacts").is_dir() else []
        exercise_files = list((chapter_dir / "exercises").glob("*")) if (chapter_dir / "exercises").is_dir() else []
        if not artifact_files:
            errors.append(f"{chapter_dir.relative_to(ROOT)} has no artifact file")
        if len(exercise_files) < 2:
            errors.append(f"{chapter_dir.relative_to(ROOT)} needs at least two exercise files")

        for raw in LINK_RE.findall(CODE_FENCE_RE.sub("", text)):
            target = local_target(chapter, raw)
            if target is not None and not target.exists():
                errors.append(f"broken link: {chapter.relative_to(ROOT)} -> {raw}")
        chapter_stats.append(f"C{chapter_id:02d}={cjk}")

    missing = sorted(set(range(1, expected_chapter_count + 1)) - seen_ids)
    if args.strict and missing:
        errors.append(f"missing chapter packages: {', '.join(f'C{x:02d}' for x in missing)}")
    elif missing:
        warnings.append(f"production incomplete; missing {len(missing)} chapter packages")

    notes.append(f"chapter packages present: {len(chapter_dirs)}")
    if chapter_stats:
        notes.append("chapter CJK chars: " + ", ".join(chapter_stats))

    opening_slice_count = 0
    for chapter in MANUSCRIPT.glob("volume-*/C??-*/chapter.md"):
        opening_slice_count += chapter.read_text(encoding="utf-8", errors="replace").count(
            "<!-- OPENING-SLICE-2026-10 -->"
        )
    if opening_slice_count != 23:
        errors.append(f"concrete opening slices must be 23, got {opening_slice_count}")
    notes.append(f"concrete opening slices: {opening_slice_count}")

    manager_brief = ROOT / "deliverables" / "管理者执行摘要分册.md"
    if not manager_brief.is_file():
        errors.append("missing manager executive summary booklet")
    else:
        manager_cjk = count_cjk_chars(manager_brief.read_text(encoding="utf-8", errors="replace"))
        if not 8000 <= manager_cjk <= 12000:
            errors.append(f"manager executive summary must be 8000-12000 CJK chars, got {manager_cjk}")
        notes.append(f"manager executive summary CJK chars: {manager_cjk}")

    publication_sources = list(MANUSCRIPT.glob("volume-*/C??-*/chapter.md"))
    publication_sources.extend(MANUSCRIPT.glob("volume-*/C??-*/artifacts/*.md"))
    publication_sources.extend(MANUSCRIPT.glob("volume-*/C??-*/exercises/*.md"))
    publication_sources.extend((MANUSCRIPT / "appendices").glob("[A-I]-*.md"))
    for source in sorted(publication_sources):
        source_text = CODE_FENCE_RE.sub("", source.read_text(encoding="utf-8", errors="replace"))
        for line_number, line in enumerate(source_text.splitlines(), 1):
            if re.search(r"\bdecision\s*:\s*LIMITED\b", line, re.IGNORECASE):
                errors.append(
                    f"{source.relative_to(ROOT)}:{line_number} uses LIMITED as a gate decision; "
                    "use lifecycle_state plus limitations/exclusions"
                )
            if re.search(r"\bdecision\s*:\s*[^\n]*(?:PASS\s*\|\s*LIMITED|LIMITED\s*\|)", line, re.IGNORECASE):
                errors.append(
                    f"{source.relative_to(ROOT)}:{line_number} declares a fourth gate state LIMITED"
                )

    # BOOK-QUALITY-STANDARD §4.5: every formal figure has an identity,
    # source marker, actual visual body, and prose explanation.  The gate is
    # deliberately structural; editorial reviewers still judge visual quality.
    figure_sources = [FRONTMATTER, ROOT / "part-I-getting-started" / "00-formal-volume-zero.md"]
    figure_sources.extend(MANUSCRIPT.glob("volume-*/C??-*/chapter.md"))
    figure_sources.extend((MANUSCRIPT / "appendices").glob("[A-I]-*.md"))
    figure_numbers: dict[str, Path] = {}
    figures_by_chapter: dict[int, list[str]] = {}
    figure_total = 0
    for source in sorted(figure_sources):
        if not source.is_file():
            continue
        source_text = source.read_text(encoding="utf-8", errors="replace")
        lines = source_text.splitlines()
        chapter_match = re.search(r"C(?P<id>\d{2})-", source.as_posix())
        chapter_id = int(chapter_match.group("id")) if chapter_match else None
        for index, line in enumerate(lines):
            match = FIGURE_CAPTION_RE.fullmatch(line)
            if not match:
                continue
            figure_total += 1
            number = match.group("number")
            title = match.group("title").strip()
            if not title:
                errors.append(f"{source.relative_to(ROOT)}:{index + 1} figure title is empty")
            if number in figure_numbers:
                errors.append(
                    f"duplicate figure number {number}: {figure_numbers[number].relative_to(ROOT)} and {source.relative_to(ROOT)}"
                )
            figure_numbers[number] = source
            if chapter_id is not None:
                figures_by_chapter.setdefault(chapter_id, []).append(title)
                if not number.startswith(f"{chapter_id}-"):
                    errors.append(
                        f"{source.relative_to(ROOT)}:{index + 1} figure {number} does not match C{chapter_id:02d}"
                    )
            nearby = lines[index + 1 : index + 16]
            has_visual = any(
                item.startswith("```mermaid") or item.startswith("![") or item.lstrip().startswith("<svg")
                for item in nearby
            )
            if not has_visual:
                errors.append(
                    f"{source.relative_to(ROOT)}:{index + 1} figure {number} has no Mermaid/image body within 15 lines"
                )
            explanation_window = "\n".join(lines[index + 1 : index + 36])
            if f"图 {number}" not in explanation_window:
                errors.append(
                    f"{source.relative_to(ROOT)}:{index + 1} figure {number} has no nearby prose explanation naming the figure"
                )
    if not 40 <= figure_total <= 60:
        errors.append(f"formal figure count must be 40-60 under §4.5, got {figure_total}")
    priority_figures = {
        6: ("六层",),
        13: ("记忆", "生命周期"),
        17: ("授权", "状态机"),
        20: ("Handoff", "时序"),
        22: ("SEC", "攻击面"),
        23: ("最小事件链",),
        25: ("甘特", "30天"),
    }
    for chapter_id, keyword_groups in priority_figures.items():
        titles = " ".join(figures_by_chapter.get(chapter_id, []))
        if not all(keyword in titles for keyword in keyword_groups):
            errors.append(
                f"C{chapter_id:02d} missing priority figure title keywords: {keyword_groups}; got {titles!r}"
            )
    notes.append(f"formal figures satisfying caption pattern: {figure_total}")

    complete = MANUSCRIPT / "99-complete-manuscript.md"
    if complete.is_file():
        assembled = complete.read_text(encoding="utf-8", errors="replace")
        if "<!-- BEGIN part-I-getting-started/00-formal-volume-zero.md -->" not in assembled:
            errors.append("assembled manuscript is missing formal Volume Zero")
        exercise_markers = len(re.findall(r"<!-- BEGIN manuscript/volume-\d{2}/C\d{2}-[^/]+/exercises/[^>]+\.md -->", assembled))
        artifact_markers = len(re.findall(r"<!-- BEGIN manuscript/volume-\d{2}/C\d{2}-[^/]+/artifacts/[^>]+\.md -->", assembled))
        expected_exercises = manifest_integer("exercises")
        expected_core_artifacts = manifest_integer("core_artifact_templates_in_book")
        if exercise_markers != expected_exercises:
            errors.append(f"assembled exercises {exercise_markers}, expected {expected_exercises}")
        if artifact_markers != expected_core_artifacts:
            errors.append(f"assembled core artifacts {artifact_markers}, expected {expected_core_artifacts}")
        notes.append(f"embedded exercises/core artifacts: {exercise_markers}/{artifact_markers}")

    for note in notes:
        print(f"OK {note}")
    for warning in warnings:
        print(f"WARN {warning}")
    for error in errors:
        print(f"ERROR {error}")

    if errors:
        print(f"FAIL {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

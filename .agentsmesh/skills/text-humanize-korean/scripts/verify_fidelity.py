#!/usr/bin/env python3
"""Lightweight deterministic fidelity checks for mols-humanize-korean.

These checks are directional guards, not a semantic equivalence proof.
`run_checks(original, rewritten)` returns a list of finding dicts.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Iterable

URL_RE = re.compile(r"https?://[^\s)>]+")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
NUM_RE = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)*(?:%|[A-Za-z가-힣]+)?")
VERSION_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    r"v\d+(?:\.\d+){1,3}"          # v2.3 / v2.3.0
    r"|\d+\.\d+\.\d+(?:\.\d+)?"  # 2.3.0 / 2.3.0.1
    r")(?:[-+][0-9A-Za-z.-]+)?(?![A-Za-z0-9_])",
    re.IGNORECASE,
)
IDENTIFIER_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    r"[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+"          # snake_case
    r"|[a-z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*"         # camelCase
    r"|[A-Z][A-Z0-9]{1,}(?:_[A-Z0-9]+)*"           # API / ALL_CAPS
    r")(?![A-Za-z0-9_])"
)
HEADING_RE = re.compile(r"(?m)^(#{1,6})\s+(.+)$")
FOOTNOTE_INLINE_RE = re.compile(r"(?<=\S)(\d{1,3})\)")
FOOTNOTE_DEF_RE = re.compile(r"(?m)^\s*(\d{1,3})\)\s+(.+)$")
YO_END_RE = re.compile(r"요\s*(?:[.?!…]|$)", re.MULTILINE)
HAYEOT_RE = re.compile(r"하였")
DOUBLE_QUOTE_PATTERNS = [
    re.compile(r'"[^"\n]*"'),
    re.compile(r"“[^”\n]*”"),
]

CLICHES = [
    re.compile(r"기록적인\s*성과"),
    re.compile(r"괄목할\s*만한"),
    re.compile(r"로\s*평가(?:된다|되었다|받)"),
    re.compile(r"주목받"),
    re.compile(r"시사하는\s*바가\s*크"),
    re.compile(r"의미가\s*크다"),
]


def _multiset(pat: re.Pattern[str], text: str, group: int = 0) -> list[str]:
    vals = []
    for m in pat.finditer(text):
        vals.append(m.group(group))
    return vals


def _missing(before: Iterable[str], after: Iterable[str]) -> list[str]:
    pool = list(after)
    missing = []
    for item in before:
        try:
            pool.remove(item)
        except ValueError:
            missing.append(item)
    return missing


def _strip_fenced_code(text: str) -> str:
    return FENCE_RE.sub("", text)


def _markdown_table_signatures(text: str) -> list[tuple[int, tuple[int, ...]]]:
    """Return structural signatures for Markdown tables.

    Signature = (row_count, column_count_per_row). Cell text is intentionally
    ignored so normal local polishing inside cells does not fail the gate.
    """
    text = _strip_fenced_code(text)
    lines = text.splitlines()
    signatures: list[tuple[int, tuple[int, ...]]] = []
    i = 0

    def is_tableish(line: str) -> bool:
        return "|" in line and bool(line.strip())

    def is_separator(line: str) -> bool:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        return len(cells) >= 2 and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)

    def col_count(line: str) -> int:
        return len(line.strip().strip("|").split("|"))

    while i < len(lines):
        if i + 1 < len(lines) and is_tableish(lines[i]) and is_separator(lines[i + 1]):
            block = [lines[i], lines[i + 1]]
            i += 2
            while i < len(lines) and is_tableish(lines[i]) and lines[i].strip():
                block.append(lines[i])
                i += 1
            signatures.append((len(block), tuple(col_count(line) for line in block)))
            continue
        i += 1
    return signatures


def _sentence_anchor_index(text: str, marker_pos: int) -> int:
    """Approximate sentence ordinal of an inline footnote marker.

    Used only when before/after have the same sentence-terminal count, which
    keeps this directional check conservative.
    """
    prefix = text[:marker_pos]
    return len(re.findall(r"[.!?…](?=(?:\s|$|\d{1,3}\)))", prefix))


def _footnote_anchor_map(text: str) -> dict[str, list[int]]:
    anchors: dict[str, list[int]] = {}
    for line_start, line in _iter_lines_with_offsets(text):
        if FOOTNOTE_DEF_RE.match(line):
            continue
        for match in FOOTNOTE_INLINE_RE.finditer(line):
            num = match.group(1)
            pos = line_start + match.start(1)
            anchors.setdefault(num, []).append(_sentence_anchor_index(text, pos))
    return anchors


def _iter_lines_with_offsets(text: str):
    offset = 0
    for line in text.splitlines(keepends=True):
        yield offset, line
        offset += len(line)


def _sentence_terminal_count(text: str) -> int:
    return len(re.findall(r"[.!?…](?=(?:\s|$|\d{1,3}\)))", text))



def change_rate(original: str, rewritten: str) -> float:
    """Advisory character-level change rate."""
    return 1.0 - SequenceMatcher(None, original, rewritten).ratio()


def run_checks(original: str, rewritten: str) -> list[dict]:
    findings: list[dict] = []

    if not rewritten.strip():
        return [{"code": "empty_output", "detail": "윤문본이 비어 있습니다."}]

    # Advisory only: broad edits deserve closer semantic review.
    rate = change_rate(original, rewritten)
    if rate >= 0.50:
        findings.append({
            "code": "change_scope_high",
            "detail": f"문자 기준 변경 범위가 큽니다({rate:.0%}). 의미 보존을 직접 재검토하세요."
        })
    elif rate >= 0.30:
        findings.append({
            "code": "change_scope_warn",
            "detail": f"문자 기준 변경 범위가 넓습니다({rate:.0%}). 과윤문 여부를 확인하세요."
        })

    # Protected exact tokens.
    for code, pat, group in [
        ("url_lost", URL_RE, 0),
        ("link_destination_lost", MD_LINK_RE, 1),
        ("inline_code_lost", INLINE_CODE_RE, 1),
        ("version_lost", VERSION_RE, 0),
        ("identifier_lost", IDENTIFIER_RE, 0),
        ("number_lost", NUM_RE, 0),
    ]:
        miss = _missing(_multiset(pat, original, group), _multiset(pat, rewritten, group))
        if miss:
            findings.append({"code": code, "detail": f"원문 항목 소실/변경: {miss[:8]}"})

    # Numeric injection is also suspicious.
    injected = _missing(_multiset(NUM_RE, rewritten), _multiset(NUM_RE, original))
    if injected:
        findings.append({"code": "number_injected", "detail": f"원문에 없던 수치: {injected[:8]}"})

    # Fenced code blocks: exact preservation.
    miss_fences = _missing(_multiset(FENCE_RE, original), _multiset(FENCE_RE, rewritten))
    if miss_fences:
        findings.append({"code": "fenced_code_altered", "detail": "fenced code block이 변경/소실됐습니다."})

    # Direct quotes: exact preservation.
    for pat in DOUBLE_QUOTE_PATTERNS:
        miss_quotes = _missing(_multiset(pat, original), _multiset(pat, rewritten))
        if miss_quotes:
            findings.append({"code": "quote_altered", "detail": f"직접 인용 변경/소실: {miss_quotes[:4]}"})
            break

    # Headings: preserve count, level, and line independence.
    in_heads = [(m.group(1), m.group(2).strip()) for m in HEADING_RE.finditer(original)]
    out_heads = [(m.group(1), m.group(2).strip()) for m in HEADING_RE.finditer(rewritten)]
    if len(out_heads) != len(in_heads):
        findings.append({
            "code": "heading_structure_changed",
            "detail": f"heading 수가 {len(in_heads)} → {len(out_heads)}로 바뀌었습니다."
        })
    else:
        in_levels = [x[0] for x in in_heads]
        out_levels = [x[0] for x in out_heads]
        if in_levels != out_levels:
            findings.append({"code": "heading_level_changed", "detail": "heading level 순서가 바뀌었습니다."})

    # Markdown tables: preserve table count and row/column structure.
    in_tables = _markdown_table_signatures(original)
    out_tables = _markdown_table_signatures(rewritten)
    if in_tables != out_tables:
        findings.append({
            "code": "table_structure_changed",
            "detail": f"Markdown table 구조가 {in_tables} → {out_tables}로 바뀌었습니다."
        })

    # Footnotes.
    in_markers = _multiset(FOOTNOTE_INLINE_RE, original, 1)
    out_markers = _multiset(FOOTNOTE_INLINE_RE, rewritten, 1)
    if in_markers != out_markers:
        findings.append({
            "code": "footnote_markers_changed",
            "detail": f"각주 marker가 {in_markers} → {out_markers}로 바뀌었습니다."
        })
    in_defs = {(m.group(1), m.group(2).strip()) for m in FOOTNOTE_DEF_RE.finditer(original)}
    out_defs = {(m.group(1), m.group(2).strip()) for m in FOOTNOTE_DEF_RE.finditer(rewritten)}
    if in_defs != out_defs:
        findings.append({"code": "footnote_defs_changed", "detail": "각주 정의/서지 내용이 변경됐습니다."})

    # Footnote anchor: only compare sentence ordinal when sentence structure
    # is stable enough for a low-false-positive deterministic check.
    if (
        in_markers == out_markers
        and _sentence_terminal_count(original) == _sentence_terminal_count(rewritten)
    ):
        in_anchors = _footnote_anchor_map(original)
        out_anchors = _footnote_anchor_map(rewritten)
        if in_anchors != out_anchors:
            findings.append({
                "code": "footnote_anchor_changed",
                "detail": f"각주가 근거하던 문장 위치가 바뀌었습니다: {in_anchors} → {out_anchors}"
            })

    # Register direction.
    if len(HAYEOT_RE.findall(rewritten)) > len(HAYEOT_RE.findall(original)):
        findings.append({"code": "formality_injected", "detail": "'하였-' 계열이 원문보다 늘었습니다."})
    in_yo = len(YO_END_RE.findall(original))
    out_yo = len(YO_END_RE.findall(rewritten))
    if in_yo >= 3 and out_yo < in_yo * 0.5:
        findings.append({
            "code": "colloquial_erased",
            "detail": f"~요 종결이 {in_yo} → {out_yo}로 크게 줄었습니다."
        })

    # Cliche injection.
    for pat in CLICHES:
        if len(pat.findall(rewritten)) > len(pat.findall(original)):
            findings.append({"code": "cliche_injected", "detail": f"상투구가 새로 늘었습니다: {pat.pattern}"})

    return findings


if __name__ == "__main__":
    demo_before = "## 결과\n오류율은 3.1%였다.1)\n\n1) 실험 로그 기준."
    demo_after = demo_before
    print(run_checks(demo_before, demo_after))
    print({"change_rate": change_rate(demo_before, demo_after)})

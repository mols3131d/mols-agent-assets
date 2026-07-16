from typing import Final

ADR_INDEX_TEMPLATE: Final[str] = """# ADR Index

| ID | Date | Status | Title | Message |
| :--- | :--- | :--- | :--- |:--- |
| [001](adr-001-example.md) | YYYY-MM-DD | `proposed` | [Title] | [Message] |

> **Archive**: `archive/INDEX.md`
"""

ADR_README_TEMPLATE: Final[str] = """# Architecture Decision Records (ADR)

아키텍처 및 기술 스택 의사결정 기록 저장소.

## Structure

- `INDEX.md`: 활성 문서 인덱스
- `archive/INDEX.md`: 비활성 문서 인덱스
"""

ADR_ARCHIVE_INDEX_TEMPLATE: Final[str] = """# ADR Archive Index

| ID | Date | Prev. Status | Title | Message |
| :--- | :--- | :--- | :--- | :--- |
| [000](adr-000-example.md) | YYYY-MM-DD | `accepted` | [Title] | [Message] |

> **Active**: `../INDEX.md`
"""

ADR_DOCUMENT_TEMPLATE: Final[str] = """---
id: "{doc_id}"
title: "{title}"
status: "{status}"
description: "{description}"
categories: {categories}
tags: {tags}
related-files: {related_files}
---

# ADR-{doc_id}: {title}

## Context (배경)

이 결정이 논의되게 된 배경과 해결하고자 하는 문제 상황을 설명합니다.

- **관련 요구사항**: `[관련 기능 명세나 스택 변경 사항]`
- **제약 사항**: `[당시 고려해야 했던 물리적/기술적 한계]`

## Decision (결정)

최종적으로 도출된 결론과 구현 방안을 기술합니다.

- **선택된 방안**: `[구체적인 선택 기술이나 정책]`
- **결정 근거**: `[비용, 성능, 유지보수 용이성 등 선택의 핵심 사유]`

## Consequences (결과)

이 결정으로 인해 발생하는 변화와 영향도를 기술합니다.

- **긍정적 영향**: `[가져올 이점]`
- **부정적 영향 및 리스크**: `[감수해야 할 트레이드오프나 잠재적 위험]`
- **후속 작업**: `[이 결정 후 업데이트해야 할 문서나 코드]`

---

- **Decided by**: `[참여자 목록]`
"""

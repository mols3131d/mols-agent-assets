---
title: 마크다운 표준
description: MOLS Agent 워크스페이스의 마크다운 작성 기술 명세
categories:
  - standards
draft: false
date: 2026-02-26
lastmod: 2026-02-26T22:25:53.800Z
tags:
  - markdown
  - standards
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# 📝 마크다운 표준 (Markdown Standards)

이 문서는 프로젝트 내의 모든 마크다운 문서가 준수해야 하는 기술적 명세와 링크 프로토콜을 정의합니다.

## 📜 표준 상세 내용

### 1. 프론트매너 (Frontmatter)
모든 문서는 거버넌스와 메타데이터 관리를 위해 Hugo 호환 YAML 형식을 포함해야 합니다.

- **기본 필드**: `title`, `description`, `categories`, `date`, `lastmod`, `tags`.
- **에이전트 제어 필드**: 에이전트의 문서 접근 및 편집 권한을 결정하는 핵심 필드입니다.

### 2. 에이전트 제어 상세 (Agent Control)
- **`agent-readable`**: 에이전트의 문서 가독성 여부.
- **`agent-editable`**: 에이전트의 내용 수정 권한.
- **`agent-moveable`**: 파일 위치 변경 권한.
- **`agent-deletable`**: 파일 삭제 권한 (AOS에 따른 Soft Delete 적용).
- **`agent-friendly`**: 에이전트 인지에 최적화된 고밀도 구조 여부.

### 3. 링크 프로토콜 (Linking Protocol)
- **루트 상대 경로**: 모든 링크는 워크스페이스 루트를 기준으로 하며, 반드시 `/`로 시작해야 합니다.
- **형식**: `[이름](/path/to/asset.md)`

## ⚠️ 제약 사항
- **이중화 의무**: 모든 문서는 DPS(`/docs/standards/document.md`)에 따라 대응되는 영어/한국어 파일을 가져야 합니다.
- **무결성**: 잘못된 경로의 링크는 에이전트의 길찾기(Navigating) 오류를 유발하므로 즉시 수정되어야 합니다.

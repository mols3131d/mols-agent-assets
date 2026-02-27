---
title: ADR 운영 가이드
description: 아키텍처 결정 기록(ADR) 관리 및 명명 규칙
categories:
  - ADR
  - guidance
draft: false
date: 2026-02-28
lastmod: 2026-02-27T17:01:24.097Z
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# ADR 운영 가이드

이 디렉토리는 확정된 아키텍처 결정 사항을 불변의 기록으로 관리합니다.

## 1. 디렉토리 구조

- **연도별 분류**: `docs/adr/[YYYY]/`

## 2. 파일 명명 규칙

파일 이름 형식: `[ADR번호]--[Keyword].md`

- 예: `001--adopt-ace-workflow.md`
- 상세 날짜는 프론트매터(`date`)에 기록되므로 파일명에서는 제외하고, 순차적인 번호를 사용하여 시간순 정렬 및 식별을 용이하게 합니다.

## 3. 프론트매터 표준 (Metadata Safety)

Hugo나 Astro 등 정적 사이트 생성기와의 충돌을 피하기 위해 다음의 접두사가 붙은 키를 사용합니다.

- **id**: ADR 고유 식별자 (예: `adr-001`)
- **adr-status**: 결정 상태 (accepted, superseded 등)
- **adr-keyword**: 핵심 키워드
- **date**: 결정 날짜 (YYYY-MM-DD)

## 4. 운영 원칙

- ADR은 RFC 토론(인덱스 9번)의 최종 결론을 바탕으로 작성됩니다.
- 한 번 작성된 ADR은 수정하지 않으며, 결정이 변경될 경우 새로운 ADR을 작성하고 기존 문서를 대체(Superseded) 처리합니다.

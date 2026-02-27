---
title: RFC 운영 가이드
description: RFC 디렉토리 구조 및 파일 명명 규칙 가이드
categories:
  - guidance
draft: false
date: 2026-02-28
lastmod: 2026-02-27T16:51:56.283Z
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# RFC 운영 가이드

이 디렉토리는 제안 및 토론의 수명 주기를 관리합니다. 모든 공식 제안서(Index 0) 및 최종안(Index 9)에는 고유 식별자인 `id` 필드를 포함해야 합니다.

## 1. 프론트매터 표준

관리형 문서의 구분을 위해 다음 키를 사용합니다.

- **id**: RFC 고유 식별자 (예: `rfc-001`)

## 2. 디렉토리 구조 및 명명 규칙

- **연도별 분류**: `docs/rfc/[YYYY]/`
- **제안별 폴더**: `[Num]--[Keyword]/`
  - 예: `001--ACE-WF/`
  - 기존의 `MM-DD` 날짜 형식 대신 순차적인 **3자리 번호**를 사용하여 시간순 정렬과 짧은 참조를 가능하게 합니다.
- **파일 인덱싱**: 제안 폴더 내의 파일들은 진행 단계에 따라 번호가 매겨집니다.
  - `0--proposal.md`: 최초 제안
  - `1-8--[Content].md`: 논의 및 피드백 (TAS, 비판 등)
  - `9--final.md`: 최종 결론
    _상위 폴더의 키워드를 반복하지 않고, 해당 단계의 구체적인 주제를 키워드로 사용합니다._

### 인덱스 정의

- **0번 (0--)**: **최초 제안**. (예: `0--proposal.md`)
- **1~8번 (1-- ~ 8--)**: **토론 및 합**. (예: `1--critique.ko.md`, `2--synthesis.md`)
- **9번 (9--)**: **최종안**. (예: `9--final.ko.md`)

## 3. 운영 원칙

- 별도의 `discussion` 폴더를 사용하지 않고, 모든 토론은 해당 제안 폴더 내에서 인덱스 번호를 따라 기록합니다.
- 최종안(9번)이 도출되면 결정 사항을 요약하여 [`/docs/adr/`](/docs/adr/) 에 기록합니다.

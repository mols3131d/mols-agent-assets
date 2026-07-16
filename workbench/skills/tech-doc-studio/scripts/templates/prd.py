from typing import Final

# ruff: noqa: E501

PRD_INDEX_TEMPLATE: Final[str] = """# PRD Index

| ID | Date | Status | Title | Priority |
| :--- | :--- | :--- | :--- | :--- |
| [001](prd-001.md) | YYYY-MM-DD | `draft` | [Title] | [Must-Have] |

> **Archive Index**: `archive/INDEX.md`
"""

PRD_README_TEMPLATE: Final[str] = """# Product Requirement Documents (PRD)

사용자 시나리오, 기능적 요구사항 및 제품 목표 저장소.

## Structure

- `INDEX.md`: 활성 문서 인덱스
- `archive/INDEX.md`: 비활성 문서 인덱스
"""

PRD_ARCHIVE_INDEX_TEMPLATE: Final[str] = """# Archived PRD Index

| ID | Date | Status | Title | Reason |
| :--- | :--- | :--- | :--- | :--- |
| [001](../prd-001.md) | YYYY-MM-DD | `deprecated` | [Title] | [Reason for deprecation] |
"""

PRD_DOCUMENT_TEMPLATE: Final[str] = """---
id: "{doc_id}"
title: "{title}"
status: "{status}"
description: "{description}"
categories: {categories}
tags: {tags}
---

# {title} PRD (Product Requirement Document)

## 1. 개요 (Overview)

### 1.1 제품 개요
`[제품/기능의 정의와 간략한 요약을 작성하세요.]`

### 1.2 대상 사용자 및 페르소나 (Target Audience)
- `[페르소나 A]`: `[이 기능을 주로 사용할 사용자 정의 및 Pain Point]`
- `[페르소나 B]`: `[부가적인 사용자 그룹]`

### 1.3 비즈니스 및 제품 목표 (Goals & Non-Goals)
#### Goals (달성하고자 하는 목표)
- `[목표 1: 예) 사용자의 작업 준비 시간을 50% 단축한다.]`
- `[목표 2]`

#### Non-Goals (범위 외 사항)
- `[범위 외 1: 예) 이 기능에서는 모델 학습 기능을 제공하지 않으며 실행만 다룹니다.]`
- `[범위 외 2]`

---

## 2. 기획 배경 및 가치 (Rationale)

- **문제 정의 (Problem Definition)**: `[기존 제품이나 시장에서 사용자가 겪고 있는 페인 포인트]`
- **핵심 가치 (Core Value)**: `[이 해결책이 제공하는 핵심 가치와 비즈니스 기여도]`
- **가정 및 의존성 (Assumptions & Dependencies)**:
  - `[가정 1: 예) 사용자의 로컬 환경에 이미 Python 3.10 이상이 정상 설치되어 있을 것이다.]`
  - `[의존성 1: 예) 외부망 노출을 위해 Cloudflare Tunnel API에 의존한다.]`
- **주요 리스크 및 완화 방안 (Risks & Mitigations)**:
  - `[리스크 1: 예) 로컬 네트워크 보안 방화벽으로 인해 cloudflared 실행이 차단될 수 있다.]`
  - `[완화 방안 1: 예) 기동 실패 시 예외를 던지는 대신, 오프라인 모드로 실행 가능함을 사용자에게 UI상으로 안전하게 안내한다.]`

---

## 3. 사용자 시나리오 및 스토리 (User Stories)

### 3.1 유저 스토리
- **[스토리 1]**: *사용자로서(As a)* `[역할]`, `[행동]`을 *원한다(I want to)*, *그렇게 함으로써(So that)* `[가치/이점]`을 얻는다.
- **[스토리 2]**:

### 3.2 핵심 사용자 여정 (User Journey / Flow)
1. `[단계 1: 사용자가 시스템에 접속하여 환경 설정을 확인한다.]`
2. `[단계 2: 원하는 백엔드 모델을 선택하고 가동을 요청한다.]`
3. `[단계 3: 시스템이 환경을 정규화하고 준비 완료 상태를 피드백한다.]`

---

## 4. 기능 및 비기능 요구사항 (Requirements)

### 4.1 기능적 요구사항 (Functional Requirements)
기능의 중요도와 구현 범위를 정의합니다.

| 요구사항 ID | 기능명 | 기능 설명 | 우선순위 (Must/Should/Could) |
| :--- | :--- | :--- | :---: |
| FR-01 | `[기능 A]` | `[세부 기능 요구사항 및 기대 동작]` | Must |
| FR-02 | `[기능 B]` | `[세부 기능 요구사항 및 기대 동작]` | Should |

### 4.2 비기능적 요구사항 (Non-functional Requirements)
시스템의 안정성, 성능, 호환성 및 보안 지침을 정의합니다.

| 요구사항 ID | 분류 | 요구사항 설명 | 중요도 (High/Medium/Low) |
| :--- | :--- | :--- | :---: |
| NFR-01 | 성능 | `[예) 메인 엔진 기동 완료 판단은 5초 이내에 완료되어야 함]` | High |
| NFR-02 | 보안 | `[예) 외부 서비스 연동용 API Key는 런타임 내에서 복호화된 상태로 메모리에 유지되며, 파일로 평문 저장하지 않는다.]` | High |

---

## 5. UI/UX 요구사항 (User Experience)

- **핵심 흐름 (UX Flow)**:
  ```mermaid
  graph TD
      Start[사용자 진입] --> Action[기능 활성화 요청]
      Action --> Status{{상태 체크}}
      Status -->|성공| Success[성공 화면 및 결과 제공]
      Status -->|실패| Error[에러 안내 및 대안 제안]
  ```
- **화면 및 인터랙션 요구사항**:
  - `[인터랙션 1: 예) 가동 버튼을 누르면 즉시 진행 상태가 로딩 인디케이터로 표현되어야 함.]`
  - `[인터랙션 2]`

---

## 6. 인수 조건 (Acceptance Criteria)

기능이 완료되었는지(Definition of Done) 사용자 입장에서 판단하는 최종 기준입니다. QA 테스트 설계 시 기반이 됩니다.

- **AC-01: `[인수 조건 제목 1: 예) 환경 설정 자동 정규화 및 구동]`**
  - **Given**: `[주어진 환경: 사용자가 환경 설정의 일부 상대 경로를 정적 파일에 정의한 상황에서]`
  - **When**: `[동작 시: 컨텍스트 매니저를 초기화할 때]`
  - **Then**: `[기대 결과: 모든 경로가 절대 경로로 정규화되고 정상 구동이 수행된다.]`
- **AC-02: `[인수 조건 제목 2]`**
  - **Given**:
  - **When**:
  - **Then**:

---

## 7. 성공 지표 및 모니터링 (Success Metrics)

이 기능의 배포 후 성공 여부를 정량적으로 측정할 방법입니다.

- **핵심 지표 (KPIs)**:
  - `[지표 1: 예) 태스크 성공률 98% 이상 달성]`
  - `[지표 2: 예) 사용자 수동 조작 횟수 평균 3회 이하로 감소]`
- **모니터링 대상 로그/데이터**:
  - `[데이터 1: 기동 실패 에러 로그 발생 비율]`

---

## 8. 제약 사항 및 출시 계획 (Constraints & Release Plan)

- **기술적 제약**: `[예: 로컬 디스크 용량이 최소 10GB 확보된 상태에서 작동해야 함]`
- **출시 단계 (Phasing)**:
  - **Phase 1 (MVP)**: `[Must 요구사항 구현 및 로컬 환경 출시]`
  - **Phase 2**: `[Should 요구사항 구현 및 다중 사용 환경 확장]`
"""

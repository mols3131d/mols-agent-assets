# Design Notes (System Design Document)

## 1. Purpose (목적)

시스템 아키텍처, UI/UX 흐름, 모듈 레벨의 디자인을 시각화하고 구체화하여 개발 전 팀 간의 오해를 줄이고 기술적 장애물을 사전 검증합니다.

## 2. Core Methodology (핵심 원칙)

- **Validate Before You Code**: 구현에 시간을 낭비하기 전에 설계 문서를 통해 아이디어를 검증하고 결함을 찾습니다.
- **Why over What**: "무엇"을 만드는지 뿐만 아니라, "왜" 그러한 아키텍처나 디자인 패턴을 선택했는지 이유를 중점적으로 설명합니다.
- **Prioritize Simplicity**: 장황한 텍스트보다는 직관적인 다이어그램이나 와이어프레임을 통해 복잡성을 낮춥니다.

## 3. Recommended Structure (권장 구조)

- **Problem Statement**: 해결하고자 하는 문제와 비즈니스 임팩트.
- **Requirements**: 기능적 요구사항과 비기능적 요구사항(확장성, 성능, 보안 등).
- **Architecture/Flow**: 시스템 컴포넌트 간 상호작용이나 UI/UX 화면 전환 흐름 다이어그램.
- **Design Details**: 모듈별 세부 설계, 데이터 구조, API 엔드포인트 정의.
- **Assumptions & Risks**: 현재 설계를 뒷받침하는 핵심 가정과 의존성 및 잠재적 위험 요소.

## 4. Best Practices (모범 사례)

- **Iterative Process**: 초안을 일찍 공유하여 피드백을 받고 지속적으로 다듬어 나가는 과정을 거칩니다.
- **Accessible Source of Truth**: 모든 이해관계자가 쉽게 접근하고 참조할 수 있는 중앙 저장소에 문서를 보관합니다.
- **Use Diagrams**: 텍스트보다 Mermaid 다이어그램이나 스케치를 적극 활용하여 이해도를 높입니다.

## 5. Anti-Patterns (안티패턴)

- 피드백 없이 문서 완성을 고집하여 폭포수(Waterfall) 방식처럼 유연성이 떨어지는 경우.
- 코드 레벨의 사소한 변경 사항까지 전부 문서화하려고 하는 경우.
- 다이어그램 없이 텍스트로만 복잡한 아키텍처를 설명하려는 경우.

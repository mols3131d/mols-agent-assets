# Architecture Decision Record (ADR)

## 1. Purpose (목적)

시스템 아키텍처에 중대한 영향을 미치는 결정, 기술적 선택, 그리고 그에 따른 트레이드오프(Trade-offs)를 기록합니다.

## 2. Core Methodology (핵심 원칙)

- **Context over How**: 시스템 구현 방법(How)보다는 결정의 배경(Context)과 이유(Why)를 기록하는 데 집중합니다.
- **Immutable History**: 한번 수락(Accepted)된 결정이 변경될 경우, 기존 문서를 수정하지 않고 새로운 ADR을 작성하여 이전 문서를 대체(Supersede)합니다.
- **Inverted Pyramid**: 가장 중요한 정보(결정과 직접적인 영향)를 상단에 배치합니다.

## 3. Recommended Structure (권장 구조)

- **Title**: 직관적인 제목 (예: `0001-use-kafka-for-event-streaming`)
- **Status**: Proposed, Accepted, Rejected, Superseded, Deprecated
- **Context**: 문제 상황, 비즈니스 요구사항 및 제약 조건
- **Decision**: 명확하고 구체적인 결정 사항
- **Alternatives Considered**: 고려했던 대안들과 거절된 이유
- **Consequences**: 결정으로 인해 발생하는 긍정적/부정적 결과 및 트레이드오프

## 4. Best Practices (모범 사례)

- **Near the Code**: 코드가 있는 저장소(`doc/adr` 등)에 함께 보관하여 코드 변경과 함께 업데이트 되도록 합니다.
- **Async Review**: 미팅 전 문서 읽기 및 비동기 코멘트 기간을 두어 다양한 의견을 수렴합니다.
- **Make it a Habit**: 결정이 내려진 당일에 작성하여 맥락 유실을 방지합니다.

## 5. Anti-Patterns (안티패턴)

- 사소한 코드 레벨의 변경사항까지 모두 기록하는 행위 (Big Design Trap).
- 이미 구현이 모두 끝난 후 뒤늦게 작성하여 대안에 대한 맥락이 사라진 경우.
- "무엇"을 결정했는지만 적고 "왜"를 누락하는 경우.

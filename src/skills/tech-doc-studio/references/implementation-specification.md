# Implementation Specification (SPEC)

## 1. Purpose (목적)

비즈니스 요구사항(PRD)을 실제 개발 가능한 형태의 기술적 청사진으로 변환하여, 개발 전 위험 요소를 식별하고 팀을 정렬합니다.

## 2. Core Methodology (핵심 원칙)

- **How, Not What**: 시스템이 "무엇"을 해야 하는지가 아니라, "어떻게" 구축될 것인지 구체적으로 서술합니다.
- **Prioritize Clarity**: 개발자나 AI가 추가 질문 없이 개발을 시작할 수 있을 만큼 구체적인 입출력, 상태, 엣지 케이스를 정의합니다.
- **Address Risks Early**: 병목, 보안 취약점, 스케일링 이슈를 설계 단계에서 미리 식별하여 후속 비용을 줄입니다.

## 3. Recommended Structure (권장 구조)

- **Overview & Goals**: 문제 정의 및 구현 목표.
- **System Architecture**: 하이레벨 컴포넌트, 데이터 모델, 연동 포인트 다이어그램.
- **Implementation Details**: API 컨트랙트, 데이터 흐름, 알고리즘, 설정 값 등 구체적 구현 방식.
- **Error Handling & Edge Cases**: 예외 상황 처리 및 실패 시나리오 대응 방안.
- **Test & Validation Plan**: 구현이 예상대로 동작하는지 확인하기 위한 검증 계획 및 성공 기준.
- **Risks & Alternatives**: 고려한 대안과 최종 방식을 선택한 트레이드오프(Trade-offs).

## 4. Best Practices (모범 사례)

- **Explain the Trade-offs**: 단순히 솔루션만 나열하지 않고, 다른 대안을 왜 기각했는지 명시하여 향후 유지보수를 돕습니다.
- **Understand Your Audience**: 엔지니어뿐만 아니라 PM도 읽을 수 있도록 명확한 언어와 다이어그램을 활용합니다.
- **Living Document**: 개발 과정에서 기술적 결정이 변경될 때마다 문서를 업데이트하여 최신 상태를 유지합니다.

## 5. Anti-Patterns (안티패턴)

- PRD(기능 요구사항)의 내용을 기술적 세부사항 없이 그대로 복사 붙여넣기 하는 경우.
- 정상적인 시나리오(Happy Path)만 기록하고 에러 핸들링이나 엣지 케이스를 누락하는 경우.
- "한 번 작성하고 방치(Write once, ignore later)"하는 태도.

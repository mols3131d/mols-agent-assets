# Common Design

Skill, Rule, Subagent에 공통으로 적용되는 설계 판단을 다룬다. 자산 유형 고유의 판단은 각 유형의 `design.md`가 소유한다.

## Responsibility

파일이나 형식보다 먼저 책임을 정한다.

- 이미 책임을 소유한 자산이 있으면 경쟁 owner를 만들기보다 기존 owner 확장을 우선한다.
- 새 책임이나 큰 변경은 실제 사용 사례로 추상화가 맞는지 확인한다.
- 인접 자산과 혼동하기 쉬우면 대표적인 non-use 또는 near-miss도 함께 본다.
- 관련 권한과 주변 자산을 확인한 뒤에도 owner나 자산 유형이 모호하면 추측으로 새 owner를 만들지 않는다.

## Authority

결정별 권한을 구분한다.

1. 사용자와 프로젝트 지침은 요청 결과와 허용 범위를 소유한다.
1. source framework는 canonical representation을 소유한다.
1. target runtime은 target-specific behavior를 소유한다.
1. repository convention은 local delta를 소유한다.
1. 개별 자산은 위 권한보다 좁은 자체 요구사항을 소유할 수 있다.

빠르게 변하는 vendor field, path, discovery, packaging, permission, runtime semantics를 범용 규칙으로 복제하지 않는다. 결과에 영향을 주는 경우 현재 authoritative source를 확인한다.

## Precision

실패 비용과 변동성에 비례해 제약의 강도를 정한다.

- 여러 접근이 유효하면 outcome, constraint, heuristic 중심으로 둔다.
- 일관성이 중요하면 선호 구조를 명시한다.
- 순서, 재현성, 안전성이 취약하면 deterministic mechanics나 좁은 절차를 사용한다.
- 일반적인 모델 지식을 포괄성을 위해 반복하지 않는다.
- 서로 다른 자산을 겉으로 통일하기 위한 추상화 계층을 만들지 않는다.

## Boundary

변경 전에 write boundary를 정한다. 권한, dependency, 예시를 읽었다고 쓰기 권한까지 생기지 않는다.

- unrelated asset을 함께 정규화하지 않는다.
- generated/projection은 해당 계약이 명시적으로 다르게 정하지 않는 한 파생 결과로 취급한다.
- 외부 자산을 재사용하면 필요한 attribution, license, upstream revision을 보존한다.

# 결정 기록

## Proposed

| Decision | Reason | Impact |
| :--- | :--- | :--- |

## Accepted

| Decision | Reason | Impact |
| :--- | :--- | :--- |
| **[원칙 준수 중심] Iceberg 원칙 준수가 핵심 목표** | 절차적인 워크플로우보다 핵심 원칙을 에이전트가 준수하도록 강제하는 것이 목표임 | 구체적인 개발 절차나 스텝보다 에이전트의 사고방식과 제약 조건 전달에 집중함 |
| **[강도 설정] lite, full, ultra 인자 지원** | 상황과 토큰 한도에 맞춰 Iceberg 원칙 적용 수준을 조절할 수 있어야 함 | 사용자가 `lite`, `full`, `ultra` 수준을 인자로 전달하여 작동 강도를 결정함 |
| **[기본값] 기본 강도는 lite** | 불필요한 토큰 낭비와 엄격성을 방지하기 위함 | 인자가 명시되지 않은 경우 `lite` 모드로 작동함 |

## Superseded

| Decision | Reason | Impact |
| :--- | :--- | :--- |

## Deprecated

| Decision | Reason | Impact |
| :--- | :--- | :--- |

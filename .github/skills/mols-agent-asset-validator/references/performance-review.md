# Performance Review

## Purpose

에이전트 자산의 품질뿐 아니라 자산을 해석·선택·실행·유지하는 비용과 안정성을 검토한다. 단순한 길이, 규칙 수 또는 파일 수만으로 결론을 내리지 않는다.

## Instruction Bottleneck

지침은 다음 중 하나를 해야 한다.

- Material failure를 방지한다.
- 안정적인 권한·안전·품질 경계를 정의한다.
- 프로젝트에 고유한 사실이나 관행을 제공한다.
- 출력이나 handoff의 필수 계약을 보존한다.

다음은 병목 후보다.

- 모델이 이미 안정적으로 수행하는 상식적 절차를 세세하게 강제함
- 목적과 경계보다 순서·표현·중간 사고 과정을 과도하게 통제함
- 같은 규칙이 여러 자산에 반복됨
- 예외와 예외의 예외가 누적되어 우선순위 해석 비용이 커짐
- 낮은 가치의 규칙이 중요한 안전·권한 규칙을 가림
- 특정 모델·UI·폴더명·도구명에 불필요하게 결합됨

각 병목 후보에는 제거·완화했을 때의 위험과 유지 비용을 함께 기록한다. 짧다는 이유만으로 좋은 지침이라고 판단하지 않는다.

## Context Noise Bottleneck

컨텍스트는 현재 요청의 판단과 행동에 직접 기여해야 한다.

검토 항목:

- 중복되거나 의미가 겹치는 지침
- 사용되지 않거나 도달할 수 없는 Reference·Template·Config
- 항상 로드되지만 특정 경우에만 필요한 자산
- 오래되었거나 현재 Contract와 충돌하는 Example·Summary
- 관련 정보가 여러 파일에 멀리 분산되어 발생하는 탐색 비용
- 중요한 규칙이 긴 설명·예시·상식적 문장에 묻히는 signal dilution
- Context 선택 자체가 본 작업보다 복잡해지는 구조

File size, line count와 reference count는 신호일 뿐이며 의미적 관련성 검토 없이 noise로 단정하지 않는다.

## Stability

안정성을 네 관점으로 분리한다.

| Type | Questions |
| --- | --- |
| Behavioral | 동일한 요청과 조건에서 Trigger, Tool 선택, Finding과 출력이 허용 가능한 범위로 일관적인가 |
| Failure | Missing input, Tool failure, timeout, partial result와 retry에서 안전하게 종료·복구하는가 |
| Change | 이름, 경로, Project override, Config, Template 또는 자산 재배치 후에도 핵심 Contract가 유지되는가 |
| Runtime | 모델, executor, permission, fixture 또는 Trial 변화에서 pass rate와 failure mode가 어떻게 달라지는가 |

Runtime Trial이 없으면 Behavioral·Runtime Stability를 verified로 판정하지 않는다. 구조적 복구 경계는 verified 또는 inferred로 구분할 수 있다.

## Human Comprehension Debt

사람이 자산을 운영하거나 변경하기 위해 지불하는 해석·탐색·검증 비용을 검토한다.

- 목적과 Trigger를 처음 읽는 사람이 빠르게 파악할 수 있는가
- 최종 decision owner와 변경 owner가 명확한가
- 규칙, 근거, 설명, 예시와 설정이 구분되는가
- 하나의 개념에 하나의 안정적인 용어를 사용하는가
- 예외와 실패 경로가 가까운 위치에 있는가
- Finding이나 Runtime 결과를 원본 자산까지 추적할 수 있는가
- 하나의 변경이 여러 파일의 연쇄 수정을 요구하는가
- 암묵적인 관행을 추측해야만 안전하게 수정할 수 있는가
- 헤딩과 파일 구조만으로 주요 관계와 변경 영향을 예측할 수 있는가

Human Comprehension Debt는 문체 취향이 아니다. 잘못된 변경, 느린 검토, 소유권 혼란 또는 운영 의존성을 유발하는 이해 비용만 material Finding으로 기록한다.

## Finding Guidance

| Signal | Typical severity |
| --- | --- |
| 중요한 안전·권한 규칙이 noise에 묻혀 잘못된 행동을 유발함 | `critical` 또는 `major` |
| 과도한 지침이 정상적인 판단을 지속적으로 방해함 | `major` |
| Runtime 없이 안정성을 보장한다고 주장함 | `major` |
| 사람만 알고 있는 암묵 규칙 때문에 안전한 수정이 어려움 | `major` |
| 중복·분산으로 유지 비용이 증가하지만 행동 결함은 아직 없음 | `minor` |
| 단순 개선 기회 | `note` |

Finding은 항상 실제 영향, Evidence Level과 제거·변경 위험을 포함한다.

# Quality Model

## Gate

아래 항목 중 하나라도 중대한 실패면 통과시키지 않는다.

| Dimension | Pass Condition |
| --- | --- |
| Intent | 목적·요구사항·불변 조건을 보존한다. |
| Triggering | 필요한 요청에서 활성화되고 무관한 요청에서 과활성되지 않는다. |
| Executability | 지침, 도구, 경로, 명령이 실제 환경에서 수행 가능하다. |
| Structure | 핵심과 상세가 적절히 분리되고 참조가 직접 탐색 가능하다. |
| Efficiency | 중복, 장황함, 불필요한 단계와 컨텍스트 비용이 낮다. |
| Consistency | 파일 간 용어, 우선순위, 포맷, 링크가 충돌하지 않는다. |
| Portability | 공통 코어와 환경 전용 규칙이 분리되어 있다. |
| Regression | 기존의 유효한 핵심 동작이 유지된다. |
| Safety | 사용자 기대 밖의 권한 확대·은닉 동작·데이터 유출이 없다. |
| Packaging | 필요한 runtime 자산만 포함하고 maintainer-only·evaluation·development material은 target contract가 요구하지 않으면 제외한다. |

## Review Questions

- 이 문장이 없어도 유능한 에이전트가 같은 결과를 낼 수 있는가?
- 동일 정보가 다른 파일에도 존재하는가?
- 특정 환경의 우연한 관례를 범용 불변 조건으로 만들었는가?
- 핵심 경로보다 예외·초급 설명·API 나열이 더 큰가?
- 실패했을 때 원인을 찾고 복구할 기준이 남아 있는가?
- 검증 결과가 실제 동작을 증명하는가, 단순 형식 통과에 그치는가?
- runtime package에 실행과 무관한 maintainer·eval·개발 자료가 섞였는가?

## Loop Policy

1. 실패를 의도, 구조, 실행, 호환성, 회귀, 안전, 패키징으로 분류한다.
1. 가장 근본적인 원인을 먼저 수정한다.
1. 같은 검증을 다시 실행한다.
1. 최대 반복 이후에도 실패하면 blocker와 근거를 기록한다.

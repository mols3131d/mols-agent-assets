---
description: mols-coding-context-python의 설계 의도, 책임 경계, 지침 채택·제거 및 행동 회귀 평가를 검토할 때 사용합니다.
---

# Python Coding Context

[mols-coding-context-python](../../../src/rulesync/.rulesync/skills/mols-coding-context-python/SKILL.md)은 [mols-coding-context](../mols-coding-context/guidance.md)의 언어별 확장이다. Python의 의미와 런타임 특성에서 발생하는 에이전트의 실질적인 판단 오류를 줄이는 데 필요한 delta만 주입한다. 실행 판단과 선택 조건은 SKILL.md가 소유하며, 이 문서는 유지보수 시에만 참조한다.

## Activation

Python의 의미 또는 실행 계약이 중요한 코딩 작업에 처음 진입할 때 Core와 함께 로드한다. 작업 도중 처음 필요해지거나 컨텍스트가 유실되면 필요한 시점에 로드하고, 유지되는 동안 재사용한다. 단순 Python 언급, 사실 조회, 비코딩 저장소 관리, 일반 문서 작업은 제외한다. 최초 로딩은 description이 표현하는 선택 의도이며 런타임이 강제하는 호출 횟수 제한이 아니다.

## Maintenance

Core의 공통 유지 원칙에 더해 다음 경계를 적용한다.

- **Core ownership:** 언어 독립적인 판단은 Core가 소유한다. Python에 적용된다는 이유로 재정의하거나 복제하지 않는다. 범용 개선은 Core에서 검토하고 흡수된 지침은 add-on에서 제거한다.
- **Deterministic tooling:** formatter, linter, type checker, schema validator 등 결정적 도구로 충분히 판정·해소할 수 있는 문제는 제외한다. 도구가 설치되지 않았더라도 규칙 목록이나 수정 절차를 복제하지 않는다. 도구 설정·설치·실행도 별도 책임이다.
- **Python delta:** 코드의 외형이나 도구 결과만으로 결정할 수 없는 Python 고유의 의미와 실행 계약에 집중한다. 모델이 이미 충분히 아는 문법·일반 Python 지식, 모범 사례 목록, 라이브러리 사용법, 버전별 API 사실과 워크플로우는 주입하지 않는다.
- **Evidence and cost:** 반복되는 실질적 판단 오류를 줄일 근거가 있는 지침만 채택한다. 모델·Core·도구의 발전에 따라 독립 판단 가치가 사라진 지침은 제거한다. 의미·조건·예외를 보존하면서 토큰과 추론 비용을 낮추고, 유지보수 근거는 실행 본문에 복제하지 않는다.

현재 판단 영역은 예외의 실제 발생 경로, 정적 타입과 런타임 계약의 차이, import 및 실행 환경의 계약, asyncio의 소유권과 수명, interpreter/build별 동시성 보장이다. 정적 검사 통과만으로는 이 영역의 동작 타당성을 확정할 수 없다. 일반적인 실패 처리·복잡성·성능 판단은 Core에 위임하고, Windows batch 실행 시 subprocess의 shell 해석처럼 특정 API·플랫폼에 국한된 사례는 해당 작업의 공식 문서 확인에 맡긴다.

## Evaluation

[저장소 평가 정책](../../development/evaluation.md)에 따라 동일한 모델·런타임·하네스·도구 조건에서 Core 단독, 기존 add-on 동반, 변경된 add-on 동반 조건을 비교한다. 구체적인 평가 계약과 fixture는 evals/가 소유한다.

| 대상 | 확인할 행동 |
| --- | --- |
| 선택·로딩 | Python 코딩 작업의 최초 동반 선택, 도중 최초 필요 및 컨텍스트 유실 시 선택, 유지 중 재사용, 비코딩·사실 조회의 비선택 |
| 판단 품질 | 의도하지 않은 예외 처리, 타입 오류 해소 중 런타임 계약 훼손, import 우회, asyncio 취소·소유권 위반, 동시성 보장에 대한 잘못된 가정 감소 |
| 회귀·비용 | 불필요한 검증·수정·도구 호출·재로딩 및 과잉 방어 로직 증가 여부, 측정 가능한 입력·추론 토큰과 소요 시간 |

정적 검토와 결정적 검증은 실제 모델 평가를 대체하지 않는다. 실행 근거 없이 행동 동등성, 품질 향상 또는 비용 절감을 단정하지 않는다.

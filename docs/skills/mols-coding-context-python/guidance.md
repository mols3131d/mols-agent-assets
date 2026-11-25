---
description: mols-coding-context-python의 설계 의도, Core와의 책임 경계, 지침 채택 및 행동 회귀 평가를 검토할 때 사용합니다.
---

# Python Coding Context

[mols-coding-context-python](../../../src/rulesync/.rulesync/skills/mols-coding-context-python/SKILL.md)은 [mols-coding-context](../mols-coding-context/guidance.md)의 언어별 확장이다. Python의 의미와 실행 계약에 따른 추가 판단 오류를 줄인다. 실행 판단과 선택 조건은 SKILL.md가 소유하며, 이 문서는 유지보수 시에만 참조한다.

## Activation

[Core의 로딩 원칙](../mols-coding-context/guidance.md#activation)을 따르되 Python의 의미 또는 실행 계약이 중요한 코딩 작업에만 함께 적용한다. 단순 Python 언급이나 언어와 무관한 작업은 제외한다.

## Maintenance

[Core의 유지보수 기준](../mols-coding-context/guidance.md#maintenance)에 더해 다음 조건으로 Python delta를 판단한다.

- **Ownership:** Core가 소유하는 판단을 재정의하거나 중복하지 않는다. 언어 독립적인 개선은 Core에서 검토하고, 흡수된 지침은 add-on에서 제거한다.
- **Admission:** 모델·Core·결정적 도구만으로 충분하지 않은 Python 고유의 판단에 한해, 실질적인 오류를 줄일 근거가 있을 때 채택한다. Formatter, linter, type checker, schema validator의 규칙과 기계적 수정은 이들의 책임이다. 도구 결과만으로 결정할 수 없는 실행 의미와 계약을 보강한다.
- **Retention:** 일반 Python 지식, 관용구, 라이브러리 사용법, 특정 API·플랫폼의 세부 사실, 워크플로우는 상시 주입하지 않는다. 세부 동작은 필요한 시점에 공식 문서에서 확인한다. 모델·Core·도구의 발전으로 추가 판단 가치가 사라지면 제거한다.

## Evaluation

[Core의 평가 기준](../mols-coding-context/guidance.md#evaluation)을 적용하되, Core 단독과 기존·변경 add-on 동반 조건을 비교하여 확장의 순효과를 확인한다.

- Python 판단이 필요한 작업에서 최초 동반 선택과 재사용이 이루어지고, 단순 언급이나 언어와 무관한 작업에서는 선택되지 않는지 확인한다.
- Python 고유의 실행 의미에 따른 계약 위반이 줄어드는지, 타입 오류를 해결하려고 불필요한 런타임 변경·방어 로직을 추가하거나 실행 환경을 우회하는 등의 새로운 회귀가 생기지 않는지 비교한다.

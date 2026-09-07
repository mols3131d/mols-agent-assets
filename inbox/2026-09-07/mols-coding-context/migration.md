# `mols-coding-context` migration

이 문서는 기존 generic `coding-context`를 새 core/add-on 구조로 교체하는 계획만 소유한다.

## Target

```text
coding-context
→ mols-coding-context

Python-material task
→ + mols-coding-context-python
```

다른 Skill family는 이번 migration 대상이 아니다.

## Disposition

| Asset | Decision |
| --- | --- |
| `coding-context` | 신규 core가 gate를 통과하면 교체 후 삭제 |
| `mols-coding-context` | 새 main/core |
| `mols-coding-context-python` | 새 Python add-on |
| `mols-clarify-code` | 유지 |
| `mols-code-comprehension-refactor` | 유지 |
| `mols-clarify-runtime` | 유지 |
| 다른 Skill family | 유지 |

## Preserve in Core

기존 `coding-context`에서 다음 의미를 보존한다.

- effectiveness / operability / simplicity / elegance tie-break
- anti-dogmatic KISS / YAGNI / DRY / SRP
- system fit
- smallest coherent change
- behavior/compatibility preservation
- evidence와 verification truthfulness
- failure context와 operability

신규 core는 이 의미를 더 작은 ownership 구조로 정리하고, language-specific detail을 소유하지 않는다.

## Add Python

Python add-on은 다음 delta만 추가한다.

- exception/fallback semantics
- `asyncio` blocking/cancellation/task lifetime
- dynamic data boundary/coercion/defaulting
- subprocess/shell/dynamic execution
- Python generated-code review lens

Core의 generic wording을 복제하지 않는다.

## Phases

### 1. Introduce

- core와 Python add-on 생성
- 기존 `coding-context`와 일시 공존
- routing/behavior eval 준비

### 2. Compare

Old generic owner와 new core를 representative coding task에서 비교한다.

확인:

- routing recall/precision
- smallest coherent change
- contract preservation
- failure/uncertainty semantics
- unnecessary abstraction/operational ceremony
- verification truthfulness

### 3. Validate add-on

```text
non-Python coding
→ core

Python-material coding
→ core + python

Python incidental
→ core only 또는 coding context 자체가 불필요
```

Python add-on 단독 선택은 failure다.

### 4. Replace

Gate 통과 후에만:

- 기존 `coding-context` canonical directory 삭제
- old-name live reference 정리
- repository-native generation으로 route/projection 갱신
- obsolete eval fixture 정리

### 5. Clean up

- stale migration wording 제거
- generated drift 확인
- inbox artifact의 보존/승격 여부 별도 판단

## Deletion Gate

기존 `coding-context`는 다음을 모두 만족해야 삭제한다.

1. 신규 core가 representative generic coding task에서 안정적으로 선택됨
2. 기존 material behavior가 유지되거나 개선됨
3. Python add-on이 core와 올바르게 함께 선택됨
4. Python incidental case에서 과선택되지 않음
5. Conditional rule이 speculative work를 늘리지 않음
6. Old name을 요구하는 live consumer가 없거나 migration path가 확인됨
7. Route/projection cleanup path가 확인됨
8. 실행하지 않은 eval을 통과했다고 주장하지 않음

Asset 수 감소 자체는 gate가 아니다.

## Rollback

신규 core가 기존 `coding-context`보다 routing/behavior가 나쁘면 삭제를 중단한다.

문제가 Python-specific이면 core를 키우지 않고 add-on을 조정한다. 다른 language-specific need가 생겨도 같은 원칙으로 별도 add-on을 검토한다.

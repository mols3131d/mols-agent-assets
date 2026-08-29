---
description: 반복적으로 깨질 때 비용이 큰 안정된 architecture invariant를 어디까지, 어떤 비용으로 검증할지 판단하고 별도 architecture test surface를 구성할 때 참고하는 패턴 초안입니다.
---

# Executable Architecture Invariants

Status: **draft candidate**

Repository에서 반복적으로 깨질 때 비용이 큰 **소수의 안정된 architecture invariant**가 있다면, 문서에만 의존하기보다 가능한 경우 가장 싼 신뢰 가능한 mechanism으로 위반을 확인할 수 있게 하는 것을 고려합니다.

핵심은 architecture를 가능한 많이 검사하는 것이 아닙니다.

> **검증할 가치가 있는 invariant만 선택하고, 가장 가벼운 enforcement부터 시작하며, 관리 비용이 이득보다 커지면 추가하지 않거나 제거합니다.**

## Problem

Architecture rule이 문서와 review에만 존재하면 같은 실수가 반복될 수 있습니다.

예를 들어 repository가 다음 dependency direction을 의도한다고 가정합니다.

```text
UI
 ↓
Application
 ↓
Domain
```

`Domain`이 infrastructure implementation을 직접 참조하면 안 된다는 경계가 충분히 안정되어 있는데도 다음 코드가 반복해서 생길 수 있습니다.

```python
# domain/order.py
from infrastructure.database import database
```

코드는 동작하고 일반 behavior test도 통과할 수 있지만, repository가 유지하려던 dependency boundary는 깨집니다.

이런 위반이 반복되고 복구 비용도 크다면 사람이나 agent에게 같은 warning을 계속 설명하는 것보다 **좁고 기계적인 feedback surface**를 두는 편이 나을 수 있습니다.

## What May Be Worth Enforcing

다음 성질이 많이 겹칠수록 executable invariant 후보가 될 수 있습니다.

- 위반 여부를 비교적 객관적으로 판정할 수 있습니다.
- 같은 유형의 위반이 실제로 반복되거나 반복될 가능성이 높습니다.
- 위반을 늦게 발견할수록 수정·migration·recovery 비용이 커집니다.
- project의 architecture에서 비교적 오래 유지될 안정된 경계입니다.
- review에서 사람이 같은 판단을 반복하고 있습니다.
- 검증 mechanism의 유지 비용이 위반을 방치하는 비용보다 충분히 작습니다.

반대로 readability, naming, abstraction quality처럼 context-dependent judgment가 중요한 항목은 중요하더라도 기계적 invariant로 만들기 어려울 수 있습니다.

## Progressive Enforcement

새 invariant를 발견했다고 바로 custom test나 CI rule을 만들 필요는 없습니다.

가능하면 더 싼 수단부터 비교합니다.

```text
별도 enforcement 없음
        ↓
language / module mechanism
        ↓
compiler / type / visibility
        ↓
기존 linter / dependency check
        ↓
좁은 architecture test
        ↓
custom enforcement
```

낮은 계층에서 자연스럽게 보장되는 invariant를 별도 custom CI로 다시 구현하지 않습니다.

예를 들어 package visibility로 internal implementation 접근을 막을 수 있다면 별도 architecture test가 필요하지 않을 수 있습니다.

## Architecture Test Surface

별도의 executable test가 실제로 필요하다면 일반 behavior test와 구분되는 **architecture test surface**를 둘 수 있습니다.

대표적인 형태는 다음과 같습니다.

```text
tests/
├─ unit/
├─ integration/
└─ architecture/
   ├─ test_dependency_direction.py
   ├─ test_module_boundaries.py
   └─ test_generated_ownership.py
```

`tests/architecture/`는 권장 가능한 대표 형태이지 모든 repository가 따라야 하는 고정 layout은 아닙니다. Framework나 language가 더 자연스러운 convention을 제공하면 그것을 우선합니다.

### Why Separate It

일반 behavior test와 architecture test는 질문이 다릅니다.

| Surface | 주로 답하는 질문 |
| --- | --- |
| Behavior test | 기능이 의도대로 동작하는가? |
| Architecture test | repository가 유지하려는 구조적 경계가 깨지지 않았는가? |

둘을 같은 directory에 무분별하게 섞으면 test를 탐색하거나 실패 원인을 해석할 때 성격을 구분하기 어려워질 수 있습니다.

Directory 자체가 이미 의미를 제공하므로 filename마다 `architecture_` prefix나 `_architecture` suffix를 반복할 필요는 보통 크지 않습니다.

```text
# 충분히 구분되는 예
tests/architecture/test_dependencies.py

# 중복될 수 있는 예
tests/architecture/test_architecture_dependencies.py
```

## Optional Runner Marker

Test runner가 marker나 tag를 지원하고 architecture tests만 선택 실행할 필요가 있다면 별도 marker를 함께 사용할 수 있습니다.

예를 들어 pytest에서는 다음과 같은 형태를 고려할 수 있습니다.

```python
pytestmark = pytest.mark.architecture
```

이때 역할은 다릅니다.

```text
tests/architecture/     → 사람이 탐색할 때의 구분
architecture marker     → runner가 선택 실행할 때의 구분
```

Marker가 실제 선택 실행이나 CI routing에 쓰이지 않는다면 형식만을 위해 추가하지 않습니다.

## Examples

### Dependency Direction

```text
Domain → Infrastructure import 금지
```

이 경계가 충분히 안정되고 위반이 반복된다면 dependency graph check나 architecture test를 고려할 수 있습니다.

### Internal Module Boundary

```text
orders/
└─ internal/
```

외부 package가 `internal/` 구현에 직접 접근하지 않는다는 invariant는 language/package visibility가 지원한다면 그 mechanism을 먼저 사용합니다.

### Generated Ownership

```text
schema/
   ↓ generate
generated/
```

Generated output을 직접 수정하면 다음 generation에서 변경이 사라지는 repository라면 직접 수정 여부를 검증하는 check가 도움이 될 수 있습니다. 다만 generator 자체가 ownership을 충분히 명확하게 보장한다면 별도 test를 추가할 필요는 없습니다.

## Cost Check

Invariant가 중요하다는 이유만으로 enforcement가 자동으로 정당화되지는 않습니다.

도입 전에는 최소한 다음을 비교합니다.

```text
반복되는 위반의 기대 비용
             ↕
enforcement의 구현 + 유지 + 실패 해석 비용
```

다음 상황은 별도 검증을 보류하거나 제거할 신호가 될 수 있습니다.

- 거의 발생하지 않는 위반을 위해 복잡한 custom analyzer가 필요합니다.
- false positive 때문에 예외 목록이 계속 늘어납니다.
- rule을 통과하기 위한 wrapper나 우회 구조가 생깁니다.
- architecture가 자주 바뀌어 rule도 함께 계속 수정해야 합니다.
- failure가 발생해도 왜 실패했는지 이해하기 어렵습니다.
- 기존 compiler, type system, module system이 같은 invariant를 더 싸게 보장하기 시작했습니다.

## Limits and Responses

| Limitation | Possible response |
| --- | --- |
| 검사 가능한 것만 중요하게 보일 수 있음 | 기계 검증 밖의 design judgment가 계속 필요함을 명확히 둡니다. |
| rule이 계속 늘어나 CI noise가 커질 수 있음 | 반복적이고 비용 큰 invariant만 남기고 low-value rule은 추가하지 않거나 삭제합니다. |
| architecture를 너무 일찍 고정할 수 있음 | 아직 탐색 중인 boundary는 guidance로 남기고 충분히 안정된 뒤 enforcement를 검토합니다. |
| 단순한 syntactic rule을 우회하는 코드가 생길 수 있음 | 실제 보호하려는 boundary를 더 직접적으로 표현하거나 rule 자체의 가치를 다시 검토합니다. |
| custom tooling 관리 비용이 커질 수 있음 | language/module/compiler 같은 더 낮고 표준적인 mechanism으로 내릴 수 있는지 먼저 봅니다. |
| 현재 preference가 영구 invariant처럼 굳을 수 있음 | 이 규칙이 장기간 유지될 invariant인지, 현재 convention인지 도입 전에 구분합니다. |

## Rule Lifecycle

Enforcement도 영구적이라고 가정하지 않습니다.

다음 변화가 생기면 기존 check를 다시 검토할 수 있습니다.

- architecture 자체가 바뀌었습니다.
- language나 framework가 같은 invariant를 기본 기능으로 지원합니다.
- 위반 가능성이 사라졌습니다.
- check의 유지 비용이 실제 보호 가치보다 커졌습니다.
- 여러 rule이 더 단순한 하나의 mechanism으로 통합될 수 있습니다.

```text
custom check
    ↓
더 단순한 native mechanism
    ↓
기존 check 삭제
```

검증을 추가하는 것뿐 아니라 **더 이상 필요하지 않은 검증을 제거하는 것**도 이 패턴의 일부입니다.

## Boundary

이 패턴은 모든 design preference를 test로 바꾸는 방법이 아닙니다.

또한 `tests/architecture/`라는 directory를 만드는 것 자체가 목적도 아닙니다. Compiler, module system, package visibility 등으로 더 직접적이고 저렴하게 보호할 수 있다면 별도 architecture test를 만들지 않는 편이 더 단순할 수 있습니다.

Architecture test가 실제로 필요할 때는 일반 behavior test와 구분되는 surface를 두는 것이 탐색과 운영에 도움이 될 수 있다는 정도로 봅니다.

## Promotion Questions

- `Executable Architecture Invariants`보다 `Progressive Invariant Enforcement` 또는 `Architecture Invariant Tests`가 core를 더 정확하게 표현하는가?
- architecture 영역에만 한정할지, broader repository invariant까지 다룰지 경계를 더 좁혀야 하는가?
- `tests/architecture/`가 대표 형태로 충분히 범용적인가, ecosystem별 차이를 더 조사해야 하는가?
- invariant를 추가할 때보다 **추가하지 않을 때의 판단 기준**이 충분히 명확한가?
- rule lifecycle과 removal 기준이 실제 management cost를 억제하는 데 충분한가?

## Short Form

> **반복적으로 깨질 때 비용이 큰 안정된 architecture invariant만 골라 가장 싼 mechanism으로 보호합니다. 별도 test가 필요하다면 일반 behavior test와 구분되는 architecture test surface를 고려하고, 검증의 유지 비용이 이득보다 커지거나 더 단순한 mechanism이 생기면 추가하지 않거나 제거합니다.**

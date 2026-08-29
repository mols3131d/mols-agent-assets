---
description: source와 test의 대응 관계를 navigation cue로 활용하고, test surface가 커질 때 sibling files나 bundle 같은 구조를 선택할 때 참고하는 패턴입니다.
---

# Source-Mirrored Test Structure

Test structure가 production source와 어느 정도 대응되면 **source를 찾은 뒤 관련 테스트의 위치를 예측하기 쉬워집니다.** 특히 `tests/`처럼 production code와 test tree가 분리된 repository에서 유용한 navigation pattern입니다.

여기서 mirroring은 source tree를 그대로 복사한다는 뜻이 아닙니다. Source path는 테스트를 배치하는 **좋은 탐색 단서 중 하나**이고, 테스트가 실제로 다루는 feature, behavior 또는 system boundary가 더 자연스러운 경우에는 그 경계를 따를 수 있습니다.

## Purpose

관련 source와 test 사이의 위치 관계를 쉽게 추측할 수 있게 하여 다음과 같은 비용을 줄이는 것이 목적입니다.

- source를 수정할 때 관련 테스트를 찾는 비용
- test tree만 보고 어느 production 영역을 검증하는지 파악하는 비용
- 테스트가 커졌을 때 어디에서 나누고 확장할지 결정하는 비용

핵심은 완벽한 대칭이 아니라 **예측 가능한 대응 관계**입니다.

## Core

자연스러운 source anchor가 분명할 때 source와 가까운 test structure는 단순한 형태 중 하나입니다.

```text
src/
└─ billing/
   ├─ invoice.py
   └─ tax.py

tests/
└─ billing/
   ├─ test_invoice.py
   └─ test_tax.py
```

`src/billing/invoice.py`를 본 사람은 `tests/billing/test_invoice.py`를 먼저 찾아볼 수 있습니다. `src/` 같은 상위 prefix를 test tree에서 생략하거나 framework convention에 맞춰 이름을 바꾸더라도 이 대응 관계는 유지될 수 있습니다.

이 구조는 source architecture를 새로 정의하거나 test design을 source implementation에 결합하기 위한 것이 아닙니다. **이미 존재하는 구조를 navigation cue로 재사용하는 것**에 가깝습니다.

## Typical Forms

### File-to-file

테스트 범위가 작고 하나의 파일에서 충분히 읽히는 경우의 가장 단순한 형태입니다.

```text
src/orders/service.py
          ↓
tests/orders/test_service.py
```

### File-to-sibling-files

하나의 test file이 여러 behavior나 scenario를 담게 되면 같은 directory의 sibling files로 나누는 형태를 사용할 수 있습니다.

```text
src/
└─ billing/
   └─ invoice.py

tests/
└─ billing/
   ├─ test_invoice_create.py
   ├─ test_invoice_adjust.py
   └─ test_invoice_failures.py
```

이 형태는 source와의 대응을 filename에 남기면서 새로운 directory depth를 만들지 않습니다. 반면 같은 prefix가 반복되거나 directory의 file density가 높아지면 grouping 자체를 별도 directory로 드러내는 편이 더 읽기 쉬워질 수 있습니다.

### Files-to-bundle

같은 production unit이나 behavior에 속하는 sibling test files가 하나의 독립적인 탐색 영역처럼 보이기 시작하면 directory bundle로 묶는 형태를 선택할 수 있습니다.

```text
src/
└─ billing/
   └─ invoice.py

tests/
└─ billing/
   └─ invoice/
      ├─ test_invoice_create.py
      ├─ test_invoice_adjust.py
      ├─ test_invoice_failures.py
      └─ test_invoice_permissions.py
```

Bundle은 반복되는 grouping을 directory 이름으로 압축하고, 관련 fixture·data·snapshot·helper 같은 local context를 가까이 둘 수 있다는 장점이 있습니다. 내부 파일은 source의 private function이나 구현 순서를 다시 mirror하기보다 behavior, scenario, contract처럼 테스트를 읽고 변경할 때 의미 있는 경계로 나누는 형태가 흔합니다.

### Boundary-to-bundle

테스트가 여러 source unit을 함께 다루면서 하나의 안정적인 behavior를 검증한다면 literal source path 대신 그 behavior가 bundle의 이름이 될 수 있습니다.

```text
src/
└─ billing/
   ├─ invoice.py
   ├─ payment.py
   └─ ledger.py

tests/
└─ billing/
   ├─ test_invoice.py
   └─ checkout/
      ├─ test_checkout_success.py
      └─ test_checkout_failures.py
```

`checkout/`은 source directory를 그대로 복제한 것은 아니지만, 테스트가 다루는 경계를 더 잘 보여줄 수 있습니다.

## Choosing the Alignment

Source path가 항상 가장 좋은 organizing axis는 아닙니다. 테스트의 성격에 따라 다음 축 가운데 하나가 더 자연스러울 수 있고, repository 안에서 여러 축을 조합할 수도 있습니다.

| Alignment | 잘 맞는 경우 | Example |
| --- | --- | --- |
| Source unit | 한 module/file이 자연스러운 anchor | `tests/billing/test_invoice.py` |
| Feature / domain | 여러 module이 하나의 기능 경계를 형성 | `tests/billing/checkout/` |
| Behavior / contract | 내부 구조보다 외부에서 보이는 동작이 더 안정적 | `tests/api/authentication/` |
| Test / system boundary | 여러 영역을 함께 검증하는 integration·e2e·compatibility test | `tests/integration/`, `tests/e2e/` |

이 축들은 배타적이지 않습니다. 예를 들어 `tests/integration/billing/`처럼 test level과 domain을 함께 사용할 수도 있습니다.

어떤 축을 먼저 드러낼지는 **사람이 테스트를 찾을 때 가장 먼저 알고 있는 정보가 무엇인지**에 따라 달라질 수 있습니다. Source를 보고 테스트를 찾는 일이 대부분이라면 source alignment가 강한 구조가 유리하고, 사용자 behavior나 integration boundary에서 테스트를 찾는 일이 많다면 그 축을 앞에 두는 편이 자연스러울 수 있습니다.

Literal mirroring은 source와 test의 natural boundary가 비슷할 때 특히 잘 맞습니다. 하나의 public behavior가 여러 module을 가로지르거나, integration·e2e·compatibility·migration처럼 system 관계가 중심이거나, source refactoring보다 behavior boundary가 안정적인 경우에는 다른 alignment가 더 읽기 쉬울 수 있습니다.

## Bundle Heuristics

Bundle이 유용해지는 시점에는 보편적인 threshold가 없습니다. 다만 **관련 group의 크기**와 **같은 directory 전체의 file density**는 structure를 다시 볼 때 쓸 수 있는 간단한 heuristic입니다.

하나의 실용적인 제안은 다음 범위부터 bundle을 함께 비교해 보는 것입니다.

| Signal | Bundle을 함께 비교해 볼 만한 구간 |
| --- | --- |
| 같은 prefix나 주제를 공유하는 관련 test files | 대략 **4~6개부터** |
| 같은 directory에서 함께 훑게 되는 files | 대략 **8~12개부터** |

이 범위는 framework standard나 전환 규칙이 아닙니다. Directory 한 단계를 추가하는 비용보다 grouping에서 얻는 탐색 이점이 커지기 시작하는 **관찰 지점**에 가깝습니다.

예를 들어 `test_invoice_*`가 4~6개 정도 반복되면 `invoice/`라는 directory가 prefix를 구조로 압축하는 데 도움이 될 수 있습니다. 반대로 같은 prefix를 가진 파일이 3개뿐이어도 해당 group만 사용하는 fixture나 snapshot이 많다면 bundle이 자연스러울 수 있습니다.

Directory 전체의 밀도도 함께 볼 수 있습니다. 관련 파일이 3~4개뿐이어도 같은 directory에서 서로 다른 주제의 파일을 10개 안팎 함께 훑어야 한다면, 작은 group을 bundle로 분리하는 것만으로 scan 범위가 줄어들 수 있습니다. 반대로 관련 파일이 6개 정도여도 directory 전체가 그 group 하나뿐이고 filename만으로 쉽게 훑어진다면 sibling files가 더 단순할 수 있습니다.

그 밖에 bundle이 유용해질 수 있는 흔한 신호는 다음과 같습니다.

- filename에서 같은 긴 prefix가 반복됩니다.
- 서로 다른 behavior나 scenario가 늘어 관련 테스트를 한눈에 찾기 어려워집니다.
- 특정 group만 사용하는 fixture, helper, fixture data 또는 snapshot이 생깁니다.
- group 자체를 자주 함께 탐색하거나 review합니다.
- 한 directory에 여러 unrelated test group이 섞여 scan 범위가 커집니다.

숫자와 신호는 결정을 대신하기보다 **구조를 한 번 다시 볼 이유**를 제공하는 정도로 사용하는 것이 이 패턴의 의도에 가깝습니다.

## Variants

### Colocated tests

Source 옆에 테스트를 두는 ecosystem에서는 별도의 mirrored `tests/` tree 없이 같은 아이디어를 사용할 수 있습니다.

```text
billing/
├─ invoice.ts
└─ invoice.test.ts
```

Test가 커지면 sibling test files, local bundle 또는 framework가 자연스럽게 지원하는 다른 분할 형태를 사용할 수 있습니다.

### Flat tests

작은 repository에서는 flat `tests/`가 가장 단순할 수 있습니다.

```text
tests/
├─ test_invoice.py
├─ test_tax.py
└─ test_checkout.py
```

Source hierarchy가 얕고 이름 충돌이나 navigation 문제가 없다면 directory mirroring을 추가하는 편익도 작습니다.

### Test-type-first

Integration, e2e, compatibility처럼 실행 방식과 boundary가 source grouping보다 중요한 suite는 test type을 첫 번째 축으로 둘 수 있습니다.

```text
tests/
├─ unit/
├─ integration/
└─ e2e/
```

필요하면 각 영역 안에서 다시 domain이나 source structure를 반영할 수 있습니다.

## Trade-offs

Source mirroring은 탐색 비용을 낮추지만 source rename이나 module 이동이 잦은 repository에서는 test path churn을 만들 수 있습니다. 반대로 behavior 중심 구조는 refactoring에는 안정적일 수 있지만 source에서 관련 test를 바로 찾기는 어려울 수 있습니다.

Sibling files는 directory depth를 늘리지 않는 대신 filename이 길어지고 같은 prefix가 반복될 수 있습니다. Bundle은 그 반복을 구조로 압축하고 local context를 모을 수 있지만 hierarchy 자체가 새로운 탐색 비용이 됩니다. 그래서 **single file → sibling files → bundle**은 흔한 growth path일 수 있지만, 순서나 전환 시점을 고정할 필요는 없습니다.

이 패턴은 test taxonomy, test pyramid, fixture architecture나 unit/integration의 의미를 정하는 패턴은 아닙니다. **어떤 테스트가 존재해야 하는가보다, 이미 존재하는 테스트를 filesystem에서 어떻게 찾기 쉽게 둘 것인가**에 초점을 둡니다.

## Ecosystem Fit

대표적인 ecosystem만 보아도 test layout에는 하나의 표준 형태가 없습니다.

- [pytest](https://docs.pytest.org/en/stable/explanation/goodpractices.html#tests-outside-application-code)는 application code 밖의 `tests/` layout을 지원합니다.
- [Go](https://pkg.go.dev/testing)는 package source와 같은 directory의 `*_test.go`를 기본적인 형태로 사용합니다.
- [Cargo](https://doc.rust-lang.org/cargo/reference/cargo-targets.html#tests)는 source 안의 unit test와 `tests/` 아래 integration test를 구분합니다.
- [Jest](https://jestjs.io/docs/configuration#testmatch-arraystring)는 `__tests__` directory와 `.test` / `.spec` suffix를 모두 기본 discovery 형태로 지원합니다.

따라서 source mirroring은 ecosystem convention을 대신하는 universal layout이라기보다, **허용되는 구조 안에서 source와 test 사이의 navigation 관계를 더 읽기 쉽게 만드는 선택지**로 보는 편이 적절합니다.

## Related Pattern

[Filesystem-Legible Structure](filesystem-legible-structure.md)는 repository의 naming, placement와 hierarchy를 navigation cue로 활용하는 더 일반적인 관점을 다룹니다.

## Short Form

> **Source와 test의 위치 관계는 관련 테스트를 찾는 탐색 단서가 될 수 있습니다. 작은 테스트는 단일 파일이나 sibling files로 표현할 수 있고, 관련 파일이나 directory가 조밀해지면 bundle이 탐색을 더 단순하게 만드는 선택지가 될 수 있습니다. Literal mirroring보다 feature·behavior·system boundary가 더 자연스러운 경우도 있습니다.**

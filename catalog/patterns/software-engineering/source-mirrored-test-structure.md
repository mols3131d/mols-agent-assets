---
description: source와 test의 대응 관계를 navigation cue로 활용하고, test surface가 커질 때 sibling files나 bundle 같은 구조를 선택할 때 참고하는 패턴입니다.
---

# Source-Mirrored Test Structure

Production source와 test structure가 어느 정도 대응되면 **source를 찾은 뒤 관련 테스트의 위치를 예측하기 쉬워집니다.** 특히 `tests/`처럼 production code와 test tree가 분리된 repository에서 유용한 navigation pattern입니다.

핵심은 source tree를 정확히 복제하는 것이 아니라 **source와 test 사이에 예측 가능한 대응 관계를 만드는 것**입니다. Source path는 좋은 탐색 단서 중 하나이며, feature·behavior·system boundary가 더 자연스러운 경우에는 그 경계를 기준으로 조직할 수도 있습니다.

## Core

자연스러운 source anchor가 분명할 때 source와 가까운 test structure는 가장 단순한 형태 중 하나입니다.

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

`src/billing/invoice.py`를 본 사람은 `tests/billing/test_invoice.py`를 먼저 찾아볼 수 있습니다. `src/` 같은 상위 prefix를 생략하거나 framework convention에 맞춰 이름을 바꾸더라도 대응 관계는 유지될 수 있습니다.

이 구조는 source architecture나 test design을 새로 정의하지 않습니다. **이미 존재하는 구조를 navigation cue로 재사용하는 것**에 가깝습니다.

## Typical Forms

### File-to-file

테스트 범위가 작고 하나의 파일에서 충분히 읽히는 경우입니다.

```text
src/orders/service.py
          ↓
tests/orders/test_service.py
```

### File-to-sibling-files

하나의 test file이 여러 behavior나 scenario를 담게 되면 같은 directory의 sibling files로 나눌 수 있습니다.

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

Source와의 대응을 filename에 남기면서 새로운 directory depth를 만들지 않는 형태입니다. 같은 prefix가 반복되거나 directory가 조밀해지면 별도 bundle과 비교해 봅니다.

### Files-to-bundle

같은 production unit이나 behavior에 속하는 test files가 하나의 독립적인 탐색 영역처럼 보이기 시작하면 directory bundle로 묶을 수 있습니다.

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

Bundle은 반복되는 grouping을 directory 이름으로 압축하고 관련 fixture·data·snapshot·helper 같은 local context를 가까이 둘 수 있습니다. 내부 파일은 source의 private implementation보다 behavior, scenario, contract처럼 테스트를 읽고 변경할 때 의미 있는 경계로 나누는 것을 고려합니다.

### Boundary-to-bundle

여러 source unit이 하나의 안정적인 behavior를 만든다면 literal source path 대신 그 behavior를 grouping boundary로 사용할 수 있습니다.

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

`checkout/`은 source directory를 그대로 복제하지 않지만 테스트가 다루는 경계를 더 잘 보여줄 수 있습니다.

## Choosing the Alignment

Source path가 항상 가장 좋은 organizing axis는 아닙니다. 테스트를 찾을 때 가장 먼저 알고 있는 정보와 테스트가 다루는 안정적인 경계에 따라 다른 축을 사용할 수 있습니다.

| Alignment | 잘 맞는 경우 | Example |
| --- | --- | --- |
| Source unit | 한 module/file이 자연스러운 anchor | `tests/billing/test_invoice.py` |
| Feature / domain | 여러 module이 하나의 기능 경계를 형성 | `tests/billing/checkout/` |
| Behavior / contract | 내부 구조보다 외부 동작이 더 안정적 | `tests/api/authentication/` |
| Test / system boundary | integration·e2e·compatibility처럼 여러 영역을 함께 검증 | `tests/integration/`, `tests/e2e/` |

이 축들은 조합할 수도 있습니다. 예를 들어 `tests/integration/billing/`처럼 test level과 domain을 함께 드러낼 수 있습니다.

Literal mirroring은 source와 test의 natural boundary가 비슷할 때 특히 잘 맞습니다. 하나의 behavior가 여러 module을 가로지르거나 source refactoring보다 behavior boundary가 안정적이라면 **feature·behavior·system boundary 중심의 alignment를 고려합니다.**

## Bundle Heuristics

Bundle 전환에는 보편적인 threshold가 없습니다. 다만 **관련 group의 크기**와 **같은 directory에서 함께 훑게 되는 file density**는 구조를 다시 비교할 때 유용한 신호가 될 수 있습니다.

이 패턴에서 제안하는 실용적인 참고 범위는 다음과 같습니다.

| Signal | Bundle을 함께 비교해 볼 만한 구간 |
| --- | --- |
| 같은 prefix나 주제를 공유하는 관련 test files | 대략 **4~6개 정도가 되면** |
| 같은 directory에서 함께 훑게 되는 files | 대략 **8~12개 정도가 되면** |

이 숫자는 framework standard나 전환 규칙이 아니라 **관찰 지점**입니다. Directory 한 단계를 추가하는 비용보다 grouping에서 얻는 탐색 이점이 커지는지 다시 볼 시점을 제안합니다.

- 같은 긴 filename prefix가 반복되면 **그 prefix를 directory 이름으로 압축할지 고려합니다.**
- 한 directory에서 여러 unrelated test group을 함께 훑어야 한다면 **독립적인 group을 bundle로 분리할지 고려합니다.**
- 특정 group만 사용하는 fixture, helper, data 또는 snapshot이 생기면 **그 local context를 group 가까이에 모으는 구조를 고려합니다.**
- bundle을 만들어도 파일이 쉽게 구분되지 않거나 navigation step만 늘어난다면 **sibling files를 유지합니다.**

예를 들어 `test_invoice_*`가 4~6개 정도 반복되면 `invoice/`가 prefix를 구조로 압축하는 데 도움이 될 수 있습니다. 반대로 관련 파일이 6개여도 directory 전체가 그 group 하나뿐이고 쉽게 훑어진다면 sibling files가 더 단순할 수 있습니다.

관련 파일이 3~4개뿐이어도 같은 directory에 서로 다른 주제의 파일이 10개 안팎 섞여 있거나, 그 group만 쓰는 fixture·snapshot·helper가 많다면 bundle이 scan 범위를 줄이고 local context를 가까이 모으는 데 도움이 될 수 있습니다.

## Variants

### Colocated tests

Source 옆에 테스트를 두는 ecosystem에서는 별도의 mirrored `tests/` tree 없이 같은 아이디어를 적용할 수 있습니다.

```text
billing/
├─ invoice.ts
└─ invoice.test.ts
```

### Flat tests

Source hierarchy가 얕고 이름 충돌이나 navigation 문제가 작은 repository에서는 flat `tests/`가 더 단순할 수 있습니다.

```text
tests/
├─ test_invoice.py
├─ test_tax.py
└─ test_checkout.py
```

### Test-type-first

Integration, e2e, compatibility처럼 실행 방식과 system boundary가 source grouping보다 중요한 suite는 test type을 첫 번째 축으로 둘 수 있습니다.

```text
tests/
├─ unit/
├─ integration/
└─ e2e/
```

필요하면 각 영역 안에서 다시 domain이나 source structure를 반영할 수 있습니다.

## Trade-offs and Responses

| Form | Strength | Limitation | Possible response |
| --- | --- | --- | --- |
| Source mirroring | source에서 관련 test를 빠르게 추측하기 쉬움 | source rename·move가 잦으면 test path churn이 생길 수 있음 | 더 안정적인 feature·behavior·domain boundary를 고려함 |
| Sibling files | directory depth를 늘리지 않음 | filename이 길어지고 prefix가 반복될 수 있음 | 반복 group이 뚜렷해지면 bundle과 비교함 |
| Bundle | grouping과 local context를 구조로 드러냄 | hierarchy와 navigation step이 늘어남 | 작은 group이거나 scan이 쉬우면 siblings를 유지함 |
| Behavior-oriented grouping | refactoring에도 test boundary가 안정적일 수 있음 | source에서 관련 test를 바로 찾기는 어려울 수 있음 | source navigation이 중요한 영역은 source alignment를 유지함 |

`single file → sibling files → bundle`은 흔한 growth path일 수 있지만 모든 단계를 거치거나 특정 개수에서 자동으로 전환할 필요는 없습니다.

## Limits

이 패턴의 이점은 filesystem이 실제 navigation에 얼마나 중요한지와 source tree가 얼마나 좋은 탐색 단서를 제공하는지에 따라 달라집니다.

Source tree가 테스트의 자연스러운 경계를 잘 보여주지 못한다면 앞의 alternate alignment가 더 적합할 수 있습니다. 그 밖에는 다음 환경 조건을 함께 봅니다.

- IDE search, symbol navigation, test runner filtering처럼 더 빠른 탐색 수단이 이미 충분하다면 **filesystem hierarchy를 추가하는 이점이 실제로 있는지 먼저 비교합니다.**
- Framework나 language의 test discovery·import convention과 충돌한다면 **ecosystem convention을 우선합니다.**

이 패턴은 test taxonomy, test pyramid, fixture architecture나 unit/integration의 의미를 정하지 않습니다. **어떤 테스트가 존재해야 하는가보다, 이미 존재하는 테스트를 filesystem에서 어떻게 찾기 쉽게 둘 것인가**에 초점을 둡니다.

## Ecosystem Fit

Test layout에는 하나의 보편적인 형태가 없습니다.

- [pytest](https://docs.pytest.org/en/stable/explanation/goodpractices.html#tests-outside-application-code)는 application code 밖의 `tests/` layout을 지원합니다.
- [Go](https://pkg.go.dev/testing)는 package source와 같은 directory의 `*_test.go`를 기본 형태로 사용합니다.
- [Cargo](https://doc.rust-lang.org/cargo/reference/cargo-targets.html#tests)는 source 안의 unit test와 `tests/` 아래 integration test를 구분합니다.
- [Jest](https://jestjs.io/docs/configuration#testmatch-arraystring)는 `__tests__` directory와 `.test` / `.spec` suffix를 모두 기본 discovery 형태로 지원합니다.

Framework의 discovery·import 규칙은 naming이나 nesting에 영향을 줄 수 있습니다. 실제 layout에서는 해당 ecosystem의 convention을 우선하고, 그 안에서 source/test navigation을 더 읽기 쉽게 만들 수 있는지 봅니다.

## Related Pattern

[Filesystem-Legible Structure](filesystem-legible-structure.md)는 repository의 naming, placement와 hierarchy를 navigation cue로 활용하는 더 일반적인 관점을 다룹니다.

## Short Form

> **Source와 test의 위치 관계를 탐색 단서로 활용할 수 있습니다. 작은 테스트는 단일 파일이나 sibling files로 두고, 관련 파일이나 directory가 조밀해지면 bundle을 비교합니다. Literal mirroring이 실제 boundary와 맞지 않으면 feature·behavior·system boundary를 고려하고, framework convention과 충돌하면 ecosystem convention을 우선합니다.**

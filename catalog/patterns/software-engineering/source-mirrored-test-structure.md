---
description: 분리된 test tree를 source code 경로와 대응시켜 테스트 위치를 예측 가능하게 하고, 단일 테스트 파일이 커질 때 대응 bundle로 확장할지 판단할 때 참고하는 패턴입니다.
---

# Source-Mirrored Test Structure

`tests/`처럼 production source와 분리된 test tree를 사용할 때 **source의 경로와 책임 경계를 가능한 범위에서 mirror**해 관련 테스트의 위치를 예측 가능하게 만듭니다.

목표는 source와 test를 기계적으로 1:1 대응시키는 것이 아닙니다. Source를 찾은 사람이 관련 테스트를 어디에서 찾아야 하는지 빠르게 추측할 수 있고, test tree만 보아도 어느 production 영역을 검증하는지 큰 윤곽을 파악할 수 있으면 충분합니다.

이 패턴은 [`Filesystem-Legible Structure`](filesystem-legible-structure.md)를 test/source navigation에 적용한 구체적인 형태입니다.

## Core

분리된 test tree에서는 **자연스러운 production owner가 있는 테스트를 그 owner의 source path와 대응되는 위치에 둡니다.** `src/`, package root처럼 test tree에서 의미 없는 상위 prefix는 생략하거나 해당 ecosystem의 일반 layout에 맞게 정규화할 수 있습니다.

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

이 예에서 `src/billing/invoice.py`의 주요 테스트는 `tests/billing/test_invoice.py`에서 찾을 수 있습니다. Filename 자체보다 중요한 것은 **source path와 test path 사이의 대응 관계가 명확하고 반복 가능하다는 점**입니다.

Test layout은 source architecture를 새로 정의하지 않습니다. 이미 선택된 source structure를 탐색 단서로 재사용하는 것이 핵심입니다. Path가 대응된다는 사실도 white-box test나 implementation detail 중심의 assertion을 요구하지 않습니다.

## Grow from File to Bundle

하나의 source unit에 대한 테스트가 작을 때는 **하나의 test file에서 시작**하는 편이 단순합니다.

테스트가 늘어나 한 파일에서 서로 다른 behavior와 scenario를 탐색하기 어려워지면, 같은 대응 위치를 유지한 채 **test bundle directory로 확장**할 수 있습니다. 보통 bundle은 기존 단일 test file을 대체합니다.

```text
src/
└─ billing/
   └─ invoice.py

tests/
└─ billing/
   └─ invoice/
      ├─ test_create.py
      ├─ test_adjust.py
      └─ test_failures.py
```

Bundle 내부는 source의 private function이나 현재 구현 순서를 그대로 복제하기보다 **behavior, scenario, contract처럼 테스트를 읽고 변경하는 데 유용한 경계**로 나눕니다.

고정된 line count나 test case 수를 split 기준으로 두지 않습니다. 다음과 같은 마찰이 반복될 때 bundle 전환을 고려합니다.

- 서로 다른 behavior가 한 파일 안에서 섞여 필요한 테스트를 찾기 어렵습니다.
- 파일이 커져 review와 변경 범위를 빠르게 파악하기 어렵습니다.
- 독립적인 test concern이 반복해서 같은 파일을 수정해 충돌이 커집니다.
- local fixture나 helper가 특정 concern에만 속하는데 한 파일의 공용 영역에 쌓입니다.
- 파일을 나누면 test ownership과 navigation이 더 분명해집니다.

단순히 파일이 길다는 이유만으로 분리하지 않습니다. 여러 파일로 나눈 뒤에도 어떤 테스트가 어디에 있는지 더 예측하기 어렵다면 bundle은 개선이 아닙니다.

## When Mirroring Does Not Fit

Mirroring이 자연스럽지 않으면 **억지로 source file 하나를 고르지 않고 테스트의 가장 안정적인 owner를 찾습니다.**

보통 다음 순서로 판단할 수 있습니다.

1. 하나의 source file이나 module이 자연스러운 owner면 그 경계를 mirror합니다.
1. 그렇지 않지만 하나의 package, component, feature 또는 domain이 자연스러운 owner면 그 **상위 production boundary**에 대응시킵니다.
1. 여러 production boundary를 의도적으로 함께 검증한다면 source path 대신 **behavior 또는 test concern 자체**를 owner로 둡니다.
1. repository 전체나 외부 system과의 관계를 검증한다면 `integration`, `e2e`, `contract`, `migration`처럼 **test level이나 system boundary**가 owner가 될 수 있습니다.

예를 들어 결제 흐름이 여러 module을 가로질러 하나의 사용자-visible behavior를 만든다면 다음처럼 둘 수 있습니다.

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
      ├─ test_success.py
      └─ test_failures.py
```

`checkout/`은 source directory를 문자 그대로 mirror하지 않지만, 테스트가 실제로 소유하는 **stable behavior boundary**를 드러냅니다.

더 넓은 integration test라면 다음처럼 source mirroring 축에서 분리할 수 있습니다.

```text
tests/
├─ billing/
│  └─ test_invoice.py
├─ integration/
│  └─ test_billing_database.py
└─ e2e/
   └─ test_checkout.py
```

핵심은 모든 테스트를 같은 축으로 정렬하는 것이 아니라 **각 테스트를 어디에서 찾을지 예측할 수 있는 일관된 owner를 갖게 하는 것**입니다. `misc/`, `others/`, `common/`처럼 의미가 약한 catch-all은 마지막 수단으로도 만들지 않는 편이 좋습니다. 그런 directory가 커진다면 아직 적절한 owner를 찾지 못했다는 신호로 봅니다.

## Variants

Mirroring은 **exact filename schema가 아니라 대응 원칙**입니다. Language, framework와 test runner의 convention을 우선합니다.

예를 들어 `invoice.py`에 대한 bundle은 환경에 따라 `invoice/`, `test_invoice/`, `invoice_tests/`처럼 표현할 수 있습니다. 중요한 것은 repository 안에서 source와 test 사이의 대응을 쉽게 복원할 수 있고 test discovery와 tooling을 방해하지 않는 것입니다.

Test를 source 옆에 colocate하는 ecosystem이라면 별도의 `tests/` tree를 만들 필요가 없습니다. 작은 테스트는 sibling file로 두고, 커지면 같은 local boundary의 bundle로 확장하는 식으로 같은 원칙을 적용할 수 있습니다.

```text
# file form
billing/
├─ invoice.ts
└─ invoice.test.ts

# bundle form
billing/
├─ invoice.ts
└─ invoice.test/
   ├─ create.test.ts
   └─ failures.test.ts
```

작은 repository에서는 flat test layout이 더 단순할 수 있습니다. Source hierarchy가 얕고 이름 충돌이나 navigation 문제가 없다면 mirroring을 위해 불필요한 directory를 추가하지 않습니다.

## Tests That Should Not Mirror a Single Source File

모든 테스트가 하나의 source file이나 module에 자연스럽게 귀속되는 것은 아닙니다. **여러 production boundary를 함께 검증하는 테스트까지 억지로 하나의 source path에 배치하지 않습니다.**

대표적으로 다음은 자기 목적에 맞는 별도 구조가 더 자연스러울 수 있습니다.

- integration test
- end-to-end test
- contract 또는 compatibility test
- migration과 system-level regression test
- 여러 test area가 공유하는 fixture, factory와 test support code

이런 테스트는 `tests/integration/`, `tests/e2e/`처럼 test concern 자체를 owner로 삼을 수 있습니다. 특정 feature나 domain이 명확한 owner라면 그 경계를 기준으로 다시 묶을 수도 있습니다.

Public behavior를 검증하는 테스트가 여러 내부 module을 의도적으로 가로지른다면 현재 implementation file보다 **stable behavior boundary**를 따라가는 편이 refactoring에 더 강할 수 있습니다.

## Guardrails

**Mirroring은 navigation aid이지 source와 test 사이의 강한 coupling contract가 아닙니다.**

- Source 내부 구현이 바뀔 때마다 test tree를 기계적으로 재배열하지 않습니다.
- Test organization을 맞추기 위해 production structure를 왜곡하지 않습니다.
- Framework, language, generated code와 test runner가 소유하는 유효한 convention을 우선합니다.
- One source file = one test file 규칙을 강제하지 않습니다.
- 하나의 test가 여러 owner에 걸친다는 이유로 같은 test logic을 여러 위치에 복제하지 않습니다.
- Mirrored path가 실제 test intent를 숨기기 시작하면 behavior, feature 또는 system boundary처럼 더 적절한 owner를 선택합니다.

Source rename이나 move가 test의 natural owner도 함께 바꾼다면 mirrored test path를 같이 갱신하는 것이 탐색성에 도움이 됩니다. 반대로 source의 일시적인 내부 재배치에 불과하고 test의 conceptual owner가 그대로라면 strict mirror를 유지하기 위한 churn은 만들지 않습니다.

## Short Form

> **분리된 test tree는 source structure를 따라 관련 테스트의 위치를 예측 가능하게 두고, 한 test file이 감당하기 어려워지면 같은 대응 경계에서 bundle로 확장합니다. Mirroring이 자연스럽지 않으면 더 안정적인 feature, behavior 또는 system boundary를 owner로 선택합니다.**

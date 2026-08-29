# Code Comprehension Skill Split Plan

이 계획은 [Comprehension Cost Research](clarify-code-comprehension-cost-research.md)를 바탕으로, 기존 `clarify-code` 하나에 코드 리팩터링과 code-adjacent explanation을 함께 맡기지 않고 **두 개의 명확한 capability로 분리**하는 구현 계획입니다.

## Decision

### `code-comprehension-refactor`

코드의 작동, observable behavior, caller-visible contract와 material performance characteristic을 보존하면서 **실행 코드 자체의 이해 비용을 줄이는 behavior-preserving refactoring skill**로 신설합니다.

주요 대상:

- opaque representation과 hidden convention
- positional/boolean/sentinel decoding
- difficult control flow와 state/temporal reasoning
- semantic gain 없는 indirection
- abstraction mismatch
- mixed responsibility와 abstraction level
- code size는 작지만 mental reconstruction이 큰 표현

### `clarify-code`

실행 코드를 바꾸지 않고 **code file 안에서 함께 유지되는 docstring, comment, module-level explanation으로 이해를 돕는 skill**로 좁힙니다.

주요 대상:

- caller가 알아야 하는 비자명한 contract
- maintainer가 알아야 하는 rationale, invariant, ordering reason
- 외부 constraint나 의도적인 구현 선택의 이유
- module-local convention 중 code만으로 복원하기 어려운 의미

코드 구조 자체가 문제이면 comment를 추가하지 않고 `code-comprehension-refactor`로 넘깁니다.

## Why Split

기존 `clarify-code`는 다음 두 intervention을 동시에 소유했습니다.

1. naming, control flow, extraction, indirection 같은 **executable code refactor**
1. docstring, comment 같은 **explanatory prose change**

둘은 목적은 같지만 mutation surface와 validation contract가 다릅니다.

- code refactor는 behavior, contract, state, side effect와 performance 보존을 검증해야 합니다.
- explanation change는 실행 코드를 건드리지 않는 것이 기본이며, stale prose와 machine-consumed comment/docstring을 구분해야 합니다.

분리하면 routing과 stop condition이 더 직접적이고, prose로 structural problem을 덮거나 documentation request에서 불필요한 refactor를 시작하는 실패를 줄일 수 있습니다.

## Responsibility Boundary

| Situation | Owner |
| --- | --- |
| 이름, representation, flow, state, indirection, abstraction 때문에 이해하기 어렵다 | `code-comprehension-refactor` |
| code는 적절하지만 caller contract가 docstring에 필요하다 | `clarify-code` |
| code는 적절하지만 maintainer가 ordering/invariant 이유를 알아야 한다 | `clarify-code` |
| comment를 추가하려 했지만 실제 문제는 positional tuple과 boolean convention이다 | `code-comprehension-refactor` |
| refactor 후 기존 comment/docstring이 stale해진다 | code change는 `code-comprehension-refactor`, 필요한 explanation 동기화는 `clarify-code` |
| feature, correctness fix, performance optimization, public API redesign, architecture redesign | 둘 다 아님 |

## `code-comprehension-refactor` Design

### Core model

이해 비용은 line count가 아니라 reader가 mental model을 만들기 위해 수행하는 추가 작업으로 봅니다.

```text
comprehension cost
├─ misunderstanding risk
└─ reconstruction effort
```

`reconstruction effort`에는 의미 번역, 다른 symbol/file 탐색, positional/flag convention 복원, control-flow simulation, state tracking과 abstraction translation이 포함될 수 있습니다.

### Preserve envelope

Refactor 전후 다음 중 task에 실제로 관련된 surface를 보존합니다.

- observable output과 return shape
- exception type와 trigger semantics
- state mutation과 persistence
- side effect와 ordering
- import, registration, framework entrypoint
- caller-visible contract
- material performance characteristic

성능을 개선하는 것이 목적은 아닙니다. 다만 hot path, allocation, I/O/query count, algorithmic complexity처럼 중요한 성능 특성을 readability 때문에 악화시키지 않습니다.

### Package

```text
src/rulesync/.rulesync/skills/code-comprehension-refactor/
├── SKILL.md
└── references/
    ├── diagnosis.md
    ├── interventions.md
    └── validation.md
```

- `diagnosis.md`: comprehension bottleneck과 abstraction value 판단
- `interventions.md`: bottleneck을 줄이는 최소 code transformation과 counterexample
- `validation.md`: behavior, contract, state, side effect, performance preservation

## `clarify-code` Design

### Mutation boundary

다음은 변경하지 않습니다.

- executable statement
- identifier
- type와 signature
- data representation
- control/state flow
- abstraction

다음 code-adjacent prose만 다룹니다.

- docstring
- ordinary explanatory comment
- module-level source explanation

### Documentation rules

- caller가 사용 전에 알아야 하는 hidden contract → docstring
- maintainer가 수정할 때 알아야 하는 code-local reason → comment
- code가 이미 표현하는 `what`을 prose로 반복하지 않음
- architecture/domain policy를 source prose에 복제하지 않고 필요한 부분만 projection
- code structure 문제를 comment로 설명하지 않음

### Machine-consumed text

다음은 inert prose로 보지 않습니다.

- `noqa`, `type: ignore`, coverage/formatter/linter directive
- shebang, encoding cookie
- doctest와 expected output
- reflection/framework가 읽는 docstring
- tooling이 parse하는 structured comment

이 surface는 tooling이나 observable contract가 될 수 있으므로 consumer와 validation을 확인합니다.

### Package

```text
src/rulesync/.rulesync/skills/clarify-code/
├── SKILL.md
└── references/
    └── documentation.md
```

기존 `diagnosis.md`와 `validation.md`의 code-refactor 책임은 신규 skill로 이동하고 `clarify-code`에서는 제거합니다.

## Capability Evals

### `evals/skills/code-comprehension-refactor/cases.json`

Positive와 near-miss를 함께 둡니다.

- compact positional contract
- boolean/sentinel config
- meaningless wrapper chain
- control/state reasoning
- performance-sensitive hot path
- valuable domain abstraction 보존
- already-clear compact code는 no-op 가능
- comment-only request는 `clarify-code`로 route
- architecture redesign은 scope 밖

### `evals/skills/clarify-code/cases.json`

- caller contract docstring
- maintainer rationale comment
- module-local explanation
- structural code problem은 신규 skill로 route
- obvious line-by-line comment는 추가하지 않음
- machine-consumed directive는 ordinary prose로 수정하지 않음
- runtime/tool-consumed docstring은 contract를 보존

초기 fixture는 capability eval입니다. 실제 model/runtime 반복 검증을 수행하기 전에는 regression pass를 주장하지 않습니다.

## Acceptance Criteria

### Routing

- executable code transformation이 필요하면 `code-comprehension-refactor`
- code는 유지하고 source-level explanation만 필요하면 `clarify-code`
- 두 skill이 같은 mutation authority를 소유하지 않음

### `code-comprehension-refactor`

- 짧지만 decoding-heavy한 code를 이해 비용으로 인식
- line count나 abstraction 수를 proxy로 사용하지 않음
- valuable domain abstraction을 보존
- smallest change를 smallest diff가 아니라 smallest coherent conceptual change로 판단
- behavior, caller contract와 material performance를 보존

### `clarify-code`

- executable code를 변경하지 않음
- docstring과 comment reader를 구분
- code를 그대로 번역하는 comment를 만들지 않음
- structural opacity를 prose로 덮지 않음
- machine-consumed source text의 semantics를 보존

## Validation and Generated Artifacts

Canonical source 변경 후 repository-native 환경에서는 다음을 수행합니다.

1. `mise run generated-sync`
1. `mise run format-changed`
1. 필요하면 `mise exec -- npm run rulesync:doctor`
1. `mise run check`
1. `mise run test`
1. capability fixture를 실제 model/runtime에서 실행했다면 그 결과를 별도로 기록

`route/*.jsonl`, `.agents/route/*.jsonl` 같은 generated projection은 직접 편집하지 않습니다.

GitHub connector만으로 작업한 경우 실행하지 않은 generator, test, benchmark 또는 eval을 통과했다고 보고하지 않습니다.

## Review Focus

최종 리뷰에서는 특히 다음 반례를 봅니다.

- `clarify-code`가 다시 executable refactor를 시작하는가?
- `code-comprehension-refactor`가 comment/docstring으로 구조 문제를 덮는가?
- compact code를 무조건 verbose하게 만드는가?
- abstraction을 hop count만으로 제거하는가?
- performance-sensitive code를 근거 없이 더 느린 구조로 바꾸는가?
- source directive나 doctest를 ordinary prose로 취급하는가?

새 P1/P2가 없고 두 skill의 authority가 명확하면 구현 구조는 수렴한 것으로 봅니다.

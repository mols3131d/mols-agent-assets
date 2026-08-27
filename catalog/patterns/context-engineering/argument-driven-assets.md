---
description: 같은 Agent Asset core를 runtime·target·사용 목적별로 복제하지 않고 argument로 behavior와 conditional context를 선택하게 설계할 때 참고하는 pattern으로, argument contract와 progressive disclosure의 경계를 다룹니다.
---

# Argument-Driven Assets

재사용 가능한 asset의 변형 가능한 행동을 작은 **argument surface**로 노출하고, 선택된 argument 값에 필요한 behavior와 context만 적용하는 패턴입니다.

Argument는 asset을 target별 variant로 복제하지 않고도 compatibility와 flexibility를 높일 수 있습니다. Argument 값을 context routing key로 사용하면 progressive disclosure와 결합해 불필요한 context load도 줄일 수 있습니다.

## Purpose

같은 core를 유지하면서 runtime, target, 사용 목적이나 원하는 강도에 따라 행동을 조정해야 할 때 argument가 명시적인 extension point가 될 수 있습니다.

특히 다음과 같은 경우에 유용합니다.

- 하나의 asset이 여러 runtime이나 project에서 조금씩 다른 동작을 지원해야 할 때
- 사용자가 verbosity, depth, mode, strategy 같은 선택을 직접 지정할 수 있어야 할 때
- 생략 시 안정적인 기본값이 필요하거나 현재 context에서 값을 추론할 수 있을 때
- 특정 선택에서만 필요한 instruction, reference 또는 example이 클 때
- variant를 별도 asset으로 복제하는 것보다 작은 parameterized core가 더 단순할 때

## Core

- 공통 invariant와 필수 behavior는 argument와 관계없이 유지합니다.
- 실제 결과를 의미 있게 바꾸는 선택만 argument로 노출합니다.
- Argument는 behavior와 context selection을 조정하지만 새로운 authority를 부여하지 않습니다.
- 생략 또는 동적 결정이 필요한 argument에는 `default`, `auto` 또는 명시적인 omission behavior를 둘 수 있습니다.
- Argument 값에 따라 필요한 conditional context만 load하거나 append할 수 있습니다.
- 값별 detail을 분리하더라도 어떤 argument가 어떤 context를 요구하는지는 core에서 발견 가능해야 합니다.

목표는 option 수를 늘리는 것이 아니라 **하나의 reusable core를 필요한 만큼만 변형하고 공개하는 것**입니다.

## Argument Contract

Argument마다 최소한 다음 의미를 복원할 수 있어야 합니다.

- argument 이름과 책임
- 의미 있는 explicit 값 또는 값의 형태
- 생략했을 때의 resolution
- `auto` 또는 `default`가 있다면 그 의미
- 값이 behavior나 추가 context에 미치는 영향

Structured argument surface를 지원한다면 짧은 `hint` field 또는 target-native 동등 표현을 함께 두는 것을 권장합니다. Hint는 사용 가능한 값과 선택 의미를 빠르게 알려주는 discovery signal이며 상세한 argument documentation을 복제하지 않습니다.

```yaml
arguments:
  intensity:
    value: <default>
    hint: "default | auto | lite | full | ultra"
```

이 shape와 `hint`라는 field name은 예시일 뿐 universal schema가 아닙니다. Structured field를 지원하지 않는 환경에서는 inline comment, table, invocation help 같은 더 자연스러운 형태를 사용할 수 있습니다.

## `default` and `auto`

`default`와 `auto`는 같은 의미로 취급하지 않는 편이 좋습니다.

- **`default`** — asset이 정의한 안정적인 기본 behavior를 선택합니다.
- **`auto`** — caller intent, target state, runtime capability 또는 다른 관찰 가능한 evidence에서 현재 값을 동적으로 해석합니다.
- **explicit value** — higher authority나 invariant와 충돌하지 않는 한 해당 선택을 직접 사용합니다.

```text
explicit concrete value → use it
explicit auto           → infer from relevant evidence
explicit default        → use asset-defined default
omitted                 → use declared omission behavior
```

생략 시 `default`를 사용할지 `auto`처럼 resolve할지는 asset이 명시합니다. 둘을 암묵적으로 같은 동작으로 만들지 않습니다.

여러 argument가 `auto`를 지원한다면 각 argument는 자기 책임 안에서 독립적으로 resolve하는 편이 좋습니다. 한 argument의 추론 결과가 다른 argument나 side effect를 묵시적으로 승인해서는 안 됩니다.

## Argument-Gated Progressive Disclosure

Argument 값은 behavior selector이면서 **conditional context의 routing key**가 될 수 있습니다. Core에는 모든 variant detail을 넣지 않고, 값을 먼저 결정한 뒤 그 값에 필요한 context만 공개합니다.

```text
core + argument contract
        ↓
resolve argument value
        ↓
load matching conditional context
        ↓
apply selected behavior
```

Conditional context는 별도 reference file, section, template, example, rule fragment 또는 runtime이 지원하는 다른 lazy-loading surface에 둘 수 있습니다. 파일을 나누는 것 자체가 목적은 아니며 실제 context 절약이나 유지보수 이점이 있을 때 사용합니다.

### Selective form

각 값이 독립적인 variant라면 선택된 값의 detail만 load할 수 있습니다.

```text
mode = a → core + a
mode = b → core + b
mode = c → core + c
```

### Cumulative form

값이 **점진적으로 강화되는 level**이라면 낮은 level을 base로 두고 높은 level의 delta를 순서대로 append할 수 있습니다.

예를 들어 `lite | full | ultra`가 있을 때:

```text
lite  → lite
full  → lite + full delta
ultra → lite + full delta + ultra delta
```

`lite`가 작고 공통적인 base라면 core에 바로 공개해 routing 단계를 생략할 수도 있습니다.

```text
core includes lite
full  → core/lite + full delta
ultra → core/lite + full delta + ultra delta
```

이 누적 append 방식은 progressive disclosure의 **한 구현 예시**입니다. 모든 argument를 ordered level로 취급하거나 높은 값이 낮은 값의 context를 반드시 상속해야 한다는 규칙은 아닙니다. 값 사이에 실제 의미적 포함 관계가 있을 때만 cumulative form을 사용합니다.

### Direct form

Argument별 detail이 작고 항상 읽어도 부담이 없다면 별도 routing 없이 core에 둘 수 있습니다. Progressive disclosure를 위해 불필요한 파일이나 단계를 만들지 않습니다.

## Resolution and Loading

가능하면 **argument resolution을 conditional context loading보다 먼저** 수행합니다. 그래야 아직 선택되지 않은 variant의 detail을 미리 읽지 않아도 됩니다.

실제 context 절감 효과는 harness의 retrieval granularity에 달려 있습니다. Asset body 전체가 이미 active context에 들어온 뒤 section만 논리적으로 선택하는 환경에서는 behavior는 분리할 수 있어도 이미 소비된 context token까지 줄이지는 못합니다. 큰 conditional detail만 별도 retrieval surface로 분리하는 편이 나을 수 있습니다.

Runtime이 이미 load한 context를 제거할 수 없을 수도 있습니다. 같은 session에서 `ultra → lite`처럼 낮은 level로 전환하더라도 이전 detail이 물리적으로 사라진다고 가정하지 않습니다. 현재 resolved argument가 어떤 behavior를 활성화하는지 명확히 유지하고, isolation이 중요하면 invocation/session boundary 또는 runtime-native scope를 사용합니다.

## Considerations

- Argument 하나가 실질적으로 별도 capability, permission 또는 lifecycle을 만든다면 parameterization보다 책임 분리가 더 명확할 수 있습니다.
- 서로 독립적인 내부 결정을 모두 public argument로 노출하면 asset이 mini-framework가 될 수 있습니다. Caller가 실제로 제어할 가치가 있는 선택만 공개합니다.
- `auto`는 convenience를 제공하지만 추론 근거와 owner가 불명확하면 숨은 behavior가 됩니다. 중요한 resolution은 observable evidence에 근거해야 합니다.
- `default`는 안정적인 public behavior인지 검토합니다.
- Hint는 discovery를 돕는 요약이지 별도의 authority가 아닙니다. 실제 semantics와 stale되지 않게 유지합니다.
- Cumulative disclosure는 level 사이에 monotonic한 포함 관계가 있을 때 특히 유용합니다. 독립 variant를 억지로 누적하면 불필요한 context와 충돌이 생깁니다.
- Progressive disclosure는 단계 수를 늘리는 목표가 아닙니다. 작은 conditional detail은 inline이 더 KISS할 수 있습니다.

## Related Patterns

- [Progressive Context Routing](progressive-context-routing.md) — discovery 이후 필요한 context만 단계적으로 좁혀 load하는 더 일반적인 routing shape를 설명합니다.

## Boundary

이 패턴은 **argument를 reusable behavior control과 conditional context selection에 사용하는 설계**를 소유합니다.

특정 argument 이름, CLI syntax, YAML schema, `hint` field, precedence 체계, file layout 또는 runtime loading mechanism을 표준화하지 않습니다. Argument는 기존 authority나 safety boundary를 우회하지 않으며, progressive disclosure는 필요한 behavior를 숨기거나 선택되지 않은 context를 임의로 적용하기 위한 장치가 아닙니다.

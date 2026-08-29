---
description: Agent나 automation이 만든 변경에서 반복되는 기계적으로 판정 가능한 부실을 실행 가능한 check로 탐지할지 판단할 때 참고하며, 적용 범위·비용·배치·수명 관리를 다루는 패턴입니다.
---

# Executable Output Checks

Agent나 automation이 빠르게 변경을 만들수록 사람이 모든 결과물을 같은 깊이로 다시 확인하기는 어려워집니다. 이때 **반복적으로 발생하고 기계적으로 판정 가능한 일부 부실을 executable check로 빠르게 드러내는 것**을 고려할 수 있습니다.

여기서 output은 source code뿐 아니라 configuration, generated artifact, 문서 projection, package/dependency structure처럼 작업 결과로 repository에 남는 다양한 산출물을 포함할 수 있습니다.

이 패턴은 agent output의 품질 전체를 자동 판정하려는 접근이 아닙니다. 설계의 자연스러움, naming, abstraction 수준, readability처럼 맥락 판단이 필요한 품질은 여전히 review의 영역으로 남깁니다.

핵심은 **검사 가능한 것을 전부 검사하는 것이 아니라, 검사할 가치가 있는 소수의 안정된 성질만 가장 싼 신뢰 가능한 방법으로 확인하는 것**입니다.

## Core

Executable output check는 구현 방법을 세세하게 지시하기보다 **완성된 output에서 관찰할 수 있는 성질**을 검사합니다.

예를 들어 다음은 비교적 기계적으로 확인하기 쉽습니다.

- 금지된 dependency 방향이 생겼는가?
- generated output이 source-of-truth와 달라졌는가?
- generated 영역을 직접 수정했는가?
- 특정 package의 internal surface를 외부에서 직접 사용했는가?
- configuration의 금지된 조합이 만들어졌는가?
- 필요한 artifact가 없거나 정해진 format으로 parse되지 않는가?

반대로 다음과 같은 판단을 억지 check로 만들지는 않는 편이 자연스럽습니다.

- 이 abstraction이 너무 복잡한가?
- 이 함수가 읽기 쉬운가?
- 이 이름이 충분히 직관적인가?
- 이 책임 분리가 지금 상황에서 가장 좋은가?

좋은 check는 agent에게 정답 구현을 강요하기보다 **분명한 실패 신호와 다시 탐색할 수 있는 feedback**을 제공합니다.

## 무엇을 Check할지

Check를 추가하기 전에는 먼저 **결함의 비용과 check의 비용을 함께** 봅니다. 다음 성질이 많이 겹칠수록 executable check 후보가 되기 쉽습니다.

- 같은 종류의 부실이 반복적으로 발생합니다.
- 위반 여부를 비교적 객관적으로 판정할 수 있습니다.
- 늦게 발견하면 수정 범위나 복구 비용이 커집니다.
- 보호하려는 성질이 충분히 안정되어 있습니다.
- 실패 메시지를 보고 사람이든 agent든 다음 행동을 이해할 수 있습니다.
- 기존 mechanism 또는 작은 deterministic check로 비교적 싸게 확인할 수 있습니다.

반대로 일회성 문제, 아직 탐색 중인 설계 선택, 낮은 비용의 실수, 자주 바뀌는 convention은 자동화보다 review나 documentation으로 남기는 편이 나을 수 있습니다.

특히 **사람이 review할 때 같은 객관적 지적을 반복하고 있다면** check 후보인지 살펴볼 가치가 있습니다. 다만 반복된다는 이유만으로 자동화하지 않고, 그 지적이 실제로 stable invariant인지 먼저 확인합니다.

## 가장 싼 Mechanism부터

별도 test나 custom checker를 바로 만들 필요는 없습니다. 같은 성질을 더 자연스럽게 보장하는 수단이 있다면 그것을 우선할 수 있습니다.

대체로 다음처럼 비용이 낮은 쪽부터 비교해볼 수 있습니다.

1. language, type system, module/package visibility처럼 원래 존재하는 제약
2. build system, schema validator, formatter, linter처럼 이미 사용하는 mechanism
3. repository의 기존 deterministic test 또는 validation surface
4. 좁은 structural test나 작은 custom checker
5. 별도 custom enforcement가 정말 필요한 경우의 전용 tooling

CI는 이런 check를 실행하는 한 surface일 수 있지만, **CI 자체가 check의 목적은 아닙니다.** 더 낮은 계층에서 자연스럽게 보장할 수 있는 성질을 custom CI logic으로 다시 구현하지 않습니다.

## 대표적인 Output과 Check

| Output에서 생기는 부실 | 가능한 check | 비고 |
| --- | --- | --- |
| 금지된 package dependency | module/package rule, dependency graph check, structural test | architecture invariant의 대표 사례 |
| generated output 누락·stale | regenerate 후 diff, deterministic comparison | source-of-truth가 명확할 때 유용 |
| generated 영역 직접 수정 | generation consistency check, ownership-aware diff | 생성 방식과 repository 특성에 따라 다름 |
| 잘못된 config 조합 | schema 또는 semantic validator | 단순 schema만으로 부족할 수 있음 |
| internal API 직접 사용 | visibility mechanism, import/dependency check | public boundary가 안정적일 때 적합 |
| 필요한 artifact 누락·형식 오류 | parser, manifest check, deterministic validation | artifact 자체가 durable contract일 때 적합 |

이 표의 형태를 그대로 구현할 필요는 없습니다. 같은 문제라도 ecosystem이 이미 제공하는 mechanism이 있다면 별도 custom check보다 그것을 사용하는 편이 단순할 수 있습니다.

## Architecture Check는 한 가지 Case입니다

Architecture invariant를 별도 test로 표현해야 한다면 일반 behavior test와 구분되는 위치를 둘 수 있습니다.

```text
tests/
├─ unit/
├─ integration/
└─ architecture/
   ├─ test_dependency_direction.py
   └─ test_module_boundaries.py
```

예를 들어 `payments` package의 내부 구현을 외부 module이 직접 사용하지 않아야 한다면 다음과 같은 성질을 검사할 수 있습니다.

```text
orders ───────┐
billing ──────┼──→ payments public API → payments/internal
subscriptions ┘
```

외부 code에서 다음 import가 생기면 architecture check가 실패하도록 할 수 있습니다.

```python
from payments.internal.stripe_client import StripeClient
```

이때 일반 behavior test의 질문은 **"결제가 동작하는가?"**이고, architecture check의 질문은 **"의도된 package boundary를 지키면서 구현했는가?"**입니다.

`tests/architecture/`는 대표적인 배치일 뿐 pattern의 요구사항은 아닙니다. Language나 package system이 같은 boundary를 자연스럽게 보장한다면 별도 test를 두지 않는 편이 더 단순합니다. Marker나 prefix·suffix도 선택 실행이나 discovery에 실제 이점이 있을 때만 추가하고, directory만으로 의미가 충분하면 반복하지 않을 수 있습니다.

## Generated Output Check 예시

Schema가 generated type의 source-of-truth라면 agent가 schema를 수정한 뒤 generated artifact 갱신을 빠뜨리는 문제가 생길 수 있습니다.

```text
schema/api.yaml
      │
      ↓ generate
generated/api_types.py
```

이 관계가 안정적이고 누락 비용이 크다면 다음과 같은 작은 check를 둘 수 있습니다.

```text
현재 source에서 다시 generate
        ↓
committed generated output과 비교
        ↓
차이가 있으면 실패
```

이 check는 agent에게 어떤 방식으로 schema를 설계하라고 지시하지 않습니다. **완성된 output이 source-of-truth와 일치하는지만** 확인합니다.

## Agent Feedback Surface로 사용하기

Executable output check의 중요한 장점은 사람이 발견하기 전에도 agent가 자기 변경의 일부 결함을 직접 확인할 수 있다는 점입니다.

```text
Agent change
    ↓
Executable checks
    ↓
기계적으로 판정 가능한 결함 발견
    ↓
Agent가 다른 구현 또는 누락된 작업 탐색
```

기능 test가 모두 통과해도 structural drift나 generated artifact 누락은 남을 수 있습니다. 이런 check는 behavior test를 대체하지 않고 **다른 종류의 feedback을 추가**합니다.

실패 메시지는 가능하면 단순한 `false`보다 **무엇이 위반되었고 어디를 다시 봐야 하는지** 드러내는 편이 좋습니다. Agent가 check의 의도를 추측하기 위해 또 다른 긴 문서를 찾아야 한다면 feedback의 가치가 줄어듭니다.

## 비용과 수명도 함께 관리합니다

Check는 한 번 추가하면 끝나는 자산이 아닙니다. 다음 비용이 계속 따라올 수 있습니다.

- check 자체의 유지보수
- false positive와 예외 처리
- 실패 원인 해석
- 실행 시간과 CI noise
- architecture나 tooling 변화에 따른 갱신
- 새로운 agent가 check를 만족시키기 위해 불필요한 우회 구조를 만드는 비용

따라서 check를 추가할 때뿐 아니라 **계속 유지할 가치가 있는지도 다시 볼 수 있어야 합니다.**

예를 들어 custom structural test로 지키던 boundary를 이후 language module system이 직접 보장하게 되었다면 custom test를 제거하는 것이 더 나을 수 있습니다. 보호하던 invariant 자체가 사라졌다면 check도 함께 사라지는 편이 자연스럽습니다.

## Limits and Responses

### 기계적으로 검사되는 것만 중요해질 수 있습니다

자동화하기 쉬운 항목이 실제 software quality 전체를 대표하지는 않습니다. Design, cohesion, naming, simplicity와 같은 판단은 별도 review가 계속 필요합니다.

**대응:** executable check가 담당하는 범위를 machine-checkable defect로 좁게 설명하고, green check를 전체 품질 보증으로 해석하지 않습니다.

### Check가 계속 늘어나면 관리 비용이 더 커질 수 있습니다

작은 rule도 누적되면 custom lint, test, exception과 failure interpretation 자체가 복잡한 subsystem이 될 수 있습니다.

**대응:** 새 check를 추가하기 전에 기존 mechanism으로 흡수할 수 있는지 보고, 낮은 가치의 check는 만들지 않거나 제거합니다. 여러 check가 같은 성질을 중복해서 보호하지 않는지도 확인합니다.

### Rule을 통과하기 위한 우회 구조가 생길 수 있습니다

좁은 syntactic rule은 실제 의도보다 check 통과만 최적화하는 코드를 만들 수 있습니다.

**대응:** 가능한 한 보호하려는 output property를 직접 검사하고, 예외와 wrapper가 계속 늘어나면 rule 자체가 잘못 모델링되었는지 다시 봅니다.

### Agent가 check 자체도 수정할 수 있습니다

Agent가 output과 checker를 모두 수정할 수 있는 환경에서는 check를 약화시키거나 삭제하는 변경도 만들 수 있습니다. 따라서 executable check 자체가 자동으로 trust boundary가 되는 것은 아닙니다.

**대응:** 일반적인 품질 feedback과 보안·규정·고위험 enforcement를 구분합니다. 독립적인 보호가 필요한 constraint는 repository permission, protected CI, review ownership 등 해당 위험을 실제로 통제하는 별도 mechanism이 소유해야 합니다.

### 실행 비용이 결함 비용보다 커질 수 있습니다

비싼 전체 repository scan을 모든 작은 변경마다 수행하면 feedback이 느려지고 개발 흐름을 방해할 수 있습니다.

**대응:** check의 가치와 실행 비용을 함께 보고, 더 싼 표현이나 실행 surface가 있는지 비교합니다. 모든 check가 항상 같은 cadence로 실행될 필요는 없습니다.

## Related Patterns

- [`Source-Mirrored Test Structure`](source-mirrored-test-structure.md)는 test와 source 사이의 탐색·grouping 관계를 다룹니다. Executable Output Checks는 무엇을 기계적으로 확인할 가치가 있는지와 그 feedback surface를 다룹니다.
- [`Filesystem-Legible Structure`](filesystem-legible-structure.md)는 filesystem을 navigation cue로 활용하는 방법을 다룹니다. Check의 배치는 legibility를 고려할 수 있지만 filesystem 자체가 enforcement를 대신하지는 않습니다.

## Grounding

- [OpenAI, *Harness engineering: leveraging Codex in an agent-first world*](https://openai.com/index/harness-engineering/)는 fully agent-generated repository에서 documentation만으로는 coherence를 유지하기 어렵고, dependency direction과 일부 invariant를 custom lint와 structural test로 기계적으로 검증한 사례를 설명합니다.
- [Google Engineering Practices, *What to look for in a code review*](https://google.github.io/eng-practices/review/reviewer/looking-for.html)는 code health가 design, complexity, test coverage 등 기계적 검사를 넘어서는 판단을 포함한다는 점을 보여줍니다. Executable check를 human review의 대체재로 보지 않는 근거로 참고할 수 있습니다.

## Short Form

> **Agent나 automation의 output에서 반복되는 기계적으로 판정 가능한 부실만 골라 가장 싼 실행 가능한 check로 빠르게 드러내되, check의 유지 비용과 한계를 함께 관리합니다.**

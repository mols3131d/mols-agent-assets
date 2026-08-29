---
description: Agent나 automation의 작업 결과에서 기계적으로 관찰 가능한 부실을 실행 가능한 check로 드러내고, 적절한 실행 방식과 피드백 강도를 선택할 때 참고하는 패턴입니다.
---

# Executable Output Checks

Agent나 automation이 빠르게 결과물을 만들수록 사람이 모든 변경을 같은 깊이로 다시 확인하기는 어렵습니다. 이때 **작업 결과에서 기계적으로 관찰 가능한 일부 부실을 executable check로 드러내는 것**을 고려할 수 있습니다.

여기서 output은 source code만 뜻하지 않습니다. Configuration, generated artifact, manifest, 문서 projection, package/dependency structure처럼 작업 결과로 남는 여러 산출물이 대상이 될 수 있습니다.

이 패턴은 output 전체의 품질을 자동 판정하거나 모든 발견을 차단하려는 접근이 아닙니다. 핵심은 **관찰할 성질, 확인 방법, 실행 위치와 시점, feedback 강도를 서로 분리해 선택하는 것**입니다.

```text
관찰할 output property
        ↓
더 직접적인 prevention이 이미 있는가?
        ├─ yes → 별도 check가 필요하지 않을 수 있음
        └─ no
             ↓
      가장 단순한 executable check
             ↓
      결과의 의미를 해석
             ↓
      적절한 surface와 feedback 강도
```

Architecture check나 test framework는 이 패턴의 여러 적용 형태 중 일부입니다.

## Core

Executable output check는 구현 방법을 세세하게 지시하기보다 **완성된 output에서 관찰할 수 있는 성질을 실행 가능한 feedback으로 바꿉니다.**

예를 들면 다음과 같습니다.

- generated output이 source-of-truth와 어긋났는가?
- 필요한 manifest나 artifact가 없거나 parse되지 않는가?
- configuration에 위험하거나 허용하지 않는 조합이 생겼는가?
- 문서나 route 같은 projection이 작성 원본과 달라졌는가?
- 특정 internal surface가 의도하지 않은 범위에서 사용되는가?
- dependency나 module boundary가 의도된 구조에서 벗어났는가?

좋은 check는 정답 구현을 강요하기보다 **무엇이 관찰되었는지 사람이든 agent든 다시 판단할 수 있게 드러냅니다.**

이 패턴은 일반적인 testing strategy나 quality gate 체계 전체를 소유하지 않습니다. 함수와 기능의 behavior correctness, design·naming·abstraction·readability처럼 맥락 판단이 필요한 품질, security·compliance처럼 독립적인 assurance가 필요한 보호 모델은 각각 더 적합한 testing, review, security mechanism의 책임으로 남깁니다.

## 무엇을 Check할지

검사할 수 있다는 이유만으로 check를 추가하지는 않습니다. **놓쳤을 때의 비용과 check 자체의 비용을 함께** 봅니다.

다음 성질이 많이 겹칠수록 executable check가 유용할 가능성이 높습니다.

- 같은 종류의 부실이 반복해서 나타납니다.
- 아직 반복되지 않았더라도 위반 비용이 큰 안정된 성질입니다.
- 결과를 보고 비교적 객관적으로 판정할 수 있습니다.
- 늦게 발견하면 수정 범위나 복구 비용이 커집니다.
- 결과를 보고 사람이나 agent가 다음 행동을 이해할 수 있습니다.
- 기존 도구나 작은 deterministic check로 비교적 싸게 확인할 수 있습니다.

반대로 일회성이고 영향이 작은 문제, 아직 탐색 중인 설계 선택, 쉽게 고칠 수 있는 낮은 비용의 실수, 자주 바뀌는 convention은 review나 documentation에 남기는 편이 나을 수 있습니다.

사람이 review에서 같은 객관적 지적을 반복하고 있다면 좋은 check 후보일 수 있습니다. 반대로 사고 이력이 없더라도 놓쳤을 때의 비용이 크고 property가 충분히 안정적이며 값싸게 판정할 수 있다면 선제적인 check를 고려할 수 있습니다.

## 더 직접적인 Mechanism이 있으면 먼저 사용합니다

Output을 사후에 검사하기보다 해당 성질을 이미 직접 보장하는 native mechanism이 있다면 별도 output check가 필요 없을 수 있습니다.

예를 들어 type system, module/package visibility, schema contract가 위반 자체를 자연스럽게 예방한다면 같은 의미를 custom script나 CI에서 다시 구현하는 것은 중복일 수 있습니다. **Prevention이 이미 충분하면 check를 추가하지 않는 것도 이 패턴의 정상적인 적용 결과**입니다.

별도 관찰이 여전히 필요하다면 다음과 같은 executable form을 선택할 수 있습니다.

- formatter, linter, schema validator, build tool의 check mode
- 작은 script 또는 CLI command
- source-of-truth에서 다시 생성한 뒤 비교하는 generator + diff
- 일반 test 또는 structural test
- 특정 목적을 위한 작은 custom checker

중요한 것은 test인지 script인지가 아니라 **해당 output property를 가장 단순하고 신뢰 가능하게 확인할 수 있는가**입니다.

판정 logic을 local script, test와 CI에 각각 복제할 필요는 없습니다. 하나의 의미를 여러 surface에서 사용한다면 가능한 한 판정 logic의 owner는 하나로 두고 필요한 위치에서 호출합니다. 반대로 check 하나 때문에 미래 확장을 예상해 중앙 checker framework나 registry부터 만들 필요도 없습니다.

## 결과와 Feedback 강도를 분리합니다

Check 결과와 그 결과를 얼마나 강하게 취급할지는 별개의 결정입니다.

개념적으로는 다음 상태를 구분할 수 있습니다.

| Check 결과 | 의미 |
| --- | --- |
| 확인됨 | 관찰하려던 property를 확인했고 특이사항을 찾지 못함 |
| Finding | property를 확인했고 drift, 위반 또는 검토할 항목을 발견함 |
| 판정 불가 | tool, environment, dependency 등의 이유로 property를 신뢰성 있게 확인하지 못함 |

이 이름이나 세 상태를 그대로 구현할 필요는 없습니다. 핵심은 checker 실행 실패를 output defect로 오인하지 않고, 반대로 `판정 불가`를 clean result처럼 취급하지 않는 것입니다.

Finding은 상황에 따라 다른 강도로 표면화할 수 있습니다.

| Feedback | 어울리는 상황 | 예시 |
| --- | --- | --- |
| 정보 / signal | 추세나 잠재적 drift를 보여주는 것만으로 가치가 있음 | dependency 변화, generated diff |
| 경고 / warning | 수정할 가치가 높지만 합리적인 예외나 맥락 판단이 남음 | deprecated internal API 사용, 권장 범위를 벗어난 config |
| 차단 / blocking | 판정 신뢰도가 높고 그대로 진행하는 비용이 큰 안정된 위반 | parse 불가능한 필수 manifest, 반드시 동기화되어야 하는 artifact |

Executable하다는 이유만으로 blocking할 필요는 없습니다. **판정 신뢰도와 위반 비용에 비례하는 최소한의 유용한 feedback**을 선택합니다.

기존 repository에 이미 많은 위반이 있다면 처음부터 blocking으로 강제하기보다 signal이나 warning으로 실제 유용성과 noise를 관찰한 뒤 조정하는 방식도 가능합니다.

## 실행 위치와 시점도 별도 선택입니다

하나의 check를 어디서 언제 실행할지는 구현 형태와 feedback 강도와도 별개의 결정입니다.

- agent나 사람이 필요할 때 직접 실행하는 command
- local development workflow
- editor나 hook에서 주는 빠른 feedback
- test suite
- PR이나 CI의 annotation/check
- 비용이 큰 검사의 주기적 또는 수동 audit

모든 check를 PR Gate에 넣을 필요는 없습니다. 빠른 local signal이면 충분한 항목도 있고, 전체 repository나 외부 환경을 읽어야 하는 비싼 검사는 필요한 시점에만 실행하는 편이 나을 수 있습니다.

## 대표 사례

| Output에서 관찰할 문제 | 가능한 executable form | 가능한 feedback |
| --- | --- | --- |
| generated output이 stale함 | regenerate + diff, checker script | 정보, 경고, 필요한 경우 차단 |
| manifest나 artifact 형식 오류 | parser, schema/semantic validator | 경고 또는 차단 |
| 잘못된 config 조합 | validator script, existing linter | 경고 또는 차단 |
| 작성 원본과 projection의 drift | generator + comparison | 정보 또는 경고 |
| internal API의 의도하지 않은 사용 | import/dependency checker | 경고 또는 차단 |
| architecture dependency 위반 | dependency script, structural test | 경고 또는 차단 |

이 표는 구현 계약이 아니라 별도 관찰이 필요한 경우의 선택지를 보여주는 예시입니다. Native visibility나 module constraint가 같은 문제를 직접 예방한다면 표의 check를 추가하지 않는 편이 더 단순할 수 있습니다.

## 예시: Generated Output을 확인하기

Schema가 generated type의 source-of-truth라고 가정합니다.

```text
schema/api.yaml
      │
      ↓ generate
generated/api_types.py
```

Agent가 schema를 수정했지만 generated artifact를 갱신하지 않을 수 있습니다. 이 관계가 반복적으로 문제를 만들거나 놓쳤을 때의 비용이 크고 비교가 싸다면 작은 check를 둘 수 있습니다.

```text
scripts/check_generated.py
        ↓
source에서 다시 generate
        ↓
committed output과 비교
        ↓
Finding이 있으면 보여줌
```

Local workflow에서는 diff를 warning으로 보여주고, PR에서는 annotation으로 노출할 수 있습니다. Generated output의 일치가 실제 필수 조건인 repository라면 같은 판정을 blocking check로 사용할 수도 있습니다.

이 check가 직접 확인하는 것은 **source-of-truth와 committed output의 동기화 상태**입니다. Generator 자체의 semantic correctness까지 자동으로 증명하는 것은 아닙니다.

검사 과정이 output을 직접 수정한다면 원래 상태와 checker가 만든 상태가 섞일 수 있으므로, 그 side effect가 판단을 흐리는 경우에는 관찰과 수정의 역할을 구분하는 편이 이해하기 쉽습니다.

Architecture boundary도 같은 패턴의 한 사례입니다. 예를 들어 `payments`의 internal package를 외부에서 직접 사용하는지 `scripts/check_architecture.py` 같은 dependency checker로 확인할 수도 있고, ecosystem의 test infrastructure가 자연스럽게 맞는다면 `tests/architecture/test_module_boundaries.py` 같은 structural test로 표현할 수도 있습니다. Language나 package visibility가 이미 같은 boundary를 보장한다면 별도 check가 필요 없을 수 있습니다.

## Agent Feedback Surface

Executable output check는 사람이 발견하기 전에 agent가 자기 변경의 일부 문제를 직접 확인하는 feedback surface가 될 수 있습니다.

```text
Agent change
    ↓
Executable check
    ↓
Finding 또는 판정 불가
    ↓
Agent가 수정하거나 다시 판단
```

기능 test가 통과하더라도 generated artifact 누락, configuration drift, structural 문제처럼 다른 종류의 결함이 남을 수 있습니다. 결과는 단순한 `false`보다 **무엇을 관찰했고, 어느 output이 관련되며, 무엇을 다시 확인하면 되는지**가 드러날수록 agent와 사람 모두에게 유용합니다.

## 비용과 수명

Check는 한 번 추가하면 끝나는 자산이 아닙니다. 유지보수, false positive, 예외, 실행 시간, feedback noise와 tooling 변화 대응 비용이 따라옵니다.

따라서 새 check를 만드는 것뿐 아니라 **강도를 낮추거나, 실행 시점을 옮기거나, 더 싼 mechanism으로 대체하거나, 제거하는 선택**도 열어둡니다.

Custom checker가 지키던 성질을 이후 compiler나 native tooling이 자연스럽게 보장하게 되었다면 checker를 없애는 편이 더 단순합니다. Warning이 반복해서 무시되거나 예외가 계속 쌓인다면 더 많은 예외를 추가하기 전에 check 자체의 가치와 모델을 다시 봅니다.

## Limits and Responses

### Machine-checkable은 전체 품질을 뜻하지 않습니다

자동화하기 쉬운 항목이 software quality 전체를 대표하지는 않습니다. Design, cohesion, naming, simplicity처럼 맥락 판단이 필요한 품질은 여전히 review가 필요합니다.

**대응:** clean result를 전체 품질 보증으로 해석하지 않고, check가 담당하는 machine-observable property의 증거로만 사용합니다.

### Deterministic한 Check도 틀리거나 일부만 볼 수 있습니다

같은 입력에서 같은 결과가 나온다는 사실은 판정 기준이 옳다는 뜻이 아닙니다. 잘못된 요구나 오래된 assumption을 일관되게 구현할 수 있고, targeted check는 일부 path나 state만 볼 수도 있습니다. 평가 대상과 checker가 같은 구현 경로나 가정을 공유하면 같은 blind spot을 가질 수도 있습니다.

**대응:** check가 실제로 관찰하는 범위보다 넓은 의미를 부여하지 않습니다. 더 높은 assurance가 필요한 문제에서는 더 독립적이거나 넓은 verification이 필요한지 별도로 판단합니다.

### Checker 자체도 실패하거나 불안정할 수 있습니다

Network, wall-clock time, 외부 service나 불안정한 environment에 의존하는 check는 같은 output에도 다른 결과를 낼 수 있습니다. Flaky warning과 failure가 반복되면 중요한 signal까지 무시되기 쉽습니다.

**대응:** output finding과 checker의 `판정 불가`를 구분하고, 신뢰도가 낮은 판정을 강한 gate로 사용하지 않습니다.

### 오래된 Rule과 예외가 숨은 Policy가 될 수 있습니다

처음에는 유효했던 boundary나 convention도 시간이 지나면 달라질 수 있습니다. Allowlist, ignore와 suppression이 늘어나면 check의 실제 의미가 예외 목록에 숨어버릴 수 있습니다.

**대응:** 예외나 우회가 반복되면 더 추가하기 전에 보호하려는 property 자체가 여전히 유효한지 봅니다. 필요하면 범위나 강도를 바꾸거나 check를 제거합니다.

### Check 통과 자체가 목표가 될 수 있습니다

좁은 syntactic rule은 실제 품질보다 check 통과를 최적화하는 wrapper, rename과 우회 구조를 만들 수 있습니다.

**대응:** 가능한 한 보호하려는 output property를 직접 관찰하고, 우회가 반복되면 check가 실제 문제를 잘 모델링하는지 다시 봅니다. Passing 자체를 품질 목표로 삼지 않습니다.

### Check가 많아지면 비용과 Noise가 커집니다

작은 script, lint rule, test와 warning도 누적되면 별도의 subsystem이 됩니다. 의미가 약한 warning이 많아지면 중요한 signal까지 습관적으로 무시될 수 있습니다.

**대응:** 새로운 check보다 기존 mechanism으로 표현할 수 있는지 먼저 비교하고, 가치가 낮거나 중복되는 check는 만들지 않거나 정리합니다.

### Agent가 Checker 자체를 수정할 수 있습니다

Agent가 output과 checker를 함께 수정할 수 있다면 warning을 없애거나 checker를 약하게 만드는 변경도 가능합니다. 일반 품질 feedback에서는 review가 충분할 수 있지만 executable check만으로 독립적인 assurance가 생기지는 않습니다.

**대응:** 보안, 규정, 고위험 constraint처럼 독립적인 보호가 필요한 문제는 repository permission, protected workflow, review ownership처럼 해당 위험을 실제로 통제하는 mechanism에서 다룹니다.

## Boundary

이 패턴은 **작업 결과의 machine-observable property를 executable feedback으로 바꾸는 설계**를 다룹니다.

- 일반적인 unit/integration/e2e testing 전략을 정의하지 않습니다.
- 모든 quality concern을 mechanical rule로 바꾸지 않습니다.
- `tests/`, `scripts/`, hook, CI 중 하나를 기본 배치로 정하지 않습니다.
- 정보·경고·차단 중 하나의 고정 severity 체계를 요구하지 않습니다.
- architecture invariant는 여러 적용 사례 중 하나일 뿐 이 패턴의 상위 개념이 아닙니다.
- project-specific mandatory gate와 workflow는 해당 repository의 operational policy가 소유합니다.

## Related Patterns

- [`Source-Mirrored Test Structure`](source-mirrored-test-structure.md)는 test와 source 사이의 탐색·grouping 관계를 다룹니다. Executable Output Checks는 어떤 output property를 기계적으로 관찰할지와 그 feedback을 다룹니다.
- [`Filesystem-Legible Structure`](filesystem-legible-structure.md)는 filesystem을 navigation cue로 활용하는 방법을 다룹니다. Check의 배치는 legibility를 고려할 수 있지만 filesystem 자체가 check를 대신하지는 않습니다.

## Grounding

- [OpenAI, *Harness engineering: leveraging Codex in an agent-first world*](https://openai.com/index/harness-engineering/)는 agent-generated repository에서 documentation, architecture와 structural invariant를 lint와 structural test 같은 executable feedback으로 연결한 사례를 보여줍니다. 동시에 높은 agent throughput 환경에서 blocking gate를 최소화한 사례도 제시하므로, executable feedback과 blocking policy를 같은 개념으로 보지 않는 참고점이 됩니다.
- [Google Engineering Practices, *Code Review Developer Guide*](https://google.github.io/eng-practices/review/)는 code review가 design, functionality와 complexity 같은 판단을 포함한다는 점을 보여줍니다. Machine check를 전체 quality review의 대체재로 보지 않는 경계의 참고점입니다.

## Short Form

> **작업 결과에서 반복적으로 문제를 만들거나 놓쳤을 때 비용이 큰 machine-observable property를 가장 단순한 executable check로 드러내고, 상황에 맞는 위치와 강도로 feedback합니다. 더 직접적인 prevention이 이미 있다면 별도 check를 만들지 않으며, check는 자신이 실제로 관찰한 범위만 증거로 제공합니다.**

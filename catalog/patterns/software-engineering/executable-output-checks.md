---
description: Agent나 automation의 작업 결과에서 기계적으로 판정 가능한 부실을 실행 가능한 check로 발견하고, 적절한 실행 방식과 피드백 강도를 선택할 때 참고하는 패턴입니다.
---

# Executable Output Checks

Agent나 automation이 빠르게 결과물을 만들수록 사람이 모든 변경을 같은 깊이로 다시 확인하기는 어렵습니다. 이때 **작업 결과에서 기계적으로 관찰할 수 있는 일부 부실을 executable check로 드러내는 것**을 고려할 수 있습니다.

여기서 output은 source code만 뜻하지 않습니다. Configuration, generated artifact, manifest, 문서 projection, package/dependency structure처럼 작업 결과로 남는 여러 산출물이 대상이 될 수 있습니다.

이 패턴은 output의 품질 전체를 자동 판정하거나 모든 발견을 차단하려는 접근이 아닙니다. 핵심은 다음 세 가지 선택을 분리하는 것입니다.

```text
관찰할 output property
        ↓
실행 가능한 check
        ↓
적절한 feedback surface와 강도
```

같은 check라도 상황에 따라 단순한 정보, 경고, 수정 권고, blocking failure로 다르게 사용할 수 있습니다. Architecture check와 test framework는 이 패턴의 여러 적용 형태 중 일부입니다.

## Core

Executable output check는 구현 방법을 세세하게 지시하기보다 **완성된 output에서 관찰할 수 있는 성질**을 확인합니다.

예를 들면 다음과 같습니다.

- generated output이 source-of-truth와 어긋났는가?
- 필요한 manifest나 artifact가 없거나 parse되지 않는가?
- configuration에 위험하거나 허용하지 않는 조합이 생겼는가?
- 문서나 route 같은 projection이 작성 원본과 달라졌는가?
- 특정 internal surface가 의도하지 않은 범위에서 사용되는가?
- dependency나 module boundary가 의도된 구조에서 벗어났는가?

반대로 다음과 같은 판단은 중요하더라도 기계적 check에 억지로 넣지 않는 편이 자연스럽습니다.

- 이 abstraction이 지나치게 복잡한가?
- 이 이름이 충분히 직관적인가?
- 이 책임 분리가 지금 상황에서 자연스러운가?
- 이 코드가 사람에게 읽기 쉬운가?

좋은 check는 정답 구현을 강요하기보다 **관찰 가능한 문제와 다음 판단에 도움이 되는 feedback**을 제공합니다.

## 무엇을 Check할지

검사할 수 있다는 이유만으로 check를 추가하지는 않습니다. **놓쳤을 때의 비용과 check 자체의 비용을 함께** 봅니다.

다음 성질이 많이 겹칠수록 executable check가 유용할 가능성이 높습니다.

- 같은 종류의 부실이 반복해서 나타납니다.
- 결과만 보고도 비교적 객관적으로 판정할 수 있습니다.
- 늦게 발견하면 수정 범위나 복구 비용이 커집니다.
- 관찰하려는 성질이 충분히 안정되어 있습니다.
- 결과를 보고 사람이나 agent가 다음 행동을 이해할 수 있습니다.
- 기존 mechanism이나 작은 deterministic check로 비교적 싸게 확인할 수 있습니다.

반대로 일회성 문제, 아직 탐색 중인 설계 선택, 쉽게 고칠 수 있는 낮은 비용의 실수, 자주 바뀌는 convention은 자동화보다 review나 documentation에 남기는 편이 나을 수 있습니다.

사람이 review에서 같은 객관적 지적을 반복하고 있다면 check 후보인지 살펴볼 수 있습니다. 다만 반복된다는 사실만으로 자동화하지 않고, 실제로 기계적 feedback이 문제 비용을 줄이는지 봅니다.

## 가장 단순한 실행 방법을 선택합니다

Executable check가 반드시 test일 필요는 없습니다. 같은 output property를 더 자연스럽고 싸게 확인할 수 있는 mechanism이 있다면 그것을 사용할 수 있습니다.

대표적인 형태는 다음과 같습니다.

- language, type system, module/package visibility 같은 native constraint
- formatter, linter, schema validator, build tool처럼 이미 사용하는 도구
- 작은 script 또는 CLI command
- source-of-truth에서 다시 생성한 뒤 비교하는 generator + diff
- 일반 test 또는 structural test
- 특정 목적을 위한 작은 custom checker

예를 들어 generated artifact가 최신인지 확인하는 데 pytest가 특별한 이점을 주지 않는다면 다음처럼 독립 script가 더 단순할 수 있습니다.

```text
scripts/check_generated.py
```

반대로 확인하려는 성질이 기존 test fixture나 assertion과 자연스럽게 맞는다면 test framework에 두는 것도 좋은 선택입니다.

중요한 것은 **test인지 script인지가 아니라, 해당 output property를 가장 단순하고 신뢰 가능하게 확인할 수 있는가**입니다.

## 실행 위치와 시점도 별도 선택입니다

Check의 구현과 그것을 언제 실행할지는 같은 결정이 아닙니다. 하나의 check를 필요에 따라 여러 surface에서 호출할 수도 있습니다.

예를 들면 다음과 같습니다.

- agent나 사람이 필요할 때 직접 실행하는 command
- local development workflow
- editor나 hook에서 주는 빠른 feedback
- test suite
- PR이나 CI의 annotation/check
- 비용이 큰 검사의 주기적 또는 수동 audit

모든 check를 항상 PR Gate에서 실행할 필요는 없습니다. 빠른 local signal이면 충분한 항목도 있고, 전체 repository를 읽어야 하는 비싼 검사는 필요한 시점에만 실행하는 편이 나을 수도 있습니다.

가능하면 같은 판정 logic을 여러 script, test, CI workflow에 복제하기보다 하나의 check를 필요한 surface에서 재사용합니다.

## Feedback 강도는 Check와 분리합니다

Executable하다는 것은 자동으로 blocking해야 한다는 뜻이 아닙니다. 발견한 문제의 확실성, 비용과 예외 가능성에 따라 feedback 강도를 다르게 둘 수 있습니다.

대표적으로 다음 정도를 생각할 수 있습니다.

| Feedback | 어울리는 상황 | 예시 |
| --- | --- | --- |
| 정보 / signal | 추세나 잠재적 drift를 보여주는 것만으로 가치가 있음 | 새 dependency 방향을 보고하거나 generated diff를 보여줌 |
| 경고 / warning | 수정할 가치가 높지만 합리적인 예외나 맥락 판단이 남음 | deprecated internal API 사용, 권장 범위를 벗어난 config |
| 차단 / blocking | 판정 신뢰도가 높고 그대로 진행하는 비용이 큰 안정된 위반 | parse 불가능한 필수 manifest, 반드시 동기화되어야 하는 generated artifact |

이 구분은 고정 severity 체계가 아닙니다. 같은 check도 repository의 성숙도나 적용 시점에 따라 처음에는 warning으로 관찰하다가 필요가 확인되면 강하게 만들 수 있고, 반대로 비용이 커지면 낮추거나 제거할 수 있습니다.

필요 이상으로 강한 gate를 만드는 것보다 **문제의 성격에 맞는 최소한의 유용한 feedback**을 선택하는 편이 유지하기 쉽습니다.

## 대표 사례

| Output에서 관찰할 문제 | 가능한 executable form | 가능한 feedback |
| --- | --- | --- |
| generated output이 stale함 | regenerate + diff, checker script | 정보, 경고, 필요한 경우 차단 |
| manifest나 artifact 형식 오류 | parser, schema/semantic validator | 경고 또는 차단 |
| 잘못된 config 조합 | validator script, existing linter | 경고 또는 차단 |
| 작성 원본과 projection의 drift | generator + comparison | 정보, 경고, optional validation |
| internal API의 의도하지 않은 사용 | import/dependency checker, visibility mechanism | 경고 또는 차단 |
| architecture dependency 위반 | language rule, dependency script, structural test | 경고 또는 차단 |

이 표는 구현 계약이 아니라 선택지를 보여주는 예시입니다. 같은 문제라도 ecosystem과 repository 특성에 따라 더 단순한 방법이 있을 수 있습니다.

## 예시: Generated Output을 Script로 확인하기

Schema가 generated type의 source-of-truth라고 가정합니다.

```text
schema/api.yaml
      │
      ↓ generate
generated/api_types.py
```

Agent가 schema를 수정했지만 generated artifact를 갱신하지 않을 수 있습니다. 이 관계가 반복적으로 문제를 만들고 기계적으로 비교하기 쉽다면 작은 check를 둘 수 있습니다.

```text
scripts/check_generated.py
        ↓
현재 source에서 다시 generate
        ↓
committed output과 비교
        ↓
차이가 있으면 결과를 보고
```

이 script가 반드시 process를 실패시킬 필요는 없습니다. Local workflow에서는 변경된 파일을 보여주는 warning으로 사용할 수 있고, PR에서는 annotation으로 노출할 수 있습니다. Repository가 generated output의 일치를 실제 필수 조건으로 취급하는 경우에만 blocking check로 사용할 수도 있습니다.

이 check는 agent에게 schema를 어떻게 설계하라고 지시하지 않습니다. **완성된 output이 source-of-truth와 일치하는지 관찰 가능한 feedback으로 바꾸는 것**이 목적입니다.

## Architecture는 한 가지 적용 사례입니다

Architecture boundary도 output에서 기계적으로 확인할 수 있다면 같은 패턴을 적용할 수 있습니다. 예를 들어 `payments`의 internal package를 외부 code가 직접 import하는지 확인할 수 있습니다.

```python
from payments.internal.stripe_client import StripeClient
```

이를 확인하는 형태는 하나로 정해져 있지 않습니다.

```text
scripts/check_architecture.py
```

처럼 dependency를 검사하는 script일 수도 있고, ecosystem이 자연스럽게 지원한다면 다음처럼 별도 structural test일 수도 있습니다.

```text
tests/
└─ architecture/
   └─ test_module_boundaries.py
```

더 좋은 language/package visibility가 이미 같은 boundary를 보장한다면 별도의 check 자체가 필요 없을 수도 있습니다.

즉 architecture는 이 패턴의 출발 사례 중 하나일 뿐, pattern의 범위나 기본 배치를 정의하지 않습니다.

## Agent Feedback Surface로 활용하기

Executable output check는 사람이 발견하기 전에 agent가 자기 변경의 일부 문제를 직접 발견하는 feedback surface가 될 수 있습니다.

```text
Agent change
    ↓
Executable check
    ↓
정보 / 경고 / 실패
    ↓
필요하면 Agent가 수정 또는 재검토
```

기능 test가 통과하더라도 generated artifact 누락, configuration drift, structural 문제처럼 다른 종류의 결함이 남을 수 있습니다. Output check는 behavior test를 대체하지 않고 **별도의 관찰 가능한 feedback**을 추가합니다.

결과는 가능하면 단순한 `false`보다 무엇이 관찰되었는지, 어느 output이 관련되는지, 다음에 무엇을 확인하면 좋은지를 드러내는 편이 유용합니다. 경고 수준의 check도 agent가 읽고 판단할 수 있도록 결과가 명확하면 가치가 있습니다.

## 비용과 수명도 함께 봅니다

Check는 한 번 추가하면 끝나는 자산이 아닙니다. 다음 비용이 따라올 수 있습니다.

- check 자체의 유지보수
- false positive와 예외 처리
- 실행 시간과 feedback noise
- 실패나 경고의 해석 비용
- tooling과 output structure 변화에 따른 갱신
- check를 만족시키기 위한 불필요한 우회 구현

따라서 새 check를 만드는 것뿐 아니라 **더 약하게 운영하거나, 더 싼 mechanism으로 옮기거나, 제거하는 선택**도 열어둡니다.

예를 들어 custom script로 확인하던 성질을 이후 compiler나 language module system이 자연스럽게 보장하게 되었다면 script를 없애는 편이 더 단순합니다. 더 이상 중요한 문제가 아니거나 warning이 계속 noise만 만든다면 severity를 낮추거나 check 자체를 제거할 수도 있습니다.

## Limits and Responses

Executable check는 **관찰 가능한 증거를 만드는 surface이지, 그 자체가 truth나 policy는 아닙니다.** 가장 위험한 실패는 check가 틀렸는데도 deterministic하게 통과하거나, 일부만 보고 전체를 보증한다고 오해하는 경우입니다.

### 기계적으로 검사되는 것만 중요해질 수 있습니다

자동화하기 쉬운 항목이 실제 software quality 전체를 대표하지는 않습니다. Design, cohesion, naming, simplicity 같은 판단은 review가 계속 필요합니다.

**대응:** check가 담당하는 범위를 machine-observable property로 좁게 보고, 결과가 깨끗하다고 해서 output 전체의 품질이 보장된다고 해석하지 않습니다.

### Deterministic한 Check도 잘못된 모델을 구현할 수 있습니다

같은 입력에서 항상 같은 결과가 나온다는 사실은 check의 판정 기준이 옳다는 뜻이 아닙니다. 잘못 이해한 요구사항, 오래된 assumption, 우연한 repository 구조를 안정된 rule처럼 코드화하면 **일관되게 틀린 feedback**을 만들 수 있습니다.

**대응:** 무엇을 보호하려는 check인지 output property를 설명할 수 있게 두고, checker 변경도 그 property가 여전히 타당한지 함께 review합니다. Reproducibility를 validity와 같은 의미로 취급하지 않습니다.

### Check가 보는 범위를 전체 Coverage로 오해할 수 있습니다

Targeted script나 incremental check는 빠른 대신 일부 path, file type, state만 볼 수 있습니다. 한 surface에서 통과했다는 사실이 다른 실행 경로나 repository 전체에서도 같은 성질이 유지된다는 뜻은 아닐 수 있습니다.

**대응:** check가 관찰하는 범위를 결과와 문맥에서 이해할 수 있게 하고, 누락 비용이 큰 경우에만 더 넓은 audit나 별도 verification을 보완적으로 고려합니다. 좁은 check를 전체 보증처럼 표현하지 않습니다.

### Check가 오래된 결정을 고착시킬 수 있습니다

처음에는 유효했던 boundary나 convention도 architecture, product 요구, tooling이 바뀌면 더 이상 최선이 아닐 수 있습니다. Check가 오래 남으면 과거의 선택이 현재의 불변 조건처럼 보이고 합리적인 변화까지 막을 수 있습니다.

**대응:** 예외가 반복되거나 check 때문에 자연스러운 변경이 계속 우회된다면 implementation보다 보호하려는 property 자체가 아직 유효한지 먼저 다시 봅니다. 필요하면 warning으로 낮추거나 범위를 바꾸거나 제거합니다.

### 예외 목록이 또 하나의 숨은 Policy가 될 수 있습니다

Allowlist, ignore path, suppression과 special case가 계속 늘어나면 check의 실제 의미가 본문보다 예외 목록에 숨어버릴 수 있습니다. 이 상태에서는 새 contributor나 agent가 왜 어떤 위반은 허용되고 다른 위반은 막히는지 이해하기 어렵습니다.

**대응:** 예외는 이유를 이해할 수 있게 두고 가능한 한 좁게 유지합니다. 예외가 반복되는 종류나 넓은 영역을 차지하기 시작하면 예외를 더 추가하기보다 check의 모델이나 적용 범위를 다시 설계하는 편이 나을 수 있습니다.

### Check가 계속 늘어나면 관리 비용과 Noise가 더 커질 수 있습니다

작은 script, lint rule, test와 warning도 쌓이면 또 하나의 복잡한 subsystem이 될 수 있습니다. 특히 의미가 약한 warning이 많아지면 중요한 signal까지 습관적으로 무시될 수 있습니다.

**대응:** 새로운 check보다 기존 mechanism으로 표현할 수 있는지 먼저 비교하고, 가치가 낮거나 중복되는 check는 만들지 않거나 정리합니다. 반복해서 무시되는 signal은 사람의 주의를 요구하기보다 삭제·통합·강도 조정을 검토합니다.

### Feedback 강도가 판정 신뢰도보다 클 수 있습니다

유용한 signal까지 모두 blocking으로 만들면 예외 처리와 우회 구현이 늘고 개발 흐름이 불필요하게 경직될 수 있습니다. 반대로 실제로 반드시 지켜야 하는 안정된 property를 계속 warning으로만 두면 중요한 실패를 놓칠 수 있습니다.

**대응:** 정보, 경고, 차단 중 **판정 신뢰도와 위반 비용에 비례하는 수준**을 선택합니다. Check의 구현 여부와 severity를 한 결정으로 묶지 않고, 운영하면서 강도를 바꿀 수 있게 둡니다.

### Check를 통과하기 위한 우회가 생길 수 있습니다

좁은 syntactic rule은 실제 품질보다 check 통과만 최적화하는 결과를 만들 수 있습니다. Rule을 피해 wrapper를 하나 더 만들거나 이름만 바꾸는 식의 변화가 반복되면 metric이나 check가 목표를 대신하기 시작한 신호일 수 있습니다.

**대응:** 가능한 한 보호하려는 output property를 직접 관찰하고, 예외와 wrapper가 계속 늘어난다면 check가 실제 문제를 잘 모델링하는지 다시 봅니다. Passing 자체를 품질 목표로 삼지 않습니다.

### Agent가 Check 자체도 수정할 수 있습니다

Agent가 output과 checker를 함께 수정할 수 있다면 warning을 없애거나 test를 약하게 만드는 변경도 가능합니다. 일반 품질 feedback에서는 review로 충분할 수 있지만, executable check만으로 독립적인 assurance가 생기는 것은 아닙니다.

**대응:** 보안, 규정, 고위험 constraint처럼 독립적인 보호가 필요한 문제는 repository permission, protected workflow, review ownership 등 해당 위험을 실제로 통제하는 mechanism에서 다룹니다.

### 실행 비용이 발견 가치보다 커질 수 있습니다

전체 repository를 매번 스캔하는 check는 작은 변경에 비해 지나치게 비쌀 수 있습니다. 느린 feedback은 agent와 사람 모두에게 iteration cost를 키우고, 결국 check를 건너뛰는 동기를 만들 수도 있습니다.

**대응:** targeted check, on-demand command, periodic audit처럼 더 싼 실행 시점을 비교하고, 항상 실행할 필요가 없는 check를 상시 gate로 만들지 않습니다. 더 싼 native mechanism이 같은 property를 보장하게 되면 custom check를 제거하는 것도 정상적인 선택입니다.

## Related Patterns

- [`Source-Mirrored Test Structure`](source-mirrored-test-structure.md)는 test와 source 사이의 탐색·grouping 관계를 다룹니다. Executable Output Checks는 어떤 output property를 기계적으로 관찰할지와 그 feedback을 다룹니다.
- [`Filesystem-Legible Structure`](filesystem-legible-structure.md)는 filesystem을 navigation cue로 활용하는 방법을 다룹니다. Check의 파일 배치는 legibility를 고려할 수 있지만 filesystem 자체가 check를 대신하지는 않습니다.

## Grounding

- [OpenAI, *Harness engineering: leveraging Codex in an agent-first world*](https://openai.com/index/harness-engineering/)는 agent-generated repository에서 dependency direction과 structural invariant를 lint와 structural test로 확인한 사례를 보여줍니다. 이 패턴에서는 이를 architecture에 한정하지 않고 **machine-observable output property를 executable feedback으로 바꾸는 한 사례**로 참고합니다.
- [Google Engineering Practices, *What to look for in a code review*](https://google.github.io/eng-practices/review/reviewer/looking-for.html)는 좋은 review가 design, complexity, naming과 test 등 기계적 검사만으로 환원되지 않는 여러 판단을 포함한다는 점을 보여줍니다. Executable check를 전체 품질 판단의 대체재로 보지 않는 경계로 참고할 수 있습니다.

## Short Form

> **작업 결과에서 반복적으로 문제를 만드는 machine-observable property를 가장 단순한 executable check로 드러내고, 상황에 맞는 위치와 강도로 feedback합니다. Check는 truth나 policy 자체가 아니며, 문제보다 비싸지면 약화·이동·제거할 수 있습니다.**
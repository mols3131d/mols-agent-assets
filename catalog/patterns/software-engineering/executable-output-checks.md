---
description: Agent나 automation의 작업 결과에서 기계적으로 관찰 가능한 부실을 실행 가능한 check로 드러내고, 적절한 실행 방식과 피드백 강도를 선택할 때 참고하는 패턴입니다.
---

# Executable Output Checks

Agent나 automation이 빠르게 결과물을 만들수록 사람이 모든 변경을 같은 깊이로 다시 확인하기는 어렵습니다. 이때 **작업 결과에서 기계적으로 관찰할 수 있는 일부 부실을 executable check로 드러내는 것**을 고려할 수 있습니다.

여기서 output은 source code만 뜻하지 않습니다. Configuration, generated artifact, manifest, 문서 projection, package/dependency structure처럼 작업 결과로 남는 여러 산출물이 대상이 될 수 있습니다.

이 패턴은 output의 품질 전체를 자동 판정하거나 모든 발견을 차단하려는 접근이 아닙니다. 핵심은 서로 다른 선택을 분리하는 것입니다.

```text
관찰할 output property
        ↓
실행 가능한 check
        ↓
실행할 surface와 시점
        ↓
적절한 feedback 강도
```

같은 check라도 필요할 때만 실행할 수 있고, 결과를 정보나 경고로 보여줄 수도 있으며, 정말 안정적이고 비용이 큰 위반만 차단할 수도 있습니다. Architecture check와 test framework는 여러 적용 형태 중 일부입니다.

## Core

Executable output check는 구현 방법을 세세하게 지시하기보다 **완성된 output에서 관찰할 수 있는 성질**을 확인합니다.

예를 들면 다음과 같습니다.

- generated output이 source-of-truth와 어긋났는가?
- 필요한 manifest나 artifact가 없거나 parse되지 않는가?
- configuration에 위험하거나 허용하지 않는 조합이 생겼는가?
- 문서나 route 같은 projection이 작성 원본과 달라졌는가?
- 특정 internal surface가 의도하지 않은 범위에서 사용되는가?
- dependency나 module boundary가 의도된 구조에서 벗어났는가?

좋은 check는 정답 구현을 강요하기보다 **관찰 가능한 문제를 사람이든 agent든 다시 판단할 수 있는 feedback으로 바꿉니다.**

### 이 패턴이 소유하지 않는 것

Executable Output Checks는 일반적인 testing strategy나 quality gate 체계 전체를 정의하지 않습니다.

- 함수와 기능의 behavior correctness를 어떻게 test할지는 해당 testing 전략이 다룹니다.
- design, naming, abstraction, readability처럼 맥락 판단이 필요한 품질은 review 영역으로 남깁니다.
- security, compliance처럼 독립적인 assurance가 필요한 constraint의 권한·보호 모델을 이 패턴이 대신하지 않습니다.
- test directory, script path, marker, CI cadence와 severity 체계를 고정하지 않습니다.

이 패턴이 다루는 것은 **작업 결과에서 비교적 명확하게 관찰할 수 있는 성질을 실행 가능한 feedback으로 만들 가치가 있는지, 있다면 어떤 형태와 강도가 적절한지**입니다.

## 무엇을 Check할지

검사할 수 있다는 이유만으로 check를 추가하지는 않습니다. **놓쳤을 때의 비용과 check 자체의 비용을 함께** 봅니다.

다음 성질이 많이 겹칠수록 executable check가 유용할 가능성이 높습니다.

- 같은 종류의 부실이 반복해서 나타나거나, 아직 반복되지 않았더라도 위반 비용이 큰 안정된 성질입니다.
- 결과를 보고 비교적 객관적으로 판정할 수 있습니다.
- 늦게 발견하면 수정 범위나 복구 비용이 커집니다.
- 관찰하려는 성질이 충분히 안정되어 있습니다.
- 결과를 보고 사람이나 agent가 다음 행동을 이해할 수 있습니다.
- 기존 mechanism이나 작은 deterministic check로 비교적 싸게 확인할 수 있습니다.

반대로 일회성이고 영향이 작은 문제, 아직 탐색 중인 설계 선택, 쉽게 고칠 수 있는 낮은 비용의 실수, 자주 바뀌는 convention은 review나 documentation에 남기는 편이 나을 수 있습니다.

사람이 review에서 같은 객관적 지적을 반복하고 있다면 check 후보인지 살펴볼 수 있습니다. 반복 이력이 없더라도 **놓쳤을 때의 비용이 크고 property가 충분히 안정적이며 값싸게 판정할 수 있다면** 후보가 될 수 있습니다. 어느 경우든 기계적 feedback이 실제 문제 비용을 줄이는지 봅니다.

## 가장 단순한 실행 방법을 선택합니다

Executable check가 반드시 test일 필요는 없습니다. 같은 output property를 더 자연스럽고 싸게 확인할 수 있는 mechanism이 있다면 그것을 사용할 수 있습니다.

대표적인 형태는 다음과 같습니다.

- language, type system, module/package visibility 같은 native constraint
- formatter, linter, schema validator, build tool처럼 이미 사용하는 도구
- 작은 script 또는 CLI command
- source-of-truth에서 다시 생성한 뒤 비교하는 generator + diff
- 일반 test 또는 structural test
- 특정 목적을 위한 작은 custom checker

예를 들어 generated artifact가 최신인지 확인하는 데 test fixture가 필요하지 않다면 `scripts/check_generated.py` 같은 독립 script가 더 단순할 수 있습니다. 반대로 확인하려는 성질이 기존 assertion이나 fixture와 자연스럽게 맞는다면 test framework에 두는 것도 좋은 선택입니다.

중요한 것은 **test인지 script인지가 아니라 해당 output property를 가장 단순하고 신뢰 가능하게 확인할 수 있는가**입니다.

판정 logic을 local script, test와 CI에 각각 복제할 필요는 없습니다. 하나의 의미를 여러 surface에서 사용해야 한다면 가능한 한 판정 logic의 owner는 하나로 두고 필요한 위치에서 호출합니다. 반대로 check가 하나뿐인데 미래 확장을 예상해 중앙 checker framework나 registry부터 만들지는 않습니다.

## 실행 결과와 Feedback을 구분합니다

Check가 실행되었다고 해서 결과가 항상 단순한 pass/fail인 것은 아닙니다. 특히 **output의 문제와 checker 자체의 실패를 섞지 않는 것**이 중요합니다.

개념적으로는 다음 상태를 구분할 수 있습니다.

| Check 결과 | 의미 |
| --- | --- |
| 확인됨 | 관찰하려던 property를 확인했고 특이사항을 찾지 못함 |
| Finding | property를 확인했고 drift, 위반 또는 검토할 항목을 발견함 |
| 판정 불가 | tool, environment, dependency 등의 이유로 property 자체를 신뢰성 있게 확인하지 못함 |

이 이름이나 세 상태를 그대로 구현할 필요는 없습니다. 핵심은 generator 실행 실패나 network 오류를 곧바로 `generated output이 잘못됨`으로 오인하지 않는 것입니다. 반대로 판정 불가를 clean result처럼 취급해서도 안 됩니다.

Finding을 어떻게 표면화할지도 별도 선택입니다.

| Feedback | 어울리는 상황 | 예시 |
| --- | --- | --- |
| 정보 / signal | 추세나 잠재적 drift를 보여주는 것만으로 가치가 있음 | dependency 변화나 generated diff를 보여줌 |
| 경고 / warning | 수정할 가치가 높지만 합리적인 예외나 맥락 판단이 남음 | deprecated internal API 사용, 권장 범위를 벗어난 config |
| 차단 / blocking | 판정 신뢰도가 높고 그대로 진행하는 비용이 큰 안정된 위반 | parse 불가능한 필수 manifest, 반드시 동기화되어야 하는 artifact |

Executable하다는 이유만으로 blocking할 필요는 없습니다. **판정 신뢰도와 위반 비용에 비례하는 최소한의 유용한 feedback**을 선택합니다.

## 실행 위치와 시점도 별도 선택입니다

하나의 check를 어디서 언제 실행할지는 구현 형태와 별개의 결정입니다.

- agent나 사람이 필요할 때 직접 실행하는 command
- local development workflow
- editor나 hook에서 주는 빠른 feedback
- test suite
- PR이나 CI의 annotation/check
- 비용이 큰 검사의 주기적 또는 수동 audit

모든 check를 PR Gate에 넣을 필요는 없습니다. 빠른 local signal이면 충분한 항목도 있고, 전체 repository나 외부 환경을 읽어야 하는 비싼 검사는 필요한 시점에만 실행하는 편이 나을 수도 있습니다.

## 대표 사례

| Output에서 관찰할 문제 | 가능한 executable form | 가능한 feedback |
| --- | --- | --- |
| generated output이 stale함 | regenerate + diff, checker script | 정보, 경고, 필요한 경우 차단 |
| manifest나 artifact 형식 오류 | parser, schema/semantic validator | 경고 또는 차단 |
| 잘못된 config 조합 | validator script, existing linter | 경고 또는 차단 |
| 작성 원본과 projection의 drift | generator + comparison | 정보 또는 경고 |
| internal API의 의도하지 않은 사용 | import/dependency checker, visibility mechanism | 경고 또는 차단 |
| architecture dependency 위반 | language rule, dependency script, structural test | 경고 또는 차단 |

이 표는 구현 계약이 아니라 선택지를 보여주는 예시입니다.

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
Finding이 있으면 보여줌
```

Local workflow에서는 diff를 warning으로 보여주고, PR에서는 annotation으로 노출할 수 있습니다. Generated output의 일치가 실제 필수 조건인 repository라면 같은 판정을 blocking check로 사용할 수도 있습니다.

Architecture boundary 역시 같은 패턴의 한 사례입니다. `payments`의 internal package를 외부에서 직접 사용하는지 `scripts/check_architecture.py`로 확인할 수도 있고, ecosystem과 test infrastructure가 자연스럽게 맞는다면 `tests/architecture/test_module_boundaries.py` 같은 structural test로 표현할 수도 있습니다. Language나 package visibility가 이미 같은 boundary를 보장한다면 별도 check가 필요 없을 수 있습니다.

## Agent Feedback Surface로 활용하기

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

기능 test가 통과해도 generated artifact 누락, configuration drift, structural 문제처럼 다른 종류의 결함이 남을 수 있습니다. 결과는 단순한 `false`보다 무엇을 관찰했고 어느 output이 관련되며 다음에 무엇을 확인하면 좋은지 드러낼수록 유용합니다.

## 비용과 수명도 함께 봅니다

Check는 한 번 추가하면 끝나는 자산이 아닙니다. 유지보수, false positive, 예외, 실행 시간, feedback noise와 tooling 변화 대응 비용이 따라옵니다.

따라서 새 check를 만드는 것뿐 아니라 **더 약하게 운영하거나, 더 싼 mechanism으로 옮기거나, 제거하는 선택**도 열어둡니다. Custom script가 지키던 성질을 이후 compiler나 language module system이 자연스럽게 보장한다면 script를 없애는 편이 더 단순합니다.

기존 repository에 이미 많은 위반이 있다면 새 check를 곧바로 blocking으로 만드는 것이 항상 좋은 시작은 아닙니다. 필요하면 먼저 signal이나 warning으로 관찰하거나, 변경된 범위에서 유용성을 확인한 뒤 적용 범위를 넓힐 수 있습니다. Baseline이나 allowlist를 사용한다면 그것 자체가 영구적인 예외 저장소가 되지 않는지도 봅니다.

## Limits and Responses

Executable check는 **관찰 가능한 증거를 만드는 surface이지, 그 자체가 truth나 policy는 아닙니다.**

### 기계적으로 검사되는 것만 중요해질 수 있습니다

자동화하기 쉬운 항목이 software quality 전체를 대표하지는 않습니다.

**대응:** check가 담당하는 범위를 machine-observable property로 좁게 보고, clean result를 design이나 readability까지 포함한 전체 품질 보증으로 해석하지 않습니다.

### Deterministic한 Check도 잘못되거나 일부만 볼 수 있습니다

같은 입력에서 같은 결과가 나온다는 사실은 판정 기준이 옳다는 뜻이 아닙니다. 잘못 이해한 요구사항이나 오래된 assumption을 일관되게 구현할 수도 있고, targeted check는 일부 path나 state만 볼 수도 있습니다.

**대응:** 무엇을 관찰하는 check인지 설명할 수 있게 두고, reproducibility를 validity나 full coverage와 같은 의미로 취급하지 않습니다. 누락 비용이 클 때만 더 넓은 verification을 보완적으로 고려합니다.

### Checker의 환경 의존성과 Flakiness가 신뢰를 깎을 수 있습니다

Network, wall-clock time, 외부 service나 불안정한 environment에 의존하는 check는 같은 output에도 다른 결과를 낼 수 있습니다. 반복되는 flaky warning과 failure는 결국 무시되기 쉽습니다.

**대응:** 가능하면 deterministic하고 재현 가능한 입력으로 판정합니다. 외부 의존성이 필요한 경우에는 output violation과 `판정 불가`를 구분하고, 신뢰도가 낮은 판정을 강한 gate로 사용하지 않습니다.

### 오래된 Rule과 예외가 숨은 Policy가 될 수 있습니다

처음에는 유효했던 boundary나 convention도 시간이 지나면 달라질 수 있습니다. Allowlist, ignore와 suppression이 늘어나면 실제 의미가 예외 목록에 숨어버릴 수도 있습니다.

**대응:** 예외나 우회가 반복되면 더 추가하기 전에 보호하려는 property 자체가 아직 유효한지 다시 봅니다. 필요하면 범위나 강도를 바꾸거나 check를 제거합니다.

### Check와 Warning이 쌓이면 비용과 Noise가 커집니다

작은 script, lint rule, test와 warning도 누적되면 별도의 subsystem이 됩니다. 의미가 약한 warning이 많으면 중요한 signal까지 습관적으로 무시될 수 있습니다.

**대응:** 기존 mechanism으로 표현할 수 있는지 먼저 비교하고, 가치가 낮거나 중복되는 check는 만들지 않거나 정리합니다. 반복해서 무시되는 signal은 삭제·통합·강도 조정을 검토합니다.

### Check 통과 자체가 목표가 될 수 있습니다

좁은 syntactic rule은 실제 품질보다 check 통과를 최적화하는 wrapper, rename과 우회 구조를 만들 수 있습니다.

**대응:** 가능한 한 보호하려는 output property를 직접 관찰하고, 우회가 반복되면 check가 실제 문제를 잘 모델링하는지 다시 봅니다. Passing 자체를 품질 목표로 삼지 않습니다.

### Agent가 Check 자체도 수정할 수 있습니다

Agent가 output과 checker를 함께 수정할 수 있다면 warning을 없애거나 checker를 약하게 만드는 변경도 가능합니다. 일반 품질 feedback에서는 review가 충분할 수 있지만 executable check만으로 독립적인 assurance가 생기지는 않습니다.

**대응:** 보안, 규정, 고위험 constraint처럼 독립 보호가 필요한 문제는 repository permission, protected workflow, review ownership 등 해당 위험을 실제로 통제하는 mechanism에서 다룹니다.

### 실행 비용이 발견 가치보다 커질 수 있습니다

전체 repository를 매번 스캔하는 check는 작은 변경에 비해 지나치게 비쌀 수 있고 느린 feedback은 check를 건너뛰는 동기를 만들 수도 있습니다.

**대응:** targeted check, on-demand command, periodic audit처럼 더 싼 실행 시점을 비교하고, 항상 실행할 필요가 없는 check를 상시 gate로 만들지 않습니다.

## Related Patterns

- [`Source-Mirrored Test Structure`](source-mirrored-test-structure.md)는 test와 source 사이의 탐색·grouping 관계를 다룹니다. Executable Output Checks는 어떤 output property를 기계적으로 관찰할지와 그 feedback을 다룹니다.
- [`Filesystem-Legible Structure`](filesystem-legible-structure.md)는 filesystem을 navigation cue로 활용하는 방법을 다룹니다. Check의 파일 배치는 legibility를 고려할 수 있지만 filesystem 자체가 check를 대신하지는 않습니다.

## Grounding

- [OpenAI, *Harness engineering: leveraging Codex in an agent-first world*](https://openai.com/index/harness-engineering/)는 agent-generated repository에서 dependency direction과 structural invariant를 lint와 structural test로 확인한 사례를 보여줍니다. 이 패턴에서는 이를 architecture에 한정하지 않고 machine-observable output property를 executable feedback으로 바꾸는 한 사례로 참고합니다.
- [Google Engineering Practices, *What to look for in a code review*](https://google.github.io/eng-practices/review/reviewer/looking-for.html)는 좋은 review가 design, complexity, naming과 test 등 기계적 검사만으로 환원되지 않는 여러 판단을 포함한다는 점을 보여줍니다. Executable check를 전체 품질 판단의 대체재로 보지 않는 경계로 참고할 수 있습니다.

## Short Form

> **작업 결과에서 반복되거나 놓쳤을 때 비용이 큰 machine-observable property를 가장 단순한 executable check로 드러내고, 상황에 맞는 위치와 강도로 feedback합니다. Check는 truth나 policy 자체가 아니며, 문제보다 비싸지면 약화·이동·제거할 수 있습니다.**

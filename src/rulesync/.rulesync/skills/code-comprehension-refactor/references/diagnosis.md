# Diagnosis

이해 비용을 code size나 style metric으로 추정하지 않는다. **독자가 현재 task에 필요한 mental model을 만들기 위해 어떤 추가 작업을 하는지**를 본다.

Core `SKILL.md`가 common-path bottleneck 판단과 preservation gate를 소유한다. 이 reference는 root cause, usage surface, abstraction value 또는 여러 cognitive cost 사이의 trade-off가 단순하지 않을 때 사용한다.

## Comprehension Cost

이 Skill에서 이해 비용은 두 축으로 본다.

- **Misunderstanding risk** — 잘못 이해하거나 misuse할 가능성과 그 영향
- **Reconstruction effort** — 올바르게 이해하기 위해 필요한 불필요한 번역, 탐색, navigation, 추론, 상태 추적과 simulation

Destructive side effect, approval·validation gate, ordering, invariant처럼 오해 영향이 큰 문제를 우선한다. 위험이 낮아도 반복적으로 읽거나 수정하는 코드에서 reconstruction effort가 크면 material한 병목일 수 있다.

코드가 짧거나 syntax가 작다는 사실은 낮은 comprehension cost의 증거가 아니다. Negative condition, overloaded boolean/sentinel, implicit precedence처럼 작은 construct도 실제 reader가 반복해서 잘못 해석한다면 material할 수 있다.

## Usage Surface

Preservation surface는 explicit function caller에 한정되지 않는다.

- public import와 direct/internal caller
- framework가 발견·호출하는 callback, hook, plugin 또는 DI entrypoint
- config, manifest, runtime registration 또는 string/dynamic lookup으로 연결되는 symbol/path
- serialization, reflection, schema, generated code 또는 naming convention이 의존하는 surface
- persisted representation이나 wire/storage shape

Rename, move, extraction, inline 또는 representation change 전에 대상 이름·경로·identity·shape가 실제 consumer에게 observable한지 확인한다.

Public/private visibility는 safety proxy가 아니다. 반대로 dynamic usage가 **가능할 수 있다는 추측만으로** 모든 local rename을 막지도 않는다. 현재 repository, framework, config와 usage evidence에서 material한 coupling 신호가 있을 때만 범위를 넓혀 본다.

## Diagnose and Intervene

| Bottleneck | Signal | Reader가 하는 추가 작업 | Typical direction |
| --- | --- | --- | --- |
| Lexical / semantic decoding | generic name, abbreviation, overloaded term, domain vocabulary와 어긋난 이름 | identifier와 실제 role/domain meaning을 번역하거나 검색 | repository-established domain term, more specific internal name/API |
| Representation | positional value, boolean/sentinel, generic container나 compact DSL이 의미를 압축 | 위치·flag·sentinel·shape 규칙을 기억하고 펼침 | named field/argument, explicit domain value, local representation simplification |
| Hidden dependency | 중요한 관계가 global/context/registration/convention에 숨어 있음 | 현재 code 밖의 관계를 찾아 연결 | 필요한 dependency/contract를 더 직접적으로 노출 |
| Control flow | nesting, compound/negative condition, mixed abstraction level이 흐름을 가림 | 가능한 실행 경로를 mental simulation | guard clause, condition naming, local flow simplification |
| State / temporal reasoning | mutation, ordering, phase 또는 mode가 의미를 바꿈 | 이전·현재·다음 state와 순서를 동시에 추적 | state owner, phase/order를 code structure에 더 직접 반영 |
| Navigation | wrapper/helper/delegation이 새 의미 없이 이동만 늘림 | 여러 symbol·file을 열어 같은 의미를 재구성 | inline, merge, needless indirection 제거 |
| Abstraction mismatch | abstraction이 domain concept보다 generic하거나 실제 문제와 멀음 | generic model을 domain model로 반복 번역 | domain-shaped API/representation, local generic layer 축소 |
| Responsibility | 서로 다른 이유로 변하는 작업이나 abstraction level이 섞임 | 부분을 분류하고 관계를 재구성 | 자연스러운 책임 경계가 있을 때만 regroup/extract |
| Noise | dead/redundant branch, stale option, boilerplate가 핵심을 가림 | 현재 behavior와 무관한 정보를 계속 필터링 | 실제로 불필요한 surface만 제거 |

한 코드가 여러 row에 걸릴 수 있다. Row 수를 score로 사용하지 않는다.

## Coherent Bottleneck

Taxonomy row는 진단 lens이지 Work unit이 아니다.

다음처럼 여러 signal이 **같은 hidden rule 또는 mental-model burden의 다른 표면**이면 하나의 coherent bottleneck으로 볼 수 있다.

- `cfg = (mode, False, None)`처럼 naming과 representation이 같은 positional/sentinel rule을 숨김
- mutable mode flag와 nested negative flow가 같은 temporal state machine을 어렵게 만듦
- wrapper chain이 generic abstraction mismatch를 만들며 동일한 domain translation을 반복시킴

반대로 단지 같은 파일에 있다는 이유로 rename, dead-code cleanup, extraction을 묶지 않는다.

판단 질문:

1. 같은 underlying rule·state·domain concept를 이해해야 이 문제들이 함께 풀리는가?
2. 한 edit만 하면 reader가 나머지 표현을 다시 decode해야 하는가?
3. edits가 함께 바뀌어야 동일한 semantic을 일관되게 표현하는가?
4. 어느 edit를 빼도 primary bottleneck이 material하게 남는가?

대부분 `아니오`라면 별도 concern이다.

## Abstraction Value Test

Abstraction은 제거 대상이 아니다. 다음 질문으로 **semantic gain이 navigation·decoding cost를 정당화하는지** 본다.

유지할 가치가 커지는 신호:

- stable domain concept에 이름을 준다.
- invariant, validation, compatibility 또는 policy를 한 곳에서 보존한다.
- 여러 caller의 반복 reasoning을 실제로 줄인다.
- volatile implementation detail을 격리한다.
- call site에서 intent를 implementation보다 더 직접적으로 보여준다.

축소를 검토할 신호:

- line/token 수만 줄이고 새 의미를 제공하지 않는다.
- wrapper를 열어도 다른 이름으로 같은 호출만 있다.
- positional/generic/boolean metadata를 숨겼을 뿐 domain meaning은 더 멀어졌다.
- 사용하려면 implementation, schema 또는 DSL rule을 먼저 열어야 한다.
- 한 번 쓰이는 abstraction이 새 concept와 navigation surface만 추가한다.

Hop count만으로 판단하지 않는다. 한 번의 이동으로 중요한 domain concept나 invariant를 얻는다면 여러 줄의 직접 코드보다 이해 비용이 낮을 수 있다.

## Local vs Broader Comprehension

Local explicitness가 repository 전체의 이해 비용을 늘릴 수 있다.

예를 들어 한 함수에서만 새로운 synonym, helper pattern 또는 representation을 만들면 그 함수는 조금 더 explicit해 보여도 reader는 기존 repository terminology와 새 local vocabulary를 함께 배워야 한다.

따라서 다음을 함께 본다.

- established domain term 또는 representation을 재사용할 수 있는가
- local rename이 repository-wide semantic consistency를 높이는가, 낮추는가
- abstraction을 없애며 duplicated policy나 repeated reasoning을 여러 caller로 퍼뜨리는가
- local navigation 감소가 global duplication/consistency cost보다 실제로 큰가

Consistency 자체도 절대 규칙이 아니다. Established pattern이 comprehension bottleneck의 원인이라면 evidence를 갖고 바꿀 수 있지만, 한 target만 새 vocabulary로 이탈하는 것을 clarity improvement로 착각하지 않는다.

## Priority

우선순위는 대략 다음 질문으로 결정한다.

1. 잘못 이해했을 때 behavior, data, invariant 또는 usage contract에 미치는 영향이 큰가?
2. 올바르게 이해하기 위해 반복적인 decoding·search·navigation·simulation이 필요한가?
3. 이 code surface가 caller·maintainer에게 자주 읽히거나 수정되는가?
4. 같은 root cause에 묶인 signal인가, 서로 독립적인 cleanup인가?
5. 병목을 줄이는 change가 observable/usage contract와 material performance를 안전하게 보존할 수 있는가?

숫자 score를 만들지 않는다. 가장 material한 **coherent bottleneck**을 먼저 해결한다.

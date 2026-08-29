# Diagnosis

이해 비용을 code size나 style metric으로 추정하지 않는다. **독자가 현재 작업에 필요한 mental model을 만들기 위해 어떤 추가 작업을 하는지**를 본다.

## Comprehension Cost

이 skill에서 이해 비용은 두 축으로 본다.

- **Misunderstanding risk** — 잘못 이해하거나 misuse할 가능성과 그 영향
- **Reconstruction effort** — 올바르게 이해하기 위해 필요한 불필요한 번역, 탐색, 추론, 상태 추적과 simulation

Destructive side effect, approval·validation gate, ordering, invariant처럼 오해 영향이 큰 문제를 우선한다. 다만 위험이 낮아도 반복적으로 읽거나 수정하는 코드에서 reconstruction effort가 크면 material한 병목일 수 있다.

## Usage Surface

Caller는 명시적인 함수 호출에 한정되지 않는다.

- public import와 직접 caller
- framework가 발견·호출하는 callback, hook, plugin entrypoint
- config나 runtime registration으로 연결되는 entrypoint
- serialization, reflection, schema 또는 naming convention이 의존하는 surface

rename, move, extraction, representation change 전에 대상 이름·경로·shape가 caller-visible contract인지 확인한다.

## Diagnose and Intervene

| Bottleneck | Signal | Reader가 하는 추가 작업 | Typical direction |
| --- | --- | --- | --- |
| Intent | 이름이나 call site만으로 목적이 불명확하다 | identifier와 domain meaning을 번역한다 | internal rename, 더 specific한 API/name |
| Representation | positional value, boolean/sentinel, generic container나 compact DSL이 의미를 압축한다 | 위치·flag·sentinel·shape 규칙을 기억하고 펼친다 | named field/argument, explicit domain value, local representation simplification |
| Hidden dependency | 중요한 관계가 global/context/registration/convention에 숨어 있다 | 현재 코드 밖의 관계를 찾아 연결한다 | 필요한 dependency나 contract를 가까운 surface에 노출 |
| Control flow | nesting, compound condition, mixed abstraction level이 흐름을 가린다 | 가능한 실행 경로를 머릿속에서 simulation한다 | guard clause, condition naming, local flow simplification |
| State / temporal reasoning | mutation, ordering, phase 또는 mode가 의미를 바꾼다 | 이전·현재·다음 state를 동시에 추적한다 | state ownership, phase/order를 더 직접적으로 표현 |
| Navigation | wrapper/helper/delegation이 새 의미 없이 이동만 늘린다 | 여러 symbol·file을 열어 같은 의미를 재구성한다 | inline, merge, needless indirection 제거 |
| Abstraction mismatch | abstraction이 domain concept보다 generic하거나 실제 문제와 멀다 | generic model을 domain model로 반복 번역한다 | domain-shaped API/representation, local abstraction 축소 |
| Responsibility | 서로 다른 이유로 변하는 작업이나 abstraction level이 섞인다 | 부분을 분류하고 관계를 다시 구성한다 | 자연스러운 책임 경계가 있을 때만 regroup/extract |
| Noise | dead/redundant branch, stale option, boilerplate가 핵심을 가린다 | 현재 behavior와 무관한 정보를 계속 필터링한다 | 실제로 불필요한 surface만 제거 |

한 코드가 여러 row에 걸릴 수 있다. row 수를 score로 사용하지 않는다.

## Abstraction Value Test

Abstraction은 제거 대상이 아니다. 다음 질문으로 **semantic gain이 navigation·decoding cost를 정당화하는지** 본다.

유지할 가치가 커지는 신호:

- stable domain concept에 이름을 준다.
- invariant, validation 또는 policy를 한 곳에서 보존한다.
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

## Priority

우선순위는 대략 다음 질문으로 결정한다.

1. 잘못 이해했을 때 behavior, data, invariant 또는 caller misuse에 미치는 영향이 큰가?
1. 올바르게 이해하기 위해 반복적인 번역·탐색·simulation이 필요한가?
1. 이 코드가 caller·maintainer에게 자주 읽히거나 수정되는가?
1. 병목을 줄이는 변경이 behavior·contract·performance를 안전하게 보존할 수 있는가?

숫자 score를 만들지 않는다. 가장 material한 bottleneck 하나를 먼저 해결한다.

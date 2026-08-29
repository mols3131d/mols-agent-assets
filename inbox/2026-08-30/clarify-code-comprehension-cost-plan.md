# Clarify Code — Comprehension Cost Improvement Plan

이 계획은 [Comprehension Cost Research](clarify-code-comprehension-cost-research.md)를 바탕으로 `clarify-code`가 **짧지만 의미 해독 비용이 큰 코드까지 안정적으로 진단하면서, 좋은 abstraction이나 compact code를 과하게 풀어쓰지 않도록** 개선하는 작업을 정의합니다.

## Goal

`clarify-code`의 기존 핵심 책임인 behavior-preserving clarification을 유지하면서 다음 behavior를 추가합니다.

1. line count와 syntactic complexity가 낮아도 **representation decoding, hidden convention, navigation, mental simulation 때문에 이해 비용이 큰 코드**를 reading bottleneck으로 인식합니다.
1. misunderstanding risk뿐 아니라 **불필요한 reconstruction effort**도 material한 comprehension debt로 판단합니다.
1. abstraction을 무조건 제거하지 않고 **제공하는 semantic value와 추가하는 navigation/decoding cost를 비교**합니다.
1. improvement는 code를 verbose하게 만드는 것이 아니라 **reader가 필요한 mental model을 더 직접적으로 만들게 하는 최소한의 coherent change**를 선택합니다.

## Preserve

이번 변경에서 다음 계약은 유지합니다.

- feature나 public behavior를 추가하지 않음
- observable behavior와 caller-visible contract 보존
- correctness review, performance optimization, system architecture redesign을 대체하지 않음
- 가장 중요한 reading bottleneck부터 bounded하게 처리
- naming/structure로 해결할 수 있는 문제를 prose로 덮지 않음
- caller contract는 docstring, maintainer-only rationale은 comment라는 현재 documentation ownership 유지
- 관련 없는 cleanup이나 future abstraction을 섞지 않음
- 변경 전후 가능한 가장 작은 validation으로 behavior 보존 확인

## Design Decisions

### `comprehension cost`를 상위 개념으로 사용한다

현재 스킬의 `오해 비용`은 중요한 우선순위 signal이지만 범위가 좁습니다. 이를 제거하지 않고 다음 관계로 확장합니다.

```text
comprehension cost
├─ misunderstanding risk
└─ reconstruction effort
```

- `misunderstanding risk`: 잘못 이해하거나 misuse했을 때의 가능성·영향
- `reconstruction effort`: 올바르게 이해하기 위해 reader가 수행해야 하는 불필요한 번역·탐색·추론·시뮬레이션

우선순위는 여전히 destructive side effect, gate, ordering, invariant처럼 영향이 큰 오해를 먼저 봅니다. 다만 그런 위험이 없다는 이유만으로 compact opaque representation을 무시하지 않습니다.

이 관계를 별도 taxonomy file이나 score model로 만들지 않고 `SKILL.md`와 `diagnosis.md`의 judgment language로만 표현합니다.

### `Representation`을 독립 bottleneck으로 추가한다

현재 `Intent`, `Caller contract`, `Rationale`, `Responsibility`, `Control flow`, `Navigation`만으로는 compact schema/contract/config의 문제를 안정적으로 포착하기 어렵습니다.

`diagnosis.md`에 다음 계열을 추가합니다.

| Bottleneck | Signal | Smallest useful intervention |
| --- | --- | --- |
| Representation | positional value, boolean/sentinel, generic container/DSL 등이 domain meaning을 압축해 reader가 hidden convention을 복원해야 함 | named field/argument, explicit domain value, local representation simplification |

구체적인 wording은 구현 후 전체 table의 abstraction level과 길이에 맞춰 다듬습니다.

### `Navigation`은 hop count가 아니라 semantic gain으로 판단한다

현재의 “abstraction이 의미보다 navigation cost를 더 만들면 축소한다”는 원칙을 보존하되 다음 의미로 정밀화합니다.

- hop이 있어도 stable domain concept, invariant, reuse, encapsulation을 제공하면 유지 가능
- wrapper/helper를 열어도 새 의미가 거의 없고 다시 이동해야 한다면 축소 후보
- abstraction이 제공하는 semantic gain보다 navigation + decoding cost가 큰지를 판단

이를 통해 “helper가 있으니 inline” 같은 기계적인 behavior를 막습니다.

### `smallest change`를 conceptual surface 기준으로 보정한다

`smallest intervention`은 줄 수가 가장 적게 바뀌는 solution이 아닙니다.

예를 들어 positional tuple의 의미를 comment 한 줄로 설명하는 것이 diff는 작지만, 모든 reader가 계속 tuple contract를 해독해야 한다면 병목을 제거하지 못합니다. 반대로 새 class를 만드는 것도 지나친 solution일 수 있습니다.

판단은 다음과 같이 둡니다.

> 현재 병목을 실질적으로 제거하면서 behavior와 contract를 보존하고, 새 conceptual surface를 가장 적게 추가하는 변경을 선택한다.

### Architecture boundary와 local de-abstraction을 분리한다

`architecture redesign` 제외는 유지합니다. 대신 다음 local change가 clarification scope에 포함될 수 있음을 명확히 합니다.

- needless local indirection 제거
- opaque local representation을 domain-shaped representation으로 변경
- generic local wrapper를 더 직접적인 code/API로 축소
- caller-visible behavior를 바꾸지 않는 local extraction/inlining/regrouping

System-level component boundary, dependency architecture, public API redesign처럼 behavior/architecture decision이 주목적인 변경은 계속 out of scope입니다.

## Planned Changes

### 1. `src/rulesync/.rulesync/skills/clarify-code/SKILL.md`

**목적:** 항상 로드되는 core에서 이번 failure mode를 인식할 최소 signal을 제공합니다.

변경 후보:

- 첫 문장의 `오해 비용` 중심 표현을 `이해 비용` 중심으로 확장
- caller/maintainer가 필요한 mental model을 과도한 해석 없이 형성해야 한다는 목적을 명확히 함
- Workflow 진단 단계에서 다음을 함께 보게 함
  - misunderstanding impact
  - hidden decoding/reconstruction effort
  - 자주 반복되는 reading cost
- “짧거나 syntax가 단순해도 hidden convention을 복원해야 하면 bottleneck이 될 수 있음”을 짧게 명시
- local representation/indirection simplification이 architecture redesign과 다름을 Boundary에서 보정
- `smallest`를 line count로 오해하지 않도록 최소한의 calibration 추가

**하지 않을 것:** comprehension taxonomy 전체나 긴 예시는 `SKILL.md`에 넣지 않습니다. 항상 로드되는 context를 늘리지 않기 위해 상세 판단은 `diagnosis.md`가 소유합니다.

### 2. `src/rulesync/.rulesync/skills/clarify-code/references/diagnosis.md`

**목적:** comprehension cost의 실제 진단과 intervention 선택을 소유합니다.

변경 후보:

- `Representation` bottleneck 추가
- 현재 `Navigation` row를 semantic gain 대비 indirection cost 관점으로 보강
- bottleneck priority 문구를 `misunderstanding impact` + `reconstruction effort`로 확장
- abstraction value test 추가
  - stable domain concept인가
  - invariant/validation을 보존하는가
  - repeated reasoning을 줄이는가
  - volatile implementation detail을 격리하는가
  - 이런 benefit이 navigation/decoding cost보다 큰가
- intervention ladder를 짧게 보강
  - naming/specific value
  - named representation
  - local flow/structure simplification
  - needless indirection removal
  - extraction은 실제 책임 경계가 있을 때만
  - prose는 code로 표현할 수 없는 contract/rationale에만

필요하면 calibration example을 2–3개만 둡니다. 예시는 rule을 대신하지 않고 이번 실제 failure와 near-miss를 구분하는 역할만 합니다.

### 3. `references/documentation.md`

기본 계획은 **변경 없음**입니다.

현재 문서는 이미 다음을 올바르게 소유합니다.

- code/name으로 표현 가능한 정보는 prose로 반복하지 않음
- caller-visible hidden contract만 docstring으로 projection
- maintainer-only code-local 이유는 comment

Implementation review에서 새 diagnosis와 실제 contradiction이 발견될 때만 최소 수정합니다.

### 4. `references/validation.md`

기본 계획은 **변경 없음**입니다.

현재 behavior envelope와 before/after validation contract가 local representation refactor에도 충분히 적용됩니다. 새 validation machinery를 Skill package 안에 추가하지 않습니다.

### 5. `evals/skills/clarify-code/cases.json`

이번 failure는 실제 사용에서 확인된 behavior gap이므로 repository-owned capability fixture를 추가할 가치가 있습니다.

초기에는 **capability eval**로 취급합니다. 아직 runtime 반복 evidence가 없으므로 merge-blocking regression contract라고 부르지 않습니다.

예상 case:

| Case | Expected behavior |
| --- | --- |
| positional contract object | 짧더라도 `Representation`/decoding bottleneck으로 인식 |
| boolean/sentinel-heavy config | flag/sentinel 의미를 더 direct한 representation으로 만들지 검토 |
| comment-only patch temptation | representation으로 해결 가능하면 comment-only fix를 우선하지 않음 |
| clear named compact structure | 짧다는 이유로 expand하거나 새 abstraction을 만들지 않음 |
| valuable domain abstraction | invariant/domain concept를 보존하는 abstraction 유지 |
| meaningless one-use wrapper | semantic gain이 없으면 inline/merge 후보로 판단 |
| complex nested control flow | 기존 Control flow behavior 유지 |
| caller-visible public contract | clarification 명목으로 public contract를 깨지 않음 |
| architecture redesign request | Skill scope를 system architecture redesign으로 확대하지 않음 |

Assertion은 특정 문장이나 exact refactoring을 고정하지 않고 **진단·보존 경계·intervention direction**을 검사합니다.

### 6. Generated discovery artifacts

Canonical Skill의 `description`이 바뀌면 route projection도 갱신될 수 있습니다. Generated file은 직접 편집하지 않고 repository-native `mise run generated-sync`를 사용합니다.

## Candidate Behavior Examples

아래 예시는 구현 방향을 고정하는 template이 아니라 positive/near-miss calibration입니다.

### Positive: compact하지만 decoding-heavy

```python
contract = Contract(
    ("id", str, True),
    ("state", State, False),
    ("ttl", int, None),
)
```

`True`, `False`, `None`과 tuple position의 의미를 다른 definition에서 반복해서 복원해야 한다면 clarification 후보입니다.

가능한 intervention은 context에 따라 다릅니다.

- named field
- keyword/named argument
- enum/specific domain value
- constructor/API가 이미 지원한다면 더 explicit한 existing representation

새 dataclass/class를 만드는 것이 항상 답은 아닙니다.

### Near miss: compact하고 이미 domain-shaped

```python
RetryPolicy(
    max_attempts=3,
    backoff=EXPONENTIAL,
    retry_on=TRANSIENT_ERRORS,
)
```

각 값의 role이 call site에서 드러나고 domain contract를 자연스럽게 표현한다면 line 수를 늘리거나 wrapper를 제거할 이유가 없습니다.

### Near miss: abstraction이 비용을 지불할 가치가 있음

```python
if policy.can_publish(change):
    publish(change)
```

`can_publish`가 stable policy boundary와 invariant를 캡슐화한다면 implementation을 inline해서 “explicit”하게 만드는 것이 오히려 comprehension cost를 키울 수 있습니다.

## Acceptance Criteria

### Recall

- compact positional/flag/sentinel representation을 실제 reading bottleneck 후보로 인식함
- misunderstanding risk가 낮아도 반복적인 reconstruction effort가 material하면 개선을 고려함
- long/nested code뿐 아니라 small confusing pattern도 scope에 들어옴

### Precision

- line count, tuple/dict/lambda/DSL 사용 자체를 문제로 보지 않음
- clear compact code를 억지로 verbose하게 만들지 않음
- stable domain abstraction과 invariant-owning abstraction을 보존함
- comment/helper/class를 readability ceremony로 추가하지 않음

### Boundary

- observable behavior와 caller-visible contract 보존
- local de-abstraction과 system architecture redesign을 구분
- correctness/performance/feature work로 scope가 확장되지 않음
- unrelated cleanup을 섞지 않음

### Operability

- reader가 diagnosis taxonomy를 외우지 않아도 core workflow에서 representation decoding을 발견할 수 있음
- 상세 판단은 `diagnosis.md`에 있어 always-loaded `SKILL.md`가 불필요하게 커지지 않음
- 같은 원칙을 `coding-context`와 중복 정의하지 않고 `clarify-code`에 필요한 operational delta만 둠

## Validation Plan

구현 후 다음 순서로 검증합니다.

1. 변경된 canonical Skill과 references를 전체 재독해 responsibility·routing·boundary contradiction 확인
1. capability fixture의 positive / near-miss / negative case를 semantic review
1. `mise run format-changed`
1. `mise exec -- npm run rulesync:doctor` 또는 현재 repository policy가 요구하는 대응 Rulesync validation
1. `mise run test`
1. `description` 또는 generated discovery가 영향받으면 `mise run generated-sync` 후 generated diff 검토
1. 현재 snapshot에서 `clarify-code` behavior를 다시 simulated review하여 Recall / Precision / Boundary를 각각 확인

Runtime/model eval을 실제로 실행하지 않았다면 runtime behavior가 검증됐다고 표현하지 않습니다.

## Review Lenses

Implementation 후 최소 다음 관점으로 재리뷰합니다.

### Under-correction

- `Representation` row만 추가되고 core workflow가 여전히 위험한 오해만 우선하여 실제 compact contract를 놓치지 않는가?
- `unnecessary indirection` wording만 바뀌고 semantic decoding을 독립적으로 보지 못하지 않는가?

### Over-correction

- compact code를 모두 verbose하게 만들도록 유도하지 않는가?
- abstraction 제거가 default가 되지 않는가?
- named object/helper를 무분별하게 추가하지 않는가?

### Duplication

- `coding-context`의 KISS/explicitness 원칙을 그대로 복제하지 않는가?
- `documentation.md`의 prose ownership을 다시 정의하지 않는가?
- Research 문서의 taxonomy 전체가 runtime Skill에 불필요하게 복사되지 않는가?

### Behavioral fidelity

- caller-visible contract와 runtime registration을 보존하는가?
- behavior-preserving clarification이라는 Skill의 정체성이 유지되는가?

## Expected File Scope

기본 예상 변경 범위:

```text
src/rulesync/.rulesync/skills/clarify-code/
├── SKILL.md
└── references/
    └── diagnosis.md

evals/skills/clarify-code/
└── cases.json

route/...                    # generated, description 변경 시 필요한 projection만
.agents/route/...            # generated, 영향이 있을 때만
```

`documentation.md`, `validation.md`, 새 script, schema, analyzer, dedicated runtime framework는 material한 추가 근거가 생기지 않는 한 변경하지 않습니다.

## Stop Conditions

다음이 모두 만족되면 implementation loop를 종료할 수 있습니다.

- 실제 failure인 compact contract case를 진단할 수 있음
- clear compact code와 valuable abstraction near-miss를 구분함
- core Skill이 불필요하게 길어지지 않음
- 새 taxonomy/framework가 아니라 기존 diagnosis owner의 작은 확장으로 해결됨
- behavior/public contract 보존 경계가 유지됨
- 적용 가능한 deterministic checks가 통과하거나 미실행 한계가 명시됨
- 추가 loop가 새로운 material finding을 만들 가능성이 낮음

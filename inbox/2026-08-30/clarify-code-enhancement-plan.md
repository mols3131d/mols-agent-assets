# Clarify Code — Enhancement Plan

이 계획은 [Clarify Code Enhancement Research](clarify-code-enhancement-research.md)의 초안을 심층 조사로 검증한 뒤 갱신한 구현 계획입니다.

## Decision

`clarify-code`를 크게 확장하거나 새 reference를 추가하지 않습니다.

현재 responsibility split을 유지하면서 다음 세 판단만 더 명확하게 만듭니다.

1. **Explanation Value** — 설명이 실제로 어떤 추론·탐색·오해 비용을 제거하는가?
2. **Information Type** — caller contract인지, maintainer constraint/consequence/rationale인지?
3. **Placement and Scope** — 그 의미가 적용되는 가장 적절하고 안정적인 source surface는 어디인가?

핵심 목표는 comment/docstring 수를 늘리는 것이 아니라 **불필요한 explanation도 comprehension cost라는 사실을 Skill behavior에 반영하는 것**입니다.

## Preserve

다음 responsibility split은 변경하지 않습니다.

| Surface | Owner |
| --- | --- |
| executable code의 representation, naming, flow, state, indirection, abstraction | `code-comprehension-refactor` |
| code-adjacent docstring, comment, module-level explanation | `clarify-code` |
| user-facing guide, README, standalone documentation | 별도 document capability |

`clarify-code`는 executable statement, identifier, type/signature, representation, control/state flow와 abstraction을 변경하지 않습니다.

## Research-Driven Design

### Explanation Value

Comment가 있다는 사실은 improvement가 아닙니다. 연구에서는 comment의 comprehension impact가 snippet마다 좋아지거나 나빠졌고, comment가 상당한 visual attention을 소비했습니다.

따라서 설명을 추가하거나 유지하기 전에 다음을 판단합니다.

- 이 설명이 없으면 reader가 무엇을 추론하거나 찾아야 하는가?
- 그 inference/search/misunderstanding cost가 material한가?
- explanation이 실제로 그 비용을 줄이는가?
- code, name, type 또는 이미 가까이 있는 contract가 같은 정보를 충분히 전달하는가?
- 설명이 추가하는 reading, attention, maintenance, stale risk보다 이익이 큰가?

실제 score를 계산하지 않습니다.

No-op, redundant prose 제거, stale prose 교정도 정상적인 성공 결과입니다.

### Information Type

`what vs why`만으로 판단하지 않고 reader가 필요로 하는 정보 유형을 더 구체적으로 봅니다.

#### Caller-facing docstring

좋은 후보:

- hidden contract
- boundary condition / call restriction
- non-obvious input/output semantics
- externally visible side effect
- exception meaning
- overwrite / idempotency / caching semantics
- protocol/framework constraint 중 caller가 알아야 하는 부분

Implementation algorithm과 source-only reasoning은 넣지 않습니다.

#### Maintainer-facing comment

좋은 후보:

- invariant / constraint
- ordering consequence
- external system limitation
- intentional unusual implementation choice
- 더 단순해 보이는 alternative가 현재도 유효한 constraint 때문에 잘못되는 이유

마지막 항목은 **durable negative knowledge**로 취급합니다. 과거에 alternative를 검토했다는 history 자체가 아니라 미래 maintainer가 다시 시도할 가능성이 높고 현재 constraint가 여전히 유효할 때만 남깁니다.

### Placement and Scope

Locality는 절대적인 “바로 위에 comment를 둔다” 규칙이 아닙니다.

의미의 실제 scope와 owner를 맞춥니다.

| Meaning | Preferred surface |
| --- | --- |
| 한 API의 caller contract | 해당 docstring |
| 한 branch/statement/order의 local rationale | 해당 code 근처 comment |
| file 전체에 안정적으로 적용되는 local convention | module-level explanation |
| 여러 module에 걸친 architecture/domain policy | canonical owner; source에는 필요한 projection만 |

판단 기준:

- reader가 explanation과 대상 code의 관계를 다시 탐색해야 하는가?
- comment scope가 실제 invariant보다 넓게 읽히는가?
- 여러 local comment에 같은 context를 복제하고 있는가?
- 더 넓은 stable owner가 semantic을 더 정확히 소유하는가?

### Stability

Comment의 길이보다 **어떤 semantic에 결합되어 있는가**를 봅니다.

선호:

- durable invariant
- current external constraint
- caller-visible contract
- current rejected-alternative constraint

경계:

- line-by-line implementation narration
- identifier spelling 반복
- temporary algorithm step
- historical discussion/log
- local source에 복제한 broad policy

Code-comment inconsistency 연구를 근거로 automated checker를 만들지는 않습니다. `clarify-code`가 변경하는 prose가 현재 code/contract와 맞고 쉽게 fragile해지지 않는지 review하는 수준으로 둡니다.

## Exact Change Set

### 1. `src/rulesync/.rulesync/skills/clarify-code/SKILL.md`

**작은 보강만 합니다.**

현재 activation과 mutation boundary는 이미 충분히 명확하므로 frontmatter `description`은 기본적으로 변경하지 않습니다.

Workflow의 prose 판단 단계에 다음 의미를 짧게 흡수합니다.

- 설명을 추가하는 것이 목적이 아니며, 먼저 어떤 non-obvious comprehension cost를 제거할지 확인
- explanation이 code/name/type을 반복하거나 읽는 비용만 늘리면 no-op 또는 제거
- 상세 placement/scope 판단은 `Documentation` reference에 위임

Stop condition도 필요하면 한 문장 보강합니다.

> 추가 prose가 제거하는 comprehension cost보다 읽기·유지 비용이 크면 추가하지 않는다.

항상 로드되는 core에 taxonomy나 연구 detail을 넣지 않습니다.

### 2. `src/rulesync/.rulesync/skills/clarify-code/references/documentation.md`

주요 변경 owner입니다.

#### 새 section: `Explanation Value`

Docstrings 앞에 짧게 추가합니다.

판단 순서:

1. reader가 code만으로 복원하기 어려운 non-obvious meaning을 특정
2. explanation이 제거할 inference/search/misunderstanding cost를 확인
3. code/name/type으로 이미 충분한 정보면 prose를 추가하지 않음
4. explanation 자체의 attention/stale cost보다 가치가 있을 때만 유지

Formula나 score는 넣지 않습니다.

#### 새 section: `Placement and Scope`

Module-Level Explanation 또는 Contract Projection과 중복되지 않게 통합합니다.

핵심:

- 의미가 local하면 가까운 surface를 선호
- 실제 scope보다 넓게 읽히는 comment를 피함
- 여러 symbol에 걸친 stable policy를 local comment마다 복제하지 않음
- 가까움보다 owner correctness가 우선하며 broad policy는 canonical owner에 둠

#### `Comments` section 보강

현재 좋은 대상 목록을 다음 관점으로 조정합니다.

- policy/invariant 적용 이유 → invariant / constraint
- 비자명한 예외 처리 이유 → failure/consequence
- 순서가 중요한 이유 → ordering consequence
- 외부 시스템 제약 → external constraint
- 의도적 특이 구현 → intentional choice
- 더 단순해 보이는 대안을 사용하지 못하는 local constraint → durable rejected alternative / negative knowledge

`why`를 제거하지 않되 이 구체적인 meaning이 판단 owner가 되게 합니다.

#### `Final Pass` 보강

다음 질문을 추가하거나 기존 질문과 통합합니다.

- 이 설명이 없으면 reader는 무엇을 추론하거나 찾아야 하는가?
- 설명이 그 비용을 실제로 줄이는가?
- 의미가 적용되는 scope와 위치가 맞는가?
- current code/contract와 모순되는가?
- implementation detail이나 identifier에 불필요하게 결합되어 fragile한가?
- 미래 maintainer가 자연스럽게 시도할 잘못된 alternative를 예방하는 durable constraint인가?

질문 수를 무작정 늘리지 않고 기존 duplicate를 합쳐 6–8개 수준으로 유지합니다.

### 3. `evals/skills/clarify-code/cases.json`

현재 7개 case는 유지합니다.

추가 후보는 **4개**로 제한합니다.

#### `no-net-value-comment`

Prompt:

> Code와 naming이 이미 명확하지만 readability를 위해 설명 comment를 하나 더 달아달라.

Expected:

- explanation이 제거할 non-obvious cost가 없으면 no-op
- comment quantity를 quality proxy로 사용하지 않음

#### `durable-rejected-alternative`

Prompt:

> 더 단순한 caching 방법이 보이지만 same-request permission visibility invariant 때문에 사용할 수 없다. Code는 현재 적절하다.

Expected:

- current constraint와 consequence를 가까운 comment로 설명 가능
- 과거 discussion/history dump를 만들지 않음

#### `placement-scope`

Prompt:

> 특정 branch의 ordering rationale를 module docstring에 길게 설명해달라.

Expected:

- local rationale는 해당 code 가까운 surface를 선택
- module 전체 rule처럼 scope를 확대하지 않음

#### `stale-implementation-narration`

Prompt:

> Comment가 old identifier와 예전 algorithm step을 설명하지만 실제 invariant는 여전히 존재한다.

Expected:

- stale narration을 그대로 polishing하지 않음
- 현재 durable invariant/constraint 중심으로 교정하거나 불필요하면 제거
- executable code는 변경하지 않음

추가 case가 기존 case와 실질적으로 중복되면 합칩니다. Fixture 수 자체가 목표가 아닙니다.

## What Not to Change

### 새 reference를 만들지 않는다

`comment-design.md`, `explanation-value.md`, `placement.md` 같은 새 reference는 현재 필요하지 않습니다.

모두 같은 activation과 mutation surface를 공유하며 `documentation.md`에서 함께 읽히는 판단입니다. SRP를 파일 수로 해석하지 않습니다.

### frontmatter routing을 넓히지 않는다

현재 `clarify-code` description은 docstring/comment/module-level explanation과 주요 hidden meaning을 충분히 표현합니다.

이번 enhancement가 discovery scope를 바꾸는 것은 아니므로 description 변경은 기본적으로 하지 않습니다. 따라서 이 계획대로라면 generated `route/skills.jsonl` update도 필요하지 않을 가능성이 높습니다.

### comment smell taxonomy를 복제하지 않는다

외부 연구의 obvious, vague, irrelevant, non-local, too-much-information taxonomy 전체를 Skill에 넣지 않습니다.

현재 Skill behavior에 필요한 local delta만 흡수합니다.

- redundant/obvious → existing rule + Explanation Value
- non-local → Placement and Scope
- misleading/stale → Final Pass consistency/stability
- too much information → net value + proper owner

### automated comment quality machinery를 만들지 않는다

- quality score
- comment density target
- stale-comment detector
- linter/analyzer

이번 observed need에 비해 과합니다.

## Review Gates

### Responsibility

- executable code를 변경하지 않는가?
- structural opacity를 prose로 보상하지 않고 `code-comprehension-refactor`로 넘기는가?
- standalone documentation 책임을 가져오지 않는가?

### Recall

- caller가 실제로 알아야 할 hidden contract를 놓치지 않는가?
- maintainer가 현재 invariant/constraint/order consequence를 복원해야 하는 경우 comment를 고려하는가?
- durable rejected alternative를 useful negative knowledge로 인식하는가?

### Precision

- obvious code에 comment를 추가하지 않는가?
- “왜”라는 이유만으로 저가치 rationale를 남기지 않는가?
- non-local/long comment를 기계적으로 제거하지 않는가?
- broad policy를 local source에 복제하지 않는가?
- history를 current invariant처럼 기록하지 않는가?

### Stability

- code와 explanation이 모순되지 않는가?
- comment가 volatile identifier/implementation detail을 불필요하게 복제하지 않는가?
- meaning scope와 explanation scope가 맞는가?

### Context Economy

- 항상 로드되는 `SKILL.md`가 불필요하게 커지지 않는가?
- 상세 judgment는 기존 `documentation.md` 한 곳에서 소유하는가?
- 같은 의미를 여러 section에서 반복하지 않는가?

## Validation Plan

구현 후 다음 순서로 확인합니다.

1. `SKILL.md`와 `documentation.md`를 함께 읽어 responsibility와 terminology 일치 확인
2. `code-comprehension-refactor`와 overlap review
3. capability fixture positive/negative semantic review
4. `route/skills.jsonl` diff가 생기지 않아야 하는지 확인; frontmatter를 변경하지 않으면 generated route update 불필요
5. repository deterministic test / PR Gate
6. 가능하면 model/runtime capability eval

Runtime eval을 실행하지 않으면 fixture 존재와 semantic review만 보고하고 runtime pass를 주장하지 않습니다.

## Acceptance Criteria

완료 상태는 다음과 같습니다.

- `clarify-code`가 comment/docstring 추가 자체를 improvement로 보지 않음
- explanation이 제거할 inference/search/misunderstanding cost를 먼저 판단함
- 필요한 contract/rationale는 information type과 실제 scope에 맞는 surface에 위치함
- comment가 constraint/consequence/invariant/negative knowledge를 전달하고 code narration을 늘리지 않음
- stale implementation narration을 polishing하지 않고 current durable meaning으로 교정하거나 제거함
- long/non-local comment를 단순 규칙으로 판단하지 않고 owner와 scope로 판단함
- `code-comprehension-refactor`와 mutation responsibility가 겹치지 않음
- 새 reference, score, analyzer 없이 기존 package를 고도화함

## Planned Diff

```text
src/rulesync/.rulesync/skills/clarify-code/
├── SKILL.md                         # small behavior calibration
└── references/
    └── documentation.md             # main enhancement

evals/skills/clarify-code/
└── cases.json                       # + bounded capability cases
```

`description`을 변경하지 않는 한 generated route는 변경하지 않습니다.

## Research Basis

이번 계획은 다음 근거를 반영합니다.

- comments의 comprehension effect는 context-dependent이며 comment 자체가 attention을 소비함
- relevant information을 적절한 위치에서 제공하면 information-seeking/cognitive cost를 줄일 수 있음
- obvious, misleading, vague, non-local, too-much-information comment가 실제 품질 문제로 관찰됨
- comment quality는 단일 metric이 아니라 consistency, completeness, readability 등 여러 속성을 가짐
- rationale에서 constraints, alternatives, side effects 같은 정보는 개발자가 필요하지만 찾기 어려움
- code-comment inconsistency와 fragile comment는 stale prose의 maintenance risk를 보여줌
- API docstring은 caller-facing implementation-independent contract와 자연스럽게 연결됨

세부 source와 limitation은 Research 문서가 소유하며 Skill 본문에는 복제하지 않습니다.

## Status

Deep-research plan complete. 다음 단계는 이 범위대로 Implementation → Review이며, 조사 결과 추가 package나 architecture가 필요하다는 근거는 발견되지 않았습니다.

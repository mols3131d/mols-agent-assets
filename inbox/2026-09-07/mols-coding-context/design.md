# `mols-coding-context*` 설계

이 문서는 `mols-coding-context`와 `mols-coding-context-python`의 responsibility, activation, family-local composition, rule admission과 content boundary를 정의한다. 실제 `SKILL.md` 작성은 후속 구현에서 수행한다.

## Goal

Coding agent가 코드를 생성·수정·리뷰·설명할 때 필요한 engineering judgment를 **작고 선택 가능한 instruction context**로 제공한다.

목표는 새로운 coding workflow를 만드는 것이 아니다.

```text
applicable authority
        ↓
frontmatter discovery
        ↓
mols-coding-context
        ↓
Python semantics가 material하면
mols-coding-context-python
        ↓
concrete task execution
        ↓
repository-native verification
```

다른 Skill family가 현재 task에 함께 필요하면 모델/하네스가 그 Skill의 frontmatter를 별도로 보고 독립 선택한다. `mols-coding-context*`가 다른 Skill을 호출·참조·로드하지 않는다.

## Family boundary

같은 prefix와 책임 계층을 가진 다음 둘만 하나의 family로 본다.

```text
mols-coding-context
mols-coding-context-python
```

Family 내부에서는 base/overlay 관계를 명시할 수 있다.

Family 밖에서는 다음을 하지 않는다.

- 다른 Skill을 prerequisite로 선언
- 다른 Skill 이름을 body에서 route 대상으로 나열
- 다른 Skill의 reference를 읽으라고 지시
- 다른 Skill의 lifecycle을 신규 family가 소유
- cross-family compatibility layer 생성

Composite task의 multi-selection은 router/model의 책임이다.

## Why Skill routing

Coding context의 적용 여부는 path만으로 안정적으로 결정되지 않는다.

- 같은 repository에서도 code implementation과 PR metadata 작업은 다르다.
- 같은 `.py` file이라도 runtime semantics를 수정하는 작업과 문서 예시를 옮기는 작업은 다르다.
- task가 code review, implementation, refactor, debugging 중 무엇인지에 따라 필요한 judgment가 달라진다.

따라서 model-selected Skill의 semantic routing을 사용한다.

Canonical Skill의 `name`·`description`이 discovery signal이므로 **selection 전에 필요한 trigger와 near-miss boundary를 frontmatter에 둔다.** Body에만 activation 조건을 숨기지 않는다.

## Frontmatter design

### `mols-coding-context`

Recommended draft:

```yaml
---
name: mols-coding-context
description: >-
  Baseline engineering judgment for any task whose active work surface materially
  includes executable code or code-facing software contracts, including code
  analysis or explanation, implementation, modification, debugging, testing,
  refactoring, review, API or data-model changes, dependency decisions,
  performance work, and maintainability work. Select even for simple or routine
  coding tasks and independently alongside any other task-relevant Skill. This
  Skill adds coding judgment only and does not own the task workflow. Do not
  select for pure factual programming lookup, repository administration with no
  code-facing work, or non-code writing where code is incidental.
---
```

### Trigger intent

High recall이 우선이다. 다음 code-facing work는 난이도와 관계없이 baseline 후보가 된다.

- code analysis/explanation with engineering judgment
- implementation/modification/debugging
- tests/refactor/review
- API/data model/dependency decision
- performance/maintainability

False positive를 줄이는 핵심 negative는 세 가지다.

- pure factual programming lookup
- repository administration with no code-facing work
- non-code writing where code is incidental

`independently alongside any other task-relevant Skill`은 다른 Skill을 참조하지 않고 router의 multi-selection을 허용한다는 신호다.

### `mols-coding-context-python`

Recommended draft:

```yaml
---
name: mols-coding-context-python
description: >-
  Python-specific coding judgment overlay. Select together with
  mols-coding-context whenever the active work materially depends on Python code,
  Python runtime semantics, or Python-facing tests, especially for exception and
  failure semantics, asyncio or concurrency and cancellation, dynamic data
  boundaries, subprocess or dynamic execution, and Python-specific generated-code
  risks. Do not select merely because a repository contains incidental Python
  files or tooling, or because Python is mentioned without code-facing work.
  Adds Python-specific judgment only; exact API and version behavior remains with
  current project and runtime authority.
---
```

`mols-coding-context` 직접 언급은 같은 family의 base/overlay contract이므로 허용한다.

### Python trigger intent

Positive signal:

- Python code or Python-facing test가 active mutation/review surface
- Python runtime behavior가 결과를 바꿈
- exception/fallback semantics
- `asyncio`, cancellation, task lifetime
- dynamic Python boundary/coercion/defaulting
- subprocess/shell/dynamic execution
- Python generated-code quality review

Near-miss:

- repository에 incidental Python tooling만 존재
- Python이 문서나 PR title에만 등장
- Python snippet을 단순 인용/포맷
- factual language comparison

Path는 supporting signal일 수 있지만 selection authority는 task semantics다.

## Frontmatter optimization principles

### Put selection evidence in `description`

Model/harness가 body를 읽기 전에 선택해야 하므로 다음 정보는 frontmatter가 소유한다.

- 무엇을 제공하는가
- 어떤 active work에서 선택하는가
- 중요한 positive examples의 semantic category
- realistic near-miss
- workflow owner가 아니라는 boundary
- 같은 family dependency가 있으면 그 관계

### Do not encode procedure in `description`

Frontmatter는 router다. 다음은 넣지 않는다.

- implementation steps
- validation checklist
- exhaustive smell catalog
- specific command
- long policy rationale

### Prefer semantic phrases over brittle keywords

`Python`, `asyncio`, `review` 같은 단어가 등장했다고 바로 trigger하지 않는다. `active work materially depends on ...`처럼 실제 task relation을 표현한다.

### Preserve independent multi-selection

Base description은 다른 task-relevant Skill과 독립적으로 함께 선택될 수 있음을 알리되 다른 Skill 이름을 나열하지 않는다.

Family 밖의 Skill과 composition을 body contract로 만들지 않는다.

## Rule application model

Skill selection과 rule application은 다르다.

```text
Skill selected
≠ every rule applies
≠ every nearby code smell must be changed
```

현재 target, change와 failure path에 material한 rule만 적용한다.

예:

- Python Skill이 선택됐지만 async code가 없음 → async rule은 행동을 만들지 않음
- remote call이 있어도 retry requirement가 없음 → retry mechanism을 자동 추가하지 않음
- trusted internal typed object → external validation layer를 억지로 추가하지 않음
- comment-only edit → unrelated runtime refactor로 확대하지 않음

이 gate가 없으면 context가 checklist가 되어 YAGNI를 위반한다.

## `mols-coding-context`

### Responsibility

Language-independent coding judgment와 agent-generated software의 stable failure-prevention invariant를 소유한다.

### Authority and fit

- explicit requirement, repository contract, observable compatibility, safety/security와 target runtime constraint가 general preference보다 우선한다.
- existing boundary, caller, data flow, failure behavior, tests와 local convention을 필요한 만큼 확인한다.
- materially equivalent하면 established local/default option을 우선한다.
- local code problem을 evidence 없이 architecture problem으로 확대하지 않는다.

### Minimum sufficient complexity

- smallest coherent change를 선호한다.
- shorter code, fewer classes/helpers 자체를 simplicity evidence로 사용하지 않는다.
- abstraction은 stable concept, invariant, ownership 또는 repeated reasoning을 실제로 줄일 때 도입한다.
- speculative configuration, extension point, caching, concurrency, dependency, framework를 current requirement 없이 추가하지 않는다.

### Preserve observable contracts

- behavior-preserving change를 주장하기 전에 candidate change가 건드릴 수 있는 consumer surface를 확인한다.
- public API뿐 아니라 serialization, registration, config/string lookup, side-effect ordering, error semantics와 material performance 같은 실제 observable surface를 필요한 만큼 본다.
- readability/cleanup 명목으로 behavior를 조용히 바꾸지 않는다.

### Preserve failure and uncertainty

- 실패를 정상값처럼 위장해 downstream 판단을 왜곡하지 않는다.
- `failed`, `absent`, `unknown`, `empty`의 차이가 consumer decision을 바꾸면 의미를 보존한다.
- broad fallback은 caller contract가 실제로 그 의미를 받아들일 때만 사용한다.
- material failure는 diagnose/recover/verify할 만큼 context를 보존한다.

### Respect boundaries and shapes

- external/model/tool/network/storage/config input을 internal invariant로 사용하기 전에 필요한 boundary에서 shape와 semantics를 확인한다.
- unverified dynamic shape를 guessed field/default chain으로 정상화하지 않는다.
- 특정 validation framework를 universal default로 강제하지 않는다.

### Operational machinery needs semantics

Retry, timeout, idempotency, concurrency, caching, observability는 generic ceremony가 아니다.

- 실제 failure/latency/load/ownership requirement가 있는지 본다.
- mechanism이 해결하는 failure mode와 lifecycle을 설명할 수 있어야 한다.
- side effect가 있으면 retry/reconciliation semantics를 먼저 확인한다.
- evidence 없는 hardening으로 task scope를 확대하지 않는다.

### Legibility

- control flow, data flow, state와 ownership이 가능한 한 직접 드러나게 한다.
- comments/docstrings는 code narration보다 non-obvious contract, constraint, consequence, durable rationale에 사용한다.
- 확인되지 않은 rationale를 code shape만 보고 만들지 않는다.
- new helper/layer가 줄이는 이해 비용보다 navigation, terminology, coupling을 더 만들지 않는지 본다.

### Evidence and verification

- tests의 존재를 proof로 취급하지 않는다.
- changed behavior와 material failure path를 cheapest useful level에서 검증한다.
- 실행하지 않은 test/benchmark/runtime observation을 수행했다고 주장하지 않는다.
- stable하고 반복적으로 판정 가능한 invariant는 가능한 경우 lint/static check/schema/test/CI 같은 executable feedback owner로 이동한다.

## `mols-coding-context-python`

### Responsibility

Python-specific semantic/runtime failure를 예방하는 conditional judgment overlay다.

소유하지 않는 것:

- Python tutorial
- PEP 8 복제
- framework best-practice catalogue
- Ruff/Bandit rule list
- exact library version behavior
- generic coding principle의 재정의

### Exception and fallback semantics

- 처리하려는 expected exception과 failure contract를 가능한 구체적으로 식별한다.
- broad `Exception` catch가 필요해도 unexpected failure를 silent success-like fallback으로 바꾸지 않는다.
- large `try`가 unrelated programming/parsing error까지 domain fallback으로 삼키지 않는지 본다.
- exception translation은 필요한 cause/actionable context를 보존한다.
- `None`, `False`, empty collection, sentinel이 failed/not-found/empty를 모호하게 합치면 caller semantics를 확인한다.

Exact hierarchy와 library-specific exception은 current source가 소유한다.

### `asyncio` and concurrency

현재 code가 async/concurrent일 때만 적용한다.

- event loop 안의 blocking I/O/process/sleep을 무심코 섞지 않는다.
- task lifetime과 owner를 잃는 fire-and-forget pattern을 기본값으로 만들지 않는다.
- local Python/runtime에서 structured concurrency가 맞으면 적절한 native mechanism을 우선 검토한다.
- cancellation을 ordinary error처럼 삼켜 timeout/task-group control semantics를 깨뜨리지 않는다.
- timeout은 arbitrary number가 아니라 operation/caller failure policy의 일부다.

Exact blocking-call pattern이 Ruff로 안정적으로 검출되면 analyzer가 detection을 소유한다.

### Dynamic data boundary

현재 boundary가 dynamic/untrusted/externally shaped일 때만 적용한다.

- `dict[str, Any]`와 `.get(..., default)`가 requiredness/unknown을 숨기는지 본다.
- annotation만으로 runtime validation이 생긴다고 가정하지 않는다.
- coercion, unknown-field ignore, defaulting이 decision을 바꾸면 실제 validation semantics를 확인한다.
- dataclass, TypedDict, Pydantic, attrs 등 특정 representation을 universal preference로 강제하지 않는다.

### Subprocess and dynamic execution

현재 code가 process/shell/generated execution boundary를 다룰 때만 적용한다.

- shell이 필요하지 않으면 structured argv/native API를 우선한다.
- model/tool/user/external text를 그대로 shell command나 host-language execution으로 승격하지 않는다.
- dynamic execution이 requirement면 trust boundary, allowed capability, isolation, input/output contract를 먼저 확인한다.
- `shell=True`, `eval`, `exec` token만으로 무조건 defect를 선언하지 않고 실제 trust/requirement를 본다.

### LLM producer artifacts

Python code generation/review에서 다음을 lens로 사용한다.

- Confident fallback
- Over-protective handler
- Docstring hallucination
- Narrative comment
- Boilerplate padding
- Redundant type comment

이 taxonomy를 동일 가중치의 lint checklist로 사용하지 않는다. Outcome impact와 local evidence를 우선한다.

## Producer artifact vs target-system failure

두 종류를 구분한다.

```text
producer artifact
→ 모델 생성 습관 자체를 검토

target-system semantic failure
→ 해당 construct가 실제 code에 있을 때만 적용
```

이 구분이 없으면 Python Skill이 async, retry, schema, security machinery를 불필요하게 추가할 수 있다.

## Cross-family isolation

실제 `SKILL.md`에는 다른 prefix/family Skill 이름을 넣지 않는 것을 기본으로 한다.

다른 Skill과 responsibility가 동시에 적용되는지는 각각의 frontmatter와 global route contract가 결정한다.

따라서 신규 family는 다음 문장을 갖지 않는다.

```text
"이 상황이면 <다른-family-skill>을 읽어라"
"<다른-family-skill>을 먼저 실행해라"
"<다른-family-skill>이 없으면 대신 수행한다"
```

이 방식은 dependency graph, stale cross-reference와 routing coupling을 줄인다.

## Tooling ownership

| Concern | Owner |
| --- | --- |
| exact language/runtime behavior | current Python/library docs/source |
| formatting/simple static smell | repository formatter/Ruff |
| deterministic security pattern | repository-selected SAST |
| type consistency | repository-selected type checker |
| observable behavior | tests/runtime evidence |
| generic engineering judgment | `mols-coding-context` |
| Python semantic judgment | `mols-coding-context-python` |
| repository/path-specific invariant | repository/nested instruction or scoped Rule |

## Package shape

초기에는 둘 다 single-file Skill로 시작한다.

```text
src/rulesync/.rulesync/skills/mols-coding-context/
└── SKILL.md

src/rulesync/.rulesync/skills/mols-coding-context-python/
└── SKILL.md
```

Reference split은 independent loading value가 eval에서 확인된 뒤에만 한다.

Python body가 커지고 특정 rule family가 반복적으로 irrelevant loading을 만든다는 evidence가 생기면 same-family reference split을 검토할 수 있다.

## Content admission rule

새 context rule을 넣기 전에 순서대로 본다.

1. user/repository/runtime/language authority가 이미 결정하는가?
2. formatter/linter/type checker/test/SAST가 안정적으로 판정하는가?
3. 다른 asset family가 소유할 specialized procedure인가?
4. 여러 representative coding task에서 model judgment를 실제로 바꾸는가?
5. base와 Python overlay 중 어느 applicability가 더 정확한가?
6. current construct가 없는데도 불필요한 work를 유도할 위험이 있는가?
7. context cost와 staleness risk를 정당화하는가?

1~3에서 더 직접적인 owner가 있으면 신규 context에 복제하지 않는다.

## Non-goals

- clean-code encyclopedia
- 모든 AI code smell taxonomy
- 모든 Python gotcha
- 모든 security rule
- coding workflow orchestration
- unrelated code normalization
- cross-family Skill dependency/reference
- Python Skill selection만으로 async/retry/schema/security layer 추가
- language별 overlay의 선제적 대량 생성

## Intended steady state

```text
model / harness discovery
│
├─ mols-coding-context
├─ mols-coding-context-python  # when material
└─ other independently applicable assets

no cross-family Skill dependency
```

핵심은 instruction을 늘리는 것이 아니라 **frontmatter routing precision과 family-local context를 통해 필요한 판단만 필요한 task에 로드하는 것**이다.

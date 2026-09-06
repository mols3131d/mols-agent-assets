# `mols-coding-context` evaluation

이 문서는 core/add-on 구조의 routing과 behavior를 검증하는 기준을 정의한다.

## Core Contract

```text
Generic code-facing task
→ mols-coding-context

Python-material code-facing task
→ mols-coding-context
 + mols-coding-context-python

Non-code task
→ neither
```

Python add-on 단독 선택은 failure다.

다른 task-relevant Skill은 각자의 frontmatter 때문에 독립적으로 함께 선택될 수 있어야 한다.

## Routing Evaluation

### Core positive

- 기능 구현
- bug fix
- code review
- refactor
- test 작성/수정
- API/data-model change
- dependency decision
- performance/maintainability work
- correctness/contract 판단이 필요한 code explanation
- routine code mutation

### Core near-miss

- branch/PR metadata만 관리
- README prose만 수정
- programming factual lookup
- code block이 incidental한 non-code writing
- engineering judgment가 필요 없는 단순 quoting/formatting

### Python add-on positive

- Python implementation 수정
- pytest/fixture/test helper 수정 또는 review
- Python exception/fallback semantics
- `asyncio`, cancellation, task lifetime
- Python subprocess/shell/dynamic execution
- external/model/tool data를 Python runtime state로 사용
- Python generated-code quality review

### Python add-on near-miss

- repo에 Python helper가 있지만 다른 language만 수정
- Markdown의 Python snippet을 그대로 이동
- Python path/metadata만 다룸
- Python이 issue/PR text에만 등장
- factual language comparison

### Paired materiality

```text
"Python coroutine cancellation을 수정"
→ core + python

"Python service README 오타 수정"
→ coding context 불필요 가능
```

```text
"TypeScript client만 수정하지만 repo에 Python service도 존재"
→ core only
```

## Composite Routing

목적은 cross-family dependency가 아니라 independent multi-selection을 검증하는 것이다.

Representative cases:

- code-facing task + code-adjacent prose responsibility
- code-facing task + specialized refactor responsibility
- code-facing task + runtime investigation responsibility
- Python coding task + independently applicable task Skill
- code review + repository-context responsibility

Pass:

- core/add-on은 자기 frontmatter 때문에 선택됨
- 다른 applicable Skill도 자기 frontmatter 때문에 선택됨
- 한 Skill이 다른 family를 relay/redirect하지 않음

## Core Behavior

### Smallest coherent change

Pass:

- current boundary와 consumer를 먼저 사용
- 필요한 최소 coherent surface만 변경
- speculative future-proofing 없음

Fail:

- architecture redesign으로 확대
- unrelated cleanup 포함
- current consumer 없는 config/framework 추가

### Contract preservation

Pass:

- candidate change가 실제로 영향을 줄 observable contract를 필요한 만큼 확인
- readability/cleanup 명목의 silent behavior change 없음
- test 존재만으로 compatibility를 과대 주장하지 않음

### Failure semantics

Fixture: external/tool failure를 `None` 또는 empty result로 바꾸면 downstream이 “데이터 없음”으로 오해할 수 있음.

Pass:

- failed/absent/unknown을 material할 때 구분
- failure context 보존
- caller contract 없는 success-like fallback을 만들지 않음

### Operational machinery

Fixture: remote call은 있지만 retry/timeout/concurrency requirement는 없음.

Pass:

- actual failure policy를 먼저 확인
- context에 mechanism이 언급됐다는 이유만으로 추가하지 않음

## Python Add-on Behavior

### Exception scope

Pass:

- expected exception과 caller-visible semantics를 확인
- broad catch가 unrelated bug를 success-like fallback으로 숨기지 않음
- translation 시 필요한 cause/context 보존

### Async

Pass:

- blocking operation, task owner/lifetime, cancellation semantics를 실제 construct가 있을 때만 검토
- unrelated concurrency abstraction을 추가하지 않음

### Dynamic boundary

Pass:

- requiredness/coercion/default/extra-field semantics가 downstream decision에 material한지 확인
- annotation을 runtime validation으로 오해하지 않음
- 새 validation dependency를 근거 없이 추가하지 않음

### Subprocess / dynamic execution

Pass:

- shell 또는 dynamic execution requirement와 trust boundary를 먼저 확인
- structured/constrained execution path를 검토
- token match만으로 unconditional defect를 선언하지 않음

### Generated-code lens

Pass 기준은 smell label 사용이 아니라 다음 outcome이다.

- hallucinated documentation 감소
- narrative noise 감소
- silent failure 감소
- unnecessary defensive padding 감소

## Conditional-rule False Positive

Add-on이 올바르게 선택됐어도 irrelevant rule은 행동을 만들지 않아야 한다.

| Fixture | Expected non-action |
| --- | --- |
| synchronous parser | async abstraction 추가 안 함 |
| trusted internal typed flow | validation framework 추가 안 함 |
| local pure function | retry/timeout 추가 안 함 |
| no subprocess/dynamic execution | security redesign으로 확대 안 함 |
| comment-only local change | unrelated runtime refactor 안 함 |

## Future Language Add-on Check

새 language add-on이 생기면 같은 contract를 검증한다.

```text
language-material task
→ core + matching add-on

other-language-only task
→ core without unrelated add-on

polyglot task
→ core + each material language add-on
```

Core가 언어별 dispatch logic을 소유하거나 모든 language context를 항상 로드하면 regression으로 본다.

## Deterministic Validation

후속 구현에서 최소 확인:

- Skill package/frontmatter/schema validation
- canonical description과 generated route 일치
- Python add-on 단독 선택 방지 fixture
- stale `coding-context` reference 탐색
- 신규 Skill에 cross-family direct dependency/reference 없음
- eval fixture schema correctness
- repository-native generation drift 없음

## Exit Gates

### Routing ready

- core positive recall이 충분함
- core near-miss false positive가 과하지 않음
- Python material task에서 core + add-on pairing이 안정적
- Python incidental task에서 add-on 과선택이 낮음
- independent multi-selection이 유지됨

### Behavior ready

- 기존 generic baseline보다 material regression 없음
- Python-specific failure fixture에서 judgment가 안정적이거나 개선됨
- conditional-rule eval에서 unnecessary work가 증가하지 않음
- deterministic owner와 instruction owner가 중복되지 않음

### Migration ready

- live old-name consumer 정리 가능
- route/projection cleanup path 확인
- 미수행 runtime/model eval을 pass로 주장하지 않음

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
- Python performance bottleneck 분석/최적화

### Python add-on near-miss

- repo에 Python helper가 있지만 다른 language만 수정
- Python source file에서 Python semantics와 무관한 prose/comment만 수정
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

### Smallest coherent change / scope inflation

Fixture: 한 함수의 null-handling bug를 수정하면 충분하지만 주변 module에 오래된 naming과 중복 helper가 보임.

Pass:

- current boundary와 consumer를 먼저 사용
- 필요한 최소 coherent surface만 변경
- bug fix와 무관한 architecture redesign/cleanup을 새 scope로 만들지 않음

Fail:

- repository-wide abstraction 도입
- unrelated rename/refactor 포함
- current consumer 없는 config/framework 추가

### Contract preservation

Pass:

- candidate change가 실제로 영향을 줄 observable contract를 필요한 만큼 확인
- readability/cleanup 명목의 silent behavior change 없음
- test 존재만으로 compatibility를 과대 주장하지 않음

### Failure semantics / confident fallback

Fixture: external/tool failure를 `None` 또는 empty result로 바꾸면 downstream이 “데이터 없음”으로 오해할 수 있음.

Pass:

- failed/absent/unknown을 material할 때 구분
- failure context 보존
- caller contract 없는 success-like fallback을 만들지 않음

### Dependency decision

Pass:

- dependency가 제거하는 implementation/maintenance/operational/security/correctness burden과 새 비용을 비교
- 단순 편의나 speculative use만으로 dependency를 추가하지 않음

### Change separation

Pass:

- functional change와 큰 mechanical refactor를 같이 묶으면 review/rollback/diagnosis/verification이 materially 어려워지는지 판단
- 그렇지 않은 작은 local cleanup은 불필요하게 분리하지 않음

### Robustness theater

Fixture: 한 번 실행되는 internal file transform에 retry, cache, concurrency, plugin configuration을 추가할 명시적 failure/load requirement가 없음.

Pass:

- concrete failure/latency/load/ownership requirement가 없으면 mechanism을 추가하지 않음
- “production-ready” 또는 “robust”라는 추상적 이유를 evidence로 취급하지 않음
- side-effect retry가 실제로 필요할 때만 idempotency/reconciliation semantics 확인

### Verification theater

Fixture: acceptance는 사용자-visible end-to-end behavior지만 unit test 하나만 통과함.

Pass:

- unit test success는 그 test가 검증한 범위로만 주장
- available한 cheapest useful acceptance-layer check를 수행하거나 미검증 gap을 명시
- 실행하지 않은 compatibility/runtime check를 pass로 보고하지 않음

## Evidence-Driven Optimization

### Baseline and bottleneck

Fixture: “이 코드를 더 빠르게 해줘”라는 요청만 있고 bottleneck 위치는 아직 모름.

Pass:

- target metric/constraint와 representative workload를 먼저 식별
- practical하면 baseline/profile/benchmark로 dominant cost를 찾음
- syntax나 직감만으로 cache/concurrency/rewrite를 먼저 선택하지 않음

### Reduce first

Fixture: hot path가 같은 data를 두 번 parse하고 unnecessary copy를 수행함.

Pass:

- 새로운 cache/framework보다 repeated work와 copy 제거를 먼저 검토
- 가장 작은 owner에서 변경
- observable behavior와 failure semantics 보존

### Compare and stop

Pass:

- 같은 representative condition에서 before/after evidence 비교
- benchmark를 실행하지 않았으면 measured improvement라고 주장하지 않음
- 목표 달성 또는 diminishing gain 이후 speculative micro-optimization을 계속 만들지 않음

Fail:

- “더 효율적일 것”이라는 코드 모양만으로 성능 개선 선언
- metric 없이 여러 optimization mechanism 동시 추가
- 작은 gain을 위해 material complexity/portability regression을 숨김

## Python Add-on Behavior

### Exception scope / over-protective handler

Pass:

- expected exception과 caller-visible semantics를 확인
- broad catch가 unrelated bug를 success-like fallback으로 숨기지 않음
- `try` scope를 intended failure source에 맞게 제한
- translation 시 필요한 cause/context 보존

### Async

Pass:

- blocking operation, task owner/lifetime, cancellation semantics를 실제 construct가 있을 때만 검토
- unrelated concurrency abstraction을 추가하지 않음
- cancellation을 ordinary exception fallback으로 삼키지 않음

### Runtime validation

Pass:

- annotation만으로 runtime validation이 생긴다고 가정하지 않음
- requiredness/coercion/variant/extra-field semantics가 downstream decision에 material하면 actual boundary behavior 확인
- 새 validation dependency/representation을 근거 없이 추가하지 않음

### Subprocess / dynamic execution

Pass:

- shell 또는 dynamic execution requirement와 input provenance/trust boundary를 먼저 확인
- shell semantics가 불필요하면 structured argv/direct API를 검토
- `shell=True`, `eval`, `exec` token match만으로 unconditional defect를 선언하지 않음

### Python optimization delta

Fixture: CPU-bound인지 I/O-bound인지 불명확한 Python path를 “async로 바꾸면 빨라질 것”이라고 제안할 수 있음.

Pass:

- target interpreter/build와 representative workload evidence 확인
- CPU/I/O, allocation/data movement, serialization/interop 중 dominant cost를 먼저 식별
- async/thread/process/native/vectorized path/memoization을 folklore로 선택하지 않음
- measured gain과 complexity/memory/startup/cancellation/portability trade-off를 함께 판단

## Conditional-rule False Positive

Add-on이 올바르게 선택됐어도 irrelevant rule은 행동을 만들지 않아야 한다.

| Fixture | Expected non-action |
| --- | --- |
| synchronous parser | async abstraction 추가 안 함 |
| trusted internal typed flow | validation framework 추가 안 함 |
| local pure function | retry/timeout 추가 안 함 |
| no subprocess/dynamic execution | security redesign으로 확대 안 함 |
| comment-only local change | unrelated runtime refactor 안 함 |
| performance concern/evidence 없음 | profiling/optimization work를 새 scope로 만들지 않음 |

## Drop Regression

삭제한 instruction이 다시 들어오지 않는지 review한다.

- generic comments/docstring authoring rule을 core에 다시 추가하지 않음
- Python에서 `None`/empty/sentinel generic semantics를 core와 중복하지 않음
- `.get`, `shell=True`, `eval`, `exec` 같은 token 하나를 defect trigger로 만들지 않음
- Python representation/library 목록을 checklist로 확장하지 않음
- retry/cache/concurrency/observability를 condition 없는 mandatory review list로 만들지 않음
- LLM code-smell taxonomy 전체를 core/add-on에 복제하지 않음

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
- Python incidental/prose-only task에서 add-on 과선택이 낮음
- independent multi-selection이 유지됨

### Behavior ready

- 기존 generic baseline보다 material regression 없음
- scope inflation/robustness theater/confident fallback/verification theater fixture에서 불필요한 work가 증가하지 않음
- optimization fixture에서 baseline → bottleneck → narrow change → comparison/stop 판단이 유지됨
- Python-specific failure fixture에서 judgment가 안정적이거나 개선됨
- conditional-rule eval에서 unnecessary work가 증가하지 않음
- deterministic owner와 instruction owner가 중복되지 않음

### Migration ready

- live old-name consumer 정리 가능
- route/projection cleanup path 확인
- 미수행 runtime/model eval을 pass로 주장하지 않음

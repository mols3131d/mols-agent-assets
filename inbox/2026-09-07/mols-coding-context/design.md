# `mols-coding-context` 설계

이 문서는 coding context의 **core/add-on architecture와 instruction budget**을 정의한다.

## Goal

Code-facing task에 필요한 engineering judgment를 작고 선택 가능한 context로 제공하고, LLM/agent가 만들기 쉬운 불필요한 scope·mechanism·fallback·verification claim을 줄인다.

```text
mols-coding-context
└─ language-independent core

mols-coding-context-python
└─ Python-specific add-on
```

Core는 항상 main entry다. Add-on은 해당 언어의 semantics가 현재 작업에 material할 때만 core와 함께 선택한다.

## Why core + add-on

Generic coding judgment와 language-specific semantics는 함께 필요할 수 있지만 같은 책임은 아니다.

Core가 소유하는 것:

- system fit과 smallest coherent change
- observable contract 보존
- failure/absence/unknown 의미 보존
- external/executable boundary 판단
- operational machinery의 evidence gate
- verification truthfulness와 stop condition
- evidence-driven optimization judgment

Python add-on이 소유하는 것:

- Python exception/fallback semantics delta
- `asyncio`, cancellation, task lifetime
- annotation과 runtime validation의 Python nuance
- subprocess/shell/dynamic execution nuance
- Python performance mechanism 선택의 runtime-evidence delta

Add-on은 core의 generic rule을 다시 쓰지 않는다.

## Activation

### Core

현재 active work가 executable code 또는 code-facing contract를 material하게 다루면 선택한다.

대표적인 positive:

- implementation/modification/debugging
- test/refactor/review
- API/data-model/dependency decision
- performance/maintainability
- correctness/contract 판단이 필요한 code explanation

대표적인 near-miss:

- pure factual programming lookup
- code-facing work가 없는 repository administration
- code가 incidental한 non-code writing

### Python add-on

Core가 적용되는 task 중 현재 결과가 Python code semantics, Python runtime behavior 또는 Python-facing tests에 material하게 의존하면 함께 선택한다.

Path나 `.py` 존재 자체는 충분한 trigger가 아니다. Python 파일 안의 prose-only 수정처럼 Python semantics가 결과를 바꾸지 않는 작업도 add-on trigger가 아니다.

```text
Python service exception handler 수정
→ core + python

Python helper가 repo에 있지만 TypeScript만 수정
→ core only

Python code fence를 문서에서 이동
→ neither 또는 task에 필요한 다른 asset만
```

## Add-on Contract

Language add-on은 다음 contract를 따른다.

1. Core와 함께 사용한다.
2. Core를 반복하지 않는다.
3. 그 언어에서만 달라지는 semantic/runtime judgment만 추가한다.
4. Exact API/version behavior는 current authoritative source에 맡긴다.
5. 해당 language construct가 없으면 관련 rule은 행동을 만들지 않는다.

즉:

```text
Skill selected
≠ every rule applies
```

Python add-on이 선택됐어도 async code가 없으면 async rule은 아무 작업도 만들지 않는다.

## Instruction Budget

새 instruction은 다음 중 하나를 충족할 때만 admission한다.

- 없으면 반복적으로 발생하는 material engineering error를 직접 줄임
- observable invariant, failure meaning, safety/trust boundary 또는 required default를 보존함
- generic authority/tooling만으로 안정적으로 복원하기 어려운 ambiguity를 해결함
- language add-on에서는 core로 표현할 수 없는 material semantic/runtime delta를 제공함

다음은 admission 근거가 아니다.

- 일반적으로 좋은 practice라는 이유
- 특정 keyword/library가 등장했다는 이유
- “더 robust해 보임” 또는 “future-proof해 보임”
- model이 언젠가 실수할 수 있다는 막연한 가능성
- rule을 더 많이 두면 더 안전할 것이라는 가정

새 rule은 기존 rule의 condition을 더 정확히 하는 것으로 해결할 수 있는지 먼저 본다. 같은 failure를 여러 문장이 막으면 가장 직접적인 owner만 남긴다.

## Anti-pattern Lenses

두 Skill은 code-smell taxonomy를 소유하지 않는다. 대신 여러 언어와 task에서 decision quality를 실제로 바꾸는 root anti-pattern만 유지한다.

### Core

- **Scope inflation** — local issue를 architecture rewrite, unrelated cleanup 또는 broad refactor로 확대
- **Robustness theater** — failure/constraint evidence 없이 fallback, retry, cache, concurrency, configuration 또는 abstraction 추가
- **Confident fallback** — failure/unknown을 success-like absence/empty value로 변환
- **Verification theater** — 일부 test나 static inspection을 전체 acceptance evidence로 과대 해석
- **Premature optimization** — metric, baseline 또는 bottleneck evidence 전에 optimization mechanism 선택

### Python delta

- **Over-protective handler** — broad/oversized catch로 unrelated failure를 삼킴
- **Annotation-as-validation** — type annotation을 runtime validation으로 오해
- **Async by reflex** — task lifetime/failure model 없이 async/concurrency machinery 추가
- **Token security heuristic** — `shell=True`, `eval`, `exec` token 자체만으로 unconditional defect 판정
- **Python folklore optimization** — target runtime/workload evidence 없이 async/thread/process/vectorization/native path 등을 성능 해법으로 선택

Narrative Comment, Docstring Hallucination, Redundant Type Comment 같은 concern은 이 core/add-on의 직접 owner가 아니다. 별도 prose/tooling owner 또는 deterministic mechanism으로 처리하고 여기에는 복제하지 않는다.

## Evidence-Driven Optimization

Optimization은 core의 generic judgment이며, Python add-on은 language delta만 추가한다.

Core process:

```text
target
→ locate dominant cost
→ reduce existing work first
→ narrow optimization
→ compare
→ stop
```

- **Target** — metric/constraint/cost와 representative workload를 정하고 practical하면 baseline을 확보
- **Locate** — profile/benchmark/trace/complexity/data-flow evidence로 dominant cost 식별
- **Reduce first** — mechanism을 추가하기 전에 work, indirection, allocation, data movement, repeated I/O 제거 검토
- **Narrow optimization** — 가장 작은 owner에서 observable contract를 보존하며 변경
- **Compare / stop** — 같은 조건에서 before/after를 비교하고 목표 달성, diminishing gain 또는 complexity cost가 커지면 종료

Optimization process 자체가 모든 coding task의 workflow가 되지는 않는다. Performance/resource/material maintenance cost가 scope이거나 evidence가 bottleneck을 가리킬 때만 활성화한다.

Python add-on은 다음만 추가한다.

- interpreter/build와 representative workload를 기준으로 측정
- CPU/I/O, allocation/data movement, serialization/interop 중 실제 dominant cost 확인
- `async`, threads/processes, native/vectorized path, memoization 같은 Python mechanism을 folklore만으로 고르지 않음

## Extensibility

다른 언어 add-on은 필요와 evidence가 생겼을 때만 추가한다.

```text
mols-coding-context-<language>
```

새 add-on을 만들 기준:

- core로 표현하기 어려운 language-specific failure semantics가 반복적으로 존재
- 별도 applicability/loading value가 분명함
- deterministic tooling이나 official docs만으로 해결되지 않는 model judgment가 있음
- context와 maintenance cost를 정당화함

단순히 언어가 많이 쓰인다는 이유로 add-on을 만들지 않는다.

Polyglot task에서는 필요한 add-on을 함께 선택할 수 있다.

```text
Python service + TypeScript client
→ core + python + typescript  # 해당 add-on이 실제 존재하고 둘 다 material한 경우
```

Core가 language router가 되지는 않는다. 각 add-on의 frontmatter가 자기 applicability를 소유한다.

## Cross-family Boundary

다른 Skill family와의 조합은 model/harness의 independent selection에 맡긴다.

신규 Skill body에는 다음을 넣지 않는다.

- 다른 family Skill을 먼저 읽으라는 지시
- 다른 family Skill을 prerequisite/fallback으로 선언
- 다른 family의 reference path
- 다른 family의 lifecycle/deprecation 정책

Same-family core/add-on 관계만 직접 표현한다.

## Rule Admission

새 instruction을 넣기 전에 다음을 본다.

1. 사용자/repository/runtime/language authority가 이미 결정하는가?
2. formatter/linter/type checker/test/SAST가 안정적으로 판정하는가?
3. 다른 asset이 더 직접적인 owner인가?
4. representative task에서 model judgment를 실제로 바꾸는가?
5. Core와 add-on 중 더 정확한 applicability owner가 어디인가?
6. 해당 construct가 없는데도 unnecessary work를 유도하지 않는가?
7. existing instruction을 더 정확히 하거나 삭제하는 것이 새 rule보다 나은가?

더 직접적인 owner가 있으면 context에 복제하지 않는다.

## Package Shape

두 package는 single-file Skill로 유지한다.

```text
src/rulesync/.rulesync/skills/mols-coding-context/
└── SKILL.md

src/rulesync/.rulesync/skills/mols-coding-context-python/
└── SKILL.md
```

Reference split은 실제로 independent loading value가 확인된 뒤에만 한다.

## Non-goals

- coding workflow orchestration
- clean-code encyclopedia
- LLM code-smell taxonomy 복제
- language/API reference 복제
- deterministic lint rule catalogue
- generic security checklist
- generic optimization checklist
- 모든 language add-on의 선제적 생성
- cross-family dependency graph

성공 기준은 Skill 수나 rule 수가 아니라 **routing precision, context relevance, semantic ownership, evidence quality와 unnecessary work 감소**다.

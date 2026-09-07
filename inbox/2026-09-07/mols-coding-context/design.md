# `mols-coding-context` 설계

이 문서는 coding context의 **core/add-on architecture**를 정의한다.

## Goal

Code-facing task에 필요한 engineering judgment를 작고 선택 가능한 context로 제공한다.

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
- dynamic/external boundary 판단
- retry/timeout/concurrency 같은 operational machinery의 도입 기준
- legibility와 verification truthfulness

Python add-on이 소유하는 것:

- Python exception/fallback semantics
- `asyncio`, cancellation, task lifetime
- Python dynamic data boundary와 runtime validation nuance
- subprocess/shell/dynamic execution nuance

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
4. 여러 representative task에서 model judgment를 실제로 바꾸는가?
5. Core와 add-on 중 더 정확한 applicability owner가 어디인가?
6. 해당 construct가 없는데도 unnecessary work를 유도하지 않는가?

더 직접적인 owner가 있으면 context에 복제하지 않는다.

## Package Shape

초기 package는 둘 다 single-file Skill로 유지한다.

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
- language/API reference 복제
- deterministic lint rule catalogue
- generic AI-generated-code smell taxonomy
- 모든 language add-on의 선제적 생성
- cross-family dependency graph

성공 기준은 Skill 수가 아니라 **routing precision, context relevance, semantic ownership과 unnecessary work 감소**다.

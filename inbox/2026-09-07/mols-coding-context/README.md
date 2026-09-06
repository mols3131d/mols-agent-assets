# `mols-coding-context` 설계 번들

이 번들은 `mols-coding-context`와 `mols-coding-context-python`을 **모델이 현재 coding task의 의미를 판단해 선택적으로 주입하는 instruction context**로 설계하기 위한 조사·설계 자료다.

이번 단계에서는 실제 Skill을 만들거나 기존 Skill을 삭제하지 않는다.

## 결론

초기 구조는 하나의 coding-context family다.

```text
code-facing task
│
├─ mols-coding-context
│  └─ language-independent engineering judgment
│
└─ Python-specific semantics가 material하면
   └─ mols-coding-context-python
      └─ Python-specific judgment overlay
```

두 Skill은 같은 prefix와 responsibility family를 공유하므로 family 내부 composition을 가질 수 있다. `mols-coding-context-python`은 base를 대체하지 않고 함께 선택되는 overlay다.

다른 prefix/family의 Skill과는 직접 의존하거나 서로를 참조하지 않는다. 각 Skill은 자기 frontmatter `description`만으로 독립적으로 discovery되고, 모델/하네스가 현재 task에서 여러 책임이 동시에 적용된다고 판단할 때 각각 선택한다.

즉 신규 context Skill은 다른 coding Skill을 호출하거나 로드하거나 이름으로 route하지 않는다.

## 핵심 설계 원칙

- **Frontmatter-first discovery** — selection 전에 모델/하네스가 볼 수 있는 `name`·`description`에 intended use와 near-miss boundary를 충분히 표현한다.
- **Independent multi-selection** — 다른 Skill과의 조합은 cross-reference가 아니라 router의 독립 selection으로 해결한다.
- **Family-local composition only** — `mols-coding-context*`처럼 명확한 같은 family 안에서만 base/overlay 관계를 표현한다.
- **Semantic routing** — path나 확장자만이 아니라 현재 task의 active work surface와 판단 필요성을 본다.
- **Conditional rules, not a checklist** — Skill이 선택됐다고 모든 rule을 적용하거나 주변 코드를 정리하지 않는다. 현재 변경과 failure surface에 material한 rule만 사용한다.
- **Small high-signal context** — model이 반복해서 잘못 판단하는 고비용 failure mode를 우선하고 language/API encyclopaedia를 만들지 않는다.
- **Standard first, local delta only** — Python·library·runtime의 정확한 계약은 authoritative source가 소유한다.
- **Mechanize deterministic invariants** — Ruff, type checker, formatter, tests, SAST가 안정적으로 판정할 수 있는 항목을 prose로 중복하지 않는다.
- **One concern, one semantic owner** — generic principle은 base가, Python-specific semantics는 overlay가 소유한다.

## Frontmatter trigger 초안

### `mols-coding-context`

```yaml
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
```

목표는 high recall을 유지하면서 세 가지 near-miss를 명시하는 것이다.

- pure factual programming lookup
- repository administration without code-facing work
- non-code writing with incidental code

다른 Skill 이름은 넣지 않는다. `independently alongside any other task-relevant Skill`만으로 multi-selection 가능성을 알린다.

### `mols-coding-context-python`

```yaml
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
```

`mols-coding-context`를 이름으로 참조하는 것은 같은 family의 base/overlay contract이므로 허용한다. 그 외 Skill 이름은 frontmatter나 body에서 참조하지 않는다.

## 문서

| 문서 | 책임 |
| --- | --- |
| [research.md](research.md) | repository state, routing 구조, 외부 연구와 coding-agent/Python failure pattern 조사 |
| [design.md](design.md) | 두 context Skill의 responsibility, activation, family-local composition, rule admission과 content boundary |
| [migration.md](migration.md) | 기존 `coding-context` 교체와 다른 Skill family의 독립성 보존 전략 |
| [evaluation.md](evaluation.md) | frontmatter routing, behavior, family pairing, context cost와 migration gate |

## `mols-coding-context`

현재 `coding-context`의 후속 owner다. 일반 clean-code 백과사전이 아니라 여러 coding task에서 반복적으로 필요한 engineering judgment를 소유한다.

주요 축:

- system fit과 smallest coherent change
- observable behavior와 실제 consumer contract 보존
- failure·absence·unknown을 필요 이상으로 정상값에 합치지 않기
- external/dynamic boundary를 추측한 shape로 사용하지 않기
- retries, timeout, concurrency, abstraction 같은 복잡성은 실제 semantics와 evidence가 있을 때만 도입하기
- code legibility와 verification evidence를 implementation convenience보다 우선하기
- 안정적이고 기계적으로 판정 가능한 invariant는 executable feedback으로 이동하기

## `mols-coding-context-python`

Python-specific rule overlay다. Python 파일이 존재한다는 사실보다 **현재 coding judgment가 Python semantics에 의존하는지**가 중요하다.

초기 focus:

- exception scope와 failure semantics
- `asyncio` blocking, task lifetime, cancellation과 structured concurrency
- dynamic/raw data boundary와 permissive fallback/coercion
- subprocess, shell과 dynamic execution trust boundary
- LLM-generated Python에서 반복되는 confident fallback, over-protective handler, narrative comment, docstring hallucination 등의 review lens
- Python official contract와 Ruff/type checker/test/SAST 사이의 ownership 분리

각 항목은 적용 여부를 모델이 현재 code와 task에 맞춰 판단한다. Python Skill을 선택했다는 이유로 async, retry, validation layer를 새로 만들지 않는다.

## 다른 Skill family와의 관계

`mols-coding-context*`는 다른 Skill family의 lifecycle이나 routing을 소유하지 않는다.

- 다른 Skill을 이름으로 호출하지 않는다.
- 다른 Skill을 prerequisite로 선언하지 않는다.
- 다른 Skill의 body/reference를 읽으라고 지시하지 않는다.
- 다른 Skill을 대체한다고 주장하지 않는다.
- 다른 Skill과의 selection 조합은 router/model이 각 frontmatter를 독립적으로 판단하게 둔다.

설계 문서에서는 migration boundary를 설명하기 위해 기존 Skill을 언급할 수 있지만, 실제 신규 `SKILL.md`에는 cross-family reference를 넣지 않는 것이 기본이다.

## Migration 방향

이번 설계에서 직접 교체 대상으로 확정하는 것은 신규 base의 predecessor인 `coding-context`뿐이다.

- `coding-context` → `mols-coding-context`로 교체 후 삭제
- 다른 prefix/family의 existing Skill → 유지, 이번 migration에서 직접 변경·참조 관계를 만들지 않음

## 다음 구현 경계

후속 구현에서는 다음 순서가 가장 작다.

1. 위 trigger contract를 기반으로 `mols-coding-context` 생성
2. 같은 family overlay인 `mols-coding-context-python` 생성
3. frontmatter positive / negative / near-miss / composite routing eval 추가
4. base + Python family pairing과 Python incidental false positive 평가
5. behavior와 context-noise eval 수행
6. 기존 `coding-context`의 대체 가능성 검증
7. gate를 통과하면 `coding-context`만 삭제하고 route/lock/current references 정리

다른 Skill family의 수정은 이 implementation scope에 포함하지 않는다.

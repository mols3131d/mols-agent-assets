# `mols-coding-context*` migration

이 문서는 신규 coding context family를 도입하면서 기존 generic coding context의 ownership을 어떻게 이전할지 정의한다.

## Migration objective

목표는 하나다.

```text
coding-context
→ mols-coding-context

+ new same-family overlay
→ mols-coding-context-python
```

다른 prefix/family의 Skill은 이번 migration의 dependency, reference, deletion 또는 redesign 대상이 아니다.

## Disposition

| Current asset | Disposition |
| --- | --- |
| `coding-context` | `mols-coding-context`로 replace 후 삭제 |
| `mols-clarify-code` | 유지, out of migration scope |
| `mols-code-comprehension-refactor` | 유지, out of migration scope |
| `mols-clarify-runtime` | 유지, out of migration scope |
| 그 밖의 다른 Skill family | 독립 유지 |

설계 문서가 기존 asset을 inventory 목적으로 언급할 수는 있지만, 신규 `SKILL.md`가 다른 family의 Skill을 참조하거나 의존하게 만들지 않는다.

## `coding-context` → `mols-coding-context`

### Preserve

현재 generic baseline의 다음 meaning을 이어받는다.

- effectiveness / operability / simplicity / elegance tie-break
- KISS / YAGNI / DRY / SRP의 anti-dogmatic interpretation
- fit the system
- smallest coherent change
- behavior/compatibility preservation
- required behavior와 stylistic preference 구분
- evidence와 verification truthfulness
- failure context와 operability
- material finding 우선 review discipline

### Refine

Agent-generated code에서 반복적으로 가치가 큰 다음 boundary를 더 선명하게 한다.

- failed / absent / unknown / empty를 무근거하게 하나의 정상값에 합치지 않기
- external/dynamic shape를 추측하지 않기
- retry/timeout/concurrency/observability를 semantics 없이 ceremony로 추가하지 않기
- stable deterministic invariant를 executable feedback으로 옮기기

### Compress

다음 중복은 줄인다.

- maintainability/simple/explicitness의 유사 wording
- verification/review의 evidence boundary 반복
- generic hardening 문구

목표는 rule 수 증가가 아니라 signal density 개선이다.

## `mols-coding-context-python` introduction

Python overlay는 신규 same-family surface다.

초기 rule family:

- exception/fallback semantics
- `asyncio` blocking/cancellation/task lifetime
- dynamic data boundary/coercion/defaulting
- subprocess/shell/dynamic execution
- Python-specific LLM producer artifacts
- Python official contract와 Ruff/type/test/SAST ownership boundary

기존 다른 Skill의 Python example이나 procedure를 찾아 기계적으로 이관하지 않는다.

## Cross-family isolation contract

신규 family의 canonical Skill에는 다음을 넣지 않는다.

- 다른 prefix/family Skill 이름을 prerequisite로 지정
- 다른 Skill을 읽거나 호출하라는 instruction
- 다른 Skill이 없을 때 대신 수행한다는 fallback
- 다른 Skill의 reference path
- 다른 Skill의 lifecycle/deprecation policy

Composite task에서는 route layer가 각 Skill의 `name`·`description`을 독립적으로 평가해 필요한 asset을 여러 개 선택한다.

이 contract의 목적은 다음 coupling을 막는 것이다.

- stale skill-name reference
- dependency chain
- routing relay
- one Skill rename이 unrelated family에 전파되는 change
- body를 읽기 전에 필요한 selection 정보를 body reference에 숨기는 문제

## Frontmatter migration

기존 `coding-context`의 broad activation semantics는 유지하되 신규 name과 role을 명확히 한다.

### New base

```yaml
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
```

### Python overlay

```yaml
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
```

Frontmatter wording은 implementation eval에서 조정할 수 있지만 semantic boundary는 유지한다.

## Migration phases

### Phase 1 — Introduce

1. `mols-coding-context` 생성
2. `mols-coding-context-python` 생성
3. trigger/behavior eval fixture 추가
4. repository-native generator로 route/projection 갱신
5. 기존 `coding-context`와 일시 공존

다른 Skill family는 수정하지 않는다.

### Phase 2 — Compare

```text
old coding-context
vs
new mols-coding-context
```

확인:

- generic coding routing precision/recall
- system fit / smallest change
- contract preservation
- failure/uncertainty semantics
- evidence truthfulness
- unnecessary abstraction/operational ceremony
- context footprint

### Phase 3 — Validate same-family routing

```text
non-Python coding
→ mols-coding-context

Python-material coding
→ mols-coding-context
 + mols-coding-context-python

Python incidental
→ no Python overlay
```

특히 overlay-only selection을 failure로 본다.

### Phase 4 — Replace old generic owner

Gate 통과 후:

- `coding-context` canonical directory 삭제
- old-name direct dependency/reference 정리
- route/lock/projection을 repository-native owner로 갱신
- obsolete old eval fixture 정리

다른 Skill family의 파일은 변경하지 않는다.

### Phase 5 — Garbage collect migration-only state

- stale `coding-context` current-state reference 제거
- temporary compatibility wording 제거
- generated drift 확인
- inbox artifact의 승격/보존 여부는 별도 판단

## Deletion gate

기존 `coding-context`만 다음을 모두 만족하면 삭제한다.

1. `mols-coding-context`가 representative generic coding task에서 baseline으로 안정적으로 선택됨
2. current material behavior가 유지되거나 개선됨
3. new failure/boundary rules가 speculative work를 유도하지 않음
4. Python overlay가 base와 올바르게 pairing됨
5. old name을 요구하는 live consumer가 없거나 migration path가 확인됨
6. generated route/lock/reference cleanup이 확인됨
7. 실행하지 않은 runtime eval을 통과했다고 주장하지 않음

Asset 수 감소 자체는 gate가 아니다.

## Rollback

신규 base가 current `coding-context`보다 routing 또는 behavior가 나쁘면 old generic owner 삭제를 중단한다.

원인이 신규 base의 과도한 scope면 rule을 줄이고, Python-specific concern이면 same-family overlay로 내리고, 다른 task-specific concern이면 그 concern의 existing owner를 그대로 둔다.

Migration의 목표는 다른 Skill을 재편하는 것이 아니라 **generic coding context family를 명확한 frontmatter routing과 최소한의 semantic ownership으로 교체하는 것**이다.

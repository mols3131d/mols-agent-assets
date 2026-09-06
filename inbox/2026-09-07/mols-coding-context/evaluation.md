# `mols-coding-context*` evaluation

이 문서는 신규 coding context family의 frontmatter routing, behavior, same-family composition, context cost와 `coding-context` migration을 어떻게 검증할지 정의한다. 실제 eval fixture와 runner 변경은 후속 구현에서 수행한다.

## Evaluation questions

1. `mols-coding-context` frontmatter가 code-facing task에서 높은 recall을 유지하는가?
2. Pure factual lookup, repository administration, incidental-code prose에서 false positive를 억제하는가?
3. Python-specific semantics가 material할 때 `mols-coding-context-python`이 base와 함께 선택되는가?
4. Python이 incidental할 때 overlay가 선택되지 않는가?
5. 다른 task-relevant Skill이 동시에 적용돼도 신규 family가 독립 multi-selection을 방해하지 않는가?
6. Cross-family direct dependency/reference 없이 composite routing이 작동하는가?
7. Selected Skill의 rule이 checklist처럼 과적용되어 unnecessary work를 만들지 않는가?
8. 기존 `coding-context` 대비 generic behavior regression 없이 signal density가 개선되는가?

## Evidence layers

| Evidence | 판정 가능 범위 |
| --- | --- |
| deterministic validation | frontmatter/schema/path/reference/route drift |
| static semantic review | responsibility, authority, family boundary, context duplication |
| routing eval | model/harness가 `name`·`description`을 보고 어떤 Skill set을 선택하는지 |
| behavior eval | selected context가 실제 output/judgment를 어떻게 바꾸는지 |
| composite routing eval | 다른 독립 Skill과 동시에 적용될 때 multi-selection이 유지되는지 |
| baseline comparison | old `coding-context` 대비 신규 base의 regression/개선 |
| context comparison | irrelevant loaded context와 unnecessary work가 줄었는지 |

Runtime/model을 실제 실행하지 않았다면 routing/behavior 성능을 검증했다고 주장하지 않는다.

## Frontmatter under evaluation

### Base

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

Eval 결과에 따라 wording을 조정할 수 있지만 intended semantic boundary는 바꾸지 않는다.

## Routing contract

```text
Generic coding task
→ mols-coding-context

Python-material coding task
→ mols-coding-context
 + mols-coding-context-python

Non-code task
→ neither
```

Python overlay-only selection은 failure다.

다른 task-relevant Skill이 독립적으로 적용되는 composite case에서는 coding-context family와 다른 applicable asset이 각각 자기 frontmatter 때문에 선택되어야 한다. 특정 cross-family pair를 신규 Skill의 dependency contract로 만들지 않는다.

## Base trigger cases

Positive:

- 기능 구현, bug fix, code review, refactor
- test 작성/수정
- API/data model/dependency decision
- performance/maintainability work
- correctness/contract 판단이 필요한 code explanation
- 단순하지만 실제 code mutation이 있는 routine task

Negative / near-miss:

- branch/PR metadata 관리만 수행
- README prose만 수정
- programming language 역사/개념 factual lookup
- 코드 블록이 incidental example인 비코딩 문서 작업
- code token의 단순 formatting/quoting

## Python overlay trigger cases

Positive:

- `.py` implementation 또는 Python-facing test 수정/review
- Python exception/fallback semantics
- `asyncio`, task lifetime, cancellation
- Python subprocess/shell/dynamic execution boundary
- model/tool/external JSON을 Python runtime state로 사용
- Python-specific generated-code artifact review

Negative / near-miss:

- repository에 Python helper가 있지만 다른 language만 수정
- Python snippet을 Markdown에 그대로 인용
- factual language comparison
- Python path/metadata만 다루고 code behavior는 판단하지 않음
- PR title이나 issue text에 Python이 등장

## Composite routing cases

목적은 특정 Skill dependency가 아니라 **independent selection property**를 검증하는 것이다.

- code-facing task + code-adjacent prose task
- code-facing task + specialized refactor task
- code-facing task + runtime investigation task
- Python coding task + independently applicable task Skill
- code review + repository-context loader

Pass:

- 각 책임의 Skill이 자기 frontmatter 때문에 선택됨
- 신규 family가 다른 Skill 이름을 몰라도 multi-selection이 됨
- 한 Skill이 다른 Skill을 relay/redirect하지 않음

Fail:

- base가 broad하다는 이유로 더 구체적인 independently applicable Skill이 사라짐
- 다른 Skill이 선택됐다는 이유로 base가 누락됨
- body cross-reference가 없으면 selection이 실패함
- 불필요한 double routing/relay가 생김

## Generic behavior cases

### Smallest coherent change

Local defect를 현재 boundary 안에서 고칠 수 있는데 new service/layer/config/framework를 추가하기 쉬운 task를 둔다.

Pass는 current boundary와 consumer를 먼저 사용하고 필요한 최소 coherent surface만 변경하며 speculative future-proofing을 하지 않는 것이다.

### Contract preservation

Readability/cleanup change가 serialization/order/registration 같은 non-obvious consumer surface를 건드릴 수 있는 fixture를 둔다. Candidate change의 실제 contract를 필요한 만큼 확인하고 behavior-preserving claim을 test 존재만으로 과대 주장하지 않아야 한다.

### Failure semantics

External/tool call 실패가 `None`이나 empty list로 바뀌어 downstream이 “데이터 없음”으로 오해할 수 있는 fixture를 둔다. Failed/absent/unknown을 material할 때 구분하고 failure context를 보존해야 한다.

### Operational machinery

Remote call은 있으나 retry/timeout/concurrency requirement가 없는 fixture를 둔다. Context에 해당 mechanism이 언급됐다는 이유만으로 generic hardening을 추가하면 fail이다.

### Legibility

Narrative comment와 실제 non-obvious invariant가 섞인 fixture에서 code narration은 제거/미작성하고 invariant/contract/rationale는 evidence-backed하게 보존해야 한다.

## Python behavior cases

- broad exception + success-like fallback
- oversized `try` scope
- blocking call inside async path
- cancellation suppression
- task lifetime loss
- dynamic raw boundary with `.get()` defaults
- model output + shell execution
- narrative comment / hallucinated docstring / boilerplate padding / redundant type comment

Pass 기준은 특정 implementation이나 taxonomy label이 아니라 contract fidelity, failure visibility, current Python semantics와 unnecessary work 억제다.

## Conditional-rule false-positive eval

Python Skill이 올바르게 선택된 task에서도 irrelevant rule이 work를 만들지 않는지 확인한다.

| Fixture | Expected non-action |
| --- | --- |
| pure synchronous parser | async abstraction 추가 안 함 |
| internal trusted typed flow | validation framework 추가 안 함 |
| local pure function | retry/timeout 추가 안 함 |
| no subprocess/dynamic execution | sandbox/security redesign으로 task 확대 안 함 |
| comment-only local edit | unrelated runtime refactor 안 함 |

## `coding-context` baseline comparison

```text
old coding-context
vs
new mols-coding-context
```

Gate:

- generic code-facing routing에 material regression 없음
- system fit / smallest coherent change / behavior preservation / evidence truthfulness 유지 또는 개선
- failure/uncertainty/boundary semantics가 더 명확함
- speculative operational mechanism insertion이 증가하지 않음
- independent multi-selection behavior가 악화되지 않음
- body/context가 불필요하게 비대해지지 않음

## Context cost review

Token 수 하나를 quality metric으로 사용하지 않는다. Irrelevant Skill selection, Python incidental loading, same-family semantic duplication, unnecessary work/tool call, cross-family reference 의존 여부를 함께 본다.

## Deterministic validation

후속 implementation에서 최소 확인:

- Skill package/frontmatter/schema validation
- route generation drift 없음
- route description과 canonical frontmatter 일치
- Python overlay base-pairing fixture integrity
- stale old `coding-context` reference 탐색
- 신규 `SKILL.md`에 cross-family Skill name/reference가 없는지 확인
- eval fixture correctness
- repository formatting과 source-authority/layout policy 준수

## Exit gates

Frontmatter ready:

- base positive task recall 충분
- base near-miss false positive 억제
- Python material task에서 base+overlay pairing 안정
- Python incidental near-miss에서 overlay 억제
- composite task에서 independent multi-selection 유지
- selection을 위해 body cross-reference 불필요

Behavior ready:

- current baseline보다 generic behavior가 material하게 나빠지지 않음
- Python failure fixtures에서 semantic judgment 개선 또는 안정
- conditional-rule eval에서 speculative work 증가 없음
- deterministic owner와 instruction owner 중복 없음

Old generic deletion ready:

기존 `coding-context`만 semantic 보존, representative routing/behavior regression 없음, Python pairing, independent multi-selection, consumer cleanup path, generated route/lock cleanup, truthfulness gate를 통과하면 삭제한다. Asset 수 감소 자체는 gate가 아니다.

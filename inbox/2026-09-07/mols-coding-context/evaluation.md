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

### Expected core sets

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

### Independent multi-selection

다른 task-relevant Skill이 독립적으로 적용되는 composite case에서는:

```text
expected set
= coding-context family members that apply
+ independently applicable other assets
```

신규 Skill body가 다른 family를 이름으로 참조하지 않아도 router가 각 frontmatter를 independently 평가해 multi-select해야 한다.

특정 cross-family pair를 신규 Skill의 dependency contract로 만들지 않는다.

## Base trigger cases

### Positive

- 기능 구현
- bug fix
- code review
- refactor
- test 작성/수정
- API/data model change
- dependency decision
- performance/maintainability work
- code explanation에서 correctness/contract 판단이 필요한 경우
- 단순하지만 실제 code mutation이 있는 routine task

### Negative / near-miss

- branch/PR metadata 관리만 수행
- README prose만 수정
- programming language 역사/개념 factual lookup
- 코드 블록이 incidental example인 비코딩 문서 작업
- code token의 단순 formatting/quoting으로 engineering judgment가 필요하지 않음

### Paired intent cases

같은 vocabulary라도 intent가 다르면 결과가 달라져야 한다.

```text
"이 함수의 실패 처리를 수정해줘"
→ base

"실패 처리란 무슨 뜻이야?"
→ pure factual explanation이면 base 불필요 가능
```

```text
"이 PR의 코드 변경을 리뷰해줘"
→ base

"PR 제목만 바꿔줘"
→ base 불필요
```

## Python overlay trigger cases

### Positive

- `.py` implementation 수정
- pytest/fixture/test helper 수정 또는 review
- Python exception/fallback semantics 검토
- `asyncio`, task lifetime, cancellation 처리
- Python subprocess/shell/dynamic execution boundary
- model/tool/external JSON을 Python runtime state로 사용
- Python-specific generated-code artifact review

### Negative / near-miss

- repository에 Python build/helper script가 있지만 TypeScript만 수정
- Python snippet을 Markdown에 그대로 인용
- “Python과 Rust 중 어떤 언어가 인기인가?”
- Python file path/metadata만 다루고 code behavior는 판단하지 않음
- PR title이나 issue text에 Python이 등장

### Materiality paired cases

```text
"Python service의 exception handler를 수정해줘"
→ base + python

"Python service README의 오타만 고쳐줘"
→ coding context 불필요 가능
```

```text
"이 Python coroutine의 cancellation 처리 검토"
→ base + python

"이 문서의 Python code fence를 이동해줘"
→ Python overlay 불필요 가능
```

## Composite routing cases

목적은 특정 Skill dependency를 검증하는 것이 아니라 **independent selection property**를 검증하는 것이다.

Case family:

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

기존 specialized coding Skill들의 representative task는 이 composite set에서 regression check로 사용할 수 있지만, 신규 Skill의 dependency로 선언하지 않는다.

## Generic behavior cases

### Smallest coherent change

Fixture: local defect를 현재 boundary 안에서 고칠 수 있는데 new service/layer/config/framework를 추가하기 쉬운 task.

Pass:

- current boundary와 consumer를 먼저 사용
- 필요한 최소 coherent surface만 변경
- speculative future-proofing 없음

Fail:

- architecture redesign으로 확대
- unrelated cleanup 포함
- current consumer 없는 option/config 추가

### Contract preservation

Fixture: readability/cleanup change가 serialization/order/registration 같은 non-obvious consumer surface를 건드릴 수 있음.

Pass:

- candidate change가 영향을 줄 contract를 필요한 만큼 확인
- hidden usage를 근거 없이 무시하지도, 가능성만으로 모든 change를 막지도 않음
- behavior-preserving claim을 test 존재만으로 과대 주장하지 않음

### Failure semantics

Fixture: external/tool call 실패를 `None` 또는 empty list로 바꾸면 downstream이 “데이터 없음”으로 오해할 수 있음.

Pass:

- failed/absent/unknown을 material할 때 구분
- failure context 보존
- fallback contract가 없으면 정상값으로 위장하지 않음

### Operational machinery

Fixture: remote call이 있으나 retry/timeout/concurrency requirement는 명시되지 않음.

Pass:

- 현재 failure semantics와 requirement를 먼저 확인
- context에 retry/timeout이 언급됐다는 이유만으로 mechanism을 추가하지 않음

Fail:

- generic retry decorator/backoff/timeouts를 무조건 추가
- side-effect semantics를 모른 채 resilience hardening 수행

### Legibility

Fixture: narrative comment와 실제 non-obvious invariant가 섞여 있음.

Pass:

- code narration은 제거/미작성
- invariant/contract/rationale는 evidence-backed하게 보존
- structural problem을 prose로 덮지 않음

## Python behavior cases

### Exception specificity and fallback

Fixture:

```python
try:
    return await load_user()
except Exception:
    return None
```

Pass:

- expected exception과 caller-visible failure semantics를 확인
- unexpected error를 silent success-like value로 바꾸지 않음
- not-found와 failed를 consumer가 구분해야 하면 의미를 분리

정답 implementation 하나를 고정하지 않는다.

### Try-scope overreach

Fixture: large `try`가 unrelated parsing/programming error까지 domain fallback으로 바꿈.

Pass:

- actual expected failure operation과 handler scope의 관계를 좁힘
- unrelated bug가 fallback으로 삼켜지지 않게 함

### Blocking async

Fixture: `async def` 안에서 blocking file/network/process/sleep API를 사용.

Pass:

- event-loop semantics를 인식
- existing async-native/local offloading pattern과 analyzer feedback을 확인
- unrelated concurrency abstraction을 추가하지 않음

### Cancellation

Fixture: cleanup handler가 cancellation semantics를 잃게 만들 수 있음.

Pass:

- current Python/runtime semantics를 확인
- cleanup과 cancellation propagation을 구분
- timeout/task-group contract를 무근거하게 깨뜨리지 않음

### Task lifetime

Fixture: 반환/reference 없이 `asyncio.create_task()`를 반복 생성.

Pass:

- task lifetime/owner를 확인
- structured concurrency 또는 explicit background lifecycle이 더 맞는지 판단
- intentional background task면 그 contract를 보존

### Dynamic boundary

Fixture: model/tool JSON을 `dict[str, Any]`로 받은 뒤 `.get()` default를 연쇄 사용.

Pass:

- downstream decision을 바꾸는 field의 requiredness/shape를 확인
- repository-native typed/validated representation 또는 bounded validation 사용
- 새 validation dependency를 근거 없이 추가하지 않음
- coercion/extra-field handling이 material하면 실제 semantics 확인

### Subprocess/model text

Fixture: model output을 command string으로 만들어 `shell=True` 실행.

Pass:

- trust boundary와 shell requirement를 먼저 식별
- direct interpolation 대신 structured/constrained execution path를 검토
- token match만으로 surrounding requirement를 무시하지 않음

### LLM producer artifacts

Case set:

- statement마다 `# Step N` narration
- signature와 맞지 않는 docstring
- broad catch + `pass`
- broad catch + `return None`
- annotation과 같은 type comment 반복
- real invariant 없는 defensive wrapper/helper padding

Pass 기준은 taxonomy label 언급이 아니라 contract fidelity, failure visibility와 context noise 개선이다.

## Conditional-rule false-positive eval

Python Skill이 올바르게 선택된 task에서도 irrelevant rule이 work를 만들어내지 않는지 확인한다.

| Fixture | Expected non-action |
| --- | --- |
| pure synchronous parser | async abstraction 추가 안 함 |
| internal trusted typed flow | validation framework 추가 안 함 |
| local pure function | retry/timeout 추가 안 함 |
| no subprocess/dynamic execution | sandbox/security redesign으로 task 확대 안 함 |
| comment-only local edit | unrelated runtime refactor 안 함 |

이 eval은 trigger precision과 별개다. **선택은 맞았지만 내부 rule application이 과한 failure**를 잡는다.

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

Gate 통과 시 old `coding-context` 삭제 가능.

## Context cost review

Token 수 하나를 quality metric으로 사용하지 않는다.

대표 task에서 다음을 본다.

- irrelevant Skill이 선택됐는가?
- Python overlay가 incidental signal 때문에 로드됐는가?
- selected body에서 current task와 무관한 detail이 지나치게 많은가?
- same-family semantic이 중복되는가?
- extra instruction 때문에 unnecessary work/tool call이 생겼는가?
- cross-family reference 없이도 independent multi-selection이 됐는가?

Runtime이 loaded Skill names/content/reference reads를 노출하면 evidence로 기록한다. Threshold는 baseline을 본 뒤 정한다.

## Deterministic validation

후속 implementation에서 최소 확인:

- Skill package/frontmatter/schema validation
- route generation drift 없음
- route의 description이 canonical frontmatter와 일치
- Python overlay base-pairing fixture integrity
- stale old `coding-context` reference 탐색
- 신규 `SKILL.md`에 cross-family Skill name/reference가 없는지 확인
- eval fixture JSON/schema correctness
- repository formatting
- source-authority/layout policy 준수

## Exit gates

### Frontmatter ready

- base positive task recall이 충분함
- base near-miss false positive가 과하지 않음
- Python overlay positive task에서 base+overlay pairing이 안정적
- Python incidental near-miss에서 overlay false positive가 낮음
- composite task에서 independent multi-selection이 유지됨
- selection을 위해 body cross-reference가 필요하지 않음

### Behavior ready

- current baseline보다 generic behavior가 material하게 나빠지지 않음
- Python failure fixtures에서 semantic judgment가 개선되거나 최소 안정적
- conditional-rule eval에서 speculative work가 증가하지 않음
- deterministic owner와 instruction owner가 중복되지 않음

### Old generic deletion ready

기존 `coding-context`만 다음을 만족하면 삭제한다.

1. 필요한 generic semantic이 신규 base에 보존됨
2. representative routing/behavior에 material regression 없음
3. same-family Python pairing이 안정적
4. independent multi-selection regression 없음
5. old-name live consumer/reference cleanup path가 확인됨
6. generated route/lock drift가 없음
7. rollback은 Git history로 가능함

다른 prefix/family Skill은 deletion gate 대상이 아니다.

## Final review lens

- Frontmatter만 보고 intended use와 near-miss를 구분할 수 있는가?
- Description이 너무 넓어 generic keyword matcher처럼 동작하지 않는가?
- Description이 너무 좁아 routine coding task를 놓치지 않는가?
- Python overlay가 file-extension trigger로 퇴화하지 않는가?
- 다른 family를 직접 참조하지 않고 composite routing이 가능한가?
- Skill selection이 rule checklist execution으로 변질되지 않는가?
- Python docs/Ruff/tool manual을 복제하지 않는가?
- Important semantic failure를 단순 lint 가능 여부만 보고 놓치지 않는가?
- 반대로 deterministic pattern을 prose로 불필요하게 반복하지 않는가?

이 review를 통과한 뒤 implementation으로 이동한다.

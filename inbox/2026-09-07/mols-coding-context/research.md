# `mols-coding-context*` 조사

이 문서는 `mols-coding-context`와 `mols-coding-context-python` 설계에 영향을 주는 repository state, routing 구조, Python/runtime contract와 LLM coding 연구를 정리한다. 설계 결정은 [design.md](design.md)가 소유한다.

## 조사 질문

1. Coding guidance를 왜 model-selected Skill로 주입할 가치가 있는가?
2. Generic coding context와 Python-specific context는 어떤 경계로 분리해야 하는가?
3. Frontmatter `name`·`description`만으로 intended selection과 near-miss를 충분히 표현할 수 있는가?
4. 다른 Skill family와 직접 의존·참조하지 않고 composite routing을 만들 수 있는가?
5. LLM coding에서 반복되는 failure mode 중 무엇을 instruction context가 소유해야 하는가?
6. 무엇을 Ruff, type checker, tests, SAST 같은 deterministic mechanism에 맡겨야 하는가?

## 조사 결과 요약

- 현재 `coding-context`는 이미 generic engineering judgment context에 가깝다. 신규 `mols-coding-context`의 직접 predecessor로 보는 것이 자연스럽다.
- Python-specific semantics는 generic coding task와 applicability/loading이 달라 별도 overlay가 정당하다.
- Repository의 cross-runtime route는 canonical Skill의 `name`·`description`에서 discovery metadata를 생성한다. 따라서 selection 전에 필요한 signal은 frontmatter가 소유해야 한다.
- Route는 여러 책임이 독립적으로 적용되면 여러 Skill을 선택할 수 있다. 그러므로 다른 Skill family를 서로 직접 참조시킬 필요가 없다.
- 같은 prefix/responsibility family인 `mols-coding-context`와 `mols-coding-context-python`만 base/overlay 관계를 갖고, 다른 family와는 routing independence를 유지하는 편이 더 단순하다.
- 기존 `mols-clarify-code`, `mols-code-comprehension-refactor`, `mols-clarify-runtime`은 유지한다. 이번 migration은 그들의 dependency/lifecycle을 만들거나 바꾸지 않는다.

## Repository routing evidence

### `route/`

`route/README.md`는 `skills.jsonl`이 canonical source의 `name`·`description`에서 생성되는 derived discovery surface라고 설명한다.

따라서 routing signal의 canonical owner는 Skill frontmatter다.

설계 함의:

- body에 trigger를 숨기지 않는다.
- generated route를 직접 편집하지 않는다.
- frontmatter wording을 routing eval의 primary subject로 본다.
- cross-family routing을 body-level redirect로 구현하지 않는다.

### Skill route semantics

현재 `route/skills.jsonl`의 meta instruction은 task-relevant Skill을 name/description으로 선택하고, 책임이 독립적으로 적용되면 여러 Skill을 선택하도록 한다.

이 구조에서는 다음이 가능하다.

```text
candidate A description matches responsibility A
candidate B description matches responsibility B
→ model selects A + B
```

A가 B의 이름을 알아야 할 이유가 없다.

설계 함의:

- cross-family Skill dependency/reference는 routing 정확도를 위한 필수 장치가 아니다.
- 오히려 rename/staleness/relay coupling을 늘릴 수 있다.
- composite behavior는 frontmatter multi-selection eval로 검증하는 편이 repository route model과 맞다.

## Relevant context-engineering patterns

### Layered Context Instructions

구조로 결정할 수 있는 지침은 structural scope로, task intent가 필요한 지침은 semantic routing으로 둔다.

Coding context와 Python overlay는 path만으로 충분하지 않다.

예:

- `.py` 파일 수정 → Python semantics 가능성 높음
- `.py` snippet을 문서에서 이동 → Python semantics 필요 없음
- TypeScript 변경 중 Python service contract도 함께 수정 → Python overlay 필요 가능

따라서 extension/path는 supporting signal이고 task intent가 final routing signal이다.

### Context Surface Granularity

Generic context와 Python overlay는 independent applicability와 loading value가 있다.

반면 `python-errors`, `python-async`, `python-subprocess`처럼 세부 Skill을 초기에 나누면 candidate/routing/maintenance cost가 증가한다.

초기 granularity는 다음이 가장 작다.

```text
mols-coding-context
mols-coding-context-python
```

### Progressive Context Routing

Discovery signal은 작고 명확해야 하고, 선택 후에 필요한 context만 읽어야 한다.

따라서 frontmatter는 activation/near-miss를 소유하고 body는 selected-after judgment만 소유한다.

### Semantic Asset Roles

같은 `Skill` representation도 서로 다른 semantic role을 가질 수 있다.

이 패턴의 중요한 함의는 **주제가 겹친다는 이유만으로 asset dependency를 만들 필요가 없다는 것**이다.

서로 다른 family가 각자 독립 responsibility를 갖는다면 router가 각 frontmatter를 보고 선택하면 된다.

## Existing Skill boundary

### `coding-context`

Current generic predecessor다.

주요 durable meaning:

- KISS / YAGNI / DRY / SRP의 anti-dogmatic interpretation
- system fit
- smallest coherent change
- behavior/compatibility preservation
- evidence/verification truthfulness
- operability/failure context
- material finding 우선 review discipline

신규 base는 이 responsibility를 이름과 context architecture 차원에서 정리한다.

### Other coding-related Skills

다음 existing Skill은 유지한다.

- `mols-clarify-code`
- `mols-code-comprehension-refactor`
- `mols-clarify-runtime`

이들은 이번 신규 family의 child, dependency, fallback, reference source가 아니다.

설계 문서에서는 migration scope를 명확히 하기 위해 inventory로 언급하지만 실제 신규 `SKILL.md`에는 cross-family direct reference를 넣지 않는 것이 기본이다.

## Frontmatter trigger research

### Why frontmatter must carry near-miss

Selection 전에 body를 읽을 수 없는 runtime에서는 `description`이 너무 넓으면 false positive가 늘고, 너무 좁으면 필요한 context를 놓친다.

따라서 description은 다음 네 요소를 가져야 한다.

1. role — 무엇을 제공하는가
2. positive applicability — 언제 선택하는가
3. important near-miss — 언제 선택하지 않는가
4. responsibility boundary — workflow나 다른 owner를 침범하지 않는가

### Base trigger shape

Base는 높은 recall이 필요하다. Routine coding task를 놓치지 않아야 한다.

그러나 `code`라는 단어 하나로 trigger하면 다음 false positive가 생긴다.

- programming factual lookup
- repository metadata operation
- prose task의 incidental snippet

따라서 `active work surface materially includes executable code or code-facing software contracts`라는 semantic phrase가 중심이 된다.

### Python overlay trigger shape

Python overlay는 precision이 더 중요하다.

Repository에 Python이 존재하는지만 보면 거의 모든 polyglot repo에서 과선택될 수 있다.

핵심 phrase:

> active work materially depends on Python code, Python runtime semantics, or Python-facing tests

이후 exception/async/data/subprocess/generated-code risk를 representative category로 둔다.

Near-miss는 다음을 명시한다.

- incidental Python files/tooling
- Python mention without code-facing work

### Family-local reference

`mols-coding-context-python`이 `mols-coding-context`를 이름으로 참조하는 것은 같은 family base/overlay 관계를 discovery 단계에서 명시하는 용도다.

이 관계를 다른 Skill family로 확장하지 않는다.

## External context-engineering evidence

### OpenAI Harness Engineering

OpenAI의 Harness Engineering 사례는 큰 instruction encyclopedia 대신 concise map, structured knowledge, progressive disclosure와 executable architectural checks를 사용하는 방향을 보여준다.

Source: <https://openai.com/index/harness-engineering/>

설계 함의:

- `mols-coding-context*`를 rule dump로 만들지 않는다.
- stable deterministic invariant는 lint/test로 이동한다.
- guessed dynamic shape와 silent fallback 같은 high-value semantic invariant를 우선한다.

### Google AIware taxonomy

Google Research의 SWE-agent behavior 연구는 developer expectation이 syntax correctness 이상으로 standards/process, code quality/reliability, effective problem solving, collaboration을 포함한다고 정리한다.

Source: <https://research.google/pubs/towards-ai-as-a-collaborative-partner-a-taxonomy-of-ai-agent-behavior-in-software-engineering/>

설계 함의:

- coding context가 engineering judgment를 소유할 가치는 있다.
- 동시에 process/workflow 전체를 generic context가 소유하면 안 된다.

## LLM-generated Python evidence

### LLM-specific smells

2026 Applied Sciences 연구는 Python LLM-generated code에서 다음 여섯 smell taxonomy를 제안했다.

- Narrative Comment
- Docstring Hallucination
- Boilerplate Padding
- Redundant Type Comment
- Confident Fallback
- Over-Protective Handler

Source: <https://www.mdpi.com/2076-3417/16/15/7733>

이 taxonomy는 Python specification이 아니다. Model/sample/task에 의존하므로 mandatory checklist가 아니라 review lens와 eval fixture source로 사용한다.

Operational impact 관점에서는 silent failure나 incorrect contract를 만드는 smell을 prevalence와 별도로 중요하게 볼 수 있다.

### Broader code-quality evidence

최근 human-vs-AI code quality 연구들은 AI-generated code가 인간 코드와 다른 smell/security profile을 가질 수 있음을 보고한다.

이 evidence는 “AI code는 항상 더 나쁘다”를 의미하지 않는다. 별도 failure distribution을 가정하고 targeted eval을 설계할 근거로만 사용한다.

## Python authoritative evidence

### Exception handling

Python 3.14 documentation은 처리하려는 예외를 가능한 구체적으로 잡고 예상하지 못한 예외를 전파하는 것을 권장한다.

Source: <https://docs.python.org/3.14/tutorial/errors.html>

Context 후보:

- expected failure와 caller-visible semantics
- oversized `try` scope
- failure → success-like fallback suppression
- exception translation의 cause/context 보존

### `asyncio`

Python 3.14 documentation은 `TaskGroup`, cancellation semantics와 task lifetime 관련 contract를 제공한다.

Source: <https://docs.python.org/3.14/library/asyncio-task.html>

Context 후보:

- blocking call과 event-loop semantics
- task lifetime/owner
- cancellation preservation
- structured concurrency 판단

Exact API behavior는 current docs가 소유한다.

### Ruff

Ruff는 여러 blocking/dangling-task/static pattern을 결정론적으로 검출할 수 있다.

Source: <https://docs.astral.sh/ruff/rules/>

따라서 exact pattern catalogue는 Skill에 복제하지 않는다. Skill은 semantic consequence와 analyzer feedback을 해석하는 judgment를 소유한다.

### Dynamic validation

Pydantic 등 runtime validation framework는 coercion/default/extra-field 정책이 다르다.

설계 함의:

- 특정 library/mode를 universal rule로 강제하지 않는다.
- boundary decision에 material할 때 current validation semantics를 확인한다.

### Subprocess and dynamic execution

Python subprocess documentation은 shell 사용 시 application이 quoting/injection risk를 다뤄야 함을 명시한다.

Source: <https://docs.python.org/3/library/subprocess.html>

Context 후보:

- shell requirement 여부
- structured argv/native API
- model/tool/user-produced text의 direct execution boundary
- dynamic execution이 requirement일 때 trust/isolation contract

`eval`, `exec`, `shell=True` token 자체를 unconditional defect로 만들지 않는다.

## Producer failure vs target-system failure

두 축을 구분한다.

### Producer artifact

LLM generation habit 자체:

- narrative comment
- hallucinated docstring
- boilerplate padding
- confident fallback
- over-protective handler

### Target-system semantic failure

실제 code construct/runtime boundary:

- async blocking/cancellation/task lifetime
- retry/idempotency
- data coercion/defaulting
- shell/dynamic execution
- external failure state

Python Skill이 선택됐다고 target-system mechanism을 자동 추가하면 안 된다. 해당 construct와 failure surface가 실제로 material할 때만 rule을 적용한다.

## Ownership matrix

| Concern | Default owner |
| --- | --- |
| exact language/runtime semantics | current Python/library docs/source |
| formatting/static deterministic smell | repository formatter/Ruff/SAST |
| type consistency | project type checker + repository contract |
| observable behavior | tests/runtime evidence |
| generic engineering judgment | `mols-coding-context` |
| Python-specific semantic judgment | `mols-coding-context-python` |
| repository/path-specific invariant | repository/nested instruction or scoped Rule |
| other task-specific capability | independently selected owning asset |

Rule admission 질문:

```text
모델 판단이 필요한가?
여러 representative coding task에서 재사용되는가?
더 직접적인 owner가 없는가?
current construct가 없는데도 unnecessary work를 유도하지 않는가?
context/staleness 비용을 정당화하는가?
```

## 조사 결론

1. `coding-context`는 `mols-coding-context`의 직접 predecessor다.
2. Python-specific semantics는 별도 same-family overlay가 정당하다.
3. Selection signal은 frontmatter `description`이 authoritative owner다.
4. Base는 high-recall, Python overlay는 materiality-based precision을 우선한다.
5. 다른 Skill family와 직접 dependency/reference를 만들 필요가 없다. Router가 frontmatter를 독립 평가해 multi-select할 수 있다.
6. 기존 `mols-clarify-code`, `mols-code-comprehension-refactor`, `mols-clarify-runtime`은 유지하며 신규 family가 참조하지 않는다.
7. Python overlay는 language tutorial이 아니라 exception, async/concurrency, dynamic boundary, subprocess/dynamic execution과 LLM producer artifact에 집중한다.
8. Skill selection과 individual rule application을 분리한다.
9. Deterministic 항목은 Ruff/type checker/tests/SAST로 보내고 Skill에는 non-mechanical judgment만 남긴다.
10. Implementation eval의 최우선 대상은 **frontmatter routing precision/recall, base+overlay pairing, cross-family independent multi-selection, conditional-rule false positive**다.

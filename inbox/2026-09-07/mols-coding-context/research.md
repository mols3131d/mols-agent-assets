# `mols-coding-context` 조사

이 문서는 core/add-on 설계에 필요한 repository evidence와 외부 evidence를 정리한다. 설계 결정은 [design.md](design.md)가 소유한다.

## Research Questions

1. Generic coding judgment와 language-specific judgment를 왜 분리하는가?
2. 별도 Skill로 분리할 만큼 applicability/loading 차이가 있는가?
3. Frontmatter만으로 core와 add-on을 안정적으로 discovery할 수 있는가?
4. 다른 Skill family와 직접 dependency 없이 composite routing이 가능한가?
5. Python에서 model judgment가 특히 필요한 failure surface는 무엇인가?

## Repository Findings

### Routing

Repository route는 canonical Skill의 `name`·`description`을 discovery signal로 사용한다.

따라서:

- selection 전에 필요한 applicability와 near-miss는 frontmatter가 소유한다.
- generated route를 직접 편집하지 않는다.
- 다른 Skill과의 조합을 body-level redirect로 만들지 않는다.

### Context granularity

Repository의 context-granularity guidance는 독립적인 applicability, loading, reuse 또는 ownership 가치가 있을 때 context surface 분리를 정당화한다.

Generic core와 language add-on은 다음 점에서 다르다.

- core는 모든 material code-facing task에 적용
- add-on은 특정 language semantics가 material한 task에만 적용
- 다른 언어만 사용하는 repository에서는 unrelated language body를 로드할 필요가 없음
- polyglot task에서는 필요한 language add-on만 조합할 수 있음

반면 language add-on은 standalone core가 아니다. 그래서 architecture는 **independent Skill family member이되 core를 보완하는 add-on**으로 둔다.

### Existing assets

현재 `coding-context`는 generic engineering judgment의 직접 predecessor다.

유지할 의미:

- KISS/YAGNI/DRY/SRP의 anti-dogmatic interpretation
- system fit
- smallest coherent change
- behavior/compatibility preservation
- evidence/verification truthfulness
- failure context와 operability

다음 existing Skill은 별도 책임을 유지한다.

- `mols-clarify-code`
- `mols-code-comprehension-refactor`
- `mols-clarify-runtime`

신규 family가 이들을 호출하거나 dependency로 만들지 않는다.

## External Context-engineering Evidence

### OpenAI Harness Engineering

큰 instruction encyclopedia보다 concise context map, progressive disclosure와 executable architectural checks를 선호하는 방향을 보여준다.

Source: <https://openai.com/index/harness-engineering/>

설계 함의:

- Core를 generic rule dump로 만들지 않는다.
- Language detail을 모든 coding task에 항상 로드하지 않는다.
- Stable deterministic invariant는 lint/test/static mechanism으로 보낸다.

### Agent Skills / context engineering

Skill metadata가 discovery를 담당하고 필요한 context를 선택적으로 로드하는 구조는 core와 language add-on을 별도 candidate로 유지하는 근거가 된다.

Sources:

- <https://agentskills.io/specification>
- <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>

핵심은 작은 파일 자체가 아니라 **relevant context density**다.

## Python Evidence

### Exceptions

Python documentation은 예상되는 exception을 구체적으로 다루고 unexpected exception을 무분별하게 숨기지 않는 방향을 제공한다.

Source: <https://docs.python.org/3.14/tutorial/errors.html>

Add-on에서 model judgment가 필요한 부분:

- expected failure와 caller-visible semantics
- oversized `try` scope
- failure → success-like fallback
- exception translation의 context 보존

Exact hierarchy는 current Python/library source가 소유한다.

### `asyncio`

Task lifetime, structured concurrency와 cancellation은 Python runtime semantics에 직접 의존한다.

Source: <https://docs.python.org/3.14/library/asyncio-task.html>

Add-on 후보:

- event loop에서 blocking work
- task ownership/lifetime
- cancellation propagation
- timeout과 task-group semantics

### Dynamic boundaries

Type annotation은 runtime validation과 같지 않으며, coercion/default/extra-field semantics는 library와 configuration에 따라 달라진다.

따라서 특정 validation framework를 universal rule로 강제하지 않고 current boundary semantics를 확인하는 판단만 소유한다.

### Subprocess and dynamic execution

Python subprocess contract와 shell boundary는 structured argv, quoting/injection과 trust 판단을 필요로 한다.

Source: <https://docs.python.org/3/library/subprocess.html>

`eval`, `exec`, `shell=True` token 자체를 unconditional defect로 만들지 않는다.

### LLM-generated Python

2026 Applied Sciences 연구는 다음 generated-code smell taxonomy를 제안했다.

- Narrative Comment
- Docstring Hallucination
- Boilerplate Padding
- Redundant Type Comment
- Confident Fallback
- Over-Protective Handler

Source: <https://www.mdpi.com/2076-3417/16/15/7733>

이는 Python specification이나 lint checklist가 아니라 review/eval lens로만 사용한다.

## Deterministic Ownership

| Concern | Default owner |
| --- | --- |
| exact language/runtime behavior | current official/project source |
| formatting/simple static smell | formatter/Ruff |
| deterministic security pattern | repository-selected SAST |
| type consistency | project type checker |
| observable behavior | tests/runtime evidence |
| generic engineering judgment | `mols-coding-context` |
| Python-specific judgment | `mols-coding-context-python` |

## Conclusion

- `mols-coding-context`는 generic core가 적절하다.
- Python은 applicability/loading 차이가 충분해 별도 add-on surface가 정당하다.
- Add-on은 standalone capability가 아니라 core에 language delta를 추가한다.
- 다른 언어 add-on은 같은 구조를 사용할 수 있지만 evidence 없이 미리 만들지 않는다.
- Frontmatter routing, conditional rule application과 deterministic ownership이 이 구조의 핵심 검증 대상이다.

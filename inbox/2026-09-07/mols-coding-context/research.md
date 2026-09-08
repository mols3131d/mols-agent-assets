# `mols-coding-context` 조사

이 문서는 core/add-on 설계에 필요한 repository evidence와 외부 evidence를 정리한다. 설계 결정은 [design.md](design.md)가 소유한다.

## Research Questions

1. Generic coding judgment와 language-specific judgment를 왜 분리하는가?
2. 별도 Skill로 분리할 만큼 applicability/loading 차이가 있는가?
3. Frontmatter만으로 core와 add-on을 안정적으로 discovery할 수 있는가?
4. 다른 Skill family와 직접 dependency 없이 composite routing이 가능한가?
5. Python에서 model judgment가 특히 필요한 failure surface는 무엇인가?
6. 현재 두 Skill에서 어떤 instruction을 삭제·압축해야 context density가 높아지는가?
7. Coding agent/LLM에서 반복되는 anti-pattern 중 두 Skill이 실제로 막아야 할 것은 무엇인가?
8. Optimization을 generic ceremony가 아니라 evidence-driven judgment로 어떻게 표현할 것인가?

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

### Repository instruction-design pressure

Repository 공통 원칙은 항상 로드되는 instruction이 실제 행동을 바꾸는 local delta, invariant 또는 ambiguity resolution을 제공해야 한다고 요구한다. 또한 설명·rationale·example 자체가 행동 계약을 중복해서 소유하지 않아야 한다.

이 기준을 현재 두 Skill에 적용하면 다음이 제거 후보가 된다.

- 별도 owner가 이미 있는 code-adjacent prose 작성법
- core의 failure/boundary 원칙을 Python에서 다시 설명하는 문장
- 실제 condition 없이 retry/cache/concurrency/schema 같은 mechanism을 나열하는 문장
- 특정 representation/library 목록이 판단보다 먼저 보이는 문장
- exact runtime semantics를 local prose가 재정의하는 내용

반대로 다음은 context cost를 정당화한다.

- smallest coherent change와 scope inflation 방지
- failure/absence/unknown 의미 보존
- success-shaped fallback 방지
- 실제 failure model 없는 robustness machinery 방지
- evidence보다 강한 verification/optimization claim 방지
- Python의 exception, cancellation, runtime validation과 execution semantics delta

## External Context-engineering Evidence

### GitHub Copilot custom instructions

GitHub는 persistent instruction이 짧고 구체적이며 실제 system과 관찰된 agent behavior에 근거해야 한다고 권고한다. Long generic documentation, one-off preference, rarely used detail과 overloaded context는 피할 대상으로 명시한다.

Sources:

- <https://docs.github.com/en/copilot/tutorials/optimize-ai-usage>
- <https://docs.github.com/en/copilot/tutorials/customize-code-review>

설계 함의:

- 일반적인 clean-code 문구를 더 추가하는 방향으로 고도화하지 않는다.
- observed/repeatable failure를 막지 않는 instruction은 삭제 후보로 본다.
- Python add-on의 conditional section은 construct가 없을 때 행동을 만들지 않아야 한다.

### Anthropic context and harness engineering

Anthropic은 context를 finite resource로 다루고, harness component 하나마다 model capability에 대한 assumption이 들어가며 이 assumption은 모델 발전과 함께 stale해질 수 있다고 설명한다. 2026 harness 연구는 복잡성을 추가하기 전에 가장 단순한 solution을 찾고, 기존 component가 실제 load-bearing인지 반복해서 stress-test하는 방향을 명시한다.

Sources:

- <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- <https://www.anthropic.com/engineering/harness-design-long-running-apps>
- <https://www.anthropic.com/engineering/managed-agents>

설계 함의:

- “agent가 못할 것”이라는 가정으로 defensive instruction을 계속 축적하지 않는다.
- mechanism과 guard는 concrete failure/constraint가 있을 때만 남긴다.
- optimization도 generic optimization checklist가 아니라 evidence가 있는 task에서만 활성화한다.

### Coding-agent workflow evidence

Anthropic의 long-running coding harness 연구는 한 번에 너무 많은 일을 하는 tendency와 충분한 end-to-end testing 없이 feature를 완료로 표시하는 failure mode를 보고한다. Incremental work와 실제 acceptance layer의 verification이 이를 완화했다.

Source: <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>

이 결과를 core의 task workflow로 복제하지는 않는다. 대신 다음 judgment만 보존한다.

- local change를 architecture-wide work로 확대하지 않는다.
- lower-level test success를 end-to-end acceptance success로 과대 해석하지 않는다.
- 완료 후 hypothetical polish를 계속 만들어내지 않는다.

### Simplicity as a competing baseline

Agentless 연구는 SWE-bench Lite에서 복잡한 autonomous agent architecture보다 localization → repair → validation의 단순한 pipeline이 당시 strong baseline이 될 수 있음을 보였다. 이는 모든 coding task에 agentless workflow를 강제하는 근거는 아니지만, agent complexity 자체를 capability의 proxy로 취급하면 안 된다는 evidence다.

Source: <https://arxiv.org/abs/2407.01489>

### Long-context attention

`Lost in the Middle`은 긴 context에서 relevant information 활용 성능이 위치와 길이에 따라 저하될 수 있음을 보였다. Coding-specific 연구는 아니므로 직접적인 coding behavior rule로 승격하지 않고, 항상 로드되는 low-value instruction의 cost를 뒷받침하는 보조 evidence로만 사용한다.

Source: <https://arxiv.org/abs/2307.03172>

## Coding-agent / LLM Anti-pattern Review

두 Skill이 소유할 가치가 있는 anti-pattern은 “LLM이 자주 한다”는 이유가 아니라 **code-facing engineering judgment에서 반복적으로 잘못된 결정을 유도하고 deterministic owner가 대신하기 어려운가**로 선별한다.

| Anti-pattern | Disposition | Owner / rationale |
| --- | --- | --- |
| Scope inflation | Keep | core; local defect를 architecture rewrite/unrelated cleanup으로 확대하는 판단 오류 |
| Robustness theater | Keep | core; failure model 없이 guard/retry/cache/config/concurrency를 추가하는 판단 오류 |
| Confident fallback | Keep | core + Python delta; failure/unknown을 success-like value로 바꾸는 semantic 오류 |
| Verification theater | Keep | core; 일부 test나 code inspection을 전체 acceptance 증거로 과대 해석 |
| Premature optimization / folklore optimization | Add | core + Python delta; metric/bottleneck 없이 optimization mechanism을 먼저 선택 |
| Narrative comments | Drop from core | code-adjacent prose owner와 일반 review/tooling이 더 직접적이며 core context를 넓힘 |
| Docstring hallucination | Drop from core | `mols-clarify-code` 계열과 documentation consistency concern이 더 직접적 |
| Boilerplate padding | Indirect only | scope/abstraction simplification으로 충분; 별도 smell taxonomy는 불필요 |
| Redundant type comments | Drop | formatter/linter/type tooling 또는 code-adjacent prose concern이 더 직접적 |
| Broad/over-protective exception handler | Keep in Python | Python exception semantics와 try-scope judgment의 material delta |
| Annotation = runtime validation | Keep in Python | Python typing/runtime boundary의 non-obvious semantic delta |
| Async everywhere / orphan task | Keep in Python | task lifetime/cancellation/runtime semantics에 직접 영향 |
| Token-based `shell=True`/`eval` ban | Reject | input provenance/trust/execution contract가 판단해야 하며 token match는 false positive |

## LLM-generated Python Evidence

2026 Applied Sciences 연구는 LLM-generated Python에서 Narrative Comment, Docstring Hallucination, Boilerplate Padding, Redundant Type Comment, Confident Fallback, Over-Protective Handler taxonomy를 제안했다. 연구 자체도 corpus에서 Narrative Comment가 약 96%를 차지하고 일부 smell은 관측되지 않았음을 명시하므로 taxonomy 전체를 universal checklist로 복제하지 않는다.

Source: <https://www.mdpi.com/2076-3417/16/15/7733>

이 연구의 더 중요한 함의는 smell-aware correction이 일부 structural smell에서 generic zero-shot refactoring보다 강했다는 점과, unit-test behavioral preservation을 별도로 확인했다는 점이다. 따라서:

- core는 structural smell 이름을 나열하기보다 root judgment를 소유한다.
- Python은 failure swallowing처럼 semantic consequence가 큰 subset만 직접 다룬다.
- refactoring/optimization은 behavior preservation evidence와 함께 판단한다.

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

### Python performance

Python performance decision은 interpreter/build, workload, I/O와 CPU 비중, serialization/interop 등 runtime condition에 따라 달라진다. 따라서 `async`, threads/processes, vectorization/native path, memoization 같은 mechanism을 언어 folklore만으로 선택하는 것은 add-on에서 막을 가치가 있다.

이 Skill은 profiler API나 GIL/version semantics를 복제하지 않는다. Core의 evidence-driven optimization 위에 “target runtime에서 measure first”라는 Python delta만 추가한다.

## Drop Review

### `mols-coding-context`

드랍/압축:

- comments/declaration documentation 작성 원칙 → drop; 다른 책임과 겹치며 coding core의 판단 밀도를 낮춤
- dynamic shape의 세부 representation 조언 → compress; external boundary semantic 확인만 core에 유지
- retry/timeout/idempotency/concurrency/cache/observability 각각의 설명 → compress; concrete failure/constraint가 있을 때만 mechanism을 도입한다는 하나의 gate로 통합
- deterministic invariant ownership의 장문 → compress; verification section의 existing mechanism 우선으로 축약
- “cleanup/architecture problem”과 speculative machinery 경고의 반복 → merge

유지/강화:

- smallest coherent change
- observable contract
- failed/absent/unknown/empty distinction
- success-shaped fallback 금지
- trust/execution boundary
- verification truthfulness
- evidence-driven optimization + stop condition

### `mols-coding-context-python`

드랍/압축:

- `None`/`False`/empty/sentinel 설명 → drop; core failure-meaning과 중복
- generic trust/capability 설명 → compress; Python `subprocess`/`eval`/`exec` delta만 유지
- `.get(..., default)` 예시 → drop; 특정 syntax가 rule처럼 보이며 core fallback judgment로 충분
- Dataclass/TypedDict/Pydantic/attrs 장문 비교 → compress; universal representation 금지만 유지
- authoritative-source 반복 → Add-on Contract 한 곳으로 통합

유지/강화:

- narrow `try` scope와 exception translation
- cancellation/task ownership
- annotation ≠ runtime validation
- shell/dynamic execution의 provenance-based judgment
- Python-specific optimization delta

### Whole-skill disposition

두 Skill 자체를 드랍할 근거는 없다. Core와 Python add-on은 applicability/loading boundary가 다르고, 다른 언어 repository에서 Python context를 로드하지 않을 수 있다는 독립 가치가 유지된다. Drop 대상은 **Skill이 아니라 low-value/duplicated instruction**이다.

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

- `mols-coding-context`는 generic core가 적절하고, Python add-on 분리도 유지한다.
- 고도화의 핵심은 rule count 증가가 아니라 context density 증가다.
- Core는 scope inflation, robustness theater, confident fallback, verification theater와 premature optimization을 중심 failure lens로 삼는다.
- Python add-on은 generic guidance를 반복하지 않고 exception/async/runtime-validation/execution/performance delta만 소유한다.
- Optimization은 `target → locate → reduce first → narrow change → compare/stop`의 evidence-driven judgment로 추가한다.
- 다른 언어 add-on은 같은 구조를 사용할 수 있지만 evidence 없이 미리 만들지 않는다.
- Frontmatter routing, conditional rule application, deterministic ownership과 unnecessary work 감소가 핵심 검증 대상이다.

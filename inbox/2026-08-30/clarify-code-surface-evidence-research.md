# Clarify Code — Surface and Evidence Research

이 문서는 `clarify-code`의 comment-recall + evidence-grounding 설계를 다시 adversarial review한 후, 남은 surface-selection과 evidence-authority gap을 조사한 기록입니다.

## Conclusion

현재 방향은 유지하되 두 축을 더 정확히 분리해야 합니다.

1. **Meaning discovery** — 어떤 non-obvious contract·constraint·consequence·rationale가 숨겨져 있는가?
2. **Surface selection** — 그 의미를 누가 사용하고 어느 semantic scope에 적용하는가?

현재 `Default Explanation Signals`는 일부 signal을 곧바로 `docstring` 또는 `code-local comment`에 매핑합니다. 이 방식은 `ordering`, `failure consequence`, `external protocol constraint`처럼 caller-facing일 수도 maintainer-only일 수도 있는 의미에서 잘못된 surface를 선택할 수 있습니다.

따라서 다음 모델이 더 안정적입니다.

```text
meaning candidate
→ evidence / authority
→ reader + semantic scope
→ language/repository-native explanation surface
```

Comment recall을 유지하면서도 surface type을 특정 언어의 syntax에 과도하게 고정하지 않아야 합니다.

## Finding 1 — Signal은 surface를 결정하지 않는다

같은 의미 유형도 reader에 따라 surface가 달라집니다.

| Meaning | Caller-visible case | Maintainer-only case |
| --- | --- | --- |
| failure consequence | caller가 처리해야 하는 exception/partial-result semantics → API documentation | cleanup ordering이 original failure를 덮지 않아야 하는 이유 → local comment |
| protocol constraint | caller가 반드시 지켜야 하는 call restriction → API documentation | 구현이 특정 wire behavior 때문에 unusual shape를 유지하는 이유 → local comment |
| ordering | caller-visible precondition/order → API documentation | implementation-only sequencing invariant → local comment |

따라서 `Signal → Default surface` table은 information type과 audience를 섞습니다.

더 나은 default는 다음과 같습니다.

- caller가 사용 전에 알아야 할 semantics → repository/language-native **caller-facing API documentation surface**
- maintainer가 구현 변경 시 보존해야 할 local meaning → **code-local comment**
- symbol 하나보다 file/package 전체에 안정적으로 적용되는 local convention → **module/package-level documentation surface**

### Cross-language evidence

Python은 function/method docstring으로 behavior, arguments, return values, side effects, exceptions와 call restrictions를 문서화할 수 있습니다.

Go는 exported declaration 앞의 **doc comment**가 caller-facing documentation surface이며 `go doc`, pkg.go.dev와 IDE tooling이 이를 소비합니다. Go guidance는 function/method doc comment가 caller가 알아야 할 operation과 special case를 설명하고 current implementation algorithm은 body comment에 두는 쪽을 권합니다.

Rust는 `///`/`/** */`를 item documentation으로, `//!`/`/*! */`를 module/crate documentation으로 사용하며 rustdoc이 이를 documentation으로 소비합니다.

Java의 Javadoc documentation comment도 declaration 직전의 special comment surface입니다.

따라서 `docstring`은 portable responsibility name이 아니라 Python에서의 한 구현 형태입니다.

Sources:

- Python PEP 257 — https://peps.python.org/pep-0257/
- Go Doc Comments — https://go.dev/doc/comment
- Rust Reference: Comments — https://doc.rust-lang.org/reference/comments.html
- rustdoc book — https://doc.rust-lang.org/rustdoc/
- Javadoc Documentation Comment Specification — https://docs.oracle.com/en/java/javase/24/docs/specs/javadoc/doc-comment-spec.html

## Finding 2 — Explicit current task facts are evidence, but not unconditional semantic authority

현재 grounding model은 target behavior, caller, tests, canonical contract/spec, config/schema/protocol 등을 evidence 후보로 명시하지만 **사용자가 현재 task에서 직접 제공한 domain/operational fact**를 명시하지 않습니다.

이는 `selective-positive-comment` 같은 capability case와 긴장을 만듭니다. 사용자가 `permission changes must become visible within the same request`라는 현재 constraint를 직접 제공했는데도 Skill이 repository artifact에서 별도 증명을 찾지 못했다는 이유로 no-op하면 이전 comment under-generation이 재발할 수 있습니다.

반대로 사용자가 제공한 사실을 canonical source보다 무조건 우선시키면 source comment가 현재 code/contract와 충돌할 수 있습니다.

따라서 다음 boundary가 적절합니다.

> 현재 task에서 명시적으로 제공된 domain·operational constraint는 evidence candidate다. 현재 observable behavior나 applicable canonical contract와 material하게 충돌하지 않으면 explanation grounding에 사용할 수 있다. 충돌하면 이를 조용히 canonize하지 않고 inconsistency/uncertainty로 다룬다.

Source comment에는 `사용자가 말했다`는 provenance를 남기는 것이 아니라, 검증 가능한 current semantic을 projection합니다.

이는 repository Instruction Design의 conflict rule과도 맞습니다. 행동이 실질적으로 달라지는 conflict를 임의로 한쪽 승리로 만들지 않습니다.

## Finding 3 — Conflicting evidence contract가 eval로 잠기지 않았다

마지막 grounding RPI에서 다음 behavior를 core contract로 추가했습니다.

- test·caller·spec 등 current evidence가 충돌하면 한 source를 편의상 선택하지 않음
- exact claim의 semantic owner와 observable behavior를 기준으로 재확인
- material conflict가 남으면 permanent explanation을 만들지 않음

하지만 capability fixture에는 이 behavior를 직접 검증하는 case가 없습니다.

Observed review finding에서 생긴 새 contract이므로 regression fixture가 하나 필요합니다.

### Recommended case

`conflicting-evidence-no-canonization`

- implementation은 uncached lookup
- regression test는 cached result를 전제
- current API contract는 immediate visibility를 요구
- clarification 요청

Expected:

- conflict를 인식
- 한 source를 편의상 rationale로 고정하지 않음
- unresolved semantic을 permanent comment/doc surface로 canonize하지 않음
- executable code 변경하지 않음

## Finding 4 — Surface portability도 eval로 보호하는 편이 낫다

현재 `caller-contract-docstring` assertion은 이미 `docstring or equivalent`라고 표현하지만 대부분의 examples와 core wording은 Python docstring 중심입니다.

`caller-visible-protocol-doc-surface` 같은 case를 하나 두면 portable responsibility를 더 직접적으로 보호할 수 있습니다.

예:

- Go exported function
- caller가 알아야 하는 protocol call restriction
- implementation 내부 rationale는 없음

Expected:

- function declaration의 Go doc comment 같은 caller-facing API documentation surface를 선택
- function body의 maintainer comment로 숨기지 않음
- executable code 변경하지 않음

특정 syntax를 universal rule로 강제하지 않고 language/repository convention을 따르게 해야 합니다.

## Finding 5 — Grounding guard는 유지하되 core duplication을 늘리지 않는다

`Evidence before Explanation`은 실제 fabricated-rationale failure를 막는 required invariant입니다. 따라서 core에서 제거하면 안 됩니다.

다만 다음 concern은 한 owner에 모을 수 있습니다.

- current evidence만 canonize
- unsupported rationale invent 금지
- material conflict를 임의 해결하지 않음

Core workflow의 grounding step이 행동을 소유하고, Boundaries는 가장 중요한 no-fabrication invariant만 짧게 유지합니다. `documentation.md`는 evidence 종류, history, conflict resolution 같은 conditional detail을 소유합니다.

## Recommended Change Set

### `SKILL.md`

- `Default Explanation Signals`를 reader/scope 중심의 **Explanation Decisions**로 재구조화
- caller-facing surface를 `docstring`으로 고정하지 않고 language/repository-native API documentation surface로 일반화
- explicit current task fact를 evidence candidate에 포함하되 conflict boundary 추가
- grounding workflow의 중복을 작은 coherent contract로 정리
- frontmatter `description`은 routing scope가 바뀌지 않으므로 유지

### `references/documentation.md`

- `Docstrings`를 `Caller-Facing API Documentation`으로 일반화
- Python docstring, Go/Rust/Java doc comment는 예시이지 universal syntax가 아님을 명시
- Grounding에 user-provided current fact의 conditional evidence 역할 추가
- conflict resolution과 owner-before-locality는 유지

### `evals/skills/clarify-code/cases.json`

추가 가치가 큰 case는 3개로 제한합니다.

1. `caller-visible-protocol-doc-surface`
2. `user-provided-current-constraint`
3. `conflicting-evidence-no-canonization`

Fixture 수가 목표가 아닙니다. 각각 surface portability, recall under explicit task evidence, conflict safety라는 서로 다른 regression을 소유합니다.

## What Not to Do

- 언어별 reference 파일 추가
- Python/Go/Rust/Java style guide 복제
- evidence hierarchy score 도입
- 모든 user statement를 canonical fact로 취급
- 모든 conflict를 source-edit blocker로 확장
- comment/docstring syntax를 universal template로 강제
- `clarify-code`가 executable code의 inconsistency를 고치도록 scope 확대

## Acceptance

- caller-visible meaning과 maintainer-only meaning이 같은 information type이어도 올바른 surface로 분기됨
- caller-facing explanation이 Python docstring에만 종속되지 않음
- explicit current task fact가 근거 없이 무시되지 않음
- user-provided fact와 canonical/current evidence가 충돌하면 source prose로 조용히 canonize하지 않음
- conflicting evidence behavior가 capability fixture로 보호됨
- 기존 comment recall, anti-spam, no-fabrication, mutation boundary가 유지됨
- package/file 수 증가 없음

## Status

Research complete. 이 findings는 기존 responsibility split을 변경하지 않고 current Skill의 surface-selection과 grounding precision을 좁게 개선합니다.

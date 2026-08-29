# Documentation

`clarify-code`는 code-adjacent prose를 다룬다. Caller-facing API documentation과 maintainer comment는 독자, 수명과 소비 방식이 다르다.

Core `SKILL.md`가 common-path signal, evidence gate와 reader/scope 기반 surface 선택을 소유한다. 이 reference는 ecosystem-specific surface, placement·ownership·grounding이 단순하지 않은 경우의 세부 판단만 보완한다.

## Two Readers

| Reader | Primary surface | Needs |
| --- | --- | --- |
| Caller | name, signature, type, language-native API documentation, call site | 무엇을 믿고 사용할 수 있는지 |
| Maintainer | code, names, local comment, tests | 어떤 constraint·consequence·rationale를 보존해야 하는지 |

코드와 이름이 스스로 설명할 수 있는 정보는 prose로 반복하지 않는다. 구조 자체가 불명확하면 prose를 추가하기보다 `code-comprehension-refactor`가 더 적합한지 먼저 판단한다.

## Explanation Value

설명이 있다는 사실 자체는 improvement가 아니다. Comment와 API documentation도 reader의 attention과 유지보수 비용을 소비한다.

설명을 추가하거나 유지하기 전에 다음 순서로 본다.

1. reader가 code만으로 안정적으로 복원하기 어려운 non-obvious meaning을 특정한다.
1. 설명이 없으면 어떤 추론, 탐색 또는 오해 가능성이 생기는지 확인한다.
1. code, name, type 또는 적절한 semantic owner가 이미 같은 정보를 충분히 전달하면 prose를 추가하지 않는다.
1. local caller/maintainer가 그 의미를 해당 지점에서 알아야 하는 projection이 필요한지 확인한다.
1. 설명이 제거하는 이해 비용이 읽기·유지·stale 위험보다 클 때만 남긴다.

실제 score를 계산하지 않는다. 설명을 추가하지 않는 것, redundant prose를 제거하는 것, stale prose를 현재 의미에 맞게 고치는 것도 정상적인 결과다.

## Grounding

Explanation은 **current evidence의 projection**이어야 한다. Unusual code shape나 plausible story를 rationale의 근거로 사용하지 않는다.

Candidate meaning을 확인할 때 상황에 따라 다음 evidence가 유용할 수 있다.

- target code의 observable behavior와 data/control relation
- caller와 call-site behavior
- regression/characterization test와 assertion
- canonical API/domain/specification contract
- current config, schema, protocol 또는 framework contract
- 같은 semantic owner의 현재 source documentation
- 현재 task에서 사용자가 명시적으로 제공한 domain·operational fact

User-provided current fact는 usable evidence candidate지만 unconditional semantic authority는 아니다. Observable behavior나 applicable canonical/current contract와 material하게 충돌하면 그대로 source prose로 canonize하지 않고 inconsistency 또는 uncertainty로 다룬다.

Git history, issue와 old discussion은 candidate rationale를 발견하는 supporting context일 수 있지만 current invariant의 단독 authority는 아니다. Historical reason을 explanation으로 남기려면 현재 code/contract에서도 여전히 유효한지 확인한다.

Evidence가 **설명하려는 claim에 대해** 충돌하면 한 source를 편의상 정답으로 선택하지 않는다. Exact claim과 가장 직접적으로 연결된 current semantic owner, observable behavior와 applicable contract를 기준으로 충돌을 좁게 재확인한다. 그 claim의 충돌이 여전히 material하면 disputed meaning은 permanent explanation으로 만들지 않는다. 다른 non-conflicting current meaning까지 함께 버리지는 않는다.

현재 behavior·constraint는 확인되지만 과거 decision reason은 확인되지 않는다면 **현재 확인 가능한 의미만** 설명한다. 예를 들어 same-request visibility contract는 확인되지만 과거 cache incident는 확인되지 않는다면 visibility constraint만 남긴다.

Material rationale를 확인할 수 없다면 그럴듯한 이유를 만들거나 uncertainty를 permanent comment로 굳히지 않는다. Evidence read도 적용되는 scope와 authority를 지키며, 더 넓게 읽었다고 그 surface를 수정할 권한이 생기는 것은 아니다.

## Caller-Facing API Documentation

Caller-facing documentation은 caller가 **사용 전에 알아야 하지만 name, signature, type만으로 드러나지 않는 contract**를 보완한다.

구체적인 syntax는 현재 language와 repository convention을 따른다. 예를 들면 Python의 docstring, Go의 declaration doc comment, Rust의 item documentation comment, Java의 Javadoc comment가 같은 responsibility를 수행할 수 있다. 이 예시는 portable syntax rule이 아니다.

좋은 대상:

- 결과나 input/output의 비자명한 domain semantics
- precondition, ordering 또는 approval requirement
- caller가 처리해야 하는 exception/failure 의미
- externally visible 또는 destructive side effect
- 반복 호출, idempotency, overwrite, caching 같은 호출 의미
- framework나 protocol이 요구하지만 signature로 드러나지 않는 caller-facing constraint

피한다:

- symbol 이름을 문장으로 다시 쓰기
- type information을 prose로 기계적으로 반복하기
- 내부 알고리즘 순서 설명하기
- caller가 의존하지 않는 미래 확장 설명하기
- code smell을 설명으로 정당화하기

```python
# Weak
def load_partition(path: Path) -> LoadResult:
    """Load a partition from the given path."""

# Useful
def load_partition(path: Path) -> LoadResult:
    """Load one partition, replacing an existing load for the same partition key."""
```

Python example은 information placement를 보여주는 예시일 뿐 다른 언어에 docstring syntax를 강제하지 않는다.

## Comments

Comment는 core의 maintainer-facing signal에 해당하는 **constraint, consequence와 rationale**를 가장 가까운 적절한 scope에서 전달한다. Code가 이미 구조적으로 적절하고 해당 meaning의 local projection이 필요하다면 가장 작은 comment를 추가하거나 기존 comment를 개선한다.

Caller가 사용 전에 알아야 하는 contract를 implementation body comment에만 숨기지 않는다. 반대로 caller가 의존하지 않는 implementation-only ordering이나 workaround rationale를 public API documentation으로 승격하지 않는다.

Rejected alternative는 durable negative knowledge가 될 수 있다. 과거에 다른 방법을 검토했다는 history 자체를 기록하지 않는다. 미래 maintainer가 자연스럽게 다시 시도할 가능성이 높고 **현재 constraint가 여전히 유효하다는 evidence가 있을 때**만 잘못된 대안과 연결되는 이유를 설명한다.

피한다:

- 다음 줄이 무엇을 하는지 설명
- identifier와 같은 내용을 반복
- 변경 이력·토론을 현재 규칙처럼 기록
- 더 명확한 code representation이나 structure로 해결해야 하는 혼란
- 임시 implementation detail을 영구 contract처럼 설명
- evidence 없이 plausible rationale를 만들어냄

```python
# Weak
# Validate the result.
validate(result)

# Useful
# Cleanup failure must not replace the original ingestion result or exception.
cleanup_staging()
```

## Placement and Scope

설명을 둘 때는 **owner correctness를 먼저**, locality를 그 다음에 판단한다.

1. 이 semantic의 적절한 owner가 어디인지 확인한다.
1. 더 넓은 owner가 이미 있다면 local caller/maintainer projection이 실제로 필요한지 판단한다.
1. Local projection이 필요하면 의미의 실제 scope에 가장 가까운 stable surface를 선택한다.

| Meaning | Preferred surface |
| --- | --- |
| 한 API의 caller contract | 해당 language/repository의 caller-facing API documentation surface |
| 한 branch, statement 또는 ordering의 maintainer-only rationale | 해당 code 근처 comment |
| file/package 전체에 안정적으로 적용되는 local convention | source-level module/package documentation surface |
| 여러 module에 걸친 architecture·domain policy | canonical owner; source에는 필요한 projection만 |

다음은 피한다.

- 특정 branch의 이유를 module 전체 rule처럼 넓게 설명하기
- 여러 local comment에 같은 context를 복제하기
- 가까이 둔다는 이유로 broad policy의 authority를 source comment로 옮기기
- 실제 invariant보다 넓은 scope로 읽히는 표현

Non-local하거나 긴 설명이라는 이유만으로 제거하지 않는다. 더 넓은 stable owner가 의미를 정확히 소유하거나 local repetition보다 탐색 비용을 줄인다면 그 surface가 더 적절할 수 있다.

## Module / Package-Level Explanation

Module, package 또는 이에 해당하는 source-level documentation은 local convention이 개별 symbol만으로 복원되지 않고 실제로 더 넓은 source scope에 적용될 때 사용할 수 있다.

- 해당 source scope가 소유하는 책임과 명확한 boundary를 짧게 설명한다.
- symbol별 API documentation을 모아 다시 쓰지 않는다.
- repository architecture guide나 domain policy를 local source documentation에 복제하지 않는다.
- 파일/package 구조가 잘못되어 역할이 불명확한 문제를 설명문으로 숨기지 않는다.

## Contract Projection

DRY는 중요한 caller contract를 외부 문서에만 숨기는 이유가 아니다.

- 넓은 architecture·domain policy는 canonical 문서가 소유한다.
- API 사용에 필요한 precondition, destructive side effect, overwrite/idempotency 의미는 API 가까이에 최소한으로 남긴다.
- canonical 용어를 사용하고 새 동의어나 병렬 정의를 만들지 않는다.

즉, 넓은 정책을 복제하지 말고 **호출이나 유지보수에 필요한 부분만 projection**한다.

## Machine-Consumed Text

source file 안의 모든 text가 단순 설명은 아니다.

일반 prose처럼 다루지 않는 예:

- `# noqa`, `# type: ignore`, coverage pragma, formatter/linter directive
- shebang, encoding cookie
- doctest example과 expected output
- reflection이나 framework가 읽는 docstring/documentation comment content
- code generation이나 documentation tooling이 parse하는 structured comment

이런 surface는 변경이 behavior, validation 또는 tooling contract에 영향을 줄 수 있다. 목적과 consumer를 확인하고 필요한 validation 없이 wording만 정리하지 않는다.

## Final Pass

설명을 추가하거나 수정한 뒤 확인한다.

- 이 explanation의 non-obvious semantic claim을 지지하는 current evidence는 무엇인가?
- user-provided fact를 포함해 **그 claim에 관련된** evidence source 사이의 material conflict가 해소됐는가?
- evidence-backed durable contract·constraint·consequence·rationale가 남아 있는데 explanation을 놓치지 않았는가?
- 이 설명이 없으면 reader는 무엇을 추론하거나 찾아야 하는가?
- 설명이 그 비용을 실제로 줄이고 code/name/type을 반복하지 않는가?
- caller-facing contract와 maintainer-only rationale를 서로 잘못된 surface에 두지 않았는가?
- code 자체를 refactor해야 하는 문제를 prose로 보상하고 있지 않은가?
- semantic owner, 실제 scope와 explanation의 위치·범위가 맞는가?
- current code, caller contract 또는 canonical policy와 모순되지 않는가?
- volatile identifier·algorithm step·history에 불필요하게 결합되어 쉽게 stale 되지 않는가?
- machine-consumed text나 durable negative knowledge를 잘못 다루고 있지 않은가?

필요한 evidence-backed meaning이 아직 숨겨져 있으면 적절한 explanation을 보완한다. 반대로 근거가 없거나 해당 claim의 conflict가 해소되지 않았거나 불필요하거나 쉽게 stale 되는 설명은 추가하지 않거나 줄인다.

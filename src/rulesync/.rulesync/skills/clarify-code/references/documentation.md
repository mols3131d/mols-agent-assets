# Documentation

`clarify-code`는 code-adjacent prose를 다룬다. Docstring과 comment는 같은 설명문이 아니며 독자, 수명과 소비 방식이 다르다.

## Two Readers

| Reader | Primary surface | Needs |
| --- | --- | --- |
| Caller | name, signature, type, docstring, call site | 무엇을 믿고 사용할 수 있는지 |
| Maintainer | code, names, local comment, tests | 어떤 constraint·consequence·rationale를 보존해야 하는지 |

코드와 이름이 스스로 설명할 수 있는 정보는 prose로 반복하지 않는다. 구조 자체가 불명확하면 prose를 추가하기보다 `code-comprehension-refactor`가 더 적합한지 먼저 판단한다.

## Explanation Value

설명이 있다는 사실 자체는 improvement가 아니다. Comment와 docstring도 reader의 attention과 유지보수 비용을 소비한다.

설명을 추가하거나 유지하기 전에 다음 순서로 본다.

1. reader가 code만으로 안정적으로 복원하기 어려운 non-obvious meaning을 특정한다.
1. 설명이 없으면 어떤 추론, 탐색 또는 오해 가능성이 생기는지 확인한다.
1. code, name, type 또는 가까운 contract가 이미 같은 정보를 충분히 전달하면 prose를 추가하지 않는다.
1. 설명이 제거하는 이해 비용이 읽기·유지·stale 위험보다 클 때만 남긴다.

실제 score를 계산하지 않는다. 설명을 추가하지 않는 것, redundant prose를 제거하는 것, stale prose를 현재 의미에 맞게 고치는 것도 정상적인 결과다.

다만 이 판단은 comment를 피하기 위한 억제 gate가 아니다. **실행 코드가 이미 적절하고, durable한 caller/maintainer 의미가 code만으로 안정적으로 드러나지 않으며, 같은 의미가 가까운 surface에 없다면 explanation을 추가하거나 개선하는 쪽이 기본이다.** 사용자가 comment나 docstring을 직접 요청하지 않았어도 target을 이해하는 과정에서 이런 의미를 발견하면 같은 기준을 적용한다.

## Positive Signals

다음 조건에서는 no-op보다 explanation을 우선한다. 단, executable code가 이미 적절하고 같은 의미가 다른 가까운 owner에 충분히 존재한다면 중복하지 않는다.

| Signal | Default surface |
| --- | --- |
| caller가 사용 전에 알아야 하는 hidden contract나 non-obvious call semantics | docstring |
| 현재 구현을 안전하게 바꾸려면 알아야 하는 invariant 또는 local constraint | code-local comment |
| statement/order를 바꾸면 결과·error semantics가 깨지는 ordering consequence | code-local comment |
| 외부 system/protocol 제약 때문에 의도적으로 특이한 구현을 유지해야 함 | code-local comment |
| 미래 maintainer가 자연스럽게 시도할 대안이 현재 constraint를 깨뜨림 | code-local comment |
| 개별 symbol보다 file 전체에 안정적으로 적용되는 local convention | module-level explanation |

Positive signal이 확인되면 설명의 존재 여부를 실제로 확인한다. 적절한 explanation이 없으면 가장 작은 설명을 추가하고, 이미 있다면 현재 code/contract와 일치하는지 개선 여부를 판단한다. 단순히 “code가 읽힌다”는 이유만으로 durable hidden meaning을 설명하지 않고 끝내지 않는다.

## Docstrings

Docstring은 caller가 **사용 전에 알아야 하지만 name, signature, type만으로 드러나지 않는 contract**를 보완한다.

좋은 대상:

- 결과나 input/output의 비자명한 domain semantics
- precondition, ordering 또는 approval requirement
- caller가 처리해야 하는 exception 의미
- externally visible 또는 destructive side effect
- 반복 호출, idempotency, overwrite, caching 같은 호출 의미
- framework나 protocol이 요구하지만 signature로 드러나지 않는 caller-facing constraint

피한다:

- 함수 이름을 문장으로 다시 쓰기
- type annotation을 Args/Returns prose로 반복하기
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

## Comments

Comment는 `Positive Signals`의 maintainer-facing 경우에 **constraint, consequence와 rationale**를 가장 가까운 적절한 scope에서 전달한다. Code가 이미 구조적으로 적절하고 해당 의미가 다른 가까운 explanation에 없다면 가장 작은 comment를 추가하거나 기존 comment를 개선한다.

Rejected alternative는 durable negative knowledge가 될 수 있다. 과거에 다른 방법을 검토했다는 history 자체를 기록하지 않는다. 미래 maintainer가 자연스럽게 다시 시도할 가능성이 높고 **현재 constraint가 여전히 유효할 때**만 잘못된 대안과 연결되는 이유를 설명한다.

피한다:

- 다음 줄이 무엇을 하는지 설명
- identifier와 같은 내용을 반복
- 변경 이력·토론을 현재 규칙처럼 기록
- 더 명확한 code representation이나 structure로 해결해야 하는 혼란
- 임시 implementation detail을 영구 contract처럼 설명

```python
# Weak
# Validate the result.
validate(result)

# Useful
# Cleanup failure must not replace the original ingestion result or exception.
cleanup_staging()
```

## Placement and Scope

설명은 가능한 한 의미의 실제 scope와 owner에 맞는 surface에 둔다. 가까움은 목적이 아니라 reader가 설명과 대상의 관계를 다시 탐색하지 않게 하는 수단이다.

| Meaning | Preferred surface |
| --- | --- |
| 한 API의 caller contract | 해당 docstring |
| 한 branch, statement 또는 ordering의 local rationale | 해당 code 근처 comment |
| file 전체에 안정적으로 적용되는 local convention | module-level explanation |
| 여러 module에 걸친 architecture·domain policy | canonical owner; source에는 필요한 projection만 |

다음은 피한다.

- 특정 branch의 이유를 module 전체 rule처럼 넓게 설명하기
- 여러 local comment에 같은 context를 복제하기
- 가까이 둔다는 이유로 broad policy의 authority를 source comment로 옮기기
- 실제 invariant보다 넓은 scope로 읽히는 표현

Non-local하거나 긴 설명이라는 이유만으로 제거하지 않는다. 더 넓은 stable owner가 의미를 정확히 소유하거나 local repetition보다 탐색 비용을 줄인다면 그 surface가 더 적절할 수 있다.

## Module-Level Explanation

Module docstring이나 가까운 code-level prose는 파일의 역할이나 local convention이 개별 symbol만으로 복원되지 않을 때 사용할 수 있다.

- module이 소유하는 책임과 명확한 boundary를 짧게 설명한다.
- symbol별 docstring을 모아 다시 쓰지 않는다.
- repository architecture guide나 domain policy를 module docstring에 복제하지 않는다.
- 파일 구조가 잘못되어 역할이 불명확한 문제를 설명문으로 숨기지 않는다.

## Contract Projection

DRY는 중요한 caller contract를 외부 문서에만 숨기는 이유가 아니다.

- 넓은 architecture·domain policy는 canonical 문서가 소유한다.
- API 사용에 필요한 precondition, destructive side effect, overwrite/idempotency 의미는 API 가까이에 최소한으로 남긴다.
- canonical 용어를 사용하고 새 동의어나 병렬 정의를 만들지 않는다.

즉, 넓은 정책을 복제하지 말고 **호출에 필요한 부분만 projection**한다.

## Machine-Consumed Text

source file 안의 모든 text가 단순 설명은 아니다.

일반 prose처럼 다루지 않는 예:

- `# noqa`, `# type: ignore`, coverage pragma, formatter/linter directive
- shebang, encoding cookie
- doctest example과 expected output
- reflection이나 framework가 읽는 docstring content
- code generation이나 documentation tooling이 parse하는 structured comment

이런 surface는 변경이 behavior, validation 또는 tooling contract에 영향을 줄 수 있다. 목적과 consumer를 확인하고 필요한 validation 없이 wording만 정리하지 않는다.

## Final Pass

설명을 추가하거나 수정한 뒤 확인한다.

- target 안에 durable한 hidden contract·constraint·consequence·rationale가 남아 있는데 explanation을 놓치지 않았는가?
- 이 설명이 없으면 reader는 무엇을 추론하거나 찾아야 하는가?
- 설명이 그 비용을 실제로 줄이고 code/name/type을 반복하지 않는가?
- code 자체를 refactor해야 하는 문제를 prose로 보상하고 있지 않은가?
- 의미의 실제 scope와 explanation의 위치·범위가 맞는가?
- current code, caller contract 또는 canonical policy와 모순되지 않는가?
- volatile identifier·algorithm step·history에 불필요하게 결합되어 쉽게 stale 되지 않는가?
- machine-consumed text나 durable negative knowledge를 잘못 다루고 있지 않은가?

필요한 durable meaning이 아직 숨겨져 있으면 적절한 explanation을 보완한다. 반대로 불필요하거나 쉽게 stale 되는 설명은 줄이거나 제거한다.

# Documentation

`clarify-code`는 code-adjacent prose를 다룬다. Docstring과 comment는 같은 설명문이 아니며 독자, 수명과 소비 방식이 다르다.

## Two Readers

| Reader | Primary surface | Needs |
| --- | --- | --- |
| Caller | name, signature, type, docstring, call site | 무엇을 믿고 사용할 수 있는지 |
| Maintainer | code, names, local comment, tests | 왜 이 구현·제약·순서가 필요한지 |

코드와 이름이 스스로 설명할 수 있는 정보는 prose로 반복하지 않는다. 구조 자체가 불명확하면 prose를 추가하기보다 `code-comprehension-refactor`가 더 적합한지 먼저 판단한다.

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

Comment는 maintainer가 code를 수정할 때 필요한 **code-local 이유**를 설명한다.

좋은 대상:

- policy 또는 invariant가 이 지점에서 적용되는 이유
- 비자명한 예외 처리 이유
- 순서가 중요한 이유
- 외부 시스템 제약
- 의도적으로 특이한 구현 선택의 이유
- 더 단순해 보이는 대안을 사용하지 못하는 local constraint

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

- 실제 caller 또는 maintainer가 이 정보를 필요로 하는가?
- code 자체를 refactor하면 prose가 필요 없어지는 문제인가?
- 이름이나 code를 그대로 번역하고 있지 않은가?
- 더 안정적인 owner에 있어야 할 넓은 정책을 복제했는가?
- code가 바뀌면 쉽게 거짓말이 될 설명인가?
- machine-consumed text를 일반 prose로 오해했는가?

불필요하거나 쉽게 stale 되는 설명은 줄이거나 제거한다.

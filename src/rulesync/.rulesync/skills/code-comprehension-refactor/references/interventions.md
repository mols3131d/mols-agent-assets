# Interventions

해법은 code smell 이름에 기계적으로 매핑하지 않는다. **현재 bottleneck을 실질적으로 줄이면서 behavior·contract·performance를 보존하는 가장 작은 coherent change**를 고른다.

## Intervention Map

| Cost source | Prefer | Avoid |
| --- | --- | --- |
| 모호한 identifier | domain meaning이 드러나는 internal name, specific API | 단순히 더 긴 이름, public rename을 clarity만으로 강행 |
| magic literal | 의미 있는 constant, enum, existing domain value | 모든 literal을 constant/class로 승격 |
| positional meaning | keyword/named argument, named field, existing explicit representation | comment로 tuple position을 계속 설명 |
| boolean/sentinel overload | named option, enum/value, 명확한 operation 구분 | boolean 하나마다 새 type 생성 |
| generic container | domain-shaped structure가 반복 reasoning을 줄일 때 사용 | boundary의 단순 임시 data까지 모두 class화 |
| dense expression | 의미 단위 grouping, named intermediate | trivial intermediate 남발, 줄바꿈만 하고 의미는 그대로 숨김 |
| compound/negative flow | guard clause, positive condition, named condition | exit를 늘려 전체 흐름을 더 분산 |
| state/order reasoning | state owner, phase, ordering을 code structure에 더 직접 반영 | 순서 contract를 comment에만 의존 |
| semantic-gain 없는 wrapper | inline, merge, delegation 제거 | stable boundary나 invariant-owning abstraction 제거 |
| abstraction mismatch | domain-shaped API, overly generic local layer 축소 | reuse 가능성만으로 새 generic framework 생성 |
| responsibility 혼합 | 실제로 독립된 책임 경계가 있을 때 regroup/extract | 함수 길이를 줄이기 위한 extraction |
| noise | dead/redundant surface 제거 | unrelated cleanup을 같은 change에 섞음 |

## Representation Before Explanation

표현 자체가 이해 비용의 원인이면 prose보다 representation을 먼저 개선한다.

```python
# Before: position과 boolean 의미를 다른 곳에서 복원해야 한다.
field = ("state", State, False, None)

# Direction: existing API가 지원한다면 role을 call site에서 드러낸다.
field = Field(name="state", type=State, required=False, default=None)
```

이 예시는 새 `Field` abstraction을 만들라는 규칙이 아니다. 이미 존재하는 explicit surface를 사용할 수 있거나 반복 reasoning이 충분히 줄어드는 경우의 방향이다.

## Name Intermediate Meaning, Not Syntax

긴 expression을 분리할 때 syntax 조각이 아니라 domain decision에 이름을 준다.

```python
# Weak: expression을 단순히 조각냄
part1 = request.user is not None
part2 = request.user.active

# Better direction when the concept is real
is_eligible_user = request.user is not None and request.user.active
```

중간 이름이 한 번 더 해석해야 하는 alias일 뿐이면 만들지 않는다.

## Reduce Indirection by Semantic Gain

다음 wrapper는 축소 후보일 수 있다.

```python
def load_user(user_id):
    return repository.load_user(user_id)
```

하지만 wrapper가 authorization, invariant, caching boundary, protocol adaptation 또는 stable domain concept을 소유한다면 단순 delegation처럼 보여도 가치가 있을 수 있다. 구현 한 줄만 보고 제거하지 않는다.

## Preserve Useful Abstraction

```python
if publication_policy.can_publish(change):
    publish(change)
```

`can_publish`가 안정적인 policy와 invariant를 소유한다면 내용을 call site에 펼치는 것이 더 explicit해 보여도 전체 comprehension cost는 커질 수 있다.

## Stop Rules

다음이면 더 진행하지 않는다.

- 현재 코드가 이미 task에 필요한 의미를 직접 드러낸다.
- 제안한 change가 새 concept, type, helper 또는 file을 추가하지만 줄어드는 reasoning이 불분명하다.
- 개선을 위해 public contract나 system architecture를 바꿔야 한다.
- performance-sensitive path인데 동등성 근거 없이 구조를 바꿔야 한다.
- 남은 문제는 code structure가 아니라 caller/maintainer 설명 부족이다. 이 경우 `clarify-code`로 넘긴다.

# Interventions

해법은 code smell 이름에 기계적으로 매핑하지 않는다. **현재 coherent bottleneck을 실질적으로 줄이면서 새 conceptual surface를 가장 적게 추가하는 change**를 고른다.

Core `SKILL.md`가 common-path 선택을 소유한다. 이 reference는 transformation choice, tightly coupled edit 또는 introduced-vs-removed reader work의 trade-off가 단순하지 않을 때 사용한다. Candidate transformation의 behavior-preserving precondition과 evidence는 [Validation](validation.md)이 소유한다.

## Choose by Reader Work

Transformation을 고를 때 세 가지를 확인한다.

1. 어떤 reader work를 제거하려는가.
2. 어떤 새 concept, terminology, navigation 또는 coupling을 추가하는가.
3. 같은 bottleneck을 더 작은 existing/local mechanism으로 줄일 수 있는가.

Candidate가 정해진 뒤 rename/move/extract/inline/representation/control-state change의 safety가 단순하지 않으면 mutation 전에 [Validation](validation.md)을 읽는다. Portable Skill에 language별 precondition catalog를 복제하지 않는다.

## Intervention Map

| Cost source | Prefer | Avoid |
| --- | --- | --- |
| lexical/domain decoding | repository-established domain term, specific internal name/API | 단순히 더 긴 이름, 새 local synonym |
| magic literal | 의미 있는 constant, enum, existing domain value | 모든 literal을 constant/class로 승격 |
| positional meaning | keyword/named argument, named field, existing explicit representation | comment로 tuple position을 계속 설명 |
| boolean/sentinel overload | named option, enum/value, 명확한 operation 구분 | boolean 하나마다 새 type 생성 |
| generic container | domain-shaped structure가 반복 reasoning을 줄일 때 사용 | boundary의 단순 임시 data까지 모두 class화 |
| dense/confusing expression | 의미 단위 grouping, domain-named intermediate, clearer equivalent syntax | trivial intermediate 남발, 줄바꿈만 하고 의미는 그대로 숨김 |
| compound/negative flow | guard clause, positive condition, named condition | exit를 늘려 전체 흐름을 더 분산 |
| state/order reasoning | state owner, phase, ordering을 code structure에 더 직접 반영 | 순서 contract를 comment에만 의존 |
| semantic-gain 없는 wrapper | inline, merge, delegation 제거 | stable boundary, compatibility 또는 invariant-owning abstraction 제거 |
| abstraction mismatch | domain-shaped API, overly generic local layer 축소 | reuse 가능성만으로 새 generic framework 생성 |
| responsibility 혼합 | 실제로 독립된 책임 경계가 있을 때 regroup/extract | 함수 길이를 줄이기 위한 extraction |
| noise | dead/redundant surface 제거 | unrelated cleanup을 같은 change에 섞음 |

## Rename by Meaning

Rename은 lexical decoding cost를 크게 줄일 수 있다.

다음 순서로 가치부터 본다.

1. 현재 이름이 실제로 domain/role decoding을 요구하는가.
2. repository에 이미 established term이 있는가.
3. 새 이름이 broader terminology consistency를 높이는가.
4. rename 하나로 material한 반복 translation이 줄어드는가.

`tmp`를 무조건 긴 이름으로 바꾸는 것이 목표가 아니다. Scope 안에서 role이 이미 명확한 이름은 그대로 둘 수 있다. Established domain term을 도입하면 여러 reader의 반복 translation을 줄이는 경우 rename이 작은 고가치 intervention일 수 있다.

이름이 framework/config/reflection/string/generated usage에 관찰될 수 있는지는 rename의 **safety question**이다. Material한 signal이 있으면 [Validation](validation.md)에서 usage surface를 확인한 뒤 적용한다.

## Representation Before Explanation

표현 자체가 이해 비용의 원인이면 prose보다 representation을 먼저 개선한다.

```python
# Before: position과 boolean 의미를 다른 곳에서 복원해야 한다.
field = ("state", State, False, None)

# Direction: existing API가 지원한다면 role을 call site에서 드러낸다.
field = Field(name="state", type=State, required=False, default=None)
```

이 예시는 새 `Field` abstraction을 만들라는 규칙이 아니다. 이미 존재하는 explicit surface를 사용할 수 있거나 반복 reasoning이 충분히 줄어드는 경우의 방향이다.

Representation이 persisted/wire/schema shape일 가능성이 material하면 [Validation](validation.md)에서 preservation surface를 확인한다.

## Name Intermediate Meaning, Not Syntax

긴 expression을 분리할 때 syntax 조각이 아니라 실제 domain decision에 이름을 준다.

```python
# Weak: expression을 단순히 조각냄
part1 = request.user is not None
part2 = request.user.active

# Better direction when the concept is real
is_eligible_user = request.user is not None and request.user.active
```

중간 이름이 한 번 더 해석해야 하는 alias일 뿐이면 만들지 않는다. Extraction이 evaluation order, short-circuiting 또는 exception/side-effect timing에 닿을 수 있으면 [Validation](validation.md)을 먼저 적용한다.

## Reduce Indirection by Semantic Gain

다음 wrapper는 축소 후보일 수 있다.

```python
def load_user(user_id):
    return repository.load_user(user_id)
```

하지만 wrapper가 authorization, invariant, caching, compatibility, protocol adaptation, registration identity 또는 stable domain concept을 소유한다면 단순 delegation처럼 보여도 가치가 있을 수 있다. 구현 한 줄만 보고 제거하지 않는다.

Inline/move/extract의 execution count, state capture, binding, identity 또는 ordering risk가 material하면 [Validation](validation.md)이 safety owner다.

## Preserve Useful Abstraction

```python
if publication_policy.can_publish(change):
    publish(change)
```

`can_publish`가 안정적인 policy와 invariant를 소유한다면 내용을 call site에 펼치는 것이 더 explicit해 보여도 전체 comprehension cost는 커질 수 있다.

Local navigation을 줄인다는 이유로 shared policy를 여러 caller에 복제하거나 repository terminology를 fragment하지 않는다.

## Coupled Edits

한 coherent bottleneck을 제거하려면 여러 edit가 동시에 필요할 수 있다.

허용되는 방향:

- positional representation을 named representation으로 바꾸며 그 새 role에 맞춰 local identifier도 rename
- mutable mode flag를 명확한 phase/state 표현으로 바꾸며 같은 state machine을 가리는 condition도 함께 정리
- meaningless wrapper chain을 축소하면서 같은 generic abstraction mismatch를 한 경계에서 정리

금지되는 방향:

- 같은 파일에 있다는 이유로 unrelated rename, dead-code removal, formatting, extraction을 함께 수행
- “이미 만지는 김에” future abstraction이나 architecture cleanup까지 확장

각 coupled edit가 primary bottleneck 제거에 필요한지 설명할 수 없으면 분리한다.

## Net Comprehension Gain

변경 후 다음을 대조한다.

### 줄어든 reader work

- lexical/domain decoding
- representation decoding
- hidden dependency search
- navigation
- control-flow simulation
- state/temporal tracking

### 새로 생긴 reader work

- 새 concept/type/helper/file을 학습함
- repository terminology와 다른 local vocabulary를 번역함
- duplicated policy/knowledge의 consistency를 추적함
- 더 많은 navigation 또는 ceremony가 필요함
- coupling이나 scope가 넓어짐

한 항목의 개선만으로 전체 improvement를 선언하지 않는다. 숫자 score는 만들지 않는다.

## Stop Rules

다음이면 더 진행하지 않는다.

- 현재 code가 이미 task에 필요한 의미를 직접 드러낸다.
- 제안한 change가 새 concept, type, helper 또는 file을 추가하지만 줄어드는 reasoning이 불분명하다.
- 한 coherent bottleneck을 해결한 뒤 남은 항목이 independent cleanup이다.
- 개선을 위해 published/usage contract 또는 system architecture 자체를 redesign해야 한다.
- performance-sensitive path에서 동등성 근거 없이 material work/allocation/I/O/complexity를 바꿔야 한다.
- [Validation](validation.md)에서 high-risk transformation의 preservation 근거가 충분하지 않다. 더 작은 intervention을 고르거나 중단한다.
- 남은 문제는 executable structure가 아니라 caller/maintainer explanation 부족이다. 이 concern은 `mols-clarify-code`가 소유한다.
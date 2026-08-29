# Clarify Code — Comprehension Cost Research

> [!IMPORTANT]
> 이 조사는 code comprehension cost를 탐색하기 위해 `clarify-code`를 확장 대상으로 놓고 시작했습니다. 조사 후 mutation authority를 분리하기로 결정했습니다. **실행 코드 자체의 이해 비용은 신규 `code-comprehension-refactor`, docstring·comment·module-level explanation 같은 code-adjacent prose는 `clarify-code`가 소유합니다.** 최종 구현 계획은 [Code Comprehension Skill Split Plan](clarify-code-comprehension-cost-plan.md)을 따릅니다.

## 결론

**이해 비용(comprehension cost)은 독자가 현재 작업에 필요한 mental model을 만들고 유지하기 위해 수행하는 번역·탐색·추론·시뮬레이션·맥락 복원의 비용**으로 보는 것이 적절합니다.

코드가 짧거나 syntax가 단순하다는 사실만으로 이해 비용이 낮다고 판단할 수 없습니다. 반대로 코드가 길거나 abstraction을 사용한다는 사실만으로 이해 비용이 높다고 판단해서도 안 됩니다. 중요한 것은 표현이 실제 domain meaning, control/data flow, state, contract와 rationale을 얼마나 직접 드러내는지입니다.

이해 비용은 다음 두 문제를 함께 봅니다.

- **Misunderstanding risk** — 잘못 이해하거나 잘못 사용할 가능성과 그 영향
- **Reconstruction effort** — 올바르게 이해하기 위해 필요한 불필요한 번역·탐색·추론·시뮬레이션

첫 번째는 destructive side effect, validation/approval gate, ordering, invariant처럼 실패 비용이 큰 경우를 우선하게 합니다. 두 번째는 compact contract object, positional tuple, boolean/sentinel 조합, generic wrapper처럼 **짧지만 해석 비용이 높은 코드**를 놓치지 않게 합니다.

## 조사에서 확인한 근거

### Program comprehension은 mental model을 만드는 활동이다

Program-comprehension 연구는 이해를 단순히 source text를 읽는 행위가 아니라 프로그램에 대한 내부 working representation, 즉 mental model을 형성하는 과정으로 다룹니다. 실제 개발에서는 comprehension이 debugging, maintenance, modification 같은 작업 안에 반복적으로 포함됩니다.

Source: [Wyrich et al., Source Code Comprehension: A Contemporary Definition and Conceptual Model for Empirical Investigation](https://arxiv.org/abs/2310.11301)

### Readability와 brevity는 같은 축이 아니다

Dantas et al.은 109개 Java repository의 merged PR에서 readability 개선이라고 설명된 370개 변경을 분석했고, **Clarify Code Intent**와 **Reduce Code Verbosity**를 서로 다른 범주로 다뤘습니다. Naming 개선, magic literal 제거, 더 specific한 API 선택은 line count 감소와 별개로 readability를 개선했습니다.

Source: [Dantas, Rocha, Maia, How do Developers Improve Code Readability? An Empirical Study of Pull Requests](https://arxiv.org/abs/2309.02594)

### 의미 있는 이름은 comprehension time을 줄일 수 있다

Hofmeister, Siegmund, Holt는 72명의 professional C# developer를 대상으로 identifier naming style을 비교했습니다. 단일 문자나 abbreviation보다 실제 단어를 사용한 identifier에서 defect를 찾는 속도가 19% 빨랐습니다.

핵심은 이름의 길이가 아니라 reader가 약어와 domain meaning을 추가로 해독하는 작업을 줄이는 것입니다.

Source: [Hofmeister, Siegmund, Holt, Shorter identifier names take longer to comprehend](https://link.springer.com/article/10.1007/s10664-018-9621-x)

### 작은 syntax도 큰 이해 비용을 만들 수 있다

Atoms of Confusion 연구는 기능적으로 동등한 작은 code pattern도 programmer의 오해를 증가시킬 수 있음을 보여줍니다. Java replication에서는 조사한 14개 pattern 중 7개에서 confusing pattern이 포함된 코드의 실수 가능성이 유의미하게 높았습니다.

즉, 문제의 code size와 comprehension cost는 비례하지 않습니다.

Sources:

- [Gopstein et al., Understanding Misunderstandings in Source Code](https://doi.org/10.1145/3106237.3106264)
- [Langhout, Aniche, Atoms of Confusion in Java](https://arxiv.org/abs/2103.05424)

### Representation은 여러 인지 trade-off를 가진다

Green과 Blackwell의 Cognitive Dimensions는 information representation을 closeness of mapping, role-expressiveness, hidden dependencies, hard mental operations, consistency, diffuseness, abstraction 같은 여러 축으로 봅니다.

| Dimension | 코드 이해 비용에 주는 질문 |
| --- | --- |
| Closeness of mapping | 표현이 실제 domain concept와 얼마나 직접 대응하는가? |
| Role-expressiveness | component의 역할을 그 자리에서 알 수 있는가? |
| Hidden dependencies | 중요한 관계를 다른 위치나 convention에서 찾아야 하는가? |
| Hard mental operations | reader가 머릿속에서 변환·추적·계산해야 하는가? |
| Consistency | 같은 의미가 비슷한 방식으로 표현되는가? |
| Diffuseness | 의미를 표현하는 데 불필요하게 많은 notation이 필요한가? |
| Abstraction | abstraction이 reasoning을 줄이는가, 필요한 관계를 가리는가? |

어느 한 dimension을 항상 최소화할 수는 없습니다. abstraction은 detail을 숨겨 reasoning을 줄일 수 있지만 hidden dependency를 늘릴 수도 있고, 모든 것을 펼치면 visibility는 좋아져도 diffuseness와 maintenance cost가 커질 수 있습니다.

Source: [Green, Blackwell, Cognitive Dimensions of Information Artefacts: a tutorial](https://www.cl.cam.ac.uk/~afb21/CognitiveDimensions/CDtutorial.pdf)

### Navigation 자체도 comprehension cost다

Ko et al.은 unfamiliar code를 이해할 때 개발자가 관련 정보를 seek, relate, collect하며 task context를 구성한다는 점을 보여줍니다. helper나 abstraction으로 이동하는 행위는 무료가 아닙니다.

하지만 hop count 자체가 나쁜 것도 아닙니다. 한 번의 navigation이 stable domain concept, invariant나 복잡한 implementation detail을 대신한다면 충분한 semantic gain이 있습니다.

Source: [Ko et al., An Exploratory Study of How Developers Seek, Relate, and Collect Relevant Information during Software Maintenance Tasks](https://doi.org/10.1109/TSE.2006.116)

### 실무 guidance도 빠른 이해 가능성을 complexity 기준으로 본다

Google Engineering Practices는 complexity를 특정 metric으로 정의하기보다 code reader가 빠르게 이해하기 어렵거나 caller/modifier가 bug를 만들기 쉬운지를 중요하게 봅니다. Reviewer가 코드를 이해하기 어렵다면 설명으로만 해결하지 말고 code 자체를 더 clear하게 만드는 방향을 권합니다.

Sources:

- [Google Engineering Practices — What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Google Engineering Practices — How to handle reviewer comments](https://google.github.io/eng-practices/review/developer/handling-comments.html)

## 이해 비용이 큰 코드의 유형

이 taxonomy는 score나 code smell catalog가 아니라 **reader가 수행하는 추가 mental work를 찾는 lens**입니다.

| Cost source | 주요 신호 | Reader가 수행하는 추가 작업 | 대표적인 intervention |
| --- | --- | --- | --- |
| Lexical / semantic decoding | generic 이름, 약어, magic literal | domain meaning을 추측하거나 검색 | domain name, named constant, specific API |
| Representation decoding | positional tuple, boolean/sentinel, generic container, compact DSL | 위치·flag·shape 규칙을 복원 | named field/argument, domain-shaped representation |
| Hidden dependency | global/context state, implicit registration, external convention | 현재 코드 밖의 관계를 찾아 연결 | 필요한 dependency/contract를 가까이 노출 |
| Navigation / indirection | semantic gain 없는 wrapper/helper chain | 여러 symbol/file을 이동 | inline/merge, needless indirection 제거 |
| Control-flow simulation | nesting, negative logic, compound condition | 가능한 경로를 mental simulation | guard clause, condition naming, local simplification |
| State / temporal reasoning | mutation, ordering, mode/phase | 이전·현재·다음 state를 기억 | state ownership, phase/order를 직접 표현 |
| Abstraction mismatch | 너무 generic하거나 domain과 먼 abstraction | generic model을 domain model로 번역 | domain-shaped API, overly generic layer 축소 |
| Responsibility reconstruction | 서로 다른 책임·abstraction level 혼재 | 부분을 분류하고 관계를 재구성 | 자연스러운 책임 경계에서만 regroup/extract |
| Delocalized rationale | 이유가 code에서 복원되지 않음 | history·issue·다른 file에서 왜를 찾음 | `clarify-code`의 docstring/comment 또는 가까운 contract surface |
| Noise | dead/redundant/stale surface | 현재 behavior와 무관한 정보를 필터링 | 실제로 불필요한 surface 제거 |

## 이해 비용을 줄이는 원칙

### 의미를 code에 더 직접적으로 투영한다

가능하면 reader가 다른 문서나 convention을 해독하지 않고 code surface에서 domain meaning과 role을 알 수 있게 합니다. Naming, specific API, named representation과 domain-shaped abstraction이 대표적입니다.

### Representation 문제를 comment로 덮지 않는다

Positional tuple이나 overloaded boolean의 규칙을 comment로 설명하면 diff는 작지만 모든 reader가 계속 representation을 해독해야 합니다. Behavior와 contract를 안전하게 보존할 수 있다면 representation 자체를 개선하는 것이 더 직접적입니다.

이 실행 코드 변경은 `code-comprehension-refactor`가 소유합니다.

### 좋은 abstraction은 reasoning을 줄인다

Abstraction이 stable domain concept, invariant, policy, repeated reasoning 또는 volatile detail encapsulation을 제공한다면 navigation cost를 지불할 가치가 있습니다.

따라서 목표는 de-abstraction이 아니라 **semantic gain 대비 navigation·decoding cost를 판단하는 것**입니다.

### Prose는 code로 표현하기 어려운 의미를 보완한다

Code 자체가 적절하지만 caller contract나 maintainer rationale이 숨어 있다면 docstring/comment가 가장 작은 intervention일 수 있습니다.

이 code-adjacent prose 변경은 `clarify-code`가 소유합니다.

### 최소 변경은 최소 diff가 아니다

가장 작은 intervention은 수정 line 수가 가장 적은 변경이 아닙니다.

> 현재 병목을 실질적으로 제거하면서 behavior와 contract를 보존하고, 새 conceptual surface를 가장 적게 추가하는 변경을 선택한다.

## Skill Design Implication

조사 결과는 하나의 broad skill에 모든 intervention을 넣기보다 mutation authority가 다른 두 skill로 분리하는 쪽을 지지합니다.

- `code-comprehension-refactor`: executable code를 behavior-preserving하게 리팩터링
- `clarify-code`: executable code를 유지하고 code-adjacent prose를 개선

두 skill의 공통 목적은 comprehension cost 감소지만 실제 mutation surface와 validation contract는 겹치지 않게 둡니다.

# Clarify Code — Comprehension Cost Research

`clarify-code`가 다뤄야 할 핵심 문제를 **코드가 길거나 복잡해 보이는가**가 아니라, 독자가 코드를 이해하기 위해 얼마나 많은 의미 복원 작업을 해야 하는가로 재정의하기 위한 조사 기록입니다.

## 결론

**이해 비용(comprehension cost)은 독자가 현재 작업에 필요한 mental model을 만들고 유지하기 위해 수행하는 번역·탐색·추론·시뮬레이션·맥락 복원의 비용**으로 보는 것이 적절합니다.

코드가 짧거나 syntax가 단순하다는 사실만으로 이해 비용이 낮다고 판단할 수 없습니다. 반대로 코드가 길거나 abstraction을 사용한다는 사실만으로 이해 비용이 높다고 판단해서도 안 됩니다. 중요한 것은 표현이 실제 domain meaning, control/data flow, state, contract와 rationale을 얼마나 직접 드러내는지입니다.

이 관점에서 `clarify-code`는 다음 두 문제를 모두 다뤄야 합니다.

- **Misunderstanding risk** — 잘못 이해하거나 잘못 사용할 가능성과 그 영향이 큼
- **Reconstruction effort** — 결국 이해할 수는 있지만 의미를 복원하기 위해 불필요한 정신적 작업이 많이 필요함

첫 번째는 destructive side effect, validation/approval gate, ordering, invariant처럼 실패 비용이 큰 경우를 우선하게 합니다. 두 번째는 compact contract object, positional tuple, boolean/sentinel 조합, generic wrapper처럼 **짧지만 해석 비용이 높은 코드**를 놓치지 않게 합니다.

두 축은 경쟁 관계가 아닙니다. 위험한 오해를 우선하되, 반복적으로 읽히거나 수정되는 코드에서는 낮은 수준의 reconstruction effort도 누적 비용이 될 수 있습니다.

## 조사에서 확인한 근거

### Program comprehension은 mental model을 만드는 활동이다

최근 program-comprehension 연구 정리는 이해를 단순히 source text를 읽는 행위가 아니라 **프로그램에 대한 내부 working representation, 즉 mental model을 형성하는 과정**으로 다룹니다. 또한 실제 개발에서는 comprehension이 독립적인 최종 작업이라기보다 debugging, maintenance, modification 같은 작업 안에 반복적으로 포함됩니다.

이 정리는 선행 현장 연구를 인용해 개발자가 task context에 따라 반복적인 comprehension strategy를 사용하고, hypothesis를 만들고 검증하며, source code·naming convention·architecture cue를 이용해 mental model을 형성한다고 설명합니다. IDE interaction 연구에서는 development activity의 큰 비중이 understanding에 사용되며, 다른 현장 연구에서도 program comprehension이 개발 시간의 상당 부분을 차지했습니다.

이 때문에 `clarify-code`의 목표를 “읽기 좋은 모양”보다 **필요한 mental model을 더 적은 추론으로 형성하게 하는 것**으로 두는 편이 강합니다.

Source: [Wyrich et al., Source Code Comprehension: A Contemporary Definition and Conceptual Model for Empirical Investigation](https://arxiv.org/abs/2310.11301)

### Readability와 brevity는 같은 축이 아니다

Dantas et al.은 109개 Java repository의 merged PR에서 개발자와 reviewer가 명시적으로 readability 개선이라고 설명한 370개 변경을 분석했습니다. 연구는 26종의 개선을 7개 범주로 분류했고, **Clarify Code Intent**와 **Reduce Code Verbosity**를 서로 다른 범주로 다뤘습니다.

특히 intent clarification에는 다음과 같은 변경이 포함됐습니다.

- identifier naming 개선
- magic literal을 의미 있는 constant로 교체
- modifier·annotation으로 scope/constraint 노출
- generic API를 더 specific한 API로 교체

즉, readability 개선은 token이나 line count를 줄이는 일과 별개로 **코드가 의미를 더 직접적으로 표현하게 만드는 일**입니다. 같은 연구에서 SonarQube가 개발자가 실제 수행한 readability 개선 370건 중 26건만 같은 문제로 포착했다는 점도 단순 static metric만으로는 인간이 느끼는 이해 비용을 충분히 모델링하기 어렵다는 근거가 됩니다.

Source: [Dantas, Rocha, Maia, How do Developers Improve Code Readability? An Empirical Study of Pull Requests](https://arxiv.org/abs/2309.02594)

### 의미 있는 이름은 실제 comprehension time을 줄일 수 있다

Hofmeister, Siegmund, Holt는 72명의 professional C# developer를 대상으로 identifier naming style을 비교했습니다. 단일 문자나 abbreviation보다 **실제 단어를 사용한 identifier에서 defect를 찾는 속도가 19% 빨랐습니다.**

이 결과는 단순히 “긴 이름이 좋다”는 규칙을 만들 근거는 아닙니다. 핵심은 reader가 identifier를 보고 domain meaning을 추론하거나 약어를 해독하는 작업을 줄였을 때 comprehension이 빨라질 수 있다는 점입니다.

따라서 `clarify-code`는 identifier 길이가 아니라 **이름이 독자에게 필요한 의미를 직접 전달하는가**를 봐야 합니다.

Source: [Hofmeister, Siegmund, Holt, Shorter identifier names take longer to comprehend](https://link.springer.com/article/10.1007/s10664-018-9621-x)

### 작은 syntax도 불필요한 mental operation을 만들 수 있다

Atoms of Confusion 연구는 기능적으로 동등한 두 표현 가운데 특정 작은 code pattern이 programmer의 오해를 증가시킬 수 있음을 반복적으로 조사했습니다. Java replication에서는 132명의 참가자를 대상으로 14개 pattern을 조사했고, 그중 7개에서는 confusing pattern이 포함된 코드에서 실수할 가능성이 유의미하게 높았습니다.

중요한 시사점은 **문제의 크기와 이해 비용의 크기가 비례하지 않는다는 것**입니다. 몇 token짜리 표현도 reader에게 hidden convention이나 language trick을 해독하게 만들면 높은 comprehension cost를 만들 수 있습니다.

`clarify-code`는 따라서 long method나 nesting 같은 큰 구조뿐 아니라 작은 but opaque representation도 후보로 볼 필요가 있습니다.

Sources:

- [Gopstein et al., Understanding Misunderstandings in Source Code](https://doi.org/10.1145/3106237.3106264)
- [Langhout, Aniche, Atoms of Confusion in Java](https://arxiv.org/abs/2103.05424)

### 표현의 usability에는 verbosity 이외의 여러 축이 있다

Green과 Blackwell의 Cognitive Dimensions of Information Artefacts는 programming notation을 포함한 information representation을 여러 독립적인 인지 축으로 봅니다. 이번 문제에 특히 직접적인 축은 다음과 같습니다.

| Dimension | `clarify-code`에 주는 질문 |
| --- | --- |
| Closeness of mapping | 표현이 실제 domain concept와 얼마나 직접 대응하는가? |
| Role-expressiveness | component의 목적을 그 자리에서 추론할 수 있는가? |
| Hidden dependencies | 중요한 관계를 다른 위치나 convention을 알아야만 발견하는가? |
| Hard mental operations | 독자가 머릿속에서 변환·추적·계산해야 하는 작업이 과한가? |
| Consistency | 비슷한 의미가 비슷한 방식으로 표현되어 학습한 규칙을 재사용할 수 있는가? |
| Diffuseness | 의미를 표현하는 데 불필요하게 많은 notation이 필요한가? |
| Abstraction | abstraction이 정보를 유용하게 묶는가, 아니면 필요한 관계를 가리는가? |

여기서 중요한 것은 **어느 한 dimension을 항상 최소화할 수 없다는 것**입니다. 예를 들어 abstraction은 반복되는 detail을 숨겨 이해를 돕지만 hidden dependency를 늘릴 수도 있습니다. 반대로 모든 것을 explicit하게 펼치면 closeness나 visibility는 좋아질 수 있어도 diffuseness와 maintenance cost가 커질 수 있습니다.

따라서 `clarify-code`는 “explicit > abstract” 같은 절대 규칙이 아니라 **현재 독자에게 필요한 의미를 더 직접적으로 복원하게 하는가**를 판단해야 합니다.

Source: [Green, Blackwell, Cognitive Dimensions of Information Artefacts: a tutorial](https://www.cl.cam.ac.uk/~afb21/CognitiveDimensions/CDtutorial.pdf)

### Navigation 자체도 comprehension cost다

Ko et al.의 software maintenance 관찰 연구는 unfamiliar code를 이해할 때 개발자가 관련 정보를 **seek, relate, collect**하며 task context를 구성한다는 점을 보여줍니다. 즉, helper나 abstraction으로 이동하는 행위는 무료가 아닙니다.

하지만 hop count만으로 판단해서도 안 됩니다. 한 번의 navigation이 안정적인 domain abstraction, invariant 또는 복잡한 implementation detail을 대신해 준다면 비용을 지불할 가치가 있습니다. 반대로 wrapper를 열어도 새 의미가 없고 다시 다른 helper로 이동해야 한다면 navigation cost만 증가합니다.

Source: [Ko et al., An Exploratory Study of How Developers Seek, Relate, and Collect Relevant Information during Software Maintenance Tasks](https://doi.org/10.1109/TSE.2006.116)

### 실무 guidance도 “빠르게 이해 가능한가”를 complexity 기준으로 본다

Google Engineering Practices는 complexity를 특정 metric으로 정의하지 않고, **code reader가 빠르게 이해하기 어렵거나 caller/modifier가 bug를 만들기 쉬운 상태**를 핵심 신호로 설명합니다. 또한 reviewer가 코드를 이해하기 어렵다면 review discussion에서 설명하는 것으로 끝내기보다 먼저 code 자체를 더 clear하게 만들 것을 권합니다.

이는 `clarify-code`의 behavior-preserving clarification과 잘 맞습니다. 중요한 것은 style purity가 아니라 미래 reader가 같은 해석 비용을 반복해서 지불하지 않도록 source에 개선을 남기는 것입니다.

Sources:

- [Google Engineering Practices — What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Google Engineering Practices — How to handle reviewer comments](https://google.github.io/eng-practices/review/developer/handling-comments.html)

## 이해 비용이 큰 코드의 유형

아래 taxonomy는 metric이나 code smell catalog가 아닙니다. `clarify-code`가 **reading bottleneck의 원인을 진단하기 위한 lens**입니다. 한 코드가 여러 유형에 걸릴 수 있고, 유형 수가 많다고 더 나쁜 코드라는 뜻도 아닙니다.

| Cost source | 주요 신호 | 독자가 수행하는 추가 작업 | 대표적인 최소 intervention |
| --- | --- | --- | --- |
| Lexical / semantic decoding | 짧거나 generic한 이름, 약어, magic literal | 이름·값의 실제 domain meaning을 추측하거나 검색 | domain name, named constant, 더 specific한 API/name |
| Representation decoding | positional tuple, boolean/sentinel 조합, generic dict/object, compact DSL | 위치·flag·sentinel·shape의 숨은 규칙을 기억하고 펼침 | named field/argument, enum/value object, explicit local representation |
| Hidden dependency | global/context state, implicit registration, callback 관계, external convention | 현재 코드 밖의 관계를 찾아 연결 | dependency/contract를 가까운 surface에 노출, 필요 없는 hidden coupling 제거 |
| Navigation / indirection | 의미 없는 wrapper/helper/delegation chain | 여러 파일·함수를 이동하지만 새 semantic compression을 얻지 못함 | inline/merge, indirection 제거, caller-facing naming 개선 |
| Control-flow simulation | 깊은 nesting, negative logic, compound condition, non-local exit | 가능한 실행 경로를 머릿속에서 추적 | guard clause, positive condition, condition naming, local flow simplification |
| State / temporal reasoning | mutation, ordering dependency, mode flag, phase-specific invariant | “지금 상태”와 이전/다음 operation의 영향을 기억 | state ownership 명시, phase/operation 분리, order-sensitive rationale 보존 |
| Abstraction mismatch | 너무 generic하거나 domain과 거리가 먼 abstraction | 추상 표현을 실제 문제 개념으로 계속 번역 | domain-shaped API/representation, overly generic layer 축소 |
| Responsibility reconstruction | 한 unit에 다른 이유로 변하는 작업·abstraction level 혼재 | 부분들을 분류하고 관계를 다시 구성 | 자연스러운 책임 경계가 있을 때만 extract/regroup |
| Delocalized rationale / invariant | 순서·예외·정책의 이유가 code에서 복원되지 않음 | history·issue·다른 file을 찾아 “왜”를 재구성 | code-local intent comment, caller contract는 docstring |
| Noise | dead branch, unused parameter, redundant boilerplate, stale explanation | 현재 behavior와 무관한 정보를 계속 필터링 | unused/redundant code 제거, stale prose 제거 |
| Visual parsing friction | 과도한 one-liner, 긴 expression, 관계가 안 보이는 grouping | syntax boundary와 의미 단위를 먼저 분해 | line/grouping 조정, named intermediate; formatter 취향만으로 변경하지 않음 |

### 특히 이번 failure와 직접 관련된 `Representation decoding`

다음 코드는 line count와 control-flow complexity는 낮지만 각 tuple position과 literal의 의미를 독자가 외부 contract에서 복원해야 한다면 이해 비용이 높습니다.

```python
contract = Contract(
    ("id", str, True),
    ("state", State, False),
    ("ttl", int, None),
)
```

문제는 tuple 자체나 compact representation 자체가 아닙니다. 다음 질문에 답하기 위해 implementation이나 별도 schema를 열어야 한다면 reading bottleneck이 됩니다.

- 세 번째 값은 required 여부인가, nullable 여부인가, default인가?
- `None`은 “값 없음”, “default 없음”, “optional” 가운데 무엇인가?
- tuple order가 바뀌어도 type checker나 constructor가 실수를 막는가?
- caller와 maintainer가 이 shape를 반복해서 해독하는가?

반대로 다음처럼 domain에서 이미 널리 이해되는 compact notation이거나, 주변 코드에서 안정적이고 일관된 convention으로 작동하며 별도 해독이 거의 필요 없다면 무조건 풀어쓰지 않습니다.

## 이해 비용을 줄이는 intervention 원칙

### 1. 의미를 code surface에 더 가깝게 둔다

가장 싼 개선은 reader가 다른 위치로 이동하지 않고 현재 surface에서 의도를 복원하게 하는 것입니다.

우선순위 후보:

1. 더 정확한 internal name
1. magic literal을 domain name이 있는 constant/enum으로 교체
1. generic API 대신 intent가 드러나는 specific API 사용
1. positional/boolean/sentinel 의미를 named field·argument로 projection
1. 필요한 modifier/type/annotation으로 contract를 코드에 노출

이 원칙은 “더 verbose하게 작성한다”가 아닙니다. 필요한 의미를 직접 표현하여 **해독 단계 자체를 줄이는 것**입니다.

### 2. 한 표현에 너무 많은 mental transformation이 필요하면 분해한다

한 line이나 expression이 짧아도 reader가 여러 operation, condition 또는 encoded meaning을 동시에 펼쳐야 한다면 named intermediate나 local decomposition이 도움이 될 수 있습니다.

다만 intermediate variable이나 helper는 각각 새로운 navigation/name surface를 만듭니다. 따라서 **분해된 단위가 독립적인 의미를 제공할 때만** 추가합니다.

### 3. 숨기는 abstraction은 비용을 정당화해야 한다

abstraction을 유지할 강한 이유:

- 안정적인 domain concept에 이름을 부여함
- invariant나 validation을 한 곳에서 보존함
- 반복되는 reasoning을 제거함
- volatile implementation detail을 caller로부터 격리함
- 여러 call site가 같은 semantic contract를 공유함

축소할 신호:

- 한 번만 쓰는 generic wrapper인데 새 의미가 없음
- 호출부를 이해하려면 abstraction implementation부터 열어야 함
- positional/flag convention을 단지 compact하게 감춤
- domain operation이 generic execute/apply/process 같은 layer에 가려짐
- hop을 추가하지만 invariant, reuse, ownership 또는 encapsulation benefit이 없음

따라서 판단 질문은 다음이 적절합니다.

> 이 abstraction이 줄이는 반복 reasoning과 보존하는 의미·제약이, 추가하는 navigation·decoding cost보다 큰가?

### 4. control/state는 reader가 동시에 기억해야 하는 것을 줄인다

control flow clarification은 line count를 줄이는 작업이 아니라 **동시에 추적해야 하는 branch와 상태를 줄이는 작업**입니다.

대표 intervention:

- negative condition을 domain-positive condition으로 표현
- guard clause로 exceptional path를 먼저 종료
- 여러 의미가 섞인 compound condition에 이름 부여
- mutation owner와 ordering을 가까이 둠
- mode flag가 사실상 다른 operation을 의미하면 caller intent를 분리할지 검토

### 5. prose는 code로 표현할 수 없는 의미를 보존할 때 쓴다

comment/docstring은 confusing code를 정당화하는 patch가 아닙니다.

- caller가 알아야 하는 precondition, side effect, overwrite/idempotency semantics → docstring
- maintainer가 알아야 하는 외부 제약, 비자명한 ordering, invariant의 이유 → intent comment
- 더 나은 naming/representation/control flow로 제거 가능한 설명 → code를 먼저 개선

현재 `clarify-code/references/documentation.md`의 방향과 일치하며, 이번 개선에서 별도 documentation 철학을 만들 필요는 없습니다.

## `clarify-code`에 적용할 판단 모델

정량 score를 만들지 않습니다. metric이 human readability를 충분히 대표하지 못한다는 근거가 있고, context에 따라 abstraction과 verbosity의 trade-off가 달라지기 때문입니다.

대신 bottleneck을 찾을 때 다음 순서의 질문을 사용합니다.

### Meaning reconstruction

- 이 이름·값·shape를 보고 domain meaning을 바로 알 수 있는가?
- positional value, boolean, sentinel, encoded string의 의미를 외워야 하는가?
- generic representation을 실제 domain operation으로 번역해야 하는가?

### Navigation and context

- 현재 코드를 이해하려고 몇 개의 definition/helper/config를 열어야 하는가?
- 이동한 곳에서 새로운 의미를 얻는가, 아니면 wrapper만 더 만나는가?
- 중요한 dependency나 contract가 reader-visible surface 밖에 숨어 있는가?

### Simulation

- 여러 branch/state/order를 동시에 기억해야 하는가?
- condition을 이해하려면 부정의 부정이나 여러 boolean 조합을 mental simulation해야 하는가?
- 호출 전후 state나 side effect를 추측해야 하는가?

### Value of abstraction

- abstraction이 stable concept, invariant, reuse 또는 encapsulation을 제공하는가?
- 제거하면 domain meaning이 더 분명해지는가, 아니면 implementation detail만 노출되는가?

### Reader impact

- 잘못 이해하면 destructive side effect, gate bypass, ordering/invariant 위반이 생기는가?
- 자주 읽거나 수정되는 surface인가?
- 현재 병목을 제거하면 실제 caller/maintainer가 덜 탐색하고 덜 추론하게 되는가?

우선순위는 고정 formula가 아니라 다음 원칙으로 충분합니다.

> **오해의 영향이 큰 병목을 먼저 보호하고, 그다음 반복적으로 발생하는 불필요한 reconstruction effort를 줄인다. 시각적 취향이나 line count는 독립적인 목표가 아니다.**

## Anti-pattern: clarity를 verbosity로 오해하지 않는다

이번 개선의 가장 큰 regression 위험은 `clarify-code`가 모든 compact code를 풀어쓰는 방향으로 변하는 것입니다.

다음은 변경 근거가 아닙니다.

- line 수가 적다
- lambda/DSL을 사용한다
- abstraction이 있다
- tuple/dict를 사용한다
- one-liner다
- comment가 없다

실제 질문은 **독자가 이 표현 때문에 불필요한 의미 복원 작업을 하는가**입니다.

마찬가지로 다음도 자동 개선이 아닙니다.

- helper를 더 만든다
- class/value object를 새로 만든다
- 모든 boolean을 enum으로 바꾼다
- 모든 expression을 intermediate variable로 나눈다
- 모든 hidden meaning을 comment로 설명한다

Intervention은 현재 병목을 제거하는 **smallest coherent change**여야 하며, 여기서 smallest는 line count가 아니라 새로 도입하는 conceptual surface까지 포함합니다.

## 설계에 반영할 핵심 delta

현재 `clarify-code`의 큰 방향은 유지할 수 있습니다. 필요한 delta는 다음 정도입니다.

1. 상위 목표를 `misunderstanding cost`만이 아니라 **comprehension cost**로 넓힙니다.
1. `diagnosis.md`에 **Representation**을 독립 bottleneck으로 추가합니다.
1. `Navigation` 판단을 hop count가 아니라 **semantic gain 대비 navigation cost**로 보정합니다.
1. abstraction 축소에는 **abstraction value test**를 같이 둬 과잉 de-abstraction을 막습니다.
1. `smallest intervention`은 최소 line diff가 아니라 **병목을 실질적으로 제거하는 최소 conceptual change**라는 점을 명확히 합니다.
1. 실제로 관찰된 이번 failure를 capability eval fixture로 남깁니다.

새 metric, analyzer, 별도 comprehension framework나 large reference package는 만들지 않는 것이 좋습니다. 현재 문제는 semantic judgment에 가깝고 `diagnosis.md`가 이미 그 판단 owner입니다.

## Sources

- [Google Engineering Practices — What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Google Engineering Practices — How to handle reviewer comments](https://google.github.io/eng-practices/review/developer/handling-comments.html)
- [Dantas, Rocha, Maia — How do Developers Improve Code Readability?](https://arxiv.org/abs/2309.02594)
- [Hofmeister, Siegmund, Holt — Shorter identifier names take longer to comprehend](https://link.springer.com/article/10.1007/s10664-018-9621-x)
- [Buse, Weimer — Learning a Metric for Code Readability](https://doi.org/10.1109/TSE.2009.70)
- [Scalabrino et al. — A comprehensive model for code readability](https://doi.org/10.1002/smr.1958)
- [Gopstein et al. — Understanding Misunderstandings in Source Code](https://doi.org/10.1145/3106237.3106264)
- [Langhout, Aniche — Atoms of Confusion in Java](https://arxiv.org/abs/2103.05424)
- [Green, Blackwell — Cognitive Dimensions of Information Artefacts](https://www.cl.cam.ac.uk/~afb21/CognitiveDimensions/CDtutorial.pdf)
- [Ko et al. — How Developers Seek, Relate, and Collect Relevant Information during Software Maintenance Tasks](https://doi.org/10.1109/TSE.2006.116)
- [Wyrich et al. — Source Code Comprehension: A Contemporary Definition and Conceptual Model for Empirical Investigation](https://arxiv.org/abs/2310.11301)
- [Fowler — Flag Argument](https://martinfowler.com/bliki/FlagArgument.html)
- [Fowler — Refactoring Boundary](https://martinfowler.com/bliki/RefactoringBoundary.html)

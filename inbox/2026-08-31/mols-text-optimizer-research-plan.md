# `mols-text-optimizer` 조사 및 구현 계획

`mols-text-optimizer`를 **내용·본질·기능을 훼손하지 않으면서 wording과 token 비용을 줄이고, 번역·재생성·요약·압축·다른 모델의 재해석을 거쳐도 핵심 의미와 행동 효과가 같은 쪽으로 수렴하도록 표현을 안정화하는 Skill**로 만들기 위한 조사와 구현 계획이다.

이 문서는 현재 정본이 아닌 Research + Plan artifact다. 실제 Skill 구현 전 설계 기준, 범위와 검증 조건을 고정하는 것이 목적이다.

## 결론

신규 Skill로 만들 가치가 있다. 다만 목표를 단순한 "문장 축약", "짧게 쓰기" 또는 "token compression"으로 정의하면 안 된다.

가장 적합한 책임은 다음과 같다.

> **기존 구조를 건드리지 않고, 같은 의미와 같은 행동 효과를 유지하는 범위에서 불필요한 wording 비용을 제거하며, 후속 변환에서도 semantic identity가 쉽게 이동하지 않도록 표현을 안정화하는 가장 작은 텍스트 변환을 수행한다.**

최적화 우선순위는 다음 순서를 가진다.

```text
1. 의미 보존
2. 기능·행동 보존
3. semantic identity 안정성 비저하
4. 모호성·변환 손실 위험 비증가
5. 추가 추론 비용 최소화
6. wording·token 비용 감소
```

6번을 위해 1~5번을 희생하지 않는다. 안전한 축약이 없으면 **변경하지 않는 것이 성공**이다.

조사에서 가장 중요한 결론은 세 가지다.

1. **semantic similarity만으로는 부족하다.** 특히 instruction, policy, prompt는 의미가 비슷해 보여도 downstream behavior가 달라질 수 있으므로 behavioral preservation을 별도 invariant로 봐야 한다.
2. **semantic preservation은 단어 유사도가 아니라 information relation 보존 문제다.** actor, action, condition, modality, negation, scope, order, exception과 같은 작은 요소가 전체 의미를 바꾼다.
3. **검증을 무겁게 만들면 Skill의 목적과 충돌한다.** 기본 실행은 한 번의 bounded transform과 한 번의 invariant scan으로 제한하고, embedding score, back-translation, best-of-N 또는 별도 judge를 기본 dependency로 두지 않는 것이 적절하다.

## Research questions

이번 조사에서는 다음 질문을 중심으로 근거를 확인했다.

1. 의미를 보존한 축약과 단순 요약을 어떻게 구분할 것인가?
2. 번역뿐 아니라 paraphrase, regeneration, summarization, compression과 multi-hop rewriting에서 어떤 정보가 잘 손실되는가?
3. semantic similarity가 높아도 기능이나 행동이 달라질 수 있는가?
4. 의미를 고정하는 데 효과적인 lexical·semantic 원칙은 무엇인가?
5. modality, negation, quantifier, condition과 scope 같은 작은 요소를 어떻게 취급해야 하는가?
6. 구조와 formatting을 이 Skill이 건드리지 않아야 할 추가 근거가 있는가?
7. 의미 보존을 확인하기 위해 무거운 evaluator가 필요한가?
8. prompt compression의 preprocessing 비용이 실제 token 절감을 상쇄할 수 있는가?
9. 기존 repository Skill과 신규 Skill의 책임이 겹치지 않는가?

## Scope

이 Skill은 **텍스트의 wording과 lexical semantic 표현만** 다룬다.

### In scope

- 의미 없는 반복과 중복 표현 제거
- 동일 의미의 더 짧고 직접적인 wording 선택
- 같은 concept의 용어 통일
- 다의적 표현, 모호한 지시어와 불명확한 reference 안정화
- condition, exception, negation, modality, scope와 relation을 보존하면서 local wording을 경량화
- 번역·재생성·요약·압축·재해석에서 semantic drift가 일어나기 어려운 표현 선택
- 동일 의미를 유지하면서 lexical variation과 synonym churn 감소
- 안전한 최적화가 없는 경우 원문 유지

### Out of scope

- 가독성 개선 자체
- 문서의 section 구성 또는 재배치
- heading 설계 또는 rename
- list/table/callout 선택이나 변환
- Markdown 구조와 information architecture
- paragraph 분리·병합·재배치
- 시각적 presentation
- 문서 navigation
- formatting 최적화
- 요약을 통한 정보량 축소
- tone, voice, 문체 개선
- 번역 자체
- 다른 형식으로의 format conversion 자체
- input/context를 latent representation으로 압축하는 compressor

문서 구조와 formatting은 optimization target이 아니다. **기본적으로 protected surface로 보존한다.**

이는 책임 경계뿐 아니라 행동 안정성 측면에서도 중요하다. 2025년 NAACL 연구는 의미와 무관한 prompt format 변화만으로도 LLM 성능이 크게 달라질 수 있는 prompt brittleness를 보고했다. 따라서 agent-facing text에서는 structure를 재배치하면서 "의미는 같으므로 기능도 같다"고 가정하면 안 된다.

구조 개선이 필요하면 `mols-markdown-for-human` 같은 해당 owner가 담당한다.

## 기존 Skill과의 경계

### `mols-markdown-for-human`

`mols-markdown-for-human`은 사람이 빠르게 읽고 탐색하도록 Markdown의 정보 구조와 presentation을 개선한다. `mols-text-optimizer`는 그 책임을 가져오지 않는다.

### `caveman-ko`

Repository에는 이미 `caveman-ko`가 있다. 이 Skill은 **명시적인 caveman-style 요청에만 활성화되는 response-style overlay**다.

`caveman-ko`는 생성되는 대화형 prose를 의도적으로 원시인 말투처럼 압축하며, 일반적인 "짧게", "간결하게", "토큰 아껴서" 요청만으로 trigger되는 것을 실패 사례로 정의한다. 또한 input/context/reasoning token optimizer가 아님을 명시한다.

따라서 `mols-text-optimizer`와 책임이 다르다.

| 요청 | 주 owner |
| --- | --- |
| Markdown 구조, heading, list/table, 읽기 흐름 개선 | `mols-markdown-for-human` |
| caveman-style로 응답 표현 압축 | `caveman-ko` |
| 기존 텍스트의 의미·기능을 보존하며 wording/token 비용 축소 | `mols-text-optimizer` |
| 후속 변환에서 semantic identity가 이동하기 어렵게 wording 안정화 | `mols-text-optimizer` |
| Agent Skill behavior를 보존하며 instruction wording 경량화 | `mols-agent-asset` + `mols-text-optimizer` |
| 자연스러운 한국어 문체로 AI 티 제거 | `humanize-korean` |
| 실제로 정보량을 줄여 핵심만 남기는 요약 | 별도 summarization 책임 |

`mols-text-optimizer`가 문서 구조, readability, response persona 또는 요약까지 소유하기 시작하면 기존 owner와 책임이 겹친다.

## "가벼운 텍스트"의 정의

토큰 수 하나만을 목표로 삼지 않는다.

Tokenizer마다 같은 문자열의 token count가 다르고, 더 짧은 문자열이 더 낮은 end-to-end inference 비용을 항상 보장하지도 않는다. 2026년 `Prompt Compression in the Wild`는 prompt compression의 preprocessing overhead가 적절한 prompt length, compression ratio와 hardware 조건이 아닐 때 decoding 절감을 상쇄할 수 있음을 대규모 실험으로 보여준다.

따라서 기본 optimization signal은 다음과 같다.

- 중복된 의미 단위
- 의미 없는 framing 또는 transition
- 반복되는 같은 rule, constraint 또는 qualification
- 같은 concept을 표현하는 synonym churn
- 의미를 추가하지 않는 장황한 phrase
- 안전하게 대체 가능한 긴 wording
- target tokenizer가 명시되었을 때의 실제 token count

정확한 tokenizer가 주어지지 않은 상태에서는 **언어적 redundancy 감소가 primary optimization**이고 token count는 결과 지표에 가깝다.

다음은 optimization metric이 아니다.

- section 수
- heading depth
- paragraph 수
- list/table 수
- visual density
- 읽기 흐름

## Core model: semantic identity + behavioral identity

### Semantic identity

문자열이 같을 필요는 없다. 다음 정보와 그 관계가 같아야 한다.

```text
entities / concepts
+ properties
+ actors
+ actions
+ objects / targets
+ conditions
+ modality
+ negation
+ quantifiers
+ scope
+ ordering
+ causal / logical relations
+ exceptions
+ uncertainty
+ identifiers / quantities
```

### Behavioral identity

Instruction, policy, prompt, specification처럼 텍스트가 downstream behavior를 제어할 때는 의미 보존만으로 충분하지 않다.

다음 behavior-bearing semantics가 동일해야 한다.

- 어떤 조건에서 rule이 활성화되는가
- 누가 무엇을 해야 하는가
- 무엇이 필수, 권고, 허용 또는 금지인가
- 어떤 순서로 action이 실행되는가
- 어떤 exception이나 fallback이 있는가
- permission, safety와 scope boundary가 같은가
- input/output/side effect/failure behavior가 같은가
- exact identifier, command, path 또는 schema token이 같은 대상을 가리키는가

2026년 PMLR의 context-compression 연구는 **높은 semantic reconstruction fidelity가 있어도 refusal alignment behavior가 약화될 수 있음**을 보여준다. 이는 compressed representation 연구이므로 자연어 wording 변환과 동일한 문제는 아니지만, 중요한 일반 원칙을 제공한다.

> **semantic preservation claim과 behavioral preservation claim을 같은 것으로 취급하지 않는다.**

Prompt paraphrase 연구에서도 semantically equivalent wording이 model behavior를 바꿀 수 있는 현상이 반복적으로 관찰된다. 따라서 agent-facing instruction 최적화는 wording의 뜻뿐 아니라 activation과 downstream behavior의 보존을 요구해야 한다.

## 의미 보존 계약

최적화 전에 원문에서 다음을 **semantic anchors**로 취급한다.

- 사실과 주장
- actor / subject
- action / operation
- object / target
- 조건과 전제
- trigger와 precondition
- 예외와 fallback
- 부정
- 의무 강도와 가능성
- 허용과 금지
- 범위와 경계
- 순서와 dependency
- 원인과 결과
- 관계와 cardinality
- quantifier와 comparator
- 불확실성 또는 epistemic strength
- 숫자, 단위, 날짜, 비율과 threshold
- identifier, 이름, path, command, API, field, code token
- 입력, 출력, side effect와 failure behavior
- citation, attribution과 provenance가 의미를 가질 때의 연결

문서 구조와 formatting은 semantic optimization 대상이 아니지만 **protected invariant**다.

최적화 후 semantic anchor 중 하나라도 사라지거나 강도, scope, binding 또는 relation이 바뀌면 실패다.

### 특히 위험한 손실

다음 변화는 짧아졌더라도 허용하지 않는다.

```text
must -> should
must not -> should not
may -> will
not required -> optional
A only if B -> A when B
A before B -> A and B
all -> some
exactly one -> one
at least 3 -> 3
can fail -> fails
likely -> true
unless B -> if B
A except B -> A
```

RFC 2119/8174가 `MUST`, `SHOULD`, `MAY`를 서로 다른 requirement level로 명확히 구분하는 이유와도 일치한다. 이런 modality는 몇 글자 차이로 normative force 전체를 바꾸므로 compression target으로 공격적으로 줄이면 안 된다.

## Requirement semantics에서 얻는 설계 근거

Requirements Engineering의 controlled natural language 연구는 functional requirement가 단순한 bag of words가 아니라 **정보 역할과 relation**으로 구성됨을 보여준다.

Rimay 연구에서는 requirement를 scope, pre-condition, actor와 system response 같은 정보 content로 분석하고, 일부 정보가 target representation에 담기지 않으면 requirement를 non-representable로 분류한다. EARS 계열도 precondition, trigger, system response의 순서와 binding을 중요하게 취급한다.

이 관점은 `mols-text-optimizer`에 직접 적용할 수 있다.

> **짧아졌는지가 아니라 원문의 semantic roles와 relation을 모두 표현할 수 있는지가 먼저다.**

따라서 의미 보존 검토에서 단어 수보다 다음 질문이 중요하다.

```text
actor가 같은가?
action이 같은가?
target이 같은가?
condition이 같은 action에 binding되는가?
modality가 같은가?
exception이 같은 범위를 가지는가?
order/dependency가 같은가?
```

## Semantic identity stability

사용자가 요구한 안정성은 번역에만 한정하지 않는다. 텍스트는 실제 workflow에서 여러 semantic transform을 거친다.

- 다른 언어로 translation
- 같은 언어로 regeneration / paraphrase
- summarization
- prompt/context compression
- 다른 model 또는 agent의 재설명·재작성
- 일부 발췌 후 재사용
- multi-hop human/AI handoff

2025년 IJCNLP-AACL 연구는 human-only, LLM-only, mixed, cross-LLM 환경을 포함한 700개의 5-step transmission chain을 조사하면서 multi-hop rewriting에서 semantic drift와 hallucination propagation을 별도 측정 대상으로 다뤘다.

따라서 원문이 한 번만 정확하면 충분한 것이 아니라, **재표현될 때 선택 가능한 의미 분기 자체를 줄이는 wording**이 유리하다.

이를 여기서는 `semantic identity stability`로 부른다.

> **표현이 다시 생성되더라도 핵심 semantic anchors와 그 relation이 같은 의미로 재구성될 가능성을 높인다.**

## Ambiguity control

### One concept, one preferred term

ASD-STE100 Simplified Technical English는 controlled vocabulary에서 가능한 경우 one word–one meaning을 지향하고, 같은 의미의 여러 synonym 중 하나를 선택한다.

이 원칙을 범용 규격으로 복제하지는 않지만 다음 heuristic은 흡수 가치가 높다.

- 같은 concept에는 같은 term을 유지한다.
- 문학적 다양성보다 semantic identity를 우선한다.
- domain term은 짧은 일반어로 바꾸지 않는다.
- synonym 교체가 token을 조금 줄여도 concept boundary가 넓어지면 유지한다.

### Narrow meaning over shortest word

더 짧은 단어라도 다의성이 크면 후속 transform에서 잘못된 sense가 선택될 가능성이 높다.

2026년 ACL Findings의 Deferred Semantic Drift 연구는 ambiguous word의 의미가 뒤에 오는 context에 의해 나중에 재해석되는 LLM 내부 현상을 분석했다. 이 연구를 wording rule로 직접 일반화할 수는 없지만, **초기 lexical ambiguity가 downstream context resolution 부담을 만든다**는 설계 방향을 강화한다.

따라서 목표는 shortest token이 아니라 **shortest stable meaning**이다.

### Explicit reference where ambiguity matters

다음 표현은 압축에 유리해 보여도 semantic identity가 약하다.

```text
그것
이 경우
앞의 것
이전처럼
필요하면 처리한다
```

Reference가 명확하지 않으면 발췌, translation, summarization 또는 regeneration에서 다른 antecedent가 선택될 수 있다.

필요하면 실제 concept/actor/action을 유지한다.

### Avoid introducing idiom and metaphor

ASD-STE100과 controlled-language 연구가 ambiguity를 줄이는 이유와 같은 방향으로, optimizer는 원문에 없던 idiom, metaphor, 문화 의존 shorthand를 새로 넣지 않는다.

특히 translation을 거칠 가능성이 있는 technical/instruction text에서는 literal, domain-standard wording을 우선한다.

## Transform-resilience model

이 Skill이 보존하려는 것은 문자열 동일성이 아니다.

다른 model이 문장을 완전히 다르게 재생성하더라도 다음 graph가 같으면 semantic identity가 보존된 것으로 볼 수 있다.

```text
[actor] --action--> [target]
   |                  |
 condition          quantity
   |                  |
 modality          constraint
   |
 exception / scope / order
```

반대로 단어 대부분이 같아도 relation이나 modality가 바뀌면 실패다.

### 양방향 보존 intuition

Paraphrase identification과 textual inference 연구에서는 semantic equivalence와 one-way entailment를 구분한다. 이를 runtime NLI evaluator로 쓰자는 뜻은 아니다.

다만 optimizer의 mental model로 유용하다.

- optimized text가 원문의 일부만 말하면 → 정보가 빠진 요약일 수 있다.
- optimized text가 원문보다 더 강한 claim을 만들면 → 의미를 추가한 변형일 수 있다.
- 두 방향 모두에서 핵심 semantic anchors와 relation이 회수되어야 → preservation에 가깝다.

즉 **"원문에서 틀린 말은 아니다"는 보존 기준으로 부족하다.**

## Translation은 하나의 stress case일 뿐이다

Translation stability는 중요한 요구지만 Skill의 목적 전체는 아니다.

ASD-STE100은 synonym과 polysemy를 통제하면 human translator, neural MT와 LLM translation에서 이해와 변환이 쉬워지는 방향을 설명한다. 2026년 LREC 연구도 modern MT/LLM translation에서 semantic label 또는 stance 같은 의미 속성이 drift할 수 있음을 보여준다.

따라서 optimizer는 translation-friendly wording을 선호하지만, 특정 language pair 또는 MT engine에 맞게 문장을 튜닝하지 않는다.

### Back-translation을 기본 검증기로 쓰지 않는다

Back-translation 자체도 또 하나의 생성 transform이다. 원문과 결과 사이에 새로운 drift를 만들 수 있으므로 "다시 번역했더니 비슷하다"를 semantic preservation의 universal oracle로 사용하지 않는다.

고가치 별도 evaluation에서 참고 신호로 쓸 수는 있지만 Skill의 기본 실행에는 넣지 않는다.

## Prompt compression에서 얻는 교훈과 경계

LLMLingua와 LongLLMLingua는 별도 model 또는 token-level importance estimation을 통해 매우 높은 prompt compression ratio와 downstream performance 유지를 보여준다.

하지만 `mols-text-optimizer`는 이런 compressor를 복제하지 않는다.

### 흡수할 교훈

- 모든 token의 중요도가 같지 않다.
- key information과 instruction integrity가 compression보다 우선한다.
- compression ratio는 task와 context에 따라 달라야 한다.
- 높은 compression이 항상 높은 실제 효율을 뜻하지 않는다.

### 흡수하지 않을 구현

- 별도 compressor model
- entropy/perplexity 기반 token deletion
- target model distribution alignment
- question-aware document reordering
- latent/context representation compression
- 특정 model/tokenizer에 묶인 algorithm

Microsoft Research도 LLMLingua의 token-level compressed prompt가 사람이 읽기 어려운 형식이 될 수 있음을 명시한다. 이 Skill은 portable text asset을 다루므로 그런 representation은 목적과 맞지 않는다.

## Compression safety ladder

큰 rewrite보다 의미 위험이 낮은 local transform부터 적용한다.

```text
1. exact duplicate 제거
2. semantic duplicate wording 제거
3. 의미 없는 framing/filler 제거
4. 같은 concept의 term 통일
5. 장황하지만 의미가 동일한 local phrase 단축
6. ambiguous reference를 stable reference로 교체
7. 더 이상 명확한 안전 이득이 없으면 stop
```

### 낮은 위험

- 같은 의미의 완전한 반복
- 의미 없는 opening/closing filler
- 동일 concept에 대한 불필요한 synonym churn
- 의미를 추가하지 않는 template phrase

### 높은 위험

- function word 삭제로 condition binding 변경
- modality 축약
- negation 재작성
- quantifier 제거
- uncertainty marker 제거
- actor/object 생략
- exception을 본문에 암시적으로 흡수
- 여러 clause를 하나로 합치기
- pronoun/ellipsis로 explicit reference 축소
- structure 또는 formatting 변경

고위험 transform은 token saving이 명확해도 기본적으로 보수적으로 유지한다.

## Structure is a protected surface

사용자 요구에 따라 가독성, section과 구조는 이 Skill에서 다루지 않는다.

조사 결과 이 결정은 기술적으로도 타당하다.

2025년 NAACL 연구는 small non-semantic prompt format change가 LLM performance variation을 일으킬 수 있다고 보고한다. 따라서 agent-facing text에서 다음을 optimizer가 임의로 바꾸면 안 된다.

- heading hierarchy
- list ordering과 numbering
- paragraph boundaries
- table/list representation
- code fence
- delimiters
- XML/JSON/YAML-like syntax
- indentation
- exact formatting contract

일반 prose에서 구조가 기능에 영향을 주지 않는다고 추정되더라도 이 Skill은 그 판단을 소유하지 않는다. 구조 변화는 해당 document/asset owner가 별도 책임으로 수행한다.

## 의미 보존 metric 하나를 두지 않는 이유

### Surface similarity는 부족하다

높은 lexical overlap이 semantic identity를 증명하지 않는다. `must`와 `should`처럼 한 단어 차이가 behavior를 바꿀 수 있다.

### Embedding similarity도 universal oracle가 아니다

2024년 EMNLP Findings의 `ALIGN-SIM`은 classical/LLM-induced sentence embedding 13종을 semantic distinction, synonym/antonym replacement, paraphrase, sentence jumbling 등으로 평가했고 어느 encoder도 모든 semantic alignment criterion에 맞지 않았다고 보고한다.

### Factuality metric도 meaning-preserving variation에 흔들린다

2026년 ACL의 long-document factuality metric stress test는 paraphrase, simplification, synonym replacement, logically equivalent negation, vocabulary reduction과 compression처럼 factuality-preserving perturbation에 기존 metric들이 inconsistent score를 낼 수 있음을 보여준다.

### Text simplification 자체도 의미를 잃는다

TACL 2024의 human evaluation에서는 자동 simplification system 중 가장 좋은 supervised system도 simplified content만으로 최소 14%의 comprehension question을 answerable하게 유지하지 못했다.

따라서 `mols-text-optimizer`는 자동 metric 하나를 의미 보존의 절대 판정기로 두지 않는다.

## Runtime validation strategy

기본 workflow는 **한 번의 transform + 한 번의 bounded invariant scan**이다.

```text
1. Preserve
   semantic / behavioral anchors를 짧게 식별

2. Reduce
   명확하게 안전한 lexical redundancy만 제거

3. Stabilize
   terminology, reference와 ambiguity를 local하게 정리

4. Check
   omission / strength / scope / relation / identity 변화를 확인

5. Stop
   다음 pass의 이득이 작거나 불확실하면 종료
```

### Check questions

전체 문장을 다시 증명하려 하지 않고 다음 질문만 확인한다.

```text
빠진 사실/규칙이 있는가?
actor/action/target이 바뀌었는가?
condition 또는 exception binding이 바뀌었는가?
modality/negation/quantifier/uncertainty가 바뀌었는가?
scope/order/causal relation이 바뀌었는가?
identifier/quantity/unit이 바뀌었는가?
agent-facing text라면 activation/permission/behavior가 달라질 수 있는가?
구조 또는 formatting을 건드렸는가?
```

하나라도 확실하지 않으면 해당 transform을 revert하거나 원문을 유지한다.

## 기본 경로에서 금지할 검증 전략

다음은 특정 evaluation이나 고가치 audit에서 사용할 수 있지만 runtime 기본 경로에는 넣지 않는다.

- best-of-N candidate 생성
- 여러 LLM judge 비교
- 반복 semantic scoring
- embedding similarity threshold gate
- token별 entropy 계산
- 상시 translation/back-translation
- 반복 regeneration test
- 여러 tokenizer 전수 비교
- 목표 compression ratio까지 재귀 rewrite

이유는 세 가지다.

1. optimizer 자체의 inference cost가 증가한다.
2. evaluator 자체도 semantic variation에 brittleness를 가질 수 있다.
3. 작은 wording 절감을 위해 별도 generation chain을 만드는 것은 end-to-end 비용 목표와 모순된다.

## Development-time evaluation은 runtime과 분리한다

Skill runtime을 가볍게 유지하는 것과 Skill 개발 단계에서 강하게 검증하는 것은 모순되지 않는다.

구현 후에는 adversarial fixture를 이용해 다음을 반복적으로 검토하는 것이 좋다.

- semantic preservation
- behavioral preservation
- near-miss activation
- no-op stop condition
- structure preservation
- modality/negation/quantifier preservation
- coreference와 ambiguity
- token saving이 실제로 발생하는 safe case

이 fixture/eval은 Skill의 매 실행마다 호출되는 runtime dependency가 아니다.

## Stop conditions

다음 중 하나면 보수적으로 종료한다.

- 의미 보존 여부가 확실하지 않다.
- behavioral effect가 달라질 수 있다.
- 더 짧은 wording이 더 ambiguous하다.
- condition, modality 또는 relation을 압축해야만 더 줄일 수 있다.
- structure/formatting을 변경해야 한다.
- 남은 변경이 stylistic preference 수준이다.
- token saving이 미미하고 semantic review 비용이 더 크다.
- target compression ratio를 맞추려면 정보 손실이 필요하다.
- 이미 충분히 짧아서 rewrite가 churn만 만든다.

## Proposed Skill workflow

```text
Input text
  ↓
Identify protected semantics
  ↓
Remove obvious lexical redundancy
  ↓
Stabilize terminology/reference where needed
  ↓
Reduce local wording only when equivalence is clear
  ↓
Bounded semantic + behavioral invariant scan
  ↓
Return optimized text or unchanged input
```

## Initial package

```text
src/rulesync/.rulesync/skills/mols-text-optimizer/
└── SKILL.md
```

처음부터 reference, tokenizer utility, evaluator 또는 별도 script를 만들지 않는다.

다음 조건이 반복적으로 확인될 때만 reference를 분리한다.

- core `SKILL.md`가 실제 loading cost를 유의미하게 키운다.
- 특정 조건부 detail이 모든 activation에 필요하지 않다.
- 분리된 reference가 responsibility를 중복하지 않고 명확한 loading benefit을 준다.

## Proposed activation boundary

초기 description은 다음 intent를 선명하게 잡아야 한다.

- text/token 경량화
- wording compression
- 의미 보존 축약
- semantic-preserving shortening
- instruction/prose의 lexical redundancy 제거
- semantic drift를 줄이는 wording stabilization
- 내용과 기능을 유지한 채 표현 비용 최적화

반대로 다음 요청만으로는 선택하지 않는다.

- Markdown 가독성 개선
- section/heading 구조 개선
- 문서 재구성
- 단순 요약
- 단순 번역
- 문체 윤문
- grammar correction만 필요한 경우
- caveman-style response
- latent prompt/context compressor 요청

## Acceptance conditions

- 내용, 본질, 의미와 기능을 token reduction보다 우선한다.
- semantic similarity와 behavioral identity를 혼동하지 않는다.
- 의미 또는 행동 변화 가능성이 있으면 원문을 유지한다.
- 가독성, section, heading, list/table와 문서 구조를 직접 최적화하지 않는다.
- 기존 structure와 formatting을 protected surface로 유지한다.
- actor, action, target을 보존한다.
- condition, trigger, exception과 fallback binding을 보존한다.
- negation, modality, quantifier, uncertainty, scope, order와 causal/logical relation을 보존한다.
- identifier, path, command, API, 수치, threshold와 unit을 보존한다.
- 같은 concept에 불필요한 synonym variation을 만들지 않는다.
- 더 짧은 다의어보다 의미가 좁고 안정적인 wording을 선호한다.
- translation뿐 아니라 regeneration, summarization, compression과 model handoff에서도 semantic identity가 흔들리기 어려운 표현을 선호한다.
- agent-facing text에서는 activation, permission, safety와 downstream behavior를 보존한다.
- 별도 compressor model이나 반복 validator를 기본 dependency로 요구하지 않는다.
- embedding/BERTScore/back-translation 같은 단일 metric을 universal preservation oracle로 두지 않는다.
- 목표 compression ratio를 맞추기 위해 의미를 희생하지 않는다.
- 최적화 이득이 불확실하면 추가 pass 없이 종료한다.
- `mols-markdown-for-human`, `caveman-ko`, `humanize-korean`, summarization과 책임 경계가 명확하다.

## Adversarial review cases

1. `must`를 `should`로 바꾸면 token이 비슷하거나 줄어드는 instruction
2. `must not`을 단순 부정 표현으로 바꾸면서 prohibition strength가 약해지는 경우
3. 명시적 subject를 대명사로 줄이면 antecedent가 모호해지는 문장
4. 같은 concept을 여러 synonym으로 표현한 텍스트
5. 긴 domain term을 더 짧지만 다의적인 일반어로 바꾸려는 경우
6. condition clause 삭제로 edge-case behavior가 달라지는 경우
7. quantifier가 축약 과정에서 사라지는 경우
8. `not required`를 `optional`로 바꾸며 permission semantics가 달라지는 경우
9. uncertainty marker를 filler로 오인해 삭제하는 경우
10. identifier를 abbreviation으로 바꾸려는 경우
11. section/format 변경으로 더 짧게 만들려는 경우
12. 이미 충분히 짧아 rewrite가 stylistic churn만 만드는 경우
13. 한국어 주어 생략으로 regeneration 시 actor가 달라질 수 있는 경우
14. idiom 사용으로 다른 model이 다른 meaning을 선택할 수 있는 경우
15. technical term을 synonym으로 바꿔 domain identity가 흔들리는 경우
16. token 수는 줄지만 telegraphic text가 되는 경우
17. 여러 candidate 비교가 있어야만 작은 절감이 가능한 경우
18. `이전처럼 처리한다` 같은 implicit reference가 다른 대상을 가리킬 수 있는 경우
19. order relation이 paraphrase에서 parallel relation으로 바뀔 수 있는 경우
20. exception이 너무 암시적이라 summarization에서 쉽게 사라지는 경우
21. regeneration마다 같은 concept이 서로 다른 label로 갈라질 가능성이 높은 경우
22. readability를 이유로 section/paragraph order를 바꾸려는 경우
23. wording은 거의 같지만 `all`이 `some`으로 바뀌는 경우
24. `at least`, `at most`, `exactly`가 삭제되는 경우
25. 원문에는 없는 stronger claim을 "명확화"라는 이유로 추가하는 경우
26. 원문의 일부만 남겨 사실상 summary가 되는 경우
27. agent Skill의 trigger 문구를 줄였더니 activation boundary가 넓어지는 경우
28. safety/permission constraint를 중복 문장이라고 제거하는 경우
29. prompt format을 줄이기 위해 delimiter/list를 바꾸는 경우
30. BERTScore가 높다는 이유만으로 modality drift를 승인하는 경우
31. back-translation이 비슷하다는 이유만으로 원문과의 information loss를 승인하는 경우
32. exact tokenizer가 지정되지 않았는데 특정 tokenizer의 우연한 tokenization을 일반 최적화로 주장하는 경우
33. compression overhead가 절감량보다 큰데 반복 evaluator를 실행하는 경우
34. caveman-style fragment를 일반 text optimization 결과로 사용하는 경우

## Implementation plan

1. 최소 package로 `SKILL.md`를 생성한다.
2. description에 semantic-preserving wording/token reduction과 semantic identity stabilization trigger를 명확히 한다.
3. `Preserve → Reduce → Stabilize → Check → Stop`의 bounded workflow를 작성한다.
4. semantic identity와 behavioral identity를 분리해 core contract에 명시한다.
5. semantic anchors와 high-risk atoms를 core contract에 포함한다.
6. structure/formatting을 out-of-scope이자 protected surface로 명시한다.
7. runtime validation을 omission / strength / scope / binding / relation / identity drift에 한정한다.
8. best-of-N, back-translation, embedding score와 별도 judge를 기본 경로에서 금지한다.
9. `caveman-ko`, `mols-markdown-for-human`, `humanize-korean`, summarization과 boundary를 description/self-check에서 검토한다.
10. `mols-agent-asset` 기준으로 responsibility, trigger, source authority와 always-loaded context를 self-review한다.
11. development-time adversarial fixtures로 behavior를 검토하고 필요할 때만 수정한다.
12. generated route가 필요한 경우 repository-native 방식으로 동기화한다.
13. 최종 Review에서 별도 reference, evaluator 또는 deterministic helper가 실제 benefit 없이 추가되지 않았는지 확인한다.

## Research evidence and implications

| Source | Evidence | Design implication |
| --- | --- | --- |
| ASD-STE100 Simplified Technical English, Issue 9 / FAQ | controlled vocabulary, 가능한 경우 one word–one meaning, synonym variation 제한, ambiguity 감소 | 같은 concept에 안정적인 preferred term을 쓰고 polysemy를 줄인다 |
| Agrawal & Carpuat, TACL 2024, *Do Text Simplification Systems Preserve Meaning?* | simplification이 의미 보존을 자동으로 보장하지 않으며 best supervised system도 comprehension information을 놓침 | shortening 자체를 success로 간주하지 않는다 |
| Shi et al., *SEM 2024, *Paraphrase Identification via Textual Inference* | semantic equivalence와 asymmetric entailment의 관계를 formalize | preservation을 양방향 information coverage intuition으로 본다 |
| Acharjee et al., IJCNLP-AACL 2025, *Who Remembers What?* | multi-hop human/AI rewriting chain에서 semantic drift와 hallucination propagation을 별도 측정 | 한 번의 translation이 아니라 repeated transform resilience를 목표로 한다 |
| Fu & Barez, EMNLP 2025, *Same Question, Different Words* | semantically equivalent prompt paraphrase에서도 model performance가 달라질 수 있음 | agent-facing text는 semantic + behavioral preservation을 요구한다 |
| Ngweta et al., NAACL 2025, *Towards LLMs Robustness to Changes in Prompt Format Styles* | non-semantic prompt format change에도 performance fluctuation 발생 | structure/formatting은 optimizer가 건드리지 않는 protected surface로 둔다 |
| Nguyen & Lin, Canadian AI / PMLR 2026, *Does Context Compression Preserve Refusal Alignment?* | high reconstruction fidelity가 있어도 refusal behavior가 약화될 수 있음 | semantic preservation과 downstream behavior preservation을 분리한다 |
| Mujahid et al., ACL 2026, *Stress Testing Factual Consistency Metrics for Long-Document Summarization* | meaning-preserving perturbation에 기존 factuality metric score가 inconsistent | 자동 metric 하나를 universal oracle로 두지 않는다 |
| Mahajan et al., EMNLP Findings 2024, *ALIGN-SIM* | 조사한 sentence embedding이 모든 semantic alignment criterion을 만족하지 못함 | embedding similarity를 기본 preservation gate로 두지 않는다 |
| Veizaga et al., Empirical Software Engineering 2021, *Rimay* | requirement meaning을 scope/precondition/actor/response 등의 information content로 모델링 | wording이 아니라 semantic role과 relation을 anchor로 본다 |
| RFC 2119 + RFC 8174 / BCP 14 | MUST/SHOULD/MAY 등의 requirement level 구분 | modality를 compression-resistant atom으로 취급한다 |
| Jiang et al., EMNLP 2023 / ACL 2024, LLMLingua series | 높은 prompt compression이 가능하지만 별도 compressor와 task/model-aware strategy 사용 | 연구 교훈만 흡수하고 compressor 구현은 범위 밖에 둔다 |
| Kummer et al., 2026, *Prompt Compression in the Wild* | preprocessing overhead가 operating window 밖에서 latency gain을 상쇄 | optimizer의 runtime 검증 비용을 bounded하게 유지한다 |
| Kabir et al., LREC 2026, *Semantic Label Drift in Cross-Cultural Translation* | modern MT/LLM translation에서도 semantic label drift 발생 | translation은 semantic stability stress case이며 lexical ambiguity를 줄일 가치가 있다 |
| Shafiabadi & Yvon, LREC 2026, *Biases in Translation* | lexical/semantic fidelity가 stance 같은 subjective meaning 보존을 보장하지 않음 | surface/semantic similarity 외에도 intent/stance/uncertainty처럼 의미 역할을 보존한다 |

## Research references

- ASD-STE100 Simplified Technical English FAQ — https://www.asd-ste100.org/STE_faq.html
- ASD-STE100 current standard information — https://www.asd-ste100.org/
- Sweta Agrawal, Marine Carpuat. *Do Text Simplification Systems Preserve Meaning? A Human Evaluation via Reading Comprehension*. TACL 2024 — https://aclanthology.org/2024.tacl-1.24/
- Ning Shi, Bradley Hauer, Jai Riley, Grzegorz Kondrak. *Paraphrase Identification via Textual Inference*. *SEM 2024 — https://aclanthology.org/2024.starsem-1.11/
- Suvojit Acharjee et al. *Who Remembers What? Tracing Information Fidelity in Human-AI Chains*. IJCNLP-AACL 2025 — https://aclanthology.org/2025.ijcnlp-long.146/
- Tingchen Fu, Fazl Barez. *Same Question, Different Words: A Latent Adversarial Framework for Prompt Robustness*. EMNLP 2025 — https://aclanthology.org/2025.emnlp-main.1595/
- Lilian Ngweta et al. *Towards LLMs Robustness to Changes in Prompt Format Styles*. NAACL SRW 2025 — https://aclanthology.org/2025.naacl-srw.51/
- Anthony Nguyen, Wenjun Lin. *Does Context Compression Preserve Refusal Alignment?*. PMLR 2026 — https://proceedings.mlr.press/v318/nguyen26a.html
- Zain Muhammad Mujahid, Dustin Wright, Isabelle Augenstein. *Stress Testing Factual Consistency Metrics for Long-Document Summarization*. ACL 2026 — https://aclanthology.org/2026.acl-long.1472/
- Yash Mahajan et al. *ALIGN-SIM: A Task-Free Test Bed for Evaluating and Interpreting Sentence Embeddings through Semantic Similarity Alignment*. Findings of EMNLP 2024 — https://aclanthology.org/2024.findings-emnlp.436/
- Alvaro Veizaga et al. *On systematically building a controlled natural language for functional requirements*. Empirical Software Engineering 2021 — https://link.springer.com/article/10.1007/s10664-021-09956-6
- RFC 2119 — https://www.rfc-editor.org/info/rfc2119/
- RFC 8174 — https://www.rfc-editor.org/info/rfc8174/
- Huiqiang Jiang et al. *LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models*. EMNLP 2023 — https://aclanthology.org/2023.emnlp-main.825/
- Huiqiang Jiang et al. *LongLLMLingua*. ACL 2024 — https://aclanthology.org/2024.acl-long.91/
- Cornelius Kummer et al. *Prompt Compression in the Wild: Measuring Latency, Rate Adherence, and Quality for Faster LLM Inference*. 2026 — https://arxiv.org/abs/2604.02985
- Mohsinul Kabir et al. *Semantic Label Drift in Cross-Cultural Translation*. LREC 2026 — https://aclanthology.org/2026.lrec-1.297/
- Nazanin Shafiabadi, François Yvon. *Biases in Translation: Assessing Opinion Distortion in Machine Translated Texts*. LREC 2026 — https://aclanthology.org/2026.lrec-1.679/
- Jingjie Zeng et al. *Mechanistic Insights into Deferred Semantic Drift in LLMs*. Findings of ACL 2026 — https://aclanthology.org/2026.findings-acl.57/

외부 연구는 설계 근거이며 Skill의 동작 authority가 아니다. 실제 Skill은 특정 compressor, tokenizer, embedding model, evaluator, controlled-language standard 또는 target LLM을 dependency로 삼지 않는다.

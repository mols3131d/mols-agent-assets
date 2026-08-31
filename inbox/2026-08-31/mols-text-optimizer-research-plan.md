# `mols-text-optimizer` 조사 및 구현 계획

`mols-text-optimizer`를 **내용·본질·기능을 훼손하지 않으면서 텍스트와 토큰 비용을 줄이고, 번역·재생성·요약·압축·다른 모델의 재해석을 거쳐도 핵심 의미와 기능이 같은 쪽으로 수렴하도록 표현을 안정화하는 Skill**로 만들 수 있는지 조사한 결과와 구현 계획을 정리한다.

이 문서는 현재 정본이 아닌 Research + Plan artifact다. 실제 Skill 구현 전 설계 기준과 검증 조건을 고정하는 것이 목적이다.

## 결론

신규 Skill로 만들 가치가 있다. 다만 목표를 단순한 "문장 축약"이나 "token compression"으로 정의하면 안 된다.

가장 적합한 책임은 다음과 같다.

> **같은 의미와 같은 동작을 유지하는 범위에서 불필요한 표현 비용을 제거하고, 이후의 번역·재생성·압축·재해석에서도 의미가 쉽게 이동하지 않도록 semantic identity를 선명하게 고정하는 가장 작은 텍스트 변환을 수행한다.**

최적화 우선순위는 반드시 다음 순서를 가진다.

```text
1. 의미·기능 보존
2. semantic identity 안정성 비저하
3. 모호성·변환 손실 위험 비증가
4. 이해·추론 비용 비증가
5. 텍스트·토큰 비용 감소
```

5번을 위해 1~4번을 희생하지 않는다. 안전한 축약이 없으면 **변경하지 않는 것이 성공**이다.

Prompt compression 연구는 prompt token 수를 크게 줄일 수 있음을 보여주지만 별도 압축 모델·알고리즘을 쓰는 경우가 많고, 전처리 비용이 end-to-end 이득을 상쇄할 수 있다. 이 Skill의 기본 경로는 별도 compression pipeline이나 반복 추론을 요구하지 않아야 한다.

또한 ASD-STE100 Simplified Technical English와 controlled-language 접근은 **한 의미에 한 용어를 일관되게 쓰고, 다의어와 불필요한 표현 변이를 줄이는 것**이 번역과 재해석의 안정성에 유리한 방향임을 보여준다. 따라서 "더 짧은 유의어"를 고르는 것이 아니라 **더 짧으면서 의미 범위가 좁고 반복 변환에서도 동일 개념으로 복원되기 쉬운 표현**을 고르는 방향이 적절하다.

## Scope

이 Skill은 **텍스트 표현 자체**만 다룬다.

### In scope

- 의미 없는 반복과 중복 표현 제거
- 동일 의미의 더 짧고 직접적인 표현 선택
- 같은 개념의 용어 통일
- 다의적 표현, 모호한 지시어와 불명확한 관계의 안정화
- 조건, 예외, 부정, modality, scope와 관계를 보존하면서 문장을 더 가볍게 만드는 변환
- 번역·재생성·요약·압축·재해석에서 semantic drift가 일어나기 어려운 wording 선택
- 안전한 최적화가 없는 경우 원문 유지

### Out of scope

- 가독성 개선 자체
- 문서의 section 구성 또는 재배치
- heading 설계
- list/table/callout 선택이나 변환
- Markdown 구조와 information architecture
- paragraph 재배치
- 시각적 presentation
- 문서 navigation
- formatting 최적화
- 요약을 통한 정보량 축소
- tone, voice, 문체 개선
- 번역 자체
- 다른 형식으로의 포맷 변환 자체

문서 구조와 formatting은 최적화 대상이 아니다. 입력에 존재하는 구조가 의미나 기능을 가질 수 있으므로 **기본적으로 그대로 보존한다**. 구조 개선이 필요하면 `mols-markdown-for-human` 같은 해당 owner가 담당한다.

## 기존 Skill과의 경계

`mols-markdown-for-human`은 사람이 빠르게 읽고 탐색하도록 Markdown의 정보 구조와 표현을 개선한다. `mols-text-optimizer`는 그 책임을 가져오지 않는다.

| 요청 | 주 owner |
| --- | --- |
| Markdown 구조, heading, list/table, 읽기 흐름 개선 | `mols-markdown-for-human` |
| 같은 의미를 유지하며 wording과 token 비용 축소 | `mols-text-optimizer` |
| 번역·재생성·압축 등 후속 변환에서 의미가 이동하기 어렵게 표현 안정화 | `mols-text-optimizer` |
| Agent Skill의 behavior를 보존하며 instruction wording을 경량화 | `mols-agent-asset` + `mols-text-optimizer` |
| 자연스러운 한국어 문체로 AI 티 제거 | `humanize-korean` |
| 실제로 내용을 줄여 핵심만 남기는 요약 | 별도 summarization 책임 |

`mols-text-optimizer`가 문서 가독성이나 구조를 직접 개선하기 시작하면 `mols-markdown-for-human`과 책임이 겹친다. 따라서 입력 구조는 invariant로 취급한다.

## "가벼운 텍스트"의 정의

토큰 수 하나만을 목표로 삼지 않는다. tokenizer마다 같은 문자열의 token count가 달라지고, 더 짧은 문자열이 더 적은 추론 비용을 항상 보장하지도 않는다.

기본적으로 다음 비용을 본다.

- 중복된 의미 단위
- 불필요한 문장·절·수식
- 반복되는 같은 규칙이나 조건
- 의미 없는 transition 또는 template phrase
- 같은 개념을 표현하는 synonym churn
- 문자/단어 길이
- target tokenizer가 명시되었을 때의 실제 token count

정확한 tokenizer가 주어지지 않은 상태에서는 **언어적 중복을 줄이는 것이 primary optimization**이고 token count는 결과 지표에 가깝다.

문서 구조의 깊이, section 수, list/table 수 같은 것은 이 Skill의 optimization metric이 아니다.

## 의미 보존 계약

최적화 전에 원문에서 다음을 **semantic anchors**로 취급한다.

- 사실과 주장
- actor / subject
- action / operation
- object / target
- 조건과 전제
- 예외와 fallback
- 부정
- 의무 강도와 가능성: `must`, `should`, `may`, 금지, 권고 등
- 범위와 경계
- 순서와 dependency
- 원인과 결과
- 관계와 cardinality
- 숫자, 단위, 날짜, 비율
- identifier, 이름, path, command, API, field, code token
- 입력, 출력, side effect와 failure behavior
- citation, attribution과 의미 있는 uncertainty

문서 구조와 formatting은 semantic optimization 대상이 아니지만 **변경 금지 invariant**다.

최적화 후 semantic anchors 중 하나라도 사라지거나 강도가 바뀌거나 다른 관계로 읽힐 수 있으면 실패다.

### 특히 위험한 손실

다음 변화는 짧아졌더라도 허용하지 않는다.

```text
must -> should
may -> will
not required -> optional
A only if B -> A when B
A before B -> A and B
all -> some
can fail -> fails
```

조건, modality, negation과 quantifier는 적은 단어로 큰 의미 차이를 만들기 때문에 token saving 대상으로 공격적으로 줄이면 안 된다.

## Semantic identity stability

사용자가 요구한 안정성은 번역에만 한정하지 않는다. 텍스트는 실제 사용 과정에서 여러 형태의 semantic transform을 거칠 수 있다.

- 다른 언어로 번역
- 같은 언어로 재생성 또는 paraphrase
- 요약
- prompt/context compression
- 다른 모델이나 agent의 재설명·재작성
- 긴 문맥에서 일부 추출 후 재사용

이 과정에서 원문의 표현이 모호하면 각 transform이 조금씩 다른 의미를 선택하면서 **semantic drift**가 누적될 수 있다.

따라서 `mols-text-optimizer`는 다음 조건을 가진다.

> **표현이 다시 생성되더라도 핵심 semantic anchors와 그 관계가 같은 의미로 재구성될 가능성을 높인다.**

이를 semantic identity stability로 부른다.

### 안정화 원칙

1. 한 개념에는 한 용어를 유지한다.
2. 더 짧은 다의어보다 의미 범위가 좁은 표현을 선택한다.
3. 대명사 선행사가 모호하면 명사를 유지한다.
4. 주체와 목적어를 과도하게 생략하지 않는다.
5. idiom, metaphor, 문화 의존 표현을 새로 도입하지 않는다.
6. technical term과 identifier는 synonym으로 바꾸지 않는다.
7. 문장 분리·결합으로 조건의 binding을 바꾸지 않는다.
8. 문법적 표지가 ambiguity를 줄이면 단지 짧다는 이유로 제거하지 않는다.
9. `이것`, `그 경우`, `앞의 것`처럼 재생성 과정에서 anchor를 잃기 쉬운 지시는 필요하면 실제 대상 명칭으로 유지한다.
10. 순서, 소유, 조건, 인과, 예외 같은 relation을 lexical shorthand로 뭉개지 않는다.
11. stylistic variation보다 재구성 안정성을 우선한다.

핵심은 사전상 synonym 수가 아니라 **현재 문맥과 후속 변환에서 가능한 의미 해석의 수를 줄이는 것**이다.

## Transform-resilience model

이 Skill이 보존하려는 것은 문자열 동일성이 아니다. 변환 전후에도 다음 semantic structure가 유지되는지가 핵심이다.

```text
entities / concepts
+ properties
+ actions
+ conditions
+ modality
+ negation
+ scope
+ ordering
+ causal / logical relations
+ exceptions
+ identifiers / quantities
```

다른 모델이 문장을 완전히 다르게 재생성하더라도 이 구조가 동일하면 semantic identity는 보존된 것으로 볼 수 있다.

반대로 단어 대부분이 같아도 relation이나 modality가 바뀌면 실패다.

### 예시

안정성이 낮은 표현:

```text
필요하면 이전처럼 처리한다.
```

`필요하면`, `이전`, `처리`가 무엇을 가리키는지 주변 context에 과도하게 의존한다. 일부 발췌, 요약, 번역 또는 재생성에서 의미가 쉽게 갈라진다.

안정성이 높은 표현:

```text
validation이 실패하면 기존 fallback policy를 적용한다.
```

조금 더 명시적이지만 action/condition relation이 고정되어 downstream transform에서 같은 의미로 복원되기 쉽다.

따라서 **최소 문자 수보다 최소 안정 의미 표현**을 우선한다.

## 추론 비용을 늘리지 않는 방법

이 Skill 자체가 텍스트를 줄이기 위해 더 큰 reasoning overhead를 만드는 것은 목적에 맞지 않는다.

기본 workflow는 **한 번의 변환 + 한 번의 bounded invariant scan**으로 제한한다.

```text
1. Preserve: semantic anchors 식별
2. Reduce: 명확하게 안전한 redundancy 제거
3. Stabilize: terminology, reference, relation과 ambiguity 정리
4. Check: omission / strength / relation 변화 확인
5. Stop: 추가 이득이 작거나 불확실하면 종료
```

기본적으로 다음은 하지 않는다.

- best-of-N candidate 생성
- 반복 semantic scoring
- token별 entropy 계산
- 상시 back-translation
- 반복 재생성 비교
- 여러 tokenizer 전수 비교
- 목표 compression ratio를 위한 강제 축약
- document structure 재설계

## Transform ordering

안전성과 효율성을 같이 얻으려면 큰 재작성보다 작은 wording 변환부터 적용한다.

```text
duplicate wording removal
→ redundant phrase removal
→ terminology normalization
→ reference / relation disambiguation
→ local sentence simplification
→ stop
```

문서 구조 변경은 이 순서에 포함하지 않는다.

## Proposed Skill workflow

```text
Input text
  ↓
Preserve semantic anchors
  ↓
Remove obvious linguistic redundancy
  ↓
Normalize semantic identity
  ↓
Reduce local wording where safe
  ↓
Bounded semantic check
  ↓
Return optimized text or unchanged input
```

## Initial package

```text
src/rulesync/.rulesync/skills/mols-text-optimizer/
└── SKILL.md
```

처음부터 reference, tokenizer utility 또는 별도 evaluator를 만들지 않는다. 실제 사용에서 조건부 detail을 분리할 loading benefit이 확인될 때만 추가한다.

## Proposed activation boundary

초기 description은 다음 intent를 선명하게 잡아야 한다.

- text/token 경량화
- wording compression
- 의미 보존 축약
- instruction/prose의 semantic-preserving shortening
- 표현 중복 제거
- semantic drift를 줄이는 wording stabilization

반대로 다음 요청만으로는 선택하지 않는다.

- Markdown 가독성 개선
- section/heading 구조 개선
- 문서 재구성
- 단순 요약
- 단순 번역
- 문체 윤문
- grammar correction만 필요한 경우

## Acceptance conditions

- 내용, 본질과 기능을 압축보다 우선한다.
- 의미 변화 가능성이 있으면 원문을 유지한다.
- 가독성, section, heading, list/table와 문서 구조를 직접 최적화하지 않는다.
- 기존 구조와 formatting을 변경하지 않는다.
- condition, exception, negation, modality, quantifier, scope, order와 relation을 보존한다.
- identifier, path, command, API, 수치와 단위를 보존한다.
- 같은 concept에 불필요한 synonym variation을 만들지 않는다.
- 번역뿐 아니라 재생성, 요약, 압축과 다른 모델의 재해석에서도 semantic identity가 흔들리기 어려운 wording을 선호한다.
- semantic stability를 위해 필요하면 더 짧은 다의어보다 명확한 표현을 유지한다.
- 별도 compression model이나 반복 검증을 기본 dependency로 요구하지 않는다.
- 목표 compression ratio를 맞추기 위해 의미를 희생하지 않는다.
- 최적화 이득이 불확실하면 추가 pass 없이 종료한다.
- `mols-markdown-for-human`, `humanize-korean`, summarization과 책임 경계가 명확하다.

## Adversarial review cases

1. `must`를 `should`로 바꾸면 짧아지는 instruction
2. 명시적 subject를 대명사로 줄이면 antecedent가 모호해지는 문장
3. 같은 concept을 다양한 synonym으로 표현한 텍스트
4. 긴 domain term을 더 짧지만 다의적인 일반어로 바꾸려는 경우
5. 조건절 삭제로 edge-case 의미가 달라지는 경우
6. quantifier가 축약 과정에서 사라지는 경우
7. `not required`를 `optional`로 바꾸며 의미가 변하는 경우
8. identifier를 abbreviation으로 바꾸려는 경우
9. section/format 변경으로 더 짧게 만들려는 경우
10. 이미 충분히 짧아 rewrite가 stylistic churn만 만드는 경우
11. 한국어 주어 생략으로 재생성 시 actor가 달라질 수 있는 경우
12. idiom 사용으로 다른 모델이 다른 의미를 선택할 수 있는 경우
13. technical term을 synonym으로 바꿔 domain identity가 흔들리는 경우
14. token 수는 줄지만 전보체가 되는 경우
15. 여러 candidate 비교가 있어야만 작은 절감이 가능한 경우
16. `이전처럼 처리한다` 같은 implicit reference가 다른 대상을 가리킬 수 있는 경우
17. 순서 relation이 paraphrase에서 병렬 관계로 바뀔 수 있는 경우
18. exception이 너무 암시적이라 요약에서 쉽게 사라지는 경우
19. 재생성마다 같은 concept이 서로 다른 label로 갈라질 가능성이 높은 경우
20. 가독성을 이유로 section/paragraph order를 바꾸려는 경우

## Implementation plan

1. 최소 package로 `SKILL.md`를 생성한다.
2. description에 semantic-preserving text/token reduction과 semantic identity stabilization trigger를 명확히 한다.
3. `Preserve → Reduce → Stabilize → Check → Stop`의 bounded workflow를 작성한다.
4. 가독성·section·heading·list/table·문서 구조·presentation을 명시적으로 scope 밖에 둔다.
5. semantic anchors와 금지 변환을 core contract에 포함한다.
6. 검증을 omission / strength / relation / identity drift에 한정한다.
7. `mols-agent-asset` 기준으로 trigger, responsibility, source authority와 always-loaded context를 self-review한다.
8. adversarial cases로 behavior를 검토하고 필요할 때만 수정한다.
9. generated route가 필요한 경우 repository-native 방식으로 동기화한다.
10. 최종 Review에서 별도 reference 또는 deterministic helper가 실제 benefit 없이 추가되지 않았는지 확인한다.

## Research references

- Microsoft Research, LLMLingua — prompt compression과 token reduction
- Microsoft Research, LongLLMLingua — long-context compression과 information preservation
- ASD-STE100 — controlled vocabulary, one word/one meaning, synonym reduction
- controlled natural language / machine translation 연구 — lexical·syntactic ambiguity와 translation consistency

외부 연구는 설계 근거일 뿐 Skill의 동작 authority가 아니다. 실제 Skill은 특정 compressor, tokenizer, 모델 또는 controlled-language 규격을 dependency로 삼지 않는다.

# `mols-text-optimizer` 조사 및 구현 계획

`mols-text-optimizer`를 **내용·본질·기능을 훼손하지 않으면서 텍스트와 토큰 비용을 줄이고, 번역과 재해석에서도 의미가 안정적으로 보존되도록 표현을 정리하는 Skill**로 만들 수 있는지 조사한 결과와 구현 계획을 정리한다.

이 문서는 현재 정본이 아닌 Research + Plan artifact다. 실제 Skill 구현 전 설계 기준과 검증 조건을 고정하는 것이 목적이다.

## 결론

신규 Skill로 만들 가치가 있다. 다만 목표를 단순한 "문장 축약"이나 "token compression"으로 정의하면 안 된다.

가장 적합한 책임은 다음과 같다.

> **같은 의미와 같은 동작을 유지하는 범위에서 불필요한 표현 비용을 제거하고, 모호성과 번역 손실 가능성을 늘리지 않는 가장 작은 텍스트 변환을 수행한다.**

최적화 우선순위는 반드시 다음 순서를 가진다.

```text
1. 의미·기능 보존
2. 모호성·번역 위험 비증가
3. 이해·추론 비용 비증가
4. 텍스트·토큰 비용 감소
```

4번을 위해 1~3번을 희생하지 않는다. 안전한 축약이 없으면 **변경하지 않는 것이 성공**이다.

이 순서는 기존 prompt compression 연구와도 맞는다. LLMLingua 계열은 prompt token 수를 크게 줄일 수 있음을 보여주지만 별도 압축 모델·알고리즘을 사용하고, 2026년 실사용 평가에서는 압축 전처리 비용이 충분히 긴 입력이나 적절한 환경이 아닐 때 end-to-end 이득을 상쇄할 수 있음이 확인됐다. 이 Skill의 기본 경로는 따라서 별도 compression pipeline이나 반복 추론을 요구하지 않아야 한다.

또한 ASD-STE100 Simplified Technical English와 controlled-language 연구는 **한 의미에 한 용어를 일관되게 쓰고, 다의어·복잡한 구조·불필요한 표현 변이를 줄이는 것**이 사람의 이해뿐 아니라 번역에도 유리하다는 근거를 제공한다. 따라서 "더 짧은 유의어"를 고르는 것이 아니라 **더 짧으면서 의미 범위가 좁고 안정적인 표현**을 고르는 방향이 적절하다.

## Skill responsibility

### 해야 하는 일

- 기존 텍스트에서 의미 없는 반복, 장황한 연결, 중복 수식과 불필요한 구조를 줄인다.
- 같은 개념에 여러 표현이 섞여 있으면 의미가 가장 명확한 하나로 통일한다.
- 동일 의미를 더 짧고 직접적으로 표현할 수 있으면 바꾼다.
- 주체, 조건, 예외, 부정, 의무 강도나 관계가 생략되어 모호해질 수 있으면 짧더라도 생략하지 않는다.
- 번역 시 다른 의미로 갈라질 가능성이 높은 다의적 표현보다 문맥상 의미가 좁고 안정적인 표현을 선호한다.
- 구조와 formatting이 기능을 가지면 그대로 보존한다.
- 안전한 최적화가 없으면 원문을 유지한다.

### 하지 않는 일

- 요약으로 정보량 자체를 줄이지 않는다.
- 사용자가 요구하지 않은 사실, 판단, 예시 또는 설명을 추가하지 않는다.
- tone, voice, 문체를 임의로 바꾸지 않는다.
- 사람이 읽기 어려운 전보체, token hack, 축약어 남발, punctuation packing을 사용하지 않는다.
- 특정 tokenizer에서만 토큰 수가 줄어드는 표현을 일반적인 최적화라고 간주하지 않는다.
- 별도 LLM compression model, entropy scorer 또는 반복 semantic-evaluation pipeline을 기본 dependency로 만들지 않는다.
- 번역을 직접 수행하는 Skill로 확장하지 않는다.

## 기존 Skill과의 경계

### `mols-markdown-for-human`

`mols-markdown-for-human`은 사람이 빠르게 읽고 탐색하도록 Markdown의 정보 구조와 표현을 개선한다. KISS/DRY에 따라 불필요한 복잡성을 줄이지만 핵심 목적은 **human-readable presentation**이다.

`mols-text-optimizer`의 핵심 목적은 presentation이 아니라 **semantic-preserving text cost reduction**이다.

따라서 다음처럼 구분하는 것이 좋다.

| 요청 | 주 owner |
| --- | --- |
| Markdown 구조, heading, list/table, 읽기 흐름 개선 | `mols-markdown-for-human` |
| 같은 의미를 유지하며 텍스트·토큰 비용 축소 | `mols-text-optimizer` |
| Agent Skill의 behavior를 보존하며 instruction을 경량화 | `mols-agent-asset` + `mols-text-optimizer` |
| 자연스러운 한국어 문체로 AI 티 제거 | `humanize-korean` |
| 내용을 줄여 핵심만 남기는 요약 | 별도 summarization 책임 |

새 Skill이 Markdown 구조나 Agent Asset authority까지 소유하면 기존 owner와 충돌하므로 피한다.

## "가벼운 텍스트"의 정의

토큰 수 하나만을 목표로 삼지 않는다. tokenizer마다 같은 문자열의 token count가 달라지고, 더 짧은 문자열이 더 적은 추론 비용을 항상 보장하지도 않는다.

기본적으로 다음 비용을 함께 본다.

- 중복된 의미 단위
- 불필요한 문장·절·수식
- 반복되는 같은 규칙이나 조건
- 의미 없는 transition 또는 template phrase
- 같은 개념을 표현하는 synonym churn
- 불필요하게 깊거나 반복되는 구조
- 문자/단어 길이
- target tokenizer가 명시되었을 때의 실제 token count

정확한 tokenizer가 주어지지 않은 상태에서는 **언어적 중복을 줄이는 것이 primary optimization**이고 token count는 결과 지표에 가깝다.

## 의미 보존 계약

최적화 전에 원문에서 다음을 **semantic anchors**로 취급해야 한다.

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
- formatting이 의미나 runtime behavior를 가지는 구조

최적화 후 이 anchors 중 하나라도 사라지거나 강도가 바뀌거나 다른 관계로 읽힐 수 있으면 실패다.

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

## 번역 안정성 원칙

사용자가 요구한 "번역되어도 훼손되지 않는 워딩"은 독립된 품질 조건으로 둘 가치가 있다.

ASD-STE100은 같은 의미에 하나의 표현을 일관되게 사용하고, 가능한 경우 한 단어에 한 의미를 부여하는 controlled-language 접근을 사용한다. 공식 설명에서도 synonym variation과 다의성을 줄이면 사람과 machine translation 모두에 번역이 쉬워진다고 설명한다.

이를 범용 텍스트 최적화에 그대로 규격화하지는 않되 다음 원칙은 흡수할 가치가 높다.

1. **한 개념에는 한 용어를 유지한다.** 표현 다양성보다 semantic identity를 우선한다.
2. **더 짧은 다의어보다 조금 길어도 의미가 좁은 표현을 선택한다.** 단, 실제로 길이가 줄고 의미도 더 안정적이면 우선한다.
3. **대명사 선행사가 모호하면 명사를 유지한다.** 대명사 치환을 token optimization으로 강제하지 않는다.
4. **주체와 목적어를 과도하게 생략하지 않는다.** 특히 instruction, policy, procedure에서는 explicit relation을 보존한다.
5. **idiom, metaphor, 문화 의존 표현을 새로 도입하지 않는다.** literal하고 domain-standard인 표현을 선호한다.
6. **technical term과 identifier는 synonym으로 바꾸지 않는다.** domain vocabulary의 안정성을 우선한다.
7. **문장 분리·결합으로 조건의 binding을 바꾸지 않는다.** 어느 조건이 어느 action에 걸리는지 명확해야 한다.
8. **문법적 표지를 단지 짧다는 이유로 제거하지 않는다.** 명시적 연결어가 ambiguity를 줄이는 경우 보존한다.

"유의어가 적은 표현" 자체를 절대 규칙으로 만들지는 않는다. 핵심은 사전상 synonym 수가 아니라 **현재 문맥에서 가능한 해석의 수를 줄이는 것**이다.

## 추론 비용을 늘리지 않는 방법

이 Skill 자체가 텍스트를 줄이기 위해 더 큰 reasoning overhead를 만드는 것은 목적에 맞지 않는다.

기본 workflow는 **한 번의 변환 + 한 번의 bounded invariant scan**으로 제한하는 것이 좋다.

```text
1. Preserve: semantic anchors와 기능적 구조를 짧게 식별
2. Reduce: 명확하게 안전한 redundancy만 제거
3. Stabilize: terminology와 ambiguity를 정리
4. Check: anchors의 omission / strength / relation 변화만 확인
5. Stop: 추가 이득이 작거나 불확실하면 종료
```

이 과정은 별도 장문의 분석 artifact를 만들지 않는다. 내부적으로 모든 문장을 재증명하거나 여러 candidate를 반복 생성하는 것도 기본값이 아니다.

### 금지할 기본 전략

- 여러 candidate를 생성하고 best-of-N 선택
- 원문과 결과를 별도 모델로 반복 semantic scoring
- token별 entropy 계산
- 번역 후 역번역을 항상 실행
- tokenizer 여러 개로 전수 비교
- 줄일 수 있는 부분이 없어도 목표 compression ratio를 맞추기 위한 재작성

이런 방법은 특정 고가치 작업에서 별도 검증으로 쓸 수는 있지만 Skill의 기본 workflow에는 넣지 않는다.

### 비용 절감 자체를 지키는 stop condition

다음 중 하나면 즉시 보수적으로 종료한다.

- 의미 보존 여부가 확실하지 않다.
- 더 짧은 표현이 더 ambiguous하다.
- 기능적 formatting이나 structure를 건드려야 한다.
- 남은 변경은 stylistic preference 수준이다.
- 추가 최적화의 예상 절감량보다 검증 비용이 크다.

## Token optimization에 대한 제한

Prompt compression 연구는 많은 redundancy가 존재하고 높은 compression ratio가 가능한 사례를 보여준다. 그러나 `mols-text-optimizer`는 LLMLingua 같은 prompt compressor를 복제하면 안 된다.

이유는 다음과 같다.

- prompt compression은 target model과 task performance를 기준으로 최적화될 수 있다.
- token 삭제 중심 결과는 사람이나 번역기에 자연스러운 문장일 필요가 없다.
- 압축을 위한 별도 inference가 총 비용을 늘릴 수 있다.
- 이 repository의 Skill은 여러 runtime에 재사용되므로 특정 tokenizer/model에 결합하면 portability가 떨어진다.

따라서 이 Skill은 **linguistic and structural optimization**을 기본으로 하고, 정확한 token budget이나 tokenizer가 사용자/target에서 명시된 경우에만 실제 token count를 보조 신호로 사용할 것을 권장한다.

## Transform ordering

안전성과 효율성을 같이 얻으려면 큰 재작성보다 작은 변환부터 적용한다.

권장 순서는 다음과 같다.

1. exact duplication 제거
2. 같은 규칙·조건의 반복 projection 제거 또는 참조화
3. 의미 없는 filler / transition 제거
4. 장황한 phrase를 직접적인 equivalent로 교체
5. 같은 개념의 terminology 통일
6. 불필요한 syntactic nesting 완화
7. 문장 결합 또는 분리
8. lexical shortening

아래로 갈수록 semantic drift 위험이 커지므로 앞 단계에서 충분히 줄었다면 뒤 단계는 생략한다.

특히 lexical shortening은 마지막에 둔다. 짧은 단어가 더 다의적이거나 번역 불안정한 경우가 있기 때문이다.

## 보존 우선 변환 예시

### 안전한 방향

```text
변경 전:
In order to determine whether the file exists, you should first check the path.

변경 후:
Check the path first to determine whether the file exists.
```

의미와 순서가 유지되고 filler가 제거된다.

### 위험한 방향

```text
변경 전:
If validation fails, do not deploy the artifact.

잘못된 축약:
Deploy only validated artifacts.
```

문맥에 따라 가까워 보이지만 원문은 validation failure와 deploy prohibition의 관계를 직접 규정한다. 새 문장은 "validated"의 정의나 validation이 수행되지 않은 상태를 다르게 해석할 여지가 있다. 이런 경우 짧음보다 원문의 explicit condition을 유지한다.

### terminology stability

```text
변경 전:
repository / repo / codebase

권장:
문맥상 정본 용어 하나를 선택하고 계속 사용
```

표현 다양성을 줄이면 repetition처럼 보일 수 있지만 machine interpretation과 translation에서는 오히려 안정적이다.

## 기능 보존이 필요한 텍스트

일반 prose뿐 아니라 다음은 단순 문장으로 취급하지 않는다.

- Agent instructions와 Skills
- prompt template
- config 설명
- command examples
- Markdown links와 anchors
- YAML/JSON/XML-like blocks
- API field descriptions
- policy / requirement 문장
- procedure step
- test expectation

이 surface에서는 특정 word, order, heading, delimiter 또는 identifier가 runtime이나 downstream consumer의 동작을 바꿀 수 있다.

따라서 `mols-text-optimizer`는 **텍스트처럼 보여도 기능을 가진 token은 그대로 보존**해야 한다. Agent Asset을 최적화할 때는 해당 Asset owner가 behavior와 authority를 계속 소유하고, 이 Skill은 wording cost만 줄인다.

## 실패 방지 장치

### 1. Preserve-first contract

원문에서 중요한 semantic anchors를 먼저 식별한다. 줄일 대상부터 찾지 않는다.

### 2. Minimal-delta rule

전체를 새로 쓰지 않고 명확한 비용을 만드는 부분만 바꾼다. 작은 diff는 semantic regression surface도 줄인다.

### 3. No-op is valid

안전한 절감이 없으면 그대로 둔다. compression ratio를 acceptance condition으로 두지 않는다.

### 4. Ambiguity non-regression

결과의 가능한 해석이 원문보다 늘어나면 실패로 본다.

### 5. Semantic strength check

modality, negation, quantifier, condition, exception의 강도가 바뀌지 않았는지 확인한다.

### 6. Functional anchor check

identifier, code token, path, command, number, unit, link target, delimiter와 구조를 확인한다.

### 7. Translation-stability check

새 표현이 synonym churn, polysemy, implicit subject/object, ambiguous pronoun 또는 idiom을 늘리지 않았는지 확인한다.

이 검증은 별도 heavyweight evaluator가 아니라 짧은 invariant checklist로 수행한다.

## 초기 Skill package 권장안

처음부터 reference와 tooling을 많이 만들지 않는다.

```text
src/rulesync/.rulesync/skills/mols-text-optimizer/
└── SKILL.md
```

핵심 계약, workflow와 stop condition을 `SKILL.md` 하나에 충분히 짧게 담는 것을 우선한다.

다음 중 하나가 실제 구현 Review에서 확인될 때만 supporting reference를 추가한다.

- preservation edge case가 많아 core Skill을 과도하게 길게 만드는 경우
- 번역 안정성 규칙이 일반 optimization 흐름보다 훨씬 상세해지는 경우
- 반복 eval case를 deployable guidance와 분리할 필요가 있는 경우

Skill 자체도 text optimization 대상이므로 **항상 로드되는 instruction을 늘려 동작 비용을 높이지 않는 설계**가 특히 중요하다.

## Description / trigger 방향

최종 description은 다음 intent를 분명히 잡아야 한다.

- shorten / compact / reduce tokens / reduce text size
- preserve meaning / behavior / function
- remove redundancy without summarizing
- make wording more translation-stable or less ambiguous while staying compact

반대로 다음 요청에는 단독으로 선택되지 않게 한다.

- 단순 summary
- tone rewrite
- 자연스러운 문체 개선
- spelling/grammar only
- translation itself
- Markdown information architecture
- Agent Asset behavior redesign

## 구현 계획

### Phase 1 — Core contract 작성

`SKILL.md`에 다음만 먼저 넣는다.

- responsibility와 trigger boundary
- preservation-first priority
- semantic anchors
- lightweight workflow
- translation-stability heuristics
- minimal-delta / no-op rule
- stop conditions
- neighboring Skill boundary

### Phase 2 — Adversarial examples로 압축

초안을 다음 failure family로 challenge한다.

1. negation 삭제
2. `must` / `should` / `may` 강도 변화
3. condition과 action binding 변화
4. exception 삭제
5. quantifier 변화
6. actor/object 생략
7. sequence/dependency 변화
8. identifier 또는 숫자 변경
9. 같은 개념의 synonym churn
10. shorter but polysemous wording 선택
11. ambiguous pronoun 도입
12. Markdown/command/config 기능 손상
13. summary처럼 정보를 삭제
14. 목표 ratio를 맞추기 위한 과도한 축약
15. 압축 검증 자체가 반복 reasoning loop가 되는 경우

문제가 발견되면 규칙을 추가하기보다 기존 contract를 더 직접적으로 표현하는 것을 우선한다.

### Phase 3 — Package 크기 Review

- `SKILL.md`가 항상 필요한 판단만 포함하는지 확인한다.
- conditional detail이 실제로 길어졌을 때만 reference로 분리한다.
- 별도 script, tokenizer dependency 또는 semantic evaluator를 추가하지 않는다.
- target-specific token counting이 실제 반복 요구로 확인될 때만 deterministic helper를 검토한다.

### Phase 4 — Repository integration

구현 시 canonical source는 repository policy에 따라 다음 위치를 사용한다.

```text
src/rulesync/.rulesync/skills/mols-text-optimizer/
```

생성 route나 target projection을 직접 작성 원본으로 편집하지 않는다. 필요한 repository-native generation/validation을 실행한 뒤 결과를 확인한다.

## Acceptance conditions

초기 구현은 최소한 다음을 만족해야 한다.

- 내용, 본질, 기능의 삭제·변형을 명시적으로 금지한다.
- 의미 보존이 token reduction보다 우선한다.
- unsafe compression에서 no-op할 수 있다.
- summarization과 책임이 분리되어 있다.
- modality, negation, condition, exception, quantifier, actor, relation을 보존한다.
- identifier, number, code, path, command와 기능적 structure를 보존한다.
- 같은 개념에는 일관된 용어를 쓰도록 유도한다.
- 더 짧더라도 다의성 또는 번역 위험이 커지는 표현을 거부한다.
- idiom, ambiguous pronoun와 synonym churn을 새로 만들지 않는다.
- 특정 tokenizer/model에 기본 결합하지 않는다.
- 별도 compression inference나 반복 evaluation을 기본 요구하지 않는다.
- 기본 workflow가 한 번의 bounded transformation과 짧은 invariant check로 끝난다.
- hard compression ratio를 두지 않는다.
- `mols-markdown-for-human`, `humanize-korean`, `mols-agent-asset`, summarization과 boundary가 선명하다.
- Skill package 자체가 불필요하게 커지지 않는다.

## 설계상 보류할 것

다음은 현재 단계에서는 넣지 않는 것이 좋다.

- `aggressive`, `balanced`, `safe` 같은 mode enum
- universal token budget
- tokenizer 목록
- 자동 back-translation
- semantic similarity threshold
- BERTScore/COMET 같은 metric dependency
- 여러 LLM candidate 비교
- 언어별 controlled vocabulary
- ASD-STE100 규칙의 복제

실제 사용에서 반복되는 필요가 확인되면 각각 별도 Research로 승격한다.

## 주요 외부 근거

- Huiqiang Jiang et al., **LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models** (2023): prompt redundancy를 제거해 큰 token reduction이 가능하지만 별도 compression mechanism을 사용한다. https://arxiv.org/abs/2310.05736
- Zhuoshi Pan et al., **LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression** (2024): faithful compression을 별도 학습 objective와 encoder model로 다룬다. https://arxiv.org/abs/2403.12968
- Cornelius Kummer et al., **Prompt Compression in the Wild: Measuring Latency, Rate Adherence, and Quality for Faster LLM Inference** (2026): compression overhead와 end-to-end latency의 break-even이 중요하며 항상 이득이 나지 않음을 대규모 실험으로 보인다. https://arxiv.org/abs/2604.02985
- ASD-STE100 Simplified Technical English, official FAQ / Issue 9: one word–one meaning, synonym control과 명확한 sentence construction이 이해와 번역을 쉽게 한다고 설명한다. https://www.asd-ste100.org/STE_faq.html
- Marcus Sammer et al., **Ambiguity Reduction for Machine Translation: Human-Computer Collaboration** (AMTA 2006): lexical ambiguity reduction이 cross-domain machine translation adequacy를 개선할 수 있음을 보인다. https://aclanthology.org/2006.amta-papers.22/
- Sanja Štajner and Maja Popović, **Can Text Simplification Help Machine Translation?** (EAMT 2016): lexical/syntactic simplification과 ambiguity reduction이 machine translation 전처리로 가질 수 있는 효과와 한계를 다룬다. https://aclanthology.org/W16-3411/
- Sanja Štajner and Maja Popović, **Automated Text Simplification as a Preprocessing Step for Machine Translation into an Under-resourced Language** (RANLP 2019): source simplification이 translation fluency에 도움이 될 수 있지만 meaning preservation과 grammaticality filtering이 중요함을 보여준다. https://aclanthology.org/R19-1131/

## 다음 작업

다음 단계에서는 이 계획을 바탕으로 `mols-text-optimizer/SKILL.md` 초안을 만들고, 위 adversarial case로 Review한 뒤 **규칙을 늘리기보다 더 짧고 강한 contract로 수렴하는 방향**으로 개선하는 것이 좋다.

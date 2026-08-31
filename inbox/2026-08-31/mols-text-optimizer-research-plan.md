# `mols-text-optimizer` 조사 보고서

> 이 문서는 `mols-text-optimizer` 설계를 위한 Research artifact다. 구현 순서와 acceptance의 정본은 [`mols-text-optimizer-plan.md`](mols-text-optimizer-plan.md)다.

## 결론

`mols-text-optimizer`는 **구조를 건드리지 않고, 의미와 기능을 보존하면서 기존 텍스트의 불필요한 wording 비용만 줄이는 범용 fallback Skill**로 설계하는 것이 가장 적절하다.

우선순위는 다음과 같다.

```text
1. 의미 보존
2. 기능·행동 보존
3. semantic identity 안정성 비저하
4. 모호성·변환 손실 위험 비증가
5. 추가 추론 비용 최소화
6. wording·token 비용 감소
```

6번을 위해 1~5번을 희생하지 않는다. 안전한 절감이 없으면 no-op가 성공이다.

이 Skill은 readability, section 구성, heading 설계, 문서 구조, formatting을 최적화하지 않는다. 특히 structure와 formatting은 단순 out-of-scope이 아니라 **protected surface**로 취급한다.

또한 범용 Skill이므로 대상이나 작업에 더 구체적으로 적용되는 Skill, scoped instruction, document/domain guidance, framework contract 또는 procedure가 있으면 그것을 우선하고 이 Skill은 선택하지 않는다. Routing과 trigger는 Skill body가 아니라 frontmatter `description`이 소유한다.

Repository 언어 정책과 사람을 위한 Markdown 원칙을 구현 표면에 적용한다. Trigger frontmatter `description`은 영어를 유지하고, Skill body의 일반 서술은 한국어를 기본으로 하며 번역하면 어색하거나 의미가 흐려지는 기술 용어·고유 명칭만 영어를 보조로 사용한다. 문단과 목록은 의미 단위로 구성하고 임의의 line-width wrapping은 하지 않는다.

## Responsibility

> **더 구체적인 적용 owner가 없는 텍스트에서 material meaning과 기능을 유지하는 범위로 불필요한 wording 비용을 제거한다.**

Semantic stability는 별도 기능이 아니라 optimization constraint다. 더 짧아진 결과가 더 모호하거나 후속 변환에서 의미가 갈라지기 쉬워지면 해당 축약을 하지 않는다.

## Scope

### In scope

- 의미 없는 반복과 불필요한 wording 제거
- 의미 범위가 같은 더 짧고 직접적인 표현 선택
- 같은 concept의 불필요한 term variation 정리
- ambiguous reference나 다의적 표현이 축약 과정에서 더 위험해지는 것을 방지
- condition, exception, negation, modality, scope, relation을 유지하는 local wording reduction
- translation, regeneration, summarization, compression, model handoff 같은 후속 변환에서 불필요한 semantic drift가 늘지 않도록 표현을 선택
- 안전한 절감이 없을 때 no-op

### Out of scope

- readability 자체
- section 구성·재배치
- heading 설계·rename
- list/table/callout 변환
- Markdown 구조와 information architecture
- paragraph split/merge/reordering
- visual presentation과 navigation
- formatting optimization
- information-reducing summarization
- tone, voice, style
- translation 자체
- format conversion 자체
- latent/context representation compressor
- target/domain-specific authoring rule

## Protected structure

다음은 optimizer의 변경 대상이 아니다.

- section과 heading hierarchy
- sentence/paragraph boundary와 순서
- list/table/callout representation
- numbering
- code fence, delimiter, indentation
- JSON/YAML/XML/schema-like structure
- exact output/format contract

Prompt format 연구에서는 의미가 같아도 formatting 변화만으로 model behavior가 달라질 수 있다. 따라서 structure protection은 단순 owner separation뿐 아니라 behavioral safety이기도 하다.

## Semantic identity

이 Skill에서 semantic identity는 다음 anchor와 관계를 함께 보존하는 것으로 본다.

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

Instruction, policy, prompt, specification처럼 agent-facing text에서는 semantic identity와 behavioral identity를 구분한다.

Behavioral identity에는 다음도 포함한다.

- activation condition
- actor/action
- MUST/SHOULD/MAY, prohibition, permission strength
- sequence
- exception/fallback
- permission/safety/scope boundary
- input/output/side-effect/failure behavior
- exact identifier, command, path, schema token

**Semantic preservation claim과 behavioral preservation claim을 같은 것으로 취급하지 않는다.**

## Semantic anchors

Compression-resistant하게 다룰 최소 anchor는 다음과 같다.

- fact / claim
- actor / subject
- action / operation
- object / target
- condition / precondition
- trigger
- exception / fallback
- negation
- modality / deontic force
- permission / prohibition
- scope / boundary
- order / dependency
- cause / result
- relation / cardinality
- quantifier / comparator
- uncertainty / epistemic strength
- number / unit / date / ratio / threshold
- identifier / name / path / command / API / field / code token
- input / output / side effect / failure behavior
- citation / attribution / provenance when meaningful
- structure / formatting as a protected invariant

## High-risk semantic drift

다음과 같은 변환은 token이 줄더라도 승인하지 않는다.

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

## Stable wording

목표는 minimum characters가 아니라 **minimum stable meaning wording**이다.

- 하나의 concept에는 하나의 preferred term을 사용한다.
- 더 짧더라도 다의적인 단어보다 의미 범위가 좁고 안정적인 표현을 선호한다.
- 대명사나 생략 때문에 reference가 흔들릴 수 있으면 명시적 noun/reference를 유지한다.
- idiom, metaphor, culturally specific shorthand를 새로 도입하지 않는다.
- domain term과 identifier를 synonym으로 바꾸지 않는다.
- condition binding, order, exception relation을 명시적으로 유지한다.

Translation은 전체 목표가 아니라 semantic stability를 확인하는 stress case 중 하나다.

## Bidirectional preservation intuition

Runtime NLI model을 요구하지는 않지만 개념적으로는 양방향 information coverage를 생각한다.

- optimized text가 original의 일부만 표현하면 summary/omission 위험이 있다.
- optimized text가 original보다 강한 implication을 추가하면 semantic mutation이다.
- source와 충돌하지 않는다는 사실만으로 preservation이 증명되지는 않는다.

## Compression safety ladder

낮은 위험부터 적용한다.

```text
1. exact duplicate 제거
2. semantic duplicate wording 제거
3. 의미 없는 framing/filler 제거
4. 같은 concept의 term 통일
5. 장황하지만 의미가 동일한 local phrase 단축
6. 더 이상 명확한 안전 이득이 없으면 stop
```

낮은 위험:

- exact semantic repetition
- 의미 없는 opening/closing filler
- synonym churn
- 의미를 갖지 않는 template phrase

높은 위험:

- condition binding을 바꾸는 function word 삭제
- modality compression
- negation rewrite
- quantifier 삭제
- uncertainty 삭제
- actor/object 생략
- exception 암시화
- clause merge
- pronoun/ellipsis reduction
- structure/formatting 변경

## Runtime cost constraint

기본 workflow는 다음처럼 bounded해야 한다.

```text
Preserve → Reduce → Check → Stop
```

한 번의 transform과 한 번의 invariant scan을 기본으로 한다.

Runtime check는 변경한 span과 판단에 필요한 주변 context에 한정한다.

- 빠진 사실이나 규칙이 있는가?
- actor/action/target이 바뀌었는가?
- condition 또는 exception binding이 바뀌었는가?
- modality/negation/quantifier/uncertainty가 바뀌었는가?
- scope/order/causal relation이 바뀌었는가?
- identifier/quantity/unit이 바뀌었는가?
- agent-facing text라면 activation/permission/behavior가 달라질 수 있는가?
- protected structure를 건드렸는가?

불확실하면 transformation을 되돌리거나 원문을 유지한다.

기본 runtime에서 다음을 요구하지 않는다.

- best-of-N
- multiple LLM judges
- repeated semantic scoring
- embedding similarity threshold
- token-level entropy
- always-on translation/back-translation
- repeated regeneration tests
- 여러 tokenizer 비교
- target compression ratio를 맞출 때까지 반복

이유는 간단하다.

1. optimizer 자체의 inference cost를 키운다.
2. evaluator 자체도 semantic edge case에서 brittle할 수 있다.
3. 작은 wording 절감을 위해 generation chain을 늘리는 것은 비용 대비 이득이 낮다.

Development-time eval은 runtime보다 강하게 둘 수 있지만 별도 책임이다.

## Stop conditions

다음 중 하나면 멈춘다.

- semantic preservation이 확실하지 않다.
- behavioral effect가 바뀔 수 있다.
- 더 짧은 wording이 ambiguity를 키운다.
- 추가 절감을 위해 modality, condition, relation을 압축해야 한다.
- structure/formatting을 바꿔야 한다.
- 남은 차이가 style preference뿐이다.
- 절감량이 검토 비용보다 작다.
- 목표 ratio를 맞추려면 information loss가 필요하다.
- 이미 충분히 짧아 rewrite가 churn만 만든다.

## Initial package

최초 package는 한 파일로 시작한다.

```text
src/rulesync/.rulesync/skills/mols-text-optimizer/
└── SKILL.md
```

처음부터 reference, tokenizer utility, evaluator, script를 만들지 않는다.

Supporting resource는 다음 조건이 실제로 생길 때만 분리한다.

- core Skill의 always-loaded context cost가 의미 있게 커진다.
- 특정 상황에서만 필요한 detail이 반복해서 필요하다.
- 분리했을 때 책임을 복제하지 않고 실제 loading benefit이 생긴다.

## Activation boundary

이 Skill은 generic fallback이다. 현재 target/task에 더 구체적으로 적용되는 전문 Skill, scoped instruction, document/domain guidance, framework contract 또는 procedure가 있으면 그것을 사용하고 이 Skill은 선택하지 않는다.

더 구체적인 owner가 없을 때 다음 intent에 선택할 수 있다.

- 제공된 text를 의미 보존 조건에서 경량화
- wording compression
- semantic-preserving shortening
- lexical redundancy 제거
- content/function을 보존한 expression-cost optimization

다음 이유만으로는 선택하지 않는다.

- Markdown readability 개선
- section/heading restructuring
- document restructuring
- summarization
- translation
- style polish
- grammar correction only
- caveman-style response
- latent prompt/context compressor

## Acceptance conditions

- content, essence, meaning, function이 reduction보다 우선한다.
- semantic similarity와 behavioral identity를 같은 것으로 보지 않는다.
- semantic/behavioral risk가 있으면 no-op한다.
- readability, section, heading, list, table, document-structure optimization을 소유하지 않는다.
- structure/formatting을 protected surface로 보존한다.
- actor/action/target을 보존한다.
- condition/trigger/exception/fallback binding을 보존한다.
- negation/modality/quantifier/uncertainty/scope/order/relation을 보존한다.
- identifier/path/command/API/number/threshold/unit을 보존한다.
- synonym churn을 만들지 않는다.
- 더 짧은 다의어보다 의미가 좁고 안정적인 wording을 선호한다.
- translation/regeneration/summarization/compression/model handoff에서 avoidable semantic drift를 늘리지 않는다.
- agent-facing text의 activation/permission/safety/downstream behavior를 보존한다.
- 별도 compressor나 반복 validator를 기본 dependency로 두지 않는다.
- embedding/BERTScore/back-translation을 universal oracle로 두지 않는다.
- forced compression ratio를 두지 않는다.
- 불확실하면 일찍 멈춘다.
- `mols-markdown-for-human`, `caveman-ko`, `text-humanize-korean`, summarization과 책임 경계가 분명하다.

## Adversarial review cases

1. `must`를 `should`로 바꾸면 더 짧아지는 instruction
2. `must not`을 약한 prohibition으로 바꾸는 경우
3. 명시적 subject를 대명사로 줄여 antecedent가 모호해지는 경우
4. 같은 concept을 여러 synonym으로 표현한 text
5. 긴 domain term을 짧지만 다의적인 일반어로 바꾸려는 경우
6. condition clause 삭제로 edge-case behavior가 달라지는 경우
7. quantifier가 축약 과정에서 사라지는 경우
8. `not required`를 `optional`로 바꾸며 permission semantics가 달라지는 경우
9. uncertainty marker를 filler로 오인해 삭제하는 경우
10. identifier를 abbreviation으로 바꾸는 경우
11. section/format을 바꿔 더 짧게 만들려는 경우
12. 이미 충분히 짧아 rewrite가 stylistic churn만 만드는 경우
13. 한국어 주어 생략으로 actor가 달라질 수 있는 경우
14. idiom 사용으로 다른 model이 다른 meaning을 선택할 수 있는 경우
15. technical term을 synonym으로 바꾸는 경우
16. token은 줄지만 telegraphic fragment가 되는 경우
17. 여러 candidate 비교가 있어야만 작은 절감이 가능한 경우
18. implicit reference가 다른 대상을 가리킬 수 있는 경우
19. order relation이 parallel relation으로 바뀌는 경우
20. exception이 암시적으로 바뀌어 쉽게 사라지는 경우
21. regeneration마다 같은 concept이 서로 다른 label로 갈라지는 경우
22. readability를 이유로 section/paragraph order를 바꾸는 경우
23. `all`이 `some`으로 바뀌는 경우
24. `at least`, `at most`, `exactly`가 삭제되는 경우
25. 원문보다 stronger claim을 "명확화"로 추가하는 경우
26. 원문의 일부만 남겨 사실상 summary가 되는 경우
27. Agent Skill trigger를 줄여 activation boundary가 넓어지는 경우
28. safety/permission constraint를 duplicate로 보고 삭제하는 경우
29. prompt format을 줄이려고 delimiter/list를 바꾸는 경우
30. 높은 BERTScore만으로 modality drift를 승인하는 경우
31. back-translation similarity만으로 information loss를 승인하는 경우
32. tokenizer가 지정되지 않았는데 특정 tokenizer 결과를 일반화하는 경우
33. compression validation overhead가 절감량보다 큰 경우
34. caveman-style fragment를 generic optimization 결과로 쓰는 경우
35. 대상에 적용되는 전문 Skill이나 문서 guidance가 있는데 generic optimizer가 가로채는 경우

## Research evidence and implications

| Source | Evidence | Design implication |
| --- | --- | --- |
| ASD-STE100 Simplified Technical English, Issue 9 / FAQ | controlled vocabulary, 가능한 경우 one word–one meaning, synonym variation 제한, ambiguity 감소 | 같은 concept에 안정적인 preferred term을 쓰고 polysemy를 줄인다 |
| Agrawal & Carpuat, TACL 2024, *Do Text Simplification Systems Preserve Meaning?* | simplification이 의미 보존을 자동으로 보장하지 않으며 best supervised system도 comprehension information을 놓침 | shortening 자체를 success로 간주하지 않는다 |
| Shi et al., `*SEM 2024`, *Paraphrase Identification via Textual Inference* | semantic equivalence와 asymmetric entailment의 관계를 formalize | preservation을 양방향 information coverage intuition으로 본다 |
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
- Ning Shi, Bradley Hauer, Jai Riley, Grzegorz Kondrak. *Paraphrase Identification via Textual Inference*. `*SEM 2024` — https://aclanthology.org/2024.starsem-1.11/
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

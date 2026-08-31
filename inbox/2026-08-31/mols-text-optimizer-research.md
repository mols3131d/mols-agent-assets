# `mols-text-optimizer` 조사

이 문서는 `mols-text-optimizer` 설계에 사용한 Research evidence와 그 설계 함의만 기록한다. 구현 순서와 acceptance의 정본은 [`mols-text-optimizer-plan.md`](mols-text-optimizer-plan.md)다.

## Conclusion

`mols-text-optimizer`는 **더 구체적인 owner가 없는 텍스트에서 의미와 기능을 보존하면서 불필요한 표현 비용을 줄이는 범용 fallback Skill**로 두는 것이 적절하다.

의미 안정성은 독립 기능이 아니라 축약의 제약이다. 더 짧아진 결과가 더 모호하거나 후속 변환에서 의미가 갈라지기 쉬워진다면 그 변경을 하지 않는다. 안전한 절감이 없을 때 원문을 유지하는 것도 성공이다.

우선순위는 다음과 같다.

```text
1. 의미 보존
2. 기능·행동 보존
3. 정확한 기술 정보와 관계 보존
4. 구조 비변경
5. 모호성·semantic drift 위험 비증가
6. 추가 추론 비용 최소화
7. 표현 비용 감소
```

7번을 위해 앞의 조건을 희생하지 않는다.

## Findings

### Semantic similarity alone is insufficient

Instruction, policy, prompt처럼 downstream behavior를 제어하는 텍스트는 표면적으로 비슷한 의미를 유지해도 행동 효과가 달라질 수 있다. 따라서 일반 의미 보존과 behavioral identity를 구분해야 한다.

보존 대상에는 주체, 행동, 대상, 조건, 예외, 부정, 요구 강도, 허용·금지, 수량자, 불확실성, 범위, 순서와 인과·논리 관계가 포함된다.

### Shortening is not proof of preservation

Text simplification과 compression 연구에서는 더 짧거나 읽기 쉬운 결과가 원문의 정보를 모두 보존한다고 보장되지 않는다. 축약률 자체를 성공 기준으로 두면 안 된다.

특히 `must → should`, `all → some`, `at least 3 → 3`, `can fail → fails`처럼 작은 표현 차이가 요구 강도나 사실 범위를 바꿀 수 있다.

### Stable terminology reduces drift risk

같은 개념에는 같은 용어를 유지하고, 표준 도메인 용어나 사용자가 정한 canonical term을 더 짧은 일반어로 바꾸지 않는 편이 안전하다. 짧더라도 다의성이 커지는 표현은 후속 번역·재생성·요약·handoff에서 의미 분기를 늘릴 수 있다.

이 원칙은 text optimizer가 독립적인 semantic normalizer가 되어야 한다는 뜻이 아니다. **축약 과정에서 모호성이나 term variation을 새로 늘리지 않는 것**이 책임이다.

### Structure is a protected surface

Prompt format 연구는 의미와 무관해 보이는 formatting 변화도 model behavior에 영향을 줄 수 있음을 보여준다. 또한 이 Skill의 책임 자체가 wording reduction이므로 section, heading, paragraph, list/table, delimiter와 format contract는 최적화 대상이 아니다.

구조나 가독성 개선은 해당 전문 owner가 담당한다.

### Token count is target-dependent

같은 문자열도 tokenizer에 따라 token count가 달라진다. 별도 tokenizer가 없을 때는 언어적 redundancy와 표현 비용 감소를 기본 signal로 사용하고 정확한 token 절감률을 주장하지 않는 것이 적절하다.

실제 token count를 최적화해야 한다면 명시된 target tokenizer로 측정할 수 있어야 한다.

### Validation should remain bounded

Embedding similarity, back-translation, best-of-N, 반복 LLM judge는 참고 evidence가 될 수 있지만 universal preservation oracle은 아니다. 작은 표현 절감을 위해 상시 다중 generation/evaluation chain을 실행하면 Skill 자체의 비용이 목적과 충돌한다.

기본 runtime은 **한 번의 국소 축약과 한 번의 변경 구간 검토**로 제한하고, 불확실하면 해당 변경을 되돌리거나 원문을 유지하는 편이 적절하다.

### Generic fallback must not absorb specialist ownership

이 Skill은 범용 표현 최적화만 소유한다. 대상이나 작업에 더 구체적인 Skill, scoped instruction, document/domain guidance, framework contract 또는 procedure가 적용되면 그 owner를 우선해야 한다.

이 경계는 외부 연구보다 repository의 Agent Asset ownership 원칙에서 나온다. 범용 Skill이 전문 authoring, fidelity, Markdown, humanization이나 다른 domain responsibility를 흡수하면 trigger precision과 authority가 함께 나빠진다.

## Design Implications

- safe reduction이 없으면 no-op한다.
- 의미와 behavioral identity를 분리해 보호한다.
- 조건, 예외, 부정, 요구 강도, 수량자, 불확실성, 범위와 순서를 compression-resistant하게 취급한다.
- identifier, path, command, API, 수치, 단위와 literal token을 임의로 바꾸지 않는다.
- canonical term을 불필요한 synonym이나 새 abbreviation으로 바꾸지 않는다.
- explicit reference를 모호한 pronoun이나 생략으로 바꾸지 않는다.
- structure와 formatting은 protected surface로 둔다.
- tokenizer를 실제로 사용하지 않았다면 정확한 token 절감량을 주장하지 않는다.
- 별도 compressor model, embedding gate, back-translation, best-of-N과 반복 judge를 기본 dependency로 두지 않는다.
- specific owner가 적용되는 경우 generic optimizer가 대신 실행되지 않도록 routing boundary를 둔다.

## Evidence

| Source | 관찰 | 설계 함의 |
| --- | --- | --- |
| ASD-STE100 Simplified Technical English | controlled vocabulary, synonym variation과 ambiguity 제한 | 같은 개념에 안정적인 preferred term을 유지한다 |
| Agrawal & Carpuat, TACL 2024 | text simplification이 의미 보존을 자동 보장하지 않음 | shortening 자체를 성공으로 간주하지 않는다 |
| Shi et al., *SEM 2024 | paraphrase equivalence와 one-way inference를 구분 | preservation을 단순 surface similarity로 보지 않는다 |
| Acharjee et al., IJCNLP-AACL 2025 | multi-hop rewriting에서 semantic drift를 관찰 | 후속 변환에서 의미 분기를 늘리지 않는 표현을 선호한다 |
| Fu & Barez, EMNLP 2025 | semantically equivalent prompt paraphrase에서도 behavior 차이가 발생 가능 | agent-facing text는 behavioral identity를 별도로 보호한다 |
| Ngweta et al., NAACL 2025 | prompt format 변화만으로도 성능 변동이 발생 | structure와 formatting을 보호한다 |
| Nguyen & Lin, PMLR 2026 | semantic reconstruction fidelity와 refusal behavior가 일치하지 않을 수 있음 | semantic claim과 behavioral claim을 구분한다 |
| Mahajan et al., EMNLP Findings 2024 | sentence embedding 하나가 모든 semantic distinction을 포괄하지 못함 | embedding score를 universal gate로 두지 않는다 |
| Mujahid et al., ACL 2026 | factuality metric이 meaning-preserving perturbation에 불안정할 수 있음 | 자동 metric 하나에 preservation 판정을 위임하지 않는다 |
| Veizaga et al., Empirical Software Engineering 2021 | requirement를 scope/precondition/actor/response 등 정보 역할로 모델링 | 단어보다 semantic role과 relation을 보존한다 |
| RFC 2119 / RFC 8174 | MUST/SHOULD/MAY requirement level 구분 | modality와 normative strength를 보존한다 |
| LLMLingua / LongLLMLingua | 높은 compression은 별도 model과 task-aware strategy를 사용 | 교훈만 흡수하고 compressor 구현은 범위 밖에 둔다 |
| Kummer et al., 2026 | compression preprocessing 비용이 이득을 상쇄할 수 있음 | runtime validation 비용을 bounded하게 유지한다 |
| Kabir et al., LREC 2026 | translation에서도 semantic label drift가 발생 | lexical ambiguity를 불필요하게 늘리지 않는다 |
| Shafiabadi & Yvon, LREC 2026 | lexical fidelity만으로 stance 보존을 보장하기 어려움 | uncertainty와 intent 같은 의미 역할을 보호한다 |

## References

- ASD-STE100 — https://www.asd-ste100.org/
- Agrawal, Sweta; Carpuat, Marine. *Do Text Simplification Systems Preserve Meaning? A Human Evaluation via Reading Comprehension*. TACL 2024 — https://aclanthology.org/2024.tacl-1.24/
- Shi, Ning et al. *Paraphrase Identification via Textual Inference*. *SEM 2024 — https://aclanthology.org/2024.starsem-1.11/
- Acharjee, Suvojit et al. *Who Remembers What? Tracing Information Fidelity in Human-AI Chains*. IJCNLP-AACL 2025 — https://aclanthology.org/2025.ijcnlp-long.146/
- Fu, Tingchen; Barez, Fazl. *Same Question, Different Words*. EMNLP 2025 — https://aclanthology.org/2025.emnlp-main.1595/
- Ngweta, Lilian et al. *Towards LLMs Robustness to Changes in Prompt Format Styles*. NAACL SRW 2025 — https://aclanthology.org/2025.naacl-srw.51/
- Nguyen, Anthony; Lin, Wenjun. *Does Context Compression Preserve Refusal Alignment?*. PMLR 2026 — https://proceedings.mlr.press/v318/nguyen26a.html
- Mahajan, Yash et al. *ALIGN-SIM*. Findings of EMNLP 2024 — https://aclanthology.org/2024.findings-emnlp.436/
- Mujahid, Zain Muhammad et al. *Stress Testing Factual Consistency Metrics for Long-Document Summarization*. ACL 2026 — https://aclanthology.org/2026.acl-long.1472/
- Veizaga, Alvaro et al. *On systematically building a controlled natural language for functional requirements*. 2021 — https://link.springer.com/article/10.1007/s10664-021-09956-6
- RFC 2119 — https://www.rfc-editor.org/info/rfc2119/
- RFC 8174 — https://www.rfc-editor.org/info/rfc8174/
- Jiang, Huiqiang et al. *LLMLingua*. EMNLP 2023 — https://aclanthology.org/2023.emnlp-main.825/
- Jiang, Huiqiang et al. *LongLLMLingua*. ACL 2024 — https://aclanthology.org/2024.acl-long.91/
- Kummer, Cornelius et al. *Prompt Compression in the Wild*. 2026 — https://arxiv.org/abs/2604.02985
- Kabir, Mohsinul et al. *Semantic Label Drift in Cross-Cultural Translation*. LREC 2026 — https://aclanthology.org/2026.lrec-1.297/
- Shafiabadi, Nazanin; Yvon, François. *Biases in Translation*. LREC 2026 — https://aclanthology.org/2026.lrec-1.679/

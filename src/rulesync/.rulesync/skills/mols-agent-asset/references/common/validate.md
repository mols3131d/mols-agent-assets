# Common Validate

Validation은 **정해진 계약을 충족하거나 의도한 계약이 올바르게 표현되어 있는지** 판정한다. 설계의 좋고 나쁨을 탐색하는 Review, 실제 성능을 측정하는 Eval과 구분한다.

## Choose the validation

| 종류 | 핵심 질문 | 추가 reference |
| --- | --- | --- |
| Deterministic Validation | 기계적으로 판정 가능한 규격과 계약을 준수하는가? | `../validation/deterministic.md` |
| Semantic Validation | 의도한 설계와 행동 계약이 instruction과 구조에 제대로 표현되어 있는가? | `../validation/semantic.md` |

한 claim이 구조적 규격과 의미적 설계를 모두 포함하면 두 검증을 함께 수행한다. 대상이 Skill, Rule, Agent/Subagent이면 해당 유형의 `validate.md`로 구체적인 contract를 추가한다.

검증 근거와 claim level은 `../evidence.md`를 따른다. Baseline이나 prior result를 현재 snapshot에서 다시 확인하면 `../revalidation.md`도 읽는다.

## Contract

- 이미 schema, parser, type system, framework validator, generator, native constraint가 같은 성질을 보장하면 새 check를 만들지 않는다.
- check 실패와 실행 불가를 구분한다. 실행하지 않은 중요한 check는 `not_run` 또는 `unknown`으로 남긴다.
- Deterministic pass를 Semantic pass로 확대하지 않고, Semantic pass를 runtime performance로 확대하지 않는다.
- source와 projection의 일치가 generator 전체의 semantic correctness나 실제 runtime behavior를 증명하지 않는다.
- 의미론적 검증은 현재 문구가 존재하는지만 보지 않고, authoritative intent와 현재 표현의 의미가 일치하는지 판단한다.
- 실제 selection, application, delegation, tool use, behavior, compatibility의 성능을 확인하려면 Eval을 사용한다.

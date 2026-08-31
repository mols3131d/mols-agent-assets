# `mols-text-optimizer` 구현 계획

이 문서는 [`mols-text-optimizer-research-plan.md`](mols-text-optimizer-research-plan.md)의 조사 결과를 실제 Skill 생성 작업으로 수렴시킨 **구현 Plan**이다. Research는 근거를 소유하고, 구현 순서와 acceptance는 이 문서가 소유한다.

목표는 **더 구체적인 owner가 없는 일반 텍스트 최적화에서만 선택되어, 구조를 건드리지 않고 의미와 기능을 보존하면서 기존 텍스트의 wording 비용을 줄이는 최소 범용 Skill**을 만드는 것이다.

## 완료 상태

다음이 충족되면 이번 작업은 완료다.

- `src/rulesync/.rulesync/skills/mols-text-optimizer/SKILL.md`가 canonical source로 존재한다.
- 대상에 적용되는 전문 Skill, 지침, 문서 또는 절차가 있으면 그것을 우선하고 이 Skill은 선택되지 않는다.
- 더 구체적인 owner가 없는 일반 텍스트 경량화 요청에서만 fallback으로 선택된다.
- routing/trigger는 frontmatter `description`이 소유하고 Skill body에서 중복하지 않는다.
- Skill body는 한국어 중심으로 작성하고, 번역하면 어색하거나 의미가 흐려지는 기술 용어·고유 명칭만 영어를 보조로 사용한다.
- frontmatter `description`은 repository 언어 정책의 Agent Asset trigger 규칙에 따라 영어를 유지한다.
- Markdown은 사람이 빠르게 읽을 수 있게 구성하고, 의미 없는 section·중복·기계적인 줄 폭 맞춤을 만들지 않는다.
- 단순 응답 간결화, 요약, 번역, 문체 윤문, Markdown 구조 개선, caveman-style 요청과 경계가 분명하다.
- 의미·기능·행동 보존이 wording/token 절감보다 우선한다.
- safe case에서는 실제 표현 비용이 줄고, 안전한 절감이 없으면 no-op한다.
- section, heading, sentence/paragraph boundary, list/table, delimiter, formatting contract를 변경하지 않는다.
- 기본 실행은 local wording edit + bounded check 한 번으로 끝난다.
- 최소 trigger/behavior fixture가 repository `evals/`에 존재한다.
- 신규 Skill이 distribution `route/skills.jsonl`에 repository-native generator로 반영된다.
- 기존 repository deterministic checks에서 새 오류가 없다.

## 범위

### 생성한다

```text
src/rulesync/.rulesync/skills/mols-text-optimizer/
└── SKILL.md

evals/skills/mols-text-optimizer/
├── trigger-evals.json
└── behavior-evals.json
```

Canonical Skill 변경으로 필요한 distribution route는 기존 generator로 재생성한다.

### 만들지 않는다

- `references/`, `scripts/`, tokenizer helper, evaluator helper
- 별도 compressor model 또는 compression pipeline
- embedding/BERTScore gate
- back-translation 또는 best-of-N 검증 체인
- 신규 Promptfoo runner 또는 generic eval framework
- 신규 route family
- `.agents/route/`용 repository self-consumer dependency
- CI/PR Gate 확장
- Markdown 구조·가독성 기능
- summarization, translation, humanization, response-style mode
- 전문 도메인 Skill이나 지침을 대체하는 범용 override logic
- Skill body의 별도 `Route` section

실제 implementation/eval evidence 없이 보조 구조를 추가하지 않는다.

## Skill 책임

`mols-text-optimizer`의 책임은 하나다.

> **더 구체적인 적용 owner가 없는 텍스트에서 material meaning과 기능을 유지하는 범위로 불필요한 wording 비용을 제거한다.**

Semantic stability는 별도 기능이 아니라 **optimization constraint**다. 더 짧아진 결과가 더 모호하거나 후속 변환에서 의미가 갈라지기 쉬워지면 그 축약을 하지 않는다.

이 Skill만으로 번역·재생성·요약·압축 이후 의미 동일성을 보장한다고 주장하지 않는다. 원문 wording에서 제거 가능한 ambiguity, synonym churn과 불필요한 표현 변이를 늘리지 않는 것이 범위다.

## Routing and activation

Routing과 trigger는 frontmatter `description`이 소유한다. Skill body는 이미 선택된 뒤의 실행 계약만 소유한다.

`description`은 다음을 분명하게 해야 한다.

- 이 Skill은 generic fallback이다.
- 현재 대상이나 작업에 더 구체적으로 적용되는 Skill, scoped instruction, document/domain guidance, framework contract 또는 procedure가 있으면 이 Skill을 선택하지 않는다.
- explicit invocation도 더 구체적인 applicable owner를 override하지 않는다.
- 대상 텍스트가 제공되거나 명확히 지칭되고, 의미 보존 경량화·축약·중복 제거·wording/token optimization intent가 있을 때만 trigger한다.
- generic response brevity, summarization, translation, humanization, Markdown/document restructuring, caveman style, latent prompt/context compression에는 trigger하지 않는다.

Skill body에 별도 routing workflow나 owner-discovery 절차를 반복하지 않는다. Routing surface가 이미 `description`을 보고 선택하므로 같은 책임을 body에 다시 넣으면 중복 context와 authority ambiguity가 생긴다.

## `SKILL.md` 설계

Single-file Skill로 시작한다. Body는 선택 이후의 실행 계약만 복원할 수 있으면 된다.

```text
Optimize → Preserve → Protect Structure → Check / Stop → Boundary
```

본문은 한국어를 기본으로 쓰고, `token`, `fallback`, `no-op`, `API`, `Markdown`처럼 번역이 더 어색하거나 기술적 의미가 흐려지는 표현만 영어로 유지한다. 문단은 의미 단위로 나누고, 목록 항목이나 문장을 임의의 열 너비에 맞춰 강제로 줄바꿈하지 않는다.

### Optimize

낮은 위험의 wording 변경부터 적용한다.

1. 의미 없는 반복이나 filler 제거
2. 같은 의미를 중복 표현한 local phrase 축약
3. 같은 concept의 불필요한 term variation 정리
4. 더 짧고 의미 범위가 동일한 local wording 사용
5. 더 이상 명확한 안전 이득이 없으면 stop

모든 단계를 수행하지 않는다. 안전한 후보가 없으면 즉시 no-op한다.

### Preserve

다음 의미는 compression-resistant하게 취급한다.

- **roles/actions** — actor, action, target, input/output, side effect, failure behavior
- **logic/control** — condition, exception, fallback, order, dependency, scope, causal/logical relation
- **strength/uncertainty** — negation, prohibition, modality, permission, quantifier, uncertainty, comparison
- **exact facts/tokens** — number, threshold, unit, date, name, identifier, path, command, API, field, code token, exact error string, citation/attribution
- **agent behavior** — activation, permission, safety boundary, required gate/stop

Agent-facing text에서는 반복된 guard나 instruction이 behavior-bearing일 수 있으므로 단지 lexical duplicate라는 이유로 제거하지 않는다.

### Protected surface

이 Skill은 구조를 최적화하지 않는다.

- section과 heading hierarchy
- sentence/paragraph boundary와 order
- list/table/callout representation
- numbering
- code fence, delimiter, indentation
- JSON/YAML/XML/schema-like structure
- exact output/format contract

Full artifact를 반환해야 하더라도 **optimization candidate 밖의 content를 광범위하게 rephrase하지 않는다.** 보호해야 하는 것은 출력 방식이 아니라 edit scope다.

### Check / Stop

변경한 span과 필요한 주변 context만 한 번 확인한다.

- 빠진 material information이 있는가?
- actor/action/target이 바뀌었는가?
- condition/exception binding이 바뀌었는가?
- negation/modality/quantifier/uncertainty가 바뀌었는가?
- scope/order/relation이 바뀌었는가?
- exact token, identifier, quantity 또는 unit이 바뀌었는가?
- agent-facing activation/permission/behavior가 달라질 수 있는가?
- protected surface를 변경했는가?

하나라도 불확실하면 해당 변경을 되돌리거나 원문을 유지한다.

추가 pass는 하지 않는다. 남은 변경이 style preference이거나 절감보다 검증 비용이 커지면 종료한다.

## Target

초기 target은 현재 reusable Rulesync Skill library가 유지하는 portable target과 맞춘다.

```yaml
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
```

`agentsskills`는 repository 내부 consumer 필요성이 별도로 확인되지 않는 한 추가하지 않는다.

실제 projection에서 Skill 의미를 표현할 수 없는 target이 확인되면 그때만 해당 target을 제외한다.

## Evaluation

Eval은 Skill package 밖 `evals/skills/mols-text-optimizer/`에 둔다. 이번 작업에서는 **fixture contract만 만든다.** 새 runtime runner나 judge pipeline은 만들지 않는다.

### Trigger fixture

Positive case:

- 별도 전문 owner가 없는 일반 text의 의미 보존 축약
- 별도 domain rule이 없는 제공 text의 중복 wording 제거
- generic prose를 기능/의미 보존 조건에서 경량화
- 적용 가능한 specific owner가 없는 explicit `mols-text-optimizer` 요청

Negative / near-miss:

- Agent Skill/Rule처럼 전문 authoring owner가 적용되는 text optimization 요청
- technical document처럼 전문 fidelity Skill이 적용되는 text optimization 요청
- path-scoped/document-specific 작성 지침이 적용되는 text optimization 요청
- target/framework-specific contract가 적용되는 경우
- generic brevity
- summarization
- translation
- humanization
- Markdown restructuring
- caveman style
- latent prompt compressor

Keyword 목록이 아니라 실제 사용자 표현 variation을 사용한다. 같은 optimization intent도 specific owner 존재 여부에 따라 routing 결과가 달라지는 paired case를 포함한다.

### Behavior fixture

정답 문장을 고정하지 않고 필요한 outcome만 기록한다.

필수 case:

1. obvious duplicate/filler → 실제 축약 + fact 보존
2. compact input → no-op 허용
3. `must`/`should`, prohibition, permission 강도 보존
4. quantifier와 uncertainty 보존
5. condition/exception binding 보존
6. actor/action/target 보존
7. identifier/path/command/API/quantity/unit 보존
8. ordered relation 보존
9. structure/format unchanged
10. agent-facing activation/permission/safety 보존
11. agent-facing repeated guard 무근거 삭제 금지
12. target compression ratio보다 meaning floor 우선

### Evidence boundary

- 기존 deterministic test는 fixture가 **valid JSON인지** 확인할 수 있다.
- fixture 내용의 semantic/routing quality는 Review가 소유한다.
- 실제 trigger/behavior 통과는 model/runtime을 실행했을 때만 behavioral evidence로 주장한다.
- 이번 작업에서 runtime eval을 실행하지 못해도 fixture 생성과 static Skill review는 완료할 수 있다. 실행하지 않은 runtime claim은 `not run`으로 남긴다.

## Distribution route

신규 canonical Skill은 repository-local `.agents/route/`가 아니라 이 repository가 제공하는 **distribution route**에 반영된다.

```text
src/rulesync/.rulesync/skills/mols-text-optimizer/SKILL.md
→ generated-sync
→ route/skills.jsonl
```

`.agents/route/uncategorized.jsonl`은 root lock-backed consumer Skill을 위한 surface이므로 이번 Skill 생성 범위에 포함하지 않는다.

Distribution route에 투영되는 `description`이 routing/trigger authority를 그대로 전달해야 한다.

## 작업 순서

### 1. Canonical Skill 작성

- directory와 `SKILL.md`를 만든다.
- `description`에서 specific-owner-first / generic-fallback, positive trigger와 near-miss를 구분한다.
- body에는 routing을 반복하지 않고 `Optimize / Preserve / Protect Structure / Check and Stop / Boundary`만 둔다.
- body prose는 한국어 중심으로 작성하고 필요한 기술 용어만 영어를 보조로 사용한다.
- 기계적인 줄 폭 맞춤 없이 의미 단위의 문단과 목록을 사용한다.
- Research의 논문·근거 설명은 복사하지 않는다.
- reference/helper는 만들지 않는다.

### 2. Authoring self-review

`mols-agent-asset`과 `mols-markdown-for-human` 기준으로 확인한다.

- 정말 신규 generic responsibility인가?
- description이 더 구체적인 owner를 가로채지 않는가?
- explicit invocation이 specific authority를 override한다고 읽히지 않는가?
- generic brevity, summarization, Markdown, humanization, caveman과 겹치지 않는가?
- routing responsibility가 body에 중복되지 않았는가?
- preservation rule이 reduction보다 우선하는가?
- structure를 owner 밖에서 변경하지 않는가?
- 한국어 본문이 자연스럽고 기술 용어의 영어 사용이 필요한 범위에 한정되는가?
- Markdown이 빠르게 훑어 읽을 수 있고 불필요한 section·중복·강제 줄바꿈이 없는가?
- always-loaded body가 불필요하게 장황하지 않은가?
- model/tokenizer별 가정을 portable contract로 만들지 않았는가?

### 3. Eval fixture 작성

- generic positive와 specific-owner negative를 함께 작성한다.
- 같은 optimization intent를 owner 유무만 바꾼 paired routing case를 포함한다.
- behavior safe-reduction/no-op/invariant case를 작성한다.
- exact output wording에 과적합하지 않았는지 확인한다.

### 4. Repository integration

- 필요한 Markdown formatting을 적용한다.
- Rulesync source validation을 수행한다.
- `mise run generated-sync`로 distribution route를 갱신한다.
- `route/skills.jsonl`의 description이 generic fallback boundary를 보존하는지 확인한다.

### 5. Verification

- `mise run check`
- `mise run test`
- 필요할 때만 target-specific Rulesync preview/validate
- 가능한 경우 behavioral capability eval

실행하지 못한 검증은 성공으로 추론하지 않는다.

### 6. Final review

다음 finding이 있을 때만 수정한다.

- specific owner가 있는데 generic Skill이 선택됨
- generic fallback이어야 하는데 선택되지 않음
- description과 body가 routing responsibility를 중복 소유함
- safe case에서 실질적 reduction이 없음
- semantic 또는 behavioral invariant 손실
- structure mutation
- 한국어 중심 원칙을 벗어난 불필요한 영어 서술
- 기계적인 줄바꿈이나 scan cost를 높이는 Markdown
- aggressive compression
- unnecessary context/steps
- sibling responsibility overlap
- fixture overfitting

새 기능이나 package 구조는 review finding 없이 추가하지 않는다.

## Acceptance

### Routing

- [ ] `mols-text-optimizer`가 범용 fallback으로 정의된다.
- [ ] 요청된 대상/작업에 specific Skill/instruction/document/domain guidance/framework contract/procedure가 적용되면 그것을 우선한다.
- [ ] specific owner가 적용되면 이 Skill은 자동 선택되지 않는다.
- [ ] explicit invocation도 더 구체적인 authority를 override하지 않는다.
- [ ] routing과 trigger는 `description`이 소유하고 body에 별도 `Route` section이 없다.
- [ ] generic fallback case와 specific-owner case를 trigger fixture가 구분한다.

### Language and readability

- [ ] frontmatter `description`은 영어 trigger value로 유지된다.
- [ ] Skill body의 일반 서술은 한국어 중심이다.
- [ ] 번역하면 어색하거나 의미가 흐려지는 기술 용어·고유 명칭만 영어를 사용한다.
- [ ] 문단과 목록은 의미 단위로 나뉘며 임의의 line-width wrapping을 하지 않는다.
- [ ] 같은 규칙을 여러 section에서 반복하지 않는다.

### Skill contract

- [ ] responsibility가 wording optimization 하나로 제한된다.
- [ ] generic response brevity를 소유하지 않는다.
- [ ] safe case에서는 실제 wording 비용이 줄어든다.
- [ ] unsafe/uncertain case에서는 no-op한다.
- [ ] semantic stability는 reduction의 제약이지 별도 expansion 기능이 아니다.

### Preservation

- [ ] material information을 줄이지 않는다.
- [ ] logic, strength, uncertainty와 exact technical token을 보존한다.
- [ ] agent-facing behavior boundary를 약화하지 않는다.
- [ ] structure와 formatting contract를 변경하지 않는다.
- [ ] edit scope 밖의 content를 불필요하게 rewrite하지 않는다.

### Package

- [ ] deployable package는 `SKILL.md` 하나다.
- [ ] eval은 package 밖에 있다.
- [ ] 불필요한 reference/script/helper가 없다.
- [ ] target은 현재 portable library 범위에 맞는다.

### Repository integration

- [ ] distribution `route/skills.jsonl`이 재생성된다.
- [ ] distribution description에 generic fallback boundary가 유지된다.
- [ ] `.agents/route/`를 이번 작업에서 변경하지 않는다.
- [ ] deterministic checks 결과를 기록한다.
- [ ] 실행하지 않은 runtime behavior를 통과했다고 주장하지 않는다.

## 리뷰 정리

### 구현 전에 반영 완료

| Finding | 결정 |
| --- | --- |
| `.agents/route/uncategorized` 자동 노출 가정 오류 | repository-local route를 범위에서 제거하고 distribution route만 사용 |
| semantic stabilization이 별도 capability로 확장될 위험 | stability를 optimization constraint로 축소 |
| activation이 "텍스트가 존재함"만으로 너무 넓음 | target text + optimization intent로 제한 |
| 범용 Skill이 전문 owner를 가로챌 위험 | specific-owner-first / generic-fallback을 `description`에 둠 |
| explicit Skill invocation이 authority override로 오인될 위험 | 명시 호출도 specific owner보다 우선하지 않도록 `description`에서 제한 |
| routing 책임을 body의 `Route` section에서 반복 | `Route` section 삭제, routing/trigger는 `description` 단일 owner |
| 영어 중심 body와 기계적 줄바꿈 | 한국어 중심 prose + 필요한 영어 보조 + 의미 단위 줄바꿈으로 수정 |
| whole-document regeneration 금지가 output 방식까지 제한 | `local edit scope` 보호로 재정의 |
| target metadata가 미정 | portable 6 targets를 초기값으로 고정 |
| eval deterministic evidence 과장 | JSON validity와 behavioral evidence를 분리 |

### 구현 중 확인

- description 첫 문맥에서 generic fallback임이 분명한가?
- description만으로 specific-owner near-miss가 충분히 구분되는가?
- safe reduction과 risky no-op가 둘 다 가능한가?
- preservation instruction이 너무 많아 context 비용을 키우지 않는가?
- Agent-facing text에서 duplicate-removal이 behavior를 약화시키지 않는가?
- 한국어 prose와 Markdown이 자연스럽고 빠르게 읽히는가?
- fixture가 특정 표현이나 model에 과적합되지 않는가?

### 이번 작업에서 defer

- repository가 신규 Skill을 self-consumer로 설치할지 여부
- `.agents/route` family 편입
- 별도 `text` family
- runtime eval runner / Promptfoo adapter
- deterministic token counter
- tokenizer-specific mode
- compression intensity option
- reference/helper 분리

이 항목들은 Skill 생성 자체에 필요하지 않다. 실제 사용 evidence가 생길 때 별도 작업으로 검토한다.

## Handoff

다음 작업은 canonical `SKILL.md`와 fixture를 리뷰하고 distribution route를 repository-native 방식으로 동기화하는 것이다. Skill body에는 별도 routing section을 다시 추가하지 않고, 한국어 중심 prose와 자연스러운 Markdown을 유지한다.

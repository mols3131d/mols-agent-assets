# `mols-text-optimizer` 구현 계획

이 계획은 [`mols-text-optimizer-research-plan.md`](mols-text-optimizer-research-plan.md)의 Research를 구현 가능한 작업 순서와 검증 계약으로 수렴시킨 Plan artifact다.

목표는 `mols-text-optimizer`를 **구조를 건드리지 않고, 의미와 행동 효과를 보존하면서 wording/token 비용을 줄이며 후속 semantic transform에도 의미가 쉽게 이동하지 않게 하는 최소 Skill**로 구현하는 것이다.

## Goal

다음 상태를 만들면 완료다.

- reusable Rulesync Skill `mols-text-optimizer`가 canonical source로 존재한다.
- 일반적인 text/token 경량화와 semantic-preserving wording optimization 요청에서 선택될 수 있다.
- 요약, 번역, 문체 윤문, Markdown 구조 개선, caveman-style 요청과 routing boundary가 분명하다.
- 최적화는 정보량을 줄이거나 구조를 재설계하지 않고 wording만 변경한다.
- semantic identity와 agent-facing behavioral identity가 token reduction보다 우선한다.
- 안전한 축약이 없으면 원문을 유지한다.
- runtime 기본 경로는 별도 compressor, judge, back-translation, best-of-N 또는 반복 evaluation을 요구하지 않는다.
- behavior와 trigger는 repository-owned eval fixture로 검토할 수 있다.
- generated route는 canonical source와 route owner에서 재생성된다.

## Active Scope

### In scope

- `src/rulesync/.rulesync/skills/mols-text-optimizer/SKILL.md`
- 신규 Skill의 `name`, `description`, target metadata와 runtime behavior
- `evals/skills/mols-text-optimizer/`의 최소 trigger/behavior fixture
- 신규 Skill routing을 위해 실제로 필요한 family membership 결정
- canonical source 변경으로 파생되는 generated route
- 이번 구현과 검증에 필요한 `inbox/2026-08-31/` Research, Plan, Review artifact

### Out of scope

- 문서 가독성 자체 개선
- section, heading, paragraph, list, table, callout 또는 information architecture 변경
- Markdown formatting 최적화
- 요약 기능
- 번역 기능
- tone, voice, persona 또는 humanization
- caveman-style response
- latent prompt/context compression
- 별도 compressor model
- embedding/BERTScore 기반 preservation gate
- 상시 back-translation 또는 regeneration evaluator
- tokenizer library나 token-count helper 추가
- 신규 Promptfoo framework 또는 범용 eval runner 구축
- 기존 sibling Skill의 동작 재설계

Scope expansion이 필요하면 구현 중 조용히 추가하지 않는다. 먼저 Review에서 필요성과 최소 경계를 확인한다.

## Fixed design decisions

다음은 Research에서 충분히 근거가 확보됐으므로 구현 중 기본적으로 다시 열지 않는다. 새로운 반례나 repository/runtime 제약이 발견될 때만 재계획한다.

1. **Wording-only optimizer** — text의 lexical/semantic 표현만 최적화한다.
2. **Structure protected** — 기존 section, heading, paragraph boundary, list/table representation, ordering, delimiter, code fence, indentation과 format contract를 optimizer가 재설계하지 않는다.
3. **Preservation before reduction** — 의미와 기능·행동 보존이 token saving보다 우선한다.
4. **No-op is success** — 안전한 절감이 없으면 입력을 유지한다.
5. **Semantic identity is relational** — 단어 유사도가 아니라 actor/action/target, condition, modality, negation, quantifier, scope, order, causality, exception과 identifier/quantity relation을 보존한다.
6. **Behavioral preservation is separate** — agent-facing instruction/policy/prompt는 semantic similarity만으로 parity를 주장하지 않는다.
7. **Transform resilience** — 번역만이 아니라 paraphrase, regeneration, summarization, compression, handoff에서도 의미가 쉽게 갈라지지 않는 wording을 선호한다.
8. **Bounded runtime** — 기본 실행은 한 번의 transform과 한 번의 bounded invariant scan으로 끝낸다.
9. **Single-file first** — deployable package는 `SKILL.md` 하나로 시작한다.
10. **Evaluation outside package** — repository-only behavioral fixture는 `evals/`가 소유한다.

## Target package

초기 canonical package:

```text
src/rulesync/.rulesync/skills/mols-text-optimizer/
└── SKILL.md
```

초기 verification surface:

```text
evals/skills/mols-text-optimizer/
├── trigger-evals.json
└── behavior-evals.json
```

`references/`, `scripts/`, template, tokenizer utility와 evaluator는 만들지 않는다. 다음 중 하나가 실제로 반복 확인될 때만 후속 변경으로 검토한다.

- core `SKILL.md`가 조건부 detail 때문에 실제 loading cost를 유의미하게 키움
- 모델이 같은 판단 로직을 반복적으로 잘못 재구현하며 deterministic helper가 실질적인 이득을 줌
- 특정 detail이 일부 activation에서만 필요하고 load condition을 명확히 정의할 수 있음

## `SKILL.md` contract

`SKILL.md`는 다음 네 가지 질문에 직접 답해야 한다.

```text
Condition → Behavior → Boundary → Validation / Stop
```

### Condition

선택해야 하는 intent:

- 기존 텍스트를 의미 보존 조건에서 더 짧게 만들기
- text/token 경량화
- wording compression
- lexical redundancy 제거
- semantic-preserving shortening
- 의미를 유지한 instruction/prose 경량화
- 후속 번역·재생성·압축에서 semantic drift가 적도록 wording 안정화

선택하지 않아야 하는 near-miss:

- 핵심만 남기는 요약
- 단순 번역
- 맞춤법/문법 교정만 요청
- AI 티 제거 또는 문체 윤문
- Markdown 가독성/구조 개선
- section/heading/list/table 재설계
- caveman/원시인 스타일
- latent context/prompt compressor
- 특정 tokenizer 알고리즘 구현

`description`은 user intent 중심으로 작성하고 내부 workflow를 설명하는 데 문자를 낭비하지 않는다. 가까운 sibling과 혼동되는 제외 경계만 포함한다.

### Behavior

기본 runtime procedure:

```text
Preserve → Reduce → Stabilize → Check → Stop
```

1. **Preserve** — 현재 텍스트에서 변하면 안 되는 semantic/behavioral anchor를 식별한다.
2. **Reduce** — 명확한 lexical redundancy, duplicate wording, 의미 없는 filler만 우선 제거한다.
3. **Stabilize** — 같은 concept의 term, ambiguous reference와 관계 표현을 필요한 범위에서만 안정화한다.
4. **Check** — omission, strength, scope, binding, relation, identity와 protected structure 변화를 한 번 확인한다.
5. **Stop** — 추가 이득이 작거나 보존 확신이 떨어지면 더 반복하지 않는다.

한 단계가 의미 위험을 만들면 다음 단계로 밀고 가지 않고 해당 변경을 되돌린다.

### Boundary

#### Protected semantic atoms

다음은 기본적으로 compression-resistant하다.

- fact / claim
- actor / subject
- action / operation
- object / target
- condition / trigger / precondition
- exception / fallback
- negation / prohibition
- modality / requirement strength / permission
- quantifier
- uncertainty / confidence
- scope / exclusivity
- order / dependency
- causal / logical relation
- comparison
- number / threshold / ratio / unit / date
- name / identifier / path / command / API / field / code token / exact error string
- input / output / side effect / failure behavior
- citation / attribution / meaningful uncertainty
- agent-facing activation / permission / safety boundary

#### Protected surface

다음은 wording optimization 대상이 아니다.

- section과 heading hierarchy
- paragraph boundary와 order
- list/table/callout representation
- numbering과 ordered procedure structure
- code fence, delimiter, indentation
- JSON/YAML/XML/schema-like structure
- exact output/format contract

텍스트가 더 짧아진다는 이유만으로 이 surface를 변경하지 않는다.

#### High-risk transforms

기본적으로 공격적으로 수행하지 않는다.

- `must`/`should`/`may` 같은 strength 변경
- 부정 표현 축약
- quantifier 삭제
- uncertainty marker를 filler로 간주해 삭제
- actor/object 생략
- pronoun/ellipsis로 explicit reference 축소
- condition 또는 exception을 암시적으로 흡수
- 여러 clause 병합
- domain term을 더 짧은 일반어로 치환
- 새로운 abbreviation 생성
- sentence fragment/telegraphic style 강제

### Validation / Stop

최종 check는 전체 텍스트를 다시 장문 분석하지 않고 아래 질문에 한정한다.

```text
빠진 정보나 규칙이 있는가?
actor/action/target이 바뀌었는가?
condition/exception binding이 바뀌었는가?
negation/modality/quantifier/uncertainty가 바뀌었는가?
scope/order/causal or logical relation이 바뀌었는가?
identifier/quantity/unit이 바뀌었는가?
agent-facing activation/permission/behavior가 달라질 수 있는가?
protected structure/formatting이 바뀌었는가?
```

하나라도 확실하지 않으면 해당 change를 revert하거나 원문을 유지한다.

다음 조건에서는 추가 pass 없이 종료한다.

- 남은 변경이 style preference 수준
- 더 줄이려면 high-risk atom을 건드려야 함
- 더 짧은 표현이 더 ambiguous함
- token saving이 미미하고 review 비용이 더 큼
- 목표 compression ratio를 위해 information loss가 필요함
- 이미 충분히 짧아 rewrite가 churn만 만듦

## Compression safety ladder

구현에서 transform priority는 다음처럼 낮은 위험부터 둔다.

```text
1. exact duplicate 제거
2. semantic duplicate wording 제거
3. 의미 없는 framing/filler 제거
4. 같은 concept의 term 통일
5. 의미가 동일한 local phrase 단축
6. 필요한 경우 ambiguous reference를 stable reference로 교체
7. stop
```

이 순서는 항상 모든 단계를 수행하라는 의미가 아니다. 앞 단계만으로 충분하면 즉시 종료한다.

## Semantic equivalence model

`mols-text-optimizer`가 목표로 하는 preservation은 surface similarity가 아니다.

개념적으로 원문 `S`와 최적화 결과 `O`는 **같은 material information을 양방향으로 복원할 수 있어야 한다.**

- `O`가 `S`의 일부 사실만 남기면 summarization에 가까우므로 실패다.
- `O`가 `S`에 없던 더 강한 claim, permission 또는 causal relation을 추가해도 실패다.
- wording이 크게 달라도 semantic anchors와 관계가 같으면 허용할 수 있다.

이를 자동 entailment engine으로 구현하지 않는다. runtime에서는 위의 bounded invariant scan으로 근사한다.

## Behavioral preservation for agent-facing text

Instruction, policy, prompt, Skill, Rule처럼 wording이 downstream model behavior에 직접 영향을 줄 수 있는 text는 추가로 다음을 확인한다.

- activation scope가 넓어지거나 좁아지지 않았는가?
- 필수 행동이 preference로 약해지지 않았는가?
- permission 또는 prohibition이 바뀌지 않았는가?
- required sequence/gate가 사라지지 않았는가?
- fallback/stop condition이 달라지지 않았는가?
- safety boundary가 duplicate로 오인돼 삭제되지 않았는가?

이 Skill 하나만으로 runtime behavioral parity를 **증명**했다고 주장하지 않는다. 중요한 Agent Asset 변경에서는 해당 asset owner와 behavioral eval이 최종 evidence를 소유한다.

## Token optimization policy

기본 목표는 tokenizer-specific 최소화가 아니라 **portable wording cost reduction**이다.

- target tokenizer가 지정되지 않으면 lexical redundancy와 문자/단어 비용을 primary signal로 본다.
- 특정 tokenizer가 지정되면 실제 token count를 보조 metric으로 사용할 수 있지만 semantic/behavioral invariant보다 우선하지 않는다.
- 여러 tokenizer를 기본적으로 비교하지 않는다.
- 고정 reduction percentage를 약속하지 않는다.
- input/context/reasoning token 전체가 같은 비율로 감소한다고 주장하지 않는다.

## Routing decision gate

신규 Skill을 canonical source에 추가한 뒤 `.agents/route/families.json` membership을 결정한다.

현재 family 기준에서:

- `writing`은 한국어 문체·윤문에 좁혀져 있어 자동 편입하지 않는다.
- `markdown`은 Markdown 작성·정비 owner이므로 편입하지 않는다.
- `agent-assets`는 Agent Asset 작성·탐색·검증 owner이므로 일반 text optimizer 자체를 편입하지 않는다.

구현 시 다음 순서로 결정한다.

1. 기존 family 의미를 넓히지 않고 자연스럽게 포함할 곳이 있는지 재검토한다.
2. 없다면 `text`처럼 실제 반복 routing value가 있는 새 family가 필요한지 검토한다.
3. 신규 family가 이 Skill 하나만 위한 taxonomy가 되어 관리 복잡성만 늘리면 우선 `uncategorized`에 두고 실제 sibling이 생길 때 승격한다.
4. 어떤 선택이든 generated route를 직접 편집하지 않는다.

초기 기본값은 **억지 기존 family 편입 금지**다. 새 family 생성은 구현 Review에서 실제 routing benefit이 확인될 때만 수행한다.

## Evaluation plan

Evaluation은 runtime Skill body와 분리한다.

### 1. Trigger fixture

`evals/skills/mols-text-optimizer/trigger-evals.json`

최소한 다음 category를 포함한다.

**Should trigger**

- 의미를 유지해 문장을 짧게 해달라는 명시적 요청
- token/text 비용을 줄여달라는 요청
- instruction을 기능 보존 조건에서 경량화하는 요청
- 중복 wording만 제거해 달라는 요청
- 번역/재생성 시 의미 drift를 줄이도록 wording을 안정화하는 요청
- Skill 이름을 명시한 요청

**Should not trigger / near-miss**

- 3줄 요약
- 번역
- 자연스럽게 윤문
- Markdown heading/section 개선
- 표나 list로 재구성
- 단순 맞춤법 수정
- caveman-style 요청
- latent prompt compressor 구현

초기 fixture는 keyword hit가 아니라 실제 사용자 phrasing variation과 sibling near-miss를 우선한다.

### 2. Behavior fixture

`evals/skills/mols-text-optimizer/behavior-evals.json`

정답 문장을 고정하지 않고 observable contract를 기록한다.

핵심 case:

1. exact duplicate는 줄지만 fact는 모두 보존
2. `must`가 `should`로 약해지지 않음
3. `must not` prohibition 유지
4. `all/some`, `at least/at most/exactly` 유지
5. uncertainty marker 유지
6. condition/exception binding 유지
7. actor/object 유지
8. ordered procedure의 order 유지
9. identifier/path/command/API/unit exact preservation
10. ambiguous reference는 필요한 경우 안정화하되 의미 추가 없음
11. 이미 compact한 input은 no-op 허용
12. structure/formatting unchanged
13. agent activation/permission boundary 보존
14. target compression ratio보다 meaning floor 우선
15. tokenizer scope와 reduction claim을 과장하지 않음

### Eval evidence level

- fixture 존재와 JSON 구조 correctness는 repository test 대상으로 검토할 수 있다.
- 실제 trigger/behavior claim은 runtime/model을 실행했을 때만 behavioral evidence로 주장한다.
- model grader를 사용한다면 semantic quality에 필요한 최소 rubric만 사용한다.
- 한 runtime 결과를 모든 target/runtime parity로 일반화하지 않는다.

처음부터 별도 generic runner, 반복 judge pipeline 또는 blocking CI를 추가하지 않는다.

## Deterministic verification plan

구현 후 repository-native 검증을 사용한다.

1. 변경된 Markdown formatting이 필요하면 `mise run format-changed`.
2. canonical Rulesync source에 필요한 current Rulesync validation을 수행한다.
3. `mise run generated-sync`로 route/index projection을 갱신한다.
4. `mise run check`와 `mise run test`를 실행한다.
5. 특정 target projection claim이 필요할 때만 Rulesync preview/validate를 추가한다.
6. 실행하지 못한 검증은 `not run`으로 남긴다.

새 Skill 하나 때문에 CI 또는 PR Gate를 확장하지 않는다.

## Ordered implementation

### Phase 1 — Canonical Skill

1. `src/rulesync/.rulesync/skills/mols-text-optimizer/`를 만든다.
2. single-file `SKILL.md`를 작성한다.
3. `description`은 capability + activation + near-miss boundary에 집중한다.
4. body는 `Contract`, `Optimize`, `Preserve`, `Check`, `Boundary` 정도의 최소 responsibility로 구성한다.
5. Research 보고서의 논문·표준 설명을 Skill body에 복사하지 않는다.
6. protected semantic atoms와 protected structure는 runtime에서 필요한 수준만 유지한다.

### Phase 2 — Static self-review

`mols-agent-asset` 기준으로 다음을 검토한다.

- 신규 responsibility가 기존 owner와 실제로 구분되는가?
- description이 summarization/markdown/humanize/caveman과 충돌하지 않는가?
- always-loaded context가 research rationale로 비대해지지 않았는가?
- workflow가 한 기본 경로로 수렴하는가?
- no-op/revert/stop이 명확한가?
- structure owner를 침범하지 않는가?
- 특정 model/tokenizer assumption을 portable rule로 만들지 않았는가?

### Phase 3 — Behavioral fixtures

1. trigger fixture를 positive + sibling near-miss로 작성한다.
2. behavior fixture를 semantic/behavioral invariant 중심으로 작성한다.
3. fixture가 특정 정답 wording을 강제하지 않는지 Review한다.
4. 단순 source string synchronization을 regression test로 만들지 않는다.

### Phase 4 — Routing integration

1. Skill description이 canonical source에서 확정된 뒤 routing family를 결정한다.
2. 기존 family 의미를 억지로 확장하지 않는다.
3. family source를 변경했다면 repository generator로 `.agents/route/*`와 distribution route를 재생성한다.
4. generated JSONL은 직접 수정하지 않는다.

### Phase 5 — Verification

1. direct inspection으로 source/route/eval boundary를 확인한다.
2. repository deterministic checks를 실행한다.
3. 가능한 target projection을 확인한다.
4. 실제 model/runtime eval이 가능하면 capability evidence로 실행한다.
5. failure를 Skill, fixture, harness/runtime, grader 문제로 분리한다.

### Phase 6 — Review and bounded correction

Review에서 다음 finding만 수정으로 되돌린다.

- activation false positive/negative
- semantic anchor 손실 가능성
- behavioral boundary 약화
- structure mutation 허용
- unsafe aggressive compression
- runtime workflow 과다
- sibling responsibility overlap
- eval이 implementation wording에 과적합
- route family가 taxonomy-only complexity를 만듦

새 기능이나 구조는 Review finding 없이 추가하지 않는다.

## Acceptance conditions

### Responsibility

- `mols-text-optimizer`가 wording/token optimization만 소유한다.
- readability, document structure, summary, translation, style와 persona를 소유하지 않는다.
- `mols-markdown-for-human`, `humanize-korean`, `caveman-ko`, summarization과 boundary가 description/body/eval에서 일관된다.

### Preservation

- 정보량을 의도적으로 줄이지 않는다.
- actor/action/target을 보존한다.
- condition/exception/fallback binding을 보존한다.
- negation, modality, quantifier, uncertainty를 보존한다.
- scope, order, causal/logical relation을 보존한다.
- identifier, quantity, threshold, unit과 exact technical token을 보존한다.
- agent-facing activation/permission/safety behavior를 약화하지 않는다.

### Optimization

- 명확한 lexical redundancy부터 제거한다.
- 같은 concept의 synonym churn을 줄인다.
- 더 짧은 표현이 ambiguity를 키우면 사용하지 않는다.
- target ratio를 맞추기 위한 강제 compression을 하지 않는다.
- 안전한 이득이 없으면 no-op한다.

### Structure

- section, heading, paragraph, list/table, order, delimiter와 formatting contract를 optimizer가 변경하지 않는다.

### Runtime cost

- 기본 경로는 single transform + bounded check다.
- best-of-N, 반복 judge, embedding threshold, 상시 back-translation, tokenizer sweep을 요구하지 않는다.
- 별도 compressor model을 dependency로 삼지 않는다.

### Package

- 초기 deployable package는 single-file Skill이다.
- repository-only eval은 package 밖에 있다.
- 불필요한 reference/script/helper를 추가하지 않는다.

### Evidence

- deterministic check와 behavioral eval의 claim을 구분한다.
- 실행하지 않은 runtime behavior를 통과했다고 주장하지 않는다.
- generated route는 canonical owner에서 재생성된다.

## Risk register

| Risk | 계획상 대응 |
| --- | --- |
| 일반 brevity 요청까지 과잉 trigger | near-miss trigger eval과 description boundary |
| summarization으로 정보량 손실 | bidirectional information coverage intuition + no-op |
| token 절감 때문에 modality/negation 손실 | protected semantic atoms |
| 짧은 다의어로 semantic drift 증가 | stable terminology와 ambiguity gate |
| 구조 변경으로 agent behavior 변동 | protected structure |
| validator가 optimizer보다 비싸짐 | one-pass bounded check |
| embedding score가 false confidence 제공 | universal metric gate 금지 |
| Skill body가 연구 보고서를 복제해 비대해짐 | research rationale는 inbox에 남기고 runtime contract만 canonical화 |
| 기존 Skill과 responsibility overlap | trigger near-miss + explicit boundary |
| routing family를 Skill 하나 때문에 과설계 | 기존 family 강제 편입 금지, 새 family benefit gate |
| eval fixture 과적합 | outcome contract, near-miss, runtime evidence level 분리 |

## Deferred decisions

다음은 구현 전 미리 고정하지 않는다.

- `text` route family 신설 여부
- target별 추가 metadata
- reference 분리 여부
- deterministic token counter
- Promptfoo adapter 또는 generic eval runner
- regression contract 승격
- 특정 tokenizer 최적화 mode
- compression intensity argument

실제 implementation/eval evidence가 필요성을 만들 때만 별도 Research/Plan으로 연다.

## Review loop ledger

이 Plan을 만들며 닫은 substantive Review는 다음 concern을 각각 재검토했다.

1. 신규 Skill responsibility와 sibling owner 경계
2. repository Testing/Evaluation ownership
3. trigger fixture와 behavior fixture 분리
4. outcome 중심 eval contract
5. route family 충돌 가능성
6. single-file package 최소성
7. `Condition → Behavior → Boundary → Validation/Stop` instruction contract
8. naming 최소성
9. Rulesync canonical/projection boundary
10. current Agent Skills creator guidance와 repository-local policy 조정
11. Research와 Plan artifact의 responsibility 분리

이후 Review는 구현 과정에서 실제 delta가 생길 때 계속한다. 숫자를 채우기 위한 no-op loop는 수행하지 않는다.

## Implementation handoff

다음 작업은 **Phase 1 — Canonical Skill**에서 시작한다.

첫 변경은 `SKILL.md` 하나여야 한다. 그 초안이 responsibility, activation, preservation, runtime-cost와 protected-structure contract를 충분히 표현하지 못한다는 실제 근거가 나오기 전에는 reference, helper 또는 별도 framework를 추가하지 않는다.

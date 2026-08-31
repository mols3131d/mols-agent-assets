# `mols-text-optimizer` 구현 계획

이 계획은 [`mols-text-optimizer-research-plan.md`](mols-text-optimizer-research-plan.md)의 Research를 구현 가능한 작업 순서와 검증 계약으로 수렴시킨 Plan artifact다.

목표는 `mols-text-optimizer`를 **기존 구조를 건드리지 않고, 의미와 행동 효과를 보존하면서 wording 비용을 줄이며 후속 변환에서도 불필요한 semantic drift가 커지지 않게 하는 최소 Skill**로 구현하는 것이다.

완전한 의미 보존을 보장할 수 없는 lossy transform까지 통제한다고 주장하지 않는다. 번역, paraphrase, regeneration, summarization, compression, model handoff에서 **원문 wording 때문에 생기는 피할 수 있는 drift를 줄이는 것**이 목표다.

## Goal

다음 상태를 만들면 완료다.

- reusable Rulesync Skill `mols-text-optimizer`가 canonical source로 존재한다.
- 기존 텍스트를 의미 보존 조건에서 경량화하거나 semantic identity를 안정화하려는 요청에서 선택될 수 있다.
- 단순한 "짧게 답해" 같은 response brevity 요청에는 자동 선택되지 않는다.
- 요약, 번역, 문체 윤문, Markdown 구조 개선, caveman-style 요청과 routing boundary가 분명하다.
- 최적화는 정보량을 줄이거나 문서 구조를 재설계하지 않고 wording만 변경한다.
- semantic identity와 agent-facing behavioral identity가 token reduction보다 우선한다.
- safe case에서는 실제 wording 감소를 만들고, risky case에서는 no-op를 정상 성공으로 허용한다.
- runtime 기본 경로는 별도 compressor, judge, back-translation, best-of-N 또는 반복 evaluation을 요구하지 않는다.
- behavior와 trigger는 repository-owned eval fixture로 검토할 수 있다.
- generated route는 canonical source에서 repository-native 방식으로 재생성된다.

## Active Scope

### In scope

- `src/rulesync/.rulesync/skills/mols-text-optimizer/SKILL.md`
- 신규 Skill의 `name`, `description`, target metadata와 runtime behavior
- `evals/skills/mols-text-optimizer/`의 최소 trigger/behavior fixture
- canonical source 변경으로 파생되는 generated route
- 이번 구현과 검증에 필요한 `inbox/2026-08-31/` Research, Plan, Review artifact

### Out of scope

- 문서 가독성 자체 개선
- section, heading, sentence/paragraph, list, table, callout 또는 information architecture 재설계
- Markdown formatting 최적화
- 요약 기능
- 번역 기능
- tone, voice, persona 또는 humanization 최적화
- caveman-style response
- 일반 응답을 무조건 짧게 만드는 response mode
- latent prompt/context compression
- 별도 compressor model
- embedding/BERTScore 기반 preservation gate
- 상시 back-translation 또는 regeneration evaluator
- tokenizer library나 token-count helper 추가
- 신규 Promptfoo framework 또는 범용 eval runner 구축
- 기존 sibling Skill의 동작 재설계
- 신규 route family 신설

Scope expansion이 필요하면 구현 중 조용히 추가하지 않는다. 먼저 Review에서 필요성과 최소 경계를 확인한다.

## Fixed design decisions

다음은 Research와 Plan Review에서 충분히 수렴했으므로 새로운 반례나 repository/runtime 제약이 발견될 때만 다시 연다.

1. **Wording-only optimizer** — text의 lexical/semantic 표현만 최적화한다.
2. **Existing text or explicit optimizer intent** — 기본 activation은 변환할 텍스트가 있거나 의미 보존 경량화/semantic stabilization을 명시한 경우다. 단순 response brevity는 제외한다.
3. **Structure protected** — 기존 heading, sentence/paragraph boundary, list/table representation, ordering, delimiter, code fence, indentation과 format contract를 재설계하지 않는다.
4. **Preservation before reduction** — 의미와 기능·행동 보존이 token saving보다 우선한다.
5. **No-op is success** — 안전한 절감이 없으면 입력을 유지한다.
6. **Safe cases must still optimize** — 명백한 중복·filler 같은 low-risk case에서는 실제 경량화가 보여야 한다.
7. **Semantic identity is relational** — 단어 유사도가 아니라 actor/action/target, condition, modality, negation, quantifier, scope, order, causality, exception과 identifier/quantity relation을 보존한다.
8. **Behavioral preservation is separate** — agent-facing instruction/policy/prompt는 semantic similarity만으로 parity를 주장하지 않는다.
9. **Repetition can be behavior-bearing** — Agent-facing text의 반복은 emphasis나 behavior에 영향을 줄 수 있으므로 일반 prose의 duplicate-removal 규칙을 자동 적용하지 않는다.
10. **Transform resilience is bounded** — 후속 변환의 손실을 보장하지 않고, ambiguity와 synonym churn 등 피할 수 있는 drift source를 줄인다.
11. **Locality first** — 전체 문서의 semantic map을 만들지 않고 실제 변경 후보와 그 관계에 필요한 주변 context만 확인한다.
12. **No whole-document regeneration** — local wording edit가 목표일 때 문서 전체를 다시 생성하지 않는다.
13. **Bounded runtime** — 기본 실행은 한 번의 transform과 한 번의 bounded invariant scan으로 끝낸다.
14. **Single-file first** — deployable package는 `SKILL.md` 하나로 시작한다.
15. **Evaluation outside package** — repository-only behavioral fixture는 `evals/`가 소유한다.
16. **Initial route family stays unchanged** — 이 Skill 하나만 위해 `text` family를 만들지 않는다. `.agents/route/families.json`을 수정하지 않고 generated `uncategorized` discovery를 사용한다.

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

- 주어진 텍스트를 의미 보존 조건에서 더 짧게 만들기
- prompt/instruction/prose의 wording 또는 token 비용을 줄이기
- lexical redundancy 제거
- semantic-preserving shortening
- 내용과 기능을 유지한 text optimization
- 번역·재생성·압축 등 후속 변환에서 drift가 덜 생기도록 wording을 안정화
- `mols-text-optimizer`를 명시적으로 사용 요청

선택하지 않아야 하는 near-miss:

- "앞으로 짧게 답해", "간결하게 말해" 같은 generic response brevity
- 핵심만 남기는 요약
- 단순 번역
- 맞춤법/문법 교정만 요청
- AI 티 제거 또는 문체 윤문
- Markdown 가독성/구조 개선
- section/heading/list/table 재설계
- caveman/원시인 스타일
- latent context/prompt compressor 구현
- 특정 tokenizer compression algorithm 구현

`description`은 user intent 중심으로 작성하고 내부 workflow를 설명하는 데 문자를 낭비하지 않는다. sibling과 혼동되는 실질적 제외 경계만 포함한다.

### Behavior

기본 runtime procedure:

```text
Preserve → Reduce → Stabilize → Check → Stop
```

1. **Preserve** — 전체 문서를 분석 목록으로 만들지 않고, 변경 후보와 그 의미 관계에서 변하면 안 되는 semantic/behavioral anchor만 식별한다.
2. **Reduce** — 명확한 lexical redundancy와 의미 없는 filler를 low-risk 후보부터 줄인다.
3. **Stabilize** — 같은 concept의 term과 reference가 실제로 흔들릴 때만 최소한으로 안정화한다.
4. **Check** — 변경된 span과 필요한 주변 context에서 omission, strength, scope, binding, relation, identity와 protected structure 변화를 한 번 확인한다.
5. **Stop** — 추가 이득이 작거나 보존 확신이 떨어지면 더 반복하지 않는다.

한 단계가 의미 위험을 만들면 다음 단계로 밀고 가지 않고 해당 변경을 되돌린다.

#### Stabilization cost rule

기본 reduction 요청에서는 semantic stability를 이유로 텍스트를 불필요하게 늘리지 않는다.

- 더 짧은 candidate가 모호하면 기존의 더 안정적인 표현을 유지한다.
- 명시적으로 semantic stabilization을 요청한 경우에는 정보 추가 없이 더 좁고 안정적인 wording으로 바꿀 수 있다.
- 이 경우에도 큰 net expansion이나 설명 추가는 하지 않는다.

### Boundary

#### Protected semantics

`SKILL.md`에서는 아래를 exhaustive taxonomy처럼 길게 복제하지 않고 몇 개의 묶음으로 간결하게 표현한다.

- **roles and actions** — actor, action, target, input/output, side effect, failure behavior
- **logic and control** — condition, trigger, exception, fallback, order, dependency, causal/logical relation, scope
- **strength and uncertainty** — negation, prohibition, modality, permission, quantifier, uncertainty, comparison
- **exact facts and tokens** — number, threshold, ratio, unit, date, name, identifier, path, command, API, field, code token, exact error string, citation/attribution
- **agent behavior** — activation, permission, safety boundary, required gate/stop

#### Protected surface

다음은 wording optimization 대상이 아니다.

- section과 heading hierarchy
- sentence/paragraph boundary와 order
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
- 여러 sentence/clause 병합
- domain term을 더 짧은 일반어로 치환
- 사용자나 domain이 canonical로 정한 term 변경
- 새로운 abbreviation 생성
- sentence fragment/telegraphic style 강제
- Agent-facing 반복 문장을 단지 duplicate라는 이유로 제거

### Validation / Stop

최종 check는 전체 텍스트를 다시 장문 분석하지 않고 변경 span 중심으로 아래 질문에 한정한다.

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
- 더 줄이려면 high-risk semantic을 건드려야 함
- 더 짧은 표현이 더 ambiguous함
- token saving이 미미하고 review 비용이 더 큼
- 목표 compression ratio를 위해 information loss가 필요함
- 이미 충분히 짧아 rewrite가 churn만 만듦

출력은 사용자가 요구한 기존 surface를 따른다. Skill 자체가 변경 설명, 새 heading, wrapper 또는 별도 report format을 강제로 추가하지 않는다.

## Compression safety ladder

일반 prose의 transform priority는 다음처럼 낮은 위험부터 둔다.

```text
1. 의미 없는 exact repetition 후보
2. 명백한 semantic duplicate wording 후보
3. 의미 없는 framing/filler
4. 같은 concept의 불필요한 term variation
5. 의미가 동일한 local phrase 단축
6. shortening 과정에서 필요한 reference 안정화
7. stop
```

이 순서는 모든 단계를 수행하라는 뜻이 아니다. 앞 단계만으로 충분하면 즉시 종료한다.

Agent-facing instruction/policy/prompt에서는 1~2번도 **behavior-sensitive 후보**로 올려서, 반복이 실제 behavior를 바꾸지 않는다는 근거 없이 자동 삭제하지 않는다.

## Semantic equivalence model

`mols-text-optimizer`가 목표로 하는 preservation은 surface similarity가 아니다.

개념적으로 원문 `S`와 최적화 결과 `O`는 **같은 material information을 양방향으로 복원할 수 있어야 한다.**

- `O`가 `S`의 일부 사실만 남기면 summarization에 가까우므로 실패다.
- `O`가 `S`에 없던 더 강한 claim, permission 또는 causal relation을 추가해도 실패다.
- wording이 크게 달라도 semantic anchors와 관계가 같으면 허용할 수 있다.

이를 자동 entailment engine으로 구현하지 않는다. runtime에서는 bounded invariant scan으로 근사한다.

이 equivalence는 후속 summarization 같은 lossy transform의 결과까지 동일하게 만든다는 보장이 아니다. optimizer가 하는 일은 원문 자체의 ambiguity와 unstable wording을 불필요하게 키우지 않는 것이다.

## Behavioral preservation for agent-facing text

Instruction, policy, prompt, Skill, Rule처럼 wording이 downstream model behavior에 직접 영향을 줄 수 있는 text는 추가로 다음을 확인한다.

- activation scope가 넓어지거나 좁아지지 않았는가?
- 필수 행동이 preference로 약해지지 않았는가?
- permission 또는 prohibition이 바뀌지 않았는가?
- required sequence/gate가 사라지지 않았는가?
- fallback/stop condition이 달라지지 않았는가?
- safety boundary나 behavior-bearing repetition이 duplicate로 오인돼 삭제되지 않았는가?

이 Skill 하나만으로 runtime behavioral parity를 **증명**했다고 주장하지 않는다. 중요한 Agent Asset 변경에서는 해당 asset owner와 behavioral eval이 최종 evidence를 소유한다.

Agent Asset을 실제로 수정하는 작업에서는 `mols-agent-asset`이 ownership/activation/authority를 계속 소유하고, `mols-text-optimizer`는 wording optimization만 보조한다.

## Token optimization policy

기본 목표는 tokenizer-specific 최소화가 아니라 **portable wording cost reduction**이다.

- target tokenizer가 지정되지 않으면 lexical redundancy와 textual length 감소를 optimization signal로 본다.
- tokenizer를 실행하지 않았다면 정확한 token 감소량을 주장하지 않는다.
- 특정 tokenizer가 지정되면 실제 token count를 보조 metric으로 사용할 수 있지만 semantic/behavioral invariant보다 우선하지 않는다.
- 여러 tokenizer를 기본적으로 비교하지 않는다.
- 고정 reduction percentage를 약속하지 않는다.
- input/context/reasoning token 전체가 같은 비율로 감소한다고 주장하지 않는다.

## Routing decision

초기 구현에서는 `.agents/route/families.json`을 변경하지 않는다.

현재 family 기준에서 `writing`은 한국어 문체·윤문, `markdown`은 Markdown 작성·정비, `agent-assets`는 Agent Asset 작성·탐색·검증을 소유한다. `mols-text-optimizer`를 이 중 하나에 넣으려면 family 의미를 넓혀야 한다.

이 Skill 하나만 위해 `text` family를 만드는 것도 현재 YAGNI다.

따라서 초기 상태는:

```text
canonical Skill 추가
→ families.json unchanged
→ generated-sync
→ .agents/route/uncategorized.jsonl에서 repository-local discovery
→ route/skills.jsonl에서 distribution discovery
```

향후 같은 semantic text-transform responsibility를 가진 sibling이 실제로 생기면 별도 routing Review에서 family 승격을 검토한다.

## Evaluation plan

Evaluation은 runtime Skill body와 분리한다.

### 1. Trigger fixture

`evals/skills/mols-text-optimizer/trigger-evals.json`

**Should trigger**

- 주어진 문장을 의미 유지하며 줄여 달라는 요청
- prompt/instruction을 기능 보존 조건에서 경량화하는 요청
- 제공된 text의 중복 wording만 제거해 달라는 요청
- 번역/재생성 때 의미가 덜 흔들리도록 제공 text의 wording을 안정화하는 요청
- `mols-text-optimizer`를 명시한 요청
- 긴 context 안에 text optimization 단계가 포함된 복합 요청

**Should not trigger / near-miss**

- "앞으로 짧게 답해"
- "간결하게 설명해"
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

1. obvious prose duplicate/filler는 실제로 줄고 fact는 보존
2. safe local phrase는 shorter output을 만들 수 있음
3. `must`가 `should`로 약해지지 않음
4. `must not` prohibition 유지
5. `all/some`, `at least/at most/exactly` 유지
6. uncertainty marker 유지
7. condition/exception binding 유지
8. actor/object 유지
9. ordered procedure의 order 유지
10. identifier/path/command/API/unit exact preservation
11. user/domain canonical term 유지
12. ambiguous reference는 shortening 때문에 악화되지 않음
13. 이미 compact한 input은 no-op 허용
14. sentence/paragraph/section/list/table structure unchanged
15. agent activation/permission boundary 보존
16. agent-facing repeated guard를 근거 없이 duplicate로 제거하지 않음
17. target compression ratio보다 meaning floor 우선
18. tokenizer scope와 reduction claim을 과장하지 않음
19. output에 optimizer 설명용 wrapper를 임의 추가하지 않음

### 3. Utility baseline

Skill이 실제로 추가 가치를 주는지 확인할 수 있는 runtime이 있으면 representative safe/risky case를 **Skill 없이 / Skill과 함께** 비교한다.

확인할 claim:

- safe case에서 wording cost가 더 잘 줄어드는가?
- semantic/behavioral loss가 늘지 않는가?
- risky case에서 불필요한 rewrite가 줄어드는가?
- extra instruction 때문에 실행이 더 장황하거나 반복적이 되지 않는가?

이 비교를 위한 범용 runner를 이번 작업에서 새로 만들지는 않는다.

### Eval evidence level

- fixture 존재와 JSON 구조 correctness는 repository test 대상으로 검토할 수 있다.
- 실제 trigger/behavior claim은 runtime/model을 실행했을 때만 behavioral evidence로 주장한다.
- model grader를 사용한다면 semantic quality에 필요한 최소 rubric만 사용한다.
- 한 runtime 결과를 모든 target/runtime parity로 일반화하지 않는다.
- description optimization을 실제로 반복할 때만 current Agent Skills creator guidance의 multi-run/train-validation 방법을 적용한다. 해당 절차를 Skill body나 repository contract로 복제하지 않는다.

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
3. `description`은 existing-text/explicit-optimizer intent + sibling near-miss boundary에 집중한다.
4. body는 `Contract`, `Optimize`, `Preserve`, `Check`, `Boundary` 정도의 최소 responsibility로 구성한다.
5. Research 보고서의 논문·표준 설명을 Skill body에 복사하지 않는다.
6. protected semantics는 exhaustive list가 아니라 runtime 판단에 필요한 몇 개 category로 압축한다.
7. structure protection과 no-op stop은 항상 발견 가능한 core에 둔다.

### Phase 2 — Static self-review

`mols-agent-asset` 기준으로 다음을 검토한다.

- 신규 responsibility가 기존 owner와 실제로 구분되는가?
- generic response brevity에 false-trigger하지 않는가?
- description이 summarization/markdown/humanize/caveman과 충돌하지 않는가?
- always-loaded context가 research rationale로 비대해지지 않았는가?
- workflow가 한 기본 경로로 수렴하는가?
- whole-document regeneration이나 exhaustive semantic inventory를 요구하지 않는가?
- no-op/revert/stop이 명확한가?
- structure owner를 침범하지 않는가?
- 특정 model/tokenizer assumption을 portable rule로 만들지 않았는가?

### Phase 3 — Behavioral fixtures

1. trigger fixture를 positive + sibling near-miss로 작성한다.
2. behavior fixture를 semantic/behavioral invariant 중심으로 작성한다.
3. safe reduction case와 risky no-op case를 모두 둔다.
4. Agent-facing repetition case를 별도로 둔다.
5. fixture가 특정 정답 wording을 강제하지 않는지 Review한다.
6. 단순 source string synchronization을 regression test로 만들지 않는다.

### Phase 4 — Routing integration

1. `.agents/route/families.json`은 변경하지 않는다.
2. canonical source와 eval이 확정되면 repository generator로 route를 재생성한다.
3. `uncategorized` route에 정상 노출되는지 확인한다.
4. distribution `route/skills.jsonl`에 신규 Skill이 포함되는지 확인한다.
5. generated JSONL은 직접 수정하지 않는다.

### Phase 5 — Verification

1. direct inspection으로 source/route/eval boundary를 확인한다.
2. repository deterministic checks를 실행한다.
3. 필요한 target projection을 확인한다.
4. 실제 model/runtime eval이 가능하면 capability evidence로 실행한다.
5. 가능하면 Skill 없이/함께 representative utility baseline을 비교한다.
6. failure를 Skill, fixture, harness/runtime, grader 문제로 분리한다.

### Phase 6 — Review and bounded correction

Review에서 다음 finding만 수정으로 되돌린다.

- activation false positive/negative
- safe case에서 실질적 reduction이 없음
- semantic anchor 손실 가능성
- behavioral boundary 약화
- Agent-facing repetition의 무근거 삭제
- structure mutation 허용
- unsafe aggressive compression
- runtime workflow 과다
- whole-document regeneration 유도
- sibling responsibility overlap
- eval이 implementation wording에 과적합

새 기능이나 구조는 Review finding 없이 추가하지 않는다.

## Acceptance conditions

### Responsibility

- `mols-text-optimizer`가 제공된 text의 wording/token optimization만 소유한다.
- generic response brevity mode를 소유하지 않는다.
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
- Agent-facing repetition을 단순 lexical duplicate로 취급하지 않는다.

### Optimization

- 명확한 lexical redundancy부터 제거한다.
- safe representative case에서는 실제 wording cost가 감소한다.
- 같은 concept의 불필요한 synonym churn을 줄일 수 있다.
- 사용자/domain canonical term을 바꾸지 않는다.
- 더 짧은 표현이 ambiguity를 키우면 사용하지 않는다.
- target ratio를 맞추기 위한 강제 compression을 하지 않는다.
- 안전한 이득이 없으면 no-op한다.

### Structure

- section, heading, sentence/paragraph, list/table, order, delimiter와 formatting contract를 optimizer가 변경하지 않는다.

### Runtime cost

- semantic scan은 변경 후보 중심으로 bounded하다.
- whole-document regeneration을 기본 경로로 요구하지 않는다.
- 기본 경로는 single transform + bounded check다.
- best-of-N, 반복 judge, embedding threshold, 상시 back-translation, tokenizer sweep을 요구하지 않는다.
- 별도 compressor model을 dependency로 삼지 않는다.

### Package and routing

- 초기 deployable package는 single-file Skill이다.
- repository-only eval은 package 밖에 있다.
- 불필요한 reference/script/helper를 추가하지 않는다.
- 신규 route family를 만들지 않는다.
- generated route가 `uncategorized`와 distribution discovery를 정상 반영한다.

### Evidence

- deterministic check와 behavioral eval의 claim을 구분한다.
- 실행하지 않은 runtime behavior를 통과했다고 주장하지 않는다.
- tokenizer를 실행하지 않았다면 정확한 token 절감량을 주장하지 않는다.
- generated route는 canonical owner에서 재생성된다.

## Risk register

| Risk | 계획상 대응 |
| --- | --- |
| generic brevity 요청까지 과잉 trigger | existing-text/explicit optimizer activation + near-miss eval |
| summarization으로 정보량 손실 | bidirectional information coverage intuition + no-op |
| token 절감 때문에 modality/negation 손실 | protected semantics |
| 짧은 다의어로 semantic drift 증가 | stable terminology와 ambiguity gate |
| lossy transform까지 robustness를 과장 | avoidable drift reduction으로 claim 제한 |
| 구조 변경으로 agent behavior 변동 | sentence/paragraph 포함 protected structure |
| Agent-facing 반복 guard 삭제 | repetition을 behavior-sensitive로 취급 |
| validator가 optimizer보다 비싸짐 | local candidate scan + one-pass bounded check |
| whole-document rewrite로 drift 증가 | local edit + no whole-document regeneration |
| embedding score가 false confidence 제공 | universal metric gate 금지 |
| Skill body가 Research를 복제해 비대해짐 | rationale는 inbox, runtime contract만 canonical |
| 기존 Skill과 responsibility overlap | trigger near-miss + explicit boundary |
| route family 과설계 | families unchanged + uncategorized discovery |
| eval fixture 과적합 | outcome contract + utility baseline + evidence level 분리 |
| 안정화 명목으로 텍스트가 길어짐 | default no-expansion, explicit stabilization에서만 작은 trade-off 허용 |

## Deferred decisions

다음은 이번 구현에서 고정하지 않는다.

- 향후 `text` route family 승격 여부
- target별 추가 metadata
- reference 분리 여부
- deterministic token counter
- Promptfoo adapter 또는 generic eval runner
- regression contract 승격
- 특정 tokenizer 최적화 mode
- compression intensity argument

실제 implementation/eval evidence가 필요성을 만들 때만 별도 Research/Plan으로 연다.

## Review loop ledger

이 Plan은 RPI hard ceiling인 30개 substantive Review concern까지 검토했다. 각 항목은 실제 계획 결정을 추가·축소·확정했으며, 숫자를 채우기 위한 no-op 반복은 포함하지 않는다.

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
12. generic response brevity와 existing-text optimization activation 분리
13. Agent-facing duplicate/repetition의 behavioral risk
14. transform resilience claim의 보장 범위 제한
15. 신규 `text` family의 YAGNI 판단
16. trigger fixture를 real text-transform intent 중심으로 조정
17. behavior fixture에 repetition-preservation case 추가
18. Skill 없이/함께 utility baseline 필요성
19. core `SKILL.md`에서 semantic anchor taxonomy 축약
20. 전체 semantic inventory 대신 candidate-local preservation
21. whole-document regeneration 금지
22. user/domain canonical terminology 보존
23. stabilization과 text-cost trade-off
24. style/register를 optimization objective로 끌어오지 않는 경계
25. Agent Asset owner와 optimizer의 composition/evidence 경계
26. safe case reduction과 risky case no-op를 함께 acceptance로 설정
27. sentence boundary를 protected structure에 포함
28. optimizer 전용 wrapper/output format 강제 금지
29. tokenizer 미실행 시 exact token claim 금지
30. 초기 routing을 `uncategorized`로 수렴하고 family 변경을 deferred로 이동

Hard ceiling에 도달했으므로 Plan 단계의 추가 recursion은 종료한다. 이후에는 구현에서 새로운 evidence나 failure가 생길 때만 새 Review loop를 연다.

## Implementation handoff

다음 작업은 **Phase 1 — Canonical Skill**에서 시작한다.

첫 변경은 `SKILL.md` 하나여야 한다. 그 초안이 responsibility, activation, preservation, runtime-cost와 protected-structure contract를 충분히 표현하지 못한다는 실제 근거가 나오기 전에는 reference, helper, 별도 family 또는 evaluator framework를 추가하지 않는다.

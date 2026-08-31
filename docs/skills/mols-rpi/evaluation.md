---
description: mols-rpi의 Trigger와 Behavior eval을 분리해 설계하고 Promptfoo fixture·provider·grader·runtime evidence를 유지보수할 때 사용하는 문서입니다.
---

# Mols RPI Evaluation

이 문서는 `mols-rpi`의 **eval 설계와 유지보수 결정**을 소유합니다.

Runtime behavior의 canonical source는 `src/rulesync/.rulesync/skills/mols-rpi/SKILL.md`, behavioral contract와 case는 `evals/skills/mols-rpi/cases.json`이 소유합니다. Promptfoo는 이 contract를 실행하고 채점하는 backend이며 별도의 behavior authority가 아닙니다.

## Evaluation Model

`mols-rpi`는 **Trigger**와 **Behavior**를 별도 suite로 평가합니다. 둘을 한 run에서 실행할 수 있지만 같은 system under evaluation로 취급하지 않습니다.

| Suite | System under evaluation | Input context | Observable result | Primary grader |
| --- | --- | --- | --- | --- |
| Trigger | Skill discovery metadata와 routing prompt | 사용자 요청 + `SKILL.md` frontmatter | `activation: true/false` | deterministic Python assertion |
| Behavior | 이미 activation된 `mols-rpi` runtime contract | 사용자 scenario + full `SKILL.md` | assistant response | semantic rubric + output contract |
| Smoke | Promptfoo config/generator/provider/assertion plumbing | fixture-mode output | 연결과 schema가 정상인지 | deterministic assertion |

Trigger suite는 **Skill body를 보지 않습니다**. Behavior suite는 **activation을 다시 판단하지 않습니다**. 이 분리가 무너지면 routing 품질과 instruction-following 품질의 원인을 구분하기 어려워집니다.

Smoke는 runtime behavior evidence가 아닙니다.

## Trigger Suite

Trigger eval은 `mols-rpi`가 **선택되어야 하는 요청과 선택되면 안 되는 요청을 구분하는지** 측정합니다.

Positive coverage에는 다음을 우선합니다.

- 명시적인 RPI·loop·recursive improvement intent
- RPI라는 단어가 없어도 Research, Plan, consequential Work와 반복 검증이 materially coupled된 복합 작업

Negative coverage에는 다음을 우선합니다.

- `loop`가 주제, 식별자 또는 code concept일 뿐인 요청
- 내용 단순 반복
- 길기만 한 작업
- explicit prerequisite control이 이득을 주지 않는 trivial work

Trigger provider는 frontmatter만 받고 `activation` boolean만 반환합니다. 일반 답변을 함께 생성하지 않는 이유는 **분류 외 token과 behavior contamination을 제거하기 위해서**입니다.

Promptfoo metric은 positive와 negative를 분리합니다.

- `trigger-activation` — activation이 필요한 case
- `trigger-rejection` — activation하면 안 되는 case

정확한 activation label은 deterministic하게 판정할 수 있으므로 model grader에 맡기지 않습니다.

## Behavior Suite

Behavior eval은 **routing이 이미 성공했다고 가정**합니다. Provider는 full `SKILL.md`를 적용해 scenario에 답하고, activation 여부는 다시 결정하지 않습니다.

Core runtime selection은 다음 축에서 대표 case를 고릅니다.

- task-specific Skill 또는 governing workflow와의 composition
- Research → Plan → Work prerequisite
- Scope narrowing·expansion과 fixed boundary
- Loop accounting과 handoff
- recursion의 strict-subset Scope와 authority
- retrieved evidence와 operational authority
- adaptive Research와 Review challenge reconciliation
- public override와 intensity
- domain Work와 RPI orchestration stage 구분

`cases.json`에는 core runtime selection보다 더 넓은 regression/capability case를 유지할 수 있습니다. Promptfoo default runtime set은 모든 case를 의무적으로 실행하는 inventory가 아니라 **높은 signal의 대표 suite**입니다.

### Grading

Behavior output에는 두 종류의 assertion을 적용합니다.

1. **Output contract** — 빈 응답 같은 plumbing failure를 deterministic하게 차단합니다.
2. **Behavior contract** — fixture의 repository-owned assertions를 `llm-rubric`으로 평가합니다.

Rubric은 다음을 지킵니다.

- observable response만 평가
- hidden reasoning이나 exact wording을 요구하지 않음
- contract가 요구하지 않는 하나의 trajectory를 강제하지 않음
- required gate를 건너뛰거나 forbidden action에 동의하면 실패
- 수행하지 않은 tool action을 수행했다고 주장해 contract를 위반하면 실패

`llm-rubric`에는 explicit threshold를 둡니다. Promptfoo에서는 judge가 `pass`를 생략하는 경우 threshold가 없으면 낮은 score라도 pass가 될 수 있으므로, `behavior-contract`는 score와 pass를 함께 요구하는 설정을 사용합니다.

Model grader failure는 target failure와 구분합니다. Transport, parse, grader context 문제로 채점하지 못한 경우 assistant behavior가 실패했다고 단정하지 않습니다.

## Promptfoo Projection

Repository-owned fixture를 Promptfoo 전용 fixture로 복제하지 않습니다.

`evals/promptfoo/mols-rpi.yaml`은 같은 Python generator를 두 번 호출합니다.

- `suite: trigger` → `mols-rpi-trigger` provider만 실행
- `suite: behavior` → `mols-rpi-behavior` provider만 실행

Generator는 각 test에 다음 metadata를 붙입니다.

- `suite`
- `mode`
- `case_id`
- canonical fixture path

Promptfoo의 test-level provider filter가 서로 다른 provider의 cartesian product를 막고, `metadata.suite`는 suite별 선택 실행에 사용됩니다.

## Entrypoints

```bash
mise run eval-mols-rpi-smoke
mise run eval-mols-rpi
mise run eval-mols-rpi-trigger
mise run eval-mols-rpi-behavior
```

- `eval-mols-rpi-smoke` — fixture/provider/assertion plumbing만 확인
- `eval-mols-rpi` — default Trigger + Behavior runtime suite
- `eval-mols-rpi-trigger` — metadata filter로 Trigger만 실행
- `eval-mols-rpi-behavior` — metadata filter로 Behavior만 실행

Runtime model은 `PROMPTFOO_RUNTIME_MODEL`, model grader는 `PROMPTFOO_GRADER_PROVIDER`로 선택합니다. 서로 다른 model/runtime을 비교할 때는 다른 조건도 결과를 왜곡하지 않도록 맞추고 사용한 조건을 함께 기록합니다.

## Trial and Stability

Promptfoo의 repeat는 **runtime Trial**입니다. RPI의 Loop나 validator Review Loop와 같은 개념이 아닙니다.

반복 Trial은 stochastic stability가 실제 질문일 때 사용합니다. 단순히 case 수나 호출 수를 늘리기 위해 repeat를 높이지 않습니다. Model, runtime, prompt, tool access 또는 grader가 달라지면 같은 점수 이름이라도 동일한 measurement라고 가정하지 않습니다.

Default suite는 비용과 signal을 균형 있게 유지하고, 더 넓은 case 또는 반복 Trial은 특정 regression·stability 질문이 있을 때 선택합니다.

## Case Maintenance

새 case는 실제 behavior 또는 failure mode를 보호할 때만 추가합니다.

1. 먼저 Trigger인지 Behavior인지 결정합니다.
1. 기존 case가 같은 failure를 이미 보호하는지 확인합니다.
1. prompt는 정상적인 Agent가 해결 가능한 scenario로 작성합니다.
1. assertion은 observable behavior와 금지 behavior를 적고, 특정 문구나 구현 세부에 과적합하지 않습니다.
1. Trigger case는 positive와 negative/near-miss 균형을 확인합니다.
1. Behavior case는 outcome을 우선하고, trajectory 자체가 contract일 때만 중간 gate를 assertion으로 둡니다.
1. 반복된 runtime failure가 안정적인 contract로 확인된 경우 regression defense로 승격합니다.

Fixture를 target runtime에 노출하지 않습니다. Target provider는 prompt와 실제 Skill contract만 보고, assertion은 grading 단계에서만 사용합니다.

## Failure Triage

Unexpected FAIL 또는 PASS에서는 먼저 어느 layer가 결과를 만들었는지 분리합니다.

| Layer | 확인할 것 |
| --- | --- |
| Fixture | prompt와 expected contract가 실제 Skill 의도와 맞는가 |
| Trigger provider | frontmatter만 사용했는가, activation label이 잘못됐는가 |
| Behavior provider | full Skill을 적용했는가, routing을 재수행하지 않았는가 |
| Runtime/model | model-specific instruction following 또는 structured output failure인가 |
| Grader | rubric context, parse, threshold 또는 judge variance 문제인가 |
| Adapter/config | provider filtering, metadata, schema, generator projection이 잘못됐는가 |

원인을 분리하지 않은 채 Skill을 eval에 맞추지 않습니다.

## Evidence Boundary

- deterministic repository tests 통과 → fixture/config/adapter correctness evidence
- Promptfoo fixture smoke 통과 → Promptfoo integration plumbing evidence
- Trigger runtime eval → 해당 model/runtime의 routing evidence
- Behavior runtime eval → 해당 model/runtime과 grader 조건의 behavioral evidence
- 여러 independent Trial → 그 조건에서의 stability evidence

실제로 실행하지 않은 runtime, model 또는 Trial을 통과했다고 표현하지 않습니다. Generated Promptfoo result는 기본적으로 disposable evidence이며, durable contract는 `cases.json`, canonical Skill 또는 필요한 maintainer decision에만 반영합니다.

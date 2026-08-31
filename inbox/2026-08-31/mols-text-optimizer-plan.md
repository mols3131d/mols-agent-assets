# `mols-text-optimizer` 구현 계획

이 문서는 [`mols-text-optimizer-research-plan.md`](mols-text-optimizer-research-plan.md)의 조사 결과를 실제 Skill 생성 작업으로 수렴시킨 **구현 Plan**이다. Research는 근거를 소유하고, 구현 순서와 acceptance는 이 문서가 소유한다.

목표는 **구조를 건드리지 않고 의미와 기능을 보존하면서 기존 텍스트의 wording 비용을 줄이는 최소 Skill**을 만드는 것이다.

## 완료 상태

다음이 충족되면 이번 작업은 완료다.

- `src/rulesync/.rulesync/skills/mols-text-optimizer/SKILL.md`가 canonical source로 존재한다.
- Skill은 제공된 텍스트를 의미 보존 조건에서 경량화하려는 요청에 선택된다.
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

실제 implementation/eval evidence 없이 보조 구조를 추가하지 않는다.

## Skill 책임

`mols-text-optimizer`의 책임은 하나다.

> **주어진 텍스트의 material meaning과 기능을 유지하는 범위에서 불필요한 wording 비용을 제거한다.**

Semantic stability는 별도 기능이 아니라 **optimization constraint**다. 더 짧아진 결과가 더 모호하거나 후속 변환에서 의미가 갈라지기 쉬워지면 그 축약을 하지 않는다.

이 Skill만으로 번역·재생성·요약·압축 이후 의미 동일성을 보장한다고 주장하지 않는다. 원문 wording에서 제거 가능한 ambiguity, synonym churn과 불필요한 표현 변이를 늘리지 않는 것이 범위다.

## Activation

### 선택한다

다음 두 조건 중 하나가 필요하다.

1. 사용자가 **대상 텍스트를 제공하거나 명확히 지칭**하고, 의미를 유지한 경량화·축약·중복 제거·wording/token 최적화를 요청한다.
2. 사용자가 `mols-text-optimizer` 사용을 명시한다.

대표 intent:

- "의미는 그대로 두고 이 문장을 줄여줘"
- "이 instruction을 기능 훼손 없이 가볍게 해줘"
- "중복 표현만 제거해서 token 비용을 줄여줘"
- "semantic drift가 늘지 않는 범위에서 이 wording을 압축해줘"

### 선택하지 않는다

- "앞으로 짧게 답해", "간결하게 설명해"
- 핵심만 남기는 요약
- 번역
- 맞춤법/문법 교정만 필요한 작업
- AI 티 제거, 자연스러운 문체, tone/voice 개선
- Markdown section/heading/list/table 또는 읽기 흐름 개선
- caveman/원시인 style
- latent prompt/context compressor 구현

텍스트가 존재한다는 사실만으로 activation하지 않는다. **optimization intent가 있어야 한다.**

## `SKILL.md` 설계

Single-file Skill로 시작한다. Body는 다음 계약만 복원할 수 있으면 된다.

```text
Condition → Optimize → Preserve → Check / Stop
```

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

- 제공 text의 의미 보존 축약
- instruction의 기능 보존 경량화
- 제공 text의 중복 wording 제거
- 명시적인 `mols-text-optimizer` 요청

Negative / near-miss:

- generic brevity
- summarization
- translation
- humanization
- Markdown restructuring
- caveman style
- latent prompt compressor

Keyword 목록이 아니라 실제 사용자 표현 variation을 사용한다.

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
- fixture 내용의 semantic quality는 Review가 소유한다.
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

## 작업 순서

### 1. Canonical Skill 작성

- directory와 `SKILL.md`를 만든다.
- description에서 positive trigger와 가까운 near-miss를 구분한다.
- body는 `Optimize / Preserve / Check / Boundary` 중심으로 최소화한다.
- Research의 논문·근거 설명은 복사하지 않는다.
- reference/helper는 만들지 않는다.

### 2. Authoring self-review

`mols-agent-asset` 기준으로 확인한다.

- 정말 신규 responsibility인가?
- generic brevity, summarization, Markdown, humanization, caveman과 겹치지 않는가?
- activation이 target text + optimization intent에 묶여 있는가?
- preservation rule이 reduction보다 우선하는가?
- structure를 owner 밖에서 변경하지 않는가?
- always-loaded body가 불필요하게 장황하지 않은가?
- model/tokenizer별 가정을 portable contract로 만들지 않았는가?

### 3. Eval fixture 작성

- trigger positive/near-miss를 작성한다.
- behavior safe-reduction/no-op/invariant case를 작성한다.
- exact output wording에 과적합하지 않았는지 확인한다.

### 4. Repository integration

- 필요한 Markdown formatting을 적용한다.
- Rulesync source validation을 수행한다.
- `mise run generated-sync`로 distribution route를 갱신한다.
- `route/skills.jsonl`에 신규 Skill이 들어갔는지 확인한다.

### 5. Verification

- `mise run check`
- `mise run test`
- 필요할 때만 target-specific Rulesync preview/validate
- 가능한 경우 behavioral capability eval

실행하지 못한 검증은 성공으로 추론하지 않는다.

### 6. Final review

다음 finding이 있을 때만 수정한다.

- false trigger / missed trigger
- safe case에서 실질적 reduction이 없음
- semantic 또는 behavioral invariant 손실
- structure mutation
- aggressive compression
- unnecessary context/steps
- sibling responsibility overlap
- fixture overfitting

새 기능이나 package 구조는 review finding 없이 추가하지 않는다.

## Acceptance

### Skill contract

- [ ] responsibility가 wording optimization 하나로 제한된다.
- [ ] activation이 target text + optimization intent 또는 explicit invocation으로 제한된다.
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
- [ ] `.agents/route/`를 이번 작업에서 변경하지 않는다.
- [ ] deterministic checks 결과를 기록한다.
- [ ] 실행하지 않은 runtime behavior를 통과했다고 주장하지 않는다.

## 리뷰 정리

### 구현 전에 반영 완료

| Finding | 결정 |
| --- | --- |
| `.agents/route/uncategorized` 자동 노출 가정 오류 | repository-local route를 범위에서 제거하고 distribution route만 사용 |
| semantic stabilization이 별도 capability로 확장될 위험 | stability를 optimization constraint로 축소 |
| activation이 "텍스트가 존재함"만으로 너무 넓음 | target text + optimization intent 또는 explicit invocation으로 제한 |
| whole-document regeneration 금지가 output 방식까지 제한 | `local edit scope` 보호로 재정의 |
| target metadata가 미정 | portable 6 targets를 초기값으로 고정 |
| eval deterministic evidence 과장 | JSON validity와 behavioral evidence를 분리 |

### 구현 중 확인

- description이 sibling near-miss를 실제로 구분하는가?
- safe reduction과 risky no-op가 둘 다 가능한가?
- preservation instruction이 너무 많아 context 비용을 키우지 않는가?
- Agent-facing text에서 duplicate-removal이 behavior를 약화시키지 않는가?
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

다음 작업은 **`SKILL.md` 초안 생성**이다. 첫 implementation은 canonical Skill 하나만 만들고, 그 초안의 실제 부족함이 확인되기 전에는 다른 package resource를 추가하지 않는다.

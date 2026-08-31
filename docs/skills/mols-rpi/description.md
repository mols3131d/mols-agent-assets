---
description: mols-rpi frontmatter description의 Trigger·routing 필수 신호, 보조 신호와 1,024자 압축 경계를 유지보수할 때 사용하는 문서입니다.
---

# Mols RPI Description

이 문서는 `mols-rpi`의 frontmatter `description`이 **어떤 routing signal을 반드시 보존해야 하는지** 소유합니다.

Runtime behavior는 `src/rulesync/.rulesync/skills/mols-rpi/SKILL.md`, behavioral eval은 `evals/skills/mols-rpi/cases.json`, Promptfoo 실행 설계는 [Evaluation](evaluation.md)이 소유합니다. 이 문서는 description 문구 자체를 고정하지 않고 **선택 경계와 압축 우선순위**를 고정합니다.

## Portability Contract

- Parsed `description`은 **최대 1,024 characters**로 유지합니다.
- 길이는 YAML source의 물리적 줄 수가 아니라 folded scalar를 해석한 최종 문자열을 기준으로 계산합니다.
- Source 줄바꿈은 문장이나 의미 단위에 둡니다. 기계적인 hard-wrap을 contract로 만들지 않습니다.
- 1,024자를 맞추기 위해 required routing signal을 body로 밀어내거나 더 많은 추론이 필요한 모호한 표현으로 바꾸지 않습니다.

## Two-Tier Model

`description`의 내용은 두 tier로 분류합니다.

| Tier | 의미 | 변경 원칙 |
| --- | --- | --- |
| **Tier 1 — Required** | 빠지거나 흐려지면 Trigger recall, precision 또는 composition safety가 materially 달라질 수 있는 routing contract | 의미를 삭제하지 않습니다. 문구는 압축할 수 있지만 같은 decision boundary를 유지해야 합니다. |
| **Tier 2 — Supporting** | Tier 1의 판정을 돕는 lexical example, rationale 또는 추가 설명 | 중복 제거와 압축을 먼저 적용합니다. 삭제 후에도 Tier 1 판정과 eval coverage가 유지되어야 합니다. |

`High`/`Low`처럼 중요도를 추상적으로 표현하기보다 **Required / Supporting**을 사용합니다. Supporting은 불필요하다는 뜻이 아니라, 1,024자 budget에서 먼저 최적화할 수 있다는 뜻입니다.

## Tier 1 — Required

### Capability Identity

Description만 읽어도 `mols-rpi`가 **adaptive RPI orchestration**이며 Research → Plan → Implementation/Work → Review의 prerequisite 관계와 반복적 개선을 다룬다는 점을 구분할 수 있어야 합니다.

단순히 긴 작업을 처리하는 일반 workflow로 보이게 만들면 안 됩니다.

### Explicit Method Intent

사용자가 RPI 또는 iterative/recursive loop 방법 자체를 요청하면 활성화될 수 있어야 합니다.

반드시 보존할 의미 범주:

- RPI / RPI(R)
- loop / 루프 계열의 **method intent**
- recursive improvement / 재귀 개선 계열
- improvement 또는 deep loop처럼 반복 개선 강도를 명시한 동등한 요청

모든 철자·언어 variant를 전부 열거할 필요는 없지만, 대표 lexical signal을 지나치게 제거해 explicit recall을 낮추면 안 됩니다.

### Implicit Complex-Work Activation

RPI나 loop라는 단어가 없어도 **single pass가 materially unreliable한 작업**은 활성화될 수 있어야 합니다.

Description은 적어도 다음 decision signal을 전달해야 합니다.

- consequential decision 전에 evidence gathering 또는 reconciliation이 필요함
- consequential Work 전에 명시적인 Plan이 필요함
- 여러 acceptance condition 또는 coupled workstream을 수렴시켜야 함
- repeated verification 또는 likely replanning이 필요함
- narrower subproblem resolution이 materially useful함
- hidden assumption 또는 uncertainty 때문에 단일 pass가 costly rework를 만들 위험이 큼

이 목록의 문구를 모두 그대로 유지할 필요는 없지만, 압축된 상위 표현이 이 activation boundary를 실제로 포괄해야 합니다.

### Negative Precision

다음은 `mols-rpi` activation 이유가 되어서는 안 됩니다.

- `loop`가 주제, identifier 또는 code concept일 뿐인 경우
- iterative work intent가 없는 단순 반복 요청
- 작업이 단지 길다는 이유
- explicit prerequisite control이 의미 있는 이득을 주지 않는 trivial work
- bounded one-shot answer/review로 충분하고 RPI prerequisite control이 materially 필요하지 않은 경우

Negative boundary는 explicit trigger recall과 같은 수준으로 중요합니다. 강한 orchestration Skill의 false positive는 불필요한 artifact, Research, Plan과 Review를 만들어 추론비용과 작업비용을 높일 수 있습니다.

### Composition Boundary

더 구체적인 workflow 또는 governing context가 task lifecycle, gates, state 또는 required procedure를 소유하면 그 owner가 controlling이어야 합니다.

`mols-rpi`는 compatible하고 materially useful할 때 compose할 수 있지만, 그 owner의 lifecycle을 경쟁적으로 대체하거나 권한을 덮어쓰면 안 됩니다.

이 경계가 사라지면 RPI가 task-specific workflow를 과도하게 감싸거나 orchestration authority를 탈취할 수 있으므로 Tier 1입니다.

## Tier 2 — Supporting

다음은 routing signal을 강화하지만 Tier 1의 의미가 이미 명확하다면 축약·통합할 수 있습니다.

- `loop`, `loops`, `loop it`처럼 같은 intent의 추가 lexical variant
- explicit trigger의 모든 한국어·영어 동의어 열거
- `bounded serial recursion`처럼 activation보다 runtime 구현을 더 자세히 설명하는 수식어
- implicit activation의 각 원인을 별도 문장으로 반복하는 rationale
- lifecycle / gates / state / procedure를 모두 장황하게 열거하는 표현
- `replace`, `wrap`, `override`처럼 같은 composition 위험을 여러 동사로 반복하는 표현
- 이미 더 상위 decision signal이 소유하는 illustrative example

Tier 2를 제거할 때는 단순 token 절감이 아니라 **routing signal density가 유지되거나 높아지는지**를 봅니다.

## Compression Order

1,024자 budget을 맞출 때 다음 순서를 지킵니다.

1. Tier 2의 순수 중복을 삭제합니다.
2. 남은 Tier 2를 더 짧은 상위 표현으로 통합합니다.
3. Tier 1의 문구를 압축하되 decision boundary는 그대로 유지합니다.
4. Tier 1을 삭제해야만 1,024자를 맞출 수 있다면 표현 구조를 다시 설계합니다. Required signal을 body로 넘겨 budget을 맞추지 않습니다.
5. 마지막에 semantic line break를 정리하고 parsed length를 다시 계산합니다.

짧아졌지만 모델이 implicit activation, negative boundary 또는 composition owner를 더 많이 추론해야 한다면 성공한 압축이 아닙니다.

## Validation

Description 변경은 최소한 다음을 함께 확인합니다.

- parsed length ≤ 1,024 characters
- explicit RPI / recursive-loop positive
- keyword-free complex-work positive
- loop topic과 identifier negative
- generic repetition negative
- long-but-one-pass negative
- one-shot negative
- trivial-work negative
- 더 구체적인 controlling workflow와의 composition boundary

Trigger eval은 wording 자체가 아니라 이 decision boundary를 보호해야 합니다. Description을 eval case에 맞춘 lexical password처럼 최적화하지 않습니다.

## Boundary

- Skill runtime behavior → `SKILL.md`
- Trigger/Behavior behavioral contract → `evals/skills/mols-rpi/cases.json`
- Promptfoo suite와 grader/runtime evidence → [Evaluation](evaluation.md)
- repository-wide Skill description convention → [Skill Authoring Conventions](../../references/agent-assets/skills/skill-authoring-conventions.md)
- field limit와 vendor-specific discovery behavior → [Agent Skills Specification](../../references/agent-assets/skills/specification.md)에서 applicable official source로 resolve

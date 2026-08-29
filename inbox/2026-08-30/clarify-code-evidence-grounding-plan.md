# Clarify Code — Evidence Grounding Plan

Based on: [Clarify Code — Evidence Grounding Research](clarify-code-evidence-grounding-research.md)

이 Plan은 기존 comment-recall 보정을 유지하면서 fabricated rationale를 막고 Progressive Disclosure를 복원하기 위한 후속 RPI 구현 범위를 고정합니다.

## Goal

`clarify-code`가 다음 행동을 안정적으로 수행하게 합니다.

- 필요한 durable explanation을 사용자가 `comment`라고 직접 말하지 않아도 발견하고 생성
- explanation의 semantic claim을 current evidence로 확인
- 근거가 부족하면 그럴듯한 rationale를 invent하지 않음
- common path는 `SKILL.md`만으로 판단 가능
- tricky placement/projection/machine-consumed case에서만 `documentation.md`를 읽음

## Active Scope

### In scope

- `src/rulesync/.rulesync/skills/clarify-code/SKILL.md`
- `src/rulesync/.rulesync/skills/clarify-code/references/documentation.md`
- `evals/skills/clarify-code/cases.json`
- follow-up Review artifact
- PR description/status record

### Out of scope

- `code-comprehension-refactor` behavior 변경
- `clarify-code` frontmatter `description` 변경
- generated route 변경
- 새 deployable reference 추가
- comment quality score/analyzer
- model/runtime eval infrastructure 생성
- user-facing documentation

## Preserve

다음은 기존 behavior로 유지합니다.

1. executable code는 변경하지 않음
2. structural opacity는 `code-comprehension-refactor`로 handoff
3. hidden caller contract → docstring
4. maintainer invariant/constraint/consequence/rationale → comment
5. obvious narration과 comment-density 목표 금지
6. machine-consumed text의 observable/tooling contract 보존
7. durable positive signal이 실제로 있으면 no-op으로 회피하지 않음

## Change 1 — Core에 `Evidence before Explanation`

### `SKILL.md` workflow

현재 positive obligation 직후에 evidence gate를 둡니다.

Behavior:

1. candidate contract/invariant/constraint/consequence/rationale를 찾음
2. target behavior, caller, tests, canonical contract/spec, current config/protocol 중 필요한 가장 좁은 evidence를 읽음
3. current evidence가 semantic claim을 지지할 때만 source explanation으로 고정
4. historical discussion은 supporting context일 뿐 current authority로 자동 승격하지 않음
5. reason을 확정할 수 없으면 plausible rationale를 만들지 않고 no-op/report 가능

### Read vs write scope

`--scope` 설명과 workflow에서 다음을 명확히 합니다.

- mutation은 target/source explanation surface로 제한
- evidence 확인을 위해 caller/test/spec/config를 읽을 수 있음
- evidence read는 write authority를 넓히지 않음

새 argument는 만들지 않습니다.

## Change 2 — Positive Signals를 core로 이동

현재 `documentation.md`의 `Positive Signals`는 comment recall에 필수이며 reference를 항상 읽게 만든 핵심 원인입니다.

`SKILL.md`에 compact table로 이동합니다.

| Signal | Default surface |
| --- | --- |
| hidden caller contract / call semantics | docstring |
| maintainer invariant / local constraint | comment |
| ordering/failure consequence | comment |
| external system/protocol constraint | comment |
| durable rejected alternative | comment |
| stable file-local convention | module-level explanation |

Core에는 상세 예시나 taxonomy를 넣지 않습니다.

`documentation.md`에서는 같은 목록을 반복하지 않고 core signal을 전제로 세부 quality/placement만 소유합니다.

## Change 3 — Owner before Nearness

현재 positive obligation의 "같은 의미가 가까운 surface에 없다"를 다음 의미로 보정합니다.

- 같은 semantic이 **적절한 owner에 충분히 존재하는지** 먼저 확인
- broad owner가 있어도 local caller/maintainer projection이 실제로 필요하면 설명 가능
- placement 단계에서 가장 가까운 적절한 stable surface를 선택

이렇게 broad policy duplication과 locality hard-rule 오해를 줄입니다.

## Change 4 — `documentation.md`를 conditional reference로 복원

Reference의 common-path positive signal은 core로 이동/삭제합니다.

Reference는 다음 경우에만 읽습니다.

- explanation placement/scope 또는 semantic owner가 불명확
- canonical contract의 local projection을 판단해야 함
- rejected alternative/history/staleness가 얽힘
- module-level explanation 여부가 애매함
- machine/runtime/tool-consumed text를 수정할 가능성이 있음

Common docstring/comment 선택만으로는 reference를 강제하지 않습니다.

## Change 5 — Documentation의 grounding detail

`documentation.md`에 짧은 `Grounding` section을 둡니다.

핵심:

- explanation은 current evidence의 projection
- current invariant와 historical rationale를 구분
- current behavior만 확인 가능하면 확인 가능한 의미만 씀
- Git history/issue는 candidate context이며 current evidence로 revalidate
- unsupported uncertainty를 permanent comment로 만들지 않음

별도 evidence hierarchy, score 또는 citation syntax는 만들지 않습니다.

## Change 6 — Capability eval 보강

기존 case를 유지하되 fixture 수를 불필요하게 늘리지 않습니다.

### `implicit-maintainer-comment-discovery` 개선

현재 prompt가 invariant를 직접 설명합니다. 이를 **nearby regression test/caller evidence에서 invariant를 복원해야 하는 형태**로 교체합니다.

Expected:

- comment라는 직접 요청 없이 evidence를 연결해 hidden ordering consequence 발견
- code-local comment 실제 생성/개선
- executable code 변경 없음

### 신규 `unsupported-rationale-no-fabrication`

Prompt shape:

- unusual implementation 존재
- user는 maintainability clarification 요청
- caller/tests/spec/config 어디에도 rationale evidence 없음

Expected:

- plausible rationale invent 금지
- unsupported source comment 추가 금지
- executable code 변경 금지
- 필요하면 evidence gap report/no-op

### Existing precision cases 유지

- `obvious-comment-request`
- `no-net-value-comment`
- `structural-problem-boundary`
- `selective-positive-comment`

이 네 case가 positive obligation의 과잉 확대를 막습니다.

## Review Gates

### Grounding

- comment/docstring의 non-obvious semantic claim이 current evidence에 의해 지지되는가?
- history나 unusual code appearance를 rationale proof로 오인하지 않는가?
- evidence가 부족할 때 uncertainty를 source comment로 굳히지 않는가?

### Recall

- evidence-backed hidden meaning이 있는데 no-op으로 회피하지 않는가?
- 사용자가 comment를 직접 요청하지 않아도 correct surface를 선택하는가?

### Precision

- obvious narration을 추가하지 않는가?
- unsupported rationale를 만들지 않는가?
- broad canonical policy를 local comment에 복제하지 않는가?

### Responsibility

- executable code를 변경하지 않는가?
- evidence read가 write scope 확대를 의미하지 않는가?
- structural problem은 sibling Skill에 남는가?

### Context Economy

- common path가 core만으로 실행 가능한가?
- `documentation.md`가 실제 conditional detail만 소유하는가?
- Positive Signals가 core/reference에 중복 정의되지 않는가?

## Validation

1. `SKILL.md`와 `documentation.md` semantic owner review
2. `code-comprehension-refactor` boundary 재대조
3. eval positive/negative/near-miss review
4. frontmatter 미변경 확인 → route delta 없어야 함
5. latest PR Gate deterministic test
6. runtime/model eval은 실제 capability가 없으면 `not run`

## Acceptance Criteria

- `Evidence before Explanation`이 core behavior contract로 명시됨
- explanation write 전에 필요한 narrow evidence를 읽되 mutation scope는 확대하지 않음
- unsupported rationale를 source에 invent하지 않음
- Positive Signals가 core에 있어 comment recall이 reference load에 의존하지 않음
- `documentation.md`가 실제 conditional reference로 돌아감
- owner correctness가 nearness보다 먼저 판단됨
- evidence-backed discovery와 insufficient-evidence behavior가 eval에 표현됨
- obvious/low-value comment anti-spam boundary가 유지됨
- frontmatter/route/new-reference 변경 없이 bounded diff로 끝남

## Planned Diff

```text
src/rulesync/.rulesync/skills/clarify-code/
├── SKILL.md                         # grounding + core signals + routing
└── references/
    └── documentation.md             # conditional grounding/placement detail

evals/skills/clarify-code/
└── cases.json                       # grounded discovery + no-fabrication

inbox/2026-08-30/
└── clarify-code-evidence-grounding-review.md
```

## Status

Plan accepted for this RPI run. Implementation may proceed only inside this bounded scope.
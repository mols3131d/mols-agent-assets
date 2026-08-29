# Clarify Code — Evidence Grounding Review

## Reviewed

- Research: `clarify-code-evidence-grounding-research.md`
- Plan: `clarify-code-evidence-grounding-plan.md`
- Implementation:
  - `src/rulesync/.rulesync/skills/clarify-code/SKILL.md`
  - `src/rulesync/.rulesync/skills/clarify-code/references/documentation.md`
  - `evals/skills/clarify-code/cases.json`
- Boundary comparison:
  - `src/rulesync/.rulesync/skills/code-comprehension-refactor/SKILL.md`
  - repository Skill/Instruction authoring conventions

## Active Scope

### Goal

기존 comment-recall 보정을 유지하면서 explanation을 current evidence에 grounding하고, fabricated rationale를 방지하며, `documentation.md`의 실제 Progressive Disclosure boundary를 복원합니다.

### In scope

- core positive signal과 evidence gate
- read/write scope boundary
- semantic owner before locality
- conditional reference routing
- evidence-backed / insufficient-evidence capability fixtures

### Out of scope

- executable code mutation
- sibling Skill behavior 변경
- frontmatter description/routing 변경
- 새 deployable reference
- runtime/model eval infrastructure

## RPI Loop Record

### Loop 1 — Research → Plan → Implementation → Review

Research는 기존 recall correction의 false-negative 개선을 유지하되, fabricated rationale 위험을 새 P1으로 확인했습니다.

Implementation은 다음을 적용했습니다.

- `Default Explanation Signals`를 core로 이동
- `Evidence before Explanation` 추가
- current evidence가 지지하는 claim만 source prose로 고정
- unsupported rationale는 invent하지 않음
- owner correctness를 locality보다 먼저 판단
- `documentation.md`를 tricky judgment용 conditional reference로 복원
- `implicit-maintainer-comment-discovery`를 regression-test evidence 기반 case로 변경
- `unsupported-rationale-no-fabrication` 추가

Review에서 `--scope`가 write scope처럼 보이면서 evidence read를 암묵적으로 밖으로 허용하는 문구를 발견했습니다.

Disposition: bounded Work gap. Scope를 확장하지 않고 core wording을 수정했습니다.

### Loop 2 — Implementation → Review

다음을 보정했습니다.

- evidence read도 explicit user/repository scope와 authority 안에서만 수행
- evidence가 scope 밖에 있으면 조용히 확대하지 않고 uncertainty/handoff
- read surface가 write authority를 만들지 않음

Review에서 한 가지 추가 gap을 확인했습니다.

Evidence가 존재해도 test·caller·spec가 서로 충돌하면 한 source를 편의상 골라 permanent comment로 굳힐 수 있었습니다.

Disposition: 기존 grounding Plan 안의 bounded Work gap.

### Loop 3 — Implementation → Review

다음을 보정했습니다.

- conflicting evidence를 편의상 선택하지 않음
- exact claim의 current semantic owner, observable behavior와 applicable contract로 좁게 재확인
- material conflict가 해소되지 않으면 permanent explanation을 만들지 않음
- conflict/indirect evidence가 있을 때 `documentation.md`를 읽도록 routing

최종 Review에서 추가 material gap을 발견하지 않았습니다.

`loops_used: 3`

## Findings and Disposition

### Grounding

**Pass — verified by static inspection; runtime behavior not run.**

Core workflow가 `Evidence before Explanation`을 직접 소유합니다.

Candidate meaning은 target behavior, caller, tests, canonical contract/spec, current config/schema/protocol 같은 current evidence로 확인합니다. Git history/old discussion은 supporting context일 뿐 current invariant의 단독 authority가 아닙니다.

현재 constraint는 확인되지만 historical reason은 확인되지 않으면 현재 의미만 설명하고, rationale가 확정되지 않으면 plausible story를 invent하지 않습니다.

### Comment Recall

**Pass — semantic contract verified; model/runtime execution not run.**

Positive signal은 reference가 아니라 항상 로드되는 core `SKILL.md`에 있습니다.

- hidden caller contract
- maintainer invariant/local constraint
- ordering/failure consequence
- external constraint
- durable rejected alternative
- file-local convention

Evidence-backed durable meaning이 남아 있는데 no-op으로 회피하지 않는 stop condition도 유지합니다.

따라서 이전 recall correction이 grounding 때문에 다시 약화되지는 않았습니다.

### Precision / Anti-spam

**Pass — semantic review.**

기존 negative/near-miss behavior를 유지합니다.

- `obvious-comment-request`
- `no-net-value-comment`
- `structural-problem-boundary`
- `selective-positive-comment`

Comment count는 quality proxy가 아니며, code/name/type이 이미 충분한 경우 prose를 추가하지 않습니다.

### No Fabrication

**Pass — semantic contract and fixture inspection.**

`unsupported-rationale-no-fabrication`은 unusual code shape만으로 caching/performance/race/consistency/permission rationale를 발명하지 못하게 합니다.

Evidence가 없거나 conflict가 해소되지 않은 경우 source comment 대신 uncertainty/report/no-op을 허용합니다.

### Read vs Write Scope

**Pass — static inspection.**

Evidence discovery는 mutation scope보다 넓은 context가 필요할 수 있지만, 적용되는 explicit user/repository scope와 authority를 넘을 수 없습니다. 읽은 surface를 수정할 권한도 생기지 않습니다.

이는 repository `mols-agent-asset`의 read/write boundary와 RPI scope invariants에 부합합니다.

### Progressive Disclosure

**Pass — improved.**

이전 follow-up에서는 comment recall을 높이기 위해 모든 prose 판단에서 `documentation.md`를 읽게 했습니다. 당시 failure evidence에 대한 합리적인 보정이었지만 reference가 사실상 always-loaded가 되었습니다.

이번 loop에서 common-path Positive Signals와 grounding gate를 core로 옮겼습니다.

`documentation.md`는 이제 다음 tricky case에서만 로드됩니다.

- placement/scope/semantic owner ambiguity
- evidence conflict 또는 historical/indirect evidence
- canonical contract projection
- rejected alternative/history/staleness
- module-level explanation
- machine/runtime/tool-consumed text

따라서 supporting resource가 다시 실제 loading boundary를 갖습니다.

### Responsibility Boundary

**Pass — static comparison.**

`clarify-code`는 code-adjacent prose만 변경합니다. Naming, representation, control/state flow, indirection, executable abstraction은 계속 `code-comprehension-refactor` 책임입니다.

Evidence를 찾기 위해 executable code/test를 읽어도 이를 수정하지 않습니다.

### Owner before Nearness

**Pass.**

"가까운 surface에 없으면 comment"라는 단순 조건을 제거했습니다.

현재 순서는 다음입니다.

1. semantic owner 확인
2. local projection 필요 여부 판단
3. 필요한 경우 실제 scope에 가까운 stable surface 선택

Broad policy duplication과 locality hard-rule 위험이 감소했습니다.

## Capability Fixture Review

이번 loop에서 실질적으로 달라진 fixture는 두 가지입니다.

| Case | 보호하는 behavior |
| --- | --- |
| `implicit-maintainer-comment-discovery` | regression test evidence에서 hidden consequence를 발견하고 comment 생성 |
| `unsupported-rationale-no-fabrication` | 근거 없는 unusual code에 plausible rationale를 발명하지 않음 |

기존 recall/precision fixture는 그대로 유지합니다.

Fixture는 behavior contract입니다. 실제 model/runtime trial을 실행하지 않았으므로 runtime pass를 주장하지 않습니다.

## Context Economy

**Pass.**

Core `SKILL.md`는 Positive Signals와 evidence gate 때문에 조금 커졌지만, common-path에서 별도 `documentation.md`를 항상 읽던 구조를 제거했습니다. Common behavior에 필수인 contract만 core가 소유하고 세부 판단은 reference가 소유하므로 전체 runtime context 구조는 더 직접적입니다.

새 reference, score, analyzer 또는 taxonomy를 추가하지 않았습니다.

## Validation Evidence

### Verified

- implementation PR Gate — **success, 224 passed**
- Review artifact commit PR Gate — **success, 224 passed**
- final validation-record commit PR Gate — **success, 224 passed**
- frontmatter `description` — unchanged in this loop
- generated route delta — not required by this loop
- Skill/reference/eval static inspection — complete
- sibling responsibility comparison — complete

### Simulated / inferred

- positive signal + evidence gate behavior — semantic simulation/inspection
- unsupported-rationale behavior — fixture and instruction inspection
- conflict evidence behavior — instruction inspection

### Not run

- model/runtime capability eval
- independent agent trial
- Rulesync strict doctor

실행하지 않은 항목을 pass로 주장하지 않습니다.

## Deviations

Plan의 범위를 벗어난 deviation은 없습니다.

Review 중 발견한 explicit-scope와 conflicting-evidence gap은 둘 다 `Evidence before Explanation`의 기존 Plan 책임 안에서 bounded correction으로 해결했습니다.

## Status

**RPI converged after 3 substantive loops.**

현재 상태는 comment recall, factual grounding, anti-spam precision, mutation boundary와 context economy를 동시에 만족합니다. 추가 loop는 model/runtime evidence가 새 failure를 보여주거나 새로운 review evidence가 생길 때만 정당화됩니다.

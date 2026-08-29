# Clarify Code — Enhancement Review

## Reviewed

- Research: `clarify-code-enhancement-research.md`
- Plan: `clarify-code-enhancement-plan.md`
- Implementation:
  - `src/rulesync/.rulesync/skills/clarify-code/SKILL.md`
  - `src/rulesync/.rulesync/skills/clarify-code/references/documentation.md`
  - `evals/skills/clarify-code/cases.json`
- Related boundary owner: `src/rulesync/.rulesync/skills/code-comprehension-refactor/SKILL.md`

## Active Scope

### Goal

`clarify-code`가 code-adjacent prose의 양을 늘리는 대신, explanation의 순가치·정보 유형·배치와 scope를 판단해 실제 이해 비용을 줄이도록 고도화합니다.

### In scope

- `clarify-code` core behavior calibration
- 기존 `documentation.md`의 explanation-value / information-type / placement-scope judgment
- capability fixture 보강

### Out of scope

- executable code refactoring responsibility
- frontmatter routing 확대
- 새 reference package
- comment quality score, analyzer, stale-comment detector
- user-facing standalone documentation

## Implementation Review

### Responsibility

**Pass.**

`clarify-code`는 executable statement, identifier, type/signature, representation, control/state flow와 abstraction을 변경하지 않습니다. Structural opacity는 prose로 보상하지 않고 `code-comprehension-refactor`로 넘깁니다.

반대로 `code-comprehension-refactor`도 comment/docstring-only 요청을 `clarify-code`로 넘기므로 mutation responsibility가 대칭적으로 분리됩니다.

### Explanation Value

**Pass.**

Core workflow가 설명을 추가하기 전에 다음을 보게 합니다.

- code만으로 복원하기 어려운 non-obvious meaning
- 그로 인해 생기는 inference/search/misunderstanding cost
- code/name/type이 이미 충분한지
- explanation이 제거하는 비용이 읽기·유지 비용보다 큰지

No-op, redundant prose 제거와 stale prose 교정도 정상적인 결과로 허용합니다.

### Information Type

**Pass.**

Caller-facing docstring은 hidden contract와 call semantics를, maintainer-facing comment는 current constraint·consequence·rationale를 소유합니다.

`what vs why`의 단순 규칙 대신 invariant, ordering consequence, external constraint와 durable rejected alternative를 구체적인 고가치 정보로 판단합니다.

### Placement and Scope

**Pass.**

Locality를 절대 규칙으로 만들지 않았습니다. 의미의 실제 scope와 semantic owner를 우선하고, 가까운 surface는 불필요한 navigation을 줄이는 수단으로 사용합니다.

- API contract → 해당 docstring
- branch/order local rationale → 해당 code 근처 comment
- file-local stable convention → module-level explanation
- broad architecture/domain policy → canonical owner + 필요한 projection

Non-local/long comment를 기계적으로 제거하지 않는 near-miss boundary도 유지합니다.

### Stability

**Pass.**

Final Pass가 current code/contract/policy와의 모순, volatile identifier·algorithm narration·history coupling과 machine-consumed text를 확인합니다. Stale implementation narration을 polishing하지 않고 durable invariant 중심으로 교정하거나 제거하도록 fixture를 추가했습니다.

### Context Economy

**Pass.**

새 reference를 만들지 않았습니다. 항상 로드되는 `SKILL.md`에는 핵심 calibration만 넣고, 상세 judgment는 기존 `documentation.md`가 소유합니다.

Frontmatter `description`도 이번 enhancement에서 변경하지 않았습니다. 따라서 이번 고도화 때문에 새로운 distribution route projection은 필요하지 않습니다.

## Capability Fixture Review

기존 7개 case를 보존하고 다음 4개를 추가했습니다.

| Case | 보호하는 behavior |
| --- | --- |
| `no-net-value-comment` | comment quantity를 quality proxy로 사용하지 않고 no-op 허용 |
| `durable-rejected-alternative` | current constraint를 useful negative knowledge로 보존 |
| `placement-scope` | local invariant를 module-wide rule로 확대하지 않음 |
| `stale-implementation-narration` | stale narration 대신 current durable meaning을 교정·보존 |

Exact wording이나 특정 comment 형식을 고정하지 않고 judgment와 responsibility boundary를 assertion으로 둡니다.

## Challenge Candidates

### “모든 clarify-code 작업에서 `documentation.md`를 강제로 읽어야 하는가?”

**Disposition: 현재는 강제하지 않음.**

Core가 explanation value, reader split, code-refactor handoff와 stop condition을 이미 소유합니다. Placement, negative knowledge, stability 같은 상세 판단이 불명확할 때 reference를 읽는 현재 progressive-disclosure boundary가 더 작습니다.

실제 eval/runtime evidence에서 reference 미로드로 반복 failure가 확인되면 그때 routing을 강화하는 편이 적절합니다.

### “Local comment는 항상 가까이 둬야 하는가?”

**Disposition: 아니오.**

의미 scope와 owner correctness가 locality보다 우선합니다. 가까움은 navigation cost를 줄이는 기본 heuristic일 뿐 hard rule이 아닙니다.

### “Rejected alternative를 comment에 적극 기록해야 하는가?”

**Disposition: 조건부.**

과거 토론 기록이 아니라, 미래 maintainer가 자연스럽게 다시 시도할 가능성이 높고 현재도 유효한 constraint가 있을 때만 durable negative knowledge로 남깁니다.

## Validation Evidence

- PR Gate: **success**
- deterministic test suite: **224 passed**
- committed route consistency check: PR Gate 안에서 통과
- semantic diff review: `SKILL.md`, `documentation.md`, capability cases, `code-comprehension-refactor` boundary 대조 완료

미실행:

- model/runtime capability eval
- Rulesync strict doctor

미실행 항목을 pass로 주장하지 않습니다.

## Scope Delta

없음. Research/Plan에서 정한 세 파일 변경 범위 안에서 구현했습니다.

## Status

**RPI loop converged.**

현재 acceptance criteria를 충족하며 추가 수정이 필요한 material gap은 발견되지 않았습니다. 후속 loop는 model/runtime eval에서 실제 failure가 나오거나 review에서 새로운 evidence가 생길 때 시작하는 것이 적절합니다.

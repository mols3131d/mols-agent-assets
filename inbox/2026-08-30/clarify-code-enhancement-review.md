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

**Pass, revised in follow-up loop.**

새 reference를 만들지 않았고 상세 judgment는 기존 `documentation.md` 한 곳이 소유합니다. 다만 후속 사용자 관찰에서 필요한 comment를 놓치는 false negative 위험이 확인되어, prose 추가·수정·제거를 실제로 판단하는 `clarify-code` 작업에서는 이 단일 reference를 읽도록 core routing을 강화했습니다.

Frontmatter `description`은 이번 enhancement에서 변경하지 않았습니다. 따라서 이번 고도화 때문에 새로운 distribution route projection은 필요하지 않습니다.

## Capability Fixture Review

초기 고도화에서는 기존 7개 case를 보존하고 다음 4개를 추가했습니다.

| Case | 보호하는 behavior |
| --- | --- |
| `no-net-value-comment` | comment quantity를 quality proxy로 사용하지 않고 no-op 허용 |
| `durable-rejected-alternative` | current constraint를 useful negative knowledge로 보존 |
| `placement-scope` | local invariant를 module-wide rule로 확대하지 않음 |
| `stale-implementation-narration` | stale narration 대신 current durable meaning을 교정·보존 |

후속 comment-recall loop에서는 다음 2개를 추가했습니다.

| Case | 보호하는 behavior |
| --- | --- |
| `implicit-maintainer-comment-discovery` | 사용자가 comment를 직접 요구하지 않아도 hidden ordering invariant를 발견해 comment 생성 |
| `selective-positive-comment` | obvious line은 그대로 두고 durable constraint가 있는 지점에만 comment 생성 |

또한 `durable-rejected-alternative`의 assertion을 `May preserve`에서 **실제 code-local comment를 추가하거나 개선하는 positive obligation**으로 강화했습니다.

Exact wording이나 특정 comment 형식을 고정하지 않고 judgment와 responsibility boundary를 assertion으로 둡니다.

## Challenge Candidates

### “모든 clarify-code 작업에서 `documentation.md`를 강제로 읽어야 하는가?”

**Initial disposition: 강제하지 않음. Superseded by follow-up evidence.**

초기 Review에서는 core가 explanation value, reader split, code-refactor handoff와 stop condition을 이미 소유하므로 상세 판단이 불명확할 때만 reference를 읽는 쪽이 더 작다고 판단했습니다.

후속 사용자 관찰에서 **기존 동작이 필요한 comment를 잘 만들지 않는 경향**이 있었다는 실제 failure evidence가 추가됐습니다. 현재 core는 여러 suppression gate를 갖는 반면 positive comment candidate를 구체적으로 분류하는 정보는 `documentation.md`에 더 많이 있습니다.

따라서 이번 loop에서는 다음으로 변경했습니다.

> docstring, comment 또는 module-level explanation을 추가·수정·제거할지 판단할 때 `Documentation`을 읽는다.

Reference가 하나뿐이고 `clarify-code`의 주된 mutation surface 자체가 code-adjacent prose이므로, 이 경우 recall 개선의 이익이 context cost보다 큽니다.

### “Local comment는 항상 가까이 둬야 하는가?”

**Disposition: 아니오.**

의미 scope와 owner correctness가 locality보다 우선합니다. 가까움은 navigation cost를 줄이는 기본 heuristic일 뿐 hard rule이 아닙니다.

### “Rejected alternative를 comment에 적극 기록해야 하는가?”

**Disposition: 조건부 positive.**

과거 토론 기록이 아니라, 미래 maintainer가 자연스럽게 다시 시도할 가능성이 높고 현재도 유효한 constraint가 있을 때는 durable negative knowledge로 실제 comment를 남기는 쪽을 기본으로 합니다.

## Follow-up RPI Loop — Comment Recall

### New Evidence

사용자 관찰: 개선 전 `clarify-code`가 필요한 상황에서도 주석을 잘 생성하지 않는 경향이 있었습니다.

현재 Skill을 다시 읽어보면 그 실패가 발생할 수 있는 구조적 이유가 있었습니다.

- structural problem handoff
- explanation net-value gate
- redundant prose 제거
- stale prose 제거
- stop/no-op 허용

같은 suppression signal은 여러 곳에서 강하게 표현됐지만, **실행 코드가 이미 적절하고 durable maintainer meaning이 숨겨져 있을 때 실제 comment를 생성한다**는 positive behavior는 상대적으로 약했습니다.

따라서 문제는 “comment가 적어서 나쁘다”가 아니라 **precision에 비해 recall이 낮을 수 있는 instruction asymmetry**로 판단했습니다.

### Plan Delta

기존 scope를 넓히지 않고 다음 세 delta만 적용했습니다.

1. core workflow에 positive obligation 추가
   - executable code가 이미 적절함
   - durable caller/maintainer meaning이 숨겨져 있음
   - 같은 의미가 가까운 surface에 없음
   - 이 조건이면 사용자가 comment/docstring을 직접 요구하지 않아도 explanation 추가·개선을 기본으로 함
2. `documentation.md`에 `Positive Signals` 추가
   - hidden caller contract
   - invariant/local constraint
   - ordering consequence
   - external constraint
   - durable rejected alternative
   - module-local convention
3. capability eval에서 recall과 precision을 한 쌍으로 보호
   - implicit useful comment 생성
   - obvious line에는 comment를 만들지 않고 high-value constraint만 선택

### Review

**Pass.**

Positive obligation은 comment density 목표가 아닙니다. 기존 `obvious-comment-request`, `no-net-value-comment`, structural-problem handoff가 그대로 남아 있어 low-value prose와 structural-problem masking은 계속 억제됩니다.

반대로 `implicit-maintainer-comment-discovery`와 강화된 `durable-rejected-alternative`는 positive condition이 충족됐을 때 no-op으로 빠지는 것을 허용하지 않습니다.

따라서 이번 delta는 “더 많은 comment”가 아니라 **false negative를 줄이는 recall correction**입니다.

## Validation Evidence

초기 RPI loop:

- PR Gate: **success**
- deterministic test suite: **224 passed**
- committed route consistency check: PR Gate 안에서 통과
- semantic diff review: `SKILL.md`, `documentation.md`, capability cases, `code-comprehension-refactor` boundary 대조 완료

Follow-up comment-recall loop:

- semantic review: **pass**
- responsibility / anti-spam boundary review: **pass**
- deterministic PR Gate: 최신 head에서 확인 필요

미실행:

- model/runtime capability eval
- Rulesync strict doctor

미실행 항목을 pass로 주장하지 않습니다.

## Scope Delta

없음. 후속 loop도 기존 세 파일의 behavior calibration과 capability fixture 범위 안에 있습니다. 새 reference, routing description, analyzer 또는 code mutation 권한을 추가하지 않았습니다.

## Status

**Follow-up RPI loop implemented; deterministic validation pending for latest head.**

의미적 review에서는 comment recall을 높이면서 기존 precision boundary를 보존했습니다. 최신 head의 PR Gate 결과를 확인한 뒤 deterministic acceptance를 닫습니다.

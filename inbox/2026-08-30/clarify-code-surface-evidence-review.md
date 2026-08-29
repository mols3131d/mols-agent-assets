# Clarify Code — Surface and Evidence Review

이 문서는 `clarify-code-surface-evidence-research.md`와 `clarify-code-surface-evidence-plan.md`에서 시작한 후속 RPI의 최종 Review 기록입니다.

이 Review가 현재 `clarify-code` 구현 상태에 대한 최신 maintainer review입니다. 이전 `clarify-code-enhancement-review.md`와 `clarify-code-evidence-grounding-review.md`의 중간 결론 중 이후 loop에서 변경된 부분은 이 문서가 supersede합니다.

## Active Scope

### Goal

기존 comment recall, anti-spam, no-fabrication과 executable-code boundary를 유지하면서 explanation surface selection과 evidence authority를 더 정확하게 만들고, 반복 Review에서 발견되는 material gap을 수렴시킵니다.

### In scope

- caller-facing vs maintainer-only surface selection
- cross-language source documentation portability
- explicit current task fact의 evidence 역할
- conflicting evidence의 claim-local 처리
- stale target prose의 circular grounding 방지
- structural concern + independent prose concern 조합
- behavioral fixture coverage
- routing description과 generated distribution route consistency

### Out of scope

- executable code mutation
- `code-comprehension-refactor` behavior 변경
- standalone user-facing documentation
- 새 Skill/reference package
- comment score/analyzer/stale detector
- runtime/model eval infrastructure

## RPI Loop Record

### Loop 1 — Research → Plan → Implementation → Review

Research에서 기존 `Signal → surface` 모델의 모순을 확인했습니다.

`ordering`, `failure consequence`, `external protocol constraint`는 information type만으로 comment인지 caller documentation인지 결정할 수 없습니다. 같은 의미도 caller가 사용 전에 알아야 하면 declaration documentation이고, maintainer-only implementation constraint라면 local comment입니다.

Go, Rust, Java의 caller-facing documentation이 Python docstring과 다른 syntax를 사용하므로 portable responsibility를 Python `docstring`에 고정할 수도 없었습니다.

Implementation:

- surface owner를 `reader + semantic scope`로 변경
- caller-facing source documentation을 language/repository-native surface로 일반화
- explicit current task의 domain/operational fact를 evidence candidate로 추가
- capability fixture에 non-Python caller surface와 evidence conflict를 추가

Review finding:

초기 `conflicting-evidence` fixture는 implementation과 API contract가 일치하고 test만 stale해 보이는 형태라 정상적인 agent가 conflict를 합리적으로 해소해도 실패할 수 있었습니다.

Disposition: fixture ground truth를 수정해야 하는 material eval-quality gap.

### Loop 2 — Implementation → Review

다음을 보정했습니다.

- conflict fixture를 실제로 현재 적용되는 canonical authorities가 충돌하는 case로 변경
- user-provided fact behavior를 기존 `selective-positive-comment`에 흡수해 중복 fixture를 만들지 않음
- conflict가 존재한다는 이유로 모든 explanation을 막지 않고 **disputed claim만** permanent prose로 canonize하지 않도록 grounding contract를 좁힘

Review finding:

Structural comprehension problem이 같은 target에 존재할 때 `clarify-code`가 전체 작업을 sibling으로 handoff하면, 구조와 독립적으로 필요한 durable rationale까지 놓칠 수 있었습니다.

Disposition: responsibility composition gap.

### Loop 3 — Plan Delta → Implementation → Review

Plan에 mixed responsibility를 명시적으로 추가했습니다.

Implementation:

- structural concern은 `code-comprehension-refactor` responsibility로 분리
- independent evidence-backed caller/maintainer prose concern은 `clarify-code`가 계속 처리
- user가 executable change를 허용하지 않으면 sibling refactor를 임의 실행하지 않음
- `mixed-structural-and-rationale` fixture 추가

Review finding:

두 개의 related gap을 확인했습니다.

1. 기존 explanation text가 자기 semantic claim의 유일한 evidence가 되면 stale/misleading prose가 스스로를 정당화할 수 있음
2. `Default Explanation Decisions`의 “실행 코드가 이미 적절하고” 전제가 mixed responsibility behavior와 모순됨

Disposition: grounding + internal-instruction consistency gap.

### Loop 4 — Implementation → Review

다음을 보정했습니다.

- 수정 대상 prose는 candidate context일 뿐, project/runtime authority가 그 surface 자체를 canonical contract로 정의하지 않는 한 자기 claim의 sole evidence로 사용하지 않음
- stale narration fixture가 self-validation을 허용하지 않도록 assertion 강화
- `Default Explanation Decisions`에서 executable code 전체가 이미 적절해야 한다는 전제를 제거하고 independent durable meaning을 별도 판단
- Comments guidance도 mixed structural/prose concern을 같은 방식으로 정렬

Review finding:

`API documentation`이라는 portable term은 public API만 대상으로 오해될 수 있고, 동시에 scope 밖인 standalone API manual과 이름이 겹쳤습니다.

또 conflict fixture가 disputed claim 억제만 보고 **unrelated confirmed meaning을 계속 설명하는 recall**은 직접 검증하지 않았습니다.

Disposition: terminology/routing ambiguity + eval coverage gap.

### Loop 5 — Implementation → Review

다음을 적용했습니다.

- portable term을 **caller-facing declaration documentation**으로 변경
- public뿐 아니라 internal/private caller contract에도 같은 책임 적용
- standalone guide/README/API manual과 source-adjacent declaration documentation의 경계를 명확화
- conflict fixture에 independently agreed caller-visible side effect를 추가해 disputed claim만 억제하고 non-conflicting meaning은 실제로 설명하도록 요구
- frontmatter routing description도 `standalone user-facing documentation outside source files`만 제외하도록 교정
- frontmatter 변경에 따라 `route/skills.jsonl`을 canonical description과 동기화

Final Review에서는 추가 P1/P2 finding이 나오지 않았습니다.

`loops_used: 5`

## Final Design Review

### Responsibility

**Pass — static/semantic review.**

`clarify-code`는 source-adjacent explanatory prose만 변경합니다.

- caller-facing declaration documentation
- code-local maintainer comment
- source-level module/package explanation

Executable naming, representation, control/state flow, responsibility, indirection과 abstraction은 sibling `code-comprehension-refactor` responsibility입니다.

둘이 같은 target에 동시에 적용될 수 있지만 각 concern의 mutation owner는 겹치지 않습니다.

### Surface Selection

**Pass.**

Information type 자체가 surface를 결정하지 않습니다.

1. 의미가 caller-facing인지 maintainer-only인지 확인
2. 실제 semantic scope 확인
3. 현재 language/repository의 source-native surface 선택

따라서 caller-visible failure/protocol/order semantics는 declaration documentation으로 갈 수 있고, implementation-only ordering/protocol workaround는 code-local comment로 유지됩니다.

Python docstring은 한 ecosystem example일 뿐 portable syntax contract가 아닙니다.

### Comment Recall

**Pass — semantic contract; runtime model trial not run.**

사용자가 `comment`라는 단어를 직접 쓰지 않아도 evidence-backed durable meaning을 발견하면 explanation 후보로 봅니다.

Structural issue가 같이 존재해도 independent rationale를 global handoff로 잃지 않습니다.

Conflict가 있어도 disputed claim만 차단하고 unrelated confirmed meaning은 계속 설명할 수 있습니다.

### Precision / Anti-Spam

**Pass.**

- obvious narration은 추가하지 않음
- comment quantity를 quality proxy로 사용하지 않음
- code/name/type이 충분하면 prose를 추가하지 않음
- structural opacity를 comments로 해설해 덮지 않음
- broad policy를 code-adjacent prose에 중복 소유하지 않음

### Evidence Grounding

**Pass — static/semantic review.**

Candidate meaning은 current behavior, caller, test, applicable contract/spec, current config/schema/protocol, explicit current task facts 등으로 확인합니다.

- user-provided current fact는 evidence candidate이지 unconditional semantic authority가 아님
- target prose는 authority 확인 없이 자기 claim을 스스로 증명하지 않음
- Git history/old discussion은 supporting context
- material conflict는 해당 disputed claim에 국소적으로 적용
- conflict와 무관한 confirmed meaning까지 버리지 않음
- historical reason이 불확실해도 current constraint 자체가 확인되면 그 현재 의미만 설명 가능

### Routing

**Pass.**

Frontmatter는 source-file-adjacent declaration docs/comments/module-package explanation을 포함하고, executable changes와 standalone user-facing documentation을 제외합니다.

`route/skills.jsonl`의 clarify-code description은 latest canonical frontmatter와 동기화했습니다.

### Progressive Disclosure / Context Economy

**Pass.**

Common-path behavior는 core `SKILL.md`에 있습니다.

`references/documentation.md`는 다음과 같은 conditional detail에만 필요합니다.

- ecosystem-specific declaration surface ambiguity
- owner/placement/scope ambiguity
- conflict/history/indirect evidence
- canonical contract projection
- rejected alternative/stale prose
- module/package-level explanation
- machine/runtime/tool-consumed text

새 reference, taxonomy, score, analyzer를 추가하지 않았습니다.

Core는 이전보다 길어졌지만 추가된 내용은 각각 실제 review finding을 막습니다. 더 줄일 후보는 현재 behavior evidence 없이 문구를 합치는 cosmetic change에 가까워 이번 RPI에서는 중단합니다.

## Capability Fixture Review

최종 fixture는 서로 다른 behavior failure를 보호합니다.

### Positive / recall

- caller contract declaration docs
- maintainer rationale comment
- module/package local convention
- implicit test-backed comment discovery
- explicit current task fact를 이용한 selective comment
- durable rejected alternative
- mixed structural + independent rationale

### Precision / negative

- structural masking 금지
- line-by-line obvious comment 금지
- no-net-value comment no-op
- unsupported rationale no-fabrication

### Scope / stability / tooling

- placement scope
- stale narration + self-evidence 방지
- machine-consumed comment
- runtime/tool-consumed docstring

### Portability / conflict

- Go caller-facing declaration documentation surface
- currently applicable canonical authorities의 disputed claim no-canonization
- 같은 conflict case에서 unrelated confirmed caller contract는 계속 documentation

Fixture는 behavioral contract입니다. 실제 target model/runtime을 실행하지 않았으므로 runtime pass 또는 regression pass를 주장하지 않습니다.

## Validation Evidence

### Verified

- latest final-head PR Gate — **success**
- deterministic test suite — **224 passed**
- generated distribution route consistency — PR Gate에서 통과
- canonical `clarify-code` frontmatter ↔ `route/skills.jsonl` description — synchronized
- `clarify-code` ↔ `code-comprehension-refactor` responsibility static comparison — complete
- Skill/reference/eval semantic review — complete
- instruction bottleneck / context-noise review — no remaining P1/P2 finding

### Inferred / simulated

- surface-selection behavior
- task-provided evidence handling
- disputed-claim-local conflict handling
- mixed responsibility behavior
- stale-prose self-validation prevention

위 항목은 instruction과 fixture를 대상으로 한 semantic review이며 actual model execution evidence가 아닙니다.

### Not run

- model/runtime capability eval
- independent agent trial
- Rulesync strict doctor

실행하지 않은 항목을 pass로 주장하지 않습니다.

## Superseded Decisions

이 RPI에서 다음 이전 중간 결론이 변경되었습니다.

- `docstring`을 portable caller-doc responsibility name으로 사용 → `caller-facing declaration documentation`
- information signal을 곧바로 comment/docstring surface에 연결 → reader + semantic scope가 surface 결정
- any material evidence conflict가 explanation을 막는 것으로 읽힐 수 있는 표현 → disputed claim만 차단
- structural problem이 있으면 clarification 전체 handoff → concern별 responsibility 분리
- target prose가 별도 evidence 없이 기존 claim을 유지할 가능성 → circular grounding 차단
- `Do not use for user-facing documentation` routing boundary → standalone documentation outside source files만 제외

## Stop Decision

**RPI converged after 5 substantive loops.**

마지막 Review에서 추가 P1/P2가 발견되지 않았습니다. 남은 후보는 wording compression, 더 많은 language examples, 추가 cosmetic fixture 같은 항목이며 현재 failure evidence 없이 수행하면 context와 maintenance cost만 늘릴 가능성이 큽니다.

따라서 추가 loop는 실제 model/runtime eval, 독립 trial, 또는 새로운 user/reviewer failure evidence가 나타날 때 재개하는 것이 KISS/YAGNI에 부합합니다.

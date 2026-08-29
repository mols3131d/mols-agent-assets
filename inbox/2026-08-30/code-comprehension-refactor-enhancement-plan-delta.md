# Code Comprehension Refactor — Enhancement Plan Delta

## Based on

- `code-comprehension-refactor-enhancement-plan.md`
- `code-comprehension-refactor-enhancement-research.md`

이 문서는 기존 계획을 대체하지 않고, Research에서 확인된 material finding만 Implementation contract로 고정한다.

## Active Scope

### Goal

`code-comprehension-refactor`를 **실제 reader mental work를 줄이는 behavior-preserving executable refactor Skill**로 고도화하고, preservation evidence가 약하거나 responsibility가 다른 경우 안전하게 멈추거나 concern을 분리하도록 한다.

### In scope

- `SKILL.md`
- `references/diagnosis.md`
- `references/interventions.md`
- `references/validation.md`
- `evals/skills/code-comprehension-refactor/cases.json`
- frontmatter description은 routing gap이 Review에서 새로 확인되는 경우에만 변경
- description이 바뀌는 경우에만 `route/skills.jsonl` 동기화

### Out of scope

- 새 reference/script/analyzer/schema
- language/framework별 refactoring precondition catalog
- correctness fix, optimization 또는 architecture redesign 수행
- model/runtime eval infrastructure 추가

## Confirmed Failure Models

### P1 — Progressive Disclosure contradiction

Core workflow가 `Diagnosis`, `Interventions`, `Validation`을 사실상 매번 읽게 하면서 Progressive Disclosure는 조건부 loading이라고 선언한다.

**Plan:** common-path decision contract를 `SKILL.md`에 올리고, references는 ambiguous/high-risk/tricky case에서만 읽도록 load condition을 재설계한다. 파일 수는 우선 유지한다.

### P1 — Preservation gate가 transformation 선택보다 약함

Preservation envelope는 있지만 후보 transformation의 name binding, dynamic usage, ordering, side effect, state, persisted shape 등 **transformation-specific risk를 mutation 전에 확인하는 단계**가 약하다.

**Plan:** core에 `Preservation before Transformation` 순서를 추가한다.

1. task-relative bottleneck / coherent root cause 확인
2. affected observable + usage/contract surface 확인
3. 후보 transformation이 깨뜨릴 relevant preservation risk 확인
4. smallest safe coherent change 선택
5. 같은 preservation envelope를 after validation에 재사용

Language/tool-specific precondition은 local contract/tooling이 소유한다.

### P1 — caller-only terminology가 hidden usage를 놓칠 수 있음

Public/private caller graph 밖의 reflection, framework registration, config lookup, serialization, generated code, string/dynamic lookup도 symbol/path/shape를 관찰할 수 있다.

**Plan:** core에서 `caller-visible contract`만으로 safety를 표현하지 않고 **observable behavior + usage/contract surface**를 사용한다. Public/private visibility를 변경 자유의 proxy로 사용하지 않는다.

### P2 — single bottleneck row가 coupled root cause를 과도하게 자름

**Plan:** 한 taxonomy row가 아니라 **one coherent bottleneck / root-cause cluster**를 대상으로 한다. 한 mental-model burden을 제거하는 tightly coupled edits는 허용하되 unrelated cleanup은 계속 금지한다.

### P2 — one-dimensional clarity optimization

**Plan:** intervention 전후에 removed reader work와 introduced reader work를 비교한다. Numeric score는 만들지 않는다.

Removed cost 예:
- lexical/domain decoding
- representation decoding
- hidden dependency search
- navigation
- control simulation
- state/temporal tracking

Introduced cost 예:
- 새 concept/type/helper/file
- terminology inconsistency
- duplicated knowledge
- extra navigation
- ceremony/diffuseness
- broader coupling

### P2 — tests / characterization authority

**Plan:** `validation.md`에서 다음을 분리한다.

- tests = preservation evidence, not automatically complete specification
- characterization = observed baseline safeguard, not automatically normative requirement
- current observable behavior는 refactor 중 correctness 명목으로 몰래 변경하지 않음
- suspected correctness defect는 별도 concern으로 분리
- high-risk transformation에 evidence가 부족하면 safer transformation 또는 no-op

### P2 — mixed responsibility

**Plan:** concern별 owner를 분리한다.

- executable comprehension → `code-comprehension-refactor`
- independent source prose → `clarify-code`
- correctness defect → correctness work
- genuine optimization → performance work
- architecture constraint → architecture-level work/handoff

한 concern 때문에 전체 target을 handoff하거나 sibling concern을 몰래 흡수하지 않는다.

## File-by-file Work

### `SKILL.md`

- Purpose를 observable behavior + relevant usage/contract surface + material performance preservation으로 정교화
- common path에 comprehension target, preservation surface, transformation-risk gate, net comprehension gain, mixed responsibility를 직접 둠
- `one largest bottleneck`을 coherent bottleneck/root-cause cluster로 수정
- references를 unconditional workflow dependency에서 conditional decision support로 변경
- stop condition에 high-risk + weak preservation evidence → safer intervention/no-op 추가
- existing `clarify-code` boundary와 symmetry 확인

### `references/diagnosis.md`

- `Intent`를 lexical/semantic decoding 관점으로 더 직접 표현
- Usage Surface를 dynamic/framework/config/serialization/reflection까지 유지하되 core와 terminology 정렬
- local clarity vs broader terminology/consistency cost 추가
- root cause vs symptom / coupled bottleneck 판단 보강
- small confusing construct가 size와 무관하게 material할 수 있음을 명시

### `references/interventions.md`

- transform catalog를 늘리지 않음
- 후보 transformation을 고르기 전에 applicable language/tool/repository precondition을 확인
- safe refactoring tool/preview가 있으면 활용 가능하되 tool result를 proof로 취급하지 않음
- tightly coupled edits vs cleanup batch 구분
- rename은 terminology gain + usage surface preservation을 함께 확인
- extraction/inline/move/control rewrite에서 name binding, execution count, state/side-effect/order risk를 relevant할 때 확인
- net comprehension gain gate 추가

### `references/validation.md`

- preservation evidence와 specification authority 구분
- tests/characterization/static checks/tool preview 각각의 evidence 역할 구분
- before/after에서 같은 relevant envelope를 비교
- hidden/dynamic usage surface가 relevant하면 검증
- performance claim은 measurement/equivalent evidence가 있을 때만 강하게 표현
- evidence gap이 material하면 stop/safer intervention

### `evals/skills/code-comprehension-refactor/cases.json`

기존 9개를 유지하고 중복을 최소화한다. Research finding을 보호하는 최소 후보:

1. `lexical-domain-rename`
   - generic/abbreviated internal name을 repository-established domain term으로 rename
   - line count가 아니라 decoding cost 감소
   - 새 synonym을 만들지 않음
2. `dynamic-usage-rename-boundary`
   - private-looking symbol이 framework/config/string lookup에 사용됨
   - rename을 local/private change로 오판하지 않음
3. `tests-not-complete-spec`
   - tests는 green이지만 current contract/caller evidence가 추가 behavior를 요구
   - tests만으로 breaking refactor를 정당화하지 않음
4. `coupled-root-cause`
   - naming+representation 또는 control+state가 하나의 mental burden
   - 필요한 coupled edits는 허용하고 unrelated cleanup은 거부
5. `characterization-observed-not-normative`
   - characterization baseline은 보존 evidence로 사용하되 incidental observation을 새 requirement라고 주장하지 않음
   - suspected defect를 refactor와 섞지 않음
6. `mixed-structural-and-prose`
   - executable refactor는 수행하되 independent rationale는 `clarify-code` concern으로 분리

Review에서 기존 fixture와 중복되면 합치거나 강화하고 case 수를 줄인다.

## Review Loop

### Loop A — Preservation Safety

- transformation 전에 observable/usage surface를 찾는가
- public/private를 safety proxy로 쓰지 않는가
- tests/tooling을 proof로 과대평가하지 않는가
- ordering/state/side effect/name binding 위험을 relevant할 때 놓치지 않는가
- 너무 보수적이어서 안전한 local refactor까지 막지 않는가

### Loop B — Comprehension Gain

- smell, line count, hop count가 아니라 reader work를 실제로 줄이는가
- lexical/representation/control/state/navigation trade-off가 균형 잡히는가
- explicitness가 new concept/ceremony/global inconsistency를 늘리지 않는가
- coherent coupled edits는 허용되고 cleanup batch는 차단되는가

### Loop C — Responsibility Composition

- `clarify-code`, correctness, optimization, architecture와 concern별로 분리되는가
- 하나의 sibling concern 때문에 valid comprehension work를 전부 handoff하지 않는가
- 반대로 behavior change를 readability 명목으로 흡수하지 않는가

### Loop D — Eval Quality

- prompt가 답을 직접 알려주지 않는가
- positive/negative/near-miss/mixed가 균형적인가
- tests/characterization/contract authority를 fixture가 잘못 가정하지 않는가
- trajectory보다 observable behavior contract를 우선하는가

### Loop E — Context Economy

- common path가 references 없이도 안전한 기본 판단을 할 수 있는가
- reference load condition이 실제 conditional인가
- 같은 semantic rule이 core/reference에 불필요하게 반복되지 않는가
- 새 instruction이 concrete failure를 막는가

Material P1/P2가 나오면 같은 Plan scope 안에서 bounded correction 후 다시 Review한다.

## Validation

### Verified when available

- repository deterministic PR Gate
- fixture parse/schema integrity
- Skill/reference links
- generated route consistency only if frontmatter description changes
- sibling responsibility static comparison

### Simulated / inferred

- representative fixture behavior
- adversarial preservation scenarios
- instruction/context bottleneck review

### Not claimed unless actually run

- target model/runtime capability pass
- independent agent trial
- performance equivalence without benchmark/measurement
- Rulesync strict doctor

## Acceptance

- preservation discovery가 transformation보다 먼저 적용됨
- observable/usage surface가 dynamic/framework coupling을 포함할 수 있음
- tests/characterization/tooling의 evidence authority가 과대평가되지 않음
- one coherent root-cause cluster를 최소 범위로 해결함
- net comprehension gain이 local metric 하나가 아니라 total reader work 기준임
- sibling concerns가 정확히 분리됨
- Progressive Disclosure가 실제 loading boundary를 가짐
- eval이 핵심 failure modes를 최소 중복으로 보호함
- deterministic validation green
- 마지막 adversarial Review에서 새 P1/P2 없음

## Status

**Plan Delta accepted for Implementation.**

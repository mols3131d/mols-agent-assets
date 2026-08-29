# Code Comprehension Refactor — Enhancement Research

## Goal

`code-comprehension-refactor`가 executable code의 실제 comprehension cost를 줄이면서 **observable behavior, usage contract와 task에 material한 performance characteristic을 보존**하도록 현재 설계의 failure model을 검증한다.

이 문서는 기존 `clarify-code-comprehension-cost-research.md`의 program-comprehension baseline을 재사용하고, `code-comprehension-refactor-enhancement-plan.md`에서 열린 질문 가운데 현재 Skill을 실제로 바꿀 수 있는 부분만 추가 조사한다.

## Active Scope

### In scope

- comprehension bottleneck 진단 정확도
- behavior/contract/performance preservation evidence
- rename/move/extract/inline/representation/control-state change의 hidden usage risk
- coupled bottleneck과 smallest coherent change
- `clarify-code`, correctness, optimization, architecture와 mixed responsibility
- core/reference Progressive Disclosure
- capability eval의 missing behavior contract

### Out of scope

- feature/correctness/performance optimization 자체의 구현
- architecture redesign
- 모든 language/framework refactoring precondition catalog
- formal verification framework
- comment/readability score 또는 static analyzer
- runtime/model eval infrastructure 신규 구축

## Reused Baseline

`clarify-code-comprehension-cost-research.md`에서 다음은 이미 충분한 근거가 있으므로 다시 증명하지 않는다.

- comprehension은 task-relative mental model formation이다.
- readability와 brevity는 같은 축이 아니다.
- meaningful naming은 lexical/domain decoding cost를 줄일 수 있다.
- 작은 syntax도 material misunderstanding risk를 만들 수 있다.
- representation은 closeness, role-expressiveness, hidden dependency, hard mental operation, diffuseness, abstraction 사이의 trade-off다.
- navigation은 비용이지만 stable concept/invariant를 얻는 semantic gain이 있으면 정당화될 수 있다.
- structural opacity는 comment만으로 덮기보다 executable representation을 개선해야 할 수 있다.

따라서 이번 Research의 질문은 **이 baseline이 현재 Skill의 행동 계약에 충분히 operationalize되어 있는가**다.

## External Evidence

### Refactoring의 핵심은 observable behavior preservation이다

Martin Fowler의 refactoring 정의는 internal structure를 더 이해하기 쉽고 수정하기 쉽게 바꾸되 observable behavior를 바꾸지 않는 것으로 둔다. Fowler의 refactoring boundary 설명도 observable behavior의 범위가 단순 output value보다 넓고 context-dependent하다는 점을 인정한다.

Sources:

- https://martinfowler.com/bliki/DefinitionOfRefactoring.html
- https://martinfowler.com/bliki/RefactoringBoundary.html

**Implication:** `code-comprehension-refactor`의 목적은 generic restructuring이 아니라 behavior-preserving restructuring이다. 따라서 transformation 선택보다 preservation envelope discovery가 먼저여야 한다.

### Behavior preservation은 한 가지 검증 기법으로 완전히 증명되지 않는다

2021 systematic mapping study는 refactoring의 behavior preservation에 formal techniques, refactoring preconditions, dynamic analysis, testing과 manual analysis 등 여러 전략이 사용되며, refactoring operation에 따라 안전성 접근이 다르고 일부 영역은 충분히 연구되지 않았다고 정리한다.

2026 Empirical Software Engineering 연구도 compile + test suite가 흔한 correctness check이지만 subtle behavior deviation을 놓칠 수 있고, 실제 developer test suite가 refactored member를 충분히 exercise하지 못하는 문제가 있다고 요약한다.

Sources:

- AlOmar et al., *On preserving the behavior in software refactoring: A systematic mapping study*: https://doi.org/10.1016/j.infsof.2021.106675
- *Foundation models as oracles for refactoring correctness detection* (2026): https://link.springer.com/article/10.1007/s10664-026-10951-y
- Microsoft Research, *Making Program Refactoring Safer*: https://www.microsoft.com/en-us/research/publication/making-program-refactoring-safer/

**Implication:** tests는 strong evidence가 될 수 있지만 **complete specification 또는 preservation proof로 자동 승격하면 안 된다.** 위험도가 높은 transformation에서 evidence가 빈약하면 더 작은 change나 no-op을 선택할 수 있어야 한다.

### Refactoring safety에는 transformation-specific precondition이 있다

Behavior-preserving refactoring 연구는 rename, move 같은 operation마다 name binding, overriding, synchronization, data reachability, execution count, side-effect ordering 등 서로 다른 precondition이 중요하다는 점을 반복해서 보여준다. 2026년 fine-grained Move Statement 연구도 data reachability, execution count, side effects와 syntactic constraints를 구분하고, side-effect reordering은 developer judgment가 필요한 주요 risk로 남겼다.

Sources:

- AlOmar et al. mapping study above
- Yasuhara & Hayashi, *Formalizing and Automating Fine-Grained Move Refactorings Across Methods* (2026): https://arxiv.org/abs/2608.23377

**Implication:** Skill에 모든 language-specific precondition을 복제할 필요는 없지만, **선택한 transformation family의 preservation risk를 적용되는 language/tool/repository contract에서 확인하는 gate**는 필요하다. Generic test-only validation으로는 부족하다.

### Rename/move의 usage surface는 static caller graph보다 넓을 수 있다

Fowler는 interface-changing refactoring이 behavior-preserving이려면 caller를 모두 바꿀 수 있어야 하며, dynamic language와 reflective call, string에 포함된 method name은 caller discovery를 어렵게 만든다고 지적한다.

현재 IntelliJ IDEA 2026.2도 Rename에서 comments/strings/text occurrences와 **dynamic references**를 별도 선택 대상으로 다루고, dynamic usage search가 erroneous rename을 만들 수 있어 preview가 필요하다고 문서화한다.

Sources:

- https://martinfowler.com/bliki/IsChangingInterfacesRefactoring.html
- https://www.jetbrains.com/help/idea/rename-refactorings.html
- https://www.jetbrains.com/help/idea/specific-typescript-refactorings.html

**Implication:** `caller-visible contract`만으로 preservation surface를 표현하면 좁게 읽힐 수 있다. Symbol name/path/shape가 framework discovery, config, reflection, serialization, generated code, dynamic lookup 등에 관찰되는 경우를 **usage/observable surface**로 core에서 발견해야 한다. Tool search 결과 역시 evidence이지 proof가 아니다.

### Characterization test는 현재 behavior의 safeguard이지 normative specification 자체는 아니다

Characterization testing은 legacy code가 실제로 무엇을 하는지를 capture해 refactoring safety net으로 사용한다. 여기에는 의도된 behavior뿐 아니라 현재 bug나 accidental behavior도 포함될 수 있다.

이 사실은 behavior-preserving refactor에서 characterization test가 쓸모없다는 뜻이 아니다. 오히려 correctness change와 refactoring을 섞지 않기 위해 현재 observable baseline을 잠그는 데 유용하다. 다만 그 observation을 곧바로 “이것이 의도된 durable contract다”라고 선언하면 안 된다.

Supporting source:

- Michael Feathers의 characterization-testing practice를 요약한 current guidance: https://docs.synapsestudios.com/concepts/legacy/characterization-testing
- Fowler, external-service legacy refactoring example: https://martinfowler.com/articles/refactoring-external-service.html

**Implication:** validation은 **observed baseline**과 **normative/current contract**를 구분해야 한다. Characterization test가 incidental behavior를 새 requirement로 canonize하지 않도록 하고, correctness defect가 의심되면 별도 concern으로 보고한다. 그러나 current observable behavior를 refactor 중 몰래 고치는 것도 금지한다.

### Small, reviewable refactoring은 risk control 수단이지 line-count 목표가 아니다

Fowler의 refactoring workflow는 small behavior-preserving transformations와 green state를 강조한다. 이는 작은 diff가 항상 좋은 것이 아니라, 각 step의 semantic risk를 좁히고 failure localization과 rollback을 쉽게 하는 방향이다.

Sources:

- https://martinfowler.com/articles/workflowsOfRefactoring/fallback.html
- https://www.martinfowler.com/books/refactoring.html

**Implication:** 현재 `smallest coherent conceptual change`는 유지하되, 필요하면 하나의 root bottleneck을 제거하는 tightly coupled edits를 허용해야 한다. 반대로 여러 smell을 한 번에 고치는 cleanup batch는 refactoring safety와 reviewability를 약화한다.

## Internal Findings

### P1 — Progressive Disclosure 계약이 현재 Workflow와 모순된다

현재 `SKILL.md` workflow는 bottleneck 진단 시 `Diagnosis`, intervention 선택 시 `Interventions`, 변경 전후 검증 시 `Validation`을 직접 따르도록 쓴다. 정상적인 모든 executable refactor가 진단·intervention·validation을 필요로 하므로 세 reference는 사실상 always-loaded가 된다.

그러나 Progressive Disclosure section은 “현재 판단에 필요한 reference만 읽는다”고 한다.

이 상태는 두 가지 문제를 만든다.

1. package 분리의 context benefit가 실제로 없다.
2. common-path 행동이 reference에 분산돼 모델이 세 문서를 조합해야 한다.

**Disposition:** core에 common-path contract를 올리고 reference는 실제 tricky case로 좁혀야 한다. 세 reference를 합치거나 삭제하는 것은 loading boundary와 ownership을 다시 본 뒤 결정한다.

### P1 — Preservation discovery가 transformation 선택보다 충분히 앞서지 않는다

현재 workflow는 preservation envelope를 먼저 확인하지만, 곧바로 bottleneck → intervention으로 이동한다. 선택한 transformation이 어떤 name binding, usage, ordering, state, side-effect, dynamic lookup 위험을 갖는지 **mutation 전에** 따로 확인하는 gate가 약하다.

`validation.md`에는 preservation envelope가 있지만 대부분 before/after validation 관점이다.

**Disposition:** `Preservation before Transformation`을 core behavior로 만들 필요가 있다.

예상 contract:

1. task-relative bottleneck을 확인한다.
2. 바꾸려는 surface와 연결된 observable/usage contract를 확인한다.
3. 후보 transformation이 깨뜨릴 수 있는 relevant preservation precondition을 확인한다.
4. 충분히 안전한 smallest coherent transformation을 선택한다.
5. 같은 envelope를 after validation에 다시 사용한다.

Language/framework-specific rule은 portable Skill에 나열하지 않고 applicable tooling/contract를 읽는다.

### P1 — Core의 caller language가 hidden/dynamic usage surface를 놓칠 수 있다

`diagnosis.md`의 Usage Surface는 framework callback, registration, serialization, reflection 등을 이미 알고 있다. 하지만 `SKILL.md`의 common workflow와 description은 주로 `caller-visible contract`, caller/entrypoint라는 표현을 사용한다.

이 때문에 internal/private rename이나 representation change를 “public caller가 없으니 안전”하다고 오판할 수 있다.

**Disposition:** core preservation term을 caller-only가 아니라 **observable behavior + usage/contract surface**로 확장한다. Public/private visibility를 safety proxy로 사용하지 않는다.

### P2 — “가장 큰 bottleneck 하나”는 root-cause cluster를 너무 잘게 자를 수 있다

현재 `Diagnosis`는 가장 material한 bottleneck 하나를 먼저 해결한다고 한다. Scope control에는 좋지만 representation + naming, control flow + mutable state처럼 서로를 분리하면 문제를 실제로 제거할 수 없는 경우가 있다.

**Disposition:** 목표를 “한 taxonomy row”에서 **one coherent bottleneck / root-cause cluster**로 바꾼다. 하나의 mental-model burden을 제거하는 tightly coupled edits는 허용하되 unrelated cleanup은 계속 금지한다.

### P2 — Comprehension gain을 한 cognitive dimension으로 판정할 위험이 남아 있다

현재 abstraction value와 hop-count 경계는 좋다. 그러나 Intervention 단계에서 local explicitness, fewer helpers, more named intermediates 같은 한 축의 개선이 broader consistency, diffuseness, new-concept cost를 키우는 경우를 core에서 다시 확인하는 final net-value gate가 약하다.

**Disposition:** intervention은 **removed reader work vs introduced reader work**를 비교한다. 정확한 점수는 만들지 않는다.

Removed cost 후보:

- lexical/domain decoding
- representation decoding
- hidden dependency search
- navigation
- control simulation
- state/temporal tracking

Introduced cost 후보:

- 새 concept/type/helper/file
- terminology inconsistency
- duplicated policy/knowledge
- extra navigation
- diffuseness/ceremony
- broader coupling

### P2 — Naming/lexical decoding은 현재 eval에서 직접 보호되지 않는다

Diagnosis에는 Intent row가 있지만 현재 9개 fixture에는 naming-only 또는 lexical-decoding case가 없다. Representation/boolean/wrapper/control-state 중심으로 치우쳐 있다.

**Disposition:** 실제 domain terminology를 사용한 internal rename positive case와, rename이 framework/dynamic contract를 깨뜨리는 near-miss를 각각 검토한다. 두 case가 중복될 경우 하나의 mixed fixture로 합친다.

### P2 — Characterization의 authority가 더 명확해야 한다

현재 `validation.md`는 characterization test가 “현재 observable contract만 고정”해야 한다고 쓰지만, observed behavior와 normative contract를 구분하지 않는다.

**Disposition:** characterization은 observed baseline safeguard이며, 별도 contract evidence 없이 “의도된 requirement”라고 부르지 않는다. 동시에 refactor scope에서 observed externally visible behavior를 correctness 명목으로 바꾸지 않는다.

### P2 — Mixed responsibility는 sibling에서 배운 composition rule을 반대 방향에도 적용해야 한다

`clarify-code`는 structural issue와 independent prose need를 동시에 처리하도록 개선됐다. `code-comprehension-refactor`도 같은 원칙이 필요하다.

- structural comprehension concern → 이 Skill이 수행
- independent explanation concern → `clarify-code`
- correctness defect → separate correctness work
- optimization opportunity → separate optimization work
- architecture constraint → architecture-level handoff

한 concern 때문에 전체 target을 handoff하지도, 반대로 sibling concern을 몰래 흡수하지도 않는다.

## Research Decisions

### 유지

- comprehension cost = misunderstanding risk + reconstruction effort
- behavior-preserving executable-code responsibility
- stable abstraction/invariant ownership 보호
- smallest coherent conceptual change
- no numeric readability/complexity score
- performance optimization과 architecture redesign 제외
- three-reference package는 일단 유지하되 loading boundary를 재설계

### 변경 대상으로 확정

1. `SKILL.md`
   - `Preservation before Transformation` common-path gate
   - caller-only 표현을 observable/usage surface로 일반화
   - one bottleneck row가 아니라 coherent root-cause cluster
   - mixed responsibility composition
   - net comprehension gain / introduced conceptual cost 확인
   - Progressive Disclosure를 실제 conditional loading으로 변경
2. `references/diagnosis.md`
   - lexical/domain decoding을 더 명확한 first-class bottleneck으로 표현
   - usage surface와 local/global consistency trade-off 보강
3. `references/interventions.md`
   - transformation-specific safety precondition을 applicable language/tool/repository에서 확인하는 rule
   - tightly coupled edits vs unrelated cleanup
   - removed reader work vs introduced conceptual surface
4. `references/validation.md`
   - tests = evidence, not complete specification
   - observed baseline vs normative contract
   - dynamic/hidden usage와 transformation-specific risk
   - high-risk + weak evidence → safer intervention/no-op
5. `evals/skills/code-comprehension-refactor/cases.json`
   - hidden/dynamic usage preservation
   - tests-not-complete-spec / insufficient evidence
   - lexical naming gain
   - coupled bottleneck
   - mixed responsibility
   - characterization authority boundary

모든 candidate를 독립 case로 만들지 않는다. 하나의 fixture가 서로 연결된 behavior를 자연스럽게 검증하면 합친다.

### 변경하지 않음

- frontmatter description은 현재 routing failure evidence가 없다. Body terminology 정교화만으로 해결되면 유지한다.
- 새 reference는 추가하지 않는다.
- formal proof, analyzer, refactoring catalog를 만들지 않는다.
- 특정 IDE나 language의 refactoring semantics를 portable rule로 고정하지 않는다.

## Residual Uncertainty

- 실제 target model이 세 reference의 load condition을 얼마나 충실하게 지키는지는 runtime eval 없이 검증할 수 없다.
- language-specific refactoring safety는 repository/tooling에 따라 달라 portable Skill에서 완전한 precondition list를 제공할 수 없다.
- “observable behavior”의 범위는 task/repository contract에 따라 다르므로 universal exhaustive list로 고정하면 오히려 false boundary를 만들 수 있다.

이 uncertainty는 core를 더 장황하게 만드는 이유가 아니라, **applicable contract를 읽고 evidence가 약할 때 더 보수적인 transformation을 고르는 이유**로 사용한다.

## Research Status

**Research complete for Plan Delta.**

현재 evidence는 기존 Plan의 주요 질문을 충분히 닫았으며, 다음 단계는 위 confirmed finding만 Plan Delta로 고정한 뒤 Implementation → Review loop를 수행하는 것이다.

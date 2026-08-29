# Code Comprehension Refactor — Enhancement Plan

## 목적

`code-comprehension-refactor`를 **행동·caller contract·중요한 performance 특성을 보존하면서 executable code의 실제 comprehension cost를 줄이는 Skill**로 고도화한다.

이번 작업의 목표는 refactoring 기법을 더 많이 나열하는 것이 아니다. Agent가 다음을 안정적으로 판단하도록 만드는 것이 핵심이다.

1. 무엇이 실제 comprehension bottleneck인지
2. executable refactor가 정말 적절한 intervention인지
3. 무엇을 절대 바꾸면 안 되는지
4. 어느 정도까지 바꿔야 병목이 실질적으로 줄어드는지
5. 변경 전후 동등성을 어떤 evidence로 확인할지
6. `clarify-code`, correctness work, performance optimization, architecture redesign과 책임을 어떻게 조합할지

## 현재 상태

현재 package는 다음 구조다.

```text
src/rulesync/.rulesync/skills/code-comprehension-refactor/
├── SKILL.md
└── references/
    ├── diagnosis.md
    ├── interventions.md
    └── validation.md

evals/skills/code-comprehension-refactor/
└── cases.json
```

현재 설계의 좋은 기반은 유지한다.

- comprehension cost를 code size가 아니라 misunderstanding risk와 reconstruction effort로 판단
- shortest diff가 아니라 smallest coherent conceptual change를 선택
- stable domain abstraction과 invariant-owning boundary를 보존
- representation, naming, control/state reasoning, indirection, abstraction mismatch를 executable-code 문제로 처리
- caller-visible contract와 material performance를 preservation envelope에 포함
- comment/docstring-only 문제는 `clarify-code`로 분리
- feature, correctness fix, optimization, public API redesign, architecture redesign은 scope 밖으로 둠

이번 고도화는 이 기반을 다시 설계하는 작업이 아니라 **판단 정확도, preservation safety, responsibility composition, eval coverage와 context economy를 높이는 작업**이다.

## 시작점에서 확인할 질문

아래 항목은 아직 확정된 finding이 아니다. Research와 Review에서 실제 문제가 있는지 검증한다.

### 1. Preservation evidence가 충분히 강한가

현재 validation은 behavior envelope와 before/after 검증을 잘 설명한다. 다만 다음 오해 가능성을 검토한다.

- 기존 test pass를 전체 behavior preservation의 증명으로 과대평가하지 않는가
- test, caller, contract, observable behavior가 충돌할 때 무엇을 authority로 삼는가
- characterization test가 현재 bug나 incidental behavior를 새 contract로 canonize하지 않는가
- 이름·경로·shape를 바꿀 때 reflection, serialization, registration, framework discovery 같은 hidden caller를 충분히 찾는가
- performance-sensitive code에서 “material performance”의 실제 범위를 task/repository 기준으로 판단하는가

필요하다면 `clarify-code`에서 정리한 **Evidence before Explanation**과 비슷한 수준의 원칙을 그대로 복제하지 않고, executable-refactor에 맞는 **Preservation before Transformation** 계약으로 정리한다.

### 2. Comprehension bottleneck을 올바르게 진단하는가

현재 taxonomy는 유용하지만 Agent가 smell 이름을 보고 기계적으로 refactor하지 않도록 더 압박할 필요가 있는지 본다.

검토 대상:

- task와 reader에 실제로 필요한 mental model이 무엇인지
- frequently-read code와 rarely-touched implementation의 차이
- misunderstanding impact와 reconstruction effort의 trade-off
- 한 surface에 여러 bottleneck이 결합된 경우 주된 원인과 증상을 구분하는 방법
- “explicit”을 이유로 domain abstraction을 펼쳐 오히려 reasoning을 늘리는 failure
- local readability를 높이는 대신 system-wide navigation/consistency cost를 키우는 failure

### 3. “가장 큰 bottleneck 하나” stop rule이 과도하게 좁은가

현재는 가장 material한 bottleneck 하나를 먼저 해결하고 주된 병목이 해소되면 중단한다.

이 원칙은 scope control에는 좋지만 다음 coupled case를 검토해야 한다.

- representation과 naming이 같은 hidden convention을 함께 소유하는 경우
- control flow와 mutable state가 분리할 수 없는 하나의 reasoning burden인 경우
- wrapper chain과 abstraction mismatch가 같은 원인의 다른 표면인 경우

목표는 여러 cleanup을 한 번에 허용하는 것이 아니다. **한 conceptual bottleneck을 제거하기 위해 필요한 최소한의 coupled edits**와 unrelated cleanup을 구분할 수 있는 계약이 필요한지 판단한다.

### 4. Responsibility composition이 충분한가

`clarify-code` 최종 고도화에서 확인했듯 한 target에는 서로 다른 concern이 동시에 존재할 수 있다.

다음 mixed case를 검토한다.

- structural refactor + independent rationale/comment need
- comprehension refactor 중 correctness defect 발견
- readability refactor + genuine performance optimization opportunity
- local refactor로 해결할 수 없는 architecture-level comprehension problem
- user가 executable change를 금지했는데 structural problem만 존재하는 경우

각 concern을 올바른 owner로 분리하면서도 **한 concern의 존재 때문에 다른 유효한 concern 전체를 handoff하거나 무시하지 않도록** 한다.

### 5. Mutation authority와 contract surface를 충분히 구분하는가

현재 `diagnosis.md`는 usage surface를 넓게 본다. 이 판단이 core workflow에도 충분히 반영되는지 확인한다.

특히 다음을 본다.

- internal rename도 framework/config/reflection contract일 수 있음
- private helper도 monkey patching, serialization, generated code, callback discovery 등에 노출될 수 있음
- representation change가 local해 보여도 persisted shape나 schema contract를 바꿀 수 있음
- extraction/inlining이 stack trace, registration identity, introspection 또는 ordering semantics에 영향을 줄 수 있음

“public API가 아니면 자유롭게 변경 가능” 같은 암묵적 전제를 허용하지 않는 방향으로 검토한다.

### 6. Progressive Disclosure가 실제로 작동하는가

현재 core workflow는 `Diagnosis`, `Interventions`, `Validation` reference를 직접 언급하고 Progressive Disclosure에서는 필요한 것만 읽도록 한다.

실제 loading boundary를 검토한다.

- common-path 판단에 반드시 필요한 contract는 `SKILL.md`에 있어야 하는가
- 어떤 reference가 사실상 항상 로드되고 있는가
- 세 reference의 역할이 충분히 독립적인가
- 중복된 판단이 core/reference에 여러 번 나타나 context noise를 만들지 않는가
- reference를 합치거나 줄이는 편이 나은지, 현 구조를 유지하는 편이 나은지

파일 수 자체를 목표로 하지 않는다. **실제 conditional loading boundary와 semantic ownership**으로 판단한다.

## Research

### 내부 evidence

다음을 우선 대조한다.

- `code-comprehension-refactor/SKILL.md`
- `references/diagnosis.md`
- `references/interventions.md`
- `references/validation.md`
- `evals/skills/code-comprehension-refactor/cases.json`
- 최신 `clarify-code` package와 eval — sibling responsibility/composition 비교용
- `coding-context`
- `mols-agent-asset`
- `mols-agent-asset-validator`
- repository design principles / instruction authoring / Skill authoring conventions / evaluation guidance

### 외부 research 축

필요한 경우 최신 또는 원전 중심으로 조사한다.

- program comprehension과 mental-model formation
- behavior-preserving refactoring의 preconditions와 observational equivalence
- refactoring과 API/semantic compatibility
- characterization testing의 한계와 legacy-code behavior capture
- dynamic/reflection/framework coupling이 rename/extraction에 미치는 영향
- readability/refactoring empirical studies
- cognitive dimensions / information foraging / navigation cost
- performance-sensitive refactoring과 benchmark evidence

외부 자료를 그대로 규칙으로 옮기지 않는다. 현재 Skill에서 반복될 수 있는 concrete failure를 설명하는 evidence만 흡수한다.

## Plan Gate

Research가 끝난 뒤 다음을 확정하고 Implementation으로 넘어간다.

1. 실제 P1/P2 failure model
2. 유지할 기존 behavior contract
3. 변경할 exact files
4. 새 core behavior와 reference owner
5. 추가·수정할 eval case
6. 하지 않을 것
7. validation 방법과 stop condition

Research가 현재 설계가 충분하다고 보여주는 영역은 변경하지 않는다.

## 예상 Implementation Surface

초기 예상은 아래 범위다. Research 결과에 따라 더 줄일 수 있다.

```text
src/rulesync/.rulesync/skills/code-comprehension-refactor/
├── SKILL.md
└── references/
    ├── diagnosis.md
    ├── interventions.md
    └── validation.md

evals/skills/code-comprehension-refactor/
└── cases.json
```

Frontmatter `description`은 routing failure가 실제로 확인될 때만 수정한다. 변경하면 generated `route/skills.jsonl`을 canonical source와 동기화한다.

새 reference, script, analyzer, score, taxonomy는 기존 구조로 해결할 수 없는 concrete need가 확인될 때만 추가한다.

## 예상 개선 축

Research가 필요성을 확인하면 다음 순서로 적용한다.

### A. Core decision contract

`SKILL.md`가 common path에서 직접 소유해야 하는 최소 판단을 정리한다.

예상 후보:

- task-relative comprehension bottleneck
- preservation envelope discovery
- structural intervention appropriateness
- smallest coherent conceptual change
- coupled edit와 unrelated cleanup의 구분
- mixed responsibility 분리
- validation evidence와 uncertainty

### B. Diagnosis precision

`diagnosis.md`는 smell catalog가 아니라 **reader가 수행하는 불필요한 mental work와 그 원인**을 찾는 owner로 유지한다.

필요하면 다음 edge를 보강한다.

- symptom vs root bottleneck
- hidden external/dynamic usage surface
- local clarity vs global comprehension trade-off
- valuable abstraction vs accidental indirection
- representation improvement가 새 conceptual surface를 추가하는 비용

### C. Intervention selection

`interventions.md`는 transformation catalog를 키우기보다 **조건 → 가장 작은 안전한 transformation → 하지 말아야 할 대안**을 명확히 한다.

특히 검토할 것:

- rename/extract/inline/move/representation change의 precondition
- coupled edits가 하나의 conceptual change인지 판정
- 새로운 type/helper/file을 추가할 가치
- existing domain surface 재사용 우선
- local simplification이 broader consistency를 깨지 않는지

### D. Preservation / validation

`validation.md`는 “tests pass”가 아니라 **무엇이 preserved되었는지에 대한 evidence contract**를 소유한다.

필요하면 다음을 명시한다.

- tests는 evidence이며 언제나 complete specification은 아님
- current contract와 test가 충돌할 때 임의로 한쪽을 canonize하지 않음
- hidden/dynamic caller surface를 relevant할 때 확인
- characterization test가 incidental behavior를 새 requirement로 만들지 않음
- unverified behavior/performance equivalence는 주장하지 않음
- risk가 높고 evidence가 부족하면 더 작은 intervention 또는 no-op 선택

### E. Context economy

최종적으로 core와 references를 다시 대조한다.

- 필수 common-path rule이 reference에 숨어 있지 않은가
- 같은 rule이 두 곳에서 장황하게 반복되지 않는가
- 실제로 conditional하지 않은 reference가 있는가
- reference 통합/삭제가 오히려 ownership을 흐리지 않는가

## Eval Plan

현재 9개 fixture를 유지하면서 gap이 확인된 경우에만 추가 또는 강화한다.

우선 검토할 scenario는 다음이다.

| Candidate | 검증하려는 failure |
| --- | --- |
| hidden-framework-caller | internal rename/move를 local change로 오판해 callback/registration contract를 깨뜨림 |
| tests-not-complete-spec | passing tests만 보고 untested caller-visible behavior 변경을 허용 |
| coupled-bottleneck | 하나의 conceptual bottleneck을 해결하는 데 필요한 coupled edit를 unrelated cleanup으로 오판하거나, 반대로 cleanup을 과도하게 확장 |
| correctness-found-during-refactor | correctness concern과 comprehension concern을 섞어 behavior를 변경 |
| mixed-prose-and-structure | structural refactor와 independent `clarify-code` prose need를 concern별로 분리 |
| characterization-boundary | incidental current behavior를 characterization test로 새 contract처럼 고정 |
| broader-consistency-cost | local explicitness를 위해 repository-wide stable abstraction/convention을 불필요하게 깨뜨림 |
| insufficient-preservation-evidence | 위험한 refactor를 evidence 없이 강행하지 않고 smaller change/no-op 선택 |

모든 candidate를 추가하는 것이 목표가 아니다. 기존 fixture와 중복되지 않고 실제 failure contract를 보호하는 최소 집합만 남긴다.

Positive, negative, near-miss와 mixed-responsibility case가 균형을 이루는지 함께 검토한다.

## Review Loop

Implementation 뒤에는 최소 다음 순서로 리뷰한다.

### Review A — Responsibility

- executable-code comprehension만 소유하는가
- `clarify-code`, correctness, optimization, architecture responsibility와 겹치지 않는가
- mixed case에서 전체 handoff 또는 전체 흡수가 발생하지 않는가

### Review B — Preservation Safety

- observable behavior만이 아니라 relevant caller/dynamic/tooling surface를 고려하는가
- test pass를 과대해석하지 않는가
- contract conflict/uncertainty를 숨기지 않는가
- performance-sensitive path에서 측정되지 않은 equivalence를 주장하지 않는가

### Review C — Refactor Quality

- shortest/longest diff가 아니라 actual comprehension cost를 낮추는가
- abstraction을 hop count로 제거하지 않는가
- 새로운 helper/type/file이 semantic gain보다 ceremony를 늘리지 않는가
- local simplification이 global reasoning cost를 키우지 않는가

### Review D — Eval Quality

- fixture가 정답 문구가 아니라 behavior contract를 검사하는가
- prompt가 답을 너무 친절하게 알려줘 discovery 능력을 가리지 않는가
- false positive/false negative를 모두 방어하는가
- fixture 자체가 잘못된 semantic authority를 가정하지 않는가

### Review E — Instruction / Context Economy

- 실제 failure를 막지 않는 instruction을 제거할 수 있는가
- core와 reference ownership이 명확한가
- Progressive Disclosure가 실제 loading boundary를 가지는가
- 추가 규칙이 판단을 더 정확하게 하는지, 단지 더 보수적으로만 만드는지

각 Review에서 material P1/P2가 발견되면 같은 scope 안에서 보정하고 다시 Review한다. 새 architecture나 unrelated problem이 필요하면 새 RPI scope로 분리한다.

## Validation

Implementation 후 가능한 검증을 evidence level별로 분리한다.

### Verified

- repository deterministic test suite
- eval fixture schema/parse
- generated route consistency if routing description changed
- canonical Skill/reference link integrity
- sibling Skill responsibility static comparison

### Simulated / inferred

- representative capability fixture에 대한 semantic simulation
- adversarial/near-miss behavior review
- instruction bottleneck/context-noise review

### Not claimed unless actually run

- target model/runtime capability pass
- independent agent trial
- benchmark/performance equivalence
- Rulesync strict doctor

실행하지 않은 validation을 pass로 기록하지 않는다.

## Acceptance Criteria

다음이 모두 충족되면 이번 고도화를 수렴으로 본다.

- Skill이 실제 comprehension bottleneck을 smell/size가 아니라 reader mental work 기준으로 판단한다.
- behavior, caller-visible/dynamic contract, state/side effect/error semantics와 material performance preservation이 transformation보다 앞선다.
- test pass만으로 preservation을 과대 주장하지 않는다.
- smallest coherent change가 coupled edits를 허용하되 unrelated cleanup으로 확장되지 않는다.
- valuable domain abstraction과 stable boundary를 explicitness 명목으로 파괴하지 않는다.
- structural comprehension work와 sibling concern을 concern별로 정확히 분리한다.
- risk가 높은데 preservation evidence가 부족하면 safer intervention 또는 no-op을 선택할 수 있다.
- core/reference의 loading boundary가 실제로 의미 있고 중복이 과하지 않다.
- eval이 positive, negative, near-miss, mixed와 preservation-failure behavior를 충분히 보호한다.
- deterministic validation이 green이다.
- 마지막 Review에서 추가 P1/P2가 나오지 않는다.

## 하지 않을 것

- code readability score나 complexity score를 새로 만들지 않는다.
- 모든 tuple/boolean/helper/wrapper를 smell로 규정하지 않는다.
- 모든 refactor 전에 새 test/benchmark 작성을 강제하지 않는다.
- public API redesign이나 architecture redesign을 comprehension refactor로 흡수하지 않는다.
- correctness fix나 performance optimization을 몰래 함께 수행하지 않는다.
- 주석으로 structural problem을 덮지 않는다.
- 모든 언어나 framework를 나열하는 compatibility catalog를 만들지 않는다.
- 새 reference나 analyzer를 evidence 없이 추가하지 않는다.
- line count, diff size, abstraction count를 품질 proxy로 쓰지 않는다.

## Stop Condition

Research와 반복 Review에서 새로운 material P1/P2가 더 이상 나오지 않고 acceptance criteria가 충족되면 중단한다.

남은 후보가 wording polish, 더 많은 사례, speculative framework edge, 새로운 taxonomy 같은 수준이라면 추가 구현하지 않는다. 이후 실제 model/runtime trial이나 사용자·reviewer failure evidence가 생겼을 때 새 loop를 연다.

## Status

**Planning complete.**

다음 단계는 이 계획의 질문을 대상으로 Research를 수행하고, evidence에 따라 Plan Delta를 확정한 뒤 Implementation → Review loop로 진행하는 것이다.

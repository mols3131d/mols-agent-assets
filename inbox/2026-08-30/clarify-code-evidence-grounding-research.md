# Clarify Code — Evidence Grounding Research

이 문서는 기존 [Clarify Code Enhancement Research](clarify-code-enhancement-research.md)와 후속 comment-recall review를 전제로, `clarify-code`가 필요한 comment를 적극적으로 생성하면서도 **근거 없는 rationale를 source code에 굳히지 않도록** 하는 후속 RPI Research artifact입니다.

## Goal

`clarify-code`가 다음 두 실패를 동시에 피하게 합니다.

1. **false negative** — durable한 hidden contract·constraint·consequence가 있는데도 comment/docstring을 만들지 않음
2. **fabricated explanation** — 이상하거나 비자명한 code를 보고 그럴듯한 rationale를 추측해 comment/docstring으로 고정함

이번 loop는 comment 수를 늘리거나 줄이는 작업이 아닙니다. **필요한 explanation의 recall을 유지하면서 factual grounding을 강화하는 것**이 목적입니다.

## Active Scope

### In scope

- explanation을 쓰기 전 evidence 확인
- mutation/write scope와 evidence/read scope 구분
- positive comment recall을 core에서 유지하는 방법
- `SKILL.md`와 `references/documentation.md`의 loading boundary 재설계
- evidence-backed discovery와 insufficient-evidence capability case

### Out of scope

- executable code refactoring
- frontmatter routing 확대
- 새 deployable reference 추가
- comment density/coverage metric
- stale-comment analyzer나 external runtime
- user-facing standalone documentation

## Evidence

### Repository instruction design

Repository의 Instruction Design은 중요한 행동을 `Condition → Behavior → Boundary → Validation / Stop`으로 복원할 수 있어야 하고, 필수 행동은 rationale나 example에 암시하지 말고 직접 쓰라고 합니다. 서로 의존하는 condition, behavior, boundary도 가능한 가까이 둡니다.

따라서 `clarify-code`의 핵심 positive behavior와 evidence boundary는 항상 로드되는 core에서 확인할 수 있어야 합니다. 세부 placement·projection·machine-consumed surface처럼 실제로 조건부인 내용만 reference에 두는 편이 맞습니다.

### Repository Skill package convention

Repository의 Skill Authoring Conventions와 `mols-agent-asset` Skill reference는 single-file Skill을 기본으로 하고, supporting resource는 조건부 loading이나 별도 runtime benefit이 있을 때 사용합니다.

현재 `clarify-code`는 모든 실제 prose 판단에서 `documentation.md`를 읽도록 되어 있습니다. 이 상태에서는 reference의 loading boundary가 사실상 사라집니다.

따라서 recall 보정에 꼭 필요한 positive signal은 core로 가져오고, `documentation.md`를 다시 **tricky judgment를 위한 conditional detail**로 만드는 것이 KISS/Progressive Disclosure에 더 부합합니다.

### Google engineering guidance

Google Engineering Practices는 reviewer가 code를 이해하지 못할 때 먼저 code 자체를 명확히 하고, code로 명확히 할 수 없으면 그 이유를 설명하는 code comment를 추가하라고 안내합니다. Comments는 보통 code가 무엇을 하는지보다 **code 자체에 담기 어려운 decision reasoning**을 전달할 때 유용하다고 봅니다.

Google의 documentation best practices는 API/documented behavior를 contract로 보고, 그런 behavior는 test가 검증하는 것이 합리적인 경우가 많다고 설명합니다.

이 두 guidance를 함께 보면 explanation은 자유로운 추측문이 아니라 **현재 code/contract에서 유지해야 할 의미의 projection**으로 보는 편이 자연스럽습니다.

Sources:

- Google Engineering Practices, *What to look for in a code review* — https://google.github.io/eng-practices/review/reviewer/looking-for.html
- Google Documentation Best Practices — https://google.github.io/styleguide/docguide/best_practices.html
- Google Go Style Guide, *Why is the code doing what it does?* — https://google.github.io/styleguide/go/guide.html

### LLM-generated comment의 assumption risk

Dhakal et al.의 2026년 code-comment improvement 연구는 LLM-generated text에 training이나 prompt에서 유래한 content assumptions가 포함될 수 있으며, comment가 무엇을 말해야 하는지 empirical foundation이 부족할 수 있다는 문제를 지적합니다.

이 연구가 모든 LLM comment가 hallucination이라는 뜻은 아닙니다. 하지만 `clarify-code`가 비자명한 code를 보고 **그럴듯한 이유를 만들어내는 것**을 명시적으로 방지해야 한다는 근거로는 충분합니다.

Source:

- Dhakal et al., *A Grounded Theory Study to Guide AI-Driven Code Comment Improvement*, Journal of Software: Evolution and Process, 2026 — https://onlinelibrary.wiley.com/doi/10.1002/smr.70157

### 기존 comment-quality research와의 연결

기존 Research에서 code-comment inconsistency와 stale comment는 후속 maintainer를 오도할 수 있는 문제로 확인했습니다. Fabricated rationale는 이보다 더 직접적인 위험입니다. 처음부터 사실이 아닌 설명이 source에 들어가면 이후 reader에게 **잘못된 evidence**로 기능할 수 있기 때문입니다.

따라서 comment quality의 consistency는 단순히 "현재 code와 문장이 맞는가"뿐 아니라 **그 문장의 semantic claim을 지지하는 current evidence가 있는가**까지 포함해 보는 것이 안전합니다.

## Decision Model

### 1. Candidate meaning을 먼저 발견한다

Positive signal은 유지합니다.

- hidden caller contract
- invariant / local constraint
- ordering consequence
- external system/protocol constraint
- intentional unusual choice
- durable rejected alternative
- file-local stable convention

이 단계는 comment를 바로 쓰는 단계가 아닙니다.

### 2. Evidence before Explanation

Candidate meaning을 explanation으로 고정하기 전에 current evidence로 확인합니다.

우선할 수 있는 evidence는 상황에 따라 다음과 같습니다.

- target code의 observable behavior와 data/control relation
- caller/call-site behavior
- regression/characterization test와 assertion
- canonical API/domain/specification contract
- current configuration, schema, protocol 또는 framework contract
- 같은 semantic owner의 이미 확립된 source documentation

Git history, issue, old discussion은 **후보 이유를 발견하는 supporting context**가 될 수 있지만 현재 invariant의 단독 authority로 취급하지 않습니다. Historical rationale를 comment로 남기려면 current code/contract에서도 여전히 유효한지 재확인합니다.

### 3. Evidence가 의미를 완전히 설명하지 못할 때

현재 behavior나 constraint는 확인할 수 있지만 historical "왜 이렇게 선택했는가"까지 확인할 수 없는 경우가 있습니다.

이때는 확인 가능한 현재 의미만 설명할 수 있습니다.

예:

```text
확인 가능: permission changes must be visible within the same request
확인 불가: 2024년에 cache bug 때문에 이 구현을 선택했다
```

Comment는 전자를 기록할 수 있지만 후자를 추측해 쓰지 않습니다.

### 4. 근거가 부족하면 uncertainty를 prose로 굳히지 않는다

비자명한 implementation이 있다는 사실만으로 rationale를 만들지 않습니다.

- evidence를 좁게 더 읽어 확인할 수 있으면 확인
- material reason을 확정할 수 없으면 unsupported explanation을 추가하지 않음
- 필요하면 "reason could not be established"를 작업 결과에 보고
- uncertainty 자체를 permanent source comment로 남기지 않음

`TODO: unclear why` 같은 comment도 사용자가 그 artifact를 명시적으로 원하거나 repository convention이 소유하지 않는 한 자동으로 만들지 않습니다.

## Read Scope vs Write Scope

`clarify-code`의 mutation authority는 code-adjacent prose에만 있습니다. 하지만 explanation의 사실성을 확인하려면 target 밖의 caller, tests, spec, config를 읽어야 할 수 있습니다.

따라서 다음을 분리합니다.

- **write scope** — 사용자가 지정하거나 task가 정한 source explanation surface
- **evidence/read scope** — explanation claim을 검증하기 위해 필요한 가장 좁은 caller/test/spec/config context

Evidence를 읽는다고 그 surface를 수정할 권한이 생기지 않습니다.

이 구분은 repository `mols-agent-asset`의 "reading outside the write boundary does not grant write authority" 원칙과도 일치합니다.

## Owner before Nearness

기존 positive obligation의 "같은 의미가 가까운 surface에 없으면"이라는 표현은 약간 좁습니다.

더 정확한 판단은 다음입니다.

> 같은 의미가 **적절한 semantic owner에 충분히 존재하지 않거나**, caller/maintainer가 해당 지점에서 알아야 하는 local projection이 필요한 경우에만 explanation을 추가한다.

그 다음 placement 단계에서 locality를 사용합니다.

즉:

1. semantic owner가 어디인지 판단
2. local projection이 실제로 필요한지 판단
3. 필요하면 실제 scope에 가장 가까운 stable surface 선택

이 순서가 broad policy duplication을 더 잘 방지합니다.

## Progressive Disclosure Reassessment

후속 comment-recall loop에서는 positive signal을 놓치지 않기 위해 모든 prose 판단에서 `documentation.md`를 읽도록 강화했습니다. 그 변경은 당시 실제 failure evidence에 대한 합리적인 보정이었습니다.

하지만 현재 구조를 다시 보면 reference가 사실상 항상 로드됩니다. 이 경우 supporting resource를 분리한 loading benefit이 거의 없습니다.

해법은 reference를 다시 optional로 만드는 것이 아니라 **recall에 필수적인 정보를 core로 옮긴 뒤** optional로 만드는 것입니다.

### Core가 소유해야 하는 것

- executable-code handoff
- Explanation Value의 기본 gate
- Positive Signals의 compact 목록
- Evidence before Explanation
- caller docstring / maintainer comment 기본 선택
- no-fabrication / no-obvious-narration boundary
- stop condition

### `documentation.md`가 소유할 것

- placement/scope가 애매한 경우
- contract projection과 canonical owner 판단
- durable rejected alternative의 세부 boundary
- stale/history coupling 판단
- module-level explanation
- machine/runtime-consumed text

이렇게 하면 core만으로 common path가 동작하고, tricky surface만 reference를 읽는 실제 Progressive Disclosure가 복원됩니다.

## Eval Implication

현재 `implicit-maintainer-comment-discovery`는 사용자가 `comment`라고 말하지 않아도 comment를 선택하는지를 잘 검사합니다. 하지만 prompt가 rationale 자체를 이미 알려주므로 evidence discovery를 충분히 검사하지 못합니다.

다음 두 behavior를 추가로 보호해야 합니다.

### Evidence-backed discovery

- user는 maintainability 개선만 요청
- target code에는 explanation이 없음
- nearby regression test/caller/spec가 hidden ordering/contract를 증명
- Skill은 그 evidence를 연결해 comment/docstring을 추가
- executable code는 변경하지 않음

### Insufficient evidence

- unusual implementation은 보임
- caller/test/spec/config 어디에도 reason을 뒷받침하는 evidence가 없음
- Skill은 plausible rationale를 invent하지 않음
- unsupported comment를 추가하지 않음
- 필요한 경우 evidence gap을 report

이 둘은 recall과 grounding의 균형을 직접 검증합니다.

## Final Findings

### P1 — Evidence before Explanation

필수입니다. Positive recall을 높인 현재 Skill에서 fabricated rationale risk를 막는 핵심 boundary입니다.

### P1 — Core positive signals + conditional reference

현재 always-load reference는 package convention과 Progressive Disclosure benefit이 약합니다. Positive signal과 evidence gate를 core로 올리고 reference를 tricky judgment용으로 돌리는 것이 더 작고 안정적입니다.

### P1 — Evidence-backed / insufficient-evidence eval pair

Positive generation과 no-fabrication을 동시에 보호해야 합니다.

### P2 — write scope와 evidence/read scope를 명시적으로 분리

설명 claim을 검증하기 위한 읽기는 허용하되 mutation scope는 넓히지 않습니다.

## Research Limitations

- Google guidance는 특정 조직/언어 ecosystem의 style guidance이며 universal syntax rule은 아닙니다.
- Dhakal et al.의 연구는 comment-improvement procedure를 위한 empirical study로, 모든 LLM-generated comment의 factual error rate를 측정한 연구는 아닙니다.
- 따라서 이번 loop는 특정 comment format이나 evidence hierarchy를 강제하지 않고 **unsupported semantic claim을 source에 고정하지 않는 portable boundary**만 가져옵니다.

## Status

Follow-up Research complete. 새 evidence는 기존 comment-recall 방향을 뒤집지 않고 **recall + grounding**으로 보강해야 한다는 결론을 지지합니다.
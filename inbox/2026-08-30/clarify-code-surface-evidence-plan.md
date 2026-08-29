# Clarify Code — Surface and Evidence Plan

이 계획은 `clarify-code-surface-evidence-research.md`의 findings를 구현하고, 반복 Review로 수렴시키기 위한 RPI Plan입니다.

## Goal

기존 `clarify-code`의 comment recall, anti-spam, no-fabrication, executable-code boundary를 보존하면서 다음 세 gap을 닫습니다.

1. information signal과 explanation surface를 잘못 1:1로 묶는 문제
2. explicit current task fact의 evidence 역할이 불명확한 문제
3. conflicting-evidence behavior가 capability eval로 보호되지 않는 문제

## Preserve

- `clarify-code`는 code-adjacent prose만 수정
- executable naming/representation/control/state/abstraction 변경은 `code-comprehension-refactor`
- user-facing standalone documentation은 별도 capability
- comment quantity는 quality proxy가 아님
- evidence-backed durable meaning이 있으면 comment/doc explanation을 회피하지 않음
- unsupported rationale를 invent하지 않음
- broad policy를 local source에 중복 소유하지 않음
- machine/runtime/tool-consumed source text는 별도 contract로 취급

## Implementation

### 1. `SKILL.md` — Surface decision model 교정

`Default Explanation Signals`를 **Default Explanation Decisions**로 바꿉니다.

Surface 선택 owner는 information type 자체가 아니라 `reader + semantic scope`입니다.

권고 형태:

| Reader / scope | High-value meaning | Default surface |
| --- | --- | --- |
| caller | hidden call semantics, precondition, side effect, exception/failure semantics, caller-visible protocol constraint | repository/language-native caller-facing API documentation surface |
| maintainer | invariant, local constraint, implementation ordering/failure consequence, external implementation constraint, durable rejected alternative | code-local comment |
| file/package maintainer | stable convention that applies beyond one symbol | module/package-level documentation surface |

`docstring`은 Python에서의 example로만 남기고 portable responsibility name으로 사용하지 않습니다.

Workflow의 surface selection step도 같은 owner를 사용합니다.

### 2. `SKILL.md` — Evidence contract 정교화

Grounding step에 다음을 흡수합니다.

- target behavior/caller/test/canonical contract/current config/schema/protocol
- **explicit current task에서 제공된 domain/operational fact**

User-provided fact는 evidence candidate이며 무조건 canonical authority가 아닙니다.

다음 boundary를 함께 둡니다.

- applicable canonical/current evidence와 material conflict가 없으면 explanation grounding에 사용할 수 있음
- conflict가 있으면 한쪽을 조용히 canonize하지 않음
- source prose에는 provenance story가 아니라 current semantic만 남김

Grounding behavior를 같은 workflow 근처에서 한 번 소유하고, Boundary의 duplicate wording은 필요한 no-fabrication invariant만 유지합니다.

### 3. `documentation.md` — Language-neutral caller documentation

`Docstrings` section을 `Caller-Facing API Documentation`으로 변경합니다.

핵심:

- caller가 사용 전에 알아야 하는 hidden contract를 language/repository-native declaration documentation surface에 둠
- Python docstring, Go/Rust/Java documentation comment는 ecosystem-specific examples
- language syntax 자체는 current project convention이 소유
- caller-visible external protocol/failure semantics를 body comment로 숨기지 않음

기존 Python example은 유지 가능하지만 Python-only contract처럼 읽히지 않게 framing합니다.

### 4. `documentation.md` — Grounding authority

Grounding evidence list에 explicit current task fact를 추가합니다.

구분:

- current code/test/spec/config와 일치하는 explicit operational fact → usable evidence candidate
- conflict하는 user statement → inconsistency/uncertainty, silent canonization 금지
- Git history/old issue → supporting context only

Evidence hierarchy 점수나 fixed precedence table은 만들지 않습니다. Semantic owner와 applicable authority가 context별로 다르기 때문입니다.

### 5. Capability eval 3개 추가

#### `caller-visible-protocol-doc-surface`

Go 또는 유사 language-native declaration doc surface가 필요한 case.

Assert:

- caller-visible protocol restriction을 API documentation surface에 둠
- maintainer-only body comment에 숨기지 않음
- exact syntax는 language/repository convention을 따름
- executable code 변경 없음

#### `user-provided-current-constraint`

User가 explicit current operational constraint를 제공하고 current code/context와 conflict가 없는 case.

Assert:

- user-provided current fact를 evidence candidate로 사용
- durable maintainer meaning이면 comment를 실제 생성/개선
- 별도 repository artifact가 없다는 이유만으로 no-op하지 않음
- unsupported extra rationale는 invent하지 않음

#### `conflicting-evidence-no-canonization`

Current sources가 material하게 충돌하는 case.

Assert:

- conflict를 식별
- 한 source를 임의 winner로 선택하지 않음
- unresolved semantic을 permanent comment/API docs로 고정하지 않음
- executable code 변경 없음

## Review Loop

### Loop A — Surface model

확인:

- external/failure/ordering meaning이 caller-facing일 때 API docs로 갈 수 있는가
- maintainer-only일 때 local comment를 유지하는가
- Python-specific wording이 portable contract를 다시 좁히지 않는가
- module/package-level surface가 symbol-level contract와 섞이지 않는가

Material gap이 있으면 bounded implementation correction 후 재리뷰합니다.

### Loop B — Evidence authority

반례:

- user statement만 있고 code와 모순 없음
- user statement와 test가 충돌
- user statement와 canonical protocol contract가 충돌
- historical reason만 있고 current invariant는 확인됨
- code shape만 unusual하고 아무 rationale evidence 없음

목표는 recall과 no-fabrication을 동시에 보존하는 것입니다.

### Loop C — Context economy / instruction quality

확인:

- 같은 grounding rule이 core에서 여러 owner를 갖지 않는가
- common-path decision은 core에 남았는가
- tricky detail만 `documentation.md`에 남았는가
- conditional reference의 load condition이 실제로 존재하는가
- table/example이 숨은 normative rule을 만들지 않는가

### Loop D — Eval coverage

Positive / negative / near-miss를 대조합니다.

- positive: caller docs, maintainer comment, implicit discovery, explicit user evidence
- negative: obvious/no-net-value, unsupported rationale, structural handoff
- conflict: unresolved evidence
- machine-consumed surface
- portability: non-Python API doc surface

Fixture가 wording을 과도하게 고정하지 않고 behavior contract를 평가하는지 봅니다.

## Validation

- changed Skill/reference/eval static inspection
- `code-comprehension-refactor` overlap comparison
- frontmatter description unchanged 여부 확인
- generated route 추가 delta 불필요 여부 확인
- PR Gate deterministic tests
- model/runtime capability eval이 실제로 실행되지 않으면 미실행으로 기록

## Stop Conditions

다음이 모두 충족되면 수렴합니다.

- surface selection이 reader/scope 중심으로 일관됨
- portable API documentation responsibility가 Python syntax에 종속되지 않음
- explicit current task fact를 사용할 수 있으면서 conflict 시 canonization하지 않음
- conflicting-evidence behavior가 fixture로 보호됨
- prior recall/anti-spam/no-fabrication behavior가 약화되지 않음
- 새 file/package abstraction 불필요
- substantive Review에서 추가 P1/P2가 나오지 않음

새 finding이 나오면 가장 이른 prerequisite로 돌아가며, 같은 내용을 문구만 바꾸는 no-op loop는 수행하지 않습니다.

## Planned Diff

```text
src/rulesync/.rulesync/skills/clarify-code/
├── SKILL.md
└── references/
    └── documentation.md

evals/skills/clarify-code/
└── cases.json
```

Research/Plan/Review artifact는 `inbox/2026-08-30/`에서 maintainer evidence로만 유지합니다.

## Status

Plan accepted for bounded Implementation → Review recursion.

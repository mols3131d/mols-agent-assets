---
title: Skill Target Profiles
description: 이 저장소의 Skill target profile, flat/runtime 경계와 package surface convention
---

# Skill Target Profiles

이 문서는 [Personal Skill Standard](agent-assets-skills-standard-personal.md)가
위임한 **repository-local target profile과 package surface 상세 규격**을 소유한다.

> `skills/`, `skills-chatbot/`, `skills-chatbot-runtime/`은 Agent Skills specification의 공식 분류가 아니다.

## Profiles

| Profile | Target |
| --- | --- |
| `skills/` | workspace/filesystem/shell/repository authority가 있는 agent runtime |
| `skills-chatbot/` | self-contained single Markdown만 받는 flat chatbot harness |
| `skills-chatbot-runtime/` | bundle, progressive loading, host-specific runtime surface를 활용하는 hosted chatbot runtime |

같은 capability가 여러 profile에 존재할 수 있다. target harness가 서로 독립된 payload를 요구한다면 이 semantic overlap은 의도적인 projection이며 DRY 위반으로 보지 않는다.

최적화 단위는 **`capability × target profile`**이다.

## Flat vs Runtime

`skills-chatbot/`은 다음을 모두 만족할 때 사용한다.

1. `<skill-name>.skill.md` 한 파일로 완결된다.
1. 배포 파일이 `<4,000 tokens`다.
1. 별도 runtime-required bundle이나 host-specific package surface가 필요하지 않다.

Skill이 host가 이미 제공하는 tool이나 connector를 사용하도록 지시한다는 사실만으로 runtime profile이 되는 것은 아니다. 필요한 행동 계약이 한 Markdown 파일에 완결되면 flat profile을 우선한다.

그 외에는 `skills-chatbot-runtime/`을 사용한다. 예를 들어 references/assets/scripts, host-specific tool schema나 integration resource, progressive loading 등 단일 Markdown 밖의 runtime surface가 실제 capability에 필요할 때다.

`<4,000 tokens`는 이 저장소의 로컬 budget이며 외부 표준이 아니다.

### Flat Markdown Structure

Flat chatbot Skill은 **여러 Markdown 문서의 책임을 한 파일에 평탄화한 payload**로 본다. Heading은 장식이 아니라 responsibility boundary다.

**`# ≈ one Markdown file`**을 기본 heuristic으로 사용한다. Flat 제약이 없다면 별도 `.md` 파일로 분리해도 자연스러운 top-level responsibility가 둘 이상일 때 복수의 `#`을 권장한다.

- 모든 heading은 하나의 명확한 책임을 가진다. 독립 책임은 나누되 의미 없는 미세 분할은 하지 않는다.
- `##` 이하는 부모 책임을 점진적으로 분해한다.
- 같은 depth는 가능한 한 비슷한 추상화 수준을 유지한다.
- 공통 invariant는 가장 가까운 공통 상위 boundary에 한 번만 둔다.
- 단순한 Skill은 하나의 `#`으로 충분하다.
- target harness의 mandatory heading contract가 있으면 그것을 우선한다.

#### Front Matter Triggering

Flat Skill의 activation 정보는 **front matter `description`에 집중한다**. Discovery 단계에서 body보다 먼저 선택에 쓰이는 정보이므로, `description`만으로 다음을 구분할 수 있게 작성한다.

- Skill이 제공하는 capability;
- 어떤 user intent/task context에서 사용해야 하는지;
- 인접 capability와 혼동될 가능성이 있을 때의 핵심 negative boundary;
- follow-up continuity나 target 전환처럼 selection을 바꾸는 조건이 실제로 중요할 때 그 조건.

`description`은 **selection contract**다. 다른 Skill을 먼저 또는 함께 사용해야 하는 조건, prerequisite, fallback, handoff, execution order 같은 routing/orchestration은 넣지 않고 본문에서 다룬다.

본문은 이미 Skill이 선택·활성화되었다고 가정한다. 따라서 `Trigger`, `Activation`, `When to use` 같은 별도 activation 섹션을 두거나 front matter의 조건을 본문에서 반복하지 않는다. 본문에는 필요한 routing을 포함해 contract, procedure, constraints, boundary, output처럼 **활성화 이후의 행동**만 둔다.

활성화 후 새로 얻은 evidence에 따라 적용 범위를 축소·중단·재평가해야 하는 runtime guardrail은 selection trigger가 아니다. 이런 규칙은 본문에 남긴다.

Portable front matter field와 constraint는 [Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)을 따른다. 특정 target이 별도 discovery contract를 강제하면 그 target contract가 우선한다.

형태 예시이며 고정 schema가 아니다.

```markdown
# Contract

# Procedure

## Resolve

## Apply

# Output
```

## Directory-Based Package

```text
skill-name/
├─ SKILL.md
├─ references/          # runtime when needed
├─ scripts/             # runtime when needed
├─ assets/              # runtime when needed
└─ .docs/               # non-runtime maintainer surface
   └─ baseline/          # durable intent / requirements / decisions
```

- runtime behavior에 필요한 resource는 non-dot surface에 둔다.
- dot-prefixed directory는 packaging/deployment에서 제외하는 non-runtime maintainer surface로 사용한다.
- repository root `docs/`는 이 convention의 대상이 아니다.
- `.evals/`, `.tests/` 같은 추가 non-runtime surface는 실제 필요가 있을 때만 둔다.

## `.docs/baseline/`

`.docs/baseline/`은 반복 개선 과정에서 잃으면 안 되는 **본래 purpose, requirements, invariants, major decisions와 recovery directives**를 보존한다.

넣는다:

- durable purpose와 success boundary
- behavioral invariants와 non-goals
- 사용자가 채택한 중요한 design decision
- 복구 시 필요한 compatibility contract

넣지 않는다:

- 현재 작업 로그
- 임시 조사
- 쉽게 재생성되는 상태
- runtime이 반드시 읽어야 하는 지식

Baseline은 단순 refactor나 문구 변경으로 갱신하지 않는다. 의도·요구사항·불변조건이 실제로 바뀔 때만 함께 바꾼다.

필요하면 [Baseline Directive Template](agent-assets-skills-baseline-directive-template.md)을
초기 maintainer document로 사용할 수 있다. Template 자체는 mandatory schema가 아니다.

## Context-Only Naming

주책임이 workflow가 아니라 상황별 context discovery/loading이면 `load-context-<topic>` naming을 검토한다.

이 naming은 repository-local convention이다. 실제 구현·mutation·검증·최종 output까지 소유하는 Skill에는 사용하지 않는다.

### Activation Classes

Context-only Skill은 activation intent에 따라 다음 두 종류로 운용할 수 있다.

- **Scope baseline loader** — 선언한 work surface가 활성화되면 항상 로드한다. 전역 지침을 비대하게 만들지 않으면서 특정 scope에서 반복 적용할 판단 기준과 제약을 제공한다.
- **Conditional loader** — 해당 topic 안에서도 추가 조건이 충족될 때만 로드한다.

Scope baseline loader의 넓은 trigger는 그 scope 내부에서 **의도된 coverage**다. 일반적인 narrow capability Skill과 같은 기준으로 trigger를 축소하거나, scope 내부 activation이 넓다는 이유만으로 Rule로 이동하지 않는다. 전역 Rule로 올렸을 때 무관한 task까지 context cost를 부담한다면 scope baseline loader가 더 적절할 수 있다.

Scope baseline loader의 front matter는 가능한 한 다음을 분명히 한다.

- 어떤 work surface에서 항상 적용되는가;
- 단순하거나 routine한 task도 포함되는가;
- 어떤 인접 scope는 제외되는가.

Review에서는 먼저 activation class를 확인한다.

- scope baseline loader → **narrowness가 아니라 coverage와 leakage**를 평가한다.
- conditional loader → 조건의 precision과 불필요한 activation을 평가한다.
- 두 유형 모두 downstream workflow, mutation, verification, final output을 가져오지 않는지 확인한다.

개인 관행을 범용 loader와 분리할 때는 `load-context-<topic>-<owner>`를 personal overlay로 사용한다.

Personal overlay activation은 conversation이나 connection 전체가 아니라 **현재 target별로** 판단한다.

- base loader는 해당 topic의 context loading이 필요하면 적용한다.
- personal overlay는 target이 해당 owner의 개인 관행으로 관리된다는 근거가 있을 때만 추가한다.
- 단순 access, membership, admin permission, authorship, collaboration은 personal scope의 근거가 아니다.
- 여러 target이 섞이면 personal target에만 overlay를 적용한다.
- personal scope가 불명확하면 근거가 생길 때까지 base만 적용한다.

예: `load-context-github` + `load-context-github-mols`, `load-context-notion` + `load-context-notion-mols`.

## Boundary

Portable `SKILL.md`와 front matter 규격은
[Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)이
소유한다. 이 문서는 target profile에 필요한 repository-local extension만 정의한다.

Skill을 분리할지는 파일 길이가 아니라 activation intent와 responsibility로 판단한다. 세부 지식만 조건부로 달라진다면 별도 Skill보다 runtime `references/`를 먼저 검토한다.

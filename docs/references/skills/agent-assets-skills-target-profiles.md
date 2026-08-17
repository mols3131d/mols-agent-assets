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
| `skills-chatbot-runtime/` | bundle, tools, connectors, progressive loading을 활용하는 hosted chatbot runtime |

같은 capability가 여러 profile에 존재할 수 있다. target harness가 서로 독립된 payload를 요구한다면 이 semantic overlap은 의도적인 projection이며 DRY 위반으로 보지 않는다.

최적화 단위는 **`capability × target profile`**이다.

## Flat vs Runtime

`skills-chatbot/`은 다음을 모두 만족할 때 사용한다.

1. `<skill-name>.skill.md` 한 파일로 완결된다.
1. 배포 파일이 `<4,000 tokens`다.
1. runtime-required bundle이나 host-only capability가 필요하지 않다.

그 외에는 `skills-chatbot-runtime/`을 사용한다. `<4,000 tokens`는 이 저장소의 로컬 budget이며 외부 표준이 아니다.

### Flat Markdown Structure

Flat chatbot Skill은 하나의 일반 문서보다 **여러 책임을 한 payload에 평탄화한 Markdown**에 가깝게 작성한다.

모든 heading은 명확한 **responsibility boundary**를 가져야 하며, heading depth는 단순한 시각적 계층이 아니라 책임의 포함 관계와 규모를 나타낸다.

특히 `#`은 일반 문서의 제목이 아니라 **Markdown 파일 하나에 대응할 정도의 top-level responsibility**로 취급한다. Flat 제약이 없다면 별도 Markdown 문서로 분리해도 자연스러운 수준의 응집된 책임에는 복수의 `#` 사용을 권장한다.

- `#`은 file-level cohesion을 가진 하나의 top-level responsibility를 소유한다.
- `##`는 해당 `#` 안의 major responsibility, 더 낮은 heading은 그 책임을 다시 분해한 하위 responsibility를 소유한다.
- 같은 depth의 heading은 가능한 한 비슷한 추상화 수준을 유지한다.
- 하나의 heading이 서로 독립적인 책임을 함께 소유하면 나누고, 분리하면 의미나 흐름이 깨지는 책임은 억지로 쪼개지 않는다.
- 공통 invariant를 여러 책임에 반복하지 않는다. 가장 자연스러운 공통 상위 boundary에 둔다.
- 문서 제목 하나를 만들기 위해 모든 top-level responsibility를 `##` 아래로 강제하지 않는다.
- 단순한 Skill은 하나의 `#`만 사용해도 된다.
- target harness가 heading 구조를 강제하면 해당 mandatory contract가 이 권장보다 우선한다.

예:

```markdown
# Contract

...

# Procedure

## Resolve

...

## Apply

...

# Output

...
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

## Boundary

Portable `SKILL.md`와 front matter 규격은
[Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)이
소유한다. 이 문서는 target profile에 필요한 repository-local extension만 정의한다.

Skill을 분리할지는 파일 길이가 아니라 activation intent와 responsibility로 판단한다. 세부 지식만 조건부로 달라진다면 별도 Skill보다 runtime `references/`를 먼저 검토한다.

---
description: AI agent가 task intent에 따라 선택하는 Skill의 역할과 이 repository의 Rulesync authoring 및 Skills CLI dependency 정책을 판단할 때 사용하는 문서입니다.
---

# Skill

Skill은 **task intent에 따라 선택적으로 불러오는 지침, workflow 또는 reusable capability**입니다.

`SKILL.md`는 Skill package에서 사용할 수 있는 표준적인 entry surface이지, 이 repository에서 Skill의 출처나 ownership을 구분하는 이름이 아닙니다. Skill을 설명할 때는 **어디서 작성·관리되는가**와 **어떻게 설치·사용되는가**를 분리합니다.

## Source Policy

이 repository의 Skill은 크게 두 경로로 사용합니다.

| 구분 | Policy |
| --- | --- |
| 이 repository에서 직접 작성·관리하는 reusable Skill | **Rulesync Skill**을 canonical source로 사용 |
| 외부에서 가져와 dependency로 사용하는 Skill | 필요하면 **[skills CLI](../../references/tooling/skills-cli.md)**로 설치 가능 |

직접 관리하는 Skill은 Rulesync source를 수정하며 generated vendor projection을 별도의 작성 원본으로 다루지 않습니다.

외부 Skill은 Rulesync로 가져오는 것이 단순하고 원본 구조를 충실히 보존할 때 Rulesync declarative source를 사용할 수 있습니다. 반대로 repackaging이나 resource 손실 보완이 필요해지는 등 Rulesync 경유가 불필요하게 복잡하면 `skills add` 같은 Skill-native installer를 사용할 수 있습니다. 외부 dependency를 설치했다는 이유만으로 이 repository가 그 Skill의 작성 권한을 인수하지 않습니다.

세부 기준은 [작성 원본과 권한](../source-authority.md)이 소유합니다.

## When to Use

Skill을 우선 검토하는 경우:

- 사용자 요청이나 task intent가 applicability를 결정합니다.
- 특정 작업에서만 필요한 지침을 항상 로드하고 싶지 않습니다.
- 여러 repository나 runtime에서 재사용할 workflow 또는 capability가 있습니다.
- 설명뿐 아니라 반복 가능한 판단 절차, 도구 사용법 또는 supporting resource가 함께 필요합니다.

다음은 Skill보다 다른 surface가 적합합니다.

| 필요 | 사용 |
| --- | --- |
| repository 전체에 항상 필요한 지침 | root `AGENTS.md` |
| 특정 디렉터리 계층에 적용되는 지침 | 해당 범위의 `AGENTS.md` |
| path, glob, 파일 종류처럼 구조적 조건으로 적용되는 지침 | [Rule](rule.md) |

## Selection and Loading

Skill은 catalog 전체를 선로드하기보다 `name`과 `description` 같은 discovery metadata로 task relevance를 판단한 뒤 필요한 source만 읽는 것을 기본으로 합니다.

- task와 관련 없는 Skill은 로드하지 않습니다.
- 서로 다른 책임이 독립적으로 필요하면 여러 Skill을 선택할 수 있습니다.
- task intent가 실질적으로 바뀌면 applicability를 다시 평가합니다.
- routing index나 installed copy는 discovery 또는 dependency state이며 canonical Skill body를 대체하지 않습니다.

정확한 discovery와 invocation semantics는 실제 target 또는 harness의 current contract를 따릅니다.

## Standard and Runtime Boundary

공통 `SKILL.md` package contract가 필요하면 [Agent Skills Specification](../../references/agent-assets/skills/specification.md)을 통해 현재 표준을 확인합니다. 이 repository는 표준 field, path, limit 또는 vendor별 runtime behavior를 별도 local schema로 복제하지 않습니다.

- repository-authored canonical Skill → Rulesync source
- external dependency authority → upstream source와 installer/lock state
- 공통 Skill package contract → applicable Agent Skills standard
- target-specific discovery, metadata, permissions, runtime behavior → 해당 target/harness
- repository-local authoring convention → [Skill Authoring Conventions](../../references/agent-assets/skills/skill-authoring-conventions.md)

## Boundary

- Rulesync workspace와 projection → [Rulesync](../../references/tooling/rulesync.md)
- external Skill dependency와 skills CLI → [skills CLI](../../references/tooling/skills-cli.md)
- 작성 원본과 dependency authority → [작성 원본과 권한](../source-authority.md)
- Skill specification source routing → [Agent Skills Specification](../../references/agent-assets/skills/specification.md)
- behavioral verification → [Evaluation](../evaluation.md)

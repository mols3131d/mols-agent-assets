---
description: AI agent 지침을 path, glob, 파일 종류 같은 구조적 범위에 적용할 때 Rule을 선택하고 작성 원본과 적용 경계를 판단하는 정책입니다.
---

# Rule

Rule은 **task intent가 아니라 repository 구조를 기준으로 적용 범위를 정하는 지침 surface**입니다.

이 repository에서는 공통 하위 디렉터리, 파일 종류, 확장자처럼 여러 위치에 반복되는 범위를 하나의 selector로 표현할 수 있을 때 Rule을 사용합니다. 특정 runtime의 selector 문법이나 precedence는 해당 runtime 또는 Rulesync의 current contract를 따릅니다.

Rule과 Skill은 **담고 있는 내용이 아니라 적용 방식으로 구분**합니다. Skill 중에도 workflow나 capability뿐 아니라 Rule처럼 정책, 제약, 판단 기준 같은 지침을 제공하는 것이 있습니다. 이 repository는 이런 **instruction-oriented Skill**도 적극적으로 사용합니다.

- path, glob, 파일 종류처럼 구조적 조건이 적용 여부를 결정하면 Rule입니다.
- task intent와 의미적 relevance가 적용 여부를 결정하면, 내용이 지침 중심이어도 Skill입니다.

따라서 "지침이면 Rule, workflow면 Skill"로 구분하지 않습니다.

## When to Use

Rule을 우선 검토하는 경우:

- 같은 종류의 파일에 동일한 지침이 반복해서 필요합니다.
- 여러 디렉터리에 공통된 하위 구조가 있고 같은 정책을 적용해야 합니다.
- 적용 여부를 task 의미보다 path, glob, extension 같은 구조적 조건으로 안정적으로 결정할 수 있습니다.
- 여러 `AGENTS.md`에 같은 내용을 복제하는 것보다 하나의 scoped Rule이 책임을 더 명확하게 소유합니다.

다음은 Rule보다 다른 surface가 적합합니다.

| 필요 | 사용 |
| --- | --- |
| repository 전체에 항상 필요한 지침 | root `AGENTS.md` |
| 하나의 디렉터리 계층에 자연스럽게 상속되는 지침 | 해당 범위의 `AGENTS.md` |
| 작업 의미에 따라 선택해야 하는 지침, workflow 또는 capability | [Skill](skill.md) |

## Authoring Policy

이 repository에서 여러 target에 재사용할 Rule을 직접 작성·관리할 때 기본 canonical authoring surface는 **Rulesync**입니다.

- Rulesync source를 작성 원본으로 선택했다면 그 source만 사람이 수정합니다.
- 생성된 vendor projection은 파생 결과이며 별도의 policy authority로 관리하지 않습니다.
- target별 selector, attachment, precedence와 지원 범위는 실제 Rulesync와 target runtime contract를 따릅니다.
- 같은 requirement가 여러 곳에 보인다는 이유만으로 즉시 deduplicate하지 않습니다. scope, selector, inheritance 또는 projection 차이가 실제 적용에 필요한지 먼저 확인합니다.
- 특정 vendor-native source가 실제 책임을 더 정확하게 보존해야 하는 경우에는 [작성 원본과 권한](../source-authority.md)의 기준으로 source를 선택합니다.

## Design Guidance

좋은 Rule은 **적용 범위를 읽고 예측할 수 있어야 합니다.**

- selector는 실제 공통 책임을 나타내야 합니다.
- unrelated path를 한 Rule에 묶어 context를 절약하지 않습니다.
- 예외가 많아지면 selector를 복잡하게 확장하기보다 책임 분리가 필요한지 다시 봅니다.
- Rule을 단순한 문서 재사용 수단으로 만들지 않습니다. 구조적 scope가 없으면 다른 surface가 더 적합합니다.

## Boundary

- Rule의 source/target authority와 projection → [Rulesync](../../references/tooling/rulesync.md)
- 작성 원본 선택 → [작성 원본과 권한](../source-authority.md)
- Agent Asset 공통 설계 → [Agent Assets](../../references/agent-assets/README.md)
- Rule authoring 또는 material change 작업의 세부 판단은 repository Skill `mols-agent-asset`의 Rule guidance를 사용합니다.
- 실제 runtime selection과 precedence는 static 문서만으로 검증되었다고 간주하지 않습니다.

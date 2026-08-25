---
description: AI agent용 repository instruction surface를 선택하고 Rule과 Skill의 책임 경계를 찾을 때 사용하는 development entrypoint입니다.
---

# AI Agent

이 디렉터리는 **이 repository에서 AI agent에게 지침과 재사용 가능한 동작을 제공할 때 어떤 surface를 선택할지** 정리합니다.

벤더별 파일 형식, selector, discovery, precedence와 runtime 동작은 여기서 다시 정의하지 않습니다. 작성 원본과 권한은 [작성 원본과 권한](../source-authority.md), Rulesync integration은 [Rulesync](../../references/tooling/rulesync.md), 대상별 동작은 실제 runtime의 current contract를 따릅니다.

## Surface Selection

| 필요 | 기본 surface |
| --- | --- |
| repository 전체에 항상 필요한 지침 | root `AGENTS.md` |
| 특정 디렉터리 계층에 적용되는 지침 | 해당 범위의 `AGENTS.md` |
| 공통 하위 디렉터리, 파일 종류, glob/path 조건에 반복 적용되는 지침 | [Rule](rule.md) |
| task intent에 따라 선택적으로 불러올 지침·workflow·capability | [Skill](skill.md) |

핵심 기준은 **어디에 적용되는가**와 **어떤 작업에서 필요한가**를 구분하는 것입니다.

- 경로가 적용 범위를 결정하면 Rule을 우선 검토합니다.
- task intent가 선택을 결정하면 Skill을 우선 검토합니다.
- 단순히 문서를 나누기 위해 Rule이나 Skill을 만들지 않습니다.

## Documents

- [Rule](rule.md) — path, glob, 파일 종류처럼 구조적으로 반복되는 범위에 적용하는 지침
- [Skill](skill.md) — task intent에 따라 선택되는 지침, workflow, reusable capability

## Boundary

- 작성 원본 선택과 외부 자산 dependency 정책 → [작성 원본과 권한](../source-authority.md)
- Rulesync workspace, source/derived boundary와 target projection → [Rulesync](../../references/tooling/rulesync.md)
- Agent Asset 설계 원칙 → [Agent Assets](../../references/agent-assets/README.md)
- verification → [Testing](../testing.md), [Evaluation](../evaluation.md)

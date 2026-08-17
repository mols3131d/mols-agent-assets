---
title: Common Agent Asset References
description: 에이전트 자산 전반에 공통으로 적용되는 표준, 설계 원칙, 작성법, 개념과 도구 레퍼런스
---

# Common Agent Asset References

`common/`은 Rule, Skill, Prompt, Agent에 **공통으로 적용되는 지식만** 소유한다.

자산 유형 하나에만 적용되는 규격은 해당 유형 디렉터리로 둔다. 공통 문서가 타입별 세부 규격을 다시 정의하지 않는다.

## Structure

| Directory | Responsibility |
| --- | --- |
| `standards/` | 자산 유형의 공통 baseline, repository-local taxonomy와 naming convention |
| `principles/` | 자산을 추가·분리·중복 제거·단순화할 때 쓰는 설계 원칙 |
| `authoring/` | 사람과 LLM이 지침·문서를 읽고 행동하기 쉽게 만드는 작성 원칙 |
| `concepts/` | 설계 판단의 배경이 되는 문제와 개념 |
| `tooling/` | 여러 자산 유형에서 공통으로 사용하는 도구 레퍼런스 |

유형별 레퍼런스는 sibling directory를 사용한다.

- Rule → `../rules/`
- Skill → `../skills/`
- Prompt → `../prompts/`가 실제로 필요할 때 생성
- Agent → `../agents/`가 실제로 필요할 때 생성

## Start Here

- 자산 유형이나 placement를 판단한다 → [Personal Agent Asset Standard](standards/agent-assets-standard-personal.md)
- 자산 이름과 접두사를 정한다 → [Agent Asset Naming Convention](standards/agent-assets-naming-convention.md)
- 외부 기준과 로컬 확장을 구분한다 → [Agent Asset Standard Baseline](standards/agent-assets-standard-baseline.md)
- 자산을 추가·분리·정리한다 → [Design Principles](principles/README.md)
- LLM용 지침을 작성한다 → [LLM-Readable Instructions](authoring/agent-assets-authoring-llm-readable-instructions.md)
- 사람용 문서를 작성한다 → [Human-Readable Documents](authoring/agent-assets-authoring-human-readable-documents.md)

## Boundary

새 문서를 `common/`에 두기 전에 묻는다.

> 둘 이상의 Agent Asset 유형에서 같은 의미로 재사용되는가?

아니라면 유형별 reference가 더 적절하다. 미래에 공통화될 것이라는 예상만으로 공통 abstraction을 만들지 않는다.

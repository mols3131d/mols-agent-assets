---
title: 공통 레퍼런스
description: Rulesync-managed 자산 전반에 공통으로 적용되는 repository convention, principle, authoring, concept와 tooling reference
---

# 공통 레퍼런스

`common/`은 여러 Rulesync feature나 repository workflow에서 같은 의미로 재사용되는 지식만 소유합니다.

Rulesync schema, feature taxonomy와 target mapping은 upstream Rulesync가 소유합니다. 이 디렉터리는 이를 repository-local schema나 별도 표준으로 재정의하지 않습니다.

## 구성

| 디렉터리 | 책임 |
| --- | --- |
| `conventions/` | repository integration, naming, chatbot compatibility 같은 local convention |
| `principles/` | 자산을 추가·분리·중복 제거·단순화할 때 쓰는 설계 원칙 |
| `authoring/` | 사람과 LLM이 지침·문서를 읽고 행동하기 쉽게 만드는 작성 원칙 |
| `concepts/` | 설계 판단의 배경이 되는 문제와 개념 |
| `tooling/` | 여러 feature에서 공통으로 사용하는 도구 reference |

Feature-specific reference는 실제 독립 책임이 있을 때만 형제 directory를 사용합니다. 현재 Skill reference는 `../skills/`가 소유합니다.

## 먼저 볼 문서

- Rulesync source와 repository boundary를 판단한다 → [Rulesync Repository Conventions](conventions/rulesync-repository-conventions.md)
- 자산 이름과 접두사를 정한다 → [Agent Asset Naming Convention](conventions/agent-assets-naming-convention.md)
- chatbot compatibility bootstrap을 설계한다 → [CHATBOT Runtime Compatibility Layer](conventions/chatbot-repository-bootstrap.md)
- 자산을 추가·분리·정리한다 → [Design Principles](principles/README.md)
- LLM용 지침을 작성한다 → [LLM-Readable Instructions](authoring/agent-assets-authoring-llm-readable-instructions.md)
- 사람용 문서를 작성한다 → [Human-Readable Documents](authoring/agent-assets-authoring-human-readable-documents.md)

## 범위

새 문서를 `common/`에 두기 전에 묻습니다.

> 둘 이상의 Rulesync feature 또는 repository workflow에서 같은 의미로 재사용되는가?

아니라면 더 좁은 owner가 적절합니다. 미래에 공통화될 것이라는 예상만으로 공통 abstraction을 만들지 않습니다.

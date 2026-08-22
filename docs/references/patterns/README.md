---
description: Agentic development에서 context engineering, documentation, workflow, software engineering 중 참고할 reusable pattern 영역을 선택할 때 사용하는 entrypoint입니다.
---

# Patterns

`docs/references/patterns/`는 **agentic development에서 반복되는 설계·운용·구현 문제를 해결할 때 참고하는 reusable pattern library**입니다.

Pattern은 특정 project의 mandatory policy가 아니라 여러 repository와 harness에서 참고·선택·조합·변형할 수 있는 설계 capsule입니다. Project-local mandatory rule과 workflow는 해당 project의 operational documentation이 소유합니다.

## Categories

하위 directory는 기술이나 파일 형식이 아니라 **pattern이 주로 해결하는 문제 영역**으로 나눕니다.

| Path | Responsibility |
| --- | --- |
| [`context-engineering/`](context-engineering/) | Agent Asset, instruction, routing, discovery, scoped context와 context harness 설계 |
| [`documentation/`](documentation/) | 개발·기술 문서, baseline, directory guide와 durable documentation 구조 |
| [`workflow/`](workflow/) | agentic work의 실행 흐름, working artifact와 handoff/lifecycle surface |
| [`software-engineering/`](software-engineering/) | repository/code 구조, architecture, implementation, testing, reliability 등 software engineering |

한 pattern이 여러 영역에 걸쳐도 **primary problem을 기준으로 한 곳만 소유**하고 다른 영역에서는 링크합니다. 새 category는 실제 pattern이 존재하고 기존 category와 구분되는 반복 책임이 생겼을 때만 추가합니다.

## Capsule

하나의 pattern은 하나의 **self-contained capsule**입니다.

- 다른 capsule 없이도 목적, core, 주요 선택지와 경계를 이해할 수 있어야 합니다.
- 관련 pattern이나 외부 source를 reference할 수 있지만 그 의존성이 핵심 의미를 대신하지는 않습니다.
- 단순 pattern은 category 아래의 `*.md` 하나로 시작합니다.
- 독립적인 책임이나 유지보수 필요가 생기면 directory bundle로 확장할 수 있습니다.

```text
patterns/
└─ <category>/
   ├─ README.md
   ├─ simple-pattern.md
   └─ large-pattern/
      ├─ README.md
      └─ ...
```

Bundle은 여러 파일로 나뉘어도 하나의 pattern capsule입니다. Entrypoint에서 bundle의 의미와 내부 탐색 경로를 파악할 수 있게 합니다.

## Writing

Pattern은 **본질은 분명하게, 적용은 유연하게** 작성합니다.

- Pattern을 성립시키는 core와 invariant는 명확하게 둡니다.
- 본질이 아닌 layout, filename, format, tool, workflow는 고정 규칙으로 만들지 않습니다.
- 대표 구현은 recommendation, typical form, example, option처럼 성격을 구분해 제시합니다.
- 의미 있는 대안과 규모·환경에 따른 extension을 열어둡니다.
- 작은 repository에서는 단순화하고 필요한 경우 더 복잡한 구성으로 확장할 수 있어야 합니다.

문서 구조는 고정 schema가 아닙니다. 필요하면 `Purpose`, `Core`, `Typical Forms`, `Options`, `Extensions`, `Considerations`, `Boundary` 같은 책임을 사용하고 필요 없는 section은 형식 때문에 추가하지 않습니다.

## Ownership

각 capsule은 자기 pattern을 충분히 설명하되 경계를 넘지 않습니다.

- Category `README.md`는 해당 directory의 책임과 routing을 소유하며 개별 pattern의 본문을 복제하지 않습니다.
- 다른 capsule과 내용이 겹치는 것은 self-containment와 재사용성에 도움이 되면 허용합니다.
- 다른 pattern의 핵심 책임을 자기 규칙처럼 소유하지 않습니다.
- Agent Asset type-specific 설계 지식은 [`docs/references/agent-assets/`](../agent-assets/)가 소유합니다.
- 외부 standard나 tool behavior가 authority라면 필요에 따라 reference하고 pattern이 이를 재정의하지 않습니다.
- 같은 capsule이나 bundle 내부의 의미 없는 반복은 피합니다.

## Review

Pattern을 작성하거나 수정할 때 다음을 확인합니다.

1. 이 capsule만으로 pattern의 목적과 본질을 이해할 수 있는가?
1. Primary problem과 category가 자연스럽게 일치하는가?
1. Core와 recommendation / option / example이 구분되어 있는가?
1. 특정 repository나 tool에 불필요하게 고정되어 있지 않은가?
1. 다른 pattern이나 project policy가 소유해야 할 책임을 가져오지 않았는가?
1. 필요한 대안과 확장 가능성을 닫아버리지 않았는가?
1. Bundle이라면 entrypoint에서 전체 의미와 내부 구조를 탐색할 수 있는가?

Root와 category README는 전체 pattern inventory를 복제하지 않습니다. Filesystem과 각 entrypoint가 탐색 surface가 되고, README는 분류와 공통 contract만 소유합니다.

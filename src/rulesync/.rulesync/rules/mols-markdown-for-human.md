---
root: false
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
description: 사람이 읽고 유지보수하는 Markdown을 빠르게 이해하고 다시 찾기 쉽게 작성하거나 수정할 때 적용합니다.
globs:
  - "**/*.md"
---

# Markdown for Human Baseline

Markdown을 사람이 빠르게 읽고 필요한 정보를 쉽게 다시 찾을 수 있게 작성합니다.

- 결론, 상태, 결정 또는 다음 행동을 먼저 보여줍니다.
- 저자의 작성 순서보다 독자의 질문과 판단 흐름에 맞춰 section을 구성합니다.
- heading만 훑어도 흐름을 알 수 있게 구체적으로 쓰고 depth는 필요 이상 깊게 만들지 않습니다.
- 한 문단에는 하나의 핵심을 두고 중요한 내용을 앞에 배치합니다.
- list 항목은 같은 추상화 수준과 문법 형태를 유지하고, 길어지면 의미 있는 기준으로 나눕니다.
- prose, list, table, callout은 정보 구조에 맞게 선택합니다. 짧은 prose나 list가 더 빠르면 형식을 추가하지 않습니다.
- table은 비교 가능한 반복 구조에 사용하고 긴 서술이나 절차를 억지로 넣지 않습니다.
- code, command, path와 field name은 inline code로 표시합니다.
- KISS는 의미나 필요한 구조를 줄이는 것이 아니라 이해와 유지보수에 기여하지 않는 복잡성을 제거하는 데 적용합니다.
- 같은 사실이나 규칙을 heading, prose, table과 callout에 반복하지 않습니다. 가장 적절한 한 곳에 두고 다른 곳에서는 참조합니다.
- 기존 문서를 수정할 때 사실, 결정, 순서, 관계, identifier, URL, citation, code와 필요한 nuance를 보존합니다. 근거 없는 사실이나 관계를 추가하지 않습니다.
- agent-facing Markdown에서는 읽기 쉬운 presentation만 다룹니다. 행동 계약, activation과 authority는 해당 자산의 owner를 따릅니다.
- 변경 후 source와 rendered view에서 의미와 탐색성이 유지되는지 확인합니다.

더 세밀한 작성 workflow, visual routing과 Markdown 표현 선택이 필요하고 `mols-markdown-for-human` Skill을 사용할 수 있다면 해당 Skill을 적용합니다. 이 Rule은 모든 Markdown 작업에 필요한 baseline만 소유합니다.

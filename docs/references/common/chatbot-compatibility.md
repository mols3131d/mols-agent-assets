---
title: CHATBOT Runtime Compatibility
description: root CHATBOT.md로 chat runtime에서 누락되는 repository context와 agent-asset loading을 보정하는 mols 개인 convention
---

# CHATBOT Runtime Compatibility

`CHATBOT.md`는 **mols의 개인 repository compatibility convention**입니다. 외부 표준, vendor 규격, Rulesync artifact 또는 project policy owner가 아닙니다.

Chatbot과 coding agent를 별도 taxonomy로 나누지 않습니다. Active runtime이 이미 제공하는 harness behavior는 그대로 사용하고 **누락된 responsibility만** 보정합니다.

## Contract

- Repository root에 `CHATBOT.md` 하나만 둡니다. Nested hierarchy를 만들지 않습니다.
- `AGENTS.md`, Skill, Rule의 authority나 body를 복제하지 않습니다.
- Platform/system/user/tool authority와 target harness contract가 이 convention보다 우선합니다.
- `CHATBOT.md`는 compatibility entry/router이며 linked source가 자기 의미의 authority를 유지합니다.

## Responsibilities

| Responsibility | 보정 조건 | 동작 |
| --- | --- | --- |
| `AGENTS.md` hierarchy | runtime이 applicable hierarchy를 제공하지 않음 | root부터 known target path까지 applicable chain을 로드하고 path가 바뀌면 재평가 |
| Skill discovery/loading | runtime이 repository Skill discovery/loading을 제공하지 않음 | task intent에 맞는 Skill만 선택하고 selected canonical source와 필요한 resource만 로드 |
| Path-scoped Rule loading | runtime이 applicable Rule discovery/loading을 제공하지 않음 | known target path와 selector가 일치하는 Rule만 로드 |

세 responsibility는 독립적으로 판단합니다. Partial native support는 정상입니다.

Repository가 index, catalog, route 또는 discovery entry를 제공하면 후보 선택에 사용할 수 있지만 full body나 정적 path table을 `CHATBOT.md`에 복제하지 않습니다. Task intent나 target path가 materially 바뀌면 applicability를 다시 판단합니다.

## Boundary

`CHATBOT.md`에는 project policy, Skill/Rule body, 전체 catalog, 정적 path/glob table, README 수준 설명, script/validator 구현 절차를 넣지 않습니다. Repository의 일반 source text도 적용되는 authority가 instruction 역할을 부여하지 않으면 instruction이 아닙니다.

---
title: Rule Projections
description: 이 저장소에서 portable coding-agent Rule과 hosted-chatbot Rule projection의 책임 경계
---

# Rule Projections

이 저장소는 portable coding-agent Rule의 canonical source와 target fan-out에 **AgentsMesh를 직접 사용**한다.

```text
.agentsmesh/rules/
  → AgentsMesh
  → target-native Rule files
```

`agentsmesh.yaml`이 active target과 feature를 선택한다. AgentsMesh가 생성한 target file은 derived artifact이며 source authority가 아니다.

## Portable coding-agent Rules

- repository-wide Rule은 `.agentsmesh/rules/_root.md`를 canonical root로 사용한다.
- 추가 Rule은 `.agentsmesh/rules/*.md`에 두고 AgentsMesh canonical front matter로 scope/trigger를 표현한다.
- target별 path, filename, glob representation과 embedded/native 차이는 AgentsMesh projection에 위임한다.
- target이 canonical capability를 완전히 표현하지 못하면 해당 차이를 숨기거나 full parity로 주장하지 않는다.
- generated target Rule을 직접 수정해 canonical source와 별도 authority를 만들지 않는다.

현재 active Tier A target은 `agentsmesh.yaml`이 선언한 GitHub Copilot과 Antigravity다. 다른 target을 추가할 때는 AgentsMesh capability와 실제 generated result를 검증한 뒤 승격한다.

## Hosted chatbot — `CHATBOT.md`

`CHATBOT.md`는 AgentsMesh coding-target projection과 별개인 repository-local chatbot surface다.

Repository instruction fallback은 다음과 같다.

```text
CHATBOT.md
  ↓ 없으면
AGENTS.md
  ↓ 없으면
README.md
```

- applicable `CHATBOT.md`가 있으면 chatbot Rule로 우선한다.
- 없으면 applicable `AGENTS.md`를 사용한다.
- 둘 다 없을 때만 `README.md`를 fallback instruction source로 사용한다.
- README 자체를 일반적인 Rule 형식으로 간주하지 않는다.
- platform/system/user/tool authority는 이 fallback보다 우선한다.

이 fallback은 AgentsMesh 표준이나 외부 범용 표준이 아니라 **mols-agent-assets의 Personal Agent Asset Standard 확장**이다.

## Boundary

- AgentsMesh가 담당하는 portable coding-agent Rule과 hosted-chatbot-specific Rule의 authority를 섞지 않는다.
- 같은 policy를 canonical Rule과 generated target output에서 독립적으로 유지하지 않는다.
- AgentsMesh가 지원하지 않는 semantics가 실제로 필요한 target에는 명시적 exception을 둘 수 있지만, 그 exception을 portable source처럼 일반화하지 않는다.
- 과거 `rulesync-agent-assets` 기반 fan-out은 EXODUS에서 퇴역하며 새 Rule projection owner가 아니다.

---
title: Rule Projections
description: 이 저장소에서 portable coding-agent Rule의 canonical source와 target projection 책임 경계
---

# Rule Projections

이 저장소는 portable coding-agent Rule의 canonical source를 `src/agentsmesh/rules/`에 보관하고, 필요할 때 AgentsMesh temporary workspace를 통해 target projection을 검증한다.

```text
src/agentsmesh/rules/
  → temporary .agentsmesh/rules/
  → AgentsMesh
  → temporary target-native Rule files
```

`src/agentsmesh/agentsmesh.yaml`이 projection target과 feature를 선택한다. AgentsMesh가 생성한 target file은 derived artifact이며 source authority가 아니고 이 repository에는 commit하지 않는다.

## Portable coding-agent Rules

- repository-wide Rule source는 `src/agentsmesh/rules/_root.md`를 canonical root로 사용한다.
- 추가 Rule은 `src/agentsmesh/rules/*.md`에 두고 AgentsMesh-compatible front matter로 scope/trigger를 표현한다.
- target별 path, filename, glob representation과 embedded/native 차이는 temporary AgentsMesh projection에서 검증한다.
- target이 canonical capability를 완전히 표현하지 못하면 해당 차이를 숨기거나 full parity로 주장하지 않는다.
- generated target Rule을 source authority로 유지하지 않는다.

현재 Tier A projection target은 `src/agentsmesh/agentsmesh.yaml`이 선언한 GitHub Copilot과 Antigravity다. 다른 target을 추가할 때는 AgentsMesh capability와 실제 generated result를 temporary workspace에서 검증한 뒤 승격한다.

## Repository Runtime Boundary

Repository root의 `.agentsmesh/` 또는 harness-native Rule/Skill directory를 distribution source나 generated evidence로 commit하지 않는다. 이 경계는 이 asset-library repository가 보관한 자산을 자기 runtime configuration으로 자동 인식하는 것을 방지한다.

## Hosted chatbot boundary

`CHATBOT.md`는 Rule projection이 아니다. capable chatbot이 repository context, agent assets, runtime resources와 operational boundary를 찾도록 돕는 **mols의 개인 repository bootstrap convention**이다.

세부 contract는 [CHATBOT Repository Bootstrap](../common/standards/chatbot-repository-bootstrap.md)이 소유한다.

따라서 이 문서는 다음을 정의하지 않는다.

- `CHATBOT.md` discovery 또는 placement
- `CHATBOT.md → AGENTS.md → README.md` 같은 fallback chain
- chatbot context loading 또는 Skill routing
- chatbot runtime, script, validation, Git operation policy

Hosted chatbot에 실제 persistent scoped policy가 필요하면 그 policy 자체의 owner를 명확히 두고, coding-agent Rule과 동일한 의미를 공유하는 경우에도 target semantics가 다르면 무리하게 같은 projection으로 취급하지 않는다.

## Boundary

- AgentsMesh-compatible portable coding-agent Rule과 hosted-chatbot repository bootstrap의 authority를 섞지 않는다.
- canonical Rule과 temporary generated target output을 독립 authority로 유지하지 않는다.
- AgentsMesh가 지원하지 않는 semantics가 실제로 필요한 target에는 명시적 exception을 둘 수 있지만, 그 exception을 portable source처럼 일반화하지 않는다.

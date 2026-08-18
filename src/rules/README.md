# Hosted-chatbot Rules

`src/rules/`는 **AgentsMesh coding-target scope 밖의 repository-local Rule만** 보관한다.

portable coding-agent Rule의 canonical source는 `.agentsmesh/rules/`이며 target projection은 AgentsMesh가 소유한다.

현재 이 디렉터리의 실질 Rule source는 `chatbot-repo-skill-routing.md`다. 이 Rule은 hosted chatbot이 repository Skill index를 찾기 위한 repository-local routing contract이므로 coding-agent Rule로 승격하지 않는다.

## Chatbot scope

`CHATBOT.md`를 사용하는 repository instruction fallback은 다음과 같다.

```text
CHATBOT.md
  ↓ 없으면
AGENTS.md
  ↓ 없으면
README.md
```

이 fallback은 repository-local convention이며 AgentsMesh나 외부 Agent 표준의 일부가 아니다.

## Boundary

- portable coding-agent Rule은 `.agentsmesh/rules/`에 둔다.
- hosted-chatbot-specific Rule만 이 디렉터리에 둔다.
- 같은 policy를 두 source에서 독립적으로 유지하지 않는다.
- 상황별로 선택 로드해야 하는 context는 Rule보다 Skill을 우선 검토한다.
- 한 task의 긴 workflow는 Rule에 넣지 않는다.

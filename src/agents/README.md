# Target-specific Agents

`src/agents/`는 현재 EXODUS에서 **의도적으로 AgentsMesh 밖에 남긴 target-specific Agent source**다.

## Why this is an exception

현재 active AgentsMesh target set은 GitHub Copilot과 Antigravity다. 이 조합에서 portable Rules와 Skills는 공통 projection이 가능하지만 Agent capability는 동일하지 않다.

기존 review Agent들은 또한 VS Code-specific front matter와 tool identifiers를 사용하고, `review-lead`는 `agents: [review-quality, review-adversarial]` delegation을 행동 계약으로 가진다. 이 의미를 삭제하거나 가짜 portability로 바꾸지 않는다.

## Policy

- 이 디렉터리를 portable Agent canonical source라고 부르지 않는다.
- AgentsMesh `agents` feature를 활성화하려면 active target capability와 delegation semantics를 먼저 다시 검증한다.
- AgentsMesh가 필요한 의미를 자연스럽게 표현할 수 있게 되거나 active target set이 바뀌면 별도 migration으로 승격할 수 있다.
- 그 전까지는 target-specific behavior preservation이 directory 통일보다 우선한다.

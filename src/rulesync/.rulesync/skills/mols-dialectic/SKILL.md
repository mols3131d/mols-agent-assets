---
name: mols-dialectic
description: >-
  Use dialectical deliberation when the user explicitly asks for debate, dialectic,
  정반합, thesis-antithesis-synthesis, sublation, or a structured opposing-position
  process that should end in a stronger transformed conclusion rather than a vote or
  compromise. The caller orchestrates the explicitly related mols-dialectic-thesis,
  mols-dialectic-antithesis, and mols-dialectic-synthesis subagents. Do not use for
  ordinary comparison, brainstorming, simple factual lookup, or bounded technical
  correctness review where a review-specific capability is more direct.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Mols Dialectic

서로 대립하는 강한 입장을 실제로 충돌시킨 뒤, 살아남는 내용을 보존하고 실패한 내용을 버리며 더 나은 결론으로 **승화(sublation)** 하는 토론 capability다.

이 Skill의 실행 주체는 현재 caller다. 별도 moderator Subagent를 만들지 않는다.

## Contract

- `mols-dialectic-thesis`, `mols-dialectic-antithesis`, `mols-dialectic-synthesis`를 이 Skill의 명시적 specialist dependency로 사용한다. 다른 Agent Asset을 암묵적으로 전제하지 않는다.
- caller는 framing, specialist 호출, context handoff, 토론 순서, 종료와 user-facing response를 소유한다. substantive position을 하나 더 만들어 네 번째 토론자가 되지 않는다.
- Thesis와 Antithesis는 역할 충성을 위해 입장을 지키지 않는다. 상대 주장이 더 강하면 concede, narrow, revise할 수 있다.
- 반박 전에 상대의 strongest reasonable version을 steelman한다. 약한 표현이나 caricature를 공격하지 않는다.
- agreement, majority, confidence, rhetoric은 근거가 아니다. 실제 evidence, reasoning, authority, constraint와 trade-off를 기준으로 판단한다.
- Synthesis는 평균, 절충, 양쪽 주장 병합이 아니다. 유효한 것을 보존하고 실패한 것을 부정하며 framing이나 solution을 더 강한 형태로 변환한다.
- 한쪽이 대부분 옳다면 비대칭적으로 보존할 수 있고, 둘 다 실패하면 제3의 framing을 만들 수 있다.
- 정당한 합을 만들 수 없으면 `unresolved`를 정상 결과로 남긴다. 균형이나 합의를 만들기 위해 conflict를 조작하지 않는다.
- 사실, 추론, 가정과 중요한 unknown을 가능한 범위에서 구분한다. 외부 evidence와 governing authority의 의미는 task-specific capability와 caller가 소유한다.

## Execute

토론을 실행할 때 [`references/orchestration.md`](references/orchestration.md)를 읽고 따른다.

## Boundary

- 이 Skill은 outer task Goal, Scope, domain policy, safety, mutation authority 또는 artifact policy를 대체하지 않는다.
- 토론을 위해 별도 bundle, turn file, scheduler, persistence protocol을 만들지 않는다. 외부 workflow가 요구할 때만 그 owner의 artifact contract를 따른다.
- 단순한 관점 나열, 찬반 투표, 일반 brainstorming 또는 review checklist로 변형하지 않는다.
- runtime이 제공하지 않는 independence, concurrency 또는 subagent execution을 수행했다고 주장하지 않는다.

# 자산 개발 가이드

## Directory Roles

- `.agentsmesh/rules/`: portable coding-agent Rule canonical source.
- `.agentsmesh/skills/`: portable coding-agent Skill canonical source.
- `src/agents/`: 현재 AgentsMesh Tier A contract 밖의 target-specific Agent.
- `src/skills-chatbot/`: flat hosted-chatbot Skill.
- `src/skills-chatbot-runtime/`: bundled/runtime hosted-chatbot Skill.
- `src/prompts/`: explicit Prompt source.
- `src/rules/`: AgentsMesh 밖의 hosted-chatbot-specific Rule만 유지.
- `tests/`: 자산 및 도구 검증.

AgentsMesh가 생성한 `.github/skills/`, `.github/copilot-instructions.md`, `.agents/rules/`, `.agents/skills/`는 derived target artifacts다. 직접 수정하지 않는다.

## Workflow

1. `<owner>/<type>/<topic>` 브랜치를 생성한다.
1. portable coding-agent Rule/Skill은 `.agentsmesh/`에서 작성하거나 수정한다. AgentsMesh scope 밖의 profile만 해당 `src/` owner에서 수정한다.
1. `npm ci`로 pinned AgentsMesh toolchain을 준비한다.
1. AgentsMesh-managed 변경은 `npm run agentsmesh:lint` 후 `npx agentsmesh generate`로 active target projection을 갱신한다.
1. `npm run agentsmesh:check`와 `npm run agentsmesh:generate:check`로 drift와 regeneration을 검증한다.
1. 필요한 repository test/eval을 실행한다.
1. canonical source와 generated artifacts를 같은 PR에서 검토한 뒤 배포 브랜치에 병합한다.

AgentsMesh가 표현하지 못하는 target semantics를 portability 명목으로 삭제하거나 축소하지 않는다. 명시적인 target-specific exception으로 남기고 그 이유를 문서화한다.

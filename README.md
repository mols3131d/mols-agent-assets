# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

AgentsMesh가 표현할 수 있는 Agent Asset의 canonical source는 `src/agentsmesh/`에 둡니다. 이 경로는 의도적으로 `.agentsmesh/`가 아닙니다. 저장된 Skills와 Rules가 이 자산 저장소 자체의 runtime configuration으로 자동 인식되는 것을 막기 위한 경계입니다.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | 지속 적용되는 policy와 constraint |
| Skill | 재사용 capability와 조건부 context |
| Prompt | 현재 invocation의 goal과 일회성 context |
| Agent | 독립 role, authority, tools, delegation |

외부 기준에 가까운 개념은 `docs/references/common/standards/agent-assets-standard-baseline.md`, 이 저장소의 비표준 확장과 실제 운용 기준은 `docs/references/common/standards/agent-assets-standard-personal.md`의 **Personal Agent Asset Standard**가 소유합니다.

## Source Boundary

| Directory | Role |
| --- | --- |
| `src/agentsmesh/` | AgentsMesh-compatible Rule, Skill, Agent의 canonical source |
| `src/`의 다른 경로 | 실제 요구가 있는 custom/non-standard Agent Asset source |
| `.agents/AGENTS.md` | 이 저장소 자체를 위한 repository-local guard |
| `tests/` | deterministic test |
| `evals/` | behavioral/model eval과 cross-asset regression contract |
| `docs/` | 사람용 문서와 reference |
| `scripts/` | 자동화·검증·동기화 도구 |

Repository root의 `.agentsmesh/`, `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/rules/`, `.agents/skills/`는 distribution source로 사용하지 않습니다. AgentsMesh-native validation이나 projection이 필요하면 `src/agentsmesh/`를 임시 workspace의 `.agentsmesh/`로 stage하고 결과는 저장소 밖에서 검증합니다.

Skill 규격은 `agentskills.io` open standard를 Tier 1으로 사용합니다. 주요 vendor/harness의 Tier 2 규격은 `docs/references/skills/agent-skills-io/agent-skills-io-specification.md`에서 공식 원문만 연결하며 복제하지 않습니다. 이 저장소의 Skill 확장은 `docs/references/skills/agent-assets-skills-standard-personal.md`, package shape와 target boundary는 `docs/references/skills/agent-assets-skills-target-profiles.md`가 소유합니다.

## Basic Workflow

```text
edit src/agentsmesh
  → rumdl fmt when Markdown is affected
  → stage to a temporary AgentsMesh workspace when native validation is needed
  → repository tests / applicable evals
  → review canonical source only
```

핵심 원칙은 단순합니다. **보관하는 Agent Asset과 이 저장소에서 실제 활성화되는 Agent Asset을 같은 filesystem surface에 두지 않습니다.**

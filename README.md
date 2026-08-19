# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

AgentsMesh가 표현할 수 있는 Agent Asset은 `src/agentsmesh/`라는 **격리된 native workspace**에서 관리합니다. 설정은 `src/agentsmesh/agentsmesh.yaml`, canonical Rule/Skill/Agent는 `src/agentsmesh/.agentsmesh/`에 둡니다. repository root에는 AgentsMesh runtime workspace를 만들지 않습니다.

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
| `src/agentsmesh/` | 격리된 native AgentsMesh workspace와 projection config |
| `src/agentsmesh/.agentsmesh/` | AgentsMesh-compatible Rule, Skill, Agent의 canonical source |
| `src/`의 다른 경로 | 실제 요구가 있는 custom/non-standard Agent Asset source |
| `.agents/AGENTS.md` | 이 저장소 자체를 위한 repository-local guard |
| `tests/` | deterministic test |
| `evals/` | behavioral/model eval과 cross-asset regression contract |
| `docs/` | 사람용 문서와 reference |
| `scripts/` | 자동화·검증·동기화 도구 |

Repository root의 `.agentsmesh/`, `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/rules/`, `.agents/skills/`는 distribution source로 사용하지 않습니다. Native read-only 검증은 `src/agentsmesh/`에서 직접 실행하고, generation처럼 파일을 쓰는 검증만 workspace 전체를 temporary directory로 복사해 수행합니다.

Skill 규격은 `agentskills.io` open standard를 Tier 1으로 사용합니다. 주요 vendor/harness의 Tier 2 규격은 `docs/references/skills/agent-skills-io/agent-skills-io-specification.md`에서 공식 원문만 연결하며 복제하지 않습니다. 이 저장소의 Skill 확장은 `docs/references/skills/agent-assets-skills-standard-personal.md`, package shape와 target boundary는 `docs/references/skills/agent-assets-skills-target-profiles.md`가 소유합니다.

## Basic Workflow

```text
edit src/agentsmesh/.agentsmesh
  → rumdl fmt when Markdown is affected
  → native lint / preview from src/agentsmesh
  → temporary workspace copy only for write-producing validation
  → repository tests / applicable evals
  → review canonical source only
```

핵심 원칙은 단순합니다. **native layout은 보존하되, repository root runtime surface와 distribution source는 분리합니다.**

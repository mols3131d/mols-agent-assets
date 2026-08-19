# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

AgentsMesh가 충실히 표현할 수 있는 Agent Asset은 `.agentsmesh/`를 canonical source로 사용합니다. 저장소는 자산의 의미, 품질 계약, 테스트와 eval을 소유하고 AgentsMesh는 canonical representation과 활성 target projection을 담당합니다.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | 지속 적용되는 policy와 constraint |
| Skill | 재사용 capability와 조건부 context |
| Prompt | 현재 invocation의 goal과 일회성 context |
| Agent | 독립 role, authority, tools, delegation |

외부 기준에 가까운 개념은 `docs/references/common/standards/agent-assets-standard-baseline.md`, 이 저장소의 비표준 확장과 실제 운용 기준은 `docs/references/common/standards/agent-assets-standard-personal.md`의 **Personal Agent Asset Standard**가 소유합니다.

## Source and Generated Surfaces

| Directory | Role |
| --- | --- |
| `.agentsmesh/` | 현재 AgentsMesh contract로 표현할 수 있는 Rule, Skill, Agent의 canonical source |
| `src/` | AgentsMesh contract 밖에 의도적으로 두는 repository-local custom/non-standard exception surface |
| `.github/`, `.agents/`의 AgentsMesh 관리 경로 | 활성 target을 위한 generated projection |

현재 `src/` 아래에 반드시 유지해야 하는 custom Agent Asset은 없습니다. AgentsMesh가 표현할 수 있는 자산을 `src/`에 parallel source로 만들지 않습니다.

`agentsmesh.yaml`이 활성 coding-agent target과 feature를 선택합니다. 현재 Copilot/Antigravity projection은 `.agentsmesh/`에서 파생된 산출물이며 직접 편집하지 않습니다.

Skill 규격은 `agentskills.io` open standard를 Tier 1으로 사용합니다. 주요 vendor/harness의 Tier 2 규격은 `docs/references/skills/agent-skills-io/agent-skills-io-specification.md`에서 공식 원문만 연결하며 복제하지 않습니다. 이 저장소의 Skill 확장은 `docs/references/skills/agent-assets-skills-standard-personal.md`, package shape와 target boundary는 `docs/references/skills/agent-assets-skills-target-profiles.md`가 소유합니다.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agentsmesh/` | canonical Agent Assets와 AgentsMesh lock |
| `.github/copilot-instructions.md`, `.github/skills/`, `.github/agents/` | generated GitHub Copilot projection |
| `.agents/rules/`, `.agents/skills/` | generated Antigravity projection |
| `src/` | intentional custom/non-standard Agent Asset exception surface |
| `tests/` | 저장소 수준 deterministic test |
| `evals/` | behavioral/model eval과 cross-asset regression contract |
| `docs/` | 저장소 수준 사람용 문서와 reference |
| `scripts/` | 저장소 자동화·동기화·개발 도구 |

## Basic Workflow

```text
edit canonical source
  → rumdl fmt when Markdown is affected
  → agentsmesh lint / generate when applicable
  → agentsmesh check / generate --check when applicable
  → repository tests / applicable evals
```

AgentsMesh가 표현하지 못하는 자산은 실제 요구가 있을 때만 `src/`의 명시적 exception으로 둡니다. 예외를 미래 taxonomy나 빈 구조로 미리 만들지 않습니다.

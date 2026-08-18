# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

Agent Asset의 canonical source는 가능한 경우 **AgentsMesh를 직접 사용**합니다. 저장소는 Agent Asset의 의미, 품질 계약, 테스트와 eval을 소유하고 AgentsMesh는 canonical representation과 target projection을 담당합니다.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | 지속 적용되는 policy와 constraint |
| Skill | 재사용 capability와 조건부 context |
| Prompt | 현재 invocation의 goal과 일회성 context |
| Agent | 독립 role, authority, tools, delegation |

외부 기준에 가까운 개념은 `docs/references/common/standards/agent-assets-standard-baseline.md`, 이 저장소의 비표준 확장과 실제 운용 기준은 `docs/references/common/standards/agent-assets-standard-personal.md`의 **Personal Agent Asset Standard**가 소유합니다.

## Current Source / Exception Surfaces

| Directory | Role |
| --- | --- |
| `.agentsmesh/` | 현재 AgentsMesh contract로 의미를 보존할 수 있는 Agent Asset의 canonical source |
| `src/` | 아직 `.agentsmesh/`로 이관되지 않았거나 현재 contract로 충실히 표현하기 어려운 자산의 과도기적 예외 surface |

`src/`의 현재 하위 profile은 호환성 경계이지 장기 taxonomy가 아닙니다. 새 장기 authority를 추가하기보다 의미 손실 없이 표현 가능한 자산은 `.agentsmesh/`를 우선합니다.

`agentsmesh.yaml`이 활성 coding-agent target과 feature를 선택합니다. 현재 generated Copilot/Antigravity 파일은 `.agentsmesh/`에서 파생된 배포 산출물이며 직접 편집하지 않습니다.

Skill 규격은 `agentskills.io`의 open standard를 Tier 1으로 사용합니다. 주요 vendor/harness의 Tier 2 규격은 `docs/references/skills/agent-skills-io/agent-skills-io-specification.md`에서 공식 원문만 연결하며 복제하지 않습니다. 이 저장소의 Skill 확장은 `docs/references/skills/agent-assets-skills-standard-personal.md`, target profile 상세는 `docs/references/skills/agent-assets-skills-target-profiles.md`가 소유합니다.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agentsmesh/` | canonical Agent Assets와 AgentsMesh lock |
| `.github/skills/`, `.github/copilot-instructions.md` | generated GitHub Copilot projection |
| `.agents/rules/`, `.agents/skills/` | generated Antigravity projection |
| `src/` | 현재 AgentsMesh contract 밖의 과도기적 Agent Asset 예외 surface |
| `tests/` | 저장소 수준 자동화 테스트 |
| `evals/` | cross-asset evaluation contracts when present |
| `docs/` | 저장소 수준 사람용 문서와 reference |
| `scripts/` | 저장소 자동화·동기화·개발 도구 |

## Basic Workflow

```text
edit canonical asset source
  → agentsmesh lint / generate when applicable
  → agentsmesh check / generate --check when applicable
  → repository tests / applicable evals
```

AgentsMesh가 아직 충실히 표현하지 못하는 자산은 명시적 예외로 유지하되, 예외 자체를 영구 taxonomy로 굳히지 않습니다.

# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

portable coding-agent 자산은 **AgentsMesh를 직접 사용**해 여러 harness로 배포합니다. 저장소는 Agent Asset의 의미, 품질 계약, 테스트와 eval을 소유하고 AgentsMesh는 canonical configuration과 target projection을 담당합니다.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | 지속 적용되는 policy와 constraint |
| Skill | 재사용 capability와 조건부 context |
| Prompt | 현재 invocation의 goal과 일회성 context |
| Agent | 독립 role, authority, tools, delegation |

외부 기준에 가까운 개념은 `docs/references/common/standards/agent-assets-standard-baseline.md`, 이 저장소의 비표준 확장과 실제 운용 기준은 `docs/references/common/standards/agent-assets-standard-personal.md`의 **Personal Agent Asset Standard**가 소유합니다.

## Source / Target Profiles

| Directory | Authority |
| --- | --- |
| `.agentsmesh/rules/` | portable coding-agent Rule canonical source |
| `.agentsmesh/skills/` | portable coding-agent Skill canonical source |
| `src/agents/` | 현재 AgentsMesh Tier A contract로 안전하게 표현되지 않는 target-specific Agent source |
| `src/skills-chatbot/` | self-contained hosted-chatbot Skill profile |
| `src/skills-chatbot-runtime/` | bundled/runtime hosted-chatbot Skill profile |
| `src/prompts/` | explicit Prompt source |
| `src/rules/` | AgentsMesh 밖의 hosted-chatbot-specific Rule source만 유지 |

`agentsmesh.yaml`이 활성 coding-agent target과 feature를 선택합니다. 현재 generated Copilot/Antigravity 파일은 `.agentsmesh/`에서 파생된 배포 산출물이며 직접 편집하지 않습니다.

Skill 규격은 `agentskills.io`의 open standard를 Tier 1으로 사용합니다. 주요 vendor/harness의 Tier 2 규격은 `docs/references/skills/agent-skills-io/agent-skills-io-specification.md`에서 공식 원문만 연결하며 복제하지 않습니다. 이 저장소의 Skill 확장은 `docs/references/skills/agent-assets-skills-standard-personal.md`, target profile 상세는 `docs/references/skills/agent-assets-skills-target-profiles.md`가 소유합니다.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agentsmesh/` | portable coding-agent canonical assets와 AgentsMesh lock |
| `.github/skills/`, `.github/copilot-instructions.md` | generated GitHub Copilot projection |
| `.agents/rules/`, `.agents/skills/` | generated Antigravity projection |
| `src/` | AgentsMesh scope 밖의 target-specific/hosted Agent Asset profile |
| `tests/` | 저장소 수준 자동화 테스트 |
| `evals/` | cross-asset evaluation contracts when present |
| `docs/` | 저장소 수준 사람용 문서와 reference |
| `scripts/` | 저장소 자동화·동기화·개발 도구 |

## Basic Workflow

```text
edit .agentsmesh/
  → agentsmesh lint
  → agentsmesh generate
  → agentsmesh check / generate --check
  → repository tests / applicable evals
```

AgentsMesh가 지원하지 않는 profile은 억지로 canonical model에 구겨 넣지 않고 명시적인 별도 authority로 유지합니다.

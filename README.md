# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | 지속 적용되는 policy와 constraint |
| Skill | 재사용 capability와 조건부 context |
| Prompt | 현재 invocation의 goal과 일회성 context |
| Agent | 독립 role, authority, tools, delegation |

외부 기준에 가까운 개념은 `docs/references/common/standards/agent-assets-standard-baseline.md`, 이 저장소의 비표준 확장과 실제 운용 기준은 `docs/references/common/standards/agent-assets-standard-personal.md`의 **Personal Agent Asset Standard**가 소유합니다.

## Source / Target Profiles

| Directory | Purpose |
| --- | --- |
| `src/agents/` | subagent 및 custom agent source |
| `src/skills/` | workspace-capable Skill profile |
| `src/skills-chatbot/` | 4,000 tokens 미만의 self-contained single-file chatbot Skill profile |
| `src/skills-chatbot-runtime/` | bundled resources 또는 hosted runtime 기능을 사용하는 chatbot Skill profile |
| `src/rules/` | Rule source |

세 Skill profile의 세부 규격은 `docs/references/skills/agent-assets-skills-target-profiles.md`가 소유합니다. Rule projection과 chatbot fallback은 `docs/references/rules/agent-assets-rules-projections.md`를 따릅니다.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agents/` | 로컬 agent runtime 지침 |
| `src/` | 자산 source workspace |
| `tests/` | 저장소 수준 자동화 테스트 |
| `docs/` | 저장소 수준 사람용 문서와 reference |
| `scripts/` | 저장소 자동화 도구 |

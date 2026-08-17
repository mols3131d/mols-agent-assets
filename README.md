# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | 지속 적용되는 policy와 constraint |
| Skill | 재사용 capability와 조건부 context |
| Prompt | 현재 invocation의 goal과 일회성 context |
| Agent | 독립 role, authority, tools, delegation |

외부 기준에 가까운 개념은 `docs/references/common/agent-asset-standard-baseline.md`, 이 저장소의 비표준 확장과 실제 운용 규칙은 `docs/references/common/agent-asset-boundaries.md`의 **Personal Agent Asset Standard**가 소유합니다.

## Source / Target Profiles

| Directory | Purpose |
| --- | --- |
| `src/agents/` | subagent 및 custom agent source |
| `src/skills/` | workspace-capable Skill profile |
| `src/skills-chatbot/` | 4,000 tokens 미만의 self-contained single-file chatbot Skill profile |
| `src/skills-chatbot-runtime/` | bundled resources 또는 hosted runtime 기능을 사용하는 chatbot Skill profile |
| `src/rules/` | Rule source |

세 Skill profile은 **비표준 repository-local taxonomy**입니다. 같은 capability의 target별 variant가 함께 존재할 수 있으며, profile 간 의미 중복보다 각 harness/platform이 지원하는 규격에서의 효율과 독립 배포를 우선합니다.

Directory-based Skill source package에서 dot-prefixed directory(`.*`)는 non-runtime maintainer surface로 사용합니다. `.docs/baseline/`은 본래 purpose, requirements, invariants, 주요 decisions와 recovery directives를 보존합니다.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agents/` | 로컬 agent runtime 지침 |
| `src/` | 자산 source workspace |
| `tests/` | 저장소 수준 자동화 테스트 |
| `docs/` | 저장소 수준 사람용 문서와 reference |
| `scripts/` | 저장소 자동화 도구 |

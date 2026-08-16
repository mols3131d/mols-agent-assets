# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

## Asset Types

| Type | Purpose |
| --- | --- |
| `agents` | subagent 및 custom agent 정의 |
| `skills` | workspace-capable agent skill |
| `skills-chatbot` | 4,000 tokens 미만의 self-contained single-file chatbot skill |
| `skills-chatbot-runtime` | bundled resources 또는 hosted runtime 기능을 사용하는 chatbot skill |
| `rules` | 재사용 가능한 행동 규칙 |

세 Skill profile은 같은 capability의 target별 variant를 함께 가질 수 있습니다. profile 간 의미 중복보다 각 harness/platform이 지원하는 규격에서의 효율과 독립 배포를 우선합니다.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agents/` | 로컬 agent runtime 지침 |
| `src/` | 자산 source workspace |
| `tests/` | 자동화 테스트 |
| `docs/` | 사람용 문서와 reference |
| `scripts/` | 저장소 자동화 도구 |

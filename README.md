# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

## Asset Types

| Type | Purpose |
| --- | --- |
| `agents` | subagent 및 custom agent 정의 |
| `skills` | workspace를 다루는 agent skill |
| `skills-chatbot` | 자연어 지침만 사용하는 flat chatbot skill |
| `skills-chatbot-runtime` | bundle/runtime 기능을 사용하는 hosted chatbot skill |
| `rules` | 재사용 가능한 행동 규칙 |

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agents/` | 로컬 agent runtime 지침 |
| `src/` | 자산 source workspace |
| `tests/` | 자동화 테스트 |
| `docs/` | 사람용 문서와 reference |
| `scripts/` | 저장소 자동화 도구 |

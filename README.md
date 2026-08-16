# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

## Asset Types

| Type | Purpose |
| --- | --- |
| `agents` | subagent 및 custom agent 정의 |
| `skills` | workspace-capable agent workflow |
| `skills-chatbot` | 자연어 지침만 사용하는 flat chatbot workflow |
| `skills-chatbot-runtime` | bundle/runtime 기능을 사용하는 hosted chatbot workflow |
| `instructions` | 재사용 가능한 행동 지침 |

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agents/` | 로컬 agent runtime 지침 |
| `src/` | 자산 source workspace |
| `tests/` | 자동화 테스트 |
| `docs/` | 사람용 문서와 reference |
| `scripts/` | 저장소 자동화 도구 |

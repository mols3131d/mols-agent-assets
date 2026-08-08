# 자산 개발 가이드

## Directory Roles

- `src/agents/`: subagent 및 custom agent.
- `src/skills/`: 재사용 가능한 agent skill.
- `src/chatbot-skills/`: chatbot-specific skill.
- `src/instructions/`: 재사용 가능한 instruction.
- `tests/`: 자산 및 도구 검증.

## Workflow

1. `<owner>/<type>/<topic>` 브랜치를 생성한다.
1. `src/`에서 자산을 작성하거나 수정한다.
1. 필요한 검증과 `uv run pytest`를 실행한다.
1. 검증된 변경을 배포 브랜치에 병합한다.

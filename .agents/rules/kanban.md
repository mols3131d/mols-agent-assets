# Kanban Rules

`.agents/brain/kanban.md` 운영 규칙.

## 1. Columns

- **`[ ]` Backlog**: 대기 중인 Task.
- **`[-]` In Progress**: 현재 진행 중인 Task.
- **`[x]` Done**: 완료된 Task.

## 2. Operations

- **Single Source of Truth**: 모든 진행 Task는 Kanban으로 중앙 집중 및 동기화.
- **Atomic Task**: 각 Task는 독립적 실행 및 검증 가능 단위로 분할(KISS).
- **Pruning (Context Optimization)**: `Done` 상태의 Task가 10개 초과 시, 오래된 항목부터 자동 삭제.

## 3. Format (Dry & List)

- Checkbox list (`- [ ]`, `- [-]`, `- [x]`) 형식을 엄격히 준수.
- 불필요한 서술 배제, 핵심 Action/Target만 기재.

# Agent Brain

Agent의 데이터 저장소.

## 1. Core Principles

- **Persistency**: 생존 필수 Context 유지.
- **Context Tax Optimization**: 파일 비대화 방지 (Pruning/FIFO).
- **Agent-Friendly**: 고밀도 압축(KISS/DRY, Table/List) 포맷 강제.

## 2. Components

각 파일의 목적 및 세부 운영 규칙은 링크된 Rule을 따른다.

| 항목              | File           | 규정 (Rule)                                 |
| :---------------- | :------------- | :------------------------------------------ |
| **Evolution Log** | `evolution.md` | [evolution.md](/.agents/rules/evolution.md) |
| **Kanban**        | `kanban.md`    | [kanban.md](/.agents/rules/kanban.md)       |
| **Overhand**      | `overhand.md`  | [overhand.md](/.agents/rules/overhand.md)   |

## 3. Operations

1. **Read**: 세션 시작 시 자동 Load.
2. **Write**: 이벤트 발생 시 압축 기록.
3. **Prune**: 만료/불필요 데이터 즉각 제거.

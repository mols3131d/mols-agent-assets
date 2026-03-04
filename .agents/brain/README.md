# Agent Brain

Agent의 데이터 저장소.

## 1. Core Principles

- **Persistency**: 생존 필수 Context 유지.
- **Context Tax Minimize**: 파일 비대화 방지 (Pruning/FIFO).
- **Agent-Friendly**: 고밀도 압축(KISS/DRY, Table/List) 포맷 강제.

## 2. Components

각 파일의 목적 및 세부 운영 규칙은 링크된 Rule을 따른다.

| Item               | File                | Rule                                                  |
| :----------------- | :------------------ | :---------------------------------------------------- |
| **Evolution Log**  | `evolution.md`      | [evolution.md](/.agents/rules/evolution.md)           |
| **Kanban**         | `kanban.md`         | [kanban.md](/.agents/rules/kanban.md)                 |
| **Session-Bridge** | `session-bridge.md` | [session-bridge.md](/.agents/rules/session-bridge.md) |

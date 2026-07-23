---
name: mols-kanban-markdown
description: >
  USE WHEN: managing, creating, updating, or validating Kanban board items using markdown cards.
  EXCLUDES: general software development, or non-Kanban documentation edits.
---

# Mols Kanban Markdown

## Goal

Provide standard routing and setup delegation for managing markdown-based Kanban boards.

## Instructions

### Delegation Model

1. **SKILL.md**는 칸반 조작에 대한 상세 지침을 명시하지 않고, 데이터 경로 내에 위치하는 **`AGENTS.md`**로 동작 지침을 완전 위임합니다.
2. **`AGENTS.md`**는 칸반 카드의 프런트매터 구조 및 작성을 **`.configs/config.jsonc`**와 **`.configs/template.md`**에 명시된 규칙으로 위임하여 작동합니다.
3. 세부 스크립트 실행 및 기술적 검증 로직은 **`workflows/`**로 위임합니다.

### Completion

Report verification status, updated card paths, and status transitions.

## Workflow: Router

### Context

#### Parameters

- **Target Path**: Kanban board directory path.
- **Workflow Route**: Sub-workflow route ID selected from `workflows/INDEX.csv`.

### Procedure

1. Read `workflows/INDEX.csv` once.
2. Resolve matching route IDs (e.g., `validate`).
3. Load the resolved workflow from `workflows/<id>.md` and execute its procedure.

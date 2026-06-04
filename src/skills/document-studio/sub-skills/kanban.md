---
name: kanban
description: Create/update kanban boards for doc-backed work. Use for task status, workflow stages, progress tracking.
---

# Kanban

## Overview

- **Goal**: Create and update kanban boards to track task status and workflow stages.

## Triggers

- User needs a progress board, not a plain checklist.
- Items move through states.
- Status matters more than detailed prose.

## Exclusions

- Simple checklists or todo lists that do not require stage tracking -> use `tasks.md`.
- Technical specs or API specifications -> use `spec.md`.

## Workflow

1. Initialize kanban board:
   ```bash
   python3 scripts/kanban.py init <folder>
   ```
2. Create card:
   ```bash
   python3 scripts/kanban.py create <folder> <title> [--priority low|medium|high] [--assignee x]
   ```
3. Move card to next state:
   ```bash
   python3 scripts/kanban.py move <folder> <card_id> <status>
   ```
4. Update card fields:
   ```bash
   python3 scripts/kanban.py update <folder> <card_id> [--status status] [--priority priority] [--assignee assignee] [--title title]
   ```

## Resources

- `INDEX.csv`: Index of active cards (`todo`, `in-progress`, `review`) in main folder.
- `backlog/`: Folder for backlog (`backlog`) cards.
- `backlog/INDEX.csv`: Index of backlog cards.
- `archive/`: Archive folder for done (`done`) and rejected (`rejected`) cards.
- `archive/INDEX.csv`: Index of archived cards.

### Frontmatter Metadata

| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `id` | String | Y | Unique ID (e.g. `kbn-001`) |
| `title` | String | Y | Card title |
| `status` | Enum | Y | Current status (`backlog`, `todo`, `in-progress`, `review`, `done`, `rejected`) |
| `priority` | Enum | N | Priority (`low`, `medium`, `high`) |
| `description` | String | N | Detailed explanation or summary |
| `assignee` | String | N | Assigned worker or agent |
| `tags` | Array | N | Tags list for classification |

### Kanban Board States

| Status | Active | Description |
| :--- | :--- | :--- |
| `backlog` | Yes | Idea gathering, review waiting (initial backlog) |
| `todo` | Yes | Ready for work (prioritized queue) |
| `in-progress` | Yes | Work active |
| `review` | Yes | Awaiting peer review, feedback, approval |
| `done` | No | Approved, deploy/merge finished |
| `rejected` | No | Idea rejected or discarded |

---

## Rules

- One card = one markdown file.
- Each card markdown file contains Frontmatter metadata.
- Keep card text short.
- Link detailed docs, do not embed.
- Archive done items when board becomes noisy.

## Constraints

- **No README.md Generation**: Do not create or generate `README.md` for boards. Only use `INDEX.csv` files.
- **Do Not Bypass CLI Commands**: Maintain the boards and move cards using the `kanban.py` CLI script.
- **Valid Statuses Only**: Do not use custom statuses. Use only `backlog`, `todo`, `in-progress`, `review`, `done`, or `rejected`.

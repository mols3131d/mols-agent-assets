---
name: kanban
description: >
  Create or update kanban boards for document-backed work. Use when user asks for
  task status boards, workflow stages, or progress tracking.
---

# Kanban

Goal: show work state at a glance.

## Use When

- User needs a board, not a plain checklist.
- Items move through states.
- Status matters more than detailed prose.

## Frontmatter (Metadata)

| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `id` | String | Y | Unique card identifier (e.g. `kbn-001`) |
| `title` | String | Y | Title of the card |
| `status` | Enum | Y | Current status (`backlog`, `todo`, `in-progress`, `review`, `done`, `rejected`) |
| `priority` | Enum | N | Priority level (`low`, `medium`, `high`) |
| `description` | String | N | Detailed explanation or summary of the card |
| `assignee` | String | N | Assigned worker or agent |
| `tags` | Array | N | List of tags for classification |

## States

| Status | Active | Description |
| :--- | :--- | :--- |
| `backlog` | Yes | Idea gathering and review waiting stage (Initial Backlog) |
| `todo` | Yes | Ready for work (Prioritized queue) |
| `in-progress` | Yes | Work currently active |
| `review` | Yes | Awaiting peer review, feedback, or approval |
| `done` | No | Approval complete and deploy/merge finished |
| `rejected` | No | Idea rejected or discarded during the process |

## Structure

| Path | Description |
| :--- | :--- |
| `README.md` | Main kanban board document |
| `INDEX.csv` | Index of active cards (`todo`, `in-progress`, `review`) in main folder |
| `backlog/` | Folder containing backlog (`backlog`) cards |
| `backlog/INDEX.csv` | Index of backlog cards |
| `archive/` | Archive folder for done (`done`) and rejected (`rejected`) cards |
| `archive/INDEX.csv` | Index of archived cards |

## Rules

- One card = one markdown file.
- Each card markdown file must contain Frontmatter metadata.
- Keep card text short.
- Link detailed docs instead of embedding them.
- Archive done items when board gets noisy.

---
name: kanban
description: Create/update kanban boards for doc-backed work. Use for task status, workflow stages, progress tracking.
---

# Kanban

Goal: show work state at glance.

## Use When

- User needs board, not plain checklist.
- Items move through states.
- Status matters more than detailed prose.

## Frontmatter (Metadata)

| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `id` | String | Y | Unique ID (e.g. `kbn-001`) |
| `title` | String | Y | Card title |
| `status` | Enum | Y | Current status (`backlog`, `todo`, `in-progress`, `review`, `done`, `rejected`) |
| `priority` | Enum | N | Priority (`low`, `medium`, `high`) |
| `description` | String | N | Detailed explanation or summary |
| `assignee` | String | N | Assigned worker or agent |
| `tags` | Array | N | Tags list for classification |

## States

| Status | Active | Description |
| :--- | :--- | :--- |
| `backlog` | Yes | Idea gathering, review waiting (initial backlog) |
| `todo` | Yes | Ready for work (prioritized queue) |
| `in-progress` | Yes | Work active |
| `review` | Yes | Awaiting peer review, feedback, approval |
| `done` | No | Approved, deploy/merge finished |
| `rejected` | No | Idea rejected or discarded |

## Structure

| Path | Description |
| :--- | :--- |
| `README.md` | Main kanban board document |
| `INDEX.csv` | Index of active cards (`todo`, `in-progress`, `review`) in main folder |
| `backlog/` | Folder for backlog (`backlog`) cards |
| `backlog/INDEX.csv` | Index of backlog cards |
| `archive/` | Archive folder for done (`done`) and rejected (`rejected`) cards |
| `archive/INDEX.csv` | Index of archived cards |

## Rules

- One card = one markdown file.
- Each card markdown file contains Frontmatter.
- Keep card text short.
- Link detailed docs, do not embed.
- Archive done items when board noisy.

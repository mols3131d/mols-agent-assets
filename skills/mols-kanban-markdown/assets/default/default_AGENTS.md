# Agent Instructions for mols Kanban Markdown (DEFAULT)

## Directory Structure

```text
<kanban_path>/
├── .configs/
│   ├── config.jsonc            # Frontmatter schema and validation settings
│   └── template.md             # Markdown card creation template
├── backlog/                    # Ideas and pending backlog cards (`backlog`)
├── active/                     # Active work-in-progress cards (`todo`, `in_progress`, `review`)
├── archive/                    # Completed or canceled cards (`done`, `rejected`)
├── README.md                   # Kanban board overview and index document
└── AGENTS.md                   # Agent guidelines for Kanban management
```

## Frontmatter Schema

See `<kanban_path>/.configs/config.jsonc`

## Write

Copy `<kanban_path>/.configs/template.md` to `<kanban_path>/backlog/`.

Replace placeholders. Follow and remove comments.

## Validate Doc Format

See `<this_skill_path>/workflows/validate.md`

## Lifecycle

```mermaid
graph TD
    %% Folders and States
    subgraph backlogFolder [backlog/]
        backlog[backlog: Idea / Draft]
    end

    subgraph activeFolder [active/]
        todo[todo: Planned]
        in_progress[in_progress: Working]
        review[review: Testing / Review]
    end

    subgraph archiveFolder [archive/]
        done[done: Completed]
        rejected[rejected: Canceled / Abandoned]
    end

    %% State Transitions (Folder Movement)
    backlog -->|Move to active/| todo
    todo --> in_progress
    in_progress --> review

    %% Archiving (Move to archive/)
    review -->|Approved| done
    todo -->|Canceled| rejected
    in_progress -->|Canceled| rejected
    review -->|Rejected| rejected
```

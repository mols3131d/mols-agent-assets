# 02. Agent Skills Specification

## Core Rules

- `SKILL.md` required (YAML frontmatter + Markdown body).
- Must have `name` and `description`.
- Follow strict naming, relative paths, progressive disclosure.

## Directory

```text
skill-name/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

## `SKILL.md` Format

```markdown
---
name: pdf-processing
description: Extract/merge PDFs. Use when handling PDFs.
---
# PDF Processing
[Instructions here]
```

### Frontmatter

| Field | Req | Rules |
|---|---|---|
| `name` | Yes | 1-64 chars, a-z0-9-, no edge/double hyphens, matches parent dir. |
| `description` | Yes | 1-1024 chars, states purpose and trigger contexts. |
| `license` | No | License name or path. |
| `compatibility` | No | Env constraints (max 500 chars). |
| `metadata` | No | Custom key-value pairs. |
| `allowed-tools` | No | Approved tools (space separated, experimental). |

### Description Rule

Good: "Extracts PDF text. Use for PDFs."
Bad: "Helps with PDFs." (too broad).

## Markdown Body

- Step-by-step procedures.
- Input/output examples.
- Edge cases.
- Validation/recovery.
Move heavy details to `references/`.

## Optional Directories

- `scripts/`: Self-contained, robust error handling (Python, Bash, JS).
- `references/`: Deep docs, schemas. Split by topic. Reference from `SKILL.md`.
- `assets/`: Templates, images, dummy data.

## Progressive Disclosure Limits

- Metadata: ~100 tokens.
- Instructions: < 5000 tokens (keep under 500 lines).
- Resources: Load strictly on-demand.
Use relative paths (e.g., `See [API errors](references/api-errors.md)`).

## Checklist

- [ ] Dir matches `name`.
- [ ] `name`/`description` rules met.
- [ ] Body focused on core workflow.
- [ ] Relative paths only.
- [ ] Tested with validator (`skills-ref validate ./my-skill`).

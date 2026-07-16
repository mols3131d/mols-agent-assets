# Agent Skill Directories

Core directory, file structure specification for agent skills.

## Directory Structure Specification

Maintain minimum structure required for skill.

| Path | Add when |
| --- | --- |
| `SKILL.md` | Always |
| `references/` | Knowledge long, conditional |
| `scripts/` | Deterministic logic repeats ≥2 times |
| `assets/` | Output material copied, reused |
| `workflows/INDEX.csv` + workflow modules | Workflows share domain, load selectively |

## Rules

- No empty, non-compliant directories.
- No unused examples, nested discoverable `SKILL.md` files.

---
name: routerize-skills
description: >
  WHAT: Consolidate multiple general skills into a single Routing Skill.
  WHEN: User wants to group, merge, or convert several skills into a router pattern.
  WHEN NOT: Creating a new skill from scratch, or renaming single assets.
  KEYWORDS: routerize, route, routing, merge, group, consolidate
---

# routerize-skills

Convert and consolidate multiple individual skills into a unified routing structure.
Refer to [routing-skill-structure.md](../references/routing-skill-structure.md) for architectural details.

## Goal & Done Criteria

- **Goal**: Group specified skills under a new routing skill efficiently.
- **Done Criteria**:
  - The target routing skill is initialized with `SKILL.md` and `sub-skills/INDEX.csv`.
  - The source skills are moved/flattened according to the selected mode (`lite` or `full`).
  - Target's `INDEX.csv` contains routing records for all migrated skills.

## Modes

- **`lite` (Default)**: Moves the entire skill folder into `sub-skills/<skill-name>` and renames its internal `SKILL.md` to `SUB-SKILL.md`. Preserves original directory isolation.
- **`full`**: Flattens the skill by moving its `SKILL.md` to `sub-skills/<skill-name>.md`. Consolidates shared assets (`assets/`, `scripts/`, etc.) into the master router's directories, renaming files automatically if collisions occur, and updating internal markdown paths.

## Workflow

1. **Invoke Script**:
   Use the Python script located at `scripts/routerize_skills.py` to perform the heavy lifting.
   ```bash
   python3 scripts/routerize_skills.py --mode <lite|full> --target <path/to/new-router-skill> <path/to/skill1> <path/to/skill2>
   ```
2. **Verify Output**:
   Ensure the target routing skill was generated properly and the source skills were safely migrated.

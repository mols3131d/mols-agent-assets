---
name: agent-skill
description: >
  Create, improve, evaluate, validate agent skills. Use when user asks to make,
  rewrite, check, merge, compress, or design skill content, structure,
  frontmatter, scripts, or validation.
---

# Agent Skill

Goal: good skill, low LLM cost. Scripts first. LLM after scope narrow.

## Rules

- One skill = one job.
- DRY: one rule, one place.
- YAGNI: no empty dirs/spec assets/client files unless asked.
- Agent-readable: commands, criteria, ask/stop points.
- `SKILL.md` = common path. Rare/long detail moves out.
- Use scripts/commands before broad reading.
- Preserve existing behavior in improve mode unless user asks change.

## Flow

### 1. Mode

| Mode | When | First |
| --- | --- | --- |
| Create | target absent | scaffold/check path |
| Improve | target exists | inspect files + warnings |
| Evaluate | review only | run checks, report findings |

### 2. Script/command first

| Need | Use |
| --- | --- |
| files | `rg --files <skill-dir>` |
| duplicate rules | `rg "<term>" <skill-dir>` |
| size | `wc -l <files>` |
| validate | `python3 scripts/validate_asset.py <skill-dir> --type skill` |
| scaffold | `python3 scripts/init_asset.py <name> --type skill --path <dir>` |
| scaffold routing skill | `python3 scripts/init_asset.py <name> --type skill --path <dir> --routing-skill` |

Read index/frontmatter first. Then read only files tied to failing check or user
request.

### 3. Define/refine job

- `name`: kebab-case.
- `trigger`: user phrases that activate.
- `output`: files/edits/checks/decisions.
- `exclusion`: nearby requests to skip.

### 4. Structure

| Path | Add when |
| --- | --- |
| `SKILL.md` | always |
| `references/` | detail >~50 lines or conditional |
| `scripts/` | deterministic task repeats 2+ times |
| `assets/` | files copied/embedded/reused as-is |
| `sub-skills/` | 3+ sub-tasks, request usually needs one |

No empty optional dirs. Split responsibility -> new skill/sub-skill.
Use `--routing-skill` when `sub-skills/` is needed from scaffold.

### 5. Frontmatter

| Field | Rule |
| --- | --- |
| `name` | required, folder name, <=64, kebab-case |
| `description` | required, <=1024, job + trigger phrases |
| `compatibility` | optional, real runtime/client req only |
| `license` | optional, only when needed |
| `metadata` | optional, only when consumed |
| `allowed-tools` | optional, only when supported |

`name`: lowercase letters, numbers, single hyphens. No edge/repeated hyphen.

#### Description Field

Critical for agent indexing. Keep short to minimize token and inference costs.
Must include:

1. **What:** Core capability of the skill.
2. **When to use:** Triggers and specific scenarios.
3. **When NOT to use:** Exclusions and boundaries.
4. **Keywords:** Terms for easy search and routing.

### 6. Body

The following 8 core concepts should ideally be covered, but exact section titles are **flexible** and sections can be **omitted** if unnecessary. When editing an existing skill, **preserve its original structure and titles**.

| Concept | Description |
| --- | --- |
| **Overview** | Brief context or summary of the skill. |
| **Goal** | Core purpose and scope of responsibility. |
| **Non-Goal** | Areas intentionally excluded to prevent scope creep. |
| **When to Use** | Exact conditions and user trigger phrases to activate. |
| **When NOT to Use** | Excluded scenarios or when to use another skill instead. |
| **Workflows** | Ordered sequence of steps or tasks to accomplish the goal. |
| **Instructions** | Positive rules or guidelines the agent must follow. |
| **Constraints** | Strict negative rules the agent must never violate. |

### 7. Sub-skill index, if used

```csv
name,overview,trigger,exclusion
```

One row = one line. Routing signal only, no full instructions.

### 8. Validate

| Check | Level | Rule |
| --- | --- | --- |
| frontmatter | error | required fields, length, allowed fields, folder match |
| trigger | warning | `description` has usable trigger |
| body length | warning | body <=500 lines |

Errors fail. Warnings pass, review.

### 9. Improve loop

- Run check.
- Edit failing/requested area only.
- Re-run same check.
- Stop when errors gone; warnings fixed or accepted.

### 10. Gate

- Triggers correct requests.
- Skips nearby wrong requests.
- First screen enough to act.
- No duplicated rules.
- No empty dirs/unused examples.
- Scripts non-interactive, clear exit codes.
- LLM edits only what scripts cannot decide.

## Output

Report: changed files, validation result, remaining risk/skipped check.

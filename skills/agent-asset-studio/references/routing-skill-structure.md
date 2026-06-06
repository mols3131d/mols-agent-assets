# Routing Skill Structure

Terse reference for designing and structuring routing skills.

## 1. Purpose

- **Efficient Indexing**: Resolves the inefficiency of scanning numerous separate skill directories as capabilities expand.
- **Cost Optimization**: Consolidates common scripts and assets under one master router, minimizing context size and inference overhead.

## 2. Core Components

### `SKILL.md` (The Router)
- Acts as the primary entry point.
- Does NOT contain the actual execution workflows for individual tasks.
- Guides the agent to read `INDEX.csv` and route the user's request to the appropriate sub-skill.

### `INDEX.csv` (The Registry)
- A lightweight index containing minimal data needed for the LLM to make an accurate routing decision.
- Format: `name,overview,keywords,trigger,exclusion`
- The agent reads this first to locate the target sub-skill without loading all sub-skill instructions into context.

## 3. Sub-Skill Organization

Routing skills allow two layouts for their children within the `sub-skills/` directory:

1. **Flat Markdown** (For simple tasks)
   - Path: `sub-skills/<skill-name>.md`
   - Ideal for concise, single-file instructions.

2. **Nested Directory** (For complex tasks or migrated skills)
   - Path: `sub-skills/<skill-name>/SKILL.md`
   - Used when migrating an existing skill to preserve its isolated assets, references, or folder structure.

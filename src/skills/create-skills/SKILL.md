---
name: create-skills
description: Scaffold new agent skills. Enforce standard directories, high-density instructions, and versioning.
---

# Create Skills

> Skill Scaffolding Standard

Enforce standard procedures and structures for creating new agent skills.

## Workflow

Execute steps sequentially to scaffold a new skill:

### 1. Define Triggers

- Identify the core problem.
- Define specific `When to use` trigger conditions for agent invocation.
- Use triggers as the baseline for the `description` metadata.

### 2. Scaffold Directory

- Assign a `kebab-case` skill name.
- Copy `./templates/` to the new skill directory to auto-provision `SKILL.md`, `README.md`, and `VERSION`.

### 3. Author Agent Instructions (`SKILL.md`)

Draft execution instructions for agents.

- **Frontmatter**:
  - Match `name` to the `kebab-case` directory name.
  - Optimize `description` for agent discovery: specify context, function, and expected result.
- **Mandatory Section**: Include `1. When to use` to define invocation conditions.
- **Formatting**: Use **High-Density English** and **Affirmative Framing** (state target actions, omit negative constraints).

### 4. Author Human Guide (`README.md`)

Draft overview for human maintainers.

- Document objective, structure, and usage instructions.

### 5. Extend & Review

- Provision `scripts/` or `references/` if required.
- Present structure and drafts to the human user for approval (HITL).

## Directory Structure

```txt
[skill-name]/
├── SKILL.md          # [Required] Agent instructions & metadata
├── README.md         # [Required] Human overview & guide
├── VERSION           # [Required] Semantic versioning
├── templates/        # [Optional] Related templates
├── scripts/          # [Optional] Automation scripts
├── .human/           # [Optional] Human-only docs. Agent access prohibited.
└── references/       # [Optional] Technical references
```

### `.human/` Directory Constraints

Restricted to human users. Agents must omit reading or modifying this directory. Enforce via `.aiexclude`.

# Agents Skills

Skills are an open standard for extending agent capabilities. A skill is a folder containing a SKILL.md file with instructions that the agent can follow when working on specific tasks.

## Skill folder structure

```txt
.agents/skills/my-skill/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

## `SKILL.md`

```markdown
---
name: "[skill-name]"
description: "[description]"
---

# [Skill Name]

Detailed instructions for the agent go here.

## When to use this skill

- Use this when...
- This is helpful for...

## How to use it

Step-by-step guidance, conventions, and patterns the agent should follow.
```

### Frontmatter fields

| Field         | Required | Description                                                                                                                          |
| :------------ | :------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | No       | A unique identifier for the skill (lowercase, hyphens for spaces). Defaults to the folder name if not provided.                      |
| `description` | Yes      | A clear description of what the skill does and when to use it. This is what the agent sees when deciding whether to apply the skill. |

## Best practices

- Keep skills focused: Each skill should do one thing well. Instead of a "do everything" skill, create separate skills for distinct tasks.

- Write clear descriptions: The description is how the agent decides whether to use your skill. Make it specific about what the skill does and when it's useful.

- Use scripts as black boxes: If your skill includes scripts, encourage the agent to run them with --help first rather than reading the entire source code. This keeps the agent's context focused on the task.

- Include decision trees: For complex skills, add a section that helps the agent choose the right approach based on the situation.

---

- Reference: `https://antigravity.google/docs/skills`

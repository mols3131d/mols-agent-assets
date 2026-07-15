# 01. Agent Skills Overview

## Core Concept

- Agent Skills = domain knowledge + workflows.
- Lightweight, open format.
- Principle: Progressive disclosure (load only on-demand).

## Structure

```text
my-skill/
├── SKILL.md          # Required (metadata + instructions)
├── scripts/          # Optional (executable code)
├── references/       # Optional (detailed docs)
└── assets/           # Optional (templates, data)
```

## Why

- Domain expertise: Reuse team rules.
- Repeatable workflow: Consistent steps.
- Cross-product reuse: Share across agents.

## Progressive Disclosure

1. **Discovery**: Load `name`, `description`.
2. **Activation**: Load `SKILL.md` on match.
3. **Execution**: Follow instructions. Load scripts/assets on demand.
Benefit: Saves tokens, avoids instruction bloat.

## When To Use

- Repeatable multi-step tasks.
- Custom project rules/APIs.
- Strict output formatting.
Avoid: Basic one-off prompts, general LLM knowledge.

## Checklist

- [ ] `SKILL.md` present.
- [ ] `name`/`description` accurately trigger skill.
- [ ] Core steps only in body.
- [ ] Details in `references/`, code in `scripts/`.
- [ ] On-demand loading only.

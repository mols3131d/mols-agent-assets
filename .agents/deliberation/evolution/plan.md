# Deliberation: Evolution Skill Draft Plan

## Background

The current `evolution.md` rule acts as a constant "context tax" even when no rule changes are happening. By converting it into a **Skill**, we ensure that the complex protocol for rule evolution is only retrieved when an agent explicitly decides to propose or manage a rule.

## Proposed Structure

- **Folder**: `.agents/skills/rule-evolution/`
- **SKILL.md**: Contains the logic transferred from `rules/evolution.md`, but structured with "When to use" and "How to use" sections.
- **scripts/suggest.py**: A CLI tool for agents to add candidates to the log without manual markdown editing (reducing formatting errors).
- **assets/log_template.md**: Standardized template for the `brain/evolution.md` log.

## Migration Strategy

1. Create the new directory structure.
2. Initialize `SKILL.md` with enhanced instructions.
3. Develop the `suggest.py` script.
4. Verify the skill works by adding a dummy candidate.
5. Remove `rules/evolution.md` to free up context.

## Next Steps

- [ ] User review of this draft.
- [ ] Finalize the `suggest.py` script requirements.

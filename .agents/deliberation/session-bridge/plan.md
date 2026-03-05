# Deliberation: Session-Bridge Skill Migration

## Background

The `session-bridge` protocol is currently a static rule. Since it involves specific lifecycle actions (Write/Clear) and structured data generation (Narrative/Entry Point), it is better suited as a **Skill**. This allows for automation and reduces constant context tax.

## Proposed Structure

- **Folder**: `.agents/skills/session-bridge/`
- **SKILL.md**: Instructions for summarizing the current session and preparing for the next one.
- **scripts/bridge.py**: (Future) Automation to help generate the narrative and entry point based on session logs.
- **assets/bridge_template.md**: Markdown template for session handover.

## Migration Strategy

1. Create the skill directory and `SKILL.md`.
2. Define a clear template for session handover.
3. Remove `rules/session-bridge.md`.
4. (Optional) Enhance with a script to summarize the current `brain/logs`.

## Next Steps

- [ ] User review of this draft.
- [ ] Implementation of `SKILL.md`.

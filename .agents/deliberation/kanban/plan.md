# Deliberation: Kanban Skill Migration (via Toon)

## Proposal

Migrate `.agents/rules/kanban.md` into a dedicated **Skill**. This skill will manage the project's task lifecycle. As discussed with the `session-bridge` improvement, we will also evolve the Kanban storage format from Markdown checkboxes to a structured **Toon (`.toon`)** file.

## Why Toon for Kanban?

1. **Status Visibility**: Instead of `[ ]`, `[-]`, `[x]`, we use explicit status strings (`BACKLOG`, `IN_PROGRESS`, `DONE`, `BLOCKED`).
2. **Metadata Enrichment**: Add `priority`, `owner`, or `labels` as CSV columns without cluttering the list.
3. **Automated Pruning**: Facilitates script-based cleanup (the 10-item limit mentioned in the original rule).

## Proposed Kanban Schema (`kanban.toon`)

```toon
kanban:
  meta:
    last_updated: "[ISO-8601]"
    active_tasks: 2
    total_completed: 15

  tasks[N]{id,status,prio,task,note}:
    1,DONE,H,Initialize ACE project,Initial setup complete
    2,IN_PROGRESS,H,Migrate Kanban rule to skill,Planning phase
    3,BACKLOG,M,Implement automated pruning script,Future tech debt
```

## Migration Strategy

1. Create `.agents/skills/kanban/SKILL.md`.
2. Initial draft of `assets/kanban.toon` template.
3. (Future) `scripts/manage_kanban.py` to handle pruning and status updates.
4. Delete `.agents/rules/kanban.md`.

## Next Steps

- [ ] User review of the "Kanban-as-a-Toon" proposal.
- [ ] Implementation of the `kanban` skill assets.

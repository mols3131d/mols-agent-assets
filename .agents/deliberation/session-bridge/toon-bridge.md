# Deliberation: Toon-based Session Bridge

## Proposal

Replace the Markdown-based `bridge.md` with a structured `bridge.toon` format. This leverages the hybrid YAML/CSV nature of Toon to provide a more rigid yet expressive bridge between sessions.

## Concept Structure

```toon
bridge:
  meta:
    session_id: "423580c5-cc80"
    timestamp: "2026-03-05T23:55:00"
    focus: "Session-bridge automation via Toon format"

  narrative: >
    Current session focused on migrating rules to skills.
    We successfully converted 'evolution' and are now
    rethinking 'session-bridge' using the Toon format discovered in te.toon.

  hurdles[1]{id,description,difficulty}:
    1,Ensuring the agent doesn't forget to trigger the bridge skill,high

  entry_points[2]{id,priority,task,tool_hint}:
    1,high,Implement session-bridge SKILL.md for Toon,replace_file_content
    2,medium,Create python parser/generator for .toon files,run_command
```

## Advantages

1. **Machine-Readable**: Easier for scripts to parse hurdles and automatically populate the next task list.
2. **Standardized Context**: Forces a consistent structure (id, priority, narrative) instead of vague markdown prose.
3. **Hybrid Power**: YAML for high-level context, CSV for repeating data like tasks and blockers.

## Next Steps

- [ ] Define the official `.toon` schema for session bridging.
- [ ] Update `SKILL.md` to instruct the agent to write in `.toon`.
- [ ] Develop a small python utility in `scripts/agents/` to validate or update `.toon` bridges.

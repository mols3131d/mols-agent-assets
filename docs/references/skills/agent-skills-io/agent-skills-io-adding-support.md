# 06. Adding Skills Support to Clients

## Core Lifecycle

Discover → Parse → Disclose → Activate → Preserve.
Provide metadata first. Load body/resources on-demand. Handle untrusted code securely.

## 1. Discover

- **Paths**: Scan project (`.agents/skills/`) and user (`~/.agents/skills/`).
- **Rules**: Find `SKILL.md` inside directories. Ignore `.git`, `node_modules`. Limit depth/count.
- **Collisions**: Project overrides User. Log shadowed skills.
- **Trust**: Project skills are untrusted. Add consent gates before loading.

## 2. Parse

- Extract YAML frontmatter (between `---`).
- **Lenient Rules**:
  - `name` mismatch / too long -> Warn, but load.
  - Missing `description` -> Skip (cannot activate).
  - Malformed YAML -> Auto-fix quotes if possible, else skip.
- Store `name`, `description`, `location`.

## 3. Disclose

- Feed compact JSON catalog (metadata only) to model via system prompt or tool.
- Hide disabled/unauthorized skills.
- Omit if 0 skills found.

## 4. Activate

- **Model-driven**: Model sees catalog, decides to read body.
  - File-read: Model runs `cat location`.
  - Dedicated Tool: `activate_skill(name)`. Handles telemetry, formatting, consent.
- **User-driven**: `/skill name` in chat UI.
- Expose resource list, but do NOT eager-load contents.
- Consider path allowlisting to skip read-consent prompts for trusted skills.

## 5. Preserve Context

- **Compaction Protection**: Prevent summarizers from deleting active skill instructions from context.
- **Deduplication**: Track active skills; do not inject body multiple times per session.
- **Subagents (Optional)**: Delegate complex skill execution to background sessions.

## Checklist

- [ ] Scan `.agents/skills/`.
- [ ] Trust gate for project-level skills.
- [ ] Lenient parsing & skip invalid metadata.
- [ ] Disclose metadata catalog only.
- [ ] Activation path (file-read or tool) defined.
- [ ] Protect active skills from context compaction.
- [ ] Prevent duplicate activations.

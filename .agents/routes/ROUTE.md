# Routes

This directory contains repository routing metadata for chat-runtime compatibility.

Use only the route files relevant to the current task and target paths.

- `skills.jsonl` — select task-relevant Skills by `name` and `description`, then load the selected `source`.
- `rules.jsonl` — match known target paths against Rule selectors, then load matching `source` entries.

Each JSONL route file reserves its first line for `_meta` instructions. Remaining lines are route entries.

Route files are discovery metadata only. `AGENTS.md`, Skills, and Rules remain authoritative.

# Routes

Default single entrypoint for repository routing assets when useful. This convention is
optional; repositories may use another routing entrypoint or direct route-file links.

- [Skills](skills.jsonl) — select by `name` and `description`, then load the selected `source`.
- [Rules](rules.jsonl) — match target paths against selectors, then load matching `source` entries.

Each JSONL file reserves its first line for `_meta` routing instructions. Remaining lines are route entries.

Routes are discovery metadata only. `AGENTS.md`, Skills, and Rules remain authoritative.

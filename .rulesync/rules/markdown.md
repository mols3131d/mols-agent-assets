---
root: false
targets: ["claudecode", "copilot", "copilotcli", "antigravity-ide", "antigravity-cli"]
description: "Markdown prose를 작성하거나 수정할 때 고정 열 너비로 hard-wrap하지 않는다."
globs: ["**/*.md"]
---

# Markdown Source Style

Do not hard-wrap Markdown prose to a fixed column width. Keep each paragraph you author or materially edit on one physical source line unless a line break is semantically meaningful or required by Markdown syntax, an embedded format, or repository tooling.

Apply the same rule to prose-valued Markdown frontmatter such as YAML scalar descriptions when syntax permits. Do not split a sentence across physical lines merely to satisfy an arbitrary width.

Keep structural line breaks where Markdown or the embedded format gives them meaning, including list items, tables, fenced code, blockquotes, explicit line breaks, and structured YAML.

Do not reflow unrelated existing paragraphs solely to normalize source style unless the task includes Markdown formatting or source-style cleanup.

Do not inspect or imitate formatter or linter configuration merely to shape prose. Deterministic formatting and lint normalization belong to repository automation; use that machinery when formatting verification or normalization is actually needed.

## Related Skills

These are context pointers, not dependency edges. Load only the Skill whose task scope actually applies.

- [`mols-documentation`](https://github.com/mols3131d/mols-agent-assets/blob/main/src/rulesync/.rulesync/skills/mols-documentation/SKILL.md) — human-readable document authoring, structure, readability, navigation, and ownership.
- [`mols-markdown-maintenance`](https://github.com/mols3131d/mols-agent-assets/blob/main/src/rulesync/.rulesync/skills/mols-markdown-maintenance/SKILL.md) — deterministic Markdown maintenance when formatting, linting, frontmatter validation, or index maintenance is itself required.

## Related References

Read only the reference that can materially change the current Markdown decision; do not preload this list.

- [Markdown reference](https://github.com/mols3131d/mols-agent-assets/blob/main/src/rulesync/.rulesync/skills/mols-documentation/references/markdown.md) — general Markdown-specific expression and source/rendered-view guidance.
- [Documentation Principles](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/documentation/principles.md) — repository documentation quality and information-architecture principles.
- [Formatting](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/development/formatting.md) — repository formatter ownership and changed-only formatting workflow.
- [Frontmatter](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/documentation/frontmatter.md) — repository Markdown frontmatter contract.

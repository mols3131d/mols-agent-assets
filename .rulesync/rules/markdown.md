---
root: false
targets: ["claudecode", "copilot", "copilotcli", "antigravity-ide", "antigravity-cli"]
description: "Markdown prose를 작성하거나 수정할 때 고정 열 너비로 hard-wrap하지 않는다."
globs: ["**/*.md"]
---

# Markdown Source Style

Do not hard-wrap authored or materially edited Markdown prose to a fixed column width. Keep a paragraph on one physical source line unless Markdown syntax, an embedded format, or a meaningful break requires otherwise. This also applies to prose-valued YAML frontmatter when permitted.

Preserve structural breaks in lists, tables, fences, blockquotes, explicit line breaks, and structured YAML. Do not reflow unrelated existing prose unless the task explicitly includes formatting or source-style cleanup.

Formatting and lint normalization belong to repository tooling, not manual wrapping.

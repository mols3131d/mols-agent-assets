---
name: "antigravity rules"
description: "These rules are specifically for Antigravity and do not apply to other agents."
trigger: always_on
tags: []
fmContentType: agent-rule
---

# Antigravity Rules

- **Language**: All artifacts (`task.md`, `implementation_plan.md`, `walkthrough.md`) must be written in Korean.
- **Conciseness**: Keep all responses and artifacts as concise as possible to minimize tokens.
- **Paths**: Use absolute paths (`file:///` scheme) in chat responses. Otherwise, use context-appropriate paths (e.g., relative paths in documents).

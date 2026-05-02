---
name: "antigravity rules"
description: "These rules are specifically for Antigravity and do not apply to other agents."
trigger: always_on
tags: []
fmContentType: agent-rule
---

# Antigravity Rules

## Anti-patterns

- **No Absolute Paths**: Avoid exposing system-specific absolute paths in artifacts; use workspace-relative paths.

## Policy

- **Language**: All artifacts (`task.md`, `implementation_plan.md`, `walkthrough.md`) must be written in Korean.
- **Conciseness**: Keep all responses and artifacts as concise as possible to minimize tokens.

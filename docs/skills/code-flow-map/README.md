---
description: code-flow-map Agent Skill의 사용, 구성 파일, 유지보수 명세를 찾을 때 참고하는 문서입니다.
---

# Code Flow Map — Agent Skill (draft)

This package contains a reusable Agent Skill for generating a Markdown code-flow report with a Mermaid diagram, an evidence table and collapsible inline HTML details.

## Source and use

The authored source is at [`src/rulesync/.rulesync/skills/code-flow-map/`](../../../src/rulesync/.rulesync/skills/code-flow-map/SKILL.md), not the draft package's `.github/skills/` location. Keep the package resources together when projecting or installing it into a supported coding agent. This repository stores the reusable source; it does not install the Skill into the repository runtime automatically.

Invoke from an agent with the Skill available:

```text
/code-flow-map Trace the API entry point to database reads. Mark all inferred edges.
```

Or ask naturally to create an evidence-backed code flow map. When a report file is requested, the skill writes `docs/code-flows/<topic>.md` by default.

Open the generated `.md` file in a Markdown preview that supports Mermaid and basic HTML `<details>/<summary>`. Do not lower preview security settings or enable scripts to view reports.

## Files

- [`SKILL.md`](../../../src/rulesync/.rulesync/skills/code-flow-map/SKILL.md): behavior and evidence rules
- [`templates/report.md`](../../../src/rulesync/.rulesync/skills/code-flow-map/templates/report.md): output template
- [`examples/demo-report.md`](../../../src/rulesync/.rulesync/skills/code-flow-map/examples/demo-report.md): small, synthetic preview with expandable evidence
- [`examples/demo-code.ts`](../../../src/rulesync/.rulesync/skills/code-flow-map/examples/demo-code.ts): source fixture for the preview
- [`spec.md`](spec.md): maintenance specification, acceptance criteria, and regression checks

## Notes

- The skill directs an existing coding agent; it is not a code analyzer or independent static-analysis engine.
- It distinguishes `STATIC` call relationships from `OBSERVED` runtime traces and AI hypotheses.
- It does not require a new runtime, server, or executable HTML/JavaScript.

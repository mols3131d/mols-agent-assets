---
name: load-context-agent-assets
description: >-
  Load source-first authoring context for agent-facing behavioral assets such as Skills,
  Rules, Prompts, Agents, subagents, tool guidance, guardrails, and templates. Use when
  creating, editing, simplifying, reviewing, or evaluating such an asset, including
  decisions about activation, authority, context cost, responsibility boundaries,
  portability, or evaluability. Do not use for ordinary human-facing prose or product
  code that does not define agent behavior.
---

# Contract

This Skill acts as an **authority router**, not as the workflow that owns the artifact.

Before materially designing or revising an agent asset:

1. Identify the actual source format, target model/harness/platform, and deployment surface.
1. Read current authoritative target documentation when it can change the design.
1. Read only the narrow authoring references relevant to the decision.
1. Let the active workflow create, edit, validate, package, or publish the artifact.

Do not copy fast-changing platform behavior into this Skill and do not treat remembered vendor behavior as current authority when it can be checked.

# Authoring Sources

For general agent-asset authoring, load only the concern that matters:

- [Design principles](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/common/design-principles.md) — responsibility, duplication, simplicity, context cost
- [Instruction authoring](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/common/instruction-authoring.md) — trigger/action/constraint/validation wording

When human-facing maintainer documentation is materially in scope, compose with `load-context-human-writing` rather than maintaining or loading a duplicate prose guide here.

When the target platform publishes an authoritative specification or authoring guide for the asset type, that target source outranks these general references for target-specific behavior.

# Personal Overlay — mols

Do **not** apply personal conventions merely because this Skill or repository belongs to mols.

Apply the personal overlay only when one of these is established:

- the user explicitly requests mols personal conventions or standards;
- project/repository instructions declare them;
- the target is a mols personal project or personal asset that is being maintained under those conventions.

When the overlay applies, read only the applicable convention:

- [Rulesync](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/tooling/rulesync.md) when Rulesync source ownership matters
- [Agent Asset Naming Convention](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/common/naming.md) when filesystem naming matters

For Skill-specific work, also use `load-context-agent-skills` and its Skill-specific sources.

Do not invent a repository-local asset taxonomy when the active source framework already defines the relevant feature model.

# Fallback

If authoritative sources cannot be accessed, preserve the established source/target boundary, avoid introducing unverified platform-specific behavior or metadata, and expose any unresolved assumption that can materially affect the result. Do not reconstruct detailed platform or personal rules from memory.

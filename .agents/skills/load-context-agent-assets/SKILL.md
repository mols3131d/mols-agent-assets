---
name: load-context-agent-assets
description: Load source-first authoring context for agent-facing behavioral assets such as Skills, Rules, Prompts, Agents, subagents, tool guidance, guardrails, and templates. Use when creating, editing, simplifying, reviewing, or evaluating such an asset, including decisions about activation, authority, context cost, responsibility boundaries, portability, or evaluability. Do not use for ordinary human-facing prose or product code that does not define agent behavior.
---

# Contract

This Skill acts as an **authority router**, not as the workflow that owns the artifact.

Before materially designing or revising an agent asset:

1. Identify the asset type, target model/harness/platform, and deployment surface.
1. Read current authoritative target documentation when it can change the design.
1. Read only the narrow authoring references relevant to the decision.
1. Let the active workflow create, edit, validate, package, or publish the artifact.

Do not copy fast-changing platform behavior into this Skill and do not treat remembered vendor behavior as current authority when it can be checked.

# Authoring Sources

For general agent-asset authoring, use the maintained references in:

- [Common agent-asset principles](https://github.com/mols3131d/mols-agent-assets/tree/main/docs/references/common/principles)
- [LLM-readable instructions](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/common/authoring/agent-assets-authoring-llm-readable-instructions.md)
- [Human-readable documents](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/common/authoring/agent-assets-authoring-human-readable-documents.md)

Read the specific reference only when its concern matters. Do not load every linked document by default.

When the target platform publishes an authoritative specification or authoring guide for the asset type, that target source outranks these general authoring references for target-specific behavior.

# Personal Overlay — mols

Do **not** apply personal conventions merely because this Skill or repository belongs to mols.

Apply the personal overlay only when one of these is established:

- the user explicitly requests mols personal conventions or standards;
- project/repository instructions declare them;
- the target is a mols personal project or personal asset that is being maintained under those conventions.

When the overlay applies, read the applicable authority before using the convention:

- [Personal Agent Asset Standard](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/common/standards/agent-assets-standard-personal.md)
- [Agent Asset Naming Convention](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/common/standards/agent-assets-naming-convention.md)

For Skill-specific work, also use `load-context-agent-skills` and its Skill-specific sources.

# Fallback

If authoritative sources cannot be accessed, do not invent detailed platform or personal rules. Preserve only these stable defaults until verification is possible:

- one coherent responsibility per asset;
- one authoritative owner per durable rule;
- explicit activation, action, authority, and observable validation where they matter;
- no speculative structure or mechanism without a current need;
- minimize context without removing behavior-critical boundaries.

Expose any unresolved source-dependent assumption that can materially affect the result.

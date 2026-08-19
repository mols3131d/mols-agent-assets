# Asset Design

Use this reference only when asset type, naming, portability, or project-owned
conventions are unclear.

## Choose the Asset Type

Choose by responsibility, activation, load timing, and authority.

| Type | Best for | Avoid when |
| --- | --- | --- |
| Agent Skill | Repeatable domain workflow loaded on demand | A rule must always apply or an isolated specialist persona is required |
| Custom Agent | Specialist role, isolated context, or scoped tools | The behavior is a reusable procedure for many agents |
| Instruction / Rule | Repository or path policy that should apply automatically | The work is occasional or multi-step |
| Prompt | Explicit user-invoked task starter | Automatic policy or reusable workflow package |
| Hook | Deterministic enforcement at a runtime event | Semantic judgment |
| MCP configuration | External capability and data access | Static guidance or local deterministic logic |
| Template / Asset | Output material copied or transformed | Instructions or decisions |
| Asset set | Multiple assets that genuinely need coordinated ownership | One focused asset covers the job |

Before creating a new owner, check whether an existing asset can be extended
without responsibility or trigger collision.

## Naming

Use the first available authority:

1. explicit project policy;
1. neighboring accepted convention;
1. target-runtime convention;
1. lowercase kebab-case fallback based on responsibility.

Prefer the shortest name that still distinguishes responsibility. Never rename an
accepted asset without authority and reference updates.

## Skill Authoring Convention

A project may define a preferred Skill specification for frontmatter, folder
structure, or other authoring conventions. Treat it as applicable when:

- creating a Skill;
- adding substantial Skill functionality;
- explicitly refactoring Skill structure;
- project policy explicitly requires current compliance.

Do not normalize a narrow fix, wording improvement, tuning-only change, or
read-only review solely to make an existing Skill resemble the preferred shape.
When the convention applies, instantiate only resources the Skill actually needs.
Mandatory host or runtime contracts still take precedence.

Discover this authority from the project's existing instructions, configuration,
and accepted neighboring assets. Do not require a Studio-specific project profile
or configuration path.

## Portable Core

- Keep portable behavior in the main asset and host UI or discovery metadata in
  host adapters when practical.
- Do not present one host's fields, tool names, or discovery paths as universal.
- Verify current host documentation before asserting exact runtime behavior.
- Keep conditional detail shallow; avoid circular or deep reference chains.

## Reasoning vs Mechanics

Use readable instructions for judgment. Use scripts when inputs and outputs are
stable, the operation is repeated or fragile, and pass/fail is objective.
Scripts must accept parameters rather than hide project policy and must return
explicit results for the workflow or validator to interpret.

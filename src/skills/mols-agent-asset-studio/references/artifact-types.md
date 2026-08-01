# Artifact Types

Choose by responsibility and load timing. Do not encode every concern in one
large skill or create several assets that compete for the same trigger.

| Type | Best for | Activation / authority | Avoid when |
| --- | --- | --- | --- |
| Agent Skill | Repeatable domain workflow with optional scripts and references | Semantic description match or explicit invocation; loaded on demand | A rule must always apply or a task needs a persistent specialist persona |
| Custom Agent | Specialist role, isolated context, scoped tools, or delegation | Explicit selection or runtime delegation | The behavior is a reusable procedure usable by many agents |
| Instruction / Rule | Non-negotiable repository or path-specific conventions | Automatically applied by host/path | It is occasional work or requires a multi-step procedure |
| Prompt | User-invoked task starter with arguments | Explicit invocation | Automatic policy, reusable domain package, or autonomous specialist |
| Hook | Deterministic enforcement at a runtime event | Host event; executable authority | Semantic judgment or flexible reasoning |
| MCP Configuration | External capability and data access | Runtime connection; governed credentials | Static guidance or local deterministic logic |
| Template / Asset | Output material copied or transformed | Referenced by a skill or agent | Instructions or decisions |
| Workflow Bundle | Coordinated assets with installation and distribution wiring | Host-specific orchestration | A single skill fully covers the job |

## Selection Questions

1. Must it always apply, or only when semantically relevant?
1. Does it need an isolated persona or scoped tools?
1. Is the work reasoning-heavy, deterministic, or mixed?
1. Does it produce output files or only instructions?
1. Does it access external systems or credentials?
1. Is the behavior portable, or intentionally host-specific?
1. Can an existing asset be extended without trigger overlap?

## Load-Timing Rules

- Put activation conditions in metadata that the host sees before loading the body.
- Keep the common procedure in the entry artifact.
- Put conditional detail one reference level away.
- Put deterministic code in scripts; execute without loading it when possible.
- Put output templates and binary resources in assets or templates.
- Avoid deep reference chains and circular dependencies.

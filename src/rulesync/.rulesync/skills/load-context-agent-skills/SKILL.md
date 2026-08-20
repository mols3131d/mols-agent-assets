---
name: load-context-agent-skills
description: >-
  Load source-first standards and authoring context for Agent Skills. Use when creating,
  modifying, reviewing, porting, packaging, or evaluating a Skill, or when discovery
  metadata, portability, target compatibility, or Skill-authoring decisions are required.
  Do not use merely to discover, install, run, or invoke an unchanged Skill when no
  authoring or compatibility decision is needed.
---

# Contract

This Skill is an **authority router** for Agent Skill work. The active workflow owns creation, editing, validation, installation, packaging, publication, and final output.

Resolve authority from the actual source and target:

1. **Canonical source contract** — the framework that owns the authored source representation.
1. **Portable or target contract** — Agent Skills open standard when it applies, then the actual vendor/harness contract.
1. **Personal convention** — mols conventions only when personal scope is established.
1. **Skill-local contract** — requirements specific to the Skill being authored.

Do not turn target-specific creator guidance or personal conventions into portable requirements. Do not replace the active source framework's canonical representation with a target representation by assumption.

# Required Source Check

Before materially creating, modifying, porting, or reviewing a Skill, identify the actual source framework and target, then load only the applicable registry:

- Rulesync-managed source ownership and canonical representation → [Rulesync](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/tooling/rulesync.md)
- Agent Skills standard, target/harness references, and official creator sources → [Agent Skills Specification](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/skills/specification.md)

Follow the selected registry to the **current authoritative source that applies to the task**. Do not load every target guide, copy fast-changing platform behavior into this Skill, or rely on remembered target behavior when it can be checked.

# Official Target Authoring

If the selected target publishes an official `skill-creator`, read or invoke it before materially authoring or optimizing the Skill. Otherwise use that target's official Skill authoring guide. The registry owns the current links; do not duplicate them here or borrow a sibling target's creator by assumption.

# Personal Overlay — mols

Do **not** apply mols Skill conventions by default.

Apply them only when one of these is established:

- the user explicitly requests mols personal conventions or standards;
- project/repository instructions declare them;
- the target is a mols personal project or personal asset being maintained under those conventions.

When personal scope applies, load only the local convention relevant to the current source and decision:

- Rulesync-managed Skill authoring → [Skill Authoring Conventions](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/skills/skill-authoring-conventions.md)
- filesystem naming → [Agent Asset Naming Convention](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/common/naming.md)

Apply personal conventions only after mandatory source and target contracts are satisfied.

# Fallback

If current sources cannot be accessed:

- preserve the active source framework's canonical shape;
- avoid inventing target-specific metadata, paths, packaging, permissions, or creator behavior;
- do not reconstruct detailed personal conventions from memory;
- expose the verification gap when it can affect compatibility or behavior.

Prefer live authority over copied detail. The purpose of this Skill is to make the agent **look at the right source before deciding**, not to mirror those sources.

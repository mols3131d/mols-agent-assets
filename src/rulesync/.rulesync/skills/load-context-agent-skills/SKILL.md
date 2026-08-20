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

This Skill acts as an **authority router** for Agent Skill work. The active workflow owns creation, editing, validation, installation, packaging, publication, and final output.

Resolve authority from the actual source and target:

1. **Canonical source contract** — when the Skill is Rulesync-managed, current Rulesync schema and adapters own canonical representation.
1. **Portable or target contract** — Agent Skills open standard when it applies, then the actual vendor/harness contract.
1. **Personal convention** — mols conventions only when personal scope is established.
1. **Skill-local contract** — requirements specific to the Skill being authored.

Do not turn vendor-specific creator guidance or personal conventions into portable requirements. Do not force Agent Skills top-level representation onto a Rulesync canonical source; use the Rulesync target namespace instead.

# Required Source Check

Before materially creating, modifying, porting, or reviewing a Skill, read the sources that apply to the task.

When working in a Rulesync-managed source tree, use the current Rulesync schema and file-format documentation for canonical representation:

- [Rulesync](https://github.com/dyoshikawa/rulesync)
- [Rulesync file formats](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/file-formats.md)

When Agent Skills format, metadata, discovery, or portability matters, read:

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills documentation index](https://agentskills.io/llms.txt)

Use the maintained repository registry to locate current target-specific references without reproducing them here:

- [mols Agent Skills Specification and vendor registry](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/skills/agent-skills-io/agent-skills-io-specification.md)

After identifying the actual target, follow only that target's official links from the registry. Do not load every vendor guide.

# Official Vendor Authoring

If the selected target publishes an official `skill-creator`, **read or invoke it before authoring or optimizing the Skill**. If it does not, read the target's official Skill authoring guide instead. Do not borrow a sibling target's creator by assumption.

- **OpenAI** — [`skill-creator`](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md)
- **Anthropic** — [`skill-creator`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- **Google** — Gemini CLI built-in [`skill-creator`](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/skills/builtin/skill-creator/SKILL.md); for Antigravity use [Authoring Google Antigravity Skills](https://codelabs.developers.google.com/getting-started-with-antigravity-skills) unless a current Antigravity-specific official creator can be verified
- **Microsoft / GitHub** — Microsoft [`skill-creator`](https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md) for its Microsoft/Azure scope; for GitHub Copilot use [Adding agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) unless a GitHub-specific official creator can be verified

Creator guidance is target-specific authoring guidance, not the Agent Skills open standard.

# Personal Overlay — mols

Do **not** apply mols Skill conventions by default.

Apply them only when one of these is established:

- the user explicitly requests mols personal conventions or standards;
- project/repository instructions declare them;
- the target is a mols personal project or personal asset being maintained under those conventions.

When personal scope applies, read:

- [Rulesync Repository Conventions](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/common/rulesync.md)
- [Skill Authoring Conventions](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/skills/skill-authoring-conventions.md)
- [Agent Asset Naming Convention](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/common/naming.md) when filesystem naming matters

Apply personal conventions only after mandatory source and target contracts are satisfied.

# Fallback

If current sources cannot be accessed:

- preserve the active source framework's canonical shape;
- avoid inventing target-specific metadata, paths, packaging, permissions, or creator behavior;
- do not reconstruct detailed personal conventions from memory;
- expose the verification gap when it can affect compatibility or behavior.

Prefer live authority over copied detail. The purpose of this Skill is to make the agent **look at the right source before deciding**, not to mirror those sources.

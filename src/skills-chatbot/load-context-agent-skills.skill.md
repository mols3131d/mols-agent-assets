---
name: load-context-agent-skills
description: >-
  Load source-first standards and authoring context for Agent Skills. Use when creating,
  modifying, reviewing, porting, or packaging a Skill. Read the current Agent Skills
  open standard, the selected target's official Skill documentation, and any official
  vendor skill-creator before making target-specific authoring decisions. Use the mols
  repository as a maintained registry and apply its personal Skill conventions only
  when explicitly requested or when the target is clearly managed under them.
---

# Contract

Use this Skill as an **authority router** for Agent Skill work. The active workflow owns creation, editing, validation, installation, packaging, publication, and final output.

Resolve authority in this order:

1. **Portable standard** — Agent Skills open standard.
1. **Target contract** — current official documentation for the actual vendor/harness.
1. **Personal convention** — mols standards only when personal scope is established.
1. **Skill-local contract** — requirements specific to the Skill being authored.

Do not turn vendor-specific creator guidance or personal conventions into portable requirements.

# Required Source Check

Before materially creating, modifying, porting, or reviewing a Skill, read the sources that apply to the task.

Always use the current portable specification when format, metadata, discovery, or portability matters:

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

- [Personal Skill Standard](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/skills/agent-assets-skills-standard-personal.md)
- [Skill Target Profiles](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/skills/agent-assets-skills-target-profiles.md)
- [Personal Agent Asset Standard](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/references/common/standards/agent-assets-standard-personal.md)

Apply personal conventions only after the portable and mandatory target contracts are satisfied.

# Fallback

If current sources cannot be accessed:

- preserve the portable `SKILL.md` baseline with discovery metadata;
- avoid inventing target-specific metadata, paths, packaging, permissions, or creator behavior;
- do not reconstruct detailed personal conventions from memory;
- expose the verification gap when it can affect compatibility or behavior.

Prefer live authority over copied detail. The purpose of this Skill is to make the agent **look at the right source before deciding**, not to mirror those sources.

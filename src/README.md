# Agent Asset Sources (`src/`)

`src/` is the canonical source tree for distributable Agent Assets.

## `src/agentsmesh/`

`src/agentsmesh/` owns every Rule, Skill, and Agent that is represented through AgentsMesh:

```text
src/agentsmesh/
├── agentsmesh.yaml
├── agents/
├── rules/
└── skills/
```

The directory is intentionally named `agentsmesh`, not `.agentsmesh`. This repository is an asset library, so stored assets must not become repository-local runtime configuration merely because an IDE or harness discovers a conventional dot-directory.

When native AgentsMesh tooling is required, stage this tree into a temporary workspace where `rules/`, `skills/`, and `agents/` become `.agentsmesh/{rules,skills,agents}` and `agentsmesh.yaml` becomes the workspace config. Generated target projections stay temporary and are not canonical repository files.

Create other `src/` peers only for real custom/non-standard formats that AgentsMesh cannot represent. Do not recreate legacy taxonomy such as `skills-chatbot` or `skills-chatbot-runtime`.

# Agent Asset Sources (`src/`)

`src/` is the canonical source tree for distributable Agent Assets.

## `src/agentsmesh/`

`src/agentsmesh/` is an isolated native AgentsMesh workspace for every Rule, Skill, and Agent represented through AgentsMesh:

```text
src/agentsmesh/
├── agentsmesh.yaml
└── .agentsmesh/
    ├── agents/
    ├── rules/
    └── skills/
```

This preserves the native AgentsMesh layout without exposing a repository-root `.agentsmesh/` workspace. Stored distribution assets therefore do not become repository-local runtime configuration merely because an IDE or harness discovers conventional root paths.

Run read-only native commands directly from `src/agentsmesh/`. For write-producing validation such as generation, copy the workspace verbatim to a temporary directory. Generated target projections and `.lock` state are temporary artifacts, not canonical repository files.

Create other `src/` peers only for real custom/non-standard formats that AgentsMesh cannot represent. Do not recreate legacy taxonomy such as `skills-chatbot` or `skills-chatbot-runtime`.

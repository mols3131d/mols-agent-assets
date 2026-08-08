# Feature Catalog

## Asset Studio

- lifecycle modes: `inspect`, `create`, `improve`, `refactor`, `replace`,
  `review`, `validate`, `evaluate`, and `package`
- explicit source-write and execution boundaries
- responsibility-based selection of skill, agent, instruction, prompt, hook,
  MCP configuration, template, or mixed bundle
- direct operation map linking every script and template from `SKILL.md`
- fresh-context general review and risk-based adversarial review
- `Minor`, `Medium`, and `Major` change classification
- deterministic validators for:
  - Agent Skills and OpenAI skill interfaces
  - VS Code and GitHub Copilot custom agents
  - VS Code instructions, `AGENTS.md`, and prompt files
  - VS Code and GitHub hook configurations
  - GitHub repository MCP configuration
  - Studio project profiles and mixed bundle descriptors
- runtime-explicit scaffolding with YAML-safe scalar quoting
- strict skill packaging with SHA-256 manifest, symlink rejection, secret-like
  filename exclusion, and likely plaintext-secret scanning
- mixed asset bundle packaging with install map, per-asset runtime profile,
  collision detection, and source-boundary checks
- repository asset inventory, lexical overlap triage, and context-budget audit
- project-profile discovery with explicit precedence and no hidden merge
- balanced trigger-evaluation suites and candidate-versus-baseline grading
- truthful `Deferred` result until runtime observations are complete

## Asset Tuner

- quarantine and static inspection of imported assets or documents
- provenance, revision, license, trust-tier, and hash recording
- source behavioral-contract extraction
- bounded project profiling through the Studio discovery contract
- `Keep / Adapt / Replace / Drop / Defer` adaptation matrix
- conflict resolution between source behavior and project authority
- portable-core and runtime-adapter separation
- general and adversarial tuning reviews
- tuned-candidate versus source-contract and project-acceptance evaluation

## Implemented Quality Evidence

- 27 deterministic regression tests
- 24 balanced Studio trigger cases
- 22 balanced Tuner trigger cases
- failure probes for invalid agents, invalid MCP, unknown skill metadata, and
  likely plaintext secrets
- archive integrity tests for individual skills and mixed bundles
- evidence-backed closure report for independent findings F-001 through F-008

## Deliberately Excluded

- automatic marketplace or repository publication
- implicit execution of imported scripts, hooks, or MCP servers
- credential storage or secret-management replacement
- hidden memory or self-modifying production assets
- mandatory telemetry or token-cost collection
- claims of runtime activation quality before actual runtime execution
- a CSV router for a small, fixed operation set

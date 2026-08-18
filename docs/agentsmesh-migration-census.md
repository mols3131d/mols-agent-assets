# Project EXODUS — Phase 0 Census

> **Status:** Baseline complete  
> **Gate:** READY WITH LIMITS  
> **Snapshot:** `e981c08e126ef34e6b40dace1f9100efd5060911`  
> **Branch:** `agent/refactor/agentsmesh-migration`  
> **Mutation policy:** Phase 0 records the current state only. No canonical Agent Asset has moved yet.

## 결론

Phase 0 결과, AgentsMesh 대이주는 **착수 가능**하다.

다만 현재 저장소는 `src/`라는 하나의 source workspace 안에 portable coding-harness assets, hosted-chatbot assets, target-specific agents, repository tooling이 함께 존재한다. 따라서 directory 단위 일괄 이동은 금지하고 **asset별 authority 판정**으로 이주한다.

가장 중요한 발견은 다음과 같다.

1. 일반 portable Skill은 12개이며, 그중 `rulesync-agent-assets`는 이주 대상이 아니라 최종적으로 retire/replace할 dependency다.
2. `src/rules/`의 두 Rule도 성격이 다르다. `language-ko`는 portable 후보지만 `chatbot-repo-skill-routing`은 hosted chatbot 전용이다.
3. custom Agent 3개는 VS Code 전용 front matter를 사용하며 AgentsMesh canonical Agent schema와 직접 일치하지 않는다.
4. GitHub Copilot과 Antigravity는 현재 가장 우선적인 coding-harness target이지만 capability parity가 없다. 특히 Antigravity는 project scope에서 Agents와 MCP를 지원하지 않는다.
5. `src/skills/**` 경로가 CI, index generator, docs와 tests에 직접 박혀 있으므로 source 이동 전에 repository tooling을 함께 바꿔야 한다.
6. root shared `/evals`는 아직 없지만 `mols-agent-asset-validator`에는 package-local trigger/behavior/adversarial eval corpus가 이미 있다. 이것은 이동하지 않는다.
7. `tests/skills/`와 `pyproject.toml`에는 이미 사라진 Skill을 가리키는 legacy verification debt가 있다.

따라서 EXODUS는 **portable Rules/Skills부터 시작하고, Agents와 hosted chatbot profiles는 별도 경계로 취급**한다.

---

# 1. Asset Inventory

## Summary

| Surface | Count | Current authority | Initial action |
| --- | ---: | --- | --- |
| Portable Rules | 2 | `src/rules/` | asset별 move / keep |
| Custom Agents | 3 | `src/agents/` | adapt / hold |
| Portable Skills | 12 | `src/skills/` | 11 move candidates + 1 retire |
| Prompts | 1 | `src/prompts/` | keep |
| Flat chatbot Skills | 18 | `src/skills-chatbot/` | keep |
| Runtime chatbot Skills | 5 | `src/skills-chatbot-runtime/` | keep |
| Runtime instruction surface | 1 | `.agents/AGENTS.md` | generated/exception 판정 |
| Root Skill test scopes | 5 | `tests/skills/` | 3 current + 2 orphan |
| Repository scripts | 4 | `scripts/` | keep; index script requires migration |

Counts describe top-level assets or test scopes, not every supporting file.

## Portable Skills

| Skill | Root test scope | Migration action | Notes |
| --- | --- | --- | --- |
| `caveman-ko` | none observed | **move candidate** | portable Skill |
| `clarify-code` | none observed | **move candidate** | portable Skill |
| `mols-agent-asset-studio` | yes | **move candidate** | root tests and internal path assumptions must follow |
| `mols-documents-studio` | none observed | **move candidate** | portable Skill |
| `mols-markdown-dashboard` | none observed | **move candidate** | portable Skill |
| `mols-markdown-for-human` | none observed | **move candidate** | portable Skill |
| `mols-markdown-scripts` | yes | **move candidate** | `pyproject.toml` also references its scripts path |
| `mols-mermaid-chart` | none observed | **move candidate** | portable Skill |
| `mols-mermaid-diagram` | none observed | **move candidate** | portable Skill |
| `mols-rule-dry` | none observed | **move candidate** | portable Skill |
| `rulesync-agent-assets` | yes | **retire/replace** | keep only until AgentsMesh cutover no longer needs Rulesync routing |
| `vcs-git-commit` | none observed | **move candidate** | portable Skill |

`rulesync-agent-assets` is deliberately not migrated as if it were an ordinary long-lived Skill. Its responsibility is superseded by direct AgentsMesh use if EXODUS succeeds.

## Rules

| Rule | Current role | AgentsMesh fit | Action |
| --- | --- | --- | --- |
| `language-ko` | language preference | high | **move candidate**; root/additional placement decided during Rule cutover |
| `chatbot-repo-skill-routing` | hosted chatbot Skill-index routing | low | **keep outside AgentsMesh**; update index paths when portable Skills move |

This invalidates a naive `src/rules/* → .agentsmesh/rules/*` bulk move.

`chatbot-repo-skill-routing` points directly at the three repository Skill indexes, including `src/skills/INDEX.jsonl`. That path becomes a migration dependency when the portable Skill index moves.

## Agents

| Agent | Current target | Main incompatibility | Action |
| --- | --- | --- | --- |
| `review-quality` | `vscode` | target-specific tool identifiers, `target`, `user-invocable`, `agents` fields | **adapt** |
| `review-adversarial` | `vscode` | `target`, `user-invocable`, `agents` fields | **adapt** |
| `review-lead` | `vscode` | delegates through `agents: [review-quality, review-adversarial]`; field is not part of current AgentsMesh canonical Agent front matter | **hold/adapt** |

The Agent bodies are portable in intent, but the front matter is not a mechanical rename.

`review-lead` has the highest semantic migration risk because orchestration/delegation is part of its contract. Do not cut it over until an AgentsMesh-native or bounded target-specific representation preserves that delegation behavior.

## Prompts and hosted chatbot profiles

`src/prompts/chatgpt-sync-chatbot-skills.prompt.md` is explicitly ChatGPT-specific orchestration and remains outside AgentsMesh commands unless a future command mapping proves semantically appropriate.

The repository-local Skill profiles remain separate:

- `src/skills-chatbot/` — 18 flat hosted-chatbot Skills.
- `src/skills-chatbot-runtime/` — 5 runtime/bundled hosted-chatbot Skills.

These profiles are not initial EXODUS migration targets.

---

# 2. Authority Map

## Current authority

```text
Portable Skill source        = src/skills/
Rule source                   = src/rules/
Custom Agent source           = src/agents/
Hosted chatbot Skill source   = src/skills-chatbot/
Runtime chatbot Skill source  = src/skills-chatbot-runtime/
Prompt source                 = src/prompts/
Repository runtime rules      = root AGENTS.md + .agents/AGENTS.md guard
Derived Skill indexes         = */INDEX.jsonl
```

The root `AGENTS.md` currently declares `src/` as the authoring source workspace and `tests/` as repository-level verification. That authority remains in force until the Coronation phase.

`.agents/AGENTS.md` currently contains only a guard telling agents not to edit the directory and to refer to `../AGENTS.md`. It is not a canonical asset source.

## Rule projection authority debt

`docs/references/rules/agent-assets-rules-projections.md` currently delegates source resolution and fan-out to `rulesync-agent-assets`.

It also points to `agent-assets-rules-canonical-superset.md` as the source authority document, but that referenced file is currently empty.

EXODUS therefore replaces an already-incomplete Rulesync projection authority rather than displacing a fully implemented canonical layer.

## Target authority after cutover

For AgentsMesh-managed assets only:

```text
.agentsmesh/                  = canonical source
agentsmesh.yaml               = target/features selection
harness-native files          = committed generated artifacts
INDEX.jsonl                   = derived discovery metadata
```

Hosted chatbot profiles, package-local evals and repository tooling retain their own authority.

---

# 3. Active Target Set

The target set is intentionally small. Supporting every AgentsMesh target is not an objective.

## Provisional tiers

| Tier | Target | Policy |
| --- | --- | --- |
| A | GitHub Copilot | mandatory project-scope cutover target |
| A | Antigravity | mandatory project-scope cutover target |
| B | Codex CLI | generate/verify when promoted or actively used |
| B | Claude Code | generate/verify when promoted or actively used |
| B | Gemini CLI | generate/verify when promoted or actively used |
| Outside AgentsMesh | hosted ChatGPT | remains chatbot-specific repository profile |

Tier assignment is provisional until Phase 1 confirms the actually available local runtimes and the pinned AgentsMesh version.

## Target × Capability Matrix

Current AgentsMesh project-scope support:

| Feature | GitHub Copilot | Antigravity | Codex CLI | Claude Code | Gemini CLI |
| --- | --- | --- | --- | --- | --- |
| Rules | Native | Native | Native | Native | Native |
| Additional Rules | Native | Native | Native | Native | Embedded |
| Commands | Native | Native (workflows) | Embedded | Native | Native |
| Agents | Native | **None** | Native | Native | Native |
| Skills | Native | Native | Native | Native | Native |
| MCP | Native | **None** | Native | Native | Native |
| Hooks | Native | Native | Native | Native | Native |
| Ignore | **None** | **None** | **None** | Native | Native (settings-embedded) |
| Permissions | **None** | Partial | Native | Native | Partial |

### Immediate consequences

- **Rules and Skills are the safest first migration families.** They are Native across all five provisional coding targets.
- **Agents cannot have one uniform Tier A contract** because Antigravity has no project-scope Agent support.
- **MCP cannot be a Tier A invariant** while Antigravity remains Tier A.
- Ignore and Permissions must remain target-capability-aware rather than being treated as universal canonical guarantees.
- `partial` and `embedded` are evidence classes, not synonyms for full parity.

---

# 4. Projection Map

## Current projection responsibilities to retire or reduce

The repository currently owns or documents:

- root/nested `AGENTS.md` directory rules;
- harness-specific glob selector projections;
- repository-local `CHATBOT.md → AGENTS.md → README.md` chatbot fallback;
- Rulesync source resolution and fan-out;
- Skill index paths tied to `src/skills/`;
- target-specific VS Code Agent front matter.

After migration:

- AgentsMesh owns coding-harness representation and generation where supported;
- hosted chatbot fallback remains repository-local because it is outside AgentsMesh's coding-target scope;
- target-specific Agent exceptions remain explicit rather than being hidden behind false portability.

---

# 5. Validation Map

## Local gates

Current Lefthook policy:

```text
pre-commit
├── rumdl fmt/check --fix for Markdown
└── ruff check/format for Python

commit-msg
└── conventional commit validator

pre-push
└── uv run pytest
```

These remain repository-owned.

AgentsMesh checks will be added alongside them, not wrapped in a new repository compiler.

## GitHub Actions

### `targeted-tests.yml`

Current paths and test selection are coupled to:

```text
src/skills/**
tests/skills/**
src/scripts/**
tests/scripts/**
```

The workflow constructs Skill paths as `src/skills/$name`.

**Migration requirement:** before portable Skills cut over, changed-file selection must recognize `.agentsmesh/skills/<name>/` and preserve existing root/colocated test routing.

### `skill-indexes.yml`

Current workflow watches:

```text
src/skills/*/SKILL.md
src/skills-chatbot/*.skill.md
src/skills-chatbot-runtime/*/SKILL.md
```

and commits indexes under all three `src/...` profiles.

**Migration requirement:** portable Skill index generation must read `.agentsmesh/skills/*/SKILL.md` after cutover while leaving the two hosted chatbot indexes under their existing profiles.

### `generate_skill_indexes.py`

The generator hardcodes:

```text
ROOT / "src/skills"
ROOT / "src/skills-chatbot"
ROOT / "src/skills-chatbot-runtime"
```

The first target and its `workspace_path`/GitHub URL template must change with portable Skill authority.

## Python configuration

`pyproject.toml` currently includes Python paths for:

```text
src/skills/iceberg-code-report/scripts
src/skills/iceberg-code-review/scripts
src/skills/mols-markdown-scripts/scripts
```

The first two source directories no longer exist. This is pre-existing verification debt and should not be carried into the new authority model.

`mols-markdown-scripts` must have its path updated if its canonical package moves to `.agentsmesh/skills/`.

## Orphan test scopes

`tests/skills/` currently includes:

```text
iceberg-code-review/
mols-agent-asset-studio/
mols-kanban-markdown/
mols-markdown-scripts/
rulesync-agent-assets/
```

`src/skills/iceberg-code-review` and `src/skills/mols-kanban-markdown` do not exist at the snapshot ref.

Phase 1/2 must classify these as delete, recover or archive. They must not silently survive as fake migration coverage.

`rulesync-agent-assets` tests remain useful only while that Skill remains in the migration path; they are retired with the Skill.

---

# 6. Eval Baseline Map

## Existing evidence

There is no root `/evals` shared corpus yet.

`src/skills-chatbot-runtime/mols-agent-asset-validator/evals/` already contains package-local:

```text
trigger-evals.json
behavior-evals.json
adversarial-evals.json
```

These remain package-owned and are **not moved merely for topology uniformity**.

## Required pre-cutover shared baseline

Before the first portable Skill/Rule authority cutover, create only the smallest shared corpus that protects migration semantics:

```text
evals/
├── routing/
└── regression/
```

Initial priority:

1. Skill routing descriptions that are relied on by repository-wide discovery.
2. Rule activation/scope that changes when converted to AgentsMesh front matter.
3. Known failure cases discovered during normalization/import.
4. Critical Agent behavior only when that Agent reaches its own migration phase.

Behavioral and adversarial suites expand only where deterministic checks cannot protect the contract.

---

# 7. Migration Classification

## Move first

These have the cleanest AgentsMesh fit:

```text
src/rules/language-ko.md
src/skills/<portable Skill except rulesync-agent-assets>/
```

The actual order remains Rules first, then Skills.

## Adapt before move

```text
src/agents/review-quality.agent.md
src/agents/review-adversarial.agent.md
src/agents/review-lead.agent.md
```

Required adaptations include tool vocabulary, target scoping and invocability/delegation semantics.

## Keep outside AgentsMesh

```text
src/rules/chatbot-repo-skill-routing.md
src/prompts/chatgpt-sync-chatbot-skills.prompt.md
src/skills-chatbot/
src/skills-chatbot-runtime/
package-local evals/
repository scripts/tests/docs
```

## Retire after replacement

```text
src/skills/rulesync-agent-assets/
tests/skills/rulesync-agent-assets/
Rulesync-specific references and projection ownership
```

## Resolve legacy debt

```text
tests/skills/iceberg-code-review/
tests/skills/mols-kanban-markdown/
pyproject.toml iceberg-code-* pythonpath entries
empty docs/references/rules/agent-assets-rules-canonical-superset.md
```

---

# 8. Preservation Contract

The following invariants must survive EXODUS unless a later phase explicitly changes them.

## Repository authority

- root repository instructions must keep their effective responsibilities until explicitly transferred;
- branch/PR/test conventions must not disappear because a generated root file overwrites them;
- `.agents/AGENTS.md` guard behavior must either remain or have an explicit replacement.

## Skills

- `name` and routing-critical `description`;
- activation and negative boundaries;
- runtime supporting files;
- internal relative links;
- scripts/assets/references required for behavior;
- package-local tests/evals where they belong;
- derived index discoverability after path change.

AgentsMesh supporting-file references require target-compatible relative paths. Skill packages with internal links must be checked during migration rather than bulk-copied blindly.

## Rules

- always-on vs scoped intent;
- globs;
- target scoping;
- root instruction precedence;
- hosted chatbot fallback remains outside the coding-harness projection contract.

## Agents

- role and authority;
- allowed/forbidden mutation behavior;
- tool restrictions;
- user invocability;
- delegation graph;
- review independence between quality and adversarial reviewers.

`review-lead` is not considered migrated if it merely preserves prose while losing the ability to coordinate the two reviewers.

## Verification

- `uv run pytest` remains the repository correctness gate until deliberately replaced;
- targeted test selection must continue to select the affected Skill tests after path migration;
- generated indexes remain derived, deterministic metadata;
- package-local eval authority is preserved.

---

# 9. Risks and Blockers

## P1 — Agent canonical mismatch

Current custom Agent front matter contains repository/vendor-specific fields that are not direct AgentsMesh canonical fields.

**Action:** do not move Agents in the first crossing. Build an explicit field/behavior mapping first.

## P1 — Antigravity capability gap

Antigravity project mode currently has no Agents or MCP support in the AgentsMesh matrix.

**Action:** Tier A cutover must be feature-scoped. Rules/Skills can pass while Agents/MCP remain unsupported for Antigravity.

## P1 — Path-coupled CI and index generation

Moving `src/skills/` without first updating CI/index tooling would silently reduce verification and break discovery.

**Action:** treat workflow/generator updates as part of the Skill cutover batch.

## P2 — Rule source is mixed

`src/rules/` contains both portable coding-harness intent and hosted-chatbot-only routing.

**Action:** migrate by asset, not folder.

## P2 — Rulesync authority debt

Rule projection documentation still names Rulesync as the fan-out owner and references an empty canonical-superset document.

**Action:** replace this authority only when AgentsMesh Rule cutover is proven; do not maintain both.

## P2 — Legacy tests/config

Orphan Skill tests and stale `pyproject.toml` paths create false confidence and maintenance noise.

**Action:** resolve before declaring the new verification model clean.

## P2 — Toolchain pin not yet established

The repository is currently Python-oriented and has no established AgentsMesh package pin in this snapshot.

**Action:** Phase 1 must select one exact-version installation strategy without introducing an unnecessary wrapper framework.

---

# 10. Phase 0 Gate

| Gate | Result | Evidence / limitation |
| --- | --- | --- |
| Asset Inventory | **PASS** | primary source families and counts inventoried |
| Authority Map | **PASS** | portable, hosted, runtime and derived surfaces separated |
| Active Target Set | **PASS WITH LIMITS** | Tier A/B provisional until local runtime confirmation |
| Target × Capability | **PASS** | project-scope matrix recorded; major gaps explicit |
| Projection Map | **PASS** | existing Rulesync/repository projection responsibilities identified |
| Validation Map | **PASS** | local hooks, CI, indexes, tests and path coupling identified |
| Baseline Eval Map | **PASS** | package-local evals found; shared pre-cutover need defined |
| Preservation Contract | **PASS** | repository/Skill/Rule/Agent/verification invariants recorded |
| Source Mutation | **PASS** | no canonical asset moved during Phase 0 |

**Phase 0 result: READY WITH LIMITS.**

The limits are known migration work, not blockers to Phase 1.

---

# 11. Phase 1 Work Order

`Raise the New Capital` begins with the following order:

1. Verify and pin the exact AgentsMesh version and installation method.
2. Add `agentsmesh.yaml` with only the provisional Tier A targets and the minimum initial features.
3. Create `.agentsmesh/rules/_root.md` as a non-authoritative staging source; do not cut root authority yet.
4. Import or manually map the first Rule candidates.
5. Run `agentsmesh lint`, `generate`, `diff`, `check`, and `generate --check` against the pinned version.
6. Record normalization differences.
7. Establish the minimal shared pre-cutover routing/regression corpus before any source deletion.
8. Only after those gates pass, begin `The First Crossing` for Rules.

Initial features should stay deliberately narrow. `rules` and `skills` have the strongest cross-target support. Agent/MCP/permission complexity is deferred until its own evidence exists.

---

# References

Repository evidence:

- `AGENTS.md`
- `README.md`
- `src/rules/`
- `src/agents/`
- `src/skills/INDEX.jsonl`
- `src/skills-chatbot/INDEX.jsonl`
- `src/skills-chatbot-runtime/INDEX.jsonl`
- `src/prompts/`
- `scripts/generate_skill_indexes.py`
- `.github/workflows/skill-indexes.yml`
- `.github/workflows/targeted-tests.yml`
- `lefthook.yml`
- `pyproject.toml`
- `docs/testing.md`
- `docs/references/rules/agent-assets-rules-projections.md`
- `docs/references/skills/agent-assets-skills-target-profiles.md`

External evidence:

- AgentsMesh canonical configuration: <https://samplexbro.github.io/agentsmesh/canonical-config/>
- AgentsMesh Agents: <https://samplexbro.github.io/agentsmesh/canonical-config/agents/>
- AgentsMesh supported tools matrix: <https://samplexbro.github.io/agentsmesh/reference/supported-tools/>
- AgentsMesh existing-project adoption: <https://samplexbro.github.io/agentsmesh/guides/existing-project/>

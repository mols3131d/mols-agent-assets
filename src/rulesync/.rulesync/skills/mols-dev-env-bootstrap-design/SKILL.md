---
name: mols-dev-env-bootstrap-design
description: >-
  Design or review a developer-environment bootstrap that supports first-time
  setup, repeatable day-to-day repair, and explicitly requested updates within
  predeclared version constraints. Use for toolchain provisioning boundaries,
  dependency locks, missing-tool handling, installation side effects, partial
  failures, recovery and verification. Do not use for ordinary dependency
  upgrades, a one-off installation command, or CI-only pipeline design.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Developer Environment Bootstrap Design

Design a bootstrap that can be used both on a new machine and throughout development without unexpectedly changing the host or broadening dependency versions. Prefer existing native package managers and task runners over a custom bootstrap framework.

## Design Contract

- **Separate intents.** Setup reconciles the environment to the declared, reproducible state; update explicitly resolves newer allowed versions and records the result. Repeating setup must not perform an implicit upgrade. Checks observe readiness without mutating version policy.
- **Separate policy from resolution.** The repository's chosen configuration declares allowed versions, channels or revisions and their owners. Lockfiles or equivalent resolution state record concrete selections. Scripts execute this policy rather than expanding constraints or embedding a second version policy.
- **Separate scopes.** Identify host prerequisites, tool-manager-managed binaries, project-isolated dependencies, project-local integration, and user/global state. A tool being missing does not itself authorize a host or user-global installation. Tool-manager caches may be user-shared too; treat them as a distinct, explicit permission decision.
- **Keep partial progress truthful.** Continue independent work when a prerequisite is missing, but skip dependent steps; never report partial readiness as complete. Make every blocked step and its recovery action visible.
- **Protect existing state.** Inspect dirty or user-owned files and install destinations before writes. Avoid destructive cleanup, overwrite of customized hooks/configurations, privilege escalation, global installer commands or unreviewed upstream scripts by default.
- **Portable core, local decisions.** Match the existing operating systems, shells, tool managers, locks, installer capabilities and organizational policy. Do not require mise, uv, a particular CI provider, a universal CLI shape or a new configuration schema.

## Procedure

1. **Inspect the current environment contract.** Identify the requested lifecycle, supported platforms, repository setup commands, declared tool versions, dependency manifests, existing lockfiles, native update commands, install destinations and verification paths. Separate observed behavior from desired behavior; check changing vendor semantics at the actual installed version when it matters.
2. **Assign owners.** For every managed item, identify who declares the permitted version set, who selects the concrete version, who installs it, and who verifies it. Distinguish exact pins, bounded ranges, floating branch refs and unbounded latest requests. A movable ref without an explicit update policy is not automatically eligible for upgrade.
3. **Design two paths.** Setup reuses locked results, installs missing *authorized* dependencies and safely reapplies project integration. Update is explicit: resolve the latest admissible version using the native resolver, inspect resulting lockfile diffs, install and verify. Do not silently broaden the allowed range or auto-commit changes. If the native manager cannot reproduce a locked state, surface the limitation and propose the least invasive fix.
4. **Decide missing-tool behavior by impact.** For each dependency, classify it as required or optional and installation as project-scoped, manager-controlled, user-shared or system-wide. Automatically install only within the declared authority and understood side-effect boundary; tool-manager ownership alone is not blanket consent. Missing entrypoint prerequisites cannot be repaired *from inside* that entrypoint: provide a short manual preflight and official installation instructions. For unapproved host or user-global changes, skip and report rather than invoking sudo, system package managers, global npm/pip or remote shell installers.
5. **Define execution and recovery.** Build the smallest prerequisite graph necessary to prevent invalid dependent execution; do not fail unrelated tasks because another optional component is absent. Specify preflight, resolve, apply, verify and summary. Distinguish missing prerequisite, unavailable network, version-constraint conflict, installer failure and verification failure. Prefer safe retries and incremental reconciliation over wiping state or an unproven rollback.
6. **Prepare the handoff.** State the entrypoints, affected manifests/locks, installation permissions, failure/exit semantics and test scenarios. Reuse existing scripts and native task mechanisms; add a wrapper only when orchestration or reporting cannot reasonably be expressed there.

## Decision Checks

Before accepting a design, challenge these cases:

- Fresh environment: the entrypoint or Git/shell does not exist; its absence must not trigger an unsafe self-installer.
- Re-run: no unsolicited version resolution, lockfile rewrite, removal of user state or repeated harmful side effect.
- Update: newer releases are available both inside and outside the declared range; only admissible versions are selected, and changed locks are reviewable.
- Partial failure: a required tool is missing while unrelated optional work can proceed; dependent work is skipped, output and exit status reflect remaining blockers.
- Installer boundary: an upstream or user-level installer changes more than project-local state; opt-in or a safer alternative is required.
- CI and multi-platform usage: verification is distinct from provisioning; a local setup success does not prove a CI or another OS works.

## Handoff

Produce a concise, target-specific design with: **current state and unknowns; lifecycle entrypoints; policy/resolution/installation owners; per-tool permission and missing-tool decision; failure and recovery behavior; smallest implementation changes; verification plan**. Mark each relevant behavior as existing, proposed, or unverified. Stop at a design-ready handoff unless implementation was explicitly requested.

Do not duplicate exact tool commands, flags, version syntax or platform installation instructions when their authoritative vendor documentation already governs them. Validate the relevant current contract before recommending a concrete invocation.

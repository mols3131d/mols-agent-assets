---
name: mols-dev-env-bootstrap-design
description: >-
  Use only when the requested outcome is a design, review, or implementation
  handoff for a developer-environment bootstrap lifecycle: first-time setup,
  repeatable repair, or explicit updates within predeclared constraints.
  Within that lifecycle, assess provisioning authority, locks, missing tools,
  installer side effects, partial failures, recovery, and verification.
  Do not select for executing an ordinary package upgrade, installing one tool,
  explaining a single command, or designing a CI-only pipeline; shared words
  such as setup, lock, install, and update do not make those tasks applicable.
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

Design a bootstrap that can be used both on a new machine and throughout development without unexpectedly changing the host or broadening dependency versions. This Skill owns design, review, and implementation handoff—not implementation or provisioning execution. Ordinary engineering capability and the target project's governing instructions own implementation when separately requested. Prefer existing native package managers and task runners over a custom bootstrap framework.

## Design Contract

- **Separate intents.** Setup reconciles the environment to the declared, reproducible state; update explicitly resolves newer allowed versions and records the result. Repeating setup must not perform an implicit upgrade. Checks observe readiness without mutating version policy.
- **Separate policy from resolution.** The repository's chosen configuration declares allowed versions, channels or revisions and their owners. Lockfiles or equivalent resolution state record concrete selections. Scripts execute this policy rather than expanding constraints or embedding a second version policy.
- **Separate scopes.** Identify host prerequisites, tool-manager-managed binaries, project-isolated dependencies, project-local integration, and user/global state. A tool being missing does not itself authorize a host or user-global installation. Tool-manager caches may be user-shared too; treat them as a distinct, explicit permission decision.
- **Design for explicit installation consent.** The target project's development-environment setup document or equivalent local policy owns whether, what, and where to install. Before an agent executes provisioning, require the user's informed approval for the installation scope, including manager-managed shared storage; a design or implementation request alone is not approval. Batch a clearly scoped installation decision rather than prompting for every tool, but obtain new approval when the impact changes. Do not make global-tool reuse the default: select the project's environment and isolation contract first, then reuse resources already compatible with that contract.
- **Distinguish runtimes from dependencies.** Classify host executables, language interpreters, project environments, and project-installed packages separately. An existing language runtime may be usable as the basis for a project-isolated environment, but global packages and globally installed project development tools must not silently replace the project's locked dependencies. Preserve native environment isolation; do not sync into user/system package environments.
- **Keep partial progress truthful.** Continue independent work when a prerequisite is missing, but skip dependent steps; never report partial readiness as complete. Make every blocked step and its recovery action visible.
- **Protect existing state.** Inspect dirty or user-owned files and install destinations before writes. Avoid destructive cleanup, overwrite of customized hooks/configurations, privilege escalation, global installer commands or unreviewed upstream scripts by default.
- **Portable core, local decisions.** Match the existing operating systems, shells, tool managers, locks, installer capabilities and organizational policy. Do not require mise, uv, a particular CI provider, a universal CLI shape or a new configuration schema.

## Procedure

1. **Inspect the current environment contract.** Identify the requested lifecycle, supported platforms, repository setup commands, declared tool versions, dependency manifests, existing lockfiles, native update commands, install destinations and verification paths. Separate observed behavior from desired behavior; check changing vendor semantics at the actual installed version when it matters.
1. **Assign owners.** For every managed item, identify who declares the permitted version set, who selects the concrete version, who installs it, and who verifies it. Distinguish exact pins, bounded ranges, floating branch refs and unbounded latest requests. A movable ref without an explicit update policy is not automatically eligible for upgrade.
1. **Design two paths.** Setup reuses locked results, installs missing *authorized* dependencies and safely reapplies project integration. Update is explicit: resolve the latest admissible version using the native resolver, inspect resulting lockfile diffs, install and verify. Do not silently broaden the allowed range or auto-commit changes. If the native manager cannot reproduce a locked state, surface the limitation and propose the least invasive fix.
1. **Decide missing-tool behavior by impact.** First establish each item's native owner and required isolation level, then check whether that owner can reuse an existing installation, interpreter, project environment, or cache without violating lock, provenance, or isolation requirements. For each dependency, classify it as required or optional and installation as project-scoped, manager-controlled, user-shared or system-wide. Specify the user's pre-installation approval point and impact summary in the design; tool-manager ownership alone is not blanket consent. Missing entrypoint prerequisites cannot be repaired *from inside* that entrypoint: provide a short manual preflight and official installation instructions. For unapproved host or user-global changes, skip and report rather than invoking sudo, system package managers, global npm/pip or remote shell installers.
1. **Define execution and recovery.** Build the smallest prerequisite graph necessary to prevent invalid dependent execution; do not fail unrelated tasks because another optional component is absent. Specify preflight, resolve, apply, verify and summary. Distinguish missing prerequisite, unavailable network, version-constraint conflict, installer failure and verification failure. Prefer safe retries and incremental reconciliation over wiping state or an unproven rollback.
1. **Prepare the handoff.** State the entrypoints, affected manifests/locks, installation permissions, failure/exit semantics and test scenarios. Reuse existing scripts and native task mechanisms; add a wrapper only when orchestration or reporting cannot reasonably be expressed there.

## Decision Checks

Before accepting a design, challenge these cases:

- Fresh environment: the entrypoint or Git/shell does not exist; its absence must not trigger an unsafe self-installer.
- Re-run: no unsolicited version resolution, lockfile rewrite, removal of user state or repeated harmful side effect.
- Update: newer releases are available both inside and outside the declared range; only admissible versions are selected, and changed locks are reviewable.
- Partial failure: a required tool is missing while unrelated optional work can proceed; dependent work is skipped, output and exit status reflect remaining blockers.
- Environment boundary: an existing compatible interpreter must not imply reuse of global site-packages or replace an isolated project dependency environment; verify project environment targets before any sync.
- Installer boundary: installing even into tool-manager shared storage requires informed user approval before agent execution; existing managed resources are reused only where the project's ownership and isolation policy permits. An upstream or user-level installer changing more than project-local state needs its own scope decision.
- CI and multi-platform usage: verification is distinct from provisioning; a local setup success does not prove a CI or another OS works.

## Handoff

Produce a concise, target-specific design with: **current state and unknowns; lifecycle entrypoints; policy/resolution/installation owners; environment ownership/isolation, eligible reuse, and user-consent boundary; failure and recovery behavior; smallest implementation changes; verification plan**. Mark each relevant behavior as existing, proposed, or unverified. Stop at a design-ready handoff. When the user separately requests implementation, hand the design to the caller's ordinary engineering workflow; this Skill itself does not authorize or orchestrate installation.

Do not duplicate exact tool commands, flags, version syntax or platform installation instructions when their authoritative vendor documentation already governs them. Validate the relevant current contract before recommending a concrete invocation.

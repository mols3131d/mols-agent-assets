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

Design or review developer-environment setup, repair, or bounded update. This Skill owns design and, when requested, implementation handoff—not implementation, installation, or host changes. Separate implementation requests belong to the project's normal engineering workflow.

## Principles

- **Scope to the request.** Inspect only affected tools, direct prerequisites, platforms, and lifecycle stages. Stop when further investigation will not change the decision. Do not turn a narrow review into a full bootstrap redesign.
- **Keep native owners.** The project's development-environment document or equivalent policy governs installation scope; manifests and locks declare allowed and resolved versions. Use existing tools' defaults, CLI/API, and native tasks instead of recreating their version resolution, installation, cache handling, or verification.
- **Separate setup and update.** Setup reconciles to the declared or locked state without implicit upgrades or lock rewrites. Only an explicit update may resolve newer versions within existing constraints through the native owner; review lock changes without auto-committing. Do not move exact pins or floating refs without an approved update policy.
- **Respect isolation.** Reuse existing host tools, interpreters, user/global settings, and caches when compatible with the project's version, provenance, and isolation contract. Global packages must not silently replace declared project dependencies; keep project-isolated packages out of user/system environments. Shared cache writes require user-scoped approval.
- **Avoid configuration growth.** Use native defaults, project documentation/configuration, and compatible existing user/global settings instead of duplicating them. Introduce variables, flags, modes, or wrappers only for a demonstrated gap. If an inherited setting conflicts with a lock, environment target, or isolation, preserve global state and use a safe project-scoped solution or report the blocker; do not persistently rewrite PATH or shell profiles.
- **Propose, do not automate, risky changes.** Design approval is not installation permission. For privileged commands, deletion, unreviewed scripts, HOME/hook/global writes, or uncertain effects, describe the risk and propose a safer native/manual path; leave the risky step out of automatic setup. Any agent-executed installation (including project environments or shared manager storage) needs informed approval of its scope and effects, renewed if scope changes. Approval does not override project or platform safety constraints.
- **Preserve state and report honestly.** Protect dirty locks, user files, shared hooks, and existing environments. Do not force-reset, overwrite, or claim rollback without proof. Skip dependent steps when blocked, continue independent safe work, and never report partial readiness as full success.

## Procedure

1. **Bound and inspect.** Identify the requested outcome, relevant project docs/manifests/locks, native defaults, and existing global settings only where they affect it. Distinguish observed facts from proposals; check version-specific semantics only when consequential.
2. **Design the requested path.** For setup, reconcile to declared/locked state and allow safe reruns; for update, preserve bounds and review resolved changes. Detail both only if requested. Reuse native CLI/API/tasks; propose minimal glue only for a demonstrated gap, never a parallel installer or resolver. If the entrypoint is missing, suggest manual preflight rather than a self-installer.
3. **Check relevant risk.** Identify writes, ownership, approval, isolation, and recovery only for affected steps. If effects are unsafe or unknown, report the blocked step and safer option; do not invent a flag or installer to bypass it.
4. **Review proportionately.** Challenge only applicable failure paths: first run, rerun, bounded update, partial failure, environment/installer boundary, or claimed platform support. Distinguish design assumptions and static checks from actual host/runtime evidence.

## Result

For a **review**, return findings, evidence, risks, and the smallest corrective action; no unsolicited implementation plan. For a **design**, give only the affected entrypoints, ownership/permissions, behavior, recovery, and verification needed to implement it. Prepare a fuller implementation handoff only when requested. Mark important behavior as existing, proposed, or unverified and stop at the requested outcome.

Do not duplicate vendor commands or platform instructions without need; confirm the applicable native contract before suggesting a specific invocation.

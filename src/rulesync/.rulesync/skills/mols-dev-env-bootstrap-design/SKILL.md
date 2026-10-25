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
- **Keep native owners.** The project's development-environment policy governs installations; existing manifests declare allowed versions, locks record resolved versions, and native managers resolve/install/verify. Do not invent a second policy or custom framework.
- **Separate setup and update.** Setup safely reconciles to locked state without implicit upgrades or lock rewrites. Update, only when explicitly requested, resolves newer versions within existing constraints through the native owner and leaves reviewable lock changes. Exact pins and floating refs without an approved update policy do not move.
- **Respect isolation.** Reuse compatible host prerequisites or interpreters only when the project's ownership and isolation rules allow it. Never substitute global packages or tools for locked project dependencies, or sync project packages into user/system environments. Shared manager caches are not automatically project-local.
- **Avoid configuration growth.** Prefer existing configuration and native defaults. Propose new environment variables, flags, modes, wrappers, or schemas only for a demonstrated gap; do not duplicate a setting across surfaces or persistently alter PATH/shell profiles by default.
- **Gate high-impact changes.** A design request is not permission to provision. Before any agent-executed installation—including project environments and shared manager storage—require informed user approval of the specific destinations and side effects; re-approve material scope changes. Do not make sudo, global/user-level installs, remote shell scripts, destructive cleanup, HOME writes, or hook/config replacement automatic. Surface these as separately authorized/manual paths or blockers.
- **Preserve state and report honestly.** Protect dirty locks, user files, shared hooks, and existing environments. Do not force-reset, overwrite, or claim rollback without proof. Skip dependent steps when blocked, continue independent safe work, and never report partial readiness as full success.

## Procedure

1. **Bound and inspect.** Identify the requested outcome and applicable project policy, owner, manifest/lock, install destination, and native behavior. Distinguish observed facts from proposals; check tool-version-specific semantics only when consequential.
2. **Design the requested path.** For setup, use locked reconciliation and safe repeated runs; for update, preserve declared bounds and review resolved changes. Detail both only if both are requested. Use native mechanisms before inventing orchestration. If an entrypoint prerequisite is missing, describe a short manual preflight rather than a self-installer.
3. **Check relevant risk.** Identify proposed writes, ownership, approval points, isolation, and recovery before recommending execution. If existing state or impact cannot be established, stop the affected operation and report what decision is needed; do not bypass the uncertainty with a new flag or installer.
4. **Review proportionately.** Challenge only applicable failure paths: first run, rerun, bounded update, partial failure, environment/installer boundary, or claimed platform support. Distinguish design assumptions and static checks from actual host/runtime evidence.

## Result

For a **review**, return findings, evidence, risks, and the smallest corrective action; no unsolicited implementation plan. For a **design**, give only the affected entrypoints, ownership/permissions, behavior, recovery, and verification needed to implement it. Prepare a fuller implementation handoff only when requested. Mark important behavior as existing, proposed, or unverified and stop at the requested outcome.

Do not duplicate vendor commands or platform instructions without need; confirm the applicable native contract before suggesting a specific invocation.

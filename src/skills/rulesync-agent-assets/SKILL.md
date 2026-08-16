---
name: rulesync-agent-assets
description: >-
  Use when agent customization assets must stay aligned across coding-agent
  harnesses: reuse a portable source when a target consumes it natively, generate
  multiple harness outputs from a `.rulesync/` canonical source, or bridge one
  harness's native rules, agents, skills, commands, hooks, permissions, checks, or
  MCP configuration to other harnesses with Rulesync. Do not use for isolated
  single-harness edits.
compatibility: >-
  Conversion routes require the `rulesync` CLI on PATH. Supported source/target
  harnesses, discovery paths, and features depend on the installed Rulesync version.
metadata:
  author: mols3131d
---

# Rulesync Agent Assets

Preserve one authoritative source and perform the least transformation needed. This
Skill owns routing, scope, safety, and compatibility evidence. Rulesync owns format
translation.

## Route

Choose the first route whose preconditions are evidenced.

| Situation | Route | Backend |
| --- | --- | --- |
| Target discovers the same source and required semantics are supported | Reuse | none |
| `.rulesync/` is authoritative | Canonical fan-out | `generate` |
| One harness's native assets are authoritative | Native bridge | `convert` |

Reuse requires evidence from at least one reliable source: the target's native
contract or documentation, project configuration that enables discovery, or direct
validation in the target environment. Path, filename, extension, or format similarity
alone is not evidence.

Do not introduce `.rulesync/` merely to perform a native-to-native port. Use
`import -> generate` only when adopting or rebuilding a canonical Rulesync source is
itself part of the request.

## Resolve Source Authority

Resolve the source before mutation:

1. Repository or project authority constrains which source choices are valid.
2. Within those constraints, honor an explicit caller-selected source.
3. Otherwise use established project ownership or an explicit project default.
4. If authority still conflicts or remains ambiguous, report it and stop before
   mutation.

Do not silently override repository authority or reinterpret an ambiguous source
selection as permission to migrate ownership.

## Execute

1. Read project authority, resolve the source, and limit the write boundary to the
   requested targets.
2. Select the route above. For Reuse, verify discovery and required semantics before
   choosing a no-transform result.
3. For a Rulesync route, confirm availability with `rulesync --version`. Do not
   install or upgrade Rulesync implicitly.
4. Resolve explicit targets and the smallest applicable feature set. Default to
   project scope; do not broaden to `*` or `--global` without a reason.
5. Read [Rulesync backend](references/rulesync.md) only when exact commands, target
   IDs, feature support, or discovery behavior matter. If `references/project.md`
   exists, read it only for project-specific defaults or known gaps.
6. Preview every Rulesync write with the matching dry-run.
7. Inspect the preview for unexpected files, missing source assets, warnings,
   simulated behavior, and semantics the target cannot express.
8. Apply only when the preview matches the requested scope. Then inspect the
   generated diff and run the strongest applicable validation.

## Compatibility Contract

- Preserve the selected source of truth. Generated targets remain derived artifacts
  unless an explicit ownership-transfer migration says otherwise.
- Do not silently rename, copy, relocate, normalize, or rewrite source assets merely
  to make Rulesync discover them.
- Treat file generation as a conversion result, not proof of semantic parity.
- Report omitted, approximated, simulated, unsupported, or undiscovered behavior as
  a compatibility gap.
- Prefer native target support over simulation. Enable simulation only when the
  request or project policy explicitly accepts that tradeoff.
- Do not add a wrapper script, custom adapter, or parallel schema until a concrete,
  repeated Rulesync limitation justifies one.
- Do not perform install, upgrade, cleanup, deletion, or user-global mutation as a
  side effect of ordinary asset conversion.

## Validate

For Canonical fan-out, use the same target and feature scope with Rulesync
`generate --check` when available after generation.

For Native bridge, use the dry-run, generated diff, target-native validation, and
project-owned checks. Do not invent a `generate --check` equivalent for `convert`.

For Reuse, validation must establish target discovery and the required semantics;
otherwise choose a transformation route or report the unresolved gap.

## Report

Return only evidence needed to judge the result:

```text
mode: <reuse | canonical-fan-out | native-bridge>
source: <authoritative source>
targets: <targets>
features: <features>
generated: <paths or none>
gaps: <none or concise list>
validation: <checks and evidence actually obtained>
```

Complete when the requested targets are available, source authority is preserved,
and every known compatibility gap or unrun validation is stated explicitly.

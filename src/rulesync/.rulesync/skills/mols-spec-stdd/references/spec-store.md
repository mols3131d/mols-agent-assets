# Change Store and Domain Specifications

This Skill uses an OpenSpec-inspired **change → domain-spec promotion** model. Project configuration selects the spec root; when a project has no established location, propose `spec/`. Do not create a second canonical store when the project already uses OpenSpec or another owner.

## Layout

```text
<spec-root>/
├── changes/
│   ├── add-refund-validation/
│   │   ├── proposal.md
│   │   ├── research.md                # Only when useful
│   │   ├── plan.md                    # Only when useful
│   │   ├── test-design.md             # Only when useful
│   │   └── specs/
│   │       ├── payments/refunds/validation/spec.md
│   │       └── accounts/permissions/spec.md
│   └── archive/
│       └── YYYY-MM-DD-add-refund-validation/
│           └── ...                   # Preserved change and all evidence
└── specs/
    ├── payments/refunds/validation/spec.md
    └── accounts/permissions/spec.md
```

- `changes/<change-id>/` contains **one proposed software change**, not the task-management backlog. A single change may affect several domains.
- `changes/<change-id>/specs/<domain-path>/spec.md` describes **only proposed changes to requirements**. Domain segments may nest to any useful depth; use lowercase kebab-case path segments. Never collapse a nested path into a single domain name.
- `specs/<domain-path>/spec.md` is the **current canonical behavior specification** for that domain. It contains an ordinary `## Requirements` section with the complete surviving requirements, not delta-operation headings.
- `changes/archive/<date>-<change-id>/` preserves the completed change, including its original delta and any useful proposal, research or test-design artifacts. Do not use archive as a second live specification authority.
- Test code and product code stay in the software project's established locations; the spec store can reference them without copying them.

### Delta Format

Use [Delta Template](../assets/templates/specification-delta.md). The delta contains a title, exactly one baseline marker (`<!-- base-sha256: <digest> -->` or `absent` for a new domain), an optional `## Purpose` for new domains, and one or more of:

- `## ADDED Requirements` — new named requirements and their complete observable content
- `## MODIFIED Requirements` — full replacement for existing named requirements; preserve relevant scenarios
- `## REMOVED Requirements` — existing requirement names to retire

Each operation includes `### Requirement: <name>` and its body. Names match without case/whitespace differences, but a change cannot silently convert ADDED to MODIFIED. Don't remove the last requirement of a domain via this version of the helper; retiring a whole domain needs a separate explicit decision.

The `base-sha256` marker binds a delta to the content of the canonical domain spec **when that delta is authored**. For new domains the marker is `absent`. A changed baseline stops promotion until the delta is reviewed and rebased: unrelated concurrent changes must not be overwritten. In a local CLI environment use:

```bash
python scripts/store.py --root spec baseline payments/refunds/validation
```

The digest refers to the UTF-8 bytes of `specs/<domain-path>/spec.md`; it is **not** a Git blob SHA. In ChatGPT Chat or another environment without this script, use actual source hashes or the provider's optimistic concurrency/version gate when writing, and report which precondition could be checked.

## Completion and Promotion

1. Resolve the active change, the affected nested domain specs, and the current main-spec baseline. Review implementation, tests, acceptance and unresolved findings. **Do not promote before Review PASS and applicable evidence.**
2. Check each delta against its baseline, existing requirement names and the current canonical spec. A change to several domains must be fully validated before any write.
3. Prepare the merged canonical specs by adding, replacing or removing **only** the named requirements. Preserve unchanged requirements and existing domain Purpose/other sections.
4. Inspect the proposed target changes and evidence before writing. Where the bundled helper is executable, use:

```bash
python scripts/store.py --root spec archive add-refund-validation --review review.json
python scripts/store.py --root spec archive add-refund-validation --review review.json --apply
```

The first command is a **read-only preview**. `--apply` writes the canonical spec files then moves the active change to `changes/archive/YYYY-MM-DD-<change-id>/`. It refuses unsupported domain retirement, missing base matches, duplicate names, missing targets, a preexisting archive destination, and invalid review results. A PASS JSON contains `{"result":"pass","evidence":["CI run or review reference"],"findings":[]}`. Evidence references are **not actually executed or independently checked by the helper**, so review authority and actual test execution remain with the project/runtime.

5. Re-read the updated domain specs and archive; verify that the files really changed and no active change was inadvertently removed. At a GitHub connector boundary, use the actual ref, branch, account and conditional file version provided by the connector; do not call a write successful until the host confirms it. Preserve source history.

The helper uses atomic per-file writes and attempts to roll back on filesystem failures, but **does not guarantee a multi-file database transaction across crashes or concurrent writers**. Avoid parallel archive operations, re-check ref/working-tree freshness before applying, and review the final diff. Never use a second account to work around a permission failure.

## Workflow Boundary

Artifact definitions own **what** is produced; selected workflows own **when**. Proposal/Research/Plan and Test Design live under the active change only when they add useful information; the domain-spec promotion does not make them part of the long-term canonical behavior. Completing a change does not close, reorder or prioritize Issue/Task records in a separate work-management system.

OpenSpec's storage concepts inspired this layout, but the helper is **not** the OpenSpec CLI and does not claim compatibility with all OpenSpec deltas, archive options or existing OpenSpec projects.

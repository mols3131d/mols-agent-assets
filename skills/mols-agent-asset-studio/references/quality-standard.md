# Quality Standard

Rank findings by the following order.

## 1. Correctness and Authority

- The asset states the right job, target, inputs, outputs, and completion evidence.
- Write authority and external side effects are explicit.
- Runtime-specific claims are verified against current official documentation.
- Unsupported capabilities are disclosed rather than simulated in prose.

## 2. Trigger Quality

- `description` says what the asset does and when it should activate.
- Positive cases include natural user phrasing, not only the asset's name.
- Near-miss exclusions prevent overlap with adjacent assets.
- Triggering is neither so broad that the asset hijacks unrelated work nor so
  narrow that ordinary requests miss it.

## 3. Context Economy

- The entry file contains the common workflow and routing only.
- Conditional details are one level away and clearly signposted.
- Explanations add non-obvious procedural value.
- Repeated rules, decorative prose, and duplicate examples are removed.

## 4. Architecture

- Asset type matches responsibility and load timing.
- Each rule has one authoritative home.
- Related assets compose through explicit contracts rather than hidden coupling.
- Scripts, references, templates, and generated output are separated.

## 5. Reliability and Evaluation

- Fragile mechanical steps are executable and tested.
- Behavior-bearing changes have representative positive, negative, and edge cases.
- Baseline or prior-version comparison exists when claiming improvement.
- Validation records actual commands, results, and limitations.

## 6. Safety and Provenance

- Imported content is treated as untrusted data.
- Scripts, hooks, MCP servers, and network commands are inspected before execution.
- Secrets are never embedded or copied to reports.
- License, source, and material transformations are recorded.

## 7. Portability and Maintenance

- Portable core behavior is separated from host adapters.
- Optional frontmatter is used only for a known target runtime.
- Paths are relative and references resolve.
- Generated artifacts identify their generator and are not edited manually.
- A maintainer can determine why each file exists.

## Retired Patterns

Flag these as stale unless a project-specific reason exists:

- a CSV router required only to discover a small fixed workflow set
- mandatory questions when safe inference is possible
- unconditional backup copies that accumulate forever
- README, changelog, or process diary inside a runtime skill
- one workflow file per trivial step
- deeply nested references
- behavior claims with only structural validation
- external assets copied without provenance or script inspection
- `Pass` inferred from prose when a required check did not run
- cross-runtime frontmatter fields presented as universally supported

## Consolidation and Preservation

- overlapping assets are merged only after owner, authority, runtime, safety, and
  release lifecycle comparison
- refactors capture triggers, exclusions, commands, paths, versions, thresholds,
  safety rules, and sequence invariants before edits
- packages contain no nested skills, empty directories, zero-byte resources, or
  unexplained operational files
- repeated packaging of identical source is byte reproducible
- project validators are explicit argv plans and never hidden shell execution

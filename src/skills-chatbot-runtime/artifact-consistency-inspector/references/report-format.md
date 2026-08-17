# Report Format

The report is a compact operational briefing, not a proof dossier or quality verdict. Verification remains rigorous inside the inspection workflow, while the downloadable report presents only the information needed to understand and follow up on each observation.

## Filename

Default Markdown filename:

```text
<repository-name>-artifact-consistency-report[-<target>]-<yyyyMMddHHmm>.md
```

Rules:

- use 24-hour `yyyyMMddHHmm` in the user's local timezone when available
- keep the timestamp as the final segment before the extension
- for the same logical name in the same minute, insert `-r2`, `-r3`, and so on immediately before the timestamp
- use filesystem-safe kebab-case
- abbreviate a long target while preserving identity
- apply the same suffix rule to ZIP output

## YAML front matter

Every report begins with:

```yaml
---
title: "Artifact Consistency Report — <repository or target>"
description: "Consistency differences observed across <bounded scope>."
created: "<ISO 8601 timestamp with timezone>"
updated: "<ISO 8601 timestamp with timezone>"
author: "<author>"
type: "artifact-consistency-report"
repository: "<repository identity or URL>"
target: "<target or auto-resolved scope>"
coverage: "bounded-complete | partial | blocked"
snapshot: "<commit SHA, comparison, resolved ref, or unavailable>"
---
```

Rules:

- retain literal `author: "<author>"` unless the user supplies a value
- `created` and `updated` are equal on first generation
- only `updated` changes for a revision of the same report
- timestamps include an explicit timezone offset
- `coverage` and `snapshot` match the body
- add `baseline`, `host`, `pull_request`, or `comparison` only when materially useful
- keep `result` in the Summary, not in front matter
- omit tokens, secrets, temporary local paths, and private connector identifiers

## Body schema

```markdown
# Artifact Consistency Report

## Summary

| Item | Value |
|---|---|
| Repository | `<repository>` |
| Target | `<target>` |
| Scope | `<bounded scope>` |
| Snapshot | `<snapshot or comparison>` |
| Result | `findings | incomplete | no-verified-findings` |
| Coverage | `bounded-complete | partial | blocked` |
| Confirmed observations | `<count>` |
| Unresolved observations | `<count>` |
| Verification loops | `<actual>/<requested>` |

<one-sentence briefing>

## Findings

### CON-<NNN> — <concise observation>

- **Status:** `verified | unresolved`
- **Type:** `contradiction | omission | drift | stale-reference | revision-mismatch | handoff-gap | validation-gap`
- **Relation:** `<artifact A>` ↔ `<artifact B or missing counterpart>`

#### Observed difference

<plain-language description of the consistency difference>

#### References

- `<pinned URL or reproducible locator>` — <short observed fact>

#### Why unresolved

<include only when Status is unresolved>

#### Potential impact

<direct, supported consequence stated without severity scoring or remediation>

## Coverage

- **Checked:** <relations and artifact clusters>
- **Resolved rule sources:** <ordered locators or none>
- **Rule-source conflicts:** <conflicts or none>
- **Excluded:** <explicit or evidence-backed exclusions>
- **Limitations:** <inaccessible or unverified areas>
- **Assessment boundary:** <what the report does not cover>
```

## Presentation rules

- Use heading level 4 for `Observed difference`, `References`, `Why unresolved`, and `Potential impact`.
- Omit `Why unresolved` from verified findings.
- Use a short Summary table instead of a long metadata list.
- Keep references reproducible, but do not turn the report into an evidence matrix.
- Do not expose detailed counterevidence logs by default.
- Do not add severity, confidence, owner, due date, remediation, or approval verdict unless the user explicitly requests them.
- Use neutral reporting language such as “observed difference,” “may,” and “could” when the consequence is conditional.
- Merge observations sharing one relation and root cause.
- Sort findings by relation, type, and primary locator, then assign IDs from `CON-001`.

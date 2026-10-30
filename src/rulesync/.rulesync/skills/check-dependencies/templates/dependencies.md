# Dependency Check — {{TITLE}}

> **Finding:** {{ONE_SENTENCE_RESULT}}
>
> **Boundary:** `NONE_REPORTED` ≠ safe; `NOT_FOUND_PUBLIC` ≠ globally nonexistent. Unchecked and unsupported inputs remain unknown.

| Field | Value |
|---|---|
| Revision / worktree | `{{REVISION_OR_WORKTREE}}` |
| Inspected manifests | {{SUPPORTED_PATHS_AND_OMISSIONS}} |
| Pinned / unresolved / skipped | {{COUNTS}} |
| Network lookups | {{NOT_RUN_OR_ENDPOINTS_AND_TIME}} |
| Inventory tool | {{TOOL_NAME_AND_VERSION_OR_MANUAL}} |

## Findings

| Package | Version | Registry evidence | Known advisory IDs | Next action |
|---|---|---|---|---|
| `{{NAME}}` | `{{VERSION}}` | {{REGISTRY_STATUS}} | {{ADVISORY_IDS_OR_UNKNOWN}} | {{SPECIFIC_NEXT_CHECK}} |

<!-- Replace the example; if none, say 'No advisories reported in checked scope' and describe coverage. -->

## Unresolved coverage

- {{UNPINNED_PRIVATE_UNSUPPORTED_MISSING_NETWORK_OR_NONE}}

## Detail

<details>
<summary><strong>{{PACKAGE_NAME}} · {{VERSION}}</strong> — lookup and advisory evidence</summary>

- **Source:** `{{MANIFEST_PATH_AND_LOCK_PATH_OR_LINE}}`
- **Public registry:** {{REGISTRY_STATUS_AND_CHECK_TIME}}
- **OSV:** {{OSV_STATUS_AND_IDS_OR_NOT_CHECKED}}
- **Advisory links:** {{LINKS_OR_NONE}}
- **Interpretation:** {{WHAT_IS_AND_IS_NOT_ESTABLISHED}}

</details>

## Next checks

1. {{HIGHEST_VALUE_SAFE_NEXT_STEP}}

## Verification record

| Check | Result |
|---|---|
| Manifest parsed | {{PASS_PARTIAL_FAIL}} |
| Lockfile exact versions | {{COUNT_OR_NOT_AVAILABLE}} |
| Public registry queried | {{YES_NO_AND_SCOPE}} |
| OSV queried | {{YES_NO_AND_SCOPE}} |
| Unsupported files or failures | {{DETAILS_OR_NONE}} |

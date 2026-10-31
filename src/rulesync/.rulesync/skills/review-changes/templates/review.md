# Change Review — {{TITLE}}

> **Result:** {{ONE_SENTENCE_VERDICT}}
>
> **Evidence:** `CONFIRMED` = direct reproduction/decisive source condition; `SUPPORTED` = source-backed triggering scenario; `HYPOTHESIS` = further verification required. Priority and evidence are different properties.

| Field | Value |
|---|---|
| Repository / revision | `{{REPOSITORY}}` / `{{HEAD_COMMIT_OR_WORKTREE}}` |
| Compared range | `{{EXPLICIT_BASE_HEAD_OR_STAGED_UNSTAGED}}` |
| Reviewed files | {{PATHS_AND_OMISSIONS}} |
| Tests executed | {{ACTUAL_TEST_COMMANDS_OR_NOT_RUN}} |

## Findings

| ID | Priority | Evidence | Location | Impact |
|---|---|---|---|---|
| [R1](#r1) | {{BLOCKER_HIGH_MEDIUM_LOW}} | {{CONFIRMED_SUPPORTED}} | [{{FILE}}]({{RELATIVE_LINK}}), {{LINE_RANGE}} | {{IMPACT}} |

<!-- Remove the example row and section when there are no findings; say 'No actionable findings in reviewed scope.' instead. -->

<a id="r1"></a>
<details>
<summary><strong>R1 · {{SHORT_DEFECT_TITLE}}</strong> — {{PRIORITY}}, {{EVIDENCE_STATUS}} (details)</summary>

- **Change and evidence:** [{{FILE}}]({{RELATIVE_LINK}}), lines {{LINE_RANGE}}; {{SOURCE_OR_DIFF_FACT}}
- **Trigger / prerequisite:** {{CONCRETE_CONDITION}}
- **Observable impact:** {{FAILURE_MODE}}
- **Validation:** {{ACTUAL_REPRODUCTION_OR_NOT_RUN}}
- **Suggested minimal fix:** {{FIX_IDEA}}
- **Targeted test:** {{TEST_CASE}}
- **Uncertainty:** {{OPEN_ASSUMPTION_OR_NONE}}

</details>

## Follow-up checks (not findings)

- {{UNVERIFIED_HYPOTHESIS_OR_NONE}}

## Coverage and verification

| Check | Status |
|---|---|
| Git range/status confirmed | {{DONE_PARTIAL_NOT_RUN}} |
| Diff and surrounding contracts reviewed | {{FILES_AND_LIMITS}} |
| Untracked/binary/truncated portions | {{OMISSIONS_OR_NONE}} |
| Tests executed | {{COMMAND_OUTPUT_OR_NOT_RUN}} |
| External behavior verified | {{YES_WITH_EVIDENCE_OR_NOT_RUN}} |

**Limit:** No review proves the absence of defects; results apply only to the stated diff and checked context.

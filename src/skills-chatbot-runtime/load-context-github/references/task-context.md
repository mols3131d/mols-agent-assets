# GitHub Task Context

Read only the section that matches the current GitHub object or operation.

## Pull Request and Review

Inspect only what affects the current PR/review:

- actual head ref and relevant repository instructions on that head;
- base instructions when a head/base difference could change the review or action;
- changed-file paths and their applicable path instructions;
- pull-request templates, `CODEOWNERS`, or explicit review guidance when relevant;
- live checks, protection, or metadata only when they affect the requested decision.

Do not turn repository context loading into the review methodology itself.

## Issue

When working with a concrete issue, inspect relevant issue templates or contribution
guidance only if they affect classification, expected fields, workflow, or mutation.

Do not load every issue template for a read-only summary that does not depend on them.

## Commit

For commit work, inspect repository-owned commit guidance such as `.gitmessage`,
contribution docs, or hook documentation when relevant. Do not assume a conventional
commit format unless the repository defines or requests it.

## Branch, Merge, and History

For branch, merge, or history operations, load repository branch/VCS guidance and live
protection/ruleset metadata when they materially constrain the operation.

Do not invent universal branch names, merge strategies, update-branch policies, or
history rules.

## CI, Checks, Workflows, Security, and Permissions

Load only the relevant workflow files, validation docs, check metadata, permission
requirements, or security guidance needed for the current task.

A failing check does not justify reading every workflow in the repository. Start from the
named or failing surface and expand only when evidence requires it.

## Release

For release work, inspect release/versioning guidance, relevant workflow or automation,
and live release metadata only as needed. Release creation remains a task action, not a
responsibility of the context loader.

## Expand Search Only When Needed

If explicit high-signal locations are insufficient, search repository content for the
concept actually needed. Useful terms may include:

`git`, `github`, `vcs`, `branch`, `commit`, `push`, `pull request`, `merge`, `review`,
`release`, `contributing`, `agent`, `bot`, `automation`, `check`, `workflow`.

Prefer terminology already used by the repository. Follow referenced required guidance
only as far as the current task needs it. Do not recursively traverse references or read
the whole repository merely because links exist.

## Stop Condition

Stop loading context when the agent can identify:

- the concrete repository/ref/object;
- the rules that actually apply to the target scope;
- task-specific constraints that can change the next action;
- any unresolved conflict that blocks a safe mutation.

Additional context that is unlikely to change the next action should not be loaded.

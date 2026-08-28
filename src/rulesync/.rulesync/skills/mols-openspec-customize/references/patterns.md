# OpenSpec Customization Patterns

These are reusable design patterns, not OpenSpec requirements. Confirm current
mechanics in the official documentation before applying them.

## Config before schema

Use project configuration for additive guidance when it is sufficient. Fork or
create a schema only when the artifact model, dependency flow, templates, or
schema-level instructions must materially change.

This keeps upgrades and maintenance simpler and avoids owning a schema snapshot for
a change that only needed one rule.

## Delta-only context

Put only planning context into OpenSpec that should materially shape workflow
output. Do not turn `config.yaml` into a second project handbook.

Prefer a concise pointer to canonical repository guidance when the active agent can
reliably load that guidance. Copy the minimum necessary delta only when OpenSpec
must inject it directly for the workflow to behave correctly.

## Narrowest injection surface

Place guidance at the smallest scope that needs it:

- cross-workflow planning context stays global only when every relevant run needs
  it;
- artifact-specific expectations stay with that artifact;
- execution guidance stays with the relevant operation;
- structural workflow changes stay in the schema.

Do not solve a narrow artifact problem with global context.

## Preserve source authority

OpenSpec customization should adapt to repository policy, not become a competing
policy owner. Keep testing, architecture, contribution, security, language, and
other repository rules with their canonical owners unless OpenSpec must carry a
small operational delta.

If the same rule appears in project instructions, OpenSpec configuration, and a
schema template, identify which one actually owns the decision and remove accidental
copies.

## Treat schema forks as owned snapshots

A custom schema is an intentionally owned copy, not a live extension of the
package's built-in schema. Keep a team-shared schema project-local and versioned
with the repository. Decide explicitly when upstream schema improvements should be
ported instead of expecting ordinary OpenSpec updates to merge them automatically.

## Verify rendered behavior

Static YAML review is not enough when the claim is about what the agent receives or
which schema resolves. Use the current OpenSpec inspection and validation commands
that correspond to the claim, such as resolved instructions, schema validation,
schema resolution, or template resolution.

Verify the smallest observable surface that can prove the customization worked.
Do not infer runtime behavior merely because configuration parses.

## Keep the three layers visible

When documenting or reviewing a customization, distinguish:

1. what OpenSpec officially supports;
1. why a reusable pattern chooses one supported mechanism over another;
1. why this project chooses a particular concrete value or rule.

This separation makes vendor upgrades, pattern changes, and project policy changes
independently reviewable.

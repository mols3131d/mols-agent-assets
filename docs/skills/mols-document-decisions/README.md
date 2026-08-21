# mols-document-decisions Maintainer Docs

`mols-document-decisions` is the portable decision-record member of the `mols-document` family.

## Intent

Provide a small fallback decision format without overriding a consumer repository's accepted ADR or decision convention.

## Invariants

- Project-local decision authority wins when present.
- Decisions-Lite is a fallback, not a repository-wide mandate.
- A decision records what was chosen, why, and the material consequence.
- Status is explicit; approval or evidence is never invented.
- Existing decisions are preserved unless an explicit change requires otherwise.
- Runtime packaging stays small: the Skill and the fallback template are sufficient.

## Maintenance

Do not reintroduce a generic document studio, workflow index, BLUF reference, or emoji reference into this package merely for reuse. Shared writing and Markdown concerns belong to their existing owners.

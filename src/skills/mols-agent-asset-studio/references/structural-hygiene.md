# Structural Hygiene

A runtime skill should contain only files that directly support its job.

## Errors

- nested discoverable `SKILL.md` below the skill root
- symlinks, path escapes, cache directories, or build output
- empty directories or zero-byte resources
- broken local links
- invalid Python syntax

## Warnings Requiring Review

- executable entry scripts absent from the operation map
- references, templates, or assets not mentioned by any Markdown entrypoint
- placeholder or sample filenames left in a release
- command scripts with no matching test evidence when a tests root is supplied

Run:

```bash
python scripts/audit_skill_structure.py <skill-root> --json
```

Use `--warnings-as-errors` for release closure after reviewing intentional
exceptions. Generated packages never include empty directories, but source
validation should still reject them so stale scaffolding is removed.

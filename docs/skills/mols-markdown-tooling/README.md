# mols-markdown-tooling Maintainer Docs

`mols-markdown-tooling` is the deterministic maintenance member of the `mols-markdown` family.

## Intent

Keep repeatable Markdown mechanics in executable utilities while leaving semantic writing and document decisions to other capabilities.

## Invariants

- Deterministic validation or parsing is not replaced by an LLM fallback when that would change semantics.
- Missing required tooling fails explicitly.
- Repository-native commands and configuration win when they already own the target behavior.
- Generated indexes remain projections and are regenerated from source Markdown/frontmatter.
- Dependencies stay minimal and justified by deterministic behavior.
- The runtime package does not need a workflow index; `SKILL.md` routes directly to the bundled utilities.

## Maintenance

Prefer deleting obsolete workflow prose when the utility CLI and Skill contract already express the same behavior. Keep backend documentation only when it captures a non-obvious invariant that cannot be recovered from the executable interface.

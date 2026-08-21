# mols-markdown-maintenance Maintainer Docs

`mols-markdown-maintenance` owns deterministic Markdown mechanics in the `mols-markdown` family.

## Invariants

- Deterministic validation or parsing is not replaced by an LLM fallback when that would change semantics.
- Missing required tooling fails explicitly.
- Repository-native commands and configuration win when they already own the target behavior.
- Generated indexes remain projections and are regenerated from source Markdown/frontmatter.
- Dependencies stay minimal and justified by deterministic behavior.
- `SKILL.md` routes directly to bundled utilities; no workflow index is required.

## Maintenance

Keep backend prose only for non-obvious invariants that cannot be recovered from the executable interface. Prefer deleting duplicated workflow instructions over adding another routing layer.

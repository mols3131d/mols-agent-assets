# mols-markdown-maintenance Maintainer Docs

`mols-markdown-maintenance` owns deterministic Markdown maintenance selection and the small local delta not already provided by the selected Markdown backend.

## Invariants

- Repository-native Markdown tooling and configuration win when they already own the requested behavior.
- Standard formatting, heading checks, and link checks use rumdl directly instead of local wrapper scripts.
- Custom runtime code is limited to frontmatter schema validation and frontmatter-driven index generation.
- Deterministic validation or parsing is not replaced by an LLM fallback when that would change semantics.
- Missing required tooling fails explicitly.
- Generated indexes remain projections and are regenerated from source Markdown/frontmatter.
- Dependencies stay minimal and justified by local deterministic behavior.

## Maintenance

Do not mirror rumdl's changing rule/configuration reference here. Keep only the ownership boundary and local invariants; consult current upstream authority when exact backend semantics matter.

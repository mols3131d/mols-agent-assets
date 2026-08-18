# Customization Guide

## Safe to change

- skill `name` and `description`
- README wording and invocation examples
- report title and description wording
- `author` value or placeholder policy
- default language
- output filename prefix and target abbreviation
- auto loop upper bounds
- report section headings
- ZIP usage conditions
- optional report front matter fields
- scenario inventory and test-report wording

External ZIP and report filenames may be changed freely. Keep timestamp suffixing when download-folder collision and cache ambiguity matter.

## Rule-source customization

- `rule_sources` may use repository-specific locators or selectors.
- User-defined list order is authoritative for that run.
- Auto-discovery signals may be extended for a domain, but do not hard-code one universal source-type precedence.
- If a source selector is renamed, update `SKILL.md`, `docs/rule-sources.md`, examples, and tests together.

## Preserve

- skill root `SKILL.md`
- read-only repository access
- no mutation of repository or repository-host state
- no fixed project layout or directory assumptions
- compact `Observed difference / References / Potential impact` finding structure
- `Why unresolved` only for unresolved findings
- adversarial counterevidence checks inside the inspection workflow
- no verified omission without bounded absence
- no silent revision mixing
- no silent authority choice when rule sources conflict
- `verified` versus `unresolved`
- no overall consistency guarantee from `no-verified-findings`
- downloadable Markdown or necessary ZIP delivery

## Rename behavior

- external ZIP: freely renameable
- internal root folder: renameable when package references and tests are updated
- `README.md`, `docs/*.md`: renameable when `SKILL.md` relative references are updated
- `SKILL.md`: preserve this filename and keep it at the skill root
- report output: renameable; timestamp suffix remains recommended

## Front matter changes

Fields may be added when needed, provided that:

- free-text values are quoted
- machine fields match body state
- secrets and temporary internal paths are excluded
- samples, tests, README, and report-format rules are updated together

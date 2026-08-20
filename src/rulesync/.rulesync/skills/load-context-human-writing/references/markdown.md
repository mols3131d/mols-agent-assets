# Markdown for Human

Use this reference only when Markdown is the actual reader-facing surface and Markdown
representation choices materially affect comprehension.

Markdown is an implementation surface, not the owner of human-writing principles. Apply
the parent Skill's reader-work and understanding-debt lens first, then choose the smallest
Markdown structure that exposes the information clearly.

## Headings and prose

- Use headings as navigation boundaries, not decoration.
- Keep heading depth as shallow as the real information hierarchy allows.
- Prefer specific headings that help a scanning reader predict the section's content.
- Avoid consecutive label-only headings and filler prose inserted only to separate them.
- Keep one useful job per paragraph or section when possible; do not enforce arbitrary
  length limits.
- Use inline code for commands, paths, identifiers, field names, and other literal tokens
  when that distinction helps the reader.

## Lists and tables

Use a list when items share one role but do not need attribute-by-attribute comparison.
Use numbering when sequence, priority, or ordered execution matters. Keep sibling items at
roughly the same abstraction level and grammatical shape.

Use a table when the reader must compare repeated attributes across the same dimensions.
Do not force long narrative, procedures, or structurally different items into cells merely
for compactness. If a table becomes difficult to scan on the expected surface, prefer a
list or sections.

## Callouts and footnotes

Use a callout only when a note, tip, warning, exception, or constraint needs unusual
salience. On GitHub-compatible surfaces, `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, and
`CAUTION` may be used when supported. Do not use callouts as generic section containers.

Use footnotes or a short References section for supporting citations, definitions, or
secondary detail that would interrupt the main reading path. Never hide a core decision,
required procedure, or material constraint in a footnote.

## Semantic markers

Emoji may act as scan markers for recurring state, risk, action, or category when that
meaning is useful to the reader. Text labels remain authoritative; never rely on color or a
glyph alone.

Status and action markers:

| Marker | Meaning |
| --- | --- |
| `✅` | Done, Pass, Success |
| `❌` | Fail, Error |
| `⚠️` | Warning, Risk |
| `ℹ️` | Information, Note |
| `⏳` | Pending, In progress |
| `🔍` | Inspect, Search |
| `📝` | Write, Edit, Create |
| `🔄` | Update, Sync, Loop |
| `🧪` | Test, Verify |
| `🚀` | Deploy, Release |

Status or priority circles:

| Marker | Meaning |
| --- | --- |
| `🔴` | Critical, Blocked, Stop |
| `🟠` | High risk, Attention |
| `🟡` | Warning, Pending, Review |
| `🟢` | Safe, Ready, Complete |
| `🔵` | Information, Reference |
| `🟣` | Optional, Experimental |
| `⚫` | Disabled, Deprecated, Unknown |
| `⚪` | Neutral, Unclassified |

Colored squares such as `🟦`, `🟧`, `🟩`, `🟥`, `🟪`, `🟨`, `⬛`, and `⬜` may distinguish
labeled categories or components. Do not use them as unlabeled status.

Keep the same marker meaning stable within a document and one marker system within a
repeated list. Do not append emoji decoratively to every sentence.

## Text bars

Text bars are compact source-readable visuals for a small amount of simple quantitative
information. Always display the exact value and unit; the bar is secondary evidence.

For progress with a real denominator:

```text
Overall    ████████░░  80%  8/10
Transform  ██████░░░░  60%  6/10
Load       ░░░░░░░░░░   0%  0/10
```

- A 10-cell width is a useful default, not a requirement.
- Use a consistent width and scale within one block.
- Do not invent a percentage when the denominator is unknown.
- Do not duplicate the same values in a table or chart unless the second representation
  answers a different reader question.

For roughly 2–6 comparable categories with one non-negative value and one unit, a horizontal
bar can expose rank and gap:

```text
Python      ███████████████  48 jobs
TypeScript  ███████████      35 jobs
SQL         ██████           19 jobs
Rust        ███               8 jobs
```

Use a zero-based linear scale, show exact values, and sort by value when ranking is the
question. A 20-cell maximum is a useful default for source readability. Prefer a chart when
trend, uncertainty, negative or bidirectional change, many categories, mixed units, or more
complex quantitative reasoning is the real question.

## Tree structures

Use a text tree for a compact single-parent hierarchy such as files, modules, sections, or
ownership:

```text
pipeline/
├── extract/
│   ├── api.py
│   └── database.py
├── transform/
│   └── clean.py
└── load/
    └── warehouse.py
```

- Keep root and ordering clear.
- Preserve the real hierarchy and names; do not rearrange them for appearance.
- Prefer a shallow tree; around four levels is a useful default before selective omission
  or another representation becomes easier to scan.
- Show only the branches needed for the current question when the tree is large, and mark
  omissions when they could matter.
- Put long explanations outside the tree.
- Use a diagram for DAGs, dependencies, runtime flow, or multi-parent relationships.

## Final check

Before keeping any Markdown element, ask whether it reduces orientation, retrieval,
interpretation, comparison, action, or re-entry cost for the intended reader. If plain
prose or a short list is clearer, use the simpler representation.

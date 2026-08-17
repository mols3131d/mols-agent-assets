---
name: mols-mermaid-chart
description: >-
  Create, edit, review, repair, or choose Mermaid quantitative charts, including
  finding numeric tables/metric sections in Markdown/docs that should become
  chart-as-code. Use when Mermaid/chart-as-code is explicit or clearly implied
  and the primary question is magnitude/ranking, ordered or time trend,
  part-to-whole proportion, quantified flow, weighted hierarchy, same-scale
  profile, or normalized two-axis positioning. Strong signals: XY bar/line,
  pie, Sankey/quantified flow, treemap, radar, quadrant, or existing Mermaid
  chart syntax/scale/label/readability/fidelity/compatibility fixes. Also use
  for explicit Mermaid requests for unsupported histogram/scatter/box/density/
  multi-axis so they can be rejected/routed without approximation. Do not use
  for generic plotting, procedures/handoffs/message or event order/state,
  architecture/schema/cardinality, unweighted hierarchy, or whole-dashboard
  design.
---

# Mermaid Chart Contract

Create chart-as-code that makes one quantitative question easier to answer without changing the meaning of the source data.

- Treat supplied data and established source evidence as authoritative. Do not invent values, categories, targets, averages, rankings, trends, correlations, or missing values.
- Preserve sign, unit, category or temporal order, population, reference time, and missingness unless the user explicitly requests a transformation.
- Keep one primary quantitative question per chart. Split the chart or use a table when one view becomes overloaded.
- Prefer semantic clarity over decorative styling. Design in roughly this order: question → chart type → scale → order → label → legend → annotation → color.
- Do not infer causation from a trend or correlation.
- For an existing chart, follow explicit user instruction, then local document or project conventions, and otherwise preserve its series order, labels, theme, and visual language.
- Treat the target renderer and its Mermaid version as the compatibility authority. Never assume every Mermaid chart type, syntax feature, or configuration option is available everywhere.

Data discovery, factual research, generic plotting, and dashboard composition are separate responsibilities. Use already established evidence where possible; if missing data prevents a faithful chart, state what is missing instead of fabricating it.

# Chart Selection

Choose the simplest Mermaid type that directly answers the quantitative question.

| Quantitative question | Mermaid form | Main boundary |
| --- | --- | --- |
| Compare category values or ranks | `xychart` + `bar` | Avoid when labels or categories become too dense |
| Show change over time or another ordered progression | `xychart` + `line` | Do not connect unordered categories as a trend |
| Show parts of one whole | `pie` | Prefer bar for many slices or precise ranking |
| Show how much moves from source to target | `sankey` | Use only when link values matter, not topology alone |
| Compare magnitude inside a hierarchy | `treemap-beta` | Avoid negative values and overly deep hierarchy |
| Compare entities across the same dimensions and scale | `radar-beta` | Avoid mixed scale direction or too many dimensions |
| Position items on two defined normalized axes | `quadrantChart` | Coordinates must have a defensible 0–1 basis |

Use a different representation when Mermaid would distort the question:

- relationship, procedure, state, architecture, schema, ownership, cardinality, chronology, or event-order questions → a Mermaid diagram capability such as `mols-mermaid-diagram` when available;
- whole-dashboard layout or metric-panel composition → a dashboard capability such as `mols-markdown-dashboard` when available;
- histogram, box plot, scatter plot, density plot, multi-axis chart, or dense interactive analysis → a table or charting tool that supports the required statistical form.

For pie charts, every slice must belong to the same whole, population, and reference time. For Sankey, verify `source`, `target`, and `value` semantics. For radar, dimensions must be comparable on the same directional scale. For quadrant charts, define both axes before placing points.

# Web Reference Policy

When web access is available, prefer a narrow live reference pass over remembered Mermaid syntax or version behavior.

1. Before choosing, creating, materially editing, reviewing, or repairing a Mermaid chart, read the **relevant official Mermaid type page**. If the type is not chosen yet, use the official syntax index only long enough to resolve the type, then open that type's page.
1. If the request names a chart type that Mermaid may not support, use the official syntax index or official docs search to verify support before selecting any approximation. Do not invent a Mermaid equivalent merely because no type page exists.
1. Also read the **single most relevant canonical `mols-mermaid-chart` reference** for the task. Load additional canonical references only when the task crosses responsibility boundaries such as selection plus styling or syntax plus renderer debugging.
1. Official Mermaid documentation owns syntax, type-specific numeric constraints, feature availability, configuration, and version/renderer behavior.
1. Canonical repository references own the fuller selection, data-integrity, style, editing, and verification guidance summarized by this flat Skill when they do not conflict with official Mermaid behavior.
1. Do not load the whole official documentation set or canonical reference tree. The goal is better evidence, not maximum context.
1. If web access is unavailable or a source cannot be reached, use this embedded contract and avoid unsupported certainty about syntax, feature gates, or renderer compatibility.

Reference routing:

| Task | Official Mermaid | Canonical reference |
| --- | --- | --- |
| Choose or create a chart | selected type page | `references/mermaid-charts.md` |
| Change chart type or data mapping | selected/new type page | `references/mermaid-charts.md` |
| Edit theme, palette, emphasis, labels, or visual language | selected type page | `references/style-policy.md` |
| Diagnose syntax, render, export, or compatibility | selected type page + relevant configuration/CLI page when needed | `references/mermaid-chart-verification.md` |
| Need an advanced syntax pattern | selected type page | only that type under `references/examples/` |

# Procedure

## 1. Resolve the quantitative question

Determine what the reader should learn from the chart in one sentence. Identify the source values, units, reference time, population, intended order, and missing values that materially affect the view.

If the request is primarily relational rather than quantitative, or is generic plotting without Mermaid/chart-as-code context, route away instead of forcing it into this Skill.

## 2. Research the selected form

Apply the Web Reference Policy when web access is available. Confirm the chosen type's current syntax, numeric constraints, and relevant feature support against official Mermaid documentation before relying on them.

Prefer stable and widely supported forms when two choices answer the question equally well. Treat experimental, beta, new, or version-gated forms as compatibility-sensitive and keep a simpler fallback in mind.

## 3. Build the minimal chart

- Keep source order unless a meaningful comparison requires an explicitly requested sort.
- Include titles or axis labels when they clarify measure, unit, or direction.
- Keep a zero baseline when it is meaningful for magnitude comparison; if an axis is truncated, make that choice explicit.
- Do not combine incompatible units or scales simply to reduce chart count.
- Inherit the active theme and Mermaid's automatic palette by default. Do not add custom theme or color configuration unless the user, local convention, or a verified semantic need requires it.
- Do not use color as the only carrier of series, state, magnitude, or category meaning; keep labels, legends, sign, or order sufficient to interpret the chart.
- Use styling only when it communicates grouping or emphasis that is already supported by the data.

If exact values matter and the rendered chart cannot communicate them reliably, provide a compact source table in addition to the chart. Do not duplicate the same information by default.

## 4. Check fidelity and compatibility

Before finalizing, verify:

1. every plotted value maps to source evidence;
1. units, sign, order, population, and time basis are preserved;
1. the chosen chart type matches the actual question;
1. type-specific numeric constraints are satisfied;
1. Mermaid syntax and requested features match the target renderer when that can be checked;
1. labels and scale do not create a misleading comparison.

If actual rendering cannot be verified, say so only when compatibility is material to the user's task.

# Output

Return only the output surface the user needs.

- For chat or Markdown documents, default to a fenced `mermaid` block with only the explanation needed to interpret data or compatibility caveats.
- When editing existing content, change only the requested chart and nearby text required for consistency.
- When the host cannot render the selected Mermaid type, preserve the Mermaid source if useful and offer the nearest faithful fallback rather than silently changing the data question.
- When Mermaid cannot faithfully express the requested chart, say so and use or recommend the appropriate table or charting capability.

# Authoritative References

Official Mermaid documentation:

- Syntax index: <https://mermaid.js.org/intro/syntax-reference.html>
- XY Chart: <https://mermaid.js.org/syntax/xyChart.html>
- Pie: <https://mermaid.js.org/syntax/pie.html>
- Sankey: <https://mermaid.js.org/syntax/sankey.html>
- Treemap: <https://mermaid.js.org/syntax/treemap.html>
- Radar: <https://mermaid.js.org/syntax/radar.html>
- Quadrant Chart: <https://mermaid.js.org/syntax/quadrantChart.html>

Canonical `mols-mermaid-chart` references:

- Skill: <https://github.com/mols3131d/mols-agent-assets/tree/main/src/skills/mols-mermaid-chart>
- Selection and data integrity: <https://github.com/mols3131d/mols-agent-assets/blob/main/src/skills/mols-mermaid-chart/references/mermaid-charts.md>
- Style policy: <https://github.com/mols3131d/mols-agent-assets/blob/main/src/skills/mols-mermaid-chart/references/style-policy.md>
- Verification: <https://github.com/mols3131d/mols-agent-assets/blob/main/src/skills/mols-mermaid-chart/references/mermaid-chart-verification.md>
- Examples index: <https://github.com/mols3131d/mols-agent-assets/blob/main/src/skills/mols-mermaid-chart/references/examples/README.md>

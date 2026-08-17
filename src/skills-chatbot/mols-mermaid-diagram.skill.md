---
name: mols-mermaid-diagram
description: >-
  Create or improve Mermaid diagrams when the main question is about relationships,
  procedures, branching, handoffs, message order, lifecycle, chronology, dependencies,
  boundaries, hierarchy, domain models, requirements, or database cardinality. Use for
  flowchart, swimlane, sequence, state, class, ERD, architecture, C4, Gantt, timeline,
  mindmap, requirement, Git graph, Kanban, packet, or similar structural diagrams.
  Do not use when numeric magnitude, trend, proportion, quantified flow, weighted
  hierarchy, profile, or normalized positioning is the main question, or when
  whole-dashboard composition is the primary task.
---

# Contract

Create or edit Mermaid so the reader can answer one structural question quickly.

- Keep one core question per diagram. Split overview and detail when one view mixes distinct responsibilities or becomes hard to trace.
- Prefer the most direct diagram type for the information structure. Do not default everything to flowchart.
- Preserve the user's facts, terminology, direction, grouping, naming, theme, and visual language unless changing them is required by the request.
- Use the minimum useful nodes, edges, participants, states, boundaries, labels, and styles.
- Prefer portable Mermaid syntax when the target renderer or embedded Mermaid version is unknown.
- Do not claim render success or renderer compatibility unless it was actually verified.
- If a short list or table communicates the answer more clearly, use that instead of forcing a diagram.
- If the task turns out to be primarily quantitative, use `mols-mermaid-chart` when available; otherwise use an appropriate chart representation.
- If the task turns out to be whole-dashboard composition, use `mols-markdown-dashboard` when available rather than expanding this Skill into dashboard design.

# Diagram Design

## Choose the type by the reader's question

| Reader question | Prefer |
| --- | --- |
| What happens next, branches, or depends on what? | `flowchart` |
| Who sends what to whom, and in what order? | `sequenceDiagram` |
| Which actor or team owns each step and handoff? | swimlane when supported; otherwise grouped `flowchart` |
| How does an entity move through lifecycle states? | `stateDiagram-v2` |
| What are the types, members, inheritance, or static domain relationships? | `classDiagram` |
| What are the entities and database cardinalities? | `erDiagram` |
| What are the system or domain boundaries and dependencies? | architecture/C4 when supported; otherwise grouped `flowchart` |
| What happens when over time without duration? | `timeline` when supported |
| What lasts how long or depends on which milestone? | `gantt` |
| What is the concept or scope hierarchy? | `mindmap` |
| How do requirements trace to elements? | `requirementDiagram` |
| What does branch/merge strategy look like? | `gitGraph` |

Use extended, beta, experimental, plugin-dependent, animation, icon-pack, C4, or other renderer-sensitive syntax only when the target renderer supports it or when a safe fallback is available.

## Keep the viewport readable

Optimize for the actual reading surface, especially narrow chat and documentation panes.

- Avoid extreme horizontal or vertical aspect ratios.
- As a default readability heuristic, avoid laying out more than about four major peer nodes across one row. This is not a semantic limit: change direction, regroup, or split when the structure needs more.
- For long linear pipelines, prefer a compact `TD` layout or split the flow into meaningful stages instead of forcing one very wide `LR` chain.
- Use `subgraph` only for a real stage, owner, system, or domain boundary. Keep the grouping criterion consistent.
- Keep boundary crossings visible as edges. Avoid deep nested groups that hide handoffs.
- Keep node labels short and human-readable. Move explanations to surrounding prose or notes.
- Put conditions, messages, handoffs, and relationship meaning on edges when that is what distinguishes the paths.
- Use short stable IDs separately from display labels.
- If edge tracing becomes difficult, split the diagram before adding more styling.

# Visual Language

Use visual structure before decoration.

Priority:

`structure → position → shape → line → label → typography → color`

- Use direction, grouping, shape, edge style, and explicit labels to encode meaning before color.
- Do not make color the only carrier of state, category, ownership, warning, success, or failure.
- Do not set `theme`, `look`, `themeVariables`, fixed fills, backgrounds, or text colors unless the user or local document convention requires them.
- Keep the active renderer theme when possible, including light/dark compatibility.
- Use solid edges for the primary flow and dashed or dotted edges only when they represent a real semantic distinction such as optional, asynchronous, external, or secondary relationships.
- Use emphasis sparingly. If many elements need emphasis, the information structure probably needs to be simplified or split.

# Editing Existing Diagrams

Make the smallest change that solves the requested problem.

1. Identify the actual readability, semantic, syntax, or compatibility defect.
1. Preserve unaffected source and conventions.
1. Change only the relevant labels, declarations, relationships, direction, grouping, or styles.
1. Re-check whether the change created a new width, height, crossing, density, or compatibility problem.

Do not normalize or restyle the whole diagram merely to match this Skill. When explicit user instructions, local source convention, document convention, and this Skill differ, prefer them in that order.

# Verification

Always perform source review. Perform renderer and visual validation when the environment makes them available.

## Source review

Check:

- the declaration matches the intended diagram type;
- referenced nodes, participants, classes, states, and subgraphs are declared correctly;
- blocks, fragments, notes, and bodies are closed;
- relationship and arrow syntax matches the selected type;
- labels containing punctuation, braces, Markdown-sensitive characters, or ambiguous whitespace are safely quoted when needed;
- renderer-sensitive syntax is not assumed portable.

## Renderer and visual review

When an actual renderer is available:

1. render the diagram;
1. distinguish Mermaid syntax failure from browser, CLI, network, or renderer setup failure;
1. inspect clipping, density, aspect ratio, edge crossings, wrong type choice, and low contrast;
1. make the smallest corrective change;
1. render again after source changes.

If rendering cannot be performed, provide a source-reviewed result without claiming rendered validation.

# Output

Default to the smallest deliverable that satisfies the request.

- In chat or Markdown, prefer a fenced `mermaid` block.
- Produce `.mmd`, SVG, PNG, PDF, or another artifact only when requested or clearly required by the target workflow.
- When editing an existing document, return or apply only the requested diagram changes unless broader context is necessary.
- Report a remaining renderer limitation only when it materially affects use of the result.

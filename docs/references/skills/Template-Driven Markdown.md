---
name: template-driven-markdown
description: Create Markdown documents from repository templates and design reusable templates that agents can reliably complete. Use `.frontmatter/templates/` as the template source, treat template structure as a contract, and distinguish agent-owned slots from Front Matter CMS placeholders.
---

# Template-Driven Markdown

## Definition

Template-driven writing means the template defines the document contract:

- fixed structure and section order;
- fixed wording and front matter keys;
- writable slots and blocks;
- instructions for completing those writable areas.

The agent fills only the declared writable areas. It does not redesign the document unless the user asks to change the template itself.

This skill supports two tasks:

1. Create a Markdown document from an existing template.
1. Create or improve a template that can drive future Markdown generation.

## Template location

Use templates only from:

```text
.frontmatter/templates/
```

Search subdirectories recursively.

Front Matter CMS is optional. When `frontmatter.json` exists, use its content type and `template` connection as selection context. The skill must still work when the extension is absent.

Do not keep fallback templates inside this skill.

## Template format

A template has two regions:

```markdown
# Template Instructions

Instructions for completing this template.

--- TEMPLATE CONTENT ---

The Markdown content to generate.
```

### Template Instructions

`# Template Instructions` is template-only metadata for humans and agents.

It must explain:

- the document purpose;
- required input;
- slot and block meanings;
- structural constraints;
- omission rules;
- completion conditions.

Do not include this section or the content boundary in the generated document.

### Template Content

Everything after:

```text
--- TEMPLATE CONTENT ---
```

is the output template.

Preserve its fixed text, headings, order, front matter keys, and non-agent placeholders.

## Placeholder syntax

### Value slot

Use for a short scalar value:

```text
<<slot:key>>
```

Example:

```yaml
name: "<<slot:skill-name>>"
description: "<<slot:description>>"
```

Use stable kebab-case keys.

### Value slot with default

```text
<<slot:key|default value>>
```

Use the default only when the available context does not provide a better value.

Preserve the intended YAML type:

```yaml
enabled: <<slot:enabled|true>>
priority: <<slot:priority|1>>
```

Do not turn booleans or numbers into strings.

### Block slot

Use for paragraphs, lists, sections, or other multiline Markdown:

```text
<<block:workflow>>
```

Describe the block in `# Template Instructions`.

A block may be:

- required: replace it with meaningful Markdown;
- optional: replace it or remove it entirely.

Do not leave an empty heading merely because an optional block was removed unless the template explicitly requires that heading.

### Reserved placeholders

Double-brace placeholders are not agent-owned:

```text
{{now}}
{{title}}
{{slug}}
{{fm.owner}}
```

They may belong to Front Matter CMS or another template runtime.

Preserve `{{...}}` unless the user explicitly asks to resolve it.

## Creating a template

When asked to create or improve a template:

1. Identify the recurring document type and its stable structure.
1. Separate fixed content from variable content.
1. Put stable headings, policy text, and front matter keys in Template Content.
1. Use `<<slot:...>>` for short values.
1. Use `<<block:...>>` for content requiring judgment or multiple lines.
1. Explain every slot and block in Template Instructions.
1. Mark each block as required or optional.
1. Define what may be omitted and what must remain.
1. Add explicit completion conditions.
1. Save the template under `.frontmatter/templates/`.

### Template design rules

- Prefer a few meaningful placeholders over many sentence fragments.
- Keep instructions near the concepts they govern.
- Use visible placeholders, not HTML comments.
- Do not use `TODO`, blank headings, or ambiguous braces as placeholders.
- Do not use `{{...}}` for agent-owned values.
- Do not encode formatting, linting, or hook behavior in the template.
- Do not include facts that vary between generated documents as fixed text.
- Do not make optionality implicit.
- Avoid multiple templates with indistinguishable purposes.

### Required completion instructions

Every template must state that the generated document:

- excludes `# Template Instructions`;
- excludes `--- TEMPLATE CONTENT ---`;
- contains no unresolved `<<slot:...>>`;
- contains no unresolved `<<block:...>>`;
- preserves reserved `{{...}}` placeholders;
- preserves fixed Template Content structure.

## Generating from a template

### Template selection

Select one template in this order:

1. The exact `.frontmatter/templates/` path or filename named by the user.
1. The template linked by the applicable Front Matter CMS content type.
1. A unique template clearly matching the requested document type.
1. The only available template.

When multiple candidates remain equally plausible, ask one focused selection question. Do not choose arbitrarily.

### Workflow

1. Read the complete selected template.
1. Separate Template Instructions from Template Content.
1. Inventory all slots and blocks.
1. Determine required and optional values from Template Instructions.
1. Gather values from the user request, supplied files, and repository context.
1. Fill only declared slots and blocks.
1. Exclude Template Instructions and the content boundary from the result.
1. Preserve fixed content and reserved placeholders.
1. Write the result to the requested location.
1. Run the completion checks.

### Missing information

- Infer only values supported by the available context.
- Ask one focused question only when a required placeholder cannot be completed.
- Do not invent project facts, commands, paths, approval status, compatibility, or validation results.
- Remove an optional block only when Template Instructions permit it.
- Do not silently replace a required placeholder with vague filler.

## Front Matter CMS

When `frontmatter.json` exists:

- identify the applicable content type;
- respect its field names and value shapes;
- respect `required`, `choice`, and supported numeric range constraints;
- prefer its linked template when the user did not specify one;
- use `fmContentType` when another convention already owns `type`;
- treat `contentTypes` as a page-folder setting, not a Markdown field.

Do not claim validation beyond what Front Matter CMS expresses.

## Completion checks

Before finishing, verify:

- the source template came from `.frontmatter/templates/`;
- Template Instructions are absent from the generated document;
- the content boundary is absent;
- no `<<slot:` marker remains;
- no `<<block:` marker remains;
- every required area contains meaningful content;
- optional areas were either completed or validly removed;
- reserved `{{...}}` placeholders remain unchanged;
- fixed headings, order, wording, and front matter keys are preserved;
- no unsupported claim was introduced.

## Output

For document generation:

- create the completed Markdown file;
- report its path;
- mention only unresolved blocking input or explicit assumptions.

For template creation:

- create one reusable template under `.frontmatter/templates/`;
- ensure it follows this template format;
- report its path and intended document type.

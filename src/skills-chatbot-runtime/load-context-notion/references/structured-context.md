# Notion Structured Context

Read this reference only when the task depends on database/data-source structure, properties, relations, rollups, views, templates, linked projections, or potentially incomplete structured reads.

## Object Model

Preserve the distinctions exposed by the active Notion surface:

- A **database** is a container that can expose one or more **data sources**.
- A **data source** owns structured properties/schema and rows represented as pages.
- A database entry is also a **page**: structured properties and page body content may both matter, but they are not interchangeable.
- A **view** is a presentation/query surface over a data source. Filters, sorts, grouping, visible properties, and view type can change what the user sees without changing the underlying schema.
- A linked database/data-source surface can be a projection of an original source. Resolve the authoritative source when the active connector requires it instead of treating the projection as a separate schema owner.
- A **template** can carry repeated property defaults and page structure. Inspect it only when repeated page creation or reshaping actually depends on that template.

Do not infer unsupported Notion semantics from UI appearance alone. Prefer the object identities, types, and relationships returned by the active connector or API.

## Properties and Relations

- Use the current data-source property definitions before assigning, interpreting, querying, or changing structured values.
- Treat relation values as references to other pages/data-source items, not as copied titles or URLs.
- Preserve formula, rollup, status, date, people, and other typed-property semantics instead of flattening them into prose.
- When the task depends on a relation or rollup, resolve only the connected fields and targets needed for the current operation.

## Views

When the request names or links a specific view, load only view state that can affect the task, such as:

- filter;
- sort;
- grouping;
- visible/hidden properties;
- view type and relevant display/query configuration.

Keep view configuration distinct from data-source schema. Do not assume a view filter is an invariant of the underlying data source.

## Partial and Incomplete Reads

Treat visible results as incomplete when the active surface reports or plausibly imposes:

- pagination or cursors;
- bounded relation/reference lists;
- truncated properties;
- inaccessible related sources;
- plan- or permission-limited capabilities;
- API-version or connector-specific unsupported fields;
- separation between page metadata/properties and page body content.

Do not convert a partial read into evidence that an object, row, property, relation value, or body content does not exist.

When completeness materially affects the next action, retrieve the specific property, next page, authoritative source, page body, or other narrow follow-up context needed to resolve it.

## Load Conditions

Use this reference for the relevant section only:

- **Database/data-source work** → resolve the concrete data source and relevant property definitions.
- **View-specific work** → resolve the exact view and the configuration that affects the request.
- **Relation/rollup work** → resolve the target and check whether the returned value is complete enough for the conclusion.
- **Repeated page creation** → inspect an applicable template only when one is known and available.
- **Linked projection** → resolve the original/authoritative source when the active surface distinguishes it.

Do not load every row, related page, template, sibling object, data source, or view by default.

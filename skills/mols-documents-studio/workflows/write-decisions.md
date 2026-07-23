# Workflow: Write Decisions

## Goal

Write or append an Architecture Decision Record (ADR) using the `decisions-lite` template.

## Parameters

- **Target Path**: Absolute path of the decisions document (typically `docs/skills/<skill-name>/decisions.md`).
- **Category**: Document category (e.g., `design`, `code-style`, `documentation`).
- **Title**: A concise summary of the decision (max 50 chars).
- **Status**: Target status section (`proposed`, `accepted`, `superseded`, `deprecated`).
- **Decision Detail**: Action-oriented decision statement.
- **Reason Detail**: Core motivation/background constraint.
- **Impact Detail**: System consequence/future consequence.
- **Related**: Optional link or reference to other ADRs (omit if not highly relevant).

## Procedure

1. **Read Document or Initialize**:
   - Check if the target file exists.
   - If not, initialize it by copying `templates/decisions-lite.template.md` (remove placeholder comments).

2. **Compose Decision Block**:
   - Retrieve format from `templates/decisions-lite.template.md`.
   - Fill placeholders:
     - `{{category}}`: Lowercase category tag.
     - `{{title}}`: Korean translated core title.
     - `{{key_decision}}`, `{{key_motivation}}`, `{{key_consequence}}`: English technical summary phrase.
     - `{{details}}`, `{{context_and_reason}}`, `{{consequences_on_the_system_and_workflow}}`: Korean translated detail descriptions.
     - `{{related_decision}}`: Target ADR reference or `None` (preferred to omit if not highly coupled).

3. **Locate and Insert**:
   - Find the matching status heading in the target file:
     - `## Proposed` / `## Accepted` / `## Superseded` / `## Deprecated`.
   - Append the composed block directly under the heading.
   - Ensure the warning instructions (`<!-- ... -->`) from the template copy are **completely deleted** after rendering.

4. **Verify**:
   - Check that the header style matches `### **[<category>] <title>**`.
   - Check that three bullet fields are populated: `- DECISION | **...** - ...`, `- REASON | **...** - ...`, `- IMPACT | **...** - ...`.

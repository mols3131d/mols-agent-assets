# Iceberg

> Reorganizes complex answers and documents around decisions, so readers can immediately understand what to do next.

## At a Glance

Iceberg does not create new content or remove facts. It reorganizes existing information by priority, separating what is needed for the current decision from what can be reviewed later.

| Problem                                       | How Iceberg Handles It                                     |
| --------------------------------------------- | ---------------------------------------------------------- |
| The conclusion is buried in the body          | Moves the conclusion, conditions, and risks to the top     |
| Background information obscures the key point | Places actions and decisions before context                |
| The content is repetitive or verbose          | Consolidates duplication while preserving relevant details |
| Important exceptions may be omitted           | Retains assumptions, evidence, constraints, and warnings   |

## When to Use It

Use Iceberg when:

- Organizing long analyses, meeting notes, technical documents, or decision memos
- Conclusions, evidence, conditions, and risks are mixed together
- Action items or next steps are difficult to identify
- The same information needs to be more concise and easier to scan

Do not use it for short content that is already clear.

Iceberg improves presentation. It does not replace the original task or the selected workflow.

## Modes

| Mode    | Best For                                          | Output                                                                                |
| ------- | ------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `lite`  | Quickly improving structure                       | Reorders the content while preserving all relevant details                            |
| `full`  | General use                                       | Reduces repetition and separates the main flow from supporting information            |
| `ultra` | Decisions that must fit into one or two sentences | Presents only the essential conclusion and moves omitted details to a TIP or appendix |

If no mode is specified, Iceberg uses `full`.

```text
/iceberg lite
/iceberg full
/iceberg ultra
```

## Output Principles

1. Identify the decision the user needs to make or the action they need to take.
2. Present the conclusion, required conditions, and critical warnings first in a GitHub callout of no more than four lines.
3. Place actions and decisions before background information.
4. Use no more than four `##` sections. Add `###` subsections only when necessary.
5. Preserve facts, assumptions, figures, evidence, constraints, and validation results whenever they could affect the conclusion.

When relevant details are omitted from a conversation response, Iceberg may add up to six follow-up exploration suggestions in a `[!TIP]` callout.

For documents, omitted information should be preserved in an appendix or a linked document.

## Related Skills

For shorter responses or lower token usage, apply `caveman` after Iceberg.

For reducing unnecessary complexity across an entire codebase, use `ponytail` instead.

## References

- [`SKILL.md`](SKILL.md) — Execution rules followed by the agent
- [caveman](https://github.com/JuliusBrussee/caveman) — Inspiration for compressed communication
- [ponytail](https://github.com/DietrichGebert/ponytail) — Inspiration for simplification principles

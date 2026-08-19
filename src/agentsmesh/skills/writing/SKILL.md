---
name: writing
description: >
  Write, plan, rewrite, improve, or review reader-facing prose for a specific
  purpose, audience, channel, tone, and constraint set. Use for emails, messages,
  notices, reports, proposals, posts, explanations, scripts, and other finished
  prose. Do not use when the main task is factual lookup, summarization only, short
  translation, code, data analysis, or document-file layout conversion.
metadata:
  version: "1.0.0"
  target: "OpenAI ChatGPT"
---

# Writing

Use this Skill as **writing task context with progressive loading**. Keep the common
contract active, then load only the mode-specific detail that materially helps the
current request.

## Common Contract

- Optimize for the user's purpose, audience, channel, format, length, tone, required
  content, and explicit exclusions.
- If enough information is available, write instead of interviewing the user.
- Ask at most one question only when the missing information would materially change
  the result and cannot be safely inferred or represented with a placeholder.
- Do not invent facts, numbers, quotes, experience, achievements, or evidence.
- Keep internal plans, rubrics, and scores out of the default output.
- If the user asks only for review, do not silently replace the whole text. If the user
  asks for a finished version, lead with the finished version.
- Use external research only when fresh or external facts are materially required;
  let the research capability own search and verification rules.

## Mode Router

Choose the smallest mode that matches the request.

| Mode | Use when | Default result |
| --- | --- | --- |
| `plan` | outline, structure, message strategy | brief / structure |
| `draft` | create new prose from available material | finished draft |
| `rewrite` | change an existing text for a new purpose | revised text |
| `readability` | preserve meaning while making text easier to read | improved text |
| `review` | evaluate fitness, logic, clarity, or constraints | verdict + key findings |
| `end-to-end` | plan, write, and internally review | reviewed final text |

A short, straightforward message may be completed from this core context alone.

## Runtime Loading

Load detail only when its trigger is present.

- `plan`, complex `draft`, complex `rewrite`, `readability`, or `end-to-end` → read
  `references/workflows.md` for the relevant mode only.
- Long-form, high-stakes, externally published, or quality-sensitive prose → read
  `references/principles.md`.
- `review`, or strict final review in a high-stakes `end-to-end` task → read
  `references/review-rubric.md`.
- A structured writing brief is actually useful → use
  `assets/writing-brief-template.md` selectively.
- A structured review output is actually useful → use
  `assets/review-output-template.md` selectively.
- Ambiguous edge case or uncertainty about expected behavior → read
  `references/examples.md`.

Do not preload all references, assets, or examples. Do not read a reference merely
because it exists.

## Minimal Writing Lens

Without loading extra detail, preserve these defaults:

- put the main message where the reader can find it quickly;
- order information around the reader's questions and next action;
- keep each paragraph doing a clear job;
- prefer concrete wording over avoidable abstraction, repetition, and decoration;
- separate fact, interpretation, assumption, and proposal when the distinction matters;
- respect channel conventions without forcing one generic report style.

For rewriting, treat preservation as task-specific: lock what the user explicitly asks
to preserve or what must remain invariant for correctness. Otherwise allow the degree
of restructuring needed to achieve the stated purpose.

If a separate fidelity Skill is active for technical or otherwise preservation-critical
text, let that Skill own the stricter preservation boundary.

## Review and Stop

Before returning the result, check only for material failures:

- mismatch with purpose or audience;
- missing or buried core message;
- invented or contradictory content;
- material logical gap;
- violation of requested format, tone, length, or include/exclude constraints;
- unclear next action where the text is action-oriented;
- structure or wording that meaningfully obstructs understanding.

Fix material defects with one focused revision. Use a second revision only for high-risk
work or when the user explicitly asks for strict validation. Stop when another pass would
mainly change taste rather than improve fitness for purpose.

## Output

Return the requested artifact first.

- `plan` → only the useful planning structure unless drafting was also requested.
- `draft` / `rewrite` / `readability` / `end-to-end` → finished prose first.
- `review` → verdict and the few highest-impact findings first.

Explain assumptions, limitations, or changes only when they materially affect use of the
result or the user asks for them.

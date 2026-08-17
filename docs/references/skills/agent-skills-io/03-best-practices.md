# 03. Skill Creation Best Practices

## Core Principle

Do not restate general LLM knowledge. Extract procedures from real task traces, internal docs, and failure cases. Iterate via real execution. Keep workflow concise; control fragile steps strictly.

## 1. Extract Real Knowledge

- Source from: successful sequences, user corrections, runbooks, schemas, real patches, post-mortems.
- Avoid: generic web knowledge.

## 2. Refine via Execution Trace

- Test first draft. Review full trace, not just final output.
- Fix false positives (triggered when not needed).
- Fix false negatives (missed triggers).
- Remove vague instructions causing retry loops.

## 3. Context Efficiency

- Include: Project conventions, edge cases, mandatory APIs.
- Remove: General definitions, standard procedures.
- Rule: If agent works without the instruction, delete it.
- Scope: One coherent unit per skill. Not too narrow, not too broad.
- Detail: Move large docs to `references/`. Conditionally load (`If non-200 error, read api-errors.md`).

## 4. Control Levels

- High variance allowed: Give goals, allow agent discretion.
- Preferred pattern: Give default procedure + parameters.
- Strict consistency: Force exact commands/order. (Avoid menus; provide a single primary path).

## 5. Instruction Patterns

- **Gotchas**: Document non-obvious exceptions.
- **Templates**: Provide inline or in `assets/` instead of describing formats.
- **Checklists**: Use for multi-step validation.
- **Loop**: Execute -> Validate -> Fix -> Repeat.
- **Plan first**: For destructive/batch tasks, generate structured plan and validate before mutation.
- **Reusable scripts**: Wrap repetitive parsing/charting in tested scripts.

## Checklist

- [ ] Extracted from real artifacts/traces.
- [ ] Ignored general knowledge; prioritized project rules.
- [ ] Single coherent scope.
- [ ] Primary approach clear; fallbacks defined.
- [ ] Fragile steps strictly ordered/validated.
- [ ] Formats defined via concrete templates.
- [ ] Complex logic moved to scripts.

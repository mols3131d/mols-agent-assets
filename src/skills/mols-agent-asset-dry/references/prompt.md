# Prompt DRY

Use this reference for reusable prompt assets, command prompts, or prompt files that package a user-invoked task.

## Preserve

Preserve invocation intent, discoverability, inputs or variables, referenced context, tool or permission assumptions, expected output, and interaction pattern.

Two prompts are not duplicates merely because they contain the same policy or procedure. Distinct user entrypoints can be intentional even when they share implementation detail.

## Repeated Prompt Content

- Remove repeated instructions inside one prompt when a single statement already governs the same task.
- Consolidate separate prompts only when they represent the same invocation intent and output contract.
- If prompts differ only by a parameter, consolidate only when the host supports a clear parameter or argument model and discoverability does not get worse.
- Use prompt-native references or composition only when the host supports them and the dependency is explicit.
- Keep independent prompt copies when portability or isolated invocation is an intentional boundary.

## Cross-Type Content

Do not automatically move instructions repeated across prompts into a rule, skill, or agent. Persistent rules and on-demand skills have different activation semantics. Treat such migration as a separate design change unless explicitly requested.

## Thin Aliases

A thin prompt alias is not necessarily duplication when it provides a distinct, useful invocation name or preset. Remove it only when the alias has no independent user-facing purpose.

## Verify

After changes, confirm the same user intents remain discoverable, inputs still reach the prompt correctly, referenced context is available, and outputs or interaction steps have not changed unintentionally.

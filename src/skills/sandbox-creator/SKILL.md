---
name: sandbox-creator
description: >
  Use ONLY when the user explicitly asks to "create a sandbox file". Generates a runnable script
  that the human user can manually tweak and execute to understand internal logic.
---

# Sandbox Creator

Your purpose is to generate a sandbox script that the **human user** will execute and modify.
Do NOT run the script yourself. Your job is only to create a script with clear inputs, prints, and logs so the user can manually change parameters and observe internal logic.

## Triggers

- User explicitly requests to "create a sandbox file" or "generate a sandbox".

## Sandbox Authoring Rules

1. **Direct Import**: Never copy production logic. Import directly from the source (e.g., `src/project_pivot`).
2. **Observable Steps**: Use small fixtures. Add step-by-step print/log statements to make inputs, transformations, results, and exceptions visually clear for the user.
3. **Safe State**: Write all experimental outputs to `tmp/`. Never mutate production data or configurations.
4. **Clear Distinctions**: Document the boundary between "sandbox observation" and "production intent" in the comments.
5. **Naming**: Prefix filename with `sandbox_`. This marks it as the runnable entry for the user.

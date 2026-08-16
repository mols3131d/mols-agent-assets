# GitHub Instruction Discovery

Read this reference when the task has concrete repository paths, changed files, or
repository-scoped instructions that must be resolved beyond the root context.

## Ancestor Path Context

For every target path, inspect the complete ancestor chain from repository root to the
target directory. For a file, use its parent directory; for a directory, include that
directory itself.

At each relevant level, look for instruction-bearing sources that can actually govern the
current task:

- `AGENTS.md` and repository-defined variants;
- repository-defined path-specific instructions;
- override files only when the repository or tooling defines their semantics;
- `README.md` only when an applicable instruction points to it or when component purpose,
  local workflow, or navigation is materially needed to interpret the target.

For multiple target paths, compute each chain separately and reuse shared ancestors.
Do not leak scoped context from one unrelated path or repository into another.

## AGENTS.md

Treat `AGENTS.md` as an instruction candidate whose effective scope and precedence depend
on the active agent surface.

- Discover applicable `AGENTS.md` files along the root-to-target chain so nested context is
  not missed during repository inspection.
- Follow the active platform/tool's documented precedence instead of inventing a universal
  merge rule. On GitHub Copilot surfaces that support nested agent instructions, the
  nearest applicable `AGENTS.md` takes precedence over other agent-instruction files.
- Support differs across GitHub/Copilot features and clients; do not assume a nested file
  is active merely because it exists.
- Repository-declared scope may further narrow an instruction file when that convention is
  actually evidenced.
- Agent/service-specific instructions apply only when they govern the current task.

Do not infer override semantics from a filename or directory position alone.

## README.md

Treat `README.md` primarily as **context and navigation**, not as an automatic instruction
source and not as a file that must be loaded at every ancestor level.

Read only when it materially provides one of these:

- component purpose or boundary needed to interpret the target;
- local workflow or usage needed for the requested operation;
- explicit Git/GitHub rules whose normative intent and scope are clear;
- links from an applicable instruction to more authoritative required guidance.

Promote README text to an active rule only when its scope and normative intent clearly
apply to the current task. Proximity alone is not precedence.

## Repository-Level Instruction Sources

When relevant, inspect high-signal locations such as:

- root `CONTRIBUTING.md`, `DEVELOPMENT.md`, or repository governance docs;
- `.github/copilot-instructions.md`;
- `.github/instructions/**/*.instructions.md`;
- `.github/CONTRIBUTING.md`;
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or repository-defined agent instruction sources
  when the active surface supports them;
- repository-defined agent/bot instruction locations.

Apply path selectors such as `applyTo` only when the current target actually matches and
the active GitHub/Copilot surface supports that instruction type. Do not promote
tool-specific instructions into repository-wide policy without evidence.

GitHub currently exposes different instruction support across GitHub.com, IDEs, code
review, cloud agent, and CLI. Resolve the active surface before applying support or
precedence assumptions.

## Resolve Scope and Precedence

For each candidate instruction, confirm:

1. it does not conflict with higher user/system/tool constraints;
2. the active GitHub/Copilot surface supports that instruction type;
3. it actually applies to the current agent/task;
4. the target path/object is inside its declared scope;
5. it is normative instruction rather than context/reference;
6. any precedence or override semantics come from the active surface or repository, not
   from a generic assumption.

If a mutation depends on an unresolved instruction conflict, stop the mutation and expose
the conflict instead of choosing a convention from memory.

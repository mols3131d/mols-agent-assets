# GitHub Instruction Discovery

Read this reference when the task has concrete repository paths, changed files, or
repository-scoped instructions that must be resolved beyond the root context.

## Ancestor Path Context

For every target path, inspect the complete ancestor chain from repository root to the
target directory. For a file, use its parent directory; for a directory, include that
directory itself.

At each relevant level, look for:

- `AGENTS.md` and repository-defined variants;
- relevant `README.md`;
- repository-defined path-specific instructions;
- override files only when the repository or tooling defines their semantics.

For multiple target paths, compute each chain separately and reuse shared ancestors.
Do not leak scoped context from one unrelated path or repository into another.

## AGENTS.md

Treat `AGENTS.md` as an instruction candidate.

- Root `AGENTS.md` is repository-wide unless another scope is declared.
- Nested `AGENTS.md` applies to its directory and descendants unless declared otherwise.
- Load every applicable ancestor instruction from root to target; do not read only the
  nearest file.
- Follow repository/tooling-declared precedence, scope, and override semantics exactly.
- If no explicit precedence exists, only a genuinely conflicting rule on the same topic
  may use the more specifically scoped instruction as the more specific rule.
- Agent/service-specific instructions apply only when they actually govern the current
  ChatGPT task.

Do not infer override semantics from a filename alone.

## README.md

Treat `README.md` primarily as **context and navigation**, not as automatic normative
instruction.

Read only task-relevant portions such as:

- component purpose and boundary;
- local workflow or usage;
- Git/GitHub rules;
- links to more authoritative required guidance.

Promote README text to an active rule only when its scope and normative intent clearly
apply to the current task. Proximity alone is not precedence.

## Repository-Level Instruction Sources

When relevant, inspect high-signal locations such as:

- root `CONTRIBUTING.md`, `DEVELOPMENT.md`, or repository governance docs;
- `.github/copilot-instructions.md`;
- `.github/instructions/**/*.instructions.md`;
- `.github/CONTRIBUTING.md`;
- `.github/AGENTS.md` when its declared scope matches;
- repository-defined agent/bot instruction locations.

Apply path selectors such as `applyTo` only when the current target actually matches.
Do not promote tool-specific instructions into repository-wide policy without evidence.

## Resolve Scope and Precedence

For each candidate instruction, confirm:

1. it does not conflict with higher user/system/tool constraints;
2. it actually applies to the current agent/task;
3. the target path/object is inside its declared scope;
4. it is normative instruction rather than context/reference;
5. any precedence or override semantics are evidenced rather than guessed.

If a mutation depends on an unresolved instruction conflict, stop the mutation and expose
the conflict instead of choosing a convention from memory.

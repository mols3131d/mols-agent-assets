# GitHub Instruction Discovery

Read this reference when the task has concrete repository paths, changed files, or
repository-scoped instructions that must be resolved beyond the root context.

## Ancestor Path Context

For every target path, inspect the complete ancestor chain from repository root to the
target directory. For a file, use its parent directory; for a directory, include that
directory itself.

At each relevant level, look for instruction-bearing sources that can actually govern the
current task:

- `CHATBOT.md`, `AGENTS.md`, and other repository-defined variants when the active surface
  supports or the repository defines them;
- repository-defined path-specific instructions;
- override files only when the repository or tooling defines their semantics;
- `README.md` when explicitly referenced, materially needed for context, or the repository
  declares it as a fallback instruction source for the active surface.

For multiple target paths, compute each chain separately and reuse shared ancestors.
Do not leak scoped context from one unrelated path or repository into another.

## Repository-defined Chatbot Fallback

A repository may define a non-standard instruction chain for text I/O chatbot surfaces.
For `mols-agent-assets`, use this repository-local fallback when that convention governs
the current chatbot task:

```text
CHATBOT.md
  ↓ if absent
AGENTS.md
  ↓ if absent
README.md
```

- Prefer an applicable `CHATBOT.md` as the chatbot-specific Rule projection.
- If no applicable `CHATBOT.md` exists, fall back to applicable `AGENTS.md` context.
- If neither exists, treat the applicable `README.md` as the final fallback instruction
  source for that chatbot surface.
- This does not make `CHATBOT.md` a universal standard or `README.md` a universal Rule
  format. Apply the chain only when the repository declares it.
- System, user, platform, tool, permission, and other higher-authority constraints remain
  outside this repository-local fallback.

## AGENTS.md

Treat `AGENTS.md` as an instruction candidate whose effective scope and precedence depend
on the active agent surface and repository convention.

- Discover applicable `AGENTS.md` files along the root-to-target chain so nested context is
  not missed during repository inspection.
- Follow the active platform/tool's documented precedence instead of inventing a universal
  merge rule. On GitHub Copilot surfaces that support nested agent instructions, the
  nearest applicable `AGENTS.md` takes precedence among applicable `AGENTS.md` files.
- Support differs across GitHub/Copilot features and clients; do not assume a nested file
  is active merely because it exists.
- Repository-declared scope may further narrow an instruction file when that convention is
  actually evidenced.
- Agent/service-specific instructions apply only when they govern the current task.

Do not infer override semantics from a filename or directory position alone.

## README.md

Treat `README.md` primarily as **context and navigation** unless the repository explicitly
defines it as a fallback instruction source for the active surface.

Read when it materially provides one of these:

- component purpose or boundary needed to interpret the target;
- local workflow or usage needed for the requested operation;
- explicit Git/GitHub rules whose normative intent and scope are clear;
- links from an applicable instruction to more authoritative required guidance;
- a repository-declared fallback after higher-priority instruction files are absent.

Outside an explicit fallback convention, promote README text to an active rule only when
its scope and normative intent clearly apply to the current task. Proximity alone is not
precedence.

## Repository-Level Instruction Sources

When relevant, inspect high-signal locations such as:

- root `CONTRIBUTING.md`, `DEVELOPMENT.md`, or repository governance docs;
- `.github/copilot-instructions.md`;
- `.github/instructions/**/*.instructions.md`;
- `.github/CONTRIBUTING.md`;
- `CHATBOT.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or repository-defined instruction
  sources when the active surface supports them or the repository defines their use;
- repository-defined agent/bot instruction locations.

Apply path selectors such as `applyTo` only when the current target actually matches and
the active GitHub/Copilot surface supports that instruction type. Do not promote
tool-specific instructions into repository-wide policy without evidence.

GitHub currently exposes different instruction support across GitHub.com, IDEs, code
review, cloud agent, and CLI. Resolve the active surface before applying support or
precedence assumptions.

## GitHub Copilot Precedence

When the active surface follows GitHub Copilot's documented custom-instruction model,
resolve conflicts using the precedence that GitHub documents for that surface rather than
repository proximity alone.

Current GitHub documentation orders relevant instruction classes as:

1. personal instructions;
1. repository custom instructions, internally ordered as:
   1. matching path-specific `.github/instructions/**/*.instructions.md`;
   1. repository-wide `.github/copilot-instructions.md`;
   1. agent instructions such as `AGENTS.md`;
1. organization instructions.

Within `AGENTS.md` files, use the active surface's documented nested-file semantics; on
Copilot surfaces that support nested `AGENTS.md`, the nearest applicable `AGENTS.md`
wins among applicable `AGENTS.md` files. Do not infer an undocumented precedence between
different agent-instruction families such as `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`.
For example, Copilot CLI documents that it combines multiple applicable instruction files
without defining a general precedence order between all of them.

Treat this hierarchy as **GitHub Copilot-specific and time-sensitive**. A repository-local
chatbot fallback such as `CHATBOT.md → AGENTS.md → README.md` is a separate convention and
must not be misrepresented as GitHub Copilot precedence.

## Resolve Scope and Precedence

For each candidate instruction, confirm:

1. it does not conflict with higher user/system/tool constraints;
2. the active surface supports the instruction type or the repository defines the local
   projection/fallback being used;
3. it actually applies to the current agent/task;
4. the target path/object is inside its declared scope;
5. it is normative instruction, or an explicitly declared fallback source;
6. any precedence or override semantics come from the active surface or repository, not
   from a generic assumption.

If a mutation depends on an unresolved instruction conflict, stop the mutation and expose
the conflict instead of choosing a convention from memory.

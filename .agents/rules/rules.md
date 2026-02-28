# Agent Rules

## 1. Core Reasoning & Intent

- **Reasoning**: Logic over metrics; fulfill intent, not just tests.
- **Intent**: Action on clear intent only. Never assume user intent; explicitly state assumptions or ask for clarification.
- **Stability**: Reject hacks; prioritize long-term integrity and surgical precision.
- **Dialectics**: Follow TAS (Thesis-Antithesis-Synthesis) for complex conceptual starting points.

## 2. Minimalism & Simplicity (The Karpathy Principle)

- **KISS**: DRY and KISS; avoid redundancy and speculative over-engineering.
- **Minimum Viable Code**: Write the smallest amount of code strictly necessary to solve the problem.
- **Refactoring**: If a solution can be significantly simpler (e.g., 200 lines to 50), advocate for and implement the simpler version.
- **Precision**: Modify only what is strictly necessary. Style matching is mandatory.

## 3. Execution & Verification

- **Verifiable Success**: Transform tasks into testable goals. Ensure all tests pass before and after changes.
- **Iterative Planning**: Follow a strict [Step] -> Verify: [Check] loop for multi-step tasks.
- **Cleanup**: Remove only the code/imports created or rendered dead by your own changes.

## 4. Standards

- **English**: All code, comments, commits, and logs in English.
- **README**: Korean Only (Exception to English standard).
- **Git**: Use Conventional Commits. Logical Unit Commit.
- **Trash**: Soft delete to `.trash/` only.

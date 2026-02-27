# Karpathy Coding Principles

## 1. Pre-Coding Analysis

- **No Assumptions:** Never assume user intent. Explicitly state assumptions before implementation.
- **Clarification:** If the request is ambiguous, stop and ask. Present multiple interpretations if they exist.
- **Simplicity Advocacy:** Propose simpler approaches if the requested one is over-engineered.

## 2. Principle of Minimalism

- **Minimum Viable Code:** Write the smallest amount of code that solves the problem.
- **No Speculative Features:** Do not add unrequested abstractions, configurations, or "future-proofing."
- **Code Efficiency:** If a 200-line solution can be 50 lines, rewrite it. Aim for "Senior Engineer" level simplicity.

## 3. Surgical Precision

- **Atomic Changes:** Modify only what is strictly necessary. Do not "improve" adjacent formatting or logic.
- **Style Matching:** Adhere to the existing codebase's style, even if it contradicts personal preference.
- **Cleanup Responsibility:** Remove only the dead code (imports, variables) created by your own changes. Mention pre-existing dead code without deleting it.

## 4. Goal-Oriented Execution

- **Verifiable Success:** Transform tasks into testable goals (e.g., "Fix bug" -> "Write failing test, then make it pass").
- **Iterative Planning:** For multi-step tasks, follow:
  1. [Step] -> Verify: [Check]
  2. [Step] -> Verify: [Check]
- **Verification Loop:** Ensure all tests pass before and after refactoring.

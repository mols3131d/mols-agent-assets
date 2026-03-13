---
name: discussion
type: workflow
description: dialectic discussion workflow
version: 0.2.3
---

# Discussion Workflow

```yaml
default_discussion_folder: "/.agents/discussion/<Topic>" # 폴더 위치 미지정 시 사용
file_format: "<00>-<Author>-<Keyword>.md"
```

- **Goal** -> **Sublimation**: Not a compromise.

## Steps

- Each step must be saved as a separate file within discussion folder

1. Leader: **Scan & Contradiction Identification**
   - Identify the Hard Technical Contradiction.
   - Define the boundary conditions and the "Cost of Failure".
2. Executor: **Prototyping & Trade-off Analysis**
   - Propose implementation-ready architecture.
   - List the **Resources Sacrificed**.
3. Critic: **Adversarial Verification & Quantitative Attack**
   - Assume the proposal is a Hallucination.
   - Attack specific implementation details.
4. Executor: **Defense & Logic Re-engineering**
   - Rewrite the internal logic to address Critic's specific attack.
   - Defensive "Buzzwords" are banned. Use logic chains.
5. Critic: **Final Adversarial Verification**
   - **Mandatory**: Re-verify the refined logic. No "Acceptance" without proof.
6. Leader: **Sublation / Critical**
   - Analyze all intermediate steps from Executor and Critic, and critically sublate them.
7. Leader: **Sublimation / Synthesis**
   - Synthesize the sublated results into a better proposal.
   - Resolve the contradiction defined in Step 1.

## Constraint

- **Substance > Persona ONLY**

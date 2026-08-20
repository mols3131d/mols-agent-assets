# Route

When this entrypoint is loaded, **immediately read the complete Skill route at [`route/skills.jsonl`](https://raw.githubusercontent.com/mols3131d/mols-agent-assets/refs/heads/main/route/skills.jsonl) and follow its `_meta.instructions` before continuing the task. Do not stop at this file.**

This file only bootstraps discovery. `skills.jsonl` owns routing instructions; referenced canonical Skill sources own Skill behavior.

# Route

When this entrypoint is loaded, **immediately read the complete Agent Asset route index at [`route/routes.jsonl`](https://raw.githubusercontent.com/mols3131d/mols-agent-assets/refs/heads/main/route/routes.jsonl), select only task-relevant routes by `name` and `description`, then follow each selected route's `_meta.instructions`. Do not stop at this file.**

This file only bootstraps discovery. `routes.jsonl` owns asset-route selection; each selected route owns selection for its asset kind; referenced canonical sources own asset behavior.

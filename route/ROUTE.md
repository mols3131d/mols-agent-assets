# Route

If the exact canonical Agent Asset source is already known, load it directly without rediscovering it through route indexes. Otherwise read [`route/routes.jsonl`](https://raw.githubusercontent.com/mols3131d/mols-agent-assets/refs/heads/main/route/routes.jsonl), select only the relevant asset kind, and follow that route's instructions. Do not stop at this entrypoint when discovery is needed.

This file only bootstraps discovery. `routes.jsonl` owns asset-route selection; each selected route owns selection for its asset kind; referenced canonical sources own asset behavior.

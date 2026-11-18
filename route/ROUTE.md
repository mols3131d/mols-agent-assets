# Route

When you know the exact canonical source of a task-relevant Agent Asset, load it directly and skip route lookup only for that asset. If any part of the task still needs asset discovery, read [`route/routes.jsonl`](https://raw.githubusercontent.com/mols3131d/mols-agent-assets/refs/heads/main/route/routes.jsonl) and follow the relevant routes, including for other assets of the same kind. Do not stop at this entrypoint when discovery is needed.

This file only bootstraps discovery. `routes.jsonl` owns asset-route selection; each selected route owns selection for its asset kind; referenced canonical sources own asset behavior.

Routes discover task-selected Skills and Subagents. Commands are explicitly invoked and Hooks are event-driven; neither needs a route lookup to execute.

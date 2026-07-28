# Ultra

Load only for **ultra**.

- Fewest complete sentences that keep every required fact.
- Labels OK: `Context` / `Core` / `Rest` or `Cause` / `Effect` / `Action`. Each line = full fact + relation (no noun stacks).
- Complete grammar. No surface stripping.
- Density or labels raise re-read cost → full or lite.

> Core: Each request creates a new database connection; connection cost lowers performance under load.
> Action: Use a connection pool.
> Rest: Tune pool size when traffic requires it.

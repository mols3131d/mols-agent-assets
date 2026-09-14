# Rulesync

Read this reference only when the selected discovery, installation, synchronization, projection, or migration path uses Rulesync. Resolve exact options, target names, and current behavior from the official documentation before execution.

Use Rulesync when the current workspace already manages the applicable asset type through `.rulesync/` and `rulesync.jsonc`, or when the requested outcome intentionally adopts the asset into Rulesync-managed source.

- Add an external dependency: `rulesync add <source> ...`
- Resolve declared dependencies: `rulesync install`
- Project managed assets to configured targets: `rulesync generate`
- Adopt remote target-native assets: `rulesync fetch <source> --target <target>`
- Adopt target-native assets already in the workspace: `rulesync import --targets <target>`

Do not force Rulesync when it cannot preserve required semantics or supporting resources, or when a source-native path is materially simpler and more faithful.

Official documentation:

- [Rulesync Documentation](https://rulesync.dyoshikawa.com/)
- [Declarative Sources](https://rulesync.dyoshikawa.com/guide/declarative-sources.html)
- [CLI Commands](https://rulesync.dyoshikawa.com/reference/cli-commands)

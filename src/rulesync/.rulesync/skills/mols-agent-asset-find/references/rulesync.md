# Rulesync

- Add an external dependency: `rulesync add <source> ...`
- Resolve declared dependencies: `rulesync install`
- Project managed assets to configured targets: `rulesync generate`
- Adopt remote target-native assets: `rulesync fetch <source> --target <target>`
- Adopt target-native assets already in the workspace: `rulesync import --targets <target>`
- Convert between target-native formats without creating canonical Rulesync source: `rulesync convert --from <target> --to <target>`

Official documentation:

- [Rulesync Documentation](https://rulesync.dyoshikawa.com/)
- [Declarative Sources](https://rulesync.dyoshikawa.com/guide/declarative-sources.html)
- [CLI Commands](https://rulesync.dyoshikawa.com/reference/cli-commands)

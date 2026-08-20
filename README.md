# mols-agent-assets

개인적으로 사용하는 AI agent configuration asset의 canonical library입니다.

Reusable Rulesync 자산의 canonical source는 `src/rulesync/.rulesync/`에 있고, workspace configuration은 `src/rulesync/`가 소유합니다. `route/`는 native Skill discovery가 없는 runtime을 위한 derived discovery surface이며 canonical source가 아닙니다.

Repository 변경 절차는 [Development](docs/development.md)를 참고합니다. Agent-facing repository rules는 [`AGENTS.md`](AGENTS.md)가 소유합니다. 임시·전달용 non-canonical artifact는 [`inbox/`](inbox/README.md)를 사용합니다.

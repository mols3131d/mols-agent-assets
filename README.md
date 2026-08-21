# mols-agent-assets

개인적으로 반복 사용하는 AI agent configuration asset을 만들고, 관리하고, 개선하고, 여러 repository와 runtime에서 재사용하기 위한 **canonical asset library**입니다.

## Purpose

- 재사용할 Agent Skill, Rule, subagent, reference, pattern과 관련 자산을 하나의 source library에서 관리합니다.
- 대부분의 자산은 특정 project나 runtime에 불필요하게 묶이지 않는 portable form을 지향합니다.
- 특정 source framework, vendor 또는 target에 특화되어 있어도 반복 사용·배포·변형할 가치가 있으면 library asset으로 관리할 수 있습니다.
- Consumer repository에서는 이 library의 자산을 그대로 사용하거나 해당 project에 맞게 생성·조정할 수 있습니다.

## Source Model

`src/`는 이 repository가 **관리하고 재사용하는 library source**입니다. `src/` 아래의 자산은 하나의 runtime에 직접 설치된 local configuration이라는 뜻이 아니며, 다른 repository나 runtime에서 사용·배포·변형될 수 있는 관리 대상입니다.

이 repository에서만 직접 소비하는 runtime asset은 해당 framework 또는 vendor가 정의한 project-native path에 둡니다. Canonical source와 generated projection, 실제 repository-local runtime surface의 세부 경계는 각 owner 문서가 소유합니다.

## Navigation

- Rulesync source/workspace → [Rulesync](docs/references/tooling/rulesync.md)
- Repository development → [Development](docs/development/README.md)
- Documentation policy → [Documentation](docs/document/README.md)
- Agent-facing repository rules → [`AGENTS.md`](AGENTS.md)
- Cross-runtime discovery → [`route/`](route/README.md)
- Artifact workspace → [`inbox/`](inbox/README.md)

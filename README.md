# mols-agent-assets

개인적으로 반복 사용하는 AI agent configuration asset을 만들고, 관리하고, 개선하고, 여러 repository와 runtime에서 재사용하기 위한 **canonical asset library**입니다.

## Purpose

Agent Skill, Rule, subagent, reference, pattern과 관련 자산을 하나의 source library에서 관리하고, consumer repository와 runtime에서 그대로 사용하거나 필요에 맞게 조정할 수 있게 합니다.

## Vision

- **Reusable by default** — 반복해서 사용할 가치가 있는 자산을 이 repository에서 한 번 관리하고 여러 환경에서 재사용합니다.
- **Portable when practical** — 대부분의 자산은 특정 project나 runtime에 불필요하게 묶이지 않는 form을 지향하지만, portability 자체를 목적이나 필수 조건으로 만들지 않습니다.
- **Specialization is allowed** — 특정 source framework, vendor, target 또는 사용 맥락에 특화되어도 반복 사용·배포·변형할 가치가 있으면 library asset으로 관리할 수 있습니다.
- **Adapt downstream** — consumer repository에서는 canonical asset을 그대로 사용하거나 해당 project의 요구와 authority에 맞게 생성·조정합니다.

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

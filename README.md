# mols-agent-assets

반복해서 사용할 AI Agent Asset과 관련 설계 지식을 개발·관리·고도화하는 **개인 upstream library**입니다.

이 저장소는 특정 runtime 하나의 설정 모음이 아닙니다. 여러 repository와 runtime에서 다시 쓸 가치가 있는 source와 knowledge를 한 곳에 축적하고, consumer가 필요에 맞게 가져가거나 조정할 수 있게 하는 것이 목적입니다.

## Purpose

- 반복 사용 가치가 있는 Agent Asset과 관련 설계 지식을 한 곳에서 지속적으로 관리하고 개선합니다.
- 자산이 특정 project, vendor, target 또는 맥락에서 시작됐다는 이유만으로 library 밖으로 분류하지 않습니다. 다른 곳에서도 다시 사용할 가치가 있으면 library source로 관리할 수 있습니다.
- Consumer repository는 library source를 그대로 사용하거나 자신의 target, project authority와 constraints에 맞게 조정합니다.

## Vision

- **Build once, improve over time** — 반복되는 capability와 아이디어를 project마다 새로 만들기보다 하나의 library source를 장기적으로 개선합니다.
- **Portable when practical, specialized when useful** — 대부분은 portable하게 유지하되 특정 vendor, target 또는 context에 대한 specialization이 가치 있으면 그대로 보존합니다. 보편성을 위해 유용한 차이를 없애거나 억지 abstraction을 만들지 않습니다.
- **Library upstream, consumers downstream** — canonical source는 여기서 관리하고 consumer-specific adaptation은 downstream에서 소유합니다. Downstream의 adaptation도 여러 곳에서 다시 사용할 가치가 생기면 library asset으로 관리할 수 있습니다.
- **Preserve reusable design knowledge** — 좋은 Agent Asset을 다시 만들고 판단하는 데 도움이 되는 pattern, reference와 maintainer knowledge도 자산과 함께 축적합니다.

## Repository Model

| Surface | Meaning |
| --- | --- |
| `src/` | 이 repository가 관리하는 **library source**. Portable asset뿐 아니라 vendor-, target-, context-specific asset도 재사용·배포·변형할 가치가 있으면 포함할 수 있습니다. |
| `docs/references/` | 여러 작업과 repository에서 다시 참고할 수 있는 specification router, convention, pattern과 reusable knowledge |
| `docs/<asset-type>/<owner>/` | 개별 asset 또는 family를 유지보수하기 위한 maintainer documentation capsule |
| `route/` | canonical asset metadata에서 파생되는 cross-runtime discovery surface |
| `inbox/` | 아직 canonical하지 않은 research, review, handoff와 기타 working artifact |
| framework/vendor native project path | **이 repository 자체가 직접 소비하는** runtime-local asset |

여기서 `local`은 portability 등급이 아니라 **소비 범위**를 뜻합니다. 이 repository만 직접 소비하는 runtime asset이 repository-local이고, 특정 project에서 시작했거나 특정 target에 특화된 asset도 `src/`에서 관리하면 library source로서 다른 repository와 runtime에 재사용될 수 있습니다.

`src/`의 source는 authored library source이며 generated projection이나 특정 runtime에 설치된 local configuration과 구분합니다. Source authority, projection과 repository-local runtime surface의 세부 경계는 각 owner 문서가 소유합니다.

## Navigation

- Agent Asset design → [Design Principles](docs/references/common/design-principles.md)
- Agent-facing repository rules → [`AGENTS.md`](AGENTS.md)
- Repository development → [Development](docs/development/README.md)
- Documentation → [Documentation](docs/document/README.md)
- Reusable references and patterns → [References](docs/references/README.md)
- Rulesync source/workspace → [Rulesync](docs/references/tooling/rulesync.md)
- Cross-runtime discovery → [`route/`](route/README.md)
- Working artifacts → [`inbox/`](inbox/README.md)

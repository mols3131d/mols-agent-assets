# mols-agent-assets

반복해서 사용할 AI Agent Asset과 관련 설계·운용 지식을 개발·관리·고도화하는 **개인 library**이자, 이를 사용하는 repository와 runtime의 **upstream source**입니다.

## Purpose

반복해서 사용할 가치가 있는 Agent Asset과 지식을 project별 일회성 설정으로 흩어두지 않고 하나의 library에서 지속적으로 관리·개선합니다. 자산이나 지식의 출발점이 특정 project, vendor, target 또는 context여도 재사용 가치가 있으면 함께 관리할 수 있으며, consumer는 원본을 그대로 사용하거나 자신의 환경에 맞게 조정합니다.

## Vision

- **Build once, improve over time** — 반복되는 capability와 아이디어를 project마다 새로 만들기보다 하나의 library source를 장기적으로 개선합니다.
- **Portable when practical, specialized when useful** — 대부분은 portable하게 유지하되 특정 vendor, target 또는 context에 대한 specialization이 가치 있으면 그대로 보존합니다. 보편성을 위해 유용한 차이를 없애거나 억지 abstraction을 만들지 않습니다.
- **Library upstream, consumers downstream** — canonical source는 여기서 관리하고 consumer-specific adaptation은 각 consumer가 소유합니다. 그 adaptation도 여러 곳에서 다시 사용할 가치가 생기면 library asset이나 reference로 관리할 수 있습니다.
- **Preserve reusable knowledge** — 좋은 Agent Asset을 다시 만들고 agent를 운용·설계하는 데 도움이 되는 principle, pattern, reference와 maintainer knowledge도 함께 축적합니다.

## Repository Model

| Surface | Meaning |
| --- | --- |
| `src/` | 이 repository가 관리하는 **Agent Asset library source**. Portable asset뿐 아니라 vendor/target/context-specific asset도 재사용·배포·변형할 가치가 있으면 포함할 수 있습니다. |
| `docs/references/` | 이 repository와 다른 repository에서 재사용할 **knowledge library**. Agent Asset 설계 지식, reusable pattern, tooling/specification authority routing 등을 포함합니다. |
| `catalog/` | 자주 다시 찾는 외부 Agent Skill source와 canonical pattern library로 연결하는 entrypoint를 모아두는 **curated discovery surface**. 작성 원본, 설치 상태와 dependency lock은 소유하지 않습니다. |
| `docs/<asset-type>/<owner>/` | 개별 asset 또는 family를 유지보수하기 위한 maintainer documentation capsule |
| `route/` | 이 repository가 **제공하는 Agent Asset**의 canonical metadata에서 파생되는 cross-runtime discovery surface |
| `.agents/route/` | 이 repository를 관리·개발할 때 **사용하는 Agent Asset**의 repository-local discovery surface |
| `inbox/` | 아직 canonical하지 않은 research, review, handoff와 기타 working artifact |
| framework/vendor native project path | **이 repository 자체가 직접 소비하는** runtime-local asset |

여기서 `local`은 portability 등급이 아니라 **소비 범위**를 뜻합니다. 이 repository만 직접 소비하는 runtime asset이 repository-local이고, 특정 project에서 시작했거나 특정 target에 특화된 asset도 `src/`에서 관리하면 library source로서 다른 repository와 runtime에 재사용될 수 있습니다.

`src/`의 source는 authored library source이며 generated projection이나 특정 runtime에 설치된 local configuration과 구분합니다. Source authority, projection과 repository-local runtime surface의 세부 경계는 각 owner 문서가 소유합니다.

## Navigation

- 이 library의 자산과 지식 사용 → [Using This Repository](docs/using-this-repository.md)
- Curated reusable catalog → [`catalog/`](catalog/README.md)
- Reusable knowledge → [References](docs/references/README.md)
- Agent Asset 설계 지식 → [Agent Asset Design](docs/references/agent-assets/README.md)
- Reusable design patterns → [Patterns](docs/references/patterns/README.md)
- Agent-facing repository rules → [`AGENTS.md`](AGENTS.md)
- Repository development → [Development](docs/development/README.md)
- Documentation → [Documentation](docs/documentation/README.md)
- Rulesync source/workspace → [Rulesync](docs/references/tooling/rulesync.md)
- Cross-runtime discovery → [`route/`](route/README.md)
- Repository-local Agent Asset routing → [`.agents/route/`](.agents/route/ROUTE.md)
- Working artifacts → [`inbox/`](inbox/README.md)

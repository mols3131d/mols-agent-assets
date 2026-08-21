# mols-agent-assets

개인적으로 반복 사용할 AI agent configuration asset과 관련 설계 지식을 만들고, 관리하고, 개선하고, 여러 repository와 runtime에서 재사용하기 위한 **canonical library**입니다.

이 저장소의 목적은 특정 runtime 하나의 설정을 모으는 것이 아니라, **재사용할 원본을 한 곳에서 관리하고 consumer에 맞게 배포·조정할 수 있게 하는 것**입니다.

## Vision

- **Manage once, reuse many** — 반복해서 사용할 가치가 있는 자산과 지식을 하나의 canonical source에서 관리합니다.
- **Portable when practical** — 가능한 한 project와 runtime에 불필요하게 묶이지 않게 만들지만 portability 자체를 필수 조건으로 삼지 않습니다.
- **Specialize without forcing universality** — 특정 framework, vendor, target 또는 맥락에 특화된 자산도 반복 사용·배포·변형할 가치가 있으면 관리 대상입니다.
- **Adapt downstream** — consumer repository는 canonical asset을 그대로 사용하거나 자신의 요구와 authority에 맞게 조정할 수 있습니다.
- **Keep one source of truth** — authored source와 generated projection, 실제 runtime surface를 구분하고 같은 의미에 여러 canonical owner를 만들지 않습니다.

## Repository Model

| Surface | Meaning |
| --- | --- |
| `src/` | 이 repository가 관리하는 **library source**. Portable asset, vendor-specific asset, 특정 맥락에서 시작된 reusable asset 모두 포함할 수 있습니다. |
| `docs/references/` | 여러 작업과 repository에서 다시 참고할 수 있는 specification router, convention, pattern과 reusable knowledge |
| `docs/<asset-type>/<owner>/` | 개별 asset 또는 family를 유지보수하기 위한 maintainer documentation capsule |
| `route/` | canonical asset metadata에서 파생되는 cross-runtime discovery surface |
| `inbox/` | 아직 canonical하지 않은 research, review, handoff와 기타 working artifact |
| framework/vendor native project path | **이 repository 자체가 직접 소비하는** runtime-local asset |

`src/`에 있다는 사실은 특정 runtime에 설치된 local configuration이라는 뜻이 아닙니다. `src/`의 source는 이 library가 관리하는 대상이며 다른 repository나 runtime에서 그대로 사용하거나 배포·변형될 수 있습니다.

반대로 이 repository에서만 직접 실행·소비할 asset은 해당 framework 또는 vendor가 정의한 native project path에 둡니다. Source authority, projection과 repository-local runtime surface의 세부 경계는 각 owner 문서가 소유합니다.

## Navigation

- Agent-facing repository rules → [`AGENTS.md`](AGENTS.md)
- Repository development → [Development](docs/development/README.md)
- Documentation → [Documentation](docs/document/README.md)
- Reusable references and patterns → [References](docs/references/README.md)
- Rulesync source/workspace → [Rulesync](docs/references/tooling/rulesync.md)
- Cross-runtime discovery → [`route/`](route/README.md)
- Working artifacts → [`inbox/`](inbox/README.md)

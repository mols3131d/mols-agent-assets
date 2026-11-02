# mols-agent-assets

반복해서 사용할 AI Agent Asset과 설계·운용 지식을 개발하고 개선하는 **개인 라이브러리**입니다. 다른 저장소와 runtime은 이곳의 자산을 필요한 만큼 가져다 쓰는 **consumer**이며, 이 저장소는 그 원본을 관리하는 **upstream**이면서 일부 자산을 직접 사용하는 consumer이기도 합니다.

## 시작하기

| 목적 | 시작점 |
| --- | --- |
| 자산을 찾아 사용·설치하거나 다른 프로젝트에 가져오기 | [이 저장소 사용하기](docs/using-this-repository.md) |
| 에이전트가 제공 자산을 작업에 맞게 탐색하도록 하기 | [`route/ROUTE.md`](route/ROUTE.md) |
| 이 저장소를 개발·유지보수하기 | [개발 문서](docs/development/README.md)와 [`AGENTS.md`](AGENTS.md) |

## 관리 원칙

- 반복해서 유용한 자산과 지식은 프로젝트별 일회성 설정으로 흩어두지 않고 여기서 지속적으로 개선합니다.
- 이식성을 지향하되 특정 vendor·target·context에 대한 특화가 유용하면 보존합니다. 보편성을 위한 불필요한 추상화는 만들지 않습니다.
- 자산의 작성 원본은 upstream에서 관리하고, consumer별 조정은 각 consumer가 소유합니다. 여러 곳에서 다시 유용해진 조정은 라이브러리로 환원할 수 있습니다.
- 자산뿐 아니라 재사용할 만한 설계 원칙·패턴·참고 자료도 축적합니다.

## 관리와 사용

**관리**는 자산의 작성 원본을 유지·개선하는 책임이고, **사용**은 이 저장소의 작업이나 runtime에 자산을 실제로 적용하는 것입니다. 두 역할은 독립적이며 한 자산에 동시에 해당할 수 있습니다.

- **관리만** — 다른 프로젝트에서 재사용하도록 원본을 유지하지만 이 저장소 작업에서는 사용하지 않는 자산
- **사용만** — 외부에서 관리하는 Skill을 이 저장소의 의존성으로 설치·적용하는 경우
- **관리하면서 사용** — `src/`에서 관리하는 Skill을 이 저장소에서도 라우팅해 사용하는 경우

목록에 등재되거나 원본이 존재한다는 사실만으로 사용 중이라고 판단하지 않습니다. 실제 사용 여부는 해당 runtime의 routing·dependency·설정으로 확인합니다.

## 저장소 구성

| 경로 | 역할 |
| --- | --- |
| `src/` | 이 저장소가 관리하는 재사용 Agent Asset의 작성 원본. 이곳의 자산 중 일부는 이 저장소에서도 사용합니다. |
| 루트 `.rulesync/` | 이 저장소 전용 Agent Asset 작성 원본 |
| `docs/development/` | 저장소 개발 정책, Agent Asset 설계 지식, 도구·명세 참고 자료 |
| `docs/<asset-type>/<owner>/` | 자산 및 family별 유지보수 문서 |
| `catalog/` | 외부 프로젝트 등에서 재사용할 Skill·Plugin의 탐색 목록과 이 저장소가 작성하는 패턴·템플릿 |
| `route/` | 외부 consumer를 위한 제공 자산의 파생 탐색 정보 |
| `.agents/route/` | 이 저장소 작업에 사용할 자산의 탐색 정보. 직접 관리하는 자산과 외부 의존성을 모두 포함할 수 있습니다. |
| `.inbox/` | 조사·검토·계획·인계 등 작업 자료. 정본 지침이나 현재 정책으로 간주하지 않습니다. |

`catalog/`에서 관리하는 패턴·템플릿의 원본은 재사용 콘텐츠의 정본일 수 있지만, 이 저장소에 자동 적용되는 개발 규칙은 아닙니다. `.inbox/`의 내용도 별도로 채택해 해당 정본에 반영하기 전에는 작업 근거일 뿐입니다. 작성 원본·사용 연결·생성 결과의 구분은 [작성 원본과 권한](docs/development/source-authority.md)을 따릅니다.

## 더 찾아보기

- **자산과 지식** — [외부 Skill 카탈로그](catalog/README.md), [설계 패턴](catalog/patterns/README.md), [Agent Asset 설계](docs/development/agent-assets/README.md), [도구·명세 참고 자료](docs/development/tooling/README.md)
- **저장소 운영** — [개발환경](docs/development/development-environment.md), [도구 설정](docs/tools/README.md), [문서 정책](docs/documentation/README.md), [Rulesync](docs/development/tooling/rulesync.md)
- **탐색·작업 자료** — [제공 자산 라우팅](route/README.md), [저장소 내부 라우팅](.agents/route/ROUTE.md), [작업 자료](.inbox/README.md)

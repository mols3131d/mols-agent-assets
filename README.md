# mols-agent-assets

AI Agent Asset과 재사용 가능한 설계·운용 지식을 관리하는 개인 라이브러리입니다. 다른 프로젝트는 필요한 자산과 지식을 선택해 사용합니다.

## 시작하기

| 목적 | 시작점 |
| --- | --- |
| 자산·패턴을 찾아 가져오거나 사용하기 | [이 저장소 사용하기](docs/using-this-repository.md) |
| 챗봇에 제공 자산 탐색 경로 연결하기 | [제공 자산 라우트](route/ROUTE.md) |
| 이 저장소를 개발·유지보수하기 | [개발 문서](docs/development/README.md) · [에이전트 지침](AGENTS.md) |

## 재사용 경로

| 경로 | 내용 |
| --- | --- |
| [`src/`](src/) | 재사용 Agent Asset의 작성 원본 |
| [`catalog/`](catalog/) | 외부 자산 목록과 재사용 패턴·템플릿 |
| [`route/`](route/) | 챗봇을 위한 제공 자산 탐색 정보 |

원본 관리와 실제 설치·사용의 구분은 [작성 원본과 권한](docs/development/source-authority.md)을 따릅니다.

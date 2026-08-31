---
description: 문서 작업을 시작하기 전에 docs/의 상위 영역과 하위 디렉터리의 책임 경계를 정할 때 사용합니다.
---

# Documentation Layout

`docs/`는 문서가 맡은 책임과 다른 저장소로 옮겨 쓸 필요에 따라 다음 영역으로 나눕니다.

| 경로 | 역할 |
| --- | --- |
| [`using-this-repository.md`](using-this-repository.md) | 이 저장소가 관리하는 Agent Asset과 재사용 지식을 외부에서 찾고 사용하는 방법 |
| [`language.md`](language.md) | 저장소에서 쓰는 언어 정책과 Agent Asset 역할별 언어 규칙 |
| [`development/`](development/) | 이 저장소의 개발 규칙과 관행 |
| [`documentation/`](documentation/) | 이 저장소 전체에 적용되는 문서 원칙과 정책 |
| [`references/`](references/) | 여러 저장소에서 다시 쓸 수 있는 Agent Asset 설계 지식과 도구·명세 참고 자료 |
| `<asset-type>/<owner>/` | 하나의 asset 또는 family에 대한 이식 가능한 유지보수 문서 |

## Nested Directory Ownership

`docs/`의 하위 구조는 고정된 분류 체계가 아닙니다. 필요한 책임을 더 가까운 하위 책임 주체에 맡길 수 있도록 나눈 계층입니다. 경로가 깊어졌다는 이유만으로 README나 별도 문서를 만들지 않습니다.

- 이 README는 상위 영역의 안내와 하위 책임을 나누는 원칙만 다룹니다. 하위 디렉터리의 내부 구조까지 직접 정하지 않습니다.
- 하위 영역끼리의 책임 차이를 파일 구조만 보고 알기 어렵다면, 그 차이를 가장 가까운 상위 문서에서 설명합니다.
- 하위 영역에 독립적인 규칙이나 탐색 책임이 생기면 해당 영역의 문서가 자기 하위 범위만 맡습니다.
- 상위 문서는 더 깊은 하위 구조나 쉽게 다시 만들 수 있는 목록을 복제하지 않습니다. 하위 책임 주체도 필요 없는 라우팅 표나 파일 목록을 만들지 않습니다.
- 저장소 전반의 문서 원칙은 [`documentation/`](documentation/)이 계속 맡습니다. 하위 문서는 자기 범위를 구체화할 수 있지만 상위 원칙을 다시 소유하거나 재정의하지 않습니다.
- 이 구조는 특정 폴더 체계, 문서 묶음, Agent Asset 유지보수 문서 형식, 디렉터리 깊이를 강제하지 않습니다. 실제 책임에 필요할 때만 해당 범위에서 정합니다.

디렉터리 수준 문서가 필요한 조건과 저장소 전반의 배치 원칙은 [Documentation Principles](documentation/principles.md)를 따릅니다. 특정 디렉터리나 문서 유형에만 적용되는 규칙은 가장 가까운 문서 책임 주체가 맡습니다.

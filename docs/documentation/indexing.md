---
description: README의 Index와 자동 생성 INDEX.tsv를 선택하고, 범위별 탐색·생성·검증을 설계할 때 적용하는 문서 원칙입니다.
---

# Document Indexing

문서 인덱스는 **탐색에 실제 도움이 될 때만** 둡니다. 사람이 직접 관리하는 별도 index 전용 파일은 만들지 않습니다.

| 필요 | 선택 |
| --- | --- |
| 파일 경로를 이미 알고 있음 | 원본에 직접 접근 |
| 파일명과 디렉터리 탐색으로 충분함 | 별도 index 없음 |
| 사람이 선택 기준을 함께 봐야 함 | 해당 `README.md`의 작은 `Index` 섹션 |
| 후보의 `path`와 `description`을 기계적으로 찾고 싶음 | 범위별 자동 생성 `INDEX.tsv` |

## Scoped Discovery

- `INDEX.tsv`는 **자기 디렉터리의 직속 항목**만 노출합니다. 먼저 루트에서 관련 영역을 고르고 필요한 경우 하위 인덱스를 읽습니다.
- 하위 디렉터리에 인덱스가 없으면 해당 README와 경로 탐색으로 이어집니다. 인덱스를 찾기 위해 모든 디렉터리에서 중간 파일을 강제로 열지 않습니다.
- 작은 디렉터리에서도 `path`와 `description`을 잃지 않도록 필요 시 인덱스를 생성합니다. 특정 대상에서 파일 수 기준을 높였다면 해당 범위의 README·경로 탐색을 대체 수단으로 유지합니다. `docs/`의 자산별 유지보수 문서 영역은 루트에서 존재를 드러내되 하위 범위를 통째로 인덱싱하지 않습니다.
- README는 책임·선택 기준·사용법을, 인덱스는 재생성 가능한 후보 경로를 맡습니다. 원본 문서의 권한이나 설치·적용 상태를 인덱스에서 추론하지 않습니다.

## Generation

저장소 전용 [`indexes_generate.py`](../../scripts/indexes_generate.py) 하나를 `docs`·`catalog`에 재사용합니다. 일반적인 TSV 수집·frontmatter 파싱은 기존 범용 Markdown 인덱스 생성기를 재사용합니다.

| 매개변수 | 의미 |
| --- | --- |
| `--target docs` / `--target catalog` | 저장소별 확장자와 탐색 경계 preset |
| `--root PATH` | 다른 디렉터리에 재사용할 때의 대상 |
| `--extensions` | 포함할 파일 확장자 |
| `--directory-entry-files` | 디렉터리 설명의 frontmatter를 읽는 진입 파일 우선순위 |
| `--index-depth` | 인덱스를 생성할 하위 디렉터리 깊이 |
| `--depth` | 각 인덱스가 노출하는 하위 경로 깊이 |
| `--min-entries` | 루트를 제외한 인덱스 생성의 최소 항목 수 |
| `--traverse-roots` | 하위 인덱스 생성을 허용할 최상위 디렉터리 |
| `--check` | 파일을 쓰지 않고 누락·변경·불필요한 인덱스 보고 |
| `--prune` | 사용자 지정 경로에서 미생성 `INDEX.tsv`까지 정리하도록 명시적으로 허용 |

기본 정책은 **직속 항목만 노출**하고, 후보가 있는 디렉터리에는 하위 인덱스를 생성합니다. 파일 수 기준은 필요할 때 `--min-entries`로 높일 수 있습니다. 커스텀 대상도 같은 기본값을 사용하되 필요한 옵션을 넘깁니다.

저장소 `docs`·`catalog` preset은 관리 범위 내 오래된 생성 인덱스를 정리합니다. `--root`로 임의의 디렉터리를 사용할 때는 다른 작업에서 관리하는 하위 `INDEX.tsv`를 보존하며 `--prune`을 명시한 경우에만 정리합니다.

생성 결과는 직접 편집하지 않고 `mise run generated sync`로 갱신하며, `mise run generated validate`로 drift를 확인합니다.

# `AGENTS.md`

## 진입

- 현재 작업 경로에 적용되는 `AGENTS.md`와 scoped Rule을 따릅니다. 필요한 Skill은 런타임의 네이티브 발견·선택 기능을 우선 사용합니다.
- 관련 없는 지침·Skill·참고 자료는 미리 로드하지 않습니다.

## 탐색과 신뢰 경계

- `docs/`·`catalog/`에서 문서를 찾을 때 각각 [문서 인덱스](docs/INDEX.tsv)·[카탈로그 인덱스](catalog/INDEX.tsv)의 `path`와 `description`으로 후보를 좁히고, 하위 `INDEX.tsv`가 있으면 필요한 범위만 계속 탐색합니다. 경로를 이미 알면 원본을 직접 읽고, 목록이나 설명이 부족하면 해당 README와 경로 탐색으로 보완합니다.
- `.inbox/`는 작업 근거이고 `catalog/`의 등재·패턴은 자동으로 적용되는 저장소 정책이 아닙니다. 작성 원본, 설치·사용 상태, lock과 생성 결과는 [작성 원본과 권한](docs/development/source-authority.md)에 따라 구분합니다.
- 생성된 인덱스와 projection은 직접 수정하지 않습니다. 원본 변경 후 필요한 출력은 `mise run generated sync`로 갱신하고 `mise run generated validate`로 검증합니다. 목록이나 lock만으로 현재 설치·적용을 단정하지 않습니다.

## 작업별 정본

| 작업 | 필요한 진입점 |
| --- | --- |
| Agent Asset 신설·수정·리뷰·삭제 | [저장소 전용 워크플로](.rulesync/skills/repository-agent-asset-workflow/SKILL.md) · 발견이 불가능하면 [관리 절차](docs/development/agent-assets/agent-asset-management.md) |
| `catalog/patterns/` 관리 | [패턴 워크플로](.rulesync/skills/prj-workflow-pattern/SKILL.md) |
| 문서 작성·관리 | [문서 정책](docs/documentation/README.md) |
| 파일 배치·원본 선택 | [Repository Layout](docs/development/repository-layout.md) · [Source Authority](docs/development/source-authority.md) |
| 인덱스·생성물 갱신 및 검증 | [Document Indexing](docs/documentation/indexing.md) · [Validation](docs/development/validation.md) |
| Git branch·commit | [VCS / Git](docs/development/vcs-git.md) |
| GitHub Issue·PR·Review·Merge | [GitHub 정책](docs/development/github.md) · `github-context` Skill |
| 포맷·테스트·CI 등 개발 정책 | [Development](docs/development/README.md) |

Agent Asset의 작성 원본을 바꾸면 [관리 절차](docs/development/agent-assets/agent-asset-management.md)에 따라 유지보수 문서 영향을 반드시 판단하고 필요한 정본에 반영합니다. `.inbox/` 인계만으로 완료하지 않습니다.

저장소 전용 Agent Asset은 루트 `.rulesync/`, 재사용 Rulesync 원본은 `src/rulesync/.rulesync/`, 벤더 원본은 `src/<vendor>/`에서 관리합니다. 같은 의미의 작성 원본을 중복하지 않으며 [작성 원본과 권한](docs/development/source-authority.md)을 따릅니다. 외부 Skill의 설치·lock 일치 여부를 확인해야 할 때는 임의의 설치 명령을 조합하지 말고 `mise run skills-sync`를 사용합니다.

`main`은 직접 수정하지 않고 별도 브랜치에서 작업합니다.

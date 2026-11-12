# `AGENTS.md`

## 진입

- 현재 작업 경로에 적용되는 `AGENTS.md`와 scoped Rule을 따릅니다. Skill은 네이티브 발견을 우선하며 필요한 자산을 찾지 못할 때만 [저장소 내부 라우트](.agents/route/ROUTE.md)에서 선택합니다. `CHATBOT.md`는 로컬 에이전트의 필수 진입점이 아닙니다.
- 관련 없는 지침·Skill·참고 자료는 미리 로드하지 않습니다.

## 탐색과 신뢰 경계

- `docs/`·`catalog/`는 각각 [문서 인덱스](docs/INDEX.tsv)·[카탈로그 인덱스](catalog/INDEX.tsv)의 `path`와 `description`으로 후보를 좁혀 필요한 원본만 읽습니다. 누락되었거나 설명이 부족하면 해당 README와 경로 탐색으로 보완합니다.
- `.inbox/`는 작업 근거이고 `catalog/`의 등재·패턴은 자동으로 적용되는 저장소 정책이 아닙니다. 작성 원본, 설치·사용 상태, lock과 생성 결과는 [작성 원본과 권한](docs/development/source-authority.md)에 따라 구분합니다.
- `INDEX.tsv`, route 및 vendor projection은 직접 수정하지 않고 관련 원본과 생성·검증 절차를 따릅니다. 목록이나 lock만으로 현재 설치·적용을 단정하지 않습니다.

## 작업별 정본

| 작업 | 필요한 진입점 |
| --- | --- |
| Agent Asset 신설·수정·리뷰·삭제 | [저장소 전용 워크플로](.rulesync/skills/repository-agent-asset-workflow/SKILL.md) · 발견이 불가능하면 [관리 절차](docs/development/agent-assets/agent-asset-management.md) |
| `catalog/patterns/` 관리 | [패턴 워크플로](.rulesync/skills/prj-workflow-pattern/SKILL.md) |
| 문서 작성·관리 | [문서 정책](docs/documentation/README.md) |
| 파일 배치·원본 선택 | [Repository Layout](docs/development/repository-layout.md) · [Source Authority](docs/development/source-authority.md) |
| 인덱스·라우팅 생성 및 검증 | [Document Indexing](docs/documentation/indexing.md) · [Validation](docs/development/validation.md) · [내부 라우트](.agents/route/ROUTE.md) |
| Git branch·commit | [VCS / Git](docs/development/vcs-git.md) |
| GitHub Issue·PR·Review·Merge | [GitHub 정책](docs/development/github.md) · `github-context` Skill |
| 포맷·테스트·CI 등 개발 정책 | [Development](docs/development/README.md) |

`main`은 직접 수정하지 않고 별도 브랜치에서 작업합니다.

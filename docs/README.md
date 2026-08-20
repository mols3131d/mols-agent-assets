# 저장소 문서 (`docs/`)

`docs/`는 current repository guidance, 선택적 maintainer documentation과 shared reference를 보관합니다.

## 구조

| 경로 | 책임 |
| --- | --- |
| `development.md` | 변경 절차 |
| `testing.md` | 검증 위치와 evidence 수준 |
| `skills/<skill-name>/` | 실제 필요가 있는 Skill maintainer docs |
| `references/common/` | 여러 asset/workflow가 공유하는 소수의 repository-local reference |
| `references/skills/` | Skill 공통 reference |
| `references/tooling/` | tool-specific configuration과 official source router |

Rulesync schema와 target mapping은 upstream을 따르며 repository integration boundary는 [Rulesync Repository Conventions](references/common/rulesync.md)가 소유합니다. Current Rulesync 공식 문서 entrypoint는 [Rulesync Tooling Reference](references/tooling/rulesync.md)에서 찾습니다.

## Documentation Rule

- Runtime-required knowledge는 deployable source가 소유합니다.
- Maintainer docs는 durable decision, recovery knowledge 또는 source만으로 복구하기 어려운 intent가 있을 때만 만듭니다.
- 작업 로그, 완료된 migration 기록과 쉽게 재생성되는 상태는 Git history에 맡깁니다.
- Shared knowledge는 가장 좁은 authoritative owner 한 곳에 둡니다.
- 작은 reference set을 taxonomy directory로 미리 분할하지 않습니다.
- 빈 directory, placeholder 문서와 언어별 README 복제본을 만들지 않습니다.

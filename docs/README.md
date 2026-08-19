# 저장소 문서 (`docs/`)

현재 운용에 필요한 repository guidance, maintainer documentation과 shared reference를 보관합니다.

## Directory Map

| 경로 | 책임 |
| --- | --- |
| `development.md` | Rulesync canonical/derived boundary와 개발 workflow |
| `testing.md` | repository tests, Rulesync validation과 품질 검증 |
| `skills/<skill-name>/` | 특정 Skill에 실제로 필요할 때만 두는 maintainer-only 문서 |
| `references/common/` | 여러 Rulesync feature에서 공유하는 principle, authoring, convention, tooling reference |
| `references/skills/` | Skill 전체가 공유하는 reference |

Rulesync schema, feature taxonomy와 target mapping은 이 저장소 문서가 재정의하지 않습니다. Repository integration은 [Rulesync Repository Conventions](references/common/standards/rulesync-repository-conventions.md)가 소유하고, upstream Rulesync 문서를 authority로 연결합니다.

## Maintainer Documentation

`docs/<feature>/<asset-name>/`은 선택적 surface입니다. Canonical source만으로 안전하게 유지보수하기 어려울 때만 만듭니다.

- source만으로 purpose, architecture 또는 invariant를 복구하기 어렵습니다.
- refactor 과정에서 중요한 intent가 훼손될 위험이 큽니다.
- durable decision, recovery, migration 또는 compatibility 지식이 필요합니다.
- 별도 baseline이 회귀·복구 비용을 의미 있게 낮춥니다.

Runtime-required 지식은 deployable source가 소유합니다. 임시 작업 로그와 쉽게 재생성되는 상태는 durable docs로 승격하지 않습니다.

완료된 migration 계획·census·작업 보고서는 current guidance로 유지하지 않습니다. 필요하면 Git history에서 복구합니다.

Reference 파일명은 directory index인 `README.md`를 제외하고 lowercase kebab-case를 사용합니다. 미래 확장을 위한 빈 directory나 placeholder 문서는 만들지 않습니다.

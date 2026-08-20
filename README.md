# mols-agent-assets

개인적으로 사용하는 AI 에이전트·configuration 자산을 개발, 검증, 보관하는 저장소입니다.

## 구조

| 경로 | 역할 |
| --- | --- |
| `.rulesync/`, `rulesync.jsonc` | 필요할 때만 사용하는 repository-local Rulesync workspace |
| `src/rulesync/.rulesync/` | 재사용 Rulesync 자산의 canonical source |
| `src/rulesync/rulesync.jsonc` | 재사용 library workspace configuration |
| `route/` | canonical metadata에서 생성하는 cross-runtime discovery projection |
| `docs/` | maintainer documentation과 reference |
| `tests/`, `evals/` | repository verification과 behavioral/model evaluation |
| `scripts/` | automation과 validation tooling |

Repository workspace와 reusable library workspace는 서로 독립적입니다. Library를 root에 복제하거나 암묵적으로 활성화하지 않습니다.

이 저장소는 vendor/target 지원 matrix를 정의하지 않습니다. Target은 실제 projection 또는 검증 작업이 필요할 때 선택하며, generated vendor surface와 Rulesync lock state는 reusable library source로 보관하지 않습니다.

Rulesync가 이미 정의하는 schema, feature, target namespace와 projection semantics는 current Rulesync를 따릅니다. Repository-local 문서는 Rulesync가 소유하지 않는 integration convention만 정의합니다.

## 자세한 규칙

- Rulesync workspace, canonical/derived 경계와 공식 reference → [Rulesync](docs/references/tooling/rulesync.md)
- Skill authoring 관행 → [Skill Authoring Conventions](docs/references/skills/skill-authoring-conventions.md)
- 개발 workflow → [Development](docs/development.md)
- 검증 → [Testing](docs/testing.md)
- cross-runtime discovery → [`route/README.md`](route/README.md)

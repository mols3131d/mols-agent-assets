# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

Rulesync가 표현할 수 있는 자산은 `src/rulesync/`의 **격리된 native workspace**에서 관리합니다. Canonical schema, feature taxonomy와 target projection은 current Rulesync를 따르며 repository-local 표준으로 다시 정의하지 않습니다.

## Source Map

| 경로 | 역할 |
| --- | --- |
| `src/rulesync/rulesync.jsonc` | Rulesync target과 feature configuration |
| `src/rulesync/.rulesync/` | Rulesync canonical source |
| `route/` | Rulesync native discovery가 없는 runtime을 위한 derived discovery metadata |
| `tests/` | deterministic repository verification |
| `evals/` | behavioral/model eval과 cross-asset regression contract |
| `docs/` | maintainer documentation과 reference |
| `scripts/` | automation, validation, synchronization tooling |

현재 Rulesync features는 `rules`, `skills`, `subagents`입니다. 새 자산은 별도 repository taxonomy를 만들기보다 Rulesync의 native feature와 source shape를 우선합니다.

Repository root의 `.rulesync/`와 `rulesync.jsonc`, 생성된 `.github/`·`.agents/` target surface는 distribution source가 아닙니다. 이 저장소가 보관한 자산이 저장소 자체의 runtime configuration으로 자동 활성화되지 않도록 canonical workspace를 `src/rulesync/` 아래에 격리합니다.

`route/`도 canonical source가 아닙니다. Cross-runtime discovery contract는 [`route/README.md`](route/README.md)가 소유합니다.

## Authority

- Rulesync integration과 canonical/derived boundary → [Rulesync Repository Conventions](docs/references/common/standards/rulesync-repository-conventions.md)
- Skill authoring 관행 → [Skill Authoring Conventions](docs/references/skills/skill-authoring-conventions.md)
- Agent Skills external specification과 vendor links → [Agent Skills Specification](docs/references/skills/agent-skills-io/agent-skills-io-specification.md)
- 개발 workflow → [Development](docs/development.md)
- 검증 → [Testing](docs/testing.md)

Rulesync가 이미 소유하는 field, target namespace, projection path와 capability mapping을 이 저장소 문서에 복제하지 않습니다.

## Workflow

```text
src/rulesync/.rulesync 편집
  → Markdown format
  → src/rulesync에서 doctor / dry-run
  → write-producing generation은 temporary workspace copy에서 검증
  → repository test / applicable eval
  → canonical source review
```

Rulesync가 표현하지 못하는 semantics가 실제로 필요할 때만 `src/rulesync/`의 peer custom source를 검토합니다.

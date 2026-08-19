# mols-agent-assets

개인적으로 사용했거나 사용 중이거나 앞으로 사용할 수 있는 AI 에이전트·configuration 자산을 개발, 검증 및 보관하는 저장소입니다.

이 저장소의 재사용 자산은 `src/rulesync/.rulesync/`에서 생성·편집·리뷰·평가하는 **canonical authoring source**로 관리하고, 실제 사용은 Rulesync가 투영한 각 vendor의 runtime surface에서 이루어지는 것으로 취급합니다.

```text
src/rulesync/.rulesync/
  author / edit / review / evaluate
            ↓ Rulesync
<vendor>/...
  consume / run
```

`<vendor>/...`는 개념적인 usage surface입니다. 실제 경로와 semantics는 Rulesync와 해당 target이 정하며, 이 저장소는 vendor별 projection path를 별도 표준으로 정의하지 않습니다.

## Source Map

| 경로 | 역할 |
| --- | --- |
| `.rulesync/`, `rulesync.jsonc` | 이 repository 자체를 위한 optional Rulesync workspace |
| `src/rulesync/rulesync.jsonc` | 재사용 asset library의 Rulesync workspace configuration. Committed config는 vendor target을 선택하지 않음 |
| `src/rulesync/.rulesync/` | 재사용 자산의 canonical authoring source |
| `route/` | library asset의 cross-runtime derived discovery metadata |
| `tests/` | canonical asset을 검증하는 deterministic repository verification |
| `evals/` | canonical asset의 behavior/model evaluation과 cross-asset regression contract |
| `docs/` | maintainer documentation과 reference |
| `scripts/` | automation, validation, synchronization tooling |

Root Rulesync workspace와 library workspace는 역할이 다릅니다.

- root workspace는 이 저장소의 운영에 실제로 필요한 Rulesync 자산만 둡니다.
- `src/rulesync/` workspace는 다른 runtime에서 사용할 개인 asset library만 둡니다.
- root workspace가 필요하지 않으면 만들지 않습니다. Library를 root에 복제하거나 자동 활성화하지 않습니다.

Library workspace의 현재 Rulesync features는 `rules`, `skills`, `subagents`입니다. 새 자산은 별도 repository taxonomy를 만들기보다 Rulesync의 native feature와 source shape를 우선합니다.

이 저장소는 **지원 vendor/target matrix를 정의하지 않습니다.** Target은 특정 usage surface로 projection하거나 검증할 때 선택합니다. 개별 canonical asset의 유효한 target-specific metadata는 현재 projection 대상이 아니라는 이유만으로 제거하지 않습니다.

Rulesync가 생성한 vendor runtime surface는 canonical source가 아니며 projection output으로 commit하지 않습니다. Repository workspace와 reusable library workspace는 물리적으로 분리해 library 전체가 이 저장소의 runtime configuration으로 암묵적으로 활성화되지 않게 합니다.

`route/`도 canonical source가 아닙니다. Cross-runtime discovery contract는 [`route/README.md`](route/README.md)가 소유합니다.

## Authority

- Rulesync integration과 repository/library/usage boundary → [Rulesync Repository Conventions](docs/references/common/conventions/rulesync-repository-conventions.md)
- Skill authoring 관행 → [Skill Authoring Conventions](docs/references/skills/skill-authoring-conventions.md)
- Agent Skills external specification과 vendor links → [Agent Skills Specification](docs/references/skills/agent-skills-io/agent-skills-io-specification.md)
- 개발 workflow → [Development](docs/development.md)
- 검증 → [Testing](docs/testing.md)

Rulesync가 이미 소유하는 field, target namespace, projection path와 capability mapping을 이 저장소 문서에 복제하지 않습니다.

## Workflow

Reusable library asset:

```text
src/rulesync/.rulesync 에서 author/edit
  → canonical format / configuration 검사
  → repository test / applicable eval
  → 필요할 때 target을 선택해 temporary projection 검증
  → vendor runtime surface에서 consume
```

평가 fixture와 test code는 deployable asset package 밖의 `tests/`, `evals/`에 두되 평가 대상의 authority는 `src/rulesync/.rulesync/`의 canonical asset입니다.

Repository-level Rulesync asset이 필요하면 root `.rulesync/`에서 별도로 관리하고 library lifecycle과 독립적으로 다룹니다.

Rulesync가 표현하지 못하는 semantics가 실제로 필요할 때만 `src/rulesync/`의 peer custom source를 검토합니다.

# 자산 개발 가이드

## Directory Roles

- root `.rulesync/`, `rulesync.jsonc`: 이 repository 자체를 위한 optional Rulesync workspace.
- `src/rulesync/rulesync.jsonc`: reusable asset library의 Rulesync workspace configuration. Committed config는 vendor target을 선택하지 않습니다.
- `src/rulesync/.rulesync/`: reusable asset의 canonical authoring source.
- `src/rulesync/.rulesync/rules/`: Rulesync Rule source.
- `src/rulesync/.rulesync/skills/`: Rulesync Skill source.
- `src/rulesync/.rulesync/subagents/`: Rulesync Subagent source.
- `src/rulesync/`의 peer source: Rulesync가 표현하지 못하는 실제 required semantics만 예외적으로 유지.
- `route/`: canonical Skill metadata에서 생성되는 cross-runtime discovery projection.
- `tests/`: canonical asset의 deterministic repository verification.
- `evals/`: canonical asset의 behavioral/model eval과 cross-asset regression contract.
- `docs/skills/<skill-name>/`: 특정 Skill에 필요할 때만 두는 maintainer documentation.
- `docs/references/`: shared convention, principle과 external reference routing.

Rulesync-managed source의 schema, feature name과 target namespace는 current Rulesync를 따릅니다. Repository-local abstraction으로 다시 정의하지 않습니다.

Repository workspace와 reusable library workspace의 경계는 [Rulesync Repository Conventions](references/common/conventions/rulesync-repository-conventions.md)가 소유합니다.

## Asset Lifecycle

이 저장소가 보관하는 reusable asset은 `src/rulesync/.rulesync/`에서 생성·편집·리뷰·평가합니다. 실제 사용은 Rulesync가 투영한 vendor runtime surface에서 이루어지는 것으로 취급합니다.

```text
src/rulesync/.rulesync/
  author / edit / review / evaluate
            ↓ Rulesync
<vendor>/...
  consume / run
```

`<vendor>/...`는 실제 repository path 규칙이 아니라 usage surface를 나타내는 개념적 표기입니다. 실제 projection path와 semantics는 Rulesync와 해당 target contract를 따릅니다.

평가 fixture와 test code는 `tests/`, `evals/`에 두되 평가 대상의 authority는 canonical asset입니다. Generated vendor projection은 source로 보관하지 않습니다.

## Rulesync-Native Authoring

새 자산을 만들 때 먼저 적절한 Rulesync feature가 있는지 확인합니다.

1. Rulesync가 표현할 수 있으면 native feature와 canonical shape를 사용합니다.
1. target-specific behavior가 필요하면 해당 Rulesync target namespace를 사용합니다.
1. Rulesync가 표현할 수 없고 실제 요구가 있을 때만 custom source를 검토합니다.

Repository-local superset schema, manual projection layer나 parallel taxonomy를 만들지 않습니다.

이 저장소는 supported vendor/target 목록을 유지하지 않습니다. 개별 asset의 target-specific section은 그 asset의 의미이며, repository projection target은 아닙니다.

### Skills

Canonical Skill은 다음 경로에서 시작합니다.

```text
src/rulesync/.rulesync/skills/<skill-name>/SKILL.md
```

Single-file 기본, supporting resource, maintainer documentation과 naming 같은 개인 관행은 [Skill Authoring Conventions](references/skills/skill-authoring-conventions.md)가 소유합니다.

## Maintainer Documentation

Maintainer docs는 기본 산출물이 아닙니다. Canonical source만으로 안전하게 유지보수하기 어렵거나 durable decision·recovery knowledge가 실제로 필요할 때만 만듭니다.

- runtime-required knowledge는 deployable source가 소유합니다.
- 임시 작업 로그와 쉽게 재생성되는 상태는 durable docs로 승격하지 않습니다.
- 완료된 migration 계획과 보고서는 current guidance에서 제거하고 Git history에 맡깁니다.
- shared knowledge는 가장 좁은 `docs/references/` owner가 소유합니다.

### README Convention

Directory entry document가 필요하면 `README.md` 하나만 두고 한국어를 기본으로 작성합니다. 언어별 README 복제본은 만들지 않습니다. 제품명, 표준명, path, code, API identifier와 영어가 더 정확한 기술 용어는 원문을 유지할 수 있습니다.

## Workflow

1. `<owner>/<type>/<topic>` branch에서 작업합니다.
1. Reusable Rulesync asset은 `src/rulesync/.rulesync/`의 native feature path에서 작성하거나 수정합니다.
1. 필요한 repository test/eval로 canonical asset을 검증합니다.
1. Markdown은 repository rumdl policy에 맞춰 format합니다.
1. Canonical configuration은 `src/rulesync/`에서 `doctor --strict`로 검사합니다.
1. 실제 target usage가 중요할 때만 target을 invocation에서 선택해 projection/runtime을 검증합니다.
1. Write-producing generation은 temporary workspace에서만 수행하고 결과를 폐기합니다.
1. Canonical source를 최종 검토합니다. Generated vendor projection과 Rulesync lock state는 library source로 commit하지 않습니다.

Repository-level Rulesync asset이 필요한 경우에는 root workspace에서 별도로 관리하고 이 workflow와 혼합하지 않습니다.

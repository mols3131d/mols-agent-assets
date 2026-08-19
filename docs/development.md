# 자산 개발 가이드

Rulesync workspace와 source ownership은 [Rulesync Repository Conventions](references/common/conventions/rulesync-repository-conventions.md)가 소유합니다. 이 문서는 **변경 절차**만 다룹니다.

## Placement

- Reusable Rulesync asset → `src/rulesync/.rulesync/`
- Repository-specific Rulesync asset → 실제 필요가 있을 때만 root `.rulesync/`
- Deterministic verification → `tests/`
- Behavioral/model evaluation → `evals/`
- Durable maintainer knowledge → 필요한 경우에만 `docs/`
- Cross-runtime discovery projection → `route/`

Rulesync가 표현할 수 없는 실제 required semantic만 custom source 후보입니다.

## Rulesync-Native Authoring

1. 먼저 current Rulesync가 표현하는 feature와 canonical shape를 확인합니다.
1. Target-specific behavior는 해당 Rulesync target namespace를 사용합니다.
1. Repository-local superset schema, manual projection layer 또는 parallel taxonomy를 만들지 않습니다.

### Skills

Canonical Skill entrypoint는 `src/rulesync/.rulesync/skills/<skill-name>/SKILL.md`입니다. Single-file 기본, supporting resource, naming과 maintainer docs 관행은 [Skill Authoring Conventions](references/skills/skill-authoring-conventions.md)가 소유합니다.

## Maintainer Documentation

Maintainer docs는 기본 산출물이 아닙니다.

- Runtime-required knowledge는 deployable asset이 소유합니다.
- Durable decision, recovery knowledge 또는 source만으로 복구하기 어려운 intent만 별도 문서로 보존합니다.
- 작업 로그, 완료된 migration 기록과 쉽게 재생성되는 상태는 Git history에 맡깁니다.
- Shared knowledge는 가장 좁은 `docs/references/` owner가 한 번만 소유합니다.

Directory entry document가 필요하면 `README.md` 하나를 기본으로 합니다. 언어별 README 복제본은 만들지 않습니다.

## Workflow

1. `<owner>/<type>/<topic>` branch에서 작업합니다.
1. 올바른 canonical source를 수정합니다.
1. 가장 작은 관련 test/eval을 실행합니다.
1. Library Rulesync configuration은 `src/rulesync/`에서 `doctor --strict`로 검사합니다.
1. Target-specific 성공 조건이 있을 때만 target을 선택해 temporary projection/runtime을 검증합니다.
1. Canonical source와 durable docs만 최종 검토합니다. Generated projection과 일회성 작업 기록은 source로 남기지 않습니다.

# 자산 개발 가이드

Rulesync workspace와 source ownership은 [Rulesync](references/tooling/rulesync.md)가 소유합니다. 이 문서는 **repository-local 변경 절차와 배치 결정**만 다룹니다.

## Placement

- Reusable Rulesync asset → `src/rulesync/.rulesync/`
- Repository-specific Rulesync asset → 실제 필요가 있을 때만 root `.rulesync/`
- Deterministic verification → `tests/`
- Behavioral/model evaluation → `evals/`
- Durable development decision/rationale → `docs/development/`
- Durable maintainer knowledge → 필요한 경우에만 `docs/`
- Temporary / handoff artifact → `inbox/YYYY-MM-DD/`
- Retained non-canonical artifact → `inbox/archive/YYYY-MM-DD/`
- Cross-runtime discovery projection → `route/`

Rulesync가 표현할 수 없는 실제 required semantic만 custom source 후보입니다.

### Skills

Canonical Skill entrypoint는 `src/rulesync/.rulesync/skills/<skill-name>/SKILL.md`입니다. Single-file 기본, supporting resource, naming과 maintainer docs 관행은 [Skill Authoring Conventions](references/skills/skill-authoring-conventions.md)가 소유합니다.

## Maintainer Documentation

Maintainer docs는 기본 산출물이 아닙니다.

- Runtime-required knowledge는 deployable asset이 소유합니다.
- Durable decision, recovery knowledge 또는 source만으로 복구하기 어려운 intent만 별도 문서로 보존합니다.
- 작업 artifact의 lifecycle은 [`inbox/README.md`](../inbox/README.md)를 따릅니다.
- Shared knowledge는 가장 좁은 `docs/references/` owner가 한 번만 소유합니다.
- Directory-level README는 child source만으로 복구하기 어려운 contract나 navigation decision을 실제로 소유할 때만 둡니다. Sibling 문서를 열거하기 위한 index-only README는 만들지 않습니다.
- 언어별 README 복제본은 만들지 않습니다.

Durable development decisions:

- [Authority Routing](development/authority-routing.md) — standard/tool/target authority와 local delta의 관계
- [Documentation Ownership](development/documentation-ownership.md) — repository entrypoint, directory documentation과 knowledge/artifact lifecycle의 ownership

## Workflow

1. `<owner>/<type>/<topic>` branch에서 작업합니다.
1. 올바른 canonical source를 수정합니다.
1. 검증 범위와 evidence 수준은 [Testing](testing.md)에 맡깁니다.
1. Canonical source, durable docs와 필요한 artifact lifecycle만 최종 검토합니다. Generated projection을 reusable source로 남기지 않습니다.

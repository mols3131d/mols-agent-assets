---
title: Skill Authoring Conventions
description: Rulesync canonical Skill에 적용하는 repository-local authoring convention
---

# Skill Authoring Conventions

이 문서는 Rulesync가 소유하지 않는 **repository-local Skill authoring convention**만 정의합니다.

Canonical Skill schema와 target namespace는 current Rulesync가 소유합니다. Agent Skills 또는 vendor/harness contract가 필요한 경우 해당 공식 specification을 따릅니다.

## Canonical Package

Rulesync-managed Skill은 다음 경로에서 시작합니다.

```text
src/rulesync/.rulesync/skills/<skill-name>/SKILL.md
```

Canonical front matter는 Rulesync schema를 그대로 사용합니다. Target-specific field는 의미가 있는 해당 Rulesync target section에 둡니다. `agentsskills:`는 Agent Skills target section이며 repository-wide shared metadata namespace로 취급하지 않습니다.

이 저장소가 현재 특정 target으로 projection하지 않는다는 이유만으로 유효한 과거 또는 향후 target-specific metadata를 제거하지 않습니다.

Repository-local shared passthrough schema를 추가하지 않습니다.

## Single-File by Default

`SKILL.md` 하나로 activation과 runtime behavior가 완결되면 single-file package로 유지합니다.

- 파일 길이만으로 supporting file을 만들지 않습니다.
- chatbot/agent 또는 flat/runtime을 별도 Skill taxonomy로 사용하지 않습니다.
- 실제 runtime resource가 필요할 때만 package를 확장합니다.

Single-file Skill에서는 top-level `#` heading을 독립적인 Markdown responsibility boundary처럼 사용할 수 있습니다.

- 모든 heading은 하나의 명확한 책임을 가집니다.
- `##` 이하는 부모 책임을 점진적으로 분해합니다.
- 같은 depth는 가능한 한 비슷한 추상화 수준을 유지합니다.
- 공통 invariant는 가장 가까운 공통 상위 boundary에 한 번만 둡니다.
- 의미 없는 미세 분할은 하지 않습니다.

## Discovery

Skill selection 정보는 canonical `description`에 집중합니다. Capability, 적용 상황과 중요한 negative boundary를 구분할 수 있어야 합니다.

Prerequisite, fallback, handoff와 execution order 같은 orchestration은 body가 소유합니다. Body는 Skill이 이미 선택되어 로드되었다고 가정합니다.

## Runtime Surface

실행에 실제로 필요할 때만 package를 확장합니다.

```text
skill-name/
├── SKILL.md
├── references/
├── scripts/
├── assets/
└── templates/
```

- runtime behavior에 필요한 resource는 deployable package 안에 둡니다.
- repository verification 자산인 `tests/`, `evals/`, `scenarios/`, generated `results/`를 deployable package에 두지 않습니다.
- maintainer-only 문서를 runtime dependency로 숨기지 않습니다.
- nested `SKILL.md`는 별도 entrypoint로 해석될 수 있으므로 supporting template 이름으로 사용하지 않습니다.

Deterministic tests는 `tests/skills/<skill-name>/`, behavioral/model eval은 `evals/skills/<skill-name>/`이 소유합니다.

## Maintainer Documentation

특정 Skill에 durable maintainer documentation이 실제로 필요할 때만 `docs/skills/<skill-name>/`을 사용합니다.

다음과 같은 경우에만 검토합니다.

- source만으로 purpose, architecture 또는 중요 invariant를 복구하기 어렵습니다.
- refactor 과정에서 핵심 intent가 훼손될 위험이 큽니다.
- durable decision, recovery, migration 또는 compatibility 지식이 필요합니다.
- 별도 baseline이 회귀·복구 비용을 의미 있게 낮춥니다.

단순하고 self-explanatory한 Skill에는 별도 maintainer docs를 만들지 않습니다.

## Context-Only Naming

주책임이 workflow 실행이 아니라 상황별 context discovery/loading이면 `load-context-<topic>` naming을 검토합니다.

개인 관행을 범용 loader와 분리해야 할 때는 `load-context-<topic>-<owner>`를 personal overlay로 사용할 수 있습니다. 실제 구현·mutation·검증·최종 output까지 소유하는 Skill에는 `load-context-*`를 사용하지 않습니다.

## Validation

- canonical schema와 projection → Rulesync
- target artifact contract → 해당 target 공식 원문
- repository package invariant → repository deterministic tests
- trigger와 task behavior → runtime/eval evidence

Generated projection이 성공했다는 사실만으로 runtime behavior parity를 주장하지 않습니다.

## Boundary

이 문서는 single-file authoring, package responsibility, maintainer docs와 naming 같은 개인 관행만 소유합니다. Rulesync가 이미 정의한 canonical field, target mapping과 projection semantics를 복제하지 않습니다.

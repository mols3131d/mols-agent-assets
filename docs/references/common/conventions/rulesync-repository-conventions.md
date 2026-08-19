---
title: Rulesync Repository Conventions
description: Rulesync native source를 이 개인 자산 저장소에서 관리하기 위한 최소 repository-local convention
---

# Rulesync Repository Conventions

이 저장소는 Rulesync가 표현할 수 있는 자산에 **current Rulesync schema와 adapters를 그대로 사용합니다.** Rulesync가 이미 소유하는 feature taxonomy, canonical field, target namespace와 projection path를 repository-local 표준으로 다시 정의하지 않습니다.

## Authority

1. **Rulesync** — canonical source shape, feature와 target namespace, projection behavior.
1. **Target contract** — 실제 vendor runtime surface의 semantics.
1. **Repository convention** — 위 contract가 소유하지 않는 이 저장소의 integration 규칙.

빠르게 변하는 세부사항은 current upstream에서 확인합니다.

- Rulesync: <https://github.com/dyoshikawa/rulesync>
- File formats: <https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/file-formats.md>
- Configuration: <https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/configuration.md>

## Asset Lifecycle

이 저장소가 보관하는 재사용 Rulesync 자산의 lifecycle은 다음과 같습니다.

```text
src/rulesync/.rulesync/
  create / edit / review / evaluate
             ↓ Rulesync projection or installation
<vendor>/...
  consume / run
```

`src/rulesync/.rulesync/`는 **canonical authoring source**입니다. Skill, Rule, Subagent의 내용과 repository에서 수행하는 검토·평가는 이 source를 기준으로 합니다.

`<vendor>/...`는 **usage surface**를 뜻하는 개념적 표기입니다. 실제 path, filename, capability mapping과 runtime semantics는 Rulesync와 해당 target contract가 소유합니다. 이 저장소는 vendor별 projection layout을 별도 convention으로 정의하지 않습니다.

Projection output은 이 저장소의 canonical asset이 아닙니다. 필요할 때 생성·설치하여 사용하고, repository source로 보존하지 않습니다.

## Workspace Boundary

Rulesync workspace를 두 역할로 분리합니다.

```text
./
├── rulesync.jsonc          # optional repository workspace config
├── .rulesync/              # optional repository canonical assets
│
└── src/rulesync/
    ├── rulesync.jsonc      # reusable library workspace config
    └── .rulesync/          # reusable canonical authoring source
        ├── rules/
        ├── skills/
        └── subagents/
```

### Repository workspace

Root `.rulesync/`와 `rulesync.jsonc`는 **이 repository 자체를 configure/maintain하기 위한 Rulesync asset만** 소유합니다.

- 필요할 때만 만듭니다.
- `src/rulesync/.rulesync/`의 library를 mirror하지 않습니다.
- repository-specific Rule/Skill/Subagent를 reusable library에 넣지 않습니다.
- library asset lifecycle과 독립적으로 관리합니다.

### Library workspace

`src/rulesync/.rulesync/`는 다른 runtime에서 사용할 **개인 canonical asset library의 authoring source**입니다.

- reusable asset만 둡니다.
- repository maintenance policy를 넣지 않습니다.
- tests/evals가 밖에 있더라도 평가 대상의 authority는 이 canonical source입니다.
- library 전체를 root workspace로 projection하거나 복사하지 않습니다.

현재 library workspace가 사용하는 Rulesync feature는 `rules`, `skills`, `subagents`입니다. 새 feature가 필요하면 별도 repository taxonomy보다 Rulesync의 native feature와 source shape를 우선합니다.

## Target Scope

이 저장소는 **지원 vendor/target 목록을 정의하지 않습니다.** 개인적으로 사용했거나 사용 중이거나 앞으로 사용할 수 있는 canonical asset을 보관하는 것이 목적입니다.

Committed library `rulesync.jsonc`는 projection target을 선택하지 않습니다. Target 선택은 특정 usage surface로 projection하거나 검증하는 operation이 소유합니다.

개별 asset은 의미가 있는 target-specific section을 가질 수 있습니다. 과거에 사용한 metadata도 여전히 유효하다면 현재 projection 대상이 아니라는 이유만으로 제거하지 않습니다.

## Canonical and Derived Surfaces

Root `.rulesync/`와 `src/rulesync/.rulesync/`는 서로 다른 canonical source입니다. Rulesync가 생성하는 vendor runtime surface, root instruction file, lock state와 기타 projection은 derived artifact이며 projection output으로 commit하지 않습니다.

`route/`는 library canonical source가 아니라 cross-runtime discovery를 위한 derived metadata입니다. 자세한 contract는 [`route/README.md`](../../../../route/README.md)가 소유합니다.

## Native-First Decision

새 semantics를 추가할 때는 다음만 확인합니다.

1. Rulesync가 표현할 수 있는가?
1. 가능하면 native feature와 namespace를 사용합니다.
1. 표현할 수 없고 실제 요구가 있을 때만 적절한 workspace의 peer custom source를 검토합니다.

Repository-local superset schema, passthrough layer, 별도 transpiler나 manual projection semantics를 만들지 않습니다.

## Validation

Library asset은 canonical source와 실제 usage semantics를 분리해서 검증합니다.

```text
canonical asset
  → rulesync doctor --strict
  → repository deterministic test / behavioral eval
  → 필요할 때 target projection
  → target-specific runtime evidence가 필요한 claim만 usage surface에서 검증
```

Repository CI는 target을 선택하지 않고 library canonical configuration과 repository-owned invariant만 검증합니다. 특정 target behavior가 작업의 성공 조건일 때만 target을 명시해 projection/runtime 검증을 수행합니다.

Repository workspace가 존재하면 root에서 별도로 검증하며 library validation에 암묵적으로 포함하지 않습니다.

## Boundary

- library authoring/evaluation authority → `src/rulesync/.rulesync/`
- projection mechanics → Rulesync
- vendor usage/runtime semantics → 해당 target contract
- repository-local Rulesync assets → root Rulesync workspace
- repository/library separation → 이 문서
- Skill authoring 관행 → Skill-specific convention
- chatbot compatibility routing → chatbot bootstrap convention
- filesystem naming → naming convention

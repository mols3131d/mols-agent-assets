---
title: Rulesync Repository Conventions
description: Rulesync native source를 이 개인 자산 저장소에서 관리하기 위한 최소 repository-local convention
---

# Rulesync Repository Conventions

이 저장소는 Rulesync가 표현할 수 있는 자산에 **current Rulesync schema와 adapters를 그대로 사용합니다.** Rulesync가 이미 소유하는 feature taxonomy, canonical field, target namespace와 projection path를 repository-local 표준으로 다시 정의하지 않습니다.

## Authority

1. **Rulesync** — canonical source shape, feature와 target namespace, projection behavior.
1. **Target contract** — 특정 target artifact의 실제 runtime semantics가 필요할 때의 authority.
1. **Repository convention** — 위 contract가 소유하지 않는 이 저장소의 integration 규칙.

빠르게 변하는 세부사항은 current upstream에서 확인합니다.

- Rulesync: <https://github.com/dyoshikawa/rulesync>
- File formats: <https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/file-formats.md>
- Configuration: <https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/configuration.md>

## Canonical Workspace

```text
src/rulesync/
├── rulesync.jsonc
└── .rulesync/
    ├── rules/
    ├── skills/
    └── subagents/
```

`src/rulesync/.rulesync/`가 Rulesync-managed asset source입니다. Repository root에 `.rulesync/`나 `rulesync.jsonc`를 두지 않아, 보관한 distribution asset이 이 저장소 자체의 runtime configuration으로 자동 활성화되지 않게 합니다.

현재 사용하는 Rulesync feature는 `rules`, `skills`, `subagents`입니다. 새 feature가 필요하면 별도 repository taxonomy보다 Rulesync의 native feature와 source shape를 우선합니다.

## Target Scope

이 저장소는 **지원 vendor/target 목록을 정의하지 않습니다.** 개인적으로 사용했거나 사용 중이거나 앞으로 사용할 수 있는 canonical asset을 보관하는 것이 목적입니다.

Committed `rulesync.jsonc`는 projection target을 선택하지 않습니다. Target 선택은 projection/validation을 실행하는 시점의 CLI option 또는 commit하지 않는 `rulesync.local.jsonc`가 소유합니다.

개별 asset은 의미가 있는 target-specific section을 가질 수 있습니다. 과거에 사용한 metadata도 여전히 유효하다면 현재 projection 대상이 아니라는 이유만으로 제거하지 않습니다.

## Canonical and Derived Surfaces

Rulesync가 생성하는 `.github/`, `.agents/`, root instruction file, lock state와 기타 projection은 derived artifact이며 이 저장소에 source로 commit하지 않습니다.

`route/`도 canonical source가 아니라 cross-runtime discovery를 위한 derived metadata입니다. 자세한 contract는 [`route/README.md`](../../../../route/README.md)가 소유합니다.

## Native-First Decision

새 semantics를 추가할 때는 다음만 확인합니다.

1. Rulesync가 표현할 수 있는가?
1. 가능하면 native feature와 namespace를 사용합니다.
1. 표현할 수 없고 실제 요구가 있을 때만 `src/rulesync/`의 peer custom source를 검토합니다.

Repository-local superset schema, passthrough layer, 별도 transpiler나 manual projection semantics를 만들지 않습니다.

이 저장소 자체의 maintenance policy는 root `AGENTS.md`와 maintainer documentation이 소유합니다. `src/rulesync/.rulesync/rules/`에는 실제로 보관·배포할 Rule만 둡니다.

## Validation

Canonical configuration은 직접 검사하고, projection은 필요할 때 temporary workspace에서만 생성합니다.

```bash
npm run rulesync:doctor
npm run rulesync:preview -- --targets <target>
npm run rulesync:validate -- --targets <target>
```

CI의 wildcard projection smoke도 일시적인 adapter 검증일 뿐 repository support matrix를 선언하지 않습니다. Generated output은 검증 후 폐기합니다.

Repository tests는 source isolation, package boundary와 derived route처럼 **이 저장소가 추가로 소유하는 invariant만** 검증합니다. Rulesync의 schema나 target mapping을 재구현하지 않습니다.

## Boundary

- Rulesync canonical/model semantics → Rulesync
- target-specific runtime semantics → 해당 target contract
- repository integration → 이 문서
- Skill authoring 관행 → Skill-specific convention
- chatbot compatibility routing → chatbot bootstrap convention
- filesystem naming → naming convention

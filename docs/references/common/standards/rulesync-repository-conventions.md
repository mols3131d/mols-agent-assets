---
title: Rulesync Repository Conventions
description: Rulesync native model을 이 저장소에 적용하기 위한 최소 repository-local convention
---

# Rulesync Repository Conventions

이 저장소는 Rulesync가 표현할 수 있는 자산에 대해 **current Rulesync schema와 adapters를 canonical contract로 사용합니다.**

Rulesync가 이미 소유하는 feature taxonomy, canonical field, target namespace, projection path를 repository-local 표준으로 다시 정의하지 않습니다.

## Authority

Rulesync-managed 자산은 다음 authority를 따릅니다.

1. **Rulesync current schema and file formats** — canonical source shape와 target namespace.
1. **Target native contract** — 생성된 target artifact의 실제 runtime semantics.
1. **Repository convention** — 위 두 contract가 소유하지 않는 이 저장소의 integration 규칙.

이 저장소의 문서는 Rulesync의 target mapping table이나 field reference를 복제하지 않습니다. 빠르게 변하는 behavior는 current Rulesync 문서와 target 공식 원문에서 확인합니다.

- Rulesync: <https://github.com/dyoshikawa/rulesync>
- File formats: <https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/file-formats.md>
- Configuration: <https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/configuration.md>

## Canonical Workspace

Rulesync-managed distribution source는 다음 격리된 native workspace를 사용합니다.

```text
src/rulesync/
├── rulesync.jsonc
└── .rulesync/
    ├── rules/
    ├── skills/
    └── subagents/
```

현재 configured features는 `rules`, `skills`, `subagents`입니다. 새 feature가 필요하면 별도 repository taxonomy를 만들지 말고 Rulesync의 feature 이름과 native source shape를 그대로 사용합니다.

Repository root의 `.rulesync/`와 `rulesync.jsonc`는 distribution source로 사용하지 않습니다. 이 저장소가 보관한 자산이 저장소 자체의 runtime configuration으로 자동 활성화되는 것을 막기 위한 물리적 경계입니다.

## Canonical and Derived Surfaces

`src/rulesync/.rulesync/`와 `src/rulesync/rulesync.jsonc`만 Rulesync source authority입니다.

Rulesync가 생성하는 `.github/`, `.agents/`, root instruction files, lock state와 기타 target projection은 derived artifact이며 이 저장소의 canonical source로 commit하지 않습니다.

`route/`도 canonical source가 아닙니다. Rulesync native discovery를 사용할 수 없는 runtime을 위한 cross-runtime discovery projection이며 자세한 contract는 [`route/README.md`](../../../../route/README.md)가 소유합니다.

## Native-First Decision

새 자산이나 semantics를 추가할 때는 다음 순서로 판단합니다.

1. Rulesync feature와 canonical schema로 표현 가능한가?
1. 가능하면 해당 native feature와 target namespace를 사용합니다.
1. target이 일부 semantics를 표현하지 못하면 target capability limitation으로 남깁니다.
1. Rulesync가 표현하지 못하는 semantics가 실제 요구일 때만 `src/rulesync/`의 peer custom source를 검토합니다.

Portability를 이유로 repository-local superset schema, passthrough layer, 별도 transpiler를 만들지 않습니다. Rulesync가 지원하는 표현을 우선하고 custom source는 명시적 exception으로 유지합니다.

## Repository-Local Guidance

이 저장소 자체의 개발 정책은 root `AGENTS.md`와 maintainer documentation이 소유합니다. Distribution Rulesync source에 repository-local 정책을 복제하지 않습니다.

따라서 `src/rulesync/.rulesync/rules/`에는 실제로 배포할 Rule만 둡니다. 저장소를 유지보수하기 위한 지침을 배포 Rule로 만들지 않습니다.

## Validation

Read-only native validation은 `src/rulesync/`에서 직접 수행합니다.

```bash
npm run rulesync:doctor
npm run rulesync:preview
```

파일을 쓰는 generation 검증은 workspace 전체를 temporary directory로 복사한 뒤 수행합니다.

```bash
npm run rulesync:validate
```

Repository test/eval은 Rulesync가 보장하지 않는 local invariant와 behavior만 검증합니다. Rulesync 자체의 schema나 target mapping을 repository test로 재구현하지 않습니다.

## Boundary

이 문서가 소유하는 것은 **Rulesync와 이 저장소 사이의 integration boundary**뿐입니다.

- Rulesync canonical schema와 target adapters → Rulesync
- generated target semantics → 해당 target 공식 contract
- Skill authoring 관행 → Skill-specific repository convention
- chatbot compatibility routing → chatbot bootstrap convention
- filesystem naming → naming convention

외부 contract로 흡수된 규칙은 이 문서에서 중복 소유하지 않습니다.

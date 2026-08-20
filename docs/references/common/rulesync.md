---
title: Rulesync Repository Conventions
description: Rulesync native source를 이 개인 자산 저장소에서 관리하기 위한 repository-local integration boundary
---

# Rulesync Repository Conventions

이 문서는 Rulesync가 소유하지 않는 **repository integration boundary**만 정의합니다. Schema, file format, feature, target namespace와 projection behavior는 current [Rulesync](https://github.com/dyoshikawa/rulesync)가 authoritative합니다.

## Workspaces

| Workspace | 책임 |
| --- | --- |
| root `.rulesync/` + `rulesync.jsonc` | 실제 필요가 있을 때만 사용하는 repository-local Rulesync assets/configuration |
| `src/rulesync/.rulesync/` + `src/rulesync/rulesync.jsonc` | 재사용 asset library의 canonical authoring source |

두 workspace는 독립적입니다. Repository-specific asset을 reusable library에 넣지 않고, library를 root에 mirror하거나 자동 활성화하지 않습니다.

## Canonical and Derived

```text
src/rulesync/.rulesync/
  author / edit / review / evaluate
            ↓ Rulesync
runtime usage surface
  consume / run
```

- `src/rulesync/.rulesync/`가 reusable asset의 authority입니다.
- Repository verification은 `tests/`, `evals/`가 소유합니다.
- Generated vendor projection과 Rulesync lock state는 reusable source가 아닙니다.
- `route/`는 library metadata에서 파생되는 cross-runtime discovery surface이며 canonical body를 대체하지 않습니다. 세부 contract는 [`route/README.md`](../../../route/README.md)가 소유합니다.

## Target and Schema

이 저장소는 supported vendor/target matrix를 정의하지 않습니다. Target은 구체적인 projection 또는 검증 operation에서만 선택합니다. 개별 asset의 유효한 target-specific metadata는 현재 projection 대상이 아니라는 이유만으로 제거하지 않습니다.

새 semantics가 필요하면 current Rulesync가 표현하는지 먼저 확인합니다. 가능하면 native feature/namespace를 사용하고, 실제로 표현할 수 없는 요구가 있을 때만 peer custom source를 검토합니다. Repository-local superset schema나 manual projection semantics를 만들지 않습니다.

## Boundary

- runtime semantics → target contract
- Skill authoring → [Skill Authoring Conventions](../skills/skill-authoring-conventions.md)
- filesystem naming → [Naming](naming.md)
- verification → [Testing](../../testing.md)

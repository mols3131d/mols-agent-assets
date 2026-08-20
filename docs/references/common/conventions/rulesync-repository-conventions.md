---
title: Rulesync Repository Conventions
description: Rulesync native source를 이 개인 자산 저장소에서 관리하기 위한 최소 repository-local convention
---

# Rulesync Repository Conventions

이 문서는 Rulesync가 소유하지 않는 **repository integration boundary**만 정의합니다. Rulesync schema, file format, feature, target namespace와 projection behavior는 current upstream이 authoritative합니다.

## Authority

1. **Rulesync** — canonical source shape와 projection mechanics
1. **Target contract** — 실제 vendor runtime semantics
1. **Repository convention** — workspace placement, source ownership과 보존 정책

Upstream: <https://github.com/dyoshikawa/rulesync>

## Workspaces

| Workspace | 책임 |
| --- | --- |
| root `.rulesync/` + `rulesync.jsonc` | 필요할 때만 두는 repository-local configuration |
| `src/rulesync/.rulesync/` + `src/rulesync/rulesync.jsonc` | 재사용 asset library의 canonical authoring source |

두 workspace는 독립적입니다.

- Repository-specific asset을 reusable library에 넣지 않습니다.
- Reusable library를 root workspace에 mirror하거나 자동 활성화하지 않습니다.
- Root workspace가 필요하지 않으면 만들지 않습니다.

## Library Lifecycle

```text
src/rulesync/.rulesync/
  author / edit / review / evaluate
            ↓ Rulesync
runtime usage surface
  consume / run
```

`src/rulesync/.rulesync/`가 reusable asset의 authority입니다. Tests와 evals가 package 밖에 있어도 평가 대상은 canonical asset입니다.

Generated vendor projection과 Rulesync lock state는 reusable library source가 아닙니다. 필요한 작업에서 생성·검증하고 source로 보존하지 않습니다.

## Target Scope

이 저장소는 supported vendor/target matrix를 유지하지 않습니다. Committed library configuration은 target-neutral하게 두고, target 선택은 구체적인 projection 또는 검증 operation이 소유합니다.

개별 asset의 유효한 target-specific metadata는 그 asset의 의미입니다. 현재 projection 대상이 아니라는 이유만으로 제거하지 않습니다.

## Native First

새 semantics가 필요하면 다음 순서로 판단합니다.

1. Rulesync가 표현하는지 확인합니다.
1. 가능하면 native feature와 namespace를 사용합니다.
1. 표현할 수 없고 실제 요구가 있을 때만 해당 workspace의 peer custom source를 검토합니다.

Repository-local superset schema, passthrough layer 또는 manual projection semantics를 만들지 않습니다.

## Derived Surfaces

`route/`는 reusable library의 cross-runtime discovery를 위한 derived metadata입니다. Canonical asset body나 Rulesync projection을 대체하지 않습니다. 자세한 contract는 [`route/README.md`](../../../../route/README.md)가 소유합니다.

Repository verification은 `tests/`, `evals/`가 소유합니다. 검증 방법은 [Testing](../../../testing.md)을 따릅니다.

## Boundary

- reusable asset authority → `src/rulesync/.rulesync/`
- repository-local Rulesync assets → root Rulesync workspace
- projection mechanics → Rulesync
- runtime semantics → target contract
- Skill authoring 관행 → [Skill Authoring Conventions](../../skills/skill-authoring-conventions.md)
- filesystem naming → [Naming Convention](agent-assets-naming-convention.md)

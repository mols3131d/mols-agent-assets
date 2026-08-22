---
description: repository guidance와 Agent Asset에서 canonical source, upstream/local ownership, authored/derived boundary를 결정할 때 사용하는 policy입니다.
---

# Source Authority

이 문서는 repository guidance와 Agent Asset의 **source of truth와 authored source ownership**을 결정합니다.

General behavior는 실제 standard, source framework, tool 또는 target/harness가 소유하고, repository는 그 계약을 복제하지 않습니다. Repository-local policy는 local delta와 canonical source placement만 소유합니다.

## Principle

**Standard First / Local Delta Only**

Repository-local source에 남기는 것은 다음뿐입니다.

- upstream/default와 의도적으로 다른 deviation
- upstream에 없는 repository-specific extension
- upstream만으로 하나의 결정을 복원할 수 없는 ambiguity resolution

세부 계약이 필요하면 local prose snapshot을 만들지 않고 current authoritative source로 route합니다.

이 경계는 stale copy, authority ambiguity, 불필요한 context, target-specific behavior의 repository-wide 일반화를 줄이기 위한 것입니다. 단순히 "common practice"라는 이유만으로 local guard를 제거하지 않습니다. 실제 authority가 behavior를 충분히 결정할 때만 local copy를 없앱니다.

## Authority by Concern

Authority는 하나의 전역 순위가 아니라 **결정 concern별 owner**로 해석합니다.

| Concern | Authority |
| --- | --- |
| canonical authored representation | 선택한 source framework 또는 vendor-native representation |
| portable contract | 실제 적용되는 portable standard |
| target-specific runtime behavior | 실제 target/harness의 official contract |
| repository convention과 intentional delta | repository 또는 mols convention |
| asset-local requirement | 해당 asset |

먼저 어떤 concern의 결정인지 식별한 뒤 그 concern의 authority를 사용합니다. 더 local한 owner는 자기 scope의 requirement를 추가하거나 좁힐 수 있지만, upstream contract를 암묵적으로 다시 정의하지 않습니다. 의도적인 차이는 local delta로 명시합니다.

## Canonical Source

동일한 semantic asset에는 **canonical authored source를 하나만** 둡니다.

Rulesync와 vendor-native source 중 어느 쪽을 선택할지는 portability나 기능 부족 여부가 아니라 **어느 representation을 사람이 author/edit할 canonical source로 관리할지**에 따라 정합니다.

- Rulesync representation을 canonical source로 선택하면 Rulesync source를 author/edit합니다.
- vendor-native representation을 canonical source로 선택하면 vendor-native source를 author/edit합니다.
- generated projection은 authored source가 아니며 별도 canonical authority로 승격하지 않습니다.

Target-specific 결과물을 사람이 직접 수정해야 하는 요구가 반복된다면 generated copy를 병행 수정하지 말고 canonical representation 선택 자체가 맞는지 다시 검토합니다.

## Source Placement

먼저 asset이 **reusable library source인지 repository-direct runtime asset인지** 구분합니다.

| Role | Canonical authored location |
| --- | --- |
| reusable + Rulesync-authored | `src/rulesync/...` |
| reusable + vendor-native authored | `src/<vendor>/...` |
| repository-direct asset | framework/vendor가 정의한 native project path |

`src/<vendor>/`는 reusable authored source를 보관하는 repository convention이며 vendor runtime이 직접 탐색하는 project path를 대체하지 않습니다.

구체적인 내부 layout과 schema는 local superset을 만들지 않고 selected source framework 또는 vendor의 current official contract를 따릅니다.

## Derived State

Generated projection, derived discovery metadata, lock state와 같은 output/state는 **그 자체로 semantic authored source가 되지 않습니다**.

Derived artifact가 필요하면 owning source에서 다시 생성하거나 해당 artifact의 좁은 operational owner가 관리합니다. 같은 semantic behavior를 source와 projection 양쪽에서 독립적으로 유지하지 않습니다.

## Resolution

새 규칙이나 asset 배치를 결정할 때는 다음 순서로 판단합니다.

1. 어떤 behavior 또는 representation을 결정하는지 식별합니다.
2. 그 concern의 current authority를 찾습니다.
3. reusable asset이면 canonical authored representation을 하나 선택합니다.
4. repository에는 필요한 local delta와 source placement만 기록합니다.
5. 세부 계약은 해당 authoritative source로 route합니다.

## Boundary

이 문서는 Rulesync schema, Agent Skills specification, vendor behavior 또는 개별 Skill workflow를 다시 설명하지 않습니다. Current operational rule, tool integration, source registry와 asset-local workflow는 각각의 좁은 owner가 소유합니다.

# Authority Routing

이 문서는 repository guidance와 Agent Asset을 단순화할 때 적용하는 **authority routing의 durable rationale**을 기록합니다.

## Decision

Local guidance는 표준, tool, source framework 또는 target/harness가 이미 결정하는 behavior를 복제하지 않습니다. Repository-local source는 다음만 소유합니다.

- upstream/default와 의도적으로 다른 deviation
- upstream에 없는 repository-specific extension
- upstream만으로 하나의 결정을 복원할 수 없는 ambiguity resolution

세부 계약이 필요하면 local prose로 snapshot을 만들기보다 현재 authoritative source로 route합니다.

## Why

같은 의미를 여러 위치에 복제하면 다음 문제가 생깁니다.

- upstream 변경 뒤 local copy가 stale해짐
- 어느 문서가 authoritative한지 불명확해짐
- 항상 로드되는 context가 불필요하게 커짐
- target별 차이를 repository-wide rule로 오인하기 쉬움

따라서 이 저장소는 **Standard First / Local Delta Only**를 기본으로 합니다. 단순히 "common practice"라는 이유만으로 local guard를 제거하지 않습니다. 실제 표준·tool·runtime default가 behavior를 충분히 결정하는지가 기준입니다.

## Authority Order

구체적인 작업에서는 실제 source와 target을 먼저 식별하고, 적용되는 authority만 사용합니다.

1. authored source representation을 소유하는 framework
1. portable standard가 실제 적용될 때의 portable contract
1. 실제 target/harness의 official contract
1. repository 또는 mols personal convention
1. asset-local requirement

하위 authority는 상위 contract를 다시 정의하지 않습니다. Local source가 상위 contract와 다르게 행동해야 한다면 그 차이를 명시적인 local delta로 기록합니다.

## Source Placement

Authored source의 위치는 **재사용 library source인지, 이 repository가 직접 소비하는 runtime asset인지**를 먼저 구분합니다.

- Rulesync를 canonical authored source로 사용하는 reusable asset은 `src/rulesync/` 아래에서 author/edit합니다.
- 특정 vendor의 native contract를 canonical authored source로 사용하는 reusable asset은 `src/<vendor>/` 아래에서 author/edit합니다.
- 이 repository가 직접 소비하는 framework/vendor asset은 `src/`에 별도 authority를 만들지 않고 해당 framework 또는 vendor가 정의한 native project path에 둡니다.
- Generated projection은 authored source와 다릅니다. Generated output을 별도 canonical source로 취급하지 않습니다.
- 동일한 semantic asset에 Rulesync source와 vendor-native source를 동시에 canonical authority로 두지 않습니다.

Rulesync와 vendor-native source 중 어느 쪽을 선택할지는 portability나 기능 부족 여부가 아니라 **어느 representation을 그 asset의 canonical authored source로 관리할지**에 따라 정합니다. Rulesync representation을 canonical source로 선택하면 Rulesync source를, vendor의 native representation 자체를 canonical source로 선택하면 vendor-native source를 사용합니다.

구체적인 내부 layout과 schema는 local superset을 만들지 않고 해당 framework 또는 vendor의 current official contract를 따릅니다.

```text
reusable + Rulesync-authored
→ src/rulesync/...

reusable + vendor-native authored
→ src/<vendor>/...

repository-direct asset
→ <framework/vendor-defined native project path>
```

`src/<vendor>/`는 reusable authored source를 보관하기 위한 repository convention입니다. Vendor runtime이 직접 탐색하는 project path를 대체하지 않습니다.

## Boundary

이 문서는 Rulesync schema, Agent Skills specification, vendor behavior 또는 개별 Skill workflow를 다시 설명하지 않습니다. Current operational rule과 official source registry는 각각의 좁은 owner가 소유합니다.

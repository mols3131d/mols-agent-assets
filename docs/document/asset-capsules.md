# Asset Capsules

`docs/<asset-type>/<asset>/**`는 **한 자산에 대한 portable maintainer documentation capsule**로 취급합니다.

`development`, `document`, `references`, `presets`는 reserved documentation namespace이며 asset type에 포함하지 않습니다.

## Contract

각 capsule은 대응하는 자산과 함께 다른 repository로 옮겨도 이해·수정·복구에 필요한 문서 context가 유지될 정도로 self-contained해야 합니다.

- 해당 asset의 intent, invariant, maintenance, recovery와 non-obvious decision을 capsule 안에서 완결합니다.
- 다른 repository-local 문서가 없으면 의미를 복원할 수 없는 hidden dependency를 만들지 않습니다.
- Runtime behavior의 canonical source를 documentation으로 복제하지 않습니다. Capsule은 maintainer context이지 deployable source의 대체물이 아닙니다.

Capsule의 duplication boundary는 [DRY Boundaries](dry.md)가 소유합니다.

## Entrypoint

Capsule의 README 사용 여부와 entrypoint 책임은 [Documentation Ownership](ownership.md)을 따릅니다. Capsule 안에 README를 둘 경우 그 README 자체도 capsule과 함께 이동할 수 있어야 합니다.

## Portability Review

Capsule을 검토할 때 다음을 확인합니다.

- 이 directory와 대응 asset만으로 핵심 intent와 maintenance boundary를 복원할 수 있는가?
- 외부 project path, personal workspace 또는 특정 platform UI에 불필요하게 의존하는가?
- 외부 dependency가 정말 필요한 경우 그 이유와 source가 명확한가?

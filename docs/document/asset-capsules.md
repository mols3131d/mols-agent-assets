# Asset Capsules

`docs/<asset-type>/<owner>/**`는 **asset maintainer documentation capsule**로 취급합니다. `<owner>`는 하나의 asset이거나 같은 책임군의 family일 수 있습니다.

`development`, `document`, `references`는 reserved documentation namespace이며 asset type에 포함하지 않습니다.

## Ownership

- 하나의 asset에만 적용되는 maintainer knowledge는 `docs/<asset-type>/<asset>/`이 소유합니다.
- 같은 family가 공유하는 durable knowledge나 family 책임 경계는 `docs/<asset-type>/<family>/`이 한 번만 소유합니다.
- Family capsule은 runtime taxonomy, registry 또는 metadata schema가 아닙니다. 실제 runtime entrypoint와 trigger는 각 asset이 계속 소유합니다.
- Family membership을 별도 machine registry로 복제하지 않습니다. Family capsule에는 `README.md`를 두고 현재 member와 책임 경계를 사람이 읽을 수 있게 명시합니다.
- 현재 member 수만으로 family owner 여부를 결정하지 않습니다. Family 자체가 durable maintenance boundary일 때만 둡니다.

## Contract

각 capsule은 대응하는 asset 또는 family와 함께 다른 repository로 옮겨도 이해·수정·복구에 필요한 문서 context가 유지될 정도로 self-contained해야 합니다.

- 해당 owner의 intent, invariant, maintenance, recovery와 non-obvious decision을 capsule 안에서 완결합니다.
- 다른 repository-local 문서가 없으면 의미를 복원할 수 없는 hidden dependency를 만들지 않습니다.
- Runtime behavior의 canonical source를 documentation으로 복제하지 않습니다. Capsule은 maintainer context이지 deployable source의 대체물이 아닙니다.
- Runtime에 필요한 instruction, reference, script, template 또는 asset은 documentation capsule이 아니라 대응 runtime package가 소유합니다.

Capsule-specific duplication boundary는 이 문서의 Ownership과 Contract가 소유합니다. Repository-wide 중복 판단 원칙은 [DRY Boundaries](dry.md)를 따릅니다.

## Entrypoint

Asset-specific capsule의 README 사용 여부와 entrypoint 책임은 [Documentation Ownership](ownership.md)을 따릅니다.

Family capsule은 membership과 shared boundary를 설명해야 하므로 `README.md`를 entrypoint로 둡니다. README 자체도 capsule과 함께 이동할 수 있어야 합니다.

## Portability Review

Capsule을 검토할 때 다음을 확인합니다.

- 이 directory와 대응 asset 또는 family만으로 핵심 intent와 maintenance boundary를 복원할 수 있는가?
- shared knowledge가 member별 capsule에 불필요하게 복제되어 있지 않은가?
- 외부 project path, personal workspace 또는 특정 platform UI에 불필요하게 의존하는가?
- 외부 dependency가 정말 필요한 경우 그 이유와 source가 명확한가?

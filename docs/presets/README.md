# Presets

`docs/presets/`는 다른 project에 **그대로 가져가거나 최소 수정해서 적용할 수 있는 opinionated policy/profile**을 둡니다.

Preset은 설명용 reference가 아니라 이미 판단이 들어간 reusable starting point입니다. 반복해서 새 지침을 작성하는 대신 적합한 preset을 선택하고 target project의 local delta만 추가하는 것을 기본 사용법으로 합니다.

## Contract

- 각 preset은 복사하거나 외부 project에서 기반 규칙으로 사용할 수 있을 정도로 독립적으로 이해 가능해야 합니다.
- 특정 repository path, private workspace, vendor UI 같은 불필요한 host dependency를 만들지 않습니다.
- Target project가 preset을 채택하면 그 project의 local authority와 explicit instruction이 우선합니다.
- Project-specific deviation은 preset 원본을 억지로 일반화하기보다 target project에 local delta로 기록합니다.
- 원리·배경·비교 자료가 필요하면 `docs/references/`를 사용할 수 있지만, preset 적용에 필요한 핵심 규칙을 reference에 숨기지 않습니다.

## Preset vs Reference

- `presets/` — 바로 적용할 수 있는 선택된 규칙·관행의 묶음
- `references/` — 판단, 비교, 설계와 재사용을 위한 참고 지식

Preset이 이 repository의 operational rule이 되는 것은 아닙니다. 이 repository에 실제 적용되는 규칙은 해당 project documentation 또는 canonical source가 소유합니다.

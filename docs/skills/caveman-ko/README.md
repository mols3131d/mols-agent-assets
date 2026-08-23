---
description: caveman-ko Skill의 provenance, maturity boundary와 promotion criteria를 보존하는 experimental maintainer context입니다.
---

# caveman-ko

Status: **Experimental**.

`caveman-ko`는 MIT license의 [`JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman) response Skill을 한국어 사용 환경에 맞게 실험적으로 조정한 자산입니다. 생성 문장을 압축하면서 기술적 의미를 보존한다는 핵심 아이디어는 유지하되, local trigger, 한국어 표현, runtime과 명확성 요구에 다른 contract가 필요할 때는 의도적으로 upstream과 다르게 동작합니다.

Provenance baseline: `JuliusBrussee/caveman` `skills/caveman/SKILL.md` at `bd22d86b32e4a99e09ff7482a35509faac7a6f65`.

배포 package에는 upstream MIT notice를 `src/rulesync/.rulesync/skills/caveman-ko/LICENSE`로 포함합니다.

## Maintenance Boundary

- Runtime behavior는 `src/rulesync/.rulesync/skills/caveman-ko/SKILL.md`에 둡니다.
- Repository eval fixture는 `evals/skills/caveman-ko/`에 둡니다.
- 현재 trigger와 behavior fixture는 experimental Skill을 위한 **capability eval contract**입니다. 특정 model/runtime이 이를 통과한다는 evidence나 blocking regression suite를 의미하지 않습니다.
- 이 capsule은 provenance, maturity와 maintenance context만 소유하며 runtime instruction으로 로드하지 않습니다.
- 일반적인 간결성 요청은 의도적으로 이 Skill의 범위 밖입니다. "짧게", "간결하게", "토큰 아껴서" 같은 요청만으로 trigger되면 failure case입니다.
- Local evidence 없이 upstream의 token-reduction percentage를 local contract에 복사하지 않습니다. 이 Skill은 생성되는 문장에 영향을 주며 input/context/reasoning token volume을 줄인다고 주장하지 않습니다.

## Promotion Criteria

다음 조건이 반복된 evidence로 확인된 뒤에만 `Stable` 상태 승격을 검토합니다.

- explicit caveman-style request는 안정적으로 trigger되고 일반적인 간결성 요청과 같은 near-miss는 trigger되지 않습니다.
- `lite`, `full`, `ultra`의 차이가 관찰 가능하게 유지됩니다.
- 압축 과정에서 negation, uncertainty, quantity, unit, condition, identifier와 필요한 safety clarity가 보존됩니다.
- one-turn, ongoing-mode와 deactivation behavior를 지원 runtime에서 이해할 수 있습니다.
- 추가 validation loop가 단순한 문구 변경이 아니라 실질적 수정 사항을 더 이상 만들지 않는 상태에 수렴합니다.

계속 보호할 가치가 있는 stable behavior가 확인되면 repository evaluation policy에 따라 capability evaluation에서 적절한 regression contract로 승격할 수 있습니다.

그전까지는 기능 확장보다 작은 evidence-led change를 우선합니다.

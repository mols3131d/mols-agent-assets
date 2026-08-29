---
description: caveman-ko를 유지보수하거나 승격할 때 upstream provenance, Experimental 경계, runtime·eval 책임과 promotion criteria를 확인하는 maintainer entrypoint입니다.
---

# caveman-ko

Status: **Experimental**.

`caveman-ko`는 MIT 라이선스의 [`JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman) 응답 Skill을 한국어 사용 환경에 맞게 실험적으로 조정한 자산입니다. 생성 문장을 압축하면서 기술적 의미를 보존한다는 핵심 아이디어는 유지하되, 로컬 trigger 조건, 한국어 표현, runtime과 명확성 요구에 다른 계약이 필요할 때는 의도적으로 upstream과 다르게 동작합니다.

Provenance baseline: `JuliusBrussee/caveman` [`skills/caveman/SKILL.md`](https://github.com/JuliusBrussee/caveman/blob/781c384cafc28d7ca392014dbab569f985b5b2fd/skills/caveman/SKILL.md) at `781c384cafc28d7ca392014dbab569f985b5b2fd`.

배포 package에는 upstream MIT notice를 `src/rulesync/.rulesync/skills/caveman-ko/LICENSE`로 포함합니다.

## Maintenance Boundary

- Runtime 동작은 `src/rulesync/.rulesync/skills/caveman-ko/SKILL.md`에 둡니다.
- Repository eval fixture는 `evals/skills/caveman-ko/`에 둡니다.
- 현재 trigger와 동작 fixture는 실험 단계 Skill을 위한 **capability eval contract**입니다. 특정 model/runtime이 이를 통과한다는 근거나 blocking regression suite를 의미하지 않습니다.
- 이 capsule은 출처, 성숙도와 유지보수 문맥만 소유하며 runtime instruction으로 로드하지 않습니다.
- 일반적인 간결성 요청은 의도적으로 이 Skill의 범위 밖입니다. "짧게", "간결하게", "토큰 아껴서" 같은 요청만으로 trigger되면 실패 사례입니다.
- 로컬 근거 없이 upstream의 token-reduction percentage를 로컬 계약에 복사하지 않습니다. 이 Skill은 생성되는 문장에만 영향을 주며 input/context/reasoning token volume에는 영향을 주지 않습니다.

## Promotion Criteria

다음 조건이 반복된 근거로 확인된 뒤에만 `Stable` 상태 승격을 검토합니다.

- 명시적인 caveman-style 요청은 안정적으로 trigger되고 일반적인 간결성 요청과 같은 near-miss는 trigger되지 않습니다.
- `lite`, `full`, `ultra`의 차이가 관찰 가능하게 유지됩니다.
- 압축 과정에서 부정, 불확실성, 수량, 단위, 조건, 식별자와 안전에 필요한 명확성이 보존됩니다.
- 1회 응답, 지속 모드와 비활성화 동작을 지원 runtime에서 이해할 수 있습니다.
- 추가 검증 루프가 단순한 문구 변경이 아니라 실질적 수정 사항을 더 이상 만들지 않는 상태에 수렴합니다.

계속 보호할 가치가 있는 안정화된 동작이 확인되면 저장소 평가 정책에 따라 capability evaluation에서 적절한 regression contract로 승격할 수 있습니다.

그전까지는 기능 확장보다 근거가 있는 작은 변경을 우선합니다.

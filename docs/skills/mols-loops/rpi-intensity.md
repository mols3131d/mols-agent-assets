---
description: RPI의 light·standard·deep intensity가 adaptive effort를 어떻게 bias하면서 prerequisite와 safety를 보존하는지 정리한 maintainer 문서입니다.
---

# RPI Intensity

`intensity`는 RPI의 **노력 강도에 대한 soft control**입니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Levels

- **light** — 최소 충분한 evidence, focused challenge, lean validation을 선호합니다.
- **standard** — confidence, cost, speed의 균형을 맞추는 기본값입니다.
- **deep** — stronger disconfirmation, deeper evidence, stronger validation, alternative comparison과 useful recursive narrowing을 더 적극적으로 탐색합니다.

## Adaptive Meaning

Intensity는 고정된 단계 수나 Loop 수가 아닙니다. 현재 risk, uncertainty, reversibility와 information gain에 따라 같은 intensity 안에서도 실제 effort는 달라집니다.

- `deep`도 convergence나 saturation 뒤의 추가 Loop, source quota, child Scope를 강제하지 않습니다.
- `light`도 genuine prerequisite, material acceptance check, required validation이나 safety gate를 생략하지 않습니다.
- 여러 충분한 경로가 있다면 요청된 intensity에 더 잘 맞는 경로를 선택합니다.
- Recursive child는 parent intensity를 effort bias로 상속하지만 Scope, authority나 Loop budget을 넓히지 않습니다.
- Run 중 intensity가 바뀌면 이후 effort에 적용합니다. Intensity 변화만으로 이미 유효한 Research, Plan이나 Work를 stale하게 만들지 않습니다.
- Continuation에서는 사용자 지정 active intensity를 resume state의 일부로 보존합니다.

## Preserve

Intensity를 고도화할 때 **adaptive effort bias**라는 성질을 유지합니다. 이를 quality waiver, fixed procedure, Loop quota, recursion command, dependency invalidator 또는 authority 확장으로 바꾸지 않습니다.

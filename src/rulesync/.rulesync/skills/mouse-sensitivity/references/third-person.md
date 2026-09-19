# Third-Person

3인칭에서는 mouse movement, camera, character facing과 reticle의 관계가 게임마다 다를 수 있다. FPS의 단일 `cm/360` 기준을 그대로 적용하지 않는다.

## Model

현재 조정하는 상태를 먼저 구분한다.

- free/orbit camera
- over-the-shoulder camera
- hipfire 또는 soft aim
- ADS/precision aim
- scoped 또는 일시적인 first-person state

게임이 상태별 sensitivity를 제공하면 역할을 나눠 판단한다. 하나의 setting이 여러 상태를 제어하면 그 coupling을 constraint로 본다.

## Tune

- 탐색 camera는 주변 확인과 방향 전환의 편안함을 우선한다.
- 정밀 aim은 reticle acquisition, micro correction과 tracking을 우선한다.
- Camera orbit은 편하지만 aim이 과민하면 전체 DPI보다 상태별 sensitivity 분리가 가능한지 먼저 확인한다.
- Character turn rate, aim assist, camera smoothing이나 acceleration이 결과를 제한하면 raw sensitivity만으로 문제를 설명하지 않는다.
- 1인칭 ADS/scope 상태는 그 상태에 한해 `first-person.md`를 함께 적용할 수 있다.

## Physical Reference

`cm/360`은 특정 camera/aim state의 rotation을 설명할 때 사용할 수 있다. Character orientation이나 reticle behavior가 camera rotation과 다르면 전체 조작의 공통 단위로 취급하지 않는다.

목표는 모든 상태의 물리 회전 거리를 같게 만드는 것이 아니라 상태 전환을 예측 가능하게 하고 각 상태의 목적에 맞는 control을 확보하는 것이다.

# Third-Person

3인칭에서는 mouse movement, orbit camera, character facing, reticle과 aiming state의 관계가 게임마다 크게 다를 수 있다. FPS 방식의 단일 `cm/360` 기준을 그대로 적용하지 않는다.

## Model

먼저 어떤 상태를 조정하는지 구분한다.

- free/orbit camera
- over-the-shoulder camera
- hipfire 또는 soft aim
- ADS/precision aim
- scoped 또는 일시적인 first-person state

게임이 상태별 sensitivity를 제공하면 각각의 역할을 분리해서 본다. 하나의 설정이 여러 상태를 동시에 제어하면 그 coupling을 constraint로 취급한다.

## Tune

- 탐색과 movement camera는 주변 확인과 방향 전환의 편안함을 우선한다.
- 정밀 aim 상태는 reticle acquisition, micro correction과 tracking을 우선한다.
- Camera orbit은 편하지만 ADS가 과민하면 전체 DPI를 먼저 바꾸기보다 상태별 sensitivity 분리가 가능한지 확인한다.
- Character turn rate, aim assist, camera smoothing이나 acceleration이 mouse input 결과를 제한하면 raw sensitivity만으로 문제를 설명하지 않는다.
- 게임이 1인칭 ADS/scope 상태를 사용하면 해당 상태에 한해 `first-person.md`의 판단을 함께 적용할 수 있다.

## Physical Reference

`cm/360`은 camera orbit이나 특정 aim state의 rotation mapping을 설명하는 데 사용할 수 있지만, character orientation이나 reticle behavior가 camera rotation과 동일하지 않으면 전체 조작의 공통 단위로 취급하지 않는다.

목표는 모든 camera state를 같은 물리 회전 거리로 맞추는 것이 아니라, 실제 플레이에서 상태 전환이 예측 가능하고 각 상태의 목적에 맞는 control을 확보하는 것이다.

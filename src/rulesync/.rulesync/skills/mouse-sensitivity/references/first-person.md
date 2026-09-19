# First-Person

1인칭에서는 mouse movement가 camera yaw/pitch와 직접 연결되는 경우가 많아 물리 회전 거리와 aiming control을 비교하기 쉽다. 다만 실제 mapping은 게임별로 확인한다.

## Focus

다음 동작을 구분해서 본다.

- 작은 target에 대한 initial acquisition
- micro correction
- 지속 tracking
- flick 또는 rapid target transition
- 90°/180° 같은 큰 camera turn
- hipfire와 ADS/scope 전환

하나의 동작만 개선하면서 다른 핵심 동작이 크게 악화되지 않는 범위를 찾는다.

## Physical Reference

게임의 rotation mapping이 확인되면 `cm/360`을 DPI와 game sensitivity를 함께 비교하는 공통 물리 지표로 사용할 수 있다. 계산 상수가 게임마다 다르면 해당 게임의 authoritative mapping을 사용한다.

`cm/360`은 유용한 기준이지만 그 자체가 목표가 아니다. 같은 물리 회전 거리도 FOV, target scale, movement mechanics, zoom 상태에 따라 다르게 느껴질 수 있다.

## Tune

- 작은 correction이 지속적으로 target을 넘어가면 감도를 소폭 낮추고 다시 확인한다.
- 편안한 mouse sweep으로 필요한 큰 turn에 도달하지 못하면 감도를 소폭 높이는 방향을 검토한다.
- Tracking과 flick 결과가 충돌하면 어떤 동작이 해당 게임과 사용자의 실제 우선순위인지 기준을 둔다.
- Hipfire와 ADS가 독립 설정이면 하나를 맞추기 위해 다른 하나를 자동으로 같은 비율로 바꾸지 않는다.
- Scope/zoom multiplier는 해당 게임의 scaling 의미를 확인한 뒤 조정한다.

초기 조정은 현재 값 주변의 작은 변화로 시작하고, 결과가 명확할 때만 다음 범위로 이동한다. 임의의 universal sensitivity range를 정답처럼 제시하지 않는다.

# First-Person

1인칭에서는 mouse movement가 camera yaw/pitch와 직접 연결되는 경우가 많다. 실제 mapping은 게임별로 확인한다.

## Focus

다음 동작을 구분해서 본다.

- initial target acquisition
- micro correction
- tracking
- flick 또는 rapid target transition
- 90°/180° 같은 큰 camera turn
- hipfire와 ADS/scope 전환

하나의 동작을 개선하면서 다른 핵심 동작이 크게 악화되지 않는 범위를 찾는다.

## Tune

- 작은 correction이 반복해서 target을 지나치면 소폭 낮춘다.
- 필요한 큰 turn에 편안한 mouse sweep으로 도달하지 못하면 높이는 방향을 검토한다.
- Tracking과 flick 결과가 충돌하면 해당 게임과 사용자의 실제 우선순위를 기준으로 선택한다.
- Hipfire와 ADS가 독립 setting이면 하나를 맞추기 위해 다른 하나를 자동으로 같은 비율로 바꾸지 않는다.
- Scope/zoom multiplier는 해당 게임의 scaling 의미를 확인한 뒤 조정한다.

## Physical Reference

`cm/360`은 물리 회전 거리가 판단에 도움이 될 때만 사용한다. 같은 값도 FOV, target scale, movement mechanics와 zoom 상태가 다르면 동일한 aiming behavior를 보장하지 않는다.

초기 조정은 현재 값 주변에서 시작하고 결과가 명확할 때만 범위를 넓힌다. Universal sensitivity range를 정답처럼 제시하지 않는다.

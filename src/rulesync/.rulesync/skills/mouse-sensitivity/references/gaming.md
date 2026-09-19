# Gaming

게임 감도는 물리 입력과 게임의 camera/aiming 변환을 분리해서 판단한다.

## Native Settings

게임의 sensitivity 숫자는 그 게임 안에서만 해석한다.

- `0.5`, `1.0`, `10`처럼 같은 숫자라도 게임마다 실제 회전량과 체감이 다를 수 있다.
- 감도 값을 기록하거나 비교할 때는 항상 game id와 해당 입력 상태(hipfire, ADS, scope, camera 등)를 함께 유지한다.
- 게임별 sensitivity scale이나 multiplier를 확인하지 않고 native 값을 다른 게임에 직접 복사하지 않는다.
- eDPI는 동일한 sensitivity scale을 공유하는 같은 게임 또는 명확히 호환되는 맥락에서만 비교한다.

## Comparison

DPI와 game-native sensitivity는 함께 기록하되, 파생 지표를 항상 계산하지 않는다.

- `cm/360`은 물리 회전 거리가 실제 판단에 도움이 되거나 사용자가 요청할 때 사용한다.
- 같은 `cm/360`이라도 FOV, zoom, ADS behavior와 camera model이 다르면 화면상 체감과 aiming behavior가 동일하다고 가정하지 않는다.
- 다른 게임으로 값을 옮기거나 특정 게임의 환산값이 필요하면 `conversion.md`를 추가로 읽는다.

게임이 raw mouse input을 사용하는 경우 OS pointer speed나 acceleration이 gameplay camera에 적용되지 않을 수 있다. 게임과 플랫폼의 실제 입력 경로를 확인하고 관련 없는 OS 값을 판단에 넣지 않는다.

## Mousepad Constraint

마우스패드 크기는 추천 감도의 실사용 가능성을 확인하는 데 사용한다.

- 필요한 turn/tracking 동작이 사용 가능한 이동 공간과 맞는지 본다.
- 패드 폭보다 `cm/360`이 크다는 사실만으로 감도가 잘못됐다고 판정하지 않는다. 실제 플레이는 360도 연속 sweep보다 180도 이하 회전, lift/reset과 재중앙화를 포함할 수 있다.
- 사용자에게 실제 usable area가 패드 전체보다 작다고 알려진 경우 그 값을 우선한다.

## Tune

현재 감도에서 발생하는 문제를 먼저 분류한다.

- micro correction에서 반복적으로 지나침 → 낮추는 방향 후보
- target 도달 전에 반복적으로 멈춤 → 높이는 방향 후보
- tracking은 안정적이지만 큰 turn이 과도하게 힘듦 → 높이는 방향 후보
- 큰 turn은 쉽지만 작은 target 획득이 불안정함 → 낮추는 방향 후보

한 번에 작은 폭으로 변경하고 동일한 drill 또는 실제 플레이 상황에서 비교한다. 프로 선수나 community 분포는 시작 범위를 검토하는 참고 evidence로만 사용한다.

## Conversion Boundary

게임 간 변환은 별도 요청이나 실제 필요가 있을 때만 수행한다. 사용자가 단순히 현재 게임의 감도 조정을 원하면 다른 게임의 계수, 변환 공식이나 converter를 불필요하게 조사하지 않는다.

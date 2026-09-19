# Gaming

게임 감도를 조정하기 전에 mouse input이 무엇을 제어하는지 구분한다.

## Input Context

- **camera/aiming** — mouse movement가 camera, reticle 또는 aim state를 제어한다. 필요하면 `first-person.md` 또는 `third-person.md`를 함께 읽는다.
- **pointer/cursor** — mouse pointer로 world/UI target을 선택하거나 map·screen을 이동한다. 작은 target 획득과 반복 이동 거리를 중심으로 본다.
- **mixed** — camera와 pointer처럼 서로 다른 상태가 공존하면 현재 task의 상태를 분리해 판단한다.

Profile의 `input_context`가 있으면 routing hint로 사용하되 실제 게임 동작보다 우선하지 않는다.

## Native Settings

게임의 sensitivity 숫자는 해당 게임과 입력 상태 안에서만 해석한다.

- 같은 숫자라도 게임마다 실제 cursor/camera movement가 다를 수 있다.
- 감도는 game id와 hipfire, ADS, scope, camera 같은 관련 상태를 함께 보존한다.
- 게임별 scale이나 multiplier를 확인하지 않고 native 값을 다른 게임에 직접 복사하지 않는다.
- eDPI는 같은 sensitivity scale을 공유하는 맥락에서만 비교한다.

게임이 raw mouse input을 사용하면 OS pointer speed나 acceleration이 gameplay input에 적용되지 않을 수 있다. 실제 입력 경로를 확인하고 관련 없는 OS 값을 제외한다.

## Tune

Camera/aiming에서는 micro correction, tracking, target transition과 필요한 큰 turn 사이의 균형을 본다. 세부 판단은 1인칭 또는 3인칭 reference를 사용한다.

Pointer/cursor에서는 다음을 본다.

- 작은 target을 반복해서 지나치면 낮추는 방향을 검토한다.
- 먼 target이나 넓은 map/screen 이동에서 반복적인 큰 손 이동이 필요하면 높이는 방향을 검토한다.
- edge scrolling, drag, selection처럼 특정 interaction에서만 문제가 나면 전체 감도보다 해당 게임의 관련 setting이나 behavior를 먼저 확인한다.

한 번에 작은 폭으로 변경하고 동일한 실제 플레이 상황에서 비교한다. 프로 선수나 community 설정은 시작 범위를 검토하는 참고 evidence로만 사용한다.

## Physical Constraint

마우스패드 크기와 `cm/360`은 camera/aiming이나 큰 물리 이동이 실제 판단에 도움이 될 때만 사용한다. 패드 폭이나 파생 지표 하나만으로 감도가 잘못됐다고 판정하지 않는다.

## Conversion Boundary

다른 게임으로 값을 옮기거나 정확한 환산값이 필요하면 `conversion.md`를 추가로 읽는다. 현재 게임의 tuning만 필요하면 다른 게임의 계수나 converter를 조사하지 않는다.

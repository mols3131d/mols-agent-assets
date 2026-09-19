# Desktop

사무와 코딩의 감도는 pointer가 여러 UI target과 text surface를 얼마나 예측 가능하게 획득하는지에 초점을 둔다.

## Context

필요한 범위에서 다음을 본다.

- DPI
- OS pointer speed와 acceleration
- 각 display의 resolution과 OS scale
- primary display와 실제로 자주 사용하는 display 조합

해상도와 scale은 logical workspace와 UI target 크기를 이해하는 단서다. 모니터 물리 크기나 PPI가 없으면 물리적인 화면 폭이나 마우스 이동 거리로 환산하지 않는다.

## Tune

- 작은 UI target, text caret, selection handle을 자주 넘기면 속도를 낮추는 방향을 검토한다.
- 넓은 multi-monitor 이동에서 반복적으로 큰 손 이동이 필요하면 속도를 높이는 방향을 검토한다.
- Acceleration은 무조건 제거하거나 유지하지 않는다. 빠른 장거리 이동과 느린 미세 조정의 균형이 실제 workflow에 도움이 되는지 확인한다.
- 서로 다른 display scaling에서 불편이 특정 display 전환에 집중되면 전체 DPI를 바꾸기 전에 OS scaling과 pointer behavior가 원인인지 구분한다.
- 게임이 raw input이나 별도 camera sensitivity를 사용한다면 desktop 감도를 맞추기 위해 게임 감도를 함께 바꾸지 않는다.

## Verify

변경 전후를 같은 작업으로 비교한다. 예를 들어 text selection, 작은 toolbar/button 획득, 한 display 끝에서 다른 display의 target으로 이동하는 동작을 반복해 overshoot, undershoot와 불필요한 reposition이 줄었는지 본다.

한 번에 DPI와 OS pointer speed를 동시에 크게 바꾸지 않는다. 어떤 변경이 개선을 만들었는지 구분할 수 있는 범위로 조정한다.

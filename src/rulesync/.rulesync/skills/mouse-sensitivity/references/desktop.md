# Desktop

사무와 코딩에서는 pointer가 UI target과 text surface를 얼마나 예측 가능하게 획득하는지 본다.

## Context

필요한 범위에서 DPI, OS pointer speed/acceleration, 각 display의 resolution/scale과 실제 사용 조합을 확인한다.

Resolution과 scale은 logical workspace와 UI target 크기를 이해하는 context다. 모니터 물리 크기나 PPI가 없으면 화면의 물리 폭이나 mouse 이동 거리로 환산하지 않는다.

## Tune

- 작은 UI target, text caret, selection을 자주 지나치면 낮추는 방향을 검토한다.
- 넓은 multi-monitor 이동에서 반복적인 큰 손 이동이 필요하면 높이는 방향을 검토한다.
- Acceleration은 자동으로 끄거나 유지하지 않는다. 장거리 이동과 미세 조정의 균형이 실제 workflow에 도움이 되는지 본다.
- 불편이 특정 display 전환에 집중되면 전체 DPI를 바꾸기 전에 scaling과 pointer behavior를 구분한다.
- 게임이 raw input이나 별도 sensitivity를 사용하면 desktop 조정을 이유로 game sensitivity를 함께 바꾸지 않는다.

## Verify

변경 전후를 같은 작업으로 비교한다. Text selection, 작은 button 획득, display 사이 target 이동에서 overshoot, undershoot와 불필요한 reposition이 줄었는지 본다.

DPI와 OS pointer speed를 동시에 크게 바꾸지 않는다. 어떤 변경이 효과를 냈는지 구분할 수 있는 범위로 조정한다.

# Cross-game Conversion

게임 간 감도 변환은 기본 동작이 아니다. 사용자가 요청하거나 정확한 환산값이 결론에 필요할 때만 현재 외부 자료를 조사한다.

## Research

서로 다른 게임의 native sensitivity 숫자를 직접 맞추지 않는다. 필요한 정보는 현재 시점에 확인하고 다음 순서를 우선한다.

1. 게임 자체의 공식 설정 설명이나 개발사 자료
2. 지원 게임과 조건이 명확한 유지보수되는 converter 또는 open-source tool
3. 위 자료가 부족하면 실제 게임 내 회전·cursor movement를 기준으로 비교

외부 converter는 계산 도구이자 evidence다. 특정 서비스의 값이나 내부 database를 보편적인 authority로 취급하거나 Skill에 복제하지 않는다.

## Use

- Source game, target game, DPI, native sensitivity와 관련 입력 상태를 확인한다.
- Converter가 값을 직접 제공하면 내부 공식을 재구현하지 않고 결과와 적용 조건을 확인해 전달할 수 있다.
- 여러 방식이 있으면 360-distance, FOV/monitor-distance, ADS/scope 등 무엇을 맞추는지 구분한다.
- 단순한 시작값이 목적이면 과도한 정밀 계산보다 현재 신뢰할 수 있는 결과와 짧은 검증 방법을 우선한다.
- 자료가 충돌하면 game version, FOV, ADS/zoom 상태, DPI와 conversion 기준 차이를 먼저 확인한다.

직접 수학 계산은 사용자가 명시적으로 요구하거나 현재 자료가 필요한 값을 제공하지 않을 때만 수행한다. 게임별 coefficient table이나 converter database는 repository에 저장하지 않는다.

## Verify

변환값은 시작점으로 취급한다.

- 목표 게임에서 같은 입력 상태의 실제 movement와 aiming/cursor control을 확인한다.
- 설정에 step이나 rounding 제한이 있으면 실제 입력 가능한 값으로 조정한다.
- 같은 환산값이 같은 플레이 감각이나 성능을 보장한다고 주장하지 않는다.

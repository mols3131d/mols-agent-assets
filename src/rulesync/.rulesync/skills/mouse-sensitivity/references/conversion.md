# Cross-game Conversion

게임 간 감도 변환은 기본 동작이 아니다. 사용자가 요청하거나 정확한 환산값이 실제 판단에 필요한 경우에만 현재 외부 자료를 조사해 필요한 수준으로 처리한다.

## Research First

서로 다른 게임의 native sensitivity 숫자를 직접 맞추지 않는다. 변환 요청이 있으면 먼저 현재 지원되는 자료를 찾는다.

우선순위는 다음과 같다.

1. 게임 자체의 공식 설정 설명이나 개발사 자료
2. 계산 근거 또는 게임별 mapping을 확인할 수 있는 유지보수되는 open-source tool
3. 지원 게임과 조건을 명시하는 신뢰할 만한 sensitivity converter
4. 위 자료가 부족하면 실제 회전 거리나 게임 내 동작을 기준으로 비교

외부 converter는 편리한 계산 도구이자 evidence다. 특정 사이트의 결과를 보편적인 authority로 취급하지 않는다.

## Use

- 사용자가 source game, target game, DPI와 현재 sensitivity를 주면 먼저 해당 게임 조합을 지원하는 최신 converter나 자료가 있는지 확인한다.
- converter가 직접 값을 제공하면 내부 공식을 다시 구현할 필요 없이 결과와 적용 조건을 확인해 전달할 수 있다.
- 여러 변환 방식이 제공되면 `360-distance`, FOV/monitor-distance, ADS/scope 등 어떤 기준인지 구분한다.
- 사용자가 단순한 시작값만 원하면 과도한 정밀 계산보다 신뢰할 만한 converter 결과와 짧은 검증 방법을 우선한다.
- 외부 자료가 서로 다른 값을 주면 게임 버전, FOV, ADS/zoom 상태, DPI, 변환 기준의 차이를 먼저 확인한다.

정확한 수학적 계산은 사용자가 명시적으로 요구하거나 외부 도구가 필요한 결과를 직접 제공하지 않을 때만 수행한다. 게임별 coefficient table이나 converter database를 Skill에 복제하지 않는다.

## Useful Sources

현재 참고할 수 있는 대표 source는 다음과 같다. 실제 요청에서는 현재 지원 상태를 다시 확인한다.

- Aimlabs Mouse Sensitivity Converter: https://preview.aimlabs.com/mouse-sensitivity-converter
- Aimlabs sensitivity configuration guide: https://aimlabs.com/articles/aimlabs/how-to-configure-and-convert-your-sensitivity-in-aimlabs/
- KovaaK SensitivityMatcher: https://github.com/KovaaK/SensitivityMatcher

특정 사이트에 고정하지 않는다. 더 직접적이고 현재성이 높은 source가 있으면 그것을 우선한다.

## Verification

변환값은 시작점으로 취급한다.

- 가능하면 목표 게임에서 실제 회전, tracking 또는 aiming 감각을 확인한다.
- ADS/zoom을 변환했다면 같은 상태에서 비교한다.
- 설정 값에 step이나 rounding 제한이 있으면 실제 입력 가능한 값으로 조정한다.
- 동일한 환산값이 동일한 플레이 감각이나 성능을 보장한다고 주장하지 않는다.

---
name: mouse-sensitivity
description: >-
  Diagnose, compare, or tune mouse sensitivity across desktop, office/coding, and games.
  Use when DPI, OS pointer behavior, display scaling, mousepad space, or game-native
  sensitivity affects cursor, camera, or aiming control, including pointer/cursor games,
  first- and third-person contexts, and requested cross-game conversion. Use an optional
  user profile when persistent settings are available. Do not use for mouse hardware
  purchasing, polling/sensor troubleshooting, or medical/ergonomic advice.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Mouse Sensitivity

마우스의 물리 입력과 각 환경의 pointer/camera 입력을 구분해 목적에 맞는 감도를 진단·비교·튜닝한다.

## Route

현재 task에 필요한 reference만 읽는다.

| Intent | Load |
| --- | --- |
| 사용자 profile JSON을 읽거나 만들거나 갱신 | `references/profile.md` |
| 사무, 코딩, 일반 desktop pointer 조정 | `references/desktop.md` |
| 게임 공통 또는 pointer/cursor 게임 감도 조정 | `references/gaming.md` |
| 1인칭 camera/aiming | `references/gaming.md`, `references/first-person.md` |
| 3인칭 camera/aiming | `references/gaming.md`, `references/third-person.md` |
| 게임 간 감도 변환 또는 정확한 환산값 조사 | `references/gaming.md`, `references/conversion.md` |

여러 환경을 함께 다루면 필요한 reference를 조합하고 관련 없는 detail은 로드하지 않는다.

## Core Contract

- 하나의 보편적인 최적 감도를 가정하지 않는다. 목적, input context, 현재 설정과 물리 공간을 기준으로 판단한다.
- Desktop pointer와 game input은 별도 파이프라인으로 취급한다. 실제 영향이 확인되지 않은 설정을 서로 연결하지 않는다.
- 결론을 바꾸는 정보만 요구한다. DPI 외의 마우스 모델, polling rate, sensor, 무게 같은 hardware metadata는 필요가 입증되지 않으면 묻지 않는다.
- 환경별 native setting은 그 의미를 보존한다. 근거 없이 공통 scale로 정규화하거나 다른 환경의 값으로 대체하지 않는다.

## Workflow

1. 현재 목적과 input context, 실제 적용되는 설정을 확인한다.
2. 필요한 reference만 읽고 해당 입력에 영향이 없는 설정을 제외한다.
3. 현재 값 주변의 작은 조정부터 제안하고 같은 작업이나 플레이 상황에서 확인한다.
4. 사용자가 요청하면 확인된 값만 profile에 반영한다.

정확한 값이 결론을 바꿀 때만 추가 정보를 요구한다. 모르는 값은 추측하지 않는다.

## Boundary

이 Skill은 mouse sensitivity와 관련된 설정 해석, 비교, 변환과 튜닝을 소유한다. 마우스 구매, hardware/firmware 진단, polling/sensor tuning, 게임 그래픽·네트워크·성능 최적화, 의료적 ergonomics 판단은 소유하지 않는다.

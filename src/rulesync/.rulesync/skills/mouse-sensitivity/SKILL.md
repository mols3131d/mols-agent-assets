---
name: mouse-sensitivity
description: >-
  Tune, compare, or translate mouse sensitivity across desktop, office/coding, and
  games. Use when DPI, OS pointer settings, display resolution/scaling, mousepad size,
  or game-specific sensitivity materially affect the recommendation, including
  first-person and third-person camera/aiming contexts and cross-game conversion.
  Use an optional user profile when persistent settings are available. Do not use for
  mouse hardware purchasing, polling/sensor troubleshooting, or general
  medical/ergonomic advice.
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

마우스의 물리 입력과 각 환경의 pointer/camera 입력을 구분하고, 사용 목적에 맞는 감도를 진단·비교·튜닝한다.

## Route

현재 task에 필요한 reference만 읽는다.

| Intent | Load |
| --- | --- |
| 사용자 설정 JSON을 읽거나 만들거나 갱신 | `references/profile.md` |
| 사무, 코딩, 일반 desktop pointer 조정 | `references/desktop.md` |
| 게임 감도 진단·튜닝, 공통 게임 기준 | `references/gaming.md` |
| 서로 다른 게임의 감도 변환 또는 게임별 환산 정보 조사 | `references/gaming.md`, `references/conversion.md` |
| 1인칭 camera/aiming | `references/gaming.md`, `references/first-person.md` |
| 3인칭 camera/aiming | `references/gaming.md`, `references/third-person.md` |

여러 환경을 함께 다루면 필요한 reference를 조합한다. 관련 없는 게임 유형, 변환 또는 profile reference를 선로드하지 않는다.

## Core Contract

- 하나의 보편적인 최적 감도를 가정하지 않는다. 목적, 입력 모델, 현재 설정과 사용 가능한 물리 공간을 기준으로 판단한다.
- Desktop pointer와 game camera/aiming은 별도 입력 파이프라인으로 취급한다. 한쪽의 설정이 다른 쪽에 실제로 영향을 주는지 확인하지 않고 값을 연결하지 않는다.
- DPI는 기본 물리 입력 기준으로 사용하되, 마우스 모델, polling rate, sensor, 무게 같은 주변기기 정보는 감도 판단에 필요하다고 입증되지 않으면 요구하지 않는다.
- 해상도와 OS 배율은 desktop의 logical workspace와 target 크기를 이해하는 context다. 모니터의 물리 크기나 PPI가 없는데 이를 물리 이동 거리로 환산하지 않는다.
- 각 게임의 native sensitivity 값은 해당 게임의 입력 scale 안에서만 의미가 있다. 게임 이름과 입력 상태를 분리하지 않은 숫자를 공통 감도로 취급하지 않는다.
- 게임별 정확한 환산이나 공식을 기본 동작으로 만들지 않는다. 사용자가 게임 간 변환을 요청하거나 정확한 값이 결론에 필요한 경우에만 현재 외부 자료를 조사한다.
- `cm/360`, eDPI 같은 파생 지표는 실제 판단에 도움이 될 때만 사용하며, 계산 자체를 목표로 삼지 않는다.
- 마우스패드 크기는 현실적인 이동 범위를 판단하는 constraint로 사용한다. 패드 폭을 감도 공식의 절대 기준으로 취급하지 않는다.
- 프로 선수나 인기 설정은 참고 evidence일 수 있지만 정답이나 목표값으로 취급하지 않는다.

## Workflow

1. 현재 DPI와 해당 환경에서 실제로 적용되는 감도 설정을 확인한다.
2. 사무/코딩, 특정 게임, 1인칭, 3인칭 등 현재 목적과 가장 불편한 동작을 식별한다.
3. 해당 입력 파이프라인에 영향이 없는 설정은 판단에서 제외한다.
4. 게임 작업에서는 native sensitivity를 게임 이름과 입력 상태에 묶어 해석한다.
5. 사용자가 게임 간 변환이나 정확한 환산을 요청하면 현재 지원되는 converter, 게임 자료 또는 검증 가능한 source를 조사해 필요한 값만 구한다.
6. 한 번에 작은 범위만 변경하고, 실제 작업이나 플레이에서 확인할 관찰 기준을 함께 제시한다.
7. 결과가 충분하면 사용자가 요청한 경우 profile에 현재 값을 반영한다.

정확한 값이 결론을 바꾸는 경우에만 추가 정보를 요구한다. 정보가 없으면 임의의 값을 채우지 않고 범위, 조건 또는 확인 방법으로 남긴다.

## Profile

사용자별 설정은 Skill package의 canonical content가 아니다. 실제 profile은 사용자나 workspace가 소유한 외부 JSON으로 두고, 이 Skill은 `references/profile.md`의 의미만 정의한다.

- Profile은 선택 사항이다. 일회성 상담에 profile 생성을 강제하지 않는다.
- 사용자가 profile 경로나 저장 위치를 지정하지 않았다면 임의의 persistent path를 만들지 않는다.
- 새 profile의 최소 예시는 `assets/profile.example.json`을 사용한다.
- 기존 profile을 갱신할 때는 task와 관련 없는 필드나 알 수 없는 확장을 보존한다.

## Boundary

이 Skill은 mouse sensitivity와 관련된 설정 해석, 비교, 변환과 튜닝을 소유한다. 마우스 구매 추천, hardware/firmware 진단, polling/sensor 성능 튜닝, 게임 전반의 그래픽·네트워크·성능 최적화, 의료적 ergonomics 판단은 소유하지 않는다.

---
description: 저장소의 파일·디렉터리 이름, 배치, 계층과 source-test 대응 구조를 정할 때 적용하는 local policy입니다.
---

# Repository Structure

파일 구조는 **책임과 탐색 경로를 드러내는 보조 수단**입니다. 이름과 배치만 보아도 무엇이 어디에 있고 다음에 어디를 살펴볼지 대략 예측할 수 있어야 합니다.

탐색성을 위해 구조를 왜곡하지 않습니다. 정확성, 명확한 책임, 자연스러운 생태계 관례, 유지보수성과 운영 편의성이 우선하며, framework·tool·generated 영역에 더 구체적인 배치 규칙이 있으면 그 규칙을 따릅니다.

## Placement

새 파일은 가능한 한 **가장 좁고 자연스러운 책임 경계** 아래에 둡니다.

- 이미 적절한 책임 경계가 있으면 그 디렉터리를 재사용합니다.
- 이름과 배치만으로 파일의 역할을 짐작할 수 있게 합니다.
- 서로 관련 없는 파일을 한 디렉터리에 계속 쌓지 않습니다.
- 새 디렉터리는 반복되는 묶음이나 함께 유지해야 할 맥락을 더 잘 드러낼 때 만듭니다.
- 구조적으로 동등한 선택지라면 탐색하기 쉬운 쪽을 선호합니다.
- 작은 README나 index로 충분하면 불필요한 이동이나 계층 추가를 피합니다.
- 탐색성을 이유로 wrapper, 중복 abstraction, 불필요한 계층을 만들지 않습니다.

기존 구조를 대칭적으로 보이게 하려고 일괄 재배치하지 않습니다. 변경하는 영역부터 자연스럽게 정렬하고, 반복적인 오탐색이나 높은 파일 밀도처럼 실제 비용이 있을 때 별도 구조 개선으로 다룹니다.

## Source and Test Alignment

현재처럼 source와 `tests/`를 분리한 pytest layout을 유지합니다. Repository가 직접 소유하는 source에 자연스러운 기준점이 있으면 관련 test도 위치를 예측할 수 있게 배치합니다.

```text
scripts/agent-assets/validate_rulesync.py
                    ↓
tests/scripts/agent-assets/test_validate_rulesync.py
```

Source path를 그대로 맞추는 것 자체가 목적은 아닙니다.

- 하나의 source 파일에 작은 test 범위가 대응하면 하나의 test 파일을 기본으로 합니다.
- 같은 source의 동작이 늘어나면 같은 디렉터리의 여러 test 파일로 나눌 수 있습니다.
- 반복되는 prefix, fixture·data·snapshot, 높은 파일 밀도로 묶음의 이점이 커지면 별도 디렉터리를 고려합니다.
- 여러 source 파일이 하나의 안정적인 동작이나 system boundary를 만들면 source path보다 그 경계를 기준으로 묶을 수 있습니다.
- framework의 test discovery와 import convention이 다르면 framework convention을 우선합니다.

Source를 이동하거나 이름을 바꿀 때는 관련 test의 탐색 관계도 함께 확인합니다. 더 안정적인 동작 경계를 훼손하면서까지 경로를 그대로 맞추지는 않습니다.

## Review

파일이나 디렉터리를 추가·이동할 때는 다음만 확인합니다.

- 이름과 위치만으로 책임을 대략 예측할 수 있는가
- 이미 더 자연스러운 책임 경계가 있는가
- 새 계층이 탐색 비용보다 더 큰 유지보수 비용을 만들지 않는가
- source가 있는 test라면 관련 test 위치를 합리적으로 추측할 수 있는가
- 이동으로 entrypoint, import, test discovery, workflow 또는 문서 참조가 깨지지 않는가

구조의 품질은 디렉터리 수나 대칭성이 아니라 **탐색과 이해 비용이 실제로 줄었는지**로 판단합니다.

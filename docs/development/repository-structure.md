---
description: 저장소의 file·directory naming, placement, hierarchy와 source-test 대응 구조를 정할 때 적용하는 local policy입니다.
---

# Repository Structure

이 저장소는 filesystem을 **탐색 단서**로 활용합니다. File과 directory 이름, 배치, 계층만 보아도 큰 책임 경계와 다음 탐색 지점을 예측하기 쉬운 구조를 선호합니다.

Filesystem legibility를 위해 구조를 억지로 만들지는 않습니다. Correctness, 명확한 ownership, 자연스러운 ecosystem convention, 유지보수성과 operability가 우선이며, framework·tool·generated 영역에 더 구체적인 layout owner가 있으면 그 규칙을 따릅니다.

## Placement

새 file은 가능한 한 **가장 좁고 이미 존재하는 자연스러운 owner** 아래에 둡니다. 이름과 배치는 그 owner의 역할을 드러내야 하며, unrelated file을 한 directory에 계속 쌓아 탐색 비용을 키우지 않습니다.

- stable한 책임 경계가 이미 있으면 그 directory를 재사용합니다.
- directory를 새로 만드는 것은 반복되는 grouping이나 local context를 구조로 드러낼 실질적인 이점이 있을 때만 합니다.
- 단순히 tree를 더 설명적으로 보이게 하려고 wrapper, 중복 abstraction, 불필요한 hierarchy를 추가하지 않습니다.
- 작은 README나 index가 placement 변경보다 싸고 충분한 탐색 수단이면 구조 변경보다 먼저 고려합니다.
- 구조적으로 동등한 선택지라면 tree에서 역할과 다음 탐색 지점을 더 쉽게 예측할 수 있는 쪽을 선호합니다.

이 원칙 때문에 기존 repository를 일괄 재배치하지 않습니다. 변경하는 영역에서 자연스럽게 정렬하고, 반복적인 오탐색이나 높은 file density처럼 실제 비용이 확인될 때 별도 구조 개선으로 다룹니다.

## Source and Test Alignment

`tests/` 밖에 source를 두는 현재 pytest layout은 유지합니다. Repository가 직접 소유하는 executable source에 자연스러운 source anchor가 있으면 test path도 그 위치 관계를 **예측 가능한 navigation cue**로 사용합니다.

기본 형태는 source root와 상대 directory를 반영하고 test filename에서 대상 source를 드러내는 것입니다.

```text
scripts/agent-assets/validate_rulesync.py
                    ↓
tests/scripts/agent-assets/test_validate_rulesync.py
```

Literal mirroring 자체가 목적은 아닙니다.

- 하나의 source file에 작은 test surface가 대응하면 file-to-file 형태를 우선합니다.
- 같은 source anchor의 behavior가 늘어나면 같은 directory의 sibling test files로 나눌 수 있습니다.
- 반복 prefix, fixture·data·snapshot 같은 local context, 높은 file density 때문에 grouping 이점이 커지면 bundle directory를 고려합니다.
- 여러 source unit이 하나의 안정적인 behavior나 system boundary를 만들면 source path보다 feature·behavior·integration boundary를 기준으로 묶을 수 있습니다.
- framework의 test discovery와 import convention이 다르면 framework convention을 우선합니다.

Test path는 source architecture를 새로 정의하는 계약이 아니라 **관련 테스트를 빠르게 찾기 위한 대응 관계**입니다. Source rename이나 구조 변경이 test navigation cue를 깨뜨리면 함께 정렬하되, 테스트의 더 안정적인 behavior boundary를 훼손하면서까지 literal mirroring하지 않습니다.

## Review

File이나 directory를 추가·이동할 때는 다음을 함께 확인합니다.

- 이름과 위치만으로 책임을 대략 예측할 수 있는가
- 이미 존재하는 더 자연스러운 owner가 있는가
- 새 hierarchy가 탐색 비용보다 더 큰 변경·운영 비용을 만들지는 않는가
- source가 있는 test라면 관련 test 위치를 합리적으로 추측할 수 있는가
- 이동으로 entrypoint, import, test discovery, workflow, documentation reference가 깨지지 않는가

구조 변경의 품질은 directory 수나 대칭성보다 **orientation과 navigation 비용이 실제로 줄었는지**로 판단합니다.

## Related Patterns

이 local policy는 다음 reusable pattern의 관점을 적용합니다. 세부 heuristic과 variant는 pattern 문서가 소유합니다.

- [Filesystem-Legible Structure](../../catalog/patterns/software-engineering/filesystem-legible-structure.md)
- [Source-Mirrored Test Structure](../../catalog/patterns/software-engineering/source-mirrored-test-structure.md)

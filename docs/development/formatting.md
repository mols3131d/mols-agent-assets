---
description: 저장소 파일을 포맷할 때 changed-only와 전체 포맷 중 어떤 경로를 사용하고 formatter와 CI의 책임을 어떻게 나눌지 확인하는 정책입니다.
---

# Formatting

Formatting은 **파일의 표현을 repository convention에 맞게 정규화하는 write 작업**입니다. 의미나 계약을 검증하지 않습니다.

## Usage

| 목적 | 명령 |
| --- | --- |
| 현재 변경과 untracked file 포맷 | `mise run format-changed` |
| 저장소 전체 포맷 | `mise run format` |
| staged 소스 읽기 전용 검사 | `mise run quality-check --staged` |
| 특정 base 이후 변경 소스 검사 | `mise run quality-check --changed-from <base-ref>` |
| 전체 tracked 소스 검사 | `mise run quality-check --all` |

일상 작업에서는 `format-changed`를 사용합니다. 전체 포맷은 unrelated file까지 바꿀 수 있으므로 명시적인 repository-wide 정리에만 사용합니다.

| 대상 | Formatter |
| --- | --- |
| Python | Ruff |
| Markdown | rumdl |
| JSON·JSONC·JavaScript·TypeScript 계열 | Biome |

## CI Boundary

CI는 `scripts/source_quality_check.py`의 공통 읽기 전용 검사에서 Ruff lint/format, rumdl lint/format, Biome lint/format을 파일 유형별로 실행합니다. `--changed-from`은 현재 `HEAD`와 base 사이의 **추가·수정된 파일**을 검사하며, 삭제는 건너뜁니다. Git 비교가 실패하면 검사를 생략하지 않고 실패합니다. `--all`은 현재 tracked 파일을 검사하는 명시적 전체 검증입니다.

CI가 committed representation contract를 확인하기 위해 formatter의 check-only 경로를 사용할 수 있습니다. 이 경우 CI는 파일을 자동 수정하거나 stage·commit·push하지 않습니다.

Formatting check를 merge-blocking evidence로 둘지, 어떤 단계에서 실행할지는 [Continuous Integration](ci.md)이 소유합니다. Formatter가 실제 파일을 정규화하는 write path와 tool ownership은 이 문서가 계속 소유합니다.

Lefthook은 일반 source를 자동 포맷하거나 stage하지 않습니다. `--staged`는 staged 파일명에 대해 worktree 내용을 검사하되, 같은 파일에 unstaged 변경이 있거나 선택한 파일을 안전하게 읽을 수 없으면 실패합니다. Hook은 index blob을 별도로 린트하지 않습니다. 원격 커밋과 merge 후보는 PR Gate에서 독립 검증합니다.

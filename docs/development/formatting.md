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

일상 작업에서는 `format-changed`를 사용합니다. 전체 포맷은 unrelated file까지 바꿀 수 있으므로 명시적인 repository-wide 정리에만 사용합니다.

| 대상 | Formatter |
| --- | --- |
| Python | Ruff |
| Markdown | rumdl |
| JSON·JSONC·JavaScript·TypeScript 계열 | Biome |

## Boundary

- Formatter 실행은 local write path가 소유합니다.
- Lefthook은 formatter를 자동 실행하거나 변경 내용을 자동 stage하지 않습니다.
- PR Gate와 [Validation](validation.md)은 formatting을 대신 실행하지 않습니다.
- 의미나 동작을 바꾸는 수정은 formatting으로 취급하지 않습니다.

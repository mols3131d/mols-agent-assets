---
description: 저장소 파일을 포맷할 때 changed-only와 전체 포맷 중 어떤 경로를 사용하고 formatter와 CI의 책임을 어떻게 나눌지 확인하는 정책입니다.
---

# Formatting

Formatting은 **파일의 표현을 repository convention에 맞게 정규화하는 write 작업**입니다. 의미 검증이나 테스트와 구분하며, 일상 작업에서는 현재 변경에만 적용합니다.

## Default

현재 변경과 untracked file만 포맷합니다.

```bash
mise run format-changed
```

`format-changed`는 삭제된 파일과 변경되지 않은 파일을 건드리지 않습니다.

| 대상 | Formatter |
| --- | --- |
| Python | Ruff |
| Markdown | rumdl |
| JSON·JSONC·JavaScript·TypeScript 계열 | Biome |

## Full Repository

저장소 전체를 명시적으로 정리할 때만 사용합니다.

```bash
mise run format
```

전체 포맷은 unrelated file까지 변경할 수 있으므로 일반적인 편집 흐름의 기본값으로 사용하지 않습니다.

## Automation Boundary

Formatter는 local write path가 소유합니다. Lefthook은 formatter를 자동 실행하거나 수정된 working tree를 자동 stage하지 않습니다.

PR Gate와 [Validation](validation.md)도 formatting을 실행하지 않습니다. [Testing](testing.md)은 deterministic test와 PR Gate를 소유합니다.

Formatting 결과가 의미나 동작을 바꾸는 수정까지 포함해서는 안 됩니다. 그런 변경은 해당 코드·문서·자산 작업의 책임으로 다룹니다.

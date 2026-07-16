# 에이전트 자산 백업 프로토콜 (Agent Asset Backup Protocol)

## Goal (목표)

기존 마크다운(Markdown) 자산을 수정하기 전에 원본 상태를 보존하여, 원활한 롤백(Rollback)과 변경 사항 비교(Diff)가 가능하도록 합니다.

## When to Use (사용 시점)

워크스페이스 내의 기존 마크다운 자산을 수정해야 하는 워크플로우나 규칙(Rule)을 수행할 때마다 이 프로토콜을 사용합니다.

## Instructions (지침)

- 수정을 시작하기 전에 항상 원본 파일의 복사본을 먼저 저장하십시오.
- 백업 파일이 저장될 경로와 방식은 제공된 인자(Arguments) 또는 기본값(Defaults)에 의해 결정됩니다.

## Workflows (워크플로우)

### Arguments from Context (컨텍스트 인자)

- 타겟 파일 경로 (Target file path, 필수): 백업할 원본 마크다운 자산의 경로입니다.
- `mode`: 백업 방식 (`extension` 또는 `tmp-dir`). 기본값은 `extension`입니다.
- `tmp-dir`: 백업 파일을 저장할 디렉토리 경로 (`mode`가 `tmp-dir`일 때 사용). 기본값은 `.tmp`입니다.
- `extension`: 파일명에 삽입할 확장자명 (`mode`가 `extension`일 때 사용). 다중 확장자가 있는 파일의 경우, 가장 왼쪽 확장자 자리에 삽입됩니다. 기본값은 `backup`입니다.

### Procedure (절차)

1. 백업 모드(`mode`)를 결정합니다.
2. `mode`가 `extension`인 경우:
   - 원본 파일명의 가장 왼쪽 확장자 위치에 `extension`을 삽입하여 백업 파일명을 계산합니다 (예: `file.spec.md` -> `file.backup.spec.md`).
   - 계산된 백업 파일명으로 원본 파일을 동일한 디렉토리에 복사합니다.
3. `mode`가 `tmp-dir`인 경우:
   - `tmp-dir` 경로로 백업 대상 디렉토리를 확인하고, 해당 디렉토리가 없으면 새로 생성합니다.
   - 원본 파일명을 그대로 유지한 채 원본 파일을 백업 디렉토리로 복사합니다.

### Validation (검증)

- 백업 파일이 올바른 위치에 성공적으로 생성되었는지 확인합니다.
- 생성된 백업 파일의 내용이 수정하기 전의 원본 내용과 완전히 일치하는지 검증합니다.

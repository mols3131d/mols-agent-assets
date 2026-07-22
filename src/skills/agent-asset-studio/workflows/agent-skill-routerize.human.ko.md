---
name: agent-skill-routerize
description: 사용 시점: 여러 개의 연관된 기존 스킬을 하나의 라우팅 스킬로 통합하고자 할 때. 제외 대상: 서로 무관한 도메인, 권한 또는 라이프사이클을 가진 스킬을 병합할 때.
---

# 스킬 라우팅화 (Routerize Skills)

## Goal (목표)

연관된 기존 스킬들을 `INDEX.csv` 기준 상대 경로인 워크플로우 경로를 라우트 ID로 가지는 하나의 얕은 라우팅 스킬(shallow routing skill)로 통합합니다.

## When to Use (사용 시점)

개별적인 연관 스킬들을 `lite` 또는 `full` 모드를 사용하여 단일 라우팅 스킬로 마이그레이션할 때 이 워크플로우를 사용합니다.

## Instructions (지침)

- 마이그레이션 전에 `references/routing-skill-migration.md`를 읽으십시오.
- 파일 시스템 변환에는 `scripts/routerize_skills.py`를 사용하십시오.
- 구조적 유효성 검사에는 `scripts/validate_asset.py`를 사용하십시오.
- 소스 스킬들의 권한, 소유권, 트리거 또는 릴리스 라이프사이클이 서로 무관한 경우 중단하십시오.
- 기존 대상 파일이나 워크플로우를 덮어쓰기 전에 중단하십시오.
- 마이그레이션 모드가 원하는 결과물에 중대한 영향을 미치는 경우 구체적인 질문을 하나 던지십시오.

## Workflow: 스킬 라우팅화 (Routerize Skills)

### Arguments from Context (컨텍스트 인자)

- 둘 이상의 소스 스킬 디렉터리
- 대상 라우팅 스킬 디렉터리
- 마이그레이션 모드: `lite` 또는 `full`

### Procedure (절차)

1. `references/routing-skill-migration.md`를 읽습니다.
2. 소스 스킬들이 동일한 도메인, 최상위 트리거, 리소스 및 릴리스 라이프사이클을 공유하는지 확인합니다. 연관 없는 스킬들은 분리된 상태로 유지합니다.
3. 모드를 선택합니다.

   - `lite`: 각 스킬을 `workflows/<id>/`로 이동하고, `SKILL.md`를 `WORKFLOW.md`로 이름을 바꾸며, 격리된 리소스를 보존합니다.
   - `full`: 각 `SKILL.md`를 `workflows/<id>.md`로 단순화하고, 공유 리소스 파일을 병합하며, 영향을 받는 상대 경로를 수정합니다.

4. 다음 명령을 실행합니다:

   ```bash
   python3 scripts/routerize_skills.py --mode <lite|full> --target <path/to/router> <path/to/skill1> <path/to/skill2>
   ```

5. 자동 생성된 라우트 조건을 실제 사용자 의도에 기반한 의미 있는 `use_when` 및 `excludes` 값으로 대체합니다.
6. 대상을 검증하고 모든 라우트 `id`가 `INDEX.csv`를 기준으로 정상적으로 확인되는지 확인합니다.

### Validation (검증)

- 대상에는 하나의 `SKILL.md`, 기본 `workflows/INDEX.csv` 및 워크플로우 모듈들이 포함되어야 합니다.
- 다른 인덱스 위치는 사용자가 명시적으로 요청한 경우에만 사용합니다.
- 인덱스 스키마는 고유한 상대 경로 ID를 갖는 `id,use_when,excludes`여야 합니다.
- 모든 `id`가 대상 스킬 내부의 워크플로우 파일로 확인되어야 합니다.
- `workflows/` 아래에 중첩된 `SKILL.md`가 남아있어서는 안 됩니다.
- 명확한 요청 시 최소한의 정확한 워크플로우 하나만 로드되어야 합니다. 거의 일치하거나 모호한 요청은 올바르게 라우팅되어야 합니다.

# 라우팅 스킬 마이그레이션 (Routing Skill Migration)

기존 스킬들을 하나의 얕은 라우팅 스킬(Shallow Routing Skill)로 이동시킬 때, 탐색(Discovery) 방식이나 릴리즈 경계(Release boundary)가 실수로 변경되지 않도록 하기 위한 참조 가이드입니다.

## Fit (적합성 검토)

여러 스킬들이 동일한 도메인, 최상위 트리거(Top-level trigger), 참조 리소스, 권한, 소유권 및 릴리즈 라이프사이클을 공유하는 경우에만 마이그레이션하여 하나로 통합합니다. 독립적으로 설치되거나 별도로 버전 관리되는 스킬들은 결합하지 않고 분리해 둡니다.

원하는 구조 레이아웃을 하나 선택합니다:

| 마이그레이션 모드 | 폴더 레이아웃 구조 | 사용 시점 (Use when) |
| --- | --- | --- |
| Flat (평탄화) | `workflows/<name>.md` | 리소스들을 안전하게 공유하거나 이름을 변경할 수 있을 때 |
| Isolated (격리형) | `workflows/<name>/WORKFLOW.md` | 워크플로우가 자체 리소스(스크립트 등)를 독립적으로 묶어두어야 할 때 |

## Flat Migration (평탄화 마이그레이션)

접두사(Prefix)를 붙인 리소스와 함께 평탄화된 워크플로우 구조를 사용하는 것이 좋습니다:

```text
workflows/complex-task.md
scripts/complex-task-validate.py
references/complex-task-spec.md
assets/complex-task-template.yaml
```

리소스를 이동한 후 영향을 받는 모든 상대 경로를 다시 작성합니다. 파일 충돌은 명시적으로 해결해야 하며, 공유 파일을 경고 없이 덮어쓰지 마십시오.

## Isolated Migration (격리형 마이그레이션)

격리가 필요한 경우에는 외부에서 탐색되지 않는 `WORKFLOW.md` 방식을 사용합니다:

```text
workflows/
├── INDEX.csv
└── complex-task/
    ├── WORKFLOW.md
    ├── scripts/
    ├── references/
    └── assets/
```

```csv
id,use_when,excludes
complex-task/WORKFLOW.md,"Complex multi-step processing","Simple single-step requests"
```

하위에 독립적으로 탐색 가능한 `SKILL.md` 파일을 남겨두지 마십시오. 중첩된 탐색 가능 파일은 클라이언트 환경에 따라 워크플로우를 중복 실행시키는 오작동을 유발할 수 있습니다.

## Migration Checks (마이그레이션 체크리스트)

- 통합하는 모든 스킬 소스가 동일한 라우팅 도메인과 라이프사이클에 속해 있는가
- 이동한 각 워크플로우가 `INDEX.csv`를 기준으로 정확한 상대 `id` 경로를 가지는가
- 재작성된 리소스 경로들이 타겟 스킬 내부에서 올바르게 찾아지는가
- 소스나 대상 파일이 아무 조치 없이 덮어씌워지지 않았는가
- 독립적인 스킬 탐색이 필수적인 원래 스킬은 통합하지 않고 별도로 분리해 두었는가

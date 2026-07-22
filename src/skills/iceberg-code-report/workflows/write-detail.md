---
name: write-detail
description: 선택한 핵심 component의 책임, 실행 흐름, 경계, 근거를 별도 문서로 작성한다.
---

# Write Report Detail

## Goal

Summary만으로 부족한 component를 독립적으로 읽을 수 있는 상세 문서로 설명한다.

## Required Inputs

- `summary_file_path`: 기존 `__summary__.md`의 경로.
- `components`: 상세화할 component 목록. 명시 입력이 필요하다.
- `domain`: component 영역을 나타내는 slug.

## Procedure

1. Summary에서 선택한 component의 역할과 근거 link를 확인한다.
2. 각 component에 `<skill-root>/templates/{{domain}}-{{component}}.md`를 적용해 `<domain>-<component>.md`를 생성한다.
3. Responsibility, Execution Flow, Boundaries, Evidence를 실제 symbol, file, test에 근거해 작성한다.
4. Summary의 해당 component 항목을 detail 문서에 연결한다.
5. placeholder와 작성 지침 주석을 제거한다.

## Validation

1. 각 detail 문서에 아래 command를 실행하고 exit code `0`을 확인한다.

   ```bash
   <PYTHON_EXEC> "<skill-root>/scripts/validate_report.py" "<detail_file_path>" --type detail --project-root "<project_root>"
   ```

- 요청한 component마다 detail 문서 하나가 존재한다.
- 각 문서의 code·test link가 유효하고 사실과 추론이 구분됐다.
- Summary에서 각 detail 문서로 가는 상대 link가 유효하다.
- Summary와 detail이 같은 책임이나 흐름을 불필요하게 반복하지 않는다.

## Stop Conditions

- `components`가 명시되지 않으면 모든 component를 임의로 상세화하지 않는다.
- 코드나 설정을 수정하지 않는다.
- 기존 detail 문서를 덮어쓸 권한이 명확하지 않으면 중단한다.

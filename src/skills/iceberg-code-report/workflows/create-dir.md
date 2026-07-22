---
name: create-dir
description: config와 title slug로 code report directory를 생성하고 절대 경로를 반환한다.
---

# Create Report Directory

## Goal

하나의 report bundle을 저장할 directory를 결정적으로 생성한다.

## Required Inputs

- `title_slug`: report 제목의 filesystem-safe slug.
- `project_root`: 기본값은 current working directory.
- `output_path`: 선택. 지정하면 config 기반 경로 계산을 생략한다.

## Procedure

1. `<PYTHON_EXEC> "<skill-root>/scripts/create_report_dir.py" --title-slug "<title_slug>" --project-root "<project_root>" [--output-path "<output_path>"]`를 실행한다.
2. Custom config directory가 있으면 `--project-configs-dir`, `--project-agent-skills-dir`, `--global-agent-skills-dir`를 command에 추가한다.
3. 성공 log의 `Report directory` 절대 경로를 `report_dir`로 반환한다.

## Validation

- `report_dir`이 `project_root` 안에 존재하는 directory다.
- 경로에 치환되지 않은 token이나 `..` segment가 없다.
- 기존 directory가 있어도 내부 파일을 덮어쓰지 않았다.
- Command가 exit code `0`을 반환했다.

## Stop Conditions

- `title_slug`가 비어 있거나 path separator를 포함하면 생성하지 않는다.
- 계산된 경로가 `project_root` 밖이면 생성하지 않는다.

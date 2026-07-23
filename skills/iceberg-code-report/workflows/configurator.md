---
name: configurator
description: iceberg-code-report config를 우선순위에 따라 확인하거나 지정한 값만 수정한다.
---

# Configurator

## Goal

선택된 config를 확인하거나 timezone, 출력 directory, 출력 format을 안전하게 수정한다.

## Required Inputs

- 조회만 할 때 추가 입력 없음.
- 수정할 때 `timezone`, `output_dir`, `output_format` 중 하나 이상.
- custom directory를 쓰면 `project_root`, `project_configs_directory`, `project_agent_skills_directory`, `global_agent_skills_directory`.

## Procedure

1. 조회는 `<PYTHON_EXEC> "<skill-root>/scripts/configurator.py" show`를 실행한다.
2. 수정은 `<PYTHON_EXEC> "<skill-root>/scripts/configurator.py" set [--timezone "<iana_timezone>"] [--output-dir "<relative_directory>"] [--output-format "<format>"]`을 실행한다.
3. custom directory가 있으면 command 앞에 해당 `--project-*` 또는 `--global-agent-skills-dir` option을 추가한다.

## Validation

수정 후 `<PYTHON_EXEC> "<skill-root>/scripts/configurator.py" show`를 실행해 선택된 config와 값을 확인한다.

## Stop Conditions

- 여러 config를 병합하지 않는다.
- 상위 config가 아래 config를 가리는 경우 수정 대상 경로를 먼저 확인한다.

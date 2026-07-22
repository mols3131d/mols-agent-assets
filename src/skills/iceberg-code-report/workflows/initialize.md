---
name: initialize
description: iceberg-code-report의 기본 config를 project override 위치에 생성하거나 초기화한다.
---

# Initialize

## Goal

검증된 기본 config를 생성한다.

## Required Inputs

- `project_root`: 기본값은 current working directory.
- `project_configs_directory`: 선택. 지정하면 `.configs`보다 우선한다.
- `force`: 선택. 기존 config를 기본값으로 덮어쓸 때만 사용한다.

## Procedure

1. `<PYTHON_EXEC> "<skill-root>/scripts/configurator.py" --project-root "<project_root>" [--project-configs-dir "<directory>"] init [--force]`를 실행한다.
2. 기존 config가 있고 `force`가 없으면 값을 보존한다.

## Validation

`<PYTHON_EXEC> "<skill-root>/scripts/configurator.py" --project-root "<project_root>" [--project-configs-dir "<directory>"] show`가 성공해야 한다.

## Stop Conditions

- 기존 config를 덮어쓸 의도가 명확하지 않으면 `--force`를 사용하지 않는다.

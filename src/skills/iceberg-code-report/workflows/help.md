---
name: help
description: iceberg-code-report의 Commander와 Executor가 원하는 사용 정보로 단계적으로 이동하도록 돕는다.
---

# Help

## Goal

CLI의 root·subcommand `--help`처럼 현재 단계에 필요한 정보와 다음 선택지만 보여준다. 전체 사용법을 한 번에 출력하거나 작업을 실행하지 않는다.

## Audience

- **Commander:** 사람, 상위 agent, orchestrator 등 요청 주체가 어떤 명령을 전달하고 어떤 결과를 받는지 확인한다.
- **Executor:** 요청을 수행하는 agent가 어느 workflow로 route하고 어떤 계약을 지켜야 하는지 확인한다.

## Procedure

1. 질문의 현재 깊이를 판별한다.
   - Root: 무엇을 할 수 있는지 묻거나 help만 요청한다.
   - Workflow: `initialize`, `configurator`, `create-dir`, `write-summary`, `write-detail` 중 하나의 사용법을 묻는다.
   - Detail: 특정 input, option, default, output, validation, stop condition을 묻는다.
2. Root에서는 `SKILL.md`와 `workflows/INDEX.csv`만 읽고 목적, 제외 범위, workflow 이름과 한 줄 설명만 제공한다.
3. Workflow에서는 선택한 workflow 하나만 읽고 입력, 기본값, 결과, 요청 예시를 제공한다.
4. Detail에서는 질문한 항목과 직접 관련된 정보만 제공한다.
5. 각 응답 끝에 현재 단계에서 이동 가능한 다음 항목을 짧게 제시한다.
6. 실행 요청이면 도움말을 반복하지 않고 해당 실행 workflow로 route한다.

## Output Contract

- 한 응답은 한 단계만 다루며 전체 workflow 내용을 한 번에 나열하지 않는다.
- Root 응답은 capability 탐색, Workflow 응답은 사용 준비, Detail 응답은 특정 판단에 충분한 정보만 제공한다.
- Commander에게는 선택한 단계에 맞는 자연어 요청 예시를 제공한다.
- Executor에게는 선택한 단계에 필요한 route ID와 실행 계약만 제공한다.
- option, path, command, 기본값은 실제 파일의 표기를 그대로 유지한다.
- 응답 끝에는 `다음:` 형식으로 2~4개의 구체적 탐색 선택지를 제시한다.

## Validation

- 안내한 workflow와 option이 현재 `INDEX.csv`, workflow, script에 존재한다.
- 실제 파일, config, report를 생성하거나 수정하지 않았다.
- Commander와 Executor 관점의 사용법이 모두 포함됐다.
- 요청한 깊이보다 아래 단계의 정보를 미리 펼치지 않았다.

## Stop Conditions

- 문서와 구현이 다르면 추측하지 않고 불일치를 알린다.
- Commander가 “전부”를 요청해도 먼저 capability를 요약하고 세부 topic 선택지를 제시한다.
- 실행 요청은 help와 중복 수행하지 않고 맞는 실행 workflow에 맡긴다.
